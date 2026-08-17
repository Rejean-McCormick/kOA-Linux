"""Cross-check the public Python bindings against dependency-owned schemas."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

koa_interfaces = pytest.importorskip("koa_interfaces", reason="B-0017 Python bindings are absent")

from koa_interfaces import (  # noqa: E402
    SCHEMA_PATHS,
    AuthoritativeOutcome,
    AvailabilityState,
    CapabilityExecutionState,
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
    JobRequest,
    JobState,
    JobStatus,
    Readiness,
    ReadinessClass,
    ReceiptClass,
    ReceiptCommitState,
    ReceiptEnvelope,
    ReceiptOutcome,
    SchemaCatalog,
    VersionNegotiation,
)

NOW = datetime(2026, 8, 6, 16, 0, 0, tzinfo=timezone.utc)
EXPECTED_SCHEMA_PATHS = {
    "event_envelope": "interfaces/transport/event-envelope.schema.json",
    "error_envelope": "interfaces/transport/error-envelope.schema.json",
    "idempotency": "interfaces/transport/idempotency.schema.json",
    "version_negotiation": "interfaces/transport/version-negotiation.schema.json",
    "health_status": "interfaces/health/health-status.schema.json",
    "readiness": "interfaces/health/readiness.schema.json",
    "receipt_envelope": "interfaces/receipts/receipt-envelope.schema.json",
    "correlation": "interfaces/receipts/correlation.schema.json",
    "job_request": "interfaces/jobs/job-request.schema.json",
    "job_status": "interfaces/jobs/job-status.schema.json",
    "identity_context": "interfaces/identity/identity-context.schema.json",
    "capability_snapshot": "interfaces/capabilities/capability-snapshot.schema.json",
}


def _capability() -> CapabilityState:
    return CapabilityState(
        capability_id="test.read",
        health_state=HealthState.HEALTHY,
        availability_state=AvailabilityState.AVAILABLE,
        execution_state=CapabilityExecutionState.COMPLETED,
        authoritative_outcome=AuthoritativeOutcome.CHANGE_COMMITTED,
        authority_effect="authoritative_change",
        critical=True,
        usable_operations=("read",),
    )



def _health_readiness_sample() -> dict[str, object]:
    observed = NOW.isoformat().replace("+00:00", "Z")
    return {
        "schema_version": "1.0.0",
        "readiness_id": "readiness:test_component:local_read:001",
        "component_id": "test_component",
        "component_contract_ref": "docs/contracts/components/test.component.json",
        "capability_id": "local_read",
        "readiness_class": "readiness.local_read",
        "ready": True,
        "operational_state": "healthy",
        "usable_operation_classes": ["read"],
        "denied_operation_classes": [],
        "conditions": [
            {
                "condition_id": "process_alive",
                "category": "process_liveness",
                "required": True,
                "status": "satisfied",
                "observed_at": observed,
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
        "reason_codes": [],
    }

def _samples() -> dict[str, dict]:
    correlation = Correlation("corr:test:001", request_id="request:test:001")
    identity = IdentityContext(
        actor_ref="service:test-client",
        subject_ref="subject:test:001",
        identity_type=IdentityType.SERVICE,
        authenticated=True,
        assurance_level="local_peer_verified",
        authority_refs=("decision:test:001",),
    )
    idempotency = Idempotency(
        idempotency_key="idem:test:001",
        request_id="request:test:001",
        correlation_id=correlation.correlation_id,
        operation="test.work",
        owner_component_id="test_worker",
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
    error = ErrorEnvelope(
        error_id="error:test:001",
        error_code="dependency_unavailable",
        error_class=ErrorCategory.DEPENDENCY_UNAVAILABLE,
        message="required dependency is unavailable",
        interface={
            "interface_id": "test.errors",
            "interface_version": "1.0.0",
            "contract_ref": "docs/contracts/components/test.component.json",
        },
        producer={"component_id": "test_source"},
        intended_receiver={"kind": "component", "identifier": "test_target"},
        correlation=correlation.to_dict(),
        occurred_at=NOW,
        outcome={
            "state": "blocked",
            "finality": "non_final",
            "authoritative_effect": "unchanged",
        },
        retry={
            "allowed": True,
            "strategy": "status_resolution",
            "idempotency_required": True,
        },
        reason_codes=("DEPENDENCY_UNAVAILABLE",),
        details={"dependency_ref": "test_dependency"},
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
    capability = _capability()
    return {
        "event_envelope": EventEnvelope(
            message_id="message:test:001",
            event_id="event:test:001",
            event_type="test.fact_committed",
            event_version="1.0.0",
            interface={
                "interface_id": "test.events",
                "interface_version": "1.0.0",
                "contract_ref": "docs/contracts/components/test.component.json",
            },
            publisher={"component_id": "test_source"},
            intended_receivers=(
                {"kind": "component", "identifier": "test_target"},
            ),
            correlation=correlation,
            occurred_at=NOW,
            committed_at=NOW,
            payload_representation={
                "media_type": "application/json",
                "schema_ref": "urn:koa:test:payload:1",
                "schema_version": "1.0.0",
                "encoding": "identity",
            },
            payload={"value": 1},
            ordering={
                "scope": "test.subject",
                "sequence": 1,
                "partition_key": "subject:test:001",
            },
            replay={"mode": "original", "duplicate_handling": "ignore_if_applied"},
            disclosure={"class": "operator_restricted", "payload_minimized": True},
            authority={
                "effect": "committed_fact_evidence",
                "publisher_owns_fact": True,
                "grants_mutation_authority": False,
                "transfers_ownership": False,
            },
        ).to_dict(),
        "error_envelope": error.to_dict(),
        "idempotency": idempotency.to_dict(),
        "version_negotiation": VersionNegotiation(
            message_type="version_selection",
            negotiation_id="negotiation:test:001",
            interface_id="test.command",
            sender={"component_id": "test_source"},
            intended_receiver={"kind": "component", "identifier": "test_target"},
            correlation_id=correlation.correlation_id,
            offered_versions=("1.0.0",),
            selected_version="1.0.0",
            compatibility_mode="exact",
            authority={
                "transport_grants_authority": False,
                "selection_changes_domain_authority": False,
                "receiving_contract_remains_authoritative": True,
            },
        ).to_dict(),
        "health_status": HealthStatus(
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
            readiness=(_health_readiness_sample(),),
            freshness={
                "source": "health:test_component",
                "confidence": "direct",
                "staleness_state": "current",
                "observed_at": NOW.isoformat().replace("+00:00", "Z"),
                "age_seconds": 0,
            },
            disclosure_class="machine_readable_local",
        ).to_dict(),
        "readiness": Readiness(
            component_id="test_component",
            readiness_class=ReadinessClass.LOCAL_READ,
            state=HealthState.HEALTHY,
            accepting_work=True,
            observed_at=NOW,
            usable_operations=("read",),
        ).to_dict(),
        "receipt_envelope": ReceiptEnvelope(
            receipt_id="receipt:test:001",
            receipt_schema_version="1.0.0",
            receipt_class=ReceiptClass.TRANSITION,
            transition_type="test_state_change",
            producer_component_id="test_component",
            subject_ref="subject:test:001",
            scope="component:test_component",
            correlation=correlation,
            outcome=ReceiptOutcome.COMMITTED,
            commit_state=ReceiptCommitState.COMMITTED,
            requested_at=NOW,
            committed_at=NOW,
            recorded_at=NOW,
            authority_refs=("decision:test:001",),
        ).to_dict(),
        "correlation": correlation.to_dict(),
        "job_request": JobRequest(
            job_id="job:test:001",
            job_type="test.work",
            interface_version="1.0.0",
            sender="test_client",
            intended_receiver="test_worker",
            payload_schema="urn:koa:test:job-payload:1",
            payload={"operation": "bounded"},
            created_at=NOW,
            correlation=correlation,
            idempotency=idempotency,
            identity_context=identity,
        ).to_dict(),
        "job_status": JobStatus(
            job_id="job:test:001",
            state=JobState.COMPLETED,
            observed_at=NOW,
            correlation_id=correlation.correlation_id,
            progress=100,
            result={"outcome": "no_effect"},
        ).to_dict(),
        "identity_context": identity.to_dict(),
        "capability_snapshot": CapabilitySnapshot(
            snapshot_id="snapshot:test:001",
            component_id="test_component",
            observed_at=NOW,
            contract_version="1.0.0",
            capabilities=(capability,),
            profile_refs=("profile:user_lightweight",),
        ).to_dict(),
    }


def test_binding_schema_path_inventory_is_exact() -> None:
    assert dict(SCHEMA_PATHS) == EXPECTED_SCHEMA_PATHS
    assert set(_samples()) == set(EXPECTED_SCHEMA_PATHS)


def test_binding_round_trips_are_deterministic() -> None:
    samples = _samples()
    assert ErrorEnvelope.from_dict(samples["error_envelope"]).to_dict() == samples["error_envelope"]
    assert Correlation.from_dict(samples["correlation"]).to_dict() == samples["correlation"]
    assert Idempotency.from_dict(samples["idempotency"]).to_dict() == samples["idempotency"]
    assert VersionNegotiation.from_dict(samples["version_negotiation"]).to_dict() == samples["version_negotiation"]
    assert HealthStatus.from_dict(samples["health_status"]).to_dict() == samples["health_status"]


def test_binding_payloads_validate_when_dependency_schemas_are_present(
    repository_root: Path, load_json, draft_2020_validator
) -> None:
    missing = [relative for relative in EXPECTED_SCHEMA_PATHS.values() if not (repository_root / relative).is_file()]
    if missing:
        pytest.skip("B-0014 to B-0016 schemas are not integrated: " + ", ".join(missing))
    catalog = SchemaCatalog.from_repository(repository_root)
    samples = _samples()
    for logical_name, relative in EXPECTED_SCHEMA_PATHS.items():
        schema = load_json(repository_root / relative)
        draft_2020_validator(schema).validate(samples[logical_name])
        assert catalog.bindings[logical_name].repository_path == relative
