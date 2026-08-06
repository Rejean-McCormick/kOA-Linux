from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "operations/src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from koa_operations.diagnostics.health import (  # noqa: E402
    CollectorDescriptor,
    DiagnosticDataClass,
    HealthObservation,
    HealthState,
    summarize_health,
)

NOW = datetime(2026, 8, 6, 16, 0, tzinfo=timezone.utc)


def _collector(component_id: str) -> CollectorDescriptor:
    return CollectorDescriptor(
        collector_id=f"{component_id}.health.v1",
        component_id=component_id,
        version="1.0.0",
        supported_fields=("status", "reason_code"),
        data_classes=(DiagnosticDataClass.PUBLIC_OPERATIONAL,),
        max_records=8,
        max_age_seconds=60,
        redaction_profile="health.public.v1",
    )


def test_aggregate_health_preserves_worst_declared_state() -> None:
    descriptors = (_collector("audit-broker"), _collector("identity-and-trust"))
    observations = (
        HealthObservation(
            component_id="audit-broker",
            observed_at=NOW,
            state=HealthState.HEALTHY,
            release_ref="release-set:active",
        ),
        HealthObservation(
            component_id="identity-and-trust",
            observed_at=NOW,
            state=HealthState.DEGRADED,
            reason_codes=("trust_store_degraded",),
            release_ref="release-set:active",
        ),
    )
    result = summarize_health(descriptors, observations, now=NOW)
    assert result.state is HealthState.DEGRADED
    assert result.authoritative is False
    assert tuple(item.component_id for item in result.components) == (
        "audit-broker",
        "identity-and-trust",
    )
    assert "trust_store_degraded" in result.reason_codes


def test_stale_or_missing_health_never_becomes_healthy() -> None:
    descriptors = (_collector("audit-broker"), _collector("identity-and-trust"))
    observations = (
        HealthObservation(
            component_id="audit-broker",
            observed_at=NOW - timedelta(minutes=5),
            state=HealthState.HEALTHY,
        ),
    )
    result = summarize_health(descriptors, observations, now=NOW)
    assert result.state is HealthState.UNKNOWN
    assert all(item.stale for item in result.components)
    assert {"observation_missing", "observation_stale"} <= set(result.reason_codes)
