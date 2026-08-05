<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-LIFE-018",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "lifecycle",
  "scope": [
    "global",
    "supply_chain:sbom",
    "supply_chain:provenance",
    "supply_chain:signing"
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
    "DEC-DEV-001",
    "DEC-COMP-001",
    "DEC-DATA-001",
    "DEC-AI-001",
    "DEC-HW-001"
  ],
  "requirement_ids": [
    "REQ-LIFE-SUPPLY-001",
    "REQ-LIFE-SUPPLY-002",
    "REQ-LIFE-SUPPLY-003",
    "REQ-LIFE-SUPPLY-004",
    "REQ-LIFE-SUPPLY-005",
    "REQ-LIFE-SUPPLY-006",
    "REQ-LIFE-SUPPLY-007",
    "REQ-LIFE-SUPPLY-008",
    "REQ-LIFE-SUPPLY-009",
    "REQ-LIFE-SUPPLY-010",
    "REQ-LIFE-SUPPLY-011",
    "REQ-LIFE-SUPPLY-012",
    "REQ-LIFE-SUPPLY-013",
    "REQ-LIFE-SUPPLY-014",
    "REQ-LIFE-SUPPLY-015",
    "REQ-LIFE-SUPPLY-016",
    "REQ-LIFE-SUPPLY-017",
    "REQ-LIFE-SUPPLY-018",
    "REQ-LIFE-SUPPLY-019",
    "REQ-LIFE-SUPPLY-020",
    "REQ-LIFE-SUPPLY-021",
    "REQ-LIFE-SUPPLY-022",
    "REQ-LIFE-SUPPLY-023",
    "REQ-LIFE-SUPPLY-024",
    "REQ-LIFE-SUPPLY-025",
    "REQ-LIFE-SUPPLY-026",
    "REQ-LIFE-SUPPLY-027",
    "REQ-LIFE-SUPPLY-028",
    "REQ-LIFE-SUPPLY-029",
    "REQ-LIFE-SUPPLY-030",
    "REQ-LIFE-SUPPLY-031",
    "REQ-LIFE-SUPPLY-032",
    "REQ-LIFE-SUPPLY-033",
    "REQ-LIFE-SUPPLY-034",
    "REQ-LIFE-SUPPLY-035",
    "REQ-LIFE-SUPPLY-036"
  ],
  "lock_ids": [
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-AUTH-001",
    "LOCK-AUTH-002",
    "LOCK-AUTH-003",
    "LOCK-AUTH-004",
    "LOCK-DATA-001",
    "LOCK-COMP-001",
    "LOCK-AI-002",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
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
    "DOC-SYS-001",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-007",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-017",
    "DOC-SYS-019",
    "DOC-PROF-011",
    "DOC-DEV-005",
    "DOC-DEV-015"
  ],
  "tags": [
    "sbom",
    "provenance",
    "signing",
    "attestation",
    "supply-chain",
    "build-materials",
    "software-bill-of-materials",
    "key-custody",
    "trust-roots",
    "revocation",
    "reproducible-builds",
    "offline-verification"
  ]
}
KOA:DOC-META:END -->

# SBOM, Provenance, and Signing

## 1. Purpose

This document defines the kOA lifecycle for software bills of materials, build and creation provenance, attestations, signatures, signing keys, trust roots, and supply-chain verification.

The lifecycle connects exact source and material identities to an exact artifact and then preserves the statements and evidence used to verify, publish, release, import, activate, revoke, export, and restore that artifact.

It separates:

- an SBOM from a vulnerability or license decision;
- provenance from publication approval;
- an attestation from the truth of every possible claim;
- a signature from compatibility or activation authority;
- builder identity from signer identity;
- signer identity from release authority;
- key identity from artifact identity;
- trust roots from network location;
- technical integrity from ordinary documentation validation.

Exact formats and algorithms remain owned by artifact-class, schema, profile, and security contracts.

## 2. Scope

This document applies to:

- software and service artifacts;
- system images and recovery artifacts;
- container or equivalent runtime artifacts;
- governance policy bundles;
- compiled language artifacts;
- Kristal Runtime Packs;
- Ariane Atlases and drivers;
- migration and schema artifacts;
- build manifests;
- release manifests;
- Release Sets;
- software bills of materials;
- provenance attestations;
- signature envelopes;
- signing certificates and trust bundles;
- verification reports;
- offline release bundles;
- supply-chain evidence;
- revoked, superseded, archived, exported, restored, and mirrored artifacts.

It applies to developer workstations, build farms, controlled build workers, signing environments, hardware-backed key stores, repositories, mirrors, hubs, control planes, sovereign offline nodes, and clean-room restore environments.

It does not define:

- one mandatory SBOM standard;
- one mandatory provenance-envelope standard;
- one mandatory signature algorithm;
- one mandatory certificate authority;
- one mandatory transparency-log product;
- one mandatory hardware security module;
- exact profile topology;
- component business-data provenance;
- user-interface display;
- ordinary Markdown content hashing;
- private-to-public application-content disclosure.

Those details remain with canonical schemas, artifact classes, profiles, security documents, component contracts, and implementation recipes.

## 3. Canonical References

| Canonical reference | Ownership |
| --- | --- |
| `contracts/artifact-classes.contract.json` | Per-class SBOM, provenance, integrity, signature, verification, publication, activation, rollback, revocation, retention, and evidence requirements. |
| `contracts/release-channels.contract.json` | Channel-specific publication, signing, compatibility, revocation, and release rules. |
| `generated/authority-manifest.json` | Active authority release, canonical registries, signing and activation order, and cutover state. |
| `generated/decision-index.json` | Accepted supply-chain, lifecycle, authority, identity, profile, and development decisions. |
| `contracts/profiles/*.profile.json` | Build-worker isolation, signing topology, key hardware, repository placement, mirrors, offline trust bundles, resources, and network exposure. |
| `generated/component-catalog.json` | Runtime owners, component boundaries, and artifact-producing or consuming responsibilities. |
| `contracts/components/*.component.json` | Component-specific artifact inputs, outputs, verification, runtime admission, activation, rollback, and evidence. |
| `contracts/integration-types.contract.json` | External package sources, repositories, mirrors, signing services, and external candidate boundaries. |
| `schemas/sbom.schema.json` | Canonical SBOM structure and validation vocabulary. |
| `schemas/provenance-attestation.schema.json` | Canonical provenance and attestation structure. |
| `schemas/signature-envelope.schema.json` | Canonical signature-envelope structure. |
| `schemas/artifact-manifest.schema.json` | Artifact identity, inventory, compatibility, and lifecycle manifest. |
| `schemas/release-manifest.schema.json` | Exact channel-release membership and release evidence. |
| `schemas/release-set.schema.json` | Compatible cross-channel selection and target scope. |
| `generated/requirements-index.json` | Requirement statements displayed in section 5. |
| `generated/assertion-index.json` | Lifecycle, signing, key, authority, profile, development, and ownership invariants. |
| `generated/traceability.json` | Source, material, builder, artifact, SBOM, provenance, signature, release, test, evidence, exception, and claim relationships. |
| `generated/exception-index.json` | Approved bounded deviations and compensating controls. |
| `generated/test-catalog.json` | Supply-chain, security, lifecycle, operations, profile, exit, and documentation tests. |
| `generated/evidence-catalog.json` | Executed build, verification, approval, signing, publication, activation, revocation, recovery, and restore evidence. |
| `02-system/19-release-and-artifact-identity.md` | Global artifact, release, Release Set, verification, activation, and revocation identity. |
| `05-development/15-artifact-publication.md` | Candidate verification, approval, signing, repository publication, and release publication process. |

## 4. Model and Responsibilities

### 4.1 Supply-chain graph

The supply-chain graph is:

`text
source and material identities
-> controlled build or creation
-> immutable subject artifact
-> SBOM
-> provenance attestation
-> verification report
-> review and approval
-> signature when required
-> publication and release evidence
-> target verification
-> independent activation
`

Every node has its own identity.

Every edge has an explicit relationship rather than an inferred filename or directory relationship.

### 4.2 SBOM model

An SBOM describes the composition of one exact subject.

A release-grade software SBOM can contain:

- SBOM identity and schema version;
- subject artifact or release identity;
- creator and creation context;
- component identity;
- component name and version;
- supplier or publisher when known;
- package, content, or repository identities;
- source relationship;
- direct and transitive dependency relationships;
- vendored and embedded relationships;
- base-image and runtime-layer relationships;
- license declarations and detected license evidence;
- integrity values required by the artifact class;
- external references;
- known unknowns and omissions;
- provenance and verification references.

The artifact class defines which fields and component categories apply.

### 4.3 SBOM completeness

Completeness is evaluated against the actual subject.

Possible comparison sources include:

- resolved dependency locks;
- package-manager state;
- compiled binary inventory;
- packaged archive inventory;
- container or filesystem layers;
- vendored source directories;
- generated assets;
- base artifacts;
- firmware or plugin inventory;
- runtime dependency declarations;
- artifact manifest.

Declared dependencies alone do not prove packaged composition.

### 4.4 SBOM interpretation boundary

An SBOM is evidence about composition.

Separate processes decide:

- vulnerability exposure;
- exploitability;
- license compatibility;
- policy acceptance;
- operational risk;
- profile compatibility;
- release approval;
- target activation.

A vulnerability database can change without changing the artifact or SBOM identity. A new analysis result links to the existing subject.

### 4.5 Provenance model

Provenance states how one subject was created.

A release-grade provenance statement can include:

- subject identity;
- source and material identities;
- dependency-lock identities;
- build definition;
- toolchain and compiler identities;
- builder workload, node, tenant, and environment identities;
- profile and platform;
- declared parameters;
- network-use state;
- mutable external input state;
- secret-use classification without secret disclosure;
- manual-step declarations;
- start, completion, or monotonic sequence context;
- output identities;
- test and evidence references;
- reproducibility context;
- limitations and unresolved conditions.

Provenance remains useful when the build is not fully hermetic, provided the non-hermetic inputs are explicit.

### 4.6 Attestation model

An attestation is one identified issuer's statement about one identified subject.

Examples include:

- build provenance;
- SBOM generation;
- vulnerability scan result;
- license analysis;
- reproducibility comparison;
- test completion;
- review approval;
- repository acceptance;
- release publication;
- activation verification.

Each attestation declares its predicate and scope.

An attestation is not treated as a universal statement about the subject.

### 4.7 Reproducible builds

Reproducibility compares independently executed builds from the same declared inputs.

The comparison distinguishes:

- byte-identical output;
- artifact-class content identity equivalence;
- normalized comparison;
- expected nondeterministic fields;
- unexplained difference;
- incomplete comparison.

The artifact class or assurance profile determines the required result.

An unexplained difference does not retain the original immutable identity.

### 4.8 Role separation

| Role | Supply-chain responsibility | Boundary |
| --- | --- | --- |
| Source owner | Approves or maintains source inputs. | Source control does not grant release signing. |
| Builder or creator | Produces the subject from fixed inputs. | Build completion does not grant publication. |
| SBOM generator | Creates composition evidence for the subject. | It does not approve licenses or vulnerabilities. |
| Provenance attester | Attests to the declared build or creation statement. | It does not grant release or activation authority. |
| Verifier | Validates subject, SBOM, provenance, signatures, compatibility, and evidence. | It does not mutate the subject. |
| Reviewer | Evaluates risk, policy, exception, and release suitability. | It does not replace cryptographic verification. |
| Signer | Signs one exact declared subject or statement. | A signature does not activate the artifact. |
| Publisher | Transfers an approved subject to a repository or channel. | Repository access is not signing authority. |
| Release authority | Approves one release within a declared channel and scope. | It does not activate every target. |
| Activation authority | Approves one target activation. | It does not rewrite prior attestations. |
| Trust-root authority | Issues, delegates, rotates, or revokes trust. | Trust-root authority is scoped rather than universal. |
| Runtime owner | Independently verifies and activates compatible artifacts. | It does not replace published evidence. |

### 4.9 Signature model

A signature envelope binds:

- the exact subject or statement;
- signature-envelope version;
- signer identity;
- key or certificate identity;
- issuing trust chain;
- purpose and scope;
- algorithm class;
- creation context;
- expiry or sequence context when applicable;
- verification material;
- evidence references.

The signed subject can be:

- an artifact;
- an artifact manifest;
- an SBOM;
- a provenance attestation;
- a release manifest;
- a Release Set;
- a revocation record;
- a trust-bundle update;
- an evidence bundle.

The artifact contract defines the signed unit.

### 4.10 Key classes

Key classes remain distinct.

| Key class | Typical purpose |
| --- | --- |
| System release signing | Sign system-channel artifacts or releases. |
| Services release signing | Sign services-channel artifacts or releases. |
| Governance signing | Sign governance policy bundles and governance releases. |
| Knowledge signing | Sign Kristal, language, Ariane, or other knowledge-channel artifacts. |
| Authority recognition | Sign authority or trust-recognition statements. |
| Provenance attestation | Sign build or creation provenance statements. |
| Audit anchoring | Protect audit evidence or independent evidence anchors. |
| Node and workload identity | Authenticate nodes and workloads. |
| Recovery | Authorize protected recovery or trust replacement. |

A key class cannot be substituted silently for another class.

### 4.11 Key custody

Key custody can use:

- a hardware security module;
- a hardware token;
- a platform security processor;
- a threshold or split-custody service;
- another independently validated protected mechanism.

The profile and artifact contract determine the required assurance.

Protected keys remain outside ordinary application and build environments.

Signing requests contain exact subject and approval identities rather than unrestricted arbitrary data.

### 4.12 Trust roots and certificates

Trust is scoped by:

- authority domain;
- tenant or organization;
- environment;
- release channel;
- artifact class;
- signer purpose;
- profile;
- validity period or sequence;
- delegation constraints.

Trust roots, intermediates, signer certificates, and delegations have separate identities and lifecycle records.

Network retrieval does not establish trust by itself.

### 4.13 Revocation model

Revocation can apply separately to:

- artifact;
- release;
- signer;
- signing key;
- certificate;
- issuer;
- trust root;
- attestation;
- approval;
- repository;
- build worker or builder identity.

A revocation record identifies scope, reason, effective state, authority, freshness, remediation, and evidence.

Revoking a signer does not automatically define the treatment of every previously signed artifact. The artifact class and revocation record define that effect.

### 4.14 Offline verification

An offline trust bundle can contain:

- scoped trust roots;
- required intermediates;
- signer records;
- revocation state or epoch;
- artifact and release manifests;
- SBOMs;
- provenance attestations;
- signature envelopes;
- inventories;
- verification policies;
- compatibility context;
- evidence references.

The receiving environment reports the trust and revocation freshness available at verification time.

### 4.15 Ordinary documentation boundary

Ordinary Markdown documentation is validated through identity, path, ownership, references, decisions, requirements, locks, structure, language, generated blocks, and traceability.

Supply-chain integrity controls can protect:

- a signed documentation release;
- a release archive;
- a generated site bundle;
- an exported evidence package;
- another declared release artifact.

That bundle-level protection does not create an automatic file-content-hash requirement for each ordinary Markdown source file.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-LIFE-SUPPLY-001,REQ-LIFE-SUPPLY-002,REQ-LIFE-SUPPLY-003,REQ-LIFE-SUPPLY-004,REQ-LIFE-SUPPLY-005,REQ-LIFE-SUPPLY-006,REQ-LIFE-SUPPLY-007,REQ-LIFE-SUPPLY-008,REQ-LIFE-SUPPLY-009,REQ-LIFE-SUPPLY-010,REQ-LIFE-SUPPLY-011,REQ-LIFE-SUPPLY-012,REQ-LIFE-SUPPLY-013,REQ-LIFE-SUPPLY-014,REQ-LIFE-SUPPLY-015,REQ-LIFE-SUPPLY-016,REQ-LIFE-SUPPLY-017,REQ-LIFE-SUPPLY-018,REQ-LIFE-SUPPLY-019,REQ-LIFE-SUPPLY-020,REQ-LIFE-SUPPLY-021,REQ-LIFE-SUPPLY-022,REQ-LIFE-SUPPLY-023,REQ-LIFE-SUPPLY-024,REQ-LIFE-SUPPLY-025,REQ-LIFE-SUPPLY-026,REQ-LIFE-SUPPLY-027,REQ-LIFE-SUPPLY-028,REQ-LIFE-SUPPLY-029,REQ-LIFE-SUPPLY-030,REQ-LIFE-SUPPLY-031,REQ-LIFE-SUPPLY-032,REQ-LIFE-SUPPLY-033,REQ-LIFE-SUPPLY-034,REQ-LIFE-SUPPLY-035,REQ-LIFE-SUPPLY-036 -->
- **REQ-LIFE-SUPPLY-001 — SHALL:** Every release-grade artifact identifies the applicable SBOM, provenance, integrity, signature, verification, and evidence requirements declared by its artifact-class contract.
- **REQ-LIFE-SUPPLY-002 — SHALL:** An SBOM identifies the exact subject artifact or release to which it applies and does not rely only on a project name, repository, branch, filename, or mutable tag.
- **REQ-LIFE-SUPPLY-003 — SHALL:** A release-grade software SBOM records applicable direct and transitive components, versions, suppliers or publishers when known, dependency relationships, package or content identities, licenses, and source or build relationships.
- **REQ-LIFE-SUPPLY-004 — SHALL:** The SBOM is derived from the resolved build and packaged result rather than from declared dependencies alone.
- **REQ-LIFE-SUPPLY-005 — SHALL:** Packaged libraries, vendored code, generated assets, plugins, firmware, runtime layers, base images, and other included components appear in the SBOM when their artifact-class contract makes them applicable.
- **REQ-LIFE-SUPPLY-006 — SHALL:** Unknown, unresolved, intentionally omitted, or unverifiable SBOM entries remain explicit with stable reason codes and do not disappear through silent normalization.
- **REQ-LIFE-SUPPLY-007 — SHALL:** SBOM completeness is validated against the artifact inventory, package metadata, build output, and declared artifact-class rules.
- **REQ-LIFE-SUPPLY-008 — SHALL NOT:** An SBOM is treated as a vulnerability report, license approval, compatibility decision, activation authority, or proof that the listed software is safe.
- **REQ-LIFE-SUPPLY-009 — SHALL:** Provenance identifies the exact subject artifact, source materials, dependency and toolchain identities, builder identity, build definition, parameters, environment, profile, platform, and result.
- **REQ-LIFE-SUPPLY-010 — SHALL:** Provenance records whether network access, mutable external inputs, non-hermetic tools, secrets, manual steps, or nondeterministic operations affected the build or creation process.
- **REQ-LIFE-SUPPLY-011 — SHALL:** Source revisions, lockfiles, compiler or generator versions, build scripts, base artifacts, and policy inputs used by a release-grade build remain independently resolvable.
- **REQ-LIFE-SUPPLY-012 — SHALL:** A provenance attestation binds one exact subject identity to one exact declared statement and preserves the attestation predicate, issuer, time or sequence context, scope, and evidence references.
- **REQ-LIFE-SUPPLY-013 — SHALL NOT:** A provenance attestation is interpreted as publication approval, release approval, compatibility, audience eligibility, or target activation unless its declared statement explicitly and validly covers that decision.
- **REQ-LIFE-SUPPLY-014 — SHALL:** Reproducible-build evidence is produced when required by the artifact class, profile, assurance overlay, release channel, or accepted decision.
- **REQ-LIFE-SUPPLY-015 — SHALL:** A reproducibility comparison records source and toolchain identity, controlled environment differences, expected nondeterministic fields, output comparison method, and result.
- **REQ-LIFE-SUPPLY-016 — SHALL NOT:** A rebuild with different content silently reuses the original immutable artifact identity.
- **REQ-LIFE-SUPPLY-017 — SHALL:** Builder, verifier, reviewer, attester, publisher, signer, release authority, activation authority, trust-root authority, and runtime owner remain distinct authority dimensions.
- **REQ-LIFE-SUPPLY-018 — SHALL:** Signing occurs only after required artifact, manifest, SBOM, provenance, compatibility, policy, and review checks complete.
- **REQ-LIFE-SUPPLY-019 — SHALL:** Every signature identifies the signed subject, signed statement, signature envelope, signer identity, key or certificate identity, trust scope, algorithm class, creation context, and verification requirements.
- **REQ-LIFE-SUPPLY-020 — SHALL NOT:** A valid signature alone proves artifact safety, compatibility, release approval, tenant eligibility, audience eligibility, or activation authority.
- **REQ-LIFE-SUPPLY-021 — SHALL:** Signing keys are scoped by purpose, artifact class, release channel, environment, tenant or authority domain, and permitted operation.
- **REQ-LIFE-SUPPLY-022 — SHALL NOT:** Release-signing, authority-signing, governance-signing, audit-anchoring, or recovery private keys are normally exportable to developer workspaces, ordinary build workers, application nodes, logs, caches, or support bundles.
- **REQ-LIFE-SUPPLY-023 — SHALL:** Protected signing operations use the custody, independent approval, hardware protection, threshold control, or equivalent assurance declared by the active profile and artifact contract.
- **REQ-LIFE-SUPPLY-024 — SHALL:** Key issuance, activation, delegation, rotation, expiry, suspension, revocation, archival, compromise response, and destruction remain explicit lifecycle transitions with evidence.
- **REQ-LIFE-SUPPLY-025 — SHALL:** Artifact, signer, key, certificate, issuer, trust root, attestation, and release revocations retain separate identities, scopes, reasons, effective states, and remediation effects.
- **REQ-LIFE-SUPPLY-026 — SHALL:** Offline verification uses a bounded trust bundle, scoped trust roots, known revocation or freshness state, required signatures, exact inventories, and explicit staleness reporting.
- **REQ-LIFE-SUPPLY-027 — SHALL:** Downgrade, substitution, identity collision, manifest replacement, signature stripping, attestation replacement, and trust-root substitution attempts are rejected.
- **REQ-LIFE-SUPPLY-028 — SHALL:** SBOMs, provenance attestations, signature envelopes, verification reports, and release evidence are immutable or controlled-version artifacts linked to the subject lifecycle.
- **REQ-LIFE-SUPPLY-029 — SHALL:** Critical build, verification, approval, signing, publication, import, activation, revocation, key-management, recovery, and export transitions produce classified machine-readable evidence.
- **REQ-LIFE-SUPPLY-030 — SHALL:** Export, backup, restore, mirror transfer, repository migration, and clean-room rebuild preserve or independently reconstruct artifact, SBOM, provenance, signer, trust, revocation, and evidence relationships.
- **REQ-LIFE-SUPPLY-031 — SHALL:** Restored supply-chain records are independently revalidated before supporting publication, release, activation, or conformance claims.
- **REQ-LIFE-SUPPLY-032 — SHALL:** External AI, SenTient, user imports, and external integrations remain candidate sources whose contribution is identified in provenance and admitted by the owning artifact or component contract.
- **REQ-LIFE-SUPPLY-033 — SHALL:** Profile contracts own concrete signing topology, hardware placement, repository placement, worker isolation, offline mirror, network exposure, resource limits, and orchestrator use.
- **REQ-LIFE-SUPPLY-034 — SHALL NOT:** Ordinary Markdown documentation receives a file-content-hash requirement merely because SBOM, provenance, or signing controls exist elsewhere in the lifecycle.
- **REQ-LIFE-SUPPLY-035 — SHALL:** A signed documentation or release bundle can apply integrity and signature controls at the bundle or artifact-class level without assigning an automatic hash requirement to every ordinary Markdown source file.
- **REQ-LIFE-SUPPLY-036 — SHALL:** Every active supply-chain claim has complete decision, requirement, lock, profile, component, artifact, release, SBOM, provenance, signature, test, evidence, exception, and authority traceability.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Collect build materials

1. Resolve the artifact class.
2. identify the exact source revision or source artifacts.
3. identify dependency declarations and resolved locks.
4. identify base images, runtime layers, vendored code, firmware, plugins, and generators.
5. identify build scripts, toolchains, compilers, and platform.
6. identify profile, environment, worker, and resource context.
7. freeze the material identities for the build.
8. reject unresolved mutable references required for release-grade identity.

### 6.2 Generate the SBOM

1. Identify the exact built or packaged subject.
2. inspect resolved and packaged composition.
3. collect direct, transitive, vendored, embedded, generated, base, and runtime components as applicable.
4. record versions, suppliers, identities, licenses, and relationships.
5. record explicit unknowns and omissions.
6. compare the SBOM to the artifact inventory and build materials.
7. validate the SBOM schema.
8. assign the SBOM identity.
9. link it to the subject artifact and evidence.

### 6.3 Create provenance

1. Select the exact subject artifact.
2. bind the frozen source and material identities.
3. record builder, node, workload, profile, environment, platform, and toolchain identities.
4. record build definition and parameters.
5. record network, mutable-input, secret-use, manual-step, and nondeterminism context.
6. record output identities and verification references.
7. create the provenance attestation.
8. sign the attestation when required.
9. preserve the attestation separately from the subject bytes.

### 6.4 Verify supply-chain evidence

1. Parse subject, manifest, SBOM, provenance, and signature envelopes through bounded schemas.
2. verify subject and manifest identity.
3. verify SBOM subject binding and completeness.
4. verify provenance materials, builder, toolchain, environment, and result.
5. verify signatures and trust scope.
6. verify revocation and freshness.
7. verify artifact-class and channel requirements.
8. verify compatibility, policy, exceptions, and required tests.
9. record pass, fail, blocked, or not-applicable outcomes.
10. leave the subject unchanged.

### 6.5 Perform reproducibility comparison

1. Provision an independent controlled build environment.
2. obtain the same declared source, materials, lockfiles, toolchain, and build definition.
3. run the build without reusing the original mutable workspace state.
4. generate independent SBOM and provenance evidence.
5. compare outputs under the declared comparison method.
6. classify expected nondeterministic fields.
7. record equivalent, different, incomplete, or blocked status.
8. treat unexplained differences according to the artifact-class policy.

### 6.6 Approve signing

1. Identify the exact subject and signed statement.
2. identify the required key class and signer scope.
3. verify supply-chain evidence and review results.
4. verify release channel, environment, tenant, artifact class, and expiry.
5. resolve required independent approvals.
6. bind approval to the subject, statement, key class, policy, exceptions, and replay-protection identity.
7. reject material changes after approval.

### 6.7 Sign

1. Authenticate the signing requester and protected signing service.
2. retrieve or resolve the protected key without exposing private material.
3. reverify the exact subject and approval identity.
4. create the declared signature envelope.
5. verify the resulting signature.
6. record signer, key, certificate, trust chain, purpose, scope, and time or sequence context.
7. store signing evidence.
8. return the signed statement without granting publication or activation automatically.

### 6.8 Publish and release

1. Publish the subject, manifest, SBOM, provenance, signature envelope, and required evidence atomically or through a reconciled immutable set.
2. receive durable repository acknowledgement.
3. create the exact channel-release manifest.
4. verify member identities and supply-chain evidence.
5. obtain release authority.
6. sign the release when required.
7. publish release evidence.
8. preserve the distinction between published and active state.

### 6.9 Verify at import or activation

1. Obtain the subject and required supply-chain records.
2. verify bounded inventory and artifact identity.
3. verify SBOM, provenance, signatures, trust scope, and revocation state.
4. verify channel, profile, environment, component, and compatibility.
5. verify activation authority and required evidence.
6. stage the subject.
7. activate only through the owning lifecycle procedure.
8. record verification and activation evidence separately.

### 6.10 Rotate or revoke a key

1. Identify the key class, scope, issuer, signer, affected subjects, and repositories.
2. create the rotation, suspension, compromise, or revocation record.
3. authenticate independent approvers when required.
4. activate the replacement key or trust path.
5. publish updated trust and revocation records.
6. evaluate previously signed artifacts under their artifact-class rules.
7. block unauthorized new signing.
8. update offline trust bundles and mirrors.
9. preserve historical verification evidence.
10. record remediation.

### 6.11 Export and restore

1. Export artifacts, manifests, SBOMs, provenance, signatures, trust records, revocations, releases, and evidence.
2. verify the export independently.
3. restore into a clean repository or environment.
4. preserve identities and graph relationships.
5. revalidate schemas, signatures, trust, revocation, and compatibility.
6. rebuild derived indexes and caches.
7. re-execute required verification and clean-room build checks.
8. support publication or activation claims only after revalidation.
9. record restore evidence.

## 7. Failure and Degradation

### 7.1 Incomplete SBOM

A missing required component, relationship, subject binding, inventory match, or explicit omission blocks the applicable supply-chain claim.

The artifact can remain a candidate for correction.

### 7.2 Unresolvable provenance

Missing source, lockfile, toolchain, builder, build definition, environment, material, or result identity blocks release-grade verification.

A descriptive narrative does not replace resolvable identities.

### 7.3 Signature failure

An invalid envelope, key, certificate, signer, trust chain, purpose, scope, algorithm class, or signed subject blocks the signed claim.

The verifier does not fall back to unsigned acceptance when signing is required.

### 7.4 Trust-root uncertainty

An unknown, newly fetched, expired, revoked, incorrectly scoped, or unverifiable trust root blocks the dependent verification.

Network availability does not broaden trust.

### 7.5 Key compromise

A suspected compromise triggers:

- signing suspension;
- affected key and signer revocation evaluation;
- repository and mirror notification;
- artifact and release impact analysis;
- replacement-key activation;
- re-signing or replacement where contracts permit;
- rollback or forward repair when active artifacts are affected;
- incident and recovery evidence.

### 7.6 Reproducibility failure

An unexplained output difference blocks a required reproducibility claim.

The original artifact identity remains associated only with its original bytes or artifact-class content identity.

### 7.7 Repository partial state

A subject without required manifest, SBOM, provenance, signature, or evidence remains unavailable or quarantined according to the artifact contract.

Partial records do not create a complete published claim.

### 7.8 Offline freshness uncertainty

An offline verifier exposes the trust and revocation epoch or freshness state it used.

Policy determines whether the artifact remains usable, restricted, or blocked.

Uncertainty does not disappear from evidence.

### 7.9 Evidence-store failure

Required local signing, publication, revocation, or activation evidence remains durable before the transition reports completion.

Remote forwarding can queue within explicit bounds.

### 7.10 Resource pressure

Resource controls can reduce:

- build concurrency;
- SBOM scanning concurrency;
- reproducibility workers;
- mirror replication;
- optional vulnerability reanalysis.

They preserve:

- subject integrity;
- cancellation;
- signing authorization;
- trust and revocation processing;
- critical evidence;
- rollback and recovery.

### 7.11 External-source failure

An unavailable external package source, transparency service, signing service, or analysis provider degrades only the dependent capability.

The system does not replace the source, signer, or trust root silently.

### 7.12 Restore inconsistency

A restored artifact with missing, altered, or inconsistent SBOM, provenance, signature, trust, revocation, or evidence relationships remains inactive and unsupported for release claims.

Clean restoration continues from independently verified records.

## 8. Cross-System Interactions

| Counterparty | Supply-chain interaction | Boundary |
| --- | --- | --- |
| Source control | Provides exact source and dependency-declaration identity. | It does not prove packaged composition or release approval. |
| UV and other dependency managers | Provide resolved dependency and lock identities. | A lockfile does not alone prove packaged contents. |
| Build farm | Produces subjects, SBOMs, provenance, test results, and reproducibility evidence. | Ordinary workers do not hold protected release-signing keys. |
| Artifact verifier | Validates subject, SBOM, provenance, signatures, trust, compatibility, and evidence. | Verification does not mutate or activate the subject. |
| Identity and Trust | Resolves builder, attester, signer, key, certificate, issuer, trust root, artifact, repository, environment, and revocation identity. | Identity resolution remains distinct from authorization. |
| Governance Policy Runtime | Decides signing, publication, exception, downgrade, trust replacement, and activation policy. | Policy does not expose private keys or rewrite artifacts. |
| Protected signing environment | Applies signatures under scoped key custody and approval. | It does not choose arbitrary subjects or grant target activation. |
| Artifact repository | Stores immutable subjects and supply-chain records. | Repository possession is not trust or activation authority. |
| Release authority | Approves exact channel releases. | Release approval does not activate every target. |
| Runtime owner | Verifies and activates compatible artifacts independently. | Runtime activation does not rewrite SBOM or provenance history. |
| Audit Broker | Stores classified supply-chain and key-management evidence. | Audit does not become an authorization or signing service. |
| Resource Governor | Bounds build, scanning, verification, signing queues, and recovery resources. | Resource state does not change trust or artifact identity. |
| External package or analysis provider | Supplies candidate materials or analysis. | External output remains subject to local identity, provenance, policy, and verification. |
| Offline mirror or transfer bundle | Carries immutable subjects and trust material. | Physical possession does not grant trust or activation. |

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Closed decisions

| Decision | Closed rule |
| --- | --- |
| `DEC-LIFE-001` | Supply-chain evidence follows independent system, services, governance, and knowledge release lifecycles. |
| `DEC-REL-001` | Release Set compatibility uses exact artifact and release identities and does not replace per-artifact verification. |
| `DEC-ART-001` | Artifact-class contracts own applicable SBOM, provenance, signing, verification, revocation, and evidence requirements. |
| `DEC-AUTH-001` | Build, attestation, approval, signing, publication, release, trust, and activation authority remain explicit and bounded. |
| `DEC-IDENT-001` | Source, material, builder, subject, SBOM, attestation, signer, key, certificate, trust root, release, repository, and environment identities remain distinct. |
| `DEC-DEV-001` | Developer workspaces and ordinary build workers remain separated from protected signing and production activation authority. |
| `DEC-COMP-001` | Runtime owners verify and activate artifacts through explicit component contracts. |
| `DEC-DATA-001` | Supply-chain processing does not authorize direct writes to component business-data stores. |
| `DEC-AI-001` | External AI and SenTient contributions remain identified candidate inputs until local admission. |
| `DEC-HW-001` | High-assurance signing and trust can require hardware-backed or independently equivalent key protection. |

### 9.2 Prohibited assumptions

Authors, implementers, validators, and AI agents do not assume that:

- a dependency declaration is a complete SBOM;
- a lockfile is a complete SBOM;
- a container label is an SBOM;
- an SBOM proves absence of vulnerabilities;
- an SBOM approves licenses;
- provenance proves artifact safety;
- provenance proves release authorization;
- a signature proves compatibility;
- a signature proves tenant or audience eligibility;
- a signature grants activation authority;
- one signing key can be reused for every channel and purpose;
- repository write access is signing authority;
- a developer workstation is a protected signing environment;
- a build worker can export release-signing private keys;
- a network-retrieved root is trusted automatically;
- key rotation revokes every prior artifact automatically;
- signer revocation and artifact revocation have identical effects;
- a reproducible source revision guarantees reproducible output without controlled materials and toolchains;
- a mutable tag is an immutable subject identity;
- missing SBOM entries can be omitted silently;
- external AI output is verified provenance;
- an offline bundle is trusted because it is signed by an unknown key;
- restore recreates trust without revalidation;
- every artifact class needs the same SBOM or signing fields;
- ordinary Markdown requires per-file content hashes.

A new implementation-affecting supply-chain choice requires an accepted owner decision before dependent authority becomes active.

## 10. Validation Criteria

| Validation group | Required tests |
| --- | --- |
| Software supply-chain evidence | `TEST-SEC-008`, `TEST-SEC-015`, `TEST-LIFE-015`, `TEST-SYS-011` |
| Identity, authority, and signing | `TEST-SEC-003`, `TEST-SEC-005`, `TEST-SEC-006`, `TEST-SEC-007`, `TEST-SYS-004`, `TEST-CROSS-008`, `TEST-CROSS-009`, `TEST-CROSS-014` |
| Artifact lifecycle and attack resistance | `TEST-LIFE-001`, `TEST-LIFE-002`, `TEST-LIFE-003`, `TEST-LIFE-004`, `TEST-LIFE-005`, `TEST-LIFE-006`, `TEST-LIFE-007`, `TEST-LIFE-008`, `TEST-LIFE-009`, `TEST-LIFE-010`, `TEST-LIFE-011` |
| Profiles, build workers, and resources | `TEST-PROF-004`, `TEST-PROF-005`, `TEST-PROF-006`, `TEST-PROF-007`, `TEST-PROF-008`, `TEST-PROF-009`, `TEST-PROF-013`, `TEST-PROF-014`, `TEST-PROF-015`, `TEST-OPS-003`, `TEST-OPS-010` |
| Operations and incident response | `TEST-OPS-002`, `TEST-OPS-004`, `TEST-OPS-005`, `TEST-OPS-006`, `TEST-OPS-007`, `TEST-OPS-008`, `TEST-OPS-009` |
| External and component boundaries | `TEST-SYS-012`, `TEST-CROSS-013`, `TEST-CROSS-015`, `TEST-EXIT-008` |
| Portability and clean restoration | `TEST-EXIT-001`, `TEST-EXIT-002`, `TEST-EXIT-003`, `TEST-EXIT-005`, `TEST-EXIT-006` |
| Documentation and traceability | `TEST-DOC-VAL-003`, `TEST-DOC-VAL-005`, `TEST-DOC-VAL-006`, `TEST-DOC-VAL-007`, `TEST-DOC-VAL-008`, `TEST-DOC-VAL-009`, `TEST-DOC-VAL-010`, `TEST-DOC-VAL-012`, `TEST-DOC-VAL-016`, `TEST-DOC-VAL-017`, `TEST-DOC-VAL-018`, `TEST-DOC-VAL-019`, `TEST-DOC-VAL-020` |

Additional validation confirms:

1. every SBOM binds to an exact subject identity;
2. direct, transitive, vendored, embedded, generated, base, and runtime components are represented when applicable;
3. SBOM completeness is compared with actual artifact inventory;
4. unknown and omitted entries are explicit;
5. provenance resolves source, materials, locks, toolchain, builder, environment, parameters, and output;
6. network, mutable input, manual step, secret use, and nondeterminism context is represented;
7. every attestation declares one subject, predicate, issuer, scope, and evidence relationship;
8. reproducibility evidence follows the artifact-class comparison method;
9. unexplained content differences do not reuse immutable identity;
10. signer, key, certificate, issuer, trust root, purpose, channel, artifact class, tenant, environment, and validity scope resolve;
11. required separation of duties and protected key custody pass;
12. private keys remain absent from ordinary workers, application nodes, caches, logs, and support bundles;
13. trust and revocation state is current or explicitly stale;
14. downgrade, substitution, collision, manifest replacement, signature stripping, and trust-root substitution tests fail safely;
15. repositories preserve complete subject, SBOM, provenance, signature, release, and evidence relationships;
16. offline bundles have exact inventories and bounded verification;
17. export and clean restore preserve or reconstruct the supply-chain graph;
18. restored records are revalidated before use;
19. external candidate contributions remain identified and non-authoritative until admission;
20. ordinary Markdown retains non-hash validation unless included in a declared signed artifact;
21. every requirement maps to an active test or approved manual control;
22. every active claim has current traceability and evidence;
23. no unresolved authority marker exists;
24. all active prose is in English.

A failed required check blocks the affected SBOM, provenance, signature, artifact, release, activation, trust, or conformance claim.

## 11. Non-Normative Examples

### 11.1 Python service artifact

A build farm receives an exact source revision, `pyproject.toml`, `uv.lock`, Python identity, UV identity, base image, and build definition.

It creates the service artifact, scans the packaged output, generates an SBOM from resolved and packaged components, creates provenance, and runs tests.

A separate verifier checks the subject, SBOM, provenance, software bill of materials, compatibility, and evidence. A protected services-channel signer signs the approved release manifest.

### 11.2 Container base image

A service image declares one base image in source configuration.

The generated SBOM records the actual resolved immutable base identity and included layers rather than only the mutable source tag.

A later tag change does not alter the existing artifact or SBOM identity.

### 11.3 Reproducibility comparison

Two isolated build workers receive the same source, lockfiles, toolchain, build definition, and controlled base artifacts.

Their outputs differ only in a declared normalized timestamp field. The artifact-class comparison treats the normalized subjects as equivalent and records the difference explicitly.

An unexplained binary difference would fail the reproducibility result.

### 11.4 Signing service

A publisher submits an exact artifact-manifest identity and signing approval to a protected signing service.

The service verifies the request, signs only the declared manifest, returns the signature envelope, and records key, signer, purpose, scope, and evidence.

The private key never enters the publisher workspace.

### 11.5 Signer revocation

A signing certificate is revoked after suspected compromise.

Repositories publish the revocation state. Verifiers evaluate previously signed artifacts under the declared effective time, scope, and artifact-class rules.

The revocation does not silently erase historical signatures or automatically define every active-artifact response.

### 11.6 Offline node

A sovereign node imports an offline bundle containing an artifact, manifest, SBOM, provenance, signatures, trust bundle, and revocation epoch.

The node verifies the complete inventory and displays the revocation freshness used. It stages the artifact but leaves activation to the normal governed component procedure.

### 11.7 External candidate source

An external AI service proposes release notes, a dependency classification, or a candidate summary.

The contribution appears in provenance as an external candidate input. Local review and artifact admission determine whether any part becomes authoritative release content.

The external service does not attest to the local build unless an explicit trusted attestation contract exists.

### 11.8 Documentation bundle

A documentation release process packages active Markdown files, generated registries, validation reports, and a release manifest into one signed archive.

The archive receives an artifact identity, inventory, integrity values, provenance, and signature.

The individual ordinary Markdown source files continue to use registry, reference, structure, decision, requirement, lock, language, and traceability validation without automatic per-file content hashes.

### 11.9 Clean restore

A clean repository restores artifacts, SBOMs, provenance attestations, signatures, trust records, revocations, releases, and evidence.

Independent validation detects a missing provenance relationship for one artifact. That artifact remains unavailable for release or activation claims until the relationship is restored or regenerated through an approved process.

### 11.10 Key rotation

A knowledge-channel signing key approaches expiry.

Independent custodians activate a replacement key, publish the new trust path, update offline bundles, retain historical verification for the predecessor, and stop new signing with the old key.

Existing valid artifacts remain governed by their signatures, validity context, and current revocation policy.
