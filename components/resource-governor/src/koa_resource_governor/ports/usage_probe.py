"""Read-only resource usage observation boundary."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, runtime_checkable


@runtime_checkable
class UsageProbe(Protocol):
    """Observe resource metadata without reading workload business content."""

    def observe_usage(
        self,
        target_execution_ref: str,
        **selector: object,
    ) -> Mapping[str, object]:
        """Return one RG-IF-005 observation for the selected execution."""
        raise RuntimeError("protocol method must be implemented by an adapter")
