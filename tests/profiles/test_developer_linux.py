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

CONTRACT = _contract("developer-linux-workstation.profile.json")


def test_developer_linux_identity_and_environment() -> None:
    _assert_identity(CONTRACT, "developer_linux_workstation", "primary_profile")
    assert CONTRACT["target_environment"]["host_os_families"] == ["linux"]
    assert CONTRACT["hardware_envelope"]["cpu"]["minimum"] == 8
    assert CONTRACT["hardware_envelope"]["memory"]["minimum"] == 32
    assert CONTRACT["hardware_envelope"]["storage"]["minimum"] == 1000


def test_developer_linux_workspace_isolation_and_authority() -> None:
    assert CONTRACT["capabilities"]["workspace_isolation"]["state"] == "required"
    assert CONTRACT["capabilities"]["production_activation"]["state"] == "excluded"
    assert CONTRACT["security"]["secrets_management"] == "workspace_scoped_secrets"
    assert CONTRACT["data_and_storage"]["cross_component_direct_writes_allowed"] is False


def test_developer_linux_workbenches_are_optional() -> None:
    assert CONTRACT["components"]["resource_governor"]["state"] == "required"
    for component_id in ("kristal_runtime", "orgo", "konnaxion", "semantik_architect_runtime", "sentient", "ariane_runtime"):
        assert CONTRACT["components"][component_id]["state"] == "optional"
    assert set(CONTRACT["ai_boundary"]["approved_external_surfaces"]) == {"chatgpt", "suno", "gamma", "ariane-voice"}


def test_developer_linux_claim_tests_are_preserved() -> None:
    ids = _claim_tests(CONTRACT)
    assert len(ids) == 13
    assert ids[0] == "TEST-PROFILE-DEV-LINUX-001"
    assert all(item.startswith("TEST-DEV-") for item in ids[1:])
