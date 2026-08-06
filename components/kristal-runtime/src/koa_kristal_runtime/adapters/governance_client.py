"""Public-interface client for governed Kristal Runtime transitions."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from koa_interfaces import Correlation, ProtocolError, UnixHttpClient


class GovernanceDecision(StrEnum):
    ALLOW = "allow"
    DENY = "deny"
    BLOCKED = "blocked"


class GovernedAction(StrEnum):
    ACTIVATE = "runtime_pack_activation"
    ROLLBACK = "runtime_pack_rollback"
    REVOKE = "runtime_pack_revocation"
    RESTRICTED_STATUS = "restricted_status_query"


@dataclass(frozen=True, slots=True)
class PolicyEvaluation:
    request_id: str
    correlation_id: str
    action: GovernedAction
    decision: GovernanceDecision
    authorization_ref: str | None
    policy_set_ref: str
    reason_codes: tuple[str, ...]
    obligations: tuple[Mapping[str, Any], ...]
    expires_at: datetime | None
    decided_at: datetime
    receipt: Mapping[str, Any]

    @property
    def allowed(self) -> bool:
        return self.decision is GovernanceDecision.ALLOW


class GovernanceClient:
    """Request operation-bound policy decisions; never infer permission from transport."""

    def __init__(self, transport: UnixHttpClient, *, evaluate_path: str = "/v1/governance/evaluate") -> None:
        if not isinstance(transport, UnixHttpClient) and not hasattr(transport, "request"):
            raise TypeError("transport must implement the common request interface")
        self._transport = transport
        self._evaluate_path = evaluate_path

    @classmethod
    def from_socket(cls, socket_path: str, *, timeout_seconds: float = 5.0) -> "GovernanceClient":
        return cls(UnixHttpClient(socket_path, sender="kristal_runtime", timeout_seconds=timeout_seconds, interface_version="1.0.0"))

    @staticmethod
    def _text(value: Any, field: str, *, optional: bool = False) -> str | None:
        if value is None and optional:
            return None
        if not isinstance(value, str) or not value.strip():
            raise ProtocolError(f"policy response {field} must be a non-empty string")
        return value.strip()

    @classmethod
    def _strings(cls, value: Any, field: str) -> tuple[str, ...]:
        if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
            raise ProtocolError(f"policy response {field} must be an array")
        result = tuple(cls._text(item, field) for item in value)
        if len(result) != len(set(result)):
            raise ProtocolError(f"policy response {field} must not contain duplicates")
        return result  # type: ignore[return-value]

    @staticmethod
    def _time(value: Any, field: str, *, optional: bool = False) -> datetime | None:
        if value is None and optional:
            return None
        if not isinstance(value, str) or not value.strip():
            raise ProtocolError(f"policy response {field} must be a timestamp")
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ProtocolError(f"policy response {field} is invalid") from exc
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            raise ProtocolError(f"policy response {field} must include a timezone")
        return parsed.astimezone(timezone.utc)

    def evaluate(
        self, *, request_id: str, correlation: Correlation, action: GovernedAction,
        actor: Mapping[str, Any], candidate_artifact_ref: str | None,
        current_artifact_ref: str | None, artifact_digest: str | None,
        verification_receipt_ref: str | None, resource_grant_ref: str | None,
        context: Mapping[str, Any],
    ) -> PolicyEvaluation:
        body = {
            "request_id": request_id, "correlation_id": correlation.correlation_id,
            "component_id": "kristal_runtime", "action": GovernedAction(action).value,
            "actor": dict(actor), "candidate_artifact_ref": candidate_artifact_ref,
            "current_artifact_ref": current_artifact_ref, "artifact_digest": artifact_digest,
            "verification_receipt_ref": verification_receipt_ref,
            "resource_grant_ref": resource_grant_ref, "context": dict(context),
        }
        response = self._transport.request("POST", self._evaluate_path, body=body, correlation=correlation, idempotency_key=request_id, expected_status=(200,))
        if not isinstance(response, Mapping):
            raise ProtocolError("policy evaluation response must be an object")
        for field, expected in {"request_id": request_id, "correlation_id": correlation.correlation_id, "action": body["action"]}.items():
            if response.get(field) != expected:
                raise ProtocolError(f"policy evaluation {field} mismatch")
        try:
            decision = GovernanceDecision(response.get("decision"))
        except ValueError as exc:
            raise ProtocolError("policy decision is unknown") from exc
        authorization_ref = self._text(response.get("authorization_ref"), "authorization_ref", optional=True)
        reasons = self._strings(response.get("reason_codes", []), "reason_codes")
        if decision is GovernanceDecision.ALLOW and authorization_ref is None:
            raise ProtocolError("allowed policy evaluation requires authorization_ref")
        if decision is not GovernanceDecision.ALLOW and not reasons:
            raise ProtocolError("deny or blocked policy decision requires reason_codes")
        obligations_raw = response.get("obligations", [])
        if not isinstance(obligations_raw, Sequence) or isinstance(obligations_raw, (str, bytes, bytearray)):
            raise ProtocolError("policy obligations must be an array")
        obligations = []
        for item in obligations_raw:
            if not isinstance(item, Mapping):
                raise ProtocolError("policy obligations must contain objects")
            obligations.append(MappingProxyType(dict(item)))
        receipt = response.get("receipt")
        if not isinstance(receipt, Mapping) or receipt.get("request_id") != request_id or receipt.get("correlation_id") != correlation.correlation_id:
            raise ProtocolError("policy evaluation receipt correlation mismatch")
        return PolicyEvaluation(
            request_id, correlation.correlation_id, GovernedAction(action), decision,
            authorization_ref, self._text(response.get("policy_set_ref"), "policy_set_ref"), reasons,
            tuple(obligations), self._time(response.get("expires_at"), "expires_at", optional=True),
            self._time(response.get("decided_at"), "decided_at"), MappingProxyType(dict(receipt)),
        )  # type: ignore[arg-type]
