"""Health, readiness and capability-state bindings."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping

from .errors import (
    InterfaceValidationError,
    _enum_value,
    _format_timestamp,
    _freeze_mapping,
    _optional_text,
    _parse_timestamp,
    _require_text,
    _string_tuple,
    _unexpected_fields,
)

HEALTH_STATUS_SCHEMA_PATH = "interfaces/health/health-status.schema.json"
READINESS_SCHEMA_PATH = "interfaces/health/readiness.schema.json"
CAPABILITY_SNAPSHOT_SCHEMA_PATH = "interfaces/capabilities/capability-snapshot.schema.json"


class HealthState(StrEnum):
    STARTING = "starting"
    HEALTHY = "healthy"
    CONSTRAINED = "constrained"
    READ_ONLY = "read_only"
    ADVISORY_ONLY = "advisory_only"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    RECOVERING = "recovering"
    MAINTENANCE = "maintenance"
    STOPPING = "stopping"
    FAILED = "failed"


class AvailabilityState(StrEnum):
    AVAILABLE = "available"
    DEGRADED = "degraded"
    DEFERRED_ONLY = "deferred_only"
    BLOCKED = "blocked"
    UNAVAILABLE = "unavailable"


class CapabilityExecutionState(StrEnum):
    NOT_STARTED = "not_started"
    ACCEPTED = "accepted"
    QUEUED = "queued"
    RUNNING = "running"
    AWAITING_DEPENDENCY = "awaiting_dependency"
    AWAITING_AUTHORITY = "awaiting_authority"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"
    CONFLICTED = "conflicted"
    EXPIRED = "expired"


class AuthoritativeOutcome(StrEnum):
    NO_EFFECT = "no_effect"
    CANDIDATE_CREATED = "candidate_created"
    REQUEST_RECORDED = "request_recorded"
    CHANGE_COMMITTED = "change_committed"
    POLICY_DECISION_RECORDED = "policy_decision_recorded"
    EVIDENCE_RECORDED = "evidence_recorded"
    EXTERNAL_EFFECT_CONFIRMED = "external_effect_confirmed"
    ROLLED_BACK = "rolled_back"


class ReadinessClass(StrEnum):
    LOCAL_READ = "readiness.local_read"
    AUTHORITATIVE_WRITE = "readiness.authoritative_write"
    BACKGROUND_WORK = "readiness.background_work"
    PUBLICATION = "readiness.publication"
    ACTIVATION = "readiness.activation"
    RECOVERY = "readiness.recovery"


def _raise_boolean(field_name: str) -> bool:
    raise InterfaceValidationError(f"{field_name} must be a boolean")


@dataclass(frozen=True, slots=True)
class CapabilityState:
    capability_id: str
    health_state: HealthState
    availability_state: AvailabilityState
    execution_state: CapabilityExecutionState = CapabilityExecutionState.NOT_STARTED
    authoritative_outcome: AuthoritativeOutcome = AuthoritativeOutcome.NO_EFFECT
    authority_effect: str = "none"
    critical: bool = False
    usable_operations: tuple[str, ...] = ()
    denied_operations: tuple[str, ...] = ()
    dependency_states: Mapping[str, str] = field(default_factory=lambda: MappingProxyType({}))
    reason_codes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "capability_id", _require_text(self.capability_id, "capability_id")
        )
        object.__setattr__(
            self, "health_state", _enum_value(HealthState, self.health_state, "health_state")
        )
        object.__setattr__(
            self,
            "availability_state",
            _enum_value(AvailabilityState, self.availability_state, "availability_state"),
        )
        object.__setattr__(
            self,
            "execution_state",
            _enum_value(CapabilityExecutionState, self.execution_state, "execution_state"),
        )
        object.__setattr__(
            self,
            "authoritative_outcome",
            _enum_value(AuthoritativeOutcome, self.authoritative_outcome, "authoritative_outcome"),
        )
        object.__setattr__(
            self, "authority_effect", _require_text(self.authority_effect, "authority_effect")
        )
        object.__setattr__(
            self, "usable_operations", _string_tuple(self.usable_operations, "usable_operations")
        )
        object.__setattr__(
            self, "denied_operations", _string_tuple(self.denied_operations, "denied_operations")
        )
        object.__setattr__(
            self,
            "dependency_states",
            _freeze_mapping(self.dependency_states, "dependency_states"),
        )
        object.__setattr__(self, "reason_codes", _string_tuple(self.reason_codes, "reason_codes"))
        if self.availability_state is AvailabilityState.AVAILABLE and self.health_state not in {
            HealthState.HEALTHY,
            HealthState.CONSTRAINED,
        }:
            raise InterfaceValidationError(
                "availability_state=available requires healthy or constrained health_state"
            )
        if self.availability_state in {AvailabilityState.BLOCKED, AvailabilityState.UNAVAILABLE}:
            if not self.denied_operations:
                raise InterfaceValidationError(
                    "blocked or unavailable capabilities must identify denied_operations"
                )

    def to_dict(self) -> dict[str, Any]:
        return {
            "capability_id": self.capability_id,
            "health_state": self.health_state.value,
            "availability_state": self.availability_state.value,
            "execution_state": self.execution_state.value,
            "authoritative_outcome": self.authoritative_outcome.value,
            "authority_effect": self.authority_effect,
            "critical": self.critical,
            "usable_operations": list(self.usable_operations),
            "denied_operations": list(self.denied_operations),
            "dependency_states": dict(self.dependency_states),
            "reason_codes": list(self.reason_codes),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> CapabilityState:
        if not isinstance(data, Mapping):
            raise InterfaceValidationError("capability state must be an object")
        allowed = {
            "capability_id", "health_state", "availability_state", "execution_state",
            "authoritative_outcome", "authority_effect", "critical", "usable_operations",
            "denied_operations", "dependency_states", "reason_codes",
        }
        _unexpected_fields(data, allowed)
        required = {"capability_id", "health_state", "availability_state"}
        missing = sorted(required - set(data))
        if missing:
            raise InterfaceValidationError(f"missing fields: {', '.join(missing)}")
        return cls(
            capability_id=data["capability_id"],
            health_state=data["health_state"],
            availability_state=data["availability_state"],
            execution_state=data.get("execution_state", CapabilityExecutionState.NOT_STARTED),
            authoritative_outcome=data.get(
                "authoritative_outcome", AuthoritativeOutcome.NO_EFFECT
            ),
            authority_effect=data.get("authority_effect", "none"),
            critical=(
                data.get("critical", False)
                if isinstance(data.get("critical", False), bool)
                else _raise_boolean("critical")
            ),
            usable_operations=_string_tuple(data.get("usable_operations"), "usable_operations"),
            denied_operations=_string_tuple(data.get("denied_operations"), "denied_operations"),
            dependency_states=_freeze_mapping(data.get("dependency_states"), "dependency_states"),
            reason_codes=_string_tuple(data.get("reason_codes"), "reason_codes"),
        )


@dataclass(frozen=True, slots=True)
class HealthStatus:
    component_id: str
    instance_id: str
    state: HealthState
    observed_at: datetime
    contract_version: str
    schema_version: str
    capabilities: tuple[CapabilityState, ...]
    startup_complete: bool
    freshness_seconds: int
    reason_codes: tuple[str, ...] = ()
    active_artifact_refs: tuple[str, ...] = ()
    details: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    SCHEMA_PATH = HEALTH_STATUS_SCHEMA_PATH

    def __post_init__(self) -> None:
        object.__setattr__(self, "component_id", _require_text(self.component_id, "component_id"))
        object.__setattr__(self, "instance_id", _require_text(self.instance_id, "instance_id"))
        object.__setattr__(self, "state", _enum_value(HealthState, self.state, "state"))
        object.__setattr__(self, "observed_at", _parse_timestamp(self.observed_at, "observed_at"))
        object.__setattr__(
            self, "contract_version", _require_text(self.contract_version, "contract_version")
        )
        object.__setattr__(
            self, "schema_version", _require_text(self.schema_version, "schema_version")
        )
        if not isinstance(self.capabilities, tuple):
            object.__setattr__(self, "capabilities", tuple(self.capabilities))
        if not self.capabilities or not all(
            isinstance(item, CapabilityState) for item in self.capabilities
        ):
            raise InterfaceValidationError("capabilities must contain CapabilityState values")
        if not isinstance(self.freshness_seconds, int) or self.freshness_seconds < 0:
            raise InterfaceValidationError("freshness_seconds must be a non-negative integer")
        object.__setattr__(self, "reason_codes", _string_tuple(self.reason_codes, "reason_codes"))
        object.__setattr__(
            self,
            "active_artifact_refs",
            _string_tuple(self.active_artifact_refs, "active_artifact_refs"),
        )
        object.__setattr__(self, "details", _freeze_mapping(self.details, "details"))
        if self.state is HealthState.HEALTHY and any(
            capability.critical
            and capability.health_state
            not in {HealthState.HEALTHY, HealthState.CONSTRAINED}
            for capability in self.capabilities
        ):
            raise InterfaceValidationError(
                "aggregate health cannot hide an unhealthy critical capability"
            )
        if not self.startup_complete and self.state is HealthState.HEALTHY:
            raise InterfaceValidationError("healthy status requires startup_complete=true")

    def to_dict(self) -> dict[str, Any]:
        return {
            "component_id": self.component_id,
            "instance_id": self.instance_id,
            "state": self.state.value,
            "observed_at": _format_timestamp(self.observed_at),
            "contract_version": self.contract_version,
            "schema_version": self.schema_version,
            "capabilities": [item.to_dict() for item in self.capabilities],
            "startup_complete": self.startup_complete,
            "freshness_seconds": self.freshness_seconds,
            "reason_codes": list(self.reason_codes),
            "active_artifact_refs": list(self.active_artifact_refs),
            "details": dict(self.details),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> HealthStatus:
        if not isinstance(data, Mapping):
            raise InterfaceValidationError("health status must be an object")
        allowed = {
            "component_id", "instance_id", "state", "observed_at", "contract_version",
            "schema_version", "capabilities", "startup_complete", "freshness_seconds",
            "reason_codes", "active_artifact_refs", "details",
        }
        _unexpected_fields(data, allowed)
        required = allowed - {"reason_codes", "active_artifact_refs", "details"}
        missing = sorted(required - set(data))
        if missing:
            raise InterfaceValidationError(f"missing fields: {', '.join(missing)}")
        raw_capabilities = data["capabilities"]
        if isinstance(raw_capabilities, str) or not isinstance(raw_capabilities, (list, tuple)):
            raise InterfaceValidationError("capabilities must be an array")
        return cls(
            component_id=data["component_id"],
            instance_id=data["instance_id"],
            state=data["state"],
            observed_at=data["observed_at"],
            contract_version=data["contract_version"],
            schema_version=data["schema_version"],
            capabilities=tuple(CapabilityState.from_dict(item) for item in raw_capabilities),
            startup_complete=(
                data["startup_complete"]
                if isinstance(data["startup_complete"], bool)
                else _raise_boolean("startup_complete")
            ),
            freshness_seconds=data["freshness_seconds"],
            reason_codes=_string_tuple(data.get("reason_codes"), "reason_codes"),
            active_artifact_refs=_string_tuple(
                data.get("active_artifact_refs"), "active_artifact_refs"
            ),
            details=_freeze_mapping(data.get("details"), "details"),
        )


@dataclass(frozen=True, slots=True)
class Readiness:
    component_id: str
    readiness_class: ReadinessClass
    state: HealthState
    accepting_work: bool
    observed_at: datetime
    capability_id: str | None = None
    usable_operations: tuple[str, ...] = ()
    denied_operations: tuple[str, ...] = ()
    required_dependencies: Mapping[str, str] = field(
        default_factory=lambda: MappingProxyType({})
    )
    reason_codes: tuple[str, ...] = ()
    recovery_conditions: tuple[str, ...] = ()

    SCHEMA_PATH = READINESS_SCHEMA_PATH

    def __post_init__(self) -> None:
        object.__setattr__(self, "component_id", _require_text(self.component_id, "component_id"))
        object.__setattr__(
            self,
            "readiness_class",
            _enum_value(ReadinessClass, self.readiness_class, "readiness_class"),
        )
        object.__setattr__(self, "state", _enum_value(HealthState, self.state, "state"))
        object.__setattr__(self, "observed_at", _parse_timestamp(self.observed_at, "observed_at"))
        object.__setattr__(
            self, "capability_id", _optional_text(self.capability_id, "capability_id")
        )
        object.__setattr__(
            self, "usable_operations", _string_tuple(self.usable_operations, "usable_operations")
        )
        object.__setattr__(
            self, "denied_operations", _string_tuple(self.denied_operations, "denied_operations")
        )
        object.__setattr__(
            self,
            "required_dependencies",
            _freeze_mapping(self.required_dependencies, "required_dependencies"),
        )
        object.__setattr__(self, "reason_codes", _string_tuple(self.reason_codes, "reason_codes"))
        object.__setattr__(
            self,
            "recovery_conditions",
            _string_tuple(self.recovery_conditions, "recovery_conditions"),
        )
        safe_accepting_states = {
            HealthState.HEALTHY,
            HealthState.CONSTRAINED,
            HealthState.READ_ONLY,
            HealthState.DEGRADED,
        }
        if self.accepting_work and self.state not in safe_accepting_states:
            raise InterfaceValidationError(
                "accepting_work=true is invalid for the declared readiness state"
            )
        if self.accepting_work and not self.usable_operations:
            raise InterfaceValidationError("accepting readiness must identify usable_operations")
        if not self.accepting_work and not self.denied_operations:
            raise InterfaceValidationError(
                "non-accepting readiness must identify denied_operations"
            )

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "component_id": self.component_id,
            "readiness_class": self.readiness_class.value,
            "state": self.state.value,
            "accepting_work": self.accepting_work,
            "observed_at": _format_timestamp(self.observed_at),
            "usable_operations": list(self.usable_operations),
            "denied_operations": list(self.denied_operations),
            "required_dependencies": dict(self.required_dependencies),
            "reason_codes": list(self.reason_codes),
            "recovery_conditions": list(self.recovery_conditions),
        }
        if self.capability_id is not None:
            result["capability_id"] = self.capability_id
        return result

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Readiness:
        if not isinstance(data, Mapping):
            raise InterfaceValidationError("readiness must be an object")
        allowed = {
            "component_id", "readiness_class", "state", "accepting_work", "observed_at",
            "capability_id", "usable_operations", "denied_operations", "required_dependencies",
            "reason_codes", "recovery_conditions",
        }
        _unexpected_fields(data, allowed)
        required = {"component_id", "readiness_class", "state", "accepting_work", "observed_at"}
        missing = sorted(required - set(data))
        if missing:
            raise InterfaceValidationError(f"missing fields: {', '.join(missing)}")
        return cls(
            component_id=data["component_id"],
            readiness_class=data["readiness_class"],
            state=data["state"],
            accepting_work=(
                data["accepting_work"]
                if isinstance(data["accepting_work"], bool)
                else _raise_boolean("accepting_work")
            ),
            observed_at=data["observed_at"],
            capability_id=data.get("capability_id"),
            usable_operations=_string_tuple(data.get("usable_operations"), "usable_operations"),
            denied_operations=_string_tuple(data.get("denied_operations"), "denied_operations"),
            required_dependencies=_freeze_mapping(
                data.get("required_dependencies"), "required_dependencies"
            ),
            reason_codes=_string_tuple(data.get("reason_codes"), "reason_codes"),
            recovery_conditions=_string_tuple(
                data.get("recovery_conditions"), "recovery_conditions"
            ),
        )


@dataclass(frozen=True, slots=True)
class CapabilitySnapshot:
    snapshot_id: str
    component_id: str
    observed_at: datetime
    contract_version: str
    capabilities: tuple[CapabilityState, ...]
    profile_refs: tuple[str, ...] = ()

    SCHEMA_PATH = CAPABILITY_SNAPSHOT_SCHEMA_PATH

    def __post_init__(self) -> None:
        object.__setattr__(self, "snapshot_id", _require_text(self.snapshot_id, "snapshot_id"))
        object.__setattr__(self, "component_id", _require_text(self.component_id, "component_id"))
        object.__setattr__(self, "observed_at", _parse_timestamp(self.observed_at, "observed_at"))
        object.__setattr__(
            self, "contract_version", _require_text(self.contract_version, "contract_version")
        )
        if not isinstance(self.capabilities, tuple):
            object.__setattr__(self, "capabilities", tuple(self.capabilities))
        if not all(isinstance(item, CapabilityState) for item in self.capabilities):
            raise InterfaceValidationError("capabilities must contain CapabilityState values")
        identifiers = [item.capability_id for item in self.capabilities]
        if len(identifiers) != len(set(identifiers)):
            raise InterfaceValidationError("capability_id values must be unique in a snapshot")
        object.__setattr__(self, "profile_refs", _string_tuple(self.profile_refs, "profile_refs"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "component_id": self.component_id,
            "observed_at": _format_timestamp(self.observed_at),
            "contract_version": self.contract_version,
            "capabilities": [item.to_dict() for item in self.capabilities],
            "profile_refs": list(self.profile_refs),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> CapabilitySnapshot:
        if not isinstance(data, Mapping):
            raise InterfaceValidationError("capability snapshot must be an object")
        allowed = {
            "snapshot_id", "component_id", "observed_at", "contract_version",
            "capabilities", "profile_refs",
        }
        _unexpected_fields(data, allowed)
        required = allowed - {"profile_refs"}
        missing = sorted(required - set(data))
        if missing:
            raise InterfaceValidationError(f"missing fields: {', '.join(missing)}")
        raw = data["capabilities"]
        if isinstance(raw, str) or not isinstance(raw, (list, tuple)):
            raise InterfaceValidationError("capabilities must be an array")
        return cls(
            snapshot_id=data["snapshot_id"],
            component_id=data["component_id"],
            observed_at=data["observed_at"],
            contract_version=data["contract_version"],
            capabilities=tuple(CapabilityState.from_dict(item) for item in raw),
            profile_refs=_string_tuple(data.get("profile_refs"), "profile_refs"),
        )
