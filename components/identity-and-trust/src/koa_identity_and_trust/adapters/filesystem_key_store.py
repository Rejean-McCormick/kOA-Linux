"""Profile-bounded filesystem key-handle storage.

This adapter is suitable only where the active profile explicitly permits a
filesystem-backed protected path. It never silently substitutes for a TPM or
other hardware-backed provider.
"""

from __future__ import annotations

import os
import re
import tempfile
from pathlib import Path

_KEY_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


class KeyStoreError(RuntimeError):
    """Raised when protected key material cannot be stored safely."""


class FilesystemKeyStore:
    """Store opaque private material with restrictive permissions and atomic IO."""

    def __init__(self, root: str | os.PathLike[str], *, create: bool = False) -> None:
        candidate = Path(root).expanduser()
        if candidate.is_symlink():
            raise KeyStoreError("protected key-store root must not be a symbolic link")
        if create:
            candidate.mkdir(mode=0o700, parents=True, exist_ok=True)
        self._root = candidate.resolve()
        self._validate_root()

    @property
    def root(self) -> Path:
        return self._root

    def _validate_root(self) -> None:
        if not self._root.exists() or not self._root.is_dir():
            raise KeyStoreError("protected key-store directory is unavailable")
        if self._root.is_symlink():
            raise KeyStoreError("protected key-store root must not be a symbolic link")
        mode = self._root.stat().st_mode & 0o777
        if mode & 0o077:
            raise KeyStoreError(
                f"protected key-store permissions are too broad: {mode:04o}"
            )

    def _path(self, key_id: str) -> Path:
        if not _KEY_ID.fullmatch(key_id):
            raise ValueError("key_id must be a bounded opaque identifier")
        path = self._root / f"{key_id}.key"
        if path.parent != self._root:
            raise ValueError("key_id escapes the protected key-store root")
        return path

    def exists(self, key_id: str) -> bool:
        path = self._path(key_id)
        return path.is_file() and not path.is_symlink()

    def put(self, key_id: str, material: bytes, *, replace: bool = False) -> str:
        """Atomically store opaque material and return its stable reference."""

        if not isinstance(material, bytes) or not material:
            raise ValueError("private material must be non-empty bytes")
        self._validate_root()
        destination = self._path(key_id)
        if destination.exists() and not replace:
            raise FileExistsError(f"protected key reference already exists: {key_id}")
        if destination.is_symlink():
            raise KeyStoreError("refusing to replace a symbolic link")

        fd, temporary_name = tempfile.mkstemp(prefix=".koa-key-", dir=self._root)
        temporary = Path(temporary_name)
        try:
            os.fchmod(fd, 0o600)
            with os.fdopen(fd, "wb", closefd=True) as stream:
                stream.write(material)
                stream.flush()
                os.fsync(stream.fileno())
            if replace:
                os.replace(temporary, destination)
            else:
                try:
                    os.link(temporary, destination, follow_symlinks=False)
                except FileExistsError as exc:
                    raise FileExistsError(
                        f"protected key reference already exists: {key_id}"
                    ) from exc
                temporary.unlink()
            os.chmod(destination, 0o600, follow_symlinks=False)
            self._fsync_directory()
        except BaseException:
            try:
                os.close(fd)
            except OSError:
                pass
            temporary.unlink(missing_ok=True)
            raise
        return self.reference(key_id)

    def get(self, key_id: str) -> bytes:
        """Load opaque material for an already-authorized internal operation."""

        self._validate_root()
        path = self._path(key_id)
        try:
            stat = path.lstat()
        except FileNotFoundError as exc:
            raise KeyError(key_id) from exc
        if path.is_symlink() or not path.is_file():
            raise KeyStoreError("protected key reference is not a regular file")
        if stat.st_mode & 0o077:
            raise KeyStoreError("protected key material permissions are too broad")
        return path.read_bytes()

    def delete(self, key_id: str) -> None:
        """Remove a key reference after lifecycle authorization has completed."""

        path = self._path(key_id)
        if path.is_symlink():
            raise KeyStoreError("refusing to delete a symbolic link")
        try:
            path.unlink()
        except FileNotFoundError as exc:
            raise KeyError(key_id) from exc
        self._fsync_directory()

    def reference(self, key_id: str) -> str:
        self._path(key_id)
        return f"file-key://{key_id}"

    # Port-friendly aliases with explicit semantics.
    store = put
    load = get
    destroy = delete

    def _fsync_directory(self) -> None:
        descriptor = os.open(self._root, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
