"""Contract evidence for Governance Policy Runtime's public API."""

from __future__ import annotations

import json
from pathlib import Path
import tomllib

import pytest

from koa_governance_policy_runtime.api import (
    API_VERSION,
    DECISION_CONTEXT_FIELDS,
    INTERFACE_VERSIONS,
    ROUTE_DEFINITIONS,
    DecisionClass,
    DecisionReceipt,
    DecisionResult,
    ModelValidationError,
    ObligationType,
    PolicyBundleStageResponse,
    PolicySetActivationResponse,
)

COMPONENT_ROOT = Path(__file__).resolve().parents[2]
REPOSITORY_ROOT = COMPONENT_ROOT.parents[1]
CONTRACT_PATH = REPOSITORY_ROOT / "docs/contracts/components/governance-policy-runtime.component.json"
SCHEMA_PATH = REPOSITORY_ROOT / "docs/contracts/artifact-contracts/policy-bundle.schema.json"
PAYLOAD_PATH = COMPONENT_ROOT / "packaging/payload.toml"


def _contract() -> dict:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def test_sys_gov_001_public_interface_registry_matches_contract() -> None:
    contract = _contract()
    expected = {item["name"]: item["interface_id"] for item in contract["provided_interfaces"]}
    assert {name: route.contract_interface_id for name, route in ROUTE_DEFINITIONS.items()} == expected
    assert set(INTERFACE_VERSIONS) == set(expected)
    assert set(INTERFACE_VERSIONS.values()) == {API_VERSION}


def test_sys_gov_002_command_and_event_identifiers_remain_closed() -> None:
    contract = _contract()
    assert [(item["command_id"], item["name"]) for item in contract["commands"]] == [
        ("CMD-GOV-POL-001", "evaluate_policy"),
        ("CMD-GOV-POL-002", "stage_policy_bundle"),
        ("CMD-GOV-POL-003", "activate_policy_set"),
        ("CMD-GOV-POL-004", "rollback_policy_set"),
    ]
    assert [item["event_id"] for item in contract["published_events"]] == [f"EVENT-GOV-POL-{index:03d}" for index in range(1, 11)]


def test_sys_gov_003_decision_classes_and_bounded_context_match_contract() -> None:
    contract = _contract()
    assert {item.value for item in DecisionClass} == set(contract["canonical_responsibility"]["decision_classes"])
    for decision_class in DecisionClass:
        assert DECISION_CONTEXT_FIELDS[decision_class] == frozenset(contract["decision_semantics"][decision_class.value]["required_context"])


def test_sys_gov_004_result_and_obligation_enums_match_contract() -> None:
    output = _contract()["output_contracts"]["policy_evaluation_response"]
    assert {item.value for item in DecisionResult} == set(output["result_enum"])
    assert {item.value for item in ObligationType} == set(output["obligation_types"])


def test_sys_gov_005_decision_receipt_is_not_execution_evidence(service, make_request, valid_evaluation_payload) -> None:
    from koa_governance_policy_runtime.api import GovernancePolicyRuntimeApi

    response = GovernancePolicyRuntimeApi(service).dispatch(make_request("evaluate_decision", valid_evaluation_payload))
    contract = _contract()["output_contracts"]["decision_receipt"]
    serialized = json.dumps(response.result, sort_keys=True)
    assert contract["receipt_is_execution_evidence"] is False
    assert "execution_payload" not in serialized
    assert "private_key" not in serialized
    assert response.result["receipt"]["receipt_id"] == "decision-receipt-001"


def test_sys_gov_006_staging_and_activation_models_enforce_atomic_authority() -> None:
    with pytest.raises(ModelValidationError, match="must not activate"):
        PolicyBundleStageResponse("bundle-1", "set-2", "plan-1", active=True)
    with pytest.raises(ModelValidationError, match="must be atomic"):
        PolicySetActivationResponse("set-1", "set-2", "release-1", "receipt-1", atomic=False)


def test_sys_gov_007_payload_preserves_component_authority_and_paths() -> None:
    payload = tomllib.loads(PAYLOAD_PATH.read_text(encoding="utf-8"))
    contract = _contract()
    assert payload["component_id"] == contract["component_id"] == "governance_policy_runtime"
    assert payload["component_version"] == contract["version"] == API_VERSION
    assert payload["authority"]["partial_policy_authority"] is False
    assert payload["authority"]["direct_cross_component_database_access"] is False
    assert payload["authority"]["native_or_automatic_external_ai"] is False
    assert payload["installation"]["state_root"] == "/var/lib/koa/policies"
    assert payload["installation"]["socket_path"] == "/run/koa/sockets/governance-policy-runtime.sock"
    assert {item["interface_id"] for item in payload["interface"]} == set(INTERFACE_VERSIONS)


def test_sys_gov_008_policy_bundle_schema_identifies_governance_artifact_without_activation_grant() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    assert schema["properties"]["artifact_type"]["const"] == "governance_policy_bundle"
    assert schema["properties"]["artifact_class"]["const"] == "policy_bundle"
    assert schema["properties"]["release_channel"]["const"] == "governance"
    assert "does not grant activation authority" in schema["description"]
