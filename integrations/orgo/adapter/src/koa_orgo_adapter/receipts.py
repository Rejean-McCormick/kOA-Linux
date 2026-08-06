"""Deterministic adapter receipts for Orgo boundary attempts."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
from types import MappingProxyType
from typing import Any, Callable, Mapping, Protocol

from .client import ClientResult


class ReceiptSink(Protocol):
    def record(self, receipt: "IntegrationReceipt") -> None:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class IntegrationReceipt:
    receipt_id: str
    receipt_schema_version: str
    receipt_class: str
    transition_type: str
    producer_component_id: str
    request_id: str
    correlation_id: str
    actor_ref: str
    authority_domain: str
    operation_id: str
    capability_id: str
    decision: str
    execution_state: str
    commit_state: str
    outcome: str
    reason_code: str
    recorded_at: str
    remote_reference: str | None
    evidence: Mapping[str, Any]
    disclosure_class: str = "operator_restricted"
    retention_class: str = "integration_evidence"

    def __post_init__(self) -> None:
        object.__setattr__(self, "evidence", MappingProxyType(dict(self.evidence)))

    def as_mapping(self) -> Mapping[str, Any]:
        data = asdict(self)
        data["evidence"] = dict(self.evidence)
        return MappingProxyType(data)


class ReceiptFactory:
    def __init__(self, *, now: Callable[[], datetime] | None = None) -> None:
        self._now = now or (lambda: datetime.now(timezone.utc))

    def from_result(
        self,
        *,
        result: ClientResult,
        request_id: str,
        actor_ref: str,
        authority_domain: str,
        capability_id: str,
        operation_digest: str,
    ) -> IntegrationReceipt:
        for field, value in {
            "request_id": request_id,
            "correlation_id": result.correlation_id,
            "actor_ref": actor_ref,
            "authority_domain": authority_domain,
            "capability_id": capability_id,
            "operation_digest": operation_digest,
        }.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field} is required for an integration receipt")
        recorded_at = self._now().astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
        decision, execution_state, commit_state, outcome = _states(result)
        receipt_basis = {
            "producer_component_id": "orgo-integration-adapter",
            "request_id": request_id,
            "correlation_id": result.correlation_id,
            "operation_id": result.operation_id,
            "outcome": outcome,
            "reason_code": result.reason_code,
            "recorded_at": recorded_at,
            "remote_reference": result.remote_reference,
            "operation_digest": operation_digest,
        }
        receipt_id = "orgo-receipt-" + sha256(_canonical_json(receipt_basis).encode()).hexdigest()
        return IntegrationReceipt(
            receipt_id=receipt_id,
            receipt_schema_version="1.0.0",
            receipt_class="transition_receipt",
            transition_type="external_subsystem_operation",
            producer_component_id="orgo-integration-adapter",
            request_id=request_id,
            correlation_id=result.correlation_id,
            actor_ref=actor_ref,
            authority_domain=authority_domain,
            operation_id=result.operation_id,
            capability_id=capability_id,
            decision=decision,
            execution_state=execution_state,
            commit_state=commit_state,
            outcome=outcome,
            reason_code=result.reason_code,
            recorded_at=recorded_at,
            remote_reference=result.remote_reference,
            evidence={
                "operation_digest": operation_digest,
                "failure_class": result.failure_class.value if result.failure_class else None,
                "retryable": result.retryable,
                "external_acknowledgement_is_local_acceptance": False,
            },
        )


def persist_receipt(sink: ReceiptSink, receipt: IntegrationReceipt) -> None:
    try:
        sink.record(receipt)
    except Exception as exc:
        raise RuntimeError("orgo_receipt_persistence_failed") from exc


def operation_digest(*, operation_id: str, payload: Mapping[str, Any], identity_context: Mapping[str, Any]) -> str:
    safe_identity = {
        "actor_id": identity_context.get("actor_id"),
        "authority_domain": identity_context.get("authority_domain"),
        "tenant_id": identity_context.get("tenant_id"),
    }
    basis = {"operation_id": operation_id, "payload": dict(payload), "identity": safe_identity}
    return "sha256:" + sha256(_canonical_json(basis).encode()).hexdigest()


def _canonical_json(value: Mapping[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)


def _states(result: ClientResult) -> tuple[str, str, str, str]:
    if result.state.value == "succeeded":
        return "authorized", "completed", "external_acknowledged", "committed"
    if result.state.value == "rejected":
        return "denied", "not_executed", "not_committed", "denied"
    if result.state.value == "unavailable":
        return "indeterminate", "not_executed", "not_committed", "failed"
    return "indeterminate", "unknown_remote_state", "not_committed", "indeterminate"
