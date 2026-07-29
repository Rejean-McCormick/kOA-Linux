# Component — `koa-publication-gateway`

## 1. Purpose

The Publication Gateway is the controlled boundary between private operational domains and public/common surfaces. It prevents direct database coupling and enforces selective disclosure.

## 2. Supported flows

### Konnaxion to Orgo

- structured submissions;
- public decisions requiring execution;
- validation or review requests;
- incidents and user feedback;
- distribution problems.

### Orgo to Konnaxion

- approved publications;
- non-sensitive progress summaries;
- public decision records;
- released Kristal references;
- redacted accountability reports;
- withdrawal or revocation notices.

## 3. Publication pipeline

```text
candidate output
  → schema validation
  → data classification
  → disclosure and rights policy
  → redaction/transformation
  → human or dual approval when required
  → signed publication bundle
  → Konnaxion import
  → publication receipt
```

## 4. Guarantees

The gateway MUST:

- preserve source and correlation identifiers;
- record the policy and approvals applied;
- prevent sensitive-field leakage;
- support withdrawal and supersession;
- be idempotent;
- avoid mutable shared storage;
- reject unknown data classifications;
- keep public and confidential receipts distinct.

## 5. Failure behavior

A disclosure-policy failure blocks publication but does not roll back the originating Orgo workflow. The workflow enters a reviewable state with stable reason codes.

## 6. Transformations

Transformations MUST be declared and reproducible. AI MAY propose a redaction or summary only when policy allows; binding publication uses deterministic validation and required human/community review.
