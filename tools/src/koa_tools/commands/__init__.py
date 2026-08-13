"""Command registration and safe process orchestration for :mod:`koa_tools`.

The command modules in this package deliberately contain orchestration only.
They validate a closed set of repository-relative inputs, construct an ordered
execution plan, and delegate domain work to the public generator, assembly,
host-image, and release entry points that own that work.
"""

from __future__ import annotations

import argparse
import os
import re
import shlex
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable, Mapping, Sequence

CANONICAL_PROFILES: tuple[str, ...] = (
    "user-lightweight",
    "developer-linux-workstation",
    "developer-windows-wsl",
    "sovereign-linux-node",
    "sovereign-hub",
    "build-farm",
    "control-plane",
    "high-assurance",
    "sovereign-offline",
    "appliance-shell",
)

CANONICAL_OVERLAYS: tuple[str, ...] = (
    "high-assurance",
    "sovereign-offline",
    "appliance-shell",
)

ASSEMBLY_RENDERERS: tuple[str, ...] = (
    "systemd",
    "quadlet",
    "compose",
    "kubernetes",
    "image",
    "offline-bundle",
)

RELEASE_CHANNELS: tuple[str, ...] = (
    "system",
    "services",
    "governance",
    "knowledge",
)

_IDENTIFIER = re.compile(r"[a-z0-9][a-z0-9._-]{0,127}\Z")


class CommandError(RuntimeError):
    """A deterministic, user-actionable command failure."""


@dataclass(frozen=True, slots=True)
class Invocation:
    """One public tool invocation in an ordered orchestration plan."""

    label: str
    argv: tuple[str, ...]
    required_paths: tuple[str, ...] = ()
    environment: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.label.strip():
            raise ValueError("invocation label cannot be empty")
        if not self.argv or not all(isinstance(part, str) and part for part in self.argv):
            raise ValueError("invocation argv must contain non-empty strings")


Configure = Callable[[argparse.ArgumentParser], None]
Execute = Callable[[argparse.Namespace], int]


@dataclass(frozen=True, slots=True)
class CommandDefinition:
    """Description consumed by the repository-level CLI from bundle B-0008."""

    name: str
    summary: str
    configure: Configure
    execute: Execute

    def __post_init__(self) -> None:
        if not _IDENTIFIER.fullmatch(self.name):
            raise ValueError(f"invalid command name: {self.name!r}")
        if not self.summary.strip():
            raise ValueError("command summary cannot be empty")


COMMAND_MODULES: tuple[str, ...] = (
    "generate",
    "assemble",
    "build_image",
    "build_component",
    "build_bundle",
    "release",
)


def add_repository_options(parser: argparse.ArgumentParser) -> None:
    """Add options shared by every orchestration command."""

    parser.add_argument(
        "--repository-root",
        type=Path,
        help="Repository root; defaults to the nearest parent containing docs/AI_CONTEXT.md.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate the plan and print invocations without executing them.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print every delegated invocation before execution.",
    )


def repository_root(explicit: Path | None = None) -> Path:
    """Resolve and validate the kOA repository root.

    Root discovery is intentionally anchored on the normative AI entry point;
    it does not infer a repository from an arbitrary ``.git`` directory.
    """

    if explicit is not None:
        candidates = (explicit,)
    else:
        current = Path.cwd().resolve()
        candidates = (current, *current.parents)

    for candidate in candidates:
        root = candidate.expanduser().resolve()
        if (root / "docs" / "AI_CONTEXT.md").is_file():
            return root

    requested = str(explicit) if explicit is not None else str(Path.cwd())
    raise CommandError(
        "unable to locate a kOA repository root from "
        f"{requested!r}; expected docs/AI_CONTEXT.md"
    )


def validate_identifier(value: str, *, label: str) -> str:
    """Validate a stable lowercase identifier accepted by build metadata."""

    if not _IDENTIFIER.fullmatch(value):
        raise CommandError(
            f"{label} must match {_IDENTIFIER.pattern!r}; received {value!r}"
        )
    return value


def repository_path(
    root: Path,
    value: str | Path,
    *,
    label: str,
    must_exist: bool = False,
    expected_kind: str | None = None,
    generated_output: bool = False,
) -> Path:
    """Resolve a repository-relative path without allowing traversal.

    ``generated_output`` additionally confines the path to ``generated/`` so
    orchestration never overwrites manually maintained source content.
    """

    raw = Path(value)
    if raw.is_absolute() or ".." in raw.parts or raw == Path("."):
        raise CommandError(f"{label} must be a non-empty repository-relative path")

    resolved = (root / raw).resolve(strict=False)
    try:
        relative = resolved.relative_to(root)
    except ValueError as exc:
        raise CommandError(f"{label} escapes the repository root: {value!s}") from exc

    if generated_output and (not relative.parts or relative.parts[0] != "generated"):
        raise CommandError(f"{label} must be located under generated/")

    if must_exist and not resolved.exists():
        raise CommandError(f"required {label} does not exist: {relative.as_posix()}")
    if expected_kind == "file" and resolved.exists() and not resolved.is_file():
        raise CommandError(f"{label} is not a file: {relative.as_posix()}")
    if expected_kind == "directory" and resolved.exists() and not resolved.is_dir():
        raise CommandError(f"{label} is not a directory: {relative.as_posix()}")

    return relative


def profile_settings_path(profile: str) -> str:
    if profile not in CANONICAL_PROFILES:
        raise CommandError(f"unsupported profile: {profile!r}")
    return f"profiles/implementation-settings/{profile}.toml"


def overlay_settings_paths(overlays: Iterable[str]) -> tuple[str, ...]:
    result: list[str] = []
    seen: set[str] = set()
    for overlay in overlays:
        if overlay not in CANONICAL_OVERLAYS:
            raise CommandError(f"unsupported overlay: {overlay!r}")
        if overlay in seen:
            raise CommandError(f"duplicate overlay: {overlay!r}")
        seen.add(overlay)
        result.append(f"profiles/overlays/{overlay}.toml")
    return tuple(result)


def source_date_epoch(value: int) -> str:
    if value < 0:
        raise CommandError("source-date-epoch must be a non-negative integer")
    return str(value)


def python_script(root: Path, relative_script: str, *arguments: str) -> tuple[str, ...]:
    script = repository_path(
        root,
        relative_script,
        label="Python entry point",
        must_exist=True,
        expected_kind="file",
    )
    return (sys.executable, script.as_posix(), *arguments)


def assembly_cli(*arguments: str) -> tuple[str, ...]:
    """Return the public assembly CLI invocation without importing its internals."""

    return ("uv", "run", "--project", "assembly", "python", "-m", "koa_assembly", *arguments)


def _validate_executable(argv0: str) -> None:
    if "/" in argv0 or "\\" in argv0:
        executable = Path(argv0)
        if not executable.exists():
            raise CommandError(f"required executable does not exist: {argv0}")
        return
    if shutil.which(argv0) is None:
        raise CommandError(f"required executable is not available on PATH: {argv0}")


def _stable_environment(extra: Mapping[str, str]) -> dict[str, str]:
    environment = dict(os.environ)
    environment.update(
        {
            "LANG": "C",
            "LC_ALL": "C",
            "PYTHONHASHSEED": "0",
            "TZ": "UTC",
        }
    )
    environment.update(extra)
    return environment


def run_plan(
    args: argparse.Namespace,
    invocations: Sequence[Invocation],
) -> int:
    """Validate and execute an ordered plan, stopping at the first failure."""

    root = repository_root(getattr(args, "repository_root", None))
    dry_run = bool(getattr(args, "dry_run", False))
    verbose = bool(getattr(args, "verbose", False))

    if not invocations:
        raise CommandError("the orchestration plan is empty")

    for index, invocation in enumerate(invocations, start=1):
        for path in invocation.required_paths:
            repository_path(
                root,
                path,
                label=f"input for {invocation.label}",
                must_exist=True,
            )
        _validate_executable(invocation.argv[0])

        display = shlex.join(invocation.argv)
        if dry_run or verbose:
            print(f"[{index}/{len(invocations)}] {invocation.label}: {display}")
        if dry_run:
            continue

        completed = subprocess.run(
            invocation.argv,
            cwd=root,
            env=_stable_environment(invocation.environment),
            check=False,
        )
        if completed.returncode != 0:
            raise CommandError(
                f"{invocation.label} failed with exit status {completed.returncode}"
            )

    return 0


def load_commands() -> tuple[CommandDefinition, ...]:
    """Load command definitions lazily to avoid CLI import cycles."""

    from . import assemble, build_bundle, build_component, build_image, generate, release

    definitions = (
        generate.COMMAND,
        assemble.COMMAND,
        build_image.COMMAND,
        build_component.COMMAND,
        build_bundle.COMMAND,
        release.COMMAND,
    )
    names = [definition.name for definition in definitions]
    if len(names) != len(set(names)):
        raise RuntimeError("duplicate koa_tools command name")
    return definitions


def register_commands(subparsers: argparse._SubParsersAction) -> tuple[CommandDefinition, ...]:
    """Register all bundle commands on the repository-level argparse parser."""

    definitions = load_commands()
    for definition in definitions:
        parser = subparsers.add_parser(definition.name, help=definition.summary)
        definition.configure(parser)
        parser.set_defaults(command_handler=definition.execute)
    return definitions


def standalone_main(
    definition: CommandDefinition,
    argv: Sequence[str] | None = None,
) -> int:
    """Run one command module directly for local validation and diagnostics."""

    parser = argparse.ArgumentParser(prog=f"koa {definition.name}", description=definition.summary)
    definition.configure(parser)
    args = parser.parse_args(argv)
    try:
        return definition.execute(args)
    except CommandError as exc:
        parser.error(str(exc))
        return 2  # pragma: no cover - argparse.error raises SystemExit


__all__ = [
    "ASSEMBLY_RENDERERS",
    "CANONICAL_OVERLAYS",
    "CANONICAL_PROFILES",
    "COMMAND_MODULES",
    "CommandDefinition",
    "CommandError",
    "Invocation",
    "RELEASE_CHANNELS",
    "add_repository_options",
    "assembly_cli",
    "load_commands",
    "overlay_settings_paths",
    "profile_settings_path",
    "python_script",
    "register_commands",
    "repository_path",
    "repository_root",
    "run_plan",
    "source_date_epoch",
    "standalone_main",
    "validate_identifier",
]
