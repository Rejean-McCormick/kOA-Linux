"""Terminal evidence for the shared UCKK adapter boundary.

These receipts describe one adapter call.  They never replace the canonical
publication or import receipts produced by the direction-specific workflows.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
from hashlib import sha256
import json
import re
from types import MappingProxyType
from typing import Any, Mapping, Sequence


class Direction(StrEnum):
    """The two UCKK directions remain distinct authority paths."""

    PUBLISH_TO_UCKK = "publish_to_uckk"
    IMPORT_FROM_UCKK = "import_from_uckk"


class TerminalOutcome(StrEnum):
    """Terminal result of one adapter boundary attempt sequence."""

    SUCCEEDED = "succeeded"
    QUEUED = "queued"
    REJECTED = "rejected"
    FAILED = "failed"
    QUARANTINED = "quarantined"
    UNKNOWN_OUTCOME = "unknown_outcome"
    PARTIAL_REQUIRES_REVIEW = "partial_requires_review"


class ReceiptValidationError(ValueError):
    """Raised when terminal evidence is incomplete or contradictory."""


_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{2,255}$")
_REASON_RE = re.compile(r"^[a-z][a-z0-9_]{2,127}$")
_DIGEST_RE = re.compile(r"^sha256:[a-f0-9]{64}$")
_TIMESTAMP_RE = re.compile(
    r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?Z$"
)
_FAILURE_CLASSES = frozenset(
    {
        "timeout",
        "unavailable",
        "rate_limited",
        "remote_5xx",
        "authentication",
        "authorization",
        "validation",
        "compatibility",
        "integrity",
        "ambiguous_outcome",
        "circuit_open",
        "unknown",
    }
)


def canonical_json(value: Any) -> bytes:
    """Return the deterministic JSON representation used for evidence digests."""

    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def payload_digest(value: Any) -> str:
    return "sha256:" + sha256(canonical_json(value)).hexdigest()


def utc_timestamp(value: datetime) -> str:
    if value.tzinfo is None:
        raise ReceiptValidationError("timestamps must be timezone-aware")
    return value.astimezone(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z"
    )


def _validate_timestamp(value: str, field: str) -> None:
    if not isinstance(value, str) or not _TIMESTAMP_RE.fullmatch(value):
        raise ReceiptValidationError(f"{field} must be an RFC 3339 UTC timestamp")


def _validate_identifier(value: str, field: str) -> None:
    if not isinstance(value, str) or not _ID_RE.fullmatch(value):
        raise ReceiptValidationError(f"{field} is invalid")


def _immutable_mapping(value: Mapping[str, Any]) -> Mapping[str, Any]:
    # A JSON round-trip also rejects unserialisable provider objects.
    copy = json.loads(canonical_json(value))
    return MappingProxyType(copy)


@dataclass(frozen=True, slots=True)
class ItemOutcome:
    """Visible per-item evidence when a remote result is partial."""

    item_ref: str
    outcome: str
    reason_code: str | None = None

    def __post_init__(self) -> None:
        _validate_identifier(self.item_ref, "item_ref")
        if self.outcome not in {"succeeded", "failed", "rejected", "unknown"}:
            raise ReceiptValidationError("invalid item outcome")
        if self.outcome != "succeeded":
            if self.reason_code is None or not _REASON_RE.fullmatch(self.reason_code):
                raise ReceiptValidationError(
                    "a non-success item outcome requires a valid reason_code"
                )
        elif self.reason_code is not None:
            raise ReceiptValidationError(
                "a successful item outcome cannot carry a reason_code"
            )

    def as_dict(self) -> dict[str, Any]:
        return {
            "item_ref": self.item_ref,
            "outcome": self.outcome,
            "reason_code": self.reason_code,
        }


@dataclass(frozen=True, slots=True)
class TerminalReceipt:
    """Immutable terminal evidence for one bounded UCKK boundary call."""

    receipt_id: str
    direction: Direction
    operation: str
    correlation_id: str
    idempotency_key: str
    request_digest: str
    outcome: TerminalOutcome
    attempt_count: int
    started_at: str
    completed_at: str
    authoritative_success: bool = False
    external_reference: str | None = None
    failure_class: str | None = None
    reason_code: str | None = None
    retry_exhausted: bool = False
    response_digest: str | None = None
    item_outcomes: tuple[ItemOutcome, ...] = ()

    def __post_init__(self) -> None:
        for field, value in (
            ("receipt_id", self.receipt_id),
            ("operation", self.operation),
            ("correlation_id", self.correlation_id),
            ("idempotency_key", self.idempotency_key),
        ):
            _validate_identifier(value, field)
        if not _DIGEST_RE.fullmatch(self.request_digest):
            raise ReceiptValidationError("request_digest is invalid")
        if self.response_digest is not None and not _DIGEST_RE.fullmatch(
            self.response_digest
        ):
            raise ReceiptValidationError("response_digest is invalid")
        if self.attempt_count < 0 or self.attempt_count > 20:
            raise ReceiptValidationError("attempt_count must be between 0 and 20")
        _validate_timestamp(self.started_at, "started_at")
        _validate_timestamp(self.completed_at, "completed_at")
        if self.completed_at < self.started_at:
            raise ReceiptValidationError("completed_at precedes started_at")
        if self.authoritative_success:
            raise ReceiptValidationError(
                "UCKK adapter evidence cannot declare authoritative success"
            )
        if self.external_reference is not None:
            _validate_identifier(self.external_reference, "external_reference")
        failed = self.outcome in {
            TerminalOutcome.REJECTED,
            TerminalOutcome.FAILED,
            TerminalOutcome.QUARANTINED,
            TerminalOutcome.UNKNOWN_OUTCOME,
            TerminalOutcome.PARTIAL_REQUIRES_REVIEW,
        }
        if failed:
            if self.failure_class not in _FAILURE_CLASSES:
                raise ReceiptValidationError(
                    "non-success outcome requires a classified failure"
                )
            if self.reason_code is None or not _REASON_RE.fullmatch(self.reason_code):
                raise ReceiptValidationError(
                    "non-success outcome requires a valid reason_code"
                )
        elif self.failure_class is not None or self.reason_code is not None:
            raise ReceiptValidationError(
                "successful or queued evidence cannot carry failure fields"
            )
        if self.outcome is TerminalOutcome.PARTIAL_REQUIRES_REVIEW:
            if not self.item_outcomes:
                raise ReceiptValidationError(
                    "partial outcome requires visible per-item outcomes"
                )
            if all(item.outcome == "succeeded" for item in self.item_outcomes):
                raise ReceiptValidationError(
                    "partial outcome must include at least one non-success item"
                )
        elif self.item_outcomes:
            raise ReceiptValidationError(
                "per-item outcomes are only valid for partial results"
            )

    def as_dict(self) -> Mapping[str, Any]:
        return _immutable_mapping(
            {
                "artifact_class": "uckk_adapter_terminal_receipt",
                "receipt_id": self.receipt_id,
                "direction": self.direction.value,
                "operation": self.operation,
                "correlation_id": self.correlation_id,
                "idempotency_key": self.idempotency_key,
                "request_digest": self.request_digest,
                "outcome": self.outcome.value,
                "terminal": True,
                "attempt_count": self.attempt_count,
                "started_at": self.started_at,
                "completed_at": self.completed_at,
                "authoritative_success": self.authoritative_success,
                "external_reference": self.external_reference,
                "failure_class": self.failure_class,
                "reason_code": self.reason_code,
                "retry_exhausted": self.retry_exhausted,
                "response_digest": self.response_digest,
                "item_outcomes": [item.as_dict() for item in self.item_outcomes],
            }
        )


def build_terminal_receipt(
    *,
    direction: Direction,
    operation: str,
    correlation_id: str,
    idempotency_key: str,
    request: Mapping[str, Any],
    outcome: TerminalOutcome,
    attempt_count: int,
    started_at: datetime,
    completed_at: datetime,
    response: Mapping[str, Any] | None = None,
    external_reference: str | None = None,
    failure_class: str | None = None,
    reason_code: str | None = None,
    retry_exhausted: bool = False,
    item_outcomes: Sequence[ItemOutcome] = (),
) -> TerminalReceipt:
    request_hash = payload_digest(request)
    response_hash = payload_digest(response) if response is not None else None
    core = {
        "direction": direction.value,
        "operation": operation,
        "correlation_id": correlation_id,
        "idempotency_key": idempotency_key,
        "request_digest": request_hash,
        "outcome": outcome.value,
        "attempt_count": attempt_count,
        "started_at": utc_timestamp(started_at),
        "completed_at": utc_timestamp(completed_at),
        "external_reference": external_reference,
        "failure_class": failure_class,
        "reason_code": reason_code,
        "retry_exhausted": retry_exhausted,
        "response_digest": response_hash,
        "item_outcomes": [item.as_dict() for item in item_outcomes],
    }
    receipt_id = "uckk-adapter-" + sha256(canonical_json(core)).hexdigest()
    return TerminalReceipt(
        receipt_id=receipt_id,
        direction=direction,
        operation=operation,
        correlation_id=correlation_id,
        idempotency_key=idempotency_key,
        request_digest=request_hash,
        outcome=outcome,
        attempt_count=attempt_count,
        started_at=core["started_at"],
        completed_at=core["completed_at"],
        external_reference=external_reference,
        failure_class=failure_class,
        reason_code=reason_code,
        retry_exhausted=retry_exhausted,
        response_digest=response_hash,
        item_outcomes=tuple(item_outcomes),
    )


def build_dead_letter_record(
    *,
    direction: Direction,
    message_id: str,
    payload: Mapping[str, Any],
    first_failed_at: datetime,
    quarantined_at: datetime,
    attempt_count: int,
    failure_class: str,
    reason_code: str,
    error_summary: str,
    permanent: bool,
    authority_domain: str,
    tenant_id: str | None = None,
    payload_reference: str | None = None,
    maximum_retention_days: int = 90,
) -> Mapping[str, Any]:
    """Build a schema-compatible, visible dead-letter record.

    Redrive is deliberately never automatic.  Compatibility and authorization
    must be rechecked by the direction-specific workflow before redrive.
    """

    _validate_identifier(message_id, "message_id")
    _validate_identifier(authority_domain, "authority_domain")
    if attempt_count < 1:
        raise ReceiptValidationError("attempt_count must be positive")
    if maximum_retention_days < 1:
        raise ReceiptValidationError("maximum_retention_days must be positive")
    if not _REASON_RE.fullmatch(reason_code):
        raise ReceiptValidationError("reason_code is invalid")
    if not isinstance(error_summary, str) or not error_summary.strip():
        raise ReceiptValidationError("error_summary is required")

    dead_letter_class = {
        "validation": "permanent_validation",
        "integrity": "corruption",
        "compatibility": "compatibility",
        "authorization": "authorization",
        "authentication": "authorization",
    }.get(failure_class)
    if dead_letter_class is None:
        dead_letter_class = "unknown" if permanent else "transient_exhausted"

    digest = payload_digest(payload)
    record_core = {
        "source_queue_id": f"uckk-{direction.value}",
        "message_id": message_id,
        "authority_domain": authority_domain,
        "tenant_id": tenant_id,
        "payload_digest": digest,
        "payload_reference": payload_reference,
        "first_failed_at": utc_timestamp(first_failed_at),
        "quarantined_at": utc_timestamp(quarantined_at),
        "attempt_count": attempt_count,
        "failure": {
            "class": dead_letter_class,
            "permanent": permanent,
            "reason_code": reason_code,
            "last_error_summary": error_summary.strip()[:2048],
        },
    }
    record_id = "uckk-dlq-" + sha256(canonical_json(record_core)).hexdigest()
    return _immutable_mapping(
        {
            "$schema": (
                "https://schemas.koa.local/artifact-contracts/"
                "dead-letter-record.schema.json"
            ),
            "artifact_class": "dead_letter_record",
            "record_id": record_id,
            **record_core,
            "status": "quarantined",
            "redrive": {
                "automatic": False,
                "requires_compatibility_check": True,
                "requires_authorization": True,
                "redrive_count": 0,
                "last_redrive_receipt_ref": None,
            },
            "retention": {
                "retain_until_closed": True,
                "maximum_days": maximum_retention_days,
            },
            "closure": {
                "closed": False,
                "outcome": "pending",
                "receipt_ref": None,
            },
        }
    )
