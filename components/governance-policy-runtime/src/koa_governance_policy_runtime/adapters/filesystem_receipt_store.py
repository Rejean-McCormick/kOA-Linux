"""Append-only filesystem store for governance decision and lifecycle receipts."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
import threading
from dataclasses import asdict, dataclass, is_dataclass
from datetime import datetime
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

_RECEIPT_FORMAT = "koa-governance-receipt-record/v1"


class ReceiptStoreError(RuntimeError):
    """Base error for receipt persistence."""


class InvalidReceiptError(ReceiptStoreError, ValueError):
    """A receipt is incomplete, non-canonical, or too large."""


class ReceiptConflictError(ReceiptStoreError):
    """A receipt identity was reused with different canonical content."""


class ReceiptNotFoundError(ReceiptStoreError):
    """A requested receipt does not exist."""


class ReceiptIntegrityError(ReceiptStoreError):
    """Stored receipt bytes no longer match their integrity digest."""


@dataclass(frozen=True, slots=True)
class ReceiptWriteResult:
    receipt_id: str
    canonical_digest: str
    duplicate: bool


def _json_value(value: Any) -> Any:
    if isinstance(value, datetime):
        if value.tzinfo is None or value.utcoffset() is None:
            raise InvalidReceiptError("receipt timestamps must include a timezone")
        return value.isoformat()
    if is_dataclass(value):
        return _json_value(asdict(value))
    if hasattr(value, "to_dict") and not isinstance(value, Mapping):
        return _json_value(value.to_dict())
    if isinstance(value, Mapping):
        result: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str) or not key:
                raise InvalidReceiptError("receipt object keys must be non-empty strings")
            result[key] = _json_value(item)
        return result
    if isinstance(value, (list, tuple)):
        return [_json_value(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise InvalidReceiptError(f"unsupported receipt value: {type(value).__name__}")


def _canonical_bytes(value: Any) -> bytes:
    normalized = _json_value(value)
    if not isinstance(normalized, dict):
        raise InvalidReceiptError("receipt must be an object")
    try:
        return json.dumps(
            normalized, ensure_ascii=False, allow_nan=False, separators=(",", ":"), sort_keys=True
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise InvalidReceiptError("receipt must contain canonical JSON values") from exc


class FilesystemReceiptStore:
    """Immutable receipt storage with content verification on every read."""

    def __init__(self, root: str | Path, *, max_receipt_bytes: int = 2 * 1024 * 1024) -> None:
        self.root = Path(root)
        if max_receipt_bytes <= 0:
            raise ValueError("max_receipt_bytes must be positive")
        self.max_receipt_bytes = max_receipt_bytes
        self._records = self.root / "receipts"
        self._lock = threading.RLock()
        try:
            self._records.mkdir(parents=True, exist_ok=True, mode=0o750)
        except OSError as exc:
            raise ReceiptStoreError(f"cannot initialize receipt store: {exc}") from exc

    @staticmethod
    def _text(value: Any, field: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise InvalidReceiptError(f"{field} must be a non-empty string")
        return value.strip()

    @staticmethod
    def _digest(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    def _path(self, receipt_id: str) -> Path:
        identifier = self._text(receipt_id, "receipt_id")
        digest = hashlib.sha256(identifier.encode("utf-8")).hexdigest()
        return self._records / digest[:2] / f"{digest}.json"

    @staticmethod
    def _fsync_directory(path: Path) -> None:
        descriptor = os.open(path, os.O_RDONLY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)

    def _atomic_create(self, path: Path, data: bytes) -> None:
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o750)
        descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
        temporary = Path(temporary_name)
        try:
            os.fchmod(descriptor, 0o640)
            with os.fdopen(descriptor, "wb", closefd=True) as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            os.link(temporary, path)
            self._fsync_directory(path.parent)
        finally:
            if temporary.exists():
                temporary.unlink()

    def put(self, receipt: Any) -> ReceiptWriteResult:
        payload = _json_value(receipt)
        if not isinstance(payload, dict):
            raise InvalidReceiptError("receipt must be an object")
        receipt_id = self._text(payload.get("receipt_id"), "receipt_id")
        correlation_id = self._text(payload.get("correlation_id"), "correlation_id")
        canonical_receipt = _canonical_bytes(payload)
        if len(canonical_receipt) > self.max_receipt_bytes:
            raise InvalidReceiptError("receipt exceeds the configured size limit")
        digest = self._digest(canonical_receipt)
        envelope = {
            "format": _RECEIPT_FORMAT,
            "receipt_id": receipt_id,
            "correlation_id": correlation_id,
            "canonical_digest": digest,
            "receipt": payload,
        }
        encoded = _canonical_bytes(envelope) + b"\n"
        path = self._path(receipt_id)
        with self._lock:
            if path.exists():
                existing = self.get(receipt_id)
                existing_digest = self._digest(_canonical_bytes(existing))
                if existing_digest != digest:
                    raise ReceiptConflictError("receipt_id already exists with different content")
                return ReceiptWriteResult(receipt_id, digest, True)
            try:
                self._atomic_create(path, encoded)
            except FileExistsError:
                existing = self.get(receipt_id)
                if self._digest(_canonical_bytes(existing)) != digest:
                    raise ReceiptConflictError("receipt_id concurrently reused with different content")
                return ReceiptWriteResult(receipt_id, digest, True)
            except OSError as exc:
                raise ReceiptStoreError(f"cannot persist receipt: {exc}") from exc
        return ReceiptWriteResult(receipt_id, digest, False)

    def get(self, receipt_id: str) -> Mapping[str, Any]:
        path = self._path(receipt_id)
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise ReceiptNotFoundError(receipt_id) from exc
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ReceiptIntegrityError(f"cannot read receipt {receipt_id}: {exc}") from exc
        if not isinstance(raw, dict) or raw.get("format") != _RECEIPT_FORMAT:
            raise ReceiptIntegrityError("stored receipt envelope format mismatch")
        if raw.get("receipt_id") != receipt_id:
            raise ReceiptIntegrityError("stored receipt identity mismatch")
        receipt = raw.get("receipt")
        if not isinstance(receipt, dict):
            raise ReceiptIntegrityError("stored receipt payload is not an object")
        if receipt.get("receipt_id") != receipt_id:
            raise ReceiptIntegrityError("stored receipt payload identity mismatch")
        if raw.get("correlation_id") != receipt.get("correlation_id"):
            raise ReceiptIntegrityError("stored receipt correlation mismatch")
        calculated = self._digest(_canonical_bytes(receipt))
        if calculated != raw.get("canonical_digest"):
            raise ReceiptIntegrityError("stored receipt digest mismatch")
        return MappingProxyType(receipt)

    def find_by_correlation(self, correlation_id: str, *, limit: int = 100) -> tuple[Mapping[str, Any], ...]:
        target = self._text(correlation_id, "correlation_id")
        if limit <= 0 or limit > 1000:
            raise InvalidReceiptError("limit must be between 1 and 1000")
        found: list[Mapping[str, Any]] = []
        for path in sorted(self._records.glob("*/*.json")):
            try:
                raw = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, json.JSONDecodeError) as exc:
                raise ReceiptIntegrityError(f"cannot scan receipt store: {exc}") from exc
            if raw.get("correlation_id") == target:
                found.append(self.get(self._text(raw.get("receipt_id"), "receipt_id")))
                if len(found) >= limit:
                    break
        return tuple(found)
