from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from koa_sentient_adapter import (
    CandidateImportRequest,
    ReceiptOutcome,
    ReceiptType,
    WorkbenchReceipt,
)

NOW = datetime(2026, 8, 6, 15, 0, tzinfo=timezone.utc)
PACKAGE_ROOT = Path(__file__).parents[1] / "adapter" / "src" / "koa_sentient_adapter"


def test_adapter_has_no_direct_store_host_or_listener_implementation() -> None:
    prohibited = (
        "import sqlite3",
        "import psycopg",
        "import sqlalchemy",
        "from sqlalchemy",
        "subprocess.",
        "os.system",
        "socket.listen",
        "socket.bind",
        "http.server",
        "uvicorn.run",
        "privileged_broker.execute",
        "direct_write",
    )
    sources = "\n".join(path.read_text(encoding="utf-8") for path in sorted(PACKAGE_ROOT.glob("*.py")))
    for marker in prohibited:
        assert marker not in sources


def test_only_declared_public_package_files_exist() -> None:
    assert {path.name for path in PACKAGE_ROOT.glob("*.py")} == {
        "__init__.py",
        "artifact_bridge.py",
        "bootstrap.py",
        "candidate_artifacts.py",
        "capabilities.py",
        "client.py",
        "health.py",
        "receipts.py",
        "workbench_jobs.py",
    }


def test_receipts_reject_secrets_and_remain_evidence_only() -> None:
    with pytest.raises(ValueError, match="prohibited"):
        WorkbenchReceipt.create(
            receipt_type=ReceiptType.WORKBENCH_STATE,
            outcome=ReceiptOutcome.RECORDED,
            request_id="request-001",
            correlation_id="correlation-001",
            subject_ref="workspace:sentient-001",
            actor_ref="identity:user-001",
            reason_code="CREATED",
            recorded_at=NOW,
            details={"access_token": "do-not-log"},
        )
    receipt = WorkbenchReceipt.create(
        receipt_type=ReceiptType.WORKBENCH_STATE,
        outcome=ReceiptOutcome.RECORDED,
        request_id="request-001",
        correlation_id="correlation-001",
        subject_ref="workspace:sentient-001",
        actor_ref="identity:user-001",
        reason_code="CREATED",
        recorded_at=NOW,
        details={"state": "created"},
    )
    assert receipt.to_dict()["authority_effect"] == "evidence_only"
    assert receipt.to_dict()["authoritative"] is False


def test_candidate_import_rejects_direct_database_or_filesystem_target() -> None:
    common = dict(
        request_id="request-001",
        correlation_id="correlation-001",
        candidate_id="candidate-001",
        candidate_fingerprint="a" * 64,
        source_job_ref="job:001",
        destination_owner="koa_mediatheque",
        intended_artifact_class="koa_media_record",
        actor_ref="identity:user-001",
        purpose="controlled import",
        requested_at=NOW,
        validation_refs=("test:one",),
        authority_refs=("authorization:one",),
        content_ref="candidate-store:objects/001",
    )
    with pytest.raises(ValueError, match="registered interface"):
        CandidateImportRequest(destination_interface_ref="sqlite:///var/lib/media.db", **common)
    with pytest.raises(ValueError, match="registered interface"):
        CandidateImportRequest(destination_interface_ref="/var/lib/koa/media", **common)


def test_bootstrapped_adapter_is_optional_and_non_core(adapter) -> None:
    assert adapter.subsystem_id == "sentient"
    assert adapter.core_dependency is False
    assert adapter.settings.default_enabled is False
    assert adapter.settings.public_listener_enabled is False
    assert adapter.settings.privileged_broker_direct_access is False
