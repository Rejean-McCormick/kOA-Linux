from __future__ import annotations

import json
import os
from pathlib import Path
import re
import sys
import time
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[2]
SYSTEM_TESTS = ROOT / "tests/system"
if str(SYSTEM_TESTS) not in sys.path:
    sys.path.insert(0, str(SYSTEM_TESTS))

from qemu_harness import QemuBlockedError, QemuHarness, QemuHarnessError, framebuffer_has_content

MACHINE_CONFIG = ROOT / "tests/system/qemu-machine.toml"


def _required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise QemuBlockedError(f"required offline machine-test input is missing: {name}")
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


def _surface_is_admitted(profile: dict[str, Any], surface_id: str) -> None:
    runtime = profile.get("session_runtime")
    surfaces = runtime.get("surfaces") if isinstance(runtime, dict) else None
    if not isinstance(surfaces, list):
        raise QemuBlockedError("effective profile has no session_runtime.surfaces projection")
    selected = [
        surface
        for surface in surfaces
        if isinstance(surface, dict) and surface.get("surface_id") == surface_id
    ]
    if len(selected) != 1:
        raise QemuBlockedError(
            f"offline navigation surface {surface_id!r} is not admitted by the effective profile"
        )
    modes = selected[0].get("session_modes")
    if not isinstance(modes, list) or "interactive_user" not in modes:
        raise QemuBlockedError(
            f"offline navigation surface {surface_id!r} is not admitted for interactive_user"
        )


def _navigation_qcodes() -> tuple[str, ...]:
    values = tuple(
        item.strip().lower()
        for item in _required_env("KOA_QEMU_NAVIGATION_KEYS").split(",")
        if item.strip()
    )
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


def _mediatheque_selection() -> str:
    value = _required_env("KOA_QEMU_MEDIATHEQUE_SELECTION").lower()
    if value not in {"selected", "not_selected"}:
        raise QemuBlockedError(
            "KOA_QEMU_MEDIATHEQUE_SELECTION must be 'selected' or 'not_selected'"
        )
    return value


def _active_release_set() -> dict[str, Any]:
    release_set = _json_object(
        _regular_file_from_env("KOA_QEMU_ACTIVE_RELEASE_SET"), "active Release Set"
    )
    if release_set.get("lifecycle_status") != "active":
        raise QemuBlockedError("offline Mediatheque validation requires an active Release Set")
    compatibility = release_set.get("compatibility")
    activation = release_set.get("activation")
    signature = release_set.get("signature")
    if not isinstance(compatibility, dict) or compatibility.get("status") != "tested_compatible":
        raise QemuBlockedError("active Release Set is not tested_compatible")
    if not isinstance(activation, dict) or activation.get("eligibility") != "eligible":
        raise QemuBlockedError("active Release Set is not eligible")
    if not isinstance(signature, dict) or signature.get("verification_status") != "verified":
        raise QemuBlockedError("active Release Set signature is not verified")
    return release_set


def _assert_mediatheque_service_channel(release_set: dict[str, Any], artifact_ref: str) -> None:
    channels = release_set.get("channels")
    services = channels.get("services") if isinstance(channels, dict) else None
    system = channels.get("system") if isinstance(channels, dict) else None
    service_refs = services.get("artifact_refs") if isinstance(services, dict) else None
    system_refs = system.get("artifact_refs") if isinstance(system, dict) else None
    if not isinstance(service_refs, list) or artifact_ref not in service_refs:
        raise QemuBlockedError("selected Mediatheque artifact is absent from the services channel")
    if isinstance(system_refs, list) and artifact_ref in system_refs:
        raise QemuBlockedError(
            "selected Mediatheque artifact is incorrectly present in the system channel"
        )


def _launch_offline():
    image = Path(_required_env("KOA_QEMU_IMAGE")).expanduser()
    image_format = os.environ.get("KOA_QEMU_IMAGE_FORMAT", "raw").strip().lower()
    harness = QemuHarness.from_file(MACHINE_CONFIG)
    return harness.launch(image, network_enabled=False, image_format=image_format)


def _assert_network_is_physically_disabled(argv: tuple[str, ...]) -> None:
    assert "-nic" in argv
    indexes = [index for index, value in enumerate(argv[:-1]) if value == "-nic"]
    assert indexes, "QEMU invocation contains no explicit network configuration"
    assert all(argv[index + 1] == "none" for index in indexes)
    assert not any(value.startswith("user,") for value in argv)


def test_qemu_offline_navigation_forces_network_cut_and_keeps_selected_surface() -> None:
    try:
        profile = _json_object(
            _regular_file_from_env("KOA_QEMU_ACTIVE_PROFILE"), "effective profile"
        )
        surface_id = _required_env("KOA_QEMU_NAVIGATION_SURFACE_ID")
        _surface_is_admitted(profile, surface_id)
        ready_regex = _required_env("KOA_QEMU_NAVIGATION_READY_REGEX")
        result_regex = _required_env("KOA_QEMU_NAVIGATION_RESULT_REGEX")
        qcodes = _navigation_qcodes()
        with _launch_offline() as session:
            _assert_network_is_physically_disabled(session.argv)
            session.wait_for_patterns({"navigation_ready": ready_regex})
            if session.serial_log is None:
                raise QemuHarnessError(
                    "QEMU serial log is unavailable during offline navigation validation"
                )
            before_serial = session.serial_log.read_text(encoding="utf-8", errors="replace")
            if re.search(result_regex, before_serial, re.MULTILINE):
                raise QemuHarnessError(
                    "navigation result marker was already present before offline navigation input"
                )
            _send_navigation(session, qcodes)
            observed = session.wait_for_patterns({"navigation_result": result_regex})
            frame = session.capture_framebuffer("offline-navigation.ppm")
            visible = framebuffer_has_content(frame)
    except QemuBlockedError as exc:
        pytest.fail(f"BLOCKED: {exc}", pytrace=False)
    except (QemuHarnessError, re.error) as exc:
        pytest.fail(str(exc), pytrace=False)

    assert set(observed) == {"navigation_result"}
    assert visible, "offline navigation completed without a visible local surface"


def test_qemu_offline_mediatheque_is_deterministic_without_external_network() -> None:
    try:
        if _mediatheque_selection() == "not_selected":
            pytest.skip("not_applicable: kOA Mediatheque is not selected by the active Release Set")
        release_set = _active_release_set()
        artifact_ref = _required_env("KOA_QEMU_MEDIATHEQUE_ARTIFACT_REF")
        _assert_mediatheque_service_channel(release_set, artifact_ref)
        offline_regex = _required_env("KOA_QEMU_MEDIATHEQUE_OFFLINE_REGEX")
        with _launch_offline() as session:
            _assert_network_is_physically_disabled(session.argv)
            observed = session.wait_for_patterns({"mediatheque_offline": offline_regex})
    except QemuBlockedError as exc:
        pytest.fail(f"BLOCKED: {exc}", pytrace=False)
    except (QemuHarnessError, re.error) as exc:
        pytest.fail(str(exc), pytrace=False)

    assert set(observed) == {"mediatheque_offline"}
