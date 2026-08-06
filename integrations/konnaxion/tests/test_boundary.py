from __future__ import annotations

import ast
from datetime import UTC, datetime
from pathlib import Path

import pytest

from koa_konnaxion_adapter.capabilities import CapabilityState
from koa_konnaxion_adapter.notifications import NotificationEnvelope
from koa_konnaxion_adapter.routes import AuthorityContext
from koa_konnaxion_adapter.surface_bridge import SurfaceBridge


PACKAGE = Path(__file__).parents[1] / "adapter" / "src" / "koa_konnaxion_adapter"


def test_no_private_component_or_subsystem_imports():
    forbidden_prefixes = ("components.", "koa_identity", "koa_audit", "koa_resource", "koa_governance", "koa_publication")
    for path in sorted(PACKAGE.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            else:
                continue
            assert not any(name.startswith(forbidden_prefixes) for name in names), (path, names)


def test_adapter_has_no_direct_storage_or_process_escape():
    prohibited = ("sqlite3", "subprocess", "os.system", "Path.write_", "open(", "socket.")
    for path in sorted(PACKAGE.glob("*.py")):
        text = path.read_text(encoding="utf-8")
        hits = [marker for marker in prohibited if marker in text]
        assert not hits, (path, hits)


def test_route_resolution_does_not_transfer_authority(runtime):
    capability = runtime.capabilities.snapshot_for("boundary.routes.read", runtime.observations)
    assert capability.state is CapabilityState.AVAILABLE
    resolution = runtime.routes.resolve(
        "/participation",
        authority=AuthorityContext("identity:user:1", "tenant:local:1", True, True),
        capability=capability,
    )
    assert resolution.presentation_only is True
    assert resolution.authoritative is False
    assert resolution.transfers_authority is False


def test_notification_projection_is_bounded_and_non_authoritative(runtime):
    capability = runtime.capabilities.snapshot_for("boundary.notifications.read", runtime.observations)
    projection = runtime.notifications.project(
        NotificationEnvelope(
            notification_ref="notification:konnaxion:1",
            kind="civic.notice",
            title="Participation update",
            summary="A declared Konnaxion notification is available.",
            occurred_at=datetime(2026, 8, 6, tzinfo=UTC),
            provenance_ref="provenance:konnaxion:1",
            action_route_alias="/participation",
        ),
        capability=capability,
    )
    assert projection.presentation_only is True
    assert projection.authoritative is False
    assert projection.transfers_authority is False


def test_surface_bridge_rejects_internal_catalog_duplication(manifests):
    bad = dict(manifests)
    bad["widgets"] = {"internal_workflow": ["do-not-duplicate"]}
    with pytest.raises(ValueError, match="internal catalog"):
        SurfaceBridge(bad, alignment_state="prepared_only")
