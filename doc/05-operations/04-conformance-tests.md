# Conformance Tests

## 1. Conformance levels

- **Foundation**: founding invariants and contract validation;
- **Endpoint**: local/offline/session/runtime requirements;
- **Hub**: tenant, network, database, and synchronization requirements;
- **Build**: reproducibility and artifact-generation requirements;
- **High assurance**: measured boot, split custody, and enhanced audit requirements.

## 2. Required test groups

### Host and boot

- signed image verification;
- immutable drift detection;
- failed-boot rollback;
- recovery target access;
- storage unlock and corruption behavior.

### Privilege

- arbitrary command rejection;
- operation-schema validation;
- policy binding and replay protection;
- least-privilege sandbox verification;
- break-glass expiry.

### Policy

- deterministic test vectors;
- unknown fact handling;
- separation of duties;
- bundle signature and compatibility;
- atomic activation and rollback;
- reason-code stability.

### Kristal

- signature/hash failure;
- channel trust isolation;
- downgrade/substitution rejection;
- query-contract compatibility;
- atomic activation;
- offline serving;
- cache pinning and last-known-good retention;
- revocation handling.

### Product boundaries

- no Konnaxion direct Orgo database access;
- Publication Gateway classification/redaction;
- tenant separation;
- public/private network isolation;
- integration removal without core failure.

### Privacy and rights

- role-based disclosure;
- protected audit access logging;
- no-AI data isolation;
- cultural withdrawal and cache purge;
- audience-scoped pack enforcement.

### Lifecycle

- OS/service/policy/artifact independent activation;
- Release Set compatibility;
- migration interruption and resume;
- offline bundle parser limits;
- rollback and forward repair.

### Exit

- full export;
- clean restore;
- independent verification;
- resumed workflows;
- operator independence.

## 3. Evidence

Test output records release identities, environment, node profile, test vector version, result, logs/receipts, and exceptions. A manual assertion without evidence is not a conformance result.
