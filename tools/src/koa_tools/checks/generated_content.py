"""Validation of generated repository content and its declared provenance."""
from __future__ import annotations

from dataclasses import dataclass
import fnmatch
import hashlib
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
class GeneratedRule:
    pattern: str
    source: str | None = None
    renderer: str | None = None
    sha256: str | None = None

    def matches(self, path: str) -> bool:
        if any(character in self.pattern for character in "*?["):
            return fnmatch.fnmatchcase(path, self.pattern)
        return path == self.pattern or path.startswith(self.pattern + "/")


def _rule_from_mapping(pattern: str, value: Mapping[str, Any]) -> GeneratedRule:
    source = value.get("source") or value.get("canonical_source")
    renderer = value.get("renderer") or value.get("generator")
    digest = value.get("sha256") or value.get("digest")
    if isinstance(digest, str) and digest.startswith("sha256:"):
        digest = digest.partition(":")[2]
    return GeneratedRule(
        normalize_repository_path(pattern),
        source if isinstance(source, str) and source else None,
        renderer if isinstance(renderer, str) and renderer else None,
        digest.lower() if isinstance(digest, str) and digest else None,
    )


def parse_generated_rules(data: Mapping[str, Any]) -> tuple[list[GeneratedRule], list[Finding]]:
    findings: list[Finding] = []
    rules: list[GeneratedRule] = []
    raw = first_sequence(data, ("entries", "rules", "generated_paths", "paths"))
    if raw is not None:
        for index, item in enumerate(raw):
            if isinstance(item, str):
                rules.append(GeneratedRule(normalize_repository_path(item)))
                continue
            if not isinstance(item, dict):
                findings.append(Finding("GENERATED_RULE_SHAPE", f"entry {index} must be a string or object", ".koa/generated-paths.json"))
                continue
            pattern = item.get("path") or item.get("pattern") or item.get("glob") or item.get("root")
            if not isinstance(pattern, str) or not pattern:
                findings.append(Finding("GENERATED_RULE_PATH", f"entry {index} has no path", ".koa/generated-paths.json"))
                continue
            try:
                rules.append(_rule_from_mapping(pattern, item))
            except ValueError as exc:
                findings.append(Finding("GENERATED_RULE_INVALID_PATH", f"entry {index}: {exc}", ".koa/generated-paths.json"))
    else:
        mapping = first_mapping(data, ("generated", "path_metadata", "files"))
        if mapping is None:
            findings.append(Finding("GENERATED_REGISTRY_SHAPE", "registry must contain entries/rules/paths or a generated mapping", ".koa/generated-paths.json"))
        else:
            for pattern, value in sorted(mapping.items()):
                if value is True or value is None:
                    value = {}
                if not isinstance(value, dict):
                    findings.append(Finding("GENERATED_RULE_SHAPE", f"metadata for {pattern!r} must be an object", ".koa/generated-paths.json"))
                    continue
                try:
                    rules.append(_rule_from_mapping(pattern, value))
                except ValueError as exc:
                    findings.append(Finding("GENERATED_RULE_INVALID_PATH", str(exc), ".koa/generated-paths.json"))
    return sorted(set(rules), key=lambda item: (item.pattern, item.source or "", item.renderer or "")), findings


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_generated_content(
    root: str | Path | None = None,
    *,
    paths: Iterable[str] | None = None,
) -> CheckResult:
    """Validate declarations, provenance references, and optional content digests."""

    base = repository_root(root)
    data, findings = load_json_object(base / ".koa" / "generated-paths.json", code_prefix="GENERATED_REGISTRY")
    if data is None:
        return CheckResult.build("generated-content", findings, {"checked_paths": 0, "rules": 0})
    rules, parse_findings = parse_generated_rules(data)
    findings.extend(parse_findings)
    candidates = sorted(
        {normalize_repository_path(path) for path in (paths if paths is not None else iter_repository_files(base))},
        key=str.casefold,
    )

    declared_matches = 0
    for path in candidates:
        matched = [rule for rule in rules if rule.matches(path)]
        if path.startswith("generated/") and path not in {"generated/README.md", "generated/.gitignore"} and not matched:
            findings.append(
                Finding(
                    "GENERATED_PATH_UNDECLARED",
                    "file under generated/ is not declared by .koa/generated-paths.json",
                    path,
                )
            )
            continue
        if len(matched) > 1:
            findings.append(
                Finding(
                    "GENERATED_PATH_OVERLAP",
                    f"file matches multiple generated declarations: {', '.join(rule.pattern for rule in matched)}",
                    path,
                )
            )
        if not matched:
            continue
        declared_matches += 1
        rule = matched[0]
        if rule.source:
            try:
                source = normalize_repository_path(rule.source.split("#", 1)[0])
            except ValueError as exc:
                findings.append(Finding("GENERATED_SOURCE_INVALID", str(exc), path))
            else:
                if not (base / source).is_file():
                    findings.append(Finding("GENERATED_SOURCE_MISSING", f"canonical source does not exist: {source}", path))
        if rule.sha256:
            if len(rule.sha256) != 64 or any(character not in "0123456789abcdef" for character in rule.sha256):
                findings.append(Finding("GENERATED_DIGEST_INVALID", "declared sha256 must be 64 lowercase hexadecimal characters", path))
            elif (base / path).is_file() and _sha256(base / path) != rule.sha256:
                findings.append(Finding("GENERATED_CONTENT_STALE", "content digest does not match the declared generated state", path))

    for rule in rules:
        if not any(rule.matches(path) for path in candidates):
            findings.append(Finding("GENERATED_DECLARATION_EMPTY", "generated declaration matches no committed file", rule.pattern))

    return CheckResult.build(
        "generated-content",
        findings,
        {"checked_paths": len(candidates), "declared_matches": declared_matches, "rules": len(rules)},
    )


check = check_generated_content


__all__ = ["GeneratedRule", "check", "check_generated_content", "parse_generated_rules"]
