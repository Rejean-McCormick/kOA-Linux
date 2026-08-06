"""Clock port used to make all identity and trust decisions time-explicit."""

from __future__ import annotations

from datetime import datetime
from typing import Protocol, runtime_checkable


@runtime_checkable
class Clock(Protocol):
    """Provide the authoritative evaluation time for one component instance."""

    def now(self) -> datetime:
        """Return an aware timestamp; application services normalize it to UTC."""
        raise NotImplementedError
