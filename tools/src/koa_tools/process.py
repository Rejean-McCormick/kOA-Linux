"""Safe, deterministic subprocess execution for repository tooling.

This module deliberately accepts argument vectors only.  It never invokes a
shell, never logs environment values, and captures process output so callers
can decide what evidence is safe to expose.
"""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import shlex
import subprocess
from typing import Mapping, Sequence

CommandArgument = str | os.PathLike[str]
EnvironmentValue = str | None


@dataclass(frozen=True, slots=True)
class ProcessResult:
    """Immutable result of one completed process invocation."""

    argv: tuple[str, ...]
    cwd: Path
    returncode: int
    stdout: str
    stderr: str

    @property
    def succeeded(self) -> bool:
        """Whether the process exited successfully."""

        return self.returncode == 0

    @property
    def command(self) -> str:
        """Human-readable command representation for diagnostics only."""

        return shlex.join(self.argv)


class ProcessError(RuntimeError):
    """Base class for process failures produced by this module."""


class ProcessStartError(ProcessError):
    """Raised when the operating system cannot start a process."""

    def __init__(self, argv: tuple[str, ...], cwd: Path, cause: OSError) -> None:
        self.argv = argv
        self.cwd = cwd
        self.cause = cause
        super().__init__(
            f"could not start {shlex.join(argv)} in {cwd}: "
            f"{cause.__class__.__name__}: {cause}"
        )


class ProcessTimeoutError(ProcessError):
    """Raised when a process exceeds its declared timeout."""

    def __init__(
        self,
        argv: tuple[str, ...],
        cwd: Path,
        timeout: float,
        stdout: str,
        stderr: str,
    ) -> None:
        self.argv = argv
        self.cwd = cwd
        self.timeout = timeout
        self.stdout = stdout
        self.stderr = stderr
        super().__init__(
            f"process timed out after {timeout:g}s: {shlex.join(argv)}"
        )


class ProcessExecutionError(ProcessError):
    """Raised when a completed process returns a non-zero exit code."""

    def __init__(self, result: ProcessResult) -> None:
        self.result = result
        super().__init__(
            f"process exited with code {result.returncode}: {result.command}"
        )


def _normalize_argv(argv: Sequence[CommandArgument]) -> tuple[str, ...]:
    if isinstance(argv, (str, bytes, os.PathLike)):
        raise TypeError("argv must be a sequence of arguments, not a shell command")

    normalized = tuple(os.fspath(argument) for argument in argv)
    if not normalized:
        raise ValueError("argv must contain at least one argument")

    for index, argument in enumerate(normalized):
        if not isinstance(argument, str):
            raise TypeError(f"argv[{index}] is not a string or path-like value")
        if not argument:
            raise ValueError(f"argv[{index}] must not be empty")
        if "\x00" in argument:
            raise ValueError(f"argv[{index}] contains a NUL byte")
    return normalized


def _normalize_cwd(cwd: str | os.PathLike[str] | None) -> Path:
    working_directory = Path.cwd() if cwd is None else Path(cwd)
    working_directory = working_directory.expanduser().resolve()
    if not working_directory.exists():
        raise ValueError(f"working directory does not exist: {working_directory}")
    if not working_directory.is_dir():
        raise ValueError(f"working directory is not a directory: {working_directory}")
    return working_directory


def _build_environment(
    overrides: Mapping[str, EnvironmentValue] | None,
) -> dict[str, str] | None:
    if overrides is None:
        return None

    environment = os.environ.copy()
    for key, value in overrides.items():
        if not isinstance(key, str) or not key or "=" in key or "\x00" in key:
            raise ValueError(f"invalid environment variable name: {key!r}")
        if value is None:
            environment.pop(key, None)
            continue
        if not isinstance(value, str):
            raise TypeError(f"environment value for {key!r} must be a string or None")
        if "\x00" in value:
            raise ValueError(f"environment value for {key!r} contains a NUL byte")
        environment[key] = value
    return environment


def _coerce_timeout_output(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def run_process(
    argv: Sequence[CommandArgument],
    *,
    cwd: str | os.PathLike[str] | None = None,
    environment: Mapping[str, EnvironmentValue] | None = None,
    input_text: str | None = None,
    timeout: float | None = None,
    check: bool = True,
) -> ProcessResult:
    """Execute one non-interactive process without a shell.

    ``environment`` is an overlay on the current process environment.  A
    mapping value of ``None`` removes that variable for the child process.
    Output is always captured as UTF-8 text with replacement for invalid byte
    sequences.  Callers must pass secrets through an approved injected
    environment or broker, never as command-line arguments.
    """

    normalized_argv = _normalize_argv(argv)
    working_directory = _normalize_cwd(cwd)
    child_environment = _build_environment(environment)

    if timeout is not None and timeout <= 0:
        raise ValueError("timeout must be greater than zero")
    if input_text is not None and not isinstance(input_text, str):
        raise TypeError("input_text must be a string or None")

    try:
        completed = subprocess.run(
            normalized_argv,
            cwd=working_directory,
            env=child_environment,
            input=input_text,
            stdin=subprocess.DEVNULL if input_text is None else None,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
            shell=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise ProcessTimeoutError(
            normalized_argv,
            working_directory,
            float(timeout),
            _coerce_timeout_output(exc.stdout),
            _coerce_timeout_output(exc.stderr),
        ) from exc
    except OSError as exc:
        raise ProcessStartError(normalized_argv, working_directory, exc) from exc

    result = ProcessResult(
        argv=normalized_argv,
        cwd=working_directory,
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )
    if check and not result.succeeded:
        raise ProcessExecutionError(result)
    return result
