"""Bounded, direction-preserving client for the external UCKK boundary."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from hashlib import sha256
import json
import threading
import time
import re
from typing import Any, Callable, Mapping, Protocol, Sequence, runtime_checkable

from .receipts import (
    Direction,
    ItemOutcome,
    TerminalOutcome,
    TerminalReceipt,
    ReceiptValidationError,
    build_dead_letter_record,
    build_terminal_receipt,
    canonical_json,
)


class FailureClass(StrEnum):
    TIMEOUT = "timeout"
    UNAVAILABLE = "unavailable"
    RATE_LIMITED = "rate_limited"
    REMOTE_5XX = "remote_5xx"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    VALIDATION = "validation"
    COMPATIBILITY = "compatibility"
    INTEGRITY = "integrity"
    AMBIGUOUS_OUTCOME = "ambiguous_outcome"
    CIRCUIT_OPEN = "circuit_open"
    UNKNOWN = "unknown"


class CircuitState(StrEnum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


_REASON_CODE_RE = re.compile(r"^[a-z][a-z0-9_]{2,127}$")


class ExternalCallError(RuntimeError):
    """Classified provider failure raised by a deployment transport."""

    def __init__(
        self,
        failure_class: FailureClass,
        reason_code: str,
        summary: str,
        *,
        retryable: bool | None = None,
        outcome_unknown: bool = False,
    ) -> None:
        if not isinstance(failure_class, FailureClass):
            raise TypeError("failure_class must be a FailureClass")
        if not isinstance(reason_code, str) or not _REASON_CODE_RE.fullmatch(reason_code):
            raise ValueError("reason_code must be a stable snake_case identifier")
        if not isinstance(summary, str) or not summary.strip():
            raise ValueError("summary must be a non-empty string")
        super().__init__(summary)
        self.failure_class = failure_class
        self.reason_code = reason_code
        self.summary = summary.strip()[:2048]
        self.retryable = retryable
        self.outcome_unknown = outcome_unknown


class ClientConfigurationError(ValueError):
    """Raised when the adapter is configured outside the declared envelope."""


@runtime_checkable
class UckkTransport(Protocol):
    """Deployment-owned public transport; it exposes no UCKK internals."""

    def request(
        self,
        direction: str,
        operation: str,
        payload: Mapping[str, Any],
        *,
        timeout_ms: int,
        correlation_id: str,
        idempotency_key: str,
    ) -> Mapping[str, Any]:
        """Execute one registered operation and return a JSON object."""

    def probe(self, direction: str, *, timeout_ms: int) -> Mapping[str, Any]:
        """Return a side-effect-free health observation for one direction."""


@runtime_checkable
class ReceiptSink(Protocol):
    def record_terminal_receipt(self, receipt: Mapping[str, Any]) -> None:
        """Persist or audit one terminal adapter receipt."""


@runtime_checkable
class DeadLetterSink(Protocol):
    def quarantine(self, record: Mapping[str, Any]) -> None:
        """Persist one immutable visible quarantine record."""


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    maximum_attempts: int
    backoff_base_ms: int
    backoff_multiplier: float
    backoff_max_ms: int
    retryable_failure_classes: frozenset[FailureClass]
    full_jitter: bool = True

    def __post_init__(self) -> None:
        if not 1 <= self.maximum_attempts <= 20:
            raise ClientConfigurationError("maximum_attempts must be in [1, 20]")
        if self.backoff_base_ms < 0 or self.backoff_max_ms < 0:
            raise ClientConfigurationError("backoff values must be non-negative")
        if self.backoff_multiplier < 1:
            raise ClientConfigurationError("backoff_multiplier must be at least 1")
        if not self.full_jitter:
            raise ClientConfigurationError("the architecture contract requires full jitter")

    def delay_ms(self, attempt_number: int, idempotency_key: str) -> int:
        if attempt_number < 1:
            raise ValueError("attempt_number must be positive")
        ceiling = min(
            self.backoff_max_ms,
            int(self.backoff_base_ms * self.backoff_multiplier ** (attempt_number - 1)),
        )
        if ceiling <= 0:
            return 0
        material = f"{idempotency_key}:{attempt_number}".encode("utf-8")
        value = int.from_bytes(sha256(material).digest()[:8], "big")
        return value % (ceiling + 1)


@dataclass(frozen=True, slots=True)
class CircuitBreakerPolicy:
    failure_threshold: int = 5
    failure_window_seconds: int = 30
    open_duration_seconds: int = 60
    half_open_max_probes: int = 1
    half_open_max_concurrency: int = 1

    def __post_init__(self) -> None:
        values = (
            self.failure_threshold,
            self.failure_window_seconds,
            self.open_duration_seconds,
            self.half_open_max_probes,
            self.half_open_max_concurrency,
        )
        if any(value < 1 for value in values):
            raise ClientConfigurationError("circuit breaker values must be positive")
        if self.half_open_max_concurrency > self.half_open_max_probes:
            raise ClientConfigurationError(
                "half_open_max_concurrency cannot exceed half_open_max_probes"
            )


@dataclass(frozen=True, slots=True)
class ResiliencePolicy:
    policy_id: str
    capability_ids: tuple[str, ...]
    attempt_timeout_ms: int
    total_timeout_ms: int
    retry: RetryPolicy
    circuit: CircuitBreakerPolicy = CircuitBreakerPolicy()
    degraded_mode: str = "queued_for_later"
    user_visible_state: str = "UCKK capability temporarily unavailable"
    version: str = "1.0.0"

    def __post_init__(self) -> None:
        if not self.policy_id or len(self.policy_id) > 128:
            raise ClientConfigurationError("policy_id is invalid")
        if not self.capability_ids or len(self.capability_ids) != len(
            set(self.capability_ids)
        ):
            raise ClientConfigurationError("capability_ids must be non-empty and unique")
        if self.attempt_timeout_ms < 1 or self.total_timeout_ms < 1:
            raise ClientConfigurationError("timeout budgets must be positive")
        if self.total_timeout_ms < self.attempt_timeout_ms:
            raise ClientConfigurationError(
                "total_timeout_ms cannot be lower than attempt_timeout_ms"
            )
        if self.degraded_mode not in {
            "capability_unavailable",
            "stale_labeled_read",
            "queued_for_later",
            "empty_non_authoritative_result",
        }:
            raise ClientConfigurationError("invalid degraded response mode")
        if not self.user_visible_state.strip():
            raise ClientConfigurationError("user_visible_state is required")

    @classmethod
    def background_default(
        cls, direction: Direction, capability_ids: Sequence[str]
    ) -> "ResiliencePolicy":
        return cls(
            policy_id=f"uckk.{direction.value}.background",
            capability_ids=tuple(capability_ids),
            attempt_timeout_ms=30_000,
            total_timeout_ms=120_000,
            retry=RetryPolicy(
                maximum_attempts=5,
                backoff_base_ms=1_000,
                backoff_multiplier=2.0,
                backoff_max_ms=300_000,
                retryable_failure_classes=frozenset(
                    {
                        FailureClass.TIMEOUT,
                        FailureClass.UNAVAILABLE,
                        FailureClass.RATE_LIMITED,
                        FailureClass.REMOTE_5XX,
                    }
                ),
            ),
        )

    def as_artifact(self) -> Mapping[str, Any]:
        return {
            "$schema": (
                "https://schemas.koa.local/artifact-contracts/"
                "integration-resilience-policy.schema.json"
            ),
            "artifact_class": "integration_resilience_policy",
            "authority": "architecture-patterns",
            "policy_id": self.policy_id,
            "version": self.version,
            "status": "active",
            "scope": {
                "profile_ids": [],
                "component_ids": ["uckk_adapter"],
                "capability_ids": list(self.capability_ids),
            },
            "destination": {
                "destination_id": "uckk",
                "boundary_kind": "external_network",
                "optional": True,
            },
            "timeout_budget": {
                "attempt_timeout_ms": self.attempt_timeout_ms,
                "total_timeout_ms": self.total_timeout_ms,
            },
            "retry_policy": {
                "maximum_attempts": self.retry.maximum_attempts,
                "backoff_base_ms": self.retry.backoff_base_ms,
                "backoff_multiplier": self.retry.backoff_multiplier,
                "backoff_max_ms": self.retry.backoff_max_ms,
                "full_jitter": True,
                "retryable_failure_classes": sorted(
                    item.value for item in self.retry.retryable_failure_classes
                ),
            },
            "circuit_breaker": {
                "states": ["closed", "open", "half_open"],
                "failure_threshold": self.circuit.failure_threshold,
                "failure_window_seconds": self.circuit.failure_window_seconds,
                "open_duration_seconds": self.circuit.open_duration_seconds,
                "half_open_max_probes": self.circuit.half_open_max_probes,
                "half_open_max_concurrency": self.circuit.half_open_max_concurrency,
                "manual_override_requires_receipt": True,
            },
            "degraded_response": {
                "mode": self.degraded_mode,
                "authoritative_success_prohibited": True,
                "user_visible_state": self.user_visible_state,
            },
            "observability": {
                "metrics": [
                    "uckk_call_total",
                    "uckk_call_duration_ms",
                    "uckk_circuit_state",
                    "uckk_quarantine_visible_total",
                ],
                "state_transition_events": True,
                "correlation_id_required": True,
            },
        }


@dataclass(frozen=True, slots=True)
class CircuitSnapshot:
    state: CircuitState
    recent_failures: int
    opened_at_monotonic: float | None
    half_open_probes: int


class CircuitBreaker:
    """Thread-safe state machine scoped to one UCKK direction."""

    def __init__(
        self,
        policy: CircuitBreakerPolicy,
        *,
        monotonic: Callable[[], float] = time.monotonic,
    ) -> None:
        self._policy = policy
        self._monotonic = monotonic
        self._lock = threading.Lock()
        self._failures: deque[float] = deque()
        self._state = CircuitState.CLOSED
        self._opened_at: float | None = None
        self._half_open_probes = 0
        self._half_open_in_flight = 0

    def _prune(self, now: float) -> None:
        threshold = now - self._policy.failure_window_seconds
        while self._failures and self._failures[0] < threshold:
            self._failures.popleft()

    def _advance(self, now: float) -> None:
        self._prune(now)
        if (
            self._state is CircuitState.OPEN
            and self._opened_at is not None
            and now - self._opened_at >= self._policy.open_duration_seconds
        ):
            self._state = CircuitState.HALF_OPEN
            self._half_open_probes = 0
            self._half_open_in_flight = 0

    def acquire(self) -> bool:
        now = self._monotonic()
        with self._lock:
            self._advance(now)
            if self._state is CircuitState.OPEN:
                return False
            if self._state is CircuitState.HALF_OPEN:
                if self._half_open_probes >= self._policy.half_open_max_probes:
                    return False
                if (
                    self._half_open_in_flight
                    >= self._policy.half_open_max_concurrency
                ):
                    return False
                self._half_open_probes += 1
                self._half_open_in_flight += 1
            return True

    def record_success(self) -> None:
        with self._lock:
            if self._state is CircuitState.HALF_OPEN:
                self._half_open_in_flight = max(0, self._half_open_in_flight - 1)
            self._state = CircuitState.CLOSED
            self._failures.clear()
            self._opened_at = None
            self._half_open_probes = 0

    def record_failure(self) -> None:
        now = self._monotonic()
        with self._lock:
            if self._state is CircuitState.HALF_OPEN:
                self._half_open_in_flight = max(0, self._half_open_in_flight - 1)
                self._state = CircuitState.OPEN
                self._opened_at = now
                return
            self._prune(now)
            self._failures.append(now)
            if len(self._failures) >= self._policy.failure_threshold:
                self._state = CircuitState.OPEN
                self._opened_at = now

    def release_probe_without_result(self) -> None:
        with self._lock:
            if self._state is CircuitState.HALF_OPEN:
                self._half_open_in_flight = max(0, self._half_open_in_flight - 1)

    def snapshot(self) -> CircuitSnapshot:
        now = self._monotonic()
        with self._lock:
            self._advance(now)
            return CircuitSnapshot(
                state=self._state,
                recent_failures=len(self._failures),
                opened_at_monotonic=self._opened_at,
                half_open_probes=self._half_open_probes,
            )


PUBLISH_OPERATIONS = frozenset(
    {
        "validate_destination_capability",
        "authenticate",
        "create_or_update_remote_representation",
        "upload_content",
        "attach_metadata",
        "query_publication_status",
        "receive_publication_receipt",
        "send_supported_withdrawal_notice",
    }
)
IMPORT_OPERATIONS = frozenset(
    {
        "discover_declared_catalog",
        "resolve_selected_source_graph",
        "authenticate",
        "retrieve_learning_package",
        "receive_offline_learning_package",
        "quarantine_package",
        "verify_manifest_and_integrity",
        "verify_source_and_signature",
        "resolve_license_and_restrictions",
        "validate_shared_frame_mapping",
        "request_local_acceptance",
        "create_local_records_after_acceptance",
        "record_import_receipt",
        "offer_remote_update_candidate",
    }
)


@dataclass(frozen=True, slots=True)
class ProbeResult:
    direction: Direction
    reachable: bool
    authenticated: bool
    compatible: bool
    reason_code: str | None
    observed_at: datetime
    circuit_state: CircuitState


@dataclass(frozen=True, slots=True)
class CallResult:
    receipt: TerminalReceipt
    response: Mapping[str, Any] | None
    dead_letter: Mapping[str, Any] | None

    @property
    def succeeded(self) -> bool:
        return self.receipt.outcome is TerminalOutcome.SUCCEEDED


@dataclass(slots=True)
class DirectionalClient:
    direction: Direction
    transport: UckkTransport
    policy: ResiliencePolicy
    allowed_operations: frozenset[str]
    receipt_sink: ReceiptSink | None = None
    dead_letter_sink: DeadLetterSink | None = None
    clock: Callable[[], datetime] = lambda: datetime.now(timezone.utc)
    monotonic: Callable[[], float] = time.monotonic
    sleeper: Callable[[float], None] = time.sleep
    circuit: CircuitBreaker = field(init=False)

    def __post_init__(self) -> None:
        if not isinstance(self.transport, UckkTransport):
            raise TypeError("transport must implement UckkTransport")
        if not self.allowed_operations:
            raise ClientConfigurationError("allowed_operations cannot be empty")
        self.circuit = CircuitBreaker(self.policy.circuit, monotonic=self.monotonic)

    def _now(self) -> datetime:
        value = self.clock()
        if value.tzinfo is None:
            raise ClientConfigurationError("clock must return timezone-aware datetime")
        return value.astimezone(timezone.utc)

    @staticmethod
    def _json_object(value: Mapping[str, Any], label: str) -> dict[str, Any]:
        if not isinstance(value, Mapping):
            raise ExternalCallError(
                FailureClass.VALIDATION,
                "invalid_boundary_object",
                f"{label} must be a JSON object",
                retryable=False,
            )
        try:
            return json.loads(canonical_json(value))
        except (TypeError, ValueError) as exc:
            raise ExternalCallError(
                FailureClass.VALIDATION,
                "non_json_boundary_value",
                f"{label} is not JSON-compatible",
                retryable=False,
            ) from exc

    @staticmethod
    def _classify_exception(exc: Exception) -> ExternalCallError:
        if isinstance(exc, ExternalCallError):
            return exc
        if isinstance(exc, ReceiptValidationError):
            return ExternalCallError(
                FailureClass.VALIDATION,
                "invalid_remote_evidence",
                "UCKK response evidence violates the adapter contract",
                retryable=False,
            )
        if isinstance(exc, TimeoutError):
            return ExternalCallError(
                FailureClass.TIMEOUT,
                "remote_timeout",
                "UCKK request timed out",
                retryable=True,
            )
        if isinstance(exc, (ConnectionError, OSError)):
            return ExternalCallError(
                FailureClass.UNAVAILABLE,
                "remote_unavailable",
                "UCKK endpoint is unavailable",
                retryable=True,
            )
        return ExternalCallError(
            FailureClass.UNKNOWN,
            "unclassified_transport_failure",
            "UCKK transport failed with an unclassified error",
            retryable=False,
        )

    def _retryable(self, failure: ExternalCallError) -> bool:
        if failure.outcome_unknown:
            return False
        if failure.retryable is not None:
            return failure.retryable and (
                failure.failure_class in self.policy.retry.retryable_failure_classes
            )
        return failure.failure_class in self.policy.retry.retryable_failure_classes

    def _record(self, receipt: TerminalReceipt) -> None:
        if self.receipt_sink is not None:
            self.receipt_sink.record_terminal_receipt(receipt.as_dict())

    def _quarantine(self, record: Mapping[str, Any]) -> None:
        if self.dead_letter_sink is not None:
            self.dead_letter_sink.quarantine(record)

    @staticmethod
    def _response_outcome(
        response: Mapping[str, Any],
    ) -> tuple[TerminalOutcome, str | None, str | None, tuple[ItemOutcome, ...]]:
        raw = response.get("outcome")
        mapping = {
            "succeeded": TerminalOutcome.SUCCEEDED,
            "accepted": TerminalOutcome.QUEUED,
            "queued": TerminalOutcome.QUEUED,
            "rejected": TerminalOutcome.REJECTED,
            "failed": TerminalOutcome.FAILED,
            "unknown": TerminalOutcome.UNKNOWN_OUTCOME,
            "partial": TerminalOutcome.PARTIAL_REQUIRES_REVIEW,
        }
        if raw not in mapping:
            raise ExternalCallError(
                FailureClass.VALIDATION,
                "missing_terminal_outcome",
                "UCKK response must declare a supported outcome",
                retryable=False,
            )
        outcome = mapping[str(raw)]
        failure_class = response.get("failure_class")
        reason_code = response.get("reason_code")
        items: tuple[ItemOutcome, ...] = ()
        if outcome is TerminalOutcome.PARTIAL_REQUIRES_REVIEW:
            raw_items = response.get("item_outcomes")
            if not isinstance(raw_items, list):
                raise ExternalCallError(
                    FailureClass.VALIDATION,
                    "partial_result_without_items",
                    "partial UCKK result requires item_outcomes",
                    retryable=False,
                )
            items = tuple(
                ItemOutcome(
                    item_ref=item.get("item_ref"),
                    outcome=item.get("outcome"),
                    reason_code=item.get("reason_code"),
                )
                for item in raw_items
                if isinstance(item, Mapping)
            )
            if len(items) != len(raw_items):
                raise ExternalCallError(
                    FailureClass.VALIDATION,
                    "invalid_partial_item",
                    "partial UCKK result contains an invalid item",
                    retryable=False,
                )
        if outcome in {
            TerminalOutcome.REJECTED,
            TerminalOutcome.FAILED,
            TerminalOutcome.UNKNOWN_OUTCOME,
            TerminalOutcome.PARTIAL_REQUIRES_REVIEW,
        }:
            if failure_class not in {item.value for item in FailureClass}:
                raise ExternalCallError(
                    FailureClass.VALIDATION,
                    "unclassified_remote_result",
                    "non-success UCKK result requires failure_class",
                    retryable=False,
                )
            if not isinstance(reason_code, str) or not _REASON_CODE_RE.fullmatch(reason_code):
                raise ExternalCallError(
                    FailureClass.VALIDATION,
                    "missing_reason_code",
                    "non-success UCKK result requires a stable reason_code",
                    retryable=False,
                )
        else:
            failure_class = None
            reason_code = None
        return outcome, failure_class, reason_code, items

    def execute(
        self,
        operation: str,
        payload: Mapping[str, Any],
        *,
        correlation_id: str,
        idempotency_key: str,
        authority_domain: str = "koa_linux",
        tenant_id: str | None = None,
    ) -> CallResult:
        if operation not in self.allowed_operations:
            raise ClientConfigurationError(
                f"operation is not registered for {self.direction.value}: {operation}"
            )
        request = self._json_object(payload, "payload")
        # Evidence construction validates these identifiers before transport use.
        started_at = self._now()
        started_monotonic = self.monotonic()
        first_failure_at: datetime | None = None
        last_failure: ExternalCallError | None = None
        attempts = 0

        while attempts < self.policy.retry.maximum_attempts:
            elapsed_ms = max(0, int((self.monotonic() - started_monotonic) * 1000))
            remaining_ms = self.policy.total_timeout_ms - elapsed_ms
            if remaining_ms <= 0:
                last_failure = ExternalCallError(
                    FailureClass.TIMEOUT,
                    "total_timeout_exhausted",
                    "total UCKK timeout budget exhausted",
                    retryable=False,
                )
                break
            if not self.circuit.acquire():
                last_failure = ExternalCallError(
                    FailureClass.CIRCUIT_OPEN,
                    "circuit_open",
                    "UCKK circuit is open for this direction",
                    retryable=False,
                )
                break

            attempts += 1
            attempt_timeout = min(self.policy.attempt_timeout_ms, remaining_ms)
            try:
                raw_response = self.transport.request(
                    self.direction.value,
                    operation,
                    request,
                    timeout_ms=attempt_timeout,
                    correlation_id=correlation_id,
                    idempotency_key=idempotency_key,
                )
                response = self._json_object(raw_response, "response")
                outcome, failure_class, reason_code, item_outcomes = (
                    self._response_outcome(response)
                )
                if outcome is TerminalOutcome.FAILED:
                    classified = FailureClass(str(failure_class))
                    raise ExternalCallError(
                        classified,
                        str(reason_code),
                        "UCKK returned a classified failed outcome",
                        retryable=(
                            classified in self.policy.retry.retryable_failure_classes
                        ),
                    )
                if outcome is TerminalOutcome.UNKNOWN_OUTCOME:
                    raise ExternalCallError(
                        FailureClass.AMBIGUOUS_OUTCOME,
                        str(reason_code),
                        "UCKK returned an ambiguous remote outcome",
                        retryable=False,
                        outcome_unknown=True,
                    )
            except Exception as exc:
                failure = self._classify_exception(exc)
                last_failure = failure
                first_failure_at = first_failure_at or self._now()
                self.circuit.record_failure()
                if failure.outcome_unknown or not self._retryable(failure):
                    break
                if attempts >= self.policy.retry.maximum_attempts:
                    break
                delay_ms = self.policy.retry.delay_ms(attempts, idempotency_key)
                elapsed_ms = max(
                    0, int((self.monotonic() - started_monotonic) * 1000)
                )
                remaining_ms = self.policy.total_timeout_ms - elapsed_ms
                if delay_ms >= remaining_ms:
                    break
                self.sleeper(delay_ms / 1000)
                continue

            self.circuit.record_success()
            completed_at = self._now()
            receipt = build_terminal_receipt(
                direction=self.direction,
                operation=operation,
                correlation_id=correlation_id,
                idempotency_key=idempotency_key,
                request=request,
                outcome=outcome,
                attempt_count=attempts,
                started_at=started_at,
                completed_at=completed_at,
                response=response,
                external_reference=(
                    response.get("external_reference")
                    if isinstance(response.get("external_reference"), str)
                    else None
                ),
                failure_class=failure_class,
                reason_code=reason_code,
                item_outcomes=item_outcomes,
            )
            self._record(receipt)
            return CallResult(receipt, response, None)

        assert last_failure is not None
        completed_at = self._now()
        permanent = last_failure.failure_class in {
            FailureClass.AUTHORIZATION,
            FailureClass.VALIDATION,
            FailureClass.COMPATIBILITY,
            FailureClass.INTEGRITY,
        }
        retry_exhausted = (
            not permanent
            and attempts >= self.policy.retry.maximum_attempts
        )
        if last_failure.outcome_unknown:
            outcome = TerminalOutcome.UNKNOWN_OUTCOME
        else:
            outcome = TerminalOutcome.QUARANTINED
        receipt = build_terminal_receipt(
            direction=self.direction,
            operation=operation,
            correlation_id=correlation_id,
            idempotency_key=idempotency_key,
            request=request,
            outcome=outcome,
            attempt_count=attempts,
            started_at=started_at,
            completed_at=completed_at,
            failure_class=last_failure.failure_class.value,
            reason_code=last_failure.reason_code,
            retry_exhausted=retry_exhausted,
        )
        message_id = f"{correlation_id}:{idempotency_key}"
        dead_letter = build_dead_letter_record(
            direction=self.direction,
            message_id=message_id,
            payload=request,
            first_failed_at=first_failure_at or completed_at,
            quarantined_at=completed_at,
            attempt_count=max(1, attempts),
            failure_class=last_failure.failure_class.value,
            reason_code=last_failure.reason_code,
            error_summary=last_failure.summary,
            permanent=permanent,
            authority_domain=authority_domain,
            tenant_id=tenant_id,
        )
        self._quarantine(dead_letter)
        self._record(receipt)
        return CallResult(receipt, None, dead_letter)

    def probe(self) -> ProbeResult:
        observed_at = self._now()
        if not self.circuit.acquire():
            return ProbeResult(
                direction=self.direction,
                reachable=False,
                authenticated=False,
                compatible=False,
                reason_code="circuit_open",
                observed_at=observed_at,
                circuit_state=CircuitState.OPEN,
            )
        try:
            raw = self.transport.probe(
                self.direction.value,
                timeout_ms=self.policy.attempt_timeout_ms,
            )
            response = self._json_object(raw, "probe response")
            reachable = response.get("reachable")
            authenticated = response.get("authenticated")
            compatible = response.get("compatible")
            if not all(
                isinstance(value, bool)
                for value in (reachable, authenticated, compatible)
            ):
                raise ExternalCallError(
                    FailureClass.VALIDATION,
                    "invalid_probe_response",
                    "UCKK probe response must contain boolean status fields",
                    retryable=False,
                )
            reason = response.get("reason_code")
            if reason is not None and not isinstance(reason, str):
                raise ExternalCallError(
                    FailureClass.VALIDATION,
                    "invalid_probe_reason",
                    "UCKK probe reason_code must be a string",
                    retryable=False,
                )
            if reachable and authenticated and compatible:
                self.circuit.record_success()
            else:
                self.circuit.record_failure()
            return ProbeResult(
                direction=self.direction,
                reachable=reachable,
                authenticated=authenticated,
                compatible=compatible,
                reason_code=reason,
                observed_at=observed_at,
                circuit_state=self.circuit.snapshot().state,
            )
        except Exception as exc:
            failure = self._classify_exception(exc)
            self.circuit.record_failure()
            return ProbeResult(
                direction=self.direction,
                reachable=False,
                authenticated=False,
                compatible=False,
                reason_code=failure.reason_code,
                observed_at=observed_at,
                circuit_state=self.circuit.snapshot().state,
            )


@dataclass(frozen=True, slots=True)
class UckkClient:
    """Shared holder of two independent directional clients."""

    publication: DirectionalClient
    import_: DirectionalClient

    def __post_init__(self) -> None:
        if self.publication.direction is not Direction.PUBLISH_TO_UCKK:
            raise ClientConfigurationError("publication client has the wrong direction")
        if self.import_.direction is not Direction.IMPORT_FROM_UCKK:
            raise ClientConfigurationError("import client has the wrong direction")
        if self.publication is self.import_ or self.publication.circuit is self.import_.circuit:
            raise ClientConfigurationError("UCKK directions must not share client state")
