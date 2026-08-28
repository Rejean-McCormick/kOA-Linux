"""Determinism at the profile-plan boundary."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import json
import sys

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "assembly" / "src"))

from koa_assembly.renderers import normalize_plan, plan_digest  # noqa: E402

_SHA = "sha256:" + "c" * 64


def _profile_derived_plan() -> dict:
    profile = json.loads(
        (REPO / "docs/contracts/profiles/sovereign-offline.profile.json").read_text(encoding="utf-8")
    )
    service_ids = [item.replace("_", "-") for item in profile["offline_operation"]["required_local_services"]]
    services = [
        {
            "id": service_id,
            "kind": "native",
            "command": [f"/usr/libexec/koa/{service_id}"],
            "dependencies": [],
            "environment": {},
            "ports": [],
            "mounts": [],
            "networks": [],
            "resources": {},
            "capabilities": [],
            "user": service_id,
            "criticality": "critical",
        }
        for service_id in service_ids
    ]
    return {
        "plan_id": "sovereign-offline-profile-plan",
        "profile_id": profile["profile_id"],
        "source_digests": {
            "docs/contracts/profiles/sovereign-offline.profile.json": _SHA
        },
        "services": services,
        "networks": [],
        "volumes": [],
        "packages": [],
        "files": [],
        "offline": {"enabled": True, "allow_network": False, "artifacts": []},
        "backup": {},
    }


def test_public_profile_plan_normalization_is_order_independent() -> None:
    first = _profile_derived_plan()
    second = deepcopy(first)
    second["services"].reverse()
    assert normalize_plan(first) == normalize_plan(second)
    assert plan_digest(normalize_plan(first)) == plan_digest(normalize_plan(second))


def test_profile_source_change_changes_plan_digest() -> None:
    first = normalize_plan(_profile_derived_plan())
    changed_plan = _profile_derived_plan()
    changed_plan["source_digests"]["docs/contracts/profiles/sovereign-offline.profile.json"] = "sha256:" + "d" * 64
    changed = normalize_plan(changed_plan)
    assert plan_digest(first) != plan_digest(changed)


def test_real_plan_builder_dependency_gate() -> None:
    expected = [
        REPO / "assembly/src/koa_assembly/plans/dependency_graph.py",
        REPO / "assembly/src/koa_assembly/plans/service_plan.py",
        REPO / "assembly/src/koa_assembly/plans/resource_plan.py",
        REPO / "assembly/src/koa_assembly/plans/storage_plan.py",
        REPO / "assembly/src/koa_assembly/plans/network_plan.py",
        REPO / "assembly/src/koa_assembly/plans/backup_plan.py",
    ]
    missing = [path.relative_to(REPO).as_posix() for path in expected if not path.is_file()]
    if missing:
        pytest.skip("B-0092 absent: " + ", ".join(missing))
    assert all(path.stat().st_size > 0 for path in expected)
