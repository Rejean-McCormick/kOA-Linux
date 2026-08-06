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
    user_available = " ".join(user["offline_capability_envelope"]["available_without_internet"]).lower()
    user_unavailable = " ".join(user["offline_capability_envelope"]["unavailable_without_internet"]).lower()
    node_available = " ".join(node["offline_capability_envelope"]["available_without_internet"]).lower()
    assert "ariane non-voice navigation" in user_available
    assert "external ariane voice" in user_unavailable
    assert "ariane non-voice navigation" in node_available


def test_koa_spaces_offline_routes_are_declared_and_non_authoritative() -> None:
    system = _load("docs/contracts/system.contract.json")
    spaces = system["offline_baseline"]["koa_spaces"]
    assert spaces["space_and_manifest_cache"] == "local_verified_copy"
    assert spaces["offline_routes"] == "only_routes_declared_offline_capable"
    assert spaces["remote_widgets"] == "unavailable_or_explicitly_stale"
    assert spaces["business_state_authority"] == "unchanged"
