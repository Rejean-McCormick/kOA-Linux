"""Immutable filesystem persistence for publication receipts and state changes."""

from __future__ import annotations

import fcntl
import hashlib
import json
import os
import re
import tempfile
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{2,199}$")
_STORE_FORMAT = "koa-publication-receipt-store/v1"


class ReceiptStoreError(RuntimeError):
    """Base error for local receipt persistence."""


class InvalidReceiptError(ReceiptStoreError, ValueError):
    """A receipt or change record violates a local invariant."""


class ReceiptConflictError(ReceiptStoreError):
    """An immutable identity or idempotency key was reused inconsistently."""


class ReceiptNotFoundError(ReceiptStoreError):
    """A requested receipt does not exist."""


class ReceiptIntegrityError(ReceiptStoreError):
    """Stored bytes no longer match their integrity envelope."""


class ReceiptStorageUnavailable(ReceiptStoreError):
    """The filesystem could not complete an atomic persistence operation."""


@dataclass(frozen=True, slots=True)
class StoredReceipt:
    receipt_id: str
    request_id: str
    idempotency_key: str
    digest: str
    byte_length: int
    storage_key: str
    recorded_at: datetime
    receipt: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class StoredPublicationChange:
    change_id: str
    receipt_id: str
    change_class: str
    digest: str
    storage_key: str
    recorded_at: datetime
    change: Mapping[str, Any]


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InvalidReceiptError(f"{field} must be a non-empty string")
    normalized = value.strip()
    if not _IDENTIFIER.fullmatch(normalized):
        raise InvalidReceiptError(f"{field} contains unsupported characters")
    return normalized


def _utc(value: datetime, field: str) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise InvalidReceiptError(f"{field} must be a timezone-aware datetime")
    return value.astimezone(timezone.utc)


def _timestamp(value: datetime, field: str) -> str:
    return _utc(value, field).isoformat().replace("+00:00", "Z")


def _parse_time(value: Any, field: str) -> datetime:
    if not isinstance(value, str):
        raise ReceiptIntegrityError(f"stored {field} is not a timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ReceiptIntegrityError(f"stored {field} is invalid") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ReceiptIntegrityError(f"stored {field} lacks timezone")
    return parsed.astimezone(timezone.utc)


def _canonical(value: Mapping[str, Any]) -> tuple[bytes, str]:
    try:
        raw = json.dumps(
            dict(value),
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise InvalidReceiptError("record must contain JSON-compatible values") from exc
    return raw, "sha256:" + hashlib.sha256(raw).hexdigest()


class FilesystemReceiptStore:
    """Persist immutable receipts before callers report terminal success."""

    def __init__(self, root: str | Path, *, max_record_bytes: int = 4 * 1024 * 1024) -> None:
        if max_record_bytes <= 0:
            raise ValueError("max_record_bytes must be positive")
        self._root = Path(root)
        self._max_record_bytes = max_record_bytes
        self._receipts = self._root / "receipts"
        self._changes = self._root / "changes"
        self._idempotency = self._root / "idempotency"
        try:
            for path in (self._root, self._receipts, self._changes, self._idempotency):
                path.mkdir(parents=True, exist_ok=True, mode=0o750)
                if path.is_symlink():
                    raise ReceiptStorageUnavailable("store paths cannot be symbolic links")
        except OSError as exc:
            raise ReceiptStorageUnavailable(f"cannot initialize receipt store: {exc}") from exc

    @staticmethod
    def _validate_receipt(receipt: Mapping[str, Any]) -> tuple[str, str]:
        if not isinstance(receipt, Mapping):
            raise InvalidReceiptError("receipt must be an object")
        if receipt.get("artifact_class") != "publication_receipt":
            raise InvalidReceiptError("artifact_class must be publication_receipt")
        receipt_id = _text(receipt.get("receipt_id"), "receipt_id")
        request = receipt.get("request")
        if not isinstance(request, Mapping):
            raise InvalidReceiptError("receipt request binding must be an object")
        request_id = _text(request.get("request_id"), "request.request_id")
        _text(request.get("idempotency_key"), "request.idempotency_key")
        if receipt.get("record_status") not in {"issued", "superseded"}:
            raise InvalidReceiptError("receipt record_status is unsupported")
        execution = receipt.get("execution")
        if not isinstance(execution, Mapping):
            raise InvalidReceiptError("receipt execution must be an object")
        publication_state = receipt.get("publication_state")
        if not isinstance(publication_state, Mapping):
            raise InvalidReceiptError("receipt publication_state must be an object")
        if execution.get("result") == "published" and publication_state.get("state") != "active":
            raise InvalidReceiptError("published execution requires active publication_state")
        evidence = receipt.get("evidence")
        if not isinstance(evidence, Mapping):
            raise InvalidReceiptError("receipt evidence must be an object")
        if evidence.get("source_content_in_public_evidence") is not False:
            raise InvalidReceiptError("public evidence must exclude source content")
        if evidence.get("private_identity_in_public_evidence") is not False:
            raise InvalidReceiptError("public evidence must exclude private identity")
        return receipt_id, request_id

    def store_receipt(
        self,
        *,
        receipt: Mapping[str, Any],
        idempotency_key: str,
        recorded_at: datetime,
    ) -> StoredReceipt:
        receipt_id, request_id = self._validate_receipt(receipt)
        key = _text(idempotency_key, "idempotency_key")
        request_binding = receipt.get("request")
        if not isinstance(request_binding, Mapping) or request_binding.get("idempotency_key") != key:
            raise InvalidReceiptError("receipt request idempotency_key does not match store key")
        when = _utc(recorded_at, "recorded_at")
        raw, digest = _canonical(receipt)
        if len(raw) > self._max_record_bytes:
            raise InvalidReceiptError("receipt exceeds max_record_bytes")
        receipt_path = self._receipts / f"{hashlib.sha256(receipt_id.encode('utf-8')).hexdigest()}.json"
        index_path = self._idempotency / f"{hashlib.sha256(key.encode('utf-8')).hexdigest()}.json"
        envelope = {
            "format": _STORE_FORMAT,
            "record_class": "publication_receipt",
            "receipt_id": receipt_id,
            "request_id": request_id,
            "idempotency_key": key,
            "recorded_at": _timestamp(when, "recorded_at"),
            "digest": digest,
            "byte_length": len(raw),
            "receipt": dict(receipt),
        }
        index = {
            "format": _STORE_FORMAT,
            "record_class": "idempotency_binding",
            "idempotency_key": key,
            "receipt_id": receipt_id,
            "request_id": request_id,
            "digest": digest,
            "recorded_at": envelope["recorded_at"],
        }
        with self._exclusive_lock():
            existing = self._read_envelope(receipt_path, missing_ok=True)
            idempotency = self._read_envelope(index_path, missing_ok=True)
            if existing is not None and (
                existing.get("digest") != digest or existing.get("idempotency_key") != key
            ):
                raise ReceiptConflictError("receipt identity already stores different content")
            if idempotency is not None and (
                idempotency.get("receipt_id") != receipt_id or idempotency.get("digest") != digest
            ):
                raise ReceiptConflictError("idempotency key was reused with different semantics")
            created_receipt = False
            created_index = False
            try:
                if existing is None:
                    self._atomic_create(receipt_path, envelope)
                    created_receipt = True
                if idempotency is None:
                    self._atomic_create(index_path, index)
                    created_index = True
            except (OSError, ReceiptConflictError) as exc:
                if created_index:
                    index_path.unlink(missing_ok=True)
                if created_receipt:
                    receipt_path.unlink(missing_ok=True)
                if isinstance(exc, ReceiptConflictError):
                    raise
                raise ReceiptStorageUnavailable(f"cannot store receipt: {exc}") from exc
        return self.get_receipt(receipt_id)

    def get_receipt(self, receipt_id: str) -> StoredReceipt:
        normalized = _text(receipt_id, "receipt_id")
        path = self._receipts / f"{hashlib.sha256(normalized.encode('utf-8')).hexdigest()}.json"
        envelope = self._read_envelope(path, missing_ok=True)
        if envelope is None:
            raise ReceiptNotFoundError(normalized)
        return self._stored_receipt(envelope, path)

    def append_change(
        self,
        *,
        receipt_id: str,
        change: Mapping[str, Any],
        recorded_at: datetime,
    ) -> StoredPublicationChange:
        parent = self.get_receipt(receipt_id)
        if not isinstance(change, Mapping):
            raise InvalidReceiptError("change must be an object")
        change_id = _text(change.get("change_id"), "change_id")
        change_class = _text(change.get("change_class"), "change_class")
        if change.get("historical_receipt_preserved") is not True:
            raise InvalidReceiptError("change must preserve the historical receipt")
        if change.get("affected_future_operations_stopped") is not True:
            raise InvalidReceiptError("change must stop affected future operations")
        when = _utc(recorded_at, "recorded_at")
        raw, digest = _canonical(change)
        if len(raw) > self._max_record_bytes:
            raise InvalidReceiptError("change exceeds max_record_bytes")
        directory = self._changes / hashlib.sha256(parent.receipt_id.encode("utf-8")).hexdigest()
        try:
            directory.mkdir(parents=True, exist_ok=True, mode=0o750)
            if directory.is_symlink():
                raise ReceiptStorageUnavailable("change directory cannot be a symbolic link")
        except OSError as exc:
            raise ReceiptStorageUnavailable(f"cannot initialize change directory: {exc}") from exc
        path = directory / f"{hashlib.sha256(change_id.encode('utf-8')).hexdigest()}.json"
        envelope = {
            "format": _STORE_FORMAT,
            "record_class": "publication_change",
            "change_id": change_id,
            "receipt_id": parent.receipt_id,
            "change_class": change_class,
            "recorded_at": _timestamp(when, "recorded_at"),
            "digest": digest,
            "byte_length": len(raw),
            "change": dict(change),
        }
        existing = self._read_envelope(path, missing_ok=True)
        if existing is not None:
            if existing.get("digest") != digest:
                raise ReceiptConflictError("change identity already stores different content")
            return self._stored_change(existing, path)
        try:
            self._atomic_create(path, envelope)
        except ReceiptConflictError:
            existing = self._read_envelope(path, missing_ok=False)
            if existing is None or existing.get("digest") != digest:
                raise
        except OSError as exc:
            raise ReceiptStorageUnavailable(f"cannot store publication change: {exc}") from exc
        stored = self._read_envelope(path, missing_ok=False)
        if stored is None:
            raise ReceiptStorageUnavailable("publication change disappeared after write")
        return self._stored_change(stored, path)

    def list_changes(self, receipt_id: str) -> tuple[StoredPublicationChange, ...]:
        parent = self.get_receipt(receipt_id)
        directory = self._changes / hashlib.sha256(parent.receipt_id.encode("utf-8")).hexdigest()
        if not directory.exists():
            return ()
        try:
            paths = sorted(path for path in directory.iterdir() if path.suffix == ".json")
        except OSError as exc:
            raise ReceiptStorageUnavailable(f"cannot list publication changes: {exc}") from exc
        result: list[StoredPublicationChange] = []
        for path in paths:
            envelope = self._read_envelope(path, missing_ok=False)
            if envelope is None:
                raise ReceiptStorageUnavailable("publication change disappeared while listing")
            result.append(self._stored_change(envelope, path))
        result.sort(key=lambda item: (item.recorded_at, item.change_id))
        return tuple(result)

    @contextmanager
    def _exclusive_lock(self):
        lock_path = self._root / ".store.lock"
        try:
            descriptor = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o640)
            with os.fdopen(descriptor, "a+b", closefd=True) as stream:
                fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
                try:
                    yield
                finally:
                    fcntl.flock(stream.fileno(), fcntl.LOCK_UN)
        except OSError as exc:
            raise ReceiptStorageUnavailable(f"cannot lock receipt store: {exc}") from exc

    def _stored_receipt(self, envelope: Mapping[str, Any], path: Path) -> StoredReceipt:
        receipt = envelope.get("receipt")
        if not isinstance(receipt, Mapping):
            raise ReceiptIntegrityError("stored receipt payload is invalid")
        raw, digest = _canonical(receipt)
        if envelope.get("digest") != digest or envelope.get("byte_length") != len(raw):
            raise ReceiptIntegrityError("stored receipt integrity check failed")
        receipt_id, request_id = self._validate_receipt(receipt)
        if envelope.get("receipt_id") != receipt_id or envelope.get("request_id") != request_id:
            raise ReceiptIntegrityError("stored receipt identity mismatch")
        idempotency_key = envelope.get("idempotency_key")
        if not isinstance(idempotency_key, str) or not idempotency_key:
            raise ReceiptIntegrityError("stored receipt idempotency key is invalid")
        return StoredReceipt(
            receipt_id=receipt_id,
            request_id=request_id,
            idempotency_key=idempotency_key,
            digest=digest,
            byte_length=len(raw),
            storage_key=str(path.relative_to(self._root)),
            recorded_at=_parse_time(envelope.get("recorded_at"), "recorded_at"),
            receipt=MappingProxyType(dict(receipt)),
        )

    def _stored_change(self, envelope: Mapping[str, Any], path: Path) -> StoredPublicationChange:
        change = envelope.get("change")
        if not isinstance(change, Mapping):
            raise ReceiptIntegrityError("stored change payload is invalid")
        raw, digest = _canonical(change)
        if envelope.get("digest") != digest or envelope.get("byte_length") != len(raw):
            raise ReceiptIntegrityError("stored change integrity check failed")
        change_id = _text(change.get("change_id"), "change_id")
        receipt_id = _text(envelope.get("receipt_id"), "receipt_id")
        change_class = _text(change.get("change_class"), "change_class")
        if envelope.get("change_id") != change_id or envelope.get("change_class") != change_class:
            raise ReceiptIntegrityError("stored change identity mismatch")
        return StoredPublicationChange(
            change_id=change_id,
            receipt_id=receipt_id,
            change_class=change_class,
            digest=digest,
            storage_key=str(path.relative_to(self._root)),
            recorded_at=_parse_time(envelope.get("recorded_at"), "recorded_at"),
            change=MappingProxyType(dict(change)),
        )

    def _read_envelope(self, path: Path, *, missing_ok: bool) -> Mapping[str, Any] | None:
        try:
            if path.is_symlink():
                raise ReceiptIntegrityError("stored record cannot be a symbolic link")
            raw = path.read_bytes()
        except FileNotFoundError:
            if missing_ok:
                return None
            raise ReceiptNotFoundError(path.stem)
        except OSError as exc:
            raise ReceiptStorageUnavailable(f"cannot read stored record: {exc}") from exc
        if len(raw) > self._max_record_bytes * 2:
            raise ReceiptIntegrityError("stored envelope exceeds the configured limit")
        try:
            value = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ReceiptIntegrityError("stored record is not valid UTF-8 JSON") from exc
        if not isinstance(value, Mapping) or value.get("format") != _STORE_FORMAT:
            raise ReceiptIntegrityError("stored record envelope is invalid")
        return value

    @staticmethod
    def _atomic_create(path: Path, value: Mapping[str, Any]) -> None:
        encoded = (
            json.dumps(
                dict(value),
                ensure_ascii=False,
                allow_nan=False,
                indent=2,
                sort_keys=True,
            )
            + "\n"
        ).encode("utf-8")
        descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
        temporary = Path(temporary_name)
        try:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(encoded)
                stream.flush()
                os.fsync(stream.fileno())
            os.chmod(temporary, 0o640)
            try:
                os.link(temporary, path)
            except FileExistsError as exc:
                raise ReceiptConflictError(f"record already exists: {path.name}") from exc
            directory_fd = os.open(path.parent, os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        finally:
            temporary.unlink(missing_ok=True)
