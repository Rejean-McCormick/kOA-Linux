from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[4]
BOUNDARY = ROOT / "integrations" / "external-services" / "chatgpt"


def _toml(name: str) -> dict[str, Any]:
    with (BOUNDARY / name).open("rb") as stream:
        return tomllib.load(stream)


def _failure_outcome(failure_class: str) -> dict[str, Any]:
    policy = _toml("policy.toml")
    health = _toml("health.toml")
    classes = set(policy["failure_registry"]["classes"])
    if failure_class not in classes:
        raise ValueError(f"undeclared failure class: {failure_class}")
    return {
        "terminal_state": "cancelled" if failure_class == "cancelled" else "unavailable",
        "authoritative_mutation": health["failure"]["authoritative_mutation"],
        "authoritative_success": health["failure"]["authoritative_success"],
        "receipt_required": health["failure"]["failure_receipt_required"],
        "fallback_provider": health["offline"]["fallback_provider"],
        "local_capabilities_continue": policy["degradation"][
            "unrelated_local_capabilities_continue"
        ],
    }


def test_failure_registry_is_closed_and_complete() -> None:
    policy = _toml("policy.toml")
    classes = policy["failure_registry"]["classes"]

    assert classes == [
        "integration_not_registered",
        "profile_not_permitted",
        "user_action_missing",
        "transfer_preview_unavailable",
        "data_not_admitted",
        "provider_terms_unresolved",
        "provider_unavailable",
        "quota_exhausted",
        "provider_refusal",
        "network_failure",
        "timeout",
        "model_or_service_drift",
        "invalid_response",
        "local_validation_failure",
        "acceptance_rejected",
        "cancelled",
    ]
    assert len(classes) == len(set(classes))


@pytest.mark.parametrize(
    "failure_class",
    _toml("policy.toml")["failure_registry"]["classes"],
)
def test_each_declared_failure_is_non_authoritative_and_receipted(failure_class: str) -> None:
    outcome = _failure_outcome(failure_class)

    assert outcome["terminal_state"] in {"cancelled", "unavailable"}
    assert outcome["authoritative_mutation"] is False
    assert outcome["authoritative_success"] is False
    assert outcome["receipt_required"] is True
    assert outcome["fallback_provider"] == "none"
    assert outcome["local_capabilities_continue"] is True


def test_unknown_failure_class_is_rejected() -> None:
    with pytest.raises(ValueError, match="undeclared failure class"):
        _failure_outcome("provider_magic_success")


def test_failure_receipt_contains_only_bounded_metadata() -> None:
    evidence = _toml("policy.toml")["evidence"]
    metadata = evidence["failure_metadata"]

    assert metadata["required"] == [
        "integration_id",
        "operation_id",
        "correlation_id",
        "capability_id",
        "failure_class",
        "terminal_state",
        "occurred_at",
    ]
    assert set(metadata["optional"]) == {
        "provider_request_id",
        "retry_count",
        "timeout_ms",
        "policy_decision_id",
    }
    assert evidence["minimum_metadata_only"] is True
    assert evidence["prompt_content_recorded_by_default"] is False
    assert evidence["response_content_recorded_by_default"] is False
    assert evidence["source_document_content_recorded_by_default"] is False
    assert evidence["credential_material_recorded"] is False


def test_health_and_readiness_are_distinct_and_non_authoritative() -> None:
    config = _toml("health.toml")

    assert config["health"]["states"] == [
        "healthy",
        "degraded",
        "unavailable",
        "disabled",
        "removed",
    ]
    assert config["readiness"]["states"] == ["ready", "not_ready", "disabled", "removed"]
    assert config["health"]["health_is_authority"] is False
    assert config["readiness"]["not_ready_affects"] == ["chatgpt_external_assistance"]
    assert config["readiness"]["unrelated_local_capabilities_ready"] is True


def test_probes_do_not_create_implicit_network_activity() -> None:
    probing = _toml("health.toml")["probing"]

    assert probing["probe_mode"] == "operation_scoped"
    assert probing["background_network_probe"] is False
    assert probing["startup_network_probe"] is False
    assert probing["credential_probe_without_user_operation"] is False
    assert probing["provider_content_probe"] is False
    assert probing["network_calls_in_conformance_tests"] is False
    assert probing["endpoint_from_controlled_configuration"] is True


def test_retry_policy_is_bounded_and_does_not_retry_policy_failures() -> None:
    health = _toml("health.toml")
    retry = health["retries"]
    declared = set(_toml("policy.toml")["failure_registry"]["classes"])
    retryable = set(retry["retryable_failure_classes"])
    non_retryable = set(retry["non_retryable_failure_classes"])

    assert health["timeouts"] == {"attempt_timeout_ms": 30000, "total_timeout_ms": 45000}
    assert retry["maximum_attempts"] == 2
    assert retry["full_jitter"] is True
    assert retry["idempotency_required"] is True
    assert retry["automatic_background_retry"] is False
    assert retryable == {"network_failure", "timeout", "provider_unavailable"}
    assert retryable.isdisjoint(non_retryable)
    assert retryable | non_retryable == declared
    assert {
        "profile_not_permitted",
        "user_action_missing",
        "data_not_admitted",
        "provider_terms_unresolved",
        "provider_refusal",
        "quota_exhausted",
        "model_or_service_drift",
        "invalid_response",
        "local_validation_failure",
        "acceptance_rejected",
        "cancelled",
    }.issubset(non_retryable)


def test_circuit_breaker_is_closed_and_bounded() -> None:
    circuit = _toml("health.toml")["circuit_breaker"]

    assert circuit["states"] == ["closed", "open", "half_open"]
    assert circuit["failure_threshold"] == 3
    assert circuit["failure_window_seconds"] == 60
    assert circuit["open_duration_seconds"] == 120
    assert circuit["half_open_max_probes"] == 1
    assert circuit["half_open_max_concurrency"] == 1
    assert circuit["manual_override_requires_receipt"] is True


def test_offline_state_disables_only_external_assistance() -> None:
    offline = _toml("health.toml")["offline"]

    assert offline == {
        "health_state": "unavailable",
        "readiness_state": "not_ready",
        "assistive_capability_available": False,
        "core_operation_continues": True,
        "authoritative_local_state_preserved": True,
        "fallback_provider": "none",
    }


def test_disabled_and_removed_states_preserve_core_operation() -> None:
    health = _toml("health.toml")

    assert health["disabled"] == {
        "health_state": "disabled",
        "readiness_state": "disabled",
        "new_operations_allowed": False,
        "core_operation_continues": True,
    }
    assert health["removed"] == {
        "health_state": "removed",
        "readiness_state": "removed",
        "new_operations_allowed": False,
        "accepted_output_provenance_preserved": True,
        "core_operation_continues": True,
    }


def test_no_fallback_or_background_queue_is_declared() -> None:
    degradation = _toml("policy.toml")["degradation"]

    assert degradation["mode"] == "capability_unavailable"
    assert degradation["authoritative_local_state_preserved"] is True
    assert degradation["authoritative_success_prohibited"] is True
    assert degradation["provider_substitution_prohibited"] is True
    assert degradation["local_model_substitution_prohibited"] is True
    assert degradation["native_ai_substitution_prohibited"] is True
    assert degradation["queued_background_retry_prohibited"] is True


def test_removal_preserves_prior_provenance_and_clears_runtime_configuration() -> None:
    integration = _toml("integration.toml")["removal"]
    policy = _toml("policy.toml")["removal"]

    assert integration["removable_without_core_failure"] is True
    assert integration["preserve_authoritative_local_data"] is True
    assert integration["preserve_accepted_output_provenance"] is True
    assert integration["remove_credentials_and_endpoint_configuration"] is True
    assert integration["hidden_fallback_prohibited"] is True

    assert policy["disable_new_operations_first"] is True
    assert policy["stop_active_operations_safely"] is True
    assert policy["clear_temporary_provider_session_data"] is True
    assert policy["preserve_authoritative_local_data"] is True
    assert policy["preserve_previously_accepted_provenance"] is True
    assert policy["remove_credentials"] is True
    assert policy["remove_endpoint_configuration"] is True
    assert policy["validate_no_hidden_dependency"] is True
    assert policy["validate_no_fallback"] is True
