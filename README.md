# kOA Linux Foundation

> Sovereign, immutable, offline-capable, and governable Linux operating environment for the kOA ecosystem.

**Specification version:** `0.2-foundation-english`  
**Documentation architecture:** contract-first  
**Status:** normative target architecture; implementation validation required  
**Last documentation validation:** August 4, 2026

## Overview

kOA Linux is the governed operating environment of the kOA ecosystem. It is not a general-purpose desktop distribution and it is not the product specification of every subsystem it hosts.

The repository defines:

- system invariants and operating boundaries;
- deployable profiles and resource envelopes;
- internal kOA components;
- trust, identity, storage, network, lifecycle, security, and operational rules;
- integration contracts for independently documented subsystems;
- release, recovery, conformance, and validation requirements.

Each integrated subsystem remains authoritative for its own internal domain model, workflows, state machines, complete APIs, user interfaces, and product behavior. kOA documents only the operating environment and the interfaces that cross the kOA boundary.

## Core statement

> Linux provides isolation and host mechanisms. kOA provides the governed operating environment. Source contracts and accepted decisions define authority. Integrated subsystems retain authority over their internal behavior.

## Authority model

The active documentation corpus follows these rules:

1. Source contracts and normative source documents define current facts.
2. Accepted ADRs close architectural decisions.
3. Executable validators enforce structural and semantic constraints.
4. Generated indexes support discovery but have no independent authority.
5. Subsystem documentation is referenced through reserved mount points rather than copied into kOA.
6. Missing information is not inferred from obsolete documents or undeclared compatibility behavior.

AI-assisted work starts at [`docs/AI_CONTEXT.md`](docs/AI_CONTEXT.md).

## Architecture

```text
┌──────────────────────────────────────────────────────────────────┐
│                       kOA user surfaces                          │
│ session shell • profile-specific interfaces • local operations  │
├──────────────────────────────────────────────────────────────────┤
│              profile-selected integrated subsystems              │
│ Ariane • Konnaxion • Orgo • SenTient • SemantiK Architect • UCKK│
├──────────────────────────────────────────────────────────────────┤
│                    internal kOA components                       │
│ node agent • governance • trust • audit • publication • resources│
│ Kristal runtime • UCKK dimension gateway                        │
├──────────────────────────────────────────────────────────────────┤
│ rootless services • systemd • LSM • cgroups • namespaces        │
├──────────────────────────────────────────────────────────────────┤
│                  immutable maintained Linux                      │
└──────────────────────────────────────────────────────────────────┘
```

## Integrated subsystems

| Subsystem | Role at the kOA boundary | Authoritative internal documentation |
| --- | --- | --- |
| **Ariane** | Local navigation and interaction orchestration | `docs/subsystems/ariane/` |
| **Konnaxion** | Public, community, and civic coordination | `docs/subsystems/konnaxion/` |
| **Orgo** | Private and organizational execution | `docs/subsystems/orgo/` |
| **SenTient** | Optional isolated research and enrichment workbench | `docs/subsystems/sentient/` |
| **SemantiK Architect** | Language construction and verified artifact production | `docs/subsystems/semantik-architect/` |
| **UCKK** | Native media, file classification, managed storage, provenance, rights, and lifecycle | `docs/subsystems/uckk/` |

kOA boundary summaries live in [`docs/04-components/subsystems/`](docs/04-components/subsystems/). Machine-readable boundary contracts live in [`docs/contracts/subsystems/`](docs/contracts/subsystems/).

### UCKK Mediatheque

The Mediatheque is native to UCKK. UCKK owns its complete object, version, classification, rights, restriction, provenance, rendition, duplicate-handling, import, export, audit, backup, and restore models.

kOA documents only deployment, resources, trust, storage exposure, gateways, publication, health, backup coordination, and degradation behavior.

The local baseline uses SQLite and managed local storage. XLSX and approved AI surfaces are interfaces; they are not authorities.

The mounted UCKK documentation is expected to expose the Mediatheque at:

```text
docs/subsystems/uckk/mediatheque/
```

## Internal kOA components

The internal components documented completely by kOA include:

- `koa-node-agent`;
- `governance-policy-runtime`;
- `identity-and-trust`;
- `audit-broker`;
- `publication-gateway`;
- `resource-governor`;
- `kristal-runtime`;
- `uckk-dimension-gateway`.

Their machine-readable contracts live in [`docs/contracts/components/`](docs/contracts/components/).

## Foundational principles

A conforming implementation preserves the following properties:

1. **Offline capability** — core consultation, verification, execution, and recovery remain available without permanent cloud connectivity.
2. **Verified activation** — artifacts, policies, services, and releases activate only after declared integrity, compatibility, trust, and authorization checks succeed.
3. **Safe degradation** — failures block unsafe actions while preserving context, status, evidence, and recoverability.
4. **Deterministic-first execution** — core transformations are reproducible; AI remains optional, bounded, attributable, and unable to create invisible authority.
5. **Least privilege** — integrated subsystems and optional services do not receive unrestricted host capabilities.
6. **Explicit governance** — governance rules are versioned policy artifacts rather than undocumented operator behavior.
7. **Selective audit** — the system remains auditable without indiscriminate disclosure of personal or operational data.
8. **Semantic sovereignty** — terminology, authority channels, contested concepts, and multilingual mappings remain governed and portable.
9. **Cultural rights enforcement** — consent, community authority, access conditions, withdrawal, and AI restrictions are enforced across the data lifecycle.
10. **Credible exit** — export, transfer, restore, self-hosting, trust handover, and operator independence are tested product capabilities.

## Documentation structure

| Path | Purpose |
| --- | --- |
| [`docs/00-governance/`](docs/00-governance/) | Documentation authority, change rules, ownership, validation, and lifecycle |
| [`docs/01-constitution/`](docs/01-constitution/) | Charter, scope, invariants, principles, and glossary |
| [`docs/02-system/`](docs/02-system/) | System context, logical architecture, boundaries, capabilities, and operating behavior |
| [`docs/03-profiles/`](docs/03-profiles/) | Deployable profiles, composition, activation, resources, connectivity, and degradation |
| [`docs/04-components/`](docs/04-components/) | Internal components and subsystem integration boundaries |
| [`docs/05-development/`](docs/05-development/) | Development environments, isolation, builds, tests, and publication |
| [`docs/06-lifecycle/`](docs/06-lifecycle/) | Artifacts, releases, activation, verification, recovery, and contract evolution |
| [`docs/07-security/`](docs/07-security/) | Threats, trust, privileges, storage, network, privacy, rights, and supply chain |
| [`docs/08-operations/`](docs/08-operations/) | Health, observability, capacity, backup, restore, incidents, and maintenance |
| [`docs/09-conformance/`](docs/09-conformance/) | Requirements, evidence, traceability, release gates, and executable controls |
| [`docs/10-adrs/`](docs/10-adrs/) | Accepted architecture decisions |
| [`docs/11-recipes/`](docs/11-recipes/) | Profile-specific operational recipes |
| [`docs/contracts/`](docs/contracts/) | Canonical machine-readable contracts |
| [`docs/schemas/`](docs/schemas/) | JSON Schemas for source contracts and exchanged artifacts |
| [`docs/tools/`](docs/tools/) | Generators and validators |
| [`docs/generated/`](docs/generated/) | Rebuildable indexes, catalogs, traceability, and AI context |
| [`docs/subsystems/`](docs/subsystems/) | Reserved mount points for authoritative subsystem documentation |

Do not edit files under `docs/generated/` manually.

## Recommended reading paths

### First reading

1. [`docs/README.md`](docs/README.md)
2. [`docs/01-constitution/00-charter.md`](docs/01-constitution/00-charter.md)
3. [`docs/02-system/00-system-overview.md`](docs/02-system/00-system-overview.md)
4. [`docs/04-components/04-subsystem-documentation-boundaries.md`](docs/04-components/04-subsystem-documentation-boundaries.md)
5. [`docs/09-conformance/00-conformance-model.md`](docs/09-conformance/00-conformance-model.md)

### AI and automation

1. [`docs/AI_CONTEXT.md`](docs/AI_CONTEXT.md)
2. [`docs/contracts/ai-navigation.contract.json`](docs/contracts/ai-navigation.contract.json)
3. Applicable source contract
4. Applicable subsystem boundary contract
5. Mounted authoritative subsystem documentation
6. Generated indexes for discovery only

## Mounting subsystem documentation

The six subsystem paths are intentionally reserved. Until a subsystem repository is available, an unmounted-path warning is expected and does not invalidate the kOA corpus.

Use directory junctions on Windows or symbolic links on Linux. Do not use `.lnk` shortcut files.

### Windows junction example

```bat
mklink /J docs\subsystems\ariane C:\path\to\ariane\docs
```

### Linux symbolic-link example

```bash
ln -s /path/to/ariane/docs docs/subsystems/ariane
```

Repeat with the appropriate target for each subsystem.

## Release and recovery model

kOA activates only verified and compatible release sets. An activation failure leaves the current verified release active. Recovery restores the latest verified release as one unit; it does not reactivate an undeclared operating mode.

Release identity, artifact identity, trust, compatibility, authorization, and evidence must agree before activation.

## Validation

Run the complete documentation validation pipeline from the repository root:

```bash
python docs/tools/validate_docs.py
```

The pipeline executes the specialized documentation controls, including contract, authority, graph, generated-content, subsystem-boundary, language, profile, release, and traceability checks.

Rebuild generated navigation after changing source contracts or source documents:

```bash
python docs/tools/build_indexes.py
python docs/tools/build_ai_context.py
python docs/tools/check_generated_content.py
```

Check subsystem mounts without requiring all of them to be present:

```bash
python docs/tools/check_subsystem_alignment.py
```

After all six official documentation trees are mounted, enforce their presence:

```bash
python docs/tools/check_subsystem_alignment.py --require-mounted
```

## Contributing

A documentation change should follow this sequence:

1. Update the authoritative source contract or normative source document.
2. Update only the kOA boundary when the change belongs to an external subsystem.
3. Add or update an ADR when an architectural decision changes.
4. Rebuild generated indexes and AI context.
5. Run the complete validation pipeline.
6. Commit source changes and regenerated outputs together.

Do not:

- recreate hand-maintained registries or file catalogs;
- duplicate a subsystem's internal model, complete API, workflow, or user interface;
- edit generated outputs as if they were sources;
- infer missing authority from historical documents;
- introduce undeclared substitution or compatibility behavior;
- use Windows `.lnk` files for subsystem documentation mounts.

## Implementation status

This repository defines a normative target architecture and validated documentation corpus. It does not claim that every implementation choice has been proven across all hardware, scale, threat, legal, and operational environments.

Implementation evidence is still required for areas such as:

- final host distribution and immutable-image mechanism;
- production key custody and signing topology;
- hardware-backed trust requirements by assurance level;
- capacity limits and service-level objectives;
- database and tenant isolation at scale;
- regulatory deployment profiles;
- production implementations of internal kOA components.

## Project boundary

This repository specifies kOA Linux, its internal components, profiles, operating rules, and subsystem integration boundaries.

It does not replace the complete product documentation of Ariane, Konnaxion, Orgo, SenTient, SemantiK Architect, UCKK, or future independently documented subsystems. Those systems integrate through the contracts and reserved documentation mounts defined here.
