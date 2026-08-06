"""UTC system clock adapter for Resource Governor application ports."""

from __future__ import annotations

from datetime import UTC, datetime


class SystemClock:
    """Provide timezone-aware UTC wall-clock observations."""

    def now(self) -> datetime:
        """Return the current wall-clock time as an aware UTC datetime."""

        return datetime.now(UTC)

    def now_iso(self) -> str:
        """Return a canonical RFC 3339 timestamp with a ``Z`` suffix."""

        return self.now().isoformat(timespec="microseconds").replace("+00:00", "Z")
