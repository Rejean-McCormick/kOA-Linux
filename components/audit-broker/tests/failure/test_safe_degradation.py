"""Safe-degradation evidence for the Audit Broker public API."""

from __future__ import annotations

import json
from pathlib import Path

from koa_audit_broker.api import (
    ApiOutcome,
    AuditBrokerApi,
    RequiredAuthorityUnavailable,
)

COMPONENT_ROOT = Path(__file__).resolve().parents[2]
REPOSITORY_ROOT = COMPONENT_ROOT.parents[1]
CONTRACT_PATH = REPOSITORY_ROOT / "docs/contracts/components/audit-broker.component.json"


def test_comp_audit_011_health_output_excludes_protected_record_content(
    service,
    make_request,
) -> None:
    response = AuditBrokerApi(service).dispatch(
        make_request(
            "get_audit_health",
            {"requester_identity": {"identity_ref": "operator-001"}},
        )
    )
    serialized = json.dumps(response.to_dict(), sort_keys=True)

    assert response.outcome is ApiOutcome.SUCCEEDED
    for prohibited in (
        "event_payload",
        "private_proof",
        "subject_references",
        "protected_content",
    ):
        assert prohibited not in serialized


def test_comp_audit_012_secret_fields_and_external_ai_are_absent(
    service,
    make_request,
    valid_submission_payload,
) -> None:
    payload = dict(valid_submission_payload)
    event_payload = dict(payload["event_payload"])
    event_payload["api_key"] = "must-not-be-accepted"
    payload["event_payload"] = event_payload

    response = AuditBrokerApi(service).dispatch(
        make_request("submit_audit_event", payload)
    )
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    assert response.outcome is ApiOutcome.REJECTED
    assert response.error.code == "secret_field_prohibited"
    assert service.calls == []
    assert contract["external_integrations"]["native_or_automatic_use"] is False
    assert contract["external_integrations"]["allowed"] == []


def test_comp_audit_013_missing_authority_and_internal_errors_fail_closed(
    service,
    make_request,
    valid_disclosure_payload,
) -> None:
    service.failures["request_audit_disclosure"] = RequiredAuthorityUnavailable(
        "governance_policy_runtime"
    )
    blocked = AuditBrokerApi(service).dispatch(
        make_request("request_audit_disclosure", valid_disclosure_payload)
    )
    assert blocked.outcome is ApiOutcome.REJECTED
    assert blocked.result is None
    assert blocked.error.code == "required_authority_unavailable"
    assert "governance_policy_runtime" not in json.dumps(blocked.to_dict())

    service.failures["request_audit_disclosure"] = RuntimeError(
        "protected payload value must never escape"
    )
    failed = AuditBrokerApi(service).dispatch(
        make_request("request_audit_disclosure", valid_disclosure_payload)
    )
    assert failed.outcome is ApiOutcome.FAILED
    assert failed.error.code == "internal_failure"
    assert "protected payload value" not in json.dumps(failed.to_dict())


def test_comp_audit_014_contract_claims_have_registered_tests_and_block_unknown_interfaces(
    service,
    make_request,
) -> None:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    expected_test_ids = {
        f"TEST-COMP-AUDIT-{index:03d}" for index in range(1, 15)
    }

    assert set(contract["conformance"]["required_test_ids"]) == expected_test_ids
    assert set(contract["conformance"]["test_expectations"]) == expected_test_ids
    assert contract["conformance"]["unsupported_claim_result"] == "blocked"

    response = AuditBrokerApi(service).dispatch(
        make_request("undeclared_audit_operation", {})
    )
    assert response.outcome is ApiOutcome.REJECTED
    assert response.error.code == "unregistered_interface"
    assert service.calls == []
