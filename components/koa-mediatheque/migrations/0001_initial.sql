PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS schema_migrations (
    version TEXT PRIMARY KEY,
    applied_at TEXT NOT NULL
) STRICT;

CREATE TABLE IF NOT EXISTS media_records (
    record_id TEXT PRIMARY KEY,
    current_version_id TEXT NOT NULL,
    title TEXT NOT NULL,
    media_type TEXT NOT NULL,
    record_state TEXT NOT NULL CHECK (
        record_state IN ('draft', 'active', 'restricted', 'withdrawn', 'archived', 'deleted_tombstone')
    ),
    authority_domain_id TEXT NOT NULL,
    record_json TEXT NOT NULL CHECK (json_valid(record_json)),
    revision INTEGER NOT NULL DEFAULT 1 CHECK (revision >= 1),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
) STRICT;

CREATE TABLE IF NOT EXISTS media_versions (
    version_id TEXT PRIMARY KEY,
    record_id TEXT NOT NULL REFERENCES media_records(record_id) ON DELETE RESTRICT,
    digest_algorithm TEXT NOT NULL CHECK (digest_algorithm IN ('sha256', 'sha384', 'sha512')),
    digest TEXT NOT NULL,
    storage_ref TEXT NOT NULL,
    size_bytes INTEGER NOT NULL CHECK (size_bytes >= 0),
    availability TEXT NOT NULL CHECK (
        availability IN ('managed_local', 'managed_remote_cache', 'external_reference', 'offline_unavailable', 'withdrawn')
    ),
    version_state TEXT NOT NULL CHECK (
        version_state IN ('staged', 'quarantined', 'verified', 'accepted', 'superseded', 'withdrawn', 'corrupt')
    ),
    version_json TEXT NOT NULL CHECK (json_valid(version_json)),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (record_id, version_id)
) STRICT;

CREATE INDEX IF NOT EXISTS idx_media_versions_record
    ON media_versions(record_id, created_at, version_id);
CREATE INDEX IF NOT EXISTS idx_media_versions_digest
    ON media_versions(digest_algorithm, digest);
CREATE INDEX IF NOT EXISTS idx_media_records_state
    ON media_records(record_state, updated_at, record_id);

CREATE TABLE IF NOT EXISTS publication_receipts (
    receipt_id TEXT PRIMARY KEY,
    request_id TEXT NOT NULL,
    record_id TEXT NOT NULL REFERENCES media_records(record_id) ON DELETE RESTRICT,
    version_id TEXT NOT NULL REFERENCES media_versions(version_id) ON DELETE RESTRICT,
    target_system TEXT NOT NULL,
    outcome TEXT NOT NULL CHECK (
        outcome IN ('queued', 'published', 'partially_published', 'failed', 'withdrawal_notice_sent')
    ),
    receipt_json TEXT NOT NULL CHECK (json_valid(receipt_json)),
    attached_at TEXT NOT NULL,
    UNIQUE (request_id, record_id, version_id)
) STRICT;

CREATE INDEX IF NOT EXISTS idx_publication_receipts_record
    ON publication_receipts(record_id, version_id, attached_at, receipt_id);

CREATE TRIGGER IF NOT EXISTS publication_receipts_no_update
BEFORE UPDATE ON publication_receipts
BEGIN
    SELECT RAISE(ABORT, 'publication receipts are immutable');
END;

CREATE TRIGGER IF NOT EXISTS publication_receipts_no_delete
BEFORE DELETE ON publication_receipts
BEGIN
    SELECT RAISE(ABORT, 'publication receipts are immutable');
END;

CREATE TABLE IF NOT EXISTS local_jobs (
    job_id TEXT PRIMARY KEY,
    queue_id TEXT NOT NULL,
    job_kind TEXT NOT NULL,
    subject_ref TEXT NOT NULL,
    payload_json TEXT NOT NULL CHECK (json_valid(payload_json)),
    payload_digest TEXT NOT NULL,
    state TEXT NOT NULL CHECK (
        state IN ('queued', 'leased', 'succeeded', 'failed', 'dead_letter', 'cancelled')
    ),
    priority INTEGER NOT NULL DEFAULT 100,
    attempt_count INTEGER NOT NULL DEFAULT 0 CHECK (attempt_count >= 0),
    max_attempts INTEGER NOT NULL CHECK (max_attempts >= 1),
    available_at TEXT NOT NULL,
    lease_owner TEXT,
    leased_until TEXT,
    idempotency_key TEXT NOT NULL,
    result_json TEXT CHECK (result_json IS NULL OR json_valid(result_json)),
    last_error_code TEXT,
    last_error_summary TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (queue_id, idempotency_key)
) STRICT;

CREATE INDEX IF NOT EXISTS idx_local_jobs_claim
    ON local_jobs(queue_id, state, available_at, priority, created_at, job_id);
CREATE INDEX IF NOT EXISTS idx_local_jobs_lease
    ON local_jobs(state, leased_until);

INSERT OR IGNORE INTO schema_migrations(version, applied_at)
VALUES ('0001_initial', strftime('%Y-%m-%dT%H:%M:%fZ', 'now'));
