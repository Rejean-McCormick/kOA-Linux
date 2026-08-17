from __future__ import annotations

from koa_resource_governor.api import OPERATIONS

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


def test_activation_requires_idempotency_before_service_invocation(router, complete_service):
    spec = OPERATIONS["activate_resource_envelope"]
    headers = headers_for(spec)
    headers.pop("x-koa-idempotency-key")

    result = router.dispatch("POST", spec.path, request_for(spec), headers)

    assert result.status_code == 400
    assert result.body["reason_code"] == "missing_idempotency_key"
    assert complete_service.calls == []


def test_admission_accepts_only_declared_optional_fields(router, complete_service):
    spec = OPERATIONS["admit_workload"]
    request = request_for(spec)
    request.update(
        {
            "deadline": "2026-08-06T12:10:00Z",
            "expiry": "2026-08-06T12:20:00Z",
            "queue_policy_ref": "queue-policy:test",
            "policy_decision_ref": "policy-decision:test",
            "exception_refs": [],
        }
    )
    result = router.dispatch("POST", spec.path, request, headers_for(spec))
    assert result.status_code == 200

    request["capacity_implies_authorization"] = True
    rejected = router.dispatch("POST", spec.path, request, headers_for(spec))
    assert rejected.status_code == 400
    assert rejected.body["reason_code"] == "request_contract_violation"
    assert len(complete_service.calls) == 1


def test_workload_business_content_is_rejected_before_service_invocation(router, complete_service):
    spec = OPERATIONS["admit_workload"]
    request = request_for(spec)
    request["resource_request"]["workload_payload"] = {"document": "must-not-cross"}

    result = router.dispatch("POST", spec.path, request, headers_for(spec))

    assert result.status_code == 400
    assert result.body["reason_code"] == "workload_payload_prohibited"
    assert "must-not-cross" not in repr(result.body)
    assert complete_service.calls == []


def test_unknown_version_route_and_method_fail_closed(router, complete_service):
    spec = OPERATIONS["get_component_status"]
    headers = headers_for(spec)
    headers["x-koa-contract-version"] = "999.0.0"
    wrong_version = router.dispatch("POST", spec.path, request_for(spec), headers)
    assert wrong_version.status_code == 400
    assert wrong_version.body["reason_code"] == "contract_version_unsupported"

    unknown = router.dispatch(
        "POST",
        "/v1/commands/authorize_business_operation",
        {},
        {"x-koa-contract-version": "1.0.0", "x-koa-correlation-id": "corr:test"},
    )
    assert unknown.status_code == 404
    assert unknown.body["reason_code"] == "operation_not_declared"

    wrong_method = router.dispatch("GET", spec.path, request_for(spec), headers_for(spec))
    assert wrong_method.status_code == 405
    assert wrong_method.body["reason_code"] == "method_not_allowed"
    assert complete_service.calls == []
