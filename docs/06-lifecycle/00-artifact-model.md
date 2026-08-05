<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-LIFE-000",
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
    "contracts/system.contract.json#/release_and_artifact_identity",
    "contracts/system.contract.json#/receipts_and_critical_transitions",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/integration-types.contract.json",
    "contracts/components/identity-and-trust.component.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-REL-001",
    "DEC-LIFE-001",
    "DEC-DATA-001",
    "DEC-PROFILE-001"
  ],
  "requirement_ids": [
    "REQ-LIFE-ART-001",
    "REQ-LIFE-ART-002",
    "REQ-LIFE-ART-003",
    "REQ-LIFE-ART-004",
    "REQ-LIFE-ART-005",
    "REQ-LIFE-ART-006",
    "REQ-LIFE-ART-007",
    "REQ-LIFE-ART-008",
    "REQ-LIFE-ART-009",
    "REQ-LIFE-ART-010",
    "REQ-LIFE-ART-011",
    "REQ-LIFE-ART-012",
    "REQ-LIFE-ART-013",
    "REQ-LIFE-ART-014",
    "REQ-LIFE-ART-015",
    "REQ-LIFE-ART-016",
    "REQ-LIFE-ART-017",
    "REQ-LIFE-ART-018",
    "REQ-LIFE-ART-019",
    "REQ-LIFE-ART-020",
    "REQ-LIFE-ART-021",
    "REQ-LIFE-ART-022",
    "REQ-LIFE-ART-023",
    "REQ-LIFE-ART-024",
    "REQ-LIFE-ART-025",
    "REQ-LIFE-ART-026",
    "REQ-LIFE-ART-027",
    "REQ-LIFE-ART-028"
  ],
  "lock_ids": [
    "LOCK-DOC-002",
    "LOCK-DOC-011",
    "LOCK-DOC-013",
    "LOCK-DOC-019",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-DATA-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-CONST-011",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-007",
    "DOC-SYS-008",
    "DOC-SYS-016",
    "DOC-SYS-017",
    "DOC-SYS-019",
    "DOC-SYS-020",
    "DOC-COMP-IDT-001"
  ],
  "tags": [
    "lifecycle",
    "artifact",
    "artifact-identity",
    "release-channels",
    "release-set",
    "provenance",
    "signing",
    "verification",
    "compatibility",
    "activation",
    "rollback",
    "forward-repair",
    "retention"
  ]
}
KOA:DOC-META:END -->

# Artifact Model

## 1. Purpose

This document defines the global kOA artifact model.

An artifact is a versioned, identifiable, verifiable unit that can be stored, transferred, tested, selected for a release context, staged, activated, superseded, retained, restored, or retired.

The artifact model provides a common lifecycle for:

- system images and system-level runtime material;
- component and service artifacts;
- governance policy bundles;
- Kristal artifacts;
- PGF artifacts;
- Atlases;
- language runtime packs;
- approved knowledge packages;
- Ariane runtime material;
- kOA Mediatheque packages, optional outbound UCKK publication packages, and inbound UCKK learning packages for quarantine and explicit local acceptance;
- offline bundles;
- release manifests;
- migration packages;
- provenance, SBOM, signature, receipt, and verification evidence.

Not every lifecycle object is itself a release-channel artifact. A Release Set binds channel versions. An offline bundle transports selected artifacts and trust context. A receipt records a transition. A provenance statement explains origin. These objects support the release lifecycle without becoming extra release channels.

The model separates five concepts:

`text
artifact identity
artifact bytes and manifest
release-channel membership
compatibility context
deployment activation state
`

An artifact can exist and verify successfully without being active anywhere. The same immutable artifact can be active in one deployment, staged in another, rejected in a third, and retained only for rollback in a fourth.

## 2. Scope

This document applies globally to:

- artifact production;
- artifact identity;
- artifact classes;
- manifests and payloads;
- content-integrity evidence;
- signatures and trust;
- provenance and SBOMs;
- release-channel assignment;
- Release Sets;
- compatibility declarations;
- artifact storage and caches;
- connected and offline transfer;
- staging;
- activation;
- rollback;
- forward repair;
- migration;
- supersession;
- deprecation;
- quarantine;
- revocation;
- retention;
- recovery;
- disposal;
- lifecycle receipts and evidence.

It applies across all profiles and overlays.

This document does not define the complete payload schema of every artifact class. Those structures belong to `contracts/artifact-classes.contract.json` and the corresponding artifact contracts.

It does not define one packaging technology, repository product, operating-system image format, container format, compression format, signature implementation, deployment orchestrator, or storage engine. Profiles, artifact-class contracts, toolchain contracts, and recipes own those implementation choices where necessary.

## 3. Canonical References

The canonical sources for this document are:

`text
generated/authority-manifest.json
generated/decision-index.json
contracts/system.contract.json#/release_and_artifact_identity
contracts/system.contract.json#/receipts_and_critical_transitions
contracts/release-channels.contract.json
contracts/artifact-classes.contract.json
generated/component-catalog.json
generated/profile-catalog.json
contracts/integration-types.contract.json
contracts/components/identity-and-trust.component.json
generated/requirements-index.json
generated/assertion-index.json
generated/traceability.json
generated/test-catalog.json
generated/evidence-catalog.json
generated/exception-index.json
`

Their ownership roles are:

| Canonical source | Ownership |
| --- | --- |
| `release-channels.registry.json` | The four canonical release channels and their membership rules |
| `artifact-classes.registry.json` | Artifact classes, payload contracts, lifecycle, verification, recovery, and retention behavior |
| `system.registry.json#/release_and_artifact_identity` | Global artifact identity, Release Set, compatibility, and activation model |
| `system.registry.json#/receipts_and_critical_transitions` | Lifecycle receipt and commit semantics |
| `components.registry.json` | Component ownership of produced or consumed artifacts |
| Profile contracts | Profile applicability, packaging constraints, offline behavior, assurance, and capacity |
| `integrations.registry.json` | External artifact source, destination, transfer, and trust boundaries |
| `identity-and-trust.component.json` | Signer identity, signature verification, scoped trust roots, and revocation |
| `requirements.registry.json` | Normative artifact requirements |
| `locks.registry.json` | Release, activation, rollback, data, profile, and identifier invariants |
| `traceability.registry.json` | Artifact-to-decision, requirement, test, evidence, profile, and component links |
| `test-catalog.registry.json` | Executable artifact and release validation |
| `evidence.registry.json` | Build, test, provenance, signature, compatibility, activation, and recovery evidence |
| `exceptions.registry.json` | Bounded deviations that cannot create missing trust, compatibility, or authority |

This document explains the model. It does not independently own the active artifact-class catalog or release-channel membership.

## 4. Model and Responsibilities

### 4.1 Artifact identity

A canonical artifact identity contains at least:

`text
artifact_id
artifact_class
artifact_version
release_channel
producer_identity
produced_at
content_digest
manifest_identity
provenance_reference
compatibility_declaration
`

Artifact-class contracts can require additional identity dimensions.

The canonical identity is independent from:

- repository path;
- object-store location;
- download URL;
- filename;
- container tag;
- mutable branch name;
- cache key;
- deployment-local alias;
- user-facing display name.

A content digest contributes integrity evidence. It is not a human-readable substitute for artifact class and version.

### 4.2 Artifact structure

An artifact logically consists of:

`text
manifest
payload
integrity evidence
provenance
compatibility declaration
class-required evidence
optional signatures
`

The manifest describes the artifact rather than relying on its filename or storage location.

The payload can contain one file, many files, an image, a package, a policy bundle, compiled language material, knowledge material, migration logic, or another class-defined structure.

### 4.3 Artifact classes

An artifact class defines:

- purpose;
- canonical owner;
- release channel;
- manifest schema;
- payload structure;
- identity and version rules;
- producer eligibility;
- required signatures;
- trust scope;
- compatibility dimensions;
- profile applicability;
- verification procedure;
- staging behavior;
- activation boundary;
- rollback behavior;
- forward-repair behavior;
- migration behavior;
- receipt requirements;
- retention and deletion;
- conformance evidence.

Examples of lifecycle roles include:

| Lifecycle role | Examples |
| --- | --- |
| System | Operating-system image, node runtime, system-level shell or boot material |
| Service | Component package, service bundle, container image, service migration package |
| Governance | Governance policy bundle, consent or disclosure policy package |
| Knowledge | Kristal artifact, PGF artifact, Atlas, language runtime pack, approved knowledge package |
| Lifecycle container | Release Set, offline bundle, recovery package |
| Evidence | SBOM, provenance statement, verification receipt, publication receipt |

The registry owns the exact active catalog and its mapping.

### 4.4 Release channels

The canonical release channels are:

`text
system
services
governance
knowledge
`

The channels are independent version domains with declared compatibility relationships.

The knowledge channel contains:

- Kristal artifacts;
- PGF artifacts;
- Atlases;
- language runtime packs;
- approved knowledge packages.

An offline bundle is a transport and activation container, not a fifth channel. A Release Set is a compatibility binding, not a fifth channel.

### 4.5 Release Set

A Release Set identifies the tested compatible versions selected across all four channels.

Its logical content includes:

`text
release_set_id
release_set_version
system_channel_selection
services_channel_selection
governance_channel_selection
knowledge_channel_selection
compatibility_constraints
target_profiles
verification_evidence
test_evidence
signer_identity
signature
validity
`

The effective active channel vector of a deployment resolves to one Release Set context.

An independent channel update changes that vector only after compatibility validation. The unchanged channel selections remain explicit rather than assumed.

### 4.6 Artifact and activation separation

Artifact lifecycle and deployment lifecycle are separate.

Artifact state describes the object itself:

`text
available
quarantined
verified
rejected
superseded
retired
revoked
`

Deployment activation state describes use at a target:

`text
not_present
cached
staged
activation_pending
active
rollback_available
failed
recovery_required
`

An immutable artifact can have different activation states across deployments.

### 4.7 Production and activation authority

Artifact producers can include:

- approved developer publication workflows;
- build farms;
- governance policy publication workflows;
- knowledge publication workflows;
- approved external import workflows;
- recovery tooling.

Production authority does not imply deployment activation authority.

The build farm can produce and sign a service artifact. A sovereign hub can verify and distribute it. A node lifecycle service can activate it. Each retains its own authority boundary and receipt.

### 4.8 Verification dimensions

Verification can include:

| Dimension | Question |
| --- | --- |
| Structure | Does the manifest and payload match the artifact contract? |
| Identity | Is the artifact identity complete and internally consistent? |
| Integrity | Do the bytes match the declared digest and manifest? |
| Signature | Is the required signature valid? |
| Trust | Is the signer trusted for this channel, class, environment, tenant, and purpose? |
| Provenance | Is the production origin and transformation history acceptable? |
| SBOM | Are declared components and dependencies present and acceptable? |
| Compatibility | Can the artifact coexist with the selected channel versions and target state? |
| Profile | Is the artifact applicable to the target profile and overlays? |
| Evidence | Are required tests, attestations, migrations, and approvals present? |
| Revocation | Has the signer, key, issuer, artifact, or release context been revoked? |

A positive result in one dimension does not fill a missing result in another.

### 4.9 Compatibility model

Compatibility dimensions can include:

- required system version;
- required service API version;
- required governance schema;
- required knowledge format;
- component contract version;
- database or storage schema;
- migration version;
- profile and overlay;
- processor architecture;
- operating-system family where relevant;
- runtime or package ABI;
- feature and capability identifiers;
- trust-root generation;
- minimum and maximum dependency versions;
- mutually exclusive artifacts;
- required co-activation.

Compatibility is explicit, machine-readable, and testable.

### 4.10 Provenance, SBOM, and signing

Provenance identifies:

- source repository or canonical source;
- source revision;
- toolchain identity;
- build environment;
- build invocation;
- dependency inputs;
- producer;
- transformations;
- test evidence;
- publication event.

An SBOM identifies the software or package contents required by the artifact class.

Signatures bind the artifact or release object to a signer identity and trust scope. Identity and Trust verifies that binding. Signature success does not make the artifact compatible or authorized for activation.

Cryptographic digests and signatures are appropriate here because release artifacts, signed bundles, provenance, supply-chain material, and content-integrity contracts require them. Ordinary Markdown documentation does not inherit that requirement.

### 4.11 Storage, caches, and mirrors

An artifact can be copied among:

- build output storage;
- quarantine;
- artifact repositories;
- caches;
- mirrors;
- sovereign hubs;
- nodes;
- offline media;
- recovery storage.

Each copy preserves the same canonical artifact identity and verifies against the same integrity evidence.

A cache can remove an unneeded copy without retiring the canonical artifact. A mirror can hold the artifact without becoming its producer or activation authority.

### 4.12 Offline bundles

An offline bundle can contain:

- a Release Set;
- selected channel artifacts;
- manifests;
- signatures;
- trust and revocation updates;
- compatibility declarations;
- target-profile constraints;
- migrations;
- application order;
- rollback or recovery material;
- receipts and evidence templates.

The bundle declares sequence, validity, source authority, destination profile, and rollback protection. Its presence does not permit automatic application.

### 4.13 Migration model

An artifact can require:

- configuration migration;
- data migration;
- schema migration;
- index migration;
- trust-store migration;
- policy migration;
- content-model migration.

Migration logic is versioned and bound to the artifact or release transition.

Artifact rollback and data rollback remain distinct. Some data migrations use forward repair rather than destructive reversal. The artifact-class contract declares the valid behavior.

### 4.14 Retention and disposal

Retention considers:

- active artifacts;
- rollback targets;
- recovery artifacts;
- superseded but supported versions;
- legal holds;
- audit and provenance evidence;
- SBOMs;
- signatures;
- receipts;
- migration inputs;
- deprecation windows;
- offline-distribution obligations.

Retirement removes an artifact from supported use. It does not permit identifier reuse or erase required history.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-LIFE-ART-001,REQ-LIFE-ART-002,REQ-LIFE-ART-003,REQ-LIFE-ART-004,REQ-LIFE-ART-005,REQ-LIFE-ART-006,REQ-LIFE-ART-007,REQ-LIFE-ART-008,REQ-LIFE-ART-009,REQ-LIFE-ART-010,REQ-LIFE-ART-011,REQ-LIFE-ART-012,REQ-LIFE-ART-013,REQ-LIFE-ART-014,REQ-LIFE-ART-015,REQ-LIFE-ART-016,REQ-LIFE-ART-017,REQ-LIFE-ART-018,REQ-LIFE-ART-019,REQ-LIFE-ART-020,REQ-LIFE-ART-021,REQ-LIFE-ART-022,REQ-LIFE-ART-023,REQ-LIFE-ART-024,REQ-LIFE-ART-025,REQ-LIFE-ART-026,REQ-LIFE-ART-027,REQ-LIFE-ART-028 -->
- **REQ-LIFE-ART-001 — SHALL:** Every releasable artifact have a stable artifact identity, canonical artifact class, version, release channel, producer identity, production timestamp, content-integrity digest, provenance reference, and compatibility declaration.
- **REQ-LIFE-ART-002 — SHALL:** Published artifact content be immutable for a given artifact identity and version.
- **REQ-LIFE-ART-003 — SHALL NOT:** A mutable path, filename, repository tag, container tag, cache key, download URL, display name, or deployment-local alias serve as the sole canonical artifact identity.
- **REQ-LIFE-ART-004 — SHALL:** Every releasable artifact map to exactly one canonical release channel: system, services, governance, or knowledge.
- **REQ-LIFE-ART-005 — SHALL NOT:** A Release Set, offline bundle, receipt, provenance statement, SBOM, signature, or transfer package create an additional release channel.
- **REQ-LIFE-ART-006 — SHALL:** A signed Release Set identify tested compatible versions across the system, services, governance, and knowledge channels.
- **REQ-LIFE-ART-007 — SHALL:** An independent channel update preserve all declared compatibility constraints and produce a new effective channel-version vector before activation.
- **REQ-LIFE-ART-008 — SHALL:** Artifact verification cover schema, identity, class, channel, version, digest, signature where required, signer trust, provenance, compatibility, profile applicability, and required evidence.
- **REQ-LIFE-ART-009 — SHALL NOT:** Successful integrity or signature verification alone imply compatibility, authorization, installation, publication, or activation.
- **REQ-LIFE-ART-010 — SHALL:** Artifact trust roots be resolved through Identity and Trust under the exact tenant, environment, release channel, artifact class, component, and intended-use scope.
- **REQ-LIFE-ART-011 — SHALL:** Every artifact class define its payload contract, manifest contract, identity rules, verification rules, activation boundary, rollback or forward-repair behavior, retention behavior, and conformance evidence.
- **REQ-LIFE-ART-012 — SHALL:** Artifact storage, caching, replication, mirroring, transport, and physical relocation preserve the canonical artifact identity and integrity evidence.
- **REQ-LIFE-ART-013 — SHALL NOT:** Possession, download, caching, staging, or verification of an artifact make it active.
- **REQ-LIFE-ART-014 — SHALL:** Artifact activation be an explicit deployment-scoped critical transition with target scope, authority, compatibility result, prior active state, commit result, and receipt.
- **REQ-LIFE-ART-015 — SHALL:** Published artifacts activate without partial authoritative state.
- **REQ-LIFE-ART-016 — SHALL:** A failed activation preserve the last valid authoritative state or enter a declared recovery state without reporting the new artifact as active.
- **REQ-LIFE-ART-017 — SHALL:** Every artifact class define a tested rollback path, a tested forward-repair path, or an explicit reason that only one of those recovery mechanisms is valid.
- **REQ-LIFE-ART-018 — SHALL:** Artifact rollback remain distinct from authoritative data rollback, and data restoration or migration reversal follow the owning data contract.
- **REQ-LIFE-ART-019 — SHALL:** Data, schema, index, trust, and policy migrations associated with an artifact be versioned, deterministic where applicable, compatibility-checked, evidenced, and bound to activation and recovery behavior.
- **REQ-LIFE-ART-020 — SHALL:** SBOM, provenance, signing, build, test, compatibility, migration, and release evidence remain linked to the artifact identity and version they describe.
- **REQ-LIFE-ART-021 — SHALL:** Artifact production from development or build-farm environments be separated from deployment activation authority.
- **REQ-LIFE-ART-022 — SHALL NOT:** An external AI output become a trusted or active artifact merely because an approved external surface produced it.
- **REQ-LIFE-ART-023 — SHALL:** External or candidate content enter the applicable controlled import, provenance, review, acceptance, verification, and artifact-publication workflow before authoritative use.
- **REQ-LIFE-ART-024 — SHALL:** Offline bundles identify contained artifact identities, Release Set context, trust material, compatibility constraints, validity, sequence, intended profiles, and application receipts.
- **REQ-LIFE-ART-025 — SHALL:** Artifact retention preserve required rollback targets, recovery inputs, active-version evidence, receipts, provenance, legal holds, and permanently reserved identifiers.
- **REQ-LIFE-ART-026 — SHALL:** Artifact supersession, deprecation, retirement, revocation, quarantine, and rejection remain explicit lifecycle states or dispositions with stable reason codes.
- **REQ-LIFE-ART-027 — SHALL:** Artifact lifecycle status exposed to users and operators distinguish available, verified, staged, active, superseded, retired, quarantined, rejected, failed, and recovery-required conditions truthfully.
- **REQ-LIFE-ART-028 — SHALL:** Profile-specific packaging, signing, storage, container, operating-system, orchestration, offline, and assurance requirements remain explicit and cannot become global artifact requirements through repetition.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Artifact production

Artifact production follows this sequence:

1. resolve the artifact class and release channel;
2. verify producer eligibility;
3. select canonical source and toolchain inputs;
4. build or assemble the payload in the declared environment;
5. create the manifest and compatibility declaration;
6. compute content-integrity evidence;
7. create provenance and SBOM material where required;
8. run class-required validation;
9. sign the artifact where required;
10. publish the immutable artifact identity and bytes;
11. record publication evidence.

A failed production attempt does not publish a new artifact version.

### 6.2 Import and quarantine

Imported material:

1. enters a declared import boundary;
2. receives transfer provenance;
3. remains quarantined;
4. is parsed using the expected artifact contract;
5. is verified for identity, integrity, signature, trust, compatibility, and evidence;
6. is accepted into artifact storage or rejected;
7. records the result.

External AI output remains candidate input until the applicable owning workflow accepts it and publishes a valid artifact.

### 6.3 Verification

Verification follows this sequence:

1. resolve the exact artifact identity;
2. load the active artifact-class contract;
3. validate manifest and payload structure;
4. validate digest and content integrity;
5. validate signer and scoped trust where required;
6. evaluate revocation;
7. validate provenance and SBOM requirements;
8. evaluate target profile and channel compatibility;
9. validate required tests, migrations, and evidence;
10. produce a verification receipt.

Verification does not activate the artifact.

### 6.4 Release Set construction

Release Set construction:

1. selects versions for all four channels;
2. resolves every declared cross-channel constraint;
3. runs compatibility and profile matrices;
4. binds required migrations and activation order;
5. includes rollback and repair context;
6. records test and evidence references;
7. signs the Release Set;
8. publishes the immutable Release Set identity.

### 6.5 Staging

Staging:

1. identifies the target deployment scope;
2. verifies the artifact or Release Set;
3. confirms available storage and resources;
4. transfers immutable bytes;
5. verifies the staged copy;
6. prepares but does not commit configuration and migration work;
7. records staged state;
8. leaves the active state unchanged.

### 6.6 Activation

Activation:

1. identifies target, actor, authority, profile, and current active state;
2. resolves the effective Release Set;
3. reevaluates trust, revocation, compatibility, and evidence;
4. creates a backup or checkpoint where required;
5. prepares migrations and dependent services;
6. enters the class-defined atomic commit boundary;
7. commits the new authoritative state;
8. validates health, readiness, data, and compatibility;
9. records the activation receipt;
10. retains the declared rollback or repair state.

Only the successful commit changes active identity.

### 6.7 Failed activation

When activation cannot complete:

1. stop further commit work;
2. preserve evidence;
3. determine whether authoritative state changed;
4. leave the prior valid state active when commit did not occur;
5. roll back when the class permits safe rollback;
6. enter forward repair when reversal is unsafe or invalid;
7. enter recovery when neither ordinary path can complete;
8. record the actual result;
9. avoid reporting the new artifact as active.

### 6.8 Rollback

Rollback:

1. identifies the last valid activation state;
2. validates the retained artifact and recovery material;
3. evaluates data and schema compatibility;
4. stops or isolates the failed version;
5. restores the prior executable or policy state;
6. performs only the data actions permitted by the owning data contract;
7. validates the restored state;
8. commits the rollback atomically;
9. records the rollback receipt.

### 6.9 Forward repair

Forward repair:

1. preserves the current evidence and state;
2. selects an approved repair artifact, migration, or configuration;
3. verifies compatibility and authority;
4. applies the bounded repair;
5. validates resulting state;
6. commits the repaired state;
7. records the repair and its relationship to the failed transition.

Forward repair is not an undocumented manual mutation.

### 6.10 Independent channel update

An independent channel update:

1. identifies the channel and proposed artifact versions;
2. retains explicit selections for the other three channels;
3. evaluates all cross-channel constraints;
4. runs the affected compatibility and conformance tests;
5. produces a new effective channel vector;
6. stages and activates under the normal lifecycle;
7. records the resulting Release Set context.

### 6.11 Supersession and retirement

Supersession or retirement:

1. identifies replacement and compatibility window;
2. updates supported-version policy;
3. prevents new activation where required;
4. preserves active deployments until migration policy applies;
5. retains rollback and recovery material;
6. records deprecation, revocation, retirement, or rejection reason;
7. eventually removes unneeded physical copies;
8. preserves identifiers and required evidence permanently.

## 7. Failure States and Safe Degradation

| Failure code | Condition | Protected result | Safe degraded result |
| --- | --- | --- | --- |
| `artifact_identity_incomplete` | Required identity fields are absent or inconsistent | Artifact is rejected | Current active version remains |
| `artifact_class_unknown` | Artifact class is not active or registered | Artifact is quarantined | No activation |
| `artifact_channel_invalid` | Class and release channel disagree | Artifact is rejected | Existing channel selection remains |
| `artifact_manifest_invalid` | Manifest does not match the class contract | Artifact is rejected | Preserve evidence for diagnosis |
| `artifact_integrity_failed` | Payload or manifest digest does not match | Artifact is rejected and quarantined | Current valid artifact remains |
| `artifact_signature_invalid` | Required signature does not validate | Artifact is rejected | Current trusted version remains |
| `artifact_signer_untrusted` | Signer lacks trust for exact class, channel, environment, or purpose | Artifact is rejected | Resolve the correct trust context |
| `artifact_revoked` | Artifact, signer, key, issuer, or release context is revoked | New use and activation are denied | Previously active state follows incident and recovery policy |
| `artifact_provenance_incomplete` | Required production lineage is missing | Artifact cannot support release | Rebuild through an approved workflow |
| `artifact_sbom_incomplete` | Required SBOM evidence is missing or inconsistent | Artifact cannot support release | Current valid version remains |
| `artifact_compatibility_failed` | Target profile or channel vector is incompatible | Staging or activation is denied | Existing compatible Release Set remains |
| `artifact_evidence_incomplete` | Required tests, attestations, or approvals are absent | Release or activation claim is blocked | Complete evidence |
| `artifact_staging_partial` | Staged copy is incomplete or unverifiable | Staged state is discarded or repaired | Active state remains unchanged |
| `artifact_activation_partial` | Commit cannot complete atomically | Partial state remains non-authoritative | Rollback, forward repair, or recovery |
| `artifact_rollback_invalid` | Prior executable state is incompatible with current data or schema | Rollback is denied | Use declared forward repair |
| `artifact_forward_repair_unavailable` | Required repair artifact or procedure is unavailable | Recovery state remains active | Preserve evidence and current protected state |
| `artifact_migration_failed` | Migration cannot complete or validate | New artifact remains inactive | Restore checkpoint, roll back, or repair |
| `artifact_release_set_incomplete` | One or more channel selections are unresolved | Release Set is rejected | Use previous valid Release Set |
| `artifact_offline_bundle_invalid` | Bundle signature, sequence, scope, validity, or compatibility fails | Bundle remains inactive | Previous trusted state remains |
| `artifact_receipt_missing` | Critical lifecycle transition lacks required receipt | Activation or conformance claim is blocked | Reconstruct only through approved recovery |
| `artifact_retention_violation` | Required rollback, recovery, hold, or evidence object would be deleted | Deletion is blocked | Retain until policy permits |
| `artifact_state_mismatch` | Reported activation state differs from authoritative state | Status is invalid | Reconcile from owning lifecycle state |

Failure of a proposed artifact does not invalidate the currently active artifact merely because both belong to the same class.

## 8. Cross-Component Interactions

### 8.1 Identity and Trust

Identity and Trust verifies signer identity, signatures, trust roots, revocation, and intended-use scope.

It does not decide artifact compatibility or activation.

### 8.2 Build farm and developer publication

Developer and build-farm workflows produce candidate release artifacts and evidence.

Production does not grant deployment authority. Build workers remain reproducible and isolated according to their profiles.

### 8.3 Lifecycle services and node agents

Lifecycle services or node agents verify, stage, activate, roll back, repair, restore, and report artifacts for their target scope.

They record the actual active artifact identity and Release Set context.

### 8.4 Governance Policy Runtime

Governance policy bundles belong to the governance channel.

The policy runtime validates applicable policy semantics and activates bundles atomically under the governance artifact contract. Resource Governor remains separate.

### 8.5 Knowledge components

Kristal, PGF, Atlases, language runtime packs, and approved knowledge packages belong to the knowledge channel.

The owning component validates semantic or runtime suitability in addition to generic artifact verification.

### 8.6 kOA and UCKK Mediatheque interchange

The kOA Mediatheque can store, export, import, back up, or restore class-approved local content packages. UCKK receives only explicitly authorized publication packages through the outbound bridge. The kOA Mediatheque can also accept selected UCKK learning packages through the separate import contract after quarantine and validation.

A kOA Mediatheque object identity does not replace release-artifact identity or an UCKK source identity. Imported content receives separate local identities. External Suno or Gamma results remain candidates until accepted into the kOA Mediatheque; publication to UCKK and import from UCKK remain separate governed operations.

### 8.7 Publication Gateway

Publication Gateway controls disclosure and external audience release.

Artifact publication into a repository or release channel does not automatically authorize public disclosure of protected content.

### 8.8 Resource Governor

Resource Governor admits build, verification, transfer, staging, migration, activation, rollback, and recovery workloads under bounded resources.

Capacity does not create lifecycle authority.

### 8.9 Audit Broker

Artifact and lifecycle owners produce verification, activation, rollback, repair, migration, transfer, and recovery receipts.

Audit Broker stores and serves receipts without owning artifact identity or activation state.

### 8.10 Profiles and overlays

Profiles select applicable artifacts, packaging constraints, capacity, operating-system families, storage, offline behavior, and assurance requirements.

Overlays can strengthen signing, evidence, offline, or recovery rules without silently changing artifact class or release channel.

## 9. Decision Closure and Prohibited Assumptions

This document closes the global artifact interpretation as follows:

- every releasable artifact has a stable identity;
- artifact bytes are immutable for a published identity and version;
- paths, tags, filenames, and URLs are locators or aliases;
- every releasable artifact belongs to one of four channels;
- Release Sets bind tested versions across all four channels;
- independent updates preserve explicit cross-channel compatibility;
- verification and activation are separate;
- signatures and integrity do not imply compatibility or authorization;
- activation is deployment-scoped and atomic;
- failed activation preserves the last valid state or enters recovery;
- every artifact class defines rollback or forward repair;
- artifact rollback and data rollback are separate;
- production and activation authorities are separate;
- external AI outputs remain candidate inputs;
- offline bundles are controlled containers rather than release channels;
- retention preserves rollback, recovery, provenance, receipts, and identifiers.

The following assumptions are prohibited:

- a filename is sufficient artifact identity;
- a mutable container tag is immutable provenance;
- a downloaded artifact is installed;
- a verified artifact is active;
- a valid signature proves compatibility;
- a cache or mirror becomes the producer;
- one successful test makes an artifact valid for every profile;
- release channels can be merged for convenience;
- an offline bundle is a fifth release channel;
- independent channel updates can ignore unchanged channel versions;
- activation can expose a partial authoritative state;
- executable rollback permits arbitrary database rollback;
- a migration script can be unversioned;
- an external AI output is a trusted artifact automatically;
- artifact retirement permits identifier reuse;
- deleting a cached copy retires the canonical artifact;
- ordinary Markdown documentation requires release-artifact hashes;
- profile-specific packaging or orchestration is a global requirement.

A new release channel, global artifact identity field, lifecycle state, compatibility dimension, or cross-class activation semantic requires an accepted owner decision and full impact validation.

## 10. Validation Criteria

This document is conformant when all of the following checks pass:

1. the metadata block is first, valid, and declares status `active`;
2. the document contains the required 11 normative sections;
3. all 28 requirement identifiers are unique and registered;
4. every declared decision is accepted;
5. every declared lock exists and is active;
6. the release-channel registry defines exactly `system`, `services`, `governance`, and `knowledge`;
7. every active releasable artifact class maps to exactly one release channel;
8. every artifact class defines manifest, payload, identity, verification, compatibility, activation, recovery, retention, and evidence behavior;
9. artifact identity tests reject identity based only on path, filename, URL, mutable tag, or cache key;
10. immutability tests detect changed content under an existing identity and version;
11. integrity tests verify manifest and payload digests;
12. signature tests use exact scoped trust and revocation state;
13. tests prove that signature success does not imply compatibility or activation;
14. provenance and SBOM tests link evidence to exact artifact identity and version;
15. Release Set tests bind explicit selections for all four channels;
16. independent-channel tests validate every affected cross-channel constraint;
17. profile tests reject inapplicable artifacts;
18. staging tests prove that active state remains unchanged;
19. activation tests prove atomic commit and truthful active identity;
20. failure tests prove preservation of the previous valid state;
21. rollback tests validate executable state and owning data-contract behavior;
22. forward-repair tests validate approved repair identity, authority, and result;
23. migration tests cover versioning, determinism where applicable, checkpoint, compatibility, and recovery;
24. offline-bundle tests cover signature, sequence, scope, validity, profile, compatibility, and rollback protection;
25. external-candidate tests cover controlled import, provenance, review, acceptance, and publication;
26. retention tests preserve rollback, recovery, holds, provenance, receipts, and reserved identifiers;
27. lifecycle-status tests distinguish artifact state from deployment activation state;
28. receipts cover verification, activation, rollback, repair, migration, restore, supersession, and retirement;
29. implementation choices remain within artifact classes, profiles, toolchains, or recipes;
30. no unresolved-authority marker, duplicate identifier, or unregistered normative statement exists;
31. active prose is English;
32. ordinary Markdown validation does not depend on file-content hashes.

Expected validator failure codes include:

`text
artifact_identity_incomplete
artifact_class_unknown
artifact_channel_invalid
artifact_manifest_invalid
artifact_integrity_failed
artifact_signature_invalid
artifact_signer_untrusted
artifact_revoked
artifact_provenance_incomplete
artifact_sbom_incomplete
artifact_compatibility_failed
artifact_evidence_incomplete
artifact_staging_partial
artifact_activation_partial
artifact_rollback_invalid
artifact_forward_repair_unavailable
artifact_migration_failed
artifact_release_set_incomplete
artifact_offline_bundle_invalid
artifact_receipt_missing
artifact_retention_violation
artifact_state_mismatch
`

## 11. Non-Normative Examples

### 11.1 Verified but inactive service artifact

A build farm produces and signs a service artifact. A sovereign hub verifies its identity, digest, signature, provenance, SBOM, and Release Set compatibility. The artifact remains staged until the node lifecycle service commits activation.

### 11.2 Independent knowledge update

A new language runtime pack changes only the knowledge channel. The release process retains the active system, services, and governance selections explicitly, validates all affected compatibility constraints, and creates a new effective Release Set context.

### 11.3 Failed migration

A service artifact requires a schema migration. The executable payload verifies, but migration validation fails before commit. The new artifact remains inactive and the prior service version continues.

### 11.4 Forward repair instead of data rollback

A service activation commits a non-reversible data transformation but fails a later readiness check. The artifact contract prohibits destructive data rollback. The lifecycle service activates an approved repair artifact and records forward-repair evidence.

### 11.5 Offline Release Set

A sovereign node receives a signed offline bundle containing a Release Set, channel artifacts, trust updates, migrations, compatibility evidence, and rollback material. The node verifies the bundle and stages it, but activation still requires a local authority decision and atomic commit.
