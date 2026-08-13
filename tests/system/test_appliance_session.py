from __future__ import annotations

from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import sys
import tomllib

import pytest

ROOT = Path(__file__).resolve().parents[2]


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _load_launcher():
    return _load_module(
        "koa_session_launcher_system_test",
        ROOT / "host/sessions/koa-session-launcher.py",
    )


def _load_runtime():
    return _load_module(
        "koa_session_runtime_system_test",
        ROOT / "host/sessions/session_runtime.py",
    )


def _toml(path: Path):
    with path.open("rb") as stream:
        return tomllib.load(stream)


def _launch_contract() -> dict[str, bool]:
    return {
        "general_purpose_browser": False,
        "unrestricted_terminal": False,
        "desktop_launcher": False,
        "direct_privileged_broker_access": False,
        "unrestricted_external_navigation": False,
        "developer_tools": False,
        "downloads": False,
    }


def _surface(
    surface_id: str,
    role: str,
    modes: list[str],
    *,
    native_capabilities: list[str] | None = None,
) -> dict[str, object]:
    return {
        "surface_id": surface_id,
        "role": role,
        "session_modes": modes,
        "argv": [f"/usr/libexec/koa/runtime/{surface_id}"],
        "cwd": "session_runtime",
        "launch_contract": _launch_contract(),
        "native_capabilities": native_capabilities or [],
    }


def _active_profile() -> dict[str, object]:
    modes = ["interactive_user", "maintenance", "recovery"]
    return {
        "effective_profile_id": "effective:sovereign_linux_node:test",
        "primary_profile": {"profile_id": "sovereign_linux_node", "version": "1.0.0"},
        "overlays": [{"profile_id": "appliance_shell", "version": "1.0.0"}],
        "session_runtime": {
            "schema_version": "1.0.0",
            "profile_overlay": "appliance_shell",
            "surfaces": [
                _surface("compositor", "compositor", modes),
                _surface(
                    "native-shell",
                    "native_shell",
                    modes,
                    native_capabilities=[
                        "status",
                        "recovery",
                        "accessibility",
                        "session_exit",
                        "safe_maintenance",
                        "maintenance",
                    ],
                ),
                _surface("embedded-engine", "embedded_web_engine", ["interactive_user"]),
            ],
        },
    }


def _write_active_profile(tmp_path: Path, value: dict[str, object]) -> Path:
    path = tmp_path / "active-profile.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


def test_appliance_session_is_closed_and_non_privileged() -> None:
    launcher = _load_launcher()
    graphical = _toml(ROOT / "host/sessions/graphical-session.toml")
    session = _toml(ROOT / "host/sessions/appliance-session.toml")

    runtime_policy = launcher.validate_graphical_policy(graphical)
    plan = launcher.build_session_plan(session)

    assert plan.session_mode == "interactive_user"
    assert plan.requires_handoff is False
    assert plan.critical_transition_receipt_required is False
    assert plan.executable == Path("/usr/libexec/koa/koa-appliance-session")
    assert plan.required_surface_roles == ("compositor", "native_shell")
    assert plan.optional_surface_roles == ("embedded_web_engine",)
    assert set(plan.inherited_environment) <= launcher.ALLOWED_INHERITED_ENV
    assert runtime_policy.effective_profile_path == Path("/etc/koa/active/profile.json")
    assert session["authority"]["direct_privileged_broker_access"] is False
    assert graphical["failure"]["fallback_to_unrestricted_desktop"] is False


def test_appliance_policy_rejects_privilege_desktop_and_surface_expansion() -> None:
    launcher = _load_launcher()
    session = _toml(ROOT / "host/sessions/appliance-session.toml")
    privileged = deepcopy(session)
    privileged["authority"]["direct_privileged_broker_access"] = True
    with pytest.raises(launcher.LauncherError, match="privileged broker"):
        launcher.build_session_plan(privileged)

    expanded = deepcopy(session)
    expanded["runtime"]["optional_surface_roles"].append("general_terminal")
    with pytest.raises(launcher.LauncherError, match="runtime surface envelope"):
        launcher.build_session_plan(expanded)

    graphical = _toml(ROOT / "host/sessions/graphical-session.toml")
    fallback = deepcopy(graphical)
    fallback["failure"]["fallback_to_unrestricted_desktop"] = True
    with pytest.raises(launcher.LauncherError, match="desktop fallback"):
        launcher.validate_graphical_policy(fallback)


def test_maintenance_and_recovery_preserve_separate_authority_contracts() -> None:
    launcher = _load_launcher()
    for filename, mode, context in (
        ("maintenance-session.toml", "maintenance", "maintenance_authorized"),
        ("recovery-session.toml", "recovery", "recovery_authorized"),
    ):
        plan = launcher.build_session_plan(_toml(ROOT / "host/sessions" / filename))
        assert plan.session_mode == mode
        assert plan.requires_handoff is True
        assert plan.authority_context == context
        assert plan.critical_transition_receipt_required is True
        assert plan.optional_surface_roles == ()


def test_runtime_resolves_only_surfaces_admitted_by_effective_profile(tmp_path: Path) -> None:
    runtime = _load_runtime()
    path = _write_active_profile(tmp_path, _active_profile())

    resolved = runtime.resolve_session_runtime(
        path,
        session_mode="interactive_user",
        required_roles=("compositor", "native_shell"),
        optional_roles=("embedded_web_engine",),
        required_native_capabilities=(
            "status",
            "recovery",
            "accessibility",
            "session_exit",
            "safe_maintenance",
        ),
        require_protected=False,
    )

    assert [surface.role for surface in resolved.surfaces] == [
        "compositor",
        "native_shell",
        "embedded_web_engine",
    ]
    assert resolved.effective_profile_id == "effective:sovereign_linux_node:test"


def test_runtime_rejects_unadmitted_or_general_purpose_surfaces(tmp_path: Path) -> None:
    runtime = _load_runtime()
    profile = _active_profile()
    engine = profile["session_runtime"]["surfaces"][2]
    engine["session_modes"].append("maintenance")
    path = _write_active_profile(tmp_path, profile)

    with pytest.raises(runtime.SessionRuntimeError, match="not admitted"):
        runtime.resolve_session_runtime(
            path,
            session_mode="maintenance",
            required_roles=("compositor", "native_shell"),
            optional_roles=(),
            required_native_capabilities=("status", "accessibility", "session_exit", "maintenance"),
            require_protected=False,
        )

    profile = _active_profile()
    profile["session_runtime"]["surfaces"][2]["launch_contract"]["general_purpose_browser"] = True
    path = _write_active_profile(tmp_path, profile)
    with pytest.raises(runtime.SessionRuntimeError, match="prohibited capability"):
        runtime.resolve_session_runtime(
            path,
            session_mode="interactive_user",
            required_roles=("compositor", "native_shell"),
            optional_roles=("embedded_web_engine",),
            required_native_capabilities=("status", "recovery", "accessibility", "session_exit", "safe_maintenance"),
            require_protected=False,
        )


def test_web_engine_failure_preserves_required_native_fallback(tmp_path: Path) -> None:
    runtime = _load_runtime()
    path = _write_active_profile(tmp_path, _active_profile())
    resolved = runtime.resolve_session_runtime(
        path,
        session_mode="interactive_user",
        required_roles=("compositor", "native_shell"),
        optional_roles=("embedded_web_engine",),
        required_native_capabilities=("status", "recovery", "accessibility", "session_exit", "safe_maintenance"),
        require_protected=False,
    )

    native = resolved.surface("native_shell")
    assert native is not None
    assert {"status", "recovery", "accessibility", "session_exit", "safe_maintenance"} <= set(
        native.native_capabilities
    )
    assert runtime.surface_exit_action("embedded_web_engine", 1) == "continue_degraded"
    assert runtime.surface_exit_action("native_shell", 1) == "terminate_session"



def test_supervisor_keeps_native_surfaces_after_web_engine_exit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    runtime = _load_runtime()
    monkeypatch.setenv("KOA_SESSION_MODE", "interactive_user")
    monkeypatch.setenv("KOA_SESSION_START_STATE", "locked")

    no_native_capabilities: tuple[str, ...] = ()
    surfaces = (
        runtime.SurfacePlan(
            "test-compositor",
            "compositor",
            ("interactive_user",),
            ("/usr/bin/sleep", "0.5"),
            "session_runtime",
            no_native_capabilities,
        ),
        runtime.SurfacePlan(
            "test-native-shell",
            "native_shell",
            ("interactive_user",),
            ("/usr/bin/sleep", "0.2"),
            "session_runtime",
            ("status", "recovery", "accessibility", "session_exit", "safe_maintenance"),
        ),
        runtime.SurfacePlan(
            "test-engine",
            "embedded_web_engine",
            ("interactive_user",),
            ("/usr/bin/false",),
            "session_runtime",
            no_native_capabilities,
        ),
    )
    resolved = runtime.ResolvedSessionRuntime(
        "effective:test",
        "interactive_user",
        ("compositor", "native_shell"),
        ("embedded_web_engine",),
        surfaces,
    )

    assert runtime.supervise(resolved, tmp_path, grace_seconds=1) == 0


def test_runtime_blocks_missing_projection_and_authority_context(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    runtime = _load_runtime()
    profile = _active_profile()
    profile.pop("session_runtime")
    path = _write_active_profile(tmp_path, profile)
    with pytest.raises(runtime.SessionRuntimeError, match="no 'session_runtime' runtime projection"):
        runtime.resolve_session_runtime(
            path,
            session_mode="interactive_user",
            required_roles=("compositor", "native_shell"),
            optional_roles=("embedded_web_engine",),
            required_native_capabilities=("status",),
            require_protected=False,
        )

    monkeypatch.setenv("KOA_PROFILE_OVERLAY", "appliance_shell")
    monkeypatch.setenv("KOA_SESSION_MODE", "maintenance")
    monkeypatch.setenv("KOA_SESSION_RUNTIME_DIR", str(tmp_path))
    monkeypatch.setenv("KOA_EFFECTIVE_PROFILE_PATH", str(path))
    monkeypatch.setenv("KOA_SESSION_SURFACE_PLAN_KEY", "session_runtime")
    monkeypatch.setenv("KOA_SESSION_REQUIRED_SURFACES", '["compositor","native_shell"]')
    monkeypatch.setenv("KOA_SESSION_OPTIONAL_SURFACES", "[]")
    monkeypatch.setenv(
        "KOA_SESSION_REQUIRED_NATIVE_CAPABILITIES",
        '["status","accessibility","session_exit","maintenance"]',
    )
    monkeypatch.setenv("KOA_SESSION_TERMINATION_GRACE_SECONDS", "5")
    monkeypatch.delenv("KOA_SESSION_AUTHORITY_CONTEXT", raising=False)
    monkeypatch.delenv("KOA_SESSION_DECISION_RECEIPT_ID", raising=False)
    with pytest.raises(runtime.SessionRuntimeError, match="validated authority handoff"):
        runtime._validate_session_environment("maintenance")

    monkeypatch.setenv("KOA_SESSION_AUTHORITY_CONTEXT", "maintenance_authorized")
    monkeypatch.setenv("KOA_SESSION_DECISION_RECEIPT_ID", "receipt:test")
    monkeypatch.setenv("KOA_SESSION_AUTHORITY_FD", "9")
    monkeypatch.setattr(runtime, "_validate_inherited_authority_fd", lambda fd: None)
    _, _, required, optional, native_caps, grace = runtime._validate_session_environment(
        "maintenance"
    )
    assert required == ("compositor", "native_shell")
    assert optional == ()
    assert "maintenance" in native_caps
    assert grace == 5


def test_session_entrypoints_and_runtime_destinations_are_packaged_by_mapping() -> None:
    expected = {
        "host/sessions/session_runtime.py": "/usr/libexec/koa/session_runtime.py",
        "host/sessions/koa-appliance-session.py": "/usr/libexec/koa/koa-appliance-session",
        "host/sessions/koa-maintenance-session.py": "/usr/libexec/koa/koa-maintenance-session",
        "host/sessions/koa-recovery-session.py": "/usr/libexec/koa/koa-recovery-session",
    }
    registry = json.loads((ROOT / ".koa/runtime-paths.json").read_text(encoding="utf-8"))
    mappings = {
        item["source"]: item["destination"]
        for item in registry["repository_payload_mappings"]
        if item.get("owner") == "host"
    }
    immutable = next(item for item in registry["path_classes"] if item["id"] == "immutable_payload")
    image = _toml(ROOT / "packaging/system/image.toml")

    assert expected.items() <= mappings.items()
    assert set(expected.values()) <= set(immutable["paths"])
    assert "host" in image["payload_selection"]["include_owners"]
    assert "immutable_payload" in image["payload_selection"]["include_path_classes"]
    for source in expected:
        assert (ROOT / source).is_file()
