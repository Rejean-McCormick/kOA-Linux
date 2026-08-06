"""Declarative capability projection for the Konnaxion boundary."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import re
from types import MappingProxyType
from typing import Iterable, Mapping


class DependencyState(StrEnum):
    AVAILABLE = "available"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"
    INCOMPATIBLE = "incompatible"


class CapabilityState(StrEnum):
    AVAILABLE = "available"
    DEGRADED = "degraded"
    DEFERRED = "deferred"
    UNAVAILABLE = "unavailable"
    BLOCKED = "blocked"


class FailureMode(StrEnum):
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    UNAVAILABLE = "unavailable"


_ID = re.compile(r"^[a-z][a-z0-9_.:-]{2,127}$")
_ALLOWED_DEPENDENCIES = frozenset(
    {
        "audit_broker",
        "boundary_contract",
        "governance_policy_runtime",
        "identity_and_trust",
        "konnaxion",
        "official_documentation_alignment",
        "publication_gateway",
        "resource_governor",
    }
)


@dataclass(frozen=True, slots=True)
class CapabilityDeclaration:
    """A boundary-owned declaration; never an invented subsystem catalog."""

    capability_id: str
    required_dependencies: tuple[str, ...]
    optional_dependencies: tuple[str, ...] = ()
    failure_mode: FailureMode = FailureMode.UNAVAILABLE
    user_visible: bool = False

    def __post_init__(self) -> None:
        _identifier("capability_id", self.capability_id)
        required = _dependencies("required_dependencies", self.required_dependencies, allow_empty=False)
        optional = _dependencies("optional_dependencies", self.optional_dependencies, allow_empty=True)
        if set(required) & set(optional):
            raise ValueError("a dependency cannot be both required and optional")
        object.__setattr__(self, "required_dependencies", required)
        object.__setattr__(self, "optional_dependencies", optional)


@dataclass(frozen=True, slots=True)
class CapabilitySnapshot:
    capability_id: str
    state: CapabilityState
    reasons: tuple[str, ...]
    user_visible: bool

    @property
    def usable(self) -> bool:
        return self.state in {CapabilityState.AVAILABLE, CapabilityState.DEGRADED}


class CapabilityCatalog:
    """Resolve declared capabilities from observed dependency states."""

    def __init__(self, declarations: Iterable[CapabilityDeclaration]) -> None:
        by_id: dict[str, CapabilityDeclaration] = {}
        for declaration in declarations:
            if declaration.capability_id in by_id:
                raise ValueError(f"duplicate capability declaration: {declaration.capability_id}")
            by_id[declaration.capability_id] = declaration
        if not by_id:
            raise ValueError("at least one declared capability is required")
        self._declarations = MappingProxyType(dict(sorted(by_id.items())))

    @property
    def declarations(self) -> Mapping[str, CapabilityDeclaration]:
        return self._declarations

    def resolve(self, observations: Mapping[str, DependencyState]) -> tuple[CapabilitySnapshot, ...]:
        unknown = set(observations) - _ALLOWED_DEPENDENCIES
        if unknown:
            raise ValueError(f"undeclared dependencies: {sorted(unknown)!r}")
        snapshots = [self._resolve_one(item, observations) for item in self._declarations.values()]
        return tuple(snapshots)

    def snapshot_for(
        self, capability_id: str, observations: Mapping[str, DependencyState]
    ) -> CapabilitySnapshot:
        try:
            declaration = self._declarations[capability_id]
        except KeyError as exc:
            raise KeyError(f"undeclared capability: {capability_id}") from exc
        return self._resolve_one(declaration, observations)

    @staticmethod
    def _resolve_one(
        declaration: CapabilityDeclaration, observations: Mapping[str, DependencyState]
    ) -> CapabilitySnapshot:
        required = [(dep, observations.get(dep, DependencyState.UNKNOWN)) for dep in declaration.required_dependencies]
        optional = [(dep, observations.get(dep, DependencyState.UNKNOWN)) for dep in declaration.optional_dependencies]
        reasons: list[str] = []

        authority_unknown = [dep for dep, state in required if state in {DependencyState.UNKNOWN, DependencyState.INCOMPATIBLE}]
        unavailable = [dep for dep, state in required if state is DependencyState.UNAVAILABLE]
        degraded = [dep for dep, state in required + optional if state is DependencyState.DEGRADED]
        optional_missing = [dep for dep, state in optional if state in {DependencyState.UNAVAILABLE, DependencyState.UNKNOWN, DependencyState.INCOMPATIBLE}]

        if authority_unknown:
            state = CapabilityState.BLOCKED
            reasons.extend(f"{dep}:{observations.get(dep, DependencyState.UNKNOWN).value}" for dep in authority_unknown)
        elif unavailable:
            state = CapabilityState(declaration.failure_mode.value)
            reasons.extend(f"{dep}:unavailable" for dep in unavailable)
        elif degraded or optional_missing:
            state = CapabilityState.DEGRADED
            reasons.extend(f"{dep}:{observations.get(dep, DependencyState.UNKNOWN).value}" for dep in degraded + optional_missing)
        else:
            state = CapabilityState.AVAILABLE

        return CapabilitySnapshot(
            capability_id=declaration.capability_id,
            state=state,
            reasons=tuple(sorted(set(reasons))),
            user_visible=declaration.user_visible,
        )


def _identifier(name: str, value: str) -> str:
    if not isinstance(value, str) or not _ID.fullmatch(value):
        raise ValueError(f"{name} must be a stable lowercase identifier")
    return value


def _dependencies(name: str, values: Iterable[str], *, allow_empty: bool) -> tuple[str, ...]:
    result = tuple(sorted(set(values)))
    if not result and not allow_empty:
        raise ValueError(f"{name} must not be empty")
    invalid = [item for item in result if item not in _ALLOWED_DEPENDENCIES]
    if invalid:
        raise ValueError(f"{name} contains undeclared dependencies: {invalid!r}")
    return result
