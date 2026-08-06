"""Repository discovery and containment-safe path resolution."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Final

from .config import ConfigurationError, JSONObject, load_json_object, normalize_repository_path

CONTROL_DIRECTORY: Final = ".koa"
CANONICAL_DOC_MARKERS: Final = (
    Path("docs/AI_CONTEXT.md"),
    Path("docs/contracts/system.contract.json"),
)


class RepositoryError(ConfigurationError):
    """Raised when a repository root or owned path cannot be resolved safely."""


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _resolved_existing_ancestor(path: Path) -> Path:
    cursor = path
    remainder: list[str] = []
    while not cursor.exists() and cursor != cursor.parent:
        remainder.append(cursor.name)
        cursor = cursor.parent
    try:
        resolved = cursor.resolve(strict=True)
    except OSError as exc:
        raise RepositoryError(f"cannot resolve path ancestor {cursor}: {exc}") from exc
    for name in reversed(remainder):
        resolved /= name
    return resolved


@dataclass(frozen=True, slots=True)
class Repository:
    """A validated kOA-Linux source repository root."""

    root: Path

    def __post_init__(self) -> None:
        try:
            resolved = self.root.expanduser().resolve(strict=True)
        except OSError as exc:
            raise RepositoryError(
                f"repository root cannot be resolved: {self.root}: {exc}"
            ) from exc
        if not resolved.is_dir():
            raise RepositoryError(f"repository root is not a directory: {resolved}")
        object.__setattr__(self, "root", resolved)

    @property
    def control_directory(self) -> Path:
        return self.root / CONTROL_DIRECTORY

    def resolve(self, relative_path: str, *, must_exist: bool = False) -> Path:
        """Resolve an owned repository path and reject lexical or symlink escape."""

        normalized = normalize_repository_path(relative_path, location="repository path")
        candidate = self.root
        for segment in normalized.split("/"):
            candidate /= segment
            if candidate.is_symlink():
                try:
                    target = candidate.resolve(strict=False)
                except OSError as exc:
                    raise RepositoryError(
                        f"cannot resolve symbolic link in repository path {relative_path}: {exc}"
                    ) from exc
                if not _is_relative_to(target, self.root):
                    raise RepositoryError(
                        "repository path escapes its owning root through a symbolic link: "
                        f"{relative_path}"
                    )
        resolved = _resolved_existing_ancestor(candidate)
        if not _is_relative_to(resolved, self.root):
            raise RepositoryError(
                f"repository path escapes its owning root through a symbolic link: {relative_path}"
            )
        if must_exist and not candidate.exists():
            raise RepositoryError(f"repository path does not exist: {relative_path}")
        if candidate.exists():
            try:
                actual = candidate.resolve(strict=True)
            except OSError as exc:
                raise RepositoryError(
                    f"cannot resolve repository path {relative_path}: {exc}"
                ) from exc
            if not _is_relative_to(actual, self.root):
                raise RepositoryError(
                    "repository path escapes its owning root through a symbolic link: "
                    f"{relative_path}"
                )
            return actual
        return candidate

    def control_path(self, filename: str, *, must_exist: bool = False) -> Path:
        if "/" in filename or "\\" in filename or filename in {"", ".", ".."}:
            raise RepositoryError(f"invalid control filename: {filename!r}")
        if not filename.endswith(".json"):
            raise RepositoryError(f"control filename must end in .json: {filename!r}")
        return self.resolve(f"{CONTROL_DIRECTORY}/{filename}", must_exist=must_exist)

    def load_control(self, filename: str) -> JSONObject:
        return load_json_object(self.control_path(filename, must_exist=True))


def _looks_like_repository(path: Path) -> bool:
    control_marker = path / CONTROL_DIRECTORY / "repository.json"
    if control_marker.is_file() and not control_marker.is_symlink():
        return True
    has_project = (path / "pyproject.toml").is_file()
    has_canonical_docs = all((path / marker).is_file() for marker in CANONICAL_DOC_MARKERS)
    return has_project and has_canonical_docs


def discover_repository(start: str | os.PathLike[str] | None = None) -> Repository:
    """Discover the closest repository root without crossing the filesystem root."""

    origin = Path.cwd() if start is None else Path(start).expanduser()
    if origin.exists() and origin.is_file():
        origin = origin.parent
    try:
        cursor = origin.resolve(strict=True)
    except OSError as exc:
        raise RepositoryError(
            f"repository discovery start cannot be resolved: {origin}: {exc}"
        ) from exc
    for candidate in (cursor, *cursor.parents):
        if _looks_like_repository(candidate):
            return Repository(candidate)
    raise RepositoryError(f"no kOA-Linux repository found from {origin}")
