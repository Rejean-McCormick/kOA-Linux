"""Bounded QEMU harness for machine-observed kOA system validation.

The harness owns only validation infrastructure. Product profile, release,
networking, activation, and session policy remain external inputs and are never
rewritten by this module.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
import shutil
import socket
import subprocess
import tempfile
import time
import tomllib
from typing import Mapping, Pattern


class QemuHarnessError(RuntimeError):
    """Raised when a configured VM starts but cannot satisfy validation."""


class QemuBlockedError(QemuHarnessError):
    """Raised when declared external validation prerequisites are unavailable."""


def _exact_keys(value: Mapping[str, object], expected: set[str], label: str) -> None:
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise QemuHarnessError(f"{label} keys mismatch: missing={missing}, extra={extra}")


def _string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise QemuHarnessError(f"{label} must be a non-empty string")
    return value.strip()


def _positive_int(value: object, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise QemuHarnessError(f"{label} must be a positive integer")
    return value


def _string_list(value: object, label: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not value or not all(isinstance(item, str) and item for item in value):
        raise QemuHarnessError(f"{label} must be a non-empty string array")
    return tuple(value)


def _table(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, dict):
        raise QemuHarnessError(f"{label} must be a table")
    return value


def _bounded_tail(path: Path, limit: int) -> str:
    if not path.exists():
        return ""
    size = path.stat().st_size
    with path.open("rb") as stream:
        if size > limit:
            stream.seek(size - limit)
        data = stream.read(limit)
    return data.decode("utf-8", errors="replace")


def _resolve_file(override: str | None, candidates: tuple[str, ...], label: str) -> Path:
    values = (override,) if override else candidates
    for value in values:
        path = Path(value).expanduser()
        if path.is_file() and not path.is_symlink():
            return path.resolve()
    shown = override if override else ", ".join(candidates)
    raise QemuBlockedError(f"{label} is unavailable; checked: {shown}")


def _resolve_executable(binary: str) -> Path:
    candidate = Path(binary)
    if candidate.parent != Path("."):
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return candidate.resolve()
        raise QemuBlockedError(f"QEMU executable is unavailable: {binary}")
    resolved = shutil.which(binary)
    if not resolved:
        raise QemuBlockedError(f"QEMU executable is unavailable on PATH: {binary}")
    return Path(resolved).resolve()


@dataclass(frozen=True, slots=True)
class MachineConfig:
    binary: str
    machine: str
    accelerator: str
    cpu: str
    smp: int
    memory_mib: int
    video_device: str
    rng_device: str
    timeout_seconds: int
    shutdown_timeout_seconds: int
    max_serial_log_bytes: int
    max_qemu_log_bytes: int
    uefi_code_candidates: tuple[str, ...]
    uefi_vars_candidates: tuple[str, ...]
    network_default_enabled: bool
    network_model: str

    @classmethod
    def load(cls, path: Path) -> "MachineConfig":
        try:
            document = tomllib.loads(path.read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError) as exc:
            raise QemuHarnessError(f"invalid QEMU machine configuration: {exc}") from exc
        _exact_keys(
            document,
            {"format", "format_version", "status", "scope", "architecture", "qemu", "uefi", "network"},
            "machine configuration",
        )
        if document["format"] != "koa.qemu-validation-machine" or document["format_version"] != "1.0.0":
            raise QemuHarnessError("unsupported QEMU machine configuration format")
        if document["status"] != "active" or document["scope"] != "reference_validation_platform":
            raise QemuHarnessError("QEMU machine configuration must remain an active reference validation platform")
        if document["architecture"] != "x86_64":
            raise QemuHarnessError("reference QEMU machine architecture must be x86_64")

        qemu = _table(document["qemu"], "qemu")
        _exact_keys(
            qemu,
            {
                "binary", "machine", "accelerator", "cpu", "smp", "memory_mib", "video_device", "rng_device",
                "timeout_seconds", "shutdown_timeout_seconds", "max_serial_log_bytes", "max_qemu_log_bytes",
            },
            "qemu",
        )
        uefi = _table(document["uefi"], "uefi")
        _exact_keys(uefi, {"required", "code_candidates", "vars_candidates"}, "uefi")
        if uefi["required"] is not True:
            raise QemuHarnessError("UEFI is required by the reference validation platform")
        network = _table(document["network"], "network")
        _exact_keys(network, {"default_enabled", "model"}, "network")
        if not isinstance(network["default_enabled"], bool):
            raise QemuHarnessError("network.default_enabled must be boolean")

        return cls(
            binary=_string(qemu["binary"], "qemu.binary"),
            machine=_string(qemu["machine"], "qemu.machine"),
            accelerator=_string(qemu["accelerator"], "qemu.accelerator"),
            cpu=_string(qemu["cpu"], "qemu.cpu"),
            smp=_positive_int(qemu["smp"], "qemu.smp"),
            memory_mib=_positive_int(qemu["memory_mib"], "qemu.memory_mib"),
            video_device=_string(qemu["video_device"], "qemu.video_device"),
            rng_device=_string(qemu["rng_device"], "qemu.rng_device"),
            timeout_seconds=_positive_int(qemu["timeout_seconds"], "qemu.timeout_seconds"),
            shutdown_timeout_seconds=_positive_int(qemu["shutdown_timeout_seconds"], "qemu.shutdown_timeout_seconds"),
            max_serial_log_bytes=_positive_int(qemu["max_serial_log_bytes"], "qemu.max_serial_log_bytes"),
            max_qemu_log_bytes=_positive_int(qemu["max_qemu_log_bytes"], "qemu.max_qemu_log_bytes"),
            uefi_code_candidates=_string_list(uefi["code_candidates"], "uefi.code_candidates"),
            uefi_vars_candidates=_string_list(uefi["vars_candidates"], "uefi.vars_candidates"),
            network_default_enabled=network["default_enabled"],
            network_model=_string(network["model"], "network.model"),
        )

    def network_argv(self, enabled: bool) -> tuple[str, ...]:
        if enabled:
            return ("-nic", f"user,model={self.network_model}")
        return ("-nic", "none")


@dataclass(frozen=True, slots=True)
class QemuPrerequisites:
    executable: Path
    firmware_code: Path
    firmware_vars: Path
    image: Path


class QemuHarness:
    """Launch and observe one disposable QEMU reference VM."""

    def __init__(self, config: MachineConfig) -> None:
        self.config = config

    @classmethod
    def from_file(cls, path: Path) -> "QemuHarness":
        return cls(MachineConfig.load(path))

    def preflight(self, image: Path) -> QemuPrerequisites:
        if not image.is_file() or image.is_symlink():
            raise QemuBlockedError(f"QEMU system image is unavailable or not a regular file: {image}")
        binary = os.environ.get("KOA_QEMU_BINARY", self.config.binary)
        executable = _resolve_executable(binary)
        firmware_code = _resolve_file(
            os.environ.get("KOA_QEMU_UEFI_CODE"), self.config.uefi_code_candidates, "UEFI firmware code"
        )
        firmware_vars = _resolve_file(
            os.environ.get("KOA_QEMU_UEFI_VARS"), self.config.uefi_vars_candidates, "UEFI firmware variables template"
        )
        return QemuPrerequisites(executable, firmware_code, firmware_vars, image.resolve())

    def launch(
        self,
        image: Path,
        *,
        network_enabled: bool | None = None,
        image_format: str = "raw",
    ) -> "QemuSession":
        prerequisites = self.preflight(image)
        if image_format not in {"raw", "qcow2"}:
            raise QemuHarnessError("image_format must be raw or qcow2")
        enabled = self.config.network_default_enabled if network_enabled is None else network_enabled
        return QemuSession(self.config, prerequisites, enabled, image_format)


class QemuSession:
    """Lifecycle and bounded observation surface for one QEMU process."""

    def __init__(
        self,
        config: MachineConfig,
        prerequisites: QemuPrerequisites,
        network_enabled: bool,
        image_format: str,
    ) -> None:
        self.config = config
        self.prerequisites = prerequisites
        self.network_enabled = network_enabled
        self.image_format = image_format
        self._temporary: tempfile.TemporaryDirectory[str] | None = None
        self.workdir: Path | None = None
        self.serial_log: Path | None = None
        self.qemu_log: Path | None = None
        self.qmp_socket: Path | None = None
        self.process: subprocess.Popen[bytes] | None = None
        self.argv: tuple[str, ...] = ()
        self._qemu_stream = None

    def __enter__(self) -> "QemuSession":
        self.start()
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        self.stop()

    def _argv(self) -> list[str]:
        if self.workdir is None or self.serial_log is None or self.qmp_socket is None:
            raise QemuHarnessError("QEMU session workdir is not prepared")
        vars_copy = self.workdir / "OVMF_VARS.fd"
        return [
            str(self.prerequisites.executable),
            "-name", "koa-reference-validation",
            "-machine", f"{self.config.machine},accel={self.config.accelerator}",
            "-cpu", self.config.cpu,
            "-smp", str(self.config.smp),
            "-m", str(self.config.memory_mib),
            "-nodefaults",
            "-no-reboot",
            "-display", "none",
            "-monitor", "none",
            "-serial", f"file:{self.serial_log}",
            "-qmp", f"unix:{self.qmp_socket},server=on,wait=off",
            "-device", self.config.video_device,
            "-device", self.config.rng_device,
            "-drive", f"if=pflash,format=raw,unit=0,readonly=on,file={self.prerequisites.firmware_code}",
            "-drive", f"if=pflash,format=raw,unit=1,file={vars_copy}",
            "-drive", f"file={self.prerequisites.image},if=virtio,format={self.image_format}",
            "-snapshot",
            *self.config.network_argv(self.network_enabled),
        ]

    def start(self) -> None:
        if self.process is not None:
            raise QemuHarnessError("QEMU session already started")
        self._temporary = tempfile.TemporaryDirectory(prefix="koa-qemu-")
        self.workdir = Path(self._temporary.name).resolve()
        self.serial_log = self.workdir / "serial.log"
        self.qemu_log = self.workdir / "qemu.log"
        self.qmp_socket = self.workdir / "qmp.sock"
        shutil.copyfile(self.prerequisites.firmware_vars, self.workdir / "OVMF_VARS.fd")
        environment = {
            "HOME": str(self.workdir),
            "LANG": "C",
            "LC_ALL": "C",
            "PATH": "/usr/bin:/bin",
            "TMPDIR": str(self.workdir),
        }
        self._qemu_stream = self.qemu_log.open("wb")
        self.argv = tuple(self._argv())
        try:
            self.process = subprocess.Popen(
                list(self.argv),
                cwd=self.workdir,
                env=environment,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=self._qemu_stream,
                shell=False,
            )
        except OSError:
            self._qemu_stream.close()
            self._qemu_stream = None
            self._temporary.cleanup()
            self._temporary = None
            self.workdir = None
            self.serial_log = None
            self.qemu_log = None
            self.qmp_socket = None
            raise

    def _assert_bounded(self) -> None:
        if self.serial_log is None or self.qemu_log is None:
            raise QemuHarnessError("QEMU session logs are not prepared")
        limits = (
            (self.serial_log, self.config.max_serial_log_bytes, "serial"),
            (self.qemu_log, self.config.max_qemu_log_bytes, "QEMU"),
        )
        for path, limit, label in limits:
            if path.exists() and path.stat().st_size > limit:
                self.stop()
                raise QemuHarnessError(f"{label} log exceeded the bounded capture limit of {limit} bytes")

    def _diagnostic_tail(self) -> str:
        serial = _bounded_tail(self.serial_log, min(self.config.max_serial_log_bytes, 65536)) if self.serial_log else ""
        qemu = _bounded_tail(self.qemu_log, min(self.config.max_qemu_log_bytes, 32768)) if self.qemu_log else ""
        return f"serial_tail:\n{serial}\nqemu_tail:\n{qemu}".strip()

    def wait_for_patterns(
        self,
        patterns: Mapping[str, str | Pattern[str]],
        *,
        timeout_seconds: int | None = None,
    ) -> dict[str, str]:
        if not patterns:
            raise QemuHarnessError("at least one runtime observation pattern is required")
        if self.process is None or self.serial_log is None:
            raise QemuHarnessError("QEMU session is not running")
        timeout = timeout_seconds or self.config.timeout_seconds
        if timeout < 1 or timeout > self.config.timeout_seconds:
            raise QemuHarnessError("observation timeout exceeds the configured bound")
        compiled = {
            key: re.compile(value, re.MULTILINE) if isinstance(value, str) else value
            for key, value in patterns.items()
        }
        observed: dict[str, str] = {}
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            self._assert_bounded()
            code = self.process.poll()
            text = _bounded_tail(self.serial_log, self.config.max_serial_log_bytes)
            for key, pattern in compiled.items():
                if key in observed:
                    continue
                match = pattern.search(text)
                if match:
                    observed[key] = match.group(0)
            if len(observed) == len(compiled):
                return observed
            if code is not None:
                missing = sorted(set(compiled) - set(observed))
                raise QemuHarnessError(
                    f"QEMU exited with code {code} before observations {missing}; {self._diagnostic_tail()}"
                )
            time.sleep(0.1)
        missing = sorted(set(compiled) - set(observed))
        raise QemuHarnessError(f"timed out waiting for runtime observations {missing}; {self._diagnostic_tail()}")

    def _qmp_execute(self, command: str, arguments: Mapping[str, object] | None = None) -> object:
        if self.qmp_socket is None:
            raise QemuHarnessError("QMP socket is not prepared")
        deadline = time.monotonic() + min(10, self.config.timeout_seconds)
        while not self.qmp_socket.exists():
            if self.process is not None and self.process.poll() is not None:
                raise QemuHarnessError(f"QEMU exited before QMP became available; {self._diagnostic_tail()}")
            if time.monotonic() >= deadline:
                raise QemuHarnessError("timed out waiting for QMP socket")
            time.sleep(0.05)
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            remaining = max(0.1, deadline - time.monotonic())
            client.settimeout(remaining)
            client.connect(str(self.qmp_socket))
            stream = client.makefile("rwb", buffering=0)
            greeting = self._qmp_response(stream)
            if not isinstance(greeting, dict) or "QMP" not in greeting:
                raise QemuHarnessError("invalid QMP greeting")
            self._qmp_send(stream, {"execute": "qmp_capabilities"})
            self._qmp_result(stream)
            request: dict[str, object] = {"execute": command}
            if arguments:
                request["arguments"] = dict(arguments)
            self._qmp_send(stream, request)
            return self._qmp_result(stream)

    @staticmethod
    def _qmp_send(stream, document: Mapping[str, object]) -> None:
        payload = json.dumps(document, separators=(",", ":")).encode("utf-8") + b"\r\n"
        stream.write(payload)

    @staticmethod
    def _qmp_response(stream) -> object:
        line = stream.readline(1024 * 1024)
        if not line:
            raise QemuHarnessError("QMP connection closed unexpectedly")
        try:
            return json.loads(line.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise QemuHarnessError("invalid JSON received from QMP") from exc

    @classmethod
    def _qmp_result(cls, stream) -> object:
        for _ in range(128):
            response = cls._qmp_response(stream)
            if isinstance(response, dict) and "error" in response:
                raise QemuHarnessError(f"QMP command failed: {response['error']}")
            if isinstance(response, dict) and "return" in response:
                return response["return"]
        raise QemuHarnessError("QMP response limit exceeded")

    def capture_framebuffer(self, filename: str = "frame.ppm") -> Path:
        if self.workdir is None:
            raise QemuHarnessError("QEMU session workdir is not prepared")
        if not re.fullmatch(r"[A-Za-z0-9_.-]+\.ppm", filename):
            raise QemuHarnessError("framebuffer filename must be a simple .ppm filename")
        output = self.workdir / filename
        self._qmp_execute("screendump", {"filename": str(output)})
        if not output.is_file() or output.stat().st_size < 16:
            raise QemuHarnessError("QEMU did not produce a usable framebuffer capture")
        return output

    def stop(self) -> None:
        process = self.process
        if process is not None and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=self.config.shutdown_timeout_seconds)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=self.config.shutdown_timeout_seconds)
        if self._qemu_stream is not None:
            self._qemu_stream.close()
            self._qemu_stream = None
        self.process = None
        if self._temporary is not None:
            self._temporary.cleanup()
            self._temporary = None


def framebuffer_has_content(path: Path, *, minimum_distinct_colors: int = 8) -> bool:
    """Return whether a binary PPM contains varied pixels rather than a blank surface."""

    if minimum_distinct_colors < 2:
        raise ValueError("minimum_distinct_colors must be at least two")
    data = path.read_bytes()
    if not data.startswith(b"P6"):
        raise QemuHarnessError("framebuffer capture is not binary PPM")
    position = 2
    tokens: list[bytes] = []
    while len(tokens) < 3:
        while position < len(data) and data[position:position + 1].isspace():
            position += 1
        if position >= len(data):
            raise QemuHarnessError("truncated PPM header")
        if data[position:position + 1] == b"#":
            newline = data.find(b"\n", position)
            if newline < 0:
                raise QemuHarnessError("truncated PPM comment")
            position = newline + 1
            continue
        end = position
        while end < len(data) and not data[end:end + 1].isspace():
            end += 1
        tokens.append(data[position:end])
        position = end
    try:
        width, height, maximum = (int(token) for token in tokens)
    except ValueError as exc:
        raise QemuHarnessError("invalid PPM dimensions") from exc
    if width < 1 or height < 1 or maximum != 255:
        raise QemuHarnessError("unsupported PPM framebuffer dimensions or color depth")
    if position >= len(data) or not data[position:position + 1].isspace():
        raise QemuHarnessError("PPM header is missing the pixel-data separator")
    if data[position:position + 2] == b"\r\n":
        position += 2
    else:
        position += 1
    pixels = data[position:]
    expected = width * height * 3
    if len(pixels) < expected:
        raise QemuHarnessError("truncated PPM pixel data")
    colors: set[bytes] = set()
    step = max(3, (expected // 4096 // 3) * 3)
    for offset in range(0, expected - 2, step):
        colors.add(pixels[offset:offset + 3])
        if len(colors) >= minimum_distinct_colors:
            return True
    return False


__all__ = [
    "MachineConfig",
    "QemuBlockedError",
    "QemuHarness",
    "QemuHarnessError",
    "QemuPrerequisites",
    "QemuSession",
    "framebuffer_has_content",
]
