"""Authoritative structured-state port for kOA Mediatheque."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from types import MappingProxyType
from typing import Mapping, Protocol, runtime_checkable

from .blob_store import require_digest
from .audit_sink import require_utc

_RECORD_STATES = frozenset({"draft", "active", "restricted", "withdrawn", "archived", "deleted_tombstone"})
_VERSION_STATES = frozenset({"staged", "quarantined", "verified", "accepted", "superseded", "withdrawn", "corrupt"})
_INTEGRITY_STATES = frozenset({"pending", "verified", "failed"})


def freeze_metadata(value: Mapping[str, object]) -> Mapping[str, object]:
    def freeze(item: object) -> object:
        if item is None or isinstance(item, (str, int, float, bool)):
            return item
        if isinstance(item, Mapping):
            result: dict[str, object] = {}
            for key, nested in item.items():
                if not isinstance(key, str) or not key.strip():
                    raise ValueError("metadata keys must be non-empty strings")
                result[key] = freeze(nested)
            return MappingProxyType(dict(sorted(result.items())))
        if isinstance(item, (list, tuple)):
            return tuple(freeze(nested) for nested in item)
        raise TypeError(f"unsupported metadata value: {type(item).__name__}")

    return freeze(value)  # type: ignore[return-value]


@dataclass(frozen=True, slots=True)
class Integrity:
    algorithm: str
    digest: str

    def __post_init__(self) -> None:
        algorithm, digest = require_digest(self.algorithm, self.digest)
        object.__setattr__(self, "algorithm", algorithm)
        object.__setattr__(self, "digest", digest)


@dataclass(frozen=True, slots=True)
class MediaVersion:
    record_id: str
    version_id: str
    blob_ref: str
    media_type: str
    size_bytes: int
    integrity: Integrity
    integrity_state: str
    state: str
    metadata: Mapping[str, object]
    provenance: Mapping[str, object]
    created_at: datetime
    rendition_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name in ("record_id", "version_id", "blob_ref", "media_type"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must not be empty")
        if self.size_bytes < 0:
            raise ValueError("size_bytes must be non-negative")
        if self.integrity_state not in _INTEGRITY_STATES:
            raise ValueError(f"unsupported integrity state: {self.integrity_state}")
        if self.state not in _VERSION_STATES:
            raise ValueError(f"unsupported version state: {self.state}")
        object.__setattr__(self, "metadata", freeze_metadata(self.metadata))
        object.__setattr__(self, "provenance", freeze_metadata(self.provenance))
        object.__setattr__(self, "created_at", require_utc(self.created_at))
        object.__setattr__(self, "rendition_refs", tuple(dict.fromkeys(self.rendition_refs)))


@dataclass(frozen=True, slots=True)
class MediaRecord:
    record_id: str
    authority_domain_id: str
    current_version_id: str
    state: str
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        for name in ("record_id", "authority_domain_id", "current_version_id"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must not be empty")
        if self.state not in _RECORD_STATES:
            raise ValueError(f"unsupported record state: {self.state}")
        object.__setattr__(self, "created_at", require_utc(self.created_at))
        object.__setattr__(self, "updated_at", require_utc(self.updated_at))


@dataclass(frozen=True, slots=True)
class IngestCommit:
    idempotency_key: str
    actor_id: str
    record: MediaRecord
    version: MediaVersion
    duplicate_version_refs: tuple[str, ...]
    rights_decision_ref: str


@dataclass(frozen=True, slots=True)
class MetadataRevision:
    idempotency_key: str
    actor_id: str
    record_id: str
    source_version_id: str
    new_version_id: str
    metadata: Mapping[str, object]
    rights_decision_ref: str
    changed_at: datetime

    def __post_init__(self) -> None:
        object.__setattr__(self, "metadata", freeze_metadata(self.metadata))
        object.__setattr__(self, "changed_at", require_utc(self.changed_at))


@dataclass(frozen=True, slots=True)
class RenditionRequestRecord:
    idempotency_key: str
    actor_id: str
    record_id: str
    source_version_id: str
    rendition_id: str
    job_id: str
    job_type: str
    specification: Mapping[str, object]
    rights_decision_ref: str
    requested_at: datetime

    def __post_init__(self) -> None:
        object.__setattr__(self, "specification", freeze_metadata(self.specification))
        object.__setattr__(self, "requested_at", require_utc(self.requested_at))


@dataclass(frozen=True, slots=True)
class ExportHistoryEntry:
    export_id: str
    idempotency_key: str
    actor_id: str
    record_id: str
    version_id: str
    purpose: str
    audience: str
    destination: str
    rights_decision_ref: str
    state: str
    created_at: datetime
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.state != "candidate":
            raise ValueError("application may only create export candidates")
        object.__setattr__(self, "created_at", require_utc(self.created_at))


@dataclass(frozen=True, slots=True)
class IntegrityTransition:
    idempotency_key: str
    actor_id: str
    record_id: str
    version_id: str
    expected: Integrity
    observed: Integrity
    new_integrity_state: str
    new_version_state: str
    checked_at: datetime

    def __post_init__(self) -> None:
        if self.new_integrity_state not in {"verified", "failed"}:
            raise ValueError("integrity transition must be verified or failed")
        if self.new_version_state not in {"accepted", "corrupt"}:
            raise ValueError("version transition must be accepted or corrupt")
        object.__setattr__(self, "checked_at", require_utc(self.checked_at))


@dataclass(frozen=True, slots=True)
class TombstoneResult:
    record_id: str
    version_ids: tuple[str, ...]
    unreferenced_blob_refs: tuple[str, ...]
    preserved_evidence_refs: tuple[str, ...]


@runtime_checkable
class RecordStore(Protocol):
    """Own records, versions, transitions, history, and idempotency."""

    def get_idempotent_result(self, operation: str, idempotency_key: str) -> object | None:
        """Return a completed result for this exact operation and key."""

    def remember_idempotent_result(self, operation: str, idempotency_key: str, result: object) -> None:
        """Persist the terminal result atomically with authoritative state where possible."""

    def find_versions_by_integrity(self, integrity: Integrity) -> tuple[str, ...]:
        """Find exact byte duplicates without merging authorities or record identities."""

    def commit_ingest(self, commit: IngestCommit) -> tuple[MediaRecord, MediaVersion]:
        """Atomically create the local record and accepted version."""

    def get_record(self, record_id: str) -> MediaRecord | None:
        """Return the local authoritative record."""

    def get_version(self, record_id: str, version_id: str) -> MediaVersion | None:
        """Return the exact local version."""

    def commit_metadata_revision(self, revision: MetadataRevision) -> MediaVersion:
        """Create a new local version without rewriting history."""

    def record_rendition_request(self, request: RenditionRequestRecord) -> None:
        """Persist a requested derivation before queue submission."""

    def attach_rendition_queue_ref(self, rendition_id: str, queue_ref: str) -> None:
        """Attach the queue reference to an existing rendition request."""

    def record_export_candidate(self, entry: ExportHistoryEntry) -> None:
        """Persist local export history; this does not authorize publication."""

    def apply_integrity_transition(self, transition: IntegrityTransition) -> MediaVersion:
        """Atomically mark a version accepted or corrupt."""

    def tombstone_record(self, record_id: str, *, actor_id: str, reason: str, at: datetime) -> TombstoneResult:
        """Preserve history while making the local record unavailable."""
