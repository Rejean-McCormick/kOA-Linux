"""Read-only Linux procfs resource-usage probe."""

from __future__ import annotations

import os
import uuid
from collections.abc import Mapping
from pathlib import Path
from typing import Protocol


class UsageObservationError(RuntimeError):
    """Base error for resource observation failures."""


class ProcessObservationUnavailable(UsageObservationError):
    """Raised when a process cannot be observed safely and completely enough."""


class Clock(Protocol):
    """Clock behavior consumed by usage probes."""

    def now_iso(self) -> str: ...


class ProcUsageProbe:
    """Observe resource metadata for one Linux process without reading payloads.

    The probe reads only ``stat``, ``status``, ``io``, and descriptor counts. It
    never reads ``cmdline``, ``environ``, process memory, or opened file content.
    Missing optional metrics are omitted rather than reported as zero.
    """

    def __init__(
        self,
        clock: Clock,
        *,
        proc_root: str | os.PathLike[str] = "/proc",
        clock_ticks_per_second: int | None = None,
        page_size: int | None = None,
    ) -> None:
        self._clock = clock
        self._proc_root = Path(proc_root)
        self._clock_ticks = clock_ticks_per_second or int(os.sysconf("SC_CLK_TCK"))
        self._page_size = page_size or int(os.sysconf("SC_PAGE_SIZE"))
        if self._clock_ticks <= 0 or self._page_size <= 0:
            raise ValueError("procfs conversion constants must be positive")

    def observe(
        self,
        target_execution_ref: str,
        *,
        pid: int,
        observation_id: str | None = None,
    ) -> Mapping[str, object]:
        """Return one RG-IF-005 resource-usage observation."""

        if not target_execution_ref.strip():
            raise ValueError("target_execution_ref is required")
        if isinstance(pid, bool) or not isinstance(pid, int) or pid <= 0:
            raise ValueError("pid must be a positive integer")

        process_dir = self._confined_process_dir(pid)
        stat = _parse_proc_stat(_read_text(process_dir / "stat", required=True))
        status = _parse_key_value_file(_read_text(process_dir / "status", required=True))
        observed_at = self._clock.now_iso()

        measurements: dict[str, object] = {
            "cpu": {
                "user_seconds": stat["utime_ticks"] / self._clock_ticks,
                "system_seconds": stat["stime_ticks"] / self._clock_ticks,
                "total_seconds": (stat["utime_ticks"] + stat["stime_ticks"]) / self._clock_ticks,
            },
            "memory": {
                "virtual_bytes": stat["virtual_bytes"],
                "resident_bytes": stat["resident_pages"] * self._page_size,
            },
            "processes": {
                "processes": 1,
                "threads": stat["threads"],
            },
        }

        vm_rss = _parse_kib(status.get("VmRSS"))
        vm_size = _parse_kib(status.get("VmSize"))
        if vm_rss is not None:
            measurements["memory"]["resident_bytes"] = vm_rss  # type: ignore[index]
        if vm_size is not None:
            measurements["memory"]["virtual_bytes"] = vm_size  # type: ignore[index]

        descriptor_count = _count_directory_entries(process_dir / "fd")
        if descriptor_count is not None:
            measurements["processes"]["file_descriptors"] = descriptor_count  # type: ignore[index]

        io_text = _read_text(process_dir / "io", required=False)
        if io_text is not None:
            io_values = _parse_key_value_file(io_text, separator=":")
            io_measurements: dict[str, int] = {}
            for source_name, output_name in (("read_bytes", "read_bytes"), ("write_bytes", "write_bytes")):
                parsed = _parse_nonnegative_int(io_values.get(source_name))
                if parsed is not None:
                    io_measurements[output_name] = parsed
            if io_measurements:
                measurements["io"] = io_measurements

        identifier = observation_id or _observation_id(
            "procfs", target_execution_ref, str(pid), observed_at, str(stat["start_ticks"])
        )
        return {
            "interface_id": "RG-IF-005",
            "observation_id": identifier,
            "target_execution_ref": target_execution_ref,
            "resource_measurements": measurements,
            "observed_at": observed_at,
            "measurement_source": "procfs",
            "source_metadata": {
                "pid": pid,
                "process_start_ticks": stat["start_ticks"],
            },
        }

    def observe_usage(self, target_execution_ref: str, *, pid: int) -> Mapping[str, object]:
        """Port-friendly name for one usage observation."""

        return self.observe(target_execution_ref, pid=pid)

    def sample(self, target_execution_ref: str, *, pid: int) -> Mapping[str, object]:
        """Alias matching a typical usage-probe port."""

        return self.observe(target_execution_ref, pid=pid)

    def _confined_process_dir(self, pid: int) -> Path:
        try:
            root = self._proc_root.resolve(strict=True)
            candidate = root.joinpath(str(pid))
            if candidate.is_symlink():
                raise ProcessObservationUnavailable("refusing symlinked process directory")
            process_dir = candidate.resolve(strict=True)
        except FileNotFoundError as exc:
            raise ProcessObservationUnavailable(f"process not found: {pid}") from exc
        if not process_dir.is_relative_to(root) or not process_dir.is_dir():
            raise ProcessObservationUnavailable("process path escapes procfs root")
        return process_dir


def _read_text(path: Path, *, required: bool, max_bytes: int = 256 * 1024) -> str | None:
    try:
        if path.is_symlink():
            raise ProcessObservationUnavailable(f"refusing symlinked procfs metric: {path.name}")
        with path.open("r", encoding="utf-8", errors="strict") as stream:
            value = stream.read(max_bytes + 1)
    except FileNotFoundError as exc:
        if required:
            raise ProcessObservationUnavailable(f"required procfs metric is missing: {path.name}") from exc
        return None
    except (OSError, UnicodeError) as exc:
        if required:
            raise ProcessObservationUnavailable(f"cannot read required procfs metric: {path.name}") from exc
        return None
    if len(value.encode("utf-8")) > max_bytes:
        raise ProcessObservationUnavailable(f"procfs metric exceeds size limit: {path.name}")
    return value


def _parse_proc_stat(raw: str) -> dict[str, int]:
    closing = raw.rfind(")")
    if closing <= 0:
        raise ProcessObservationUnavailable("invalid procfs stat record")
    fields = raw[closing + 1 :].split()
    if len(fields) <= 21:
        raise ProcessObservationUnavailable("incomplete procfs stat record")
    try:
        values = {
            "utime_ticks": int(fields[11]),
            "stime_ticks": int(fields[12]),
            "threads": int(fields[17]),
            "start_ticks": int(fields[19]),
            "virtual_bytes": int(fields[20]),
            "resident_pages": int(fields[21]),
        }
    except ValueError as exc:
        raise ProcessObservationUnavailable("non-integer procfs stat metric") from exc
    if any(value < 0 for value in values.values()):
        raise ProcessObservationUnavailable("negative procfs stat metric")
    return values


def _parse_key_value_file(raw: str, *, separator: str = ":") -> dict[str, str]:
    values: dict[str, str] = {}
    for line in raw.splitlines():
        if separator not in line:
            continue
        key, value = line.split(separator, 1)
        key = key.strip()
        if key and key not in values:
            values[key] = value.strip()
    return values


def _parse_kib(value: str | None) -> int | None:
    if value is None:
        return None
    parts = value.split()
    if len(parts) != 2 or parts[1] != "kB":
        return None
    parsed = _parse_nonnegative_int(parts[0])
    return None if parsed is None else parsed * 1024


def _parse_nonnegative_int(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        parsed = int(value)
    except ValueError:
        return None
    return parsed if parsed >= 0 else None


def _count_directory_entries(path: Path) -> int | None:
    try:
        return sum(1 for _ in path.iterdir())
    except OSError:
        return None


def _observation_id(*parts: str) -> str:
    return f"usage-{uuid.uuid5(uuid.NAMESPACE_URL, '|'.join(parts))}"
