"""Deterministic, secret-free receipts for Resource Governor decisions."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
import hashlib
import json
import math
import re
from types import MappingProxyType
from typing import Iterable, Mapping


COMPONENT_ID = "resource_governor"
COMPONENT_VERSION = "1.0.0"
COMPONENT_CONTRACT_REF = "docs/contracts/components/resource-governor.component.json"
RECEIPT_SCHEMA_VERSION = "2.0.0"
JSONScalar = str | int | float | bool | None


class ReceiptError(ValueError):
    """Raised when a receipt would be ambiguous, unsafe, or non-conformant."""


class ReceiptPathUnavailable(ReceiptError):
    """Raised when a critical transition cannot produce its required receipt."""


class TransitionKind(StrEnum):
    RESOURCE_ADMISSION = "resource_admission"
    ENVELOPE_ACTIVATION = "resource_envelope_activation"
    GOVERNED_OVERRIDE = "governed_resource_override"
    FORCED_TERMINATION = "forced_termination"
    EMERGENCY_DEGRADATION = "emergency_resource_degradation"
    RECOVERY = "resource_recovery"
    ROLLBACK = "resource_envelope_rollback"


class AdmissionState(StrEnum):
    ADMITTED = "admitted"
    QUEUED = "queued"
    THROTTLED = "throttled"
    PAUSED = "paused"
    DENIED = "denied"
    BLOCKED = "blocked"


class DecisionOutcome(StrEnum):
    ADMITTED = "admitted"
    QUEUED = "queued"
    THROTTLED = "throttled"
    PAUSED = "paused"
    REJECTED = "rejected"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"
    DEGRADED = "degraded"
    CANCELLED = "cancelled"
    ROLLBACK_REQUIRED = "rollback_required"
    FORWARD_REPAIR_REQUIRED = "forward_repair_required"


_CRITICAL_TRANSITIONS = frozenset(
    {
        TransitionKind.ENVELOPE_ACTIVATION,
        TransitionKind.GOVERNED_OVERRIDE,
        TransitionKind.FORCED_TERMINATION,
        TransitionKind.EMERGENCY_DEGRADATION,
        TransitionKind.RECOVERY,
        TransitionKind.ROLLBACK,
    }
)
_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/@+\-]{0,255}$")
_REASON = re.compile(r"^[A-Z][A-Z0-9_:\-]{1,127}$")
_SNAKE = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")
_ACTION = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/\-]{0,255}$")
_REF = re.compile(r"^(?!(?:/|.*(?:^|/)\.\.(?:/|$)))(?:[^#\s]+(?:#(?:/.*)?)?|(?:DOC|DEC|REQ|LOCK|ADR|TEST|EVID|EXC)-[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9]{3})$")
_SECRET = re.compile(
    r"(?:^|_)(?:password|passphrase|private_key|secret|token|credential|payload|business_data|key_material)(?:$|_)",
    re.IGNORECASE,
)
_SCOPE_KINDS = frozenset(
    {
        "profile",
        "profile_overlay",
        "component",
        "tenant",
        "node",
        "workspace",
        "artifact",
        "release_set",
        "operation",
        "integration",
        "user_session",
    }
)


def _utc(value: datetime, field_name: str) -> datetime:
    if value.tzinfo is None:
        raise ReceiptError(f"{field_name} must be timezone-aware")
    return value.astimezone(UTC)


def _timestamp(value: datetime) -> str:
    return _utc(value, "timestamp").isoformat().replace("+00:00", "Z")


def _identifier(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not _IDENTIFIER.fullmatch(normalized):
        raise ReceiptError(f"{field_name} is not a valid bounded identifier")
    return normalized


def _action(value: str) -> str:
    normalized = value.strip()
    if not _ACTION.fullmatch(normalized):
        raise ReceiptError("action is not a valid bounded action identifier")
    return normalized


def _snake(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not _SNAKE.fullmatch(normalized):
        raise ReceiptError(f"{field_name} must be a snake_case identifier")
    return normalized


def _reference(value: str, field_name: str) -> str:
    normalized = value.strip()
    if len(normalized) < 3 or len(normalized) > 1024 or not _REF.fullmatch(normalized):
        raise ReceiptError(f"{field_name} is not a canonical reference")
    return normalized


def _reason(value: str) -> str:
    normalized = value.strip()
    if not _REASON.fullmatch(normalized):
        raise ReceiptError("reason codes must be stable uppercase identifiers")
    return normalized


def _references(values: Iterable[str], field_name: str) -> tuple[str, ...]:
    return tuple(sorted({_reference(value, field_name) for value in values}))


def _trace_ids(values: Iterable[str], prefix: str, field_name: str) -> tuple[str, ...]:
    pattern = re.compile(rf"^{prefix}-[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9]{{3}}$")
    result = tuple(sorted(set(values)))
    if any(not pattern.fullmatch(value) for value in result):
        raise ReceiptError(f"{field_name} contains a non-canonical identifier")
    return result


def _safe_limits(values: Mapping[str, JSONScalar] | None) -> Mapping[str, JSONScalar]:
    if values is None:
        return MappingProxyType({})
    result: dict[str, JSONScalar] = {}
    for key, value in values.items():
        if not _SNAKE.fullmatch(key) or _SECRET.search(key):
            raise ReceiptError(f"resource limit key is prohibited or invalid: {key}")
        if not isinstance(value, (str, int, float, bool)) or isinstance(value, type(None)):
            raise ReceiptError(f"resource limit values must be JSON scalars: {key}")
        if isinstance(value, str):
            if not value or len(value) > 256:
                raise ReceiptError(f"resource limit string is invalid: {key}")
            normalized: JSONScalar = value
        elif isinstance(value, bool):
            normalized = value
        else:
            numeric = float(value)
            if not math.isfinite(numeric):
                raise ReceiptError(f"resource limit number is not finite: {key}")
            # The canonical schema currently uses overlapping number/integer oneOf branches.
            # Numeric limits are encoded as exact decimal strings to remain unambiguous.
            normalized = str(value)
        result[key] = normalized
    return MappingProxyType(dict(sorted(result.items())))


def _scope(kind: str, identifier: str | None) -> dict[str, str]:
    if kind == "global":
        if identifier is not None:
            raise ReceiptError("global scope cannot carry an identifier")
        return {"kind": "global"}
    if kind not in _SCOPE_KINDS or identifier is None:
        raise ReceiptError("non-global scope requires a registered kind and identifier")
    return {"kind": kind, "id": _identifier(identifier, "scope_id")}


@dataclass(frozen=True, slots=True)
class ResourceDecisionReceipt:
    """Immutable receipt whose serialized form follows decision-receipt schema 2.0.0."""

    payload: Mapping[str, object]

    def __post_init__(self) -> None:
        object.__setattr__(self, "payload", MappingProxyType(dict(self.payload)))

    @property
    def receipt_id(self) -> str:
        return str(self.payload["receipt_id"])

    def to_dict(self) -> dict[str, object]:
        return json.loads(json.dumps(dict(self.payload), sort_keys=True, ensure_ascii=False))

    def canonical_json(self) -> str:
        return json.dumps(dict(self.payload), sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def create_resource_receipt(
    *,
    transition_kind: TransitionKind,
    producer_instance_id: str,
    request_id: str,
    correlation_id: str,
    subject_ref: str,
    resource_ref: str,
    action: str,
    scope_kind: str,
    scope_id: str | None,
    outcome: DecisionOutcome,
    reason_codes: Iterable[str],
    decided_at: datetime,
    receipt_path_ready: bool,
    requested_at: datetime | None = None,
    admission_state: AdmissionState | None = None,
    resource_scope: str | None = None,
    envelope_ref: str | None = None,
    queue_ref: str | None = None,
    priority_class: str | None = None,
    effective_limits: Mapping[str, JSONScalar] | None = None,
    from_state: str | None = None,
    to_state: str | None = None,
    transition_status: str | None = None,
    transition_id: str | None = None,
    contract_refs: Iterable[str] = (COMPONENT_CONTRACT_REF,),
    decision_refs: Iterable[str] = (),
    requirement_refs: Iterable[str] = ("REQ-RG-001",),
    lock_refs: Iterable[str] = ("LOCK-GOV-001",),
    test_refs: Iterable[str] = (),
    evidence_refs: Iterable[str] = (),
) -> ResourceDecisionReceipt:
    """Create a deterministic resource receipt and fail closed when required."""
    kind = TransitionKind(transition_kind)
    if kind in _CRITICAL_TRANSITIONS and not receipt_path_ready:
        raise ReceiptPathUnavailable("critical resource transition requires a durable receipt path")

    decided = _utc(decided_at, "decided_at")
    requested = _utc(requested_at or decided, "requested_at")
    if decided < requested:
        raise ReceiptError("decided_at cannot precede requested_at")
    reasons = tuple(sorted({_reason(value) for value in reason_codes}))
    if not reasons:
        raise ReceiptError("at least one reason code is required")
    contracts = _references(contract_refs, "contract_refs")
    if not contracts:
        raise ReceiptError("at least one contract reference is required")

    receipt_type = "resource_admission" if kind is TransitionKind.RESOURCE_ADMISSION else "component_transition"
    canonical: dict[str, object] = {
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "artifact_class": "decision_receipt",
        "receipt_type": receipt_type,
        "timestamp": _timestamp(decided),
        "issuer": {
            "authority_id": COMPONENT_ID,
            "authority_type": "resource_governor",
            "component_id": COMPONENT_ID,
            "service_instance_id": _identifier(producer_instance_id, "producer_instance_id"),
            "software_version": COMPONENT_VERSION,
            "contract_ref": COMPONENT_CONTRACT_REF,
        },
        "request": {
            "request_id": _identifier(request_id, "request_id"),
            "subject": _identifier(subject_ref, "subject_ref"),
            "action": _action(action),
            "resource": _identifier(resource_ref, "resource_ref"),
            "requested_at": _timestamp(requested),
        },
        "context": {
            "scope": _scope(scope_kind, scope_id),
            "contract_refs": list(contracts),
            "component_id": COMPONENT_ID,
        },
        "decision": DecisionOutcome(outcome).value,
        "decision_finality": "final",
        "reason_codes": list(reasons),
        "correlation_id": _identifier(correlation_id, "correlation_id"),
        "traceability": {
            "decision_refs": list(_trace_ids(decision_refs, "DEC", "decision_refs")),
            "requirement_refs": list(_trace_ids(requirement_refs, "REQ", "requirement_refs")),
            "lock_refs": list(_trace_ids(lock_refs, "LOCK", "lock_refs")),
            "test_refs": list(_trace_ids(test_refs, "TEST", "test_refs")),
            "evidence_refs": list(_trace_ids(evidence_refs, "EVID", "evidence_refs")),
        },
        "disclosure": {
            "visibility": "authorized_internal",
            "contains_secret_values": False,
            "contains_personal_data": False,
            "contains_restricted_provenance": False,
        },
    }

    if receipt_type == "resource_admission":
        if admission_state is None or resource_scope is None:
            raise ReceiptError("resource admission receipts require admission_state and resource_scope")
        resource_decision: dict[str, object] = {
            "resource_scope": _identifier(resource_scope, "resource_scope"),
            "admission_state": AdmissionState(admission_state).value,
        }
        if envelope_ref is not None:
            resource_decision["budget_ref"] = _reference(envelope_ref, "envelope_ref")
        if queue_ref is not None:
            resource_decision["queue_ref"] = _reference(queue_ref, "queue_ref")
        if priority_class is not None:
            resource_decision["priority_class"] = _snake(priority_class, "priority_class")
        limits = _safe_limits(effective_limits)
        if limits:
            resource_decision["limits"] = dict(limits)
        canonical["resource_decision"] = resource_decision
    else:
        if None in {from_state, to_state, transition_status}:
            raise ReceiptError("component transition receipts require from_state, to_state, and status")
        allowed_statuses = {
            "accepted",
            "completed",
            "failed",
            "blocked",
            "degraded",
            "cancelled",
            "rolled_back",
            "forward_repair_required",
        }
        if transition_status not in allowed_statuses:
            raise ReceiptError("transition_status is not registered")
        canonical["transition"] = {
            "transition_id": _identifier(transition_id or request_id, "transition_id"),
            "from_state": str(from_state),
            "to_state": str(to_state),
            "transition_status": transition_status,
            "owner_ref": COMPONENT_CONTRACT_REF,
            "started_at": _timestamp(requested),
            "completed_at": _timestamp(decided),
        }

    digest = hashlib.sha256(
        json.dumps(canonical, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    ).hexdigest()
    payload = {"receipt_id": f"receipt:rg:{digest}", **canonical}
    return ResourceDecisionReceipt(payload=payload)
