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

CONTRACT = _contract("control-plane.profile.json")


def test_control_plane_identity_and_claim_matrix() -> None:
    _assert_identity(CONTRACT, "control_plane")
    assert CONTRACT["profile_type"] == "primary_deployment_profile"
    ids = _required_tests(CONTRACT)
    _assert_test_ids(ids, prefix="TEST-PROFILE-CP-", count=12)
    expectations = CONTRACT["conformance"]["test_expectations"]
    assert set(expectations) == set(ids)
    assert CONTRACT["conformance"]["unsupported_claim_result"] == "blocked"


def test_control_plane_composition_is_closed() -> None:
    composition = CONTRACT["composition"]
    assert composition["primary_profile"] is True
    assert composition["maximum_primary_profiles"] == 1
    assert composition["implicit_inheritance_allowed"] is False
    assert composition["incompatible_composition_result"] == "activation_blocked"
    assert composition["compatible_overlay_ids"] == ["high_assurance"]
    assert set(composition["incompatible_overlay_ids"]) == {"sovereign_offline", "appliance_shell"}


def test_control_plane_does_not_absorb_managed_node_authority() -> None:
    authority = CONTRACT["authority_model"]
    serialized = json.dumps(authority, sort_keys=True)
    assert "managed" in serialized
    assert "local" in serialized
    assert "authority" in serialized
    assert "mutate_tenant_or_component_source_data" in authority["prohibited_authority"]
    assert "component_authoritative_source_tables" in (
        CONTRACT["data_boundaries"]["profile_coordination_state"]["prohibited_data_classes"]
    )
    assert CONTRACT["data_boundaries"]["observation_or_caching_transfers_ownership"] is False


def test_control_plane_loss_preserves_local_correctness() -> None:
    connectivity = CONTRACT["connectivity"]
    serialized = json.dumps(connectivity, sort_keys=True)
    assert "local" in serialized
    loss = connectivity["loss_of_control_plane_connectivity"]
    assert loss["local_console"] == "operational"
    assert loss["new_remote_activation"] == "blocked"
    assert loss["silent_failover"] is False
