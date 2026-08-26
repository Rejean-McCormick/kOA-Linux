"""Validation and admission preparation for SemantiK Architect Language Packs."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Mapping, Protocol, runtime_checkable
import re

from .receipts import CommitState, Decision, ExecutionState, IntegrationReceipt, ReceiptOutcome, make_receipt

LANGUAGE_PACK_SCHEMA = "https://schemas.koa.local/artifact-contracts/language-pack.schema.json"
LANGUAGE_PACK_ARTIFACT_CLASS = "language_pack"
KNOWLEDGE_RELEASE_CHANNEL = "knowledge"
_REQUIRED_LANGUAGE_PACK_FIELDS = frozenset({
    "$schema", "artifact_id", "artifact_class", "manifest_version", "version", "manifest_language",
    "created_at", "owner", "title", "description", "release_channel", "source_project",
    "language_identity", "build", "contents", "integrity", "runtime_compatibility",
    "profile_compatibility", "behavior", "provenance", "validation", "lifecycle",
    "activation_contract", "retention", "traceability", "canonical_references", "supersedes",
    "replaced_by",
})
_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
_SECRET_KEYS = frozenset({"authorization", "credential", "password", "private_key", "secret", "token"})


class LanguagePackPreparationState(StrEnum):
    PREPARED = "prepared"
    REJECTED = "rejected"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class LanguagePackCandidate:
    artifact_ref: str
    artifact_digest: str
    manifest: Mapping[str, object]
    content_ref: str
    verification_evidence_refs: tuple[str, ...]
    provenance_ref: str
    release_set_refs: tuple[str, ...]
    authoritative: bool = False

    def __post_init__(self) -> None:
        for name in ("artifact_ref", "content_ref", "provenance_ref"):
            value = getattr(self, name).strip()
            if not value or len(value) > 512:
                raise ValueError(f"{name} must be non-empty and bounded")
            object.__setattr__(self, name, value)
        if not _DIGEST.fullmatch(self.artifact_digest):
            raise ValueError("artifact_digest must use sha256:<64 lowercase hex>")
        if self.content_ref.startswith(("data:", "inline:")):
            raise ValueError("language pack content must be referenced, not embedded")
        if self.authoritative:
            raise ValueError("external language pack candidates are non-authoritative before admission")
        manifest = dict(self.manifest)
        missing = sorted(_REQUIRED_LANGUAGE_PACK_FIELDS.difference(manifest))
        if missing:
            raise ValueError(f"language pack is missing fields: {', '.join(missing)}")
        if manifest.get("$schema") != LANGUAGE_PACK_SCHEMA:
            raise ValueError("unexpected language-pack schema identifier")
        if manifest.get("artifact_class") != LANGUAGE_PACK_ARTIFACT_CLASS:
            raise ValueError(f"artifact_class must be {LANGUAGE_PACK_ARTIFACT_CLASS}")
        if manifest.get("release_channel") != KNOWLEDGE_RELEASE_CHANNEL:
            raise ValueError("language packs belong to the knowledge channel")
        if manifest.get("manifest_language") != "en":
            raise ValueError("manifest_language must be en")
        _reject_secret_keys(manifest)
        object.__setattr__(self, "manifest", MappingProxyType(manifest))
        evidence = _unique_refs(self.verification_evidence_refs, "verification_evidence_refs")
        releases = _unique_refs(self.release_set_refs, "release_set_refs")
        if not evidence:
            raise ValueError("verification evidence is required")
        if not releases:
            raise ValueError("at least one Release Set reference is required")
        object.__setattr__(self, "verification_evidence_refs", evidence)
        object.__setattr__(self, "release_set_refs", releases)

    def to_validation_payload(self) -> Mapping[str, object]:
        return MappingProxyType({
            "artifact_ref": self.artifact_ref,
            "artifact_class": LANGUAGE_PACK_ARTIFACT_CLASS,
            "artifact_digest": self.artifact_digest,
            "content_ref": self.content_ref,
            "manifest": dict(self.manifest),
            "verification_evidence_refs": list(self.verification_evidence_refs),
            "provenance_ref": self.provenance_ref,
            "release_set_refs": list(self.release_set_refs),
            "release_channel": KNOWLEDGE_RELEASE_CHANNEL,
            "activation_requested": False,
            "authority_effect": "candidate_validation_only",
        })


@dataclass(frozen=True, slots=True)
class LanguagePackValidationDecision:
    accepted: bool
    reason_code: str
    verification_ref: str | None = None
    evidence_refs: tuple[str, ...] = ()


@runtime_checkable
class LanguagePackValidationPort(Protocol):
    """Platform validation boundary; validation does not imply runtime activation."""

    def validate_language_pack(self, payload: Mapping[str, object]) -> LanguagePackValidationDecision: ...


@dataclass(frozen=True, slots=True)
class LanguagePackPreparationResult:
    state: LanguagePackPreparationState
    artifact_ref: str
    verification_ref: str | None
    receipt: IntegrationReceipt
    reason_code: str


class LanguagePackBridge:
    """Prepares and validates a Language Pack candidate but never activates it."""

    def __init__(self, validation_port: LanguagePackValidationPort) -> None:
        if not isinstance(validation_port, LanguagePackValidationPort):
            raise TypeError("validation_port must implement LanguagePackValidationPort")
        self._validation_port = validation_port

    def prepare(self, candidate: LanguagePackCandidate, *, request_id: str, correlation_id: str) -> LanguagePackPreparationResult:
        try:
            decision = self._validation_port.validate_language_pack(candidate.to_validation_payload())
        except Exception:
            return self._result(candidate, request_id, correlation_id, LanguagePackPreparationState.BLOCKED, "language_pack_validation_unavailable")
        if not isinstance(decision, LanguagePackValidationDecision):
            return self._result(candidate, request_id, correlation_id, LanguagePackPreparationState.BLOCKED, "language_pack_validation_response_invalid")
        if not decision.accepted:
            return self._result(candidate, request_id, correlation_id, LanguagePackPreparationState.REJECTED, decision.reason_code, decision)
        if not decision.verification_ref:
            return self._result(candidate, request_id, correlation_id, LanguagePackPreparationState.BLOCKED, "verification_reference_missing", decision)
        return self._result(candidate, request_id, correlation_id, LanguagePackPreparationState.PREPARED, "language_pack_prepared", decision)

    @staticmethod
    def _result(candidate: LanguagePackCandidate, request_id: str, correlation_id: str, state: LanguagePackPreparationState,
                reason_code: str, decision: LanguagePackValidationDecision | None = None) -> LanguagePackPreparationResult:
        if state is LanguagePackPreparationState.PREPARED:
            authority, execution, outcome = Decision.AUTHORIZED, ExecutionState.SUCCEEDED, ReceiptOutcome.SUCCEEDED
        elif state is LanguagePackPreparationState.REJECTED:
            authority, execution, outcome = Decision.DENIED, ExecutionState.NOT_STARTED, ReceiptOutcome.REJECTED
        else:
            authority, execution, outcome = Decision.INDETERMINATE, ExecutionState.NOT_STARTED, ReceiptOutcome.BLOCKED
        receipt = make_receipt(
            receipt_type="language_pack_preparation",
            request_id=request_id,
            correlation_id=correlation_id,
            subject_ref=candidate.artifact_ref,
            decision=authority,
            execution_state=execution,
            commit_state=CommitState.NOT_COMMITTED,
            outcome=outcome,
            reason_code=reason_code,
            evidence_refs=decision.evidence_refs if decision else (),
        )
        return LanguagePackPreparationResult(state, candidate.artifact_ref, decision.verification_ref if decision else None, receipt, reason_code)


def _unique_refs(values: tuple[str, ...], name: str) -> tuple[str, ...]:
    refs = tuple(value.strip() for value in values if value.strip())
    if len(refs) != len(set(refs)):
        raise ValueError(f"{name} must be unique")
    return refs


def _reject_secret_keys(value: object, *, path: str = "manifest") -> None:
    if isinstance(value, Mapping):
        for raw_key, nested in value.items():
            key = str(raw_key).lower()
            if any(token in key for token in _SECRET_KEYS):
                raise ValueError(f"secret-bearing key is prohibited at {path}.{raw_key}")
            _reject_secret_keys(nested, path=f"{path}.{raw_key}")
    elif isinstance(value, (list, tuple)):
        for index, nested in enumerate(value):
            _reject_secret_keys(nested, path=f"{path}[{index}]")
