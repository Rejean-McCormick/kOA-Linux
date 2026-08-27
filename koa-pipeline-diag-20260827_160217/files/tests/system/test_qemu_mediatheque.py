from __future__ import annotations

import json
import os
from pathlib import Path
import re
import sys
import tomllib
from typing import Any

import pytest

SYSTEM_TESTS = Path(__file__).resolve().parent
if str(SYSTEM_TESTS) not in sys.path:
    sys.path.insert(0, str(SYSTEM_TESTS))

from qemu_harness import QemuBlockedError, QemuHarness, QemuHarnessError

ROOT = Path(__file__).resolve().parents[2]
MACHINE_CONFIG = ROOT / "tests/system/qemu-machine.toml"
MEDIATHEQUE_PACKAGE = ROOT / "packaging/components/koa-mediatheque.toml"
SYSTEM_IMAGE_PACKAGE = ROOT / "packaging/system/image.toml"


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


def _selection() -> str:
    value = _required_env("KOA_QEMU_MEDIATHEQUE_SELECTION").lower()
    if value not in {"selected", "not_selected"}:
        raise QemuBlockedError(
            "KOA_QEMU_MEDIATHEQUE_SELECTION must be 'selected' or 'not_selected'"
        )
    return value


def _network_enabled() -> bool:
    value = os.environ.get("KOA_QEMU_NETWORK", "off").strip().lower()
    if value not in {"on", "off"}:
        raise QemuBlockedError("KOA_QEMU_NETWORK must be 'on' or 'off'")
    return value == "on"


def _active_release_set() -> dict[str, Any]:
    release_set = _json_object(
        _regular_file_from_env("KOA_QEMU_ACTIVE_RELEASE_SET"), "active Release Set"
    )
    if release_set.get("lifecycle_status") != "active":
        raise QemuBlockedError("Mediatheque validation requires an active Release Set")
    compatibility = release_set.get("compatibility")
    activation = release_set.get("activation")
    signature = release_set.get("signature")
    if not isinstance(compatibility, dict) or compatibility.get("status") != "tested_compatible":
        raise QemuBlockedError("active Release Set is not tested_compatible")
    if not isinstance(activation, dict) or activation.get("eligibility") != "eligible":
        raise QemuBlockedError("active Release Set is not eligible for activation")
    if not isinstance(signature, dict) or signature.get("verification_status") != "verified":
        raise QemuBlockedError("active Release Set signature is not verified")
    return release_set


def _assert_mediatheque_service_channel(release_set: dict[str, Any], artifact_ref: str) -> None:
    channels = release_set.get("channels")
    if not isinstance(channels, dict):
        raise QemuBlockedError("active Release Set has no channels object")
    services = channels.get("services")
    system = channels.get("system")
    if not isinstance(services, dict) or not isinstance(system, dict):
        raise QemuBlockedError("active Release Set must declare system and services channels")
    service_refs = services.get("artifact_refs")
    system_refs = system.get("artifact_refs")
    if not isinstance(service_refs, list) or artifact_ref not in service_refs:
        raise QemuBlockedError("selected Mediatheque artifact is absent from the services channel")
    if isinstance(system_refs, list) and artifact_ref in system_refs:
        raise QemuBlockedError(
            "selected Mediatheque artifact is incorrectly present in the system channel"
        )


def test_mediatheque_package_remains_a_service_payload() -> None:
    with MEDIATHEQUE_PACKAGE.open("rb") as stream:
        package = tomllib.load(stream)
    with SYSTEM_IMAGE_PACKAGE.open("rb") as stream:
        system_image = tomllib.load(stream)

    assert package["component_id"] == "koa_mediatheque"
    assert package["release_channel"] == "services"
    assert package["admission"]["requires_release_set"] is True
    assert package["configuration"]["activation"] == "effective_profile_and_release_set_only"
    assert system_image["release_channel"] == "system"
    assert system_image["payload_selection"]["component_service_payloads_embedded"] is False
    assert (
        "packaging/components/koa-mediatheque.toml#configuration"
        in system_image["configuration_seeds"]["source_manifests"]
    )


def test_reference_image_uses_mediatheque_only_when_selected_by_release_set() -> None:
    try:
        selection = _selection()
        if selection == "not_selected":
            pytest.skip("not_applicable: kOA Mediatheque is not selected by the active Release Set")
        release_set = _active_release_set()
        artifact_ref = _required_env("KOA_QEMU_MEDIATHEQUE_ARTIFACT_REF")
        _assert_mediatheque_service_channel(release_set, artifact_ref)
        ready_regex = _required_env("KOA_QEMU_MEDIATHEQUE_READY_REGEX")
        image = Path(_required_env("KOA_QEMU_IMAGE")).expanduser()
        image_format = os.environ.get("KOA_QEMU_IMAGE_FORMAT", "raw").strip().lower()
        harness = QemuHarness.from_file(MACHINE_CONFIG)
        with harness.launch(
            image, network_enabled=_network_enabled(), image_format=image_format
        ) as session:
            observed = session.wait_for_patterns({"mediatheque_ready": ready_regex})
    except QemuBlockedError as exc:
        pytest.fail(f"BLOCKED: {exc}", pytrace=False)
    except (QemuHarnessError, re.error) as exc:
        pytest.fail(str(exc), pytrace=False)

    assert set(observed) == {"mediatheque_ready"}
