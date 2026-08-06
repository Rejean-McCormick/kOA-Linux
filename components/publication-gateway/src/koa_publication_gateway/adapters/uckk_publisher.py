"""Directional ``publish_to_uckk`` adapter for the UCKK Publication Bridge."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from koa_interfaces import Correlation, ProtocolError, UnixHttpClient


class UckkPublicationOutcome(StrEnum):
    QUEUED = "queued"
    PUBLISHED = "published"
    PARTIALLY_PUBLISHED = "partially_published"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    UNKNOWN_RECONCILIATION_REQUIRED = "unknown_reconciliation_required"


@dataclass(frozen=True, slots=True)
class UckkPublicationResult:
    receipt_id: str
    package_id: str
    attempt_id: str
    idempotency_key: str
    correlation_id: str
    outcome: UckkPublicationOutcome
    occurred_at: datetime
    item_results: tuple[Mapping[str, Any], ...]
    retry: Mapping[str, Any]
    evidence_refs: tuple[str, ...]
    receipt: Mapping[str, Any]

    @property
    def terminal_success(self) -> bool:
        return self.outcome is UckkPublicationOutcome.PUBLISHED

    @property
    def requires_reconciliation(self) -> bool:
        return self.outcome in {
            UckkPublicationOutcome.PARTIALLY_PUBLISHED,
            UckkPublicationOutcome.UNKNOWN_RECONCILIATION_REQUIRED,
        }


class UckkPublisher:
    """Publish or reconcile a declared UCKK package without implicit retry."""

    def __init__(
        self,
        transport: UnixHttpClient,
        *,
        publish_path: str = "/v1/publish-to-uckk/packages",
        reconcile_path: str = "/v1/publish-to-uckk/reconcile",
        max_package_bytes: int = 16 * 1024 * 1024,
    ) -> None:
        if not isinstance(transport, UnixHttpClient) and not hasattr(transport, "request"):
            raise TypeError("transport must implement the common request interface")
        if max_package_bytes <= 0:
            raise ValueError("max_package_bytes must be positive")
        self._transport = transport
        self._publish_path = publish_path
        self._reconcile_path = reconcile_path
        self._max_package_bytes = max_package_bytes

    @classmethod
    def from_socket(cls, socket_path: str, *, timeout_seconds: float = 30.0) -> "UckkPublisher":
        return cls(
            UnixHttpClient(
                socket_path,
                sender="publication_gateway",
                timeout_seconds=timeout_seconds,
                max_response_bytes=4 * 1024 * 1024,
                interface_version="1.0.0",
            )
        )

    @staticmethod
    def _text(value: Any, field: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ProtocolError(f"UCKK publication {field} must be a non-empty string")
        return value.strip()

    @classmethod
    def _strings(cls, value: Any, field: str) -> tuple[str, ...]:
        if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
            raise ProtocolError(f"UCKK publication {field} must be an array")
        result = tuple(cls._text(item, field) for item in value)
        if len(result) != len(set(result)):
            raise ProtocolError(f"UCKK publication {field} must be unique")
        return result

    @staticmethod
    def _timestamp(value: Any) -> datetime:
        if not isinstance(value, str):
            raise ProtocolError("UCKK publication occurred_at must be a timestamp")
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ProtocolError("UCKK publication occurred_at is invalid") from exc
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            raise ProtocolError("UCKK publication occurred_at must include timezone")
        return parsed.astimezone(timezone.utc)

    def _validate_package(self, package: Mapping[str, Any], idempotency_key: str) -> dict[str, Any]:
        if not isinstance(package, Mapping):
            raise TypeError("package must be an object")
        normalized = dict(package)
        required = {
            "package_id",
            "package_version",
            "created_at",
            "source",
            "target",
            "authorization",
            "items",
            "manifest",
            "idempotency_key",
            "frame_compatibility",
        }
        missing = sorted(required - set(normalized))
        if missing:
            raise ValueError("UCKK publication package is missing: " + ", ".join(missing))
        if normalized.get("idempotency_key") != idempotency_key:
            raise ValueError("package idempotency_key does not match transport idempotency")
        items = normalized.get("items")
        if not isinstance(items, list) or not items:
            raise ValueError("UCKK publication package items must be a non-empty array")
        try:
            encoded = json.dumps(
                normalized,
                ensure_ascii=False,
                allow_nan=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
        except (TypeError, ValueError) as exc:
            raise ValueError("UCKK publication package must contain JSON-compatible values") from exc
        if len(encoded) > self._max_package_bytes:
            raise ValueError("UCKK publication package exceeds the configured size limit")
        return normalized

    def publish(
        self,
        *,
        package: Mapping[str, Any],
        correlation: Correlation,
        idempotency_key: str,
    ) -> UckkPublicationResult:
        normalized = self._validate_package(package, idempotency_key)
        response = self._transport.request(
            "POST",
            self._publish_path,
            body={"direction": "publish_to_uckk", "package": normalized},
            correlation=correlation,
            idempotency_key=idempotency_key,
            expected_status=(200, 201, 202),
        )
        return self._parse_response(
            response,
            package_id=self._text(normalized.get("package_id"), "package_id"),
            idempotency_key=idempotency_key,
            correlation=correlation,
        )

    def reconcile(
        self,
        *,
        package_id: str,
        attempt_id: str,
        correlation: Correlation,
        idempotency_key: str,
    ) -> UckkPublicationResult:
        body = {
            "direction": "publish_to_uckk",
            "package_id": package_id,
            "attempt_id": attempt_id,
            "idempotency_key": idempotency_key,
        }
        response = self._transport.request(
            "POST",
            self._reconcile_path,
            body=body,
            correlation=correlation,
            idempotency_key=idempotency_key,
            expected_status=(200,),
        )
        return self._parse_response(
            response,
            package_id=package_id,
            idempotency_key=idempotency_key,
            correlation=correlation,
        )

    def _parse_response(
        self,
        response: Mapping[str, Any] | None,
        *,
        package_id: str,
        idempotency_key: str,
        correlation: Correlation,
    ) -> UckkPublicationResult:
        if not isinstance(response, Mapping):
            raise ProtocolError("UCKK publication response must be an object")
        if response.get("package_id") != package_id:
            raise ProtocolError("UCKK publication package identity mismatch")
        if response.get("idempotency_key") != idempotency_key:
            raise ProtocolError("UCKK publication idempotency mismatch")
        if response.get("correlation_id") != correlation.correlation_id:
            raise ProtocolError("UCKK publication correlation mismatch")
        if response.get("source_authority_preserved") is not True:
            raise ProtocolError("UCKK publication must preserve source authority")
        if response.get("remote_authority_separate") is not True:
            raise ProtocolError("UCKK publication must preserve remote authority separation")
        try:
            outcome = UckkPublicationOutcome(response.get("outcome"))
        except (TypeError, ValueError) as exc:
            raise ProtocolError("UCKK publication outcome is unknown") from exc
        item_values = response.get("item_results")
        if not isinstance(item_values, Sequence) or isinstance(item_values, (str, bytes, bytearray)):
            raise ProtocolError("UCKK publication item_results must be an array")
        items: list[Mapping[str, Any]] = []
        for item in item_values:
            if not isinstance(item, Mapping):
                raise ProtocolError("UCKK publication item result must be an object")
            items.append(MappingProxyType(dict(item)))
        if not items:
            raise ProtocolError("UCKK publication item_results must not be empty")
        retry = response.get("retry", {})
        if not isinstance(retry, Mapping):
            raise ProtocolError("UCKK publication retry must be an object")
        if outcome in {
            UckkPublicationOutcome.PARTIALLY_PUBLISHED,
            UckkPublicationOutcome.UNKNOWN_RECONCILIATION_REQUIRED,
        } and retry.get("automatic_retry_allowed") is True:
            raise ProtocolError("partial or uncertain delivery cannot permit automatic retry")
        receipt_id = self._text(response.get("receipt_id"), "receipt_id")
        attempt_id = self._text(response.get("attempt_id"), "attempt_id")
        return UckkPublicationResult(
            receipt_id=receipt_id,
            package_id=package_id,
            attempt_id=attempt_id,
            idempotency_key=idempotency_key,
            correlation_id=correlation.correlation_id,
            outcome=outcome,
            occurred_at=self._timestamp(response.get("occurred_at")),
            item_results=tuple(items),
            retry=MappingProxyType(dict(retry)),
            evidence_refs=self._strings(response.get("evidence_refs", []), "evidence_refs"),
            receipt=MappingProxyType(dict(response)),
        )
