from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Any, Iterator, Mapping

from jsonschema import Draft202012Validator, FormatChecker
import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
ADAPTER_SRC = REPOSITORY_ROOT / "integrations" / "uckk" / "adapter" / "src"
sys.path.insert(0, str(ADAPTER_SRC))

from koa_uckk_adapter.moodle_client import MoodleClientError  # noqa: E402
from koa_uckk_adapter.publication import (  # noqa: E402
    PublicationError,
    PublicationService,
    StoredPublication,
)


class SchemaPort:
    def __init__(self) -> None:
        path = REPOSITORY_ROOT / "docs/contracts/artifact-contracts/uckk-publication-package.schema.json"
        self._validator = Draft202012Validator(
            json.loads(path.read_text(encoding="utf-8")),
            format_checker=FormatChecker(),
        )

    def validate(self, package: Mapping[str, Any]) -> None:
        self._validator.validate(package)


class ManifestPort:
    def __init__(self, valid: bool = True) -> None:
        self.valid = valid

    def verify(self, package: Mapping[str, Any]) -> bool:
        return self.valid and package["manifest"]["item_count"] == len(package["items"])


class AuthorizationPort:
    def __init__(self, current: bool = True) -> None:
        self.current = current

    def authorization_is_current(self, package: Mapping[str, Any], *, at: datetime) -> bool:
        return self.current and package["authorization"]["decision_outcome"] == "allow"


class SourcePort:
    def __init__(self, stale_item_ids: set[str] | None = None) -> None:
        self.stale_item_ids = stale_item_ids or set()

    def source_item_is_current(self, item: Mapping[str, Any], *, at: datetime) -> bool:
        return item["item_id"] not in self.stale_item_ids


@dataclass(frozen=True, slots=True)
class MemoryPayload:
    data: bytes
    media_type: str
    filename: str | None

    @property
    def size_bytes(self) -> int:
        return len(self.data)

    def iter_chunks(self) -> Iterator[bytes]:
        yield self.data


class PayloadPort:
    def __init__(self, values: Mapping[str, bytes]) -> None:
        self.values = dict(values)

    def resolve_verified(
        self,
        *,
        transfer_ref: str,
        integrity: Mapping[str, Any],
        size_bytes: int,
        media_type: str,
        filename: str | None,
    ) -> MemoryPayload:
        data = self.values[transfer_ref]
        algorithm = str(integrity["algorithm"])
        digest = __import__("hashlib").new(algorithm, data).hexdigest()
        if digest != integrity["digest"] or len(data) != size_bytes:
            raise PublicationError("CONTENT_INTEGRITY_FAILED", "payload integrity verification failed")
        return MemoryPayload(data, media_type, filename)


class WorkflowStore:
    def __init__(self) -> None:
        self.values: dict[str, StoredPublication] = {}
        self.saves: list[StoredPublication] = []

    def load(self, idempotency_key: str) -> StoredPublication | None:
        return self.values.get(idempotency_key)

    def save(self, publication: StoredPublication) -> None:
        stored = deepcopy(publication)
        self.values[publication.idempotency_key] = stored
        self.saves.append(stored)


class QueuePort:
    def __init__(self) -> None:
        self.entries: list[dict[str, Any]] = []

    def enqueue(
        self,
        *,
        package: Mapping[str, Any],
        workflow: Mapping[str, Any],
        reason_code: str,
    ) -> str:
        self.entries.append(
            {"package": deepcopy(dict(package)), "workflow": deepcopy(dict(workflow)), "reason_code": reason_code}
        )
        return f"queue://uckk/{package['package_id']}"


class ReceiptPort:
    def __init__(self) -> None:
        self.values: list[dict[str, Any]] = []

    def persist(self, receipt: Mapping[str, Any]) -> str:
        value = deepcopy(dict(receipt))
        self.values.append(value)
        return f"receipt://uckk/{receipt['receipt_id']}"


class FixedClock:
    def now(self) -> datetime:
        return datetime(2026, 8, 6, 15, 0, tzinfo=timezone.utc)


class SequenceIds:
    def __init__(self) -> None:
        self.value = 0

    def new(self, prefix: str) -> str:
        self.value += 1
        return f"{prefix}_{self.value:04d}"


class FakeMoodle:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str | None]] = []
        self.initial_status: dict[str, Any] = {"outcome": "not_found"}
        self.item_status: dict[str, dict[str, Any]] = {}
        self.fail_items: dict[str, MoodleClientError] = {}
        self.authenticate_error: MoodleClientError | None = None
        self.receipt_error: MoodleClientError | None = None

    def authenticate(self, *, correlation_id: str) -> Mapping[str, Any]:
        self.calls.append(("authenticate", None))
        if self.authenticate_error is not None:
            raise self.authenticate_error
        return {"authenticated": True}

    def validate_destination_capability(
        self,
        *,
        mapping_version: str,
        object_kinds: tuple[str, ...],
        correlation_id: str,
    ) -> Mapping[str, Any]:
        self.calls.append(("validate_destination_capability", mapping_version))
        return {"supported": True, "mapping_version": mapping_version, "object_kinds": list(object_kinds)}

    def query_publication_status(
        self,
        *,
        idempotency_key: str,
        correlation_id: str,
    ) -> Mapping[str, Any]:
        self.calls.append(("query_publication_status", idempotency_key))
        return deepcopy(self.item_status.get(idempotency_key, self.initial_status))

    def create_or_update_remote_representation(
        self,
        *,
        item: Mapping[str, Any],
        idempotency_key: str,
        mapping_version: str,
        correlation_id: str,
    ) -> Mapping[str, Any]:
        item_id = str(item["item_id"])
        self.calls.append(("create_or_update_remote_representation", item_id))
        if item_id in self.fail_items:
            raise self.fail_items[item_id]
        return {"remote_object_ref": f"moodle://object/{item_id}", "updated": False}

    def upload_content(
        self,
        *,
        remote_object_ref: str,
        payload: MemoryPayload,
        integrity: Mapping[str, Any],
        idempotency_key: str,
        correlation_id: str,
    ) -> Mapping[str, Any]:
        self.calls.append(("upload_content", remote_object_ref))
        assert b"".join(payload.iter_chunks())
        return {"remote_version_ref": "remote-v1", "http_status": 201}

    def attach_metadata(
        self,
        *,
        remote_object_ref: str,
        metadata: Mapping[str, Any],
        rights_assertion: Mapping[str, Any],
        idempotency_key: str,
        correlation_id: str,
    ) -> Mapping[str, Any]:
        self.calls.append(("attach_metadata", remote_object_ref))
        return {"attached": True}

    def receive_publication_receipt(
        self,
        *,
        idempotency_key: str,
        correlation_id: str,
    ) -> Mapping[str, Any]:
        self.calls.append(("receive_publication_receipt", idempotency_key))
        if self.receipt_error is not None:
            raise self.receipt_error
        return {"receipt": {"outcome": "published"}, "receipt_ref": "uckk://receipt/remote-1"}


def media_item(item_id: str, data: bytes) -> dict[str, Any]:
    return {
        "item_id": item_id,
        "record_id": f"record_{item_id}",
        "version_id": f"version_{item_id}",
        "title": f"Media {item_id}",
        "description": "Synthetic contract fixture",
        "media_type": "text/plain",
        "content": {
            "transfer_ref": f"koa-object://mediatheque/{item_id}",
            "size_bytes": len(data),
            "original_filename": f"{item_id}.txt",
        },
        "integrity": {"algorithm": "sha256", "digest": sha256(data).hexdigest()},
        "metadata": {"language": "en", "fixture": True},
        "rights_assertion": {
            "publication_allowed": True,
            "target_allowed": True,
            "checked_at": "2026-08-06T14:55:00Z",
            "rights_policy_refs": ["rights://policy/publication"],
            "consent_refs": ["consent://fixture/1"],
            "restriction_summary": [],
        },
        "destination_mapping": {"object_kind": "media_resource", "update_policy": "create_or_update"},
    }


def publication_package(*, two_items: bool = False) -> tuple[dict[str, Any], dict[str, bytes]]:
    payloads = {
        "koa-object://mediatheque/item-a": b"alpha",
        "koa-object://mediatheque/item-b": b"bravo",
    }
    items = [media_item("item-a", payloads["koa-object://mediatheque/item-a"])]
    if two_items:
        items.append(media_item("item-b", payloads["koa-object://mediatheque/item-b"]))
    package = {
        "$schema": "https://schemas.koa.local/artifact-contracts/uckk-publication-package.schema.json",
        "package_id": "uckk_pub_pkg_contract_001",
        "package_version": "1.0.0",
        "created_at": "2026-08-06T14:50:00Z",
        "expires_at": "2026-09-01T00:00:00Z",
        "idempotency_key": "idem:uckk:contract:001",
        "source": {
            "system_id": "koa-linux",
            "component_id": "koa_mediatheque",
            "authority_domain_id": "authority://koa/local-mediatheque",
            "source_authority_preserved": True,
        },
        "target": {
            "system_id": "uckk",
            "platform_type": "moodle",
            "endpoint_id": "uckk-primary",
            "mapping_version": "1.0.0",
            "destination": {"site_ref": "site-main", "course_ref": "course-fixture"},
        },
        "authorization": {
            "publication_request_ref": "publication-request://fixture/1",
            "decision_ref": "decision://publication/allow/1",
            "decision_outcome": "allow",
            "authorized_at": "2026-08-06T14:45:00Z",
            "authorized_by_ref": "identity://publisher/fixture",
            "obligation_refs": ["obligation://minimum-necessary"],
        },
        "purpose": "contract conformance",
        "audience": "fixture learners",
        "items": items,
        "manifest": {
            "algorithm": "sha256",
            "digest": sha256(json.dumps(items, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
            "item_count": len(items),
            "total_size_bytes": sum(item["content"]["size_bytes"] for item in items),
        },
        "queue_policy": {
            "offline_queue_allowed": True,
            "maximum_attempts": 3,
            "retry_until": "2026-08-31T00:00:00Z",
            "cancel_on_authorization_change": True,
            "cancel_on_source_version_change": True,
        },
        "frame_compatibility": {
            "frame_id": "koa-uckk-shared-mediatheque-frame",
            "source_frame_version": "1.0.0",
            "target_frame_version": "1.0.0",
            "mapping_version": "1.0.0",
            "rights_preserved": True,
            "provenance_preserved": True,
            "review_required": False,
        },
    }
    return package, payloads


def make_service(
    *,
    package: Mapping[str, Any],
    payload_values: Mapping[str, bytes],
    moodle: FakeMoodle | None = None,
    authorization_current: bool = True,
    stale_item_ids: set[str] | None = None,
    manifest_valid: bool = True,
) -> tuple[PublicationService, FakeMoodle, WorkflowStore, QueuePort, ReceiptPort]:
    remote = moodle or FakeMoodle()
    workflows = WorkflowStore()
    queue = QueuePort()
    receipts = ReceiptPort()
    service = PublicationService(
        moodle=remote,
        package_schema=SchemaPort(),
        manifest_verifier=ManifestPort(manifest_valid),
        authorization=AuthorizationPort(authorization_current),
        source_authority=SourcePort(stale_item_ids),
        payloads=PayloadPort(payload_values),
        workflows=workflows,
        queue=queue,
        receipts=receipts,
        clock=FixedClock(),
        ids=SequenceIds(),
    )
    return service, remote, workflows, queue, receipts


def validate_receipt(receipt: Mapping[str, Any]) -> None:
    path = REPOSITORY_ROOT / "docs/contracts/artifact-contracts/uckk-publication-receipt.schema.json"
    Draft202012Validator(
        json.loads(path.read_text(encoding="utf-8")),
        format_checker=FormatChecker(),
    ).validate(receipt)


def validate_workflow(workflow: Mapping[str, Any]) -> None:
    path = REPOSITORY_ROOT / "docs/contracts/artifact-contracts/distributed-workflow.schema.json"
    Draft202012Validator(
        json.loads(path.read_text(encoding="utf-8")),
        format_checker=FormatChecker(),
    ).validate(workflow)


def test_successful_publication_produces_valid_receipt_and_workflow() -> None:
    package, payloads = publication_package(two_items=True)
    service, remote, workflows, queue, receipts = make_service(package=package, payload_values=payloads)

    receipt = service.publish(package, correlation_id="corr-publish-001")

    validate_receipt(receipt)
    stored = workflows.values[package["idempotency_key"]]
    validate_workflow(stored.workflow)
    assert receipt["outcome"] == "published"
    assert receipt["source_authority_preserved"] is True
    assert receipt["remote_authority_separate"] is True
    assert {item["outcome"] for item in receipt["item_results"]} == {"published"}
    assert stored.workflow["state"] == "completed"
    assert stored.workflow["evidence"]["terminal_receipt_ref"].startswith("receipt://")
    assert not queue.entries
    assert len(receipts.values) == 1
    assert ("receive_publication_receipt", package["idempotency_key"]) in remote.calls


def test_idempotent_replay_returns_recorded_receipt_without_remote_mutation() -> None:
    package, payloads = publication_package()
    service, remote, workflows, _, receipts = make_service(package=package, payload_values=payloads)
    first = service.publish(package, correlation_id="corr-first")
    call_count = len(remote.calls)

    second = service.publish(package, correlation_id="corr-replay")

    assert second == first
    assert len(remote.calls) == call_count
    assert len(receipts.values) == 1
    assert workflows.values[package["idempotency_key"]].receipt == first


def test_reusing_idempotency_key_with_different_package_is_rejected_without_overwrite() -> None:
    package, payloads = publication_package()
    service, remote, workflows, _, receipts = make_service(package=package, payload_values=payloads)
    service.publish(package, correlation_id="corr-original")
    original = workflows.values[package["idempotency_key"]]
    changed = deepcopy(package)
    changed["purpose"] = "different canonical body"

    receipt = service.publish(changed, correlation_id="corr-conflict")

    validate_receipt(receipt)
    assert receipt["outcome"] == "rejected"
    assert {item["failure_code"] for item in receipt["item_results"]} == {"IDEMPOTENCY_CONFLICT"}
    assert workflows.values[package["idempotency_key"]] == original
    assert len(receipts.values) == 2
    assert remote.calls.count(("authenticate", None)) == 1


def test_partial_publication_exposes_each_item_outcome_and_forward_repair() -> None:
    package, payloads = publication_package(two_items=True)
    remote = FakeMoodle()
    remote.fail_items["item-b"] = MoodleClientError(
        "DESTINATION_UNAVAILABLE",
        "destination unavailable",
        retryable=True,
    )
    service, _, workflows, queue, _ = make_service(
        package=package,
        payload_values=payloads,
        moodle=remote,
    )

    receipt = service.publish(package, correlation_id="corr-partial")

    validate_receipt(receipt)
    assert receipt["outcome"] == "partially_published"
    assert [item["outcome"] for item in receipt["item_results"]] == ["published", "failed"]
    assert workflows.values[package["idempotency_key"]].workflow["state"] == "forward_repair_required"
    assert not queue.entries


def test_offline_destination_creates_visible_queue_and_queued_receipt() -> None:
    package, payloads = publication_package()
    remote = FakeMoodle()
    remote.authenticate_error = MoodleClientError(
        "DESTINATION_UNAVAILABLE",
        "destination unavailable",
        retryable=True,
    )
    service, _, workflows, queue, receipts = make_service(
        package=package,
        payload_values=payloads,
        moodle=remote,
    )

    receipt = service.publish(package, correlation_id="corr-offline")

    validate_receipt(receipt)
    validate_workflow(workflows.values[package["idempotency_key"]].workflow)
    assert receipt["outcome"] == "queued"
    assert receipt["retry"]["retry_allowed"] is True
    assert queue.entries[0]["reason_code"] == "DESTINATION_UNAVAILABLE"
    assert queue.entries[0]["workflow"]["state"] == "waiting_remote"
    assert receipts.values[0]["evidence_refs"][0].startswith("queue://")


def test_expired_authorization_cancels_before_remote_access() -> None:
    package, payloads = publication_package()
    service, remote, workflows, _, _ = make_service(
        package=package,
        payload_values=payloads,
        authorization_current=False,
    )

    receipt = service.publish(package, correlation_id="corr-auth-expired")

    assert receipt["outcome"] == "cancelled"
    assert {item["failure_code"] for item in receipt["item_results"]} == {"AUTHORIZATION_EXPIRED"}
    assert workflows.values[package["idempotency_key"]].workflow["state"] == "cancelled"
    assert not remote.calls


def test_source_version_change_cancels_before_remote_access() -> None:
    package, payloads = publication_package()
    service, remote, _, _, _ = make_service(
        package=package,
        payload_values=payloads,
        stale_item_ids={"item-a"},
    )

    receipt = service.publish(package, correlation_id="corr-source-changed")

    assert receipt["outcome"] == "cancelled"
    assert receipt["item_results"][0]["failure_code"] == "SOURCE_VERSION_CHANGED"
    assert not remote.calls


def test_ambiguous_remote_result_requires_reconciliation_and_never_claims_success() -> None:
    package, payloads = publication_package()
    remote = FakeMoodle()
    remote.authenticate_error = MoodleClientError(
        "REMOTE_RESULT_AMBIGUOUS",
        "timeout",
        retryable=True,
        ambiguous=True,
    )
    service, _, workflows, _, _ = make_service(package=package, payload_values=payloads, moodle=remote)

    receipt = service.publish(package, correlation_id="corr-ambiguous")

    assert receipt["outcome"] == "unknown_reconciliation_required"
    assert receipt["retry"]["reconciliation_required"] is True
    assert workflows.values[package["idempotency_key"]].workflow["state"] == "human_intervention_required"
    assert receipt["item_results"][0]["outcome"] == "unknown"


def test_inline_content_and_changed_rights_fail_closed() -> None:
    package, payloads = publication_package()
    package["items"][0]["content"]["data"] = "inline-content"
    service, _, _, _, _ = make_service(package=package, payload_values=payloads)
    with pytest.raises(PublicationError, match="inline media payloads are prohibited"):
        service.publish(package, correlation_id="corr-inline")

    package, payloads = publication_package()
    package["items"][0]["rights_assertion"]["publication_allowed"] = False
    service, _, _, _, _ = make_service(package=package, payload_values=payloads)
    with pytest.raises(PublicationError, match="rights do not permit"):
        service.publish(package, correlation_id="corr-rights")


def test_manifest_verification_failure_stops_before_remote_access() -> None:
    package, payloads = publication_package()
    service, remote, _, _, _ = make_service(
        package=package,
        payload_values=payloads,
        manifest_valid=False,
    )
    with pytest.raises(PublicationError, match="manifest is invalid"):
        service.publish(package, correlation_id="corr-manifest")
    assert not remote.calls


def test_module_contains_no_inbound_sync_or_direct_database_implementation() -> None:
    source_root = REPOSITORY_ROOT / "integrations/uckk/adapter/src/koa_uckk_adapter"
    combined = "\n".join(
        (source_root / name).read_text(encoding="utf-8")
        for name in ("moodle_client.py", "publication.py")
    ).lower()
    prohibited = (
        "import_from_uckk",
        "bidirectional_sync",
        "direct_database_write",
        "sqlite3",
        "psycopg",
        "mysql.connector",
    )
    assert all(term not in combined for term in prohibited)
