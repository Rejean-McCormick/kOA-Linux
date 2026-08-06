"""Fail-closed and disclosure-minimization proofs."""

from __future__ import annotations

import pytest

from koa_publication_gateway.api import (
    ApiRequest,
    AuditUnavailable,
    ConsentUnavailable,
    CulturalAuthorityDisputed,
    DestinationIncompatible,
    IdentityUnavailable,
    PolicyUnavailable,
    QueueInspectionResult,
    QueueScopeDenied,
    ReceiptPersistenceFailed,
    ResourceUnavailable,
    RevalidationFailed,
    StatusScopeDenied,
    ControlledRetryRequest,
    HealthResult,
    HealthState,
    ModelValidationError,
    PublicationDecision,
    PublicationDecisionOutcome,
    PublicationRequestResult,
    PublicationState,
    REVALIDATION_DIMENSIONS,
    create_api,
)


def request(interface_id: str, payload: dict[str, object]) -> ApiRequest:
    return ApiRequest(interface_id, f"request:{interface_id}", f"correlation:{interface_id}", payload)


@pytest.mark.parametrize(
    ("failure", "code"),
    [
        (IdentityUnavailable(), "identity_unavailable"),
        (PolicyUnavailable(), "policy_unavailable"),
        (ConsentUnavailable(), "consent_unavailable"),
        (CulturalAuthorityDisputed(), "cultural_authority_disputed"),
        (DestinationIncompatible(), "destination_incompatible"),
        (ResourceUnavailable(), "resource_unavailable"),
        (AuditUnavailable(), "audit_unavailable"),
        (ReceiptPersistenceFailed(), "receipt_persistence_failed"),
    ],
)
def test_required_authority_failures_block_publication(service, publication_artifact, failure, code) -> None:
    service.failures["publication_request"] = failure
    response = create_api(service).dispatch(request("publication_request", {"publication_request": publication_artifact}))
    assert response.status == "rejected"
    assert response.error.code == code


def test_receipt_failure_never_reports_success(service, publication_artifact) -> None:
    service.failures["publication_request"] = ReceiptPersistenceFailed()
    response = create_api(service).dispatch(request("publication_request", {"publication_request": publication_artifact})).to_mapping()
    assert response["status"] == "rejected"
    assert "result" not in response
    assert response["error"]["code"] == "receipt_persistence_failed"


def test_status_scope_denial_does_not_leak_source(service) -> None:
    service.failures["publication_status_query"] = StatusScopeDenied()
    response = create_api(service).dispatch(request("publication_status_query", {"publication_request_id": "request:1", "authorized_scope_ref": "scope:denied"})).to_mapping()
    assert response["status"] == "rejected"
    assert "media:record" not in str(response)


def test_queue_scope_denial_does_not_leak_queue(service) -> None:
    service.failures["queue_inspection"] = QueueScopeDenied()
    response = create_api(service).dispatch(request("queue_inspection", {"authorized_scope_ref": "scope:denied", "limit": 10})).to_mapping()
    assert response["status"] == "rejected"
    assert "destination:remote" not in str(response)


def test_unexpected_exception_is_redacted(service) -> None:
    service.failures["health"] = RuntimeError("private source /var/lib/koa/publication-gateway/staging/secret")
    response = create_api(service).dispatch(request("health", {"authorized_scope_ref": "scope:health"})).to_mapping()
    assert response["status"] == "failed"
    assert response["error"] == {"code": "internal_failure", "message": "the publication operation failed", "field": None, "details": {}}
    assert "staging" not in str(response)


def test_reconnection_retry_requires_every_dimension(retry_payload) -> None:
    retry_payload["revalidation_dimensions"] = sorted(REVALIDATION_DIMENSIONS - {"consent"})
    with pytest.raises(ModelValidationError, match="every mutable"):
        ControlledRetryRequest.from_payload(retry_payload, request("controlled_retry", retry_payload))


def test_retry_cannot_broaden_scope(retry_payload) -> None:
    retry_payload["scope_unchanged"] = False
    with pytest.raises(ModelValidationError, match="must not broaden"):
        ControlledRetryRequest.from_payload(retry_payload, request("controlled_retry", retry_payload))


def test_wrong_api_version_is_rejected_before_service_call(service) -> None:
    response = create_api(service).dispatch(
        {
            "interface_id": "health",
            "request_id": "request:1",
            "correlation_id": "correlation:1",
            "version": "2.0.0",
            "payload": {"authorized_scope_ref": "scope:health"},
        }
    )
    assert response.status == "rejected"
    assert response.error.code == "unsupported_version"
    assert service.calls == []


def test_health_cannot_claim_healthy_without_authorities() -> None:
    with pytest.raises(ModelValidationError, match="healthy state"):
        HealthResult(HealthState.HEALTHY, True, True, False, 0)


def test_non_allow_result_cannot_stage_or_publish() -> None:
    decision = PublicationDecision("decision:1", PublicationDecisionOutcome.BLOCKED, "request:1", ("authority:1",), (), False)
    with pytest.raises(ModelValidationError, match="cannot progress"):
        PublicationRequestResult("request:1", PublicationState.STAGING, decision, None)


def test_service_result_must_use_public_model(service) -> None:
    service.health = lambda request: {"state": "healthy"}
    response = create_api(service).dispatch(request("health", {"authorized_scope_ref": "scope:health"}))
    assert response.status == "rejected"
    assert response.error.code == "invalid_service_result"
