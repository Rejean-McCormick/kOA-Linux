from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timedelta, timezone

import pytest

from koa_sentient_adapter import (
    CANDIDATE_ONLY_OPERATIONS,
    CandidateArtifact,
    CandidateArtifactClass,
    CandidateState,
    ExperimentPlan,
    InputSelection,
    SentientAdapterSettings,
    SentientOperationMap,
    WorkbenchJobRequest,
    WorkbenchJobState,
)

NOW = datetime(2026, 8, 6, 15, 0, tzinfo=timezone.utc)


def _plan() -> ExperimentPlan:
    return ExperimentPlan(
        success_criteria=("produce candidate analysis",),
        stop_conditions=("deadline reached", "resource envelope exhausted"),
        resource_envelope_ref="resource-envelope:sentient-dev",
        data_scope=("kristal:entity-001", "kristal:entity-002"),
        output_disposition="candidate_review",
        cleanup_policy_ref="cleanup-policy:sentient-default",
        test_refs=("test:contract-001",),
        evidence_refs=("evidence:experiment-plan-001",),
        max_attempts=2,
        queue_limit=10,
        concurrency_limit=1,
        max_duration_seconds=3600,
    )


def _request(selection: InputSelection, *, integration_refs: tuple[str, ...] = ()) -> WorkbenchJobRequest:
    return WorkbenchJobRequest(
        request_id="request-001",
        correlation_id="correlation-001",
        idempotency_key="idem-001",
        operation_id="entity_reconciliation",
        capability_id="sentient_isolated_analysis",
        profile_id="developer_linux_workstation",
        workspace_id="workspace:sentient-001",
        requesting_identity="identity:user-001",
        purpose="research entity reconciliation",
        created_at=NOW,
        deadline=NOW + timedelta(minutes=30),
        input_selection=selection,
        experiment_plan=_plan(),
        policy_authorization_ref="authorization:policy-001",
        resource_admission_ref="receipt:resource-admission-001",
        explicit_trigger=True,
        integration_refs=integration_refs,
    )


def test_candidate_classes_and_ai_operations_match_authority() -> None:
    assert {item.value for item in CandidateArtifactClass} == {
        "candidate_code",
        "candidate_documentation",
        "candidate_configuration",
        "candidate_model",
        "candidate_dataset",
        "candidate_index",
        "candidate_test",
        "candidate_evaluation",
        "candidate_artifact",
        "candidate_change_request",
        "analysis_report",
        "experiment_result",
    }
    assert CANDIDATE_ONLY_OPERATIONS == (
        "classification",
        "descriptive_text",
        "summarization",
        "tagging",
        "transcription",
        "translation",
    )


def test_operation_map_is_closed_and_unique(operation_map: SentientOperationMap) -> None:
    assert tuple(operation_map.as_mapping()) == (
        "health",
        "capabilities",
        "submit_job",
        "read_job",
        "cancel_job",
        "fetch_candidate",
    )
    with pytest.raises(ValueError, match="unique"):
        SentientOperationMap("same", "same", "a", "b", "c", "d")


def test_settings_are_default_off_and_reject_runtime_profile(operation_map: SentientOperationMap) -> None:
    base = dict(
        subsystem_id="sentient",
        subsystem_contract_version="1.0.0",
        adapter_contract_version="1.0.0",
        operations=operation_map,
        workspace_id="workspace:sentient-001",
        service_identity_ref="service:sentient",
        documentation_alignment_verified=True,
        allowed_destination_interfaces=("components/koa-mediatheque/public-api:candidate-import",),
    )
    settings = SentientAdapterSettings(active_profile="developer_linux_workstation", **base)
    assert settings.default_enabled is False
    assert settings.enabled is False
    with pytest.raises(ValueError, match="cannot be enabled"):
        SentientAdapterSettings(active_profile="user_lightweight", enabled=True, **base)


def test_protected_input_requires_authority_and_access_receipt() -> None:
    with pytest.raises(ValueError, match="protected input"):
        InputSelection(
            workflow_id="workflow-001",
            purpose="protected analysis",
            requesting_identity="identity:user-001",
            source_owner="koa_mediatheque",
            source_refs=("koa-media-record:001",),
            data_classes=("protected_media",),
            selected_fields=("title",),
            classification="restricted",
            retention_seconds=300,
            expires_at=NOW + timedelta(minutes=5),
            protected=True,
        )


def test_candidate_is_never_authoritative(candidate_payload: dict) -> None:
    candidate = CandidateArtifact.from_mapping(candidate_payload)
    assert candidate.state is CandidateState.CANDIDATE
    assert candidate.to_dict()["authority"] == "candidate_input"
    assert len(candidate.fingerprint) == 64
    with pytest.raises(ValueError, match="never authoritative"):
        CandidateArtifact.from_mapping({**candidate_payload, "authoritative": True})


def test_job_request_requires_explicit_trigger_and_matching_integrations(candidate_payload: dict) -> None:
    candidate = CandidateArtifact.from_mapping(candidate_payload)
    request = _request(candidate.input_selection)
    request.assert_current(NOW)
    with pytest.raises(ValueError, match="explicit trigger"):
        replace(request, explicit_trigger=False)
    with pytest.raises(ValueError, match="integration usage must agree"):
        _request(candidate.input_selection, integration_refs=("integration:chatgpt",))


def test_submit_read_and_cancel_jobs_are_receipted(adapter, candidate_payload: dict) -> None:
    selection = CandidateArtifact.from_mapping(candidate_payload).input_selection
    submitted = adapter.jobs.submit(_request(selection), now=NOW)
    assert submitted.job.state is WorkbenchJobState.ADMITTED
    assert submitted.receipt.to_dict()["authority_effect"] == "evidence_only"

    completed = adapter.jobs.read("job-001")
    assert completed.state is WorkbenchJobState.COMPLETED
    assert completed.candidate_refs == ("candidate-001",)

    cancelled = adapter.jobs.cancel(
        "job-001",
        "USER_CANCELLED",
        request_id="request-cancel-001",
        correlation_id="correlation-001",
        actor_ref="identity:user-001",
        workspace_id="workspace:sentient-001",
        now=NOW,
    )
    assert cancelled.job.state is WorkbenchJobState.CANCELLED


def test_candidate_crosses_only_owner_acceptance_gateway(adapter, gateway) -> None:
    candidate = adapter.artifacts.fetch_candidate("candidate-001")
    result = adapter.artifacts.submit_candidate(
        candidate,
        request_id="import-request-001",
        correlation_id="correlation-001",
        source_job_ref="job:job-001",
        destination_owner="koa_mediatheque",
        destination_interface_ref="components/koa-mediatheque/public-api:candidate-import",
        intended_artifact_class="koa_media_record",
        actor_ref="identity:user-001",
        purpose="review and controlled import",
        authority_refs=("authorization:import-001",),
        now=NOW + timedelta(minutes=1),
    )
    assert result.owner_result.decision.value == "accepted"
    assert result.owner_result.accepted_artifact_ref == "koa-media-record:record-001"
    assert gateway.calls[0]["authority_effect"] == "candidate_submission_only"
    assert result.receipt.authoritative is False
