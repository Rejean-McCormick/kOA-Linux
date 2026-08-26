from __future__ import annotations

import sys
from pathlib import Path
from typing import Mapping

import pytest

SRC = Path(__file__).parents[1] / "adapter" / "src"
sys.path.insert(0, str(SRC))

from koa_semantik_architect_adapter import (  # noqa: E402
    ArtifactAdmissionDecision,
    CapabilityId,
    LanguagePackValidationDecision,
    snapshot_from_external,
)


class FakeTransport:
    def __init__(self) -> None:
        self.calls: list[tuple[str, Mapping[str, object], str, str, str | None]] = []
        self.responses: dict[str, object] = {}
        self.failures: dict[str, BaseException] = {}

    def request(
        self,
        operation: str,
        payload: Mapping[str, object],
        *,
        request_id: str,
        correlation_id: str,
        idempotency_key: str | None = None,
    ) -> Mapping[str, object]:
        self.calls.append((operation, payload, request_id, correlation_id, idempotency_key))
        if operation in self.failures:
            raise self.failures[operation]
        response = self.responses.get(operation)
        if callable(response):
            response = response(payload, request_id, correlation_id)
        if response is None:
            response = {
                "operation": operation,
                "request_id": request_id,
                "correlation_id": correlation_id,
                "outcome": "succeeded",
                "payload": {},
                "evidence_refs": [],
            }
        return response  # type: ignore[return-value]


class FakeArtifactAdmission:
    def __init__(self, decision: ArtifactAdmissionDecision | None = None) -> None:
        self.decision = decision or ArtifactAdmissionDecision(
            True, "accepted", ("evidence:artifact",), "admission:artifact:1"
        )
        self.calls: list[Mapping[str, object]] = []

    def admit_compiled_candidate(self, payload: Mapping[str, object]) -> ArtifactAdmissionDecision:
        self.calls.append(payload)
        return self.decision


class FakeLanguagePackValidation:
    def __init__(self, decision: LanguagePackValidationDecision | None = None) -> None:
        self.decision = decision or LanguagePackValidationDecision(
            True, "verified", "verification:language-pack:1", ("evidence:runtime",)
        )
        self.calls: list[Mapping[str, object]] = []

    def validate_language_pack(self, payload: Mapping[str, object]) -> LanguagePackValidationDecision:
        self.calls.append(payload)
        return self.decision


@pytest.fixture
def transport() -> FakeTransport:
    return FakeTransport()


@pytest.fixture
def all_capabilities():
    return snapshot_from_external(
        [capability.value for capability in CapabilityId],
        documentation_mounted=False,
    )


@pytest.fixture
def compiler_request():
    from koa_semantik_architect_adapter import CompilerJobRequest

    return CompilerJobRequest(
        request_id="request:compile:1",
        correlation_id="correlation:compile:1",
        idempotency_key="idempotency:compile:1",
        actor_ref="identity:builder:1",
        identity_context_ref="identity-context:1",
        policy_decision_ref="decision:policy:1",
        resource_grant_ref="resource-grant:1",
        source_project_ref="language-project:fr-ca",
        source_revision="git:0123456789abcdef",
        language_tag="fr-CA",
        locale="fr_CA",
        toolchain_ref="toolchain:gf:3.12",
        target_runtime_contract_ref="contract:semantik-runtime:1",
        target_profile_refs=("profile:user-lightweight",),
        build_input_manifest_ref="manifest:build-inputs:1",
        parameters={"optimization": "release"},
    )


@pytest.fixture
def artifact_candidate():
    from koa_semantik_architect_adapter import CompiledArtifactCandidate

    return CompiledArtifactCandidate(
        artifact_ref="artifact:language-pack:fr-ca:1.0.0",
        artifact_class="language_pack",
        artifact_version="1.0.0",
        release_channel="knowledge",
        digest="sha256:" + "a" * 64,
        content_ref="artifact-store:language-pack:fr-ca:1.0.0",
        source_project_ref="language-project:fr-ca",
        source_revision="git:0123456789abcdef",
        provenance_ref="provenance:fr-ca:1",
        validation_evidence_refs=("evidence:compile:1", "evidence:runtime:1"),
        runtime_contract_ref="contract:semantik-runtime:1",
        target_profile_refs=("profile:user-lightweight",),
    )


@pytest.fixture
def language_pack_manifest():
    return {
        "$schema": "https://schemas.koa.local/artifact-contracts/language-pack.schema.json",
        "artifact_id": "language-pack:fr-ca:1.0.0",
        "artifact_class": "language_pack",
        "manifest_version": "1.0.0",
        "version": "1.0.0",
        "manifest_language": "en",
        "created_at": "2026-08-06T12:00:00Z",
        "owner": "owner:language-project:fr-ca",
        "title": "French Canada language runtime pack",
        "description": "Compiled deterministic language runtime material.",
        "release_channel": "knowledge",
        "source_project": {"project_ref": "language-project:fr-ca"},
        "language_identity": {"language_tag": "fr-CA"},
        "build": {"toolchain_ref": "toolchain:architect:1"},
        "contents": {"artifacts": []},
        "integrity": {"digest": "sha256:" + "b" * 64},
        "runtime_compatibility": {"runtime_contract_refs": ["contract:semantik-runtime:1"]},
        "profile_compatibility": {"profile_refs": ["profile:user-lightweight"]},
        "behavior": {"deterministic": True},
        "provenance": {"receipt_ref": "provenance:fr-ca:1"},
        "validation": {"evidence_refs": ["evidence:runtime:1"]},
        "lifecycle": {"state": "candidate"},
        "activation_contract": {"atomic": True},
        "retention": {"class": "published_artifact"},
        "traceability": {"requirement_ids": ["REQ-LIFE-LANG-002"]},
        "canonical_references": ["docs/contracts/artifact-contracts/language-pack.schema.json"],
        "supersedes": [],
        "replaced_by": None,
    }
