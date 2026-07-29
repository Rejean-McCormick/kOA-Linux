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
