<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONF-006",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "conformance",
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
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json",
    "generated/artifact-catalog.json",
    "contracts/artifact-contracts/release-set.schema.json",
    "contracts/artifact-contracts/provenance-receipt.schema.json",
    "contracts/artifact-contracts/decision-receipt.schema.json",
    "contracts/artifact-contracts/offline-bundle.schema.json",
    "contracts/artifact-contracts/policy-bundle.schema.json",
    "contracts/artifact-contracts/runtime-pack.schema.json",
    "contracts/artifact-contracts/language-pack.schema.json",
    "contracts/components/koa-mediatheque.component.json",
    "contracts/integrations/uckk-publication.integration.json",
    "contracts/integrations/uckk-import.integration.json",
    "contracts/artifact-contracts/uckk-learning-package.schema.json",
    "contracts/artifact-contracts/uckk-import-receipt.schema.json",
    "contracts/artifact-contracts/shared-mediatheque-frame.schema.json"
  ],
  "decision_ids": [
    "DEC-REL-001",
    "DEC-LIFE-001",
    "DEC-DATA-001",
    "DEC-PROFILE-001",
    "DEC-GOV-001",
    "DEC-GATE-001",
    "DEC-AI-001",
    "DEC-MEDIATHEQUE-001",
    "DEC-UCKK-EXT-001"
  ],
  "requirement_ids": [
    "REQ-CONF-REL-001",
    "REQ-CONF-REL-002",
    "REQ-CONF-REL-003",
    "REQ-CONF-REL-004",
    "REQ-CONF-REL-005",
    "REQ-CONF-REL-006",
    "REQ-CONF-REL-007",
    "REQ-CONF-REL-008",
    "REQ-CONF-REL-009",
    "REQ-CONF-REL-010",
    "REQ-CONF-REL-011",
    "REQ-CONF-REL-012",
    "REQ-CONF-REL-013",
    "REQ-CONF-REL-014",
    "REQ-CONF-REL-015",
    "REQ-CONF-REL-016",
    "REQ-CONF-REL-017",
    "REQ-CONF-REL-018",
    "REQ-CONF-REL-019",
    "REQ-CONF-REL-020",
    "REQ-CONF-REL-021",
    "REQ-CONF-REL-022",
    "REQ-CONF-REL-023",
    "REQ-CONF-REL-024",
    "REQ-CONF-REL-025",
    "REQ-CONF-REL-026",
    "REQ-CONF-REL-027",
    "REQ-CONF-REL-028",
    "REQ-CONF-REL-029",
    "REQ-CONF-REL-030",
    "REQ-CONF-REL-031",
    "REQ-CONF-REL-032",
    "REQ-CONF-REL-033"
  ],
  "lock_ids": [
    "LOCK-DOC-002",
    "LOCK-DOC-005",
    "LOCK-DOC-006",
    "LOCK-DOC-008",
    "LOCK-DOC-009",
    "LOCK-DOC-010",
    "LOCK-DOC-011",
    "LOCK-DOC-013",
    "LOCK-DOC-019",
    "LOCK-DOC-020",
    "LOCK-DOC-021",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-DATA-001",
    "LOCK-GATE-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-UCKK-EXT-001",
    "LOCK-UCKK-EXT-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONF-000",
    "DOC-CONF-001",
    "DOC-CONF-002",
    "DOC-CONF-003",
    "DOC-CONF-004",
    "DOC-CONF-005",
    "DOC-LIFE-000",
    "DOC-LIFE-002",
    "DOC-LIFE-003",
    "DOC-LIFE-004",
    "DOC-LIFE-005",
    "DOC-LIFE-006",
    "DOC-LIFE-007",
    "DOC-LIFE-008",
    "DOC-LIFE-009",
    "DOC-LIFE-010",
    "DOC-LIFE-011",
    "DOC-LIFE-012",
    "DOC-LIFE-017",
    "DOC-LIFE-018",
    "DOC-SYS-019",
    "DOC-SYS-020",
    "DOC-SEC-003",
    "DOC-SEC-004",
    "DOC-SEC-019",
    "DOC-OPS-003",
    "DOC-OPS-004",
    "DOC-OPS-006",
    "DOC-OPS-007",
    "DOC-OPS-010"
  ],
  "tags": [
    "conformance",
    "release-evidence",
    "release-set",
    "release-channels",
    "artifact-verification",
    "provenance",
    "sbom",
    "signing",
    "compatibility",
    "profile-evidence",
    "activation",
    "rollback",
    "recovery",
    "offline",
    "receipts",
    "selective-disclosure"
  ]
}
KOA:DOC-META:END -->

# Release Evidence

## 1. Purpose

This document defines the evidence required to support a kOA release conformance claim.

A release is not a single package or service version. It is a signed compatibility context that selects tested versions across four release channels:

`text
system
services
governance
knowledge
`

Release evidence proves three different things:

`text
artifact evidence
Release Set compatibility evidence
deployment and activation evidence
`

Artifact evidence proves what each immutable selected object is, where it came from, how it was produced, what it contains, and whether it verifies.

Release Set compatibility evidence proves that the four channel selections can operate together under the claimed profiles, overlays, modes, contracts, migrations, trust state, and integrations.

Deployment and activation evidence proves that the selected release can be staged, authorized, committed, validated, rolled back, repaired, recovered, and operated in the target scope.

No single layer replaces another.

The model prevents these false conclusions:

- a valid signature means a compatible release;
- an SBOM means the artifact was tested;
- passing artifacts mean the Release Set passes;
- a running process means activation committed;
- connected testing proves offline capability;
- staging proves deployment;
- a successful transfer proves publication or activation;
- one profile result proves every profile;
- a prior release result proves a modified release.

## 2. Scope

This document applies globally to release evidence for:

- system artifacts;
- component and service artifacts;
- governance policy bundles;
- Kristal artifacts;
- PGF artifacts;
- Atlases;
- language runtime packs;
- approved knowledge packages;
- Ariane runtime and experience artifacts;
- kOA Mediatheque release artifacts and optional UCKK publication-adapter integration artifacts;
- integration manifests;
- resource envelopes;
- migrations;
- recovery artifacts;
- offline bundles;
- Sovereignty Bundles;
- signed Release Sets;
- release candidates;
- production releases;
- profile-specific releases;
- sovereign-offline releases;
- high-assurance releases;
- independent channel updates;
- release rollback and forward repair.

It governs evidence identity, collection, verification, applicability, freshness, retention, disclosure, reevaluation, and result calculation.

It does not define artifact payload schemas, component behavior, profile membership, test implementation, evidence storage technology, signing algorithms, or release scheduling. Those values belong to their canonical owners.

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
generated/requirements-index.json
generated/assertion-index.json
generated/traceability.json
generated/test-catalog.json
generated/evidence-catalog.json
generated/exception-index.json
generated/artifact-catalog.json
contracts/artifact-contracts/release-set.schema.json
contracts/artifact-contracts/provenance-receipt.schema.json
contracts/artifact-contracts/decision-receipt.schema.json
contracts/artifact-contracts/offline-bundle.schema.json
contracts/artifact-contracts/policy-bundle.schema.json
contracts/artifact-contracts/runtime-pack.schema.json
contracts/artifact-contracts/language-pack.schema.json
`

Their ownership roles are:

| Canonical source | Ownership |
| --- | --- |
| Release-channel registry | The system, services, governance, and knowledge channels |
| Release Set contract | Exact channel selections, compatibility constraints, target profiles, signatures, and verification evidence |
| Artifact-class registry | Artifact identity, payload, verification, activation, recovery, retention, and evidence rules |
| Component contracts | Component interfaces, data ownership, failure behavior, lifecycle, and tests |
| Profile contracts | Applicability, overlays, hardware, modes, offline, security, resource, and recovery requirements |
| Integration registry | External capability, identity, data, endpoint, failure, and removal behavior |
| Provenance-receipt contract | Source, revision, materials, toolchain, environment, transformations, tests, and publication lineage |
| Decision-receipt contract | Request, decision, execution, commit, rollback, repair, and outcome evidence |
| Offline-bundle contract | Signed offline transport, sequence, trust, application order, rollback, recovery, and receipts |
| `requirements.registry.json` | Normative release-evidence requirements |
| `locks.registry.json` | Non-waivable release, lifecycle, profile, data, and documentation invariants |
| `traceability.registry.json` | Release-to-artifact, requirement, test, evidence, profile, component, and exception links |
| `test-catalog.registry.json` | Required test identities, conditions, procedures, and expected evidence |
| `evidence.registry.json` | Evidence identity, subject, producer, verification, access, and retention |
| `exceptions.registry.json` | Bounded current exceptions and compensating evidence |

This document explains evidence composition. It does not become the canonical release manifest or evidence registry.

## 4. Model and Responsibilities

### 4.1 Release-evidence package

A release-evidence package contains or references:

`text
release_claim_id
Release Set identity and signature
channel-selection manifests
artifact-evidence records
profile and overlay claims
component claims
compatibility results
test results
provenance receipts
SBOM evidence
signature and trust verification
migration evidence
activation receipts
rollback and repair results
offline evidence
exceptions
result
validity
`

The package can be distributed across evidence records. Its manifest resolves every required relationship.

### 4.2 Evidence levels

| Evidence level | Primary question |
| --- | --- |
| Artifact | Is this exact immutable object authentic, understood, traceable, testable, and valid for its class? |
| Release Set | Are all selected channel versions mutually compatible for the target scope? |
| Deployment | Can the Release Set be authorized, activated, operated, rolled back, repaired, and recovered at the target? |

A release claim passes only when all applicable levels pass.

### 4.3 Channel evidence

The Release Set includes explicit selection evidence for:

| Channel | Typical evidence |
| --- | --- |
| System | System image, node runtime, boot or recovery material, resource envelopes |
| Services | Component packages, service migrations, Ariane runtime and integration manifests |
| Governance | Governance policy bundles and governed schema or migration material |
| Knowledge | Kristal, PGF, Atlas, language runtime, and approved knowledge packages |

A lifecycle container or evidence object remains outside the channel model.

### 4.4 Artifact evidence record

Each selected artifact evidence record identifies:

`text
artifact identity
artifact class
artifact version
release channel
manifest identity
payload digest
producer
production time
provenance receipt
SBOM reference
signature requirements
signature verification
trust scope
revocation result
profile applicability
compatibility declaration
test results
recovery behavior
retention class
`

Artifact evidence remains bound to the exact bytes.

### 4.5 Integrity and signatures

Integrity evidence proves that the bytes match the declared manifest and digest.

Signature evidence proves that a signer bound a signed object to a cryptographic value.

Trust evidence proves whether that signer is trusted for the exact artifact class, channel, environment, tenant, and intended use.

These results remain separate from compatibility, authorization, and activation.

### 4.6 Provenance

Provenance evidence covers:

- canonical source identities;
- source revisions;
- source integrity;
- dependency inputs;
- base images;
- policy or knowledge inputs;
- toolchain identity and versions;
- lock or manifest inputs;
- build or compilation environment;
- network access class;
- ordered transformations;
- producer identity;
- tests;
- publication event.

External AI or external integration output appears as an external candidate material with its integration and transfer provenance. It does not become authoritative because it appears in provenance.

### 4.7 SBOM evidence

SBOM evidence identifies software-bearing contents and dependencies appropriate to the artifact class.

Verification can include:

- SBOM schema;
- artifact identity;
- component identities;
- direct and transitive dependencies;
- suppliers;
- versions;
- digests;
- licenses;
- vulnerability or policy evaluation references;
- completeness;
- relationship to provenance and build inputs.

An SBOM does not replace provenance or behavioral testing.

### 4.8 Compatibility evidence

Compatibility evidence can cover:

- four-channel version vector;
- component contracts;
- service APIs;
- governance schemas;
- knowledge formats;
- data and storage schemas;
- migrations;
- profile and overlay;
- operating mode;
- architecture;
- system family;
- runtime or ABI;
- language runtime;
- trust generation;
- external integrations;
- mutual exclusions;
- co-activation requirements;
- recovery versions.

Every evaluated constraint records its source and result.

### 4.9 Profile evidence

Profile evidence identifies the exact:

- primary profile;
- overlays;
- inherited requirements;
- capabilities;
- hardware envelope;
- architecture;
- operating modes;
- resource envelope;
- security controls;
- storage and network rules;
- offline behavior;
- recovery target;
- assurance requirements.

Evidence from `user_lightweight` does not prove `sovereign_hub`. Evidence from connected operation does not prove `sovereign_offline`.

### 4.10 Test evidence

Release test evidence includes:

- stable test identity;
- requirement and lock links;
- exact artifact or Release Set;
- target profile and overlays;
- environment;
- operating mode;
- tool and tool version;
- execution time;
- expected result;
- actual result;
- failure code;
- evidence reference.

Required test families can include:

`text
schema and contract
component integration
data ownership
security
privacy and disclosure
artifact verification
cross-channel compatibility
migration
activation
rollback
forward repair
recovery
offline
performance and resource envelope
portability and independent restoration
`

### 4.11 Migration evidence

Migration evidence identifies:

- owner;
- migration artifact;
- source and target versions;
- affected data classes;
- strategy;
- determinism or bounded nondeterminism;
- checkpoints;
- preparation result;
- execution result;
- authoritative commit;
- data validation;
- rollback or forward repair;
- final version.

A prepared or partially executed migration is not committed evidence.

### 4.12 Activation evidence

Activation evidence distinguishes:

`text
artifact verification
staging
authority decision
execution start
migration preparation
commit boundary
authoritative commit
health and readiness
active artifact identity
Release Set identity
rollback availability
final outcome
`

The owning lifecycle boundary produces the authoritative commit receipt.

### 4.13 Recovery evidence

Recovery evidence can include:

- retained rollback artifact verification;
- checkpoint verification;
- rollback result;
- forward-repair artifact identity;
- repair result;
- recovery-target activation;
- restored data validation;
- identity and trust validation;
- policy validation;
- post-recovery Release Set;
- closure receipt.

Executable rollback remains distinct from data restoration.

### 4.14 Offline evidence

Offline release evidence is produced under the claimed disconnected or restricted-connectivity condition.

It covers:

- local identity and trust;
- signed trust and revocation updates;
- bundle sequence;
- rollback protection;
- quarantine;
- bounded parsing;
- complete local artifacts;
- application ordering;
- local policy;
- local receipts;
- UCKK learning-package source, license, integrity, completeness, provenance, and shared-frame mapping evidence where applicable;
- quarantine-before-acceptance evidence and separate local identity creation;
- proof that accepted learning material remains usable offline;
- proof that reconnection does not trigger automatic upload, overwrite, deletion, or synchronization;
- activation;
- recovery;
- later reconciliation.

### 4.15 Evidence graph

The release-evidence graph links:

`text
release claim
 → Release Set
 → four channel selections
 → artifact claims
 → provenance
 → SBOM
 → signature and trust
 → tests
 → compatibility evidence
 → profile claims
 → deployment evidence
 → exceptions
`

Every mandatory edge resolves.

### 4.16 Evidence validity and disclosure

Evidence validity depends on subject identity, version, digest, scope, environment, trust state, validator version, production time, and policy.

Public or ordinary views expose a bounded proof.

Restricted source materials, security findings, private proof, credentials, personal data, and protected content remain access-controlled.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-CONF-REL-001,REQ-CONF-REL-002,REQ-CONF-REL-003,REQ-CONF-REL-004,REQ-CONF-REL-005,REQ-CONF-REL-006,REQ-CONF-REL-007,REQ-CONF-REL-008,REQ-CONF-REL-009,REQ-CONF-REL-010,REQ-CONF-REL-011,REQ-CONF-REL-012,REQ-CONF-REL-013,REQ-CONF-REL-014,REQ-CONF-REL-015,REQ-CONF-REL-016,REQ-CONF-REL-017,REQ-CONF-REL-018,REQ-CONF-REL-019,REQ-CONF-REL-020,REQ-CONF-REL-021,REQ-CONF-REL-022,REQ-CONF-REL-023,REQ-CONF-REL-024,REQ-CONF-REL-025,REQ-CONF-REL-026,REQ-CONF-REL-027,REQ-CONF-REL-028,REQ-CONF-REL-029,REQ-CONF-REL-030,REQ-CONF-REL-031,REQ-CONF-REL-032,REQ-CONF-REL-033 -->
- **REQ-CONF-REL-001 — SHALL:** Every release-evidence package identify the release claim, signed Release Set, exact system, services, governance, and knowledge channel selections, target profiles and overlays, evaluator, evidence-production interval, and release result.
- **REQ-CONF-REL-002 — SHALL:** Release evidence distinguish artifact evidence, Release Set compatibility evidence, and deployment or activation evidence.
- **REQ-CONF-REL-003 — SHALL NOT:** Passing evidence at one release-evidence level substitute for missing or failed evidence at another level.
- **REQ-CONF-REL-004 — SHALL:** Every selected release artifact have evidence for stable identity, class, version, release channel, manifest, payload integrity, producer, provenance, compatibility, and lifecycle behavior.
- **REQ-CONF-REL-005 — SHALL:** Every required artifact signature be verified against the exact tenant, environment, release channel, artifact class, signer, intended use, validity, and revocation context.
- **REQ-CONF-REL-006 — SHALL NOT:** A valid signature or matching content digest by itself establish artifact authorization, compatibility, profile applicability, publication, installation, activation, or release conformance.
- **REQ-CONF-REL-007 — SHALL:** Every software-bearing release artifact include or reference a verified SBOM appropriate to its artifact class and exact artifact identity.
- **REQ-CONF-REL-008 — SHALL:** Every release artifact include or reference verified provenance covering canonical source, source revision, materials, dependencies, toolchain, build or compilation environment, ordered transformations, tests, producer, and publication.
- **REQ-CONF-REL-009 — SHALL:** Provenance and SBOM evidence remain linked to the exact artifact version and content digest they describe.
- **REQ-CONF-REL-010 — SHALL:** Release Set evidence verify explicit compatible selections for all four canonical release channels and every applicable cross-channel compatibility constraint.
- **REQ-CONF-REL-011 — SHALL NOT:** An offline bundle, Sovereignty Bundle, receipt, provenance statement, SBOM, migration package, or publication package be represented as a fifth release channel.
- **REQ-CONF-REL-012 — SHALL:** An independent channel update include evidence that the unchanged channel selections remained explicit and that all affected compatibility constraints were reevaluated.
- **REQ-CONF-REL-013 — SHALL:** Release compatibility evidence cover component-contract versions, interfaces, data schemas, migrations, profiles, overlays, operating modes, trust generations, external integrations, and artifact-class dependencies applicable to the release.
- **REQ-CONF-REL-014 — SHALL:** Target-profile evidence be produced for the exact primary profile, overlays, architecture, hardware envelope, operating modes, offline envelope, security controls, and resource constraints being claimed.
- **REQ-CONF-REL-015 — SHALL NOT:** Evidence produced for one profile, overlay, architecture, environment, operating mode, or hardware envelope be generalized silently to another.
- **REQ-CONF-REL-016 — SHALL:** Release tests execute against immutable selected artifacts or byte-identical verified copies rather than mutable development outputs, workspace state, repository branches, or unpinned tags.
- **REQ-CONF-REL-017 — SHALL:** Release evidence include required contract, integration, security, privacy, lifecycle, migration, operational, recovery, and conformance test results for the claimed scope.
- **REQ-CONF-REL-018 — SHALL:** Activation evidence distinguish verification, staging, authority decision, execution, authoritative commit, health validation, rollback availability, and final active identity.
- **REQ-CONF-REL-019 — SHALL NOT:** Download, caching, transfer, staging, process startup, container readiness, destination receipt, or partial migration be reported as successful release activation.
- **REQ-CONF-REL-020 — SHALL:** Release evidence include tested rollback, forward-repair, or recovery behavior for every artifact class and migration path required by the Release Set.
- **REQ-CONF-REL-021 — SHALL:** Migration evidence identify owner, source version, target version, strategy, checkpoints, deterministic or bounded behavior, authoritative commit, data effects, rollback or repair path, and verification result.
- **REQ-CONF-REL-022 — SHALL:** Offline release evidence cover bundle signature, trust and revocation state, sequence, rollback protection, parsing limits, quarantine, target profiles, application order, local receipts, activation, recovery, and reconciliation.
- **REQ-CONF-REL-023 — SHALL:** Critical release decisions and transitions include machine-readable receipts that distinguish request, decision, execution, target effect, commit, failure, cancellation, rollback, forward repair, recovery, and reconciliation.
- **REQ-CONF-REL-024 — SHALL:** Release evidence identify every approved exception, its scope, expiry, compensating controls, required tests, evidence, owner, and effect on the release claim.
- **REQ-CONF-REL-025 — SHALL NOT:** An exception waive artifact identity, canonical ownership, direct cross-component write prohibitions, Release Set four-channel identity, required signing or trust checks, atomic activation, receipt truth, or another non-waivable lock.
- **REQ-CONF-REL-026 — SHALL:** Release evidence remain valid only while subject identities, artifact digests, Release Set, profile scope, trust and revocation state, validator versions, required tests, evidence freshness, and exception validity remain unchanged.
- **REQ-CONF-REL-027 — SHALL:** A material change to a selected artifact, channel selection, profile, overlay, contract, migration, integration, trust state, validator, required test, evidence item, or exception trigger reevaluation of every affected release claim.
- **REQ-CONF-REL-028 — SHALL:** Release-evidence reports expose claim identity, Release Set identity, channel selections, target scope, result, failed and blocked checks, evidence references, exceptions, evaluator, timestamps, validity, and remediation in machine-readable form.
- **REQ-CONF-REL-029 — SHALL:** Public and ordinary release-evidence views use selective disclosure and exclude secrets, private keys, credentials, protected payloads, restricted personal data, protected cultural content, and unnecessary private proof.
- **REQ-CONF-REL-030 — SHALL:** Release-evidence generation and result calculation be deterministic for identical canonical inputs, artifact bytes, Release Set, target scope, validator versions, test results, evidence, trust state, and exceptions.
- **REQ-CONF-REL-031 — SHALL:** A release claim that includes UCKK import carry evidence for integration version, source identity, package version, complete resource graph, integrity, license, restrictions, provenance, shared-frame mapping, quarantine, local acceptance, and import receipt.
- **REQ-CONF-REL-032 — SHALL:** An offline-learning claim prove that accepted UCKK material and required local runtime remain usable under the claimed disconnected condition.
- **REQ-CONF-REL-033 — SHALL NOT:** Release evidence represent remote availability, transport success, or reconnection as local acceptance, authority transfer, automatic update, or synchronization.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Evidence planning

Evidence planning:

1. identifies the release candidate and target scope;
2. resolves the signed Release Set structure;
3. inventories selected artifacts;
4. computes applicable profiles, overlays, modes, integrations, and requirements;
5. resolves required tests and evidence;
6. resolves current exceptions;
7. creates the evidence graph;
8. blocks the release claim when mandatory evidence ownership is unresolved.

### 6.2 Artifact evidence collection

For every artifact:

1. resolve exact identity and bytes;
2. validate its artifact contract;
3. verify manifest and content digest;
4. verify required signatures;
5. resolve signer trust and revocation;
6. verify provenance;
7. verify SBOM where applicable;
8. validate profile applicability;
9. execute artifact-class tests;
10. record recovery and retention evidence;
11. produce the artifact claim.

### 6.3 Release Set verification

Release Set verification:

1. verifies Release Set identity and signature;
2. resolves all four channel selections;
3. verifies every selected artifact claim;
4. loads all compatibility constraints;
5. evaluates cross-channel constraints;
6. evaluates profile and overlay constraints;
7. evaluates migrations and co-activation;
8. records every passed, failed, and blocked constraint;
9. produces the Release Set compatibility result.

### 6.4 Profile evidence production

Profile evidence production:

1. provisions the exact target profile and overlays;
2. verifies hardware and architecture;
3. applies the selected Release Set;
4. enters each claimed operating mode;
5. executes profile, security, resource, offline, and recovery tests;
6. records environment identity and tool versions;
7. preserves evidence;
8. produces the profile result.

### 6.5 Release test execution

The release test runner:

1. verifies immutable artifact inputs;
2. verifies Release Set and profile identity;
3. verifies test prerequisites;
4. executes required test families;
5. captures actual results and failure codes;
6. links evidence to requirements and locks;
7. prevents reuse outside matching scope;
8. records tool and environment versions.

### 6.6 Activation evidence production

Activation evidence production:

1. verifies target authority and pre-activation state;
2. stages selected artifacts;
3. records the authority decision;
4. prepares migrations;
5. enters the atomic commit boundary;
6. records authoritative commit or non-commit;
7. validates active identities, health, readiness, data, and policy;
8. verifies rollback or repair readiness;
9. creates activation receipts;
10. records the final deployment result.

### 6.7 Failure and recovery evidence

After a failed activation or migration:

1. preserve failure evidence;
2. identify whether commit occurred;
3. preserve or restore the last valid state;
4. execute the class-defined rollback, repair, or recovery path;
5. validate authoritative data and active identities;
6. produce recovery receipts;
7. record whether the release remains failed, blocked, or successfully recovered;
8. avoid converting recovery success into evidence that the failed release activated successfully.

### 6.8 Offline evidence production

Offline evidence production:

1. disconnects or restricts connectivity according to the claim;
2. verifies local time, identity, trust, policy, and revocation bounds;
3. verifies the signed bundle;
4. verifies sequence and rollback protection;
5. exercises quarantine and bounded parsing;
6. applies the Release Set locally;
7. captures local receipts;
8. tests local operation and recovery;
9. reconnects when the test requires reconciliation;
10. records reconciliation results.

### 6.9 Evidence verification

Evidence verification:

1. validates evidence schema;
2. resolves subject identity and scope;
3. verifies integrity and signatures where required;
4. verifies producer eligibility;
5. verifies test and requirement links;
6. verifies freshness;
7. verifies environment and profile match;
8. verifies access classification;
9. records verified, failed, or indeterminate state;
10. rejects invalid evidence from mandatory claims.

### 6.10 Release result calculation

The evaluator:

1. loads the complete evidence graph;
2. verifies every mandatory edge;
3. checks artifact claims;
4. checks Release Set compatibility;
5. checks profile and deployment claims;
6. checks tests and evidence;
7. checks exceptions;
8. identifies failed checks;
9. identifies blocked checks;
10. calculates pass, fail, or blocked;
11. produces machine-readable and selectively disclosed reports.

### 6.11 Reevaluation

Reevaluation:

1. detects changed artifacts, manifests, channel selections, profiles, contracts, tests, trust, exceptions, or evidence;
2. traverses affected evidence edges;
3. invalidates or expires affected claims;
4. reruns required validators and tests;
5. reuses only matching valid evidence;
6. produces a successor release claim.

### 6.12 Evidence retention and withdrawal

Retention and withdrawal:

1. preserve evidence required for active releases, rollback, recovery, audit, and supply chain;
2. preserve prior release claims and supersession links;
3. withdraw false, revoked, or invalid claims;
4. record withdrawal reason;
5. prevent withdrawn evidence from supporting a new pass;
6. maintain selective disclosure.

## 7. Failure States and Safe Degradation

| Failure code | Condition | Protected result | Safe degraded result |
| --- | --- | --- | --- |
| `release_evidence_claim_identity_missing` | Release claim or subject identity is absent | Claim is blocked | Complete claim identity |
| `release_evidence_release_set_missing` | Signed Release Set is absent | Release claim is blocked | Produce the Release Set |
| `release_evidence_release_set_signature_failed` | Release Set signature or trust fails | Release claim fails | Correct signing or trust |
| `release_evidence_channel_selection_incomplete` | A canonical channel selection is absent | Release claim is blocked | Complete all four selections |
| `release_evidence_artifact_claim_missing` | Selected artifact lacks a claim | Release claim is blocked | Evaluate the artifact |
| `release_evidence_artifact_identity_mismatch` | Evidence describes different bytes or version | Artifact and release claims fail | Reproduce matching evidence |
| `release_evidence_integrity_failed` | Manifest or payload digest fails | Artifact claim fails | Rebuild or retransmit |
| `release_evidence_signature_or_trust_failed` | Artifact signature, scope, or revocation fails | Artifact claim fails | Restore valid trust context |
| `release_evidence_provenance_missing` | Required provenance is absent | Artifact claim is blocked | Produce provenance |
| `release_evidence_provenance_invalid` | Source, toolchain, environment, transformation, or publication lineage fails | Artifact claim fails | Rebuild through approved flow |
| `release_evidence_sbom_missing` | Required SBOM is absent | Artifact claim is blocked | Produce the SBOM |
| `release_evidence_sbom_invalid` | SBOM identity or contents do not match | Artifact claim fails | Correct and verify the SBOM |
| `release_evidence_compatibility_failed` | Cross-channel or profile compatibility fails | Release claim fails | Select compatible versions |
| `release_evidence_compatibility_incomplete` | Required constraint was not evaluated | Release claim is blocked | Complete evaluation |
| `release_evidence_profile_mismatch` | Evidence was produced under another profile or overlay | Claim is blocked | Test the claimed scope |
| `release_evidence_test_failed` | Required release test fails | Release claim fails | Remediate and rerun |
| `release_evidence_test_not_executed` | Required release test did not run | Release claim is blocked | Execute the test |
| `release_evidence_stale` | Evidence no longer matches subject, time, trust, or scope | Claim is blocked | Refresh evidence |
| `release_evidence_activation_not_committed` | Activation did not reach authoritative commit | Deployment claim fails | Preserve prior state or recover |
| `release_evidence_false_activation_success` | Staging, startup, or transfer is reported as commit | Claim is invalidated | Correct receipts and reevaluate |
| `release_evidence_migration_failed` | Required migration fails | Release or deployment claim fails | Roll back, repair, or recover |
| `release_evidence_recovery_unverified` | Required rollback, repair, or recovery evidence is absent | Release claim is blocked | Execute recovery tests |
| `release_evidence_offline_scope_unproven` | Offline behavior was inferred rather than tested | Offline claim is blocked | Test offline conditions |
| `release_evidence_exception_invalid` | Exception is expired, overbroad, or lacks controls | Claim fails or blocks according to completed checks | Repair or remove exception |
| `release_evidence_receipt_incomplete` | Critical transition lacks truthful receipt stages | Deployment claim fails or blocks | Produce valid evidence through approved recovery |
| `release_evidence_restricted_data_exposed` | Report exposes protected evidence | Report publication fails | Produce a selective view |
| `release_evidence_result_nondeterministic` | Identical inputs produce different mandatory results | Automation claim fails | Repair evaluator determinism |

Artifact or profile evidence can remain valid after an unrelated release failure. It cannot support a passing release claim until the complete Release Set evidence graph passes.

## 8. Cross-Component Interactions

### 8.1 Release authority

The release authority identifies the Release Set and target scope.

It does not manufacture artifact, profile, compatibility, or activation evidence.

### 8.2 Artifact producers

Artifact producers provide immutable artifacts, manifests, provenance, SBOMs, tests, and publication evidence.

Production authority remains separate from target activation authority.

### 8.3 Identity and Trust

Identity and Trust verifies signer identity, signatures, trust scope, and revocation.

It does not decide cross-channel compatibility or deployment activation.

### 8.4 Component owners

Component owners provide contract, integration, migration, data-ownership, failure, and recovery evidence.

They remain the authority for their state transitions.

### 8.5 Profile evaluators

Profile evaluators produce evidence under exact profile, overlay, hardware, mode, security, resource, offline, and recovery conditions.

They cannot generalize results outside that scope.

### 8.6 Lifecycle services

Lifecycle services produce verification, staging, activation, rollback, repair, recovery, and active-identity receipts.

Their commit state determines deployment truth.

### 8.7 Test and evidence systems

Test runners execute declared tests. Evidence systems record and verify results.

Neither creates architectural authority or converts missing tests into pass results.

### 8.8 Audit Broker

Audit Broker stores, verifies, indexes, and selectively discloses release receipts and evidence.

It does not replace the release evaluator or underlying owners.

### 8.9 External integrations

External integrations contribute only their declared capability, transfer, availability, failure, and removal evidence.

External AI output remains candidate input and cannot satisfy release authority by itself.

### 8.10 Documentation and AI tooling

Documentation tooling validates registration, requirements, locks, references, traceability, and drift.

AI tools can assemble evidence manifests and summarize failures from canonical records, but they cannot infer missing evidence or claim unexecuted tests.

## 9. Decision Closure and Prohibited Assumptions

This document closes the release-evidence interpretation as follows:

- release evidence has artifact, Release Set, and deployment levels;
- the Release Set binds all four canonical channels;
- every selected artifact has exact identity-bound evidence;
- signatures, trust, integrity, provenance, SBOM, compatibility, and tests remain distinct;
- profile evidence is exact-scope evidence;
- immutable release inputs are tested;
- migrations and activation report authoritative commit;
- rollback, forward repair, and recovery are tested;
- offline claims are tested offline;
- critical transitions produce truthful receipts;
- exceptions remain bounded and cannot waive non-waivable locks;
- material changes trigger reevaluation;
- reports remain machine-readable and selectively disclosed;
- identical inputs produce deterministic mandatory results.

The following assumptions are prohibited:

- one signed artifact proves a release;
- an SBOM proves provenance;
- provenance proves compatibility;
- compatibility proves activation;
- a running process proves commit;
- staging proves deployment;
- an offline bundle is a release channel;
- one profile proves another;
- connected testing proves offline behavior;
- a previous digest supports modified bytes;
- an exception permits removal of a canonical channel;
- external AI output is release evidence without owner acceptance;
- a screenshot alone satisfies mandatory activation evidence;
- a generated report owns the facts it displays;
- a missing test is advisory;
- restricted evidence must be published for a public claim;
- ordinary Markdown hashes determine release evidence.

A new release-evidence level, canonical channel, implicit evidence-substitution rule, or non-waivable exception change requires an accepted owner decision and complete impact validation.

## 10. Validation Criteria

This document is conformant when all of the following checks pass:

1. the metadata block is first, valid, and declares status `active`;
2. the document contains the required 11 normative sections;
3. all 30 requirement identifiers are unique and registered;
4. every declared decision is accepted;
5. every declared lock exists and is active;
6. release-evidence manifests identify the claim, signed Release Set, four channel selections, target scope, evaluator, and result;
7. every selected artifact has exact identity, manifest, integrity, provenance, compatibility, test, and lifecycle evidence;
8. signature tests use exact tenant, environment, channel, class, intended use, validity, and revocation scope;
9. tests prove that integrity and signature success do not imply compatibility or activation;
10. software-bearing artifact tests validate SBOM identity, completeness, dependencies, and linkage;
11. provenance tests validate source, revision, materials, toolchain, environment, transformations, producer, tests, and publication;
12. Release Set tests require system, services, governance, and knowledge selections;
13. independent-update tests preserve explicit unchanged selections and reevaluate affected constraints;
14. compatibility tests cover component, interface, data, migration, profile, mode, trust, integration, and artifact dependencies;
15. profile tests run under exact primary profile, overlays, architecture, hardware, modes, security, resources, offline, and recovery scope;
16. immutable-input tests reject mutable branches, tags, workspaces, and unverified outputs;
17. test-family coverage includes contract, integration, security, privacy, lifecycle, migration, operations, recovery, and conformance where applicable;
18. activation tests distinguish verification, staging, authority, execution, commit, health, active identity, and rollback readiness;
19. false-success tests reject transfer, staging, startup, readiness, and partial migration as commit evidence;
20. migration tests validate owner, versions, strategy, checkpoint, commit, data result, and recovery;
21. rollback, repair, and recovery tests cover every required artifact class and migration path;
22. offline tests cover signature, trust, sequence, rollback protection, parsing, quarantine, application order, local receipts, recovery, and reconciliation;
23. receipt tests distinguish request, decision, execution, effect, commit, rollback, repair, recovery, and reconciliation;
24. exception tests cover scope, expiry, owner, controls, tests, evidence, and non-waivable locks;
25. freshness tests invalidate evidence after material subject, trust, profile, validator, test, or exception changes;
26. reevaluation tests traverse all affected claims;
27. report tests expose failed and blocked checks without false pass;
28. selective-disclosure tests protect secrets, credentials, protected payloads, personal data, cultural content, and private proof;
29. deterministic-generation tests compare identical canonical inputs and results;
30. no unresolved-authority marker, duplicate identifier, or unregistered normative statement exists;
31. active prose is English;
32. ordinary Markdown validation does not depend on file-content hashes.

Expected validator failure codes include:

`text
release_evidence_claim_identity_missing
release_evidence_release_set_missing
release_evidence_release_set_signature_failed
release_evidence_channel_selection_incomplete
release_evidence_artifact_claim_missing
release_evidence_artifact_identity_mismatch
release_evidence_integrity_failed
release_evidence_signature_or_trust_failed
release_evidence_provenance_missing
release_evidence_provenance_invalid
release_evidence_sbom_missing
release_evidence_sbom_invalid
release_evidence_compatibility_failed
release_evidence_compatibility_incomplete
release_evidence_profile_mismatch
release_evidence_test_failed
release_evidence_test_not_executed
release_evidence_stale
release_evidence_activation_not_committed
release_evidence_false_activation_success
release_evidence_migration_failed
release_evidence_recovery_unverified
release_evidence_offline_scope_unproven
release_evidence_exception_invalid
release_evidence_receipt_incomplete
release_evidence_restricted_data_exposed
release_evidence_result_nondeterministic
`

## 11. Non-Normative Examples

### 11.1 Passing release claim

A signed Release Set selects explicit system, services, governance, and knowledge versions. Every artifact verifies, all compatibility constraints pass, profile tests run under the target hardware and overlays, activation commits, and rollback and recovery tests pass. The release claim passes.

### 11.2 Blocked SBOM evidence

All artifact tests pass, but one software-bearing service artifact lacks its required verified SBOM. The artifact claim and release claim remain blocked rather than passed.

### 11.3 Failed compatibility

Each selected artifact passes independently. The governance policy bundle requires a newer services contract than the selected services channel provides. Release Set compatibility fails, so the release claim fails.

### 11.4 False activation signal

A service container starts and reports readiness, but the lifecycle owner never commits the new Release Set identity. The deployment evidence does not report successful activation.

### 11.5 Offline release evidence

A sovereign-offline target verifies a signed bundle, sequence, trust updates, four channel selections, application order, local receipts, rollback, and recovery while disconnected. Reconciliation evidence is added after connectivity returns.
