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
    DeliveryGuarantee,
    DuplicateOutcome,
    ErrorCategory,
    ErrorDisposition,
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
    Ordering,
    Readiness,
    ReadinessClass,
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
    )


def _error() -> ErrorEnvelope:
    return ErrorEnvelope(
        error_id="error:test:001",
        code="dependency_unavailable",
        category=ErrorCategory.DEPENDENCY_UNAVAILABLE,
        message="required dependency is unavailable",
        disposition=ErrorDisposition.RETRY_SAME_REQUEST,
        observed_at=NOW,
        correlation_id="corr:test:001",
        reason_codes=("dependency_unavailable",),
        details={"dependency": "test-peer"},
    )


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


def test_event_round_trip_preserves_correlation_ordering_and_idempotency() -> None:
    event = EventEnvelope(
        event_id="EVENT-TEST-001",
        event_type="test.fact_committed",
        interface_version="1.0.0",
        sender="source_component",
        intended_receiver="target_component",
        payload_schema="https://schemas.koa.local/test-payload.schema.json",
        payload={"value": 7},
        created_at=NOW,
        correlation=Correlation(
            correlation_id="corr:test:001",
            request_id="request:test:001",
            causation_id="event:test:000",
        ),
        delivery_guarantee=DeliveryGuarantee.EFFECTIVELY_ONCE,
        ordering=Ordering.PER_KEY,
        ordering_key="subject:test:001",
        idempotency=Idempotency(
            required=True,
            key="idem:test:001",
            duplicate_outcome=DuplicateOutcome.RETURN_PRIOR_RESULT,
            retention_rule="retain for the component contract period",
        ),
        evidence_refs=("evidence:test:001",),
    )
    assert EventEnvelope.from_dict(event.to_dict()) == event


def test_event_rejects_per_key_ordering_without_key() -> None:
    with pytest.raises(InterfaceValidationError, match="ordering_key"):
        EventEnvelope(
            event_id="EVENT-TEST-001",
            event_type="test.fact_committed",
            interface_version="1.0.0",
            sender="source_component",
            intended_receiver="target_component",
            payload_schema="schema:test",
            payload={},
            created_at=NOW,
            correlation=Correlation("corr:test:001"),
            delivery_guarantee=DeliveryGuarantee.AT_LEAST_ONCE,
            ordering=Ordering.PER_KEY,
        )


def test_version_negotiation_selects_first_local_preference() -> None:
    binding = VersionNegotiation(("2.0.0", "1.1.0", "1.0.0"))
    assert binding.select(("1.0.0", "1.1.0")) == "1.1.0"
    with pytest.raises(InterfaceValidationError, match="no mutually supported"):
        binding.select(("0.9.0",))


def test_identity_context_does_not_conflate_authentication_and_authority() -> None:
    with pytest.raises(InterfaceValidationError, match="cannot assert authority"):
        IdentityContext(
            actor_ref="service:test",
            subject_ref="subject:test",
            identity_type=IdentityType.SERVICE,
            authenticated=False,
            assurance_level="none",
            authority_refs=("decision:test",),
        )


def test_health_round_trip_preserves_per_capability_state() -> None:
    status = HealthStatus(
        component_id="test_component",
        instance_id="instance:test:001",
        state=HealthState.HEALTHY,
        observed_at=NOW,
        contract_version="1.0.0",
        schema_version="1.0.0",
        capabilities=(_capability(),),
        startup_complete=True,
        freshness_seconds=5,
    )
    assert HealthStatus.from_dict(status.to_dict()) == status


def test_aggregate_health_cannot_hide_failed_critical_capability() -> None:
    capability = CapabilityState(
        capability_id="critical_write",
        health_state=HealthState.UNAVAILABLE,
        availability_state=AvailabilityState.UNAVAILABLE,
        critical=True,
        denied_operations=("write",),
        reason_codes=("trust_unavailable",),
    )
    with pytest.raises(InterfaceValidationError, match="cannot hide"):
        HealthStatus(
            component_id="test_component",
            instance_id="instance:test:001",
            state=HealthState.HEALTHY,
            observed_at=NOW,
            contract_version="1.0.0",
            schema_version="1.0.0",
            capabilities=(capability,),
            startup_complete=True,
            freshness_seconds=5,
        )


def test_boolean_fields_fail_closed_instead_of_using_truthiness() -> None:
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


def test_readiness_requires_explicit_usable_or_denied_operations() -> None:
    ready = Readiness(
        component_id="test_component",
        readiness_class=ReadinessClass.LOCAL_READ,
        state=HealthState.READ_ONLY,
        accepting_work=True,
        observed_at=NOW,
        usable_operations=("read",),
        denied_operations=("write",),
    )
    assert Readiness.from_dict(ready.to_dict()) == ready
    with pytest.raises(InterfaceValidationError, match="denied_operations"):
        Readiness(
            component_id="test_component",
            readiness_class=ReadinessClass.AUTHORITATIVE_WRITE,
            state=HealthState.UNAVAILABLE,
            accepting_work=False,
            observed_at=NOW,
        )


def test_receipt_round_trip_separates_commit_from_transport_success() -> None:
    receipt = ReceiptEnvelope(
        receipt_id="receipt:test:001",
        receipt_schema_version="1.0.0",
        receipt_class=ReceiptClass.TRANSITION,
        transition_type="test_state_change",
        producer_component_id="test_component",
        subject_ref="subject:test:001",
        scope="component:test_component",
        correlation=Correlation("corr:test:001", request_id="request:test:001"),
        outcome=ReceiptOutcome.COMMITTED,
        commit_state=ReceiptCommitState.COMMITTED,
        requested_at=NOW,
        committed_at=NOW,
        recorded_at=NOW,
        target_refs=("target:test:001",),
        authority_refs=("decision:test:001",),
    )
    assert ReceiptEnvelope.from_dict(receipt.to_dict()) == receipt
    with pytest.raises(InterfaceValidationError, match="commit_state"):
        ReceiptEnvelope(
            receipt_id="receipt:test:002",
            receipt_schema_version="1.0.0",
            receipt_class=ReceiptClass.TRANSITION,
            transition_type="test_state_change",
            producer_component_id="test_component",
            subject_ref="subject:test:001",
            scope="component:test_component",
            correlation=Correlation("corr:test:002"),
            outcome=ReceiptOutcome.COMMITTED,
            recorded_at=NOW,
        )


def test_job_request_requires_idempotency_and_job_status_is_explicit() -> None:
    identity = IdentityContext(
        actor_ref="service:test-client",
        subject_ref="subject:test:001",
        identity_type=IdentityType.SERVICE,
        authenticated=True,
        assurance_level="local_peer_verified",
        authority_refs=("decision:test:001",),
    )
    request = JobRequest(
        job_id="JOB-TEST-001",
        job_type="test.work",
        interface_version="1.0.0",
        sender="test_client",
        intended_receiver="test_worker",
        payload_schema="schema:test-job",
        payload={"work": "bounded"},
        created_at=NOW,
        correlation=Correlation("corr:test:job:001"),
        idempotency=Idempotency(
            required=True,
            key="idem:test:job:001",
            duplicate_outcome=DuplicateOutcome.RETURN_PRIOR_RESULT,
            retention_rule="retain until terminal status expires",
        ),
        identity_context=identity,
    )
    assert JobRequest.from_dict(request.to_dict()) == request
    status = JobStatus(
        job_id=request.job_id,
        state=JobState.COMPLETED,
        observed_at=NOW,
        correlation_id=request.correlation.correlation_id,
        progress=100,
        result={"outcome": "no_effect"},
    )
    assert status.terminal
    assert JobStatus.from_dict(status.to_dict()) == status
    with pytest.raises(InterfaceValidationError, match="failed job must contain"):
        JobStatus(
            job_id=request.job_id,
            state=JobState.FAILED,
            observed_at=NOW,
            correlation_id=request.correlation.correlation_id,
        )


def test_capability_snapshot_rejects_duplicate_capability_ids() -> None:
    with pytest.raises(InterfaceValidationError, match="must be unique"):
        CapabilitySnapshot(
            snapshot_id="snapshot:test:001",
            component_id="test_component",
            observed_at=NOW,
            contract_version="1.0.0",
            capabilities=(_capability(), _capability()),
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


def test_unix_http_client_sends_correlation_without_implicit_retry(tmp_path: Path) -> None:
    socket_path = tmp_path / "service.sock"
    response = JobStatus(
        job_id="JOB-TEST-001",
        state=JobState.ACCEPTED,
        observed_at=NOW,
        correlation_id="corr:test:job:001",
        progress=0,
    ).to_dict()
    server = _OneShotUnixServer(socket_path, 202, response)
    server.start()
    client = UnixHttpClient(socket_path, sender="test_client")
    request = JobRequest(
        job_id="JOB-TEST-001",
        job_type="test.work",
        interface_version="1.0.0",
        sender="test_client",
        intended_receiver="test_worker",
        payload_schema="schema:test-job",
        payload={"work": "bounded"},
        created_at=NOW,
        correlation=Correlation("corr:test:job:001", request_id="request:test:job:001"),
        idempotency=Idempotency(
            required=True,
            key="idem:test:job:001",
            duplicate_outcome=DuplicateOutcome.RETURN_PRIOR_RESULT,
            retention_rule="retain until terminal status expires",
        ),
    )
    status = client.submit_job(request)
    server.join()
    assert status.state is JobState.ACCEPTED
    assert "X-Correlation-ID: corr:test:job:001" in server.request_head
    assert "Idempotency-Key: idem:test:job:001" in server.request_head


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
