<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONST-013",
  "document_class": "explanatory_markdown",
  "status": "active",
  "language": "en",
  "layer": "constitution",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/terminology.contract.json",
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "generated/document-index.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/artifact-classes.contract.json",
    "contracts/release-channels.contract.json",
    "contracts/integration-types.contract.json",
    "contracts/integrations/uckk-import.integration.json",
    "contracts/artifact-contracts/shared-mediatheque-frame.schema.json",
    "contracts/subsystems/koa-spaces.subsystem.json",
    "02-system/21-koa-spaces-experience-layer.md",
    "02-system/22-koa-spaces-interface-composition.md"
  ],
  "decision_ids": [
    "DEC-DOC-001",
    "DEC-DOC-002",
    "DEC-DOC-003"
  ],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-DOC-002",
    "LOCK-DOC-003",
    "LOCK-DOC-008",
    "LOCK-DOC-009",
    "LOCK-DOC-014",
    "LOCK-DOC-016",
    "LOCK-DOC-019",
    "LOCK-DOC-021",
    "LOCK-DOC-022",
    "LOCK-PROFILE-001",
    "LOCK-IMPL-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-DATA-001",
    "LOCK-SPACES-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-016",
    "DOC-CONST-000",
    "DOC-CONST-001",
    "DOC-CONST-002"
  ],
  "tags": [
    "constitution",
    "glossary",
    "terminology",
    "canonical-vocabulary",
    "aliases",
    "identifiers",
    "ai-context",
    "koa-spaces",
    "experience-layer"
  ]
}
KOA:DOC-META:END -->

# kOA-Linux Glossary

## 1. Scope rule

Architecture terms are interpreted from an explicit scope.

The most important distinction is:

```text
kOA Digital Ecosystem
= the full operable system of systems

kOA-Linux Operating System
= the local sovereign operating-system / platform product
```

An independently owned system can therefore be:

```text
Konnaxion
= ecosystem system in the global ecosystem scope
= integrated subsystem from the kOA-Linux host scope
```

Both descriptions are valid because they answer different architectural questions. The host-relative `subsystem` classification does not transfer Konnaxion authority to kOA-Linux.

## 2. Core architecture terms

### kOA

The product-family and umbrella name.

Use **kOA Digital Ecosystem** when the full system-of-systems scope matters. Use **kOA-Linux Operating System** for the local operating-system product.

### kOA Digital Ecosystem

The operable kOA system of systems. It includes independently owned ecosystem systems, the kOA-Linux platform, applications, gateways, artifacts, and explicit integration boundaries.

The phrase **sociotechnical operating system** can describe this broader ecosystem when human roles, governance, institutions, and software are considered together. It does not identify a separate product.

### kOA-Linux Operating System

The sovereign local operating system that provides execution, isolation, trust, storage, recovery, offline operation, resource governance, verified activation, and controlled integration for kOA ecosystem workloads.

Accepted short form: `kOA-Linux`.

### ecosystem system

An independently owned system with significant domain authority and boundaries that remain its own when integrated by kOA-Linux.

Current examples relevant to this corpus include:

- Konnaxion;
- Orgo;
- Kristal;
- SemantiK Architect;
- kOA-Linux Operating System itself.

### integrated subsystem

A host-relative kOA-Linux classification for an independently owned ecosystem system mounted or operated through a declared subsystem boundary.

```text
integrated subsystem
≠ native component
≠ authority transfer
```

### subsystem

A coherent system boundary viewed from a containing/hosting scope. `kOA Spaces` is a native optional kOA-Linux subsystem. Konnaxion, Orgo, SemantiK Architect, Ariane, and SenTient can also be represented by subsystem contracts from the kOA-Linux host scope while retaining their own internal authority.

### component

A native first-class kOA-Linux architectural responsibility with explicit interfaces, owned platform state, failure behavior, and data boundaries.

Examples include:

- Identity and Trust;
- Resource Governor;
- Governance Policy Runtime;
- Audit Broker;
- Publication Gateway;
- kOA Node Agent;
- kOA Mediatheque;
- Kristal Runtime.

A subsystem contract for an external/independent ecosystem system is not converted into native component ownership merely because it is deployed on the same host.

### application / app

A bounded software or user-facing capability. An application can present or use a domain without being an ecosystem system.

### service

A deployed executable capability. Service is a deployment/execution concept; it does not automatically define data ownership.

### service instance

One running instance of a service/component capability.

### runtime

An execution boundary that loads or serves declared capabilities/artifacts. A runtime is not automatically the complete system whose artifacts it consumes.

### gateway

A controlled boundary for admission, publication, disclosure, import, transport, privilege, or another scoped transition. A gateway does not become owner of both sides of the boundary.

### module

A context-dependent convenience term, especially in UI/presentation language. It is not sufficient by itself as an architecture category.

In normative architecture prose, qualify it as one of:

```text
ecosystem system
subsystem
component
application
service
runtime
gateway
interface module
```

A `module interface manifest` is specifically a kOA Spaces presentation artifact. It does not define the complete authority model of the system/application contributing the interface.

## 3. System names

### Konnaxion

An independently owned ecosystem system for civic/public domain capabilities. In kOA-Linux it is integrated through `contracts/subsystems/konnaxion.subsystem.json`.

### Orgo

An independently owned ecosystem system for workflow and operational coordination. Its internal Organization/Case/Task/workflow model remains Orgo-owned. In kOA-Linux it is integrated through `contracts/subsystems/orgo.subsystem.json`.

### Kristal

One epistemic ecosystem system. `Kristal Specification`, `Kristal Core`, and `Kristal implementation` describe parts/layers of the same Kristal system rather than separate products.

### Kristal Runtime

The native kOA-Linux component that owns the local runtime boundary for verified Kristal artifacts: local verification records, compatibility state, active Runtime Pack selection, activation/rollback state, runtime status, and associated receipts.

```text
Kristal Runtime component
≠ Kristal ecosystem system
```

### SemantiK Architect

An independently owned planner-centered multilingual NLG ecosystem system.

Its internal architectural center is the planner/construction runtime, not a particular renderer:

```text
semantic input
→ normalization
→ planner
→ PlannedSentence
→ ConstructionPlan
→ lexical resolution
→ renderer backend
→ SurfaceResult
```

GF/PGF is a supported renderer/tooling family, not the architecture itself.

### SemantiK Architect runtime boundary

The host-local deployment/runtime boundary used by kOA-Linux for the SemantiK Architect subsystem. kOA-Linux can govern its process lifecycle, resources, storage/network exposure, artifact admission, health, backup coordination, and safe degradation without redefining Architect's internal runtime semantics.

### GF Wordbench

Optional GF-focused tooling within SemantiK Architect language-development workflows. It is not a separate ecosystem system and is not the universal source of Architect runtime truth.

### kOA Spaces

The optional, independently versioned, replaceable experience subsystem that composes navigation and interface contributions without owning business authority.

### kOA Mediatheque

The internal kOA-Linux component that owns deterministic local media records, managed storage references, integrity state, rights, provenance, transformations, export, backup, and restore state.

### UCKK

An external Moodle platform. It is not a native kOA-Linux subsystem. Publication to UCKK and import from UCKK are separate directional integrations.

## 4. Authority and state

### owner

The system/component responsible for the semantics and authorized mutation of a state/object in a declared scope.

### authoritative state

State accepted and owned by the responsible domain owner.

### source of truth

The authoritative source for one explicitly scoped fact or object. Do not use the phrase to imply that one component owns every domain in the ecosystem.

### candidate input

External/generated/imported material not yet accepted as authoritative state by the receiving owner.

### projection / controlled read model

Derived state optimized for reading, search, analytics, UI, or integration. It does not become source authority merely because it is cached or materialized.

### receipt

Structured evidence of acceptance, rejection, activation, rollback, publication, privilege, restore, or another transition. A receipt is evidence, not the authoritative state it reports.

## 5. Interaction terms

### command

A request that the receiving owner consider and perform a mutation. The sender does not gain write authority over the receiver.

### query

A request for a read/projection without implicit mutation or ownership transfer.

### event

A fact already committed by the publisher. A consumer decides how that event affects only its own state.

### artifact

A typed versioned/identifiable object transported across a boundary. Artifact integrity and authorization/activation are separate decisions.

### Runtime Pack

A runtime-ready package class. Kristal defines Kristal Runtime Pack semantics in the Kristal system; kOA-Linux defines its own local admission/activation contract around such artifacts. The Kristal manifest discriminator and kOA-Linux artifact classification remain scoped fields, not competing universal enums.

### language pack

A kOA-Linux artifact-boundary package for SemantiK Architect runtime assets. It can contain one or more declared backend/resource families. A GF/PGF-backed pack is one supported profile, not the only possible Architect architecture.

## 6. Profile and deployment terms

### deployment profile

A complete deployable kOA-Linux identity selecting and constraining the global baseline.

### profile overlay

A composable strengthening/restriction applied to a primary profile. It is not independently deployable.

### operating mode

A mode of system activity such as interactive user, development, build, service node, hub, control plane, or recovery. It is not a deployment profile.

### workspace

A complete development isolation unit. A Git worktree can host a workspace, but the two concepts are not identical.

## 7. kOA Spaces terms

### Space

A user-facing presentation arrangement selecting, ordering, labeling, and configuring available interface modules for a declared context.

### Space definition

The validated presentation artifact that defines a Space. It does not grant business authority.

### module interface manifest

A contributor-owned presentation manifest describing routes, navigation, top-bar widgets, public labels, capability visibility, accessibility metadata, and offline presentation behavior.

### module selector

The kOA Spaces control for switching among visible/permitted interface contributions. Menu visibility is not authorization.

## 8. Required distinctions

```text
kOA Digital Ecosystem ≠ kOA-Linux Operating System

ecosystem system ≠ native component
integrated subsystem ≠ authority transfer
component ≠ service instance
module ≠ ownership category
application ≠ ecosystem system by default

Kristal ≠ Kristal Runtime component
Kristal artifact integrity ≠ authority to activate
artifact verification ≠ activation
resource grant ≠ authorization
receipt ≠ active state

SemantiK Architect ≠ GF
planner ≠ renderer
ConstructionPlan ≠ public response
language pack ≠ necessarily PGF-only

kOA Spaces route/menu ≠ business authorization
projection/cache ≠ authoritative state
```

Canonical machine vocabulary remains owned by `contracts/terminology.contract.json`.
