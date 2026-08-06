"""Transport-neutral client boundary for the independently owned Ariane subsystem."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping, Protocol, runtime_checkable

JsonScalar = str | int | float | bool | None
JsonValue = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]


class ClientFailureKind(str, Enum):
    UNAVAILABLE = "unavailable"
    TIMEOUT = "timeout"
    INCOMPATIBLE = "incompatible"
    INVALID_RESPONSE = "invalid_response"
    REJECTED = "rejected"


class ArianeClientError(RuntimeError):
    """A bounded transport or contract failure from the Ariane boundary."""

    def __init__(
        self,
        kind: ClientFailureKind,
        reason_code: str,
        message: str,
        *,
        retryable: bool = False,
    ) -> None:
        self.kind = kind
        self.reason_code = _required_text(reason_code, "reason_code")
        self.retryable = bool(retryable)
        super().__init__(_required_text(message, "message"))


@runtime_checkable
class ArianeTransport(Protocol):
    """Injected transport implemented outside this bundle.

    The transport owns endpoint syntax, authentication, TLS or Unix-socket
    details, and conversion to the official Ariane API.  This adapter never
    guesses those subsystem-internal details.
    """

    def invoke(
        self,
        operation: str,
        payload: Mapping[str, JsonValue],
        *,
        timeout_seconds: float,
    ) -> Mapping[str, Any]: ...


@dataclass(frozen=True, slots=True)
class ArianeOperationMap:
    """Official operation identifiers supplied by the declarative boundary."""

    health: str
    capabilities: str
    plan_navigation: str
    guide_navigation: str
    execute_navigation: str

    def __post_init__(self) -> None:
        values = [
            self.health,
            self.capabilities,
            self.plan_navigation,
            self.guide_navigation,
            self.execute_navigation,
        ]
        cleaned = [_required_text(value, "operation identifier") for value in values]
        if len(set(cleaned)) != len(cleaned):
            raise ValueError("Ariane operation identifiers must be unique")
        for field_name, value in zip(self.__dataclass_fields__, cleaned, strict=True):
            object.__setattr__(self, field_name, value)


@dataclass(frozen=True, slots=True)
class ArianeClient:
    """Strict client that delegates all subsystem behavior to an injected transport."""

    transport: ArianeTransport
    operations: ArianeOperationMap
    contract_version: str
    timeout_seconds: float = 5.0

    def __post_init__(self) -> None:
        if not isinstance(self.transport, ArianeTransport):
            raise TypeError("transport must implement ArianeTransport")
        object.__setattr__(self, "contract_version", _required_text(self.contract_version, "contract_version"))
        if not isinstance(self.timeout_seconds, (int, float)) or not (0 < self.timeout_seconds <= 60):
            raise ValueError("timeout_seconds must be greater than 0 and no more than 60")
        object.__setattr__(self, "timeout_seconds", float(self.timeout_seconds))

    def read_health(self, *, request_id: str) -> Mapping[str, Any]:
        return self._invoke(self.operations.health, request_id=request_id, payload={})

    def read_capabilities(self, *, request_id: str) -> Mapping[str, Any]:
        return self._invoke(self.operations.capabilities, request_id=request_id, payload={})

    def plan(self, payload: Mapping[str, JsonValue], *, request_id: str) -> Mapping[str, Any]:
        return self._invoke(self.operations.plan_navigation, request_id=request_id, payload=payload)

    def guide(self, payload: Mapping[str, JsonValue], *, request_id: str) -> Mapping[str, Any]:
        return self._invoke(self.operations.guide_navigation, request_id=request_id, payload=payload)

    def execute(self, payload: Mapping[str, JsonValue], *, request_id: str) -> Mapping[str, Any]:
        return self._invoke(self.operations.execute_navigation, request_id=request_id, payload=payload)

    def _invoke(
        self,
        operation: str,
        *,
        request_id: str,
        payload: Mapping[str, JsonValue],
    ) -> Mapping[str, Any]:
        request_id = _required_text(request_id, "request_id")
        envelope: dict[str, JsonValue] = {
            "contract_version": self.contract_version,
            "request_id": request_id,
            "payload": _json_object(payload, "payload"),
        }
        try:
            raw = self.transport.invoke(
                operation,
                MappingProxyType(envelope),
                timeout_seconds=self.timeout_seconds,
            )
        except ArianeClientError:
            raise
        except TimeoutError as exc:
            raise ArianeClientError(
                ClientFailureKind.TIMEOUT,
                "ARIANE_TRANSPORT_TIMEOUT",
                "Ariane transport timed out",
                retryable=False,
            ) from exc
        except Exception as exc:  # transport-specific failures are bounded here
            raise ArianeClientError(
                ClientFailureKind.UNAVAILABLE,
                "ARIANE_TRANSPORT_UNAVAILABLE",
                "Ariane transport is unavailable",
                retryable=False,
            ) from exc
        if not isinstance(raw, Mapping):
            raise ArianeClientError(
                ClientFailureKind.INVALID_RESPONSE,
                "ARIANE_RESPONSE_NOT_OBJECT",
                "Ariane response must be an object",
            )
        response_version = raw.get("contract_version")
        if response_version != self.contract_version:
            raise ArianeClientError(
                ClientFailureKind.INCOMPATIBLE,
                "ARIANE_CONTRACT_VERSION_UNSUPPORTED",
                "Ariane response contract version does not match the active adapter contract",
            )
        if raw.get("request_id") != request_id:
            raise ArianeClientError(
                ClientFailureKind.INVALID_RESPONSE,
                "ARIANE_RESPONSE_REQUEST_MISMATCH",
                "Ariane response request_id does not match the request",
            )
        status = raw.get("status")
        if status not in {"ok", "rejected", "failed"}:
            raise ArianeClientError(
                ClientFailureKind.INVALID_RESPONSE,
                "ARIANE_RESPONSE_STATUS_INVALID",
                "Ariane response status is missing or invalid",
            )
        if status != "ok":
            reason_code = raw.get("reason_code")
            raise ArianeClientError(
                ClientFailureKind.REJECTED,
                _required_text(reason_code, "reason_code"),
                "Ariane rejected or failed the bounded request",
                retryable=False,
            )
        response_payload = raw.get("payload")
        if not isinstance(response_payload, Mapping):
            raise ArianeClientError(
                ClientFailureKind.INVALID_RESPONSE,
                "ARIANE_RESPONSE_PAYLOAD_INVALID",
                "Ariane response payload must be an object",
            )
        return MappingProxyType(dict(response_payload))


def _required_text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def _json_object(value: Mapping[str, JsonValue], field: str) -> dict[str, JsonValue]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{field} must be a mapping")
    result: dict[str, JsonValue] = {}
    for key in sorted(value):
        clean_key = _required_text(key, f"{field} key")
        result[clean_key] = _json_value(value[key], f"{field}.{clean_key}")
    return result


def _json_value(value: JsonValue, field: str) -> JsonValue:
    if value is None or isinstance(value, (str, bool, int, float)):
        if isinstance(value, float) and (value != value or value in (float("inf"), float("-inf"))):
            raise ValueError(f"{field} must be finite")
        return value
    if isinstance(value, list):
        return [_json_value(item, f"{field}[]") for item in value]
    if isinstance(value, Mapping):
        return _json_object(value, field)
    raise TypeError(f"{field} contains a non-JSON value")
