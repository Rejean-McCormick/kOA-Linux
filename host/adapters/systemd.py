"""Thin, allowlisted systemd adapter for recovery procedures."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
import subprocess
from typing import Callable, Iterable, Sequence


class SystemdAdapterError(RuntimeError):
    """Raised when a fixed systemd operation fails."""


Runner = Callable[[Sequence[str], int], subprocess.CompletedProcess[str]]
_UNIT_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.@:-]{0,254}$")
_ALLOWED_PROPERTIES = (
    "Id",
    "LoadState",
    "ActiveState",
    "SubState",
    "Result",
    "ExecMainStatus",
    "StateChangeTimestampMonotonic",
)


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
class UnitState:
    unit: str
    load_state: str
    active_state: str
    sub_state: str
    result: str | None
    exec_main_status: int | None


class SystemdAdapter:
    """Executes only fixed actions for units admitted by the active profile."""

    def __init__(
        self,
        allowed_units: Iterable[str],
        *,
        runner: Runner = subprocess_runner,
        binary: str = "/usr/bin/systemctl",
        timeout_seconds: int = 30,
    ) -> None:
        binary_path = Path(binary)
        if not binary_path.is_absolute():
            raise ValueError("systemctl path must be absolute")
        units = frozenset(self._validate_unit(unit) for unit in allowed_units)
        self._allowed_units = units
        self._runner = runner
        self._binary = str(binary_path)
        self._timeout_seconds = timeout_seconds

    @staticmethod
    def _validate_unit(unit: str) -> str:
        if not _UNIT_PATTERN.fullmatch(unit):
            raise ValueError(f"invalid systemd unit: {unit!r}")
        return unit

    def _admit(self, unit: str) -> str:
        validated = self._validate_unit(unit)
        if validated not in self._allowed_units:
            raise SystemdAdapterError(f"systemd unit is not admitted by the active profile: {unit}")
        return validated

    def _run(self, arguments: Sequence[str]) -> subprocess.CompletedProcess[str]:
        result = self._runner((self._binary, "--no-pager", "--no-ask-password", *arguments), self._timeout_seconds)
        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip()[:500]
            raise SystemdAdapterError(f"systemctl failed with code {result.returncode}: {detail}")
        return result

    def inspect(self, unit: str) -> UnitState:
        admitted = self._admit(unit)
        properties = ",".join(_ALLOWED_PROPERTIES)
        result = self._run(("show", admitted, f"--property={properties}", "--output=json"))
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise SystemdAdapterError("systemctl returned invalid JSON") from exc
        if not isinstance(payload, dict):
            raise SystemdAdapterError("systemctl returned an invalid unit state")
        status_raw = payload.get("ExecMainStatus")
        status = int(status_raw) if isinstance(status_raw, (int, str)) and str(status_raw).isdigit() else None
        return UnitState(
            unit=admitted,
            load_state=str(payload.get("LoadState", "unknown")),
            active_state=str(payload.get("ActiveState", "unknown")),
            sub_state=str(payload.get("SubState", "unknown")),
            result=str(payload["Result"]) if payload.get("Result") else None,
            exec_main_status=status,
        )

    def stop(self, unit: str) -> UnitState:
        admitted = self._admit(unit)
        self._run(("stop", admitted))
        return self.inspect(admitted)

    def start(self, unit: str) -> UnitState:
        admitted = self._admit(unit)
        self._run(("start", admitted))
        return self.inspect(admitted)

    def restart(self, unit: str) -> UnitState:
        admitted = self._admit(unit)
        self._run(("restart", admitted))
        return self.inspect(admitted)
