<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-DEV-016",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "development",
  "scope": [
    "development_toolchain",
    "artifact_class",
    "release_transition"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "generated/document-index.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "generated/toolchain-catalog.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json",
    "schemas/impact-report.schema.json",
    "contracts/artifact-contracts/release-set.schema.json",
    "contracts/artifact-contracts/provenance-receipt.schema.json"
  ],
  "decision_ids": [
    "DEC-REL-001",
    "DEC-PROFILE-001",
    "DEC-CONTAINER-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-AI-001",
    "DEC-DOC-CHANGE-001"
  ],
  "requirement_ids": [
    "REQ-DEV-REL-001",
    "REQ-DEV-REL-002",
    "REQ-DEV-REL-003",
    "REQ-DEV-REL-004",
    "REQ-DEV-REL-005",
    "REQ-DEV-REL-006",
    "REQ-DEV-REL-007",
    "REQ-DEV-REL-008",
    "REQ-DEV-REL-009",
    "REQ-DEV-REL-010",
    "REQ-DEV-REL-011",
    "REQ-DEV-REL-012",
    "REQ-DEV-REL-013",
    "REQ-DEV-REL-014",
    "REQ-DEV-REL-015",
    "REQ-DEV-REL-016",
    "REQ-DEV-REL-017",
    "REQ-DEV-REL-018",
    "REQ-DEV-REL-019",
    "REQ-DEV-REL-020",
    "REQ-DEV-REL-021",
    "REQ-DEV-REL-022",
    "REQ-DEV-REL-023",
    "REQ-DEV-REL-024",
    "REQ-DEV-REL-025",
    "REQ-DEV-REL-026",
    "REQ-DEV-REL-027",
    "REQ-DEV-REL-028",
    "REQ-DEV-REL-029",
    "REQ-DEV-REL-030",
    "REQ-DEV-REL-031",
    "REQ-DEV-REL-032",
    "REQ-DEV-REL-033",
    "REQ-DEV-REL-034",
    "REQ-DEV-REL-035",
    "REQ-DEV-REL-036",
    "REQ-DEV-REL-037",
    "REQ-DEV-REL-038",
    "REQ-DEV-REL-039",
    "REQ-DEV-REL-040"
  ],
  "lock_ids": [
    "LOCK-DEV-001",
    "LOCK-DEV-002",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DEV-005",
    "LOCK-PROFILE-001",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-AI-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-DOC-015",
    "LOCK-DOC-020",
    "LOCK-IMPL-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-DEV-000",
    "DOC-DEV-001",
    "DOC-DEV-002",
    "DOC-DEV-003",
    "DOC-DEV-004",
    "DOC-DEV-005",
    "DOC-DEV-006",
    "DOC-DEV-007",
    "DOC-DEV-008",
    "DOC-DEV-009",
    "DOC-DEV-010",
    "DOC-DEV-011",
    "DOC-DEV-012",
    "DOC-DEV-013",
    "DOC-DEV-014",
    "DOC-DEV-015",
    "DOC-LIFE-000",
    "DOC-LIFE-001",
    "DOC-LIFE-002",
    "DOC-LIFE-003",
    "DOC-LIFE-004",
    "DOC-LIFE-012",
    "DOC-LIFE-013",
    "DOC-LIFE-015",
    "DOC-LIFE-016",
    "DOC-LIFE-018"
  ],
  "tags": [
    "development",
    "release-transition",
    "release-candidate",
    "reproducible-build",
    "validation",
    "provenance",
    "sbom",
    "release-channels",
    "release-set",
    "atomic-activation",
    "rollback",
    "forward-repair"
  ]
}
KOA:DOC-META:END -->

# Development-to-Release Transition

## 1. Purpose

This document defines the controlled transition from mutable development work to an immutable, validated, published, compatible, and activable kOA release.

The transition separates five states that are often incorrectly collapsed:

`text
development state
 ↓
release candidate
 ↓
published channel artifacts
 ↓
compatible Release Set
 ↓
active release
`

Each state has a different authority.

Development state is mutable and workspace-scoped.

A release candidate is a reproducible immutable proposal.

A published artifact is a versioned artifact available through one canonical release channel.

A Release Set binds independently versioned artifacts that have been tested together for a target profile.

An active release is the authority state selected only after complete validation and successful activation.

The transition protects:

- canonical ownership;
- component and profile boundaries;
- reproducibility;
- source and artifact provenance;
- data and migration safety;
- release-channel independence;
- policy and evidence integrity;
- rollback and forward repair;
- atomic activation;
- the previous known-good release.

No development output becomes active merely because it was built, tested locally, uploaded, signed, or published.

## 2. Scope

### 2.1 Included scope

This document applies to:

- application and service source;
- operating-system and node source;
- component contracts;
- profile contracts;
- policy bundles;
- Kristal and knowledge artifacts;
- language and runtime artifacts;
- Ariane artifacts;
- UCKK and media artifacts;
- container images;
- offline bundles;
- sovereignty bundles;
- generated documentation and AI contexts;
- database and state migrations;
- release manifests;
- SBOMs;
- provenance receipts;
- test evidence;
- publication and activation receipts.

It applies to transitions originating from:

- developer workstations;
- isolated development workspaces;
- pull-request or integration branches;
- build-farm jobs;
- controlled release workspaces;
- emergency corrective development performed under active incident and change authority.

### 2.2 Excluded scope

This document does not define:

- source-control product or hosting service;
- branch naming;
- pull-request user interface;
- continuous-integration vendor;
- container registry vendor;
- package registry vendor;
- operating-system package format;
- signature algorithm;
- production orchestration technology;
- exact approval organization;
- a universal release cadence.

Those implementation choices belong to profiles, toolchains, artifact contracts, security contracts, lifecycle documents, or recipes.

### 2.3 Transition boundary

The development-to-release boundary begins when a change is proposed for release-grade validation.

It ends when one of these terminal dispositions is recorded:

- `active`;
- `rejected`;
- `returned_to_development`;
- `superseded`;
- `withdrawn`;
- `activation_failed`;
- `rolled_back`;
- `forward_repair_required`.

The exact state identifiers belong to the release and artifact contracts.

### 2.4 Relationship to development profiles

Development profiles create mutable source, workspaces, tests, and candidates.

They do not own:

- production activation;
- release-channel identity;
- target-profile authority;
- release-signing authority;
- production secrets;
- production data;
- the active Release Set.

A developer can produce a candidate for a target profile without inheriting the privileges or data of that profile.

### 2.5 Relationship to lifecycle authority

Lifecycle authority owns:

- artifact classes;
- release channels;
- Release Sets;
- verification;
- activation;
- rollback;
- recovery;
- migration;
- forward repair;
- retention.

This development document explains the handoff into that lifecycle.

It does not redefine lifecycle enums or artifact structures.

## 3. Canonical References

### 3.1 Development authority

`text
contracts/profiles/developer-linux-workstation.profile.json
contracts/profiles/developer-windows-wsl.profile.json
contracts/profiles/build-farm.profile.json
generated/toolchain-catalog.json
contracts/toolchains/python-uv.toolchain.json
`

### 3.2 Product and component authority

`text
contracts/system.contract.json
generated/component-catalog.json
generated/component-catalog.json
contracts/components/*.component.json
generated/profile-catalog.json
contracts/profiles/*.profile.json
`

### 3.3 Release authority

`text
contracts/release-channels.contract.json
contracts/artifact-classes.contract.json
contracts/artifact-contracts/release-set.schema.json
contracts/artifact-contracts/provenance-receipt.schema.json
`

### 3.4 Change and validation authority

`text
generated/decision-index.json
generated/requirements-index.json
generated/assertion-index.json
generated/decision-index.json
generated/traceability.json
generated/test-catalog.json
generated/evidence-catalog.json
generated/exception-index.json
schemas/impact-report.schema.json
`

### 3.5 Active authority

`text
generated/authority-manifest.json
`

The active-authority pointer is updated last.

A candidate, artifact repository, release manifest, or deployment environment does not replace the authority registry.

### 3.6 Related lifecycle documents

`text
06-lifecycle/00-artifact-model.md
06-lifecycle/01-artifact-classes.md
06-lifecycle/02-release-model.md
06-lifecycle/03-release-channels.md
06-lifecycle/04-release-sets.md
06-lifecycle/12-artifact-verification.md
06-lifecycle/13-activation-and-verification.md
06-lifecycle/15-data-schema-evolution.md
06-lifecycle/16-forward-repair.md
06-lifecycle/18-sbom-provenance-and-signing.md
`

## 4. Model and Responsibilities

### 4.1 Transition model

The transition is a sequence of authority gates:

| Gate | Input | Output | Authority gained |
| --- | --- | --- | --- |
| Change closure | Mutable change | Release-eligible change packet | Permission to prepare a candidate |
| Source freeze | Workspace state | Declared source package or revision | Reproducible source identity |
| Candidate build | Declared source and toolchains | Immutable candidate artifacts | Candidate identity only |
| Candidate validation | Candidate artifacts | Validation and evidence set | Eligibility for publication |
| Publication | Validated candidate | Signed channel artifact | Published artifact identity |
| Release Set assembly | Channel artifacts | Compatible Release Set | Eligibility for target-profile staging |
| Staging | Release Set | Inactive staged state | No active authority |
| Activation | Validated staged release | Active release and receipts | Active runtime authority |
| Post-activation acceptance | Active release | Accepted or recovered disposition | Final release disposition |

No gate is implied by the next gate's infrastructure.

For example, uploading a candidate to a registry does not prove publication validation, and publication does not prove activation.

### 4.2 Change packet

A semantic transition begins with one change packet.

The change packet identifies:

- change identity;
- change class;
- accepted decisions;
- ADRs where required;
- changed canonical owners;
- changed source and generated files;
- affected components;
- affected profiles;
- affected artifact classes;
- affected release channels;
- requirements;
- locks;
- exceptions;
- impact report;
- migration and compatibility effects;
- tests;
- evidence;
- rollback or forward-repair strategy;
- release disposition.

Patch changes can use a reduced packet when standing editorial or maintenance authority applies.

### 4.3 Source identity

Release source is an exact revision or reproducible source package.

The source identity includes all declared release inputs, such as:

- tracked source;
- canonical contracts;
- generated source inputs;
- dependency lock files;
- toolchain contracts;
- build definitions;
- migration definitions;
- profile definitions;
- release configuration;
- required fixtures;
- declared vendored dependencies.

Local editor settings, workspace caches, undeclared patches, home-directory files, and machine-specific paths remain outside the source identity.

### 4.4 Clean transition workspace

Release preparation occurs in a clean isolated workspace.

The workspace has:

- a unique identity;
- isolated dependency environments;
- isolated services;
- isolated databases and migrations;
- isolated secrets;
- explicit network policy;
- declared toolchains;
- bounded resources;
- clean generated outputs;
- no production credentials;
- no undeclared local state.

A developer workspace can be used only after it proves equivalent cleanliness and reproducibility.

Release-grade validation normally uses a fresh build-farm or dedicated release worker.

### 4.5 Toolchain closure

Every tool that can alter the candidate or validation result is identified.

This includes:

- compilers;
- interpreters;
- package managers;
- container runtimes;
- image builders;
- documentation generators;
- schema validators;
- test runners;
- migration tools;
- signing tools;
- SBOM generators;
- provenance generators;
- archive and bundle tools.

A toolchain reference identifies the version and relevant configuration.

An undeclared workstation-global tool does not become a release input.

### 4.6 Dependency closure

Dependencies are resolved through declared lock state or equivalent immutable resolution.

External inputs identify:

- source location or artifact reference;
- immutable identity;
- expected integrity;
- license or policy data required by the artifact class;
- retention or reproducibility method;
- target architecture where relevant.

A release build can use network access only when the build contract permits it and the resulting inputs remain declared and reproducible.

A transient network response is not a valid hidden build input.

### 4.7 Candidate build

A candidate build produces immutable candidate artifacts.

Candidate identity is derived from the artifact contract and release process.

The build records:

- source identity;
- toolchain identity;
- dependency identity;
- target profile or platform;
- build options;
- generated inputs;
- artifact outputs;
- build diagnostics;
- provenance;
- candidate status.

Candidate artifacts remain non-authoritative.

### 4.8 Reproducibility

Reproducibility means the declared inputs and toolchains can produce a semantically equivalent artifact according to the artifact contract.

Some artifact classes can require byte-for-byte identity.

Others can permit declared non-semantic differences such as archive timestamps when the contract normalizes or records them.

The artifact contract owns the required reproducibility class.

A candidate that fails its required reproducibility class remains unpublished.

### 4.9 Generated content

Generated content is refreshed before release validation.

Generation uses active canonical sources and declared generators.

Examples include:

- documentation indexes;
- profile catalogs;
- component catalogs;
- traceability matrices;
- release-channel matrices;
- AI context packages;
- manifests;
- derived schemas or client bindings;
- build metadata.

Generated output is validated against a clean regeneration.

Generated files do not become an independent source of product authority.

### 4.10 Test levels

Candidate validation can include:

| Level | Focus |
| --- | --- |
| Unit | Local implementation behavior |
| Component contract | Observable interfaces, states, errors, data boundaries, and compatibility |
| Integration | Registered cross-component interactions |
| Profile | Conditional inclusion, topology, isolation, resources, security, and degradation |
| Artifact | Identity, structure, provenance, activation, and compatibility |
| Migration | State transition, rollback boundary, and forward repair |
| Security | Trust, privilege, secrets, disclosure, supply chain, and prohibited access |
| Recovery | Backup, restore, rollback, known-good state, and clean-node restoration |
| Documentation | Registries, schemas, requirements, locks, generated projections, language, and traceability |
| Release Set | Cross-channel and target-profile compatibility |
| Activation | Staging, atomic transition, readiness, acceptance, and recovery |

Only applicable tests run for a candidate, but applicability is explicit and reviewable.

### 4.11 Evidence model

Evidence is tied to:

- candidate identity;
- source revision;
- profile;
- component-contract versions;
- artifact-class versions;
- Release Set;
- test identity;
- toolchain identity;
- execution environment;
- result;
- time;
- retained diagnostics.

A test definition is not evidence that the test ran.

A log without the required identity and result context is not automatically valid test evidence.

### 4.12 Security and secret separation

The transition separates:

- developer credentials;
- test credentials;
- build credentials;
- artifact-publication credentials;
- release-signing credentials;
- staging credentials;
- production activation credentials.

Release artifacts exclude all environment credentials.

Signing and activation authority can require distinct identities or approvals according to the active security and profile contracts.

### 4.13 Candidate immutability

After approval for signing or publication, candidate content is immutable.

Changes such as these create a new candidate:

- rebuilding with changed inputs;
- modifying a manifest;
- replacing a dependency;
- editing generated files;
- changing a signature-covered field;
- changing migration content;
- changing packaging;
- changing profile compatibility;
- changing a test-relevant file.

A new candidate repeats every affected gate.

Approval is never transferred silently to changed bytes or changed semantics.

### 4.14 Artifact classes

Every published output belongs to a registered artifact class.

Examples include:

- system image;
- service artifact;
- policy bundle;
- runtime pack;
- language pack;
- Kristal or knowledge artifact;
- Ariane artifact;
- UCKK or media artifact;
- offline bundle;
- sovereignty bundle;
- Release Set;
- provenance receipt.

The artifact class defines structure, verification, activation, rollback, forward repair, and retention.

### 4.15 Release channels

The four canonical release channels are:

| Channel | Primary content |
| --- | --- |
| `system` | Operating-system images, kernel, host runtime, recovery base, and node-level services |
| `services` | Application services, gateways, workers, and service runtime artifacts |
| `governance` | Policy bundles, revocations, governance controls, and related governed artifacts |
| `knowledge` | Kristal, PGF, language packs, Atlas, and approved knowledge packages |

Each channel has independent:

- artifact identity;
- version;
- signature;
- publication;
- compatibility;
- retention;
- rollback or replacement behavior.

An artifact can reference another channel through compatibility metadata.

It does not absorb the other channel's authority.

### 4.16 Release Set

A Release Set binds exact compatible versions across channels for one or more target profiles.

It identifies:

- Release Set identity and version;
- target profiles and overlays;
- system artifacts;
- service artifacts;
- governance artifacts;
- knowledge artifacts;
- component-contract versions;
- profile-contract versions;
- migration plan;
- rollback or forward-repair plan;
- test and evidence set;
- known-good predecessor;
- activation and acceptance rules.

A Release Set can omit a channel only when the target profile and release contract explicitly allow that channel to remain at a compatible active version.

### 4.17 Compatibility

Compatibility evaluation includes:

- component interfaces;
- event and command versions;
- data schemas;
- migrations;
- profile composition;
- policy-bundle inputs and evaluator versions;
- runtime and knowledge artifact consumers;
- security and trust state;
- recovery artifacts;
- documentation and AI context;
- release-channel constraints.

Unknown required compatibility blocks release.

Compatibility is not inferred from version numbering alone.

### 4.18 Migrations

A candidate that changes persistent state declares:

- source state;
- target state;
- migration identity;
- owner;
- preconditions;
- backup or snapshot requirement;
- ordering;
- downtime or online behavior;
- rollback boundary;
- forward-repair behavior;
- verification;
- evidence.

The owning component controls its migration.

A release process does not write directly into another component's authoritative storage outside that component's migration contract.

### 4.19 Rollback and forward repair

Rollback restores a previous compatible known-good state.

Forward repair moves the system from a failed or irreversible intermediate condition to a valid supported state.

The release plan identifies:

- when rollback is safe;
- when rollback becomes unsafe;
- what state must be retained;
- how forward repair is authorized;
- what evidence is required;
- what user-visible or operator-visible impact occurs.

An irreversible migration without a tested forward-repair path is not release eligible.

### 4.20 Publication

Publication makes an immutable validated artifact available in its release channel.

Publication verifies:

- artifact identity;
- artifact class;
- provenance;
- SBOM where applicable;
- signatures;
- test and evidence completeness;
- target compatibility metadata;
- retention;
- deprecation or predecessor links;
- publication authority.

Publication produces a receipt.

Publication does not activate the artifact.

### 4.21 Promotion

Promotion moves the same immutable artifact identity through permitted repository or environment stages.

Examples include:

`text
candidate repository
 ↓
release repository
 ↓
offline bundle
 ↓
staging node
 ↓
production node
`

Promotion preserves identity and provenance.

Rebuilding separately for each environment is a new build, not promotion.

### 4.22 Staging

Staging copies or installs candidate artifacts into an inactive area.

Staging can perform:

- verification;
- unpacking;
- migration preflight;
- local compatibility checks;
- resource checks;
- readiness preparation;
- backup preparation.

Staged content has no active authority.

Existing services, policies, schemas, or knowledge remain active until the activation boundary succeeds.

### 4.23 Activation

Activation changes the active Release Set or equivalent authority pointer.

The activation sequence resolves:

1. exact target profile;
2. current known-good Release Set;
3. candidate Release Set;
4. signatures and provenance;
5. compatibility;
6. migration readiness;
7. backup and recovery readiness;
8. policy and trust readiness;
9. staged artifacts;
10. activation authority;
11. atomic transition;
12. post-activation readiness;
13. acceptance or recovery disposition;
14. activation receipt.

The active pointer changes last.

### 4.24 Post-activation acceptance

Post-activation acceptance verifies the real activated state.

It can include:

- boot acceptance;
- service readiness;
- schema and migration verification;
- policy evaluation;
- component-contract probes;
- profile-specific offline behavior;
- critical user journey;
- backup and recovery readiness;
- evidence durability.

Failure triggers rollback or forward repair according to the release plan.

### 4.25 Documentation and AI context

Documentation authority changes follow the same release discipline.

Before activation:

- canonical registries validate;
- requirements and locks align;
- normative Markdown aligns;
- generated projections refresh;
- AI context packages refresh;
- traceability completes;
- evidence validates.

AI context is a generated projection.

It does not become authoritative merely because implementation agents consume it.

### 4.26 Approvals and segregation

The active profile, artifact class, and security contracts determine required approvals.

Possible roles include:

- change author;
- code reviewer;
- component owner;
- profile owner;
- security reviewer;
- migration reviewer;
- release builder;
- signing authority;
- publication authority;
- activation authority;
- evidence reviewer.

One person can hold multiple roles only where the active assurance contract permits it.

Approval identities and results are recorded.

### 4.27 Return to development

A failed gate produces a machine-readable disposition.

The disposition identifies:

- candidate;
- failed gate;
- failed tests or checks;
- affected requirements and locks;
- invalid or missing evidence;
- compatibility or migration issue;
- retained diagnostics;
- whether candidate artifacts remain reusable;
- required source or contract change;
- whether a new decision or exception is required;
- next permitted state.

The active release remains unchanged.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-DEV-REL-001,REQ-DEV-REL-002,REQ-DEV-REL-003,REQ-DEV-REL-004,REQ-DEV-REL-005,REQ-DEV-REL-006,REQ-DEV-REL-007,REQ-DEV-REL-008,REQ-DEV-REL-009,REQ-DEV-REL-010,REQ-DEV-REL-011,REQ-DEV-REL-012,REQ-DEV-REL-013,REQ-DEV-REL-014,REQ-DEV-REL-015,REQ-DEV-REL-016,REQ-DEV-REL-017,REQ-DEV-REL-018,REQ-DEV-REL-019,REQ-DEV-REL-020,REQ-DEV-REL-021,REQ-DEV-REL-022,REQ-DEV-REL-023,REQ-DEV-REL-024,REQ-DEV-REL-025,REQ-DEV-REL-026,REQ-DEV-REL-027,REQ-DEV-REL-028,REQ-DEV-REL-029,REQ-DEV-REL-030,REQ-DEV-REL-031,REQ-DEV-REL-032,REQ-DEV-REL-033,REQ-DEV-REL-034,REQ-DEV-REL-035,REQ-DEV-REL-036,REQ-DEV-REL-037,REQ-DEV-REL-038,REQ-DEV-REL-039,REQ-DEV-REL-040 -->
- **REQ-DEV-REL-001 — SHALL:** Every development-to-release transition begin from an identified source revision and an identified change packet.
- **REQ-DEV-REL-002 — SHALL:** Every semantic change entering release preparation reference an accepted owner decision.
- **REQ-DEV-REL-003 — SHALL:** Every major semantic change entering release preparation include a complete direct and transitive impact report.
- **REQ-DEV-REL-004 — SHALL:** Release preparation use a clean source tree or a declared reproducible source package containing every release input.
- **REQ-DEV-REL-005 — SHALL NOT:** Undeclared uncommitted files, local overrides, editor state, workspace caches, or machine-specific paths influence a release artifact.
- **REQ-DEV-REL-006 — SHALL:** All build, generation, test, validation, and packaging toolchains used for a release be versioned and identified.
- **REQ-DEV-REL-007 — SHALL:** Release-grade builds run in an isolated reproducible environment.
- **REQ-DEV-REL-008 — SHALL:** Every external build input be declared, integrity-verified, and retained or reproducibly resolvable according to its artifact contract.
- **REQ-DEV-REL-009 — SHALL NOT:** Release reproducibility depend on an unqualified mutable image tag, floating dependency, undeclared network response, or mutable shared workspace state.
- **REQ-DEV-REL-010 — SHALL:** A release candidate be rebuilt or independently verified from the declared inputs before publication.
- **REQ-DEV-REL-011 — SHALL:** A release candidate carry provenance linking source, decisions, contracts, profiles, toolchains, build inputs, generated artifacts, and validation.
- **REQ-DEV-REL-012 — SHALL:** Applicable software artifacts include an SBOM or equivalent registered dependency inventory.
- **REQ-DEV-REL-013 — SHALL:** Generated registries, documents, catalogs, manifests, and AI contexts be regenerated from active canonical sources before release validation.
- **REQ-DEV-REL-014 — SHALL NOT:** A stale generated projection support a release, conformance, or implementation claim.
- **REQ-DEV-REL-015 — SHALL:** Release validation include every applicable component, profile, artifact, migration, security, data-authority, lifecycle, and documentation control.
- **REQ-DEV-REL-016 — SHALL:** A validation claim identify the exact tests that executed and their terminal results.
- **REQ-DEV-REL-017 — SHALL NOT:** A skipped, unavailable, incomplete, or blocked test be represented as passing.
- **REQ-DEV-REL-018 — SHALL:** Every release-blocking requirement have valid evidence for the exact candidate artifact and target profile.
- **REQ-DEV-REL-019 — SHALL:** Active exceptions affecting a candidate be resolved, disclosed, validated, and linked to their compensating controls and evidence.
- **REQ-DEV-REL-020 — SHALL:** Developer, test, staging, production, and release-signing secrets remain separate.
- **REQ-DEV-REL-021 — SHALL NOT:** A release artifact contain development credentials, test identities, private workspace paths, undeclared fixtures, or mutable local state.
- **REQ-DEV-REL-022 — SHALL:** A candidate artifact be immutable after approval for signing or publication.
- **REQ-DEV-REL-023 — SHALL:** Any post-approval content change create a new candidate identity and repeat all affected validation.
- **REQ-DEV-REL-024 — SHALL:** Published artifacts be assigned to their canonical artifact class and release channel.
- **REQ-DEV-REL-025 — SHALL:** System, services, governance, and knowledge release channels retain independent artifact identity, versioning, signatures, and compatibility.
- **REQ-DEV-REL-026 — SHALL NOT:** One release channel silently embed, activate, or replace another release channel's authority.
- **REQ-DEV-REL-027 — SHALL:** A Release Set identify the exact compatible artifact versions required by each target profile.
- **REQ-DEV-REL-028 — SHALL:** Release Set validation include cross-channel compatibility, component-contract compatibility, profile compatibility, migration compatibility, and recovery compatibility.
- **REQ-DEV-REL-029 — SHALL:** A candidate that changes persistent state define migration, backup, rollback, and forward-repair behavior before publication.
- **REQ-DEV-REL-030 — SHALL:** An irreversible migration declare a tested forward-repair path and the point after which rollback is unsafe.
- **REQ-DEV-REL-031 — SHALL:** Release staging preserve the active known-good release until candidate validation and activation complete.
- **REQ-DEV-REL-032 — SHALL NOT:** A staged, uploaded, signed, or published candidate become active merely because it exists.
- **REQ-DEV-REL-033 — SHALL:** Activation change authoritative state atomically across every artifact and channel included in the Release Set.
- **REQ-DEV-REL-034 — SHALL NOT:** Partial service, policy, system, knowledge, schema, or documentation authority be exposed as an active release.
- **REQ-DEV-REL-035 — SHALL:** Failed activation preserve or restore the previous known-good release or execute the declared forward-repair plan.
- **REQ-DEV-REL-036 — SHALL:** The authority registry or equivalent active-release pointer be updated only after all candidate artifacts, tests, evidence, migrations, generated projections, and activation checks pass.
- **REQ-DEV-REL-037 — SHALL:** Release promotion preserve artifact identity and provenance rather than rebuilding untracked content for each environment.
- **REQ-DEV-REL-038 — SHALL:** A failed release gate return a machine-readable disposition to development identifying affected objects, failed controls, retained artifacts, and required corrective work.
- **REQ-DEV-REL-039 — SHALL:** A release transition record approvals, segregation of duties where required, publication receipts, activation receipts, and final release disposition.
- **REQ-DEV-REL-040 — SHALL:** A semantic change to release gates, channel ownership, artifact identity, compatibility, migration, signing, evidence, or activation use an accepted owner decision and complete impact analysis.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Enter release preparation

1. Create or resolve the change packet.
2. classify the change.
3. resolve accepted decisions and ADRs.
4. compute direct and transitive impact.
5. resolve affected components, profiles, artifacts, channels, requirements, locks, tests, and evidence.
6. verify that no required decision remains missing.
7. select the exact source revision.
8. create a clean release workspace.
9. record the transition from mutable development to release preparation.

### 6.2 Freeze release inputs

1. Capture the source identity.
2. capture dependency lock state.
3. capture toolchain versions.
4. capture base-image and build-environment identities.
5. capture profile and component-contract versions.
6. capture generator and schema versions.
7. capture migration inputs.
8. capture permitted external build inputs.
9. reject undeclared local or remote inputs.
10. produce the source-input manifest.

### 6.3 Build a release candidate

1. Provision an isolated build environment.
2. verify the input manifest.
3. resolve dependencies.
4. generate required source and documentation projections.
5. build each candidate artifact.
6. record artifact identities.
7. generate provenance.
8. generate an SBOM where applicable.
9. preserve build logs and diagnostics.
10. mark artifacts as immutable release candidates.

### 6.4 Verify reproducibility

1. Rebuild or independently verify from the same declared inputs.
2. compare results according to the artifact's reproducibility class.
3. explain only contract-permitted non-semantic differences.
4. reject unexplained differences.
5. retain comparison evidence.
6. bind successful reproducibility evidence to the candidate identity.

### 6.5 Run candidate validation

1. Resolve the applicable test matrix.
2. provision isolated test environments.
3. verify candidate identities before test execution.
4. run unit and component tests.
5. run integration and profile tests.
6. run migration and recovery tests where applicable.
7. run security and supply-chain checks.
8. run documentation and generated-content validation.
9. run Release Set compatibility checks.
10. record every terminal test result.
11. retain evidence and diagnostics.
12. block publication when a release-blocking test does not pass.

### 6.6 Review exceptions

1. Resolve exceptions affecting the candidate.
2. verify active status, scope, owner, and closure condition.
3. verify compensating controls.
4. run exception-specific validation.
5. record exception evidence.
6. disclose the exception in the release evidence.
7. block the candidate when the exception is missing, expired, incompatible, or unsupported.

### 6.7 Approve and sign a candidate

1. Freeze the candidate content.
2. complete required reviews.
3. verify validation and evidence completeness.
4. verify artifact-class metadata.
5. verify target release channel.
6. verify signing authority.
7. sign the immutable candidate.
8. create signing and provenance receipts.
9. prevent post-signing mutation.
10. create a new candidate if any content changes.

### 6.8 Publish channel artifacts

1. Submit the signed candidate to the canonical release channel.
2. verify identity, signature, provenance, and artifact class.
3. verify retention and predecessor links.
4. publish the exact candidate identity.
5. record repository or bundle location.
6. produce a publication receipt.
7. leave the artifact inactive.

### 6.9 Assemble a Release Set

1. Select exact published versions from each required channel.
2. identify target profiles and overlays.
3. resolve component and profile contracts.
4. resolve cross-channel compatibility.
5. resolve migrations and ordering.
6. resolve rollback and forward repair.
7. resolve predecessor Release Set.
8. attach tests and evidence.
9. validate the Release Set schema.
10. sign and publish the Release Set as an inactive artifact.

### 6.10 Stage a release

1. Select the target deployment and effective profile.
2. verify the active known-good Release Set.
3. verify the candidate Release Set.
4. verify signatures and trust.
5. verify local artifact availability.
6. create or verify backup and recovery state.
7. stage system, service, governance, and knowledge artifacts.
8. perform migration preflight.
9. perform local compatibility and resource checks.
10. retain the active release unchanged.
11. produce staging evidence.

### 6.11 Activate a release

1. Obtain activation authority.
2. quiesce affected transitions where required.
3. confirm backup and recovery readiness.
4. execute declared migrations in the required order.
5. activate the complete compatible Release Set.
6. update the active release pointer last.
7. start or reload selected components.
8. evaluate health and readiness.
9. run post-activation acceptance.
10. produce activation and acceptance receipts.
11. mark the release active only after all acceptance conditions pass.

### 6.12 Handle activation failure

1. detect the failed activation or acceptance condition.
2. stop further incompatible mutation.
3. preserve diagnostics and evidence.
4. determine rollback safety.
5. restore the previous known-good Release Set when safe.
6. execute forward repair when rollback is unsafe.
7. validate the recovered authority state.
8. produce failure and recovery receipts.
9. return the candidate to development or supersede it.
10. keep the affected release inactive.

### 6.13 Promote an artifact

1. identify the immutable published artifact.
2. verify source and destination repository policy.
3. copy or expose the same artifact identity.
4. preserve signatures and provenance.
5. verify integrity after promotion.
6. record the promotion receipt.
7. do not rebuild content as part of promotion.

### 6.14 Withdraw or supersede a candidate

1. identify the candidate or published artifact.
2. record the reason.
3. prevent new Release Sets from selecting it.
4. preserve historical identity and evidence.
5. link the replacement when available.
6. retain or remove bytes according to artifact-retention policy.
7. never reuse the retired identifier.

## 7. Failure States and Safe Degradation

| Failure condition | Required response | Preserved state | Blocked transition |
| --- | --- | --- | --- |
| Source revision is not exact | Reject release preparation | Development workspace | Candidate build |
| Source tree contains undeclared state | Recreate clean source input | Existing active release | Release-grade build |
| Toolchain version is unresolved | Block build | Source and prior artifacts | Candidate creation |
| Dependency is floating or unverifiable | Block build | Previous valid candidate or release | Reproducible candidate |
| Generated projection is stale | Regenerate and revalidate | Canonical source authority | Candidate validation |
| Reproducibility check fails | Reject candidate | Build evidence and prior release | Publication |
| Required test fails | Return candidate to development | Active release | Publication |
| Required test is skipped or unavailable | Mark validation blocked | Active release | Passing release claim |
| Required evidence is missing | Mark gate blocked | Candidate and diagnostics | Publication or activation |
| Exception is expired or unsupported | Reject affected release claim | Underlying requirement and active release | Exception-dependent release |
| Secret contamination is detected | Revoke affected credentials and rebuild from clean inputs | Active release | Publication |
| SBOM or provenance is incomplete | Reject applicable artifact | Candidate diagnostics | Signing or publication |
| Candidate changes after approval | Invalidate approval and create new candidate | Historical candidate | Publication under prior approval |
| Signature verification fails | Quarantine artifact | Active release | Staging or activation |
| Artifact is assigned to wrong channel | Reject publication | Candidate | Channel publication |
| Cross-channel compatibility is unknown | Reject Release Set | Published channel artifacts | Release Set activation |
| Migration preflight fails | Preserve current state | Known-good release | Activation |
| Backup or recovery readiness fails | Preserve current state | Known-good release | Risk-bearing activation |
| Staging fails | Remove or isolate staged content | Active release | Activation |
| Partial activation is detected | Stop and recover | Previous known-good state where possible | Continued operation on mixed authority |
| Post-activation readiness fails | Roll back or forward repair | Recoverable state and evidence | Release acceptance |
| Rollback is unsafe | Execute declared forward repair | Recoverable unaffected authority | Blind downgrade |
| Authority pointer update fails | Preserve or restore prior pointer | Previous active release | Candidate authority |
| Publication repository is unavailable | Defer publication | Validated candidate | Published status |
| Signing authority is unavailable | Keep candidate unsigned and inactive | Validated candidate | Publication requiring signature |
| Final validation report is incomplete | Mark release blocked | Candidate evidence | Release claim |

Failure remains gate-scoped.

A failed release does not weaken component boundaries, profile rules, security controls, evidence requirements, or data ownership.

## 8. Cross-Component Interactions

### 8.1 Development workspace and build farm

The development workspace produces source and local evidence.

The build farm or release worker independently consumes declared inputs and produces reproducible candidates.

Mutable workspace volumes, credentials, ports, databases, and local dependency environments do not cross the boundary unless explicitly represented as versioned release inputs.

### 8.2 Component owners

Each component owner verifies:

- component-contract compatibility;
- owned data and migration behavior;
- interfaces and events;
- degradation;
- recovery;
- target-profile behavior.

A release workflow does not change a component's state directly outside the component's activation or migration contract.

### 8.3 Profile owners

A profile owner verifies:

- component selection;
- overlays;
- resource envelope;
- isolation;
- security;
- network and storage behavior;
- offline envelope;
- recovery;
- profile-specific conformance.

Passing one profile does not imply passing another.

### 8.4 Resource Governor

Resource Governor controls release-time or activation-time workload resources where selected.

It does not decide whether a candidate is authorized for publication or activation.

Release authority does not bypass resource safety.

### 8.5 Governance Policy Runtime

Governance Policy Runtime can evaluate publication, privilege, exception, or activation decisions for profiles that select it.

It does not build artifacts, schedule resources, sign releases, or execute host mutation.

### 8.6 Identity and Trust

Identity and Trust verifies:

- builders;
- reviewers;
- signers;
- artifacts;
- Release Sets;
- activation requests;
- trust roots;
- provenance.

Verification does not replace compatibility, tests, or evidence.

### 8.7 kOA Node Agent and privileged activation

A node agent can stage and coordinate a profile-authorized release operation.

A narrow privileged boundary executes required host mutation.

The Release Set, policy decision, node operation, and activation receipt remain correlated.

### 8.8 Audit Broker

Audit Broker receives selected change, publication, signing, activation, exception, rollback, and recovery evidence.

It does not become the canonical owner of source, artifacts, releases, or application state.

### 8.9 Publication Gateway

Publication Gateway handles governed disclosure or external publication of product content.

Artifact publication into a release channel is a lifecycle operation and is not automatically the same as cross-domain product publication.

The applicable contracts keep those responsibilities distinct.

### 8.10 External integrations and AI

External services can assist a development workflow only through registered, explicit, non-authoritative boundaries.

External AI output remains candidate input.

It cannot approve, sign, publish, activate, or directly modify release authority.

Any adopted result enters the release process as changed source or canonical authority and receives a new candidate identity and affected validation.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Closed decisions

| Decision or ADR | Closed choice |
| --- | --- |
| `DEC-PROFILE-001` | Target-profile behavior and conformance remain explicit |
| `DEC-CONTAINER-001` | Build and runtime container choices remain profile-scoped |
| `DEC-DATA-001` | Release and migration workflows preserve component data ownership |
| `DEC-GOV-001` | Policy evaluation and resource control remain separate |
| `DEC-AI-001` | External AI remains optional, explicit, and non-authoritative |
| `DEC-DOC-CHANGE-001` | Semantic changes use the canonical change and impact protocol |

### 9.2 Protected locks

| Lock | Protected relationship |
| --- | --- |
| `LOCK-DEV-001` to `LOCK-DEV-005` | Workspace, dependency, service, port, data, and cache isolation |
| `LOCK-PROFILE-001` | A target-profile release rule does not become global |
| `LOCK-DATA-001` | Release and migration work cannot directly write foreign authoritative state |
| `LOCK-GOV-001` | Policy and resource authorities remain separate |
| `LOCK-AI-002` | External AI output cannot directly modify release authority |
| `LOCK-LIFE-001` | Published artifacts do not activate partially |
| `LOCK-LIFE-002` | Artifact classes define rollback or forward repair |
| `LOCK-LIFE-003` | Release Sets bind compatible versions |
| `LOCK-LIFE-004` | Independent channel updates preserve compatibility |
| `LOCK-DOC-015` | Major semantic changes receive transitive impact analysis |
| `LOCK-DOC-020` | Release-grade documentation validation runs from clean state |
| `LOCK-IMPL-001` | Recipes and local pipeline behavior do not redefine lifecycle authority |

### 9.3 Prohibited assumptions

The following assumptions are invalid:

- a successful local build is a release;
- a passing unit test proves profile conformance;
- uploading an artifact publishes it;
- publishing an artifact activates it;
- signing an artifact proves compatibility;
- a signature proves tests passed;
- a Release Set is optional when channels must move together;
- a version number proves compatibility;
- a mutable image tag identifies a release;
- the latest dependency is a reproducible dependency;
- a developer workspace is clean because the developer says it is;
- uncommitted files can be added after validation;
- a release can be rebuilt differently for each environment and retain the same identity;
- staging can modify active state;
- one release channel can carry hidden policy or knowledge authority;
- a service update can silently run another component's migration;
- a migration is safe because it succeeded once;
- rollback is always possible;
- forward repair can be designed after failure;
- skipped tests can be treated as passing;
- a test definition proves execution;
- logs without candidate identity are sufficient evidence;
- an exception can remain undisclosed;
- production signing keys can be used in developer workspaces;
- development secrets can be removed after publication;
- a partial activation is acceptable during a maintenance window;
- an active pointer can be changed before readiness;
- external AI can approve or activate a release;
- generated AI context can replace canonical registries;
- current CI behavior defines lifecycle authority;
- a recipe or vendor pipeline creates a release rule;
- failed activation permits mixed authority to remain active;
- an identifier can be reused after withdrawal.

Unresolved ownership, decision, compatibility, migration, signing, evidence, or recovery behavior blocks the affected release transition.

## 10. Validation Criteria

This document is conformant when:

1. the document is registered as `DOC-DEV-016`;
2. the path is `05-development/16-development-to-release-transition.md`;
3. the active language is English;
4. every linked decision is accepted;
5. every listed lock is active;
6. every release transition begins with an identified source revision and change packet;
7. semantic changes have accepted owner decisions;
8. major changes have complete impact reports;
9. release builds use clean declared source inputs;
10. release toolchains are versioned and identified;
11. build environments are isolated and reproducible;
12. dependencies and external build inputs are immutable or reproducibly resolved;
13. candidate reproducibility passes its artifact-class requirement;
14. generated content matches clean regeneration;
15. component, integration, profile, artifact, migration, security, recovery, documentation, and Release Set controls run when applicable;
16. skipped or blocked tests are not reported as passing;
17. evidence binds to exact candidate and profile identities;
18. active exceptions are disclosed and validated;
19. development and release credentials remain separate;
20. release artifacts contain no development secrets or undeclared workspace state;
21. approved candidates remain immutable;
22. changed candidates receive new identity and affected validation;
23. every artifact belongs to one canonical artifact class;
24. every published artifact belongs to one canonical release channel;
25. system, services, governance, and knowledge identities remain independent;
26. Release Sets identify exact compatible versions;
27. cross-channel and target-profile compatibility passes;
28. migrations have owner, ordering, backup, rollback boundary, and forward repair;
29. irreversible migrations have tested forward repair;
30. staging preserves the active known-good release;
31. publication does not imply activation;
32. activation is atomic;
33. partial authority is rejected;
34. failed activation restores known-good state or forward repairs;
35. the active authority pointer changes last;
36. promotion preserves artifact identity;
37. failure dispositions are machine-readable and actionable;
38. approvals, publication, activation, and recovery receipts are retained;
39. all 40 linked requirements resolve;
40. all required tests execute;
41. all required evidence validates;
42. no unresolved release state exists;
43. generated release and AI context projections match canonical authority;
44. complete documentation validation passes.

Expected test coverage includes:

`text
TEST-DEV-REL-001 Exact source and change-packet identity
TEST-DEV-REL-002 Clean release source
TEST-DEV-REL-003 Toolchain and dependency closure
TEST-DEV-REL-004 Isolated reproducible candidate build
TEST-DEV-REL-005 Candidate reproducibility
TEST-DEV-REL-006 Provenance and SBOM completeness
TEST-DEV-REL-007 Clean generated-content regeneration
TEST-DEV-REL-008 Applicable test-matrix execution
TEST-DEV-REL-009 No false pass for skipped or blocked tests
TEST-DEV-REL-010 Candidate-specific evidence completeness
TEST-DEV-REL-011 Exception disclosure and controls
TEST-DEV-REL-012 Secret and environment separation
TEST-DEV-REL-013 Candidate immutability
TEST-DEV-REL-014 Artifact-class and channel ownership
TEST-DEV-REL-015 Four-channel independence
TEST-DEV-REL-016 Release Set compatibility
TEST-DEV-REL-017 Migration rollback boundary
TEST-DEV-REL-018 Forward-repair readiness
TEST-DEV-REL-019 Inactive staging
TEST-DEV-REL-020 Atomic activation
TEST-DEV-REL-021 Known-good rollback
TEST-DEV-REL-022 Identity-preserving promotion
TEST-DEV-REL-023 Authority pointer updated last
TEST-DEV-REL-024 Machine-readable return to development
`

The test catalog and evidence registry own executable controls and evidence definitions.

This document does not claim that those tests have already executed.

## 11. Non-Normative Examples

> **Non-normative example:** These examples illustrate valid transition patterns. They do not redefine artifact, release, profile, or toolchain contracts.

### 11.1 Service release

A developer changes Orgo.

The change packet identifies the Orgo component contract, target profiles, service artifact, migration impact, tests, and evidence.

A clean build worker produces one immutable service image with provenance and an SBOM.

The image passes component and profile tests, is signed, and is published to the `services` channel.

A Release Set selects the image with compatible system, governance, and knowledge versions.

The target node stages and atomically activates the Release Set.

### 11.2 Governance policy release

A policy owner changes a policy rule under an accepted decision.

A policy bundle is built and validated against Governance Policy Runtime, target profiles, exceptions, tests, and receipts.

The bundle is published to the `governance` channel.

Publication does not change the active policy set.

Activation occurs only through a compatible Release Set or a contract-permitted compatible governance-channel update.

### 11.3 Knowledge artifact release

GF Wordbench produces a language artifact.

The build records source grammar, toolchain, dependency locks, tests, and provenance.

The artifact is published to the `knowledge` channel.

SemantiK Architect Runtime consumes it only after compatibility and activation.

The workbench does not remain available for runtime operation.

### 11.4 System image release

A signed operating-system image is built from declared source, base packages, kernel, node services, and toolchains.

Recovery and rollback tests pass.

The image is published to the `system` channel.

A sovereign node stages the image while retaining the active known-good image.

Activation changes the complete compatible Release Set and verifies boot readiness.

### 11.5 Failed migration test

A service candidate passes unit tests but its data migration fails restore testing.

The candidate remains inactive.

The failure disposition identifies the migration, affected component, failed test, diagnostics, and required corrective work.

The developer creates a new candidate after correcting the migration.

### 11.6 Irreversible migration

A migration transforms stored data in a way that prevents safe rollback after a declared commit point.

Before publication, the release includes:

- a verified backup;
- a tested pre-commit rollback;
- the commit point;
- a tested forward-repair artifact;
- recovery evidence.

Without the forward-repair path, the release remains blocked.

### 11.7 Offline sovereign promotion

A complete signed Release Set and its artifacts are assembled into an offline bundle.

The same immutable identities move to removable media and into a sovereign-offline node's quarantine.

The node verifies, stages, and activates the Release Set locally.

No artifact is rebuilt on the offline node.

### 11.8 External AI contribution

A developer uses an approved external AI surface to suggest code or documentation.

The output remains candidate material.

After review, adopted changes become ordinary source changes in the change packet.

The release process does not treat the external transcript as approval, evidence, provenance of the final artifact, or activation authority.

### 11.9 Invalid environment rebuild

A team builds one image for tests and rebuilds a different image from a mutable branch for production while reusing the same version.

The process is invalid.

Promotion preserves one immutable validated artifact identity.

### 11.10 Invalid partial activation

A release updates services first, policy later, and knowledge artifacts the next day even though the compatibility plan requires all three together.

The deployment exposes mixed authority and is invalid.

The valid transition stages all required channel artifacts and activates the compatible Release Set atomically.
