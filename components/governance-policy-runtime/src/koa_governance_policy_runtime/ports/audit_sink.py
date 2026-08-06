"""Selective evidence boundary to Audit Broker.

The sink accepts minimized policy-decision and lifecycle evidence. It does not
own policy state and cannot change a decision or activation outcome.
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
    subject_refs: tuple[str, ...]
    payload: Mapping[str, Any]
    evidence_refs: tuple[str, ...] = ()


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
    """Submit minimized evidence through Audit Broker's public interface."""

    @abstractmethod
    def is_available(self) -> bool:
        """Report whether evidence can be accepted or durably buffered."""
        raise NotImplementedError("an AuditSink adapter is required")

    @abstractmethod
    def submit(self, evidence: AuditEvidence) -> AuditSubmission:
        """Submit one immutable evidence record."""
        raise NotImplementedError("an AuditSink adapter is required")
