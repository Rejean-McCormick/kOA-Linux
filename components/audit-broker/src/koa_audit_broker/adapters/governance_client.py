"""Public-interface client for Governance Policy Runtime decisions."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from koa_interfaces import Correlation, ProtocolError, UnixHttpClient


class PolicyDecisionResult(StrEnum):
    ALLOW = "allow"
    DENY = "deny"
    BLOCKED = "blocked"


class DecisionClass(StrEnum):
    AUTHORIZATION = "authorization"
    DISCLOSURE = "disclosure"
    CONSENT = "consent"
    PRIVILEGE = "privilege"
    EXCEPTION = "exception"


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    request_id: str
    correlation_id: str
    decision_class: DecisionClass
    result: PolicyDecisionResult
    policy_set_ref: str
    authority_version: str
    evaluated_at: datetime
    evaluator_identity: Mapping[str, Any]
    obligations: tuple[Mapping[str, Any], ...]
    diagnostics: tuple[Mapping[str, Any], ...]
    receipt: Mapping[str, Any]

    @property
    def allowed(self) -> bool:
        return self.result is PolicyDecisionResult.ALLOW

    @property
    def authoritative_denial(self) -> bool:
        return self.result is PolicyDecisionResult.DENY

    @property
    def blocked(self) -> bool:
        return self.result is PolicyDecisionResult.BLOCKED


class GovernanceClient:
    """Evaluates exact governed requests without broadening returned authority."""

    def __init__(
        self,
        transport: UnixHttpClient,
        *,
        evaluate_path: str = "/v1/governance/evaluate-decision",
    ) -> None:
        if not isinstance(transport, UnixHttpClient) and not hasattr(transport, "request"):
            raise TypeError("transport must implement the common UnixHttpClient request interface")
        self._transport = transport
        self._evaluate_path = evaluate_path

    @classmethod
    def from_socket(cls, socket_path: str, *, timeout_seconds: float = 5.0) -> "GovernanceClient":
        return cls(
            UnixHttpClient(
                socket_path,
                sender="audit_broker",
                timeout_seconds=timeout_seconds,
                interface_version="1.0.0",
            )
        )

    @staticmethod
    def _text(value: Any, field: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ProtocolError(f"policy response {field} must be a non-empty string")
        return value.strip()

    @staticmethod
    def _mapping(value: Any, field: str) -> Mapping[str, Any]:
        if not isinstance(value, Mapping):
            raise ProtocolError(f"policy response {field} must be an object")
        return MappingProxyType(dict(value))

    @classmethod
    def _mapping_sequence(cls, value: Any, field: str) -> tuple[Mapping[str, Any], ...]:
        if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
            raise ProtocolError(f"policy response {field} must be an array")
        return tuple(cls._mapping(item, field) for item in value)

    def _parse(
        self,
        response: Mapping[str, Any],
        *,
        request_id: str,
        correlation_id: str,
        decision_class: DecisionClass,
        expected_authority_version: str | None,
    ) -> PolicyDecision:
        if response.get("request_id") != request_id:
            raise ProtocolError("policy response request_id mismatch")
        if response.get("correlation_id") != correlation_id:
            raise ProtocolError("policy response correlation_id mismatch")
        try:
            returned_class = DecisionClass(response.get("decision_class"))
            result = PolicyDecisionResult(response.get("result"))
        except ValueError as exc:
            raise ProtocolError("policy response contains an unknown decision class or result") from exc
        if returned_class is not decision_class:
            raise ProtocolError("policy response decision_class mismatch")
        authority_version = self._text(response.get("authority_version"), "authority_version")
        if expected_authority_version is not None and authority_version != expected_authority_version:
            raise ProtocolError("policy response authority_version mismatch")
        evaluated_raw = response.get("evaluated_at")
        if not isinstance(evaluated_raw, str):
            raise ProtocolError("policy response evaluated_at must be a timestamp")
        try:
            evaluated_at = datetime.fromisoformat(evaluated_raw.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ProtocolError("policy response evaluated_at is invalid") from exc
        if evaluated_at.tzinfo is None or evaluated_at.utcoffset() is None:
            raise ProtocolError("policy response evaluated_at must include a timezone")
        receipt = self._mapping(response.get("receipt"), "receipt")
        if receipt.get("request_id") != request_id or receipt.get("correlation_id") != correlation_id:
            raise ProtocolError("policy decision receipt correlation mismatch")
        return PolicyDecision(
            request_id=request_id,
            correlation_id=correlation_id,
            decision_class=returned_class,
            result=result,
            policy_set_ref=self._text(response.get("policy_set_ref"), "policy_set_ref"),
            authority_version=authority_version,
            evaluated_at=evaluated_at.astimezone(timezone.utc),
            evaluator_identity=self._mapping(response.get("evaluator_identity"), "evaluator_identity"),
            obligations=self._mapping_sequence(response.get("obligations", []), "obligations"),
            diagnostics=self._mapping_sequence(response.get("diagnostics", []), "diagnostics"),
            receipt=receipt,
        )

    def evaluate_decision(
        self,
        *,
        request_id: str,
        correlation: Correlation,
        decision_class: DecisionClass | str,
        requester: Mapping[str, Any],
        action: str,
        target: Mapping[str, Any],
        scope: Mapping[str, Any],
        policy_set_ref: str,
        authority_version: str,
        evaluation_context: Mapping[str, Any],
        exception_ids: Sequence[str] = (),
        prior_receipt_refs: Sequence[str] = (),
        requested_at: datetime | None = None,
    ) -> PolicyDecision:
        selected = DecisionClass(decision_class)
        body = {
            "request_id": request_id,
            "correlation_id": correlation.correlation_id,
            "decision_class": selected.value,
            "requester": dict(requester),
            "action": action,
            "target": dict(target),
            "scope": dict(scope),
            "policy_set_ref": policy_set_ref,
            "authority_version": authority_version,
            "evaluation_context": dict(evaluation_context),
            "exception_ids": list(exception_ids),
            "prior_receipt_refs": list(prior_receipt_refs),
        }
        if requested_at is not None:
            if requested_at.tzinfo is None or requested_at.utcoffset() is None:
                raise ValueError("requested_at must include a timezone")
            body["requested_at"] = requested_at.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
        response = self._transport.request(
            "POST", self._evaluate_path, body=body, correlation=correlation,
            idempotency_key=request_id, expected_status=(200,),
        )
        if response is None:
            raise ProtocolError("policy evaluation response cannot be empty")
        return self._parse(
            response, request_id=request_id, correlation_id=correlation.correlation_id,
            decision_class=selected, expected_authority_version=authority_version,
        )

    def evaluate_disclosure(self, **kwargs: Any) -> PolicyDecision:
        kwargs["decision_class"] = DecisionClass.DISCLOSURE
        kwargs.setdefault("action", "audit_broker.request_audit_disclosure")
        kwargs.setdefault("target", {"component_id": "audit_broker"})
        return self.evaluate_decision(**kwargs)

    def evaluate_retention_action(self, **kwargs: Any) -> PolicyDecision:
        kwargs["decision_class"] = DecisionClass.AUTHORIZATION
        kwargs.setdefault("action", "audit_broker.apply_retention_action")
        kwargs.setdefault("target", {"component_id": "audit_broker"})
        return self.evaluate_decision(**kwargs)
