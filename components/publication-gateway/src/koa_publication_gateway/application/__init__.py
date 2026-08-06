"""Application primitives for Publication Gateway.

The module contains only deterministic value handling, closed lifecycle checks,
and minimized evidence helpers shared by the five use cases. Domain objects from
B-0055 may satisfy the structural ``as_mapping`` boundary without being imported
here.
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
from types import MappingProxyType
from typing import Any, TypeAlias
from uuid import UUID, uuid5, NAMESPACE_URL

from ..ports import AuditEvidence, AuditSink, PublicationState

JsonScalar: TypeAlias = str | int | float | bool | None
JsonValue: TypeAlias = JsonScalar | Mapping[str, "JsonValue"] | tuple["JsonValue", ...]


class ApplicationError(RuntimeError):
    """Closed application failure with a stable reason code."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.details = freeze_mapping(details or {})


@dataclass(frozen=True, slots=True)
class EvidenceResult:
    retained: bool
    evidence_ref: str | None
    reason_codes: tuple[str, ...]


_PERMITTED_TRANSITIONS = frozenset(
    {
        (PublicationState.RECEIVED, PublicationState.VALIDATING),
        (PublicationState.VALIDATING, PublicationState.AWAITING_AUTHORITY),
        (PublicationState.VALIDATING, PublicationState.DENIED),
        (PublicationState.VALIDATING, PublicationState.BLOCKED),
        (PublicationState.AWAITING_AUTHORITY, PublicationState.AWAITING_REVIEW),
        (PublicationState.AWAITING_AUTHORITY, PublicationState.APPROVED),
        (PublicationState.AWAITING_AUTHORITY, PublicationState.DENIED),
        (PublicationState.AWAITING_AUTHORITY, PublicationState.BLOCKED),
        (PublicationState.AWAITING_REVIEW, PublicationState.APPROVED),
        (PublicationState.AWAITING_REVIEW, PublicationState.DENIED),
        (PublicationState.AWAITING_REVIEW, PublicationState.BLOCKED),
        (PublicationState.APPROVED, PublicationState.STAGING),
        (PublicationState.APPROVED, PublicationState.CANCELLED),
        (PublicationState.STAGING, PublicationState.READY),
        (PublicationState.STAGING, PublicationState.FAILED),
        (PublicationState.READY, PublicationState.PUBLISHING),
        (PublicationState.READY, PublicationState.CANCELLED),
        (PublicationState.PUBLISHING, PublicationState.PUBLISHED),
        (PublicationState.PUBLISHING, PublicationState.PARTIALLY_DELIVERED),
        (PublicationState.PUBLISHING, PublicationState.FAILED),
        (PublicationState.PUBLISHED, PublicationState.REVOKED),
        (PublicationState.PARTIALLY_DELIVERED, PublicationState.REMEDIATING),
        (PublicationState.FAILED, PublicationState.REMEDIATING),
        (PublicationState.REVOKED, PublicationState.REMEDIATING),
        (PublicationState.REMEDIATING, PublicationState.CLOSED),
        # Explicit safe-degradation edges used before delivery begins.
        (PublicationState.RECEIVED, PublicationState.BLOCKED),
        (PublicationState.READY, PublicationState.BLOCKED),
        (PublicationState.BLOCKED, PublicationState.VALIDATING),
        # Receipt persistence can move a known delivery effect into repair.
        (PublicationState.PUBLISHING, PublicationState.REMEDIATING),
    }
)


def ensure_transition(current: PublicationState, target: PublicationState) -> None:
    if current == target:
        return
    if (current, target) not in _PERMITTED_TRANSITIONS:
        raise ApplicationError(
            "invalid_state_transition",
            f"publication state cannot move from {current.value} to {target.value}",
        )


def as_mapping(value: object, *, name: str) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    converter = getattr(value, "as_mapping", None)
    if callable(converter):
        converted = converter()
        if isinstance(converted, Mapping):
            return converted
    raise ApplicationError("invalid_input", f"{name} must be a mapping-compatible value")


def freeze(value: Any) -> JsonValue:
    if isinstance(value, Mapping):
        return MappingProxyType({str(key): freeze(item) for key, item in sorted(value.items())})
    if isinstance(value, (list, tuple)):
        return tuple(freeze(item) for item in value)
    if isinstance(value, datetime):
        return isoformat(value)
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise ApplicationError(
        "non_json_value",
        f"unsupported value type in application boundary: {type(value).__name__}",
    )


def freeze_mapping(value: Mapping[str, Any]) -> Mapping[str, JsonValue]:
    frozen = freeze(value)
    if not isinstance(frozen, Mapping):
        raise ApplicationError("invalid_mapping", "expected a mapping")
    return frozen


def thaw(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [thaw(item) for item in value]
    return value


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        thaw(value),
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def fingerprint(value: Any) -> str:
    return "sha256:" + sha256(canonical_json(value)).hexdigest()


def deterministic_id(prefix: str, *parts: Any) -> str:
    material = "\x1f".join(
        part if isinstance(part, str) else canonical_json(part).decode("utf-8")
        for part in parts
    )
    return f"{prefix}:{uuid5(NAMESPACE_URL, material)}"


def isoformat(value: datetime) -> str:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ApplicationError("untrusted_time", "timestamps must be timezone-aware")
    return value.isoformat()


def require_text(mapping: Mapping[str, Any], key: str, *, code: str = "invalid_request") -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ApplicationError(code, f"{key} is required")
    return value.strip()


def require_mapping(
    mapping: Mapping[str, Any],
    key: str,
    *,
    code: str = "invalid_request",
) -> Mapping[str, Any]:
    value = mapping.get(key)
    if not isinstance(value, Mapping):
        raise ApplicationError(code, f"{key} must be an object")
    return value


def require_sequence(
    mapping: Mapping[str, Any],
    key: str,
    *,
    non_empty: bool = False,
    code: str = "invalid_request",
) -> tuple[Any, ...]:
    value = mapping.get(key)
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise ApplicationError(code, f"{key} must be an array")
    result = tuple(value)
    if non_empty and not result:
        raise ApplicationError(code, f"{key} must not be empty")
    return result


def require_uuid(value: str, *, field: str) -> str:
    try:
        return str(UUID(value))
    except (ValueError, AttributeError) as exc:
        raise ApplicationError("invalid_request", f"{field} must be a UUID") from exc


def request_id(request: Mapping[str, Any]) -> str:
    return require_text(request, "request_id")


def idempotency_key(request: Mapping[str, Any]) -> str:
    context = require_mapping(request, "request_context")
    return require_uuid(require_text(context, "idempotency_id"), field="request_context.idempotency_id")


def correlation_id(request: Mapping[str, Any]) -> str:
    return require_text(require_mapping(request, "request_context"), "correlation_id")


def selection_ids(request: Mapping[str, Any]) -> tuple[str, ...]:
    selection = require_mapping(request, "selection")
    elements = require_sequence(selection, "selected_elements", non_empty=True)
    identifiers: list[str] = []
    for item in elements:
        if not isinstance(item, Mapping):
            raise ApplicationError("invalid_request", "selected_elements entries must be objects")
        identifiers.append(require_text(item, "selection_id"))
    if len(set(identifiers)) != len(identifiers):
        raise ApplicationError("invalid_request", "selection identifiers must be unique")
    return tuple(identifiers)


def transformation_ids(request: Mapping[str, Any]) -> tuple[str, ...]:
    plan = require_mapping(request, "transformation_plan")
    transformations = require_sequence(plan, "transformations")
    identifiers: list[str] = []
    for item in transformations:
        if not isinstance(item, Mapping):
            raise ApplicationError("invalid_request", "transformations entries must be objects")
        identifiers.append(require_text(item, "transformation_id"))
    if len(set(identifiers)) != len(identifiers):
        raise ApplicationError("invalid_request", "transformation identifiers must be unique")
    return tuple(identifiers)


def audience_scope_refs(request: Mapping[str, Any]) -> tuple[str, ...]:
    intent = require_mapping(request, "publication_intent")
    values = require_sequence(intent, "audience_scope_refs", non_empty=True)
    refs = tuple(str(value) for value in values)
    if any(not value for value in refs) or len(set(refs)) != len(refs):
        raise ApplicationError("invalid_request", "audience scope must contain unique references")
    return refs


def submit_audit(
    sink: AuditSink,
    *,
    request: Mapping[str, Any],
    event_type: str,
    outcome: str,
    occurred_at: datetime,
    payload: Mapping[str, Any],
    subject_refs: tuple[str, ...],
    evidence_refs: tuple[str, ...] = (),
) -> EvidenceResult:
    rid = request_id(request)
    cid = correlation_id(request)
    event = AuditEvidence(
        evidence_id=deterministic_id("audit-event", rid, event_type, outcome, payload),
        event_type=event_type,
        correlation_id=cid,
        occurred_at=occurred_at,
        request_id=rid,
        outcome=outcome,
        subject_refs=subject_refs,
        payload=freeze_mapping(payload),
        evidence_refs=evidence_refs,
        restricted=True,
    )
    if not sink.is_available():
        return EvidenceResult(False, None, ("audit_unavailable",))
    try:
        submission = sink.submit(event)
    except Exception as exc:
        return EvidenceResult(False, None, ("audit_submission_failed", type(exc).__name__))
    return EvidenceResult(submission.retained, submission.evidence_ref, submission.reason_codes)


__all__ = [
    "ApplicationError",
    "EvidenceResult",
    "JsonValue",
    "as_mapping",
    "audience_scope_refs",
    "canonical_json",
    "correlation_id",
    "deterministic_id",
    "ensure_transition",
    "fingerprint",
    "freeze",
    "freeze_mapping",
    "idempotency_key",
    "isoformat",
    "request_id",
    "require_mapping",
    "require_sequence",
    "require_text",
    "require_uuid",
    "selection_ids",
    "submit_audit",
    "thaw",
    "transformation_ids",
]
