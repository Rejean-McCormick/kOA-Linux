from __future__ import annotations

import socket
import tomllib
import urllib.request
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
GAMMA_ROOT = REPOSITORY_ROOT / "integrations" / "external-services" / "gamma"


def load_toml(name: str) -> dict[str, object]:
    with (GAMMA_ROOT / name).open("rb") as handle:
        return tomllib.load(handle)


def deny_network(*_args: object, **_kwargs: object) -> None:
    raise AssertionError("Gamma boundary tests must not perform network access")


def test_loading_boundary_performs_no_network_access(monkeypatch) -> None:
    monkeypatch.setattr(socket, "create_connection", deny_network)
    monkeypatch.setattr(urllib.request, "urlopen", deny_network)

    assert load_toml("integration.toml")["integration"]["integration_id"] == "gamma"
    assert load_toml("policy.toml")["policy"]["default_decision"] == "deny"
    assert load_toml("health.toml")["health"]["active_network_probe"] is False


def test_unresolved_external_authority_blocks_operation() -> None:
    integration = load_toml("integration.toml")
    policy = load_toml("policy.toml")
    failure = integration["failure"]
    terms = policy["provider_terms"]

    assert terms["resolution"] == "required_before_enablement_and_transfer"
    for key in (
        "service_terms",
        "data_retention",
        "training_or_secondary_reuse",
        "data_location",
        "account_configuration",
    ):
        assert terms[key] == "runtime_authority_required"
    assert terms["unresolved_result"] == "blocked"
    assert failure["policy_indeterminate"] == "blocked"
    assert failure["audit_unavailable"] == "blocked"
    assert failure["terms_unresolved"] == "blocked"
    assert failure["credentials_unavailable"] == "blocked"
    assert failure["endpoint_unresolved"] == "blocked"


def test_failure_never_mutates_authority_or_selects_substitute() -> None:
    failure = load_toml("integration.toml")["failure"]
    assert failure["provider_unavailable"] == "capability_unavailable"
    assert failure["offline"] == "capability_unavailable"
    assert failure["authoritative_mutation_on_failure"] is False
    assert failure["silent_substitution"] is False
    assert failure["alternate_provider_fallback"] is False
    assert failure["local_model_fallback"] is False
    assert failure["transport_timeout"] == "unknown_result_requires_user_reconciliation"


def test_health_and_readiness_preserve_unrelated_core() -> None:
    health = load_toml("health.toml")
    states = health["states"]

    assert health["health"]["active_network_probe"] is False
    assert health["health"]["provider_probe_on_status_request"] is False
    assert states["disabled"]["healthy"] is True
    assert states["disabled"]["ready"] is False
    assert states["disabled"]["core_impact"] == "none"
    for name in ("degraded", "blocked", "unavailable", "unknown_result"):
        assert states[name]["ready"] is False
        assert states[name]["core_impact"] == "gamma_capability_only"

    readiness = health["readiness"]
    assert readiness["provider_reachability_is_sufficient"] is False
    assert readiness["credential_presence_is_sufficient"] is False
    assert readiness["network_reachability_is_sufficient"] is False
    assert health["offline"]["local_capabilities_preserved"] is True
    assert health["offline"]["queued_for_automatic_replay"] is False
    assert health["offline"]["alternate_provider_selected"] is False


def test_timeout_cannot_trigger_automatic_retry() -> None:
    integration = load_toml("integration.toml")
    limits = integration["limits"]
    failure = integration["failure"]

    assert limits["maximum_attempts"] == 1
    assert limits["automatic_retry_allowed"] is False
    assert limits["maximum_queued_requests"] == 0
    assert failure["transport_timeout"] == "unknown_result_requires_user_reconciliation"


def test_failure_evidence_is_minimized_and_explicit() -> None:
    health = load_toml("health.toml")
    evidence = health["failure_evidence"]
    integration_evidence = load_toml("integration.toml")["evidence"]

    assert evidence["authoritative_state_mutated_must_be"] is False
    assert evidence["include_raw_payload"] is False
    assert evidence["include_secret"] is False
    assert "failure_class" in evidence["required_fields"]
    assert "correlation_id" in evidence["required_fields"]
    assert integration_evidence["failure_receipt_required"] is True
    assert integration_evidence["raw_payloads_in_receipts"] is False


def test_removal_is_complete_and_identifier_is_not_reused() -> None:
    lifecycle = load_toml("integration.toml")["lifecycle"]
    removal = load_toml("policy.toml")["removal"]

    assert lifecycle["removal_breaks_core"] is False
    assert lifecycle["retired_identifier_reuse_allowed"] is False
    assert lifecycle["preserve_accepted_output_provenance"] is True
    assert lifecycle["reconcile_pending_operations_before_removal"] is True
    assert all(
        removal[key] is True
        for key in (
            "revoke_credentials",
            "close_network_paths",
            "stop_adapter",
            "preserve_required_evidence",
            "reconcile_pending_candidates",
            "verify_native_capability_independence",
        )
    )
    assert removal["silent_provider_replacement"] is False
