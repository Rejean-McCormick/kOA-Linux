PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS schema_migrations (
    version TEXT PRIMARY KEY,
    applied_at TEXT NOT NULL
) STRICT;

CREATE TABLE IF NOT EXISTS identities (
    identity_id TEXT PRIMARY KEY,
    subject_type TEXT NOT NULL CHECK (subject_type IN (
        'human', 'service', 'component_instance', 'node', 'device',
        'workspace', 'tenant', 'organization', 'external_integration',
        'artifact_signer', 'recovery_operator'
    )),
    display_name TEXT NOT NULL,
    owner_ref TEXT,
    tenant_ref TEXT,
    environment TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN (
        'pending', 'active', 'suspended', 'revoked', 'expired', 'retired'
    )),
    created_at TEXT NOT NULL,
    activated_at TEXT,
    expires_at TEXT,
    revoked_at TEXT,
    retired_at TEXT,
    credential_refs_json TEXT NOT NULL DEFAULT '[]' CHECK (json_valid(credential_refs_json)),
    evidence_refs_json TEXT NOT NULL DEFAULT '[]' CHECK (json_valid(evidence_refs_json)),
    public_attributes_json TEXT NOT NULL DEFAULT '{}' CHECK (json_valid(public_attributes_json)),
    revision INTEGER NOT NULL DEFAULT 0 CHECK (revision >= 0),
    CHECK (status <> 'active' OR activated_at IS NOT NULL),
    CHECK (status <> 'revoked' OR revoked_at IS NOT NULL),
    CHECK (status <> 'retired' OR retired_at IS NOT NULL)
) STRICT;

CREATE TABLE IF NOT EXISTS credentials (
    credential_id TEXT PRIMARY KEY,
    subject_identity_id TEXT NOT NULL REFERENCES identities(identity_id) ON UPDATE RESTRICT ON DELETE RESTRICT,
    credential_type TEXT NOT NULL CHECK (credential_type IN (
        'password_verifier', 'public_key', 'x509_certificate', 'ssh_certificate',
        'service_token', 'device_credential', 'recovery_code', 'attestation_credential'
    )),
    issuer_ref TEXT NOT NULL,
    scope_json TEXT NOT NULL CHECK (json_valid(scope_json)),
    issued_at TEXT NOT NULL,
    not_before TEXT NOT NULL,
    expires_at TEXT,
    status TEXT NOT NULL CHECK (status IN (
        'pending', 'active', 'suspended', 'revoked', 'expired', 'retired'
    )),
    key_or_material_reference TEXT NOT NULL,
    revocation_reference TEXT NOT NULL,
    evidence_refs_json TEXT NOT NULL DEFAULT '[]' CHECK (json_valid(evidence_refs_json)),
    revision INTEGER NOT NULL DEFAULT 0 CHECK (revision >= 0),
    CHECK (expires_at IS NULL OR expires_at > not_before)
) STRICT;

CREATE TABLE IF NOT EXISTS trust_roots (
    trust_root_id TEXT PRIMARY KEY,
    root_type TEXT NOT NULL,
    public_material_ref TEXT NOT NULL,
    scope_json TEXT NOT NULL CHECK (json_valid(scope_json)),
    scope_fingerprint TEXT NOT NULL,
    owner_ref TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN (
        'staged', 'active', 'suspended', 'revoked', 'superseded', 'retired'
    )),
    activated_at TEXT,
    expires_at TEXT,
    revoked_at TEXT,
    supersedes_ref TEXT REFERENCES trust_roots(trust_root_id) ON UPDATE RESTRICT ON DELETE RESTRICT,
    evidence_refs_json TEXT NOT NULL DEFAULT '[]' CHECK (json_valid(evidence_refs_json)),
    revision INTEGER NOT NULL DEFAULT 0 CHECK (revision >= 0),
    UNIQUE (scope_fingerprint, trust_root_id),
    CHECK (status <> 'active' OR activated_at IS NOT NULL),
    CHECK (status <> 'revoked' OR revoked_at IS NOT NULL)
) STRICT;

CREATE TABLE IF NOT EXISTS revocations (
    revocation_id TEXT PRIMARY KEY,
    target_ref TEXT NOT NULL,
    target_type TEXT NOT NULL CHECK (target_type IN (
        'identity', 'credential', 'certificate', 'key', 'trust_root',
        'issuer', 'node', 'service', 'artifact_signer'
    )),
    scope_json TEXT NOT NULL CHECK (json_valid(scope_json)),
    reason_code TEXT NOT NULL,
    authority_ref TEXT NOT NULL,
    effective_at TEXT NOT NULL,
    recorded_at TEXT NOT NULL,
    evidence_refs_json TEXT NOT NULL DEFAULT '[]' CHECK (json_valid(evidence_refs_json)),
    UNIQUE (target_ref, target_type, effective_at)
) STRICT;

CREATE TABLE IF NOT EXISTS verification_results (
    verification_id TEXT PRIMARY KEY,
    result TEXT NOT NULL CHECK (result IN ('trusted', 'untrusted', 'indeterminate')),
    resolved_identity_ref TEXT,
    resolved_trust_root_ref TEXT,
    validated_scope_json TEXT NOT NULL CHECK (json_valid(validated_scope_json)),
    algorithm TEXT,
    credential_or_artifact_ref TEXT NOT NULL,
    verified_at TEXT NOT NULL,
    reason_code TEXT NOT NULL,
    evidence_refs_json TEXT NOT NULL DEFAULT '[]' CHECK (json_valid(evidence_refs_json))
) STRICT;

CREATE TABLE IF NOT EXISTS trust_update_state (
    scope_fingerprint TEXT PRIMARY KEY,
    active_sequence INTEGER NOT NULL CHECK (active_sequence >= 0),
    package_ref TEXT NOT NULL,
    applied_at TEXT NOT NULL,
    receipt_ref TEXT NOT NULL
) STRICT;

CREATE INDEX IF NOT EXISTS idx_identities_subject_status
    ON identities(subject_type, status);
CREATE INDEX IF NOT EXISTS idx_identities_tenant_environment
    ON identities(tenant_ref, environment);
CREATE INDEX IF NOT EXISTS idx_credentials_subject_status
    ON credentials(subject_identity_id, status);
CREATE INDEX IF NOT EXISTS idx_credentials_expiry
    ON credentials(expires_at) WHERE expires_at IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_trust_roots_scope_status
    ON trust_roots(scope_fingerprint, status);
CREATE INDEX IF NOT EXISTS idx_revocations_target
    ON revocations(target_ref, target_type, effective_at);
CREATE INDEX IF NOT EXISTS idx_verification_results_object_time
    ON verification_results(credential_or_artifact_ref, verified_at);

INSERT OR IGNORE INTO schema_migrations(version, applied_at)
VALUES ('0001_initial', strftime('%Y-%m-%dT%H:%M:%fZ', 'now'));
