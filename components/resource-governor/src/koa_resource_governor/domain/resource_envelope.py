"""Versioned resource envelopes and their hard-boundary invariants."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from enum import Enum
from re import compile as compile_pattern
from typing import Iterable

from .resource_claim import PriorityClass, ResourceDimension, allowed_units


_SEMVER = compile_pattern(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


class EnvelopeStatus(str, Enum):
    """Canonical lifecycle states of a resource-envelope artifact."""

    ACTIVE = "active"
    DEPRECATED = "deprecated"
    SUPERSEDED = "superseded"
    RETIRED = "retired"


class EnvelopeKind(str, Enum):
    """Canonical resource-envelope scopes from the artifact contract."""

    PROFILE_BASELINE = "profile_baseline"
    PROFILE_OVERLAY = "profile_overlay"
    NODE_CAPACITY_PARTITION = "node_capacity_partition"
    WORKSPACE_BUDGET = "workspace_budget"
    COMPONENT_BUDGET = "component_budget"
    SERVICE_INSTANCE_BUDGET = "service_instance_budget"
    JOB_BUDGET = "job_budget"
    WORKER_BUDGET = "worker_budget"
    PROCESS_GROUP_BUDGET = "process_group_budget"
    CAPABILITY_BUDGET = "capability_budget"
    QUEUE_BUDGET = "queue_budget"
    STORAGE_BUDGET = "storage_budget"
    SHARED_RESOURCE_POOL = "shared_resource_pool"


class OverloadBehavior(str, Enum):
    """Canonical default degradation behavior declared by an envelope."""

    THROTTLE_THEN_QUEUE = "throttle_then_queue"
    QUEUE_THEN_REJECT = "queue_then_reject"
    SHED_OPTIONAL_THEN_STOP = "shed_optional_then_stop"
    FAIL_JOB = "fail_job"
    PROFILE_DEFINED = "profile_defined"


class Environment(str, Enum):
    """Deployment environments recognized by the resource-envelope schema."""

    DEVELOPMENT = "development"
    TEST = "test"
    STAGING = "staging"
    PRODUCTION = "production"
    RECOVERY = "recovery"
    OFFLINE = "offline"


def _required(name: str, value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def _instant(name: str, value: datetime | None) -> datetime | None:
    if value is None:
        return None
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be a timezone-aware datetime")
    return value.astimezone(timezone.utc)


def _refs(name: str, values: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted({_required(name, value) for value in values}))


def _number(name: str, value: Decimal | int | float | str | None) -> Decimal | None:
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a finite number")
    try:
        number = value if isinstance(value, Decimal) else Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{name} must be a finite number") from exc
    if not number.is_finite():
        raise ValueError(f"{name} must be a finite number")
    return number


@dataclass(frozen=True, slots=True)
class ResourceLimit:
    """Reservation, optional soft limit, and enclosing hard limit."""

    dimension: ResourceDimension
    unit: str
    reservation: Decimal | int | float | str
    hard_limit: Decimal | int | float | str
    soft_limit: Decimal | int | float | str | None = None

    def __post_init__(self) -> None:
        dimension = ResourceDimension(self.dimension)
        unit = _required("unit", self.unit)
        reservation = _number("reservation", self.reservation)
        soft_limit = _number("soft_limit", self.soft_limit)
        hard_limit = _number("hard_limit", self.hard_limit)
        assert reservation is not None and hard_limit is not None

        if unit not in allowed_units(dimension):
            expected = ", ".join(sorted(allowed_units(dimension)))
            raise ValueError(
                f"unit {unit!r} is not registered for {dimension.value}; expected one of: {expected}"
            )
        if reservation < 0:
            raise ValueError("reservation cannot be negative")
        if hard_limit <= 0:
            raise ValueError("hard_limit must be greater than zero")
        if reservation > hard_limit:
            raise ValueError("reservation cannot exceed hard_limit")
        if soft_limit is not None:
            if soft_limit <= 0:
                raise ValueError("soft_limit must be greater than zero")
            if reservation > soft_limit:
                raise ValueError("reservation cannot exceed soft_limit")
            if soft_limit > hard_limit:
                raise ValueError("soft_limit cannot exceed hard_limit")

        object.__setattr__(self, "dimension", dimension)
        object.__setattr__(self, "unit", unit)
        object.__setattr__(self, "reservation", reservation)
        object.__setattr__(self, "soft_limit", soft_limit)
        object.__setattr__(self, "hard_limit", hard_limit)


@dataclass(frozen=True, slots=True)
class ResourceEnvelope:
    """Immutable, versioned resource boundary for one exact target.

    Numeric values come from the active profile or envelope artifact.  This
    model interprets and compares them; it never invents profile thresholds.
    """

    envelope_id: str
    version: str
    status: EnvelopeStatus
    envelope_kind: EnvelopeKind
    target_scope: str
    target_id: str
    profile_refs: tuple[str, ...]
    environment: Environment
    priority_class: PriorityClass
    priority: int
    limits: tuple[ResourceLimit, ...]
    max_concurrency: int
    queue_capacity: int
    retry_limit: int
    overload_behavior: OverloadBehavior
    effective_at: datetime
    expires_at: datetime | None = None
    parent_envelope_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        envelope_id = _required("envelope_id", self.envelope_id)
        version = _required("version", self.version)
        if not _SEMVER.fullmatch(version):
            raise ValueError("version must be a valid semantic version")

        profile_refs = _refs("profile_ref", self.profile_refs)
        if not profile_refs:
            raise ValueError("profile_refs must contain at least one active profile")
        parent_refs = _refs("parent_envelope_ref", self.parent_envelope_refs)
        if envelope_id in parent_refs:
            raise ValueError("a resource envelope cannot name itself as a parent")

        if isinstance(self.priority, bool) or not isinstance(self.priority, int):
            raise ValueError("priority must be an integer from 0 through 100")
        if not 0 <= self.priority <= 100:
            raise ValueError("priority must be an integer from 0 through 100")
        for name, value in (
            ("max_concurrency", self.max_concurrency),
            ("queue_capacity", self.queue_capacity),
            ("retry_limit", self.retry_limit),
        ):
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ValueError(f"{name} must be a non-negative integer")

        limits = tuple(self.limits)
        if not limits:
            raise ValueError("limits must contain at least one resource dimension")
        if not all(isinstance(item, ResourceLimit) for item in limits):
            raise ValueError("limits entries must be ResourceLimit values")
        dimensions = [item.dimension for item in limits]
        if len(set(dimensions)) != len(dimensions):
            raise ValueError("limits cannot contain duplicate dimensions")
        limits = tuple(sorted(limits, key=lambda item: item.dimension.value))

        effective_at = _instant("effective_at", self.effective_at)
        expires_at = _instant("expires_at", self.expires_at)
        assert effective_at is not None
        if expires_at is not None and expires_at <= effective_at:
            raise ValueError("expires_at must be later than effective_at")
        status = EnvelopeStatus(self.status)
        if status is EnvelopeStatus.ACTIVE and expires_at is not None and expires_at <= effective_at:
            raise ValueError("an active envelope must have a valid effective interval")

        object.__setattr__(self, "envelope_id", envelope_id)
        object.__setattr__(self, "version", version)
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "envelope_kind", EnvelopeKind(self.envelope_kind))
        object.__setattr__(self, "target_scope", _required("target_scope", self.target_scope))
        object.__setattr__(self, "target_id", _required("target_id", self.target_id))
        object.__setattr__(self, "profile_refs", profile_refs)
        object.__setattr__(self, "environment", Environment(self.environment))
        object.__setattr__(self, "priority_class", PriorityClass(self.priority_class))
        object.__setattr__(self, "limits", limits)
        object.__setattr__(self, "overload_behavior", OverloadBehavior(self.overload_behavior))
        object.__setattr__(self, "effective_at", effective_at)
        object.__setattr__(self, "expires_at", expires_at)
        object.__setattr__(self, "parent_envelope_refs", parent_refs)
        object.__setattr__(self, "evidence_refs", _refs("evidence_ref", self.evidence_refs))

    def is_effective_at(self, instant: datetime) -> bool:
        """Return whether this active envelope is effective at an instant."""

        at = _instant("instant", instant)
        assert at is not None
        if self.status is not EnvelopeStatus.ACTIVE or at < self.effective_at:
            return False
        return self.expires_at is None or at < self.expires_at

    def limit_for(self, dimension: ResourceDimension | str) -> ResourceLimit | None:
        """Return the declared limit for one dimension."""

        wanted = ResourceDimension(dimension)
        return next((item for item in self.limits if item.dimension is wanted), None)

    def assert_within(self, enclosing: ResourceEnvelope) -> None:
        """Reject any weakening of an enclosing hard resource boundary.

        Omitted child dimensions inherit their enclosing boundary.  Dimensions
        explicitly re-declared by the child must use the same unit and a hard
        limit no greater than the enclosing one.
        """

        if not isinstance(enclosing, ResourceEnvelope):
            raise TypeError("enclosing must be a ResourceEnvelope")
        for child_limit in self.limits:
            parent_limit = enclosing.limit_for(child_limit.dimension)
            if parent_limit is None:
                raise ValueError(
                    f"enclosing envelope has no {child_limit.dimension.value} boundary"
                )
            if child_limit.unit != parent_limit.unit:
                raise ValueError(
                    f"cannot compare {child_limit.dimension.value} limits with different units"
                )
            if child_limit.hard_limit > parent_limit.hard_limit:
                raise ValueError(
                    f"{child_limit.dimension.value} hard_limit weakens enclosing boundary"
                )
        if self.max_concurrency > enclosing.max_concurrency:
            raise ValueError("max_concurrency weakens enclosing boundary")
        if self.queue_capacity > enclosing.queue_capacity:
            raise ValueError("queue_capacity weakens enclosing boundary")
        if self.retry_limit > enclosing.retry_limit:
            raise ValueError("retry_limit weakens enclosing boundary")

    @property
    def grants_business_authority(self) -> bool:
        """Resource envelopes have no authorization effect."""

        return False
