"""Deterministic, selectively disclosed receipts for kOA Mediatheque transitions."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
import hashlib
import json
import re
from types import MappingProxyType
from typing import Iterable, Mapping


COMPONENT_ID = "koa_mediatheque"
COMPONENT_VERSION = "1.0.0"
COMPONENT_CONTRACT_REF = "docs/contracts/components/koa-mediatheque.component.json"
RECEIPT_SCHEMA_VERSION = "2.0.0"


class ReceiptError(ValueError):
    """Raised when receipt data is unsafe, incomplete, or non-conformant."""


class ReceiptPathUnavailable(ReceiptError):
    """Raised when a critical transition lacks a durable evidence path."""


class TransitionKind(StrEnum):
    MEDIA_RECORD_CREATED = "media_record_created"
    MEDIA_VERSION_STAGED = "media_version_staged"
    MEDIA_VERSION_ACCEPTED = "media_version_accepted"
    MEDIA_VERSION_QUARANTINED = "media_version_quarantined"
    CLASSIFICATION_CHANGED = "classification_changed"
    RIGHTS_CHANGED = "rights_changed"
    RENDITION_COMPLETED = "rendition_completed"
    LIFECYCLE_CHANGED = "lifecycle_changed"
    PUBLICATION_CANDIDATE_CREATED = "publication_candidate_created"
    PUBLICATION_RESULT_ATTACHED = "publication_result_attached"
    INTEGRITY_FAILURE_DETECTED = "integrity_failure_detected"
    BACKUP_CHECKPOINT_CREATED = "backup_checkpoint_created"
    RESTORE_VERIFIED = "restore_verified"


class DecisionOutcome(StrEnum):
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    DEGRADED = "degraded"
    QUARANTINED = "quarantined"
    CANCELLED = "cancelled"


_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/@+\-]{0,255}$")
_ACTION = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/\-]{0,255}$")
_REASON = re.compile(r"^[A-Z][A-Z0-9_:\-]{1,127}$")
_REF = re.compile(r"^(?!(?:/|.*(?:^|/)\.\.(?:/|$)))(?:[^#\s]+(?:#(?:/.*)?)?|(?:DOC|DEC|REQ|LOCK|ADR|TEST|EVID|EXC)-[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9]{3})$")
_SECRET = re.compile(
    r"(?:^|_)(?:password|passphrase|private_key|secret|token|credential|payload|content|restricted_metadata|key_material)(?:$|_)",
    re.IGNORECASE,
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


def _reference(value: str, field_name: str) -> str:
    normalized = value.strip()
    if len(normalized) < 3 or len(normalized) > 1024 or not _REF.fullmatch(normalized):
        raise ReceiptError(f"{field_name} is not a canonical reference")
    return normalized


def _trace(values: Iterable[str], prefix: str, field_name: str) -> list[str]:
    pattern = re.compile(rf"^{prefix}-[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9]{{3}}$")
    result = sorted(set(values))
    if any(not pattern.fullmatch(value) for value in result):
        raise ReceiptError(f"{field_name} contains a non-canonical identifier")
    return result


def _safe_evidence(values: Mapping[str, str] | None) -> dict[str, str]:
    result: dict[str, str] = {}
    for key, value in (values or {}).items():
        if _SECRET.search(key) or not re.fullmatch(r"[a-z][a-z0-9_]{0,63}", key):
            raise ReceiptError(f"prohibited evidence key: {key}")
        result[key] = _reference(value, key)
    return dict(sorted(result.items()))


@dataclass(frozen=True, slots=True)
class MediathequeReceipt:
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


def create_transition_receipt(
    *,
    transition_kind: TransitionKind,
    producer_instance_id: str,
    request_id: str,
    correlation_id: str,
    subject_ref: str,
    resource_ref: str,
    action: str,
    from_state: str,
    to_state: str,
    transition_status: str,
    outcome: DecisionOutcome,
    reason_codes: Iterable[str],
    decided_at: datetime,
    receipt_path_ready: bool,
    requested_at: datetime | None = None,
    input_refs: Iterable[str] = (),
    evidence_refs_by_kind: Mapping[str, str] | None = None,
    decision_refs: Iterable[str] = ("DEC-MEDIATHEQUE-001",),
    requirement_refs: Iterable[str] = ("REQ-MEDIATHEQUE-001",),
    lock_refs: Iterable[str] = ("LOCK-MEDIATHEQUE-001",),
    test_refs: Iterable[str] = (),
    evidence_refs: Iterable[str] = (),
    restricted_provenance: bool = False,
) -> MediathequeReceipt:
    kind = TransitionKind(transition_kind)
    if not receipt_path_ready:
        raise ReceiptPathUnavailable("kOA Mediatheque transitions require a durable receipt path")
    decided = _utc(decided_at, "decided_at")
    requested = _utc(requested_at or decided, "requested_at")
    if decided < requested:
        raise ReceiptError("decided_at cannot precede requested_at")
    reasons = sorted({_reason(value) for value in reason_codes})
    if not reasons:
        raise ReceiptError("at least one reason code is required")
    if transition_status not in {
        "accepted", "completed", "failed", "blocked", "degraded", "cancelled", "rolled_back", "forward_repair_required"
    }:
        raise ReceiptError("transition_status is not registered")
    safe_refs = _safe_evidence(evidence_refs_by_kind)
    contract_refs = [
        COMPONENT_CONTRACT_REF,
        "docs/contracts/artifact-contracts/koa-media-record.schema.json",
        "docs/contracts/artifact-contracts/shared-mediatheque-frame.schema.json",
    ]
    receipt_type = "component_transition"
    canonical: dict[str, object] = {
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "artifact_class": "decision_receipt",
        "receipt_type": receipt_type,
        "timestamp": _timestamp(decided),
        "issuer": {
            "authority_id": COMPONENT_ID,
            "authority_type": "component",
            "component_id": COMPONENT_ID,
            "service_instance_id": _identifier(producer_instance_id, "producer_instance_id"),
            "software_version": COMPONENT_VERSION,
            "contract_ref": COMPONENT_CONTRACT_REF,
        },
        "request": {
            "request_id": _identifier(request_id, "request_id"),
            "subject": _identifier(subject_ref, "subject_ref"),
            "action": _action_value(action),
            "resource": _identifier(resource_ref, "resource_ref"),
            "resource_type": "media_record",
            "component_id": COMPONENT_ID,
            "requested_at": _timestamp(requested),
            "input_refs": sorted(
                {_reference(value, "input_ref") for value in input_refs}
                | set(safe_refs.values())
            ),
        },
        "context": {
            "scope": {"kind": "component", "id": COMPONENT_ID},
            "contract_refs": contract_refs,
            "component_id": COMPONENT_ID,
        },
        "transition": {
            "transition_id": _identifier(request_id, "transition_id"),
            "from_state": str(from_state),
            "to_state": str(to_state),
            "transition_status": transition_status,
            "owner_ref": COMPONENT_CONTRACT_REF,
            "started_at": _timestamp(requested),
            "completed_at": _timestamp(decided),
        },
        "decision": DecisionOutcome(outcome).value,
        "decision_finality": "final",
        "reason_codes": reasons,
        "correlation_id": _identifier(correlation_id, "correlation_id"),
        "traceability": {
            "decision_refs": _trace(decision_refs, "DEC", "decision_refs"),
            "requirement_refs": _trace(requirement_refs, "REQ", "requirement_refs"),
            "lock_refs": _trace(lock_refs, "LOCK", "lock_refs"),
            "test_refs": _trace(test_refs, "TEST", "test_refs"),
            "evidence_refs": _trace(evidence_refs, "EVID", "evidence_refs"),
        },
        "disclosure": {
            "visibility": "restricted" if restricted_provenance else "authorized_internal",
            "contains_secret_values": False,
            "contains_personal_data": False,
            "contains_restricted_provenance": restricted_provenance,
        },
    }
    digest = hashlib.sha256(
        json.dumps(canonical, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    ).hexdigest()
    return MediathequeReceipt(payload={"receipt_id": f"receipt:mediatheque:{digest}", **canonical})


def _reason(value: str) -> str:
    normalized = value.strip()
    if not _REASON.fullmatch(normalized):
        raise ReceiptError("reason codes must be stable uppercase identifiers")
    return normalized


def _action_value(value: str) -> str:
    normalized = value.strip()
    if not _ACTION.fullmatch(normalized):
        raise ReceiptError("action is not a valid bounded action identifier")
    return normalized
