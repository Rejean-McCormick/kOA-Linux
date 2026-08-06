from __future__ import annotations

import ast
from pathlib import Path

import pytest

from koa_ariane_adapter import (
    CandidateIntent,
    IntentRejected,
    IntentSource,
    NavigationEvidenceType,
    NavigationMode,
    NavigationReceipt,
    ReceiptClass,
    ReceiptOutcome,
)

from conftest import NOW


ADAPTER_ROOT = Path(__file__).resolve().parents[1] / "adapter" / "src" / "koa_ariane_adapter"


def test_adapter_has_no_direct_host_database_or_network_implementation() -> None:
    prohibited_roots = {
        "asyncio.subprocess",
        "http.client",
        "httpx",
        "os",
        "requests",
        "socket",
        "sqlite3",
        "subprocess",
        "urllib",
    }
    found: list[str] = []
    for path in sorted(ADAPTER_ROOT.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            else:
                continue
            for name in names:
                if any(name == root or name.startswith(f"{root}.") for root in prohibited_roots):
                    found.append(f"{path.name}:{name}")
    assert found == []


def test_guidance_calls_guidance_operation_not_execution(adapter, transport, guidance_request) -> None:
    snapshot = adapter.health.probe(request_id="health:guidance").capabilities
    outcome = adapter.navigation.guide(guidance_request, snapshot, now=NOW)
    assert outcome.result.state.value == "planned"
    operations = [call[0] for call in transport.calls]
    assert "navigation.guide" in operations
    assert "navigation.execute" not in operations


def test_completed_automation_requires_verification_and_emits_two_receipts(
    adapter,
    transport,
    automation_request,
) -> None:
    transport.navigation_state = "completed"
    transport.navigation_reason = "ARIANE_TRANSITION_VERIFIED"
    snapshot = adapter.health.probe(request_id="health:execute").capabilities
    outcome = adapter.navigation.execute(automation_request, snapshot, now=NOW)
    assert outcome.result.state.value == "completed"
    assert [receipt.evidence_type for receipt in outcome.receipts] == [
        NavigationEvidenceType.EXECUTION,
        NavigationEvidenceType.VERIFICATION,
    ]
    assert all(receipt.outcome is ReceiptOutcome.COMMITTED for receipt in outcome.receipts)


def test_candidate_intent_rejects_authority_fields() -> None:
    with pytest.raises(IntentRejected) as error:
        CandidateIntent.from_mapping(
            {
                "candidate_id": "candidate:bad",
                "source": IntentSource.EXTERNAL_VOICE.value,
                "application_id": "app.example",
                "goal_id": "goal.example",
                "created_at": NOW.isoformat(),
                "parameters": {},
                "authority_refs": ["authority:forbidden"],
            }
        )
    assert error.value.reason_code == "ARIANE_INTENT_FORBIDDEN_AUTHORITY_FIELD"


def test_receipts_reject_secrets_and_raw_capture() -> None:
    with pytest.raises(ValueError, match="prohibited"):
        NavigationReceipt.create(
            receipt_class=ReceiptClass.TRANSITION,
            evidence_type=NavigationEvidenceType.FAILURE,
            outcome=ReceiptOutcome.FAILED,
            request_id="request:1",
            correlation_id="correlation:1",
            subject_ref="identity:user:1",
            actor_ref="identity:user:1",
            application_ref="app.example",
            reason_code="ARIANE_TEST_FAILURE",
            recorded_at=NOW,
            details={"raw_screen": "private content"},
        )


def test_receipt_is_deterministic_for_same_transition() -> None:
    kwargs = dict(
        receipt_class=ReceiptClass.TRANSITION,
        evidence_type=NavigationEvidenceType.CANCELLATION,
        outcome=ReceiptOutcome.CANCELLED,
        request_id="request:1",
        correlation_id="correlation:1",
        subject_ref="identity:user:1",
        actor_ref="identity:user:1",
        application_ref="app.example",
        reason_code="ARIANE_CANCELLED_BY_USER",
        recorded_at=NOW,
    )
    first = NavigationReceipt.create(**kwargs)
    second = NavigationReceipt.create(**kwargs)
    assert first.receipt_id == second.receipt_id
    assert first.to_dict() == second.to_dict()
