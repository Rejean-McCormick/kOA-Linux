"""Content-addressed managed blob storage for the kOA Mediatheque."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import re
import stat
import tempfile
from typing import BinaryIO, Final


class BlobStoreError(RuntimeError):
    """Base class for managed-content storage failures."""


class BlobIntegrityError(BlobStoreError):
    """Raised when bytes do not match their declared integrity identity."""


@dataclass(frozen=True, slots=True)
class StoredBlob:
    storage_ref: str
    algorithm: str
    digest: str
    size_bytes: int


_ALGORITHMS: Final = {"sha256": 64, "sha384": 96, "sha512": 128}
_REF_RE = re.compile(r"^koa-blob://(sha256|sha384|sha512)/([0-9a-f]+)$")


class FilesystemBlobStore:
    """Store immutable blobs under a component-owned content root.

    The public reference is content-addressed and deterministic. Staging files are
    private implementation details and never become record authority.
    """

    def __init__(self, root: str | os.PathLike[str], *, max_blob_bytes: int) -> None:
        if max_blob_bytes < 1:
            raise ValueError("max_blob_bytes must be positive")
        self.root = Path(root).expanduser().resolve(strict=False)
        self.max_blob_bytes = max_blob_bytes
        self._blob_root = self.root / "blobs"
        self._stage_root = self.root / "staging"
        self._quarantine_root = self.root / "quarantine"
        for path in (self.root, self._blob_root, self._stage_root, self._quarantine_root):
            path.mkdir(mode=0o700, parents=True, exist_ok=True)
            if path.is_symlink():
                raise BlobStoreError(f"managed storage directory is a symlink: {path}")
            os.chmod(path, 0o700)

    def put_bytes(
        self,
        data: bytes,
        *,
        algorithm: str = "sha256",
        expected_digest: str | None = None,
    ) -> StoredBlob:
        from io import BytesIO

        return self.put_stream(
            BytesIO(data), algorithm=algorithm, expected_digest=expected_digest
        )

    def put_stream(
        self,
        stream: BinaryIO,
        *,
        algorithm: str = "sha256",
        expected_digest: str | None = None,
        chunk_size: int = 1024 * 1024,
    ) -> StoredBlob:
        algorithm = self._validate_algorithm(algorithm)
        if chunk_size < 4096 or chunk_size > 16 * 1024 * 1024:
            raise ValueError("chunk_size is outside the allowed range")
        if expected_digest is not None:
            self._validate_digest(algorithm, expected_digest)

        hasher = hashlib.new(algorithm)
        size = 0
        descriptor, temporary_name = tempfile.mkstemp(prefix="blob-", dir=self._stage_root)
        temporary = Path(temporary_name)
        try:
            os.fchmod(descriptor, 0o600)
            with os.fdopen(descriptor, "wb", closefd=True) as target:
                while True:
                    chunk = stream.read(chunk_size)
                    if not chunk:
                        break
                    if not isinstance(chunk, (bytes, bytearray, memoryview)):
                        raise BlobStoreError("blob stream returned non-binary data")
                    size += len(chunk)
                    if size > self.max_blob_bytes:
                        raise BlobStoreError("blob exceeds the active profile limit")
                    target.write(chunk)
                    hasher.update(chunk)
                target.flush()
                os.fsync(target.fileno())
            digest = hasher.hexdigest()
            if expected_digest is not None and digest != expected_digest:
                quarantine = self._quarantine_root / temporary.name
                os.replace(temporary, quarantine)
                os.chmod(quarantine, 0o600)
                raise BlobIntegrityError("blob digest does not match expected integrity")
            destination = self._path_for(algorithm, digest, create_parent=True)
            if destination.exists():
                temporary.unlink(missing_ok=True)
                if not self.verify(self.make_ref(algorithm, digest)):
                    raise BlobIntegrityError("existing content-addressed blob is corrupt")
            else:
                os.replace(temporary, destination)
                os.chmod(destination, 0o600)
                self._fsync_directory(destination.parent)
            return StoredBlob(
                storage_ref=self.make_ref(algorithm, digest),
                algorithm=algorithm,
                digest=digest,
                size_bytes=size,
            )
        except Exception:
            temporary.unlink(missing_ok=True)
            raise

    def open(self, storage_ref: str) -> BinaryIO:
        algorithm, digest = self.parse_ref(storage_ref)
        path = self._path_for(algorithm, digest)
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        try:
            descriptor = os.open(path, flags)
        except OSError as exc:
            raise BlobStoreError("managed blob cannot be opened safely") from exc
        try:
            metadata = os.fstat(descriptor)
            if not stat.S_ISREG(metadata.st_mode):
                raise BlobStoreError("managed blob reference is not a regular file")
            if metadata.st_size > self.max_blob_bytes:
                raise BlobStoreError("managed blob exceeds the active profile limit")
            if metadata.st_mode & 0o077:
                raise BlobStoreError("managed blob permissions are too broad")
            resolved = path.resolve(strict=True)
            if not resolved.is_relative_to(self._blob_root):
                raise BlobStoreError("managed blob escapes storage root")
            return os.fdopen(descriptor, "rb", closefd=True)
        except Exception:
            os.close(descriptor)
            raise

    def iter_bytes(self, storage_ref: str, *, chunk_size: int = 1024 * 1024) -> Iterator[bytes]:
        if chunk_size < 4096 or chunk_size > 16 * 1024 * 1024:
            raise ValueError("chunk_size is outside the allowed range")
        with self.open(storage_ref) as source:
            while chunk := source.read(chunk_size):
                yield chunk

    def read_bytes(self, storage_ref: str, *, maximum_bytes: int | None = None) -> bytes:
        limit = self.max_blob_bytes if maximum_bytes is None else maximum_bytes
        if limit < 0 or limit > self.max_blob_bytes:
            raise ValueError("maximum_bytes exceeds the active profile limit")
        result = bytearray()
        for chunk in self.iter_bytes(storage_ref):
            result.extend(chunk)
            if len(result) > limit:
                raise BlobStoreError("blob exceeds the requested read limit")
        return bytes(result)

    def exists(self, storage_ref: str) -> bool:
        try:
            algorithm, digest = self.parse_ref(storage_ref)
            path = self._path_for(algorithm, digest)
            self._assert_regular_managed_file(path)
            return True
        except (BlobStoreError, FileNotFoundError):
            return False

    def verify(self, storage_ref: str) -> bool:
        algorithm, digest = self.parse_ref(storage_ref)
        hasher = hashlib.new(algorithm)
        try:
            for chunk in self.iter_bytes(storage_ref):
                hasher.update(chunk)
        except FileNotFoundError:
            return False
        return hasher.hexdigest() == digest

    def remove_unreferenced(self, storage_ref: str, *, expected_digest: str) -> None:
        """Remove a blob only after its caller has proven it is unreferenced."""
        algorithm, digest = self.parse_ref(storage_ref)
        if digest != expected_digest:
            raise BlobIntegrityError("deletion digest does not match storage reference")
        path = self._path_for(algorithm, digest)
        self._assert_regular_managed_file(path)
        path.unlink()
        self._fsync_directory(path.parent)

    @staticmethod
    def make_ref(algorithm: str, digest: str) -> str:
        algorithm = FilesystemBlobStore._validate_algorithm(algorithm)
        FilesystemBlobStore._validate_digest(algorithm, digest)
        return f"koa-blob://{algorithm}/{digest}"

    @staticmethod
    def parse_ref(storage_ref: str) -> tuple[str, str]:
        match = _REF_RE.fullmatch(storage_ref)
        if match is None:
            raise BlobStoreError("invalid managed blob reference")
        algorithm, digest = match.groups()
        FilesystemBlobStore._validate_digest(algorithm, digest)
        return algorithm, digest

    @staticmethod
    def _validate_algorithm(algorithm: str) -> str:
        if algorithm not in _ALGORITHMS:
            raise BlobStoreError(f"unsupported digest algorithm: {algorithm!r}")
        return algorithm

    @staticmethod
    def _validate_digest(algorithm: str, digest: str) -> None:
        expected_length = _ALGORITHMS.get(algorithm)
        if expected_length is None or not re.fullmatch(r"[0-9a-f]+", digest):
            raise BlobStoreError("invalid digest")
        if len(digest) != expected_length:
            raise BlobStoreError("digest length does not match algorithm")

    def _path_for(self, algorithm: str, digest: str, *, create_parent: bool = False) -> Path:
        self._validate_digest(algorithm, digest)
        parent = self._blob_root / algorithm / digest[:2]
        if create_parent:
            parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            if parent.is_symlink():
                raise BlobStoreError("blob directory is a symlink")
            os.chmod(parent, 0o700)
        candidate = parent / digest
        resolved_parent = parent.resolve(strict=False)
        if not resolved_parent.is_relative_to(self._blob_root):
            raise BlobStoreError("blob path escapes managed storage")
        return candidate

    def _assert_regular_managed_file(self, path: Path) -> None:
        if path.is_symlink():
            raise BlobStoreError("managed blob is a symlink")
        stat = path.stat()
        if not path.is_file():
            raise BlobStoreError("managed blob reference is not a regular file")
        resolved = path.resolve(strict=True)
        if not resolved.is_relative_to(self._blob_root):
            raise BlobStoreError("managed blob escapes storage root")
        if stat.st_size > self.max_blob_bytes:
            raise BlobStoreError("managed blob exceeds the active profile limit")

    @staticmethod
    def _fsync_directory(path: Path) -> None:
        descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
