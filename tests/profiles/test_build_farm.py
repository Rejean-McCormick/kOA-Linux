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

CONTRACT = _contract("build-farm.profile.json")


def test_build_farm_identity_and_unasserted_claim() -> None:
    _assert_identity(CONTRACT, "build_farm")
    assert CONTRACT["independently_deployable"] is True
    conformance = CONTRACT["conformance"]
    assert conformance["claim_level"] == "profile"
    assert conformance["claims"] == []
    assert conformance["evidence_required"] is True
    assert conformance["partial_conformance_allowed"] is False


def test_build_farm_composition_is_fail_closed() -> None:
    composition = CONTRACT["composition"]
    assert composition["conflict_policy"] == "fail_closed"
    assert composition["required_overlays"] == []
    assert set(composition["optional_overlays"]) == {"high_assurance", "sovereign_offline"}
    assert "appliance_shell" in composition["incompatible_profiles"]
    assert CONTRACT["inheritance"]["override_policy"] == "strengthen_or_restrict_only"


def test_build_farm_required_pipeline_capabilities() -> None:
    capabilities = CONTRACT["capabilities"]
    for capability_id in (
        "isolated_parallel_build_workers",
        "automated_test_execution",
        "artifact_cache",
        "artifact_export_and_transfer",
    ):
        assert capabilities[capability_id]["state"] == "required"
    assert capabilities["external_ai_assistance"]["state"] == "excluded"


def test_build_farm_signing_does_not_follow_build_success() -> None:
    signing = CONTRACT["capabilities"]["artifact_signing"]
    assert signing["state"] == "conditional"
    assert any("does not automatically authorize signing" in condition for condition in signing["conditions"])
