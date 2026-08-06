"""Classification value objects owned by the kOA Mediatheque domain."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


def _required_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _optional_text(value: str | None, field_name: str) -> str | None:
    if value is None:
        return None
    return _required_text(value, field_name)


def _unique_texts(values: Iterable[str], field_name: str) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)):
        raise TypeError(f"{field_name} must be an iterable of strings, not a scalar")
    normalized = tuple(_required_text(value, field_name) for value in values)
    if len(set(normalized)) != len(normalized):
        raise ValueError(f"{field_name} must not contain duplicate values")
    return tuple(sorted(normalized))


@dataclass(frozen=True, slots=True, order=True)
class Collection:
    """A locally owned collection definition.

    A collection groups records for local navigation. Membership does not grant
    disclosure, publication, or access authority.
    """

    collection_id: str
    label: str
    description: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "collection_id", _required_text(self.collection_id, "collection_id"))
        object.__setattr__(self, "label", _required_text(self.label, "label"))
        object.__setattr__(self, "description", _optional_text(self.description, "description"))


@dataclass(frozen=True, slots=True, order=True)
class Dimension:
    """A locally governed classification dimension."""

    dimension_id: str
    label: str
    description: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "dimension_id", _required_text(self.dimension_id, "dimension_id"))
        object.__setattr__(self, "label", _required_text(self.label, "label"))
        object.__setattr__(self, "description", _optional_text(self.description, "description"))


@dataclass(frozen=True, slots=True, order=True)
class Tag:
    """A normalized local tag value."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", _required_text(self.value, "tag"))


@dataclass(frozen=True, slots=True, order=True)
class Relationship:
    """A typed relationship to another local media record."""

    relationship_type: str
    target_record_id: str
    note: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "relationship_type",
            _required_text(self.relationship_type, "relationship_type"),
        )
        object.__setattr__(
            self,
            "target_record_id",
            _required_text(self.target_record_id, "target_record_id"),
        )
        object.__setattr__(self, "note", _optional_text(self.note, "note"))

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "relationship_type": self.relationship_type,
            "target_record_id": self.target_record_id,
        }
        if self.note is not None:
            result["note"] = self.note
        return result


@dataclass(frozen=True, slots=True)
class Classification:
    """Canonical local classification attached to a media record version."""

    collection_ids: tuple[str, ...] = ()
    dimension_ids: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    relationships: tuple[Relationship, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "collection_ids",
            _unique_texts(self.collection_ids, "collection_ids"),
        )
        object.__setattr__(
            self,
            "dimension_ids",
            _unique_texts(self.dimension_ids, "dimension_ids"),
        )
        object.__setattr__(self, "tags", _unique_texts(self.tags, "tags"))

        relationships = tuple(self.relationships)
        if not all(isinstance(item, Relationship) for item in relationships):
            raise TypeError("relationships must contain Relationship instances")
        keys = tuple(
            (item.relationship_type, item.target_record_id, item.note or "")
            for item in relationships
        )
        if len(set(keys)) != len(keys):
            raise ValueError("relationships must not contain duplicates")
        object.__setattr__(
            self,
            "relationships",
            tuple(
                sorted(
                    relationships,
                    key=lambda item: (
                        item.relationship_type,
                        item.target_record_id,
                        item.note or "",
                    ),
                )
            ),
        )

    @classmethod
    def from_entities(
        cls,
        *,
        collections: Iterable[Collection] = (),
        dimensions: Iterable[Dimension] = (),
        tags: Iterable[Tag] = (),
        relationships: Iterable[Relationship] = (),
    ) -> Classification:
        """Build classification references without transferring entity authority."""

        return cls(
            collection_ids=tuple(item.collection_id for item in collections),
            dimension_ids=tuple(item.dimension_id for item in dimensions),
            tags=tuple(item.value for item in tags),
            relationships=tuple(relationships),
        )

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "collection_ids": list(self.collection_ids),
            "dimension_ids": list(self.dimension_ids),
            "tags": list(self.tags),
        }
        if self.relationships:
            result["relationships"] = [item.to_dict() for item in self.relationships]
        return result
