"""Canonical local media record and shared Mediatheque frame domain model."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
import math
import re
from typing import Iterable, Mapping

from .collection import Classification, Relationship
from .provenance import Provenance, SharedProvenance
from .rendition import Integrity, Rendition
from .rights import Disclosure, Rights, SharedDisclosureStatus, SharedRights

_RECORD_ID = re.compile(r"^koa_media_[A-Za-z0-9][A-Za-z0-9._-]*$")
_VERSION_ID = re.compile(r"^koa_media_version_[A-Za-z0-9][A-Za-z0-9._-]*$")
_SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
_SHARED_FRAME_ID = "koa-uckk-shared-mediatheque-frame"


def _required_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _optional_text(value: str | None, field_name: str) -> str | None:
    return None if value is None else _required_text(value, field_name)


def _unique_texts(values: Iterable[str], field_name: str) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)):
        raise TypeError(f"{field_name} must be an iterable of strings, not a scalar")
    normalized = tuple(_required_text(value, field_name) for value in values)
    if len(set(normalized)) != len(normalized):
        raise ValueError(f"{field_name} must not contain duplicate values")
    return tuple(sorted(normalized))


def _utc_datetime(value: datetime | None, field_name: str) -> datetime | None:
    if value is None:
        return None
    if not isinstance(value, datetime):
        raise TypeError(f"{field_name} must be a datetime")
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must be timezone-aware")
    return value.astimezone(UTC)


def _timestamp(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _enum_value(value: object, enum_type: type[StrEnum], field_name: str) -> StrEnum:
    if isinstance(value, enum_type):
        return value
    try:
        return enum_type(value)  # type: ignore[arg-type]
    except (TypeError, ValueError) as exc:
        allowed = ", ".join(item.value for item in enum_type)
        raise ValueError(f"{field_name} must be one of: {allowed}") from exc


def _finite_nonnegative(value: int | float, field_name: str) -> int | float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{field_name} must be numeric")
    if not math.isfinite(value) or value < 0:
        raise ValueError(f"{field_name} must be finite and non-negative")
    return value


@dataclass(frozen=True, slots=True)
class _FrozenObject:
    items: tuple[tuple[str, object], ...]


def _freeze_json(value: object, field_name: str) -> object:
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(f"{field_name} must not contain non-finite numbers")
        return value
    if isinstance(value, Mapping):
        items: list[tuple[str, object]] = []
        for key, child in value.items():
            normalized_key = _required_text(key, f"{field_name} key")
            items.append((normalized_key, _freeze_json(child, f"{field_name}.{normalized_key}")))
        keys = [key for key, _ in items]
        if len(keys) != len(set(keys)):
            raise ValueError(f"{field_name} contains duplicate normalized keys")
        return _FrozenObject(tuple(sorted(items, key=lambda item: item[0])))
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_json(item, f"{field_name}[]") for item in value)
    raise TypeError(f"{field_name} contains a non-JSON value: {type(value).__name__}")


def _thaw_json(value: object) -> object:
    if isinstance(value, _FrozenObject):
        return {key: _thaw_json(child) for key, child in value.items}
    if isinstance(value, tuple):
        return [_thaw_json(child) for child in value]
    return value


class ContentAvailability(StrEnum):
    MANAGED_LOCAL = "managed_local"
    MANAGED_REMOTE_CACHE = "managed_remote_cache"
    EXTERNAL_REFERENCE = "external_reference"
    OFFLINE_UNAVAILABLE = "offline_unavailable"
    WITHDRAWN = "withdrawn"


@dataclass(frozen=True, slots=True)
class ContentBinding:
    availability: ContentAvailability
    storage_ref: str
    size_bytes: int
    original_filename: str | None = None
    encoding: str | None = None
    duration_seconds: float | None = None
    width: int | None = None
    height: int | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "availability",
            _enum_value(self.availability, ContentAvailability, "availability"),
        )
        object.__setattr__(self, "storage_ref", _required_text(self.storage_ref, "storage_ref"))
        if isinstance(self.size_bytes, bool) or not isinstance(self.size_bytes, int):
            raise TypeError("size_bytes must be an integer")
        if self.size_bytes < 0:
            raise ValueError("size_bytes must be non-negative")
        object.__setattr__(
            self,
            "original_filename",
            _optional_text(self.original_filename, "original_filename"),
        )
        object.__setattr__(self, "encoding", _optional_text(self.encoding, "encoding"))
        if self.duration_seconds is not None:
            duration = _finite_nonnegative(self.duration_seconds, "duration_seconds")
            object.__setattr__(self, "duration_seconds", float(duration))
        for field_name in ("width", "height"):
            value = getattr(self, field_name)
            if value is not None:
                if isinstance(value, bool) or not isinstance(value, int):
                    raise TypeError(f"{field_name} must be an integer")
                if value < 1:
                    raise ValueError(f"{field_name} must be at least 1")

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "availability": self.availability.value,
            "storage_ref": self.storage_ref,
            "size_bytes": self.size_bytes,
        }
        if self.original_filename is not None:
            result["original_filename"] = self.original_filename
        if self.encoding is not None:
            result["encoding"] = self.encoding
        if self.duration_seconds is not None:
            result["duration_seconds"] = self.duration_seconds
        if self.width is not None:
            result["width"] = self.width
        if self.height is not None:
            result["height"] = self.height
        return result


class RecordState(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    RESTRICTED = "restricted"
    WITHDRAWN = "withdrawn"
    ARCHIVED = "archived"
    DELETED_TOMBSTONE = "deleted_tombstone"


class VersionState(StrEnum):
    STAGED = "staged"
    QUARANTINED = "quarantined"
    VERIFIED = "verified"
    ACCEPTED = "accepted"
    SUPERSEDED = "superseded"
    WITHDRAWN = "withdrawn"
    CORRUPT = "corrupt"


@dataclass(frozen=True, slots=True)
class RecordLifecycle:
    record_state: RecordState
    version_state: VersionState
    created_at: datetime
    updated_at: datetime
    supersedes_version_id: str | None = None
    withdrawal_ref: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "record_state",
            _enum_value(self.record_state, RecordState, "record_state"),
        )
        object.__setattr__(
            self,
            "version_state",
            _enum_value(self.version_state, VersionState, "version_state"),
        )
        created_at = _utc_datetime(self.created_at, "created_at")
        updated_at = _utc_datetime(self.updated_at, "updated_at")
        assert created_at is not None and updated_at is not None
        if updated_at < created_at:
            raise ValueError("updated_at must not precede created_at")
        object.__setattr__(self, "created_at", created_at)
        object.__setattr__(self, "updated_at", updated_at)
        supersedes = _optional_text(self.supersedes_version_id, "supersedes_version_id")
        if supersedes is not None and not _VERSION_ID.fullmatch(supersedes):
            raise ValueError("supersedes_version_id must be a kOA media version identifier")
        object.__setattr__(self, "supersedes_version_id", supersedes)
        object.__setattr__(
            self,
            "withdrawal_ref",
            _optional_text(self.withdrawal_ref, "withdrawal_ref"),
        )
        if (
            self.record_state is RecordState.WITHDRAWN
            or self.version_state is VersionState.WITHDRAWN
        ) and self.withdrawal_ref is None:
            raise ValueError("withdrawn record or version state requires withdrawal_ref")

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "record_state": self.record_state.value,
            "version_state": self.version_state.value,
            "created_at": _timestamp(self.created_at),
            "updated_at": _timestamp(self.updated_at),
        }
        if self.supersedes_version_id is not None:
            result["supersedes_version_id"] = self.supersedes_version_id
        if self.withdrawal_ref is not None:
            result["withdrawal_ref"] = self.withdrawal_ref
        return result


class ExternalPublicationOutcome(StrEnum):
    QUEUED = "queued"
    PUBLISHED = "published"
    PARTIALLY_PUBLISHED = "partially_published"
    FAILED = "failed"
    WITHDRAWAL_NOTICE_SENT = "withdrawal_notice_sent"


@dataclass(frozen=True, slots=True)
class ExternalPublicationReference:
    """A remote-result reference that never replaces local source authority."""

    target_system: str
    package_id: str
    receipt_ref: str
    outcome: ExternalPublicationOutcome
    remote_object_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "target_system", _required_text(self.target_system, "target_system"))
        object.__setattr__(self, "package_id", _required_text(self.package_id, "package_id"))
        object.__setattr__(self, "receipt_ref", _required_text(self.receipt_ref, "receipt_ref"))
        object.__setattr__(
            self,
            "outcome",
            _enum_value(self.outcome, ExternalPublicationOutcome, "outcome"),
        )
        object.__setattr__(
            self,
            "remote_object_refs",
            _unique_texts(self.remote_object_refs, "remote_object_refs"),
        )

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "target_system": self.target_system,
            "package_id": self.package_id,
            "receipt_ref": self.receipt_ref,
            "outcome": self.outcome.value,
        }
        if self.remote_object_refs:
            result["remote_object_refs"] = list(self.remote_object_refs)
        return result


class OriginSystem(StrEnum):
    KOA_LINUX = "koa-linux"
    UCKK = "uckk"
    OTHER_DECLARED_SOURCE = "other_declared_source"


@dataclass(frozen=True, slots=True)
class SharedObjectIdentity:
    authority_domain_id: str
    object_id: str
    origin_system: OriginSystem | None = None
    external_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "authority_domain_id",
            _required_text(self.authority_domain_id, "authority_domain_id"),
        )
        object.__setattr__(self, "object_id", _required_text(self.object_id, "object_id"))
        if self.origin_system is not None:
            object.__setattr__(
                self,
                "origin_system",
                _enum_value(self.origin_system, OriginSystem, "origin_system"),
            )
        object.__setattr__(
            self,
            "external_refs",
            _unique_texts(self.external_refs, "external_refs"),
        )

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "authority_domain_id": self.authority_domain_id,
            "object_id": self.object_id,
        }
        if self.origin_system is not None:
            result["origin_system"] = self.origin_system.value
        if self.external_refs:
            result["external_refs"] = list(self.external_refs)
        return result


@dataclass(frozen=True, slots=True)
class SharedVersionIdentity:
    version_id: str
    created_at: datetime | None = None
    supersedes_version_ref: str | None = None
    source_version_ref: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "version_id", _required_text(self.version_id, "version_id"))
        object.__setattr__(self, "created_at", _utc_datetime(self.created_at, "created_at"))
        object.__setattr__(
            self,
            "supersedes_version_ref",
            _optional_text(self.supersedes_version_ref, "supersedes_version_ref"),
        )
        object.__setattr__(
            self,
            "source_version_ref",
            _optional_text(self.source_version_ref, "source_version_ref"),
        )

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {"version_id": self.version_id}
        if self.created_at is not None:
            result["created_at"] = _timestamp(self.created_at)
        if self.supersedes_version_ref is not None:
            result["supersedes_version_ref"] = self.supersedes_version_ref
        if self.source_version_ref is not None:
            result["source_version_ref"] = self.source_version_ref
        return result


@dataclass(frozen=True, slots=True)
class SharedMedia:
    media_type: str
    title: str | None = None
    description: str | None = None
    language_tags: tuple[str, ...] = ()
    accessibility: object = field(default_factory=dict)
    renditions: tuple[Rendition, ...] = ()
    collections: tuple[str, ...] = ()
    dimensions: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    relationships: tuple[Relationship, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "media_type", _required_text(self.media_type, "media_type"))
        object.__setattr__(self, "title", _optional_text(self.title, "title"))
        object.__setattr__(self, "description", _optional_text(self.description, "description"))
        object.__setattr__(
            self,
            "language_tags",
            _unique_texts(self.language_tags, "language_tags"),
        )
        object.__setattr__(self, "accessibility", _freeze_json(self.accessibility, "accessibility"))
        renditions = tuple(self.renditions)
        if not all(isinstance(item, Rendition) for item in renditions):
            raise TypeError("renditions must contain Rendition instances")
        rendition_ids = [item.rendition_id for item in renditions]
        if len(rendition_ids) != len(set(rendition_ids)):
            raise ValueError("renditions must have unique rendition_id values")
        object.__setattr__(
            self,
            "renditions",
            tuple(sorted(renditions, key=lambda item: item.rendition_id)),
        )
        object.__setattr__(self, "collections", _unique_texts(self.collections, "collections"))
        object.__setattr__(self, "dimensions", _unique_texts(self.dimensions, "dimensions"))
        object.__setattr__(self, "tags", _unique_texts(self.tags, "tags"))
        relationships = tuple(self.relationships)
        if not all(isinstance(item, Relationship) for item in relationships):
            raise TypeError("relationships must contain Relationship instances")
        relationship_keys = [
            (item.relationship_type, item.target_record_id, item.note or "")
            for item in relationships
        ]
        if len(relationship_keys) != len(set(relationship_keys)):
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

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {"media_type": self.media_type}
        if self.title is not None:
            result["title"] = self.title
        if self.description is not None:
            result["description"] = self.description
        if self.language_tags:
            result["language_tags"] = list(self.language_tags)
        accessibility = _thaw_json(self.accessibility)
        if accessibility != {}:
            result["accessibility"] = accessibility
        if self.renditions:
            result["renditions"] = [item.to_dict() for item in self.renditions]
        if self.collections:
            result["collections"] = list(self.collections)
        if self.dimensions:
            result["dimensions"] = list(self.dimensions)
        if self.tags:
            result["tags"] = list(self.tags)
        if self.relationships:
            result["relationships"] = [item.to_dict() for item in self.relationships]
        return result


class SharedLifecycleState(StrEnum):
    CANDIDATE = "candidate"
    QUARANTINED = "quarantined"
    ACCEPTED = "accepted"
    ACTIVE = "active"
    SUPERSEDED = "superseded"
    WITHDRAWN = "withdrawn"
    REJECTED = "rejected"
    DELETED_TOMBSTONE = "deleted_tombstone"


@dataclass(frozen=True, slots=True)
class SharedLifecycle:
    state: SharedLifecycleState
    authority_domain_id: str
    transitioned_at: datetime | None = None
    retention_policy_ref: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "state", _enum_value(self.state, SharedLifecycleState, "state"))
        object.__setattr__(
            self,
            "authority_domain_id",
            _required_text(self.authority_domain_id, "authority_domain_id"),
        )
        object.__setattr__(
            self,
            "transitioned_at",
            _utc_datetime(self.transitioned_at, "transitioned_at"),
        )
        object.__setattr__(
            self,
            "retention_policy_ref",
            _optional_text(self.retention_policy_ref, "retention_policy_ref"),
        )

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "state": self.state.value,
            "authority_domain_id": self.authority_domain_id,
        }
        if self.transitioned_at is not None:
            result["transitioned_at"] = _timestamp(self.transitioned_at)
        if self.retention_policy_ref is not None:
            result["retention_policy_ref"] = self.retention_policy_ref
        return result


@dataclass(frozen=True, slots=True)
class SharedFrameMapping:
    source_frame_version: str | None = None
    target_frame_version: str | None = None
    mapping_version: str | None = None
    lossless: bool | None = None
    review_required: bool | None = None
    unmapped_fields: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for field_name in ("source_frame_version", "target_frame_version"):
            value = _optional_text(getattr(self, field_name), field_name)
            if value is not None and not _SEMVER.fullmatch(value):
                raise ValueError(f"{field_name} must use semantic version form")
            object.__setattr__(self, field_name, value)
        object.__setattr__(
            self,
            "mapping_version",
            _optional_text(self.mapping_version, "mapping_version"),
        )
        if self.lossless is not None and not isinstance(self.lossless, bool):
            raise TypeError("lossless must be a boolean")
        if self.review_required is not None and not isinstance(self.review_required, bool):
            raise TypeError("review_required must be a boolean")
        object.__setattr__(
            self,
            "unmapped_fields",
            _unique_texts(self.unmapped_fields, "unmapped_fields"),
        )
        if self.lossless is True and self.unmapped_fields:
            raise ValueError("a lossless mapping cannot declare unmapped_fields")
        if self.lossless is False and self.review_required is not True:
            raise ValueError("a lossy mapping requires explicit review")

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {}
        for field_name in ("source_frame_version", "target_frame_version", "mapping_version"):
            value = getattr(self, field_name)
            if value is not None:
                result[field_name] = value
        if self.lossless is not None:
            result["lossless"] = self.lossless
        if self.review_required is not None:
            result["review_required"] = self.review_required
        if self.unmapped_fields:
            result["unmapped_fields"] = list(self.unmapped_fields)
        return result


@dataclass(frozen=True, slots=True)
class SharedMediathequeFrame:
    frame_version: str
    object_identity: SharedObjectIdentity
    version_identity: SharedVersionIdentity
    integrity: Integrity
    media: SharedMedia
    rights: SharedRights
    provenance: SharedProvenance
    lifecycle: SharedLifecycle
    mapping: SharedFrameMapping | None = None
    frame_id: str = _SHARED_FRAME_ID

    def __post_init__(self) -> None:
        if self.frame_id != _SHARED_FRAME_ID:
            raise ValueError(f"frame_id must be {_SHARED_FRAME_ID!r}")
        frame_version = _required_text(self.frame_version, "frame_version")
        if not _SEMVER.fullmatch(frame_version):
            raise ValueError("frame_version must use semantic version form")
        object.__setattr__(self, "frame_version", frame_version)
        expected_types = {
            "object_identity": SharedObjectIdentity,
            "version_identity": SharedVersionIdentity,
            "integrity": Integrity,
            "media": SharedMedia,
            "rights": SharedRights,
            "provenance": SharedProvenance,
            "lifecycle": SharedLifecycle,
        }
        for field_name, expected_type in expected_types.items():
            if not isinstance(getattr(self, field_name), expected_type):
                raise TypeError(f"{field_name} must be a {expected_type.__name__} instance")
        if self.mapping is not None and not isinstance(self.mapping, SharedFrameMapping):
            raise TypeError("mapping must be a SharedFrameMapping instance")
        if self.lifecycle.authority_domain_id != self.object_identity.authority_domain_id:
            raise ValueError("shared lifecycle and object identity must use the same authority domain")

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "frame_id": self.frame_id,
            "frame_version": self.frame_version,
            "object_identity": self.object_identity.to_dict(),
            "version_identity": self.version_identity.to_dict(),
            "integrity": self.integrity.to_dict(include_verification=False),
            "media": self.media.to_dict(),
            "rights": self.rights.to_dict(),
            "provenance": self.provenance.to_dict(),
            "lifecycle": self.lifecycle.to_dict(),
        }
        if self.mapping is not None:
            result["mapping"] = self.mapping.to_dict()
        return result


_DISCLOSURE_TO_SHARED = {
    Disclosure.PRIVATE: SharedDisclosureStatus.PRIVATE,
    Disclosure.RESTRICTED: SharedDisclosureStatus.RESTRICTED,
    Disclosure.ORGANIZATION: SharedDisclosureStatus.ORGANIZATION_PRIVATE,
    Disclosure.COMMUNITY: SharedDisclosureStatus.SHAREABLE,
    Disclosure.PUBLIC: SharedDisclosureStatus.PUBLIC,
}


@dataclass(frozen=True, slots=True)
class MediaRecord:
    """Canonical kOA-local media record and accepted version representation."""

    shared_frame: SharedMediathequeFrame
    record_id: str
    version_id: str
    title: str
    media_type: str
    content: ContentBinding
    integrity: Integrity
    classification: Classification
    rights: Rights
    provenance: Provenance
    lifecycle: RecordLifecycle
    description: str | None = None
    renditions: tuple[Rendition, ...] = ()
    external_publications: tuple[ExternalPublicationReference, ...] = ()

    def __post_init__(self) -> None:
        record_id = _required_text(self.record_id, "record_id")
        version_id = _required_text(self.version_id, "version_id")
        if not _RECORD_ID.fullmatch(record_id):
            raise ValueError("record_id must match the canonical kOA media identifier pattern")
        if not _VERSION_ID.fullmatch(version_id):
            raise ValueError("version_id must match the canonical kOA media version pattern")
        object.__setattr__(self, "record_id", record_id)
        object.__setattr__(self, "version_id", version_id)
        object.__setattr__(self, "title", _required_text(self.title, "title"))
        object.__setattr__(self, "media_type", _required_text(self.media_type, "media_type"))
        object.__setattr__(self, "description", _optional_text(self.description, "description"))

        expected_types = {
            "shared_frame": SharedMediathequeFrame,
            "content": ContentBinding,
            "integrity": Integrity,
            "classification": Classification,
            "rights": Rights,
            "provenance": Provenance,
            "lifecycle": RecordLifecycle,
        }
        for field_name, expected_type in expected_types.items():
            if not isinstance(getattr(self, field_name), expected_type):
                raise TypeError(f"{field_name} must be a {expected_type.__name__} instance")
        if not self.integrity.is_verified:
            raise ValueError("canonical local media integrity must be verified")

        renditions = tuple(self.renditions)
        if not all(isinstance(item, Rendition) for item in renditions):
            raise TypeError("renditions must contain Rendition instances")
        rendition_ids = [item.rendition_id for item in renditions]
        if len(rendition_ids) != len(set(rendition_ids)):
            raise ValueError("renditions must have unique rendition_id values")
        for rendition in renditions:
            if rendition.version_id != self.version_id:
                raise ValueError("every rendition must reference this media version_id")
        object.__setattr__(
            self,
            "renditions",
            tuple(sorted(renditions, key=lambda item: item.rendition_id)),
        )

        publications = tuple(self.external_publications)
        if not all(isinstance(item, ExternalPublicationReference) for item in publications):
            raise TypeError(
                "external_publications must contain ExternalPublicationReference instances"
            )
        publication_keys = [
            (item.target_system, item.package_id, item.receipt_ref)
            for item in publications
        ]
        if len(publication_keys) != len(set(publication_keys)):
            raise ValueError("external_publications must not contain duplicates")
        object.__setattr__(
            self,
            "external_publications",
            tuple(
                sorted(
                    publications,
                    key=lambda item: (
                        item.target_system,
                        item.package_id,
                        item.receipt_ref,
                    ),
                )
            ),
        )

        self._validate_shared_frame_binding()
        self._validate_lifecycle_content_consistency()

    def _validate_shared_frame_binding(self) -> None:
        frame = self.shared_frame
        if frame.object_identity.object_id != self.record_id:
            raise ValueError("shared frame object_id must equal the local record_id")
        if frame.object_identity.origin_system not in (None, OriginSystem.KOA_LINUX):
            raise ValueError("a local media record frame must retain kOA-Linux origin identity")
        if frame.version_identity.version_id != self.version_id:
            raise ValueError("shared frame version_id must equal the local version_id")
        if frame.integrity.algorithm is not self.integrity.algorithm:
            raise ValueError("shared frame and local integrity algorithms must match")
        if frame.integrity.digest != self.integrity.digest:
            raise ValueError("shared frame and local integrity digests must match")
        if frame.media.media_type != self.media_type:
            raise ValueError("shared frame media_type must equal the local media_type")
        if frame.media.title is not None and frame.media.title != self.title:
            raise ValueError("shared frame title must equal the local title when present")
        if frame.media.collections != self.classification.collection_ids:
            raise ValueError("shared frame collections must preserve local collection_ids")
        if frame.media.dimensions != self.classification.dimension_ids:
            raise ValueError("shared frame dimensions must preserve local dimension_ids")
        if frame.media.tags != self.classification.tags:
            raise ValueError("shared frame tags must preserve local tags")
        expected_disclosure = _DISCLOSURE_TO_SHARED[self.rights.disclosure]
        if frame.rights.disclosure_status is not expected_disclosure:
            raise ValueError("shared frame disclosure_status must preserve local disclosure")

    def _validate_lifecycle_content_consistency(self) -> None:
        if self.content.availability is ContentAvailability.WITHDRAWN and not (
            self.lifecycle.record_state
            in {RecordState.WITHDRAWN, RecordState.DELETED_TOMBSTONE}
            or self.lifecycle.version_state is VersionState.WITHDRAWN
        ):
            raise ValueError("withdrawn content requires a withdrawn or tombstoned lifecycle")
        if self.lifecycle.version_state is VersionState.ACCEPTED and not self.integrity.is_verified:
            raise ValueError("unverified content cannot become accepted")
        if self.lifecycle.version_state is VersionState.CORRUPT and self.lifecycle.record_state is RecordState.ACTIVE:
            raise ValueError("a corrupt version cannot be the active record version")

    def has_same_bytes_as(self, other: MediaRecord) -> bool:
        """Compare byte identity only; equal bytes never merge record authority."""

        if not isinstance(other, MediaRecord):
            raise TypeError("other must be a MediaRecord")
        return (
            self.integrity.algorithm is other.integrity.algorithm
            and self.integrity.digest == other.integrity.digest
        )

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "shared_frame": self.shared_frame.to_dict(),
            "record_id": self.record_id,
            "version_id": self.version_id,
            "title": self.title,
            "media_type": self.media_type,
            "content": self.content.to_dict(),
            "integrity": self.integrity.to_dict(include_verification=True),
            "classification": self.classification.to_dict(),
            "rights": self.rights.to_dict(),
            "provenance": self.provenance.to_dict(),
            "lifecycle": self.lifecycle.to_dict(),
        }
        if self.description is not None:
            result["description"] = self.description
        if self.renditions:
            result["renditions"] = [item.to_dict() for item in self.renditions]
        if self.external_publications:
            result["external_publications"] = [
                item.to_dict() for item in self.external_publications
            ]
        return result
