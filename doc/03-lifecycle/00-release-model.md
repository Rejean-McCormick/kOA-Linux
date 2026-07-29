# Release Model

## 1. Four release channels

kOA separates four independently versioned and signed channels:

1. **OS Image** — kernel, systemd, host runtime, node services, recovery, graphical base;
2. **Service Bundle** — Konnaxion, Orgo, Kristal Runtime, gateways, and optional services;
3. **Governance Policy Bundle** — roles, decisions, disclosure, rights, AI capabilities, activation, recourse, and emergency rules;
4. **Kristal Artifact Channels** — epistemic states, Exchanges, decisions, recognition, Runtime Packs, reader policies, and revocations.

No channel may silently embed and activate another channel's authority.

## 2. Release Set

A Release Set is the signed compatibility statement for a tested combination. It declares at minimum:

- release-set identity and version;
- OS image identity;
- service bundle identity;
- Governance Policy Bundle identity;
- supported Kristal and query contracts;
- minimum and maximum schema versions;
- node profiles supported;
- migration requirements;
- rollback constraints;
- signer and signature envelope.

## 3. Lifecycle states

```text
proposed → built → verified → approved → published
         → staged → active → superseded → revoked/retired
```

The states of each channel are independent. A published artifact is not automatically approved for every tenant or node.

## 4. Promotion

Promotion across development, test, pilot, and production MUST preserve artifact identity. Rebuilding source for each environment creates a different artifact and requires independent verification.

## 5. Database compatibility

Zero-downtime or blue/green activation requires schema compatibility with both old and new code while they coexist. Migrations use expand/contract or another explicitly reversible method.

## 6. Release evidence

A production release SHOULD include:

- software bill of materials;
- provenance attestation;
- reproducible-build evidence;
- vulnerability scan results;
- schema and contract test results;
- conformance vectors;
- migration plan;
- rollback plan;
- known limitations;
- signed approvals.

## 7. Canary and blue/green

Canary MAY be used for services and selected artifact channels when observability and cohort isolation exist. Blue/green SHOULD be used where a complete parallel state can be validated before switching. Neither pattern removes the need for database compatibility or rollback testing.
