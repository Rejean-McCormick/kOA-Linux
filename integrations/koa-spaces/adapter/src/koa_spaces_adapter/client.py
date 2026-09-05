"""Fail-closed public transport client for the optional Koali Spaces subsystem."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol, runtime_checkable


class SpacesClientError(RuntimeError):
    """Base error for the Koali Spaces integration client."""


class SubsystemUnavailable(SpacesClientError):
    """Raised when the optional Koali Spaces subsystem cannot be reached."""


class BoundaryResponseError(SpacesClientError):
    """Raised when the Koali Spaces boundary returns invalid data."""


@runtime_checkable
class SpacesTransport(Protocol):
    def request(
        self,
        operation: str,
        payload: Mapping[str, Any] | None,
        *,
        timeout_seconds: float,
    ) -> Mapping[str, Any]: ...


_ALLOWED_OPERATIONS = frozenset(
    {
        "health.read",
        "capabilities.read",
        "capabilities.update",
        "shell.state.read",
        "space.activate",
        "space.rollback",
        "space.deactivate",
        "manifest.read",
    }
)


def _json_object(value: Mapping[str, Any] | None, *, label: str) -> dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise BoundaryResponseError(f"{label} must be a JSON object")
    return {str(key): item for key, item in value.items()}


@dataclass(frozen=True, slots=True)
class SpacesClient:
    transport: SpacesTransport
    timeout_seconds: float = 5.0

    def __post_init__(self) -> None:
        if not isinstance(self.timeout_seconds, (int, float)) or not 0 < self.timeout_seconds <= 60:
            raise ValueError("timeout_seconds must be in (0, 60]")

    def call(
        self, operation: str, payload: Mapping[str, Any] | None = None
    ) -> Mapping[str, Any]:
        if operation not in _ALLOWED_OPERATIONS:
            raise ValueError(f"unsupported Koali Spaces operation: {operation}")
        try:
            response = self.transport.request(
                operation,
                _json_object(payload, label="request"),
                timeout_seconds=float(self.timeout_seconds),
            )
        except SpacesClientError:
            raise
        except (OSError, TimeoutError, ConnectionError) as exc:
            raise SubsystemUnavailable(operation) from exc
        if not isinstance(response, Mapping):
            raise BoundaryResponseError("response must be a JSON object")
        return _json_object(response, label="response")

    def read_health(self) -> Mapping[str, Any]:
        return self.call("health.read")

    def read_capabilities(self) -> Mapping[str, Any]:
        return self.call("capabilities.read")

    def update_capabilities(self, capability_snapshot: Mapping[str, Any]) -> Mapping[str, Any]:
        return self.call("capabilities.update", {"capability_snapshot": dict(capability_snapshot)})

    def read_shell_state(self) -> Mapping[str, Any]:
        return self.call("shell.state.read")

    def read_manifest(self, manifest_ref: str) -> Mapping[str, Any]:
        return self.call("manifest.read", {"manifest_ref": manifest_ref})

    def activate_space(self, payload: Mapping[str, Any]) -> Mapping[str, Any]:
        return self.call("space.activate", payload)

    def rollback_space(self, payload: Mapping[str, Any]) -> Mapping[str, Any]:
        return self.call("space.rollback", payload)

    def deactivate_space(self, payload: Mapping[str, Any]) -> Mapping[str, Any]:
        return self.call("space.deactivate", payload)
