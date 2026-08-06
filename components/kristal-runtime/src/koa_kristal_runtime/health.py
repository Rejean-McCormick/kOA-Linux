"""Bounded Kristal Runtime health and readiness reporting."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime
from enum import StrEnum
from threading import RLock
from typing import Callable
import re


class RuntimeState(StrEnum):
    INACTIVE = "inactive"
    VERIFICATION_PENDING = "verification_pending"
    VERIFIED = "verified"
    ACTIVE = "active"
    BLOCKED = "blocked"
    DEGRADED = "degraded"
    ROLLBACK_IN_PROGRESS = "rollback_in_progress"
    FAILED = "failed"


class CheckState(StrEnum):
    PASS = "pass"
    FAIL = "fail"
    UNKNOWN = "unknown"


class DependencyState(StrEnum):
    AVAILABLE = "available"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"


HEALTH_CHECKS = (
    "active_record_accessible",
    "local_state_accessible",
    "process_responsive",
    "receipt_store_accessible",
)
READINESS_CHECKS = (
    "artifact_contracts_resolve",
    "evidence_path_resolves",
    "interface_version_compatible",
    "knowledge_release_channel_resolves",
    "profile_membership_resolves",
    "runtime_state_resolves",
)
CAPABILITIES = (
    "kristal_identity_resolution",
    "runtime_pack_activation",
    "runtime_pack_rollback",
    "runtime_pack_validation",
    "runtime_status_query",
)
_REFERENCE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/@+-]{0,254}$")


@dataclass(frozen=True, slots=True)
class HealthSnapshot:
    component_id: str
    contract_version: str
    runtime_version: str
    observed_at: datetime
    runtime_state: RuntimeState
    healthy: bool
    ready: bool
    health_checks: tuple[tuple[str, CheckState], ...]
    readiness_checks: tuple[tuple[str, CheckState], ...]
    available_capabilities: tuple[str, ...]
    blocked_capabilities: tuple[str, ...]
    reasons: tuple[str, ...]
    active_runtime_pack_ref: str | None
    last_valid_runtime_pack_ref: str | None
    profile_ref: str | None
    revocation_freshness_ref: str | None
    identity_and_trust: DependencyState
    resource_governor: DependencyState
    governance_policy_runtime: DependencyState
    audit_broker: DependencyState
    offline_operation: bool

    def as_dict(self) -> dict[str, object]:
        return {
            "active_runtime_pack_ref": self.active_runtime_pack_ref,
            "audit_broker": self.audit_broker.value,
            "available_capabilities": list(self.available_capabilities),
            "blocked_capabilities": list(self.blocked_capabilities),
            "component_id": self.component_id,
            "contract_version": self.contract_version,
            "governance_policy_runtime": self.governance_policy_runtime.value,
            "health_checks": {name: state.value for name, state in self.health_checks},
            "healthy": self.healthy,
            "identity_and_trust": self.identity_and_trust.value,
            "last_valid_runtime_pack_ref": self.last_valid_runtime_pack_ref,
            "observed_at": _format_time(self.observed_at),
            "offline_operation": self.offline_operation,
            "profile_ref": self.profile_ref,
            "readiness_checks": {name: state.value for name, state in self.readiness_checks},
            "ready": self.ready,
            "reasons": list(self.reasons),
            "resource_governor": self.resource_governor.value,
            "revocation_freshness_ref": self.revocation_freshness_ref,
            "runtime_state": self.runtime_state.value,
            "runtime_version": self.runtime_version,
        }


@dataclass(frozen=True, slots=True)
class _OperationalState:
    runtime_state: RuntimeState = RuntimeState.INACTIVE
    process_responsive: CheckState = CheckState.UNKNOWN
    local_state_accessible: CheckState = CheckState.UNKNOWN
    active_record_accessible: CheckState = CheckState.UNKNOWN
    receipt_store_accessible: CheckState = CheckState.UNKNOWN
    profile_membership_resolves: CheckState = CheckState.UNKNOWN
    artifact_contracts_resolve: CheckState = CheckState.UNKNOWN
    knowledge_release_channel_resolves: CheckState = CheckState.UNKNOWN
    interface_version_compatible: CheckState = CheckState.UNKNOWN
    runtime_state_resolves: CheckState = CheckState.UNKNOWN
    evidence_path_resolves: CheckState = CheckState.UNKNOWN
    canonical_content_resolver_available: bool = False
    validation_engine_available: bool = False
    activation_executor_available: bool = False
    rollback_executor_available: bool = False
    active_runtime_pack_ref: str | None = None
    last_valid_runtime_pack_ref: str | None = None
    profile_ref: str | None = None
    revocation_freshness_ref: str | None = None
    identity_and_trust: DependencyState = DependencyState.UNKNOWN
    resource_governor: DependencyState = DependencyState.UNKNOWN
    governance_policy_runtime: DependencyState = DependencyState.UNKNOWN
    audit_broker: DependencyState = DependencyState.UNKNOWN
    trust_validation_required: bool = True
    offline_operation: bool = False
    additional_reasons: tuple[str, ...] = ()


class KristalRuntimeHealth:
    COMPONENT_ID = "kristal_runtime"
    CONTRACT_VERSION = "1.0.0"

    def __init__(self, *, runtime_version: str, clock: Callable[[], datetime]) -> None:
        self._runtime_version = runtime_version
        self._clock = clock
        self._state = _OperationalState()
        self._lock = RLock()

    def update(self, **changes: object) -> None:
        allowed = set(_OperationalState.__dataclass_fields__)
        unknown = sorted(set(changes) - allowed)
        if unknown:
            raise ValueError("unknown health fields: " + ", ".join(unknown))
        for name in ("active_runtime_pack_ref", "last_valid_runtime_pack_ref", "profile_ref", "revocation_freshness_ref"):
            value = changes.get(name)
            if value is not None and not _REFERENCE.fullmatch(str(value)):
                raise ValueError(f"{name} must be a bounded reference")
        if "additional_reasons" in changes:
            changes["additional_reasons"] = tuple(sorted(set(changes["additional_reasons"])))
        with self._lock:
            self._state = replace(self._state, **changes)

    def snapshot(self) -> HealthSnapshot:
        with self._lock:
            state = self._state
        health = tuple((name, getattr(state, name)) for name in HEALTH_CHECKS)
        readiness = tuple((name, getattr(state, name)) for name in READINESS_CHECKS)
        healthy = all(value is CheckState.PASS for _, value in health)
        ready = healthy and all(value is CheckState.PASS for _, value in readiness)

        available = ["health_and_readiness"]
        blocked: list[str] = []
        if healthy and state.runtime_state_resolves is CheckState.PASS:
            available.append("runtime_status_query")
        else:
            blocked.append("runtime_status_query")
        if state.canonical_content_resolver_available and state.artifact_contracts_resolve is CheckState.PASS:
            available.append("kristal_identity_resolution")
        else:
            blocked.append("kristal_identity_resolution")
        trust_ok = (not state.trust_validation_required) or state.identity_and_trust is DependencyState.AVAILABLE
        if ready and state.validation_engine_available and trust_ok:
            available.append("runtime_pack_validation")
        else:
            blocked.append("runtime_pack_validation")
        governance_ok = state.governance_policy_runtime is DependencyState.AVAILABLE
        resource_ok = state.resource_governor is DependencyState.AVAILABLE
        active_preconditions = ready and trust_ok and governance_ok and resource_ok
        if active_preconditions and state.activation_executor_available:
            available.append("runtime_pack_activation")
        else:
            blocked.append("runtime_pack_activation")
        if active_preconditions and state.rollback_executor_available and state.last_valid_runtime_pack_ref is not None:
            available.append("runtime_pack_rollback")
        else:
            blocked.append("runtime_pack_rollback")

        reasons = list(state.additional_reasons)
        for name, value in health + readiness:
            if value is not CheckState.PASS:
                reasons.append(f"{name}:{value.value}")
        if state.trust_validation_required and not trust_ok:
            reasons.append("required_trust_unavailable")
        if not governance_ok:
            reasons.append("required_governance_authority_unavailable")
        if not resource_ok:
            reasons.append("required_resource_admission_unavailable")
        if not state.canonical_content_resolver_available:
            reasons.append("canonical_content_resolver_unavailable")
        if not state.validation_engine_available:
            reasons.append("runtime_pack_validation_engine_unavailable")
        return HealthSnapshot(
            component_id=self.COMPONENT_ID,
            contract_version=self.CONTRACT_VERSION,
            runtime_version=self._runtime_version,
            observed_at=_utc_time(self._clock()),
            runtime_state=state.runtime_state,
            healthy=healthy,
            ready=ready,
            health_checks=health,
            readiness_checks=readiness,
            available_capabilities=tuple(sorted(set(available))),
            blocked_capabilities=tuple(sorted(set(blocked))),
            reasons=tuple(sorted(set(reasons))),
            active_runtime_pack_ref=state.active_runtime_pack_ref,
            last_valid_runtime_pack_ref=state.last_valid_runtime_pack_ref,
            profile_ref=state.profile_ref,
            revocation_freshness_ref=state.revocation_freshness_ref,
            identity_and_trust=state.identity_and_trust,
            resource_governor=state.resource_governor,
            governance_policy_runtime=state.governance_policy_runtime,
            audit_broker=state.audit_broker,
            offline_operation=state.offline_operation,
        )


def _utc_time(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("health clock must return a timezone-aware datetime")
    return value.astimezone(UTC)


def _format_time(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
