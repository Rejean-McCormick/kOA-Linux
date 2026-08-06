from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Iterable, Mapping, Sequence

from .capabilities import normalize_identifier


class ComponentMembership(StrEnum):
    REQUIRED = "required"
    OPTIONAL = "optional"
    CONDITIONAL = "conditional"
    PROHIBITED = "prohibited"
    EXTERNAL_INTEGRATION_ONLY = "external_integration_only"


@dataclass(frozen=True, slots=True)
class ComponentEntry:
    component_id: str
    membership: ComponentMembership
    conditions: tuple[str, ...] = ()
    sources: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "component_id": self.component_id,
            "membership": self.membership.value,
            "conditions": list(self.conditions),
            "sources": list(self.sources),
        }


@dataclass(frozen=True, slots=True)
class ComponentConflict:
    component_id: str
    memberships: tuple[ComponentMembership, ...]
    sources: tuple[str, ...]
    reason: str


@dataclass(frozen=True, slots=True)
class ComponentResolution:
    entries: tuple[ComponentEntry, ...]
    conflicts: tuple[ComponentConflict, ...] = ()

    def as_map(self) -> dict[str, ComponentEntry]:
        return {entry.component_id: entry for entry in self.entries}

    @property
    def valid(self) -> bool:
        return not self.conflicts


def _component_identifier(item: object) -> tuple[str, tuple[str, ...]]:
    if isinstance(item, str):
        return normalize_identifier(item), ()
    if item is None:
        raise ValueError("component member cannot be null")
    if not isinstance(item, Mapping):
        raise ValueError("component member must be a string or object")
    identifier = item.get("component_id", item.get("id"))
    if identifier is None and isinstance(item.get("component_ref"), str):
        identifier = item["component_ref"].rsplit("/", 1)[-1]
    if not isinstance(identifier, str):
        raise ValueError("component object requires component_id, id, or component_ref")
    raw_conditions = item.get("conditions")
    if raw_conditions is None and isinstance(item.get("condition"), str):
        raw_conditions = [item["condition"]]
    if raw_conditions is None:
        conditions: tuple[str, ...] = ()
    else:
        if isinstance(raw_conditions, str):
            raw_conditions = [raw_conditions]
        if not isinstance(raw_conditions, Sequence) or isinstance(raw_conditions, (bytes, bytearray)):
            raise ValueError("component conditions must be strings")
        normalized_conditions = []
        for condition in raw_conditions:
            if not isinstance(condition, str) or not condition.strip():
                raise ValueError("component conditions must be non-empty strings")
            normalized_conditions.append(condition.strip())
        conditions = tuple(sorted(set(normalized_conditions)))
    return normalize_identifier(identifier), conditions


def _entries_from_group(
    value: object,
    membership: ComponentMembership,
    source: str,
) -> list[ComponentEntry]:
    if value is None:
        return []
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise ValueError("component membership group must be an array")
    entries = []
    for item in value:
        if item is None:
            continue
        identifier, conditions = _component_identifier(item)
        entries.append(ComponentEntry(identifier, membership, conditions, (source,)))
    return entries


def extract_components(contract: Mapping[str, Any], source: str) -> tuple[ComponentEntry, ...]:
    if not isinstance(contract, Mapping):
        raise TypeError("profile contract must be a mapping")
    entries: list[ComponentEntry] = []

    grouped_sources = []
    for key in ("components", "component_membership"):
        value = contract.get(key)
        if isinstance(value, Mapping):
            grouped_sources.append(value)

    group_aliases = {
        "required": ComponentMembership.REQUIRED,
        "optional": ComponentMembership.OPTIONAL,
        "available_on_demand": ComponentMembership.OPTIONAL,
        "optional_isolated_workbenches": ComponentMembership.OPTIONAL,
        "conditional": ComponentMembership.CONDITIONAL,
        "prohibited": ComponentMembership.PROHIBITED,
        "excluded": ComponentMembership.PROHIBITED,
        "managed_node_dependencies": ComponentMembership.EXTERNAL_INTEGRATION_ONLY,
    }
    for grouped in grouped_sources:
        if any(key in grouped for key in group_aliases):
            for key, membership in group_aliases.items():
                entries.extend(_entries_from_group(grouped.get(key), membership, source))
        else:
            for component_id, details in grouped.items():
                if not isinstance(details, Mapping) or "state" not in details:
                    continue
                state = str(details["state"]).strip().lower()
                membership_aliases = {
                    "required": ComponentMembership.REQUIRED,
                    "optional": ComponentMembership.OPTIONAL,
                    "conditional": ComponentMembership.CONDITIONAL,
                    "prohibited": ComponentMembership.PROHIBITED,
                    "excluded": ComponentMembership.PROHIBITED,
                }
                if state not in membership_aliases:
                    raise ValueError(f"unsupported component state: {state!r}")
                raw_conditions = details.get("conditions", ())
                if isinstance(raw_conditions, str):
                    raw_conditions = [raw_conditions]
                if not isinstance(raw_conditions, Sequence):
                    raise ValueError("component conditions must be an array")
                conditions = tuple(sorted({str(item).strip() for item in raw_conditions if str(item).strip()}))
                entries.append(
                    ComponentEntry(
                        normalize_identifier(component_id),
                        membership_aliases[state],
                        conditions,
                        (source,),
                    )
                )

    selection = contract.get("component_selection")
    if isinstance(selection, Mapping):
        entries.extend(
            _entries_from_group(selection.get("required_components"), ComponentMembership.REQUIRED, source)
        )
        workbenches = selection.get("selectable_component_workbenches")
        if workbenches is not None:
            if not isinstance(workbenches, Sequence) or isinstance(workbenches, (str, bytes, bytearray)):
                raise ValueError("selectable_component_workbenches must be an array")
            for workbench in workbenches:
                if not isinstance(workbench, Mapping):
                    raise ValueError("workbench entry must be an object")
                component_ids = workbench.get("component_ids", ())
                entries.extend(_entries_from_group(component_ids, ComponentMembership.OPTIONAL, source))

    for key, membership in {
        "required_components": ComponentMembership.REQUIRED,
        "optional_components": ComponentMembership.OPTIONAL,
        "conditional_components": ComponentMembership.CONDITIONAL,
        "prohibited_components": ComponentMembership.PROHIBITED,
    }.items():
        entries.extend(_entries_from_group(contract.get(key), membership, source))

    policy = contract.get("component_policy")
    if isinstance(policy, Mapping):
        policy_groups = {
            "required_component_additions": ComponentMembership.REQUIRED,
            "required_component_ids": ComponentMembership.REQUIRED,
            "conditionally_required_components": ComponentMembership.CONDITIONAL,
            "optional_component_ids": ComponentMembership.OPTIONAL,
            "prohibited_component_ids": ComponentMembership.PROHIBITED,
        }
        for key, membership in policy_groups.items():
            entries.extend(_entries_from_group(policy.get(key), membership, source))

    return tuple(sorted(entries, key=lambda item: (item.component_id, item.membership.value, item.conditions)))


def _merge_memberships(memberships: set[ComponentMembership]) -> ComponentMembership | None:
    if ComponentMembership.REQUIRED in memberships and ComponentMembership.PROHIBITED in memberships:
        return None
    if ComponentMembership.PROHIBITED in memberships:
        return ComponentMembership.PROHIBITED
    if ComponentMembership.REQUIRED in memberships:
        return ComponentMembership.REQUIRED
    if ComponentMembership.CONDITIONAL in memberships:
        return ComponentMembership.CONDITIONAL
    if ComponentMembership.OPTIONAL in memberships:
        return ComponentMembership.OPTIONAL
    return ComponentMembership.EXTERNAL_INTEGRATION_ONLY


def merge_components(groups: Iterable[Iterable[ComponentEntry]]) -> ComponentResolution:
    collected: dict[str, list[ComponentEntry]] = {}
    for group in groups:
        for entry in group:
            collected.setdefault(entry.component_id, []).append(entry)

    merged: list[ComponentEntry] = []
    conflicts: list[ComponentConflict] = []
    for component_id in sorted(collected):
        candidates = collected[component_id]
        memberships = {candidate.membership for candidate in candidates}
        membership = _merge_memberships(memberships)
        sources = tuple(sorted({source for candidate in candidates for source in candidate.sources}))
        conditions = tuple(sorted({condition for candidate in candidates for condition in candidate.conditions}))
        if membership is None:
            conflicts.append(
                ComponentConflict(
                    component_id=component_id,
                    memberships=tuple(sorted(memberships, key=lambda item: item.value)),
                    sources=sources,
                    reason="required_and_prohibited",
                )
            )
            continue
        merged.append(ComponentEntry(component_id, membership, conditions, sources))

    return ComponentResolution(tuple(merged), tuple(conflicts))
