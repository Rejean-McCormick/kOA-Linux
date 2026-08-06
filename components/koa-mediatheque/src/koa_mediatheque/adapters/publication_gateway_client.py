"""Public Publication Gateway adapter; never sends directly to destinations."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
import hashlib
import json
from typing import Any, Protocol, runtime_checkable


class PublicationGatewayError(RuntimeError):
    """Raised when publication admission or status evidence is invalid."""


@runtime_checkable
class PublicationGatewayTransport(Protocol):
    def submit_publication_request(
        self, request: Mapping[str, Any], *, idempotency_key: str
    ) -> Mapping[str, Any]:
        raise NotImplementedError

    def get_publication_status(self, request_id: str) -> Mapping[str, Any]:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class PublicationResult:
    request_id: str
    status: str
    decision: str | None
    receipt_ref: str | None
    response: Mapping[str, Any]


_TERMINAL = frozenset(
    {"published", "rejected", "cancelled", "withdrawn", "superseded", "failed", "conflicted", "expired", "recovery_required"}
)
_KNOWN = _TERMINAL | {
    "requested", "validating", "policy_pending", "approval_pending",
    "transformation_pending", "ready", "deferred", "submitted", "withdrawal_pending",
}


class PublicationGatewayClient:
    """Submit governed requests only through Publication Gateway's public API."""

    def __init__(
        self,
        transport: PublicationGatewayTransport | Callable[..., Mapping[str, Any]],
    ) -> None:
        self._transport = transport

    def submit(
        self, request: Mapping[str, Any], *, idempotency_key: str
    ) -> PublicationResult:
        self._validate_request(request)
        if not idempotency_key.strip():
            raise PublicationGatewayError("idempotency_key must not be empty")
        transport = self._transport
        try:
            method = getattr(transport, "submit_publication_request", None)
            if callable(method):
                response = method(request, idempotency_key=idempotency_key)
            elif callable(transport):
                response = transport(request, idempotency_key=idempotency_key)
            else:
                raise PublicationGatewayError("transport has no public publication interface")
        except PublicationGatewayError:
            raise
        except Exception as exc:
            raise PublicationGatewayError("Publication Gateway submission failed") from exc
        return self._parse_response(response, expected_request_id=str(request["request_id"]))

    def status(self, request_id: str) -> PublicationResult:
        if not request_id.strip():
            raise PublicationGatewayError("request_id must not be empty")
        method = getattr(self._transport, "get_publication_status", None)
        if not callable(method):
            raise PublicationGatewayError("transport has no public status interface")
        try:
            response = method(request_id)
        except Exception as exc:
            raise PublicationGatewayError("Publication Gateway status query failed") from exc
        return self._parse_response(response, expected_request_id=request_id)

    @staticmethod
    def derive_idempotency_key(request: Mapping[str, Any]) -> str:
        try:
            encoded = json.dumps(request, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        except (TypeError, ValueError) as exc:
            raise PublicationGatewayError("request is not JSON serializable") from exc
        return f"koa-mediatheque-publication:{hashlib.sha256(encoded.encode()).hexdigest()}"

    @staticmethod
    def _validate_request(request: Mapping[str, Any]) -> None:
        if not isinstance(request, Mapping):
            raise PublicationGatewayError("publication request must be an object")
        if request.get("artifact_class") != "publication_request":
            raise PublicationGatewayError("artifact_class must be publication_request")
        if not isinstance(request.get("request_id"), str) or not request["request_id"].strip():
            raise PublicationGatewayError("publication request_id is required")
        if request.get("status") not in {"requested", "deferred"}:
            raise PublicationGatewayError("new publication request has an invalid status")
        source = request.get("source")
        if not isinstance(source, Mapping):
            raise PublicationGatewayError("publication source must be an object")
        try:
            serialized = json.dumps(request, ensure_ascii=False, separators=(",", ":")).lower()
        except (TypeError, ValueError) as exc:
            raise PublicationGatewayError("publication request is not JSON serializable") from exc
        for prohibited in ('"content_bytes"', '"media_bytes"', '"private_key"', '"password"', '"token"'):
            if prohibited in serialized:
                raise PublicationGatewayError("publication request contains prohibited inline or secret data")

    @staticmethod
    def _parse_response(
        response: Mapping[str, Any], *, expected_request_id: str
    ) -> PublicationResult:
        if not isinstance(response, Mapping):
            raise PublicationGatewayError("Publication Gateway returned a non-object response")
        request_id = str(response.get("request_id") or "")
        if request_id != expected_request_id:
            raise PublicationGatewayError("Publication Gateway response request_id mismatch")
        status = str(response.get("status") or "")
        if status not in _KNOWN:
            raise PublicationGatewayError(f"unsupported publication status: {status!r}")
        decision_value = response.get("decision")
        decision = str(decision_value) if decision_value is not None else None
        if decision is not None and decision not in {"allow", "deny", "blocked", "review_required"}:
            raise PublicationGatewayError("unsupported publication decision")
        receipt_value = response.get("receipt_ref") or response.get("receipt_id")
        receipt_ref = str(receipt_value) if receipt_value else None
        if status in _TERMINAL and not receipt_ref:
            raise PublicationGatewayError("terminal publication outcome lacks a receipt")
        return PublicationResult(
            request_id=request_id,
            status=status,
            decision=decision,
            receipt_ref=receipt_ref,
            response=dict(response),
        )
