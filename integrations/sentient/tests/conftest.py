from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta, timezone
from typing import Any, Mapping

import pytest

from koa_sentient_adapter import (
    OwnerAcceptanceGateway,
    SentientAdapterSettings,
    SentientOperationMap,
    SentientTransport,
    bootstrap_adapter,
)

NOW = datetime(2026, 8, 6, 15, 0, tzinfo=timezone.utc)


class FakeTransport(SentientTransport):
    def __init__(self, results: Mapping[str, Mapping[str, Any]]) -> None:
        self.results = {key: deepcopy(value) for key, value in results.items()}
        self.calls: list[tuple[str, Mapping[str, Any], float]] = []
        self.failure: BaseException | None = None

    def request(
        self,
        operation: str,
        payload: Mapping[str, Any],
        *,
        timeout_seconds: float,
    ) -> Mapping[str, Any]:
        self.calls.append((operation, deepcopy(payload), timeout_seconds))
        if self.failure is not None:
            raise self.failure
        result = deepcopy(self.results[operation])
        if "contract_version" in result:
            return result
        return {"contract_version": "1.0.0", "status": "ok", "result": result}


class FakeGateway(OwnerAcceptanceGateway):
    def __init__(self) -> None:
        self.calls: list[Mapping[str, object]] = []
        self.result: dict[str, Any] = {
            "decision": "accepted",
            "destination_owner": "koa_mediatheque",
            "candidate_id": "candidate-001",
            "decision_ref": "decision:koa-mediatheque:accept-001",
            "decided_at": NOW.isoformat(),
            "reason_code": "OWNER_ACCEPTED",
            "accepted_artifact_ref": "koa-media-record:record-001",
            "evidence_refs": ["evidence:validation-001"],
        }

    def submit_candidate(self, request: Mapping[str, object]) -> Mapping[str, Any]:
        self.calls.append(deepcopy(request))
        return deepcopy(self.result)


@pytest.fixture
def operation_map() -> SentientOperationMap:
    return SentientOperationMap(
        health="sentient.health.v1",
        capabilities="sentient.capabilities.v1",
        submit_job="sentient.job.submit.v1",
        read_job="sentient.job.read.v1",
        cancel_job="sentient.job.cancel.v1",
        fetch_candidate="sentient.candidate.fetch.v1",
    )


@pytest.fixture
def candidate_payload() -> dict[str, Any]:
    return {
        "candidate_id": "candidate-001",
        "artifact_class": "analysis_report",
        "state": "candidate",
        "authoritative": False,
        "media_type": "application/json",
        "content_ref": "candidate-store:objects/candidate-001",
        "digest": {"algorithm": "sha256", "value": "a" * 64},
        "size_bytes": 4096,
        "created_at": NOW.isoformat(),
        "expires_at": (NOW + timedelta(days=7)).isoformat(),
        "input_selection": {
            "workflow_id": "workflow-001",
            "purpose": "research entity reconciliation",
            "requesting_identity": "identity:user-001",
            "source_owner": "kristal_runtime",
            "source_refs": ["kristal:entity-001", "kristal:entity-002"],
            "data_classes": ["governed_knowledge"],
            "selected_fields": ["identifier", "label", "source_refs"],
            "classification": "internal",
            "retention_seconds": 604800,
            "expires_at": (NOW + timedelta(days=7)).isoformat(),
            "integration_refs": [],
            "authority_refs": ["authorization:policy-001"],
            "access_receipt_refs": [],
            "protected": False,
        },
        "provenance": {
            "input_selection_ref": "input-selection:workflow-001",
            "source_refs": ["kristal:entity-001", "kristal:entity-002"],
            "source_revisions": ["revision:source-001"],
            "tool_versions": ["tool:reconciler@1.0.0"],
            "model_versions": ["model:local-analysis@1.0.0"],
            "dependency_versions": ["dependency:engine@1.0.0"],
            "toolchain_versions": ["python@3.13"],
            "execution_environment_ref": "workspace:sentient-001",
            "transformations": ["entity_reconciliation"],
            "evaluations": ["evaluation:consistency-001"],
            "producing_identity": "service:sentient-workbench",
            "produced_at": NOW.isoformat(),
            "output_refs": ["candidate-store:objects/candidate-001"],
            "limitations": ["candidate requires owner review"],
            "configuration_refs": ["config:experiment-001"],
            "prompt_refs": [],
            "acceptance_state": "candidate",
        },
        "validation_refs": ["test:contract-001", "test:boundary-001"],
        "metadata": {"confidence": 0.72, "review_required": True},
    }


@pytest.fixture
def transport(operation_map: SentientOperationMap, candidate_payload: dict[str, Any]) -> FakeTransport:
    capabilities = {
        "subsystem_id": "sentient",
        "observed_at": NOW.isoformat(),
        "default_enabled": False,
        "authority_effect": "candidate_input_only",
        "capabilities": [
            {
                "capability_id": "sentient_isolated_analysis",
                "purpose": "isolated research and enrichment",
                "direction": "bidirectional",
                "state": "healthy",
                "observed_at": NOW.isoformat(),
                "operations": ["classification", "summarization", "tagging"],
                "candidate_output_classes": ["analysis_report", "candidate_artifact"],
                "requires_network": False,
                "integration_refs": [],
                "reason_code": "OK",
            }
        ],
    }
    results = {
        operation_map.health: {
            "subsystem_id": "sentient",
            "state": "healthy",
            "ready": True,
            "observed_at": NOW.isoformat(),
            "reason_code": "OK",
            "active_jobs": 1,
            "queue_depth": 0,
            "candidate_storage_available": True,
            "core_impact": "none",
            "evidence_refs": ["evidence:health-001"],
        },
        operation_map.capabilities: capabilities,
        operation_map.submit_job: {
            "job_id": "job-001",
            "request_id": "request-001",
            "state": "admitted",
            "observed_at": NOW.isoformat(),
            "reason_code": "RESOURCE_ADMITTED",
            "candidate_refs": [],
            "evidence_refs": ["receipt:resource-admission-001"],
            "retryable": False,
            "authoritative_effect": False,
        },
        operation_map.read_job: {
            "job_id": "job-001",
            "request_id": "request-001",
            "state": "completed",
            "observed_at": NOW.isoformat(),
            "reason_code": "CANDIDATE_PRODUCED",
            "candidate_refs": ["candidate-001"],
            "evidence_refs": ["receipt:job-complete-001"],
            "retryable": False,
            "authoritative_effect": False,
        },
        operation_map.cancel_job: {
            "job_id": "job-001",
            "request_id": "request-001",
            "state": "cancelled",
            "observed_at": NOW.isoformat(),
            "reason_code": "USER_CANCELLED",
            "candidate_refs": [],
            "evidence_refs": ["receipt:job-cancelled-001"],
            "retryable": False,
            "authoritative_effect": False,
        },
        operation_map.fetch_candidate: candidate_payload,
    }
    return FakeTransport(results)


@pytest.fixture
def gateway() -> FakeGateway:
    return FakeGateway()


@pytest.fixture
def settings(operation_map: SentientOperationMap) -> SentientAdapterSettings:
    return SentientAdapterSettings(
        subsystem_id="sentient",
        subsystem_contract_version="1.0.0",
        adapter_contract_version="1.0.0",
        operations=operation_map,
        active_profile="developer_linux_workstation",
        workspace_id="workspace:sentient-001",
        service_identity_ref="service:sentient-workbench",
        documentation_alignment_verified=True,
        enabled=True,
        allowed_destination_interfaces=(
            "components/koa-mediatheque/public-api:candidate-import",
            "components/kristal-runtime/public-api:candidate-import",
        ),
    )


@pytest.fixture
def adapter(settings: SentientAdapterSettings, transport: FakeTransport, gateway: FakeGateway):
    return bootstrap_adapter(settings, transport=transport, owner_gateway=gateway)
