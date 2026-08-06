"""Derived index port used for bounded deterministic local queries."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True, slots=True)
class IndexQueryPage:
    items: Sequence[Mapping[str, Any]]
    next_cursor: str | None = None
    total_count: int | None = None


class IndexStore(Protocol):
    def query(
        self,
        artifact_id: str,
        artifact_version: str,
        query_class: str,
        parameters: Mapping[str, Any],
        *,
        limit: int,
        cursor: str | None,
        timeout_ms: int,
    ) -> IndexQueryPage:
        raise NotImplementedError

    def withdraw(self, artifact_id: str, artifact_version: str, scope: str) -> None:
        """Remove or disable derived query structures for a revoked scope."""
        raise NotImplementedError
