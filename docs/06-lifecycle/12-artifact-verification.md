<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-LIFE-012",
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
    "generated/evidence-catalog.json",
    "contracts/components/identity-and-trust.component.json",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/components/resource-governor.component.json"
  ],
  "decision_ids": [
    "DEC-REL-001",
    "DEC-DATA-001",
    "DEC-PROFILE-001"
  ],
  "requirement_ids": [
    "REQ-LIFE-VERIFY-001",
    "REQ-LIFE-VERIFY-002",
    "REQ-LIFE-VERIFY-003",
    "REQ-LIFE-VERIFY-004",
    "REQ-LIFE-VERIFY-005",
    "REQ-LIFE-VERIFY-006",
    "REQ-LIFE-VERIFY-007",
    "REQ-LIFE-VERIFY-008",
    "REQ-LIFE-VERIFY-009",
    "REQ-LIFE-VERIFY-010",
    "REQ-LIFE-VERIFY-011",
    "REQ-LIFE-VERIFY-012",
    "REQ-LIFE-VERIFY-013",
    "REQ-LIFE-VERIFY-014",
    "REQ-LIFE-VERIFY-015",
    "REQ-LIFE-VERIFY-016",
    "REQ-LIFE-VERIFY-017",
    "REQ-LIFE-VERIFY-018",
    "REQ-LIFE-VERIFY-019",
    "REQ-LIFE-VERIFY-020",
    "REQ-LIFE-VERIFY-021",
    "REQ-LIFE-VERIFY-022",
    "REQ-LIFE-VERIFY-023",
    "REQ-LIFE-VERIFY-024",
    "REQ-LIFE-VERIFY-025",
    "REQ-LIFE-VERIFY-026",
    "REQ-LIFE-VERIFY-027",
    "REQ-LIFE-VERIFY-028",
    "REQ-LIFE-VERIFY-029",
    "REQ-LIFE-VERIFY-030"
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
    "DOC-SYS-014",
    "DOC-SYS-017",
    "DOC-SYS-019",
    "DOC-SYS-020",
    "DOC-PROFILE-001",
    "DOC-PROFILE-003",
    "DOC-COMP-000",
    "DOC-LIFE-000",
    "DOC-LIFE-001",
    "DOC-LIFE-002",
    "DOC-LIFE-003",
    "DOC-LIFE-004",
    "DOC-LIFE-011"
  ],
  "tags": [
    "lifecycle",
    "artifact-verification",
    "artifact-identity",
    "integrity",
    "provenance",
    "trust",
    "compatibility",
    "quarantine",
    "verification-receipts"
  ]
}
KOA:DOC-META:END -->

# Artifact Verification

## 1. Purpose

This document defines the common verification model for kOA release artifacts.

Artifact verification determines whether one exact artifact is structurally valid, correctly identified, intact, sufficiently traceable, trusted for its declared purpose, compatible with a target, and eligible for a later lifecycle transition.

Verification is distinct from publication, distribution, installation, import, migration, staging, and activation. A verified result supports those later decisions but does not perform them.

The model applies common checks across artifact classes while leaving class-specific structure, claims, activation behavior, and recovery behavior to the applicable artifact and component contracts.

## 2. Scope

This document applies to:

- every artifact registered in an active artifact class;
- artifacts in the system, services, governance, and knowledge release channels;
- Release Sets;
- system images, service artifacts, policy bundles, Runtime Packs, Kristal artifacts, compiled language packs, Ariane artifacts, offline bundles, sovereignty bundles, and other registered artifact classes;
- artifacts received from repositories, mirrors, removable media, offline transfer, control planes, build systems, or local publication workflows;
- verification before publication, import, installation, staging, migration, activation, rollback, recovery, or conformance claims;
- artifact identity, schema, class, channel, integrity, provenance, trust, compatibility, authorization, quarantine, revocation, receipts, tests, and evidence.

This document does not:

- define the structure of an individual artifact class;
- assign artifact-class or release-channel membership manually in prose;
- make a successful verification result an activation decision;
- prescribe one digest algorithm, signature scheme, trust store, transparency system, package manager, scanner, or verification tool globally;
- permit verification tools to mutate application-owned authoritative data;
- replace profile-specific assurance and offline-transfer rules;
- replace artifact-owner activation, migration, rollback, or forward-repair contracts.

## 3. Canonical References

| Canonical reference | Ownership role |
| --- | --- |
| `contracts/artifact-classes.contract.json` | Owns artifact-class identity, canonical owner, release-channel membership, and class-level lifecycle properties. |
| `generated/artifact-catalog.json` | Owns artifact-contract catalog membership, paths, active versions, and lifecycle status. |
| `contracts/artifact-contracts/*.schema.json` | Owns artifact structure, required claims, integrity scope, and artifact-specific validation rules. |
| `contracts/release-channels.contract.json` | Owns the system, services, governance, and knowledge channel identities and membership rules. |
| `contracts/artifact-contracts/release-set.schema.json` | Owns the Release Set structure and compatibility evidence fields. |
| `generated/component-catalog.json` and component contracts | Own target admission, artifact use, activation, migration, and recovery boundaries. |
| `contracts/profiles/*.profile.json` | Owns profile-specific trust, assurance, offline-transfer, hardware, and evidence requirements. |
| `contracts/components/identity-and-trust.component.json` | Owns identity, credential, signature, trust-root, and revocation verification services. |
| `contracts/components/governance-policy-runtime.component.json` | Owns policy authorization and governed-exception decisions when required. |
| `contracts/components/resource-governor.component.json` | Owns resource admission and limits for verification work. |
| `generated/requirements-index.json` | Owns the normative statements displayed in Section 5. |
| `generated/assertion-index.json` | Owns activation, recovery, Release Set, channel, data-authority, profile, and canonical-ownership assertions. |
| `generated/traceability.json` | Owns decision, requirement, lock, test, artifact, profile, and evidence relationships. |
| `generated/test-catalog.json` and `generated/evidence-catalog.json` | Own verification test and evidence identities. |

This Markdown document explains verification behavior. Canonical artifact claims and exact verification fields remain in machine-readable contracts.

## 4. Model and Responsibilities

### 4.1 Verification subject

The verification subject is one immutable artifact instance.

It is identified by:

- canonical artifact identity;
- artifact version;
- artifact class;
- integrity claim;
- release channel;
- source or custody reference;
- applicable artifact-contract version.

Two files with the same display name are not the same verification subject unless their canonical identity and required integrity claims agree.

### 4.2 Verification context

A verification result is valid only within its recorded context.

The context includes:

- target component, node, deployment, or publication boundary;
- effective profile and overlays;
- active artifact contract;
- active release-channel contract;
- trust roots and trust policy;
- revocation information;
- compatibility inputs;
- required Release Set;
- verifier identity and version;
- applicable policy authorization;
- verification time.

A change to a context element can require re-evaluation even when the artifact bytes remain unchanged.

### 4.3 Common verification layers

| Layer | Question answered |
| --- | --- |
| Envelope | Can the artifact be safely parsed as the declared artifact class? |
| Identity | Does the artifact identify the expected canonical object and version? |
| Class | Does the active artifact-class registry permit this classification? |
| Channel | Does the artifact belong to the declared release channel? |
| Integrity | Do recalculated digests match the declared integrity scope? |
| Provenance | Can the declared producer, source, build or assembly path, and custody be resolved? |
| Trust | Are required credentials and signatures valid for this purpose and context? |
| Compatibility | Can this artifact operate with the target, profile, data state, and selected artifacts? |
| Authorization | Is the requested later use permitted where policy evaluation applies? |
| Class-specific | Do additional checks declared by the artifact contract pass? |
| Evidence | Is the verification result complete, reproducible, and traceable? |

Passing one layer does not imply that another layer passed.

### 4.4 Outcome model

| Outcome | Meaning |
| --- | --- |
| `verified` | Every required check completed successfully for the recorded context |
| `failed` | At least one completed check contradicted an active requirement |
| `blocked` | At least one required check or authority could not be resolved or executed |
| `quarantined` | The artifact is isolated from ordinary use pending rejection, inspection, or a new valid verification |
| `revoked` | Active revocation policy prohibits new activation or use |

A result can include detailed sub-results while exposing one final outcome.

### 4.5 Verification receipt

A verification receipt records:

- receipt identity;
- artifact identity, version, class, channel, and integrity claim;
- source and target;
- artifact-contract version;
- verifier identity and version;
- effective profile and overlays;
- trust and revocation context;
- compatibility context;
- policy references when applicable;
- individual check outcomes;
- final outcome;
- time;
- evidence references;
- redaction or disclosure classification.

The receipt is evidence of a verification decision. It is not the artifact and does not replace the artifact owner's active-state record.

### 4.6 Integrity model

Integrity scope is artifact-contract owned.

The scope can cover:

- exact file bytes;
- a canonical serialized representation;
- a manifest and its members;
- an archive entry set;
- a filesystem image;
- a content-addressed object graph;
- another deterministic scope declared by the artifact contract.

The verifier recalculates required digests over that scope. A digest copied from the same untrusted source without recomputation does not establish integrity.

### 4.7 Provenance and trust

Provenance answers where the artifact came from and how it was produced or assembled.

Trust answers whether the identities and credentials associated with that provenance are authorized for the declared artifact, channel, purpose, and target.

A provenance chain can be complete but untrusted. A signature can be cryptographically valid but outside its authorized scope. Both dimensions are evaluated independently.

### 4.8 Compatibility

Compatibility is target-specific.

The verifier can consider:

- system and runtime versions;
- component contracts;
- artifact dependencies;
- release-channel combinations;
- effective profile and overlays;
- hardware or platform constraints when profile-owned;
- data-schema and migration state;
- downgrade and substitution policy;
- required Release Set;
- deprecation and revocation state.

Compatibility evidence identifies the tests, constraints, or accepted matrices used to reach the result.

### 4.9 Result reuse

A stored result can avoid repeated work only when its complete verification context remains equivalent.

Result reuse ends when:

- artifact content or digest changes;
- artifact-contract semantics change;
- verifier semantics change;
- trust roots or trust policy change;
- revocation information changes;
- target or profile changes;
- compatibility inputs change;
- required authorization expires or changes;
- the reuse period declared by the active contract ends.

### 4.10 Safe verification execution

Verification treats artifact input as untrusted until the required checks pass.

Parsing, extraction, canonicalization, metadata reading, signature verification, and class-specific inspection use bounded resources and declared failure behavior.

Embedded code, scripts, macros, plugins, migration logic, and active content remain disabled unless an isolated artifact-specific verification contract explicitly requires controlled execution.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-LIFE-VERIFY-001,REQ-LIFE-VERIFY-002,REQ-LIFE-VERIFY-003,REQ-LIFE-VERIFY-004,REQ-LIFE-VERIFY-005,REQ-LIFE-VERIFY-006,REQ-LIFE-VERIFY-007,REQ-LIFE-VERIFY-008,REQ-LIFE-VERIFY-009,REQ-LIFE-VERIFY-010,REQ-LIFE-VERIFY-011,REQ-LIFE-VERIFY-012,REQ-LIFE-VERIFY-013,REQ-LIFE-VERIFY-014,REQ-LIFE-VERIFY-015,REQ-LIFE-VERIFY-016,REQ-LIFE-VERIFY-017,REQ-LIFE-VERIFY-018,REQ-LIFE-VERIFY-019,REQ-LIFE-VERIFY-020,REQ-LIFE-VERIFY-021,REQ-LIFE-VERIFY-022,REQ-LIFE-VERIFY-023,REQ-LIFE-VERIFY-024,REQ-LIFE-VERIFY-025,REQ-LIFE-VERIFY-026,REQ-LIFE-VERIFY-027,REQ-LIFE-VERIFY-028,REQ-LIFE-VERIFY-029,REQ-LIFE-VERIFY-030 -->
- **REQ-LIFE-VERIFY-001 — SHALL:** Every artifact verification evaluates one immutable artifact instance identified by its canonical artifact identity, version, class, and integrity claim.
- **REQ-LIFE-VERIFY-002 — SHALL:** Verification resolves the active artifact contract and validates the artifact structure before interpreting artifact-specific claims.
- **REQ-LIFE-VERIFY-003 — SHALL:** Verification confirms that the artifact class and release channel agree with the active artifact-class and release-channel contracts.
- **REQ-LIFE-VERIFY-004 — SHALL NOT:** An artifact is treated as valid for a class or release channel based only on its filename, location, extension, transport, repository, or operator description.
- **REQ-LIFE-VERIFY-005 — SHALL:** Integrity verification recalculates every required digest over the exact byte or canonical-content scope declared by the artifact contract.
- **REQ-LIFE-VERIFY-006 — SHALL NOT:** A digest, checksum, signature, or manifest claim is accepted when its algorithm, scope, encoding, referenced object, or expected value is unresolved.
- **REQ-LIFE-VERIFY-007 — SHALL:** Provenance verification resolves the artifact producer, build or assembly process, source references, toolchain or generator identity when applicable, and custody history required by the artifact contract.
- **REQ-LIFE-VERIFY-008 — SHALL:** Trust verification validates required signatures, credentials, trust roots, validity intervals, revocation state, and authorization scope against the target verification context.
- **REQ-LIFE-VERIFY-009 — SHALL NOT:** A cryptographically valid signature is interpreted as artifact authorization beyond the signer's declared trust and release scope.
- **REQ-LIFE-VERIFY-010 — SHALL:** Compatibility verification evaluates the artifact against the target component, active system state, effective profile, selected overlays, required release channels, data-schema state, and applicable Release Set.
- **REQ-LIFE-VERIFY-011 — SHALL NOT:** A newer version, successful download, successful installation, successful parsing, or successful startup substitutes for compatibility verification.
- **REQ-LIFE-VERIFY-012 — SHALL:** Profile-specific trust, signing, offline-transfer, hardware, assurance, and evidence checks are applied only when the effective profile or overlay requires them.
- **REQ-LIFE-VERIFY-013 — SHALL:** Verification distinguishes verified, failed, blocked, quarantined, and revoked outcomes.
- **REQ-LIFE-VERIFY-014 — SHALL:** A failed outcome identifies at least one completed check whose result contradicts an active artifact, integrity, provenance, trust, compatibility, or policy requirement.
- **REQ-LIFE-VERIFY-015 — SHALL:** A blocked outcome identifies a required check, authority, contract, key, revocation source, compatibility source, or validation tool that could not be resolved or executed.
- **REQ-LIFE-VERIFY-016 — SHALL:** A quarantined outcome prevents installation, execution, import, publication, and activation outside the explicit quarantine-inspection contract.
- **REQ-LIFE-VERIFY-017 — SHALL:** A revoked outcome prevents new activation and applies the active replacement, recovery, or removal policy while preserving historical identity and evidence.
- **REQ-LIFE-VERIFY-018 — SHALL NOT:** A failed, blocked, quarantined, or revoked artifact becomes active through operator convenience, fallback search, alternate mirror selection, or silent substitution.
- **REQ-LIFE-VERIFY-019 — SHALL:** A verification result records the artifact identity, integrity claim, artifact contract version, verifier identity and version, verification time, target, effective profile, trust context, compatibility context, individual check outcomes, and final outcome.
- **REQ-LIFE-VERIFY-020 — SHALL:** A cached verification result is reusable only when the artifact bytes or canonical content, artifact contract, verifier, trust context, revocation context, target, profile, compatibility context, and required policy are unchanged.
- **REQ-LIFE-VERIFY-021 — SHALL:** Verification is repeated after transfer when the transfer, storage, extraction, repackaging, canonicalization, or materialization process can alter the verified integrity scope.
- **REQ-LIFE-VERIFY-022 — SHALL:** Offline bundle verification validates the bundle identity, manifest completeness, contained artifact identities, integrity relationships, provenance, trust, compatibility, and authorization before contained artifacts leave quarantine.
- **REQ-LIFE-VERIFY-023 — SHALL:** Artifact-specific validation checks declared by the active artifact contract are completed in addition to the common verification checks.
- **REQ-LIFE-VERIFY-024 — SHALL NOT:** Artifact verification executes unverified artifact code, migration logic, policy logic, macros, plugins, or embedded active content outside an isolated verification contract.
- **REQ-LIFE-VERIFY-025 — SHALL:** Verification tools operate with bounded resources, bounded input handling, declared failure behavior, and no mutation authority over component-owned application data.
- **REQ-LIFE-VERIFY-026 — SHALL:** Verification evidence and receipts disclose only the information required for traceability and conformance while protecting secret values, private keys, restricted source information, and sensitive artifact content.
- **REQ-LIFE-VERIFY-027 — SHALL:** Verification completion does not publish, install, import, migrate, stage, or activate the artifact unless a separate active contract explicitly performs that transition.
- **REQ-LIFE-VERIFY-028 — SHALL:** Every activation revalidates or references a still-valid verification result whose context covers the exact target activation request.
- **REQ-LIFE-VERIFY-029 — SHALL:** A semantic change to verification checks, trust interpretation, digest scope, outcome semantics, quarantine behavior, or result-reuse policy is accepted and validated before activation.
- **REQ-LIFE-VERIFY-030 — SHALL:** Every active artifact-verification requirement is traceable to accepted decisions, applicable locks, validation tests, and required evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Receiving an artifact

Artifact intake:

1. records source, transport, claimed identity, and claimed class;
2. places the artifact in an unverified or quarantine location;
3. prevents ordinary installation, execution, import, and activation;
4. selects the expected artifact contract from trusted canonical metadata;
5. creates a verification request and context identity;
6. begins common and class-specific checks.

Claims inside the artifact do not select their own authority without external canonical confirmation.

### 6.2 Performing common verification

The verifier:

1. safely parses the artifact envelope;
2. validates schema and required fields;
3. resolves identity, version, class, and channel;
4. recalculates required integrity claims;
5. verifies provenance;
6. verifies credentials, signatures, trust roots, validity, and revocation where required;
7. evaluates compatibility with the recorded target context;
8. resolves applicable policy authorization;
9. runs artifact-specific checks;
10. records every check result;
11. determines the final outcome;
12. emits the verification receipt.

### 6.3 Verifying after transfer

After transfer or materialization:

1. identifies the integrity scope verified before transfer;
2. determines whether transport, extraction, repackaging, canonicalization, storage, or installation changed that scope;
3. recalculates required digests on the target representation;
4. re-evaluates changed trust, revocation, profile, or compatibility context;
5. emits a target-side result;
6. keeps the artifact inactive until later lifecycle prerequisites pass.

### 6.4 Verifying an offline bundle

Offline bundle verification:

1. validates the bundle envelope and identity;
2. validates manifest completeness;
3. enumerates every contained artifact;
4. verifies manifest-to-artifact integrity relationships;
5. verifies bundle and artifact provenance and trust;
6. evaluates target profile and offline-import authorization;
7. verifies compatibility and Release Set relationships;
8. quarantines the complete bundle when a required relationship is invalid or ambiguous;
9. emits bundle-level and artifact-level receipts.

### 6.5 Reusing a verification result

Before reuse:

1. resolve the stored receipt;
2. match the exact artifact identity and integrity claim;
3. match the artifact-contract and verifier versions;
4. match the target, profile, trust, revocation, compatibility, and policy context;
5. confirm that the result remains within its declared reuse period;
6. reuse only the checks whose context remains unchanged;
7. rerun all invalidated checks;
8. emit a new decision or an explicit reuse receipt.

### 6.6 Handing off to activation

Verification handoff:

1. exposes the verified artifact and receipt through an active lifecycle contract;
2. keeps the artifact staged but inactive;
3. allows the activating owner to revalidate receipt scope and freshness;
4. obtains activation-specific authorization and resource admission;
5. performs migration and activation only through the owner contract;
6. records activation separately from verification.

## 7. Failure States and Safe Degradation

| Failure condition | Required response | Preserved state | Blocked or degraded behavior | Evidence |
| --- | --- | --- | --- | --- |
| Artifact contract cannot be resolved | Return `blocked` and retain quarantine | Existing active artifacts | Artifact interpretation and use | Contract-resolution record |
| Envelope cannot be parsed safely | Return `failed` and retain quarantine | Existing active artifacts | Further ordinary processing | Parse failure |
| Claimed identity conflicts with expected identity | Return `failed` | Expected target identity | Candidate use | Identity mismatch |
| Artifact class or channel is invalid | Return `failed` | Canonical class and channel mappings | Publication, installation, or activation | Classification result |
| Digest mismatch occurs | Return `failed` and quarantine | Existing valid artifacts | Candidate use | Integrity report |
| Digest scope is ambiguous | Return `blocked` | Existing valid artifacts | Integrity claim | Scope-resolution report |
| Provenance is incomplete | Return `failed` or `blocked` according to the missing claim and contract | Existing trusted artifacts | Candidate use | Provenance result |
| Required signer or trust root is invalid | Return `failed` | Existing trusted state | Candidate use | Trust result |
| Revocation source is unavailable | Return `blocked` when revocation checking is required | Existing active state | Candidate activation | Revocation-source status |
| Credential or artifact is revoked | Return `revoked` | Historical identity and evidence | New activation or adoption | Revocation receipt |
| Compatibility is false | Return `failed` | Last compatible artifact set | Candidate activation | Compatibility report |
| Compatibility source is unavailable | Return `blocked` | Last compatible artifact set | Candidate activation | Compatibility-source status |
| Verification tool fails | Return `blocked`; do not interpret the check as passed | Previous valid verification results within scope | New verification decision | Tool failure |
| Resource limit is reached | Stop the affected check safely and return `blocked` or `failed` according to the contract | Verifier and host integrity | Unbounded processing | Resource-limit evidence |
| Active content attempts execution | Reject or isolate according to the artifact contract | Verification environment | Embedded execution | Active-content incident |
| Evidence path is unavailable | Apply the declared synchronous-fail or bounded-queue rule | Source verification state | Result requiring unavailable mandatory evidence | Evidence-path state |
| Cached result context differs | Invalidate affected cached checks | Unchanged reusable checks | Stale result reuse | Context comparison |
| Offline bundle member is missing | Quarantine the bundle | Current local release state | Bundle import and member activation | Bundle completeness report |

## 8. Cross-Component Interactions

### 8.1 Artifact source and channel authority

The source supplies the artifact and its claims.

The channel authority confirms channel membership and publication status. Neither source location nor channel storage substitutes for independent target verification.

### 8.2 Identity and Trust

Identity and Trust verifies credentials, signatures, trust roots, authorization scope, validity intervals, and revocation state.

The artifact verifier consumes those results and records their context. It does not broaden the signer's authority.

### 8.3 Artifact owner and activating component

The artifact owner defines class-specific claims and compatibility.

The target component or lifecycle authority admits and activates the artifact. Verification does not mutate the target component's authoritative state.

### 8.4 Governance Policy Runtime

The Governance Policy Runtime evaluates policy authorization and governed exceptions when required by the effective profile or transition.

Policy approval does not establish integrity or compatibility and does not perform activation.

### 8.5 Resource Governor

The Resource Governor bounds CPU, memory, I/O, processes, queues, time, and concurrency used by verification.

Resource admission does not establish artifact trust or authorization.

### 8.6 Evidence authority

The evidence authority preserves verification receipts and authorized views.

It does not rewrite the artifact, verification decision, target activation state, or source provenance.

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Effect |
| --- | --- |
| `DEC-REL-001` | Establishes four release channels, Release Sets, independent compatible updates, and owner-controlled artifact activation. |
| `DEC-DATA-001` | Preserves component data ownership and prohibits verification or lifecycle shortcuts that write directly across component boundaries. |
| `DEC-PROFILE-001` | Keeps profile-specific trust, assurance, hardware, offline-transfer, and evidence checks within explicit profile scope. |

### Prohibited assumptions

- a file is valid because it came from a known URL, mirror, registry, removable device, or operator;
- a filename or extension proves artifact class;
- a matching checksum copied from the same source proves integrity;
- a valid signature proves authorization for every artifact, channel, profile, and target;
- complete provenance automatically establishes trust;
- trust automatically establishes compatibility;
- successful parsing establishes safety;
- successful installation establishes verification;
- successful startup establishes compatibility;
- the newest artifact is the correct artifact;
- a verification receipt remains valid after trust, revocation, profile, target, contract, or verifier changes;
- quarantine is an activation state;
- operator approval can silently override a failed or blocked check;
- verification can execute embedded active content without isolation;
- verification can mutate component-owned application data;
- a profile-specific signature or hardware rule applies globally;
- missing revocation or compatibility data can be treated as success;
- a Release Set eliminates artifact-level verification.

## 10. Validation Criteria

This document is conformant when:

1. `DOC-LIFE-012` is active at `06-lifecycle/12-artifact-verification.md`.
2. Every canonical reference resolves.
3. Every listed decision exists with status `accepted`.
4. Every requirement in Section 5 exists with identical strength, statement, scope, owner, source decision, and validation mapping.
5. Every listed lock exists and is active.
6. Every active artifact class resolves one active artifact contract and one canonical release channel.
7. Every verification request identifies one immutable artifact instance and one complete verification context.
8. Envelope and schema validation occurs before artifact-specific claim interpretation.
9. Identity, class, channel, integrity, provenance, trust, compatibility, policy, and class-specific checks produce separate recorded outcomes.
10. Required digests are recalculated over the contract-owned integrity scope.
11. Required signatures and credentials are evaluated for trust scope, validity, and revocation.
12. Compatibility includes the target, effective profile, data state, selected artifacts, and Release Set where applicable.
13. Final outcomes are limited to `verified`, `failed`, `blocked`, `quarantined`, and `revoked`.
14. Failed, blocked, quarantined, and revoked artifacts cannot proceed through ordinary activation paths.
15. Verification receipts contain the complete context and individual check outcomes.
16. Cached-result reuse fails when any required context element changes.
17. Target-side re-verification occurs when transfer or materialization can change the integrity scope.
18. Offline bundle verification validates manifest completeness and all contained-artifact relationships.
19. Verification does not execute unverified active content outside an isolated declared contract.
20. Verification tools have bounded resources and no component-data mutation authority.
21. Receipts and logs protect secrets, private keys, restricted provenance, and sensitive artifact content.
22. Verification completion remains separate from publication, installation, import, migration, and activation.
23. Every activation references a still-valid result covering the exact target request.
24. Critical verification decisions map to tests and evidence.
25. Profile-specific controls remain profile-scoped.
26. Active prose is English and contains no unresolved-authority marker.
27. No normative keyword appears outside the generated requirement block.
28. The documentation dependency graph remains acyclic.

The validation entry point is:

`bash
python docs/tools/validate_docs.py
`

## 11. Non-Normative Examples

> **Non-normative example:** This example illustrates independent integrity verification.

A node downloads a Runtime Pack and a digest file from the same mirror. The node recalculates the Runtime Pack digest and compares it with a trusted manifest rather than treating the downloaded digest file alone as proof.

> **Non-normative example:** This example illustrates scoped signature trust.

A signature can be valid for a development artifact repository but not authorized for a sovereign production release channel. Cryptographic validity and release authorization are evaluated separately.

> **Non-normative example:** This example illustrates context invalidation.

A service artifact can remain byte-for-byte unchanged while a required dependency is revoked. The previous compatibility result no longer covers the new target context and is reevaluated.

> **Non-normative example:** This example illustrates verification and activation separation.

A language pack can be verified and staged while the current pack remains active. SemantiK Architect Runtime changes its active state only through its separate atomic activation contract.

> **Non-normative example:** This example illustrates offline quarantine.

An offline bundle with one missing manifest member remains quarantined as a complete bundle. Valid-looking members do not leave quarantine through an implicit partial import.
