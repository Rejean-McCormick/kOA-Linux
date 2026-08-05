<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-LIFE-002",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "lifecycle",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/decision-index.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "generated/artifact-catalog.json",
    "contracts/artifact-contracts/release-set.schema.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-REL-001",
    "DEC-DATA-001",
    "DEC-PROFILE-001"
  ],
  "requirement_ids": [
    "REQ-LIFE-REL-001",
    "REQ-LIFE-REL-002",
    "REQ-LIFE-REL-003",
    "REQ-LIFE-REL-004",
    "REQ-LIFE-REL-005",
    "REQ-LIFE-REL-006",
    "REQ-LIFE-REL-007",
    "REQ-LIFE-REL-008",
    "REQ-LIFE-REL-009",
    "REQ-LIFE-REL-010",
    "REQ-LIFE-REL-011",
    "REQ-LIFE-REL-012",
    "REQ-LIFE-REL-013",
    "REQ-LIFE-REL-014",
    "REQ-LIFE-REL-015",
    "REQ-LIFE-REL-016",
    "REQ-LIFE-REL-017",
    "REQ-LIFE-REL-018",
    "REQ-LIFE-REL-019",
    "REQ-LIFE-REL-020",
    "REQ-LIFE-REL-021",
    "REQ-LIFE-REL-022",
    "REQ-LIFE-REL-023",
    "REQ-LIFE-REL-024",
    "REQ-LIFE-REL-025",
    "REQ-LIFE-REL-026",
    "REQ-LIFE-REL-027",
    "REQ-LIFE-REL-028"
  ],
  "lock_ids": [
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-DATA-001",
    "LOCK-PROFILE-001",
    "LOCK-DOC-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-009",
    "DOC-GOV-010",
    "DOC-CONST-002",
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-SYS-002",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-006",
    "DOC-SYS-007",
    "DOC-SYS-008",
    "DOC-SYS-014",
    "DOC-SYS-017",
    "DOC-SYS-019",
    "DOC-SYS-020",
    "DOC-PROFILE-001",
    "DOC-PROFILE-003",
    "DOC-COMP-000",
    "DOC-DEV-014",
    "DOC-DEV-015",
    "DOC-DEV-016",
    "DOC-LIFE-000",
    "DOC-LIFE-001"
  ],
  "tags": [
    "lifecycle",
    "release-model",
    "release-channels",
    "release-sets",
    "artifact-identity",
    "compatibility",
    "atomic-activation",
    "rollback",
    "forward-repair"
  ]
}
KOA:DOC-META:END -->

# Release Model

## 1. Purpose

This document defines the global kOA release model.

The model gives every released artifact a stable identity, a canonical artifact class, one release channel, explicit compatibility, verifiable provenance, and a declared activation and recovery contract.

It separates release publication from deployment activation. A published artifact can be discovered and distributed without becoming active. An artifact becomes active only through the authority that owns its activation boundary.

The release model also permits independent evolution of system, service, governance, and knowledge artifacts while using Release Sets to record combinations that have been tested as compatible.

## 2. Scope

This document applies to:

- all published kOA artifacts;
- the system, services, governance, and knowledge release channels;
- Release Sets;
- system images and recovery artifacts;
- component and service artifacts;
- governance policy bundles;
- Kristal Runtime Packs and Kristal artifacts;
- compiled language packs;
- Ariane and other knowledge-channel artifacts assigned by canonical contracts;
- offline bundles and staged release transfer;
- release publication, distribution, installation, verification, activation, rollback, forward repair, supersession, revocation, and retirement;
- profile-specific release and assurance controls;
- compatibility tests, receipts, provenance, and conformance evidence.

This document does not:

- duplicate artifact schemas;
- assign channel membership manually in prose;
- prescribe one package manager, repository protocol, container registry, update agent, cluster orchestrator, or operating-system mechanism;
- require every profile to activate every release channel;
- make publication equivalent to activation;
- transfer application-data ownership to a release system;
- replace artifact-specific activation, migration, rollback, or recovery contracts.

## 3. Canonical References

| Canonical reference | Ownership role |
| --- | --- |
| `contracts/release-channels.contract.json` | Owns release-channel identities, membership rules, active versions, and lifecycle status. |
| `contracts/artifact-classes.contract.json` | Owns artifact-class identities, canonical owners, assigned release channels, and class-level lifecycle behavior. |
| `generated/artifact-catalog.json` | Owns artifact-contract catalog membership, paths, active versions, and lifecycle status. |
| `contracts/artifact-contracts/*.schema.json` | Owns the observable structure and required claims of each artifact class. |
| `contracts/artifact-contracts/release-set.schema.json` | Owns the Release Set artifact structure. |
| `contracts/system.contract.json` | Owns global release and activation behavior that profiles and components cannot weaken. |
| `generated/component-catalog.json` and component contracts | Own component artifact admission, activation, data migration, and recovery boundaries. |
| `contracts/profiles/*.profile.json` | Owns profile applicability, required channels, assurance controls, offline behavior, and evidence requirements. |
| `generated/requirements-index.json` | Owns the normative statements displayed in Section 5. |
| `generated/assertion-index.json` | Owns activation, recovery, Release Set, channel independence, data-authority, profile, and canonical-ownership assertions. |
| `generated/traceability.json` | Owns decision, requirement, lock, test, artifact, profile, and evidence relationships. |
| `generated/test-catalog.json` and `generated/evidence-catalog.json` | Own release validation-test and evidence identities. |

Markdown explains the lifecycle model. Canonical artifact and release values remain in their registries and contracts.

## 4. Model and Responsibilities

### 4.1 Release channels

The release model has four independent channels:

| Channel | Responsibility |
| --- | --- |
| `system` | System-image, boot, recovery, platform, and other artifacts assigned to the system authority |
| `services` | Component and service implementation artifacts assigned to service owners |
| `governance` | Governance policy and governed-control artifacts |
| `knowledge` | Kristal, language, Ariane, and other knowledge artifacts assigned by canonical artifact contracts |

The table describes channel purpose. Exact artifact membership remains owned by the release-channel and artifact-class registries.

Channel independence means that a channel can publish and activate a compatible update without requiring unrelated artifacts to receive new versions. It does not permit compatibility checks to be skipped.

### 4.2 Release artifact identity

A release artifact is an immutable, versioned publication unit with:

- artifact identity;
- artifact class;
- artifact version;
- release channel;
- integrity claim;
- provenance;
- compatibility declaration;
- applicable profile information;
- required trust claims;
- lifecycle status;
- canonical owner.

Artifact identity does not depend on the machine where it is downloaded, staged, or activated.

### 4.3 Release Set

A Release Set is a versioned compatibility statement.

It identifies:

- Release Set identity and version;
- applicable profiles or deployment classes;
- selected artifacts and versions by required channel;
- compatibility constraints;
- test results and evidence;
- provenance;
- validation outcome;
- lifecycle status;
- replacement relationships.

A Release Set does not merge channel ownership. Each artifact remains owned and activated by its own authority.

### 4.4 Lifecycle states

The global lifecycle distinguishes these states:

| State | Meaning |
| --- | --- |
| `candidate` | Built or assembled but not accepted for publication |
| `verified` | Artifact structure and required claims passed pre-publication validation |
| `published` | Available through its canonical release channel |
| `distributed` | Transferred to a target or staging location |
| `installed` | Materialized on a target but not necessarily selected |
| `staged` | Prepared for an activation attempt |
| `active` | Selected by the owning authority as current |
| `blocked` | Missing or failed authority, compatibility, trust, or validation |
| `superseded` | Replaced for new adoption while history remains |
| `deprecated` | Still identifiable but discouraged according to policy |
| `revoked` | Prohibited from new activation under the active revocation policy |
| `retired` | No longer active or available for new adoption; identity remains reserved |

Artifact contracts can refine these states without collapsing publication into activation.

### 4.5 Publication and activation separation

Publication is a channel operation. Activation is an owner operation.

The publication authority verifies that an artifact belongs in its channel and has the required publication claims.

The activating authority verifies target-specific conditions and changes active state through the artifact's declared boundary.

A repository, registry, mirror, offline bundle, cache, or control plane can distribute an artifact without acquiring activation or component-data authority.

### 4.6 Compatibility

Compatibility is evaluated across:

- artifact class;
- artifact version;
- release channel;
- target component and version;
- system and runtime version;
- governance policy version;
- knowledge artifact version;
- profile and overlays;
- data-schema and migration state;
- supported upgrade and downgrade paths;
- required trust and evidence.

Compatibility can be represented by ranges, explicit sets, constraints, or named test matrices owned by canonical contracts.

### 4.7 Activation boundary

Each artifact class defines an activation boundary.

Examples include:

- a bootable system slot or image selection;
- a component deployment or service version;
- a policy-bundle pointer;
- a Runtime Pack pointer;
- an active compiled language-pack record.

Atomicity applies to the authoritative boundary owned by the activating authority. Cross-channel coordination uses a Release Set and ordered activation plan rather than pretending that unrelated owners share one datastore transaction.

### 4.8 Recovery

Every artifact class declares one or both of:

- rollback to a known valid predecessor;
- forward repair to a new valid state.

The recovery contract identifies:

- recoverable predecessor;
- compatibility conditions;
- migration implications;
- evidence requirements;
- terminal failure behavior;
- operator or authority required to proceed.

The last valid state remains identifiable until the new state is verified as active.

### 4.9 Profile interpretation

Profiles can require:

- selected release channels;
- signed or measured artifacts;
- trust-root constraints;
- offline bundle transfer;
- staged activation;
- maintenance windows;
- independent recovery paths;
- enhanced evidence;
- control-plane coordination.

Those requirements remain profile-scoped. A profile implementation mechanism does not become the global release model.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-LIFE-REL-001,REQ-LIFE-REL-002,REQ-LIFE-REL-003,REQ-LIFE-REL-004,REQ-LIFE-REL-005,REQ-LIFE-REL-006,REQ-LIFE-REL-007,REQ-LIFE-REL-008,REQ-LIFE-REL-009,REQ-LIFE-REL-010,REQ-LIFE-REL-011,REQ-LIFE-REL-012,REQ-LIFE-REL-013,REQ-LIFE-REL-014,REQ-LIFE-REL-015,REQ-LIFE-REL-016,REQ-LIFE-REL-017,REQ-LIFE-REL-018,REQ-LIFE-REL-019,REQ-LIFE-REL-020,REQ-LIFE-REL-021,REQ-LIFE-REL-022,REQ-LIFE-REL-023,REQ-LIFE-REL-024,REQ-LIFE-REL-025,REQ-LIFE-REL-026,REQ-LIFE-REL-027,REQ-LIFE-REL-028 -->
- **REQ-LIFE-REL-001 — SHALL:** Every published release artifact has a stable artifact identity, artifact class, version, release channel, integrity claim, provenance, compatibility declaration, lifecycle status, and canonical owner.
- **REQ-LIFE-REL-002 — SHALL:** The canonical release channels are system, services, governance, and knowledge.
- **REQ-LIFE-REL-003 — SHALL NOT:** An artifact is published or activated through a release channel other than the channel assigned by its active artifact-class and release-channel contracts.
- **REQ-LIFE-REL-004 — SHALL:** Release-channel identities and membership are owned by contracts/release-channels.contract.json rather than by component prose, profile prose, or implementation recipes.
- **REQ-LIFE-REL-005 — SHALL:** A Release Set identifies a tested compatible combination of required artifact versions across the applicable release channels.
- **REQ-LIFE-REL-006 — SHALL:** A Release Set records its identity, version, applicable profiles, channel members, compatibility evidence, validation outcome, provenance, and lifecycle status.
- **REQ-LIFE-REL-007 — SHALL NOT:** A required release channel is omitted from a Release Set that claims complete compatibility for a profile requiring that channel.
- **REQ-LIFE-REL-008 — SHALL:** Independent channel updates are permitted only when active compatibility constraints and required cross-channel tests remain satisfied.
- **REQ-LIFE-REL-009 — SHALL NOT:** A newer artifact version is treated as compatible solely because its version is numerically or temporally newer.
- **REQ-LIFE-REL-010 — SHALL:** Publication, distribution, installation, verification, staging, activation, and retirement are represented as distinct lifecycle states or transitions.
- **REQ-LIFE-REL-011 — SHALL NOT:** Publication or installation alone makes an artifact active.
- **REQ-LIFE-REL-012 — SHALL:** Before activation, the owning authority validates artifact identity, class, channel, integrity, provenance, required trust, profile applicability, compatibility, authorization, and required evidence.
- **REQ-LIFE-REL-013 — SHALL:** Every artifact class defines its own activation boundary, atomicity rule, rollback behavior, forward-repair behavior, and last-valid-state handling.
- **REQ-LIFE-REL-014 — SHALL NOT:** An activation leaves partial authoritative state across the artifact boundary owned by the activating component or lifecycle authority.
- **REQ-LIFE-REL-015 — SHALL:** A failed activation preserves or restores the last valid authoritative state or enters the declared forward-repair state.
- **REQ-LIFE-REL-016 — SHALL NOT:** A downgrade, substitution, channel reassignment, or compatibility override occurs without an active authorization and the applicable validation evidence.
- **REQ-LIFE-REL-017 — SHALL:** Data migrations required by an artifact are declared, ordered, validated, and connected to rollback or forward-repair behavior before activation.
- **REQ-LIFE-REL-018 — SHALL NOT:** A release artifact writes directly to another component's authoritative data outside the owning component's active migration, import, or command contract.
- **REQ-LIFE-REL-019 — SHALL:** Profile contracts determine which release channels, artifact classes, trust controls, offline transfer controls, and evidence requirements apply to an effective deployment.
- **REQ-LIFE-REL-020 — SHALL NOT:** A profile-specific release mechanism becomes a global requirement through implementation prevalence or repeated documentation.
- **REQ-LIFE-REL-021 — SHALL:** Offline release transfer verifies bundle identity, manifest completeness, artifact integrity, provenance, compatibility, and authorization before local staging or activation.
- **REQ-LIFE-REL-022 — SHALL:** Every critical release transition emits a machine-readable receipt identifying the release or artifact, source, target, initiating authority, verification result, activation result, and recovery state.
- **REQ-LIFE-REL-023 — SHALL:** Revocation, deprecation, supersession, and retirement preserve artifact identity, history, evidence, replacement relationships, and affected-profile information.
- **REQ-LIFE-REL-024 — SHALL NOT:** A retired artifact identifier or Release Set identifier is reused.
- **REQ-LIFE-REL-025 — SHALL:** Release evidence is sufficient to reproduce the compatibility decision and determine which artifacts and profiles were tested.
- **REQ-LIFE-REL-026 — SHALL:** A release or conformance claim is blocked when required identity, integrity, trust, compatibility, profile, test, evidence, or authority information is missing or ambiguous.
- **REQ-LIFE-REL-027 — SHALL:** A semantic change to release-channel identity, artifact-class membership, Release Set semantics, compatibility rules, activation boundaries, or recovery behavior is accepted and validated before activation.
- **REQ-LIFE-REL-028 — SHALL:** Every active release requirement is traceable to accepted decisions, applicable locks, validation tests, and required evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Publishing an artifact

Publication follows this sequence:

1. resolve the artifact identity and class;
2. resolve the canonical owner and release channel;
3. validate the artifact against its active schema;
4. verify integrity, provenance, required trust, and publication authorization;
5. evaluate declared compatibility and profile metadata;
6. connect tests and evidence;
7. assign the accepted lifecycle state;
8. publish through the canonical channel;
9. emit the publication receipt.

Publication does not select the artifact as active on any target.

### 6.2 Creating a Release Set

Release Set creation:

1. identifies the applicable profiles;
2. identifies every channel required by those profiles;
3. selects candidate artifact identities and versions;
4. resolves direct and transitive compatibility constraints;
5. resolves data-migration and activation-order dependencies;
6. executes required cross-channel tests;
7. records test and evidence references;
8. signs or otherwise authenticates the set when required;
9. publishes the validated Release Set.

A missing required channel or unresolved compatibility condition blocks the set.

### 6.3 Distributing and staging

Distribution and staging:

1. resolve the target profile and current active state;
2. verify the Release Set or individual compatible artifact;
3. transfer the artifact through an authorized path;
4. verify integrity after transfer;
5. materialize it without changing the active selection;
6. prepare target-specific activation prerequisites;
7. record staging state and evidence.

### 6.4 Activating an artifact

The activating authority:

1. resolves the staged artifact and active contract;
2. verifies target identity and profile;
3. verifies artifact identity, class, channel, integrity, provenance, trust, and compatibility;
4. verifies authorization and resource prerequisites;
5. verifies required migration state;
6. preserves the last valid state;
7. applies the artifact-class activation procedure;
8. changes the active selection atomically within its boundary;
9. verifies health and readiness;
10. emits an activation receipt;
11. enters rollback or forward repair when activation cannot complete safely.

### 6.5 Updating one channel independently

An independent channel update:

1. keeps unaffected channel versions unchanged;
2. selects the candidate artifact for the changed channel;
3. re-evaluates all cross-channel compatibility constraints;
4. runs the required affected tests;
5. creates or updates the compatible Release Set when required;
6. stages and activates the artifact through its owner;
7. records the resulting active combination.

### 6.6 Revoking or retiring an artifact

Revocation or retirement:

1. identifies affected artifacts, Release Sets, profiles, and targets;
2. records the reason and effective policy;
3. blocks prohibited new activations;
4. selects a valid replacement or recovery path;
5. preserves historical identity, provenance, evidence, and replacement links;
6. updates compatibility and conformance views;
7. verifies active targets are handled according to the revocation contract.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Preserved state | Blocked or degraded behavior | Evidence |
| --- | --- | --- | --- | --- |
| Artifact identity or class is unresolved | Reject publication or activation | Existing active artifacts | Candidate artifact | Identity-resolution failure |
| Release channel is incorrect | Reject the artifact for that channel | Existing channel state | Publication or activation | Channel-validation outcome |
| Integrity or provenance fails | Quarantine or reject the artifact | Current active state | Candidate use | Integrity or provenance failure |
| Required trust cannot be established | Keep the operation blocked | Existing trusted state | Publication, transfer, or activation | Trust-validation outcome |
| Compatibility is unresolved or false | Reject the candidate combination | Last compatible Release Set | Incompatible update | Compatibility report |
| Required channel is absent from a Release Set | Reject the completeness claim | Existing validated Release Sets | New set activation | Release Set validation failure |
| Transfer is incomplete | Discard or quarantine the staged copy | Current active artifact | Candidate staging | Transfer evidence |
| Installation succeeds but activation fails | Keep installed artifact inactive | Last valid active state | Candidate activation | Activation failure receipt |
| Migration fails before commit | Restore pre-migration state when valid | Last valid data and artifact state | New activation | Migration outcome |
| Migration cannot be reversed | Enter declared forward repair | Last coherent repair state | Rollback path | Forward-repair evidence |
| Health verification fails after activation | Roll back or enter forward repair | Recoverable predecessor when valid | Candidate active state | Health and recovery receipt |
| Control plane is unavailable | Owners retain local valid authority and declared offline behavior | Current local active state | New centrally coordinated activation | Coordination-health record |
| Offline bundle is invalid or incomplete | Quarantine the bundle | Existing local release state | Offline staging or activation | Bundle-validation report |
| Evidence path is unavailable | Apply the artifact contract's synchronous-fail or bounded-queue rule | Source activation authority | Transition requiring unavailable mandatory evidence | Evidence-path state |
| Artifact is revoked | Block new activation and follow replacement policy | Historical identity and evidence | Revoked artifact adoption | Revocation record |

## 8. Cross-Component Interactions

### 8.1 Release-channel authority

Each channel authority accepts artifacts only from declared artifact owners and only through active publication contracts.

A channel authority does not become the owner of the artifact's application semantics or target activation state.

### 8.2 Artifact owners and activating components

Artifact owners define compatibility and publication claims.

Activating components or lifecycle authorities define target admission, migration, active selection, health verification, rollback, and repair.

The same organization or service can implement both roles, but the authority boundaries remain explicit.

### 8.3 Release Set coordination

A Release Set coordinates compatibility across channel owners.

The coordinator can validate the combination and order work. It cannot bypass an artifact owner's verification or write directly to component-owned authoritative state.

### 8.4 Resource and policy authorities

The Resource Governor supplies resource admission for verification, transfer, installation, activation, migration, and recovery work.

The Governance Policy Runtime supplies authorization and governed-exception decisions where required.

Neither authority owns the release artifact or performs the component's authoritative activation transition.

### 8.5 Evidence and audit

Publication, compatibility, staging, activation, rollback, repair, revocation, and retirement can emit receipts.

The evidence authority preserves those records without becoming the owner of source artifacts or active component state.

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Effect |
| --- | --- |
| `DEC-REL-001` | Establishes four independent release channels and compatible Release Sets. |
| `DEC-DATA-001` | Preserves component data ownership during release, migration, activation, and recovery. |
| `DEC-PROFILE-001` | Keeps profile-specific release and assurance mechanisms scoped to active profiles. |

### Prohibited assumptions

- publication makes an artifact active;
- installation makes an artifact active;
- the newest version is automatically compatible;
- all profiles require every release channel;
- channel independence eliminates cross-channel testing;
- a Release Set transfers ownership among channel owners;
- a control plane can bypass artifact-owner activation;
- one package manager or deployment technology defines the global release model;
- a profile-specific signed-image mechanism applies to every profile;
- a partial activation can be treated as success;
- rollback is always possible after an irreversible migration;
- forward repair can be left undefined;
- a release artifact can write directly to another component's database;
- a revoked identifier can be reused;
- missing evidence can be reconstructed from operator memory;
- a mirror, cache, or offline bundle becomes canonical release authority;
- a recipe can assign artifact-class or channel membership;
- compatibility can be inferred from successful startup alone.

## 10. Validation Criteria

This document is conformant when:

1. `DOC-LIFE-002` is active at `06-lifecycle/02-release-model.md`.
2. Every canonical reference resolves.
3. Every listed decision exists with status `accepted`.
4. Every requirement in Section 5 exists with identical strength, statement, scope, owner, source decision, and validation mapping.
5. Every listed lock exists and is active.
6. The release-channel registry contains exactly the canonical `system`, `services`, `governance`, and `knowledge` identities.
7. Every active artifact class resolves to exactly one canonical release channel.
8. Every published artifact has identity, class, version, channel, integrity, provenance, compatibility, lifecycle, and owner claims.
9. Publication, distribution, installation, staging, and activation remain distinguishable.
10. Every Release Set declares applicable profiles, required channel members, compatibility constraints, tests, evidence, and lifecycle.
11. No required channel is omitted from a complete Release Set claim.
12. Independent channel updates rerun affected compatibility validation.
13. Every artifact activation validates identity, class, channel, integrity, provenance, trust, profile, compatibility, authorization, and evidence.
14. Every activation boundary prevents partial authoritative activation.
15. Every artifact class resolves rollback or forward-repair behavior.
16. The last valid state remains identifiable through activation and recovery.
17. Unauthorized downgrade, substitution, channel reassignment, and compatibility override fail validation.
18. Data migrations resolve ordering, validation, and recovery before activation.
19. Release paths do not permit direct cross-component data writes.
20. Profile-specific release controls remain profile-scoped.
21. Offline release transfer validates complete bundle and artifact claims.
22. Critical lifecycle transitions map to receipts, tests, and evidence.
23. Revoked, superseded, deprecated, and retired identities remain historically traceable.
24. Retired artifact and Release Set identifiers are not reused.
25. Active prose is English and contains no unresolved-authority marker.
26. No normative keyword appears outside the generated requirement block.
27. The documentation dependency graph remains acyclic.

The validation entry point is:

`bash
python docs/tools/validate_docs.py
`

## 11. Non-Normative Examples

> **Non-normative example:** This example illustrates channel independence.

A service artifact can receive a compatible patch while the active system, governance, and knowledge artifacts remain unchanged. The affected compatibility checks still run before activation.

> **Non-normative example:** This example illustrates publication and activation separation.

A new Runtime Pack can be published in the knowledge channel and downloaded to a node. Kristal Runtime keeps the previous pack active until verification and atomic activation succeed.

> **Non-normative example:** This example illustrates Release Set coordination.

A Release Set can bind one system image, several service versions, one governance policy bundle, and selected knowledge artifacts for a sovereign-node profile. Each owner still activates its artifact through its own contract.

> **Non-normative example:** This example illustrates forward repair.

A service update can include an irreversible data migration. When the new service cannot start after the migration, the declared recovery path can require a corrected forward version rather than restoring an incompatible older service.

> **Non-normative example:** This example illustrates profile scoping.

A sovereign profile can require signed offline bundles and staged activation. A developer profile can use a simpler local distribution mechanism while preserving artifact identity, compatibility, and owner-controlled activation.
