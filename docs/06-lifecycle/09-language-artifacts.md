<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-LIFE-009",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "lifecycle",
  "scope": [
    "artifact_class:pgf_artifact",
    "artifact_class:language_runtime_pack",
    "release_channel:knowledge"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/global_capabilities",
    "contracts/system.contract.json#/global_boundaries",
    "generated/component-catalog.json",
    "contracts/subsystems/semantik-architect.subsystem.json",
    "generated/profile-catalog.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json",
    "contracts/artifact-contracts/language-pack.schema.json",
    "contracts/artifact-contracts/runtime-pack.schema.json",
    "contracts/artifact-contracts/release-set.schema.json",
    "contracts/artifact-contracts/provenance-receipt.schema.json"
  ],
  "decision_ids": [
    "DEC-REL-001",
    "DEC-PROFILE-001",
    "DEC-AI-001",
    "DEC-DATA-001"
  ],
  "requirement_ids": [
    "REQ-LIFE-LANG-001",
    "REQ-LIFE-LANG-002",
    "REQ-LIFE-LANG-003",
    "REQ-LIFE-LANG-004",
    "REQ-LIFE-LANG-005",
    "REQ-LIFE-LANG-006",
    "REQ-LIFE-LANG-007",
    "REQ-LIFE-LANG-008",
    "REQ-LIFE-LANG-009",
    "REQ-LIFE-LANG-010",
    "REQ-LIFE-LANG-011",
    "REQ-LIFE-LANG-012",
    "REQ-LIFE-LANG-013",
    "REQ-LIFE-LANG-014",
    "REQ-LIFE-LANG-015",
    "REQ-LIFE-LANG-016",
    "REQ-LIFE-LANG-017",
    "REQ-LIFE-LANG-018",
    "REQ-LIFE-LANG-019",
    "REQ-LIFE-LANG-020",
    "REQ-LIFE-LANG-021",
    "REQ-LIFE-LANG-022",
    "REQ-LIFE-LANG-023",
    "REQ-LIFE-LANG-024",
    "REQ-LIFE-LANG-025",
    "REQ-LIFE-LANG-026",
    "REQ-LIFE-LANG-027",
    "REQ-LIFE-LANG-028",
    "REQ-LIFE-LANG-029",
    "REQ-LIFE-LANG-030",
    "REQ-LIFE-LANG-031",
    "REQ-LIFE-LANG-032",
    "REQ-LIFE-LANG-033",
    "REQ-LIFE-LANG-034",
    "REQ-LIFE-LANG-035",
    "REQ-LIFE-LANG-036",
    "REQ-LIFE-LANG-037",
    "REQ-LIFE-LANG-038",
    "REQ-LIFE-LANG-039",
    "REQ-LIFE-LANG-040"
  ],
  "lock_ids": [
    "LOCK-COMP-002",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-DATA-001",
    "LOCK-PROFILE-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-IMPL-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-002",
    "DOC-DEV-016",
    "DOC-LIFE-000",
    "DOC-LIFE-001",
    "DOC-LIFE-002",
    "DOC-LIFE-003",
    "DOC-LIFE-004",
    "DOC-LIFE-012",
    "DOC-LIFE-013",
    "DOC-LIFE-018"
  ],
  "tags": [
    "lifecycle",
    "language-artifacts",
    "pgf",
    "language-runtime-pack",
    "gf-wordbench",
    "semantik-architect-runtime",
    "knowledge-channel",
    "deterministic-language-runtime",
    "atomic-activation",
    "rollback",
    "offline"
  ]
}
KOA:DOC-META:END -->

# Language Artifacts

## 1. Purpose

This document defines the lifecycle of compiled language artifacts used by kOA.

The lifecycle separates language construction from runtime language execution:

`text
authoritative language project
 ↓
GF Wordbench build and validation
 ↓
compiled PGF candidate
 ↓
language runtime pack candidate
 ↓
knowledge-channel publication
 ↓
compatible Release Set
 ↓
SemantiK Architect Runtime staging
 ↓
atomic activation
 ↓
deterministic runtime rendering
`

GF Wordbench owns language construction and candidate production.

SemantiK Architect Runtime consumes published compiled artifacts.

The runtime does not contain the language-construction factory and does not compile grammars during normal user operation.

The lifecycle exists to provide:

- deterministic language output;
- reproducible language builds;
- explicit source and toolchain provenance;
- runtime compatibility;
- profile-specific installation;
- offline installation and use;
- atomic activation;
- rollback or forward repair;
- independently versioned knowledge-channel delivery;
- evidence for every authoritative transition.

## 2. Scope

### 2.1 Included artifacts

This document applies to:

- compiled PGF candidates;
- published PGF artifacts;
- language runtime pack candidates;
- published language runtime packs;
- language manifests;
- compatibility declarations;
- validation reports;
- provenance receipts;
- release evidence;
- activation and rollback receipts;
- offline language bundles;
- derived runtime indexes and caches.

### 2.2 Included lifecycle activities

The lifecycle covers:

- source selection;
- language-project build sessions;
- compilation;
- candidate packaging;
- reproducibility;
- validation;
- review;
- publication;
- release-channel assignment;
- Release Set compatibility;
- staging;
- activation;
- runtime loading;
- rollback;
- forward repair;
- deprecation;
- retirement;
- backup;
- offline transfer;
- retention;
- evidence.

### 2.3 Excluded scope

This document does not define:

- the GF language itself;
- grammar syntax;
- the Resource Grammar Library;
- the exact language-pack JSON schema;
- exact manifest field names;
- the complete SemantiK runtime API;
- product-specific message catalogs;
- translation editorial policy;
- linguistic style guides;
- exact release repository implementation;
- exact signature algorithm;
- application-specific structured-input schemas.

Those facts belong to language projects, toolchain contracts, artifact contracts, component contracts, profile contracts, security documents, and product-domain contracts.

### 2.4 Artifact authority classes

| Object | Authority class | Owner |
| --- | --- | --- |
| Language source project | Authoritative build source | Language project and GF Wordbench workflow |
| Local build output | Mutable or disposable candidate | Build workspace |
| Compiled PGF candidate | Non-authoritative candidate artifact | Candidate build |
| Language runtime pack candidate | Non-authoritative candidate artifact | Candidate packaging workflow |
| Published PGF artifact | Published immutable artifact | `knowledge` release channel |
| Published language runtime pack | Published immutable artifact | `knowledge` release channel |
| Active installed language pack | Active runtime authority | Effective Release Set and runtime activation state |
| Previous compatible pack | Recovery authority | Runtime lifecycle state |
| Rendered output | Derived runtime result | Requesting component and runtime interaction |
| Runtime cache | Derived and rebuildable | SemantiK Architect Runtime |
| Validation report | Evidence input | Test and evidence system |

A published artifact is immutable but inactive until selected and activated.

### 2.5 Relationship to profiles

Profiles determine:

- which languages are installed;
- which language packs are active;
- permitted locales and scripts;
- offline requirements;
- storage and memory envelopes;
- trust and signature requirements;
- activation mode;
- rollback retention;
- update source;
- evidence obligations.

A profile can install only the languages required by its environment.

The global baseline does not require every available language pack.

## 3. Canonical References

### 3.1 Components

`text
generated/component-catalog.json
contracts/components/gf-wordbench.component.json
contracts/components/semantik-architect-runtime.component.json
`

GF Wordbench owns the build workflow.

SemantiK Architect Runtime owns deterministic consumption, loading, active-pack state, and runtime rendering.

### 3.2 Artifact contracts

`text
contracts/artifact-contracts/language-pack.schema.json
contracts/artifact-contracts/runtime-pack.schema.json
contracts/artifact-contracts/release-set.schema.json
contracts/artifact-contracts/provenance-receipt.schema.json
`

The artifact contracts own exact structure, required fields, identifiers, verification, compatibility, and lifecycle metadata.

### 3.3 Release authority

`text
contracts/release-channels.contract.json
contracts/artifact-classes.contract.json
generated/authority-manifest.json
`

PGF artifacts and language runtime packs belong to the `knowledge` release channel.

The active authority index changes only after complete validation and activation.

### 3.4 Validation and change authority

`text
generated/decision-index.json
generated/requirements-index.json
generated/assertion-index.json
generated/traceability.json
generated/test-catalog.json
generated/evidence-catalog.json
generated/exception-index.json
`

### 3.5 Related documents

`text
02-system/02-logical-architecture.md
05-development/16-development-to-release-transition.md
06-lifecycle/00-artifact-model.md
06-lifecycle/01-artifact-classes.md
06-lifecycle/02-release-model.md
06-lifecycle/03-release-channels.md
06-lifecycle/04-release-sets.md
06-lifecycle/12-artifact-verification.md
06-lifecycle/13-activation-and-verification.md
06-lifecycle/18-sbom-provenance-and-signing.md
`

## 4. Model and Responsibilities

### 4.1 Build and runtime separation

The language system has two primary responsibilities.

| Responsibility | Component |
| --- | --- |
| Edit, compile, validate, and package language projects | GF Wordbench |
| Load published packs and render deterministic language output | SemantiK Architect Runtime |

The runtime does not contain:

- the GF compiler;
- grammar repair tools;
- language-construction workspaces;
- development scenarios;
- build-only dependencies;
- workbench publication credentials.

The workbench does not become a required user-runtime service.

### 4.2 Language project

A language project is the authoritative build source for one declared language target or a contract-defined related language set.

A release-grade build identifies:

- project identity;
- language and locale identity;
- script and regional variant where applicable;
- source revision;
- grammar sources;
- message sources;
- structured-input contracts;
- GF toolchain;
- resource grammar inputs;
- dependency state;
- validation fixtures;
- target runtime contract;
- intended profiles;
- compatibility baseline.

A GF Wordbench session operates on one active language project.

Parallel projects use isolated workspaces and dependency environments.

### 4.3 Build inputs

Build inputs are closed and reproducible.

They can include:

- abstract and concrete grammar sources;
- lexicons;
- message patterns;
- morphological resources;
- resource grammar dependencies;
- structured-input schemas;
- test corpora;
- accepted linguistic fixtures;
- build configuration;
- compiler configuration;
- target runtime contract;
- packaging configuration.

Untracked local files and mutable shared workbench state remain excluded.

### 4.4 Compiled PGF candidate

The compiled PGF candidate is the executable grammar output produced by GF Wordbench.

It remains a candidate until:

- build provenance is complete;
- required validation passes;
- packaging is complete;
- review is complete;
- publication succeeds.

The PGF candidate has an artifact identity and integrity evidence according to its artifact contract.

The candidate does not become authoritative because it compiles successfully.

### 4.5 Language runtime pack

A language runtime pack is the installable unit consumed by SemantiK Architect Runtime.

It binds:

- one or more contract-permitted compiled PGF artifacts;
- language and locale identity;
- runtime compatibility;
- resource grammar compatibility;
- structured-input compatibility;
- manifest;
- provenance;
- validation evidence;
- required companion artifacts;
- activation and rollback metadata;
- deprecation and predecessor relationships where applicable.

The exact contents and cardinalities remain owned by `language-pack.schema.json`.

### 4.6 Candidate identity

Candidate identity distinguishes every release-grade build.

A new candidate is created when any semantic or signature-covered input changes, including:

- grammar source;
- lexicon;
- message source;
- GF toolchain;
- resource grammar dependency;
- structured-input contract;
- packaging;
- manifest;
- target runtime contract;
- target profile;
- compatibility declaration;
- validation-relevant fixture.

Candidate approval does not transfer to changed content.

### 4.7 Provenance

Language-artifact provenance links:

- language project;
- source revision;
- change packet;
- accepted decisions;
- GF toolchain;
- resource grammar inputs;
- build environment;
- dependencies;
- generated PGF;
- language runtime pack;
- tests;
- evidence;
- reviewer and publication events;
- target release channel.

Provenance describes how the artifact was produced.

It does not replace linguistic, runtime, compatibility, or release validation.

### 4.8 Reproducibility

A release-grade language build runs in an isolated environment with identified tools and dependencies.

Reproducibility is evaluated according to the artifact contract.

The build comparison can require:

- identical compiled semantic content;
- identical manifest semantics;
- identical compatibility declarations;
- identical normalized package contents;
- explanation of contract-permitted non-semantic differences.

Unexplained build differences block publication.

### 4.9 Validation classes

Language candidates can require these validation classes:

| Validation class | Purpose |
| --- | --- |
| Source closure | Confirms all build inputs are declared |
| GF compilation | Confirms grammar compilation succeeds |
| Structural validation | Confirms artifact and manifest structure |
| Language identity | Confirms language, locale, script, and variant |
| Runtime compatibility | Confirms supported runtime contract |
| Resource grammar compatibility | Confirms declared grammar-library relationship |
| Structured-input compatibility | Confirms accepted input shapes and keys |
| Deterministic rendering | Confirms repeatable output for recorded inputs |
| Regression | Detects unintended output or interpretation change |
| Coverage | Evaluates contract-defined language and message coverage |
| Packaging | Confirms complete runtime pack assembly |
| Offline load | Confirms use without network dependency |
| Activation | Confirms inactive staging and atomic activation |
| Rollback | Confirms restoration of the prior compatible pack |
| Profile | Confirms target-profile installation and resource behavior |
| Evidence | Confirms results bind to the exact candidate |

The test catalog owns executable tests and terminal result semantics.

### 4.10 Deterministic rendering

SemantiK Architect Runtime produces language output from:

- structured input;
- selected active language pack;
- selected language and locale;
- declared rendering operation;
- active runtime contract.

The same semantic inputs and artifact versions produce the same semantic output.

Runtime output does not rely on:

- external generative AI;
- an embedding model;
- autonomous classification;
- an autonomous language-selection model;
- an undeclared remote service.

### 4.11 Message reuse

Runtime implementations can optimize repeated language output through:

1. static message catalogs;
2. validated parameterized patterns;
3. cached rendered results;
4. deterministic PGF generation.

Optimization does not change authority.

A cache entry remains derived from an active published language artifact and declared input.

A cache is invalidated or segregated when relevant artifact, locale, runtime, message, or structured-input versions change.

### 4.12 External AI boundary

External AI can assist a person during drafting or research only through the registered non-authoritative workflow.

Externally generated material remains candidate source.

Before adoption into a language project, it receives:

- provenance;
- human or owner review;
- linguistic validation;
- compatibility review;
- controlled source integration;
- the complete build and release process.

An external AI response cannot directly produce an active PGF or runtime pack.

### 4.13 Knowledge release channel

PGF artifacts and language runtime packs are published through `knowledge`.

The channel preserves independent:

- identity;
- version;
- signature or integrity evidence;
- provenance;
- compatibility;
- deprecation;
- retention.

A knowledge-channel update can be released independently only when compatibility with the active Release Set remains valid.

### 4.14 Release Set relationship

A Release Set identifies the exact language artifacts for each target profile.

Compatibility can depend on:

- SemantiK Architect Runtime version;
- language-pack contract version;
- GF artifact format;
- resource grammar relationship;
- structured-input contracts;
- message-key contracts;
- profile;
- companion knowledge artifacts;
- application consumers;
- activation and rollback capability.

Unknown required compatibility blocks selection.

### 4.15 Staging

The runtime stages a candidate pack outside active authority.

Staging can perform:

- package verification;
- manifest validation;
- provenance verification;
- compatibility checks;
- extraction;
- local indexing;
- load testing;
- deterministic fixture tests;
- resource checks;
- rollback preparation.

Staged artifacts remain invisible to normal runtime selection.

### 4.16 Activation

Activation changes the active language-pack pointer or equivalent active mapping.

The logical sequence is:

`text
verify package
 ↓
verify compatibility
 ↓
stage complete pack
 ↓
load and test staged pack
 ↓
retain current pack
 ↓
atomically switch active mapping
 ↓
run acceptance checks
 ↓
retain or restore
`

The previous compatible pack remains available until acceptance succeeds.

### 4.17 Installed language set

A runtime loads only packs installed and selected for the effective environment.

For example, one environment can install two locale-specific packs without installing every supported language.

Each pack retains separate:

- identity;
- version;
- activation state;
- compatibility;
- evidence;
- previous version;
- deprecation state.

One failed language pack does not necessarily disable another compatible active pack.

### 4.18 Runtime requests

A runtime request identifies:

- requesting component;
- structured input;
- rendering operation;
- selected language or locale;
- expected runtime contract;
- correlation identity;
- output constraints defined by the calling contract.

The requesting component remains responsible for the authority and meaning of its structured input.

The language runtime owns rendering, not the source business facts.

### 4.19 Data ownership

Language artifacts can encode grammar, lexicon, messages, and rendering rules.

They do not own:

- Orgo workflow data;
- Konnaxion domain data;
- Kristal epistemic source state;
- Ariane navigation state;
- UCKK media state;
- governance policy;
- identity state.

Rendering text from foreign structured data does not transfer ownership.

### 4.20 Derived runtime state

Derived runtime state can include:

- loaded grammar representation;
- message indexes;
- lookup tables;
- rendered-message caches;
- warmup data;
- performance metadata.

Derived state remains rebuildable from:

- the active language artifact;
- runtime configuration;
- declared inputs.

It does not become a second source of language authority.

### 4.21 Compatibility classes

Language-artifact changes can be classified by effect.

| Change | Typical compatibility effect |
| --- | --- |
| Editorial source change with identical runtime semantics | Patch |
| Addition of optional message or compatible language coverage | Minor |
| Change to required message key or structured input | Major |
| Change to grammar interpretation or rendering semantics | Major |
| Change to runtime interface | Major |
| Removal of supported locale or operation | Major |
| Packaging-only change with identical contents and contracts | Patch or minor according to artifact contract |
| Security or integrity metadata update | Classified by runtime and package impact |

The canonical change classifier owns final classification.

### 4.22 Migration

A language migration can be required when:

- message keys change;
- structured-input schemas change;
- consumer contracts change;
- grammar interpretation changes;
- pack structure changes;
- runtime API changes;
- locale identity changes;
- companion artifacts change.

Migration identifies affected consumers and profiles.

A consumer is not silently updated by changing the language artifact alone when its input contract also changes.

### 4.23 Rollback

Rollback restores the previous compatible active pack.

Rollback checks:

- prior pack availability;
- prior runtime compatibility;
- structured-input compatibility;
- cache invalidation;
- profile compatibility;
- companion artifact compatibility;
- receipt and evidence readiness.

A previous pack is not restored when current consumer state is incompatible with it.

### 4.24 Forward repair

Forward repair is required when a change creates an irreversible compatibility transition.

Examples can include:

- removal of input structures after consumer migration;
- pack-store format migration;
- irreversible companion-artifact migration.

The repair plan exists and is tested before publication.

### 4.25 Offline installation

Offline installation uses a registered offline bundle or equivalent controlled artifact transfer.

The offline flow verifies:

- artifact identity;
- signature or integrity evidence;
- provenance;
- language-pack contract;
- Release Set;
- runtime compatibility;
- profile compatibility;
- required companion artifacts;
- rollback or repair material.

Offline installation does not weaken validation.

### 4.26 Backup and recovery

Backup preserves published and active language artifacts separately from rebuildable caches.

Recovery material identifies:

- active pack;
- previous pack;
- Release Set;
- runtime version;
- companion artifacts;
- activation receipts;
- provenance;
- compatibility.

A clean compatible node can restore the selected language environment without GF Wordbench.

### 4.27 Deprecation and retirement

Deprecation identifies:

- deprecated artifact;
- replacement;
- affected consumers;
- affected profiles;
- support period;
- migration path;
- removal condition;
- known compatibility restrictions.

Retirement removes the artifact from new selection while preserving its identity, history, evidence, and required recovery retention.

Retired identifiers remain reserved.

### 4.28 Retention classes

| State | Retention treatment |
| --- | --- |
| Authoritative source | Retained by source-control and project policy |
| Failed local build | Disposable unless diagnostics or evidence require retention |
| Candidate | Retained through review or release disposition |
| Published artifact | Retained by artifact-retention policy |
| Active pack | Retained while active |
| Previous compatible pack | Retained through rollback window |
| Deprecated pack | Retained through support and migration window |
| Retired pack | Retained according to historical, recovery, and legal policy |
| Validation evidence | Retained according to evidence policy |
| Runtime cache | Rebuildable and independently disposable |

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-LIFE-LANG-001,REQ-LIFE-LANG-002,REQ-LIFE-LANG-003,REQ-LIFE-LANG-004,REQ-LIFE-LANG-005,REQ-LIFE-LANG-006,REQ-LIFE-LANG-007,REQ-LIFE-LANG-008,REQ-LIFE-LANG-009,REQ-LIFE-LANG-010,REQ-LIFE-LANG-011,REQ-LIFE-LANG-012,REQ-LIFE-LANG-013,REQ-LIFE-LANG-014,REQ-LIFE-LANG-015,REQ-LIFE-LANG-016,REQ-LIFE-LANG-017,REQ-LIFE-LANG-018,REQ-LIFE-LANG-019,REQ-LIFE-LANG-020,REQ-LIFE-LANG-021,REQ-LIFE-LANG-022,REQ-LIFE-LANG-023,REQ-LIFE-LANG-024,REQ-LIFE-LANG-025,REQ-LIFE-LANG-026,REQ-LIFE-LANG-027,REQ-LIFE-LANG-028,REQ-LIFE-LANG-029,REQ-LIFE-LANG-030,REQ-LIFE-LANG-031,REQ-LIFE-LANG-032,REQ-LIFE-LANG-033,REQ-LIFE-LANG-034,REQ-LIFE-LANG-035,REQ-LIFE-LANG-036,REQ-LIFE-LANG-037,REQ-LIFE-LANG-038,REQ-LIFE-LANG-039,REQ-LIFE-LANG-040 -->
- **REQ-LIFE-LANG-001 — SHALL:** GF Wordbench own language construction, compilation, validation, and candidate packaging.
- **REQ-LIFE-LANG-002 — SHALL:** SemantiK Architect Runtime consume only published compatible compiled language artifacts.
- **REQ-LIFE-LANG-003 — SHALL NOT:** The user runtime include or invoke the GF language-construction toolchain during normal operation.
- **REQ-LIFE-LANG-004 — SHALL:** Each language-artifact build identify one active language project and its declared locale, script, and compatibility target.
- **REQ-LIFE-LANG-005 — SHALL:** Every release-grade language build use identified grammar sources, message sources, GF toolchain, resource grammar inputs, dependency state, and validation fixtures.
- **REQ-LIFE-LANG-006 — SHALL NOT:** Undeclared local files, mutable shared workbench state, editor state, or machine-specific paths influence a published language artifact.
- **REQ-LIFE-LANG-007 — SHALL:** The compiled PGF candidate and its packaging manifest have stable artifact identities.
- **REQ-LIFE-LANG-008 — SHALL:** A language runtime pack bind its compiled PGF, manifest, compatibility declaration, provenance, validation results, and required runtime metadata.
- **REQ-LIFE-LANG-009 — SHALL:** Language-artifact provenance link the source project, source revision, toolchain, resource grammar inputs, build environment, tests, and candidate identity.
- **REQ-LIFE-LANG-010 — SHALL:** Language candidates pass compilation, structural, compatibility, deterministic-rendering, regression, packaging, load, activation, and rollback validation applicable to the artifact.
- **REQ-LIFE-LANG-011 — SHALL:** Validation identify the exact language, locale, PGF candidate, runtime-pack candidate, runtime contract, target profiles, tests, and terminal results.
- **REQ-LIFE-LANG-012 — SHALL NOT:** A skipped, blocked, unavailable, or incomplete language test be represented as passing.
- **REQ-LIFE-LANG-013 — SHALL:** Published language artifacts produce deterministic results for the recorded structured inputs and active artifact versions.
- **REQ-LIFE-LANG-014 — SHALL NOT:** External AI output directly define, compile, validate, publish, activate, or mutate authoritative language artifacts.
- **REQ-LIFE-LANG-015 — SHALL:** Externally assisted language material remain candidate source until reviewed and explicitly adopted into the authoritative language project.
- **REQ-LIFE-LANG-016 — SHALL:** PGF artifacts and language runtime packs be published through the `knowledge` release channel.
- **REQ-LIFE-LANG-017 — SHALL:** A published language artifact retain independent identity, version, provenance, compatibility, and signature or integrity evidence according to its artifact contract.
- **REQ-LIFE-LANG-018 — SHALL NOT:** Publication of a language artifact activate it in a runtime.
- **REQ-LIFE-LANG-019 — SHALL:** A Release Set identify the exact language artifacts compatible with the selected SemantiK Architect Runtime and target profiles.
- **REQ-LIFE-LANG-020 — SHALL:** Independent knowledge-channel language updates preserve declared compatibility with active system, services, governance, runtime, and profile versions.
- **REQ-LIFE-LANG-021 — SHALL:** A runtime stage a complete verified language pack before changing the active language-artifact pointer.
- **REQ-LIFE-LANG-022 — SHALL:** Language-artifact activation be atomic and preserve the previously active compatible pack until the replacement passes load and acceptance checks.
- **REQ-LIFE-LANG-023 — SHALL NOT:** A partially copied, partially verified, partially indexed, or partially loaded language pack become active.
- **REQ-LIFE-LANG-024 — SHALL:** The runtime load only language packs installed and selected for the effective operating environment.
- **REQ-LIFE-LANG-025 — SHALL:** Multiple installed language packs retain separate identities, compatibility, activation, rollback, and evidence state.
- **REQ-LIFE-LANG-026 — SHALL:** Derived language caches remain rebuildable and subordinate to the active published language artifacts.
- **REQ-LIFE-LANG-027 — SHALL NOT:** A cache, rendered message, local patch, or workbench output replace the active published language artifact as authority.
- **REQ-LIFE-LANG-028 — SHALL:** A failed language activation retain or restore the previous compatible language pack.
- **REQ-LIFE-LANG-029 — SHALL:** A language change that prevents safe rollback define and test forward-repair behavior before publication.
- **REQ-LIFE-LANG-030 — SHALL:** Language-artifact backup and offline bundles preserve artifact identity, provenance, compatibility, signatures or integrity evidence, and Release Set relationships.
- **REQ-LIFE-LANG-031 — SHALL:** Offline installation and activation perform the same artifact, compatibility, validation, and atomicity checks as connected installation.
- **REQ-LIFE-LANG-032 — SHALL:** A language artifact declare its supported runtime contract, target language and locale, required companion artifacts, and incompatible predecessor or successor states.
- **REQ-LIFE-LANG-034 — SHALL:** Deprecation identify replacement artifacts, affected profiles and consumers, support window, migration path, and removal conditions.
- **REQ-LIFE-LANG-035 — SHALL NOT:** A retired language-artifact identity or version identifier be reused.
- **REQ-LIFE-LANG-036 — SHALL:** Language source, candidates, published artifacts, active packs, previous packs, validation evidence, and derived caches use distinct retention and authority classifications.
- **REQ-LIFE-LANG-037 — SHALL:** Runtime consumers pass structured inputs through active component contracts and remain responsible for the meaning and authority of those inputs.
- **REQ-LIFE-LANG-038 — SHALL NOT:** SemantiK Architect Runtime acquire ownership of Orgo, Konnaxion, Kristal, Ariane, or another component's source data by rendering language output.
- **REQ-LIFE-LANG-039 — SHALL:** Build, publication, activation, rollback, deprecation, and retirement events produce the receipts and evidence required by the applicable artifact, profile, and release contracts.
- **REQ-LIFE-LANG-040 — SHALL:** A semantic change to language-artifact ownership, packaging, compatibility, release-channel placement, activation, rollback, or runtime consumption use an accepted owner decision and complete impact analysis.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Start a language build session

1. Identify the language project.
2. resolve the source revision.
3. select one active language target for the session.
4. resolve locale, script, and regional variant.
5. resolve GF toolchain and resource grammar inputs.
6. resolve structured-input and runtime contracts.
7. resolve target profiles and compatibility baseline.
8. create an isolated workbench environment.
9. record the build-input manifest.
10. block the session when a required input or decision is unresolved.

### 6.2 Compile a PGF candidate

1. Verify source closure.
2. verify toolchain identity.
3. resolve declared dependencies.
4. run GF compilation.
5. collect compiler diagnostics.
6. create the PGF candidate identity.
7. record provenance.
8. retain the candidate as non-authoritative.
9. reject publication eligibility when compilation or source closure fails.

### 6.3 Build a language runtime pack

1. Select a validated PGF candidate.
2. create the language and locale manifest.
3. declare runtime and resource grammar compatibility.
4. declare structured-input and message compatibility.
5. include required companion artifacts.
6. attach provenance and validation references.
7. define activation, rollback, and deprecation relationships.
8. assemble the immutable candidate package.
9. validate the package against its artifact contract.
10. assign a new candidate identity.

### 6.4 Validate a candidate

1. Resolve the applicable test matrix.
2. run source-closure and reproducibility checks.
3. run compilation and structural checks.
4. run deterministic rendering fixtures.
5. run regression and coverage checks.
6. run runtime compatibility tests.
7. run profile and offline-load tests.
8. run staging, activation, and rollback tests.
9. record every terminal result.
10. bind evidence to the exact candidate identities.
11. keep the candidate blocked when required validation does not pass.

### 6.5 Review and approve

1. Review source changes.
2. review linguistic and message changes.
3. review compatibility impact.
4. review target profiles and consumers.
5. review validation and evidence.
6. resolve active exceptions.
7. freeze candidate content.
8. record approval.
9. create a new candidate if content changes after approval.

### 6.6 Publish to the knowledge channel

1. Verify candidate identity and immutability.
2. verify artifact class.
3. verify provenance and validation evidence.
4. verify signature or integrity requirements.
5. verify compatibility metadata.
6. publish the PGF artifact and language runtime pack as applicable.
7. record publication receipts.
8. retain the artifacts as published but inactive.

### 6.7 Add to a Release Set

1. Select exact published artifact versions.
2. select target profiles.
3. resolve SemantiK Architect Runtime version.
4. resolve structured-input consumer versions.
5. resolve companion knowledge artifacts.
6. run cross-channel compatibility.
7. attach migration, rollback, and forward-repair information.
8. attach tests and evidence.
9. publish the signed compatible Release Set.
10. leave it inactive until deployment activation.

### 6.8 Stage a language pack

1. Resolve the target runtime and profile.
2. verify the active and candidate Release Sets.
3. verify package identity, provenance, and compatibility.
4. copy the complete package into inactive staging.
5. verify extracted or mounted contents.
6. build only derived staging indexes and caches.
7. load the staged pack in an isolated validation context.
8. run local acceptance fixtures.
9. verify rollback readiness.
10. produce staging evidence.

### 6.9 Activate a language pack

1. Obtain activation authority.
2. verify that the staged pack remains unchanged.
3. retain the current compatible pack.
4. atomically change the active language mapping.
5. load the new pack.
6. run runtime acceptance checks.
7. invalidate or segregate incompatible caches.
8. record activation evidence.
9. keep the new pack active only after acceptance passes.

### 6.10 Handle failed activation

1. Stop new requests from selecting the failed pack.
2. preserve diagnostics and staging evidence.
3. determine whether rollback is compatible.
4. restore the previous active mapping when safe.
5. clear or segregate incompatible derived caches.
6. execute forward repair when rollback is unsafe.
7. validate the recovered runtime state.
8. produce failure and recovery receipts.
9. return the candidate to development or supersede it.

### 6.11 Install from an offline bundle

1. Receive the bundle through the approved offline boundary.
2. quarantine the bundle.
3. verify transfer authority.
4. verify artifact and Release Set identity.
5. verify provenance and signatures or integrity evidence.
6. verify complete companion artifacts.
7. stage the language pack.
8. run local compatibility and acceptance checks.
9. activate atomically.
10. retain local receipts and recovery artifacts.

### 6.12 Deprecate or retire

1. Identify the artifact and affected consumers.
2. identify the replacement.
3. classify compatibility and migration.
4. publish deprecation metadata.
5. update Release Set selection policy.
6. preserve support and rollback material.
7. prevent new selection after retirement.
8. preserve identity and historical evidence.
9. never reuse the retired identifier.

## 7. Failure States and Safe Degradation

| Failure condition | Required response | Preserved state | Blocked transition |
| --- | --- | --- | --- |
| Language project is unresolved | Block build | Existing published artifacts | Candidate creation |
| GF toolchain is unresolved | Block build | Source project and active runtime | Compilation |
| Required grammar dependency is missing | Block build | Existing candidates and active packs | Compilation |
| Compilation fails | Retain diagnostics | Source and active packs | PGF candidate approval |
| Reproducibility fails | Reject candidate | Existing published and active artifacts | Publication |
| Manifest or package validation fails | Reject package | Valid PGF candidate when separately valid | Runtime-pack publication |
| Required language test fails | Return candidate to development | Active pack | Publication |
| Required test is skipped or unavailable | Mark validation blocked | Active pack | Passing release claim |
| Provenance is incomplete | Reject candidate | Source and diagnostics | Publication |
| Runtime compatibility is unknown | Reject Release Set selection | Published artifact | Staging |
| Profile compatibility is unknown | Reject target-profile selection | Other compatible profiles | Installation |
| Package verification fails | Quarantine package | Active pack | Staging |
| Staging is incomplete | Remove or isolate staging | Active pack | Activation |
| Staged load fails | Keep candidate inactive | Active pack | Activation |
| Atomic switch fails | Preserve or restore active mapping | Previous pack | Candidate authority |
| Post-activation acceptance fails | Roll back or forward repair | Recoverable runtime state | Release acceptance |
| Previous pack is incompatible | Use declared forward repair | Current recoverable state | Blind rollback |
| Runtime cache is corrupt | Rebuild cache | Active published pack | Cache use |
| One installed language fails | Disable affected language | Other compatible languages | Failed language selection |
| External AI is unavailable | No effect on native lifecycle | Build and runtime without external AI | Optional external assistance |
| Offline bundle is incomplete | Reject import | Local active packs | Offline staging |
| Evidence storage is unavailable | Block receipt-required transition | Active pack | Activation or retirement claim |
| Retired artifact is requested | Reject new activation | Historical retention | New selection |

Failure does not permit runtime compilation, partial pack activation, unverified package use, external AI substitution, or cache authority.

## 8. Cross-Component Interactions

### 8.1 GF Wordbench

GF Wordbench owns:

- language-project session;
- build environment;
- compilation;
- candidate packaging;
- workbench validation;
- candidate provenance;
- submission for publication.

It does not activate runtime artifacts directly.

### 8.2 SemantiK Architect Runtime

SemantiK Architect Runtime owns:

- installed-pack state;
- staged-pack state;
- active language mapping;
- deterministic rendering;
- derived caches;
- runtime health;
- activation and rollback results.

It does not edit or compile language sources during normal operation.

### 8.3 Product components

Orgo, Konnaxion, and other callers provide structured input through their active contracts.

The caller owns the input facts and interprets the result in its own workflow.

The language runtime owns only the rendering operation and its runtime evidence.

### 8.4 Kristal Runtime

Kristal can supply registered epistemic references or companion knowledge artifacts through active contracts.

Language artifacts do not absorb Kristal authority.

Kristal artifacts and language artifacts can share the `knowledge` release channel while retaining separate artifact identities and owners.

### 8.5 Ariane Runtime

Ariane can consume language output for local interaction when its contract selects the runtime.

Ariane local navigation remains available according to its own degradation contract.

A language-pack failure does not authorize external voice or external AI as a silent substitute.

### 8.6 Release and artifact services

Artifact publication verifies and stores immutable language artifacts.

Release Set assembly verifies compatibility across the knowledge channel and other required channels.

Publication and selection do not activate the runtime.

### 8.7 Identity and Trust

Identity and Trust verifies builders, signers, artifacts, Release Sets, and activation requests where required.

Signature verification does not replace semantic and runtime validation.

### 8.8 Governance Policy Runtime

A profile can require policy evaluation for publication, privileged activation, exception use, or offline import.

Governance Policy Runtime does not compile or render language artifacts.

### 8.9 Audit Broker

Audit Broker receives selected build, publication, activation, rollback, exception, and retirement evidence.

It does not store unrestricted grammar source or become the owner of language artifacts.

### 8.10 External AI

An approved external AI surface can provide candidate drafting assistance only through an explicit workflow.

Adopted content enters the authoritative language project and receives the complete build and release lifecycle.

The external output itself never becomes a runtime pack.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Closed decisions

| Decision | Closed choice |
| --- | --- |
| `DEC-REL-001` | PGF artifacts and language runtime packs belong to the independently versioned `knowledge` channel |
| `DEC-PROFILE-001` | Installed and active language sets remain profile-specific |
| `DEC-AI-001` | Native language rendering is deterministic and does not depend on external AI |
| `DEC-DATA-001` | Rendering does not transfer ownership of caller data |

### 9.2 Protected locks

| Lock | Protected relationship |
| --- | --- |
| `LOCK-COMP-002` | User runtime consumes compiled artifacts; language construction remains in GF Wordbench |
| `LOCK-AI-001` | Runtime language output does not introduce native generative AI |
| `LOCK-AI-002` | External AI output cannot directly mutate authoritative language artifacts |
| `LOCK-DATA-001` | The runtime cannot write directly into caller-owned source state |
| `LOCK-PROFILE-001` | Installed language requirements remain profile-specific |
| `LOCK-LIFE-001` | Language artifacts do not activate partially |
| `LOCK-LIFE-002` | Artifact classes define rollback or forward repair |
| `LOCK-LIFE-003` | Release Sets bind compatible versions |
| `LOCK-LIFE-004` | Independent knowledge updates preserve compatibility |
| `LOCK-IMPL-001` | A workbench recipe or runtime implementation does not redefine lifecycle authority |

### 9.3 Prohibited assumptions

The following assumptions are invalid:

- the runtime compiles grammars;
- GF Wordbench is required on a user system;
- successful compilation proves release eligibility;
- a PGF file without manifest and compatibility data is an activable language pack;
- a local workbench output is published;
- publication activates a pack;
- the newest language pack is automatically compatible;
- version numbers alone prove compatibility;
- every profile installs every language;
- one installed language failure disables every language;
- a cached rendering becomes language authority;
- a runtime cache can survive incompatible artifact changes without validation;
- an external AI result can be compiled and activated without review;
- external AI unavailability affects native deterministic rendering;
- a signature proves linguistic or runtime correctness;
- the `knowledge` channel can silently change service or governance authority;
- a language update can silently change a caller's structured-input contract;
- a runtime can infer missing locale or target-profile authority;
- an incomplete offline bundle is acceptable because the node is disconnected;
- rollback is always safe;
- forward repair can be designed after an irreversible change;
- a retired identifier can be reused;
- a rendered sentence transfers ownership of source facts to the runtime;
- historical language documentation overrides active artifact contracts;
- workbench implementation details create release requirements.

Missing source, toolchain, compatibility, validation, profile, Release Set, activation, or recovery authority blocks the affected lifecycle transition.

## 10. Validation Criteria

This document is conformant when:

1. the document is registered as `DOC-LIFE-009`;
2. the path is `06-lifecycle/09-language-artifacts.md`;
3. the active language is English;
4. scope resolves to PGF artifacts, language runtime packs, and the `knowledge` channel;
5. GF Wordbench and SemantiK Architect Runtime resolve as separate components;
6. build and runtime responsibilities do not overlap;
7. the runtime has no normal-operation compiler dependency;
8. each build identifies one active language project;
9. source, toolchain, grammar dependencies, fixtures, and target contracts are identified;
10. undeclared local inputs are absent;
11. PGF and runtime-pack candidate identities are stable and unique;
12. language-pack structure validates against its artifact contract;
13. provenance binds exact source, toolchain, candidate, and tests;
14. reproducibility meets the artifact-class requirement;
15. all applicable language and runtime tests execute;
16. skipped or blocked tests are not reported as passing;
17. deterministic rendering tests pass;
18. external AI is absent from native build authority and runtime authority;
19. PGF and runtime packs publish only through `knowledge`;
20. publication does not alter runtime activation;
21. Release Set compatibility resolves;
22. staged packs remain inactive;
23. activation is atomic;
24. partial packages cannot become active;
25. previous compatible packs remain available through acceptance;
26. installed language selection matches the effective profile;
27. multiple language packs retain separate lifecycle state;
28. caches are derived and rebuildable;
29. failed activation rolls back or forward repairs;
30. offline installation applies equivalent checks;
31. compatibility declarations cover runtime, structured input, profiles, and companion artifacts;
33. deprecation and retirement preserve identifiers and history;
34. backup and recovery preserve active and previous pack relationships;
35. caller data ownership remains with callers;
36. receipts and evidence cover build, publication, activation, rollback, and retirement;
37. all 40 linked requirements resolve;
38. all required tests execute;
39. all required evidence validates;
40. no unresolved language-artifact authority exists;
41. generated catalogs and AI contexts match canonical authority;
42. complete documentation validation passes.

Expected test coverage includes:

`text
TEST-LIFE-LANG-001 GF Wordbench and runtime separation
TEST-LIFE-LANG-002 One active language project per build session
TEST-LIFE-LANG-003 Release-grade source and toolchain closure
TEST-LIFE-LANG-004 PGF compilation
TEST-LIFE-LANG-005 Language-pack schema validation
TEST-LIFE-LANG-006 Candidate provenance
TEST-LIFE-LANG-007 Reproducible language build
TEST-LIFE-LANG-008 Deterministic rendering
TEST-LIFE-LANG-009 Structured-input compatibility
TEST-LIFE-LANG-010 Regression and coverage
TEST-LIFE-LANG-011 External AI non-authority
TEST-LIFE-LANG-012 Knowledge-channel publication
TEST-LIFE-LANG-013 Release Set compatibility
TEST-LIFE-LANG-014 Inactive staging
TEST-LIFE-LANG-015 Atomic language-pack activation
TEST-LIFE-LANG-016 Previous-pack rollback
TEST-LIFE-LANG-017 Forward-repair readiness
TEST-LIFE-LANG-018 Multiple installed language isolation
TEST-LIFE-LANG-019 Derived-cache rebuild
TEST-LIFE-LANG-020 Offline bundle installation
TEST-LIFE-LANG-021 Deprecation and retirement
TEST-LIFE-LANG-022 Caller data-authority preservation
TEST-LIFE-LANG-023 Receipt and evidence completeness
`

The test catalog and evidence registry own executable tests and evidence definitions.

This document does not claim that those tests have already executed.

## 11. Non-Normative Examples

> **Non-normative example:** These examples illustrate valid lifecycle behavior. They do not redefine component or artifact contracts.

### 11.1 Build and publish one locale

GF Wordbench opens one active `fr-CA` language project.

A clean build environment compiles the grammar and produces a PGF candidate.

The workbench packages the candidate with its language manifest, runtime compatibility, provenance, and validation evidence.

The artifact is published to the `knowledge` channel and later selected by a compatible Release Set.

### 11.2 Two installed languages

A profile installs `fr-CA` and `en-CA`.

Each pack has separate identity, version, compatibility, activation state, previous version, and evidence.

A failed `en-CA` update leaves the accepted `fr-CA` pack active.

### 11.3 Deterministic message rendering

Orgo sends a registered structured message input and selects `fr-CA`.

SemantiK Architect Runtime renders using the active `fr-CA` pack.

Repeated requests with the same semantic input and active versions produce the same semantic output.

Orgo retains ownership of the workflow facts.

### 11.4 Cached message

A frequently used parameterized message is rendered and cached.

The cache key includes the relevant active pack and input-contract versions.

After language-pack activation, incompatible cache entries are invalidated.

The cache never replaces the active language pack.

### 11.5 Failed activation

A new language pack passes package verification but fails local deterministic acceptance after staging.

The active mapping remains on the previous pack.

The failed candidate and diagnostics return to development.

No user request observes a partially loaded pack.

### 11.6 Offline sovereign installation

A signed Release Set and language pack arrive in an approved offline bundle.

The sovereign node quarantines and verifies the bundle, stages the complete pack, runs local compatibility tests, and activates it atomically.

GF Wordbench is not installed on the node.

### 11.7 External drafting assistance

A language developer uses an approved external AI surface to suggest candidate wording.

The developer reviews the suggestion and edits the authoritative language source.

The resulting source change receives normal compilation, regression, compatibility, publication, and activation validation.

The external response is not itself a language artifact.

### 11.8 Breaking message-key change

A language project removes a required message key used by Konnaxion.

The change is major because the structured-input contract changes.

Konnaxion, the language pack, profile compatibility, migration, tests, and Release Set are updated together.

### 11.9 Invalid runtime compilation

A runtime deployment downloads grammar source and compiles a new PGF when a message is missing.

The deployment is invalid.

The correct path returns the issue to GF Wordbench, publishes a validated replacement, and activates it through the lifecycle.

### 11.10 Invalid partial package

A deployment copies a new PGF into the active directory before its manifest, compatibility data, and validation state are available.

The deployment exposes partial authority and is invalid.
