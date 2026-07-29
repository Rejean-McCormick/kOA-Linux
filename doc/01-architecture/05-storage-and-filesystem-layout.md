# Storage and Filesystem Layout

## 1. Design goals

Storage must support immutable releases, tenant isolation, offline operation, atomic activation, rollback, encrypted sensitive state, export, and forensic reconstruction.

## 2. Recommended layout

```text
/usr/                         immutable OS content
/etc/koa/                     host configuration and pinned policy
/run/koa/                     ephemeral sockets, locks, and runtime state
/var/lib/koa/
├── node/                     node identity and local state
├── releases/                 Release Sets and activation records
├── policies/                 installed Governance Policy Bundles
├── kristal/
│   └── <tenant>/<env>/<channel>/
│       ├── packs/<runtime_pack_id>/
│       ├── active -> packs/<runtime_pack_id>
│       └── state.json
├── konnaxion/<tenant>/       Konnaxion state
├── orgo/<tenant>/            Orgo state
├── publication/<tenant>/     staged and published disclosure bundles
├── audit/                    class-separated receipts and evidence
├── exports/                  generated Sovereignty Bundles
├── quarantine/               untrusted imports
└── backups/                  local encrypted backup staging
```

## 3. Immutability classes

### Image immutable

OS content is replaced only by signed image activation.

### Artifact immutable

Release artifacts and Kristal artifacts are addressed by identity and never modified in place. New content produces a new identity or version.

### Append-oriented

Receipts, activation history, revocations, and critical audit events append new records. Correction produces a superseding record.

### Mutable operational state

Cases, Tasks, sessions, caches, and work queues remain mutable under product transaction rules.

## 4. Encryption

Sensitive Orgo, identity, audit, rights, and export data MUST be encrypted at rest. Keys SHOULD be scoped by tenant and purpose. A storage snapshot MUST NOT implicitly become an authorized plaintext export.

## 5. Runtime Pack cache policy

Each channel MUST define:

- maximum disk allocation;
- active pack;
- last-known-good pack;
- pinned packs;
- highest activated release identity;
- downgrade policy;
- eviction order;
- stale and expiry handling.

The active and last-known-good packs MUST survive ordinary garbage collection.

## 6. Quarantine

Removable media and offline bundles enter quarantine. The system MUST verify media policy, manifest, signature, hashes, compatibility, audience, and revocation state before moving content into an installed store.

## 7. Backup semantics

Backups MUST identify:

- product and schema versions;
- tenant and data class;
- encryption and key dependency;
- snapshot consistency point;
- included and excluded artifacts;
- restore prerequisites;
- retention and deletion policy.

## 8. Deletion and withdrawal

Content-addressed identity does not eliminate legal or governance deletion duties. The system MUST support revocation, removal from authorized distribution, cache purge, cryptographic erasure where applicable, and retention of minimal non-sensitive proof that a governed transition occurred.
