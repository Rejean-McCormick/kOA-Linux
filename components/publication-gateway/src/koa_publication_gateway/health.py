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
        return self.publication.ready

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
        observed_text = observed_at.isoformat().replace("+00:00", "Z")
        dependency_map = MappingProxyType(
            {
                "audit_broker": state.audit_broker,
                "governance_policy_runtime": state.governance_policy_runtime,
                "identity_and_trust": state.identity_and_trust,
                "resource_governor": state.resource_governor,
            }
        )
        dependencies = tuple(
            {
                "dependency_id": name,
                "classification": "required_component",
                "state": dependency_state.value,
                "required_for_this_class": True,
                "observed_at": observed_text,
                **(
                    {}
                    if dependency_state is DependencyState.AVAILABLE
                    else {"reason_codes": [f"{name.upper()}_{dependency_state.value.upper()}"]}
                ),
            }
            for name, dependency_state in dependency_map.items()
        )

        publication_conditions = (
            _readiness_condition(
                "startup_complete",
                "startup_completion",
                CheckState.PASS if state.startup_complete else CheckState.FAIL,
                observed_text,
            ),
            *(
                _readiness_condition(
                    name,
                    _condition_category(name),
                    value,
                    observed_text,
                )
                for name, value in readiness_checks
            ),
        )
        inspection_conditions = (
            _readiness_condition(
                "process_responsive",
                "process_liveness",
                state.process_responsive,
                observed_text,
            ),
        )
        publication_reason_codes = tuple(
            sorted({reason.upper() for reason in reasons})
        )
        if not publication_ready and not publication_reason_codes:
            publication_reason_codes = ("PUBLICATION_NOT_READY",)

        if aggregate_state is HealthState.HEALTHY:
            publication_state = (
                HealthState.HEALTHY if publication_ready else HealthState.DEGRADED
            )
        else:
            publication_state = aggregate_state

        readiness_freshness = MappingProxyType(
            {
                "source": f"health:{self.COMPONENT_ID}",
                "confidence": "direct",
                "staleness_state": "current",
                "observed_at": observed_text,
                "age_seconds": 0,
            }
        )
        contract_ref = "docs/contracts/components/publication-gateway.component.json"
        publication_readiness = Readiness(
            readiness_id="readiness:publication_gateway:governed_publication",
            component_id=self.COMPONENT_ID,
            component_instance_id=self._instance_id,
            component_contract_ref=contract_ref,
            capability_id="governed_publication",
            readiness_class=ReadinessClass.PUBLICATION,
            ready=publication_ready,
            operational_state=publication_state,
            usable_operation_classes=PUBLICATION_OPERATIONS if publication_ready else (),
            denied_operation_classes=() if publication_ready else PUBLICATION_OPERATIONS,
            conditions=publication_conditions,
            dependencies=dependencies,
            active_contract=MappingProxyType(
                {"ref": contract_ref, "version": self.CONTRACT_VERSION}
            ),
            profile_refs=state.profile_refs,
            freshness=readiness_freshness,
            observed_at=observed_at,
            reason_codes=() if publication_ready else publication_reason_codes,
            recovery_conditions=(
                "bind_explicit_publisher_and_receipt_store",
                "restore_required_authorities",
                "revalidate_queued_requests_before_delivery",
            )
            if not publication_ready
            else (),
        )
        inspection_readiness = Readiness(
            readiness_id="readiness:publication_gateway:local_inspection",
            component_id=self.COMPONENT_ID,
            component_instance_id=self._instance_id,
            component_contract_ref=contract_ref,
            capability_id="local_inspection",
            readiness_class=ReadinessClass.LOCAL_READ,
            ready=local_inspection_ready,
            operational_state=(
                HealthState.HEALTHY if local_inspection_ready else HealthState.UNAVAILABLE
            ),
            usable_operation_classes=INSPECTION_OPERATIONS if local_inspection_ready else (),
            denied_operation_classes=() if local_inspection_ready else INSPECTION_OPERATIONS,
            conditions=inspection_conditions,
            freshness=readiness_freshness,
            observed_at=observed_at,
            reason_codes=() if local_inspection_ready else ("PROCESS_UNAVAILABLE",),
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


def _condition_category(name: str) -> str:
    return {
        "audit_path_ready": "dependency_readiness",
        "destination_acknowledgement_path_ready": "execution_readiness",
        "governance_policy_runtime_ready": "policy_readiness",
        "identity_and_trust_ready": "identity_and_trust_readiness",
        "publisher_adapter_ready": "execution_readiness",
        "receipt_directory_accessible": "execution_readiness",
        "receipt_store_ready": "execution_readiness",
        "resource_envelope_ready": "dependency_readiness",
        "schema_versions_supported": "contract_readiness",
        "staging_directory_accessible": "execution_readiness",
        "trusted_time_ready": "dependency_readiness",
    }[name]


def _readiness_condition(
    condition_id: str, category: str, state: CheckState, observed_at: str
) -> dict[str, object]:
    status = {
        CheckState.PASS: "satisfied",
        CheckState.FAIL: "unsatisfied",
        CheckState.UNKNOWN: "unknown",
    }[state]
    result: dict[str, object] = {
        "condition_id": condition_id,
        "category": category,
        "required": True,
        "status": status,
        "observed_at": observed_at,
    }
    if state is not CheckState.PASS:
        result["reason_codes"] = [f"{condition_id.upper()}_{state.value.upper()}"]
    return result


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
