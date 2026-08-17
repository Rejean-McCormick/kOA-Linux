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


def _plain_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _plain_value(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_plain_value(item) for item in value]
    if isinstance(value, list):
        return [_plain_value(item) for item in value]
    return value


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
    """Component health binding.

    Canonical instances serialize to ``health-status.schema.json``.  The legacy
    constructor fields remain accepted temporarily so existing component code
    can migrate without changing its in-process health API in the same patch.
    """

    component_id: str
    observed_at: datetime
    schema_version: str = "1.0.0"

    # Canonical health-status fields.
    health_report_id: str | None = None
    component_contract_ref: str | None = None
    process_liveness: Mapping[str, Any] | None = None
    startup: Mapping[str, Any] | None = None
    overall_state: HealthState | None = None
    readiness: tuple[Mapping[str, Any], ...] = ()
    freshness: Mapping[str, Any] | None = None
    disclosure_class: str | None = None
    component_instance_id: str | None = None
    profile_refs: tuple[str, ...] = ()
    limitations: tuple[Mapping[str, Any], ...] = ()
    recovery_conditions: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()

    # Legacy compatibility surface.  These fields are never emitted by a
    # canonical instance.
    instance_id: str | None = None
    state: HealthState | None = None
    contract_version: str | None = None
    capabilities: tuple[CapabilityState, ...] = ()
    startup_complete: bool | None = None
    freshness_seconds: int | None = None
    reason_codes: tuple[str, ...] = ()
    active_artifact_refs: tuple[str, ...] = ()
    details: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    _canonical_mode: bool = field(init=False, repr=False, compare=False, default=False)

    SCHEMA_PATH = HEALTH_STATUS_SCHEMA_PATH

    def __post_init__(self) -> None:
        object.__setattr__(self, "component_id", _require_text(self.component_id, "component_id"))
        object.__setattr__(self, "observed_at", _parse_timestamp(self.observed_at, "observed_at"))
        object.__setattr__(
            self, "schema_version", _require_text(self.schema_version, "schema_version")
        )
        object.__setattr__(self, "reason_codes", _string_tuple(self.reason_codes, "reason_codes"))

        canonical_mode = any(
            value is not None
            for value in (
                self.health_report_id,
                self.component_contract_ref,
                self.process_liveness,
                self.startup,
                self.overall_state,
                self.freshness,
                self.disclosure_class,
            )
        ) or bool(self.readiness)
        object.__setattr__(self, "_canonical_mode", canonical_mode)

        if canonical_mode:
            self._validate_canonical()
        else:
            self._validate_legacy()

    def _validate_canonical(self) -> None:
        required_text = {
            "health_report_id": self.health_report_id,
            "component_contract_ref": self.component_contract_ref,
            "disclosure_class": self.disclosure_class,
        }
        missing = [name for name, value in required_text.items() if value is None]
        if self.process_liveness is None:
            missing.append("process_liveness")
        if self.startup is None:
            missing.append("startup")
        if self.overall_state is None:
            missing.append("overall_state")
        if not self.readiness:
            missing.append("readiness")
        if self.freshness is None:
            missing.append("freshness")
        if missing:
            raise InterfaceValidationError(
                "canonical health status missing fields: " + ", ".join(sorted(missing))
            )

        health_report_id = _require_text(self.health_report_id, "health_report_id")
        if not health_report_id.startswith("health:"):
            raise InterfaceValidationError("health_report_id must start with 'health:'")
        object.__setattr__(self, "health_report_id", health_report_id)
        object.__setattr__(
            self,
            "component_contract_ref",
            _require_text(self.component_contract_ref, "component_contract_ref"),
        )
        object.__setattr__(
            self,
            "component_instance_id",
            _optional_text(self.component_instance_id, "component_instance_id"),
        )
        object.__setattr__(self, "overall_state", _enum_value(HealthState, self.overall_state, "overall_state"))
        object.__setattr__(self, "state", self.overall_state)

        disclosure = _require_text(self.disclosure_class, "disclosure_class")
        allowed_disclosures = {
            "minimal_public",
            "authenticated_operational",
            "restricted_diagnostic",
            "machine_readable_local",
        }
        if disclosure not in allowed_disclosures:
            raise InterfaceValidationError("unsupported disclosure_class")
        object.__setattr__(self, "disclosure_class", disclosure)

        process_liveness = self._health_mapping(
            self.process_liveness,
            "process_liveness",
            required={"state", "observed_at", "reason_codes"},
        )
        liveness_state = process_liveness["state"]
        if liveness_state not in {"alive", "stopping", "failed"}:
            raise InterfaceValidationError("process_liveness.state is invalid")
        if liveness_state in {"stopping", "failed"} and not process_liveness["reason_codes"]:
            raise InterfaceValidationError(
                "non-alive process_liveness requires reason_codes"
            )
        object.__setattr__(self, "process_liveness", process_liveness)

        startup = self._health_mapping(
            self.startup,
            "startup",
            required={"state", "observed_at", "reason_codes"},
        )
        startup_state = _enum_value(HealthState, startup["state"], "startup.state")
        if startup_state is not HealthState.HEALTHY and not startup["reason_codes"]:
            raise InterfaceValidationError("non-healthy startup requires reason_codes")
        object.__setattr__(self, "startup", startup)
        object.__setattr__(self, "startup_complete", startup_state is HealthState.HEALTHY)

        readiness_items: list[Mapping[str, Any]] = []
        for item in self.readiness:
            if not isinstance(item, Mapping):
                raise InterfaceValidationError("readiness must contain objects")
            readiness_items.append(MappingProxyType(dict(item)))
        object.__setattr__(self, "readiness", tuple(readiness_items))

        freshness = self._health_mapping(
            self.freshness,
            "freshness",
            required={"source", "confidence", "staleness_state", "observed_at"},
        )
        if freshness["confidence"] not in {"direct", "derived", "reported", "unknown"}:
            raise InterfaceValidationError("freshness.confidence is invalid")
        if freshness["staleness_state"] not in {"current", "stale", "unknown"}:
            raise InterfaceValidationError("freshness.staleness_state is invalid")
        age_seconds = freshness.get("age_seconds")
        if age_seconds is not None and (
            not isinstance(age_seconds, int) or isinstance(age_seconds, bool) or age_seconds < 0
        ):
            raise InterfaceValidationError("freshness.age_seconds must be a non-negative integer")
        object.__setattr__(self, "freshness", freshness)
        object.__setattr__(self, "freshness_seconds", age_seconds if age_seconds is not None else 0)

        object.__setattr__(self, "profile_refs", _string_tuple(self.profile_refs, "profile_refs"))
        object.__setattr__(
            self,
            "recovery_conditions",
            _string_tuple(self.recovery_conditions, "recovery_conditions"),
        )
        object.__setattr__(self, "evidence_refs", _string_tuple(self.evidence_refs, "evidence_refs"))
        limitation_items: list[Mapping[str, Any]] = []
        for item in self.limitations:
            if not isinstance(item, Mapping):
                raise InterfaceValidationError("limitations must contain objects")
            limitation_items.append(MappingProxyType(dict(item)))
        object.__setattr__(self, "limitations", tuple(limitation_items))

        if liveness_state == "failed" and self.overall_state is not HealthState.FAILED:
            raise InterfaceValidationError(
                "failed process_liveness requires overall_state=failed"
            )
        if liveness_state == "stopping" and self.overall_state is not HealthState.STOPPING:
            raise InterfaceValidationError(
                "stopping process_liveness requires overall_state=stopping"
            )
        if self.overall_state is not HealthState.HEALTHY and not self.reason_codes:
            raise InterfaceValidationError("non-healthy overall_state requires reason_codes")
        if freshness["staleness_state"] == "stale" and self.overall_state is HealthState.HEALTHY:
            raise InterfaceValidationError("stale freshness cannot report overall_state=healthy")
        if freshness["staleness_state"] == "stale" and not self.reason_codes:
            raise InterfaceValidationError("stale freshness requires reason_codes")

        # Compatibility aliases for code that reads these attributes.
        if self.instance_id is None and self.component_instance_id is not None:
            object.__setattr__(self, "instance_id", self.component_instance_id)

    def _validate_legacy(self) -> None:
        required = {
            "instance_id": self.instance_id,
            "state": self.state,
            "contract_version": self.contract_version,
            "startup_complete": self.startup_complete,
            "freshness_seconds": self.freshness_seconds,
        }
        missing = [name for name, value in required.items() if value is None]
        if missing:
            raise InterfaceValidationError(
                "legacy health status missing fields: " + ", ".join(sorted(missing))
            )
        object.__setattr__(self, "instance_id", _require_text(self.instance_id, "instance_id"))
        object.__setattr__(self, "state", _enum_value(HealthState, self.state, "state"))
        object.__setattr__(
            self, "contract_version", _require_text(self.contract_version, "contract_version")
        )
        if not isinstance(self.capabilities, tuple):
            object.__setattr__(self, "capabilities", tuple(self.capabilities))
        if not self.capabilities or not all(
            isinstance(item, CapabilityState) for item in self.capabilities
        ):
            raise InterfaceValidationError("capabilities must contain CapabilityState values")
        if not isinstance(self.startup_complete, bool):
            _raise_boolean("startup_complete")
        if (
            not isinstance(self.freshness_seconds, int)
            or isinstance(self.freshness_seconds, bool)
            or self.freshness_seconds < 0
        ):
            raise InterfaceValidationError("freshness_seconds must be a non-negative integer")
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

    @staticmethod
    def _health_mapping(
        value: Mapping[str, Any] | None,
        field_name: str,
        *,
        required: set[str],
    ) -> Mapping[str, Any]:
        if not isinstance(value, Mapping):
            raise InterfaceValidationError(f"{field_name} must be an object")
        missing = sorted(required - set(value))
        if missing:
            raise InterfaceValidationError(
                f"{field_name} missing fields: {', '.join(missing)}"
            )
        return MappingProxyType(dict(value))

    def to_dict(self) -> dict[str, Any]:
        if self._canonical_mode:
            result: dict[str, Any] = {
                "schema_version": self.schema_version,
                "health_report_id": self.health_report_id,
                "component_id": self.component_id,
                "component_contract_ref": self.component_contract_ref,
                "process_liveness": _plain_value(self.process_liveness),
                "startup": _plain_value(self.startup),
                "overall_state": self.overall_state.value,
                "readiness": [_plain_value(item) for item in self.readiness],
                "freshness": _plain_value(self.freshness),
                "observed_at": _format_timestamp(self.observed_at),
                "reason_codes": list(self.reason_codes),
                "disclosure_class": self.disclosure_class,
            }
            if self.component_instance_id is not None:
                result["component_instance_id"] = self.component_instance_id
            if self.profile_refs:
                result["profile_refs"] = list(self.profile_refs)
            if self.limitations:
                result["limitations"] = [_plain_value(item) for item in self.limitations]
            if self.recovery_conditions:
                result["recovery_conditions"] = list(self.recovery_conditions)
            if self.evidence_refs:
                result["evidence_refs"] = list(self.evidence_refs)
            return result

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

        if "health_report_id" in data or "component_contract_ref" in data:
            allowed = {
                "schema_version",
                "health_report_id",
                "component_id",
                "component_instance_id",
                "component_contract_ref",
                "profile_refs",
                "process_liveness",
                "startup",
                "overall_state",
                "readiness",
                "limitations",
                "freshness",
                "observed_at",
                "reason_codes",
                "recovery_conditions",
                "evidence_refs",
                "disclosure_class",
            }
            _unexpected_fields(data, allowed)
            required = {
                "schema_version",
                "health_report_id",
                "component_id",
                "component_contract_ref",
                "process_liveness",
                "startup",
                "overall_state",
                "readiness",
                "freshness",
                "observed_at",
                "reason_codes",
                "disclosure_class",
            }
            missing = sorted(required - set(data))
            if missing:
                raise InterfaceValidationError(f"missing fields: {', '.join(missing)}")
            raw_readiness = data["readiness"]
            if isinstance(raw_readiness, str) or not isinstance(raw_readiness, (list, tuple)):
                raise InterfaceValidationError("readiness must be an array")
            raw_limitations = data.get("limitations", ())
            if isinstance(raw_limitations, str) or not isinstance(raw_limitations, (list, tuple)):
                raise InterfaceValidationError("limitations must be an array")
            return cls(
                component_id=data["component_id"],
                observed_at=data["observed_at"],
                schema_version=data["schema_version"],
                health_report_id=data["health_report_id"],
                component_instance_id=data.get("component_instance_id"),
                component_contract_ref=data["component_contract_ref"],
                profile_refs=_string_tuple(data.get("profile_refs"), "profile_refs"),
                process_liveness=data["process_liveness"],
                startup=data["startup"],
                overall_state=data["overall_state"],
                readiness=tuple(raw_readiness),
                limitations=tuple(raw_limitations),
                freshness=data["freshness"],
                reason_codes=_string_tuple(data.get("reason_codes"), "reason_codes"),
                recovery_conditions=_string_tuple(
                    data.get("recovery_conditions"), "recovery_conditions"
                ),
                evidence_refs=_string_tuple(data.get("evidence_refs"), "evidence_refs"),
                disclosure_class=data["disclosure_class"],
            )

        allowed = {
            "component_id",
            "instance_id",
            "state",
            "observed_at",
            "contract_version",
            "schema_version",
            "capabilities",
            "startup_complete",
            "freshness_seconds",
            "reason_codes",
            "active_artifact_refs",
            "details",
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
            observed_at=data["observed_at"],
            schema_version=data["schema_version"],
            instance_id=data["instance_id"],
            state=data["state"],
            contract_version=data["contract_version"],
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
