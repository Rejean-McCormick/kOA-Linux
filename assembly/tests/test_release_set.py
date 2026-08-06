from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path

import pytest

from koa_assembly.releases import (
    ArtifactManifestEntry,
    ManifestValidationError,
    RecoveryDeclaration,
    ReleaseLockError,
    ReleaseManifest,
    ReleaseSetValidationError,
    build_release_lock,
    build_release_manifest,
    build_release_set,
    load_release_lock,
    load_release_set,
    validate_release_set,
    verify_release_lock,
    version_satisfies,
)


SHA = {
    "system": "1" * 64,
    "services": "2" * 64,
    "governance": "3" * 64,
    "knowledge": "4" * 64,
}
NAMESPACE = {
    "system": "koa.system",
    "services": "koa.services",
    "governance": "koa.governance",
    "knowledge": "koa.knowledge",
}


def manifest(channel: str, *, artifact_ref: str | None = None) -> ReleaseManifest:
    version = "1.2.3"
    source_ref = f"releases/{channel}/{version}"
    return build_release_manifest(
        channel_id=channel,
        release_id=f"koa.{channel}.1.2.3",
        version=version,
        manifest_ref=f"{source_ref}/manifest",
        source_release_ref=source_ref,
        artifacts=(
            ArtifactManifestEntry(
                artifact_ref=artifact_ref or f"artifacts/{channel}/{version}",
                artifact_class=f"{channel}_artifact",
                version=version,
                channel_id=channel,
                sha256=SHA[channel],
                size_bytes=100 + len(channel),
                provenance_ref=f"provenance/{channel}/{version}",
                sbom_ref=f"sbom/{channel}/{version}",
            ),
        ),
        provenance_ref=f"provenance/{channel}/{version}",
        validation_evidence_refs=(f"evidence/{channel}/{version}",),
        recovery=RecoveryDeclaration(
            mode="rollback",
            procedure_ref=f"recovery/{channel}/{version}",
        ),
        interface_versions={f"interface.{channel}": "1.0.0"},
        schema_versions={f"schema.{channel}": "1.0.0"},
    )


def manifests() -> tuple[ReleaseManifest, ...]:
    return tuple(manifest(channel) for channel in NAMESPACE)


def compatibility(*, actual: str = "1.2.3", result: str = "pass") -> dict:
    return {
        "status": "tested_compatible",
        "evaluated_at": "2026-08-06T14:00:00-04:00",
        "evaluator_ref": "validators/release-set/1.0.0",
        "constraint_results": [
            {
                "constraint_id": "system-services-runtime",
                "kind": "minimum_supported_version",
                "subject_ref": "interfaces/runtime",
                "operator": "semver_satisfies",
                "expected": "1.0.0",
                "actual": actual,
                "result": result,
                "evidence_refs": ["evidence/compatibility/system-services-runtime"],
            }
        ],
        "test_evidence_refs": ["evidence/release-set/1.0.0"],
    }


def build(
    schema_path: Path,
    *,
    selected_manifests: tuple[ReleaseManifest, ...] | None = None,
    compatibility_value: dict | None = None,
    target_result: str = "pass",
    signature_status: str = "verified",
):
    return build_release_set(
        release_set_id="koa.release-set.2026.08.06.1",
        version="1.0.0",
        lifecycle_status="active",
        issued_at="2026-08-06T14:15:00-04:00",
        effective_at="2026-08-06T14:30:00-04:00",
        issuer={
            "issuer_id": "koa.release-authority",
            "issuer_type": "release_authority",
            "authority_ref": "authority/release-authority/2026-08",
        },
        authority={
            "release_authority_ref": "authority/release-authority/2026-08",
            "approval_refs": ["approvals/release-set/2026.08.06.1"],
            "decision_refs": ["decisions/DEC-REL-001"],
        },
        target_scope={
            "profile_results": [
                {
                    "profile_id": "sovereign_hub",
                    "profile_contract_ref": "contracts/profiles/sovereign-hub.profile.json",
                    "result": target_result,
                    "evidence_refs": ["evidence/profile/sovereign-hub/1"],
                }
            ]
        },
        manifests=selected_manifests or manifests(),
        compatibility=compatibility_value or compatibility(),
        activation={
            "eligibility": "eligible",
            "strategy": "atomic_set_switch",
            "partial_activation_allowed": False,
            "activation_evidence_refs": ["evidence/activation/1"],
            "failure_result": "rollback_to_previous_compatible_set",
            "previous_good_release_set_ref": "release-sets/2026.07.20.2",
        },
        signature={
            "signature_artifact_ref": "signatures/release-set/1",
            "signer_identity_ref": "identities/release-signer-01",
            "signing_authority_ref": "authority/release-authority/2026-08",
            "signed_at": "2026-08-06T14:15:00-04:00",
            "verification_status": signature_status,
            "verification_evidence_refs": ["evidence/signature/1"],
        },
        provenance={
            "provenance_receipt_ref": "provenance/release-set/1",
            "release_channels_registry_ref": "contracts/release-channels.contract.json",
            "artifact_classes_registry_ref": "contracts/artifact-classes.contract.json",
            "generator_id": "release-set-builder",
            "generator_version": "1.0.0",
        },
        schema_path=schema_path,
    )


def test_manifest_is_deterministic_and_projects_to_channel_schema() -> None:
    first = manifest("services")
    second = build_release_manifest(
        channel_id="services",
        release_id=first.release_id,
        version=first.version,
        manifest_ref=first.manifest_ref,
        source_release_ref=first.source_release_ref,
        artifacts=reversed(first.artifacts),
        provenance_ref=first.provenance_ref,
        validation_evidence_refs=reversed(first.validation_evidence_refs),
        recovery=first.recovery,
        interface_versions=dict(reversed(first.interface_versions)),
        schema_versions=dict(reversed(first.schema_versions)),
    )
    assert first.canonical_bytes() == second.canonical_bytes()
    projection = first.to_channel_release()
    assert projection["channel_id"] == "services"
    assert projection["release_namespace"] == "koa.services"
    assert projection["artifact_refs"] == ["artifacts/services/1.2.3"]


def test_manifest_rejects_wrong_namespace_and_artifact_channel() -> None:
    base = manifest("system")
    with pytest.raises(ManifestValidationError, match="requires namespace"):
        ReleaseManifest(
            channel_id=base.channel_id,
            release_namespace="koa.services",
            release_id=base.release_id,
            version=base.version,
            manifest_ref=base.manifest_ref,
            source_release_ref=base.source_release_ref,
            artifacts=base.artifacts,
            provenance_ref=base.provenance_ref,
            validation_evidence_refs=base.validation_evidence_refs,
            recovery=base.recovery,
        )
    wrong = replace(base.artifacts[0], channel_id="knowledge")
    with pytest.raises(ManifestValidationError, match="manifest channel_id"):
        replace(base, artifacts=(wrong,))


def test_manifest_mapping_is_closed() -> None:
    value = manifest("governance").to_dict()
    value["unexpected"] = True
    with pytest.raises(ManifestValidationError, match="unsupported fields"):
        ReleaseManifest.from_mapping(value)


def test_release_set_validates_against_canonical_schema(repository_root: Path) -> None:
    release_set = build(
        repository_root / "docs/contracts/artifact-contracts/release-set.schema.json"
    )
    document = release_set.to_dict()
    assert set(document["channels"]) == {"system", "services", "governance", "knowledge"}
    assert document["compatibility"]["status"] == "tested_compatible"
    assert release_set.digest == release_set.digest


def test_manifest_input_order_does_not_change_release_set(repository_root: Path) -> None:
    schema = repository_root / "docs/contracts/artifact-contracts/release-set.schema.json"
    first = build(schema, selected_manifests=manifests())
    second = build(schema, selected_manifests=tuple(reversed(manifests())))
    assert first.canonical_bytes() == second.canonical_bytes()


def test_missing_or_duplicate_channel_manifest_is_rejected(repository_root: Path) -> None:
    schema = repository_root / "docs/contracts/artifact-contracts/release-set.schema.json"
    with pytest.raises(ReleaseSetValidationError, match="exactly one manifest"):
        build(schema, selected_manifests=manifests()[:-1])
    duplicate = (*manifests(), manifest("system"))
    with pytest.raises(ReleaseSetValidationError, match="duplicate channel"):
        build(schema, selected_manifests=duplicate)


def test_incompatible_version_is_rejected(repository_root: Path) -> None:
    schema = repository_root / "docs/contracts/artifact-contracts/release-set.schema.json"
    with pytest.raises(ReleaseSetValidationError, match="incompatible"):
        build(schema, compatibility_value=compatibility(actual="0.9.0", result="fail"))


def test_false_compatibility_success_is_rejected(repository_root: Path) -> None:
    schema = repository_root / "docs/contracts/artifact-contracts/release-set.schema.json"
    with pytest.raises(ReleaseSetValidationError, match="claims 'pass'"):
        build(schema, compatibility_value=compatibility(actual="0.9.0", result="pass"))


def test_unverified_active_release_set_is_rejected_by_schema(repository_root: Path) -> None:
    schema = repository_root / "docs/contracts/artifact-contracts/release-set.schema.json"
    with pytest.raises(ReleaseSetValidationError, match="verified"):
        build(schema, signature_status="unverified")


def test_failed_target_profile_blocks_activation(repository_root: Path) -> None:
    schema = repository_root / "docs/contracts/artifact-contracts/release-set.schema.json"
    with pytest.raises(ReleaseSetValidationError, match="target profile"):
        build(schema, target_result="fail")


def test_duplicate_artifact_across_channels_is_rejected(repository_root: Path) -> None:
    schema = repository_root / "docs/contracts/artifact-contracts/release-set.schema.json"
    values = list(manifests())
    values[1] = manifest("services", artifact_ref=values[0].artifacts[0].artifact_ref)
    with pytest.raises(ReleaseSetValidationError, match="duplicate artifact_ref"):
        build(schema, selected_manifests=tuple(values))


def test_mismatched_source_release_refs_are_rejected(repository_root: Path) -> None:
    schema = repository_root / "docs/contracts/artifact-contracts/release-set.schema.json"
    release_set = build(schema)
    document = release_set.to_dict()
    document["provenance"]["source_release_refs"][0] = "releases/system/other"
    with pytest.raises(ReleaseSetValidationError, match="source_release_refs"):
        validate_release_set(document, schema_path=schema)


def test_lock_is_reproducible_and_independent_of_manifest_order(repository_root: Path) -> None:
    schema = repository_root / "docs/contracts/artifact-contracts/release-set.schema.json"
    release_set = build(schema)
    first = build_release_lock(release_set, manifests())
    second = build_release_lock(release_set, tuple(reversed(manifests())))
    assert first.canonical_bytes() == second.canonical_bytes()
    assert len(first.channels) == 4
    assert len(first.artifacts) == 4
    verify_release_lock(first, release_set, manifests())


def test_tampered_lock_is_rejected(repository_root: Path) -> None:
    schema = repository_root / "docs/contracts/artifact-contracts/release-set.schema.json"
    release_set = build(schema)
    lock = build_release_lock(release_set, manifests())
    tampered = replace(lock, release_set_sha256="f" * 64)
    with pytest.raises(ReleaseLockError, match="does not reproduce"):
        verify_release_lock(tampered, release_set, manifests())


def test_manifest_change_after_release_set_is_rejected_by_lock(repository_root: Path) -> None:
    schema = repository_root / "docs/contracts/artifact-contracts/release-set.schema.json"
    release_set = build(schema)
    original = manifests()
    lock = build_release_lock(release_set, original)
    changed = list(original)
    changed[0] = replace(
        changed[0],
        artifacts=(replace(changed[0].artifacts[0], sha256="a" * 64),),
    )
    with pytest.raises(ReleaseLockError, match="does not reproduce"):
        verify_release_lock(lock, release_set, changed)


def test_load_release_set_rejects_duplicate_json_keys(
    repository_root: Path, tmp_path: Path
) -> None:
    schema = repository_root / "docs/contracts/artifact-contracts/release-set.schema.json"
    path = tmp_path / "duplicate.json"
    path.write_text('{"release_set_id":"one","release_set_id":"two"}', encoding="utf-8")
    with pytest.raises(ReleaseSetValidationError, match="duplicate object key"):
        load_release_set(path, schema_path=schema)


def test_semver_constraints_are_closed_and_prerelease_aware() -> None:
    assert version_satisfies("1.5.0", ">=1.0.0,<2.0.0")
    assert not version_satisfies("2.0.0", ">=1.0.0,<2.0.0")
    assert version_satisfies("1.0.0", ">1.0.0-rc.1")
    with pytest.raises(ReleaseSetValidationError, match="invalid semantic version"):
        version_satisfies("latest", ">=1.0.0")


def test_canonical_schema_example_passes_schema_and_semantics(repository_root: Path) -> None:
    schema = repository_root / "docs/contracts/artifact-contracts/release-set.schema.json"
    raw = json.loads(schema.read_text(encoding="utf-8"))
    result = validate_release_set(deepcopy(raw["examples"][0]), schema_path=schema)
    assert result.release_set_id == "koa.release-set.2026.08.03.1"


def test_release_lock_round_trip_and_duplicate_key_rejection(
    repository_root: Path, tmp_path: Path
) -> None:
    schema = repository_root / "docs/contracts/artifact-contracts/release-set.schema.json"
    release_set = build(schema)
    lock = build_release_lock(release_set, manifests())
    path = tmp_path / "release.lock.json"
    path.write_bytes(lock.canonical_bytes())
    loaded = load_release_lock(path)
    assert loaded.canonical_bytes() == lock.canonical_bytes()

    path.write_text('{"format":"koa.release-lock","format":"duplicate"}', encoding="utf-8")
    with pytest.raises(ReleaseLockError, match="duplicate object key"):
        load_release_lock(path)
