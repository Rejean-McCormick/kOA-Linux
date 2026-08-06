"""Deterministic, authority-aware diagnostics for kOA assembly.

Diagnostics are data, not log strings.  Every diagnostic identifies the authority
that justifies it and the source location that triggered it.  This allows callers
to render text, JSON, or evidence without losing the canonical source.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Iterable, Iterator, Mapping, Sequence


class Severity(StrEnum):
    """Severity used by assembly validation."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class Diagnostic:
    """One deterministic diagnostic tied to an authority source."""

    code: str
    severity: Severity
    message: str
    authority: str
    source_path: str
    pointer: str = ""
    hint: str = ""
    context: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        for field_name in ("code", "message", "authority", "source_path"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")
        if not isinstance(self.severity, Severity):
            object.__setattr__(self, "severity", Severity(self.severity))
        normalized_context: list[tuple[str, str]] = []
        seen: set[str] = set()
        for key, value in self.context:
            key = str(key).strip()
            if not key or key in seen:
                raise ValueError("diagnostic context keys must be unique and non-empty")
            seen.add(key)
            normalized_context.append((key, str(value)))
        object.__setattr__(self, "context", tuple(sorted(normalized_context)))

    @property
    def sort_key(self) -> tuple[int, str, str, str, str]:
        severity_rank = {
            Severity.ERROR: 0,
            Severity.WARNING: 1,
            Severity.INFO: 2,
        }
        return (
            severity_rank[self.severity],
            self.source_path,
            self.pointer,
            self.code,
            self.message,
        )

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "code": self.code,
            "severity": self.severity.value,
            "message": self.message,
            "authority": self.authority,
            "source_path": self.source_path,
        }
        if self.pointer:
            payload["pointer"] = self.pointer
        if self.hint:
            payload["hint"] = self.hint
        if self.context:
            payload["context"] = dict(self.context)
        return payload


@dataclass(slots=True)
class DiagnosticBag:
    """Mutable collector whose public iteration is always deterministic."""

    _items: list[Diagnostic] = field(default_factory=list)

    def add(self, diagnostic: Diagnostic) -> Diagnostic:
        if not isinstance(diagnostic, Diagnostic):
            raise TypeError("diagnostic must be a Diagnostic")
        self._items.append(diagnostic)
        return diagnostic

    def error(
        self,
        code: str,
        message: str,
        *,
        authority: str,
        source_path: str,
        pointer: str = "",
        hint: str = "",
        context: Mapping[str, object] | None = None,
    ) -> Diagnostic:
        return self.add(
            Diagnostic(
                code=code,
                severity=Severity.ERROR,
                message=message,
                authority=authority,
                source_path=source_path,
                pointer=pointer,
                hint=hint,
                context=_normalize_context(context),
            )
        )

    def warning(
        self,
        code: str,
        message: str,
        *,
        authority: str,
        source_path: str,
        pointer: str = "",
        hint: str = "",
        context: Mapping[str, object] | None = None,
    ) -> Diagnostic:
        return self.add(
            Diagnostic(
                code=code,
                severity=Severity.WARNING,
                message=message,
                authority=authority,
                source_path=source_path,
                pointer=pointer,
                hint=hint,
                context=_normalize_context(context),
            )
        )

    def info(
        self,
        code: str,
        message: str,
        *,
        authority: str,
        source_path: str,
        pointer: str = "",
        hint: str = "",
        context: Mapping[str, object] | None = None,
    ) -> Diagnostic:
        return self.add(
            Diagnostic(
                code=code,
                severity=Severity.INFO,
                message=message,
                authority=authority,
                source_path=source_path,
                pointer=pointer,
                hint=hint,
                context=_normalize_context(context),
            )
        )

    def extend(self, diagnostics: Iterable[Diagnostic]) -> None:
        for diagnostic in diagnostics:
            self.add(diagnostic)

    @property
    def has_errors(self) -> bool:
        return any(item.severity is Severity.ERROR for item in self._items)

    @property
    def error_count(self) -> int:
        return sum(item.severity is Severity.ERROR for item in self._items)

    @property
    def warning_count(self) -> int:
        return sum(item.severity is Severity.WARNING for item in self._items)

    def sorted(self) -> tuple[Diagnostic, ...]:
        return tuple(sorted(self._items, key=lambda item: item.sort_key))

    def to_dict(self) -> dict[str, Any]:
        return {
            "result": "blocked" if self.has_errors else "pass",
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "diagnostics": [item.to_dict() for item in self.sorted()],
        }

    def render_text(self) -> str:
        lines: list[str] = []
        for item in self.sorted():
            location = item.source_path + item.pointer
            lines.append(
                f"{item.severity.value.upper()} {item.code} {location}: {item.message} "
                f"[authority: {item.authority}]"
            )
            if item.hint:
                lines.append(f"  hint: {item.hint}")
            for key, value in item.context:
                lines.append(f"  {key}: {value}")
        result = "BLOCKED" if self.has_errors else "PASS"
        lines.append(
            f"{result}: {self.error_count} error(s), {self.warning_count} warning(s)"
        )
        return "\n".join(lines)

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[Diagnostic]:
        return iter(self.sorted())


class AssemblyDiagnosticError(RuntimeError):
    """Raised when strict loading cannot return an authoritative result."""

    def __init__(self, message: str, diagnostics: Sequence[Diagnostic]) -> None:
        self.diagnostics = tuple(sorted(diagnostics, key=lambda item: item.sort_key))
        super().__init__(message)


def _normalize_context(
    context: Mapping[str, object] | None,
) -> tuple[tuple[str, str], ...]:
    if not context:
        return ()
    return tuple(sorted((str(key), str(value)) for key, value in context.items()))
