from __future__ import annotations

import hashlib
import sys
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Mapping

import pytest

SRC = Path(__file__).resolve().parents[3] / "src"
sys.path.insert(0, str(SRC))

from koa_mediatheque.application import (  # noqa: E402
    BuildRendition,
    BuildRenditionRequest,
    DeleteMedia,
    DeleteMediaRequest,
    ExportMedia,
    ExportMediaRequest,
    IngestMedia,
    IngestMediaRequest,
    UpdateMetadata,
    UpdateMetadataRequest,
    VerifyIntegrity,
    VerifyIntegrityRequest,
    stable_identifier,
)
from koa_mediatheque.ports import (  # noqa: E402
    AuditEvent,
    BlobDescriptor,
    EvidenceReceipt,
    ExportHistoryEntry,
    IngestCommit,
    Integrity,
    IntegrityTransition,
    JobRequest,
    JobSubmission,
    MediaRecord,
    MediaVersion,
    MetadataRevision,
    RenditionRequestRecord,
    RightsDecision,
    RightsRequest,
    StagedBlob,
    TombstoneResult,
)

NOW = datetime(2026, 8, 6, 15, 0, tzinfo=timezone.utc)


class FixedClock:
    def __init__(self, now: datetime = NOW) -> None:
        self.value = now

    def now(self) -> datetime:
        return self.value


class MemoryAudit:
    def __init__(self) -> None:
        self.events: list[AuditEvent] = []
        self.receipts: list[EvidenceReceipt] = []

    def emit(self, event: AuditEvent) -> None:
        self.events.append(event)

    def record_receipt(self, receipt: EvidenceReceipt) -> None:
        self.receipts.append(receipt)


class StubRights:
    def __init__(self, decision: RightsDecision | None = None) -> None:
        self.decision = decision or RightsDecision(
            "decision-1",
            "allowed",
            "policy_allowed",
            NOW,
            ("policy-receipt-1",),
            ("title", "description"),
            1_000_000,
            NOW + timedelta(hours=1),
        )
        self.requests: list[RightsRequest] = []

    def evaluate(self, request: RightsRequest) -> RightsDecision:
        self.requests.append(request)
        return self.decision


class MemoryQueue:
    def __init__(self, outcome: str = "queued") -> None:
        self.outcome = outcome
        self.requests: list[JobRequest] = []

    def enqueue(self, request: JobRequest) -> JobSubmission:
        self.requests.append(request)
        queue_ref = f"queue:{request.job_id}" if self.outcome in {"queued", "already_queued"} else None
        return JobSubmission(self.outcome, queue_ref, f"queue_{self.outcome}")


class MemoryBlobs:
    def __init__(self) -> None:
        self.staged: dict[str, tuple[bytes, str]] = {}
        self.managed: dict[str, tuple[bytes, str]] = {}
        self.stage_calls = 0
        self.digest_calls = 0
        self.fail_delete: set[str] = set()
        self.describe_override: BlobDescriptor | None = None

    def stage(self, content: bytes, media_type: str, *, staging_key: str) -> StagedBlob:
        self.stage_calls += 1
        ref = f"staged:{staging_key}"
        self.staged[ref] = (bytes(content), media_type)
        return StagedBlob(ref, media_type, len(content))

    def calculate_digest(self, blob_ref: str, algorithm: str) -> str:
        self.digest_calls += 1
        if blob_ref in self.staged:
            content = self.staged[blob_ref][0]
        else:
            content = self.managed[blob_ref][0]
        return hashlib.new(algorithm, content).hexdigest()

    def commit(self, staging_ref: str, *, blob_key: str) -> BlobDescriptor:
        content, media_type = self.staged.pop(staging_ref)
        ref = f"blob:{blob_key}"
        self.managed[ref] = (content, media_type)
        return BlobDescriptor(ref, media_type, len(content))

    def discard_staged(self, staging_ref: str) -> None:
        self.staged.pop(staging_ref, None)

    def describe(self, blob_ref: str) -> BlobDescriptor:
        if self.describe_override is not None:
            return self.describe_override
        content, media_type = self.managed[blob_ref]
        return BlobDescriptor(blob_ref, media_type, len(content))

    def delete(self, blob_ref: str) -> None:
        if blob_ref in self.fail_delete:
            raise OSError("simulated deletion failure")
        self.managed.pop(blob_ref, None)
        self.staged.pop(blob_ref, None)


class MemoryRecords:
    def __init__(self) -> None:
        self.records: dict[str, MediaRecord] = {}
        self.versions: dict[tuple[str, str], MediaVersion] = {}
        self.idempotency: dict[tuple[str, str], object] = {}
        self.rendition_requests: dict[str, RenditionRequestRecord] = {}
        self.rendition_queue_refs: dict[str, str] = {}
        self.exports: list[ExportHistoryEntry] = []
        self.fail_ingest = False
        self.tombstones: list[str] = []

    def get_idempotent_result(self, operation: str, idempotency_key: str) -> object | None:
        return self.idempotency.get((operation, idempotency_key))

    def remember_idempotent_result(self, operation: str, idempotency_key: str, result: object) -> None:
        self.idempotency[(operation, idempotency_key)] = result

    def find_versions_by_integrity(self, integrity: Integrity) -> tuple[str, ...]:
        return tuple(sorted(version.version_id for version in self.versions.values() if version.integrity == integrity))

    def commit_ingest(self, commit: IngestCommit) -> tuple[MediaRecord, MediaVersion]:
        if self.fail_ingest:
            raise RuntimeError("simulated authoritative-store failure")
        if commit.record.record_id in self.records:
            raise ValueError("record identity already exists")
        self.records[commit.record.record_id] = commit.record
        self.versions[(commit.record.record_id, commit.version.version_id)] = commit.version
        return commit.record, commit.version

    def get_record(self, record_id: str) -> MediaRecord | None:
        return self.records.get(record_id)

    def get_version(self, record_id: str, version_id: str) -> MediaVersion | None:
        return self.versions.get((record_id, version_id))

    def commit_metadata_revision(self, revision: MetadataRevision) -> MediaVersion:
        source = self.versions[(revision.record_id, revision.source_version_id)]
        version = replace(
            source,
            version_id=revision.new_version_id,
            metadata=revision.metadata,
            created_at=revision.changed_at,
        )
        self.versions[(revision.record_id, version.version_id)] = version
        record = self.records[revision.record_id]
        self.records[revision.record_id] = replace(record, current_version_id=version.version_id, updated_at=revision.changed_at)
        return version

    def record_rendition_request(self, request: RenditionRequestRecord) -> None:
        self.rendition_requests[request.rendition_id] = request

    def attach_rendition_queue_ref(self, rendition_id: str, queue_ref: str) -> None:
        self.rendition_queue_refs[rendition_id] = queue_ref

    def record_export_candidate(self, entry: ExportHistoryEntry) -> None:
        self.exports.append(entry)

    def apply_integrity_transition(self, transition: IntegrityTransition) -> MediaVersion:
        current = self.versions[(transition.record_id, transition.version_id)]
        updated = replace(
            current,
            integrity_state=transition.new_integrity_state,
            state=transition.new_version_state,
        )
        self.versions[(transition.record_id, transition.version_id)] = updated
        return updated

    def tombstone_record(self, record_id: str, *, actor_id: str, reason: str, at: datetime) -> TombstoneResult:
        record = self.records[record_id]
        self.records[record_id] = replace(record, state="deleted_tombstone", updated_at=at)
        related = [version for (owner, _), version in self.versions.items() if owner == record_id]
        for version in related:
            self.versions[(record_id, version.version_id)] = replace(version, state="withdrawn")
        self.tombstones.append(record_id)
        return TombstoneResult(
            record_id,
            tuple(version.version_id for version in related),
            tuple(dict.fromkeys(version.blob_ref for version in related)),
            ("publication-receipt-1", "audit-receipt-1"),
        )


class World:
    def __init__(self, rights: RightsDecision | None = None, queue_outcome: str = "queued") -> None:
        self.clock = FixedClock()
        self.audit = MemoryAudit()
        self.rights = StubRights(rights)
        self.jobs = MemoryQueue(queue_outcome)
        self.blobs = MemoryBlobs()
        self.records = MemoryRecords()

    def ingest(self, *, key: str = "ingest-1", content: bytes = b"hello", declared: str | None = None,
               record_id: str | None = None) -> object:
        return IngestMedia(self.records, self.blobs, self.rights, self.audit, self.clock).execute(
            IngestMediaRequest(
                key,
                "actor-1",
                "koa-local",
                content,
                "text/plain",
                {"title": "Manual", "description": "Local copy", "secret": "restricted"},
                {"source_system": "koa-linux", "acquisition_method": "created_local"},
                record_id=record_id,
                declared_digest=declared,
            )
        )


def denied_decision() -> RightsDecision:
    return RightsDecision("decision-denied", "denied", "policy_denied", NOW, ("policy-denial-1",))


def indeterminate_decision() -> RightsDecision:
    return RightsDecision("decision-indeterminate", "indeterminate", "policy_unavailable", NOW, ("policy-error-1",))


def expired_decision() -> RightsDecision:
    return RightsDecision(
        "decision-expired", "allowed", "policy_allowed", NOW - timedelta(hours=2),
        ("policy-receipt-old",), ("title",), 1000, NOW - timedelta(hours=1),
    )


def test_stable_identifier_is_deterministic_and_scoped() -> None:
    assert stable_identifier("media", "a", "b") == stable_identifier("media", "a", "b")
    assert stable_identifier("media", "a", "b") != stable_identifier("version", "a", "b")


def test_integrity_rejects_malformed_digest() -> None:
    with pytest.raises(ValueError, match="invalid sha256 digest"):
        Integrity("sha256", "abc")


def test_ingest_request_rejects_empty_content() -> None:
    with pytest.raises(ValueError, match="content"):
        IngestMediaRequest("key", "actor", "koa", b"", "text/plain", {}, {})


def test_ingest_accepts_verified_content_and_emits_evidence() -> None:
    world = World()
    result = world.ingest()
    assert result.outcome == "accepted"
    version = world.records.get_version(result.record_id, result.version_id)
    assert version is not None and version.state == "accepted" and version.integrity_state == "verified"
    assert world.audit.receipts[-1].receipt_type == "media_ingest"
    assert world.audit.events[-1].event_type == "media_record_created"


def test_ingest_is_idempotent_without_restaging_bytes() -> None:
    world = World()
    first = world.ingest()
    second = world.ingest()
    assert second == first
    assert world.blobs.stage_calls == 1
    assert len(world.records.records) == 1


def test_duplicate_bytes_do_not_merge_record_identity() -> None:
    world = World()
    first = world.ingest(key="one", record_id="record-one")
    second = world.ingest(key="two", record_id="record-two")
    assert first.record_id != second.record_id
    assert second.duplicate_version_refs == (first.version_id,)
    assert len(world.records.records) == 2


def test_declared_integrity_mismatch_is_quarantined() -> None:
    world = World()
    result = world.ingest(declared="0" * 64)
    version = world.records.get_version(result.record_id, result.version_id)
    assert result.outcome == "quarantined"
    assert version is not None and version.state == "quarantined" and version.integrity_state == "failed"
    assert world.audit.receipts[-1].outcome == "failed"


@pytest.mark.parametrize("decision,outcome", [(denied_decision(), "denied"), (indeterminate_decision(), "indeterminate"), (expired_decision(), "denied")])
def test_ingest_fails_closed_before_staging(decision: RightsDecision, outcome: str) -> None:
    world = World(decision)
    result = world.ingest()
    assert result.outcome == outcome
    assert world.blobs.stage_calls == 0
    assert not world.records.records


def test_ingest_compensates_managed_blob_when_record_commit_fails() -> None:
    world = World()
    world.records.fail_ingest = True
    with pytest.raises(RuntimeError, match="authoritative-store"):
        world.ingest()
    assert world.blobs.managed == {}
    assert world.blobs.staged == {}


def test_metadata_update_creates_new_version_and_preserves_source() -> None:
    world = World()
    ingested = world.ingest()
    result = UpdateMetadata(world.records, world.rights, world.audit, world.clock).execute(
        UpdateMetadataRequest("meta-1", "actor-1", ingested.record_id, ingested.version_id, {"title": "Revised"})
    )
    assert result.outcome == "updated"
    assert result.version_id != ingested.version_id
    assert world.records.get_version(ingested.record_id, ingested.version_id).metadata["title"] == "Manual"
    assert world.records.get_version(ingested.record_id, result.version_id).metadata["title"] == "Revised"


def test_metadata_update_requires_exact_existing_version() -> None:
    world = World()
    with pytest.raises(LookupError, match="source media version"):
        UpdateMetadata(world.records, world.rights, world.audit, world.clock).execute(
            UpdateMetadataRequest("meta", "actor", "missing", "version", {"title": "x"})
        )


def test_metadata_update_rejects_nonaccepted_source() -> None:
    world = World()
    result = world.ingest(declared="0" * 64)
    with pytest.raises(ValueError, match="accepted, verified"):
        UpdateMetadata(world.records, world.rights, world.audit, world.clock).execute(
            UpdateMetadataRequest("meta", "actor", result.record_id, result.version_id, {"title": "x"})
        )


def test_metadata_update_denied_does_not_create_version() -> None:
    world = World()
    ingested = world.ingest()
    world.rights.decision = denied_decision()
    result = UpdateMetadata(world.records, world.rights, world.audit, world.clock).execute(
        UpdateMetadataRequest("meta-denied", "actor", ingested.record_id, ingested.version_id, {"title": "x"})
    )
    assert result.outcome == "denied"
    assert len(world.records.versions) == 1


@pytest.mark.parametrize("queue_outcome", ["queued", "already_queued", "deferred", "rejected"])
def test_rendition_queue_outcomes_are_explicit(queue_outcome: str) -> None:
    world = World(queue_outcome=queue_outcome)
    ingested = world.ingest()
    result = BuildRendition(world.records, world.rights, world.jobs, world.audit, world.clock).execute(
        BuildRenditionRequest("rendition-1", "actor", ingested.record_id, ingested.version_id,
                              "thumbnail", {"width": 320, "height": 180})
    )
    assert result.outcome == queue_outcome
    assert result.rendition_id in world.records.rendition_requests
    if queue_outcome in {"queued", "already_queued"}:
        assert result.rendition_id in world.records.rendition_queue_refs
    else:
        assert result.rendition_id not in world.records.rendition_queue_refs


def test_rendition_denied_never_enqueues() -> None:
    world = World()
    ingested = world.ingest()
    world.rights.decision = denied_decision()
    result = BuildRendition(world.records, world.rights, world.jobs, world.audit, world.clock).execute(
        BuildRenditionRequest("rendition-denied", "actor", ingested.record_id, ingested.version_id,
                              "preview", {"seconds": 10})
    )
    assert result.outcome == "denied"
    assert world.jobs.requests == []


def test_rendition_rejects_unverified_source() -> None:
    world = World()
    ingested = world.ingest(declared="0" * 64)
    with pytest.raises(ValueError, match="accepted, verified"):
        BuildRendition(world.records, world.rights, world.jobs, world.audit, world.clock).execute(
            BuildRenditionRequest("rendition", "actor", ingested.record_id, ingested.version_id,
                                  "thumbnail", {"width": 10})
        )


def test_export_creates_selective_candidate_without_publication_authority() -> None:
    world = World()
    ingested = world.ingest()
    result = ExportMedia(world.records, world.blobs, world.rights, world.audit, world.clock).execute(
        ExportMediaRequest("export-1", "actor", ingested.record_id, ingested.version_id,
                           "training", "team-a", "uckk", ("title", "secret", "description"))
    )
    assert result.outcome == "candidate_created"
    assert dict(result.candidate.metadata) == {"description": "Local copy", "title": "Manual"}
    assert result.reason_code == "publication_authorization_still_required"
    assert world.records.exports[-1].state == "candidate"
    assert world.records.exports[-1].destination == "uckk"


@pytest.mark.parametrize("decision,outcome", [(denied_decision(), "denied"), (indeterminate_decision(), "indeterminate"), (expired_decision(), "denied")])
def test_export_fails_closed_on_rights(decision: RightsDecision, outcome: str) -> None:
    world = World()
    ingested = world.ingest()
    world.rights.decision = decision
    result = ExportMedia(world.records, world.blobs, world.rights, world.audit, world.clock).execute(
        ExportMediaRequest("export-closed", "actor", ingested.record_id, ingested.version_id,
                           "training", "team", "uckk", ("title",))
    )
    assert result.outcome == outcome
    assert result.candidate is None
    assert world.records.exports == []


def test_export_respects_content_size_bound() -> None:
    world = World()
    ingested = world.ingest(content=b"123456")
    world.rights.decision = RightsDecision(
        "decision-small", "allowed", "policy_allowed", NOW, ("policy-1",), ("title",), 3, NOW + timedelta(hours=1)
    )
    result = ExportMedia(world.records, world.blobs, world.rights, world.audit, world.clock).execute(
        ExportMediaRequest("export-size", "actor", ingested.record_id, ingested.version_id,
                           "training", "team", "uckk", ("title",))
    )
    assert result.outcome == "denied"
    assert result.reason_code == "content_exceeds_rights_bound"


def test_export_rejects_withdrawn_record() -> None:
    world = World()
    ingested = world.ingest()
    world.records.records[ingested.record_id] = replace(world.records.records[ingested.record_id], state="withdrawn")
    with pytest.raises(ValueError, match="lifecycle"):
        ExportMedia(world.records, world.blobs, world.rights, world.audit, world.clock).execute(
            ExportMediaRequest("export-withdrawn", "actor", ingested.record_id, ingested.version_id,
                               "training", "team", "uckk")
        )


def test_export_detects_blob_descriptor_drift() -> None:
    world = World()
    ingested = world.ingest()
    version = world.records.get_version(ingested.record_id, ingested.version_id)
    world.blobs.describe_override = BlobDescriptor(version.blob_ref, "application/octet-stream", version.size_bytes)
    with pytest.raises(RuntimeError, match="does not match"):
        ExportMedia(world.records, world.blobs, world.rights, world.audit, world.clock).execute(
            ExportMediaRequest("export-drift", "actor", ingested.record_id, ingested.version_id,
                               "training", "team", "uckk")
        )


def test_verify_integrity_accepts_matching_managed_content() -> None:
    world = World()
    ingested = world.ingest()
    result = VerifyIntegrity(world.records, world.blobs, world.audit, world.clock).execute(
        VerifyIntegrityRequest("verify-1", "actor", ingested.record_id, ingested.version_id)
    )
    assert result.outcome == "verified"
    assert result.version_state == "accepted"
    assert world.audit.events[-1].event_type == "integrity_verified"


def test_verify_integrity_marks_corrupt_on_mismatch() -> None:
    world = World()
    ingested = world.ingest()
    version = world.records.get_version(ingested.record_id, ingested.version_id)
    world.blobs.managed[version.blob_ref] = (b"tampered", version.media_type)
    result = VerifyIntegrity(world.records, world.blobs, world.audit, world.clock).execute(
        VerifyIntegrityRequest("verify-corrupt", "actor", ingested.record_id, ingested.version_id)
    )
    assert result.outcome == "failed"
    assert result.version_state == "corrupt"
    assert world.audit.events[-1].event_type == "integrity_failure_detected"


def test_verify_integrity_is_idempotent() -> None:
    world = World()
    ingested = world.ingest()
    app = VerifyIntegrity(world.records, world.blobs, world.audit, world.clock)
    first = app.execute(VerifyIntegrityRequest("verify-idem", "actor", ingested.record_id, ingested.version_id))
    calls = world.blobs.digest_calls
    second = app.execute(VerifyIntegrityRequest("verify-idem", "actor", ingested.record_id, ingested.version_id))
    assert second == first
    assert world.blobs.digest_calls == calls


def test_delete_tombstones_and_preserves_evidence() -> None:
    world = World()
    ingested = world.ingest()
    result = DeleteMedia(world.records, world.blobs, world.rights, world.audit, world.clock).execute(
        DeleteMediaRequest("delete-1", "actor", ingested.record_id, "retention_expired")
    )
    assert result.outcome == "tombstoned"
    assert world.records.get_record(ingested.record_id).state == "deleted_tombstone"
    assert result.preserved_evidence_refs == ("publication-receipt-1", "audit-receipt-1")
    assert world.blobs.managed


def test_delete_purges_only_store_declared_unreferenced_blobs() -> None:
    world = World()
    ingested = world.ingest()
    version = world.records.get_version(ingested.record_id, ingested.version_id)
    result = DeleteMedia(world.records, world.blobs, world.rights, world.audit, world.clock).execute(
        DeleteMediaRequest("delete-purge", "actor", ingested.record_id, "owner_request", purge_unreferenced_content=True)
    )
    assert result.outcome == "tombstoned"
    assert result.deleted_blob_refs == (version.blob_ref,)
    assert version.blob_ref not in world.blobs.managed


def test_delete_reports_cleanup_pending_instead_of_false_success() -> None:
    world = World()
    ingested = world.ingest()
    version = world.records.get_version(ingested.record_id, ingested.version_id)
    world.blobs.fail_delete.add(version.blob_ref)
    result = DeleteMedia(world.records, world.blobs, world.rights, world.audit, world.clock).execute(
        DeleteMediaRequest("delete-fail", "actor", ingested.record_id, "owner_request", purge_unreferenced_content=True)
    )
    assert result.outcome == "tombstoned_cleanup_pending"
    assert result.cleanup_pending_refs == (version.blob_ref,)
    assert world.audit.receipts[-1].outcome == "failed"


def test_delete_denied_preserves_record_and_content() -> None:
    world = World()
    ingested = world.ingest()
    world.rights.decision = denied_decision()
    result = DeleteMedia(world.records, world.blobs, world.rights, world.audit, world.clock).execute(
        DeleteMediaRequest("delete-denied", "actor", ingested.record_id, "request")
    )
    assert result.outcome == "denied"
    assert world.records.get_record(ingested.record_id).state == "active"
    assert world.blobs.managed


def test_rights_context_contains_no_media_bytes() -> None:
    world = World()
    ingested = world.ingest()
    ExportMedia(world.records, world.blobs, world.rights, world.audit, world.clock).execute(
        ExportMediaRequest("export-context", "actor", ingested.record_id, ingested.version_id,
                           "training", "team", "uckk", ("title",))
    )
    request = world.rights.requests[-1]
    assert all(isinstance(value, str) for value in request.context.values())
    assert "content" not in request.context


def test_audit_surfaces_are_redacted() -> None:
    world = World()
    world.ingest()
    serialized = repr(world.audit.events[-1]) + repr(world.audit.receipts[-1])
    assert "hello" not in serialized
    assert "restricted" not in serialized
    assert "secret" not in serialized
