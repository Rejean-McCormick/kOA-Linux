from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Iterable, Mapping, Sequence


class CapabilityMembership(StrEnum):
    REQUIRED = "required"
    OPTIONAL = "optional"
    CONDITIONAL = "conditional"
    PROHIBITED = "prohibited"
    NOT_APPLICABLE = "not_applicable"


@dataclass(frozen=True, slots=True)
class CapabilityEntry:
    capability_id: str
    membership: CapabilityMembership
    conditions: tuple[str, ...] = ()
    sources: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "capability_id": self.capability_id,
            "membership": self.membership.value,
            "conditions": list(self.conditions),
            "sources": list(self.sources),
        }


@dataclass(frozen=True, slots=True)
class CapabilityConflict:
    capability_id: str
    memberships: tuple[CapabilityMembership, ...]
    sources: tuple[str, ...]
    reason: str


@dataclass(frozen=True, slots=True)
class CapabilityResolution:
    entries: tuple[CapabilityEntry, ...]
    conflicts: tuple[CapabilityConflict, ...] = ()
    unresolved_dependencies: tuple[str, ...] = ()

    def as_map(self) -> dict[str, CapabilityEntry]:
        return {entry.capability_id: entry for entry in self.entries}

    @property
    def valid(self) -> bool:
        return not self.conflicts and not self.unresolved_dependencies


def normalize_identifier(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("identifier must be a string")
    normalized = value.strip().lower().replace("-", "_").replace(" ", "_")
    while "__" in normalized:
        normalized = normalized.replace("__", "_")
    if not normalized or normalized.startswith("_") or normalized.endswith("_"):
        raise ValueError(f"invalid identifier: {value!r}")
    allowed = set("abcdefghijklmnopqrstuvwxyz0123456789_")
    if any(character not in allowed for character in normalized):
        raise ValueError(f"invalid identifier: {value!r}")
    return normalized


def _conditions_from_item(item: Mapping[str, Any]) -> tuple[str, ...]:
    raw = item.get("conditions")
    if raw is None and isinstance(item.get("condition"), str):
        raw = [item["condition"]]
    if raw is None:
        return ()
    if isinstance(raw, str):
        raw = [raw]
    if not isinstance(raw, Sequence) or isinstance(raw, (bytes, bytearray)):
        raise ValueError("capability conditions must be strings")
    conditions = []
    for condition in raw:
        if not isinstance(condition, str) or not condition.strip():
            raise ValueError("capability conditions must be non-empty strings")
        conditions.append(condition.strip())
    return tuple(sorted(set(conditions)))


def _item_identifier(item: object) -> tuple[str, tuple[str, ...]]:
    if isinstance(item, str):
        return normalize_identifier(item), ()
    if not isinstance(item, Mapping):
        raise ValueError("capability member must be a string or object")
    identifier = item.get("capability_id", item.get("capability", item.get("id")))
    if not isinstance(identifier, str):
        raise ValueError("capability object requires capability_id, capability, or id")
    return normalize_identifier(identifier), _conditions_from_item(item)


def _membership_from_state(value: object) -> CapabilityMembership:
    if not isinstance(value, str):
        raise ValueError("capability state must be a string")
    normalized = value.strip().lower()
    aliases = {
        "required": CapabilityMembership.REQUIRED,
        "optional": CapabilityMembership.OPTIONAL,
        "conditional": CapabilityMembership.CONDITIONAL,
        "prohibited": CapabilityMembership.PROHIBITED,
        "excluded": CapabilityMembership.PROHIBITED,
        "disabled": CapabilityMembership.PROHIBITED,
        "not_applicable": CapabilityMembership.NOT_APPLICABLE,
    }
    try:
        return aliases[normalized]
    except KeyError as exc:
        raise ValueError(f"unsupported capability state: {value!r}") from exc


def _entries_from_grouped_mapping(
    grouped: Mapping[str, Any], source: str
) -> list[CapabilityEntry]:
    aliases = {
        "required": CapabilityMembership.REQUIRED,
        "optional": CapabilityMembership.OPTIONAL,
        "conditional": CapabilityMembership.CONDITIONAL,
        "prohibited": CapabilityMembership.PROHIBITED,
        "excluded": CapabilityMembership.PROHIBITED,
        "not_applicable": CapabilityMembership.NOT_APPLICABLE,
        "disabled": CapabilityMembership.PROHIBITED,
    }
    entries: list[CapabilityEntry] = []
    for key, membership in aliases.items():
        raw = grouped.get(key)
        if raw is None:
            continue
        if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes, bytearray)):
            raise ValueError(f"capabilities.{key} must be an array")
        for item in raw:
            identifier, conditions = _item_identifier(item)
            entries.append(CapabilityEntry(identifier, membership, conditions, (source,)))
    return entries


def extract_capabilities(contract: Mapping[str, Any], source: str) -> tuple[CapabilityEntry, ...]:
    """Normalize only capability shapes explicitly used by active profile contracts."""

    if not isinstance(contract, Mapping):
        raise TypeError("profile contract must be a mapping")
    entries: list[CapabilityEntry] = []

    capabilities = contract.get("capabilities")
    if isinstance(capabilities, Mapping):
        grouped_keys = {"required", "optional", "conditional", "prohibited", "excluded", "not_applicable"}
        if grouped_keys.intersection(capabilities):
            entries.extend(_entries_from_grouped_mapping(capabilities, source))
        else:
            for capability_id, details in capabilities.items():
                if not isinstance(details, Mapping) or "state" not in details:
                    continue
                membership = _membership_from_state(details["state"])
                conditions = _conditions_from_item(details)
                entries.append(
                    CapabilityEntry(
                        normalize_identifier(capability_id), membership, conditions, (source,)
                    )
                )

    envelope = contract.get("capability_envelope")
    if isinstance(envelope, Mapping):
        entries.extend(_entries_from_grouped_mapping(envelope, source))

    policy = contract.get("capability_policy")
    if isinstance(policy, Mapping):
        policy_groups = {
            "required_capability_ids": CapabilityMembership.REQUIRED,
            "optional_capability_ids": CapabilityMembership.OPTIONAL,
            "conditional_capability_ids": CapabilityMembership.CONDITIONAL,
            "disabled_capability_ids": CapabilityMembership.PROHIBITED,
            "prohibited_capability_ids": CapabilityMembership.PROHIBITED,
        }
        for key, membership in policy_groups.items():
            raw = policy.get(key)
            if raw is None:
                continue
            if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes, bytearray)):
                raise ValueError(f"capability_policy.{key} must be an array")
            for item in raw:
                identifier, conditions = _item_identifier(item)
                entries.append(CapabilityEntry(identifier, membership, conditions, (source,)))

    top_level_groups = {
        "required_capabilities": CapabilityMembership.REQUIRED,
        "optional_capabilities": CapabilityMembership.OPTIONAL,
        "conditional_capabilities": CapabilityMembership.CONDITIONAL,
        "prohibited_capabilities": CapabilityMembership.PROHIBITED,
    }
    for key, membership in top_level_groups.items():
        raw = contract.get(key)
        if raw is None:
            continue
        if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes, bytearray)):
            raise ValueError(f"{key} must be an array")
        for item in raw:
            identifier, conditions = _item_identifier(item)
            entries.append(CapabilityEntry(identifier, membership, conditions, (source,)))

    return tuple(sorted(entries, key=lambda item: (item.capability_id, item.membership.value, item.conditions)))


def _merge_memberships(memberships: set[CapabilityMembership]) -> CapabilityMembership | None:
    if CapabilityMembership.REQUIRED in memberships and CapabilityMembership.PROHIBITED in memberships:
        return None
    if CapabilityMembership.PROHIBITED in memberships:
        return CapabilityMembership.PROHIBITED
    if CapabilityMembership.REQUIRED in memberships:
        return CapabilityMembership.REQUIRED
    if CapabilityMembership.CONDITIONAL in memberships:
        return CapabilityMembership.CONDITIONAL
    if CapabilityMembership.OPTIONAL in memberships:
        return CapabilityMembership.OPTIONAL
    return CapabilityMembership.NOT_APPLICABLE


def merge_capabilities(
    groups: Iterable[Iterable[CapabilityEntry]],
    dependencies: Mapping[str, Iterable[str]] | None = None,
) -> CapabilityResolution:
    collected: dict[str, list[CapabilityEntry]] = {}
    for group in groups:
        for entry in group:
            collected.setdefault(entry.capability_id, []).append(entry)

    merged: list[CapabilityEntry] = []
    conflicts: list[CapabilityConflict] = []
    for capability_id in sorted(collected):
        candidates = collected[capability_id]
        memberships = {candidate.membership for candidate in candidates}
        membership = _merge_memberships(memberships)
        sources = tuple(sorted({source for candidate in candidates for source in candidate.sources}))
        conditions = tuple(sorted({condition for candidate in candidates for condition in candidate.conditions}))
        if membership is None:
            conflicts.append(
                CapabilityConflict(
                    capability_id=capability_id,
                    memberships=tuple(sorted(memberships, key=lambda item: item.value)),
                    sources=sources,
                    reason="required_and_prohibited",
                )
            )
            continue
        merged.append(CapabilityEntry(capability_id, membership, conditions, sources))

    merged_map = {entry.capability_id: entry for entry in merged}
    unresolved: list[str] = []
    if dependencies:
        for raw_capability_id, raw_dependencies in sorted(dependencies.items()):
            capability_id = normalize_identifier(raw_capability_id)
            owner = merged_map.get(capability_id)
            if owner is None or owner.membership in {
                CapabilityMembership.PROHIBITED,
                CapabilityMembership.NOT_APPLICABLE,
            }:
                continue
            for raw_dependency in sorted(raw_dependencies):
                dependency = normalize_identifier(raw_dependency)
                dependency_entry = merged_map.get(dependency)
                if dependency_entry is None:
                    unresolved.append(f"{capability_id}->{dependency}:missing")
                elif dependency_entry.membership in {
                    CapabilityMembership.PROHIBITED,
                    CapabilityMembership.NOT_APPLICABLE,
                }:
                    unresolved.append(f"{capability_id}->{dependency}:{dependency_entry.membership.value}")

    return CapabilityResolution(
        entries=tuple(merged),
        conflicts=tuple(conflicts),
        unresolved_dependencies=tuple(sorted(set(unresolved))),
    )
