# Component — `koa-audit-broker`

## 1. Purpose

`koa-audit-broker` receives, validates, classifies, sequences, stores, and exports audit events and decision receipts without collapsing auditability into surveillance.

## 2. Audit classes

```text
Public Transparency Receipts
Tenant Operational Audit
Restricted Evidence Audit
Personal Privacy Records
Security and Node Audit
```

Each class has separate access, retention, encryption, export, and deletion rules.

## 3. Event requirements

Critical events include:

- authentication and privilege transitions;
- policy decisions;
- workflow approvals and overrides;
- artifact verification and activation;
- publication and withdrawal;
- key and trust-root changes;
- export/import/restore;
- break-glass actions;
- configuration and policy activation;
- access to restricted evidence.

## 4. Integrity

Events SHOULD be chained, signed, or periodically anchored so unauthorized alteration is detectable. The broker MUST reject malformed events and preserve a visible gap/error record rather than silently dropping them.

## 5. Privacy

Public receipts use pseudonymous or aggregate identifiers when possible. Sensitive evidence remains in protected stores and may be referenced by hash or opaque handle. Audit readers MUST themselves be audited.

## 6. Availability

Local critical event capture MUST continue during network outage. Forwarding is asynchronous, resumable, and idempotent. Application correctness MUST NOT depend on immediate central log delivery.

## 7. Export

Exports identify class, scope, time range, redaction policy, integrity proof, and recipient authorization. An audit export is not an unrestricted data dump.
