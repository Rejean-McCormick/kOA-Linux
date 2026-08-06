"""Bounded Governance Policy Runtime health and readiness reporting."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime
from enum import StrEnum
from threading import RLock
from typing import Callable
import re


class ComponentState(StrEnum):
    UNINITIALIZED = "uninitialized"
    STARTING = "starting"
    READY = "ready"
    DEGRADED = "degraded"
    STOPPING = "stopping"
    UNAVAILABLE = "unavailable"


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
    "local_storage_accessible",
    "process_responsive",
    "receipt_store_accessible",
)
READINESS_CHECKS = (
    "active_policy_set_resolves",
    "authority_version_resolves",
    "critical_receipt_path_ready",
    "evaluator_version_compatible",
    "policy_set_compatible_with_components",
    "policy_set_compatible_with_profile",
    "required_exception_data_resolves",
    "required_trust_sources_resolve",
)
DECISION_CAPABILITIES = (
    "evaluate_authorization",
    "evaluate_consent",
    "evaluate_disclosure",
    "evaluate_exception",
    "evaluate_privilege",
)
_REFERENCE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/@+-]{0,254}$")


@dataclass(frozen=True, slots=True)
class HealthSnapshot:
    component_id: str
    contract_version: str
    runtime_version: str
    observed_at: datetime
    component_state: ComponentState
    healthy: bool
    ready: bool
    health_checks: tuple[tuple[str, CheckState], ...]
    readiness_checks: tuple[tuple[str, CheckState], ...]
    available_capabilities: tuple[str, ...]
    blocked_capabilities: tuple[str, ...]
    reasons: tuple[str, ...]
    active_policy_set_ref: str | None
    previous_valid_policy_set_ref: str | None
    authority_version: str | None
    profile_ref: str | None
    audit_path_state: DependencyState
    activation_path_state: DependencyState
    resource_peer_state: DependencyState
    offline_governed_operation: bool

    def as_dict(self) -> dict[str, object]:
        return {
            "active_policy_set_ref": self.active_policy_set_ref,
            "activation_path_state": self.activation_path_state.value,
            "audit_path_state": self.audit_path_state.value,
            "authority_version": self.authority_version,
            "available_capabilities": list(self.available_capabilities),
            "blocked_capabilities": list(self.blocked_capabilities),
            "component_id": self.component_id,
            "component_state": self.component_state.value,
            "contract_version": self.contract_version,
            "health_checks": {name: state.value for name, state in self.health_checks},
            "healthy": self.healthy,
            "observed_at": _format_time(self.observed_at),
            "offline_governed_operation": self.offline_governed_operation,
            "previous_valid_policy_set_ref": self.previous_valid_policy_set_ref,
            "profile_ref": self.profile_ref,
            "readiness_checks": {
                name: state.value for name, state in self.readiness_checks
            },
            "ready": self.ready,
            "reasons": list(self.reasons),
            "resource_peer_state": self.resource_peer_state.value,
            "runtime_version": self.runtime_version,
        }


@dataclass(frozen=True, slots=True)
class _OperationalState:
    component_state: ComponentState = ComponentState.UNINITIALIZED
    process_responsive: CheckState = CheckState.UNKNOWN
    local_storage_accessible: CheckState = CheckState.UNKNOWN
    receipt_store_accessible: CheckState = CheckState.UNKNOWN
    active_policy_set_resolves: CheckState = CheckState.UNKNOWN
    policy_set_compatible_with_profile: CheckState = CheckState.UNKNOWN
    policy_set_compatible_with_components: CheckState = CheckState.UNKNOWN
    authority_version_resolves: CheckState = CheckState.UNKNOWN
    required_trust_sources_resolve: CheckState = CheckState.UNKNOWN
    required_exception_data_resolves: CheckState = CheckState.UNKNOWN
    evaluator_version_compatible: CheckState = CheckState.UNKNOWN
    critical_receipt_path_ready: CheckState = CheckState.UNKNOWN
    evaluation_engine_available: bool = False
    bundle_stage_path_ready: bool = False
    activation_path_state: DependencyState = DependencyState.UNKNOWN
    audit_path_state: DependencyState = DependencyState.UNKNOWN
    resource_peer_state: DependencyState = DependencyState.UNKNOWN
    active_policy_set_ref: str | None = None
    previous_valid_policy_set_ref: str | None = None
    authority_version: str | None = None
    profile_ref: str | None = None
    offline_governed_operation: bool = False
    additional_reasons: tuple[str, ...] = ()


class GovernancePolicyHealth:
    """Thread-safe bounded health state supplied by explicit probes."""

    COMPONENT_ID = "governance_policy_runtime"
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
        for name in (
            "active_policy_set_ref",
            "previous_valid_policy_set_ref",
            "authority_version",
            "profile_ref",
        ):
            value = changes.get(name)
            if value is not None and not _REFERENCE.fullmatch(str(value)):
                raise ValueError(f"{name} must be a bounded reference")
        if "additional_reasons" in changes:
            reasons = tuple(sorted(set(changes["additional_reasons"])))
            changes["additional_reasons"] = reasons
        with self._lock:
            self._state = replace(self._state, **changes)

    def snapshot(self) -> HealthSnapshot:
        with self._lock:
            state = self._state
        observed_at = _utc_time(self._clock())
        health = tuple((name, getattr(state, name)) for name in HEALTH_CHECKS)
        readiness = tuple((name, getattr(state, name)) for name in READINESS_CHECKS)
        healthy = all(value is CheckState.PASS for _, value in health)
        canonical_ready = all(value is CheckState.PASS for _, value in readiness)
        ready = healthy and canonical_ready and state.evaluation_engine_available

        available = ["health_and_readiness"]
        blocked: list[str] = []
        if state.process_responsive is CheckState.PASS and state.local_storage_accessible is CheckState.PASS:
            available.append("get_policy_set_status")
        else:
            blocked.append("get_policy_set_status")

        if ready:
            available.extend(DECISION_CAPABILITIES)
        else:
            blocked.extend(DECISION_CAPABILITIES)

        if state.bundle_stage_path_ready:
            available.append("stage_policy_bundle")
        else:
            blocked.append("stage_policy_bundle")
        if state.activation_path_state is DependencyState.AVAILABLE:
            available.extend(("activate_policy_set", "rollback_policy_set"))
        else:
            blocked.extend(("activate_policy_set", "rollback_policy_set"))
        if state.receipt_store_accessible is CheckState.PASS:
            available.append("get_decision_receipt")
        else:
            blocked.append("get_decision_receipt")

        reasons = list(state.additional_reasons)
        for name, value in health + readiness:
            if value is not CheckState.PASS:
                reasons.append(f"{name}:{value.value}")
        if not state.evaluation_engine_available:
            reasons.append("policy_evaluation_engine_unavailable")
        reasons = sorted(set(reasons))

        return HealthSnapshot(
            component_id=self.COMPONENT_ID,
            contract_version=self.CONTRACT_VERSION,
            runtime_version=self._runtime_version,
            observed_at=observed_at,
            component_state=state.component_state,
            healthy=healthy,
            ready=ready,
            health_checks=health,
            readiness_checks=readiness,
            available_capabilities=tuple(sorted(set(available))),
            blocked_capabilities=tuple(sorted(set(blocked))),
            reasons=tuple(reasons),
            active_policy_set_ref=state.active_policy_set_ref,
            previous_valid_policy_set_ref=state.previous_valid_policy_set_ref,
            authority_version=state.authority_version,
            profile_ref=state.profile_ref,
            audit_path_state=state.audit_path_state,
            activation_path_state=state.activation_path_state,
            resource_peer_state=state.resource_peer_state,
            offline_governed_operation=state.offline_governed_operation,
        )


def _utc_time(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("health clock must return a timezone-aware datetime")
    return value.astimezone(UTC)


def _format_time(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
