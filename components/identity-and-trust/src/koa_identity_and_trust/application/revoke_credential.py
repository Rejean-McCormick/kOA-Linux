"""Revoke a credential, invalidate dependent sessions, and record evidence."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
from hashlib import sha256
from typing import Mapping

from . import Conflict, InvalidRequest, NotFound, canonical_json, require_text, require_utc, stable_ref
from ..ports import (
    AuditEvent,
    AuditSink,
    Clock,
    IdempotencyRecord,
    IdentityStore,
    TransitionReceiptRecord,
    TrustScope,
)


@dataclass(frozen=True, slots=True)
class RevokeCredentialCommand:
    request_id: str
    idempotency_key: str
    credential_ref: str
    scope: TrustScope
    reason_code: str
    authority_ref: str
    effective_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class RevokeCredentialResult:
    request_id: str
    credential_ref: str
    resulting_status: str
    effective_at: datetime
    invalidated_sessions: int
    receipt_ref: str


class RevokeCredential:
    """Perform a fail-closed credential revocation transition."""

    operation_id = "revoke_trust_object"

    def __init__(self, store: IdentityStore, clock: Clock, audit: AuditSink) -> None:
        self._store = store
        self._clock = clock
        self._audit = audit

    def execute(self, command: RevokeCredentialCommand) -> RevokeCredentialResult:
        request_id = require_text(command.request_id, "request_id")
        idempotency_key = require_text(command.idempotency_key, "idempotency_key")
        credential_ref = require_text(command.credential_ref, "credential_ref")
        reason_code = require_text(command.reason_code, "reason_code")
        authority_ref = require_text(command.authority_ref, "authority_ref")
        now = require_utc(self._clock.now(), "clock.now")
        effective_at = require_utc(command.effective_at or now, "effective_at")
        if effective_at > now:
            raise InvalidRequest(
                "future scheduled revocation is not supported by this operation",
                reason_code="unsupported_transition",
            )
        fingerprint = sha256(
            canonical_json(
                {
                    "request_id": request_id,
                    "credential_ref": credential_ref,
                    "scope": dict(command.scope.as_mapping()),
                    "reason_code": reason_code,
                    "authority_ref": authority_ref,
                    "effective_at": effective_at.isoformat(),
                }
            ).encode("utf-8")
        ).hexdigest()
        prior = self._store.get_idempotency(self.operation_id, idempotency_key)
        if prior is not None:
            if prior.request_fingerprint != fingerprint:
                raise Conflict("idempotency key conflict", reason_code="idempotency_conflict")
            return self._result_from_response(prior.response)

        credential = self._store.get_credential(credential_ref)
        if credential is None:
            raise NotFound("credential not found", reason_code="credential_not_found")
        if effective_at < require_utc(credential.issued_at, "credential.issued_at"):
            raise InvalidRequest(
                "effective_at cannot precede credential issuance",
                reason_code="unsupported_transition",
            )
        if not credential.scope.exact_match(command.scope):
            raise Conflict("revocation scope does not exactly match credential scope", reason_code="trust_scope_mismatch")
        if credential.status == "revoked":
            raise Conflict("credential is already revoked", reason_code="credential_revoked")
        if credential.status == "retired":
            raise Conflict("retired credential cannot transition to revoked", reason_code="credential_not_active")

        receipt_ref = stable_ref("receipt", self.operation_id, request_id, credential_ref)
        self._audit.ensure_available(critical=True)
        revoked = replace(credential, status="revoked", revoked_at=effective_at)
        result: RevokeCredentialResult
        with self._store.transaction():
            self._store.put_credential(revoked)
            invalidated = self._store.invalidate_sessions_for_credential(credential_ref, effective_at=effective_at)
            result = RevokeCredentialResult(
                request_id=request_id,
                credential_ref=credential_ref,
                resulting_status="revoked",
                effective_at=effective_at,
                invalidated_sessions=invalidated,
                receipt_ref=receipt_ref,
            )
            response = self._response_mapping(result)
            receipt = TransitionReceiptRecord(
                receipt_ref=receipt_ref,
                receipt_class="transition_receipt",
                transition="credential_revocation",
                request_id=request_id,
                operation_id=self.operation_id,
                subject_refs=(credential.subject_identity_id, credential_ref),
                outcome="committed",
                reason_code=reason_code,
                occurred_at=effective_at,
                authority_ref=authority_ref,
                evidence_refs=credential.evidence_refs,
                details={"invalidated_sessions": str(invalidated), "target_type": "credential"},
            )
            self._store.append_receipt(receipt)
            self._store.put_idempotency(
                IdempotencyRecord(
                    operation_id=self.operation_id,
                    idempotency_key=idempotency_key,
                    request_fingerprint=fingerprint,
                    response=response,
                    created_at=now,
                )
            )
            self._audit.publish(
                AuditEvent(
                    event_id=stable_ref("event", self.operation_id, request_id, credential_ref),
                    operation_id=self.operation_id,
                    request_id=request_id,
                    event_type="credential_revoked",
                    outcome="committed",
                    occurred_at=effective_at,
                    subject_refs=(credential.subject_identity_id, credential_ref),
                    reason_code=reason_code,
                    receipt_ref=receipt_ref,
                    evidence_refs=credential.evidence_refs,
                    details={"invalidated_sessions": str(invalidated), "target_type": "credential"},
                )
            )
        return result

    @staticmethod
    def _response_mapping(result: RevokeCredentialResult) -> Mapping[str, str]:
        return {
            "request_id": result.request_id,
            "credential_ref": result.credential_ref,
            "resulting_status": result.resulting_status,
            "effective_at": result.effective_at.isoformat(),
            "invalidated_sessions": str(result.invalidated_sessions),
            "receipt_ref": result.receipt_ref,
        }

    @staticmethod
    def _result_from_response(response: Mapping[str, str]) -> RevokeCredentialResult:
        return RevokeCredentialResult(
            request_id=response["request_id"],
            credential_ref=response["credential_ref"],
            resulting_status=response["resulting_status"],
            effective_at=require_utc(datetime.fromisoformat(response["effective_at"]), "effective_at"),
            invalidated_sessions=int(response["invalidated_sessions"]),
            receipt_ref=response["receipt_ref"],
        )
