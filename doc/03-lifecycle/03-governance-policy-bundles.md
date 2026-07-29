# Governance Policy Bundle Lifecycle

## 1. Purpose

Policy is a release artifact. It MUST NOT be treated as untracked administrator configuration when it affects authorization, disclosure, rights, decision procedures, activation, AI use, or recourse.

## 2. Bundle contents

A bundle contains:

- manifest and unique identity;
- policy modules;
- schemas;
- declared input facts;
- reason-code catalog;
- obligations catalog;
- test vectors;
- migration or supersession rules;
- owner and approval metadata;
- signature envelope.

## 3. Authoring and review

Policy changes pass through an explicit Orgo workflow. The workflow records proposal, rationale, affected groups, simulation results, approvals, dissent, effective date, and recourse procedure.

## 4. Static validation

Before publication, the build pipeline checks:

- schema validity;
- missing references;
- unreachable or contradictory rules;
- nondeterministic functions;
- excessive resource use;
- unsupported runtime features;
- changed outcomes against a regression corpus;
- separation-of-duty violations.

## 5. Simulation

High-impact policy SHOULD be evaluated against historical or synthetic decision cases. Simulation output is advisory evidence; it does not itself authorize activation.

## 6. Activation

The bundle is staged, verified, compatibility-checked, and activated atomically. The active and previous known-good bundles remain available. Existing decision receipts retain their original policy identity.

## 7. Emergency policy

Emergency policy has explicit scope, start, expiry, authority, and review. It MUST NOT become permanent through omission.

## 8. Forking and local governance

A tenant MAY fork policy under its authority. The fork receives a new identity and lineage. It MUST NOT masquerade as the upstream policy or authority channel.
