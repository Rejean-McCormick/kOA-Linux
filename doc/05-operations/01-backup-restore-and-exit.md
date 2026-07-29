# Backup, Restore, and Exit

## 1. Backup scope

Backups cover declared product state, governance policy, trust references, Kristal artifacts or references, audit classes, rights/consent records, and restore metadata. Immutable artifacts may be referenced if independent availability is guaranteed; otherwise they are included.

## 2. Backup properties

Backups MUST be:

- encrypted;
- tenant-scoped;
- integrity-protected;
- versioned;
- retention-governed;
- tested by restore;
- independent from the active node where possible.

## 3. Restore

Restore occurs on a clean compatible environment and verifies:

- bundle identity and signature;
- tenant and audience;
- encryption keys;
- schema versions and migrations;
- trust-root continuity;
- artifact inventory;
- policy compatibility;
- post-restore health.

## 4. Sovereignty Bundle

A complete exit export SHOULD contain:

```text
manifest and signature
identity and delegation data
Governance Policy Bundles
Konnaxion export
Orgo export
Kristal artifacts and references
rights and consent records
audit receipts by authorized class
trust-root handover material
restore instructions and tests
```

Private signing keys are included only under a specific protected handover profile; otherwise new keys are enrolled.

## 5. Exit test

A credible exit test:

1. exports a tenant;
2. provisions a clean compatible node from public/documented materials;
3. imports the bundle;
4. verifies hashes and policy;
5. rebuilds indexes;
6. resumes authorized workflows;
7. proves the original operator is no longer required.

## 6. Objectives

Deployments MUST define RPO and RTO by data class and node profile. Recovery of public cache is less critical than identity, protected evidence, policy, and active operational work.
