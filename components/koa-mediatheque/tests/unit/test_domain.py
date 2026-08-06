from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta

import pytest

from koa_mediatheque.domain import (
    AcquisitionMethod,
    AiUse,
    Classification,
    Collection,
    ContentAvailability,
    ContentBinding,
    DigestAlgorithm,
    Dimension,
    Disclosure,
    ExternalPublicationOutcome,
    ExternalPublicationReference,
    Integrity,
    LicenseStatus,
    MediaRecord,
    OriginSystem,
    Provenance,
    Publication,
    RecordLifecycle,
    RecordState,
    Relationship,
    Rendition,
    Rights,
    SharedDisclosureStatus,
    SharedFrameMapping,
    SharedLifecycle,
    SharedLifecycleState,
    SharedMedia,
    SharedMediathequeFrame,
    SharedObjectIdentity,
    SharedProvenance,
    SharedRights,
    SharedVersionIdentity,
    SourceType,
    Tag,
    VersionState,
)

NOW = datetime(2026, 8, 6, 12, 0, tzinfo=UTC)
DIGEST_A = "a" * 64
DIGEST_B = "b" * 64


def _integrity(digest: str = DIGEST_A) -> Integrity:
    return Integrity(
        algorithm=DigestAlgorithm.SHA256,
        digest=digest,
        verified_at=NOW,
        verified_by="integrity-worker",
    )


def _classification() -> Classification:
    return Classification(
        collection_ids=("manuals",),
        dimension_ids=("repair",),
        tags=("offline", "practical"),
        relationships=(
            Relationship(
                relationship_type="supplements",
                target_record_id="koa_media_related",
            ),
        ),
    )


def _rights() -> Rights:
    return Rights(
        disclosure=Disclosure.ORGANIZATION,
        publication=Publication.ALLOWED_FOR_DECLARED_TARGETS,
        allowed_target_ids=("uckk-training",),
        ai_use=AiUse.METADATA_CANDIDATES_ONLY,
        consent_refs=("consent:42",),
        cultural_rights_refs=("culture:community-a",),
        license="CC-BY-NC-4.0",
        retention_class="operational_manual",
        restrictions=("no-commercial-redistribution",),
    )


def _shared_frame(
    *,
    record_id: str = "koa_media_manual_001",
    version_id: str = "koa_media_version_manual_001_v1",
    digest: str = DIGEST_A,
) -> SharedMediathequeFrame:
    classification = _classification()
    return SharedMediathequeFrame(
        frame_version="1.0.0",
        object_identity=SharedObjectIdentity(
            authority_domain_id="koa-local:node-a",
            object_id=record_id,
            origin_system=OriginSystem.KOA_LINUX,
            external_refs=("uckk:source:manual-77",),
        ),
        version_identity=SharedVersionIdentity(
            version_id=version_id,
            created_at=NOW,
            source_version_ref="uckk:version:3",
        ),
        integrity=Integrity(DigestAlgorithm.SHA256, digest),
        media=SharedMedia(
            media_type="application/pdf",
            title="Repair manual",
            language_tags=("en", "fr"),
            accessibility={"transcript": False, "page_count": 24},
            collections=classification.collection_ids,
            dimensions=classification.dimension_ids,
            tags=classification.tags,
            relationships=classification.relationships,
        ),
        rights=SharedRights(
            license_status=LicenseStatus.DECLARED,
            license_ref="CC-BY-NC-4.0",
            disclosure_status=SharedDisclosureStatus.ORGANIZATION_PRIVATE,
            consent_refs=("consent:42",),
            restriction_refs=("no-commercial-redistribution",),
            cultural_rights_refs=("culture:community-a",),
        ),
        provenance=SharedProvenance(
            source_system="uckk",
            acquisition_method=AcquisitionMethod.IMPORTED_OFFLINE_BUNDLE,
            source_object_ref="uckk:source:manual-77",
            source_version_ref="uckk:version:3",
            acquired_at=NOW,
            receipt_refs=("receipt:import:9",),
        ),
        lifecycle=SharedLifecycle(
            state=SharedLifecycleState.ACCEPTED,
            authority_domain_id="koa-local:node-a",
            transitioned_at=NOW,
            retention_policy_ref="retention:manuals",
        ),
        mapping=SharedFrameMapping(
            source_frame_version="1.0.0",
            target_frame_version="1.0.0",
            mapping_version="map-1",
            lossless=True,
            review_required=False,
        ),
    )


def _record(
    *,
    record_id: str = "koa_media_manual_001",
    version_id: str = "koa_media_version_manual_001_v1",
    digest: str = DIGEST_A,
) -> MediaRecord:
    integrity = _integrity(digest)
    return MediaRecord(
        shared_frame=_shared_frame(
            record_id=record_id,
            version_id=version_id,
            digest=digest,
        ),
        record_id=record_id,
        version_id=version_id,
        title="Repair manual",
        description="Offline equipment repair instructions.",
        media_type="application/pdf",
        content=ContentBinding(
            availability=ContentAvailability.MANAGED_LOCAL,
            storage_ref="content/sha256/aa/manual.pdf",
            size_bytes=2048,
            original_filename="manual.pdf",
        ),
        integrity=integrity,
        classification=_classification(),
        rights=_rights(),
        provenance=Provenance(
            source_type=SourceType.IMPORTED,
            source_ref="uckk:source:manual-77",
            acquired_at=NOW,
            creator_refs=("person:author",),
            custodian_ref="organization:maintenance",
            evidence_refs=("receipt:import:9",),
        ),
        lifecycle=RecordLifecycle(
            record_state=RecordState.ACTIVE,
            version_state=VersionState.ACCEPTED,
            created_at=NOW,
            updated_at=NOW,
        ),
        external_publications=(
            ExternalPublicationReference(
                target_system="uckk",
                package_id="package:22",
                receipt_ref="receipt:publish:22",
                outcome=ExternalPublicationOutcome.PUBLISHED,
                remote_object_refs=("uckk:media:991",),
            ),
        ),
    )


def test_classification_entities_build_deterministic_references() -> None:
    classification = Classification.from_entities(
        collections=(Collection("manuals", "Manuals"),),
        dimensions=(Dimension("repair", "Repair"),),
        tags=(Tag("practical"), Tag("offline")),
        relationships=(Relationship("supplements", "koa_media_related"),),
    )

    assert classification.collection_ids == ("manuals",)
    assert classification.dimension_ids == ("repair",)
    assert classification.tags == ("offline", "practical")
    assert classification.to_dict()["relationships"] == [
        {
            "relationship_type": "supplements",
            "target_record_id": "koa_media_related",
        }
    ]


def test_classification_rejects_duplicate_normalized_values() -> None:
    with pytest.raises(ValueError, match="duplicate"):
        Classification(tags=("offline", "offline"))


def test_rights_require_declared_targets_only_for_target_bounded_publication() -> None:
    with pytest.raises(ValueError, match="requires at least one"):
        Rights(
            disclosure=Disclosure.PRIVATE,
            publication=Publication.ALLOWED_FOR_DECLARED_TARGETS,
            ai_use=AiUse.PROHIBITED,
        )

    with pytest.raises(ValueError, match="valid only"):
        Rights(
            disclosure=Disclosure.PRIVATE,
            publication=Publication.PROHIBITED,
            allowed_target_ids=("uckk",),
            ai_use=AiUse.PROHIBITED,
        )


def test_rights_embargo_is_a_time_fact_not_an_authorization() -> None:
    rights = Rights(
        disclosure=Disclosure.RESTRICTED,
        publication=Publication.REVIEW_REQUIRED,
        ai_use=AiUse.PROHIBITED,
        embargo_until=NOW + timedelta(days=1),
    )

    assert rights.is_embargoed(NOW)
    assert not rights.is_embargoed(NOW + timedelta(days=2))


def test_provenance_requires_external_source_reference() -> None:
    with pytest.raises(ValueError, match="requires source_ref"):
        Provenance(source_type=SourceType.IMPORTED, acquired_at=NOW)


def test_derived_provenance_requires_lineage() -> None:
    with pytest.raises(ValueError, match="derivation_ref"):
        Provenance(
            source_type=SourceType.DERIVED,
            source_ref="koa_media_source",
            acquired_at=NOW,
        )


def test_integrity_enforces_algorithm_specific_lowercase_digest() -> None:
    with pytest.raises(ValueError, match="64"):
        Integrity(DigestAlgorithm.SHA256, "a" * 96)
    with pytest.raises(ValueError, match="lowercase"):
        Integrity(DigestAlgorithm.SHA256, "A" * 64)


def test_stored_rendition_requires_verified_integrity() -> None:
    with pytest.raises(ValueError, match="verified integrity"):
        Rendition(
            rendition_id="preview-1",
            kind="preview",
            version_id="koa_media_version_manual_001_v1",
            integrity=Integrity(DigestAlgorithm.SHA256, DIGEST_A),
            storage_ref="renditions/preview.pdf",
        )


def test_shared_frame_rejects_authority_domain_mismatch() -> None:
    with pytest.raises(ValueError, match="same authority domain"):
        SharedMediathequeFrame(
            frame_version="1.0.0",
            object_identity=SharedObjectIdentity("koa-local:a", "object-1"),
            version_identity=SharedVersionIdentity("version-1"),
            integrity=Integrity(DigestAlgorithm.SHA256, DIGEST_A),
            media=SharedMedia(media_type="application/pdf"),
            rights=SharedRights(LicenseStatus.UNKNOWN, SharedDisclosureStatus.PRIVATE),
            provenance=SharedProvenance("local", AcquisitionMethod.CREATED_LOCAL),
            lifecycle=SharedLifecycle(SharedLifecycleState.CANDIDATE, "koa-local:b"),
        )


def test_lossy_shared_frame_mapping_requires_review() -> None:
    with pytest.raises(ValueError, match="requires explicit review"):
        SharedFrameMapping(lossless=False, review_required=False, unmapped_fields=("rights",))


def test_media_record_serializes_to_canonical_schema_shape() -> None:
    serialized = _record().to_dict()

    assert set(serialized) == {
        "shared_frame",
        "record_id",
        "version_id",
        "title",
        "description",
        "media_type",
        "content",
        "integrity",
        "classification",
        "rights",
        "provenance",
        "lifecycle",
        "external_publications",
    }
    assert serialized["record_id"] == "koa_media_manual_001"
    assert serialized["integrity"] == {
        "algorithm": "sha256",
        "digest": DIGEST_A,
        "verified_at": "2026-08-06T12:00:00Z",
        "verified_by": "integrity-worker",
    }
    assert serialized["shared_frame"]["frame_id"] == "koa-uckk-shared-mediatheque-frame"
    assert serialized["shared_frame"]["object_identity"]["object_id"] == serialized["record_id"]


def test_media_record_rejects_noncanonical_local_identifiers() -> None:
    with pytest.raises(ValueError, match="record_id"):
        _record(record_id="uckk:manual:1")


def test_media_record_rejects_shared_identity_or_integrity_drift() -> None:
    record = _record()
    with pytest.raises(ValueError, match="object_id"):
        MediaRecord(
            shared_frame=_shared_frame(record_id="koa_media_other"),
            record_id=record.record_id,
            version_id=record.version_id,
            title=record.title,
            media_type=record.media_type,
            content=record.content,
            integrity=record.integrity,
            classification=record.classification,
            rights=record.rights,
            provenance=record.provenance,
            lifecycle=record.lifecycle,
        )

    with pytest.raises(ValueError, match="digests"):
        MediaRecord(
            shared_frame=_shared_frame(digest=DIGEST_B),
            record_id=record.record_id,
            version_id=record.version_id,
            title=record.title,
            media_type=record.media_type,
            content=record.content,
            integrity=record.integrity,
            classification=record.classification,
            rights=record.rights,
            provenance=record.provenance,
            lifecycle=record.lifecycle,
        )


def test_media_record_rejects_lossy_rights_mapping() -> None:
    frame = _shared_frame()
    incompatible_frame = SharedMediathequeFrame(
        frame_version=frame.frame_version,
        object_identity=frame.object_identity,
        version_identity=frame.version_identity,
        integrity=frame.integrity,
        media=frame.media,
        rights=SharedRights(
            license_status=LicenseStatus.DECLARED,
            disclosure_status=SharedDisclosureStatus.PUBLIC,
        ),
        provenance=frame.provenance,
        lifecycle=frame.lifecycle,
        mapping=frame.mapping,
    )
    record = _record()

    with pytest.raises(ValueError, match="disclosure_status"):
        MediaRecord(
            shared_frame=incompatible_frame,
            record_id=record.record_id,
            version_id=record.version_id,
            title=record.title,
            media_type=record.media_type,
            content=record.content,
            integrity=record.integrity,
            classification=record.classification,
            rights=record.rights,
            provenance=record.provenance,
            lifecycle=record.lifecycle,
        )


def test_withdrawn_lifecycle_requires_evidence_reference() -> None:
    with pytest.raises(ValueError, match="withdrawal_ref"):
        RecordLifecycle(
            record_state=RecordState.WITHDRAWN,
            version_state=VersionState.WITHDRAWN,
            created_at=NOW,
            updated_at=NOW,
        )


def test_corrupt_version_cannot_remain_active() -> None:
    record = _record()
    with pytest.raises(ValueError, match="corrupt"):
        MediaRecord(
            shared_frame=record.shared_frame,
            record_id=record.record_id,
            version_id=record.version_id,
            title=record.title,
            media_type=record.media_type,
            content=record.content,
            integrity=record.integrity,
            classification=record.classification,
            rights=record.rights,
            provenance=record.provenance,
            lifecycle=RecordLifecycle(
                record_state=RecordState.ACTIVE,
                version_state=VersionState.CORRUPT,
                created_at=NOW,
                updated_at=NOW,
            ),
        )


def test_equal_bytes_do_not_merge_record_identity_or_authority() -> None:
    first = _record()
    second = _record(
        record_id="koa_media_manual_002",
        version_id="koa_media_version_manual_002_v1",
    )

    assert first.has_same_bytes_as(second)
    assert first != second
    assert first.record_id != second.record_id


def test_domain_objects_are_immutable_and_nested_json_is_defensively_frozen() -> None:
    frame = _shared_frame()
    with pytest.raises(FrozenInstanceError):
        frame.frame_version = "2.0.0"  # type: ignore[misc]

    source = {"features": ["captions"]}
    media = SharedMedia(media_type="video/mp4", accessibility=source)
    source["features"].append("audio-description")
    assert media.to_dict()["accessibility"] == {"features": ["captions"]}


def test_local_frame_origin_cannot_be_replaced_by_uckk_identity() -> None:
    frame = _shared_frame()
    uckk_identity = SharedObjectIdentity(
        authority_domain_id=frame.object_identity.authority_domain_id,
        object_id=frame.object_identity.object_id,
        origin_system=OriginSystem.UCKK,
    )
    uckk_frame = SharedMediathequeFrame(
        frame_version=frame.frame_version,
        object_identity=uckk_identity,
        version_identity=frame.version_identity,
        integrity=frame.integrity,
        media=frame.media,
        rights=frame.rights,
        provenance=frame.provenance,
        lifecycle=frame.lifecycle,
        mapping=frame.mapping,
    )
    record = _record()

    with pytest.raises(ValueError, match="kOA-Linux origin"):
        MediaRecord(
            shared_frame=uckk_frame,
            record_id=record.record_id,
            version_id=record.version_id,
            title=record.title,
            media_type=record.media_type,
            content=record.content,
            integrity=record.integrity,
            classification=record.classification,
            rights=record.rights,
            provenance=record.provenance,
            lifecycle=record.lifecycle,
        )
