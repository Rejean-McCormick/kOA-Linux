from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timedelta, timezone

import pytest

from koa_sentient_adapter import (
    CandidateArtifact,
    ExperimentPlan,
    InputSelection,
    SentientAdapterSettings,
    SentientClientError,
    WorkbenchJobRequest,
    WorkbenchUnavailable,
    bootstrap_adapter,
)

NOW = datetime(2026, 8, 6, 15, 0, tzinfo=timezone.utc)


def _request(selection: InputSelection, *, deadline: datetime | None = None) -> WorkbenchJobRequest:
    plan = ExperimentPlan(
        success_criteria=("candidate created",),
        stop_conditions=("deadline",),
        resource_envelope_ref="resource-envelope:sentient-dev",
        data_scope=("source:one",),
        output_disposition="candidate_review",
        cleanup_policy_ref="cleanup:default",
        test_refs=("test:one",),
        evidence_refs=("evidence:one",),
        max_attempts=1,
        queue_limit=2,
        concurrency_limit=1,
        max_duration_seconds=1800,
    )
    return WorkbenchJobRequest(
        request_id="request-001",
        correlation_id="correlation-001",
        idempotency_key="idem-001",
        operation_id="classification",
        capability_id="sentient_isolated_analysis",
        profile_id="developer_linux_workstation",
        workspace_id="workspace:sentient-001",
        requesting_identity="identity:user-001",
        purpose="bounded analysis",
        created_at=NOW,
        deadline=deadline or NOW + timedelta(minutes=10),
        input_selection=selection,
        experiment_plan=plan,
        policy_authorization_ref="authorization:one",
        resource_admission_ref="resource-admission:one",
    )


def test_unaligned_or_disabled_workbench_fails_explicitly(settings, transport, gateway, candidate_payload) -> None:
    selection = CandidateArtifact.from_mapping(candidate_payload).input_selection
    unaligned = bootstrap_adapter(
        replace(settings, documentation_alignment_verified=False),
        transport=transport,
        owner_gateway=gateway,
    )
    with pytest.raises(WorkbenchUnavailable, match="DOCUMENTATION_ALIGNMENT"):
        unaligned.jobs.submit(_request(selection), now=NOW)

    disabled = bootstrap_adapter(
        replace(settings, enabled=False),
        transport=transport,
        owner_gateway=gateway,
    )
    with pytest.raises(WorkbenchUnavailable, match="DISABLED_BY_DEFAULT"):
        disabled.jobs.submit(_request(selection), now=NOW)


def test_expired_work_is_rejected_before_transport(adapter, transport, candidate_payload) -> None:
    selection = CandidateArtifact.from_mapping(candidate_payload).input_selection
    request = _request(selection, deadline=NOW + timedelta(seconds=10))
    with pytest.raises(ValueError, match="expired"):
        adapter.jobs.submit(request, now=NOW + timedelta(seconds=11))
    assert all(call[0] != adapter.client.operations.submit_job for call in transport.calls)


def test_network_access_is_default_off_and_destination_scoped(operation_map) -> None:
    base = dict(
        subsystem_id="sentient",
        subsystem_contract_version="1.0.0",
        adapter_contract_version="1.0.0",
        operations=operation_map,
        active_profile="developer_linux_workstation",
        workspace_id="workspace:sentient-001",
        service_identity_ref="service:sentient",
        documentation_alignment_verified=True,
        enabled=True,
        allowed_destination_interfaces=("components/kristal-runtime/public-api:candidate-import",),
    )
    with pytest.raises(ValueError, match="requires destination-scoped"):
        SentientAdapterSettings(network_enabled=True, **base)
    with pytest.raises(ValueError, match="require network_enabled"):
        SentientAdapterSettings(allowed_integration_refs=("integration:chatgpt",), **base)


def test_provider_or_transport_failure_preserves_candidate_state(adapter, transport) -> None:
    candidate = adapter.artifacts.fetch_candidate("candidate-001")
    fingerprint = candidate.fingerprint
    transport.failure = TimeoutError("timeout")
    with pytest.raises(SentientClientError) as exc:
        adapter.jobs.read("job-001")
    assert exc.value.reason_code == "SENTIENT_TIMEOUT"
    assert candidate.fingerprint == fingerprint
    assert candidate.authoritative is False


def test_owner_rejection_keeps_candidate_non_authoritative(adapter, gateway) -> None:
    candidate = adapter.artifacts.fetch_candidate("candidate-001")
    gateway.result = {
        "decision": "rejected",
        "destination_owner": "koa_mediatheque",
        "candidate_id": "candidate-001",
        "decision_ref": "decision:reject-001",
        "decided_at": NOW.isoformat(),
        "reason_code": "OWNER_VALIDATION_FAILED",
        "accepted_artifact_ref": None,
        "evidence_refs": ["evidence:reject-001"],
    }
    result = adapter.artifacts.submit_candidate(
        candidate,
        request_id="import-request-002",
        correlation_id="correlation-002",
        source_job_ref="job:job-001",
        destination_owner="koa_mediatheque",
        destination_interface_ref="components/koa-mediatheque/public-api:candidate-import",
        intended_artifact_class="koa_media_record",
        actor_ref="identity:user-001",
        purpose="controlled import",
        authority_refs=("authorization:import-001",),
        now=NOW + timedelta(minutes=1),
    )
    assert result.owner_result.decision.value == "rejected"
    assert result.candidate.authoritative is False
    assert result.receipt.outcome.value == "failed"
