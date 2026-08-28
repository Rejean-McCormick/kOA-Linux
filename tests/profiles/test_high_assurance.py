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

CONTRACT = _contract("high-assurance.profile.json")


def test_high_assurance_identity_and_composition() -> None:
    _assert_identity(CONTRACT, "high_assurance", "profile_overlay")
    assert set(CONTRACT["composition"]["compatible_primary_profiles"]) == {"user_lightweight", "developer_linux_workstation", "sovereign_linux_node", "sovereign_hub", "build_farm", "control_plane"}
    assert CONTRACT["composition"]["composition_priority"] == 100
    assert CONTRACT["composition"]["conflict_policy"] == "strongest_restriction_wins"
    assert "developer_windows_wsl" in CONTRACT["composition"]["incompatible_profiles"]


def test_high_assurance_required_controls() -> None:
    for capability_id in ("hardware_rooted_trust", "measured_boot", "strong_identity_and_authentication", "tamper_evident_audit", "separation_of_duties"):
        assert CONTRACT["capabilities"][capability_id]["state"] == "required"
    assert CONTRACT["security"]["trust_model"] == "high_assurance_trust"
    assert "hardware_root_of_trust" in CONTRACT["security"]["required_controls"]


def test_high_assurance_component_additions() -> None:
    for component_id in ("identity_and_trust", "governance_policy_runtime", "audit_broker", "koa_node_agent", "resource_governor"):
        assert CONTRACT["components"][component_id]["state"] == "required"
    assert CONTRACT["components"]["publication_gateway"]["state"] == "conditional"


def test_high_assurance_claims_remain_explicit() -> None:
    ids = _claim_tests(CONTRACT)
    assert ids
    assert len(ids) == len(set(ids))
    assert CONTRACT["conformance"]["partial_conformance_allowed"] is False
