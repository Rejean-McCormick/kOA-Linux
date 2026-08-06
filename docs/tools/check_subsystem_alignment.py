#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import stat
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_SUBSYSTEMS = {
    "ariane": "ariane",
    "konnaxion": "konnaxion",
    "orgo": "orgo",
    "sentient": "sentient",
    "semantik_architect": "semantik-architect",
    "koa_spaces": "koa-spaces",
}

FORBIDDEN_SUBSYSTEM_IDS = {"uckk"}
FORBIDDEN_MOUNT_SLUGS = {"uckk"}


def is_link_or_junction(path: Path) -> bool:
    if path.is_symlink():
        return True
    try:
        attrs = path.stat(follow_symlinks=False).st_file_attributes
    except (AttributeError, OSError):
        return False
    return bool(attrs & stat.FILE_ATTRIBUTE_REPARSE_POINT)


def load_json(path: Path, failures: list[str]) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        failures.append(f"{path}: {exc}")
        return None
    if not isinstance(value, dict):
        failures.append(f"{path}: top-level value must be an object")
        return None
    return value


def check_forbidden_uckk_artifacts(failures: list[str]) -> None:
    forbidden_contract = ROOT / "contracts" / "subsystems" / "uckk.subsystem.json"
    if forbidden_contract.exists():
        failures.append(
            f"{forbidden_contract}: UCKK is an external Moodle platform; use an integration contract, not a subsystem contract"
        )

    for slug in sorted(FORBIDDEN_MOUNT_SLUGS):
        mount = ROOT / "subsystems" / slug
        shortcut = mount.with_suffix(".lnk")
        if mount.exists() or mount.is_symlink():
            failures.append(
                f"{mount}: UCKK is external and must not be mounted as active subsystem documentation"
            )
        if shortcut.exists():
            failures.append(
                f"{shortcut}: UCKK is external and must not be represented by a subsystem shortcut"
            )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate independently owned subsystem contracts and documentation mounts."
    )
    parser.add_argument(
        "--require-mounted",
        action="store_true",
        help="Fail when one of the six reserved subsystem documentation mounts is absent.",
    )
    args = parser.parse_args(argv)

    failures: list[str] = []
    warnings: list[str] = []
    seen: set[str] = set()

    contracts_dir = ROOT / "contracts" / "subsystems"
    for path in sorted(contracts_dir.glob("*.subsystem.json")):
        document = load_json(path, failures)
        if document is None:
            continue

        subsystem_id = document.get("subsystem_id")
        if not isinstance(subsystem_id, str) or not subsystem_id:
            failures.append(f"{path}: subsystem_id missing")
            continue

        if subsystem_id in FORBIDDEN_SUBSYSTEM_IDS:
            failures.append(
                f"{path}: {subsystem_id!r} is an external platform and is prohibited as a subsystem identity"
            )
            continue

        slug = REQUIRED_SUBSYSTEMS.get(subsystem_id)
        if slug is None:
            failures.append(f"{path}: undeclared subsystem_id {subsystem_id!r}")
            continue

        if subsystem_id in seen:
            failures.append(f"{path}: duplicate subsystem_id {subsystem_id!r}")
            continue
        seen.add(subsystem_id)

        expected_mount = f"subsystems/{slug}"
        actual_mount = document.get("official_documentation", {}).get("mount_path")
        if actual_mount != expected_mount:
            failures.append(f"{path}: mount_path must be {expected_mount!r}")

        rules = document.get("boundary_rules", {})
        if rules.get("direct_cross_subsystem_writes") != "prohibited":
            failures.append(f"{path}: cross-write prohibition missing")
        if rules.get("internal_behavior_duplication") != "prohibited":
            failures.append(f"{path}: duplication prohibition missing")

        if subsystem_id == "koa_spaces":
            if document.get("optional") is not True:
                failures.append(f"{path}: kOA Spaces must remain optional")
            if document.get("replaceable") is not True:
                failures.append(f"{path}: kOA Spaces must remain replaceable")
            if document.get("authority") != "non_authoritative_presentation":
                failures.append(f"{path}: kOA Spaces authority must be non_authoritative_presentation")
            if rules.get("presentation_grants_authority") is not False:
                failures.append(f"{path}: presentation_grants_authority must be false")
            if rules.get("menu_visibility_is_authorization") is not False:
                failures.append(f"{path}: menu_visibility_is_authorization must be false")
            if rules.get("replacement_preserves_business_state") is not True:
                failures.append(f"{path}: replacement_preserves_business_state must be true")

    missing = sorted(set(REQUIRED_SUBSYSTEMS) - seen)
    if missing:
        failures.append("missing subsystem contracts: " + ", ".join(missing))

    for subsystem_id, slug in REQUIRED_SUBSYSTEMS.items():
        expected = ROOT / "subsystems" / slug
        shortcut = expected.with_suffix(".lnk")

        if shortcut.exists():
            failures.append(f"{shortcut}: .lnk unsupported; use junction or symlink")
            continue

        if not expected.exists():
            message = f"{expected}: reserved path is not mounted"
            (failures if args.require_mounted else warnings).append(message)
            continue

        if not expected.is_dir():
            failures.append(f"{expected}: mount is not a directory")
            continue

        # A normal directory is accepted for portable test fixtures. Production
        # installations should use a junction or symbolic link to the official docs.
        _ = is_link_or_junction(expected)

    check_forbidden_uckk_artifacts(failures)

    for item in warnings:
        print("WARN:", item)
    for item in failures:
        print("FAIL:", item)

    print("check_subsystem_alignment:", "fail" if failures else "pass")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
