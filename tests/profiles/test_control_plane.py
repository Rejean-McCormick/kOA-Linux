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

CONTRACT = _contract("control-plane.profile.json")


def test_control_plane_identity_and_composition() -> None:
    _assert_identity(CONTRACT, "control_plane", "primary_profile")
    assert CONTRACT["composition"]["optional_overlays"] == ["high_assurance"]
    assert set(CONTRACT["composition"]["incompatible_profiles"]) == {"sovereign_offline", "appliance_shell"}


def test_control_plane_capability_and_authority_boundaries() -> None:
    assert CONTRACT["capabilities"]["deployment_coordination"]["state"] == "required"
    assert CONTRACT["capabilities"]["release_coordination"]["state"] == "required"
    assert CONTRACT["capabilities"]["direct_write_to_managed_component_authoritative_tables"]["state"] == "excluded"
    assert CONTRACT["data_and_storage"]["cross_component_direct_writes_allowed"] is False


def test_control_plane_components_and_security() -> None:
    for component_id in ("resource_governor", "governance_policy_runtime", "identity_and_trust", "audit_broker", "koa_node_agent"):
        assert CONTRACT["components"][component_id]["state"] == "required"
    assert CONTRACT["components"]["sentient"]["state"] == "excluded"
    assert CONTRACT["security"]["trust_model"] == "service_trust"
    assert CONTRACT["target_environment"]["network_expectation"] == "controlled_network_required"


def test_control_plane_claim_tests_are_preserved() -> None:
    ids = _claim_tests(CONTRACT)
    assert len(ids) == 12
    assert all(item.startswith("TEST-PROFILE-CP-") for item in ids)
