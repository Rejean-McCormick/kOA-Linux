from __future__ import annotations

import json
from pathlib import Path

import pytest


def _root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "docs/contracts/profiles").is_dir():
            return candidate
    raise RuntimeError("repository root with docs/contracts/profiles was not found")


ROOT = _root()


def _contract(filename: str) -> dict:
    path = ROOT / "docs/contracts/profiles" / filename
    return json.loads(path.read_text(encoding="utf-8"))


def _required_tests(contract: dict) -> tuple[str, ...]:
    conformance = contract["conformance"]
    for key in ("required_tests", "required_test_ids", "test_ids"):
        value = conformance.get(key)
        if value is not None:
            assert isinstance(value, list)
            return tuple(value)
    return ()


def _assert_identity(contract: dict, profile_id: str) -> None:
    assert contract["profile_id"] == profile_id
    assert contract["version"] == "1.0.0"
    assert contract["status"] == "active"
    assert contract["language"] == "en"
    schema_ref = contract["$schema"]
    assert schema_ref == "../../schemas/deployment-profile.schema.json"
    assert (ROOT / "docs/schemas/deployment-profile.schema.json").is_file()


def _assert_test_ids(ids: tuple[str, ...], *, prefix: str, count: int | None = None) -> None:
    assert ids, "a claimable profile must declare its tests explicitly"
    assert len(ids) == len(set(ids)), "test identifiers must be unique"
    assert all(test_id.startswith(prefix) for test_id in ids)
    if count is not None:
        assert len(ids) == count


def _base_test_ids(profile_ids: list[str]) -> set[str]:
    filenames = {
        "user_lightweight": "user-lightweight.profile.json",
        "developer_linux_workstation": "developer-linux-workstation.profile.json",
        "developer_windows_wsl": "developer-windows-wsl.profile.json",
        "sovereign_linux_node": "sovereign-linux-node.profile.json",
        "sovereign_hub": "sovereign-hub.profile.json",
        "build_farm": "build-farm.profile.json",
        "control_plane": "control-plane.profile.json",
    }
    result: set[str] = set()
    for profile_id in profile_ids:
        result.update(_required_tests(_contract(filenames[profile_id])))
    return result

CONTRACT = _contract("sovereign-linux-node.profile.json")


def test_sovereign_node_identity_and_claim_matrix() -> None:
    _assert_identity(CONTRACT, "sovereign_linux_node")
    assert CONTRACT["profile_type"] == "primary"
    ids = _required_tests(CONTRACT)
    _assert_test_ids(ids, prefix="TEST-PROFILE-SOV-", count=16)
    assert {item["test_id"] for item in CONTRACT["conformance"]["test_intents"]} == set(ids)
    assert CONTRACT["conformance"]["missing_required_test_result"] == "blocked"
    assert CONTRACT["conformance"]["overlay_claims_are_separate"] is True


def test_sovereign_node_release_and_privilege_claims() -> None:
    lifecycle = CONTRACT["release_and_lifecycle"]
    assert lifecycle["partial_activation_permitted"] is False
    assert lifecycle["artifact_validation_before_activation"] is True
    assert lifecycle["rollback_or_forward_repair_required"] is True
    security = CONTRACT["security_and_privacy"]
    assert security["least_privilege_required"] is True
    assert "narrow privileged broker" in security["security_baseline"]
    assert security["default_deny_network_required"] is True


def test_sovereign_node_offline_claim_is_local() -> None:
    offline = CONTRACT["offline_capability_envelope"]
    assert offline["claim"] == "sovereign_local_operation"
    assert offline["validation_required"] is True
    network = CONTRACT["network_and_integrations"]
    assert network["inbound"]["public_inbound_service_permitted_by_default"] is False
    assert network["inbound"]["default"] == "deny"
    assert network["outbound"]["default"] == "deny"
    assert "do not select an undeclared provider" in network["remote_dependency_failure"]


def test_sovereign_node_overlay_compatibility_is_explicit() -> None:
    entries = {
        item["overlay_id"]: item["compatibility"]
        for item in CONTRACT["composition"]["overlay_compatibility"]
    }
    assert entries["high_assurance"] == "compatible"
    assert entries["sovereign_offline"] == "compatible"
    assert entries["appliance_shell"] == "compatible"
