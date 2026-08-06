from __future__ import annotations

from copy import deepcopy
import ast
from pathlib import Path

import pytest

from conftest import LOCAL_AUTHORITY, NOW, SOURCE_AUTHORITY, make_service
from koa_uckk_adapter.learning_import import ImportAction, ImportRequest
from koa_uckk_adapter.mediatheque_frame import FrameMappingError
from koa_uckk_adapter.package_verification import TransportKind, VerificationDisposition

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = REPOSITORY_ROOT / "integrations/uckk/adapter/src/koa_uckk_adapter"


def test_verified_projection_preserves_source_and_creates_no_local_identity(
    valid_package,
) -> None:
    service, deps = make_service(valid_package)
    report = deps["verifier"].verify(
        valid_package,
        transport_kind=TransportKind.ONLINE,
        verified_at=NOW,
    )

    assert report.disposition is VerificationDisposition.VERIFIED
    candidate = report.candidates[0]
    request = candidate.to_mediatheque_request()
    assert request["candidate_state"] == "quarantined"
    assert request["local_record_id"] is None
    assert request["local_version_id"] is None
    assert request["provenance"]["source_authority_domain_id"] == SOURCE_AUTHORITY
    assert request["authority_domain_id"] == LOCAL_AUTHORITY
    assert request["provenance"]["source_object_ref"].startswith("uckk:")


def test_online_import_uses_explicit_selection_and_public_acceptance(
    valid_package, import_request
) -> None:
    service, deps = make_service(valid_package)

    result = service.import_online(import_request)

    assert result.outcome == "accepted"
    assert [call["operation"] for call in deps["client"].calls] == [
        "resolve_selected_source_graph",
        "retrieve_learning_package",
    ]
    assert deps["client"].calls[0]["payload"]["selection"]["source_object_refs"] == [
        "uckk:object:course-001"
    ]
    assert result.local_record_refs == ("koa_media_import_001",)
    assert result.local_version_refs == ("koa_media_version_import_001",)
    assert result.receipt["authority_separation_preserved"] is True
    assert len(deps["mediatheque"].accept_calls) == 1


def test_quarantine_is_first_local_transition_before_verification_and_acceptance(
    valid_package, import_request
) -> None:
    service, deps = make_service(valid_package)

    service.import_online(import_request)

    events = deps["events"]
    assert events.index("quarantine_place") < events.index("verify_manifest")
    assert events.index("quarantine_place") < events.index("verify_resource")
    assert events.index("verify_resource") < events.index("governance_evaluate")
    assert events.index("governance_evaluate") < events.index("mediatheque_accept")


def test_remote_update_is_only_a_candidate_and_never_an_overwrite(
    valid_package, import_request
) -> None:
    update_request = ImportRequest(
        request_id=import_request.request_id,
        package_id=import_request.package_id,
        idempotency_key="idem:uckk:update:001",
        correlation_id=import_request.correlation_id,
        actor_ref=import_request.actor_ref,
        authority_domain_id=import_request.authority_domain_id,
        endpoint_id=import_request.endpoint_id,
        selection_type=import_request.selection_type,
        source_object_refs=import_request.source_object_refs,
        source_version_refs=import_request.source_version_refs,
        action=ImportAction.OFFER_UPDATE_CANDIDATE,
    )
    service, deps = make_service(valid_package)

    result = service.import_online(update_request)

    assert result.outcome == "update_candidate"
    assert not deps["mediatheque"].accept_calls
    assert len(deps["mediatheque"].update_calls) == 1
    assert result.receipt["update_policy"] == {
        "automatic_remote_overwrite": False,
        "remote_version_ref": "uckk:version:course-001:v1",
        "local_decision_required": True,
        "conflict_state": "local_changes_present",
    }


def test_source_authority_cannot_be_relabelled_as_local(valid_package) -> None:
    package = deepcopy(valid_package)
    package["provenance"]["source_authority_domain_id"] = LOCAL_AUTHORITY
    package["resources"][0]["frame"]["object_identity"]["authority_domain_id"] = LOCAL_AUTHORITY
    package["resources"][0]["frame"]["lifecycle"]["authority_domain_id"] = LOCAL_AUTHORITY
    service, deps = make_service(package)

    report = deps["verifier"].verify(
        package,
        transport_kind=TransportKind.ONLINE,
        verified_at=NOW,
    )

    assert report.disposition is VerificationDisposition.QUARANTINED
    assert "SOURCE_AUTHORITY_MISMATCH" in report.failure_codes


def test_mismatched_frame_mapping_is_blocked(valid_package) -> None:
    package = deepcopy(valid_package)
    package["resources"][0]["frame"]["mapping"]["mapping_version"] = "9.9.9"
    service, deps = make_service(package)

    report = deps["verifier"].verify(
        package,
        transport_kind=TransportKind.ONLINE,
        verified_at=NOW,
    )

    assert report.disposition is VerificationDisposition.QUARANTINED
    assert "MAPPING_METADATA_CONFLICT" in report.failure_codes
    assert "FRAME_INCOMPATIBLE" in report.failure_codes


def test_new_modules_have_no_direct_database_network_or_background_sync() -> None:
    files = (
        SOURCE_ROOT / "learning_import.py",
        SOURCE_ROOT / "mediatheque_frame.py",
        SOURCE_ROOT / "package_verification.py",
    )
    forbidden_imports = {
        "sqlite3",
        "psycopg",
        "sqlalchemy",
        "requests",
        "httpx",
        "socket",
        "subprocess",
    }
    imports: set[str] = set()
    combined = ""
    for source in files:
        text = source.read_text(encoding="utf-8")
        combined += text.lower()
        tree = ast.parse(text, filename=str(source))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
    assert imports.isdisjoint(forbidden_imports)
    assert "bidirectional_sync" not in combined
    assert "last_writer_wins" not in combined
    assert "automatic_remote_overwrite\": true" not in combined
