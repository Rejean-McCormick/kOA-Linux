# kOA Linux Foundation

**Version:** 0.2-foundation-english  
**Date:** 2026-07-29  
**Status:** normative target architecture; implementation validation required

## Purpose

This repository defines the founding architecture for **kOA Linux**, the sovereign appliance runtime of the kOA Digital Ecosystem.

The design treats Linux as the maintained mechanism layer; Konnaxion and Orgo as co-principal product planes; Kristal as the shared epistemic foundation; and the kOA Governance Plane as the bridge that turns explicit sociotechnical rules into inspectable, receipted, least-privilege operations.

## Core statement

> Linux provides the security and isolation mechanisms. Kristal provides the epistemic contracts. Konnaxion and Orgo provide the principal coordination and execution planes. The kOA Governance Plane turns sociotechnical rules into signed, inspectable, contestable, and reversible decisions.

## Architecture at a glance

```text
┌──────────────────────────────────────────────────────────────┐
│                    koa-session-shell                         │
│ Konnaxion workspace • Orgo workspace • Kristal Library      │
├──────────────────────────────────────────────────────────────┤
│                    Application Plane                         │
│ Konnaxion Core • Orgo Core • Kristal Runtime • adapters     │
├──────────────────────────────────────────────────────────────┤
│                    Governance Plane                          │
│ policy runtime • audit broker • publication gateway         │
├──────────────────────────────────────────────────────────────┤
│                    Node Plane                                │
│ node agent • trust • releases • sync • export • recovery    │
├──────────────────────────────────────────────────────────────┤
│ rootless containers • systemd • LSM • cgroups • namespaces  │
├──────────────────────────────────────────────────────────────┤
│                 immutable maintained Linux                   │
└──────────────────────────────────────────────────────────────┘
```

## Repository map

| Directory | Contents |
|---|---|
| `00-foundation/` | charter, invariants, scope, glossary |
| `01-architecture/` | logical/physical architecture, node profiles, storage, network, boot |
| `02-components/` | component and domain specifications |
| `03-lifecycle/` | release channels, updates, policy, Kristal, offline, rollback, migration |
| `04-security/` | threat model, baseline, privacy, keys, AI, integration, cultural rights |
| `05-operations/` | observability, backup/exit, degradation, SLOs, conformance, incidents |
| `06-contracts/` | JSON Schemas and examples |
| `07-systemd/` | illustrative systemd and Quadlet units |
| `08-adrs/` | founding architecture decisions |

## Normative reading order

1. `00-foundation/00-charter.md`
2. `00-foundation/01-normative-invariants.md`
3. `01-architecture/00-system-context.md`
4. `01-architecture/01-logical-architecture.md`
5. `01-architecture/04-process-and-trust-boundaries.md`
6. `03-lifecycle/00-release-model.md`
7. `04-security/00-threat-model.md`
8. `05-operations/04-conformance-tests.md`
9. `REQUIREMENTS-MATRIX.md`

A single combined edition is available in `KOA-LINUX-FOUNDATION.md`.

## Normative language

- **MUST / MUST NOT** — required for conformance;
- **SHOULD / SHOULD NOT** — expected unless a documented ADR explains the exception;
- **MAY** — optional behavior that must preserve all invariants.

## Principal design decisions

- maintained standard Linux kernel;
- immutable signed OS image;
- minimal Wayland product shell, not GNOME;
- rootless Podman/Quadlet for application services;
- one narrow privileged node broker;
- deterministic local policy runtime;
- Konnaxion and Orgo as co-principal security and product domains;
- Kristal as a transversal epistemic foundation;
- four independent signed release channels;
- selective audit rather than total transparency;
- no mandatory Kubernetes on endpoints;
- tested export, restore, and credible exit.

## Implementation status

This repository is a founding specification. It does not claim that the following choices have been proven across all target hardware:

- final base distribution;
- exact immutable-image implementation;
- final compositor and web engine;
- TPM requirements by assurance level;
- final key-custody topology;
- final SLOs and capacity numbers;
- regulatory profiles;
- complete production code for the specified node services.

Those decisions require prototypes, benchmarks, security review, and deployment evidence.

## Validation included in this archive

The archive build validates:

- JSON syntax and JSON Schema structure;
- YAML example syntax when PyYAML is available;
- English filename policy;
- Markdown internal links in the root README and consolidated index;
- absence of broken relative file references in generated indexes;
- SHA-256 manifest consistency;
- ZIP integrity.
