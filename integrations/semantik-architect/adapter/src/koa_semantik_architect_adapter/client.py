"""Transport-neutral SemantiK Architect client boundary."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping, Protocol, runtime_checkable


class SemantikClientError(RuntimeError):
    reason_code = "external_protocol_failure"
    public_message = "the SemantiK Architect operation failed"


class ExternalUnavailable(SemantikClientError):
    reason_code = "external_unavailable"
    public_message = "SemantiK Architect is unavailable"


class ExternalRejected(SemantikClientError):
    reason_code = "external_rejected"
    public_message = "SemantiK Architect rejected the request"


class ExternalIndeterminate(SemantikClientError):
    reason_code = "external_indeterminate"
    public_message = "the external operation outcome is indeterminate"


class ExternalProtocolError(SemantikClientError):
    reason_code = "external_protocol_invalid"
    public_message = "SemantiK Architect returned an invalid response"


@runtime_checkable
class Transport(Protocol):
    """Minimal transport supplied by the deployment-specific B-0067 boundary."""

    def request(
        self,
        operation: str,
        payload: Mapping[str, object],
        *,
        request_id: str,
        correlation_id: str,
        idempotency_key: str | None = None,
    ) -> Mapping[str, object]: ...


@dataclass(frozen=True, slots=True)
class ExternalResponse:
    operation: str
    request_id: str
    correlation_id: str
    outcome: str
    payload: Mapping[str, object]
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.outcome not in {"accepted", "succeeded", "rejected", "failed", "cancelled", "indeterminate"}:
            raise ExternalProtocolError("unregistered external outcome")
        object.__setattr__(self, "payload", MappingProxyType(dict(self.payload)))
        object.__setattr__(self, "evidence_refs", tuple(self.evidence_refs))


class SemantikArchitectClient:
    """Validates correlation and terminal semantics without assuming HTTP or internals."""

    def __init__(self, transport: Transport) -> None:
        if not isinstance(transport, Transport):
            raise TypeError("transport must implement the public Transport protocol")
        self._transport = transport

    def invoke(
        self,
        operation: str,
        payload: Mapping[str, object],
        *,
        request_id: str,
        correlation_id: str,
        idempotency_key: str | None = None,
    ) -> ExternalResponse:
        try:
            raw = self._transport.request(
                operation,
                MappingProxyType(dict(payload)),
                request_id=request_id,
                correlation_id=correlation_id,
                idempotency_key=idempotency_key,
            )
        except SemantikClientError:
            raise
        except (ConnectionError, TimeoutError, OSError) as exc:
            raise ExternalUnavailable() from exc
        except Exception as exc:
            raise ExternalProtocolError() from exc
        if not isinstance(raw, Mapping):
            raise ExternalProtocolError("response must be an object")
        response = self._parse(operation, raw)
        if response.request_id != request_id or response.correlation_id != correlation_id:
            raise ExternalProtocolError("response correlation mismatch")
        if response.outcome == "rejected":
            raise ExternalRejected()
        if response.outcome == "indeterminate":
            raise ExternalIndeterminate()
        return response

    def health(self, *, request_id: str, correlation_id: str) -> ExternalResponse:
        return self.invoke("health", {}, request_id=request_id, correlation_id=correlation_id)

    def capabilities(self, *, request_id: str, correlation_id: str) -> ExternalResponse:
        return self.invoke("capabilities", {}, request_id=request_id, correlation_id=correlation_id)

    def submit_compiler_job(
        self,
        payload: Mapping[str, object],
        *,
        request_id: str,
        correlation_id: str,
        idempotency_key: str,
    ) -> ExternalResponse:
        return self.invoke(
            "compiler_job.submit",
            payload,
            request_id=request_id,
            correlation_id=correlation_id,
            idempotency_key=idempotency_key,
        )

    def compiler_job_status(
        self, job_ref: str, *, request_id: str, correlation_id: str
    ) -> ExternalResponse:
        return self.invoke(
            "compiler_job.status",
            {"job_ref": job_ref},
            request_id=request_id,
            correlation_id=correlation_id,
        )

    def cancel_compiler_job(
        self,
        job_ref: str,
        *,
        request_id: str,
        correlation_id: str,
        idempotency_key: str,
    ) -> ExternalResponse:
        return self.invoke(
            "compiler_job.cancel",
            {"job_ref": job_ref},
            request_id=request_id,
            correlation_id=correlation_id,
            idempotency_key=idempotency_key,
        )

    def fetch_artifact(
        self, artifact_ref: str, *, request_id: str, correlation_id: str
    ) -> ExternalResponse:
        return self.invoke(
            "artifact.fetch",
            {"artifact_ref": artifact_ref},
            request_id=request_id,
            correlation_id=correlation_id,
        )

    @staticmethod
    def _parse(operation: str, raw: Mapping[str, object]) -> ExternalResponse:
        required = ("operation", "request_id", "correlation_id", "outcome", "payload")
        if any(name not in raw for name in required):
            raise ExternalProtocolError("response is missing required fields")
        if raw["operation"] != operation:
            raise ExternalProtocolError("response operation mismatch")
        if not all(isinstance(raw[name], str) and raw[name] for name in ("request_id", "correlation_id", "outcome")):
            raise ExternalProtocolError("response identifiers must be strings")
        if not isinstance(raw["payload"], Mapping):
            raise ExternalProtocolError("response payload must be an object")
        evidence = raw.get("evidence_refs", ())
        if not isinstance(evidence, (list, tuple)) or not all(isinstance(item, str) and item for item in evidence):
            raise ExternalProtocolError("evidence_refs must be an array of strings")
        return ExternalResponse(
            operation=operation,
            request_id=str(raw["request_id"]),
            correlation_id=str(raw["correlation_id"]),
            outcome=str(raw["outcome"]),
            payload=raw["payload"],
            evidence_refs=tuple(evidence),
        )
