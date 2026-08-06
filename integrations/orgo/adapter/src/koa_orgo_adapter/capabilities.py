"""Declared capability projection for the Orgo integration."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Iterable, Mapping

from .client import OperationDeclaration


class CapabilityState(StrEnum):
    AVAILABLE = "available"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    DISABLED = "disabled"


@dataclass(frozen=True, slots=True)
class CapabilityDeclaration:
    capability_id: str
    operation_ids: tuple[str, ...]
    user_visible: bool
    offline_state: CapabilityState
    removal_state: CapabilityState

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "CapabilityDeclaration":
        required = {"capability_id", "operation_ids", "user_visible", "offline_state", "removal_state"}
        missing = required - set(value)
        unknown = set(value) - required
        if missing or unknown:
            raise ValueError(f"invalid capability declaration; missing={sorted(missing)} unknown={sorted(unknown)}")
        capability_id = _non_empty(value["capability_id"], "capability_id")
        raw_operations = value["operation_ids"]
        if not isinstance(raw_operations, list) or not raw_operations:
            raise ValueError("operation_ids must be a non-empty list")
        operations = tuple(_non_empty(item, "operation_id") for item in raw_operations)
        if len(set(operations)) != len(operations):
            raise ValueError("operation_ids must be unique")
        if not isinstance(value["user_visible"], bool):
            raise ValueError("user_visible must be boolean")
        return cls(
            capability_id=capability_id,
            operation_ids=operations,
            user_visible=value["user_visible"],
            offline_state=CapabilityState(str(value["offline_state"])),
            removal_state=CapabilityState(str(value["removal_state"])),
        )


@dataclass(frozen=True, slots=True)
class CapabilityStatus:
    capability_id: str
    state: CapabilityState
    reason_code: str
    operation_ids: tuple[str, ...]
    user_visible: bool
    authoritative_success_prohibited: bool = True
    substitute_capability_id: None = None


class CapabilityRegistry:
    def __init__(
        self,
        *,
        declarations: Iterable[CapabilityDeclaration],
        operations: Mapping[str, OperationDeclaration],
    ) -> None:
        indexed: dict[str, CapabilityDeclaration] = {}
        declared_operations = set(operations)
        assigned: set[str] = set()
        for declaration in declarations:
            if declaration.capability_id in indexed:
                raise ValueError(f"duplicate capability_id: {declaration.capability_id}")
            missing = set(declaration.operation_ids) - declared_operations
            if missing:
                raise ValueError(f"capability references undeclared operations: {sorted(missing)}")
            for operation_id in declaration.operation_ids:
                if operations[operation_id].capability_id != declaration.capability_id:
                    raise ValueError(f"operation {operation_id} belongs to a different capability")
                if operation_id in assigned:
                    raise ValueError(f"operation assigned more than once: {operation_id}")
                assigned.add(operation_id)
            indexed[declaration.capability_id] = declaration
        if assigned != declared_operations:
            raise ValueError(f"operations without capability: {sorted(declared_operations - assigned)}")
        self._declarations = MappingProxyType(indexed)

    @property
    def declarations(self) -> Mapping[str, CapabilityDeclaration]:
        return self._declarations

    def snapshot(
        self,
        *,
        integration_enabled: bool,
        health_state: str,
        disabled_capabilities: Iterable[str] = (),
        boundary_condition: str = "online",
    ) -> tuple[CapabilityStatus, ...]:
        if boundary_condition not in {"online", "offline", "removed"}:
            raise ValueError("boundary_condition must be online, offline, or removed")
        disabled = set(disabled_capabilities)
        unknown = disabled - set(self._declarations)
        if unknown:
            raise ValueError(f"unknown disabled capabilities: {sorted(unknown)}")
        result: list[CapabilityStatus] = []
        for capability_id in sorted(self._declarations):
            declaration = self._declarations[capability_id]
            if not integration_enabled or capability_id in disabled:
                state = CapabilityState.DISABLED
                reason = "integration_disabled" if not integration_enabled else "capability_disabled"
            elif boundary_condition == "removed":
                state = declaration.removal_state
                reason = "orgo_removed"
            elif boundary_condition == "offline":
                state = declaration.offline_state
                reason = "orgo_offline"
            elif health_state == "healthy":
                state = CapabilityState.AVAILABLE
                reason = "orgo_available"
            elif health_state == "degraded":
                state = CapabilityState.DEGRADED
                reason = "orgo_degraded"
            else:
                state = CapabilityState.UNAVAILABLE
                reason = "orgo_unavailable"
            result.append(
                CapabilityStatus(
                    capability_id=capability_id,
                    state=state,
                    reason_code=reason,
                    operation_ids=declaration.operation_ids,
                    user_visible=declaration.user_visible,
                )
            )
        return tuple(result)


def _non_empty(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value
