"""Fail-closed and last-valid-state proofs for the public API boundary."""

from __future__ import annotations

from copy import deepcopy

import pytest

from koa_kristal_runtime.api import (
    ArtifactIncompatible,
    ArtifactUntrusted,
    AtomicActivationFailed,
    AuthorizationUnavailable,
    EvidenceUnavailable,
    ForwardRepairRequired,
    ResourceGrantUnavailable,
    StatusScopeDenied,
    ApiRequest,
    Receipt,
    RuntimePackTransitionResult,
    RuntimePackVerificationResult,
    create_api,
)
from koa_kristal_runtime.api.models import ModelValidationError, VERIFICATION_CHECKS


def request(interface_id: str, payload: dict[str, object]) -> ApiRequest:
    return ApiRequest(interface_id, f"request.{interface_id}", f"correlation.{interface_id}", payload)


@pytest.mark.parametrize(
    ("failure", "code"),
    [
        (ArtifactUntrusted(), "artifact_untrusted"),
        (ArtifactIncompatible(), "artifact_incompatible"),
        (EvidenceUnavailable(), "evidence_unavailable"),
    ],
)
def test_validation_authority_failures_are_rejected(service, runtime_pack, failure, code) -> None:
    service.failures["runtime_pack_validation"] = failure
    response = create_api(service).dispatch(request("runtime_pack_validation", {"runtime_pack": runtime_pack}))
    assert response.status == "rejected"
    assert response.error.code == code
    assert service.active_runtime_identity.endswith("community-services-previous")


@pytest.mark.parametrize(
    ("failure", "code"),
    [
        (AuthorizationUnavailable(), "authorization_unavailable"),
        (ResourceGrantUnavailable(), "resource_grant_unavailable"),
        (AtomicActivationFailed(), "activation_failed"),
    ],
)
def test_activation_failure_preserves_current_runtime(service, failure, code) -> None:
    previous = service.active_runtime_identity
    service.failures["runtime_pack_activation"] = failure
    response = create_api(service).dispatch(
        request(
            "runtime_pack_activation",
            {
                "activation_request_id": "activation.1",
                "verified_runtime_pack_ref": "verification-record:community-services:1.0.0",
                "authorization_ref": "decision:allow:activation.1",
                "resource_grant_ref": "resource-grant:activation.1",
            },
        )
    )
    assert response.status == "rejected"
    assert response.error.code == code
    assert service.active_runtime_identity == previous


def test_rollback_forward_repair_is_explicit(service) -> None:
    service.failures["runtime_pack_rollback"] = ForwardRepairRequired()
    response = create_api(service).dispatch(
        request(
            "runtime_pack_rollback",
            {
                "rollback_request_id": "rollback.1",
                "target_last_valid_runtime_ref": "runtime-pack:knowledge/community-services-previous",
                "authorization_ref": "decision:allow:rollback.1",
            },
        )
    )
    assert response.status == "rejected"
    assert response.error.code == "forward_repair_required"


def test_status_scope_denial_does_not_leak_runtime_state(service) -> None:
    service.failures["runtime_status_query"] = StatusScopeDenied()
    response = create_api(service).dispatch(
        request("runtime_status_query", {"authorized_status_scope": "scope:denied"})
    ).to_mapping()
    assert response["status"] == "rejected"
    assert response["error"]["code"] == "status_scope_denied"
    assert "runtime-pack:" not in str(response)


def test_unexpected_exception_is_redacted(service) -> None:
    service.failures["runtime_status_query"] = RuntimeError("secret backend location /private/db.sqlite")
    response = create_api(service).dispatch(
        request("runtime_status_query", {"authorized_status_scope": "scope:status:read"})
    ).to_mapping()
    assert response["status"] == "failed"
    assert response["error"] == {"code": "internal_failure", "message": "the Kristal Runtime operation failed"}
    assert "db.sqlite" not in str(response)


def test_nonverified_result_cannot_be_activation_eligible() -> None:
    receipt = Receipt(
        "receipt:validation:blocked",
        "verification_receipt",
        "runtime_pack_validation",
        "blocked",
        "correlation.1",
        "runtime-pack:knowledge/community-services",
    )
    with pytest.raises(ModelValidationError, match="cannot be activation eligible"):
        RuntimePackVerificationResult(
            "blocked",
            True,
            "verification-record:blocked",
            "runtime-pack:knowledge/community-services",
            "1.0.0",
            "sha256:" + "a" * 64,
            {name: "blocked" for name in VERIFICATION_CHECKS},
            receipt,
        )


def test_failed_transition_cannot_discard_last_valid_state() -> None:
    receipt = Receipt(
        "receipt:activation:failed",
        "transition_receipt",
        "runtime_pack_activation",
        "failed",
        "correlation.1",
        "runtime-pack:knowledge/community-services",
    )
    with pytest.raises(ModelValidationError, match="preserve the last valid state"):
        RuntimePackTransitionResult("runtime_pack_activation", "failed", None, False, receipt)


def test_wrong_api_version_is_rejected_before_service_call(service) -> None:
    response = create_api(service).dispatch(
        {
            "interface_id": "runtime_status_query",
            "request_id": "request.1",
            "correlation_id": "correlation.1",
            "version": "2.0.0",
            "payload": {"authorized_status_scope": "scope:status:read"},
        }
    )
    assert response.status == "rejected"
    assert response.error.code == "unsupported_version"
    assert service.calls == []
