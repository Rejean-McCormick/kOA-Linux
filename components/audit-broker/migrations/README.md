# Audit Broker migrations

`0001_initial.sql` creates only Audit Broker-owned state:

- bounded accepted audit records and idempotency keys;
- ordered chain-of-custody entries;
- retention and hold projections;
- access/disclosure receipts and disclosure packages;
- append-only correction and invalidation lineage;
- migration state.

The migration deliberately stores structured values as canonical JSON text. This
keeps the logical schema identical for SQLite and PostgreSQL while avoiding any
claim that a shared physical database transfers source-component ownership.

## Application

The SQLite and PostgreSQL adapters expose an explicit `migrate()` operation.
Migration is never performed as an implicit side effect of a read or write.
Production activation must run migration under the component lifecycle and
backup/recovery controls.

The SQL is intentionally limited to portable DDL. Append-only behavior is
implemented by the adapters and should additionally be enforced by deployment
roles: the Audit Broker runtime role requires `INSERT` and bounded projection
updates, but no arbitrary `UPDATE` or `DELETE` on immutable record, custody,
receipt, package, or invalidation tables.

## Versioning

The initial schema version is `0001`. A later semantic migration requires the
accepted owner decision, contract/schema update, compatibility validation,
recovery point, migration test, evidence, and rollback or forward repair
specified by the component contract.
