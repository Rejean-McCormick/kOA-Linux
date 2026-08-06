"""System clock adapter with explicit UTC and monotonic time domains."""

from __future__ import annotations

import time
from datetime import datetime, timezone


class SystemClock:
    """Clock port implementation; wall time is always timezone-aware UTC."""

    def now(self) -> datetime:
        return datetime.now(timezone.utc)

    def monotonic_ns(self) -> int:
        return time.monotonic_ns()
