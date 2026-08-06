"""Conformance checks for canonical profile contracts and the minimal plan fixture."""

from __future__ import annotations

import re
from pathlib import Path

EXPECTED_PROFILES = {
    "appliance-shell.profile.json": "appliance_shell",
    "build-farm.profile.json": "build_farm",
    "control-plane.profile.json": "control_plane",
    "developer-linux-workstation.profile.json": "developer_linux_workstation",
    "developer-windows-wsl.profile.json": "developer_windows_wsl",
    "high-assurance.profile.json": "high_assurance",
    "sovereign-hub.profile.json": "sovereign_hub",
    "sovereign-linux-node.profile.json": "sovereign_linux_node",
    "sovereign-offline.profile.json": "sovereign_offline",
    "user-lightweight.profile.json": "user_lightweight",
}
SEMVER = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")


def test_profile_contract_inventory_is_exact(contracts_root: Path) -> None:
    profile_root = contracts_root / "profiles"
    assert {path.name for path in profile_root.glob("*.profile.json")} == set(EXPECTED_PROFILES)


def test_profile_contract_common_identity(contracts_root: Path, load_json) -> None:
    ids: set[str] = set()
    for filename, expected_id in EXPECTED_PROFILES.items():
        contract = load_json(contracts_root / "profiles" / filename)
        assert contract["profile_id"] == expected_id
        assert contract["profile_id"] not in ids
        ids.add(contract["profile_id"])
        assert contract["status"] == "active"
        assert contract["language"] == "en"
        assert SEMVER.fullmatch(contract["version"])


def test_minimal_profile_plan_resolves_exact_contract_sources(
    repository_root: Path, fixtures_root: Path, load_json
) -> None:
    plan = load_json(fixtures_root / "minimal-profile-plan.json")
    entries = plan["profile_contracts"]
    assert plan["generator"]["deterministic"] is True
    assert plan["capability_resolution"] == {
        "missing_capability_result": "unavailable",
        "silent_substitution": False,
    }
    assert {entry["profile_id"] for entry in entries} == set(EXPECTED_PROFILES.values())
    assert len(entries) == len(EXPECTED_PROFILES)
    for entry in entries:
        source = repository_root / entry["source"]
        contract = load_json(source)
        assert contract["profile_id"] == entry["profile_id"]


def test_minimal_profile_plan_has_no_implicit_overlay(fixtures_root: Path, load_json) -> None:
    plan = load_json(fixtures_root / "minimal-profile-plan.json")
    assert plan["selected_profile_id"] == "user_lightweight"
    assert plan["overlay_profile_ids"] == []
