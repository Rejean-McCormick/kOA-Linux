"""Static validation of repository dependency directions and local versions."""
from __future__ import annotations

import ast
from dataclasses import dataclass
import fnmatch
from pathlib import Path, PurePosixPath
import re
import tomllib
from typing import Any, Iterable, Mapping, Sequence

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
        return fnmatch.fnmatchcase(source, self.source) and fnmatch.fnmatchcase(
            target, self.target
        )


@dataclass(frozen=True, slots=True)
class LocalPythonProject:
    name: str
    normalized_name: str
    version_text: str
    version: tuple[int, ...]
    manifest: str
    requirements: tuple[str, ...]


_DISTRIBUTION_SEPARATOR = re.compile(r"[-_.]+")
_REQUIREMENT = re.compile(
    r"^\s*([A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?)"
    r"(?:\[[^\]]+\])?\s*(.*?)\s*$"
)
_RELEASE_VERSION = re.compile(r"^(0|[1-9][0-9]*)(?:\.(0|[1-9][0-9]*))*$")
_SPECIFIER = re.compile(r"^(===|==|!=|~=|>=|<=|>|<)\s*([^\s]+)$")


def _path_patterns(value: Any) -> tuple[str, ...]:
    if isinstance(value, str):
        return (value,)
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return tuple(value)
    return ()


def parse_dependency_rules(
    data: Mapping[str, Any],
) -> tuple[list[DependencyRule], list[Finding]]:
    findings: list[Finding] = []
    rules: list[DependencyRule] = []
    raw_rules = first_sequence(data, ("rules", "dependency_rules", "constraints")) or []
    for index, item in enumerate(raw_rules):
        if not isinstance(item, dict):
            findings.append(
                Finding(
                    "DEPENDENCY_RULE_SHAPE",
                    f"rule {index} must be an object",
                    ".koa/dependency-rules.json",
                )
            )
            continue
        sources = _path_patterns(item.get("source") or item.get("from") or item.get("sources"))
        denied = _path_patterns(
            item.get("deny") or item.get("denied_targets") or item.get("forbidden")
        )
        allowed = _path_patterns(item.get("allow") or item.get("allowed_targets"))
        reason = item.get("reason") if isinstance(item.get("reason"), str) else ""
        if not sources or (not denied and not allowed):
            findings.append(
                Finding(
                    "DEPENDENCY_RULE_FIELDS",
                    f"rule {index} requires source plus allow or deny targets",
                    ".koa/dependency-rules.json",
                )
            )
            continue
        try:
            normalized_sources = tuple(normalize_repository_path(value) for value in sources)
            normalized_denied = tuple(normalize_repository_path(value) for value in denied)
            normalized_allowed = tuple(normalize_repository_path(value) for value in allowed)
        except ValueError as exc:
            findings.append(
                Finding(
                    "DEPENDENCY_RULE_INVALID_PATH",
                    f"rule {index}: {exc}",
                    ".koa/dependency-rules.json",
                )
            )
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
                    rules.append(
                        DependencyRule(
                            normalize_repository_path(source),
                            normalize_repository_path(target),
                            True,
                        )
                    )
                except ValueError as exc:
                    findings.append(
                        Finding(
                            "DEPENDENCY_RULE_INVALID_PATH",
                            str(exc),
                            ".koa/dependency-rules.json",
                        )
                    )
    return sorted(
        set(rules), key=lambda item: (item.source, item.target, item.allowed)
    ), findings


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


def _normalize_distribution_name(value: str) -> str:
    return _DISTRIBUTION_SEPARATOR.sub("-", value).lower()


def _parse_release_version(value: str) -> tuple[int, ...] | None:
    if not _RELEASE_VERSION.fullmatch(value):
        return None
    return tuple(int(part) for part in value.split("."))


def _compare_release(left: Sequence[int], right: Sequence[int]) -> int:
    size = max(len(left), len(right))
    normalized_left = tuple(left) + (0,) * (size - len(left))
    normalized_right = tuple(right) + (0,) * (size - len(right))
    return (normalized_left > normalized_right) - (normalized_left < normalized_right)


def _compatible_upper_bound(version: tuple[int, ...]) -> tuple[int, ...]:
    if len(version) <= 2:
        return (version[0] + 1,)
    prefix = list(version[:-1])
    prefix[-1] += 1
    return tuple(prefix)


def _single_specifier_allows(
    version: tuple[int, ...], operator: str, requested: str
) -> bool | None:
    if operator in {"==", "!="} and requested.endswith(".*"):
        prefix = _parse_release_version(requested[:-2])
        if prefix is None:
            return None
        matches = tuple(version[: len(prefix)]) == prefix
        return matches if operator == "==" else not matches

    requested_version = _parse_release_version(requested)
    if requested_version is None:
        return None
    comparison = _compare_release(version, requested_version)
    if operator in {"==", "==="}:
        return comparison == 0
    if operator == "!=":
        return comparison != 0
    if operator == ">=":
        return comparison >= 0
    if operator == "<=":
        return comparison <= 0
    if operator == ">":
        return comparison > 0
    if operator == "<":
        return comparison < 0
    if operator == "~=":
        return comparison >= 0 and _compare_release(
            version, _compatible_upper_bound(requested_version)
        ) < 0
    return None


def _specifier_allows(version: tuple[int, ...], specifier: str) -> bool | None:
    if not specifier:
        return True
    outcomes: list[bool] = []
    for raw_clause in specifier.split(","):
        clause = raw_clause.strip()
        if not clause:
            continue
        match = _SPECIFIER.fullmatch(clause)
        if match is None:
            return None
        outcome = _single_specifier_allows(version, match.group(1), match.group(2))
        if outcome is None:
            return None
        outcomes.append(outcome)
    return all(outcomes)


def _parse_requirement(value: str) -> tuple[str, str] | None:
    requirement = value.split(";", 1)[0].strip()
    match = _REQUIREMENT.fullmatch(requirement)
    if match is None:
        return None
    name = _normalize_distribution_name(match.group(1))
    remainder = match.group(2).strip()
    if remainder.startswith("@"):
        return name, ""
    return name, remainder


def _requirement_strings(data: Mapping[str, Any]) -> tuple[str, ...]:
    values: list[str] = []
    project = data.get("project")
    if isinstance(project, Mapping):
        dependencies = project.get("dependencies")
        if isinstance(dependencies, list):
            values.extend(item for item in dependencies if isinstance(item, str))
        optional = project.get("optional-dependencies")
        if isinstance(optional, Mapping):
            for group in optional.values():
                if isinstance(group, list):
                    values.extend(item for item in group if isinstance(item, str))
    groups = data.get("dependency-groups")
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                values.extend(item for item in group if isinstance(item, str))
    return tuple(sorted(set(values), key=str.casefold))


def _discover_python_projects(
    base: Path, paths: Iterable[str]
) -> tuple[dict[str, LocalPythonProject], list[Finding]]:
    projects: dict[str, LocalPythonProject] = {}
    findings: list[Finding] = []
    manifests = sorted(
        relative for relative in paths if PurePosixPath(relative).name == "pyproject.toml"
    )
    for relative in manifests:
        absolute = base / relative
        try:
            data = tomllib.loads(absolute.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
            findings.append(
                Finding(
                    "DEPENDENCY_PYPROJECT_PARSE",
                    f"cannot parse Python project manifest: {exc}",
                    relative,
                )
            )
            continue
        project = data.get("project")
        if not isinstance(project, Mapping):
            continue
        name = project.get("name")
        version_text = project.get("version")
        if not isinstance(name, str) or not name.strip():
            findings.append(
                Finding(
                    "DEPENDENCY_LOCAL_PROJECT_NAME",
                    "local Python project has no valid project.name",
                    relative,
                )
            )
            continue
        if not isinstance(version_text, str) or not version_text.strip():
            findings.append(
                Finding(
                    "DEPENDENCY_LOCAL_PROJECT_VERSION",
                    "local Python project has no static project.version",
                    relative,
                )
            )
            continue
        version = _parse_release_version(version_text.strip())
        if version is None:
            findings.append(
                Finding(
                    "DEPENDENCY_LOCAL_PROJECT_VERSION",
                    f"local project version cannot be compared deterministically: {version_text}",
                    relative,
                )
            )
            continue
        normalized_name = _normalize_distribution_name(name.strip())
        candidate = LocalPythonProject(
            name=name.strip(),
            normalized_name=normalized_name,
            version_text=version_text.strip(),
            version=version,
            manifest=relative,
            requirements=_requirement_strings(data),
        )
        existing = projects.get(normalized_name)
        if existing is not None:
            findings.append(
                Finding(
                    "DEPENDENCY_LOCAL_PROJECT_DUPLICATE",
                    f"local project name duplicates {existing.manifest}",
                    relative,
                )
            )
            continue
        projects[normalized_name] = candidate
    return projects, findings


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
        if (
            len(target_parts) >= 2
            and target_parts[0] == "components"
            and target_parts[1] != source_component
        ):
            return "private cross-component import is prohibited"
        if "domain" in source_parts and target_parts and target_parts[0] in {
            "host",
            "profiles",
            "packaging",
            "release",
            "integrations",
            "assembly",
        }:
            return "component domain cannot depend on platform or integration implementation"
    if (
        len(source_parts) >= 2
        and source_parts[0] == "integrations"
        and len(target_parts) >= 2
        and target_parts[0] == "integrations"
        and target_parts[1] != source_parts[1]
    ):
        return "one integration cannot import another integration's private source"
    return None


def _rule_decision(
    rules: list[DependencyRule], source: str, target: str
) -> tuple[bool | None, str]:
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
    """Check imports, local versions, and path dependencies against direction rules."""

    base = repository_root(root)
    data, findings = load_json_object(
        base / ".koa" / "dependency-rules.json", code_prefix="DEPENDENCY_REGISTRY"
    )
    if data is None:
        return CheckResult.build("dependencies", findings, {"checked_edges": 0, "rules": 0})
    rules, parse_findings = parse_dependency_rules(data)
    findings.extend(parse_findings)
    candidates = sorted(
        {
            normalize_repository_path(path)
            for path in (paths if paths is not None else iter_repository_files(base))
        },
        key=str.casefold,
    )
    packages = _discover_python_packages(base, candidates)
    local_projects, project_findings = _discover_python_projects(base, candidates)
    findings.extend(project_findings)
    edges: set[tuple[str, str, str]] = set()
    local_requirements = 0

    for project in sorted(local_projects.values(), key=lambda item: item.manifest):
        for raw_requirement in project.requirements:
            parsed = _parse_requirement(raw_requirement)
            if parsed is None:
                continue
            target_name, specifier = parsed
            target = local_projects.get(target_name)
            if target is None or target.manifest == project.manifest:
                continue
            local_requirements += 1
            edges.add(
                (
                    project.manifest,
                    target.manifest,
                    f"Python dependency {raw_requirement}",
                )
            )
            outcome = _specifier_allows(target.version, specifier)
            if outcome is False:
                findings.append(
                    Finding(
                        "DEPENDENCY_LOCAL_VERSION_MISMATCH",
                        (
                            f"{raw_requirement} does not admit local "
                            f"{target.name} {target.version_text}"
                        ),
                        project.manifest,
                    )
                )
            elif outcome is None:
                findings.append(
                    Finding(
                        "DEPENDENCY_LOCAL_VERSION_UNCHECKED",
                        f"unsupported local version specifier in {raw_requirement}",
                        project.manifest,
                    )
                )

    for relative in candidates:
        absolute = base / relative
        if relative.endswith(".py") and absolute.is_file():
            imports, error = _python_imports(absolute)
            if error:
                findings.append(
                    Finding(
                        "DEPENDENCY_PYTHON_PARSE",
                        f"cannot parse Python source: {error}",
                        relative,
                    )
                )
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
                    findings.append(
                        Finding(
                            "DEPENDENCY_PATH_ESCAPE",
                            f"path dependency escapes repository: {match.group(1)}",
                            relative,
                        )
                    )
                else:
                    edges.add((relative, target, "Cargo path dependency"))

    for source, target, description in sorted(edges):
        decision, reason = _rule_decision(rules, source, target)
        default_reason = _default_forbidden(source, target)
        if decision is False or (decision is None and default_reason):
            message_reason = reason or default_reason or "dependency is denied by registry"
            findings.append(
                Finding(
                    "DEPENDENCY_PROHIBITED",
                    f"{description} targets {target}: {message_reason}",
                    source,
                )
            )

    return CheckResult.build(
        "dependencies",
        findings,
        {
            "checked_edges": len(edges),
            "local_python_projects": len(local_projects),
            "local_python_requirements": local_requirements,
            "python_packages": len(packages),
            "rules": len(rules),
        },
    )


check = check_dependencies


__all__ = [
    "DependencyRule",
    "LocalPythonProject",
    "check",
    "check_dependencies",
    "parse_dependency_rules",
]
