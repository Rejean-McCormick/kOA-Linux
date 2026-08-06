# kOA-Linux Operating System

> Sovereign, local-first, offline-capable, and governable operating system for kOA ecosystem workloads.

**Documentation architecture:** contract-first  
**Status:** normative target architecture; implementation validation required  
**Last documentation validation:** August 6, 2026

## Overview

kOA-Linux Operating System provides a governed local execution environment for knowledge, coordination, media, language, navigation, publication, recovery, and offline operation.

kOA Spaces is the optional, replaceable global experience layer. It composes validated navigation and presentation contributions into the module selector, active-module sidebar, top bar, and shared page surface. It does not own business authority, authorization, workflows, subsystem data, host privilege, resource admission, release activation, backup, or recovery.

It is not a general-purpose desktop distribution, and it does not absorb the internal authority of the applications and independently documented systems it hosts or integrates.

The repository defines:

- constitutional and system invariants;
- deployment profiles and resource envelopes;
- internal kOA components;
- trust, identity, storage, network, lifecycle, security, and operations rules;
- integration boundaries for independent systems and external services;
- release, recovery, conformance, and validation requirements.

## Core statement

> kOA-Linux owns the local operating boundary. Each component or independent system owns its declared domain. kOA Spaces owns only the optional global presentation and navigation frame. The kOA Mediatheque is the private offline media authority. UCKK is the online Moodle learning and dissemination platform. Interface composition and controlled interchange never merge authority.

## Authority model

1. Source contracts and normative source documents define current facts.
2. Accepted decisions close architectural choices.
3. Executable validators enforce declared structural and semantic constraints.
4. Generated indexes support discovery but have no independent authority.
5. Independently documented systems retain authority over their internal domain model and behavior.
6. Missing information is not inferred from obsolete documents or undeclared compatibility behavior.

AI-assisted work starts at [`docs/AI_CONTEXT.md`](docs/AI_CONTEXT.md).

## Architecture

```text
┌──────────────────────────────────────────────────────────────────┐
│                         user surfaces                            │
│ local work • guidance • private instructions • offline learning │
├──────────────────────────────────────────────────────────────────┤
│             optional kOA Spaces experience layer                 │
│ module selector • sidebar • top bar • shared page surface       │
├──────────────────────────────────────────────────────────────────┤
│                 profile-selected kOA systems                     │
│ Ariane • Konnaxion • Orgo • Kristal • language runtimes         │
├──────────────────────────────────────────────────────────────────┤
│                    internal kOA components                       │
│ node • governance • trust • audit • resources • publication     │
│ kOA Mediatheque: private, local, offline authority              │
├──────────────────────────────────────────────────────────────────┤
│               governed external interchange                     │
│ publish_to_uckk • import_from_uckk • receipts • provenance      │
├──────────────────────────────────────────────────────────────────┤
│         UCKK: online Moodle learning and dissemination          │
│ courses • learning paths • instructions • UCKK Mediatheque      │
└──────────────────────────────────────────────────────────────────┘
```

## kOA Spaces experience layer

kOA Spaces is an independently documented, optional subsystem integrated by kOA-Linux as the global experience and navigation layer.

It owns:

- the module selector;
- the active-module sidebar;
- global top-bar composition;
- the shared page surface and presentation routing;
- responsive and accessibility behavior of the global shell;
- offline presentation state;
- validation and atomic activation of Space definitions and interface manifests.

It does not own:

- authentication or authorization;
- business workflows or domain state;
- media, learning, task, governance, or publication authority;
- release signing or host-level activation authority;
- privileged host operations;
- resource admission or scheduling;
- backup, restore, or disaster recovery;
- the internal implementation of Ariane, Konnaxion, Orgo, SenTient, SemantiK Architect, or another contributing system.

A route, menu item, alias, sidebar entry, or widget is a presentation contribution only. Every operation remains authorized and executed by the system that owns the underlying capability and state. Removing kOA Spaces removes that presentation surface without transferring or deleting the authoritative state of contributing systems.

Canonical entry points:

- [`docs/02-system/21-koa-spaces-experience-layer.md`](docs/02-system/21-koa-spaces-experience-layer.md);
- [`docs/02-system/22-koa-spaces-interface-composition.md`](docs/02-system/22-koa-spaces-interface-composition.md);
- [`docs/03-profiles/14-koa-spaces-deployment.md`](docs/03-profiles/14-koa-spaces-deployment.md);
- [`docs/04-components/subsystems/koa-spaces.md`](docs/04-components/subsystems/koa-spaces.md);
- [`docs/contracts/subsystems/koa-spaces.subsystem.json`](docs/contracts/subsystems/koa-spaces.subsystem.json).

## The two Mediatheques

The **kOA Mediatheque** and the **UCKK Mediatheque** use the same shared Mediatheque frame or compatible versions of it. The frame covers object identity, versions, hashes, metadata, dimensions, collections, relationships, rights, restrictions, provenance, renditions, lifecycle, manifests, and receipts.

They remain distinct authorities:

| Surface | Primary role | Connectivity | Authority |
| --- | --- | --- | --- |
| **kOA Mediatheque** | Private local files, instructions, organizational knowledge, downloaded learning material, and offline use | Fully local and offline-capable | Owns local records, local versions, storage bindings, local rights state, and local lifecycle |
| **UCKK Mediatheque** | Online educational distribution inside UCKK/Moodle | Online platform | Owns UCKK records, courses, paths, activities, permissions, and online lifecycle |

A common frame does not create a shared database, shared identifier space, shared access control, shared lifecycle, or automatic synchronization.

## Governed UCKK interchange

kOA-Linux exposes two explicit operations:

```text
publish_to_uckk
import_from_uckk
```

### Local to online

```text
local selection
→ rights, consent, and disclosure review
→ Publication Gateway authorization
→ UCKK-specific package and transport
→ UCKK acceptance
→ local publication receipt
```

The kOA source remains authoritative locally. UCKK creates or updates a separate online object and becomes authoritative for that remote object.

### Online to local

```text
UCKK course, path, instruction, or resource selection
→ source, license, integrity, and compatibility verification
→ controlled download or offline bundle transfer
→ quarantine and validation
→ explicit acceptance by the kOA Mediatheque
→ local offline availability with preserved UCKK provenance
```

The imported copy becomes a local kOA object. It does not grant kOA write authority over the UCKK source.

No background bidirectional synchronization is implied. Each direction has its own request, validation, receipt, failure state, and conflict policy.

## Offline learning and private instruction

A deployment can use kOA-Linux as a private operational library or as an offline learning environment. It may contain:

- the complete kOA-Linux user and administrator manual;
- procedures for one organization;
- a school curriculum for an isolated community;
- maintenance and emergency instructions;
- a local professional training program;
- an “univers-cité” devoted to bread making, agriculture, construction, health, or another practical domain.

An installation is not required to accept a universal public catalog. It can keep all locally authored content private. Selected UCKK courses and learning paths can be downloaded, verified, retained locally, and consulted for long periods without Internet access.

## Internal kOA components

Internal components documented completely by kOA include:

- `koa_node_agent`;
- `governance_policy_runtime`;
- `identity_and_trust`;
- `audit_broker`;
- `publication_gateway`;
- `resource_governor`;
- `kristal_runtime`;
- `koa_mediatheque`.

UCKK is not an internal kOA-Linux component and is not required for local or offline operation.

## Independently documented systems

Ariane, kOA Spaces, Konnaxion, Orgo, SenTient, and SemantiK Architect retain authority over their internal behavior. kOA boundary summaries live under [`docs/04-components/subsystems/`](docs/04-components/subsystems/), and their machine-readable boundary contracts live under [`docs/contracts/subsystems/`](docs/contracts/subsystems/). kOA Spaces is integrated only as the optional navigation and interface-composition layer; its presence does not make presentation artifacts authoritative.

UCKK is handled as an external online Moodle integration rather than as a mounted local subsystem.

## Foundational principles

1. **Offline continuity** — installed local capabilities and content remain usable without permanent connectivity.
2. **Explicit authority** — every mutation, import, publication, activation, or privilege use has a resolvable owner and authorization path.
3. **Component separation** — common schemas and shared infrastructure do not merge authority.
4. **Safe degradation** — unavailable external services disable only their dependent operations.
5. **Verified transitions** — imported bundles, publications, releases, restores, and critical mutations produce structured evidence.
6. **Deterministic-first operation** — core local behavior is reproducible; AI remains optional and non-authoritative.
7. **Selective disclosure** — private local content is not transferred merely because a compatible online destination exists.
8. **Portability and exit** — export, transfer, restore, self-hosting, and independent consumption remain testable capabilities.
9. **Replaceable experience layer** — kOA Spaces may be disabled or replaced without transferring authority, deleting business state, or disabling native administration and subsystem interfaces.

## Documentation structure

| Path | Purpose |
| --- | --- |
| [`docs/00-governance/`](docs/00-governance/) | Documentation authority, change rules, ownership, validation, and lifecycle |
| [`docs/01-constitution/`](docs/01-constitution/) | Charter, scope, invariants, principles, and glossary |
| [`docs/02-system/`](docs/02-system/) | System context, architecture, offline behavior, and integration boundaries |
| [`docs/03-profiles/`](docs/03-profiles/) | Deployable profiles and capability envelopes |
| [`docs/04-components/`](docs/04-components/) | Internal components and integration boundaries |
| [`docs/05-development/`](docs/05-development/) | Development environments, builds, tests, and publication |
| [`docs/06-lifecycle/`](docs/06-lifecycle/) | Artifacts, releases, activation, recovery, and contract evolution |
| [`docs/07-security/`](docs/07-security/) | Trust, privileges, security controls, profile applicability, storage, network, privacy, rights, and supply chain |
| [`docs/08-operations/`](docs/08-operations/) | Health, capacity, backup, restore, incidents, and maintenance |
| [`docs/09-conformance/`](docs/09-conformance/) | Requirements, evidence, traceability, and executable controls |
| [`docs/10-adrs/`](docs/10-adrs/) | Active architectural decisions |
| [`docs/11-recipes/`](docs/11-recipes/) | Profile-specific non-normative implementation recipes |
| [`docs/contracts/`](docs/contracts/) | Canonical machine-readable contracts |
| [`docs/schemas/`](docs/schemas/) | JSON Schemas for contracts and exchanged artifacts |
| [`docs/tools/`](docs/tools/) | Generators and validators |
| [`docs/generated/`](docs/generated/) | Rebuildable indexes, catalogs, traceability, and AI context |

Do not edit files under `docs/generated/` manually.

## Recommended reading path

1. [`docs/README.md`](docs/README.md)
2. [`docs/01-constitution/00-charter.md`](docs/01-constitution/00-charter.md)
3. [`docs/02-system/00-system-overview.md`](docs/02-system/00-system-overview.md)
4. [`docs/02-system/12-koa-mediatheque-system-boundary.md`](docs/02-system/12-koa-mediatheque-system-boundary.md)
5. [`docs/04-components/koa-mediatheque.md`](docs/04-components/koa-mediatheque.md)
6. [`docs/04-components/uckk-publication-bridge.md`](docs/04-components/uckk-publication-bridge.md)
7. [`docs/04-components/uckk-import-bridge.md`](docs/04-components/uckk-import-bridge.md)
8. [`docs/10-adrs/ADR-032-directional-interchange-between-koa-and-uckk-mediatheques.md`](docs/10-adrs/ADR-032-directional-interchange-between-koa-and-uckk-mediatheques.md)
9. [`docs/09-conformance/00-conformance-model.md`](docs/09-conformance/00-conformance-model.md)

### kOA Spaces architecture review

1. [`docs/02-system/21-koa-spaces-experience-layer.md`](docs/02-system/21-koa-spaces-experience-layer.md)
2. [`docs/02-system/22-koa-spaces-interface-composition.md`](docs/02-system/22-koa-spaces-interface-composition.md)
3. [`docs/03-profiles/14-koa-spaces-deployment.md`](docs/03-profiles/14-koa-spaces-deployment.md)
4. [`docs/04-components/subsystems/koa-spaces.md`](docs/04-components/subsystems/koa-spaces.md)
5. [`docs/contracts/subsystems/koa-spaces.subsystem.json`](docs/contracts/subsystems/koa-spaces.subsystem.json)
6. [`docs/contracts/artifact-contracts/space-definition.schema.json`](docs/contracts/artifact-contracts/space-definition.schema.json)
7. [`docs/contracts/artifact-contracts/module-interface-manifest.schema.json`](docs/contracts/artifact-contracts/module-interface-manifest.schema.json)

### Security architecture review

1. [`docs/07-security/00-threat-model.md`](docs/07-security/00-threat-model.md)
2. [`docs/07-security/01-security-baseline.md`](docs/07-security/01-security-baseline.md)
3. [`docs/07-security/21-security-control-architecture.md`](docs/07-security/21-security-control-architecture.md)
4. [`docs/07-security/22-security-control-profile-matrix.md`](docs/07-security/22-security-control-profile-matrix.md)
5. [`docs/contracts/security-controls.contract.json`](docs/contracts/security-controls.contract.json)
6. [`docs/09-conformance/04-profile-test-matrices.md`](docs/09-conformance/04-profile-test-matrices.md)
7. [`docs/09-conformance/05-test-evidence.md`](docs/09-conformance/05-test-evidence.md)

The thematic security documents define security behavior and requirements. The security-controls contract owns control identifiers, categories, profile applicability, validation bindings, failure behavior, and evidence classes.

## Validation

From the repository root:

```powershell
python docs\tools\build_indexes.py
python docs\tools\build_ai_context.py
python docs\tools\validate_docs.py
```

A passing validator proves the constraints implemented by the current validators. It does not replace semantic review of product identity, authority, or integration direction.

## Implementation status

This repository currently defines a normative target architecture. A requirement is not an implementation claim. Runtime conformance requires corresponding code, tests, evidence, operational procedures, and release validation.
