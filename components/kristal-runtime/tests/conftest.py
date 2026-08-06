"""Contract fixtures for the Kristal Runtime public API bundle."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys

import pytest

COMPONENT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = COMPONENT_ROOT / "src"
if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

from koa_kristal_runtime.api import (  # noqa: E402
    HealthVector,
    KristalIdentityResolutionResponse,
    Receipt,
    RuntimePackTransitionResult,
    RuntimePackVerificationResult,
    RuntimeStatusResponse,
)
from koa_kristal_runtime.api.models import VERIFICATION_CHECKS  # noqa: E402

DIGEST_A = "sha256:" + "a" * 64
DIGEST_B = "sha256:" + "b" * 64
BARE_DIGEST_A = "a" * 64


def repository_root() -> Path:
    current = Path(__file__).resolve()
    for candidate in (current, *current.parents):
        if (candidate / "docs" / "AI_CONTEXT.md").is_file():
            return candidate
    raise RuntimeError("repository root with docs/AI_CONTEXT.md was not found")


def make_runtime_pack(**overrides: object) -> dict[str, object]:
    pack: dict[str, object] = {
        "schema_version": "1.0.0",
        "artifact_class": "runtime_pack",
        "artifact_identity": "runtime-pack:knowledge/community-services",
        "artifact_version": "1.0.0",
        "release_channel": "knowledge",
        "lifecycle": {"status": "verified"},
        "created_at": "2026-08-03T18:00:00-04:00",
        "artifact_digest": DIGEST_A,
        "digest_scope": "canonical_manifest_and_payload",
        "provenance": {
            "producer": {
                "producer_id": "kristal-runtime-pack-builder",
                "producer_type": "build_system",
                "contract_ref": "contracts/components/kristal-runtime.component.json",
                "software_version": "1.0.0",
            },
            "build_id": "build:runtime-pack:community-services:1.0.0",
            "built_at": "2026-08-03T18:00:00-04:00",
            "source_materials": [
                {
                    "material_id": "source:community-services:2026-08-03",
                    "digest": DIGEST_B,
                    "source_ref": "EVID-COMP-KRISTAL-001",
                    "version": "2026.08.03",
                }
            ],
            "generator": {"id": "kristal-runtime-pack-builder", "version": "1.0.0"},
            "reproducible_build": True,
            "provenance_receipt_ref": "EVID-COMP-KRISTAL-002",
        },
        "compatibility_constraints": {
            "target_component": "kristal_runtime",
            "target_component_contract_ref": "contracts/components/kristal-runtime.component.json",
            "runtime_api_version": ">=1.0.0,<2.0.0",
            "pack_format_version": "1.0.0",
            "supported_profile_ids": ["user_lightweight", "sovereign_hub"],
            "compatibility_evidence_refs": ["EVID-COMP-KRISTAL-003"],
        },
        "manifest": {
            "manifest_version": "1.0.0",
            "manifest_digest": DIGEST_B,
            "total_uncompressed_size_bytes": 42,
            "entries": [
                {
                    "path": "knowledge/index.json",
                    "role": "knowledge_index",
                    "media_type": "application/json",
                    "digest": DIGEST_A,
                    "size_bytes": 42,
                    "required": True,
                    "content_identity": "kristal:community-services:index",
                    "load_order": 0,
                }
            ],
        },
        "verification": {
            "required_checks": list(VERIFICATION_CHECKS),
            "quarantine_on_nonverified_outcome": True,
            "reverify_after_integrity_scope_change": True,
            "verification_receipt_schema_ref": "contracts/artifact-contracts/decision-receipt.schema.json",
        },
        "activation_contract": {
            "owner_component": "kristal_runtime",
            "component_contract_ref": "contracts/components/kristal-runtime.component.json",
            "interface_id": "runtime_pack_activation",
            "activation_boundary": "active_runtime_pack_record",
            "activation_mode": "atomic_pointer_switch",
            "partial_authoritative_activation_allowed": False,
            "last_valid_state_retained_until_success": True,
            "verification_receipt_required": True,
            "authorization_required": True,
            "resource_grant_required": True,
            "recovery": {
                "rollback_supported": True,
                "last_valid_predecessor_required": True,
                "forward_repair_supported": True,
                "rollback_compatibility_constraint": ">=0.9.0,<2.0.0",
                "forward_repair_contract_ref": "docs/06-lifecycle/16-forward-repair.md",
            },
        },
        "replacement_policy": {
            "implicit_downgrade_allowed": False,
            "implicit_substitution_allowed": False,
            "authorization_required": True,
            "compatibility_validation_required": True,
        },
        "content_handling": {
            "immutable_after_publication": True,
            "unverified_execution_allowed": False,
            "direct_cross_component_mutation_allowed": False,
            "secret_values_allowed": False,
        },
        "disclosure": {
            "visibility": "authorized_internal",
            "contains_secret_values": False,
            "contains_personal_data": False,
            "contains_restricted_content": False,
            "rights_policy_refs": ["REQ-COMP-KRISTAL-006"],
        },
    }
    for key, value in overrides.items():
        pack[key] = value
    return deepcopy(pack)


def make_kristal_artifact() -> dict[str, object]:
    return {
        "artifact_id": "kristal-artifact.community-services",
        "artifact_version": "1.0.0",
        "artifact_class": "kristal_artifact",
        "content_identity": {"algorithm": "sha256", "digest": BARE_DIGEST_A},
        "manifest": {
            "entries": [{"path": "content/index.json", "sha256": BARE_DIGEST_A}],
            "query_contract_refs": ["contracts/queries/community-services-v1.json"],
        },
        "provenance": {
            "source_refs": ["EVID-COMP-KRISTAL-001"],
            "producer": "kristal-runtime-pack-builder",
            "build_receipt_ref": "EVID-COMP-KRISTAL-002",
        },
        "rights": {"license": "CC-BY-4.0", "audiences": ["general_public"]},
        "compatibility": {"kristal_runtime": ">=1.0.0,<2.0.0", "schema_versions": ["1.0.0"]},
        "signatures": [],
    }


class ContractServiceDouble:
    """Narrow public-port double; it is not a persistence or adapter replacement."""

    def __init__(self) -> None:
        self.failures: dict[str, Exception] = {}
        self.calls: list[str] = []
        self.active_runtime_identity = "runtime-pack:knowledge/community-services-previous"
        self.last_valid_runtime_identity = self.active_runtime_identity
        self.verification_record_ref = "verification-record:community-services:1.0.0"
        self.activation_record_ref = "activation-record:community-services:previous"

    def _raise_if_configured(self, interface_id: str) -> None:
        self.calls.append(interface_id)
        failure = self.failures.get(interface_id)
        if failure is not None:
            raise failure

    def resolve_kristal_identity(self, request):
        self._raise_if_configured("kristal_identity_resolution")
        digest = request.content_digest or DIGEST_A
        return KristalIdentityResolutionResponse(
            "resolved",
            "verified",
            "kristal:community-services:index",
            digest,
        )

    def validate_runtime_pack(self, request):
        self._raise_if_configured("runtime_pack_validation")
        self.verification_record_ref = f"verification-record:{request.artifact_identity}:{request.artifact_version}"
        receipt = Receipt(
            "receipt:runtime-pack-validation:1",
            "verification_receipt",
            "runtime_pack_validation",
            "verified",
            request.correlation_id,
            request.artifact_identity,
            ("EVID-COMP-KRISTAL-003",),
        )
        return RuntimePackVerificationResult(
            "verified",
            True,
            self.verification_record_ref,
            request.artifact_identity,
            request.artifact_version,
            request.artifact_digest,
            {name: "pass" for name in VERIFICATION_CHECKS},
            receipt,
        )

    def activate_runtime_pack(self, request):
        self._raise_if_configured("runtime_pack_activation")
        self.last_valid_runtime_identity = self.active_runtime_identity
        self.active_runtime_identity = "runtime-pack:knowledge/community-services"
        self.activation_record_ref = f"activation-record:{request.activation_request_id}"
        receipt = Receipt(
            f"receipt:{request.activation_request_id}",
            "transition_receipt",
            "runtime_pack_activation",
            "activated",
            request.correlation_id,
            self.active_runtime_identity,
            ("EVID-COMP-KRISTAL-004",),
        )
        return RuntimePackTransitionResult(
            "runtime_pack_activation",
            "activated",
            self.active_runtime_identity,
            True,
            receipt,
        )

    def rollback_runtime_pack(self, request):
        self._raise_if_configured("runtime_pack_rollback")
        self.active_runtime_identity = request.target_last_valid_runtime_ref
        self.activation_record_ref = f"rollback-record:{request.rollback_request_id}"
        receipt = Receipt(
            f"receipt:{request.rollback_request_id}",
            "recovery_receipt",
            "runtime_pack_rollback",
            "rolled_back",
            request.correlation_id,
            self.active_runtime_identity,
            ("EVID-COMP-KRISTAL-005",),
        )
        return RuntimePackTransitionResult(
            "runtime_pack_rollback",
            "rolled_back",
            self.active_runtime_identity,
            True,
            receipt,
        )

    def query_runtime_status(self, request):
        self._raise_if_configured("runtime_status_query")
        return RuntimeStatusResponse(
            self.active_runtime_identity,
            "verified",
            "active",
            HealthVector("active", True, True, True, True, True, True),
            self.verification_record_ref,
            self.activation_record_ref,
        )


@pytest.fixture
def service() -> ContractServiceDouble:
    return ContractServiceDouble()


@pytest.fixture
def runtime_pack() -> dict[str, object]:
    return make_runtime_pack()
