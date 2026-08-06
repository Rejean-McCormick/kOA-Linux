"""Integration of models, dispatcher, and the preceding-bundle public port."""

from __future__ import annotations

from koa_kristal_runtime.api import ApiRequest, create_api


def request(interface_id: str, payload: dict[str, object], number: int) -> ApiRequest:
    return ApiRequest(interface_id, f"request.{number}", f"correlation.{number}", payload)


def test_identity_resolution_is_non_mutating(service) -> None:
    api = create_api(service)
    previous = service.active_runtime_identity
    response = api.dispatch(
        request(
            "kristal_identity_resolution",
            {"content_digest": "sha256:" + "a" * 64},
            1,
        )
    )
    assert response.status == "succeeded"
    assert response.result["outcome"] == "resolved"
    assert response.result["resolved_kristal_identity"] == "kristal:community-services:index"
    assert service.active_runtime_identity == previous


def test_validate_activate_query_and_rollback_flow(service, runtime_pack) -> None:
    api = create_api(service)

    validation = api.dispatch(request("runtime_pack_validation", {"runtime_pack": runtime_pack}, 1))
    assert validation.status == "succeeded"
    assert validation.result["outcome"] == "verified"
    assert validation.result["activation_eligible"] is True
    assert validation.result["receipt"]["transition"] == "runtime_pack_validation"

    activation = api.dispatch(
        request(
            "runtime_pack_activation",
            {
                "activation_request_id": "activation.1",
                "verified_runtime_pack_ref": validation.result["verification_record_ref"],
                "authorization_ref": "decision:allow:activation.1",
                "resource_grant_ref": "resource-grant:activation.1",
            },
            2,
        )
    )
    assert activation.status == "succeeded"
    assert activation.result["outcome"] == "activated"
    assert activation.result["last_valid_state_preserved"] is True
    assert activation.result["receipt"]["correlation_id"] == "correlation.2"

    status = api.dispatch(
        request("runtime_status_query", {"authorized_status_scope": "scope:status:read"}, 3)
    )
    assert status.status == "succeeded"
    assert status.result["activation_state"] == "active"
    assert status.result["health_state"]["process_alive"] is True
    assert status.result["health_state"]["activation_ready"] is True

    rollback = api.dispatch(
        request(
            "runtime_pack_rollback",
            {
                "rollback_request_id": "rollback.1",
                "target_last_valid_runtime_ref": "runtime-pack:knowledge/community-services-previous",
                "authorization_ref": "decision:allow:rollback.1",
            },
            4,
        )
    )
    assert rollback.status == "succeeded"
    assert rollback.result["outcome"] == "rolled_back"
    assert rollback.result["active_runtime_identity"].endswith("community-services-previous")
    assert rollback.result["receipt"]["receipt_class"] == "recovery_receipt"


def test_response_preserves_request_correlation(service) -> None:
    response = create_api(service).dispatch(
        request("runtime_status_query", {"authorized_status_scope": "scope:status:read"}, 99)
    ).to_mapping()
    assert response["request_id"] == "request.99"
    assert response["correlation_id"] == "correlation.99"
    assert response["interface_id"] == "runtime_status_query"
    assert response["version"] == "1.0.0"


def test_service_result_must_be_a_registered_public_model(service) -> None:
    service.query_runtime_status = lambda request: {"state": "active"}
    response = create_api(service).dispatch(
        request("runtime_status_query", {"authorized_status_scope": "scope:status:read"}, 5)
    )
    assert response.status == "rejected"
    assert response.error.code == "invalid_service_result"
