from __future__ import annotations

import json
from pathlib import Path


def _root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "docs/contracts/profiles").is_dir():
            return candidate
    raise RuntimeError("repository root with docs/contracts/profiles was not found")


ROOT = _root()


def _contract(filename: str) -> dict:
    return json.loads((ROOT / "docs/contracts/profiles" / filename).read_text(encoding="utf-8"))


def _assert_identity(contract: dict, profile_id: str, profile_kind: str) -> None:
    assert contract["profile_id"] == profile_id
    assert contract["profile_kind"] == profile_kind
    assert contract["independently_deployable"] is (profile_kind == "primary_profile")
    assert contract["version"] == "1.0.0"
    assert contract["status"] == "active"
    assert contract["language"] == "en"
    assert contract["$schema"] == "../../schemas/deployment-profile.schema.json"
    assert contract["terminology_ref"].startswith("contracts/terminology.contract.json#/terms/TERM-PROFILE-")


def _claim_tests(contract: dict) -> tuple[str, ...]:
    claims = contract["conformance"]["claims"]
    assert claims
    return tuple(claims[0]["test_ids"])

CONTRACT = _contract("appliance-shell.profile.json")


def test_appliance_shell_identity_and_composition() -> None:
    _assert_identity(CONTRACT, "appliance_shell", "profile_overlay")
    composition = CONTRACT["composition"]
    assert set(composition["compatible_primary_profiles"]) == {"user_lightweight", "sovereign_linux_node"}
    assert composition["composition_priority"] == 300
    assert composition["conflict_policy"] == "fail_closed"


def test_appliance_shell_capability_and_component_boundaries() -> None:
    assert CONTRACT["capabilities"]["ariane_local_navigation"]["state"] == "required"
    assert CONTRACT["capabilities"]["unrestricted_terminal_access"]["state"] == "excluded"
    assert CONTRACT["components"]["ariane_runtime"]["state"] == "required"
    assert CONTRACT["components"]["resource_governor"]["state"] == "required"
    assert CONTRACT["components"]["sentient"]["state"] == "excluded"


def test_appliance_shell_offline_and_security() -> None:
    assert CONTRACT["offline_behavior"]["recovery_without_internet"] is True
    assert "external_ai" in CONTRACT["offline_behavior"]["unavailable_capabilities"]
    assert CONTRACT["security"]["privilege_model"] == "least_privilege"
    assert CONTRACT["security"]["network_default"] == "local_only"


def test_appliance_shell_claim_tests_are_preserved() -> None:
    ids = _claim_tests(CONTRACT)
    assert len(ids) == 15
    assert all(item.startswith("TEST-PROFILE-APP-") for item in ids)
