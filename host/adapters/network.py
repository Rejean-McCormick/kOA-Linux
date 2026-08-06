"""Thin, allowlisted network adapter for recovery isolation."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
import subprocess
from typing import Callable, Iterable, Sequence


class NetworkAdapterError(RuntimeError):
    """Raised when a fixed network operation fails."""


Runner = Callable[[Sequence[str], int], subprocess.CompletedProcess[str]]
_INTERFACE_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:@-]{0,31}$")


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
class LinkState:
    interface: str
    index: int
    operational_state: str
    flags: tuple[str, ...]
    mtu: int


class NetworkAdapter:
    """Reads or changes link state only for interfaces admitted by a profile."""

    def __init__(
        self,
        allowed_interfaces: Iterable[str],
        *,
        runner: Runner = subprocess_runner,
        binary: str = "/usr/sbin/ip",
        timeout_seconds: int = 20,
    ) -> None:
        if not Path(binary).is_absolute():
            raise ValueError("ip path must be absolute")
        self._allowed = frozenset(self._validate_interface(name) for name in allowed_interfaces)
        self._runner = runner
        self._binary = binary
        self._timeout_seconds = timeout_seconds

    @staticmethod
    def _validate_interface(interface: str) -> str:
        if not _INTERFACE_PATTERN.fullmatch(interface):
            raise ValueError(f"invalid interface name: {interface!r}")
        return interface

    def _admit(self, interface: str) -> str:
        admitted = self._validate_interface(interface)
        if admitted not in self._allowed:
            raise NetworkAdapterError(f"interface is not admitted by the active profile: {interface}")
        return admitted

    def _run(self, arguments: Sequence[str]) -> subprocess.CompletedProcess[str]:
        result = self._runner((self._binary, *arguments), self._timeout_seconds)
        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip()[:500]
            raise NetworkAdapterError(f"ip failed with code {result.returncode}: {detail}")
        return result

    def inspect(self, interface: str) -> LinkState:
        admitted = self._admit(interface)
        result = self._run(("-json", "link", "show", "dev", admitted))
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise NetworkAdapterError("ip returned invalid JSON") from exc
        if not isinstance(payload, list) or len(payload) != 1 or not isinstance(payload[0], dict):
            raise NetworkAdapterError("ip returned an unexpected link result")
        record = payload[0]
        flags = record.get("flags") if isinstance(record.get("flags"), list) else []
        return LinkState(
            interface=admitted,
            index=int(record.get("ifindex", 0)),
            operational_state=str(record.get("operstate", "UNKNOWN")).lower(),
            flags=tuple(sorted(str(flag) for flag in flags)),
            mtu=int(record.get("mtu", 0)),
        )

    def isolate(self, interface: str) -> LinkState:
        admitted = self._admit(interface)
        self._run(("link", "set", "dev", admitted, "down"))
        return self.inspect(admitted)

    def restore(self, interface: str) -> LinkState:
        admitted = self._admit(interface)
        self._run(("link", "set", "dev", admitted, "up"))
        return self.inspect(admitted)
