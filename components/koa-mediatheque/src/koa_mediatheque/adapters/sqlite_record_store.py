"""SQLite authoritative record store for the kOA Mediatheque."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from contextlib import closing, contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sqlite3
from typing import Any, Iterator


class RecordStoreError(RuntimeError):
    """Base error for canonical media-record persistence."""


class RecordValidationError(RecordStoreError):
    """Raised when a record violates the canonical local contract."""


class RecordConflictError(RecordStoreError):
    """Raised on optimistic revision or immutable receipt conflicts."""


@dataclass(frozen=True, slots=True)
class StoredRecord:
    record: Mapping[str, Any]
    revision: int


_RECORD_RE = re.compile(r"^koa_media_[A-Za-z0-9][A-Za-z0-9._-]*$")
_VERSION_RE = re.compile(r"^koa_media_version_[A-Za-z0-9][A-Za-z0-9._-]*$")
_DIGEST_LENGTHS = {"sha256": 64, "sha384": 96, "sha512": 128}
_RECORD_STATES = {"draft", "active", "restricted", "withdrawn", "archived", "deleted_tombstone"}
_VERSION_STATES = {"staged", "quarantined", "verified", "accepted", "superseded", "withdrawn", "corrupt"}
_AVAILABILITY = {"managed_local", "managed_remote_cache", "external_reference", "offline_unavailable", "withdrawn"}
_DISCLOSURE = {"private", "restricted", "organization", "community", "public"}
_PUBLICATION = {"prohibited", "review_required", "allowed_for_declared_targets"}
_AI_USE = {"prohibited", "metadata_candidates_only", "approved_bounded_use"}
_SOURCE_TYPES = {"created_local", "imported", "received", "captured", "derived"}
_TOP_REQUIRED = {
    "shared_frame", "record_id", "version_id", "title", "media_type", "content",
    "integrity", "classification", "rights", "provenance", "lifecycle",
}
_TOP_OPTIONAL = {"$schema", "description", "renditions", "external_publications"}
_SECRET_KEYS = {"password", "secret", "token", "credential", "credentials", "private_key"}


def _canonical_json(value: Mapping[str, Any]) -> str:
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    except (TypeError, ValueError) as exc:
        raise RecordValidationError("record must be JSON serializable") from exc


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def _require_object(container: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = container.get(key)
    if not isinstance(value, Mapping):
        raise RecordValidationError(f"{key} must be an object")
    return value


def _require_string(container: Mapping[str, Any], key: str) -> str:
    value = container.get(key)
    if not isinstance(value, str) or not value.strip():
        raise RecordValidationError(f"{key} must be a non-empty string")
    return value


def _parse_timestamp(value: str, name: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise RecordValidationError(f"{name} must be an RFC 3339 timestamp") from exc
    if parsed.tzinfo is None:
        raise RecordValidationError(f"{name} must include a timezone")
    return parsed.astimezone(timezone.utc)


def _reject_secrets(value: Any, path: str = "record") -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            normalized = str(key).lower().replace("-", "_")
            if normalized in _SECRET_KEYS:
                raise RecordValidationError(f"secret-bearing field prohibited at {path}.{key}")
            _reject_secrets(item, f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _reject_secrets(item, f"{path}[{index}]")
    elif isinstance(value, (bytes, bytearray, memoryview)):
        raise RecordValidationError(f"binary content is prohibited in record JSON at {path}")


def validate_media_record(record: Mapping[str, Any]) -> None:
    if not isinstance(record, Mapping):
        raise RecordValidationError("media record must be an object")
    missing = _TOP_REQUIRED - set(record)
    unknown = set(record) - _TOP_REQUIRED - _TOP_OPTIONAL
    if missing:
        raise RecordValidationError(f"missing required fields: {sorted(missing)}")
    if unknown:
        raise RecordValidationError(f"unknown top-level fields: {sorted(unknown)}")
    _reject_secrets(record)

    record_id = _require_string(record, "record_id")
    version_id = _require_string(record, "version_id")
    if not _RECORD_RE.fullmatch(record_id):
        raise RecordValidationError("record_id does not match the canonical pattern")
    if not _VERSION_RE.fullmatch(version_id):
        raise RecordValidationError("version_id does not match the canonical pattern")
    _require_string(record, "title")
    media_type = _require_string(record, "media_type")

    content = _require_object(record, "content")
    availability = _require_string(content, "availability")
    storage_ref = _require_string(content, "storage_ref")
    if availability not in _AVAILABILITY:
        raise RecordValidationError("unsupported content availability")
    size_bytes = content.get("size_bytes")
    if not isinstance(size_bytes, int) or isinstance(size_bytes, bool) or size_bytes < 0:
        raise RecordValidationError("content.size_bytes must be a non-negative integer")
    if availability == "managed_local" and not storage_ref.startswith("koa-blob://"):
        raise RecordValidationError("managed_local content requires a managed blob reference")

    integrity = _require_object(record, "integrity")
    algorithm = _require_string(integrity, "algorithm")
    digest = _require_string(integrity, "digest")
    if algorithm not in _DIGEST_LENGTHS or not re.fullmatch(r"[0-9a-f]+", digest):
        raise RecordValidationError("unsupported integrity identity")
    if len(digest) != _DIGEST_LENGTHS[algorithm]:
        raise RecordValidationError("digest length does not match integrity algorithm")
    _parse_timestamp(_require_string(integrity, "verified_at"), "integrity.verified_at")

    classification = _require_object(record, "classification")
    for key in ("collection_ids", "dimension_ids", "tags"):
        values = classification.get(key)
        if not isinstance(values, list) or any(not isinstance(item, str) for item in values):
            raise RecordValidationError(f"classification.{key} must be a string array")
        if len(values) != len(set(values)):
            raise RecordValidationError(f"classification.{key} must contain unique values")

    rights = _require_object(record, "rights")
    if rights.get("disclosure") not in _DISCLOSURE:
        raise RecordValidationError("unsupported rights.disclosure")
    if rights.get("publication") not in _PUBLICATION:
        raise RecordValidationError("unsupported rights.publication")
    if rights.get("ai_use") not in _AI_USE:
        raise RecordValidationError("unsupported rights.ai_use")
    if rights.get("publication") == "allowed_for_declared_targets" and not rights.get("allowed_target_ids"):
        raise RecordValidationError("declared-target publication requires allowed_target_ids")

    provenance = _require_object(record, "provenance")
    if provenance.get("source_type") not in _SOURCE_TYPES:
        raise RecordValidationError("unsupported provenance.source_type")
    _parse_timestamp(_require_string(provenance, "acquired_at"), "provenance.acquired_at")

    lifecycle = _require_object(record, "lifecycle")
    record_state = _require_string(lifecycle, "record_state")
    version_state = _require_string(lifecycle, "version_state")
    if record_state not in _RECORD_STATES or version_state not in _VERSION_STATES:
        raise RecordValidationError("unsupported lifecycle state")
    created_at = _parse_timestamp(_require_string(lifecycle, "created_at"), "lifecycle.created_at")
    updated_at = _parse_timestamp(_require_string(lifecycle, "updated_at"), "lifecycle.updated_at")
    if updated_at < created_at:
        raise RecordValidationError("lifecycle.updated_at precedes created_at")
    if version_state == "accepted" and availability in {"offline_unavailable", "withdrawn"}:
        raise RecordValidationError("accepted version must have usable declared content")

    frame = _require_object(record, "shared_frame")
    if frame.get("frame_id") != "koa-uckk-shared-mediatheque-frame":
        raise RecordValidationError("shared frame identity is invalid")
    frame_version = _require_string(frame, "frame_version")
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", frame_version):
        raise RecordValidationError("shared frame version is invalid")
    object_identity = _require_object(frame, "object_identity")
    authority_domain_id = _require_string(object_identity, "authority_domain_id")
    if object_identity.get("object_id") != record_id:
        raise RecordValidationError("shared frame object identity differs from local record identity")
    version_identity = _require_object(frame, "version_identity")
    if version_identity.get("version_id") != version_id:
        raise RecordValidationError("shared frame version identity differs from local version identity")
    frame_integrity = _require_object(frame, "integrity")
    if frame_integrity.get("algorithm") != algorithm or frame_integrity.get("digest") != digest:
        raise RecordValidationError("shared frame integrity differs from local integrity")
    frame_media = _require_object(frame, "media")
    if frame_media.get("media_type") != media_type:
        raise RecordValidationError("shared frame media type differs from local media type")
    frame_rights = _require_object(frame, "rights")
    if frame_rights.get("license_status") not in {"declared", "restricted", "unknown", "not_applicable"}:
        raise RecordValidationError("shared frame license status is invalid")
    if frame_rights.get("disclosure_status") not in {"private", "organization_private", "restricted", "shareable", "public"}:
        raise RecordValidationError("shared frame disclosure status is invalid")
    frame_provenance = _require_object(frame, "provenance")
    _require_string(frame_provenance, "source_system")
    if frame_provenance.get("acquisition_method") not in {
        "created_local", "imported_online", "imported_offline_bundle", "published_copy", "derived_local", "other_declared"
    }:
        raise RecordValidationError("shared frame acquisition method is invalid")
    frame_lifecycle = _require_object(frame, "lifecycle")
    if frame_lifecycle.get("authority_domain_id") != authority_domain_id:
        raise RecordValidationError("shared frame lifecycle authority does not match object authority")
    if frame_lifecycle.get("state") not in {
        "candidate", "quarantined", "accepted", "active", "superseded", "withdrawn", "rejected", "deleted_tombstone"
    }:
        raise RecordValidationError("shared frame lifecycle state is invalid")


class SqliteRecordStore:
    """Persist canonical records, versions and immutable publication receipts."""

    def __init__(
        self,
        database: str | os.PathLike[str],
        *,
        migration_path: str | os.PathLike[str] | None = None,
        timeout_seconds: float = 5.0,
    ) -> None:
        self.database = str(database)
        self.migration_path = Path(migration_path) if migration_path else None
        self.timeout_seconds = timeout_seconds

    def initialize(self) -> None:
        if self.migration_path is None:
            raise RecordStoreError("migration_path is required to initialize the store")
        script = self.migration_path.read_text(encoding="utf-8")
        with closing(self._connect(require_schema=False)) as connection:
            connection.executescript(script)
            violations = connection.execute("PRAGMA foreign_key_check").fetchall()
            if violations:
                raise RecordStoreError(f"foreign-key violations after migration: {violations!r}")
            integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
            if integrity != "ok":
                raise RecordStoreError(f"SQLite integrity check failed: {integrity}")
            connection.commit()

    def save(self, record: Mapping[str, Any], *, expected_revision: int | None = None) -> StoredRecord:
        validate_media_record(record)
        encoded = _canonical_json(record)
        record_id = str(record["record_id"])
        version_id = str(record["version_id"])
        content = record["content"]
        integrity = record["integrity"]
        lifecycle = record["lifecycle"]
        authority_domain = record["shared_frame"]["object_identity"]["authority_domain_id"]
        with self._transaction() as connection:
            existing = connection.execute(
                "SELECT revision, created_at FROM media_records WHERE record_id = ?", (record_id,)
            ).fetchone()
            if existing is None:
                if expected_revision not in (None, 0):
                    raise RecordConflictError("record does not exist at expected revision")
                revision = 1
                connection.execute(
                    """
                    INSERT INTO media_records(
                        record_id, current_version_id, title, media_type, record_state,
                        authority_domain_id, record_json, revision, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        record_id, version_id, record["title"], record["media_type"],
                        lifecycle["record_state"], authority_domain, encoded, revision,
                        lifecycle["created_at"], lifecycle["updated_at"],
                    ),
                )
            else:
                current_revision = int(existing["revision"])
                if expected_revision is not None and expected_revision != current_revision:
                    raise RecordConflictError("record revision conflict")
                revision = current_revision + 1
                result = connection.execute(
                    """
                    UPDATE media_records SET
                        current_version_id = ?, title = ?, media_type = ?, record_state = ?,
                        authority_domain_id = ?, record_json = ?, revision = ?, updated_at = ?
                    WHERE record_id = ? AND revision = ?
                    """,
                    (
                        version_id, record["title"], record["media_type"], lifecycle["record_state"],
                        authority_domain, encoded, revision, lifecycle["updated_at"], record_id,
                        current_revision,
                    ),
                )
                if result.rowcount != 1:
                    raise RecordConflictError("record changed concurrently")
            version_existing = connection.execute(
                """
                SELECT record_id, digest_algorithm, digest, storage_ref, size_bytes
                FROM media_versions WHERE version_id = ?
                """,
                (version_id,),
            ).fetchone()
            if version_existing is None:
                connection.execute(
                    """
                    INSERT INTO media_versions(
                        version_id, record_id, digest_algorithm, digest, storage_ref,
                        size_bytes, availability, version_state, version_json, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        version_id, record_id, integrity["algorithm"], integrity["digest"],
                        content["storage_ref"], content["size_bytes"], content["availability"],
                        lifecycle["version_state"], encoded, lifecycle["created_at"], lifecycle["updated_at"],
                    ),
                )
            else:
                immutable_identity = (
                    version_existing["record_id"],
                    version_existing["digest_algorithm"],
                    version_existing["digest"],
                    version_existing["storage_ref"],
                    int(version_existing["size_bytes"]),
                )
                requested_identity = (
                    record_id, integrity["algorithm"], integrity["digest"],
                    content["storage_ref"], int(content["size_bytes"]),
                )
                if immutable_identity != requested_identity:
                    raise RecordConflictError("an existing version's content identity cannot be rewritten")
                connection.execute(
                    """
                    UPDATE media_versions
                    SET availability = ?, version_state = ?, version_json = ?, updated_at = ?
                    WHERE version_id = ?
                    """,
                    (content["availability"], lifecycle["version_state"], encoded, lifecycle["updated_at"], version_id),
                )
        return StoredRecord(record=dict(record), revision=revision)

    def get(self, record_id: str) -> StoredRecord | None:
        with closing(self._connect()) as connection:
            row = connection.execute(
                "SELECT record_json, revision FROM media_records WHERE record_id = ?", (record_id,)
            ).fetchone()
        if row is None:
            return None
        return StoredRecord(record=json.loads(row["record_json"]), revision=int(row["revision"]))

    def get_version(self, version_id: str) -> Mapping[str, Any] | None:
        with closing(self._connect()) as connection:
            row = connection.execute(
                "SELECT version_json FROM media_versions WHERE version_id = ?", (version_id,)
            ).fetchone()
        return json.loads(row["version_json"]) if row is not None else None

    def list_records(
        self,
        *,
        record_states: Sequence[str] | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[StoredRecord]:
        if not 1 <= limit <= 1000 or offset < 0:
            raise ValueError("invalid pagination bounds")
        parameters: list[Any] = []
        where = ""
        if record_states:
            invalid = set(record_states) - _RECORD_STATES
            if invalid:
                raise ValueError(f"unsupported record states: {sorted(invalid)}")
            placeholders = ",".join("?" for _ in record_states)
            where = f" WHERE record_state IN ({placeholders})"
            parameters.extend(record_states)
        parameters.extend((limit, offset))
        with closing(self._connect()) as connection:
            rows = connection.execute(
                f"SELECT record_json, revision FROM media_records{where} ORDER BY updated_at, record_id LIMIT ? OFFSET ?",
                parameters,
            ).fetchall()
        return [StoredRecord(record=json.loads(row["record_json"]), revision=row["revision"]) for row in rows]

    def find_by_digest(self, algorithm: str, digest: str) -> list[Mapping[str, Any]]:
        if algorithm not in _DIGEST_LENGTHS or len(digest) != _DIGEST_LENGTHS[algorithm]:
            raise ValueError("invalid integrity identity")
        with closing(self._connect()) as connection:
            rows = connection.execute(
                """
                SELECT version_json FROM media_versions
                WHERE digest_algorithm = ? AND digest = ?
                ORDER BY record_id, version_id
                """,
                (algorithm, digest),
            ).fetchall()
        return [json.loads(row["version_json"]) for row in rows]

    def attach_publication_receipt(
        self,
        *,
        record_id: str,
        version_id: str,
        request_id: str,
        receipt: Mapping[str, Any],
    ) -> None:
        for name, value in {"record_id": record_id, "version_id": version_id, "request_id": request_id}.items():
            if not value.strip():
                raise RecordValidationError(f"{name} must not be empty")
        receipt_id = receipt.get("receipt_id") or receipt.get("receipt_ref")
        if not isinstance(receipt_id, str) or not receipt_id.strip():
            raise RecordValidationError("publication receipt identity is required")
        outcome = receipt.get("outcome") or receipt.get("publication_state") or receipt.get("status")
        if outcome not in {"queued", "published", "partially_published", "failed", "withdrawal_notice_sent"}:
            raise RecordValidationError("unsupported publication receipt outcome")
        target_system = receipt.get("target_system")
        if not isinstance(target_system, str) or not target_system.strip():
            destination = receipt.get("destination")
            if isinstance(destination, Mapping):
                target_system = destination.get("system_id") or destination.get("destination_id")
        if not isinstance(target_system, str) or not target_system.strip():
            raise RecordValidationError("publication target system is required")
        encoded = _canonical_json(receipt)
        with self._transaction() as connection:
            version = connection.execute(
                "SELECT record_id FROM media_versions WHERE version_id = ?", (version_id,)
            ).fetchone()
            if version is None or version["record_id"] != record_id:
                raise RecordValidationError("publication receipt references an unknown local version")
            existing = connection.execute(
                "SELECT receipt_json FROM publication_receipts WHERE receipt_id = ?", (receipt_id,)
            ).fetchone()
            if existing is not None:
                if existing["receipt_json"] != encoded:
                    raise RecordConflictError("publication receipt identity conflict")
                return
            connection.execute(
                """
                INSERT INTO publication_receipts(
                    receipt_id, request_id, record_id, version_id, target_system,
                    outcome, receipt_json, attached_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (receipt_id, request_id, record_id, version_id, target_system, outcome, encoded, _utc_now()),
            )

    def publication_receipts(self, record_id: str) -> list[Mapping[str, Any]]:
        with closing(self._connect()) as connection:
            rows = connection.execute(
                "SELECT receipt_json FROM publication_receipts WHERE record_id = ? ORDER BY attached_at, receipt_id",
                (record_id,),
            ).fetchall()
        return [json.loads(row["receipt_json"]) for row in rows]

    def integrity_check(self) -> bool:
        with closing(self._connect()) as connection:
            return connection.execute("PRAGMA integrity_check").fetchone()[0] == "ok" and not connection.execute(
                "PRAGMA foreign_key_check"
            ).fetchall()

    def backup(self, destination: str | os.PathLike[str]) -> Path:
        target = Path(destination).expanduser().resolve(strict=False)
        target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        if target.exists():
            raise RecordStoreError("backup destination already exists")
        with closing(self._connect()) as source, closing(sqlite3.connect(target)) as backup:
            source.execute("PRAGMA wal_checkpoint(FULL)")
            source.backup(backup)
            result = backup.execute("PRAGMA integrity_check").fetchone()[0]
            if result != "ok":
                raise RecordStoreError(f"backup integrity check failed: {result}")
        os.chmod(target, 0o600)
        return target

    @contextmanager
    def _transaction(self) -> Iterator[sqlite3.Connection]:
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _connect(self, *, require_schema: bool = True) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database, timeout=self.timeout_seconds)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute(f"PRAGMA busy_timeout = {int(self.timeout_seconds * 1000)}")
        if require_schema:
            present = connection.execute(
                "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'media_records'"
            ).fetchone()
            if present is None:
                connection.close()
                raise RecordStoreError("media schema is missing; apply component migrations first")
        return connection
