"""Injected-transport client that does not reproduce Konnaxion internals."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
import hashlib
import json
import re
from threading import RLock
from typing import Any, Protocol

from .capabilities import CapabilityCatalog, DependencyState
from .receipts import BoundaryOutcome, BoundaryReceipt, ReceiptFactory


class TransportUnavailable(RuntimeError):
    """The declared Konnaxion transport is unavailable."""


class TransportTimeout(RuntimeError):
    """Execution may have occurred; status lookup is required."""


class IncompatibleResponse(RuntimeError):
    """The response cannot be interpreted under the declared contract."""


class RequestConflict(ValueError):
    """An idempotency key was reused for different request material."""


class Transport(Protocol):
    def send(self, request: "AdapterRequest") -> "TransportResponse":
        """Send one declared request through an implementation-owned transport."""
        raise NotImplementedError("a transport implementation is required")


@dataclass(frozen=True, slots=True)
class RequestContext:
    actor_ref: str
    tenant_ref: str
    purpose: str
    correlation_id: str
    idempotency_key: str
    contract_version: str
    identity_verified: bool
    governance_authorized: bool


@dataclass(frozen=True, slots=True)
class AdapterRequest:
    operation: str
    capability_id: str
    context: RequestContext
    payload: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class TransportResponse:
    status_code: int
    payload: Mapping[str, Any]
    remote_reference: str | None = None
    contract_version: str = "1.0.0"


@dataclass(frozen=True, slots=True)
class AdapterResponse:
    transport_status: str
    candidate_payload: Mapping[str, Any] | None
    authoritative: bool
    receipt: BoundaryReceipt


_STABLE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/@+-]{2,254}$")
_OPERATION = re.compile(r"^[a-z][a-z0-9_.:-]{2,127}$")
_SECRET_KEYS = {"access_token", "api_key", "authorization", "cookie", "password", "private_key", "secret", "token"}


class BoundaryClient:
    """Forward declared operations exactly once per in-process idempotency record.

    A successful transport response is returned as candidate material only.  It
    never means local authoritative acceptance.
    """

    def __init__(
        self,
        *,
        transport: Transport,
        capability_catalog: CapabilityCatalog,
        observations: Mapping[str, DependencyState],
        allowed_operations: Mapping[str, str],
        max_payload_bytes: int = 65536,
        receipt_factory: ReceiptFactory | None = None,
    ) -> None:
        if max_payload_bytes < 1 or max_payload_bytes > 1_048_576:
            raise ValueError("max_payload_bytes must be between 1 and 1048576")
        normalized: dict[str, str] = {}
        for operation, capability_id in allowed_operations.items():
            if not _OPERATION.fullmatch(operation):
                raise ValueError(f"invalid declared operation: {operation!r}")
            if capability_id not in capability_catalog.declarations:
                raise ValueError(f"operation references undeclared capability: {capability_id}")
            normalized[operation] = capability_id
        if not normalized:
            raise ValueError("at least one declared operation is required")
        self._transport = transport
        self._catalog = capability_catalog
        self._observations = dict(observations)
        self._allowed_operations = dict(sorted(normalized.items()))
        self._max_payload_bytes = max_payload_bytes
        self._receipt_factory = receipt_factory or ReceiptFactory()
        self._seen: dict[str, tuple[str, AdapterResponse]] = {}
        self._lock = RLock()

    def invoke(self, request: AdapterRequest, *, observed_at: datetime) -> AdapterResponse:
        digest = self._validate_request(request)
        with self._lock:
            previous = self._seen.get(request.context.idempotency_key)
            if previous is not None:
                previous_digest, previous_response = previous
                if previous_digest != digest:
                    raise RequestConflict("idempotency key reused with different payload or context")
                duplicate = self._receipt(
                    request, observed_at, digest, BoundaryOutcome.DUPLICATE, "duplicate_effect_prevented",
                    remote_reference=previous_response.receipt.remote_reference,
                )
                return AdapterResponse(
                    transport_status="duplicate",
                    candidate_payload=deepcopy(previous_response.candidate_payload),
                    authoritative=False,
                    receipt=duplicate,
                )

            blocked = self._preflight_reason(request)
            if blocked is not None:
                response = AdapterResponse(
                    transport_status="blocked",
                    candidate_payload=None,
                    authoritative=False,
                    receipt=self._receipt(request, observed_at, digest, BoundaryOutcome.BLOCKED, blocked),
                )
                self._seen[request.context.idempotency_key] = (digest, response)
                return response

            try:
                remote = self._transport.send(request)
            except TransportTimeout:
                response = AdapterResponse(
                    transport_status="indeterminate",
                    candidate_payload=None,
                    authoritative=False,
                    receipt=self._receipt(
                        request, observed_at, digest, BoundaryOutcome.BLOCKED,
                        "timeout_status_lookup_required",
                    ),
                )
            except TransportUnavailable:
                response = AdapterResponse(
                    transport_status="unavailable",
                    candidate_payload=None,
                    authoritative=False,
                    receipt=self._receipt(
                        request, observed_at, digest, BoundaryOutcome.FAILED,
                        "external_subsystem_unavailable",
                    ),
                )
            else:
                response = self._translate_response(request, remote, observed_at, digest)

            self._seen[request.context.idempotency_key] = (digest, response)
            return response

    def _validate_request(self, request: AdapterRequest) -> str:
        if request.operation not in self._allowed_operations:
            raise ValueError(f"undeclared operation: {request.operation}")
        expected = self._allowed_operations[request.operation]
        if request.capability_id != expected:
            raise ValueError("operation capability mismatch")
        context = request.context
        for name in ("actor_ref", "tenant_ref", "purpose", "correlation_id", "idempotency_key"):
            value = getattr(context, name)
            if not isinstance(value, str) or not _STABLE.fullmatch(value):
                raise ValueError(f"{name} must be a stable reference")
        if context.contract_version != "1.0.0":
            raise ValueError("unsupported subsystem contract version")
        payload = deepcopy(dict(request.payload))
        _reject_secret_fields(payload)
        encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")
        if len(encoded) > self._max_payload_bytes:
            raise ValueError("payload exceeds declared inline limit")
        digest_material = {
            "operation": request.operation,
            "capability_id": request.capability_id,
            "actor_ref": context.actor_ref,
            "tenant_ref": context.tenant_ref,
            "purpose": context.purpose,
            "contract_version": context.contract_version,
            "payload": payload,
        }
        canonical = json.dumps(digest_material, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def _preflight_reason(self, request: AdapterRequest) -> str | None:
        context = request.context
        if not context.identity_verified:
            return "identity_not_verified"
        if not context.governance_authorized:
            return "governance_not_authorized"
        snapshot = self._catalog.snapshot_for(request.capability_id, self._observations)
        if not snapshot.usable:
            return f"capability_{snapshot.state.value}"
        return None

    def _translate_response(
        self, request: AdapterRequest, remote: TransportResponse, observed_at: datetime, digest: str
    ) -> AdapterResponse:
        if remote.contract_version != request.context.contract_version:
            raise IncompatibleResponse("remote contract version mismatch")
        if not 100 <= remote.status_code <= 599:
            raise IncompatibleResponse("remote status code outside HTTP-compatible range")
        payload = deepcopy(dict(remote.payload))
        _reject_secret_fields(payload)
        if 200 <= remote.status_code < 300:
            outcome = BoundaryOutcome.FORWARDED
            status = "forwarded"
            reason = "transport_acknowledged_not_authoritative"
            candidate = payload
        elif remote.status_code in {401, 403}:
            outcome = BoundaryOutcome.REJECTED
            status = "rejected"
            reason = "remote_authorization_rejected"
            candidate = None
        elif remote.status_code in {408, 429, 500, 502, 503, 504}:
            outcome = BoundaryOutcome.FAILED
            status = "unavailable"
            reason = "remote_transient_failure_no_automatic_retry"
            candidate = None
        else:
            outcome = BoundaryOutcome.REJECTED
            status = "rejected"
            reason = "remote_request_rejected"
            candidate = None
        return AdapterResponse(
            transport_status=status,
            candidate_payload=candidate,
            authoritative=False,
            receipt=self._receipt(
                request, observed_at, digest, outcome, reason, remote_reference=remote.remote_reference,
                details={"remote_status_code": remote.status_code},
            ),
        )

    def _receipt(
        self,
        request: AdapterRequest,
        observed_at: datetime,
        digest: str,
        outcome: BoundaryOutcome,
        reason: str,
        *,
        remote_reference: str | None = None,
        details: Mapping[str, Any] | None = None,
    ) -> BoundaryReceipt:
        return self._receipt_factory.issue(
            issued_at=observed_at,
            correlation_id=request.context.correlation_id,
            idempotency_key=request.context.idempotency_key,
            operation=request.operation,
            request_digest=digest,
            outcome=outcome,
            reason_code=reason,
            remote_reference=remote_reference,
            details=details,
        )


def _reject_secret_fields(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            if str(key).lower() in _SECRET_KEYS:
                raise ValueError(f"secret-like payload field prohibited: {key}")
            _reject_secret_fields(child)
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for child in value:
            _reject_secret_fields(child)
