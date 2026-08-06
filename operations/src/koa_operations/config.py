"""Strict configuration, path, and deterministic JSON primitives."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import tempfile
import tomllib
from pathlib import Path, PurePosixPath
from typing import Any, Mapping


class ConfigurationError(ValueError):
    """Raised when operational input is ambiguous, unsafe, or malformed."""


_IDENTIFIER = re.compile(r"^[a-z0-9][a-z0-9._:-]{0,127}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


def identifier(value: object, field: str) -> str:
    if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value):
        raise ConfigurationError(f"{field} must be a lower-case stable identifier")
    return value


def reference(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > 512:
        raise ConfigurationError(f"{field} must be a non-empty stable reference")
    if any(ch in value for ch in ("\x00", "\r", "\n")):
        raise ConfigurationError(f"{field} contains a forbidden control character")
    return value


def sha256_value(value: object, field: str) -> str:
    if not isinstance(value, str) or not _SHA256.fullmatch(value):
        raise ConfigurationError(f"{field} must be a lower-case SHA-256 digest")
    return value


def relative_path(value: object, field: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise ConfigurationError(f"{field} must be a non-empty POSIX relative path")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise ConfigurationError(f"{field} escapes its declared root")
    normalized = str(path)
    if len(normalized) > 512:
        raise ConfigurationError(f"{field} is too long")
    return normalized


def canonical_json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def json_digest(value: object) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def file_digest(path: Path, *, chunk_size: int = 1024 * 1024) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        while chunk := stream.read(chunk_size):
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ConfigurationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _regular_input(path: Path, max_bytes: int) -> bytes:
    try:
        metadata = path.lstat()
    except FileNotFoundError as exc:
        raise ConfigurationError(f"configuration file does not exist: {path}") from exc
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise ConfigurationError(f"configuration input must be a regular non-symlink file: {path}")
    if metadata.st_size > max_bytes:
        raise ConfigurationError(f"configuration input exceeds {max_bytes} bytes: {path}")
    return path.read_bytes()


def load_mapping(path: str | Path, *, max_bytes: int = 2 * 1024 * 1024) -> dict[str, Any]:
    source = Path(path)
    raw = _regular_input(source, max_bytes)
    try:
        if source.suffix.lower() == ".json":
            value = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object)
        elif source.suffix.lower() == ".toml":
            value = tomllib.loads(raw.decode("utf-8"))
        else:
            raise ConfigurationError("configuration files must use .json or .toml")
    except (UnicodeDecodeError, json.JSONDecodeError, tomllib.TOMLDecodeError) as exc:
        raise ConfigurationError(f"cannot parse {source}: {exc}") from exc
    if not isinstance(value, dict):
        raise ConfigurationError(f"top-level value must be an object: {source}")
    return value


def reject_symlink_chain(path: Path) -> None:
    absolute = path.absolute()
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current /= part
        if not current.exists() and not current.is_symlink():
            continue
        if current.is_symlink():
            raise ConfigurationError(f"symlink path component is forbidden: {current}")


def ensure_directory(path: Path, *, mode: int = 0o700) -> Path:
    reject_symlink_chain(path.parent)
    path.mkdir(parents=True, exist_ok=True, mode=mode)
    reject_symlink_chain(path)
    if not path.is_dir():
        raise ConfigurationError(f"expected directory: {path}")
    try:
        path.chmod(mode)
    except PermissionError:
        pass
    return path


def write_json_atomic(
    path: str | Path,
    payload: object,
    *,
    overwrite: bool = False,
    mode: int = 0o600,
) -> Path:
    destination = Path(path)
    ensure_directory(destination.parent)
    reject_symlink_chain(destination.parent)
    if destination.exists() or destination.is_symlink():
        if not overwrite:
            raise ConfigurationError(f"refusing to overwrite immutable output: {destination}")
        if destination.is_symlink() or not destination.is_file():
            raise ConfigurationError(f"output must be a regular file: {destination}")
    data = canonical_json_bytes(payload)
    fd, temporary_name = tempfile.mkstemp(prefix=f".{destination.name}.", dir=destination.parent)
    temporary = Path(temporary_name)
    try:
        os.fchmod(fd, mode)
        with os.fdopen(fd, "wb", closefd=True) as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if overwrite:
            os.replace(temporary, destination)
        else:
            try:
                os.link(temporary, destination)
            except FileExistsError as exc:
                raise ConfigurationError(
                    f"refusing to overwrite immutable output: {destination}"
                ) from exc
            temporary.unlink()
        directory_fd = os.open(destination.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary.exists():
            temporary.unlink()
    return destination


def require_mapping(value: object, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ConfigurationError(f"{field} must be an object")
    return value


def require_list(value: object, field: str) -> list[Any]:
    if not isinstance(value, list):
        raise ConfigurationError(f"{field} must be a list")
    return value
