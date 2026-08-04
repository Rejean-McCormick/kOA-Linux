<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONF-002",
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
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "contracts/integration-types.contract.json",
    "contracts/ai-navigation.contract.json"
  ],
  "decision_ids": [
    "DEC-DOC-001",
    "DEC-DOC-002",
    "DEC-DOC-003",
    "DEC-DOC-004"
  ],
  "requirement_ids": [
    "REQ-CONF-TRACE-001",
    "REQ-CONF-TRACE-002",
    "REQ-CONF-TRACE-003",
    "REQ-CONF-TRACE-004",
    "REQ-CONF-TRACE-005",
    "REQ-CONF-TRACE-006",
    "REQ-CONF-TRACE-007",
    "REQ-CONF-TRACE-008",
    "REQ-CONF-TRACE-009",
    "REQ-CONF-TRACE-010",
    "REQ-CONF-TRACE-011",
    "REQ-CONF-TRACE-012",
    "REQ-CONF-TRACE-013",
    "REQ-CONF-TRACE-014",
    "REQ-CONF-TRACE-015",
    "REQ-CONF-TRACE-016",
    "REQ-CONF-TRACE-017",
    "REQ-CONF-TRACE-018",
    "REQ-CONF-TRACE-019",
    "REQ-CONF-TRACE-020",
    "REQ-CONF-TRACE-021",
    "REQ-CONF-TRACE-022",
    "REQ-CONF-TRACE-023",
    "REQ-CONF-TRACE-024",
    "REQ-CONF-TRACE-025",
    "REQ-CONF-TRACE-026",
    "REQ-CONF-TRACE-027",
    "REQ-CONF-TRACE-028",
    "REQ-CONF-TRACE-029",
    "REQ-CONF-TRACE-030"
  ],
  "lock_ids": [
    "LOCK-DOC-002",
    "LOCK-DOC-005",
    "LOCK-DOC-006",
    "LOCK-DOC-007",
    "LOCK-DOC-008",
    "LOCK-DOC-009",
    "LOCK-DOC-010",
    "LOCK-DOC-011",
    "LOCK-DOC-013",
    "LOCK-DOC-019",
    "LOCK-DOC-020"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-003",
    "DOC-GOV-004",
    "DOC-GOV-009",
    "DOC-GOV-010",
    "DOC-CONST-002",
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-PROFILE-001",
    "DOC-COMP-000",
    "DOC-LIFE-002",
    "DOC-SEC-015",
    "DOC-OPS-001",
    "DOC-OPS-012",
    "DOC-CONF-000",
    "DOC-CONF-001"
  ],
  "tags": [
    "conformance",
    "requirements",
    "traceability",
    "decisions",
    "locks",
    "tests",
    "evidence",
    "coverage",
    "impact-analysis",
    "validation"
  ]
}
KOA:DOC-META:END -->

# Requirement Traceability

## 1. Purpose

This document defines how kOA requirements are traced from accepted authority through validation and evidence.

Traceability answers five questions:

1. why a requirement exists;
2. who owns it;
3. where it applies;
4. how it is validated;
5. which evidence supports a conformance, profile, or release claim.

The traceability model is machine-first. Canonical registries own identities and relationships. Markdown explains the model and generated projections make it visible without becoming a second source of authority.

## 2. Scope

This document applies to:

- accepted decisions;
- active requirements;
- active locks;
- normative and explanatory documents;
- canonical registry and JSON Pointer references;
- profiles and overlays;
- component contracts;
- artifact classes and artifact contracts;
- release and conformance claims;
- tests and explicitly assigned manual controls;
- evidence and decision receipts;
- exceptions and waivers;
- ADRs;
- integrations;
- generated indexes, matrices, reports, and AI context packages;
- direct and transitive change-impact analysis;
- migration, supersession, retirement, and historical preservation;
- repository validation before merge, release, profile claims, and authority activation.

This document does not:

- make Markdown links semantic dependencies;
- infer relationships from file names, imports, prose similarity, or implementation behavior;
- make generated matrices canonical owners;
- define the internal business behavior of components;
- replace requirement identification, test-evidence, release-evidence, profile-claim, exception, or migration contracts;
- permit incomplete relationships to be hidden by aggregate percentages;
- authorize automatic semantic repair.

## 3. Canonical References

| Canonical reference | Ownership role |
| --- | --- |
| `generated/traceability.json` | Owns cross-object relationship records, direction, status, coverage, and reverse indexes. |
| `generated/requirements-index.json` | Owns requirement identity, version, status, strength, scope, owner, source, canonical references, locks, and validation declarations. |
| `generated/decision-index.json` | Owns decision identity, status, authority, supersession, and authorization scope. |
| `generated/assertion-index.json` | Owns protected invariants and their executable assertions or manual controls. |
| `generated/document-index.json` | Owns document identity, path, scope, dependencies, and displayed requirement, decision, lock, exception, test, and evidence identifiers. |
| `generated/test-catalog.json` | Owns test identity, subject, method, scope, applicability, expected outcome, and evidence production. |
| `generated/evidence-catalog.json` | Owns evidence identity, producer, subject, scope, provenance, result, retention, and supported claims. |
| `generated/exception-index.json` | Owns authorized deviations, scope, duration, compensating controls, tests, evidence, and review state. |
| `generated/decision-index.json` | Owns ADR identity, decision relationships, lifecycle, and historical rationale references. |
| `generated/profile-catalog.json` and profile contracts | Own profile and overlay applicability used by traceability scope checks. |
| `generated/component-catalog.json` and component contracts | Own component identity and contract applicability used by relationship validation. |
| `contracts/artifact-classes.contract.json` and artifact contracts | Own artifact-class identity and lifecycle applicability. |
| `contracts/release-channels.contract.json` | Owns release-channel identity used by release and artifact traceability. |
| `contracts/ai-navigation.contract.json` | Owns generated AI-context package definitions and canonical source sets. |
| `generated/authority-manifest.json` | Identifies which canonical objects are active authority after all required validation passes. |

The registries own the facts. This document describes how their relationships are checked and used.

## 4. Model and Responsibilities

### 4.1 Traceability graph

The traceability model is a directed graph.

Common node classes include:

- decision;
- requirement;
- lock;
- document;
- profile;
- component;
- artifact class;
- artifact contract;
- release channel;
- integration;
- ADR;
- exception;
- test;
- evidence;
- generated projection;
- AI context package.

Common edge meanings include:

```text
decision authorizes requirement
requirement is explained by document
requirement is constrained by lock
requirement is validated by test
test produces evidence
evidence supports requirement
document depends on document
profile applies requirement
component implements requirement
artifact contract satisfies requirement
exception affects requirement
decision supersedes decision
object contributes to generated projection
```

Exact edge identifiers and fields remain registry-owned.

### 4.2 Requirement chain

A complete basic chain is:

```text
accepted decision
    ↓
active requirement
    ↓
applicable lock
    ↓
validation test or manual control
    ↓
evidence
    ↓
conformance, profile, or release claim
```

Documents, profiles, components, artifact contracts, and exceptions add scope and implementation relationships around this chain.

A requirement is not considered validated merely because it appears in a document.

### 4.3 Directionality and reverse indexes

Relationship direction preserves meaning.

For example:

```text
DEC-DOC-004 authorizes REQ-CONF-TRACE-023
REQ-CONF-TRACE-023 validated_by TEST-CONF-TRACE-023
TEST-CONF-TRACE-023 produces EVID-CONF-TRACE-023
```

Reverse indexes support questions such as:

- which requirements depend on a decision;
- which documents display a requirement;
- which locks constrain a profile claim;
- which tests validate an artifact contract;
- which evidence items support a release;
- which active claims are affected by a changed canonical object.

Forward and reverse representations agree. Reverse indexing does not create a second relationship.

### 4.4 Requirement identity and versions

A requirement identity is stable across compatible wording or metadata corrections governed by the requirement-version policy.

A semantic replacement records:

- predecessor identity and version;
- successor identity and version;
- supersession relationship;
- effective state;
- affected documents and contracts;
- updated tests and evidence;
- migration and compatibility impact.

Historical versions remain traceable and cannot be reused as new objects.

### 4.5 Scope compatibility

A relationship is valid only when endpoint scopes are compatible.

Scope checks can include:

- global;
- profile;
- profile overlay;
- component;
- artifact class;
- development toolchain;
- migration-only;
- release channel;
- environment;
- tenant or node where evidence is execution-specific.

A profile-specific test result cannot support a global claim unless the test catalog and claim contract explicitly establish that relationship.

### 4.6 Tests and controls

A test relationship records:

- test identity and active version;
- validated requirement or lock;
- subject and subject version;
- applicability;
- execution method;
- environment or profile;
- expected outcome;
- failure meaning;
- evidence type;
- evidence producer;
- repeatability or manual-control conditions.

An explicitly assigned manual control remains identifiable, reviewable, and evidence-producing. Unassigned human judgment does not count as validation.

### 4.7 Evidence

Evidence is tied to the exact validation context.

Evidence can identify:

- evidence identity;
- producing test or authority;
- requirement and lock subjects;
- tested document, profile, component, artifact, or release;
- subject version;
- execution environment;
- effective profile;
- result;
- occurrence time;
- provenance;
- retention;
- disclosure;
- supersession or invalidation.

Evidence remains historical when a subject changes, but it no longer supports the new version unless the applicable contract permits reuse.

### 4.8 Exceptions

An exception is a first-class traceability object.

It links:

```text
accepted exception decision
    ↓
exception record
    ↓
affected requirement and lock
    ↓
bounded scope and validity
    ↓
compensating control
    ↓
test and evidence
    ↓
review, expiry, revocation, or closure
```

An exception records a controlled deviation. It does not edit the original requirement or lock.

### 4.9 Coverage

Coverage is evaluated per required relationship, not only as one percentage.

Useful statuses include:

- complete;
- incomplete;
- not applicable;
- exempted by active exception;
- blocked;
- out of current validation scope.

A coverage summary can report counts, but every mandatory gap remains individually visible.

### 4.10 Impact analysis

A semantic change begins at the canonical owner and traverses direct and transitive relationships.

The impact set can include:

- decisions;
- requirements;
- locks;
- documents;
- profiles and overlays;
- components;
- artifact contracts;
- release claims;
- tests;
- evidence;
- exceptions;
- generated projections;
- AI context packages;
- migration obligations.

Impact analysis identifies review and regeneration obligations. It does not automatically approve the changes.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-CONF-TRACE-001,REQ-CONF-TRACE-002,REQ-CONF-TRACE-003,REQ-CONF-TRACE-004,REQ-CONF-TRACE-005,REQ-CONF-TRACE-006,REQ-CONF-TRACE-007,REQ-CONF-TRACE-008,REQ-CONF-TRACE-009,REQ-CONF-TRACE-010,REQ-CONF-TRACE-011,REQ-CONF-TRACE-012,REQ-CONF-TRACE-013,REQ-CONF-TRACE-014,REQ-CONF-TRACE-015,REQ-CONF-TRACE-016,REQ-CONF-TRACE-017,REQ-CONF-TRACE-018,REQ-CONF-TRACE-019,REQ-CONF-TRACE-020,REQ-CONF-TRACE-021,REQ-CONF-TRACE-022,REQ-CONF-TRACE-023,REQ-CONF-TRACE-024,REQ-CONF-TRACE-025,REQ-CONF-TRACE-026,REQ-CONF-TRACE-027,REQ-CONF-TRACE-028,REQ-CONF-TRACE-029,REQ-CONF-TRACE-030 -->
- **REQ-CONF-TRACE-001 — SHALL:** Every active normative requirement has one stable requirement identifier, one active version, one status, one strength, one scope, one owner, one accepted source decision, canonical references, applicable locks, and validation relationships.
- **REQ-CONF-TRACE-002 — SHALL:** The traceability registry is the canonical owner of cross-object relationships among documents, decisions, requirements, locks, tests, evidence, profiles, components, artifacts, integrations, exceptions, and generated projections.
- **REQ-CONF-TRACE-003 — SHALL NOT:** Markdown links, repeated prose, file proximity, naming similarity, implementation imports, issue references, or repository history substitute for a canonical traceability relationship.
- **REQ-CONF-TRACE-004 — SHALL:** Every traceability relationship identifies a valid source object, valid target object, relationship type, direction, status, scope, and canonical registry location.
- **REQ-CONF-TRACE-005 — SHALL:** Every active requirement resolves at least one accepted owner decision and every referenced decision authorizes the requirement within its declared scope.
- **REQ-CONF-TRACE-006 — SHALL NOT:** A proposed, rejected, archived, unresolved, or otherwise non-authorizing decision supports an active requirement, profile claim, release claim, conformance claim, or implementation context.
- **REQ-CONF-TRACE-007 — SHALL:** Every active requirement resolves every declared canonical reference and the referenced object remains active and compatible with the requirement scope.
- **REQ-CONF-TRACE-008 — SHALL:** Every active requirement resolves every declared lock and each lock protects at least one observable assertion relevant to that requirement.
- **REQ-CONF-TRACE-009 — SHALL:** Every active requirement has at least one applicable validation relationship to an active test or an explicitly assigned manual control.
- **REQ-CONF-TRACE-010 — SHALL:** Every conformance claim resolves the required evidence produced by the tests or controls that validate its requirements.
- **REQ-CONF-TRACE-011 — SHALL NOT:** A test result is represented as evidence for a requirement outside the test's declared validation scope, profile, component, artifact class, version, environment, or execution context.
- **REQ-CONF-TRACE-012 — SHALL:** Every evidence item records the producing test or authority, evidenced requirements, evidenced documents or claims, subject version, execution context, outcome, time, provenance, and retention status.
- **REQ-CONF-TRACE-013 — SHALL:** Document metadata requirement identifiers, decision identifiers, lock identifiers, exceptions, dependencies, tests, and evidence agree with the canonical registries and traceability graph.
- **REQ-CONF-TRACE-014 — SHALL:** Every semantic document dependency is represented by document identity and contributes to transitive impact analysis.
- **REQ-CONF-TRACE-015 — SHALL NOT:** A document, requirement, lock, test, evidence item, profile claim, release claim, or generated context references a retired identifier as though it were a new active object.
- **REQ-CONF-TRACE-016 — SHALL:** Supersession preserves predecessor and successor identities, relationship direction, effective version, impact set, migration obligations, and historical evidence.
- **REQ-CONF-TRACE-017 — SHALL:** Exceptions and waivers identify the exact affected requirements, locks, scopes, profiles, components, versions, authorizing decision, validity period, compensating controls, tests, evidence, and review state.
- **REQ-CONF-TRACE-018 — SHALL NOT:** An exception broadens scope, changes canonical ownership, replaces an accepted decision, or silently removes a validation or evidence obligation.
- **REQ-CONF-TRACE-019 — SHALL:** The traceability graph supports forward traversal from decisions to requirements, documents, tests, and evidence and reverse traversal from evidence and tests to the requirements and decisions they support.
- **REQ-CONF-TRACE-020 — SHALL:** Forward and reverse indexes agree on relationship identity, endpoints, type, status, and scope.
- **REQ-CONF-TRACE-021 — SHALL:** Coverage calculations use canonical active-object inventories and distinguish complete, incomplete, not applicable, exempted, blocked, and out-of-scope relationships.
- **REQ-CONF-TRACE-022 — SHALL NOT:** A numeric coverage percentage hides missing mandatory relationships, unresolved references, inactive authority, failed tests, missing evidence, or scope conflicts.
- **REQ-CONF-TRACE-023 — SHALL:** A semantic change produces an impact set covering direct and transitive decisions, requirements, locks, documents, profiles, components, artifact contracts, tests, evidence, generated projections, and AI context packages.
- **REQ-CONF-TRACE-024 — SHALL:** Traceability validation is executed from a clean repository state against schema-valid canonical registries and deterministic generated projections.
- **REQ-CONF-TRACE-025 — SHALL:** A missing required relationship, broken endpoint, contradictory edge, scope mismatch, inactive authority, or stale generated projection blocks the affected conformance, profile, or release claim.
- **REQ-CONF-TRACE-026 — SHALL NOT:** Validation automatically invents decisions, relationships, scopes, tests, evidence, exceptions, or semantic repairs.
- **REQ-CONF-TRACE-027 — SHALL:** Traceability changes are versioned, reviewed, validated for referential integrity and coverage impact, and activated with the canonical objects they describe.
- **REQ-CONF-TRACE-028 — SHALL:** Generated traceability matrices, indexes, reports, and AI contexts remain derived views and disclose their canonical sources and generation context.
- **REQ-CONF-TRACE-029 — SHALL:** Validation detects duplicate identifiers, orphan objects, missing reverse links, inconsistent scopes, unresolved decisions, unvalidated locks, tests without subjects, evidence without producers, stale versions, and relationship cycles prohibited by the active model.
- **REQ-CONF-TRACE-030 — SHALL:** Every active requirement-traceability requirement is itself traceable to accepted decisions, applicable locks, validation tests, and required evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Registering a requirement

Requirement registration:

1. assigns the stable requirement identity and version;
2. resolves an accepted source decision;
3. records strength, scope, owner, and statement;
4. resolves canonical references;
5. resolves applicable locks;
6. defines validation tests or manual controls;
7. identifies required evidence;
8. records explaining documents and implementing contracts;
9. validates all graph endpoints and scopes;
10. activates the requirement only after the complete chain passes.

### 6.2 Registering a validation relationship

Validation registration:

1. resolves the active requirement or lock;
2. resolves the test or manual-control identity;
3. records subject, version, profile, component, artifact, or environment applicability;
4. records expected outcomes and failure meaning;
5. records the evidence type and producer;
6. updates forward and reverse indexes;
7. validates endpoint status and scope;
8. activates the relationship with its canonical owners.

### 6.3 Recording evidence

Evidence registration:

1. resolves the producing test or authority;
2. resolves the exact tested subjects and versions;
3. records execution context and effective profile;
4. records outcome, time, provenance, and disclosure;
5. records supported requirements, locks, documents, and claims;
6. validates that the producer is authorized for those relationships;
7. updates reverse indexes;
8. calculates coverage without hiding failed or missing obligations.

### 6.4 Changing a requirement

Requirement change:

1. classifies the change as editorial, compatible, or semantic;
2. resolves the accepted authorizing decision;
3. preserves the predecessor version;
4. computes direct and transitive impact;
5. updates locks, documents, profiles, components, artifact contracts, tests, and evidence obligations;
6. regenerates derived projections;
7. validates the complete graph;
8. activates the replacement last.

### 6.5 Applying an exception

Exception application:

1. resolves the active requirement and lock;
2. resolves the accepted exception decision;
3. records exact scope, validity, and reason;
4. records compensating controls;
5. assigns tests and evidence;
6. updates affected claims and coverage;
7. blocks use outside the exception scope;
8. expires, revokes, renews, or closes through an explicit transition.

### 6.6 Validating traceability

Validation:

1. starts from a clean repository state;
2. validates every canonical registry against its schema;
3. builds the active-object inventory;
4. resolves every relationship endpoint;
5. verifies status, version, direction, and scope;
6. compares forward and reverse indexes;
7. detects duplicate, orphaned, stale, conflicting, and cyclic relationships;
8. calculates mandatory relationship coverage;
9. blocks affected claims for every mandatory gap;
10. regenerates and verifies matrices, reports, and AI contexts.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Preserved state | Blocked behavior | Validation outcome |
| --- | --- | --- | --- | --- |
| Requirement has no accepted decision | Keep the requirement inactive | Existing accepted authority | Requirement and dependent claims | `missing_owner_decision` |
| Canonical reference does not resolve | Invalidate the relationship | Unaffected graph | Affected requirement and projections | `canonical_reference_not_found` |
| Requirement has no validation | Mark coverage incomplete | Requirement history | Conformance claim | `missing_validation_relationship` |
| Required evidence is missing | Preserve test outcome records | Existing unrelated evidence | Claim requiring that evidence | `missing_required_evidence` |
| Test scope conflicts with requirement scope | Reject the validation edge | Test and requirement identities | Scope-incompatible claim | `traceability_scope_mismatch` |
| Forward and reverse links disagree | Reject the conflicting relationship set | Last valid traceability graph | Affected claims and projections | `traceability_index_mismatch` |
| Duplicate active identifier exists | Block every conflicting object | Historical identities | Conflicting active objects | `duplicate_active_identifier` |
| Object is orphaned | Report the object and missing relationship | Object history | Active use requiring the missing edge | `orphan_traceability_object` |
| Retired identifier is reused | Reject the new object | Historical retired object | New activation | `retired_identifier_reuse` |
| Exception expired | Remove exception coverage and recalculate claims | Original requirement and evidence | Continued exempted claim | `exception_not_active` |
| Evidence subject version changed | Preserve historical evidence | Previous-version claim history | New-version claim | `evidence_subject_version_mismatch` |
| Generated matrix is stale | Regenerate from canonical sources | Canonical graph | Use of stale projection | `generated_projection_stale` |
| Cycle violates graph policy | Reject affected dependencies | Acyclic valid subgraph | Affected activation | `prohibited_traceability_cycle` |
| Repository is not clean | Stop authority validation | Existing active authority | New conformance or release claim | `unclean_validation_state` |
| Registry is only partially populated | Report exact missing coverage | Existing represented relationships | Completeness claim | `traceability_coverage_incomplete` |

Incomplete traceability blocks affected claims. It does not authorize validators to invent missing relationships.

## 8. Cross-Component Interactions

### 8.1 Documentation and registries

Documentation metadata displays identifiers drawn from canonical registries.

The traceability validator compares those displayed identifiers with the documentation registry, requirement registry, lock registry, and relationship graph. Markdown does not author the relationship independently.

### 8.2 Profiles

Profile claims select applicable requirements, locks, tests, and evidence.

A profile can add stricter requirements and controls. It cannot generalize its evidence to another profile without an explicit compatible relationship.

### 8.3 Components

Component contracts declare applicable requirements, owned interfaces, data boundaries, artifacts, failure behavior, and tests.

Traceability connects those declarations to global and profile authority without transferring component ownership to the conformance system.

### 8.4 Lifecycle and releases

A release claim resolves:

- artifact identities and versions;
- release channels;
- applicable requirements and locks;
- verification and compatibility tests;
- produced evidence;
- effective profiles;
- exceptions;
- Release Set relationships.

A release cannot use stale evidence from a materially different artifact or profile context.

### 8.5 Test and evidence systems

Test runners produce results through test-catalog identities.

Evidence systems preserve authorized evidence and provenance. They do not decide which requirement exists or broaden the test's declared scope.

### 8.6 Generated projections and AI contexts

Generated matrices, indexes, impact reports, and AI contexts consume the canonical graph.

They can improve navigation and implementation context. They remain invalid when stale and cannot replace missing canonical authority.

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Effect |
| --- | --- |
| `DEC-DOC-001` | Keeps active documentation and canonical identifiers in English. |
| `DEC-DOC-002` | Establishes machine-readable canonical ownership and generated human-readable projections. |
| `DEC-DOC-003` | Requires complete decision closure before dependent authority becomes active. |
| `DEC-DOC-004` | Requires deterministic impact analysis and validation before authority activation. |

### Prohibited assumptions

- a hyperlink declares a semantic dependency;
- a requirement is valid because it appears in several documents;
- a test name proves that it validates a requirement;
- a passing test supports every profile and version;
- an evidence file supports a claim without a producing relationship;
- a generated matrix is canonical authority;
- an aggregate percentage proves complete mandatory coverage;
- a proposed decision can authorize implementation;
- a stale evidence item automatically applies to a changed subject;
- an expired exception remains effective;
- a retired identifier can be recycled;
- similar names imply equivalent scope;
- an issue or commit message replaces a traceability edge;
- a validator can infer missing semantic relationships;
- a reverse index can disagree with the canonical forward edge;
- a document can list a requirement that is absent from the registry;
- a release claim can omit failed or blocked evidence;
- migration is complete because replacement files exist;
- current runtime behavior proves conformance;
- repository validation from a dirty state is authoritative.

## 10. Validation Criteria

This document is conformant when:

1. `DOC-CONF-002` is active at `09-conformance/02-requirement-traceability.md`.
2. Every canonical reference resolves.
3. Every listed decision exists with status `accepted`.
4. Every requirement in Section 5 exists with identical strength, statement, scope, owner, source decision, canonical references, locks, and validation.
5. Every listed lock exists and is active.
6. Every active requirement has exactly one identity, active version, owner, strength, scope, and accepted source decision.
7. Every requirement canonical reference resolves to an active compatible object.
8. Every requirement lock relationship resolves and has a validation assertion or manual control.
9. Every active requirement has applicable validation.
10. Every conformance claim has required evidence.
11. Tests cannot validate subjects outside declared scope and versions.
12. Evidence resolves its producer, subjects, versions, context, result, provenance, and retention.
13. Document metadata agrees with canonical registries and traceability links.
14. Semantic document dependencies use document identities and the graph remains acyclic.
15. Supersession preserves predecessor, successor, impact, tests, evidence, and history.
16. Exceptions are active, scoped, authorized, time-bounded, compensated, tested, and evidenced.
17. Forward and reverse indexes agree exactly.
18. Coverage reports expose every mandatory missing or failed relationship.
19. Impact analysis includes all direct and transitive canonical and generated dependents.
20. Validation runs from a clean repository state.
21. Missing, conflicting, stale, inactive, or scope-invalid relationships block affected claims.
22. Validators perform no automatic semantic repair.
23. Generated matrices, reports, and AI contexts match canonical sources.
24. Retired identifiers remain reserved.
25. Duplicate and orphan objects are rejected or reported as incomplete.
26. Critical traceability paths map to tests and evidence.
27. Active prose is English and contains no unresolved-authority marker.
28. No normative keyword appears outside the generated requirement block.

The validation entry point is:

```bash
python docs/tools/validate_docs.py
```

## 11. Non-Normative Examples

> **Non-normative example:** This example illustrates a complete requirement chain.

`DEC-DEV-001` can authorize a workspace-isolation requirement. A development lock constrains it, a repository test validates it, and an evidence item records the result for the two developer profiles.

> **Non-normative example:** This example illustrates scope mismatch.

A test executed only for `developer_linux_workstation` does not by itself support a `developer_windows_wsl` or global conformance claim.

> **Non-normative example:** This example illustrates historical evidence.

Evidence for Runtime Pack version `1.2.3` remains valid historical evidence after version `1.3.0` is published. It does not support the new version unless the artifact contract explicitly permits reuse.

> **Non-normative example:** This example illustrates an exception.

A time-bounded exception can affect one requirement for one profile and version. Its compensating control, test, evidence, review date, and expiry remain visible while the original requirement stays unchanged.

> **Non-normative example:** This example illustrates generated projections.

A traceability matrix can display decision-to-requirement-to-test-to-evidence chains. Editing the matrix cannot change those chains; the canonical registries must change first.
