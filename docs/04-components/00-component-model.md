<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-COMP-000",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "component",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/decision-index.json",
    "generated/document-index.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/integration-types.contract.json",
    "contracts/artifact-classes.contract.json",
    "contracts/release-channels.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "schemas/component-contract.schema.json"
  ],
  "decision_ids": [
    "DEC-CONST-COMP-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-GATE-001",
    "DEC-AI-001",
    "DEC-SENT-001",
    "DEC-PROFILE-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-COMP-MODEL-001",
    "REQ-COMP-MODEL-002",
    "REQ-COMP-MODEL-003",
    "REQ-COMP-MODEL-004",
    "REQ-COMP-MODEL-005",
    "REQ-COMP-MODEL-006",
    "REQ-COMP-MODEL-007",
    "REQ-COMP-MODEL-008",
    "REQ-COMP-MODEL-009",
    "REQ-COMP-MODEL-010",
    "REQ-COMP-MODEL-011",
    "REQ-COMP-MODEL-012",
    "REQ-COMP-MODEL-013",
    "REQ-COMP-MODEL-014",
    "REQ-COMP-MODEL-015",
    "REQ-COMP-MODEL-016",
    "REQ-COMP-MODEL-017",
    "REQ-COMP-MODEL-018",
    "REQ-COMP-MODEL-019",
    "REQ-COMP-MODEL-020",
    "REQ-COMP-MODEL-021",
    "REQ-COMP-MODEL-022",
    "REQ-COMP-MODEL-023",
    "REQ-COMP-MODEL-024",
    "REQ-COMP-MODEL-025",
    "REQ-COMP-MODEL-026",
    "REQ-COMP-MODEL-027",
    "REQ-COMP-MODEL-028"
  ],
  "lock_ids": [
    "LOCK-DOC-002",
    "LOCK-DOC-008",
    "LOCK-DOC-009",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-PROFILE-001",
    "LOCK-IMPL-001",
    "LOCK-AI-001",
    "LOCK-SENT-001",
    "LOCK-LIFE-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-SYS-004"
  ],
  "tags": [
    "components",
    "component-model",
    "component-contracts",
    "authority-boundaries",
    "data-ownership",
    "interfaces",
    "safe-degradation",
    "conformance"
  ]
}
KOA:DOC-META:END -->

# Component Model

## 1. Purpose

This document defines the common model for every kOA component.

A component is a bounded architectural authority with a stable identity, a declared responsibility, owned state, observable contracts, explicit dependencies, and defined failure behavior. Components collaborate through contracts while retaining separate authority, data ownership, lifecycle, and conformance obligations.

The model prevents repository structure, deployment topology, shared infrastructure, operational convenience, or repeated prose from creating implicit component authority.

## 2. Scope

This document applies to:

- every component registered in `generated/component-catalog.json`;
- every entry in `generated/component-catalog.json`;
- every individual contract under `contracts/components/`;
- every component explanation under `04-components/`;
- every effective profile that includes, excludes, requires, or optionally enables a component;
- every cross-component interface, event, artifact exchange, gateway, policy decision, resource decision, and evidence flow;
- every component-owned data set, state machine, receipt, cache, index, projection, and import;
- component activation, deactivation, upgrade, rollback, recovery, replacement, and retirement;
- component security, privacy, resources, observability, operations, tests, and evidence.

This document defines the common component contract and authority model.

It does not:

- assign detailed behavior to an individual component;
- define profile-specific component membership;
- prescribe one process, container, host, database, transport, or orchestration technology per component;
- make a shared library or implementation package a component automatically;
- duplicate canonical component identities, interfaces, states, capabilities, or resource values;
- replace component-specific contracts, profile contracts, artifact contracts, or integration contracts.

## 3. Canonical References

| Canonical reference | Ownership role |
| --- | --- |
| `generated/component-catalog.json#/components` | Owns component identity, classification, primary responsibility, high-level authority boundary, and the canonical contract reference. |
| `generated/component-catalog.json#/components` | Owns contract catalog membership, contract paths, active versions, and lifecycle status. |
| `contracts/components/*.component.json` | Owns detailed observable behavior for each component. |
| `schemas/component-contract.schema.json` | Defines the required structure of an individual component contract. |
| `schemas/component-contract-index.schema.json` | Defines the required structure of the component-contract index. |
| `contracts/profiles/*.profile.json` | Owns component membership, activation mode, deployment topology, and profile-scoped requirements. |
| `contracts/system.contract.json` | Owns global boundaries that component contracts cannot weaken. |
| `contracts/integration-types.contract.json` | Owns integration identity, classification, transfer direction, and external trust boundaries. |
| `contracts/artifact-classes.contract.json` and artifact contracts | Own artifact identity classes and observable formats. |
| `contracts/release-channels.contract.json` | Owns release-channel identity and channel membership. |
| `generated/requirements-index.json` | Owns the normative statements displayed in Section 5. |
| `generated/assertion-index.json` | Owns component, data, profile, gateway, governance, AI, implementation, and lifecycle alignment assertions. |
| `generated/traceability.json` | Owns decision, requirement, lock, test, and evidence relationships. |
| `generated/exception-index.json` | Owns approved scoped deviations and compensating controls. |
| `generated/test-catalog.json` and `generated/evidence-catalog.json` | Own component conformance test and evidence identities. |

Markdown explains the model. It does not own canonical component values.

## 4. Model and Responsibilities

### 4.1 Component identity

Every component identity resolves across four canonical layers:

| Layer | Responsibility |
| --- | --- |
| Component registry | Stable component identity, display identity, classification, primary responsibility, high-level authority boundary |
| Component-contract index | Contract catalog membership, path, active version, lifecycle |
| Individual component contract | Observable behavior, owned data, interfaces, events, states, dependencies, failure, security, resources, lifecycle, validation |
| Effective profile | Membership, activation mode, topology, profile-scoped limits, physical isolation, profile conformance |

These layers are complementary. None silently absorbs the ownership of another.

### 4.2 Component qualification

An architectural unit qualifies as a component when it has:

- a responsibility that remains meaningful independently from implementation packaging;
- state, decisions, artifacts, or observable behavior that need an explicit owner;
- a stable interface boundary;
- independent lifecycle or compatibility obligations;
- explicit failure ownership;
- profile membership that can be resolved;
- testable conformance conditions.

A library, module, worker, process, container, database, host, or deployment unit is not automatically a component. It can implement part of a component or host several components.

### 4.3 Responsibility boundary

A component contract distinguishes:

- responsibilities it owns;
- responsibilities owned elsewhere;
- authoritative and derived state;
- accepted candidate inputs;
- observable interfaces;
- emitted and consumed events;
- artifacts it accepts and produces;
- required and optional dependencies;
- prohibited direct-access paths;
- profile applicability;
- authority and privilege boundaries;
- failure and recovery behavior.

The primary responsibility remains singular enough to identify why the component exists. Supporting responsibilities remain bounded by that primary purpose.

### 4.4 Authority classes

Component behavior can involve several authority roles:

| Authority role | Meaning |
| --- | --- |
| Authoritative owner | Validates and applies accepted state transitions for its owned domain |
| Custodian | Stores, transports, backs up, or processes data without acquiring semantic ownership |
| Gateway | Controls a declared trust, disclosure, publication, or ingestion boundary |
| Broker | Executes a narrow mediated action without acquiring source-domain ownership |
| Derived processor | Produces a cache, index, projection, preview, analysis, or candidate artifact |
| Advisory workbench | Produces reviewed candidate output without native system authority |
| Coordinator | Coordinates contracts while each target retains its own mutation authority |

The canonical classification for a concrete component remains in the registry and contract. This table explains roles rather than defining a competing enum.

### 4.5 Data authority

The owning component controls:

- accepted identifiers and schemas;
- invariants and state transitions;
- mutation interfaces;
- retention and deletion behavior;
- export and import behavior;
- backup and restore behavior;
- compatibility and migration behavior;
- evidence for critical transitions.

Caches, replicas, indexes, analytical stores, search stores, generated views, AI contexts, and receipts remain derived or evidentiary unless an accepted owner decision explicitly transfers canonical ownership.

### 4.6 Interfaces and interactions

A component can expose:

- queries that return authorized views;
- commands that request owner-controlled transitions;
- events that report occurred facts;
- artifact import and export contracts;
- gateways that cross trust or disclosure boundaries;
- administrative operations;
- health and readiness interfaces;
- evidence and receipt interfaces.

Every interface declares its direction, caller or destination, input or output contract, version, authentication, authorization, idempotency or replay behavior, timeout, failure outcomes, and authoritative effect.

Internal implementation details are not stable public interfaces unless the active contract explicitly exposes them.

### 4.7 Events and messaging

An emitted event describes an accepted fact or state transition. It does not transfer ownership of the producer's source state.

Where a local authoritative commit emits an external event, the component contract defines an atomic publication pattern such as a transactional outbox or an accepted equivalent.

Consumers declare idempotency, duplicate behavior, ordering assumptions, replay behavior, and poison-input handling. Queue and retry growth remain finite.

### 4.8 Dependencies

Dependencies are classified as:

- required;
- optional;
- profile-conditional;
- integration-conditional;
- prohibited.

A dependency declaration includes:

- dependency identity;
- required capability;
- authority retained by the dependency;
- startup and readiness behavior;
- timeout and retry ownership;
- failure impact;
- recovery behavior.

Dependency direction does not transfer responsibility. Circular dependencies require an accepted decision and explicit startup, recovery, deadlock, replay, and evidence rules.

### 4.9 Profile participation

Profile contracts determine whether a component is:

- required;
- optional;
- excluded;
- prohibited.

They also determine activation mode, deployment topology, profile-specific resource envelopes, physical isolation, offline behavior, and conformance evidence.

Global logical component and data ownership remains stable across profiles unless an accepted global owner decision changes it.

### 4.10 Lifecycle and artifacts

Component lifecycle includes:

- contract activation;
- runtime activation;
- artifact verification;
- version compatibility;
- atomic update;
- rollback or forward repair;
- migration;
- deprecation;
- supersession;
- retirement.

The applicable artifact contract owns artifact structure. The release-channel registry owns channel identity. The component contract owns how the component validates, admits, activates, uses, rejects, and recovers from those artifacts.

### 4.11 Security, resources, and operations

A component contract separates:

- authentication from authorization;
- application authority from host privilege;
- Governance Policy Runtime decisions from component mutations;
- Resource Governor decisions from business authorization;
- public accountability information from restricted evidence;
- secrets from ordinary logs, receipts, exports, and images.

The contract also defines health, readiness, degraded state, bounded logs, metrics, backup scope, restore validation, maintenance, queues, retries, timeouts, concurrency, and safe shutdown.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-COMP-MODEL-001,REQ-COMP-MODEL-002,REQ-COMP-MODEL-003,REQ-COMP-MODEL-004,REQ-COMP-MODEL-005,REQ-COMP-MODEL-006,REQ-COMP-MODEL-007,REQ-COMP-MODEL-008,REQ-COMP-MODEL-009,REQ-COMP-MODEL-010,REQ-COMP-MODEL-011,REQ-COMP-MODEL-012,REQ-COMP-MODEL-013,REQ-COMP-MODEL-014,REQ-COMP-MODEL-015,REQ-COMP-MODEL-016,REQ-COMP-MODEL-017,REQ-COMP-MODEL-018,REQ-COMP-MODEL-019,REQ-COMP-MODEL-020,REQ-COMP-MODEL-021,REQ-COMP-MODEL-022,REQ-COMP-MODEL-023,REQ-COMP-MODEL-024,REQ-COMP-MODEL-025,REQ-COMP-MODEL-026,REQ-COMP-MODEL-027,REQ-COMP-MODEL-028 -->
- **REQ-COMP-MODEL-001 — SHALL:** Every active component has one stable component identifier, one declared primary responsibility, one accountable owner, and one active component contract.
- **REQ-COMP-MODEL-002 — SHALL:** The components registry is the canonical owner of component identity, classification, primary responsibility, high-level authority boundary, and canonical contract reference.
- **REQ-COMP-MODEL-003 — SHALL:** The component-contract index is the canonical owner of component-contract catalog membership, contract path, active version, and lifecycle status.
- **REQ-COMP-MODEL-004 — SHALL:** Each individual component contract owns its observable interfaces, authoritative data declarations, state transitions, events, artifacts, dependencies, failure behavior, security boundary, resource behavior, lifecycle behavior, and validation requirements.
- **REQ-COMP-MODEL-005 — SHALL:** Profile contracts own component membership, activation mode, deployment topology, profile-scoped resource envelopes, and profile-scoped physical isolation.
- **REQ-COMP-MODEL-006 — SHALL NOT:** A Markdown document, recipe, generated projection, current implementation, deployment manifest, or profile silently redefines a component's canonical identity or responsibility.
- **REQ-COMP-MODEL-007 — SHALL:** Every authoritative data set and state machine exposed by a component identifies exactly one canonical owning component or canonical owning registry.
- **REQ-COMP-MODEL-008 — SHALL NOT:** A component writes directly to another component's authoritative tables, private files, private queues, internal object namespaces, or private state.
- **REQ-COMP-MODEL-009 — SHALL:** Every cross-component query, command, event, artifact transfer, gateway transfer, policy decision, resource decision, and evidence submission uses an explicit active contract.
- **REQ-COMP-MODEL-010 — SHALL:** Every authority-bearing interaction identifies the source, destination, direction, operation, contract version, authorization boundary, resource boundary, failure owner, and required evidence.
- **REQ-COMP-MODEL-011 — SHALL:** A component validates identity, schema, compatibility, authorization, replay constraints, and applicable profile conditions before applying an authoritative mutation.
- **REQ-COMP-MODEL-012 — SHALL NOT:** A query result, cache, index, replica, analytical result, AI context, external AI output, receipt, or generated projection becomes authoritative solely because it contains or describes component data.
- **REQ-COMP-MODEL-013 — SHALL:** Derived data records its authoritative source, derivation purpose, synchronization or generation state, invalidation behavior, and permitted use.
- **REQ-COMP-MODEL-014 — SHALL:** Candidate input becomes authoritative only after the owning component accepts it through an explicit import, command, or admission contract.
- **REQ-COMP-MODEL-015 — SHALL:** Every active component contract declares required dependencies, optional dependencies, prohibited dependencies, and the capability impact of dependency loss.
- **REQ-COMP-MODEL-016 — SHALL:** Failure or removal of an optional component or integration remains bounded to the capabilities that explicitly depend on it.
- **REQ-COMP-MODEL-017 — SHALL NOT:** Failure, unavailability, or removal of a component transfers its authority to another component by implication.
- **REQ-COMP-MODEL-018 — SHALL:** Every component contract defines bounded queues, retries, timeouts, concurrency, cancellation, shutdown, replay, and poison-input behavior where those mechanisms apply.
- **REQ-COMP-MODEL-019 — SHALL:** Every component contract distinguishes component authority, Governance Policy Runtime authority, Resource Governor authority, gateway authority, artifact authority, and host-privilege authority where those boundaries apply.
- **REQ-COMP-MODEL-020 — SHALL NOT:** A component broadens its own authority because it is co-located with another component, uses shared infrastructure, performs coordination, holds a replica, or has administrative access.
- **REQ-COMP-MODEL-021 — SHALL:** Versioned artifact activation verifies identity, artifact class, release channel, compatibility, integrity, required trust, and authorization before atomic activation.
- **REQ-COMP-MODEL-022 — SHALL:** A component preserves the last valid authoritative state during failed activation and provides declared rollback or forward-repair behavior.
- **REQ-COMP-MODEL-023 — SHALL:** Every critical component transition produces machine-readable evidence identifying the initiating authority, subject, operation, contract, result, and recovery state.
- **REQ-COMP-MODEL-024 — SHALL:** A component is active only in effective profiles that declare it as required or optional and satisfy all of its declared prerequisites.
- **REQ-COMP-MODEL-025 — SHALL NOT:** A component's existence in the repository, component catalog, installation image, or running process proves that the component is active or conformant in a profile.
- **REQ-COMP-MODEL-026 — SHALL:** A semantic change to component identity, responsibility, authoritative data ownership, dependency direction, interface authority, or failure semantics is activated only with an accepted decision, impact analysis, updated contracts, requirements, locks, tests, and evidence.
- **REQ-COMP-MODEL-027 — SHALL:** Component retirement or replacement preserves identifiers, data lineage, compatibility policy, migration behavior, predecessor deactivation, and historical evidence.
- **REQ-COMP-MODEL-028 — SHALL:** Every active component requirement is traceable to accepted decisions, applicable locks, validation tests, and required evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Introducing a component

A new component is introduced by:

1. defining the bounded responsibility and adjacent owners;
2. recording an accepted owner decision;
3. assigning a stable component identifier;
4. registering the component and canonical contract reference;
5. creating the indexed component contract;
6. declaring authoritative and derived data;
7. declaring interfaces, events, artifacts, dependencies, and prohibited access paths;
8. declaring profile participation and prerequisites;
9. declaring security, resource, lifecycle, failure, recovery, and evidence behavior;
10. registering requirements, locks, tests, and evidence;
11. validating the complete authority and dependency graph;
12. activating the registry, contract, profile, and documentation changes atomically.

A repository package or running process does not create an active component before this sequence completes.

### 6.2 Processing an authority-bearing command

The receiving component:

1. resolves the source identity and active contract;
2. verifies authentication and trust;
3. resolves applicable profile and capability conditions;
4. obtains required policy authorization;
5. obtains required resource admission;
6. validates schema, compatibility, invariants, idempotency, and replay constraints;
7. applies the transition through its own authoritative state machine;
8. emits required events and evidence;
9. returns the component-owned result.

A coordinator, gateway, broker, or policy service does not replace the owning component's transition.

### 6.3 Accepting candidate input

Candidate input follows this sequence:

1. identify the source and transfer contract;
2. classify the input as unverified or candidate;
3. verify schema, identity, integrity, provenance, compatibility, and authorization;
4. quarantine or reject invalid input;
5. present valid candidate input to the owning component;
6. apply owner-specific validation and conflict rules;
7. create authoritative state only after owner acceptance;
8. record the acceptance or rejection outcome.

### 6.4 Changing a component boundary

A responsibility, data-ownership, dependency-direction, or interface-authority change:

1. records an accepted owner decision;
2. calculates transitive impact;
3. updates the component registry;
4. updates the component-contract index and affected contracts;
5. updates profiles, integrations, artifacts, requirements, and locks;
6. defines migration, compatibility, predecessor behavior, and recovery;
7. updates tests, evidence, documentation, and generated contexts;
8. validates all affected interactions;
9. activates the replacement boundary last.

### 6.5 Retiring or replacing a component

Retirement or replacement:

1. identifies the successor or declares that no successor exists;
2. prevents new undeclared adoption;
3. migrates or exports authoritative data through an active contract;
4. drains or records accepted work;
5. disables predecessor mutation paths;
6. preserves historical identifiers and evidence;
7. validates dependent profile and component behavior;
8. activates the successor or removal atomically;
9. retains rollback or forward-repair behavior for the declared transition.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Preserved authority | Blocked or degraded behavior | Evidence |
| --- | --- | --- | --- | --- |
| Component registry and contract identity disagree | Block activation | Last valid component authority | Conflicting component version | Identity-alignment failure |
| Required component contract is absent or invalid | Keep component inactive | Other valid components | Component capabilities | Contract-validation failure |
| Profile membership cannot be resolved | Keep component inactive | Effective profile without the unresolved component | Component activation and conformance claim | Profile-resolution failure |
| Caller identity or authorization is invalid | Reject before mutation | Current component state | Requested operation | Authentication or authorization record |
| Interface or artifact version is incompatible | Reject before mutation or activation | Current compatible state | Incompatible operation | Compatibility failure |
| Required dependency is unavailable | Enter declared capability-specific degradation | Unaffected component capabilities | Dependent capability | Dependency-health record |
| Optional dependency is unavailable | Keep only the optional capability unavailable | Core component authority | Optional capability | Optional-dependency status |
| Queue, retry, or timeout bound is reached | Stop automatic progression and expose a terminal or intervention state | Existing authoritative state | Further automatic attempts | Bound-exhaustion evidence |
| Derived data is stale or source identity is unknown | Invalidate, quarantine, or rebuild derived data | Authoritative source | Use of derived data as current | Derivation-state evidence |
| Resource admission is unavailable | Keep new resource-dependent work blocked | Existing bounded work | New unresolved work | Resource-decision failure |
| Required policy decision is unavailable | Keep governed action blocked | Non-gated component behavior | Policy-gated operation | Policy-resolution failure |
| Artifact activation fails | Preserve or restore the last valid state | Previous active artifact and component state | Candidate activation | Activation and recovery receipt |
| Evidence path is unavailable | Apply the component's declared synchronous-fail or bounded-evidence-queue behavior | Source transition authority | Transition requiring unavailable mandatory evidence | Evidence-path status |
| Storage pressure occurs | Protect authoritative state and remove or pause regenerable work first | Authoritative data | Cache, index, preview, or optional ingestion | Storage-pressure record |
| Ownership conflict is detected | Block the affected authority claim | Last valid owner | Parallel ownership or mutation | Ownership-conflict report |

## 8. Cross-Component Interactions

### 8.1 Interaction classes

| Interaction class | Permitted effect | Authority rule |
| --- | --- | --- |
| Query | Returns an authorized view | Consumer does not acquire source ownership |
| Command | Requests a state transition | Owning component validates and applies it |
| Event | Reports an occurred fact | Consumer follows the event contract and replay rules |
| Artifact transfer | Transfers an immutable or versioned artifact | Receiving owner controls admission and activation |
| Gateway transfer | Crosses a trust, disclosure, publication, or ingestion boundary | Gateway controls only its declared boundary |
| Policy decision | Returns an authorization outcome | Policy service does not execute the application mutation |
| Resource decision | Returns or applies a resource grant | Resource service does not authorize business behavior |
| Evidence submission | Records a transition or proof | Evidence system does not rewrite source state |

### 8.2 Required interaction fields

Every active cross-component interaction identifies:

- source and destination components;
- direction and interaction class;
- active contract and version;
- input and output schemas;
- authentication and trust mechanism;
- authorization point;
- authoritative owner of every affected state;
- idempotency, ordering, replay, timeout, and retry behavior;
- resource and queue bounds;
- failure owner;
- audit or receipt behavior;
- prohibited direct-access path.

### 8.3 Required separations

The component model preserves these system separations:

- Resource Governor remains separate from Governance Policy Runtime.
- Publication Gateway authorizes disclosure before UCKK Publication Bridge performs UCKK-specific packaging and transport.
- Kristal epistemic identity remains separate from workflow and interface state.
- The user language runtime remains separate from the language-construction workbench.
- SenTient remains optional, isolated, and non-authoritative.
- External AI surfaces remain outside native component authority.
- Evidence custody remains separate from source-state mutation.
- Profile deployment topology remains separate from global logical ownership.

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Effect |
| --- | --- |
| `DEC-CONST-COMP-001` | Establishes component separation as a global constitutional property. |
| `DEC-DATA-001` | Establishes logical data ownership independently of profile-dependent physical isolation. |
| `DEC-GOV-001` | Separates Resource Governor authority from Governance Policy Runtime authority. |
| `DEC-UCKK-EXT-001` | Requires Publication Gateway authorization before UCKK-specific packaging and transport. |
| `DEC-AI-001` | Keeps native component authority free of generative AI and autonomous AI decision paths. |
| `DEC-SENT-001` | Keeps SenTient optional, isolated, and non-authoritative. |
| `DEC-PROFILE-001` | Establishes explicit primary profiles and overlays that own component membership conditions. |
| `DEC-REL-001` | Establishes release-channel identity and compatible Release Sets. |

### Prohibited assumptions

- a package, service, process, container, database, or host is automatically a component;
- repository presence proves profile membership;
- runtime presence proves conformance;
- a component owns data because it reads, stores, indexes, backs up, or coordinates that data;
- shared infrastructure creates shared authority;
- administrative access grants semantic ownership;
- a coordinator can mutate target state directly;
- a gateway owns the source or destination domain;
- a policy decision performs the governed action;
- a resource grant authorizes the business action;
- an event consumer owns the producer's source state;
- a cache, replica, receipt, or generated context is authoritative;
- an optional dependency can disable unrelated core capabilities;
- failure transfers authority silently;
- a recipe or current implementation defines the canonical component boundary;
- missing component behavior can be inferred from a similar component;
- a profile can weaken a global prohibition;
- repeated Markdown creates a new canonical responsibility.

## 10. Validation Criteria

This document is conformant when:

1. `DOC-COMP-000` is active at `04-components/00-component-model.md`.
2. Every canonical reference resolves.
3. Every listed decision exists with status `accepted`.
4. Every requirement in Section 5 exists with identical strength, statement, scope, owner, source decision, and validation mapping.
5. Every listed lock exists and is active.
6. Every active component has one unique component identifier.
7. Every active component resolves to one indexed active component contract.
8. Registry identity, index identity, contract identity, and documentation identity agree.
9. Every component declares one bounded primary responsibility.
10. Every authoritative data domain resolves to one owning component or registry.
11. No component contract authorizes direct writes to another component's private authoritative state.
12. Every inbound and outbound interaction references an active contract and valid schema.
13. Every authority-bearing mutation resolves authentication, authorization, profile conditions, compatibility, replay behavior, and resource admission.
14. Every derived-data declaration identifies source, purpose, state, invalidation, and permitted use.
15. Every candidate-input path terminates at an owning-component acceptance decision.
16. Every dependency declares classification, authority retained, failure impact, and recovery.
17. Every queue, retry, timeout, concurrency, cancellation, and replay mechanism is bounded where applicable.
18. Every component declares failure and safe-degradation behavior.
19. Profile membership and activation mode resolve only from active profile contracts.
20. Global logical ownership remains stable across profile topology.
21. Artifact activation validates identity, class, channel, integrity, compatibility, trust, and authorization.
22. Failed activation preserves or restores the last valid state.
23. Every critical transition maps to a test and evidence requirement.
24. Component replacement prevents parallel active writers and preserves lineage.
25. Resource Governor and Governance Policy Runtime remain separate.
26. UCKK publication requires gateway authorization followed by bridge transport.
27. SenTient remains optional, isolated, and non-authoritative.
28. External AI output remains candidate input until owner acceptance.
29. Active prose is English and contains no unresolved-authority marker.
30. No normative keyword appears outside the generated requirement block.
31. The documentation dependency graph remains acyclic.

The validation entry point is:

```bash
python docs/tools/validate_docs.py
```

## 11. Non-Normative Examples

> **Non-normative example:** This example illustrates component qualification.

A PostgreSQL process is infrastructure rather than automatically being a component. Konnaxion and Orgo can use separate schemas and identities on that process while remaining distinct components with separate ownership.

> **Non-normative example:** This example illustrates gateway authority.

The UCKK Publication Bridge can validate, package, and transport an authorized representation to the external UCKK platform. The kOA Mediatheque remains the owner of local media state, Publication Gateway remains the disclosure authority, and UCKK owns only its separately accepted destination copy.

> **Non-normative example:** This example illustrates derived data.

SenTient can build an authorized analytical index. The index remains derived workbench data. An owning component can accept a selected result only through an explicit import contract.

> **Non-normative example:** This example illustrates policy and resource separation.

The Governance Policy Runtime can approve an export while the Resource Governor keeps the export queued because the system lacks an available I/O grant. The owning component proceeds only after both prerequisites are valid.

> **Non-normative example:** This example illustrates component lifecycle.

Kristal Runtime can verify and atomically activate a compatible Runtime Pack while retaining the previous valid pack as the recovery state. The activation does not make Kristal a universal workflow engine or operational database.
