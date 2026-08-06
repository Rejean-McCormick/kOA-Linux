"""Public transport client for the optional kOA Spaces subsystem.

The adapter intentionally knows no subsystem-internal endpoints or storage.  A
transport supplied by the deployment maps the stable boundary operation names
to the independently versioned subsystem implementation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol, runtime_checkable


class SpacesClientError(RuntimeError):
    """Base error for the kOA Spaces boundary client."""


class SubsystemUnavailable(SpacesClientError):
    """Raised when the optional subsystem cannot be reached."""


class BoundaryResponseError(SpacesClientError):
    """Raised when a response violates the declared public boundary."""


@runtime_checkable
class SpacesTransport(Protocol):
    """Deployment-supplied transport for public kOA Spaces operations."""

    def request(
        self,
        operation: str,
        payload: Mapping[str, Any] | None,
        *,
        timeout_seconds: float,
    ) -> Mapping[str, Any]:
        """Execute one registered public operation and return a JSON object."""


_ALLOWED_OPERATIONS = frozenset(
    {
        "health.read",
        "capabilities.read",
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
    """Small fail-closed client for the public kOA Spaces boundary."""

    transport: SpacesTransport
    timeout_seconds: float = 5.0

    def __post_init__(self) -> None:
        if not isinstance(self.timeout_seconds, (int, float)) or self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        if self.timeout_seconds > 60:
            raise ValueError("timeout_seconds must not exceed 60 seconds")
        if not isinstance(self.transport, SpacesTransport):
            raise TypeError("transport must implement SpacesTransport")

    def call(
        self,
        operation: str,
        payload: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        if operation not in _ALLOWED_OPERATIONS:
            raise ValueError(f"unregistered kOA Spaces operation: {operation}")
        request_payload = _json_object(payload, label="payload")
        try:
            response = self.transport.request(
                operation,
                request_payload,
                timeout_seconds=float(self.timeout_seconds),
            )
        except (TimeoutError, ConnectionError, OSError) as exc:
            raise SubsystemUnavailable(f"kOA Spaces unavailable during {operation}") from exc
        except SpacesClientError:
            raise
        except Exception as exc:  # transport boundary: convert unknown provider failures
            raise SpacesClientError(f"kOA Spaces transport failed during {operation}") from exc
        return _json_object(response, label="response")

    def read_health(self) -> dict[str, Any]:
        return self.call("health.read")

    def read_capabilities(self) -> dict[str, Any]:
        return self.call("capabilities.read")

    def read_manifest(self, manifest_ref: str) -> dict[str, Any]:
        if not manifest_ref or len(manifest_ref) > 512:
            raise ValueError("manifest_ref must be between 1 and 512 characters")
        return self.call("manifest.read", {"manifest_ref": manifest_ref})

    def activate_space(self, request: Mapping[str, Any]) -> dict[str, Any]:
        return self.call("space.activate", request)

    def rollback_space(self, request: Mapping[str, Any]) -> dict[str, Any]:
        return self.call("space.rollback", request)

    def deactivate_space(self, request: Mapping[str, Any]) -> dict[str, Any]:
        return self.call("space.deactivate", request)
