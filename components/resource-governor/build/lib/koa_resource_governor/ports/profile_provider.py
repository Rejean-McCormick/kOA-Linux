"""Read-only profile and resource-envelope provider boundary."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, runtime_checkable

from ..domain import ResourceEnvelope


ProfileDocument = Mapping[str, object]
EnvelopeDocument = ResourceEnvelope | Mapping[str, object]


@runtime_checkable
class ProfileProvider(Protocol):
    """Load explicitly selected profile facts and envelope artifacts."""

    def get_active_profile(self) -> ProfileDocument:
        """Return the active profile document without changing it."""
        raise RuntimeError("protocol method must be implemented by an adapter")

    def get_resource_envelope(self, reference: str) -> EnvelopeDocument:
        """Return exactly the referenced envelope or fail."""
        raise RuntimeError("protocol method must be implemented by an adapter")
