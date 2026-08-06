"""Contract and artifact proofs for Publication Gateway."""

from __future__ import annotations

import json
from pathlib import Path
import tomllib

import pytest
from jsonschema import Draft202012Validator

from koa_publication_gateway.api import (
    API_VERSION,
    INTERFACE_VERSIONS,
    PUBLICATION_REQUEST_REQUIRED_FIELDS,
    ROUTE_DEFINITIONS,
    ExecutionResult,
    ModelValidationError,
    PublicationDecision,
    PublicationDecisionOutcome,
    PublicationReceipt,
    PublicationRecordState,
    PublicationRequestCommand,
    PublicationRequestResult,
    PublicationState,
)

EXPECTED_INTERFACES = {
    "publication_request",
    "revocation_or_withdrawal_notice",
    "publication_status_query",
    "health",
    "queue_inspection",
    "controlled_retry",
}


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_component_contract_identity_and_interfaces(repository_root: Path) -> None:
    contract = load_json(repository_root / "docs/contracts/components/publication-gateway.component.json")
    assert contract["component_id"] == "publication_gateway"
    assert contract["version"] == API_VERSION
    callable_interfaces = {
        entry["interface_id"]
        for group in ("inbound", "administrative")
        for entry in contract["interfaces"][group]
    }
    assert callable_interfaces == EXPECTED_INTERFACES
    assert contract["authority"]["direct_cross_component_authoritative_writes_allowed"] is False
    assert contract["authority"]["authority_transfer_by_publication"] is False


def test_route_registry_and_payload_match_contract(repository_root: Path) -> None:
    payload = tomllib.loads((repository_root / "components/publication-gateway/packaging/payload.toml").read_text())
    assert set(ROUTE_DEFINITIONS) == EXPECTED_INTERFACES
    assert set(INTERFACE_VERSIONS.values()) == {API_VERSION}
    assert {item["interface_id"] for item in payload["interface"]} == EXPECTED_INTERFACES
    assert payload["component_id"] == "publication_gateway"
    assert payload["authority"]["partial_delivery_as_success"] is False
    assert payload["authority"]["direct_cross_component_database_access"] is False


def test_artifact_schemas_are_valid_and_keep_contract_ids(repository_root: Path) -> None:
    request_schema = load_json(repository_root / "docs/contracts/artifact-contracts/publication-request.schema.json")
    receipt_schema = load_json(repository_root / "docs/contracts/artifact-contracts/publication-receipt.schema.json")
    Draft202012Validator.check_schema(request_schema)
    Draft202012Validator.check_schema(receipt_schema)
    assert request_schema["$id"].endswith("/publication-request.schema.json")
    assert receipt_schema["$id"].endswith("/publication-receipt.schema.json")
    assert frozenset(request_schema["required"]) == PUBLICATION_REQUEST_REQUIRED_FIELDS
    assert receipt_schema["properties"]["artifact_class"]["const"] == "publication_receipt"


def test_component_decision_and_delivery_enums_remain_exact(repository_root: Path) -> None:
    contract = load_json(repository_root / "docs/contracts/components/publication-gateway.component.json")
    assert contract["decision_model"]["results"] == ["allow", "deny", "blocked", "review_required"]
    assert contract["state_machine"]["automatic_transition_after_reconnection_allowed"] is False
    assert contract["idempotency_and_delivery"]["partial_delivery_requires_remediation"] is True
    assert contract["gateway_separation"]["publication_gateway_performs_uckk_transport"] is False


def test_publication_request_model_accepts_bounded_artifact(publication_artifact) -> None:
    command = PublicationRequestCommand(publication_artifact)
    assert command.artifact_request_id == "publication-request:example:001"
    assert command.publication_request["source"]["source_authority_preserved"] is True


def test_secret_material_is_rejected(mutable_publication_artifact) -> None:
    mutable_publication_artifact["security"]["api_key"] = "not-allowed"
    with pytest.raises(ModelValidationError, match="secret material"):
        PublicationRequestCommand(mutable_publication_artifact)


def test_unbounded_selection_is_rejected(mutable_publication_artifact) -> None:
    mutable_publication_artifact["selection"]["minimum_necessary_reviewed"] = False
    with pytest.raises(ModelValidationError, match="minimum necessary"):
        PublicationRequestCommand(mutable_publication_artifact)


def test_direct_destination_write_is_rejected(mutable_publication_artifact) -> None:
    mutable_publication_artifact["destination"]["direct_authoritative_write_allowed"] = True
    with pytest.raises(ModelValidationError, match="declared interface"):
        PublicationRequestCommand(mutable_publication_artifact)


def test_allow_decision_requires_obligations() -> None:
    with pytest.raises(ModelValidationError, match="must not be empty"):
        PublicationDecision("decision:1", PublicationDecisionOutcome.ALLOW, "request:1", ("authority:1",), (), True)


def test_non_allow_decision_cannot_execute() -> None:
    with pytest.raises(ModelValidationError, match="only an allow"):
        PublicationDecision("decision:1", PublicationDecisionOutcome.BLOCKED, "request:1", ("authority:1",), (), True)


def test_published_receipt_requires_destination_acknowledgement() -> None:
    with pytest.raises(ModelValidationError, match="destination acknowledgement"):
        PublicationReceipt(
            "receipt:1", "request:1", "source:v1", "destination:1", "audience:1", "decision:1",
            ExecutionResult.PUBLISHED, PublicationRecordState.ACTIVE, "correlation:1", ("evidence:1",),
        )


def test_partial_delivery_requires_remediation() -> None:
    with pytest.raises(ModelValidationError, match="explicit remediation"):
        PublicationReceipt(
            "receipt:1", "request:1", "source:v1", "destination:1", "audience:1", "decision:1",
            ExecutionResult.PARTIALLY_DELIVERED, PublicationRecordState.REMEDIATION_PENDING, "correlation:1", ("evidence:1",),
        )


def test_published_state_cannot_hide_failed_receipt() -> None:
    decision = PublicationDecision("decision:1", PublicationDecisionOutcome.ALLOW, "request:1", ("authority:1",), ("obligation:1",), True)
    receipt = PublicationReceipt(
        "receipt:1", "request:1", "source:v1", "destination:1", "audience:1", "decision:1",
        ExecutionResult.FAILED, PublicationRecordState.NOT_PUBLISHED, "correlation:1", ("evidence:1",),
    )
    with pytest.raises(ModelValidationError, match="acknowledged receipt"):
        PublicationRequestResult("request:1", PublicationState.PUBLISHED, decision, receipt)
