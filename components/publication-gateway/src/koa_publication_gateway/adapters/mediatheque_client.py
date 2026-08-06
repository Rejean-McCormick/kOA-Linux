"""Public-interface client for bounded kOA Mediatheque representations."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from koa_interfaces import Correlation, ProtocolError, UnixHttpClient


class RepresentationStatus(StrEnum):
    READY = "ready"
    BLOCKED = "blocked"
    NOT_FOUND = "not_found"
    VERSION_CONFLICT = "version_conflict"


@dataclass(frozen=True, slots=True)
class BoundedRepresentation:
    request_id: str
    correlation_id: str
    status: RepresentationStatus
    source_object_ref: str
    source_version_ref: str
    representation_ref: str | None
    representation_digest: str | None
    media_type: str | None
    byte_length: int | None
    payload_ref: str | None
    rights_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    reason_codes: tuple[str, ...]
    verified_at: datetime
    receipt: Mapping[str, Any]


class MediathequeClient:
    """Retrieve only an approved bounded representation through a public API."""

    def __init__(
        self,
        transport: UnixHttpClient,
        *,
        representation_path: str = "/v1/publication/representations",
        max_payload_bytes: int = 512 * 1024,
    ) -> None:
        if not isinstance(transport, UnixHttpClient) and not hasattr(transport, "request"):
            raise TypeError("transport must implement the common request interface")
        if max_payload_bytes <= 0:
            raise ValueError("max_payload_bytes must be positive")
        self._transport = transport
        self._representation_path = representation_path
        self._max_payload_bytes = max_payload_bytes

    @classmethod
    def from_socket(cls, socket_path: str, *, timeout_seconds: float = 10.0) -> "MediathequeClient":
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
            raise ProtocolError(f"Mediatheque response {field} must be a non-empty string")
        return value.strip()

    @classmethod
    def _strings(cls, value: Any, field: str) -> tuple[str, ...]:
        if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
            raise ProtocolError(f"Mediatheque response {field} must be an array")
        result = tuple(cls._text(item, field) or "" for item in value)
        if len(result) != len(set(result)):
            raise ProtocolError(f"Mediatheque response {field} must be unique")
        return result

    @staticmethod
    def _time(value: Any) -> datetime:
        if not isinstance(value, str):
            raise ProtocolError("Mediatheque response verified_at must be a timestamp")
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ProtocolError("Mediatheque response verified_at is invalid") from exc
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            raise ProtocolError("Mediatheque response verified_at must include timezone")
        return parsed.astimezone(timezone.utc)

    def get_bounded_representation(
        self,
        *,
        request_id: str,
        correlation: Correlation,
        idempotency_key: str,
        source_object_ref: str,
        source_version_ref: str,
        selection: Mapping[str, Any],
        transformation_plan: Mapping[str, Any],
        destination: Mapping[str, Any],
        approval_refs: Sequence[str],
    ) -> BoundedRepresentation:
        body = {
            "request_id": request_id,
            "correlation_id": correlation.correlation_id,
            "source_object_ref": source_object_ref,
            "source_version_ref": source_version_ref,
            "selection": dict(selection),
            "transformation_plan": dict(transformation_plan),
            "destination": dict(destination),
            "approval_refs": list(approval_refs),
            "minimum_necessary_required": True,
            "source_authority_preserved": True,
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
            raise ValueError("representation request must contain JSON-compatible values") from exc
        if len(encoded) > self._max_payload_bytes:
            raise ValueError("representation request exceeds the configured size limit")
        response = self._transport.request(
            "POST",
            self._representation_path,
            body=body,
            correlation=correlation,
            idempotency_key=idempotency_key,
            expected_status=(200,),
        )
        if not isinstance(response, Mapping):
            raise ProtocolError("Mediatheque representation response must be an object")
        expected = {
            "request_id": request_id,
            "correlation_id": correlation.correlation_id,
            "source_object_ref": source_object_ref,
            "source_version_ref": source_version_ref,
        }
        for field, value in expected.items():
            if response.get(field) != value:
                raise ProtocolError(f"Mediatheque representation {field} mismatch")
        try:
            status = RepresentationStatus(response.get("status"))
        except (TypeError, ValueError) as exc:
            raise ProtocolError("Mediatheque representation status is unknown") from exc
        representation_ref = self._text(response.get("representation_ref"), "representation_ref", optional=True)
        representation_digest = self._text(response.get("representation_digest"), "representation_digest", optional=True)
        media_type = self._text(response.get("media_type"), "media_type", optional=True)
        payload_ref = self._text(response.get("payload_ref"), "payload_ref", optional=True)
        byte_length = response.get("byte_length")
        if byte_length is not None and (
            not isinstance(byte_length, int) or isinstance(byte_length, bool) or byte_length < 0
        ):
            raise ProtocolError("Mediatheque response byte_length must be non-negative")
        reasons = self._strings(response.get("reason_codes", []), "reason_codes")
        if status is RepresentationStatus.READY:
            if not all((representation_ref, representation_digest, media_type, payload_ref)):
                raise ProtocolError("ready representation requires identity, digest, media type and payload_ref")
            if byte_length is None:
                raise ProtocolError("ready representation requires byte_length")
        elif not reasons:
            raise ProtocolError("non-ready representation requires reason_codes")
        receipt = response.get("receipt")
        if not isinstance(receipt, Mapping):
            raise ProtocolError("Mediatheque representation receipt must be an object")
        if receipt.get("request_id") != request_id or receipt.get("correlation_id") != correlation.correlation_id:
            raise ProtocolError("Mediatheque representation receipt correlation mismatch")
        return BoundedRepresentation(
            request_id=request_id,
            correlation_id=correlation.correlation_id,
            status=status,
            source_object_ref=source_object_ref,
            source_version_ref=source_version_ref,
            representation_ref=representation_ref,
            representation_digest=representation_digest,
            media_type=media_type,
            byte_length=byte_length,
            payload_ref=payload_ref,
            rights_refs=self._strings(response.get("rights_refs", []), "rights_refs"),
            provenance_refs=self._strings(response.get("provenance_refs", []), "provenance_refs"),
            reason_codes=reasons,
            verified_at=self._time(response.get("verified_at")),
            receipt=MappingProxyType(dict(receipt)),
        )
