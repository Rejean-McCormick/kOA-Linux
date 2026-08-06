"""Append-only, correlated operational evidence records."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Mapping

from .config import (
    ConfigurationError,
    canonical_json_bytes,
    ensure_directory,
    identifier,
    json_digest,
    reference,
    write_json_atomic,
)


class EvidenceError(RuntimeError):
    """Raised when evidence cannot be recorded or its chain is invalid."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _timestamp(value: str) -> str:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise EvidenceError("evidence timestamp must be RFC 3339") from exc
    if parsed.tzinfo is None:
        raise EvidenceError("evidence timestamp must include an offset")
    return parsed.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


@dataclass(frozen=True, slots=True)
class EvidenceRecord:
    payload: Mapping[str, object]
    digest: str
    path: Path


class EvidenceJournal:
    """Writes immutable records linked by digest within one correlation scope."""

    def __init__(self, root: str | Path, *, clock: Callable[[], str] = utc_now) -> None:
        self.root = ensure_directory(Path(root))
        self.clock = clock

    def _records(self, correlation_id: str) -> list[Path]:
        directory = self.root / identifier(correlation_id, "correlation_id")
        if not directory.exists():
            return []
        return sorted(directory.glob("[0-9][0-9][0-9][0-9][0-9][0-9]-*.json"))

    def record(
        self,
        *,
        operation_id: str,
        correlation_id: str,
        phase: str,
        outcome: str,
        subject_ref: str,
        details: Mapping[str, object],
        classification: str = "operational",
    ) -> EvidenceRecord:
        operation = identifier(operation_id, "operation_id")
        correlation = identifier(correlation_id, "correlation_id")
        phase_id = identifier(phase, "phase")
        outcome_id = identifier(outcome, "outcome")
        if outcome_id not in {"succeeded", "failed", "blocked"}:
            raise EvidenceError(f"unsupported evidence outcome: {outcome_id}")
        classification_id = identifier(classification, "classification")
        subject = reference(subject_ref, "subject_ref")
        if not isinstance(details, Mapping):
            raise EvidenceError("evidence details must be an object")
        directory = ensure_directory(self.root / correlation)
        previous_digest: str | None = None
        records = self._records(correlation)
        sequence = len(records) + 1
        if records:
            import json
            previous_payload = json.loads(records[-1].read_text(encoding="utf-8"))
            previous_digest = hashlib.sha256(canonical_json_bytes(previous_payload)).hexdigest()
        occurred_at = _timestamp(self.clock())
        detail_digest = json_digest(dict(details))
        stable = {
            "operation_id": operation,
            "correlation_id": correlation,
            "phase": phase_id,
            "outcome": outcome_id,
            "subject_ref": subject,
            "occurred_at": occurred_at,
            "details_digest": detail_digest,
            "previous_evidence_digest": previous_digest,
        }
        evidence_id = "evidence-" + hashlib.sha256(canonical_json_bytes(stable)).hexdigest()[:24]
        payload: dict[str, object] = {
            "format": "koa.operations.evidence.v1",
            "evidence_id": evidence_id,
            "sequence": sequence,
            **stable,
            "classification": classification_id,
        }
        path = directory / f"{sequence:06d}-{evidence_id}.json"
        try:
            write_json_atomic(path, payload)
        except ConfigurationError as exc:
            raise EvidenceError(str(exc)) from exc
        return EvidenceRecord(payload=payload, digest=json_digest(payload), path=path)

    def verify(self, correlation_id: str) -> tuple[str, ...]:
        import json
        correlation = identifier(correlation_id, "correlation_id")
        previous: str | None = None
        digests: list[str] = []
        for expected_sequence, path in enumerate(self._records(correlation), start=1):
            payload = json.loads(path.read_text(encoding="utf-8"))
            if payload.get("sequence") != expected_sequence:
                raise EvidenceError(f"non-contiguous evidence sequence at {path}")
            if payload.get("correlation_id") != correlation:
                raise EvidenceError(f"correlation mismatch at {path}")
            if payload.get("previous_evidence_digest") != previous:
                raise EvidenceError(f"broken evidence chain at {path}")
            previous = hashlib.sha256(canonical_json_bytes(payload)).hexdigest()
            digests.append(previous)
        return tuple(digests)
