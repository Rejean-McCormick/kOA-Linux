# Publication Gateway persistence migration

`0001_initial.sql` defines the first relational representation of state owned by Publication Gateway:

- publication request identities and lifecycle state;
- governance decisions and obligations;
- destination attempts, including partial and uncertain delivery;
- durable publication receipts;
- append-only withdrawal, revocation, correction, expiry, remediation, and limitation records.

The migration does not create tables for source-component content, Mediatheque records, UCKK remote state, Identity and Trust records, policy bundles, or Audit Broker evidence. Those remain owned by their respective authorities.

The current adapter in this bundle, `FilesystemReceiptStore`, persists immutable receipts and append-only state changes as canonical JSON. The SQL migration is retained for validated relational deployments and data migration tooling. Application wiring must select one authoritative receipt backend; it must not dual-write both stores.

## Safety properties

- The migration is enclosed in one explicit transaction.
- Publication receipts are immutable historical records.
- State changes reference an existing receipt and cannot claim that history was erased.
- Partial or uncertain delivery cannot enable automatic retry.
- Idempotency identities are unique.
- Foreign keys prevent deletion of referenced publication history.

Validate the migration by applying it to a new database and by proving that a failed statement rolls the transaction back before activation.
