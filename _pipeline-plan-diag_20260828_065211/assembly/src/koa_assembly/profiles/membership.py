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


class SubsystemMembership(StrEnum):
    REQUIRED = "required"
    OPTIONAL = "optional"
    CONDITIONAL = "conditional"
    PROHIBITED = "prohibited"


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
class SubsystemEntry:
    subsystem_id: str
    membership: SubsystemMembership
    conditions: tuple[str, ...] = ()
    sources: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "subsystem_id": self.subsystem_id,
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
class SubsystemConflict:
    subsystem_id: str
    memberships: tuple[SubsystemMembership, ...]
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


@dataclass(frozen=True, slots=True)
class SubsystemResolution:
    entries: tuple[SubsystemEntry, ...]
    conflicts: tuple[SubsystemConflict, ...] = ()

    def as_map(self) -> dict[str, SubsystemEntry]:
        return {entry.subsystem_id: entry for entry in self.entries}

    @property
    def valid(self) -> bool:
        return not self.conflicts


def _conditions(item: Mapping[str, object], *, subject: str) -> tuple[str, ...]:
    raw_conditions = item.get("conditions")
    if raw_conditions is None and isinstance(item.get("condition"), str):
        raw_conditions = [item["condition"]]
    if raw_conditions is None:
        return ()
    if isinstance(raw_conditions, str):
        raw_conditions = [raw_conditions]
    if not isinstance(raw_conditions, Sequence) or isinstance(raw_conditions, (bytes, bytearray)):
        raise ValueError(f"{subject} conditions must be strings")
    normalized = []
    for condition in raw_conditions:
        if not isinstance(condition, str) or not condition.strip():
            raise ValueError(f"{subject} conditions must be non-empty strings")
        normalized.append(condition.strip())
    return tuple(sorted(set(normalized)))


def _identifier(item: object, *, kind: str) -> tuple[str, tuple[str, ...]]:
    if isinstance(item, str):
        return normalize_identifier(item), ()
    if item is None:
        raise ValueError(f"{kind} member cannot be null")
    if not isinstance(item, Mapping):
        raise ValueError(f"{kind} member must be a string or object")
    id_key = f"{kind}_id"
    ref_key = f"{kind}_ref"
    identifier = item.get(id_key, item.get("id"))
    if identifier is None and isinstance(item.get(ref_key), str):
        identifier = str(item[ref_key]).rsplit("/", 1)[-1]
    if not isinstance(identifier, str):
        raise ValueError(f"{kind} object requires {id_key}, id, or {ref_key}")
    return normalize_identifier(identifier), _conditions(item, subject=kind)


def _subsystem_contract_ref(item: object) -> str | None:
    if not isinstance(item, Mapping):
        return None
    for key in ("subsystem_ref", "contract_ref", "component_ref"):
        value = item.get(key)
        if isinstance(value, str) and ("/subsystems/" in value or value.endswith(".subsystem.json")):
            return value
    return None


def _subsystem_id_from_ref(ref: str) -> str:
    tail = ref.split("#", 1)[0].rsplit("/", 1)[-1]
    if tail.endswith(".subsystem.json"):
        tail = tail[: -len(".subsystem.json")]
    return normalize_identifier(tail)


def _component_entries(value: object, membership: ComponentMembership, source: str) -> list[ComponentEntry]:
    if value is None:
        return []
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise ValueError("component membership group must be an array")
    entries = []
    for item in value:
        if item is None:
            continue
        if _subsystem_contract_ref(item) is not None:
            continue
        identifier, conditions = _identifier(item, kind="component")
        entries.append(ComponentEntry(identifier, membership, conditions, (source,)))
    return entries


def _subsystem_entries(value: object, membership: SubsystemMembership, source: str) -> list[SubsystemEntry]:
    if value is None:
        return []
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise ValueError("subsystem membership group must be an array")
    entries = []
    for item in value:
        if item is None:
            continue
        identifier, conditions = _identifier(item, kind="subsystem")
        entries.append(SubsystemEntry(identifier, membership, conditions, (source,)))
    return entries


def extract_components(contract: Mapping[str, Any], source: str) -> tuple[ComponentEntry, ...]:
    if not isinstance(contract, Mapping):
        raise TypeError("profile contract must be a mapping")
    entries: list[ComponentEntry] = []
    grouped_sources = [
        value for key in ("components", "component_membership")
        if isinstance((value := contract.get(key)), Mapping)
    ]
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
    state_aliases = {
        "required": ComponentMembership.REQUIRED,
        "optional": ComponentMembership.OPTIONAL,
        "conditional": ComponentMembership.CONDITIONAL,
        "prohibited": ComponentMembership.PROHIBITED,
        "excluded": ComponentMembership.PROHIBITED,
    }
    for grouped in grouped_sources:
        if any(key in grouped for key in group_aliases):
            for key, membership in group_aliases.items():
                entries.extend(_component_entries(grouped.get(key), membership, source))
        else:
            for component_id, details in grouped.items():
                if not isinstance(details, Mapping) or "state" not in details:
                    continue
                state = str(details["state"]).strip().lower()
                if state not in state_aliases:
                    raise ValueError(f"unsupported component state: {state!r}")
                conditions = _conditions(details, subject="component")
                entries.append(ComponentEntry(normalize_identifier(component_id), state_aliases[state], conditions, (source,)))

    selection = contract.get("component_selection")
    if isinstance(selection, Mapping):
        entries.extend(_component_entries(selection.get("required_components"), ComponentMembership.REQUIRED, source))
        workbenches = selection.get("selectable_component_workbenches")
        if workbenches is not None:
            if not isinstance(workbenches, Sequence) or isinstance(workbenches, (str, bytes, bytearray)):
                raise ValueError("selectable_component_workbenches must be an array")
            for workbench in workbenches:
                if not isinstance(workbench, Mapping):
                    raise ValueError("workbench entry must be an object")
                entries.extend(_component_entries(workbench.get("component_ids", ()), ComponentMembership.OPTIONAL, source))

    for key, membership in {
        "required_components": ComponentMembership.REQUIRED,
        "optional_components": ComponentMembership.OPTIONAL,
        "conditional_components": ComponentMembership.CONDITIONAL,
        "prohibited_components": ComponentMembership.PROHIBITED,
    }.items():
        entries.extend(_component_entries(contract.get(key), membership, source))

    policy = contract.get("component_policy")
    if isinstance(policy, Mapping):
        for key, membership in {
            "required_component_additions": ComponentMembership.REQUIRED,
            "required_component_ids": ComponentMembership.REQUIRED,
            "conditionally_required_components": ComponentMembership.CONDITIONAL,
            "optional_component_ids": ComponentMembership.OPTIONAL,
            "prohibited_component_ids": ComponentMembership.PROHIBITED,
        }.items():
            entries.extend(_component_entries(policy.get(key), membership, source))

    return tuple(sorted(entries, key=lambda item: (item.component_id, item.membership.value, item.conditions)))


def extract_subsystems(contract: Mapping[str, Any], source: str) -> tuple[SubsystemEntry, ...]:
    if not isinstance(contract, Mapping):
        raise TypeError("profile contract must be a mapping")
    entries: list[SubsystemEntry] = []
    grouped_sources = [
        value for key in ("subsystems", "subsystem_membership", "integrated_subsystems")
        if isinstance((value := contract.get(key)), Mapping)
    ]
    aliases = {
        "required": SubsystemMembership.REQUIRED,
        "optional": SubsystemMembership.OPTIONAL,
        "available_on_demand": SubsystemMembership.OPTIONAL,
        "conditional": SubsystemMembership.CONDITIONAL,
        "prohibited": SubsystemMembership.PROHIBITED,
        "excluded": SubsystemMembership.PROHIBITED,
    }
    for grouped in grouped_sources:
        if any(key in grouped for key in aliases):
            for key, membership in aliases.items():
                entries.extend(_subsystem_entries(grouped.get(key), membership, source))
        else:
            for subsystem_id, details in grouped.items():
                if not isinstance(details, Mapping) or "state" not in details:
                    continue
                state = str(details["state"]).strip().lower()
                if state not in {k: v for k, v in aliases.items() if k != "available_on_demand"}:
                    raise ValueError(f"unsupported subsystem state: {state!r}")
                entries.append(SubsystemEntry(normalize_identifier(subsystem_id), aliases[state], _conditions(details, subject="subsystem"), (source,)))
    for key, membership in {
        "required_subsystems": SubsystemMembership.REQUIRED,
        "optional_subsystems": SubsystemMembership.OPTIONAL,
        "conditional_subsystems": SubsystemMembership.CONDITIONAL,
        "prohibited_subsystems": SubsystemMembership.PROHIBITED,
    }.items():
        entries.extend(_subsystem_entries(contract.get(key), membership, source))

    # Existing profile contracts may still place independently owned systems inside
    # component-shaped groups while pointing at subsystem contracts. Classify them
    # by the referenced contract, not by the container name.
    for container_key in ("components", "component_membership"):
        grouped = contract.get(container_key)
        if not isinstance(grouped, Mapping):
            continue
        for group_key, membership in {
            "required": SubsystemMembership.REQUIRED,
            "optional": SubsystemMembership.OPTIONAL,
            "available_on_demand": SubsystemMembership.OPTIONAL,
            "conditional": SubsystemMembership.CONDITIONAL,
            "prohibited": SubsystemMembership.PROHIBITED,
            "excluded": SubsystemMembership.PROHIBITED,
        }.items():
            values = grouped.get(group_key)
            if not isinstance(values, Sequence) or isinstance(values, (str, bytes, bytearray)):
                continue
            for item in values:
                ref = _subsystem_contract_ref(item)
                if ref is None:
                    continue
                if isinstance(item, Mapping) and isinstance(item.get("component_id"), str):
                    subsystem_id = normalize_identifier(str(item["component_id"]).replace("_runtime", ""))
                else:
                    subsystem_id = _subsystem_id_from_ref(ref)
                entries.append(SubsystemEntry(subsystem_id, membership, _conditions(item, subject="subsystem") if isinstance(item, Mapping) else (), (source,)))

    selection = contract.get("component_selection")
    if isinstance(selection, Mapping):
        workbenches = selection.get("selectable_component_workbenches")
        if isinstance(workbenches, Sequence) and not isinstance(workbenches, (str, bytes, bytearray)):
            for workbench in workbenches:
                if not isinstance(workbench, Mapping):
                    continue
                ids = workbench.get("component_ids")
                refs = workbench.get("contract_refs")
                if not isinstance(ids, Sequence) or isinstance(ids, (str, bytes, bytearray)):
                    continue
                if not isinstance(refs, Sequence) or isinstance(refs, (str, bytes, bytearray)):
                    continue
                if len(ids) != len(refs):
                    continue
                for raw_id, raw_ref in zip(ids, refs):
                    if isinstance(raw_id, str) and isinstance(raw_ref, str) and ("/subsystems/" in raw_ref or raw_ref.endswith(".subsystem.json")):
                        subsystem_id = normalize_identifier(raw_id.replace("_runtime", ""))
                        entries.append(SubsystemEntry(subsystem_id, SubsystemMembership.OPTIONAL, (), (source,)))

    deduped = {(entry.subsystem_id, entry.membership, entry.conditions, entry.sources): entry for entry in entries}
    return tuple(sorted(deduped.values(), key=lambda item: (item.subsystem_id, item.membership.value, item.conditions)))


def _merge_component_memberships(memberships: set[ComponentMembership]) -> ComponentMembership | None:
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


def _merge_subsystem_memberships(memberships: set[SubsystemMembership]) -> SubsystemMembership | None:
    if SubsystemMembership.REQUIRED in memberships and SubsystemMembership.PROHIBITED in memberships:
        return None
    if SubsystemMembership.PROHIBITED in memberships:
        return SubsystemMembership.PROHIBITED
    if SubsystemMembership.REQUIRED in memberships:
        return SubsystemMembership.REQUIRED
    if SubsystemMembership.CONDITIONAL in memberships:
        return SubsystemMembership.CONDITIONAL
    return SubsystemMembership.OPTIONAL


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
        membership = _merge_component_memberships(memberships)
        sources = tuple(sorted({source for candidate in candidates for source in candidate.sources}))
        conditions = tuple(sorted({condition for candidate in candidates for condition in candidate.conditions}))
        if membership is None:
            conflicts.append(ComponentConflict(component_id, tuple(sorted(memberships, key=lambda item: item.value)), sources, "required_and_prohibited"))
        else:
            merged.append(ComponentEntry(component_id, membership, conditions, sources))
    return ComponentResolution(tuple(merged), tuple(conflicts))


def merge_subsystems(groups: Iterable[Iterable[SubsystemEntry]]) -> SubsystemResolution:
    collected: dict[str, list[SubsystemEntry]] = {}
    for group in groups:
        for entry in group:
            collected.setdefault(entry.subsystem_id, []).append(entry)
    merged: list[SubsystemEntry] = []
    conflicts: list[SubsystemConflict] = []
    for subsystem_id in sorted(collected):
        candidates = collected[subsystem_id]
        memberships = {candidate.membership for candidate in candidates}
        membership = _merge_subsystem_memberships(memberships)
        sources = tuple(sorted({source for candidate in candidates for source in candidate.sources}))
        conditions = tuple(sorted({condition for candidate in candidates for condition in candidate.conditions}))
        if membership is None:
            conflicts.append(SubsystemConflict(subsystem_id, tuple(sorted(memberships, key=lambda item: item.value)), sources, "required_and_prohibited"))
        else:
            merged.append(SubsystemEntry(subsystem_id, membership, conditions, sources))
    return SubsystemResolution(tuple(merged), tuple(conflicts))
