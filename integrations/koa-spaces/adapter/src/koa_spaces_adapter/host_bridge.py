"""Narrow host lifecycle bridge for the optional kOA Spaces process."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol, runtime_checkable


class HostBridgeError(RuntimeError):
    """Raised when the declared host lifecycle interface rejects an operation."""


@runtime_checkable
class HostLifecyclePort(Protocol):
    """Public host lifecycle interface supplied by the deployment."""

    def invoke(
        self,
        operation_id: str,
        parameters: Mapping[str, Any],
        *,
        correlation_id: str,
        idempotency_key: str,
    ) -> Mapping[str, Any]:
        """Invoke one profile-registered lifecycle operation."""


@dataclass(frozen=True, slots=True)
class HostBridge:
    port: HostLifecyclePort
    start_operation_id: str
    stop_operation_id: str
    status_operation_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.port, HostLifecyclePort):
            raise TypeError("port must implement HostLifecyclePort")
        for value in (
            self.start_operation_id,
            self.stop_operation_id,
            self.status_operation_id,
        ):
            if not value or len(value) > 160:
                raise ValueError("host operation identifiers must be explicit and bounded")

    def _invoke(
        self,
        operation_id: str,
        *,
        profile_id: str,
        correlation_id: str,
        idempotency_key: str,
    ) -> Mapping[str, Any]:
        if not profile_id or not correlation_id or not idempotency_key:
            raise ValueError("profile, correlation, and idempotency identifiers are required")
        result = self.port.invoke(
            operation_id,
            {"subsystem_id": "koa_spaces", "profile_id": profile_id},
            correlation_id=correlation_id,
            idempotency_key=idempotency_key,
        )
        if not isinstance(result, Mapping):
            raise HostBridgeError("host lifecycle response must be an object")
        state = result.get("state")
        if state not in {"accepted", "completed", "rejected", "failed"}:
            raise HostBridgeError("host lifecycle response has an invalid state")
        if state in {"rejected", "failed"}:
            raise HostBridgeError(f"host lifecycle operation {state}")
        return result

    def start(
        self, *, profile_id: str, correlation_id: str, idempotency_key: str
    ) -> Mapping[str, Any]:
        return self._invoke(
            self.start_operation_id,
            profile_id=profile_id,
            correlation_id=correlation_id,
            idempotency_key=idempotency_key,
        )

    def stop(
        self, *, profile_id: str, correlation_id: str, idempotency_key: str
    ) -> Mapping[str, Any]:
        return self._invoke(
            self.stop_operation_id,
            profile_id=profile_id,
            correlation_id=correlation_id,
            idempotency_key=idempotency_key,
        )

    def status(
        self, *, profile_id: str, correlation_id: str, idempotency_key: str
    ) -> Mapping[str, Any]:
        return self._invoke(
            self.status_operation_id,
            profile_id=profile_id,
            correlation_id=correlation_id,
            idempotency_key=idempotency_key,
        )
