<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-DEV-015",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "development",
  "scope": [
    "development_toolchain:artifact_publication",
    "release_channel:system",
    "release_channel:services",
    "release_channel:governance",
    "release_channel:knowledge"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json",
    "contracts/artifact-classes.contract.json",
    "contracts/release-channels.contract.json",
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
    "DEC-LIFE-001",
    "DEC-REL-001",
    "DEC-ART-001",
    "DEC-AUTH-001",
    "DEC-IDENT-001",
    "DEC-COMP-001",
    "DEC-DATA-001",
    "DEC-AI-001",
    "DEC-DEV-001"
  ],
  "requirement_ids": [
    "REQ-DEV-ARTPUB-001",
    "REQ-DEV-ARTPUB-002",
    "REQ-DEV-ARTPUB-003",
    "REQ-DEV-ARTPUB-004",
    "REQ-DEV-ARTPUB-005",
    "REQ-DEV-ARTPUB-006",
    "REQ-DEV-ARTPUB-007",
    "REQ-DEV-ARTPUB-008",
    "REQ-DEV-ARTPUB-009",
    "REQ-DEV-ARTPUB-010",
    "REQ-DEV-ARTPUB-011",
    "REQ-DEV-ARTPUB-012",
    "REQ-DEV-ARTPUB-013",
    "REQ-DEV-ARTPUB-014",
    "REQ-DEV-ARTPUB-015",
    "REQ-DEV-ARTPUB-016",
    "REQ-DEV-ARTPUB-017",
    "REQ-DEV-ARTPUB-018",
    "REQ-DEV-ARTPUB-019",
    "REQ-DEV-ARTPUB-020",
    "REQ-DEV-ARTPUB-021",
    "REQ-DEV-ARTPUB-022",
    "REQ-DEV-ARTPUB-023",
    "REQ-DEV-ARTPUB-024",
    "REQ-DEV-ARTPUB-025",
    "REQ-DEV-ARTPUB-026",
    "REQ-DEV-ARTPUB-027",
    "REQ-DEV-ARTPUB-028",
    "REQ-DEV-ARTPUB-029",
    "REQ-DEV-ARTPUB-030"
  ],
  "lock_ids": [
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-AUTH-001",
    "LOCK-AUTH-002",
    "LOCK-AUTH-003",
    "LOCK-DATA-001",
    "LOCK-COMP-001",
    "LOCK-AI-002",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-DEV-003",
    "LOCK-DEV-004"
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
    "DOC-SYS-001",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-007",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-017",
    "DOC-SYS-019",
    "DOC-DEV-003",
    "DOC-DEV-004",
    "DOC-DEV-005"
  ],
  "tags": [
    "artifact-publication",
    "release-publication",
    "build-provenance",
    "supply-chain",
    "signing",
    "publisher",
    "release-channel",
    "promotion",
    "repository",
    "offline-bundle",
    "revocation",
    "release-set"
  ]
}
KOA:DOC-META:END -->

# Artifact Publication

## 1. Purpose

This document defines the kOA development process for publishing verified artifacts and releases.

Publication is the controlled transition that makes an immutable candidate available through an identified repository, release channel, mirror, or offline bundle.

It separates:

- artifact creation from publication;
- verification from approval;
- approval from signing;
- signing from repository transfer;
- publication from installation;
- publication from activation;
- build identity from release identity;
- release publication from Release Set compatibility;
- technical artifact publication from private-to-public content disclosure;
- developer access from signing, release, and activation authority.

The process preserves artifact identity from the verified build or creation result through every environment and repository.

## 2. Scope

This document applies to publication of:

- system images and recovery artifacts;
- service and component packages;
- container or equivalent service artifacts;
- governance policy bundles;
- Kristal Runtime Packs;
- compiled language artifacts;
- Ariane Atlases and drivers;
- schema and migration artifacts;
- offline release bundles;
- software bills of materials;
- provenance attestations;
- signed release manifests;
- release evidence;
- other artifacts classified by `contracts/artifact-classes.contract.json`.

It applies to developer workstations, build farms, signing environments, artifact repositories, sovereign mirrors, hubs, control planes, and offline transfer procedures.

It does not define:

- private-to-public application-content disclosure;
- component business-data publication;
- exact repository product;
- exact signature algorithm;
- exact continuous-integration product;
- exact package format;
- exact source-control system;
- exact build command;
- exact rollout or deployment strategy;
- profile-specific repository addresses or credentials;
- runtime activation procedures owned by components.

Publication Gateway remains the owner of governed private-to-public content disclosure. This document owns the development and release process for technical artifacts.

## 3. Canonical References

| Canonical reference | Ownership |
| --- | --- |
| `contracts/artifact-classes.contract.json` | Artifact identities, manifests, verification, integrity, compatibility, publication, activation, rollback, revocation, retention, and evidence requirements. |
| `contracts/release-channels.contract.json` | System, services, governance, and knowledge release-channel identities and publication rules. |
| `generated/authority-manifest.json` | Active registry versions, authority release, canonical ownership, cutover, and activation order. |
| `generated/decision-index.json` | Accepted release, artifact, authority, identity, component, and development decisions. |
| `contracts/profiles/*.profile.json` | Build, signing, repository, mirror, offline, resource, topology, and channel-role realization. |
| `generated/component-catalog.json` | Runtime owners, component boundaries, and authoritative data ownership. |
| `contracts/components/*.component.json` | Component artifact inputs, outputs, admission, activation, rollback, and runtime ownership. |
| `contracts/integration-types.contract.json` | External repository, mirror, distribution, external AI, and integration boundaries. |
| `schemas/artifact-manifest.schema.json` | Artifact-manifest structure. |
| `schemas/release-manifest.schema.json` | Release-manifest structure. |
| `schemas/release-set.schema.json` | Compatible cross-channel Release Set structure. |
| `generated/requirements-index.json` | Requirement statements displayed in section 5. |
| `generated/assertion-index.json` | Release-channel, authority, lifecycle, profile, component, and development invariants. |
| `generated/traceability.json` | Source, decision, requirement, lock, profile, component, artifact, release, test, evidence, and claim relationships. |
| `generated/exception-index.json` | Approved bounded publication exceptions and compensating controls. |
| `generated/test-catalog.json` | Lifecycle, security, profile, operations, boundary, exit, and documentation test definitions. |
| `generated/evidence-catalog.json` | Executed build, verification, signing, publication, mirror, recovery, and conformance evidence. |
| `02-system/19-release-and-artifact-identity.md` | Global release and artifact identity model. |
| `11-recipes/development/artifact-publication.md` | Non-authoritative command examples for publication workflows. |

## 4. Model and Responsibilities

### 4.1 Publication context

The artifact publication path is:

```text
source identity
-> build or creation
-> immutable candidate
-> verification
-> review and approval
-> signing when required
-> repository publication
-> release publication
-> Release Set compatibility
-> independent target admission and activation
```

Publication ends when the destination confirms durable availability and evidence is secured.

Installation, staging, rollout, migration, and activation remain later transitions.

### 4.2 Identity model

A publication operation resolves these distinct identities:

| Identity | Meaning |
| --- | --- |
| Source identity | Exact source revision, source artifact, policy source, grammar source, or knowledge source used to create the candidate. |
| Toolchain identity | Build, compiler, generator, packager, validation, and platform identities used for the result. |
| Candidate identity | Immutable artifact produced before publication. |
| Artifact-class identity | Contract governing manifest, verification, publication, activation, rollback, and revocation. |
| Artifact identity | Stable identity of the published artifact instance. |
| Release identity | Exact artifact collection published within one release channel. |
| Release-channel identity | System, services, governance, or knowledge. |
| Publisher identity | Authority or organization submitting the artifact for publication. |
| Signer identity | Identity creating a required artifact or release signature. |
| Repository identity | Destination responsible for durable publication and retrieval. |
| Target scope | Tenant, environment, profile, platform, channel, and audience of valid use. |
| Activation owner | Runtime component or lifecycle mechanism that can later activate the artifact. |

A filename, URL, tag, branch, directory, or cache location is an alias or location rather than canonical identity.

### 4.3 Role separation

| Role | Responsibility | Excluded authority |
| --- | --- | --- |
| Author or source owner | Creates or approves source input. | Does not gain publication, signing, or activation authority automatically. |
| Builder or creator | Produces the candidate from fixed inputs. | Does not approve its own release merely by completing the build. |
| Verifier | Evaluates required schemas, tests, provenance, integrity, dependencies, and compatibility. | Does not mutate the candidate or grant target activation. |
| Reviewer | Evaluates risk, impact, licensing, rights, exceptions, and release suitability. | Does not replace cryptographic or automated verification. |
| Publisher | Submits an approved candidate to the declared destination and channel. | Does not gain signing or target activation authority automatically. |
| Signer | Applies a signature through the declared protected key class and approval path. | Does not choose an unauthorized artifact, channel, or target scope. |
| Release authority | Approves a release within one declared channel and scope. | Does not activate the release in every target environment. |
| Activation authority | Approves activation in one target environment. | Does not retroactively change publication evidence. |
| Runtime owner | Verifies and activates the artifact in component-owned state. | Does not overwrite the published candidate. |

One human or service can hold more than one role only when active policy permits the combination. Required separation of duties remains explicit.

### 4.4 Publication states

The development publication lifecycle uses these conceptual states:

```text
source_selected
-> building
-> candidate_created
-> verifying
-> verified
-> review_required
-> approved
-> signing
-> signed_or_signature_not_required
-> publishing
-> published
```

Alternative states include:

```text
rejected
blocked
quarantined
incompatible
publication_failed
superseded
revoked
withdrawn
archived
```

These states are independent from:

```text
installed
staged
activating
active
rolled_back
```

### 4.5 Candidate immutability

The candidate is fixed before release-grade verification.

A material change to:

- bytes;
- manifest;
- dependency set;
- build metadata;
- provenance;
- signature envelope;
- included artifact;
- channel;
- target scope;
- exception set;

creates a new candidate or publication request identity and repeats applicable verification.

Repository-side mutation does not preserve the prior artifact identity.

### 4.6 Build and creation evidence

Software and generated artifacts can require:

- source revision;
- build definition;
- dependency lock identity;
- Python, compiler, or generator identity;
- operating-system and architecture identity;
- build worker identity;
- hermeticity or network-use result;
- test results;
- vulnerability result;
- license result;
- software bill of materials;
- provenance attestation;
- reproducibility result;
- known limitations;
- migration and rollback information.

Knowledge, governance, language, and navigation artifacts can use different evidence defined by their artifact class.

### 4.7 Verification

Verification evaluates every applicable artifact-class rule.

The evaluation can include:

- schema;
- artifact identity;
- manifest;
- content integrity;
- publisher;
- signer;
- provenance;
- source identity;
- toolchain identity;
- dependency identity;
- release-channel eligibility;
- platform and profile compatibility;
- component compatibility;
- authority-release compatibility;
- migration readiness;
- revocation;
- downgrade and substitution resistance;
- tests and manual controls;
- exception validity.

A failed required check leaves the candidate unpublished.

### 4.8 Approval

Approval binds one exact publication request.

The approval record includes:

- candidate and manifest identity;
- release channel;
- repository destination;
- target environment and profile scope;
- release identity when applicable;
- policy identity and result;
- required reviewers;
- exception set;
- expiry;
- replay-protection identity;
- obligations;
- approval evidence.

A material change invalidates the approval.

### 4.9 Signing

Signing occurs only when the artifact-class or release-channel contract requires it.

The signing operation:

- resolves the correct key class;
- resolves signer authority;
- verifies candidate identity again;
- verifies approval and separation of duties;
- applies the declared signature envelope;
- records signature identity and evidence;
- avoids exposing the private key to ordinary workspaces or build workers.

A signature attests only to the declared signed statement.

### 4.10 Repository publication

A repository accepts only a valid publication request.

Repository behavior includes:

- immutable artifact storage;
- exact identity lookup;
- collision rejection;
- atomic manifest and artifact visibility;
- idempotent retry;
- durable acknowledgement;
- access control;
- retention;
- supersession and revocation metadata;
- mirror and export support;
- evidence.

A mutable tag can point to an immutable identity when the artifact contract permits it. The tag is not the identity.

### 4.11 Release channels

The independent channels are:

- system;
- services;
- governance;
- knowledge.

An artifact class declares its permitted channel.

A release manifest lists exact immutable members.

A channel publication does not include another channel implicitly.

### 4.12 Release Set compatibility

A Release Set binds compatible channel releases for one target scope.

It records:

- system selection;
- services selection;
- governance selection;
- knowledge selection;
- intentionally absent channels;
- profile and environment;
- compatibility result;
- migration state;
- authority release;
- active exceptions;
- predecessor;
- evidence.

Release Set creation is a compatibility publication step. It does not activate the member releases.

### 4.13 Promotion

Promotion carries the same immutable artifact between controlled environments.

```text
verified candidate identity
-> development availability
-> test availability
-> pilot availability
-> production availability
```

Environment-specific configuration remains a separate declared artifact or runtime input.

Rebuilding from the same source produces a new candidate unless the artifact-class identity model and reproducibility evidence prove identity equivalence.

### 4.14 Offline publication

Offline publication uses a bundle containing:

- bundle identity;
- complete inventory;
- immutable member identities;
- manifests;
- required signatures;
- provenance;
- compatibility;
- revocation freshness context;
- target scope;
- import instructions;
- evidence references.

The receiving environment performs bounded parsing and ordinary admission. Media presence does not grant trust or activation.

### 4.15 Artifact publication and content disclosure

Artifact publication makes a technical lifecycle object available.

Publication Gateway governs private-to-public application content.

Examples:

- a signed service package uses artifact publication;
- a governance policy bundle uses artifact publication;
- a compiled language artifact uses artifact publication;
- an Orgo accountability result becoming public Konnaxion content uses Publication Gateway.

The two processes can produce or consume artifacts, but they retain separate authority, data, receipts, and tests.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-DEV-ARTPUB-001,REQ-DEV-ARTPUB-002,REQ-DEV-ARTPUB-003,REQ-DEV-ARTPUB-004,REQ-DEV-ARTPUB-005,REQ-DEV-ARTPUB-006,REQ-DEV-ARTPUB-007,REQ-DEV-ARTPUB-008,REQ-DEV-ARTPUB-009,REQ-DEV-ARTPUB-010,REQ-DEV-ARTPUB-011,REQ-DEV-ARTPUB-012,REQ-DEV-ARTPUB-013,REQ-DEV-ARTPUB-014,REQ-DEV-ARTPUB-015,REQ-DEV-ARTPUB-016,REQ-DEV-ARTPUB-017,REQ-DEV-ARTPUB-018,REQ-DEV-ARTPUB-019,REQ-DEV-ARTPUB-020,REQ-DEV-ARTPUB-021,REQ-DEV-ARTPUB-022,REQ-DEV-ARTPUB-023,REQ-DEV-ARTPUB-024,REQ-DEV-ARTPUB-025,REQ-DEV-ARTPUB-026,REQ-DEV-ARTPUB-027,REQ-DEV-ARTPUB-028,REQ-DEV-ARTPUB-029,REQ-DEV-ARTPUB-030 -->
- **REQ-DEV-ARTPUB-001 — SHALL:** Every published artifact has a stable artifact identity that is independent of filename, repository path, tag, cache key, transfer location, and activation state.
- **REQ-DEV-ARTPUB-002 — SHALL:** Artifact publication preserves the exact verified artifact bytes or artifact-class identity produced by the approved build or creation process.
- **REQ-DEV-ARTPUB-003 — SHALL NOT:** Promotion between development, test, pilot, and production rebuilds an artifact while retaining the prior artifact identity.
- **REQ-DEV-ARTPUB-004 — SHALL:** Every publication identifies the artifact class, artifact identity, version or content identity, publisher, signer when applicable, release channel, target scope, provenance, compatibility constraints, and lifecycle state.
- **REQ-DEV-ARTPUB-005 — SHALL:** Builder, verifier, reviewer, publisher, signer, release authority, activation authority, and runtime owner remain distinct roles and authority dimensions.
- **REQ-DEV-ARTPUB-006 — SHALL NOT:** Build success, repository write access, possession of a signing key, or a valid signature alone grants release publication or target activation authority.
- **REQ-DEV-ARTPUB-007 — SHALL:** A publication candidate passes every verification required by its artifact-class contract before approval or signing.
- **REQ-DEV-ARTPUB-008 — SHALL:** Release-grade software artifacts include applicable source identity, toolchain identity, dependency identity, build environment identity, test results, provenance, and software-bill-of-material evidence.
- **REQ-DEV-ARTPUB-009 — SHALL:** A release publication identifies the exact immutable member artifacts and the compatibility rules that bind them.
- **REQ-DEV-ARTPUB-010 — SHALL:** System, services, governance, and knowledge artifacts publish only through their declared independent release channels.
- **REQ-DEV-ARTPUB-011 — SHALL NOT:** Publishing one release channel silently publishes, approves, or activates another channel.
- **REQ-DEV-ARTPUB-012 — SHALL:** A Release Set records one compatible selection for every applicable channel and identifies intentionally absent channels.
- **REQ-DEV-ARTPUB-013 — SHALL:** Publication repositories reject identity collision, silent overwrite, mutable replacement, unauthorized downgrade, substitution, and incorrectly scoped publication.
- **REQ-DEV-ARTPUB-014 — SHALL:** A published artifact remains historically identifiable after supersession, revocation, withdrawal, archival, or repository migration.
- **REQ-DEV-ARTPUB-015 — SHALL:** Signing uses the key class, signer scope, approval path, and signature envelope required by the artifact-class and release-channel contracts.
- **REQ-DEV-ARTPUB-016 — SHALL NOT:** Release-signing, authority-signing, governance-signing, or recovery private keys are exposed to ordinary developer workspaces or ordinary build workers.
- **REQ-DEV-ARTPUB-017 — SHALL:** Publication approval binds the exact artifact, manifest, channel, destination, environment scope, policy version, exception set, expiry, and replay-protection identity.
- **REQ-DEV-ARTPUB-018 — SHALL:** Publication is idempotent and a duplicate request returns or reconciles the prior publication result without creating a second artifact identity.
- **REQ-DEV-ARTPUB-019 — SHALL:** A publication reports completion only after the destination confirms durable acceptance and required local evidence is secured.
- **REQ-DEV-ARTPUB-020 — SHALL NOT:** Artifact publication implies installation, staging, activation, rollout, migration, or runtime authority.
- **REQ-DEV-ARTPUB-021 — SHALL:** Published candidates remain inactive until the target runtime independently verifies compatibility, authority, revocation, and activation conditions.
- **REQ-DEV-ARTPUB-022 — SHALL:** Offline publication bundles use bounded parsing, explicit inventories, provenance, signatures when required, compatibility metadata, and controlled import without automatic activation.
- **REQ-DEV-ARTPUB-023 — SHALL:** Interrupted build handoff, signing, repository upload, manifest publication, release publication, or mirror replication resumes idempotently or enters controlled recovery.
- **REQ-DEV-ARTPUB-024 — SHALL:** Revocation blocks future activation and publication reuse and triggers the artifact-class treatment for already published or active instances.
- **REQ-DEV-ARTPUB-025 — SHALL:** External AI, SenTient, user imports, and external integrations produce only candidate material until an owning artifact or component contract admits it.
- **REQ-DEV-ARTPUB-026 — SHALL NOT:** Artifact publication is confused with private-to-public content disclosure performed by Publication Gateway.
- **REQ-DEV-ARTPUB-027 — SHALL:** Publication evidence records evaluated identities, verification results, approvals, signatures, channel, repository result, exceptions, compatibility, and resulting lifecycle state.
- **REQ-DEV-ARTPUB-028 — SHALL:** Profile contracts own publication topology, repository placement, network exposure, offline mirrors, resource limits, worker isolation, and permitted channel roles.
- **REQ-DEV-ARTPUB-029 — SHALL:** Export, backup, restore, mirror transfer, and repository migration preserve artifact, release, channel, provenance, revocation, supersession, and evidence identity.
- **REQ-DEV-ARTPUB-030 — SHALL:** Every active artifact-publication claim has complete decision, requirement, lock, profile, artifact, release, test, evidence, exception, and authority traceability.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Create the publication candidate

1. Resolve the source identity and artifact class.
2. resolve the project, component, profile, and target scope.
3. resolve the fixed build or creation definition.
4. resolve dependency and toolchain identities.
5. execute the controlled build or creation task.
6. collect output, provenance, and build evidence.
7. create the immutable candidate and manifest.
8. assign the candidate identity.
9. close the build task without publication authority.

### 6.2 Verify the candidate

1. Parse the manifest through bounded validation.
2. verify candidate and artifact-class identity.
3. verify source, toolchain, dependency, and provenance identity.
4. verify content integrity when required.
5. verify test, license, vulnerability, and software-bill-of-material results when applicable.
6. verify channel eligibility.
7. verify profile, platform, component, and authority compatibility.
8. verify revocation, downgrade, and substitution controls.
9. verify exception state.
10. record a verified or rejected result.

Verification does not change candidate bytes.

### 6.3 Approve publication

1. Create a publication request for one exact candidate.
2. identify the channel, destination, target scope, and release.
3. identify required reviewers and separation of duties.
4. present verification and risk evidence.
5. resolve policy and exceptions.
6. record reviewer decisions.
7. bind approval to the exact request and expiry.
8. block the request after any material change.

### 6.4 Sign the artifact or release

1. Resolve whether signing applies.
2. resolve the protected key class.
3. authenticate the signer and independent approvers.
4. reverify candidate and manifest identity.
5. verify publication approval.
6. create the declared signature.
7. verify the signature envelope.
8. record signer, key, algorithm class, signed statement, and evidence.
9. return the signed candidate without repository publication authority.

### 6.5 Publish to a repository

1. Authenticate the publisher and destination.
2. revalidate approval, expiry, scope, signature, revocation, and candidate identity.
3. reserve or verify the immutable repository identity.
4. transfer the candidate and manifest.
5. verify received content identity.
6. publish artifact and manifest visibility atomically.
7. receive durable acknowledgement.
8. record the repository location and publication result.
9. preserve the prior result for idempotent replay.
10. emit publication evidence.

### 6.6 Publish a channel release

1. Select exact published member artifacts.
2. verify that each artifact class permits the channel.
3. verify member compatibility.
4. create the release manifest.
5. run channel-level tests.
6. resolve release authority.
7. sign the release manifest when required.
8. publish the immutable release.
9. preserve predecessor and lifecycle relationships.
10. record release evidence.

### 6.7 Publish a Release Set

1. Identify the target profile and environment.
2. resolve one release for every applicable channel.
3. record intentionally absent channels.
4. evaluate cross-channel compatibility.
5. evaluate migrations and rollback constraints.
6. resolve authority release and exceptions.
7. run applicable tests.
8. create the immutable Release Set.
9. publish it through the declared artifact contract.
10. leave target activation to the target lifecycle owner.

### 6.8 Promote an artifact

1. Select the previously verified immutable identity.
2. verify destination eligibility.
3. verify approval for the new environment scope.
4. transfer or mirror the same artifact.
5. verify identity after transfer.
6. publish environment-specific availability metadata separately.
7. preserve original provenance and verification.
8. record promotion evidence.

### 6.9 Revoke or supersede

1. Identify the artifact, release, channel, publisher, signer, and target scope.
2. create a verified revocation or supersession record.
3. block new publication reuse and activation.
4. update repositories and mirrors.
5. notify runtime owners and Release Set evaluators.
6. apply active-state behavior through artifact-class contracts.
7. preserve historical identity and evidence.
8. publish the replacement relationship when applicable.

### 6.10 Recover an interrupted publication

1. Identify the last verified state and operation identity.
2. inspect repository and local journals or equivalent evidence.
3. determine whether transfer, manifest visibility, signature, or acknowledgement completed.
4. resume only an idempotent declared step.
5. otherwise quarantine partial destination state.
6. revalidate authority, expiry, revocation, and identity.
7. reconcile or retry without creating a new identity.
8. record recovery evidence.

### 6.11 Export and restore

1. export immutable artifacts, manifests, releases, Release Sets, revocations, supersession records, and evidence.
2. verify the export independently.
3. restore into a clean repository or environment.
4. preserve exact identities and relationships.
5. revalidate trust and revocation.
6. confirm that inactive, revoked, and superseded state remains correct.
7. run repository and artifact retrieval tests.
8. record restore evidence.

## 7. Failure and Degradation

### 7.1 Build or creation failure

An incomplete build produces no verified publication candidate.

Fixed source and toolchain identities, diagnostics, and available evidence remain preserved.

A retry creates or confirms a candidate only through the artifact-class identity rules.

### 7.2 Verification failure

A schema, provenance, dependency, test, compatibility, license, vulnerability, integrity, revocation, or authority failure blocks publication.

The candidate can remain quarantined for diagnosis.

### 7.3 Approval failure

Rejected, incomplete, conflicting, expired, or missing approval leaves the candidate verified but unpublished.

The candidate does not gain publication authority because it passed technical checks.

### 7.4 Signing failure

A missing key, invalid signer, failed approval, signature error, or custody violation blocks signed publication.

The build worker does not fall back to an unprotected key or unsigned channel when signing is required.

### 7.5 Repository failure

A repository outage, capacity failure, collision, or failed durable acknowledgement leaves publication incomplete.

A bounded idempotent retry uses the same request and candidate identities after revalidation.

### 7.6 Partial visibility

An artifact without its required manifest, release relationship, or evidence remains unavailable or quarantined.

The repository does not expose a partially published release as complete.

### 7.7 Identity collision

An existing immutable identity with different content or manifest produces a security failure.

The repository does not overwrite the existing object.

### 7.8 Incompatible release

A valid release can remain published but unavailable for a specific target or Release Set.

Existing compatible releases remain available.

### 7.9 Mirror or offline transfer failure

Failure of one mirror or transfer path does not change artifact identity or revoke a valid repository copy.

The receiving side does not trust an unverifiable alternate source.

### 7.10 Revoked artifact

A revoked artifact remains historically identifiable.

New publication reuse and activation are blocked.

Active treatment follows the artifact-class contract.

### 7.11 Resource pressure

Build, verification, upload, mirror, and replication concurrency can reduce.

Integrity verification, cancellation, evidence, revocation, and recovery remain protected.

Resource pressure does not permit partial publication or skipped verification.

### 7.12 Network loss

Local candidate creation, verification, approval preparation, signing in an authorized local environment, offline bundle creation, and evidence retention can continue.

Remote repository publication remains unavailable or deferred.

Queued publication is fully revalidated after connectivity returns.

### 7.13 Evidence failure

A publication requiring durable local evidence does not report completion until that evidence is secured.

Evidence forwarding can remain queued within declared bounds.

## 8. Cross-System Interactions

| Counterparty | Publication interaction | Authority boundary |
| --- | --- | --- |
| Source repository | Supplies exact source revision and project metadata. | Source presence does not grant publication authority. |
| Developer workspace | Creates candidates and local verification results. | Ordinary workspaces do not hold protected release-signing keys. |
| Build farm | Produces release-grade artifacts and build evidence from fixed inputs. | Build workers do not approve, sign, or activate automatically. |
| Artifact verifier | Evaluates artifact-class requirements. | Verification does not mutate the candidate or grant activation. |
| Governance Policy Runtime | Evaluates publication, signing, exception, downgrade, and release decisions. | Policy does not perform repository transfer. |
| Identity and Trust | Resolves builder, verifier, reviewer, publisher, signer, repository, artifact, environment, and revocation identity. | Authentication remains distinct from authorization. |
| Signing environment | Applies protected signatures. | Signing does not publish or activate by itself. |
| Artifact repository | Stores immutable artifacts and manifests. | Repository possession does not grant target activation. |
| Release-channel registry | Defines channel identity and membership. | One channel does not absorb another channel's authority. |
| Release Set evaluator | Validates cross-channel compatibility. | Compatibility publication does not activate targets. |
| Runtime component | Independently admits and activates compatible artifacts. | Runtime activation does not rewrite the published artifact. |
| Audit Broker | Stores classified publication and signing evidence. | Audit does not approve publication. |
| Resource Governor | Applies deterministic resource and queue controls. | Resource controls do not change artifact identity or approval. |
| Publication Gateway | Governs private-to-public application-content disclosure. | It is not the technical release repository or release authority. |
| External integration or AI | Can provide candidate source or assistive material. | External output remains non-authoritative until local admission. |

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Closed decisions

| Decision | Closed rule |
| --- | --- |
| `DEC-LIFE-001` | System, services, governance, and knowledge publish and activate through independent release channels. |
| `DEC-REL-001` | Release Sets bind compatible exact channel releases for one target scope. |
| `DEC-ART-001` | Artifact-class contracts own identity, verification, publication, activation, rollback, revocation, and evidence rules. |
| `DEC-AUTH-001` | Build, verification, approval, signing, publication, release, and activation authority remain explicit and bounded. |
| `DEC-IDENT-001` | Source, toolchain, candidate, artifact, publisher, signer, repository, environment, release, and authority identities remain distinct. |
| `DEC-COMP-001` | Runtime owners admit and activate artifacts only through explicit component contracts. |
| `DEC-DATA-001` | Publication does not authorize direct writes to another component's authoritative data stores. |
| `DEC-AI-001` | External AI and SenTient output remains candidate material until local owning-contract admission. |
| `DEC-DEV-001` | Development and build workspaces remain isolated from protected signing and production activation authority. |

### 9.2 Prohibited assumptions

Authors, implementers, validators, and AI agents do not assume that:

- a successful build is publishable;
- a verified artifact is approved;
- an approved artifact is signed;
- a signed artifact is authorized for every channel;
- a published artifact is installed;
- an installed artifact is active;
- a repository tag is an immutable identity;
- a filename uniquely identifies an artifact;
- promotion can rebuild while preserving identity;
- a valid signature proves compatibility;
- a valid signature grants activation authority;
- a builder can approve its own release when separation of duties applies;
- repository administrators can silently replace immutable artifacts;
- latest means compatible or authorized;
- one release channel includes another;
- a Release Set activates its members;
- mirror possession grants trust;
- removable-media possession grants trust;
- a partial upload can be exposed as a complete release;
- external AI output is a release artifact automatically;
- Publication Gateway is the software release repository;
- a profile-specific repository technology applies globally;
- ordinary Markdown requires an artifact hash unless its artifact class declares release-integrity treatment.

A new implementation-affecting publication choice requires an accepted owner decision before dependent authority becomes active.

## 10. Validation Criteria

| Validation group | Required tests |
| --- | --- |
| Release-channel independence | `TEST-LIFE-001`, `TEST-LIFE-002`, `TEST-LIFE-012`, `TEST-LIFE-013`, `TEST-LIFE-014` |
| Verification, activation, and recovery | `TEST-LIFE-003`, `TEST-LIFE-004`, `TEST-LIFE-005`, `TEST-LIFE-006`, `TEST-LIFE-007`, `TEST-LIFE-008`, `TEST-LIFE-009`, `TEST-LIFE-010`, `TEST-LIFE-011`, `TEST-LIFE-015` |
| Supply-chain and authority | `TEST-SEC-003`, `TEST-SEC-005`, `TEST-SEC-006`, `TEST-SEC-007`, `TEST-SEC-008`, `TEST-SEC-015`, `TEST-SYS-004`, `TEST-SYS-011` |
| Component and publication boundaries | `TEST-CROSS-002`, `TEST-CROSS-003`, `TEST-CROSS-008`, `TEST-CROSS-009`, `TEST-CROSS-013`, `TEST-CROSS-014`, `TEST-CROSS-015`, `TEST-SYS-013`, `TEST-SYS-014` |
| Profiles and build environments | `TEST-PROF-004`, `TEST-PROF-005`, `TEST-PROF-006`, `TEST-PROF-007`, `TEST-PROF-008`, `TEST-PROF-009`, `TEST-PROF-011`, `TEST-PROF-012`, `TEST-PROF-013`, `TEST-PROF-014`, `TEST-PROF-015` |
| Operations and incident handling | `TEST-OPS-002`, `TEST-OPS-003`, `TEST-OPS-004`, `TEST-OPS-005`, `TEST-OPS-006`, `TEST-OPS-007`, `TEST-OPS-008`, `TEST-OPS-009`, `TEST-OPS-010` |
| Portability and repository exit | `TEST-EXIT-001`, `TEST-EXIT-002`, `TEST-EXIT-003`, `TEST-EXIT-005`, `TEST-EXIT-006`, `TEST-EXIT-008` |
| Documentation and traceability | `TEST-DOC-VAL-003`, `TEST-DOC-VAL-004`, `TEST-DOC-VAL-005`, `TEST-DOC-VAL-006`, `TEST-DOC-VAL-007`, `TEST-DOC-VAL-008`, `TEST-DOC-VAL-009`, `TEST-DOC-VAL-010`, `TEST-DOC-VAL-012`, `TEST-DOC-VAL-016`, `TEST-DOC-VAL-017`, `TEST-DOC-VAL-018`, `TEST-DOC-VAL-019`, `TEST-DOC-VAL-020` |

Repository and workflow validation additionally confirms:

1. every published object resolves to one active artifact class;
2. artifact and release identities are unique;
3. immutable identity collision and overwrite attempts fail;
4. publication preserves exact verified candidate identity;
5. source, dependency, toolchain, build, test, provenance, and software-bill-of-material evidence is complete when applicable;
6. builder, verifier, reviewer, publisher, signer, release, and activation roles resolve;
7. protected signing keys remain outside ordinary workspaces and build workers;
8. every artifact belongs to a permitted release channel;
9. release manifests list exact immutable members;
10. cross-channel compatibility resolves before Release Set publication;
11. publication approval binds exact scope and remains current;
12. repository transfer is idempotent and durably acknowledged;
13. publication does not create an activation claim;
14. offline bundles use bounded parsing and no automatic activation;
15. revocation and supersession propagate to repositories, mirrors, Release Sets, and runtime owners;
16. export and restore preserve identities, provenance, lifecycle state, and evidence;
17. Publication Gateway remains separate from technical artifact publication;
18. every requirement maps to an active test or approved manual control;
19. every active claim has current traceability and evidence;
20. no unresolved authority marker exists;
21. all active prose is in English.

A failed required check blocks the affected artifact, release, Release Set, publication, or conformance claim.

## 11. Non-Normative Examples

### 11.1 Service artifact

A build farm creates a service package from an exact source revision and committed dependency lock.

The verifier checks tests, provenance, software bill of materials, vulnerabilities, and compatibility. An authorized reviewer approves the services-channel publication. A protected signer signs the release manifest. The publisher uploads the immutable artifact and manifest.

No production service changes until a target runtime independently activates it.

### 11.2 Governance bundle

A governance policy bundle passes schema and policy test vectors.

The governance release authority approves the exact bundle. The governance signing key signs it through a protected signing environment. The bundle is published to the governance channel.

A node later verifies its authority release and activates it atomically through Governance Policy Runtime.

### 11.3 Compiled language artifact

GF Wordbench produces and validates a compiled language candidate.

The artifact is published to the knowledge channel with source, compiler, test, and provenance evidence.

SemantiK Architect Runtime separately verifies and activates the artifact.

### 11.4 Same artifact across environments

A service artifact is first available to test, then pilot, then production.

Each promotion transfers the same immutable identity. Environment configuration and activation approval remain separate.

A rebuild for production would create a new candidate and require new verification.

### 11.5 Duplicate upload

A repository acknowledgement is lost after durable storage.

The publisher retries with the same request and artifact identity. The repository verifies the existing content and returns the prior publication result.

It does not create another identity.

### 11.6 Identity collision

A publisher attempts to upload different bytes under an existing immutable identity.

The repository rejects the request as an identity collision and records security evidence.

The existing artifact remains unchanged.

### 11.7 Offline bundle

A sovereign build process creates a signed offline bundle containing exact artifacts, manifests, inventory, provenance, compatibility, and evidence.

The receiving node applies bounded parsing and verifies every member. The bundle becomes available locally but remains inactive until the normal target activation procedure succeeds.

### 11.8 External AI candidate

An external AI service proposes release notes or a documentation summary.

The output remains candidate content. A local owner reviews and admits it into a release artifact when appropriate.

The external service cannot sign, publish, or activate the release.

### 11.9 Publication Gateway distinction

Orgo produces a redacted accountability report for public Konnaxion display.

That disclosure uses Publication Gateway.

The service package that implements Publication Gateway is published through the artifact-publication process described here.

### 11.10 Revocation

A published service artifact is found to contain a critical defect.

A verified revocation record blocks new activation, updates repositories and mirrors, invalidates affected Release Sets, and notifies runtime owners. Active deployments follow the artifact-class rollback or forward-repair procedure.

The revoked artifact remains historically identifiable.
