"""Trusted clock boundary for policy evaluation and lifecycle transitions."""

from __future__ import annotations

from abc import abstractmethod
from datetime import datetime
from typing import Protocol, runtime_checkable


@runtime_checkable
class Clock(Protocol):
    """Return trusted, timezone-aware time."""

    @abstractmethod
    def now(self) -> datetime:
        """Return the current trusted instant."""
        raise NotImplementedError("a trusted Clock adapter is required")
