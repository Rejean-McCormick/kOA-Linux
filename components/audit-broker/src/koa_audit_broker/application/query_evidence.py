"""Use case for policy-governed, minimized audit queries."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
import json
from typing import Any, Mapping

from ..ports.clock import Clock
from ..ports.event_store import (
    AccessOutcome,
    AccessReceipt,
    AuditDocument,
    EventStore,
    EvidenceQuery,
)
from ..ports.identity_context import IdentityContextPort, IdentityReference
from ..ports.policy_decision import (
    DisclosureAuthorizationRequest,
    FieldAction,
    PolicyDecision,
    PolicyDecisionPort,
    PolicyOutcome,
    Selectors,
)


@dataclass(frozen=True, slots=True)
class QueryEvidenceCommand:
    request_id: str
    requester_identity: IdentityReference
    purpose: str
    requested_scope: tuple[str, ...]
    selectors: Selectors
    requested_fields: tuple[str, ...]
    desired_output_class: str
    expires_at: datetime
    limit: int


@dataclass(frozen=True, slots=True)
class QueryEvidenceResult:
    outcome: AccessOutcome
    receipt_id: str
    requester_identity_ref: str | None
    records: tuple[AuditDocument, ...]
    total_matched: int
    effective_scope: tuple[str, ...]
    policy_decision_ref: str | None
    next_cursor: str | None = None
    source_content_complete: bool = True
    reason_codes: tuple[str, ...] = ()


class AuditAccessReceiptPersistenceError(RuntimeError):
    """A protected access attempt could not be durably receipted."""


def _aware(value: datetime, name: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")
    return value


def _receipt_id(request_id: str, outcome: AccessOutcome) -> str:
    return f"audit-access-{sha256(f'{request_id}\0{outcome.value}'.encode()).hexdigest()}"


def _selectors_narrower(effective: Selectors, requested: Selectors) -> bool:
    if not effective or set(effective) != set(requested):
        return False
    for key, effective_value in effective.items():
        if key not in requested:
            return False
        requested_value = requested[key]
        requested_values = (
            {requested_value} if isinstance(requested_value, str) else set(requested_value)
        )
        effective_values = (
            {effective_value} if isinstance(effective_value, str) else set(effective_value)
        )
        if not effective_values <= requested_values:
            return False
    return True


def _policy_is_narrower(decision: PolicyDecision, command: QueryEvidenceCommand) -> bool:
    if not decision.effective_scope or not set(decision.effective_scope) <= set(command.requested_scope):
        return False
    if decision.valid_until is not None and command.expires_at > decision.valid_until:
        return False
    if not _selectors_narrower(decision.effective_selectors, command.selectors):
        return False
    if not set(decision.field_actions) <= set(command.requested_fields):
        return False
    if decision.maximum_records < 0:
        return False
    return decision.purpose == command.purpose


def _pseudonymize(value: Any, *, decision_ref: str, field: str) -> str:
    canonical = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    digest = sha256(f"{decision_ref}\0{field}\0{canonical}".encode()).hexdigest()
    return f"pseudonym:{digest}"


def apply_field_actions(
    record: Mapping[str, Any], *, decision: PolicyDecision
) -> dict[str, Any]:
    """Apply only the exact field transformations authorized by policy."""

    output: dict[str, Any] = {}
    for field, action in decision.field_actions.items():
        if field not in record:
            continue
        if action is FieldAction.INCLUDE:
            output[field] = record[field]
        elif action is FieldAction.PSEUDONYMIZE:
            output[field] = _pseudonymize(
                record[field], decision_ref=decision.decision_ref, field=field
            )
        elif action is FieldAction.REDACT:
            continue
        else:  # closed enum guard for foreign implementations
            raise ValueError(f"unsupported field action: {action!r}")
    return output


class QueryEvidenceHandler:
    """Execute one deterministic query within external identity and policy authority."""

    def __init__(
        self,
        *,
        store: EventStore,
        identities: IdentityContextPort,
        policies: PolicyDecisionPort,
        clock: Clock,
    ) -> None:
        self._store = store
        self._identities = identities
        self._policies = policies
        self._clock = clock

    def _finish(
        self,
        command: QueryEvidenceCommand,
        *,
        now: datetime,
        outcome: AccessOutcome,
        identity_ref: str | None,
        policy_decision_ref: str | None,
        effective_scope: tuple[str, ...] = (),
        effective_fields: tuple[str, ...] = (),
        records: tuple[AuditDocument, ...] = (),
        total_matched: int = 0,
        next_cursor: str | None = None,
        source_content_complete: bool = True,
        reason_codes: tuple[str, ...] = (),
    ) -> QueryEvidenceResult:
        receipt_id = _receipt_id(command.request_id, outcome)
        receipt = AccessReceipt(
            receipt_id=receipt_id,
            request_id=command.request_id,
            requester_identity_ref=identity_ref,
            purpose=command.purpose,
            policy_decision_ref=policy_decision_ref,
            requested_scope=command.requested_scope,
            effective_scope=effective_scope,
            outcome=outcome,
            occurred_at=now,
            requested_fields=command.requested_fields,
            effective_fields=effective_fields,
            record_count=len(records),
            reason_codes=reason_codes,
        )
        try:
            self._store.record_access_receipt(receipt)
        except Exception as exc:
            raise AuditAccessReceiptPersistenceError(
                "access receipt was not durable"
            ) from exc
        return QueryEvidenceResult(
            outcome=outcome,
            receipt_id=receipt_id,
            requester_identity_ref=identity_ref,
            records=records,
            total_matched=total_matched,
            effective_scope=effective_scope,
            policy_decision_ref=policy_decision_ref,
            next_cursor=next_cursor,
            source_content_complete=source_content_complete,
            reason_codes=reason_codes,
        )

    def execute(self, command: QueryEvidenceCommand) -> QueryEvidenceResult:
        now = _aware(self._clock.now(), "clock.now()")
        _aware(command.expires_at, "expires_at")
        if not command.request_id.strip() or not command.purpose.strip():
            raise ValueError("request_id and purpose are required")
        if not command.requested_scope or not command.requested_fields:
            raise ValueError("requested_scope and requested_fields must be explicit")
        if command.limit <= 0:
            raise ValueError("limit must be positive")
        if command.expires_at <= now:
            return self._finish(
                command,
                now=now,
                outcome=AccessOutcome.EXPIRED,
                identity_ref=None,
                policy_decision_ref=None,
                reason_codes=("request_expired",),
            )

        verification = self._identities.verify_requester(
            command.requester_identity,
            operation="get_audit_record_metadata",
            purpose=command.purpose,
            at=now,
        )
        if not verification.authenticated:
            return self._finish(
                command,
                now=now,
                outcome=AccessOutcome.DENIED,
                identity_ref=verification.identity_ref,
                policy_decision_ref=None,
                reason_codes=verification.reason_codes or ("requester_not_authenticated",),
            )
        assert verification.identity_ref is not None

        decision = self._policies.authorize_disclosure(
            DisclosureAuthorizationRequest(
                request_id=command.request_id,
                requester_identity=command.requester_identity,
                requester_identity_ref=verification.identity_ref,
                purpose=command.purpose,
                requested_scope=command.requested_scope,
                selectors=command.selectors,
                requested_fields=command.requested_fields,
                desired_output_class=command.desired_output_class,
                expires_at=command.expires_at,
                requested_limit=command.limit,
            ),
            at=now,
        )
        if decision.outcome is PolicyOutcome.UNAVAILABLE:
            return self._finish(
                command,
                now=now,
                outcome=AccessOutcome.FAILED,
                identity_ref=verification.identity_ref,
                policy_decision_ref=decision.decision_ref,
                reason_codes=decision.reason_codes or ("policy_runtime_unavailable",),
            )
        if decision.outcome is PolicyOutcome.EXPIRED or (
            decision.valid_until is not None and decision.valid_until <= now
        ):
            return self._finish(
                command,
                now=now,
                outcome=AccessOutcome.EXPIRED,
                identity_ref=verification.identity_ref,
                policy_decision_ref=decision.decision_ref,
                reason_codes=decision.reason_codes or ("policy_decision_expired",),
            )
        if decision.outcome is PolicyOutcome.DENIED:
            return self._finish(
                command,
                now=now,
                outcome=AccessOutcome.DENIED,
                identity_ref=verification.identity_ref,
                policy_decision_ref=decision.decision_ref,
                reason_codes=decision.reason_codes or ("policy_denied",),
            )
        if not decision.permits_work:
            return self._finish(
                command,
                now=now,
                outcome=AccessOutcome.FAILED,
                identity_ref=verification.identity_ref,
                policy_decision_ref=decision.decision_ref,
                reason_codes=("unsupported_policy_outcome",),
            )
        if not _policy_is_narrower(decision, command):
            return self._finish(
                command,
                now=now,
                outcome=AccessOutcome.FAILED,
                identity_ref=verification.identity_ref,
                policy_decision_ref=decision.decision_ref,
                reason_codes=("policy_scope_expansion_rejected",),
            )

        limit = min(command.limit, decision.maximum_records)
        if limit <= 0:
            return self._finish(
                command,
                now=now,
                outcome=AccessOutcome.DENIED,
                identity_ref=verification.identity_ref,
                policy_decision_ref=decision.decision_ref,
                reason_codes=("policy_allows_zero_records",),
            )
        try:
            page = self._store.query_evidence(
                EvidenceQuery(
                    request_id=command.request_id,
                    purpose=command.purpose,
                    selectors=decision.effective_selectors,
                    effective_scope=decision.effective_scope,
                    field_actions=decision.field_actions,
                    limit=limit,
                )
            )
            records = tuple(
                apply_field_actions(record, decision=decision) for record in page.records[:limit]
            )
        except Exception as exc:
            return self._finish(
                command,
                now=now,
                outcome=AccessOutcome.FAILED,
                identity_ref=verification.identity_ref,
                policy_decision_ref=decision.decision_ref,
                reason_codes=("query_failed", type(exc).__name__),
            )

        partial = (
            decision.outcome is PolicyOutcome.PARTIALLY_ALLOWED
            or page.total_matched > len(records)
            or not page.source_content_complete
        )
        outcome = AccessOutcome.PARTIALLY_ALLOWED if partial else AccessOutcome.ALLOWED
        return self._finish(
            command,
            now=now,
            outcome=outcome,
            identity_ref=verification.identity_ref,
            policy_decision_ref=decision.decision_ref,
            effective_scope=decision.effective_scope,
            effective_fields=tuple(decision.field_actions),
            records=records,
            total_matched=page.total_matched,
            next_cursor=page.next_cursor,
            source_content_complete=page.source_content_complete,
            reason_codes=decision.reason_codes,
        )
