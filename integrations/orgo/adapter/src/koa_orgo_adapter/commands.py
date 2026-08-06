"""Governed command forwarding to Orgo without internal workflow simulation."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .client import ClientResult, ClientState, FailureClass, OperationMode, OrgoClient
from .receipts import ReceiptFactory, ReceiptSink, operation_digest, persist_receipt


@dataclass(frozen=True, slots=True)
class CommandOutcome:
    state: ClientState
    reason_code: str
    receipt_id: str
    remote_reference: str | None
    retryable: bool


class CommandService:
    def __init__(self, *, client: OrgoClient, receipts: ReceiptSink, receipt_factory: ReceiptFactory) -> None:
        self._client = client
        self._receipts = receipts
        self._receipt_factory = receipt_factory

    def submit(
        self,
        *,
        operation_id: str,
        command: Mapping[str, Any],
        identity_context: Mapping[str, Any],
        policy_decision: Mapping[str, Any],
        resource_admission: Mapping[str, Any],
        request_id: str,
        correlation_id: str,
        idempotency_key: str,
    ) -> CommandOutcome:
        preflight = _preflight(operation_id, correlation_id, policy_decision, resource_admission)
        result = preflight or self._client.invoke(
            operation_id=operation_id,
            expected_mode=OperationMode.COMMAND,
            payload=command,
            identity_context=identity_context,
            correlation_id=correlation_id,
            idempotency_key=idempotency_key,
        )
        declaration = self._client.operations.get(operation_id)
        capability_id = declaration.capability_id if declaration else "undeclared"
        receipt = self._receipt_factory.from_result(
            result=result,
            request_id=request_id,
            actor_ref=str(identity_context.get("actor_id", "unknown")),
            authority_domain=str(identity_context.get("authority_domain", "unknown")),
            capability_id=capability_id,
            operation_digest=operation_digest(
                operation_id=operation_id,
                payload=command,
                identity_context=identity_context,
            ),
        )
        persist_receipt(self._receipts, receipt)
        return CommandOutcome(
            state=result.state,
            reason_code=result.reason_code,
            receipt_id=receipt.receipt_id,
            remote_reference=result.remote_reference,
            retryable=result.retryable,
        )


def _preflight(
    operation_id: str,
    correlation_id: str,
    policy_decision: Mapping[str, Any],
    resource_admission: Mapping[str, Any],
) -> ClientResult | None:
    if policy_decision.get("decision") != "allow" or policy_decision.get("binding") != operation_id:
        return ClientResult(
            state=ClientState.REJECTED,
            operation_id=operation_id,
            correlation_id=correlation_id,
            payload={},
            reason_code="explicit_policy_authorization_required",
            failure_class=FailureClass.AUTHORIZATION,
        )
    if resource_admission.get("admitted") is not True or resource_admission.get("binding") != operation_id:
        return ClientResult(
            state=ClientState.UNAVAILABLE,
            operation_id=operation_id,
            correlation_id=correlation_id,
            payload={},
            reason_code="resource_admission_required",
            failure_class=FailureClass.TRANSIENT,
            retryable=True,
        )
    return None
