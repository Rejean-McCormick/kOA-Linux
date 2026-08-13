"""Machine-observed failed-candidate and explicit previous-good validation."""

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
BOOT_POLICY = ROOT / "host/boot/boot-policy.toml"


def _required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise QemuBlockedError(f"required rollback machine-test input is missing: {name}")
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


def _serial_text(session) -> str:
    if session.serial_log is None:
        raise QemuHarnessError("QEMU serial log is unavailable during rollback validation")
    return session.serial_log.read_text(encoding="utf-8", errors="replace")


def _first_match(text: str, pattern: str, label: str) -> re.Match[str]:
    match = re.search(pattern, text, re.MULTILINE)
    if match is None:
        raise QemuHarnessError(f"missing rollback observation after QEMU completion: {label}")
    return match


def test_boot_policy_requires_explicit_lkg_and_separates_acceptance() -> None:
    with BOOT_POLICY.open("rb") as stream:
        policy = tomllib.load(stream)

    assert policy["automatic_fallback"] is False
    assert policy["activation_and_acceptance_are_separate"] is True
    assert policy["require_atomic_state_updates"] is True
    assert policy["require_health_verdict_for_acceptance"] is True
    assert policy["failure_mode"] == "retain_active_and_require_explicit_lkg_or_recovery"
    assert set(policy["slots"]["required_distinct_roles"]) == {
        "active",
        "candidate",
        "previous_good",
        "recovery",
    }
    assert policy["retention"]["retain_failed_candidate_evidence"] is True
    assert policy["retention"]["retain_previous_good"] is True


def test_failed_candidate_is_rejected_before_explicit_previous_good_becomes_ready() -> None:
    try:
        image = _regular_file_from_env("KOA_QEMU_FAILED_CANDIDATE_IMAGE")
        candidate_identity = _required_env("KOA_QEMU_FAILED_CANDIDATE_IDENTITY")
        previous_good_identity = _required_env("KOA_QEMU_PREVIOUS_GOOD_IDENTITY")
        rejected_regex = _required_env("KOA_QEMU_CANDIDATE_REJECTED_REGEX")
        lkg_selected_regex = _required_env("KOA_QEMU_LKG_SELECTED_REGEX")
        lkg_ready_regex = _required_env("KOA_QEMU_LKG_READY_REGEX")
        image_format = os.environ.get("KOA_QEMU_IMAGE_FORMAT", "raw").strip().lower()

        harness = QemuHarness.from_file(MACHINE_CONFIG)
        with harness.launch(
            image,
            network_enabled=_network_enabled(),
            image_format=image_format,
        ) as session:
            observed = session.wait_for_patterns(
                {
                    "candidate_identity": re.escape(candidate_identity),
                    "candidate_rejected": rejected_regex,
                    "lkg_selected": lkg_selected_regex,
                    "previous_good_identity": re.escape(previous_good_identity),
                    "lkg_ready": lkg_ready_regex,
                }
            )
            serial = _serial_text(session)

        candidate_match = _first_match(serial, re.escape(candidate_identity), "candidate identity")
        rejected_match = _first_match(serial, rejected_regex, "candidate rejection")
        selected_match = _first_match(serial, lkg_selected_regex, "explicit previous_good selection")
        previous_good_match = _first_match(
            serial, re.escape(previous_good_identity), "previous_good identity"
        )
        ready_match = _first_match(serial, lkg_ready_regex, "previous_good readiness")
    except QemuBlockedError as exc:
        pytest.fail(f"BLOCKED: {exc}", pytrace=False)
    except (QemuHarnessError, re.error) as exc:
        pytest.fail(str(exc), pytrace=False)

    assert set(observed) == {
        "candidate_identity",
        "candidate_rejected",
        "lkg_selected",
        "previous_good_identity",
        "lkg_ready",
    }
    assert candidate_match.start() <= rejected_match.start()
    assert rejected_match.start() < selected_match.start()
    assert selected_match.start() <= previous_good_match.start()
    assert previous_good_match.start() <= ready_match.start()
