<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-LIFE-017",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "lifecycle",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/system.contract.json#/release_and_artifact_identity",
    "contracts/system.contract.json#/degradation_baseline/contract_incompatibility",
    "contracts/system.contract.json#/profile_model",
    "contracts/system.contract.json#/critical_transitions",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "contracts/artifact-contracts/release-set.schema.json",
    "generated/profile-catalog.json",
    "generated/component-catalog.json",
    "generated/decision-index.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/document-index.json"
  ],
  "decision_ids": [
    "DEC-SYS-001",
    "DEC-PROFILE-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-REL-001",
    "DEC-CONTAINER-001",
    "DEC-K8S-001",
    "DEC-HW-001",
    "DEC-AI-001"
  ],
  "requirement_ids": [
    "REQ-LIFE-CAD-001",
    "REQ-LIFE-CAD-002",
    "REQ-LIFE-CAD-003",
    "REQ-LIFE-CAD-004",
    "REQ-LIFE-CAD-005",
    "REQ-LIFE-CAD-006",
    "REQ-LIFE-CAD-007",
    "REQ-LIFE-CAD-008",
    "REQ-LIFE-CAD-009",
    "REQ-LIFE-CAD-010",
    "REQ-LIFE-CAD-011",
    "REQ-LIFE-CAD-012",
    "REQ-LIFE-CAD-013",
    "REQ-LIFE-CAD-014",
    "REQ-LIFE-CAD-015",
    "REQ-LIFE-CAD-016",
    "REQ-LIFE-CAD-017",
    "REQ-LIFE-CAD-018",
    "REQ-LIFE-CAD-019",
    "REQ-LIFE-CAD-020",
    "REQ-LIFE-CAD-021",
    "REQ-LIFE-CAD-022",
    "REQ-LIFE-CAD-023",
    "REQ-LIFE-CAD-024"
  ],
  "lock_ids": [
    "LOCK-SYS-001",
    "LOCK-SYS-002",
    "LOCK-SYS-003",
    "LOCK-SYS-004",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-CONST-003",
    "DOC-SYS-000",
    "DOC-SYS-018",
    "DOC-DEV-014",
    "DOC-LIFE-000",
    "DOC-LIFE-001",
    "DOC-LIFE-002",
    "DOC-LIFE-003",
    "DOC-LIFE-004",
    "DOC-LIFE-007",
    "DOC-LIFE-013",
    "DOC-LIFE-014",
    "DOC-LIFE-015",
    "DOC-LIFE-016"
  ],
  "tags": [
    "lifecycle",
    "compatibility",
    "deprecation",
    "supersession",
    "migration",
    "release-sets",
    "profiles",
    "components",
    "interfaces",
    "artifacts",
    "evidence",
    "recovery"
  ]
}
KOA:DOC-META:END -->

# Compatibility and Deprecation

## 1. Purpose

This document defines how kOA declares, evaluates, tests, evidences, changes, deprecates, supersedes, revokes, archives, and removes compatibility relationships.

Compatibility is a relationship between exact objects in an exact context. It is not an intrinsic property of one version in isolation.

A version number, schema pass, signature, build result, shared technology, or historical deployment can contribute evidence. None of them alone proves that a producer, consumer, profile, artifact, release, migration, or target remains semantically compatible.

Deprecation is a managed lifecycle state. It warns consumers, constrains new use, preserves lineage, and directs migration. It is distinct from immediate revocation and from final archival or deletion.

## 2. Scope

This document applies to compatibility and deprecation involving:

- decisions, requirements, locks, and normative contracts;
- primary profiles and overlays;
- components and component compositions;
- commands, queries, APIs, events, errors, and state models;
- schemas and data migrations;
- toolchains, runtimes, operating systems, architectures, containers, and orchestration;
- system, services, governance, and knowledge release channels;
- artifacts, manifests, signatures, Release Sets, offline bundles, and activation targets;
- hardware envelopes, workloads, resource limits, and recovery capacity;
- backup, restore, rollback, forward repair, portability, and exit;
- tests, evidence, receipts, documentation, generated projections, and AI context packages.

This document does not define compatibility by informal convention. The owning canonical contract defines each supported relationship.

## 3. Canonical References

| Canonical reference | Ownership |
| --- | --- |
| `contracts/system.contract.json#/release_and_artifact_identity` | Independent channel updates, Release Set binding, non-partial activation, and recovery |
| `contracts/system.contract.json#/degradation_baseline/contract_incompatibility` | Blocking behavior, preservation of valid state, and prohibition of schema guessing |
| `contracts/system.contract.json#/profile_model` | Explicit primary-profile and overlay composition |
| `contracts/system.contract.json#/critical_transitions` | Receipts required for artifact and release activation |
| `contracts/release-channels.contract.json` | Release-channel identities, versions, compatibility, and support |
| `contracts/artifact-classes.contract.json` | Artifact identities, manifests, activation, migration, recovery, deprecation, and retention |
| `contracts/artifact-contracts/release-set.schema.json` | Complete compatible multi-channel release composition |
| `generated/profile-catalog.json` | Profile identities, overlays, membership, and compatibility |
| `generated/component-catalog.json` | Component identities, interfaces, and responsibility boundaries |
| `generated/decision-index.json` | Accepted semantic authority and supersession lineage |
| `generated/requirements-index.json` | Normative statements projected in Section 5 |
| `generated/assertion-index.json` | Cross-file invariants that compatibility cannot weaken silently |
| `generated/traceability.json` | Direct and transitive dependency and impact relationships |
| `generated/test-catalog.json` | Registered compatibility, migration, recovery, and deprecation tests |
| `generated/evidence-catalog.json` | Active evidence validity, invalidation, expiry, and supersession |
| `generated/document-index.json` | Document identity, lifecycle, dependencies, and generated projections |

## 4. Model and Responsibilities

### 4.1 Compatibility relation

A compatibility relation identifies:

`text
producer object and version
consumer or target object and version
primary profile and overlays
implementation and platform context
capability and feature state
connectivity state
data and migration state
release and artifact composition
security and trust state
hardware and resource envelope
validity conditions
registered tests and evidence
`

A result applies only to the declared matrix cell. Another profile, overlay, version, architecture, data state, Release Set, or recovery path requires its own declaration or an explicitly broader tested claim.

### 4.2 Compatibility dimensions

| Dimension | Questions | Required validation evidence |
| --- | --- | --- |
| Schema and syntax | Required fields, types, enums, structure, canonicalization, and parse behavior | Schema and contract tests |
| Interface | Request, response, event, command, query, error, timeout, idempotency, and version behavior | Producer-consumer contract tests |
| Behavior | Meaning, invariants, authority, state transitions, failure states, and safe degradation | Unit, component, and scenario tests |
| Data | Storage model, migrations, references, ownership, retention, provenance, export, and recovery | Migration, integrity, rollback, and ownership tests |
| Profile and capability | Primary profile, overlays, component membership, capability state, implementation choices, and hardware envelope | Exact profile matrix tests |
| Runtime and platform | Operating system, architecture, runtime, compiler, library, container, orchestration, filesystem, and network assumptions | Platform and cross-environment tests |
| Security and trust | Identity, signatures, trust scope, revocation, secrets, privilege, disclosure, consent, and policy decisions | Security, authorization, and trust tests |
| Artifact and release | Artifact class, manifest, release channel, Release Set, integrity, signing, activation, and retention | Artifact and release-gate tests |
| Offline and connectivity | Local capability, queues, import, reconnect, expiry, and absence of silent fallback | Offline and reconnection tests |
| Operations and recovery | Health, readiness, backup, restore, rollback, forward repair, incident, and exit behavior | Operations and recovery tests |
| Resource and capacity | CPU, memory, I/O, storage, concurrency, queue, dataset, and workload limits | Hardware-envelope and pressure tests |

A relation can pass one dimension and fail another. Complete compatibility requires every applicable dimension to pass.

### 4.3 Compatibility classifications

| Classification | Meaning | Operational effect |
| --- | --- | --- |
| Compatible | The declared producer and consumer relation works without migration under the exact tested conditions. | Activation or continued use may proceed within the declared scope. |
| Conditionally compatible | Compatibility depends on a profile, overlay, feature state, migration, runtime, version, or operational constraint. | Proceed only after every declared condition is validated. |
| Migration compatible | The relation becomes compatible only after an explicit versioned migration or translation. | Stage, migrate, validate, then activate; preserve recovery. |
| Incompatible | One or more required semantic, authority, data, security, profile, release, or recovery conditions fail. | Block the affected transition and preserve the existing valid state. |
| Deprecated but supported | The object remains usable for declared existing consumers during a bounded support condition. | Warn, prevent unsupported expansion, and execute the migration plan. |
| Revoked or security-invalid | The object or trust relationship cannot safely remain active. | Block or quarantine according to the security and recovery contract. |
| Historical only | The object is retained for receipts, provenance, audit, recovery, migration, or reproducibility but is not activatable. | Permit authorized historical access only. |

The canonical registry or contract owns the actual state value and scope. This table explains the lifecycle meaning.

### 4.4 Change classification

A change can be:

- editorial, with no semantic effect;
- compatible and additive;
- conditionally compatible;
- migration compatible;
- incompatible;
- deprecating;
- superseding;
- revoking or security-invalidating;
- archival or removal.

The version or release label records identity. The semantic change and its compatibility declaration determine behavior.

An additive field is not automatically compatible when it changes canonicalization, signatures, defaults, authority, resource use, persistence, error handling, or downstream assumptions.

### 4.5 Contract and interface compatibility

Interface compatibility includes:

- accepted requests and inputs;
- produced responses, events, and errors;
- required and optional fields;
- defaults and canonicalization;
- authentication and authorization;
- idempotency and replay behavior;
- ordering and concurrency;
- timeouts and retries;
- state transitions;
- failure and recovery behavior;
- version negotiation;
- observability and receipts.

A consumer cannot rely on an undeclared field, side effect, error message, ordering property, or implementation detail.

### 4.6 Data compatibility

Data compatibility includes schema, meaning, ownership, references, provenance, retention, and recovery.

A migration defines:

- source and target versions;
- preconditions;
- transformations;
- validation;
- compatibility window;
- read and write behavior during transition;
- rollback, restore, or forward repair;
- receipts and evidence;
- treatment of deprecated fields and historical records.

Physical storage sharing cannot make incompatible component ownership compatible.

### 4.7 Profile and platform compatibility

Profile compatibility resolves the exact primary profile and overlays.

Platform compatibility records operating system, architecture, runtime, toolchain, container or non-container implementation, filesystem, network, device, and hardware assumptions.

Kubernetes, containers, Linux, WSL, systemd, GNOME, KDE, or another implementation choice does not create global compatibility merely because multiple deployments use it.

### 4.8 Artifact and release compatibility

An artifact declares:

- artifact class and identity;
- manifest version;
- supported consumers and targets;
- required dependencies;
- incompatible versions;
- activation preconditions;
- migration or conversion;
- recovery;
- retention and deprecation.

An independent release-channel update checks every affected active relationship.

A Release Set binds all required channel identities. A failed required cell blocks the complete authoritative activation.

### 4.9 Deprecation model

A deprecation record identifies:

- deprecated object and version;
- reason;
- replacement or terminal disposition;
- affected consumers and profiles;
- new-use cutoff;
- support conditions;
- migration or coexistence plan;
- warnings and diagnostics;
- tests and evidence;
- security and trust conditions;
- retention and historical obligations;
- removal condition.

Deprecation does not alter the old object's semantics. It limits future use and directs an explicit transition.

### 4.10 Supersession, revocation, and history

Supersession creates lineage from an old object to a replacement. The record states whether both can coexist and whether translation, migration, rollback, or historical reproduction remains possible.

Revocation is not ordinary deprecation. A compromised key, unsafe artifact, invalid trust relationship, or critical security defect can require immediate blocking or quarantine.

Historical objects remain available when required for:

- audit and receipts;
- prior decision reproduction;
- backup and restore;
- rollback or incident analysis;
- migration validation;
- legal or cultural-rights obligations;
- provenance and supply-chain records;
- offline fleet support.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-LIFE-CAD-001,REQ-LIFE-CAD-002,REQ-LIFE-CAD-003,REQ-LIFE-CAD-004,REQ-LIFE-CAD-005,REQ-LIFE-CAD-006,REQ-LIFE-CAD-007,REQ-LIFE-CAD-008,REQ-LIFE-CAD-009,REQ-LIFE-CAD-010,REQ-LIFE-CAD-011,REQ-LIFE-CAD-012,REQ-LIFE-CAD-013,REQ-LIFE-CAD-014,REQ-LIFE-CAD-015,REQ-LIFE-CAD-016,REQ-LIFE-CAD-017,REQ-LIFE-CAD-018,REQ-LIFE-CAD-019,REQ-LIFE-CAD-020,REQ-LIFE-CAD-021,REQ-LIFE-CAD-022,REQ-LIFE-CAD-023,REQ-LIFE-CAD-024 -->
- **REQ-LIFE-CAD-001 — SHALL:** Every active compatibility claim shall identify the exact producer object, consumer or target object, versions, profile context, overlays, implementation context, connectivity state, and applicable validity conditions.
- **REQ-LIFE-CAD-002 — SHALL:** Compatibility shall be declared through canonical contracts or registries and shall not be inferred from names, version ordering, tags, file locations, shared technology, or historical coexistence.
- **REQ-LIFE-CAD-003 — SHALL:** A compatibility declaration shall state supported versions or ranges, known incompatibilities, required dependencies, feature or capability conditions, migration requirements, recovery behavior, tests, and evidence.
- **REQ-LIFE-CAD-004 — SHALL:** Compatibility evaluation shall cover every applicable schema, interface, behavior, data, profile, runtime, platform, security, trust, artifact, release, offline, operational, resource, and recovery dimension.
- **REQ-LIFE-CAD-005 — SHALL NOT:** A valid schema, signature, build, unit-test result, semantic-version label, or shared runtime shall by itself establish complete compatibility.
- **REQ-LIFE-CAD-006 — SHALL:** An additive change shall preserve existing accepted inputs, outputs, authority boundaries, failure behavior, and recovery behavior unless an explicit compatibility condition narrows its supported scope.
- **REQ-LIFE-CAD-007 — SHALL:** A conditionally compatible change shall identify the exact profiles, capabilities, feature states, versions, migrations, or deployment conditions under which compatibility holds.
- **REQ-LIFE-CAD-008 — SHALL:** An incompatible semantic change shall use a new versioned contract or artifact identity and shall define migration, coexistence or cutover, rollback or forward repair, tests, evidence, and deprecation impact.
- **REQ-LIFE-CAD-009 — SHALL NOT:** A runtime, component, migration, importer, or activation path shall guess a missing schema, transform an unknown version implicitly, or silently substitute another provider, artifact, interface, profile, or implementation.
- **REQ-LIFE-CAD-010 — SHALL:** Independent release-channel updates shall activate only when declared compatibility with every affected active channel, profile, component, artifact, runtime, and recovery path remains satisfied.
- **REQ-LIFE-CAD-011 — SHALL:** A Release Set shall bind all required channels and shall prevent partial authoritative activation when any required compatibility relationship fails.
- **REQ-LIFE-CAD-012 — SHALL:** Profile and overlay compatibility shall be resolved from active profile contracts, and a profile-specific compatibility result shall not become global through repetition or common implementation.
- **REQ-LIFE-CAD-013 — SHALL:** Data compatibility shall preserve logical ownership, declared migrations, reference integrity, retention, provenance, rollback or forward-repair behavior, and cross-component access boundaries.
- **REQ-LIFE-CAD-014 — SHALL:** Security and trust compatibility shall include signer scope, trust roots, revocation, credential format, privilege boundaries, disclosure rules, policy-runtime compatibility, and break-glass constraints where applicable.
- **REQ-LIFE-CAD-015 — SHALL:** A deprecation record shall identify the deprecated object, reason, replacement or terminal disposition, affected consumers, migration path, support conditions, warning behavior, evidence, and the condition that ends new activation or support.
- **REQ-LIFE-CAD-016 — SHALL NOT:** Deprecation shall not silently remove an object, alter its semantics, revoke it, delete required history, or redirect consumers to an incompatible replacement.
- **REQ-LIFE-CAD-017 — SHALL:** A deprecated object may support existing consumers only within its declared compatibility, security, retention, and support conditions and shall be rejected for new use after its declared new-use cutoff.
- **REQ-LIFE-CAD-018 — SHALL:** Supersession shall preserve lineage from the old object to the replacement and shall identify whether coexistence, migration, translation, rollback, or historical reproduction remains supported.
- **REQ-LIFE-CAD-019 — SHALL:** Revocation or security invalidation shall be treated separately from ordinary deprecation and shall define immediate blocking, quarantine, trust removal, recovery, evidence invalidation, and notification behavior.
- **REQ-LIFE-CAD-020 — SHALL:** Removal or archival shall occur only after dependency, retention, recovery, audit, legal, cultural-rights, offline, reproducibility, and historical-reconstruction obligations are satisfied.
- **REQ-LIFE-CAD-021 — SHALL:** A material compatibility or deprecation change shall trigger direct and transitive impact analysis across decisions, requirements, locks, profiles, components, interfaces, artifacts, releases, documents, tests, evidence, migrations, and generated projections.
- **REQ-LIFE-CAD-022 — SHALL:** Compatibility and deprecation evidence shall identify the exact tested matrix cells, environment, versions, profiles, migration state, result, validity interval or invalidation conditions, and supporting artifacts.
- **REQ-LIFE-CAD-023 — SHALL:** Contract incompatibility shall block the affected transition, preserve the existing valid state, and require explicit migration, rollback, restore, forward repair, or accepted replacement before authority changes.
- **REQ-LIFE-CAD-024 — SHALL:** Every active compatibility, deprecation, supersession, migration, support, removal, and release claim shall be traceable to accepted decisions, active requirements, applicable locks, registered tests, and valid evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Declare compatibility

1. Identify the producer and consumer or target objects.
2. record exact versions and canonical identities;
3. resolve profile, overlays, capabilities, implementation, platform, connectivity, data, release, trust, and resource context;
4. enumerate every applicable compatibility dimension;
5. declare supported, conditional, migration-required, and incompatible cases;
6. define required migration and recovery behavior;
7. register tests for each claimed matrix cell;
8. produce evidence;
9. register the compatibility declaration and traceability.

### 6.2 Evaluate a candidate change

1. Resolve the accepted source decision.
2. classify the semantic change;
3. compute direct and transitive impact;
4. compare old and new contracts, data, behavior, profiles, artifacts, tests, and recovery;
5. identify affected compatibility matrix cells;
6. update declarations, migrations, deprecations, tests, and evidence;
7. validate independent channel and Release Set impact;
8. activate the new authority only after all affected checks pass.

### 6.3 Perform a compatibility test

1. Select one registered matrix cell.
2. provision the exact producer, consumer, profile, overlay, implementation, platform, data, release, security, and resource context;
3. execute schema and interface tests;
4. execute behavioral and authority tests;
5. execute migration and data-integrity tests when applicable;
6. execute security, trust, offline, operations, resource, and recovery tests;
7. record every assertion and environment identity;
8. register evidence with validity and invalidation conditions.

### 6.4 Introduce an incompatible version

1. Create or reference an accepted owner decision.
2. assign a new versioned contract or artifact identity;
3. preserve the old active contract within its support scope;
4. define migration, translation, coexistence, cutover, rollback, restore, or forward repair;
5. define profile and release compatibility;
6. publish deprecation and consumer impact;
7. test the old, transition, and new states;
8. produce evidence;
9. activate the replacement last.

### 6.5 Deprecate an object

1. Identify the deprecated object and reason.
2. identify every affected consumer, profile, artifact, release, document, test, and evidence record;
3. select a replacement or terminal disposition;
4. define the new-use cutoff and existing-use conditions;
5. define migration and recovery;
6. add machine-readable warnings and diagnostics;
7. preserve historical lineage;
8. validate the replacement path;
9. register the deprecation and evidence;
10. monitor remaining supported use until the removal condition is satisfied.

### 6.6 Migrate a consumer

1. Verify the consumer's current version and state.
2. verify target compatibility and migration preconditions;
3. create a recovery point;
4. stage the replacement dependency, interface, artifact, or data model;
5. execute the versioned migration;
6. validate data, behavior, authority, security, performance, offline, and recovery;
7. cut over atomically or through the declared coexistence window;
8. produce migration and activation receipts;
9. retain or dispose of the old state according to deprecation and recovery rules.

### 6.7 Revoke an unsafe object

1. Authenticate the revocation authority.
2. identify the object, trust scope, affected targets, claims, and evidence;
3. block new use or activation immediately;
4. quarantine artifacts or credentials where applicable;
5. invalidate dependent compatibility and release evidence;
6. preserve unaffected valid state;
7. execute rollback, replacement, credential rotation, restore, or repair;
8. notify affected operators and owners;
9. record revocation and recovery receipts;
10. preserve historical lineage.

### 6.8 Archive or remove

1. Verify that no supported active consumer remains.
2. verify migration completion;
3. verify retention, audit, legal, cultural-rights, recovery, offline, and reproducibility obligations;
4. preserve required receipts, provenance, schemas, migration tools, and historical artifacts;
5. mark the object non-activatable;
6. update registries, traceability, tests, evidence, documents, and generated projections;
7. remove only disposable runtime copies and unneeded distribution paths;
8. retain the canonical historical record.

## 7. Failure States and Safe Degradation

| Failure state | Required response | Preserved state | Blocked behavior or claim |
| --- | --- | --- | --- |
| Compatibility declaration missing | Block the affected integration, migration, release, or activation. | Current valid state | Inferred compatibility |
| Schema parses but behavior differs | Classify the relation as incompatible or conditionally compatible and run semantic tests. | Existing valid behavior | Schema-only approval |
| Unknown version | Reject or quarantine the object. | Known supported versions | Version guessing |
| Unsupported profile or overlay | Block activation for that composition. | Other validated profile results | Cross-profile inference |
| Migration incomplete | Keep the old authoritative state or enter the declared recovery path. | Pre-migration recovery point | Partial migrated authority |
| Independent channel update conflicts | Block the channel activation. | Existing compatible Release Set | Partial update |
| Release Set cell fails | Block the complete authoritative transition. | Previous valid Release Set | Partial Release Set activation |
| Deprecated dependency still required | Retain support within declared conditions and continue the migration plan. | Existing supported consumers | Premature removal |
| New-use cutoff reached | Reject new consumers while preserving declared existing-use behavior. | Existing supported deployments | New activation |
| Replacement is incompatible | Block automatic redirection and require explicit migration or coexistence. | Deprecated object within support conditions | Silent substitution |
| Object revoked | Apply immediate block or quarantine, invalidate dependent evidence, and invoke recovery. | Unaffected trusted state and historical lineage | Ordinary deprecation delay |
| Evidence expired or invalidated | Remove it from active compatibility support and rerun the affected matrix cell. | Historical result | Current compatibility claim |
| Control plane unavailable | Preserve local validated versions and block unsupported new coordinated changes. | Node-local active state | Unverified remote desired state |
| Resource or recovery capacity insufficient | Block migration or activation before mutation. | Current valid state and recovery capacity | Unrecoverable transition |

Contract incompatibility blocks the affected transition and preserves the existing valid state. Automatic schema guessing and silent substitution remain prohibited.

## 8. Cross-Component Interactions

| Producer or owner | Consumer | Interaction | Authority boundary |
| --- | --- | --- | --- |
| Owner decision registry | Contracts and lifecycle workflows | Authorizes semantic change, supersession, or retirement | Version labels cannot replace owner decisions |
| Profile index and profile contracts | Compatibility evaluator | Define valid primary-profile and overlay composition | One profile result cannot become global implicitly |
| Component contract | Producer and consumer tests | Defines interface, behavior, data, authority, and failure semantics | Implementation details are not compatibility authority |
| Data owner | Migration workflow | Defines source meaning, ownership, retention, and target constraints | Migration tooling cannot transfer ownership |
| Release channel | Target or Release Set | Supplies versioned channel artifacts | Publication is not target compatibility or activation |
| Release Set | Node Agent or target lifecycle | Binds required channel versions and compatibility | One channel cannot activate when a required cell fails |
| Identity and Trust | Artifact and interface verifier | Supplies signer identity, trust scope, and revocation | Trust validation does not prove behavioral compatibility |
| Governance Policy Runtime | Governed transitions | Supplies authorization, disclosure, privilege, consent, and exceptions | Compatibility tooling cannot invent policy |
| Resource Governor | Tests, migrations, and activations | Bounds CPU, memory, I/O, storage, concurrency, queues, and jobs | Capacity does not change semantic compatibility |
| kOA Node Agent | Target transition | Performs final validation, activation, rollback, repair, and receipts | Control-plane desired state is not sufficient authority |
| Audit Broker | Lifecycle and release workflows | Records selective compatibility, migration, deprecation, activation, and revocation evidence | Observation does not alter lifecycle state |
| Test and evidence registries | Merge, release, and support gates | Supply registered validation and active evidence | Historical or invalid evidence cannot support current claims |
| Documentation registry | Review and impact workflow | Tracks dependent explanations and generated projections | Markdown does not own canonical compatibility values |

No interaction permits direct writes to another component's authoritative source tables.

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Closed question |
| --- | --- |
| `DEC-SYS-001` | Compatibility operates inside the local-first, modular, explicit-authority system baseline. |
| `DEC-PROFILE-001` | Primary profiles and overlays define explicit compatibility scope. |
| `DEC-DATA-001` | Data compatibility preserves logical ownership and prohibits direct cross-component source writes. |
| `DEC-GOV-001` | Policy authority and resource authority remain separate during migration and activation. |
| `DEC-REL-001` | Independent channel updates, Release Sets, non-partial activation, receipts, and recovery govern release compatibility. |
| `DEC-CONTAINER-001` | Container-runtime choice is profile-scoped and does not define global application compatibility. |
| `DEC-K8S-001` | Kubernetes is not an endpoint requirement and does not grant application compatibility or authority. |
| `DEC-HW-001` | Hardware and capacity compatibility requires profile-specific measured evidence. |
| `DEC-AI-001` | AI output cannot decide, infer, migrate, activate, or validate compatibility authoritatively. |

### Prohibited assumptions

- Higher version means compatible.
- A patch label means no semantic change.
- A major label defines the migration automatically.
- Schema validation proves behavioral compatibility.
- Signature validation proves semantic compatibility.
- Build success proves runtime or profile compatibility.
- Unit tests prove Release Set compatibility.
- Shared implementation technology proves interface compatibility.
- A commonly used profile rule is global.
- One successful migration proves every data state.
- A deprecated object is already removed.
- A deprecated object may change semantics silently.
- Deprecation and security revocation are interchangeable.
- A replacement can be selected by name similarity.
- Automatic redirects are acceptable without compatibility tests.
- Unknown versions can use the nearest known schema.
- Old and new writers may coexist without an explicit data contract.
- A control plane can override target incompatibility.
- Existing invalid evidence remains valid until manually deleted.
- Historical artifacts can be deleted when current operation no longer needs them.
- External AI can choose a compatible replacement.
- Missing migration or recovery behavior may be inferred from industry practice.

## 10. Validation Criteria

1. The metadata block parses as JSON and declares `DOC-LIFE-017`, status `active`, language `en`, lifecycle layer, and global scope.
2. All eleven required sections exist in numerical order.
3. Every decision ID is accepted in `generated/decision-index.json`.
4. Every requirement ID appears exactly once in `generated/requirements-index.json`.
5. Every lock ID resolves to an active lock.
6. `TEST-LIFE-CAD-001` verifies complete compatibility subject and context identity.
7. `TEST-LIFE-CAD-002` rejects compatibility inferred from names, versions, tags, paths, technology, or coexistence.
8. `TEST-LIFE-CAD-003` verifies supported, conditional, migration-required, incompatible, recovery, test, and evidence declarations.
9. `TEST-LIFE-CAD-004` verifies all applicable compatibility dimensions.
10. `TEST-LIFE-CAD-005` verifies that schema, signature, build, unit tests, and version labels cannot establish complete compatibility alone.
11. `TEST-LIFE-CAD-006` verifies additive-change preservation of inputs, outputs, authority, failures, and recovery.
12. `TEST-LIFE-CAD-007` verifies conditionally compatible profile, feature, runtime, version, and migration constraints.
13. `TEST-LIFE-CAD-008` verifies incompatible-version identity, migration, coexistence, cutover, recovery, and evidence.
14. `TEST-LIFE-CAD-009` rejects schema guessing, implicit transformation, and silent substitution.
15. `TEST-LIFE-CAD-010` verifies independent release-channel compatibility.
16. `TEST-LIFE-CAD-011` verifies complete Release Set compatibility and non-partial activation.
17. `TEST-LIFE-CAD-012` verifies exact profile and overlay scope.
18. `TEST-LIFE-CAD-013` verifies data ownership, migration, integrity, retention, provenance, and recovery.
19. `TEST-LIFE-CAD-014` verifies security, trust, privilege, disclosure, policy-runtime, and break-glass compatibility.
20. `TEST-LIFE-CAD-015` verifies complete deprecation records and warning behavior.
21. `TEST-LIFE-CAD-016` verifies new-use cutoff and bounded existing-use support.
22. `TEST-LIFE-CAD-017` verifies supersession lineage, coexistence, translation, migration, rollback, and historical reproduction.
23. `TEST-LIFE-CAD-018` verifies distinct revocation and security-invalidation behavior.
24. `TEST-LIFE-CAD-019` verifies removal prerequisites and historical retention.
25. `TEST-LIFE-CAD-020` verifies impact analysis, evidence validity, failure blocking, valid-state preservation, and full traceability.
26. Active prose is English and contains no unresolved marker, placeholder, metadata hash, or source hash.
27. The generated requirement block matches the canonical requirement registry.

These criteria define validation requirements. They do not claim that any specific producer, consumer, version, profile, migration, artifact, Release Set, or deprecation already conforms.

## 11. Non-Normative Examples

> **Non-normative example:** A response schema adds an optional field. Contract tests pass for old consumers, but canonical signing includes every field. The signature representation changed, so security and artifact compatibility still require explicit validation.

> **Non-normative example:** A services-channel update supports the active system and knowledge versions but requires a newer governance bundle. Independent activation is blocked until the governance compatibility condition is satisfied or a complete Release Set is used.

> **Non-normative example:** An interface version is deprecated. Existing consumers may continue until the declared cutoff under the tested support conditions. New registrations are rejected, and each consumer has a recorded migration to the replacement.

> **Non-normative example:** A database migration supports rollback only before new writers begin. The compatibility declaration identifies that boundary, and the activation workflow verifies the forward-repair path before cutover.

> **Non-normative example:** A signing key is compromised. Affected artifacts are revoked rather than ordinarily deprecated. New activation stops immediately, dependent evidence is invalidated, trusted replacements are staged, and historical receipts remain preserved.

> **Non-normative example:** ChatGPT suggests that two API versions appear compatible. The suggestion may inform review, but only registered contract, profile, data, security, lifecycle, resource, and recovery tests with valid evidence support the compatibility claim.
