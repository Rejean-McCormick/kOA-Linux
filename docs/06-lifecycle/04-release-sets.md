<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-LIFE-004",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "lifecycle",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/release_model",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-REL-001",
    "DEC-LIFE-001",
    "DEC-IMAGE-001",
    "DEC-OS-001",
    "DEC-SEC-001",
    "DEC-OFFLINE-001",
    "DEC-RECEIPT-001",
    "DEC-AUDIT-001",
    "DEC-PORT-001",
    "DEC-PROFILE-001",
    "DEC-COMP-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-INTEGRATION-001",
    "DEC-AI-001",
    "DEC-KRISTAL-001",
    "DEC-LANG-001"
  ],
  "requirement_ids": [
    "REQ-LIFE-RSET-001",
    "REQ-LIFE-RSET-002",
    "REQ-LIFE-RSET-003",
    "REQ-LIFE-RSET-004",
    "REQ-LIFE-RSET-005",
    "REQ-LIFE-RSET-006",
    "REQ-LIFE-RSET-007",
    "REQ-LIFE-RSET-008",
    "REQ-LIFE-RSET-009",
    "REQ-LIFE-RSET-010",
    "REQ-LIFE-RSET-011",
    "REQ-LIFE-RSET-012",
    "REQ-LIFE-RSET-013",
    "REQ-LIFE-RSET-014",
    "REQ-LIFE-RSET-015",
    "REQ-LIFE-RSET-016",
    "REQ-LIFE-RSET-017",
    "REQ-LIFE-RSET-018",
    "REQ-LIFE-RSET-019",
    "REQ-LIFE-RSET-020",
    "REQ-LIFE-RSET-021",
    "REQ-LIFE-RSET-022",
    "REQ-LIFE-RSET-023",
    "REQ-LIFE-RSET-024",
    "REQ-LIFE-RSET-025",
    "REQ-LIFE-RSET-026",
    "REQ-LIFE-RSET-027",
    "REQ-LIFE-RSET-028",
    "REQ-LIFE-RSET-029",
    "REQ-LIFE-RSET-030"
  ],
  "lock_ids": [
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-REL-001",
    "LOCK-REL-002",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SEC-001",
    "LOCK-SEC-002",
    "LOCK-OFFLINE-001",
    "LOCK-PORT-001",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-LIFE-000",
    "DOC-LIFE-001",
    "DOC-LIFE-002",
    "DOC-LIFE-003",
    "DOC-SYS-001",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-007",
    "DOC-SYS-009",
    "DOC-SYS-017",
    "DOC-SYS-019",
    "DOC-SYS-020",
    "DOC-PROFILE-001",
    "DOC-PROFILE-003",
    "DOC-CONST-000",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-CONST-011"
  ],
  "tags": [
    "lifecycle",
    "release-sets",
    "release-channels",
    "system",
    "services",
    "governance",
    "knowledge",
    "compatibility",
    "staging",
    "activation",
    "rollback",
    "forward-repair",
    "offline-bundles",
    "receipts"
  ]
}
KOA:DOC-META:END -->

# Release Sets

## 1. Purpose

This document defines the kOA Release Set model.

A Release Set is the complete, compatible release identity activated on a target. It binds the four independent release channels into one explicit operational composition:

`text
system
services
governance
knowledge
`

The channels can evolve independently, but a deployment never activates a channel in isolation from the compatibility evaluation of the resulting complete set.

The Release Set model exists to prevent:

- implicit “latest” dependencies;
- incompatible channel combinations;
- unregistered mixed-version operation;
- partial authoritative activation claims;
- unsafe rollback assumptions;
- hidden online dependencies;
- loss of release, migration, recovery, and evidence lineage.

The Release Set manifest is canonical for the selected four-channel composition. Individual services, processes, images, policies, and artifacts report their resolved identities but do not independently redefine the active set.

## 2. Scope

This document applies globally to:

- Release Set manifests;
- system releases;
- services releases;
- governance releases;
- knowledge releases;
- primary profiles and overlays;
- immutable system images;
- service artifacts;
- governance policy bundles;
- Kristal artifacts;
- language artifacts;
- Ariane artifacts;
- component schemas and migrations;
- online and offline update flows;
- staging, activation, rollback, recovery, and forward repair;
- portability and restore;
- release evidence and conformance claims.

It applies to user, developer, sovereign, hub, build, and control profiles according to each profile's lifecycle role.

A Build Farm can produce Release Set candidates and validation evidence. An operational target independently validates and activates the candidate under its own profile and authority.

This document does not prescribe one packaging technology, repository implementation, signature format, service manager, container runtime, bootloader, database engine, or transport.

## 3. Canonical References

| Canonical reference | Responsibility |
| --- | --- |
| `contracts/release-channels.contract.json` | Channel identities, version rules, compatibility, publication, support, and retention |
| `contracts/artifact-classes.contract.json` | Artifact validation, activation, rollback, retention, and profile applicability |
| `generated/authority-manifest.json` | Active authority release and activated canonical versions |
| `generated/decision-index.json` | Accepted release, lifecycle, image, security, offline, component, and evidence decisions |
| `contracts/system.contract.json#/release_model` | Global release and activation model |
| `generated/component-catalog.json` | Component inventory, release-channel membership, and data ownership |
| `generated/component-catalog.json` | Component interface, schema, migration, and compatibility contracts |
| `generated/profile-catalog.json` | Profile and overlay compatibility |
| `contracts/integration-types.contract.json` | Required and optional external dependencies |
| `generated/requirements-index.json` | Normative Release Set requirements |
| `generated/assertion-index.json` | Release, lifecycle, profile, component, data, security, offline, and implementation assertions |
| `generated/traceability.json` | Relationships among releases, artifacts, profiles, migrations, tests, and evidence |
| `generated/exception-index.json` | Time-bounded Release Set exceptions and compensating controls |
| `generated/test-catalog.json` | Manifest, compatibility, staging, activation, rollback, offline, and restore tests |
| `generated/evidence-catalog.json` | Release and critical-transition evidence |

The adjacent lifecycle documents are:

`text
06-lifecycle/00-artifact-model.md
06-lifecycle/01-artifact-classes.md
06-lifecycle/02-release-model.md
06-lifecycle/03-release-channels.md
06-lifecycle/05-system-image-updates.md
06-lifecycle/06-service-updates.md
06-lifecycle/07-governance-policy-bundles.md
06-lifecycle/08-kristal-artifacts.md
06-lifecycle/09-language-artifacts.md
06-lifecycle/10-ariane-artifacts.md
06-lifecycle/11-offline-bundles.md
06-lifecycle/12-artifact-verification.md
06-lifecycle/13-activation-and-verification.md
06-lifecycle/14-recovery.md
06-lifecycle/15-data-schema-evolution.md
06-lifecycle/16-forward-repair.md
06-lifecycle/17-contract-evolution-and-removal.md
06-lifecycle/18-sbom-provenance-and-signing.md
06-lifecycle/19-artifact-retention.md
`

## 4. Release Set Model and Responsibilities

### 4.1 Four-channel composition

Every Release Set selects one explicit release identity from each channel.

| Channel | Owns |
| --- | --- |
| `system` | Host operating system, kernel, boot and recovery material, base runtime, node-level platform artifacts |
| `services` | Component services, service schemas, service migrations, workers, adapters, and service-level interfaces |
| `governance` | Governance policy bundles, rights and consent policy, authorization rules, controlled exceptions, and governance-compatible evidence rules |
| `knowledge` | Kristal, language, Ariane, and other versioned knowledge or deterministic runtime artifacts |

A channel can retain its prior identity while another channel changes. The resulting tuple still receives a complete Release Set identity and complete compatibility evaluation.

### 4.2 Release Set identity

A Release Set identity is stable and immutable.

The manifest records:

- Release Set identifier and version;
- status;
- issue and support information;
- authority release;
- four channel identities;
- applicable primary profiles and overlays;
- target architectures and host envelopes;
- component and artifact inventory;
- schema and migration requirements;
- compatibility rules;
- external dependency assumptions;
- offline bundle relationship;
- predecessor, supersession, rollback, and recovery relationships;
- required tests and evidence.

The Release Set identifier is not inferred from local filenames, installation time, or process versions.

### 4.3 Status model

| Status | Meaning |
| --- | --- |
| `candidate` | Assembled but not fully validated |
| `validated` | Required candidate validation passed for declared targets |
| `staged` | Material is present on a target but not authoritative |
| `active` | The target's canonical active-set pointer and required health evidence confirm activation |
| `superseded` | A later Release Set replaces it for a declared scope |
| `withdrawn` | Release authority has removed it from new activation eligibility |
| `failed` | Candidate or target activation failed |
| `recovery_eligible` | Retained and validated for a declared recovery purpose |

A set can be active on one target and merely validated or superseded elsewhere. Target state and registry state remain distinguishable.

### 4.4 Release channel owner

Each channel owner:

- publishes channel releases;
- validates channel-internal artifacts;
- declares compatibility;
- records support and deprecation;
- supplies channel-specific rollback or repair behavior;
- provides required evidence.

A channel owner does not independently activate a target's complete Release Set.

### 4.5 Release Set assembler

The assembler resolves a candidate four-channel composition.

It verifies that every selected release exists, is eligible, and declares sufficient compatibility data.

The assembler produces a candidate manifest. It does not grant deployment authority.

### 4.6 Target lifecycle owner

The target lifecycle owner:

- validates target identity and profile;
- imports or retrieves the candidate;
- stages artifacts;
- executes component-owned migrations;
- evaluates health gates;
- activates the set;
- records receipts;
- initiates rollback, recovery, or forward repair when needed.

On sovereign production nodes, privileged host mutation uses the narrow broker path and immutable-image lifecycle defined by the active profile.

### 4.7 Components and artifact owners

Each component and artifact owner validates its own:

- version;
- schema;
- dependencies;
- migrations;
- activation;
- rollback or repair;
- runtime health;
- data ownership.

A Release Set coordinates those owners without replacing them.

### 4.8 Compatibility graph

Compatibility is a graph rather than four independent version checks.

It includes:

- system-to-services runtime compatibility;
- services-to-governance policy interfaces;
- services-to-knowledge artifact compatibility;
- governance-to-knowledge classification and rights behavior;
- profile-to-system and profile-to-service compatibility;
- component-to-component interfaces and events;
- schema and migration compatibility;
- integration and offline assumptions;
- recovery and last-known-good compatibility.

A complete graph result is required for activation.

### 4.9 Active-set authority

The active Release Set is the declared authority identity for the target's activated software and artifact composition.

Local process versions, package inventory, service discovery, and health reports are observations. They are checked against the active manifest.

A mismatch is a lifecycle failure, not an alternate Release Set.

### 4.10 Physical staging versus authority activation

Artifacts can be downloaded, imported, unpacked, mounted, loaded, migrated, or warmed before activation.

Those operations are physical preparation.

Authority changes only through the declared activation transition after all required checks pass.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-LIFE-RSET-001,REQ-LIFE-RSET-002,REQ-LIFE-RSET-003,REQ-LIFE-RSET-004,REQ-LIFE-RSET-005,REQ-LIFE-RSET-006,REQ-LIFE-RSET-007,REQ-LIFE-RSET-008,REQ-LIFE-RSET-009,REQ-LIFE-RSET-010,REQ-LIFE-RSET-011,REQ-LIFE-RSET-012,REQ-LIFE-RSET-013,REQ-LIFE-RSET-014,REQ-LIFE-RSET-015,REQ-LIFE-RSET-016,REQ-LIFE-RSET-017,REQ-LIFE-RSET-018,REQ-LIFE-RSET-019,REQ-LIFE-RSET-020,REQ-LIFE-RSET-021,REQ-LIFE-RSET-022,REQ-LIFE-RSET-023,REQ-LIFE-RSET-024,REQ-LIFE-RSET-025,REQ-LIFE-RSET-026,REQ-LIFE-RSET-027,REQ-LIFE-RSET-028,REQ-LIFE-RSET-029,REQ-LIFE-RSET-030 -->
- **REQ-LIFE-RSET-001 — SHALL:** Every active deployment identify exactly one active Release Set that names the system, services, governance, and knowledge release identities in effect.
- **REQ-LIFE-RSET-002 — SHALL NOT:** An active Release Set use an implicit latest value, unresolved range, mutable branch, environment-dependent default, or omitted release-channel identity.
- **REQ-LIFE-RSET-003 — SHALL:** Every Release Set have a stable identifier, immutable manifest version, status, profile applicability, component inventory, artifact inventory, compatibility declarations, required migrations, validation policy, and lifecycle relationships.
- **REQ-LIFE-RSET-004 — SHALL:** The Release Set manifest be signed by an authorized release identity and verified before staging, activation, rollback, recovery, or offline import.
- **REQ-LIFE-RSET-005 — SHALL NOT:** A published Release Set manifest be modified in place; any semantic change create a new Release Set identity and explicit supersession relationship.
- **REQ-LIFE-RSET-006 — SHALL:** Each referenced release and artifact be active or eligible for the declared Release Set status, resolve through canonical registries, and satisfy its artifact-class validation rules.
- **REQ-LIFE-RSET-007 — SHALL:** A Release Set declare the primary profiles, overlays, architectures, operating-system envelopes, component versions, artifact versions, and external dependency assumptions for which it is compatible.
- **REQ-LIFE-RSET-008 — SHALL:** Compatibility validation include direct and transitive relationships across all four release channels, profiles, components, schemas, events, artifacts, policies, integrations, offline envelopes, migrations, and recovery paths.
- **REQ-LIFE-RSET-009 — SHALL NOT:** An independently updated release channel become active unless the complete resulting four-channel Release Set passes compatibility and conformance validation.
- **REQ-LIFE-RSET-010 — SHALL:** A Release Set distinguish candidate, validated, staged, active, superseded, withdrawn, failed, and recovery-eligible states.
- **REQ-LIFE-RSET-011 — SHALL:** Staging preserve the currently active Release Set and avoid changing authoritative behavior until activation conditions are satisfied.
- **REQ-LIFE-RSET-012 — SHALL NOT:** Partial staging, successful download, signature verification, artifact extraction, service restart, migration start, or individual channel validation be reported as complete Release Set activation.
- **REQ-LIFE-RSET-013 — SHALL:** Activation validate target identity, active profile composition, authority, storage, resources, artifact integrity, compatibility, migration readiness, policy availability, evidence path, rollback or repair path, and required health gates.
- **REQ-LIFE-RSET-014 — SHALL:** The authoritative active-set transition be atomic even when artifact staging, data migration, service restart, or health verification occurs in multiple class-specific phases.
- **REQ-LIFE-RSET-015 — SHALL NOT:** A deployment expose a mixed undeclared active state in which different components report incompatible or unregistered channel identities.
- **REQ-LIFE-RSET-016 — SHALL:** Every component and lifecycle control plane expose the active Release Set identity and its own resolved release and artifact identities without treating local process state as the canonical set manifest.
- **REQ-LIFE-RSET-017 — SHALL:** Required data migrations execute through component-owned migration contracts in declared order and complete their activation health gates before the Release Set is reported active.
- **REQ-LIFE-RSET-018 — SHALL:** Rollback eligibility be declared per artifact class, component, migration, and target profile, including the exact last-known-good or recovery-eligible Release Set.
- **REQ-LIFE-RSET-019 — SHALL NOT:** The existence of a prior Release Set, backup, system slot, database snapshot, service image, or down migration be treated as proof that rollback is safe.
- **REQ-LIFE-RSET-020 — SHALL:** When reverse activation is unsafe or impossible, the Release Set define forward repair, restoration, isolation, or recovery behavior and the operator decision points that govern it.
- **REQ-LIFE-RSET-021 — SHALL:** A failed activation retain or restore a declared valid authority state, identify any partial physical changes, block unsupported mixed operation, and produce a machine-readable failure result.
- **REQ-LIFE-RSET-022 — SHALL:** Offline import and activation use a complete verified bundle containing or referencing every required Release Set manifest, release-channel manifest, artifact, migration, trust input, validation rule, and recovery instruction.
- **REQ-LIFE-RSET-023 — SHALL NOT:** Offline operation weaken signature, authority, compatibility, profile, policy, migration, evidence, or health validation.
- **REQ-LIFE-RSET-024 — SHALL:** Optional external integrations remain removable and must not be required for Release Set activation unless the target profile explicitly declares them as required dependencies.
- **REQ-LIFE-RSET-025 — SHALL:** Every Release Set activation, rollback, withdrawal, recovery selection, and forward-repair completion produce a machine-readable receipt identifying target, previous set, candidate set, resulting set, actor, authority, profile, channel identities, result, reason codes, and evidence.
- **REQ-LIFE-RSET-026 — SHALL:** Release Set evidence remain selectively disclosable, attributable, retained, and free of unrestricted governed payloads and private signing material.
- **REQ-LIFE-RSET-027 — SHALL:** A superseded or withdrawn Release Set remain resolvable for audit, rollback analysis, restore, portability, and migration lineage according to retention rules.
- **REQ-LIFE-RSET-028 — SHALL:** Portability and restore packages identify the source Release Set and the compatible target Release Sets or migration paths required to restore authoritative operation.
- **REQ-LIFE-RSET-029 — SHALL:** A Release Set conformance claim identify the exact target, profile composition, authority release, four channel identities, artifacts, migrations, tests, exceptions, evidence, and validity conditions.
- **REQ-LIFE-RSET-030 — SHALL:** Release Set conformance pass only when manifest, signature, authority, compatibility, profile, staging, migration, activation, rollback or repair, offline, receipt, restore, and evidence tests all pass.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Assembly and Validation Procedure

### 6.1 Select channel releases

The assembler receives:

- target profile or profile family;
- target architecture and host envelope;
- requested system release;
- requested services release;
- requested governance release;
- requested knowledge release;
- applicable exceptions;
- intended lifecycle purpose.

Every channel identity is explicit.

### 6.2 Resolve artifacts and components

For each channel, the assembler resolves:

- release manifest;
- artifact inventory;
- component inventory;
- artifact-class contracts;
- schema versions;
- migrations;
- profile applicability;
- support state;
- integration assumptions;
- required trust and evidence inputs.

An unresolved object blocks the candidate.

### 6.3 Evaluate compatibility

Compatibility evaluation covers:

1. channel-to-channel constraints;
2. profile and overlay composition;
3. architecture and operating-system support;
4. component interfaces;
5. event schemas;
6. data schemas and migration paths;
7. artifact formats;
8. governance policy interfaces;
9. knowledge runtime interfaces;
10. offline envelopes;
11. external integration assumptions;
12. rollback, recovery, and forward-repair paths.

A validator that cannot evaluate a required relationship reports a blocked result.

### 6.4 Build the candidate manifest

The candidate manifest records the resolved composition and its validation plan.

It identifies:

- predecessor sets;
- supported source sets;
- migration order;
- expected active artifacts;
- target health gates;
- rollback candidates;
- recovery candidates;
- forward-repair package;
- required receipts;
- retention obligations.

### 6.5 Verify release authority

The candidate is signed by an authorized release identity.

The target verifies:

- signer authority;
- manifest status;
- profile scope;
- validity interval;
- withdrawal state;
- applicable exception state;
- trust material.

Verification success does not yet activate the set.

### 6.6 Run pre-staging tests

Pre-staging tests can include:

- artifact availability;
- storage and resource capacity;
- architecture compatibility;
- schema preflight;
- migration dry run;
- policy bundle validation;
- knowledge artifact loading;
- service interface validation;
- offline completeness;
- recovery-path readiness.

The candidate moves to `validated` only when all applicable required tests pass.

### 6.7 Create offline representation

When offline use is required, the Release Set is represented by a verified offline bundle.

The bundle carries or references all required manifests, artifacts, migrations, trust inputs, validation logic, operator instructions, and recovery material.

The offline representation identifies the exact Release Set. It does not create a second mutable definition.

## 7. Staging, Activation, Rollback, and Forward Repair

### 7.1 Stage the candidate

The target stages the candidate without changing active authority.

Staging can include:

- importing artifacts;
- writing an inactive system slot;
- preparing service images or packages;
- loading inactive policy bundles;
- loading inactive knowledge artifacts;
- creating migration backups;
- running expand-phase migrations;
- warming derived caches;
- checking recovery media.

The target retains the active Release Set and its recovery path.

### 7.2 Pre-activation gate

Before activation, the target confirms:

- target and profile identity;
- complete candidate manifest;
- valid release authority;
- current source Release Set;
- compatible migration source state;
- required backups;
- storage and resource reserves;
- component readiness;
- policy availability;
- evidence buffering;
- rollback or repair eligibility;
- health-test availability.

A failed precondition leaves the candidate staged or failed.

### 7.3 Execute migrations

Component-owned migrations run in declared order.

The lifecycle coordinator records progress but does not write participant data directly.

Expand and data-migration phases can precede active-set switching when compatibility permits.

The candidate cannot be reported active until required migration verification and application compatibility pass.

### 7.4 Activate class-specific artifacts

System, service, governance, and knowledge artifacts use their class-specific activation procedures.

Examples include:

- switching an immutable system-image slot;
- activating a service version;
- activating a governance policy bundle;
- activating a Kristal or language artifact.

The lifecycle transaction records every class-specific result.

### 7.5 Switch active-set authority

After all required activation steps and initial health gates pass, the target atomically changes its canonical active Release Set identity.

The active-set receipt identifies the previous and new sets.

Components then report their resolved identities against the new manifest.

### 7.6 Confirm health

Post-switch validation confirms:

- required services are available;
- component contracts are compatible;
- data stores are healthy;
- migrations are complete;
- governance decisions are available;
- knowledge artifacts load correctly;
- offline envelope remains accurate;
- critical receipts are durable;
- recovery remains available.

The target reports active success only after required health confirmation.

### 7.7 Rollback

Rollback selects a declared recovery-eligible Release Set.

It validates:

- artifact availability;
- data compatibility;
- migration reversibility or restored data;
- profile compatibility;
- policy compatibility;
- knowledge compatibility;
- evidence path.

Rollback can restore the previous set, another recovery set, or a restored state. It is never inferred solely from the existence of an old artifact.

### 7.8 Forward repair

Forward repair is used when returning to the previous set would be unsafe.

It can:

- activate corrected service artifacts;
- apply repair migrations;
- replace a failed policy or knowledge artifact;
- isolate an affected component;
- restore from a validated backup;
- construct a new Release Set.

Forward repair receives its own Release Set or declared repair identity and evidence.

### 7.9 Withdrawal

A Release Set can be withdrawn from future activation.

Already active targets follow the withdrawal contract:

- continue temporarily under bounded support;
- enter required update;
- isolate affected capabilities;
- roll back;
- recover;
- decommission.

Withdrawal does not erase the manifest or its historical evidence.

## 8. Failure States and Safe Degradation

| Failure condition | Required behavior | Retained state | Prohibited behavior | Evidence |
| --- | --- | --- | --- | --- |
| One channel identity is missing | Block assembly | Current active set | Implicit latest or omitted channel | Manifest result |
| Manifest signature or authority fails | Reject the candidate | Current active set and verified recovery sets | Staging or activation as trusted | Verification result |
| Artifact is missing or invalid | Block affected candidate | Current active artifacts | Partial-set activation | Artifact result |
| Profile compatibility fails | Reject for the target | Candidate for other valid profiles | Treating hardware similarity as compatibility | Profile result |
| Transitive compatibility cannot be evaluated | Mark candidate blocked | Current active set | Assuming compatibility from direct pairs | Compatibility result |
| Storage capacity is insufficient | Stop before unsafe staging or migration | Current active set | Exhausting active storage or recovery reserve | Capacity result |
| Migration preflight fails | Keep candidate inactive | Source schema and active services | Starting later phases | Migration preflight |
| Migration partially completes | Execute declared repair, restore, or compatible hold state | Independently valid committed component states | Reporting active success | Migration evidence |
| One service activation fails | Retain or restore declared valid composition | Current or recovery-eligible set | Mixed undeclared active services | Service result |
| Governance bundle fails | Fail closed for affected governed capabilities | Explicitly safe local or read-only behavior | Using stale or absent policy as approval | Governance result |
| Knowledge artifact fails | Keep prior compatible artifact or disable dependent capability | Unaffected services and knowledge | Treating missing knowledge as current | Knowledge result |
| System-image health gate fails | Return to recovery-eligible image or repair path | Verified recovery environment | Marking the candidate active | Boot-health receipt |
| Active-set pointer changes but health fails | Initiate declared rollback or repair and report activation failure | Last verifiable authority state | Leaving the target in an unregistered mixed state | Activation failure receipt |
| Evidence path is unavailable | Block critical activation transition | Current active set and noncritical staging | Unevidenced active-set switch | Evidence state |
| Internet becomes unavailable | Use verified offline material or retain current set | Declared local offline envelope | Weakening validation or selecting an undeclared source | Offline status |
| Optional integration is unavailable | Disable only that integration | Core compatible set | Blocking unrelated activation without profile requirement | Integration status |
| Rollback is data-incompatible | Use forward repair or validated restoration | Current protected data and recovery tools | Forcing reverse activation | Recovery decision |
| Candidate is withdrawn during staging | Stop new activation and apply withdrawal policy | Current active set | Completing activation without explicit authority | Withdrawal result |
| Component reports a mismatched identity | Mark target degraded or failed and reconcile through lifecycle controls | Verified unaffected components | Accepting the process report as a new set | Identity-drift evidence |
| Recovery candidate is unavailable | Block risky activation or use another declared repair path | Current active set | Proceeding without required recovery | Recovery-readiness result |

Safe degradation preserves a declared valid authority state. It does not create an unofficial Release Set, silently mix channels, bypass governance, weaken offline validation, or promote staged material.

## 9. Cross-System Interactions

### 9.1 Build Farm

Build Farm produces channel artifacts, candidate manifests, provenance, and test evidence from declared inputs.

It can assemble and validate Release Set candidates.

It does not activate operational targets.

### 9.2 Profile contracts

Profiles define:

- required components;
- hardware and architecture envelope;
- lifecycle model;
- offline requirements;
- integration assumptions;
- rollback and recovery strength;
- conformance tests.

A Release Set is compatible only with the profiles listed by its validated manifest.

### 9.3 Component contracts

Component contracts define service interfaces, schemas, migrations, events, health, rollback, and repair behavior.

The Release Set coordinates their versions and lifecycle order.

### 9.4 Resource Governor

Resource Governor reserves and admits resources for staging, migration, processing, and validation.

It does not authorize release activation.

### 9.5 Governance Policy Runtime

Governance Policy Runtime can evaluate deployment, exception, disclosure, privilege, and emergency policy where the active profile requires it.

A policy decision does not replace technical compatibility or health evidence.

### 9.6 kOA Node Agent and privileged broker

On applicable profiles, kOA Node Agent reports active-set identity, target state, recovery readiness, and health.

Privileged host mutations such as system-image activation use the narrow broker contract.

Neither component rewrites the Release Set manifest.

### 9.7 Audit Broker

Audit Broker records and routes activation, rollback, withdrawal, recovery, and repair evidence.

Selective disclosure reveals the release facts needed for assurance without exposing private signing material or governed payloads.

### 9.8 Offline bundles

An offline bundle transports a complete Release Set and its activation dependencies across an offline boundary.

Import and activation remain separate transitions.

### 9.9 Portability and restore

Exports and backups identify their source Release Set.

Restore validates either the same set or a declared compatible migration target.

A successful data restore does not automatically prove complete Release Set activation.

### 9.10 External integrations

External repositories, registries, mirrors, and update transports remain removable delivery mechanisms.

They cannot define the active Release Set by availability or naming convention.

## 10. Decision Closure and Validation Criteria

This document is supported by the accepted decisions declared in its metadata.

A semantic Release Set change requires:

1. an accepted owner decision;
2. impact analysis across all four channels, profiles, components, schemas, migrations, artifacts, integrations, offline bundles, lifecycle, recovery, tests, evidence, portability, and documentation;
3. canonical contract updates;
4. complete validation before authority activation.

The following assumptions are prohibited:

- each channel can be activated independently without evaluating the resulting set;
- an omitted channel means “keep whatever is installed” without recording its identity;
- “latest” is a valid active release identity;
- a directory, repository tag, branch, package list, or process inventory is the canonical Release Set;
- a signed artifact proves complete Release Set compatibility;
- download or import proves staging success;
- staging proves activation;
- service startup proves complete activation;
- an active system image alone defines the active Release Set;
- one healthy component compensates for an incompatible component;
- a governance bundle can be skipped because services appear healthy;
- knowledge artifacts can be changed without services compatibility checks;
- an old system slot proves safe rollback;
- a database backup proves safe rollback;
- a down migration proves reversibility;
- a Build Farm result activates a target;
- offline operation permits weaker verification;
- an optional integration can become a hidden activation dependency;
- a target can remain indefinitely in an undeclared mixed state;
- local process versions can redefine the active set;
- withdrawal deletes historical lineage;
- restore success proves the complete software and policy composition;
- an exception can be omitted from the Release Set claim;
- source-code behavior can override the active manifest.

This document is conformant when:

1. it is registered as `DOC-LIFE-004`, active, English, and globally scoped;
2. every canonical reference resolves;
3. every declared decision is accepted;
4. every requirement is unique, active, and testable;
5. every lock exists and applicable assertions pass;
6. every active target identifies one complete Release Set;
7. every Release Set identifies all four channel releases explicitly;
8. manifests are immutable, signed, and authority-verified;
9. every selected artifact resolves and passes artifact-class validation;
10. profile, architecture, operating-system, component, schema, event, artifact, policy, integration, offline, migration, and recovery compatibility pass;
11. independent channel updates produce a newly validated complete set;
12. candidate, validated, staged, active, superseded, withdrawn, failed, and recovery-eligible states remain distinguishable;
13. staging does not change active authority;
14. active-set switching is atomic at the authority boundary;
15. components report identities consistent with the active manifest;
16. required component-owned migrations complete and validate before active success;
17. rollback candidates have proven class-specific and data compatibility;
18. unsafe reversal uses tested forward repair or restoration;
19. failed activation preserves or restores a declared valid state;
20. offline bundles contain complete activation and recovery dependencies;
21. optional integrations remain removable unless explicitly required by profile;
22. critical lifecycle transitions produce machine-readable receipts;
23. evidence is attributable, retained, and selectively disclosable;
24. superseded and withdrawn sets remain resolvable for lineage and recovery;
25. portability and restore identify source and compatible target sets;
26. claims include target, composition, authority, channels, artifacts, migrations, tests, exceptions, evidence, and validity;
27. no partial or mixed state is represented as active;
28. no unresolved marker or implicit release identity exists;
29. required conformance tests and evidence resolve through traceability;
30. the active text contains the complete required section structure.

Applicable failure codes include:

`text
release_set_identity_missing
release_channel_identity_missing
implicit_release_identity
release_set_manifest_invalid
release_set_signature_invalid
release_set_authority_invalid
release_set_manifest_mutated
release_artifact_unresolved
release_set_profile_incompatible
release_set_transitive_compatibility_blocked
release_set_partial_staging
release_set_partial_activation
release_set_mixed_active_state
release_set_component_identity_drift
release_set_migration_incomplete
release_set_health_gate_failed
release_set_rollback_unproven
release_set_forward_repair_missing
release_set_offline_bundle_incomplete
release_set_evidence_path_unavailable
release_set_receipt_missing
release_set_restore_target_undefined
release_set_claim_incomplete
`

A required validator that cannot run produces `blocked`, not `pass`.

## 11. Non-Normative Examples

### Example 1 — Services-only change

A deployment retains its current system, governance, and knowledge releases while selecting a newer services release.

The assembler creates a new Release Set identity containing all four channel identities. Component, schema, policy-interface, knowledge-interface, profile, migration, rollback, and offline checks run before activation.

### Example 2 — Governance update

A new governance release changes a policy interface used by Publication Gateway and Orgo.

The candidate remains blocked until the selected services release proves compatibility with the new governance bundle. The governance channel is not activated merely because its bundle validates internally.

### Example 3 — Knowledge update

A new language artifact is published in the knowledge channel.

The Release Set validates SemantiK runtime compatibility, profile applicability, artifact loading, offline availability, and rollback behavior. The other channel identities remain explicit in the new set.

### Example 4 — Sovereign node activation

A sovereign node stages a signed immutable system image, service artifacts, governance bundle, and knowledge artifacts.

Component-owned migrations run, health gates pass, and the narrow privileged broker switches the system image. The node records one active-set receipt after the complete composition is confirmed.

### Example 5 — Failed migration

A services candidate requires a data migration that fails validation after a partial backfill.

The target does not report the candidate active. It retains the prior authority state, runs the declared repair or restoration procedure, and records the partial physical changes and failure evidence.

### Example 6 — Unsafe rollback

A successful migration changes data in a way that cannot safely return to the prior services release.

A later service failure triggers the forward-repair path instead of forced rollback. The repair produces a new validated Release Set and preserves migration lineage.

### Example 7 — Offline update

An offline sovereign deployment imports a verified bundle containing the complete Release Set, all required artifacts, migrations, trust material, tests, and recovery instructions.

Import leaves the current set active. Activation occurs later after local preflight, staging, migration, and health validation.

### Example 8 — Restore to a newer set

A backup created under an older Release Set is restored into a clean environment using a newer compatible set.

The restore process identifies the source set, applies declared component-owned migrations, validates all four target channel identities, and activates the target set only after restore and lifecycle checks both pass.
