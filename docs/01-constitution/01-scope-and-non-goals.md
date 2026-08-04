<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONST-001",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "constitution",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/system.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json"
  ],
  "decision_ids": [
    "DEC-AI-001",
    "DEC-ARI-001",
    "DEC-CONTAINER-001",
    "DEC-DATA-001",
    "DEC-GATE-001",
    "DEC-GOV-001",
    "DEC-HW-001",
    "DEC-K8S-001",
    "DEC-PROFILE-001",
    "DEC-REL-001",
    "DEC-SENT-001",
    "DEC-SHELL-001",
    "DEC-UCKK-001"
  ],
  "requirement_ids": [
    "REQ-CONST-SCOPE-001",
    "REQ-CONST-SCOPE-002",
    "REQ-CONST-SCOPE-003",
    "REQ-CONST-SCOPE-004",
    "REQ-CONST-SCOPE-005",
    "REQ-CONST-SCOPE-006",
    "REQ-CONST-SCOPE-007",
    "REQ-CONST-SCOPE-008",
    "REQ-CONST-SCOPE-009",
    "REQ-CONST-SCOPE-010",
    "REQ-CONST-SCOPE-011",
    "REQ-CONST-SCOPE-012",
    "REQ-CONST-SCOPE-013",
    "REQ-CONST-SCOPE-014",
    "REQ-CONST-SCOPE-015",
    "REQ-CONST-SCOPE-016",
    "REQ-CONST-SCOPE-017",
    "REQ-CONST-SCOPE-018",
    "REQ-CONST-SCOPE-019",
    "REQ-CONST-SCOPE-020"
  ],
  "lock_ids": [
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-DATA-001",
    "LOCK-GATE-001",
    "LOCK-GOV-001",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-SENT-001",
    "LOCK-UCKK-001",
    "LOCK-UCKK-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-CONST-000"
  ],
  "tags": [
    "constitution",
    "scope",
    "non-goals",
    "global-baseline",
    "profile-boundaries",
    "offline",
    "ai-boundary"
  ]
}
KOA:DOC-META:END -->

# Scope and Non-Goals

## 1. Purpose

This document defines the constitutional boundary of the kOA operating environment. It explains what belongs to the global system baseline, what belongs only to a named conditional scope, and what the project deliberately does not attempt to make universal.

The document exists to prevent scope inflation. It keeps optional tools, deployment choices, historical implementation patterns, external services, and profile-specific controls from silently becoming global requirements.

The canonical system model is owned by `contracts/system.contract.json`. Normative statements are owned by `generated/requirements-index.json`, and cross-file scope protections are owned by `generated/assertion-index.json`. This document explains how those sources apply together.

The deterministic outcome is a clear answer to each of these questions:

- Is a capability part of the global baseline?
- Is it conditional on a profile, overlay, component, artifact class, or toolchain?
- Is it optional or external?
- Is it an implementation choice rather than a system guarantee?
- Is it outside current active authority?

## 2. Scope

### 2.1 Global scope of this document

This document applies globally to the active kOA documentation and architecture. It governs the classification of system capabilities, deployment obligations, component responsibilities, optional integrations, development facilities, lifecycle mechanisms, and implementation choices.

It applies to:

- the common kOA operating baseline;
- user and developer operating modes;
- primary deployment profiles and composable overlays;
- first-class components and their authority boundaries;
- local and offline operation;
- external integration boundaries;
- release and artifact compatibility boundaries;
- development workspaces and toolchain isolation;
- conformance claims that depend on correct scope classification.

### 2.2 Scope classes

The recognized scope classes are:

| Scope class | Meaning |
| --- | --- |
| `global` | Applies across every active deployment unless a more restrictive active rule controls a specific capability. |
| `profile` | Applies only to one named primary deployment profile. |
| `profile_overlay` | Applies only when the named overlay is explicitly composed with a compatible primary profile. |
| `component` | Applies only inside the named component’s canonical responsibility and authority boundary. |
| `artifact_class` | Applies only to artifacts of the named canonical class. |
| `development_toolchain` | Applies only to the named development or build toolchain. |
| `migration_only` | Governs lineage and disposition without defining current product behavior. |

A profile rule does not become global because several profiles use it. An overlay does not apply until explicitly composed. A component rule does not control another component. A migration rule does not define current runtime behavior.

### 2.3 Included system outcomes

The kOA scope includes a governed operating environment that can:

- support stable daily user operation;
- support isolated development and build activity;
- operate locally and continue defined core capabilities without Internet access;
- run a common deterministic baseline without native AI;
- activate optional capabilities only through explicit scope and authority;
- keep component data ownership and interfaces explicit;
- manage resource use deterministically;
- produce, verify, activate, roll back, restore, export, and retire governed artifacts;
- support profile-specific sovereignty, security, assurance, and appliance behavior without imposing those choices globally;
- provide traceable validation and conformance evidence.

### 2.4 Conditional scope

The following are conditional rather than universal:

- sovereign host controls;
- immutable signed operating-system images;
- measured or verified boot;
- a narrow privileged broker;
- rootless Podman and Quadlet;
- a minimal Wayland appliance shell;
- Kubernetes control-plane deployment;
- high-assurance controls;
- fully offline overlays;
- build-farm services;
- development workbenches;
- external AI surfaces;
- SenTient;
- external voice for Ariane.

Their exact applicability is owned by the corresponding profile, overlay, component, integration, artifact, or toolchain contract.

### 2.5 Explicit non-goals

The global kOA baseline is not intended to be:

- a mandatory cloud service;
- an Internet-dependent platform;
- a native generative-AI platform;
- an autonomous agent system;
- a universal AI classifier, summarizer, embedding service, or routing engine;
- a single monolithic application with one undifferentiated data authority;
- a system in which every component or workbench runs continuously;
- a universal Linux distribution requirement for every deployment and developer host;
- a mandate for one desktop environment, service manager, container runtime, or orchestration platform;
- a requirement to use Kubernetes on user or developer endpoints;
- a requirement to deploy sovereign or high-assurance controls in profiles that do not claim them;
- an authorization for direct cross-component database writes;
- an authorization for optional integrations to become core dependencies;
- an authorization for external AI output to become system authority;
- a replacement for the internal responsibility of each first-class component;
- a mechanism for treating recipes, examples, or current implementations as architecture by repetition;
- an active home for undecided future capabilities.

These non-goals limit the baseline. They do not prohibit a compatible profile or integration from implementing a bounded capability after its authority, scope, contracts, validation, and failure behavior are explicit.

## 3. Canonical References

| Canonical reference | Responsibility in this document |
| --- | --- |
| `contracts/system.contract.json` | Owns the global system model, operating modes, global capabilities, AI boundary, offline baseline, profile-independent boundaries, and safe-degradation baseline. |
| `generated/requirements-index.json` | Owns the normative statements selected and rendered in Section 5. |
| `generated/assertion-index.json` | Owns the cross-file assertions that prevent profile promotion, optional-capability promotion, component-boundary violations, and conflicting scope representations. |

Related active decisions are identified in the generated metadata block. Their canonical records belong to `generated/decision-index.json`; this document does not duplicate their lifecycle or ownership data.

## 4. Model and Responsibilities

### 4.1 Global baseline

The global baseline is the smallest common set of architectural guarantees shared across active kOA deployment profiles. It defines behavior that remains true regardless of host implementation details.

The baseline includes:

- explicit authority and fail-closed resolution;
- local and offline-capable core operation;
- no native AI dependency;
- deterministic resource governance;
- explicit component separation;
- explicit logical data ownership;
- controlled cross-component interaction;
- safe degradation by capability;
- verifiable artifact and release identity;
- portability, restoration, and credible exit;
- selective audit and controlled evidence.

The baseline does not select a universal host topology, desktop shell, container runtime, service manager, storage topology, or cluster orchestrator.

### 4.2 Profiles and overlays

Primary profiles define complete deployment forms. Overlays add compatible conditional guarantees without replacing the primary profile identity.

The primary profile set is:

- `user_lightweight`;
- `developer_linux_workstation`;
- `developer_windows_wsl`;
- `sovereign_linux_node`;
- `sovereign_hub`;
- `build_farm`;
- `control_plane`.

The composable overlay set is:

- `high_assurance`;
- `sovereign_offline`;
- `appliance_shell`.

Profile inheritance and overlay composition are explicit and machine-readable. Similar implementations do not imply inheritance.

### 4.3 User and developer boundaries

User operation consumes verified runtime artifacts and favors stable, bounded resource use. Development operation enables selected workbenches for modification, compilation, testing, migration, and publication.

The user baseline does not include every development compiler, research workbench, build service, search engine, or heavy processing stack. Development mode does not require all workbenches to run together.

### 4.4 AI and external-service boundary

The native baseline does not include generative AI, classification models, summarization models, embedding models, autonomous agents, or AI-based routing authority.

Approved external surfaces are optional, user-triggered, capability-scoped, removable, and unable to write directly to authoritative stores. ChatGPT, Suno, Gamma, and the approved Ariane voice adapter remain external surfaces rather than native baseline capabilities.

External outputs remain candidate inputs until a responsible component accepts them through a controlled workflow.

### 4.5 SenTient boundary

SenTient is an optional isolated research and enrichment workbench. It is not part of the default user-lightweight baseline, not always active, not an authority over canonical data, and not required for offline core operation.

Its dependencies, storage, service identity, temporary data, network access, and resource use remain isolated. Its outputs require provenance, review, controlled import, and component-level acceptance.

### 4.6 UCKK boundary

The native UCKK pipeline is deterministic and local. Its baseline responsibilities include controlled ingestion, integrity verification where the artifact contract requires it, user-supplied metadata, deterministic media processing, storage, export, backup, and restoration.

Native UCKK behavior does not include AI classification, AI summarization, AI-generated categories, AI routing, AI tagging, AI transcription, AI translation, or AI content generation.

Suno and Gamma are optional external adapters. They are not automatic ingestion or routing dependencies.

### 4.7 Ariane boundary

Ariane local navigation is independent of external AI and voice availability. Keyboard, pointer, touch, menus, deterministic commands, accessibility controls, and local shortcuts remain local capabilities.

External voice is an optional input path. Its absence disables voice input only; it does not disable Ariane local navigation or unrelated core capabilities.

### 4.8 Component and data-authority boundary

Each first-class component owns a bounded responsibility and authoritative data domain. Components interact through explicit contracts, gateways, events, artifacts, or approved service interfaces.

A shared physical database process may be permitted by a lightweight profile, but logical ownership remains separate. Physical consolidation does not grant cross-component write authority.

Resource Governor controls deterministic resource allocation and scheduling. Governance Policy Runtime controls authorization, disclosure, consent, privilege, and governed exceptions in profiles that deploy it. Neither authority substitutes for the other.

Publication Gateway controls cross-domain disclosure and publication. UCKK Dimension Gateway controls user-selected media transfer and admission into UCKK. Neither contract substitutes for the other.

### 4.9 Implementation boundary

Implementation recipes may describe systemd, Quadlet, Podman, Docker, Wayland, desktop environments, Kubernetes, storage layouts, and network layouts. Those choices remain non-normative unless adopted by an active profile or toolchain contract.

A working implementation proves feasibility. It does not independently define system scope.

### 4.10 Release boundary

The system, services, governance, and knowledge channels have independent identities. A Release Set expresses tested compatibility across them.

Matching version numbers, recency, or co-installation do not prove compatibility. Optional independent updates remain bounded by declared compatibility constraints.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-CONST-SCOPE-001,REQ-CONST-SCOPE-002,REQ-CONST-SCOPE-003,REQ-CONST-SCOPE-004,REQ-CONST-SCOPE-005,REQ-CONST-SCOPE-006,REQ-CONST-SCOPE-007,REQ-CONST-SCOPE-008,REQ-CONST-SCOPE-009,REQ-CONST-SCOPE-010,REQ-CONST-SCOPE-011,REQ-CONST-SCOPE-012,REQ-CONST-SCOPE-013,REQ-CONST-SCOPE-014,REQ-CONST-SCOPE-015,REQ-CONST-SCOPE-016,REQ-CONST-SCOPE-017,REQ-CONST-SCOPE-018,REQ-CONST-SCOPE-019,REQ-CONST-SCOPE-020 -->
- **REQ-CONST-SCOPE-001 — SHALL:** The kOA global baseline provide governed local operation without requiring Internet access or native AI.
- **REQ-CONST-SCOPE-002 — SHALL:** A global rule apply across active profiles only when its canonical owner declares global scope.
- **REQ-CONST-SCOPE-003 — SHALL:** Every conditional capability or requirement be assigned to an explicit profile, profile overlay, component, artifact class, or development toolchain scope.
- **REQ-CONST-SCOPE-004 — SHALL NOT:** A profile-specific or implementation-specific rule become global through repetition, historical use, or implementation prevalence.
- **REQ-CONST-SCOPE-005 — SHALL NOT:** The global baseline require every component, optional workbench, or development environment to be active simultaneously.
- **REQ-CONST-SCOPE-006 — SHALL:** Core user operation remain available without any external AI surface.
- **REQ-CONST-SCOPE-007 — SHALL NOT:** An external AI output directly mutate authoritative component state or become authoritative without explicit acceptance.
- **REQ-CONST-SCOPE-008 — SHALL:** SenTient remain optional, isolated, non-authoritative, and absent from the default user-lightweight baseline.
- **REQ-CONST-SCOPE-009 — SHALL:** Native UCKK ingestion, routing, metadata handling, and deterministic media processing operate without AI.
- **REQ-CONST-SCOPE-010 — SHALL:** Ariane local navigation remain available when the optional external voice capability is unavailable.
- **REQ-CONST-SCOPE-011 — SHALL:** Every component retain explicit logical ownership of its authoritative data.
- **REQ-CONST-SCOPE-012 — SHALL NOT:** A component write directly to another component’s authoritative source tables.
- **REQ-CONST-SCOPE-013 — SHALL:** Resource Governor and Governance Policy Runtime remain separate authorities with non-overlapping canonical responsibilities.
- **REQ-CONST-SCOPE-014 — SHALL:** Publication Gateway and UCKK Dimension Gateway remain separate contracts with distinct disclosure and ingestion responsibilities.
- **REQ-CONST-SCOPE-015 — SHALL NOT:** Kubernetes be required by a single-node user or developer endpoint baseline.
- **REQ-CONST-SCOPE-016 — SHALL NOT:** A specific desktop shell, service manager, container runtime, or host layout become a global requirement unless an accepted global decision activates it.
- **REQ-CONST-SCOPE-017 — SHALL:** Failure or removal of an optional integration leave unrelated core capabilities operational.
- **REQ-CONST-SCOPE-018 — SHALL:** A scope promotion or scope expansion require an accepted owner decision, transitive impact analysis, canonical registry updates, and validation.
- **REQ-CONST-SCOPE-019 — SHALL NOT:** A proposed, future, experimental, migration-only, or unregistered capability be represented as active baseline behavior.
- **REQ-CONST-SCOPE-020 — SHALL:** Authority resolution fail closed when a capability’s owner, scope, decision status, or applicable profile cannot be determined.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Scope classification workflow

The canonical classification workflow for a new or changed capability is:

1. Identify the capability, behavior, guarantee, implementation choice, or constraint being classified.
2. Identify its exclusive canonical owner.
3. Determine whether the fact is global or conditional.
4. For a conditional fact, identify the exact profile, overlay, component, artifact class, or toolchain.
5. Identify the accepted owner decision that authorizes the classification.
6. Record the fact in the owning registry or contract.
7. Connect applicable requirements and Interfile Alignment Locks.
8. Compute direct and transitive impact.
9. Update explanatory documents without copying canonical ownership.
10. Update tests, evidence, generated projections, and AI contexts.
11. Run complete validation.
12. Activate the resulting authority release only after validation passes.

A missing owner, missing decision, ambiguous scope, or unresolved conflict stops the workflow before activation.

### 6.2 Global-scope promotion

Promotion from a conditional scope to global scope is a major semantic change. Its review includes:

- the reason the property must apply to every profile;
- compatibility with lightweight, developer, sovereign, build, and control-plane profiles;
- offline and degraded-operation consequences;
- component and data-authority consequences;
- resource-envelope consequences;
- release, migration, security, and conformance impact;
- replacement or preservation of existing profile-scoped rules.

The previous conditional rule remains authoritative until the replacement authority release activates.

### 6.3 Optional-capability admission

An optional capability enters an applicable profile only after its capability boundary, dependencies, data movement, authority limitations, resource envelope, failure behavior, uninstallability, validation, and evidence are explicit.

Optional admission does not alter the global baseline unless a separate global-scope decision is accepted and activated.

### 6.4 Removal from scope

Removing a capability or guarantee follows impact-controlled deprecation or supersession. Historical identifiers remain reserved, affected profiles and components receive an explicit disposition, and existing artifacts receive a compatibility or migration path where required.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Authority retained | Authority denied | Evidence |
| --- | --- | --- | --- | --- |
| Canonical owner cannot be identified | Block activation and report the missing ownership boundary. | Previously active authority | New or changed capability | Ownership validation result |
| Scope is ambiguous | Block activation and report the conflicting candidate scopes. | Existing scoped behavior | Scope promotion or inheritance | Scope-validation result |
| Required owner decision is absent or not accepted | Keep the dependent object inactive. | Existing active release | Proposed behavior | Decision-closure result |
| Profile contract is unavailable or invalid | Do not claim or activate that profile. | Global baseline where independently valid | Profile-specific guarantees | Profile validation result |
| Optional integration is unavailable | Disable only the dependent optional capability. | Unrelated local core capabilities | Integration-dependent operation | Health and capability status |
| Internet access is unavailable | Continue declared offline-capable behavior. | Local data and local runtime authority | Internet-dependent optional operations | Offline conformance evidence |
| External AI surface is unavailable | Preserve native operation and deny the external operation. | Local deterministic authority | External AI-dependent output | Integration status or receipt |
| Ariane external voice is unavailable | Preserve local navigation and expose voice as unavailable. | Local Ariane navigation | Voice input | Capability status |
| SenTient is absent, stopped, or fails | Preserve core user operation and deny SenTient work. | Core runtime authority | SenTient research operation | Workbench health record |
| Cross-component direct-write attempt occurs | Deny the write and preserve owner boundaries. | Owning component authority | Unauthorized mutation | Security or database access evidence |
| Release Set is incomplete or incompatible | Block activation. | Previously active compatible Release Set | Candidate release activation | Release-validation evidence |
| Implementation recipe conflicts with an active profile | Ignore the recipe as authority and block non-conformant activation. | Active profile contract | Recipe-derived override | Profile and lock validation |

Safe degradation never creates new authority, silently substitutes a different external service, promotes optional behavior, or weakens a component boundary.

## 8. Cross-Component Interactions

### 8.1 Interaction rule

Cross-component interaction is contract-driven. Every interaction identifies a producer, consumer, direction, interface or artifact, trust boundary, data owner, failure behavior, and applicable evidence.

A consumer receives only the authority granted by the interaction contract. Receiving data does not transfer ownership of the producer’s authoritative store.

### 8.2 Resource governance

Components declare resource needs and work classes to Resource Governor. Resource Governor may schedule, throttle, queue, suspend, or stop work within active resource policy. It does not decide disclosure, consent, privilege, semantic truth, or component data ownership.

### 8.3 Governance policy

Where a profile deploys Governance Policy Runtime, governed authorization precedes privileged or disclosure-sensitive action. Governance Policy Runtime does not allocate CPU, memory, I/O, or job concurrency.

### 8.4 Publication and ingestion gateways

Publication Gateway mediates outward or cross-domain disclosure. UCKK Dimension Gateway mediates user-selected transfer into UCKK. Data crossing either boundary retains explicit provenance and acceptance state.

### 8.5 External services

An external service interaction is initiated through its approved integration boundary. The user-visible operation identifies the external surface and transferred data. The external service cannot directly access or mutate authoritative component storage.

### 8.6 Development workspaces

Development workspaces isolate mutable dependencies, services, ports, databases, secrets, temporary data, and process identities. Shared immutable caches do not transfer mutable authority between workspaces.

## 9. Decision Closure and Prohibited Assumptions

The architecture decisions referenced in the metadata close the scope questions addressed by this document.

The following assumptions are prohibited:

1. Every useful feature belongs in the global baseline.
2. A historically deployed Linux control applies to Windows, lightweight, or developer profiles.
3. An optional integration becomes core because many users enable it.
4. External AI is native because the interface is presented inside a kOA workflow.
5. SenTient belongs to the default user installation.
6. UCKK ingestion performs AI analysis because optional external media tools exist.
7. Ariane requires voice or AI to provide navigation.
8. Physical database consolidation permits cross-component writes.
9. Resource Governor and Governance Policy Runtime are interchangeable.
10. Publication Gateway and UCKK Dimension Gateway are interchangeable.
11. A container runtime is a deployment profile.
12. Kubernetes is required because it is permitted in control-plane or build profiles.
13. A recipe defines architecture because it works in one deployment.
14. An absent rule has an obvious default scope.
15. A future capability is active because its path appears in the target documentation inventory.
16. A generated context package is complete authority beyond its declared scope.

When a requested behavior depends on a fact not owned by active authority, the result is blocked until an accepted decision and canonical representation exist.

## 10. Validation Criteria

This document is conformant when all of the following checks pass:

1. The file is registered as `DOC-CONST-001` at `01-constitution/01-scope-and-non-goals.md`.
2. The document class is `normative_markdown`, status is `active`, language is `en`, layer is `constitution`, and scope is `global`.
3. The metadata matches `generated/document-index.json`.
4. Every canonical reference resolves.
5. Every listed decision exists with accepted status before this document participates in active authority.
6. Every listed requirement exists with the exact rendered text, strength, scope, owner, source decision, lock mapping, and validation method.
7. Every listed lock exists and its applicable assertions pass.
8. The document contains all eleven mandatory sections in the required order.
9. Normative keywords appear only in the generated requirements block.
10. The document does not duplicate canonical enums or defaults owned by another registry.
11. No profile-specific requirement is represented as global.
12. No recipe or implementation choice is represented as universal architecture.
13. Optional external services are not represented as native or required.
14. SenTient is not represented as default, authoritative, always active, or required for offline core operation.
15. Native UCKK behavior is represented as deterministic and non-AI.
16. Ariane local navigation is represented as independent of external voice availability.
17. Direct cross-component writes are prohibited.
18. Conditional scope and overlay composition remain explicit.
19. The dependency graph remains acyclic.
20. No unresolved marker, provisional decision marker, temporary default, or parallel authority appears.
21. Complete documentation validation returns `pass` before authority activation.

## 11. Non-Normative Examples

### 11.1 Correct profile scoping

A sovereign Linux node may adopt an immutable signed operating-system image, rootless Podman, Quadlet, a narrow privileged broker, and a minimal appliance shell. These choices remain properties of the sovereign profile or appliance overlay. They do not become requirements for a Windows/WSL developer workstation or a lightweight user installation.

### 11.2 Correct optional integration behavior

A user explicitly exports selected content to Gamma, receives a result, reviews it, and imports the accepted result with provenance. Gamma remains removable, and UCKK continues local ingestion and storage when Gamma is unavailable.

### 11.3 Correct component ownership

A lightweight installation may operate one PostgreSQL process. Orgo and Konnaxion still use separate logical ownership boundaries and database identities. Neither component writes directly to the other’s authoritative tables.

### 11.4 Incorrect global promotion

A recipe demonstrates a Quadlet deployment for a sovereign node. Copying the same recipe into several repositories does not make Quadlet a global kOA requirement.

### 11.5 Correct degraded Ariane behavior

The external voice adapter is unavailable. Ariane exposes voice as unavailable while keyboard, pointer, touch, menus, deterministic commands, and accessibility navigation remain operational.

### 11.6 Correct blocked result

A proposed capability has no accepted decision and no explicit profile. The capability is not added to the baseline, not assigned an inferred default, and not included in an active conformance claim.
