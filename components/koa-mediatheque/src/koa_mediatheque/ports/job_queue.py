"""Bounded background-job queue port."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping, Protocol, runtime_checkable

_ALLOWED_TYPES = frozenset({"thumbnail", "preview", "text_extraction", "transcode", "index"})
_ALLOWED_PRIORITIES = frozenset({"interactive", "normal", "background"})
_ALLOWED_OUTCOMES = frozenset({"queued", "already_queued", "deferred", "rejected"})


@dataclass(frozen=True, slots=True)
class JobRequest:
    job_id: str
    idempotency_key: str
    job_type: str
    priority: str
    payload: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.job_id.strip() or not self.idempotency_key.strip():
            raise ValueError("job_id and idempotency_key must not be empty")
        if self.job_type not in _ALLOWED_TYPES:
            raise ValueError(f"unsupported job type: {self.job_type}")
        if self.priority not in _ALLOWED_PRIORITIES:
            raise ValueError(f"unsupported priority: {self.priority}")
        frozen: dict[str, str] = {}
        for key, value in self.payload.items():
            if not isinstance(key, str) or not key.strip() or not isinstance(value, str):
                raise ValueError("job payload must contain non-empty string keys and string values")
            frozen[key] = value
        object.__setattr__(self, "payload", MappingProxyType(dict(sorted(frozen.items()))))


@dataclass(frozen=True, slots=True)
class JobSubmission:
    outcome: str
    queue_ref: str | None
    reason_code: str

    def __post_init__(self) -> None:
        if self.outcome not in _ALLOWED_OUTCOMES:
            raise ValueError(f"unsupported queue outcome: {self.outcome}")
        if not self.reason_code.strip():
            raise ValueError("reason_code must not be empty")
        if self.outcome in {"queued", "already_queued"} and not (self.queue_ref or "").strip():
            raise ValueError("queued jobs require queue_ref")


@runtime_checkable
class JobQueue(Protocol):
    def enqueue(self, request: JobRequest) -> JobSubmission:
        """Queue bounded work; resource pressure returns deferred, never false success."""
