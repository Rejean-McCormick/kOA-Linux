"""Thin storage adapter for verified read-only recovery sources."""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import subprocess
from typing import Callable, Iterable, Sequence


class StorageAdapterError(RuntimeError):
    """Raised when a constrained storage operation fails."""


Runner = Callable[[Sequence[str], int], subprocess.CompletedProcess[str]]


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
class MountState:
    source: str
    target: str
    filesystem_type: str | None
    options: tuple[str, ...]
    read_only: bool


class StorageAdapter:
    """Mounts only admitted sources onto admitted targets with fixed safe flags."""

    def __init__(
        self,
        allowed_sources: Iterable[str],
        allowed_targets: Iterable[str],
        *,
        runner: Runner = subprocess_runner,
        mount_binary: str = "/usr/bin/mount",
        umount_binary: str = "/usr/bin/umount",
        findmnt_binary: str = "/usr/bin/findmnt",
        timeout_seconds: int = 60,
    ) -> None:
        for binary in (mount_binary, umount_binary, findmnt_binary):
            if not Path(binary).is_absolute():
                raise ValueError("storage utility paths must be absolute")
        self._allowed_sources = frozenset(self._validate_absolute(value, must_exist=False) for value in allowed_sources)
        self._allowed_targets = frozenset(self._validate_absolute(value, must_exist=False) for value in allowed_targets)
        self._runner = runner
        self._mount_binary = mount_binary
        self._umount_binary = umount_binary
        self._findmnt_binary = findmnt_binary
        self._timeout_seconds = timeout_seconds

    @staticmethod
    def _validate_absolute(value: str, *, must_exist: bool) -> str:
        path = Path(value)
        if not path.is_absolute() or ".." in path.parts:
            raise ValueError(f"absolute normalized path required: {value!r}")
        if must_exist and not path.exists():
            raise FileNotFoundError(path)
        if path.exists() and path.is_symlink():
            raise StorageAdapterError(f"symbolic links are prohibited: {value}")
        return os.path.normpath(value)

    def _admit_source(self, source: str) -> str:
        normalized = self._validate_absolute(source, must_exist=False)
        if normalized not in self._allowed_sources:
            raise StorageAdapterError(f"storage source is not admitted by the active profile: {source}")
        return normalized

    def _admit_target(self, target: str) -> str:
        normalized = self._validate_absolute(target, must_exist=False)
        if normalized not in self._allowed_targets:
            raise StorageAdapterError(f"mount target is not admitted by the active profile: {target}")
        return normalized

    def _run(self, binary: str, arguments: Sequence[str]) -> subprocess.CompletedProcess[str]:
        result = self._runner((binary, *arguments), self._timeout_seconds)
        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip()[:500]
            raise StorageAdapterError(f"storage command failed with code {result.returncode}: {detail}")
        return result

    def inspect(self, target: str) -> MountState | None:
        admitted = self._admit_target(target)
        result = self._runner(
            (
                self._findmnt_binary,
                "--json",
                "--canonicalize",
                "--output",
                "SOURCE,TARGET,FSTYPE,OPTIONS",
                "--target",
                admitted,
            ),
            self._timeout_seconds,
        )
        if result.returncode == 1:
            return None
        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip()[:500]
            raise StorageAdapterError(f"findmnt failed with code {result.returncode}: {detail}")
        try:
            payload = json.loads(result.stdout)
            filesystems = payload.get("filesystems")
        except (json.JSONDecodeError, AttributeError) as exc:
            raise StorageAdapterError("findmnt returned invalid JSON") from exc
        if not isinstance(filesystems, list) or len(filesystems) != 1 or not isinstance(filesystems[0], dict):
            raise StorageAdapterError("findmnt returned an unexpected mount result")
        record = filesystems[0]
        options = tuple(sorted(part for part in str(record.get("options", "")).split(",") if part))
        return MountState(
            source=str(record.get("source", "")),
            target=str(record.get("target", admitted)),
            filesystem_type=str(record["fstype"]) if record.get("fstype") else None,
            options=options,
            read_only="ro" in options and "rw" not in options,
        )

    def mount_read_only(self, source: str, target: str) -> MountState:
        admitted_source = self._admit_source(source)
        admitted_target = self._admit_target(target)
        target_path = Path(admitted_target)
        if not target_path.exists() or not target_path.is_dir() or target_path.is_symlink():
            raise StorageAdapterError("mount target must be an existing non-symlink directory")
        self._run(
            self._mount_binary,
            ("--read-only", "--options", "nosuid,nodev,noexec", "--", admitted_source, admitted_target),
        )
        state = self.inspect(admitted_target)
        if state is None or not state.read_only:
            raise StorageAdapterError("recovery source did not mount read-only")
        return state

    def unmount(self, target: str) -> None:
        admitted = self._admit_target(target)
        self._run(self._umount_binary, ("--", admitted))
        if self.inspect(admitted) is not None:
            raise StorageAdapterError("mount remains active after unmount")
