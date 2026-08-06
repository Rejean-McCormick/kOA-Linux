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

CONTRACT = _contract("user-lightweight.profile.json")


def test_user_lightweight_identity_and_claim_matrix() -> None:
    _assert_identity(CONTRACT, "user_lightweight")
    assert CONTRACT["profile_type"] == "primary"
    conformance = CONTRACT["conformance"]
    ids = _required_tests(CONTRACT)
    _assert_test_ids(ids, prefix="TEST-PROFILE-USER-", count=12)
    assert {item["test_id"] for item in conformance["test_intents"]} == set(ids)
    assert conformance["claim_requires_all_required_tests"] == "pass"
    assert conformance["missing_required_test_result"] == "blocked"
    assert conformance["missing_required_evidence_result"] == "fail"


def test_user_lightweight_overlay_claims_are_explicit() -> None:
    compatibility = {
        item["overlay_id"]: item["compatibility"]
        for item in CONTRACT["composition"]["overlay_compatibility"]
    }
    assert compatibility == {
        "appliance_shell": "compatible",
        "sovereign_offline": "compatible_with_constraints",
        "high_assurance": "not_compatible",
    }
    assert CONTRACT["composition"]["default_overlays"] == []


def test_user_lightweight_resource_and_offline_claims() -> None:
    assert CONTRACT["hardware_envelope"]["cpu"]["heavy_job_concurrency"] == 1
    assert CONTRACT["resource_governance"]["resource_governor_required"] is True
    assert CONTRACT["ai_boundary"]["native_ai_runtime_present"] is False
    assert CONTRACT["offline_capability_envelope"]["claim"] == "core_local_operation"
    assert CONTRACT["offline_capability_envelope"]["validation_required"] is True
    assert CONTRACT["network_and_integrations"]["external_egress"]["provider_substitution_permitted"] is False


def test_user_lightweight_component_boundaries() -> None:
    required = {item["component_id"] for item in CONTRACT["component_membership"]["required"]}
    excluded = {item["component_id"] for item in CONTRACT["component_membership"]["excluded"]}
    assert {"identity-and-trust", "resource-governor", "koa_mediatheque", "koa-node-agent"} <= required
    assert {"sentient", "gf-wordbench"} <= excluded
    assert CONTRACT["security_and_privacy"]["direct_host_privilege_permitted"] is False
