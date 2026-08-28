"""Determinism at the already-resolved deployment-plan boundary."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "assembly" / "src"))

from koa_assembly.renderers import normalize_plan, plan_digest  # noqa: E402

_SHA = "sha256:" + "c" * 64


def _resolved_plan_fixture() -> dict:
    """Return explicit test data; this fixture is not derived from a profile authority."""

    return {
        "plan_id": "sovereign-offline-fixture-plan",
        "profile_id": "sovereign_offline",
        "source_digests": {
            "tests/reproducibility/resolved-plan-fixture": _SHA,
        },
        "services": [
            {
                "id": "fixture-a",
                "kind": "native",
                "command": ["/usr/bin/true"],
                "dependencies": [],
                "environment": {},
                "ports": [],
                "mounts": [],
                "networks": [],
                "resources": {},
                "capabilities": [],
                "user": "nobody",
                "criticality": "critical",
            },
            {
                "id": "fixture-b",
                "kind": "native",
                "command": ["/usr/bin/true"],
                "dependencies": ["fixture-a"],
                "environment": {},
                "ports": [],
                "mounts": [],
                "networks": [],
                "resources": {},
                "capabilities": [],
                "user": "nobody",
                "criticality": "important",
            },
        ],
        "networks": [],
        "volumes": [],
        "packages": [],
        "files": [],
        "offline": {
            "enabled": True,
            "allow_network": False,
            "verification_policy": "verify-before-use",
            "artifacts": [],
        },
        "backup": {},
    }


def test_resolved_plan_normalization_is_order_independent() -> None:
    first = _resolved_plan_fixture()
    second = deepcopy(first)
    second["services"].reverse()
    assert normalize_plan(first) == normalize_plan(second)
    assert plan_digest(normalize_plan(first)) == plan_digest(normalize_plan(second))


def test_resolved_plan_source_change_changes_plan_digest() -> None:
    first = normalize_plan(_resolved_plan_fixture())
    changed_plan = _resolved_plan_fixture()
    changed_plan["source_digests"]["tests/reproducibility/resolved-plan-fixture"] = "sha256:" + "d" * 64
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
        pytest.skip("resolved-plan builder dependencies absent: " + ", ".join(missing))
    assert all(path.stat().st_size > 0 for path in expected)
