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

CONTRACT = _contract("appliance-shell.profile.json")


def test_appliance_shell_identity_and_overlay_scope() -> None:
    _assert_identity(CONTRACT, "appliance_shell")
    assert CONTRACT["profile_type"] == "overlay"
    composition = CONTRACT["composition"]
    assert composition["composable"] is True
    assert set(composition["compatible_base_profiles"]) == {"user_lightweight", "sovereign_linux_node"}
    assert set(composition["incompatible_base_profiles"]) == {
        "developer_linux_workstation",
        "developer_windows_wsl",
        "sovereign_hub",
        "build_farm",
        "control_plane",
    }


def test_appliance_shell_cannot_broaden_authority() -> None:
    inheritance = CONTRACT["composition"]["inheritance"]
    assert inheritance["overlay_can_broaden_authority"] is False
    assert inheritance["overlay_can_broaden_data_ownership"] is False
    assert inheritance["overlay_can_broaden_external_integrations"] is False
    assert all(item["result"] == "composition_rejected" for item in CONTRACT["composition"]["conflicts"])


def test_appliance_shell_claims_are_overlay_specific() -> None:
    ids = _required_tests(CONTRACT)
    _assert_test_ids(ids, prefix="TEST-PROFILE-APP-", count=15)
    base_ids = _base_test_ids(CONTRACT["composition"]["compatible_base_profiles"])
    assert set(ids).isdisjoint(base_ids)
    conformance = CONTRACT["conformance"]
    assert conformance["claim_type"] == "profile_overlay"
    assert "missing_required_test_or_evidence" in conformance["claim_blocking_conditions"]


def test_appliance_shell_ordinary_session_is_restricted() -> None:
    ordinary = CONTRACT["security"]["ordinary_session"]
    assert ordinary["direct_host_mutation"] is False
    assert ordinary["privileged_processes_exposed_to_session"] is False
    assert ordinary["unrestricted_device_access"] is False
    assert ordinary["unrestricted_local_socket_access"] is False
    prohibited = set(CONTRACT["capabilities"]["prohibited"])
    assert {"unrestricted_terminal_access", "ordinary_session_package_installation"} <= prohibited


def test_appliance_shell_offline_navigation_remains_local() -> None:
    offline = CONTRACT["offline_behavior"]
    assert offline["local_shell_available"] is True
    assert offline["ariane_local_navigation_available"] is True
    assert offline["external_ai_available"] is False
    assert offline["false_success_reporting"] is False
