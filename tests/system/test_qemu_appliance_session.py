from __future__ import annotations

import os
from pathlib import Path
import re
import sys

import pytest

SYSTEM_TESTS = Path(__file__).resolve().parent
if str(SYSTEM_TESTS) not in sys.path:
    sys.path.insert(0, str(SYSTEM_TESTS))

from qemu_harness import QemuBlockedError, QemuHarness, QemuHarnessError, framebuffer_has_content

ROOT = Path(__file__).resolve().parents[2]
MACHINE_CONFIG = ROOT / "tests/system/qemu-machine.toml"


def _required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise QemuBlockedError(f"required machine-test input is missing: {name}")
    return value


def _network_enabled() -> bool:
    value = os.environ.get("KOA_QEMU_NETWORK", "off").strip().lower()
    if value not in {"on", "off"}:
        raise QemuBlockedError("KOA_QEMU_NETWORK must be 'on' or 'off'")
    return value == "on"


def test_qemu_framebuffer_rejects_blank_surface(tmp_path: Path) -> None:
    frame = tmp_path / "blank.ppm"
    frame.write_bytes(b"P6\n2 2\n255\n" + (b"\x00\x00\x00" * 4))

    assert framebuffer_has_content(frame, minimum_distinct_colors=2) is False



def test_qemu_framebuffer_accepts_visible_variation(tmp_path: Path) -> None:
    frame = tmp_path / "visible.ppm"
    frame.write_bytes(
        b"P6\n2 2\n255\n"
        + b"\x00\x00\x00"
        + b"\xff\x00\x00"
        + b"\x00\xff\x00"
        + b"\x00\x00\xff"
    )

    assert framebuffer_has_content(frame, minimum_distinct_colors=3) is True

def test_reference_image_observes_actual_appliance_session() -> None:
    try:
        image = Path(_required_env("KOA_QEMU_IMAGE")).expanduser()
        expected_release = _required_env("KOA_QEMU_EXPECTED_RELEASE_IDENTITY")
        compositor_ready = _required_env("KOA_QEMU_COMPOSITOR_READY_REGEX")
        session_ready = _required_env("KOA_QEMU_SESSION_READY_REGEX")
        image_format = os.environ.get("KOA_QEMU_IMAGE_FORMAT", "raw").strip().lower()
        harness = QemuHarness.from_file(MACHINE_CONFIG)
        with harness.launch(image, network_enabled=_network_enabled(), image_format=image_format) as session:
            observed = session.wait_for_patterns(
                {
                    "systemd": r"(?i)(?:systemd\[1\]:|Welcome to .*Linux)",
                    "release_identity": re.escape(expected_release),
                    "critical_target": r"(?i)Reached target .*kOA critical authority services",
                    "compositor": compositor_ready,
                    "appliance_session": session_ready,
                }
            )
            framebuffer = session.capture_framebuffer()
            visible = framebuffer_has_content(framebuffer)
    except QemuBlockedError as exc:
        pytest.fail(f"BLOCKED: {exc}", pytrace=False)
    except (QemuHarnessError, re.error) as exc:
        pytest.fail(str(exc), pytrace=False)

    assert set(observed) == {"systemd", "release_identity", "critical_target", "compositor", "appliance_session"}
    assert visible, "the runtime reported the appliance session but the observed framebuffer remained blank"
