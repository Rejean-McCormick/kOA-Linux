from __future__ import annotations

import json
import tomllib
from collections.abc import Mapping, Sequence
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
GAMMA_ROOT = REPOSITORY_ROOT / "integrations" / "external-services" / "gamma"
DOCS_ROOT = REPOSITORY_ROOT / "docs"


def load_toml(name: str) -> dict[str, object]:
    with (GAMMA_ROOT / name).open("rb") as handle:
        return tomllib.load(handle)


def iter_scalar_values(value: object):
    if isinstance(value, Mapping):
        for child in value.values():
            yield from iter_scalar_values(child)
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for child in value:
            yield from iter_scalar_values(child)
    else:
        yield value


def iter_keys(value: object):
    if isinstance(value, Mapping):
        for key, child in value.items():
            yield str(key)
            yield from iter_keys(child)
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for child in value:
            yield from iter_keys(child)


def test_contract_identity_and_closed_capability() -> None:
    contract_path = DOCS_ROOT / "contracts" / "integrations" / "gamma.integration.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    integration = load_toml("integration.toml")

    declared = integration["integration"]
    assert declared["integration_id"] == contract["integration_id"] == "gamma"
    assert declared["contract_version"] == contract["version"] == "1.0.0"
    assert declared["integration_type"] == contract["integration_type"]
    assert declared["authority"] == contract["authority"] == "non_authoritative"
    assert declared["availability"] == contract["availability"] == "optional"

    capability = integration["capability"]
    assert capability["capability_id"] == "presentation.generate_candidate"
    assert capability["trigger"] == "explicit_user_action"
    assert capability["result_class"] == "candidate_presentation_artifact"
    assert capability["result_authority"] == "non_authoritative_candidate_source"
    assert capability["background_invocation_allowed"] is False
    assert capability["automatic_ingestion_invocation_allowed"] is False
    assert capability["direct_authoritative_store_write_allowed"] is False
    assert capability["automatic_publication_allowed"] is False


def test_activation_requires_local_authorities() -> None:
    integration = load_toml("integration.toml")
    activation = integration["activation"]
    assert activation == {
        "default_enabled": False,
        "profile_permission_required": True,
        "governance_decision_required": True,
        "audit_receipts_required": True,
        "provider_terms_resolution_required": True,
        "credentials_resolution_required": True,
        "endpoint_resolution_required": True,
        "implicit_enablement_allowed": False,
    }

    dependencies = integration["dependencies"]
    assert dependencies["policy_component"] == "governance-policy-runtime"
    assert dependencies["audit_component"] == "audit-broker"
    declared_paths = {
        *dependencies["transport_schemas"],
        *dependencies["health_schemas"],
        *dependencies["receipt_schemas"],
    }
    expected_paths = {
        "interfaces/transport/event-envelope.schema.json",
        "interfaces/transport/error-envelope.schema.json",
        "interfaces/transport/version-negotiation.schema.json",
        "interfaces/health/health-status.schema.json",
        "interfaces/health/readiness.schema.json",
        "interfaces/receipts/receipt-envelope.schema.json",
        "interfaces/receipts/correlation.schema.json",
    }
    assert declared_paths == expected_paths


def test_network_and_work_are_finitely_bounded() -> None:
    integration = load_toml("integration.toml")
    network = integration["network"]
    limits = integration["limits"]

    assert network["default_policy"] == "deny"
    assert network["direction"] == "outbound_only"
    assert network["protocol"] == "https"
    assert network["endpoint_reference"].startswith("config://")
    assert "://api." not in network["endpoint_reference"]
    assert network["hard_coded_endpoint_allowed"] is False
    assert network["inbound_callbacks_allowed"] is False
    assert network["remote_administration_allowed"] is False
    assert network["certificate_validation_required"] is True

    assert 0 < limits["request_timeout_seconds"] <= 120
    assert limits["maximum_attempts"] == 1
    assert limits["automatic_retry_allowed"] is False
    assert 0 < limits["maximum_concurrency"] <= 4
    assert limits["maximum_queued_requests"] == 0
    assert 0 < limits["maximum_request_bytes"] <= 25 * 1024 * 1024
    assert 0 < limits["maximum_response_bytes"] <= 100 * 1024 * 1024
    assert limits["provider_rate_limit_behavior"] == "fail_closed_and_report"


def test_transfer_and_candidate_authority_are_separate() -> None:
    policy = load_toml("policy.toml")
    transfer = policy["transfer"]
    candidate = policy["candidate"]
    prohibited_effects = candidate["prohibited_effects"]

    assert policy["policy"]["default_decision"] == "deny"
    assert policy["policy"]["explicit_user_action_required"] is True
    assert policy["policy"]["transfer_preview_required"] is True
    assert transfer["source_selection"] == "explicit_objects_and_fields_only"
    assert transfer["data_minimization_required"] is True
    assert "no_ai" in transfer["prohibited_data_classes"]
    assert "secret" in transfer["prohibited_data_classes"]
    assert "credential" in transfer["prohibited_data_classes"]
    assert all(
        transfer[field] is False
        for field in (
            "implicit_repository_access",
            "implicit_component_store_access",
            "implicit_tenant_access",
            "implicit_profile_access",
            "implicit_host_access",
        )
    )

    assert candidate["status"] == "non_authoritative"
    assert candidate["controlled_import_required"] is True
    assert candidate["destination_validation_required"] is True
    assert candidate["explicit_acceptance_required"] is True
    assert all(prohibited_effects.values())
    assert policy["publication"]["separate_workflow_required"] is True
    assert policy["publication"]["publication_gateway_required"] is True
    assert policy["publication"]["generation_implies_consent"] is False


def test_no_secret_or_provider_endpoint_is_embedded() -> None:
    forbidden_key_fragments = ("api_key", "token_value", "password", "private_key")
    forbidden_value_fragments = ("sk-", "bearer ", "api.gamma", "gamma.app/api")

    for name in ("integration.toml", "policy.toml", "health.toml"):
        parsed = load_toml(name)
        normalized_keys = {key.lower() for key in iter_keys(parsed)}
        assert not any(
            fragment in key
            for key in normalized_keys
            for fragment in forbidden_key_fragments
        )
        for scalar in iter_scalar_values(parsed):
            if isinstance(scalar, str):
                lowered = scalar.lower()
                assert not any(fragment in lowered for fragment in forbidden_value_fragments)

    credential_ref = load_toml("policy.toml")["credentials"]["secret_reference"]
    assert credential_ref == "secret://integrations/gamma/credential"


def test_directory_contains_boundary_declarations_and_tests_only() -> None:
    relative_files = {
        path.relative_to(GAMMA_ROOT).as_posix()
        for path in GAMMA_ROOT.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }
    assert relative_files == {
        "README.md",
        "health.toml",
        "integration.toml",
        "policy.toml",
        "tests/test_boundary.py",
        "tests/test_failure.py",
    }
    assert not any(path.suffix in {".whl", ".jar", ".so", ".dll"} for path in GAMMA_ROOT.rglob("*"))
