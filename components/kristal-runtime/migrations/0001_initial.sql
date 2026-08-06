-- Kristal Runtime owned state, migration 0001.
-- SQLite 3.35+; the enclosing transaction prevents partial activation of the schema.
PRAGMA foreign_keys = ON;
BEGIN IMMEDIATE;

CREATE TABLE IF NOT EXISTS schema_migrations (
    version INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    applied_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS artifacts (
    artifact_ref TEXT PRIMARY KEY,
    artifact_class TEXT NOT NULL CHECK (artifact_class IN ('runtime_pack', 'kristal_artifact')),
    artifact_identity TEXT NOT NULL,
    artifact_version TEXT NOT NULL,
    artifact_digest TEXT NOT NULL,
    document_digest TEXT NOT NULL CHECK (document_digest GLOB 'sha256:[0-9a-f]*'),
    storage_key TEXT NOT NULL UNIQUE,
    byte_length INTEGER NOT NULL CHECK (byte_length >= 0),
    disposition TEXT NOT NULL CHECK (
        disposition IN ('staged', 'quarantined', 'verified', 'rejected', 'revoked', 'superseded')
    ),
    verification_id TEXT,
    registered_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (artifact_class, artifact_identity, artifact_version, artifact_digest)
);

CREATE TABLE IF NOT EXISTS verification_records (
    verification_id TEXT PRIMARY KEY,
    request_id TEXT NOT NULL UNIQUE,
    correlation_id TEXT NOT NULL,
    artifact_ref TEXT NOT NULL REFERENCES artifacts(artifact_ref),
    outcome TEXT NOT NULL CHECK (outcome IN ('verified', 'blocked', 'rejected', 'failed')),
    activation_eligible INTEGER NOT NULL CHECK (activation_eligible IN (0, 1)),
    checks_json TEXT NOT NULL,
    reason_codes_json TEXT NOT NULL,
    identity_receipt_ref TEXT,
    policy_receipt_ref TEXT,
    receipt_ref TEXT NOT NULL,
    recorded_at TEXT NOT NULL,
    canonical_digest TEXT NOT NULL CHECK (canonical_digest GLOB 'sha256:[0-9a-f]*'),
    CHECK (outcome = 'verified' OR activation_eligible = 0)
);

CREATE INDEX IF NOT EXISTS verification_records_artifact_idx
    ON verification_records(artifact_ref, recorded_at);
CREATE INDEX IF NOT EXISTS verification_records_correlation_idx
    ON verification_records(correlation_id, recorded_at);

CREATE TABLE IF NOT EXISTS activation_records (
    transition_id TEXT PRIMARY KEY,
    request_id TEXT NOT NULL UNIQUE,
    correlation_id TEXT NOT NULL,
    operation TEXT NOT NULL CHECK (operation IN ('activate', 'rollback')),
    outcome TEXT NOT NULL CHECK (outcome IN ('activated', 'rolled_back', 'blocked', 'failed')),
    candidate_artifact_ref TEXT REFERENCES artifacts(artifact_ref),
    previous_artifact_ref TEXT REFERENCES artifacts(artifact_ref),
    resulting_artifact_ref TEXT REFERENCES artifacts(artifact_ref),
    verification_id TEXT REFERENCES verification_records(verification_id),
    authorization_ref TEXT,
    resource_grant_ref TEXT,
    receipt_ref TEXT NOT NULL,
    reason_codes_json TEXT NOT NULL,
    occurred_at TEXT NOT NULL,
    canonical_digest TEXT NOT NULL CHECK (canonical_digest GLOB 'sha256:[0-9a-f]*'),
    CHECK (
        (outcome IN ('activated', 'rolled_back') AND resulting_artifact_ref IS NOT NULL)
        OR (outcome IN ('blocked', 'failed') AND resulting_artifact_ref = previous_artifact_ref)
    )
);

CREATE INDEX IF NOT EXISTS activation_records_correlation_idx
    ON activation_records(correlation_id, occurred_at);
CREATE INDEX IF NOT EXISTS activation_records_candidate_idx
    ON activation_records(candidate_artifact_ref, occurred_at);

CREATE TABLE IF NOT EXISTS runtime_state (
    singleton_id INTEGER PRIMARY KEY CHECK (singleton_id = 1),
    active_artifact_ref TEXT REFERENCES artifacts(artifact_ref),
    previous_artifact_ref TEXT REFERENCES artifacts(artifact_ref),
    revision INTEGER NOT NULL CHECK (revision >= 0),
    last_transition_id TEXT REFERENCES activation_records(transition_id),
    updated_at TEXT
);

INSERT OR IGNORE INTO runtime_state(singleton_id, revision) VALUES (1, 0);
INSERT OR IGNORE INTO schema_migrations(version, name, applied_at)
VALUES (1, '0001_initial', strftime('%Y-%m-%dT%H:%M:%fZ', 'now'));

COMMIT;
