from __future__ import annotations

from koa_identity_and_trust.api import OPERATIONS

from .._support import headers_for, request_for


def test_every_declared_operation_dispatches_through_public_service(router, complete_service):
    for operation_id, spec in OPERATIONS.items():
        result = router.dispatch("POST", spec.path, request_for(spec), headers_for(spec))
        assert result.status_code == 200, (operation_id, result.body)
        assert result.body["operation_id"] == operation_id
        assert result.body["outcome"] == "completed"
        assert set(result.body["payload"]) == set(spec.response_fields)
        assert result.headers["x-koa-correlation-id"] == f"corr:{operation_id}:test"

    assert [call[0] for call in complete_service.calls] == list(OPERATIONS)


def test_critical_transition_requires_idempotency_key(router, complete_service):
    spec = OPERATIONS["issue_credential"]
    headers = headers_for(spec)
    headers.pop("x-koa-idempotency-key")

    result = router.dispatch("POST", spec.path, request_for(spec), headers)

    assert result.status_code == 400
    assert result.body["outcome"] == "rejected"
    assert result.body["reason_code"] == "missing_idempotency_key"
    assert complete_service.calls == []


def test_unknown_contract_version_fails_before_service_invocation(router, complete_service):
    spec = OPERATIONS["resolve_identity"]
    headers = headers_for(spec)
    headers["x-koa-contract-version"] = "999.0.0"

    result = router.dispatch("POST", spec.path, request_for(spec), headers)

    assert result.status_code == 400
    assert result.body["reason_code"] == "algorithm_or_version_unsupported"
    assert complete_service.calls == []


def test_unknown_route_and_wrong_method_are_rejected(router, complete_service):
    unknown = router.dispatch(
        "POST",
        "/v1/commands/grant_universal_administrator_authority",
        {},
        {"x-koa-contract-version": "1.0.0", "x-koa-correlation-id": "corr:test"},
    )
    assert unknown.status_code == 404
    assert unknown.body["reason_code"] == "operation_not_declared"

    spec = OPERATIONS["resolve_identity"]
    wrong_method = router.dispatch("GET", spec.path, request_for(spec), headers_for(spec))
    assert wrong_method.status_code == 405
    assert wrong_method.body["reason_code"] == "method_not_allowed"
    assert complete_service.calls == []


def test_authentication_response_contains_no_authorization_decision(router):
    spec = OPERATIONS["authenticate_subject"]
    result = router.dispatch("POST", spec.path, request_for(spec), headers_for(spec))

    assert result.status_code == 200
    response = result.body["payload"]
    assert response["identity_result"] == "established"
    assert "authorized" not in response
    assert "authorization_result" not in response
    assert "policy_decision" not in response
