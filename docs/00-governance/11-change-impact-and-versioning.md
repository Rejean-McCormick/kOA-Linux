<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-GOV-011",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "governance",
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
    "contracts/ai-navigation.contract.json",
    "schemas/impact-report.schema.json"
  ],
  "decision_ids": [
    "DEC-DOC-002",
    "DEC-DOC-004",
    "DEC-DOC-005"
  ],
  "requirement_ids": [
    "REQ-CHG-001",
    "REQ-CHG-002",
    "REQ-CHG-003",
    "REQ-CHG-004",
    "REQ-CHG-005",
    "REQ-CHG-006",
    "REQ-CHG-007",
    "REQ-CHG-008",
    "REQ-CHG-009",
    "REQ-CHG-010",
    "REQ-CHG-011",
    "REQ-CHG-012",
    "REQ-CHG-013",
    "REQ-CHG-014",
    "REQ-CHG-015",
    "REQ-CHG-016",
    "REQ-CHG-017",
    "REQ-CHG-018",
    "REQ-CHG-019",
    "REQ-CHG-020",
    "REQ-CHG-021",
    "REQ-CHG-022",
    "REQ-CHG-023",
    "REQ-CHG-024",
    "REQ-CHG-025",
    "REQ-CHG-026",
    "REQ-CHG-027",
    "REQ-CHG-028",
    "REQ-CHG-029",
    "REQ-CHG-030",
    "REQ-CHG-031",
    "REQ-CHG-032",
    "REQ-CHG-033",
    "REQ-CHG-034",
    "REQ-CHG-035",
    "REQ-CHG-036"
  ],
  "lock_ids": [
    "LOCK-DOC-002",
    "LOCK-DOC-004",
    "LOCK-DOC-005",
    "LOCK-DOC-006",
    "LOCK-DOC-007",
    "LOCK-DOC-008",
    "LOCK-DOC-009",
    "LOCK-DOC-010",
    "LOCK-DOC-011",
    "LOCK-DOC-012",
    "LOCK-DOC-013",
    "LOCK-DOC-015",
    "LOCK-DOC-016",
    "LOCK-DOC-017",
    "LOCK-DOC-018",
    "LOCK-DOC-019",
    "LOCK-DOC-020"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-004",
    "DOC-GOV-009",
    "DOC-GOV-010",
    "DOC-GOV-013"
  ],
  "tags": [
    "change-control",
    "impact-analysis",
    "semantic-versioning",
    "interfile-alignment",
    "activation",
    "rollback"
  ]
}
KOA:DOC-META:END -->

# Change Impact and Versioning

## 1. Purpose

This document defines how changes to kOA documentation and canonical contracts are classified, analyzed, versioned, reviewed, activated, and reversed.

Its purpose is to prevent a local edit from creating hidden inconsistencies elsewhere in the documentation system.

The process treats every semantic change as a graph operation. A changed decision, registry value, requirement, profile rule, component boundary, artifact contract, lock, or document may affect direct and transitive dependents.

The change process therefore produces an explicit impact report before activation.

This document also defines semantic change classes, registry and document versioning, impact-analysis inputs and outputs, required dispositions, canonical path and identifier changes, lock mutation, generated-content regeneration, documentation-release activation, rollback, and forward repair.

---

## 2. Scope

This contract applies to changes involving:

- owner decisions;
- authority order;
- canonical registries;
- JSON Schemas;
- terminology;
- requirements;
- Interfile Alignment Locks;
- profiles and overlays;
- component contracts;
- artifact contracts;
- toolchain contracts;
- ADRs;
- Markdown documents;
- recipes explicitly adopted by profiles;
- tests and evidence;
- generated indexes and matrices;
- generated AI context packages;
- canonical paths and identifiers;
- documentation tooling that can alter generated or validated output.

Purely local notes, scratch files, and untracked drafts remain outside active authority. They enter this process when registered or referenced by an active object.

---

## 3. Canonical References

The canonical references for change impact and versioning are:

`text
generated/authority-manifest.json
generated/decision-index.json
generated/document-index.json
generated/requirements-index.json
generated/assertion-index.json
generated/decision-index.json
generated/traceability.json
generated/exception-index.json
contracts/ai-navigation.contract.json
schemas/impact-report.schema.json
generated/impact/
generated/manifests/
`

| Concern | Canonical owner |
| --- | --- |
| Accepted reason for a semantic change | `decisions.registry.json` |
| active paths, versions, and statuses | `authority.registry.json` |
| Document versions, paths, and dependencies | `documentation.registry.json` |
| Requirement versions and statements | `requirements.registry.json` |
| Lock versions and mutation policies | `locks.registry.json` |
| ADR rationale, when required | `10-adrs/README.md` and the applicable active ADR |
| Cross-object relationships | `traceability.registry.json` |
| Approved deviations | `exceptions.registry.json` |
| Context-package definitions | `ai-context.registry.json` |
| Impact-report structure | `impact-report.schema.json` |

The impact report is generated. It records analysis and dispositions but does not independently define system behavior.

---

## 4. Model and Responsibilities

### 4.1 Change object

Every controlled change has a stable change identity:

`text
CHG-<YEAR>-<SEQUENCE>
`

Example:

`text
CHG-2026-0042
`

A change object records its title, accepted decisions, semantic class, state, requester, and canonical targets.

### 4.2 Change states

Controlled changes use these states:

`text
draft
analyzing
blocked
approved
implementing
validating
ready_for_activation
active
rolled_back
superseded
abandoned
`

| State | Meaning |
| --- | --- |
| `draft` | Change exists but has no complete impact analysis |
| `analyzing` | Canonical targets and dependents are being resolved |
| `blocked` | Required decision, review, evidence, or validation is missing |
| `approved` | Change class and impact scope are accepted |
| `implementing` | Canonical and dependent objects are being modified |
| `validating` | Full required validation is running |
| `ready_for_activation` | All checks pass; authority manifest has not switched |
| `active` | New documentation release is authoritative |
| `rolled_back` | Previous authority manifest was restored |
| `superseded` | A later change replaces this change |
| `abandoned` | Change closed without activation |

### 4.3 Semantic change classes

#### Patch

A patch changes no architectural meaning.

Examples include spelling, grammar, formatting, navigational-link repair, generated-content repair without canonical-source change, and clarification that does not alter scope, behavior, or interpretation.

A patch does not change canonical values, requirements, requirement strength, profile membership, component ownership, defaults, state transitions, lock assertions, or authority order.

#### Minor

A minor change adds backward-compatible information or capability without weakening active constraints.

Examples include a new optional profile capability, backward-compatible field, recipe, explanatory document, non-breaking artifact field, test for an existing requirement, generated view, or optional integration classification.

A minor change does not invalidate previously conformant active objects.

#### Major

A major change alters meaning, compatibility, ownership, scope, or authority.

Examples include requirement changes, global/profile scope movement, component-boundary changes, canonical-owner changes, identifier-semantic changes, canonical-path changes, enum removal or rename, incompatible artifact contracts, state-machine changes, lock changes, authority-order changes, decision outcome changes, AI-boundary changes, release-channel changes, or weakened validation gates.

When classification is ambiguous, the larger class applies.

### 4.4 Versioned objects

Versioned objects include registries, schemas, profiles, component contracts, artifact contracts, toolchain contracts, requirements, locks, ADR metadata, documentation releases, and generated AI-context formats.

Each versioned object records semantic version, status, modification date, predecessor version where applicable, and content version.

The version describes semantic compatibility, not the number of edits.

### 4.5 Documentation release

A documentation release is an atomic set containing:

- the authority manifest;
- exact canonical registry versions;
- exact schema versions;
- active normative documents;
- generated projections;
- generated AI context packages;
- validation results;
- evidence references;
- activation manifest.

Recommended identity:

`text
KOA-DOC-RELEASE-<major>.<minor>.<patch>
`

### 4.6 Impact graph


Common edges include `owns`, `references`, `depends_on`, `implements`, `constrains`, `validated_by`, `evidenced_by`, `generated_from`, `included_in`, `supersedes`, `adopts`, `inherits`, `exempts`, and `maps_from`.

Impact resolution traverses outgoing dependency edges from every changed canonical node.

### 4.7 Responsibilities

- **Product owner:** decisions determining product meaning, capability, scope, and tradeoffs.
- **Architecture owner:** system boundaries, profile structure, canonical ownership, locks, and compatibility classification.
- **Documentation maintainer:** registries, documents, generators, metadata, and documentation-release manifests.
- **Component owner:** changes to component responsibilities, data ownership, interfaces, states, and failure behavior.
- **Validation owner:** tests and confirmation that validation reflects changed requirements and locks.
- **AI agent:** scoped analysis and edits under active authority; reports impact, blockers, and results; does not approve its own assumptions.

---

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-CHG-001,REQ-CHG-002,REQ-CHG-003,REQ-CHG-004,REQ-CHG-005,REQ-CHG-006,REQ-CHG-007,REQ-CHG-008,REQ-CHG-009,REQ-CHG-010,REQ-CHG-011,REQ-CHG-012,REQ-CHG-013,REQ-CHG-014,REQ-CHG-015,REQ-CHG-016,REQ-CHG-017,REQ-CHG-018,REQ-CHG-019,REQ-CHG-020,REQ-CHG-021,REQ-CHG-022,REQ-CHG-023,REQ-CHG-024,REQ-CHG-025,REQ-CHG-026,REQ-CHG-027,REQ-CHG-028,REQ-CHG-029,REQ-CHG-030,REQ-CHG-031,REQ-CHG-032,REQ-CHG-033,REQ-CHG-034,REQ-CHG-035,REQ-CHG-036 -->

- **REQ-CHG-001 — SHALL:** Every semantic change have a stable `CHG-ID`.
- **REQ-CHG-002 — SHALL:** Every semantic change reference at least one accepted owner decision.
- **REQ-CHG-003 — SHALL:** Every controlled change be classified as `patch`, `minor`, or `major`.
- **REQ-CHG-004 — SHALL:** Ambiguous change classification resolve to the larger semantic class.
- **REQ-CHG-005 — SHALL:** Every semantic change identify its canonical target objects before dependent prose is modified.
- **REQ-CHG-006 — SHALL:** Every semantic change produce a machine-readable direct and transitive impact report.
- **REQ-CHG-007 — SHALL:** Impact analysis traverse canonical references, semantic document dependencies, traceability links, lock relationships, generated-content sources, and AI-context inclusion relationships.
- **REQ-CHG-008 — SHALL:** Every object identified by an impact report receive one explicit disposition.
- **REQ-CHG-009 — SHALL NOT:** A change activate while an affected object has no disposition.
- **REQ-CHG-010 — SHALL:** Allowed impact dispositions be `updated`, `reviewed_no_change`, `regenerated`, `deprecated`, `superseded`, `exception_applied`, or `blocked`.
- **REQ-CHG-011 — SHALL:** A `reviewed_no_change` disposition include reviewer identity and rationale.
- **REQ-CHG-012 — SHALL:** A `blocked` disposition identify the missing decision, contract, review, test, evidence, or tool.
- **REQ-CHG-013 — SHALL:** Canonical registries be modified before explanatory Markdown for semantic changes.
- **REQ-CHG-014 — SHALL:** Generated content be regenerated after all canonical source changes are complete.
- **REQ-CHG-015 — SHALL:** Tests and traceability be updated before activation.
- **REQ-CHG-016 — SHALL:** `authority.registry.json` be updated last.
- **REQ-CHG-017 — SHALL NOT:** A partial set of changed registries or generated files become active.
- **REQ-CHG-018 — SHALL:** Documentation releases activate atomically through an authority manifest.
- **REQ-CHG-019 — SHALL:** Every versioned canonical object use semantic versioning.
- **REQ-CHG-020 — SHALL:** A patch preserve architectural meaning and compatibility.
- **REQ-CHG-021 — SHALL:** A minor version remain backward-compatible with active consumers unless an explicit compatibility adapter is part of the same release.
- **REQ-CHG-022 — SHALL:** A major version identify all incompatible changes and required migrations.
- **REQ-CHG-023 — SHALL:** A canonical path change be classified as major.
- **REQ-CHG-024 — SHALL:** A canonical path change declare the old path, new path, activation release, redirect mechanism, and redirect expiration policy.
- **REQ-CHG-025 — SHALL NOT:** A retired identifier be reused.
- **REQ-CHG-026 — SHALL:** A replacement identifier declare `supersedes`, and the retired identifier declare `replaced_by`.
- **REQ-CHG-027 — SHALL:** A lock mutation follow the lock’s declared mutation policy.
- **REQ-CHG-028 — SHALL:** A lock weakening, scope change, assertion change, or retirement be classified as major.
- **REQ-CHG-029 — SHALL:** A change include an ADR only when it introduces or changes a non-obvious, workaround-based, or regression-prone implementation choice that cannot be adequately protected by the canonical current-system description alone.
- **REQ-CHG-030 — SHALL:** Validation run from a clean repository state against the complete proposed documentation release.
- **REQ-CHG-031 — SHALL NOT:** A failed, skipped, unavailable, or incomplete required validation be reported as passed.
- **REQ-CHG-032 — SHALL:** Activation record exact paths, versions, statuses, validation results, and evidence references.
- **REQ-CHG-033 — SHALL:** Rollback restore a complete previously valid authority manifest.
- **REQ-CHG-034 — SHALL NOT:** Rollback reactivate an object that is incompatible with irreversible data or artifact migrations.
- **REQ-CHG-035 — SHALL:** An irreversible migration define forward-repair behavior before activation.
- **REQ-CHG-036 — SHALL:** AI-generated change summaries list decisions, canonical targets, affected documents, requirements, locks, exceptions, tests, and validation status.

<!-- GENERATED:REQUIREMENTS:END -->

---

## 6. Procedures or State Transitions

### 6.1 Standard semantic-change procedure

`text
accepted decision
 ↓
change object created
 ↓
semantic class selected
 ↓
canonical targets identified
 ↓
impact graph resolved
 ↓
impact report reviewed
 ↓
canonical sources modified
 ↓
dependent contracts modified
 ↓
normative and explanatory documents modified
 ↓
generated content rebuilt
 ↓
tests and evidence updated
 ↓
complete validation
 ↓
authority manifest updated
 ↓
atomic activation
`

### 6.2 Impact-analysis procedure

`compute_impact.py` receives change ID, changed canonical paths, changed JSON Pointers, changed object IDs, semantic class, and decision IDs.

It resolves:

1. direct canonical references;
2. document dependencies;
3. transitive document dependents;
4. requirement links;
5. lock links;
6. profile membership and inheritance;
7. component ownership;
8. artifact and toolchain dependencies;
9. ADR relationships;
10. test and evidence relationships;
11. generated projections;
12. generated AI contexts;
14. authority-manifest entries.

The output is written to:

`text
generated/impact/IMPACT-<date>-<change-id>.json
`

### 6.3 Impact-report structure

An impact report records schema, impact ID, change ID, semantic class, decision IDs, canonical targets, affected objects, relationship type, graph distance, dispositions, review evidence, unresolved objects, and activation eligibility.

### 6.4 Disposition rules

- `updated`: object changed semantically or structurally.
- `reviewed_no_change`: object reviewed and remains correct; includes reviewer, date, source version, and rationale.
- `regenerated`: fully derived object rebuilt from canonical sources.
- `deprecated`: temporarily available but scheduled for removal.
- `superseded`: replaced by a new object.
- `exception_applied`: approved exception temporarily permits divergence and references an active `EXC-ID`.
- `blocked`: activation cannot continue and the exact blocker is recorded.

### 6.5 Patch procedure

A patch uses reduced impact analysis only when automated checks prove that canonical meaning is unchanged.

Patch review covers modified files, links, metadata, generated content, language, and formatting. If interpretation changes, the change is reclassified.

### 6.6 Minor-change procedure

A minor change includes compatibility review, dependent-context review, generated-content regeneration, applicable tests, minor version increments for changed canonical objects, and a documentation-release minor increment when active behavior is extended.

### 6.7 Major-change procedure

A major change includes an accepted owner decision, a full transitive impact report, a migration plan, a compatibility statement, a rollback or forward-repair plan, full validation, major increments for incompatible canonical objects, and a major documentation-release increment when the authority contract changes incompatibly. Add a short ADR only when the change meets the criteria in `10-adrs/README.md`.

### 6.8 Lock-mutation procedure

A lock change requires an accepted decision, major classification, affected-assertion analysis, protected-object resolution, replacement assertions, requirement and test updates, full validation, and activation of the new lock version.

A lock is never edited merely to make an existing validation failure disappear.

### 6.9 Canonical path-change procedure

A path change records old path, new path, major classification, activation release, redirect mechanism, and minimum redirect lifetime.

All canonical references are migrated in the same release. The old path remains reserved.

### 6.10 Activation procedure

Activation occurs only when:

- no affected object lacks a disposition;
- no required disposition is `blocked`;
- schemas validate;
- references resolve;
- locks pass;
- graph checks pass;
- generated artifacts are current;
- tests pass;
- required evidence exists;
- authority versions match.

The final operation updates the authority manifest.

### 6.11 Rollback procedure

Rollback restores the previous authority index, active registry versions, generated projections, AI context packages, and documentation-release manifest.

Rollback does not reconstruct files individually.

### 6.12 Forward repair

Forward repair is used when rollback is unsafe because an irreversible migration has occurred.

The plan records the irreversible operation, affected versions, incompatibility, repaired target state, repair procedure, validation, and evidence.

---

## 7. Failure States and Safe Degradation

### 7.1 Incomplete impact report

When impact analysis cannot resolve all dependencies, the change becomes `blocked`, unresolved edges are listed, activation remains unavailable, and the previous release remains active.

### 7.2 Unknown canonical owner

When no exclusive owner can be identified, the change is blocked and an owner decision is required. No document becomes an informal owner.

### 7.3 Multiple canonical owners

When multiple active objects claim the same fact, the new change cannot activate, both claimants are reported, and previous valid authority remains active.

### 7.4 Stale generated content

When generated content does not match source versions, the release is invalid, regeneration is required, and manual correction is rejected.

### 7.5 Failed validation

When a required validation fails, activation stops. Successful checks remain evidence but do not create partial authority.

### 7.6 Unavailable validation tooling

Unavailable required validation results in `blocked`, not `pass`.

### 7.7 Incompatible rollback

When rollback would reactivate contracts incompatible with migrated state, rollback is blocked and forward repair is selected. Affected profiles and components use declared safe degradation where supported.

### 7.8 Authority-manifest mismatch

When active paths, versions, or statuses differ from the authority manifest, the release is inconsistent, conformance claims are invalid, and the last valid manifest remains authoritative.

---

## 8. Cross-Component Interactions

### 8.1 Decisions registry

The decision registry provides the authorized reason for semantic change. A change cannot convert an informal preference into active architecture.

### 8.2 Documentation registry

The documentation registry provides document path, version, status, semantic dependencies, canonical references, tags, and generated sections. These relationships drive impact.

### 8.3 Requirements registry

Requirement changes affect generated requirement blocks, linked locks, profile claims, component contracts, tests, evidence, and conformance results. A requirement-strength change is major.

### 8.4 Locks registry

A change touching a protected canonical reference automatically includes the lock and every object selected by the lock.

### 8.5 Traceability registry

Traceability expands impact from architecture into validation:

`text
decision
 → requirement
 → profile
 → component
 → test
 → evidence
 → conformance claim
`

### 8.6 AI context registry

A changed object affects every generated context package that includes the object, its scope, profile, component, requirements, locks, or prohibited assumptions.

### 8.7 Authority registry

The authority registry does not initiate changes. It activates the validated result.


---

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Missing change class

An AI agent does not infer the smallest convenient class. Ambiguity resolves to the larger class.

### 9.2 Missing owner decision

A semantic change without an accepted decision remains blocked. The agent may draft a proposal, but it has no authority until accepted.

### 9.3 Missing dependency

Absence from an impact report does not prove absence of impact when the graph is incomplete. Graph incompleteness is a validation failure.

### 9.4 Current implementation

Implementation prevalence does not determine compatibility class. A recipe used everywhere can remain non-normative.

### 9.5 Version numbers

A version number cannot be incremented merely to avoid required migration. Semantic meaning determines the class.

### 9.6 Manual generated-file edits

A manual change to generated output is not a valid patch. The source or generator changes, then output is regenerated.

### 9.7 Validation claims

An AI agent cannot report that all checks passed unless every required check executed successfully against the complete proposed release.

### 9.8 Review without change

`reviewed_no_change` is not a default. It requires explicit review and rationale.

### 9.9 Silent lock weakening

A lock cannot be weakened to accommodate an implementation that violates current architecture. The decision changes first, or the implementation changes.

---

## 10. Validation Criteria

This document is conformant when these checks pass:

### 10.1 Metadata

- `DOC-GOV-011` exists in `documentation.registry.json`.
- The registered path matches this file.
- The document class is `normative_markdown`.
- All canonical references and dependencies resolve.
- The generated metadata matches its registered source.

### 10.2 Requirements

- Every listed `REQ-CHG-*` exists.
- Every requirement references an accepted decision.
- Every requirement has scope, owner, validation, and lock relationships.
- No normative keyword exists outside the generated requirement block.

### 10.3 Impact-report schema

- Every impact report validates against `impact-report.schema.json`.
- Every changed canonical target appears.
- Every affected object has a valid disposition.
- Every `reviewed_no_change` disposition has evidence.
- Every `blocked` disposition identifies a blocker.
- No unresolved affected object remains at activation.

### 10.4 Graph integrity

- All graph nodes resolve.
- All typed edges are valid.
- Semantic document dependencies are acyclic.
- Generated-from relationships resolve to active sources.
- Traceability is complete for active claims.

### 10.5 Version integrity

- Every changed versioned object has a valid semantic-version transition.
- Major incompatibilities use major increments.
- Retired identifiers are not reused.
- Replacement objects contain bidirectional supersession links.
- Canonical path changes include redirect records.

### 10.6 Activation integrity

- The proposed release is complete.
- All required validation executed successfully.
- All active versions match the authority manifest.
- Generated AI contexts match source versions.
- The authority index was updated after all other artifacts.
- The activation manifest identifies the previous release.

### 10.7 Rollback integrity

- The previous authority manifest remains available.
- Rollback compatibility is explicitly evaluated.
- Irreversible migrations have forward-repair plans.
- Rollback does not create mixed-version authority.

---

## 11. Non-Normative Examples

### 11.1 Patch example

Correcting a spelling error is a patch when no identifier, field, interpretation, scope, or semantic meaning changes.

### 11.2 Minor example

Adding a new optional generated catalog is minor when it derives from existing canonical data and changes no authority.

### 11.3 Major example

Moving `rootless Podman required` from `sovereign_linux_node` to global scope is major because profile scope and implementation requirements change.

### 11.4 Direct and transitive impact

A change to:

`text
contracts/toolchains/python-uv.toolchain.json#/environment_isolation
`

may directly affect `REQ-DEV-UV-001`, `LOCK-DEV-001`, `DOC-DEV-003`, and the developer profile. It may transitively affect development conformance, generated AI context, workspace recipes, evidence, and release gates.

### 11.5 Valid reviewed-no-change disposition

`json
{
 "object_type": "document",
 "object_id": "DOC-OPS-004",
 "disposition": "reviewed_no_change",
 "review": {
 "reviewer": "operations-architecture",
 "reviewed_on": "2026-08-03",
 "source_version": "2.1.0",
 "rationale": "The document resolves limits dynamically from the profile registry."
 }
}
`

### 11.6 Invalid reviewed-no-change disposition

A disposition containing only an object ID and `reviewed_no_change` is invalid because reviewer, date, source version, and rationale are missing.

### 11.7 Valid blocked result

`json
{
 "change_id": "CHG-2026-0042",
 "status": "blocked",
 "blockers": [
 {
 "type": "missing_test_evidence",
 "requirement_id": "REQ-DEV-UV-001",
 "test_id": "TEST-DEV-UV-001"
 }
 ]
}
`

### 11.8 Invalid activation

Updating Markdown and switching the authority registry before generated contexts are rebuilt creates mixed-version authority and fails this contract.

### 11.9 Valid authority activation sequence

`text
canonical registries
→ schemas
→ requirements and locks
→ documents
→ tests and evidence
→ generated projections
→ AI contexts
→ complete validation
→ authority registry
`
