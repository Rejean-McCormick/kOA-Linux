"""Public-interface client for Identity and Trust signature verification."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from koa_interfaces import Correlation, ProtocolError, UnixHttpClient


class SignatureVerificationResult(StrEnum):
    VERIFIED = "verified"
    INVALID = "invalid"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class SignatureVerification:
    request_id: str
    correlation_id: str
    artifact_ref: str
    artifact_digest: str
    result: SignatureVerificationResult
    verified_signature_ids: tuple[str, ...]
    rejected_signature_ids: tuple[str, ...]
    reason_codes: tuple[str, ...]
    signer_assertions: tuple[Mapping[str, Any], ...]
    trust_scope_ref: str
    verified_at: datetime
    receipt: Mapping[str, Any]

    @property
    def verified(self) -> bool:
        return self.result is SignatureVerificationResult.VERIFIED


class IdentitySignatureVerifier:
    """Delegate cryptographic and trust verification without inferring authority."""

    def __init__(
        self,
        transport: UnixHttpClient,
        *,
        verify_path: str = "/v1/identity/verify-artifact-signatures",
    ) -> None:
        if not isinstance(transport, UnixHttpClient) and not hasattr(transport, "request"):
            raise TypeError("transport must implement the common request interface")
        self._transport = transport
        self._verify_path = verify_path

    @classmethod
    def from_socket(
        cls, socket_path: str, *, timeout_seconds: float = 5.0
    ) -> "IdentitySignatureVerifier":
        return cls(
            UnixHttpClient(
                socket_path,
                sender="governance_policy_runtime",
                timeout_seconds=timeout_seconds,
                interface_version="1.0.0",
            )
        )

    @staticmethod
    def _text(value: Any, field: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ProtocolError(f"signature verification {field} must be a non-empty string")
        return value.strip()

    @staticmethod
    def _strings(value: Any, field: str) -> tuple[str, ...]:
        if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
            raise ProtocolError(f"signature verification {field} must be an array")
        result = tuple(IdentitySignatureVerifier._text(item, field) for item in value)
        if len(result) != len(set(result)):
            raise ProtocolError(f"signature verification {field} must not contain duplicates")
        return result

    @staticmethod
    def _mappings(value: Any, field: str) -> tuple[Mapping[str, Any], ...]:
        if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
            raise ProtocolError(f"signature verification {field} must be an array")
        result = []
        for item in value:
            if not isinstance(item, Mapping):
                raise ProtocolError(f"signature verification {field} entries must be objects")
            result.append(MappingProxyType(dict(item)))
        return tuple(result)

    def verify_bundle(
        self,
        *,
        request_id: str,
        correlation: Correlation,
        artifact_ref: str,
        artifact_digest: str,
        signatures: Sequence[Mapping[str, Any]],
        trust_scope_ref: str,
        minimum_signatures: int,
        required_signer_roles: Sequence[str],
        required_purposes: Sequence[str],
    ) -> SignatureVerification:
        if minimum_signatures < 1:
            raise ValueError("minimum_signatures must be positive")
        body = {
            "request_id": request_id,
            "correlation_id": correlation.correlation_id,
            "artifact_ref": artifact_ref,
            "artifact_digest": artifact_digest,
            "signatures": [dict(item) for item in signatures],
            "trust_scope_ref": trust_scope_ref,
            "minimum_signatures": minimum_signatures,
            "required_signer_roles": list(required_signer_roles),
            "required_purposes": list(required_purposes),
        }
        response = self._transport.request(
            "POST",
            self._verify_path,
            body=body,
            correlation=correlation,
            idempotency_key=request_id,
            expected_status=(200,),
        )
        if response is None or not isinstance(response, Mapping):
            raise ProtocolError("signature verification response must be an object")
        for field, expected in {
            "request_id": request_id,
            "correlation_id": correlation.correlation_id,
            "artifact_ref": artifact_ref,
            "artifact_digest": artifact_digest,
            "trust_scope_ref": trust_scope_ref,
        }.items():
            if response.get(field) != expected:
                raise ProtocolError(f"signature verification {field} mismatch")
        try:
            result = SignatureVerificationResult(response.get("result"))
        except ValueError as exc:
            raise ProtocolError("signature verification result is unknown") from exc
        verified_ids = self._strings(response.get("verified_signature_ids", []), "verified_signature_ids")
        rejected_ids = self._strings(response.get("rejected_signature_ids", []), "rejected_signature_ids")
        if set(verified_ids) & set(rejected_ids):
            raise ProtocolError("a signature cannot be both verified and rejected")
        reason_codes = self._strings(response.get("reason_codes", []), "reason_codes")
        if result is SignatureVerificationResult.VERIFIED and len(verified_ids) < minimum_signatures:
            raise ProtocolError("verified result does not satisfy minimum_signatures")
        if result is SignatureVerificationResult.INVALID and not rejected_ids:
            raise ProtocolError("invalid verification requires rejected signatures")
        if result is SignatureVerificationResult.BLOCKED and not reason_codes:
            raise ProtocolError("blocked verification requires an explicit reason code")
        raw_time = self._text(response.get("verified_at"), "verified_at")
        try:
            verified_at = datetime.fromisoformat(raw_time.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ProtocolError("signature verification verified_at is invalid") from exc
        if verified_at.tzinfo is None or verified_at.utcoffset() is None:
            raise ProtocolError("signature verification verified_at must include a timezone")
        receipt = response.get("receipt")
        if not isinstance(receipt, Mapping):
            raise ProtocolError("signature verification receipt must be an object")
        if receipt.get("request_id") != request_id or receipt.get("correlation_id") != correlation.correlation_id:
            raise ProtocolError("signature verification receipt correlation mismatch")
        return SignatureVerification(
            request_id=request_id,
            correlation_id=correlation.correlation_id,
            artifact_ref=artifact_ref,
            artifact_digest=artifact_digest,
            result=result,
            verified_signature_ids=verified_ids,
            rejected_signature_ids=rejected_ids,
            reason_codes=reason_codes,
            signer_assertions=self._mappings(response.get("signer_assertions", []), "signer_assertions"),
            trust_scope_ref=trust_scope_ref,
            verified_at=verified_at.astimezone(timezone.utc),
            receipt=MappingProxyType(dict(receipt)),
        )
