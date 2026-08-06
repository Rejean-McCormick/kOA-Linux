"""Apply a governed artifact revocation and withdraw derived query structures."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Literal

from ..ports import ArtifactStore, AuditSink, IndexStore, PolicyEvaluator
from . import (
    ApplicationError,
    ArtifactRef,
    as_mapping,
    deterministic_id,
    evaluate_policy_port,
    freeze_mapping,
    record_evidence_port,
    thaw,
    validate_artifact_structure,
)

RevocationOutcome = Literal["revoked", "already_revoked"]
_ALLOWED_SCOPES = frozenset({"activation", "distribution", "query", "all"})


@dataclass(frozen=True, slots=True)
class RevocationResult:
    outcome: RevocationOutcome
    artifact: ArtifactRef
    revocation_id: str
    scope: str
    evidence_receipt_ref: str
    replacement_artifact_ref: str | None


class RevokeArtifact:
    def __init__(
        self,
        artifact_store: ArtifactStore,
        index_store: IndexStore,
        policy_evaluator: PolicyEvaluator,
        audit_sink: AuditSink,
    ) -> None:
        self._artifacts = artifact_store
        self._index = index_store
        self._policy = policy_evaluator
        self._audit = audit_sink

    def __call__(
        self,
        artifact_id: str,
        artifact_version: str,
        *,
        actor_context: object,
        request_id: str,
        reason_code: str,
        scope: str,
        replacement_artifact_ref: str | None = None,
    ) -> RevocationResult:
        for value, field in (
            (artifact_id, "artifact_id"),
            (artifact_version, "artifact_version"),
            (request_id, "request_id"),
            (reason_code, "reason_code"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ApplicationError("invalid_input", f"{field} is required")
        if scope not in _ALLOWED_SCOPES:
            raise ApplicationError("revocation_scope_invalid", "revocation scope is not declared")
        if replacement_artifact_ref is not None and not replacement_artifact_ref.strip():
            raise ApplicationError("invalid_input", "replacement_artifact_ref cannot be empty")
        actor = as_mapping(actor_context, name="actor_context")
        stored = self._artifacts.get_artifact(artifact_id, artifact_version)
        if stored is None:
            raise ApplicationError("artifact_not_found", "artifact is not admitted")
        artifact = as_mapping(stored, name="stored artifact")
        ref = validate_artifact_structure(artifact)
        expected_id = deterministic_id(
            "revocation",
            request_id,
            ref.as_mapping(),
            {"reason_code": reason_code, "scope": scope, "replacement": replacement_artifact_ref or ""},
        )
        decision = evaluate_policy_port(
            self._policy,
            "kristal.artifact.revoke",
            actor,
            {**thaw(ref.as_mapping()), "scope": scope},
            {
                "request_id": request_id,
                "reason_code": reason_code,
                "replacement_artifact_ref": replacement_artifact_ref,
            },
        )
        _require_allow(decision.outcome, decision.reason_code)
        if decision.obligations:
            unsupported = set(decision.obligations) - {"maximum_scope"}
            if unsupported:
                raise ApplicationError(
                    "unsupported_policy_obligation",
                    "revocation policy returned unenforceable obligations",
                    details={"obligations": sorted(unsupported)},
                )
            maximum = decision.obligations.get("maximum_scope")
            if maximum is not None and not _scope_within(scope, str(maximum)):
                raise ApplicationError("policy_scope_expansion", "requested revocation exceeds policy scope")

        existing = self._artifacts.get_revocation(artifact_id, artifact_version)
        if existing is not None:
            record = as_mapping(existing, name="revocation record")
            if record.get("revocation_id") != expected_id:
                raise ApplicationError(
                    "revocation_conflict",
                    "artifact is already revoked by a different request or scope",
                )
            self._withdraw_index(ref, scope)
            return RevocationResult(
                "already_revoked",
                ref,
                expected_id,
                scope,
                _require_text(record.get("evidence_receipt_ref"), "evidence_receipt_ref"),
                replacement_artifact_ref,
            )

        event = {
            "event_id": expected_id,
            "event_type": "kristal.artifact.revocation",
            "outcome": "revoked",
            "request_id": request_id,
            "artifact": thaw(ref.as_mapping()),
            "scope": scope,
            "reason_code": reason_code,
            "replacement_artifact_ref": replacement_artifact_ref,
            "policy_decision_id": decision.decision_id,
            "policy_receipt_ref": decision.receipt_ref,
        }
        receipt = record_evidence_port(self._audit, event, "revocation")
        record = freeze_mapping(
            {
                "revocation_id": expected_id,
                "request_id": request_id,
                "artifact_id": ref.artifact_id,
                "artifact_version": ref.artifact_version,
                "content_digest": ref.content_digest,
                "scope": scope,
                "reason_code": reason_code,
                "replacement_artifact_ref": replacement_artifact_ref,
                "policy_decision_id": decision.decision_id,
                "policy_receipt_ref": decision.receipt_ref,
                "evidence_receipt_ref": receipt,
                "status": "revoked",
            }
        )
        outcome = self._artifacts.record_revocation(thaw(record))
        if outcome not in {"created", "existing"}:
            raise ApplicationError("store_protocol_error", "artifact store returned an unknown outcome")
        self._withdraw_index(ref, scope)
        return RevocationResult(
            "revoked" if outcome == "created" else "already_revoked",
            ref,
            expected_id,
            scope,
            receipt,
            replacement_artifact_ref,
        )

    def _withdraw_index(self, ref: ArtifactRef, scope: str) -> None:
        if scope not in {"query", "all"}:
            return
        try:
            self._index.withdraw(ref.artifact_id, ref.artifact_version, scope)
        except Exception as exc:
            raise ApplicationError(
                "revocation_cleanup_failed",
                "the authoritative revocation is recorded but derived indexes were not withdrawn",
                details={"artifact_id": ref.artifact_id, "scope": scope},
            ) from exc


def _scope_within(requested: str, maximum: str) -> bool:
    if maximum == "all":
        return requested in _ALLOWED_SCOPES
    return requested == maximum


def _require_allow(outcome: str, reason: str | None) -> None:
    if outcome == "allow":
        return
    if outcome == "deny":
        raise ApplicationError("policy_denied", "revocation was denied", details={"reason_code": reason})
    if outcome == "blocked":
        raise ApplicationError("policy_unavailable", "revocation policy is unavailable", details={"reason_code": reason})
    raise ApplicationError("policy_protocol_error", "policy returned an unknown outcome")


def _require_text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise ApplicationError("store_integrity_error", f"stored {field} is invalid")
    return value
