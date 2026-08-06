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
        raise AssertionError("failure tests must be hermetic")

    monkeypatch.setattr(socket, "create_connection", denied)
    monkeypatch.setattr(socket.socket, "connect", denied)


def test_limits_retries_and_queueing_are_bounded() -> None:
    integration = _load("integration.toml")
    limits = integration["limits"]
    retry = integration["retry"]
    breaker = integration["circuit_breaker"]
    assert 0 < limits["max_audio_duration_seconds"] <= 60
    assert 0 < limits["max_audio_bytes"] <= 4 * 1024 * 1024
    assert 0 < limits["connect_timeout_seconds"] <= limits["operation_timeout_seconds"]
    assert limits["max_concurrent_operations"] == 1
    assert limits["queue_enabled"] is False
    assert limits["max_queued_operations"] == 0
    assert retry["max_attempts"] == 1
    assert retry["automatic_retry"] is False
    assert retry["replay_requires_new_user_action"] is True
    assert breaker["enabled"] is True
    assert breaker["failure_threshold"] > 0
    assert breaker["open_seconds"] > 0
    assert breaker["half_open_max_operations"] == 1


def test_failure_never_mutates_authoritative_state_or_substitutes() -> None:
    policy = _load("policy.toml")
    failure = policy["failure"]
    assert failure["authoritative_mutation_on_failure"] is False
    assert failure["silent_fallback"] is False
    assert failure["alternate_provider"] is False
    assert failure["local_model_substitution"] is False
    assert failure["stale_credential_fallback"] is False
    assert failure["weaker_policy_fallback"] is False
    assert failure["broader_transfer_fallback"] is False
    assert failure["failure_scope"] == "external_voice_capability_only"


def test_provider_probe_is_not_implicit_or_background() -> None:
    provider = _load("health.toml")["probe"]["provider"]
    assert provider["kind"] == "explicit_operation_or_operator_check"
    assert provider["network_access"] is True
    assert provider["run_on_startup"] is False
    assert provider["run_in_background"] is False
    assert provider["user_operation_may_trigger"] is True
    assert provider["operator_check_may_trigger"] is True
    assert 0 < provider["timeout_seconds"] <= 10


def test_every_declared_terminal_failure_has_namespaced_reason_code() -> None:
    evidence = _load("health.toml")["failure_evidence"]
    reason_codes = evidence["reason_codes"]
    expected = {
        "profile_not_permitted",
        "policy_denied",
        "user_cancelled",
        "data_ineligible",
        "transfer_failed",
        "provider_timeout",
        "provider_unavailable",
        "provider_rate_limited",
        "response_invalid",
        "candidate_incomplete",
        "candidate_ambiguous",
        "candidate_unrecognized",
        "candidate_unsafe",
        "local_validation_failed",
        "circuit_open",
        "offline",
    }
    assert set(reason_codes) == expected
    assert len(set(reason_codes.values())) == len(reason_codes)
    assert all(value.startswith("ariane_voice.") for value in reason_codes.values())
    assert evidence["emit_for_each_terminal_failure"] is True
    assert evidence["reason_codes_required"] is True
    assert evidence["correlation_required"] is True


def test_failure_receipts_are_minimized_and_schema_bound() -> None:
    health = _load("health.toml")
    evidence = health["failure_evidence"]
    policy_evidence = _load("policy.toml")["evidence"]
    assert health["receipt_schema_ref"] == "interfaces/receipts/receipt-envelope.schema.json"
    assert health["correlation_schema_ref"] == "interfaces/receipts/correlation.schema.json"
    assert evidence["receipt_class"] == "transfer_receipt"
    assert evidence["transition_type"] == "external_voice_operation"
    assert evidence["commit_state"] == "not_applicable"
    assert set(evidence["terminal_outcomes"]) == {"failed", "cancelled", "denied", "expired"}
    assert evidence["raw_audio_in_receipt"] is False
    assert evidence["transcript_in_receipt"] is False
    assert evidence["candidate_parameters_in_receipt"] is False
    assert evidence["credentials_in_receipt"] is False
    assert policy_evidence["failure_receipt_required"] is True
    assert policy_evidence["raw_audio_in_receipt"] is False
    assert policy_evidence["credentials_in_receipt"] is False


def test_offline_and_removal_close_only_external_voice() -> None:
    integration = _load("integration.toml")
    health = _load("health.toml")["health"]
    offline = integration["offline"]
    removal = integration["removal"]
    assert offline["behavior"] == "capability_unavailable"
    assert offline["local_navigation_continues"] is True
    assert offline["deferred_network_queue"] is False
    assert offline["local_model_fallback"] is False
    assert offline["alternate_provider_fallback"] is False
    assert health["core_system_health_affected"] is False
    assert health["local_ariane_navigation_affected"] is False
    assert removal["stop_adapter"] is True
    assert removal["preserve_required_evidence"] is True
    assert removal["reconcile_pending_candidates"] is True


def test_observability_excludes_payload_and_secret_content() -> None:
    observability = _load("health.toml")["observability"]
    required_flags = [
        "operation_id_required",
        "correlation_id_required",
        "profile_ref_required",
        "endpoint_reference_required",
        "result_required",
        "duration_required",
        "retry_state_required",
    ]
    assert all(observability[name] is True for name in required_flags)
    assert observability["raw_audio_logged"] is False
    assert observability["transcript_logged_by_default"] is False
    assert observability["candidate_parameters_logged_by_default"] is False
    assert observability["secret_values_logged"] is False
