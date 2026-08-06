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

CONTRACT = _contract("sovereign-hub.profile.json")


def test_sovereign_hub_identity_and_claim_state() -> None:
    _assert_identity(CONTRACT, "sovereign_hub")
    assert CONTRACT["classification"]["kind"] == "primary_profile"
    assert CONTRACT["classification"]["production_profile"] is True
    assert CONTRACT["classification"]["sovereign_conformance_profile"] is True
    ids = _required_tests(CONTRACT)
    assert ids
    assert len(ids) == len(set(ids))
    assert CONTRACT["conformance"]["current_claim"] == "not_asserted"
    assert CONTRACT["conformance"]["missing_evidence_result"] == "blocked"


def test_sovereign_hub_topology_does_not_merge_authority() -> None:
    authority = CONTRACT["authority"]
    assert "tenant_data" in authority["does_not_own"]
    assert "component_responsibility" in authority["does_not_own"]
    data = CONTRACT["data_authority"]
    assert data["logical_ownership_required"] is True
    assert data["direct_cross_component_authoritative_writes_allowed"] is False
    assert data["caches_and_reproducible_derivatives_are_authoritative"] is False


def test_sovereign_hub_failure_is_scoped() -> None:
    failure = CONTRACT["failure_behavior"]
    assert failure["single_component_failure"] == "preserve_unrelated_component_capabilities"
    assert failure["external_ai_unavailable"] == "disable_external_assistance_only"
    assert failure["database_unavailable"] == "degrade_affected_component_without_cross_component_failover_writes"
    assert CONTRACT["ai_boundary"]["external_output_direct_authoritative_mutation_allowed"] is False


def test_sovereign_hub_is_not_node_conformance_by_implication() -> None:
    assert CONTRACT["classification"]["sovereign_linux_node_conformance_implied"] is False
    assert CONTRACT["classification"]["deployment_form"] == ["single_node", "small_cluster"]
