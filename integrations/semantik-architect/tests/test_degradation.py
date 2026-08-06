from __future__ import annotations

from koa_semantik_architect_adapter import (
    ArtifactAdmissionDecision,
    ArtifactBridge,
    ArtifactBridgeState,
    CompilerJobCoordinator,
    CompilerJobState,
    RuntimePackBridge,
    RuntimePackPreparationState,
    RuntimePackValidationDecision,
    SemantikArchitectClient,
)
from conftest import FakeArtifactAdmission, FakeRuntimeValidation


def test_compiler_unavailable_returns_blocked_receipt(transport, all_capabilities, compiler_request):
    transport.failures["compiler_job.submit"] = ConnectionError("offline")
    result = CompilerJobCoordinator(SemantikArchitectClient(transport), all_capabilities).submit(compiler_request)
    assert result.state is CompilerJobState.BLOCKED
    assert result.job_ref is None
    assert result.receipt.outcome.value == "blocked"
    assert result.reason_code == "external_unavailable"


def test_compiler_rejection_does_not_claim_execution(transport, all_capabilities, compiler_request):
    transport.responses["compiler_job.submit"] = {
        "operation": "compiler_job.submit",
        "request_id": compiler_request.request_id,
        "correlation_id": compiler_request.correlation_id,
        "outcome": "rejected",
        "payload": {"state": "rejected"},
        "evidence_refs": [],
    }
    result = CompilerJobCoordinator(SemantikArchitectClient(transport), all_capabilities).submit(compiler_request)
    assert result.state is CompilerJobState.REJECTED
    assert result.receipt.execution_state.value == "not_started"


def test_correlation_mismatch_fails_closed(transport, all_capabilities, compiler_request):
    transport.responses["compiler_job.submit"] = {
        "operation": "compiler_job.submit",
        "request_id": compiler_request.request_id,
        "correlation_id": "correlation:wrong",
        "outcome": "accepted",
        "payload": {"state": "submitted", "job_ref": "job:1"},
        "evidence_refs": [],
    }
    result = CompilerJobCoordinator(SemantikArchitectClient(transport), all_capabilities).submit(compiler_request)
    assert result.state is CompilerJobState.FAILED
    assert result.reason_code == "external_protocol_invalid"


def test_artifact_admission_failure_is_blocked(artifact_candidate):
    class BrokenPort:
        def admit_compiled_candidate(self, payload):
            raise RuntimeError("database password leaked")

    result = ArtifactBridge(BrokenPort()).admit(
        artifact_candidate, request_id="request:artifact:1", correlation_id="correlation:artifact:1"
    )
    assert result.state is ArtifactBridgeState.BLOCKED
    assert result.receipt.reason_code == "admission_authority_unavailable"
    assert "password" not in str(result.receipt.to_mapping())


def test_artifact_rejection_remains_non_committed(artifact_candidate):
    port = FakeArtifactAdmission(ArtifactAdmissionDecision(False, "policy_denied"))
    result = ArtifactBridge(port).admit(
        artifact_candidate, request_id="request:artifact:2", correlation_id="correlation:artifact:2"
    )
    assert result.state is ArtifactBridgeState.REJECTED
    assert result.receipt.commit_state.value == "not_committed"


def test_runtime_validation_unavailable_does_not_activate(language_pack_manifest):
    from koa_semantik_architect_adapter import LanguageRuntimePackCandidate

    class BrokenValidation:
        def validate_language_runtime_pack(self, payload):
            raise RuntimeError("offline")

    candidate = LanguageRuntimePackCandidate(
        "artifact:pack:1",
        "sha256:" + "e" * 64,
        language_pack_manifest,
        "artifact-store:pack:1",
        ("evidence:1",),
        "provenance:1",
        ("release-set:1",),
    )
    result = RuntimePackBridge(BrokenValidation()).prepare(
        candidate, request_id="request:pack:1", correlation_id="correlation:pack:1"
    )
    assert result.state is RuntimePackPreparationState.BLOCKED
    assert result.receipt.commit_state.value == "not_committed"
    assert result.verification_ref is None


def test_runtime_validation_rejection_is_explicit(language_pack_manifest):
    from koa_semantik_architect_adapter import LanguageRuntimePackCandidate

    port = FakeRuntimeValidation(RuntimePackValidationDecision(False, "runtime_incompatible"))
    candidate = LanguageRuntimePackCandidate(
        "artifact:pack:2",
        "sha256:" + "f" * 64,
        language_pack_manifest,
        "artifact-store:pack:2",
        ("evidence:2",),
        "provenance:2",
        ("release-set:2",),
    )
    result = RuntimePackBridge(port).prepare(
        candidate, request_id="request:pack:2", correlation_id="correlation:pack:2"
    )
    assert result.state is RuntimePackPreparationState.REJECTED
    assert result.reason_code == "runtime_incompatible"
