"""Audit Broker-owned receipt construction with selective disclosure."""

from __future__ import annotations

import json
import re
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from types import MappingProxyType
from typing import Iterable, Mapping

_TOKEN = re.compile(r"^[a-z][a-z0-9_]{2,127}$")
_REFERENCE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/#@+-]{0,511}$")
_RECEIPT_NAMESPACE = uuid.UUID("b7212675-4991-56a8-a950-a4ae48805d2d")


class ReceiptKind(StrEnum):
    INGESTION = "audit_ingestion"
    ACCESS = "audit_access"
    DISCLOSURE = "audit_disclosure"
    RETENTION = "audit_retention"
    INVALIDATION = "audit_invalidation"
    RECOVERY = "audit_recovery"


class ReceiptOutcome(StrEnum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    QUARANTINED = "quarantined"
    ALLOWED = "allowed"
    PARTIALLY_ALLOWED = "partially_allowed"
    DENIED = "denied"
    APPLIED = "applied"
    PARTIALLY_APPLIED = "partially_applied"
    INVALIDATED = "invalidated"
    NOT_FOUND = "not_found"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    FAILED = "failed"
    RECOVERED = "recovered"


@dataclass(frozen=True, slots=True)
class AuditReceipt:
    schema_version: str
    receipt_id: str
    receipt_kind: ReceiptKind
    transition_type: str
    producer_component_id: str
    producer_contract_ref: str
    request_id: str
    correlation_id: str
    outcome: ReceiptOutcome
    reason_code: str
    occurred_at: datetime
    completed_at: datetime
    actor_ref: str | None
    subject_refs: tuple[str, ...]
    target_refs: tuple[str, ...]
    effective_scope: tuple[str, ...]
    authority_refs: tuple[str, ...]
    decision_ref: str | None
    evidence_refs: tuple[str, ...]
    disclosure_class: str

    def as_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "receipt_id": self.receipt_id,
            "receipt_kind": self.receipt_kind.value,
            "transition_type": self.transition_type,
            "producer": {
                "component_id": self.producer_component_id,
                "contract_ref": self.producer_contract_ref,
            },
            "request_id": self.request_id,
            "correlation_id": self.correlation_id,
            "outcome": self.outcome.value,
            "reason_code": self.reason_code,
            "occurred_at": _format_time(self.occurred_at),
            "completed_at": _format_time(self.completed_at),
            "actor_ref": self.actor_ref,
            "subject_refs": list(self.subject_refs),
            "target_refs": list(self.target_refs),
            "effective_scope": list(self.effective_scope),
            "authority_refs": list(self.authority_refs),
            "decision_ref": self.decision_ref,
            "evidence_refs": list(self.evidence_refs),
            "disclosure_class": self.disclosure_class,
            "authoritative_state_owner_transferred": False,
        }

    def canonical_json(self) -> str:
        return json.dumps(self.as_dict(), ensure_ascii=False, separators=(",", ":"), sort_keys=True)


class AuditReceiptFactory:
    """Create receipts only for Audit Broker-owned transitions."""

    COMPONENT_ID = "audit_broker"
    CONTRACT_REF = "contracts/components/audit-broker.component.json"
    SCHEMA_VERSION = "1.0.0"
    _ALLOWED_TRANSITIONS = MappingProxyType(
        {
            ReceiptKind.INGESTION: frozenset(
                {"submit_audit_event", "validate_submission_envelope"}
            ),
            ReceiptKind.ACCESS: frozenset(
                {"request_audit_disclosure", "get_audit_record_metadata"}
            ),
            ReceiptKind.DISCLOSURE: frozenset({"request_audit_disclosure"}),
            ReceiptKind.RETENTION: frozenset({"apply_retention_action"}),
            ReceiptKind.INVALIDATION: frozenset({"invalidate_audit_record"}),
            ReceiptKind.RECOVERY: frozenset({"recover_audit_broker_state"}),
        }
    )
    _POLICY_GATED = frozenset({ReceiptKind.ACCESS, ReceiptKind.DISCLOSURE, ReceiptKind.RETENTION})

    def create(
        self,
        *,
        receipt_kind: ReceiptKind,
        transition_type: str,
        request_id: str,
        correlation_id: str,
        outcome: ReceiptOutcome,
        reason_code: str,
        occurred_at: datetime,
        completed_at: datetime,
        actor_ref: str | None = None,
        subject_refs: Iterable[str] = (),
        target_refs: Iterable[str] = (),
        effective_scope: Iterable[str] = (),
        authority_refs: Iterable[str] = (),
        decision_ref: str | None = None,
        evidence_refs: Iterable[str] = (),
        disclosure_class: str = "restricted_summary",
    ) -> AuditReceipt:
        self._validate_token("transition_type", transition_type)
        self._validate_token("reason_code", reason_code)
        self._validate_token("disclosure_class", disclosure_class)
        if transition_type not in self._ALLOWED_TRANSITIONS[receipt_kind]:
            raise ValueError(
                f"transition {transition_type!r} is not owned by receipt kind {receipt_kind.value!r}"
            )
        if receipt_kind in self._POLICY_GATED and not decision_ref:
            raise ValueError("policy-gated Audit Broker receipt requires decision_ref")

        occurred = _utc_time("occurred_at", occurred_at)
        completed = _utc_time("completed_at", completed_at)
        if completed < occurred:
            raise ValueError("completed_at must not precede occurred_at")

        refs = {
            "request_id": _reference("request_id", request_id),
            "correlation_id": _reference("correlation_id", correlation_id),
            "actor_ref": _optional_reference("actor_ref", actor_ref),
            "decision_ref": _optional_reference("decision_ref", decision_ref),
        }
        subjects = _reference_tuple("subject_refs", subject_refs)
        targets = _reference_tuple("target_refs", target_refs)
        scope = _reference_tuple("effective_scope", effective_scope)
        if outcome in {ReceiptOutcome.ALLOWED, ReceiptOutcome.PARTIALLY_ALLOWED} and not scope:
            raise ValueError("allowed or partially allowed receipt requires effective_scope")
        authorities = _reference_tuple("authority_refs", authority_refs)
        evidence = _reference_tuple("evidence_refs", evidence_refs)

        identity_material = {
            "receipt_kind": receipt_kind.value,
            "transition_type": transition_type,
            "request_id": refs["request_id"],
            "correlation_id": refs["correlation_id"],
            "outcome": outcome.value,
            "reason_code": reason_code,
            "occurred_at": _format_time(occurred),
            "completed_at": _format_time(completed),
            "actor_ref": refs["actor_ref"],
            "subject_refs": subjects,
            "target_refs": targets,
            "effective_scope": scope,
            "authority_refs": authorities,
            "decision_ref": refs["decision_ref"],
            "evidence_refs": evidence,
            "disclosure_class": disclosure_class,
        }
        canonical = json.dumps(identity_material, separators=(",", ":"), sort_keys=True)
        receipt_id = f"audit-receipt:{uuid.uuid5(_RECEIPT_NAMESPACE, canonical)}"

        return AuditReceipt(
            schema_version=self.SCHEMA_VERSION,
            receipt_id=receipt_id,
            receipt_kind=receipt_kind,
            transition_type=transition_type,
            producer_component_id=self.COMPONENT_ID,
            producer_contract_ref=self.CONTRACT_REF,
            request_id=str(refs["request_id"]),
            correlation_id=str(refs["correlation_id"]),
            outcome=outcome,
            reason_code=reason_code,
            occurred_at=occurred,
            completed_at=completed,
            actor_ref=refs["actor_ref"],
            subject_refs=subjects,
            target_refs=targets,
            effective_scope=scope,
            authority_refs=authorities,
            decision_ref=refs["decision_ref"],
            evidence_refs=evidence,
            disclosure_class=disclosure_class,
        )

    @staticmethod
    def _validate_token(name: str, value: str) -> None:
        if not _TOKEN.fullmatch(value):
            raise ValueError(f"{name} must match {_TOKEN.pattern}")


def _reference(name: str, value: str) -> str:
    if not _REFERENCE.fullmatch(value):
        raise ValueError(f"{name} is not a valid bounded reference")
    return value


def _optional_reference(name: str, value: str | None) -> str | None:
    return None if value is None else _reference(name, value)


def _reference_tuple(name: str, values: Iterable[str]) -> tuple[str, ...]:
    normalized = tuple(sorted(set(values)))
    for value in normalized:
        _reference(name, value)
    return normalized


def _utc_time(name: str, value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")
    return value.astimezone(UTC)


def _format_time(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
