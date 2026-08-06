from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import hashlib
import json
from typing import Any, Iterable, Mapping

from .capabilities import (
    CapabilityEntry,
    CapabilityMembership,
    CapabilityResolution,
    merge_capabilities,
    normalize_identifier,
)
from .membership import ComponentEntry, ComponentResolution, merge_components
from .overlays import (
    ProfileDescriptor,
    ProfileKind,
    describe_profile,
    order_overlays,
    validate_overlay_compatibility,
)


class ResolutionOutcome(StrEnum):
    PASS = "pass"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class ResolutionIssue:
    code: str
    profiles: tuple[str, ...]
    detail: str

    def to_dict(self) -> dict[str, object]:
        return {"code": self.code, "profiles": list(self.profiles), "detail": self.detail}


@dataclass(frozen=True, slots=True)
class EffectiveProfile:
    effective_profile_id: str
    primary_profile_id: str
    primary_version: str
    overlays: tuple[tuple[str, str], ...]
    contributing_profiles: tuple[tuple[str, str, str], ...]
    capabilities: tuple[CapabilityEntry, ...]
    components: tuple[ComponentEntry, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "effective_profile_id": self.effective_profile_id,
            "primary_profile": {
                "profile_id": self.primary_profile_id,
                "version": self.primary_version,
            },
            "overlays": [
                {"profile_id": profile_id, "version": version}
                for profile_id, version in self.overlays
            ],
            "contributing_profiles": [
                {"profile_id": profile_id, "version": version, "source": source}
                for profile_id, version, source in self.contributing_profiles
            ],
            "capabilities": [entry.to_dict() for entry in self.capabilities],
            "components": [entry.to_dict() for entry in self.components],
        }


@dataclass(frozen=True, slots=True)
class ResolutionResult:
    outcome: ResolutionOutcome
    effective_profile: EffectiveProfile | None
    issues: tuple[ResolutionIssue, ...]
    ordered_profiles: tuple[str, ...]

    @property
    def passed(self) -> bool:
        return self.outcome is ResolutionOutcome.PASS

    def require_effective(self) -> EffectiveProfile:
        if self.effective_profile is None:
            details = "; ".join(f"{issue.code}: {issue.detail}" for issue in self.issues)
            raise ValueError(f"profile composition blocked: {details}")
        return self.effective_profile


class ProfileResolver:
    def __init__(self, contracts: Mapping[str, Mapping[str, Any]]) -> None:
        descriptors: dict[str, ProfileDescriptor] = {}
        for source, contract in sorted(contracts.items()):
            descriptor = describe_profile(contract, source)
            if descriptor.profile_id in descriptors:
                raise ValueError(f"duplicate profile identity: {descriptor.profile_id}")
            descriptors[descriptor.profile_id] = descriptor
        self._profiles = descriptors

    @property
    def profile_ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._profiles))

    def _get(self, profile_id: str) -> ProfileDescriptor | None:
        return self._profiles.get(normalize_identifier(profile_id))

    def _inheritance_order(self, root: ProfileDescriptor) -> tuple[ProfileDescriptor, ...]:
        state: dict[str, int] = {}
        ordered: list[ProfileDescriptor] = []

        def visit(profile: ProfileDescriptor, path: tuple[str, ...]) -> None:
            current_state = state.get(profile.profile_id, 0)
            if current_state == 1:
                cycle = " -> ".join((*path, profile.profile_id))
                raise ValueError(f"profile inheritance cycle: {cycle}")
            if current_state == 2:
                return
            state[profile.profile_id] = 1
            for parent_id in profile.inherited_profiles:
                parent = self._profiles.get(parent_id)
                if parent is None:
                    raise LookupError(f"unresolved inherited profile: {profile.profile_id}->{parent_id}")
                visit(parent, (*path, profile.profile_id))
            state[profile.profile_id] = 2
            ordered.append(profile)

        visit(root, ())
        return tuple(ordered)

    def resolve(
        self,
        primary_profile_id: str,
        overlay_ids: Iterable[str] = (),
        *,
        capability_dependencies: Mapping[str, Iterable[str]] | None = None,
        explicit_base_capabilities: Iterable[str] = (),
    ) -> ResolutionResult:
        issues: list[ResolutionIssue] = []
        primary = self._get(primary_profile_id)
        if primary is None:
            return ResolutionResult(
                ResolutionOutcome.BLOCKED,
                None,
                (ResolutionIssue("primary_missing", (normalize_identifier(primary_profile_id),), "primary profile is not registered"),),
                (),
            )
        if primary.kind is not ProfileKind.PRIMARY:
            issues.append(
                ResolutionIssue("primary_kind_invalid", (primary.profile_id,), "selected primary is an overlay")
            )
        if not primary.active:
            issues.append(
                ResolutionIssue("primary_inactive", (primary.profile_id,), "primary profile is not active")
            )

        normalized_overlay_ids = [normalize_identifier(value) for value in overlay_ids]
        if len(normalized_overlay_ids) != len(set(normalized_overlay_ids)):
            issues.append(
                ResolutionIssue(
                    "duplicate_overlay",
                    tuple(sorted(normalized_overlay_ids)),
                    "an overlay was selected more than once",
                )
            )
        overlays: list[ProfileDescriptor] = []
        for overlay_id in sorted(set(normalized_overlay_ids)):
            overlay = self._profiles.get(overlay_id)
            if overlay is None:
                issues.append(
                    ResolutionIssue("overlay_missing", (overlay_id,), "selected overlay is not registered")
                )
                continue
            if not overlay.active:
                issues.append(
                    ResolutionIssue("overlay_inactive", (overlay_id,), "selected overlay is not active")
                )
            overlays.append(overlay)

        try:
            primary_lineage = self._inheritance_order(primary)
        except (LookupError, ValueError) as exc:
            issues.append(ResolutionIssue("inheritance_invalid", (primary.profile_id,), str(exc)))
            primary_lineage = (primary,)

        for overlay in overlays:
            try:
                lineage = self._inheritance_order(overlay)
            except (LookupError, ValueError) as exc:
                issues.append(ResolutionIssue("inheritance_invalid", (overlay.profile_id,), str(exc)))
                continue
            inherited = tuple(profile.profile_id for profile in lineage[:-1])
            if inherited:
                issues.append(
                    ResolutionIssue(
                        "overlay_inheritance_present",
                        (overlay.profile_id, *inherited),
                        "overlay inheritance must be explicitly evaluated by its owner contract",
                    )
                )

        primary_capability_ids = {
            entry.capability_id
            for profile in primary_lineage
            for entry in profile.capabilities
            if entry.membership.value not in {"prohibited", "not_applicable"}
        }
        explicit_capability_entries = tuple(
            CapabilityEntry(
                normalize_identifier(capability_id),
                CapabilityMembership.REQUIRED,
                (),
                ("explicit_base_capabilities",),
            )
            for capability_id in sorted(set(explicit_base_capabilities))
        )
        primary_capability_ids.update(entry.capability_id for entry in explicit_capability_entries)
        for compatibility_issue in validate_overlay_compatibility(
            primary, overlays, frozenset(primary_capability_ids)
        ):
            issues.append(
                ResolutionIssue(
                    compatibility_issue.code,
                    compatibility_issue.profiles,
                    compatibility_issue.detail,
                )
            )

        try:
            ordered_overlays = order_overlays(overlays)
        except ValueError as exc:
            issues.append(
                ResolutionIssue(
                    "overlay_order_cycle",
                    tuple(sorted(overlay.profile_id for overlay in overlays)),
                    str(exc),
                )
            )
            ordered_overlays = tuple(sorted(overlays, key=lambda item: item.profile_id))

        selected_profiles = (*primary_lineage, *ordered_overlays)
        capability_groups = [profile.capabilities for profile in selected_profiles]
        if explicit_capability_entries:
            capability_groups.insert(len(primary_lineage), explicit_capability_entries)
        capability_resolution: CapabilityResolution = merge_capabilities(
            capability_groups, capability_dependencies
        )
        component_resolution: ComponentResolution = merge_components(
            profile.components for profile in selected_profiles
        )
        for conflict in capability_resolution.conflicts:
            issues.append(
                ResolutionIssue(
                    "capability_conflict",
                    conflict.sources,
                    f"{conflict.capability_id}: {conflict.reason}",
                )
            )
        for dependency in capability_resolution.unresolved_dependencies:
            issues.append(
                ResolutionIssue(
                    "capability_dependency_unresolved",
                    tuple(profile.profile_id for profile in selected_profiles),
                    dependency,
                )
            )
        for conflict in component_resolution.conflicts:
            issues.append(
                ResolutionIssue(
                    "component_conflict",
                    conflict.sources,
                    f"{conflict.component_id}: {conflict.reason}",
                )
            )

        issues = sorted(issues, key=lambda issue: (issue.code, issue.profiles, issue.detail))
        ordered_ids = tuple(profile.profile_id for profile in selected_profiles)
        if issues:
            return ResolutionResult(ResolutionOutcome.BLOCKED, None, tuple(issues), ordered_ids)

        contributing = tuple(
            (profile.profile_id, profile.version, profile.source) for profile in selected_profiles
        )
        digest_payload = {
            "profiles": contributing,
            "capabilities": [entry.to_dict() for entry in capability_resolution.entries],
            "components": [entry.to_dict() for entry in component_resolution.entries],
        }
        digest = hashlib.sha256(
            json.dumps(digest_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        effective = EffectiveProfile(
            effective_profile_id=f"effective:{primary.profile_id}:{digest}",
            primary_profile_id=primary.profile_id,
            primary_version=primary.version,
            overlays=tuple((overlay.profile_id, overlay.version) for overlay in ordered_overlays),
            contributing_profiles=contributing,
            capabilities=capability_resolution.entries,
            components=component_resolution.entries,
        )
        return ResolutionResult(ResolutionOutcome.PASS, effective, (), ordered_ids)
