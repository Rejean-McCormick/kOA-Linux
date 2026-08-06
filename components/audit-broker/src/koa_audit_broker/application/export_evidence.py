"""Use case for destination-bound private evidence packages."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
import json
from typing import Any

from ..ports.clock import Clock
from ..ports.event_store import (
    AccessOutcome,
    AuditDocument,
    DisclosurePackage,
    DisclosureReceipt,
    EventStore,
)
from ..ports.identity_context import IdentityReference
from .query_evidence import QueryEvidenceCommand, QueryEvidenceHandler, QueryEvidenceResult


@dataclass(frozen=True, slots=True)
class ExportEvidenceCommand:
    request_id: str
    requester_identity: IdentityReference
    purpose: str
    requested_scope: tuple[str, ...]
    selectors: dict[str, str | tuple[str, ...]]
    requested_fields: tuple[str, ...]
    desired_output_class: str
    destination_ref: str
    expires_at: datetime
    limit: int
    maximum_package_bytes: int


@dataclass(frozen=True, slots=True)
class ExportEvidenceResult:
    outcome: AccessOutcome
    receipt_id: str
    access_receipt_id: str
    package: DisclosurePackage | None
    policy_decision_ref: str | None
    reason_codes: tuple[str, ...] = ()


class AuditDisclosureReceiptPersistenceError(RuntimeError):
    """A disclosure-package attempt could not be durably receipted."""


def _canonical(records: tuple[AuditDocument, ...]) -> bytes:
    return json.dumps(
        records,
        sort_keys=True,
        separators=(",", ":"),
        default=lambda value: value.isoformat() if isinstance(value, datetime) else str(value),
    ).encode()


def _stable_id(prefix: str, *parts: str) -> str:
    return f"{prefix}-{sha256(chr(0).join(parts).encode()).hexdigest()}"


class ExportEvidenceHandler:
    """Prepare a bounded package; it never performs cross-domain publication."""

    def __init__(
        self,
        *,
        query_handler: QueryEvidenceHandler,
        store: EventStore,
        clock: Clock,
    ) -> None:
        self._queries = query_handler
        self._store = store
        self._clock = clock

    def _record_receipt(
        self,
        command: ExportEvidenceCommand,
        query: QueryEvidenceResult,
        *,
        now: datetime,
        outcome: AccessOutcome,
        package_ref: str | None,
        reason_codes: tuple[str, ...],
    ) -> str:
        receipt_id = _stable_id("audit-disclosure", command.request_id, outcome.value)
        receipt = DisclosureReceipt(
            receipt_id=receipt_id,
            request_id=command.request_id,
            requester_identity_ref=query.requester_identity_ref,
            purpose=command.purpose,
            policy_decision_ref=query.policy_decision_ref,
            requested_scope=command.requested_scope,
            effective_scope=query.effective_scope,
            outcome=outcome,
            occurred_at=now,
            package_ref=package_ref,
            destination_ref=command.destination_ref,
            delivery_state="not_attempted",
            reason_codes=reason_codes,
        )
        try:
            self._store.record_disclosure_receipt(receipt)
        except Exception as exc:
            raise AuditDisclosureReceiptPersistenceError(
                "disclosure receipt was not durable"
            ) from exc
        return receipt_id

    def execute(self, command: ExportEvidenceCommand) -> ExportEvidenceResult:
        now = self._clock.now()
        if now.tzinfo is None or now.utcoffset() is None:
            raise ValueError("clock.now() must be timezone-aware")
        if not command.destination_ref.strip():
            raise ValueError("destination_ref is required")
        if command.maximum_package_bytes <= 0:
            raise ValueError("maximum_package_bytes must be positive")
        query = self._queries.execute(
            QueryEvidenceCommand(
                request_id=command.request_id,
                requester_identity=command.requester_identity,
                purpose=command.purpose,
                requested_scope=command.requested_scope,
                selectors=command.selectors,
                requested_fields=command.requested_fields,
                desired_output_class=command.desired_output_class,
                expires_at=command.expires_at,
                limit=command.limit,
            )
        )
        if query.outcome not in {AccessOutcome.ALLOWED, AccessOutcome.PARTIALLY_ALLOWED}:
            receipt_id = self._record_receipt(
                command,
                query,
                now=now,
                outcome=query.outcome,
                package_ref=None,
                reason_codes=query.reason_codes,
            )
            return ExportEvidenceResult(
                outcome=query.outcome,
                receipt_id=receipt_id,
                access_receipt_id=query.receipt_id,
                package=None,
                policy_decision_ref=query.policy_decision_ref,
                reason_codes=query.reason_codes,
            )

        if command.desired_output_class in {"public", "cross_domain_publication"}:
            reasons = ("publication_gateway_required",)
            receipt_id = self._record_receipt(
                command,
                query,
                now=now,
                outcome=AccessOutcome.DENIED,
                package_ref=None,
                reason_codes=reasons,
            )
            return ExportEvidenceResult(
                outcome=AccessOutcome.DENIED,
                receipt_id=receipt_id,
                access_receipt_id=query.receipt_id,
                package=None,
                policy_decision_ref=query.policy_decision_ref,
                reason_codes=reasons,
            )

        records = query.records
        partial = query.outcome is AccessOutcome.PARTIALLY_ALLOWED
        while records and len(_canonical(records)) > command.maximum_package_bytes:
            records = records[:-1]
            partial = True
        if not records and query.records:
            reasons = ("package_size_limit_exceeded",)
            receipt_id = self._record_receipt(
                command,
                query,
                now=now,
                outcome=AccessOutcome.FAILED,
                package_ref=None,
                reason_codes=reasons,
            )
            return ExportEvidenceResult(
                outcome=AccessOutcome.FAILED,
                receipt_id=receipt_id,
                access_receipt_id=query.receipt_id,
                package=None,
                policy_decision_ref=query.policy_decision_ref,
                reason_codes=reasons,
            )

        payload = _canonical(records)
        integrity_digest = sha256(payload).hexdigest()
        package_id = _stable_id(
            "audit-package",
            command.request_id,
            command.destination_ref,
            integrity_digest,
        )
        record_refs = tuple(
            str(record.get("audit_record_id"))
            for record in records
            if record.get("audit_record_id") is not None
        )
        package = DisclosurePackage(
            package_id=package_id,
            request_id=command.request_id,
            purpose=command.purpose,
            scope=query.effective_scope,
            records=records,
            record_refs=record_refs,
            redaction_profile="policy-field-actions",
            generated_at=now,
            expires_at=command.expires_at,
            chain_of_custody_ref=_stable_id("audit-custody", package_id, "prepared"),
            policy_decision_ref=query.policy_decision_ref or "missing",
            output_class=command.desired_output_class,
            destination_ref=command.destination_ref,
            integrity_algorithm="sha256",
            integrity_digest=integrity_digest,
        )
        try:
            self._store.create_disclosure_package(package)
        except Exception as exc:
            reasons = ("package_persistence_failed", type(exc).__name__)
            receipt_id = self._record_receipt(
                command,
                query,
                now=now,
                outcome=AccessOutcome.FAILED,
                package_ref=None,
                reason_codes=reasons,
            )
            return ExportEvidenceResult(
                outcome=AccessOutcome.FAILED,
                receipt_id=receipt_id,
                access_receipt_id=query.receipt_id,
                package=None,
                policy_decision_ref=query.policy_decision_ref,
                reason_codes=reasons,
            )

        outcome = AccessOutcome.PARTIALLY_ALLOWED if partial else AccessOutcome.ALLOWED
        receipt_id = self._record_receipt(
            command,
            query,
            now=now,
            outcome=outcome,
            package_ref=package.package_id,
            reason_codes=query.reason_codes,
        )
        return ExportEvidenceResult(
            outcome=outcome,
            receipt_id=receipt_id,
            access_receipt_id=query.receipt_id,
            package=package,
            policy_decision_ref=query.policy_decision_ref,
            reason_codes=query.reason_codes,
        )
