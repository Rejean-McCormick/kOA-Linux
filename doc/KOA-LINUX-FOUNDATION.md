# kOA Linux — Consolidated Founding Specification
**Version:** 0.2-foundation-english  
**Date:** 2026-07-29  
**Status:** normative target architecture; implementation validation required
This edition consolidates the normative Markdown documents in this repository. The individual files remain the maintenance units. JSON Schemas, examples, and systemd/Quadlet samples remain separate files in the same archive.
## Table of Contents
- [kOA Linux Founding Charter](#koa-linux-founding-charter) — `00-foundation/00-charter.md`
- [Normative Invariants](#normative-invariants) — `00-foundation/01-normative-invariants.md`
- [Scope and Non-Goals](#scope-and-non-goals) — `00-foundation/02-scope-and-non-goals.md`
- [Glossary](#glossary) — `00-foundation/03-glossary.md`
- [System Context](#system-context) — `01-architecture/00-system-context.md`
- [Logical Architecture](#logical-architecture) — `01-architecture/01-logical-architecture.md`
- [Physical Architecture](#physical-architecture) — `01-architecture/02-physical-architecture.md`
- [Node Profiles](#node-profiles) — `01-architecture/03-node-profiles.md`
- [Process and Trust Boundaries](#process-and-trust-boundaries) — `01-architecture/04-process-and-trust-boundaries.md`
- [Storage and Filesystem Layout](#storage-and-filesystem-layout) — `01-architecture/05-storage-and-filesystem-layout.md`
- [Network Topology](#network-topology) — `01-architecture/06-network-topology.md`
- [Boot, Session, and Recovery](#boot-session-and-recovery) — `01-architecture/07-boot-session-and-recovery.md`
- [Component — `koa-session-shell`](#component-koa-session-shell) — `02-components/00-koa-session-shell.md`
- [Component — `koa-node-agent`](#component-koa-node-agent) — `02-components/01-koa-node-agent.md`
- [Component — `koa-policy-runtime`](#component-koa-policy-runtime) — `02-components/02-koa-policy-runtime.md`
- [Principal Domain — Konnaxion](#principal-domain-konnaxion) — `02-components/03-konnaxion.md`
- [Principal Domain — Orgo](#principal-domain-orgo) — `02-components/04-orgo.md`
- [Plane — Kristal Runtime](#plane-kristal-runtime) — `02-components/05-kristal-runtime-plane.md`
- [Component — `koa-publication-gateway`](#component-koa-publication-gateway) — `02-components/06-publication-gateway.md`
- [Component — `koa-audit-broker`](#component-koa-audit-broker) — `02-components/07-audit-broker.md`
- [Identity and Trust](#identity-and-trust) — `02-components/08-identity-and-trust.md`
- [Release Model](#release-model) — `03-lifecycle/00-release-model.md`
- [Operating-System Updates](#operating-system-updates) — `03-lifecycle/01-os-updates.md`
- [Service Updates](#service-updates) — `03-lifecycle/02-service-updates.md`
- [Governance Policy Bundle Lifecycle](#governance-policy-bundle-lifecycle) — `03-lifecycle/03-governance-policy-bundles.md`
- [Kristal Artifact Lifecycle](#kristal-artifact-lifecycle) — `03-lifecycle/04-kristal-artifacts.md`
- [Offline Bundles](#offline-bundles) — `03-lifecycle/05-offline-bundles.md`
- [Rollback and Recovery](#rollback-and-recovery) — `03-lifecycle/06-rollback-and-recovery.md`
- [Data Migrations](#data-migrations) — `03-lifecycle/07-data-migrations.md`
- [Threat Model](#threat-model) — `04-security/00-threat-model.md`
- [Security Baseline](#security-baseline) — `04-security/01-security-baseline.md`
- [Privacy and Disclosure](#privacy-and-disclosure) — `04-security/02-privacy-and-disclosure.md`
- [Secrets and Keys](#secrets-and-keys) — `04-security/03-secrets-and-keys.md`
- [AI Boundaries](#ai-boundaries) — `04-security/04-ai-boundaries.md`
- [Integration Without Contamination](#integration-without-contamination) — `04-security/05-integration-without-contamination.md`
- [Cultural Rights, Consent, and Community Authority](#cultural-rights-consent-and-community-authority) — `04-security/06-cultural-rights-and-consent.md`
- [Observability](#observability) — `05-operations/00-observability.md`
- [Backup, Restore, and Exit](#backup-restore-and-exit) — `05-operations/01-backup-restore-and-exit.md`
- [Capability-Based Degradation](#capability-based-degradation) — `05-operations/02-capability-degradation.md`
- [SLOs and Health](#slos-and-health) — `05-operations/03-slos-and-health.md`
- [Conformance Tests](#conformance-tests) — `05-operations/04-conformance-tests.md`
- [Incident Response](#incident-response) — `05-operations/05-incident-response.md`
- [ADR-001-standard-maintained-linux-kernel — Use a Standard Maintained Linux Kernel](#adr-001-standard-maintained-linux-kernel-use-a-standard-maintained-linux-kernel) — `08-adrs/ADR-001-standard-maintained-linux-kernel.md`
- [ADR-002-immutable-os-image — Use an Immutable OS Image](#adr-002-immutable-os-image-use-an-immutable-os-image) — `08-adrs/ADR-002-immutable-os-image.md`
- [ADR-003-no-gnome-product-shell — Do Not Use GNOME as the Product Shell](#adr-003-no-gnome-product-shell-do-not-use-gnome-as-the-product-shell) — `08-adrs/ADR-003-no-gnome-product-shell.md`
- [ADR-004-minimal-wayland-and-embedded-web-engine — Use a Minimal Maintained Wayland Stack and Embedded Web Engine](#adr-004-minimal-wayland-and-embedded-web-engine-use-a-minimal-maintained-wayland-stack-and-embedded-web-engine) — `08-adrs/ADR-004-minimal-wayland-and-embedded-web-engine.md`
- [ADR-005-rootless-podman-and-quadlet — Use Rootless Podman and Quadlet for Application Services](#adr-005-rootless-podman-and-quadlet-use-rootless-podman-and-quadlet-for-application-services) — `08-adrs/ADR-005-rootless-podman-and-quadlet.md`
- [ADR-006-konnaxion-and-orgo-co-principal — Treat Konnaxion and Orgo as Co-Principal Product Planes](#adr-006-konnaxion-and-orgo-co-principal-treat-konnaxion-and-orgo-as-co-principal-product-planes) — `08-adrs/ADR-006-konnaxion-and-orgo-co-principal.md`
- [ADR-007-kristal-transversal-epistemic-foundation — Treat Kristal as a Transversal Epistemic Foundation](#adr-007-kristal-transversal-epistemic-foundation-treat-kristal-as-a-transversal-epistemic-foundation) — `08-adrs/ADR-007-kristal-transversal-epistemic-foundation.md`
- [ADR-008-four-release-channels — Separate OS, Services, Governance Policy, and Kristal Channels](#adr-008-four-release-channels-separate-os-services-governance-policy-and-kristal-channels) — `08-adrs/ADR-008-four-release-channels.md`
- [ADR-009-governance-policy-runtime — Introduce `koa-policy-runtime`](#adr-009-governance-policy-runtime-introduce-koa-policy-runtime) — `08-adrs/ADR-009-governance-policy-runtime.md`
- [ADR-010-selective-audit — Use Selective Audit, Not Total Transparency](#adr-010-selective-audit-use-selective-audit-not-total-transparency) — `08-adrs/ADR-010-selective-audit.md`
- [ADR-011-no-kubernetes-on-endpoints — Do Not Require Kubernetes on Endpoints](#adr-011-no-kubernetes-on-endpoints-do-not-require-kubernetes-on-endpoints) — `08-adrs/ADR-011-no-kubernetes-on-endpoints.md`
- [ADR-012-single-narrow-privileged-broker — Use One Narrow Privileged Node Broker](#adr-012-single-narrow-privileged-broker-use-one-narrow-privileged-node-broker) — `08-adrs/ADR-012-single-narrow-privileged-broker.md`
- [Founding Requirements Matrix](#founding-requirements-matrix) — `REQUIREMENTS-MATRIX.md`
- [Sources, Documentary Authority, and Provenance](#sources-documentary-authority-and-provenance) — `SOURCES.md`

---

<!-- Source: 00-foundation/00-charter.md -->

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

---

<!-- Source: 00-foundation/01-normative-invariants.md -->

# Normative Invariants

The following invariants define the minimum acceptable form of kOA Linux. A conforming implementation MUST satisfy every invariant that applies to its declared node profile.

## I-01 — Maintained standard kernel

kOA Linux MUST use a standard Linux kernel from a recognized maintenance chain. Product-specific kernel patches MUST be minimal, published, reviewable, and upstreamable or removable.

## I-02 — Immutable operating-system base

The operating-system base MUST be image-built, signed, and replaced atomically. Production nodes MUST NOT depend on undocumented in-place mutation of `/usr` or equivalent system content.

## I-03 — Verified boot and release identity

A node MUST be able to establish the identity of the booted OS image and the active release set. Deployments requiring high assurance SHOULD bind this identity to Secure Boot, measured boot, TPM-backed evidence, or an equivalent hardware root of trust.

## I-04 — Four independent release channels

OS images, service bundles, governance policy bundles, and Kristal artifact channels MUST have independent identities and signatures. A signed Release Set MUST declare tested compatible combinations.

## I-05 — Konnaxion and Orgo are co-principal

Konnaxion and Orgo MUST be represented as principal peer workspaces. Neither may be implemented as an ungoverned administrative submodule of the other.

## I-06 — Kristal is transversal

Kristal MUST remain a shared epistemic foundation, not an operational database, workflow engine, voting system, or UI framework.

## I-07 — One narrow privileged broker

Normal product services MUST NOT run with unrestricted root privilege. Privileged node mutations MUST pass through `koa-node-agent` or an equivalent narrow broker with an allowlisted operation contract.

## I-08 — Policy before privilege

A sensitive operation MUST receive an explicit policy decision before the privileged broker executes it. The decision and operation MUST be correlated and auditable.

## I-09 — Offline minimum capability

Each node profile MUST declare its offline capability envelope. The endpoint profile MUST retain access to active verified knowledge, local identity, local work, policy evaluation, and recovery without a permanent cloud dependency.

## I-10 — Fail closed for authority

Verification failure, ambiguity, expired trust, or incompatible contracts MUST NOT silently produce an authoritative result. The system MUST withhold activation or execution and expose a stable reason code.

## I-11 — Safe degradation by capability

Fail-closed behavior MUST NOT be interpreted as indiscriminate shutdown. The system MUST distinguish consultation, advisory use, publication, and execution. Context MAY remain visible with explicit status while unsafe activation remains blocked.

## I-12 — Atomic activation and known-good rollback

OS images, service bundles, policy bundles, and Runtime Packs MUST support atomic activation or an equivalent no-partial-state guarantee. A last-known-good state MUST be retained according to policy.

## I-13 — Tenant and security-domain separation

Konnaxion, Orgo, Kristal caches, and tenant data MUST be separated by explicit identities, storage boundaries, trust roots, and disclosure policies. Cross-domain sharing MUST use a declared gateway or contract.

## I-14 — Auditable without becoming a panopticon

The system MUST preserve public accountability and confidential evidence as separate disclosure classes. Auditability MUST NOT require indiscriminate exposure of personal or sensitive data.

## I-15 — Content-addressed immutable knowledge identity

Kristal content identity MUST be derived from declared canonical content, not tenant workflow state, UI metadata, or operator-specific storage paths.

## I-16 — AI is bounded and replaceable

AI MAY propose, extract, classify, summarize, translate, or assist. It MUST NOT become the sole correctness path for core civic transformations or directly grant system privilege.

## I-17 — Open interfaces and credible exit

A tenant MUST be exportable into a documented Sovereignty Bundle and restorable on a clean compatible node. Exit tests MUST be performed, not merely documented.

## I-18 — Deterministic receipts

Policy decisions, activations, publications, releases, and critical transitions MUST emit stable machine-readable receipts with input identities, policy identity, outcome, reason codes, and correlation identifiers.

## I-19 — Integration without contamination

External tools MUST be classified as native, annexed, connected, mimicked, or forbidden. Annexed and connected tools MUST be capability-limited and prevented from silently mutating trusted core state.

## I-20 — Reproducibility is a release property

A release MUST record the source, dependencies, build policy, toolchain identity, configuration, and artifact hashes needed to reproduce or independently verify its outputs.

---

<!-- Source: 00-foundation/02-scope-and-non-goals.md -->

# Scope and Non-Goals

## 1. Scope

This foundation defines the target architecture for a sovereign Linux appliance that hosts the kOA Digital Ecosystem. It covers:

- system image composition and boot;
- node profiles and deployment topology;
- product and trust boundaries;
- local and offline operation;
- policy evaluation and privileged enforcement;
- identity, trust roots, signatures, and release activation;
- Konnaxion, Orgo, and Kristal placement;
- update, rollback, recovery, export, and exit;
- observability, incident response, and conformance;
- examples of systemd and Podman Quadlet integration;
- machine-readable contracts for releases, policies, decisions, nodes, integrations, offline bundles, and cultural rights.

## 2. Normative authority

This documentation defines a target architecture. It does not claim that every implementation detail has already been proven in production. Statements use the following meanings:

- **MUST / MUST NOT**: required for conformance;
- **SHOULD / SHOULD NOT**: expected unless a documented architecture decision explains the exception;
- **MAY**: optional behavior that must still preserve the invariants.

## 3. Deliberate non-goals

### 3.1 Custom kernel development

The project does not aim to maintain a new kernel, scheduler, filesystem, display protocol, or container runtime unless a proven requirement cannot be met by maintained upstream components.

### 3.2 General-purpose workstation compatibility

kOA Linux is an appliance platform. Arbitrary desktop software compatibility is secondary to integrity, reproducibility, bounded capability, and recovery.

### 3.3 Microservices as an objective

Service extraction is not a success metric. Konnaxion and Orgo SHOULD remain modular monoliths or coherent service groups until independent scaling, technology, trust, or lifecycle requirements justify extraction.

### 3.4 Universal online federation

Every node is not required to participate in a public federation. Orgo may operate in a hermetic environment. Federation is explicit, scoped, and revocable.

### 3.5 Universal truth authority

Kristal represents assertions, evidence, validation, recognition, certainty, scope, and disagreement. It does not establish a monopoly over truth.

### 3.6 Full SPARQL on constrained endpoints

Kristal Runtime Packs use constrained, portable query contracts. Full remote graph semantics are not a requirement for endpoints.

### 3.7 Total transparency

The system does not equate auditability with public exposure of all data. Selective disclosure and protected evidence are required.

### 3.8 Mandatory AI

Core correctness, activation, authorization, and recovery MUST remain functional without AI.

### 3.9 Mandatory blockchain

Content addressing, signatures, append-only receipts, and federation do not require a blockchain. A ledger MAY be integrated only when its threat model and governance benefit are explicit.

### 3.10 Hyperscale architecture on endpoints

Cell-based architecture, service meshes, Kubernetes, and global sharding are not endpoint requirements. They MAY be used in control or build environments when justified by measured scale and failure-domain needs.

## 4. Decisions intentionally left to implementation profiles

The following require prototype evidence or deployment-specific selection:

- base distribution and image technology;
- bootc/OSTree versus an equivalent immutable image mechanism;
- SELinux versus another maintained LSM profile;
- TPM requirements by assurance level;
- exact Wayland compositor and embedded web engine;
- local database implementation per product profile;
- central observability stack;
- key custody and threshold-signing topology;
- hardware sizing, energy, and thermal design;
- supported CPU architectures;
- regulatory retention and disclosure periods.

---

<!-- Source: 00-foundation/03-glossary.md -->

# Glossary

**Activation** — Atomic transition that makes a verified OS image, service bundle, policy bundle, or Runtime Pack active.

**Advisory reading** — A result produced by an explicit lens, such as domain-bounded competence weighting, that informs but does not silently replace the baseline reading.

**Annex** — External component integrated in an isolated, capability-limited, replaceable form.

**Authority channel** — Named source of recognition or validation authority with explicit scope and lineage.

**Capability envelope** — Set of functions a node may perform in a given state, including offline or degraded states.

**Decision receipt** — Machine-readable record of a policy or governance decision, including policy identity, subject, action, outcome, reason codes, and correlation data.

**Endpoint** — User-facing kOA node optimized for local continuity and constrained resources.

**Fail closed** — Refusal to grant authority, activate, publish, or execute when required verification cannot be completed.

**Governance Policy Bundle** — Signed, versioned collection of roles, rules, thresholds, disclosure constraints, rights, AI capabilities, escalation paths, and recourse procedures.

**Hermetic operation** — Operation within a closed or tightly controlled network without a required Internet dependency.

**Konnaxion** — Principal public and commons-oriented plane for discovery, education, collaboration, deliberation, culture, publication, and distribution.

**Kristal** — Framework and artifact family for portable, traceable, queryable, offline-usable epistemic state.

**Kristal Runtime Pack** — Derived, indexed, offline-executable artifact optimized for constrained deterministic queries.

**Last-known-good** — Most recent previously active artifact set that remains verified, compatible, and authorized for rollback.

**Mimic** — Reimplement a useful pattern natively rather than integrating an external platform whose architecture or governance would dominate the core.

**Node profile** — Declared set of roles, services, resources, trust assumptions, and offline guarantees for a kOA node.

**Orgo** — Principal private and operational plane for signals, Cases, Tasks, assignments, approvals, escalation, execution, closure, audit, and synchronization.

**Policy decision point** — Component that evaluates a declared request against versioned policy and returns an allow, deny, or review result.

**Publication Gateway** — Controlled boundary that moves approved non-sensitive outputs between private and public domains.

**Reader policy** — Explicit policy selecting which assertions, authority channels, scopes, certainty levels, and statuses are visible in a context.

**Recourse** — Defined procedure to challenge, review, correct, revoke, or supersede an output, decision, policy, or artifact.

**Release Set** — Signed compatibility manifest binding an OS image, service bundle, governance policy bundle, and supported Kristal contracts/channels.

**Safe degradation** — Reduced operation that preserves authorized context and local continuity while blocking unsafe authority or execution.

**Security domain** — Set of processes, identities, storage, keys, and policies separated from other domains.

**Sovereignty Bundle** — Complete portable tenant export containing data, policy, Kristal artifacts, receipts, trust handover material, and restore instructions.

**Structured Epistemic State** — Kristal representation of assertions, provenance, scope, uncertainty, validation, recognition, and related epistemic metadata.

**System of systems** — Architecture that coordinates independent components through explicit contracts without collapsing them into one inseparable platform.

**Trust root** — Pinned key, certificate, or equivalent anchor used to verify signatures and authority chains.

---

<!-- Source: 01-architecture/00-system-context.md -->

# System Context

## 1. Context statement

kOA Linux sits between maintained hardware/Linux mechanisms and the kOA product ecosystem. It provides an appliance-grade runtime rather than a new social application.

```text
People and institutions
        |
        v
koa-session-shell
  |             |
  v             v
Konnaxion      Orgo
       \       /
        v     v
     Kristal Runtime
           |
           v
kOA Governance and Node Runtime
           |
           v
Linux + hardware
```

## 2. External actors

- **participant**: learns, contributes, deliberates, votes, creates, or collaborates;
- **operator**: maintains node availability without owning civic meaning;
- **tenant administrator**: manages tenant policy within delegated authority;
- **reviewer/approver**: performs workflow decisions;
- **auditor**: inspects selected receipts and evidence;
- **authority channel**: validates or recognizes artifacts within a scope;
- **external system**: submits signals or consumes approved outputs;
- **release authority**: signs compatible release artifacts;
- **recovery custodian**: restores nodes and trust under a defined break-glass process.

## 3. Principal product relationships

### 3.1 Konnaxion

Konnaxion is the open/global plane. It consumes Kristal artifacts for search, navigation, education, civic workflows, curation, and offline access. It produces public contributions, deliberation outputs, and requests that may become Orgo work.

### 3.2 Orgo

Orgo is the private/organizational plane. It receives signals, creates Cases and Tasks, routes responsibility, executes approvals, manages sensitive workflows, and records operational outcomes. It orchestrates work around Kristal but does not own Kristal semantics.

### 3.3 Kristal

Kristal is the shared epistemic substrate. It carries portable state, provenance, validation, authority recognition, federation, reader-policy metadata, query contracts, and Runtime Packs.

### 3.4 Specialized engines

SenTient resolves ambiguity when resolution is required. Architect renders deterministic, traceable output from validated query results. Neither engine is required on every endpoint.

## 4. Context boundaries

The system MUST distinguish:

- local node state from federated state;
- tenant state from global content identity;
- operational workflow from epistemic payload;
- public disclosure from private evidence;
- advisory computation from binding decisions;
- governance authorization from Linux privilege;
- active artifacts from installed, cached, quarantined, revoked, or expired artifacts.

## 5. Trust assumptions

The architecture assumes that:

- networks fail and may be hostile;
- services become slow, unavailable, or compromised;
- administrators can make mistakes or abuse privilege;
- signing keys can be lost or revoked;
- governance rules can drift or be captured;
- AI can hallucinate, bias, or overreach;
- storage can corrupt;
- clocks can be wrong;
- federation peers may disagree legitimately.

No design may rely on the opposite assumptions for correctness.

---

<!-- Source: 01-architecture/01-logical-architecture.md -->

# Logical Architecture

## 1. Planes

```text
Experience Plane
├── koa-session-shell
├── Konnaxion workspace
└── Orgo workspace

Application Plane
├── Konnaxion Core
├── Orgo Core
├── Kristal Runtime Plane
└── Specialized adapters

Governance Plane
├── koa-policy-runtime
├── policy registry
├── decision receipts
├── recourse workflows
└── disclosure, rights, and AI policies

Node Plane
├── koa-node-agent
├── trust store
├── release manager
├── audit broker
├── export and recovery
└── local synchronization transport

Linux Mechanism Plane
├── systemd
├── SELinux or equivalent LSM
├── namespaces, cgroups, and seccomp
├── Podman and Quadlet
├── storage encryption and integrity
└── Wayland, graphics, audio, and input
```

## 2. Dependency rule

Dependencies point toward more stable contracts:

```text
UI → domain API → domain ports → adapters
                         ↓
                 policy decision API
                         ↓
                  node operation API
```

Konnaxion and Orgo MUST NOT:

- execute arbitrary root commands;
- modify the immutable system image;
- read signing private keys;
- activate a Runtime Pack by directly moving files;
- read or write the other domain's internal database;
- convert an advisory result into a privileged operation without workflow and policy evaluation.

## 3. Contract types

### 3.1 Synchronous contracts

Use only when an immediate response is required:

- local authentication;
- policy decision;
- Kristal query;
- node status;
- interactive user action.

Synchronous chains MUST have explicit timeout budgets, cancellation, bounded retries, and degraded behavior.

### 3.2 Asynchronous contracts

Prefer for:

- synchronization;
- builds;
- publication;
- distribution;
- telemetry;
- notifications;
- SenTient and Architect work;
- large export/import operations.

Messages MUST carry stable event identifiers and correlation identifiers. Consumers MUST be idempotent. Poison messages MUST enter a reviewable dead-letter flow.

### 3.3 Artifact contracts

Use for immutable, signed, or content-addressed objects:

- OS image;
- service bundle;
- policy bundle;
- Kristal artifacts;
- offline bundle;
- Sovereignty Bundle.

## 4. Consistency model

Internal product transactions use ACID where possible. When a transaction must emit an external event, the product MUST use a Transactional Outbox or an equivalent atomic handoff.

Long-running distributed workflows are durable state machines. A compensation may be declared only when it restores a valid business state. An incorrect publication, recognition, or signature normally requires revocation or a superseding release, not deletion of history.

## 5. Modularity

Konnaxion and Orgo SHOULD be modular monoliths or coherent service groups, not artificial microservice constellations. Internal modules MUST expose public interfaces and MUST NOT reach into each other's private persistence structures.

Independently deployable services are justified when one or more of the following apply:

- different technology stack;
- independent trust domain;
- materially different scaling profile;
- optional availability;
- heavy resource isolation;
- separate release authority.

Expected independent services include SenTient, Architect Build, Kristal Compiler, signing/authority services, distribution registries, and central observability.

## 6. Policy and enforcement sequence

```text
Request
  ↓
Authentication and context resolution
  ↓
koa-policy-runtime
  ↓ allow / deny / require-review + receipt
Workflow approval when required
  ↓
koa-node-agent allowlisted operation
  ↓
Linux mechanism
  ↓
operation receipt and audit event
```

The policy runtime never performs unrestricted node mutation. The node agent never invents policy.

---

<!-- Source: 01-architecture/02-physical-architecture.md -->

# Physical Architecture

## 1. Appliance layers

```text
┌──────────────────────────────────────────────────────────────┐
│                    User Experience                           │
│ koa-session-shell • Konnaxion • Orgo • Kristal Library      │
├──────────────────────────────────────────────────────────────┤
│                    Application Services                      │
│ Konnaxion Core • Orgo Core • Kristal Runtime • adapters     │
├──────────────────────────────────────────────────────────────┤
│                    Governance Services                       │
│ policy runtime • audit broker • publication gateway         │
├──────────────────────────────────────────────────────────────┤
│                    Node Services                             │
│ node agent • release manager • sync • export • recovery     │
├──────────────────────────────────────────────────────────────┤
│                    Container Boundary                        │
│ rootless Podman • Quadlet • namespaces • cgroups • seccomp  │
├──────────────────────────────────────────────────────────────┤
│                    Immutable Linux                           │
│ kernel • systemd • LSM • storage • networking • Wayland     │
├──────────────────────────────────────────────────────────────┤
│                    Hardware / Firmware                       │
└──────────────────────────────────────────────────────────────┘
```

## 2. Host operating system

The host SHOULD contain only components required to:

- boot and verify the image;
- unlock and mount approved storage;
- establish networking and local time;
- start node and governance services;
- launch the minimal graphical session;
- operate containers;
- perform update, rollback, export, and recovery.

Development tools, compilers, arbitrary package managers, and user-installed system daemons SHOULD be excluded from production endpoint images.

## 3. Container placement

Application services SHOULD run as rootless containers under dedicated system identities. The host MUST reserve privileged services for operations that cannot be safely delegated, such as measured identity, device management, encrypted-volume lifecycle, signed activation, and controlled recovery.

## 4. Data placement

- immutable binaries: image-managed `/usr` or equivalent;
- host policy and declared configuration: `/etc/koa`;
- durable service state: `/var/lib/koa/<domain>`;
- runtime state: `/run/koa`;
- signed installed artifacts: `/var/lib/koa/artifacts`;
- audit receipts: `/var/lib/koa/audit` with class-specific protection;
- removable/offline import staging: quarantined path not directly executable.

## 5. Graphical stack

The endpoint SHOULD use a maintained minimal Wayland compositor and a tested embedded web engine or browser runtime. GNOME is not part of the product shell. Standard Linux services may still be used when they provide maintained device, accessibility, media, or network functionality.

## 6. Hardware assurance profiles

### Baseline

- UEFI Secure Boot when supported;
- encrypted durable storage;
- signed OS and artifacts;
- recovery key procedure;
- no assumption of TPM availability.

### Enhanced

- TPM-backed node keys;
- measured boot evidence;
- sealed storage keys;
- remote or local attestation;
- tamper-evident audit anchoring.

### High assurance

- split key custody;
- hardware security module or threshold signing;
- dual-control recovery;
- physically protected build/signing nodes;
- controlled media transfer.

A node profile MUST declare which assurance level it implements.

---

<!-- Source: 01-architecture/03-node-profiles.md -->

# Node Profiles

## 1. Profile model

A node profile is a signed declaration of roles, services, minimum resources, trust assumptions, network exposure, and offline guarantees. A node MUST NOT silently enable a role not declared by its profile.

## 2. `koa-endpoint`

Purpose: user-facing local workstation or terminal.

Required capabilities:

- `koa-session-shell`;
- Konnaxion and Orgo workspaces appropriate to the tenant;
- Kristal verification, local pack store, constrained query runtime, and reader-policy evaluation;
- local identity and policy evaluation;
- local queues and resumable synchronization;
- safe import of signed offline bundles;
- last-known-good rollback and user-visible status;
- recovery environment.

Constraints:

- no mandatory cloud connection;
- no full Kristal compiler requirement;
- no mandatory SenTient, Architect Build, Solr, Elasticsearch, or large model runtime;
- low idle resource use;
- support for constrained and refurbished hardware profiles where validated.

## 3. `koa-sovereign-hub`

Purpose: local institutional or community infrastructure.

Typical capabilities:

- Konnaxion API and local web delivery;
- Orgo Core and workflow services;
- PostgreSQL and message broker;
- tenant identity and trust services;
- Kristal repository and distribution cache;
- publication gateway;
- local container registry;
- local backup and restore;
- LAN operation without Internet;
- controlled external federation.

The hub MUST preserve operation when upstream services are unavailable. Public and private interfaces MUST use separate network and disclosure policies.

## 4. `koa-build-farm`

Purpose: heavy deterministic and assisted build workloads.

Typical capabilities:

- Kristal Compiler;
- optional Claim-IR extraction;
- SenTient resolution;
- Architect Build;
- validation engines;
- large indexes and content-addressed caches;
- reproducibility workers;
- artifact assembly.

Private release signing SHOULD occur in a separate security domain. Build workers MUST NOT be trusted solely because they produced an artifact; outputs require independent verification.

## 5. `koa-control-plane`

Purpose: release, policy, registry, and fleet governance.

Typical capabilities:

- Release Set publication;
- service and artifact registries;
- policy registry;
- trust-root and revocation distribution;
- fleet inventory and health summaries;
- approval workflows;
- central audit aggregation where authorized.

The control plane MUST NOT be required for an endpoint's minimum offline capability.

## 6. Optional specialized profiles

Deployments MAY define:

- kiosk or classroom profile;
- mobile field node;
- air-gapped Orgo node;
- cultural archive node;
- public library node;
- disaster-response hub;
- high-assurance review station.

Every specialized profile MUST inherit the founding invariants and specify its deviations, limits, and test suite.

## 7. Role composition

Profiles MAY be combined on one physical machine only when the resulting trust and resource boundaries remain acceptable. Build/signing, public/private, and multi-tenant combinations require explicit threat-model review.

---

<!-- Source: 01-architecture/04-process-and-trust-boundaries.md -->

# Process and Trust Boundaries

## 1. Security domains

At minimum, the host defines separate domains for:

- graphical session shell;
- Konnaxion services;
- Orgo services;
- Kristal Runtime;
- governance policy runtime;
- audit broker;
- publication gateway;
- node agent;
- optional AI/specialized engines;
- update and recovery.

Each domain SHOULD have a dedicated Unix identity, container namespace, storage path, SELinux label or equivalent, resource limits, and network policy.

## 2. Privilege hierarchy

```text
Unprivileged UI
    ↓ local authenticated API
Domain service
    ↓ policy request
koa-policy-runtime
    ↓ signed/receipted decision
koa-node-agent
    ↓ fixed operation
Linux mechanism
```

No service may pass arbitrary shell fragments, filesystem paths, unit names, device names, or container arguments to the privileged broker unless the operation contract validates them against a closed schema and allowlist.

## 3. Konnaxion / Orgo boundary

Konnaxion MUST NOT read Orgo private data directly. Orgo MUST NOT publish into Konnaxion by direct database write. Exchange occurs through:

- authenticated domain API;
- asynchronous event contract;
- `koa-publication-gateway`;
- signed/exported artifact;
- approved synchronization contract.

## 4. Kristal boundary

Kristal content identity excludes tenant workflow state. Konnaxion and Orgo may reference Kristal identifiers, but MUST keep assignments, approvals, ACLs, distribution status, and operational audit outside the hashed epistemic payload.

## 5. AI boundary

AI processes run in a separate capability domain. They receive only data classes explicitly authorized by policy. Restricted cultural, personal, or operational data MUST NOT be mounted or transmitted merely because an application promises not to use it.

## 6. Signing boundary

Release signing keys MUST NOT be available to ordinary build workers, Konnaxion, Orgo, or the session shell. Signing requests MUST identify artifact hashes and policy context. High-assurance signing SHOULD require independent review or threshold approval.

## 7. Recovery boundary

Recovery uses a separate target and reduced service set. Recovery credentials and trust transitions MUST be logged and SHOULD require dual control for high-assurance deployments.

## 8. Resource boundaries

CPU, memory, process count, storage, I/O, and network egress MUST be bounded per service. Heavy optional engines MUST NOT be able to starve policy evaluation, local identity, active Kristal access, Orgo critical workflows, or recovery.

---

<!-- Source: 01-architecture/05-storage-and-filesystem-layout.md -->

# Storage and Filesystem Layout

## 1. Design goals

Storage must support immutable releases, tenant isolation, offline operation, atomic activation, rollback, encrypted sensitive state, export, and forensic reconstruction.

## 2. Recommended layout

```text
/usr/                         immutable OS content
/etc/koa/                     host configuration and pinned policy
/run/koa/                     ephemeral sockets, locks, and runtime state
/var/lib/koa/
├── node/                     node identity and local state
├── releases/                 Release Sets and activation records
├── policies/                 installed Governance Policy Bundles
├── kristal/
│   └── <tenant>/<env>/<channel>/
│       ├── packs/<runtime_pack_id>/
│       ├── active -> packs/<runtime_pack_id>
│       └── state.json
├── konnaxion/<tenant>/       Konnaxion state
├── orgo/<tenant>/            Orgo state
├── publication/<tenant>/     staged and published disclosure bundles
├── audit/                    class-separated receipts and evidence
├── exports/                  generated Sovereignty Bundles
├── quarantine/               untrusted imports
└── backups/                  local encrypted backup staging
```

## 3. Immutability classes

### Image immutable

OS content is replaced only by signed image activation.

### Artifact immutable

Release artifacts and Kristal artifacts are addressed by identity and never modified in place. New content produces a new identity or version.

### Append-oriented

Receipts, activation history, revocations, and critical audit events append new records. Correction produces a superseding record.

### Mutable operational state

Cases, Tasks, sessions, caches, and work queues remain mutable under product transaction rules.

## 4. Encryption

Sensitive Orgo, identity, audit, rights, and export data MUST be encrypted at rest. Keys SHOULD be scoped by tenant and purpose. A storage snapshot MUST NOT implicitly become an authorized plaintext export.

## 5. Runtime Pack cache policy

Each channel MUST define:

- maximum disk allocation;
- active pack;
- last-known-good pack;
- pinned packs;
- highest activated release identity;
- downgrade policy;
- eviction order;
- stale and expiry handling.

The active and last-known-good packs MUST survive ordinary garbage collection.

## 6. Quarantine

Removable media and offline bundles enter quarantine. The system MUST verify media policy, manifest, signature, hashes, compatibility, audience, and revocation state before moving content into an installed store.

## 7. Backup semantics

Backups MUST identify:

- product and schema versions;
- tenant and data class;
- encryption and key dependency;
- snapshot consistency point;
- included and excluded artifacts;
- restore prerequisites;
- retention and deletion policy.

## 8. Deletion and withdrawal

Content-addressed identity does not eliminate legal or governance deletion duties. The system MUST support revocation, removal from authorized distribution, cache purge, cryptographic erasure where applicable, and retention of minimal non-sensitive proof that a governed transition occurred.

---

<!-- Source: 01-architecture/06-network-topology.md -->

# Network Topology

## 1. Network zones

```text
User Session Zone
        |
Application Gateway
   |             |
Public Zone    Private Zone
Konnaxion      Orgo
   |             |
Publication Gateway
        |
Kristal Distribution / Federation Zone
        |
External Networks
```

## 2. Default-deny principle

Inbound and outbound communication MUST be denied unless declared by service profile. Internal location does not imply trust. Every cross-domain request requires authenticated identity, tenant context, action scope, and correlation data.

## 3. Public zone

Konnaxion-facing services MAY expose controlled HTTP endpoints. Public services MUST NOT share an addressable database or unrestricted filesystem with Orgo.

## 4. Private zone

Orgo SHOULD have no public inbound endpoint by default. Remote access requires tenant policy, strong authentication, rate limits, and audit. Hermetic mode MUST remain supported where declared.

## 5. Node-local APIs

Privileged and policy APIs SHOULD use Unix domain sockets with peer credential verification. TCP loopback is permitted only when mutual authentication and equivalent confinement are demonstrated.

## 6. Federation

Federation peers are explicitly configured. Trust is scoped by tenant, environment, channel, authority, and artifact type. A valid signature from another trust domain MUST NOT be accepted automatically.

## 7. Offline and intermittent links

Synchronization MUST be resumable, idempotent, bandwidth-aware, and manifest-first. Transfer priority SHOULD be:

1. revocations and trust-root updates;
2. security and governance policies;
3. critical Orgo operational state;
4. Kristal manifests and indexes;
5. essential content;
6. large media;
7. optional caches.

## 8. Resilience controls

Remote calls MUST use timeout budgets, exponential backoff with jitter, circuit breakers, rate limits, and bulkheads where failure could cascade. Reconnection MUST NOT create a retry storm.

## 9. Name and time dependencies

Local correctness MUST NOT depend on public DNS or online time sources during offline operation. The node SHOULD cache necessary name data and record clock uncertainty. Expiry decisions affected by uncertain time MUST fail safely and visibly.

---

<!-- Source: 01-architecture/07-boot-session-and-recovery.md -->

# Boot, Session, and Recovery

## 1. Boot sequence

```text
Firmware / Secure Boot
        ↓
Signed bootloader and kernel
        ↓
Immutable OS image
        ↓
Storage unlock and integrity checks
        ↓
koa-node.target
        ↓
policy runtime, audit broker, node agent
        ↓
koa-services.target
        ↓
Konnaxion, Orgo, Kristal Runtime
        ↓
koa-graphical.target
        ↓
koa-session-shell
```

A failed optional application service MUST NOT prevent recovery access. A failed trust or policy foundation MUST prevent sensitive activation and expose an actionable diagnostic state.

## 2. Session startup

The shell authenticates the user, resolves tenant and role context, displays node and synchronization status, and offers Konnaxion and Orgo as principal workspaces. It MUST NOT grant direct shell or root access as part of ordinary use.

## 3. Watchdog and health

Critical node services SHOULD use systemd watchdogs or equivalent supervision. Readiness MUST distinguish process existence from ability to satisfy the service's critical contract.

## 4. Recovery entry

Recovery MAY be entered through:

- automatic boot fallback after repeated failure;
- signed operator request;
- physical recovery gesture;
- verified removable media;
- remote management only under a declared high-assurance policy.

## 5. Recovery capabilities

Recovery SHOULD provide:

- booted image and Release Set inspection;
- previous image rollback;
- policy and Runtime Pack rollback;
- storage and filesystem diagnostics;
- trusted time and trust-root repair;
- encrypted backup restore;
- Sovereignty Bundle import;
- audit export;
- factory reset with explicit data handling.

Recovery MUST NOT silently erase tenant data or replace trust roots.

## 6. Break-glass operations

Break-glass operations MUST:

- be narrowly defined;
- require stronger authentication than ordinary administration;
- state duration and scope;
- emit a tamper-evident receipt;
- trigger review;
- expire automatically where possible.

## 7. Boot success criteria

A new OS image is considered successful only after required node, policy, storage, Kristal, and session checks pass within a bounded interval. Otherwise the system SHOULD return to the last-known-good image.

---

<!-- Source: 02-components/00-koa-session-shell.md -->

# Component — `koa-session-shell`

## 1. Purpose

`koa-session-shell` is the minimal native product shell for a kOA endpoint. It owns session lifecycle and workspace composition; it is not Konnaxion itself and it does not implement Orgo business logic.

## 2. Responsibilities

The shell MUST provide:

- user authentication handoff and session lock;
- tenant and workspace selection;
- principal entry points to Konnaxion and Orgo;
- global notifications and search entry points;
- local, offline, synchronization, and trust status;
- safe import/export entry points;
- accessibility and localization integration;
- recovery and support entry points when policy permits;
- an explicit indication when the node is degraded, stale, or running a fallback release.

## 3. Non-responsibilities

The shell MUST NOT:

- execute arbitrary system commands;
- own product domain data;
- interpret Kristal semantics independently;
- store signing keys;
- silently switch tenants;
- make governance decisions;
- hide verification or synchronization failures.

## 4. Process model

The shell SHOULD run as an unprivileged system or user service under a dedicated identity. It communicates through authenticated local APIs:

```text
koa-session-shell
├── Konnaxion local gateway
├── Orgo local gateway
├── Kristal query/status API
├── policy decision API
└── node status/operation API
```

The shell receives no direct write access to `/var/lib/koa` product stores.

## 5. Workspace model

```text
Home
├── Konnaxion
├── Orgo
├── Kristal Library
├── Global Search
├── Notifications
├── Sync and Node Status
└── Session and Accessibility
```

Deployments MAY visually emphasize one workspace, but both principal planes remain addressable when installed and authorized.

## 6. Failure behavior

- Konnaxion unavailable: Orgo, Kristal Library, and node status remain available when healthy.
- Orgo unavailable: Konnaxion and approved public knowledge remain available.
- network unavailable: local capability envelope remains accessible.
- policy runtime unavailable: read-only safe surfaces MAY remain, but sensitive operations are denied.
- active Runtime Pack invalid: affected knowledge views are blocked or labeled according to capability policy.

## 7. Security requirements

The shell MUST use origin and navigation restrictions for embedded web content. External links MUST open through an explicit policy-controlled handoff. File pickers MUST stage imported content into quarantine rather than exposing arbitrary host paths.

## 8. Conformance evidence

A shell implementation MUST demonstrate:

- no root or unrestricted D-Bus dependency;
- correct tenant separation;
- visible degraded-state indicators;
- functional offline session startup;
- workspace isolation after one workspace crashes;
- keyboard, screen-reader, and locale support for declared profiles.

---

<!-- Source: 02-components/01-koa-node-agent.md -->

# Component — `koa-node-agent`

## 1. Purpose

`koa-node-agent` is the sole narrow privileged broker for normal kOA node management. It exposes fixed high-level operations rather than a command execution interface.

## 2. Allowed operation classes

A baseline agent MAY implement:

- inspect node identity and booted release;
- stage and activate a verified OS image;
- activate or roll back a declared service bundle;
- activate or roll back a Governance Policy Bundle;
- install, activate, pin, unpin, or quarantine a Kristal Runtime Pack;
- manage declared encrypted volumes;
- import a verified offline bundle;
- export approved node evidence;
- enter recovery target;
- restart an allowlisted service group;
- rotate a node-scoped key through a governed workflow.

Every operation MUST have a closed schema, preconditions, authorization class, idempotency behavior, timeout, result schema, and stable error codes.

## 3. Prohibited interface

The agent MUST NOT expose:

- arbitrary shell execution;
- arbitrary systemd unit control;
- arbitrary file copy or path traversal;
- arbitrary container image or argument execution;
- generic package-manager access;
- unrestricted device access;
- raw private-key export.

## 4. Request contract

A request contains at least:

```json
{
  "operation": "activate_runtime_pack",
  "request_id": "uuid",
  "tenant_id": "tenant:example",
  "policy_decision_id": "decision:...",
  "artifact_id": "sha256:...",
  "expected_active_id": "sha256:...",
  "parameters": {},
  "correlation_id": "corr:..."
}
```

The agent verifies caller identity, decision binding, decision expiry, artifact identity, current state, operation allowlist, and replay/idempotency state.

## 5. Atomicity

Activation MUST use an atomic pointer, boot slot, transaction, or equivalent mechanism. A crash MUST leave either the previous valid state or the complete new state active—never a partially activated state.

## 6. Idempotency

Repeated requests with the same request identity and equivalent body MUST return the recorded result. Reuse with a different body MUST fail.

## 7. Audit

The agent emits an operation receipt containing:

- request and policy decision identities;
- authenticated caller;
- before and after state;
- artifact hashes;
- result and reason codes;
- duration;
- recovery or rollback token when applicable.

## 8. Hardening

The service SHOULD use systemd sandboxing, a dedicated SELinux domain, minimal Linux capabilities, `NoNewPrivileges`, protected system paths, private temporary storage, restricted address families, bounded resources, and a local Unix socket.

## 9. Emergency path

Break-glass actions use separate operation names and stronger policy. The agent MUST NOT infer emergency authorization from caller UID alone.

---

<!-- Source: 02-components/02-koa-policy-runtime.md -->

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

---

<!-- Source: 02-components/03-konnaxion.md -->

# Principal Domain — Konnaxion

## 1. Role

Konnaxion is the principal public and commons-oriented plane of kOA. It provides discovery, education, collaboration, deliberation, cultural exchange, public knowledge surfaces, collective curation, and distribution.

## 2. Architecture

The existing product stack is a modular web platform. The target kOA Linux architecture preserves Konnaxion's own global application layout and route/module structure while hosting it inside the wider `koa-session-shell`.

Konnaxion SHOULD remain a modular monolith or coherent application group with explicit module APIs. It MUST NOT be split into network services merely to satisfy an architectural fashion.

## 3. Kristal responsibilities

Konnaxion owns the user-facing functions for:

- browsing and searching Runtime Packs;
- selecting and explaining reader policies;
- showing validation, certainty, authority, and disagreement labels;
- offline delivery and cache status;
- requesting pack installation/activation;
- displaying stale, provisional, contested, expired, or revoked states;
- collecting non-mutating feedback signals;
- distributing approved public artifacts.

Konnaxion does not own Kristal content identity or validation semantics.

## 4. Relationship with Orgo

Konnaxion sends structured signals, submissions, public decisions, requests, and feedback to Orgo through contracts. It receives approved non-sensitive publications and execution summaries through the Publication Gateway.

Konnaxion MUST NOT access Orgo's private persistence directly.

## 5. SmartVote and EkoH

Where SmartVote is used, Konnaxion MUST preserve explicit readings rather than compressing all authority into one hidden score. At minimum, the baseline and advisory weighted results remain distinguishable. Weighting rules are versioned, domain-bounded, explainable, and contestable.

SmartVote MUST NOT map directly to Linux roles, root privilege, signing authority, or node activation.

## 6. Offline behavior

When offline, Konnaxion MUST:

- serve active verified local content;
- display synchronization age and trust status;
- queue idempotent permitted actions;
- avoid activating artifacts that require unavailable trust material;
- continue local navigation and search within the declared capability envelope;
- preserve user work for later synchronization.

## 7. Security

Konnaxion runs in the public security domain. It uses separate credentials, storage, network, and caches from Orgo. Public input is untrusted and MUST pass validation, rate limiting, content controls, and workflow gates before it can influence trusted artifacts or operations.

## 8. Observability

Konnaxion emits operational metrics and receipts, not raw private knowledge by default. Feedback about pack use or errors creates Orgo work or distribution adjustments; it MUST NOT mutate Kristal Exchange directly.

---

<!-- Source: 02-components/04-orgo.md -->

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

---

<!-- Source: 02-components/05-kristal-runtime-plane.md -->

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

---

<!-- Source: 02-components/06-publication-gateway.md -->

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

---

<!-- Source: 02-components/07-audit-broker.md -->

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

---

<!-- Source: 02-components/08-identity-and-trust.md -->

# Identity and Trust

## 1. Identity layers

kOA distinguishes:

- human identity;
- pseudonymous participation identity;
- organization and tenant identity;
- role and delegation identity;
- node identity;
- service workload identity;
- publisher and signer identity;
- authority-channel identity;
- artifact content identity.

These identities MUST NOT be collapsed into one universal identifier.

## 2. Authentication

Local authentication MUST remain possible for declared offline use. Deployments MAY federate identity online, but MUST define cached credential, expiry, revocation, and emergency behavior.

High-impact operations SHOULD require phishing-resistant factors or hardware-backed credentials.

## 3. Authorization

Authorization combines authenticated attributes, tenant, action, resource, policy version, workflow state, and node context. Unix group membership alone is insufficient for governance authorization.

## 4. Node identity

A node has a stable public identity and rotatable keys. TPM-backed keys SHOULD be used for enhanced assurance. Node replacement and key loss require a governed re-enrollment workflow.

## 5. Trust roots

Trust roots are scoped by:

- tenant;
- environment;
- release channel;
- artifact type;
- authority domain.

A signature valid under another tenant or environment MUST NOT be accepted automatically.

## 6. Key separation

Separate keys SHOULD exist for:

- OS release signing;
- service release signing;
- policy bundle signing;
- Kristal publishing;
- authority recognition;
- node identity;
- audit anchoring;
- export encryption.

## 7. Revocation

Revocation information MUST be distributable offline in signed, versioned form. Nodes record the newest accepted revocation epoch and apply downgrade protection.

## 8. Delegation and recourse

Role delegation is explicit, scoped, time-bounded, and revocable. Decisions retain the identity of both delegator and acting subject where appropriate. Identity challenges and corrections use a defined recourse workflow rather than silent operator edits.

---

<!-- Source: 03-lifecycle/00-release-model.md -->

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

---

<!-- Source: 03-lifecycle/01-os-updates.md -->

# Operating-System Updates

## 1. Image model

The OS is built as an immutable signed image. The reference implementation SHOULD use bootc/OSTree or an equivalent maintained image mechanism with atomic deployment and rollback.

## 2. Build pipeline

```text
source and lockfiles
  → reproducible image build
  → SBOM and provenance
  → security and integration tests
  → image signature
  → Release Set binding
  → registry/offline publication
```

## 3. Staging

A node stages an image without changing the active boot. It verifies:

- signature and trust scope;
- image digest;
- Release Set compatibility;
- hardware and node profile;
- required storage space;
- required migration prerequisites;
- revocation and downgrade state.

## 4. Activation

Activation is requested through policy and performed by `koa-node-agent`. The node records the expected new boot identity and previous known-good deployment.

## 5. Boot health

A new image is accepted only after required services, storage, policy runtime, active artifacts, and graphical/session checks pass. Failure causes automatic or operator-approved rollback according to profile.

## 6. Offline update

An offline OS bundle contains the image, signatures, Release Set, revocation information, compatibility metadata, and import instructions. The node MUST NOT trust removable media merely because it is physically present.

## 7. Emergency security update

Emergency update policy MAY shorten ordinary approval, but MUST preserve signature, compatibility, receipt, rollback, and post-event review. Emergency authority expires automatically.

## 8. Drift control

Production nodes MUST report or locally expose whether the running image matches a signed release identity. Undocumented local mutation is a conformance failure.

---

<!-- Source: 03-lifecycle/02-service-updates.md -->

# Service Updates

## 1. Packaging

Services are distributed as signed OCI images referenced by digest. Tags are convenience pointers and MUST NOT be the sole activation identity.

## 2. Service Bundle

A Service Bundle manifest declares:

- image digests;
- Quadlet/unit versions;
- configuration schema versions;
- required secrets by reference, not value;
- database migration set;
- network and storage requirements;
- health checks;
- resource limits;
- compatible OS and policy versions.

## 3. Rootless execution

Application containers SHOULD run rootless under dedicated service identities. Images SHOULD be read-only, use explicit writable volumes, drop capabilities, and have bounded resources.

## 4. Deployment strategies

- **recreate**: acceptable for non-critical or local services with bounded downtime;
- **blue/green**: preferred when parallel validation is possible;
- **canary**: allowed only with observability and rollback thresholds;
- **rolling**: allowed on multi-node hubs when schema compatibility is proven.

## 5. Health and acceptance

A running process is not sufficient. Acceptance checks include domain API readiness, dependency health, policy connectivity, database compatibility, and representative contract tests.

## 6. Rollback

Rollback MUST account for data migrations and emitted events. If a schema or event cannot be reversed safely, the release MUST use forward repair or a superseding service bundle rather than pretending rollback is complete.

## 7. Supply-chain controls

Images SHOULD be minimal, pinned, scanned, SBOM-producing, provenance-attested, and rebuilt regularly from maintained bases. Runtime installation of packages is prohibited in production images.

---

<!-- Source: 03-lifecycle/03-governance-policy-bundles.md -->

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

---

<!-- Source: 03-lifecycle/04-kristal-artifacts.md -->

# Kristal Artifact Lifecycle

## 1. General lifecycle

```text
source/input
  → Structured Epistemic State
  → optional Claim-IR and SenTient resolution
  → Working Exchange
  → review and validation decisions
  → authority recognition
  → Reference Exchange
  → Runtime Pack
  → distribution and activation
  → feedback, revision, supersession, or revocation
```

Compilation, validation, recognition, and distribution are distinct. A working artifact may exist without being a recognized reference, and reader policy determines what is visible in a context.

## 2. Build identity

Every build records:

- input artifact identities;
- schemas and contract versions;
- compiler and toolchain identity;
- policy selections;
- deterministic mode and resource limits;
- output identities;
- warnings and unresolved states.

## 3. Publication

Publication does not mutate an artifact. It associates immutable artifact identity with channel, audience, authority, and status metadata.

## 4. Runtime Pack compilation

A Runtime Pack is derived from declared source artifacts and policies. It MUST include a manifest, query contract, file inventory, source lineage, compatibility requirements, and status metadata.

## 5. Activation

Konnaxion owns the product-facing request and status experience. `koa-policy-runtime` evaluates activation policy. `koa-node-agent` performs the atomic filesystem/state transition. The Kristal Runtime verifies and serves the active pack.

## 6. Revocation and supersession

Revocation and supersession are signed records. Offline nodes apply the newest trusted revocation epoch they possess and display staleness when freshness cannot be established.

## 7. Tenant independence

Tenant IDs, ACLs, approvals, assignments, and distribution status MUST NOT alter core Kristal content identity. Tenants may sign, recognize, or distribute the same content differently.

## 8. Conformance

Implementations MUST test signature failure, hash mismatch, incompatible query contract, substitution attack, downgrade attack, atomic activation, offline serving, cache pinning, and rollback authorization.

---

<!-- Source: 03-lifecycle/05-offline-bundles.md -->

# Offline Bundles

## 1. Purpose

Offline Bundles carry releases, policies, trust updates, Kristal artifacts, synchronization payloads, or recovery material across disconnected boundaries.

## 2. Bundle classes

- OS update bundle;
- service update bundle;
- Governance Policy Bundle package;
- Kristal distribution bundle;
- revocation/trust update bundle;
- synchronization bundle;
- Sovereignty Bundle;
- recovery bundle.

## 3. Required envelope

Every bundle declares:

- bundle class and version;
- issuer and intended audience;
- tenant, environment, and channel scope;
- creation and expiry information with clock assumptions;
- payload inventory and hashes;
- dependencies and compatibility;
- confidentiality/encryption metadata;
- replay and sequence protection;
- signatures.

## 4. Import sequence

```text
media detection
  → copy to quarantine
  → parse bounded manifest
  → verify signature and trust scope
  → verify inventory and size limits
  → scan/validate payload by class
  → check replay, expiry, revocation, compatibility
  → policy decision
  → stage
  → explicit activation or synchronization
```

## 5. Media threats

The importer MUST defend against path traversal, symlink escape, decompression bombs, oversized manifests, parser ambiguity, duplicate names, device spoofing, stale signed content, and malicious optional metadata.

## 6. Confidential bundles

Sensitive bundles SHOULD be encrypted to tenant or node recipients. Signature verification and decryption errors fail closed. Decrypted material is not left in shared temporary paths.

## 7. Receipts

Import and activation are separate receipted events. A valid bundle may be installed but not authorized for activation.

---

<!-- Source: 03-lifecycle/06-rollback-and-recovery.md -->

# Rollback and Recovery

## 1. Rollback classes

- OS deployment rollback;
- service bundle rollback;
- Governance Policy Bundle rollback;
- Runtime Pack rollback;
- configuration rollback;
- data restore;
- trust-root recovery.

Each class has different safety semantics. A common button MUST NOT hide those differences.

## 2. Triggers

Rollback MAY be triggered by:

- explicit authorized operator action;
- failed health acceptance;
- verified revocation;
- repeated runtime errors crossing a declared threshold;
- failed migration checkpoint;
- incident-response workflow.

The same verified trigger sequence and state SHOULD produce the same rollback decision.

## 3. Authorization

Rollback is governed. Downgrading below security or revocation floors requires a separate emergency policy, stronger approval, and visible risk receipt.

## 4. Known-good retention

Nodes retain at least:

- active state;
- previous known-good state;
- recovery environment;
- required manifests and signatures;
- migration and rollback metadata.

## 5. Data recovery

Restore uses a clean compatibility check, not blind file replacement. The system verifies tenant, schema, artifact, encryption, and trust dependencies before committing restored state.

## 6. Trust recovery

Trust-root replacement is one of the highest-impact operations. It SHOULD require dual control, physical or out-of-band evidence, a continuity statement, and post-event audit.

## 7. Recovery test

Every supported node profile MUST have an automated or rehearsed test proving that a failed update, corrupted active pack, unavailable network, and lost application service can reach a safe recoverable state.

---

<!-- Source: 03-lifecycle/07-data-migrations.md -->

# Data Migrations

## 1. Principles

Migrations are versioned release artifacts. They MUST be observable, restartable or safely resumable, and bound to compatible service versions.

## 2. Migration classes

- additive schema change;
- backfill;
- index build;
- contract transition;
- data classification change;
- encryption/key migration;
- tenant split/merge;
- export/import format migration.

## 3. Expand/contract

Online services SHOULD use:

1. expand schema;
2. deploy code compatible with old and new forms;
3. backfill with checkpoints;
4. switch reads/writes;
5. verify;
6. contract only after rollback window closes.

## 4. Irreversible changes

An irreversible migration MUST be declared as such. It requires a tested backup/restore path, explicit approval, and a forward-repair plan. It MUST NOT be described as safely rollbackable.

## 5. Offline nodes

Offline nodes may skip multiple versions. Migrations MUST declare supported upgrade paths and reject unsupported jumps with a stable diagnostic.

## 6. Tenant safety

Migration progress, failure, and locks are tenant-aware. Failure for one tenant MUST NOT corrupt another tenant or silently expose cross-tenant data.

## 7. Epistemic versus operational migration

Operational schema migrations do not rewrite Kristal content identity. Kristal contract changes create new declared artifacts or projections with lineage.

---

<!-- Source: 04-security/00-threat-model.md -->

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

---

<!-- Source: 04-security/01-security-baseline.md -->

# Security Baseline

## 1. Host baseline

- maintained standard kernel and firmware;
- Secure Boot where supported;
- immutable signed OS image;
- full-disk or volume encryption for durable sensitive state;
- SELinux enforcing or equivalent mandatory access control;
- minimal installed packages;
- automatic security update workflow with rollback;
- restricted local console and recovery;
- accurate inventory of active release identities.

## 2. Service baseline

- dedicated service identities;
- rootless containers where feasible;
- no privileged containers;
- read-only root filesystem;
- dropped Linux capabilities;
- `NoNewPrivileges`;
- seccomp and LSM confinement;
- explicit writable mounts;
- resource quotas;
- default-deny network;
- structured logs and health checks;
- secrets by reference, never embedded in images.

## 3. Application baseline

- strong session management;
- tenant context on every request;
- authorization at service boundaries;
- CSRF, XSS, SSRF, injection, and upload protections;
- idempotency for retryable writes;
- rate limiting and abuse controls;
- bounded parsers and payload size;
- safe error messages that do not reveal cross-tenant existence;
- security headers and origin restrictions.

## 4. Privileged operation baseline

- allowlisted node-agent operations;
- policy decision binding;
- replay protection;
- before/after state verification;
- operation timeout and cancellation;
- decision and operation receipts;
- dual control for trust roots, release signing, and destructive recovery at high assurance.

## 5. Development baseline

- code review and protected branches;
- dependency lockfiles;
- secret scanning;
- SAST and dependency vulnerability scanning;
- container and IaC scanning;
- reproducible builds where feasible;
- signed commits/tags for release inputs;
- threat-model review for new trust boundaries;
- conformance tests in CI.

## 6. Vulnerability response

Every component has an owner, supported versions, update path, and severity process. A vulnerability that invalidates trust or artifact safety may trigger revocation, emergency policy, or channel freeze.

---

<!-- Source: 04-security/02-privacy-and-disclosure.md -->

# Privacy and Disclosure

## 1. Principle

kOA must be auditable without becoming a panopticon. Transparency applies to decisive mediation and institutional action; privacy protects people, vulnerable groups, and restricted evidence.

## 2. Data classes

A baseline classification includes:

- public;
- community-visible;
- tenant-internal;
- restricted;
- highly sensitive;
- legal/regulated;
- cultural-restricted;
- secret/key material.

Unknown classification defaults to restricted handling.

## 3. Disclosure decision

Disclosure policy considers:

- subject and role;
- tenant and purpose;
- object classification;
- consent and rights;
- workflow state;
- audience;
- jurisdiction and retention;
- minimum necessary fields;
- redaction obligations;
- whether aggregate or cryptographic proof can replace raw data.

## 4. Selective transparency

Public accountability SHOULD expose:

- rule and policy identity;
- process stage;
- aggregate or pseudonymous participation;
- decision outcome and rationale references;
- artifact hashes and validation status;
- dissent or unresolved state when publishable.

It SHOULD NOT expose protected identities, testimony, medical data, security details, or cultural restrictions without authority.

## 5. Access logging

Reading restricted evidence is an auditable action. Access logs are themselves protected and retained according to policy.

## 6. Redaction and derivation

Published redactions and summaries MUST identify their source, transformation, policy, and reviewer. Derived public data MUST be reviewed for re-identification risk.

## 7. Data subject and community rights

The system SHOULD support access, correction, restriction, objection, withdrawal, and deletion/erasure workflows as applicable. Community authority may add collective consent or protocol requirements beyond individual consent.

---

<!-- Source: 04-security/03-secrets-and-keys.md -->

# Secrets and Keys

## 1. Key classes

- OS release signing;
- service bundle signing;
- Governance Policy Bundle signing;
- Kristal publisher signing;
- authority recognition signing;
- node identity;
- workload identity;
- audit anchoring;
- tenant data encryption;
- offline/export encryption;
- recovery.

Keys of different classes MUST NOT be reused merely for convenience.

## 2. Custody

Private release and authority keys SHOULD be held outside application nodes, preferably in an HSM, hardware token, or threshold-signing system. Build workers produce hashes and attestations, not unrestricted signing authority.

## 3. Node secrets

Node secrets SHOULD be hardware-bound where available. Services receive only the secrets required for their purpose, through protected files, credentials APIs, or secret stores—not environment variables exposed broadly.

## 4. Rotation

Every key class has issuance, activation, overlap, rotation, revocation, compromise, archival, and destruction procedures. Verification supports declared overlap without accepting indefinite old keys.

## 5. Backup and recovery

Key backup is encrypted, access-controlled, tested, and separated from ordinary data backup. Recovery of a key does not automatically authorize its continued use; policy may require reissuance.

## 6. Compromise

A suspected signing-key compromise triggers channel freeze, revocation publication, artifact review, replacement trust material, and incident receipts. Offline distribution of revocation is part of the response plan.

## 7. Secrets in logs and exports

Secrets, raw tokens, private keys, and unredacted credentials MUST NOT enter logs, audit receipts, crash reports, or Sovereignty Bundles unless the bundle explicitly uses a protected key-handover profile.

---

<!-- Source: 04-security/04-ai-boundaries.md -->

# AI Boundaries

## 1. Principle

AI assists under governance. It is never the invisible sovereign of the system.

## 2. Permitted roles

Policy MAY allow AI to:

- propose metadata;
- extract schema-constrained candidates;
- summarize with source references;
- translate with traceability;
- detect duplicates or conflicts;
- suggest routing or dependencies;
- generate review candidates;
- assist accessibility descriptions;
- optimize non-authoritative workflows.

## 3. Prohibited roles

AI MUST NOT by itself:

- grant Linux or application privilege;
- activate releases or Runtime Packs;
- determine final cultural authority, consent, or rights;
- erase disagreement or uncertainty;
- publish binding validation or recognition;
- silently rank civic value;
- replace required human/community approval;
- become the only path to core correctness or recovery.

## 4. Capability enforcement

AI services receive explicit capabilities for data classes, tools, network destinations, models, retention, and output uses. Enforcement occurs at mount, network, API, and publication boundaries—not only in prompts.

## 5. Provenance

AI-assisted outputs MUST record model/tool identity where known, prompt or task contract as permitted, inputs or hashes, output, uncertainty/warnings, reviewer, and final disposition.

## 6. Deterministic gates

Schema validation, signature checks, policy evaluation, activation, authorization, and release acceptance remain deterministic. AI output may feed those gates only as untrusted candidate input.

## 7. Local and remote models

Remote model use requires disclosure and data-transfer policy. Restricted data MUST NOT leave the node or tenant unless explicitly authorized. Local models remain untrusted code and run in a constrained domain.

## 8. Failure behavior

AI unavailability reduces assistance but MUST NOT remove minimum local capability. Suspected hallucination or model compromise triggers review, quarantine of affected outputs, and possible model capability revocation.

---

<!-- Source: 04-security/05-integration-without-contamination.md -->

# Integration Without Contamination

## 1. Classification

Every external capability is classified as:

- **native** — implemented and governed within the core;
- **annexed** — isolated local component with a declared capability manifest;
- **connected** — external API/system behind an anti-corruption layer;
- **mimicked** — useful interaction pattern reimplemented natively;
- **forbidden** — incompatible with safety, governance, rights, or trust requirements.

## 2. Annex requirements

An annexed component MUST have:

- dedicated identity and storage;
- default-deny network;
- no direct database access to core domains;
- no signing keys;
- declared data classes;
- declared offline and failure behavior;
- explicit update owner;
- bounded resources;
- removable operation without core collapse;
- audit and health integration.

## 3. Connected systems

Connections use an Anti-Corruption Layer that maps external identifiers, states, and errors into kOA contracts. External semantics MUST NOT leak directly into core domain models without review.

## 4. Mimic decision

Mimic rather than annex when the external platform is opaque, structurally dominant, incompatible with offline or tenant boundaries, or would create a second source of governance truth.

## 5. Failure isolation

An optional integration failure MUST degrade its own capability, not prevent local identity, policy evaluation, critical Orgo work, active Kristal consultation, or recovery.

## 6. Manifest

Each integration has a signed manifest declaring mode, owner, version, network, filesystems, data classes, capabilities, dependencies, trust, health, and removal procedure.

## 7. Exit

Core data and governance state MUST remain exportable without the integrated tool. No integration may become an undocumented mandatory intermediary.

---

<!-- Source: 04-security/06-cultural-rights-and-consent.md -->

# Cultural Rights, Consent, and Community Authority

## 1. Principle

Cultural sovereignty cannot be protected by storage alone. Context, provenance, authority, consent, rights, access, reuse, AI restrictions, withdrawal, and decision pathways must be enforceable.

## 2. Rights object

A cultural object or collection may declare:

- creator and rights holder;
- community or collective authority;
- cultural context and protocol;
- access audience;
- display, download, reproduction, and reuse rights;
- licensing conditions;
- AI training and inference restrictions;
- attribution obligations;
- embargo or review date;
- withdrawal sensitivity;
- dispute and dissent status;
- applicable jurisdiction and stewardship.

## 3. Enforcement points

Rights policy MUST be checked at:

- ingestion;
- metadata editing;
- search/discovery;
- read/query;
- render;
- download;
- publication;
- synchronization;
- backup/export;
- AI access;
- federation;
- withdrawal and purge.

## 4. Audience-specific artifacts

Restricted data SHOULD NOT be placed into a universal Runtime Pack and hidden only by UI. Build separate audience-scoped packs or encrypted shards when needed:

- public;
- community;
- research;
- institution;
- exhibition;
- preservation.

## 5. Authority and consent

Authority may be individual, collective, institutional, Indigenous, or multi-party. Policy MUST represent disagreement and missing consent. Lack of a denial is not consent.

## 6. AI restrictions

A `no-ai-training` or equivalent rule is enforced by capability boundaries. Restricted content is not mounted into the AI service domain. AI MUST NOT infer sacred or restricted meaning without authorized review.

## 7. Withdrawal

Withdrawal creates a governed transition: stop new distribution, update indexes and channels, purge authorized caches when required, issue revocation/withdrawal records, and retain only the minimal lawful audit proof.

## 8. Review and recourse

Rights decisions include evidence, authority, participants, dissent, effective period, review date, and appeal path. Automated suggestions remain reviewable and reversible.

---

<!-- Source: 05-operations/00-observability.md -->

# Observability

## 1. Goals

Observability supports reliability, accountability, security, and reconstruction without exposing unnecessary sensitive content.

## 2. Signals

### Metrics

- availability and latency by capability;
- queue depth and retry rate;
- policy decision outcomes and evaluation time;
- activation and rollback success;
- synchronization age and conflict count;
- storage/cache pressure;
- verification failures;
- resource saturation;
- export/restore test results.

### Logs

Structured logs include timestamp, node, tenant where permitted, service, stage, outcome, error code, dependency, attempt, duration, and correlation ID. Raw claims, testimony, tokens, or secrets are excluded by default.

### Traces

Distributed tracing MAY be used across online services. Trace context MUST NOT create cross-tenant correlation leakage. Offline flows preserve correlation identifiers for later reconstruction.

### Receipts

Receipts are durable evidence for policy, privilege, release, publication, and governance transitions. They are not interchangeable with debugging logs.

## 3. Health model

Health distinguishes:

- process alive;
- dependency reachable;
- contract ready;
- capable of local read;
- capable of write;
- capable of authoritative publication/execution;
- degraded but safe.

## 4. Alerting

Alerts are tied to user or governance impact, not only infrastructure thresholds. Critical alerts include trust failure, repeated activation failure, audit gap, cross-tenant denial anomaly, revocation staleness, and recovery failure.

## 5. Offline operation

Nodes retain bounded local metrics, logs, and receipts. Forwarding resumes with backoff and idempotency. Storage exhaustion policies prioritize security and decision evidence over verbose diagnostics.

---

<!-- Source: 05-operations/01-backup-restore-and-exit.md -->

# Backup, Restore, and Exit

## 1. Backup scope

Backups cover declared product state, governance policy, trust references, Kristal artifacts or references, audit classes, rights/consent records, and restore metadata. Immutable artifacts may be referenced if independent availability is guaranteed; otherwise they are included.

## 2. Backup properties

Backups MUST be:

- encrypted;
- tenant-scoped;
- integrity-protected;
- versioned;
- retention-governed;
- tested by restore;
- independent from the active node where possible.

## 3. Restore

Restore occurs on a clean compatible environment and verifies:

- bundle identity and signature;
- tenant and audience;
- encryption keys;
- schema versions and migrations;
- trust-root continuity;
- artifact inventory;
- policy compatibility;
- post-restore health.

## 4. Sovereignty Bundle

A complete exit export SHOULD contain:

```text
manifest and signature
identity and delegation data
Governance Policy Bundles
Konnaxion export
Orgo export
Kristal artifacts and references
rights and consent records
audit receipts by authorized class
trust-root handover material
restore instructions and tests
```

Private signing keys are included only under a specific protected handover profile; otherwise new keys are enrolled.

## 5. Exit test

A credible exit test:

1. exports a tenant;
2. provisions a clean compatible node from public/documented materials;
3. imports the bundle;
4. verifies hashes and policy;
5. rebuilds indexes;
6. resumes authorized workflows;
7. proves the original operator is no longer required.

## 6. Objectives

Deployments MUST define RPO and RTO by data class and node profile. Recovery of public cache is less critical than identity, protected evidence, policy, and active operational work.

---

<!-- Source: 05-operations/02-capability-degradation.md -->

# Capability-Based Degradation

## 1. Principle

The system degrades capabilities, not truth labels. It distinguishes the ability to inspect, advise, publish, and execute.

## 2. Reference matrix

| State | Inspect context | Use as advisory | Publish as reference | Execute/activate |
|---|---:|---:|---:|---:|
| verified and active | yes | yes | policy-dependent | yes |
| provisional | labeled | limited | no by default | policy-dependent |
| contested | labeled | limited | no as single reference | no by default |
| expired/stale | labeled | limited | no | no |
| revoked | audit/quarantine only | no | no | no |
| corrupted | no | no | no | no |
| incompatible | manifest/diagnostic only | no | no | no |

## 3. Dependency failures

- network loss: local capability continues;
- central identity loss: cached local identity follows declared expiry policy;
- policy runtime loss: sensitive writes deny; safe reads may continue;
- audit forwarding loss: local capture continues;
- Konnaxion loss: Orgo and Kristal may continue;
- Orgo loss: Konnaxion and approved public knowledge may continue;
- AI loss: assistance stops; core correctness continues;
- build farm loss: active releases remain usable.

## 4. Visibility

Users and operators MUST see degraded state, affected capability, last successful synchronization, active release identities, and next safe action. Graceful degradation without visible logging is a failure.

## 5. Restoration

Recovery from degradation uses bounded retries with jitter, health revalidation, and replay-safe queues. A returning dependency MUST NOT immediately receive an uncontrolled backlog storm.

---

<!-- Source: 05-operations/03-slos-and-health.md -->

# SLOs and Health

## 1. SLO model

SLOs are defined by capability and node profile, not only by service uptime.

Representative endpoint objectives:

- local session start success;
- active Kristal query availability while offline;
- local Orgo critical-work availability;
- policy decision latency;
- signed activation success;
- rollback success;
- synchronization recovery after reconnect;
- backup and exit restore success.

## 2. Suggested initial targets

These are engineering starting points, not established production commitments:

- local policy decision p95 under 100 ms for ordinary rules;
- local Kristal query p95 under 250 ms for declared endpoint query classes;
- node-agent operation receipt success above 99.9% excluding denied requests;
- automatic rollback after failed boot acceptance within two boot attempts;
- no loss of committed critical Orgo work under one abrupt power interruption after storage flush guarantees;
- quarterly successful Sovereignty Bundle restore for critical tenants.

## 3. Error budgets

An error budget applies to the capability. Repeated safe denials caused by invalid artifacts are not availability failures, but unexplained denials or inability to inspect reason codes are.

## 4. Health endpoints

Health outputs are authenticated according to sensitivity. Public endpoints expose minimal status. Detailed dependency, tenant, and security state is restricted.

## 5. Synthetic tests

Nodes SHOULD periodically test active pack queries, policy vectors, publication-gateway redaction, local queue durability, and recovery prerequisites without mutating production truth.

---

<!-- Source: 05-operations/04-conformance-tests.md -->

# Conformance Tests

## 1. Conformance levels

- **Foundation**: founding invariants and contract validation;
- **Endpoint**: local/offline/session/runtime requirements;
- **Hub**: tenant, network, database, and synchronization requirements;
- **Build**: reproducibility and artifact-generation requirements;
- **High assurance**: measured boot, split custody, and enhanced audit requirements.

## 2. Required test groups

### Host and boot

- signed image verification;
- immutable drift detection;
- failed-boot rollback;
- recovery target access;
- storage unlock and corruption behavior.

### Privilege

- arbitrary command rejection;
- operation-schema validation;
- policy binding and replay protection;
- least-privilege sandbox verification;
- break-glass expiry.

### Policy

- deterministic test vectors;
- unknown fact handling;
- separation of duties;
- bundle signature and compatibility;
- atomic activation and rollback;
- reason-code stability.

### Kristal

- signature/hash failure;
- channel trust isolation;
- downgrade/substitution rejection;
- query-contract compatibility;
- atomic activation;
- offline serving;
- cache pinning and last-known-good retention;
- revocation handling.

### Product boundaries

- no Konnaxion direct Orgo database access;
- Publication Gateway classification/redaction;
- tenant separation;
- public/private network isolation;
- integration removal without core failure.

### Privacy and rights

- role-based disclosure;
- protected audit access logging;
- no-AI data isolation;
- cultural withdrawal and cache purge;
- audience-scoped pack enforcement.

### Lifecycle

- OS/service/policy/artifact independent activation;
- Release Set compatibility;
- migration interruption and resume;
- offline bundle parser limits;
- rollback and forward repair.

### Exit

- full export;
- clean restore;
- independent verification;
- resumed workflows;
- operator independence.

## 3. Evidence

Test output records release identities, environment, node profile, test vector version, result, logs/receipts, and exceptions. A manual assertion without evidence is not a conformance result.

---

<!-- Source: 05-operations/05-incident-response.md -->

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

---

<!-- Source: 08-adrs/ADR-001-standard-maintained-linux-kernel.md -->

# ADR-001-standard-maintained-linux-kernel — Use a Standard Maintained Linux Kernel

**Status:** Accepted

## Context

kOA requires long-term security maintenance, broad hardware support, measured boot, and upstream compatibility.

## Decision

Use a standard kernel from a recognized distribution or upstream maintenance chain. Product patches remain minimal and upstreamable.

## Consequences

Avoids permanent kernel maintenance burden. Product differentiation remains in policy, services, artifacts, and UX. A custom kernel is permitted only after evidence that an invariant cannot be met upstream.

---

<!-- Source: 08-adrs/ADR-002-immutable-os-image.md -->

# ADR-002-immutable-os-image — Use an Immutable OS Image

**Status:** Accepted

## Context

In-place package mutation creates drift, weakens rollback, and makes field nodes hard to verify.

## Decision

Build and sign the complete OS image and activate it atomically using bootc/OSTree or an equivalent maintained mechanism.

## Consequences

Provides reproducibility and rollback. Requires image build infrastructure and disciplined data separation.

---

<!-- Source: 08-adrs/ADR-003-no-gnome-product-shell.md -->

# ADR-003-no-gnome-product-shell — Do Not Use GNOME as the Product Shell

**Status:** Accepted

## Context

The endpoint needs a constrained appliance experience rather than a general desktop session with a large mutable surface.

## Decision

Use a minimal native `koa-session-shell` on maintained Wayland components. Standard Linux services may still be used where they solve device or accessibility needs.

## Consequences

Reduces resource use and attack surface. The project assumes responsibility for a focused shell and accessibility integration.

---

<!-- Source: 08-adrs/ADR-004-minimal-wayland-and-embedded-web-engine.md -->

# ADR-004-minimal-wayland-and-embedded-web-engine — Use a Minimal Maintained Wayland Stack and Embedded Web Engine

**Status:** Accepted

## Context

Konnaxion and Orgo are web-oriented products, but the node requires a secure appliance session and native recovery/status surfaces.

## Decision

Use a maintained minimal Wayland compositor and a tested WPE/Cog or equivalent embedded browser engine. Keep the shell native and the product workspaces web-hosted.

## Consequences

Preserves existing product investment while avoiding a full desktop environment. Browser updates become a critical security dependency.

---

<!-- Source: 08-adrs/ADR-005-rootless-podman-and-quadlet.md -->

# ADR-005-rootless-podman-and-quadlet — Use Rootless Podman and Quadlet for Application Services

**Status:** Accepted

## Context

Application services need isolation and immutable packaging without requiring endpoint Kubernetes.

## Decision

Run application services as rootless OCI containers managed through systemd Quadlet where feasible.

## Consequences

Provides familiar image distribution and systemd lifecycle. Requires careful SELinux, networking, credential, and volume design.

---

<!-- Source: 08-adrs/ADR-006-konnaxion-and-orgo-co-principal.md -->

# ADR-006-konnaxion-and-orgo-co-principal — Treat Konnaxion and Orgo as Co-Principal Product Planes

**Status:** Accepted

## Context

Konnaxion provides public knowledge and coordination; Orgo provides private operational execution. Subordinating either loses part of the knowledge-to-action loop.

## Decision

Expose both as principal workspaces under `koa-session-shell`, with separate security domains and a controlled publication boundary.

## Consequences

Clarifies product hierarchy and trust. Requires shared identity/context without shared databases.

---

<!-- Source: 08-adrs/ADR-007-kristal-transversal-epistemic-foundation.md -->

# ADR-007-kristal-transversal-epistemic-foundation — Treat Kristal as a Transversal Epistemic Foundation

**Status:** Accepted

## Context

Kristal provides portable epistemic identity, provenance, validation, recognition, federation, and offline query artifacts across products.

## Decision

Place Kristal across build, governance, distribution, and runtime planes. Do not turn it into a workflow engine or universal database.

## Consequences

Prevents semantic duplication and preserves offline knowledge integrity. Requires strict separation from operational state.

---

<!-- Source: 08-adrs/ADR-008-four-release-channels.md -->

# ADR-008-four-release-channels — Separate OS, Services, Governance Policy, and Kristal Channels

**Status:** Accepted

## Context

These artifact classes have different owners, risks, cadence, and rollback semantics.

## Decision

Sign and version them independently; bind tested compatible combinations with a Release Set.

## Consequences

Allows policy and knowledge updates without rebuilding the OS. Adds compatibility-management discipline.

---

<!-- Source: 08-adrs/ADR-009-governance-policy-runtime.md -->

# ADR-009-governance-policy-runtime — Introduce `koa-policy-runtime`

**Status:** Accepted

## Context

Sociotechnical governance cannot remain informal configuration if it controls rights, disclosure, activation, AI, or recourse.

## Decision

Compile and evaluate signed Governance Policy Bundles in a deterministic local runtime that emits decision receipts.

## Consequences

Makes governance testable and versioned. Requires policy authoring, simulation, conformance, and migration tooling.

---

<!-- Source: 08-adrs/ADR-010-selective-audit.md -->

# ADR-010-selective-audit — Use Selective Audit, Not Total Transparency

**Status:** Accepted

## Context

Civic accountability and sensitive operations both matter. A single public log would become surveillance.

## Decision

Separate public transparency receipts, tenant audit, restricted evidence, privacy records, and security audit with distinct policies.

## Consequences

Supports accountability with privacy. Increases data-classification and retention complexity.

---

<!-- Source: 08-adrs/ADR-011-no-kubernetes-on-endpoints.md -->

# ADR-011-no-kubernetes-on-endpoints — Do Not Require Kubernetes on Endpoints

**Status:** Accepted

## Context

Endpoint constraints and offline appliance operation do not justify a cluster control plane.

## Decision

Use systemd and Podman/Quadlet on endpoints. Kubernetes may be used on hubs/build/control environments only when measured scale justifies it.

## Consequences

Reduces footprint and failure modes while preserving optional scale-out elsewhere.

---

<!-- Source: 08-adrs/ADR-012-single-narrow-privileged-broker.md -->

# ADR-012-single-narrow-privileged-broker — Use One Narrow Privileged Node Broker

**Status:** Accepted

## Context

Multiple privileged product services create an unreviewable attack and governance surface.

## Decision

Route normal privileged node mutations through `koa-node-agent` with fixed schemas, policy binding, idempotency, and receipts.

## Consequences

Concentrates review and audit. The broker is high value and must remain small, hardened, and thoroughly tested.

---

<!-- Source: REQUIREMENTS-MATRIX.md -->

# Founding Requirements Matrix

This matrix turns the architecture into verifiable requirements. “Evidence” identifies the minimum proof expected from an implementation.

| ID | Requirement | Level | Owner | Verification evidence |
|---|---|---|---|---|
| KOA-FND-001 | Use a maintained standard Linux kernel. | MUST | OS | kernel provenance, support policy, patch inventory |
| KOA-FND-002 | Build and activate an immutable signed OS image. | MUST | OS | image digest/signature, drift test, rollback test |
| KOA-FND-003 | Expose booted image and active Release Set identity. | MUST | Node | status API and boot evidence |
| KOA-FND-004 | Separate OS, service, policy, and Kristal release identities. | MUST | Release | four signed manifests and compatibility test |
| KOA-FND-005 | Bind tested combinations with a signed Release Set. | MUST | Release | schema-valid Release Set and signature |
| KOA-FND-006 | Present Konnaxion and Orgo as co-principal workspaces. | MUST | UX | navigation and failure-isolation test |
| KOA-FND-007 | Keep Konnaxion and Orgo in separate security domains. | MUST | Platform | process, storage, identity, and network isolation tests |
| KOA-FND-008 | Route cross-domain publication through a controlled gateway. | MUST | Publication | no direct DB access; redaction/disclosure tests |
| KOA-FND-009 | Keep Kristal content identity independent of tenant workflow state. | MUST | Kristal | canonicalization vectors and tenant comparison test |
| KOA-FND-010 | Verify Runtime Pack signature, inventory, compatibility, and channel before activation. | MUST | Kristal/Node | negative and positive conformance vectors |
| KOA-FND-011 | Activate Runtime Packs atomically and retain last-known-good. | MUST | Node | crash-injection and rollback test |
| KOA-FND-012 | Prevent unauthorized downgrade and substitution. | MUST | Node/Kristal | downgrade and same-release/different-artifact tests |
| KOA-FND-013 | Maintain declared minimum capability without Internet. | MUST | Profile owners | cable-pull test and offline acceptance suite |
| KOA-FND-014 | Deny authority when required verification is unavailable. | MUST | All | fail-closed reason-code tests |
| KOA-FND-015 | Preserve safe labeled context where policy permits. | MUST | UX/Kristal | capability-degradation matrix test |
| KOA-FND-016 | Use one narrow normal privileged broker. | MUST | Node | privilege map and arbitrary-command rejection |
| KOA-FND-017 | Require policy decision binding for sensitive node operations. | MUST | Policy/Node | replay, expiry, caller, and decision-binding tests |
| KOA-FND-018 | Emit decision and operation receipts. | MUST | Policy/Node/Audit | schema validation and correlation test |
| KOA-FND-019 | Evaluate required policies locally and deterministically. | MUST | Policy | offline deterministic vector suite |
| KOA-FND-020 | Activate Governance Policy Bundles atomically with rollback. | MUST | Policy/Node | bundle verification and rollback test |
| KOA-FND-021 | Prevent root access from becoming the ordinary governance API. | MUST | Platform | interface review and privileged-path audit |
| KOA-FND-022 | Use rootless containers for application services where feasible. | SHOULD | Platform | runtime identity and capability inspection |
| KOA-FND-023 | Apply default-deny network policy across domains. | MUST | Network | network reachability matrix |
| KOA-FND-024 | Bound retries, queues, timeouts, and resources. | MUST | Services | fault injection and retry-storm test |
| KOA-FND-025 | Preserve public audit and private evidence as separate classes. | MUST | Audit | disclosure and access-control tests |
| KOA-FND-026 | Audit access to restricted evidence. | MUST | Audit | read-access receipt test |
| KOA-FND-027 | Keep secrets out of images, logs, receipts, and ordinary exports. | MUST | Security | secret scan and export inspection |
| KOA-FND-028 | Scope trust roots by tenant, environment, channel, and artifact class. | MUST | Trust | cross-scope rejection tests |
| KOA-FND-029 | Support signed offline revocation and trust updates. | MUST | Trust/Node | disconnected revocation test |
| KOA-FND-030 | Treat AI output as untrusted candidate input. | MUST | AI/Applications | direct-authority negative tests |
| KOA-FND-031 | Enforce AI data capabilities at mount/network/API boundaries. | MUST | AI/Platform | restricted-data isolation test |
| KOA-FND-032 | Preserve baseline and advisory readings where weighted civic results exist. | MUST | Konnaxion | result and explanation API tests |
| KOA-FND-033 | Never map SmartVote/EkoH directly to Linux privilege. | MUST | Konnaxion/Node | authorization architecture test |
| KOA-FND-034 | Enforce cultural rights and consent at every access boundary. | MUST | Rights/Applications | read, export, AI, sync, and withdrawal tests |
| KOA-FND-035 | Build audience-scoped or encrypted artifacts for restricted content. | SHOULD | Kristal/Distribution | artifact inventory and audience test |
| KOA-FND-036 | Classify every external integration. | MUST | Integration owner | signed integration manifest |
| KOA-FND-037 | Remove an optional integration without core failure. | MUST | Integration owner | removal and degraded-operation test |
| KOA-FND-038 | Use Transactional Outbox when local commit emits external events. | MUST where applicable | Product owners | transaction/failure injection test |
| KOA-FND-039 | Make consumers idempotent and poison messages reviewable. | MUST | Messaging | duplicate and dead-letter tests |
| KOA-FND-040 | Declare irreversible migrations and provide forward repair. | MUST | Data owner | migration plan and interrupted-run test |
| KOA-FND-041 | Encrypt sensitive durable state at rest. | MUST | Platform/Data | storage inspection and key-loss behavior |
| KOA-FND-042 | Provide signed offline import with quarantine. | MUST | Node | malicious media and parser-limit suite |
| KOA-FND-043 | Provide encrypted backup and verified restore. | MUST | Operations | scheduled clean restore result |
| KOA-FND-044 | Export a documented Sovereignty Bundle. | MUST | Product/Operations | schema/inventory verification |
| KOA-FND-045 | Restore a Sovereignty Bundle without the original operator. | MUST | Operations | independent clean-node exit test |
| KOA-FND-046 | Provide a separate recoverable boot target. | MUST | OS/Node | recovery-entry and action tests |
| KOA-FND-047 | Govern and receipt break-glass actions. | MUST | Policy/Node/Audit | expiry and post-review tests |
| KOA-FND-048 | Preserve local critical audit capture during network loss. | MUST | Audit | network-loss and storage-pressure tests |
| KOA-FND-049 | Produce SBOM, provenance, and conformance evidence for releases. | SHOULD | Release | release evidence bundle |
| KOA-FND-050 | Record and expose implementation exceptions through ADRs. | MUST | Architecture | ADR review and exception inventory |

---

<!-- Source: SOURCES.md -->

# Sources, Documentary Authority, and Provenance

## 1. Purpose

This foundation was derived from the kOA architecture conversation and the documentary corpus supplied with it. The source materials vary in technical authority. This repository therefore distinguishes normative technical sources, product architecture sources, and vision/governance sources.

## 2. Authority order used for this specification

1. **Kristal v5 contracts, schemas, query, activation, and integration documentation** — authoritative for Kristal artifact semantics and conformance.
2. **Orgo technical documentation** — authoritative for Orgo domain boundaries, workflow, tenancy, identity, offline, and adapter behavior.
3. **Konnaxion technical documentation and codebase guidance** — authoritative for the current product stack, global layout, modules, routes, and product constraints.
4. **SenTient and Architect technical documentation** — authoritative for their own runtime, technology, and maturity boundaries.
5. **Senior Architect Codex** — pattern catalog and trade-off guidance, not an automatic mandate to apply every pattern.
6. **Sociotechnical, thesis, commons, cultural-sovereignty, and impact documents** — sources of system goals, governance requirements, threat categories, and non-domination constraints; not direct Linux implementation specifications.

When these sources conflict, the narrower and more recent normative technical contract takes precedence within its domain.

## 3. Principal technical materials

- Kristal Framework documentation and v5 context pack: contracts, schemas, query semantics, authority, reader policy, federation, Runtime Packs, offline activation, tenant separation, and release strategies.
- Konnaxion documentation: Django/DRF/Celery/Redis backend, Next.js/React frontend, global shell/layout, module routing, public coordination, offline distribution, SmartVote/EkoH, and system-of-systems boundaries.
- Orgo documentation: Signals, Cases, Tasks, workflow, multi-tenancy, identity, offline persistence/synchronization, audit, and headless service boundaries.
- SenTient documentation: optional ambiguity resolution, entity linking, normalization, and heavy service topology.
- Architect documentation: deterministic rendering after validation, multilingual output, build pipeline, and current maturity constraints.
- Senior Architect Codex: hexagonal architecture, anti-corruption layers, modular monoliths, outbox, idempotency, resilience, immutable deployment, observability, and warnings against premature complexity.

## 4. Principal governance and systems materials

The following supplied works informed the governance, resilience, privacy, cultural-rights, and exit requirements:

- *Toward a Governable Civic Infrastructure* (thesis draft, March 2026);
- *The kOA Digital Ecosystem — A Sociotechnical Operating System for Knowledge-to-Action*;
- *Sociotechnical Operating Systems: When Governance Becomes Runtime*;
- *What Is the kOA Digital Ecosystem?*;
- *kOA: A Governable Knowledge-to-Action Ecosystem for the Commons*;
- *Operationalizing Cultural Sovereignty*;
- *SmartVote: A Governance-Grade Like for Konnaxion*;
- *Knowledge-to-Action Infrastructure* impact report;
- *A Technosocial Architecture for Knowledge-to-Action*;
- strategic and civilizational impact analyses supplied in the conversation.

These works support the following requirements:

- offline and local continuity as a governance safeguard;
- fail-closed authority with safe degradation;
- auditability without indiscriminate exposure;
- explicit, contestable, versioned rules;
- semantic sovereignty and plural authority;
- bounded AI and no invisible authority;
- separation of public deliberation from private execution;
- cultural consent, rights, withdrawal, and community authority;
- self-hosting, portability, recourse, and credible exit.

## 5. Conversation decisions incorporated

The architecture review in this conversation established:

- Konnaxion and Orgo are co-principal;
- Kristal is transversal rather than merely a Konnaxion feature;
- Claim-IR and SenTient are optional paths, not universal stages;
- `koa-session-shell` is a minimal system shell, not Konnaxion itself;
- `koa-node-agent` is the sole narrow normal privileged broker;
- policy is a separate signed release class;
- Konnaxion owns the activation experience, while privileged activation remains in the node plane;
- public/private exchange uses a controlled Publication Gateway;
- the endpoint, sovereign hub, build farm, and control plane are distinct node profiles.

## 6. Important limitations

This repository contains architecture decisions and illustrative contracts. It does not replace:

- the complete Kristal normative specification;
- source-code review of Konnaxion or Orgo;
- a selected Linux distribution's security documentation;
- hardware qualification;
- legal analysis by jurisdiction;
- a production penetration test;
- operational SLO evidence;
- formal verification of policy or artifact compilers.

## 7. Citation practice for future revisions

Future changes SHOULD identify:

- source document and version;
- whether the change is normative, inferred, or proposed;
- affected requirement IDs;
- superseded ADRs or contracts;
- validation evidence.

---
