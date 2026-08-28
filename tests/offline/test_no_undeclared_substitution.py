"""Ensure network loss cannot select an undeclared provider or authority."""

from __future__ import annotations

from pathlib import Path
import json
import sys

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "assembly" / "src"))

from koa_assembly.renderers import render  # noqa: E402

_SHA = "sha256:" + "a" * 64


def _load(path: str) -> dict:
    return json.loads((REPO / path).read_text(encoding="utf-8"))


def _plan() -> dict:
    return {
        "plan_id": "no-substitution-test",
        "profile_id": "sovereign-offline",
        "source_digests": {"docs/contracts/system.contract.json": _SHA},
        "services": [
            {
                "id": "local-core",
                "kind": "native",
                "command": ["/usr/bin/koa-local-core"],
                "dependencies": [],
                "environment": {},
                "ports": [],
                "mounts": [],
                "networks": [],
                "resources": {},
                "capabilities": [],
                "user": "koa-core",
                "criticality": "critical",
            }
        ],
        "networks": [],
        "volumes": [],
        "packages": [],
        "files": [],
        "offline": {"enabled": True, "allow_network": False, "artifacts": []},
        "backup": {},
    }


def test_global_contract_forbids_silent_substitution_and_authority_expansion() -> None:
    system = _load("docs/contracts/system.contract.json")
    degradation = system["degradation_baseline"]
    assert degradation["optional_capability_failure"]["silent_substitution"] is False
    assert degradation["experience_subsystem_failure"]["silent_authority_substitution"] is False
    assert degradation["authority_verification_failure"]["automatic_bypass"] is False
    assert degradation["contract_incompatibility"]["automatic_schema_guessing"] is False
    assert system["offline_baseline"]["internet_required_for_global_core_authority"] is False


def test_offline_bundle_projection_preserves_no_substitution_rule() -> None:
    manifest = json.loads(render("offline_bundle", _plan())[0].text)
    assert manifest["verification"]["silent_substitution_allowed"] is False
    assert manifest["verification"]["transport_grants_authority"] is False
    assert manifest["network_access_allowed"] is False


def test_user_and_node_profiles_keep_external_providers_unavailable_not_replaced() -> None:
    user = _load("docs/contracts/profiles/user-lightweight.profile.json")
    node = _load("docs/contracts/profiles/sovereign-linux-node.profile.json")

    assert user["offline_behavior"]["internet_dependency"] == "optional_external_surfaces_only"
    assert node["offline_behavior"]["internet_dependency"] == "none_for_core"
    assert user["ai_boundary"]["authoritative_decisions_allowed"] is False
    assert node["ai_boundary"]["authoritative_decisions_allowed"] is False

    user_unavailable = set(user["offline_behavior"]["unavailable_capabilities"])
    assert {"chatgpt", "suno", "gamma", "ariane_external_voice"} <= user_unavailable

    node_unavailable = set(node["offline_behavior"]["unavailable_capabilities"])
    assert "uncached_remote_artifact_retrieval" in node_unavailable

    for profile in (user, node):
        for capability in profile["capabilities"].values():
            degraded = capability["degraded_behavior"].lower()
            assert "silent" in degraded and "substitution" in degraded
