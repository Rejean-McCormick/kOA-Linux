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

CONTRACT = _contract("high-assurance.profile.json")


def test_high_assurance_identity_and_overlay_only_scope() -> None:
    _assert_identity(CONTRACT, "high_assurance")
    assert CONTRACT["profile_type"] == "profile_overlay"
    composition = CONTRACT["composition"]
    assert composition["requires_exactly_one_primary_profile"] is True
    assert composition["unresolved_composition_allowed"] is False
    assert composition["primary_profile_capabilities_can_be_expanded"] is False
    assert composition["global_invariants_can_be_weakened"] is False


def test_high_assurance_merge_is_restrictive() -> None:
    merge = CONTRACT["composition"]["merge_semantics"]
    assert merge["permissions"] == "intersection"
    assert merge["obligations"] == "union"
    assert merge["network_exposure"] == "most_restrictive"
    assert merge["resource_minimums"] == "maximum"
    assert merge["resource_maximums"] == "minimum"
    assert merge["conflict_outcome"] == "blocked"


def test_high_assurance_claim_requires_complete_evidence() -> None:
    conformance = CONTRACT["conformance"]
    ids = _required_tests(CONTRACT)
    assert ids
    assert len(ids) == len(set(ids))
    assert {test_id.split("-", 2)[1] for test_id in ids} >= {"PROF", "SEC", "LIFE", "OPS", "SYS", "CROSS", "EXIT"}
    assert conformance["activation_requires_outcome"] == "pass"
    assert conformance["missing_required_evidence_outcome"] == "blocked"
    assert conformance["expired_evidence_outcome"] == "blocked"
    assert conformance["failed_control_outcome"] == "fail"


def test_high_assurance_does_not_duplicate_base_test_ids() -> None:
    overlay_ids = set(_required_tests(CONTRACT))
    base_ids = _base_test_ids(CONTRACT["composition"]["compatible_primary_profiles"])
    assert overlay_ids.isdisjoint(base_ids)


def test_high_assurance_wsl_is_explicitly_unsupported() -> None:
    incompatible = {item["profile_id"] for item in CONTRACT["composition"]["incompatible_primary_profiles"]}
    assert incompatible == {"developer_windows_wsl"}


def test_high_assurance_ambiguous_reciprocal_declaration_blocks() -> None:
    base = _contract("user-lightweight.profile.json")
    base_state = {
        item["overlay_id"]: item["compatibility"]
        for item in base["composition"]["overlay_compatibility"]
    }["high_assurance"]
    overlay_accepts = "user_lightweight" in CONTRACT["composition"]["compatible_primary_profiles"]
    if overlay_accepts and base_state == "not_compatible":
        assert CONTRACT["composition"]["merge_semantics"]["conflict_outcome"] == "blocked"
        assert CONTRACT["composition"]["unresolved_composition_allowed"] is False
