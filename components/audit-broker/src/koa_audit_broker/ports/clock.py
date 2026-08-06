"""Time authority port for Audit Broker application services."""

from __future__ import annotations

from abc import abstractmethod
from datetime import datetime
from typing import Protocol, runtime_checkable


@runtime_checkable
class Clock(Protocol):
    """Supplies timezone-aware wall-clock instants.

    Implementations belong to the adapter layer. Application services reject
    naive values so retention, expiry, and custody ordering are unambiguous.
    """

    @abstractmethod
    def now(self) -> datetime:
        """Return the current timezone-aware instant."""
        raise NotImplementedError("a Clock adapter is required")
