"""Thin, allowlisted Podman adapter for recovery containment."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
import subprocess
from typing import Callable, Iterable, Sequence


class PodmanAdapterError(RuntimeError):
    """Raised when a fixed Podman operation fails."""


Runner = Callable[[Sequence[str], int], subprocess.CompletedProcess[str]]
_NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,127}$")


def subprocess_runner(argv: Sequence[str], timeout_seconds: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(argv),
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
        env={"PATH": "/usr/sbin:/usr/bin:/sbin:/bin", "LC_ALL": "C"},
    )


@dataclass(frozen=True, slots=True)
class ContainerState:
    name: str
    container_id: str
    status: str
    running: bool
    paused: bool
    exit_code: int | None
    image_digest: str | None


class PodmanAdapter:
    """Exposes only inspect/start/stop/pause/unpause for admitted containers."""

    def __init__(
        self,
        allowed_containers: Iterable[str],
        *,
        runner: Runner = subprocess_runner,
        binary: str = "/usr/bin/podman",
        timeout_seconds: int = 45,
    ) -> None:
        if not Path(binary).is_absolute():
            raise ValueError("podman path must be absolute")
        self._allowed = frozenset(self._validate_name(name) for name in allowed_containers)
        self._runner = runner
        self._binary = binary
        self._timeout_seconds = timeout_seconds

    @staticmethod
    def _validate_name(name: str) -> str:
        if not _NAME_PATTERN.fullmatch(name):
            raise ValueError(f"invalid container name: {name!r}")
        return name

    def _admit(self, name: str) -> str:
        admitted = self._validate_name(name)
        if admitted not in self._allowed:
            raise PodmanAdapterError(f"container is not admitted by the active profile: {name}")
        return admitted

    def _run(self, arguments: Sequence[str]) -> subprocess.CompletedProcess[str]:
        result = self._runner((self._binary, *arguments), self._timeout_seconds)
        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip()[:500]
            raise PodmanAdapterError(f"podman failed with code {result.returncode}: {detail}")
        return result

    def inspect(self, name: str) -> ContainerState:
        admitted = self._admit(name)
        result = self._run(("container", "inspect", "--format", "json", "--", admitted))
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise PodmanAdapterError("podman returned invalid JSON") from exc
        if not isinstance(payload, list) or len(payload) != 1 or not isinstance(payload[0], dict):
            raise PodmanAdapterError("podman returned an unexpected inspect result")
        record = payload[0]
        state = record.get("State") if isinstance(record.get("State"), dict) else {}
        image_digest = record.get("Digest") or record.get("ImageDigest")
        exit_raw = state.get("ExitCode")
        return ContainerState(
            name=admitted,
            container_id=str(record.get("Id", "")),
            status=str(state.get("Status", "unknown")),
            running=bool(state.get("Running", False)),
            paused=bool(state.get("Paused", False)),
            exit_code=int(exit_raw) if isinstance(exit_raw, int) else None,
            image_digest=str(image_digest) if image_digest else None,
        )

    def stop(self, name: str, *, timeout_seconds: int = 30) -> ContainerState:
        admitted = self._admit(name)
        if not 1 <= timeout_seconds <= 300:
            raise ValueError("stop timeout must be between 1 and 300 seconds")
        self._run(("container", "stop", "--time", str(timeout_seconds), "--", admitted))
        return self.inspect(admitted)

    def start(self, name: str) -> ContainerState:
        admitted = self._admit(name)
        self._run(("container", "start", "--", admitted))
        return self.inspect(admitted)

    def pause(self, name: str) -> ContainerState:
        admitted = self._admit(name)
        self._run(("container", "pause", "--", admitted))
        return self.inspect(admitted)

    def unpause(self, name: str) -> ContainerState:
        admitted = self._admit(name)
        self._run(("container", "unpause", "--", admitted))
        return self.inspect(admitted)
