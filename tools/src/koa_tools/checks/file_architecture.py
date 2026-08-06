"""Validation of the frozen repository file architecture."""
from __future__ import annotations

import fnmatch
from pathlib import Path
from typing import Any, Iterable, Mapping

from . import (
    CheckResult,
    Finding,
    first_mapping,
    first_sequence,
    iter_repository_files,
    load_json_object,
    normalize_repository_path,
    repository_root,
)
from .dependencies import check_dependencies
from .generated_content import check_generated_content
from .path_ownership import check_path_ownership


DEFAULT_TOP_LEVEL_ROOTS = frozenset(
    {
        ".github",
        ".koa",
        "LICENSES",
        "assembly",
        "ci",
        "components",
        "dev",
        "docs",
        "generated",
        "host",
        "integrations",
        "interfaces",
        "operations",
        "packaging",
        "profiles",
        "release",
        "tests",
        "tools",
    }
)
DEFAULT_ROOT_FILES = frozenset(
    {
        ".editorconfig",
        ".gitattributes",
        ".gitignore",
        ".pre-commit-config.yaml",
        ".python-version",
        ".rustfmt.toml",
        "Cargo.lock",
        "Cargo.toml",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "NOTICE.md",
        "README.md",
        "REUSE.toml",
        "SECURITY.md",
        "pyproject.toml",
        "rust-toolchain.toml",
        "uv.lock",
    }
)


def _path_values(data: Mapping[str, Any]) -> tuple[list[str], list[Finding]]:
    findings: list[Finding] = []
    raw = first_sequence(data, ("paths", "files", "inventory", "entries"))
    values: list[str] = []
    if raw is not None:
        for index, item in enumerate(raw):
            if isinstance(item, str):
                value = item
            elif isinstance(item, dict):
                value = item.get("path") or item.get("file")
            else:
                value = None
            if not isinstance(value, str) or not value:
                findings.append(Finding("FILE_LOCK_ENTRY", f"entry {index} has no path", ".koa/file-architecture.lock.json"))
                continue
            try:
                values.append(normalize_repository_path(value))
            except ValueError as exc:
                findings.append(Finding("FILE_LOCK_PATH", f"entry {index}: {exc}", ".koa/file-architecture.lock.json"))
    else:
        mapping = first_mapping(data, ("path_metadata", "file_metadata"))
        if mapping is not None:
            for value in mapping:
                try:
                    values.append(normalize_repository_path(value))
                except ValueError as exc:
                    findings.append(Finding("FILE_LOCK_PATH", str(exc), ".koa/file-architecture.lock.json"))
        else:
            findings.append(Finding("FILE_LOCK_SHAPE", "lock must contain paths/files/inventory/entries or path_metadata", ".koa/file-architecture.lock.json"))
    duplicates = sorted({path for path in values if values.count(path) > 1})
    for path in duplicates:
        findings.append(Finding("FILE_LOCK_DUPLICATE", "path appears more than once in architecture lock", path))
    return sorted(set(values), key=str.casefold), findings


def _repository_allowlist(data: Mapping[str, Any] | None) -> tuple[set[str], set[str]]:
    if data is None:
        return set(DEFAULT_TOP_LEVEL_ROOTS), set(DEFAULT_ROOT_FILES)
    root_values = data.get("allowed_top_level_roots") or data.get("top_level_roots") or data.get("roots")
    file_values = data.get("allowed_root_files") or data.get("root_files")
    roots = set(root_values) if isinstance(root_values, list) and all(isinstance(item, str) for item in root_values) else set(DEFAULT_TOP_LEVEL_ROOTS)
    files = set(file_values) if isinstance(file_values, list) and all(isinstance(item, str) for item in file_values) else set(DEFAULT_ROOT_FILES)
    return roots, files


def _ignored_patterns(data: Mapping[str, Any]) -> tuple[str, ...]:
    values = data.get("ignored_paths") or data.get("ignore") or []
    if not isinstance(values, list):
        return ()
    result: list[str] = []
    for value in values:
        if isinstance(value, str):
            try:
                result.append(normalize_repository_path(value))
            except ValueError:
                continue
    return tuple(sorted(set(result)))


def _is_ignored(path: str, patterns: tuple[str, ...]) -> bool:
    return any(fnmatch.fnmatchcase(path, pattern) or path.startswith(pattern + "/") for pattern in patterns)


def _check_symlink(base: Path, relative: str) -> Finding | None:
    path = base / relative
    if not path.is_symlink():
        return None
    try:
        resolved = path.resolve(strict=False)
        resolved.relative_to(base)
    except (OSError, ValueError):
        return Finding("FILE_SYMLINK_ESCAPE", "symbolic link escapes the repository root", relative)
    return None


def check_file_architecture(
    root: str | Path | None = None,
    *,
    include_related: bool = True,
    paths: Iterable[str] | None = None,
) -> CheckResult:
    """Compare committed paths with the frozen lock and enforce root structure."""

    base = repository_root(root)
    lock_data, findings = load_json_object(base / ".koa" / "file-architecture.lock.json", code_prefix="FILE_LOCK")
    repository_data, repository_findings = load_json_object(base / ".koa" / "repository.json", code_prefix="REPOSITORY_REGISTRY")
    findings.extend(repository_findings)
    if lock_data is None:
        return CheckResult.build("file-architecture", findings, {"actual_paths": 0, "expected_paths": 0})

    expected, lock_findings = _path_values(lock_data)
    findings.extend(lock_findings)
    ignored = _ignored_patterns(lock_data)
    actual = sorted(
        {
            normalize_repository_path(path)
            for path in (paths if paths is not None else iter_repository_files(base))
            if not _is_ignored(str(path).replace("\\", "/"), ignored)
        },
        key=str.casefold,
    )
    expected_set = set(expected)
    actual_set = set(actual)
    for path in sorted(actual_set - expected_set, key=str.casefold):
        findings.append(Finding("FILE_UNKNOWN", "committed path is not present in the frozen architecture lock", path))
    for path in sorted(expected_set - actual_set, key=str.casefold):
        findings.append(Finding("FILE_MISSING", "path declared by the frozen architecture lock is missing", path))

    allowed_roots, allowed_root_files = _repository_allowlist(repository_data)
    for path in actual:
        root_name = path.split("/", 1)[0]
        if "/" in path:
            if root_name not in allowed_roots:
                findings.append(Finding("FILE_TOP_LEVEL_ROOT", f"unknown top-level root: {root_name}", path))
        elif path not in allowed_root_files:
            findings.append(Finding("FILE_ROOT_ENTRY", "unknown file at repository root", path))
        symlink_finding = _check_symlink(base, path)
        if symlink_finding:
            findings.append(symlink_finding)

    if include_related:
        related = (
            check_path_ownership(base, paths=actual),
            check_dependencies(base, paths=actual),
            check_generated_content(base, paths=actual),
        )
        for result in related:
            findings.extend(result.findings)

    return CheckResult.build(
        "file-architecture",
        findings,
        {
            "actual_paths": len(actual),
            "expected_paths": len(expected),
            "related_checks": include_related,
        },
    )


check = check_file_architecture


__all__ = ["check", "check_file_architecture"]
