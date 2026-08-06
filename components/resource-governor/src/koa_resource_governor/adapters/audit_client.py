"""Selective-audit adapter using an injected public Audit Broker transport."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, runtime_checkable

_SECRET_FIELD_FRAGMENTS = (
    "authorization",
    "bearer",
    "credential",
    "key_material",
    "password",
    "private_key",
    "secret",
    "session_cookie",
    "token",
)
_PROHIBITED_PAYLOAD_FIELDS = {
    "business_payload",
    "command_line",
    "environment_variables",
    "request_body",
    "workload_payload",
}


class AuditDeliveryError(RuntimeError):
    """Raised when required resource evidence cannot reach the audit boundary."""


@runtime_checkable
class AuditTransport(Protocol):
    """Public Audit Broker transport implemented by HTTP, IPC, or a queue."""

    def publish(self, envelope: Mapping[str, object]) -> Mapping[str, object]: ...


class AuditClient:
    """Publish bounded resource evidence without importing Audit Broker internals."""

    def __init__(self, transport: AuditTransport, *, source: str = "resource_governor") -> None:
        if not source.strip():
            raise ValueError("audit source identity is required")
        self._transport = transport
        self._source = source

    def emit(
        self,
        event_type: str,
        payload: Mapping[str, object],
        *,
        correlation_id: str,
        occurred_at: str,
        required_receipt: bool = True,
    ) -> str | None:
        """Emit one bounded event and return its immutable receipt reference.

        ``required_receipt`` must remain true for critical resource transitions.
        An accepted-but-unreceipted response is never represented as completion.
        """

        if not event_type.strip():
            raise ValueError("event_type is required")
        if not correlation_id.strip():
            raise ValueError("correlation_id is required")
        if not occurred_at.strip():
            raise ValueError("occurred_at is required")
        _assert_bounded_resource_facts(payload)

        envelope: dict[str, object] = {
            "interface_id": "RG-IF-010",
            "source": self._source,
            "event_type": event_type,
            "correlation_id": correlation_id,
            "occurred_at": occurred_at,
            "payload": dict(payload),
        }
        try:
            response = self._transport.publish(envelope)
        except Exception as exc:
            if required_receipt:
                raise AuditDeliveryError("receipt_sink_unavailable") from exc
            return None

        accepted = response.get("accepted") is True
        receipt_ref = response.get("receipt_ref")
        if not accepted or not isinstance(receipt_ref, str) or not receipt_ref.strip():
            if required_receipt:
                raise AuditDeliveryError("audit transport returned no terminal receipt")
            return None
        return receipt_ref

    def record(self, record: Mapping[str, object], *, required_receipt: bool = True) -> str | None:
        """Port-friendly entrypoint accepting a complete bounded audit record."""

        event_type = record.get("event_type")
        correlation_id = record.get("correlation_id")
        occurred_at = record.get("occurred_at")
        payload = record.get("payload", {})
        if not isinstance(event_type, str) or not isinstance(correlation_id, str):
            raise ValueError("audit record lacks event_type or correlation_id")
        if not isinstance(occurred_at, str) or not isinstance(payload, Mapping):
            raise ValueError("audit record lacks occurred_at or bounded payload")
        return self.emit(
            event_type,
            payload,
            correlation_id=correlation_id,
            occurred_at=occurred_at,
            required_receipt=required_receipt,
        )


def _assert_bounded_resource_facts(value: object, *, path: str = "payload") -> None:
    """Reject obvious secrets and workload-content fields before publication."""

    if isinstance(value, Mapping):
        for key, nested in value.items():
            name = str(key).casefold()
            if name in _PROHIBITED_PAYLOAD_FIELDS:
                raise ValueError(f"workload content is prohibited in audit evidence: {path}.{key}")
            if any(fragment in name for fragment in _SECRET_FIELD_FRAGMENTS):
                raise ValueError(f"secret-bearing audit field is prohibited: {path}.{key}")
            _assert_bounded_resource_facts(nested, path=f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, nested in enumerate(value):
            _assert_bounded_resource_facts(nested, path=f"{path}[{index}]")
