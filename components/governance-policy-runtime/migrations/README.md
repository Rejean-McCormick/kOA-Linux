# Governance Policy Runtime filesystem state migrations

Governance Policy Runtime owns filesystem state rather than a shared database.
This directory documents the migration contract for the layouts implemented by
`filesystem_bundle_store.py` and `filesystem_receipt_store.py`.

## Current layout: version 1

```text
<state-root>/
├── bundles/<artifact-id>/<semantic-version>/
│   ├── bundle.json
│   └── record.json
├── state/
│   ├── active-policy-set.json
│   └── .store.lock
└── receipts/<receipt-id-sha256-prefix>/<receipt-id-sha256>.json
```

`bundle.json` is immutable canonical JSON. `record.json` contains the local
candidate disposition and verification references. Receipts are append-only
integrity envelopes. `active-policy-set.json` is the sole atomic pointer to the
complete active set and retains the immediately previous complete valid set.

## Migration rules

1. Stop new lifecycle mutations or keep evaluations on the previous valid set.
2. Back up the complete owned state root and verify its digests.
3. Read and validate every source record before writing any new representation.
4. Write a new versioned layout beside the current layout; never rewrite bundle
   bytes or receipt identities in place.
5. Preserve bundle references, canonical digests, decision receipt identities,
   activation receipt references, retired policy-set identifiers, provenance,
   and the previous-valid recovery path.
6. Verify every migrated record and complete policy-set snapshot.
7. Switch the layout pointer atomically only after complete validation.
8. Produce migration and recovery evidence through the application layer and
   Audit Broker public interface.
9. Retain the old verified layout until rollback is no longer required by the
   active lifecycle, evidence, and retention contracts.

Partial migration, mixed policy authority, inferred compatibility, deletion of
historical reproducibility material, and direct writes to another component's
state are prohibited. When rollback is incompatible, migration must block and
require an explicit forward-repair or recovery workflow.
