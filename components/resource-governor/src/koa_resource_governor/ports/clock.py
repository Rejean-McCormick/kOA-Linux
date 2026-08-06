"""Time boundary consumed by Resource Governor application use cases."""

from __future__ import annotations

from datetime import datetime
from typing import Protocol, runtime_checkable


@runtime_checkable
class Clock(Protocol):
    """Provide an aware current instant without coupling to the system clock."""

    def now(self) -> datetime:
        """Return the current timezone-aware instant."""
        raise RuntimeError("protocol method must be implemented by an adapter")

    def now_iso(self) -> str:
        """Return the same instant in canonical RFC 3339 form."""
        raise RuntimeError("protocol method must be implemented by an adapter")
