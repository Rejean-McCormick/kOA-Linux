<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONST-003",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "constitution",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/system.contract.json",
    "generated/decision-index.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "contracts/integration-types.contract.json",
    "generated/profile-catalog.json",
    "generated/component-catalog.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json"
  ],
  "decision_ids": [
    "DEC-SYS-001",
    "DEC-AI-001",
    "DEC-SENT-001",
    "DEC-UCKK-001",
    "DEC-ARI-001",
    "DEC-PROFILE-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-GATE-001",
    "DEC-SHELL-001",
    "DEC-CONTAINER-001",
    "DEC-K8S-001",
    "DEC-HW-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-CONST-PRIN-001",
    "REQ-CONST-PRIN-002",
    "REQ-CONST-PRIN-003",
    "REQ-CONST-PRIN-004",
    "REQ-CONST-PRIN-005",
    "REQ-CONST-PRIN-006",
    "REQ-CONST-PRIN-007",
    "REQ-CONST-PRIN-008",
    "REQ-CONST-PRIN-009",
    "REQ-CONST-PRIN-010",
    "REQ-CONST-PRIN-011",
    "REQ-CONST-PRIN-012",
    "REQ-CONST-PRIN-013",
    "REQ-CONST-PRIN-014",
    "REQ-CONST-PRIN-015",
    "REQ-CONST-PRIN-016",
    "REQ-CONST-PRIN-017",
    "REQ-CONST-PRIN-018"
  ],
  "lock_ids": [
    "LOCK-SYS-001",
    "LOCK-SYS-002",
    "LOCK-SYS-003",
    "LOCK-SYS-004",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SENT-001",
    "LOCK-UCKK-001",
    "LOCK-UCKK-002",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-003",
    "DOC-CONST-000",
    "DOC-CONST-001",
    "DOC-CONST-002"
  ],
  "tags": [
    "constitution",
    "system-principles",
    "global-baseline",
    "authority",
    "offline-continuity",
    "safe-degradation",
    "component-separation",
    "portability",
    "audit",
    "recourse"
  ]
}
KOA:DOC-META:END -->

# System Principles

## 1. Purpose

This document defines how the constitutional principles of the kOA Operating Environment apply across system design, implementation, operation, integration, lifecycle management, recovery, and conformance.

It explains the global principles that constrain every profile, overlay, component, artifact class, integration, release, and operational procedure. The canonical system model remains in `contracts/system.contract.json`; this document supplies the normative interpretation required to apply that model consistently.

The intended outcome is deterministic reasoning: the same architectural fact produces the same authority, scope, failure, evidence, and recovery conclusions regardless of which component or profile applies it.

## 2. Scope

This document applies globally to:

- all primary deployment profiles;
- all composable profile overlays;
- all components and component contracts;
- all development and build toolchains;
- all release channels and artifact classes;
- all internal and external integrations;
- all runtime, lifecycle, security, operations, conformance, and migration activities;
- all human and automated actors that make, validate, execute, or review architectural changes.

This document governs principles rather than component-specific behavior. Component interfaces, internal states, storage layouts, profile memberships, hardware selections, artifact structures, and integration payloads remain owned by their dedicated canonical contracts.

Implementation choices such as systemd, Quadlet, Podman, Docker, Wayland, GNOME, KDE Plasma, and Kubernetes are outside global constitutional scope unless an active profile or overlay adopts them explicitly.

Historical or migration material may explain lineage, but it does not create current product authority.

## 3. Canonical References

| Canonical reference | Responsibility in this document |
| --- | --- |
| `contracts/system.contract.json#/system` | Defines the system purpose, architectural style, and global non-goals. |
| `contracts/system.contract.json#/architectural_layers` | Defines the separation between constitutional, system, profile, component, and recipe layers. |
| `contracts/system.contract.json#/global_capabilities` | Defines the capabilities that the principles protect or constrain. |
| `contracts/system.contract.json#/global_boundaries` | Defines profile, component, data, privilege, and implementation boundaries. |
| `contracts/system.contract.json#/ai_boundary` | Defines the deterministic native baseline and approved external AI boundary. |
| `contracts/system.contract.json#/offline_baseline` | Defines the global offline-continuity contract. |
| `contracts/system.contract.json#/degradation_baseline` | Defines fail-closed and capability-scoped degradation behavior. |
| `contracts/system.contract.json#/resource_governance` | Separates Resource Governor authority from Governance Policy Runtime authority. |
| `contracts/system.contract.json#/release_and_artifact_identity` | Defines compatible release identity and non-partial activation. |
| `contracts/integration-types.contract.json#/policy` | Defines allowlisting, transfer disclosure, authority limits, and removal behavior for integrations. |
| `generated/profile-catalog.json` | Owns profile and overlay membership, composition, and conditional applicability. |
| `generated/component-catalog.json` | Owns component identity, responsibility, and authoritative data ownership. |
| `contracts/release-channels.contract.json` | Owns release-channel identity and membership. |
| `contracts/artifact-classes.contract.json` | Owns artifact lifecycle, activation, recovery, provenance, and retention classes. |
| `generated/decision-index.json` | Owns accepted architectural decisions referenced by this document. |
| `generated/requirements-index.json` | Owns the exact normative statements displayed in Section 5. |
| `generated/assertion-index.json` | Owns cross-file invariants that prevent principle drift. |
| `generated/traceability.json` | Owns links among decisions, requirements, locks, tests, evidence, and affected objects. |

## 4. Model and Responsibilities

### 4.1 Principle model

A system principle is a global rule for interpreting and constraining architecture. It does not replace the canonical data model of a component, profile, integration, or artifact class.

Each principle has five effects:

1. it defines an architectural direction;
2. it constrains lower-scope contracts;
3. it establishes prohibited assumptions;
4. it determines failure and degradation expectations;
5. it establishes the evidence required for a conformance claim.

A lower-scope object may strengthen a global principle. It may not weaken, silently reinterpret, or bypass it.

### 4.2 Core principles

| Principle | Meaning | Primary canonical owner |
| --- | --- | --- |
| Explicit authority | Every consequential action has an identifiable authority source and scope. | `authority.registry.json`, owner registries, and component contracts |
| Fail-closed authority | Missing or invalid authority blocks the affected action without fabricating permission. | `system.registry.json#/degradation_baseline` |
| Local-first continuity | Applicable local capabilities remain usable without Internet or optional remote services. | `system.registry.json#/offline_baseline` |
| Deterministic core | Native authoritative behavior does not depend on generative or autonomous AI. | `system.registry.json#/ai_boundary` |
| Component separation | Responsibilities, authoritative data, and state transitions have exclusive owners. | `components.registry.json` |
| Scope discipline | Global, profile, overlay, component, artifact, and toolchain rules remain distinct. | `system.registry.json#/architectural_layers` |
| Safe degradation | Failure removes or limits only the affected capability and preserves valid state. | `system.registry.json#/degradation_baseline` |
| Controlled integration | External services are explicit, bounded, removable, and non-authoritative. | `integrations.registry.json` |
| Resource proportionality | Background and heavy work remain bounded by the active resource envelope. | `system.registry.json#/resource_governance` |
| Selective accountability | Evidence supports verification and recourse without indiscriminate disclosure. | security, audit, receipt, and evidence contracts |
| Portability and exit | Data and artifacts remain exportable, restorable, migratable, and independently usable. | lifecycle and artifact contracts |
| Recoverable activation | Authoritative transitions avoid partial state and retain a recovery path. | artifact and release contracts |
| Cultural rights and consent | Rights and consent remain attached to content across system transitions. | cultural-rights and publication contracts |
| Traceable authority | Active claims resolve to canonical sources, decisions, requirements, tests, and evidence. | `traceability.registry.json` |

### 4.3 Authority responsibilities

The owning component authorizes ordinary operations within its contract. A governance policy runtime authorizes policy-governed disclosure, consent, exceptions, and sensitive privilege decisions where a profile deploys that runtime. A narrow privileged operation path performs only the host mutation already authorized by applicable policy and profile contracts.

Resource Governor manages resource allocation and scheduling. It does not decide whether an actor may disclose information, exercise privilege, or accept an exception.

Publication Gateway controls cross-domain disclosure and publication. UCKK Dimension Gateway controls admission of user-selected media into UCKK. Neither gateway substitutes for the other.

The user language runtime consumes compiled artifacts. Language construction and compilation belong to the designated build workbench.

### 4.4 Scope responsibilities

The global baseline defines behavior that applies to every deployment. A primary profile selects a deployable operating form. An overlay strengthens or specializes an explicitly compatible primary profile. A component contract defines internal responsibility within global and profile boundaries. A recipe illustrates one implementation and has no independent authority.

The narrower object is responsible for proving that its choices remain inside all higher-scope boundaries.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-CONST-PRIN-001,REQ-CONST-PRIN-002,REQ-CONST-PRIN-003,REQ-CONST-PRIN-004,REQ-CONST-PRIN-005,REQ-CONST-PRIN-006,REQ-CONST-PRIN-007,REQ-CONST-PRIN-008,REQ-CONST-PRIN-009,REQ-CONST-PRIN-010,REQ-CONST-PRIN-011,REQ-CONST-PRIN-012,REQ-CONST-PRIN-013,REQ-CONST-PRIN-014,REQ-CONST-PRIN-015,REQ-CONST-PRIN-016,REQ-CONST-PRIN-017,REQ-CONST-PRIN-018 -->
- **REQ-CONST-PRIN-001 — SHALL:** Every authoritative system action shall identify the component, contract, decision, policy, or actor that grants its authority.
- **REQ-CONST-PRIN-002 — SHALL NOT:** Ambiguous, missing, invalid, or incompatible authority shall not be replaced by an inferred permission or an implicit fallback.
- **REQ-CONST-PRIN-003 — SHALL:** Each deployment profile shall declare and validate the local and offline capabilities that remain available without external services.
- **REQ-CONST-PRIN-004 — SHALL:** Core authoritative behavior shall remain deterministic and shall not depend on native generative AI, classifiers, summarizers, embedding models, autonomous routing models, or autonomous agents.
- **REQ-CONST-PRIN-005 — SHALL:** Every component shall retain exclusive logical ownership of its authoritative data, responsibilities, and state transitions.
- **REQ-CONST-PRIN-006 — SHALL NOT:** A component shall not write directly to another component's authoritative source tables.
- **REQ-CONST-PRIN-007 — SHALL:** A profile-specific or overlay-specific rule shall remain within its declared scope unless an accepted decision promotes it to global scope.
- **REQ-CONST-PRIN-008 — SHALL:** Failure and resource pressure shall degrade only the affected capabilities while preserving valid authoritative data and unrelated local capabilities.
- **REQ-CONST-PRIN-009 — SHALL:** External integrations shall be explicitly registered, capability-scoped, removable, transparent about transferred data, and unable to mutate authoritative state directly.
- **REQ-CONST-PRIN-010 — SHALL:** External outputs shall remain candidate inputs until an owning component validates and accepts them through a controlled workflow.
- **REQ-CONST-PRIN-011 — SHALL:** Resource governance shall bound CPU, memory, I/O, concurrency, queues, jobs, and processes without assuming policy authority.
- **REQ-CONST-PRIN-012 — SHALL:** Governance policy decisions concerning authorization, disclosure, consent, privilege, and exceptions shall remain separate from resource-governance decisions.
- **REQ-CONST-PRIN-013 — SHALL:** Critical transitions shall produce sufficient machine-readable evidence to support verification, accountability, rollback, recovery, and recourse.
- **REQ-CONST-PRIN-014 — SHALL:** Audit collection and disclosure shall be selective, purpose-bound, and limited to the evidence required for the applicable claim or investigation.
- **REQ-CONST-PRIN-015 — SHALL:** System data and published artifacts shall support export, backup, restore, migration, and credible exit through documented contracts.
- **REQ-CONST-PRIN-016 — SHALL:** Activation of authoritative artifacts shall avoid partial authoritative state and shall define rollback or forward-repair behavior.
- **REQ-CONST-PRIN-017 — SHALL:** Cultural rights, consent, disclosure restrictions, and provenance obligations shall remain enforceable across storage, transformation, integration, publication, backup, and export.
- **REQ-CONST-PRIN-018 — SHALL:** Every active architectural claim shall remain traceable to its canonical owner, accepted decisions, applicable requirements, alignment locks, tests, and evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Applying a principle to an architectural change

1. Identify the architectural fact being changed.
2. Resolve its exclusive canonical owner.
3. Determine whether the change is global, profile-specific, overlay-specific, component-specific, artifact-specific, or toolchain-specific.
4. Resolve the accepted decision authorizing the semantic change.
5. Identify all applicable constitutional requirements and alignment locks.
6. Update the canonical owner before explanatory or generated projections.
7. Compute direct and transitive impact across profiles, components, contracts, documents, tests, evidence, and AI contexts.
8. Update affected lower-scope contracts without weakening higher-scope principles.
9. Execute applicable validation and conformance tests.
10. Produce evidence for every claim affected by the change.
11. Activate the new authority only after all applicable checks pass.
12. Preserve the previous valid state or provide an explicit forward-repair path.

Completion occurs when the canonical owner, dependent objects, tests, evidence, and active authority release agree.

### 6.2 Resolving authority for an operation

1. Identify the requested capability and its owning component.
2. Resolve the active profile and overlays.
3. Resolve applicable component, security, lifecycle, and integration contracts.
4. Confirm actor, policy, and privilege authority at the required scope.
5. Validate inputs and compatibility.
6. Execute only the operation authorized by the resolved contracts.
7. Produce a receipt when the operation is a critical transition.
8. Reject the operation when authority remains missing, ambiguous, expired, or incompatible.

No fallback may broaden authority.

### 6.3 Applying a profile-specific rule

1. Resolve one active primary profile.
2. Resolve zero or more explicitly compatible overlays.
3. Load only requirements and components applicable to that composition.
4. Preserve all global constitutional and system-baseline rules.
5. Apply profile-specific implementation choices only inside that composition.
6. Reject implicit inheritance and incompatible overlay combinations.
7. Record the resulting conformance scope.

A profile rule affects no other profile unless a separate accepted decision changes the global baseline or the other profile contract.

### 6.4 Using an external integration

1. Confirm that the integration exists in `contracts/integration-types.contract.json`.
2. Confirm that the active profile permits the integration.
3. Require explicit user initiation for the specific capability.
4. disclose the data selected for transfer;
5. export only the admitted input;
6. receive the output as non-authoritative candidate material;
7. validate and import the output through the owning component;
8. obtain any required user or policy acceptance;
9. record provenance or a decision receipt when applicable;
10. preserve unrelated local capability when the integration fails or is removed.

### 6.5 Activating an authoritative artifact

1. Validate the artifact contract and schema.
2. Validate compatibility with the active release set.
3. Verify integrity and signature when required by the artifact class.
4. Confirm policy and profile authorization.
5. create or verify a recovery point;
6. stage the complete candidate state;
7. activate atomically or transactionally;
8. verify the resulting state;
9. produce an activation receipt;
10. retain rollback or forward-repair capability.

A failed activation preserves the previous valid authoritative state.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Authority retained | Authority denied | Evidence |
| --- | --- | --- | --- | --- |
| Missing, ambiguous, or incompatible authority | Block the affected operation and report the unresolved authority source. | Previously valid state and unrelated capabilities | Requested mutation or transition | Validation failure or decision receipt |
| External integration unavailable | Mark only the external capability unavailable. | Local operation, local navigation, and authoritative stores | External request and automatic substitution | Integration failure record |
| Ariane voice adapter unavailable | Disable voice interaction without changing local command authority. | Keyboard, pointer, touch, menus, accessibility controls, and local shortcuts | External voice capability | Capability-status evidence |
| Resource pressure | Defer background work, reduce concurrency, and stop task-activated heavy services. | Authoritative data integrity and core control | Excess concurrency and nonessential heavy work | Resource-governance metrics |
| Component failure | Isolate the failed component and preserve other component boundaries. | Unaffected component authority | Cross-boundary repair or direct database mutation | Component health and incident evidence |
| Contract or schema incompatibility | Block import, activation, or communication using the incompatible object. | Existing valid state | Candidate incompatible state | Contract-validation report |
| Integrity or signature failure | Reject the affected artifact before import, activation, publication, or restore. | Previously verified artifact state | Unverified artifact authority | Integrity or signature verification evidence |
| Activation failure | Abort or reverse the transition without partial authority. | Previous valid active version | Partially staged or failed candidate version | Failure and recovery receipts |
| Offline transition | Remove remote-only capabilities and continue within the declared offline envelope. | Declared local capabilities | Remote-only capability | Offline conformance evidence |
| Audit subsystem unavailable | Preserve primary component state and queue only bounded evidence work when allowed. | Owning component authority | Unsupported audit or conformance claim | Health record and deferred-evidence status |
| Recovery input invalid | Reject restore and retain the current valid state when safe. | Current verified state | Invalid restored state | Restore-validation report |
| Missing traceability or evidence | Block the affected conformance, release, or authority claim. | Existing independently supported claims | Unsupported claim | Traceability-validation failure |

## 8. Cross-Component Interactions

| Producer | Consumer | Canonical contract | Direction | Authority boundary | Failure ownership |
| --- | --- | --- | --- | --- | --- |
| Owning component | Another component | Versioned API, command, event, gateway, exported artifact, or declared read model | Explicit and contract-defined | Consumer cannot acquire write authority over producer data | Producer owns source-state failure; consumer owns import and local-state failure |
| Resource Governor | Components and workers | Component and profile resource envelopes | Control and observation | Resource decisions do not grant policy or data authority | Resource Governor owns scheduling and limit enforcement |
| Governance Policy Runtime | Privileged broker, Publication Gateway, or governed component | Policy decision and receipt contracts | Authorization decision | Policy authorizes; execution remains with the receiving component or broker | Policy runtime owns decision failure; executor owns operation failure |
| UCKK Dimension Gateway | UCKK Platform | Dimension-ingestion contract | User-selected media admission | Gateway verifies and transfers; UCKK owns admitted media state | Gateway owns transfer failure; UCKK owns admission failure |
| Publication Gateway | External audience or domain | Publication request and receipt contracts | Controlled outward disclosure | Gateway cannot rewrite source-domain authority | Gateway owns disclosure and delivery failure |
| GF Wordbench | Language artifact repository | Language-pack and runtime-pack contracts | Build and publish | Build workbench produces artifacts; runtime does not compile them | Workbench owns build failure; repository owns admission failure |
| SemantiK Architect Runtime | User-facing components | Compiled runtime contract | Read and evaluate | Runtime consumes approved compiled artifacts only | Runtime owns evaluation failure |
| External integration | Owning component | Integration registry and import contract | Candidate output inward | External output has no direct authority | Integration owns remote failure; component owns validation and acceptance |
| Build Farm | Artifact registry or release process | Artifact-class, provenance, and release-set contracts | Build, validate, publish | Build output gains authority only after required validation and activation | Build Farm owns build evidence; activation owner owns release transition |
| Audit Broker | Authorized evidence consumer | Audit and evidence contract | Selective evidence disclosure | Evidence access does not grant operational or source-data authority | Audit Broker owns collection and disclosure failure |

Direct cross-component writes to authoritative source tables are prohibited. Shared infrastructure, physical database processes, caches, and read models do not transfer logical ownership.

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Effect on this document |
| --- | --- |
| `DEC-SYS-001` | Establishes the local-first, modular, deterministic global system baseline. |
| `DEC-AI-001` | Excludes native generative and autonomous AI from the authoritative baseline and bounds external AI use. |
| `DEC-SENT-001` | Keeps SenTient optional, isolated, task-activated, and non-authoritative. |
| `DEC-UCKK-001` | Defines deterministic native UCKK behavior and explicit external media adapters. |
| `DEC-ARI-001` | Separates local non-AI navigation from optional external voice capability. |
| `DEC-PROFILE-001` | Establishes seven primary profiles, three overlays, and explicit composition. |
| `DEC-DATA-001` | Requires exclusive logical data ownership and prohibits cross-component source-table writes. |
| `DEC-GOV-001` | Separates Resource Governor from Governance Policy Runtime. |
| `DEC-GATE-001` | Separates Publication Gateway from UCKK Dimension Gateway. |
| `DEC-SHELL-001` | Keeps desktop and appliance-shell choices profile-scoped. |
| `DEC-CONTAINER-001` | Keeps container-runtime selection profile-scoped and avoids runtime-specific application authority. |
| `DEC-K8S-001` | Excludes Kubernetes from endpoint requirements and limits it to approved infrastructure profiles. |
| `DEC-HW-001` | Defines profile-specific hardware envelopes and bounded heavy work. |
| `DEC-REL-001` | Establishes four release channels and compatible Release Sets. |

### Prohibited assumptions

- A system administrator, root process, deployment controller, or AI agent possesses unlimited application authority.
- A commonly used implementation becomes globally required through prevalence.
- A profile rule applies to another profile without explicit composition or inheritance.
- Physical database consolidation permits cross-component writes.
- An external integration output is authoritative because a user requested it.
- Read-only access, caching, indexing, or transformation transfers ownership.
- Resource allocation decisions imply authorization, disclosure, consent, or privilege decisions.
- Publication Gateway and UCKK Dimension Gateway are interchangeable.
- User runtime components may silently perform build-workbench functions.
- Network availability is required for local authoritative operation.
- Failure permits partial authoritative activation or silent substitution.
- Auditability requires indiscriminate disclosure.
- Backup availability alone proves recoverability without a verified restore path.
- Generated documentation, recipes, prompts, tickets, code comments, or implementation defaults create architectural authority.

## 10. Validation Criteria

1. The metadata block parses as JSON and declares `DOC-CONST-003`, `active`, `en`, `constitution`, and global scope.
2. Every canonical path and JSON Pointer listed in Section 3 resolves in the assembled active corpus.
3. Every decision ID is present and accepted in `generated/decision-index.json`.
4. Every requirement ID in the metadata appears exactly once in `generated/requirements-index.json` with global scope and applicable validation mappings.
5. Every lock ID exists in `generated/assertion-index.json` and contains an executable assertion or assigned manual control.
6. No lower-scope profile, overlay, component, integration, artifact, or recipe weakens a requirement in this document.
7. `TEST-CONST-PRIN-001` verifies explicit authority and fail-closed behavior for missing authority.
8. `TEST-CONST-PRIN-002` verifies that all profiles declare an offline capability envelope.
9. `TEST-CONST-PRIN-003` verifies absence of prohibited native AI dependencies in the global baseline.
10. `TEST-CONST-PRIN-004` verifies exclusive component data ownership and rejects cross-component source-table writes.
11. `TEST-CONST-PRIN-005` verifies explicit profile composition and rejects incompatible or implicit inheritance.
12. `TEST-CONST-PRIN-006` verifies capability-scoped degradation under external-service and resource failure.
13. `TEST-CONST-PRIN-007` verifies integration allowlisting, transfer disclosure, candidate-output handling, and removal behavior.
14. `TEST-CONST-PRIN-008` verifies separation of Resource Governor and Governance Policy Runtime authority.
15. `TEST-CONST-PRIN-009` verifies atomic artifact activation and rollback or forward-repair behavior.
16. `TEST-CONST-PRIN-010` verifies selective evidence disclosure, recourse support, and absence of unsupported conformance claims.
17. `TEST-CONST-PRIN-011` verifies export, backup, restore, migration, and credible-exit contracts for applicable data and artifacts.
18. `TEST-CONST-PRIN-012` verifies complete traceability from principles to decisions, requirements, locks, tests, and evidence.
19. Active prose is English and contains no unresolved marker, template token, or prohibited placeholder.
20. The document retains all eleven required sections and the requirement block matches its canonical registry projection.

These criteria define required validation. They do not claim that the tests have already executed or that conformance evidence already exists.

## 11. Non-Normative Examples

> **Non-normative example:** This example illustrates one valid implementation or scenario. It does not redefine the canonical contract.

A user profile loses Internet access while editing local data. Local storage, deterministic Ariane navigation, compiled language artifacts, and local UCKK operations continue within the profile's offline envelope. ChatGPT, Suno, Gamma, and external Ariane voice become unavailable. The system does not substitute an unregistered provider.

> **Non-normative example:** This example illustrates one valid implementation or scenario. It does not redefine the canonical contract.

A component needs information owned by another component. It requests a versioned API response or consumes an authorized event. It may cache a declared read model, but it does not write to the producer's database or reinterpret the producer's state as its own authority.

> **Non-normative example:** This example illustrates one valid implementation or scenario. It does not redefine the canonical contract.

A lightweight deployment and a sovereign node may use different process, storage, desktop, and container layouts. Both remain conformant when each follows its active profile contract and both preserve global authority, separation, offline, recovery, and evidence principles.

> **Non-normative example:** This example illustrates one valid implementation or scenario. It does not redefine the canonical contract.

A service update passes contract, compatibility, integrity, and signature checks. The deployment stages the complete candidate, creates a recovery point, switches atomically, verifies the result, and emits an activation receipt. A failed verification leaves the previous valid version active.

> **Non-normative example:** This example illustrates one valid implementation or scenario. It does not redefine the canonical contract.

An external service produces a candidate presentation. The result is re-imported through a controlled component workflow, provenance is recorded, and a user approves it before publication. The external provider never writes directly to the authoritative publication store.
