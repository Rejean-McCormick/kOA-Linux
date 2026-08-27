"""Minimal stable command dispatcher for kOA repository tooling."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from enum import IntEnum
from importlib import import_module
import os
from pathlib import Path
import sys
from types import ModuleType
from typing import Sequence, TextIO

from koa_tools import __version__

PROGRAM_NAME = "koa"
ROOT_MARKERS = ("pyproject.toml", "uv.lock", ".python-version")


class ExitCode(IntEnum):
    """Stable process exit codes exposed by the root CLI."""

    OK = 0
    USAGE = 2
    UNAVAILABLE = 69
    SOFTWARE = 70
    INTERRUPTED = 130


@dataclass(frozen=True, slots=True)
class CommandSpec:
    """One closed command entry in the repository-tooling catalog."""

    name: str
    module: str
    summary: str


COMMANDS: tuple[CommandSpec, ...] = (
    CommandSpec("validate", "koa_tools.commands.validate", "validate repository state"),
    CommandSpec("generate", "koa_tools.commands.generate", "generate declared content"),
    CommandSpec("assemble", "koa_tools.commands.assemble", "assemble a declared profile"),
    CommandSpec("build-image", "koa_tools.commands.build_image", "build a system image"),
    CommandSpec("build-bundle", "koa_tools.commands.build_bundle", "build an offline bundle"),
    CommandSpec("verify", "koa_tools.commands.verify", "verify artifacts and evidence"),
    CommandSpec("test", "koa_tools.commands.test", "run registered test suites"),
    CommandSpec("release", "koa_tools.commands.release", "run release orchestration"),
    CommandSpec("diagnose", "koa_tools.commands.diagnose", "collect repository diagnostics"),
)
_COMMANDS_BY_NAME = {command.name: command for command in COMMANDS}


class UsageError(ValueError):
    """Raised for invalid root CLI arguments without terminating Python."""


class CommandUnavailableError(RuntimeError):
    """Raised when a catalogued command implementation is not present."""


class _ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise UsageError(message)


class _StableHelpFormatter(argparse.RawDescriptionHelpFormatter):
    def __init__(self, prog: str) -> None:
        super().__init__(prog, width=120, max_help_position=30)


def _command_help() -> str:
    width = max(len(command.name) for command in COMMANDS)
    return "\n".join(
        f"  {command.name:<{width}}  {command.summary}" for command in COMMANDS
    )


def build_parser() -> argparse.ArgumentParser:
    """Build the stable root parser without importing command modules."""

    parser = _ArgumentParser(
        prog=PROGRAM_NAME,
        add_help=False,
        description=(
            "kOA repository tooling. Root options must precede the command; "
            "command-specific options are passed to the command module."
        ),
        epilog=f"commands:\n{_command_help()}",
        formatter_class=_StableHelpFormatter,
    )
    parser.add_argument("-h", "--help", action="store_true", help="show this help")
    parser.add_argument(
        "--version", action="store_true", help="show the installed tooling version"
    )
    parser.add_argument(
        "--repository-root",
        metavar="PATH",
        help="explicit workspace root containing pyproject.toml, uv.lock, and .python-version",
    )
    parser.add_argument("command", nargs="?", choices=tuple(_COMMANDS_BY_NAME))
    parser.add_argument("command_args", nargs=argparse.REMAINDER)
    return parser


def _is_repository_root(path: Path) -> bool:
    return all((path / marker).is_file() for marker in ROOT_MARKERS)


def discover_repository_root(
    explicit_root: str | os.PathLike[str] | None = None,
    *,
    start: str | os.PathLike[str] | None = None,
) -> Path:
    """Resolve a workspace root using the canonical Python root markers."""

    if explicit_root is not None:
        candidate = Path(explicit_root).expanduser().resolve()
        if not candidate.exists():
            raise CommandUnavailableError(f"repository root does not exist: {candidate}")
        if not candidate.is_dir():
            raise CommandUnavailableError(
                f"repository root is not a directory: {candidate}"
            )
        if not _is_repository_root(candidate):
            missing = [marker for marker in ROOT_MARKERS if not (candidate / marker).is_file()]
            raise CommandUnavailableError(
                f"repository root {candidate} is missing required marker(s): "
                + ", ".join(missing)
            )
        return candidate

    candidate = Path.cwd() if start is None else Path(start)
    candidate = candidate.expanduser().resolve()
    if candidate.is_file():
        candidate = candidate.parent

    for directory in (candidate, *candidate.parents):
        if _is_repository_root(directory):
            return directory

    raise CommandUnavailableError(
        f"no repository root found from {candidate}; required markers: "
        + ", ".join(ROOT_MARKERS)
    )


def _load_command(spec: CommandSpec) -> ModuleType:
    try:
        return import_module(spec.module)
    except ModuleNotFoundError as exc:
        unavailable_names = {spec.module, "koa_tools.commands"}
        if exc.name in unavailable_names:
            raise CommandUnavailableError(
                f"command {spec.name!r} is catalogued but its module "
                f"{spec.module!r} is not present in this source revision"
            ) from exc
        raise


def _normalize_command_result(command: str, result: object) -> int:
    if isinstance(result, bool) or not isinstance(result, int):
        raise TypeError(
            f"command {command!r} returned {type(result).__name__}; an integer exit code is required"
        )
    if not 0 <= result <= 255:
        raise ValueError(
            f"command {command!r} returned exit code {result}; expected 0..255"
        )
    return result


def _system_exit_code(command: str, exc: SystemExit) -> int:
    if exc.code is None:
        return int(ExitCode.OK)
    if isinstance(exc.code, bool) or not isinstance(exc.code, int):
        raise TypeError(
            f"command {command!r} raised SystemExit with a non-integer code"
        ) from exc
    return _normalize_command_result(command, exc.code)


def main(
    argv: Sequence[str] | None = None,
    *,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
    start_directory: str | os.PathLike[str] | None = None,
) -> int:
    """Run the root CLI and return an exit code without calling ``sys.exit``."""

    output = sys.stdout if stdout is None else stdout
    errors = sys.stderr if stderr is None else stderr
    arguments = tuple(sys.argv[1:] if argv is None else argv)
    parser = build_parser()

    try:
        parsed = parser.parse_args(arguments)
    except UsageError as exc:
        print(f"{PROGRAM_NAME}: error: {exc}", file=errors)
        print(f"Try '{PROGRAM_NAME} --help' for usage.", file=errors)
        return int(ExitCode.USAGE)

    if parsed.help:
        print(parser.format_help(), end="", file=output)
        return int(ExitCode.OK)
    if parsed.version:
        print(f"koa-tools {__version__}", file=output)
        return int(ExitCode.OK)
    if parsed.command is None:
        print(parser.format_help(), end="", file=output)
        return int(ExitCode.OK)

    spec = _COMMANDS_BY_NAME[parsed.command]
    try:
        repository_root = discover_repository_root(
            parsed.repository_root,
            start=start_directory,
        )
        module = _load_command(spec)
        handler = getattr(module, "main", None)
        if not callable(handler):
            raise TypeError(f"module {spec.module!r} does not expose callable main")
        try:
            result = handler(tuple(parsed.command_args), repository_root=repository_root)
        except SystemExit as exc:
            return _system_exit_code(spec.name, exc)
        return _normalize_command_result(spec.name, result)
    except CommandUnavailableError as exc:
        print(f"{PROGRAM_NAME}: {exc}", file=errors)
        return int(ExitCode.UNAVAILABLE)
    except KeyboardInterrupt:
        print(f"{PROGRAM_NAME}: interrupted", file=errors)
        return int(ExitCode.INTERRUPTED)
    except Exception as exc:  # command boundary: convert defects to a stable CLI failure
        print(
            f"{PROGRAM_NAME}: {spec.name}: internal error: "
            f"{exc.__class__.__name__}: {exc}",
            file=errors,
        )
        return int(ExitCode.SOFTWARE)


if __name__ == "__main__":
    raise SystemExit(main())
