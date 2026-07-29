# Incident Response

## 1. Incident classes

- host or service compromise;
- signing-key compromise;
- malicious or defective release;
- policy capture or erroneous rule;
- privacy or cross-tenant disclosure;
- cultural-rights violation;
- Kristal integrity or authority failure;
- identity/credential fraud;
- denial of service;
- lost/stolen node;
- recovery or backup failure.

## 2. Response lifecycle

```text
detect → classify → contain → preserve evidence → decide
       → revoke/rollback/repair → communicate → recover
       → post-mortem → update policy/artifacts/tests
```

## 3. Containment

Containment MAY isolate a service, freeze a channel, revoke a key, disable an integration capability, switch to known-good artifacts, or enter hermetic mode. Containment MUST avoid destroying evidence unnecessarily.

## 4. Governance

High-impact containment and disclosure decisions use emergency policy, defined authority, receipts, expiry, and subsequent review. Technical urgency does not erase accountability.

## 5. Communication

Notices distinguish confirmed facts, suspected scope, affected capabilities, user action, temporary safeguards, and unknowns. The system MUST NOT claim certainty that evidence does not support.

## 6. Recovery

Recovery verifies clean image, trust roots, policies, artifacts, data integrity, and credential rotation. Returning services pass acceptance tests before rejoining normal traffic.

## 7. Post-mortem

Post-mortems are blameless regarding ordinary error but explicit about responsibility and control failure. Resulting actions become Orgo Tasks and may produce new policy, releases, Kristal knowledge, or conformance vectors.
