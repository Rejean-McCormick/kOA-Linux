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

CONTRACT = _contract("developer-windows-wsl.profile.json")


def test_developer_wsl_identity_and_environment() -> None:
    _assert_identity(CONTRACT, "developer_windows_wsl", "primary_profile")
    assert CONTRACT["target_environment"]["host_os_families"] == ["windows", "wsl2"]
    assert CONTRACT["target_environment"]["virtualization"] == "required"
    assert CONTRACT["hardware_envelope"]["cpu"]["minimum"] == 4
    assert CONTRACT["hardware_envelope"]["memory"]["minimum"] == 16


def test_developer_wsl_capability_boundaries() -> None:
    assert CONTRACT["capabilities"]["workspace_isolation"]["state"] == "required"
    assert CONTRACT["capabilities"]["production_release_signing"]["state"] == "excluded"
    assert CONTRACT["capabilities"]["native_ai_processing"]["state"] == "excluded"
    assert CONTRACT["security"]["secrets_management"] == "workspace_scoped_secrets"


def test_developer_wsl_components_are_selective() -> None:
    for component_id in ("koa_node_agent", "identity_and_trust", "resource_governor", "audit_broker"):
        assert CONTRACT["components"][component_id]["state"] == "required"
    assert CONTRACT["components"]["sentient"]["state"] == "optional"
    assert set(CONTRACT["ai_boundary"]["approved_external_surfaces"]) == {"chatgpt", "suno", "gamma", "ariane-voice"}


def test_developer_wsl_overlay_compatibility_is_closed() -> None:
    assert CONTRACT["composition"]["optional_overlays"] == []
    assert set(CONTRACT["composition"]["incompatible_profiles"]) == {"high_assurance", "sovereign_offline", "appliance_shell"}
