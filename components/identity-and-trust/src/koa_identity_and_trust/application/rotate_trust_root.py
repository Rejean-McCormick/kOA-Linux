"""Rotate an exactly scoped trust root through a staged successor lifecycle."""

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
    KeyStore,
    TransitionReceiptRecord,
    TrustRootRecord,
    TrustScope,
)


@dataclass(frozen=True, slots=True)
class RotateTrustRootCommand:
    request_id: str
    idempotency_key: str
    predecessor_ref: str
    successor_public_material_ref: str
    root_type: str
    scope: TrustScope
    owner_ref: str
    valid_from: datetime
    expires_at: datetime
    authority_ref: str
    overlap_until: datetime | None = None
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "evidence_refs", tuple(self.evidence_refs))


@dataclass(frozen=True, slots=True)
class RotateTrustRootResult:
    request_id: str
    predecessor_ref: str
    successor_ref: str
    predecessor_status: str
    successor_status: str
    activated_at: datetime
    overlap_until: datetime | None
    receipt_ref: str


class RotateTrustRoot:
    """Activate a verified successor without broadening trust or using fallback roots."""

    operation_id = "register_trust_root"

    def __init__(self, store: IdentityStore, keys: KeyStore, clock: Clock, audit: AuditSink) -> None:
        self._store = store
        self._keys = keys
        self._clock = clock
        self._audit = audit

    def execute(self, command: RotateTrustRootCommand) -> RotateTrustRootResult:
        request = self._validated(command)
        now = require_utc(self._clock.now(), "clock.now")
        if request.valid_from > now:
            raise InvalidRequest("successor valid_from may not be in the future")
        if request.expires_at <= now:
            raise InvalidRequest("successor must expire after activation")
        if request.overlap_until is not None:
            if request.overlap_until <= now or request.overlap_until >= request.expires_at:
                raise InvalidRequest("overlap_until must be after activation and before successor expiry")

        fingerprint = self._fingerprint(request)
        prior = self._store.get_idempotency(self.operation_id, request.idempotency_key)
        if prior is not None:
            if prior.request_fingerprint != fingerprint:
                raise Conflict("idempotency key conflict", reason_code="idempotency_conflict")
            return self._result_from_response(prior.response)

        predecessor = self._store.get_trust_root(request.predecessor_ref)
        if predecessor is None:
            raise NotFound("predecessor trust root not found", reason_code="trust_root_unavailable")
        if predecessor.status != "active":
            raise Conflict("predecessor trust root is not active", reason_code="trust_root_unavailable")
        if now >= require_utc(predecessor.expires_at, "predecessor.expires_at"):
            raise Conflict("predecessor trust root is expired", reason_code="trust_root_unavailable")
        if predecessor.public_material_ref == request.successor_public_material_ref:
            raise Conflict("successor material must differ from predecessor material", reason_code="state_conflict")
        if request.overlap_until is not None and request.overlap_until > predecessor.expires_at:
            raise InvalidRequest(
                "explicit overlap may not extend predecessor validity",
                reason_code="trust_scope_mismatch",
            )
        if predecessor.owner_ref != request.owner_ref:
            raise Conflict("successor owner differs from predecessor owner", reason_code="trust_scope_mismatch")
        if predecessor.root_type != request.root_type:
            raise Conflict("root type changes require a separate declared migration", reason_code="algorithm_or_version_unsupported")
        if not predecessor.scope.exact_match(request.scope):
            raise Conflict("successor scope must exactly match predecessor scope", reason_code="trust_scope_mismatch")
        active_for_scope = [
            root
            for root in self._store.list_trust_roots(request.scope)
            if root.status == "active" and root.trust_root_id != predecessor.trust_root_id
        ]
        if active_for_scope:
            raise Conflict("another active root already owns the exact scope", reason_code="trust_scope_conflict")

        successor_ref = stable_ref(
            "trust-root",
            request.predecessor_ref,
            request.successor_public_material_ref,
            request.idempotency_key,
        )
        material_id = stable_ref("material", successor_ref, request.request_id)
        receipt_ref = stable_ref("receipt", self.operation_id, request.request_id, successor_ref)

        self._audit.ensure_available(critical=True)
        staged = self._keys.stage_trust_root(
            material_id=material_id,
            public_material_ref=request.successor_public_material_ref,
            root_type=request.root_type,
            scope=request.scope,
            owner_ref=request.owner_ref,
            valid_from=request.valid_from,
            expires_at=request.expires_at,
        )
        staged_active = False
        try:
            proof = self._keys.verify_staged_trust_root(
                staged,
                root_type=request.root_type,
                scope=request.scope,
                owner_ref=request.owner_ref,
                verification_time=now,
            )
            if proof.result != "trusted":
                raise Conflict("successor trust root verification failed", reason_code=proof.reason_code)

            successor = TrustRootRecord(
                trust_root_id=successor_ref,
                root_type=request.root_type,
                public_material_ref=staged.public_material_ref,
                protected_material_ref=staged.material_ref,
                scope=request.scope,
                owner_ref=request.owner_ref,
                status="active",
                activated_at=now,
                expires_at=request.expires_at,
                supersedes_ref=predecessor.trust_root_id,
                evidence_refs=tuple(dict.fromkeys((*request.evidence_refs, *proof.evidence_refs))),
            )
            if request.overlap_until is None:
                predecessor_after = replace(predecessor, status="superseded")
                predecessor_status = "superseded"
            else:
                predecessor_after = replace(predecessor, expires_at=request.overlap_until)
                predecessor_status = "active"
            result = RotateTrustRootResult(
                request_id=request.request_id,
                predecessor_ref=predecessor.trust_root_id,
                successor_ref=successor_ref,
                predecessor_status=predecessor_status,
                successor_status="active",
                activated_at=now,
                overlap_until=request.overlap_until,
                receipt_ref=receipt_ref,
            )
            response = self._response_mapping(result)
            receipt = TransitionReceiptRecord(
                receipt_ref=receipt_ref,
                receipt_class="transition_receipt",
                transition="trust_root_supersession",
                request_id=request.request_id,
                operation_id=self.operation_id,
                subject_refs=(predecessor.trust_root_id, successor_ref),
                outcome="committed",
                reason_code="trust_root_activated",
                occurred_at=now,
                authority_ref=request.authority_ref,
                evidence_refs=successor.evidence_refs,
                details={
                    "explicit_overlap": "true" if request.overlap_until is not None else "false",
                    "root_type": request.root_type,
                },
            )
            event = AuditEvent(
                event_id=stable_ref("event", self.operation_id, request.request_id, successor_ref),
                operation_id=self.operation_id,
                request_id=request.request_id,
                event_type="trust_root_activated",
                outcome="committed",
                occurred_at=now,
                subject_refs=(predecessor.trust_root_id, successor_ref),
                reason_code="trust_root_activated",
                receipt_ref=receipt_ref,
                evidence_refs=successor.evidence_refs,
                details={
                    "explicit_overlap": "true" if request.overlap_until is not None else "false",
                    "root_type": request.root_type,
                },
            )

            with self._store.transaction():
                self._store.put_trust_root(predecessor_after)
                self._store.put_trust_root(successor)
                self._keys.activate_material(staged.material_ref, activated_at=now)
                staged_active = True
                self._store.append_receipt(receipt)
                self._store.put_idempotency(
                    IdempotencyRecord(
                        operation_id=self.operation_id,
                        idempotency_key=request.idempotency_key,
                        request_fingerprint=fingerprint,
                        response=response,
                        created_at=now,
                    )
                )
                self._audit.publish(event)
            return result
        except Exception:
            if staged_active:
                self._keys.revoke_material(
                    staged.material_ref,
                    revoked_at=now,
                    reason_code="transition_rolled_back",
                )
            else:
                self._keys.discard_staged_material(staged.material_ref)
            raise

    @staticmethod
    def _validated(command: RotateTrustRootCommand) -> RotateTrustRootCommand:
        evidence = tuple(dict.fromkeys(require_text(value, "evidence_ref") for value in command.evidence_refs))
        return RotateTrustRootCommand(
            request_id=require_text(command.request_id, "request_id"),
            idempotency_key=require_text(command.idempotency_key, "idempotency_key"),
            predecessor_ref=require_text(command.predecessor_ref, "predecessor_ref"),
            successor_public_material_ref=require_text(
                command.successor_public_material_ref,
                "successor_public_material_ref",
            ),
            root_type=require_text(command.root_type, "root_type"),
            scope=command.scope,
            owner_ref=require_text(command.owner_ref, "owner_ref"),
            valid_from=require_utc(command.valid_from, "valid_from"),
            expires_at=require_utc(command.expires_at, "expires_at"),
            authority_ref=require_text(command.authority_ref, "authority_ref"),
            overlap_until=(
                require_utc(command.overlap_until, "overlap_until")
                if command.overlap_until is not None
                else None
            ),
            evidence_refs=evidence,
        )

    @staticmethod
    def _fingerprint(command: RotateTrustRootCommand) -> str:
        return sha256(
            canonical_json(
                {
                    "request_id": command.request_id,
                    "predecessor_ref": command.predecessor_ref,
                    "successor_public_material_ref": command.successor_public_material_ref,
                    "root_type": command.root_type,
                    "scope": dict(command.scope.as_mapping()),
                    "owner_ref": command.owner_ref,
                    "valid_from": command.valid_from.isoformat(),
                    "expires_at": command.expires_at.isoformat(),
                    "authority_ref": command.authority_ref,
                    "overlap_until": command.overlap_until.isoformat() if command.overlap_until else None,
                    "evidence_refs": command.evidence_refs,
                }
            ).encode("utf-8")
        ).hexdigest()

    @staticmethod
    def _response_mapping(result: RotateTrustRootResult) -> Mapping[str, str]:
        return {
            "request_id": result.request_id,
            "predecessor_ref": result.predecessor_ref,
            "successor_ref": result.successor_ref,
            "predecessor_status": result.predecessor_status,
            "successor_status": result.successor_status,
            "activated_at": result.activated_at.isoformat(),
            "overlap_until": result.overlap_until.isoformat() if result.overlap_until else "",
            "receipt_ref": result.receipt_ref,
        }

    @staticmethod
    def _result_from_response(response: Mapping[str, str]) -> RotateTrustRootResult:
        return RotateTrustRootResult(
            request_id=response["request_id"],
            predecessor_ref=response["predecessor_ref"],
            successor_ref=response["successor_ref"],
            predecessor_status=response["predecessor_status"],
            successor_status=response["successor_status"],
            activated_at=require_utc(datetime.fromisoformat(response["activated_at"]), "activated_at"),
            overlap_until=(
                require_utc(datetime.fromisoformat(response["overlap_until"]), "overlap_until")
                if response["overlap_until"]
                else None
            ),
            receipt_ref=response["receipt_ref"],
        )
