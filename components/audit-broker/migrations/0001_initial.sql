-- Audit Broker initial schema.
-- This migration owns only Audit Broker state. All JSON values are canonical UTF-8
-- JSON text so the same logical schema can be used by SQLite and PostgreSQL.

CREATE TABLE IF NOT EXISTS audit_schema_migrations (
    version TEXT PRIMARY KEY,
    applied_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS audit_records (
    audit_record_id TEXT PRIMARY KEY,
    event_class_id TEXT NOT NULL,
    producer_component_id TEXT NOT NULL,
    producer_identity_json TEXT NOT NULL,
    occurred_at TEXT NOT NULL,
    received_at TEXT NOT NULL,
    subject_references_json TEXT NOT NULL,
    action_or_transition TEXT NOT NULL,
    outcome TEXT NOT NULL,
    purpose TEXT NOT NULL,
    classification TEXT NOT NULL,
    retention_class TEXT NOT NULL,
    correlation_id TEXT NOT NULL,
    source_refs_json TEXT NOT NULL,
    bounded_payload_json TEXT NOT NULL,
    policy_or_contract_ref TEXT NOT NULL,
    record_state TEXT NOT NULL CHECK (record_state IN (
        'received', 'validated', 'accepted', 'quarantined', 'retained',
        'held', 'archived', 'expired', 'disposed', 'invalidated'
    )),
    integrity_algorithm TEXT NOT NULL CHECK (integrity_algorithm IN ('sha256')),
    integrity_digest TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_audit_records_event_class
    ON audit_records (event_class_id, occurred_at);
CREATE INDEX IF NOT EXISTS idx_audit_records_producer
    ON audit_records (producer_component_id, occurred_at);
CREATE INDEX IF NOT EXISTS idx_audit_records_correlation
    ON audit_records (correlation_id);
CREATE INDEX IF NOT EXISTS idx_audit_records_state
    ON audit_records (record_state, occurred_at);

CREATE TABLE IF NOT EXISTS audit_idempotency_keys (
    producer_component_id TEXT NOT NULL,
    idempotency_key TEXT NOT NULL,
    request_digest TEXT NOT NULL,
    audit_record_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    PRIMARY KEY (producer_component_id, idempotency_key),
    FOREIGN KEY (audit_record_id) REFERENCES audit_records(audit_record_id)
);

CREATE TABLE IF NOT EXISTS audit_chain_of_custody (
    custody_entry_id TEXT PRIMARY KEY,
    chain_id TEXT NOT NULL,
    subject_ref TEXT NOT NULL,
    transition_type TEXT NOT NULL,
    actor_identity_json TEXT NOT NULL,
    occurred_at TEXT NOT NULL,
    result TEXT NOT NULL,
    receipt_ref TEXT NOT NULL,
    details_json TEXT NOT NULL,
    previous_entry_digest TEXT,
    entry_digest TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_audit_custody_chain_digest
    ON audit_chain_of_custody (chain_id, entry_digest);
CREATE INDEX IF NOT EXISTS idx_audit_custody_subject
    ON audit_chain_of_custody (subject_ref, occurred_at);

CREATE TABLE IF NOT EXISTS audit_retention_state (
    record_ref TEXT PRIMARY KEY,
    retention_class TEXT NOT NULL,
    state TEXT NOT NULL CHECK (state IN (
        'active', 'held', 'archived', 'expired',
        'disposition_pending', 'disposed', 'invalidated'
    )),
    effective_at TEXT NOT NULL,
    policy_or_hold_ref TEXT NOT NULL,
    next_review_or_disposition_at TEXT,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (record_ref) REFERENCES audit_records(audit_record_id)
);

CREATE TABLE IF NOT EXISTS audit_access_receipts (
    receipt_id TEXT PRIMARY KEY,
    request_id TEXT NOT NULL,
    requester_identity_json TEXT NOT NULL,
    purpose TEXT NOT NULL,
    policy_decision_ref TEXT NOT NULL,
    requested_scope_json TEXT NOT NULL,
    effective_scope_json TEXT NOT NULL,
    outcome TEXT NOT NULL CHECK (outcome IN (
        'allowed', 'partially_allowed', 'denied', 'cancelled',
        'expired', 'failed'
    )),
    occurred_at TEXT NOT NULL,
    receipt_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_audit_access_request
    ON audit_access_receipts (request_id, occurred_at);

CREATE TABLE IF NOT EXISTS audit_disclosure_packages (
    package_id TEXT PRIMARY KEY,
    request_id TEXT NOT NULL,
    purpose TEXT NOT NULL,
    scope_json TEXT NOT NULL,
    record_refs_json TEXT NOT NULL,
    redaction_profile TEXT NOT NULL,
    generated_at TEXT NOT NULL,
    expiry_or_validity TEXT NOT NULL,
    chain_of_custody_ref TEXT NOT NULL,
    delivery_state TEXT NOT NULL CHECK (delivery_state IN (
        'local', 'undelivered', 'delivery_failed', 'delivered', 'expired'
    )),
    package_json TEXT NOT NULL,
    integrity_digest TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_audit_disclosure_request
    ON audit_disclosure_packages (request_id, generated_at);

CREATE TABLE IF NOT EXISTS audit_invalidations (
    invalidation_id TEXT PRIMARY KEY,
    record_ref TEXT NOT NULL,
    source_correction_or_retraction_ref TEXT NOT NULL,
    reason TEXT NOT NULL,
    effective_at TEXT NOT NULL,
    actor_identity_json TEXT NOT NULL,
    receipt_ref TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (record_ref) REFERENCES audit_records(audit_record_id)
);

CREATE INDEX IF NOT EXISTS idx_audit_invalidations_record
    ON audit_invalidations (record_ref, effective_at);
