"""Boundary client for the independently owned Orgo subsystem.

The client forwards only operations declared by the integration configuration.  It
never interprets Orgo's domain model and never treats transport success as local
authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from threading import RLock
from time import monotonic
from types import MappingProxyType
from typing import Any, Callable, Mapping, Protocol


class OperationMode(StrEnum):
    QUERY = "query"
    COMMAND = "command"
    SURFACE = "surface"


class AuthorityEffect(StrEnum):
    NONE = "none"
    CANDIDATE_INPUT_ONLY = "candidate_input_only"
    TRANSPORT_ONLY = "transport_only"
    EVIDENCE_ONLY = "evidence_only"
    AUTHORITATIVE_AFTER_EXPLICIT_ACCEPTANCE = "authoritative_after_explicit_acceptance"
    CROSS_DOMAIN_PUBLICATION = "cross_domain_publication"


class ClientState(StrEnum):
    SUCCEEDED = "succeeded"
    REJECTED = "rejected"
    UNAVAILABLE = "unavailable"
    INDETERMINATE = "indeterminate"


class FailureClass(StrEnum):
    VALIDATION = "validation"
    AUTHORIZATION = "authorization"
    COMPATIBILITY = "compatibility"
    TRANSIENT = "transient"
    PERMANENT = "permanent"
    TIMEOUT = "timeout"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class OperationDeclaration:
    operation_id: str
    mode: OperationMode
    authority_effect: AuthorityEffect
    capability_id: str
    timeout_seconds: float
    idempotency_required: bool
    user_visible: bool

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "OperationDeclaration":
        required = {
            "operation_id",
            "mode",
            "authority_effect",
            "capability_id",
            "timeout_seconds",
            "idempotency_required",
            "user_visible",
        }
        unknown = set(value) - required
        missing = required - set(value)
        if unknown or missing:
            raise ValueError(f"invalid operation declaration; missing={sorted(missing)} unknown={sorted(unknown)}")
        operation_id = _non_empty(value["operation_id"], "operation_id")
        capability_id = _non_empty(value["capability_id"], "capability_id")
        timeout = value["timeout_seconds"]
        if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or timeout <= 0:
            raise ValueError("timeout_seconds must be a positive number")
        if not isinstance(value["idempotency_required"], bool) or not isinstance(value["user_visible"], bool):
            raise ValueError("idempotency_required and user_visible must be booleans")
        mode = OperationMode(str(value["mode"]))
        effect = AuthorityEffect(str(value["authority_effect"]))
        if mode is OperationMode.QUERY and value["idempotency_required"]:
            raise ValueError("query operations must not require an idempotency key")
        if mode is OperationMode.SURFACE and effect is not AuthorityEffect.NONE:
            raise ValueError("surface operations must have no authority effect")
        return cls(
            operation_id=operation_id,
            mode=mode,
            authority_effect=effect,
            capability_id=capability_id,
            timeout_seconds=float(timeout),
            idempotency_required=value["idempotency_required"],
            user_visible=value["user_visible"],
        )


@dataclass(frozen=True, slots=True)
class TransportResponse:
    accepted: bool
    status_code: str
    payload: Mapping[str, Any]
    remote_reference: str | None = None
    authoritative_commit: bool = False

    def __post_init__(self) -> None:
        if not self.status_code:
            raise ValueError("status_code is required")
        object.__setattr__(self, "payload", MappingProxyType(dict(self.payload)))
        if self.authoritative_commit:
            raise ValueError("an Orgo transport response cannot assert local authoritative commit")


@dataclass(frozen=True, slots=True)
class ClientResult:
    state: ClientState
    operation_id: str
    correlation_id: str
    payload: Mapping[str, Any]
    reason_code: str
    remote_reference: str | None = None
    failure_class: FailureClass | None = None
    retryable: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "payload", MappingProxyType(dict(self.payload)))
        if self.state is ClientState.SUCCEEDED and self.failure_class is not None:
            raise ValueError("successful result cannot contain a failure class")
        if self.state is not ClientState.SUCCEEDED and self.failure_class is None:
            raise ValueError("non-success result requires a failure class")


class OrgoTransport(Protocol):
    """Injected transport implemented by the deployment adapter, not by this bundle."""

    def invoke(
        self,
        *,
        operation_id: str,
        payload: Mapping[str, Any],
        identity_context: Mapping[str, Any],
        correlation_id: str,
        idempotency_key: str | None,
        timeout_seconds: float,
    ) -> TransportResponse:
        raise NotImplementedError

    def probe(self, *, timeout_seconds: float) -> Mapping[str, Any]:
        raise NotImplementedError


class TransportError(RuntimeError):
    def __init__(self, reason_code: str, failure_class: FailureClass, *, retryable: bool) -> None:
        super().__init__(reason_code)
        self.reason_code = reason_code
        self.failure_class = failure_class
        self.retryable = retryable


class CircuitOpenError(RuntimeError):
    """Raised when a remote call is blocked by the integration circuit."""


class CircuitBreaker:
    """Small deterministic circuit breaker for one external boundary."""

    def __init__(
        self,
        *,
        failure_threshold: int,
        reset_after_seconds: float,
        monotonic_clock: Callable[[], float] = monotonic,
    ) -> None:
        if failure_threshold < 1:
            raise ValueError("failure_threshold must be at least one")
        if reset_after_seconds <= 0:
            raise ValueError("reset_after_seconds must be positive")
        self._failure_threshold = failure_threshold
        self._reset_after_seconds = float(reset_after_seconds)
        self._clock = monotonic_clock
        self._lock = RLock()
        self._failures = 0
        self._opened_at: float | None = None
        self._half_open_probe_in_flight = False

    @property
    def state(self) -> str:
        with self._lock:
            if self._opened_at is None:
                return "closed"
            if self._clock() - self._opened_at >= self._reset_after_seconds:
                return "half_open"
            return "open"

    def before_call(self) -> None:
        with self._lock:
            state = self.state
            if state == "open":
                raise CircuitOpenError("orgo_circuit_open")
            if state == "half_open":
                if self._half_open_probe_in_flight:
                    raise CircuitOpenError("orgo_half_open_probe_in_progress")
                self._half_open_probe_in_flight = True

    def record_success(self) -> None:
        with self._lock:
            self._failures = 0
            self._opened_at = None
            self._half_open_probe_in_flight = False

    def record_failure(self) -> None:
        with self._lock:
            self._failures += 1
            self._half_open_probe_in_flight = False
            if self._failures >= self._failure_threshold:
                self._opened_at = self._clock()


class OrgoClient:
    def __init__(
        self,
        *,
        transport: OrgoTransport,
        operations: Mapping[str, OperationDeclaration],
        circuit_breaker: CircuitBreaker,
    ) -> None:
        if not operations:
            raise ValueError("at least one declared operation is required")
        self._transport = transport
        self._operations = MappingProxyType(dict(operations))
        self._circuit = circuit_breaker

    @property
    def operations(self) -> Mapping[str, OperationDeclaration]:
        return self._operations

    @property
    def circuit_state(self) -> str:
        return self._circuit.state

    def invoke(
        self,
        *,
        operation_id: str,
        expected_mode: OperationMode,
        payload: Mapping[str, Any],
        identity_context: Mapping[str, Any],
        correlation_id: str,
        idempotency_key: str | None = None,
    ) -> ClientResult:
        declaration = self._operations.get(operation_id)
        if declaration is None:
            return _failure(
                ClientState.REJECTED,
                operation_id,
                correlation_id,
                "undeclared_operation",
                FailureClass.VALIDATION,
            )
        if declaration.mode is not expected_mode:
            return _failure(
                ClientState.REJECTED,
                operation_id,
                correlation_id,
                "operation_mode_mismatch",
                FailureClass.VALIDATION,
            )
        if declaration.authority_effect is AuthorityEffect.CROSS_DOMAIN_PUBLICATION:
            return _failure(
                ClientState.REJECTED,
                operation_id,
                correlation_id,
                "publication_gateway_required",
                FailureClass.AUTHORIZATION,
            )
        if declaration.idempotency_required and not _is_non_empty(idempotency_key):
            return _failure(
                ClientState.REJECTED,
                operation_id,
                correlation_id,
                "idempotency_key_required",
                FailureClass.VALIDATION,
            )
        try:
            _validate_identity_context(identity_context)
            _non_empty(correlation_id, "correlation_id")
            self._circuit.before_call()
        except CircuitOpenError as exc:
            return _failure(
                ClientState.UNAVAILABLE,
                operation_id,
                correlation_id,
                str(exc),
                FailureClass.TRANSIENT,
                retryable=True,
            )
        except ValueError as exc:
            return _failure(
                ClientState.REJECTED,
                operation_id,
                correlation_id,
                str(exc),
                FailureClass.VALIDATION,
            )
        try:
            response = self._transport.invoke(
                operation_id=operation_id,
                payload=MappingProxyType(dict(payload)),
                identity_context=MappingProxyType(dict(identity_context)),
                correlation_id=correlation_id,
                idempotency_key=idempotency_key,
                timeout_seconds=declaration.timeout_seconds,
            )
        except TransportError as exc:
            self._circuit.record_failure()
            state = ClientState.INDETERMINATE if expected_mode is OperationMode.COMMAND and exc.retryable else ClientState.UNAVAILABLE
            return _failure(
                state,
                operation_id,
                correlation_id,
                exc.reason_code,
                exc.failure_class,
                retryable=exc.retryable,
            )
        except (TimeoutError, ConnectionError):
            self._circuit.record_failure()
            state = ClientState.INDETERMINATE if expected_mode is OperationMode.COMMAND else ClientState.UNAVAILABLE
            return _failure(
                state,
                operation_id,
                correlation_id,
                "orgo_transport_unavailable",
                FailureClass.TIMEOUT,
                retryable=True,
            )
        except Exception:
            self._circuit.record_failure()
            return _failure(
                ClientState.INDETERMINATE if expected_mode is OperationMode.COMMAND else ClientState.UNAVAILABLE,
                operation_id,
                correlation_id,
                "orgo_transport_failed_closed",
                FailureClass.UNKNOWN,
                retryable=False,
            )
        self._circuit.record_success()
        if not response.accepted:
            return ClientResult(
                state=ClientState.REJECTED,
                operation_id=operation_id,
                correlation_id=correlation_id,
                payload=response.payload,
                reason_code=response.status_code,
                remote_reference=response.remote_reference,
                failure_class=FailureClass.PERMANENT,
                retryable=False,
            )
        return ClientResult(
            state=ClientState.SUCCEEDED,
            operation_id=operation_id,
            correlation_id=correlation_id,
            payload=response.payload,
            reason_code=response.status_code,
            remote_reference=response.remote_reference,
        )


def _failure(
    state: ClientState,
    operation_id: str,
    correlation_id: str,
    reason_code: str,
    failure_class: FailureClass,
    *,
    retryable: bool = False,
) -> ClientResult:
    return ClientResult(
        state=state,
        operation_id=operation_id,
        correlation_id=correlation_id,
        payload={},
        reason_code=reason_code,
        failure_class=failure_class,
        retryable=retryable,
    )


def _validate_identity_context(value: Mapping[str, Any]) -> None:
    if value.get("verified") is not True:
        raise ValueError("verified_identity_required")
    _non_empty(value.get("actor_id"), "identity_context.actor_id")
    _non_empty(value.get("authority_domain"), "identity_context.authority_domain")


def _non_empty(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field}_required")
    return value


def _is_non_empty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())
