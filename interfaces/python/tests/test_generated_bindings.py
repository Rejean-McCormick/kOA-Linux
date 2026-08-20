from __future__ import annotations

import json
import socket
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pytest

from koa_interfaces import (
    SCHEMA_PATHS,
    AvailabilityState,
    CapabilitySnapshot,
    CapabilityState,
    Correlation,
    ErrorCategory,
    ErrorEnvelope,
    EventEnvelope,
    HealthState,
    HealthStatus,
    Idempotency,
    IdentityContext,
    IdentityType,
    InterfaceValidationError,
    JobRequest,
    JobState,
    JobStatus,
    Readiness,
    ReceiptClass,
    ReceiptCommitState,
    ReceiptEnvelope,
    ReceiptOutcome,
    RemoteError,
    SchemaCatalog,
    UnixHttpClient,
    VersionNegotiation,
)

NOW = datetime(2026, 8, 6, 12, 30, tzinfo=timezone.utc)


def _capability() -> CapabilityState:
    return CapabilityState(
        capability_id="local_authoritative_operation",
        health_state=HealthState.HEALTHY,
        availability_state=AvailabilityState.AVAILABLE,
        authority_effect="authoritative_change",
        critical=True,
        usable_operations=("read", "write"),
        capability_ref="docs/contracts/system.contract.json#/global_capabilities/0",
        owner_component_ref="component:test_component",
        capability_class="authoritative_state",
        offline_behavior="continuous",
        observed_at=NOW,
        dependency_observations=(),
    )


def _canonical_readiness(*, ready: bool = True) -> dict[str, Any]:
    observed = NOW.isoformat().replace("+00:00", "Z")
    return {
        "schema_version": "1.0.0",
        "readiness_id": "readiness:test_component:local_read:001",
        "component_id": "test_component",
        "component_contract_ref": "docs/contracts/components/test.component.json",
        "capability_id": "local_read",
        "readiness_class": "readiness.local_read",
        "ready": ready,
        "operational_state": "healthy" if ready else "unavailable",
        "usable_operation_classes": ["read"] if ready else [],
        "denied_operation_classes": [] if ready else ["read"],
        "conditions": [
            {
                "condition_id": "process_alive",
                "category": "process_liveness",
                "required": True,
                "status": "satisfied" if ready else "unsatisfied",
                "observed_at": observed,
                **({} if ready else {"reason_codes": ["PROCESS_UNAVAILABLE"]}),
            }
        ],
        "freshness": {
            "source": "health:test_component",
            "confidence": "direct",
            "staleness_state": "current",
            "observed_at": observed,
            "age_seconds": 0,
        },
        "observed_at": observed,
        "reason_codes": [] if ready else ["PROCESS_UNAVAILABLE"],
    }


def _idempotency(
    key: str,
    *,
    operation: str = "test.work",
    owner_component_id: str = "test_worker",
) -> Idempotency:
    return Idempotency(
        idempotency_key=key,
        request_id="request:test:job:001",
        correlation_id="corr:test:job:001",
        operation=operation,
        owner_component_id=owner_component_id,
        scope={"kind": "owner_operation"},
        canonical_request={
            "algorithm": "sha256",
            "digest": "0" * 64,
            "media_type": "application/json",
        },
        duplicate_handling={
            "action": "return_prior_result",
            "result_consistency": "exact_prior_result",
            "terminal_result_ref_required": True,
        },
        validity={
            "created_at": NOW.isoformat().replace("+00:00", "Z"),
            "retain_terminal_result_seconds": 3600,
        },
        authority={
            "receiving_owner_enforces": True,
            "transport_grants_authority": False,
            "duplicate_effects_permitted": False,
        },
    )


def _error() -> ErrorEnvelope:
    return ErrorEnvelope(
        error_id="error:test:001",
        error_code="dependency_unavailable",
        error_class=ErrorCategory.DEPENDENCY_UNAVAILABLE,
        message="required dependency is unavailable",
        interface={
            "interface_id": "test.health",
            "interface_version": "1.0.0",
            "contract_ref": "docs/contracts/components/test.component.json",
        },
        producer={"component_id": "test-peer"},
        intended_receiver={"kind": "component", "identifier": "test-client"},
        correlation={"correlation_id": "corr:test:001"},
        occurred_at=NOW,
        outcome={
            "state": "blocked",
            "finality": "non_final",
            "authoritative_effect": "unchanged",
        },
        retry={
            "allowed": True,
            "strategy": "bounded_backoff",
            "after_seconds": 1,
            "maximum_attempts": 3,
            "idempotency_required": True,
        },
        reason_codes=("DEPENDENCY_UNAVAILABLE",),
        details={"dependency_ref": "test-peer"},
        disclosure={
            "class": "operator_restricted",
            "payload_minimized": True,
            "contains_secrets": False,
        },
        authority={
            "transport_grants_authority": False,
            "error_grants_authority": False,
            "transfers_ownership": False,
        },
    )


def _identity_context(*, authorization_status: str = "granted") -> IdentityContext:
    observed = NOW.isoformat().replace("+00:00", "Z")
    authority_refs = ["decision:test:001"] if authorization_status == "granted" else []
    return IdentityContext(
        context_id="identity-context:test:001",
        observed_at=NOW,
        actor={
            "identity_id": "service:test-client",
            "subject_type": "service",
            "identity_state": "active",
        },
        subject={
            "identity_id": "subject:test:001",
            "subject_type": "human",
            "identity_state": "active",
        },
        actor_subject_relation="acts_for",
        scope={
            "environment": "test",
            "profile_ref": "profile:test",
            "component_ref": "component:test_worker",
            "capability_id": "test_work",
            "target_ref": "target:test:001",
        },
        authentication={
            "result": "established",
            "authenticated_at": observed,
            "assurance_level": "local_peer_verified",
            "factor_classes": ["service_credential"],
        },
        trust={
            "result": "trusted",
            "verified_at": observed,
            "intended_use": "test_work",
        },
        authority={
            "authorization_status": authorization_status,
            "identity_context_grants_authority": False,
            "authority_refs": authority_refs,
            "policy_decision_refs": [],
            "consent_refs": [],
            "delegation_refs": [],
        },
    )


def _target_scope() -> dict[str, Any]:
    return {
        "component_ref": "component:test_worker",
        "capability_id": "test_work",
        "target_ref": "target:test:001",
        "environment": "test",
        "profile_ref": "profile:test",
    }


def _job_request() -> JobRequest:
    return JobRequest(
        request_id="request:test:job:001",
        workload_owner_ref="component:test_worker",
        workload_class="test_work",
        target_scope=_target_scope(),
        criticality={"profile_criticality": "normal", "component_criticality": "normal"},
        priority={"class": "background", "rank": 100},
        resource_request={"cpu_millicores": 100, "memory_bytes": 1_048_576},
        submitted_at=NOW,
        execution_semantics={
            "schedule_class": "immediate",
            "delivery_semantics": "at_least_once",
            "idempotent_or_duplicate_safe": True,
            "interruptible": True,
            "authoritative_commit_owner_ref": "component:test_worker",
            "scheduler_acknowledgement_is_completion": False,
        },
        identity_context=_identity_context(),
        correlation=Correlation("corr:test:job:001", request_id="request:test:job:001"),
        idempotency=_idempotency("idem:test:job:001", operation="test_work"),
        input={
            "contract_ref": "urn:koa:test:job-payload:1",
            "media_type": "application/json",
            "payload": {"work": "bounded"},
        },
    )


def _submitted_status(*, correlation: Correlation | None = None) -> JobStatus:
    corr = correlation or Correlation("corr:test:job:001", request_id="request:test:job:001")
    observed = NOW.isoformat().replace("+00:00", "Z")
    return JobStatus(
        status_id="status:test:job:001",
        request_id="request:test:job:001",
        workload_owner_ref="component:test_worker",
        target_scope=_target_scope(),
        observed_at=NOW,
        current_state=JobState.SUBMITTED,
        state_entered_at=NOW,
        terminal=False,
        transition={
            "from_state": None,
            "to_state": "submitted",
            "transitioned_at": observed,
            "reason_codes": [],
        },
        attempt_count=0,
        authoritative_outcome="no_effect",
        correlation=corr,
        receipt_refs=(),
    )


def test_error_envelope_round_trip_uses_canonical_schema_shape() -> None:
    error = _error()
    encoded = error.to_dict()
    assert encoded["schema_version"] == "1.0.0"
    assert encoded["envelope_type"] == "error"
    assert encoded["error_code"] == "dependency_unavailable"
    assert encoded["error_class"] == "dependency"
    assert "code" not in encoded
    assert "category" not in encoded
    assert "disposition" not in encoded
    assert ErrorEnvelope.from_dict(encoded) == error


def test_schema_catalog_resolves_all_dependency_owned_schema_identifiers(tmp_path: Path) -> None:
    assert len(SCHEMA_PATHS) == 12
    for index, relative in enumerate(SCHEMA_PATHS.values(), start=1):
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(
                {
                    "$schema": "https://json-schema.org/draft/2020-12/schema",
                    "$id": f"https://schemas.koa.local/common/{index}.schema.json",
                    "title": relative,
                    "type": "object",
                }
            ),
            encoding="utf-8",
        )
    catalog = SchemaCatalog.from_repository(tmp_path)
    assert catalog.canonical_id("event_envelope").endswith("/1.schema.json")
    assert catalog.bindings["job_status"].repository_path == SCHEMA_PATHS["job_status"]


def test_schema_catalog_fails_closed_when_a_dependency_schema_is_missing(tmp_path: Path) -> None:
    with pytest.raises(InterfaceValidationError, match="missing dependency schema"):
        SchemaCatalog.from_repository(tmp_path)


def test_idempotency_round_trip_uses_canonical_schema_shape() -> None:
    context = _idempotency("idem:test:001")
    encoded = context.to_dict()
    assert encoded["schema_version"] == "1.0.0"
    assert encoded["idempotency_key"] == "idem:test:001"
    assert encoded["duplicate_handling"]["action"] == "return_prior_result"
    assert encoded["authority"]["receiving_owner_enforces"] is True
    assert "required" not in encoded
    assert "key" not in encoded
    assert Idempotency.from_dict(encoded) == context


def _event(**overrides: Any) -> EventEnvelope:
    values: dict[str, Any] = {
        "message_id": "message:test:001",
        "event_id": "EVENT-TEST-001",
        "event_type": "test.fact_committed",
        "event_version": "1.0.0",
        "interface": {
            "interface_id": "test.events",
            "interface_version": "1.0.0",
            "contract_ref": "docs/contracts/components/test.component.json",
        },
        "publisher": {"component_id": "source_component"},
        "intended_receivers": (
            {"kind": "component", "identifier": "target_component"},
        ),
        "correlation": Correlation(
            correlation_id="corr:test:001",
            request_id="request:test:001",
            causation_id="event:test:000",
        ),
        "occurred_at": NOW,
        "committed_at": NOW,
        "payload_representation": {
            "media_type": "application/json",
            "schema_ref": "https://schemas.koa.local/test-payload.schema.json",
            "schema_version": "1.0.0",
            "encoding": "identity",
        },
        "payload": {"value": 7},
        "ordering": {
            "scope": "test.subject",
            "sequence": 1,
            "partition_key": "subject:test:001",
        },
        "replay": {"mode": "original", "duplicate_handling": "ignore_if_applied"},
        "disclosure": {"class": "operator_restricted", "payload_minimized": True},
        "authority": {
            "effect": "committed_fact_evidence",
            "publisher_owns_fact": True,
            "grants_mutation_authority": False,
            "transfers_ownership": False,
        },
        "evidence": {"evidence_refs": ["evidence:test:001"]},
    }
    values.update(overrides)
    return EventEnvelope(**values)


def test_event_round_trip_preserves_canonical_domain_event_fields() -> None:
    event = _event()
    encoded = event.to_dict()
    assert encoded["envelope_type"] == "domain_event"
    assert encoded["interface"]["interface_version"] == "1.0.0"
    assert encoded["authority"]["grants_mutation_authority"] is False
    assert EventEnvelope.from_dict(encoded) == event


def test_event_replay_requires_original_identity_and_timestamp() -> None:
    with pytest.raises(InterfaceValidationError, match="replay mode missing fields"):
        _event(replay={"mode": "replay", "duplicate_handling": "ignore_if_applied"})


def _version_offer() -> VersionNegotiation:
    return VersionNegotiation(
        message_type="version_offer",
        negotiation_id="negotiation:test:001",
        interface_id="test.command",
        sender={"component_id": "test_client"},
        intended_receiver={"kind": "component", "identifier": "test_server"},
        correlation_id="corr:test:001",
        offered_versions=("2.0.0", "1.1.0", "1.0.0"),
        preferred_version="1.1.0",
        authority={
            "transport_grants_authority": False,
            "selection_changes_domain_authority": False,
            "receiving_contract_remains_authoritative": True,
        },
    )


def test_version_negotiation_round_trip_uses_canonical_message_shape() -> None:
    offer = _version_offer()
    encoded = offer.to_dict()
    assert encoded["message_type"] == "version_offer"
    assert encoded["offered_versions"] == ["2.0.0", "1.1.0", "1.0.0"]
    assert encoded["preferred_version"] == "1.1.0"
    assert encoded["automatic_schema_guessing"] is False
    assert VersionNegotiation.from_dict(encoded) == offer
    assert offer.select(("1.0.0", "1.1.0")) == "1.1.0"
    with pytest.raises(InterfaceValidationError, match="no mutually supported"):
        offer.select(("0.9.0",))


def test_version_selection_must_select_an_explicitly_offered_version() -> None:
    with pytest.raises(InterfaceValidationError, match="selected_version must be present"):
        VersionNegotiation(
            message_type="version_selection",
            negotiation_id="negotiation:test:001",
            interface_id="test.command",
            sender={"component_id": "test_server"},
            intended_receiver={"kind": "component", "identifier": "test_client"},
            correlation_id="corr:test:001",
            offered_versions=("1.0.0", "1.1.0"),
            selected_version="2.0.0",
            compatibility_mode="exact",
            authority={
                "transport_grants_authority": False,
                "selection_changes_domain_authority": False,
                "receiving_contract_remains_authoritative": True,
            },
        )


def test_identity_context_does_not_conflate_authentication_and_authority() -> None:
    context = _identity_context(authorization_status="not_evaluated")
    assert context.authenticated
    assert context.authority_refs == ()
    assert context.to_dict()["grants_action_authority"] is False
    observed = NOW.isoformat().replace("+00:00", "Z")
    with pytest.raises(InterfaceValidationError, match="identity_context_grants_authority"):
        IdentityContext(
            context_id="identity-context:test:invalid",
            observed_at=NOW,
            actor={"identity_id": "service:test-client", "subject_type": "service", "identity_state": "active"},
            subject={"identity_id": "subject:test:001", "subject_type": "human", "identity_state": "active"},
            actor_subject_relation="acts_for",
            scope=_target_scope(),
            authentication={
                "result": "established", "authenticated_at": observed,
                "assurance_level": "local_peer_verified", "factor_classes": ["service_credential"],
            },
            trust={"result": "trusted", "verified_at": observed, "intended_use": "test_work"},
            authority={
                "authorization_status": "granted",
                "identity_context_grants_authority": True,
                "authority_refs": ["decision:test:001"],
                "policy_decision_refs": [], "consent_refs": [], "delegation_refs": [],
            },
        )


def test_health_round_trip_preserves_canonical_liveness_and_readiness() -> None:
    status = HealthStatus(
        component_id="test_component",
        observed_at=NOW,
        health_report_id="health:test_component:001",
        component_instance_id="instance:test:001",
        component_contract_ref="docs/contracts/components/test.component.json",
        process_liveness={
            "state": "alive",
            "observed_at": NOW.isoformat().replace("+00:00", "Z"),
            "reason_codes": [],
        },
        startup={
            "state": "healthy",
            "observed_at": NOW.isoformat().replace("+00:00", "Z"),
            "reason_codes": [],
        },
        overall_state=HealthState.HEALTHY,
        readiness=(_canonical_readiness(),),
        freshness={
            "source": "health:test_component",
            "confidence": "direct",
            "staleness_state": "current",
            "observed_at": NOW.isoformat().replace("+00:00", "Z"),
            "age_seconds": 0,
        },
        disclosure_class="machine_readable_local",
    )
    encoded = status.to_dict()
    assert encoded["process_liveness"]["state"] == "alive"
    assert encoded["overall_state"] == "healthy"
    assert encoded["readiness"][0]["readiness_class"] == "readiness.local_read"
    assert "capabilities" not in encoded
    assert "startup_complete" not in encoded
    assert HealthStatus.from_dict(encoded).to_dict() == encoded


def test_failed_process_liveness_cannot_hide_aggregate_failure() -> None:
    with pytest.raises(InterfaceValidationError, match="overall_state=failed"):
        HealthStatus(
            component_id="test_component",
            observed_at=NOW,
            health_report_id="health:test_component:002",
            component_contract_ref="docs/contracts/components/test.component.json",
            process_liveness={
                "state": "failed",
                "observed_at": NOW.isoformat().replace("+00:00", "Z"),
                "reason_codes": ["PROCESS_FAILED"],
            },
            startup={
                "state": "failed",
                "observed_at": NOW.isoformat().replace("+00:00", "Z"),
                "reason_codes": ["PROCESS_FAILED"],
            },
            overall_state=HealthState.DEGRADED,
            readiness=(_canonical_readiness(ready=False),),
            freshness={
                "source": "health:test_component",
                "confidence": "direct",
                "staleness_state": "current",
                "observed_at": NOW.isoformat().replace("+00:00", "Z"),
                "age_seconds": 0,
            },
            reason_codes=("PROCESS_FAILED",),
            disclosure_class="machine_readable_local",
        )


def test_legacy_boolean_fields_fail_closed_instead_of_using_truthiness() -> None:
    with pytest.raises(InterfaceValidationError, match="startup_complete must be a boolean"):
        HealthStatus.from_dict(
            {
                "component_id": "test_component",
                "instance_id": "instance:test:001",
                "state": "healthy",
                "observed_at": "2026-08-06T12:30:00Z",
                "contract_version": "1.0.0",
                "schema_version": "1.0.0",
                "capabilities": [_capability().to_dict()],
                "startup_complete": "false",
                "freshness_seconds": 5,
            }
        )


def test_readiness_requires_explicit_usable_or_denied_operation_classes() -> None:
    ready = Readiness.from_dict(_canonical_readiness())
    assert Readiness.from_dict(ready.to_dict()) == ready

    blocked = _canonical_readiness(ready=False)
    blocked["denied_operation_classes"] = []
    with pytest.raises(InterfaceValidationError, match="denied_operation_classes"):
        Readiness.from_dict(blocked)


def test_receipt_round_trip_separates_commit_from_transport_success() -> None:
    receipt = ReceiptEnvelope(
        receipt_id="receipt:test:001",
        receipt_schema_version="1.0.0",
        receipt_class=ReceiptClass.TRANSITION,
        transition_type="test_state_change",
        producer_component_id="test_component",
        subject_ref="subject:test:001",
        actor_ref="service:test-client",
        target_refs=("target:test:001",),
        scope={"kind": "component", "id": "test_component"},
        requested_action="test_state_change",
        correlation=Correlation("corr:test:001", request_id="request:test:001"),
        authority_refs=("decision:test:001",),
        decision="authorized",
        execution_state="completed",
        commit_state=ReceiptCommitState.COMMITTED,
        outcome=ReceiptOutcome.COMMITTED,
        requested_at=NOW,
        completed_at=NOW,
        committed_at=NOW,
        recorded_at=NOW,
        reason_codes=(),
        component_contract_refs=("docs/contracts/components/test.component.json",),
    )
    encoded = receipt.to_dict()
    assert encoded["schema_version"] == "1.0.0"
    assert encoded["correlation"]["schema_version"] == "1.0.0"
    assert encoded["scope"] == {"kind": "component", "id": "test_component"}
    assert "correlation_id" not in encoded
    assert "request_id" not in encoded
    assert "extensions" not in encoded
    assert "reason_code" not in encoded
    assert ReceiptEnvelope.from_dict(encoded) == receipt

    with pytest.raises(InterfaceValidationError, match="commit_state"):
        ReceiptEnvelope(
            receipt_id="receipt:test:002",
            receipt_schema_version="1.0.0",
            receipt_class=ReceiptClass.TRANSITION,
            transition_type="test_state_change",
            producer_component_id="test_component",
            subject_ref="subject:test:001",
            actor_ref="service:test-client",
            target_refs=("target:test:001",),
            scope={"kind": "component", "id": "test_component"},
            requested_action="test_state_change",
            correlation=Correlation("corr:test:002"),
            authority_refs=("decision:test:001",),
            decision="authorized",
            execution_state="completed",
            commit_state=ReceiptCommitState.NOT_COMMITTED,
            outcome=ReceiptOutcome.COMMITTED,
            requested_at=NOW,
            completed_at=NOW,
            committed_at=NOW,
            recorded_at=NOW,
            reason_codes=(),
            component_contract_refs=("docs/contracts/components/test.component.json",),
        )

def test_job_request_requires_idempotency_and_job_status_is_explicit() -> None:
    request = _job_request()
    encoded_request = request.to_dict()
    assert encoded_request["request_id"] == "request:test:job:001"
    assert encoded_request["execution_semantics"]["scheduler_acknowledgement_is_completion"] is False
    assert JobRequest.from_dict(encoded_request) == request

    observed = NOW.isoformat().replace("+00:00", "Z")
    status = JobStatus(
        status_id="status:test:job:completed:001",
        request_id=request.request_id,
        workload_owner_ref=request.workload_owner_ref,
        target_scope=request.target_scope,
        observed_at=NOW,
        current_state=JobState.COMPLETED,
        state_entered_at=NOW,
        terminal=True,
        transition={
            "from_state": "running", "to_state": "completed",
            "transitioned_at": observed, "reason_codes": [],
        },
        attempt_count=1,
        attempt={
            "attempt_id": "attempt:test:001", "attempt_number": 1,
            "state": "completed", "started_at": observed, "ended_at": observed,
        },
        authoritative_outcome="no_effect",
        result={
            "result_id": "result:test:001",
            "owner_result_ref": "owner-result:test:001",
            "owner_verified": True,
            "scheduler_synthesized": False,
            "recorded_at": observed,
        },
        progress=1.0,
        correlation=request.correlation,
        receipt_refs=(),
    )
    assert status.terminal
    assert JobStatus.from_dict(status.to_dict()) == status
    with pytest.raises(InterfaceValidationError, match="failed job must contain failure"):
        JobStatus(
            status_id="status:test:job:failed:001",
            request_id=request.request_id,
            workload_owner_ref=request.workload_owner_ref,
            target_scope=request.target_scope,
            observed_at=NOW,
            current_state=JobState.FAILED,
            state_entered_at=NOW,
            terminal=True,
            transition={
                "from_state": "running", "to_state": "failed",
                "transitioned_at": observed, "reason_codes": ["execution_failed"],
            },
            attempt_count=1,
            attempt={
                "attempt_id": "attempt:test:002", "attempt_number": 1,
                "state": "failed", "started_at": observed, "ended_at": observed,
            },
            authoritative_outcome="no_effect",
            correlation=request.correlation,
            receipt_refs=(),
        )


def test_capability_snapshot_round_trip_uses_canonical_schema_shape() -> None:
    snapshot = CapabilitySnapshot(
        snapshot_id="snapshot:test:001",
        producer_component_ref="component:test_component",
        observed_at=NOW,
        profile_ref="profile:user_lightweight",
        scope={"environment": "test", "component_ref": "component:test_component"},
        capabilities=(_capability(),),
        correlation=Correlation(
            "corr:test:capability:001", request_id="request:test:capability:001"
        ).to_dict(),
    )
    encoded = snapshot.to_dict()
    assert encoded["schema_version"] == "1.0.0"
    assert encoded["substitution_applied"] is False
    assert encoded["capabilities"][0]["availability_state"] == "available"
    assert "health_state" not in encoded["capabilities"][0]
    assert CapabilitySnapshot.from_dict(encoded).to_dict() == encoded


def test_capability_snapshot_rejects_duplicate_capability_ids() -> None:
    with pytest.raises(InterfaceValidationError, match="must be unique"):
        CapabilitySnapshot(
            snapshot_id="snapshot:test:duplicate:001",
            producer_component_ref="component:test_component",
            observed_at=NOW,
            profile_ref="profile:user_lightweight",
            scope={"environment": "test", "component_ref": "component:test_component"},
            capabilities=(_capability(), _capability()),
            correlation=Correlation("corr:test:capability:duplicate:001").to_dict(),
        )


class _OneShotUnixServer:
    def __init__(self, socket_path: Path, status: int, response: dict[str, Any]) -> None:
        self.socket_path = socket_path
        self.status = status
        self.response = response
        self.request_head = ""
        self._thread = threading.Thread(target=self._serve, daemon=True)
        self._ready = threading.Event()

    def start(self) -> None:
        self._thread.start()
        assert self._ready.wait(timeout=2)

    def join(self) -> None:
        self._thread.join(timeout=2)
        assert not self._thread.is_alive()

    def _serve(self) -> None:
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(str(self.socket_path))
        server.listen(1)
        self._ready.set()
        try:
            connection, _ = server.accept()
            with connection:
                chunks = bytearray()
                while b"\r\n\r\n" not in chunks:
                    chunk = connection.recv(4096)
                    if not chunk:
                        break
                    chunks.extend(chunk)
                head, _, remainder = bytes(chunks).partition(b"\r\n\r\n")
                self.request_head = head.decode("iso-8859-1")
                content_length = 0
                for line in self.request_head.split("\r\n")[1:]:
                    name, _, value = line.partition(":")
                    if name.lower() == "content-length":
                        content_length = int(value.strip())
                while len(remainder) < content_length:
                    remainder += connection.recv(content_length - len(remainder))
                body = json.dumps(self.response, separators=(",", ":")).encode("utf-8")
                reason = "OK" if self.status < 400 else "Error"
                response_head = (
                    f"HTTP/1.1 {self.status} {reason}\r\n"
                    "Content-Type: application/json\r\n"
                    f"Content-Length: {len(body)}\r\n"
                    "Connection: close\r\n\r\n"
                ).encode("ascii")
                connection.sendall(response_head + body)
        finally:
            server.close()


@pytest.mark.skipif(
    not hasattr(socket, "AF_UNIX"),
    reason="AF_UNIX is unavailable on this Python/Windows build",
)
def test_unix_http_client_sends_correlation_without_implicit_retry(tmp_path: Path) -> None:
    socket_path = tmp_path / "service.sock"
    response = _submitted_status().to_dict()
    server = _OneShotUnixServer(socket_path, 202, response)
    server.start()
    client = UnixHttpClient(socket_path, sender="test_client")
    request = _job_request()
    status = client.submit_job(request)
    server.join()
    assert status.state is JobState.SUBMITTED
    assert "X-Correlation-ID: corr:test:job:001" in server.request_head
    assert "Idempotency-Key: idem:test:job:001" in server.request_head


@pytest.mark.skipif(
    not hasattr(socket, "AF_UNIX"),
    reason="AF_UNIX is unavailable on this Python/Windows build",
)
def test_unix_http_client_raises_typed_remote_error(tmp_path: Path) -> None:
    socket_path = tmp_path / "service.sock"
    server = _OneShotUnixServer(socket_path, 503, _error().to_dict())
    server.start()
    client = UnixHttpClient(socket_path, sender="test_client")
    with pytest.raises(RemoteError) as captured:
        client.request("GET", "/health")
    server.join()
    assert captured.value.status == 503
    assert captured.value.envelope.retryable
