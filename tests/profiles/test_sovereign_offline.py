from __future__ import annotations

import json
from pathlib import Path


def _root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "docs/contracts/profiles").is_dir():
            return candidate
    raise RuntimeError("repository root with docs/contracts/profiles was not found")


ROOT = _root()


def _contract(filename: str) -> dict:
    return json.loads((ROOT / "docs/contracts/profiles" / filename).read_text(encoding="utf-8"))


def _assert_identity(contract: dict, profile_id: str, profile_kind: str) -> None:
    assert contract["profile_id"] == profile_id
    assert contract["profile_kind"] == profile_kind
    assert contract["independently_deployable"] is (profile_kind == "primary_profile")
    assert contract["version"] == "1.0.0"
    assert contract["status"] == "active"
    assert contract["language"] == "en"
    assert contract["$schema"] == "../../schemas/deployment-profile.schema.json"
    assert contract["terminology_ref"].startswith("contracts/terminology.contract.json#/terms/TERM-PROFILE-")


def _claim_tests(contract: dict) -> tuple[str, ...]:
    claims = contract["conformance"]["claims"]
    assert claims
    return tuple(claims[0]["test_ids"])

CONTRACT = _contract("sovereign-offline.profile.json")


def test_sovereign_offline_identity_and_composition() -> None:
    _assert_identity(CONTRACT, "sovereign_offline", "profile_overlay")
    assert set(CONTRACT["composition"]["compatible_primary_profiles"]) == {"sovereign_linux_node", "sovereign_hub"}
    assert CONTRACT["composition"]["composition_priority"] == 200
    assert CONTRACT["composition"]["conflict_policy"] == "strongest_restriction_wins"


def test_sovereign_offline_has_no_external_dependency() -> None:
    assert CONTRACT["target_environment"]["network_expectation"] == "disconnected_required"
    assert CONTRACT["offline_behavior"]["continuity_level"] == "core_required"
    assert CONTRACT["offline_behavior"]["internet_dependency"] == "none_for_core"
    assert CONTRACT["ai_boundary"]["approved_external_surfaces"] == []
    assert all(binding["availability"] == "prohibited" for binding in CONTRACT["external_integrations"].values())


def test_sovereign_offline_required_local_components() -> None:
    for component_id in ("identity_and_trust", "governance_policy_runtime", "audit_broker", "resource_governor", "koa_node_agent"):
        assert CONTRACT["components"][component_id]["state"] == "required"
    assert CONTRACT["components"]["sentient"]["state"] == "excluded"
    assert CONTRACT["data_and_storage"]["cross_component_direct_writes_allowed"] is False


def test_sovereign_offline_claim_matrix_is_preserved() -> None:
    claim = CONTRACT["conformance"]["claims"][0]
    assert len(claim["test_ids"]) == 12
    assert len(claim["evidence_ids"]) == 12
    assert CONTRACT["conformance"]["partial_conformance_allowed"] is False
