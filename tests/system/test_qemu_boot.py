from __future__ import annotations

import os
from pathlib import Path
import re
import sys

import pytest

SYSTEM_TESTS = Path(__file__).resolve().parent
if str(SYSTEM_TESTS) not in sys.path:
    sys.path.insert(0, str(SYSTEM_TESTS))

from qemu_harness import MachineConfig, QemuBlockedError, QemuHarness, QemuHarnessError

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


def test_reference_machine_configuration_is_validation_only() -> None:
    document = MACHINE_CONFIG.read_text(encoding="utf-8")
    config = MachineConfig.load(MACHINE_CONFIG)

    assert 'scope = "reference_validation_platform"' in document
    assert "profile" not in {line.split("=", 1)[0].strip() for line in document.splitlines() if "=" in line}
    assert config.timeout_seconds >= config.shutdown_timeout_seconds
    assert config.max_serial_log_bytes <= 8 * 1024 * 1024
    assert config.max_qemu_log_bytes <= 1024 * 1024



def test_machine_configuration_rejects_product_scope(tmp_path: Path) -> None:
    invalid = tmp_path / "qemu-machine.toml"
    invalid.write_text(
        MACHINE_CONFIG.read_text(encoding="utf-8").replace(
            'scope = "reference_validation_platform"',
            'scope = "sovereign_linux_node"',
        ),
        encoding="utf-8",
    )

    with pytest.raises(QemuHarnessError, match="reference validation platform"):
        MachineConfig.load(invalid)

def test_network_toggle_changes_only_qemu_network_arguments() -> None:
    config = MachineConfig.load(MACHINE_CONFIG)

    assert config.network_argv(False) == ("-nic", "none")
    assert config.network_argv(True) == ("-nic", f"user,model={config.network_model}")


def test_reference_image_boot_observes_required_runtime_milestones() -> None:
    try:
        image = Path(_required_env("KOA_QEMU_IMAGE")).expanduser()
        expected_release = _required_env("KOA_QEMU_EXPECTED_RELEASE_IDENTITY")
        image_format = os.environ.get("KOA_QEMU_IMAGE_FORMAT", "raw").strip().lower()
        harness = QemuHarness.from_file(MACHINE_CONFIG)
        with harness.launch(image, network_enabled=_network_enabled(), image_format=image_format) as session:
            assert "-kernel" not in session.argv, "direct kernel boot would bypass the required UEFI boot path"
            assert any("if=pflash" in item and "readonly=on" in item for item in session.argv)
            assert any("if=pflash" in item and "readonly=on" not in item for item in session.argv)
            observed = session.wait_for_patterns(
                {
                    "kernel": r"Linux version\s+[^\r\n]+",
                    "initramfs": r"(?i)(?:Trying to unpack rootfs image as initramfs|Unpacking initramfs|Freeing initrd memory|initramfs)",
                    "systemd": r"(?i)(?:systemd\[1\]:|Welcome to .*Linux)",
                    "release_identity": re.escape(expected_release),
                    "critical_target": r"(?i)Reached target .*kOA critical authority services",
                }
            )
    except QemuBlockedError as exc:
        pytest.fail(f"BLOCKED: {exc}", pytrace=False)
    except QemuHarnessError as exc:
        pytest.fail(str(exc), pytrace=False)

    assert set(observed) == {"kernel", "initramfs", "systemd", "release_identity", "critical_target"}
