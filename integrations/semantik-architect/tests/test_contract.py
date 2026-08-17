from __future__ import annotations

import pytest

from koa_semantik_architect_adapter import (
    ADAPTER_VERSION,
    INTEGRATION_ID,
    LANGUAGE_PACK_SCHEMA,
    OFFICIAL_DOCUMENTATION_MOUNT,
    SUBSYSTEM_CONTRACT_VERSION,
    AlignmentState,
    CapabilityId,
    CommitState,
    CompilerJobRequest,
    Decision,
    ExecutionState,
    LanguageRuntimePackCandidate,
    ReceiptOutcome,
    make_receipt,
)


def test_canonical_identifiers_are_stable(all_capabilities):
    assert INTEGRATION_ID == "semantik_architect"
    assert SUBSYSTEM_CONTRACT_VERSION == "1.0.0"
    assert ADAPTER_VERSION == "1.0.0"
    assert OFFICIAL_DOCUMENTATION_MOUNT == "subsystems/semantik-architect"
    assert LANGUAGE_PACK_SCHEMA.endswith("/language-pack.schema.json")
    assert all_capabilities.subsystem_id == "semantik_architect"
    assert all_capabilities.contract_version == "1.0.0"
    assert all_capabilities.alignment_state is AlignmentState.PREPARATION_ONLY
    assert {item.capability_id for item in all_capabilities.capabilities} == set(CapabilityId)


def test_compiler_request_targets_only_knowledge(compiler_request):
    payload = compiler_request.to_payload()
    assert payload["release_channel"] == "knowledge"
    assert payload["source_revision"] == "git:0123456789abcdef"
    assert "source_content" not in payload


def test_compiler_request_rejects_secret_parameters(compiler_request):
    values = {name: getattr(compiler_request, name) for name in compiler_request.__dataclass_fields__}
    values["parameters"] = {"api_token": "sensitive"}
    with pytest.raises(ValueError, match="secret-bearing"):
        CompilerJobRequest(**values)


def test_receipt_identity_is_deterministic():
    from datetime import datetime, timezone

    clock = lambda: datetime(2026, 8, 6, 12, 0, tzinfo=timezone.utc)
    kwargs = dict(
        receipt_type="test_transition",
        request_id="request:1",
        correlation_id="correlation:1",
        subject_ref="subject:1",
        decision=Decision.AUTHORIZED,
        execution_state=ExecutionState.SUCCEEDED,
        commit_state=CommitState.NOT_APPLICABLE,
        outcome=ReceiptOutcome.SUCCEEDED,
        reason_code="test_succeeded",
        clock=clock,
    )
    first = make_receipt(**kwargs)
    second = make_receipt(**kwargs)
    assert first.receipt_id == second.receipt_id
    assert first.to_mapping()["outcome"] == "succeeded"


def test_language_runtime_pack_requires_complete_manifest(language_pack_manifest):
    candidate = LanguageRuntimePackCandidate(
        artifact_ref="artifact:language-pack:fr-ca:1.0.0",
        artifact_digest="sha256:" + "c" * 64,
        manifest=language_pack_manifest,
        content_ref="artifact-store:language-pack:fr-ca:1.0.0",
        verification_evidence_refs=("evidence:1",),
        provenance_ref="provenance:1",
        release_set_refs=("release-set:1",),
    )
    payload = candidate.to_validation_payload()
    assert payload["activation_requested"] is False
    assert payload["authority_effect"] == "candidate_validation_only"


def test_language_runtime_pack_rejects_partial_or_wrong_channel(language_pack_manifest):
    partial = dict(language_pack_manifest)
    partial.pop("validation")
    with pytest.raises(ValueError, match="missing fields"):
        LanguageRuntimePackCandidate(
            "artifact:1", "sha256:" + "d" * 64, partial, "artifact-store:1", ("evidence:1",), "provenance:1", ("release-set:1",)
        )
    wrong = dict(language_pack_manifest)
    wrong["release_channel"] = "services"
    with pytest.raises(ValueError, match="knowledge"):
        LanguageRuntimePackCandidate(
            "artifact:1", "sha256:" + "d" * 64, wrong, "artifact-store:1", ("evidence:1",), "provenance:1", ("release-set:1",)
        )


def test_compiler_job_success_paths(transport, all_capabilities, compiler_request):
    from koa_semantik_architect_adapter import CompilerJobCoordinator, CompilerJobState, SemantikArchitectClient

    transport.responses["compiler_job.submit"] = {
        "operation": "compiler_job.submit",
        "request_id": compiler_request.request_id,
        "correlation_id": compiler_request.correlation_id,
        "outcome": "accepted",
        "payload": {"state": "queued", "job_ref": "compiler-job:1"},
        "evidence_refs": ["evidence:submission:1"],
    }
    coordinator = CompilerJobCoordinator(SemantikArchitectClient(transport), all_capabilities)
    submitted = coordinator.submit(compiler_request)
    assert submitted.state is CompilerJobState.QUEUED
    assert submitted.job_ref == "compiler-job:1"
    assert submitted.receipt.outcome.value == "succeeded"

    transport.responses["compiler_job.status"] = {
        "operation": "compiler_job.status",
        "request_id": "request:status:1",
        "correlation_id": "correlation:status:1",
        "outcome": "succeeded",
        "payload": {
            "state": "succeeded",
            "job_ref": "compiler-job:1",
            "artifact_refs": ["artifact:pgf:1", "artifact:language-pack:1"],
        },
        "evidence_refs": ["evidence:compiler:1"],
    }
    completed = coordinator.status(
        "compiler-job:1", request_id="request:status:1", correlation_id="correlation:status:1"
    )
    assert completed.state is CompilerJobState.SUCCEEDED
    assert completed.artifact_refs == ("artifact:pgf:1", "artifact:language-pack:1")


def test_compiler_job_cancellation_success(transport, all_capabilities):
    from koa_semantik_architect_adapter import CompilerJobCoordinator, CompilerJobState, SemantikArchitectClient

    transport.responses["compiler_job.cancel"] = {
        "operation": "compiler_job.cancel",
        "request_id": "request:cancel:1",
        "correlation_id": "correlation:cancel:1",
        "outcome": "cancelled",
        "payload": {"state": "cancelled", "job_ref": "compiler-job:1"},
        "evidence_refs": ["evidence:cancel:1"],
    }
    result = CompilerJobCoordinator(SemantikArchitectClient(transport), all_capabilities).cancel(
        "compiler-job:1",
        request_id="request:cancel:1",
        correlation_id="correlation:cancel:1",
        idempotency_key="idempotency:cancel:1",
    )
    assert result.state is CompilerJobState.CANCELLED
    assert result.receipt.outcome.value == "cancelled"


def test_artifact_and_runtime_pack_success_paths(artifact_candidate, language_pack_manifest):
    from ._support import FakeArtifactAdmission, FakeRuntimeValidation
    from koa_semantik_architect_adapter import (
        ArtifactBridge,
        ArtifactBridgeState,
        LanguageRuntimePackCandidate,
        RuntimePackBridge,
        RuntimePackPreparationState,
    )

    artifact_result = ArtifactBridge(FakeArtifactAdmission()).admit(
        artifact_candidate, request_id="request:artifact:success", correlation_id="correlation:artifact:success"
    )
    assert artifact_result.state is ArtifactBridgeState.ADMITTED
    assert artifact_result.admission_ref == "admission:artifact:1"

    candidate = LanguageRuntimePackCandidate(
        "artifact:pack:success",
        "sha256:" + "9" * 64,
        language_pack_manifest,
        "artifact-store:pack:success",
        ("evidence:pack:success",),
        "provenance:pack:success",
        ("release-set:success",),
    )
    pack_result = RuntimePackBridge(FakeRuntimeValidation()).prepare(
        candidate, request_id="request:pack:success", correlation_id="correlation:pack:success"
    )
    assert pack_result.state is RuntimePackPreparationState.PREPARED
    assert pack_result.verification_ref == "verification:runtime-pack:1"
    assert pack_result.receipt.commit_state.value == "not_committed"
