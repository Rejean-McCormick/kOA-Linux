"""Deterministic, bounded JSON Lines export for Audit Broker-owned records."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from contextlib import suppress
from dataclasses import asdict, dataclass, is_dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from .sqlite_event_store import InvalidRecordError


DEFAULT_RECORD_FIELDS = frozenset(
    {
        "audit_record_id", "event_class_id", "producer_component_id", "producer_identity",
        "occurred_at", "received_at", "subject_references", "action_or_transition", "outcome",
        "purpose", "classification", "retention_class", "correlation_id",
        "source_receipt_or_evidence_refs", "bounded_payload", "policy_or_contract_ref",
        "record_state", "integrity_algorithm", "integrity_digest", "created_at",
    }
)


@dataclass(frozen=True, slots=True)
class JournalExportResult:
    export_id: str
    path: Path
    record_count: int
    byte_count: int
    sha256: str


def _json_value(value: Any) -> Any:
    if isinstance(value, datetime):
        if value.tzinfo is None or value.utcoffset() is None:
            raise InvalidRecordError("journal timestamps must include a timezone")
        return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return _json_value(asdict(value))
    if isinstance(value, Mapping):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_value(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise InvalidRecordError(f"journal value of type {type(value).__name__} is not JSON-compatible")


def _mapping(value: Any) -> dict[str, Any]:
    if is_dataclass(value):
        value = asdict(value)
    elif not isinstance(value, Mapping) and hasattr(value, "to_dict"):
        value = value.to_dict()
    if not isinstance(value, Mapping):
        raise InvalidRecordError("journal records must be mappings or dataclass-like values")
    return {str(key): _json_value(item) for key, item in value.items()}


def _line(value: Mapping[str, Any]) -> bytes:
    return (json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n").encode("utf-8")


class JournalExporter:
    """Writes an atomic export with an explicit allowlist and deterministic order."""

    def __init__(self, *, max_records: int = 100_000, max_bytes: int = 1_073_741_824) -> None:
        if not isinstance(max_records, int) or max_records <= 0:
            raise ValueError("max_records must be positive")
        if not isinstance(max_bytes, int) or max_bytes <= 0:
            raise ValueError("max_bytes must be positive")
        self.max_records = max_records
        self.max_bytes = max_bytes

    def export_records(
        self,
        records: Iterable[Any],
        destination: str | Path,
        *,
        export_id: str,
        generated_at: datetime,
        field_allowlist: Sequence[str] = tuple(sorted(DEFAULT_RECORD_FIELDS)),
        overwrite: bool = False,
    ) -> JournalExportResult:
        if not isinstance(export_id, str) or not export_id.strip():
            raise InvalidRecordError("export_id must be a non-empty string")
        if generated_at.tzinfo is None or generated_at.utcoffset() is None:
            raise InvalidRecordError("generated_at must include a timezone")
        allowed = frozenset(field_allowlist)
        if not allowed or not allowed <= DEFAULT_RECORD_FIELDS:
            invalid = sorted(allowed - DEFAULT_RECORD_FIELDS)
            raise InvalidRecordError("journal field allowlist is empty or unsupported: " + ", ".join(invalid))
        target = Path(destination)
        if target.exists() and not overwrite:
            raise FileExistsError(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.parent.is_symlink():
            raise InvalidRecordError("journal destination parent may not be a symlink")

        normalized: list[dict[str, Any]] = []
        for index, record in enumerate(records, start=1):
            if index > self.max_records:
                raise InvalidRecordError("journal export exceeds max_records")
            value = _mapping(record)
            unexpected = set(value) - DEFAULT_RECORD_FIELDS
            if unexpected:
                raise InvalidRecordError("journal record has undeclared fields: " + ", ".join(sorted(unexpected)))
            selected = {key: value[key] for key in sorted(allowed) if key in value}
            normalized.append(selected)
        normalized.sort(key=lambda item: (
            str(item.get("audit_record_id", "")),
            json.dumps(item, ensure_ascii=False, separators=(",", ":"), sort_keys=True),
        ))

        generated = generated_at.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
        records_digest = hashlib.sha256()
        record_lines: list[bytes] = []
        for sequence, record in enumerate(normalized, start=1):
            raw = _line({"sequence": sequence, "record": record})
            records_digest.update(raw)
            record_lines.append(raw)
        header = _line({
            "journal_version": "1.0.0", "record_type": "header", "export_id": export_id.strip(),
            "generated_at": generated, "record_count": len(normalized),
            "field_allowlist": sorted(allowed), "records_sha256": records_digest.hexdigest(),
        })
        trailer = _line({
            "journal_version": "1.0.0", "record_type": "trailer", "export_id": export_id.strip(),
            "record_count": len(normalized), "records_sha256": records_digest.hexdigest(),
        })
        payload_size = len(header) + sum(map(len, record_lines)) + len(trailer)
        if payload_size > self.max_bytes:
            raise InvalidRecordError("journal export exceeds max_bytes")

        fd, temporary_name = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".tmp", dir=target.parent)
        digest = hashlib.sha256()
        try:
            with os.fdopen(fd, "wb") as handle:
                for part in (header, *record_lines, trailer):
                    handle.write(part); digest.update(part)
                handle.flush(); os.fsync(handle.fileno())
            if target.exists() and not overwrite:
                raise FileExistsError(target)
            os.replace(temporary_name, target)
        except Exception:
            with suppress(FileNotFoundError):
                os.unlink(temporary_name)
            raise
        return JournalExportResult(export_id.strip(), target, len(normalized), payload_size, digest.hexdigest())

    export = export_records
