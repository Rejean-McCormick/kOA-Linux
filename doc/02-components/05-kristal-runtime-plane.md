# Plane — Kristal Runtime

## 1. Purpose

The Kristal Runtime Plane verifies, stores, activates, queries, and exposes portable epistemic artifacts on hubs and endpoints. It is optimized for predictable offline execution.

## 2. Owned responsibilities

The plane owns:

- Runtime Pack manifest verification;
- content and file hash verification;
- signature and trust-root verification;
- compatibility checks;
- tenant/channel-separated pack storage;
- atomic activation and rollback;
- constrained deterministic query execution;
- local indexes;
- reader-policy evaluation support;
- status and provenance exposure;
- revocation and downgrade safety state.

## 3. Non-responsibilities

The Runtime Plane is not:

- a workflow engine;
- a voting system;
- an operational audit store;
- a universal graph database;
- a full SPARQL endpoint requirement;
- the owner of Konnaxion or Orgo user state.

## 4. Artifact model

Kristal v5-oriented deployments may handle:

- Structured Epistemic State;
- Working Exchange;
- Reference Exchange;
- validation decisions;
- authority recognition records;
- federation manifests;
- reader policies;
- Runtime Packs;
- query contracts;
- revocation and update records.

Claim-IR and SenTient are optional paths for probabilistic extraction and ambiguity resolution, not universal prerequisites.

## 5. Activation sequence

```text
fetch/import
  → quarantine
  → verify channel and audience
  → verify manifest signature
  → verify file inventory
  → check revocation and downgrade policy
  → check query/profile compatibility
  → policy decision
  → atomic activation by node agent
  → health verification
  → retain previous known-good state
```

## 6. Offline correctness

Trust roots required for correctness MUST be provisioned or securely cached before offline activation. The runtime MUST NOT fetch a trust root from the network at activation time and then treat it as trusted without an independent chain.

## 7. Query behavior

Queries MUST have explicit contracts, stable ordering, bounded resource use, and deterministic errors. Reader policy affects visibility; it MUST NOT rewrite underlying artifact status.

## 8. Feedback

Operational feedback such as activation failure, query errors, and performance summaries may be sent to Orgo. Feedback MUST NOT mutate epistemic content directly.
