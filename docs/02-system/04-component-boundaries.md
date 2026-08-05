<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-004",
  "document_class": "explanatory_markdown",
  "status": "active",
  "language": "en",
  "layer": "system",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/global_boundaries/components",
    "contracts/system.contract.json#/global_boundaries/data_authority",
    "contracts/system.contract.json#/resource_governance",
    "contracts/system.contract.json#/ai_boundary",
    "contracts/system.contract.json#/sentient_boundary",
    "generated/component-catalog.json#/component_model",
    "generated/component-catalog.json#/components",
    "generated/profile-catalog.json",
    "generated/assertion-index.json#/locks",
    "contracts/integration-types.contract.json#/integrations",
    "generated/traceability.json#/profile_component_links"
  ],
  "decision_ids": [
    "DEC-COMP-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-GATE-001",
    "DEC-SENT-001",
    "DEC-MEDIATHEQUE-001",
    "DEC-UCKK-EXT-001",
    "DEC-AI-001",
    "DEC-PROFILE-001",
    "DEC-LANG-001",
    "DEC-ARI-001"
  ],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-SENT-001",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-UCKK-EXT-001",
    "LOCK-UCKK-EXT-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-ARI-001",
    "LOCK-ARI-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-CONST-000",
    "DOC-CONST-002",
    "DOC-SYS-000"
  ],
  "tags": [
    "system",
    "explanatory-markdown",
    "component-boundaries",
    "authority-separation",
    "data-ownership"
  ]
}
KOA:DOC-META:END -->

# Component Boundaries

## 1. Purpose

This document defines the global component-boundary model of the kOA operating environment.

It establishes how first-class components are identified, how responsibilities and authoritative data are assigned, how components communicate, and which forms of coupling are prohibited.

The boundary model exists to ensure that:

- every system responsibility has an explicit owner;
- every authoritative data domain has one logical owner;
- components remain independently understandable, testable, replaceable, recoverable, and governable;
- optional components can be removed without weakening the mandatory baseline;
- profile-specific deployment choices do not redefine global responsibilities;
- integration failures remain contained;
- cross-domain disclosure remains distinct from ordinary component communication;
- implementation convenience does not create hidden authority.

A component boundary is an authority boundary, a responsibility boundary, a data-ownership boundary, and an observable contract boundary. It is not merely a process, package, repository, service, container, or user-interface boundary.

## 2. Scope

This document applies globally to:

- all first-class kOA components;
- all component contracts under `contracts/components/`;
- all component documentation under `04-components/`;
- all deployment profiles and overlays;
- all runtime, gateway, broker, workbench, platform, agent, and service components;
- all component-owned authoritative data;
- all synchronous and asynchronous component communication;
- all local and remote integration paths;
- all cross-domain publication and ingestion paths;
- all component lifecycle, degradation, recovery, and replacement behavior.

It governs logical boundaries in every deployment profile.

A profile may:

- place multiple components in one process;
- place multiple logical data stores in one database service;
- separate components into different services, containers, hosts, or trust domains;
- omit components that are optional for that profile;
- apply stronger physical isolation.

A profile does not merge logical ownership, transfer responsibilities, permit undeclared writes, or broaden component authority merely because components share a process, host, database engine, network, or operator.

This document does not define every API method, event, message schema, database table, port, socket, command, file layout, or deployment unit. Those details belong to component contracts, integration contracts, profile contracts, artifact contracts, and implementation recipes.

## 3. Canonical References

| Canonical reference | Ownership |
| --- | --- |
| `generated/authority-manifest.json` | Active authority order and registry activation. |
| `generated/decision-index.json` | Accepted owner decisions for component identity, scope, and separation. |
| `contracts/system.contract.json#/global_boundaries/components` | Global cross-component communication and ownership boundary. |
| `contracts/system.contract.json#/global_boundaries/data_authority` | Global logical data-ownership and physical-consolidation boundary. |
| `contracts/system.contract.json#/resource_governance` | Separation of resource-allocation and governance-policy authority. |
| `contracts/system.contract.json#/ai_boundary` | Global native and external AI boundary. |
| `contracts/system.contract.json#/sentient_boundary` | SenTient optionality, isolation, activation, and authority boundary. |
| `generated/component-catalog.json#/component_model` | Component identity, contract ownership, data ownership, and integration model. |
| `generated/component-catalog.json#/components` | Active first-class component inventory and high-level responsibility boundaries. |
| `generated/profile-catalog.json` | Active profile and overlay catalog and composition rules. |
| `generated/assertion-index.json#/locks` | Executable cross-file boundary and ownership invariants. |
| `contracts/integration-types.contract.json#/integrations` | External integration classification and authority boundaries. |
| `generated/component-catalog.json#/components` | Active detailed component-contract inventory. |
| `generated/traceability.json#/profile_component_links` | Profile-to-component traceability. |

The component registry owns the high-level boundary facts.

A detailed component contract owns:

- observable interfaces;
- accepted inputs;
- produced outputs;
- commands and events;
- component-specific states;
- dependency behavior;
- failure behavior;
- receipts;
- compatibility constraints.

Markdown explains those facts and does not create a competing component inventory or data-owner map.

## 4. Model and Responsibilities

### 4.1 Component definition

A component is a stable architectural unit that has:

- one unique component identifier;
- one responsibility boundary;
- one declared authority class;
- zero or more authoritative data domains;
- explicit dependencies;
- explicit inputs and outputs;
- explicit profile applicability;
- declared failure and degradation behavior;
- an active component contract;
- traceable decisions, requirements, locks, tests, and evidence.

A component may have multiple deployable processes or artifacts.

Multiple components may share a deployable artifact only when their logical boundaries, identities, interfaces, data ownership, observability, and lifecycle effects remain explicit.

### 4.2 First-class component set

The canonical first-class component set is owned by `generated/component-catalog.json`.

The active set includes:

| Component | Primary responsibility boundary |
| --- | --- |
| Ariane Runtime | Deterministic local navigation and user interaction orchestration; optional external voice is an integration, not local authority. |
| Audit Broker | Collection, routing, and selective preservation of declared audit and evidence events. |
| GF Wordbench | Development-time grammatical construction, compilation, and validation. |
| Governance Policy Runtime | Authorization, disclosure, consent, privileged decisions, and governed exceptions in profiles that deploy it. |
| Identity and Trust | Identity verification, trust evaluation, credentials, and trust-root use within declared scopes. |
| Konnaxion | Its registered product-domain responsibilities and authoritative data, independent from Orgo and other first-class components. |
| Kristal Runtime | Consumption and presentation of verified Kristal artifacts without becoming a universal workflow engine or operational database. |
| kOA Node Agent | Node-local lifecycle, health, activation, recovery, and declared host-facing operations within its privilege contract. |
| Orgo | Its registered task, organization, and orchestration responsibilities without owning unrelated component state. |
| Publication Gateway | Governed cross-domain disclosure and publication. |
| Resource Governor | Deterministic resource allocation, limits, scheduling constraints, and enforcement. |
| SemantiK Architect Runtime | Runtime consumption of compiled language artifacts; it does not perform development-time grammar construction. |
| SenTient | Optional, isolated, task-activated, non-authoritative research workbench. |
| UCKK Publication Bridge | User-selected publication to an authorized external UCKK Moodle destination under the applicable ownership and policy contract. |
| kOA Mediatheque | Deterministic native media identity, storage, processing, derived artifacts, export, backup, and restore. |

The registry may evolve through accepted decisions and ADRs. Component identity is not inferred from repository names, processes, UI labels, or historical architecture.

### 4.3 Responsibility ownership

Every system responsibility has one canonical owner.

A component may:

- execute its owned responsibilities;
- delegate a bounded operation through a declared contract;
- consume another component's output;
- request a policy or identity decision;
- publish an event or receipt;
- expose a derived or cached projection.

A component does not transfer responsibility merely by delegating execution.

A consuming component does not become the owner of the data or decision it consumes.

### 4.4 Authoritative data ownership

Each authoritative data domain has exactly one logical component owner.

Logical ownership remains constant even when:

- multiple component schemas share one database server;
- a lightweight profile consolidates physical storage;
- replicas or caches exist;
- data is exported;
- an index or projection is generated;
- backup or restore systems hold copies;
- an audit system records evidence about the data.

The owner defines the authoritative write path and state transitions.

Other components interact through declared interfaces, commands, events, import contracts, or publication contracts.

A cache, index, preview, report, search document, receipt, or projection does not replace its source authority.

### 4.5 Component identities

Each component uses its own logical identity for:

- authorization;
- data access;
- service-to-service communication;
- audit attribution;
- artifact activation;
- secrets and credentials;
- policy evaluation.

Physical consolidation does not permit shared unrestricted credentials.

A profile may implement identities through separate operating-system users, service identities, workload identities, database roles, certificates, tokens, or another declared mechanism.

### 4.6 Contracted communication

Permitted communication classes are:

| Class | Purpose |
| --- | --- |
| Request/response | Bounded query or command through a declared interface. |
| Event | Notification of a completed or observed state transition. |
| Receipt/evidence | Machine-readable proof of a critical transition or decision. |
| Artifact exchange | Transfer of a versioned, validated artifact. |
| Publication | Governed disclosure across an authority or domain boundary. |
| Ingestion | Controlled intake of user-selected or externally supplied material. |
| Read-only projection | Derived, non-authoritative representation of source data. |
| Health/capability signal | Bounded operational status without hidden control authority. |

Every communication path declares:

- producer;
- consumer;
- purpose;
- data classification;
- authority semantics;
- compatibility contract;
- failure behavior;
- retry and idempotency behavior when applicable;
- evidence requirements when applicable.

### 4.7 Dependency model

A dependency is explicit and directional.

Dependency types include:

- runtime required;
- runtime optional;
- control;
- identity;
- policy;
- audit;
- data read;
- data transport;
- publication;
- build-only.

A component does not assume that co-location creates a dependency or that network reachability grants access.

Circular runtime dependencies are prohibited unless an accepted decision, contract design, and validation rule demonstrate that startup, degradation, recovery, and replacement remain deterministic. The default is an acyclic dependency graph.

### 4.8 Authority-separation pairs

#### Resource Governor and Governance Policy Runtime

The Resource Governor owns deterministic resource allocation and enforcement.

The Governance Policy Runtime owns authorization, disclosure, consent, privilege, and governed-exception decisions within its profile scope.

Neither component owns the other's decisions.

A policy decision may constrain resource use. Resource pressure does not create, modify, or bypass policy.

#### Publication Gateway and UCKK Publication Bridge

The Publication Gateway owns governed disclosure and publication across domains.

The UCKK Publication Bridge owns only UCKK-specific package, transfer, retry, and destination-receipt state after Publication Gateway authorization.

Ingestion does not imply publication. Publication does not imply ownership of kOA Mediatheque source media or dimensions.

#### GF Wordbench and SemantiK Architect Runtime

GF Wordbench owns development-time grammar construction and compilation.

SemantiK Architect Runtime consumes compiled artifacts at runtime.

The runtime does not silently compile or redefine grammar authority.

#### Ariane Runtime and external voice services

Ariane Runtime owns deterministic local navigation and interaction orchestration.

Approved external voice services supply optional voice processing through integration contracts.

The voice provider does not own local navigation state, authority, policy, or action execution.

#### SenTient and authoritative components

SenTient may inspect approved inputs and produce isolated research output.

Its output remains non-authoritative until an explicit authorized transition imports or applies it through the owning component's contract.

### 4.9 Cross-cutting components

A cross-cutting component provides a bounded service used by multiple components.

Cross-cutting use does not grant universal authority.

Examples include:

- Identity and Trust;
- Audit Broker;
- Resource Governor;
- Governance Policy Runtime;
- Kristal Runtime;
- kOA Node Agent.

Each remains limited to its registered responsibility and data domains.

### 4.10 Optionality

Optionality is declared per profile and capability.

An optional component:

- is not required for the profile's mandatory baseline;
- can be absent without hidden substitution;
- has explicit dependency effects;
- does not become mandatory because it is commonly deployed;
- does not acquire broader authority when activated.

SenTient is optional and non-authoritative.

External AI services are integrations, not mandatory local components.

### 4.11 Deployment topology independence

Logical architecture is independent from physical topology.

The same component may be deployed as:

- an in-process module;
- a local service;
- a rootless container;
- a system service;
- a remote service;
- a profile-specific appliance service.

Topology choices do not alter responsibility, logical data ownership, required identity, or contract semantics.

### 4.12 Replacement and evolution

A component may be replaced only when the replacement:

- uses the same component identity or follows an accepted identity-succession decision;
- satisfies the active component contract;
- preserves or migrates authoritative data;
- preserves required receipts and evidence;
- respects profile and security boundaries;
- passes compatibility and conformance validation.

A new implementation is not a new component merely because its technology changes.

A new responsibility boundary is not added to an existing component merely because implementation reuse is convenient.

## 5. Applicable Canonical Constraints

This document does not create an independent component-requirement set. Product boundary authority remains in the accepted decisions, canonical registries, active component contracts, and Interfile Alignment Locks referenced by this document.

| Canonical constraint | Boundary covered |
| --- | --- |
| `LOCK-COMP-001` | Kristal identity remains independent from tenant workflow and interface state. |
| `LOCK-COMP-002` | Language construction remains separate from runtime consumption of compiled artifacts. |
| `LOCK-DATA-001` | Direct writes to another component's authoritative source tables are prohibited. |
| `LOCK-GOV-001` | Resource Governor and Governance Policy Runtime remain separate authorities. |
| `LOCK-UCKK-EXT-001` | UCKK publication transport cannot bypass Publication Gateway authorization or own local media. |
| `LOCK-SENT-001` | SenTient remains optional, isolated, task-activated, and non-authoritative. |
| `LOCK-MEDIATHEQUE-001` | Native kOA Mediatheque processing remains deterministic and non-AI. |
| `LOCK-UCKK-EXT-001` | Suno and Gamma remain optional, user-triggered external media integrations. |
| `LOCK-AI-001` | The global baseline contains no native AI capability. |
| `LOCK-AI-002` | External AI output remains candidate input and cannot directly mutate authoritative state. |
| `LOCK-PROFILE-001` | Profile-specific rules do not become global implicitly. |
| `LOCK-PROFILE-002` | Profile inheritance and overlay composition remain explicit. |
| `LOCK-ARI-001` | Ariane local navigation remains available without external voice. |
| `LOCK-ARI-002` | External voice remains optional and non-authoritative. |

A future product requirement projection may be added only after its requirement identifiers, statements, decisions, tests, evidence, and traceability links are active in their canonical registries.

## 6. Procedures or State Transitions

### 6.1 Registering a component

A component becomes part of the active system through this ordered procedure:

1. accept the owner decision defining its responsibility boundary;
2. assign a permanent component identifier and display name;
3. classify the component;
4. define its authority class;
5. assign owned responsibilities;
6. assign authoritative data domains;
7. declare prohibited overlaps;
8. declare profile applicability;
9. declare dependencies and failure behavior;
10. create the detailed component contract;
11. create the explanatory component document;
12. add requirements and locks;
13. add traceability to decisions, profiles, tests, and evidence;
14. validate ownership uniqueness and dependency coherence;
15. activate the registry, contract, and documentation records together.

A repository or implementation may exist before registration, but it has no active architectural authority as a component.

### 6.2 Adding a responsibility

To add or move a responsibility:

1. identify the existing canonical owner;
2. accept a decision defining the new ownership;
3. update the component registry;
4. update all affected component contracts;
5. update authoritative data ownership when applicable;
6. update dependencies and integrations;
7. update requirements and locks;
8. migrate state and credentials through a declared procedure;
9. update tests, evidence, profiles, and documentation;
10. validate that no duplicate owner remains;
11. activate the change atomically.

A responsibility is never moved by editing only one component document.

### 6.3 Adding a dependency

A new dependency declares:

- source component;
- target component;
- dependency type;
- required or optional status;
- capability scope;
- contract reference;
- failure behavior;
- retry and queue behavior;
- data classification;
- authority semantics;
- profile applicability.

Validation rejects undeclared dependencies discovered in active implementation or configuration evidence.

### 6.4 Cross-component data access

A component requesting another component's data:

1. uses the owning component's declared read or query interface;
2. supplies its own identity;
3. receives only data authorized for that purpose;
4. treats the result according to its authority classification;
5. preserves provenance when storing a projection;
6. does not mutate the source through an alternate path.

A required mutation is submitted as a command to the owner.

### 6.5 Physical consolidation

A profile may consolidate physical storage when it:

1. preserves separate logical schemas or ownership partitions;
2. preserves component-specific identities and permissions;
3. prevents unauthorized cross-component writes;
4. preserves backup, restore, migration, and export semantics by owner;
5. records component attribution;
6. passes profile-specific isolation tests.

### 6.6 Component degradation

When a dependency fails, the component:

1. identifies the affected capability;
2. applies the dependency's declared failure behavior;
3. stops unauthorized mutations;
4. retains only explicitly permitted authority;
5. emits observable status and evidence;
6. avoids assuming the failed component's role;
7. recovers only after dependency and contract validation succeed.

The global safe-degradation rules remain applicable.

### 6.7 Component replacement

Replacement follows this sequence:

1. validate the replacement against the active contract;
2. verify artifact identity and compatibility;
3. stop or isolate new writes;
4. migrate or attach authoritative state;
5. verify ownership and identity controls;
6. activate atomically;
7. validate dependent components;
8. preserve rollback or forward-repair capability;
9. produce activation evidence.

### 6.8 Retiring a component

A component is retired only after:

- all owned responsibilities have accepted successor owners or are explicitly removed;
- all authoritative data has a disposition;
- all dependencies and integrations are removed or redirected;
- all profile references are updated;
- all active requirements and locks are updated;
- the contract and documentation lifecycle is updated;
- archival and migration evidence is complete.

## 7. Failure States and Safe Degradation

| Failure state | Required response |
| --- | --- |
| Component registry entry is missing | The implementation is not treated as an active first-class component. |
| Duplicate responsibility owner | Activation is blocked until one canonical owner remains. |
| Duplicate authoritative data owner | Writes are blocked and activation fails. |
| Direct cross-component database write is detected | Validation fails; the write path is removed or replaced by an owner-controlled contract. |
| Required component dependency is unavailable | The affected capability fails closed or enters its declared degraded mode. |
| Optional component is unavailable | Only explicitly dependent capabilities are disabled. |
| Component contract is missing or incompatible | New activation and dependent integration are blocked. |
| Component identity cannot be verified | Identity-bound requests are rejected. |
| Policy authority is unavailable | Policy-dependent actions are blocked; no local permission is inferred. |
| Resource authority is unavailable | Work outside a previously valid declared envelope is denied or queued according to contract. |
| Cross-domain publication fails | Local source state remains authoritative; publication is not claimed. |
| kOA Mediatheque ingestion fails | No publication is implied and no partial object becomes authoritative. |
| SenTient is unavailable | The mandatory local baseline continues without replacement. |
| Derived projection is stale or unavailable | The source authority remains valid; the projection is regenerated or marked unavailable. |
| Partial component replacement | The candidate remains non-authoritative; rollback or forward repair is used. |
| Dependency cycle prevents deterministic startup | Activation is blocked until the cycle is removed or explicitly governed by an accepted design. |

A component failure does not authorize another component to access its storage, credentials, secrets, or privilege boundary.

## 8. Cross-Component Interactions

### 8.1 Identity and Trust interactions

Components request identity and trust evaluations through declared contracts.

Identity and Trust does not perform the business operation being authorized. The consuming component remains responsible for its operation.

### 8.2 Governance Policy Runtime interactions

Components provide policy-relevant context and receive bounded decisions.

The Governance Policy Runtime does not mutate the consuming component's authoritative records. It may authorize or deny a requested transition; the owner executes the transition.

### 8.3 Resource Governor interactions

Components declare workloads and resource needs. The Resource Governor applies limits and scheduling constraints.

Components do not use the Resource Governor as a policy engine.

### 8.4 Audit Broker interactions

Components emit declared events and receipts. The Audit Broker preserves and routes them according to selective-audit rules.

The Audit Broker does not become the owner of the underlying business state.

### 8.5 Publication Gateway interactions

A source component requests publication through a disclosure contract.

The Publication Gateway verifies the governed publication conditions, produces evidence, and transfers only the authorized publication payload.

It does not become the owner of the source record.

### 8.6 UCKK Publication Bridge interactions

The gateway accepts user-selected material and transfers it into the applicable kOA Mediatheque ingestion contract.

It does not publish the material across unrelated domains and does not become the owner of the resulting kOA Mediatheque record.

### 8.7 Ariane interactions

Ariane invokes component capabilities through declared commands or navigation contracts.

Ariane does not bypass component authorization, policy, or data ownership.

An external voice service produces input for Ariane through an integration contract and does not execute component mutations directly.

### 8.8 Kristal interactions

Kristal Runtime consumes verified Kristal artifacts and presents their epistemic content according to its contract.

It does not become a universal operational database, workflow engine, or cross-component write mechanism.

### 8.9 kOA Node Agent interactions

The Node Agent performs node-local lifecycle and host-facing operations through its narrow privilege and activation contracts.

Application components do not inherit its host privilege.

### 8.10 SenTient interactions

SenTient receives only explicitly approved inputs and exports isolated research results.

Import into an authoritative component requires an explicit owner-controlled review and transition.

### 8.11 Konnaxion and Orgo

Konnaxion and Orgo remain independent first-class domains.

Neither is the universal owner of all product data, workflow, publication, policy, identity, media, language, resource, or audit behavior.

Their interactions use declared contracts and preserve their respective authoritative data domains.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Accepted decisions

| Decision | Closure |
| --- | --- |
| `DEC-COMP-001` | Establishes the expanded active first-class component inventory. |
| `DEC-DATA-001` | Requires logical component ownership while permitting profile-dependent physical isolation or consolidation. |
| `DEC-GOV-001` | Separates Resource Governor authority from Governance Policy Runtime authority. |
| `DEC-UCKK-EXT-001` | Requires Publication Gateway authorization before UCKK-specific packaging and transport. |
| `DEC-SENT-001` | Defines SenTient as isolated, optional, task-activated, and non-authoritative. |
| `DEC-MEDIATHEQUE-001` | Keeps native kOA Mediatheque processing deterministic and independent from AI-driven classification or routing. |
| `DEC-AI-001` | Establishes the strict external-AI boundary and candidate-output treatment. |
| `DEC-PROFILE-001` | Defines primary profiles and composable overlays without implicit inheritance. |
| `DEC-LANG-001` | Separates development-time language construction from runtime compiled-artifact consumption. |
| `DEC-ARI-001` | Preserves local deterministic Ariane navigation while making external voice optional. |

### 9.2 Related ADRs

| ADR | Boundary effect |
| --- | --- |
| `ADR-006` | Defines expanded first-class component boundaries. |
| `ADR-009` | Defines the Governance Policy Runtime. |
| `ADR-018` | Isolates SenTient as an optional workbench. |
| `ADR-019` | Separates resource and policy authority. |
| `ADR-020` | Separates publication and kOA Mediatheque ingestion. |
| `ADR-022` | Preserves deterministic native kOA Mediatheque responsibilities. |
| `ADR-024` | Preserves logical ownership across profile-dependent physical topologies. |

### 9.3 Prohibited assumptions

The following assumptions are prohibited:

- every repository is a component;
- every process is a component;
- every UI application owns the data it displays;
- co-location merges responsibility;
- a shared database permits shared writes;
- an index owns its source data;
- a cache is authoritative;
- audit evidence owns the observed state;
- a gateway owns all transferred data;
- an orchestrator owns all orchestrated work;
- a policy engine executes the authorized business mutation;
- a resource manager decides consent or disclosure;
- publication and ingestion are the same operation;
- runtime language consumption includes grammar development;
- an optional workbench may become a hidden dependency;
- common implementation practice creates a global boundary;
- a failed component permits another component to bypass its contract;
- replacement technology automatically creates a new component identity.

## 10. Validation Criteria

This document conforms when all of the following checks pass:

1. metadata status is `active` and document class is `explanatory_markdown`;
2. the registered path is `02-system/04-component-boundaries.md`;
3. all identifiers and canonical references resolve;
4. all listed decisions are accepted;
5. the document declares no unregistered product requirement identifiers;
6. all listed locks exist and their assertions pass;
7. every active component has one registry entry and one active component contract;
8. component identifiers are unique;
9. responsibility owners are unique;
10. authoritative data-domain owners are unique;
11. component identities are logically distinct;
12. no direct cross-component authoritative-store write exists;
13. all cross-component communication paths have declared contracts;
14. all dependencies declare direction, type, optionality, purpose, and failure behavior;
15. no component depends on itself;
16. runtime dependency cycles are absent unless explicitly governed and validated;
17. profile-specific topology preserves global logical ownership;
18. optional components can be removed from profiles that do not require them;
19. Resource Governor and Governance Policy Runtime boundaries remain separate;
20. UCKK publication follows gateway authorization and bridge transport without authority collapse;
21. GF Wordbench and SemantiK Architect Runtime boundaries remain separate;
22. Ariane local navigation does not depend on external voice;
23. SenTient is not an authority source or mandatory baseline dependency;
24. derived projections preserve source provenance;
25. component replacement tests preserve data and contract compatibility;
26. failure and recovery tests prove boundary containment;
27. active content is English;
28. no unresolved-authority marker or template token appears.

The validator reports actionable failures, including:

```text
component_missing_registry_entry
component_missing_contract
component_identifier_collision
component_responsibility_owner_collision
component_data_owner_collision
component_direct_cross_write
component_undeclared_dependency
component_dependency_cycle
component_identity_not_isolated
component_contract_reference_missing
component_profile_scope_violation
component_optional_dependency_became_mandatory
component_authority_overlap
component_projection_missing_provenance
component_replacement_incompatible
```

## 11. Non-Normative Examples

### 11.1 Shared database in the lightweight profile

Orgo and Konnaxion use the same PostgreSQL service to reduce memory use. They retain separate schemas, database roles, migrations, backup mappings, ownership records, and write paths. Neither component writes the other's tables.

### 11.2 Separate databases in a sovereign profile

The same logical components use separate database services and service identities. Their responsibility and data ownership are unchanged; only physical isolation is stronger.

### 11.3 Policy-controlled publication

Konnaxion owns a record. It requests a disclosure decision from the Governance Policy Runtime and submits the approved payload to the Publication Gateway. The gateway publishes the payload and issues a receipt. Konnaxion remains the source owner.

### 11.4 kOA Mediatheque ingestion

A user selects local media in Ariane. Ariane sends a bounded command to the kOA Mediatheque, which verifies and stores the authoritative local record. A later request to publish that record to UCKK follows Publication Gateway authorization and UCKK Publication Bridge transport. Ariane and the bridge do not become media owners.

### 11.5 Resource pressure

kOA Mediatheque requests a transcode worker. The Resource Governor permits one low-priority worker. The Governance Policy Runtime is not asked to allocate CPU, and the Resource Governor does not authorize media disclosure.

### 11.6 SenTient research result

SenTient produces a candidate classification in an isolated research workspace. The result is advisory. An authorized Konnaxion import operation reviews and accepts selected values before any authoritative Konnaxion state changes.

### 11.7 Ariane voice loss

The approved external voice integration is unavailable. Ariane retains keyboard, pointer, touch, and local deterministic navigation. No alternate voice provider or embedded AI model is activated.

### 11.8 Component implementation replacement

A new Resource Governor implementation passes the existing component contract, preserves allocation-state compatibility, and activates atomically. The technology changes; the component identity and authority boundary do not.
