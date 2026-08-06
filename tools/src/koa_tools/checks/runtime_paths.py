"""Validation of repository-to-installed-runtime path mappings."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Final

from koa_tools.config import (
    ConfigurationError,
    expect_mapping,
    expect_nonempty_string,
    expect_sequence,
    load_json_object,
    normalize_repository_path,
    require_exact_keys,
)
from koa_tools.repository import Repository

RUNTIME_PATH_SCHEMA_VERSION: Final = 1
PATH_CLASSES: Final[tuple[tuple[str, str], ...]] = (
    ("/var/lib/koa-recovery", "recovery_state"),
    ("/var/cache/koa-build", "build_cache"),
    ("/usr/libexec", "immutable_payload"),
    ("/usr/share", "immutable_payload"),
    ("/usr/lib", "immutable_payload"),
    ("/usr/bin", "immutable_payload"),
    ("/etc/koa", "operator_configuration"),
    ("/run/koa", "ephemeral_runtime"),
    ("/var/lib/koa", "persistent_state"),
    ("/var/cache/koa", "runtime_cache"),
)


class RuntimePathError(ConfigurationError):
    """Raised when an installed path is ambiguous or escapes an admitted root."""


@dataclass(frozen=True, slots=True)
class RuntimePathMapping:
    source: str
    destination: str
    path_class: str
    owner: str


@dataclass(frozen=True, slots=True)
class RuntimePathIssue:
    code: str
    message: str


@dataclass(frozen=True, slots=True)
class RuntimePathCheckResult:
    issues: tuple[RuntimePathIssue, ...]
    mappings: tuple[RuntimePathMapping, ...] = ()

    @property
    def ok(self) -> bool:
        return not self.issues


def normalize_runtime_path(value: str, *, location: str = "runtime path") -> str:
    """Normalize an absolute POSIX path and reject traversal or unknown roots."""

    text = expect_nonempty_string(value, location=location)
    if "\\" in text:
        raise RuntimePathError(f"{location}: backslashes are prohibited")
    if not text.startswith("/"):
        raise RuntimePathError(f"{location}: installed runtime path must be absolute")
    raw_segments = text.split("/")[1:]
    if any(segment in {"", ".", ".."} for segment in raw_segments):
        # A final empty segment is a harmless directory marker in prose, but a
        # machine-readable mapping uses one canonical identity without it.
        raise RuntimePathError(f"{location}: empty, '.' or '..' segments are prohibited")
    canonical = PurePosixPath(text).as_posix()
    if canonical != text:
        raise RuntimePathError(f"{location}: path is not normalized: {text!r}")
    _classify_runtime_path(canonical, location=location)
    return canonical


def _classify_runtime_path(path: str, *, location: str) -> str:
    for root, path_class in PATH_CLASSES:
        if path == root or path.startswith(root + "/"):
            return path_class
    raise RuntimePathError(f"{location}: path is outside the frozen installed roots: {path}")


def validate_runtime_paths(document: Any) -> tuple[RuntimePathMapping, ...]:
    root = expect_mapping(document, location="$")
    require_exact_keys(root, required={"schema_version", "mappings"}, location="$")
    version = root["schema_version"]
    if (
        isinstance(version, bool)
        or not isinstance(version, int)
        or version != RUNTIME_PATH_SCHEMA_VERSION
    ):
        raise RuntimePathError(
            f"$.schema_version: expected integer {RUNTIME_PATH_SCHEMA_VERSION}"
        )
    entries = expect_sequence(root["mappings"], location="$.mappings")
    mappings: list[RuntimePathMapping] = []
    seen_sources: set[str] = set()
    seen_destinations: set[str] = set()
    for index, value in enumerate(entries):
        location = f"$.mappings[{index}]"
        entry = expect_mapping(value, location=location)
        require_exact_keys(
            entry,
            required={"source", "destination", "path_class", "owner"},
            location=location,
        )
        source = normalize_repository_path(entry["source"], location=f"{location}.source")
        destination = normalize_runtime_path(
            entry["destination"], location=f"{location}.destination"
        )
        declared_class = expect_nonempty_string(
            entry["path_class"], location=f"{location}.path_class"
        )
        actual_class = _classify_runtime_path(destination, location=f"{location}.destination")
        if declared_class != actual_class:
            raise RuntimePathError(
                f"{location}.path_class: {declared_class!r} does not match {actual_class!r}"
            )
        owner = expect_nonempty_string(entry["owner"], location=f"{location}.owner")
        if source in seen_sources:
            raise RuntimePathError(f"{location}.source: duplicate mapping for {source!r}")
        if destination in seen_destinations:
            raise RuntimePathError(
                f"{location}.destination: duplicate installed path {destination!r}"
            )
        seen_sources.add(source)
        seen_destinations.add(destination)
        mappings.append(
            RuntimePathMapping(
                source=source,
                destination=destination,
                path_class=declared_class,
                owner=owner,
            )
        )
    return tuple(mappings)


def check_runtime_paths_file(path: str | Path) -> RuntimePathCheckResult:
    try:
        document = load_json_object(path)
        mappings = validate_runtime_paths(document)
    except ConfigurationError as exc:
        return RuntimePathCheckResult(
            issues=(RuntimePathIssue(code="runtime_paths_invalid", message=str(exc)),)
        )
    return RuntimePathCheckResult(issues=(), mappings=mappings)


def check(repository: Repository | str | Path) -> RuntimePathCheckResult:
    try:
        repo = repository if isinstance(repository, Repository) else Repository(Path(repository))
        path = repo.control_path("runtime-paths.json", must_exist=True)
    except ConfigurationError as exc:
        return RuntimePathCheckResult(
            issues=(RuntimePathIssue(code="runtime_paths_unavailable", message=str(exc)),)
        )
    return check_runtime_paths_file(path)
