"""Static and machine-observed confinement checks for the appliance session."""

from __future__ import annotations

import os
from pathlib import Path
import re
import sys
import tomllib

import pytest

ROOT = Path(__file__).resolve().parents[2]
SYSTEM_TESTS = ROOT / "tests/system"
if str(SYSTEM_TESTS) not in sys.path:
    sys.path.insert(0, str(SYSTEM_TESTS))

from qemu_harness import (
    QemuBlockedError,
    QemuHarness,
    QemuHarnessError,
    framebuffer_has_content,
)

MACHINE_CONFIG = ROOT / "tests/system/qemu-machine.toml"
GRAPHICAL_POLICY = ROOT / "host/sessions/graphical-session.toml"
APPLIANCE_SESSION = ROOT / "host/sessions/appliance-session.toml"
APPLIANCE_SETTINGS = ROOT / "profiles/implementation-settings/appliance-shell.toml"


def _required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise QemuBlockedError(f"required confinement machine-test input is missing: {name}")
    return value


def _regular_file_from_env(name: str) -> Path:
    path = Path(_required_env(name)).expanduser()
    if not path.is_file() or path.is_symlink():
        raise QemuBlockedError(f"{name} must reference a regular file: {path}")
    return path.resolve()


def _network_enabled() -> bool:
    value = os.environ.get("KOA_QEMU_NETWORK", "off").strip().lower()
    if value not in {"on", "off"}:
        raise QemuBlockedError("KOA_QEMU_NETWORK must be 'on' or 'off'")
    return value == "on"


def _toml(path: Path) -> dict[str, object]:
    with path.open("rb") as stream:
        value = tomllib.load(stream)
    assert isinstance(value, dict)
    return value


def test_appliance_policy_has_no_general_desktop_or_direct_privilege_surface() -> None:
    graphical = _toml(GRAPHICAL_POLICY)
    compositor = graphical.get("compositor")
    surface = graphical.get("application_surface")
    failure = graphical.get("failure")
    assert isinstance(compositor, dict)
    assert isinstance(surface, dict)
    assert isinstance(failure, dict)

    assert compositor.get("full_desktop_environment") is False
    assert compositor.get("x11_fallback") is False
    assert compositor.get("application_allowlist") is True
    for key in (
        "arbitrary_application_launcher",
        "unrestricted_terminal",
        "package_manager_ui",
        "host_administration_ui",
        "development_tools",
        "unrestricted_file_browser",
        "unrestricted_external_navigation",
    ):
        assert surface.get(key) is False
    assert failure.get("fallback_to_unrestricted_desktop") is False

    ordinary = _toml(APPLIANCE_SESSION)
    authority = ordinary.get("authority")
    runtime = ordinary.get("runtime")
    assert isinstance(authority, dict)
    assert isinstance(runtime, dict)
    assert authority.get("direct_privileged_broker_access") is False
    assert authority.get("privileged_effects") == "none"
    assert runtime.get("required_surface_roles") == ["compositor", "native_shell"]

    settings = _toml(APPLIANCE_SETTINGS)
    implementation = settings.get("implementation")
    assert isinstance(implementation, dict)
    shell = implementation.get("shell")
    session = implementation.get("session")
    assert isinstance(shell, dict)
    assert isinstance(session, dict)
    assert shell.get("full_desktop_environment") is False
    assert shell.get("unrestricted_browser_chrome") is False
    assert shell.get("unrestricted_external_navigation") is False
    assert session.get("unrestricted_terminal") is False
    assert session.get("package_manager_ui") is False
    assert session.get("host_administration_ui") is False
    assert session.get("development_tools") is False


def test_reference_appliance_observes_denied_general_and_privileged_paths() -> None:
    try:
        image = _regular_file_from_env("KOA_QEMU_IMAGE")
        expected_release = _required_env("KOA_QEMU_EXPECTED_RELEASE_IDENTITY")
        session_ready_regex = _required_env("KOA_QEMU_CONFINEMENT_READY_REGEX")
        general_denied_regex = _required_env("KOA_QEMU_GENERAL_SURFACE_DENIED_REGEX")
        privilege_denied_regex = _required_env("KOA_QEMU_PRIVILEGE_PATH_DENIED_REGEX")
        image_format = os.environ.get("KOA_QEMU_IMAGE_FORMAT", "raw").strip().lower()

        harness = QemuHarness.from_file(MACHINE_CONFIG)
        with harness.launch(
            image,
            network_enabled=_network_enabled(),
            image_format=image_format,
        ) as session:
            observed = session.wait_for_patterns(
                {
                    "release_identity": re.escape(expected_release),
                    "appliance_ready": session_ready_regex,
                    "general_surface_denied": general_denied_regex,
                    "privilege_path_denied": privilege_denied_regex,
                }
            )
            framebuffer = session.capture_framebuffer("appliance-confinement.ppm")
            visible = framebuffer_has_content(framebuffer)
    except QemuBlockedError as exc:
        pytest.fail(f"BLOCKED: {exc}", pytrace=False)
    except (QemuHarnessError, re.error) as exc:
        pytest.fail(str(exc), pytrace=False)

    assert set(observed) == {
        "release_identity",
        "appliance_ready",
        "general_surface_denied",
        "privilege_path_denied",
    }
    assert visible, "confinement markers were observed but the appliance surface remained blank"
