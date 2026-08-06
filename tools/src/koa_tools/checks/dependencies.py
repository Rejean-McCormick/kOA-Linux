"""Static validation of repository dependency directions."""
from __future__ import annotations

import ast
from dataclasses import dataclass
import fnmatch
from pathlib import Path, PurePosixPath
import re
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
class DependencyRule:
    source: str
    target: str
    allowed: bool
    reason: str = ""

    def applies(self, source: str, target: str) -> bool:
        return fnmatch.fnmatchcase(source, self.source) and fnmatch.fnmatchcase(target, self.target)


def _path_patterns(value: Any) -> tuple[str, ...]:
    if isinstance(value, str):
        return (value,)
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return tuple(value)
    return ()


def parse_dependency_rules(data: Mapping[str, Any]) -> tuple[list[DependencyRule], list[Finding]]:
    findings: list[Finding] = []
    rules: list[DependencyRule] = []
    raw_rules = first_sequence(data, ("rules", "dependency_rules", "constraints")) or []
    for index, item in enumerate(raw_rules):
        if not isinstance(item, dict):
            findings.append(Finding("DEPENDENCY_RULE_SHAPE", f"rule {index} must be an object", ".koa/dependency-rules.json"))
            continue
        sources = _path_patterns(item.get("source") or item.get("from") or item.get("sources"))
        denied = _path_patterns(item.get("deny") or item.get("denied_targets") or item.get("forbidden"))
        allowed = _path_patterns(item.get("allow") or item.get("allowed_targets"))
        reason = item.get("reason") if isinstance(item.get("reason"), str) else ""
        if not sources or (not denied and not allowed):
            findings.append(Finding("DEPENDENCY_RULE_FIELDS", f"rule {index} requires source plus allow or deny targets", ".koa/dependency-rules.json"))
            continue
        try:
            normalized_sources = tuple(normalize_repository_path(value) for value in sources)
            normalized_denied = tuple(normalize_repository_path(value) for value in denied)
            normalized_allowed = tuple(normalize_repository_path(value) for value in allowed)
        except ValueError as exc:
            findings.append(Finding("DEPENDENCY_RULE_INVALID_PATH", f"rule {index}: {exc}", ".koa/dependency-rules.json"))
            continue
        for source in normalized_sources:
            for target in normalized_denied:
                rules.append(DependencyRule(source, target, False, reason))
            for target in normalized_allowed:
                rules.append(DependencyRule(source, target, True, reason))

    matrix = first_mapping(data, ("allowed_dependencies", "allowed", "dependency_matrix"))
    if matrix is not None:
        for source, targets in sorted(matrix.items()):
            for target in _path_patterns(targets):
                try:
                    rules.append(DependencyRule(normalize_repository_path(source), normalize_repository_path(target), True))
                except ValueError as exc:
                    findings.append(Finding("DEPENDENCY_RULE_INVALID_PATH", str(exc), ".koa/dependency-rules.json"))
    return sorted(set(rules), key=lambda item: (item.source, item.target, item.allowed)), findings


def _discover_python_packages(base: Path, paths: Iterable[str]) -> dict[str, str]:
    packages: dict[str, str] = {}
    for relative in paths:
        parts = PurePosixPath(relative).parts
        if "src" not in parts or not relative.endswith(".py"):
            continue
        source_index = parts.index("src")
        if source_index + 1 >= len(parts):
            continue
        package = parts[source_index + 1]
        if package.isidentifier():
            packages.setdefault(package, "/".join(parts[: source_index + 2]))
    return packages


def _python_imports(path: Path) -> tuple[set[str], str | None]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=path.as_posix())
    except (OSError, UnicodeError, SyntaxError) as exc:
        return set(), str(exc)
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            imports.add(node.module.split(".", 1)[0])
    return imports, None


def _default_forbidden(source: str, target: str) -> str | None:
    source_parts = PurePosixPath(source).parts
    target_parts = PurePosixPath(target).parts
    if len(source_parts) >= 2 and source_parts[0] == "components":
        source_component = source_parts[1]
        if len(target_parts) >= 2 and target_parts[0] == "components" and target_parts[1] != source_component:
            return "private cross-component import is prohibited"
        if "domain" in source_parts and target_parts and target_parts[0] in {"host", "profiles", "packaging", "release", "integrations", "assembly"}:
            return "component domain cannot depend on platform or integration implementation"
    if len(source_parts) >= 2 and source_parts[0] == "integrations" and len(target_parts) >= 2 and target_parts[0] == "integrations" and target_parts[1] != source_parts[1]:
        return "one integration cannot import another integration's private source"
    return None


def _rule_decision(rules: list[DependencyRule], source: str, target: str) -> tuple[bool | None, str]:
    matching = [rule for rule in rules if rule.applies(source, target)]
    denied = [rule for rule in matching if not rule.allowed]
    if denied:
        return False, denied[0].reason
    allowed = [rule for rule in matching if rule.allowed]
    if allowed:
        return True, allowed[0].reason
    return None, ""


def _resolve_toml_path_dependency(source: Path, raw_target: str, base: Path) -> str | None:
    candidate = (source.parent / raw_target).resolve()
    try:
        return candidate.relative_to(base).as_posix()
    except ValueError:
        return None


def check_dependencies(
    root: str | Path | None = None,
    *,
    paths: Iterable[str] | None = None,
) -> CheckResult:
    """Check static imports and path dependencies against declared direction rules."""

    base = repository_root(root)
    data, findings = load_json_object(base / ".koa" / "dependency-rules.json", code_prefix="DEPENDENCY_REGISTRY")
    if data is None:
        return CheckResult.build("dependencies", findings, {"checked_edges": 0, "rules": 0})
    rules, parse_findings = parse_dependency_rules(data)
    findings.extend(parse_findings)
    candidates = sorted(
        {normalize_repository_path(path) for path in (paths if paths is not None else iter_repository_files(base))},
        key=str.casefold,
    )
    packages = _discover_python_packages(base, candidates)
    edges: set[tuple[str, str, str]] = set()

    for relative in candidates:
        absolute = base / relative
        if relative.endswith(".py") and absolute.is_file():
            imports, error = _python_imports(absolute)
            if error:
                findings.append(Finding("DEPENDENCY_PYTHON_PARSE", f"cannot parse Python source: {error}", relative))
                continue
            for imported in sorted(imports):
                target = packages.get(imported)
                if target:
                    edges.add((relative, target, f"Python import {imported}"))
        elif relative.endswith("Cargo.toml") and absolute.is_file():
            try:
                text = absolute.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                findings.append(Finding("DEPENDENCY_TOML_READ", str(exc), relative))
                continue
            for match in re.finditer(r"\bpath\s*=\s*['\"]([^'\"]+)['\"]", text):
                target = _resolve_toml_path_dependency(absolute, match.group(1), base)
                if target is None:
                    findings.append(Finding("DEPENDENCY_PATH_ESCAPE", f"path dependency escapes repository: {match.group(1)}", relative))
                else:
                    edges.add((relative, target, "Cargo path dependency"))

    for source, target, description in sorted(edges):
        decision, reason = _rule_decision(rules, source, target)
        default_reason = _default_forbidden(source, target)
        if decision is False or (decision is None and default_reason):
            message_reason = reason or default_reason or "dependency is denied by registry"
            findings.append(Finding("DEPENDENCY_PROHIBITED", f"{description} targets {target}: {message_reason}", source))

    return CheckResult.build(
        "dependencies",
        findings,
        {"checked_edges": len(edges), "python_packages": len(packages), "rules": len(rules)},
    )


check = check_dependencies


__all__ = ["DependencyRule", "check", "check_dependencies", "parse_dependency_rules"]
