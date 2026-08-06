# Kristal Runtime migrations

`0001_initial.sql` creates only state owned by Kristal Runtime:

- immutable artifact index entries for Runtime Packs and Kristal artifacts;
- Runtime Pack verification records;
- activation, rollback, blocked, and failed transition records;
- the singleton active/previous Runtime Pack pointer.

Artifact bytes and manifests remain in the component-owned filesystem artifact store. The SQLite index never becomes the sole authority for artifact identity or content integrity; every filesystem read is checked against its immutable record and manifest. Local indexes are rebuildable from verified artifacts.

The migration is wrapped in `BEGIN IMMEDIATE` / `COMMIT` so a DDL failure cannot leave a partially activated schema. Apply it once through the component bootstrap using `SQLiteIndexStore.initialize(...)`. Do not run this migration against another component's database.

Runtime Pack activation and rollback are single SQLite transactions. The previous known-good reference remains present until the new state and its transition record commit together. Verification, publication, staging, and activation remain separate lifecycle events.
