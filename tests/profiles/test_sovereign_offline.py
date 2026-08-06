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

CONTRACT = _contract("sovereign-offline.profile.json")


def test_sovereign_offline_identity_and_overlay_scope() -> None:
    _assert_identity(CONTRACT, "sovereign_offline")
    assert CONTRACT["profile_type"] == "deployment_profile_overlay"
    composition = CONTRACT["composition"]
    assert composition["overlay"] is True
    assert composition["inheritance_is_explicit"] is True
    assert set(composition["allowed_base_profiles"]) == {"sovereign_linux_node", "sovereign_hub"}
    assert composition["conflict_policy"]["unresolved_conflict_result"] == "blocked"


def test_sovereign_offline_matrix_covers_every_overlay_test_once() -> None:
    conformance = CONTRACT["conformance"]
    ids = _required_tests(CONTRACT)
    _assert_test_ids(ids, prefix="TEST-PROFILE-SOV-OFF-", count=12)
    matrix_ids = [item["test_id"] for item in conformance["validation_matrix"]]
    assert tuple(matrix_ids) == ids
    assert all(item["expected_result"] == "pass" for item in conformance["validation_matrix"])
    assert conformance["partial_conformance_claim_allowed"] is False


def test_sovereign_offline_activation_gate_is_fail_closed() -> None:
    gate = CONTRACT["conformance"]["activation_gate"]
    assert gate["activation_result_on_failure"] == "blocked"
    assert all(value is True for key, value in gate.items() if key.endswith("_required"))
    assert CONTRACT["external_integrations"]["runtime_external_calls_allowed"] is False
    assert CONTRACT["external_integrations"]["automatic_external_substitution_allowed"] is False


def test_sovereign_offline_does_not_duplicate_base_test_ids() -> None:
    overlay_ids = set(_required_tests(CONTRACT))
    base_ids = _base_test_ids(CONTRACT["composition"]["allowed_base_profiles"])
    assert overlay_ids.isdisjoint(base_ids)


def test_sovereign_offline_degradation_preserves_authority_boundaries() -> None:
    degradation = CONTRACT["degradation"]
    assert degradation["silent_fallback_allowed"] is False
    assert degradation["external_substitution_allowed"] is False
    assert degradation["partial_authority_allowed"] is False


def test_sovereign_offline_ambiguous_reciprocal_declaration_blocks() -> None:
    base = _contract("user-lightweight.profile.json")
    base_state = {
        item["overlay_id"]: item["compatibility"]
        for item in base["composition"]["overlay_compatibility"]
    }["sovereign_offline"]
    overlay_prohibits = "user_lightweight" in CONTRACT["composition"]["prohibited_base_profiles"]
    if overlay_prohibits and base_state == "compatible_with_constraints":
        conflict = CONTRACT["composition"]["conflict_policy"]
        assert conflict["unresolved_conflict_result"] == "blocked"
        assert conflict["strategy"] == "deny_ambiguous_composition"
