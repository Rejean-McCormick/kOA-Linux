"""SQLite persistence adapter for Audit Broker-owned records.

The adapter accepts bounded mappings or dataclass-like domain values. It never
reads or writes a foreign component database and exposes no arbitrary SQL API.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import threading
from contextlib import contextmanager, suppress
from dataclasses import asdict, dataclass, is_dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from types import MappingProxyType
from typing import Any, Iterable, Iterator, Mapping, Sequence


RECORD_STATES = frozenset(
    {
        "received",
        "validated",
        "accepted",
        "quarantined",
        "retained",
        "held",
        "archived",
        "expired",
        "disposed",
        "invalidated",
    }
)
RETENTION_STATES = frozenset(
    {"active", "held", "archived", "expired", "disposition_pending", "disposed", "invalidated"}
)
ACCESS_OUTCOMES = frozenset(
    {"allowed", "partially_allowed", "denied", "cancelled", "expired", "failed"}
)
DELIVERY_STATES = frozenset(
    {"local", "undelivered", "delivery_failed", "delivered", "expired"}
)
REQUIRED_RECORD_FIELDS = frozenset(
    {
        "audit_record_id",
        "event_class_id",
        "producer_component_id",
        "producer_identity",
        "occurred_at",
        "received_at",
        "subject_references",
        "action_or_transition",
        "outcome",
        "purpose",
        "classification",
        "retention_class",
        "correlation_id",
        "source_receipt_or_evidence_refs",
        "policy_or_contract_ref",
    }
)
OPTIONAL_RECORD_FIELDS = frozenset(
    {"bounded_payload", "event_payload", "record_state", "integrity_algorithm", "integrity_digest"}
)


class AuditStorageError(RuntimeError):
    """Base error for bounded Audit Broker persistence operations."""


class StorageUnavailableError(AuditStorageError):
    """The owned record store could not complete an operation."""


class RecordNotFoundError(AuditStorageError):
    """The requested Audit Broker-owned record does not exist."""


class IdempotencyConflictError(AuditStorageError):
    """An idempotency key was reused for a different semantic request."""


class IntegrityConflictError(AuditStorageError):
    """Stored material does not match its recorded integrity digest."""


class InvalidRecordError(AuditStorageError, ValueError):
    """A caller supplied an incomplete, unbounded, or invalid record."""


@dataclass(frozen=True, slots=True)
class AppendResult:
    audit_record_id: str
    integrity_digest: str
    duplicate: bool


@dataclass(frozen=True, slots=True)
class QueryPage:
    records: tuple[Mapping[str, Any], ...]
    next_cursor: str | None


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _timestamp(value: Any, field: str) -> str:
    if isinstance(value, str):
        candidate = value
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise InvalidRecordError(f"{field} must be an RFC 3339 timestamp") from exc
    elif isinstance(value, datetime):
        parsed = value
        candidate = value.isoformat()
    else:
        raise InvalidRecordError(f"{field} must be a datetime or RFC 3339 string")
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise InvalidRecordError(f"{field} must include a timezone")
    normalized = parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    if not candidate.strip():
        raise InvalidRecordError(f"{field} must not be empty")
    return normalized


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InvalidRecordError(f"{field} must be a non-empty string")
    return value.strip()


def _json_value(value: Any) -> Any:
    if isinstance(value, datetime):
        return _timestamp(value, "timestamp")
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {str(k): _json_value(v) for k, v in asdict(value).items()}
    if isinstance(value, Mapping):
        return {str(k): _json_value(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [_json_value(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise InvalidRecordError(f"value of type {type(value).__name__} is not JSON-compatible")


def _mapping(value: Any, field: str) -> dict[str, Any]:
    if is_dataclass(value):
        value = asdict(value)
    elif not isinstance(value, Mapping) and hasattr(value, "to_dict"):
        value = value.to_dict()
    if not isinstance(value, Mapping):
        raise InvalidRecordError(f"{field} must be a mapping or dataclass-like value")
    return {str(k): _json_value(v) for k, v in value.items()}


def _canonical_json(value: Any) -> str:
    try:
        return json.dumps(
            _json_value(value), ensure_ascii=False, separators=(",", ":"), sort_keys=True
        )
    except (TypeError, ValueError) as exc:
        raise InvalidRecordError("value is not canonical JSON compatible") from exc


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _decode_json(value: str) -> Any:
    return json.loads(value)


def _record_payload(record: Any) -> tuple[dict[str, Any], str]:
    raw = _mapping(record, "record")
    missing = sorted(REQUIRED_RECORD_FIELDS - set(raw))
    unexpected = sorted(set(raw) - REQUIRED_RECORD_FIELDS - OPTIONAL_RECORD_FIELDS)
    if missing:
        raise InvalidRecordError("missing audit record fields: " + ", ".join(missing))
    if unexpected:
        raise InvalidRecordError("undeclared audit record fields: " + ", ".join(unexpected))
    result: dict[str, Any] = {}
    for key in REQUIRED_RECORD_FIELDS:
        result[key] = raw[key]
    for key in (
        "audit_record_id",
        "event_class_id",
        "producer_component_id",
        "action_or_transition",
        "outcome",
        "purpose",
        "classification",
        "retention_class",
        "correlation_id",
        "policy_or_contract_ref",
    ):
        result[key] = _text(result[key], key)
    result["occurred_at"] = _timestamp(result["occurred_at"], "occurred_at")
    result["received_at"] = _timestamp(result["received_at"], "received_at")
    result["producer_identity"] = _mapping(result["producer_identity"], "producer_identity")
    for key in ("subject_references", "source_receipt_or_evidence_refs"):
        value = result[key]
        if not isinstance(value, (list, tuple)) or not value:
            raise InvalidRecordError(f"{key} must be a non-empty sequence")
        result[key] = [_text(item, key) for item in value]
    payload = raw.get("bounded_payload", raw.get("event_payload", {}))
    result["bounded_payload"] = _mapping(payload, "bounded_payload")
    state = raw.get("record_state", "accepted")
    state = _text(state.value if isinstance(state, Enum) else state, "record_state")
    if state not in RECORD_STATES:
        raise InvalidRecordError(f"unsupported record_state: {state}")
    result["record_state"] = state
    algorithm = raw.get("integrity_algorithm", "sha256")
    if algorithm != "sha256":
        raise InvalidRecordError("only sha256 integrity is supported by this adapter")
    result["integrity_algorithm"] = "sha256"
    digest_material = dict(result)
    supplied_digest = raw.get("integrity_digest")
    calculated = _digest(digest_material)
    if supplied_digest is not None and supplied_digest != calculated:
        raise IntegrityConflictError("supplied integrity digest does not match the bounded record")
    result["integrity_digest"] = calculated
    return result, _digest(digest_material)


def _row_to_record(row: Mapping[str, Any]) -> Mapping[str, Any]:
    result = {
        "audit_record_id": row["audit_record_id"],
        "event_class_id": row["event_class_id"],
        "producer_component_id": row["producer_component_id"],
        "producer_identity": _decode_json(row["producer_identity_json"]),
        "occurred_at": row["occurred_at"],
        "received_at": row["received_at"],
        "subject_references": _decode_json(row["subject_references_json"]),
        "action_or_transition": row["action_or_transition"],
        "outcome": row["outcome"],
        "purpose": row["purpose"],
        "classification": row["classification"],
        "retention_class": row["retention_class"],
        "correlation_id": row["correlation_id"],
        "source_receipt_or_evidence_refs": _decode_json(row["source_refs_json"]),
        "bounded_payload": _decode_json(row["bounded_payload_json"]),
        "policy_or_contract_ref": row["policy_or_contract_ref"],
        "record_state": row["record_state"],
        "integrity_algorithm": row["integrity_algorithm"],
        "integrity_digest": row["integrity_digest"],
        "created_at": row["created_at"],
    }
    return MappingProxyType(result)


class SQLiteEventStore:
    """SQLite implementation of the Audit Broker event-store port."""

    def __init__(
        self,
        database: str | Path,
        *,
        timeout_seconds: float = 5.0,
        read_only: bool = False,
        uri: bool = False,
    ) -> None:
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        target = str(database)
        if read_only and target != ":memory:" and not target.startswith("file:"):
            target = f"file:{Path(target).resolve()}?mode=ro"
            uri = True
        self._connection = sqlite3.connect(
            target,
            timeout=timeout_seconds,
            isolation_level=None,
            check_same_thread=False,
            uri=uri,
        )
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("PRAGMA foreign_keys = ON")
        self._connection.execute(f"PRAGMA busy_timeout = {int(timeout_seconds * 1000)}")
        self._read_only = read_only
        self._lock = threading.RLock()
        self._closed = False

    def close(self) -> None:
        with self._lock:
            if not self._closed:
                self._connection.close()
                self._closed = True

    def __enter__(self) -> "SQLiteEventStore":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def _ensure_open(self) -> None:
        if self._closed:
            raise StorageUnavailableError("event store is closed")

    @contextmanager
    def _transaction(self, *, write: bool) -> Iterator[sqlite3.Connection]:
        with self._lock:
            self._ensure_open()
            if write and self._read_only:
                raise StorageUnavailableError("event store is read-only")
            try:
                self._connection.execute("BEGIN IMMEDIATE" if write else "BEGIN")
                yield self._connection
                self._connection.execute("COMMIT")
            except Exception:
                with suppress(sqlite3.Error):
                    self._connection.execute("ROLLBACK")
                raise

    @staticmethod
    def default_migration_path() -> Path:
        return Path(__file__).resolve().parents[3] / "migrations" / "0001_initial.sql"

    def migrate(self, migration_sql: str | None = None, *, applied_at: datetime | str | None = None) -> None:
        sql = migration_sql
        if sql is None:
            sql = self.default_migration_path().read_text(encoding="utf-8")
        timestamp = _timestamp(applied_at or _utc_now(), "applied_at")
        escaped_timestamp = timestamp.replace("'", "''")
        script = (
            "BEGIN IMMEDIATE;\n"
            + sql
            + "\nINSERT OR IGNORE INTO audit_schema_migrations(version, applied_at) "
              f"VALUES ('0001', '{escaped_timestamp}');\nCOMMIT;\n"
        )
        with self._lock:
            self._ensure_open()
            if self._read_only:
                raise StorageUnavailableError("event store is read-only")
            try:
                self._connection.executescript(script)
            except sqlite3.Error as exc:
                if self._connection.in_transaction:
                    self._connection.execute("ROLLBACK")
                raise StorageUnavailableError(f"SQLite migration failed atomically: {exc}") from exc

    def append_record(
        self,
        record: Any,
        *,
        idempotency_key: str,
        actor_identity: Mapping[str, Any] | None = None,
        receipt_ref: str | None = None,
    ) -> AppendResult:
        normalized, request_digest = _record_payload(record)
        key = _text(idempotency_key, "idempotency_key")
        actor = _mapping(actor_identity or normalized["producer_identity"], "actor_identity")
        receipt = _text(receipt_ref or f"receipt:{normalized['audit_record_id']}", "receipt_ref")
        now = _timestamp(_utc_now(), "created_at")
        try:
            with self._transaction(write=True) as conn:
                prior = conn.execute(
                    "SELECT request_digest, audit_record_id FROM audit_idempotency_keys "
                    "WHERE producer_component_id = ? AND idempotency_key = ?",
                    (normalized["producer_component_id"], key),
                ).fetchone()
                if prior is not None:
                    if prior["request_digest"] != request_digest:
                        raise IdempotencyConflictError(
                            "idempotency key was reused for a different audit submission"
                        )
                    existing = conn.execute(
                        "SELECT integrity_digest FROM audit_records WHERE audit_record_id = ?",
                        (prior["audit_record_id"],),
                    ).fetchone()
                    if existing is None:
                        raise IntegrityConflictError("idempotency entry references a missing record")
                    return AppendResult(prior["audit_record_id"], existing["integrity_digest"], True)
                conn.execute(
                    """INSERT INTO audit_records(
                        audit_record_id,event_class_id,producer_component_id,producer_identity_json,
                        occurred_at,received_at,subject_references_json,action_or_transition,outcome,
                        purpose,classification,retention_class,correlation_id,source_refs_json,
                        bounded_payload_json,policy_or_contract_ref,record_state,integrity_algorithm,
                        integrity_digest,created_at
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (
                        normalized["audit_record_id"], normalized["event_class_id"],
                        normalized["producer_component_id"], _canonical_json(normalized["producer_identity"]),
                        normalized["occurred_at"], normalized["received_at"],
                        _canonical_json(normalized["subject_references"]), normalized["action_or_transition"],
                        normalized["outcome"], normalized["purpose"], normalized["classification"],
                        normalized["retention_class"], normalized["correlation_id"],
                        _canonical_json(normalized["source_receipt_or_evidence_refs"]),
                        _canonical_json(normalized["bounded_payload"]), normalized["policy_or_contract_ref"],
                        normalized["record_state"], normalized["integrity_algorithm"],
                        normalized["integrity_digest"], now,
                    ),
                )
                conn.execute(
                    "INSERT INTO audit_idempotency_keys VALUES (?,?,?,?,?)",
                    (normalized["producer_component_id"], key, request_digest, normalized["audit_record_id"], now),
                )
                self._append_custody_in_transaction(
                    conn,
                    chain_id=f"custody:{normalized['audit_record_id']}",
                    subject_ref=normalized["audit_record_id"],
                    transition_type="audit_record_accepted",
                    actor_identity=actor,
                    occurred_at=normalized["received_at"],
                    result=normalized["record_state"],
                    receipt_ref=receipt,
                    details={"integrity_digest": normalized["integrity_digest"]},
                    created_at=now,
                )
                conn.execute(
                    """INSERT INTO audit_retention_state(
                        record_ref,retention_class,state,effective_at,policy_or_hold_ref,
                        next_review_or_disposition_at,updated_at
                    ) VALUES (?,?,?,?,?,?,?)""",
                    (
                        normalized["audit_record_id"], normalized["retention_class"], "active",
                        normalized["received_at"], normalized["policy_or_contract_ref"], None, now,
                    ),
                )
        except (IdempotencyConflictError, IntegrityConflictError):
            raise
        except sqlite3.IntegrityError as exc:
            raise IntegrityConflictError(f"audit record integrity constraint failed: {exc}") from exc
        except sqlite3.Error as exc:
            raise StorageUnavailableError(f"SQLite append failed: {exc}") from exc
        return AppendResult(normalized["audit_record_id"], normalized["integrity_digest"], False)

    append_event = append_record

    def get_record(self, audit_record_id: str) -> Mapping[str, Any]:
        record_id = _text(audit_record_id, "audit_record_id")
        try:
            with self._transaction(write=False) as conn:
                row = conn.execute(
                    "SELECT * FROM audit_records WHERE audit_record_id = ?", (record_id,)
                ).fetchone()
        except sqlite3.Error as exc:
            raise StorageUnavailableError(f"SQLite read failed: {exc}") from exc
        if row is None:
            raise RecordNotFoundError(record_id)
        return _row_to_record(row)

    get = get_record

    def query_records(
        self,
        *,
        event_class_id: str | None = None,
        producer_component_id: str | None = None,
        correlation_id: str | None = None,
        record_state: str | None = None,
        occurred_from: datetime | str | None = None,
        occurred_to: datetime | str | None = None,
        limit: int = 100,
        cursor: str | None = None,
    ) -> QueryPage:
        if not isinstance(limit, int) or not 1 <= limit <= 1000:
            raise InvalidRecordError("limit must be between 1 and 1000")
        clauses: list[str] = []
        values: list[Any] = []
        for column, value in (
            ("event_class_id", event_class_id),
            ("producer_component_id", producer_component_id),
            ("correlation_id", correlation_id),
            ("record_state", record_state),
        ):
            if value is not None:
                clauses.append(f"{column} = ?")
                values.append(_text(value, column))
        if occurred_from is not None:
            clauses.append("occurred_at >= ?")
            values.append(_timestamp(occurred_from, "occurred_from"))
        if occurred_to is not None:
            clauses.append("occurred_at <= ?")
            values.append(_timestamp(occurred_to, "occurred_to"))
        if cursor is not None:
            clauses.append("audit_record_id > ?")
            values.append(_text(cursor, "cursor"))
        where = " WHERE " + " AND ".join(clauses) if clauses else ""
        sql = "SELECT * FROM audit_records" + where + " ORDER BY audit_record_id LIMIT ?"
        values.append(limit + 1)
        try:
            with self._transaction(write=False) as conn:
                rows = conn.execute(sql, values).fetchall()
        except sqlite3.Error as exc:
            raise StorageUnavailableError(f"SQLite query failed: {exc}") from exc
        next_cursor = rows[limit - 1]["audit_record_id"] if len(rows) > limit else None
        selected = rows[:limit]
        return QueryPage(tuple(_row_to_record(row) for row in selected), next_cursor)

    query = query_records

    def _append_custody_in_transaction(
        self,
        conn: sqlite3.Connection,
        *,
        chain_id: str,
        subject_ref: str,
        transition_type: str,
        actor_identity: Mapping[str, Any],
        occurred_at: datetime | str,
        result: str,
        receipt_ref: str,
        details: Mapping[str, Any] | None,
        created_at: str,
    ) -> str:
        previous = conn.execute(
            "SELECT entry_digest FROM audit_chain_of_custody WHERE chain_id = ? "
            "ORDER BY occurred_at DESC, custody_entry_id DESC LIMIT 1",
            (chain_id,),
        ).fetchone()
        previous_digest = previous["entry_digest"] if previous else None
        material = {
            "chain_id": _text(chain_id, "chain_id"),
            "subject_ref": _text(subject_ref, "subject_ref"),
            "transition_type": _text(transition_type, "transition_type"),
            "actor_identity": _mapping(actor_identity, "actor_identity"),
            "occurred_at": _timestamp(occurred_at, "occurred_at"),
            "result": _text(result, "result"),
            "receipt_ref": _text(receipt_ref, "receipt_ref"),
            "details": _mapping(details or {}, "details"),
            "previous_entry_digest": previous_digest,
        }
        entry_digest = _digest(material)
        entry_id = f"CUSTODY-{entry_digest[:24].upper()}"
        conn.execute(
            """INSERT INTO audit_chain_of_custody(
                custody_entry_id,chain_id,subject_ref,transition_type,actor_identity_json,
                occurred_at,result,receipt_ref,details_json,previous_entry_digest,entry_digest,created_at
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                entry_id, material["chain_id"], material["subject_ref"], material["transition_type"],
                _canonical_json(material["actor_identity"]), material["occurred_at"], material["result"],
                material["receipt_ref"], _canonical_json(material["details"]), previous_digest,
                entry_digest, created_at,
            ),
        )
        return entry_id

    def append_chain_entry(
        self,
        *,
        chain_id: str,
        subject_ref: str,
        transition_type: str,
        actor_identity: Mapping[str, Any],
        occurred_at: datetime | str,
        result: str,
        receipt_ref: str,
        details: Mapping[str, Any] | None = None,
    ) -> str:
        now = _timestamp(_utc_now(), "created_at")
        try:
            with self._transaction(write=True) as conn:
                return self._append_custody_in_transaction(
                    conn, chain_id=chain_id, subject_ref=subject_ref,
                    transition_type=transition_type, actor_identity=actor_identity,
                    occurred_at=occurred_at, result=result, receipt_ref=receipt_ref,
                    details=details, created_at=now,
                )
        except sqlite3.IntegrityError as exc:
            raise IntegrityConflictError(f"duplicate or conflicting custody entry: {exc}") from exc
        except sqlite3.Error as exc:
            raise StorageUnavailableError(f"SQLite custody append failed: {exc}") from exc

    def custody_chain(self, subject_ref: str, *, limit: int = 1000) -> tuple[Mapping[str, Any], ...]:
        subject = _text(subject_ref, "subject_ref")
        if not isinstance(limit, int) or not 1 <= limit <= 10000:
            raise InvalidRecordError("limit must be between 1 and 10000")
        try:
            with self._transaction(write=False) as conn:
                rows = conn.execute(
                    "SELECT * FROM audit_chain_of_custody WHERE subject_ref = ? "
                    "ORDER BY occurred_at, custody_entry_id LIMIT ?", (subject, limit)
                ).fetchall()
        except sqlite3.Error as exc:
            raise StorageUnavailableError(f"SQLite custody query failed: {exc}") from exc
        return tuple(
            MappingProxyType(
                {
                    "custody_entry_id": row["custody_entry_id"],
                    "chain_id": row["chain_id"],
                    "subject_ref": row["subject_ref"],
                    "transition_type": row["transition_type"],
                    "actor_identity": _decode_json(row["actor_identity_json"]),
                    "occurred_at": row["occurred_at"],
                    "result": row["result"],
                    "receipt_ref": row["receipt_ref"],
                    "details": _decode_json(row["details_json"]),
                    "previous_entry_digest": row["previous_entry_digest"],
                    "entry_digest": row["entry_digest"],
                }
            )
            for row in rows
        )

    def set_retention_state(
        self,
        *,
        record_ref: str,
        retention_class: str,
        state: str,
        effective_at: datetime | str,
        policy_or_hold_ref: str,
        actor_identity: Mapping[str, Any],
        receipt_ref: str,
        next_review_or_disposition_at: datetime | str | None = None,
    ) -> None:
        record_id = _text(record_ref, "record_ref")
        target_state = _text(state, "state")
        if target_state not in RETENTION_STATES:
            raise InvalidRecordError(f"unsupported retention state: {target_state}")
        effective = _timestamp(effective_at, "effective_at")
        next_at = (
            _timestamp(next_review_or_disposition_at, "next_review_or_disposition_at")
            if next_review_or_disposition_at is not None else None
        )
        now = _timestamp(_utc_now(), "updated_at")
        try:
            with self._transaction(write=True) as conn:
                current = conn.execute(
                    "SELECT state FROM audit_retention_state WHERE record_ref = ?", (record_id,)
                ).fetchone()
                if current is None:
                    raise RecordNotFoundError(record_id)
                if current["state"] == "held" and target_state in {"disposed", "disposition_pending"}:
                    raise InvalidRecordError("an active hold blocks disposition")
                conn.execute(
                    """UPDATE audit_retention_state SET
                        retention_class=?,state=?,effective_at=?,policy_or_hold_ref=?,
                        next_review_or_disposition_at=?,updated_at=? WHERE record_ref=?""",
                    (
                        _text(retention_class, "retention_class"), target_state, effective,
                        _text(policy_or_hold_ref, "policy_or_hold_ref"), next_at, now, record_id,
                    ),
                )
                projected_state = {
                    "active": "retained", "held": "held", "archived": "archived",
                    "expired": "expired", "disposition_pending": "expired",
                    "disposed": "disposed", "invalidated": "invalidated",
                }[target_state]
                conn.execute(
                    "UPDATE audit_records SET record_state = ? WHERE audit_record_id = ?",
                    (projected_state, record_id),
                )
                self._append_custody_in_transaction(
                    conn, chain_id=f"custody:{record_id}", subject_ref=record_id,
                    transition_type="audit_retention_state_changed", actor_identity=actor_identity,
                    occurred_at=effective, result=target_state, receipt_ref=receipt_ref,
                    details={"policy_or_hold_ref": policy_or_hold_ref, "retention_class": retention_class},
                    created_at=now,
                )
        except (RecordNotFoundError, InvalidRecordError):
            raise
        except sqlite3.Error as exc:
            raise StorageUnavailableError(f"SQLite retention update failed: {exc}") from exc

    apply_retention = set_retention_state

    def record_access_receipt(self, receipt: Any) -> None:
        value = _mapping(receipt, "receipt")
        required = {
            "receipt_id", "request_id", "requester_identity", "purpose", "policy_decision_ref",
            "requested_scope", "effective_scope", "outcome", "occurred_at",
        }
        missing = sorted(required - set(value))
        if missing:
            raise InvalidRecordError("missing access receipt fields: " + ", ".join(missing))
        outcome = _text(value["outcome"], "outcome")
        if outcome not in ACCESS_OUTCOMES:
            raise InvalidRecordError(f"unsupported access outcome: {outcome}")
        now = _timestamp(_utc_now(), "created_at")
        try:
            with self._transaction(write=True) as conn:
                conn.execute(
                    "INSERT INTO audit_access_receipts VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    (
                        _text(value["receipt_id"], "receipt_id"), _text(value["request_id"], "request_id"),
                        _canonical_json(_mapping(value["requester_identity"], "requester_identity")),
                        _text(value["purpose"], "purpose"),
                        _text(value["policy_decision_ref"], "policy_decision_ref"),
                        _canonical_json(value["requested_scope"]), _canonical_json(value["effective_scope"]),
                        outcome, _timestamp(value["occurred_at"], "occurred_at"),
                        _canonical_json(value), now,
                    ),
                )
        except sqlite3.IntegrityError as exc:
            raise IntegrityConflictError(f"duplicate access receipt: {exc}") from exc
        except sqlite3.Error as exc:
            raise StorageUnavailableError(f"SQLite receipt append failed: {exc}") from exc

    append_receipt = record_access_receipt

    def store_disclosure_package(self, package: Any, *, delivery_state: str = "local") -> str:
        value = _mapping(package, "package")
        required = {
            "package_id", "request_id", "purpose", "scope", "record_refs",
            "redaction_profile", "generated_at", "expiry_or_validity", "chain_of_custody_ref",
        }
        missing = sorted(required - set(value))
        if missing:
            raise InvalidRecordError("missing disclosure package fields: " + ", ".join(missing))
        state = _text(delivery_state, "delivery_state")
        if state not in DELIVERY_STATES:
            raise InvalidRecordError(f"unsupported delivery state: {state}")
        digest = _digest(value)
        now = _timestamp(_utc_now(), "created_at")
        try:
            with self._transaction(write=True) as conn:
                conn.execute(
                    "INSERT INTO audit_disclosure_packages VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (
                        _text(value["package_id"], "package_id"), _text(value["request_id"], "request_id"),
                        _text(value["purpose"], "purpose"), _canonical_json(value["scope"]),
                        _canonical_json(value["record_refs"]),
                        _text(value["redaction_profile"], "redaction_profile"),
                        _timestamp(value["generated_at"], "generated_at"),
                        _text(value["expiry_or_validity"], "expiry_or_validity"),
                        _text(value["chain_of_custody_ref"], "chain_of_custody_ref"),
                        state, _canonical_json(value), digest, now,
                    ),
                )
        except sqlite3.IntegrityError as exc:
            raise IntegrityConflictError(f"duplicate disclosure package: {exc}") from exc
        except sqlite3.Error as exc:
            raise StorageUnavailableError(f"SQLite package append failed: {exc}") from exc
        return digest

    def append_invalidation(
        self,
        *,
        invalidation_id: str,
        record_ref: str,
        source_correction_or_retraction_ref: str,
        reason: str,
        effective_at: datetime | str,
        actor_identity: Mapping[str, Any],
        receipt_ref: str,
    ) -> None:
        record_id = _text(record_ref, "record_ref")
        effective = _timestamp(effective_at, "effective_at")
        now = _timestamp(_utc_now(), "created_at")
        try:
            with self._transaction(write=True) as conn:
                exists = conn.execute(
                    "SELECT 1 FROM audit_records WHERE audit_record_id = ?", (record_id,)
                ).fetchone()
                if exists is None:
                    raise RecordNotFoundError(record_id)
                conn.execute(
                    "INSERT INTO audit_invalidations VALUES (?,?,?,?,?,?,?,?)",
                    (
                        _text(invalidation_id, "invalidation_id"), record_id,
                        _text(source_correction_or_retraction_ref, "source_correction_or_retraction_ref"),
                        _text(reason, "reason"), effective,
                        _canonical_json(_mapping(actor_identity, "actor_identity")),
                        _text(receipt_ref, "receipt_ref"), now,
                    ),
                )
                conn.execute(
                    "UPDATE audit_records SET record_state = 'invalidated' WHERE audit_record_id = ?",
                    (record_id,),
                )
                conn.execute(
                    "UPDATE audit_retention_state SET state='invalidated', effective_at=?, "
                    "policy_or_hold_ref=?, updated_at=? WHERE record_ref=?",
                    (effective, source_correction_or_retraction_ref, now, record_id),
                )
                self._append_custody_in_transaction(
                    conn, chain_id=f"custody:{record_id}", subject_ref=record_id,
                    transition_type="audit_record_invalidated", actor_identity=actor_identity,
                    occurred_at=effective, result="invalidated", receipt_ref=receipt_ref,
                    details={"invalidation_id": invalidation_id, "reason": reason,
                             "source_correction_or_retraction_ref": source_correction_or_retraction_ref},
                    created_at=now,
                )
        except (RecordNotFoundError, InvalidRecordError):
            raise
        except sqlite3.IntegrityError as exc:
            raise IntegrityConflictError(f"duplicate invalidation: {exc}") from exc
        except sqlite3.Error as exc:
            raise StorageUnavailableError(f"SQLite invalidation append failed: {exc}") from exc

    invalidate = append_invalidation

    def verify_integrity(self, audit_record_id: str) -> bool:
        record = dict(self.get_record(audit_record_id))
        expected = record.pop("integrity_digest")
        record.pop("created_at", None)
        material = {key: record[key] for key in record if key != "integrity_algorithm"}
        material["integrity_algorithm"] = "sha256"
        actual = _digest(material)
        if actual != expected:
            raise IntegrityConflictError(f"integrity verification failed for {audit_record_id}")
        return True
