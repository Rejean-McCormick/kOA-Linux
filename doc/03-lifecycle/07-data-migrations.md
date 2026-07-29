# Data Migrations

## 1. Principles

Migrations are versioned release artifacts. They MUST be observable, restartable or safely resumable, and bound to compatible service versions.

## 2. Migration classes

- additive schema change;
- backfill;
- index build;
- contract transition;
- data classification change;
- encryption/key migration;
- tenant split/merge;
- export/import format migration.

## 3. Expand/contract

Online services SHOULD use:

1. expand schema;
2. deploy code compatible with old and new forms;
3. backfill with checkpoints;
4. switch reads/writes;
5. verify;
6. contract only after rollback window closes.

## 4. Irreversible changes

An irreversible migration MUST be declared as such. It requires a tested backup/restore path, explicit approval, and a forward-repair plan. It MUST NOT be described as safely rollbackable.

## 5. Offline nodes

Offline nodes may skip multiple versions. Migrations MUST declare supported upgrade paths and reject unsupported jumps with a stable diagnostic.

## 6. Tenant safety

Migration progress, failure, and locks are tenant-aware. Failure for one tenant MUST NOT corrupt another tenant or silently expose cross-tenant data.

## 7. Epistemic versus operational migration

Operational schema migrations do not rewrite Kristal content identity. Kristal contract changes create new declared artifacts or projections with lineage.
