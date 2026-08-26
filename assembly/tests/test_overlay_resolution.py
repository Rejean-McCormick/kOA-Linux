from __future__ import annotations

import json
from pathlib import Path

import pytest

from koa_assembly.profiles import ProfileResolver, ResolutionOutcome, describe_profile, order_overlays


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
PROFILE_ROOT = REPOSITORY_ROOT / "docs" / "contracts" / "profiles"


def contracts() -> dict[str, dict[str, object]]:
    return {
        path.relative_to(REPOSITORY_ROOT).as_posix(): json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(PROFILE_ROOT.glob("*.profile.json"))
    }


def profile(
    profile_id: str,
    kind: str,
    composition: dict[str, object],
    *,
    status: str = "active",
) -> dict[str, object]:
    return {
        "profile_id": profile_id,
        "profile_kind": kind,
        "version": "1.0.0",
        "status": status,
        "composition": composition,
        "capabilities": {},
        "components": {},
        "subsystems": {},
    }


def issue_codes(result: object) -> set[str]:
    return {issue.code for issue in result.issues}


def test_user_lightweight_with_appliance_shell_blocks_when_base_capabilities_are_absent() -> None:
    result = ProfileResolver(contracts()).resolve("user_lightweight", ["appliance_shell"])
    assert result.outcome is ResolutionOutcome.BLOCKED
    assert "required_base_capability_unresolved" in issue_codes(result)


def test_user_lightweight_with_appliance_shell_passes_with_explicit_base_capabilities() -> None:
    result = ProfileResolver(contracts()).resolve(
        "user_lightweight",
        ["appliance_shell"],
        explicit_base_capabilities=["interactive_user", "ariane_local_navigation"],
    )
    assert result.outcome is ResolutionOutcome.PASS


def test_user_lightweight_with_high_assurance_is_blocked_by_primary() -> None:
    result = ProfileResolver(contracts()).resolve("user_lightweight", ["high_assurance"])
    assert "primary_overlay_prohibited" in issue_codes(result)


def test_user_lightweight_with_sovereign_offline_is_blocked_by_overlay() -> None:
    result = ProfileResolver(contracts()).resolve("user_lightweight", ["sovereign_offline"])
    assert "overlay_primary_incompatible" in issue_codes(result)


def test_windows_wsl_rejects_all_active_overlays() -> None:
    resolver = ProfileResolver(contracts())
    for overlay_id in ("high_assurance", "sovereign_offline", "appliance_shell"):
        result = resolver.resolve("developer_windows_wsl", [overlay_id])
        assert result.outcome is ResolutionOutcome.BLOCKED
        assert issue_codes(result) & {
            "primary_overlay_prohibited",
            "primary_overlay_not_listed",
            "overlay_primary_incompatible",
            "overlay_primary_prohibited",
        }


def test_control_plane_high_assurance_passes() -> None:
    result = ProfileResolver(contracts()).resolve("control_plane", ["high_assurance"])
    assert result.outcome is ResolutionOutcome.PASS


def test_build_farm_sovereign_offline_conflict_is_not_guessed_away() -> None:
    result = ProfileResolver(contracts()).resolve("build_farm", ["sovereign_offline"])
    assert result.outcome is ResolutionOutcome.BLOCKED
    assert "overlay_primary_incompatible" in issue_codes(result)


def test_sovereign_hub_with_two_declared_overlays_passes() -> None:
    effective = ProfileResolver(contracts()).resolve(
        "sovereign_hub", ["sovereign_offline", "high_assurance"]
    ).require_effective()
    assert effective.overlays == (
        ("high_assurance", "1.0.0"),
        ("sovereign_offline", "1.0.0"),
    )


def test_pairwise_compatibility_must_be_declared_by_at_least_one_owner() -> None:
    source = {
        "base.json": profile(
            "base",
            "primary_profile",
            {"overlay_compatibility": [
                {"overlay_id": "left", "compatibility": "compatible"},
                {"overlay_id": "right", "compatibility": "compatible"},
            ]},
        ),
        "left.json": profile(
            "left", "profile_overlay", {"compatible_primary_profiles": ["base"]}
        ),
        "right.json": profile(
            "right", "profile_overlay", {"compatible_primary_profiles": ["base"]}
        ),
    }
    result = ProfileResolver(source).resolve("base", ["left", "right"])
    assert "overlay_pair_not_declared_compatible" in issue_codes(result)


def test_explicit_pairwise_prohibition_blocks_composition() -> None:
    source = {
        "base.json": profile(
            "base",
            "primary_profile",
            {"overlay_compatibility": [
                {"overlay_id": "left", "compatibility": "compatible"},
                {"overlay_id": "right", "compatibility": "compatible"},
            ]},
        ),
        "left.json": profile(
            "left",
            "profile_overlay",
            {
                "compatible_primary_profiles": ["base"],
                "compatible_overlays": ["right"],
                "incompatible_overlays": ["right"],
            },
        ),
        "right.json": profile(
            "right",
            "profile_overlay",
            {"compatible_primary_profiles": ["base"], "compatible_overlays": ["left"]},
        ),
    }
    result = ProfileResolver(source).resolve("base", ["left", "right"])
    assert "overlay_pair_prohibited" in issue_codes(result)


def test_required_overlay_dependency_is_enforced() -> None:
    source = {
        "base.json": profile(
            "base",
            "primary_profile",
            {"overlay_compatibility": [{"overlay_id": "child", "compatibility": "compatible"}]},
        ),
        "child.json": profile(
            "child",
            "profile_overlay",
            {"compatible_primary_profiles": ["base"], "required_overlays": ["parent"]},
        ),
    }
    result = ProfileResolver(source).resolve("base", ["child"])
    assert "required_overlay_missing" in issue_codes(result)


def test_duplicate_overlay_selection_is_blocked() -> None:
    source = {
        "base.json": profile(
            "base",
            "primary_profile",
            {"overlay_compatibility": [{"overlay_id": "overlay", "compatibility": "compatible"}]},
        ),
        "overlay.json": profile(
            "overlay", "profile_overlay", {"compatible_primary_profiles": ["base"]}
        ),
    }
    result = ProfileResolver(source).resolve("base", ["overlay", "overlay"])
    assert "duplicate_overlay" in issue_codes(result)


def test_missing_overlay_is_blocked() -> None:
    source = {"base.json": profile("base", "primary_profile", {})}
    result = ProfileResolver(source).resolve("base", ["missing"])
    assert "overlay_missing" in issue_codes(result)


def test_overlay_without_primary_compatibility_is_blocked() -> None:
    source = {
        "base.json": profile("base", "primary_profile", {}),
        "overlay.json": profile("overlay", "profile_overlay", {}),
    }
    result = ProfileResolver(source).resolve("base", ["overlay"])
    assert "missing_primary_compatibility" in issue_codes(result)


def test_primary_explicit_compatibility_list_is_closed() -> None:
    source = {
        "base.json": profile(
            "base",
            "primary_profile",
            {"compatible_overlay_ids": ["allowed"]},
        ),
        "other.json": profile(
            "other", "profile_overlay", {"compatible_primary_profiles": ["base"]}
        ),
    }
    result = ProfileResolver(source).resolve("base", ["other"])
    assert "primary_overlay_not_listed" in issue_codes(result)


def test_overlay_order_cycle_is_rejected() -> None:
    left = describe_profile(
        profile(
            "left",
            "profile_overlay",
            {
                "compatible_primary_profiles": ["base"],
                "compatible_overlays": ["right"],
                "required_overlay_order": ["left", "right"],
            },
        ),
        "left.json",
    )
    right = describe_profile(
        profile(
            "right",
            "profile_overlay",
            {
                "compatible_primary_profiles": ["base"],
                "compatible_overlays": ["left"],
                "required_overlay_order": ["right", "left"],
            },
        ),
        "right.json",
    )
    with pytest.raises(ValueError, match="ordering cycle"):
        order_overlays([left, right])


def test_overlay_order_without_edges_uses_identifier_order() -> None:
    left = describe_profile(
        profile(
            "zeta", "profile_overlay", {"compatible_primary_profiles": ["base"]}
        ),
        "zeta.json",
    )
    right = describe_profile(
        profile(
            "alpha", "profile_overlay", {"compatible_primary_profiles": ["base"]}
        ),
        "alpha.json",
    )
    assert [item.profile_id for item in order_overlays([left, right])] == ["alpha", "zeta"]
