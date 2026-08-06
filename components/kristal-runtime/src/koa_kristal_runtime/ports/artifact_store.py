"""Persistence port for authoritative Kristal artifact records."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, Protocol

StoreWriteOutcome = Literal["created", "existing"]


class ArtifactStore(Protocol):
    """Owns admitted artifacts, verification records, and revocation state."""

    def get_artifact(self, artifact_id: str, artifact_version: str) -> Mapping[str, Any] | None:
        raise NotImplementedError

    def find_by_content_digest(self, content_digest: str) -> Mapping[str, Any] | None:
        raise NotImplementedError

    def admit_artifact(
        self,
        artifact: Mapping[str, Any],
        admission_record: Mapping[str, Any],
    ) -> StoreWriteOutcome:
        """Atomically create the candidate or confirm identical existing content."""
        raise NotImplementedError

    def get_verification(self, artifact_id: str, artifact_version: str) -> Mapping[str, Any] | None:
        raise NotImplementedError

    def record_verification(self, record: Mapping[str, Any]) -> StoreWriteOutcome:
        raise NotImplementedError

    def get_revocation(self, artifact_id: str, artifact_version: str) -> Mapping[str, Any] | None:
        raise NotImplementedError

    def record_revocation(self, record: Mapping[str, Any]) -> StoreWriteOutcome:
        """Atomically persist a revocation before derived indexes are withdrawn."""
        raise NotImplementedError
