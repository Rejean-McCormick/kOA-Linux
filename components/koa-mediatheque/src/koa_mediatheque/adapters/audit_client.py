"""Public Audit Broker adapter with bounded selective disclosure."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
import hashlib
import json
from typing import Any, Protocol, runtime_checkable


class AuditClientError(RuntimeError):
    """Raised when an audit submission cannot produce an acceptable result."""


@runtime_checkable
class AuditTransport(Protocol):
    """Minimal public transport expected from an Audit Broker binding."""

    def submit_audit_event(
        self, request: Mapping[str, Any], *, idempotency_key: str
    ) -> Mapping[str, Any]:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class AuditSubmission:
    status: str
    receipt_ref: str | None
    response: Mapping[str, Any]


_SENSITIVE_KEYS = {
    "authorization",
    "credential",
    "credentials",
    "password",
    "private_key",
    "secret",
    "token",
    "raw_content",
    "content_bytes",
    "media_bytes",
}
_ALLOWED_RESULTS = frozenset({"accepted", "rejected", "quarantined"})


def _canonical_json(value: Mapping[str, Any]) -> str:
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    except (TypeError, ValueError) as exc:
        raise AuditClientError("audit event is not JSON serializable") from exc


def _reject_sensitive(value: Any, path: str = "event_payload") -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            normalized = str(key).lower().replace("-", "_")
            if normalized in _SENSITIVE_KEYS:
                raise AuditClientError(f"sensitive field is prohibited at {path}.{key}")
            _reject_sensitive(item, f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _reject_sensitive(item, f"{path}[{index}]")
    elif isinstance(value, (bytes, bytearray, memoryview)):
        raise AuditClientError(f"binary content is prohibited at {path}")


class AuditClient:
    """Submit minimized events through the Audit Broker's public interface."""

    def __init__(
        self,
        transport: AuditTransport | Callable[..., Mapping[str, Any]],
        *,
        producer_identity: str = "component:koa_mediatheque",
    ) -> None:
        if not producer_identity.strip():
            raise ValueError("producer_identity must not be empty")
        self._transport = transport
        self._producer_identity = producer_identity

    def record(
        self,
        *,
        event_class_id: str,
        action: str,
        subject_ref: str,
        outcome: str,
        correlation_id: str,
        idempotency_key: str,
        evidence_refs: Sequence[str] = (),
        reason_codes: Sequence[str] = (),
        classification: str = "restricted_metadata",
        purpose: str = "selective_accountability",
        retention_class: str = "component_audit",
        require_receipt: bool = True,
    ) -> AuditSubmission:
        values = {
            "event_class_id": event_class_id,
            "action": action,
            "subject_ref": subject_ref,
            "outcome": outcome,
            "correlation_id": correlation_id,
            "idempotency_key": idempotency_key,
        }
        for name, value in values.items():
            if not isinstance(value, str) or not value.strip():
                raise AuditClientError(f"{name} must be a non-empty string")

        event_payload: dict[str, Any] = {
            "action": action,
            "subject_ref": subject_ref,
            "outcome": outcome,
            "reason_codes": list(dict.fromkeys(reason_codes)),
            "evidence_refs": list(dict.fromkeys(evidence_refs)),
        }
        _reject_sensitive(event_payload)
        request = {
            "interface_id": "submit_audit_event",
            "interface_version": "1.0.0",
            "event_class_id": event_class_id,
            "producer_identity": self._producer_identity,
            "event_payload": event_payload,
            "classification": classification,
            "purpose": purpose,
            "retention_class": retention_class,
            "correlation_id": correlation_id,
            "source_receipt_or_evidence_refs": list(dict.fromkeys(evidence_refs)),
        }
        response = self._submit(request, idempotency_key=idempotency_key)
        status = str(response.get("status") or response.get("result") or "")
        if status not in _ALLOWED_RESULTS:
            raise AuditClientError(f"unsupported Audit Broker result: {status!r}")
        receipt_ref_value = response.get("receipt_ref") or response.get("receipt_id")
        receipt_ref = str(receipt_ref_value) if receipt_ref_value else None
        if require_receipt and not receipt_ref:
            raise AuditClientError("required terminal audit receipt is missing")
        return AuditSubmission(status=status, receipt_ref=receipt_ref, response=response)

    def derive_idempotency_key(self, event: Mapping[str, Any]) -> str:
        digest = hashlib.sha256(_canonical_json(event).encode("utf-8")).hexdigest()
        return f"koa-mediatheque-audit:{digest}"

    def _submit(
        self, request: Mapping[str, Any], *, idempotency_key: str
    ) -> Mapping[str, Any]:
        transport = self._transport
        try:
            method = getattr(transport, "submit_audit_event", None)
            if callable(method):
                result = method(request, idempotency_key=idempotency_key)
            elif callable(transport):
                result = transport(request, idempotency_key=idempotency_key)
            else:
                raise AuditClientError("audit transport has no public submit interface")
        except AuditClientError:
            raise
        except Exception as exc:  # transport failures are classified, not swallowed
            raise AuditClientError("Audit Broker submission failed") from exc
        if not isinstance(result, Mapping):
            raise AuditClientError("Audit Broker returned a non-object response")
        return dict(result)
