"""Backup coverage and deterministic restore-order plans."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Iterable, Mapping

from .dependency_graph import DependencyGraph, DependencyNode, PlanValidationError, _identifier
from .storage_plan import StoragePlan


_METHODS = frozenset({"snapshot", "logical_export", "file_copy", "artifact_reference"})
_CONSISTENCY = frozenset({"application_consistent", "filesystem_consistent", "immutable"})
_REQUIRED_COVERAGE_CLASSES = frozenset({"authoritative", "audit_or_evidence"})
_EXCLUDED_SOURCE_CLASSES = frozenset({"cache", "projection", "replica", "temporary", "backup"})


@dataclass(frozen=True, slots=True)
class BackupItem:
    backup_id: str
    source_storage_id: str
    target_storage_id: str
    owner_id: str
    method: str
    consistency: str
    restore_after: tuple[str, ...] = field(default_factory=tuple)
    offline_copy_required: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "backup_id", _identifier(self.backup_id, "backup_id"))
        object.__setattr__(
            self, "source_storage_id", _identifier(self.source_storage_id, "source_storage_id")
        )
        object.__setattr__(
            self, "target_storage_id", _identifier(self.target_storage_id, "target_storage_id")
        )
        object.__setattr__(self, "owner_id", _identifier(self.owner_id, "owner_id"))
        method = _identifier(self.method, "method")
        consistency = _identifier(self.consistency, "consistency")
        if method not in _METHODS:
            raise PlanValidationError(f"unsupported backup method: {method}")
        if consistency not in _CONSISTENCY:
            raise PlanValidationError(f"unsupported backup consistency: {consistency}")
        dependencies = tuple(sorted({_identifier(item, "restore_after") for item in self.restore_after}))
        if self.backup_id in dependencies:
            raise PlanValidationError(f"backup item {self.backup_id} cannot depend on itself")
        if not isinstance(self.offline_copy_required, bool):
            raise PlanValidationError("offline_copy_required must be boolean")
        object.__setattr__(self, "method", method)
        object.__setattr__(self, "consistency", consistency)
        object.__setattr__(self, "restore_after", dependencies)


class BackupPlan:
    """Owner-preserving backup inventory with an acyclic restore order."""

    def __init__(
        self,
        storage_plan: StoragePlan,
        items: Iterable[BackupItem],
        *,
        require_authoritative_coverage: bool = True,
    ) -> None:
        if not isinstance(storage_plan, StoragePlan):
            raise PlanValidationError("storage_plan must be a StoragePlan")
        by_id: dict[str, BackupItem] = {}
        covered_sources: set[str] = set()
        for item in items:
            if item.backup_id in by_id:
                raise PlanValidationError(f"duplicate backup item: {item.backup_id}")
            source = storage_plan.boundaries.get(item.source_storage_id)
            target = storage_plan.boundaries.get(item.target_storage_id)
            if source is None:
                raise PlanValidationError(
                    f"backup {item.backup_id} references unknown source {item.source_storage_id}"
                )
            if target is None:
                raise PlanValidationError(
                    f"backup {item.backup_id} references unknown target {item.target_storage_id}"
                )
            if source.storage_class in _EXCLUDED_SOURCE_CLASSES:
                raise PlanValidationError(
                    f"storage class {source.storage_class} is not an authoritative backup source"
                )
            if target.storage_class != "backup":
                raise PlanValidationError(f"backup target {target.storage_id} is not class 'backup'")
            if source.owner_id != item.owner_id or target.owner_id != item.owner_id:
                raise PlanValidationError(f"backup {item.backup_id} changes storage ownership")
            if target.source_storage_id != source.storage_id:
                raise PlanValidationError(
                    f"backup target {target.storage_id} is not bound to source {source.storage_id}"
                )
            by_id[item.backup_id] = item
            covered_sources.add(source.storage_id)
        if not by_id:
            raise PlanValidationError("backup plan must contain at least one backup item")
        if require_authoritative_coverage:
            required = {
                item.storage_id
                for item in storage_plan.boundaries.values()
                if item.storage_class in _REQUIRED_COVERAGE_CLASSES
            }
            missing = sorted(required - covered_sources)
            if missing:
                raise PlanValidationError("missing backup coverage: " + ", ".join(missing))
        graph = DependencyGraph(
            DependencyNode(
                node_id=item.backup_id,
                owner_id=item.owner_id,
                dependencies=item.restore_after,
                kind="backup",
            )
            for item in by_id.values()
        )
        self._items = MappingProxyType(dict(sorted(by_id.items())))
        self._graph = graph

    @property
    def items(self) -> Mapping[str, BackupItem]:
        return self._items

    @property
    def restore_order(self) -> tuple[str, ...]:
        return self._graph.order

    def to_dict(self) -> dict[str, object]:
        return {
            "items": [
                {
                    "backup_id": item.backup_id,
                    "source_storage_id": item.source_storage_id,
                    "target_storage_id": item.target_storage_id,
                    "owner_id": item.owner_id,
                    "method": item.method,
                    "consistency": item.consistency,
                    "restore_after": list(item.restore_after),
                    "offline_copy_required": item.offline_copy_required,
                }
                for item in self._items.values()
            ],
            "restore_order": list(self.restore_order),
        }
