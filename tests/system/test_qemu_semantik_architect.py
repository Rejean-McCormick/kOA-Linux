from __future__ import annotations

import json
import os
from pathlib import Path
import re
import sys
from typing import Any

import pytest

SYSTEM_TESTS = Path(__file__).resolve().parent
if str(SYSTEM_TESTS) not in sys.path:
    sys.path.insert(0, str(SYSTEM_TESTS))

from qemu_harness import QemuBlockedError, QemuHarness, QemuHarnessError

ROOT = Path(__file__).resolve().parents[2]
MACHINE_CONFIG = ROOT / "tests/system/qemu-machine.toml"
SOURCE_LOCK = ROOT / "integrations/semantik-architect/source.lock.json"
COMPATIBILITY = ROOT / "integrations/semantik-architect/compatibility.json"


def _required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise QemuBlockedError(f"required machine-test input is missing: {name}")
    return value


def _json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise QemuBlockedError(f"{label} is not readable JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise QemuBlockedError(f"{label} must be a JSON object")
    return value


def _regular_file_from_env(name: str) -> Path:
    path = Path(_required_env(name)).expanduser()
    if not path.is_file() or path.is_symlink():
        raise QemuBlockedError(f"{name} must reference a regular file: {path}")
    return path.resolve()


def _selection() -> str:
    value = _required_env("KOA_QEMU_SEMANTIK_SELECTION").lower()
    if value not in {"selected", "not_selected"}:
        raise QemuBlockedError("KOA_QEMU_SEMANTIK_SELECTION must be 'selected' or 'not_selected'")
    return value


def _network_enabled() -> bool:
    value = os.environ.get("KOA_QEMU_NETWORK", "off").strip().lower()
    if value not in {"on", "off"}:
        raise QemuBlockedError("KOA_QEMU_NETWORK must be 'on' or 'off'")
    return value == "on"


def _assert_semantik_admitted(active_profile: dict[str, Any]) -> None:
    lock = _json_object(SOURCE_LOCK, "SemantiK Architect source lock")
    compatibility = _json_object(COMPATIBILITY, "SemantiK Architect compatibility manifest")
    source = lock.get("source")
    license_record = lock.get("license")
    documentation = lock.get("documentation")
    if lock.get("admission_enabled") is not True or lock.get("status") not in {
        "admitted",
        "resolved",
    }:
        raise QemuBlockedError(f"SemantiK Architect source is not admitted: {lock.get('status')}")
    if not isinstance(source, dict) or any(
        not source.get(key) for key in ("repository", "commit", "source_sha256")
    ):
        raise QemuBlockedError("SemantiK Architect authoritative source metadata is incomplete")
    if not isinstance(license_record, dict) or not license_record.get("metadata_verified"):
        raise QemuBlockedError("SemantiK Architect license metadata is not verified")
    if not isinstance(documentation, dict) or not documentation.get("mounted_in_supplied_corpus"):
        raise QemuBlockedError("SemantiK Architect official documentation is not mounted")
    final_alignment = compatibility.get("final_alignment")
    if not isinstance(final_alignment, dict) or final_alignment.get("status") not in {
        "pass",
        "compatible",
        "admitted",
    }:
        raise QemuBlockedError("SemantiK Architect compatibility is not admitted")

    primary = active_profile.get("primary_profile")
    profile_id = primary.get("profile_id") if isinstance(primary, dict) else None
    applicability = compatibility.get("profile_applicability")
    supported = applicability.get("supported") if isinstance(applicability, dict) else None
    overlays = active_profile.get("overlays")
    explicit_overlay = isinstance(overlays, list) and any(
        isinstance(item, dict) and item.get("profile_id") == "semantik_architect"
        for item in overlays
    )
    if isinstance(supported, list) and profile_id not in supported and not explicit_overlay:
        raise QemuBlockedError(f"SemantiK Architect is not admitted by profile {profile_id!r}")


def test_semantik_unadmitted_source_is_fail_closed() -> None:
    lock = _json_object(SOURCE_LOCK, "SemantiK Architect source lock")
    compatibility = _json_object(COMPATIBILITY, "SemantiK Architect compatibility manifest")

    if lock.get("admission_enabled") is False:
        assert lock["pin_policy"]["unresolved_result"] == "blocked"
        assert (
            compatibility["subsystem_source_compatibility"][
                "default_for_unpinned_or_unversioned_source"
            ]
            == "rejected"
        )
        assert compatibility["final_alignment"]["status"] == "blocked"
    else:
        assert lock.get("status") in {"admitted", "resolved"}


def test_reference_image_runs_semantik_only_for_admitted_external_artifact() -> None:
    try:
        selection = _selection()
        if selection == "not_selected":
            pytest.skip(
                "not_applicable: SemantiK Architect is not selected by the effective profile"
            )
        active_profile = _json_object(
            _regular_file_from_env("KOA_QEMU_ACTIVE_PROFILE"), "effective profile"
        )
        _assert_semantik_admitted(active_profile)
        runtime_regex = _required_env("KOA_QEMU_SEMANTIK_READY_REGEX")
        image = Path(_required_env("KOA_QEMU_IMAGE")).expanduser()
        image_format = os.environ.get("KOA_QEMU_IMAGE_FORMAT", "raw").strip().lower()
        harness = QemuHarness.from_file(MACHINE_CONFIG)
        with harness.launch(
            image, network_enabled=_network_enabled(), image_format=image_format
        ) as session:
            observed = session.wait_for_patterns({"semantik_ready": runtime_regex})
    except QemuBlockedError as exc:
        pytest.fail(f"BLOCKED: {exc}", pytrace=False)
    except (QemuHarnessError, re.error) as exc:
        pytest.fail(str(exc), pytrace=False)

    assert set(observed) == {"semantik_ready"}
