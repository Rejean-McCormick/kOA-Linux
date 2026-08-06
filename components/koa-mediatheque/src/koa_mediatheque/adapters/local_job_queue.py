"""Durable bounded local work queue with explicit leases and dead letters."""

from __future__ import annotations

from collections.abc import Mapping
from contextlib import closing
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import json
import sqlite3
from typing import Any
import uuid


class JobQueueError(RuntimeError):
    """Raised for invalid or conflicting local queue operations."""


@dataclass(frozen=True, slots=True)
class LocalJob:
    job_id: str
    queue_id: str
    job_kind: str
    subject_ref: str
    payload: Mapping[str, Any]
    payload_digest: str
    state: str
    priority: int
    attempt_count: int
    max_attempts: int
    available_at: str
    lease_owner: str | None
    leased_until: str | None
    idempotency_key: str
    result: Mapping[str, Any] | None
    last_error_code: str | None
    last_error_summary: str | None
    created_at: str
    updated_at: str


_FORBIDDEN_PAYLOAD_KEYS = {
    "content_bytes",
    "media_bytes",
    "raw_content",
    "blob_bytes",
    "private_key",
    "password",
    "secret",
    "token",
    "credential",
}
_JOB_STATES = frozenset({"queued", "leased", "succeeded", "failed", "dead_letter", "cancelled"})


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _format_time(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def _parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def _canonical_json(value: Mapping[str, Any], *, maximum_bytes: int) -> tuple[str, str]:
    _validate_payload(value)
    try:
        encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    except (TypeError, ValueError) as exc:
        raise JobQueueError("job payload must be JSON serializable") from exc
    raw = encoded.encode("utf-8")
    if len(raw) > maximum_bytes:
        raise JobQueueError("job payload exceeds the queue envelope; use a payload reference")
    return encoded, f"sha256:{hashlib.sha256(raw).hexdigest()}"


def _validate_payload(value: Any, path: str = "payload") -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            normalized = str(key).lower().replace("-", "_")
            if normalized in _FORBIDDEN_PAYLOAD_KEYS:
                raise JobQueueError(f"inline sensitive or binary payload prohibited at {path}.{key}")
            _validate_payload(item, f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _validate_payload(item, f"{path}[{index}]")
    elif isinstance(value, (bytes, bytearray, memoryview)):
        raise JobQueueError(f"inline binary payload prohibited at {path}")


class LocalJobQueue:
    """SQLite queue without hidden worker threads or implicit replay."""

    def __init__(
        self,
        database: str,
        *,
        queue_id: str = "koa_mediatheque",
        maximum_payload_bytes: int = 64 * 1024,
        timeout_seconds: float = 5.0,
    ) -> None:
        if not queue_id.strip():
            raise ValueError("queue_id must not be empty")
        if maximum_payload_bytes < 1024:
            raise ValueError("maximum_payload_bytes is too small")
        self.database = database
        self.queue_id = queue_id
        self.maximum_payload_bytes = maximum_payload_bytes
        self.timeout_seconds = timeout_seconds

    def enqueue(
        self,
        *,
        job_kind: str,
        subject_ref: str,
        payload: Mapping[str, Any],
        idempotency_key: str,
        priority: int = 100,
        max_attempts: int = 3,
        available_at: datetime | None = None,
    ) -> LocalJob:
        for name, value in {
            "job_kind": job_kind,
            "subject_ref": subject_ref,
            "idempotency_key": idempotency_key,
        }.items():
            if not isinstance(value, str) or not value.strip():
                raise JobQueueError(f"{name} must be a non-empty string")
        if not 0 <= priority <= 1000:
            raise JobQueueError("priority must be between 0 and 1000")
        if not 1 <= max_attempts <= 100:
            raise JobQueueError("max_attempts must be between 1 and 100")
        payload_json, payload_digest = _canonical_json(
            payload, maximum_bytes=self.maximum_payload_bytes
        )
        now = _utc_now()
        ready = available_at or now
        job_id = f"koa_job_{uuid.uuid4().hex}"
        with closing(self._connect()) as connection:
            connection.execute("BEGIN IMMEDIATE")
            existing = connection.execute(
                "SELECT * FROM local_jobs WHERE queue_id = ? AND idempotency_key = ?",
                (self.queue_id, idempotency_key),
            ).fetchone()
            if existing is not None:
                if (
                    existing["job_kind"] != job_kind
                    or existing["subject_ref"] != subject_ref
                    or existing["payload_digest"] != payload_digest
                ):
                    raise JobQueueError("idempotency key was reused for different work")
                connection.commit()
                return self._row_to_job(existing)
            connection.execute(
                """
                INSERT INTO local_jobs(
                    job_id, queue_id, job_kind, subject_ref, payload_json,
                    payload_digest, state, priority, attempt_count, max_attempts,
                    available_at, idempotency_key, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, 'queued', ?, 0, ?, ?, ?, ?, ?)
                """,
                (
                    job_id,
                    self.queue_id,
                    job_kind,
                    subject_ref,
                    payload_json,
                    payload_digest,
                    priority,
                    max_attempts,
                    _format_time(ready),
                    idempotency_key,
                    _format_time(now),
                    _format_time(now),
                ),
            )
            row = connection.execute("SELECT * FROM local_jobs WHERE job_id = ?", (job_id,)).fetchone()
            connection.commit()
            if row is None:
                raise JobQueueError("enqueued job could not be read back")
            return self._row_to_job(row)

    def claim(self, *, lease_owner: str, lease_seconds: int = 60) -> LocalJob | None:
        if not lease_owner.strip():
            raise JobQueueError("lease_owner must not be empty")
        if not 1 <= lease_seconds <= 86400:
            raise JobQueueError("lease_seconds is outside the allowed range")
        now = _utc_now()
        leased_until = now + timedelta(seconds=lease_seconds)
        with closing(self._connect()) as connection:
            connection.execute("BEGIN IMMEDIATE")
            self._release_expired_in_transaction(connection, now)
            row = connection.execute(
                """
                SELECT * FROM local_jobs
                WHERE queue_id = ? AND state = 'queued' AND available_at <= ?
                ORDER BY priority ASC, created_at ASC, job_id ASC
                LIMIT 1
                """,
                (self.queue_id, _format_time(now)),
            ).fetchone()
            if row is None:
                connection.commit()
                return None
            updated = connection.execute(
                """
                UPDATE local_jobs
                SET state = 'leased', lease_owner = ?, leased_until = ?, updated_at = ?
                WHERE job_id = ? AND state = 'queued'
                """,
                (lease_owner, _format_time(leased_until), _format_time(now), row["job_id"]),
            )
            if updated.rowcount != 1:
                connection.rollback()
                return None
            claimed = connection.execute(
                "SELECT * FROM local_jobs WHERE job_id = ?", (row["job_id"],)
            ).fetchone()
            connection.commit()
            if claimed is None:
                raise JobQueueError("claimed job could not be read back")
            return self._row_to_job(claimed)

    def complete(
        self, job_id: str, *, lease_owner: str, result: Mapping[str, Any] | None = None
    ) -> LocalJob:
        result_json = None
        if result is not None:
            result_json, _ = _canonical_json(result, maximum_bytes=self.maximum_payload_bytes)
        return self._finish_lease(
            job_id,
            lease_owner=lease_owner,
            state="succeeded",
            result_json=result_json,
            error_code=None,
            error_summary=None,
        )

    def fail(
        self,
        job_id: str,
        *,
        lease_owner: str,
        error_code: str,
        error_summary: str,
        retry_delay_seconds: int = 0,
        permanent: bool = False,
    ) -> LocalJob:
        if not error_code.strip() or not error_summary.strip():
            raise JobQueueError("failure code and summary are required")
        if not 0 <= retry_delay_seconds <= 604800:
            raise JobQueueError("retry delay is outside the allowed range")
        now = _utc_now()
        with closing(self._connect()) as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute("SELECT * FROM local_jobs WHERE job_id = ?", (job_id,)).fetchone()
            self._require_lease(row, lease_owner)
            attempt_count = int(row["attempt_count"]) + 1
            exhausted = attempt_count >= int(row["max_attempts"])
            next_state = "dead_letter" if permanent or exhausted else "queued"
            available_at = now + timedelta(seconds=retry_delay_seconds)
            connection.execute(
                """
                UPDATE local_jobs
                SET state = ?, attempt_count = ?, available_at = ?, lease_owner = NULL,
                    leased_until = NULL, last_error_code = ?, last_error_summary = ?, updated_at = ?
                WHERE job_id = ?
                """,
                (
                    next_state,
                    attempt_count,
                    _format_time(available_at),
                    error_code,
                    error_summary[:2048],
                    _format_time(now),
                    job_id,
                ),
            )
            result = connection.execute("SELECT * FROM local_jobs WHERE job_id = ?", (job_id,)).fetchone()
            connection.commit()
            if result is None:
                raise JobQueueError("updated job could not be read back")
            return self._row_to_job(result)

    def cancel(self, job_id: str) -> LocalJob:
        now = _format_time(_utc_now())
        with closing(self._connect()) as connection:
            row = connection.execute("SELECT * FROM local_jobs WHERE job_id = ?", (job_id,)).fetchone()
            if row is None:
                raise JobQueueError("job not found")
            if row["state"] not in {"queued", "failed"}:
                raise JobQueueError("only non-leased pending work can be cancelled")
            connection.execute(
                "UPDATE local_jobs SET state = 'cancelled', updated_at = ? WHERE job_id = ?",
                (now, job_id),
            )
            result = connection.execute("SELECT * FROM local_jobs WHERE job_id = ?", (job_id,)).fetchone()
            connection.commit()
            if result is None:
                raise JobQueueError("updated job could not be read back")
            return self._row_to_job(result)

    def get(self, job_id: str) -> LocalJob | None:
        with closing(self._connect()) as connection:
            row = connection.execute("SELECT * FROM local_jobs WHERE job_id = ?", (job_id,)).fetchone()
            return self._row_to_job(row) if row is not None else None

    def release_expired_leases(self) -> int:
        with closing(self._connect()) as connection:
            connection.execute("BEGIN IMMEDIATE")
            count = self._release_expired_in_transaction(connection, _utc_now())
            connection.commit()
            return count

    def stats(self) -> dict[str, int]:
        with closing(self._connect()) as connection:
            rows = connection.execute(
                "SELECT state, COUNT(*) AS count FROM local_jobs WHERE queue_id = ? GROUP BY state",
                (self.queue_id,),
            ).fetchall()
        result = {state: 0 for state in sorted(_JOB_STATES)}
        result.update({str(row["state"]): int(row["count"]) for row in rows})
        return result

    def _finish_lease(
        self,
        job_id: str,
        *,
        lease_owner: str,
        state: str,
        result_json: str | None,
        error_code: str | None,
        error_summary: str | None,
    ) -> LocalJob:
        now = _format_time(_utc_now())
        with closing(self._connect()) as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute("SELECT * FROM local_jobs WHERE job_id = ?", (job_id,)).fetchone()
            self._require_lease(row, lease_owner)
            connection.execute(
                """
                UPDATE local_jobs
                SET state = ?, result_json = ?, lease_owner = NULL, leased_until = NULL,
                    last_error_code = ?, last_error_summary = ?, updated_at = ?
                WHERE job_id = ?
                """,
                (state, result_json, error_code, error_summary, now, job_id),
            )
            result = connection.execute("SELECT * FROM local_jobs WHERE job_id = ?", (job_id,)).fetchone()
            connection.commit()
            if result is None:
                raise JobQueueError("updated job could not be read back")
            return self._row_to_job(result)

    @staticmethod
    def _require_lease(row: sqlite3.Row | None, lease_owner: str) -> None:
        if row is None:
            raise JobQueueError("job not found")
        if row["state"] != "leased" or row["lease_owner"] != lease_owner:
            raise JobQueueError("job is not leased by this worker")
        if row["leased_until"] and _parse_time(row["leased_until"]) < _utc_now():
            raise JobQueueError("job lease has expired")

    def _release_expired_in_transaction(self, connection: sqlite3.Connection, now: datetime) -> int:
        result = connection.execute(
            """
            UPDATE local_jobs
            SET state = CASE
                    WHEN attempt_count + 1 >= max_attempts THEN 'dead_letter'
                    ELSE 'queued'
                END,
                attempt_count = attempt_count + 1,
                lease_owner = NULL, leased_until = NULL,
                available_at = ?, updated_at = ?,
                last_error_code = 'lease_expired',
                last_error_summary = 'worker lease expired before terminal evidence'
            WHERE queue_id = ? AND state = 'leased' AND leased_until < ?
            """,
            (_format_time(now), _format_time(now), self.queue_id, _format_time(now)),
        )
        return result.rowcount

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database, timeout=self.timeout_seconds)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute(f"PRAGMA busy_timeout = {int(self.timeout_seconds * 1000)}")
        self._ensure_table(connection)
        return connection

    @staticmethod
    def _ensure_table(connection: sqlite3.Connection) -> None:
        row = connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'local_jobs'"
        ).fetchone()
        if row is None:
            connection.close()
            raise JobQueueError("local_jobs table is missing; apply component migrations first")

    @staticmethod
    def _row_to_job(row: sqlite3.Row) -> LocalJob:
        result = json.loads(row["result_json"]) if row["result_json"] else None
        return LocalJob(
            job_id=row["job_id"],
            queue_id=row["queue_id"],
            job_kind=row["job_kind"],
            subject_ref=row["subject_ref"],
            payload=json.loads(row["payload_json"]),
            payload_digest=row["payload_digest"],
            state=row["state"],
            priority=row["priority"],
            attempt_count=row["attempt_count"],
            max_attempts=row["max_attempts"],
            available_at=row["available_at"],
            lease_owner=row["lease_owner"],
            leased_until=row["leased_until"],
            idempotency_key=row["idempotency_key"],
            result=result,
            last_error_code=row["last_error_code"],
            last_error_summary=row["last_error_summary"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )
