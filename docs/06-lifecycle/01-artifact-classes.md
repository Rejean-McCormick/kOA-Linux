<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-LIFE-001",
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
    "contracts/artifact-classes.contract.json",
    "contracts/release-channels.contract.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/artifact-catalog.json"
  ],
  "decision_ids": [
    "DEC-REL-001",
    "DEC-PROFILE-BASELINE-001",
    "DEC-DATA-001",
    "DEC-AI-001",
    "DEC-ARI-001",
    "DEC-MEDIATHEQUE-001",
    "DEC-UCKK-EXT-001"
  ],
  "requirement_ids": [
    "REQ-LIFE-CLASS-001",
    "REQ-LIFE-CLASS-002",
    "REQ-LIFE-CLASS-003",
    "REQ-LIFE-CLASS-004",
    "REQ-LIFE-CLASS-005",
    "REQ-LIFE-CLASS-006",
    "REQ-LIFE-CLASS-007",
    "REQ-LIFE-CLASS-008",
    "REQ-LIFE-CLASS-009",
    "REQ-LIFE-CLASS-010",
    "REQ-LIFE-CLASS-011",
    "REQ-LIFE-CLASS-012",
    "REQ-LIFE-CLASS-013",
    "REQ-LIFE-CLASS-014",
    "REQ-LIFE-CLASS-015",
    "REQ-LIFE-CLASS-016",
    "REQ-LIFE-CLASS-017",
    "REQ-LIFE-CLASS-018",
    "REQ-LIFE-CLASS-019",
    "REQ-LIFE-CLASS-020",
    "REQ-LIFE-CLASS-021",
    "REQ-LIFE-CLASS-022",
    "REQ-LIFE-CLASS-023",
    "REQ-LIFE-CLASS-024",
    "REQ-LIFE-CLASS-025",
    "REQ-LIFE-CLASS-026"
  ],
  "lock_ids": [
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-DATA-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-MEDIATHEQUE-002",
    "LOCK-UCKK-EXT-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-LIFE-000",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-006",
    "DOC-SYS-007",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-013",
    "DOC-SYS-015",
    "DOC-SYS-017",
    "DOC-SYS-018",
    "DOC-PRO-000",
    "DOC-PRO-009"
  ],
  "tags": [
    "artifacts",
    "artifact-classes",
    "release-channels",
    "identity",
    "integrity",
    "compatibility",
    "activation",
    "rollback",
    "provenance",
    "retention"
  ]
}
KOA:DOC-META:END -->

# Artifact Classes

## 1. Purpose

This document explains the artifact-class model of the kOA lifecycle system.

An artifact class defines the semantic kind of a versioned object and the lifecycle controls that follow from that kind. It answers questions such as:

- how the artifact receives identity;
- which release channel can carry it;
- whether it is deployable, loadable, executable, importable, transport-only, compatibility-only, or evidence-only;
- what manifest and compatibility information it carries;
- which integrity and trust checks apply;
- what staging and activation mean;
- whether rollback is possible;
- when forward repair is required;
- what evidence and retention are required;
- which component or authority executes each transition.

Artifact class and release channel are different concepts.

A release channel organizes independent versioning, signing, publication, and compatibility. An artifact class defines the structure and behavior of an artifact inside or across those channels.

The canonical artifact-class inventory and machine-readable properties are owned by:

```text
contracts/artifact-classes.contract.json
```

This document provides interpretation and procedures. It does not become a second owner of the class identifiers, schemas, defaults, channel membership, or validation rules.

## 2. Scope

This document applies globally to:

- artifacts built by developer and build-farm profiles;
- artifacts published through the four release channels;
- artifacts transferred through offline bundles;
- artifacts staged or activated on nodes and hubs;
- knowledge and media artifacts consumed by Kristal, language, Ariane, and kOA Mediatheque runtimes;
- governance policy bundles;
- migrations;
- trust and revocation updates;
- recovery material;
- Release Sets;
- Sovereignty Bundles;
- receipts, attestations, and lifecycle evidence.

It governs artifact classification from creation through:

```text
built
  → verified
  → approved
  → published
  → imported or staged
  → active when the class supports activation
  → superseded, revoked, retired, or retained as evidence
```

Not every class enters every state.

Transport, compatibility, and evidence artifacts are not activated as runtime payloads unless their class contract explicitly defines an independent active effect.

This document does not own:

- exact artifact schemas;
- exact signature algorithms;
- exact digest algorithms;
- registry endpoints;
- storage paths;
- profile-specific retention periods;
- component-specific activation commands;
- build-tool versions;
- release approval workflows.

Those details belong to artifact contracts, security contracts, profiles, component contracts, toolchains, and lifecycle registries.

## 3. Canonical References

| Canonical reference | Responsibility |
| --- | --- |
| `contracts/artifact-classes.contract.json` | Artifact-class identifiers, categories, channels, manifests, schemas, lifecycle capabilities, compatibility, evidence, retention, and owning authorities. |
| `contracts/release-channels.contract.json` | The `system`, `services`, `governance`, and `knowledge` channels and their publication authorities. |
| `contracts/system.contract.json#/release_model` | Global release-channel independence and Release Set model. |
| `generated/artifact-catalog.json` | Active artifact contract and schema inventory. |
| `generated/component-catalog.json` | Component-owned loading, execution, staging, activation, and rollback interfaces. |
| `generated/profile-catalog.json` | Profile applicability, trust, offline, recovery, and retention requirements. |
| `generated/test-catalog.json` | Artifact verification, compatibility, activation, rollback, recovery, and attack-resistance tests. |
| `generated/evidence-catalog.json` | Build, verification, approval, signing, publication, import, activation, rollback, and recovery evidence. |
| `generated/requirements-index.json` | Normative statements displayed in Section 5. |
| `generated/assertion-index.json` | Release-channel, activation, compatibility, AI, component, and data invariants. |
| `generated/traceability.json` | Links among decisions, classes, channels, contracts, profiles, tests, evidence, and documents. |
| `generated/exception-index.json` | Approved bounded deviations and compensating controls. |

The class registry owns the catalog. Tables in this document are generated projections or explanatory summaries.

## 4. Model and Responsibilities

### 4.1 Artifact identity

Every artifact has an identity separate from:

- source revision;
- human-readable version;
- filename;
- repository tag;
- publication URI;
- active deployment slot;
- tenant assignment;
- audience;
- workflow status;
- approval status.

The class contract defines which bytes and semantic fields participate in identity.

Promotion preserves artifact identity only when the artifact itself is unchanged.

A rebuild creates a new artifact instance because toolchain, environment, timestamps, generated content, or other build inputs can change even when source and declared version appear identical.

Publication metadata can associate an immutable artifact with channel, audience, status, and authority without rewriting the artifact.

### 4.2 Artifact-class categories

Artifact classes are grouped by lifecycle behavior.

| Category | Meaning |
| --- | --- |
| `deployable` | Changes the selected system or service implementation when activated. |
| `loadable` | Is loaded by a runtime without replacing the complete host or service implementation. |
| `executable_transition` | Performs a bounded migration, synchronization, recovery, or trust transition. |
| `transport_envelope` | Carries one or more artifacts across a connected or disconnected boundary. |
| `compatibility_statement` | Declares tested relationships among independently versioned artifacts. |
| `portable_exit_package` | Supports export, restoration, transfer, and credible exit. |
| `evidence` | Records a transition, test, decision, provenance statement, or publication result. |

One class can have more than one category only when its registry contract explicitly defines the interaction.

For example, an offline bundle is a transport envelope. Its contained service artifact remains a deployable service artifact and keeps its own identity.

### 4.3 Canonical class catalog

<!-- GENERATED:ARTIFACT-CLASSES:BEGIN source=contracts/artifact-classes.contract.json#/artifact_classes -->
| Artifact class | Category | Primary channel | Active effect |
| --- | --- | --- | --- |
| `system_image` | Deployable | `system` | Selects a bootable operating-system and node-runtime deployment after verified staging and boot acceptance. |
| `service_artifact` | Deployable | `services` | Selects a component or service implementation after compatibility, migration, and health validation. |
| `governance_policy_bundle` | Loadable and executable policy | `governance` | Selects the policy bundle used for governed decisions within its declared scope. |
| `kristal_artifact` | Knowledge source or recognized reference | `knowledge` | Provides immutable epistemic content and lineage; recognition and distribution status remain separate records. |
| `kristal_runtime_pack` | Loadable | `knowledge` | Supplies a verified runtime query package derived from declared Kristal sources and policies. |
| `pgf_artifact` | Loadable | `knowledge` | Supplies a compiled GF grammar artifact to the language runtime. |
| `atlas_artifact` | Loadable knowledge projection | `knowledge` | Supplies a versioned atlas or navigable knowledge projection with source lineage. |
| `language_runtime_pack` | Loadable | `knowledge` | Groups compatible compiled language resources, metadata, and runtime requirements. |
| `ariane_artifact` | Loadable | `knowledge` | Supplies deterministic local navigation, action, accessibility, or interaction definitions without granting external voice authority. |
| `approved_knowledge_package` | Loadable or importable | `knowledge` | Carries an approved knowledge package whose consumer and authority semantics are declared by contract. |
| `migration_artifact` | Executable transition | Channel of the affected artifact or data owner | Transforms declared state between compatible versions with checkpoints and recovery behavior. |
| `trust_update_bundle` | Executable transition | `governance` or class-declared trust channel scope | Updates trust roots, signer scope, revocation state, or trust epochs under a high-assurance transition. |
| `offline_bundle` | Transport envelope | Cross-channel | Carries verified payloads across disconnected boundaries; import and payload activation remain separate. |
| `recovery_bundle` | Transport envelope and recovery input | `system` or affected channel | Provides verified material and instructions for a bounded recovery procedure. |
| `sovereignty_bundle` | Portable exit package | Cross-channel | Exports declared data, artifacts, manifests, trust material, and restoration instructions for independent recovery or exit. |
| `release_set` | Compatibility statement | Cross-channel | Binds tested compatible identities from the four independent release channels. |
| `evidence_receipt` | Evidence | None | Records a decision, build, verification, publication, import, activation, rollback, recovery, or other critical transition. |
<!-- GENERATED:ARTIFACT-CLASSES:END -->

The registry can define narrower subtypes without changing the distinction between class and channel.

### 4.4 Release channels

The four canonical release channels are:

- `system`;
- `services`;
- `governance`;
- `knowledge`.

Channel identity does not replace artifact-class identity.

The `knowledge` channel includes Kristal artifacts, PGF artifacts, Atlases, language runtime packs, Ariane artifacts, and approved knowledge packages.

A class that spans channels, such as `offline_bundle`, `release_set`, `sovereignty_bundle`, or a cross-channel evidence record, declares the included channel scopes explicitly.

### 4.5 Common manifest

Every release-relevant artifact manifest contains the class-required subset of:

- artifact identity;
- artifact class;
- class-contract version;
- human-readable version;
- release channel;
- created time;
- producer;
- source identities;
- toolchain identities;
- file or payload inventory;
- integrity values;
- signatures;
- target profiles;
- architecture and platform;
- component compatibility;
- schema compatibility;
- peer-artifact compatibility;
- dependency identities;
- migration requirements;
- rollback or forward-repair constraints;
- evidence references;
- SBOM reference;
- provenance reference;
- revocation and downgrade information;
- retention class.

A transport envelope includes payload references rather than absorbing the identity of its payloads.

### 4.6 Integrity and trust

Verification is class-aware.

Common checks include:

- manifest schema;
- artifact-class match;
- payload inventory;
- digest or equivalent integrity identity;
- signature;
- signer and trust scope;
- audience and environment scope;
- expiry or validity;
- revocation;
- replay or sequence protection;
- downgrade floor;
- target profile;
- target component;
- dependency and Release Set compatibility;
- required evidence.

A cryptographically valid signature is insufficient when the signer lacks the required class, channel, profile, environment, tenant, or audience scope.

### 4.7 Compatibility

Compatibility is an explicit relationship rather than a version-number guess.

An artifact class defines its applicable compatibility dimensions, which can include:

- profile versions;
- hardware envelope;
- operating-system version;
- service API and event contract;
- component contract version;
- data-schema version;
- policy-runtime version;
- Kristal query contract;
- PGF or language-runtime contract;
- Ariane action contract;
- kOA Mediatheque object contract or UCKK publication-package contract;
- trust epoch;
- required peer-artifact identities;
- migration path;
- rollback window.

Independent channel updates remain permitted only when all declared compatibility constraints continue to pass.

### 4.8 Lifecycle states

The common lifecycle vocabulary is:

```text
built
verified
approved
published
imported
staged
active
superseded
revoked
retired
rejected
quarantined
```

The artifact-class registry defines the states and transitions applicable to each class.

Examples:

- an evidence receipt is created and retained but not staged as executable code;
- a Release Set is approved and published but does not replace a service;
- an offline bundle is imported and unpacked to quarantine, while each payload follows its own class lifecycle;
- a migration artifact is staged for execution and completes, fails, resumes, or enters forward repair;
- a Kristal source artifact can be recognized and distributed without becoming the active Runtime Pack.

### 4.9 Build, verification, and approval

Build produces a candidate artifact and build evidence.

Verification proves class-specific structure, integrity, compatibility, security, and test results.

Approval is a governance decision that authorizes a declared next step, such as publication, import, activation, or emergency use.

These remain separate transitions.

The build farm cannot approve its own artifact merely because the build and tests passed.

### 4.10 Publication

Publication associates an immutable artifact identity with:

- release channel;
- repository or distribution endpoint;
- audience;
- status;
- authority;
- signatures;
- evidence;
- revocation and supersession relationships.

Publication does not activate the artifact on every node, tenant, runtime, or component.

Republishing modified bytes creates a new artifact identity.

### 4.11 Import and quarantine

Imported artifacts enter a bounded quarantine process before staging.

Import validation includes:

- bounded manifest parsing;
- path and archive safety;
- duplicate-name handling;
- payload size and count limits;
- signature and trust;
- inventory integrity;
- audience and profile;
- expiry;
- replay and sequence protection;
- revocation and downgrade;
- class-specific validation;
- policy result when required.

A valid offline bundle can be accepted as a transport envelope while one or more payloads remain rejected or incompatible.

### 4.12 Staging and activation

Staging places a verified artifact into the location or state needed for activation without changing current authority.

Activation is class-specific.

| Class family | Activation meaning |
| --- | --- |
| System image | Select a staged boot deployment, then accept it only after boot-health validation. |
| Service artifact | Switch the component implementation using restart, blue/green, canary, rolling, or another declared strategy. |
| Governance policy bundle | Select one verified policy identity atomically while preserving decision-receipt lineage. |
| Runtime or language pack | Switch a verified pack or catalog pointer atomically and preserve the previous compatible pack. |
| Migration artifact | Execute a declared state transition; completion, checkpoint, and repair are recorded. |
| Trust update | Commit a new trust or revocation state under the class's high-impact authorization. |
| Recovery bundle | Enter and complete a declared recovery procedure. |
| Transport, compatibility, or evidence artifact | No direct runtime activation unless a separate class-specific transition is declared. |

An active pointer, boot slot, service deployment, database state, or runtime pack is not changed partially.

### 4.13 Rollback and forward repair

Rollback semantics differ by class.

- system images can return to a retained boot deployment when trust and migration floors permit;
- service artifacts can return to a previous service only while schema and emitted-event compatibility permit;
- policy bundles can return to a previous known-good policy identity when revocation and decision compatibility permit;
- runtime packs can return to a compatible retained pack;
- trust updates often require a dedicated trust-recovery procedure rather than ordinary rollback;
- irreversible migrations require forward repair;
- published knowledge source identity is not erased by activation rollback;
- evidence receipts are corrected or superseded through additional evidence rather than edited.

The class contract identifies:

- rollback trigger;
- authorization;
- previous-state retention;
- data implications;
- revocation and downgrade floors;
- recovery dependencies;
- evidence.

### 4.14 Class-specific principles

#### System image

A system image includes the operating-system and node-runtime payload declared by its contract. It is immutable after build, signed, profile-compatible, and staged separately from the active boot.

Boot success alone is not acceptance. Required service, storage, policy, runtime, and recovery checks determine acceptance.

#### Service artifact

A service artifact contains one component implementation or a declared service bundle.

Its activation accounts for API, event, data-schema, migration, and peer-service compatibility.

Runtime package installation outside the declared artifact is not part of a conforming production release.

#### Governance Policy Bundle

Policy that affects authorization, disclosure, rights, recourse, activation, emergency behavior, retention, or AI integration is a versioned governance artifact.

The bundle contains declared modules, inputs, reason and obligation catalogs, tests, ownership, approval, scope, compatibility, and signatures.

Existing decision receipts keep the policy identity used at decision time.

#### Kristal artifact and Runtime Pack

Kristal source and reference identity derives from canonical epistemic content and lineage.

Tenant, workflow, approval, assignment, distribution, and UI status do not change the core content identity.

A Runtime Pack is a derived loadable artifact with manifest, file inventory, source lineage, query contract, compatibility, and status metadata.

#### PGF and language runtime artifacts

GF Wordbench owns grammar authoring and compilation.

The runtime consumes verified compiled PGF and language packs. The runtime does not rebuild grammar sources or accept an uncompiled development workspace as a runtime pack.

#### Ariane artifacts

Ariane artifacts define deterministic local interaction structures, navigation, actions, accessibility, and local command mappings according to their contract.

Optional external voice remains a separate integration. An Ariane artifact does not embed an unapproved provider or make local navigation unavailable when voice is absent.

#### kOA Mediatheque artifacts and UCKK publication packages

The kOA Mediatheque remains deterministic. Local media identity, derivatives, exports, and packages preserve declared lineage. UCKK publication packages remain external-delivery artifacts and do not transfer authority over the local source object.

External Suno or Gamma results enter as user-triggered candidate media with provenance and controlled kOA Mediatheque admission; they do not silently become authoritative local media or UCKK publications.

#### Migration artifacts

A migration is a versioned executable transition rather than an informal administrator command.

Its identity binds code or transformation rules, source and target versions, data scope, checkpoints, resource limits, expected effects, test vectors, backup requirements, and recovery behavior.

#### Offline Bundle

An offline bundle carries artifacts and instructions across disconnected boundaries.

It includes issuer, audience, channel and environment scope, inventory, integrity, confidentiality, compatibility, replay protection, signatures, and bounded import requirements.

Import and activation produce separate receipts.

#### Release Set

A Release Set is a signed compatibility statement across the four channels.

It references artifact identities; it does not merge their identity or signing authority.

The referenced combination is tested as a set, and each channel remains independently replaceable when compatibility permits.

#### Sovereignty Bundle

A Sovereignty Bundle supports credible exit, independent restoration, and transfer.

It can contain exports, manifests, schemas, artifact references, trust material, policy references, migration guidance, and restoration instructions. It preserves each contained object's ownership and identity.

#### Evidence receipts

Receipts and attestations describe what happened.

They can record build provenance, test results, policy decisions, publication, import, activation, rollback, recovery, or exceptions.

They do not perform the transition they describe and cannot be edited to change history.

### 4.15 SBOM, provenance, and signing

Software-bearing release artifacts carry the SBOM required by their class.

Provenance identifies:

- source;
- toolchain;
- dependencies;
- build environment;
- commands;
- target;
- tests;
- policy;
- output identity.

Signing is performed through a bounded signing authority.

A successful build does not compel signing. A successful signature does not compel approval, publication, import, or activation.

### 4.16 Retention

Retention is class- and profile-specific.

The retained set can include:

- active artifact;
- previous known-good artifact;
- recovery environment or bundle;
- manifests;
- signatures;
- Release Set;
- migration metadata;
- rollback constraints;
- SBOM;
- provenance;
- activation receipt;
- revocation and supersession records;
- required audit or conformance evidence.

A cache is not a retention mechanism for authoritative recovery material.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-LIFE-CLASS-001,REQ-LIFE-CLASS-002,REQ-LIFE-CLASS-003,REQ-LIFE-CLASS-004,REQ-LIFE-CLASS-005,REQ-LIFE-CLASS-006,REQ-LIFE-CLASS-007,REQ-LIFE-CLASS-008,REQ-LIFE-CLASS-009,REQ-LIFE-CLASS-010,REQ-LIFE-CLASS-011,REQ-LIFE-CLASS-012,REQ-LIFE-CLASS-013,REQ-LIFE-CLASS-014,REQ-LIFE-CLASS-015,REQ-LIFE-CLASS-016,REQ-LIFE-CLASS-017,REQ-LIFE-CLASS-018,REQ-LIFE-CLASS-019,REQ-LIFE-CLASS-020,REQ-LIFE-CLASS-021,REQ-LIFE-CLASS-022,REQ-LIFE-CLASS-023,REQ-LIFE-CLASS-024,REQ-LIFE-CLASS-025,REQ-LIFE-CLASS-026 -->
- **REQ-LIFE-CLASS-001 — SHALL:** Every active artifact shall declare exactly one artifact class registered in contracts/artifact-classes.contract.json.
- **REQ-LIFE-CLASS-002 — SHALL:** Every artifact class shall define its identity model, release-channel eligibility, required manifest, integrity controls, compatibility fields, lifecycle states, activation semantics, recovery behavior, retention, and required evidence.
- **REQ-LIFE-CLASS-003 — SHALL NOT:** An artifact shall be interpreted or activated as a different artifact class without a declared conversion that produces a new artifact identity.
- **REQ-LIFE-CLASS-004 — SHALL:** Artifact identity shall remain stable across promotion when the artifact bytes and canonical semantic payload are unchanged.
- **REQ-LIFE-CLASS-005 — SHALL:** Rebuilding source shall produce a distinct artifact instance and shall require independent verification even when the declared version is unchanged.
- **REQ-LIFE-CLASS-006 — SHALL:** Published artifact content shall be immutable; supersession, revocation, audience, recognition, and activation status shall be represented by separate signed or receipted records.
- **REQ-LIFE-CLASS-007 — SHALL:** Every artifact class shall define whether it is deployable, loadable, executable, importable, transport-only, compatibility-only, evidence-only, or a combination explicitly permitted by its contract.
- **REQ-LIFE-CLASS-008 — SHALL NOT:** Publication, import, staging, approval, signing, or verification alone shall not be represented as activation.
- **REQ-LIFE-CLASS-009 — SHALL:** Every activatable artifact class shall define atomic activation or an equivalent transition that prevents partial authoritative state.
- **REQ-LIFE-CLASS-010 — SHALL:** Every activatable or executable artifact class shall define rollback or forward-repair behavior appropriate to its state and data effects.
- **REQ-LIFE-CLASS-011 — SHALL NOT:** An artifact shall be activated when signature, integrity, trust scope, compatibility, revocation, downgrade, profile, or required evidence validation fails.
- **REQ-LIFE-CLASS-012 — SHALL:** Every release artifact shall identify its artifact class, artifact version, release channel, target profiles, producer, source lineage, toolchain, compatibility, integrity identity, and evidence references.
- **REQ-LIFE-CLASS-013 — SHALL:** Software-bearing release artifacts shall include the SBOM and provenance required by their artifact-class contract.
- **REQ-LIFE-CLASS-014 — SHALL:** Artifact compatibility shall be evaluated against the target profile, active component contracts, data-schema versions, required peer artifacts, trust state, and applicable Release Set.
- **REQ-LIFE-CLASS-015 — SHALL:** The system, services, governance, and knowledge release channels shall remain independently versioned, signed, published, and activated.
- **REQ-LIFE-CLASS-016 — SHALL:** A Release Set shall bind only tested compatible artifact identities and shall not silently embed or activate the authority of a referenced channel.
- **REQ-LIFE-CLASS-017 — SHALL:** An offline bundle shall remain a transport envelope whose valid import does not authorize activation of its payloads.
- **REQ-LIFE-CLASS-018 — SHALL:** Migration artifacts shall declare compatible source and target versions, checkpoints, idempotency or resumability, data effects, backup requirements, and rollback or forward-repair constraints.
- **REQ-LIFE-CLASS-019 — SHALL:** Trust and revocation artifacts shall declare issuer, trust scope, sequence or epoch, applicability, validity, replay protection, and recovery behavior.
- **REQ-LIFE-CLASS-020 — SHALL:** Kristal content identity shall remain independent from tenant workflow, interface state, distribution status, and recognition status.
- **REQ-LIFE-CLASS-021 — SHALL:** Compiled language artifacts and language runtime packs shall remain distinct from development-time grammar sources and build workspaces.
- **REQ-LIFE-CLASS-022 — SHALL NOT:** Ariane artifacts shall introduce native AI authority or make local navigation depend on optional external voice.
- **REQ-LIFE-CLASS-023 — SHALL NOT:** kOA Mediatheque artifacts shall encode AI-generated classification, routing, tagging, summarization, transcription, translation, or content generation as baseline authority; UCKK publication packages shall contain only explicitly admitted and authorized content.
- **REQ-LIFE-CLASS-024 — SHALL:** Evidence-only artifacts and receipts shall be immutable, attributable, integrity-verifiable, and incapable of directly activating or mutating the state they describe.
- **REQ-LIFE-CLASS-025 — SHALL:** Artifact retention shall preserve the active artifact, required previous known-good state, applicable recovery material, manifests, signatures, compatibility metadata, and evidence for the period owned by the artifact-class and profile contracts.
- **REQ-LIFE-CLASS-026 — SHALL:** Creating or materially changing an artifact class shall require an accepted decision, registry and schema updates, impact analysis, requirements, locks, tests, evidence expectations, and lifecycle documentation before activation.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Registering an artifact class

A new class is introduced through this order:

1. accept the owner decision;
2. assign the permanent class identifier;
3. define category and eligible channels;
4. define identity and immutability;
5. define the manifest and schema;
6. define integrity and trust checks;
7. define compatibility dimensions;
8. define lifecycle states and transitions;
9. define staging and activation effects;
10. define rollback or forward repair;
11. define evidence and retention;
12. define profile and component owners;
13. add requirements and locks;
14. add verification, attack, activation, recovery, and retention tests;
15. add traceability and documentation;
16. activate the registry, schema, tests, and documentation together.

An implementation file or package format does not become an active artifact class by existing in a repository.

### 6.2 Building an artifact

Build:

1. resolves the class contract;
2. resolves source, dependencies, toolchain, and target;
3. creates a clean build environment when required;
4. executes the declared build commands;
5. collects only declared outputs;
6. assigns artifact identity;
7. generates the manifest;
8. generates SBOM and provenance when applicable;
9. records build evidence;
10. places the candidate in non-authoritative staging.

### 6.3 Verifying an artifact

Verification:

1. parses the bounded manifest;
2. validates class and contract version;
3. verifies inventory and integrity;
4. verifies signatures and trust scope;
5. verifies source and provenance;
6. evaluates vulnerability and policy checks when applicable;
7. runs class tests;
8. checks target profiles and components;
9. checks peer-artifact and schema compatibility;
10. checks revocation and downgrade state;
11. records a verification result;
12. marks the candidate verified, rejected, or quarantined.

### 6.4 Publishing an artifact

Publication:

1. verifies approval for the selected channel and audience;
2. verifies the exact artifact identity;
3. verifies signature and evidence;
4. uploads or registers the immutable artifact;
5. verifies repository state;
6. creates the publication record and receipt;
7. preserves supersession and revocation relationships.

A failed or unverifiable upload remains unconfirmed.

### 6.5 Importing an offline bundle

Import:

1. detects media or receives the bundle;
2. copies the bundle to quarantine;
3. parses a bounded manifest;
4. verifies bundle identity, signature, scope, expiry, sequence, and replay controls;
5. verifies inventory, sizes, and archive safety;
6. validates each payload by its own artifact class;
7. evaluates compatibility and policy;
8. records the import result;
9. stages eligible payloads separately;
10. leaves activation to each payload's class procedure.

### 6.6 Activating an artifact

Activation:

1. identifies the current and candidate artifacts;
2. verifies current authority and target profile;
3. verifies candidate integrity, trust, compatibility, revocation, and evidence;
4. verifies migration and recovery prerequisites;
5. stages the candidate;
6. records the expected transition;
7. performs the class-specific atomic switch or bounded executable transition;
8. runs acceptance checks;
9. commits the active identity or invokes rollback or repair;
10. produces the activation result and evidence.

### 6.7 Supersession and revocation

Supersession:

1. identifies the replacement;
2. preserves the original identity;
3. records compatibility and migration;
4. updates publication metadata;
5. retains required recovery state;
6. informs applicable Release Sets and profiles.

Revocation:

1. identifies the revoked artifact and scope;
2. records signer and authority;
3. records reason and effective sequence or epoch;
4. distributes the revocation;
5. blocks new activation;
6. evaluates active instances;
7. invokes replacement, rollback, isolation, or recovery;
8. preserves evidence.

### 6.8 Retiring an artifact class

Class retirement requires:

- no new artifact creation under the class;
- replacement or removal rationale;
- disposition of active artifacts;
- migration and compatibility guidance;
- retained schemas and identifiers;
- retained verification capability for historical artifacts;
- updated profiles, components, tests, locks, and Release Sets;
- historical evidence.

The class identifier remains reserved.

## 7. Failure States and Safe Degradation

| Failure state | Required behavior |
| --- | --- |
| Artifact class is absent or unknown | Verification and activation are blocked. |
| Artifact claims a class but fails that class's schema | The artifact is rejected or quarantined. |
| Integrity identity does not match | The artifact is rejected; no partial payload is trusted. |
| Signature is valid but signer scope is wrong | The artifact is rejected for the requested class, channel, audience, or profile. |
| Required evidence is absent | Approval, publication, import, or activation remains blocked according to the class contract. |
| Compatibility cannot be established | Staging or activation is blocked. |
| Referenced peer artifact is unavailable | Activation is blocked or a previously validated compatible set remains active. |
| Revocation freshness is unavailable offline | The node uses the newest trusted epoch it possesses and exposes staleness; higher-risk activation can remain blocked. |
| Downgrade floor is violated | Activation is blocked unless a separate authorized emergency recovery path permits it. |
| Staging fails | The current active state remains unchanged. |
| Activation acceptance fails | The class-specific rollback or forward-repair procedure begins. |
| Service rollback conflicts with data migration | The service remains blocked or moves forward to a compatible repair version. |
| Irreversible migration fails | The system uses checkpoints, verified backup, and forward repair; it does not claim complete rollback. |
| Offline bundle contains one invalid payload | The invalid payload is rejected; valid payloads remain independently evaluated and are not activated automatically. |
| Release Set is incompatible | Coordinated activation is blocked; independently compatible channel states remain unchanged. |
| Runtime Pack or language pack is corrupt | The previous known-good compatible pack remains active when available. |
| Policy bundle is invalid or contradictory | The active policy remains unchanged and the candidate is rejected. |
| Trust update fails | The existing trusted state remains active and recovery follows the trust-update contract. |
| Evidence receipt cannot be stored for an evidence-required transition | The transition remains blocked or uncommitted. |
| Retained previous artifact is missing | Automatic rollback is unavailable and the recovery or forward-repair path is used. |

A failed artifact never acquires authority merely because it is locally present, cached, imported, or signed by an unrelated trust scope.

## 8. Cross-Component Interactions

### 8.1 Build farm

The build farm produces candidate artifacts, SBOMs, provenance, test evidence, and staging records.

It does not approve, activate, or redefine artifact classes.

### 8.2 Identity and Trust

Identity and Trust verifies issuers, signers, trust roots, trust scopes, revocations, and relying context.

It does not decide component compatibility or execute activation.

### 8.3 Governance Policy Runtime

The Governance Policy Runtime evaluates activation, publication, disclosure, emergency, downgrade, exception, and other governed conditions when required by profile or class.

It does not perform filesystem, boot, service, database, or runtime-pack transitions.

### 8.4 kOA Node Agent

The Node Agent performs bounded node-local staging, activation, rollback, recovery, and host-facing transitions.

It acts only on verified class-specific requests and does not become the policy or artifact owner.

### 8.5 Component runtimes

Each component runtime verifies and consumes only artifact classes declared by its component contract.

A runtime does not reinterpret an unknown package as a supported class.

### 8.6 Publication Gateway

The Publication Gateway governs cross-domain publication and produces publication receipts.

Release-repository publication can use separate lifecycle integrations; neither path changes the artifact's source ownership.

### 8.7 Audit Broker and evidence system

Critical lifecycle transitions emit declared events and evidence.

The Audit Broker and evidence system preserve accountability without becoming the owner of active artifact state.

### 8.8 Kristal Runtime

Kristal Runtime verifies and serves active Kristal Runtime Packs.

It preserves Kristal content lineage and does not merge tenant workflow into core content identity.

### 8.9 SemantiK Architect Runtime

The language runtime loads compiled PGF and language packs.

GF Wordbench and the build farm remain responsible for development-time compilation and artifact creation.

### 8.10 Ariane Runtime

Ariane Runtime loads verified deterministic interaction artifacts.

External voice remains an optional integration and is not activated by an Ariane local artifact.

### 8.11 kOA Mediatheque and external UCKK target

The kOA Mediatheque preserves source and derived-media lineage and consumes only declared artifact or import classes. The external UCKK Moodle platform consumes only authorized publication packages through its declared integration.

External AI results use controlled export and re-import with provenance and user approval.

### 8.12 Data-owning components

Migration artifacts execute through the owning component or its declared migration boundary.

A lifecycle tool does not write another component's authoritative data outside that contract.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Accepted decisions

| Decision | Effect |
| --- | --- |
| `DEC-REL-001` | Defines four independent release channels and signed Release Sets for tested compatibility. |
| `DEC-PROFILE-BASELINE-001` | Keeps profile-specific activation, retention, trust, and recovery requirements scoped to profile contracts. |
| `DEC-DATA-001` | Preserves logical component data ownership during migrations, backup, restore, and physical topology changes. |
| `DEC-AI-001` | Prevents native AI from becoming hidden artifact authority and requires controlled acceptance of external AI output. |
| `DEC-ARI-001` | Keeps Ariane local navigation independent from optional external voice. |
| `DEC-MEDIATHEQUE-001` | Keeps kOA Mediatheque ingestion and processing deterministic and non-AI. |
| `DEC-UCKK-EXT-001` | Keeps UCKK external and limits integration to explicit governed publication. |

### 9.2 Related ADRs

| ADR | Relevance |
| --- | --- |
| `ADR-002` | Defines immutable signed system-image behavior for applicable sovereign profiles. |
| `ADR-008` | Defines the four release channels. |
| `ADR-013` | Separates global lifecycle semantics from profile-specific implementation. |
| `ADR-014` | Preserves the external AI boundary. |
| `ADR-016` | Keeps generated documentation projections separate from canonical authority. |
| `ADR-019` | Separates resource and governance-policy authority. |
| `ADR-021` | Preserves Ariane local navigation when external voice is absent. |
| `ADR-030` | Establishes the kOA Mediatheque as an internal component. |
| `ADR-031` | Establishes UCKK as an external Moodle publication target. |
| `ADR-023` | Makes overlay effects explicit. |
| `ADR-024` | Preserves logical ownership across physical deployment forms. |
| `ADR-026` | Blocks active artifact authority that depends on missing implementation decisions. |

### 9.3 Prohibited assumptions

The following assumptions are prohibited:

- a filename defines artifact class;
- a version string defines artifact identity;
- a valid signature proves compatibility;
- a published artifact is active;
- an imported bundle authorizes its payloads;
- a Release Set merges the four release channels;
- a transport envelope owns its payload identities;
- a cache is valid recovery retention;
- a build can be reproduced by reusing its version label;
- a rebuilt artifact retains the previous artifact identity;
- one rollback mechanism is safe for every class;
- a service can roll back independently of its data effects;
- an irreversible migration has ordinary rollback;
- Kristal workflow status changes content identity;
- a runtime can compile missing language source silently;
- an Ariane pack can introduce unapproved voice or AI authority;
- an external AI output is an authoritative kOA Mediatheque artifact or an authorized UCKK publication;
- a receipt can activate the state it describes;
- missing evidence can be reconstructed by assertion;
- an artifact class can be created from implementation prevalence;
- a deprecated class identifier can be reused.

## 10. Validation Criteria

This document conforms when all of the following checks pass:

1. metadata status is `active`;
2. the registered path is `06-lifecycle/01-artifact-classes.md`;
3. all identifiers and canonical references resolve;
4. all listed decisions are accepted;
5. all requirements match the requirements registry;
6. all locks exist and pass;
7. every active artifact class has one unique registry entry;
8. every class has an active schema or explicit structural contract;
9. every class defines identity and immutability;
10. every class defines eligible release channels;
11. every class defines permitted lifecycle categories;
12. every class defines applicable states and transitions;
13. every activatable class defines atomic activation or an equivalent no-partial-state transition;
14. every activatable or executable class defines rollback or forward repair;
15. every class defines compatibility dimensions;
16. every release class defines integrity and trust checks;
17. every software-bearing class defines SBOM requirements;
18. every release class defines provenance requirements;
19. every class defines evidence and retention;
20. every artifact instance references one valid class;
21. artifact class and release channel combinations are permitted;
22. immutable artifact identity survives promotion unchanged;
23. rebuild tests produce a distinct artifact identity;
24. publication tests do not change artifact bytes;
25. import and activation remain separate;
26. offline-bundle payloads retain independent identities;
27. Release Set tests cover all referenced channel identities and compatibility;
28. system-image tests cover staging, boot acceptance, rollback, and recovery;
29. service tests cover API, event, schema, migration, health, and rollback or repair;
30. policy tests cover static validation, regression vectors, atomic activation, and receipt lineage;
31. Kristal tests cover lineage, query compatibility, substitution, downgrade, activation, and revocation;
32. language tests cover PGF integrity, runtime compatibility, loading, and rollback;
33. Ariane tests prove local operation without external voice;
34. kOA Mediatheque tests prove local artifacts remain deterministic and non-AI, and UCKK integration tests prove publication is explicit and external;
35. migration tests cover checkpoints, restart, backup, unsupported jumps, and forward repair;
36. trust-update tests cover scope, sequence, replay, revocation, and recovery;
37. evidence receipts cannot mutate described state;
38. retention tests preserve required known-good and recovery material;
39. active content is English;
40. placeholder and unresolved-authority markers are absent.

The validator reports actionable failures, including:

```text
artifact_class_missing
artifact_class_identifier_collision
artifact_class_schema_missing
artifact_class_channel_invalid
artifact_class_identity_undefined
artifact_class_lifecycle_undefined
artifact_class_activation_partial
artifact_class_recovery_undefined
artifact_class_compatibility_undefined
artifact_class_evidence_undefined
artifact_class_retention_undefined
artifact_manifest_class_mismatch
artifact_integrity_failed
artifact_signer_scope_invalid
artifact_compatibility_failed
artifact_revoked
artifact_downgrade_blocked
artifact_import_activation_conflated
artifact_release_set_incompatible
artifact_migration_repair_missing
artifact_receipt_mutation_attempt
```

## 11. Non-Normative Examples

### 11.1 System image

A build farm produces a signed system image with SBOM, provenance, profile compatibility, and a Release Set reference.

A sovereign node imports and stages it. The current boot remains active until an authorized reboot selects the candidate. The node accepts the image only after required health checks pass.

### 11.2 Service artifact with migration

A Konnaxion service artifact requires an additive schema migration.

The migration artifact runs first, records its checkpoint, and preserves compatibility with the old service. The new service activates through blue/green validation. Contract and representative civic-reading tests pass before the old deployment is removed.

### 11.3 Governance policy bundle

A policy bundle contains authorization and disclosure modules, reason codes, obligations, test vectors, approval metadata, and signatures.

The Governance Policy Runtime stages and validates the candidate. Activation changes one policy identity atomically. Existing decision receipts continue to reference the prior identity.

### 11.4 Kristal Runtime Pack

A Runtime Pack is compiled from declared Kristal sources and reader policy.

Its manifest records source lineage, file inventory, query contract, compatibility, and integrity. Kristal Runtime switches the active pack pointer atomically and keeps the previous compatible pack for rollback.

### 11.5 Language pack

GF Wordbench produces a compiled PGF and language runtime pack.

The user runtime verifies the artifact and loads it without grammar compilation. A corrupt pack is rejected, and the last verified compatible language pack remains available.

### 11.6 Ariane artifact

An Ariane artifact updates deterministic menus, command mappings, and accessibility navigation.

The artifact contains no external voice credential or provider authority. Local navigation remains operational when the voice integration is unavailable.

### 11.7 Offline bundle

An offline bundle contains one system image, two service artifacts, one policy bundle, language packs, a Release Set, and revocation material.

The importer verifies the envelope and evaluates every payload separately. One incompatible language pack is rejected while the remaining payloads stay staged and inactive until their own approvals complete.

### 11.8 Release Set

A Release Set references a system image, service release, governance policy bundle, and knowledge defaults that were tested together.

A later knowledge-only update is permitted when its compatibility contract passes against the unchanged system, services, and governance identities.

### 11.9 Irreversible migration

A migration converts encrypted component records to a new non-reversible representation.

The artifact declares the change as irreversible, requires a verified backup, uses checkpoints, and defines forward repair. A failed execution does not claim that rollback restored the prior schema.

### 11.10 Evidence receipt

An activation receipt records candidate identity, prior identity, policy result, compatibility result, actor, time, outcome, and evidence references.

Editing the receipt cannot alter active state. A correction is a new linked evidence record.
