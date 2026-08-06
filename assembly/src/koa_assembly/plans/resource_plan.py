"""Owner-preserving resource plans for resolved services."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Iterable, Mapping

from .dependency_graph import PlanValidationError, _identifier
from .service_plan import ServicePlan


@dataclass(frozen=True, slots=True)
class ResourceEnvelope:
    """Closed resource limits; ``None`` means the contract did not set a limit."""

    cpu_millicores: int | None = None
    memory_bytes: int | None = None
    pids: int | None = None
    io_weight: int | None = None
    storage_bytes: int | None = None
    max_concurrency: int | None = None

    def __post_init__(self) -> None:
        for field_name in (
            "cpu_millicores",
            "memory_bytes",
            "pids",
            "storage_bytes",
            "max_concurrency",
        ):
            value = getattr(self, field_name)
            if value is not None and (not isinstance(value, int) or isinstance(value, bool) or value <= 0):
                raise PlanValidationError(f"{field_name} must be a positive integer or null")
        if self.io_weight is not None:
            if not isinstance(self.io_weight, int) or isinstance(self.io_weight, bool):
                raise PlanValidationError("io_weight must be an integer or null")
            if not 1 <= self.io_weight <= 10_000:
                raise PlanValidationError("io_weight must be between 1 and 10000")

    def to_dict(self) -> dict[str, int | None]:
        return {
            "cpu_millicores": self.cpu_millicores,
            "memory_bytes": self.memory_bytes,
            "pids": self.pids,
            "io_weight": self.io_weight,
            "storage_bytes": self.storage_bytes,
            "max_concurrency": self.max_concurrency,
        }


@dataclass(frozen=True, slots=True)
class ResourceAssignment:
    service_id: str
    owner_id: str
    workload_class: str
    envelope: ResourceEnvelope

    def __post_init__(self) -> None:
        object.__setattr__(self, "service_id", _identifier(self.service_id, "service_id"))
        object.__setattr__(self, "owner_id", _identifier(self.owner_id, "owner_id"))
        object.__setattr__(self, "workload_class", _identifier(self.workload_class, "workload_class"))
        if not isinstance(self.envelope, ResourceEnvelope):
            raise PlanValidationError("envelope must be a ResourceEnvelope")


@dataclass(frozen=True, slots=True)
class HostCapacity:
    cpu_millicores: int | None = None
    memory_bytes: int | None = None
    pids: int | None = None
    storage_bytes: int | None = None

    def __post_init__(self) -> None:
        for field_name in ("cpu_millicores", "memory_bytes", "pids", "storage_bytes"):
            value = getattr(self, field_name)
            if value is not None and (not isinstance(value, int) or isinstance(value, bool) or value <= 0):
                raise PlanValidationError(f"host {field_name} must be a positive integer or null")


class ResourcePlan:
    """A complete assignment of resource envelopes to enabled services."""

    def __init__(
        self,
        service_plan: ServicePlan,
        assignments: Iterable[ResourceAssignment],
        *,
        capacity: HostCapacity | None = None,
        require_all_services: bool = True,
    ) -> None:
        if not isinstance(service_plan, ServicePlan):
            raise PlanValidationError("service_plan must be a ServicePlan")
        by_service: dict[str, ResourceAssignment] = {}
        for assignment in assignments:
            if assignment.service_id in by_service:
                raise PlanValidationError(f"duplicate resource assignment: {assignment.service_id}")
            if assignment.service_id not in service_plan.active_services:
                raise PlanValidationError(
                    f"resource assignment references inactive or unknown service: {assignment.service_id}"
                )
            canonical_owner = service_plan.owner_of(assignment.service_id)
            if assignment.owner_id != canonical_owner:
                raise PlanValidationError(
                    f"resource owner mismatch for {assignment.service_id}: "
                    f"expected {canonical_owner}, got {assignment.owner_id}"
                )
            by_service[assignment.service_id] = assignment
        if require_all_services:
            missing = sorted(set(service_plan.active_services) - set(by_service))
            if missing:
                raise PlanValidationError("missing resource assignments: " + ", ".join(missing))
        self._service_plan = service_plan
        self._assignments = MappingProxyType(dict(sorted(by_service.items())))
        self._capacity = capacity
        if capacity is not None:
            self._validate_capacity(capacity)

    @property
    def assignments(self) -> Mapping[str, ResourceAssignment]:
        return self._assignments

    @property
    def capacity(self) -> HostCapacity | None:
        return self._capacity

    def totals(self) -> dict[str, int]:
        result: dict[str, int] = {}
        for field_name in ("cpu_millicores", "memory_bytes", "pids", "storage_bytes"):
            result[field_name] = sum(
                getattr(item.envelope, field_name) or 0 for item in self._assignments.values()
            )
        return result

    def _validate_capacity(self, capacity: HostCapacity) -> None:
        totals = self.totals()
        for field_name, total in totals.items():
            ceiling = getattr(capacity, field_name)
            if ceiling is not None and total > ceiling:
                raise PlanValidationError(
                    f"resource plan exceeds host {field_name}: {total} > {ceiling}"
                )

    def to_dict(self) -> dict[str, object]:
        return {
            "assignments": [
                {
                    "service_id": item.service_id,
                    "owner_id": item.owner_id,
                    "workload_class": item.workload_class,
                    "envelope": item.envelope.to_dict(),
                }
                for item in self._assignments.values()
            ],
            "totals": self.totals(),
            "capacity": (
                None
                if self._capacity is None
                else {
                    "cpu_millicores": self._capacity.cpu_millicores,
                    "memory_bytes": self._capacity.memory_bytes,
                    "pids": self._capacity.pids,
                    "storage_bytes": self._capacity.storage_bytes,
                }
            ),
        }
