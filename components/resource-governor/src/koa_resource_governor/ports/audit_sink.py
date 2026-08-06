"""Selective evidence boundary for resource-governance decisions."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, runtime_checkable


@runtime_checkable
class AuditSink(Protocol):
    """Persist bounded resource facts through the public Audit Broker boundary."""

    def record(
        self,
        record: Mapping[str, object],
        *,
        required_receipt: bool = True,
    ) -> str | None:
        """Return an immutable receipt reference or fail when it is required."""
        raise RuntimeError("protocol method must be implemented by an adapter")
