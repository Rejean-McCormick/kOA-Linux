"""Audit sink adapter using an injected public transport."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, runtime_checkable

_SECRET_FIELD_FRAGMENTS = (
    "password",
    "private_key",
    "secret",
    "token",
    "presented_factor",
    "key_material",
    "credential_material",
)


class AuditDeliveryError(RuntimeError):
    """Raised when required evidence cannot reach the declared audit boundary."""


@runtime_checkable
class AuditTransport(Protocol):
    """Public transport contract; implementations may use HTTP, IPC or a queue."""

    def publish(self, envelope: Mapping[str, object]) -> Mapping[str, object]: ...


class AuditClient:
    """Publish bounded evidence without importing Audit Broker internals."""

    def __init__(self, transport: AuditTransport, *, source: str = "identity_and_trust") -> None:
        if not source:
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
        required: bool = True,
    ) -> str | None:
        if not event_type or not correlation_id or not occurred_at:
            raise ValueError("event_type, correlation_id and occurred_at are required")
        _assert_no_secret_fields(payload)
        envelope: dict[str, object] = {
            "source": self._source,
            "event_type": event_type,
            "correlation_id": correlation_id,
            "occurred_at": occurred_at,
            "payload": dict(payload),
        }
        try:
            response = self._transport.publish(envelope)
        except Exception as exc:
            if required:
                raise AuditDeliveryError("receipt_path_unavailable") from exc
            return None

        accepted = response.get("accepted") is True
        receipt_ref = response.get("receipt_ref")
        if not accepted or not isinstance(receipt_ref, str) or not receipt_ref:
            if required:
                raise AuditDeliveryError("audit transport returned no terminal receipt")
            return None
        return receipt_ref

    def record(self, record: Mapping[str, object], *, required: bool = True) -> str | None:
        """Port-friendly entrypoint for a complete bounded audit record."""

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
            required=required,
        )


def _assert_no_secret_fields(value: object, *, path: str = "payload") -> None:
    """Reject obvious secret-bearing fields before evidence leaves the component."""

    if isinstance(value, Mapping):
        for key, nested in value.items():
            name = str(key).casefold()
            if any(fragment in name for fragment in _SECRET_FIELD_FRAGMENTS):
                raise ValueError(f"secret-bearing audit field is prohibited: {path}.{key}")
            _assert_no_secret_fields(nested, path=f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, nested in enumerate(value):
            _assert_no_secret_fields(nested, path=f"{path}[{index}]")
