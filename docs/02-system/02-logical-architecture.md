<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-002",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "system_baseline",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/decision-index.json",
    "contracts/system.contract.json#/system",
    "contracts/system.contract.json#/principles",
    "contracts/system.contract.json#/operating_modes",
    "contracts/system.contract.json#/global_capabilities",
    "contracts/system.contract.json#/global_boundaries",
    "contracts/system.contract.json#/data_authority",
    "contracts/system.contract.json#/cross_component_communication",
    "contracts/system.contract.json#/ai_boundary",
    "contracts/system.contract.json#/offline_baseline",
    "contracts/system.contract.json#/degradation_baseline",
    "contracts/system.contract.json#/critical_transitions",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "contracts/architecture-patterns.contract.json",
    "02-system/34-architecture-patterns.md",
    "06-lifecycle/20-resilience-and-projection-artifacts.md",
    "08-operations/20-architecture-pattern-operations.md",
    "09-conformance/22-architecture-pattern-conformance.md",
    "contracts/subsystems/koa-spaces.subsystem.json",
    "02-system/21-koa-spaces-experience-layer.md",
    "02-system/22-koa-spaces-interface-composition.md"
  ],
  "decision_ids": [
    "DEC-AI-001",
    "DEC-SENT-001",
    "DEC-MEDIATHEQUE-001",
    "DEC-UCKK-EXT-001",
    "DEC-ARI-001",
    "DEC-PROFILE-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-GATE-001",
    "DEC-RES-001",
    "DEC-MSG-001",
    "DEC-WF-001",
    "DEC-PAYLOAD-001",
    "DEC-BFF-001",
    "DEC-CQRS-001",
    "DEC-CACHE-001"
  ],
  "requirement_ids": [
    "REQ-SYS-ARCH-001",
    "REQ-SYS-ARCH-002",
    "REQ-SYS-ARCH-003",
    "REQ-SYS-ARCH-004",
    "REQ-SYS-ARCH-005",
    "REQ-SYS-ARCH-006",
    "REQ-SYS-ARCH-007",
    "REQ-SYS-ARCH-008",
    "REQ-SYS-ARCH-009",
    "REQ-SYS-ARCH-010",
    "REQ-SYS-ARCH-011",
    "REQ-SYS-ARCH-012",
    "REQ-SYS-ARCH-013",
    "REQ-SYS-ARCH-014",
    "REQ-SYS-ARCH-015",
    "REQ-SYS-ARCH-016",
    "REQ-SYS-ARCH-017",
    "REQ-SYS-ARCH-018",
    "REQ-SYS-ARCH-019",
    "REQ-SYS-ARCH-020",
    "REQ-SYS-ARCH-021",
    "REQ-SYS-ARCH-022",
    "REQ-SYS-ARCH-023",
    "REQ-SYS-ARCH-024",
    "REQ-SYS-ARCH-025",
    "REQ-SYS-ARCH-026",
    "REQ-SYS-ARCH-027",
    "REQ-SYS-ARCH-028",
    "REQ-SYS-ARCH-029",
    "REQ-SYS-ARCH-030",
    "REQ-SYS-ARCH-031",
    "REQ-SYS-ARCH-032",
    "REQ-SYS-ARCH-033",
    "REQ-SYS-ARCH-034",
    "REQ-SYS-ARCH-035",
    "REQ-SYS-ARCH-036",
    "REQ-PATTERN-001",
    "REQ-PATTERN-002",
    "REQ-PATTERN-003",
    "REQ-PATTERN-004",
    "REQ-PATTERN-005"
  ],
  "lock_ids": [
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SENT-001",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-UCKK-EXT-001",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-PROFILE-001",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-003",
    "LOCK-UCKK-EXT-002",
    "LOCK-RES-001",
    "LOCK-MSG-001",
    "LOCK-WF-001",
    "LOCK-PAYLOAD-001",
    "LOCK-BFF-001",
    "LOCK-CQRS-001",
    "LOCK-CACHE-001",
    "LOCK-SPACES-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-002",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-CONST-009",
    "DOC-SYS-000",
    "DOC-SYS-001"
  ],
  "tags": [
    "system",
    "logical-architecture",
    "logical-planes",
    "component-boundaries",
    "offline-first",
    "external-ai-boundary",
    "data-authority",
    "safe-degradation",
    "profiles",
    "architecture-patterns",
    "koa-spaces",
    "experience-layer"
  ]
}
KOA:DOC-META:END -->

# Logical Architecture

## 1. Purpose

This document explains the global logical architecture of the kOA-Linux Operating System.

It defines how system responsibilities are separated into logical planes, how registered components participate in those planes, how data and authority move between components, how deployment profiles relate to the global baseline, and how the system preserves local operation when optional capabilities or external services are unavailable.

The architecture is designed to keep these distinctions explicit:

- global behavior versus profile-specific behavior;
- logical responsibility versus physical deployment;
- authoritative component state versus derived projections;
- runtime capability versus build workbench;
- resource control versus governance policy;
- local media ingestion versus external publication;
- local deterministic capability versus optional external AI;
- core operation versus optional enrichment;
- component contract versus implementation recipe.

This document is explanatory at the architecture level. Canonical identifiers, component records, profile membership, interfaces, requirements, locks, release channels, and integration definitions remain owned by their respective registries.

## 2. Scope

This document applies globally to:

- the kOA system baseline;
- user and developer operating modes;
- all active deployment profiles and overlays;
- all registered components and component contracts;
- cross-component communication;
- data-authority boundaries;
- local and external capability boundaries;
- offline operation;
- safe degradation;
- release and artifact activation;
- critical system transitions.

It defines logical responsibility and dependency.

It does not define:

- host count;
- process count;
- database product;
- database instance count;
- container runtime;
- orchestration technology;
- network implementation;
- operating-system service manager;
- desktop shell;
- file-system layout;
- port numbers;
- CPU or memory allocations;
- workspace layout;
- component-internal schemas or algorithms.

Those choices belong to profiles, toolchain contracts, component contracts, artifact contracts, security controls, operations contracts, or non-normative recipes.

## 3. Canonical References

| Canonical reference | Architectural ownership |
| --- | --- |
| `generated/decision-index.json` | Accepted choices that authorize global logical behavior |
| `contracts/system.contract.json#/system` | System identity, purpose, scope, product domains, logical planes, baseline profiles, and core properties |
| `contracts/system.contract.json#/principles` | Global system principles |
| `contracts/system.contract.json#/operating_modes` | User and developer mode definitions |
| `contracts/system.contract.json#/global_capabilities` | Capability identities, availability, dependencies, and failure behavior |
| `contracts/system.contract.json#/global_boundaries` | Component, data, trust, privilege, network, storage, AI, publication, and integration boundaries |
| `contracts/system.contract.json#/data_authority` | Global ownership and cross-domain mutation rules |
| `contracts/system.contract.json#/cross_component_communication` | Permitted and prohibited interaction mechanisms |
| `contracts/system.contract.json#/ai_boundary` | Native and external AI boundaries |
| `contracts/system.contract.json#/offline_baseline` | Required local operation |
| `contracts/system.contract.json#/degradation_baseline` | Capability-scoped failure behavior |
| `contracts/system.contract.json#/critical_transitions` | Transitions requiring explicit authority and receipts |
| `generated/component-catalog.json` | Component identities, classes, responsibilities, data ownership, and dependencies |
| `generated/component-catalog.json` | Active component-contract inventory |
| `contracts/components/*.component.json` | Observable interfaces, events, state, data boundaries, failures, and compatibility |
| `generated/profile-catalog.json` | Profile and overlay inventory |
| `contracts/profiles/*.profile.json` | Conditional placement, activation, isolation, resources, and topology |
| `contracts/release-channels.contract.json` | Independent release-channel identity and compatibility |
| `contracts/artifact-classes.contract.json` | Artifact classes, activation, rollback, and forward repair |
| `contracts/integration-types.contract.json` | External integration identity, classification, transfer, and authority boundary |
| `generated/requirements-index.json` | Normative statements and strength |
| `generated/assertion-index.json` | Cross-file alignment assertions |
| `generated/traceability.json` | Decision-to-requirement-to-lock-to-test-to-evidence relationships |
| `generated/exception-index.json` | Approved bounded deviations |

A component name in this document is a reference to the component registry. The descriptive grouping below does not create a component, interface, profile, or dependency.

## 4. Model and Responsibilities

### 4.1 Logical architecture versus deployment architecture

Logical architecture answers:

- what responsibility exists;
- which component owns it;
- what authority the component has;
- which inputs and outputs cross its boundary;
- what dependencies are mandatory or optional;
- what happens when a dependency is unavailable.

Deployment architecture answers:

- where the component runs;
- how it is packaged;
- what host, process, container, database, network, volume, secret, or service identity it uses;
- how much resource it receives;
- how it is activated and supervised.

The same logical architecture can support:

- a lightweight single-machine user profile;
- isolated developer workspaces;
- a sovereign Linux node;
- a sovereign hub;
- a build farm;
- a control plane;
- high-assurance and sovereign-offline overlays.

Physical consolidation does not merge logical authority.

Physical separation does not create new logical authority.

### 4.2 Logical planes

The planes below organize responsibility. They do not imply a required process boundary, network zone, database, container, host, or release channel.

| Logical plane | Primary responsibility | Principal registered components | Baseline relationship |
| --- | --- | --- | --- |
| Experience and interaction | Local user navigation, deterministic commands, accessibility, optional external voice | Ariane Runtime | Local navigation belongs to applicable user profiles; voice remains optional |
| Product and workflow | Independent product-domain state and user-directed operations | Konnaxion, Orgo | First-level domains with separate authority |
| Knowledge and language runtime | Local Kristal runtime state plus hosted SemantiK Architect generation capability | Kristal Runtime, SemantiK Architect integrated subsystem | Kristal and Architect retain their own semantics; kOA-Linux owns only declared local platform state |
| Media and dimension | Deterministic media ingestion, processing, storage, routing, export, backup, restore, and controlled UCKK publication | kOA Mediatheque, UCKK Publication Bridge | Native media path remains local and deterministic |
| Governance, identity, and accountability | Identity, trust, policy decisions, selective audit, controlled exceptions | Identity and Trust, Governance Policy Runtime, Audit Broker | Identity is global; policy runtime is profile-conditioned; audit is selective |
| Resource and node operation | Deterministic resource control and profile-authorized node operations | Resource Governor, kOA Node Agent | Resource Governor is baseline; host mutation depends on profile and privilege contracts |
| Publication and external boundary | Cross-domain disclosure, publication, external transfer, and integration mediation | Publication Gateway | Publication is explicit and governed |
| Optional workbenches | Build, research, enrichment, analysis, and controlled production of candidate or released artifacts | SemantiK Architect build/tooling profiles (including GF tooling where used), SenTient | Not part of the default user runtime; availability is profile-conditioned |

A component can interact with multiple planes while retaining one registered primary responsibility.

### 4.3 High-level component map

`text
External actors and optional services
 |
 | explicit user action or governed workflow
 v
+---------------------------------------------------------------+
| Publication and external boundary |
| Publication Gateway | registered external integrations |
+---------------------------+-----------------------------------+
 |
 | versioned contracts, artifacts,
 | receipts, governed transfers
 v
+--------------------+ +----------------------+ +-------------+
| Experience | | Product and workflow | | Media |
| Ariane Runtime | | Konnaxion | | kOA Mediatheque |
| local navigation | | Orgo | | Platform |
| optional voice | | separate authorities | | Dimension |
+----------+---------+ +-----------+----------+ | Gateway |
 | | +------+------+
 +------------------------+--------------------+
 |
 | contract-defined use
 v
 +-----------------------------------+
 | Knowledge and language runtime |
 | Kristal Runtime |
 | SemantiK Architect Runtime |
 +------------------+----------------+
 |
 released artifacts only in user runtime
 |
 +------------------v----------------+
 | Optional workbenches |
 | GF Wordbench | SenTient |
 +-----------------------------------+

Cross-cutting governed services:
 Identity and Trust
 Governance Policy Runtime
 Audit Broker
 Resource Governor
 kOA Node Agent

Cross-cutting rules:
 one owner per authoritative data domain
 no direct foreign source-state writes
 capability-scoped degradation
 native core without Internet or external AI
`

The arrows represent contract-defined interaction, not direct database access.

### 4.4 Experience and interaction plane

Ariane Runtime provides the local interaction layer for applicable profiles.

Local navigation includes deterministic capabilities such as:

- keyboard input;
- pointer input;
- touch input;
- menus;
- local shortcuts;
- deterministic commands;
- accessibility controls.

Local navigation remains available without external AI.

The external voice path is a separate optional capability. It can add voice interaction when the approved external path is available and explicitly enabled. Its failure removes only voice-dependent behavior.

Ariane does not become:

- an application data owner;
- an autonomous policy authority;
- an external AI authority;
- a universal workflow engine;
- a substitute for component contracts.

Ariane requests operations through the responsible component interfaces.

### 4.5 Product and workflow plane

Konnaxion and Orgo remain independent first-level domains.

Each domain has:

- a distinct component identity;
- a distinct responsibility;
- distinct authoritative data;
- a component contract;
- explicit dependencies;
- defined events and interfaces;
- independent failure behavior.

Neither domain becomes the implicit parent of every other system component.

System services such as Ariane, kOA Mediatheque, Kristal, language runtime, identity, policy, resource governance, publication, and audit remain first-class architectural responsibilities.

Cross-domain coordination occurs through registered interactions. One product domain does not write directly into another domain's authoritative storage.

### 4.6 Knowledge and language runtime plane

Kristal Runtime provides transversal epistemic capabilities.

Kristal identity remains derived from its canonical epistemic content and stays independent of:

- tenant workflow;
- user-interface state;
- transient orchestration state;
- component-specific operational records.

Kristal does not become a universal operational database or workflow engine.

SemantiK Architect Runtime provides released language behavior by consuming compiled artifacts.

The runtime does not compile grammars or perform workbench activity in user mode.

GF Wordbench belongs to the build and development side of the architecture. It creates or validates language artifacts under an applicable developer or build profile.

The runtime and workbench are separate because:

- runtime availability must not require build tooling;
- user profiles consume released artifacts;
- development dependencies remain isolated;
- build failure must not disable an already valid runtime artifact;
- artifact activation remains versioned and reversible or forward-repairable.

### 4.7 Mediatheque and learning-content plane

This plane contains the local kOA Mediatheque and the mappings used to exchange compatible objects with the online UCKK Mediatheque.

The kOA Mediatheque owns private local records, versions, storage bindings, hashes, metadata, dimensions, collections, relationships, rights, restrictions, provenance, renditions, local lifecycle, import history, export history, backup, and restore.

UCKK remains an external online Moodle platform that owns its courses, learning paths, activities, permissions, remote records, and UCKK Mediatheque lifecycle.

Both Mediatheques use the shared Mediatheque frame or compatible frame versions. The frame supports deterministic mapping of identity, versions, integrity, metadata, rights, provenance, manifests, and receipts. It does not create a common database or common authority.

Installed UCKK-derived learning packages become local kOA objects after validation and explicit acceptance. Their UCKK source identifiers remain provenance references.

### 4.8 Governance, identity, and accountability plane

Identity and Trust provides identity and verification capabilities used across the system.

Its responsibilities can include:

- component identity;
- user or actor identity;
- trust-root references;
- signature verification;
- credential and assertion validation;
- release or artifact identity verification.

Identity infrastructure enables decisions. It does not acquire ownership of each component's operational data.

Governance Policy Runtime evaluates governance-oriented decisions such as:

- authorization;
- disclosure;
- consent;
- privilege;
- governed exceptions.

It is present only where a profile requires the corresponding governance claim.

Audit Broker records selected accountable events and evidence according to active contracts.

Selective audit means:

- critical events are identifiable;
- evidence is attributable;
- disclosure remains bounded;
- audit does not require indiscriminate replication of all component data;
- the audit store does not become the universal source of operational truth.

### 4.9 Resource and node operation plane

Resource Governor manages deterministic resource behavior, including:

- CPU limits or priorities;
- memory limits;
- I/O limits or priorities;
- concurrency;
- queues;
- job scheduling;
- worker activation;
- process limits;
- resource-pressure degradation.

Resource decisions do not authorize disclosure, consent, privilege, or policy exceptions.

Governance Policy Runtime does not schedule CPU, allocate memory, or manage media-worker concurrency.

kOA Node Agent performs node-local operations permitted by its component contract and active profile.

Node-local operation can include:

- status reporting;
- lifecycle coordination;
- artifact staging;
- activation requests;
- health observation;
- profile-authorized host interaction.

Sensitive host mutation remains behind the applicable identity, policy, privilege, and evidence boundaries.

The existence of a node agent does not make every deployment an appliance or sovereign Linux node.

### 4.10 Publication and external interchange plane

This plane separates authorization from transport and separates outbound publication from inbound acquisition.

Outbound:

```text
source component or kOA Mediatheque
→ Publication Gateway disclosure authorization
→ UCKK Publication Bridge packaging and transport
→ UCKK acceptance
→ publication receipt
```

Inbound:

```text
UCKK selection
→ controlled retrieval
→ source, license, integrity, and compatibility validation
→ quarantine
→ kOA Mediatheque acceptance
→ import receipt and local provenance
```

The two directions do not share authority, queue state, retry policy, or conflict policy by implication. No direct UCKK database access or background bidirectional synchronization is allowed.

### 4.11 Optional workbench plane

GF Wordbench and SenTient are not baseline user-runtime services.

GF Wordbench is a designated language-build workbench.

SenTient is an optional isolated research and enrichment workbench.

SenTient is not:

- required for offline core operation;
- installed in the default user profile;
- always running;
- authoritative over canonical component data;
- allowed to mutate another component's source state directly;
- allowed to control host privilege;
- a replacement for native deterministic capabilities.

SenTient outputs remain candidate artifacts. Adoption occurs only through an authoritative component workflow.

A workbench can run locally or in a build environment when an active profile permits it. Workbench availability does not alter the global runtime baseline.

### 4.12 Cross-cutting data authority

Every authoritative data domain has one owner.

Components can share physical infrastructure under a profile while preserving:

- distinct component identities;
- distinct logical namespaces;
- separate mutation authority;
- explicit contracts;
- least-privilege access;
- recoverable ownership mapping.

Permitted cross-component mechanisms include:

- versioned APIs;
- commands;
- events;
- signed artifacts;
- user-authorized export and import;
- governed gateways.

Prohibited mechanisms include:

- direct writes to another component's authoritative source tables;
- undocumented shared mutable state;
- implicit privilege inheritance;
- unregistered external calls;
- authority created by implementation side effects.

Derived indexes, caches, projections, and read models remain subordinate to their authoritative sources.

### 4.13 Profiles and overlays

The global architecture defines responsibilities and boundaries.

Profiles define conditional deployment behavior.

Primary profiles include:

- `user_lightweight`;
- `developer_linux_workstation`;
- `developer_windows_wsl`;
- `sovereign_linux_node`;
- `sovereign_hub`;
- `build_farm`;
- `control_plane`.

Composable overlays include:

- `high_assurance`;
- `sovereign_offline`;
- `appliance_shell`.

A profile can determine:

- component inclusion;
- component activation;
- host placement;
- process placement;
- database topology;
- storage topology;
- network topology;
- isolation strength;
- privilege architecture;
- resource envelopes;
- offline envelope;
- release and recovery behavior.

A profile cannot silently:

- redefine a component;
- merge authorities;
- make an optional workbench global;
- add native AI to the baseline;
- bypass a gateway;
- authorize direct cross-component source-state writes;
- turn a recipe into system authority.

### 4.14 Operating modes

User mode prioritizes stable operation with released artifacts.

Its architecture favors:

- local capability;
- deterministic behavior;
- explicit activation;
- lightweight always-on services;
- task-activated heavy workers;
- no build tooling in the normal runtime;
- no requirement for SenTient;
- no requirement for external AI;
- graceful loss of optional external capability.

Developer mode permits isolated workbenches and mutable development state.

Its architecture adds:

- workspace identities;
- independent dependency environments;
- build tools;
- component-local services;
- test and validation tools;
- multiple parallel applications or branches;
- controlled publication of artifacts.

Developer convenience does not override component boundaries, data authority, security boundaries, or release validation.

### 4.15 Release and artifact relationship

The logical architecture is delivered through versioned artifacts.

Artifact classes can include:

- system images;
- service artifacts;
- governance policy bundles;
- Kristal artifacts;
- PGF and language runtime artifacts;
- Ariane artifacts;
- kOA Mediatheque and media artifacts;
- offline bundles;
- release sets;
- receipts and provenance records.

Artifacts can be versioned independently.

Independent versioning does not permit incompatible activation.

A release set binds versions that have been tested together across release channels.

Activation preserves one coherent authority state. A failed activation retains or restores the last valid state, or follows a declared forward-repair process when rollback is not safe.

### 4.16 Native, optional, and external capability classes

| Capability class | Meaning | Failure effect |
| --- | --- | --- |
| Native baseline | Implemented inside the governed local system and required by the applicable profile | The affected capability follows its declared fail-closed or degraded behavior |
| Profile-conditioned | Available only when selected by an active profile or overlay | Profiles that do not select it remain conformant |
| On-demand | Installed or activated only for an explicit task | Idle absence does not reduce baseline conformance |
| External optional | Uses a registered external service after explicit action or governed workflow | Only the external capability becomes unavailable |
| Workbench | Produces candidate or released artifacts in a development or build context | Existing valid runtime artifacts remain usable |
| Generated projection | Derived from canonical authority for humans or AI contexts | Stale projection blocks its use but does not replace the source |

External availability never creates authority by itself.

### 4.17 Dependency classes

A dependency is classified as one of:

| Dependency class | Meaning |
| --- | --- |
| Required runtime | The component cannot provide the declared capability without the dependency |
| Optional runtime | The component preserves its core responsibility when the dependency is absent |
| Build-time | Needed to produce or validate an artifact, not to consume the released artifact |
| Activation-time | Needed to verify or activate a release or artifact |
| Evidence-time | Needed to prove conformance or a critical transition |
| External optional | Outside the native core and removable without unrelated core failure |
| Profile-conditioned | Required only for profiles that make the corresponding claim |

A component contract declares its actual dependency class. Repeated implementation does not change the classification.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SYS-ARCH-001,REQ-SYS-ARCH-002,REQ-SYS-ARCH-003,REQ-SYS-ARCH-004,REQ-SYS-ARCH-005,REQ-SYS-ARCH-006,REQ-SYS-ARCH-007,REQ-SYS-ARCH-008,REQ-SYS-ARCH-009,REQ-SYS-ARCH-010,REQ-SYS-ARCH-011,REQ-SYS-ARCH-012,REQ-SYS-ARCH-013,REQ-SYS-ARCH-014,REQ-SYS-ARCH-015,REQ-SYS-ARCH-016,REQ-SYS-ARCH-017,REQ-SYS-ARCH-018,REQ-SYS-ARCH-019,REQ-SYS-ARCH-020,REQ-SYS-ARCH-021,REQ-SYS-ARCH-022,REQ-SYS-ARCH-023,REQ-SYS-ARCH-024,REQ-SYS-ARCH-025,REQ-SYS-ARCH-026,REQ-SYS-ARCH-027,REQ-SYS-ARCH-028,REQ-SYS-ARCH-029,REQ-SYS-ARCH-030,REQ-SYS-ARCH-031,REQ-SYS-ARCH-032,REQ-SYS-ARCH-033,REQ-SYS-ARCH-034,REQ-SYS-ARCH-035,REQ-SYS-ARCH-036 -->
- **REQ-SYS-ARCH-001 — SHALL:** The canonical global logical architecture be owned by `contracts/system.contract.json` and referenced rather than redefined by secondary documents.
- **REQ-SYS-ARCH-002 — SHALL:** Logical planes group responsibilities and interactions without defining process, host, network, storage, database, or container topology.
- **REQ-SYS-ARCH-003 — SHALL:** Every active component have one registered primary responsibility and explicit registered dependencies.
- **REQ-SYS-ARCH-004 — SHALL NOT:** Membership in a logical plane expand a component's authority beyond its active component contract.
- **REQ-SYS-ARCH-005 — SHALL NOT:** The global baseline require every registered component or workbench to be installed, active, or colocated.
- **REQ-SYS-ARCH-006 — SHALL:** Deployment profiles select, condition, isolate, and place components without redefining their global responsibilities.
- **REQ-SYS-ARCH-007 — SHALL:** User-mode runtime paths consume released or compiled artifacts and exclude build-only mutation of those artifacts.
- **REQ-SYS-ARCH-008 — SHALL:** Build workbenches and development tools remain separate from user runtime responsibilities.
- **REQ-SYS-ARCH-009 — SHALL:** Konnaxion and Orgo remain independent first-level domains with separate data authority and component contracts.
- **REQ-SYS-ARCH-010 — SHALL:** Kristal remain a transversal epistemic capability whose identity is independent of tenant workflow and interface state.
- **REQ-SYS-ARCH-011 — SHALL NOT:** Kristal become a universal workflow engine or universal operational database.
- **REQ-SYS-ARCH-012 — SHALL:** Ariane local navigation operate without Internet access or AI dependency in applicable user profiles.
- **REQ-SYS-ARCH-013 — SHALL:** Ariane external voice remain an optional external capability whose unavailability does not disable local navigation.
- **REQ-SYS-ARCH-014 — SHALL:** Native kOA Mediatheque ingestion, verification, routing, storage, export, backup, and restore remain deterministic and non-AI.
- **REQ-SYS-ARCH-015 — SHALL:** Suno and Gamma interactions remain explicit user-triggered external adapters outside the native kOA Mediatheque pipeline.
- **REQ-SYS-ARCH-016 — SHALL:** SenTient remain optional, isolated, non-authoritative, absent from the default user baseline, and unnecessary for offline core operation.
- **REQ-SYS-ARCH-017 — SHALL:** The Resource Governor control deterministic resource allocation, limits, queues, concurrency, and scheduling.
- **REQ-SYS-ARCH-018 — SHALL:** The Governance Policy Runtime control authorization, disclosure, consent, privilege decisions, and governed exceptions only where an active profile requires it.
- **REQ-SYS-ARCH-019 — SHALL NOT:** The Resource Governor and Governance Policy Runtime substitute for one another or merge their authority.
- **REQ-SYS-ARCH-020 — SHALL:** Identity and Trust provide registered identity, trust, signature, and verification services without acquiring component-owned operational data authority.
- **REQ-SYS-ARCH-021 — SHALL:** The Audit Broker record selected accountable events and evidence without becoming a universal operational data store.
- **REQ-SYS-ARCH-022 — SHALL:** The Publication Gateway mediate cross-domain disclosure, publication, and release to external audiences.
- **REQ-SYS-ARCH-023 — SHALL:** The UCKK Publication Bridge package and transport only Publication-Gateway-authorized representations to the online UCKK platform; the separate UCKK Import Bridge shall retrieve selected packages into quarantine and cannot bypass local acceptance.
- **REQ-SYS-ARCH-024 — SHALL NOT:** The UCKK Publication Bridge bypass or replace Publication Gateway authorization, or own local kOA Mediatheque state.
- **REQ-SYS-ARCH-025 — SHALL NOT:** A component write directly to another component's authoritative source tables or equivalent mutable source state.
- **REQ-SYS-ARCH-026 — SHALL:** Cross-component communication use active versioned APIs, commands, events, signed artifacts, user-authorized transfers, or governed gateways.
- **REQ-SYS-ARCH-027 — SHALL:** External AI outputs remain non-authoritative candidate inputs until validated and explicitly adopted by an authoritative component workflow.
- **REQ-SYS-ARCH-028 — SHALL:** The native core preserve its required local capabilities without Internet access or external AI.
- **REQ-SYS-ARCH-029 — SHALL:** Degradation be capability-scoped, preserve unaffected capabilities, and fail closed for unverifiable authority or prohibited mutation.
- **REQ-SYS-ARCH-030 — SHALL:** Critical activation, publication, disclosure, privilege, release, rollback, restore, policy, and migration transitions produce machine-readable receipts or evidence.
- **REQ-SYS-ARCH-031 — SHALL NOT:** A deployment profile generalize its implementation choices, topology, or assurance controls into global architecture.
- **REQ-SYS-ARCH-032 — SHALL:** Component contracts remain within the active system, profile, security, lifecycle, and data-authority boundaries.
- **REQ-SYS-ARCH-033 — SHALL NOT:** A recipe, deployment example, current implementation, or historical source redefine logical architecture.
- **REQ-SYS-ARCH-034 — SHALL:** Published runtime, service, policy, knowledge, language, Ariane, and media artifacts activate without partial authoritative state.
- **REQ-SYS-ARCH-035 — SHALL:** A release set bind tested compatible versions across independently versioned release channels.
- **REQ-SYS-ARCH-036 — SHALL:** A semantic change to planes, component responsibility, authority boundaries, mandatory dependencies, or interaction patterns use an accepted decision, impact report, complete validation, and atomic authority activation.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Registering a component in the logical architecture

1. Reference an accepted owner decision.
2. Assign a stable component identifier.
3. Define one primary responsibility.
4. Define authoritative data domains.
5. Define provided and consumed interfaces.
6. Define commands, events, artifacts, and critical transitions.
7. Define required, optional, build-time, activation-time, evidence-time, external, and profile-conditioned dependencies.
8. Assign a primary logical plane.
9. Confirm that the component does not overlap another component's authority.
10. Define profile availability and default activation outside the global component identity.
11. Add requirements and locks.
12. Add tests and evidence.
13. Compute direct and transitive impact.
14. Update the component registry and component contract.
15. Update explanatory documentation and generated catalogs.
16. Run complete validation.
17. Activate the updated authority set atomically.

A directory, process, service, package, container, or repository is not automatically a registered component.

### 6.2 Adding a cross-component interaction

1. Identify producer and consumer.
2. Identify source owner and destination owner.
3. Select a permitted interaction mechanism.
4. Define the versioned contract.
5. Define authorization and trust checks.
6. Define payload integrity and compatibility.
7. Define replay, ordering, idempotency, and deduplication.
8. Define failure ownership.
9. Define receipts or evidence where applicable.
10. Confirm that no direct foreign source-state write is introduced.
11. Add traceability.
12. Validate both components and all affected profiles.
13. Activate the interaction with the compatible component versions.

### 6.3 Adding an external integration

1. Register the integration identity and classification.
2. Define whether it is optional, user-triggered, or profile-conditioned.
3. Define transferred data and destination.
4. Define explicit authorization.
5. Define the external service's non-authoritative role.
6. Define native behavior when the service is unavailable.
7. Define adoption of returned candidate outputs.
8. Define provenance or receipts.
9. Add security and privacy review.
10. Add tests and evidence.
11. Validate that unrelated core capabilities remain available without the integration.

### 6.4 Activating a profile

1. Resolve the active global system registry.
2. Resolve the primary profile and overlays.
3. Resolve selected components and their contracts.
4. Resolve artifact and release-set compatibility.
5. Resolve identity, policy, privilege, resource, network, storage, and offline constraints.
6. Verify required dependencies.
7. Confirm that optional dependencies are not treated as mandatory.
8. Confirm data-owner uniqueness.
9. Confirm cross-component contract resolution.
10. Validate the complete profile instance.
11. Activate the profile as one compatible set.
12. Produce activation evidence.

### 6.5 Degrading a capability

1. Detect the failed or unavailable dependency.
2. Identify affected capabilities.
3. Evaluate the active degradation rule.
4. Block mutations whose authority cannot be verified.
5. Preserve unaffected component capabilities.
6. Preserve the last valid authoritative state.
7. Enter read-only or advisory behavior only when explicitly permitted.
8. Report the degraded state.
9. Record evidence required by the component or profile contract.
10. Restore normal behavior only after the dependency and authority checks pass.

### 6.6 Changing logical architecture

1. Create or reference an accepted owner decision.
2. Classify the semantic change.
3. Identify changed planes, components, authorities, dependencies, interfaces, profiles, artifacts, and generated projections.
4. Generate a complete impact report.
5. Update the canonical owner first.
6. Update affected component and profile contracts.
7. Update requirements, locks, tests, evidence, ADRs, and exceptions.
8. Define migration, compatibility, rollback, or forward repair.
9. Regenerate documents and AI contexts.
10. Validate the complete proposed release.
11. Update the authority registry last.
12. Activate atomically.

## 7. Failure States and Safe Degradation

| Failure condition | System response | Preserved behavior | Blocked behavior |
| --- | --- | --- | --- |
| Component contract is missing | Mark the component inactive and block dependent activation | Previously valid release | New component authority |
| Component responsibility overlaps | Report ownership collision and block both new claims | Previous non-conflicting owners | Overlapping authority |
| Required dependency is unavailable | Apply the component's declared degradation rule | Unaffected capabilities | Dependency-bound capability |
| Optional dependency is unavailable | Remove or disable only the optional capability | Native core and unrelated components | Optional capability |
| External AI is unavailable | Disable the external operation | Local deterministic operation | External AI capability |
| Ariane voice is unavailable | Disable voice interaction | Local navigation | Voice-dependent interaction |
| kOA Mediatheque external adapter is unavailable | Reject or defer the explicit external request | Native kOA Mediatheque pipeline | External adapter output |
| SenTient is unavailable | Omit the optional workbench | User runtime and native core | SenTient research activity |
| Resource Governor is unavailable | Block resource-sensitive activation according to profile policy | Last valid controlled state | Unbounded new work |
| Governance Policy Runtime is unavailable where required | Fail closed for governed authorization, disclosure, consent, or privilege | Unaffected non-governed local capability | Governed transition |
| Identity verification fails | Reject the affected trust-dependent operation | Unaffected verified sessions or local state | Unverified operation |
| Publication validation fails | Reject publication and preserve source state | Source-domain operation | External disclosure |
| UCKK publication fails | Preserve the local kOA Mediatheque record and prior receipts; report or queue the failed external publication | Existing local media domain | New external destination copy |
| Cross-component contract version is incompatible | Reject the interaction | Compatible local operations | Incompatible transfer |
| Direct foreign source write is detected | Reject and report a lock violation | Existing valid state | Prohibited mutation |
| Generated projection is stale | Block use of the projection and regenerate | Canonical registry authority | Stale generated guidance |
| Release-set compatibility fails | Block activation | Previous valid release | Mixed incompatible release |
| Validation tool cannot execute | Mark validation blocked | Previous valid authority | New activation |

Safe degradation never grants authority that the healthy system does not possess.

A cached response, derived projection, recipe, external output, or administrator privilege cannot become a substitute owner during failure.

## 8. Cross-Component Interactions

### 8.1 Interaction pattern

`text
initiating actor or component
 |
 | explicit request, command, event, or artifact
 v
 contract boundary
 |
 | identity + authorization + integrity
 | version + compatibility + replay rules
 v
 authoritative component
 |
 | accepted state transition
 v
 response, event, artifact, receipt, or failure
`

The receiving component owns the resulting state transition.

The initiating component owns its request and any state inside its own domain.

### 8.2 Experience-to-domain interaction

Ariane can translate deterministic local user actions into registered component requests.

Ariane does not write directly to product-domain storage.

The target component validates the request and owns the result.

### 8.3 Product-to-knowledge interaction

Konnaxion or Orgo can reference or request Kristal or language-runtime capabilities through registered contracts.

The product domain retains ownership of its workflow state.

Kristal retains ownership of epistemic identity and its canonical representation.

The language runtime interprets released artifacts without acquiring product-domain authority.

### 8.4 Product-to-media interaction

A product component can request or reference kOA Mediatheque operations through the kOA Mediatheque contract.

The product component does not mutate kOA Mediatheque storage directly.

kOA Mediatheque does not acquire ownership of the product component's workflow state merely because a media object is referenced.

### 8.5 User-to-UCKK interchange

For outbound publication, the user selects exact local versions and a destination. Publication Gateway authorizes disclosure before the UCKK Publication Bridge packages and transports the approved representation.

For inbound acquisition, the user selects an UCKK course, learning path, instruction set, or resource. The controlled import path verifies source, license, integrity, compatibility, and package completeness before the kOA Mediatheque may accept a local copy.

Neither operation is called `sync`. Each produces its own request, state, receipt, and reconciliation evidence.

### 8.6 Domain-to-publication interaction

A source component or user initiates a publication request.

Publication Gateway evaluates the intended disclosure, destination, authorization, policy, representation, and evidence requirements.

The source remains authoritative for its internal data.

Publication produces a governed external result, not shared internal ownership.

### 8.7 Component-to-resource interaction

Components declare resource needs and workload classes.

Resource Governor applies deterministic limits, priorities, concurrency, queues, and scheduling.

The Resource Governor does not decide whether data can be disclosed or privilege can be granted.

### 8.8 Component-to-policy interaction

A governed operation presents context to Governance Policy Runtime.

The policy runtime returns an authorization, disclosure, consent, privilege, or exception decision according to active policy.

The calling component remains responsible for applying the decision to its own operation and state.

### 8.9 Component-to-audit interaction

A component emits a contract-defined accountable event or evidence reference.

Audit Broker records only the selected data required by the audit contract.

Audit Broker does not copy all application state or become the owner of the originating domain.

### 8.10 Workbench-to-runtime interaction

A workbench produces a candidate artifact.

The artifact passes build, validation, compatibility, provenance, and release controls.

A compatible release set activates the artifact.

The runtime consumes the released artifact and does not depend on the workbench remaining online.

### 8.11 External AI interaction

A user explicitly initiates an approved external AI operation.

The integration boundary discloses only the declared data.

The returned output is a candidate input.

An authoritative component validates and explicitly adopts any result that will affect authoritative state.

No external AI output writes directly to canonical storage.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Accepted decisions

| Decision ID | Closed architectural choice |
| --- | --- |
| `DEC-AI-001` | No native AI dependency in the global baseline; approved external AI remains optional and non-authoritative |
| `DEC-SENT-001` | SenTient is an isolated optional research and enrichment workbench |
| `DEC-MEDIATHEQUE-001` | Native kOA Mediatheque media behavior is deterministic and local |
| `DEC-ARI-001` | Ariane local navigation is non-AI; external voice is optional |
| `DEC-PROFILE-001` | Primary profiles and overlays are explicit and machine-readable |
| `DEC-DATA-001` | Logical data ownership is mandatory and direct cross-component source writes are prohibited |
| `DEC-GOV-001` | Resource Governor and Governance Policy Runtime are separate authorities |
| `DEC-UCKK-EXT-001` | Publication Gateway authorization precedes UCKK-specific packaging and transport |

### 9.2 Protected locks

| Lock ID | Protected relationship |
| --- | --- |
| `LOCK-AI-001` | Native baseline excludes generative AI, classifiers, summarizers, embeddings, autonomous routing, and autonomous agents |
| `LOCK-AI-002` | External AI output cannot directly mutate authoritative state |
| `LOCK-SENT-001` | SenTient remains optional, isolated, non-authoritative, and outside the default user baseline |
| `LOCK-MEDIATHEQUE-001` | Native kOA Mediatheque behavior remains deterministic and non-AI |
| `LOCK-UCKK-EXT-002` | Inbound and outbound UCKK operations remain explicit, directional, and non-synchronizing |
| `LOCK-ARI-001` | Ariane local navigation works without AI |
| `LOCK-ARI-002` | External voice failure does not disable local navigation |
| `LOCK-DATA-001` | No direct write into another component's authoritative source state |
| `LOCK-GOV-001` | Resource Governor and Governance Policy Runtime remain separate |
| `LOCK-UCKK-EXT-001` | UCKK remains an external authority; UCKK publication transport cannot bypass Publication Gateway authorization or own local media |
| `LOCK-COMP-001` | Kristal identity remains independent of workflow and interface state |
| `LOCK-COMP-002` | User language runtime consumes compiled artifacts; build belongs to the workbench |
| `LOCK-PROFILE-001` | Profile-specific behavior does not become global |
| `LOCK-IMPL-001` | Recipes do not create architecture |
| `LOCK-IMPL-002` | systemd, Quadlet, Wayland, and no-GNOME remain profile-scoped implementation choices |
| `LOCK-LIFE-001` | Published artifacts do not activate partially |
| `LOCK-LIFE-003` | Release sets bind compatible versions across channels |

### 9.3 Prohibited assumptions

The following assumptions are invalid:

- a logical plane is a required host, process, database, container, or network;
- every component must be installed in every profile;
- every installed component must always run;
- Konnaxion or Orgo implicitly owns all system services;
- Kristal is a workflow engine or universal database;
- Ariane requires external AI for local navigation;
- external voice failure disables local navigation;
- kOA Mediatheque requires AI for native ingestion or routing;
- Suno or Gamma can be invoked silently by background media processing;
- SenTient belongs to the default user baseline;
- SenTient output is authoritative;
- Resource Governor can authorize disclosure or privilege;
- Governance Policy Runtime controls CPU, memory, or job queues;
- Publication Gateway and UCKK Publication Bridge are interchangeable;
- the kOA and UCKK Mediatheques share a database or authority because they share a frame;
- inbound and outbound UCKK operations imply continuous bidirectional synchronization;
- a shared database creates shared authority;
- a component can repair a failed interaction through a direct foreign database write;
- an administrator or root user becomes the product-data owner;
- a developer profile defines the global production architecture;
- a sovereign Linux recipe applies to Windows or lightweight profiles;
- a current implementation defines a mandatory dependency;
- a generated diagram creates component authority;
- an external integration is part of the core merely because it is configured;
- a build workbench must remain available for runtime use;
- a missing dependency has an obvious fallback;
- failure permits partial or inferred authority.

An unresolved component responsibility, authority boundary, profile condition, mandatory dependency, or failure behavior blocks activation of the affected object.

## 10. Validation Criteria

This document is conformant when all applicable checks pass.

1. The document is registered as `DOC-SYS-002` at `02-system/02-logical-architecture.md`.
2. Its class is `normative_markdown`, status is `active`, language is `en`, and scope is global.
3. Every metadata reference resolves.
4. Every requirement ID appears once in the generated requirement block.
5. Every rendered requirement matches the requirements registry.
6. Every decision is accepted and active.
7. Every lock is active and satisfied.
8. Every active component has one active component contract.
9. Every component has one registered primary responsibility.
10. Every logical-plane membership resolves to a registered component.
11. Logical-plane grouping does not create a deployment topology.
12. Profile contracts own inclusion, activation, placement, isolation, and resource behavior.
13. No profile rule is generalized into global architecture.
14. Konnaxion and Orgo remain separate component and data authorities.
15. Kristal identity remains independent of workflow and interface state.
16. User language runtime references compiled artifacts and not build-time mutation.
17. Ariane local navigation has no external AI dependency.
18. Ariane voice is optional and independently degradable.
19. Native kOA Mediatheque capabilities are deterministic and non-AI.
20. Suno and Gamma are explicit user-triggered external adapters.
21. SenTient is absent from the default user baseline and remains non-authoritative.
22. Resource Governor and Governance Policy Runtime have non-overlapping responsibilities.
23. UCKK publication requires Publication Gateway authorization followed by the distinct UCKK transport integration.
24. Every authoritative data domain has one owner.
25. No component has permission to mutate another component's authoritative source state directly.
26. Every cross-component interaction resolves to an active contract.
27. Every external integration declares transfer, authority, offline, and failure behavior.
28. External AI outputs require authoritative adoption before state mutation.
29. Offline baseline tests pass without Internet or external AI.
30. Degradation tests preserve unaffected capabilities and fail closed for authority-sensitive operations.
31. Critical transitions have receipt or evidence definitions.
32. Release-set compatibility prevents partial or mixed incompatible activation.
33. Generated component and architecture catalogs match canonical registries.
34. Traceability reaches applicable tests and evidence.
35. Exceptions are explicit, scoped, and active.
36. No unresolved architecture marker or unregistered dependency exists.
37. Complete validation runs against the exact proposed authority set.

Expected validation coverage includes:

`text
TEST-SYS-ARCH-001 Logical-plane component coverage
TEST-SYS-ARCH-002 Plane grouping does not define deployment topology
TEST-SYS-ARCH-003 Component responsibility uniqueness
TEST-SYS-ARCH-004 Component-contract coverage
TEST-SYS-ARCH-005 Profile and global-scope separation
TEST-SYS-ARCH-006 Konnaxion and Orgo authority separation
TEST-SYS-ARCH-007 Kristal transversal identity boundary
TEST-SYS-ARCH-008 Runtime and workbench separation
TEST-SYS-ARCH-009 Ariane local and external capability separation
TEST-SYS-ARCH-010 Deterministic native kOA Mediatheque behavior
TEST-SYS-ARCH-011 SenTient optional isolation
TEST-SYS-ARCH-012 Resource and policy authority separation
TEST-SYS-ARCH-013 Publication and UCKK publication bridge separation
TEST-SYS-ARCH-014 Direct foreign source-write rejection
TEST-SYS-ARCH-015 Cross-component contract resolution
TEST-SYS-ARCH-016 External AI authoritative-adoption boundary
TEST-SYS-ARCH-017 Offline core capability
TEST-SYS-ARCH-018 Capability-scoped degradation
TEST-SYS-ARCH-019 Critical-transition receipt coverage
TEST-SYS-ARCH-020 Release-set atomic compatibility
`

The test catalog and evidence registry own the executable tests and evidence definitions. This document does not claim that those tests have already run.

## 11. Non-Normative Examples

> **Non-normative example:** Each example illustrates one possible valid arrangement. It does not redefine canonical registries, contracts, profiles, or requirements.

### 11.1 Lightweight user deployment

One machine runs:

- Ariane Runtime;
- Konnaxion;
- Orgo;
- Kristal Runtime;
- SemantiK Architect Runtime;
- kOA Mediatheque;
- UCKK Publication Bridge;
- Resource Governor;
- required identity services.

Heavy media workers activate only for a task.

SenTient, GF Wordbench, build containers, and external AI services are absent.

A single database process can be used if component identities and logical namespaces remain separate.

This is one deployment of the logical architecture, not the definition of the architecture.

### 11.2 Developer workstation

A developer profile adds:

- isolated workspaces;
- GF Wordbench;
- build and test tools;
- component-local development services;
- optional SenTient;
- publication tooling.

Runtime services and build workbenches remain distinct.

Two workspaces can run concurrently because ports, processes, databases, volumes, secrets, and dependency environments are namespaced.

### 11.3 Sovereign node

A sovereign profile can deploy:

- separate service identities;
- stronger database and storage separation;
- Governance Policy Runtime;
- Audit Broker;
- kOA Node Agent;
- a narrow privileged path;
- offline bundles;
- signed release activation;
- recovery and rollback controls.

The stronger deployment does not make its Linux, systemd, Quadlet, Wayland, or appliance-shell choices global.

### 11.4 Ariane interaction

A user selects an Orgo operation through keyboard navigation.

Ariane invokes the registered Orgo interface.

Orgo validates and performs the operation.

Ariane presents the result.

No external AI is involved, and Ariane does not mutate Orgo storage directly.

### 11.5 Optional Ariane voice

A user explicitly enables the approved external voice path.

Voice input is transferred under the integration contract.

A deterministic local command is produced and handled through the same registered component interface as non-voice navigation.

When the external voice service is unavailable, keyboard, pointer, touch, menus, shortcuts, and accessibility controls remain available.

### 11.6 Native kOA Mediatheque and imported learning content

A user creates a private local instruction set and imports a verified UCKK course package.

The kOA Mediatheque creates separate local identities and versions, preserves the UCKK source and version as provenance for the imported package, and performs deterministic verification, storage, indexing, and preview generation.

No external AI is required. Neither local object is published automatically. A later publication request and a later remote-update import are separate governed operations.

### 11.7 SenTient enrichment

A developer exports an authorized artifact to an isolated SenTient workbench.

SenTient produces candidate enrichment output.

The output returns through a registered import path.

The authoritative component validates and adopts or rejects it.

SenTient never writes directly to the component database.

### 11.8 Resource pressure

kOA Mediatheque begins a large transcode.

Resource Governor limits concurrency and lowers I/O priority.

Ariane, Orgo, Konnaxion, and local navigation remain responsive.

Governance Policy Runtime is not involved because the event is a resource decision, not an authorization or disclosure decision.

### 11.9 UCKK publication and acquisition

An organization publishes an approved local training module to UCKK. Publication Gateway verifies disclosure authority, intended audience, representation, rights, and expiry. UCKK Publication Bridge packages and transports the approved representation and records the UCKK receipt.

Later, an isolated school acquires that UCKK module for offline use. The inbound path validates the package and the kOA Mediatheque accepts a distinct local copy. The two operations share provenance but not authority or lifecycle.

### 11.10 Invalid architecture shortcut

A recipe proposes that Orgo update a Konnaxion table directly because both components share one PostgreSQL process.

The arrangement is invalid.

Shared infrastructure does not merge authority, and a recipe cannot override the component and data boundaries.

## Pattern services and artifacts

Circuit runtimes, queue quarantine, workflow coordination, projection builders, caches, and experience adapters are logical support roles attached to owning components or integrations. They are not a new authority plane. Their behavior is defined by validated artifacts and the canonical architecture-pattern contract.

## Experience Layer in the Logical Architecture

The logical architecture includes an optional presentation plane implemented by kOA Spaces. This plane can aggregate non-authoritative views and navigation contributions, but it does not become a shared domain layer. View adapters, projections, and caches retain source identity and cannot replace authoritative query, command, policy, or storage boundaries.
