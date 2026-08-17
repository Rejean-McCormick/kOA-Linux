"""Read-only systemd unit resource-usage probe."""

from __future__ import annotations

import os
import re
import subprocess
import uuid
from collections.abc import Mapping, Sequence
from typing import Protocol, runtime_checkable

_UNIT_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.@:\\-]{0,254}\.(?:service|scope|slice)$")
_PROPERTIES = (
    "ActiveState",
    "SubState",
    "Result",
    "MainPID",
    "ControlGroup",
    "CPUUsageNSec",
    "MemoryCurrent",
    "MemoryPeak",
    "TasksCurrent",
    "IOReadBytes",
    "IOWriteBytes",
)
_UNSET_UNSIGNED = {"", "[not set]", "infinity", "18446744073709551615"}


class SystemdObservationError(RuntimeError):
    """Base error for systemd observation failures."""


class SystemdObservationUnavailable(SystemdObservationError):
    """Raised when a declared unit cannot be observed through systemd."""


class Clock(Protocol):
    def now_iso(self) -> str: ...


@runtime_checkable
class SystemdPropertyReader(Protocol):
    """Read-only public systemd-property boundary."""

    source_name: str

    def read_properties(self, unit: str, properties: Sequence[str]) -> Mapping[str, str]: ...


class SystemctlPropertyReader:
    """Read unit properties with ``systemctl show`` and no shell execution."""

    source_name = "systemctl_show"

    def __init__(self, *, executable: str | os.PathLike[str] = "systemctl", timeout_seconds: float = 5.0) -> None:
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        self._executable = str(executable)
        self._timeout_seconds = timeout_seconds

    def read_properties(self, unit: str, properties: Sequence[str]) -> Mapping[str, str]:
        _validate_unit(unit)
        if not properties:
            raise ValueError("at least one systemd property is required")
        command = [
            self._executable,
            "--no-pager",
            "--plain",
            "show",
            unit,
            *[f"--property={name}" for name in properties],
        ]
        environment = {
            "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
            "LANG": "C",
            "LC_ALL": "C",
            "SYSTEMD_PAGER": "cat",
            "SYSTEMD_COLORS": "0",
        }
        try:
            completed = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                timeout=self._timeout_seconds,
                env=environment,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise SystemdObservationUnavailable("systemd_property_transport_unavailable") from exc
        if completed.returncode != 0:
            diagnostic = completed.stderr.strip().replace("\n", " ")[:256]
            raise SystemdObservationUnavailable(
                f"systemctl show failed with code {completed.returncode}: {diagnostic}"
            )
        return _parse_systemctl_output(completed.stdout)


class SystemdUsageProbe:
    """Observe bounded unit metrics without mutating systemd state."""

    def __init__(self, clock: Clock, reader: SystemdPropertyReader | None = None) -> None:
        self._clock = clock
        self._reader = reader or SystemctlPropertyReader()

    def observe(
        self,
        target_execution_ref: str,
        *,
        unit: str,
        observation_id: str | None = None,
    ) -> Mapping[str, object]:
        """Return one RG-IF-005 observation for a service, scope, or slice."""

        if not target_execution_ref.strip():
            raise ValueError("target_execution_ref is required")
        _validate_unit(unit)
        properties = self._reader.read_properties(unit, _PROPERTIES)
        observed_at = self._clock.now_iso()

        measurements: dict[str, object] = {}
        cpu_ns = _parse_unsigned(properties.get("CPUUsageNSec"))
        if cpu_ns is not None:
            measurements["cpu"] = {"total_seconds": cpu_ns / 1_000_000_000}

        memory: dict[str, int] = {}
        for source_name, output_name in (("MemoryCurrent", "current_bytes"), ("MemoryPeak", "peak_bytes")):
            parsed = _parse_unsigned(properties.get(source_name))
            if parsed is not None:
                memory[output_name] = parsed
        if memory:
            measurements["memory"] = memory

        tasks = _parse_unsigned(properties.get("TasksCurrent"))
        if tasks is not None:
            measurements["processes"] = {"tasks": tasks}

        io: dict[str, int] = {}
        for source_name, output_name in (("IOReadBytes", "read_bytes"), ("IOWriteBytes", "write_bytes")):
            parsed = _parse_unsigned(properties.get(source_name))
            if parsed is not None:
                io[output_name] = parsed
        if io:
            measurements["io"] = io

        if not measurements:
            raise SystemdObservationUnavailable("systemd returned no resource measurements")

        identifier = observation_id or _observation_id(
            self._reader.source_name, target_execution_ref, unit, observed_at
        )
        execution_state = {
            key: value
            for key, value in {
                "active_state": properties.get("ActiveState"),
                "sub_state": properties.get("SubState"),
                "result": properties.get("Result"),
                "main_pid": _parse_unsigned(properties.get("MainPID")),
                "control_group": properties.get("ControlGroup"),
            }.items()
            if value not in (None, "", "[not set]")
        }
        return {
            "interface_id": "RG-IF-005",
            "observation_id": identifier,
            "target_execution_ref": target_execution_ref,
            "resource_measurements": measurements,
            "observed_at": observed_at,
            "measurement_source": self._reader.source_name,
            "source_metadata": {
                "unit": unit,
                "execution_state": execution_state,
            },
        }

    def observe_usage(self, target_execution_ref: str, *, unit: str) -> Mapping[str, object]:
        """Port-friendly name for one usage observation."""

        return self.observe(target_execution_ref, unit=unit)

    def sample(self, target_execution_ref: str, *, unit: str) -> Mapping[str, object]:
        """Alias matching a typical usage-probe port."""

        return self.observe(target_execution_ref, unit=unit)


def _validate_unit(unit: str) -> None:
    if not isinstance(unit, str) or not _UNIT_PATTERN.fullmatch(unit):
        raise ValueError("unit must be a valid .service, .scope, or .slice name")


def _parse_systemctl_output(raw: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in raw.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key and key not in values:
            values[key] = value
    return values


def _parse_unsigned(value: str | None) -> int | None:
    if value is None or value in _UNSET_UNSIGNED:
        return None
    try:
        parsed = int(value)
    except ValueError:
        return None
    return parsed if parsed >= 0 else None


def _observation_id(*parts: str) -> str:
    return f"usage-{uuid.uuid5(uuid.NAMESPACE_URL, '|'.join(parts))}"
