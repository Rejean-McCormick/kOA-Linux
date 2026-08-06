"""Integration of public models, dispatcher, and preceding-bundle service port."""

from __future__ import annotations

from koa_publication_gateway.api import ApiRequest, REVALIDATION_DIMENSIONS, create_api


def request(interface_id: str, payload: dict[str, object], number: int) -> ApiRequest:
    return ApiRequest(interface_id, f"request:{number}", f"correlation:{number}", payload)


def test_publication_flow_returns_acknowledged_receipt(service, publication_artifact) -> None:
    response = create_api(service).dispatch(request("publication_request", {"publication_request": publication_artifact}, 1))
    assert response.status == "succeeded"
    assert response.result["state"] == "published"
    assert response.result["decision"]["outcome"] == "allow"
    assert response.result["receipt"]["execution_result"] == "published"
    assert response.result["receipt"]["destination_acknowledgement_ref"] == "uckk-ack:001"


def test_withdrawal_preserves_history_and_exposes_limitation(service) -> None:
    response = create_api(service).dispatch(
        request(
            "revocation_or_withdrawal_notice",
            {
                "publication_request_id": "publication-request:example:001",
                "action": "stop_future_release",
                "authority_ref": "authority:withdrawal:001",
                "affected_scope_ref": "scope:destination:001",
                "reason_code": "CONSENT_REVOKED",
            },
            2,
        )
    )
    assert response.status == "succeeded"
    assert response.result["state"] == "revoked"
    assert response.result["historical_receipt_preserved"] is True
    assert "request-based" in response.result["downstream_limitation"]


def test_status_and_queue_are_restricted_metadata(service) -> None:
    api = create_api(service)
    status = api.dispatch(request("publication_status_query", {"publication_request_id": "publication-request:example:001", "authorized_scope_ref": "scope:status"}, 3))
    queue = api.dispatch(request("queue_inspection", {"authorized_scope_ref": "scope:queue", "limit": 10}, 4))
    assert status.result["restricted_metadata_only"] is True
    assert queue.result["restricted_metadata_only"] is True
    assert "selected_elements" not in str(status.to_mapping())
    assert "selected_elements" not in str(queue.to_mapping())


def test_controlled_retry_revalidates_and_prevents_duplicate_effect(service, retry_payload) -> None:
    response = create_api(service).dispatch(request("controlled_retry", retry_payload, 5))
    assert response.status == "succeeded"
    assert response.result["outcome"] == "accepted"
    assert response.result["revalidation_complete"] is True
    assert response.result["duplicate_effect_prevented"] is True
    assert len(retry_payload["revalidation_dimensions"]) == len(REVALIDATION_DIMENSIONS)


def test_health_contains_no_source_content(service) -> None:
    response = create_api(service).dispatch(request("health", {"authorized_scope_ref": "scope:health"}, 6))
    assert response.status == "succeeded"
    assert response.result["state"] == "healthy"
    assert response.result["source_content_included"] is False


def test_response_preserves_transport_correlation(service) -> None:
    response = create_api(service).dispatch(request("health", {"authorized_scope_ref": "scope:health"}, 99)).to_mapping()
    assert response["interface_id"] == "health"
    assert response["request_id"] == "request:99"
    assert response["correlation_id"] == "correlation:99"
    assert response["version"] == "1.0.0"


def test_unregistered_interface_fails_before_service_call(service) -> None:
    response = create_api(service).dispatch(request("direct_database_write", {}, 7))
    assert response.status == "rejected"
    assert response.error.code == "unregistered_interface"
    assert service.calls == []
