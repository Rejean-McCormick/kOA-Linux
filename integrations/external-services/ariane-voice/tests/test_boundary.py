from __future__ import annotations

import socket
import tomllib
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str) -> dict[str, Any]:
    with (ROOT / name).open("rb") as handle:
        return tomllib.load(handle)


@pytest.fixture(autouse=True)
def _deny_network(monkeypatch: pytest.MonkeyPatch) -> None:
    def denied(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("boundary tests must not perform network access")

    monkeypatch.setattr(socket, "create_connection", denied)
    monkeypatch.setattr(socket.socket, "connect", denied)


def test_identity_matches_canonical_integration_contract() -> None:
    integration = _load("integration.toml")
    assert integration["integration_id"] == "ariane-voice"
    assert integration["integration_type"] == "external_voice"
    assert integration["availability"] == "optional"
    assert integration["authority"] == "non_authoritative"
    assert integration["result_role"] == "candidate_navigation_intent"
    assert integration["undeclared_substitution"] == "prohibited"
    assert integration["contract_ref"] == "docs/contracts/integrations/ariane-voice.integration.json"


def test_activation_is_explicit_and_never_background() -> None:
    activation = _load("integration.toml")["activation"]
    assert activation["default_enabled"] is False
    assert activation["trigger"] == "explicit_user_action"
    assert activation["voice_mode_activation_required"] is True
    assert activation["profile_permission_required"] is True
    assert activation["policy_decision_required"] is True
    assert activation["exact_transfer_confirmation_required"] is True
    assert activation["background_activation"] is False
    assert activation["scheduled_activation"] is False
    assert activation["event_triggered_activation"] is False
    assert activation["startup_network_call"] is False


def test_candidate_cannot_execute_or_acquire_authority() -> None:
    integration = _load("integration.toml")
    policy = _load("policy.toml")
    capability = integration["capability"]
    authority = policy["authority"]
    candidate = policy["candidate"]
    assert capability["direct_command_execution"] is False
    assert capability["direct_application_action"] is False
    assert capability["sensitive_action_confirmation"] is False
    assert capability["final_command_authority"] == "ariane"
    assert authority["output_authority"] == "candidate_input_until_ariane_acceptance"
    assert authority["direct_command_execution"] is False
    assert authority["direct_authoritative_mutation"] is False
    assert candidate["deterministic_command_validation_required"] is True
    assert candidate["profile_command_enablement_required"] is True
    assert candidate["direct_execution"] is False
    assert candidate["persistent_authority"] is False


def test_transfer_is_minimized_and_excludes_protected_context() -> None:
    integration = _load("integration.toml")
    policy = _load("policy.toml")
    data_flow = integration["data_flow"]
    transfer = policy["transfer"]
    assert data_flow["selected_outbound_fields"] == [
        "audio_frames",
        "locale",
        "operation_id",
        "correlation_id",
    ]
    assert transfer["allowed_fields"] == data_flow["selected_outbound_fields"]
    assert transfer["preview_required"] is True
    assert transfer["exact_confirmation_required"] is True
    assert transfer["minimization_required"] is True
    assert "secret" in transfer["blocked_data_classes"]
    assert "no_ai" in transfer["blocked_data_classes"]
    assert "credentials" in transfer["blocked_fields"]
    assert "repository_content" in transfer["blocked_fields"]
    assert data_flow["implicit_repository_access"] is False
    assert data_flow["implicit_component_store_access"] is False
    assert data_flow["implicit_secret_access"] is False
    assert data_flow["direct_authoritative_write"] is False


def test_no_concrete_endpoint_or_embedded_secret() -> None:
    integration_text = (ROOT / "integration.toml").read_text(encoding="utf-8").lower()
    policy_text = (ROOT / "policy.toml").read_text(encoding="utf-8").lower()
    combined = integration_text + policy_text
    assert "https://" not in combined
    assert "http://" not in combined
    assert "api_key =" not in combined
    assert "token =" not in combined
    assert "password =" not in combined
    transport = _load("integration.toml")["transport"]
    credentials = _load("policy.toml")["credentials"]
    assert transport["provider_endpoint_source"] == "managed_configuration_reference"
    assert transport["concrete_endpoint_in_repository"] is False
    assert transport["network_policy"] == "default_deny_declared_egress_only"
    assert credentials["managed_secret_reference_only"] is True
    assert credentials["embedded_in_source"] is False
    assert credentials["embedded_in_manifest"] is False
    assert credentials["embedded_in_log"] is False
    assert credentials["embedded_in_receipt"] is False


def test_optional_removal_preserves_local_ariane_navigation() -> None:
    integration = _load("integration.toml")
    removal = integration["removal"]
    offline = integration["offline"]
    assert integration["required_for_local_navigation"] is False
    assert offline["behavior"] == "capability_unavailable"
    assert offline["local_navigation_continues"] is True
    assert offline["local_model_fallback"] is False
    assert offline["alternate_provider_fallback"] is False
    assert removal["revoke_credentials"] is True
    assert removal["close_network_paths"] is True
    assert removal["verify_local_navigation_independence"] is True
    assert removal["reuse_retired_integration_id"] is False


def test_health_and_readiness_are_distinct() -> None:
    health = _load("health.toml")
    state = health["health"]
    readiness = health["readiness"]
    assert health["health_schema_ref"] == "interfaces/health/health-status.schema.json"
    assert health["readiness_schema_ref"] == "interfaces/health/readiness.schema.json"
    assert state["process_liveness_separate_from_readiness"] is True
    assert state["startup_separate_from_provider_availability"] is True
    assert state["provider_unavailable_overall_state"] == "degraded"
    assert state["provider_unavailable_process_liveness"] == "alive"
    assert state["provider_unavailable_readiness"] is False
    assert state["core_system_health_affected"] is False
    assert state["local_ariane_navigation_affected"] is False
    assert readiness["capability_id"] == "external_ariane_voice"
    assert readiness["operation_classes"] == ["voice_candidate_generation"]


def test_required_dependencies_are_declared_not_reimplemented() -> None:
    dependencies = _load("integration.toml")["dependencies"]
    assert dependencies["transport_contract_bundle"] == "B-0014"
    assert dependencies["health_receipt_contract_bundle"] == "B-0015"
    assert dependencies["governance_policy_runtime_bundle"] == "B-0038"
    assert dependencies["audit_broker_bundle"] == "B-0028"
    assert dependencies["ariane_adapter_bundle"] == "B-0060"
    assert dependencies["health_schema_ref"] == "interfaces/health/health-status.schema.json"
    assert dependencies["receipt_schema_ref"] == "interfaces/receipts/receipt-envelope.schema.json"
