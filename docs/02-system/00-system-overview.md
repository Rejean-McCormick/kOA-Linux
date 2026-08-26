<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-000",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "system",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/integration-types.contract.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "generated/decision-index.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
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
    "DEC-SYS-001",
    "DEC-AI-001",
    "DEC-SENT-001",
    "DEC-MEDIATHEQUE-001",
    "DEC-UCKK-EXT-001",
    "DEC-ARI-001",
    "DEC-PROFILE-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-GATE-001",
    "DEC-SHELL-001",
    "DEC-CONTAINER-001",
    "DEC-K8S-001",
    "DEC-HW-001",
    "DEC-REL-001",
    "DEC-RES-001",
    "DEC-MSG-001",
    "DEC-WF-001",
    "DEC-PAYLOAD-001",
    "DEC-BFF-001",
    "DEC-CQRS-001",
    "DEC-CACHE-001"
  ],
  "requirement_ids": [
    "REQ-SYS-OVR-001",
    "REQ-SYS-OVR-002",
    "REQ-SYS-OVR-003",
    "REQ-SYS-OVR-004",
    "REQ-SYS-OVR-005",
    "REQ-SYS-OVR-006",
    "REQ-SYS-OVR-007",
    "REQ-SYS-OVR-008",
    "REQ-SYS-OVR-009",
    "REQ-SYS-OVR-010",
    "REQ-SYS-OVR-011",
    "REQ-SYS-OVR-012",
    "REQ-SYS-OVR-013",
    "REQ-SYS-OVR-014",
    "REQ-SYS-OVR-015",
    "REQ-SYS-OVR-016",
    "REQ-SYS-OVR-017",
    "REQ-SYS-OVR-018",
    "REQ-SYS-OVR-019",
    "REQ-SYS-OVR-020",
    "REQ-PATTERN-001",
    "REQ-PATTERN-002",
    "REQ-PATTERN-003",
    "REQ-PATTERN-004",
    "REQ-PATTERN-005"
  ],
  "lock_ids": [
    "LOCK-SYS-001",
    "LOCK-SYS-002",
    "LOCK-SYS-003",
    "LOCK-SYS-004",
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
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-PROFILE-001",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
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
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-CONST-000",
    "DOC-CONST-001",
    "DOC-CONST-002",
    "DOC-CONST-003"
  ],
  "tags": [
    "system",
    "overview",
    "global-baseline",
    "operating-modes",
    "capabilities",
    "components",
    "profiles",
    "offline",
    "ai-boundary",
    "release-model",
    "architecture-patterns",
    "koa-spaces",
    "experience-layer"
  ]
}
KOA:DOC-META:END -->

# System Overview

## 1. Purpose

This document is the normative entry point for the kOA system layer.

It explains what the kOA Operating Environment is, how its major architectural layers relate, which operating modes and global capabilities exist, how profiles and components participate, and how the system behaves during integration, disconnection, degradation, activation, and recovery.

The canonical machine-readable system model is `contracts/system.contract.json`. This document interprets that model for designers, implementers, reviewers, operators, validators, and AI agents. It does not become a second owner of component inventories, profile membership, integration records, release channels, artifact structures, requirements, locks, or evidence.

The system is a local-first, offline-capable, modular operating environment for governed knowledge, coordination, language, media, navigation, publication, and sovereign deployment.

## 2. Scope

This document applies to the global kOA system baseline and to every active:

- primary deployment profile;
- profile overlay;
- component and component contract;
- development or build toolchain;
- release channel and artifact class;
- internal or external integration;
- lifecycle, security, operations, conformance, and migration workflow.

It defines global system relationships and constraints. It does not define:

- the detailed fields of a component contract;
- profile-specific component membership;
- implementation-specific service managers, desktop shells, container runtimes, or orchestration platforms;
- database schemas or component-internal state machines;
- the wire format of an integration payload;
- the full structure of an artifact contract;
- exact requirement, lock, test, or evidence objects outside their canonical registries.

Standard user and developer profiles may use maintained desktop environments such as GNOME or KDE Plasma. A minimal Wayland appliance shell is an overlay-scoped choice. Rootless Podman is preferred for applicable Linux profiles, Docker or Podman may be used for Windows and WSL development, containers are optional for `user_lightweight`, and Kubernetes is not an endpoint requirement.

## 3. Canonical References

| Canonical reference | Ownership |
| --- | --- |
| `contracts/system.contract.json#/system` | System identity, purpose, architectural style, and global non-goals |
| `contracts/system.contract.json#/architectural_layers` | Global architectural layers and their ownership boundaries |
| `contracts/system.contract.json#/operating_modes` | Global operating-mode definitions |
| `contracts/system.contract.json#/global_capabilities` | Global capability catalog |
| `contracts/system.contract.json#/global_boundaries` | Profile, component, data, privilege, and implementation boundaries |
| `contracts/system.contract.json#/ai_boundary` | Native AI prohibition and approved external AI boundary |
| `contracts/system.contract.json#/sentient_boundary` | SenTient role, availability, isolation, and admission rules |
| `contracts/system.contract.json#/ariane` | Ariane local-navigation and external-voice capability levels |
| `contracts/system.contract.json#/koa_mediatheque` | Native deterministic kOA Mediatheque operations and external-adapter workflow |
| `contracts/system.contract.json#/language_runtime` | Compiled language and knowledge runtime model |
| `contracts/system.contract.json#/resource_governance` | Resource Governor and Governance Policy Runtime separation |
| `contracts/system.contract.json#/offline_baseline` | Global offline behavior |
| `contracts/system.contract.json#/degradation_baseline` | Global failure and degradation rules |
| `contracts/system.contract.json#/hardware_envelope_classes` | Global hardware-envelope classes |
| `contracts/system.contract.json#/release_and_artifact_identity` | Release-set and artifact-activation baseline |
| `generated/component-catalog.json` | Component identity, class, responsibility, dependencies, and authoritative data ownership |
| `generated/component-catalog.json` | Active component-contract inventory |
| `generated/profile-catalog.json` | Primary profiles, overlays, composition, groups, workbenches, and profile-level integration availability |
| `contracts/integration-types.contract.json` | External integration classification, data transfer, authority, failure, and removal behavior |
| `contracts/release-channels.contract.json` | Release-channel identity, membership, and compatibility |
| `contracts/artifact-classes.contract.json` | Artifact and receipt classes, lifecycle, activation, recovery, provenance, and retention |
| `generated/decision-index.json` | Accepted owner decisions |
| `generated/requirements-index.json` | Normative requirement statements |
| `generated/assertion-index.json` | Cross-file invariants |
| `generated/traceability.json` | Decision, requirement, lock, profile, component, test, and evidence links |
| `generated/test-catalog.json` | Registered validation and conformance tests |
| `generated/evidence-catalog.json` | Registered valid evidence records |

Repository-relative paths and JSON Pointers are the canonical reference mechanism. A prose summary or diagram does not replace the referenced object.

## 4. Model and Responsibilities

### 4.1 System identity

The canonical system identifier is `koa_linux_operating_system`. Its system class is `sovereign_local_operating_system`.

The architectural style combines:

- explicit authority;
- component separation;
- local-first operation;
- offline continuity;
- deterministic core behavior;
- profile-scoped deployment;
- contract-driven integration;
- safe degradation;
- selective audit;
- portable artifacts.

The baseline is not a universal appliance specification. It does not require Kubernetes, a particular desktop, a single container runtime, shared component databases, native AI, or one fixed host layout.

### 4.2 Architectural layers

| Layer | Scope | Responsibility |
| --- | --- | --- |
| L0 — Constitutional principles | Global | Explicit authority, fail-closed behavior, offline continuity, safe degradation, separation, audit, recourse, portability, and cultural rights |
| L1 — System baseline | Global | System context, modes, capabilities, boundaries, AI, Ariane, kOA Mediatheque, language runtime, resource governance, degradation, and release identity |
| L2 — Deployment profiles | Profile and overlay | Deployable compositions, conditional capabilities, component membership, hardware, security, offline guarantees, and conformance |
| L3 — Component contracts | Component | Inputs, outputs, interfaces, events, states, failure behavior, and data boundaries |
| L4 — Implementation recipes | Non-normative unless explicitly adopted | systemd, Quadlet, containers, desktop shells, storage, networking, and development commands |

A lower layer may refine a higher layer only within the authority granted to it. An implementation recipe does not become global architecture through repetition.

### 4.3 Operating modes

| Mode | Purpose | Connectivity | Core characteristics |
| --- | --- | --- | --- |
| `interactive_user` | Operate the local user-facing kOA environment with deterministic core services and task-activated heavy work. | `online`, `restricted_network`, `offline` | local authority, non ai navigation, compiled language artifact consumption, deterministic media pipeline, bounded background work |
| `development` | Develop multiple kOA applications, branches, and worktrees in isolated reproducible workspaces. | `online`, `restricted_network` | workspace identity, isolated mutable dependencies, isolated service state, parallel workspace execution, explicit artifact publication |
| `build` | Produce reproducible, validated, provenance-bearing system, service, governance, and knowledge artifacts. | `online`, `restricted_network`, `offline_with_imported_sources` | clean workers, reproducible inputs, artifact cache, test evidence, provenance generation |
| `service_node` | Host a persistent kOA node with profile-defined availability, security, recovery, and offline guarantees. | `online`, `restricted_network`, `offline` | persistent local authority, profile scoped security, backup restore, safe degradation, controlled updates |
| `hub` | Coordinate multiple nodes, artifacts, or governed domains without replacing component or node authority. | `online`, `restricted_network`, `intermittent` | federated coordination, explicit cross domain contracts, bounded centralization, auditable distribution |
| `control_plane` | Operate deployment, release, policy, and fleet coordination services for profiles that require a control plane. | `online`, `restricted_network` | deployment coordination, release coordination, policy distribution, fleet observability |
| `recovery` | Restore a valid system, artifact set, or authoritative data state without creating partial authority. | `online`, `restricted_network`, `offline` | verified recovery input, atomic restore, rollback or forward repair, evidence generation |

An operating mode describes system activity. A deployment profile describes the deployable environment in which one or more modes operate. A mode is not a replacement for a profile.

### 4.4 Global capabilities

| Capability | Availability | Description |
| --- | --- | --- |
| `local_authoritative_operation` | `global_contract` | Authoritative local operations remain possible within the active profile's offline and security envelope. |
| `deterministic_navigation` | `profile_activated` | Ariane local navigation works without external AI or voice services. |
| `governed_knowledge_runtime` | `profile_activated` | Compiled knowledge and language artifacts are consumed locally without requiring build workbenches. |
| `deterministic_media_management` | `profile_activated` | The kOA Mediatheque ingests, verifies, transforms, stores, exports, backs up, and restores private local media and imported learning content through deterministic local operations. |
| `offline_learning_content` | `profile_activated` | Verified courses, learning paths, instructions, manuals, and resources accepted into the kOA Mediatheque remain consultable without a live UCKK connection. |
| `governed_uckk_interchange` | `optional` | Explicit outbound publication and inbound acquisition use separate authorization, validation, queue, receipt, and conflict rules. |
| `deterministic_resource_governance` | `global_baseline_component` | Resource Governor bounds CPU, memory, I/O, concurrency, queues, jobs, and processes. |
| `profile_conditioned_policy_governance` | `profile_conditioned` | Governance Policy Runtime supplies authorization, disclosure, consent, privilege decisions, and governed exceptions where required by a profile. |
| `controlled_external_integration` | `optional` | External services are explicitly classified, removable, capability-scoped, and unable to directly mutate authoritative state. |
| `selective_audit_and_recourse` | `global_contract` | Accountability evidence is produced without requiring indiscriminate disclosure. |
| `portability_restore_and_exit` | `global_contract` | Open interfaces, export, backup, restore, and credible independent exit remain system objectives. |

Capability availability remains conditioned by the active profile and overlays. The global catalog establishes meaning, not universal component installation.

### 4.5 Ecosystem systems, integrated subsystems, and native components

kOA-Linux operates inside the wider **kOA Digital Ecosystem**. The host view distinguishes independently owned ecosystem systems from native kOA-Linux components.

| Entity | Global category | kOA-Linux view | Authority boundary |
| --- | --- | --- | --- |
| Konnaxion | ecosystem system | integrated subsystem | Konnaxion owns its internal civic/public domain, API, workflow, state, and UI |
| Orgo | ecosystem system | integrated subsystem | Orgo owns its Organization/Case/Task/workflow internals |
| Kristal | ecosystem system | external normative/artifact owner plus local `kristal_runtime` consumption boundary | Kristal owns epistemic semantics; kOA-Linux owns only local runtime/admission state assigned by its contracts |
| SemantiK Architect | ecosystem system | integrated subsystem with a local runtime deployment boundary | Architect owns planner/construction/lexicon/renderer/public-generation semantics |
| Ariane | independently documented system | integrated subsystem | Ariane owns its internal navigation/interaction behavior |
| SenTient | independently documented optional system/workbench | integrated subsystem | Candidate/research output remains non-authoritative until accepted by an owner |
| kOA Spaces | kOA-Linux subsystem | optional experience subsystem | Presentation composition only; no business authority |
| kOA Mediatheque | native kOA-Linux component | native component | Owns local media records/lifecycle only |
| Resource Governor | native kOA-Linux component | native component | Owns resource admission/limits, not policy authorization |
| Governance Policy Runtime | native kOA-Linux component | native component | Owns scoped policy decisions, not resource scheduling |
| Identity and Trust | native kOA-Linux component | native component | Owns registered trust/identity verification functions |
| Audit Broker | native kOA-Linux component | native component | Preserves/selectively discloses evidence without owning observed domain state |
| Publication Gateway | native kOA-Linux component | native component | Owns controlled disclosure/publication boundary |
| kOA Node Agent | native kOA-Linux component | native component | Owns declared node-local lifecycle/operational functions |
| UCKK | external platform | external integration | UCKK remains a separate Moodle authority |

Calling Konnaxion, Orgo, or SemantiK Architect a `subsystem` in this corpus is host-relative. It does not reclassify those systems globally and does not transfer their internal authority to kOA-Linux.

### 4.6 Data and communication model

Every component has exclusive logical ownership of its authoritative data. Physical consolidation may be allowed by a profile, but it does not transfer ownership.

Cross-component communication uses only declared mechanisms:

- versioned APIs;
- commands;
- events;
- gateways;
- exported artifacts;
- controlled read models.

A consumer validates imported data and owns its resulting local state. It does not acquire write authority over the producer's source state.

### 4.7 AI and external-service boundary

The global baseline contains no native generative AI, classifier, summarizer, embedding model, autonomous routing model, autonomous agent, AI-generated category system, or AI-based ingestion decision.

Approved external surfaces are limited to the entries in `contracts/integration-types.contract.json`:

| Integration | Classification | Capability scope | Unavailable behavior |
| --- | --- | --- | --- |
| `chatgpt` | `external_ai_assistance` | user requested assistance, candidate text generation, candidate structured output, candidate analysis | The requested external assistance operation is unavailable; unrelated local capabilities remain operational. |
| `suno` | `external_media_generation` | user requested audio generation, user requested music generation, candidate media artifact return | External media generation is unavailable; deterministic local kOA Mediatheque operations remain operational. |
| `gamma` | `external_presentation_generation` | user requested presentation generation, candidate presentation artifact return | External presentation generation is unavailable; unrelated local capabilities remain operational. |
| `ariane_voice_adapter` | `external_voice_capability` | voice input processing, candidate navigation intent return | Voice controls are unavailable; Ariane local keyboard, pointer, touch, menu, shortcut, and accessibility navigation remain operational. |

External outputs remain candidate inputs until accepted by the owning component. No integration receives implicit repository access, authoritative-store access, policy authority, privilege control, release authority, or publication authority.

### 4.8 Hardware envelopes

Hardware envelopes are architectural capacity classes rather than performance guarantees.

| Envelope | CPU | Memory | Minimum storage | Additional constraints |
| --- | --- | --- | --- | --- |
| `user_lightweight` | 4 modern cores minimum, 6 recommended | 16 GiB minimum, 32 GiB recommended | 512 GB SSD | maximum 1 heavy job; zram required |
| `developer_workstation` | 8 modern cores minimum | 32 GiB minimum, 64 GiB recommended | 1 TB SSD | default maximum 2 heavy workspaces |
| `sovereign_linux_node` | 8 modern cores minimum | 32 GiB minimum, 64 GiB recommended | 1 TB encrypted SSD | recovery target required; verified backup target required |
| `build_farm` | 16 cores minimum | 64 GiB minimum | 2 TB SSD | artifact cache required; reproducible clean workers required |

Profile contracts select the applicable envelope and may strengthen it. Measurements and conformance evidence determine whether an implementation satisfies the selected envelope.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SYS-OVR-001,REQ-SYS-OVR-002,REQ-SYS-OVR-003,REQ-SYS-OVR-004,REQ-SYS-OVR-005,REQ-SYS-OVR-006,REQ-SYS-OVR-007,REQ-SYS-OVR-008,REQ-SYS-OVR-009,REQ-SYS-OVR-010,REQ-SYS-OVR-011,REQ-SYS-OVR-012,REQ-SYS-OVR-013,REQ-SYS-OVR-014,REQ-SYS-OVR-015,REQ-SYS-OVR-016,REQ-SYS-OVR-017,REQ-SYS-OVR-018,REQ-SYS-OVR-019,REQ-SYS-OVR-020 -->
- **REQ-SYS-OVR-001 — SHALL:** The kOA Operating Environment shall provide a local-first, offline-capable, modular environment for governed knowledge, coordination, language, media, navigation, publication, and sovereign deployment.
- **REQ-SYS-OVR-002 — SHALL:** Every deployment shall select exactly one registered primary profile and may apply only explicitly compatible registered overlays.
- **REQ-SYS-OVR-003 — SHALL:** The global baseline shall remain independent of profile-specific desktop, container, orchestration, host-layout, and appliance implementation choices.
- **REQ-SYS-OVR-004 — SHALL:** The active system shall preserve explicit authority, exclusive canonical ownership, component separation, deterministic core behavior, safe degradation, selective audit, and portable artifacts.
- **REQ-SYS-OVR-005 — SHALL:** Each component shall operate only within its registered responsibility, authoritative-data boundary, interfaces, and active profile membership.
- **REQ-SYS-OVR-006 — SHALL NOT:** No component shall write directly to another component's authoritative source tables or acquire authority through caching, indexing, observation, or physical infrastructure sharing.
- **REQ-SYS-OVR-007 — SHALL:** The Resource Governor shall manage deterministic resource allocation and scheduling independently from Governance Policy Runtime authorization, disclosure, consent, privilege, and exception decisions.
- **REQ-SYS-OVR-008 — SHALL:** Publication Gateway shall authorize disclosure before the UCKK Publication Bridge packages and transports an approved publication; the separate UCKK Import Bridge shall retrieve selected learning packages into quarantine for deterministic validation and explicit local acceptance, and neither direction shall create implicit synchronization.
- **REQ-SYS-OVR-009 — SHALL:** Ariane local navigation shall remain operational without AI, external voice, or network access within the active profile's local capability envelope.
- **REQ-SYS-OVR-010 — SHALL:** The native kOA Mediatheque pipeline shall perform only deterministic local ingestion, verification, transformation, storage, export, backup, and restore operations.
- **REQ-SYS-OVR-011 — SHALL:** The user language runtime shall consume approved compiled language and knowledge artifacts, while construction and compilation remain assigned to designated workbenches.
- **REQ-SYS-OVR-012 — SHALL:** The global baseline shall contain no native generative AI, classifier, summarizer, embedding model, autonomous routing model, autonomous agent, AI category generator, or AI ingestion decision.
- **REQ-SYS-OVR-013 — SHALL:** Every external integration shall be explicitly registered, user-initiated, capability-scoped, transparent about transferred data, removable without core failure, and unable to write directly to authoritative state.
- **REQ-SYS-OVR-014 — SHALL:** SenTient shall remain an optional, isolated, task-activated, non-authoritative workbench outside the default user baseline.
- **REQ-SYS-OVR-015 — SHALL:** Every active profile shall declare and test its online, restricted-network, intermittent, and offline capability behavior as applicable.
- **REQ-SYS-OVR-016 — SHALL:** Failure or resource pressure shall affect only declared capabilities, preserve valid authoritative data, reject silent substitution, and retain unrelated local operation.
- **REQ-SYS-OVR-017 — SHALL:** Published system, service, governance, and knowledge artifacts shall use registered artifact classes and release channels with declared compatibility.
- **REQ-SYS-OVR-018 — SHALL:** Authoritative artifact activation shall avoid partial state and shall preserve rollback, forward-repair, restore, or reconstruction behavior appropriate to the artifact class.
- **REQ-SYS-OVR-019 — SHALL:** Critical policy, activation, release, publication, and privileged-host transitions shall produce machine-readable receipts when required by their contracts.
- **REQ-SYS-OVR-020 — SHALL:** Every system conformance claim shall be traceable to accepted decisions, active requirements, applicable locks, registered tests, and valid evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 System composition

1. Select one registered active primary profile.
2. Select zero or more explicitly compatible active overlays.
3. Resolve the resulting component membership and optional workbenches.
4. Resolve the hardware envelope and connectivity claims.
5. Resolve applicable security, lifecycle, operations, and conformance requirements.
6. Validate profile inheritance and overlay compatibility.
7. Reject unregistered, implicit, or incompatible composition.
8. Record the conformance scope of the resulting deployment.

The resulting deployment may implement profile-specific choices, but it remains bound by all global constitutional and system requirements.

### 6.2 Local startup

1. Resolve the active Release Set and profile composition.
2. Verify required system, service, governance, and knowledge artifacts.
3. Verify profile-required trust, policy, resource, and storage prerequisites.
4. Start only components required or permitted by the profile.
5. Keep heavy optional workbenches and task workers stopped unless explicitly activated.
6. Establish component-specific data ownership and identities.
7. Apply Resource Governor envelopes.
8. Expose local Ariane navigation and other declared local capabilities.
9. Record startup or activation evidence when required.

A startup failure does not permit partial authoritative activation. The deployment retains or restores the previous valid state.

### 6.3 Ordinary authoritative operation

1. Identify the owning component and requested capability.
2. Validate the actor, input, profile, component, and policy context.
3. Resolve any required cross-component contract.
4. Execute within the owning component's authority and resource envelope.
5. Commit only the owning component's authoritative state.
6. Emit events, receipts, or exported artifacts required by the contract.
7. Preserve provenance and traceability.
8. Reject direct cross-component source-state mutation.

### 6.4 UCKK and other external integration operations

An external operation begins only after the user or a governed workflow selects the exact direction, data, purpose, and destination.

For `publish_to_uckk`, Publication Gateway evaluates disclosure, rights, consent, audience, representation, and expiry before UCKK-specific packaging and transport.

For `import_from_uckk`, the system verifies UCKK source identity, license, manifest, integrity, compatibility, and local acceptance conditions before creating a local kOA record and version.

The system records the exact external effect or a visible pending, rejected, failed, quarantined, or reconciliation-required state. It never reports generic synchronization success.

### 6.5 Offline transition

1. Detect loss or intentional removal of remote connectivity.
2. Mark remote-only capabilities unavailable.
3. Preserve local authoritative state and local declared capabilities.
4. Keep Ariane local navigation operational.
5. Keep deterministic kOA Mediatheque, language runtime, resource governance, backup, restore, and verified import available where the profile claims them.
6. Queue only bounded, visible, idempotent remote work when the profile permits queuing.
7. Do not activate an unregistered substitute.
8. Record offline conformance or operational evidence when required.

### 6.6 Heavy task activation

1. Identify the task and owning component.
2. Validate profile permission and resource availability.
3. Activate only the required worker or workbench.
4. Apply CPU, memory, I/O, concurrency, network, storage, and time limits.
5. Isolate mutable dependencies and temporary state.
6. Produce candidate outputs or authoritative results according to the component contract.
7. Stop or scale down the task-specific service after completion.
8. Preserve logs and evidence required by the applicable claim.

SenTient follows this procedure and never becomes an always-running global service.

### 6.7 Release and artifact activation

1. Resolve the artifact class and release channel.
2. Validate schema, semantics, compatibility, integrity, signature, policy, and resource preconditions.
3. Confirm Release Set compatibility when required.
4. Create or verify a recovery point.
5. Stage the complete candidate.
6. Activate atomically, transactionally, or through an immutable slot switch.
7. Verify the resulting active state.
8. Emit an activation receipt.
9. Retain rollback or forward-repair capability.
10. Preserve the previous valid state when activation fails.

## 7. Failure States and Safe Degradation

| Failure state | Required behavior | Preserved behavior | Blocked behavior |
| --- | --- | --- | --- |
| Missing or ambiguous authority | Fail closed for the affected capability and identify the unresolved authority | Existing valid state and unrelated local capabilities | Requested unauthorized action |
| Invalid profile composition | Reject activation of the composition | Previously valid profile composition | Unregistered primary profile, implicit inheritance, or incompatible overlay |
| Component unavailable | Isolate the component and expose explicit degraded status | Other component authority and valid data | Cross-component repair through direct source-table writes |
| Resource exhaustion | Defer background work, reduce concurrency, and stop task-activated heavy services | Core control, local navigation, authoritative data integrity | Excess workers and uncontrolled heavy processing |
| External service unavailable | Disable only the affected integration capability | Local system operation and local authoritative state | External request and silent provider substitution |
| Ariane voice unavailable | Disable voice input | Keyboard, pointer, touch, menus, shortcuts, accessibility, and deterministic commands | External voice capability |
| SenTient unavailable | Leave enrichment work unavailable | All baseline and ordinary development functions | Automatic replacement or baseline dependency |
| Contract incompatibility | Reject communication, import, or activation using the incompatible contract | Previous valid state | Schema guessing or partial application |
| Integrity or signature failure | Reject the artifact before admission or activation | Previously verified artifact | Unverified candidate |
| Release-set incompatibility | Block independent channel update | Existing compatible release set | Partial incompatible release |
| Offline state | Remove remote-only capabilities | Declared local offline envelope | Remote calls and hidden synchronization |
| Evidence unavailable or invalid | Block the unsupported conformance or release claim | Independently supported operation | Unsupported claim |
| Backup or restore verification failure | Preserve current valid state and reject invalid recovery input | Current verified system | Invalid restored state |
| Audit disclosure denied | Preserve source evidence and enforce disclosure policy | Operational authority unaffected unless policy requires evidence | Unauthorized evidence disclosure |

Safe degradation never authorizes a broader capability than the normal operating state.

## 8. Cross-Component Interactions

| Interaction | Producer | Consumer | Contract form | Authority result |
| --- | --- | --- | --- | --- |
| Domain coordination | Orgo or another owning domain | Authorized component | API, command, or event | Consumer acts only within its own contract |
| Knowledge consumption | Kristal Runtime or artifact repository | Konnaxion, Orgo, language, or user-facing components | Versioned knowledge artifact | Artifact identity remains independent of consumer workflow |
| Language generation deployment | SemantiK Architect subsystem | User-facing consumers | Semantic generation API/results plus declared runtime/backend assets | kOA-Linux governs deployment/artifact boundaries; Architect owns planner and realization semantics |
| Local media management | kOA Mediatheque | kOA Mediatheque | Internal component contract | kOA Mediatheque owns local media state |
| Cross-domain publication | Owning component | Publication Gateway | Publication request and receipt | Gateway controls disclosure without taking source ownership |
| Resource control | Resource Governor | Components and task workers | Resource envelope and control interface | Resource limits do not grant policy authority |
| Policy authorization | Governance Policy Runtime | Governed component, privileged broker, or Publication Gateway | Policy decision and receipt | Executor performs only the authorized action |
| Selective evidence | Components | Audit Broker | Evidence event or authorized collection interface | Audit Broker owns evidence handling, not source operations |
| External AI assistance | ChatGPT | Owning component or user workflow | Controlled export and import | Output remains candidate input |
| External media generation | Suno or Gamma | kOA Mediatheque or another owning component | Controlled export, re-import, provenance, and approval | External output has no direct authority |
| External voice | Ariane voice adapter | Ariane Runtime | Candidate navigation intent | Local deterministic validation decides execution |
| Release production | Build Farm | Artifact registry and activation owner | Artifact, provenance, SBOM, tests, evidence, and Release Set | Authority begins only after required activation |
| Node lifecycle | Control Plane or release process | kOA Node Agent | Deployment and activation contract | Node Agent cannot invent policy or component authority |

Every interaction has one producer responsibility, one consumer responsibility, an explicit contract, and a defined failure owner.

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision | Closed system question |
| --- | --- |
| `DEC-SYS-001` | kOA is a local-first modular operating environment rather than one universal appliance specification. |
| `DEC-AI-001` | The authoritative native baseline contains no generative or autonomous AI. |
| `DEC-SENT-001` | SenTient is optional, isolated, non-authoritative, and task-activated only in approved development or build profiles. |
| `DEC-MEDIATHEQUE-001` | Native kOA Mediatheque processing is deterministic; Suno and Gamma are explicit external adapters. |
| `DEC-ARI-001` | Ariane local navigation is non-AI; external voice is optional and removable. |
| `DEC-PROFILE-001` | Deployments use seven primary profiles and three composable overlays. |
| `DEC-DATA-001` | Logical component data ownership is mandatory and direct cross-component source writes are prohibited. |
| `DEC-GOV-001` | Resource Governor and Governance Policy Runtime are separate authorities. |
| `DEC-UCKK-EXT-001` | Publication Gateway authorizes disclosure before the UCKK Publication Bridge performs target-specific packaging and transport. |
| `DEC-SHELL-001` | Standard desktops are permitted; appliance shell restrictions are overlay-scoped. |
| `DEC-CONTAINER-001` | Container-runtime choices are profile-scoped and not application authority. |
| `DEC-K8S-001` | Kubernetes is not required on endpoints and is permitted only for approved infrastructure profiles. |
| `DEC-HW-001` | Hardware envelopes and concurrency limits are profile-specific architectural classes. |
| `DEC-REL-001` | System, services, governance, and knowledge are separate release channels joined by compatible Release Sets. |

### Prohibited assumptions

- Every profile contains every component.
- Every component is always running.
- A mode is equivalent to a deployment profile.
- Linux-specific implementation choices are global product requirements.
- GNOME is prohibited globally.
- Podman, Docker, systemd, Quadlet, Wayland, or Kubernetes is universally required.
- A shared database process permits shared authoritative tables.
- Konnaxion, Orgo, Kristal, or SemantiK Architect become native kOA-Linux components merely because they are hosted or integrated.
- Kristal is a universal workflow engine or operational database.
- Resource Governor may authorize disclosure or privilege.
- Governance Policy Runtime may schedule CPU or memory.
- UCKK Publication Bridge may bypass or replace Publication Gateway authorization.
- kOA Mediatheque may silently invoke external AI or media-generation services.
- Ariane voice failure disables local navigation.
- External outputs are authoritative on receipt.
- SenTient is part of the ordinary user baseline.
- Network access is required for all core capabilities.
- A Release Set may activate partially.
- A recipe or common deployment pattern creates global authority.
- Missing tests or evidence may be replaced by an implementation claim.

## 10. Validation Criteria

1. The metadata block parses as JSON and declares `DOC-SYS-000`, status `active`, language `en`, layer `system`, and global scope.
2. All eleven required sections are present in numerical order.
3. Every listed canonical path and JSON Pointer resolves in the assembled active corpus.
4. Every decision ID is accepted in `generated/decision-index.json`.
5. Every requirement ID appears exactly once in `generated/requirements-index.json`.
6. Every lock ID resolves to an active lock with an executable assertion or assigned manual control.
7. The operating-mode table matches `contracts/system.contract.json#/operating_modes`.
8. The capability table matches `contracts/system.contract.json#/global_capabilities`.
9. The integration table contains exactly the active integration allowlist from `contracts/integration-types.contract.json`.
10. The hardware table matches the active hardware-envelope classes in `contracts/system.contract.json`.
11. `TEST-SYS-OVR-001` validates one-primary-profile composition and overlay compatibility.
12. `TEST-SYS-OVR-002` validates component ownership and rejects cross-component source-table writes.
13. `TEST-SYS-OVR-003` verifies Resource Governor and Governance Policy Runtime separation.
14. `TEST-SYS-OVR-004` verifies that UCKK publication requires Publication Gateway authorization and target-specific bridge transport.
15. `TEST-SYS-OVR-005` verifies Ariane local navigation without external voice or AI.
16. `TEST-SYS-OVR-006` verifies deterministic kOA Mediatheque behavior and absence of automatic external-integration invocation.
17. `TEST-SYS-OVR-007` verifies the native AI prohibition and external-output candidate status.
18. `TEST-SYS-OVR-008` verifies SenTient profile availability, task activation, isolation, and non-authority.
19. `TEST-SYS-OVR-009` verifies each profile's declared offline envelope and capability-scoped degradation.
20. `TEST-SYS-OVR-010` verifies release-channel compatibility and non-partial artifact activation.
21. `TEST-SYS-OVR-011` verifies machine-readable receipts for applicable critical transitions.
22. `TEST-SYS-OVR-012` verifies traceability from system claims to decisions, requirements, locks, tests, and evidence.
23. Active prose is English and contains no unresolved marker, placeholder, or template token.
24. The generated requirement projection matches the canonical requirement registry.

These criteria define required validation. They do not claim that implementation conformance or operational evidence already exists.

## 11. Non-Normative Examples

> **Non-normative example:** A `user_lightweight` deployment runs local navigation, Konnaxion, Orgo, Kristal Runtime, the language runtime, kOA Mediatheque, and Resource Governor within its resource envelope. SenTient, build workbenches, and heavy search engines are absent or stopped. One heavy media task runs at a time.

> **Non-normative example:** A developer uses two branches of Konnaxion in separate workspaces. Each workspace has its own dependency environment, service namespace, ports, volumes, secrets, database identities, and resource budget. A shared download cache does not become a shared mutable environment.

> **Non-normative example:** A user sends selected material to Gamma. The system discloses the outbound content, receives a candidate presentation, validates and re-imports it, records provenance, and requires approval before publication. Gamma never receives direct publication or authoritative-store access.

> **Non-normative example:** Internet connectivity fails during local work. ChatGPT, Suno, Gamma, and Ariane external voice become unavailable. Local Ariane navigation, deterministic kOA Mediatheque operations, local language artifacts, authoritative component data, and Resource Governor remain operational within the profile's offline envelope.

> **Non-normative example:** A new services-channel artifact is compatible with the active system, governance, and knowledge versions. Validation, integrity, signature, and recovery checks pass. The complete candidate is staged and activated atomically. A receipt records the transition and the prior version remains available for rollback.

> **Non-normative example:** A sovereign node uses rootless Podman, Quadlet, a minimal Wayland appliance shell, encrypted storage, and verified activation. Those choices are valid because the active profile and overlays adopt them; they do not become requirements for a standard developer workstation.

## Cross-cutting architecture patterns

The system baseline includes a final condition-triggered pattern policy for remote resilience, asynchronous quarantine, multi-owner workflows, large payload references, experience-specific view adapters, read projections, and cache-aside. These mechanisms preserve component authority and offline continuity rather than creating a new platform layer.

## kOA Spaces Placement

kOA Spaces sits above profile-selected systems as the optional global experience layer. It composes the module selector, active-module sidebar, top bar, presentation routing, and shared page surface from validated artifacts. It is outside the privileged core and outside every contributing system's business authority.
