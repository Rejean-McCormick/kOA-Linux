from __future__ import annotations

from copy import deepcopy
import importlib.util
from pathlib import Path
import sys
import tomllib

import pytest

ROOT = Path(__file__).resolve().parents[2]


def _load_launcher():
    path = ROOT / "host/sessions/koa-session-launcher.py"
    spec = importlib.util.spec_from_file_location("koa_session_launcher_system_test", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _toml(path: Path):
    with path.open("rb") as stream:
        return tomllib.load(stream)


def test_appliance_session_is_closed_and_non_privileged() -> None:
    launcher = _load_launcher()
    graphical = _toml(ROOT / "host/sessions/graphical-session.toml")
    session = _toml(ROOT / "host/sessions/appliance-session.toml")

    launcher.validate_graphical_policy(graphical)
    plan = launcher.build_session_plan(session)

    assert plan.session_mode == "interactive_user"
    assert plan.requires_handoff is False
    assert plan.critical_transition_receipt_required is False
    assert plan.executable == Path("/usr/libexec/koa/koa-appliance-session")
    assert set(plan.inherited_environment) <= launcher.ALLOWED_INHERITED_ENV
    assert session["authority"]["direct_privileged_broker_access"] is False
    assert graphical["failure"]["fallback_to_unrestricted_desktop"] is False


def test_appliance_policy_rejects_privilege_and_desktop_fallback() -> None:
    launcher = _load_launcher()
    session = _toml(ROOT / "host/sessions/appliance-session.toml")
    privileged = deepcopy(session)
    privileged["authority"]["direct_privileged_broker_access"] = True
    with pytest.raises(launcher.LauncherError, match="privileged broker"):
        launcher.build_session_plan(privileged)

    graphical = _toml(ROOT / "host/sessions/graphical-session.toml")
    fallback = deepcopy(graphical)
    fallback["failure"]["fallback_to_unrestricted_desktop"] = True
    with pytest.raises(launcher.LauncherError, match="desktop fallback"):
        launcher.validate_graphical_policy(fallback)
