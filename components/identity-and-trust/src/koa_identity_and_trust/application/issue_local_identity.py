"""Issue and atomically activate a bounded local identity and credential."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
from typing import Mapping

from . import Conflict, InvalidRequest, canonical_json, require_text, require_utc, stable_ref
from ..ports import (
    AuditEvent,
    AuditSink,
    Clock,
    CredentialRecord,
    IdempotencyRecord,
    IdentityRecord,
    IdentityStore,
    KeyStore,
    TransitionReceiptRecord,
    TrustScope,
)

_SUBJECT_TYPES = frozenset(
    {
        "human",
        "service",
        "component_instance",
        "node",
        "device",
        "workspace",
        "tenant",
        "organization",
        "external_integration",
        "artifact_signer",
        "recovery_operator",
    }
)
_CREDENTIAL_TYPES = frozenset(
    {
        "password_verifier",
        "public_key",
        "x509_certificate",
        "ssh_certificate",
        "service_token",
        "device_credential",
        "recovery_code",
        "attestation_credential",
    }
)


@dataclass(frozen=True, slots=True)
class IssueLocalIdentityCommand:
    request_id: str
    idempotency_key: str
    subject_type: str
    display_name: str
    owner_ref: str
    tenant_ref: str | None
    environment: str
    credential_type: str
    scope: TrustScope
    not_before: datetime
    expires_at: datetime
    issuer_authority_ref: str
    intended_uses: tuple[str, ...]
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "intended_uses", tuple(self.intended_uses))
        object.__setattr__(self, "evidence_refs", tuple(self.evidence_refs))


@dataclass(frozen=True, slots=True)
class IssueLocalIdentityResult:
    request_id: str
    identity_ref: str
    credential_ref: str
    status: str
    issued_at: datetime
    expires_at: datetime
    receipt_ref: str
    authorizes_business_action: bool = False


class IssueLocalIdentity:
    """Coordinate local identity activation without creating business authority."""

    operation_id = "issue_credential"

    def __init__(self, store: IdentityStore, keys: KeyStore, clock: Clock, audit: AuditSink) -> None:
        self._store = store
        self._keys = keys
        self._clock = clock
        self._audit = audit

    def execute(self, command: IssueLocalIdentityCommand) -> IssueLocalIdentityResult:
        request = self._validated(command)
        now = require_utc(self._clock.now(), "clock.now")
        if request.not_before > now:
            raise InvalidRequest("not_before may not be later than the activation time")
        if request.expires_at <= now:
            raise InvalidRequest("expires_at must be later than the activation time")

        fingerprint = self._fingerprint(request)
        prior = self._store.get_idempotency(self.operation_id, request.idempotency_key)
        if prior is not None:
            if prior.request_fingerprint != fingerprint:
                raise Conflict(
                    "idempotency key was already used with different inputs",
                    reason_code="idempotency_conflict",
                )
            return self._result_from_response(prior.response)

        existing = self._store.find_identity(
            owner_ref=request.owner_ref,
            tenant_ref=request.tenant_ref,
            environment=request.environment,
            subject_type=request.subject_type,
        )
        if existing is not None:
            raise Conflict(
                "an identity identifier already exists or is permanently reserved for this owner and scope",
                reason_code="identity_already_exists",
            )

        identity_ref = stable_ref(
            "identity",
            request.owner_ref,
            request.tenant_ref or "-",
            request.environment,
            request.subject_type,
        )
        credential_ref = stable_ref("credential", identity_ref, request.idempotency_key)
        material_id = stable_ref("material", credential_ref, request.request_id)
        receipt_ref = stable_ref("receipt", self.operation_id, request.request_id)
        event_id = stable_ref("event", self.operation_id, request.request_id)

        self._audit.ensure_available(critical=True)
        staged = self._keys.stage_credential_material(
            material_id=material_id,
            subject_identity_id=identity_ref,
            credential_type=request.credential_type,
            scope=request.scope,
            not_before=request.not_before,
            expires_at=request.expires_at,
        )
        staged_active = False
        try:
            proof = self._keys.verify_staged_credential_material(
                staged,
                subject_identity_id=identity_ref,
                credential_type=request.credential_type,
                scope=request.scope,
            )
            if proof.result != "trusted":
                raise Conflict(
                    "staged credential material could not be verified",
                    reason_code=proof.reason_code,
                )

            identity = IdentityRecord(
                identity_id=identity_ref,
                subject_type=request.subject_type,
                display_name=request.display_name,
                owner_ref=request.owner_ref,
                tenant_ref=request.tenant_ref,
                environment=request.environment,
                status="active",
                created_at=now,
                activated_at=now,
                expires_at=request.expires_at,
                credential_refs=(credential_ref,),
                evidence_refs=request.evidence_refs,
            )
            credential = CredentialRecord(
                credential_id=credential_ref,
                subject_identity_id=identity_ref,
                credential_type=request.credential_type,
                issuer_ref=request.issuer_authority_ref,
                scope=request.scope,
                issued_at=now,
                not_before=request.not_before,
                expires_at=request.expires_at,
                status="active",
                key_or_material_reference=staged.material_ref,
                revocation_reference=stable_ref("revocation", credential_ref),
                version=staged.version,
                intended_uses=request.intended_uses,
                evidence_refs=tuple(dict.fromkeys((*request.evidence_refs, *proof.evidence_refs))),
            )
            result = IssueLocalIdentityResult(
                request_id=request.request_id,
                identity_ref=identity_ref,
                credential_ref=credential_ref,
                status="active",
                issued_at=now,
                expires_at=request.expires_at,
                receipt_ref=receipt_ref,
            )
            response = self._response_mapping(result)
            receipt = TransitionReceiptRecord(
                receipt_ref=receipt_ref,
                receipt_class="transition_receipt",
                transition="identity_activation_and_credential_issuance",
                request_id=request.request_id,
                operation_id=self.operation_id,
                subject_refs=(identity_ref, credential_ref),
                outcome="committed",
                reason_code="credential_issued",
                occurred_at=now,
                authority_ref=request.issuer_authority_ref,
                evidence_refs=credential.evidence_refs,
                details={"credential_type": request.credential_type, "subject_type": request.subject_type},
            )
            event = AuditEvent(
                event_id=event_id,
                operation_id=self.operation_id,
                request_id=request.request_id,
                event_type="credential_issued",
                outcome="committed",
                occurred_at=now,
                subject_refs=(identity_ref, credential_ref),
                reason_code="credential_issued",
                receipt_ref=receipt_ref,
                evidence_refs=credential.evidence_refs,
                details={"credential_type": request.credential_type, "subject_type": request.subject_type},
            )

            with self._store.transaction():
                self._store.put_identity(identity)
                self._store.put_credential(credential)
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
    def _validated(command: IssueLocalIdentityCommand) -> IssueLocalIdentityCommand:
        request_id = require_text(command.request_id, "request_id")
        idempotency_key = require_text(command.idempotency_key, "idempotency_key")
        subject_type = require_text(command.subject_type, "subject_type")
        if subject_type not in _SUBJECT_TYPES:
            raise InvalidRequest("unsupported subject_type", reason_code="unsupported_subject_type")
        credential_type = require_text(command.credential_type, "credential_type")
        if credential_type not in _CREDENTIAL_TYPES:
            raise InvalidRequest("unsupported credential_type", reason_code="algorithm_or_version_unsupported")
        intended_uses = tuple(dict.fromkeys(require_text(value, "intended_use") for value in command.intended_uses))
        if not intended_uses:
            raise InvalidRequest("at least one intended use is required")
        if command.scope.tenant != command.tenant_ref:
            raise InvalidRequest("credential scope tenant must exactly match tenant_ref", reason_code="trust_scope_mismatch")
        if command.scope.environment != command.environment:
            raise InvalidRequest(
                "credential scope environment must exactly match environment",
                reason_code="trust_scope_mismatch",
            )
        if command.scope.purpose is not None and command.scope.purpose not in intended_uses:
            raise InvalidRequest("scope purpose must be one of intended_uses", reason_code="trust_scope_mismatch")
        evidence = tuple(dict.fromkeys(require_text(value, "evidence_ref") for value in command.evidence_refs))
        return IssueLocalIdentityCommand(
            request_id=request_id,
            idempotency_key=idempotency_key,
            subject_type=subject_type,
            display_name=require_text(command.display_name, "display_name"),
            owner_ref=require_text(command.owner_ref, "owner_ref"),
            tenant_ref=require_text(command.tenant_ref, "tenant_ref") if command.tenant_ref is not None else None,
            environment=require_text(command.environment, "environment"),
            credential_type=credential_type,
            scope=command.scope,
            not_before=require_utc(command.not_before, "not_before"),
            expires_at=require_utc(command.expires_at, "expires_at"),
            issuer_authority_ref=require_text(command.issuer_authority_ref, "issuer_authority_ref"),
            intended_uses=intended_uses,
            evidence_refs=evidence,
        )

    @staticmethod
    def _fingerprint(command: IssueLocalIdentityCommand) -> str:
        material = {
            "request_id": command.request_id,
            "subject_type": command.subject_type,
            "display_name": command.display_name,
            "owner_ref": command.owner_ref,
            "tenant_ref": command.tenant_ref,
            "environment": command.environment,
            "credential_type": command.credential_type,
            "scope": dict(command.scope.as_mapping()),
            "not_before": command.not_before.isoformat(),
            "expires_at": command.expires_at.isoformat(),
            "issuer_authority_ref": command.issuer_authority_ref,
            "intended_uses": command.intended_uses,
            "evidence_refs": command.evidence_refs,
        }
        return sha256(canonical_json(material).encode("utf-8")).hexdigest()

    @staticmethod
    def _response_mapping(result: IssueLocalIdentityResult) -> Mapping[str, str]:
        return {
            "request_id": result.request_id,
            "identity_ref": result.identity_ref,
            "credential_ref": result.credential_ref,
            "status": result.status,
            "issued_at": result.issued_at.isoformat(),
            "expires_at": result.expires_at.isoformat(),
            "receipt_ref": result.receipt_ref,
            "authorizes_business_action": "false",
        }

    @staticmethod
    def _result_from_response(response: Mapping[str, str]) -> IssueLocalIdentityResult:
        return IssueLocalIdentityResult(
            request_id=response["request_id"],
            identity_ref=response["identity_ref"],
            credential_ref=response["credential_ref"],
            status=response["status"],
            issued_at=require_utc(datetime.fromisoformat(response["issued_at"]), "issued_at"),
            expires_at=require_utc(datetime.fromisoformat(response["expires_at"]), "expires_at"),
            receipt_ref=response["receipt_ref"],
        )
