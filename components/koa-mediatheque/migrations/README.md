# kOA Mediatheque migrations

`0001_initial.sql` creates the component-owned structured store for media records,
versions, immutable publication receipts, and the bounded local job queue.

The migration deliberately does **not** create tables for content bytes, search
indexes, UCKK state, Publication Gateway decisions, Audit Broker records, identity,
or policy. Managed bytes remain in the component-owned blob root; external owner
results are retained only as immutable references or receipts.

## Application

Apply migrations in lexical order in one exclusive maintenance transaction before
the service becomes ready. The migration requires SQLite with foreign-key and JSON
validation support. Reapplying it is safe because every object is guarded with
`IF NOT EXISTS` and the migration ledger uses `INSERT OR IGNORE`.

After applying a migration:

1. enable `PRAGMA foreign_keys = ON` for every connection;
2. run `PRAGMA foreign_key_check`;
3. require `PRAGMA integrity_check` to return `ok`;
4. coordinate a database checkpoint with the managed-content manifest before a
   backup is declared usable.

Publication receipts are immutable. Their update and deletion triggers are an
intentional preservation boundary; corrections must be represented by a new
receipt or explicit lineage rather than rewriting history.
