<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONF-007",
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
    "generated/document-index.json",
    "contracts/terminology.contract.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "contracts/ai-navigation.contract.json",
    "generated/profile-catalog.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "contracts/integration-types.contract.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "schemas/impact-report.schema.json"
  ],
  "decision_ids": [
    "DEC-DOC-001",
    "DEC-DOC-002",
    "DEC-DOC-003",
    "DEC-DOC-004"
  ],
  "requirement_ids": [
    "REQ-CONF-DRIFT-001",
    "REQ-CONF-DRIFT-002",
    "REQ-CONF-DRIFT-003",
    "REQ-CONF-DRIFT-004",
    "REQ-CONF-DRIFT-005",
    "REQ-CONF-DRIFT-006",
    "REQ-CONF-DRIFT-007",
    "REQ-CONF-DRIFT-008",
    "REQ-CONF-DRIFT-009",
    "REQ-CONF-DRIFT-010",
    "REQ-CONF-DRIFT-011",
    "REQ-CONF-DRIFT-012",
    "REQ-CONF-DRIFT-013",
    "REQ-CONF-DRIFT-014",
    "REQ-CONF-DRIFT-015",
    "REQ-CONF-DRIFT-016",
    "REQ-CONF-DRIFT-017",
    "REQ-CONF-DRIFT-018",
    "REQ-CONF-DRIFT-019",
    "REQ-CONF-DRIFT-020",
    "REQ-CONF-DRIFT-021",
    "REQ-CONF-DRIFT-022",
    "REQ-CONF-DRIFT-023",
    "REQ-CONF-DRIFT-024",
    "REQ-CONF-DRIFT-025",
    "REQ-CONF-DRIFT-026",
    "REQ-CONF-DRIFT-027",
    "REQ-CONF-DRIFT-028",
    "REQ-CONF-DRIFT-029",
    "REQ-CONF-DRIFT-030"
  ],
  "lock_ids": [
    "LOCK-DOC-002",
    "LOCK-DOC-003",
    "LOCK-DOC-005",
    "LOCK-DOC-006",
    "LOCK-DOC-007",
    "LOCK-DOC-008",
    "LOCK-DOC-009",
    "LOCK-DOC-010",
    "LOCK-DOC-011",
    "LOCK-DOC-015",
    "LOCK-DOC-016",
    "LOCK-DOC-017",
    "LOCK-DOC-019",
    "LOCK-DOC-020",
    "LOCK-DOC-021",
    "LOCK-DOC-022"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-003",
    "DOC-GOV-004",
    "DOC-GOV-005",
    "DOC-GOV-006",
    "DOC-GOV-007",
    "DOC-GOV-009",
    "DOC-GOV-010",
    "DOC-CONST-002",
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-PROFILE-001",
    "DOC-COMP-000",
    "DOC-CONF-000",
    "DOC-CONF-001",
    "DOC-CONF-002",
    "DOC-CONF-006"
  ],
  "tags": [
    "conformance",
    "documentation",
    "drift-detection",
    "canonical-ownership",
    "generated-content",
    "impact-analysis",
    "semantic-alignment",
    "validation",
    "ai-context",
    "clean-repository"
  ]
}
KOA:DOC-META:END -->

# Document Drift Detection

## 1. Purpose

This document defines how semantic and structural drift is detected across the active kOA documentation corpus.

Drift exists when a tracked document, registry, schema, contract, generated projection, example, recipe, migration record, or AI context no longer agrees with its canonical owners and declared dependencies.

The objective is not merely to detect changed text. It is to detect changed meaning, authority, scope, lifecycle, relationships, generated output, and implementation context before merge, release, profile conformance, or authority activation.

## 2. Scope

This document applies to:

- canonical registries;
- JSON Schemas;
- system and component contracts;
- deployment profiles and overlays;
- artifact and toolchain contracts;
- normative and explanatory Markdown;
- ADRs;
- requirements and locks;
- semantic document dependencies;
- tests and evidence;
- exceptions and waivers;
- examples and recipes;
- generated catalogs, indexes, matrices, reports, manifests, and AI contexts;
- migration evidence and deprecated disposition;
- authority activation;
- direct and transitive change-impact analysis;
- clean-repository validation before merge, release, and conformance claims.

This document does not:

- make textual difference equivalent to semantic drift in every case;
- require metadata or source hashes in active documentation;
- replace canonical ownership validation, traceability validation, generated-content validation, decision-closure validation, or migration validation;
- permit generated content to become independent authority;
- treat implementation behavior as proof of documentation correctness;
- authorize validators to repair semantic gaps automatically;
- make archived or migration-only sources active authority.

## 3. Canonical References

| Canonical reference | Ownership role |
| --- | --- |
| `generated/authority-manifest.json` | Owns active canonical versions and the final authority activation state. |
| `generated/document-index.json` | Owns tracked paths, document classes, status, language, layer, scope, canonical references, dependencies, tags, and generation policy. |
| `generated/decision-index.json` | Owns accepted decisions and decision lifecycle. |
| `generated/requirements-index.json` | Owns normative statements and their complete validation metadata. |
| `generated/assertion-index.json` | Owns interfile alignment assertions and their validation controls. |
| `generated/traceability.json` | Owns cross-object semantic relationships and reverse indexes. |
| `contracts/terminology.contract.json` | Owns canonical terms, identifiers, aliases, and prohibited synonyms. |
| `generated/decision-index.json` | Owns ADR identities, lifecycle, and decision relationships. |
| `generated/exception-index.json` | Owns authorized deviations and their bounded effects. |
| `contracts/ai-navigation.contract.json` | Owns AI-context package scope, source sets, read order, and generation policy. |
| System, component, profile, artifact, release, and integration registries | Own domain-specific values that documentation can only reference or project. |
| `generated/test-catalog.json` and `generated/evidence-catalog.json` | Own drift tests and evidence. |
| `schemas/impact-report.schema.json` | Owns semantic-change impact-report structure. |

The registries define what is true. Drift validation compares every secondary representation and dependent object with those owners.

## 4. Model and Responsibilities

### 4.1 Drift classes

| Drift class | Meaning |
| --- | --- |
| Structural drift | A file no longer validates against its schema or registered document class |
| Inventory drift | A tracked file is missing, unregistered, duplicated, moved, or has mismatched registry metadata |
| Ownership drift | More than one object claims the same canonical fact or a secondary object becomes an undeclared owner |
| Reference drift | A path, pointer, or identifier no longer resolves to the intended active object |
| Normative drift | Displayed requirements differ from the requirement registry or freehand normative language appears |
| Scope drift | A rule is applied outside its declared global, profile, overlay, component, artifact, toolchain, or migration scope |
| Dependency drift | Declared document dependencies are missing, stale, contradictory, or cyclic |
| Lifecycle drift | Active objects depend on non-authorizing or incompatible lifecycle states |
| Lock drift | An interfile invariant is violated or its affected objects no longer agree |
| Traceability drift | Decisions, requirements, tests, evidence, locks, documents, and claims disagree |
| Terminology drift | Canonical terms, identifiers, aliases, or prohibited synonyms are used inconsistently |
| Generated-content drift | A derived file or block differs from deterministic regeneration |
| Context drift | An AI context contains stale, inactive, unrelated, or missing authority |
| Parallel-authority drift | A second active documentation corpus or unregistered authoritative source appears |
| Migration drift | Historical or migration-only content is treated as active or its disposition is incomplete |

A single change can create several drift classes.

### 4.2 Detection layers

Drift detection operates in layers:

1. file and inventory validation;
2. schema validation;
3. canonical ownership validation;
4. reference and identifier resolution;
5. decision-closure validation;
6. scope and lifecycle validation;
7. requirement and normative-language validation;
8. interfile lock validation;
9. dependency-graph validation;
10. traceability validation;
11. deterministic regeneration;
12. AI-context validation;
13. migration and parallel-authority validation;
14. impact-disposition validation.

A later layer does not excuse a failure in an earlier layer.

### 4.3 Exact metadata alignment

For each tracked document, validation compares the document metadata with the documentation registry.

The comparison includes document identity, path, class, status, language, layer, scope, canonical references, accepted decisions, requirements, locks, exceptions, dependencies, tags, and generation policy.

Ordering is normalized only where the owning schema declares ordering insignificant.

### 4.4 Semantic comparison

Semantic validation compares owned values and relationships rather than relying only on text.

Examples include a profile capability list against the profile contract, a release-channel name against the release-channel registry, a component boundary against the component contract, a requirement block against the requirements registry, a dependency list against the documentation registry, a test-to-evidence relationship against the traceability registry, and an AI read order against the AI-context registry.

The validator reports the owner, expected semantic value, observed representation, and affected scope.

### 4.5 Deterministic regeneration

Derived content is verified by regeneration in a clean validation context.

The validator resolves generator identity, generator version, canonical inputs, renderer or template, ordering rules, locale and language, applicable scope, and output path.

The expected output is rebuilt and compared exactly with the tracked output. Manual correction of a derived output is rejected because it would not survive regeneration.

### 4.6 Change classification

| Change class | Meaning |
| --- | --- |
| Editorial | No semantic, scope, ownership, lifecycle, relationship, or generated-output effect |
| Patch | Compatible correction within existing authority |
| Minor | Compatible additive semantic change |
| Major | Ownership, boundary, scope, identifier, lifecycle, compatibility, or authority-changing change |

Classification determines the required decision, impact analysis, versioning, regeneration, tests, and evidence.

### 4.7 Impact graph

A semantic change is traced from its canonical owner through exact canonical references, JSON Pointers, tags, direct document dependencies, transitive dependencies, requirements, locks, decisions, ADRs, profiles, components, artifact contracts, tests, evidence, exceptions, generated projections, and AI contexts.

Every affected object receives a disposition before the change can be accepted.

### 4.8 Drift status

A drift finding can be informational, review required, blocking, accepted through an active scoped exception, resolved by canonical update, resolved by dependent update, resolved by regeneration, resolved by lifecycle transition, or confirmed as a false positive by the owning validator contract.

A blocking finding remains blocking until its canonical cause is resolved or an active exception explicitly covers it.

### 4.9 No automatic semantic repair

Validation tools can normalize schema-permitted ordering, regenerate derived output, report missing relationships, calculate impact, and propose a repair plan.

They cannot invent a decision, choose a canonical owner, infer a profile scope, create a requirement, assign a lock, fabricate evidence, approve an exception, or reinterpret a component boundary.

Semantic repair begins with the relevant canonical authority.

### 4.10 Validation outputs

A drift report identifies finding identity, drift class, severity, source object, affected object, canonical owner, expected state, observed state, direct impact, transitive impact, blocking claims, applicable exception, required disposition, validator and test identity, and evidence reference.

Reports are evidence of validation, not independent authority.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-CONF-DRIFT-001,REQ-CONF-DRIFT-002,REQ-CONF-DRIFT-003,REQ-CONF-DRIFT-004,REQ-CONF-DRIFT-005,REQ-CONF-DRIFT-006,REQ-CONF-DRIFT-007,REQ-CONF-DRIFT-008,REQ-CONF-DRIFT-009,REQ-CONF-DRIFT-010,REQ-CONF-DRIFT-011,REQ-CONF-DRIFT-012,REQ-CONF-DRIFT-013,REQ-CONF-DRIFT-014,REQ-CONF-DRIFT-015,REQ-CONF-DRIFT-016,REQ-CONF-DRIFT-017,REQ-CONF-DRIFT-018,REQ-CONF-DRIFT-019,REQ-CONF-DRIFT-020,REQ-CONF-DRIFT-021,REQ-CONF-DRIFT-022,REQ-CONF-DRIFT-023,REQ-CONF-DRIFT-024,REQ-CONF-DRIFT-025,REQ-CONF-DRIFT-026,REQ-CONF-DRIFT-027,REQ-CONF-DRIFT-028,REQ-CONF-DRIFT-029,REQ-CONF-DRIFT-030 -->
- **REQ-CONF-DRIFT-001 — SHALL:** Every tracked documentation object is compared with its canonical registry record for path, class, status, language, layer, scope, canonical references, decisions, requirements, locks, exceptions, dependencies, tags, and generation policy.
- **REQ-CONF-DRIFT-002 — SHALL:** Document drift detection distinguishes structural drift, reference drift, ownership drift, normative drift, dependency drift, generated-content drift, scope drift, lifecycle drift, traceability drift, terminology drift, and parallel-authority drift.
- **REQ-CONF-DRIFT-003 — SHALL NOT:** Textual similarity, matching titles, repeated wording, file proximity, repository history, or apparent implementation behavior is treated as proof that documentation objects remain semantically aligned.
- **REQ-CONF-DRIFT-004 — SHALL:** Every canonical concept resolves exactly one active canonical owner and every secondary representation either references that owner explicitly or is generated deterministically from it.
- **REQ-CONF-DRIFT-005 — SHALL NOT:** Normative Markdown, explanatory Markdown, examples, recipes, generated projections, or AI contexts redefine, narrow, broaden, or override a canonical registry value.
- **REQ-CONF-DRIFT-006 — SHALL:** Every normative statement displayed in Markdown resolves one active requirement identifier and agrees with the requirement registry on version, status, strength, scope, owner, source decision, canonical references, locks, and validation.
- **REQ-CONF-DRIFT-007 — SHALL NOT:** A normative keyword outside an approved generated requirement block creates or modifies active authority.
- **REQ-CONF-DRIFT-008 — SHALL:** Every generated file and generated block is reproducible from its declared canonical sources, generator identity, generator version, renderer, ordering rules, and active generation policy.
- **REQ-CONF-DRIFT-009 — SHALL:** Generated-content validation reconstructs the expected output in a clean validation context and compares it exactly with the tracked output.
- **REQ-CONF-DRIFT-010 — SHALL NOT:** A generated file or generated block is repaired by manual editing when regeneration can reproduce the canonical result.
- **REQ-CONF-DRIFT-011 — SHALL:** Every canonical reference resolves to an existing active object or an explicitly permitted historical or migration object within the referencing object's scope.
- **REQ-CONF-DRIFT-012 — SHALL:** Every JSON Pointer, document identity, requirement identifier, lock identifier, decision identifier, test identifier, evidence identifier, profile identifier, component identifier, artifact-class identifier, release-channel identifier, and integration identifier is validated against its canonical registry.
- **REQ-CONF-DRIFT-013 — SHALL:** Every semantic document dependency is declared by document identity and the dependency graph is validated for missing nodes, undeclared edges, stale edges, incompatible lifecycle states, and prohibited cycles.
- **REQ-CONF-DRIFT-014 — SHALL NOT:** A Markdown hyperlink, import, include, citation, or shared tag substitutes for a declared semantic dependency.
- **REQ-CONF-DRIFT-015 — SHALL:** Scope validation detects globalized profile rules, inherited rules without an active inheritance declaration, component behavior outside system or profile boundaries, and migration-only facts presented as current authority.
- **REQ-CONF-DRIFT-016 — SHALL:** Lifecycle validation detects active references to draft, proposed, rejected, deprecated, superseded, archived, revoked, retired, or otherwise non-authorizing objects unless the relationship explicitly permits historical reference.
- **REQ-CONF-DRIFT-017 — SHALL:** Terminology validation detects prohibited synonyms, conflicting identifiers, changed meanings, stale aliases, and inconsistent casing or naming where the terminology registry defines a canonical form.
- **REQ-CONF-DRIFT-018 — SHALL:** Traceability validation detects disagreement among document metadata, requirement declarations, locks, decisions, tests, evidence, exceptions, profiles, components, artifact contracts, and reverse indexes.
- **REQ-CONF-DRIFT-019 — SHALL:** Every semantic change produces a direct and transitive impact report covering canonical registries, pointers, documents, requirements, locks, decisions, ADRs, profiles, components, artifact contracts, tests, evidence, exceptions, generated projections, and AI contexts.
- **REQ-CONF-DRIFT-020 — SHALL:** Every object in an impact report receives an explicit disposition of updated, reviewed_no_change, regenerated, deprecated, superseded, archived, or blocked before the change is accepted.
- **REQ-CONF-DRIFT-021 — SHALL NOT:** A semantic change is accepted while an affected object lacks an impact disposition or while a required dependent projection remains stale.
- **REQ-CONF-DRIFT-022 — SHALL:** AI context validation confirms that every package is generated from active authority, contains only its declared scope, follows the canonical read order, includes applicable prohibitions, and excludes stale, inactive, or unrelated objects.
- **REQ-CONF-DRIFT-023 — SHALL NOT:** A generated AI context, catalog, matrix, index, manifest, or report becomes independent authority or remains valid after any canonical source affecting it changes.
- **REQ-CONF-DRIFT-024 — SHALL:** Examples and recipes are validated for references, terminology, prohibited assumptions, profile scope, component boundaries, secret leakage, and contradiction with active authority.
- **REQ-CONF-DRIFT-025 — SHALL NOT:** Repeated implementation practice, recipe wording, non-authoritative documentation, archived material, or an example silently becomes a global requirement.
- **REQ-CONF-DRIFT-026 — SHALL:** Drift validation runs from a clean repository state using the registered schemas, generators, validators, canonical source versions, and deterministic ordering rules.
- **REQ-CONF-DRIFT-027 — SHALL:** A detected drift condition identifies its class, source object, affected object, canonical owner, expected value or relationship, observed value or relationship, impact scope, and blocking status.
- **REQ-CONF-DRIFT-028 — SHALL:** Drift in active authority, normative statements, ownership, scope, lifecycle, dependencies, locks, traceability, or generated implementation context blocks the affected merge, release, profile claim, conformance claim, or authority activation.
- **REQ-CONF-DRIFT-029 — SHALL NOT:** A validator invents missing decisions, ownership, references, scope, dependencies, requirements, locks, tests, evidence, exceptions, or content to suppress a drift finding.
- **REQ-CONF-DRIFT-030 — SHALL:** Every active document-drift requirement is traceable to accepted decisions, applicable locks, validation tests, and required evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Checking a proposed change

A proposed change is checked in this order:

1. confirm a clean repository state;
2. identify changed files and canonical objects;
3. classify each change;
4. resolve accepted decisions;
5. validate schemas and inventory;
6. compute direct and transitive impact;
7. validate ownership, references, scope, lifecycle, locks, and traceability;
8. regenerate all affected projections;
9. validate examples, recipes, and AI contexts;
10. run affected tests;
11. collect evidence;
12. verify that every impact object has a disposition;
13. activate authority changes last.

### 6.2 Detecting manual generated-content edits

Generated-content validation resolves the tracked object's generation policy, resolves the active generator and canonical inputs, creates expected output in an isolated clean location, compares structure and content exactly, identifies the divergent region and affected sources, rejects manual output changes, replaces tracked output only through regeneration, and reruns downstream validation.

### 6.3 Detecting canonical-reference drift

Reference validation:

1. parses every registered canonical reference;
2. rejects absolute developer-specific paths;
3. resolves repository-relative paths;
4. resolves JSON Pointers when present;
5. verifies target identity, status, version, and scope;
6. verifies that the referenced object is the canonical owner;
7. invalidates dependent projections and contexts when resolution changes.

### 6.4 Detecting semantic dependency drift

Dependency validation builds the document graph from the documentation registry, verifies every node and edge, compares document metadata dependencies with the registry, detects undeclared semantic consumption, stale and contradictory dependencies, prohibited cycles, and computes transitive dependents.

### 6.5 Handling a drift finding

Drift resolution:

1. preserves the finding and evidence;
2. identifies the canonical owner;
3. classifies whether the owner or dependent is incorrect;
4. creates or references an accepted decision when semantics change;
5. updates the canonical object first when required;
6. updates all affected dependents;
7. regenerates derived outputs;
8. updates tests and evidence;
9. reruns complete validation;
10. closes the finding only when no affected claim remains inconsistent.

### 6.6 Scheduled full-corpus validation


## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Preserved state | Blocked behavior | Validation outcome |
| --- | --- | --- | --- | --- |
| Tracked file is unregistered | Classify it as non-authoritative until registered | Existing active corpus | New file authority | `unregistered_document` |
| Registered file is missing | Invalidate dependent objects | Remaining valid corpus | Missing document's claims | `registered_document_missing` |
| Canonical owner conflicts | Keep all conflicting values inactive | Last valid owner state | Conflicting authority | `canonical_ownership_conflict` |
| Canonical reference fails | Invalidate the reference and dependent projections | Unaffected objects | Affected claim or context | `canonical_reference_not_found` |
| Requirement block differs | Regenerate from the requirement registry | Canonical requirement | Edited normative display | `normative_projection_drift` |
| Freehand normative language appears | Reject the document update | Existing active document version | New normative prose | `unregistered_normative_statement` |
| Generated output differs | Rebuild and compare again | Canonical inputs | Stale derived output | `generated_content_stale` |
| Dependency metadata differs | Use the registry graph and block the inconsistent document | Last valid graph | Affected semantic dependency | `document_dependency_drift` |
| Prohibited cycle appears | Reject affected dependency changes | Acyclic graph | Cyclic activation | `document_dependency_cycle` |
| Scope is broadened | Keep the broader interpretation inactive | Declared canonical scope | Out-of-scope claim | `scope_drift` |
| Non-authorizing lifecycle state is referenced | Reject active use | Historical object identity | Dependent active claim | `lifecycle_authority_drift` |
| Traceability edge is missing | Mark coverage incomplete | Existing valid relationships | Affected claim | `traceability_drift` |
| AI context is stale | Rebuild or withdraw the context | Canonical authority | Implementation use of context | `ai_context_stale` |
| Impact object lacks disposition | Keep the change blocked | Existing active authority | Merge or activation | `impact_disposition_missing` |
| Repository is not clean | Stop authoritative validation | Existing active authority | New validation claim | `unclean_validation_state` |
| Parallel active corpus is detected | Classify external corpus as non-authoritative until disposition | Active `docs/` corpus | Competing authority | `parallel_active_documentation_detected` |

A readable document can remain available for diagnosis while its authority or conformance use is blocked.

## 8. Cross-Component Interactions

### 8.1 Documentation registry

The documentation registry supplies the expected inventory, class, lifecycle, scope, dependencies, and generation policy. Drift validation reports mismatches without silently editing either side.

### 8.2 Canonical domain registries

System, component, profile, lifecycle, security, operations, and conformance registries own their facts. Drift validators compare dependent documents and projections with those owners without becoming domain owners.

### 8.3 Requirement and lock registries

Requirement blocks and lock effects are checked against their canonical records. A document cannot weaken a lock or restate a requirement with a different scope or strength.

### 8.4 Traceability and impact systems

Traceability supplies semantic relationships. Impact analysis traverses those relationships and records dispositions. A missing edge is reported as incomplete authority rather than guessed from textual similarity.

### 8.5 Generators

Generators produce metadata, requirement blocks, catalogs, matrices, manifests, reports, and AI contexts. They consume canonical data and deterministic policies without introducing new architectural values.

### 8.6 CI, merge, release, and authority activation

Continuous validation can run at commit, merge, release, and authority-activation boundaries. A passing repository check supports acceptance only for the exact clean state and canonical versions that were validated.

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Effect |
| --- | --- |
| `DEC-DOC-001` | Keeps the active corpus and validation output in English. |
| `DEC-DOC-002` | Establishes machine-readable canonical owners and derived human-readable projections. |
| `DEC-DOC-003` | Prevents unresolved decisions and ambiguity from entering active authority. |
| `DEC-DOC-004` | Requires deterministic impact analysis and validation before activation. |

### Prohibited assumptions

- equal prose means equal semantics;
- a changed filename preserves document identity automatically;
- a hyperlink declares a semantic dependency;
- a generated file can be safely edited by hand;
- a stale AI context is acceptable because most facts remain correct;
- an example becomes normative through repetition;
- a recipe defines global architecture;
- a passing implementation proves documentation alignment;
- a profile rule can be restated globally;
- a proposed decision can support active content;
- a missing relationship can be inferred from names;
- a deprecated object remains active until deleted;
- regenerated output is correct without validating its canonical inputs;
- an aggregate coverage percentage hides a blocking gap;
- a dirty repository produces authoritative drift evidence;
- migration sources can silently override active documents;
- a validator can choose between conflicting owners;
- a non-semantic label can conceal a major scope or boundary change;
- authority activation can occur before dependent projections are current.

## 10. Validation Criteria

This document is conformant when:

1. `DOC-CONF-007` is active at `09-conformance/07-document-drift-detection.md`.
2. Every canonical reference resolves.
3. Every listed decision exists with status `accepted`.
4. Every requirement in Section 5 exists with identical strength, statement, scope, owner, source decision, canonical references, locks, and validation.
5. Every listed lock exists and is active.
6. Every file under `docs/` is registered or explicitly classified as non-authoritative.
7. Registered document metadata agrees with each tracked file.
8. Every canonical concept has exactly one owner.
9. Every secondary representation is an explicit reference or reproducible generated projection.
10. Requirement blocks agree exactly with the requirement registry.
11. No freehand normative keyword appears outside approved generated blocks.
12. Every canonical path, pointer, and identifier resolves.
13. Semantic dependencies use document identities and the graph remains acyclic.
14. Scope, inheritance, component, artifact, lifecycle, and migration boundaries agree with canonical contracts.
15. Terminology and identifiers agree with the terminology registry.
16. Traceability forward and reverse relationships agree.
17. Every generated object matches clean deterministic regeneration.
18. Every semantic change has a complete direct and transitive impact report.
19. Every affected object has an explicit disposition.
20. Every AI context matches active authority and its declared scope.
21. Examples and recipes contain no conflicting authority or prohibited assumption.
22. Parallel active documentation is absent.
23. Drift validation runs from a clean repository state.
24. Every blocking drift prevents affected merge, release, claim, or activation.
25. Validators perform no automatic semantic repair.
26. Critical drift checks map to tests and evidence.
27. Active prose is English and contains no unresolved-authority marker.
28. No documentation metadata or source hash field is introduced by this document.

The validation entry point is:

```bash
python docs/tools/validate_docs.py
```

## 11. Non-Normative Examples

> **Non-normative example:** This example illustrates normative drift.

The requirement registry changes a requirement's scope from global to `sovereign_linux_node`. A Markdown requirement block that still displays global scope is stale and is regenerated before the change can activate.

> **Non-normative example:** This example illustrates generated-content drift.

A component catalog is edited manually to add a capability. Clean regeneration omits the capability because it is absent from the component contract, so validation rejects the edit.

> **Non-normative example:** This example illustrates dependency drift.

A profile document begins relying on a new security document but its `depends_on` metadata and documentation-registry edge are not updated. Impact and graph validation report the missing dependency.

> **Non-normative example:** This example illustrates AI-context drift.

A release-channel decision changes, but a generated implementation context still contains the earlier channel mapping. The context is withdrawn from implementation use until rebuilt and validated.

> **Non-normative example:** This example illustrates editorial change.

Correcting punctuation without changing meaning, identifiers, scope, relationships, or generated output can be classified as editorial and does not require a semantic authority change.
