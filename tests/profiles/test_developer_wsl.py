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

CONTRACT = _contract("developer-windows-wsl.profile.json")


def test_developer_wsl_identity_and_non_claims() -> None:
    _assert_identity(CONTRACT, "developer_windows_wsl")
    assert CONTRACT["profile_type"] == "primary_profile"
    conformance = CONTRACT["conformance"]
    assert conformance["claim_type"] == "development_profile"
    assert conformance["qualifier"] == "development_convenience_profile"
    for unsupported in (
        "production_conformant",
        "sovereign_linux_conformant",
        "sovereign_offline_conformant",
        "high_assurance_conformant",
        "build_farm_conformant",
        "control_plane_conformant",
        "release_signing_conformant",
    ):
        assert conformance[unsupported] is False


def test_developer_wsl_workspace_boundary() -> None:
    workspace = CONTRACT["workspace_model"]
    assert workspace["workspace_root_policy"] == "inside_wsl_linux_filesystem"
    assert workspace["mutable_runtime_state_on_windows_mount_allowed"] is False
    assert workspace["shared_mutable_dependency_environment_allowed"] is False
    assert workspace["workspace_cleanup_must_not_delete_other_workspaces"] is True


def test_developer_wsl_container_boundary() -> None:
    containers = CONTRACT["container_model"]
    assert containers["privileged_containers_allowed"] is False
    assert containers["host_network_mode_allowed"] is False
    assert containers["mixed_backends_in_one_workspace_allowed"] is False
    assert containers["image_tags_without_digest_or_immutable_version_allowed"] is False
    assert containers["production_orchestration_conformance_claimed"] is False


def test_developer_wsl_claim_requires_current_evidence() -> None:
    conformance = CONTRACT["conformance"]
    assert conformance["deployable"] is True
    assert conformance["claim_requires_current_tests_and_evidence"] is True
    assert conformance["claim_requires_profile_id_in_receipts"] is True
    assert conformance["offline_development_claim"] == "qualified"
