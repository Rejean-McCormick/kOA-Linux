#!/usr/bin/env python3
"""Fail-closed launcher for profile-owned kOA graphical sessions.

The launcher validates root-owned policy files, consumes an optional one-shot
maintenance/recovery authority handoff from an already-open file descriptor,
starts one closed session entrypoint without a shell, supervises it within a
bounded policy, and removes only its own runtime tree on exit.

It never connects to the privileged broker, performs host mutation, mounts
media, or interprets presentation visibility as authorization.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import shutil
import signal
import stat
import subprocess
import sys
import time
import tomllib
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

SCHEMA_VERSION = "1.0.0"
PROFILE_OVERLAY = "appliance_shell"
ALLOWED_ENTRYPOINTS = {
    "interactive_user": Path("/usr/libexec/koa/koa-appliance-session"),
    "maintenance": Path("/usr/libexec/koa/koa-maintenance-session"),
    "recovery": Path("/usr/libexec/koa/koa-recovery-session"),
}
ALLOWED_INHERITED_ENV = {
    "LANG",
    "LC_ALL",
    "LC_CTYPE",
    "XDG_RUNTIME_DIR",
    "WAYLAND_DISPLAY",
}
FORBIDDEN_ENV = {
    "KOA_NODE_AGENT_SOCKET",
    "KOA_PRIVILEGED_BROKER_SOCKET",
    "KOA_BROKER_SOCKET",
}
GRAPHICAL_TOP_KEYS = {
    "schema_version",
    "policy_id",
    "config_kind",
    "profile_overlay",
    "display_protocol",
    "compositor",
    "application_surface",
    "input",
    "accessibility",
    "failure",
}
SESSION_TOP_KEYS = {
    "schema_version",
    "session_id",
    "config_kind",
    "profile_overlay",
    "session_mode",
    "display_protocol",
    "authority",
    "entrypoint",
    "runtime",
    "environment",
    "supervision",
    "cleanup",
    "presentation",
}
HANDOFF_KEYS = {
    "schema_version",
    "session_mode",
    "profile_overlay",
    "subject_id",
    "authority_context",
    "issued_at",
    "expires_at",
    "nonce",
    "decision_receipt_id",
    "execution_receipt_required",
    "allowed_entrypoint",
}
MAX_HANDOFF_BYTES = 16 * 1024


class LauncherError(RuntimeError):
    """A fail-closed configuration, authority, or runtime error."""


@dataclass(frozen=True)
class SessionPlan:
    session_id: str
    session_mode: str
    executable: Path
    arguments: tuple[str, ...]
    start_state: str
    runtime_name: str
    inherited_environment: tuple[str, ...]
    max_restarts: int
    restart_window_seconds: int
    termination_grace_seconds: int
    requires_handoff: bool
    authority_context: str
    max_handoff_ttl_seconds: int
    critical_transition_receipt_required: bool

    def as_dict(self) -> dict[str, Any]:
        return {
            "arguments": list(self.arguments),
            "authority_context": self.authority_context,
            "critical_transition_receipt_required": self.critical_transition_receipt_required,
            "executable": str(self.executable),
            "inherited_environment": list(self.inherited_environment),
            "max_handoff_ttl_seconds": self.max_handoff_ttl_seconds,
            "max_restarts": self.max_restarts,
            "requires_handoff": self.requires_handoff,
            "restart_window_seconds": self.restart_window_seconds,
            "runtime_name": self.runtime_name,
            "session_id": self.session_id,
            "session_mode": self.session_mode,
            "start_state": self.start_state,
            "termination_grace_seconds": self.termination_grace_seconds,
        }


def _read_toml(path: Path, *, require_protected: bool) -> dict[str, Any]:
    try:
        original = path.absolute()
        original_info = original.lstat()
        if stat.S_ISLNK(original_info.st_mode):
            raise LauncherError(f"configuration may not be a symlink: {path}")
        resolved = original.resolve(strict=True)
        if original != resolved:
            raise LauncherError(f"configuration path may not traverse a symlink: {path}")
    except LauncherError:
        raise
    except (FileNotFoundError, OSError) as exc:
        raise LauncherError(f"configuration not available: {path}") from exc
    if not resolved.is_file():
        raise LauncherError(f"configuration must be a regular file: {path}")
    if require_protected:
        info = resolved.stat()
        if info.st_uid != 0:
            raise LauncherError(f"installed configuration must be owned by uid 0: {path}")
        if info.st_mode & (stat.S_IWGRP | stat.S_IWOTH):
            raise LauncherError(f"installed configuration is group/world writable: {path}")
    try:
        with resolved.open("rb") as stream:
            value = tomllib.load(stream)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise LauncherError(f"invalid TOML configuration: {path}") from exc
    if not isinstance(value, dict):
        raise LauncherError(f"configuration root must be a table: {path}")
    return value


def _exact_keys(value: Mapping[str, Any], expected: set[str], label: str) -> None:
    actual = set(value)
    missing = sorted(expected - actual)
    unknown = sorted(actual - expected)
    if missing or unknown:
        raise LauncherError(f"{label} keys mismatch; missing={missing}, unknown={unknown}")


def _table(value: Mapping[str, Any], key: str, expected: set[str]) -> Mapping[str, Any]:
    item = value.get(key)
    if not isinstance(item, dict):
        raise LauncherError(f"{key} must be a TOML table")
    _exact_keys(item, expected, key)
    return item


def _bool(value: Any, label: str) -> bool:
    if type(value) is not bool:
        raise LauncherError(f"{label} must be boolean")
    return value


def _integer(value: Any, label: str, minimum: int = 0, maximum: int = 3600) -> int:
    if type(value) is not int or value < minimum or value > maximum:
        raise LauncherError(f"{label} must be an integer in [{minimum}, {maximum}]")
    return value


def _string(value: Any, label: str, *, nonempty: bool = True) -> str:
    if not isinstance(value, str) or (nonempty and not value):
        raise LauncherError(f"{label} must be a non-empty string")
    if "\x00" in value:
        raise LauncherError(f"{label} contains NUL")
    return value


def _string_list(value: Any, label: str, *, maximum: int = 32) -> tuple[str, ...]:
    if not isinstance(value, list) or len(value) > maximum:
        raise LauncherError(f"{label} must be a bounded string array")
    result = tuple(_string(item, f"{label}[]", nonempty=False) for item in value)
    if len(set(result)) != len(result):
        raise LauncherError(f"{label} contains duplicates")
    return result


def validate_graphical_policy(data: Mapping[str, Any]) -> None:
    _exact_keys(data, GRAPHICAL_TOP_KEYS, "graphical policy")
    if data["schema_version"] != SCHEMA_VERSION:
        raise LauncherError("unsupported graphical policy schema")
    if data["config_kind"] != "graphical_policy":
        raise LauncherError("graphical policy has wrong config_kind")
    if data["profile_overlay"] != PROFILE_OVERLAY or data["display_protocol"] != "wayland":
        raise LauncherError("graphical policy is not the appliance Wayland policy")

    compositor = _table(
        data,
        "compositor",
        {"class", "full_desktop_environment", "x11_fallback", "application_allowlist", "implementation_is_global_requirement"},
    )
    if compositor["class"] != "minimal_wayland_compositor":
        raise LauncherError("only the minimal Wayland compositor class is permitted")
    for key in ("full_desktop_environment", "x11_fallback", "implementation_is_global_requirement"):
        if _bool(compositor[key], f"compositor.{key}"):
            raise LauncherError(f"compositor.{key} must be false")
    if not _bool(compositor["application_allowlist"], "compositor.application_allowlist"):
        raise LauncherError("application allowlisting is required")

    surface = _table(
        data,
        "application_surface",
        {
            "arbitrary_application_launcher",
            "unrestricted_terminal",
            "package_manager_ui",
            "host_administration_ui",
            "development_tools",
            "unrestricted_file_browser",
            "unrestricted_external_navigation",
            "route_authority",
        },
    )
    for key in surface:
        if key == "route_authority":
            continue
        if _bool(surface[key], f"application_surface.{key}"):
            raise LauncherError(f"application_surface.{key} must be false")
    if surface["route_authority"] != "active_component_profile_policy_and_session_state":
        raise LauncherError("route authority must remain external to presentation")

    input_policy = _table(data, "input", {"methods", "raw_device_access", "seat_managed"})
    methods = _string_list(input_policy["methods"], "input.methods")
    required_methods = {"keyboard", "pointer", "touch", "accessibility_controls", "local_deterministic_commands"}
    if set(methods) != required_methods:
        raise LauncherError("input.methods does not match the appliance contract")
    if _bool(input_policy["raw_device_access"], "input.raw_device_access"):
        raise LauncherError("raw input device access is prohibited")
    if not _bool(input_policy["seat_managed"], "input.seat_managed"):
        raise LauncherError("input must be seat managed")

    accessibility = _table(
        data,
        "accessibility",
        {"keyboard_only_operation", "visible_focus", "scalable_text_and_controls", "non_color_only_status", "voice_is_required"},
    )
    for key in ("keyboard_only_operation", "visible_focus", "scalable_text_and_controls", "non_color_only_status"):
        if not _bool(accessibility[key], f"accessibility.{key}"):
            raise LauncherError(f"accessibility.{key} is required")
    if _bool(accessibility["voice_is_required"], "accessibility.voice_is_required"):
        raise LauncherError("voice cannot be required")

    failure = _table(
        data,
        "failure",
        {"fallback_to_unrestricted_desktop", "preserve_authoritative_application_state", "restart_bounded_shell_components", "recovery_after_repeated_or_integrity_failure"},
    )
    if _bool(failure["fallback_to_unrestricted_desktop"], "failure.fallback_to_unrestricted_desktop"):
        raise LauncherError("unrestricted desktop fallback is prohibited")
    for key in ("preserve_authoritative_application_state", "restart_bounded_shell_components", "recovery_after_repeated_or_integrity_failure"):
        if not _bool(failure[key], f"failure.{key}"):
            raise LauncherError(f"failure.{key} is required")


def build_session_plan(data: Mapping[str, Any]) -> SessionPlan:
    _exact_keys(data, SESSION_TOP_KEYS, "session configuration")
    if data["schema_version"] != SCHEMA_VERSION or data["config_kind"] != "session":
        raise LauncherError("unsupported session configuration")
    if data["profile_overlay"] != PROFILE_OVERLAY or data["display_protocol"] != "wayland":
        raise LauncherError("session is not scoped to the appliance Wayland overlay")

    mode = _string(data["session_mode"], "session_mode")
    if mode not in ALLOWED_ENTRYPOINTS:
        raise LauncherError(f"unsupported session_mode: {mode}")
    session_id = _string(data["session_id"], "session_id")

    authority = _table(
        data,
        "authority",
        {
            "requires_handoff",
            "required_context",
            "separate_authentication",
            "direct_privileged_broker_access",
            "privileged_effects",
            "critical_transition_receipt_required",
            "max_handoff_ttl_seconds",
        },
    )
    requires_handoff = _bool(authority["requires_handoff"], "authority.requires_handoff")
    separate_authentication = _bool(authority["separate_authentication"], "authority.separate_authentication")
    if _bool(authority["direct_privileged_broker_access"], "authority.direct_privileged_broker_access"):
        raise LauncherError("session may not access the privileged broker directly")
    required_context = _string(authority["required_context"], "authority.required_context")
    privileged_effects = _string(authority["privileged_effects"], "authority.privileged_effects")
    receipt_required = _bool(authority["critical_transition_receipt_required"], "authority.critical_transition_receipt_required")
    ttl = _integer(authority["max_handoff_ttl_seconds"], "authority.max_handoff_ttl_seconds", 0, 900)

    expected = {
        "interactive_user": (False, False, "ordinary", "none", False, 0),
        "maintenance": (True, True, "maintenance_authorized", "request_only", True, 300),
        "recovery": (True, True, "recovery_authorized", "request_only", True, 300),
    }[mode]
    if (requires_handoff, separate_authentication, required_context, privileged_effects, receipt_required, ttl) != expected:
        raise LauncherError(f"authority policy does not match session mode {mode}")

    entrypoint = _table(data, "entrypoint", {"executable", "arguments", "start_state"})
    executable = Path(_string(entrypoint["executable"], "entrypoint.executable"))
    if not executable.is_absolute() or executable != ALLOWED_ENTRYPOINTS[mode]:
        raise LauncherError(f"entrypoint is not the closed executable for {mode}")
    arguments = _string_list(entrypoint["arguments"], "entrypoint.arguments", maximum=16)
    start_state = _string(entrypoint["start_state"], "entrypoint.start_state")
    expected_state = {"interactive_user": "locked", "maintenance": "maintenance_locked", "recovery": "recovery_locked"}[mode]
    if start_state != expected_state:
        raise LauncherError(f"invalid start state for {mode}")

    runtime = _table(data, "runtime", {"directory_name", "mode", "clean_on_start", "clean_on_exit", "reject_symlinks"})
    runtime_name = _string(runtime["directory_name"], "runtime.directory_name")
    if "/" in runtime_name or runtime_name in {".", ".."}:
        raise LauncherError("runtime.directory_name must be one path segment")
    if runtime["mode"] != "0700":
        raise LauncherError("runtime mode must be 0700")
    for key in ("clean_on_start", "clean_on_exit", "reject_symlinks"):
        if not _bool(runtime[key], f"runtime.{key}"):
            raise LauncherError(f"runtime.{key} must be true")

    environment = _table(data, "environment", {"inherit", "clear_unlisted", "profile_overlay", "session_mode"})
    inherited = _string_list(environment["inherit"], "environment.inherit")
    if not set(inherited).issubset(ALLOWED_INHERITED_ENV):
        raise LauncherError("environment.inherit contains an unapproved variable")
    if not _bool(environment["clear_unlisted"], "environment.clear_unlisted"):
        raise LauncherError("unlisted environment variables must be cleared")
    if environment["profile_overlay"] != PROFILE_OVERLAY or environment["session_mode"] != mode:
        raise LauncherError("environment identity does not match the session")

    supervision = _table(
        data,
        "supervision",
        {"max_restarts", "restart_window_seconds", "termination_grace_seconds", "crash_return_state", "integrity_failure_action"},
    )
    max_restarts = _integer(supervision["max_restarts"], "supervision.max_restarts", 0, 3)
    restart_window = _integer(supervision["restart_window_seconds"], "supervision.restart_window_seconds", 0, 300)
    termination_grace = _integer(supervision["termination_grace_seconds"], "supervision.termination_grace_seconds", 1, 60)
    expected_supervision = {
        "interactive_user": (2, 30, "locked", "request_recovery"),
        "maintenance": (0, 0, "terminate", "request_recovery"),
        "recovery": (0, 0, "terminate", "remain_in_recovery"),
    }[mode]
    if (max_restarts, restart_window, supervision["crash_return_state"], supervision["integrity_failure_action"]) != expected_supervision:
        raise LauncherError(f"supervision policy does not match session mode {mode}")

    cleanup = _table(data, "cleanup", {"remove_runtime_tree", "preserve_authoritative_state", "release_devices", "unmount_media"})
    if not _bool(cleanup["remove_runtime_tree"], "cleanup.remove_runtime_tree"):
        raise LauncherError("runtime cleanup is required")
    if not _bool(cleanup["preserve_authoritative_state"], "cleanup.preserve_authoritative_state"):
        raise LauncherError("authoritative state must be preserved")
    if cleanup["release_devices"] != "external_owner" or cleanup["unmount_media"] != "external_owner":
        raise LauncherError("device and media lifecycle must remain outside the session launcher")

    presentation = _table(
        data,
        "presentation",
        {"visible_mode_indicator", "maintenance_controls_visible", "recovery_controls_visible", "status_and_exit_controls_required", "route_authority"},
    )
    expected_presentation = {
        "interactive_user": (False, False, False, "active_component_profile_policy_and_session_state"),
        "maintenance": (True, True, False, "registered_maintenance_interfaces_only"),
        "recovery": (True, False, True, "registered_recovery_interfaces_only"),
    }[mode]
    actual_presentation = (
        _bool(presentation["visible_mode_indicator"], "presentation.visible_mode_indicator"),
        _bool(presentation["maintenance_controls_visible"], "presentation.maintenance_controls_visible"),
        _bool(presentation["recovery_controls_visible"], "presentation.recovery_controls_visible"),
        presentation["route_authority"],
    )
    if actual_presentation != expected_presentation:
        raise LauncherError(f"presentation policy does not match session mode {mode}")
    if not _bool(presentation["status_and_exit_controls_required"], "presentation.status_and_exit_controls_required"):
        raise LauncherError("status and exit controls are required")

    return SessionPlan(
        session_id=session_id,
        session_mode=mode,
        executable=executable,
        arguments=arguments,
        start_state=start_state,
        runtime_name=runtime_name,
        inherited_environment=inherited,
        max_restarts=max_restarts,
        restart_window_seconds=restart_window,
        termination_grace_seconds=termination_grace,
        requires_handoff=requires_handoff,
        authority_context=required_context,
        max_handoff_ttl_seconds=ttl,
        critical_transition_receipt_required=receipt_required,
    )


def _parse_rfc3339(value: str, label: str) -> dt.datetime:
    text = _string(value, label)
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = dt.datetime.fromisoformat(text)
    except ValueError as exc:
        raise LauncherError(f"{label} must be RFC 3339") from exc
    if parsed.tzinfo is None:
        raise LauncherError(f"{label} must include a timezone")
    return parsed.astimezone(dt.timezone.utc)


def _validate_authority_fd(fd: int) -> None:
    if fd < 3:
        raise LauncherError("authority handoff must use a non-standard file descriptor")
    try:
        info = os.fstat(fd)
    except OSError as exc:
        raise LauncherError("authority handoff file descriptor is invalid") from exc
    if not stat.S_ISREG(info.st_mode):
        raise LauncherError("authority handoff must be an unlinked regular file")
    if info.st_uid != 0:
        raise LauncherError("authority handoff must be owned by uid 0")
    if info.st_nlink != 0:
        raise LauncherError("authority handoff must be unlinked before transfer")
    if info.st_mode & (stat.S_IWUSR | stat.S_IRWXG | stat.S_IRWXO):
        raise LauncherError("authority handoff must be owner-read-only")


def read_authority_handoff(fd: int, plan: SessionPlan, *, now: dt.datetime | None = None) -> dict[str, Any]:
    _validate_authority_fd(fd)
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = os.read(fd, min(4096, MAX_HANDOFF_BYTES + 1 - total))
        if not chunk:
            break
        chunks.append(chunk)
        total += len(chunk)
        if total > MAX_HANDOFF_BYTES:
            raise LauncherError("authority handoff exceeds the size limit")
    try:
        value = json.loads(b"".join(chunks))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise LauncherError("authority handoff is not valid JSON") from exc
    if not isinstance(value, dict):
        raise LauncherError("authority handoff must be an object")
    _exact_keys(value, HANDOFF_KEYS, "authority handoff")
    if value["schema_version"] != SCHEMA_VERSION:
        raise LauncherError("unsupported authority handoff schema")
    if value["session_mode"] != plan.session_mode or value["profile_overlay"] != PROFILE_OVERLAY:
        raise LauncherError("authority handoff scope mismatch")
    if value["authority_context"] != plan.authority_context:
        raise LauncherError("authority handoff context mismatch")
    if value["allowed_entrypoint"] != str(plan.executable):
        raise LauncherError("authority handoff entrypoint mismatch")
    if value["execution_receipt_required"] is not plan.critical_transition_receipt_required:
        raise LauncherError("authority handoff receipt requirement mismatch")
    for key in ("subject_id", "nonce", "decision_receipt_id"):
        _string(value[key], f"authority handoff {key}")
    issued = _parse_rfc3339(value["issued_at"], "authority handoff issued_at")
    expires = _parse_rfc3339(value["expires_at"], "authority handoff expires_at")
    current = (now or dt.datetime.now(dt.timezone.utc)).astimezone(dt.timezone.utc)
    if expires <= issued or current < issued or current >= expires:
        raise LauncherError("authority handoff is not currently valid")
    if (expires - issued).total_seconds() > plan.max_handoff_ttl_seconds:
        raise LauncherError("authority handoff exceeds the configured TTL")
    return value


def _runtime_base() -> Path:
    raw = os.environ.get("XDG_RUNTIME_DIR")
    if not raw:
        raise LauncherError("XDG_RUNTIME_DIR is required")
    base = Path(raw)
    if not base.is_absolute():
        raise LauncherError("XDG_RUNTIME_DIR must be absolute")
    try:
        info = base.lstat()
    except OSError as exc:
        raise LauncherError("XDG_RUNTIME_DIR is unavailable") from exc
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
        raise LauncherError("XDG_RUNTIME_DIR must be a real directory")
    if info.st_uid != os.getuid():
        raise LauncherError("XDG_RUNTIME_DIR owner mismatch")
    if info.st_mode & stat.S_IWOTH:
        raise LauncherError("XDG_RUNTIME_DIR must not be world writable")
    return base.resolve(strict=True)


def _safe_remove_tree(path: Path, base: Path) -> None:
    base_resolved = base.resolve(strict=True)
    try:
        relative = path.relative_to(base_resolved)
    except ValueError as exc:
        raise LauncherError("runtime path escapes its base") from exc
    if not relative.parts or relative.parts[0] != "koa" or len(relative.parts) < 3:
        raise LauncherError("runtime path is outside the dedicated kOA session tree")
    if not path.exists() and not path.is_symlink():
        return
    info = path.lstat()
    if stat.S_ISLNK(info.st_mode):
        raise LauncherError("runtime path may not be a symlink")
    if info.st_uid != os.getuid():
        raise LauncherError("runtime path owner mismatch")
    shutil.rmtree(path)


def prepare_runtime(plan: SessionPlan) -> Path:
    base = _runtime_base()
    root = base / "koa" / "sessions"
    if root.exists() or root.is_symlink():
        info = root.lstat()
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid():
            raise LauncherError("unsafe kOA session runtime root")
    else:
        root.mkdir(parents=True, mode=0o700)
    os.chmod(root, 0o700)
    runtime = root / plan.runtime_name
    _safe_remove_tree(runtime, base)
    runtime.mkdir(mode=0o700)
    return runtime


def cleanup_runtime(runtime: Path) -> None:
    base = _runtime_base()
    _safe_remove_tree(runtime, base)


def build_environment(plan: SessionPlan, runtime: Path, handoff: Mapping[str, Any] | None) -> dict[str, str]:
    environment: dict[str, str] = {}
    for key in plan.inherited_environment:
        value = os.environ.get(key)
        if value is not None:
            environment[key] = value
    for key in FORBIDDEN_ENV:
        environment.pop(key, None)
    environment.update(
        {
            "HOME": str(runtime),
            "KOA_PROFILE_OVERLAY": PROFILE_OVERLAY,
            "KOA_SESSION_MODE": plan.session_mode,
            "KOA_SESSION_RUNTIME_DIR": str(runtime),
            "KOA_SESSION_START_STATE": plan.start_state,
            "PATH": "/usr/bin:/bin",
        }
    )
    if handoff is not None:
        environment["KOA_SESSION_DECISION_RECEIPT_ID"] = str(handoff["decision_receipt_id"])
        environment["KOA_SESSION_AUTHORITY_CONTEXT"] = plan.authority_context
    return environment


def _emit(event: str, plan: SessionPlan, **fields: Any) -> None:
    payload = {"event": event, "session_id": plan.session_id, "session_mode": plan.session_mode, **fields}
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")), file=sys.stderr, flush=True)


def run_session(plan: SessionPlan, handoff: Mapping[str, Any] | None) -> int:
    if plan.requires_handoff and handoff is None:
        raise LauncherError("authorized session requires a validated authority handoff")
    if not plan.requires_handoff and handoff is not None:
        raise LauncherError("ordinary session does not accept authority handoff state")
    try:
        info = plan.executable.lstat()
    except OSError as exc:
        raise LauncherError(f"session entrypoint is not installed: {plan.executable}") from exc
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
        raise LauncherError("session entrypoint must be a regular non-symlink file")
    if info.st_uid != 0:
        raise LauncherError("session entrypoint must be owned by uid 0")
    if info.st_mode & (stat.S_IWGRP | stat.S_IWOTH):
        raise LauncherError("session entrypoint is group/world writable")
    if not os.access(plan.executable, os.X_OK):
        raise LauncherError("session entrypoint is not executable")
    runtime = prepare_runtime(plan)
    environment = build_environment(plan, runtime, handoff)
    command = [str(plan.executable), *plan.arguments]
    stop_requested = False
    child: subprocess.Popen[bytes] | None = None

    def request_stop(signum: int, _frame: object) -> None:
        nonlocal stop_requested
        stop_requested = True
        if child is not None and child.poll() is None:
            try:
                os.killpg(child.pid, signum)
            except ProcessLookupError:
                return

    previous = {sig: signal.getsignal(sig) for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)}
    for sig in previous:
        signal.signal(sig, request_stop)

    attempts: list[float] = []
    try:
        attempt = 0
        while True:
            attempt += 1
            _emit("session_starting", plan, attempt=attempt)
            child = subprocess.Popen(
                command,
                cwd=runtime,
                env=environment,
                close_fds=True,
                start_new_session=True,
            )
            return_code = child.wait()
            _emit("session_exited", plan, attempt=attempt, return_code=return_code)
            if return_code == 0 or stop_requested or plan.max_restarts == 0:
                return return_code
            now = time.monotonic()
            attempts = [stamp for stamp in attempts if now - stamp <= plan.restart_window_seconds]
            if len(attempts) >= plan.max_restarts:
                return return_code
            attempts.append(now)
            cleanup_runtime(runtime)
            runtime = prepare_runtime(plan)
            environment = build_environment(plan, runtime, handoff)
            environment["KOA_SESSION_START_STATE"] = "locked"
    finally:
        if child is not None and child.poll() is None:
            try:
                os.killpg(child.pid, signal.SIGTERM)
                child.wait(timeout=plan.termination_grace_seconds)
            except (ProcessLookupError, subprocess.TimeoutExpired):
                try:
                    os.killpg(child.pid, signal.SIGKILL)
                except ProcessLookupError:
                    _emit("session_process_already_exited", plan)
                child.wait()
        cleanup_runtime(runtime)
        for sig, handler in previous.items():
            signal.signal(sig, handler)
        _emit("session_runtime_cleaned", plan)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate or launch a restricted kOA appliance session.")
    parser.add_argument("action", choices=("validate", "plan", "run"))
    parser.add_argument("--graphical-policy", type=Path, required=True)
    parser.add_argument("--session", type=Path, required=True)
    parser.add_argument("--authority-fd", type=int)
    parser.add_argument(
        "--require-installed-policy-protection",
        action="store_true",
        help="require uid 0 ownership and no group/world write on configuration files",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        require_protected = args.require_installed_policy_protection or args.action == "run"
        graphical = _read_toml(args.graphical_policy, require_protected=require_protected)
        session = _read_toml(args.session, require_protected=require_protected)
        validate_graphical_policy(graphical)
        plan = build_session_plan(session)

        handoff: Mapping[str, Any] | None = None
        if plan.requires_handoff:
            if args.authority_fd is None:
                if args.action == "run":
                    raise LauncherError("an authority handoff file descriptor is required")
            else:
                handoff = read_authority_handoff(args.authority_fd, plan)
        elif args.authority_fd is not None:
            raise LauncherError("ordinary session does not accept an authority handoff")

        if args.action == "validate":
            print(json.dumps({"status": "valid", "session": plan.as_dict()}, sort_keys=True, indent=2))
            return 0
        if args.action == "plan":
            print(json.dumps(plan.as_dict(), sort_keys=True, indent=2))
            return 0
        return run_session(plan, handoff)
    except LauncherError as exc:
        print(json.dumps({"status": "blocked", "error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 78


if __name__ == "__main__":
    raise SystemExit(main())
