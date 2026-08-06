"""Public-interface client for Identity and Trust verification."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping

from koa_interfaces import Correlation, InterfaceValidationError, ProtocolError, UnixHttpClient


class IdentityResult(StrEnum):
    ESTABLISHED = "established"
    NOT_ESTABLISHED = "not_established"
    INDETERMINATE = "indeterminate"


class TrustResult(StrEnum):
    TRUSTED = "trusted"
    UNTRUSTED = "untrusted"
    INDETERMINATE = "indeterminate"


@dataclass(frozen=True, slots=True)
class IdentityVerification:
    request_id: str
    identity_ref: str | None
    identity_result: IdentityResult | None
    trust_result: TrustResult | None
    validated_scope: Mapping[str, Any]
    expires_at: datetime | None
    reason_code: str | None
    verification_ref: str | None
    receipt_ref: str | None

    @property
    def established(self) -> bool:
        return self.identity_result is IdentityResult.ESTABLISHED

    @property
    def trusted(self) -> bool:
        return self.trust_result is TrustResult.TRUSTED

    @property
    def protected_use_allowed(self) -> bool:
        return self.established or self.trusted


class IdentityClient:
    """Consumes only registered Identity and Trust request/response operations."""

    def __init__(
        self,
        transport: UnixHttpClient,
        *,
        validate_credential_path: str = "/v1/identity/validate-credential",
        authenticate_service_path: str = "/v1/identity/authenticate-service",
    ) -> None:
        if not isinstance(transport, UnixHttpClient) and not hasattr(transport, "request"):
            raise TypeError("transport must implement the common UnixHttpClient request interface")
        self._transport = transport
        self._validate_path = validate_credential_path
        self._authenticate_path = authenticate_service_path

    @classmethod
    def from_socket(cls, socket_path: str, *, timeout_seconds: float = 5.0) -> "IdentityClient":
        return cls(
            UnixHttpClient(
                socket_path,
                sender="audit_broker",
                timeout_seconds=timeout_seconds,
                interface_version="1.0.0",
            )
        )

    @staticmethod
    def _text(value: Any, field: str, *, optional: bool = False) -> str | None:
        if value is None and optional:
            return None
        if not isinstance(value, str) or not value.strip():
            raise ProtocolError(f"identity response {field} must be a non-empty string")
        return value.strip()

    @staticmethod
    def _expires(value: Any) -> datetime | None:
        if value is None:
            return None
        if not isinstance(value, str):
            raise ProtocolError("identity response expires_at must be a timestamp string")
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ProtocolError("identity response expires_at is invalid") from exc
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            raise ProtocolError("identity response expires_at must include a timezone")
        return parsed.astimezone(timezone.utc)

    def _parse(self, response: Mapping[str, Any], request_id: str) -> IdentityVerification:
        if response.get("request_id") != request_id:
            raise ProtocolError("identity response request_id mismatch")
        identity_result = response.get("identity_result")
        trust_result = response.get("trust_result")
        if identity_result is None and trust_result is None:
            raise ProtocolError("identity response omitted identity_result and trust_result")
        try:
            parsed_identity = IdentityResult(identity_result) if identity_result is not None else None
            parsed_trust = TrustResult(trust_result) if trust_result is not None else None
        except ValueError as exc:
            raise ProtocolError("identity response contains an unknown result") from exc
        scope = response.get("validated_scope", {})
        if not isinstance(scope, Mapping):
            raise ProtocolError("identity response validated_scope must be an object")
        verification = IdentityVerification(
            request_id=request_id,
            identity_ref=self._text(response.get("identity_ref"), "identity_ref", optional=True),
            identity_result=parsed_identity,
            trust_result=parsed_trust,
            validated_scope=MappingProxyType(dict(scope)),
            expires_at=self._expires(response.get("expires_at")),
            reason_code=self._text(response.get("reason_code"), "reason_code", optional=True),
            verification_ref=self._text(response.get("verification_ref"), "verification_ref", optional=True),
            receipt_ref=self._text(response.get("receipt_ref"), "receipt_ref", optional=True),
        )
        if verification.protected_use_allowed and verification.identity_ref is None:
            raise ProtocolError("successful identity or trust result omitted identity_ref")
        return verification

    def validate_credential(
        self,
        *,
        request_id: str,
        credential: Mapping[str, Any],
        intended_use: str,
        tenant_ref: str,
        environment: str,
        correlation: Correlation,
    ) -> IdentityVerification:
        body = {
            "request_id": request_id,
            "credential": dict(credential),
            "intended_use": intended_use,
            "tenant_ref": tenant_ref,
            "environment": environment,
        }
        response = self._transport.request(
            "POST", self._validate_path, body=body, correlation=correlation,
            idempotency_key=request_id, expected_status=(200,),
        )
        if response is None:
            raise ProtocolError("identity validation response cannot be empty")
        return self._parse(response, request_id)

    verify_producer = validate_credential
    verify_requester = validate_credential

    def authenticate_service(
        self,
        *,
        request_id: str,
        presented_credential: Mapping[str, Any],
        expected_subject_type: str,
        tenant_ref: str,
        environment: str,
        intended_use: str,
        correlation: Correlation,
    ) -> IdentityVerification:
        response = self._transport.request(
            "POST", self._authenticate_path,
            body={
                "request_id": request_id,
                "presented_credential": dict(presented_credential),
                "expected_subject_type": expected_subject_type,
                "tenant_ref": tenant_ref,
                "environment": environment,
                "intended_use": intended_use,
            },
            correlation=correlation, idempotency_key=request_id, expected_status=(200,),
        )
        if response is None:
            raise ProtocolError("service authentication response cannot be empty")
        return self._parse(response, request_id)
