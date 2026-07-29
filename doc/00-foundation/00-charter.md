# kOA Linux Founding Charter

## 1. Mission

kOA Linux is the sovereign execution layer of the kOA Digital Ecosystem. Its mission is to let a community or organization retain a minimum local capacity to **know, choose, act, and remember** even when the network, a cloud service, an external operator, or part of the ecosystem is unavailable, compromised, or contested.

The system MUST make the following guarantees technically enforceable:

1. local continuity;
2. verifiable integrity;
3. explicit and versioned governance;
4. selective auditability;
5. determinism where authority, safety, or reproducibility require it;
6. modularity and replaceability;
7. separation between public coordination and sensitive execution;
8. portability, self-hosting, and credible exit;
9. recourse—the ability to contest, correct, revoke, supersede, or replace;
10. optional, bounded, and non-sovereign AI.

## 2. Product nature

kOA Linux is:

- an **immutable Linux appliance image**;
- a **node runtime** for local and distributed operation;
- a **sociotechnical policy runtime**;
- a hardened host for Konnaxion, Orgo, and the Kristal Runtime Plane;
- an offline-capable operating surface;
- a signed and reversible update chain;
- a verified export, transfer, restore, and recovery capability.

kOA Linux is not:

- a custom Linux kernel fork;
- a general-purpose desktop distribution intended to run arbitrary software without policy;
- a rewrite of Konnaxion or Orgo;
- a system in which a vote, reputation score, or AI output directly receives operating-system privilege;
- a universal database;
- a mandatory blockchain;
- a Kubernetes cluster on every endpoint;
- a mechanism that claims to define one universal truth.

## 3. Governability promise

A function is governable only when all of the following are true:

- its rule and owner are identifiable;
- the rule is versioned and can be inspected by authorized parties;
- the rule can be challenged or superseded through an explicit procedure;
- execution produces a decision receipt or an equivalent trace;
- the result is inspectable under applicable disclosure rights;
- protected data remains protected;
- uncertainty or verification failure does not silently become authority;
- a recourse or correction path exists;
- the original operator can be replaced without losing essential artifacts, identities, or institutional memory.

## 4. Non-domination principles

The system MUST resist five forms of domination.

### 4.1 Infrastructural domination

No remote service may be required for the minimum local consultation, verification, and operational continuity defined by a node profile.

### 4.2 Semantic domination

Definitions, ontologies, reader policies, authority channels, and recognition relationships MUST be explicit, versioned, and replaceable. Contested meaning MUST remain representable as contested.

### 4.3 Algorithmic domination

No opaque score or hidden ranking may become the only reading of a civic decision, recommendation, or discovery result. Where weighted readings exist, baseline and advisory readings MUST remain distinguishable.

### 4.4 Administrative domination

Root access MUST NOT be the normal governance API. Sensitive actions MUST pass through declared, policy-evaluated, least-privilege operations that produce receipts.

### 4.5 Lock-in domination

The system MUST provide complete exports, documented formats, portable trust material where lawful, and a restore procedure that does not depend on the original operator.

## 5. Architectural unity

Konnaxion and Orgo are the two principal product planes:

```text
Konnaxion: discover, connect, learn, deliberate, publish, and distribute.
Orgo:      sense, organize, assign, approve, execute, close, and audit.
```

Kristal is their shared epistemic foundation:

```text
Kristal: structure, identify, version, validate, recognize, federate,
         distribute, and query portable epistemic artifacts.
```

The kOA system runtime does not compete with those products. It enforces policy, protects boundaries, provides boot and recovery, maintains node identity and trust, activates signed releases, and preserves local continuity.

## 6. Constitutional boundary

Governance rules MAY authorize operations, but they MUST NOT bypass technical safety invariants. Technical operators MAY maintain the system, but they MUST NOT silently redefine governance meaning. The architecture therefore separates:

- **legitimacy**: who may decide under which procedure;
- **epistemic status**: what is known, disputed, provisional, recognized, or revoked;
- **operational authority**: who may initiate and approve work;
- **system privilege**: which narrow mechanism may change machine state.

No single component owns all four.
