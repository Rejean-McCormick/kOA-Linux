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

CONTRACT = _contract("sovereign-hub.profile.json")


def test_sovereign_hub_identity_and_composition() -> None:
    _assert_identity(CONTRACT, "sovereign_hub", "primary_profile")
    assert set(CONTRACT["composition"]["optional_overlays"]) == {"high_assurance", "sovereign_offline"}
    assert "appliance_shell" in CONTRACT["composition"]["incompatible_profiles"]


def test_sovereign_hub_authority_and_storage() -> None:
    assert CONTRACT["capabilities"]["multi_tenant_service_hosting"]["state"] == "required"
    assert CONTRACT["capabilities"]["local_governance"]["state"] == "required"
    assert CONTRACT["data_and_storage"]["component_data_ownership_required"] is True
    assert CONTRACT["data_and_storage"]["cross_component_direct_writes_allowed"] is False
    assert CONTRACT["security"]["trust_model"] == "sovereign_trust"


def test_sovereign_hub_required_components() -> None:
    for component_id in ("koa_node_agent", "identity_and_trust", "governance_policy_runtime", "audit_broker", "resource_governor", "konnaxion", "orgo", "publication_gateway"):
        assert CONTRACT["components"][component_id]["state"] == "required"
    assert CONTRACT["components"]["sentient"]["state"] == "optional"


def test_sovereign_hub_claim_tests_are_preserved() -> None:
    ids = _claim_tests(CONTRACT)
    assert len(ids) == 16
    assert ids[0] == "TEST-PROFILE-HUB-001"
    assert all(item.startswith("TEST-HUB-") for item in ids[1:])
