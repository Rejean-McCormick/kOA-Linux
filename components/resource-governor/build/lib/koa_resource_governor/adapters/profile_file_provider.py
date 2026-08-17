"""Read-only provider for active profile and resource-envelope JSON files."""

from __future__ import annotations

import json
import os
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

_DEFAULT_MAX_BYTES = 4 * 1024 * 1024


class ProfileFileError(RuntimeError):
    """Base error for profile and envelope file access."""


class ProfileFileMissing(ProfileFileError):
    """Raised when a required profile or envelope file does not exist."""


class ProfileFileInvalid(ProfileFileError):
    """Raised when a file is unsafe, oversized, or invalid JSON."""


class ProfileFileProvider:
    """Load immutable configuration facts from explicitly configured roots.

    The provider owns no profile or envelope authority. It performs bounded,
    read-only loading and leaves schema, signature, compatibility, precedence,
    and activation decisions to the Resource Governor application layer.
    """

    def __init__(
        self,
        *,
        active_profile_path: str | os.PathLike[str],
        envelope_root: str | os.PathLike[str],
        max_bytes: int = _DEFAULT_MAX_BYTES,
    ) -> None:
        if max_bytes <= 0:
            raise ValueError("max_bytes must be positive")
        self._active_profile_path = Path(active_profile_path)
        self._envelope_root = Path(envelope_root)
        self._max_bytes = max_bytes

    def get_active_profile(self) -> Mapping[str, object]:
        """Return the active profile document as an isolated mapping copy."""

        document = _load_json_object(self._active_profile_path, self._max_bytes)
        _require_profile_identity(document)
        return document

    def load_active_profile(self) -> Mapping[str, object]:
        """Alias used by profile-provider ports."""

        return self.get_active_profile()

    def load_profile(self) -> Mapping[str, object]:
        """Short port-friendly alias for the active profile."""

        return self.get_active_profile()

    def get_resource_envelope(self, reference: str) -> Mapping[str, object]:
        """Load one envelope by a path relative to ``envelope_root``.

        A local JSON Pointer fragment is supported. Absolute paths, parent
        traversal, symlinks, and references outside the configured root fail.
        """

        relative_path, fragment = _split_reference(reference)
        candidate = _resolve_confined_file(self._envelope_root, relative_path)
        document = _load_json_object(candidate, self._max_bytes)
        selected = _resolve_json_pointer(document, fragment) if fragment else document
        if not isinstance(selected, Mapping):
            raise ProfileFileInvalid("resource envelope reference does not resolve to an object")
        result = dict(selected)
        _require_envelope_identity(result)
        return result

    def load_resource_envelope(self, reference: str) -> Mapping[str, object]:
        """Alias used by resource-envelope provider ports."""

        return self.get_resource_envelope(reference)

    def load_envelope(self, reference: str) -> Mapping[str, object]:
        """Short port-friendly alias for one resource envelope."""

        return self.get_resource_envelope(reference)

    def load_resource_envelopes(self, references: Sequence[str]) -> tuple[Mapping[str, object], ...]:
        """Load an ordered set of envelopes without silently ignoring failures."""

        return tuple(self.get_resource_envelope(reference) for reference in references)


def _load_json_object(path: Path, max_bytes: int) -> dict[str, object]:
    try:
        resolved = path.resolve(strict=True)
    except FileNotFoundError as exc:
        raise ProfileFileMissing(f"required file is missing: {path}") from exc
    if path.is_symlink() or not resolved.is_file():
        raise ProfileFileInvalid(f"required path is not a regular non-symlink file: {path}")

    try:
        size = resolved.stat().st_size
    except OSError as exc:
        raise ProfileFileError(f"cannot stat required file: {path}") from exc
    if size > max_bytes:
        raise ProfileFileInvalid(f"file exceeds configured size limit: {path}")

    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(resolved, flags)
        with os.fdopen(fd, "r", encoding="utf-8") as stream:
            raw = stream.read(max_bytes + 1)
    except OSError as exc:
        raise ProfileFileError(f"cannot read required file: {path}") from exc
    if len(raw.encode("utf-8")) > max_bytes:
        raise ProfileFileInvalid(f"file exceeds configured size limit: {path}")

    try:
        value = json.loads(raw, object_pairs_hook=_reject_duplicate_keys)
    except (UnicodeError, json.JSONDecodeError, ValueError) as exc:
        raise ProfileFileInvalid(f"invalid JSON document: {path}") from exc
    if not isinstance(value, dict):
        raise ProfileFileInvalid(f"JSON document must be an object: {path}")
    return value


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _split_reference(reference: str) -> tuple[Path, str]:
    if not reference.strip():
        raise ValueError("resource envelope reference is required")
    path_part, separator, fragment = reference.partition("#")
    relative = Path(path_part)
    if relative.is_absolute() or not path_part or ".." in relative.parts:
        raise ProfileFileInvalid("resource envelope path must be a confined relative path")
    if separator and fragment and not fragment.startswith("/"):
        raise ProfileFileInvalid("JSON Pointer fragment must be empty or begin with '/'")
    return relative, fragment


def _resolve_confined_file(root: Path, relative: Path) -> Path:
    try:
        resolved_root = root.resolve(strict=True)
    except FileNotFoundError as exc:
        raise ProfileFileMissing(f"resource envelope root is missing: {root}") from exc
    if not resolved_root.is_dir():
        raise ProfileFileInvalid("resource envelope root must be a directory")
    candidate = resolved_root.joinpath(relative)
    try:
        resolved = candidate.resolve(strict=True)
    except FileNotFoundError as exc:
        raise ProfileFileMissing(f"resource envelope is missing: {relative}") from exc
    if candidate.is_symlink() or not resolved.is_relative_to(resolved_root):
        raise ProfileFileInvalid("resource envelope path escapes its configured root")
    if not resolved.is_file():
        raise ProfileFileInvalid("resource envelope path is not a regular file")
    return resolved


def _resolve_json_pointer(document: object, fragment: str) -> object:
    current = document
    if not fragment:
        return current
    for raw_token in fragment[1:].split("/"):
        if "~" in raw_token:
            remainder = raw_token
            while "~" in remainder:
                _, marker, remainder = remainder.partition("~")
                if not remainder or remainder[0] not in {"0", "1"}:
                    raise ProfileFileInvalid("JSON Pointer contains an invalid escape")
                remainder = remainder[1:]
        token = raw_token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, Mapping):
            if token not in current:
                raise ProfileFileInvalid(f"JSON Pointer token does not resolve: {token}")
            current = current[token]
        elif isinstance(current, list):
            try:
                index = int(token)
            except ValueError as exc:
                raise ProfileFileInvalid("JSON Pointer array token is not an integer") from exc
            if index < 0 or index >= len(current):
                raise ProfileFileInvalid("JSON Pointer array index is out of range")
            current = current[index]
        else:
            raise ProfileFileInvalid("JSON Pointer traverses a scalar value")
    return current


def _require_profile_identity(document: Mapping[str, object]) -> None:
    candidates: list[object] = [document.get("profile_id"), document.get("id")]
    primary = document.get("primary_profile")
    if isinstance(primary, Mapping):
        candidates.extend((primary.get("id"), primary.get("profile_id"), primary.get("profile_ref")))
    if not any(isinstance(value, str) and value.strip() for value in candidates):
        raise ProfileFileInvalid("active profile document has no stable profile identity")


def _require_envelope_identity(document: Mapping[str, object]) -> None:
    envelope_id = document.get("envelope_id")
    version = document.get("version")
    if not isinstance(envelope_id, str) or not envelope_id.strip():
        raise ProfileFileInvalid("resource envelope has no envelope_id")
    if not isinstance(version, str) or not version.strip():
        raise ProfileFileInvalid("resource envelope has no version")
