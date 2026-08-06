"""Deterministic repository architecture checks.

The public objects in this module are deliberately small so command modules and
future CI wrappers can consume the same result model without depending on a
hosted runner.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum
import json
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Iterator, Mapping, Sequence


class Severity(IntEnum):
    """Severity ordering used to compute a process exit status."""

    INFO = 10
    WARNING = 20
    ERROR = 30


@dataclass(frozen=True, order=True, slots=True)
class Finding:
    """One actionable and stable validation diagnostic."""

    sort_key: tuple[str, str, str] = field(init=False, repr=False, compare=True)
    code: str = field(compare=False)
    message: str = field(compare=False)
    path: str = field(default="", compare=False)
    severity: Severity = field(default=Severity.ERROR, compare=False)
    hint: str | None = field(default=None, compare=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "sort_key", (self.path, self.code, self.message))

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "code": self.code,
            "severity": self.severity.name.lower(),
            "message": self.message,
        }
        if self.path:
            payload["path"] = self.path
        if self.hint:
            payload["hint"] = self.hint
        return payload


@dataclass(frozen=True, slots=True)
class CheckResult:
    """Complete outcome of one architecture check."""

    check_id: str
    findings: tuple[Finding, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def build(
        cls,
        check_id: str,
        findings: Iterable[Finding],
        metadata: Mapping[str, Any] | None = None,
    ) -> "CheckResult":
        return cls(check_id, tuple(sorted(set(findings))), metadata or {})

    @property
    def errors(self) -> tuple[Finding, ...]:
        return tuple(item for item in self.findings if item.severity >= Severity.ERROR)

    @property
    def warnings(self) -> tuple[Finding, ...]:
        return tuple(item for item in self.findings if item.severity == Severity.WARNING)

    @property
    def ok(self) -> bool:
        return not self.errors

    @property
    def exit_code(self) -> int:
        return 0 if self.ok else 1

    def to_dict(self) -> dict[str, Any]:
        return {
            "check_id": self.check_id,
            "status": "pass" if self.ok else "fail",
            "counts": {
                "errors": len(self.errors),
                "warnings": len(self.warnings),
                "findings": len(self.findings),
            },
            "findings": [item.to_dict() for item in self.findings],
            "metadata": dict(sorted(self.metadata.items())),
        }


IGNORED_DIRECTORY_NAMES = frozenset(
    {
        ".git",
        ".hg",
        ".svn",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".tox",
        ".venv",
        "__pycache__",
        "node_modules",
        "target",
    }
)
IGNORED_FILE_NAMES = frozenset({".DS_Store"})


def repository_root(value: str | Path | None = None) -> Path:
    """Return an absolute repository root without requiring it to be Git-backed."""

    return Path(value or ".").expanduser().resolve()


def normalize_repository_path(value: str | Path) -> str:
    """Normalize and validate one repository-relative POSIX path."""

    raw = str(value).replace("\\", "/").strip()
    if raw.startswith("./"):
        raw = raw[2:]
    path = PurePosixPath(raw)
    if not raw or path.is_absolute() or ".." in path.parts:
        raise ValueError(f"invalid repository-relative path: {value!r}")
    normalized = path.as_posix().rstrip("/")
    if normalized in {"", "."}:
        raise ValueError(f"invalid repository-relative path: {value!r}")
    return normalized


def iter_repository_files(root: Path) -> Iterator[str]:
    """Yield regular repository files in stable lexical order.

    Symlinks are yielded as paths but never followed. Escaping symlinks are
    diagnosed by the architecture check rather than silently traversed.
    """

    discovered: list[str] = []
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if any(part in IGNORED_DIRECTORY_NAMES for part in relative.parts[:-1]):
            continue
        if path.name in IGNORED_FILE_NAMES:
            continue
        if path.is_file() or path.is_symlink():
            discovered.append(relative.as_posix())
    yield from sorted(set(discovered), key=str.casefold)


def load_json_object(path: Path, *, code_prefix: str) -> tuple[dict[str, Any] | None, list[Finding]]:
    """Load a JSON object and return diagnostics instead of raising."""

    if ".koa" in path.parts:
        relative = PurePosixPath(*path.parts[path.parts.index(".koa") :]).as_posix()
    else:
        relative = path.name
    if not path.exists():
        return None, [
            Finding(
                f"{code_prefix}_MISSING",
                "required registry is missing",
                relative,
                hint="complete the prerequisite bundle that owns this registry",
            )
        ]
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, [Finding(f"{code_prefix}_INVALID_JSON", f"cannot load JSON: {exc}", relative)]
    if not isinstance(value, dict):
        return None, [Finding(f"{code_prefix}_INVALID_SHAPE", "registry root must be a JSON object", relative)]
    return value, []


def first_sequence(mapping: Mapping[str, Any], names: Sequence[str]) -> list[Any] | None:
    """Return the first list-valued field among compatible registry names."""

    for name in names:
        value = mapping.get(name)
        if isinstance(value, list):
            return value
    return None


def first_mapping(mapping: Mapping[str, Any], names: Sequence[str]) -> Mapping[str, Any] | None:
    """Return the first object-valued field among compatible registry names."""

    for name in names:
        value = mapping.get(name)
        if isinstance(value, dict):
            return value
    return None


def render_text(results: Sequence[CheckResult], *, verbose: bool = False) -> str:
    """Render stable human-readable output for local CLI and CI."""

    lines: list[str] = []
    for result in results:
        lines.append(f"{result.check_id}: {'pass' if result.ok else 'fail'}")
        if verbose or not result.ok:
            for finding in result.findings:
                location = f" {finding.path}:" if finding.path else ""
                lines.append(
                    f"  {finding.severity.name} {finding.code}:{location} {finding.message}"
                )
                if finding.hint:
                    lines.append(f"    hint: {finding.hint}")
    error_count = sum(len(item.errors) for item in results)
    warning_count = sum(len(item.warnings) for item in results)
    lines.append(
        f"architecture-checks: {'pass' if error_count == 0 else 'fail'} "
        f"({error_count} error(s), {warning_count} warning(s))"
    )
    return "\n".join(lines)


def combined_exit_code(results: Sequence[CheckResult], *, warnings_as_errors: bool = False) -> int:
    """Return a deterministic process status for a collection of checks."""

    if any(not result.ok for result in results):
        return 1
    if warnings_as_errors and any(result.warnings for result in results):
        return 1
    return 0


__all__ = [
    "CheckResult",
    "Finding",
    "Severity",
    "combined_exit_code",
    "first_mapping",
    "first_sequence",
    "iter_repository_files",
    "load_json_object",
    "normalize_repository_path",
    "render_text",
    "repository_root",
]
