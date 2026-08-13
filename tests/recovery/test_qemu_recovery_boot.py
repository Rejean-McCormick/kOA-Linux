"""Machine-observed recovery boot validation for the kOA appliance."""

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

from qemu_harness import QemuBlockedError, QemuHarness, QemuHarnessError

MACHINE_CONFIG = ROOT / "tests/system/qemu-machine.toml"
RECOVERY_POLICY = ROOT / "host/recovery/recovery-policy.toml"
RECOVERY_SESSION = ROOT / "host/sessions/recovery-session.toml"


def _required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise QemuBlockedError(f"required recovery machine-test input is missing: {name}")
    return value


def _regular_file_from_env(name: str) -> Path:
    path = Path(_required_env(name)).expanduser()
    if not path.is_file() or path.is_symlink():
        raise QemuBlockedError(f"{name} must reference a regular file: {path}")
    return path.resolve()


def _toml(path: Path) -> dict[str, object]:
    with path.open("rb") as stream:
        value = tomllib.load(stream)
    assert isinstance(value, dict)
    return value


def _assert_network_is_physically_disabled(argv: tuple[str, ...]) -> None:
    indexes = [index for index, value in enumerate(argv[:-1]) if value == "-nic"]
    assert indexes, "QEMU invocation contains no explicit network configuration"
    assert all(argv[index + 1] == "none" for index in indexes)
    assert not any(value.startswith("user,") for value in argv)


def test_recovery_contract_is_native_fail_closed_and_offline() -> None:
    policy = _toml(RECOVERY_POLICY)
    containment = policy.get("containment")
    boot_boundary = policy.get("boot_boundary")
    assert isinstance(containment, dict)
    assert isinstance(boot_boundary, dict)
    assert containment.get("network_enabled_by_default") is False
    assert containment.get("allowed_interfaces") == []
    assert containment.get("allowed_containers") == []
    assert boot_boundary.get("source_enter_last_known_good") == "host/boot/enter-last-known-good.py"
    assert boot_boundary.get("source_verify_release_set") == "host/boot/verify-release-set.py"

    session = _toml(RECOVERY_SESSION)
    authority = session.get("authority")
    runtime = session.get("runtime")
    presentation = session.get("presentation")
    assert isinstance(authority, dict)
    assert isinstance(runtime, dict)
    assert isinstance(presentation, dict)
    assert authority.get("direct_privileged_broker_access") is False
    assert authority.get("privileged_effects") == "request_only"
    assert runtime.get("required_surface_roles") == ["compositor", "native_shell"]
    assert runtime.get("optional_surface_roles") == []
    assert presentation.get("route_authority") == "registered_recovery_interfaces_only"


def test_reference_recovery_artifact_boots_without_network_or_web_dependency() -> None:
    try:
        image = _regular_file_from_env("KOA_QEMU_RECOVERY_IMAGE")
        expected_release = _required_env("KOA_QEMU_RECOVERY_RELEASE_IDENTITY")
        recovery_mode_regex = _required_env("KOA_QEMU_RECOVERY_MODE_REGEX")
        recovery_ready_regex = _required_env("KOA_QEMU_RECOVERY_READY_REGEX")
        image_format = os.environ.get(
            "KOA_QEMU_RECOVERY_IMAGE_FORMAT",
            os.environ.get("KOA_QEMU_IMAGE_FORMAT", "raw"),
        ).strip().lower()

        harness = QemuHarness.from_file(MACHINE_CONFIG)
        with harness.launch(image, network_enabled=False, image_format=image_format) as session:
            _assert_network_is_physically_disabled(session.argv)
            observed = session.wait_for_patterns(
                {
                    "systemd": r"(?i)(?:systemd\[1\]:|Welcome to .*Linux)",
                    "release_identity": re.escape(expected_release),
                    "recovery_mode": recovery_mode_regex,
                    "recovery_ready": recovery_ready_regex,
                }
            )
    except QemuBlockedError as exc:
        pytest.fail(f"BLOCKED: {exc}", pytrace=False)
    except (QemuHarnessError, re.error) as exc:
        pytest.fail(str(exc), pytrace=False)

    assert set(observed) == {
        "systemd",
        "release_identity",
        "recovery_mode",
        "recovery_ready",
    }
