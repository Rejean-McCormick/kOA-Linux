from __future__ import annotations

from contextlib import contextmanager
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path
import sys
from typing import Iterator, Mapping

import pytest

SRC = Path(__file__).resolve().parents[2] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from koa_identity_and_trust.application import (  # noqa: E402
    Conflict,
    InvalidRequest,
    IssueLocalIdentity,
    IssueLocalIdentityCommand,
    NotFound,
    ResolveSession,
    ResolveSessionCommand,
    RevokeCredential,
    RevokeCredentialCommand,
    RotateTrustRoot,
    RotateTrustRootCommand,
    VerifyCredential,
    VerifyCredentialCommand,
)
from koa_identity_and_trust.ports import (  # noqa: E402
    AuditEvent,
    CredentialRecord,
    IdempotencyRecord,
    IdentityRecord,
    KeyMaterialRef,
    ProofVerification,
    SessionRecord,
    TransitionReceiptRecord,
    TrustRootRecord,
    TrustScope,
    VerificationRecord,
)

NOW = datetime(2026, 8, 6, 13, 0, tzinfo=UTC)
SCOPE = TrustScope(
    tenant="tenant-a",
    environment="production",
    component="identity_and_trust",
    purpose="authenticate",
)


class FixedClock:
    def __init__(self, current: datetime = NOW) -> None:
        self.current = current

    def now(self) -> datetime:
        return self.current


class MemoryStore:
    def __init__(self) -> None:
        self.identities: dict[str, IdentityRecord] = {}
        self.credentials: dict[str, CredentialRecord] = {}
        self.roots: dict[str, TrustRootRecord] = {}
        self.sessions: dict[str, SessionRecord] = {}
        self.verifications: list[VerificationRecord] = []
        self.receipts: list[TransitionReceiptRecord] = []
        self.idempotency: dict[tuple[str, str], IdempotencyRecord] = {}

    @contextmanager
    def transaction(self) -> Iterator[None]:
        snapshot = (
            self.identities.copy(),
            self.credentials.copy(),
            self.roots.copy(),
            self.sessions.copy(),
            self.verifications.copy(),
            self.receipts.copy(),
            self.idempotency.copy(),
        )
        try:
            yield
        except Exception:
            (
                self.identities,
                self.credentials,
                self.roots,
                self.sessions,
                self.verifications,
                self.receipts,
                self.idempotency,
            ) = snapshot
            raise

    def get_identity(self, identity_id: str) -> IdentityRecord | None:
        return self.identities.get(identity_id)

    def find_identity(
        self,
        *,
        owner_ref: str,
        tenant_ref: str | None,
        environment: str,
        subject_type: str,
    ) -> IdentityRecord | None:
        return next(
            (
                record
                for record in self.identities.values()
                if record.owner_ref == owner_ref
                and record.tenant_ref == tenant_ref
                and record.environment == environment
                and record.subject_type == subject_type
            ),
            None,
        )

    def put_identity(self, record: IdentityRecord) -> None:
        self.identities[record.identity_id] = record

    def get_credential(self, credential_id: str) -> CredentialRecord | None:
        return self.credentials.get(credential_id)

    def put_credential(self, record: CredentialRecord) -> None:
        self.credentials[record.credential_id] = record

    def get_trust_root(self, trust_root_id: str) -> TrustRootRecord | None:
        return self.roots.get(trust_root_id)

    def list_trust_roots(self, scope: TrustScope) -> list[TrustRootRecord]:
        return [record for record in self.roots.values() if record.scope.exact_match(scope)]

    def put_trust_root(self, record: TrustRootRecord) -> None:
        self.roots[record.trust_root_id] = record

    def get_session(self, session_id: str) -> SessionRecord | None:
        return self.sessions.get(session_id)

    def put_session(self, record: SessionRecord) -> None:
        self.sessions[record.session_id] = record

    def invalidate_sessions_for_credential(self, credential_id: str, *, effective_at: datetime) -> int:
        count = 0
        for session_id, session in tuple(self.sessions.items()):
            if session.credential_id == credential_id and session.status == "active":
                self.sessions[session_id] = replace(session, status="revoked", revoked_at=effective_at)
                count += 1
        return count

    def append_verification(self, record: VerificationRecord) -> None:
        self.verifications.append(record)

    def append_receipt(self, record: TransitionReceiptRecord) -> None:
        self.receipts.append(record)

    def get_idempotency(self, operation_id: str, idempotency_key: str) -> IdempotencyRecord | None:
        return self.idempotency.get((operation_id, idempotency_key))

    def put_idempotency(self, record: IdempotencyRecord) -> None:
        self.idempotency[(record.operation_id, record.idempotency_key)] = record


class FakeKeyStore:
    def __init__(self) -> None:
        self.credential_result = ProofVerification("trusted", "ed25519", "credential_valid", ("evidence:key",))
        self.root_result = ProofVerification("trusted", "ed25519", "trust_root_valid", ("evidence:root",))
        self.staged: list[str] = []
        self.activated: list[str] = []
        self.retired: list[str] = []
        self.revoked: list[tuple[str, str]] = []
        self.discarded: list[str] = []
        self.proofs: list[bytes] = []

    def stage_credential_material(self, **kwargs: object) -> KeyMaterialRef:
        material_id = str(kwargs["material_id"])
        self.staged.append(material_id)
        return KeyMaterialRef(material_id, f"public:{material_id}", "memory", "ed25519", "1", "staged")

    def verify_staged_credential_material(self, material: KeyMaterialRef, **kwargs: object) -> ProofVerification:
        return self.credential_result

    def verify_credential(
        self,
        *,
        material_ref: str,
        presented_proof: bytes,
        intended_use: str,
        context: Mapping[str, str],
        verification_time: datetime,
    ) -> ProofVerification:
        self.proofs.append(presented_proof)
        return self.credential_result

    def stage_trust_root(self, **kwargs: object) -> KeyMaterialRef:
        material_id = str(kwargs["material_id"])
        public = str(kwargs["public_material_ref"])
        self.staged.append(material_id)
        return KeyMaterialRef(material_id, public, "memory", "ed25519", "1", "staged")

    def verify_staged_trust_root(self, material: KeyMaterialRef, **kwargs: object) -> ProofVerification:
        return self.root_result

    def activate_material(self, material_ref: str, *, activated_at: datetime) -> None:
        self.activated.append(material_ref)

    def retire_material(self, material_ref: str, *, retired_at: datetime) -> None:
        self.retired.append(material_ref)

    def revoke_material(self, material_ref: str, *, revoked_at: datetime, reason_code: str) -> None:
        self.revoked.append((material_ref, reason_code))

    def discard_staged_material(self, material_ref: str) -> None:
        self.discarded.append(material_ref)


class FakeAudit:
    def __init__(self, *, available: bool = True, fail_publish: bool = False) -> None:
        self.available = available
        self.fail_publish = fail_publish
        self.events: list[AuditEvent] = []
        self.availability_checks: list[bool] = []

    def ensure_available(self, *, critical: bool) -> None:
        self.availability_checks.append(critical)
        if not self.available:
            raise RuntimeError("audit unavailable")

    def publish(self, event: AuditEvent) -> None:
        if self.fail_publish:
            raise RuntimeError("audit publish failed")
        self.events.append(event)


def identity(identity_id: str = "identity-1", *, status: str = "active") -> IdentityRecord:
    return IdentityRecord(
        identity_id=identity_id,
        subject_type="service",
        display_name="Service One",
        owner_ref="owner-1",
        tenant_ref="tenant-a",
        environment="production",
        status=status,  # type: ignore[arg-type]
        created_at=NOW - timedelta(days=10),
        activated_at=NOW - timedelta(days=10),
        expires_at=NOW + timedelta(days=30),
        credential_refs=("credential-1",),
    )


def credential(
    credential_id: str = "credential-1",
    *,
    status: str = "active",
    expires_at: datetime | None = None,
    scope: TrustScope = SCOPE,
) -> CredentialRecord:
    return CredentialRecord(
        credential_id=credential_id,
        subject_identity_id="identity-1",
        credential_type="service_token",
        issuer_ref="issuer-1",
        scope=scope,
        issued_at=NOW - timedelta(days=1),
        not_before=NOW - timedelta(days=1),
        expires_at=expires_at or NOW + timedelta(days=1),
        status=status,  # type: ignore[arg-type]
        key_or_material_reference="material-1",
        revocation_reference="revocation-1",
        intended_uses=("authenticate",),
    )


def root(root_id: str = "root-1", *, scope: TrustScope = SCOPE, status: str = "active") -> TrustRootRecord:
    return TrustRootRecord(
        trust_root_id=root_id,
        root_type="ed25519_public_key",
        public_material_ref=f"public:{root_id}",
        protected_material_ref=f"material:{root_id}",
        scope=scope,
        owner_ref="owner-1",
        status=status,  # type: ignore[arg-type]
        activated_at=NOW - timedelta(days=30),
        expires_at=NOW + timedelta(days=30),
    )


def issue_command(**overrides: object) -> IssueLocalIdentityCommand:
    values: dict[str, object] = {
        "request_id": "request-issue-1",
        "idempotency_key": "idem-issue-1",
        "subject_type": "service",
        "display_name": "Local Service",
        "owner_ref": "owner-local",
        "tenant_ref": "tenant-a",
        "environment": "production",
        "credential_type": "service_token",
        "scope": SCOPE,
        "not_before": NOW - timedelta(seconds=1),
        "expires_at": NOW + timedelta(days=7),
        "issuer_authority_ref": "issuer-authority-1",
        "intended_uses": ("authenticate",),
        "evidence_refs": ("evidence:enrollment",),
    }
    values.update(overrides)
    return IssueLocalIdentityCommand(**values)  # type: ignore[arg-type]


def seeded_store() -> MemoryStore:
    store = MemoryStore()
    store.put_identity(identity())
    store.put_credential(credential())
    store.put_session(
        SessionRecord(
            session_id="session-1",
            identity_id="identity-1",
            credential_id="credential-1",
            tenant_ref="tenant-a",
            environment="production",
            assurance_context={"level": "local-strong"},
            issued_at=NOW - timedelta(hours=1),
            expires_at=NOW + timedelta(hours=1),
        )
    )
    return store


def test_trust_scope_rejects_global_unscoped_root() -> None:
    with pytest.raises(ValueError, match="unscoped"):
        TrustScope(None, None)


def test_audit_event_rejects_sensitive_details() -> None:
    with pytest.raises(ValueError, match="protected material"):
        AuditEvent("e", "op", "r", "type", "ok", NOW, details={"private_key": "x"})


def test_issue_local_identity_activates_records_and_receipt() -> None:
    store, keys, audit = MemoryStore(), FakeKeyStore(), FakeAudit()
    result = IssueLocalIdentity(store, keys, FixedClock(), audit).execute(issue_command())
    assert result.status == "active"
    assert result.authorizes_business_action is False
    assert store.identities[result.identity_ref].status == "active"
    assert store.credentials[result.credential_ref].status == "active"
    assert store.receipts[0].transition == "identity_activation_and_credential_issuance"
    assert audit.events[0].event_type == "credential_issued"
    assert keys.activated


def test_issue_local_identity_is_idempotent() -> None:
    store, keys, audit = MemoryStore(), FakeKeyStore(), FakeAudit()
    service = IssueLocalIdentity(store, keys, FixedClock(), audit)
    first = service.execute(issue_command())
    second = service.execute(issue_command())
    assert second == first
    assert len(store.identities) == 1
    assert len(keys.staged) == 1


def test_issue_local_identity_rejects_idempotency_conflict() -> None:
    store, keys, audit = MemoryStore(), FakeKeyStore(), FakeAudit()
    service = IssueLocalIdentity(store, keys, FixedClock(), audit)
    service.execute(issue_command())
    with pytest.raises(Conflict, match="different inputs"):
        service.execute(issue_command(display_name="Different"))


def test_issue_local_identity_rejects_scope_broadening() -> None:
    wrong = TrustScope("other-tenant", "production", component="identity_and_trust", purpose="authenticate")
    with pytest.raises(InvalidRequest, match="tenant"):
        IssueLocalIdentity(MemoryStore(), FakeKeyStore(), FixedClock(), FakeAudit()).execute(
            issue_command(scope=wrong)
        )




def test_issue_local_identity_never_reuses_a_retired_identifier() -> None:
    store = MemoryStore()
    retired = identity(
        identity_id="reserved",
        status="retired",
    )
    retired = replace(
        retired,
        owner_ref="owner-local",
        display_name="Retired Local Service",
        credential_refs=(),
    )
    store.put_identity(retired)
    with pytest.raises(Conflict) as error:
        IssueLocalIdentity(store, FakeKeyStore(), FixedClock(), FakeAudit()).execute(issue_command())
    assert error.value.reason_code == "identity_already_exists"


def test_issue_local_identity_fails_before_key_staging_without_audit() -> None:
    keys = FakeKeyStore()
    with pytest.raises(RuntimeError, match="audit unavailable"):
        IssueLocalIdentity(MemoryStore(), keys, FixedClock(), FakeAudit(available=False)).execute(issue_command())
    assert keys.staged == []


def test_issue_rolls_back_store_and_revokes_activated_material_when_audit_publish_fails() -> None:
    store, keys = MemoryStore(), FakeKeyStore()
    with pytest.raises(RuntimeError, match="publish failed"):
        IssueLocalIdentity(store, keys, FixedClock(), FakeAudit(fail_publish=True)).execute(issue_command())
    assert store.identities == {}
    assert store.credentials == {}
    assert keys.revoked[0][1] == "transition_rolled_back"


def test_verify_credential_returns_trusted_without_authorizing_action() -> None:
    store, keys, audit = seeded_store(), FakeKeyStore(), FakeAudit()
    result = VerifyCredential(store, keys, FixedClock(), audit).execute(
        VerifyCredentialCommand("request-v-1", "credential-1", b"proof", "authenticate", "tenant-a", "production")
    )
    assert result.trust_result == "trusted"
    assert result.identity_ref == "identity-1"
    assert result.authorizes_business_action is False
    assert len(store.verifications) == 1
    assert keys.proofs == [b"proof"]


@pytest.mark.parametrize(
    ("status", "expected"),
    [("revoked", "credential_revoked"), ("expired", "credential_expired"), ("suspended", "credential_not_active")],
)
def test_verify_credential_rejects_inactive_states(status: str, expected: str) -> None:
    store = seeded_store()
    store.put_credential(credential(status=status))
    result = VerifyCredential(store, FakeKeyStore(), FixedClock(), FakeAudit()).execute(
        VerifyCredentialCommand("request-v-state", "credential-1", b"proof", "authenticate", "tenant-a", "production")
    )
    assert result.trust_result == "untrusted"
    assert result.reason_code == expected


def test_verify_credential_rejects_expired_timestamp() -> None:
    store = seeded_store()
    store.put_credential(credential(expires_at=NOW))
    result = VerifyCredential(store, FakeKeyStore(), FixedClock(), FakeAudit()).execute(
        VerifyCredentialCommand("request-v-exp", "credential-1", b"proof", "authenticate", "tenant-a", "production")
    )
    assert result.reason_code == "credential_expired"


def test_verify_credential_rejects_scope_mismatch_without_calling_provider() -> None:
    keys = FakeKeyStore()
    result = VerifyCredential(seeded_store(), keys, FixedClock(), FakeAudit()).execute(
        VerifyCredentialCommand("request-v-scope", "credential-1", b"proof", "authenticate", "tenant-b", "production")
    )
    assert result.trust_result == "untrusted"
    assert result.reason_code == "trust_scope_mismatch"
    assert keys.proofs == []


def test_verify_credential_propagates_provider_indeterminate_result() -> None:
    keys = FakeKeyStore()
    keys.credential_result = ProofVerification("indeterminate", None, "private_key_provider_unavailable")
    result = VerifyCredential(seeded_store(), keys, FixedClock(), FakeAudit()).execute(
        VerifyCredentialCommand("request-v-provider", "credential-1", b"proof", "authenticate", "tenant-a", "production")
    )
    assert result.trust_result == "indeterminate"
    assert result.reason_code == "private_key_provider_unavailable"


def test_verify_credential_fails_closed_when_receipt_path_unavailable() -> None:
    result = VerifyCredential(seeded_store(), FakeKeyStore(), FixedClock(), FakeAudit(available=False)).execute(
        VerifyCredentialCommand("request-v-audit", "credential-1", b"proof", "authenticate", "tenant-a", "production")
    )
    assert result.trust_result == "indeterminate"
    assert result.reason_code == "receipt_path_unavailable"


def test_resolve_session_establishes_identity_but_not_authority() -> None:
    result = ResolveSession(seeded_store(), FixedClock(), FakeAudit()).execute(
        ResolveSessionCommand("request-s-1", "session-1", "tenant-a", "production", "authenticate")
    )
    assert result.identity_result == "established"
    assert result.identity_ref == "identity-1"
    assert result.assurance_context == {"level": "local-strong"}
    assert result.authorizes_business_action is False


def test_resolve_session_fails_when_credential_revoked() -> None:
    store = seeded_store()
    store.put_credential(credential(status="revoked"))
    result = ResolveSession(store, FixedClock(), FakeAudit()).execute(
        ResolveSessionCommand("request-s-revoked", "session-1", "tenant-a", "production", "read")
    )
    assert result.identity_result == "not_established"
    assert result.reason_code == "credential_revoked"


def test_resolve_session_returns_indeterminate_for_missing_identity_record() -> None:
    store = seeded_store()
    store.identities.clear()
    result = ResolveSession(store, FixedClock(), FakeAudit()).execute(
        ResolveSessionCommand("request-s-missing", "session-1", "tenant-a", "production", "read")
    )
    assert result.identity_result == "indeterminate"
    assert result.reason_code == "identity_result_indeterminate"


def test_resolve_session_rejects_cross_tenant_use() -> None:
    result = ResolveSession(seeded_store(), FixedClock(), FakeAudit()).execute(
        ResolveSessionCommand("request-s-scope", "session-1", "tenant-b", "production", "read")
    )
    assert result.identity_result == "not_established"
    assert result.reason_code == "trust_scope_mismatch"




def test_verify_credential_rejects_expired_identity() -> None:
    store = seeded_store()
    store.put_identity(replace(identity(), expires_at=NOW))
    result = VerifyCredential(store, FakeKeyStore(), FixedClock(), FakeAudit()).execute(
        VerifyCredentialCommand("request-v-id-exp", "credential-1", b"proof", "authenticate", "tenant-a", "production")
    )
    assert result.trust_result == "untrusted"
    assert result.reason_code == "identity_not_established"


def test_resolve_session_rejects_undeclared_intended_use() -> None:
    result = ResolveSession(seeded_store(), FixedClock(), FakeAudit()).execute(
        ResolveSessionCommand("request-s-use", "session-1", "tenant-a", "production", "admin")
    )
    assert result.identity_result == "not_established"
    assert result.reason_code == "trust_scope_mismatch"


def test_revoke_credential_invalidates_sessions_and_writes_receipt() -> None:
    store, audit = seeded_store(), FakeAudit()
    result = RevokeCredential(store, FixedClock(), audit).execute(
        RevokeCredentialCommand(
            "request-r-1",
            "idem-r-1",
            "credential-1",
            SCOPE,
            "security_incident",
            "authority-1",
        )
    )
    assert result.resulting_status == "revoked"
    assert result.invalidated_sessions == 1
    assert store.credentials["credential-1"].status == "revoked"
    assert store.sessions["session-1"].status == "revoked"
    assert store.receipts[-1].transition == "credential_revocation"
    assert audit.events[-1].event_type == "credential_revoked"


def test_revoke_credential_is_idempotent() -> None:
    store = seeded_store()
    service = RevokeCredential(store, FixedClock(), FakeAudit())
    command = RevokeCredentialCommand(
        "request-r-idem", "idem-r-idem", "credential-1", SCOPE, "security_incident", "authority-1"
    )
    first = service.execute(command)
    second = service.execute(command)
    assert second == first


def test_revoke_credential_rejects_scope_mismatch() -> None:
    wrong = TrustScope("tenant-b", "production", component="identity_and_trust", purpose="authenticate")
    with pytest.raises(Conflict) as error:
        RevokeCredential(seeded_store(), FixedClock(), FakeAudit()).execute(
            RevokeCredentialCommand("request-r-scope", "idem-r-scope", "credential-1", wrong, "incident", "authority")
        )
    assert error.value.reason_code == "trust_scope_mismatch"


def test_revoke_credential_rejects_future_effective_time() -> None:
    with pytest.raises(InvalidRequest, match="future"):
        RevokeCredential(seeded_store(), FixedClock(), FakeAudit()).execute(
            RevokeCredentialCommand(
                "request-r-future",
                "idem-r-future",
                "credential-1",
                SCOPE,
                "incident",
                "authority",
                NOW + timedelta(seconds=1),
            )
        )


def test_revoke_credential_reports_missing_target() -> None:
    with pytest.raises(NotFound):
        RevokeCredential(MemoryStore(), FixedClock(), FakeAudit()).execute(
            RevokeCredentialCommand("request-r-missing", "idem-r-missing", "missing", SCOPE, "incident", "authority")
        )


def rotate_command(**overrides: object) -> RotateTrustRootCommand:
    values: dict[str, object] = {
        "request_id": "request-root-1",
        "idempotency_key": "idem-root-1",
        "predecessor_ref": "root-1",
        "successor_public_material_ref": "public:root-2",
        "root_type": "ed25519_public_key",
        "scope": SCOPE,
        "owner_ref": "owner-1",
        "valid_from": NOW - timedelta(seconds=1),
        "expires_at": NOW + timedelta(days=365),
        "authority_ref": "authority-root-1",
        "evidence_refs": ("evidence:ceremony",),
    }
    values.update(overrides)
    return RotateTrustRootCommand(**values)  # type: ignore[arg-type]


def test_rotate_trust_root_supersedes_and_retires_predecessor() -> None:
    store, keys, audit = MemoryStore(), FakeKeyStore(), FakeAudit()
    store.put_trust_root(root())
    result = RotateTrustRoot(store, keys, FixedClock(), audit).execute(rotate_command())
    assert result.successor_status == "active"
    assert result.predecessor_status == "superseded"
    assert store.roots["root-1"].status == "superseded"
    assert store.roots[result.successor_ref].scope.exact_match(SCOPE)
    assert keys.retired == []
    assert store.receipts[-1].transition == "trust_root_supersession"


def test_rotate_trust_root_supports_only_explicit_bounded_overlap() -> None:
    store, keys = MemoryStore(), FakeKeyStore()
    store.put_trust_root(root())
    overlap = NOW + timedelta(hours=2)
    result = RotateTrustRoot(store, keys, FixedClock(), FakeAudit()).execute(
        rotate_command(overlap_until=overlap)
    )
    assert result.predecessor_status == "active"
    assert store.roots["root-1"].expires_at == overlap
    assert keys.retired == []


def test_rotate_trust_root_rejects_scope_expansion() -> None:
    store = MemoryStore()
    store.put_trust_root(root())
    broader = TrustScope("tenant-a", "production", purpose="authenticate")
    with pytest.raises(Conflict) as error:
        RotateTrustRoot(store, FakeKeyStore(), FixedClock(), FakeAudit()).execute(
            rotate_command(scope=broader)
        )
    assert error.value.reason_code == "trust_scope_mismatch"


def test_rotate_trust_root_does_not_extend_predecessor_during_overlap() -> None:
    store = MemoryStore()
    store.put_trust_root(root())
    with pytest.raises(InvalidRequest) as error:
        RotateTrustRoot(store, FakeKeyStore(), FixedClock(), FakeAudit()).execute(
            rotate_command(overlap_until=NOW + timedelta(days=60))
        )
    assert error.value.reason_code == "trust_scope_mismatch"


def test_rotate_trust_root_requires_new_material() -> None:
    store = MemoryStore()
    store.put_trust_root(root())
    with pytest.raises(Conflict, match="differ"):
        RotateTrustRoot(store, FakeKeyStore(), FixedClock(), FakeAudit()).execute(
            rotate_command(successor_public_material_ref="public:root-1")
        )


def test_rotate_trust_root_discards_untrusted_staged_material() -> None:
    store, keys = MemoryStore(), FakeKeyStore()
    store.put_trust_root(root())
    keys.root_result = ProofVerification("untrusted", "ed25519", "signature_invalid")
    with pytest.raises(Conflict) as error:
        RotateTrustRoot(store, keys, FixedClock(), FakeAudit()).execute(rotate_command())
    assert error.value.reason_code == "signature_invalid"
    assert len(keys.discarded) == 1
    assert store.roots["root-1"].status == "active"


def test_rotate_trust_root_rejects_conflicting_active_root() -> None:
    store = MemoryStore()
    store.put_trust_root(root())
    store.put_trust_root(root("root-conflict"))
    with pytest.raises(Conflict) as error:
        RotateTrustRoot(store, FakeKeyStore(), FixedClock(), FakeAudit()).execute(rotate_command())
    assert error.value.reason_code == "trust_scope_conflict"


def test_rotate_trust_root_fails_before_staging_without_audit() -> None:
    store, keys = MemoryStore(), FakeKeyStore()
    store.put_trust_root(root())
    with pytest.raises(RuntimeError, match="audit unavailable"):
        RotateTrustRoot(store, keys, FixedClock(), FakeAudit(available=False)).execute(rotate_command())
    assert keys.staged == []


def test_rotate_trust_root_is_idempotent() -> None:
    store, keys = MemoryStore(), FakeKeyStore()
    store.put_trust_root(root())
    service = RotateTrustRoot(store, keys, FixedClock(), FakeAudit())
    first = service.execute(rotate_command())
    second = service.execute(rotate_command())
    assert second == first
    assert len(keys.staged) == 1
