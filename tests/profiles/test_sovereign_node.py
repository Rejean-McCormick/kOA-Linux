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

CONTRACT = _contract("sovereign-linux-node.profile.json")


def test_sovereign_node_identity_and_hardware() -> None:
    _assert_identity(CONTRACT, "sovereign_linux_node", "primary_profile")
    assert CONTRACT["hardware_envelope"]["cpu"]["minimum"] == 8
    assert CONTRACT["hardware_envelope"]["memory"]["minimum"] == 32
    assert CONTRACT["hardware_envelope"]["memory"]["recommended"] == 64
    assert CONTRACT["hardware_envelope"]["storage"]["minimum"] == 1000


def test_sovereign_node_immutable_recoverable_lifecycle() -> None:
    assert CONTRACT["capabilities"]["immutable_signed_system_image"]["state"] == "required"
    assert CONTRACT["lifecycle"]["system_update_model"] == "atomic_image"
    assert CONTRACT["lifecycle"]["rollback_required"] is True
    assert CONTRACT["lifecycle"]["forward_repair_allowed"] is True
    assert CONTRACT["lifecycle"]["offline_bundle_support"] == "required"


def test_sovereign_node_security_and_offline_boundaries() -> None:
    assert CONTRACT["security"]["trust_model"] == "sovereign_trust"
    assert CONTRACT["security"]["privilege_model"] == "narrow_privileged_broker"
    assert CONTRACT["security"]["network_default"] == "closed_by_default"
    assert CONTRACT["offline_behavior"]["continuity_level"] == "core_required"
    assert CONTRACT["offline_behavior"]["recovery_without_internet"] is True
    assert set(CONTRACT["ai_boundary"]["approved_external_surfaces"]) == {"chatgpt", "suno", "gamma", "ariane-voice"}


def test_sovereign_node_overlay_compatibility_and_tests() -> None:
    assert set(CONTRACT["composition"]["optional_overlays"]) == {"high_assurance", "sovereign_offline", "appliance_shell"}
    ids = _claim_tests(CONTRACT)
    assert len(ids) == 16
    assert all(item.startswith("TEST-PROFILE-SOV-") for item in ids)
