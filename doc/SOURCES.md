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
