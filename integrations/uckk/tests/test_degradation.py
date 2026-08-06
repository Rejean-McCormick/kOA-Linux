from __future__ import annotations

from copy import deepcopy

import pytest

from conftest import make_service
from koa_uckk_adapter.learning_import import (
    ImportAction,
    ImportRequest,
    ImportWorkflowError,
    PolicyOutcome,
)


def test_remote_retrieval_failure_is_explicit_and_never_calls_mediatheque(
    valid_package, import_request
) -> None:
    service, deps = make_service(valid_package)
    deps["client"].fail_operation = "retrieve_learning_package"

    result = service.import_online(import_request)

    assert result.outcome == "failed"
    assert result.quarantine_ref is None
    assert not deps["mediatheque"].accept_calls
    assert result.receipt["validation"]["integrity_verified"] is False
    assert "reason:PACKAGE_RETRIEVAL_FAILED" in result.receipt["notes"]


def test_integrity_failure_rejects_package_after_quarantine(
    valid_package, import_request
) -> None:
    service, deps = make_service(valid_package, integrity_valid=False)

    result = service.import_online(import_request)

    assert result.outcome == "rejected"
    assert deps["events"][0] not in {"mediatheque_accept", "governance_evaluate"}
    assert "quarantine_place" in deps["events"]
    assert not deps["mediatheque"].accept_calls
    assert "RESOURCE_INTEGRITY_FAILED" in result.receipt["validation"]["failure_codes"]


def test_incomplete_manifest_remains_quarantined(valid_package, import_request) -> None:
    package = deepcopy(valid_package)
    package["manifest"]["entry_count"] = 2
    service, deps = make_service(package)

    result = service.import_online(import_request)

    assert result.outcome == "quarantined"
    assert "MANIFEST_INCOMPLETE" in result.receipt["validation"]["failure_codes"]
    assert not deps["governance"].calls


def test_unavailable_malware_scan_blocks_acceptance(valid_package, import_request) -> None:
    service, deps = make_service(valid_package, malware_outcome="unavailable_blocked")

    result = service.import_online(import_request)

    assert result.outcome == "quarantined"
    assert result.receipt["validation"]["malware_scan_outcome"] == "unavailable_blocked"
    assert "MALWARE_SCAN_UNAVAILABLE" in result.receipt["validation"]["failure_codes"]
    assert not deps["mediatheque"].accept_calls


def test_offline_bundle_import_needs_no_remote_call(
    valid_package, import_request, offline_bundle
) -> None:
    service, deps = make_service(valid_package)

    result = service.import_offline(
        import_request,
        package=valid_package,
        offline_bundle=offline_bundle,
    )

    assert result.outcome == "accepted"
    assert deps["client"].calls == []
    assert "verify_offline_bundle" in deps["events"]
    candidate = deps["mediatheque"].accept_calls[0]["candidates"][0]
    assert candidate["provenance"]["acquisition_method"] == "imported_offline_bundle"


def test_invalid_offline_bundle_remains_quarantined(
    valid_package, import_request, offline_bundle
) -> None:
    service, deps = make_service(valid_package, offline_bundle_valid=False)

    result = service.import_offline(
        import_request,
        package=valid_package,
        offline_bundle=offline_bundle,
    )

    assert result.outcome == "quarantined"
    assert "OFFLINE_BUNDLE_INVALID" in result.receipt["validation"]["failure_codes"]
    assert not deps["mediatheque"].accept_calls


def test_validate_only_never_implies_local_acceptance(valid_package, import_request) -> None:
    request = ImportRequest(
        request_id=import_request.request_id,
        package_id=import_request.package_id,
        idempotency_key="idem:uckk:validate-only:001",
        correlation_id=import_request.correlation_id,
        actor_ref=import_request.actor_ref,
        authority_domain_id=import_request.authority_domain_id,
        endpoint_id=import_request.endpoint_id,
        selection_type=import_request.selection_type,
        source_object_refs=import_request.source_object_refs,
        source_version_refs=import_request.source_version_refs,
        action=ImportAction.VALIDATE_ONLY,
    )
    service, deps = make_service(valid_package)

    result = service.import_online(request)

    assert result.outcome == "quarantined"
    assert not deps["governance"].calls
    assert not deps["mediatheque"].accept_calls
    assert "reason:EXPLICIT_LOCAL_ACCEPTANCE_REQUIRED" in result.receipt["notes"]


def test_governance_review_keeps_package_in_quarantine(valid_package, import_request) -> None:
    service, deps = make_service(valid_package, policy_outcome=PolicyOutcome.REVIEW)

    result = service.import_online(import_request)

    assert result.outcome == "quarantined"
    assert len(deps["governance"].calls) == 1
    assert not deps["mediatheque"].accept_calls


def test_idempotent_replay_returns_prior_result_without_new_side_effects(
    valid_package, import_request
) -> None:
    service, deps = make_service(valid_package)
    first = service.import_online(import_request)
    call_count = len(deps["client"].calls)
    event_count = len(deps["events"])

    second = service.import_online(import_request)

    assert second.receipt_ref == first.receipt_ref
    assert len(deps["client"].calls) == call_count
    assert len(deps["events"]) == event_count


def test_idempotency_key_cannot_be_reused_for_a_different_selection(
    valid_package, import_request
) -> None:
    service, _ = make_service(valid_package)
    service.import_online(import_request)
    changed = ImportRequest(
        request_id=import_request.request_id,
        package_id=import_request.package_id,
        idempotency_key=import_request.idempotency_key,
        correlation_id=import_request.correlation_id,
        actor_ref=import_request.actor_ref,
        authority_domain_id=import_request.authority_domain_id,
        endpoint_id=import_request.endpoint_id,
        selection_type=import_request.selection_type,
        source_object_refs=("uckk:object:course-002",),
        source_version_refs=import_request.source_version_refs,
        action=import_request.action,
    )

    with pytest.raises(ImportWorkflowError) as failure:
        service.import_online(changed)
    assert failure.value.code == "IDEMPOTENCY_CONFLICT"


def test_mediatheque_cannot_return_uckk_ids_as_local_identity(
    valid_package, import_request
) -> None:
    service, deps = make_service(valid_package)
    deps["mediatheque"].accept_response["local_record_refs"] = ["uckk:object:course-001"]

    result = service.import_online(import_request)

    assert result.outcome == "failed"
    assert result.quarantine_ref is not None
    assert "reason:INVALID_LOCAL_ACCEPTANCE" in result.receipt["notes"]
    assert deps["quarantine"].states[-1]["state"] == "failed"


def test_governance_unavailability_keeps_verified_package_quarantined(
    valid_package, import_request
) -> None:
    service, deps = make_service(valid_package)
    deps["governance"].failure = TimeoutError("policy runtime unavailable")

    result = service.import_online(import_request)

    assert result.outcome == "quarantined"
    assert result.quarantine_ref is not None
    assert "reason:GOVERNANCE_EVALUATION_UNAVAILABLE" in result.receipt["notes"]
    assert not deps["mediatheque"].accept_calls


def test_mediatheque_unavailability_produces_terminal_failure_receipt(
    valid_package, import_request
) -> None:
    service, deps = make_service(valid_package)
    deps["mediatheque"].accept_failure = ConnectionError("Mediatheque unavailable")

    result = service.import_online(import_request)

    assert result.outcome == "failed"
    assert result.quarantine_ref is not None
    assert "reason:LOCAL_ACCEPTANCE_UNAVAILABLE" in result.receipt["notes"]
    assert deps["quarantine"].states[-1]["state"] == "failed"


def test_offline_import_rejects_unallowlisted_endpoint(
    valid_package, import_request, offline_bundle
) -> None:
    service, _ = make_service(valid_package)
    request = ImportRequest(
        request_id=import_request.request_id,
        package_id=import_request.package_id,
        idempotency_key="idem:uckk:offline-unallowlisted:001",
        correlation_id=import_request.correlation_id,
        actor_ref=import_request.actor_ref,
        authority_domain_id=import_request.authority_domain_id,
        endpoint_id="uckk-untrusted",
        selection_type=import_request.selection_type,
        source_object_refs=import_request.source_object_refs,
        source_version_refs=import_request.source_version_refs,
        action=import_request.action,
    )

    with pytest.raises(ImportWorkflowError) as failure:
        service.import_offline(request, package=valid_package, offline_bundle=offline_bundle)

    assert failure.value.code == "ENDPOINT_NOT_ALLOWLISTED"
