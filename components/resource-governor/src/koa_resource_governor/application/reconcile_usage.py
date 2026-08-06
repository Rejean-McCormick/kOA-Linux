"""Reconcile RG-IF-005 observations against one active execution binding."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation

from ..domain import ResourceDimension, ResourceLimit
from ..ports import AuditSink, Clock, UsageProbe
from . import DependencyUnavailable, InvalidRequest, audit_record, require_text, require_utc


@dataclass(frozen=True, slots=True)
class ReconcileUsageCommand:
    request_id: str
    correlation_id: str
    target_execution_ref: str
    effective_limits: tuple[ResourceLimit, ...]
    selector: Mapping[str, object]
    max_observation_age: timedelta = timedelta(minutes=5)
    receipt_required: bool = False


@dataclass(frozen=True, slots=True)
class UsageReconciliation:
    request_id: str
    observation_id: str
    target_execution_ref: str
    observed_at: datetime
    state: str
    exceeded_dimensions: tuple[str, ...]
    missing_dimensions: tuple[str, ...]
    measurements: Mapping[str, object]
    receipt_refs: tuple[str, ...] = ()
    authorizes_business_action: bool = False


class ReconcileUsage:
    """Compare observed resource metadata with declared hard boundaries."""

    operation_id = "reconcile_usage"

    def __init__(self, probe: UsageProbe, clock: Clock, audit: AuditSink) -> None:
        self._probe = probe
        self._clock = clock
        self._audit = audit

    def execute(self, command: ReconcileUsageCommand) -> UsageReconciliation:
        request_id = require_text(command.request_id, "request_id")
        correlation_id = require_text(command.correlation_id, "correlation_id")
        target = require_text(command.target_execution_ref, "target_execution_ref")
        if command.max_observation_age <= timedelta(0):
            raise InvalidRequest("max_observation_age must be positive")
        limits = tuple(command.effective_limits)
        if not limits:
            raise InvalidRequest("effective_limits must not be empty")
        try:
            raw = self._probe.observe_usage(target, **dict(command.selector))
        except Exception as exc:
            raise DependencyUnavailable(
                "resource observation is unavailable",
                reason_code="resource_observation_unavailable",
            ) from exc
        observation = _validate_observation(raw, target)
        now = require_utc(self._clock.now(), "clock.now")
        if now - observation["observed_at"] > command.max_observation_age:
            raise DependencyUnavailable("resource observation is stale", reason_code="resource_observation_stale")
        measurements = observation["measurements"]
        exceeded: list[str] = []
        missing: list[str] = []
        for limit in limits:
            observed = _measurement_for(limit.dimension, measurements)
            if observed is None:
                missing.append(limit.dimension.value)
            elif observed > Decimal(limit.hard_limit):
                exceeded.append(limit.dimension.value)
        state = "violation" if exceeded else "incomplete" if missing else "within_limits"
        receipt = self._audit.record(
            audit_record(
                event_type="usage_reconciled",
                correlation_id=correlation_id,
                occurred_at=now,
                payload={
                    "interface_id": "RG-IF-005",
                    "request_id": request_id,
                    "observation_id": observation["observation_id"],
                    "target_execution_ref": target,
                    "state": state,
                    "exceeded_dimensions": tuple(sorted(exceeded)),
                    "missing_dimensions": tuple(sorted(missing)),
                },
            ),
            required_receipt=command.receipt_required,
        )
        return UsageReconciliation(
            request_id=request_id,
            observation_id=observation["observation_id"],
            target_execution_ref=target,
            observed_at=observation["observed_at"],
            state=state,
            exceeded_dimensions=tuple(sorted(exceeded)),
            missing_dimensions=tuple(sorted(missing)),
            measurements=measurements,
            receipt_refs=(receipt,) if receipt else (),
        )


def _validate_observation(value: Mapping[str, object], target: str) -> dict[str, object]:
    if value.get("interface_id") != "RG-IF-005":
        raise InvalidRequest("usage observation has an invalid interface_id")
    if value.get("target_execution_ref") != target:
        raise InvalidRequest("usage observation target does not match the request")
    observation_id = value.get("observation_id")
    measurements = value.get("resource_measurements")
    observed_at = value.get("observed_at")
    if not isinstance(observation_id, str) or not observation_id.strip():
        raise InvalidRequest("usage observation has no observation_id")
    if not isinstance(measurements, Mapping):
        raise InvalidRequest("usage observation has no resource_measurements")
    if not isinstance(observed_at, str):
        raise InvalidRequest("usage observation has no observed_at")
    try:
        instant = datetime.fromisoformat(observed_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise InvalidRequest("usage observation timestamp is invalid") from exc
    return {
        "observation_id": observation_id,
        "measurements": dict(measurements),
        "observed_at": require_utc(instant, "observed_at"),
    }


def _measurement_for(dimension: ResourceDimension, measurements: Mapping[str, object]) -> Decimal | None:
    section = measurements.get(dimension.value)
    if not isinstance(section, Mapping):
        return None
    keys = {
        ResourceDimension.CPU: ("current_millicores",),
        ResourceDimension.MEMORY: ("current_bytes", "resident_bytes"),
        ResourceDimension.IO: ("bytes_per_second",),
        ResourceDimension.STORAGE: ("used_bytes",),
        ResourceDimension.PROCESSES: ("processes", "tasks"),
        ResourceDimension.WORKERS: ("workers",),
        ResourceDimension.CONCURRENCY: ("active", "jobs"),
        ResourceDimension.QUEUES: ("items",),
        ResourceDimension.TIME: ("elapsed_seconds", "total_seconds"),
        ResourceDimension.NETWORK: ("bytes_per_second",),
        ResourceDimension.ACCELERATORS: ("devices",),
    }[dimension]
    for key in keys:
        if key in section:
            try:
                value = Decimal(str(section[key]))
            except (InvalidOperation, ValueError) as exc:
                raise InvalidRequest(f"measurement {dimension.value}.{key} is not numeric") from exc
            if not value.is_finite() or value < 0:
                raise InvalidRequest(f"measurement {dimension.value}.{key} is invalid")
            return value
    return None
