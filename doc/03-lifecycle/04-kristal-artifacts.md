# Kristal Artifact Lifecycle

## 1. General lifecycle

```text
source/input
  → Structured Epistemic State
  → optional Claim-IR and SenTient resolution
  → Working Exchange
  → review and validation decisions
  → authority recognition
  → Reference Exchange
  → Runtime Pack
  → distribution and activation
  → feedback, revision, supersession, or revocation
```

Compilation, validation, recognition, and distribution are distinct. A working artifact may exist without being a recognized reference, and reader policy determines what is visible in a context.

## 2. Build identity

Every build records:

- input artifact identities;
- schemas and contract versions;
- compiler and toolchain identity;
- policy selections;
- deterministic mode and resource limits;
- output identities;
- warnings and unresolved states.

## 3. Publication

Publication does not mutate an artifact. It associates immutable artifact identity with channel, audience, authority, and status metadata.

## 4. Runtime Pack compilation

A Runtime Pack is derived from declared source artifacts and policies. It MUST include a manifest, query contract, file inventory, source lineage, compatibility requirements, and status metadata.

## 5. Activation

Konnaxion owns the product-facing request and status experience. `koa-policy-runtime` evaluates activation policy. `koa-node-agent` performs the atomic filesystem/state transition. The Kristal Runtime verifies and serves the active pack.

## 6. Revocation and supersession

Revocation and supersession are signed records. Offline nodes apply the newest trusted revocation epoch they possess and display staleness when freshness cannot be established.

## 7. Tenant independence

Tenant IDs, ACLs, approvals, assignments, and distribution status MUST NOT alter core Kristal content identity. Tenants may sign, recognize, or distribute the same content differently.

## 8. Conformance

Implementations MUST test signature failure, hash mismatch, incompatible query contract, substitution attack, downgrade attack, atomic activation, offline serving, cache pinning, and rollback authorization.
