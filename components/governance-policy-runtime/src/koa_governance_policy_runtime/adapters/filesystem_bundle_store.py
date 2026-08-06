"""Filesystem persistence for immutable governance policy bundles.

The adapter owns only Governance Policy Runtime state. Bundle bytes are stored
immutably, candidate disposition is recorded separately, and the complete
active policy set is selected through one atomic state-file replacement. The
adapter never interprets policy semantics or treats a signature as sufficient
for activation.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import threading
from contextlib import contextmanager, suppress
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType
from typing import Any, Iterator, Mapping, Sequence

try:  # Linux is the target platform; keep import failure explicit on others.
    import fcntl
except ImportError:  # pragma: no cover - exercised only on non-POSIX hosts
    fcntl = None  # type: ignore[assignment]

_POLICY_ID = re.compile(r"^policy-bundle\.[a-z0-9]+(?:[._-][a-z0-9]+)*$")
_SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
_SCHEMA_REF = "contracts/artifact-contracts/policy-bundle.schema.json"
_STATE_FORMAT = "koa-governance-policy-set-state/v1"
_RECORD_FORMAT = "koa-governance-policy-bundle-record/v1"


class BundleStoreError(RuntimeError):
    """Base error for bounded policy-bundle persistence operations."""


class InvalidBundleError(BundleStoreError, ValueError):
    """The supplied bundle or transition metadata is invalid."""


class BundleNotFoundError(BundleStoreError):
    """A requested local bundle reference does not exist."""


class BundleConflictError(BundleStoreError):
    """The same immutable bundle reference was reused with different bytes."""


class PolicySetConflictError(BundleStoreError):
    """The requested activation conflicts with current policy-set state."""


class BundleStorageUnavailableError(BundleStoreError):
    """The owned filesystem state could not be accessed safely."""


class CandidateDisposition(StrEnum):
    STAGED = "staged"
    QUARANTINED = "quarantined"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class BundleRecord:
    bundle_ref: str
    artifact_id: str
    version: str
    canonical_digest: str
    byte_length: int
    disposition: CandidateDisposition
    verification_ref: str | None
    source_ref: str | None
    stored_at: datetime
    duplicate: bool = False


@dataclass(frozen=True, slots=True)
class PolicySetSnapshot:
    policy_set_ref: str | None
    bundle_refs: tuple[str, ...]
    previous_policy_set_ref: str | None
    previous_bundle_refs: tuple[str, ...]
    activation_receipt_ref: str | None
    activated_at: datetime | None
    generation: int


class FilesystemBundleStore:
    """Immutable bundle store with atomic complete-policy-set activation."""

    def __init__(self, root: str | Path, *, max_bundle_bytes: int = 16 * 1024 * 1024) -> None:
        self.root = Path(root)
        if max_bundle_bytes <= 0:
            raise ValueError("max_bundle_bytes must be positive")
        self.max_bundle_bytes = max_bundle_bytes
        self._thread_lock = threading.RLock()
        self._bundles = self.root / "bundles"
        self._state_dir = self.root / "state"
        self._state_path = self._state_dir / "active-policy-set.json"
        self._lock_path = self._state_dir / ".store.lock"
        self._initialize_layout()

    def _initialize_layout(self) -> None:
        try:
            self._bundles.mkdir(parents=True, exist_ok=True, mode=0o750)
            self._state_dir.mkdir(parents=True, exist_ok=True, mode=0o750)
            if not self._state_path.exists():
                try:
                    self._atomic_write_json(
                        self._state_path,
                        {
                            "format": _STATE_FORMAT,
                            "policy_set_ref": None,
                            "bundle_refs": [],
                            "previous_policy_set_ref": None,
                            "previous_bundle_refs": [],
                            "activation_receipt_ref": None,
                            "activated_at": None,
                            "generation": 0,
                        },
                        replace=False,
                    )
                except FileExistsError:
                    self._read_json(self._state_path)
        except OSError as exc:
            raise BundleStorageUnavailableError(f"cannot initialize bundle store: {exc}") from exc

    @contextmanager
    def _exclusive(self) -> Iterator[None]:
        with self._thread_lock:
            if fcntl is None:
                raise BundleStorageUnavailableError("POSIX file locking is required")
            try:
                descriptor = os.open(self._lock_path, os.O_RDWR | os.O_CREAT, 0o640)
                with os.fdopen(descriptor, "a+b", closefd=True) as lock_file:
                    fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
                    try:
                        yield
                    finally:
                        fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
            except OSError as exc:
                raise BundleStorageUnavailableError(f"cannot lock bundle store: {exc}") from exc

    @staticmethod
    def _text(value: Any, field: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise InvalidBundleError(f"{field} must be a non-empty string")
        return value.strip()

    @staticmethod
    def _timestamp(value: Any, field: str) -> datetime:
        if isinstance(value, datetime):
            parsed = value
        elif isinstance(value, str):
            try:
                parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError as exc:
                raise InvalidBundleError(f"{field} must be an RFC 3339 timestamp") from exc
        else:
            raise InvalidBundleError(f"{field} must be an RFC 3339 timestamp")
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            raise InvalidBundleError(f"{field} must include a timezone")
        return parsed.astimezone(timezone.utc)

    @staticmethod
    def _format_timestamp(value: datetime) -> str:
        return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

    @staticmethod
    def _canonical_bytes(value: Mapping[str, Any]) -> bytes:
        if not isinstance(value, Mapping):
            raise InvalidBundleError("policy bundle must be an object")
        try:
            encoded = json.dumps(
                dict(value), ensure_ascii=False, allow_nan=False, separators=(",", ":"), sort_keys=True
            ).encode("utf-8")
        except (TypeError, ValueError) as exc:
            raise InvalidBundleError("policy bundle must contain canonical JSON values") from exc
        return encoded

    @classmethod
    def _identity(cls, bundle: Mapping[str, Any]) -> tuple[str, str, str]:
        if bundle.get("$schema") != _SCHEMA_REF:
            raise InvalidBundleError(f"$schema must equal {_SCHEMA_REF}")
        if bundle.get("artifact_type") != "governance_policy_bundle":
            raise InvalidBundleError("artifact_type must equal governance_policy_bundle")
        if bundle.get("artifact_class") != "policy_bundle":
            raise InvalidBundleError("artifact_class must equal policy_bundle")
        if bundle.get("release_channel") != "governance":
            raise InvalidBundleError("release_channel must equal governance")
        artifact_id = cls._text(bundle.get("artifact_id"), "artifact_id")
        version = cls._text(bundle.get("version"), "version")
        if not _POLICY_ID.fullmatch(artifact_id):
            raise InvalidBundleError("artifact_id does not match the policy-bundle identifier contract")
        if not _SEMVER.fullmatch(version):
            raise InvalidBundleError("version must be semantic versioning")
        signatures = bundle.get("signatures")
        provenance = bundle.get("provenance")
        if not isinstance(signatures, list) or not signatures:
            raise InvalidBundleError("signed policy bundles require a non-empty signatures array")
        if not isinstance(provenance, Mapping):
            raise InvalidBundleError("policy bundles require provenance")
        return artifact_id, version, f"{artifact_id}@{version}"

    @staticmethod
    def _safe_component(value: str, field: str) -> str:
        if value in {".", ".."} or "/" in value or "\\" in value or "\x00" in value:
            raise InvalidBundleError(f"{field} contains an unsafe path component")
        return value

    def _bundle_dir(self, artifact_id: str, version: str) -> Path:
        return self._bundles / self._safe_component(artifact_id, "artifact_id") / self._safe_component(version, "version")

    @staticmethod
    def _digest(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def _read_json(path: Path) -> dict[str, Any]:
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            raise
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise BundleStorageUnavailableError(f"cannot read valid JSON from {path}: {exc}") from exc
        if not isinstance(raw, dict):
            raise BundleStorageUnavailableError(f"stored JSON root must be an object: {path}")
        return raw

    @staticmethod
    def _fsync_directory(path: Path) -> None:
        descriptor = os.open(path, os.O_RDONLY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)

    def _atomic_write_bytes(self, path: Path, data: bytes, *, replace: bool) -> None:
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o750)
        if path.exists() and not replace:
            raise FileExistsError(path)
        descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
        temporary = Path(temporary_name)
        try:
            os.fchmod(descriptor, 0o640)
            with os.fdopen(descriptor, "wb", closefd=True) as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            if not replace and path.exists():
                raise FileExistsError(path)
            os.replace(temporary, path)
            self._fsync_directory(path.parent)
        finally:
            if temporary.exists():
                temporary.unlink()

    def _atomic_write_json(self, path: Path, value: Mapping[str, Any], *, replace: bool) -> None:
        self._atomic_write_bytes(path, self._canonical_bytes(value) + b"\n", replace=replace)

    def _record_from_raw(self, raw: Mapping[str, Any], *, duplicate: bool = False) -> BundleRecord:
        try:
            disposition = CandidateDisposition(raw["disposition"])
            stored_at = self._timestamp(raw["stored_at"], "stored_at")
            return BundleRecord(
                bundle_ref=self._text(raw["bundle_ref"], "bundle_ref"),
                artifact_id=self._text(raw["artifact_id"], "artifact_id"),
                version=self._text(raw["version"], "version"),
                canonical_digest=self._text(raw["canonical_digest"], "canonical_digest"),
                byte_length=int(raw["byte_length"]),
                disposition=disposition,
                verification_ref=(
                    self._text(raw["verification_ref"], "verification_ref")
                    if raw.get("verification_ref") is not None else None
                ),
                source_ref=(
                    self._text(raw["source_ref"], "source_ref")
                    if raw.get("source_ref") is not None else None
                ),
                stored_at=stored_at,
                duplicate=duplicate,
            )
        except (KeyError, TypeError, ValueError) as exc:
            if isinstance(exc, InvalidBundleError):
                raise
            raise BundleStorageUnavailableError("stored bundle record is malformed") from exc

    def stage_bundle(
        self,
        bundle: Mapping[str, Any],
        *,
        stored_at: datetime,
        verification_ref: str,
        source_ref: str | None = None,
        expected_digest: str | None = None,
        disposition: CandidateDisposition | str = CandidateDisposition.STAGED,
    ) -> BundleRecord:
        selected = CandidateDisposition(disposition)
        canonical = self._canonical_bytes(bundle)
        if len(canonical) > self.max_bundle_bytes:
            raise InvalidBundleError("policy bundle exceeds the configured size limit")
        artifact_id, version, bundle_ref = self._identity(bundle)
        digest = self._digest(canonical)
        if expected_digest is not None and expected_digest != digest:
            raise BundleConflictError("expected digest does not match canonical bundle bytes")
        timestamp = self._timestamp(stored_at, "stored_at")
        verification = self._text(verification_ref, "verification_ref")
        source = self._text(source_ref, "source_ref") if source_ref is not None else None
        directory = self._bundle_dir(artifact_id, version)
        bundle_path = directory / "bundle.json"
        record_path = directory / "record.json"
        record_raw = {
            "format": _RECORD_FORMAT,
            "bundle_ref": bundle_ref,
            "artifact_id": artifact_id,
            "version": version,
            "canonical_digest": digest,
            "byte_length": len(canonical),
            "disposition": selected.value,
            "verification_ref": verification,
            "source_ref": source,
            "stored_at": self._format_timestamp(timestamp),
        }
        with self._exclusive():
            if bundle_path.exists() or record_path.exists():
                if not (bundle_path.exists() and record_path.exists()):
                    raise BundleStorageUnavailableError("partial immutable bundle record detected")
                existing_bytes = bundle_path.read_bytes()
                existing = self._record_from_raw(self._read_json(record_path), duplicate=True)
                if self._digest(existing_bytes.rstrip(b"\n")) != digest or existing.canonical_digest != digest:
                    raise BundleConflictError("bundle reference already exists with different bytes")
                return existing
            try:
                directory.mkdir(parents=True, exist_ok=False, mode=0o750)
                self._atomic_write_bytes(bundle_path, canonical + b"\n", replace=False)
                self._atomic_write_json(record_path, record_raw, replace=False)
            except Exception:
                for path in (record_path, bundle_path):
                    if path.exists():
                        path.unlink()
                with suppress(OSError):
                    directory.rmdir()
                raise
        return self._record_from_raw(record_raw)

    def quarantine_bundle(self, bundle: Mapping[str, Any], **kwargs: Any) -> BundleRecord:
        return self.stage_bundle(bundle, disposition=CandidateDisposition.QUARANTINED, **kwargs)

    def admit_staged(self, bundle_ref: str, *, verification_ref: str, admitted_at: datetime) -> BundleRecord:
        """Promote a quarantined candidate after an external complete verification."""
        artifact_id, version = self._split_ref(bundle_ref)
        record_path = self._bundle_dir(artifact_id, version) / "record.json"
        with self._exclusive():
            try:
                raw = self._read_json(record_path)
            except FileNotFoundError as exc:
                raise BundleNotFoundError(bundle_ref) from exc
            current = self._record_from_raw(raw)
            verification = self._text(verification_ref, "verification_ref")
            if current.disposition is CandidateDisposition.REJECTED:
                raise PolicySetConflictError("a rejected bundle cannot be staged")
            if current.disposition is CandidateDisposition.STAGED:
                if current.verification_ref != verification:
                    raise PolicySetConflictError("staged verification reference is immutable")
                return current
            raw["disposition"] = CandidateDisposition.STAGED.value
            raw["verification_ref"] = verification
            raw["admitted_at"] = self._format_timestamp(self._timestamp(admitted_at, "admitted_at"))
            self._atomic_write_json(record_path, raw, replace=True)
            return self._record_from_raw(raw)

    @staticmethod
    def _split_ref(bundle_ref: str) -> tuple[str, str]:
        if not isinstance(bundle_ref, str) or bundle_ref.count("@") != 1:
            raise InvalidBundleError("bundle_ref must be artifact_id@version")
        artifact_id, version = bundle_ref.split("@", 1)
        if not _POLICY_ID.fullmatch(artifact_id) or not _SEMVER.fullmatch(version):
            raise InvalidBundleError("bundle_ref does not match the policy bundle contract")
        return artifact_id, version

    def get_bundle(self, bundle_ref: str) -> Mapping[str, Any]:
        artifact_id, version = self._split_ref(bundle_ref)
        directory = self._bundle_dir(artifact_id, version)
        try:
            raw_bytes = (directory / "bundle.json").read_bytes()
            record = self._record_from_raw(self._read_json(directory / "record.json"))
        except FileNotFoundError as exc:
            raise BundleNotFoundError(bundle_ref) from exc
        except OSError as exc:
            raise BundleStorageUnavailableError(f"cannot read bundle {bundle_ref}: {exc}") from exc
        canonical = raw_bytes.rstrip(b"\n")
        if (record.bundle_ref, record.artifact_id, record.version) != (bundle_ref, artifact_id, version):
            raise BundleStorageUnavailableError(f"stored bundle record identity mismatch: {bundle_ref}")
        if self._digest(canonical) != record.canonical_digest:
            raise BundleStorageUnavailableError(f"bundle integrity verification failed: {bundle_ref}")
        try:
            value = json.loads(canonical)
        except (UnicodeError, json.JSONDecodeError) as exc:
            raise BundleStorageUnavailableError(f"stored bundle is invalid JSON: {bundle_ref}") from exc
        if not isinstance(value, dict):
            raise BundleStorageUnavailableError(f"stored bundle root is not an object: {bundle_ref}")
        artifact_id_read, version_read, ref_read = self._identity(value)
        if (artifact_id_read, version_read, ref_read) != (artifact_id, version, bundle_ref):
            raise BundleStorageUnavailableError(f"stored bundle identity mismatch: {bundle_ref}")
        return MappingProxyType(value)

    def get_record(self, bundle_ref: str) -> BundleRecord:
        artifact_id, version = self._split_ref(bundle_ref)
        try:
            record = self._record_from_raw(
                self._read_json(self._bundle_dir(artifact_id, version) / "record.json")
            )
        except FileNotFoundError as exc:
            raise BundleNotFoundError(bundle_ref) from exc
        if (record.bundle_ref, record.artifact_id, record.version) != (bundle_ref, artifact_id, version):
            raise BundleStorageUnavailableError(f"stored bundle record identity mismatch: {bundle_ref}")
        return record

    def list_records(self) -> tuple[BundleRecord, ...]:
        records: list[BundleRecord] = []
        if not self._bundles.exists():
            return ()
        for path in sorted(self._bundles.glob("*/*/record.json")):
            records.append(self._record_from_raw(self._read_json(path)))
        return tuple(records)

    def _read_state(self) -> dict[str, Any]:
        try:
            raw = self._read_json(self._state_path)
        except FileNotFoundError as exc:
            raise BundleStorageUnavailableError("active policy-set state is missing") from exc
        if raw.get("format") != _STATE_FORMAT:
            raise BundleStorageUnavailableError("active policy-set state format mismatch")
        generation = raw.get("generation")
        if not isinstance(generation, int) or isinstance(generation, bool) or generation < 0:
            raise BundleStorageUnavailableError("active policy-set generation is invalid")
        for ref_field, bundles_field in (
            ("policy_set_ref", "bundle_refs"),
            ("previous_policy_set_ref", "previous_bundle_refs"),
        ):
            ref = raw.get(ref_field)
            refs = raw.get(bundles_field)
            if ref is not None and (not isinstance(ref, str) or not ref.strip()):
                raise BundleStorageUnavailableError(f"{ref_field} is invalid")
            if not isinstance(refs, list) or any(not isinstance(item, str) for item in refs):
                raise BundleStorageUnavailableError(f"{bundles_field} is invalid")
            if len(refs) != len(set(refs)):
                raise BundleStorageUnavailableError(f"{bundles_field} contains duplicates")
            if (ref is None) != (len(refs) == 0):
                raise BundleStorageUnavailableError(f"{ref_field} and {bundles_field} are inconsistent")
            for bundle_ref in refs:
                try:
                    self._split_ref(bundle_ref)
                except InvalidBundleError as exc:
                    raise BundleStorageUnavailableError(
                        f"{bundles_field} contains an invalid bundle reference"
                    ) from exc
        if raw.get("policy_set_ref") is None:
            if raw.get("activation_receipt_ref") is not None or raw.get("activated_at") is not None:
                raise BundleStorageUnavailableError("empty policy state has activation metadata")
        else:
            if not isinstance(raw.get("activation_receipt_ref"), str):
                raise BundleStorageUnavailableError("active policy state lacks receipt reference")
            self._timestamp(raw.get("activated_at"), "activated_at")
        return raw

    def current_policy_set(self) -> PolicySetSnapshot:
        raw = self._read_state()
        activated = raw.get("activated_at")
        return PolicySetSnapshot(
            policy_set_ref=raw.get("policy_set_ref"),
            bundle_refs=tuple(raw.get("bundle_refs", ())),
            previous_policy_set_ref=raw.get("previous_policy_set_ref"),
            previous_bundle_refs=tuple(raw.get("previous_bundle_refs", ())),
            activation_receipt_ref=raw.get("activation_receipt_ref"),
            activated_at=self._timestamp(activated, "activated_at") if activated else None,
            generation=int(raw.get("generation", 0)),
        )

    def activate_policy_set(
        self,
        policy_set_ref: str,
        bundle_refs: Sequence[str],
        *,
        activation_receipt_ref: str,
        activated_at: datetime,
        expected_current_policy_set_ref: str | None,
    ) -> PolicySetSnapshot:
        selected_ref = self._text(policy_set_ref, "policy_set_ref")
        receipt_ref = self._text(activation_receipt_ref, "activation_receipt_ref")
        when = self._timestamp(activated_at, "activated_at")
        refs = tuple(bundle_refs)
        if not refs or len(refs) != len(set(refs)):
            raise InvalidBundleError("bundle_refs must be a non-empty unique sequence")
        for bundle_ref in refs:
            record = self.get_record(bundle_ref)
            if record.disposition is not CandidateDisposition.STAGED:
                raise PolicySetConflictError(f"bundle is not staged: {bundle_ref}")
            self.get_bundle(bundle_ref)
        with self._exclusive():
            current = self._read_state()
            if current.get("policy_set_ref") != expected_current_policy_set_ref:
                raise PolicySetConflictError("active policy set changed before activation")
            next_state = {
                "format": _STATE_FORMAT,
                "policy_set_ref": selected_ref,
                "bundle_refs": list(refs),
                "previous_policy_set_ref": current.get("policy_set_ref"),
                "previous_bundle_refs": list(current.get("bundle_refs", [])),
                "activation_receipt_ref": receipt_ref,
                "activated_at": self._format_timestamp(when),
                "generation": int(current.get("generation", 0)) + 1,
            }
            self._atomic_write_json(self._state_path, next_state, replace=True)
        return self.current_policy_set()

    def rollback_policy_set(
        self,
        *,
        rollback_receipt_ref: str,
        rolled_back_at: datetime,
        expected_current_policy_set_ref: str,
    ) -> PolicySetSnapshot:
        receipt_ref = self._text(rollback_receipt_ref, "rollback_receipt_ref")
        when = self._timestamp(rolled_back_at, "rolled_back_at")
        with self._exclusive():
            current = self._read_state()
            if current.get("policy_set_ref") != expected_current_policy_set_ref:
                raise PolicySetConflictError("active policy set changed before rollback")
            previous_ref = current.get("previous_policy_set_ref")
            previous_bundles = tuple(current.get("previous_bundle_refs", ()))
            if not previous_ref or not previous_bundles:
                raise PolicySetConflictError("no previous valid complete policy set is available")
            for bundle_ref in previous_bundles:
                self.get_bundle(bundle_ref)
            next_state = {
                "format": _STATE_FORMAT,
                "policy_set_ref": previous_ref,
                "bundle_refs": list(previous_bundles),
                "previous_policy_set_ref": current.get("policy_set_ref"),
                "previous_bundle_refs": list(current.get("bundle_refs", [])),
                "activation_receipt_ref": receipt_ref,
                "activated_at": self._format_timestamp(when),
                "generation": int(current.get("generation", 0)) + 1,
            }
            self._atomic_write_json(self._state_path, next_state, replace=True)
        return self.current_policy_set()
