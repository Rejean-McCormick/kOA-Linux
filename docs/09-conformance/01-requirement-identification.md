<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONF-001",
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
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/profile-catalog.json",
    "generated/component-catalog.json",
    "contracts/artifact-classes.contract.json"
  ],
  "decision_ids": [
    "DEC-DOC-001",
    "DEC-DOC-002",
    "DEC-DOC-003",
    "DEC-COMP-001",
    "DEC-PROFILE-BASELINE-001"
  ],
  "requirement_ids": [
    "REQ-CONF-ID-001",
    "REQ-CONF-ID-002",
    "REQ-CONF-ID-003",
    "REQ-CONF-ID-004",
    "REQ-CONF-ID-005",
    "REQ-CONF-ID-006",
    "REQ-CONF-ID-007",
    "REQ-CONF-ID-008",
    "REQ-CONF-ID-009",
    "REQ-CONF-ID-010",
    "REQ-CONF-ID-011",
    "REQ-CONF-ID-012",
    "REQ-CONF-ID-013",
    "REQ-CONF-ID-014",
    "REQ-CONF-ID-015",
    "REQ-CONF-ID-016",
    "REQ-CONF-ID-017",
    "REQ-CONF-ID-018",
    "REQ-CONF-ID-019",
    "REQ-CONF-ID-020",
    "REQ-CONF-ID-021",
    "REQ-CONF-ID-022",
    "REQ-CONF-ID-023",
    "REQ-CONF-ID-024",
    "REQ-CONF-ID-025",
    "REQ-CONF-ID-026",
    "REQ-CONF-ID-027",
    "REQ-CONF-ID-028",
    "REQ-CONF-ID-029",
    "REQ-CONF-ID-030"
  ],
  "lock_ids": [
    "LOCK-DOC-001",
    "LOCK-DOC-002",
    "LOCK-DOC-003",
    "LOCK-DOC-004",
    "LOCK-DOC-005",
    "LOCK-DOC-006",
    "LOCK-DOC-007",
    "LOCK-DOC-008",
    "LOCK-CONF-001",
    "LOCK-CONF-002",
    "LOCK-CONF-003",
    "LOCK-CONF-004",
    "LOCK-CONF-005"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-CONF-000"
  ],
  "tags": [
    "conformance",
    "requirements",
    "requirement-identifiers",
    "normative-language",
    "traceability",
    "validation",
    "lifecycle",
    "change-control",
    "generated-requirements"
  ]
}
KOA:DOC-META:END -->

# Requirement Identification

## 1. Purpose

This document defines how normative requirements are identified, allocated, owned, versioned, referenced, rendered, changed, retired, and validated across the active kOA corpus.

A requirement identifier is the permanent identity of one normative obligation.

It is not:

- a document paragraph number;
- a section number;
- a roadmap sequence;
- a priority value;
- a test identifier;
- a release identifier;
- a profile identifier;
- an implementation task;
- a generated display label.

The canonical requirement statement and its strength belong to:

```text
generated/requirements-index.json
```

Normative Markdown explains context, responsibilities, procedures, failure behavior, and examples. It selects canonical requirements by identifier and displays them through generated requirement blocks.

The identification model supports:

- stable references across document moves;
- machine-readable scope;
- explicit canonical ownership;
- accepted decision closure;
- independent validation;
- requirement-to-test-to-evidence traceability;
- controlled semantic changes;
- safe splitting and merging;
- permanent reservation of historical identifiers;
- generated projections without duplicated authority;
- exact conformance claims.

The principal identity rule is:

```text
one normative obligation
    ↔
one canonical requirement identifier
```

A requirement can appear in several valid projections, but those projections refer to the same canonical identifier and do not create additional obligations.

## 2. Scope

This document applies to every normative requirement used by:

- constitutional documents;
- governance documents;
- system-baseline documents;
- profile contracts;
- profile overlays;
- component registries and component contracts;
- artifact classes and artifact contracts;
- toolchain contracts;
- development standards;
- lifecycle standards;
- security standards;
- operations standards;
- conformance standards;
- migration controls;
- tests and evidence;
- generated matrices and AI context packages;
- exceptions and conformance claims.

It applies from initial requirement discovery through:

```text
candidate obligation
canonical-owner selection
atomic statement design
namespace allocation
identifier reservation
registry activation
document projection
validation
implementation
test and evidence linkage
semantic change
supersession
deprecation
retirement
historical retention
```

It governs requirement identity and the minimum metadata needed to interpret that identity.

It does not own:

- the accepted architectural decision that creates the obligation;
- the canonical fact constrained by the obligation;
- the implementation design;
- the exact test procedure;
- the evidence object;
- the exception object;
- the document inventory;
- the interfile lock assertion.

Those facts remain with their respective canonical registries and contracts.

## 3. Canonical References

| Canonical reference | Responsibility |
| --- | --- |
| `generated/requirements-index.json` | Requirement identifiers, versions, lifecycle, strength, statements, scope, owner, source decisions, canonical references, linked locks, and validation declarations. |
| `contracts/terminology.contract.json` | Canonical meanings of requirement, identifier, strength, scope, owner, source, validation, supersession, and conformance terms. |
| `generated/decision-index.json` | Accepted owner decisions from which active requirements derive. |
| `generated/authority-manifest.json` | Authority order and active registry versions. |
| `generated/document-index.json` | Document identifiers, paths, classes, scopes, dependencies, and allowed requirement projections. |
| `generated/assertion-index.json` | Cross-file invariants linked to requirements. |
| `generated/traceability.json` | Requirement relationships to profiles, components, artifacts, tests, evidence, exceptions, documents, and conformance claims. |
| `generated/test-catalog.json` | Test identities, procedures, fixtures, expected results, and applicability. |
| `generated/evidence-catalog.json` | Evidence identities, producers, retention, integrity, scope, and requirement coverage. |
| `generated/exception-index.json` | Approved bounded exceptions and compensating controls linked to exact requirements. |
| `generated/decision-index.json` | Accepted architectural records supporting implementation and change rationale. |
| `generated/profile-catalog.json` | Active profile and profile-overlay identifiers used in requirement scope. |
| `generated/component-catalog.json` | Active component identifiers, responsibilities, and data owners used in requirement scope and traceability. |
| `contracts/artifact-classes.contract.json` | Active artifact-class identifiers used in requirement scope and traceability. |

The requirements registry owns the obligation.

The traceability registry owns the relationship graph around the obligation.

A Markdown occurrence is a generated view.

## 4. Model and Responsibilities

### 4.1 Identifier grammar

The canonical human-readable form is:

```text
REQ-<DOMAIN-PATH>-<NUMBER>
```

The effective grammar is equivalent to:

```text
^REQ-[A-Z][A-Z0-9]*(?:-[A-Z][A-Z0-9]*)*-[0-9]{3}$
```

Examples of valid families include:

```text
REQ-DOC-006
REQ-DEV-UV-001
REQ-SEC-ID-003
REQ-SEC-CULT-014
REQ-OPS-HEALTH-002
REQ-CONF-ID-001
```

The first segment is always `REQ`.

The final segment is a three-digit allocation number.

The segments between them form the registered domain path.

A domain path groups related requirements for allocation and review. It does not create authority by itself.

### 4.2 Domain path

A domain path reflects the canonical obligation family at the time of allocation.

Common patterns include:

| Pattern | Meaning |
| --- | --- |
| `REQ-DOC-NNN` | Documentation governance and canonical corpus controls. |
| `REQ-SYS-NNN` | Global system-baseline obligations. |
| `REQ-PRO-NNN` | Profile-model obligations. |
| `REQ-COMP-NNN` | Cross-component or component-contract obligations. |
| `REQ-DEV-NNN` | Development-baseline obligations. |
| `REQ-DEV-UV-NNN` | Python and UV toolchain obligations. |
| `REQ-LIFE-NNN` | Artifact and release lifecycle obligations. |
| `REQ-SEC-NNN` | Cross-cutting security obligations. |
| `REQ-SEC-ID-NNN` | Identity, trust, and signature obligations. |
| `REQ-SEC-CULT-NNN` | Cultural-rights and consent obligations. |
| `REQ-OPS-NNN` | Cross-cutting operational obligations. |
| `REQ-OPS-HEALTH-NNN` | Health and readiness obligations. |
| `REQ-CONF-NNN` | Cross-cutting conformance obligations. |
| `REQ-CONF-ID-NNN` | Requirement-identification obligations. |

The active requirements registry and its schema determine which domain paths are allocated.

A repeated pattern in prose or implementation does not reserve a namespace.

### 4.3 Allocation number

The final number is an identifier allocation, not an ordering mechanism.

It does not indicate:

- implementation sequence;
- importance;
- severity;
- maturity;
- document order;
- test order;
- release order;
- supersession order;
- dependency order.

Gaps are valid.

A removed or retired number remains reserved.

A requirement inserted between two existing requirements receives a new unused number rather than causing renumbering.

### 4.4 Stability

A requirement identifier remains stable when:

- a document is renamed;
- a document path changes;
- a requirement moves to another explanatory document;
- section numbers change;
- a generated matrix changes order;
- a profile projection is added;
- a component projection is added;
- a context package is regenerated;
- tests are reorganized;
- implementation files move;
- the statement receives a non-semantic editorial correction and a new version;
- canonical references are updated without changing the obligation.

The identifier belongs to the obligation rather than to its current presentation.

### 4.5 Requirement record

The canonical requirement record contains at least:

| Field | Meaning |
| --- | --- |
| `requirement_id` | Permanent identity of the obligation. |
| `version` | Version of the canonical requirement record and statement. |
| `status` | Current lifecycle state. |
| `strength` | Normative force selected from the canonical keyword set. |
| `statement` | One atomic normative sentence. |
| `scope` | Applicability boundary and scoped object identifiers. |
| `owner` | Canonical authority responsible for the obligation. |
| `source` | Accepted owner decision establishing the obligation. |
| `canonical_refs` | Active canonical facts needed to interpret the statement. |
| `lock_ids` | Alignment locks that protect the obligation across files. |
| `validation` | Executable checks or assigned manual controls. |

Additional descriptive metadata can include:

- title;
- rationale reference;
- lifecycle dates;
- supersession links;
- tags;
- risk classification;
- review owner;
- change record.

Descriptive metadata does not replace the required fields.

### 4.6 Atomic statement

One requirement describes one compliance proposition.

A useful statement identifies:

```text
subject
normative action or prohibition
object or result
scope or condition when needed
```

A requirement is atomic when one conformance result can evaluate it without producing independent pass and fail outcomes for unrelated obligations.

A statement that combines independent obligations is divided.

For example, environment isolation and port isolation can share a decision and lock family while retaining separate identifiers when they can fail independently.

### 4.7 Strength

Strength is stored separately from the statement.

The canonical strengths are the five keywords defined by the documentation governance contract.

Strength affects:

- conformance interpretation;
- exception handling;
- validator expectations;
- implementation review;
- test coverage;
- reporting.

A strength change can alter the obligation materially even when most words remain unchanged.

A strength is not inferred from tone, punctuation, title, table position, or implementation behavior.

### 4.8 Scope model

Requirement scope uses the strict architecture scope classes:

| Scope kind | Meaning |
| --- | --- |
| `global` | Applies across every conforming composition unless a registered exception narrows one instance. |
| `profile` | Applies only to named active profiles. |
| `profile_overlay` | Applies only when named overlays are active. |
| `component` | Applies to named first-class components or component contracts. |
| `artifact` | Applies to named artifact classes or artifact contracts. |
| `toolchain` | Applies to named toolchain contracts. |

A requirement can identify several objects within one compatible scope kind.

An obligation with materially different strength or behavior in different scopes is separated into multiple requirements.

A profile-specific rule does not become global because multiple profiles adopt it.

A global requirement can be projected into profile documents without changing its scope.

### 4.9 Owner

The owner is the canonical authority responsible for the obligation's meaning and lifecycle.

The owner is not necessarily:

- the document author;
- the implementing component;
- the test owner;
- the repository maintainer;
- the person who proposed the change;
- the generator that rendered the statement.

Examples of owner classes include:

- documentation governance;
- system architecture;
- profile architecture;
- component authority;
- security architecture;
- lifecycle authority;
- operations authority;
- toolchain authority;
- data-owning component.

A change to canonical ownership is reviewed as a material requirement change.

### 4.10 Source decision

Every active requirement derives from an accepted owner decision.

The source decision answers why the obligation exists and who closed the architectural choice.

A requirement can reference one principal source decision and additional accepted decisions when the registry contract permits them.

A requirement does not derive authority from:

- common practice;
- an implementation default;
- a recipe;
- an issue comment;
- an AI-generated suggestion;
- an archived document;
- a draft profile;
- a test fixture;
- repeated prose.

A missing accepted source decision blocks activation.

### 4.11 Canonical references

Canonical references point to the active facts needed to interpret the obligation.

Examples include:

- a system-registry pointer;
- a component-registry entry;
- a profile contract;
- an artifact class;
- a toolchain contract;
- a schema property;
- a lifecycle contract.

Canonical references do not duplicate the requirement statement.

A requirement can remain stable when one canonical path is replaced, provided the obligation remains materially identical and the path migration is controlled.

### 4.12 Locks

A lock protects consistency across several authoritative or explanatory objects.

A requirement can link to several locks.

A lock can protect several requirements.

The requirement describes the obligation.

The lock describes the cross-file invariant and its assertions.

Neither object replaces the other.

### 4.13 Validation

Every active requirement has a validation path.

Validation can include:

- schema validation;
- repository inspection;
- static analysis;
- contract test;
- integration test;
- negative test;
- profile conformance test;
- artifact verification;
- runtime observation;
- evidence review;
- assigned manual control.

A manual control identifies:

- control owner;
- procedure;
- input;
- expected result;
- evidence;
- review interval or trigger;
- failure disposition.

A statement is not exempt from validation because it is architectural or difficult to automate.

### 4.14 Traceability

Traceability records the graph around a requirement.

Typical relationships include:

```text
decision → requirement
requirement → canonical fact
requirement → lock
requirement → document
requirement → profile
requirement → component
requirement → artifact
requirement → test
test → evidence
requirement → exception
requirement → conformance claim
requirement → superseding requirement
```

The traceability registry owns these graph relationships where the relationship is not already an intrinsic requirement field.

A document metadata list is a projection used to select requirements for that document.

### 4.15 Document projection

A normative document declares applicable requirement identifiers in its generated metadata.

Its requirements section renders the same identifiers through a generated block.

The block preserves:

- identifier;
- strength;
- exact statement;
- registry order or explicitly declared render order.

The surrounding prose can explain the requirement but cannot redefine its strength, scope, owner, source, or statement.

A requirement can appear in more than one document when each document has a valid semantic reason and the documentation registry permits the projection.

### 4.16 Generated contexts and matrices

Generated artifacts can project requirements by:

- profile;
- component;
- artifact class;
- toolchain;
- release;
- conformance claim;
- change impact;
- test coverage;
- evidence coverage;
- AI context scope.

A generated projection identifies its canonical source and applicable scope.

It does not allocate new aliases such as `R1`, `MANDATORY-7`, or a local spreadsheet number with normative authority.

Display-only row numbers remain clearly non-canonical.

### 4.17 Requirement lifecycle

The active lifecycle vocabulary is owned by the requirements registry schema.

The principal meanings are:

| Lifecycle state | Interpretation |
| --- | --- |
| `active` | Current authority and applicable to its declared scope. |
| `deprecated` | Still interpretable and possibly applicable during an announced transition, but replacement is expected. |
| `superseded` | Replaced by one or more identified requirements. |
| `retired` | No longer applicable to active conformance, but permanently retained for history and reference integrity. |

Candidate obligations remain outside active authority until the owner decision and registry activation complete.

Lifecycle state is separate from version.

A requirement can receive several versions while remaining active.

### 4.18 Versioning

Version tracks changes to the canonical requirement record.

A version increases when the statement or another interpretation-affecting field changes.

The same identifier can continue when the obligation identity remains the same.

Examples can include:

- grammatical correction that preserves meaning;
- clarification that removes ambiguity without adding or removing compliance behavior;
- canonical-reference replacement with equivalent authority;
- validation refinement that preserves the compliance proposition;
- owner-name normalization that does not transfer authority.

A conformance record identifies the exact version evaluated.

### 4.19 Material change

A new identifier is used when a change alters the identity of the obligation.

Material dimensions include:

- canonical authority;
- regulated subject;
- required or prohibited action;
- normative strength;
- compliance result;
- incompatible scope;
- safety consequence;
- data owner;
- affected component boundary;
- artifact authority;
- exception semantics.

The old identifier remains in history and links to its replacement.

A new identifier avoids making historical evidence appear to prove a different obligation.

### 4.20 Split

A split occurs when one requirement contains several independently evaluable obligations.

The process:

1. preserves the old requirement;
2. allocates one new identifier per atomic obligation;
3. records supersession from the old identifier to all new identifiers;
4. migrates documents, locks, tests, evidence expectations, exceptions, and conformance claims;
5. retires or supersedes the old requirement after coverage validation.

Historical evidence remains associated with the version it actually evaluated.

### 4.21 Merge

A merge occurs when several requirements are proven to describe one indivisible obligation.

The process:

1. identifies all source requirements;
2. accepts the owner decision for the merged meaning;
3. allocates a new identifier;
4. records all source requirements as replaced;
5. migrates every dependent relationship;
6. validates that no scope, exception, test, or evidence distinction was lost.

One source identifier is not silently selected as the survivor when doing so would rewrite the meaning of historical references.

### 4.22 Duplicate detection

Potential duplicates are compared across:

- normalized statement meaning;
- owner;
- source decision;
- subject;
- action;
- object;
- scope;
- strength;
- canonical references;
- validation result.

Similar wording does not always mean duplicate authority.

Two requirements can remain separate when they regulate different scopes or independently passable outcomes.

Exact duplicate obligations are reconciled to one canonical identifier through impact-controlled migration.

### 4.23 Exceptions

An exception references the affected requirement identifier and version.

It records:

- approved scope;
- affected objects;
- start;
- end condition or expiry;
- rationale;
- risk;
- compensating controls;
- owner;
- approval;
- tests;
- evidence;
- revocation or closure.

The requirement itself remains unchanged.

An exception does not create a weaker cloned requirement.

### 4.24 Conformance claims

A conformance claim identifies:

- target profile or composition;
- evaluated requirement identifiers and versions;
- applicability result;
- test results;
- evidence;
- manual controls;
- exceptions;
- evaluation time;
- tool versions;
- claim status.

A claim cannot rely only on a document revision or generic statement that all requirements passed.

Exact requirement identity makes partial and profile-specific claims reviewable.

### 4.25 Historical retention

Historical requirements remain resolvable after deprecation, supersession, or retirement.

Historical retention preserves:

- identifier;
- versions;
- statements;
- strengths;
- scopes;
- owners;
- source decisions;
- lifecycle transitions;
- supersession links;
- tests and evidence that applied at the time;
- exceptions and claims.

Historical retention supports audits, migration, incident review, and interpretation of old receipts.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-CONF-ID-001,REQ-CONF-ID-002,REQ-CONF-ID-003,REQ-CONF-ID-004,REQ-CONF-ID-005,REQ-CONF-ID-006,REQ-CONF-ID-007,REQ-CONF-ID-008,REQ-CONF-ID-009,REQ-CONF-ID-010,REQ-CONF-ID-011,REQ-CONF-ID-012,REQ-CONF-ID-013,REQ-CONF-ID-014,REQ-CONF-ID-015,REQ-CONF-ID-016,REQ-CONF-ID-017,REQ-CONF-ID-018,REQ-CONF-ID-019,REQ-CONF-ID-020,REQ-CONF-ID-021,REQ-CONF-ID-022,REQ-CONF-ID-023,REQ-CONF-ID-024,REQ-CONF-ID-025,REQ-CONF-ID-026,REQ-CONF-ID-027,REQ-CONF-ID-028,REQ-CONF-ID-029,REQ-CONF-ID-030 -->
- **REQ-CONF-ID-001 — SHALL:** Every normative obligation in the active kOA corpus shall have exactly one stable requirement identifier owned by generated/requirements-index.json.
- **REQ-CONF-ID-002 — SHALL:** Every requirement identifier shall match the registered REQ namespace grammar and shall contain a registered uppercase domain path followed by a three-digit allocation number.
- **REQ-CONF-ID-003 — SHALL NOT:** A requirement identifier shall encode document position, section number, priority, implementation order, release version, profile membership, lifecycle status, or test result.
- **REQ-CONF-ID-004 — SHALL:** A requirement identifier shall remain stable when its owning document, rendered section, repository path, profile projection, component projection, or generated context changes.
- **REQ-CONF-ID-005 — SHALL NOT:** A retired, deprecated, superseded, rejected, or otherwise previously allocated requirement identifier shall be reused for another obligation.
- **REQ-CONF-ID-006 — SHALL:** Every requirement shall have one atomic statement with one declared strength and one independently evaluable compliance result.
- **REQ-CONF-ID-007 — SHALL NOT:** One requirement identifier shall represent multiple independently passable obligations joined only for editorial convenience.
- **REQ-CONF-ID-008 — SHALL:** Every active requirement shall declare its version, status, strength, statement, scope, owner, accepted source decision, canonical references, linked locks, and validation method.
- **REQ-CONF-ID-009 — SHALL:** Requirement scope shall use the canonical global, profile, profile-overlay, component, artifact, or toolchain scope model and shall identify every applicable scoped object.
- **REQ-CONF-ID-010 — SHALL NOT:** A profile-, overlay-, component-, artifact-, or toolchain-specific obligation shall be represented as global through omission, repetition, implementation prevalence, or generated projection.
- **REQ-CONF-ID-011 — SHALL:** Requirement ownership shall identify the canonical authority responsible for the obligation and shall remain distinct from the document that explains it and the component that implements it.
- **REQ-CONF-ID-012 — SHALL:** Every active requirement shall derive from an accepted owner decision and shall reference only active canonical objects required to interpret the obligation.
- **REQ-CONF-ID-013 — SHALL NOT:** A proposed, rejected, superseded, archived, missing, or conflicting decision shall support an active requirement.
- **REQ-CONF-ID-014 — SHALL:** Every active requirement shall have at least one executable validation or one explicitly assigned manual control with an owner, procedure, evidence expectation, and failure result.
- **REQ-CONF-ID-015 — SHALL:** Requirement-to-test, requirement-to-evidence, requirement-to-profile, requirement-to-component, requirement-to-artifact, and requirement-to-exception relationships shall be recorded in the canonical traceability model.
- **REQ-CONF-ID-016 — SHALL NOT:** A hyperlink, prose mention, filename, heading, issue reference, commit message, or test name shall substitute for a canonical requirement relationship.
- **REQ-CONF-ID-017 — SHALL:** Normative Markdown shall select requirements by identifier and shall render their identifier, strength, and statement only through an approved generated requirements block.
- **REQ-CONF-ID-018 — SHALL NOT:** A manually authored normative keyword outside an approved generated requirements block shall create or modify an active requirement.
- **REQ-CONF-ID-019 — SHALL:** The set of requirement identifiers declared in a normative document's metadata shall exactly match the identifiers rendered in that document's generated requirements block.
- **REQ-CONF-ID-020 — SHALL:** A requirement statement text change shall increment the requirement version and shall preserve the identifier only when the obligation's authority, subject, action, strength, and compliance meaning remain materially unchanged.
- **REQ-CONF-ID-021 — SHALL:** A material change to requirement authority, subject, action, strength, compliance meaning, or incompatible scope shall create a new requirement identifier and shall explicitly supersede or retire the prior requirement.
- **REQ-CONF-ID-022 — SHALL:** Splitting one requirement into multiple obligations or merging multiple requirements into one obligation shall allocate new identifiers and shall preserve explicit lineage to every replaced identifier.
- **REQ-CONF-ID-023 — SHALL:** Duplicate requirements with the same obligation shall be reconciled to one canonical identifier, and every dependent reference shall be migrated before the duplicate becomes inactive.
- **REQ-CONF-ID-024 — SHALL NOT:** Two active requirements shall have the same identifier, and one active identifier shall not resolve to more than one version or statement.
- **REQ-CONF-ID-025 — SHALL:** Requirement allocation shall be serialized within each registered namespace and shall record the allocated identifier before dependent documents, locks, tests, or evidence are merged.
- **REQ-CONF-ID-026 — SHALL:** Exceptions shall reference the exact affected requirement identifiers and versions, shall remain scoped and bounded, and shall not alter or clone the underlying requirement statement.
- **REQ-CONF-ID-027 — SHALL:** Conformance claims shall identify the exact requirement versions evaluated, the applicable scope, the validation result, the evidence, and every approved exception.
- **REQ-CONF-ID-028 — SHALL:** Generated projections, matrices, reports, context packages, and user interfaces shall preserve canonical requirement identifiers and shall not create independent aliases with normative authority.
- **REQ-CONF-ID-029 — SHALL:** Requirement validation shall fail on identifier collision, invalid grammar, missing fields, inactive authority, invalid scope, missing validation, orphaned references, projection mismatch, illegal reuse, or incomplete supersession lineage.
- **REQ-CONF-ID-030 — SHALL:** A complete requirement-identification conformance claim shall include allocation, grammar, uniqueness, atomicity, ownership, source, scope, lifecycle, versioning, supersession, projection, traceability, exception, and negative-path tests with evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Identifying a candidate obligation

Candidate analysis follows this order:

1. identify the behavior, prohibition, boundary, or result under consideration;
2. identify the canonical fact affected;
3. identify the owner of that fact;
4. identify the accepted decision establishing the obligation;
5. determine whether an active requirement already covers the same proposition;
6. determine the exact scope;
7. separate independently evaluable obligations;
8. identify validation and evidence;
9. prepare the requirement record;
10. request identifier allocation.

A sentence found in existing prose is evidence of intent, not automatic canonical authority.

### 6.2 Allocating an identifier

Allocation:

1. selects the registered domain path;
2. locks or serializes allocation within that namespace;
3. reads the permanently reserved number set;
4. selects an unused three-digit number;
5. creates the requirement identifier;
6. writes the canonical requirement record;
7. validates grammar and uniqueness;
8. records source, scope, owner, locks, and validation;
9. records traceability;
10. releases dependent document and test changes for merge.

The allocation number is not reclaimed when activation later fails.

### 6.3 Activating a requirement

Activation:

1. verifies the source decision is accepted;
2. verifies canonical references are active;
3. verifies scope objects exist;
4. verifies owner authority;
5. verifies atomicity and strength;
6. verifies validation;
7. verifies linked locks;
8. verifies traceability;
9. updates affected normative document metadata;
10. regenerates requirement blocks;
11. runs direct and transitive impact validation;
12. activates the registry record;
13. updates authority only after the complete change passes.

### 6.4 Projecting a requirement into Markdown

Projection:

1. selects the requirement by identifier;
2. verifies document scope and allowed normative source;
3. adds the identifier to generated document metadata;
4. renders the exact canonical strength and statement;
5. preserves generated-block boundaries;
6. validates the identifier set against metadata;
7. checks authored prose for independent normative language;
8. records document dependency and traceability.

Manual statement copying is not a projection mechanism.

### 6.5 Adding tests and evidence

Coverage:

1. identifies the requirement version and scope;
2. defines positive and negative validation cases;
3. assigns test identifiers;
4. defines expected evidence;
5. records applicability by profile, component, artifact, or toolchain;
6. records the relationships in traceability;
7. executes the tests;
8. stores evidence;
9. verifies coverage status;
10. updates the conformance report.

One test can cover several requirements when each result remains independently attributable.

### 6.6 Editing without semantic change

A non-semantic edit:

1. records the change rationale;
2. compares authority, subject, action, object, strength, scope, and compliance result;
3. confirms that the obligation identity is unchanged;
4. increments the requirement version;
5. updates the canonical statement or metadata;
6. regenerates projections;
7. reruns tests affected by interpretation or parsing;
8. preserves the identifier and prior versions.

A reviewer can classify the change as material and redirect it to supersession.

### 6.7 Superseding a requirement

Supersession:

1. accepts the owner decision for the new obligation;
2. allocates the replacement identifier or identifiers;
3. records lineage from the prior requirement;
4. defines migration of profiles, components, documents, locks, tests, evidence, exceptions, and claims;
5. activates replacement requirements;
6. validates all dependents;
7. marks the old requirement superseded;
8. retains all historical versions;
9. updates generated projections.

There is no interval in which dependent authority silently points to both incompatible obligations.

### 6.8 Splitting or merging

Split and merge changes use the supersession process plus coverage checks.

The impact report proves:

- every old obligation is represented or intentionally retired;
- every scope is preserved or changed by accepted decision;
- every test has a disposition;
- every exception has a disposition;
- every evidence expectation has a disposition;
- every document projection has a disposition;
- no old identifier remains active accidentally.

### 6.9 Deprecating and retiring

Deprecation:

1. identifies the transition reason;
2. identifies replacement and migration where applicable;
3. identifies the permitted transition interval;
4. identifies remaining active scopes;
5. updates projections and guidance;
6. preserves validation for remaining applicability.

Retirement:

1. verifies no active scope still depends on the requirement;
2. verifies all replacements and migrations;
3. closes or migrates exceptions;
4. preserves historical records;
5. removes the requirement from active projections;
6. permanently reserves the identifier.

### 6.10 Correcting a collision

When an identifier collision is detected:

1. freeze affected changes;
2. identify the earliest valid canonical allocation;
3. identify every conflicting record and dependent;
4. determine whether any conflicting record reached active authority;
5. allocate new identifiers for invalid conflicting obligations;
6. migrate documents, locks, tests, evidence, exceptions, and claims;
7. preserve incident evidence;
8. validate uniqueness across the full corpus;
9. resume activation only after authority is consistent.

A collision is not fixed by keeping whichever file is read last.

### 6.11 Producing a conformance claim

Claim production:

1. resolves target profile, overlay, component, artifact, or toolchain composition;
2. computes applicable active requirements;
3. freezes the exact requirement versions;
4. resolves tests, manual controls, evidence, and exceptions;
5. executes validation from a clean declared environment;
6. records pass, fail, blocked, not-applicable, and excepted results;
7. verifies evidence completeness;
8. signs or protects the claim when its artifact contract requires it;
9. publishes or retains the claim under its lifecycle contract.

## 7. Failure States and Safe Degradation

| Failure state | Required response |
| --- | --- |
| Identifier grammar is invalid | The requirement record remains inactive and cannot be projected. |
| Domain path is not registered | Allocation is blocked until the canonical namespace is established. |
| Allocation number already exists | The new record is rejected and a new unused number is allocated. |
| Same identifier has different statements | Validation fails and affected authority is frozen until collision repair completes. |
| Same obligation has several active identifiers | Duplicate reconciliation and impact analysis begin; no alias is selected by convenience. |
| Requirement statement contains independent obligations | Activation is blocked until the statement is split or justified as one compliance proposition. |
| Strength is absent or inconsistent | The requirement remains inactive. |
| Scope is absent | The requirement remains inactive rather than defaulting to global. |
| Scoped profile, overlay, component, artifact, or toolchain does not exist | Activation is blocked. |
| Owner is absent or lacks authority | Activation is blocked. |
| Source decision is absent or not accepted | Activation is blocked. |
| Canonical reference does not resolve | Activation or continued active validation fails according to impact severity. |
| Validation is absent | The requirement remains inactive. |
| Manual control lacks owner or evidence | The requirement remains uncovered and cannot support a complete claim. |
| Traceability relationship is missing | The dependent document, test, evidence, exception, or claim remains incomplete. |
| Document metadata and generated block differ | Document validation fails and the generated projection is regenerated from canonical data. |
| Authored prose contains independent normative language | Document validation fails until the obligation is registered or the prose is made explanatory. |
| Statement meaning changes without a new identifier | Change validation fails and supersession analysis begins. |
| Identifier changes during a document move | The move is rejected and the original identifier is restored. |
| Retired identifier is reused | The new record is rejected and the historical identifier remains reserved. |
| Split loses one prior obligation | Supersession remains incomplete and the old requirement cannot retire. |
| Merge loses a scope or exception distinction | Merge remains blocked. |
| Exception points to the wrong version | The exception is invalid for the evaluated claim. |
| Test passes but evidence is missing | The requirement result remains incomplete for evidence-required claims. |
| Generated matrix creates an alias | The alias is treated as display-only and removed from canonical references. |
| Historical version cannot be resolved | Claims and receipts depending on that version remain unverifiable. |
| Registry is unavailable | Existing verified projections can remain readable, but new allocation, activation, and claims remain blocked. |
| Validation tooling is unavailable | No new complete conformance claim is issued. |

Failure preserves identifier history and does not guess requirement authority.

## 8. Cross-Component Interactions

### 8.1 Requirements registry

The requirements registry owns the requirement record and identifier lifecycle.

It does not own component behavior, profile membership, artifact behavior, or test execution.

### 8.2 Documentation registry

The documentation registry identifies which requirements a document projects and which sources are permitted.

A document path change does not change the requirement identifier.

### 8.3 Decision registry

The decision registry supplies accepted owner decisions.

A decision can create, replace, split, merge, narrow, broaden, or retire requirement authority through impact-controlled change.

### 8.4 Terminology registry

The terminology registry owns the meanings of requirement fields and lifecycle concepts.

A local glossary does not redefine requirement identity.

### 8.5 Locks registry

Locks connect requirements to cross-file assertions.

A failed lock can make one or more requirement implementations non-conformant even when individual files pass schema validation.

### 8.6 Traceability registry

The traceability registry owns the relationship graph needed for impact analysis and conformance coverage.

It allows calculation of direct and transitive dependents.

### 8.7 Profile contracts

Profile contracts identify profile-specific capabilities and values.

Requirements reference profiles by canonical identifiers.

A profile can adopt a global requirement or carry profile-scoped requirements without rewriting their identities.

### 8.8 Component contracts

Component contracts implement and expose behaviors constrained by requirements.

A component contract references applicable requirements and tests.

It does not copy a requirement into a new local identifier.

### 8.9 Artifact and toolchain contracts

Artifact and toolchain contracts reference applicable requirements.

Class- or toolchain-specific scope remains explicit.

A recipe can illustrate implementation but cannot allocate requirement authority.

### 8.10 Tests and evidence

Tests produce attributable results for exact requirement versions and scopes.

Evidence records the result under the evidence contract.

A test identifier does not substitute for a requirement identifier.

### 8.11 Exceptions

The exception registry narrows conformance for an approved bounded case.

It does not edit the requirement statement or create a permanent alternate baseline.

### 8.12 Generated contexts

AI contexts, matrices, dashboards, and reports receive requirement subsets through traceability and scope filtering.

They remain derived and non-authoritative.

An AI agent does not allocate, merge, split, or reinterpret requirements without the accepted change workflow.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Accepted decisions

| Decision | Effect |
| --- | --- |
| `DEC-DOC-001` | Establishes one canonical active documentation corpus and machine-readable authority. |
| `DEC-DOC-002` | Establishes canonical ownership, generated requirement projection, and validation separation. |
| `DEC-DOC-003` | Establishes stable identifiers, impact analysis, retirement reservation, and decision closure. |
| `DEC-COMP-001` | Keeps component behavior and data ownership distinct from requirement and document ownership. |
| `DEC-PROFILE-BASELINE-001` | Keeps profile-specific obligations scoped rather than promoted to the global baseline. |

### 9.2 Related ADRs

| ADR | Relevance |
| --- | --- |
| `ADR-006` | Preserves first-class component boundaries that requirements can target. |
| `ADR-008` | Preserves independent release-channel requirement scope. |
| `ADR-013` | Separates global requirements from profile-specific implementation. |
| `ADR-015` | Provides stable development-workspace requirement families. |
| `ADR-016` | Keeps generated documentation and AI contexts non-authoritative. |
| `ADR-023` | Keeps overlay requirements explicit. |
| `ADR-024` | Preserves logical requirement meaning across physical deployment forms. |
| `ADR-026` | Blocks active authority that depends on a missing decision. |

### 9.3 Prohibited assumptions

The following assumptions are prohibited:

- a bullet becomes a requirement because it sounds mandatory;
- a heading number is a requirement identifier;
- a test name is a requirement identifier;
- a ticket number can replace a canonical requirement identifier;
- document order defines requirement priority;
- a lower number is more important;
- identifiers can be renumbered to remove gaps;
- a requirement identifier changes when a file moves;
- a requirement identifier changes when a section moves;
- one requirement can contain several independent obligations because they share a topic;
- similar wording proves duplicate authority;
- duplicate requirements can remain active indefinitely;
- one duplicate can be selected by file read order;
- scope defaults to global when omitted;
- repeated profile adoption converts a profile requirement into a global one;
- an implementation owner is always the requirement owner;
- a document author is the canonical owner;
- a recipe creates normative authority;
- a proposed decision can support an active requirement temporarily;
- a manually copied statement is equivalent to a generated projection;
- changing strength is an editorial correction;
- a materially changed obligation can keep its identifier for convenience;
- a split can reuse the original identifier for one child without impact analysis;
- a merge can reuse one source identifier and discard the others silently;
- retired identifiers can be recycled;
- an exception changes the requirement itself;
- a passing test proves every version of a requirement;
- a conformance claim can omit requirement versions;
- a generated row number can become a canonical alias;
- an AI context can reinterpret missing scope or authority;
- historical requirement versions can be deleted after migration.

## 10. Validation Criteria

This document conforms when all of the following checks pass:

1. metadata status is `active`;
2. the registered path is `09-conformance/01-requirement-identification.md`;
3. the document class is `normative_markdown`;
4. all canonical references resolve;
5. all listed decisions are accepted;
6. all requirements match the requirements registry;
7. all locks resolve and pass;
8. every active normative obligation has one requirement identifier;
9. every identifier matches the canonical grammar;
10. every domain path is registered;
11. every allocation number is unique within its domain path;
12. every allocated identifier remains permanently reserved;
13. every active identifier resolves to one active requirement record;
14. every requirement has a version and lifecycle status;
15. every active requirement has one atomic statement;
16. every active requirement has one canonical strength;
17. every active requirement has an explicit scope;
18. every scoped object resolves;
19. no profile-specific obligation is represented as global;
20. every active requirement has a canonical owner;
21. every active requirement has an accepted source decision;
22. every canonical reference resolves to an active object;
23. every active requirement has validation or a complete manual control;
24. every linked lock exists;
25. requirement-to-test and requirement-to-evidence coverage is computable;
26. requirement-to-profile, component, artifact, and toolchain applicability is computable;
27. every normative document metadata set matches its generated requirement block;
28. rendered strengths and statements exactly match canonical records;
29. no independent normative statement exists outside generated blocks;
30. a document move preserves requirement identifiers;
31. a non-semantic edit increments version and preserves history;
32. a material change creates replacement identifiers;
33. split lineage covers every resulting requirement;
34. merge lineage covers every source requirement;
35. duplicate reconciliation preserves every dependent relationship;
36. superseded and retired requirements remain resolvable;
37. retired identifiers are not reused;
38. exceptions reference exact requirement identifiers and versions;
39. conformance claims identify exact requirement versions and scope;
40. generated projections preserve canonical identifiers;
41. invalid aliases carry no canonical authority;
42. collision tests freeze activation and preserve history;
43. orphaned requirements and orphaned references are detected;
44. direct and transitive impact analysis is complete;
45. requirement-to-test-to-evidence traceability is complete;
46. active content is English;
47. placeholder and open-authority markers are absent.

The validator reports focused failures, including:

```text
requirement_identifier_missing
requirement_identifier_grammar_invalid
requirement_namespace_unregistered
requirement_identifier_collision
requirement_identifier_reused
requirement_active_version_ambiguous
requirement_statement_missing
requirement_statement_not_atomic
requirement_strength_missing
requirement_scope_missing
requirement_scope_object_missing
requirement_profile_rule_promoted_global
requirement_owner_missing
requirement_source_decision_missing
requirement_source_decision_inactive
requirement_canonical_reference_missing
requirement_validation_missing
requirement_manual_control_incomplete
requirement_lock_missing
requirement_traceability_incomplete
requirement_document_projection_mismatch
requirement_manual_normative_prose
requirement_material_change_reused_id
requirement_split_lineage_incomplete
requirement_merge_lineage_incomplete
requirement_duplicate_active
requirement_supersession_incomplete
requirement_retired_id_reused
requirement_exception_version_mismatch
requirement_claim_version_missing
requirement_generated_alias_authoritative
requirement_historical_version_missing
requirement_orphaned
```

## 11. Non-Normative Examples

### 11.1 Stable identifier after a document move

`REQ-DEV-UV-001` appears first in one development document and later moves to a dedicated toolchain document.

The requirement identifier remains unchanged because the obligation remains unchanged. The documentation registry, dependencies, and generated projections change.

### 11.2 New requirement inserted into an existing family

The active family contains:

```text
REQ-OPS-HEALTH-001
REQ-OPS-HEALTH-002
REQ-OPS-HEALTH-003
```

A new obligation receives the next unused allocation in that namespace. Existing requirements are not renumbered to match a preferred reading order.

### 11.3 Atomic split

One historical statement combined per-workspace environment isolation and per-workspace service-state isolation.

The change allocates two new identifiers, links both to the old identifier, migrates tests and documents, and supersedes the combined statement after coverage validation.

### 11.4 Material strength change

A recommendation becomes a mandatory compatibility condition.

The authority and compliance consequence change materially. The change receives an accepted decision and a new requirement identifier rather than silently changing historical meaning.

### 11.5 Non-semantic clarification

A requirement statement is revised to replace an ambiguous pronoun with the exact component name.

Review confirms that owner, subject, action, strength, scope, and compliance result are unchanged. The same identifier receives a new version, and projections are regenerated.

### 11.6 Duplicate discovery

Two security documents reference different identifiers with the same owner, source, scope, strength, action, and result.

Impact analysis selects one canonical obligation, migrates every dependent reference, preserves historical lineage, and makes the duplicate inactive.

### 11.7 Scope separation

The global baseline requires workspace isolation.

A build-farm profile also requires clean disposable workers.

These remain separate requirements because the second obligation applies only to the build-farm profile and has an independently testable result.

### 11.8 Generated document block

A normative document metadata block selects three requirement identifiers.

Its generated requirements section displays exactly those three canonical statements. The explanatory sections discuss implementation context without copying or modifying the normative sentences.

### 11.9 Exception

One constrained test environment receives a time-bounded exception from a specific requirement version.

The exception identifies the environment, expiry, compensating control, test, and evidence. The requirement remains active and unchanged for every other scope.

### 11.10 Conformance claim

A sovereign node claim lists the exact active requirement versions applicable to its profile and overlays.

Each result links to a test or manual control, evidence, and any approved exception. A document revision alone is not used as the evaluated requirement set.
