"""Resource claims and the value objects carried by admission requests.

A resource claim describes bounded demand only.  It never establishes business
or policy authority for the workload that submitted it.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from enum import Enum
from typing import Iterable


class ResourceDimension(str, Enum):
    """Resource dimensions recognized by the Resource Governor contracts."""

    CPU = "cpu"
    MEMORY = "memory"
    IO = "io"
    STORAGE = "storage"
    PROCESSES = "processes"
    WORKERS = "workers"
    CONCURRENCY = "concurrency"
    QUEUES = "queues"
    TIME = "time"
    NETWORK = "network"
    ACCELERATORS = "accelerators"


class PriorityClass(str, Enum):
    """Canonical resource-ordering classes, from most protected to least."""

    CRITICAL_INTEGRITY = "critical_integrity"
    AUTHORITY_VERIFICATION = "authority_verification"
    INTERACTIVE = "interactive"
    OPERATIONAL = "operational"
    BACKGROUND = "background"
    HEAVY_BATCH = "heavy_batch"
    BEST_EFFORT = "best_effort"


# Units declared by the component contract plus the storage, concurrency and
# network dimensions present in the canonical resource-envelope artifact.
_ALLOWED_UNITS: dict[ResourceDimension, frozenset[str]] = {
    ResourceDimension.CPU: frozenset({"cores", "millicores", "quota_period"}),
    ResourceDimension.MEMORY: frozenset({"bytes", "MiB", "GiB"}),
    ResourceDimension.IO: frozenset(
        {"bytes_per_second", "operations_per_second", "weight"}
    ),
    ResourceDimension.STORAGE: frozenset({"bytes", "MiB", "GiB"}),
    ResourceDimension.PROCESSES: frozenset(
        {"processes", "threads", "file_descriptors"}
    ),
    ResourceDimension.WORKERS: frozenset({"workers", "jobs"}),
    ResourceDimension.CONCURRENCY: frozenset({"workers", "jobs", "items"}),
    ResourceDimension.QUEUES: frozenset({"items", "bytes", "age"}),
    ResourceDimension.TIME: frozenset({"seconds", "minutes"}),
    ResourceDimension.NETWORK: frozenset(
        {"bytes_per_second", "connections", "listeners", "queries_per_second"}
    ),
    ResourceDimension.ACCELERATORS: frozenset(
        {"devices", "fractions", "memory"}
    ),
}


def _required(name: str, value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def _optional(name: str, value: str | None) -> str | None:
    if value is None:
        return None
    return _required(name, value)


def _instant(name: str, value: datetime | None) -> datetime | None:
    if value is None:
        return None
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be a timezone-aware datetime")
    return value.astimezone(timezone.utc)


def _refs(name: str, values: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted({_required(name, value) for value in values}))


def _number(name: str, value: Decimal | int | float | str) -> Decimal:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a finite number")
    try:
        number = value if isinstance(value, Decimal) else Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{name} must be a finite number") from exc
    if not number.is_finite():
        raise ValueError(f"{name} must be a finite number")
    return number


def allowed_units(dimension: ResourceDimension | str) -> frozenset[str]:
    """Return the closed set of registered units for a dimension."""

    return _ALLOWED_UNITS[ResourceDimension(dimension)]


@dataclass(frozen=True, slots=True)
class ResourceRequest:
    """A reservation and hard limit requested in one resource dimension."""

    dimension: ResourceDimension
    unit: str
    reservation: Decimal | int | float | str
    limit: Decimal | int | float | str

    def __post_init__(self) -> None:
        dimension = ResourceDimension(self.dimension)
        unit = _required("unit", self.unit)
        reservation = _number("reservation", self.reservation)
        limit = _number("limit", self.limit)

        if unit not in allowed_units(dimension):
            expected = ", ".join(sorted(allowed_units(dimension)))
            raise ValueError(
                f"unit {unit!r} is not registered for {dimension.value}; expected one of: {expected}"
            )
        if reservation < 0:
            raise ValueError("reservation cannot be negative")
        if limit <= 0:
            raise ValueError("limit must be greater than zero")
        if reservation > limit:
            raise ValueError("reservation cannot exceed limit")

        object.__setattr__(self, "dimension", dimension)
        object.__setattr__(self, "unit", unit)
        object.__setattr__(self, "reservation", reservation)
        object.__setattr__(self, "limit", limit)


@dataclass(frozen=True, slots=True)
class ResourceClaim:
    """Immutable workload resource request used as admission input.

    The stable ``request_id`` is also the idempotent identity of the request.
    ``policy_decision_ref`` can prove a separate policy decision, but its
    presence does not force resource admission.
    """

    request_id: str
    workload_owner_ref: str
    workload_class: str
    target_scope: str
    resource_request: tuple[ResourceRequest, ...]
    criticality: PriorityClass
    priority: int
    requested_at: datetime
    deadline: datetime | None = None
    expires_at: datetime | None = None
    queue_policy_ref: str | None = None
    policy_decision_ref: str | None = None
    exception_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "request_id", _required("request_id", self.request_id))
        object.__setattr__(
            self, "workload_owner_ref", _required("workload_owner_ref", self.workload_owner_ref)
        )
        object.__setattr__(
            self, "workload_class", _required("workload_class", self.workload_class)
        )
        object.__setattr__(self, "target_scope", _required("target_scope", self.target_scope))
        object.__setattr__(self, "criticality", PriorityClass(self.criticality))

        if isinstance(self.priority, bool) or not isinstance(self.priority, int):
            raise ValueError("priority must be an integer from 0 through 100")
        if not 0 <= self.priority <= 100:
            raise ValueError("priority must be an integer from 0 through 100")

        requested_at = _instant("requested_at", self.requested_at)
        deadline = _instant("deadline", self.deadline)
        expires_at = _instant("expires_at", self.expires_at)
        assert requested_at is not None
        if deadline is not None and deadline <= requested_at:
            raise ValueError("deadline must be later than requested_at")
        if expires_at is not None and expires_at <= requested_at:
            raise ValueError("expires_at must be later than requested_at")
        if deadline is not None and expires_at is not None and deadline > expires_at:
            raise ValueError("deadline cannot be later than expires_at")

        requests = tuple(self.resource_request)
        if not requests:
            raise ValueError("resource_request must contain at least one resource dimension")
        if not all(isinstance(item, ResourceRequest) for item in requests):
            raise ValueError("resource_request entries must be ResourceRequest values")
        dimensions = [item.dimension for item in requests]
        if len(set(dimensions)) != len(dimensions):
            raise ValueError("resource_request cannot contain duplicate dimensions")
        requests = tuple(sorted(requests, key=lambda item: item.dimension.value))

        object.__setattr__(self, "resource_request", requests)
        object.__setattr__(self, "requested_at", requested_at)
        object.__setattr__(self, "deadline", deadline)
        object.__setattr__(self, "expires_at", expires_at)
        object.__setattr__(
            self, "queue_policy_ref", _optional("queue_policy_ref", self.queue_policy_ref)
        )
        object.__setattr__(
            self,
            "policy_decision_ref",
            _optional("policy_decision_ref", self.policy_decision_ref),
        )
        object.__setattr__(self, "exception_refs", _refs("exception_ref", self.exception_refs))

    def is_expired_at(self, instant: datetime) -> bool:
        """Return whether the claim is expired at an exact instant."""

        at = _instant("instant", instant)
        assert at is not None
        return self.expires_at is not None and at >= self.expires_at

    def request_for(self, dimension: ResourceDimension | str) -> ResourceRequest | None:
        """Return the request for one dimension without performing admission."""

        wanted = ResourceDimension(dimension)
        return next((item for item in self.resource_request if item.dimension is wanted), None)

    @property
    def grants_business_authority(self) -> bool:
        """Resource claims never grant authority for the workload action."""

        return False
