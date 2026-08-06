"""Resolve a bounded session into an explicit identity result."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Mapping

from . import require_text, require_utc, stable_ref
from ..ports import AuditEvent, AuditSink, Clock, IdentityStore


@dataclass(frozen=True, slots=True)
class ResolveSessionCommand:
    request_id: str
    session_ref: str
    tenant_ref: str | None
    environment: str
    intended_use: str


@dataclass(frozen=True, slots=True)
class ResolveSessionResult:
    request_id: str
    identity_result: str
    identity_ref: str | None
    assurance_context: Mapping[str, str]
    expires_at: datetime | None
    reason_code: str
    authorizes_business_action: bool = False


class ResolveSession:
    """Resolve session validity without turning it into action authorization."""

    operation_id = "resolve_session"

    def __init__(self, store: IdentityStore, clock: Clock, audit: AuditSink) -> None:
        self._store = store
        self._clock = clock
        self._audit = audit

    def execute(self, command: ResolveSessionCommand) -> ResolveSessionResult:
        request_id = require_text(command.request_id, "request_id")
        session_ref = require_text(command.session_ref, "session_ref")
        tenant_ref = require_text(command.tenant_ref, "tenant_ref") if command.tenant_ref is not None else None
        environment = require_text(command.environment, "environment")
        intended_use = require_text(command.intended_use, "intended_use")
        now = require_utc(self._clock.now(), "clock.now")

        try:
            self._audit.ensure_available(critical=False)
        except Exception:
            return self._result(
                request_id,
                session_ref,
                "indeterminate",
                None,
                {},
                None,
                "receipt_path_unavailable",
                publish=False,
            )

        session = self._store.get_session(session_ref)
        if session is None:
            return self._result(
                request_id,
                session_ref,
                "not_established",
                None,
                {},
                None,
                "session_not_found",
            )
        if session.tenant_ref != tenant_ref or session.environment != environment:
            return self._result(
                request_id,
                session_ref,
                "not_established",
                None,
                {},
                None,
                "trust_scope_mismatch",
            )
        if session.status == "revoked":
            return self._result(
                request_id,
                session_ref,
                "not_established",
                session.identity_id,
                {},
                None,
                "session_revoked",
            )
        if session.status != "active" or now >= require_utc(session.expires_at, "session.expires_at"):
            return self._result(
                request_id,
                session_ref,
                "not_established",
                session.identity_id,
                {},
                None,
                "session_expired",
            )

        identity = self._store.get_identity(session.identity_id)
        credential = self._store.get_credential(session.credential_id)
        if identity is None or credential is None:
            return self._result(
                request_id,
                session_ref,
                "indeterminate",
                session.identity_id,
                {},
                None,
                "identity_result_indeterminate",
            )
        if identity.status != "active":
            return self._result(
                request_id,
                session_ref,
                "not_established",
                identity.identity_id,
                {},
                None,
                "identity_not_established",
            )
        if identity.expires_at is not None and now >= require_utc(identity.expires_at, "identity.expires_at"):
            return self._result(
                request_id,
                session_ref,
                "not_established",
                identity.identity_id,
                {},
                None,
                "identity_not_established",
            )
        if identity.tenant_ref != tenant_ref or identity.environment != environment:
            return self._result(
                request_id,
                session_ref,
                "not_established",
                identity.identity_id,
                {},
                None,
                "subject_binding_mismatch",
            )
        if credential.status == "revoked":
            return self._result(
                request_id,
                session_ref,
                "not_established",
                identity.identity_id,
                {},
                None,
                "credential_revoked",
            )
        if credential.status != "active" or now >= require_utc(credential.expires_at, "credential.expires_at"):
            return self._result(
                request_id,
                session_ref,
                "not_established",
                identity.identity_id,
                {},
                None,
                "credential_expired",
            )
        if now < require_utc(credential.not_before, "credential.not_before"):
            return self._result(
                request_id,
                session_ref,
                "not_established",
                identity.identity_id,
                {},
                None,
                "credential_not_yet_valid",
            )
        if intended_use not in credential.intended_uses:
            return self._result(
                request_id,
                session_ref,
                "not_established",
                identity.identity_id,
                {},
                None,
                "trust_scope_mismatch",
            )
        if credential.scope.purpose is not None and credential.scope.purpose != intended_use:
            return self._result(
                request_id,
                session_ref,
                "not_established",
                identity.identity_id,
                {},
                None,
                "trust_scope_mismatch",
            )

        return self._result(
            request_id,
            session_ref,
            "established",
            identity.identity_id,
            dict(session.assurance_context),
            min(session.expires_at, credential.expires_at),
            "identity_established",
        )

    def _result(
        self,
        request_id: str,
        session_ref: str,
        identity_result: str,
        identity_ref: str | None,
        assurance_context: Mapping[str, str],
        expires_at: datetime | None,
        reason_code: str,
        *,
        publish: bool = True,
    ) -> ResolveSessionResult:
        now = require_utc(self._clock.now(), "clock.now")
        if publish:
            self._audit.publish(
                AuditEvent(
                    event_id=stable_ref("event", self.operation_id, request_id, session_ref),
                    operation_id=self.operation_id,
                    request_id=request_id,
                    event_type="session_resolution",
                    outcome=identity_result,
                    occurred_at=now,
                    subject_refs=tuple(ref for ref in (identity_ref, session_ref) if ref is not None),
                    reason_code=reason_code,
                    details={"authorizes_business_action": "false"},
                )
            )
        return ResolveSessionResult(
            request_id=request_id,
            identity_result=identity_result,
            identity_ref=identity_ref,
            assurance_context=dict(assurance_context),
            expires_at=expires_at,
            reason_code=reason_code,
        )
