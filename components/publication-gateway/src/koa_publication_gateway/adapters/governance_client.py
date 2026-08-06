"""Governance Policy Runtime adapter for publication decisions."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from koa_interfaces import Correlation, ProtocolError, UnixHttpClient


class PublicationDecision(StrEnum):
    ALLOW = "allow"
    DENY = "deny"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"


@dataclass(frozen=True, slots=True)
class PolicyEvaluation:
    request_id: str
    correlation_id: str
    decision: PublicationDecision
    policy_set_ref: str
    decision_ref: str
    obligations: tuple[Mapping[str, Any], ...]
    reason_codes: tuple[str, ...]
    expires_at: datetime | None
    receipt: Mapping[str, Any]

    @property
    def executable(self) -> bool:
        return self.decision is PublicationDecision.ALLOW


class GovernanceClient:
    """Evaluate a minimum publication context through the public policy API."""

    def __init__(
        self,
        transport: UnixHttpClient,
        *,
        evaluate_path: str = "/v1/policy/evaluate/publication",
        max_payload_bytes: int = 512 * 1024,
    ) -> None:
        if not isinstance(transport, UnixHttpClient) and not hasattr(transport, "request"):
            raise TypeError("transport must implement the common request interface")
        if max_payload_bytes <= 0:
            raise ValueError("max_payload_bytes must be positive")
        self._transport = transport
        self._evaluate_path = evaluate_path
        self._max_payload_bytes = max_payload_bytes

    @classmethod
    def from_socket(cls, socket_path: str, *, timeout_seconds: float = 5.0) -> "GovernanceClient":
        return cls(
            UnixHttpClient(
                socket_path,
                sender="publication_gateway",
                timeout_seconds=timeout_seconds,
                interface_version="1.0.0",
            )
        )

    @staticmethod
    def _text(value: Any, field: str, *, optional: bool = False) -> str | None:
        if value is None and optional:
            return None
        if not isinstance(value, str) or not value.strip():
            raise ProtocolError(f"policy response {field} must be a non-empty string")
        return value.strip()

    @staticmethod
    def _reason_codes(value: Any) -> tuple[str, ...]:
        if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
            raise ProtocolError("policy response reason_codes must be an array")
        result: list[str] = []
        for item in value:
            if not isinstance(item, str) or not item.strip():
                raise ProtocolError("policy response reason_codes must contain strings")
            result.append(item.strip())
        if len(result) != len(set(result)):
            raise ProtocolError("policy response reason_codes must be unique")
        return tuple(result)

    @staticmethod
    def _time(value: Any, field: str) -> datetime | None:
        if value is None:
            return None
        if not isinstance(value, str):
            raise ProtocolError(f"policy response {field} must be a timestamp")
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ProtocolError(f"policy response {field} is invalid") from exc
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            raise ProtocolError(f"policy response {field} must include timezone")
        return parsed.astimezone(timezone.utc)

    def evaluate_publication(
        self,
        *,
        request_id: str,
        correlation: Correlation,
        idempotency_key: str,
        identity_context: Mapping[str, Any],
        source_context: Mapping[str, Any],
        publication_intent: Mapping[str, Any],
        destination: Mapping[str, Any],
        classification: Mapping[str, Any],
        transformation_plan: Mapping[str, Any],
        approval_context: Mapping[str, Any],
        authority_references: Sequence[str],
        evaluated_at: datetime,
    ) -> PolicyEvaluation:
        if not isinstance(evaluated_at, datetime) or evaluated_at.tzinfo is None:
            raise ValueError("evaluated_at must be timezone-aware")
        body = {
            "request_id": request_id,
            "correlation_id": correlation.correlation_id,
            "action": "cross_domain_publication",
            "identity_context": dict(identity_context),
            "source_context": dict(source_context),
            "publication_intent": dict(publication_intent),
            "destination": dict(destination),
            "classification": dict(classification),
            "transformation_plan": dict(transformation_plan),
            "approval_context": dict(approval_context),
            "authority_references": list(authority_references),
            "evaluated_at": evaluated_at.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
            "resource_state_used_as_authority": False,
        }
        try:
            encoded = json.dumps(
                body,
                ensure_ascii=False,
                allow_nan=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
        except (TypeError, ValueError) as exc:
            raise ValueError("policy context must contain JSON-compatible values") from exc
        if len(encoded) > self._max_payload_bytes:
            raise ValueError("policy context exceeds the configured size limit")
        response = self._transport.request(
            "POST",
            self._evaluate_path,
            body=body,
            correlation=correlation,
            idempotency_key=idempotency_key,
            expected_status=(200,),
        )
        if not isinstance(response, Mapping):
            raise ProtocolError("policy evaluation response must be an object")
        if response.get("request_id") != request_id:
            raise ProtocolError("policy evaluation request identity mismatch")
        if response.get("correlation_id") != correlation.correlation_id:
            raise ProtocolError("policy evaluation correlation mismatch")
        try:
            decision = PublicationDecision(response.get("decision"))
        except (TypeError, ValueError) as exc:
            raise ProtocolError("policy evaluation decision is unknown") from exc
        policy_set_ref = self._text(response.get("policy_set_ref"), "policy_set_ref")
        decision_ref = self._text(response.get("decision_ref"), "decision_ref")
        obligations_value = response.get("obligations", [])
        if not isinstance(obligations_value, Sequence) or isinstance(
            obligations_value, (str, bytes, bytearray)
        ):
            raise ProtocolError("policy evaluation obligations must be an array")
        obligations: list[Mapping[str, Any]] = []
        for obligation in obligations_value:
            if not isinstance(obligation, Mapping):
                raise ProtocolError("policy evaluation obligation must be an object")
            obligations.append(MappingProxyType(dict(obligation)))
        reason_codes = self._reason_codes(response.get("reason_codes", []))
        if decision is PublicationDecision.ALLOW and not obligations:
            raise ProtocolError("allow decision requires explicit obligations")
        if decision is not PublicationDecision.ALLOW and not reason_codes:
            raise ProtocolError("non-allow decision requires reason_codes")
        receipt = response.get("receipt")
        if not isinstance(receipt, Mapping):
            raise ProtocolError("policy evaluation receipt must be an object")
        if receipt.get("request_id") != request_id or receipt.get("correlation_id") != correlation.correlation_id:
            raise ProtocolError("policy evaluation receipt correlation mismatch")
        if receipt.get("decision") != decision.value:
            raise ProtocolError("policy evaluation receipt decision mismatch")
        return PolicyEvaluation(
            request_id=request_id,
            correlation_id=correlation.correlation_id,
            decision=decision,
            policy_set_ref=policy_set_ref or "",
            decision_ref=decision_ref or "",
            obligations=tuple(obligations),
            reason_codes=reason_codes,
            expires_at=self._time(response.get("expires_at"), "expires_at"),
            receipt=MappingProxyType(dict(receipt)),
        )
