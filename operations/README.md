# kOA Operations

`koa-operations` is a bounded operational coordinator. This bundle implements the
backup `plan -> run -> verify` cycle and its correlated evidence. It does not own
component state, read component databases directly, activate restored state, or
replace component export and snapshot contracts.

## Authority boundary

A plan consumes:

1. a serialized public `BackupPlan` projection from B-0092;
2. owner-produced committed checkpoints and owner evidence;
3. release and authority references supplied by B-0099;
4. protected target identities and paths resolved by the active profile;
5. explicit resource, retention, encryption, RPO, RTO, and restore-test bounds.

The coordinator copies only regular owner-produced checkpoint files. Immutable
references and regenerable members remain references. Protected private-key
material is rejected from ordinary backup plans.

## CLI

```console
koa-operations backup plan \
  --config backup-config.json \
  --output backup-plan.json \
  --evidence-dir evidence

koa-operations backup run \
  --plan backup-plan.json \
  --output backup-run.json \
  --evidence-dir evidence

koa-operations backup verify \
  --plan backup-plan.json \
  --run-result backup-run.json \
  --canonical-schema docs/contracts/artifact-contracts/backup-set.schema.json \
  --output backup-verification.json \
  --evidence-dir evidence
```

All commands print machine-readable JSON and return non-zero status on invalid,
failed, or blocked work. Outputs are immutable by default. Reusing a path is an
error rather than an implicit overwrite.

## States and evidence

The run stage produces an `assembled` manifest and durable target
acknowledgements. Verification checks inventory, owner/checkpoint identity,
payload digests, acknowledgements, identical manifests across targets, and the
canonical backup-set schema. A successful verification can mark a set
`restore_eligible`; it never marks it `restore_tested`.

Every plan, run, and verification transition writes an immutable evidence record
under its correlation identity. Records form a digest chain and contain only a
digest of detailed operational data.

## Missing canonical schema in the supplied corpus

The normative backup document references
`docs/contracts/artifact-contracts/backup-set.schema.json`, but that schema is not
present in the supplied repository snapshot. Therefore verification without an
explicit valid schema returns `blocked`, writes evidence, and exits non-zero. It
does not convert an operational integrity check into a canonical
`restore_eligible` claim.

## Failure behavior

A failed attempt never overwrites an existing set. Staging is removed where safe,
committed targets are reported explicitly if a multi-target finalization becomes
partial, and the previous verified restore-eligible backup remains untouched.
Network access and optional external integrations are not required by this core.
