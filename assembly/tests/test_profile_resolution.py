from __future__ import annotations

import json
from pathlib import Path

import pytest

from koa_assembly.profiles import (
    CapabilityMembership,
    ComponentMembership,
    SubsystemMembership,
    ProfileResolver,
    ResolutionOutcome,
    normalize_identifier,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
PROFILE_ROOT = REPOSITORY_ROOT / "docs" / "contracts" / "profiles"


def load_active_contracts() -> dict[str, dict[str, object]]:
    return {
        path.relative_to(REPOSITORY_ROOT).as_posix(): json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(PROFILE_ROOT.glob("*.profile.json"))
    }


def minimal_profile(
    profile_id: str,
    *,
    kind: str = "primary_profile",
    capabilities: dict[str, object] | None = None,
    components: dict[str, object] | None = None,
    subsystems: dict[str, object] | None = None,
    inheritance: dict[str, object] | None = None,
    status: str = "active",
    composition: dict[str, object] | None = None,
) -> dict[str, object]:
    profile: dict[str, object] = {
        "profile_id": profile_id,
        "profile_kind": kind,
        "version": "1.0.0",
        "status": status,
        "capabilities": capabilities or {},
        "components": components or {},
        "subsystems": subsystems or {},
        "composition": composition or {},
    }
    if inheritance is not None:
        profile["inheritance"] = inheritance
    return profile


def test_all_ten_active_profile_contracts_are_registered() -> None:
    resolver = ProfileResolver(load_active_contracts())
    assert resolver.profile_ids == (
        "appliance_shell",
        "build_farm",
        "control_plane",
        "developer_linux_workstation",
        "developer_windows_wsl",
        "high_assurance",
        "sovereign_hub",
        "sovereign_linux_node",
        "sovereign_offline",
        "user_lightweight",
    )


def test_sovereign_node_composition_is_deterministic() -> None:
    contracts = load_active_contracts()
    required_base_capabilities = ["interactive_user", "ariane_local_navigation"]
    first = ProfileResolver(contracts).resolve(
        "sovereign_linux_node",
        ["appliance_shell", "high_assurance", "sovereign_offline"],
        explicit_base_capabilities=required_base_capabilities,
    ).require_effective()
    second = ProfileResolver(dict(reversed(list(contracts.items())))).resolve(
        "sovereign_linux_node",
        ["sovereign_offline", "appliance_shell", "high_assurance"],
        explicit_base_capabilities=reversed(required_base_capabilities),
    ).require_effective()
    assert first.to_dict() == second.to_dict()
    assert first.overlays == (
        ("high_assurance", "1.0.0"),
        ("sovereign_offline", "1.0.0"),
        ("appliance_shell", "1.0.0"),
    )
    assert first.effective_profile_id.startswith("effective:sovereign_linux_node:")


def test_absent_capability_is_not_substituted() -> None:
    contracts = {
        "primary.json": minimal_profile(
            "base",
            capabilities={"required": ["declared_capability"]},
        )
    }
    effective = ProfileResolver(contracts).resolve("base").require_effective()
    capability_map = {entry.capability_id: entry for entry in effective.capabilities}
    assert capability_map["declared_capability"].membership is CapabilityMembership.REQUIRED
    assert "invented_capability" not in capability_map


def test_required_and_prohibited_capability_blocks_composition() -> None:
    contracts = {
        "primary.json": minimal_profile(
            "base",
            capabilities={"required": ["export"]},
            composition={"overlay_compatibility": [{"overlay_id": "lockdown", "compatibility": "compatible"}]},
        ),
        "overlay.json": minimal_profile(
            "lockdown",
            kind="profile_overlay",
            capabilities={"prohibited": ["export"]},
            composition={"compatible_primary_profiles": ["base"]},
        ),
    }
    result = ProfileResolver(contracts).resolve("base", ["lockdown"])
    assert result.outcome is ResolutionOutcome.BLOCKED
    assert any(issue.code == "capability_conflict" for issue in result.issues)


def test_optional_capability_can_be_restricted_to_prohibited() -> None:
    contracts = {
        "primary.json": minimal_profile(
            "base",
            capabilities={"optional": ["remote_voice"]},
            composition={"overlay_compatibility": [{"overlay_id": "offline", "compatibility": "compatible"}]},
        ),
        "overlay.json": minimal_profile(
            "offline",
            kind="profile_overlay",
            capabilities={"prohibited": ["remote_voice"]},
            composition={"compatible_primary_profiles": ["base"]},
        ),
    }
    effective = ProfileResolver(contracts).resolve("base", ["offline"]).require_effective()
    membership = {entry.capability_id: entry.membership for entry in effective.capabilities}
    assert membership["remote_voice"] is CapabilityMembership.PROHIBITED


def test_missing_capability_dependency_blocks_composition() -> None:
    contracts = {
        "primary.json": minimal_profile(
            "base", capabilities={"required": ["publication"]}
        )
    }
    result = ProfileResolver(contracts).resolve(
        "base", capability_dependencies={"publication": ["identity"]}
    )
    assert result.outcome is ResolutionOutcome.BLOCKED
    assert result.issues[0].code == "capability_dependency_unresolved"
    assert "publication->identity:missing" in result.issues[0].detail


def test_prohibited_capability_dependency_blocks_composition() -> None:
    contracts = {
        "primary.json": minimal_profile(
            "base",
            capabilities={"required": ["publication"], "prohibited": ["identity"]},
        )
    }
    result = ProfileResolver(contracts).resolve(
        "base", capability_dependencies={"publication": ["identity"]}
    )
    assert any(
        issue.code == "capability_dependency_unresolved" and issue.detail.endswith(":prohibited")
        for issue in result.issues
    )


def test_required_and_prohibited_component_blocks_composition() -> None:
    contracts = {
        "primary.json": minimal_profile(
            "base",
            components={"required": ["audit-broker"]},
            composition={"overlay_compatibility": [{"overlay_id": "restricted", "compatibility": "compatible"}]},
        ),
        "overlay.json": minimal_profile(
            "restricted",
            kind="profile_overlay",
            components={"prohibited": ["audit_broker"]},
            composition={"compatible_primary_profiles": ["base"]},
        ),
    }
    result = ProfileResolver(contracts).resolve("base", ["restricted"])
    assert any(issue.code == "component_conflict" for issue in result.issues)


def test_component_identifiers_are_normalized_without_changing_membership() -> None:
    contracts = {
        "primary.json": minimal_profile(
            "base", components={"required": ["identity-and-trust"]}
        )
    }
    effective = ProfileResolver(contracts).resolve("base").require_effective()
    assert effective.components[0].component_id == "identity_and_trust"
    assert effective.components[0].membership is ComponentMembership.REQUIRED


def test_explicit_inheritance_is_applied_parent_first() -> None:
    contracts = {
        "parent.json": minimal_profile(
            "parent", capabilities={"required": ["parent_capability"]}
        ),
        "child.json": minimal_profile(
            "child",
            capabilities={"required": ["child_capability"]},
            inheritance={"inherited_profile_refs": ["parent@1.0.0"]},
        ),
    }
    result = ProfileResolver(contracts).resolve("child")
    effective = result.require_effective()
    assert result.ordered_profiles == ("parent", "child")
    assert [entry.capability_id for entry in effective.capabilities] == [
        "child_capability",
        "parent_capability",
    ]


def test_unresolved_inheritance_blocks_composition() -> None:
    contracts = {
        "child.json": minimal_profile(
            "child", inheritance={"inherited_profile_refs": ["missing@1.0.0"]}
        )
    }
    result = ProfileResolver(contracts).resolve("child")
    assert result.outcome is ResolutionOutcome.BLOCKED
    assert any(issue.code == "inheritance_invalid" for issue in result.issues)


def test_inheritance_cycle_blocks_composition() -> None:
    contracts = {
        "a.json": minimal_profile("a", inheritance={"inherited_profile_refs": ["b@1.0.0"]}),
        "b.json": minimal_profile("b", inheritance={"inherited_profile_refs": ["a@1.0.0"]}),
    }
    result = ProfileResolver(contracts).resolve("a")
    assert result.outcome is ResolutionOutcome.BLOCKED
    assert "cycle" in next(issue.detail for issue in result.issues if issue.code == "inheritance_invalid")


def test_missing_primary_blocks_without_effective_profile() -> None:
    result = ProfileResolver({}).resolve("missing")
    assert result.outcome is ResolutionOutcome.BLOCKED
    assert result.effective_profile is None
    with pytest.raises(ValueError, match="primary_missing"):
        result.require_effective()


def test_overlay_cannot_be_selected_as_primary() -> None:
    contracts = {
        "overlay.json": minimal_profile(
            "overlay",
            kind="profile_overlay",
            composition={"compatible_primary_profiles": ["base"]},
        )
    }
    result = ProfileResolver(contracts).resolve("overlay")
    assert any(issue.code == "primary_kind_invalid" for issue in result.issues)


def test_inactive_primary_and_overlay_fail_closed() -> None:
    contracts = {
        "base.json": minimal_profile("base", status="deprecated"),
        "overlay.json": minimal_profile(
            "overlay",
            kind="profile_overlay",
            status="archived",
            composition={"compatible_primary_profiles": ["base"]},
        ),
    }
    result = ProfileResolver(contracts).resolve("base", ["overlay"])
    assert {issue.code for issue in result.issues} >= {"primary_inactive", "overlay_inactive"}


def test_duplicate_profile_identity_is_rejected_at_registration() -> None:
    with pytest.raises(ValueError, match="duplicate profile identity"):
        ProfileResolver(
            {
                "one.json": minimal_profile("same"),
                "two.json": minimal_profile("same"),
            }
        )


def test_identifier_validation_rejects_path_like_values() -> None:
    assert normalize_identifier("identity-and-trust") == "identity_and_trust"
    with pytest.raises(ValueError, match="invalid identifier"):
        normalize_identifier("../identity")


def test_subsystems_resolve_in_a_separate_namespace_from_components() -> None:
    contracts = {
        "primary.json": minimal_profile(
            "base",
            components={"required": ["identity-and-trust"]},
            subsystems={"required": ["konnaxion", "orgo", "semantik_architect"]},
        )
    }
    effective = ProfileResolver(contracts).resolve("base").require_effective()
    assert {entry.component_id for entry in effective.components} == {"identity_and_trust"}
    assert {entry.subsystem_id for entry in effective.subsystems} == {"konnaxion", "orgo", "semantik_architect"}
    assert all(entry.membership is SubsystemMembership.REQUIRED for entry in effective.subsystems)


def test_required_and_prohibited_subsystem_blocks_composition() -> None:
    contracts = {
        "primary.json": minimal_profile(
            "base",
            subsystems={"required": ["orgo"]},
            composition={"overlay_compatibility": [{"overlay_id": "restricted", "compatibility": "compatible"}]},
        ),
        "overlay.json": minimal_profile(
            "restricted",
            kind="profile_overlay",
            subsystems={"prohibited": ["orgo"]},
            composition={"compatible_primary_profiles": ["base"]},
        ),
    }
    result = ProfileResolver(contracts).resolve("base", ["restricted"])
    assert any(issue.code == "subsystem_conflict" for issue in result.issues)


def test_effective_profile_declaration_is_deterministic_and_non_authoritative() -> None:
    contracts = load_active_contracts()
    effective = ProfileResolver(contracts).resolve("sovereign_linux_node").require_effective()
    digests = {source: "sha256:" + ("a" * 64) for _, _, source in effective.contributing_profiles}
    first = effective.to_declaration(source_digests=digests)
    second = effective.to_declaration(source_digests=dict(reversed(list(digests.items()))))
    assert first == second
    assert first["format"] == "koa.effective-profile"
    assert first["authority"] == "derived_projection"
    assert first["manual_edits"] == "prohibited"
    assert first["result"] == "pass"
    assert first["validation"] == {"outcome": "pass", "composition_conflicts": 0}
    assert first["unresolved_conflicts"] == []
    assert str(first["generated_evidence_identity"]).startswith("sha256:")


def test_effective_profile_declaration_rejects_unbound_source_digests() -> None:
    effective = ProfileResolver({
        "primary.json": minimal_profile("base"),
    }).resolve("base").require_effective()
    with pytest.raises(ValueError, match="source digests do not match"):
        effective.to_declaration(source_digests={"other.json": "sha256:" + "a" * 64})
