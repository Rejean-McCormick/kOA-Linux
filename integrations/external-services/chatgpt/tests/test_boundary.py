from __future__ import annotations

import ast
import json
import re
import tomllib
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[4]
BOUNDARY = ROOT / "integrations" / "external-services" / "chatgpt"
CONTRACT_PATH = ROOT / "docs" / "contracts" / "integrations" / "chatgpt.integration.json"

EXPECTED_FILES = {
    "README.md",
    "health.toml",
    "integration.toml",
    "policy.toml",
    "tests/test_boundary.py",
    "tests/test_failure.py",
}

EXPECTED_CAPABILITIES = {
    "AI-CAP-001": "candidate_drafting",
    "AI-CAP-002": "candidate_summarization",
    "AI-CAP-003": "candidate_translation",
    "AI-CAP-004": "candidate_extraction",
    "AI-CAP-005": "candidate_reconciliation",
    "AI-CAP-008": "development_assistance",
}

FORBIDDEN_IMPORT_ROOTS = {
    "aiohttp",
    "httpx",
    "openai",
    "requests",
    "socket",
    "urllib3",
}


def _toml(name: str) -> dict[str, Any]:
    with (BOUNDARY / name).open("rb") as stream:
        return tomllib.load(stream)


def _contract() -> dict[str, Any]:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def _source_files() -> list[Path]:
    return sorted(
        path
        for path in BOUNDARY.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    )


def test_exact_bundle_paths_exist() -> None:
    relative = {path.relative_to(BOUNDARY).as_posix() for path in _source_files()}
    assert relative == EXPECTED_FILES


def test_toml_files_parse_and_identify_the_same_boundary() -> None:
    integration = _toml("integration.toml")
    policy = _toml("policy.toml")
    health = _toml("health.toml")

    assert integration["schema_version"] == 1
    assert policy["schema_version"] == 1
    assert health["schema_version"] == 1
    assert {integration["integration_id"], policy["integration_id"], health["integration_id"]} == {
        "chatgpt"
    }
    assert {integration["version"], policy["version"], health["version"]} == {"1.0.0"}
    assert {integration["status"], policy["status"], health["status"]} == {"active"}


def test_integration_matches_the_canonical_contract() -> None:
    integration = _toml("integration.toml")
    contract = _contract()

    for key in (
        "integration_id",
        "title",
        "version",
        "status",
        "integration_type",
        "role",
        "authority",
        "undeclared_substitution",
        "availability",
    ):
        assert integration[key] == contract[key]

    assert integration["contract_ref"] == "docs/contracts/integrations/chatgpt.integration.json"
    assert integration["output_authority"] == "candidate_input_only"
    assert integration["enabled_by_default"] is False
    assert integration["core_dependency"] is False
    assert integration["native_dependency"] is False


def test_capability_scope_is_closed_and_candidate_only() -> None:
    capabilities = _toml("integration.toml")["capabilities"]
    actual = {item["capability_id"]: item["name"] for item in capabilities}

    assert actual == EXPECTED_CAPABILITIES
    assert len(capabilities) == len(EXPECTED_CAPABILITIES)
    assert all(item["output_authority"] == "candidate_input_only" for item in capabilities)
    assert all(item["output_class"].startswith("candidate_") for item in capabilities)


def test_only_explicit_user_invocation_is_declared() -> None:
    access = _toml("integration.toml")["access"]
    activation = _toml("policy.toml")["activation"]

    assert access["invocation_modes"] == ["explicit_user_action"]
    assert access["background_invocation"] is False
    assert access["scheduled_invocation"] is False
    assert access["autonomous_invocation"] is False
    assert access["continuous_activation"] is False
    assert access["operation_confirmation_required"] is True

    assert activation["explicit_user_action_required"] is True
    assert activation["operation_scoped_confirmation_required"] is True
    assert activation["background_activation_prohibited"] is True
    assert activation["scheduled_activation_prohibited"] is True
    assert activation["autonomous_activation_prohibited"] is True


def test_data_transfer_is_explicit_minimized_and_closed() -> None:
    integration = _toml("integration.toml")
    boundary = integration["data_boundary"]
    classifications = boundary["classification"]
    transfer = _toml("policy.toml")["transfer"]

    assert boundary["transfer_preview_required"] is True
    assert boundary["explicit_source_selection_required"] is True
    assert boundary["explicit_field_selection_required"] is True
    assert boundary["admission_required"] is True
    assert boundary["minimization_required"] is True
    assert boundary["hidden_context_transfer"] is False
    assert boundary["conversation_history_transfer_by_default"] is False
    assert classifications["permitted_by_default"] == ["public"]
    assert set(classifications["prohibited"]) == {"secret", "no-AI"}
    assert {
        "internal",
        "personal",
        "sensitive",
        "restricted",
        "cultural_rights_restricted",
    } == set(classifications["requires_explicit_authority"])

    assert transfer["only_explicitly_admitted_data"] is True
    assert transfer["minimum_necessary_representation"] is True
    assert transfer["secret_transfer_prohibited"] is True
    assert transfer["hidden_authority_context_prohibited"] is True
    assert transfer["unrelated_tenant_data_prohibited"] is True


@pytest.mark.parametrize(
    "field",
    [
        "repository_access",
        "component_store_access",
        "tenant_access",
        "profile_state_access",
        "host_access",
        "secret_access",
    ],
)
def test_implicit_access_is_prohibited(field: str) -> None:
    assert _toml("integration.toml")["data_boundary"][field] is False


def test_network_boundary_contains_no_hidden_endpoint_or_ingress() -> None:
    integration = _toml("integration.toml")
    network = integration["network"]
    credentials = integration["credentials"]

    assert network == {
        "direction": "egress_only",
        "transport": "https",
        "tls_required": True,
        "endpoint_source": "controlled_runtime_configuration",
        "hard_coded_endpoint": False,
        "ingress_listener": False,
        "callbacks": False,
        "webhooks": False,
        "general_network_access": False,
    }
    assert credentials["inline_credentials"] is False
    assert credentials["credential_source"] == "registered_secret_reference"
    assert credentials["credential_reuse_for_other_services"] is False

    text = "\n".join(
        (BOUNDARY / name).read_text(encoding="utf-8")
        for name in ("README.md", "health.toml", "integration.toml", "policy.toml")
    )
    assert re.search(r"https?://", text, flags=re.IGNORECASE) is None
    assert re.search(r"\bsk-[A-Za-z0-9_-]{8,}", text) is None
    assert "api_key =" not in text.lower()
    assert "bearer " not in text.lower()


def test_provider_assurance_is_resolved_at_operation_time() -> None:
    assurance = _toml("integration.toml")["provider_assurance"]

    assert assurance["current_terms_resolution_required"] is True
    assert assurance["retention_resolution_required"] is True
    assert assurance["training_or_secondary_reuse_resolution_required"] is True
    assert assurance["unresolved_assurance_blocks_operation"] is True
    assert assurance["model_or_service_drift_requires_reevaluation"] is True
    assert assurance["endpoint_drift_requires_reevaluation"] is True
    assert assurance["policy_drift_requires_reevaluation"] is True


def test_no_authoritative_effect_is_declared() -> None:
    integration = _toml("integration.toml")
    prohibited = integration["prohibited_effects"]
    authority = _toml("policy.toml")["authority"]

    assert all(value is False for value in prohibited.values())
    assert authority["output_authority"] == "candidate_input_only"
    assert all(value is False for key, value in authority.items() if key != "output_authority")


def test_output_requires_controlled_adoption_and_separate_publication() -> None:
    integration = _toml("integration.toml")
    adoption = integration["adoption"]
    policy = _toml("policy.toml")

    assert adoption["controlled_import_required"] is True
    assert adoption["owning_component_validation_required"] is True
    assert adoption["owning_component_acceptance_required"] is True
    assert adoption["human_or_accountable_review_required"] is True
    assert adoption["automatic_authoritative_adoption"] is False

    assert policy["publication"] == {
        "generation_is_separate_from_publication": True,
        "publication_gateway_required": True,
        "publication_request_required": True,
        "publication_policy_decision_required": True,
        "publication_receipt_required": True,
        "generation_implies_publication_consent": False,
    }


def test_tools_are_disabled_and_unrestricted_execution_is_prohibited() -> None:
    tools = _toml("policy.toml")["tools"]

    assert tools["tools_enabled_by_default"] is False
    assert tools["unrestricted_tools_prohibited"] is True
    assert tools["arbitrary_shell_prohibited"] is True
    assert tools["direct_database_access_prohibited"] is True
    assert tools["protected_signing_access_prohibited"] is True
    assert tools["node_agent_operations_prohibited"] is True
    assert tools["general_network_access_prohibited"] is True


def test_conformance_code_has_no_network_or_provider_sdk_import() -> None:
    for path in sorted((BOUNDARY / "tests").glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        assert imported.isdisjoint(FORBIDDEN_IMPORT_ROOTS), (path, imported)


def test_readme_states_non_authority_and_hermetic_tests() -> None:
    readme = (BOUNDARY / "README.md").read_text(encoding="utf-8")

    for phrase in (
        "non-authoritative",
        "explicit user action",
        "candidate material",
        "no network request",
        "No endpoint or credential is stored here",
        "Publication remains a separate operation",
    ):
        assert phrase in readme
