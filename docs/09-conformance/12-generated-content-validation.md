<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONF-012",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "conformance",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/document-index.json",
    "generated/decision-index.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "contracts/ai-navigation.contract.json",
    "contracts/artifact-classes.contract.json",
    "schemas/test-evidence.schema.json",
    "contracts/system.contract.json#/degradation_baseline/contract_incompatibility"
  ],
  "decision_ids": [
    "DEC-SYS-001",
    "DEC-PROFILE-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-REL-001",
    "DEC-AI-001"
  ],
  "requirement_ids": [
    "REQ-CONF-GEN-001",
    "REQ-CONF-GEN-002",
    "REQ-CONF-GEN-003",
    "REQ-CONF-GEN-004",
    "REQ-CONF-GEN-005",
    "REQ-CONF-GEN-006",
    "REQ-CONF-GEN-007",
    "REQ-CONF-GEN-008",
    "REQ-CONF-GEN-009",
    "REQ-CONF-GEN-010",
    "REQ-CONF-GEN-011",
    "REQ-CONF-GEN-012",
    "REQ-CONF-GEN-013",
    "REQ-CONF-GEN-014",
    "REQ-CONF-GEN-015",
    "REQ-CONF-GEN-016",
    "REQ-CONF-GEN-017",
    "REQ-CONF-GEN-018",
    "REQ-CONF-GEN-019",
    "REQ-CONF-GEN-020",
    "REQ-CONF-GEN-021",
    "REQ-CONF-GEN-022",
    "REQ-CONF-GEN-023",
    "REQ-CONF-GEN-024"
  ],
  "lock_ids": [
    "LOCK-SYS-001",
    "LOCK-SYS-002",
    "LOCK-SYS-003",
    "LOCK-SYS-004",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-CONST-003",
    "DOC-DEV-014",
    "DOC-LIFE-017",
    "DOC-CONF-000",
    "DOC-CONF-001",
    "DOC-CONF-002",
    "DOC-CONF-003",
    "DOC-CONF-004",
    "DOC-CONF-005",
    "DOC-CONF-006",
    "DOC-CONF-007",
    "DOC-CONF-008",
    "DOC-CONF-009",
    "DOC-CONF-010",
    "DOC-CONF-011"
  ],
  "tags": [
    "conformance",
    "generated-content",
    "projections",
    "renderers",
    "canonical-source",
    "drift-detection",
    "reproducibility",
    "documentation",
    "registries",
    "validation"
  ]
}
KOA:DOC-META:END -->

# Generated Content Validation

## 1. Purpose

This document defines how kOA discovers, renders, compares, validates, reviews, and evidences generated content.

Generated content is a projection of canonical authority. It improves consistency and reduces repeated manual transcription. It does not become an independent semantic owner.

A valid projection is reproducible from an exact canonical source through a registered deterministic renderer. When a projection is wrong, the correction occurs in the canonical source or renderer and the projection is regenerated.

This document applies the same standard to generated Markdown regions and machine-readable generated artifacts.

## 2. Scope

This document applies to:

- generated document metadata;
- generated normative requirement blocks;
- canonical tables, lists, matrices, indexes, and navigation;
- generated schemas, manifests, configuration, and registries;
- generated examples;
- generated traceability and compatibility projections;
- generated test and evidence summaries;
- generated release, artifact, profile, and component views;
- generated AI context packages;
- marker parsing, source resolution, rendering, comparison, semantic validation, impact analysis, and evidence;
- active and explicitly historical generated content.

It does not treat ordinary authored prose as generated merely because a tool assisted its drafting.

It does not authorize AI-produced text, examples, or corrections to bypass canonical ownership, deterministic rendering, review, or validation.

## 3. Canonical References

| Canonical reference | Ownership |
| --- | --- |
| `generated/document-index.json` | Document identity, lifecycle, dependencies, generated regions, and projection ownership |
| `generated/decision-index.json` | Accepted semantic decisions and supersession |
| `generated/requirements-index.json` | Requirement identities, strength, wording, scope, lifecycle, and ownership |
| `generated/assertion-index.json` | Cross-file invariants that generated content cannot weaken |
| `generated/traceability.json` | Source-to-projection and transitive-impact relationships |
| `generated/test-catalog.json` | Registered generated-content validation tests |
| `generated/evidence-catalog.json` | Active validation evidence, validity, invalidation, and supersession |
| `contracts/renderers.registry.json` | Renderer identities, versions, input and output contracts, ordering, normalization, and failure behavior |
| `contracts/schemas.registry.json` | Registered machine-readable schemas and compatibility |
| `contracts/artifact-classes.contract.json` | Generated artifact identity, integrity, lifecycle, and evidence |
| `schemas/test-evidence.schema.json` | Structure of generated-content test evidence |
| `contracts/system.contract.json#/degradation_baseline/contract_incompatibility` | Blocked transition, preserved valid state, and no automatic schema guessing |

## 4. Model and Responsibilities

### 4.1 Projection relationship

A generated projection has four parties:

- the canonical owner, which owns semantics;
- the source object, which supplies exact machine-readable values;
- the registered renderer, which transforms those values deterministically;
- the destination, which contains the generated payload.

The destination can explain or display authority. It cannot override its source.

### 4.2 Generated content classes

| Content class | Canonical owner | Projection | Validation focus |
| --- | --- | --- | --- |
| Document metadata | Documentation registry and referenced canonical registries | Machine-readable metadata block | Identity, lifecycle, scope, and traceability agreement |
| Requirement projection | Requirements registry | Normative requirement list | Exact IDs, strength, wording, order, and uniqueness |
| Canonical table | Component, profile, release, artifact, or other registry path | Markdown table | Rows, columns, labels, references, ordering, and cardinality |
| Canonical list or matrix | One registered source path | Markdown list or matrix | Membership, grouping, ordering, and empty-state behavior |
| Index or navigation | Documentation, profile, component, artifact, or test registry | Index entries and links | Target resolution, status filtering, labels, and stable order |
| Schema | Accepted contract and schema definitions | JSON Schema or equivalent machine-readable schema | Meta-schema validity, semantic invariants, and sample validation |
| Example artifact | Active schemas and selected canonical contracts | Machine-readable illustrative instance | Schema validity, explicit example status, and non-authority |
| Configuration or manifest | Profile, component, toolchain, release, or artifact contract | Machine-readable deployment input | Schema, references, profile scope, security, and compatibility |
| AI context package | Selected active canonical corpus and projection contract | Bounded non-authoritative context | Source lineage, freshness, scope, omissions, and no authority transfer |

### 4.3 Region markers

General generated regions use a recognized start marker, metadata lines, payload, and matching end marker.

The canonical form is represented here with escaped delimiters so it is not interpreted as a live region:

```text
&lt;!-- GENERATED:BEGIN
source=contracts/components/example.component.json#/interfaces/commands
renderer=canonical-table-v1
--&gt;
generated payload
&lt;!-- GENERATED:END --&gt;
```

The specialized requirement form declares the complete identifier set in its start marker and ends with its specialized requirement end marker.

| Marker or field | Purpose | Validation rule |
| --- | --- | --- |
| `GENERATED:BEGIN` | Begins a general generated region. | Exactly one matching general end marker; no nesting. |
| `source=` | Provides the exact canonical reference or JSON Pointer. | Resolvable registered target with compatible source class. |
| `renderer=` | Provides the registered renderer identity and behavior version. | Renderer exists and supports the source and output classes. |
| `GENERATED:END` | Ends a general generated region. | Matches the nearest unmatched general begin marker. |
| `GENERATED:REQUIREMENTS:BEGIN` | Begins the specialized requirement projection and declares its ID set. | Exactly one matching specialized end marker and an exact registry match. |
| `GENERATED:REQUIREMENTS:END` | Ends the specialized requirement projection. | Matches one specialized begin marker. |

Generated regions cannot overlap or nest. A document can contain several independent regions.

### 4.4 Source identity

The source reference is repository-relative and can include a JSON Pointer.

Source resolution verifies:

- target existence;
- registry membership where required;
- lifecycle state;
- source class;
- language and scope;
- pointer existence;
- unique identity;
- compatibility with the renderer;
- absence of circular semantic ownership.

A projection can reference an explicitly historical source only when the destination and registry mark the projection historical.

### 4.5 Renderer contract

| Aspect | Registered behavior | Conformance effect |
| --- | --- | --- |
| Identity | Stable renderer ID and version | Missing or unknown renderer blocks validation. |
| Input contract | Accepted source classes, required fields, and reference forms | Incompatible input blocks rendering. |
| Output contract | Output class, columns or fields, marker form, and empty-state representation | Unexpected shape blocks comparison. |
| Ordering | Canonical order or explicit stable sort keys | Filesystem, map, or query-result order is never implicit. |
| Normalization | Unicode, whitespace, line endings, booleans, numbers, dates, and null handling | Host or locale differences cannot change output. |
| Escaping | Markdown, JSON, YAML, HTML, code, table, and link escaping | Unsafe or structurally ambiguous output fails. |
| Failure | Missing field, invalid type, broken reference, duplicate ID, unsupported state | Rendering stops; no guessed or partial output is committed. |
| Diagnostics | Source location, renderer, object identity, and actionable reason | Diagnostics exclude secrets and non-required protected content. |

Renderer version changes are semantic changes when they can alter output.

### 4.6 Determinism and normalization

A clean rendering environment supplies:

- the selected corpus revision;
- registered renderer implementation;
- declared renderer configuration;
- fixed locale;
- fixed timezone when dates are source values;
- fixed Unicode normalization;
- fixed line endings;
- fixed serialization rules;
- no unregistered network access;
- no user-specific state.

The renderer does not insert generation time unless the canonical source owns that exact value.

Ordering comes from the source contract or stable canonical identifiers. Object-map iteration, filesystem discovery order, database return order, and parallel-worker completion order are not valid implicit ordering rules.

### 4.7 Validation pipeline

| Stage | Operation | Required result |
| --- | --- | --- |
| Discovery | Find active metadata and generated-region markers while ignoring examples inside fenced code. | Every region has a unique document location. |
| Boundary parsing | Validate recognized marker type, balance, order, and non-nesting. | A malformed region fails before rendering. |
| Source resolution | Resolve source reference, JSON Pointer, status, class, language, and scope. | Missing or incompatible source fails. |
| Renderer resolution | Resolve renderer registration and version. | Unknown or incompatible renderer fails. |
| Independent rendering | Render in a clean deterministic validation environment. | No committed payload is used as renderer input. |
| Payload comparison | Compare normalized bytes according to the registered output contract. | Any semantic or formatting drift fails. |
| Semantic validation | Validate IDs, references, cardinality, schemas, lifecycle, ownership, and scope. | Byte equality cannot hide a semantically invalid source. |
| Impact and evidence | Record affected objects, tests, report, validity, and traceability. | Only valid evidence supports an active synchronization claim. |

Byte comparison uses the renderer's declared normalization. Semantic validation remains required even when bytes match.

### 4.8 Requirement and metadata projections

The requirement projection validates:

- declared ID set;
- source registry membership;
- exact canonical strength;
- exact canonical statement;
- canonical order;
- one emission per ID;
- no additional normative statement;
- no omitted active requirement in the declared set.

Document metadata validates:

- document ID and class;
- active lifecycle state;
- language;
- layer and scope;
- canonical references;
- decisions;
- requirements;
- locks;
- exceptions;
- dependencies;
- tags.

Metadata is generated from registered authority or validated against it. A document cannot self-authorize missing registry entries.

### 4.9 Machine-readable generated artifacts

Generated JSON, JSON Schema, YAML, manifests, configuration, examples, and registries receive both structural and semantic validation.

An example artifact:

- declares that it is an example;
- uses non-production identities or clearly illustrative references;
- validates under the intended schema;
- demonstrates required invariants;
- does not claim active deployment, valid signature, release approval, activation, or conformance.

Values that resemble integrity material in an example are explicitly described as illustrative unless they are calculated from real attached artifact bytes under an evidence-producing procedure.

### 4.10 Review and authority boundaries

Reviewers inspect:

- canonical change;
- renderer change;
- regenerated differences;
- affected authority and scope;
- compatibility and lifecycle impact;
- tests and evidence.

Review of a generated diff does not transfer ownership from the canonical source.

ChatGPT can help explain a drift report or propose a source or renderer correction. The accepted source change and deterministic validation remain the authority.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-CONF-GEN-001,REQ-CONF-GEN-002,REQ-CONF-GEN-003,REQ-CONF-GEN-004,REQ-CONF-GEN-005,REQ-CONF-GEN-006,REQ-CONF-GEN-007,REQ-CONF-GEN-008,REQ-CONF-GEN-009,REQ-CONF-GEN-010,REQ-CONF-GEN-011,REQ-CONF-GEN-012,REQ-CONF-GEN-013,REQ-CONF-GEN-014,REQ-CONF-GEN-015,REQ-CONF-GEN-016,REQ-CONF-GEN-017,REQ-CONF-GEN-018,REQ-CONF-GEN-019,REQ-CONF-GEN-020,REQ-CONF-GEN-021,REQ-CONF-GEN-022,REQ-CONF-GEN-023,REQ-CONF-GEN-024 -->
- **REQ-CONF-GEN-001 — SHALL:** Every generated content region shall identify one resolvable canonical source reference and one registered renderer identity.
- **REQ-CONF-GEN-002 — SHALL:** A generated projection shall derive only from canonical source data, declared renderer configuration, and registered deterministic dependencies.
- **REQ-CONF-GEN-003 — SHALL NOT:** Generated content shall not introduce a decision, requirement, lock, profile membership, component authority, compatibility relationship, test result, evidence state, or release state absent from its canonical source.
- **REQ-CONF-GEN-004 — SHALL:** Generated regions shall use recognized, balanced, non-nested boundary markers and shall contain complete renderer metadata before the generated payload.
- **REQ-CONF-GEN-005 — SHALL:** A source reference shall identify the exact registered document, registry, schema, contract, or JSON Pointer from which the projection is rendered.
- **REQ-CONF-GEN-006 — SHALL:** A renderer shall have a stable registered identity, versioned behavior, declared input classes, declared output class, deterministic ordering rules, escaping rules, and failure behavior.
- **REQ-CONF-GEN-007 — SHALL:** Repeated rendering from identical canonical inputs, renderer version, configuration, locale, and line-ending policy shall produce byte-equivalent generated payloads.
- **REQ-CONF-GEN-008 — SHALL NOT:** Time, host identity, filesystem iteration order, locale defaults, random values, network responses, mutable caches, user-specific paths, or unregistered environment state shall affect deterministic projections.
- **REQ-CONF-GEN-009 — SHALL:** Collections shall use a declared stable ordering based on canonical identifiers or an explicit order owned by the source contract.
- **REQ-CONF-GEN-010 — SHALL:** Generated text shall apply registered escaping, normalization, newline, Unicode, table, code, link, and empty-value rules appropriate to its output format.
- **REQ-CONF-GEN-011 — SHALL:** Repository validation shall regenerate each active generated region independently and shall compare the regenerated payload with the committed payload.
- **REQ-CONF-GEN-012 — SHALL:** Any difference between committed and regenerated content shall fail the affected structural, merge, release, or conformance gate until the canonical source or renderer output is reconciled.
- **REQ-CONF-GEN-013 — SHALL NOT:** A manual edit inside a generated region shall be accepted as a correction unless the canonical source or registered renderer is updated and the region is regenerated.
- **REQ-CONF-GEN-014 — SHALL:** Generated requirement projections shall contain exactly the declared requirement identifiers, preserve canonical strength and wording, and emit each identifier exactly once.
- **REQ-CONF-GEN-015 — SHALL:** Generated metadata shall parse under its declared format and shall agree with the document registry on identity, class, status, language, layer, scope, references, decisions, requirements, locks, exceptions, dependencies, and tags.
- **REQ-CONF-GEN-016 — SHALL:** Generated tables, lists, indexes, matrices, and navigation projections shall preserve canonical identifiers, references, labels, membership, ordering, and cardinality.
- **REQ-CONF-GEN-017 — SHALL:** Generated schemas, examples, manifests, configuration, and machine-readable artifacts shall validate against their registered schema and applicable semantic checks.
- **REQ-CONF-GEN-018 — SHALL:** A generated example shall be explicitly marked as an example and shall not claim active deployment, release, conformance, evidence, signature, or authority unless a separate valid artifact establishes that claim.
- **REQ-CONF-GEN-019 — SHALL:** Generated references shall resolve to active or explicitly historical registered targets, and broken, ambiguous, circularly authoritative, or scope-incompatible references shall fail validation.
- **REQ-CONF-GEN-020 — SHALL:** A semantic source or renderer change shall trigger direct and transitive impact analysis across dependent projections, documents, schemas, examples, tests, evidence, AI context packages, and release artifacts.
- **REQ-CONF-GEN-021 — SHALL:** Deprecated, superseded, archived, or removed canonical objects shall update or invalidate every dependent generated projection according to registered lifecycle and retention rules.
- **REQ-CONF-GEN-022 — SHALL:** Generated-content validation evidence shall identify the corpus revision, source identities, renderer identities and versions, executed checks, comparison results, failures, produced reports, validity, and traceability.
- **REQ-CONF-GEN-023 — SHALL NOT:** Native or external AI output shall become an authoritative generated projection, canonical correction, validation result, or drift-resolution decision without deterministic registered rendering and validation.
- **REQ-CONF-GEN-024 — SHALL:** Every active generated-content, projection, renderer, synchronization, structural-validity, and conformance claim shall be traceable to accepted decisions, active requirements, applicable locks, registered tests, and valid evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Add a generated region

1. Identify the exclusive canonical owner.
2. select the exact source reference;
3. select or register a compatible deterministic renderer;
4. declare output shape, ordering, normalization, escaping, and empty-state behavior;
5. insert balanced non-nested markers;
6. render in a clean environment;
7. validate the payload structurally and semantically;
8. compare a second independent rendering;
9. register source-to-destination traceability;
10. commit source, renderer change when applicable, projection, tests, and evidence together.

### 6.2 Validate the active corpus

1. Select one immutable corpus revision.
2. parse document metadata and discover generated regions;
3. ignore escaped examples and fenced-code demonstrations;
4. validate marker balance, type, order, and non-nesting;
5. resolve every source and renderer;
6. render every region independently;
7. compare generated and committed payloads;
8. validate schemas, identifiers, references, lifecycle, scope, ownership, and cardinality;
9. compute direct and transitive impact;
10. emit a bounded validation report and test evidence;
11. fail the affected gate when any required check fails.

### 6.3 Correct a generated projection

1. Reproduce the mismatch.
2. determine whether the canonical source, renderer, renderer configuration, or destination registration is wrong;
3. update the owning canonical object;
4. update renderer tests when behavior changes;
5. regenerate all affected destinations;
6. inspect the complete diff;
7. run corpus validation;
8. update traceability, compatibility, and evidence;
9. preserve prior revisions through version control and lifecycle records.

A direct payload edit is discarded unless the same correction is represented in the source or renderer.

### 6.4 Change a renderer

1. Record the reason and accepted semantic authority for the change.
2. assign a new renderer behavior version;
3. define compatibility with prior input and output contracts;
4. update ordering, normalization, escaping, and failure tests;
5. identify every dependent projection;
6. regenerate the complete affected corpus;
7. review semantic and formatting changes;
8. update deprecation or supersession for the previous renderer version;
9. produce validation evidence.

### 6.5 Validate a generated requirement block

1. Parse the declared requirement IDs.
2. reject duplicate or malformed IDs;
3. resolve every ID in the requirements registry;
4. verify active lifecycle and applicable scope;
5. render canonical strength and statement;
6. verify exact ordering and one occurrence per ID;
7. verify no undeclared requirement appears;
8. compare the payload;
9. record the result.

### 6.6 Validate a generated schema or example

1. Resolve the generating contract, renderer, and target schema.
2. render in a clean environment;
3. validate the schema under its declared meta-schema when applicable;
4. validate positive and negative sample instances;
5. validate semantic invariants not expressible in the schema;
6. verify example and non-authority markers;
7. validate references and traceability;
8. compare committed and regenerated bytes;
9. record evidence.

### 6.7 Handle source lifecycle change

1. Detect deprecation, supersession, archival, revocation, or removal.
2. resolve all direct and transitive generated destinations;
3. classify each destination as update, replacement, historical retention, or removal;
4. update source references and lifecycle labels;
5. regenerate affected content;
6. invalidate stale evidence and AI context packages;
7. retain required historical lineage;
8. block active publication while unresolved stale projections remain.

### 6.8 Produce validation evidence

1. Select the corpus revision and validation subject.
2. record source and renderer identities and versions;
3. record the clean environment;
4. record marker, reference, render, comparison, schema, and semantic checks;
5. attach or reference bounded reports;
6. record result and failures;
7. define validity and invalidation conditions;
8. validate against `schemas/test-evidence.schema.json`;
9. register evidence and traceability.

## 7. Failure States and Safe Degradation

| Failure state | Required response | Preserved state | Blocked behavior or claim |
| --- | --- | --- | --- |
| Missing start or end marker | Fail the document and stop region interpretation. | Canonical source and other valid documents | Partial generated payload |
| Nested generated regions | Fail the containing document. | Source objects | Ambiguous ownership |
| Unknown source | Fail source resolution. | Committed source corpus | Guessing or nearest-name matching |
| Unknown renderer | Fail renderer resolution. | Current committed payload as historical text only | Unregistered rendering |
| Source class incompatible with renderer | Fail before generation. | Canonical source | Partial or coerced projection |
| Duplicate canonical identifiers | Fail the source registry and all affected projections. | Last valid corpus revision | Arbitrary duplicate selection |
| Committed payload differs from regeneration | Fail the affected gate and report the exact region difference. | Canonical source and regenerated candidate | Silent acceptance of drift |
| Manual edit inside generated region | Replace it through source or renderer correction and regeneration. | Review history | Manual patch as authoritative fix |
| Broken generated reference | Fail the affected projection and dependent active claim. | Resolvable unaffected references | Dead-link publication |
| Deprecated or superseded source | Apply lifecycle mapping, regenerate, or retain an explicitly historical projection. | Required lineage and retention | Unmarked stale active content |
| Schema-valid example claims authority | Fail semantic validation. | Example structure | Deployment, release, or conformance claim |
| Renderer output varies across clean runs | Classify the renderer as nondeterministic and block its projections. | Canonical inputs | Selecting one run arbitrarily |
| Validation environment lacks a dependency | Mark validation blocked and do not update committed output. | Existing valid projection | Approximate rendering |
| AI proposes a corrected projection | Treat it as candidate review material only. | Canonical source and registered renderer | Direct authoritative replacement |

Generated-content failure preserves canonical source authority and the last validated corpus. It cannot authorize approximate, guessed, partially generated, or manually patched active content.

## 8. Cross-Component Interactions

| Producer or owner | Consumer | Interaction | Authority boundary |
| --- | --- | --- | --- |
| Canonical registry or contract | Renderer | Supplies exact semantic source values | Renderer cannot invent missing authority |
| Renderer registry | Validation runner | Supplies versioned rendering behavior | Validation runner cannot select an unregistered equivalent silently |
| Documentation registry | Corpus validator | Supplies document identity, lifecycle, dependencies, and generated-region declarations | Document prose cannot self-register |
| Requirements registry | Requirement renderer | Supplies exact requirement IDs, strength, wording, and scope | Projected requirement text cannot amend the registry |
| Component and profile contracts | Table and matrix renderers | Supply interfaces, membership, states, and references | Tables do not become component or profile owners |
| Schema registry | Schema and example validators | Supplies active schemas and compatibility | A schema pass does not establish semantic authority alone |
| Traceability registry | Impact analyzer | Supplies direct and transitive dependencies | Missing links block completeness claims |
| Test catalog | Validation runner | Supplies exact tests and assertions | Runner cannot redefine pass criteria |
| Evidence registry | Merge, release, and conformance gates | Supplies active validation evidence | Registration does not repair drift |
| Version control | Reviewer and validator | Preserves source, renderer, and generated diffs | Commit history is evidence context, not semantic authority |
| Build farm | Release workflow | Produces clean generated artifacts and reports when release-authoritative generation is required | Local generation alone does not create release authority |
| External AI surface | User or reviewer | Provides candidate explanation or correction | AI output has no projection or validation authority |

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Closed question |
| --- | --- |
| `DEC-SYS-001` | Generated content remains a lower-scope projection inside the explicit-authority architecture. |
| `DEC-PROFILE-001` | Profile-specific projections retain exact profile and overlay scope. |
| `DEC-DATA-001` | Generated views cannot transfer data ownership or authorize cross-component writes. |
| `DEC-GOV-001` | Generated policy or resource views do not merge Governance Policy Runtime and Resource Governor authority. |
| `DEC-REL-001` | Release-authoritative generated artifacts use registered identity, compatibility, evidence, and lifecycle. |
| `DEC-AI-001` | Native and external AI cannot become a canonical renderer or validation authority. |

### Prohibited assumptions

- Generated text is authoritative because it is committed.
- Markdown is the canonical owner of a generated table.
- A matching visual appearance proves synchronization.
- A source filename is sufficient without an exact registered reference.
- The latest renderer implementation can replace the declared version automatically.
- Filesystem order is stable enough.
- JSON object order is a semantic order unless the source contract declares it.
- A timestamp is harmless in deterministic output.
- A clean diff proves semantic validity.
- Byte equality proves source references and lifecycle are valid.
- Schema validity proves an example is non-authoritative.
- Manual edits inside a generated region can be preserved during the next run.
- A broken reference can be replaced with the nearest matching name.
- A deprecated source remains valid because the projection has not changed.
- Requirement wording can be shortened for table width.
- An omitted row means not applicable.
- An empty result can be omitted without an explicit empty-state rule.
- Local generation proves build-farm or release reproducibility.
- An AI-generated correction can replace source or renderer review.
- Missing evidence can be replaced by reviewer confidence.

## 10. Validation Criteria

1. The metadata block parses as JSON and declares `DOC-CONF-012`, status `active`, language `en`, conformance layer, and global scope.
2. All eleven required sections exist in numerical order.
3. Every decision ID is accepted in `generated/decision-index.json`.
4. Every requirement ID appears exactly once in `generated/requirements-index.json`.
5. Every lock ID resolves to an active lock.
6. `TEST-CONF-GEN-001` verifies discovery of active generated regions and exclusion of escaped or fenced examples.
7. `TEST-CONF-GEN-002` verifies recognized balanced non-nested markers.
8. `TEST-CONF-GEN-003` verifies exact source and JSON Pointer resolution.
9. `TEST-CONF-GEN-004` verifies registered renderer identity, version, input class, output class, and configuration.
10. `TEST-CONF-GEN-005` verifies deterministic repeated rendering in independent clean environments.
11. `TEST-CONF-GEN-006` verifies stable ordering independent of filesystem, map, query, and parallel-execution order.
12. `TEST-CONF-GEN-007` verifies Unicode, whitespace, line-ending, escaping, table, code, link, and empty-state normalization.
13. `TEST-CONF-GEN-008` verifies exact committed-to-regenerated payload comparison.
14. `TEST-CONF-GEN-009` rejects manual edits inside generated regions.
15. `TEST-CONF-GEN-010` verifies requirement ID, strength, wording, order, cardinality, and uniqueness.
16. `TEST-CONF-GEN-011` verifies document metadata agreement with the documentation registry.
17. `TEST-CONF-GEN-012` verifies table, list, matrix, index, and navigation identity, membership, labels, references, ordering, and cardinality.
18. `TEST-CONF-GEN-013` verifies generated schemas against their meta-schemas and positive and negative instances.
19. `TEST-CONF-GEN-014` verifies generated examples, explicit example state, and absence of authority claims.
20. `TEST-CONF-GEN-015` verifies reference lifecycle, scope, ambiguity, circular ownership, and historical-state handling.
21. `TEST-CONF-GEN-016` verifies direct and transitive impact after source or renderer changes.
22. `TEST-CONF-GEN-017` verifies deprecation, supersession, archival, removal, and stale-projection invalidation.
23. `TEST-CONF-GEN-018` verifies validation evidence under `schemas/test-evidence.schema.json`.
24. `TEST-CONF-GEN-019` verifies that release-authoritative generation runs in the required clean build environment.
25. `TEST-CONF-GEN-020` verifies absence of native or external AI projection and validation authority.
26. `TEST-CONF-GEN-021` verifies traceability to decisions, requirements, locks, sources, renderers, destinations, tests, and evidence.
27. Active prose is English and contains no unresolved marker or placeholder.
28. The generated requirement block matches the canonical requirements registry.

These criteria define validation requirements. They do not claim that the current complete documentation corpus, every renderer, or every generated artifact already conforms.

## 11. Non-Normative Examples

> **Non-normative example:** A component contract adds one command. Regeneration adds one row to the component document's command table. A manual row added only in Markdown fails because it is absent from the contract.

> **Non-normative example:** A renderer once sorted rows using filesystem discovery order. Two clean workers emit different tables. The renderer is blocked until it sorts by the canonical identifier.

> **Non-normative example:** A requirement statement changes in the requirements registry. Every document that projects that requirement is identified through traceability, regenerated, compared, and revalidated.

> **Non-normative example:** A JSON example validates against its schema but sets `release_authority` to true. Semantic validation fails because an illustrative example cannot create release authority.

> **Non-normative example:** A profile is superseded. Its active navigation entry is removed, dependent documents point to the replacement, and an explicitly historical migration document retains the old reference.

> **Non-normative example:** ChatGPT suggests improved wording for a generated table cell. The suggestion is reviewed against the canonical source. Any accepted correction is made in the source or renderer, then regenerated deterministically.
