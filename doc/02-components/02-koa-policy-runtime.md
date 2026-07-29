# Component — `koa-policy-runtime`

## 1. Purpose

`koa-policy-runtime` turns versioned sociotechnical rules into deterministic machine-readable decisions. It is the policy decision point for authorization, disclosure, activation, rights, AI capability, export, emergency action, and other governed operations.

## 2. Core properties

The runtime MUST be:

- deterministic for the same declared inputs and policy version;
- offline-capable for locally required decisions;
- side-effect free during evaluation;
- capable of returning `allow`, `deny`, or `require_review`;
- explicit about missing facts and uncertainty;
- able to emit a signed or integrity-protected decision receipt;
- bounded in CPU, memory, recursion, and evaluation time.

## 3. Inputs

Typical input fields include:

- subject and authenticated attributes;
- tenant and environment;
- role assignments and delegations;
- action;
- resource identity and data class;
- workflow state;
- authority and reader-policy context;
- node profile and assurance level;
- current time plus clock-confidence metadata;
- active Release Set;
- emergency state;
- requested disclosure audience;
- cultural rights and consent state.

The runtime MUST distinguish provided facts, derived facts, and unavailable facts.

## 4. Policy domains

A Governance Policy Bundle MAY contain:

- authorization policy;
- separation-of-duties policy;
- workflow transition policy;
- disclosure policy;
- Kristal activation policy;
- reader-policy selection constraints;
- AI input/output capability policy;
- cultural rights and consent policy;
- export and exit policy;
- retention policy;
- emergency and break-glass policy;
- integration capability policy;
- SmartVote and advisory-reading policy references.

## 5. Decision receipt

A receipt includes the policy bundle and rule identity, normalized inputs or their hashes, outcome, reason codes, obligations, review requirements, timestamp, clock confidence, and correlation ID.

Obligations are declarative, for example:

```json
{
  "outcome": "allow",
  "obligations": [
    {"type": "redact", "fields": ["witness_identity"]},
    {"type": "retain_receipt", "days": 2555},
    {"type": "require_dual_control"}
  ]
}
```

## 6. Policy activation

A new bundle is staged, verified, conformance-tested, compatibility-checked, and activated atomically. The runtime retains the active and last-known-good bundles. Policy rollback is itself governed and receipted.

## 7. Ownership boundary

The runtime evaluates policy; it does not own workflow state, Kristal semantics, user interfaces, or privileged enforcement. Orgo orchestrates reviews and approvals. `koa-node-agent` applies allowed node mutations.

## 8. Testing

Every bundle MUST include or reference:

- positive and negative test vectors;
- separation-of-duty cases;
- unknown-input behavior;
- deterministic output vectors;
- resource-limit tests;
- backward/forward compatibility expectations;
- recourse and supersession behavior.
