"""Contract-level offline navigation conformance."""

from __future__ import annotations

from pathlib import Path
import json

REPO = Path(__file__).resolve().parents[2]


def _load(path: str) -> dict:
    return json.loads((REPO / path).read_text(encoding="utf-8"))


def test_ariane_local_navigation_remains_available_without_voice_or_external_ai() -> None:
    user = _load("docs/contracts/profiles/user-lightweight.profile.json")
    node = _load("docs/contracts/profiles/sovereign-linux-node.profile.json")

    assert user["capabilities"]["ariane_local_navigation"]["state"] == "required"
    assert user["offline_behavior"]["continuity_level"] == "core_required"
    assert node["offline_behavior"]["continuity_level"] == "core_required"

    for profile in (user, node):
        assert profile["ai_boundary"]["native_ai_dependency"] is False
        assert profile["ai_boundary"]["authoritative_decisions_allowed"] is False
        assert "ariane_external_voice" in profile["offline_behavior"]["unavailable_capabilities"]
        assert "ariane-voice" in profile["ai_boundary"]["approved_external_surfaces"]
        assert "local" in profile["ai_boundary"]["fallback_behavior"].lower()


def test_koa_spaces_offline_routes_are_declared_and_non_authoritative() -> None:
    system = _load("docs/contracts/system.contract.json")
    spaces = system["offline_baseline"]["koa_spaces"]
    assert spaces["space_and_manifest_cache"] == "local_verified_copy"
    assert spaces["offline_routes"] == "only_routes_declared_offline_capable"
    assert spaces["remote_widgets"] == "unavailable_or_explicitly_stale"
    assert spaces["business_state_authority"] == "unchanged"
