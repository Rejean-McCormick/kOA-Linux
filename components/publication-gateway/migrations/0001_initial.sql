PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

BEGIN IMMEDIATE;

CREATE TABLE IF NOT EXISTS schema_metadata (
    schema_name TEXT PRIMARY KEY,
    schema_version INTEGER NOT NULL CHECK (schema_version >= 1),
    applied_at TEXT NOT NULL
);

INSERT INTO schema_metadata(schema_name, schema_version, applied_at)
VALUES ('publication_gateway', 1, strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
ON CONFLICT(schema_name) DO UPDATE SET
    schema_version = excluded.schema_version,
    applied_at = excluded.applied_at
WHERE schema_metadata.schema_version < excluded.schema_version;

CREATE TABLE IF NOT EXISTS publication_requests (
    request_id TEXT PRIMARY KEY,
    idempotency_key TEXT NOT NULL UNIQUE,
    request_digest TEXT NOT NULL,
    source_component_ref TEXT NOT NULL,
    source_object_ref TEXT NOT NULL,
    source_version_ref TEXT NOT NULL,
    destination_ref TEXT NOT NULL,
    correlation_id TEXT NOT NULL,
    state TEXT NOT NULL CHECK (state IN (
        'received','validating','awaiting_authority','awaiting_review','denied','blocked',
        'approved','staging','ready','publishing','published','partially_delivered',
        'failed','cancelled','revoked','remediating','closed'
    )),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS publication_decisions (
    decision_ref TEXT PRIMARY KEY,
    request_id TEXT NOT NULL REFERENCES publication_requests(request_id) ON DELETE RESTRICT,
    decision TEXT NOT NULL CHECK (decision IN ('allow','deny','blocked','review_required')),
    policy_set_ref TEXT NOT NULL,
    obligations_json TEXT NOT NULL,
    reason_codes_json TEXT NOT NULL,
    receipt_ref TEXT NOT NULL,
    decided_at TEXT NOT NULL,
    UNIQUE(request_id, decision_ref)
);

CREATE TABLE IF NOT EXISTS publication_attempts (
    attempt_id TEXT PRIMARY KEY,
    request_id TEXT NOT NULL REFERENCES publication_requests(request_id) ON DELETE RESTRICT,
    destination_ref TEXT NOT NULL,
    idempotency_key TEXT NOT NULL,
    package_id TEXT,
    outcome TEXT NOT NULL CHECK (outcome IN (
        'queued','published','partially_published','failed','cancelled','rejected',
        'unknown_reconciliation_required'
    )),
    delivered_units_json TEXT NOT NULL,
    undelivered_units_json TEXT NOT NULL,
    automatic_retry_allowed INTEGER NOT NULL DEFAULT 0 CHECK (automatic_retry_allowed IN (0,1)),
    destination_state_ref TEXT,
    evidence_refs_json TEXT NOT NULL,
    occurred_at TEXT NOT NULL,
    UNIQUE(request_id, attempt_id),
    CHECK (
        outcome NOT IN ('partially_published','unknown_reconciliation_required')
        OR automatic_retry_allowed = 0
    )
);

CREATE TABLE IF NOT EXISTS publication_receipts (
    receipt_id TEXT PRIMARY KEY,
    request_id TEXT NOT NULL REFERENCES publication_requests(request_id) ON DELETE RESTRICT,
    idempotency_key TEXT NOT NULL UNIQUE,
    receipt_digest TEXT NOT NULL,
    receipt_json TEXT NOT NULL,
    record_status TEXT NOT NULL CHECK (record_status IN ('issued','superseded')),
    issued_at TEXT NOT NULL,
    recorded_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS publication_state_changes (
    change_id TEXT PRIMARY KEY,
    receipt_id TEXT NOT NULL REFERENCES publication_receipts(receipt_id) ON DELETE RESTRICT,
    change_class TEXT NOT NULL CHECK (change_class IN (
        'consent_revocation','authority_revocation','withdrawal','expiry','correction',
        'downstream_remediation','external_limitation'
    )),
    change_json TEXT NOT NULL,
    affected_future_operations_stopped INTEGER NOT NULL CHECK (affected_future_operations_stopped = 1),
    historical_receipt_preserved INTEGER NOT NULL CHECK (historical_receipt_preserved = 1),
    recorded_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_publication_requests_state
    ON publication_requests(state, updated_at);
CREATE INDEX IF NOT EXISTS idx_publication_requests_source
    ON publication_requests(source_object_ref, source_version_ref);
CREATE INDEX IF NOT EXISTS idx_publication_attempts_request
    ON publication_attempts(request_id, occurred_at);
CREATE INDEX IF NOT EXISTS idx_publication_changes_receipt
    ON publication_state_changes(receipt_id, recorded_at);

COMMIT;
