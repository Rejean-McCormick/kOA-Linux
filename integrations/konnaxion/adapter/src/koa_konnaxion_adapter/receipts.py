"""Deterministic non-authoritative receipts for boundary activity."""

from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
import hashlib
import json
import re
import uuid
from typing import Any


class BoundaryOutcome(StrEnum):
    FORWARDED = "forwarded"
    REJECTED = "rejected"
    BLOCKED = "blocked"
    FAILED = "failed"
    DUPLICATE = "duplicate"


_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/@+-]{2,254}$")
_NAMESPACE = uuid.UUID("6c661ecb-496f-58f0-80fa-4594ac23c914")
_SECRET_KEYS = {"access_token", "api_key", "authorization", "cookie", "password", "private_key", "secret", "token"}


@dataclass(frozen=True, slots=True)
class BoundaryReceipt:
    receipt_id: str
    issued_at: datetime
    correlation_id: str
    idempotency_key: str
    operation: str
    request_digest: str
    outcome: BoundaryOutcome
    reason_code: str
    remote_reference: str | None = None
    details: Mapping[str, Any] | None = None

    @property
    def is_credential(self) -> bool:
        return False

    @property
    def transfers_authority(self) -> bool:
        return False

    def as_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "receipt_id": self.receipt_id,
            "receipt_type": "integration_boundary",
            "integration_id": "konnaxion",
            "issued_at": _format_time(self.issued_at),
            "correlation_id": self.correlation_id,
            "idempotency_key": self.idempotency_key,
            "operation": self.operation,
            "request_digest": self.request_digest,
            "outcome": self.outcome.value,
            "reason_code": self.reason_code,
            "authority_effect": "none",
            "authoritative_acceptance": False,
            "credential": False,
        }
        if self.remote_reference is not None:
            result["remote_reference"] = self.remote_reference
        if self.details:
            result["details"] = deepcopy(dict(self.details))
        return result

    def canonical_json(self) -> str:
        return json.dumps(self.as_dict(), ensure_ascii=False, separators=(",", ":"), sort_keys=True)

    def sha256(self) -> str:
        return "sha256:" + hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()


class ReceiptFactory:
    def issue(
        self,
        *,
        issued_at: datetime,
        correlation_id: str,
        idempotency_key: str,
        operation: str,
        request_digest: str,
        outcome: BoundaryOutcome,
        reason_code: str,
        remote_reference: str | None = None,
        details: Mapping[str, Any] | None = None,
    ) -> BoundaryReceipt:
        when = _utc(issued_at)
        for name, value in {
            "correlation_id": correlation_id,
            "idempotency_key": idempotency_key,
            "operation": operation,
            "reason_code": reason_code,
        }.items():
            _stable(name, value)
        if not re.fullmatch(r"sha256:[0-9a-f]{64}", request_digest):
            raise ValueError("request_digest must be a lowercase sha256 digest")
        if remote_reference is not None:
            _stable("remote_reference", remote_reference)
        safe_details = {} if details is None else _safe_mapping(details)
        identity = {
            "correlation_id": correlation_id,
            "idempotency_key": idempotency_key,
            "issued_at": _format_time(when),
            "operation": operation,
            "outcome": outcome.value,
            "reason_code": reason_code,
            "remote_reference": remote_reference,
            "request_digest": request_digest,
            "details": safe_details,
        }
        receipt_id = "konnaxion-receipt:" + str(
            uuid.uuid5(_NAMESPACE, json.dumps(identity, separators=(",", ":"), sort_keys=True))
        )
        return BoundaryReceipt(
            receipt_id=receipt_id,
            issued_at=when,
            correlation_id=correlation_id,
            idempotency_key=idempotency_key,
            operation=operation,
            request_digest=request_digest,
            outcome=outcome,
            reason_code=reason_code,
            remote_reference=remote_reference,
            details=safe_details,
        )


def _safe_mapping(value: Mapping[str, Any]) -> dict[str, Any]:
    copied = deepcopy(dict(value))
    _reject_secrets(copied)
    encoded = json.dumps(copied, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    if len(encoded.encode("utf-8")) > 4096:
        raise ValueError("receipt details exceed the 4096-byte boundary")
    return copied


def _reject_secrets(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            if str(key).lower() in _SECRET_KEYS:
                raise ValueError(f"secret-like receipt field prohibited: {key}")
            _reject_secrets(child)
    elif isinstance(value, list):
        for child in value:
            _reject_secrets(child)


def _stable(name: str, value: str) -> str:
    if not isinstance(value, str) or not _ID.fullmatch(value):
        raise ValueError(f"{name} must be a stable reference")
    return value


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        raise ValueError("issued_at must be timezone-aware")
    return value.astimezone(UTC)


def _format_time(value: datetime) -> str:
    return _utc(value).isoformat(timespec="microseconds").replace("+00:00", "Z")
