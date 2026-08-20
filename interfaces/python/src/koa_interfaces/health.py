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
    """Capability state used by legacy health output and canonical snapshots.

    The historical health surface is retained for component-local callers.  A
    capability can participate in ``CapabilitySnapshot`` only when the
    canonical observation metadata is also present; snapshot serialization
    never emits the legacy health-only fields.
    """

    capability_id: str
    health_state: HealthState | None
    availability_state: AvailabilityState
    execution_state: CapabilityExecutionState = CapabilityExecutionState.NOT_STARTED
    authoritative_outcome: AuthoritativeOutcome = AuthoritativeOutcome.NO_EFFECT
    authority_effect: str = "none"
    critical: bool = False
    usable_operations: tuple[str, ...] = ()
    denied_operations: tuple[str, ...] = ()
    dependency_states: Mapping[str, str] = field(default_factory=lambda: MappingProxyType({}))
    reason_codes: tuple[str, ...] = ()

    # Canonical capability-snapshot observation metadata.  These values are
    # optional on the legacy health surface but mandatory when a snapshot is
    # serialized.
    capability_ref: str | None = None
    owner_component_ref: str | None = None
    capability_class: str | None = None
    offline_behavior: str | None = None
    observed_at: datetime | None = None
    state_entered_at: datetime | None = None
    dependency_observations: tuple[Mapping[str, Any], ...] = ()
    degradation: Mapping[str, Any] | None = None
    result_ref: str | None = None
    evidence_refs: tuple[str, ...] = ()
    receipt_refs: tuple[str, ...] = ()

    _CAPABILITY_CLASSES = frozenset({
        "authoritative_state",
        "deterministic_processing",
        "identity_and_trust",
        "governance_and_policy",
        "resource_governance",
        "navigation_and_interaction",
        "ingestion_and_transfer",
        "publication_and_disclosure",
        "audit_and_recourse",
        "artifact_lifecycle",
        "developer_workbench",
        "external_adapter",
    })
    _AUTHORITY_EFFECTS = frozenset({
        "none",
        "read_authoritative",
        "candidate_output",
        "request_authoritative_change",
        "authoritative_change",
        "transport_only",
        "policy_decision",
        "evidence_record",
    })
    _OFFLINE_BEHAVIORS = frozenset({
        "continuous", "degraded", "deferred", "unavailable", "offline_transfer"
    })
    _DEPENDENCY_TYPES = frozenset({
        "capability", "component", "authority", "data", "artifact", "resource",
        "profile", "integration", "environment",
    })
    _DEPENDENCY_REQUIREMENTS = frozenset({"hard", "conditional", "optional"})
    _DEPENDENCY_STATES = frozenset({
        "satisfied", "degraded", "deferred", "blocked", "unavailable"
    })

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "capability_id", _require_text(self.capability_id, "capability_id")
        )
        if self.health_state is not None:
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
        if not isinstance(self.critical, bool):
            _raise_boolean("critical")
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

        for field_name in (
            "capability_ref", "owner_component_ref", "capability_class", "offline_behavior",
            "result_ref",
        ):
            object.__setattr__(
                self, field_name, _optional_text(getattr(self, field_name), field_name)
            )
        if self.observed_at is not None:
            object.__setattr__(
                self, "observed_at", _parse_timestamp(self.observed_at, "observed_at")
            )
        if self.state_entered_at is not None:
            object.__setattr__(
                self, "state_entered_at", _parse_timestamp(self.state_entered_at, "state_entered_at")
            )
        object.__setattr__(
            self,
            "dependency_observations",
            self._mapping_tuple(self.dependency_observations, "dependency_observations"),
        )
        if self.degradation is not None:
            if not isinstance(self.degradation, Mapping):
                raise InterfaceValidationError("degradation must be an object")
            object.__setattr__(self, "degradation", MappingProxyType(dict(self.degradation)))
        object.__setattr__(self, "evidence_refs", _string_tuple(self.evidence_refs, "evidence_refs"))
        object.__setattr__(self, "receipt_refs", _string_tuple(self.receipt_refs, "receipt_refs"))

        canonical_metadata_present = any(
            value is not None
            for value in (
                self.capability_ref,
                self.owner_component_ref,
                self.capability_class,
                self.offline_behavior,
                self.observed_at,
            )
        )
        if (
            not canonical_metadata_present
            and self.availability_state is AvailabilityState.AVAILABLE
            and self.health_state not in {HealthState.HEALTHY, HealthState.CONSTRAINED}
        ):
            raise InterfaceValidationError(
                "availability_state=available requires healthy or constrained health_state"
            )
        if (
            not canonical_metadata_present
            and self.availability_state in {AvailabilityState.BLOCKED, AvailabilityState.UNAVAILABLE}
            and not self.denied_operations
        ):
            raise InterfaceValidationError(
                "blocked or unavailable capabilities must identify denied_operations"
            )

    @staticmethod
    def _mapping_tuple(value: Any, field_name: str) -> tuple[Mapping[str, Any], ...]:
        if value is None:
            return ()
        if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, (list, tuple)):
            raise InterfaceValidationError(f"{field_name} must be an array")
        result: list[Mapping[str, Any]] = []
        for index, item in enumerate(value):
            if not isinstance(item, Mapping):
                raise InterfaceValidationError(f"{field_name}[{index}] must be an object")
            result.append(MappingProxyType(dict(item)))
        return tuple(result)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the retained legacy health capability shape."""
        if self.health_state is None:
            raise InterfaceValidationError(
                "canonical snapshot capability has no legacy health_state serialization"
            )
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

    def _validate_snapshot_metadata(self) -> None:
        required_text = {
            "capability_ref": self.capability_ref,
            "owner_component_ref": self.owner_component_ref,
            "capability_class": self.capability_class,
            "offline_behavior": self.offline_behavior,
        }
        missing = [name for name, value in required_text.items() if value is None]
        if self.observed_at is None:
            missing.append("observed_at")
        if missing:
            raise InterfaceValidationError(
                "capability snapshot observation missing fields: " + ", ".join(sorted(missing))
            )
        if self.capability_class not in self._CAPABILITY_CLASSES:
            raise InterfaceValidationError("capability_class is not supported")
        if self.authority_effect not in self._AUTHORITY_EFFECTS:
            raise InterfaceValidationError("authority_effect is not supported by capability snapshot")
        if self.offline_behavior not in self._OFFLINE_BEHAVIORS:
            raise InterfaceValidationError("offline_behavior is not supported")
        if self.availability_state in {AvailabilityState.BLOCKED, AvailabilityState.UNAVAILABLE}:
            if not self.reason_codes:
                raise InterfaceValidationError(
                    "blocked or unavailable snapshot capability requires reason_codes"
                )
        if self.availability_state is AvailabilityState.DEGRADED and self.degradation is None:
            raise InterfaceValidationError("degraded snapshot capability requires degradation")

        for index, item in enumerate(self.dependency_observations):
            required = {
                "dependency_ref", "dependency_type", "requirement", "state", "observed_at"
            }
            missing_fields = sorted(required - set(item))
            if missing_fields:
                raise InterfaceValidationError(
                    f"dependency_observations[{index}] missing fields: "
                    + ", ".join(missing_fields)
                )
            _require_text(item["dependency_ref"], f"dependency_observations[{index}].dependency_ref")
            if item["dependency_type"] not in self._DEPENDENCY_TYPES:
                raise InterfaceValidationError(
                    f"dependency_observations[{index}].dependency_type is not supported"
                )
            if item["requirement"] not in self._DEPENDENCY_REQUIREMENTS:
                raise InterfaceValidationError(
                    f"dependency_observations[{index}].requirement is not supported"
                )
            if item["state"] not in self._DEPENDENCY_STATES:
                raise InterfaceValidationError(
                    f"dependency_observations[{index}].state is not supported"
                )
            _parse_timestamp(item["observed_at"], f"dependency_observations[{index}].observed_at")

        if self.degradation is not None:
            required = {
                "mode", "cause_class", "preserved_behaviors", "prohibited_actions",
                "recovery_preconditions", "user_visible_state",
            }
            missing_fields = sorted(required - set(self.degradation))
            if missing_fields:
                raise InterfaceValidationError(
                    "degradation missing fields: " + ", ".join(missing_fields)
                )
            for field_name in ("mode", "cause_class", "user_visible_state"):
                _require_text(self.degradation[field_name], f"degradation.{field_name}")
            for field_name in (
                "preserved_behaviors", "prohibited_actions", "recovery_preconditions"
            ):
                values = _string_tuple(self.degradation[field_name], f"degradation.{field_name}")
                if not values:
                    raise InterfaceValidationError(f"degradation.{field_name} must not be empty")

    def to_snapshot_dict(self) -> dict[str, Any]:
        self._validate_snapshot_metadata()
        result: dict[str, Any] = {
            "capability_id": self.capability_id,
            "capability_ref": self.capability_ref,
            "owner_component_ref": self.owner_component_ref,
            "capability_class": self.capability_class,
            "authority_effect": self.authority_effect,
            "availability_state": self.availability_state.value,
            "execution_state": self.execution_state.value,
            "authoritative_outcome": self.authoritative_outcome.value,
            "offline_behavior": self.offline_behavior,
            "observed_at": _format_timestamp(self.observed_at),
            "dependency_observations": [
                _plain_value(item) for item in self.dependency_observations
            ],
            "reason_codes": list(self.reason_codes),
        }
        if self.state_entered_at is not None:
            result["state_entered_at"] = _format_timestamp(self.state_entered_at)
        if self.degradation is not None:
            result["degradation"] = _plain_value(self.degradation)
        if self.result_ref is not None:
            result["result_ref"] = self.result_ref
        if self.evidence_refs:
            result["evidence_refs"] = list(self.evidence_refs)
        if self.receipt_refs:
            result["receipt_refs"] = list(self.receipt_refs)
        return result

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> CapabilityState:
        """Parse the retained legacy health capability shape."""
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

    @classmethod
    def from_snapshot_dict(cls, data: Mapping[str, Any]) -> CapabilityState:
        if not isinstance(data, Mapping):
            raise InterfaceValidationError("capability observation must be an object")
        allowed = {
            "capability_id", "capability_ref", "owner_component_ref", "capability_class",
            "authority_effect", "availability_state", "execution_state",
            "authoritative_outcome", "offline_behavior", "observed_at", "state_entered_at",
            "dependency_observations", "degradation", "reason_codes", "result_ref",
            "evidence_refs", "receipt_refs",
        }
        _unexpected_fields(data, allowed)
        required = {
            "capability_id", "capability_ref", "owner_component_ref", "capability_class",
            "authority_effect", "availability_state", "execution_state",
            "authoritative_outcome", "offline_behavior", "observed_at",
            "dependency_observations", "reason_codes",
        }
        missing = sorted(required - set(data))
        if missing:
            raise InterfaceValidationError(f"missing fields: {', '.join(missing)}")
        return cls(
            capability_id=data["capability_id"],
            health_state=None,
            availability_state=data["availability_state"],
            execution_state=data["execution_state"],
            authoritative_outcome=data["authoritative_outcome"],
            authority_effect=data["authority_effect"],
            reason_codes=_string_tuple(data["reason_codes"], "reason_codes"),
            capability_ref=data["capability_ref"],
            owner_component_ref=data["owner_component_ref"],
            capability_class=data["capability_class"],
            offline_behavior=data["offline_behavior"],
            observed_at=data["observed_at"],
            state_entered_at=data.get("state_entered_at"),
            dependency_observations=cls._mapping_tuple(
                data["dependency_observations"], "dependency_observations"
            ),
            degradation=data.get("degradation"),
            result_ref=data.get("result_ref"),
            evidence_refs=_string_tuple(data.get("evidence_refs"), "evidence_refs"),
            receipt_refs=_string_tuple(data.get("receipt_refs"), "receipt_refs"),
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
    readiness_id: str
    component_id: str
    component_contract_ref: str
    capability_id: str
    readiness_class: ReadinessClass
    ready: bool
    operational_state: HealthState
    usable_operation_classes: tuple[str, ...]
    denied_operation_classes: tuple[str, ...]
    conditions: tuple[Mapping[str, Any], ...]
    freshness: Mapping[str, Any]
    observed_at: datetime
    reason_codes: tuple[str, ...]
    schema_version: str = "1.0.0"
    component_instance_id: str | None = None
    capability_contract_ref: str | None = None
    dependencies: tuple[Mapping[str, Any], ...] = ()
    active_contract: Mapping[str, Any] | None = None
    active_schema_versions: tuple[Mapping[str, Any], ...] = ()
    active_artifact_refs: tuple[str, ...] = ()
    profile_refs: tuple[str, ...] = ()
    recovery_conditions: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()

    SCHEMA_PATH = READINESS_SCHEMA_PATH

    def __post_init__(self) -> None:
        object.__setattr__(self, "schema_version", _require_text(self.schema_version, "schema_version"))
        if self.schema_version != "1.0.0":
            raise InterfaceValidationError("schema_version must be 1.0.0")

        readiness_id = _require_text(self.readiness_id, "readiness_id")
        if not readiness_id.startswith("readiness:"):
            raise InterfaceValidationError("readiness_id must start with 'readiness:'")
        object.__setattr__(self, "readiness_id", readiness_id)
        object.__setattr__(self, "component_id", _require_text(self.component_id, "component_id"))
        object.__setattr__(
            self,
            "component_instance_id",
            _optional_text(self.component_instance_id, "component_instance_id"),
        )
        object.__setattr__(
            self,
            "component_contract_ref",
            _require_text(self.component_contract_ref, "component_contract_ref"),
        )
        object.__setattr__(
            self,
            "capability_id",
            _require_text(self.capability_id, "capability_id"),
        )
        object.__setattr__(
            self,
            "capability_contract_ref",
            _optional_text(self.capability_contract_ref, "capability_contract_ref"),
        )
        object.__setattr__(
            self,
            "readiness_class",
            _enum_value(ReadinessClass, self.readiness_class, "readiness_class"),
        )
        if not isinstance(self.ready, bool):
            _raise_boolean("ready")
        object.__setattr__(
            self,
            "operational_state",
            _enum_value(HealthState, self.operational_state, "operational_state"),
        )
        object.__setattr__(
            self,
            "usable_operation_classes",
            _string_tuple(self.usable_operation_classes, "usable_operation_classes"),
        )
        object.__setattr__(
            self,
            "denied_operation_classes",
            _string_tuple(self.denied_operation_classes, "denied_operation_classes"),
        )
        object.__setattr__(
            self,
            "conditions",
            self._mapping_tuple(self.conditions, "conditions", require_nonempty=True),
        )
        object.__setattr__(
            self,
            "dependencies",
            self._mapping_tuple(self.dependencies, "dependencies"),
        )
        object.__setattr__(
            self,
            "active_schema_versions",
            self._mapping_tuple(self.active_schema_versions, "active_schema_versions"),
        )
        object.__setattr__(
            self,
            "active_artifact_refs",
            _string_tuple(self.active_artifact_refs, "active_artifact_refs"),
        )
        object.__setattr__(self, "profile_refs", _string_tuple(self.profile_refs, "profile_refs"))
        object.__setattr__(
            self,
            "recovery_conditions",
            _string_tuple(self.recovery_conditions, "recovery_conditions"),
        )
        object.__setattr__(self, "evidence_refs", _string_tuple(self.evidence_refs, "evidence_refs"))
        object.__setattr__(self, "reason_codes", _string_tuple(self.reason_codes, "reason_codes"))
        object.__setattr__(self, "observed_at", _parse_timestamp(self.observed_at, "observed_at"))

        if not isinstance(self.freshness, Mapping):
            raise InterfaceValidationError("freshness must be an object")
        freshness = _freeze_mapping(self.freshness, "freshness")
        for field_name in ("source", "confidence", "staleness_state", "observed_at"):
            if field_name not in freshness:
                raise InterfaceValidationError(f"freshness missing field: {field_name}")
        _require_text(freshness["source"], "freshness.source")
        confidence = _require_text(freshness["confidence"], "freshness.confidence")
        if confidence not in {"direct", "derived", "reported", "unknown"}:
            raise InterfaceValidationError("unsupported freshness.confidence")
        staleness = _require_text(freshness["staleness_state"], "freshness.staleness_state")
        if staleness not in {"current", "stale", "unknown"}:
            raise InterfaceValidationError("unsupported freshness.staleness_state")
        _parse_timestamp(freshness["observed_at"], "freshness.observed_at")
        object.__setattr__(self, "freshness", freshness)

        if self.active_contract is not None:
            if not isinstance(self.active_contract, Mapping):
                raise InterfaceValidationError("active_contract must be an object")
            object.__setattr__(self, "active_contract", _freeze_mapping(self.active_contract, "active_contract"))

        self._validate_conditions()
        self._validate_dependencies()

        if self.ready and not self.usable_operation_classes:
            raise InterfaceValidationError("ready readiness must identify usable_operation_classes")
        if not self.ready and not self.denied_operation_classes:
            raise InterfaceValidationError("non-ready readiness must identify denied_operation_classes")
        if not self.ready and not self.reason_codes:
            raise InterfaceValidationError("non-ready readiness must identify reason_codes")
        if self.operational_state is HealthState.HEALTHY and not self.ready:
            raise InterfaceValidationError("operational_state=healthy requires ready=true")
        if staleness == "stale":
            if self.operational_state is HealthState.HEALTHY:
                raise InterfaceValidationError("stale freshness cannot report operational_state=healthy")
            if not self.reason_codes:
                raise InterfaceValidationError("stale freshness requires reason_codes")

    @staticmethod
    def _mapping_tuple(
        value: object,
        field_name: str,
        *,
        require_nonempty: bool = False,
    ) -> tuple[Mapping[str, Any], ...]:
        if isinstance(value, (str, bytes)) or not isinstance(value, (list, tuple)):
            raise InterfaceValidationError(f"{field_name} must be an array")
        if require_nonempty and not value:
            raise InterfaceValidationError(f"{field_name} must not be empty")
        result: list[Mapping[str, Any]] = []
        for index, item in enumerate(value):
            if not isinstance(item, Mapping):
                raise InterfaceValidationError(f"{field_name}[{index}] must be an object")
            result.append(MappingProxyType(dict(item)))
        return tuple(result)

    def _validate_conditions(self) -> None:
        categories = {
            "process_liveness",
            "startup_completion",
            "contract_readiness",
            "dependency_readiness",
            "data_readiness",
            "identity_and_trust_readiness",
            "policy_readiness",
            "local_read_readiness",
            "write_readiness",
            "execution_readiness",
            "background_work_readiness",
            "recovery_readiness",
        }
        statuses = {"satisfied", "unsatisfied", "degraded", "stale", "unknown", "not_applicable"}
        needs_reason = {"unsatisfied", "degraded", "stale", "unknown"}
        for index, condition in enumerate(self.conditions):
            for field_name in ("condition_id", "category", "required", "status"):
                if field_name not in condition:
                    raise InterfaceValidationError(f"conditions[{index}] missing field: {field_name}")
            _require_text(condition["condition_id"], f"conditions[{index}].condition_id")
            category = _require_text(condition["category"], f"conditions[{index}].category")
            if category not in categories:
                raise InterfaceValidationError(f"conditions[{index}].category is not supported")
            if not isinstance(condition["required"], bool):
                raise InterfaceValidationError(f"conditions[{index}].required must be a boolean")
            status = _require_text(condition["status"], f"conditions[{index}].status")
            if status not in statuses:
                raise InterfaceValidationError(f"conditions[{index}].status is not supported")
            if "observed_at" in condition:
                _parse_timestamp(condition["observed_at"], f"conditions[{index}].observed_at")
            if status in needs_reason and not _string_tuple(
                condition.get("reason_codes"), f"conditions[{index}].reason_codes"
            ):
                raise InterfaceValidationError(
                    f"conditions[{index}] with status={status} requires reason_codes"
                )

    def _validate_dependencies(self) -> None:
        classifications = {
            "required_component",
            "required_capability",
            "conditional",
            "optional",
            "external_integration",
        }
        states = {"available", "degraded", "stale", "unavailable", "unknown", "not_applicable"}
        needs_reason = {"degraded", "stale", "unavailable", "unknown"}
        for index, dependency in enumerate(self.dependencies):
            for field_name in ("dependency_id", "classification", "state", "required_for_this_class"):
                if field_name not in dependency:
                    raise InterfaceValidationError(f"dependencies[{index}] missing field: {field_name}")
            _require_text(dependency["dependency_id"], f"dependencies[{index}].dependency_id")
            classification = _require_text(
                dependency["classification"], f"dependencies[{index}].classification"
            )
            if classification not in classifications:
                raise InterfaceValidationError(f"dependencies[{index}].classification is not supported")
            state = _require_text(dependency["state"], f"dependencies[{index}].state")
            if state not in states:
                raise InterfaceValidationError(f"dependencies[{index}].state is not supported")
            if not isinstance(dependency["required_for_this_class"], bool):
                raise InterfaceValidationError(
                    f"dependencies[{index}].required_for_this_class must be a boolean"
                )
            if "observed_at" in dependency:
                _parse_timestamp(dependency["observed_at"], f"dependencies[{index}].observed_at")
            if state in needs_reason and not _string_tuple(
                dependency.get("reason_codes"), f"dependencies[{index}].reason_codes"
            ):
                raise InterfaceValidationError(
                    f"dependencies[{index}] with state={state} requires reason_codes"
                )

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "schema_version": self.schema_version,
            "readiness_id": self.readiness_id,
            "component_id": self.component_id,
            "component_contract_ref": self.component_contract_ref,
            "capability_id": self.capability_id,
            "readiness_class": self.readiness_class.value,
            "ready": self.ready,
            "operational_state": self.operational_state.value,
            "usable_operation_classes": list(self.usable_operation_classes),
            "denied_operation_classes": list(self.denied_operation_classes),
            "conditions": [_plain_value(item) for item in self.conditions],
            "freshness": _plain_value(self.freshness),
            "observed_at": _format_timestamp(self.observed_at),
            "reason_codes": list(self.reason_codes),
        }
        optional_text = {
            "component_instance_id": self.component_instance_id,
            "capability_contract_ref": self.capability_contract_ref,
        }
        for field_name, value in optional_text.items():
            if value is not None:
                result[field_name] = value
        if self.dependencies:
            result["dependencies"] = [_plain_value(item) for item in self.dependencies]
        if self.active_contract is not None:
            result["active_contract"] = _plain_value(self.active_contract)
        if self.active_schema_versions:
            result["active_schema_versions"] = [
                _plain_value(item) for item in self.active_schema_versions
            ]
        if self.active_artifact_refs:
            result["active_artifact_refs"] = list(self.active_artifact_refs)
        if self.profile_refs:
            result["profile_refs"] = list(self.profile_refs)
        if self.recovery_conditions:
            result["recovery_conditions"] = list(self.recovery_conditions)
        if self.evidence_refs:
            result["evidence_refs"] = list(self.evidence_refs)
        return result

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Readiness:
        if not isinstance(data, Mapping):
            raise InterfaceValidationError("readiness must be an object")
        allowed = {
            "schema_version",
            "readiness_id",
            "component_id",
            "component_instance_id",
            "component_contract_ref",
            "capability_id",
            "capability_contract_ref",
            "readiness_class",
            "ready",
            "operational_state",
            "usable_operation_classes",
            "denied_operation_classes",
            "conditions",
            "dependencies",
            "active_contract",
            "active_schema_versions",
            "active_artifact_refs",
            "profile_refs",
            "freshness",
            "observed_at",
            "reason_codes",
            "recovery_conditions",
            "evidence_refs",
        }
        _unexpected_fields(data, allowed)
        required = {
            "schema_version",
            "readiness_id",
            "component_id",
            "component_contract_ref",
            "capability_id",
            "readiness_class",
            "ready",
            "operational_state",
            "usable_operation_classes",
            "denied_operation_classes",
            "conditions",
            "freshness",
            "observed_at",
            "reason_codes",
        }
        missing = sorted(required - set(data))
        if missing:
            raise InterfaceValidationError(f"missing fields: {', '.join(missing)}")
        return cls(
            schema_version=data["schema_version"],
            readiness_id=data["readiness_id"],
            component_id=data["component_id"],
            component_instance_id=data.get("component_instance_id"),
            component_contract_ref=data["component_contract_ref"],
            capability_id=data["capability_id"],
            capability_contract_ref=data.get("capability_contract_ref"),
            readiness_class=data["readiness_class"],
            ready=data["ready"] if isinstance(data["ready"], bool) else _raise_boolean("ready"),
            operational_state=data["operational_state"],
            usable_operation_classes=_string_tuple(
                data["usable_operation_classes"], "usable_operation_classes"
            ),
            denied_operation_classes=_string_tuple(
                data["denied_operation_classes"], "denied_operation_classes"
            ),
            conditions=cls._mapping_tuple(data["conditions"], "conditions", require_nonempty=True),
            dependencies=cls._mapping_tuple(data.get("dependencies", ()), "dependencies"),
            active_contract=(
                _freeze_mapping(data["active_contract"], "active_contract")
                if data.get("active_contract") is not None
                else None
            ),
            active_schema_versions=cls._mapping_tuple(
                data.get("active_schema_versions", ()), "active_schema_versions"
            ),
            active_artifact_refs=_string_tuple(
                data.get("active_artifact_refs"), "active_artifact_refs"
            ),
            profile_refs=_string_tuple(data.get("profile_refs"), "profile_refs"),
            freshness=_freeze_mapping(data["freshness"], "freshness"),
            observed_at=data["observed_at"],
            reason_codes=_string_tuple(data["reason_codes"], "reason_codes"),
            recovery_conditions=_string_tuple(
                data.get("recovery_conditions"), "recovery_conditions"
            ),
            evidence_refs=_string_tuple(data.get("evidence_refs"), "evidence_refs"),
        )


@dataclass(frozen=True, slots=True)
class CapabilitySnapshot:
    snapshot_id: str
    producer_component_ref: str
    observed_at: datetime
    profile_ref: str
    scope: Mapping[str, Any]
    capabilities: tuple[CapabilityState, ...]
    correlation: Mapping[str, Any]
    schema_version: str = "1.0.0"
    substitution_applied: bool = False
    valid_until: datetime | None = None
    overlay_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    receipt_refs: tuple[str, ...] = ()

    SCHEMA_PATH = CAPABILITY_SNAPSHOT_SCHEMA_PATH

    def __post_init__(self) -> None:
        object.__setattr__(self, "snapshot_id", _require_text(self.snapshot_id, "snapshot_id"))
        object.__setattr__(
            self,
            "producer_component_ref",
            _require_text(self.producer_component_ref, "producer_component_ref"),
        )
        object.__setattr__(self, "observed_at", _parse_timestamp(self.observed_at, "observed_at"))
        object.__setattr__(self, "profile_ref", _require_text(self.profile_ref, "profile_ref"))
        object.__setattr__(
            self, "schema_version", _require_text(self.schema_version, "schema_version")
        )
        if self.schema_version != "1.0.0":
            raise InterfaceValidationError("schema_version must be 1.0.0")
        if self.substitution_applied is not False:
            raise InterfaceValidationError("substitution_applied must be false")
        if self.valid_until is not None:
            object.__setattr__(
                self, "valid_until", _parse_timestamp(self.valid_until, "valid_until")
            )

        if not isinstance(self.scope, Mapping):
            raise InterfaceValidationError("scope must be an object")
        scope = MappingProxyType(dict(self.scope))
        if "environment" not in scope:
            raise InterfaceValidationError("scope missing fields: environment")
        _require_text(scope["environment"], "scope.environment")
        allowed_scope = {
            "environment", "tenant_ref", "organization_ref", "node_ref", "workspace_ref",
            "component_ref", "target_ref",
        }
        _unexpected_fields(scope, allowed_scope)
        for field_name in allowed_scope - {"environment"}:
            if field_name in scope:
                _require_text(scope[field_name], f"scope.{field_name}")
        object.__setattr__(self, "scope", scope)

        if not isinstance(self.correlation, Mapping):
            raise InterfaceValidationError("correlation must be an object")
        correlation = MappingProxyType(dict(self.correlation))
        allowed_correlation = {"schema_version", "correlation_id", "request_id", "causation_id"}
        _unexpected_fields(correlation, allowed_correlation)
        missing_correlation = sorted({"schema_version", "correlation_id"} - set(correlation))
        if missing_correlation:
            raise InterfaceValidationError(
                "correlation missing fields: " + ", ".join(missing_correlation)
            )
        if correlation["schema_version"] != "1.0.0":
            raise InterfaceValidationError("correlation.schema_version must be 1.0.0")
        _require_text(correlation["correlation_id"], "correlation.correlation_id")
        for field_name in ("request_id", "causation_id"):
            if field_name in correlation:
                _require_text(correlation[field_name], f"correlation.{field_name}")
        object.__setattr__(self, "correlation", correlation)

        if not isinstance(self.capabilities, tuple):
            object.__setattr__(self, "capabilities", tuple(self.capabilities))
        if not self.capabilities or not all(
            isinstance(item, CapabilityState) for item in self.capabilities
        ):
            raise InterfaceValidationError("capabilities must contain CapabilityState values")
        for item in self.capabilities:
            item._validate_snapshot_metadata()
        identifiers = [item.capability_id for item in self.capabilities]
        if len(identifiers) != len(set(identifiers)):
            raise InterfaceValidationError("capability_id values must be unique in a snapshot")

        object.__setattr__(self, "overlay_refs", _string_tuple(self.overlay_refs, "overlay_refs"))
        object.__setattr__(self, "evidence_refs", _string_tuple(self.evidence_refs, "evidence_refs"))
        object.__setattr__(self, "receipt_refs", _string_tuple(self.receipt_refs, "receipt_refs"))

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "schema_version": self.schema_version,
            "snapshot_id": self.snapshot_id,
            "producer_component_ref": self.producer_component_ref,
            "observed_at": _format_timestamp(self.observed_at),
            "profile_ref": self.profile_ref,
            "scope": _plain_value(self.scope),
            "capabilities": [item.to_snapshot_dict() for item in self.capabilities],
            "substitution_applied": False,
            "correlation": _plain_value(self.correlation),
        }
        if self.valid_until is not None:
            result["valid_until"] = _format_timestamp(self.valid_until)
        if self.overlay_refs:
            result["overlay_refs"] = list(self.overlay_refs)
        if self.evidence_refs:
            result["evidence_refs"] = list(self.evidence_refs)
        if self.receipt_refs:
            result["receipt_refs"] = list(self.receipt_refs)
        return result

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> CapabilitySnapshot:
        if not isinstance(data, Mapping):
            raise InterfaceValidationError("capability snapshot must be an object")
        allowed = {
            "schema_version", "snapshot_id", "producer_component_ref", "observed_at",
            "valid_until", "profile_ref", "overlay_refs", "scope", "capabilities",
            "substitution_applied", "evidence_refs", "receipt_refs", "correlation",
        }
        _unexpected_fields(data, allowed)
        required = {
            "schema_version", "snapshot_id", "producer_component_ref", "observed_at",
            "profile_ref", "scope", "capabilities", "substitution_applied", "correlation",
        }
        missing = sorted(required - set(data))
        if missing:
            raise InterfaceValidationError(f"missing fields: {', '.join(missing)}")
        raw = data["capabilities"]
        if isinstance(raw, (str, bytes, bytearray)) or not isinstance(raw, (list, tuple)):
            raise InterfaceValidationError("capabilities must be an array")
        return cls(
            schema_version=data["schema_version"],
            snapshot_id=data["snapshot_id"],
            producer_component_ref=data["producer_component_ref"],
            observed_at=data["observed_at"],
            valid_until=data.get("valid_until"),
            profile_ref=data["profile_ref"],
            overlay_refs=_string_tuple(data.get("overlay_refs"), "overlay_refs"),
            scope=data["scope"],
            capabilities=tuple(CapabilityState.from_snapshot_dict(item) for item in raw),
            substitution_applied=(
                data["substitution_applied"]
                if isinstance(data["substitution_applied"], bool)
                else _raise_boolean("substitution_applied")
            ),
            evidence_refs=_string_tuple(data.get("evidence_refs"), "evidence_refs"),
            receipt_refs=_string_tuple(data.get("receipt_refs"), "receipt_refs"),
            correlation=data["correlation"],
        )

