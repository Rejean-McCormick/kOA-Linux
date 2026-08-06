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

CONTRACT = _contract("developer-linux-workstation.profile.json")


def test_developer_linux_identity_and_claims() -> None:
    _assert_identity(CONTRACT, "developer_linux_workstation")
    assert CONTRACT["classification"]["kind"] == "primary_profile"
    assert CONTRACT["classification"]["production_profile"] is False
    ids = _required_tests(CONTRACT)
    assert len(ids) == 13
    assert len(ids) == len(set(ids))
    assert "TEST-PROFILE-DEV-LINUX-001" in ids
    assert CONTRACT["conformance"]["current_claim"] == "not_asserted"
    assert CONTRACT["conformance"]["missing_evidence_result"] == "blocked"


def test_developer_linux_workspace_isolation_claims() -> None:
    isolation = CONTRACT["workspace_isolation"]
    assert isolation["mutable_dependency_environment"]["one_per_workspace"] is True
    assert isolation["mutable_dependency_environment"]["shared_between_workspaces"] is False
    assert isolation["port_allocation"]["host_port_collisions_allowed"] is False
    assert isolation["secret_namespace"]["cross_workspace_reuse_allowed"] is False
    assert isolation["secret_namespace"]["repository_storage_allowed"] is False
    assert CONTRACT["inheritance"]["implicit_inheritance_allowed"] is False


def test_developer_linux_optional_workbenches_are_not_baseline_authority() -> None:
    selection = CONTRACT["component_selection"]
    assert selection["activate_all_workbenches_required"] is False
    workbenches = {item["workbench_id"]: item for item in selection["selectable_component_workbenches"]}
    assert workbenches["sentient_development"]["non_authoritative"] is True
    assert workbenches["sentient_development"]["task_activated"] is True
    assert all(item["default_activation"] == "stopped" for item in workbenches.values())


def test_developer_linux_offline_and_ai_failure_are_scoped() -> None:
    assert CONTRACT["offline_behavior"]["missing_remote_dependency_behavior"] == "fail_closed_for_affected_operation"
    assert CONTRACT["offline_behavior"]["unrelated_local_capabilities_continue"] is True
    assert CONTRACT["ai_boundary"]["native_ai_in_profile_baseline"] is False
    assert CONTRACT["ai_boundary"]["external_output_direct_authoritative_mutation_allowed"] is False
    assert CONTRACT["container_policy"]["privileged_containers_allowed_by_default"] is False
