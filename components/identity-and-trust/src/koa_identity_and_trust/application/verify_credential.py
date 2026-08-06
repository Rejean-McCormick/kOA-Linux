"""Validate credential binding, scope, time, proof, and revocation state."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from . import require_text, require_utc, stable_ref
from ..ports import (
    AuditEvent,
    AuditSink,
    Clock,
    IdentityStore,
    KeyStore,
    TrustScope,
    VerificationRecord,
)


@dataclass(frozen=True, slots=True)
class VerifyCredentialCommand:
    request_id: str
    credential_ref: str
    presented_proof: bytes
    intended_use: str
    tenant_ref: str | None
    environment: str
    expected_subject_type: str | None = None


@dataclass(frozen=True, slots=True)
class VerifyCredentialResult:
    request_id: str
    trust_result: str
    identity_ref: str | None
    validated_scope: TrustScope | None
    reason_code: str
    verification_ref: str
    authorizes_business_action: bool = False


class VerifyCredential:
    """Produce an explicit non-authorizing trust result for one credential."""

    operation_id = "validate_credential"

    def __init__(self, store: IdentityStore, keys: KeyStore, clock: Clock, audit: AuditSink) -> None:
        self._store = store
        self._keys = keys
        self._clock = clock
        self._audit = audit

    def execute(self, command: VerifyCredentialCommand) -> VerifyCredentialResult:
        request_id = require_text(command.request_id, "request_id")
        credential_ref = require_text(command.credential_ref, "credential_ref")
        intended_use = require_text(command.intended_use, "intended_use")
        environment = require_text(command.environment, "environment")
        tenant_ref = require_text(command.tenant_ref, "tenant_ref") if command.tenant_ref is not None else None
        expected_subject_type = (
            require_text(command.expected_subject_type, "expected_subject_type")
            if command.expected_subject_type is not None
            else None
        )
        if not isinstance(command.presented_proof, bytes) or not command.presented_proof:
            return self._record(
                request_id=request_id,
                credential_ref=credential_ref,
                result="untrusted",
                identity_ref=None,
                scope=None,
                algorithm=None,
                reason_code="malformed_credential",
                evidence_refs=(),
            )

        now = require_utc(self._clock.now(), "clock.now")
        try:
            self._audit.ensure_available(critical=False)
        except Exception:
            return self._record(
                request_id=request_id,
                credential_ref=credential_ref,
                result="indeterminate",
                identity_ref=None,
                scope=None,
                algorithm=None,
                reason_code="receipt_path_unavailable",
                evidence_refs=(),
                publish=False,
            )

        credential = self._store.get_credential(credential_ref)
        if credential is None:
            return self._record(request_id, credential_ref, "untrusted", None, None, None, "credential_not_found", ())
        if credential.version != "1":
            return self._record(
                request_id,
                credential_ref,
                "untrusted",
                credential.subject_identity_id,
                None,
                None,
                "algorithm_or_version_unsupported",
                credential.evidence_refs,
            )
        if credential.status == "revoked":
            return self._record(
                request_id,
                credential_ref,
                "untrusted",
                credential.subject_identity_id,
                None,
                None,
                "credential_revoked",
                credential.evidence_refs,
            )
        if credential.status != "active":
            reason = "credential_expired" if credential.status == "expired" else "credential_not_active"
            return self._record(
                request_id,
                credential_ref,
                "untrusted",
                credential.subject_identity_id,
                None,
                None,
                reason,
                credential.evidence_refs,
            )
        if now < require_utc(credential.not_before, "credential.not_before"):
            return self._record(
                request_id,
                credential_ref,
                "untrusted",
                credential.subject_identity_id,
                None,
                None,
                "credential_not_yet_valid",
                credential.evidence_refs,
            )
        if now >= require_utc(credential.expires_at, "credential.expires_at"):
            return self._record(
                request_id,
                credential_ref,
                "untrusted",
                credential.subject_identity_id,
                None,
                None,
                "credential_expired",
                credential.evidence_refs,
            )
        if credential.scope.tenant != tenant_ref or credential.scope.environment != environment:
            return self._record(
                request_id,
                credential_ref,
                "untrusted",
                credential.subject_identity_id,
                None,
                None,
                "trust_scope_mismatch",
                credential.evidence_refs,
            )
        if intended_use not in credential.intended_uses:
            return self._record(
                request_id,
                credential_ref,
                "untrusted",
                credential.subject_identity_id,
                None,
                None,
                "trust_scope_mismatch",
                credential.evidence_refs,
            )
        if credential.scope.purpose is not None and credential.scope.purpose != intended_use:
            return self._record(
                request_id,
                credential_ref,
                "untrusted",
                credential.subject_identity_id,
                None,
                None,
                "trust_scope_mismatch",
                credential.evidence_refs,
            )

        identity = self._store.get_identity(credential.subject_identity_id)
        if identity is None:
            return self._record(
                request_id,
                credential_ref,
                "indeterminate",
                None,
                None,
                None,
                "identity_result_indeterminate",
                credential.evidence_refs,
            )
        if identity.status != "active":
            reason = "identity_not_established" if identity.status != "revoked" else "identity_revoked"
            return self._record(
                request_id,
                credential_ref,
                "untrusted",
                identity.identity_id,
                None,
                None,
                reason,
                credential.evidence_refs,
            )
        if identity.expires_at is not None and now >= require_utc(identity.expires_at, "identity.expires_at"):
            return self._record(
                request_id,
                credential_ref,
                "untrusted",
                identity.identity_id,
                None,
                None,
                "identity_not_established",
                credential.evidence_refs,
            )
        if identity.tenant_ref != tenant_ref or identity.environment != environment:
            return self._record(
                request_id,
                credential_ref,
                "untrusted",
                identity.identity_id,
                None,
                None,
                "subject_binding_mismatch",
                credential.evidence_refs,
            )
        if expected_subject_type is not None and identity.subject_type != expected_subject_type:
            return self._record(
                request_id,
                credential_ref,
                "untrusted",
                identity.identity_id,
                None,
                None,
                "subject_binding_mismatch",
                credential.evidence_refs,
            )

        proof = self._keys.verify_credential(
            material_ref=credential.key_or_material_reference,
            presented_proof=command.presented_proof,
            intended_use=intended_use,
            context={
                "credential_ref": credential.credential_id,
                "identity_ref": identity.identity_id,
                "tenant_ref": tenant_ref or "",
                "environment": environment,
            },
            verification_time=now,
        )
        scope = credential.scope if proof.result == "trusted" else None
        return self._record(
            request_id,
            credential_ref,
            proof.result,
            identity.identity_id,
            scope,
            proof.algorithm,
            proof.reason_code,
            tuple(dict.fromkeys((*credential.evidence_refs, *proof.evidence_refs))),
        )

    def _record(
        self,
        request_id: str,
        credential_ref: str,
        result: str,
        identity_ref: str | None,
        scope: TrustScope | None,
        algorithm: str | None,
        reason_code: str,
        evidence_refs: tuple[str, ...],
        *,
        publish: bool = True,
    ) -> VerifyCredentialResult:
        now = require_utc(self._clock.now(), "clock.now")
        verification_ref = stable_ref("verification", self.operation_id, request_id, credential_ref)
        record = VerificationRecord(
            verification_id=verification_ref,
            request_id=request_id,
            credential_or_artifact_ref=credential_ref,
            result=result,  # type: ignore[arg-type]
            resolved_identity_ref=identity_ref,
            resolved_trust_root_ref=None,
            validated_scope=scope,
            algorithm=algorithm,
            verified_at=now,
            reason_code=reason_code,
            evidence_refs=evidence_refs,
        )
        with self._store.transaction():
            self._store.append_verification(record)
            if publish:
                self._audit.publish(
                    AuditEvent(
                        event_id=stable_ref("event", self.operation_id, request_id, credential_ref),
                        operation_id=self.operation_id,
                        request_id=request_id,
                        event_type="credential_verification",
                        outcome=result,
                        occurred_at=now,
                        subject_refs=tuple(ref for ref in (identity_ref, credential_ref) if ref is not None),
                        reason_code=reason_code,
                        evidence_refs=evidence_refs,
                        details={"authorizes_business_action": "false"},
                    )
                )
        return VerifyCredentialResult(
            request_id=request_id,
            trust_result=result,
            identity_ref=identity_ref,
            validated_scope=scope,
            reason_code=reason_code,
            verification_ref=verification_ref,
        )
