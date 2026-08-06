"""Transport-neutral client boundary for the independently owned SenTient subsystem.

The adapter never assumes an HTTP route, socket path, database, queue, or internal
SenTient command.  B-0069 supplies an opaque operation map and a transport that
implements the declared interface.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping, Protocol, runtime_checkable

JsonScalar = str | int | float | bool | None
JsonValue = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]


class ClientFailureKind(str, Enum):
    """Bounded failure classes observable at the integration boundary."""

    UNAVAILABLE = "unavailable"
    TIMEOUT = "timeout"
    AUTHENTICATION = "authentication_failure"
    INCOMPATIBLE = "incompatible"
    INVALID_RESPONSE = "invalid_response"
    REJECTED = "rejected"
    CONFLICT = "conflict"


class SentientClientError(RuntimeError):
    """A deterministic transport or contract failure from SenTient."""

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
class SentientTransport(Protocol):
    """Injected transport implemented by the declared integration boundary."""

    def request(
        self,
        operation: str,
        payload: Mapping[str, JsonValue],
        *,
        timeout_seconds: float,
    ) -> Mapping[str, Any]:
        """Execute one declared operation and return a decoded object."""


@dataclass(frozen=True, slots=True)
class SentientOperationMap:
    """Opaque operation names supplied by B-0069.

    Field names describe kOA adapter responsibilities.  Values are interface
    identifiers owned by the independently maintained subsystem contract.
    """

    health: str
    capabilities: str
    submit_job: str
    read_job: str
    cancel_job: str
    fetch_candidate: str

    def __post_init__(self) -> None:
        values = []
        for field in (
            "health",
            "capabilities",
            "submit_job",
            "read_job",
            "cancel_job",
            "fetch_candidate",
        ):
            value = _required_text(getattr(self, field), field)
            object.__setattr__(self, field, value)
            values.append(value)
        if len(set(values)) != len(values):
            raise ValueError("Sentient operation identifiers must be unique")

    def as_mapping(self) -> Mapping[str, str]:
        return MappingProxyType(
            {
                "health": self.health,
                "capabilities": self.capabilities,
                "submit_job": self.submit_job,
                "read_job": self.read_job,
                "cancel_job": self.cancel_job,
                "fetch_candidate": self.fetch_candidate,
            }
        )


@dataclass(slots=True)
class SentientClient:
    """Small defensive client around a transport supplied by the integration."""

    transport: SentientTransport
    operations: SentientOperationMap
    contract_version: str
    timeout_seconds: float = 10.0

    def __post_init__(self) -> None:
        if not isinstance(self.transport, SentientTransport):
            raise TypeError("transport must implement SentientTransport")
        self.contract_version = _required_text(self.contract_version, "contract_version")
        if not (0 < float(self.timeout_seconds) <= 120):
            raise ValueError("timeout_seconds must be greater than zero and no more than 120")
        self.timeout_seconds = float(self.timeout_seconds)

    def health(self) -> Mapping[str, Any]:
        return self._call(self.operations.health, {})

    def capabilities(self) -> Mapping[str, Any]:
        return self._call(self.operations.capabilities, {})

    def submit_job(self, payload: Mapping[str, JsonValue]) -> Mapping[str, Any]:
        return self._call(self.operations.submit_job, payload)

    def read_job(self, job_id: str) -> Mapping[str, Any]:
        return self._call(self.operations.read_job, {"job_id": _required_text(job_id, "job_id")})

    def cancel_job(self, job_id: str, reason_code: str) -> Mapping[str, Any]:
        return self._call(
            self.operations.cancel_job,
            {
                "job_id": _required_text(job_id, "job_id"),
                "reason_code": _required_text(reason_code, "reason_code"),
            },
        )

    def fetch_candidate(self, candidate_id: str) -> Mapping[str, Any]:
        return self._call(
            self.operations.fetch_candidate,
            {"candidate_id": _required_text(candidate_id, "candidate_id")},
        )

    def _call(
        self,
        operation: str,
        payload: Mapping[str, JsonValue],
    ) -> Mapping[str, Any]:
        request_payload: dict[str, JsonValue] = {
            "contract_version": self.contract_version,
            "payload": _normalize_json_object(payload, "payload"),
        }
        try:
            response = self.transport.request(
                operation,
                request_payload,
                timeout_seconds=self.timeout_seconds,
            )
        except SentientClientError:
            raise
        except TimeoutError as exc:
            raise SentientClientError(
                ClientFailureKind.TIMEOUT,
                "SENTIENT_TIMEOUT",
                "SenTient operation timed out",
                retryable=True,
            ) from exc
        except (ConnectionError, OSError) as exc:
            raise SentientClientError(
                ClientFailureKind.UNAVAILABLE,
                "SENTIENT_UNAVAILABLE",
                "SenTient transport is unavailable",
                retryable=True,
            ) from exc
        except Exception as exc:  # defensive adapter boundary
            raise SentientClientError(
                ClientFailureKind.UNAVAILABLE,
                "SENTIENT_TRANSPORT_FAILURE",
                "SenTient transport failed without a declared error",
                retryable=False,
            ) from exc

        if not isinstance(response, Mapping):
            raise SentientClientError(
                ClientFailureKind.INVALID_RESPONSE,
                "SENTIENT_RESPONSE_NOT_OBJECT",
                "SenTient response must be an object",
            )
        response_version = response.get("contract_version")
        if response_version != self.contract_version:
            raise SentientClientError(
                ClientFailureKind.INCOMPATIBLE,
                "SENTIENT_CONTRACT_VERSION_MISMATCH",
                "SenTient response contract version is incompatible",
            )
        status = response.get("status")
        if status not in {"ok", "rejected", "conflict"}:
            raise SentientClientError(
                ClientFailureKind.INVALID_RESPONSE,
                "SENTIENT_RESPONSE_STATUS_INVALID",
                "SenTient response status is invalid",
            )
        if status != "ok":
            kind = ClientFailureKind.CONFLICT if status == "conflict" else ClientFailureKind.REJECTED
            raise SentientClientError(
                kind,
                _required_text(response.get("reason_code", "SENTIENT_REJECTED"), "reason_code"),
                _required_text(response.get("message", "SenTient rejected the request"), "message"),
                retryable=bool(response.get("retryable", False)),
            )
        result = response.get("result")
        if not isinstance(result, Mapping):
            raise SentientClientError(
                ClientFailureKind.INVALID_RESPONSE,
                "SENTIENT_RESULT_NOT_OBJECT",
                "SenTient successful response must contain an object result",
            )
        return MappingProxyType(dict(result))


def _required_text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    if len(value.strip()) > 1024:
        raise ValueError(f"{field} must not exceed 1024 characters")
    return value.strip()


def _normalize_json_object(value: Mapping[str, JsonValue], field: str) -> dict[str, JsonValue]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{field} must be an object")
    return {str(key): _normalize_json(item, f"{field}.{key}") for key, item in sorted(value.items())}


def _normalize_json(value: JsonValue, field: str) -> JsonValue:
    if value is None or isinstance(value, (str, int, bool)):
        return value
    if isinstance(value, float):
        if value != value or value in {float("inf"), float("-inf")}:
            raise ValueError(f"{field} must be finite")
        return value
    if isinstance(value, list):
        if len(value) > 4096:
            raise ValueError(f"{field} contains too many items")
        return [_normalize_json(item, f"{field}[]") for item in value]
    if isinstance(value, dict):
        return _normalize_json_object(value, field)
    raise TypeError(f"{field} contains a non-JSON value")
