# Principal Domain — Orgo

## 1. Role

Orgo is the principal private and operational plane of kOA. It converts signals into structured, accountable work and preserves execution continuity in online, intermittent, and hermetic environments.

## 2. Core objects

Orgo owns operational state such as:

- Signals;
- Cases;
- Tasks;
- assignments;
- approvals;
- reviews;
- escalations;
- deadlines and closure criteria;
- synchronization sessions and conflicts;
- distribution state;
- operational audit;
- post-mortems and follow-up.

## 3. Architecture

Orgo SHOULD use a modular domain architecture with hexagonal ports and adapters. Core logic MUST remain testable without live external services. Online and offline persistence adapters MAY differ while preserving domain contracts.

## 4. Kristal control-plane role

Orgo orchestrates work around Kristal:

```text
intake → structure → resolve when needed → review → validate
       → recognize → publish → distribute → observe → revise
```

Orgo stores who requested, reviewed, approved, distributed, or revoked work. Kristal stores epistemic payload and its declared decisions/references. Orgo MUST NOT alter Kristal content identity by inserting tenant workflow metadata.

## 5. Hermetic operation

An Orgo deployment MAY operate on a closed LAN or air-gapped node. Required identity, policy, queues, storage, trust roots, and operational interfaces MUST remain local for the declared profile.

## 6. Public disclosure

Orgo publishes only through a controlled contract. The Publication Gateway applies disclosure, redaction, rights, consent, audience, and approval policy. Direct database replication into Konnaxion is forbidden.

## 7. Workflow guarantees

Workflows MUST define:

- states and permitted transitions;
- responsible roles;
- separation of duties;
- timeouts and escalation;
- idempotency;
- retry and compensation semantics;
- evidence requirements;
- closure and post-mortem criteria;
- recourse and reopening rules.

## 8. Sensitive-data posture

Orgo data is private by default. The service MUST support tenant separation, role-based disclosure, encryption at rest, controlled exports, protected evidence, retention policy, and access auditing.

## 9. Offline synchronization

Synchronization uses explicit sessions, stable object/event identities, conflict classification, and deterministic merge policy where possible. Conflicts affecting authority, approval, rights, or sensitive evidence MUST require review rather than last-write-wins.
