<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-LIFE-003",
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
    "contracts/release-channels.contract.json",
    "schemas/release-channels.contract.schema.json",
    "contracts/artifact-classes.contract.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/integration-types.contract.json",
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
    "DEC-LIFE-CHANNEL-001",
    "DEC-SYS-COMP-001",
    "DEC-SYS-OFFLINE-001",
    "DEC-SYS-AUDIT-001"
  ],
  "requirement_ids": [
    "REQ-LIFE-CHANNEL-001",
    "REQ-LIFE-CHANNEL-002",
    "REQ-LIFE-CHANNEL-003",
    "REQ-LIFE-CHANNEL-004",
    "REQ-LIFE-CHANNEL-005",
    "REQ-LIFE-CHANNEL-006",
    "REQ-LIFE-CHANNEL-007",
    "REQ-LIFE-CHANNEL-008",
    "REQ-LIFE-CHANNEL-009",
    "REQ-LIFE-CHANNEL-010",
    "REQ-LIFE-CHANNEL-011",
    "REQ-LIFE-CHANNEL-012",
    "REQ-LIFE-CHANNEL-013",
    "REQ-LIFE-CHANNEL-014",
    "REQ-LIFE-CHANNEL-015",
    "REQ-LIFE-CHANNEL-016",
    "REQ-LIFE-CHANNEL-017",
    "REQ-LIFE-CHANNEL-018",
    "REQ-LIFE-CHANNEL-019",
    "REQ-LIFE-CHANNEL-020",
    "REQ-LIFE-CHANNEL-021",
    "REQ-LIFE-CHANNEL-022",
    "REQ-LIFE-CHANNEL-023",
    "REQ-LIFE-CHANNEL-024",
    "REQ-LIFE-CHANNEL-025",
    "REQ-LIFE-CHANNEL-026",
    "REQ-LIFE-CHANNEL-027",
    "REQ-LIFE-CHANNEL-028",
    "REQ-LIFE-CHANNEL-029",
    "REQ-LIFE-CHANNEL-030",
    "REQ-LIFE-CHANNEL-031",
    "REQ-LIFE-CHANNEL-032",
    "REQ-LIFE-CHANNEL-033",
    "REQ-LIFE-CHANNEL-034",
    "REQ-LIFE-CHANNEL-035",
    "REQ-LIFE-CHANNEL-036",
    "REQ-LIFE-CHANNEL-037",
    "REQ-LIFE-CHANNEL-038",
    "REQ-LIFE-CHANNEL-039",
    "REQ-LIFE-CHANNEL-040"
  ],
  "lock_ids": [
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
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
    "DOC-COMP-000",
    "DOC-COMP-001",
    "DOC-DEV-000"
  ],
  "tags": [
    "release-channels",
    "release-sets",
    "compatibility",
    "artifact-lifecycle",
    "signing",
    "atomic-activation",
    "rollback",
    "forward-repair",
    "offline-release",
    "conformance"
  ]
}
KOA:DOC-META:END -->

# Release Channels

## 1. Purpose

This document defines the four-channel release model used by kOA.

Release channels separate independently versioned classes of system change while preserving compatibility and atomic authority. The model allows one channel to evolve without forcing artificial version changes in every other channel, but it does not allow channel versions to activate independently as an untested mixture.

The canonical channels are:

```text
system
services
governance
knowledge
```

Every active deployment identifies one complete signed Release Set containing exactly one compatible version of each channel.

The release-channels registry owns channel identities, owners, artifact memberships, compatibility constraints, Release Set policy, and active Release Set records. This document explains those canonical rules and the lifecycle that implements them.

## 2. Scope

This document applies globally to:

- release-channel identity and ownership;
- artifact-class membership;
- channel-version publication;
- cross-channel compatibility;
- Release Set assembly;
- signing and verification;
- online and offline distribution;
- staging;
- activation;
- rollback;
- forward repair;
- revocation;
- supersession;
- archival;
- profile and component conformance claims;
- release tests, evidence, and receipts.

It applies to production, sovereign, development, build, control-plane, and recovery environments according to their profile-specific authority. A development environment can create candidate artifacts, but it cannot claim production channel publication or activation without explicit profile authority.

This document does not define the internal contents of every artifact class, the commercial distribution mechanism, a deployment schedule, or provider-specific packaging. Those concerns remain owned by artifact contracts, profiles, build contracts, integration contracts, and operational procedures.

## 3. Canonical References

Canonical ownership is distributed as follows:

| Subject | Canonical owner |
| --- | --- |
| Channel identities, owners, memberships, compatibility, and Release Sets | `contracts/release-channels.contract.json` |
| Artifact identities and artifact-class lifecycle | `contracts/artifact-classes.contract.json` |
| Active authority and canonical versions | `generated/authority-manifest.json` |
| Accepted release decisions | `generated/decision-index.json` |
| System and capability compatibility | `contracts/system.contract.json` |
| Component identities and contracts | `generated/component-catalog.json` and `contracts/components/*.component.json` |
| Profile release authority and activation constraints | `contracts/profiles/*.profile.json` |
| External and offline distribution boundaries | `contracts/integration-types.contract.json` |
| Requirement statements and strength | `generated/requirements-index.json` |
| Release and lifecycle invariants | `generated/assertion-index.json` |
| Decision, artifact, profile, test, evidence, and receipt links | `generated/traceability.json` |
| Release tests | `generated/test-catalog.json` |
| Release evidence | `generated/evidence-catalog.json` |
| Approved bounded deviations | `generated/exception-index.json` |

The release-channels registry determines membership. A package name, repository location, documentation heading, deployment unit, or implementation convention does not determine its channel.

## 4. Channel Model and Ownership

### 4.1 Channel model

The release model has four properties:

| Property | Meaning |
| --- | --- |
| Exclusive ownership | Every active channel has one canonical owner |
| Exclusive membership | Every active artifact class belongs to one channel |
| Independent versioning | A channel can publish a new version without renumbering unchanged channels |
| Complete activation | Every active state uses one compatible version from all four channels |

Independent versioning is not independent activation.

### 4.2 System channel

The system channel establishes the foundational execution substrate described by its artifact memberships.

Typical responsibilities include:

- boot and recovery artifacts;
- host and node foundations;
- foundational runtime dependencies;
- protected system configuration;
- node-level execution mechanisms;
- system compatibility metadata.

The registry remains the source of the exact artifact list.

### 4.3 Services channel

The services channel carries executable component behavior and service-level runtime artifacts.

Typical responsibilities include:

- component service packages;
- component runtime images;
- service manifests;
- compatible service configuration;
- service migrations;
- interface-compatible runtime assets.

A service package does not gain authority over the component's data or policy merely because it belongs to this channel.

### 4.4 Governance channel

The governance channel carries versioned artifacts that establish or enforce governance and authority.

Typical responsibilities include:

- active authority records;
- registries and schemas;
- accepted decisions;
- policies;
- component and profile contracts;
- lifecycle and compatibility contracts;
- compliance and conformance rules.

Governance artifacts can change how other channel artifacts are admitted or operated. They therefore participate in cross-channel compatibility.

### 4.5 Knowledge channel

The knowledge channel carries versioned knowledge-bearing and knowledge-runtime artifacts.

Typical responsibilities include:

- knowledge packages;
- language and terminology assets;
- controlled content collections;
- kOA Mediatheque artifacts and UCKK publication packages;
- runtime packs;
- indexes or index inputs whose artifact contracts make them distributable;
- other versioned knowledge resources.

Regenerable local caches remain outside release membership unless an artifact contract explicitly makes them distributable release artifacts.

### 4.6 Artifact membership

A channel membership record identifies:

- artifact-class reference;
- active or deprecated membership;
- whether every Release Set requires the class;
- compatibility group;
- explanatory notes.

Membership changes are semantic. Moving an artifact class between channels changes ownership, compatibility, release construction, and recovery behavior.

### 4.7 Channel version

A channel version includes:

```text
channel_id
channel_version
manifest_ref
artifact_refs
owner_ref
status
compatibility_metadata
test_refs
evidence_refs
activation_policy
recovery_policy
```

The manifest binds the complete artifact selection for that version.

A published channel version is immutable. Correction creates a new version or a separately governed revocation record.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-LIFE-CHANNEL-001,REQ-LIFE-CHANNEL-002,REQ-LIFE-CHANNEL-003,REQ-LIFE-CHANNEL-004,REQ-LIFE-CHANNEL-005,REQ-LIFE-CHANNEL-006,REQ-LIFE-CHANNEL-007,REQ-LIFE-CHANNEL-008,REQ-LIFE-CHANNEL-009,REQ-LIFE-CHANNEL-010,REQ-LIFE-CHANNEL-011,REQ-LIFE-CHANNEL-012,REQ-LIFE-CHANNEL-013,REQ-LIFE-CHANNEL-014,REQ-LIFE-CHANNEL-015,REQ-LIFE-CHANNEL-016,REQ-LIFE-CHANNEL-017,REQ-LIFE-CHANNEL-018,REQ-LIFE-CHANNEL-019,REQ-LIFE-CHANNEL-020,REQ-LIFE-CHANNEL-021,REQ-LIFE-CHANNEL-022,REQ-LIFE-CHANNEL-023,REQ-LIFE-CHANNEL-024,REQ-LIFE-CHANNEL-025,REQ-LIFE-CHANNEL-026,REQ-LIFE-CHANNEL-027,REQ-LIFE-CHANNEL-028,REQ-LIFE-CHANNEL-029,REQ-LIFE-CHANNEL-030,REQ-LIFE-CHANNEL-031,REQ-LIFE-CHANNEL-032,REQ-LIFE-CHANNEL-033,REQ-LIFE-CHANNEL-034,REQ-LIFE-CHANNEL-035,REQ-LIFE-CHANNEL-036,REQ-LIFE-CHANNEL-037,REQ-LIFE-CHANNEL-038,REQ-LIFE-CHANNEL-039,REQ-LIFE-CHANNEL-040 -->
- **REQ-LIFE-CHANNEL-001 — SHALL:** The active release model contain exactly four canonical channels identified as system, services, governance, and knowledge.
- **REQ-LIFE-CHANNEL-002 — SHALL NOT:** A fifth channel, alias channel, environment channel, profile channel, or provider-specific channel become active without an accepted owner decision and canonical registry change.
- **REQ-LIFE-CHANNEL-003 — SHALL:** Every active release channel have exactly one canonical owner and one exclusive artifact-class membership definition in the release-channels registry.
- **REQ-LIFE-CHANNEL-004 — SHALL NOT:** An artifact class belong actively to more than one release channel.
- **REQ-LIFE-CHANNEL-005 — SHALL:** The system channel contain artifacts that establish the compatible host, node, foundational runtime, boot, recovery, and system-execution substrate defined by its canonical artifact memberships.
- **REQ-LIFE-CHANNEL-006 — SHALL:** The services channel contain executable component services, service packages, service manifests, and service-level runtime artifacts defined by its canonical artifact memberships.
- **REQ-LIFE-CHANNEL-007 — SHALL:** The governance channel contain versioned governance, policy, authority, contract, schema, decision, and compliance artifacts defined by its canonical artifact memberships.
- **REQ-LIFE-CHANNEL-008 — SHALL:** The knowledge channel contain versioned knowledge, content, language, indexing, runtime-pack, and other knowledge-bearing artifacts defined by its canonical artifact memberships.
- **REQ-LIFE-CHANNEL-009 — SHALL NOT:** Explanatory prose redefine channel membership established by the artifact-classes and release-channels registries.
- **REQ-LIFE-CHANNEL-010 — SHALL:** Every published channel version have a semantic version, manifest, artifact references, owner, status, compatibility metadata, tests, evidence, activation policy, and recovery policy.
- **REQ-LIFE-CHANNEL-011 — SHALL:** Each channel version be immutable after publication except for lifecycle status and separately governed revocation or archival records.
- **REQ-LIFE-CHANNEL-012 — SHALL NOT:** A mutable tag, branch name, directory name, container tag without immutable identity, or deployment label serve as the canonical channel version.
- **REQ-LIFE-CHANNEL-013 — SHALL:** Independent updates to one channel be permitted only when all cross-channel compatibility constraints pass.
- **REQ-LIFE-CHANNEL-014 — SHALL:** An independent channel update produce a new Release Set containing the updated channel version and one explicitly selected compatible version of every other channel.
- **REQ-LIFE-CHANNEL-015 — SHALL NOT:** An independently updated channel activate outside a complete Release Set.
- **REQ-LIFE-CHANNEL-016 — SHALL:** Every Release Set contain exactly one system version, one services version, one governance version, and one knowledge version.
- **REQ-LIFE-CHANNEL-017 — SHALL:** Every Release Set have a stable identity, semantic version, lifecycle status, creation time, compatibility result, tests, evidence, and verified signature.
- **REQ-LIFE-CHANNEL-018 — SHALL:** Release Set lifecycle status use candidate, validated, active, superseded, revoked, or archived.
- **REQ-LIFE-CHANNEL-019 — SHALL NOT:** A candidate, incomplete, incompatible, unsigned, unverified, revoked, or archived Release Set become active.
- **REQ-LIFE-CHANNEL-020 — SHALL:** Compatibility constraints be canonical, directional where required, version-specific, artifact-class-specific, and evaluated at publication, Release Set assembly, activation, rollback, and forward repair as declared.
- **REQ-LIFE-CHANNEL-021 — SHALL:** A failed or indeterminate compatibility result block publication, assembly, activation, rollback, or repair at the applicable enforcement point.
- **REQ-LIFE-CHANNEL-022 — SHALL NOT:** Successful startup, passing smoke checks, semantic-version proximity, newest-version selection, or implementation prevalence substitute for canonical compatibility evidence.
- **REQ-LIFE-CHANNEL-023 — SHALL:** Release Set signing bind the Release Set identity, all four channel versions, manifests, compatibility result, artifact integrity references, tests, evidence, and signing identity.
- **REQ-LIFE-CHANNEL-024 — SHALL:** Signatures and functional artifact-integrity records be verified before activation and again when trust, storage, transfer, or recovery conditions require revalidation.
- **REQ-LIFE-CHANNEL-025 — SHALL NOT:** Ordinary Markdown documentation require file-content hashes as part of release-channel conformance.
- **REQ-LIFE-CHANNEL-026 — SHALL:** Release artifacts, signed manifests, Release Sets, offline bundles, archives, and provenance records use integrity metadata where their functional contracts require it.
- **REQ-LIFE-CHANNEL-027 — SHALL:** Release Set activation be atomic and prevent a partially authoritative combination of channel versions.
- **REQ-LIFE-CHANNEL-028 — SHALL:** All dependent artifacts, contracts, services, policies, and knowledge objects pass pre-activation validation before the active authority reference changes.
- **REQ-LIFE-CHANNEL-029 — SHALL:** The authority index or equivalent active-authority pointer activate last.
- **REQ-LIFE-CHANNEL-030 — SHALL:** Activation produce a durable receipt identifying prior and new Release Sets, all channel versions, actor and authority references, tests, evidence, time, and result.
- **REQ-LIFE-CHANNEL-031 — SHALL NOT:** Staging, download, signature verification, manifest verification, service restart, or artifact copy be reported as completed activation.
- **REQ-LIFE-CHANNEL-032 — SHALL:** Every published channel version and Release Set have a defined rollback, forward-repair, or rollback-or-forward-repair strategy.
- **REQ-LIFE-CHANNEL-033 — SHALL:** Rollback select a complete compatible prior Release Set rather than independently reverting one channel into an unvalidated combination.
- **REQ-LIFE-CHANNEL-034 — SHALL:** Forward repair produce a new complete compatible Release Set and preserve evidence linking the failed and repaired states.
- **REQ-LIFE-CHANNEL-035 — SHALL:** Revocation identify affected channel versions, Release Sets, trust state, activation prohibition, replacement or recovery path, and required operator action.
- **REQ-LIFE-CHANNEL-036 — SHALL:** Offline distribution preserve Release Set identity, all manifests, signatures, artifact-integrity records, compatibility evidence, rollback or repair material, and target-profile constraints.
- **REQ-LIFE-CHANNEL-037 — SHALL:** Profile conformance claims identify the active Release Set and its four channel versions.
- **REQ-LIFE-CHANNEL-038 — SHALL NOT:** A profile, node, service, component, or artifact claim conformance against an unregistered mixture of channel versions.
- **REQ-LIFE-CHANNEL-039 — SHALL:** Release-channel traceability connect decisions, channel owners, artifact classes, compatibility constraints, profiles, component contracts, tests, evidence, activation receipts, revocations, and recovery records.
- **REQ-LIFE-CHANNEL-040 — SHALL:** Release-channel conformance include exact channel count, exclusive membership, immutable versions, complete signed Release Sets, compatibility checks, atomic activation, authority-last sequencing, rollback or repair, offline transfer, profile claims, reference resolution, and absence of prohibited open-state markers.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Compatibility and Release Set Model

### 6.1 Compatibility constraints

A compatibility constraint identifies:

- stable constraint identity;
- source channel and artifact class;
- source version selector;
- target channel and artifact class;
- target version selector;
- enforcement points;
- tests;
- evidence;
- failure result.

Selectors can express equality, inequality, minimum, maximum, compatible version, or bounded version range.

Compatibility can be directional. A services version can require a minimum governance version without the governance version imposing the reverse relation.

### 6.2 Enforcement points

Constraints can be enforced at:

```text
publication
release_set_assembly
activation
rollback
forward_repair
```

A constraint is evaluated at every declared point because trust, revocation, profile, or artifact state can change after initial publication.

### 6.3 Release Set

A Release Set is the canonical compatible unit of activation.

It contains:

```text
release_set_id
version
status
created_at
system_version
services_version
governance_version
knowledge_version
compatibility_result
test_refs
evidence_refs
signature
```

The machine-readable registry represents channel versions as four entries, one for each channel.

### 6.4 Independent channel update

When one channel changes:

1. publish the new candidate channel version;
2. evaluate its compatibility constraints;
3. select compatible versions of the other three channels;
4. assemble a new candidate Release Set;
5. run cross-channel and profile tests;
6. record evidence;
7. sign the complete Release Set;
8. validate it;
9. distribute and activate it through the normal lifecycle.

Unchanged channels keep their versions, but the Release Set identity changes.

### 6.5 Release Set lifecycle

The lifecycle states are:

| State | Meaning |
| --- | --- |
| `candidate` | Assembly exists but has not completed validation |
| `validated` | Compatibility, tests, evidence, and signature verification pass |
| `active` | The Release Set is the authoritative active combination |
| `superseded` | A newer active Release Set replaced it |
| `revoked` | Trust or safety authority prohibits activation or continued use |
| `archived` | Retained for history, evidence, or recovery policy without active eligibility |

A Release Set has one lifecycle state at a time.

### 6.6 Signing

The signature binds:

- Release Set identity and version;
- all four channel identities and versions;
- every channel manifest;
- applicable artifact-integrity records;
- compatibility result;
- tests and evidence;
- signing identity;
- signing time.

Signing authority remains separate from build, publication, approval, and activation authority.

### 6.7 Integrity metadata

Release artifacts use functional integrity metadata according to their artifact contracts.

Permitted uses include:

- signed release manifests;
- artifact digests;
- signed Release Sets;
- offline bundles;
- provenance;
- archives;
- source-corpus freezes;
- cutover manifests.

Ordinary Markdown documentation does not receive a general file-hash requirement.

## 7. Publication, Distribution, and Activation

### 7.1 Channel publication

Channel publication proceeds through:

1. resolve channel ownership;
2. validate artifact-class membership;
3. verify artifact identity and provenance;
4. verify build and signing authority;
5. validate the channel manifest;
6. execute channel tests;
7. record evidence;
8. evaluate publication-time compatibility;
9. publish the immutable channel version;
10. record the publication receipt.

Publication does not activate the channel.

### 7.2 Release Set assembly

Assembly:

1. selects one published or candidate version per channel;
2. verifies all manifests;
3. evaluates every applicable compatibility constraint;
4. evaluates profile constraints;
5. executes Release Set tests;
6. binds evidence;
7. creates the Release Set manifest;
8. obtains the required signature;
9. verifies the signature;
10. enters `validated` after all checks pass.

An incomplete assembly remains `candidate`.

### 7.3 Distribution

Distribution can use:

- controlled online artifact delivery;
- local repository delivery;
- fleet-controlled delivery;
- signed offline-transfer bundle;
- recovery media;
- another registered integration path.

Distribution preserves immutable identities and does not change lifecycle status by itself.

### 7.4 Staging

Staging places all Release Set artifacts in inactive storage.

Staging verifies:

- target profile;
- available storage and resources;
- artifact identity;
- integrity;
- signature;
- compatibility;
- trust and revocation;
- rollback or repair material;
- expected active Release Set.

A staged Release Set remains inactive.

### 7.5 Atomic activation

Activation proceeds through:

```text
requested
identity_and_authority_verified
expected_state_verified
release_set_verified
all_channels_staged
pre_activation_tests_passed
activation_transaction_started
channel_artifacts_committed
authority_pointer_committed
post_activation_tests_passed
receipt_durable
active
```

A failure before the authority pointer commit preserves the prior active Release Set.

A failure after an unknown host effect enters recovery and blocks blind replay.

### 7.6 Authority-last rule

Dependent artifacts, services, policies, contracts, and knowledge objects are staged and verified first.

The active authority index or equivalent pointer changes last. This prevents documents or registries from declaring a state that the node has not completed.

### 7.7 Activation receipt

The receipt records:

- request and transaction identities;
- prior Release Set;
- new Release Set;
- all eight before-and-after channel identity and version values;
- actor, node, profile, and authority references;
- test and evidence references;
- start and finish times;
- result;
- rollback or recovery reference.

The receipt is locally durable before final success is reported.

## 8. Recovery, Revocation, and Offline Operation

### 8.1 Recovery strategy

Each channel and Release Set declares:

```text
rollback
forward_repair
rollback_or_forward_repair
```

The strategy identifies the maximum recovery window where applicable and the required locally or remotely available artifacts.

### 8.2 Rollback

Rollback:

1. identifies the current active Release Set;
2. selects a complete prior compatible Release Set;
3. verifies rollback floor and revocation state;
4. verifies all four channel artifacts;
5. executes rollback tests;
6. activates the prior set atomically;
7. records the rollback receipt;
8. preserves evidence linking the failed and restored states.

Rollback never selects four versions independently at execution time.

### 8.3 Forward repair

Forward repair:

1. records the incompatible or failed state;
2. produces corrected channel versions where needed;
3. selects compatible versions for every channel;
4. assembles a new Release Set;
5. tests, signs, validates, distributes, and activates it;
6. preserves causal evidence.

A forward repair is a new release, not an in-place mutation.

### 8.4 Revocation

Revocation records:

- affected artifact or channel versions;
- affected Release Sets;
- reason and authority;
- effective time;
- trust and activation impact;
- required shutdown, rollback, repair, or isolation action;
- evidence;
- replacement guidance.

A revoked Release Set cannot become active. An active revoked set follows the applicable emergency lifecycle contract.

### 8.5 Supersession and archival

Successful replacement marks the prior active Release Set `superseded`.

Archival preserves:

- manifests;
- signatures;
- compatibility evidence;
- tests;
- activation and recovery receipts;
- required artifacts or retrieval records;
- lifecycle history.

Archival is not active eligibility.

### 8.6 Offline release distribution

An offline release bundle includes:

- Release Set manifest;
- all four channel manifests;
- required artifacts;
- signatures;
- artifact-integrity records;
- compatibility evidence;
- profile and target constraints;
- revocation state;
- rollback or repair material;
- import instructions.

The target quarantines and verifies the bundle before staging.

### 8.7 Offline activation

Offline activation uses the same compatibility, signature, staging, atomicity, authority-last, receipt, and recovery rules as connected activation.

Network absence does not weaken release authority.

## 9. Security, Authority, and Profile Boundaries

### 9.1 Separation of authorities

Release creation and activation can involve distinct authorities:

| Responsibility | Authority |
| --- | --- |
| Source acceptance | Canonical source owner |
| Artifact build | Authorized build environment |
| Artifact identity and class | Artifact contract owner |
| Channel publication | Channel owner |
| Compatibility | Release-channel registry and tests |
| Signing | Registered signing authority |
| Approval | Applicable governance authority |
| Distribution | Registered integration or transfer path |
| Node activation | Authorized lifecycle component such as kOA Node Agent |
| Audit evidence | Audit Broker |
| Resource admission | Resource Governor |

No one responsibility implies all others.

### 9.2 Component boundaries

A services release can update component implementations. It does not change component data ownership unless governance artifacts and accepted decisions explicitly change the architecture.

Governance channel artifacts cannot directly execute host mutation. Node activation uses the registered privileged lifecycle path.

Knowledge artifacts do not become executable authority solely because they are active.

### 9.3 Profiles

Every profile identifies:

- permitted channel sources;
- build and signing trust;
- activation authority;
- update windows;
- offline-transfer support;
- rollback retention;
- evidence requirements;
- prohibited Release Sets or artifact classes.

A development profile can run candidate artifacts. A production claim uses an active compatible Release Set under the profile's authority.

### 9.4 External boundaries

External artifact repositories, build services, signing devices, federation peers, transfer media, and update services are registered integrations.

Transport success does not establish publication, compatibility, signature validity, or activation.

### 9.5 Secrets and signing keys

Signing keys use managed or hardware-backed references.

Private keys and unrestricted credentials remain absent from:

- channel manifests;
- Release Set manifests;
- receipts;
- logs;
- ordinary evidence;
- offline bundle metadata;
- documentation.

Verification material can be distributed according to trust policy.

## 10. Exceptions and Validation

### 10.1 Exceptions

A bounded exception can adjust:

- a compatibility interval;
- a distribution endpoint;
- a test environment;
- an evidence source;
- a recovery window;
- a profile-specific staging limit;
- an implementation adapter.

An exception cannot:

- create another release channel;
- place one active artifact class in two channels;
- activate an incomplete Release Set;
- bypass signature or compatibility;
- permit partial authoritative activation;
- change the authority-last rule;
- permit rollback to an unvalidated mixture;
- remove recovery;
- treat candidate artifacts as production releases;
- require ordinary Markdown hashes;
- support an unqualified conformance claim outside its scope.

### 10.2 Validation criteria

This document is conformant when validation confirms:

1. exactly four active channel identities exist;
2. each channel has one owner;
3. each active artifact class has one channel membership;
4. channel versions are semantically versioned and immutable;
5. manifests and artifact references resolve;
6. independent updates create new Release Sets;
7. every Release Set contains one version per channel;
8. lifecycle states use the canonical vocabulary;
9. compatibility constraints are canonical and pass at every enforcement point;
10. incompatible or indeterminate combinations are blocked;
11. signatures bind the complete Release Set;
12. artifact-integrity records follow artifact contracts;
13. ordinary Markdown hashes are absent as a release requirement;
14. candidate, unsigned, revoked, archived, or incomplete sets cannot activate;
15. staging remains distinct from activation;
16. activation is atomic;
17. authority activates last;
18. activation receipts are durable;
19. every published version has rollback or forward repair;
20. rollback selects a complete prior Release Set;
21. forward repair creates a new complete Release Set;
22. revocation blocks affected activation and defines recovery;
23. offline bundles preserve complete authority and recovery material;
24. profiles identify active Release Set and all four channel versions;
25. all decisions, artifacts, components, profiles, tests, evidence, receipts, and exceptions resolve;
26. no prohibited open-state marker enters active release authority.

The principal validation entry point is:

```bash
python docs/tools/validate_docs.py
```

Supporting checks include:

```text
tools/check_release_sets.py
tools/check_artifact_contracts.py
tools/check_interfile_locks.py
tools/check_component_boundaries.py
tools/check_profile_inheritance.py
tools/check_traceability.py
tools/check_decision_closure.py
tools/check_no_unresolved_state.py
```

A failed release-channel check blocks publication, Release Set validation, activation, rollback, repair, or the affected conformance claim.

## 11. Non-Normative Examples

### 11.1 Services-only change

A services channel update changes one component package. System, governance, and knowledge versions remain unchanged. A new Release Set is still assembled, tested, signed, and activated.

### 11.2 Governance compatibility floor

A new services version requires a governance schema introduced in governance version 3.2.0. A Release Set using governance 3.1.0 is blocked even when the service starts in a local smoke test.

### 11.3 Knowledge update

A new knowledge package is published while system, services, and governance remain unchanged. The new knowledge version enters a new complete Release Set after compatibility tests.

### 11.4 Failed activation

All artifacts stage successfully, but a pre-activation profile test fails. The authority pointer remains on the prior Release Set, and the staged candidate remains inactive.

### 11.5 Rollback

A post-activation service failure requires rollback. The node selects the prior complete Release Set and activates it atomically rather than reverting only the services channel.

### 11.6 Forward repair

A governance artifact is incompatible with one service. A corrected services version and the selected versions of the other channels form a new signed Release Set.

### 11.7 Offline update

A sovereign-offline node receives one signed bundle containing the Release Set, all four channel manifests, artifacts, signatures, compatibility evidence, and rollback material. The node verifies and activates it locally.

### 11.8 Revoked system artifact

A system artifact is revoked. Every Release Set containing that version becomes ineligible for new activation, and active affected nodes follow the registered rollback or repair path.

### 11.9 Candidate artifact

A developer workstation builds a services candidate. It records source, toolchain, lock, tests, evidence, and integrity, but it is not a published channel version or Release Set.

### 11.10 Documentation update

An explanatory Markdown document changes. It remains under the appropriate governance or knowledge artifact process when included by an artifact contract, but it does not receive a general file-content hash requirement.
