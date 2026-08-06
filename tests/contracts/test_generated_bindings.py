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
        required=True,
        key="idem:test:001",
        duplicate_outcome=DuplicateOutcome.RETURN_PRIOR_RESULT,
        retention_rule="retain until the terminal result expires",
    )
    error = ErrorEnvelope(
        error_id="error:test:001",
        code="dependency_unavailable",
        category=ErrorCategory.DEPENDENCY_UNAVAILABLE,
        message="required dependency is unavailable",
        disposition=ErrorDisposition.RECONCILE_BEFORE_RETRY,
        observed_at=NOW,
        correlation_id=correlation.correlation_id,
        reason_codes=("dependency_unavailable",),
    )
    capability = _capability()
    return {
        "event_envelope": EventEnvelope(
            event_id="event:test:001",
            event_type="test.fact_committed",
            interface_version="1.0.0",
            sender="test_source",
            intended_receiver="test_target",
            payload_schema="urn:koa:test:payload:1",
            payload={"value": 1},
            created_at=NOW,
            correlation=correlation,
            delivery_guarantee=DeliveryGuarantee.EFFECTIVELY_ONCE,
            ordering=Ordering.PER_KEY,
            ordering_key="subject:test:001",
            idempotency=idempotency,
        ).to_dict(),
        "error_envelope": error.to_dict(),
        "idempotency": idempotency.to_dict(),
        "version_negotiation": VersionNegotiation(("1.0.0",), selected_version="1.0.0").to_dict(),
        "health_status": HealthStatus(
            component_id="test_component",
            instance_id="instance:test:001",
            state=HealthState.HEALTHY,
            observed_at=NOW,
            contract_version="1.0.0",
            schema_version="1.0.0",
            capabilities=(capability,),
            startup_complete=True,
            freshness_seconds=5,
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
