"""Render a policy-bounded deterministic projection of a verified artifact."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from hashlib import sha256
from typing import Any

from ..ports import ArtifactStore, AuditSink, PolicyEvaluator
from . import (
    ApplicationError,
    ArtifactRef,
    JsonValue,
    as_mapping,
    canonical_json,
    deterministic_id,
    evaluate_policy_port,
    freeze_mapping,
    record_evidence_port,
    thaw,
    validate_artifact_structure,
)


@dataclass(frozen=True, slots=True)
class RenderResult:
    artifact: ArtifactRef
    view_id: str
    view_version: str
    media_type: str
    payload: Mapping[str, JsonValue]
    payload_digest: str
    evidence_receipt_ref: str


class RenderArtifact:
    def __init__(
        self,
        artifact_store: ArtifactStore,
        policy_evaluator: PolicyEvaluator,
        audit_sink: AuditSink,
    ) -> None:
        self._artifacts = artifact_store
        self._policy = policy_evaluator
        self._audit = audit_sink

    def __call__(
        self,
        artifact_id: str,
        artifact_version: str,
        *,
        view_contract: object,
        actor_context: object,
        request_id: str,
    ) -> RenderResult:
        for value, field in (
            (artifact_id, "artifact_id"),
            (artifact_version, "artifact_version"),
            (request_id, "request_id"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ApplicationError("invalid_input", f"{field} is required")
        view = as_mapping(view_contract, name="view_contract")
        actor = as_mapping(actor_context, name="actor_context")
        artifact = self._load_verified(artifact_id, artifact_version)
        ref = validate_artifact_structure(artifact)
        view_id = _require_text(view, "view_id")
        view_version = _require_text(view, "version")
        media_type = _require_text(view, "media_type")
        fields_raw = view.get("fields")
        if not isinstance(fields_raw, (list, tuple)) or not fields_raw:
            raise ApplicationError("view_contract_invalid", "fields must be a non-empty array")
        fields = tuple(str(field) for field in fields_raw)
        if len(set(fields)) != len(fields):
            raise ApplicationError("view_contract_invalid", "fields must be unique")
        _enforce_audience(artifact, actor, view)

        decision = evaluate_policy_port(
            self._policy,
            "kristal.artifact.render",
            actor,
            {**thaw(ref.as_mapping()), "view_id": view_id},
            {"request_id": request_id, "requested_fields": list(fields)},
        )
        _require_allow(decision.outcome, decision.reason_code)
        fields, redacted = _apply_obligations(fields, decision.obligations)
        payload: dict[str, Any] = {}
        for path in fields:
            value = _read_path(artifact, path)
            _write_path(payload, path, "[REDACTED]" if path in redacted else thaw(value))
        rendered = freeze_mapping(payload)
        digest = "sha256:" + sha256(canonical_json(rendered)).hexdigest()
        receipt = record_evidence_port(
            self._audit,
            {
                "event_id": deterministic_id("render", request_id, ref.as_mapping(), view_id, digest),
                "event_type": "kristal.artifact.rendered",
                "outcome": "succeeded",
                "request_id": request_id,
                "artifact": thaw(ref.as_mapping()),
                "view_id": view_id,
                "view_version": view_version,
                "payload_digest": digest,
                "policy_decision_id": decision.decision_id,
                "policy_receipt_ref": decision.receipt_ref,
            },
            "render",
        )
        return RenderResult(ref, view_id, view_version, media_type, rendered, digest, receipt)

    def _load_verified(self, artifact_id: str, artifact_version: str) -> Mapping[str, JsonValue]:
        artifact = self._artifacts.get_artifact(artifact_id, artifact_version)
        if artifact is None:
            raise ApplicationError("artifact_not_found", "artifact is not admitted")
        if self._artifacts.get_revocation(artifact_id, artifact_version) is not None:
            raise ApplicationError("artifact_revoked", "revoked artifacts cannot be rendered")
        verification = self._artifacts.get_verification(artifact_id, artifact_version)
        if verification is None or verification.get("outcome") != "verified":
            raise ApplicationError("artifact_not_verified", "artifact has no successful verification")
        return as_mapping(artifact, name="stored artifact")


def _enforce_audience(
    artifact: Mapping[str, Any], actor: Mapping[str, Any], view: Mapping[str, Any]
) -> None:
    required = view.get("required_audience")
    actor_audiences = actor.get("audiences", ())
    if not isinstance(actor_audiences, (list, tuple)):
        raise ApplicationError("identity_context_invalid", "actor audiences must be an array")
    granted = set(str(item) for item in actor_audiences)
    if required is not None and (not isinstance(required, str) or required not in granted):
        raise ApplicationError("audience_denied", "actor lacks the view audience")
    rights = artifact.get("rights")
    if isinstance(rights, Mapping):
        audiences = rights.get("audiences", ())
        if audiences and not granted.intersection(str(item) for item in audiences):
            raise ApplicationError("audience_denied", "actor lacks an artifact audience")
    disclosure = artifact.get("disclosure")
    if isinstance(disclosure, Mapping) and disclosure.get("visibility") == "restricted" and not required:
        raise ApplicationError(
            "view_contract_invalid",
            "restricted Runtime Packs require an explicit audience-bound view",
        )


def _apply_obligations(
    fields: tuple[str, ...], obligations: Mapping[str, Any]
) -> tuple[tuple[str, ...], frozenset[str]]:
    supported = {"allowed_fields", "redact_fields"}
    unknown = set(obligations) - supported
    if unknown:
        raise ApplicationError(
            "unsupported_policy_obligation",
            "render policy returned unenforceable obligations",
            details={"obligations": sorted(unknown)},
        )
    allowed_raw = obligations.get("allowed_fields")
    effective = fields
    if allowed_raw is not None:
        if not isinstance(allowed_raw, (list, tuple)):
            raise ApplicationError("policy_protocol_error", "allowed_fields must be an array")
        allowed = frozenset(str(value) for value in allowed_raw)
        if not allowed.issubset(set(fields)):
            raise ApplicationError("policy_scope_expansion", "policy attempted to add render fields")
        effective = tuple(field for field in fields if field in allowed)
    redacted_raw = obligations.get("redact_fields", ())
    if not isinstance(redacted_raw, (list, tuple)):
        raise ApplicationError("policy_protocol_error", "redact_fields must be an array")
    redacted = frozenset(str(value) for value in redacted_raw)
    if not redacted.issubset(set(effective)):
        raise ApplicationError("policy_protocol_error", "redaction targets undeclared fields")
    return effective, redacted


def _read_path(mapping: Mapping[str, Any], path: str) -> Any:
    current: Any = mapping
    for part in path.split("."):
        if not part or not isinstance(current, Mapping) or part not in current:
            raise ApplicationError("view_contract_invalid", f"view field does not exist: {path}")
        current = current[part]
    return current


def _write_path(target: dict[str, Any], path: str, value: Any) -> None:
    parts = path.split(".")
    current = target
    for part in parts[:-1]:
        next_value = current.setdefault(part, {})
        if not isinstance(next_value, dict):
            raise ApplicationError("view_contract_invalid", f"overlapping view path: {path}")
        current = next_value
    current[parts[-1]] = value


def _require_text(mapping: Mapping[str, Any], key: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value:
        raise ApplicationError("view_contract_invalid", f"{key} is required")
    return value


def _require_allow(outcome: str, reason: str | None) -> None:
    if outcome == "allow":
        return
    if outcome == "deny":
        raise ApplicationError("policy_denied", "render was denied", details={"reason_code": reason})
    if outcome == "blocked":
        raise ApplicationError("policy_unavailable", "render policy is unavailable", details={"reason_code": reason})
    raise ApplicationError("policy_protocol_error", "policy returned an unknown outcome")
