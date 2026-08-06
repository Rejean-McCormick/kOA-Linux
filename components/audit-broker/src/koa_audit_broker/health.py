"""Bounded Audit Broker health and readiness reporting."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime
from enum import StrEnum
from threading import RLock
from typing import Callable


class ComponentState(StrEnum):
    UNINITIALIZED = "uninitialized"
    STARTING = "starting"
    READY = "ready"
    DEGRADED = "degraded"
    READ_ONLY = "read_only"
    RECOVERING = "recovering"
    STOPPING = "stopping"
    UNAVAILABLE = "unavailable"


class DependencyState(StrEnum):
    AVAILABLE = "available"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"


class StorageCapacityState(StrEnum):
    NORMAL = "normal"
    WARNING = "warning"
    READ_ONLY_REQUIRED = "read_only_required"
    UNKNOWN = "unknown"


class RetentionJobState(StrEnum):
    IDLE = "idle"
    RUNNING = "running"
    DEGRADED = "degraded"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


class IntegrityAlarmState(StrEnum):
    CLEAR = "clear"
    ACTIVE = "active"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class ReadinessSnapshot:
    ready: bool
    available_capabilities: tuple[str, ...]
    blocked_capabilities: tuple[str, ...]
    reasons: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "ready": self.ready,
            "available_capabilities": list(self.available_capabilities),
            "blocked_capabilities": list(self.blocked_capabilities),
            "reasons": list(self.reasons),
        }


@dataclass(frozen=True, slots=True)
class HealthSnapshot:
    schema_version: str
    component_id: str
    observed_at: datetime
    component_state: ComponentState
    ingestion_queue_depth: int
    query_queue_depth: int
    disclosure_queue_depth: int
    storage_capacity_state: StorageCapacityState
    retention_job_state: RetentionJobState
    policy_path_state: DependencyState
    identity_path_state: DependencyState
    integrity_alarm_state: IntegrityAlarmState
    last_successful_backup_or_recovery_point: str | None
    readiness: ReadinessSnapshot

    def as_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "component_id": self.component_id,
            "observed_at": self.observed_at.isoformat().replace("+00:00", "Z"),
            "component_state": self.component_state.value,
            "ingestion_queue_depth": self.ingestion_queue_depth,
            "query_queue_depth": self.query_queue_depth,
            "disclosure_queue_depth": self.disclosure_queue_depth,
            "storage_capacity_state": self.storage_capacity_state.value,
            "retention_job_state": self.retention_job_state.value,
            "policy_path_state": self.policy_path_state.value,
            "identity_path_state": self.identity_path_state.value,
            "integrity_alarm_state": self.integrity_alarm_state.value,
            "last_successful_backup_or_recovery_point": (
                self.last_successful_backup_or_recovery_point
            ),
            "readiness": self.readiness.as_dict(),
        }


@dataclass(frozen=True, slots=True)
class _HealthState:
    component_state: ComponentState = ComponentState.UNINITIALIZED
    ingestion_queue_depth: int = 0
    query_queue_depth: int = 0
    disclosure_queue_depth: int = 0
    storage_capacity_state: StorageCapacityState = StorageCapacityState.UNKNOWN
    retention_job_state: RetentionJobState = RetentionJobState.UNKNOWN
    policy_path_state: DependencyState = DependencyState.UNKNOWN
    identity_path_state: DependencyState = DependencyState.UNKNOWN
    integrity_alarm_state: IntegrityAlarmState = IntegrityAlarmState.UNKNOWN
    last_successful_backup_or_recovery_point: str | None = None
    submission_interface_ready: bool = False
    record_store_ready: bool = False
    chain_of_custody_ready: bool = False
    receipt_generation_ready: bool = False


class AuditBrokerHealth:
    """Thread-safe bounded health state.

    The class intentionally has no generic metadata or labels field: callers cannot
    accidentally add source records, protected identifiers, or evidence payloads.
    """

    _SCHEMA_VERSION = "1.0.0"
    _COMPONENT_ID = "audit_broker"
    _ALL_CAPABILITIES = (
        "audit_event_ingestion",
        "audit_metadata_query",
        "governed_disclosure",
        "retention_actions",
        "receipt_generation",
    )

    def __init__(self, clock: Callable[[], datetime] | None = None) -> None:
        self._clock = clock or (lambda: datetime.now(UTC))
        self._lock = RLock()
        self._state = _HealthState()

    def update(self, **changes: object) -> None:
        allowed = set(_HealthState.__dataclass_fields__)
        unknown = set(changes) - allowed
        if unknown:
            raise ValueError(f"unsupported health fields: {sorted(unknown)!r}")
        for name in ("ingestion_queue_depth", "query_queue_depth", "disclosure_queue_depth"):
            if name in changes and int(changes[name]) < 0:
                raise ValueError(f"{name} must not be negative")
        with self._lock:
            self._state = replace(self._state, **changes)

    def snapshot(self) -> HealthSnapshot:
        with self._lock:
            state = self._state
        observed_at = self._clock()
        if observed_at.tzinfo is None or observed_at.utcoffset() is None:
            raise ValueError("health clock must return a timezone-aware datetime")
        readiness = self._readiness(state)
        return HealthSnapshot(
            schema_version=self._SCHEMA_VERSION,
            component_id=self._COMPONENT_ID,
            observed_at=observed_at.astimezone(UTC),
            component_state=state.component_state,
            ingestion_queue_depth=state.ingestion_queue_depth,
            query_queue_depth=state.query_queue_depth,
            disclosure_queue_depth=state.disclosure_queue_depth,
            storage_capacity_state=state.storage_capacity_state,
            retention_job_state=state.retention_job_state,
            policy_path_state=state.policy_path_state,
            identity_path_state=state.identity_path_state,
            integrity_alarm_state=state.integrity_alarm_state,
            last_successful_backup_or_recovery_point=(
                state.last_successful_backup_or_recovery_point
            ),
            readiness=readiness,
        )

    def _readiness(self, state: _HealthState) -> ReadinessSnapshot:
        reasons: list[str] = []
        available: list[str] = []
        blocked: list[str] = []

        identity_ready = state.identity_path_state is DependencyState.AVAILABLE
        storage_ready = state.record_store_ready and state.storage_capacity_state in {
            StorageCapacityState.NORMAL,
            StorageCapacityState.WARNING,
        }
        core_ready = (
            state.submission_interface_ready
            and storage_ready
            and identity_ready
            and state.chain_of_custody_ready
            and state.receipt_generation_ready
            and state.integrity_alarm_state is IntegrityAlarmState.CLEAR
        )

        if core_ready and state.component_state in {
            ComponentState.READY,
            ComponentState.DEGRADED,
        }:
            available.extend(
                ["audit_event_ingestion", "audit_metadata_query", "receipt_generation"]
            )
        else:
            blocked.extend(
                ["audit_event_ingestion", "audit_metadata_query", "receipt_generation"]
            )

        if core_ready and state.policy_path_state is DependencyState.AVAILABLE:
            available.extend(["governed_disclosure", "retention_actions"])
        else:
            blocked.extend(["governed_disclosure", "retention_actions"])

        if not identity_ready:
            reasons.append("identity_path_unavailable")
        if not state.record_store_ready:
            reasons.append("record_store_unavailable")
        if state.storage_capacity_state is StorageCapacityState.READ_ONLY_REQUIRED:
            reasons.append("storage_read_only_required")
        if state.policy_path_state is not DependencyState.AVAILABLE:
            reasons.append("policy_path_not_ready")
        if not state.chain_of_custody_ready:
            reasons.append("chain_of_custody_not_ready")
        if not state.receipt_generation_ready:
            reasons.append("receipt_generation_not_ready")
        if state.integrity_alarm_state is not IntegrityAlarmState.CLEAR:
            reasons.append("integrity_alarm_not_clear")
        if state.component_state in {
            ComponentState.UNINITIALIZED,
            ComponentState.STARTING,
            ComponentState.STOPPING,
            ComponentState.UNAVAILABLE,
            ComponentState.RECOVERING,
        }:
            reasons.append(f"component_state_{state.component_state.value}")

        available_tuple = tuple(item for item in self._ALL_CAPABILITIES if item in available)
        blocked_tuple = tuple(item for item in self._ALL_CAPABILITIES if item in blocked)
        return ReadinessSnapshot(
            ready=not blocked_tuple,
            available_capabilities=available_tuple,
            blocked_capabilities=blocked_tuple,
            reasons=tuple(sorted(set(reasons))),
        )
