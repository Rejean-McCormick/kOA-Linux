from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Mapping, Sequence

from .capabilities import CapabilityEntry, extract_capabilities, normalize_identifier
from .membership import ComponentEntry, SubsystemEntry, extract_components, extract_subsystems


class ProfileKind(StrEnum):
    PRIMARY = "primary_profile"
    OVERLAY = "profile_overlay"


@dataclass(frozen=True, slots=True)
class ProfileDescriptor:
    profile_id: str
    version: str
    kind: ProfileKind
    status: str
    source: str
    compatible_primary_profiles: frozenset[str] | None
    incompatible_primary_profiles: frozenset[str]
    compatible_overlays: frozenset[str] | None
    incompatible_overlays: frozenset[str]
    primary_compatible_overlays: frozenset[str] | None
    primary_incompatible_overlays: frozenset[str]
    required_overlays: frozenset[str]
    composition_priority: int | None
    required_base_capabilities: frozenset[str]
    inherited_profiles: tuple[str, ...]
    order_edges: tuple[tuple[str, str], ...]
    capabilities: tuple[CapabilityEntry, ...]
    components: tuple[ComponentEntry, ...]
    subsystems: tuple[SubsystemEntry, ...]

    @property
    def active(self) -> bool:
        return self.status == "active"


@dataclass(frozen=True, slots=True)
class CompatibilityIssue:
    code: str
    profiles: tuple[str, ...]
    detail: str


def _as_identifier_set(value: object, object_key: str = "profile_id") -> frozenset[str]:
    if value is None:
        return frozenset()
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise ValueError("compatibility list must be an array")
    identifiers = []
    for item in value:
        if isinstance(item, str):
            identifiers.append(normalize_identifier(item))
        elif isinstance(item, Mapping) and isinstance(item.get(object_key), str):
            identifiers.append(normalize_identifier(item[object_key]))
        else:
            raise ValueError("compatibility member must be a profile identifier or object")
    return frozenset(identifiers)


def _profile_kind(contract: Mapping[str, Any]) -> ProfileKind:
    raw = contract.get("profile_kind", contract.get("profile_type"))
    if not isinstance(raw, str):
        raise ValueError("profile contract does not declare profile_kind or profile_type")
    normalized = raw.strip().lower()
    if normalized in {"primary", "primary_profile", "primary_deployment_profile", "deployment_profile"}:
        return ProfileKind.PRIMARY
    if normalized in {"overlay", "profile_overlay", "deployment_profile_overlay"}:
        return ProfileKind.OVERLAY
    raise ValueError(f"unsupported profile kind: {raw!r}")


def _extract_inheritance(contract: Mapping[str, Any]) -> tuple[str, ...]:
    inheritance = contract.get("inheritance")
    if not isinstance(inheritance, Mapping):
        return ()
    values = []
    for key in ("inherited_profile_refs", "inherits_profile_ids", "inherits_profiles"):
        raw = inheritance.get(key)
        if raw is None:
            continue
        if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes, bytearray)):
            raise ValueError(f"inheritance.{key} must be an array")
        for item in raw:
            if not isinstance(item, str):
                raise ValueError("inherited profile references must be strings")
            profile_id = item.split("@", 1)[0]
            identifiers = normalize_identifier(profile_id)
            values.append(identifiers)
    return tuple(sorted(set(values)))


def _sequence_edges(values: object) -> tuple[tuple[str, str], ...]:
    if values is None:
        return ()
    if not isinstance(values, Sequence) or isinstance(values, (str, bytes, bytearray)):
        raise ValueError("overlay order must be an array")
    normalized = []
    aliases = {
        "primary_profile": None,
        "base_profile": None,
        "high_assurance_when_selected": "high_assurance",
        "sovereign_offline_when_selected": "sovereign_offline",
        "appliance_shell_when_selected": "appliance_shell",
    }
    for item in values:
        if not isinstance(item, str):
            raise ValueError("overlay order values must be strings")
        value = aliases.get(item, item)
        if value is not None:
            normalized.append(normalize_identifier(value))
    return tuple((left, right) for left, right in zip(normalized, normalized[1:]))


def describe_profile(contract: Mapping[str, Any], source: str) -> ProfileDescriptor:
    if not isinstance(contract, Mapping):
        raise TypeError("profile contract must be a mapping")
    raw_profile_id = contract.get("profile_id")
    raw_version = contract.get("version")
    raw_status = contract.get("status")
    if not isinstance(raw_profile_id, str) or not isinstance(raw_version, str) or not isinstance(raw_status, str):
        raise ValueError("profile_id, version, and status are required strings")
    profile_id = normalize_identifier(raw_profile_id)
    kind = _profile_kind(contract)
    composition = contract.get("composition")
    composition = composition if isinstance(composition, Mapping) else {}
    overlay_composition = contract.get("overlay_composition")
    overlay_composition = overlay_composition if isinstance(overlay_composition, Mapping) else {}
    inheritance = contract.get("inheritance")
    inheritance = inheritance if isinstance(inheritance, Mapping) else {}

    compatible_primary: frozenset[str] | None = None
    incompatible_primary = frozenset()
    compatible_overlays: frozenset[str] | None = None
    incompatible_overlays = frozenset()
    primary_compatible: frozenset[str] | None = None
    primary_incompatible = frozenset()
    required_overlays = frozenset()
    raw_priority = composition.get("composition_priority")
    if raw_priority is not None and (not isinstance(raw_priority, int) or isinstance(raw_priority, bool)):
        raise ValueError("composition.composition_priority must be an integer or null")
    composition_priority = raw_priority
    edges: list[tuple[str, str]] = []

    if kind is ProfileKind.OVERLAY:
        for key in ("compatible_primary_profiles", "allowed_base_profiles", "compatible_base_profiles"):
            if key in composition:
                compatible_primary = _as_identifier_set(composition[key])
                break
        for key in ("incompatible_primary_profiles", "prohibited_base_profiles", "incompatible_base_profiles"):
            if key in composition:
                incompatible_primary = _as_identifier_set(composition[key])
                break
        if "compatible_overlays" in composition:
            compatible_overlays = _as_identifier_set(composition["compatible_overlays"])
        elif "optional_overlays" in composition or "required_overlays" in composition:
            compatible_overlays = _as_identifier_set(composition.get("optional_overlays")) | _as_identifier_set(
                composition.get("required_overlays")
            )
        if "incompatible_overlays" in composition:
            incompatible_overlays = _as_identifier_set(composition["incompatible_overlays"])
        elif "incompatible_profiles" in composition:
            incompatible_overlays = _as_identifier_set(composition["incompatible_profiles"])
        if "incompatible_profiles" in composition:
            incompatible_primary = _as_identifier_set(composition["incompatible_profiles"])
        required_overlays = _as_identifier_set(composition.get("required_overlays"))
        required_base_capabilities = _as_identifier_set(composition.get("required_base_capabilities"), object_key="capability_id")
        edges.extend(_sequence_edges(composition.get("required_overlay_order")))
        edges.extend(_sequence_edges(composition.get("application_order")))
    else:
        compatibility_entries = composition.get("overlay_compatibility")
        if compatibility_entries is not None:
            if not isinstance(compatibility_entries, Sequence) or isinstance(
                compatibility_entries, (str, bytes, bytearray)
            ):
                raise ValueError("overlay_compatibility must be an array")
            allowed = set()
            denied = set()
            for item in compatibility_entries:
                if not isinstance(item, Mapping) or not isinstance(item.get("overlay_id"), str):
                    raise ValueError("overlay_compatibility entries require overlay_id")
                overlay_id = normalize_identifier(item["overlay_id"])
                compatibility = str(item.get("compatibility", "")).strip().lower()
                if compatibility in {"compatible", "compatible_with_constraints"}:
                    allowed.add(overlay_id)
                elif compatibility in {"not_compatible", "incompatible"}:
                    denied.add(overlay_id)
                else:
                    raise ValueError(f"unsupported overlay compatibility: {compatibility!r}")
            primary_compatible = frozenset(allowed)
            primary_incompatible = frozenset(denied)
        else:
            for container in (composition, overlay_composition, inheritance):
                for key in ("compatible_overlay_ids", "eligible_overlay_ids", "compatible_overlays"):
                    if key in container:
                        primary_compatible = _as_identifier_set(container[key])
                        break
                for key in ("incompatible_overlay_ids", "incompatible_overlays"):
                    if key in container:
                        primary_incompatible = _as_identifier_set(container[key])
                        break
                if primary_compatible is not None or primary_incompatible:
                    break
            optional_overlays = composition.get("optional_overlays")
            required_overlays = _as_identifier_set(composition.get("required_overlays"))
            if optional_overlays is not None or required_overlays:
                primary_compatible = _as_identifier_set(optional_overlays) | required_overlays
            incompatible_profiles = composition.get("incompatible_profiles")
            if incompatible_profiles is not None:
                primary_incompatible = _as_identifier_set(incompatible_profiles)
        required_overlays = _as_identifier_set(composition.get("required_overlays"))
        required_base_capabilities = frozenset()

    return ProfileDescriptor(
        profile_id=profile_id,
        version=raw_version,
        kind=kind,
        status=raw_status.strip().lower(),
        source=source,
        compatible_primary_profiles=compatible_primary,
        incompatible_primary_profiles=incompatible_primary,
        compatible_overlays=compatible_overlays,
        incompatible_overlays=incompatible_overlays,
        primary_compatible_overlays=primary_compatible,
        primary_incompatible_overlays=primary_incompatible,
        required_overlays=required_overlays,
        composition_priority=composition_priority,
        required_base_capabilities=required_base_capabilities,
        inherited_profiles=_extract_inheritance(contract),
        order_edges=tuple(sorted(set(edges))),
        capabilities=extract_capabilities(contract, source),
        components=extract_components(contract, source),
        subsystems=extract_subsystems(contract, source),
    )


def validate_overlay_compatibility(
    primary: ProfileDescriptor,
    overlays: Sequence[ProfileDescriptor],
    base_capability_ids: frozenset[str] | None = None,
) -> tuple[CompatibilityIssue, ...]:
    issues: list[CompatibilityIssue] = []
    selected_ids = {overlay.profile_id for overlay in overlays}
    declared_base_capabilities = base_capability_ids or frozenset(
        entry.capability_id
        for entry in primary.capabilities
        if entry.membership.value not in {"prohibited", "not_applicable"}
    )
    for overlay in overlays:
        if overlay.kind is not ProfileKind.OVERLAY:
            issues.append(
                CompatibilityIssue("not_overlay", (overlay.profile_id,), "selected profile is not an overlay")
            )
            continue
        if overlay.compatible_primary_profiles is None:
            issues.append(
                CompatibilityIssue(
                    "missing_primary_compatibility",
                    (primary.profile_id, overlay.profile_id),
                    "overlay does not declare compatible primary profiles",
                )
            )
        elif primary.profile_id not in overlay.compatible_primary_profiles:
            issues.append(
                CompatibilityIssue(
                    "overlay_primary_incompatible",
                    (primary.profile_id, overlay.profile_id),
                    "overlay does not permit the selected primary profile",
                )
            )
        if primary.profile_id in overlay.incompatible_primary_profiles:
            issues.append(
                CompatibilityIssue(
                    "overlay_primary_prohibited",
                    (primary.profile_id, overlay.profile_id),
                    "overlay explicitly prohibits the selected primary profile",
                )
            )
        if overlay.profile_id in primary.primary_incompatible_overlays:
            issues.append(
                CompatibilityIssue(
                    "primary_overlay_prohibited",
                    (primary.profile_id, overlay.profile_id),
                    "primary profile explicitly prohibits the overlay",
                )
            )
        if (
            primary.primary_compatible_overlays is not None
            and overlay.profile_id not in primary.primary_compatible_overlays
        ):
            issues.append(
                CompatibilityIssue(
                    "primary_overlay_not_listed",
                    (primary.profile_id, overlay.profile_id),
                    "primary profile has an explicit compatibility list that omits the overlay",
                )
            )
        missing = overlay.required_overlays - selected_ids
        if missing:
            issues.append(
                CompatibilityIssue(
                    "required_overlay_missing",
                    tuple(sorted((overlay.profile_id, *missing))),
                    "required overlay dependency is absent",
                )
            )
        missing_capabilities = overlay.required_base_capabilities - declared_base_capabilities
        for capability_id in sorted(missing_capabilities):
            issues.append(
                CompatibilityIssue(
                    "required_base_capability_unresolved",
                    (primary.profile_id, overlay.profile_id),
                    f"required base capability is absent: {capability_id}",
                )
            )

    for index, left in enumerate(overlays):
        for right in overlays[index + 1 :]:
            pair = frozenset((left.profile_id, right.profile_id))
            if right.profile_id in left.incompatible_overlays or left.profile_id in right.incompatible_overlays:
                issues.append(
                    CompatibilityIssue(
                        "overlay_pair_prohibited",
                        tuple(sorted(pair)),
                        "an overlay explicitly prohibits the other overlay",
                    )
                )
                continue
            declarations = []
            if left.compatible_overlays is not None:
                declarations.append(right.profile_id in left.compatible_overlays)
            if right.compatible_overlays is not None:
                declarations.append(left.profile_id in right.compatible_overlays)
            if not declarations or not any(declarations):
                issues.append(
                    CompatibilityIssue(
                        "overlay_pair_not_declared_compatible",
                        tuple(sorted(pair)),
                        "no active overlay contract declares this pair compatible",
                    )
                )

    return tuple(sorted(issues, key=lambda issue: (issue.code, issue.profiles, issue.detail)))


def order_overlays(overlays: Sequence[ProfileDescriptor]) -> tuple[ProfileDescriptor, ...]:
    by_id = {overlay.profile_id: overlay for overlay in overlays}
    incoming = {profile_id: set() for profile_id in by_id}
    outgoing = {profile_id: set() for profile_id in by_id}
    for overlay in overlays:
        for left, right in overlay.order_edges:
            if left in by_id and right in by_id and left != right:
                outgoing[left].add(right)
                incoming[right].add(left)

    def _order_key(profile_id: str) -> tuple[int, str]:
        priority = by_id[profile_id].composition_priority
        return (priority if priority is not None else 1001, profile_id)

    ready = sorted((profile_id for profile_id, parents in incoming.items() if not parents), key=_order_key)
    ordered_ids: list[str] = []
    while ready:
        current = ready.pop(0)
        ordered_ids.append(current)
        for child in sorted(outgoing[current]):
            incoming[child].discard(current)
            if not incoming[child] and child not in ordered_ids and child not in ready:
                ready.append(child)
                ready.sort(key=_order_key)
    if len(ordered_ids) != len(by_id):
        cycle_members = sorted(profile_id for profile_id, parents in incoming.items() if parents)
        raise ValueError(f"overlay ordering cycle: {', '.join(cycle_members)}")
    return tuple(by_id[profile_id] for profile_id in ordered_ids)
