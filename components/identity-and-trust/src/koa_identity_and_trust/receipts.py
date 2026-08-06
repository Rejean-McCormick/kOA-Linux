"""Immutable, selectively disclosed Identity and Trust receipts."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
import hashlib
import json
import re
from types import MappingProxyType
from typing import Iterable, Mapping, TypeAlias


JSONScalar: TypeAlias = str | int | float | bool | None
COMPONENT_ID = "identity_and_trust"
RECEIPT_SCHEMA_VERSION = "1.0.0"


class ReceiptError(ValueError):
    """Raised when a receipt would be ambiguous or disclose protected material."""


class ReceiptPathUnavailable(ReceiptError):
    """Raised when a critical transition lacks an approved durable receipt path."""


class ReceiptClass(StrEnum):
    DECISION = "decision_receipt"
    VERIFICATION = "verification_receipt"
    TRANSITION = "transition_receipt"
    EVIDENCE_ACCESS = "evidence_access_receipt"
    RECOVERY = "recovery_receipt"


class ReceiptOutcome(StrEnum):
    AUTHORIZED = "authorized"
    DENIED = "denied"
    INDETERMINATE = "indeterminate"
    PREPARED = "prepared"
    COMMITTED = "committed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ROLLED_BACK = "rolled_back"
    REPAIRED = "repaired"
    SUPERSEDED = "superseded"
    CLOSED = "closed"


CRITICAL_TRANSITIONS = frozenset(
    {
        "identity_activation",
        "identity_revocation",
        "credential_issuance",
        "credential_revocation",
        "trust_root_activation",
        "trust_root_revocation",
        "trust_root_supersession",
        "key_rotation",
        "offline_trust_update",
        "protected_key_restore",
        "trust_store_restore",
    }
)
_SECRET_KEY_PATTERN = re.compile(
    r"(?:^|_)(?:password|passphrase|private_key|secret|token|factor_value|credential_material|key_material)(?:$|_)",
    re.IGNORECASE,
)
_IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:/@+-]{0,255}$")


def _utc(value: datetime, *, field_name: str) -> datetime:
    if value.tzinfo is None:
        raise ReceiptError(f"{field_name} must be timezone-aware")
    return value.astimezone(UTC)


def _identifier(value: str, *, field_name: str) -> str:
    normalized = value.strip()
    if not _IDENTIFIER_PATTERN.fullmatch(normalized):
        raise ReceiptError(f"{field_name} is not a valid bounded identifier")
    return normalized


def _safe_context(values: Mapping[str, JSONScalar] | None) -> Mapping[str, JSONScalar]:
    if values is None:
        return MappingProxyType({})
    result: dict[str, JSONScalar] = {}
    for key, value in values.items():
        if _SECRET_KEY_PATTERN.search(key):
            raise ReceiptError(f"receipt context cannot contain protected field: {key}")
        if not _IDENTIFIER_PATTERN.fullmatch(key):
            raise ReceiptError(f"receipt context key is invalid: {key}")
        if isinstance(value, str) and len(value) > 2048:
            raise ReceiptError(f"receipt context value is too large: {key}")
        if not isinstance(value, (str, int, float, bool, type(None))):
            raise ReceiptError(f"receipt context values must be JSON scalars: {key}")
        result[key] = value
    return MappingProxyType(dict(sorted(result.items())))


def _timestamp(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True, slots=True)
class Receipt:
    receipt_id: str
    receipt_schema_version: str
    receipt_class: ReceiptClass
    transition_type: str
    producer_component_id: str
    producer_instance_id: str
    subject_ref: str
    actor_ref: str | None
    target_refs: tuple[str, ...]
    scope: Mapping[str, JSONScalar]
    request_id: str
    correlation_id: str
    causation_id: str | None
    authority_refs: tuple[str, ...]
    outcome: ReceiptOutcome
    reason_code: str
    requested_at: datetime
    decided_at: datetime
    committed_at: datetime | None
    evidence_refs: tuple[str, ...]
    public_context: Mapping[str, JSONScalar]

    def __post_init__(self) -> None:
        if self.producer_component_id != COMPONENT_ID:
            raise ReceiptError(f"producer_component_id is fixed to {COMPONENT_ID}")
        if self.receipt_schema_version != RECEIPT_SCHEMA_VERSION:
            raise ReceiptError(f"receipt_schema_version is fixed to {RECEIPT_SCHEMA_VERSION}")
        _identifier(self.receipt_id, field_name="receipt_id")
        _identifier(self.transition_type, field_name="transition_type")
        _identifier(self.producer_instance_id, field_name="producer_instance_id")
        _identifier(self.subject_ref, field_name="subject_ref")
        _identifier(self.request_id, field_name="request_id")
        _identifier(self.correlation_id, field_name="correlation_id")
        _identifier(self.reason_code, field_name="reason_code")
        if self.actor_ref is not None:
            _identifier(self.actor_ref, field_name="actor_ref")
        if self.causation_id is not None:
            _identifier(self.causation_id, field_name="causation_id")
        for field_name, values in (
            ("target_refs", self.target_refs),
            ("authority_refs", self.authority_refs),
            ("evidence_refs", self.evidence_refs),
        ):
            for value in values:
                _identifier(value, field_name=field_name)
        requested = _utc(self.requested_at, field_name="requested_at")
        decided = _utc(self.decided_at, field_name="decided_at")
        committed = _utc(self.committed_at, field_name="committed_at") if self.committed_at else None
        if decided < requested:
            raise ReceiptError("decided_at cannot precede requested_at")
        if committed is not None and committed < decided:
            raise ReceiptError("committed_at cannot precede decided_at")
        if self.outcome is ReceiptOutcome.COMMITTED and committed is None:
            raise ReceiptError("committed receipts require committed_at")

    def to_dict(self, *, view: str = "ordinary") -> dict[str, object]:
        if view not in {"ordinary", "restricted"}:
            raise ReceiptError("view must be 'ordinary' or 'restricted'")
        result: dict[str, object] = {
            "receipt_id": self.receipt_id,
            "receipt_schema_version": self.receipt_schema_version,
            "receipt_class": self.receipt_class.value,
            "transition_type": self.transition_type,
            "producer_component_id": self.producer_component_id,
            "producer_instance_id": self.producer_instance_id,
            "subject_ref": self.subject_ref,
            "target_refs": list(self.target_refs),
            "scope": dict(self.scope),
            "request_id": self.request_id,
            "correlation_id": self.correlation_id,
            "authority_refs": list(self.authority_refs),
            "outcome": self.outcome.value,
            "reason_code": self.reason_code,
            "requested_at": _timestamp(self.requested_at),
            "decided_at": _timestamp(self.decided_at),
            "committed_at": _timestamp(self.committed_at),
            "public_context": dict(self.public_context),
        }
        if view == "restricted":
            result.update(
                {
                    "actor_ref": self.actor_ref,
                    "causation_id": self.causation_id,
                    "evidence_refs": list(self.evidence_refs),
                }
            )
        return result


def create_receipt(
    *,
    receipt_class: ReceiptClass,
    transition_type: str,
    producer_instance_id: str,
    subject_ref: str,
    request_id: str,
    correlation_id: str,
    outcome: ReceiptOutcome,
    reason_code: str,
    requested_at: datetime,
    decided_at: datetime,
    committed_at: datetime | None = None,
    actor_ref: str | None = None,
    target_refs: Iterable[str] = (),
    scope: Mapping[str, JSONScalar] | None = None,
    causation_id: str | None = None,
    authority_refs: Iterable[str] = (),
    evidence_refs: Iterable[str] = (),
    public_context: Mapping[str, JSONScalar] | None = None,
    receipt_path_ready: bool,
) -> Receipt:
    """Create a deterministic receipt and fail closed for critical transitions."""
    if transition_type in CRITICAL_TRANSITIONS and not receipt_path_ready:
        raise ReceiptPathUnavailable("receipt_path_unavailable")
    if transition_type in CRITICAL_TRANSITIONS and receipt_class not in {
        ReceiptClass.TRANSITION,
        ReceiptClass.RECOVERY,
    }:
        raise ReceiptError("critical transitions require a transition or recovery receipt")

    normalized_scope = _safe_context(scope)
    normalized_context = _safe_context(public_context)
    targets = tuple(sorted({_identifier(value, field_name="target_refs") for value in target_refs}))
    authorities = tuple(sorted({_identifier(value, field_name="authority_refs") for value in authority_refs}))
    evidence = tuple(sorted({_identifier(value, field_name="evidence_refs") for value in evidence_refs}))
    canonical = {
        "receipt_schema_version": RECEIPT_SCHEMA_VERSION,
        "receipt_class": ReceiptClass(receipt_class).value,
        "transition_type": _identifier(transition_type, field_name="transition_type"),
        "producer_component_id": COMPONENT_ID,
        "producer_instance_id": _identifier(producer_instance_id, field_name="producer_instance_id"),
        "subject_ref": _identifier(subject_ref, field_name="subject_ref"),
        "actor_ref": _identifier(actor_ref, field_name="actor_ref") if actor_ref else None,
        "target_refs": targets,
        "scope": dict(normalized_scope),
        "request_id": _identifier(request_id, field_name="request_id"),
        "correlation_id": _identifier(correlation_id, field_name="correlation_id"),
        "causation_id": _identifier(causation_id, field_name="causation_id") if causation_id else None,
        "authority_refs": authorities,
        "outcome": ReceiptOutcome(outcome).value,
        "reason_code": _identifier(reason_code, field_name="reason_code"),
        "requested_at": _timestamp(_utc(requested_at, field_name="requested_at")),
        "decided_at": _timestamp(_utc(decided_at, field_name="decided_at")),
        "committed_at": _timestamp(_utc(committed_at, field_name="committed_at")) if committed_at else None,
        "evidence_refs": evidence,
        "public_context": dict(normalized_context),
    }
    digest = hashlib.sha256(
        json.dumps(canonical, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    ).hexdigest()
    return Receipt(
        receipt_id=f"idt-{digest[:32]}",
        receipt_schema_version=RECEIPT_SCHEMA_VERSION,
        receipt_class=ReceiptClass(receipt_class),
        transition_type=canonical["transition_type"],
        producer_component_id=COMPONENT_ID,
        producer_instance_id=canonical["producer_instance_id"],
        subject_ref=canonical["subject_ref"],
        actor_ref=canonical["actor_ref"],
        target_refs=targets,
        scope=normalized_scope,
        request_id=canonical["request_id"],
        correlation_id=canonical["correlation_id"],
        causation_id=canonical["causation_id"],
        authority_refs=authorities,
        outcome=ReceiptOutcome(outcome),
        reason_code=canonical["reason_code"],
        requested_at=_utc(requested_at, field_name="requested_at"),
        decided_at=_utc(decided_at, field_name="decided_at"),
        committed_at=_utc(committed_at, field_name="committed_at") if committed_at else None,
        evidence_refs=evidence,
        public_context=normalized_context,
    )
