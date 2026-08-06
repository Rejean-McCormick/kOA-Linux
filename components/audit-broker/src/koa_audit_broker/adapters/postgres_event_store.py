"""PostgreSQL persistence adapter using the standard DB-API connection shape.

A driver is intentionally not imported here. Deployment injects a psycopg-compatible
connection factory, keeping credentials and driver selection outside this component.
"""

from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, Iterator, Mapping, Protocol, Sequence

from .sqlite_event_store import (
    ACCESS_OUTCOMES,
    DELIVERY_STATES,
    RETENTION_STATES,
    AppendResult,
    IdempotencyConflictError,
    IntegrityConflictError,
    InvalidRecordError,
    QueryPage,
    RecordNotFoundError,
    StorageUnavailableError,
    _canonical_json,
    _decode_json,
    _digest,
    _mapping,
    _record_payload,
    _text,
    _timestamp,
    _utc_now,
)


class CursorLike(Protocol):
    description: Sequence[Sequence[Any]] | None
    rowcount: int
    def execute(self, operation: str, parameters: Sequence[Any] | None = None) -> Any: ...
    def fetchone(self) -> Any: ...
    def fetchall(self) -> Sequence[Any]: ...
    def close(self) -> None: ...


class ConnectionLike(Protocol):
    def cursor(self) -> CursorLike: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...
    def close(self) -> None: ...


def _row_mapping(cursor: CursorLike, row: Any) -> Mapping[str, Any] | None:
    if row is None:
        return None
    if isinstance(row, Mapping):
        return row
    if cursor.description is None:
        raise StorageUnavailableError("PostgreSQL cursor omitted row description")
    names = [str(column[0]) for column in cursor.description]
    return dict(zip(names, row, strict=True))


def _record_from_row(row: Mapping[str, Any]) -> Mapping[str, Any]:
    return MappingProxyType(
        {
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
    )


class PostgresEventStore:
    """PostgreSQL implementation of the Audit Broker event-store port."""

    def __init__(self, connection_factory: Callable[[], ConnectionLike]) -> None:
        if not callable(connection_factory):
            raise TypeError("connection_factory must be callable")
        self._connection_factory = connection_factory

    @staticmethod
    def default_migration_path() -> Path:
        return Path(__file__).resolve().parents[3] / "migrations" / "0001_initial.sql"

    @contextmanager
    def _transaction(self) -> Iterator[tuple[ConnectionLike, CursorLike]]:
        connection = self._connection_factory()
        cursor = connection.cursor()
        try:
            yield connection, cursor
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()

    def migrate(self, migration_sql: str | None = None, *, applied_at: datetime | str | None = None) -> None:
        sql = migration_sql or self.default_migration_path().read_text(encoding="utf-8")
        timestamp = _timestamp(applied_at or _utc_now(), "applied_at")
        try:
            with self._transaction() as (_, cursor):
                cursor.execute(sql)
                cursor.execute(
                    "INSERT INTO audit_schema_migrations(version, applied_at) VALUES (%s, %s) "
                    "ON CONFLICT (version) DO NOTHING",
                    ("0001", timestamp),
                )
        except Exception as exc:
            if isinstance(exc, (InvalidRecordError, StorageUnavailableError)):
                raise
            raise StorageUnavailableError(f"PostgreSQL migration failed: {exc}") from exc

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
            with self._transaction() as (_, cursor):
                cursor.execute(
                    "SELECT request_digest, audit_record_id FROM audit_idempotency_keys "
                    "WHERE producer_component_id=%s AND idempotency_key=%s FOR UPDATE",
                    (normalized["producer_component_id"], key),
                )
                prior = _row_mapping(cursor, cursor.fetchone())
                if prior is not None:
                    if prior["request_digest"] != request_digest:
                        raise IdempotencyConflictError(
                            "idempotency key was reused for a different audit submission"
                        )
                    cursor.execute(
                        "SELECT integrity_digest FROM audit_records WHERE audit_record_id=%s",
                        (prior["audit_record_id"],),
                    )
                    existing = _row_mapping(cursor, cursor.fetchone())
                    if existing is None:
                        raise IntegrityConflictError("idempotency entry references a missing record")
                    return AppendResult(prior["audit_record_id"], existing["integrity_digest"], True)
                cursor.execute(
                    """INSERT INTO audit_records(
                        audit_record_id,event_class_id,producer_component_id,producer_identity_json,
                        occurred_at,received_at,subject_references_json,action_or_transition,outcome,
                        purpose,classification,retention_class,correlation_id,source_refs_json,
                        bounded_payload_json,policy_or_contract_ref,record_state,integrity_algorithm,
                        integrity_digest,created_at
                    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
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
                cursor.execute(
                    "INSERT INTO audit_idempotency_keys VALUES (%s,%s,%s,%s,%s)",
                    (normalized["producer_component_id"], key, request_digest, normalized["audit_record_id"], now),
                )
                self._append_custody(
                    cursor, chain_id=f"custody:{normalized['audit_record_id']}",
                    subject_ref=normalized["audit_record_id"], transition_type="audit_record_accepted",
                    actor_identity=actor, occurred_at=normalized["received_at"],
                    result=normalized["record_state"], receipt_ref=receipt,
                    details={"integrity_digest": normalized["integrity_digest"]}, created_at=now,
                )
                cursor.execute(
                    "INSERT INTO audit_retention_state VALUES (%s,%s,%s,%s,%s,%s,%s)",
                    (
                        normalized["audit_record_id"], normalized["retention_class"], "active",
                        normalized["received_at"], normalized["policy_or_contract_ref"], None, now,
                    ),
                )
        except (IdempotencyConflictError, IntegrityConflictError, InvalidRecordError):
            raise
        except Exception as exc:
            raise StorageUnavailableError(f"PostgreSQL append failed: {exc}") from exc
        return AppendResult(normalized["audit_record_id"], normalized["integrity_digest"], False)

    append_event = append_record

    def _append_custody(
        self, cursor: CursorLike, *, chain_id: str, subject_ref: str, transition_type: str,
        actor_identity: Mapping[str, Any], occurred_at: datetime | str, result: str,
        receipt_ref: str, details: Mapping[str, Any] | None, created_at: str,
    ) -> str:
        cursor.execute(
            "SELECT entry_digest FROM audit_chain_of_custody WHERE chain_id=%s "
            "ORDER BY occurred_at DESC, custody_entry_id DESC LIMIT 1 FOR UPDATE", (chain_id,),
        )
        previous = _row_mapping(cursor, cursor.fetchone())
        previous_digest = previous["entry_digest"] if previous else None
        material = {
            "chain_id": _text(chain_id, "chain_id"), "subject_ref": _text(subject_ref, "subject_ref"),
            "transition_type": _text(transition_type, "transition_type"),
            "actor_identity": _mapping(actor_identity, "actor_identity"),
            "occurred_at": _timestamp(occurred_at, "occurred_at"), "result": _text(result, "result"),
            "receipt_ref": _text(receipt_ref, "receipt_ref"), "details": _mapping(details or {}, "details"),
            "previous_entry_digest": previous_digest,
        }
        entry_digest = _digest(material)
        entry_id = f"CUSTODY-{entry_digest[:24].upper()}"
        cursor.execute(
            "INSERT INTO audit_chain_of_custody VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (
                entry_id, material["chain_id"], material["subject_ref"], material["transition_type"],
                _canonical_json(material["actor_identity"]), material["occurred_at"], material["result"],
                material["receipt_ref"], _canonical_json(material["details"]), previous_digest,
                entry_digest, created_at,
            ),
        )
        return entry_id

    def append_chain_entry(self, **values: Any) -> str:
        now = _timestamp(_utc_now(), "created_at")
        try:
            with self._transaction() as (_, cursor):
                return self._append_custody(cursor, created_at=now, **values)
        except (InvalidRecordError, IntegrityConflictError):
            raise
        except Exception as exc:
            raise StorageUnavailableError(f"PostgreSQL custody append failed: {exc}") from exc

    def get_record(self, audit_record_id: str) -> Mapping[str, Any]:
        record_id = _text(audit_record_id, "audit_record_id")
        try:
            with self._transaction() as (_, cursor):
                cursor.execute("SELECT * FROM audit_records WHERE audit_record_id=%s", (record_id,))
                row = _row_mapping(cursor, cursor.fetchone())
        except Exception as exc:
            raise StorageUnavailableError(f"PostgreSQL read failed: {exc}") from exc
        if row is None:
            raise RecordNotFoundError(record_id)
        return _record_from_row(row)

    get = get_record

    def query_records(
        self, *, event_class_id: str | None = None, producer_component_id: str | None = None,
        correlation_id: str | None = None, record_state: str | None = None,
        occurred_from: datetime | str | None = None, occurred_to: datetime | str | None = None,
        limit: int = 100, cursor: str | None = None,
    ) -> QueryPage:
        if not isinstance(limit, int) or not 1 <= limit <= 1000:
            raise InvalidRecordError("limit must be between 1 and 1000")
        clauses: list[str] = []
        values: list[Any] = []
        for column, value in (("event_class_id", event_class_id),
                              ("producer_component_id", producer_component_id),
                              ("correlation_id", correlation_id), ("record_state", record_state)):
            if value is not None:
                clauses.append(f"{column}=%s")
                values.append(_text(value, column))
        if occurred_from is not None:
            clauses.append("occurred_at>=%s"); values.append(_timestamp(occurred_from, "occurred_from"))
        if occurred_to is not None:
            clauses.append("occurred_at<=%s"); values.append(_timestamp(occurred_to, "occurred_to"))
        if cursor is not None:
            clauses.append("audit_record_id>%s"); values.append(_text(cursor, "cursor"))
        where = " WHERE " + " AND ".join(clauses) if clauses else ""
        values.append(limit + 1)
        try:
            with self._transaction() as (_, cur):
                cur.execute("SELECT * FROM audit_records" + where + " ORDER BY audit_record_id LIMIT %s", values)
                raw_rows = cur.fetchall()
                rows = [_row_mapping(cur, row) for row in raw_rows]
        except Exception as exc:
            raise StorageUnavailableError(f"PostgreSQL query failed: {exc}") from exc
        selected = [row for row in rows[:limit] if row is not None]
        next_cursor = selected[-1]["audit_record_id"] if len(rows) > limit and selected else None
        return QueryPage(tuple(_record_from_row(row) for row in selected), next_cursor)

    query = query_records

    def set_retention_state(
        self, *, record_ref: str, retention_class: str, state: str,
        effective_at: datetime | str, policy_or_hold_ref: str,
        actor_identity: Mapping[str, Any], receipt_ref: str,
        next_review_or_disposition_at: datetime | str | None = None,
    ) -> None:
        record_id = _text(record_ref, "record_ref")
        target = _text(state, "state")
        if target not in RETENTION_STATES:
            raise InvalidRecordError(f"unsupported retention state: {target}")
        effective = _timestamp(effective_at, "effective_at")
        next_at = _timestamp(next_review_or_disposition_at, "next_review_or_disposition_at") if next_review_or_disposition_at is not None else None
        now = _timestamp(_utc_now(), "updated_at")
        try:
            with self._transaction() as (_, cursor):
                cursor.execute("SELECT state FROM audit_retention_state WHERE record_ref=%s FOR UPDATE", (record_id,))
                current = _row_mapping(cursor, cursor.fetchone())
                if current is None:
                    raise RecordNotFoundError(record_id)
                if current["state"] == "held" and target in {"disposed", "disposition_pending"}:
                    raise InvalidRecordError("an active hold blocks disposition")
                cursor.execute(
                    "UPDATE audit_retention_state SET retention_class=%s,state=%s,effective_at=%s," 
                    "policy_or_hold_ref=%s,next_review_or_disposition_at=%s,updated_at=%s WHERE record_ref=%s",
                    (_text(retention_class, "retention_class"), target, effective,
                     _text(policy_or_hold_ref, "policy_or_hold_ref"), next_at, now, record_id),
                )
                projected = {"active":"retained","held":"held","archived":"archived","expired":"expired",
                             "disposition_pending":"expired","disposed":"disposed","invalidated":"invalidated"}[target]
                cursor.execute("UPDATE audit_records SET record_state=%s WHERE audit_record_id=%s", (projected, record_id))
                self._append_custody(
                    cursor, chain_id=f"custody:{record_id}", subject_ref=record_id,
                    transition_type="audit_retention_state_changed", actor_identity=actor_identity,
                    occurred_at=effective, result=target, receipt_ref=receipt_ref,
                    details={"policy_or_hold_ref": policy_or_hold_ref, "retention_class": retention_class},
                    created_at=now,
                )
        except (RecordNotFoundError, InvalidRecordError):
            raise
        except Exception as exc:
            raise StorageUnavailableError(f"PostgreSQL retention update failed: {exc}") from exc

    apply_retention = set_retention_state

    def record_access_receipt(self, receipt: Any) -> None:
        value = _mapping(receipt, "receipt")
        required = {"receipt_id","request_id","requester_identity","purpose","policy_decision_ref",
                    "requested_scope","effective_scope","outcome","occurred_at"}
        missing = sorted(required - set(value))
        if missing: raise InvalidRecordError("missing access receipt fields: " + ", ".join(missing))
        outcome = _text(value["outcome"], "outcome")
        if outcome not in ACCESS_OUTCOMES: raise InvalidRecordError(f"unsupported access outcome: {outcome}")
        now = _timestamp(_utc_now(), "created_at")
        try:
            with self._transaction() as (_, cursor):
                cursor.execute(
                    "INSERT INTO audit_access_receipts VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (_text(value["receipt_id"],"receipt_id"),_text(value["request_id"],"request_id"),
                     _canonical_json(_mapping(value["requester_identity"],"requester_identity")),
                     _text(value["purpose"],"purpose"),_text(value["policy_decision_ref"],"policy_decision_ref"),
                     _canonical_json(value["requested_scope"]),_canonical_json(value["effective_scope"]),outcome,
                     _timestamp(value["occurred_at"],"occurred_at"),_canonical_json(value),now),
                )
        except (InvalidRecordError, IntegrityConflictError): raise
        except Exception as exc: raise StorageUnavailableError(f"PostgreSQL receipt append failed: {exc}") from exc

    append_receipt = record_access_receipt

    def store_disclosure_package(self, package: Any, *, delivery_state: str = "local") -> str:
        value = _mapping(package, "package")
        required = {"package_id","request_id","purpose","scope","record_refs","redaction_profile",
                    "generated_at","expiry_or_validity","chain_of_custody_ref"}
        missing = sorted(required - set(value))
        if missing: raise InvalidRecordError("missing disclosure package fields: " + ", ".join(missing))
        state = _text(delivery_state, "delivery_state")
        if state not in DELIVERY_STATES: raise InvalidRecordError(f"unsupported delivery state: {state}")
        digest = _digest(value); now = _timestamp(_utc_now(), "created_at")
        try:
            with self._transaction() as (_, cursor):
                cursor.execute(
                    "INSERT INTO audit_disclosure_packages VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (_text(value["package_id"],"package_id"),_text(value["request_id"],"request_id"),
                     _text(value["purpose"],"purpose"),_canonical_json(value["scope"]),
                     _canonical_json(value["record_refs"]),_text(value["redaction_profile"],"redaction_profile"),
                     _timestamp(value["generated_at"],"generated_at"),
                     _text(value["expiry_or_validity"],"expiry_or_validity"),
                     _text(value["chain_of_custody_ref"],"chain_of_custody_ref"),state,
                     _canonical_json(value),digest,now),
                )
        except (InvalidRecordError, IntegrityConflictError): raise
        except Exception as exc: raise StorageUnavailableError(f"PostgreSQL package append failed: {exc}") from exc
        return digest

    def append_invalidation(
        self, *, invalidation_id: str, record_ref: str, source_correction_or_retraction_ref: str,
        reason: str, effective_at: datetime | str, actor_identity: Mapping[str, Any], receipt_ref: str,
    ) -> None:
        record_id = _text(record_ref,"record_ref"); effective = _timestamp(effective_at,"effective_at")
        now = _timestamp(_utc_now(),"created_at")
        try:
            with self._transaction() as (_, cursor):
                cursor.execute("SELECT audit_record_id FROM audit_records WHERE audit_record_id=%s FOR UPDATE",(record_id,))
                if cursor.fetchone() is None: raise RecordNotFoundError(record_id)
                cursor.execute("INSERT INTO audit_invalidations VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                    (_text(invalidation_id,"invalidation_id"),record_id,
                     _text(source_correction_or_retraction_ref,"source_correction_or_retraction_ref"),
                     _text(reason,"reason"),effective,_canonical_json(_mapping(actor_identity,"actor_identity")),
                     _text(receipt_ref,"receipt_ref"),now))
                cursor.execute("UPDATE audit_records SET record_state='invalidated' WHERE audit_record_id=%s",(record_id,))
                cursor.execute("UPDATE audit_retention_state SET state='invalidated',effective_at=%s," 
                               "policy_or_hold_ref=%s,updated_at=%s WHERE record_ref=%s",
                               (effective,source_correction_or_retraction_ref,now,record_id))
                self._append_custody(cursor,chain_id=f"custody:{record_id}",subject_ref=record_id,
                    transition_type="audit_record_invalidated",actor_identity=actor_identity,
                    occurred_at=effective,result="invalidated",receipt_ref=receipt_ref,
                    details={"invalidation_id":invalidation_id,"reason":reason,
                             "source_correction_or_retraction_ref":source_correction_or_retraction_ref},
                    created_at=now)
        except (RecordNotFoundError,InvalidRecordError): raise
        except Exception as exc: raise StorageUnavailableError(f"PostgreSQL invalidation append failed: {exc}") from exc

    invalidate = append_invalidation

    def verify_integrity(self, audit_record_id: str) -> bool:
        record = dict(self.get_record(audit_record_id)); expected = record.pop("integrity_digest")
        record.pop("created_at",None)
        actual = _digest(record)
        if actual != expected: raise IntegrityConflictError(f"integrity verification failed for {audit_record_id}")
        return True
