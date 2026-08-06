"""Public-interface client for Identity and Trust artifact verification."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from koa_interfaces import Correlation, ProtocolError, UnixHttpClient


class IdentityVerificationResult(StrEnum):
    VERIFIED = "verified"
    INVALID = "invalid"
    BLOCKED = "blocked"


class ContentIdentityResult(StrEnum):
    RESOLVED = "resolved"
    UNRESOLVED = "unresolved"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class ArtifactIdentityVerification:
    request_id: str
    correlation_id: str
    artifact_ref: str
    artifact_digest: str
    result: IdentityVerificationResult
    verified_signature_ids: tuple[str, ...]
    rejected_signature_ids: tuple[str, ...]
    reason_codes: tuple[str, ...]
    trust_scope_ref: str | None
    verified_at: datetime
    receipt: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class ContentIdentityResolution:
    request_id: str
    correlation_id: str
    result: ContentIdentityResult
    resolved_identity: str | None
    content_digest: str
    reason_codes: tuple[str, ...]
    resolved_at: datetime
    receipt: Mapping[str, Any]


class IdentityClient:
    """Delegate identity, signature, and trust checks without granting authority."""

    def __init__(
        self, transport: UnixHttpClient, *,
        verify_path: str = "/v1/identity/verify-artifact",
        resolve_path: str = "/v1/identity/resolve-kristal-content",
    ) -> None:
        if not isinstance(transport, UnixHttpClient) and not hasattr(transport, "request"):
            raise TypeError("transport must implement the common request interface")
        self._transport = transport
        self._verify_path = verify_path
        self._resolve_path = resolve_path

    @classmethod
    def from_socket(cls, socket_path: str, *, timeout_seconds: float = 5.0) -> "IdentityClient":
        return cls(UnixHttpClient(socket_path, sender="kristal_runtime", timeout_seconds=timeout_seconds, interface_version="1.0.0"))

    @staticmethod
    def _text(value: Any, field: str, *, optional: bool = False) -> str | None:
        if value is None and optional:
            return None
        if not isinstance(value, str) or not value.strip():
            raise ProtocolError(f"identity response {field} must be a non-empty string")
        return value.strip()

    @classmethod
    def _strings(cls, value: Any, field: str) -> tuple[str, ...]:
        if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
            raise ProtocolError(f"identity response {field} must be an array")
        result = tuple(cls._text(item, field) for item in value)
        if len(result) != len(set(result)):
            raise ProtocolError(f"identity response {field} must not contain duplicates")
        return result  # type: ignore[return-value]

    @classmethod
    def _time(cls, value: Any, field: str) -> datetime:
        raw = cls._text(value, field)
        try:
            parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ProtocolError(f"identity response {field} is invalid") from exc
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            raise ProtocolError(f"identity response {field} must include a timezone")
        return parsed.astimezone(timezone.utc)

    def verify_artifact(
        self, *, request_id: str, correlation: Correlation, artifact_ref: str,
        artifact_digest: str, signatures: Sequence[Mapping[str, Any]], trust_required: bool,
        trust_scope_ref: str | None = None,
    ) -> ArtifactIdentityVerification:
        if not isinstance(trust_required, bool):
            raise ValueError("trust_required must be boolean")
        body = {
            "request_id": request_id, "correlation_id": correlation.correlation_id,
            "artifact_ref": artifact_ref, "artifact_digest": artifact_digest,
            "signatures": [dict(item) for item in signatures], "trust_required": trust_required,
            "trust_scope_ref": trust_scope_ref,
        }
        response = self._transport.request("POST", self._verify_path, body=body, correlation=correlation, idempotency_key=request_id, expected_status=(200,))
        if not isinstance(response, Mapping):
            raise ProtocolError("identity verification response must be an object")
        for field, expected in {"request_id": request_id, "correlation_id": correlation.correlation_id, "artifact_ref": artifact_ref, "artifact_digest": artifact_digest}.items():
            if response.get(field) != expected:
                raise ProtocolError(f"identity verification {field} mismatch")
        try:
            result = IdentityVerificationResult(response.get("result"))
        except ValueError as exc:
            raise ProtocolError("identity verification result is unknown") from exc
        verified = self._strings(response.get("verified_signature_ids", []), "verified_signature_ids")
        rejected = self._strings(response.get("rejected_signature_ids", []), "rejected_signature_ids")
        reasons = self._strings(response.get("reason_codes", []), "reason_codes")
        if set(verified) & set(rejected):
            raise ProtocolError("a signature cannot be both verified and rejected")
        if result is IdentityVerificationResult.INVALID and not reasons:
            raise ProtocolError("invalid identity verification requires reason_codes")
        if result is IdentityVerificationResult.BLOCKED and not reasons:
            raise ProtocolError("blocked identity verification requires reason_codes")
        if result is IdentityVerificationResult.VERIFIED and trust_required and not verified:
            raise ProtocolError("trusted verification requires at least one verified signature")
        receipt = response.get("receipt")
        if not isinstance(receipt, Mapping) or receipt.get("request_id") != request_id or receipt.get("correlation_id") != correlation.correlation_id:
            raise ProtocolError("identity verification receipt correlation mismatch")
        return ArtifactIdentityVerification(
            request_id, correlation.correlation_id, artifact_ref, artifact_digest, result,
            verified, rejected, reasons, self._text(response.get("trust_scope_ref"), "trust_scope_ref", optional=True),
            self._time(response.get("verified_at"), "verified_at"), MappingProxyType(dict(receipt)),
        )

    def resolve_content_identity(
        self, *, request_id: str, correlation: Correlation, content_digest: str,
        canonical_content_reference: str | None = None, claimed_identity: str | None = None,
    ) -> ContentIdentityResolution:
        body = {
            "request_id": request_id, "correlation_id": correlation.correlation_id,
            "content_digest": content_digest, "canonical_content_reference": canonical_content_reference,
            "claimed_identity": claimed_identity,
        }
        response = self._transport.request("POST", self._resolve_path, body=body, correlation=correlation, idempotency_key=request_id, expected_status=(200,))
        if not isinstance(response, Mapping):
            raise ProtocolError("content identity response must be an object")
        for field, expected in {"request_id": request_id, "correlation_id": correlation.correlation_id, "content_digest": content_digest}.items():
            if response.get(field) != expected:
                raise ProtocolError(f"content identity {field} mismatch")
        try:
            result = ContentIdentityResult(response.get("result"))
        except ValueError as exc:
            raise ProtocolError("content identity result is unknown") from exc
        resolved = self._text(response.get("resolved_identity"), "resolved_identity", optional=True)
        reasons = self._strings(response.get("reason_codes", []), "reason_codes")
        if result is ContentIdentityResult.RESOLVED and resolved is None:
            raise ProtocolError("resolved content identity requires resolved_identity")
        if result is not ContentIdentityResult.RESOLVED and not reasons:
            raise ProtocolError("unresolved or blocked content identity requires reason_codes")
        receipt = response.get("receipt")
        if not isinstance(receipt, Mapping) or receipt.get("request_id") != request_id or receipt.get("correlation_id") != correlation.correlation_id:
            raise ProtocolError("content identity receipt correlation mismatch")
        return ContentIdentityResolution(
            request_id, correlation.correlation_id, result, resolved, content_digest, reasons,
            self._time(response.get("resolved_at"), "resolved_at"), MappingProxyType(dict(receipt)),
        )
