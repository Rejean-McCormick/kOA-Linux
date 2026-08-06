"""Contract evidence for the Audit Broker public API and package payload."""

from __future__ import annotations

import ast
import json
import tomllib
from pathlib import Path

import pytest

from koa_audit_broker.api import (
    API_VERSION,
    INTERFACE_VERSIONS,
    REGISTERED_EVENT_MINIMUM_FIELDS,
    ROUTE_DEFINITIONS,
    ApiRequest,
    AuditDisclosureRequest,
    AuditEventClass,
    AuditEventSubmission,
    AuditReceipt,
    DisclosureOutcome,
    DisclosureResult,
    ModelValidationError,
)

COMPONENT_ROOT = Path(__file__).resolve().parents[2]
REPOSITORY_ROOT = COMPONENT_ROOT.parents[1]
CONTRACT_PATH = REPOSITORY_ROOT / "docs/contracts/components/audit-broker.component.json"
PAYLOAD_PATH = COMPONENT_ROOT / "packaging/payload.toml"
API_ROOT = COMPONENT_ROOT / "src/koa_audit_broker/api"


def _contract() -> dict[str, object]:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def test_comp_audit_001_registered_interfaces_and_events_match_contract() -> None:
    contract = _contract()
    interfaces = contract["interfaces"]
    expected_interfaces = {
        entry["interface_id"]: entry["version"]
        for kind in ("commands", "queries")
        for entry in interfaces[kind]
    }
    expected_events = {
        entry["event_class_id"]: frozenset(entry["minimum_content"])
        for entry in contract["registered_event_classes"]
    }

    assert INTERFACE_VERSIONS == expected_interfaces
    assert {definition.interface_id for definition in ROUTE_DEFINITIONS} == set(
        expected_interfaces
    )
    assert {
        event_class.value: minimum
        for event_class, minimum in REGISTERED_EVENT_MINIMUM_FIELDS.items()
    } == expected_events
    assert {member.value for member in AuditEventClass} == set(expected_events)


def test_comp_audit_002_public_api_has_no_private_cross_component_imports() -> None:
    prohibited_roots = {
        "koa_identity_and_trust",
        "koa_governance_policy_runtime",
        "koa_publication_gateway",
        "koa_resource_governor",
    }
    for source_path in sorted(API_ROOT.glob("*.py")):
        tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
        imports: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
        assert imports.isdisjoint(prohibited_roots), source_path


def test_comp_audit_003_submission_requires_minimum_declared_fields(
    valid_submission_payload: dict[str, object],
) -> None:
    payload = dict(valid_submission_payload)
    event_payload = dict(payload["event_payload"])
    event_payload.pop("decision_ref")
    payload["event_payload"] = event_payload

    with pytest.raises(ModelValidationError, match="missing declared minimum"):
        AuditEventSubmission.from_mapping(payload)

    valid = AuditEventSubmission.from_mapping(valid_submission_payload)
    assert valid.event_class_id is AuditEventClass.POLICY_DECISION_EVENT
    assert valid.idempotency_key == "idempotency-submit-001"


def test_comp_audit_004_disclosure_requires_policy_and_closed_scope(
    valid_disclosure_payload: dict[str, object],
) -> None:
    missing_policy = dict(valid_disclosure_payload)
    missing_policy.pop("policy_decision_ref")
    with pytest.raises(ModelValidationError, match="missing required field"):
        AuditDisclosureRequest.from_mapping(missing_policy)

    broadened = dict(valid_disclosure_payload)
    broadened["undeclared_authority"] = True
    with pytest.raises(ModelValidationError, match="unexpected field"):
        AuditDisclosureRequest.from_mapping(broadened)


def test_comp_audit_005_disclosure_result_cannot_leak_package_on_denial() -> None:
    receipt = AuditReceipt(
        receipt_id="receipt-denial-001",
        request_id="request-denial-001",
        outcome="denied",
        occurred_at="2026-08-06T13:30:00Z",
        reason_codes=("scope_denied",),
    )
    with pytest.raises(ModelValidationError, match="must not include a package"):
        DisclosureResult(
            outcome=DisclosureOutcome.DENIED,
            receipt=receipt,
            effective_scope={},
            disclosure_package={"private_proof": "must-not-escape"},
        )


def test_comp_audit_006_request_and_result_envelopes_are_versioned_and_correlated(
    make_request,
) -> None:
    request = ApiRequest.from_mapping(
        make_request(
            "get_audit_request_status",
            {
                "request_id": "request-disclosure-001",
                "requester_identity": {"identity_ref": "reviewer-001"},
            },
        )
    )
    assert request.version == API_VERSION
    assert request.request_id.startswith("request-")
    assert request.correlation_id.startswith("correlation-")


def test_comp_audit_007_package_payload_is_closed_and_authority_preserving() -> None:
    payload = tomllib.loads(PAYLOAD_PATH.read_text(encoding="utf-8"))
    contract = _contract()

    assert payload["component_id"] == contract["component_id"] == "audit_broker"
    assert payload["component_version"] == contract["version"] == API_VERSION
    assert payload["public_api"] == "koa_audit_broker.api"
    assert payload["authority"]["direct_cross_component_database_access"] is False
    assert payload["authority"]["native_or_automatic_external_ai"] is False
    assert {item["interface_id"] for item in payload["interface"]} == set(
        INTERFACE_VERSIONS
    )
    assert all(item["version"] == API_VERSION for item in payload["interface"])
