"""Integration evidence for the transport-neutral API/application boundary."""

from __future__ import annotations

from koa_audit_broker.api import (
    ApiOutcome,
    AuditBrokerApi,
    AuditIntegrityFailure,
)


def test_comp_audit_008_retention_and_invalidation_are_append_only(
    service,
    make_request,
) -> None:
    api = AuditBrokerApi(service)
    retention = api.dispatch(
        make_request(
            "apply_retention_action",
            {
                "record_selectors": ["audit-record-001"],
                "action": "hold",
                "policy_or_hold_ref": "hold-001",
                "effective_at": "2026-08-06T13:30:00Z",
            },
        )
    )
    invalidation = api.dispatch(
        make_request(
            "invalidate_audit_record",
            {
                "record_ref": "audit-record-001",
                "source_correction_or_retraction_ref": "source-correction-001",
                "reason": "source record corrected",
                "effective_at": "2026-08-06T13:31:00Z",
            },
        )
    )

    assert retention.outcome is ApiOutcome.SUCCEEDED
    assert retention.result["outcome"] == "applied"
    assert invalidation.outcome is ApiOutcome.SUCCEEDED
    assert invalidation.result["invalidation_record_ref"] == "audit-invalidation-001"
    assert [name for name, _ in service.calls] == [
        "apply_retention_action",
        "invalidate_audit_record",
    ]


def test_comp_audit_009_integrity_failure_is_quarantined(
    service,
    make_request,
    valid_submission_payload,
) -> None:
    service.failures["submit_audit_event"] = AuditIntegrityFailure()
    response = AuditBrokerApi(service).dispatch(
        make_request("submit_audit_event", valid_submission_payload)
    )

    assert response.outcome is ApiOutcome.REJECTED
    assert response.result is None
    assert response.error.code == "integrity_failure"
    assert response.error.details == {"service_outcome": "quarantined"}


def test_comp_audit_010_all_public_interfaces_dispatch_through_service(
    service,
    make_request,
    valid_submission_payload,
    valid_disclosure_payload,
) -> None:
    api = AuditBrokerApi(service)
    requests = [
        make_request("submit_audit_event", valid_submission_payload),
        make_request("request_audit_disclosure", valid_disclosure_payload),
        make_request(
            "apply_retention_action",
            {
                "record_selectors": ["audit-record-001"],
                "action": "archive",
                "policy_or_hold_ref": "retention-policy-001",
                "effective_at": "2026-08-06T13:30:00Z",
            },
        ),
        make_request(
            "invalidate_audit_record",
            {
                "record_ref": "audit-record-001",
                "source_correction_or_retraction_ref": "correction-001",
                "reason": "source correction",
                "effective_at": "2026-08-06T13:30:00Z",
            },
        ),
        make_request(
            "get_audit_record_metadata",
            {
                "record_ref": "audit-record-001",
                "requester_identity": {"identity_ref": "reviewer-001"},
                "purpose": "recourse_review",
            },
        ),
        make_request(
            "get_audit_request_status",
            {
                "request_id": "request-disclosure-001",
                "requester_identity": {"identity_ref": "reviewer-001"},
            },
        ),
        make_request(
            "get_audit_health",
            {"requester_identity": {"identity_ref": "operator-001"}},
        ),
    ]

    responses = [api.dispatch(request) for request in requests]

    assert all(response.outcome is ApiOutcome.SUCCEEDED for response in responses)
    assert [name for name, _ in service.calls] == [
        "submit_audit_event",
        "request_audit_disclosure",
        "apply_retention_action",
        "invalidate_audit_record",
        "get_audit_record_metadata",
        "get_audit_request_status",
        "get_audit_health",
    ]
    assert all(response.terminal for response in responses)
    assert all(
        response.correlation_id == request["correlation_id"]
        for request, response in zip(requests, responses, strict=True)
    )
