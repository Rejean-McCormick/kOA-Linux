"""Use case for authenticated, registered Audit Broker ingestion."""

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from datetime import datetime
from hashlib import sha256
import json
from typing import Any, Mapping, Sequence

from ..ports.clock import Clock
from ..ports.event_store import (
    AuditDocument,
    EventStore,
    IngestionOutcome,
    IngestionReceipt,
)
from ..ports.identity_context import IdentityContextPort, IdentityStatus

INTERFACE_VERSION = "1.0.0"
_CORE_FIELDS = frozenset(
    {
        "audit_record_id",
        "event_class_id",
        "producer_component_id",
        "producer_identity",
        "occurred_at",
        "subject_references",
        "action_or_transition",
        "outcome",
        "purpose",
        "classification",
        "retention_class",
        "retention_policy_ref",
        "correlation_id",
        "source_receipt_or_evidence_refs",
        "event_payload",
    }
)


@dataclass(frozen=True, slots=True)
class RegisteredEventClass:
    event_class_id: str
    version: str
    allowed_producer_components: frozenset[str]
    required_payload_fields: frozenset[str]
    allowed_payload_fields: frozenset[str]

    def __post_init__(self) -> None:
        if not self.event_class_id or not self.version:
            raise ValueError("registered event identity and version are required")
        if not self.allowed_producer_components:
            raise ValueError("at least one allowed producer is required")
        if not self.required_payload_fields <= self.allowed_payload_fields:
            raise ValueError("required payload fields must be allowed")


@dataclass(frozen=True, slots=True)
class AppendEventCommand:
    event: object
    idempotency_key: str
    interface_version: str = INTERFACE_VERSION


@dataclass(frozen=True, slots=True)
class AppendEventResult:
    outcome: IngestionOutcome
    receipt_id: str
    occurred_at: datetime
    record_ref: str | None = None
    custody_ref: str | None = None
    duplicate: bool = False
    reason_codes: tuple[str, ...] = ()


class AuditReceiptPersistenceError(RuntimeError):
    """A critical ingestion outcome could not be durably receipted."""


def _aware(value: datetime, name: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")
    return value


def _jsonable(value: Any) -> Any:
    if isinstance(value, datetime):
        return _aware(value, "datetime").isoformat()
    if isinstance(value, Mapping):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_jsonable(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise TypeError(f"unsupported audit value: {type(value).__name__}")


def _event_document(event: object) -> dict[str, Any]:
    if isinstance(event, Mapping):
        raw = dict(event)
    elif is_dataclass(event):
        raw = asdict(event)
    else:
        converter = next(
            (
                getattr(event, name)
                for name in ("to_audit_record", "to_record", "as_record")
                if callable(getattr(event, name, None))
            ),
            None,
        )
        if converter is not None:
            converted = converter()
            if not isinstance(converted, Mapping):
                raise TypeError("event conversion must return a mapping")
            raw = dict(converted)
        else:
            raw = {
                field: getattr(event, field)
                for field in _CORE_FIELDS
                if hasattr(event, field)
            }
    return _jsonable(raw)


def _stable_receipt_id(idempotency_key: str, outcome: IngestionOutcome) -> str:
    digest = sha256(f"{idempotency_key}\0{outcome.value}".encode()).hexdigest()
    return f"audit-ingestion-{digest}"


def _reasoned_result(
    *,
    store: EventStore,
    command: AppendEventCommand,
    document: Mapping[str, Any],
    occurred_at: datetime,
    outcome: IngestionOutcome,
    reason_codes: Sequence[str],
    identity_ref: str | None,
    record_ref: str | None = None,
    custody_ref: str | None = None,
    duplicate: bool = False,
) -> AppendEventResult:
    receipt_id = _stable_receipt_id(command.idempotency_key, outcome)
    receipt = IngestionReceipt(
        receipt_id=receipt_id,
        idempotency_key=command.idempotency_key,
        event_class_id=str(document.get("event_class_id", "unknown")),
        producer_component_id=str(document.get("producer_component_id", "unknown")),
        producer_identity_ref=identity_ref,
        correlation_id=(
            str(document["correlation_id"]) if document.get("correlation_id") else None
        ),
        outcome=outcome,
        occurred_at=occurred_at,
        record_ref=record_ref,
        custody_ref=custody_ref,
        reason_codes=tuple(reason_codes),
    )
    try:
        store.record_ingestion_receipt(receipt)
    except Exception as exc:  # adapter failure is a critical closed failure
        raise AuditReceiptPersistenceError("ingestion receipt was not durable") from exc
    return AppendEventResult(
        outcome=outcome,
        receipt_id=receipt_id,
        occurred_at=occurred_at,
        record_ref=record_ref,
        custody_ref=custody_ref,
        duplicate=duplicate,
        reason_codes=tuple(reason_codes),
    )


class AppendEventHandler:
    """Validate and append one registered event without acquiring source authority."""

    def __init__(
        self,
        *,
        store: EventStore,
        identities: IdentityContextPort,
        clock: Clock,
        registry: Mapping[str, RegisteredEventClass],
    ) -> None:
        self._store = store
        self._identities = identities
        self._clock = clock
        self._registry = dict(registry)

    def execute(self, command: AppendEventCommand) -> AppendEventResult:
        now = _aware(self._clock.now(), "clock.now()")
        if not command.idempotency_key.strip():
            raise ValueError("idempotency_key is required")
        try:
            document = _event_document(command.event)
        except (TypeError, ValueError) as exc:
            document = {}
            return _reasoned_result(
                store=self._store,
                command=command,
                document=document,
                occurred_at=now,
                outcome=IngestionOutcome.REJECTED,
                reason_codes=("invalid_event_document", type(exc).__name__),
                identity_ref=None,
            )

        missing = sorted(field for field in _CORE_FIELDS if field not in document)
        unknown = sorted(set(document) - _CORE_FIELDS)
        if missing or unknown:
            reasons = tuple(
                [f"missing:{field}" for field in missing]
                + [f"unknown:{field}" for field in unknown]
            )
            return _reasoned_result(
                store=self._store,
                command=command,
                document=document,
                occurred_at=now,
                outcome=IngestionOutcome.REJECTED,
                reason_codes=reasons,
                identity_ref=None,
            )

        event_class_id = str(document["event_class_id"])
        registered = self._registry.get(event_class_id)
        if registered is None:
            return _reasoned_result(
                store=self._store,
                command=command,
                document=document,
                occurred_at=now,
                outcome=IngestionOutcome.REJECTED,
                reason_codes=("unregistered_event_class",),
                identity_ref=None,
            )
        if command.interface_version != INTERFACE_VERSION or registered.version != INTERFACE_VERSION:
            return _reasoned_result(
                store=self._store,
                command=command,
                document=document,
                occurred_at=now,
                outcome=IngestionOutcome.REJECTED,
                reason_codes=("unsupported_interface_or_event_version",),
                identity_ref=None,
            )

        producer_component_id = str(document["producer_component_id"])
        if producer_component_id not in registered.allowed_producer_components:
            return _reasoned_result(
                store=self._store,
                command=command,
                document=document,
                occurred_at=now,
                outcome=IngestionOutcome.REJECTED,
                reason_codes=("producer_not_registered_for_event_class",),
                identity_ref=None,
            )

        payload = document["event_payload"]
        if not isinstance(payload, Mapping):
            return _reasoned_result(
                store=self._store,
                command=command,
                document=document,
                occurred_at=now,
                outcome=IngestionOutcome.REJECTED,
                reason_codes=("event_payload_not_mapping",),
                identity_ref=None,
            )
        payload_fields = frozenset(str(key) for key in payload)
        if not registered.required_payload_fields <= payload_fields:
            missing_payload = sorted(registered.required_payload_fields - payload_fields)
            return _reasoned_result(
                store=self._store,
                command=command,
                document=document,
                occurred_at=now,
                outcome=IngestionOutcome.REJECTED,
                reason_codes=tuple(f"missing_payload:{field}" for field in missing_payload),
                identity_ref=None,
            )
        if not payload_fields <= registered.allowed_payload_fields:
            excess = sorted(payload_fields - registered.allowed_payload_fields)
            return _reasoned_result(
                store=self._store,
                command=command,
                document=document,
                occurred_at=now,
                outcome=IngestionOutcome.REJECTED,
                reason_codes=tuple(f"unauthorized_payload:{field}" for field in excess),
                identity_ref=None,
            )

        occurred_at_raw = document["occurred_at"]
        if not isinstance(occurred_at_raw, str):
            return _reasoned_result(
                store=self._store,
                command=command,
                document=document,
                occurred_at=now,
                outcome=IngestionOutcome.REJECTED,
                reason_codes=("occurred_at_not_serialized",),
                identity_ref=None,
            )
        try:
            _aware(datetime.fromisoformat(occurred_at_raw), "occurred_at")
        except ValueError:
            return _reasoned_result(
                store=self._store,
                command=command,
                document=document,
                occurred_at=now,
                outcome=IngestionOutcome.REJECTED,
                reason_codes=("occurred_at_invalid",),
                identity_ref=None,
            )

        identity_raw = document["producer_identity"]
        if not isinstance(identity_raw, Mapping):
            return _reasoned_result(
                store=self._store,
                command=command,
                document=document,
                occurred_at=now,
                outcome=IngestionOutcome.REJECTED,
                reason_codes=("producer_identity_invalid",),
                identity_ref=None,
            )
        verification = self._identities.verify_producer(
            identity_raw,
            component_id=producer_component_id,
            event_class_id=event_class_id,
            operation="submit_audit_event",
            at=now,
        )
        if verification.status is IdentityStatus.UNTRUSTED:
            stored = self._store.quarantine_event(
                document,
                received_at=now,
                idempotency_key=command.idempotency_key,
                reason_codes=verification.reason_codes or ("untrusted_producer",),
            )
            return _reasoned_result(
                store=self._store,
                command=command,
                document=document,
                occurred_at=now,
                outcome=IngestionOutcome.QUARANTINED,
                reason_codes=verification.reason_codes or ("untrusted_producer",),
                identity_ref=verification.identity_ref,
                record_ref=stored.quarantine_ref,
                custody_ref=stored.custody_ref,
                duplicate=stored.duplicate,
            )
        if not verification.authenticated:
            reason = {
                IdentityStatus.REVOKED: "producer_revoked",
                IdentityStatus.EXPIRED: "producer_identity_expired",
                IdentityStatus.UNAVAILABLE: "identity_authority_unavailable",
            }.get(verification.status, "producer_not_authenticated")
            return _reasoned_result(
                store=self._store,
                command=command,
                document=document,
                occurred_at=now,
                outcome=IngestionOutcome.REJECTED,
                reason_codes=verification.reason_codes or (reason,),
                identity_ref=verification.identity_ref,
            )

        stored = self._store.append_event(
            document,
            received_at=now,
            idempotency_key=command.idempotency_key,
        )
        return _reasoned_result(
            store=self._store,
            command=command,
            document=document,
            occurred_at=now,
            outcome=IngestionOutcome.ACCEPTED,
            reason_codes=(),
            identity_ref=verification.identity_ref,
            record_ref=stored.record_id,
            custody_ref=stored.custody_ref,
            duplicate=stored.duplicate,
        )
