"""Strict configuration loading and path validation for repository tooling.

The helpers in this module deliberately reject ambiguous input.  Configuration
files are UTF-8 JSON objects, duplicate keys are invalid, non-finite numbers are
invalid, and repository paths use normalized POSIX syntax without traversal.
"""

from __future__ import annotations

import json
import math
import os
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path, PurePosixPath
from typing import Any, Final, TypeAlias

JSONScalar: TypeAlias = None | bool | int | float | str
JSONValue: TypeAlias = JSONScalar | list["JSONValue"] | dict[str, "JSONValue"]
JSONObject: TypeAlias = dict[str, JSONValue]

DEFAULT_MAX_CONFIG_BYTES: Final = 4 * 1024 * 1024


class ConfigurationError(ValueError):
    """Raised when a repository configuration file is absent or malformed."""


def _reject_constant(value: str) -> None:
    raise ConfigurationError(f"non-finite JSON number is prohibited: {value}")


def _unique_object(pairs: list[tuple[str, JSONValue]]) -> JSONObject:
    result: JSONObject = {}
    for key, value in pairs:
        if key in result:
            raise ConfigurationError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def _validate_json_tree(value: JSONValue, *, location: str = "$") -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ConfigurationError(f"{location}: non-finite number is prohibited")
    if isinstance(value, list):
        for index, item in enumerate(value):
            _validate_json_tree(item, location=f"{location}[{index}]")
    elif isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise ConfigurationError(f"{location}: object keys must be strings")
            _validate_json_tree(item, location=f"{location}.{key}")


def load_json_object(
    path: str | os.PathLike[str],
    *,
    max_bytes: int = DEFAULT_MAX_CONFIG_BYTES,
    reject_symlink: bool = True,
) -> JSONObject:
    """Load a bounded UTF-8 JSON object and reject ambiguous encodings.

    The final path itself may not be a symbolic link by default.  Parent path
    containment belongs to :mod:`koa_tools.repository`, which knows the owning
    repository root.
    """

    config_path = Path(path)
    if max_bytes <= 0:
        raise ConfigurationError("max_bytes must be positive")
    if reject_symlink and config_path.is_symlink():
        raise ConfigurationError(f"configuration path is a symbolic link: {config_path}")
    try:
        size = config_path.stat().st_size
    except FileNotFoundError as exc:
        raise ConfigurationError(f"configuration file does not exist: {config_path}") from exc
    except OSError as exc:
        raise ConfigurationError(f"cannot stat configuration file {config_path}: {exc}") from exc
    if not config_path.is_file():
        raise ConfigurationError(f"configuration path is not a regular file: {config_path}")
    if size > max_bytes:
        raise ConfigurationError(
            f"configuration file exceeds {max_bytes} bytes: {config_path} ({size} bytes)"
        )

    try:
        raw = config_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ConfigurationError(f"configuration is not valid UTF-8: {config_path}") from exc
    except OSError as exc:
        raise ConfigurationError(f"cannot read configuration file {config_path}: {exc}") from exc

    try:
        value = json.loads(
            raw,
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
    except ConfigurationError:
        raise
    except json.JSONDecodeError as exc:
        raise ConfigurationError(
            f"invalid JSON in {config_path} at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc
    if not isinstance(value, dict):
        raise ConfigurationError(f"top-level JSON value must be an object: {config_path}")
    _validate_json_tree(value)
    return value


def require_exact_keys(
    value: Mapping[str, Any],
    *,
    required: Iterable[str],
    optional: Iterable[str] = (),
    location: str = "$",
) -> None:
    """Require all mandatory keys and reject undeclared keys."""

    required_set = frozenset(required)
    optional_set = frozenset(optional)
    overlap = required_set & optional_set
    if overlap:
        raise RuntimeError(f"schema bug: keys are both required and optional: {sorted(overlap)}")
    keys = frozenset(value)
    missing = sorted(required_set - keys)
    unknown = sorted(keys - required_set - optional_set)
    if missing:
        raise ConfigurationError(f"{location}: missing required keys: {', '.join(missing)}")
    if unknown:
        raise ConfigurationError(f"{location}: unknown keys: {', '.join(unknown)}")


def expect_mapping(value: Any, *, location: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ConfigurationError(f"{location}: expected an object")
    return value


def expect_sequence(value: Any, *, location: str) -> Sequence[Any]:
    if not isinstance(value, list):
        raise ConfigurationError(f"{location}: expected an array")
    return value


def expect_nonempty_string(value: Any, *, location: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ConfigurationError(f"{location}: expected a non-empty string")
    if value != value.strip():
        raise ConfigurationError(f"{location}: surrounding whitespace is prohibited")
    if "\x00" in value:
        raise ConfigurationError(f"{location}: NUL is prohibited")
    return value


def expect_integer(value: Any, *, location: str, minimum: int | None = None) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ConfigurationError(f"{location}: expected an integer")
    if minimum is not None and value < minimum:
        raise ConfigurationError(f"{location}: expected an integer >= {minimum}")
    return value


def normalize_repository_path(value: str, *, location: str = "path") -> str:
    """Return a canonical repository-relative POSIX path.

    Absolute paths, Windows separators, empty segments, ``.`` and ``..`` are
    rejected rather than silently rewritten.  This makes path identity stable
    across platforms and prevents traversal before filesystem resolution.
    """

    text = expect_nonempty_string(value, location=location)
    if "\\" in text:
        raise ConfigurationError(f"{location}: backslashes are prohibited")
    if text.startswith("/"):
        raise ConfigurationError(f"{location}: repository path must be relative")
    if text.endswith("/"):
        raise ConfigurationError(f"{location}: trailing slash is not canonical")
    segments = text.split("/")
    if any(segment in {"", ".", ".."} for segment in segments):
        raise ConfigurationError(f"{location}: empty, '.' or '..' path segments are prohibited")
    path = PurePosixPath(text)
    canonical = path.as_posix()
    if canonical != text:
        raise ConfigurationError(f"{location}: path is not normalized: {text!r}")
    return canonical
