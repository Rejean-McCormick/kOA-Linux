<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-COMP-001",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "component",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/component_model",
    "generated/component-catalog.json",
    "schemas/component-contract.schema.json",
    "generated/profile-catalog.json",
    "contracts/artifact-classes.contract.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-COMP-CONTRACT-001",
    "DEC-SYS-COMP-001",
    "DEC-SYS-CAP-001",
    "DEC-SYS-OFFLINE-001",
    "DEC-SYS-RESOURCE-001",
    "DEC-SYS-AUDIT-001",
    "DEC-LIFE-001",
    "DEC-INT-001"
  ],
  "requirement_ids": [
    "REQ-COMP-CONTRACT-001",
    "REQ-COMP-CONTRACT-002",
    "REQ-COMP-CONTRACT-003",
    "REQ-COMP-CONTRACT-004",
    "REQ-COMP-CONTRACT-005",
    "REQ-COMP-CONTRACT-006",
    "REQ-COMP-CONTRACT-007",
    "REQ-COMP-CONTRACT-008",
    "REQ-COMP-CONTRACT-009",
    "REQ-COMP-CONTRACT-010",
    "REQ-COMP-CONTRACT-011",
    "REQ-COMP-CONTRACT-012",
    "REQ-COMP-CONTRACT-013",
    "REQ-COMP-CONTRACT-014",
    "REQ-COMP-CONTRACT-015",
    "REQ-COMP-CONTRACT-016",
    "REQ-COMP-CONTRACT-017",
    "REQ-COMP-CONTRACT-018",
    "REQ-COMP-CONTRACT-019",
    "REQ-COMP-CONTRACT-020",
    "REQ-COMP-CONTRACT-021",
    "REQ-COMP-CONTRACT-022",
    "REQ-COMP-CONTRACT-023",
    "REQ-COMP-CONTRACT-024",
    "REQ-COMP-CONTRACT-025",
    "REQ-COMP-CONTRACT-026",
    "REQ-COMP-CONTRACT-027",
    "REQ-COMP-CONTRACT-028",
    "REQ-COMP-CONTRACT-029",
    "REQ-COMP-CONTRACT-030",
    "REQ-COMP-CONTRACT-031",
    "REQ-COMP-CONTRACT-032",
    "REQ-COMP-CONTRACT-033",
    "REQ-COMP-CONTRACT-034",
    "REQ-COMP-CONTRACT-035",
    "REQ-COMP-CONTRACT-036",
    "REQ-COMP-CONTRACT-037",
    "REQ-COMP-CONTRACT-038",
    "REQ-COMP-CONTRACT-039",
    "REQ-COMP-CONTRACT-040"
  ],
  "lock_ids": [
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-OPS-001",
    "LOCK-OPS-002",
    "LOCK-OPS-003"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-002",
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-SYS-000",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-006",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-010",
    "DOC-SYS-011",
    "DOC-SYS-012",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-016",
    "DOC-SYS-017",
    "DOC-SYS-018",
    "DOC-SYS-019",
    "DOC-PROFILE-001",
    "DOC-PROFILE-002",
    "DOC-COMP-000"
  ],
  "tags": [
    "component-contracts",
    "component-boundaries",
    "data-authority",
    "interfaces",
    "events",
    "state-model",
    "failure-model",
    "offline-behavior",
    "security",
    "resources",
    "observability",
    "lifecycle",
    "conformance"
  ]
}
KOA:DOC-META:END -->

# Component Contract Rules

## 1. Purpose

This document defines the common contract rules for every architectural component in kOA.

A component contract is the machine-readable boundary between one component and the rest of the system. It identifies what the component owns, what it can observe, which requests it accepts, which outputs and events it produces, how its state changes, how it fails, how it behaves offline, which resources it consumes, how it is secured, and how its claims are tested.

The rules prevent a component from becoming an undefined collection of implementation packages or services. They also prevent neighboring responsibilities from merging through convenience, shared storage, interface access, workflow coordination, profile composition, or AI inference.

The component registry owns component identity and high-level responsibility. Each component contract owns the component's observable behavioral contract. Component Markdown explains that contract without becoming a second source of canonical values.

## 2. Scope

This document applies globally to:

- every component registered in `generated/component-catalog.json`;
- every file under `contracts/components/`;
- runtime components;
- gateways;
- brokers;
- agents;
- platforms;
- workbenches;
- services;
- local and external adapters represented as components;
- profile-specific component activation;
- component-owned data;
- component interfaces and events;
- component workflows and state transitions;
- failure and offline behavior;
- security, privacy, audit, and cultural-rights controls;
- resource and performance envelopes;
- observability and operations;
- backup, restore, upgrade, deactivation, and recovery;
- component conformance tests and evidence.

This document does not define the internal source-code layout, class structure, package names, process topology, database technology, container layout, or deployment recipe for a component. Those implementation choices remain subordinate to the observable contract.

A component contract can be stricter than this common model. It cannot remove a global boundary or leave implementation-affecting behavior implicit.

## 3. Canonical References

Canonical ownership is distributed as follows:

| Subject | Canonical owner |
| --- | --- |
| Component identity, class, primary responsibility, and canonical ownership | `generated/component-catalog.json` |
| Active component-contract inventory | `generated/component-catalog.json` |
| Component-contract structure | `schemas/component-contract.schema.json` |
| Component-specific observable behavior | `contracts/components/*.component.json` |
| Component-specific explanatory documentation | `04-components/*.md` |
| Global capability and component models | `contracts/system.contract.json` |
| Profile membership and operating envelopes | `contracts/profiles/*.profile.json` |
| Artifact identity and lifecycle rules | `contracts/artifact-classes.contract.json` |
| External and cross-boundary integrations | `contracts/integration-types.contract.json` |
| Requirement statements and strength | `generated/requirements-index.json` |
| Cross-file component invariants | `generated/assertion-index.json` |
| Decision, component, profile, interface, test, and evidence links | `generated/traceability.json` |
| Component conformance tests | `generated/test-catalog.json` |
| Component evidence | `generated/evidence-catalog.json` |
| Approved bounded deviations | `generated/exception-index.json` |
| Accepted architectural decisions | `generated/decision-index.json` |
| Active versions and authority order | `generated/authority-manifest.json` |

The component registry and component contract have distinct roles. The registry answers which component exists and what domain it owns. The contract answers how that boundary behaves.

## 4. Contract Model and Ownership

### 4.1 Required contract identity

Every component contract includes these identity fields:

| Field | Meaning |
| --- | --- |
| `$schema` | Active component-contract schema |
| `contract_id` | Stable contract identity |
| `contract_type` | `component_contract` |
| `version` | Semantic contract version |
| `status` | Lifecycle status |
| `language` | Contract language |
| `effective_at` | Activation time |
| `component_id` | Matching component registry identity |
| `component_ref` | Canonical component registry reference |
| `documentation_ref` | Matching component document |
| `authority_ref` | Active authority reference |
| `decision_refs` | Accepted decisions supporting the contract |
| `requirement_refs` | Applicable normative requirements |
| `lock_refs` | Applicable interfile locks |

A component identity is not reused after retirement. A new component receives a new identity. A compatible contract evolution preserves the component identity and versions the contract.

### 4.2 Identity and purpose

The `identity` and `purpose` sections identify:

- display name;
- component class;
- authority class;
- primary domain;
- multiplicity or singleton scope;
- execution identity;
- activation model;
- external-boundary status;
- native AI status;
- primary responsibility;
- authoritative result;
- architectural reason for the component boundary.

A component's purpose is singular even when it exposes several capabilities.

### 4.3 Responsibility partition

The `responsibilities` section uses three partitions:

| Partition | Meaning |
| --- | --- |
| `owned` | Behavior, state, transitions, and evidence for which the component is accountable |
| `owned_elsewhere` | Adjacent responsibility with an explicit canonical owner |
| `prohibited` | Behavior that the component boundary excludes |

A complete contract identifies the closest neighboring authorities. This reduces accidental overlap and gives validators concrete conflicts to detect.

### 4.4 Authority boundary

The `authority_boundary` section distinguishes:

- state and results for which the component is authoritative;
- candidate, copied, transported, derived, or externally owned material;
- decisions owned by another authority;
- behavior the component can execute only from a valid upstream decision;
- behavior that remains advisory or non-authoritative.

Reading data does not create ownership. Transporting an artifact does not create semantic authority. Coordinating a workflow does not make the coordinator the owner of every stage.

### 4.5 Component classes

The component registry uses a controlled component-class vocabulary, including:

```text
runtime
gateway
broker
workbench
platform
agent
service
privileged_broker
```

The authority class uses an explicit value such as:

```text
authoritative
authoritative_executor
derived
advisory
non_authoritative
transport
```

The precise active vocabulary remains canonical in the components registry and component-contract schema.

### 4.6 Profiles and activation

A component contract declares its applicable profile references, optionality, activation modes, and absence behavior.

Activation modes can include:

```text
always_on
socket_activated
session_activated
task_activated
manual
external_only
recovery_only
```

Profile membership comes from profile contracts. A component contract cannot infer global activation from installation or repository presence.

### 4.7 Submodules

Architecturally relevant internal submodules can appear when they own distinct internal state or implement a contractually significant stage.

A submodule record identifies:

- stable submodule identity;
- responsibility;
- authoritative or derived internal state;
- interface to sibling submodules;
- failure isolation;
- replaceability.

Implementation classes and packages remain outside the canonical component contract unless their identity is required for interoperability or lifecycle compatibility.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-COMP-CONTRACT-001,REQ-COMP-CONTRACT-002,REQ-COMP-CONTRACT-003,REQ-COMP-CONTRACT-004,REQ-COMP-CONTRACT-005,REQ-COMP-CONTRACT-006,REQ-COMP-CONTRACT-007,REQ-COMP-CONTRACT-008,REQ-COMP-CONTRACT-009,REQ-COMP-CONTRACT-010,REQ-COMP-CONTRACT-011,REQ-COMP-CONTRACT-012,REQ-COMP-CONTRACT-013,REQ-COMP-CONTRACT-014,REQ-COMP-CONTRACT-015,REQ-COMP-CONTRACT-016,REQ-COMP-CONTRACT-017,REQ-COMP-CONTRACT-018,REQ-COMP-CONTRACT-019,REQ-COMP-CONTRACT-020,REQ-COMP-CONTRACT-021,REQ-COMP-CONTRACT-022,REQ-COMP-CONTRACT-023,REQ-COMP-CONTRACT-024,REQ-COMP-CONTRACT-025,REQ-COMP-CONTRACT-026,REQ-COMP-CONTRACT-027,REQ-COMP-CONTRACT-028,REQ-COMP-CONTRACT-029,REQ-COMP-CONTRACT-030,REQ-COMP-CONTRACT-031,REQ-COMP-CONTRACT-032,REQ-COMP-CONTRACT-033,REQ-COMP-CONTRACT-034,REQ-COMP-CONTRACT-035,REQ-COMP-CONTRACT-036,REQ-COMP-CONTRACT-037,REQ-COMP-CONTRACT-038,REQ-COMP-CONTRACT-039,REQ-COMP-CONTRACT-040 -->
- **REQ-COMP-CONTRACT-001 — SHALL:** Every active component have one stable component identifier in the components registry and one active component contract matching that identifier.
- **REQ-COMP-CONTRACT-002 — SHALL:** Every active component contract validate against the active component-contract schema and reject undeclared top-level fields.
- **REQ-COMP-CONTRACT-003 — SHALL:** Every component contract identify its contract version, status, language, effective time, component reference, documentation reference, authority reference, decisions, requirements, and locks.
- **REQ-COMP-CONTRACT-004 — SHALL NOT:** A Markdown component document, implementation package, deployment manifest, recipe, or generated projection replace the canonical component contract.
- **REQ-COMP-CONTRACT-005 — SHALL:** Every component contract declare one primary responsibility, one primary domain, one component class, one authority class, and one singleton or multiplicity scope.
- **REQ-COMP-CONTRACT-006 — SHALL:** Every component contract distinguish responsibilities it owns, responsibilities owned elsewhere, and operations it is prohibited from performing.
- **REQ-COMP-CONTRACT-007 — SHALL NOT:** A component acquire authority through implementation prevalence, data access, message consumption, user-interface presentation, deployment proximity, or agent inference.
- **REQ-COMP-CONTRACT-008 — SHALL:** Every authoritative data store have one owning component and declare data classes, ownership, persistence, encryption, purpose, direct readers, governed readers, retention, deletion authority, and export rules.
- **REQ-COMP-CONTRACT-009 — SHALL NOT:** A component write directly to another component's authoritative store or treat another component's cache, projection, event copy, or replica as locally owned authority.
- **REQ-COMP-CONTRACT-010 — SHALL:** Every component contract classify derived data, candidate inputs, prohibited storage, and the effect of losing regenerable state.
- **REQ-COMP-CONTRACT-011 — SHALL NOT:** Candidate, imported, generated, externally returned, or AI-produced material become authoritative before the owning component's registered validation and acceptance transition.
- **REQ-COMP-CONTRACT-012 — SHALL:** Every inbound interface declare a stable interface identifier, interface type, caller classes, input contract, authentication, authorization, idempotency behavior, and exposure boundary.
- **REQ-COMP-CONTRACT-013 — SHALL:** Every outbound interface declare a stable interface identifier, interface type, destination, purpose, delivery model, output or payload contract, and failure behavior.
- **REQ-COMP-CONTRACT-014 — SHALL NOT:** An interface accept arbitrary fields, arbitrary commands, undocumented parameters, or incompatible versions when the active contract defines a closed schema.
- **REQ-COMP-CONTRACT-015 — SHALL:** Every administrative or privileged interface use a narrow operation model, explicit authorization, bounded parameters, audit receipts, and a declared privilege broker where host mutation is required.
- **REQ-COMP-CONTRACT-016 — SHALL NOT:** Root identity, local process identity, network reachability, or successful authentication by itself authorize an administrative or privileged operation.
- **REQ-COMP-CONTRACT-017 — SHALL:** Every emitted event declare its identifier, trigger, payload contract, delivery guarantee, idempotency key, sensitivity or audit class, and authority relationship.
- **REQ-COMP-CONTRACT-018 — SHALL:** Every consumed event declare its source, consumer behavior, duplicate handling, poison-message behavior, compatibility rules, and failure effect.
- **REQ-COMP-CONTRACT-019 — SHALL:** A component that couples an authoritative commit to an emitted event use a transactional outbox or a validated equivalent that prevents silent divergence.
- **REQ-COMP-CONTRACT-020 — SHALL:** Every at-least-once event consumer be idempotent and preserve detectable handling for malformed or poison events.
- **REQ-COMP-CONTRACT-021 — SHALL:** Every component contract declare a complete component state model, operation or workflow state model, terminal states, allowed transitions, entry conditions, and success conditions.
- **REQ-COMP-CONTRACT-022 — SHALL NOT:** A component report completion before its authoritative effect, required verification, and required receipt or evidence transition are complete.
- **REQ-COMP-CONTRACT-023 — SHALL:** Every state-changing workflow declare validation, authorization, precondition, commit, evidence, rollback, recovery, cancellation, timeout, and conflict behavior.
- **REQ-COMP-CONTRACT-024 — SHALL:** Every operation with repeatable delivery or retry exposure bind one idempotency identity to one canonical request body and reject reuse with different meaning.
- **REQ-COMP-CONTRACT-025 — SHALL:** Every versioned artifact activation preserve atomicity, compatibility validation, the previous valid state, and a registered rollback or forward-repair path.
- **REQ-COMP-CONTRACT-026 — SHALL:** Every component contract declare per-profile offline behavior, including continuous, degraded, deferred, unavailable, and offline-transfer capabilities where applicable.
- **REQ-COMP-CONTRACT-027 — SHALL NOT:** Failure or removal of an optional integration disable unrelated component capabilities or alter another component's authoritative state.
- **REQ-COMP-CONTRACT-028 — SHALL:** Every component contract define a failure taxonomy with cause, authority impact, safe behavior, recovery procedure, and observable status.
- **REQ-COMP-CONTRACT-029 — SHALL NOT:** Unknown, incompatible, unverifiable, unauthorized, expired, revoked, or corrupted input be interpreted through best effort when an authoritative effect is possible.
- **REQ-COMP-CONTRACT-030 — SHALL:** Every component contract declare identity, authentication, authorization, privilege, secret, privacy, disclosure, audit, cultural-rights, and external-integration boundaries applicable to the component.
- **REQ-COMP-CONTRACT-031 — SHALL NOT:** Credentials, secret material, unrestricted sensitive payloads, or raw private keys appear in ordinary logs, receipts, metrics, traces, exports, images, or request parameters.
- **REQ-COMP-CONTRACT-032 — SHALL:** Every component contract declare a resource class, profile-owned resource envelopes, concurrency controls, queue bounds, timeout bounds, pressure response, and Resource Governor interaction.
- **REQ-COMP-CONTRACT-033 — SHALL NOT:** A component or the Resource Governor infer authorization, consent, disclosure, privilege, publication, or governance policy from resource state.
- **REQ-COMP-CONTRACT-034 — SHALL:** Every component contract declare liveness, readiness, dependency health, degraded state, active artifact identity, structured logs, bounded metrics, and correlation identifiers.
- **REQ-COMP-CONTRACT-035 — SHALL:** Every component with durable authoritative state declare backup scope, excluded regenerable state, consistency mechanism, encryption, retention, restore validation, and independent restore behavior.
- **REQ-COMP-CONTRACT-036 — SHALL:** Every component contract declare startup, shutdown, upgrade, deactivation, schema or data migration, and recovery behavior.
- **REQ-COMP-CONTRACT-037 — SHALL:** Every cross-component interaction identify direction, contract, purpose, authority effect, ownership boundary, failure behavior, and prohibition of direct database access.
- **REQ-COMP-CONTRACT-038 — SHALL:** Component contracts preserve the separation of Resource Governor from Governance Policy Runtime and Publication Gateway from UCKK Dimension Gateway.
- **REQ-COMP-CONTRACT-039 — SHALL:** Component conformance trace to accepted decisions, requirements, locks, profiles, artifact and integration contracts, tests, and current evidence.
- **REQ-COMP-CONTRACT-040 — SHALL:** Component-contract validation include schema conformance, unique identity, ownership conflict detection, interface closure, transition completeness, failure safety, offline behavior, security, resources, lifecycle, reference resolution, and absence of prohibited open-state markers.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Data, Interface, Event, and State Rules

### 6.1 Data authority

The `data_authority` section classifies:

- authoritative stores;
- derived data;
- candidate inputs;
- prohibited storage;
- retention and deletion;
- export behavior;
- rebuildability;
- loss impact.

An authoritative store record identifies one owner and its direct and governed readers. Physical database sharing does not create logical schema sharing. Cross-component access uses the owning component's interface.

Derived data identifies its canonical sources and rebuild process. Loss of derived data produces a declared operational impact without destroying authority.

Candidate input stays outside authoritative state until the admission workflow succeeds.

### 6.2 Inbound interfaces

An inbound interface record includes:

- stable interface identity;
- transport or interaction type;
- caller classes;
- request or input contract;
- authentication;
- authorization;
- idempotency;
- compatibility;
- exposure boundary;
- rate, queue, and timeout behavior;
- failure response.

Inbound types can include local API, network API, event, file, socket, command, gateway, artifact, device, or offline bundle.

An administrative interface remains separate from an ordinary user or service interface.

### 6.3 Outbound interfaces

An outbound interface record includes:

- destination;
- purpose;
- payload or result contract;
- delivery model;
- authority effect;
- retry and duplicate behavior;
- timeout;
- failure behavior;
- disclosure and provenance controls.

A synchronous call, asynchronous event, batch artifact, or gateway transfer preserves the destination component's authority.

### 6.4 Interface compatibility

Interface compatibility covers:

- semantic interface version;
- request and response schema version;
- minimum compatible caller and destination versions;
- required feature negotiation;
- unknown field behavior;
- unknown operation behavior;
- incompatible version behavior;
- migration and deprecation intervals.

Silent reinterpretation of unknown behavior is not a compatibility strategy.

### 6.5 Events

The `events` section separates emitted and consumed events.

An emitted event records its trigger, payload contract, delivery guarantee, idempotency identity, audit class, sensitivity, and relationship to the authoritative commit.

A consumed event records its source, behavior, idempotency handling, poison-message handling, compatibility, and failure effect.

A poison event remains inspectable and does not block an entire queue indefinitely unless the active contract explicitly identifies that queue as atomic.

### 6.6 Transactional consistency

When a local authoritative commit and an external event need to remain aligned, the contract identifies a consistency mechanism such as:

```text
transactional_outbox
transactional_journal
atomic_artifact_and_receipt
durable_precommit_receipt
validated_equivalent
```

The mechanism defines crash recovery, replay, duplicate detection, and the relationship between commit status and event status.

### 6.7 State models

The `state_model` section includes:

- component operational states;
- operation or workflow states;
- terminal states;
- allowed transitions;
- entry and exit conditions;
- success conditions;
- blocked, failed, conflicted, expired, cancelled, rolled-back, and recovery states where applicable.

Availability, execution, and authoritative outcome remain distinct dimensions.

### 6.8 Operation contracts

A registered operation identifies:

- operation identity and class;
- purpose;
- authority and privilege effects;
- request, result, and receipt contracts;
- allowed parameters;
- required artifacts;
- preconditions;
- timeout;
- idempotency;
- offline behavior;
- replay behavior;
- rollback or recovery behavior.

A closed operation model is mandatory for privileged or high-impact administrative behavior.

## 7. Execution, Offline, and Failure Rules

### 7.1 Admission and commit

A state-changing operation normally progresses through:

```text
received
identity_verified
schema_verified
authorization_verified
preconditions_verified
resource_admitted
accepted
executing
commit_pending
committed
receipt_durable
completed
```

Alternative transitions include:

```text
blocked
rejected
cancelled
failed
conflicted
expired
rolled_back
recovery_required
```

The contract identifies which stages apply and which authority owns each stage.

### 7.2 Idempotency and replay

Idempotency binds one identity to one canonical operation meaning.

A replay with the same identity and same canonical body returns the recorded or equivalent result. Reuse with a different body is rejected and recorded.

External effects use destination-specific idempotency or duplicate detection before replay.

### 7.3 Atomic activation

Artifact and configuration activation use an atomic transition or a validated equivalent.

The contract identifies:

- staged state;
- pre-activation validation;
- expected current state;
- commit mechanism;
- active identity;
- last-known-good state;
- rollback floor;
- recovery path;
- post-activation verification;
- receipt and evidence.

Partial active authority remains invalid.

### 7.4 Offline behavior

The `offline_behavior` section identifies:

- profile ownership of detailed values;
- core local behavior;
- continuous capabilities;
- degraded capabilities;
- deferred operations;
- unavailable external behavior;
- offline-transfer capabilities;
- restart behavior;
- local audit durability;
- central-service dependency.

A component can have different behavior across profiles, but no profile behavior can violate global offline locks.

### 7.5 Failure model

Each failure record includes:

| Field | Meaning |
| --- | --- |
| `failure_id` | Stable failure identity |
| `cause` | Triggering condition |
| `authority_impact` | None, read-only, blocked, recovery-required, or another registered effect |
| `safe_behavior` | Behavior that preserves authority and prevents false completion |
| `recovery` | Valid path to restore service or authority |

Failure records cover identity, authorization, policy, dependency, storage, resource, network, integrity, compatibility, timeout, duplicate, queue, migration, recovery, and contract failures as applicable.

### 7.6 Degradation rules

Safe degradation preserves:

- data ownership;
- component boundaries;
- policy and privilege;
- provenance;
- required evidence;
- resource reserves;
- user-visible truth about incomplete work.

Optional capability failure does not authorize another component to assume the responsibility.

### 7.7 Restart and recovery

The contract explains how restart reconstructs:

- active contract and profile;
- committed authoritative state;
- pending operations;
- idempotency records;
- transaction journals;
- event and receipt delivery;
- active artifacts;
- last-known-good state;
- degraded capability state.

Unknown prior effects remain explicit until reconciliation proves the outcome.

## 8. Security, Resource, and Operational Rules

### 8.1 Identity and authorization

The security model identifies:

- user identity authority;
- service identity authority;
- node identity authority;
- artifact and signing identity authority;
- authentication mechanisms;
- authorization owner;
- policy and obligation binding;
- expiry and revocation;
- scope validation;
- break-glass separation.

Authentication and host privilege do not replace authorization.

### 8.2 Privilege boundaries

Host mutation uses the narrow privileged broker when required.

A component contract identifies:

- privileged operation;
- approving authority;
- broker interface;
- bounded parameters;
- preconditions;
- receipt;
- rollback or recovery;
- profile availability.

General root execution is outside ordinary component contracts.

### 8.3 Secrets, privacy, and disclosure

The security section identifies:

- managed secret mechanisms;
- prohibited secret locations;
- data classifications;
- retention;
- privacy access and correction paths;
- disclosure gateway;
- audit class;
- restricted evidence;
- cultural-rights and consent controls;
- external integration boundaries.

Public evidence remains separate from restricted evidence.

### 8.4 Resource model

The `resource_envelope` section identifies:

- resource class;
- governing profile values;
- concurrency limits;
- queue limits;
- timeout limits;
- priority;
- CPU, memory, storage, I/O, network, power, or device needs;
- pressure response;
- heavy-job behavior;
- Resource Governor interaction.

The Resource Governor enforces resources. The Governance Policy Runtime evaluates governance policy. The component retains its own data and workflow authority.

### 8.5 Observability

The `observability` section includes:

- liveness;
- readiness;
- dependency health;
- queue state;
- resource pressure;
- active artifact identity;
- degraded capabilities;
- structured logs;
- bounded metrics;
- correlation identifiers;
- trace restrictions;
- user-facing status owner.

Observability data remains classified and excludes secrets and unrestricted payloads.

### 8.6 Backup, restore, and maintenance

A durable component identifies:

- authoritative backup scope;
- excluded caches and rebuildable indexes;
- consistency mechanism;
- encryption;
- retention;
- restore procedure;
- restore validation;
- portability and exit implications;
- maintenance operations;
- migration controls.

Backup existence is not restore evidence. Restore is independently tested.

### 8.7 Lifecycle

The `lifecycle` section covers:

- startup;
- readiness;
- shutdown;
- upgrade;
- schema and data migration;
- artifact change;
- key rotation;
- deactivation;
- replacement;
- rollback;
- forward repair;
- archive and retirement.

An upgrade cannot use the unverified new implementation as its own sole authority.

## 9. Cross-Component Boundaries and Compatibility

### 9.1 Interaction records

Every interaction identifies:

| Field | Meaning |
| --- | --- |
| component reference | Neighboring component |
| direction | Inbound, outbound, or bidirectional |
| contract | Interface, event, artifact, or gateway contract |
| purpose | Required system outcome |
| authority effect | Request, candidate, transport, decision, evidence, or authoritative effect |
| data classes | Information crossing the boundary |
| failure behavior | Safe response to unavailability or rejection |
| direct database access | Always prohibited across component ownership boundaries |

Interaction records can be represented directly in the contract or derived from declared interfaces and traceability.

### 9.2 Required separations

All component contracts preserve these system separations:

- authoritative component state from workflow coordination;
- Resource Governor from Governance Policy Runtime;
- Publication Gateway from UCKK Dimension Gateway;
- local deterministic capabilities from optional external AI;
- Ariane local navigation from external voice;
- UCKK native processing from external Suno or Gamma adapters;
- runtime artifact consumption from language construction workbenches;
- ordinary component behavior from privileged host mutation;
- public transparency receipts from restricted evidence.

A component can interact with both sides of a separation without merging them.

### 9.3 Artifact boundaries

A component that consumes or produces an artifact identifies:

- artifact class;
- channel;
- schema or manifest;
- provenance;
- integrity and signature rules where applicable;
- compatibility;
- admission or activation transition;
- rollback or retirement behavior.

An artifact's presence does not activate it.

### 9.4 Integration boundaries

External providers, federation peers, devices, controlled imports, controlled exports, developer tools, and migration sources use registered integration contracts.

External AI output remains candidate material with provenance until local acceptance.

### 9.5 Profile compatibility

A component contract identifies applicability across primary profiles and overlays.

Profile-specific values include:

- activation mode;
- hardware and resources;
- network exposure;
- offline behavior;
- optional integrations;
- evidence;
- security hardening;
- backup and recovery;
- conformance claims.

A value from one profile does not become global or transfer to a sibling profile.

### 9.6 Contract evolution

Contract changes are classified by semantic impact.

A change to ownership, responsibility, authority effect, data stores, interface compatibility, state transitions, failure behavior, profile membership, security boundary, offline behavior, or validation is semantic.

Semantic changes receive an accepted decision, impact analysis, updated requirements and locks, tests, evidence, compatibility treatment, and authority activation after dependent objects pass.

## 10. Exceptions and Validation

### 10.1 Exceptions

A bounded exception can adjust an implementation adapter, evidence source, profile-specific resource value, compatibility interval, retention value, deployment endpoint, or test environment.

An exception cannot:

- create shared ownership;
- authorize direct cross-component writes;
- remove a required interface contract;
- authorize arbitrary privileged execution;
- turn external AI output into authority;
- merge separated gateways or governance responsibilities;
- permit secret leakage;
- conceal incomplete state;
- remove required recovery;
- support an unqualified conformance claim outside its scope.

The exception remains a separate registered record and does not rewrite the source component contract.

### 10.2 Required validator behavior

Validation includes:

1. schema conformance;
2. unique contract and component identities;
3. registry-contract identity alignment;
4. active decision support;
5. canonical reference resolution;
6. responsibility and ownership conflict detection;
7. authoritative-store uniqueness;
8. direct-write prohibition;
9. interface closure;
10. contract-version compatibility;
11. event consistency and consumer idempotency;
12. complete state transitions;
13. success-condition completeness;
14. operation idempotency;
15. atomic activation;
16. rollback and recovery;
17. offline behavior;
18. failure safety;
19. secret and privacy controls;
20. privilege-boundary controls;
21. resource-envelope presence;
22. observability and lifecycle completeness;
23. profile scope;
24. artifact and integration references;
25. requirement and lock alignment;
26. test and evidence currency;
27. generated documentation alignment;
28. absence of prohibited open-state markers.

### 10.3 Validation entry points

The principal validation entry point is:

```bash
python docs/tools/validate_docs.py
```

Supporting checks include:

```text
tools/check_component_boundaries.py
tools/check_canonical_ownership.py
tools/check_interfile_locks.py
tools/check_artifact_contracts.py
tools/check_profile_inheritance.py
tools/check_ai_boundary.py
tools/check_traceability.py
tools/check_generated_content.py
tools/check_no_unresolved_state.py
```

A failed component-contract check blocks activation of the affected contract and dependent claims. The last validated active contract remains authoritative until a replacement passes.

## 11. Non-Normative Examples

### 11.1 Correct data authority

A media platform owns admitted media records. Its gateway validates and transports candidate input but does not own the destination records.

### 11.2 Incorrect data authority

A workflow service reads three component databases and treats that read access as ownership. The contract model rejects the resulting shared authority.

### 11.3 Correct privileged operation

A component submits a closed, authorized request to kOA Node Agent. The request identifies expected state, policy decision, bounded parameters, deadline, idempotency key, and receipt requirements.

### 11.4 Incorrect privileged operation

A component exposes a root shell endpoint and relies on the caller to use it responsibly. That interface has no valid component-contract representation.

### 11.5 Correct external AI handling

A user invokes an approved external AI adapter through controlled export. The returned artifact retains provenance and enters a candidate state until the owning component accepts it.

### 11.6 Correct event consistency

A component commits authoritative state and records an outbox event in the same transaction. A repeated delivery is handled through the event's idempotency identity.

### 11.7 Correct offline behavior

A component continues local reads and queued local work during network loss. External publication becomes deferred, and the user-visible result remains pending until external confirmation and local reconciliation.

### 11.8 Correct profile scoping

A component is task-activated in a user profile and always-on in a control-plane profile. Both values remain in their profile contracts and do not become one global activation rule.

### 11.9 Correct recovery

A process stops after a host effect with an unknown result. The operation enters `recovery_required`; restart inspects actual state before any replay.

### 11.10 Correct separation

A component asks the Governance Policy Runtime for authorization and the Resource Governor for resource admission. It does not treat either answer as the other's decision.
