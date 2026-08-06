from __future__ import annotations

from datetime import UTC, datetime

from koa_konnaxion_adapter.health import HealthState


def test_prepared_only_health_is_not_ready(prepared_runtime):
    report = prepared_runtime.health(observed_at=datetime(2026, 8, 6, tzinfo=UTC))
    assert report.healthy is True
    assert report.ready is False
    assert report.state is HealthState.BLOCKED
    assert "official_subsystem_alignment_not_verified" in report.reasons
    assert report.as_dict()["authority_effect"] == "none"


def test_surface_snapshot_is_presentation_only(prepared_runtime):
    snapshot = prepared_runtime.surfaces.snapshot()
    assert snapshot.alignment_state == "prepared_only"
    assert snapshot.presentation_only is True
    assert snapshot.authoritative is False
    assert snapshot.transfers_authority is False
    assert set(snapshot.manifests) == {"module-interface", "sidebar", "widgets"}
