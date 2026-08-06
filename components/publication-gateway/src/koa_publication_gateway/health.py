"""Bounded Publication Gateway health and publication readiness."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime
from enum import StrEnum
from threading import RLock
from types import MappingProxyType
from typing import Callable, Mapping

from koa_interfaces import (
    AuthoritativeOutcome,
    AvailabilityState,
    CapabilityExecutionState,
    CapabilityState,
    HealthState,
    HealthStatus,
    Readiness,
    ReadinessClass,
)


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
    "configuration_valid",
    "process_responsive",
    "runtime_directory_accessible",
    "state_directory_accessible",
)
READINESS_CHECKS = (
    "audit_path_ready",
    "destination_acknowledgement_path_ready",
    "governance_policy_runtime_ready",
    "identity_and_trust_ready",
    "publisher_adapter_ready",
    "receipt_directory_accessible",
    "receipt_store_ready",
    "resource_envelope_ready",
    "schema_versions_supported",
    "staging_directory_accessible",
    "trusted_time_ready",
)
PUBLICATION_OPERATIONS = (
    "controlled_retry",
    "publication_request",
    "revocation_or_withdrawal_notice",
)
INSPECTION_OPERATIONS = (
    "health",
    "publication_status_query",
    "queue_inspection",
)


@dataclass(frozen=True, slots=True)
class ReadinessSnapshot:
    publication: Readiness
    local_inspection: Readiness

    @property
    def accepting_publication(self) -> bool:
        return self.publication.accepting_work

    def as_dict(self) -> dict[str, object]:
        return {
            "local_inspection": self.local_inspection.to_dict(),
            "publication": self.publication.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class GatewayStatus:
    health: HealthStatus
    readiness: ReadinessSnapshot
    health_checks: tuple[tuple[str, CheckState], ...]
    readiness_checks: tuple[tuple[str, CheckState], ...]
    queue_depth: int
    inflight_publications: int

    @property
    def healthy(self) -> bool:
        return self.health.state in {HealthState.HEALTHY, HealthState.CONSTRAINED}

    @property
    def ready(self) -> bool:
        return self.readiness.accepting_publication

    def as_dict(self) -> dict[str, object]:
        return {
            "health": self.health.to_dict(),
            "health_checks": {name: value.value for name, value in self.health_checks},
            "inflight_publications": self.inflight_publications,
            "queue_depth": self.queue_depth,
            "readiness": self.readiness.as_dict(),
            "readiness_checks": {
                name: value.value for name, value in self.readiness_checks
            },
            "source_content_included": False,
        }


@dataclass(frozen=True, slots=True)
class _OperationalState:
    startup_complete: bool = False
    stopping: bool = False
    configuration_valid: CheckState = CheckState.UNKNOWN
    process_responsive: CheckState = CheckState.UNKNOWN
    state_directory_accessible: CheckState = CheckState.UNKNOWN
    runtime_directory_accessible: CheckState = CheckState.UNKNOWN
    receipt_directory_accessible: CheckState = CheckState.UNKNOWN
    staging_directory_accessible: CheckState = CheckState.UNKNOWN
    schema_versions_supported: CheckState = CheckState.UNKNOWN
    identity_and_trust: DependencyState = DependencyState.UNKNOWN
    governance_policy_runtime: DependencyState = DependencyState.UNKNOWN
    audit_broker: DependencyState = DependencyState.UNKNOWN
    resource_governor: DependencyState = DependencyState.UNKNOWN
    publisher_adapter_ready: CheckState = CheckState.UNKNOWN
    receipt_store_ready: CheckState = CheckState.UNKNOWN
    destination_acknowledgement_path_ready: CheckState = CheckState.UNKNOWN
    trusted_time_ready: CheckState = CheckState.UNKNOWN
    queue_depth: int = 0
    inflight_publications: int = 0
    audit_required: bool = True
    profile_refs: tuple[str, ...] = ()
    additional_reason_codes: tuple[str, ...] = ()


class PublicationGatewayHealth:
    """Thread-safe explicit observations; no dependency discovery is performed."""

    COMPONENT_ID = "publication_gateway"
    CONTRACT_VERSION = "1.0.0"
    SCHEMA_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        instance_id: str,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        if not instance_id.strip():
            raise ValueError("instance_id must be non-empty")
        self._instance_id = instance_id.strip()
        self._clock = clock or (lambda: datetime.now(UTC))
        self._state = _OperationalState()
        self._lock = RLock()

    def update(self, **changes: object) -> None:
        allowed = set(_OperationalState.__dataclass_fields__)
        unknown = sorted(set(changes) - allowed)
        if unknown:
            raise ValueError("unknown health fields: " + ", ".join(unknown))
        for name in ("queue_depth", "inflight_publications"):
            if name in changes:
                value = changes[name]
                if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                    raise ValueError(f"{name} must be a non-negative integer")
        if "profile_refs" in changes:
            changes["profile_refs"] = tuple(sorted(set(changes["profile_refs"])))
        if "additional_reason_codes" in changes:
            changes["additional_reason_codes"] = tuple(
                sorted(set(changes["additional_reason_codes"]))
            )
        with self._lock:
            self._state = replace(self._state, **changes)

    def snapshot(self) -> GatewayStatus:
        with self._lock:
            state = self._state
        observed_at = _utc(self._clock())
        health_checks = tuple((name, getattr(state, name)) for name in HEALTH_CHECKS)
        readiness_checks = (
            ("audit_path_ready", _audit_check(state)),
            (
                "destination_acknowledgement_path_ready",
                state.destination_acknowledgement_path_ready,
            ),
            (
                "governance_policy_runtime_ready",
                _dependency_check(state.governance_policy_runtime),
            ),
            ("identity_and_trust_ready", _dependency_check(state.identity_and_trust)),
            ("publisher_adapter_ready", state.publisher_adapter_ready),
            ("receipt_directory_accessible", state.receipt_directory_accessible),
            ("receipt_store_ready", state.receipt_store_ready),
            ("resource_envelope_ready", _dependency_check(state.resource_governor)),
            ("schema_versions_supported", state.schema_versions_supported),
            ("staging_directory_accessible", state.staging_directory_accessible),
            ("trusted_time_ready", state.trusted_time_ready),
        )
        local_healthy = all(value is CheckState.PASS for _, value in health_checks)
        publication_ready = (
            state.startup_complete
            and local_healthy
            and all(value is CheckState.PASS for _, value in readiness_checks)
        )
        local_inspection_ready = state.process_responsive is CheckState.PASS

        reasons = set(state.additional_reason_codes)
        for name, value in (*health_checks, *readiness_checks):
            if value is not CheckState.PASS:
                reasons.add(f"{name}:{value.value}")
        if not state.startup_complete:
            reasons.add("startup_incomplete")
        if state.stopping:
            reasons.add("component_stopping")

        if state.stopping:
            aggregate_state = HealthState.STOPPING
        elif not state.startup_complete:
            aggregate_state = HealthState.STARTING
        elif not local_healthy:
            aggregate_state = HealthState.UNAVAILABLE
        else:
            aggregate_state = HealthState.HEALTHY

        capabilities = (
            CapabilityState(
                capability_id="publication_gateway.local_inspection",
                health_state=(HealthState.HEALTHY if local_inspection_ready else HealthState.UNAVAILABLE),
                availability_state=(
                    AvailabilityState.AVAILABLE
                    if local_inspection_ready
                    else AvailabilityState.UNAVAILABLE
                ),
                execution_state=CapabilityExecutionState.NOT_STARTED,
                authoritative_outcome=AuthoritativeOutcome.NO_EFFECT,
                authority_effect="restricted_metadata_only",
                critical=False,
                usable_operations=INSPECTION_OPERATIONS if local_inspection_ready else (),
                denied_operations=() if local_inspection_ready else INSPECTION_OPERATIONS,
                dependency_states=MappingProxyType({}),
                reason_codes=() if local_inspection_ready else ("process_unavailable",),
            ),
            CapabilityState(
                capability_id="publication_gateway.governed_publication",
                health_state=(HealthState.HEALTHY if local_healthy else HealthState.UNAVAILABLE),
                availability_state=(
                    AvailabilityState.AVAILABLE
                    if publication_ready
                    else AvailabilityState.BLOCKED
                ),
                execution_state=CapabilityExecutionState.NOT_STARTED,
                authoritative_outcome=AuthoritativeOutcome.NO_EFFECT,
                authority_effect="publication_gateway_owned_transition_only",
                critical=True,
                usable_operations=PUBLICATION_OPERATIONS if publication_ready else (),
                denied_operations=() if publication_ready else PUBLICATION_OPERATIONS,
                dependency_states=MappingProxyType(
                    {
                        "audit_broker": state.audit_broker.value,
                        "governance_policy_runtime": state.governance_policy_runtime.value,
                        "identity_and_trust": state.identity_and_trust.value,
                        "resource_governor": state.resource_governor.value,
                    }
                ),
                reason_codes=() if publication_ready else tuple(sorted(reasons)),
            ),
        )
        health = HealthStatus(
            component_id=self.COMPONENT_ID,
            instance_id=self._instance_id,
            state=aggregate_state,
            observed_at=observed_at,
            contract_version=self.CONTRACT_VERSION,
            schema_version=self.SCHEMA_VERSION,
            capabilities=capabilities,
            startup_complete=state.startup_complete,
            freshness_seconds=0,
            reason_codes=tuple(sorted(reasons)),
            active_artifact_refs=(),
            details=MappingProxyType(
                {
                    "inflight_publications": state.inflight_publications,
                    "queue_depth": state.queue_depth,
                    "source_content_included": False,
                }
            ),
        )
        dependency_map = MappingProxyType(
            {
                "audit_broker": state.audit_broker.value,
                "governance_policy_runtime": state.governance_policy_runtime.value,
                "identity_and_trust": state.identity_and_trust.value,
                "resource_governor": state.resource_governor.value,
            }
        )
        publication_readiness = Readiness(
            component_id=self.COMPONENT_ID,
            readiness_class=ReadinessClass.PUBLICATION,
            state=HealthState.HEALTHY if publication_ready else HealthState.DEGRADED,
            accepting_work=publication_ready,
            observed_at=observed_at,
            capability_id="publication_gateway.governed_publication",
            usable_operations=PUBLICATION_OPERATIONS if publication_ready else (),
            denied_operations=() if publication_ready else PUBLICATION_OPERATIONS,
            required_dependencies=dependency_map,
            reason_codes=() if publication_ready else tuple(sorted(reasons)),
            recovery_conditions=(
                "bind_explicit_publisher_and_receipt_store",
                "restore_required_authorities",
                "revalidate_queued_requests_before_delivery",
            )
            if not publication_ready
            else (),
        )
        inspection_readiness = Readiness(
            component_id=self.COMPONENT_ID,
            readiness_class=ReadinessClass.LOCAL_READ,
            state=HealthState.HEALTHY if local_inspection_ready else HealthState.UNAVAILABLE,
            accepting_work=local_inspection_ready,
            observed_at=observed_at,
            capability_id="publication_gateway.local_inspection",
            usable_operations=INSPECTION_OPERATIONS if local_inspection_ready else (),
            denied_operations=() if local_inspection_ready else INSPECTION_OPERATIONS,
            required_dependencies=MappingProxyType({}),
            reason_codes=() if local_inspection_ready else ("process_unavailable",),
            recovery_conditions=() if local_inspection_ready else ("restore_process",),
        )
        return GatewayStatus(
            health=health,
            readiness=ReadinessSnapshot(
                publication=publication_readiness,
                local_inspection=inspection_readiness,
            ),
            health_checks=health_checks,
            readiness_checks=readiness_checks,
            queue_depth=state.queue_depth,
            inflight_publications=state.inflight_publications,
        )


def _dependency_check(state: DependencyState) -> CheckState:
    return CheckState.PASS if state is DependencyState.AVAILABLE else (
        CheckState.UNKNOWN if state is DependencyState.UNKNOWN else CheckState.FAIL
    )


def _audit_check(state: _OperationalState) -> CheckState:
    if not state.audit_required:
        return CheckState.PASS
    return _dependency_check(state.audit_broker)


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("health clock must return a timezone-aware datetime")
    return value.astimezone(UTC)
