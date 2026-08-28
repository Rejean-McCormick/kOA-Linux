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

CONTRACT = _contract("user-lightweight.profile.json")


def test_user_lightweight_identity_and_hardware() -> None:
    _assert_identity(CONTRACT, "user_lightweight", "primary_profile")
    assert CONTRACT["hardware_envelope"]["cpu"]["minimum"] == 4
    assert CONTRACT["hardware_envelope"]["cpu"]["recommended"] == 6
    assert CONTRACT["hardware_envelope"]["memory"]["minimum"] == 16
    assert CONTRACT["hardware_envelope"]["memory"]["recommended"] == 32
    assert CONTRACT["hardware_envelope"]["concurrency"]["heavy_jobs"] == 1


def test_user_lightweight_local_and_offline_capabilities() -> None:
    assert CONTRACT["capabilities"]["interactive_user"]["state"] == "required"
    assert CONTRACT["capabilities"]["ariane_local_navigation"]["state"] == "required"
    assert CONTRACT["capabilities"]["offline_continuity"]["state"] == "required"
    assert CONTRACT["offline_behavior"]["continuity_level"] == "core_required"
    assert CONTRACT["offline_behavior"]["recovery_without_internet"] is True
    assert set(CONTRACT["ai_boundary"]["approved_external_surfaces"]) == {"chatgpt", "suno", "gamma", "ariane-voice"}


def test_user_lightweight_component_boundaries() -> None:
    for component_id in ("identity_and_trust", "resource_governor", "koa_mediatheque", "koa_node_agent", "ariane", "konnaxion", "orgo", "semantik_architect"):
        assert CONTRACT["components"][component_id]["state"] == "required"
    assert CONTRACT["components"]["gf_wordbench"]["state"] == "excluded"
    assert CONTRACT["components"]["sentient"]["state"] == "excluded"
    assert CONTRACT["security"]["privilege_model"] == "least_privilege"


def test_user_lightweight_composition_and_claim_tests() -> None:
    assert set(CONTRACT["composition"]["optional_overlays"]) == {"appliance_shell", "high_assurance"}
    assert "sovereign_offline" in CONTRACT["composition"]["incompatible_profiles"]
    ids = _claim_tests(CONTRACT)
    assert len(ids) == 12
    assert all(item.startswith("TEST-PROFILE-USER-") for item in ids)
