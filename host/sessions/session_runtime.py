#!/usr/bin/env python3
"""Bounded process supervisor for resolved kOA appliance-session surfaces.

This module is intentionally not a profile resolver or policy engine. It consumes
one already-resolved ``session_runtime`` projection from the active effective
profile, applies the closed session envelope validated by ``koa-session-launcher``,
and supervises only the admitted process roles.

It never connects to the privileged broker, interprets recipes, launches a shell,
or substitutes a general browser or desktop when a surface fails.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import signal
import stat
import subprocess
import sys
import time
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

PROFILE_OVERLAY = "appliance_shell"
RUNTIME_PLAN_SCHEMA_VERSION = "1.0.0"
MAX_ACTIVE_PROFILE_BYTES = 512 * 1024
ALLOWED_SESSION_MODES = frozenset({"interactive_user", "maintenance", "recovery"})
ALLOWED_SURFACE_ROLES = frozenset({"compositor", "native_shell", "embedded_web_engine"})
ALLOWED_INHERITED_ENV = frozenset({"LANG", "LC_ALL", "LC_CTYPE", "XDG_RUNTIME_DIR", "WAYLAND_DISPLAY"})
FORBIDDEN_ENV = frozenset({"KOA_NODE_AGENT_SOCKET", "KOA_PRIVILEGED_BROKER_SOCKET", "KOA_BROKER_SOCKET"})
LAUNCH_CONTRACT_KEYS = frozenset(
    {
        "general_purpose_browser",
        "unrestricted_terminal",
        "desktop_launcher",
        "direct_privileged_broker_access",
        "unrestricted_external_navigation",
        "developer_tools",
        "downloads",
    }
)
AUTHORITY_CONTEXTS = {
    "interactive_user": None,
    "maintenance": "maintenance_authorized",
    "recovery": "recovery_authorized",
}


class SessionRuntimeError(RuntimeError):
    """A fail-closed runtime-plan or session-supervision error."""


@dataclass(frozen=True, slots=True)
class SurfacePlan:
    """One already-resolved process surface selected by the effective profile."""

    surface_id: str
    role: str
    session_modes: tuple[str, ...]
    argv: tuple[str, ...]
    cwd: str
    native_capabilities: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ResolvedSessionRuntime:
    """Resolved process set for exactly one session mode."""

    effective_profile_id: str
    session_mode: str
    required_roles: tuple[str, ...]
    optional_roles: tuple[str, ...]
    surfaces: tuple[SurfacePlan, ...]

    def surface(self, role: str) -> SurfacePlan | None:
        return next((surface for surface in self.surfaces if surface.role == role), None)


def _exact_keys(value: Mapping[str, Any], expected: set[str] | frozenset[str], label: str) -> None:
    actual = set(value)
    missing = sorted(expected - actual)
    unknown = sorted(actual - expected)
    if missing or unknown:
        raise SessionRuntimeError(f"{label} keys mismatch; missing={missing}, unknown={unknown}")


def _string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value or "\x00" in value:
        raise SessionRuntimeError(f"{label} must be a non-empty NUL-free string")
    return value


def _string_list(value: Any, label: str, *, maximum: int = 32) -> tuple[str, ...]:
    if not isinstance(value, list) or len(value) > maximum:
        raise SessionRuntimeError(f"{label} must be a bounded string array")
    result = tuple(_string(item, f"{label}[]") for item in value)
    if len(result) != len(set(result)):
        raise SessionRuntimeError(f"{label} contains duplicates")
    return result


def _read_json(path: Path, *, require_protected: bool) -> dict[str, Any]:
    try:
        original = path.absolute()
        info = original.lstat()
        if stat.S_ISLNK(info.st_mode):
            raise SessionRuntimeError(f"active profile may not be a symlink: {path}")
        resolved = original.resolve(strict=True)
        if resolved != original or not resolved.is_file():
            raise SessionRuntimeError(f"active profile must be a regular direct path: {path}")
        if require_protected:
            info = resolved.stat()
            if info.st_uid != 0:
                raise SessionRuntimeError("active profile must be owned by uid 0")
            if info.st_mode & (stat.S_IWGRP | stat.S_IWOTH):
                raise SessionRuntimeError("active profile must not be group/world writable")
        raw = resolved.read_bytes()
    except SessionRuntimeError:
        raise
    except OSError as exc:
        raise SessionRuntimeError(f"active profile is unavailable: {path}") from exc
    if len(raw) > MAX_ACTIVE_PROFILE_BYTES:
        raise SessionRuntimeError("active profile exceeds the size limit")
    try:
        value = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SessionRuntimeError("active profile is not valid JSON") from exc
    if not isinstance(value, dict):
        raise SessionRuntimeError("active profile root must be an object")
    return value


def _overlay_ids(profile: Mapping[str, Any]) -> set[str]:
    candidates: list[Any] = []
    for owner in (profile, profile.get("effective_profile")):
        if not isinstance(owner, Mapping):
            continue
        if isinstance(owner.get("effective_overlay_ids"), list):
            candidates.extend(owner["effective_overlay_ids"])
        if isinstance(owner.get("overlays"), list):
            candidates.extend(owner["overlays"])
    result: set[str] = set()
    for item in candidates:
        if isinstance(item, str):
            result.add(item)
        elif isinstance(item, Mapping):
            identifier = item.get("profile_id") or item.get("overlay_id")
            if isinstance(identifier, str):
                result.add(identifier)
    return result


def _effective_profile_id(profile: Mapping[str, Any]) -> str:
    direct = profile.get("effective_profile_id")
    if isinstance(direct, str) and direct:
        return direct
    nested = profile.get("effective_profile")
    if isinstance(nested, Mapping):
        value = nested.get("effective_profile_id")
        if isinstance(value, str) and value:
            return value
    raise SessionRuntimeError("active profile does not identify the effective profile")


def _parse_surface(value: Any, index: int) -> SurfacePlan:
    if not isinstance(value, Mapping):
        raise SessionRuntimeError(f"session_runtime.surfaces[{index}] must be an object")
    expected = {
        "surface_id",
        "role",
        "session_modes",
        "argv",
        "cwd",
        "launch_contract",
        "native_capabilities",
    }
    _exact_keys(value, expected, f"session_runtime.surfaces[{index}]")
    surface_id = _string(value["surface_id"], f"session_runtime.surfaces[{index}].surface_id")
    role = _string(value["role"], f"session_runtime.surfaces[{index}].role")
    if role not in ALLOWED_SURFACE_ROLES:
        raise SessionRuntimeError(f"surface {surface_id} has an unsupported role: {role}")
    modes = _string_list(value["session_modes"], f"surface {surface_id} session_modes", maximum=3)
    if not modes or not set(modes).issubset(ALLOWED_SESSION_MODES):
        raise SessionRuntimeError(f"surface {surface_id} has invalid session modes")
    argv = _string_list(value["argv"], f"surface {surface_id} argv")
    if not argv or not Path(argv[0]).is_absolute():
        raise SessionRuntimeError(f"surface {surface_id} requires an absolute executable argv[0]")
    cwd = _string(value["cwd"], f"surface {surface_id} cwd")
    if cwd != "session_runtime" and not Path(cwd).is_absolute():
        raise SessionRuntimeError(f"surface {surface_id} cwd must be absolute or 'session_runtime'")
    launch_contract = value["launch_contract"]
    if not isinstance(launch_contract, Mapping):
        raise SessionRuntimeError(f"surface {surface_id} launch_contract must be an object")
    _exact_keys(launch_contract, LAUNCH_CONTRACT_KEYS, f"surface {surface_id} launch_contract")
    for key in LAUNCH_CONTRACT_KEYS:
        if type(launch_contract[key]) is not bool:
            raise SessionRuntimeError(f"surface {surface_id} launch_contract.{key} must be boolean")
        if launch_contract[key]:
            raise SessionRuntimeError(f"surface {surface_id} enables prohibited capability: {key}")
    native_capabilities = _string_list(
        value["native_capabilities"], f"surface {surface_id} native_capabilities", maximum=16
    )
    if role != "native_shell" and native_capabilities:
        raise SessionRuntimeError(f"only the native shell may declare native capabilities: {surface_id}")
    return SurfacePlan(surface_id, role, modes, argv, cwd, native_capabilities)


def load_runtime_projection(
    path: Path,
    *,
    plan_key: str = "session_runtime",
    require_protected: bool = True,
) -> tuple[str, tuple[SurfacePlan, ...]]:
    """Load the active profile's already-resolved appliance runtime projection."""

    profile = _read_json(path, require_protected=require_protected)
    if PROFILE_OVERLAY not in _overlay_ids(profile):
        raise SessionRuntimeError("active effective profile does not include appliance_shell")
    projection = profile.get(plan_key)
    if not isinstance(projection, Mapping):
        raise SessionRuntimeError(f"active effective profile has no {plan_key!r} runtime projection")
    _exact_keys(projection, {"schema_version", "profile_overlay", "surfaces"}, plan_key)
    if projection["schema_version"] != RUNTIME_PLAN_SCHEMA_VERSION:
        raise SessionRuntimeError("unsupported session runtime plan schema")
    if projection["profile_overlay"] != PROFILE_OVERLAY:
        raise SessionRuntimeError("session runtime plan is not scoped to appliance_shell")
    raw_surfaces = projection["surfaces"]
    if not isinstance(raw_surfaces, list) or len(raw_surfaces) > 16:
        raise SessionRuntimeError("session runtime surfaces must be a bounded array")
    surfaces = tuple(_parse_surface(value, index) for index, value in enumerate(raw_surfaces))
    ids = [surface.surface_id for surface in surfaces]
    if len(ids) != len(set(ids)):
        raise SessionRuntimeError("session runtime surface_id values must be unique")
    return _effective_profile_id(profile), surfaces


def resolve_session_runtime(
    path: Path,
    *,
    session_mode: str,
    required_roles: Sequence[str],
    optional_roles: Sequence[str],
    required_native_capabilities: Sequence[str],
    plan_key: str = "session_runtime",
    require_protected: bool = True,
) -> ResolvedSessionRuntime:
    """Select only surfaces admitted by the validated session envelope."""

    if session_mode not in ALLOWED_SESSION_MODES:
        raise SessionRuntimeError(f"unsupported session mode: {session_mode}")
    required = tuple(required_roles)
    optional = tuple(optional_roles)
    admitted = set(required) | set(optional)
    if not admitted.issubset(ALLOWED_SURFACE_ROLES) or set(required) & set(optional):
        raise SessionRuntimeError("session surface envelope is invalid")
    effective_profile_id, surfaces = load_runtime_projection(
        path, plan_key=plan_key, require_protected=require_protected
    )
    active = tuple(surface for surface in surfaces if session_mode in surface.session_modes)
    unexpected = sorted({surface.role for surface in active} - admitted)
    if unexpected:
        raise SessionRuntimeError(f"active profile exposes surfaces not admitted by session: {unexpected}")
    by_role: dict[str, SurfacePlan] = {}
    for surface in active:
        if surface.role in by_role:
            raise SessionRuntimeError(f"multiple active surfaces provide role {surface.role}")
        by_role[surface.role] = surface
    missing = sorted(set(required) - set(by_role))
    if missing:
        raise SessionRuntimeError(f"active profile is missing required session surfaces: {missing}")
    native = by_role.get("native_shell")
    required_caps = set(required_native_capabilities)
    if required_caps:
        if native is None:
            raise SessionRuntimeError("required native capabilities need a native shell")
        missing_caps = sorted(required_caps - set(native.native_capabilities))
        if missing_caps:
            raise SessionRuntimeError(f"native shell is missing required capabilities: {missing_caps}")
    selected = tuple(by_role[role] for role in (*required, *optional) if role in by_role)
    return ResolvedSessionRuntime(effective_profile_id, session_mode, required, optional, selected)


def surface_exit_action(role: str, return_code: int) -> str:
    """Return the supervisor action for a child exit without changing policy."""

    if role == "embedded_web_engine":
        return "continue_degraded"
    if role in {"compositor", "native_shell"}:
        return "terminate_session"
    raise SessionRuntimeError(f"unsupported surface role: {role}")


def _json_env_list(name: str) -> tuple[str, ...]:
    raw = os.environ.get(name)
    if raw is None:
        raise SessionRuntimeError(f"{name} is required")
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SessionRuntimeError(f"{name} must contain a JSON string array") from exc
    return _string_list(value, name)


def _validate_inherited_authority_fd(fd: int) -> None:
    if fd < 3:
        raise SessionRuntimeError("authority handoff fd must be non-standard")
    try:
        info = os.fstat(fd)
    except OSError as exc:
        raise SessionRuntimeError("authority handoff fd is not inherited") from exc
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 0:
        raise SessionRuntimeError("authority handoff fd must reference an unlinked regular file")
    if info.st_uid != 0:
        raise SessionRuntimeError("authority handoff fd must remain root-owned")
    if info.st_mode & (stat.S_IWUSR | stat.S_IRWXG | stat.S_IRWXO):
        raise SessionRuntimeError("authority handoff fd must remain owner-read-only")


def _validate_session_environment(
    expected_mode: str,
) -> tuple[Path, str, tuple[str, ...], tuple[str, ...], tuple[str, ...], int]:
    if os.environ.get("KOA_PROFILE_OVERLAY") != PROFILE_OVERLAY:
        raise SessionRuntimeError("session environment is not scoped to appliance_shell")
    if os.environ.get("KOA_SESSION_MODE") != expected_mode:
        raise SessionRuntimeError("session mode environment mismatch")
    runtime_dir = Path(_string(os.environ.get("KOA_SESSION_RUNTIME_DIR"), "KOA_SESSION_RUNTIME_DIR"))
    if not runtime_dir.is_absolute():
        raise SessionRuntimeError("KOA_SESSION_RUNTIME_DIR must be absolute")
    active_profile = Path(_string(os.environ.get("KOA_EFFECTIVE_PROFILE_PATH"), "KOA_EFFECTIVE_PROFILE_PATH"))
    if not active_profile.is_absolute():
        raise SessionRuntimeError("KOA_EFFECTIVE_PROFILE_PATH must be absolute")
    plan_key = _string(os.environ.get("KOA_SESSION_SURFACE_PLAN_KEY"), "KOA_SESSION_SURFACE_PLAN_KEY")
    required = _json_env_list("KOA_SESSION_REQUIRED_SURFACES")
    optional = _json_env_list("KOA_SESSION_OPTIONAL_SURFACES")
    native_caps = _json_env_list("KOA_SESSION_REQUIRED_NATIVE_CAPABILITIES")
    grace_raw = _string(
        os.environ.get("KOA_SESSION_TERMINATION_GRACE_SECONDS"),
        "KOA_SESSION_TERMINATION_GRACE_SECONDS",
    )
    try:
        grace = int(grace_raw)
    except ValueError as exc:
        raise SessionRuntimeError("KOA_SESSION_TERMINATION_GRACE_SECONDS must be an integer") from exc
    if grace < 1 or grace > 60:
        raise SessionRuntimeError("session termination grace must be in [1, 60]")

    expected_context = AUTHORITY_CONTEXTS[expected_mode]
    context = os.environ.get("KOA_SESSION_AUTHORITY_CONTEXT")
    receipt = os.environ.get("KOA_SESSION_DECISION_RECEIPT_ID")
    authority_fd_raw = os.environ.get("KOA_SESSION_AUTHORITY_FD")
    if expected_context is None:
        if context is not None or receipt is not None or authority_fd_raw is not None:
            raise SessionRuntimeError("ordinary session may not receive privileged authority state")
    else:
        if context != expected_context or not receipt or authority_fd_raw is None:
            raise SessionRuntimeError(f"{expected_mode} session requires its validated authority handoff")
        try:
            authority_fd = int(authority_fd_raw)
        except ValueError as exc:
            raise SessionRuntimeError("KOA_SESSION_AUTHORITY_FD must be an integer") from exc
        _validate_inherited_authority_fd(authority_fd)
    return active_profile, plan_key, required, optional, native_caps, grace


def _child_environment(surface: SurfacePlan, runtime_dir: Path, effective_profile_id: str) -> dict[str, str]:
    env: dict[str, str] = {}
    for key in ALLOWED_INHERITED_ENV:
        value = os.environ.get(key)
        if value is not None:
            env[key] = value
    env.update(
        {
            "HOME": str(runtime_dir),
            "KOA_EFFECTIVE_PROFILE_ID": effective_profile_id,
            "KOA_PROFILE_OVERLAY": PROFILE_OVERLAY,
            "KOA_SESSION_MODE": os.environ["KOA_SESSION_MODE"],
            "KOA_SESSION_RUNTIME_DIR": str(runtime_dir),
            "KOA_SESSION_START_STATE": os.environ.get("KOA_SESSION_START_STATE", "locked"),
            "KOA_SESSION_SURFACE_ID": surface.surface_id,
            "KOA_SESSION_SURFACE_ROLE": surface.role,
            "PATH": "/usr/bin:/bin",
        }
    )
    for key in ("KOA_SESSION_AUTHORITY_CONTEXT", "KOA_SESSION_DECISION_RECEIPT_ID"):
        value = os.environ.get(key)
        if value is not None:
            env[key] = value
    for key in FORBIDDEN_ENV:
        env.pop(key, None)
    return env


def _verify_executable(path: Path) -> None:
    try:
        info = path.lstat()
    except OSError as exc:
        raise SessionRuntimeError(f"surface executable is unavailable: {path}") from exc
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
        raise SessionRuntimeError(f"surface executable must be a regular non-symlink file: {path}")
    if info.st_uid != 0 or info.st_mode & (stat.S_IWGRP | stat.S_IWOTH):
        raise SessionRuntimeError(f"surface executable is not protected: {path}")
    if not os.access(path, os.X_OK):
        raise SessionRuntimeError(f"surface executable is not executable: {path}")


def _emit(event: str, **fields: Any) -> None:
    print(json.dumps({"event": event, **fields}, sort_keys=True, separators=(",", ":")), file=sys.stderr, flush=True)


def _terminate(processes: Mapping[str, subprocess.Popen[bytes]], grace_seconds: int) -> None:
    for process in processes.values():
        if process.poll() is None:
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
    deadline = time.monotonic() + grace_seconds
    for process in processes.values():
        if process.poll() is not None:
            continue
        remaining = max(0.01, deadline - time.monotonic())
        try:
            process.wait(timeout=remaining)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait(timeout=1)


def supervise(runtime: ResolvedSessionRuntime, runtime_dir: Path, *, grace_seconds: int) -> int:
    """Launch resolved surfaces with structured argv and preserve native fallback."""

    processes: dict[str, subprocess.Popen[bytes]] = {}
    stop_requested = False

    def request_stop(signum: int, _frame: object) -> None:
        nonlocal stop_requested
        stop_requested = True
        _emit("session_stop_requested", signal=signum)

    previous = {sig: signal.getsignal(sig) for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)}
    for sig in previous:
        signal.signal(sig, request_stop)
    try:
        for surface in runtime.surfaces:
            executable = Path(surface.argv[0])
            _verify_executable(executable)
            cwd = runtime_dir if surface.cwd == "session_runtime" else Path(surface.cwd)
            if not cwd.is_absolute() or not cwd.is_dir():
                raise SessionRuntimeError(f"surface cwd is unavailable: {cwd}")
            process = subprocess.Popen(
                list(surface.argv),
                cwd=cwd,
                env=_child_environment(surface, runtime_dir, runtime.effective_profile_id),
                close_fds=True,
                start_new_session=True,
            )
            processes[surface.role] = process
            _emit("surface_started", role=surface.role, surface_id=surface.surface_id, pid=process.pid)
            try:
                early_code = process.wait(timeout=0.05)
            except subprocess.TimeoutExpired:
                early_code = None
            if early_code is not None:
                action = surface_exit_action(surface.role, early_code)
                _emit("surface_exited_during_start", role=surface.role, return_code=early_code, action=action)
                if action == "terminate_session":
                    return early_code if early_code != 0 else 70
                processes.pop(surface.role, None)

        if "native_shell" not in processes or "compositor" not in processes:
            raise SessionRuntimeError("required native session surfaces did not remain available")

        while not stop_requested:
            for role, process in tuple(processes.items()):
                code = process.poll()
                if code is None:
                    continue
                action = surface_exit_action(role, code)
                _emit("surface_exited", role=role, return_code=code, action=action)
                processes.pop(role, None)
                if action == "continue_degraded":
                    _emit("native_fallback_preserved", failed_role=role)
                    continue
                return code if code != 0 else (0 if role == "native_shell" else 70)
            time.sleep(0.1)
        return 0
    finally:
        _terminate(processes, grace_seconds)
        for sig, handler in previous.items():
            signal.signal(sig, handler)


def main_for_mode(expected_mode: str) -> int:
    try:
        active_profile, plan_key, required, optional, native_caps, grace = _validate_session_environment(expected_mode)
        runtime = resolve_session_runtime(
            active_profile,
            session_mode=expected_mode,
            required_roles=required,
            optional_roles=optional,
            required_native_capabilities=native_caps,
            plan_key=plan_key,
            require_protected=True,
        )
        runtime_dir = Path(os.environ["KOA_SESSION_RUNTIME_DIR"])
        return supervise(runtime, runtime_dir, grace_seconds=grace)
    except SessionRuntimeError as exc:
        print(json.dumps({"status": "blocked", "error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 78


__all__ = [
    "ResolvedSessionRuntime",
    "SessionRuntimeError",
    "SurfacePlan",
    "load_runtime_projection",
    "main_for_mode",
    "resolve_session_runtime",
    "surface_exit_action",
    "supervise",
]
