"""Opaque task-query forwarding without ownership of Orgo task semantics."""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from .client import ClientResult, ClientState, FailureClass, OperationMode, OrgoClient
from .receipts import ReceiptFactory, ReceiptSink, operation_digest, persist_receipt


@dataclass(frozen=True, slots=True)
class TaskQueryOutcome:
    state: ClientState
    records: tuple[Mapping[str, Any], ...]
    reason_code: str
    receipt_id: str
    remote_reference: str | None


class TaskQueryService:
    def __init__(self, *, client: OrgoClient, receipts: ReceiptSink, receipt_factory: ReceiptFactory) -> None:
        self._client = client
        self._receipts = receipts
        self._receipt_factory = receipt_factory

    def query(
        self,
        *,
        operation_id: str,
        criteria: Mapping[str, Any],
        identity_context: Mapping[str, Any],
        request_id: str,
        correlation_id: str,
    ) -> TaskQueryOutcome:
        result = self._client.invoke(
            operation_id=operation_id,
            expected_mode=OperationMode.QUERY,
            payload=criteria,
            identity_context=identity_context,
            correlation_id=correlation_id,
        )
        if result.state is ClientState.SUCCEEDED:
            try:
                records = _records(result)
            except ValueError:
                result = ClientResult(
                    state=ClientState.UNAVAILABLE,
                    operation_id=operation_id,
                    correlation_id=correlation_id,
                    payload={},
                    reason_code="orgo_response_contract_invalid",
                    failure_class=FailureClass.COMPATIBILITY,
                )
                records = ()
        else:
            records = ()
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
                payload=criteria,
                identity_context=identity_context,
            ),
        )
        persist_receipt(self._receipts, receipt)
        return TaskQueryOutcome(
            state=result.state,
            records=records,
            reason_code=result.reason_code,
            receipt_id=receipt.receipt_id,
            remote_reference=result.remote_reference,
        )


def _records(result: ClientResult) -> tuple[Mapping[str, Any], ...]:
    raw = result.payload.get("records", [])
    if not isinstance(raw, list):
        raise ValueError("orgo task response records must be a list")
    records: list[Mapping[str, Any]] = []
    for item in raw:
        if not isinstance(item, Mapping):
            raise ValueError("orgo task record must be an object")
        records.append(MappingProxyType(dict(item)))
    return tuple(records)
