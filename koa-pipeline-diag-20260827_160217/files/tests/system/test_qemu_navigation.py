from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time
from typing import Any

import pytest

SYSTEM_TESTS = Path(__file__).resolve().parent
if str(SYSTEM_TESTS) not in sys.path:
    sys.path.insert(0, str(SYSTEM_TESTS))

from qemu_harness import QemuBlockedError, QemuHarness, QemuHarnessError, framebuffer_has_content

ROOT = Path(__file__).resolve().parents[2]
MACHINE_CONFIG = ROOT / "tests/system/qemu-machine.toml"
KOA_SPACES_LOCK = ROOT / "integrations/koa-spaces/source.lock.json"


def _required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise QemuBlockedError(f"required machine-test input is missing: {name}")
    return value


def _regular_file_from_env(name: str) -> Path:
    path = Path(_required_env(name)).expanduser()
    if not path.is_file() or path.is_symlink():
        raise QemuBlockedError(f"{name} must reference a regular file: {path}")
    return path.resolve()


def _json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise QemuBlockedError(f"{label} is not readable JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise QemuBlockedError(f"{label} must be a JSON object")
    return value


def _selected_surface(profile: dict[str, Any], surface_id: str) -> dict[str, Any]:
    runtime = profile.get("session_runtime")
    if not isinstance(runtime, dict):
        raise QemuBlockedError("effective profile has no session_runtime projection")
    surfaces = runtime.get("surfaces")
    if not isinstance(surfaces, list):
        raise QemuBlockedError("effective profile session_runtime.surfaces must be an array")
    selected = [
        surface
        for surface in surfaces
        if isinstance(surface, dict) and surface.get("surface_id") == surface_id
    ]
    if len(selected) != 1:
        raise QemuBlockedError(
            f"navigation surface {surface_id!r} is not uniquely admitted by the effective profile"
        )
    modes = selected[0].get("session_modes")
    if not isinstance(modes, list) or "interactive_user" not in modes:
        raise QemuBlockedError(
            f"navigation surface {surface_id!r} is not admitted for interactive_user"
        )
    return selected[0]


def _koa_spaces_selected() -> bool:
    value = os.environ.get("KOA_QEMU_KOA_SPACES_SELECTION", "not_selected").strip().lower()
    if value not in {"selected", "not_selected"}:
        raise QemuBlockedError("KOA_QEMU_KOA_SPACES_SELECTION must be 'selected' or 'not_selected'")
    return value == "selected"


def _assert_selected_koa_spaces_is_admitted() -> None:
    if not _koa_spaces_selected():
        return
    lock = _json_object(KOA_SPACES_LOCK, "kOA Spaces source lock")
    implementation = lock.get("implementation_source")
    if not isinstance(implementation, dict):
        raise QemuBlockedError("kOA Spaces source lock has no implementation_source object")
    if implementation.get("status") != "resolved" or not implementation.get("revision"):
        raise QemuBlockedError(
            "kOA Spaces is selected but its authoritative source pin is unresolved"
        )


def _network_enabled() -> bool:
    value = os.environ.get("KOA_QEMU_NETWORK", "off").strip().lower()
    if value not in {"on", "off"}:
        raise QemuBlockedError("KOA_QEMU_NETWORK must be 'on' or 'off'")
    return value == "on"


def _navigation_qcodes() -> tuple[str, ...]:
    raw = _required_env("KOA_QEMU_NAVIGATION_KEYS")
    values = tuple(item.strip().lower() for item in raw.split(",") if item.strip())
    if (
        not values
        or len(values) > 8
        or any(re.fullmatch(r"[a-z0-9-]+", item) is None for item in values)
    ):
        raise QemuBlockedError(
            "KOA_QEMU_NAVIGATION_KEYS must contain one to eight comma-separated QEMU qcodes"
        )
    return values


def _send_navigation(session, qcodes: tuple[str, ...]) -> None:
    for qcode in qcodes:
        session._qmp_execute("send-key", {"keys": [{"type": "qcode", "data": qcode}]})
        time.sleep(0.15)


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_non_spaces_profile_surface_does_not_require_koa_spaces_source() -> None:
    profile = {
        "session_runtime": {
            "surfaces": [
                {
                    "surface_id": "native-shell",
                    "session_modes": ["interactive_user"],
                }
            ]
        }
    }

    surface = _selected_surface(profile, "native-shell")

    assert surface["surface_id"] == "native-shell"


def test_navigation_surface_must_be_admitted_by_effective_profile() -> None:
    profile = {"session_runtime": {"surfaces": []}}

    with pytest.raises(QemuBlockedError, match="not uniquely admitted"):
        _selected_surface(profile, "unregistered-surface")


def test_reference_image_navigates_on_profile_selected_local_surface() -> None:
    try:
        image = Path(_required_env("KOA_QEMU_IMAGE")).expanduser()
        active_profile = _json_object(
            _regular_file_from_env("KOA_QEMU_ACTIVE_PROFILE"), "effective profile"
        )
        surface_id = _required_env("KOA_QEMU_NAVIGATION_SURFACE_ID")
        ready_regex = _required_env("KOA_QEMU_NAVIGATION_READY_REGEX")
        result_regex = _required_env("KOA_QEMU_NAVIGATION_RESULT_REGEX")
        qcodes = _navigation_qcodes()
        image_format = os.environ.get("KOA_QEMU_IMAGE_FORMAT", "raw").strip().lower()
        _selected_surface(active_profile, surface_id)
        _assert_selected_koa_spaces_is_admitted()
        harness = QemuHarness.from_file(MACHINE_CONFIG)
        with harness.launch(
            image, network_enabled=_network_enabled(), image_format=image_format
        ) as session:
            session.wait_for_patterns({"navigation_ready": ready_regex})
            before = session.capture_framebuffer("navigation-before.ppm")
            before_digest = _digest(before)
            before_visible = framebuffer_has_content(before)
            if session.serial_log is None:
                raise QemuHarnessError(
                    "QEMU serial log is unavailable during navigation validation"
                )
            before_serial = session.serial_log.read_text(encoding="utf-8", errors="replace")
            if re.search(result_regex, before_serial, re.MULTILINE):
                raise QemuHarnessError(
                    "navigation result marker was already present before navigation input"
                )
            _send_navigation(session, qcodes)
            session.wait_for_patterns({"navigation_result": result_regex})
            after = session.capture_framebuffer("navigation-after.ppm")
            after_digest = _digest(after)
            after_visible = framebuffer_has_content(after)
    except QemuBlockedError as exc:
        pytest.fail(f"BLOCKED: {exc}", pytrace=False)
    except (QemuHarnessError, re.error) as exc:
        pytest.fail(str(exc), pytrace=False)

    assert before_visible and after_visible, (
        "the selected navigation surface must be visibly rendered"
    )
    assert before_digest != after_digest, (
        "navigation input completed without an observable framebuffer transition"
    )
