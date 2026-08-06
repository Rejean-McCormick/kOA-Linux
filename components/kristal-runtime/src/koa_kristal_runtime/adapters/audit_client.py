"""Selective evidence client for the Audit Broker public interface."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from koa_interfaces import Correlation, ProtocolError, UnixHttpClient


class AuditAcceptance(StrEnum):
    ACCEPTED = "accepted"
    DUPLICATE = "duplicate"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class AuditSubmission:
    audit_record_id: str
    correlation_id: str
    acceptance: AuditAcceptance
    audit_receipt_ref: str
    accepted_at: datetime
    details: Mapping[str, Any]


class AuditClient:
    """Submit bounded evidence without writing Audit Broker storage directly."""

    _ALLOWED = frozenset({
        "artifact_imported", "artifact_verification", "runtime_pack_activation",
        "runtime_pack_activation_failed", "runtime_pack_rollback", "runtime_pack_revoked",
        "runtime_query_failure", "artifact_integrity_failure",
    })

    def __init__(self, transport: UnixHttpClient, *, submit_path: str = "/v1/audit/records", max_payload_bytes: int = 256 * 1024) -> None:
        if not isinstance(transport, UnixHttpClient) and not hasattr(transport, "request"):
            raise TypeError("transport must implement the common request interface")
        if max_payload_bytes <= 0:
            raise ValueError("max_payload_bytes must be positive")
        self._transport = transport
        self._submit_path = submit_path
        self._max_payload_bytes = max_payload_bytes

    @classmethod
    def from_socket(cls, socket_path: str, *, timeout_seconds: float = 5.0) -> "AuditClient":
        return cls(UnixHttpClient(socket_path, sender="kristal_runtime", timeout_seconds=timeout_seconds, interface_version="1.0.0"))

    @staticmethod
    def _text(value: Any, field: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} must be a non-empty string")
        return value.strip()

    @staticmethod
    def _timestamp(value: datetime) -> str:
        if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("occurred_at must be timezone-aware")
        return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

    def submit_evidence(
        self, *, audit_record_id: str, correlation: Correlation, evidence_type: str,
        producer_identity: Mapping[str, Any], subject_references: Sequence[str], outcome: str,
        purpose: str, classification: str, retention_class: str, policy_or_contract_ref: str,
        source_receipt_or_evidence_refs: Sequence[str], bounded_payload: Mapping[str, Any], occurred_at: datetime,
    ) -> AuditSubmission:
        kind = self._text(evidence_type, "evidence_type")
        if kind not in self._ALLOWED:
            raise ValueError(f"unsupported evidence_type: {kind}")
        subjects = [self._text(item, "subject_reference") for item in subject_references]
        if not subjects:
            raise ValueError("subject_references must not be empty")
        body = {
            "audit_record_id": self._text(audit_record_id, "audit_record_id"),
            "event_class_id": f"kristal_runtime.{kind}", "producer_component_id": "kristal_runtime",
            "producer_identity": dict(producer_identity), "occurred_at": self._timestamp(occurred_at),
            "received_at": self._timestamp(occurred_at), "subject_references": subjects,
            "action_or_transition": kind, "outcome": self._text(outcome, "outcome"),
            "purpose": self._text(purpose, "purpose"), "classification": self._text(classification, "classification"),
            "retention_class": self._text(retention_class, "retention_class"),
            "correlation_id": correlation.correlation_id,
            "source_receipt_or_evidence_refs": [self._text(item, "source_ref") for item in source_receipt_or_evidence_refs],
            "policy_or_contract_ref": self._text(policy_or_contract_ref, "policy_or_contract_ref"),
            "bounded_payload": dict(bounded_payload),
        }
        try:
            size = len(json.dumps(body, ensure_ascii=False, allow_nan=False, separators=(",", ":"), sort_keys=True).encode("utf-8"))
        except (TypeError, ValueError) as exc:
            raise ValueError("audit evidence must contain JSON-compatible values") from exc
        if size > self._max_payload_bytes:
            raise ValueError("audit evidence exceeds the configured size limit")
        response = self._transport.request("POST", self._submit_path, body=body, correlation=correlation, idempotency_key=body["audit_record_id"], expected_status=(200, 201, 202))
        if not isinstance(response, Mapping):
            raise ProtocolError("audit submission response must be an object")
        if response.get("audit_record_id") != body["audit_record_id"] or response.get("correlation_id") != correlation.correlation_id:
            raise ProtocolError("audit submission identity or correlation mismatch")
        try:
            acceptance = AuditAcceptance(response.get("acceptance"))
        except ValueError as exc:
            raise ProtocolError("audit submission acceptance is unknown") from exc
        receipt_ref = response.get("audit_receipt_ref")
        accepted_at = response.get("accepted_at")
        if not isinstance(receipt_ref, str) or not receipt_ref.strip() or not isinstance(accepted_at, str):
            raise ProtocolError("audit submission receipt fields are invalid")
        try:
            when = datetime.fromisoformat(accepted_at.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ProtocolError("audit submission accepted_at is invalid") from exc
        if when.tzinfo is None or when.utcoffset() is None:
            raise ProtocolError("audit submission accepted_at must include timezone")
        details = response.get("details", {})
        if not isinstance(details, Mapping):
            raise ProtocolError("audit submission details must be an object")
        return AuditSubmission(body["audit_record_id"], correlation.correlation_id, acceptance, receipt_ref.strip(), when.astimezone(timezone.utc), MappingProxyType(dict(details)))
