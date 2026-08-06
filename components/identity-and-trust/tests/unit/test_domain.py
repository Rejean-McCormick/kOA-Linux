from __future__ import annotations

from dataclasses import FrozenInstanceError, fields
from datetime import datetime, timedelta, timezone

import pytest

from koa_identity_and_trust.domain import (
    Credential,
    CredentialStatus,
    CredentialType,
    Identity,
    IdentityResult,
    IdentityStatus,
    RoleBinding,
    RoleBindingScope,
    SessionContext,
    SubjectType,
    TrustResult,
    TrustRoot,
    TrustRootStatus,
    TrustScope,
)


UTC = timezone.utc
NOW = datetime(2026, 8, 6, 12, 0, tzinfo=UTC)


def make_identity(**overrides: object) -> Identity:
    values: dict[str, object] = {
        "identity_id": "identity:user:alice",
        "subject_type": SubjectType.HUMAN,
        "display_name": "Alice",
        "owner_ref": "owner:people",
        "tenant_ref": "tenant:alpha",
        "environment": "production",
        "status": IdentityStatus.ACTIVE,
        "created_at": NOW - timedelta(days=30),
        "activated_at": NOW - timedelta(days=29),
        "expires_at": NOW + timedelta(days=30),
        "credential_refs": ("credential:2", "credential:1", "credential:1"),
        "evidence_refs": ("evidence:identity-proof",),
    }
    values.update(overrides)
    return Identity(**values)  # type: ignore[arg-type]


def make_credential(**overrides: object) -> Credential:
    values: dict[str, object] = {
        "credential_id": "credential:service:1",
        "subject_identity_id": "identity:service:catalog",
        "credential_type": CredentialType.SERVICE_TOKEN,
        "issuer_ref": "identity:issuer:local",
        "scope": "component:catalog:read",
        "issued_at": NOW - timedelta(hours=2),
        "not_before": NOW - timedelta(hours=1),
        "expires_at": NOW + timedelta(hours=1),
        "status": CredentialStatus.ACTIVE,
        "key_or_material_reference": "protected://credentials/service/1",
        "revocation_reference": "revocation://credentials/service/1",
    }
    values.update(overrides)
    return Credential(**values)  # type: ignore[arg-type]


def make_scope(**overrides: str | None) -> TrustScope:
    values: dict[str, str | None] = {
        "tenant": "tenant:alpha",
        "environment": "production",
        "release_channel": "stable",
        "artifact_class": "runtime_pack",
        "integration": None,
        "component": "kristal_runtime",
        "purpose": "artifact_verification",
    }
    values.update(overrides)
    return TrustScope(**values)


def make_root(**overrides: object) -> TrustRoot:
    values: dict[str, object] = {
        "trust_root_id": "trust-root:runtime-pack:stable",
        "root_type": "artifact_signing",
        "public_material_ref": "public-key://roots/runtime-pack-stable",
        "scope": make_scope(),
        "owner_ref": "owner:release-security",
        "status": TrustRootStatus.ACTIVE,
        "activated_at": NOW - timedelta(days=10),
        "expires_at": NOW + timedelta(days=365),
        "evidence_refs": ("evidence:ceremony",),
    }
    values.update(overrides)
    return TrustRoot(**values)  # type: ignore[arg-type]


def test_contract_enums_are_exact() -> None:
    assert {item.value for item in SubjectType} == {
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
    assert {item.value for item in IdentityStatus} == {
        "pending",
        "active",
        "suspended",
        "revoked",
        "expired",
        "retired",
    }
    assert {item.value for item in CredentialType} == {
        "password_verifier",
        "public_key",
        "x509_certificate",
        "ssh_certificate",
        "service_token",
        "device_credential",
        "recovery_code",
        "attestation_credential",
    }
    assert {item.value for item in TrustRootStatus} == {
        "staged",
        "active",
        "suspended",
        "revoked",
        "superseded",
        "retired",
    }
    assert tuple(item.value for item in IdentityResult) == (
        "established",
        "not_established",
        "indeterminate",
    )
    assert tuple(item.value for item in TrustResult) == (
        "trusted",
        "untrusted",
        "indeterminate",
    )


def test_identity_is_immutable_canonical_and_time_bounded() -> None:
    identity = make_identity()
    assert identity.credential_refs == ("credential:1", "credential:2")
    assert identity.is_active_at(NOW)
    assert not identity.is_active_at(NOW + timedelta(days=31))
    with pytest.raises(FrozenInstanceError):
        identity.display_name = "Other"  # type: ignore[misc]


def test_display_name_does_not_define_identity_equality() -> None:
    first = make_identity(display_name="Alice")
    second = make_identity(display_name="Display name changed")
    assert first.identity_id == second.identity_id
    assert first.display_name != second.display_name


def test_identity_rejects_invalid_lifecycle_timestamps() -> None:
    with pytest.raises(ValueError, match="active identity requires activated_at"):
        make_identity(activated_at=None)
    with pytest.raises(ValueError, match="revoked identity requires revoked_at"):
        make_identity(status=IdentityStatus.REVOKED, revoked_at=None)
    with pytest.raises(ValueError, match="pending identity"):
        make_identity(status=IdentityStatus.PENDING)
    with pytest.raises(ValueError, match="timezone-aware"):
        make_identity(created_at=NOW.replace(tzinfo=None))


def test_credential_contains_references_not_secret_material() -> None:
    credential = make_credential()
    names = {field.name for field in fields(credential)}
    assert credential.is_usable_at(NOW)
    assert "private_key" not in names
    assert "secret" not in names
    assert "token" not in names
    assert credential.key_or_material_reference.startswith("protected://")


def test_credential_rejects_invalid_interval_and_inactive_use() -> None:
    with pytest.raises(ValueError, match="not_before"):
        make_credential(not_before=NOW - timedelta(hours=3))
    with pytest.raises(ValueError, match="expires_at"):
        make_credential(expires_at=NOW - timedelta(hours=1))
    revoked = make_credential(status=CredentialStatus.REVOKED)
    assert revoked.is_time_valid_at(NOW)
    assert not revoked.is_usable_at(NOW)


def test_trust_scope_forbids_global_unscoped_root() -> None:
    with pytest.raises(ValueError, match="global unscoped"):
        TrustScope()


def test_trust_scope_matching_is_exact_without_cross_environment_fallback() -> None:
    registered = make_scope()
    same = make_scope()
    development = make_scope(environment="development")
    broader = TrustScope(tenant="tenant:alpha", environment="production")
    assert registered.matches_exactly(same)
    assert not registered.matches_exactly(development)
    assert not registered.matches_exactly(broader)
    assert registered.as_pairs() == (
        ("tenant", "tenant:alpha"),
        ("environment", "production"),
        ("release_channel", "stable"),
        ("artifact_class", "runtime_pack"),
        ("component", "kristal_runtime"),
        ("purpose", "artifact_verification"),
    )


def test_trust_root_requires_active_state_and_exact_scope() -> None:
    root = make_root()
    assert root.accepts_scope_at(make_scope(), NOW)
    assert not root.accepts_scope_at(make_scope(environment="development"), NOW)
    suspended = make_root(status=TrustRootStatus.SUSPENDED)
    assert not suspended.accepts_scope_at(make_scope(), NOW)


def test_trust_root_rejects_invalid_state_and_self_supersession() -> None:
    with pytest.raises(ValueError, match="active trust root requires activated_at"):
        make_root(activated_at=None)
    with pytest.raises(ValueError, match="revoked trust root requires revoked_at"):
        make_root(status=TrustRootStatus.REVOKED, revoked_at=None)
    with pytest.raises(ValueError, match="cannot supersede itself"):
        make_root(supersedes_ref="trust-root:runtime-pack:stable")
    with pytest.raises(ValueError, match="staged trust root"):
        make_root(status=TrustRootStatus.STAGED)


def test_role_binding_is_exact_evidence_not_authorization() -> None:
    scope = RoleBindingScope(
        tenant_ref="tenant:alpha",
        environment="production",
        component="publication_gateway",
        purpose="publication_review",
    )
    binding = RoleBinding(
        binding_id="role-binding:1",
        identity_id="identity:user:alice",
        role="reviewer",
        scope=scope,
        issuer_ref="identity:issuer:local",
        issued_at=NOW - timedelta(hours=2),
        not_before=NOW - timedelta(hours=1),
        expires_at=NOW + timedelta(hours=1),
        evidence_refs=("evidence:role-assignment",),
    )
    assert binding.is_effective_at(NOW)
    assert binding.matches_scope(scope)
    assert not binding.matches_scope(
        RoleBindingScope(
            tenant_ref="tenant:alpha",
            environment="development",
            component="publication_gateway",
            purpose="publication_review",
        )
    )
    assert not hasattr(binding, "authorizes")


def test_role_binding_rejects_unbounded_or_invalid_lifetime() -> None:
    with pytest.raises(ValueError, match="component"):
        RoleBindingScope(
            tenant_ref="tenant:alpha",
            environment="production",
            component="",
            purpose="review",
        )
    scope = RoleBindingScope("tenant:alpha", "production", "component", "purpose")
    with pytest.raises(ValueError, match="expires_at"):
        RoleBinding(
            binding_id="binding:1",
            identity_id="identity:1",
            role="role:1",
            scope=scope,
            issuer_ref="issuer:1",
            issued_at=NOW,
            not_before=NOW,
            expires_at=NOW,
        )


def test_session_context_is_exact_time_bounded_identity_evidence() -> None:
    session = SessionContext(
        session_id="session:1",
        identity_id="identity:user:alice",
        subject_type=SubjectType.HUMAN,
        tenant_ref="tenant:alpha",
        environment="production",
        profile_ref="profile:user-lightweight",
        authentication_context="interactive_user",
        assurance_factors=("possession", "knowledge", "knowledge"),
        issued_at=NOW - timedelta(minutes=5),
        expires_at=NOW + timedelta(minutes=55),
        credential_refs=("credential:user:alice",),
        evidence_refs=("evidence:authentication",),
    )
    assert session.assurance_factors == ("knowledge", "possession")
    assert session.is_valid_at(NOW)
    assert session.matches_context(
        tenant_ref="tenant:alpha",
        environment="production",
        profile_ref="profile:user-lightweight",
        authentication_context="interactive_user",
    )
    assert not session.matches_context(
        tenant_ref="tenant:alpha",
        environment="development",
        profile_ref="profile:user-lightweight",
        authentication_context="interactive_user",
    )
    assert not hasattr(session, "authorizes")


def test_session_context_rejects_missing_assurance_and_invalid_lifetime() -> None:
    common = {
        "session_id": "session:1",
        "identity_id": "identity:user:alice",
        "subject_type": SubjectType.HUMAN,
        "tenant_ref": "tenant:alpha",
        "environment": "production",
        "profile_ref": "profile:user-lightweight",
        "authentication_context": "interactive_user",
        "issued_at": NOW,
        "expires_at": NOW + timedelta(hours=1),
    }
    with pytest.raises(ValueError, match="at least one"):
        SessionContext(**common, assurance_factors=())
    with pytest.raises(ValueError, match="expires_at"):
        SessionContext(**{**common, "expires_at": NOW}, assurance_factors=("knowledge",))
