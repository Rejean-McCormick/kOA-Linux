# Threat Model

## 1. Protected assets

The system protects:

- human safety and due process;
- private Orgo evidence and workflows;
- public accountability and decision integrity;
- identity, delegation, and credentials;
- governance policies and their history;
- Kristal content, provenance, status, and lineage;
- signing and trust-root material;
- node availability and recovery;
- cultural rights, consent, and community authority;
- credible exit and institutional memory.

## 2. Adversaries

- remote unauthenticated attacker;
- malicious or compromised participant;
- compromised public service;
- compromised private service;
- malicious tenant administrator;
- privileged host operator;
- malicious integration or supply-chain dependency;
- stolen node or removable media;
- federation peer with conflicting or deceptive authority claims;
- AI system producing confident but unsupported output;
- governance insider changing rules gradually;
- resource exhaustion and noise-flood attacker.

## 3. Failure and capture scenarios

### T-01 — Host or service compromise

An attacker gains code execution and attempts lateral movement, key access, or persistent mutation.

Controls: immutable image, rootless containers, LSM, seccomp, minimal capabilities, domain identities, read-only images, signed updates, narrow broker.

### T-02 — Release supply-chain compromise

A build or registry serves malicious or substituted content.

Controls: digest pinning, independent signature verification, provenance, SBOM, reproducibility, Release Set compatibility, revocation, offline verification.

### T-03 — Policy capture

Rules, thresholds, disclosure, or emergency powers are quietly changed.

Controls: policy as signed release, diff and simulation, multi-party approval, receipts, public rule identity, expiry, recourse, fork/exit.

### T-04 — Semantic capture

Definitions, ontologies, translation, or authority defaults are manipulated.

Controls: versioned semantic artifacts, explicit authority channels, reader policies, lineage, contested states, local forkability, multiple readings.

### T-05 — Ranking capture

Brigading, reputation laundering, hidden weighting, or model manipulation controls visibility.

Controls: baseline/advisory separation, domain-bounded signals, public policy identity, explanation endpoints, anti-Sybil controls, audit and recourse.

### T-06 — Privacy collapse through audit

Accountability mechanisms expose vulnerable people or protected evidence.

Controls: audit classes, selective disclosure, pseudonymous public receipts, encrypted evidence, access audit, retention and deletion policy.

### T-07 — Public/private contamination

Konnaxion input reaches Orgo or trusted knowledge without validation, or Orgo secrets leak into public surfaces.

Controls: separate domains, Publication Gateway, classification, redaction, approval, no shared database, signed publication bundles.

### T-08 — AI overreach

AI output becomes hidden decision, policy, cultural authority, or privileged operation.

Controls: AI capability policy, provenance, uncertainty, human/community review, deterministic gates, no direct node privilege, optional AI path.

### T-09 — Offline downgrade and stale trust

A disconnected node accepts an old but validly signed artifact that is revoked or insecure.

Controls: monotonic release/revocation state, downgrade protection, expiry and clock confidence, stale status, emergency override policy.

### T-10 — Malicious offline media

A removable bundle exploits parsing, storage, or operator trust.

Controls: quarantine, bounded parsers, no auto-execution, signature and inventory checks, decompression limits, policy decision, isolated staging.

### T-11 — Denial of service and retry storm

A dependency failure exhausts threads, queues, storage, or network.

Controls: timeout budgets, bulkheads, backoff and jitter, circuit breakers, quotas, bounded queues, priority sync, graceful degradation.

### T-12 — Insider root abuse

A privileged operator changes state outside governance.

Controls: immutable base, narrow normal APIs, privileged action receipts, dual control for critical keys/trust, attestation, drift detection, external audit, exit rights.

### T-13 — Credential and Sybil attacks

Fake identities, impersonation, or credential laundering undermine legitimacy.

Controls: layered identity, scoped credentials, issuer verification, domain-bounded competence, revocation, contestable credential evidence.

### T-14 — Cultural extraction

Restricted or community-governed material is exposed, reused, or sent to AI without authority.

Controls: rights policy at ingest/read/export/render/AI boundaries, audience-specific packs, encryption, withdrawal, no-AI capability enforcement.

### T-15 — Recovery capture

An attacker abuses recovery to replace trust roots or extract data.

Controls: separate recovery environment, stronger authentication, dual control, sealed keys, explicit receipts, restricted exports, post-event review.

## 4. Security objectives

The architecture prioritizes:

1. safety and non-fabrication of authority;
2. containment and recoverability;
3. confidentiality of protected data;
4. integrity and provenance;
5. local availability;
6. auditability and recourse;
7. replaceability and exit.

## 5. Residual risk

No technical design proves legitimate governance or correct knowledge. The system can make rules, sources, status, decisions, and failures more visible and contestable; it cannot eliminate human abuse, institutional conflict, or physical coercion.
