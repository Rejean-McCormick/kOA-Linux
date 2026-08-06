"""Evidence port for Kristal Runtime transitions and governed reads."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol


class AuditSink(Protocol):
    def record(self, event: Mapping[str, Any]) -> str:
        """Persist an idempotent event and return its durable receipt reference."""
        raise NotImplementedError
