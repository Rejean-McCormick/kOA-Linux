from __future__ import annotations

import sys
from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timezone
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[2] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from koa_kristal_runtime.domain import (  # noqa: E402
    ArtifactClass,
    ArtifactCompatibility,
    ArtifactLocator,
    ArtifactProvenance,
    ArtifactRights,
    ContentIdentity,
    DisclosureVisibility,
    DomainValidationError,
    KristalArtifact,
    KristalManifestEntry,
    QueryContract,
    QueryFailure,
    QueryPage,
    QueryRequest,
    QueryResultItem,
    ReaderPolicy,
    ReaderRecord,
    RejectionCondition,
    ResourceLimits,
    RuntimePack,
    RuntimePackCompatibility,
    RuntimePackLifecycle,
    RuntimePackManifest,
    RuntimePackManifestEntry,
    VerificationCheck,
    VerificationFinding,
    VerificationOutcome,
    VerificationRecord,
)

UTC = timezone.utc
T0 = datetime(2026, 8, 6, 14, 0, tzinfo=UTC)
HEX_A = "a" * 64
HEX_B = "b" * 64
DIGEST_A = f"sha256:{HEX_A}"
DIGEST_B = f"sha256:{HEX_B}"


def make_kristal_artifact(content: bytes = b"canonical epistemic content") -> KristalArtifact:
    return KristalArtifact(
        artifact_id="kristal-artifact.reference.botany",
        artifact_version="2026.08",
        content_identity=ContentIdentity.from_canonical_content(content),
        manifest_entries=(
            KristalManifestEntry("claims/main.json", HEX_B),
            KristalManifestEntry("indexes/by-id.json", HEX_A),
        ),
        query_contract_refs=("query-contract.kristal.reference",),
        provenance=ArtifactProvenance(
            source_refs=("source:field-notes",),
            producer="SemantiK Architect",
            build_receipt_ref="receipt:kristal-build-1",
        ),
        rights=ArtifactRights(
            license="CC-BY-4.0",
            audiences=("audience:public",),
        ),
        compatibility=ArtifactCompatibility(
            kristal_runtime=">=1.0.0,<2.0.0",
            schema_versions=("1.0.0",),
            profile_constraints=("sovereign_offline",),
        ),
        signature_refs=("signature:publisher-1",),
        metadata={"language": "en", "reviewed": True},
    )


def make_manifest() -> RuntimePackManifest:
    return RuntimePackManifest(
        manifest_version="1.0.0",
        manifest_digest=DIGEST_A,
        entries=(
            RuntimePackManifestEntry(
                path="indexes/by-id.json",
                role="query_index",
                media_type="application/json",
                digest=DIGEST_B,
                size_bytes=100,
                required=True,
                depends_on_paths=("content/claims.json",),
                load_order=20,
            ),
            RuntimePackManifestEntry(
                path="content/claims.json",
                role="epistemic_content",
                media_type="application/json",
                digest=DIGEST_A,
                size_bytes=200,
                required=True,
                load_order=10,
            ),
        ),
    )


def make_runtime_pack(**overrides: object) -> RuntimePack:
    values: dict[str, object] = {
        "artifact_identity": "runtime-pack:reference.botany",
        "artifact_version": "1.2.0",
        "lifecycle": RuntimePackLifecycle.PUBLISHED,
        "created_at": T0,
        "artifact_digest": DIGEST_A,
        "provenance_refs": ("provenance:runtime-pack-build-1",),
        "compatibility": RuntimePackCompatibility(
            runtime_api_version=">=1.0.0,<2.0.0",
            pack_format_version="1.0.0",
            compatibility_evidence_refs=("EVID-COMP-KRISTAL-001",),
            supported_profile_ids=("sovereign_offline",),
        ),
        "manifest": make_manifest(),
        "query_contract_refs": ("query-contract.kristal.reference",),
        "reader_policy_refs": ("reader-policy.public-reference",),
        "visibility": DisclosureVisibility.PUBLIC,
        "contains_personal_data": False,
        "contains_restricted_content": False,
        "signature_refs": ("signature:knowledge-publisher-1",),
    }
    values.update(overrides)
    return RuntimePack(**values)  # type: ignore[arg-type]


def make_contract() -> QueryContract:
    return QueryContract(
        contract_id="query-contract.kristal.reference",
        version="1.0.0",
        supported_operations=("query.lookup", "query.search"),
        input_schema_ref="interfaces/kristal/query-input.schema.json",
        result_schema_ref="interfaces/kristal/query-result.schema.json",
        stable_sort_keys=("rank", "content_identity"),
        tie_breaker_key="content_identity",
        limits=ResourceLimits(
            max_page_size=50,
            timeout_ms=500,
            memory_mib=64,
            cpu_time_ms=250,
            max_result_bytes=1_000_000,
        ),
        deterministic_error_codes=(
            "audience_denied",
            "resource_budget_exceeded",
            "unsupported_operation",
        ),
        compatibility_constraint=">=1.0.0,<2.0.0",
        index_requirements=("index:by-id",),
        reader_policy_refs=("reader-policy.public-reference",),
        unsupported_operations=("query.mutate",),
    )


def passing_runtime_findings() -> tuple[VerificationFinding, ...]:
    return tuple(
        VerificationFinding(
            check=check,
            outcome=VerificationOutcome.PASS,
            evidence_refs=(f"evidence:{check.value}",),
        )
        for check in sorted(
            VerificationRecord.required_checks_for(ArtifactClass.RUNTIME_PACK),
            key=lambda item: item.value,
        )
    )


def test_content_identity_is_content_derived_and_context_independent() -> None:
    content = b"canonical epistemic content"
    artifact = make_kristal_artifact(content)

    assert artifact.verifies_content(content)
    assert not artifact.verifies_content(content + b" changed")
    serialized = artifact.as_dict()
    assert "tenant" not in serialized
    assert "interface_state" not in serialized
    assert serialized["content_identity"]["algorithm"] == "sha256"  # type: ignore[index]
    with pytest.raises(FrozenInstanceError):
        artifact.artifact_version = "changed"  # type: ignore[misc]


def test_kristal_artifact_rejects_unsafe_or_duplicate_manifest_paths() -> None:
    base = make_kristal_artifact()
    with pytest.raises(DomainValidationError, match="unsafe path"):
        replace(
            base,
            manifest_entries=(KristalManifestEntry("../escape.json", HEX_A),),
        )
    duplicate = KristalManifestEntry("claims/main.json", HEX_A)
    with pytest.raises(DomainValidationError, match="paths must be unique"):
        replace(base, manifest_entries=(duplicate, duplicate))


def test_runtime_pack_manifest_is_complete_ordered_and_dependency_safe() -> None:
    manifest = make_manifest()

    assert [entry.path for entry in manifest.entries] == [
        "content/claims.json",
        "indexes/by-id.json",
    ]
    assert manifest.total_uncompressed_size_bytes == 300

    with pytest.raises(DomainValidationError, match="dependency paths are missing"):
        RuntimePackManifest(
            manifest_version="1.0.0",
            manifest_digest=DIGEST_A,
            entries=(
                RuntimePackManifestEntry(
                    path="indexes/broken.json",
                    role="query_index",
                    media_type="application/json",
                    digest=DIGEST_A,
                    size_bytes=1,
                    required=True,
                    depends_on_paths=("missing.json",),
                ),
            ),
        )


def test_runtime_pack_enforces_channel_signatures_and_restricted_disclosure() -> None:
    pack = make_runtime_pack()
    assert pack.release_channel == "knowledge"
    assert pack.locator.artifact_class == "runtime_pack"

    with pytest.raises(DomainValidationError, match="knowledge release channel"):
        replace(pack, release_channel="services")
    with pytest.raises(DomainValidationError, match="require signatures"):
        replace(pack, signature_refs=())
    with pytest.raises(DomainValidationError, match="cannot be declared public"):
        replace(pack, contains_restricted_content=True)


def test_query_contract_requires_stable_tie_breaking_and_declared_operations() -> None:
    contract = make_contract()
    assert contract.accepts_operation("query.search")
    assert not contract.accepts_operation("query.mutate")

    with pytest.raises(DomainValidationError, match="tie_breaker_key"):
        replace(contract, tie_breaker_key="missing")
    with pytest.raises(DomainValidationError, match="both supported and unsupported"):
        replace(contract, unsupported_operations=("query.search",))
    with pytest.raises(DomainValidationError, match="status and provenance"):
        replace(contract, exposes_provenance=False)


def test_query_requests_are_bounded_and_contract_specific() -> None:
    contract = make_contract()
    request = QueryRequest(
        request_id="KQRY-ABCDEF12",
        operation="query.lookup",
        contract_id=contract.contract_id,
        contract_version=contract.version,
        parameters={"content_identity": "kristal:abc"},
        audience_ref="audience:public",
        reader_policy_ref="reader-policy.public-reference",
        page_size=25,
        requested_at=T0,
    )
    request.validate_against(contract)
    assert request.parameters_dict() == {"content_identity": "kristal:abc"}

    with pytest.raises(DomainValidationError, match="page_size exceeds"):
        replace(request, page_size=51).validate_against(contract)
    with pytest.raises(DomainValidationError, match="not supported"):
        replace(request, operation="query.mutate").validate_against(contract)


def test_query_pages_require_stable_order_and_unique_tie_breaking() -> None:
    first = QueryResultItem(
        content_identity="kristal:a",
        status="recognized",
        provenance_refs=("provenance:a",),
        sort_values=("001", "kristal:a"),
        payload={"label": "A"},
    )
    second = QueryResultItem(
        content_identity="kristal:b",
        status="recognized",
        provenance_refs=("provenance:b",),
        sort_values=("002", "kristal:b"),
        payload={"label": "B"},
    )
    page = QueryPage(
        request_id="KQRY-ABCDEF12",
        items=(first, second),
        page_size=2,
    )
    assert page.items == (first, second)

    with pytest.raises(DomainValidationError, match="stable deterministic order"):
        replace(page, items=(second, first))
    with pytest.raises(DomainValidationError, match="unique after tie-breaking"):
        replace(page, items=(first, first))


def test_reader_policy_projects_fields_without_rewriting_authoritative_state() -> None:
    record = ReaderRecord(
        content_identity="kristal:claim-1",
        audience_refs=("audience:public",),
        claim_class="taxon_claim",
        status="recognized",
        provenance_refs=("provenance:claim-1",),
        validation_state="validated",
        recognition_state="recognized",
        supersession_state="current",
        revocation_state="not_revoked",
        fields={"title": "White pine", "internal_note": "reviewed"},
    )
    policy = ReaderPolicy(
        policy_id="reader-policy.public-reference",
        version="1.0.0",
        eligible_claim_classes=("taxon_claim",),
        audience_refs=("audience:public",),
        visible_fields=("title",),
        ordering_keys=("title", "content_identity"),
        label_overrides={"taxon_claim": "Taxon"},
        explanations={"taxon_claim": "Recognized botanical reference."},
    )
    projection = policy.project(record, "audience:public")

    assert projection is not None
    assert projection.visible_fields_dict() == {"title": "White pine"}
    assert projection.content_identity == record.content_identity
    assert projection.provenance_refs == record.provenance_refs
    assert projection.revocation_state == record.revocation_state
    assert record.fields != projection.visible_fields


def test_reader_policy_denies_wrong_audience_and_revoked_content() -> None:
    policy = ReaderPolicy(
        policy_id="reader-policy.public-reference",
        version="1.0.0",
        eligible_claim_classes=("taxon_claim",),
        audience_refs=("audience:public",),
        visible_fields=("title",),
        ordering_keys=("title", "content_identity"),
    )
    record = ReaderRecord(
        content_identity="kristal:claim-1",
        audience_refs=("audience:restricted",),
        claim_class="taxon_claim",
        status="recognized",
        provenance_refs=("provenance:claim-1",),
        validation_state="validated",
        recognition_state="recognized",
        supersession_state="current",
        revocation_state="not_revoked",
        fields={"title": "Restricted record"},
    )
    assert policy.project(record, "audience:public") is None

    revoked = replace(
        record,
        audience_refs=("audience:public",),
        revocation_state="revoked",
    )
    assert policy.project(revoked, "audience:public") is None

    with pytest.raises(DomainValidationError, match="protected state"):
        replace(policy, visible_fields=("content_identity",))


def test_verification_record_requires_every_runtime_pack_check() -> None:
    locator = make_runtime_pack().locator
    record = VerificationRecord(
        candidate=locator,
        artifact_class=ArtifactClass.RUNTIME_PACK,
        verified_at=T0,
        findings=passing_runtime_findings(),
        verification_receipt_ref="receipt:runtime-pack-verification-1",
        integrity_scope_digest=DIGEST_A,
    )

    assert record.outcome is VerificationOutcome.PASS
    assert record.activation_eligible
    assert record.verifies_same_integrity_scope(DIGEST_A)

    with pytest.raises(DomainValidationError, match="missing required checks"):
        replace(record, findings=record.findings[:-1])


def test_nonpassing_verification_is_quarantined_and_never_eligible() -> None:
    findings = list(passing_runtime_findings())
    findings[0] = VerificationFinding(
        check=findings[0].check,
        outcome=VerificationOutcome.FAIL,
        reason_code="invalid_artifact_digest",
        evidence_refs=("evidence:integrity-failure",),
    )
    record = VerificationRecord(
        candidate=make_runtime_pack().locator,
        artifact_class=ArtifactClass.RUNTIME_PACK,
        verified_at=T0,
        findings=tuple(findings),
        verification_receipt_ref="receipt:runtime-pack-verification-2",
        integrity_scope_digest=DIGEST_A,
        rejection_conditions=(RejectionCondition.INVALID_ARTIFACT_DIGEST,),
    )

    assert record.outcome is VerificationOutcome.FAIL
    assert not record.activation_eligible
    assert record.quarantine_on_nonverified_outcome

    with pytest.raises(DomainValidationError, match="must remain quarantined"):
        replace(record, quarantine_on_nonverified_outcome=False)
    with pytest.raises(DomainValidationError, match="require a rejection condition"):
        replace(record, rejection_conditions=())


def test_query_failures_use_only_contract_declared_codes() -> None:
    contract = make_contract()
    failure = QueryFailure(
        request_id="KQRY-ABCDEF12",
        code="resource_budget_exceeded",
        message="The bounded query resource envelope was exhausted.",
    )
    failure.validate_against(contract)

    with pytest.raises(DomainValidationError, match="not declared"):
        replace(failure, code="unknown_failure").validate_against(contract)
