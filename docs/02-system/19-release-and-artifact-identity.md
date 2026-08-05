<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-019",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "system_baseline",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "generated/component-catalog.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json",
    "generated/profile-catalog.json"
  ],
  "decision_ids": [
    "DEC-LIFE-001",
    "DEC-REL-001",
    "DEC-ART-001",
    "DEC-AUTH-001",
    "DEC-IDENT-001",
    "DEC-COMP-001",
    "DEC-DATA-001",
    "DEC-AI-001"
  ],
  "requirement_ids": [
    "REQ-REL-ID-001",
    "REQ-REL-ID-002",
    "REQ-REL-ID-003",
    "REQ-REL-ID-004",
    "REQ-REL-ID-005",
    "REQ-REL-ID-006",
    "REQ-REL-ID-007",
    "REQ-REL-ID-008",
    "REQ-REL-ID-009",
    "REQ-REL-ID-010",
    "REQ-REL-ID-011",
    "REQ-REL-ID-012",
    "REQ-REL-ID-013",
    "REQ-REL-ID-014",
    "REQ-REL-ID-015",
    "REQ-REL-ID-016",
    "REQ-REL-ID-017",
    "REQ-REL-ID-018",
    "REQ-REL-ID-019",
    "REQ-REL-ID-020",
    "REQ-REL-ID-021",
    "REQ-REL-ID-022",
    "REQ-REL-ID-023",
    "REQ-REL-ID-024",
    "REQ-REL-ID-025",
    "REQ-REL-ID-026",
    "REQ-REL-ID-027",
    "REQ-REL-ID-028",
    "REQ-REL-ID-029",
    "REQ-REL-ID-030"
  ],
  "lock_ids": [
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-AUTH-001",
    "LOCK-AUTH-002",
    "LOCK-DATA-001",
    "LOCK-COMP-001",
    "LOCK-AI-002",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-004",
    "DOC-GOV-005",
    "DOC-GOV-009",
    "DOC-GOV-010",
    "DOC-GOV-011",
    "DOC-GOV-012",
    "DOC-GOV-013",
    "DOC-GOV-015",
    "DOC-CONST-002",
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-CONST-011",
    "DOC-SYS-000",
    "DOC-SYS-001",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-007",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-017"
  ],
  "tags": [
    "release-identity",
    "artifact-identity",
    "release-channels",
    "release-set",
    "compatibility",
    "verification",
    "activation",
    "rollback",
    "revocation",
    "provenance"
  ]
}
KOA:DOC-META:END -->

# Release and Artifact Identity

## 1. Purpose

This document defines the global identity and lifecycle model for kOA releases and artifacts.

It separates:

- artifact class from artifact instance;
- artifact identity from storage location;
- artifact verification from activation;
- release identity from component runtime state;
- release channel from deployment profile;
- publisher and signer identity from activation authority;
- installation from authority;
- rollback from forward repair;
- integrity mechanisms from ordinary documentation validation.

The model supports independent evolution of the operating system, services, governance, and knowledge while preserving compatibility, provenance, offline continuity, recovery, auditability, and credible exit.

This document explains the system-level model. Exact artifact classes, release-channel records, compatibility matrices, schemas, manifests, signatures, migration contracts, and activation procedures belong to their canonical registries and artifact contracts.

## 2. Scope

This document applies globally to:

- system images and system-release artifacts;
- service bundles and component runtime artifacts;
- governance policy bundles and authority-related artifacts;
- Kristal Runtime Packs and other knowledge artifacts;
- compiled language artifacts;
- Ariane Atlases and drivers;
- offline bundles;
- signed release manifests;
- software supply-chain evidence;
- migration artifacts;
- backup, restore, export, and recovery packages when they carry lifecycle identity;
- release sets and compatibility objects;
- candidate artifacts before admission;
- revoked, superseded, rolled-back, and archived artifacts.

It applies to local, connected, intermittent, sovereign-offline, development, build-farm, hub, and control-plane environments.

It does not define:

- component business-data identity;
- ordinary database row identity;
- user-interface state;
- temporary transfer-session identity;
- cache keys that have no artifact authority;
- exact packaging technology;
- exact signature algorithm;
- exact repository product;
- exact operating-system update technology;
- profile-specific storage paths;
- content hashes for ordinary Markdown files.

Those details belong to component contracts, artifact-class contracts, profile contracts, security documents, toolchain contracts, lifecycle documents, or implementation recipes.

## 3. Canonical References

| Canonical reference | Release and artifact ownership |
| --- | --- |
| `contracts/release-channels.contract.json` | Release-channel identities, membership, compatibility, lifecycle, and channel-specific rules. |
| `contracts/artifact-classes.contract.json` | Artifact-class identities, required metadata, verification, compatibility, activation, rollback, revocation, migration, and evidence rules. |
| `generated/authority-manifest.json` | Active registry versions, authority release, canonical ownership, cutover state, and activation order. |
| `generated/decision-index.json` | Accepted lifecycle, artifact, authority, identity, component, and AI decisions. |
| `contracts/system.contract.json` | Global release, artifact, offline, degradation, and authority model. |
| `generated/component-catalog.json` | Runtime owners and component responsibility boundaries. |
| `contracts/components/*.component.json` | Component-specific artifact inputs, outputs, activation state, runtime compatibility, and failure behavior. |
| `contracts/profiles/*.profile.json` | Profile-specific channel consumption, artifact inclusion, build, publish, mirror, activation, rollback, topology, and resource rules. |
| `contracts/integration-types.contract.json` | External artifact-source, repository, mirror, distribution, and remote-service boundaries. |
| `generated/requirements-index.json` | Normative statements displayed in section 5. |
| `generated/assertion-index.json` | Cross-file lifecycle, release, ownership, authority, and profile invariants. |
| `generated/traceability.json` | Decision, requirement, artifact, release, test, evidence, exception, and claim relationships. |
| `generated/test-catalog.json` | Artifact, lifecycle, release, security, recovery, migration, and conformance test definitions. |
| `generated/evidence-catalog.json` | Verification, activation, rollback, revocation, migration, release, and recovery evidence. |
| `generated/exception-index.json` | Approved bounded deviations and compensating controls. |

A release or artifact is active only when its canonical records and applicable authority release agree.

## 4. Model and Responsibilities

### 4.1 Identity hierarchy

The lifecycle model uses these distinct identities:

| Identity | Meaning |
| --- | --- |
| Artifact class | The contract family that defines structure, verification, compatibility, activation, rollback, revocation, and evidence. |
| Artifact instance | One immutable or controlled versioned object belonging to an artifact class. |
| Artifact version | The declared version or content identity used by the artifact class. |
| Release channel | An independently versioned lifecycle stream such as system, services, governance, or knowledge. |
| Release | A declared set of artifacts published together within one release channel. |
| Release Set | A compatible selection of releases across applicable independent channels. |
| Publisher | The authority or organization that publishes the candidate artifact. |
| Signer | The identity whose cryptographic signature attests to the artifact or manifest when signing applies. |
| Release authority | The authority permitted to approve or publish a release for a channel and scope. |
| Activation authority | The authority permitted to activate the artifact in a target environment. |
| Runtime owner | The component that owns the active runtime state for the artifact. |
| Target environment | The tenant, profile, node, cluster, workspace, or environment in which compatibility and activation are evaluated. |

These identities can refer to related entities but do not collapse into one field.

### 4.2 Independent release channels

kOA uses four independent release channels.

#### System channel

The system channel carries operating-system or appliance-level artifacts and other artifacts classified as system lifecycle objects.

It can include:

- system images;
- boot and recovery artifacts;
- host-level configuration bundles;
- system activation manifests;
- system rollback metadata.

#### Services channel

The services channel carries runtime services and component deployment artifacts.

It can include:

- service bundles;
- component runtime packages;
- service schemas;
- component migrations;
- declared service compatibility manifests.

#### Governance channel

The governance channel carries active governance artifacts.

It can include:

- policy bundles;
- authority-compatible governance configuration;
- consent, disclosure, privilege, exception, or review policy artifacts;
- governance activation and revocation metadata.

#### Knowledge channel

The knowledge channel carries portable knowledge and deterministic language or navigation artifacts.

It can include:

- Kristal Runtime Packs;
- compiled language artifacts;
- Ariane Atlases;
- Ariane driver artifacts when classified in this channel;
- knowledge indexes or manifests when their artifact class grants lifecycle identity.

The exact membership of each channel is owned by `contracts/release-channels.contract.json`.

### 4.3 Artifact-class contract

An artifact class defines:

- artifact identity format;
- version or content-identity model;
- required manifest fields;
- publisher and signer requirements;
- allowed release channels;
- target profiles and environments;
- dependency and compatibility rules;
- schema requirements;
- integrity and signature requirements;
- provenance requirements;
- admission and verification procedure;
- activation granularity;
- active-state owner;
- rollback and forward-repair behavior;
- migration behavior;
- revocation behavior;
- retention of predecessors;
- evidence requirements;
- export and restore behavior.

An artifact instance cannot weaken the contract of its artifact class.

### 4.4 Artifact identity record

A complete artifact identity record includes or references:

- artifact-class identity;
- artifact identity;
- artifact version or content identity;
- release identity;
- release-channel identity;
- publisher identity;
- signer identity when applicable;
- authority domain;
- tenant and environment scope when applicable;
- creation and publication time;
- provenance;
- source or build identity when required;
- dependency identities;
- compatibility constraints;
- schema versions;
- migration requirements;
- lifecycle status;
- revocation state;
- supersession state;
- evidence references.

Storage path, URL, filename, package-manager label, container tag, and local cache key can be recorded as locations or aliases. They are not the canonical artifact identity.

### 4.5 Release identity

A release identity records:

- release-channel identity;
- release version;
- release authority;
- exact member artifacts;
- publication state;
- compatibility constraints;
- migration requirements;
- known predecessor;
- rollback or forward-repair path;
- test and evidence references;
- revocation or supersession state.

A release contains only artifacts whose class permits membership in that channel.

### 4.6 Release Set

A Release Set represents the compatible lifecycle state of one target environment.

A Release Set records:

- target profile and environment;
- system release selection;
- services release selection;
- governance release selection;
- knowledge release selection;
- intentionally absent channels;
- compatibility-evaluation result;
- required migration state;
- active exceptions;
- authority-release identity;
- activation evidence;
- predecessor Release Set;
- recovery path.

A change in one channel produces a new Release Set identity when the compatible environment state changes.

### 4.7 Candidate, verified, staged, and active states

Artifact existence and artifact authority are separate.

A typical lifecycle is:

`text
candidate
-> received
-> parsed
-> identified
-> verified
-> compatible
-> staged
-> authorized
-> activating
-> active
`

Alternative states include:

`text
rejected
quarantined
incompatible
revoked
superseded
rollback_pending
rolled_back
repair_required
archived
`

Only the active state participates in current runtime authority.

### 4.8 Verification model

Verification evaluates the checks declared by the artifact class.

Possible checks include:

- schema validation;
- artifact identity validation;
- publisher identity;
- signer identity and signature;
- provenance;
- build or source identity;
- release-channel membership;
- tenant and environment scope;
- profile compatibility;
- component compatibility;
- dependency compatibility;
- authority-release compatibility;
- migration readiness;
- revocation state;
- downgrade and substitution resistance;
- artifact integrity;
- test and evidence completeness.

Not every artifact class requires every check. The artifact-class contract defines the applicable set.

### 4.9 Integrity model

Integrity mechanisms can include:

- signatures;
- signed manifests;
- content digests;
- Merkle or content-addressed identity;
- package checksums;
- transparency or provenance records;
- reproducible-build evidence;
- bounded archive validation.

These mechanisms apply when the artifact contract requires them.

Ordinary Markdown documentation and generated explanatory files use registry, reference, structure, decision, requirement, lock, language, and generation validation. They do not receive an automatic content-hash requirement.

### 4.10 Activation ownership

Activation authority and runtime ownership remain explicit.

Examples:

- the privileged node lifecycle mechanism activates a system image;
- a service runtime or deployment controller activates a service bundle;
- Governance Policy Runtime activates a compatible policy bundle;
- Kristal Runtime activates a verified Runtime Pack;
- SemantiK Architect Runtime activates a compiled language artifact;
- Ariane Runtime activates compatible Atlas and driver artifacts.

The component that downloads or transfers an artifact does not automatically own activation.

### 4.11 Publisher, signer, and authority separation

A publisher can create or distribute a candidate artifact.

A signer can attest to artifact or manifest identity.

A release authority can approve a release for one channel and scope.

An activation authority can approve or perform activation in one target environment.

A runtime owner manages the resulting active state.

A valid signature proves only what the signature contract states. It does not prove policy authorization, compatibility, or activation approval.

### 4.12 External and candidate artifacts

User imports, external integrations, external AI services, and SenTient can produce candidate material.

Candidate material:

- keeps provenance;
- remains outside active authority;
- enters through the owning component or artifact-class admission process;
- is classified and validated;
- receives a new local artifact identity when admitted;
- does not inherit local authority from its source.

An external service cannot directly activate an artifact or write an active runtime store.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-REL-ID-001,REQ-REL-ID-002,REQ-REL-ID-003,REQ-REL-ID-004,REQ-REL-ID-005,REQ-REL-ID-006,REQ-REL-ID-007,REQ-REL-ID-008,REQ-REL-ID-009,REQ-REL-ID-010,REQ-REL-ID-011,REQ-REL-ID-012,REQ-REL-ID-013,REQ-REL-ID-014,REQ-REL-ID-015,REQ-REL-ID-016,REQ-REL-ID-017,REQ-REL-ID-018,REQ-REL-ID-019,REQ-REL-ID-020,REQ-REL-ID-021,REQ-REL-ID-022,REQ-REL-ID-023,REQ-REL-ID-024,REQ-REL-ID-025,REQ-REL-ID-026,REQ-REL-ID-027,REQ-REL-ID-028,REQ-REL-ID-029,REQ-REL-ID-030 -->
- **REQ-REL-ID-001 — SHALL:** Every active release channel, artifact class, artifact, release, and Release Set has a stable identity that is distinct from its display name, storage path, download location, installation path, and activation state.
- **REQ-REL-ID-002 — SHALL:** The system, services, governance, and knowledge release channels retain independent identities, versions, activation state, rollback state, and compatibility relationships.
- **REQ-REL-ID-003 — SHALL NOT:** A system release implicitly activates a services, governance, or knowledge release unless an active compatibility object explicitly includes that transition.
- **REQ-REL-ID-004 — SHALL:** Every artifact identifies its artifact class, artifact identity, version or content identity, publisher, signer when signing applies, release channel, target environment, compatibility constraints, provenance, and lifecycle status.
- **REQ-REL-ID-005 — SHALL:** Artifact identity remains independent of tenant workflow state, user-interface state, cache location, transfer session, temporary filename, and deployment-specific path.
- **REQ-REL-ID-006 — SHALL:** Every release identifies the exact artifact versions or content identities that constitute the release and the compatibility rules that bind them.
- **REQ-REL-ID-007 — SHALL:** A Release Set identifies one compatible active selection from each applicable independent release channel and records any intentionally absent channel.
- **REQ-REL-ID-008 — SHALL:** Download, transfer, cache, installation, unpacking, staging, or successful schema parsing does not by itself activate an artifact.
- **REQ-REL-ID-009 — SHALL:** Verification completes before activation and includes every check required by the artifact-class contract.
- **REQ-REL-ID-010 — SHALL:** Activation is atomic at the granularity declared by the artifact-class contract and does not expose a partially active artifact state.
- **REQ-REL-ID-011 — SHALL:** The last known compatible active state remains available until the replacement activation succeeds and its required evidence is secured.
- **REQ-REL-ID-012 — SHALL:** Rollback restores a compatible predecessor when rollback is safe, and forward repair follows an explicit controlled path when rollback is unsafe.
- **REQ-REL-ID-013 — SHALL:** Artifact revocation blocks future activation and applies the artifact-class contract's declared treatment to an already active artifact.
- **REQ-REL-ID-014 — SHALL:** A superseded artifact remains historically identifiable and points to its replacement or closed disposition.
- **REQ-REL-ID-015 — SHALL:** Compatibility evaluation includes artifact class, schema version, release channel, target profile, environment, component contract, dependency versions, authority version, and required migration state when applicable.
- **REQ-REL-ID-016 — SHALL:** An incompatible, unverifiable, revoked, substituted, downgraded, or incorrectly scoped artifact remains inactive.
- **REQ-REL-ID-017 — SHALL:** Artifact integrity mechanisms are required only when the artifact-class contract declares them, including release bundles, signed artifacts, supply-chain artifacts, or content-addressed artifacts.
- **REQ-REL-ID-018 — SHALL NOT:** Ordinary Markdown documentation or generated explanatory content is assigned a content-hash requirement unless its artifact-class contract explicitly classifies it as a release-integrity artifact.
- **REQ-REL-ID-019 — SHALL:** Publisher identity, signer identity, artifact identity, release authority, activation authority, and runtime ownership remain distinct authority dimensions.
- **REQ-REL-ID-020 — SHALL NOT:** Possession of an artifact, a valid signature, or publisher trust alone grants activation authority.
- **REQ-REL-ID-021 — SHALL:** Offline import uses bounded parsing, explicit artifact identity, provenance verification, compatibility validation, authorization, and evidence before activation.
- **REQ-REL-ID-022 — SHALL:** Artifact identity and release identity survive export, backup, restore, replication, mirror transfer, and offline bundle transport.
- **REQ-REL-ID-023 — SHALL:** Candidate outputs from external AI services, SenTient, user imports, and external integrations remain non-authoritative until admitted by an owning artifact or component contract.
- **REQ-REL-ID-024 — SHALL:** Every critical verification, activation, rollback, revocation, migration, release, and recovery transition produces machine-readable evidence.
- **REQ-REL-ID-025 — SHALL:** Release and artifact evidence records the evaluated identity, authority release, environment, profile when applicable, compatibility result, test outcomes, exception references, and resulting active state.
- **REQ-REL-ID-026 — SHALL:** Deployment profiles declare which artifact classes and release channels they consume, exclude, mirror, build, publish, or activate.
- **REQ-REL-ID-027 — SHALL:** Independent release channels can be updated, rolled back, or revoked without requiring unrelated channels to change when compatibility remains valid.
- **REQ-REL-ID-028 — SHALL:** A release claim is active only when all applicable requirements, tests, evidence, exceptions, compatibility rules, and authority-release references resolve.
- **REQ-REL-ID-029 — SHALL:** Interrupted activation or migration resumes, rolls back, or enters controlled recovery without creating silent partial authority.
- **REQ-REL-ID-030 — SHALL:** Every active release-and-artifact identity statement is traceable to accepted decisions, canonical registries, requirements, locks, tests, and applicable evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Artifact admission procedure

1. Receive the artifact through a declared local, remote, or offline interface.
2. Apply bounded parsing and reject unsafe structure.
3. Resolve artifact class and identity.
4. Record provenance and source context.
5. Validate schema and required manifest fields.
6. Verify publisher and signer identities when applicable.
7. Evaluate revocation, downgrade, substitution, and scope rules.
8. Evaluate release-channel membership.
9. Evaluate profile, environment, component, dependency, and authority compatibility.
10. Run required tests or validate existing test evidence.
11. Register the candidate and verification result.
12. Reject, quarantine, or stage the artifact.

Admission does not activate the artifact.

### 6.2 Release publication procedure

1. Select verified artifact instances permitted for the release channel.
2. Resolve exact versions and dependencies.
3. validate release-channel membership and compatibility.
4. Run required release tests.
5. Register evidence and active exceptions.
6. Create the release manifest.
7. Apply required signing and integrity mechanisms.
8. Publish the release as a candidate or available release.
9. Preserve the predecessor and rollback or repair relationship.
10. Record publication evidence.

Publication makes a release available; it does not activate it in a target environment.

### 6.3 Release Set evaluation

1. Identify the target profile and environment.
2. Resolve the currently active releases in all applicable channels.
3. Select the proposed channel update.
4. Resolve transitive artifact dependencies.
5. Evaluate schema, component, profile, policy, migration, and authority compatibility.
6. Resolve required exceptions.
7. Run applicable conformance and lifecycle tests.
8. Create a candidate Release Set.
9. Register the compatibility result and evidence.
10. Authorize or reject activation.

A failed compatibility evaluation leaves the current Release Set active.

### 6.4 Activation procedure

1. Confirm the candidate artifact or Release Set is verified and compatible.
2. Resolve activation authority.
3. Confirm target environment and active profile.
4. Verify required capacity, storage, backup, and recovery conditions.
5. Preserve the last known compatible active state.
6. Execute the artifact-class activation transaction.
7. Verify the resulting active identity and state.
8. Secure required local evidence.
9. Mark the new artifact or Release Set active.
10. Retire, retain, or archive the predecessor according to policy.

Active state is reported only after verification and evidence completion.

### 6.5 Rollback procedure

1. Stop new operations that depend on the failed version.
2. Identify the last known compatible predecessor.
3. Verify predecessor availability, trust, compatibility, and revocation state.
4. Determine whether data or schema migration permits rollback.
5. Authorize rollback.
6. Execute the atomic rollback transition.
7. Verify runtime and data state.
8. record rollback evidence.
9. mark the failed version inactive, quarantined, or superseded.
10. resume dependent capabilities only after verification.

### 6.6 Forward-repair procedure

Forward repair is used when rollback would violate data, schema, or authority safety.

1. Freeze affected transitions.
2. Preserve evidence and the current recoverable state.
3. identify the repair artifact or migration.
4. verify compatibility and authority.
5. test the repair against the affected state.
6. activate the repair through the declared controlled path.
7. verify restored invariants.
8. register repair evidence.
9. resume dependent capabilities.

Forward repair is not an informal manual edit to active state.

### 6.7 Revocation procedure

1. Receive or create a verified revocation record.
2. Resolve artifact, publisher, signer, release, channel, tenant, and environment scope.
3. block future activation.
4. evaluate the active-state response defined by the artifact class.
5. deactivate, quarantine, restrict, replace, or retain in controlled degraded mode.
6. preserve historical identity and evidence.
7. notify affected runtime owners and profiles.
8. update Release Set compatibility.
9. record revocation and remediation evidence.

### 6.8 Offline import procedure

1. Mount or access the offline source through a bounded interface.
2. enforce archive, path, size, recursion, decompression, and object-count limits.
3. identify the bundle and contained artifacts.
4. verify manifests, signatures, provenance, channel, and target scope.
5. evaluate local authority freshness and revocation state.
6. verify compatibility with the target profile and environment.
7. copy candidates into controlled staging.
8. record import evidence.
9. follow ordinary admission and activation procedures.

Removable-media presence does not grant trust or activation authority.

### 6.9 Interrupted activation or migration

After interruption:

1. identify the last verified transition;
2. inspect activation journal or equivalent evidence;
3. determine whether the previous state, candidate state, or migration state is complete;
4. resume only an idempotent declared step;
5. otherwise roll back or enter controlled recovery;
6. block dependent authority until state verification completes;
7. preserve diagnostic evidence.

A partially updated collection of files is not treated as an active release.

### 6.10 Export, backup, and restore

Export and backup retain:

- artifact identity;
- artifact class;
- release and channel identity;
- publisher and signer context;
- provenance;
- compatibility metadata;
- active, revoked, superseded, or archived status;
- applicable authority and evidence references.

Restore revalidates identity, compatibility, trust, revocation, and target scope before reactivation.

## 7. Failure and Degradation

### 7.1 Unknown artifact class

An artifact with no active artifact-class contract:

- remains a non-authoritative candidate;
- cannot enter a release;
- cannot become active;
- can be archived or exported as user material when policy permits.

### 7.2 Invalid identity or provenance

When identity, manifest, provenance, publisher, signer, or scope cannot be verified:

- the artifact is rejected or quarantined;
- the current active artifact remains unchanged;
- dependent activation is blocked;
- diagnostics and evidence are retained.

### 7.3 Incompatible release

When a release is individually valid but incompatible with the target environment or other active channels:

- the release remains available but inactive for that target;
- the current Release Set remains active;
- unrelated targets can continue when compatible;
- a new compatibility decision, migration, or release is required.

### 7.4 Failed activation

When activation fails:

- active authority is not transferred to the candidate;
- the last known compatible state remains active when safe;
- partial files or state remain staged or quarantined;
- rollback or forward repair begins;
- required evidence records the failure.

### 7.5 Missing evidence

When required verification or activation evidence is missing:

- the affected release or activation claim remains blocked;
- an implementation does not infer success from installed files or running processes;
- evidence can be regenerated only by rerunning the declared verification or test.

### 7.6 Revoked active artifact

When an active artifact is revoked, the artifact-class contract determines whether to:

- deactivate immediately;
- switch to a last-known-good predecessor;
- enter restricted or read-only mode;
- block new operations while preserving existing data;
- require controlled emergency repair.

The response does not silently continue normal authority.

### 7.7 Storage or mirror failure

Failure of one repository, mirror, cache, or transport path:

- does not change artifact identity;
- does not revoke an already verified active artifact;
- can block new acquisition;
- preserves local last-known-good artifacts according to retention policy;
- does not make an unverified alternate source trusted.

### 7.8 Channel-specific failure

A failed governance update does not automatically roll back the system or services channel.

A failed knowledge activation does not automatically deactivate unrelated services.

A failed services update does not automatically invalidate a compatible system image.

The affected channel and dependent compatibility relationships determine the degradation scope.

### 7.9 Offline revocation uncertainty

When a node cannot establish whether a locally cached artifact remains valid:

- the active profile's stale-revocation policy applies;
- future activation can be blocked;
- currently active use can enter restricted or last-known-good mode when allowed;
- authority is not broadened because connectivity is unavailable.

### 7.10 Recovery failure

When rollback and forward repair both fail:

- affected capabilities remain blocked or degraded;
- the recoverable state and evidence are preserved;
- emergency or clean-restore procedures become available;
- the system does not claim an active compatible release state.

## 8. Cross-Component Interactions

| Actor or component | Release or artifact responsibility | Boundary |
| --- | --- | --- |
| Release authority | Approves publication for a declared channel and scope | Does not automatically authorize target activation. |
| Publisher | Creates and distributes candidate artifacts | Publication is not activation. |
| Signer | Attests to artifact or manifest identity | Signature is not policy approval or compatibility proof. |
| Identity and Trust | Resolves publisher, signer, node, workload, tenant, environment, and authority identity | Identity context does not replace authorization. |
| Governance Policy Runtime | Evaluates governed publication, activation, downgrade, exception, or revocation decisions | Does not perform runtime activation directly. |
| kOA Node Agent | Executes allowlisted privileged system or service lifecycle operations | Requires an operation-bound authorization decision. |
| Kristal Runtime | Verifies and activates knowledge Runtime Packs | Does not own release-channel authority. |
| SemantiK Architect Runtime | Verifies and activates compiled language artifacts | Does not compile normal runtime artifacts. |
| GF Wordbench | Builds and publishes candidate language artifacts | Does not activate user runtime state. |
| Ariane Runtime | Verifies and activates compatible Atlases and drivers | External voice does not provide artifact authority. |
| Component runtime | Owns active state for its declared service artifacts | Cannot activate another component's authoritative runtime state directly. |
| Resource Governor | Ensures activation and migration remain within resource envelopes | Does not grant lifecycle authority. |
| Audit Broker | Stores classified lifecycle receipts and evidence | Does not decide activation. |
| Profile contracts | Define consumed channels, allowed artifact classes, topology, capacity, and rollback envelopes | Profile rules cannot expand global artifact safety rules. |
| External repository or mirror | Transfers candidates | Cannot directly mark artifacts active. |
| External AI or SenTient | Produces candidate material | Candidate output requires local owning-contract admission. |

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Closed decisions

| Decision | Closed rule |
| --- | --- |
| `DEC-LIFE-001` | System, services, governance, and knowledge use independent release channels. |
| `DEC-REL-001` | A Release Set is the compatible selection of applicable channel releases for a target environment. |
| `DEC-ART-001` | Artifact-class contracts own identity, verification, compatibility, activation, rollback, revocation, and evidence rules. |
| `DEC-AUTH-001` | Publication, release approval, activation, and runtime ownership are separate explicit authorities. |
| `DEC-IDENT-001` | Publisher, signer, artifact, environment, node, workload, tenant, and authority identities remain distinct. |
| `DEC-COMP-001` | Runtime components own their declared active artifact state within component boundaries. |
| `DEC-DATA-001` | Artifact transfer does not permit direct writes to another component's authoritative store. |
| `DEC-AI-001` | External AI outputs remain candidate artifacts and are not lifecycle authority. |

### 9.2 Prohibited assumptions

Authors, implementers, validators, and AI agents do not assume that:

- downloading activates;
- installing activates;
- unpacking activates;
- a running process proves the intended artifact is active;
- a filename is an artifact identity;
- a container tag is sufficient immutable identity;
- a valid signature proves authorization or compatibility;
- publisher trust applies to every artifact class or channel;
- a release version can be reused across unrelated channels without explicit identity;
- a system update includes governance or knowledge automatically;
- latest means compatible;
- newer means authorized;
- a cached artifact remains valid after revocation;
- rollback is always safe after data migration;
- every file requires a content hash;
- ordinary Markdown requires release-integrity hashing;
- a candidate generated by AI or SenTient is active knowledge;
- a backup can reactivate artifacts without revalidation;
- a mirror can change artifact identity;
- physical possession of removable media grants trust;
- one profile's packaging technology applies globally;
- partial activation can be reported as success;
- historical artifact records can be deleted merely because they are inactive;
- a release claim exists without tests and evidence.

A new implementation-affecting lifecycle choice requires an accepted owner decision before dependent authority becomes active.

## 10. Validation Criteria

This document is conformant when all applicable checks pass.

| Validation objective | Required tests |
| --- | --- |
| Release channels remain independent | `TEST-LIFE-001`, `TEST-LIFE-012`, `TEST-LIFE-013`, `TEST-LIFE-014` |
| Release Set compatibility resolves | `TEST-LIFE-002`, `TEST-DOC-VAL-019` |
| Verification precedes activation | `TEST-LIFE-003`, `TEST-DOC-VAL-017` |
| Activation is atomic | `TEST-LIFE-004` |
| Rollback restores a valid predecessor | `TEST-LIFE-005`, `TEST-LIFE-011` |
| Forward repair is available when needed | `TEST-LIFE-006` |
| Interrupted migration resumes safely | `TEST-LIFE-007`, `TEST-MIG-012`, `TEST-MIG-013` |
| Offline bundle parsing is bounded | `TEST-LIFE-008` |
| Downgrade and substitution are rejected | `TEST-LIFE-009`, `TEST-SEC-015` |
| Revocation updates active state safely | `TEST-LIFE-010` |
| Policy, language, and knowledge artifacts activate independently | `TEST-LIFE-012`, `TEST-LIFE-013`, `TEST-LIFE-014` |
| Release evidence is complete | `TEST-LIFE-015`, `TEST-DOC-VAL-016` |
| Critical transitions produce evidence | `TEST-SYS-011` |
| Optional external sources cannot mutate authority | `TEST-CROSS-013`, `TEST-SYS-003` |
| Export and restore preserve artifact identity | `TEST-EXIT-002`, `TEST-EXIT-003`, `TEST-EXIT-005` |
| Active authority activates last | `TEST-DOC-VAL-017`, `TEST-DOC-DEC-007`, `TEST-MIG-009` |
| Supply-chain evidence is verifiable | `TEST-SEC-015` |
| No ordinary Markdown hash requirement is introduced | `TEST-DOC-VAL-020` |

Additional validation confirms:

1. every release channel and artifact class identifier is unique;
2. every active artifact belongs to one active artifact class;
3. every release member is permitted by its channel;
4. every Release Set references compatible exact release identities;
5. publisher, signer, release authority, activation authority, and runtime owner references resolve;
6. every required schema, provenance, signature, integrity, compatibility, and migration check is represented;
7. every activation maps to the resulting active artifact or Release Set identity;
8. revoked and superseded identities remain historically resolvable;
9. profile-specific packaging and topology details are not generalized;
10. ordinary Markdown files do not acquire implicit content-hash requirements;
11. every requirement in section 5 exists in `generated/requirements-index.json`;
12. every decision and lock reference resolves;
13. no unresolved authority marker exists;
14. all active prose is in English.

A failed required test blocks the affected release, activation, or conformance claim.

## 11. Non-Normative Examples

### 11.1 Independent governance update

A node runs:

- system release `system-4.2.0`;
- services release `services-7.1.3`;
- governance release `governance-2.8.1`;
- knowledge release `knowledge-15.0.4`.

A new compatible governance release is verified and activated. The resulting Release Set changes only the governance selection. The operating system, services, and knowledge remain unchanged.

### 11.2 Kristal Runtime Pack

A Runtime Pack arrives from an approved publisher.

The package is parsed, identified, verified, checked for knowledge-channel membership, matched to the target profile and Kristal Runtime version, and staged. Governance authorization is obtained when required. Kristal Runtime activates it atomically and records the new active pack identity.

The downloaded file's presence is not the active state.

### 11.3 Language artifact

GF Wordbench publishes a compiled language artifact.

SemantiK Architect Runtime verifies artifact identity, publisher, compatibility, schema, and tests. It preserves the active predecessor, activates the new artifact, verifies deterministic rendering, and records evidence.

GF Wordbench does not write the runtime's active-state store.

### 11.4 Ariane Atlas update

A new Atlas supports an updated application version.

The Atlas and compatible driver are verified together. If the application version or driver capability does not match, the pair remains inactive. A successful activation applies to new or explicitly migrated sessions and retains the prior compatible pair for rollback.

### 11.5 Failed service activation

A services release passes package verification but fails a post-activation readiness check.

The candidate is not declared active. The previous compatible services release remains active or is restored. The failure evidence identifies the candidate, environment, profile, test result, and rollback outcome.

### 11.6 Offline bundle

An operator imports a signed offline bundle from removable media.

The system applies bounded archive checks, verifies bundle and member identities, checks publisher and signer scope, evaluates revocation and compatibility, stages the candidates, and follows ordinary activation procedures.

The removable device is not trusted merely because it is physically present.

### 11.7 External AI output

A user exports selected content to Gamma and later reimports a generated presentation.

The presentation is a candidate user artifact with provenance. It is not a governance, knowledge, or release artifact until an owning contract validates and admits it. Gamma cannot activate it or publish it inside kOA.

### 11.8 Documentation validation

A normative Markdown document is validated for:

- registered identity and path;
- active status;
- English language;
- required sections;
- canonical references;
- accepted decisions;
- unique requirements;
- locks;
- traceability;
- generated-block consistency;
- absence of unresolved authority.

The file does not receive an automatic content hash. A signed documentation release bundle can still use integrity mechanisms at the bundle level when its artifact contract requires them.
