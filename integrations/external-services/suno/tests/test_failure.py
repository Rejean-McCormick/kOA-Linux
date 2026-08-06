from __future__ import annotations

from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def load_toml(name: str) -> dict[str, object]:
    with (ROOT / name).open("rb") as handle:
        return tomllib.load(handle)


def failure_map() -> dict[str, dict[str, object]]:
    failures = load_toml("policy.toml")["failure"]
    return {item["id"]: item for item in failures}


def test_failure_matrix_is_closed_and_explicit() -> None:
    failures = failure_map()
    assert set(failures) == {
        "user_not_explicit",
        "transfer_disclosure_unavailable",
        "profile_forbidden",
        "network_unavailable",
        "provider_unavailable",
        "quota_exhausted",
        "provider_refused",
        "invalid_output",
        "import_validation_failed",
        "acceptance_not_granted",
    }
    for failure in failures.values():
        assert failure["authoritative_mutation"] is False
        assert failure["fallback"] == "none"
        assert failure["preserved_capability"]


def test_network_and_provider_loss_preserve_local_mediatheque() -> None:
    failures = failure_map()
    for identifier in ("network_unavailable", "provider_unavailable"):
        assert failures[identifier]["outcome"] == "unavailable"
        assert failures[identifier]["preserved_capability"] == "deterministic_local_mediatheque"


def test_invalid_output_is_quarantined_without_mutation() -> None:
    failure = failure_map()["invalid_output"]
    assert failure["outcome"] == "quarantined"
    assert failure["authoritative_mutation"] is False
    candidate = load_toml("policy.toml")["candidate"]
    assert candidate["integrity_validation_required"] is True
    assert candidate["media_type_validation_required"] is True
    assert candidate["rights_validation_required"] is True
    assert candidate["owning_component_acceptance_required"] is True


def test_no_acceptance_means_candidate_only() -> None:
    failure = failure_map()["acceptance_not_granted"]
    assert failure["outcome"] == "candidate_only"
    assert failure["preserved_capability"] == "authoritative_local_state"


def test_no_silent_substitution_or_hidden_retry() -> None:
    integration = load_toml("integration.toml")
    resilience = load_toml("policy.toml")["resilience"]
    health = load_toml("health.toml")["degradation"]
    assert integration["undeclared_substitution"] == "prohibited"
    assert integration["network"]["provider_substitution"] is False
    assert integration["network"]["local_model_substitution"] is False
    assert resilience["silent_provider_substitution"] is False
    assert resilience["local_model_fallback"] is False
    assert resilience["native_ai_fallback"] is False
    assert resilience["hidden_retry"] is False
    assert health["automatic_fallback"] is False
    assert health["hidden_retry"] is False


def test_health_failure_is_capability_scoped() -> None:
    health = load_toml("health.toml")
    assert health["service_optional"] is True
    assert health["health_affects_core_readiness"] is False
    assert health["health_affects_mediatheque_readiness"] is False
    assert health["health_affects_only_capability"] == "external_media_generation"
    degradation = health["degradation"]
    assert degradation["core_system_state"] == "preserved"
    assert degradation["mediatheque_local_state"] == "preserved"
    assert degradation["authoritative_mutation"] is False


def test_health_reporting_never_discloses_secrets_or_payloads() -> None:
    reporting = load_toml("health.toml")["reporting"]
    assert reporting["secret_values_visible"] is False
    assert reporting["credential_values_visible"] is False
    assert reporting["request_payload_visible"] is False
    assert reporting["candidate_payload_visible"] is False


def test_removal_preserves_accepted_data_and_provenance() -> None:
    removal = load_toml("integration.toml")["removal"]
    assert removal["new_operations_blocked"] is True
    assert removal["active_operations_cancelled_safely"] is True
    assert removal["provider_credentials_removed"] is True
    assert removal["temporary_session_data_cleared"] is True
    assert removal["accepted_output_provenance_preserved"] is True
    assert removal["authoritative_local_data_preserved"] is True
    assert removal["local_core_capabilities_preserved"] is True


def test_failure_evidence_is_required_but_minimized() -> None:
    evidence = load_toml("policy.toml")["evidence"]
    assert evidence["failure_receipt_required"] is True
    assert evidence["removal_evidence_required"] is True
    assert evidence["minimum_operation_metadata_only"] is True
    assert evidence["sensitive_prompt_duplication"] is False
    assert evidence["candidate_media_duplication"] is False
