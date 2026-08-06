"""Validation of independently versioned source pins.

``.koa/source-pins.json`` is an aggregate index.  Each entry still points to the
owning integration's source lock; the aggregate never replaces that lock.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final
from urllib.parse import urlsplit

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

SOURCE_PIN_SCHEMA_VERSION: Final = 1
SOURCE_TYPES: Final = frozenset({"git", "archive", "oci", "package", "source_bundle"})
HEX_RE: Final = re.compile(r"^[0-9a-f]+$")
SOURCE_ID_RE: Final = re.compile(r"^[a-z0-9]+(?:[.-][a-z0-9]+)*$")
FLOATING_REVISIONS: Final = frozenset(
    {"head", "main", "master", "develop", "development", "stable", "latest", "nightly", "trunk"}
)


class SourcePinError(ConfigurationError):
    """Raised when a source pin is incomplete, mutable, or inconsistent."""


@dataclass(frozen=True, slots=True)
class Digest:
    algorithm: str
    value: str


@dataclass(frozen=True, slots=True)
class SourcePin:
    source_id: str
    source_type: str
    location: str
    revision: str
    owner: str
    lock_file: str
    digest: Digest | None = None


@dataclass(frozen=True, slots=True)
class SourcePinIssue:
    code: str
    message: str


@dataclass(frozen=True, slots=True)
class SourcePinCheckResult:
    issues: tuple[SourcePinIssue, ...]
    pins: tuple[SourcePin, ...] = ()

    @property
    def ok(self) -> bool:
        return not self.issues


def _parse_digest(value: Any, *, location: str) -> Digest:
    digest = expect_mapping(value, location=location)
    require_exact_keys(digest, required={"algorithm", "value"}, location=location)
    algorithm = expect_nonempty_string(digest["algorithm"], location=f"{location}.algorithm")
    encoded = expect_nonempty_string(digest["value"], location=f"{location}.value")
    if algorithm != "sha256":
        raise SourcePinError(f"{location}.algorithm: only sha256 is admitted")
    if len(encoded) != 64 or not HEX_RE.fullmatch(encoded):
        raise SourcePinError(f"{location}.value: expected 64 lowercase hexadecimal characters")
    return Digest(algorithm=algorithm, value=encoded)


def _validate_location(value: Any, *, source_type: str, location: str) -> str:
    text = expect_nonempty_string(value, location=location)
    parsed = urlsplit(text)
    if parsed.username is not None or parsed.password is not None:
        raise SourcePinError(f"{location}: embedded credentials are prohibited")
    if parsed.fragment:
        raise SourcePinError(f"{location}: URL fragments are prohibited")
    if source_type == "source_bundle":
        return normalize_repository_path(text, location=location)
    if parsed.scheme not in {"https", "ssh", "git", "oci"}:
        raise SourcePinError(
            f"{location}: source type {source_type!r} requires an admitted immutable-source URI"
        )
    if not parsed.netloc and parsed.scheme != "oci":
        raise SourcePinError(f"{location}: URI authority is missing")
    return text


def _validate_revision(value: Any, *, digest: Digest | None, location: str) -> str:
    revision = expect_nonempty_string(value, location=location)
    lowered = revision.lower()
    if lowered in FLOATING_REVISIONS or lowered.startswith("refs/heads/"):
        raise SourcePinError(f"{location}: mutable branch or floating selector is prohibited")
    if any(token in lowered for token in ("*", "latest", "snapshot")):
        raise SourcePinError(f"{location}: floating revision selector is prohibited")
    commit_shaped = len(revision) in {40, 64} and bool(HEX_RE.fullmatch(revision))
    if not commit_shaped and digest is None:
        raise SourcePinError(
            f"{location}: a non-commit revision requires an exact sha256 digest"
        )
    return revision


def _parse_pin(value: Any, *, index: int) -> SourcePin:
    location = f"$.sources[{index}]"
    pin = expect_mapping(value, location=location)
    require_exact_keys(
        pin,
        required={"source_id", "source_type", "location", "revision", "owner", "lock_file"},
        optional={"digest"},
        location=location,
    )
    source_id = expect_nonempty_string(pin["source_id"], location=f"{location}.source_id")
    if not SOURCE_ID_RE.fullmatch(source_id):
        raise SourcePinError(
            f"{location}.source_id: expected lowercase segments separated by '.' or '-'"
        )
    source_type = expect_nonempty_string(
        pin["source_type"], location=f"{location}.source_type"
    )
    if source_type not in SOURCE_TYPES:
        raise SourcePinError(
            f"{location}.source_type: unsupported value {source_type!r}; "
            f"expected one of {sorted(SOURCE_TYPES)}"
        )
    digest = (
        _parse_digest(pin["digest"], location=f"{location}.digest")
        if "digest" in pin
        else None
    )
    if source_type in {"archive", "oci", "package", "source_bundle"} and digest is None:
        raise SourcePinError(f"{location}.digest: required for source type {source_type!r}")
    revision = _validate_revision(
        pin["revision"], digest=digest, location=f"{location}.revision"
    )
    source_location = _validate_location(
        pin["location"], source_type=source_type, location=f"{location}.location"
    )
    owner = expect_nonempty_string(pin["owner"], location=f"{location}.owner")
    lock_file = normalize_repository_path(pin["lock_file"], location=f"{location}.lock_file")
    if not lock_file.startswith("integrations/") or not lock_file.endswith("/source.lock.json"):
        raise SourcePinError(
            f"{location}.lock_file: expected integrations/<integration-id>/source.lock.json"
        )
    return SourcePin(
        source_id=source_id,
        source_type=source_type,
        location=source_location,
        revision=revision,
        owner=owner,
        lock_file=lock_file,
        digest=digest,
    )


def validate_source_pins(document: Any) -> tuple[SourcePin, ...]:
    """Validate a source-pin document and return immutable typed entries."""

    root = expect_mapping(document, location="$")
    require_exact_keys(root, required={"schema_version", "sources"}, location="$")
    version = root["schema_version"]
    if (
        isinstance(version, bool)
        or not isinstance(version, int)
        or version != SOURCE_PIN_SCHEMA_VERSION
    ):
        raise SourcePinError(
            f"$.schema_version: expected integer {SOURCE_PIN_SCHEMA_VERSION}"
        )
    sources = expect_sequence(root["sources"], location="$.sources")
    pins: list[SourcePin] = []
    seen_ids: set[str] = set()
    seen_locks: set[str] = set()
    for index, value in enumerate(sources):
        pin = _parse_pin(value, index=index)
        if pin.source_id in seen_ids:
            raise SourcePinError(f"$.sources[{index}].source_id: duplicate {pin.source_id!r}")
        if pin.lock_file in seen_locks:
            raise SourcePinError(f"$.sources[{index}].lock_file: duplicate {pin.lock_file!r}")
        seen_ids.add(pin.source_id)
        seen_locks.add(pin.lock_file)
        pins.append(pin)
    return tuple(pins)


def check_source_pins_file(path: str | Path) -> SourcePinCheckResult:
    """Return a stable diagnostic result instead of raising to a caller."""

    try:
        document = load_json_object(path)
        pins = validate_source_pins(document)
    except ConfigurationError as exc:
        return SourcePinCheckResult(
            issues=(SourcePinIssue(code="source_pins_invalid", message=str(exc)),)
        )
    return SourcePinCheckResult(issues=(), pins=pins)


def check(repository: Repository | str | Path) -> SourcePinCheckResult:
    """Check the canonical aggregate source-pin file for a repository."""

    try:
        repo = repository if isinstance(repository, Repository) else Repository(Path(repository))
        path = repo.control_path("source-pins.json", must_exist=True)
    except ConfigurationError as exc:
        return SourcePinCheckResult(
            issues=(SourcePinIssue(code="source_pins_unavailable", message=str(exc)),)
        )
    return check_source_pins_file(path)
