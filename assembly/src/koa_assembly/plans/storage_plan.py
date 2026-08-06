"""Storage boundaries that preserve one authoritative owner per data set."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import PurePosixPath
from types import MappingProxyType
from typing import Iterable, Mapping

from .dependency_graph import PlanValidationError, _identifier


_STORAGE_CLASSES = frozenset(
    {
        "authoritative",
        "canonical_artifact",
        "audit_or_evidence",
        "replica",
        "projection",
        "cache",
        "backup",
        "archive",
        "workspace",
        "temporary",
        "external_managed",
    }
)
_SOURCE_REQUIRED = frozenset({"replica", "projection", "cache", "backup", "archive"})
_NON_AUTHORITATIVE = frozenset({"replica", "projection", "cache", "backup", "archive", "temporary"})


@dataclass(frozen=True, slots=True)
class StorageBoundary:
    storage_id: str
    owner_id: str
    storage_class: str
    path: str
    writer_owner_ids: tuple[str, ...] = field(default_factory=tuple)
    source_storage_id: str | None = None
    persistent: bool = True
    encrypted: bool = False
    backup_policy_id: str | None = None

    def __post_init__(self) -> None:
        storage_id = _identifier(self.storage_id, "storage_id")
        owner_id = _identifier(self.owner_id, "owner_id")
        storage_class = _identifier(self.storage_class, "storage_class")
        if storage_class not in _STORAGE_CLASSES:
            raise PlanValidationError(f"unsupported storage class: {storage_class}")
        path = _absolute_path(self.path)
        writers = tuple(sorted({_identifier(item, "writer_owner_id") for item in self.writer_owner_ids}))
        source = self.source_storage_id
        if source is not None:
            source = _identifier(source, "source_storage_id")
        if storage_class in _SOURCE_REQUIRED and source is None:
            raise PlanValidationError(f"{storage_class} storage {storage_id} requires source_storage_id")
        if storage_class not in _SOURCE_REQUIRED and source is not None:
            raise PlanValidationError(
                f"{storage_class} storage {storage_id} must not declare source_storage_id"
            )
        if source == storage_id:
            raise PlanValidationError(f"storage {storage_id} cannot derive from itself")
        if storage_class in {"authoritative", "workspace", "external_managed"}:
            if writers != (owner_id,):
                raise PlanValidationError(
                    f"{storage_class} storage {storage_id} must have exactly its owner as writer"
                )
        elif storage_class in {"canonical_artifact", "audit_or_evidence"}:
            if owner_id not in writers:
                raise PlanValidationError(f"storage owner {owner_id} must be an allowed writer")
        elif storage_class in _NON_AUTHORITATIVE and owner_id in writers:
            raise PlanValidationError(
                f"non-authoritative storage {storage_id} cannot grant ordinary owner write-back"
            )
        if storage_class == "temporary" and self.persistent:
            raise PlanValidationError("temporary storage must not be persistent")
        backup_policy = self.backup_policy_id
        if backup_policy is not None:
            backup_policy = _identifier(backup_policy, "backup_policy_id")
        if not isinstance(self.persistent, bool) or not isinstance(self.encrypted, bool):
            raise PlanValidationError("persistent and encrypted must be boolean")
        object.__setattr__(self, "storage_id", storage_id)
        object.__setattr__(self, "owner_id", owner_id)
        object.__setattr__(self, "storage_class", storage_class)
        object.__setattr__(self, "path", path)
        object.__setattr__(self, "writer_owner_ids", writers)
        object.__setattr__(self, "source_storage_id", source)
        object.__setattr__(self, "backup_policy_id", backup_policy)


class StoragePlan:
    """Closed storage inventory with non-overlapping writable authority."""

    def __init__(self, boundaries: Iterable[StorageBoundary]) -> None:
        by_id: dict[str, StorageBoundary] = {}
        for boundary in boundaries:
            if boundary.storage_id in by_id:
                raise PlanValidationError(f"duplicate storage boundary: {boundary.storage_id}")
            by_id[boundary.storage_id] = boundary
        if not by_id:
            raise PlanValidationError("storage plan must contain at least one boundary")
        for boundary in by_id.values():
            source_id = boundary.source_storage_id
            if source_id is None:
                continue
            source = by_id.get(source_id)
            if source is None:
                raise PlanValidationError(
                    f"storage {boundary.storage_id} references unknown source {source_id}"
                )
            if boundary.owner_id != source.owner_id:
                raise PlanValidationError(
                    f"derived storage {boundary.storage_id} changes owner from "
                    f"{source.owner_id} to {boundary.owner_id}"
                )
        self._validate_paths(by_id.values())
        self._boundaries = MappingProxyType(dict(sorted(by_id.items())))

    @property
    def boundaries(self) -> Mapping[str, StorageBoundary]:
        return self._boundaries

    def authoritative_for(self, owner_id: str) -> tuple[StorageBoundary, ...]:
        owner_id = _identifier(owner_id, "owner_id")
        return tuple(
            boundary
            for boundary in self._boundaries.values()
            if boundary.owner_id == owner_id and boundary.storage_class == "authoritative"
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "boundaries": [
                {
                    "storage_id": item.storage_id,
                    "owner_id": item.owner_id,
                    "storage_class": item.storage_class,
                    "path": item.path,
                    "writer_owner_ids": list(item.writer_owner_ids),
                    "source_storage_id": item.source_storage_id,
                    "persistent": item.persistent,
                    "encrypted": item.encrypted,
                    "backup_policy_id": item.backup_policy_id,
                }
                for item in self._boundaries.values()
            ]
        }

    @staticmethod
    def _validate_paths(boundaries: Iterable[StorageBoundary]) -> None:
        ordered = sorted(boundaries, key=lambda item: item.path)
        for index, left in enumerate(ordered):
            left_path = PurePosixPath(left.path)
            for right in ordered[index + 1 :]:
                right_path = PurePosixPath(right.path)
                if not (_contains(left_path, right_path) or _contains(right_path, left_path)):
                    continue
                if left.owner_id != right.owner_id and (
                    left.writer_owner_ids or right.writer_owner_ids
                ):
                    raise PlanValidationError(
                        f"overlapping writable storage boundaries with different owners: "
                        f"{left.storage_id} ({left.path}) and {right.storage_id} ({right.path})"
                    )


def _absolute_path(value: str) -> str:
    if not isinstance(value, str) or not value:
        raise PlanValidationError("storage path must be a non-empty string")
    path = PurePosixPath(value)
    if not path.is_absolute():
        raise PlanValidationError(f"storage path must be absolute: {value}")
    if ".." in path.parts or "." in path.parts:
        raise PlanValidationError(f"storage path must be normalized: {value}")
    normalized = str(path)
    if normalized != value or normalized == "/":
        raise PlanValidationError(f"storage path must be normalized and non-root: {value}")
    return normalized


def _contains(parent: PurePosixPath, child: PurePosixPath) -> bool:
    return parent == child or parent in child.parents
