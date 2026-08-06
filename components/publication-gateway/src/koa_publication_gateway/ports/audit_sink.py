"""Selective evidence boundary to Audit Broker.

The sink accepts minimized publication lifecycle evidence. It does not receive
source payloads and cannot authorize, stage, dispatch, or finalize a publication.
"""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any, Mapping, Protocol, runtime_checkable


class AuditDisposition(StrEnum):
    ACCEPTED = "accepted"
    BUFFERED = "buffered"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class AuditEvidence:
    evidence_id: str
    event_type: str
    correlation_id: str
    occurred_at: datetime
    request_id: str
    outcome: str
    subject_refs: tuple[str, ...]
    payload: Mapping[str, Any]
    evidence_refs: tuple[str, ...] = ()
    restricted: bool = True


@dataclass(frozen=True, slots=True)
class AuditSubmission:
    disposition: AuditDisposition
    evidence_ref: str | None = None
    reason_codes: tuple[str, ...] = ()

    @property
    def retained(self) -> bool:
        return self.disposition in {AuditDisposition.ACCEPTED, AuditDisposition.BUFFERED}


@runtime_checkable
class AuditSink(Protocol):
    """Submit bounded evidence through Audit Broker's public interface."""

    @abstractmethod
    def is_available(self) -> bool:
        """Return whether evidence can be accepted or durably buffered."""
        raise NotImplementedError("an AuditSink adapter is required")

    @abstractmethod
    def submit(self, evidence: AuditEvidence) -> AuditSubmission:
        """Submit one immutable, minimized evidence record."""
        raise NotImplementedError("an AuditSink adapter is required")
