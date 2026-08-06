"""Constrained filesystem operations for host recovery.

This module does not decide recovery authority.  Callers must provide an
already-authorized root and relative paths.  Every mutating operation is
confined to that root and uses atomic replacement plus fsync.
"""

from __future__ import annotations

from contextlib import contextmanager, suppress
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
from typing import Any, Iterator, Mapping


class FilesystemAdapterError(RuntimeError):
    """Base error for constrained filesystem operations."""


class UnsafePathError(FilesystemAdapterError):
    """Raised when a path escapes its declared authority root."""


class IntegrityError(FilesystemAdapterError):
    """Raised when content does not match its declared digest."""


class DuplicateJsonKeyError(FilesystemAdapterError):
    """Raised when JSON contains a duplicate object key."""


@dataclass(frozen=True, slots=True)
class FileMetadata:
    relative_path: str
    size: int
    mode: int
    modified_ns: int
    sha256: str


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJsonKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _validate_relative_path(value: str | os.PathLike[str]) -> PurePosixPath:
    raw = os.fspath(value)
    if not raw or "\x00" in raw or "\\" in raw:
        raise UnsafePathError("path must be a non-empty POSIX relative path")
    path = PurePosixPath(raw)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise UnsafePathError(f"unsafe relative path: {raw!r}")
    return path


class SafeFilesystem:
    """Filesystem facade confined beneath one non-symlink root."""

    def __init__(self, root: str | os.PathLike[str], *, create: bool = False) -> None:
        candidate = Path(root)
        if not candidate.is_absolute():
            raise UnsafePathError("authority root must be absolute")
        if candidate.exists() and candidate.is_symlink():
            raise UnsafePathError("authority root must not be a symbolic link")
        if create:
            candidate.mkdir(mode=0o700, parents=True, exist_ok=True)
        self.root = candidate.resolve(strict=False)

    def resolve(
        self,
        relative_path: str | os.PathLike[str],
        *,
        must_exist: bool = False,
        allow_directory: bool = True,
    ) -> Path:
        relative = _validate_relative_path(relative_path)
        current = self.root
        for part in relative.parts:
            current = current / part
            try:
                info = current.lstat()
            except FileNotFoundError:
                continue
            if stat.S_ISLNK(info.st_mode):
                raise UnsafePathError(f"symbolic links are prohibited: {relative}")
        resolved = current.resolve(strict=False)
        try:
            resolved.relative_to(self.root)
        except ValueError as exc:
            raise UnsafePathError(f"path escapes authority root: {relative}") from exc
        if must_exist and not resolved.exists():
            raise FileNotFoundError(resolved)
        if resolved.exists() and not allow_directory and not resolved.is_file():
            raise UnsafePathError(f"regular file required: {relative}")
        return resolved

    def ensure_directory(self, relative_path: str | os.PathLike[str], *, mode: int = 0o700) -> Path:
        destination = self.resolve(relative_path)
        destination.mkdir(mode=mode, parents=True, exist_ok=True)
        os.chmod(destination, mode)
        self.resolve(relative_path, must_exist=True)
        return destination

    def read_bytes(self, relative_path: str | os.PathLike[str], *, max_bytes: int) -> bytes:
        if max_bytes <= 0:
            raise ValueError("max_bytes must be positive")
        path = self.resolve(relative_path, must_exist=True, allow_directory=False)
        info = path.stat()
        if info.st_size > max_bytes:
            raise FilesystemAdapterError(
                f"file exceeds the permitted size ({info.st_size} > {max_bytes}): {relative_path}"
            )
        flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
        fd = os.open(path, flags)
        try:
            data = os.read(fd, max_bytes + 1)
        finally:
            os.close(fd)
        if len(data) > max_bytes:
            raise FilesystemAdapterError(f"file exceeds the permitted size: {relative_path}")
        return data

    def read_json(self, relative_path: str | os.PathLike[str], *, max_bytes: int) -> dict[str, Any]:
        raw = self.read_bytes(relative_path, max_bytes=max_bytes)
        try:
            parsed = json.loads(raw.decode("utf-8"), object_pairs_hook=_reject_duplicate_keys)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise FilesystemAdapterError(f"invalid UTF-8 JSON: {relative_path}") from exc
        if not isinstance(parsed, dict):
            raise FilesystemAdapterError("top-level JSON value must be an object")
        return parsed

    def atomic_write_bytes(
        self,
        relative_path: str | os.PathLike[str],
        data: bytes,
        *,
        mode: int = 0o600,
        overwrite: bool = True,
    ) -> Path:
        destination = self.resolve(relative_path)
        destination.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        parent_relative = destination.parent.relative_to(self.root).as_posix()
        if parent_relative != ".":
            self.resolve(parent_relative, must_exist=True)
        if not overwrite and destination.exists():
            raise FileExistsError(destination)
        temporary = destination.with_name(f".{destination.name}.{os.getpid()}.tmp")
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0)
        fd = os.open(temporary, flags, mode)
        try:
            view = memoryview(data)
            while view:
                written = os.write(fd, view)
                view = view[written:]
            os.fsync(fd)
            os.fchmod(fd, mode)
        except BaseException:
            with suppress(FileNotFoundError):
                temporary.unlink()
            raise
        finally:
            os.close(fd)
        if not overwrite and destination.exists():
            temporary.unlink(missing_ok=True)
            raise FileExistsError(destination)
        os.replace(temporary, destination)
        directory_fd = os.open(destination.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
        return destination

    def atomic_write_json(
        self,
        relative_path: str | os.PathLike[str],
        payload: Mapping[str, Any],
        *,
        mode: int = 0o600,
        overwrite: bool = True,
    ) -> Path:
        encoded = (
            json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
        ).encode("utf-8")
        return self.atomic_write_bytes(
            relative_path,
            encoded,
            mode=mode,
            overwrite=overwrite,
        )

    def copy_verified(
        self,
        source: str | os.PathLike[str],
        destination_relative: str | os.PathLike[str],
        *,
        expected_sha256: str,
        max_bytes: int,
        overwrite: bool = False,
    ) -> Path:
        if len(expected_sha256) != 64 or any(ch not in "0123456789abcdef" for ch in expected_sha256):
            raise IntegrityError("expected SHA-256 must be 64 lowercase hexadecimal characters")
        source_path = Path(source)
        if not source_path.is_absolute() or source_path.is_symlink() or not source_path.is_file():
            raise UnsafePathError("source must be an absolute regular non-symlink file")
        info = source_path.stat()
        if info.st_size > max_bytes:
            raise FilesystemAdapterError("source exceeds configured recovery limit")

        destination = self.resolve(destination_relative)
        destination.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        parent_relative = destination.parent.relative_to(self.root).as_posix()
        if parent_relative != ".":
            self.resolve(parent_relative, must_exist=True)
        if not overwrite and destination.exists():
            raise FileExistsError(destination)

        temporary = destination.with_name(f".{destination.name}.{os.getpid()}.tmp")
        source_flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
        target_flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0)
        source_fd = os.open(source_path, source_flags)
        target_fd: int | None = None
        digest = hashlib.sha256()
        total = 0
        try:
            target_fd = os.open(temporary, target_flags, 0o600)
            while True:
                chunk = os.read(source_fd, 1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > max_bytes:
                    raise FilesystemAdapterError("source exceeds configured recovery limit")
                digest.update(chunk)
                view = memoryview(chunk)
                while view:
                    written = os.write(target_fd, view)
                    view = view[written:]
            actual = digest.hexdigest()
            if actual != expected_sha256:
                raise IntegrityError(f"SHA-256 mismatch: expected {expected_sha256}, got {actual}")
            os.fsync(target_fd)
            os.fchmod(target_fd, 0o600)
        except BaseException:
            temporary.unlink(missing_ok=True)
            raise
        finally:
            os.close(source_fd)
            if target_fd is not None:
                os.close(target_fd)

        if not overwrite and destination.exists():
            temporary.unlink(missing_ok=True)
            raise FileExistsError(destination)
        os.replace(temporary, destination)
        directory_fd = os.open(destination.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
        return destination

    def metadata(self, relative_path: str | os.PathLike[str], *, max_bytes: int) -> FileMetadata:
        path = self.resolve(relative_path, must_exist=True, allow_directory=False)
        info = path.stat()
        if info.st_size > max_bytes:
            raise FilesystemAdapterError("file exceeds configured evidence limit")
        digest = hashlib.sha256(self.read_bytes(relative_path, max_bytes=max_bytes)).hexdigest()
        return FileMetadata(
            relative_path=_validate_relative_path(relative_path).as_posix(),
            size=info.st_size,
            mode=stat.S_IMODE(info.st_mode),
            modified_ns=info.st_mtime_ns,
            sha256=digest,
        )

    @contextmanager
    def exclusive_lock(self, relative_path: str | os.PathLike[str]) -> Iterator[Path]:
        path = self.resolve(relative_path)
        path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0)
        try:
            fd = os.open(path, flags, 0o600)
        except FileExistsError as exc:
            raise FilesystemAdapterError(f"recovery lock is already held: {relative_path}") from exc
        try:
            os.write(fd, f"pid={os.getpid()}\n".encode("ascii"))
            os.fsync(fd)
            yield path
        finally:
            os.close(fd)
            path.unlink(missing_ok=True)
