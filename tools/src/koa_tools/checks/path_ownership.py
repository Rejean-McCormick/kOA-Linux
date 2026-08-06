"""Validation of canonical repository path ownership."""
from __future__ import annotations

from dataclasses import dataclass
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


@dataclass(frozen=True, slots=True)
class OwnershipRule:
    owner: str
    pattern: str
    excludes: tuple[str, ...] = ()

    def matches(self, path: str) -> bool:
        if any(_matches_pattern(path, excluded) for excluded in self.excludes):
            return False
        return _matches_pattern(path, self.pattern)


def _matches_pattern(path: str, pattern: str) -> bool:
    normalized = normalize_repository_path(pattern)
    if any(character in normalized for character in "*?["):
        return fnmatch.fnmatchcase(path, normalized)
    return path == normalized or path.startswith(normalized + "/")


def _string_list(value: Any) -> tuple[str, ...]:
    if isinstance(value, str):
        return (value,)
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return tuple(value)
    return ()


def _parse_rule(item: Mapping[str, Any], findings: list[Finding], index: int) -> list[OwnershipRule]:
    owner = item.get("owner") or item.get("owner_id") or item.get("component") or item.get("authority")
    patterns = (
        _string_list(item.get("paths"))
        or _string_list(item.get("patterns"))
        or _string_list(item.get("globs"))
        or _string_list(item.get("path"))
        or _string_list(item.get("pattern"))
        or _string_list(item.get("root"))
    )
    excludes = _string_list(item.get("exclude")) or _string_list(item.get("excludes"))
    if not isinstance(owner, str) or not owner.strip():
        findings.append(Finding("OWNERSHIP_RULE_OWNER", f"rule {index} has no non-empty owner", ".koa/path-ownership.json"))
        return []
    if not patterns:
        findings.append(Finding("OWNERSHIP_RULE_PATH", f"rule {index} has no path or pattern", ".koa/path-ownership.json"))
        return []
    rules: list[OwnershipRule] = []
    for pattern in patterns:
        try:
            normalized = normalize_repository_path(pattern)
            normalized_excludes = tuple(normalize_repository_path(value) for value in excludes)
        except ValueError as exc:
            findings.append(Finding("OWNERSHIP_RULE_INVALID_PATH", f"rule {index}: {exc}", ".koa/path-ownership.json"))
            continue
        rules.append(OwnershipRule(owner.strip(), normalized, normalized_excludes))
    return rules


def parse_ownership_rules(data: Mapping[str, Any]) -> tuple[list[OwnershipRule], list[Finding]]:
    """Parse accepted explicit forms of the path ownership registry."""

    findings: list[Finding] = []
    rules: list[OwnershipRule] = []
    raw_rules = first_sequence(data, ("rules", "ownership", "owners", "entries"))
    if raw_rules is not None:
        for index, item in enumerate(raw_rules):
            if not isinstance(item, dict):
                findings.append(Finding("OWNERSHIP_RULE_SHAPE", f"rule {index} must be an object", ".koa/path-ownership.json"))
                continue
            rules.extend(_parse_rule(item, findings, index))
    else:
        mapping = first_mapping(data, ("paths", "path_owners", "ownership_by_path"))
        if mapping is not None:
            for index, (pattern, owner_value) in enumerate(sorted(mapping.items())):
                if isinstance(owner_value, str):
                    item: Mapping[str, Any] = {"path": pattern, "owner": owner_value}
                elif isinstance(owner_value, dict):
                    item = {"path": pattern, **owner_value}
                else:
                    findings.append(Finding("OWNERSHIP_RULE_SHAPE", f"owner for {pattern!r} must be a string or object", ".koa/path-ownership.json"))
                    continue
                rules.extend(_parse_rule(item, findings, index))
        else:
            findings.append(
                Finding(
                    "OWNERSHIP_REGISTRY_SHAPE",
                    "registry must contain a rules list or a paths mapping",
                    ".koa/path-ownership.json",
                )
            )
    unique = sorted(set(rules), key=lambda item: (item.pattern, item.owner, item.excludes))
    if not unique and not findings:
        findings.append(Finding("OWNERSHIP_EMPTY", "ownership registry contains no rules", ".koa/path-ownership.json"))
    return unique, findings


def check_path_ownership(
    root: str | Path | None = None,
    *,
    paths: Iterable[str] | None = None,
) -> CheckResult:
    """Check that every structural file has exactly one canonical owner."""

    base = repository_root(root)
    registry_path = base / ".koa" / "path-ownership.json"
    data, findings = load_json_object(registry_path, code_prefix="OWNERSHIP_REGISTRY")
    if data is None:
        return CheckResult.build("path-ownership", findings, {"checked_paths": 0, "rules": 0})
    rules, parse_findings = parse_ownership_rules(data)
    findings.extend(parse_findings)
    candidates = sorted(
        {
            normalize_repository_path(path)
            for path in (paths if paths is not None else iter_repository_files(base))
        },
        key=str.casefold,
    )
    ignored = set(_string_list(data.get("ignored_paths")) or _string_list(data.get("ignore")))
    normalized_ignored: set[str] = set()
    for value in sorted(ignored):
        try:
            normalized_ignored.add(normalize_repository_path(value))
        except ValueError as exc:
            findings.append(Finding("OWNERSHIP_IGNORE_INVALID", str(exc), ".koa/path-ownership.json"))

    owner_counts: dict[str, int] = {}
    for path in candidates:
        if any(_matches_pattern(path, pattern) for pattern in normalized_ignored):
            continue
        owners = sorted({rule.owner for rule in rules if rule.matches(path)})
        if not owners:
            findings.append(
                Finding(
                    "PATH_OWNER_MISSING",
                    "path has no declared canonical owner",
                    path,
                    hint="add one explicit ownership rule in .koa/path-ownership.json",
                )
            )
        elif len(owners) > 1:
            findings.append(
                Finding(
                    "PATH_OWNER_OVERLAP",
                    f"path has multiple active owners: {', '.join(owners)}",
                    path,
                    hint="split or exclude overlapping ownership rules",
                )
            )
        else:
            owner_counts[owners[0]] = owner_counts.get(owners[0], 0) + 1

    return CheckResult.build(
        "path-ownership",
        findings,
        {
            "checked_paths": len(candidates),
            "owners": len(owner_counts),
            "rules": len(rules),
        },
    )


check = check_path_ownership


__all__ = ["OwnershipRule", "check", "check_path_ownership", "parse_ownership_rules"]
