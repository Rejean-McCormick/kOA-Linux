<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-013",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "system",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/language_runtime",
    "generated/component-catalog.json#/components/semantik_architect_runtime",
    "generated/component-catalog.json#/components/gf_wordbench",
    "contracts/subsystems/semantik-architect.subsystem.json",
    "contracts/artifact-classes.contract.json#/artifact_classes/language_pack",
    "contracts/release-channels.contract.json#/channels/knowledge",
    "generated/profile-catalog.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-COMP-001",
    "DEC-PROFILE-BASELINE-001",
    "DEC-AI-001",
    "DEC-REL-001",
    "DEC-HW-001"
  ],
  "requirement_ids": [
    "REQ-SYS-LANG-001",
    "REQ-SYS-LANG-002",
    "REQ-SYS-LANG-003",
    "REQ-SYS-LANG-004",
    "REQ-SYS-LANG-005",
    "REQ-SYS-LANG-006",
    "REQ-SYS-LANG-007",
    "REQ-SYS-LANG-008",
    "REQ-SYS-LANG-009",
    "REQ-SYS-LANG-010",
    "REQ-SYS-LANG-011",
    "REQ-SYS-LANG-012",
    "REQ-SYS-LANG-013",
    "REQ-SYS-LANG-014",
    "REQ-SYS-LANG-015",
    "REQ-SYS-LANG-016",
    "REQ-SYS-LANG-017",
    "REQ-SYS-LANG-018",
    "REQ-SYS-LANG-019",
    "REQ-SYS-LANG-020"
  ],
  "lock_ids": [
    "LOCK-COMP-002",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-DATA-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-DEV-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CON-006",
    "DOC-SYS-000",
    "DOC-SYS-002",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-006",
    "DOC-SYS-008",
    "DOC-SYS-009"
  ],
  "tags": [
    "language-runtime",
    "semantik-architect",
    "gf-wordbench",
    "pgf",
    "deterministic-rendering",
    "offline",
    "language-pack"
  ]
}
KOA:DOC-META:END -->

# Language Runtime

## 1. Purpose

This document defines the global language-runtime architecture of the kOA operating environment.

It establishes the separation between language construction and language execution:

- **GF Wordbench** develops, compiles, validates, and publishes language artifacts;
- **SemantiK Architect Runtime** consumes published language artifacts and renders deterministic text from structured inputs.

The architecture exists to provide multilingual behavior that is:

- deterministic;
- available offline;
- independent from generative AI;
- reproducible from versioned language artifacts;
- lightweight in user profiles;
- isolated from development tools;
- compatible with atomic activation and recovery;
- traceable to the language pack, grammar entry point, and structured input used for a render.

The runtime is not a general text-generation service. It does not infer intent, invent facts, resolve missing authority, classify arbitrary content, translate through an AI model, or modify canonical data.

## 2. Scope

This document applies globally to:

- SemantiK Architect Runtime;
- GF Wordbench;
- compiled PGF artifacts;
- language-pack manifests;
- runtime language selection;
- structured rendering requests;
- reusable static and parameterized messages;
- language-pack installation, activation, rollback, and removal;
- runtime caches and derived renderings;
- profile-specific resource and language-loading policies;
- component integrations that request deterministic language output;
- release, evidence, backup, restore, and conformance behavior for language artifacts.

It applies to every deployment profile that provides language-runtime capability.

This document does not define:

- the internal grammar source layout used by GF Wordbench;
- the complete GF toolchain command set;
- linguistic content for a specific language;
- application-specific message catalogs;
- user-interface copy;
- arbitrary translation policy;
- external AI or voice-service behavior;
- profile-specific storage paths, service units, containers, or process topology.

Those facts belong to the applicable component contract, toolchain contract, profile contract, artifact contract, application contract, or implementation recipe.

A profile may limit the number of simultaneously loaded language packs or workers. It does not change the published language artifact, rendering semantics, or separation between build and runtime responsibilities.

## 3. Canonical References

| Canonical reference | Ownership |
| --- | --- |
| `contracts/system.contract.json#/language_runtime` | Global language-runtime model, supported operating conditions, pack activation model, and rendering classes. |
| `generated/component-catalog.json#/components/semantik_architect_runtime` | Runtime identity, high-level responsibility, dependencies, and owned state. |
| `generated/component-catalog.json#/components/gf_wordbench` | Workbench identity, high-level responsibility, dependencies, and owned build state. |
| `contracts/components/semantik-architect-runtime.component.json` | Detailed runtime interfaces, commands, events, state transitions, failures, and receipts. |
| `contracts/components/gf-wordbench.component.json` | Detailed language-build interfaces, validation, publication, and evidence behavior. |
| `contracts/artifact-classes.contract.json#/artifact_classes/language_pack` | Language-pack artifact identity, required members, compatibility, integrity, activation, and retention. |
| `contracts/release-channels.contract.json#/channels/knowledge` | Release channel for published language packs and related knowledge artifacts. |
| `generated/profile-catalog.json` | Profile and overlay inventory used to determine installation and resource policy. |
| `generated/requirements-index.json` | Normative statements displayed in Section 5. |
| `generated/assertion-index.json` | Cross-file invariants for build/runtime separation, AI exclusion, profiles, data, development, and lifecycle. |
| `generated/traceability.json` | Links among decisions, language artifacts, components, profiles, requirements, tests, and evidence. |
| `generated/evidence-catalog.json` | Build, validation, activation, rollback, compatibility, and conformance evidence. |

This document explains the language-runtime architecture. It does not become a second owner of language-pack fields, component interfaces, release-channel membership, profile limits, or artifact compatibility rules.

Artifact integrity digests used for PGF and language-pack verification are part of the artifact contract. They are distinct from documentation-file hashing, which is not required for ordinary Markdown validation.

## 4. Model and Responsibilities

### 4.1 Architectural split

The language system contains two separate component responsibilities.

| Responsibility | Canonical component |
| --- | --- |
| Edit grammar sources and linguistic resources | GF Wordbench |
| Compile source grammar into PGF | GF Wordbench |
| Validate grammar coverage and test cases | GF Wordbench |
| Assemble and publish language packs | GF Wordbench |
| Load an installed compatible language pack | SemantiK Architect Runtime |
| Validate a pack before runtime activation | SemantiK Architect Runtime |
| Render deterministic text from structured input | SemantiK Architect Runtime |
| Cache reusable deterministic rendering | SemantiK Architect Runtime |
| Report runtime pack and rendering status | SemantiK Architect Runtime |

The runtime package does not include the GF build factory, grammar-source editing environment, repair tools, development scenarios, or unpublished build state.

GF Wordbench does not become a required user-profile service merely because it produces runtime artifacts.

### 4.2 Deterministic rendering model

A rendering request contains a declared language, a declared grammar entry point or message identifier, structured parameters, and caller context permitted by the runtime contract.

The runtime:

1. resolves the active compatible language pack;
2. validates the request shape and parameter types;
3. selects the declared grammar entry point or reusable message;
4. executes the compiled PGF path;
5. returns text and machine-readable provenance;
6. does not add undeclared facts or inferred parameters.

Equivalent requests against the same active artifact and compatible runtime produce semantically equivalent output. Exact byte equality may vary only where the canonical contract explicitly permits formatting, Unicode normalization, or platform-independent serialization differences.

### 4.3 Rendering hierarchy

The preferred execution order is:

1. static message catalog entry;
2. validated parameterized message;
3. previously validated cached rendering;
4. deterministic PGF rendering.

This hierarchy reduces runtime cost without introducing AI or changing semantic authority.

A cached rendering is derived and non-authoritative. Its cache key includes the active language-pack identity, rendering entry point, normalized input, and relevant runtime-contract version.

### 4.4 Language pack

A language pack is a versioned knowledge artifact prepared for runtime consumption.

The canonical artifact contract defines its exact structure. At minimum, the pack identifies:

- language tag;
- pack identifier and version;
- compiled PGF artifact;
- manifest version;
- GF version used to build it;
- relevant Resource Grammar Library revision or equivalent grammar dependency identity;
- runtime-contract compatibility;
- build provenance;
- creation time;
- integrity digest for the PGF and package members;
- validation evidence references;
- supported entry points or capability declarations;
- dependency and compatibility constraints.

A language pack contains runtime artifacts only. It does not contain executable build scripts, mutable build environments, unpublished grammar sources, credentials, or developer workspace state unless a separate artifact class explicitly defines such content for development use.

### 4.5 Installed, active, and candidate packs

A pack may be:

- **candidate** — transferred or staged but not active;
- **installed** — verified and locally available;
- **active** — selected for runtime requests within its declared language and profile scope;
- **inactive** — installed but not selected;
- **retained predecessor** — preserved as a compatible rollback target;
- **rejected** — failed integrity, compatibility, contract, or validation checks;
- **retired** — intentionally removed from active use under lifecycle policy.

Installation does not imply activation.

A candidate pack has no runtime authority until verification and activation complete.

### 4.6 Language selection

The runtime loads only installed language packs required by the active environment and profile.

Multiple language packs may be installed. The active loaded set is profile-controlled.

The user-lightweight profile normally loads one active language at a time to preserve memory, while allowing an explicit language switch or a profile-defined bounded multilingual set. A higher-capacity profile may load more than one pack when its resource envelope permits it.

A language tag, locale, and pack identifier are explicit. The runtime does not infer a language from arbitrary user content unless a separately authorized deterministic input contract provides that value.

### 4.7 GF Wordbench sessions

GF Wordbench is a selectable developer workbench.

One Wordbench session targets one active language project at a time. Separate sessions or workspaces may target different languages when the development profile provides independent identities, dependencies, ports, temporary data, storage, and resource budgets.

The active language-project rule prevents accidental cross-language mutation inside one mutable build session. It does not prohibit parallel isolated workspaces.

### 4.8 Build outputs

A successful GF Wordbench publication produces the objects required by the language-pack artifact contract, including:

- compiled PGF;
- language-pack manifest;
- integrity records;
- validation reports;
- compatibility report;
- release evidence;
- test evidence;
- publication receipt.

Temporary builds, diagnostics, generated intermediate files, and local caches remain outside the published runtime pack.

### 4.9 Runtime outputs

A successful runtime response includes or makes available:

- rendered text;
- language tag;
- active pack identifier and version;
- runtime-contract version;
- rendering entry point or message identifier;
- status;
- deterministic error code when rendering fails;
- provenance or receipt reference when required by the caller contract.

The rendered text is an output of the owning application's structured data and the active language artifact. It does not become a new owner of the input facts.

### 4.10 Offline baseline

SemantiK Architect Runtime operates locally with installed packs and does not require Internet access.

GF Wordbench may also operate offline when its declared toolchain, source dependencies, and build inputs are locally available.

Network access is not introduced during rendering. Any retrieval of new language packs occurs through an explicit lifecycle or synchronization operation, not as a hidden rendering side effect.

### 4.11 AI boundary

The native language runtime is deterministic and non-AI.

It does not perform:

- generative text completion;
- semantic invention;
- autonomous rewriting;
- AI translation;
- AI classification;
- AI summarization;
- embedding generation;
- autonomous routing;
- model-based intent inference;
- autonomous agent execution.

External AI output may be presented to a separate authorized workflow as candidate input. It does not enter a language pack or mutate application state without explicit review, validation, and owner-controlled import.

### 4.12 Resource model

SemantiK Architect Runtime belongs to the regular user-runtime envelope.

The Resource Governor may control:

- number of runtime workers;
- number of loaded packs;
- memory limits;
- render concurrency;
- cache size;
- idle unloading;
- build-task priority;
- GF Wordbench resource budgets.

The lightweight profile normally uses one runtime worker and one active language pack. This is a profile resource policy, not a global semantic limitation.

Resource pressure may reduce concurrency, unload inactive packs, clear reproducible caches, or queue requests. It does not change grammar authority, choose a different language, invoke AI, or load an unverified pack.

### 4.13 Data ownership

GF Wordbench owns mutable language-development state within its workspace and contract.

SemantiK Architect Runtime owns runtime installation state, active-pack selection state, runtime cache state, and runtime health state within its component boundary.

Application components own the structured facts they submit for rendering.

The runtime does not write to application authoritative stores. Applications do not write directly to runtime installation or activation state.

### 4.14 Compatibility

Compatibility is evaluated among:

- language-pack contract version;
- PGF format and GF runtime compatibility;
- runtime-contract version;
- supported entry points;
- application request contract;
- target platform and profile constraints;
- knowledge release and Release Set constraints.

A version number alone does not prove compatibility.

### 4.15 Security and integrity

The runtime loads only verified packs from declared installation locations through its component contract.

A pack that fails schema, integrity, provenance, compatibility, or policy validation is rejected.

Rendering inputs are bounded by declared schemas. Untrusted text parameters remain data and do not become grammar source, executable code, file paths, commands, or unrestricted format strings.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SYS-LANG-001,REQ-SYS-LANG-002,REQ-SYS-LANG-003,REQ-SYS-LANG-004,REQ-SYS-LANG-005,REQ-SYS-LANG-006,REQ-SYS-LANG-007,REQ-SYS-LANG-008,REQ-SYS-LANG-009,REQ-SYS-LANG-010,REQ-SYS-LANG-011,REQ-SYS-LANG-012,REQ-SYS-LANG-013,REQ-SYS-LANG-014,REQ-SYS-LANG-015,REQ-SYS-LANG-016,REQ-SYS-LANG-017,REQ-SYS-LANG-018,REQ-SYS-LANG-019,REQ-SYS-LANG-020 -->
- **REQ-SYS-LANG-001 — SHALL:** SemantiK Architect Runtime shall render language output only from active, verified, compatible, compiled language artifacts.
- **REQ-SYS-LANG-002 — SHALL NOT:** The user language runtime shall not contain or invoke the GF build factory, grammar-source editor, repair workbench, or unpublished build environment during normal operation.
- **REQ-SYS-LANG-003 — SHALL:** GF Wordbench shall own language development, compilation, validation, and publication responsibilities.
- **REQ-SYS-LANG-004 — SHALL:** One GF Wordbench session shall target exactly one active language project.
- **REQ-SYS-LANG-005 — SHALL:** A language pack shall declare its identity, language tag, version, compiled PGF, runtime compatibility, build provenance, integrity records, supported capabilities, and validation evidence.
- **REQ-SYS-LANG-006 — SHALL:** Language-pack installation and activation shall be separate state transitions.
- **REQ-SYS-LANG-007 — SHALL:** Activation shall be atomic and shall preserve a compatible rollback target or an explicit forward-repair path.
- **REQ-SYS-LANG-008 — SHALL NOT:** A candidate, rejected, incompatible, partially transferred, or partially activated language pack shall not serve runtime requests.
- **REQ-SYS-LANG-009 — SHALL:** Rendering requests shall use declared structured inputs, explicit language selection, and a declared rendering entry point or message identifier.
- **REQ-SYS-LANG-010 — SHALL NOT:** The runtime shall not invent missing facts, infer undeclared parameters, or treat rendered text as the authoritative source of application data.
- **REQ-SYS-LANG-011 — SHALL:** Runtime rendering shall remain deterministic for the same compatible artifact, entry point, normalized input, and runtime-contract version.
- **REQ-SYS-LANG-012 — SHALL:** Static messages, validated parameterized messages, and compatible cached renderings may be reused before invoking PGF rendering.
- **REQ-SYS-LANG-013 — SHALL:** Every cached rendering shall remain derived, invalidatable, and bound to the active language-pack and input identity.
- **REQ-SYS-LANG-014 — SHALL:** SemantiK Architect Runtime shall operate offline with installed packs and shall not retrieve network content as a hidden rendering side effect.
- **REQ-SYS-LANG-015 — SHALL NOT:** The native language runtime shall perform generative AI, AI translation, AI classification, AI summarization, embedding generation, autonomous routing, or autonomous agent execution.
- **REQ-SYS-LANG-016 — SHALL:** Profile resource policies may limit loaded packs, workers, concurrency, and cache size without changing language-artifact authority or rendering semantics.
- **REQ-SYS-LANG-017 — SHALL:** Application components shall retain ownership of structured facts submitted for rendering, and the runtime shall not write directly to their authoritative stores.
- **REQ-SYS-LANG-018 — SHALL:** Every runtime result shall expose sufficient identity and status information to determine the language pack, version, runtime contract, and rendering entry point used.
- **REQ-SYS-LANG-019 — SHALL:** Pack activation, rollback, rejection, and recovery shall produce the evidence required by the active lifecycle and conformance contracts.
- **REQ-SYS-LANG-020 — SHALL NOT:** A profile, application, external service, or implementation recipe shall silently merge GF Wordbench and SemantiK Architect Runtime responsibilities.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Building a language pack

GF Wordbench follows this sequence:

1. open one isolated language-project workspace;
2. resolve the declared toolchain and grammar dependencies;
3. validate source identity and workspace state;
4. compile the grammar into a candidate PGF;
5. run grammar, coverage, regression, compatibility, and fixture tests;
6. assemble the candidate language-pack manifest;
7. compute artifact-integrity records required by the artifact contract;
8. produce validation and release evidence;
9. reject the candidate when any required check fails;
10. publish the accepted pack to the knowledge release channel;
11. preserve source revision and build provenance.

A local successful compilation is not a published language pack until the publication transition completes.

### 6.2 Installing a language pack

The installation authority:

1. receives the complete candidate artifact;
2. validates the artifact-class schema;
3. verifies package and PGF integrity;
4. verifies provenance and release-channel membership;
5. checks runtime, platform, profile, and dependency compatibility;
6. stores the pack in a candidate location;
7. performs a bounded load test;
8. records installation evidence;
9. marks the pack installed but inactive.

A failed candidate is quarantined or removed according to lifecycle policy.

### 6.3 Activating a language pack

Activation follows this order:

1. select an installed compatible candidate;
2. verify that required runtime entry points are present;
3. load the candidate in an isolated activation context;
4. execute activation smoke tests and representative render fixtures;
5. preserve the current compatible pack as rollback target when required;
6. atomically switch the active-pack reference;
7. invalidate caches bound to the predecessor when necessary;
8. publish activation status and evidence;
9. release predecessor resources only after the new active pack remains healthy.

No request is served from a partially activated pack.

### 6.4 Rendering

For each request, the runtime:

1. authenticates or identifies the caller as required by the component contract;
2. validates the request schema;
3. resolves the explicit language and active pack;
4. validates the rendering entry point and parameters;
5. attempts a compatible static, parameterized, or cached result;
6. otherwise executes the compiled PGF rendering;
7. returns text, status, and provenance fields;
8. emits operational evidence only when required by the calling contract.

Rendering errors do not modify application state.

### 6.5 Switching active language

A profile-controlled language switch:

1. confirms that the target pack is installed and compatible;
2. verifies available resources;
3. drains or completes in-flight requests according to contract;
4. activates or loads the target pack;
5. updates the active-language selection atomically;
6. invalidates incompatible cache entries;
7. unloads the previous pack when the profile limit requires it;
8. reports the resulting active language.

The runtime does not infer the switch from arbitrary text.

### 6.6 Updating a pack

An update is installed as a new candidate and follows the full validation and activation process.

An update does not overwrite the active pack in place.

Compatibility with applications and Release Sets is checked before activation.

### 6.7 Rollback

Rollback is allowed when the retained predecessor remains compatible with current runtime and application contracts.

The runtime:

1. stops new requests to the failed candidate;
2. records the failure;
3. atomically reselects the retained predecessor;
4. invalidates candidate-bound caches;
5. runs recovery smoke tests;
6. emits rollback evidence;
7. quarantines the failed candidate.

When rollback is unsafe, the capability remains blocked or read-only according to the active safe-degradation contract until forward repair succeeds.

### 6.8 Removing a pack

A pack may be removed only when it is inactive, not required by the active profile or Release Set, not the sole compatible rollback target, and not referenced by an active in-flight operation.

Removal preserves required release and evidence records.

### 6.9 Restoring language capability

Restore operations recover published language packs, manifests, activation state, and configuration separately from reproducible caches.

The restored pack is reverified before activation. Restored cache entries may be discarded and regenerated.

## 7. Failure States and Safe Degradation

| Failure state | Required response |
| --- | --- |
| No compatible installed pack for the requested language | Reject the request with a deterministic unavailable-language result; do not infer another language. |
| Pack manifest is invalid | Reject installation or activation and preserve the current active pack. |
| PGF or package integrity fails | Quarantine or remove the candidate; do not load it. |
| Runtime compatibility fails | Keep the candidate inactive and report the compatibility mismatch. |
| Required rendering entry point is missing | Reject that request; do not substitute an unrelated entry point. |
| Request parameters are invalid | Return a bounded validation error; do not coerce undeclared values. |
| Active pack fails after activation | Stop new use, preserve evidence, and roll back or enter forward repair. |
| Cache is corrupt or incompatible | Discard the cache entry and regenerate from the active pack. |
| Resource pressure exceeds profile limits | Reduce concurrency, unload inactive packs, clear derived caches, or queue requests. |
| GF Wordbench is unavailable | Existing published language packs remain usable; new language builds are unavailable. |
| Network is unavailable | Installed language packs continue to render locally; synchronization and new downloads are unavailable. |
| Knowledge release channel is unavailable | Existing installed packs continue; no unpublished candidate becomes active. |
| Evidence cannot be recorded for an evidence-required activation | Block activation and keep the current active pack. |
| Caller application is unavailable | The runtime preserves its own valid state and does not assume the application's responsibility. |
| External AI service is unavailable | No native language-runtime capability is affected because rendering does not depend on AI. |

A missing pack may make a language capability unavailable. It does not justify automatic external translation, generative output, or installation from an undeclared source.

## 8. Cross-Component Interactions

### 8.1 GF Wordbench

GF Wordbench publishes validated language packs. It never edits the runtime's active-pack state directly.

Publication passes through the declared artifact and release lifecycle.

### 8.2 SemantiK Architect Runtime

The runtime owns pack installation state, active selection, deterministic rendering, cache management, runtime health, and runtime evidence within its boundary.

It does not own application facts or grammar development.

### 8.3 Orgo

Orgo may request deterministic rendering of task, workflow, or organizational data that it owns.

Orgo supplies structured values and retains authority over those values. Rendered text is a presentation of Orgo-owned state.

### 8.4 Konnaxion

Konnaxion may request deterministic rendering for its registered product-domain records and interactions.

The runtime does not write Konnaxion records or become their source authority.

### 8.5 Ariane Runtime

Ariane may use language packs for local navigation labels, prompts, confirmations, and deterministic interaction text.

Ariane external voice remains a separate optional integration. Voice unavailability does not affect local text rendering.

### 8.6 Kristal Runtime

Kristal Runtime may present language-dependent content from verified Kristal or Runtime Pack artifacts according to its own contracts.

Kristal identity, language-pack identity, and application workflow state remain separate.

### 8.7 Identity and Trust

Identity and Trust may authenticate callers, packages, publishers, or trust roots according to profile and lifecycle contracts.

It does not choose linguistic output or grammar content.

### 8.8 Governance Policy Runtime

The Governance Policy Runtime may decide whether a caller may access a protected rendering capability or disclose protected input values.

It does not perform rendering or modify language artifacts.

### 8.9 Resource Governor

The Resource Governor enforces worker, memory, concurrency, cache, and build limits.

It does not choose language semantics or approve artifacts.

### 8.10 kOA Node Agent

The Node Agent may install, activate, roll back, or restore packs through narrow lifecycle commands when its profile assigns that responsibility.

Application components do not inherit the Node Agent's host privilege.

### 8.11 Audit Broker and evidence system

Build, publication, activation, rollback, rejection, and recovery events are emitted according to their contracts.

Ordinary rendering does not require a constitutional receipt unless the calling component's policy or evidence contract requires one.

### 8.12 Release system

Language packs belong to the knowledge release channel and may be included in a compatible Release Set with system, service, and governance versions.

An independent language-pack update is permitted only when compatibility constraints remain satisfied.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Accepted decisions

| Decision | Effect |
| --- | --- |
| `DEC-COMP-001` | Keeps GF Wordbench and SemantiK Architect Runtime as explicit component responsibilities. |
| `DEC-PROFILE-BASELINE-001` | Separates user-runtime behavior from selectable developer workbenches and profile-specific resource limits. |
| `DEC-AI-001` | Excludes native generative AI and silent AI fallback from the language runtime. |
| `DEC-REL-001` | Places language artifacts in the knowledge release channel and subjects them to Release Set compatibility. |
| `DEC-HW-001` | Establishes bounded profile resource envelopes, including lightweight runtime operation. |

### 9.2 Related ADRs

| ADR | Relevance |
| --- | --- |
| `ADR-006` | Establishes explicit first-class component boundaries. |
| `ADR-013` | Separates the global system baseline from profile-specific implementation choices. |
| `ADR-014` | Establishes the strict external AI boundary. |
| `ADR-017` | Defines the lightweight user hardware profile. |
| `ADR-024` | Preserves logical ownership under profile-dependent physical consolidation. |

### 9.3 Prohibited assumptions

The following assumptions are prohibited:

- the runtime may compile grammar source because GF is installed somewhere on the host;
- a language pack is active because its files are present;
- an installed pack is compatible because its language tag matches;
- multiple installed languages must all remain loaded;
- the lightweight profile globally limits every deployment to one language;
- a render may infer missing application facts;
- rendered text becomes the canonical application record;
- a cache entry may survive an incompatible pack update;
- a missing translation may be produced by an external AI provider automatically;
- an external voice service is part of the language runtime;
- Wordbench must run in normal user operation;
- one active language per Wordbench session prohibits separate isolated sessions;
- a package digest replaces schema, provenance, compatibility, or evidence validation;
- an artifact published on the knowledge channel is compatible with every runtime;
- a profile implementation recipe may redefine the language-pack contract;
- a successful process restart proves successful language capability recovery.

## 10. Validation Criteria

This document conforms when all of the following checks pass:

1. metadata status is `active`;
2. the registered path is `02-system/13-language-system-boundary.md`;
3. all identifiers and canonical references resolve;
4. every listed decision is accepted;
5. every requirement exists with identical text and strength;
6. every lock exists and its assertions pass;
7. GF Wordbench and SemantiK Architect Runtime have separate active component entries and contracts;
8. the runtime artifact excludes build tools and unpublished grammar-development state;
9. language-pack artifacts match their schema and artifact contract;
10. pack identity, language, version, PGF, compatibility, provenance, integrity, capabilities, and evidence are present;
11. candidate, installed, active, predecessor, rejected, and retired states are distinguishable;
12. installation and activation are separate;
13. activation is atomic;
14. rollback or forward repair is defined;
15. no partially activated pack serves requests;
16. rendering requests use explicit structured inputs and language selection;
17. deterministic regression fixtures pass for every supported entry point;
18. cache keys include pack and input identity;
19. incompatible cache entries are invalidated;
20. offline rendering passes without network access;
21. native runtime dependency analysis finds no generative AI, classifier, embedding model, autonomous routing model, or agent dependency;
22. user-lightweight tests enforce the declared worker, loaded-language, memory, and cache envelope;
23. profile-specific limits do not alter global semantics;
24. GF Wordbench tests enforce one active language project per session;
25. separate isolated Wordbench workspaces may operate without mutable-state collision when the development profile permits them;
26. application data ownership remains with the calling component;
27. runtime output exposes pack, language, contract, entry-point, and status identity;
28. release-channel and Release Set compatibility checks pass;
29. activation, rollback, rejection, and recovery evidence is present;
30. backup and restore exclude reproducible cache authority;
31. active content is English;
32. no prohibited open-authority marker or template token appears.

The validator reports actionable failures, including:

```text
language_runtime_build_tools_present
language_runtime_unverified_pack
language_runtime_incompatible_pack
language_runtime_partial_activation
language_runtime_missing_rollback_or_repair
language_runtime_implicit_language_selection
language_runtime_undeclared_parameter
language_runtime_nondeterministic_fixture
language_runtime_cache_identity_incomplete
language_runtime_network_dependency
language_runtime_ai_dependency
language_runtime_profile_scope_violation
language_runtime_application_owner_violation
language_runtime_missing_provenance
language_runtime_missing_activation_evidence
gf_wordbench_multiple_active_languages_in_session
```

## 11. Non-Normative Examples

### 11.1 Lightweight user profile

The system has French Canadian and English Canadian packs installed. The active profile loads French Canadian and one runtime worker. Switching to English Canadian unloads the French pack after in-flight requests complete. Both packs remain installed.

### 11.2 Deterministic task rendering

Orgo submits a task identifier, due date, participant display name, and message entry point. The runtime renders the sentence using the active pack and returns the pack version and entry-point identity. Orgo retains ownership of the task.

### 11.3 Reusable confirmation message

A validated parameterized confirmation is reused from cache. The cache key includes the language-pack version, message identifier, and normalized parameter values. Updating the pack invalidates the old cache entry.

### 11.4 Wordbench publication

A developer opens one isolated French language project in GF Wordbench, compiles a PGF, runs regression fixtures, assembles a manifest, and publishes the accepted pack to the knowledge channel. The user runtime receives only the published runtime artifact.

### 11.5 Parallel language development

Two developers use separate workspaces: one for French and one for Inuktitut. Each Wordbench session has one active language project, separate dependencies, temporary data, and resource limits. The sessions do not share mutable build state.

### 11.6 Failed pack activation

A candidate pack passes integrity checks but lacks a required application entry point. Activation is rejected. The current active pack continues serving requests, and the candidate remains inactive with a compatibility failure record.

### 11.7 Offline operation

The network is unavailable. SemantiK Architect Runtime continues rendering from installed packs. New pack synchronization and external voice processing are unavailable, but local deterministic text remains operational.

### 11.8 Resource pressure

The Resource Governor reduces rendering concurrency to one worker and unloads an inactive language pack. It does not alter the active grammar, infer another language, or invoke an AI service.
