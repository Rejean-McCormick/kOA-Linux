<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONF-011",
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
    "contracts/artifact-classes.contract.json",
    "generated/artifact-catalog.json",
    "contracts/release-channels.contract.json"
  ],
  "decision_ids": [
    "DEC-DOC-001",
    "DEC-DOC-002",
    "DEC-DOC-003",
    "DEC-COMP-001",
    "DEC-PROFILE-BASELINE-001"
  ],
  "requirement_ids": [
    "REQ-CONF-DEC-001",
    "REQ-CONF-DEC-002",
    "REQ-CONF-DEC-003",
    "REQ-CONF-DEC-004",
    "REQ-CONF-DEC-005",
    "REQ-CONF-DEC-006",
    "REQ-CONF-DEC-007",
    "REQ-CONF-DEC-008",
    "REQ-CONF-DEC-009",
    "REQ-CONF-DEC-010",
    "REQ-CONF-DEC-011",
    "REQ-CONF-DEC-012",
    "REQ-CONF-DEC-013",
    "REQ-CONF-DEC-014",
    "REQ-CONF-DEC-015",
    "REQ-CONF-DEC-016",
    "REQ-CONF-DEC-017",
    "REQ-CONF-DEC-018",
    "REQ-CONF-DEC-019",
    "REQ-CONF-DEC-020",
    "REQ-CONF-DEC-021",
    "REQ-CONF-DEC-022",
    "REQ-CONF-DEC-023",
    "REQ-CONF-DEC-024",
    "REQ-CONF-DEC-025",
    "REQ-CONF-DEC-027",
    "REQ-CONF-DEC-028",
    "REQ-CONF-DEC-029",
    "REQ-CONF-DEC-030",
    "REQ-CONF-DEC-031",
    "REQ-CONF-DEC-032"
  ],
  "lock_ids": [
    "LOCK-DOC-001",
    "LOCK-DOC-002",
    "LOCK-DOC-003",
    "LOCK-DOC-004",
    "LOCK-DOC-011",
    "LOCK-DOC-012",
    "LOCK-DOC-013",
    "LOCK-DOC-014",
    "LOCK-CONF-001",
    "LOCK-CONF-002",
    "LOCK-CONF-006",
    "LOCK-CONF-007",
    "LOCK-CONF-008",
    "LOCK-CONF-009",
    "LOCK-CONF-010"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-003",
    "DOC-GOV-004",
    "DOC-GOV-005",
    "DOC-GOV-013",
    "DOC-CONF-000",
    "DOC-CONF-001"
  ],
  "tags": [
    "conformance",
    "decision-closure",
    "owner-decisions",
    "authority-activation",
    "impact-analysis",
    "conflict-detection",
    "supersession",
    "adrs",
    "traceability",
    "validation-gate"
  ]
}
KOA:DOC-META:END -->

# Decision Closure Validation

## 1. Purpose

This document defines how kOA validates that architectural decisions are complete, accepted, applicable, non-conflicting, fully propagated, and eligible to support active authority.

A decision closes an implementation-affecting architectural matter only when the selected outcome can be interpreted and validated without guessing.

Decision closure prevents maintainers, generators, validators, AI agents, implementation code, recipes, and downstream documents from filling authority gaps through convention or inference.

The closure model distinguishes:

- a question or candidate issue;
- a proposed owner decision;
- an accepted owner decision;
- an ADR that records architectural rationale;
- a validated authority transition;
- an activated registry or documentation release;
- an exception to an active requirement;

These are different objects and transitions.

The primary rule is:

```text
accepted owner decision
    + complete impact disposition
    + passing authority-graph validation
    = eligible for activation
```

Acceptance alone does not activate authority.

An ADR alone does not activate authority.

A merged implementation alone does not activate authority.

Repeated prose, operational convention, deployment prevalence, or a generated context does not activate authority.

When an active behavior depends on a decision that cannot be verified, the affected authority remains blocked. Existing unaffected authority can remain readable and operational according to its own contracts, but no broader outcome is selected.

The canonical decision records belong to:

```text
generated/decision-index.json
```

This document owns the conformance interpretation and validation procedure for decision closure. It does not become a second owner of decision outcomes.

## 2. Scope

This document applies globally to decisions that affect:

- authority order;
- canonical ownership;
- normative defaults;
- global invariants;
- profile membership or composition;
- profile-overlay behavior;
- component identity and responsibility;
- component data ownership;
- command, query, and event boundaries;
- security and privilege;
- identity and trust;
- governance policy;
- cultural rights and consent;
- AI boundaries;
- resource authority;
- release channels;
- artifact classes and activation;
- migration and compatibility;
- failure and degradation;
- backup, restore, and recovery;
- development toolchains;
- conformance and validation.

It validates decision relationships used by:

- authority registries;
- specialized canonical registries;
- JSON Schemas;
- normative Markdown;
- explanatory Markdown where it declares dependencies;
- requirements;
- alignment locks;
- profile contracts;
- component contracts;
- artifact contracts;
- toolchain contracts;
- ADRs;
- exceptions;
- traceability;
- tests;
- evidence;
- releases;
- migration records;
- generated projections;
- AI context packages;
- conformance claims.

It applies during:

```text
decision proposal
decision review
decision acceptance
change implementation
impact propagation
full-graph validation
authority activation
deprecation
supersession
migration
retirement
historical interpretation
```

It does not require a new decision for a demonstrably non-semantic editorial correction.

It does require a decision when a change affects authority, meaning, scope, ownership, normative force, default behavior, component boundary, data ownership, profile applicability, artifact behavior, compatibility, migration, failure behavior, validation behavior, release behavior, or identifier semantics.

## 3. Canonical References

| Canonical reference | Responsibility |
| --- | --- |
| `generated/decision-index.json` | Decision identifiers, versions, states, owners, scopes, selected outcomes, rejected alternatives, affected domains, references, impact, succession, and effective dates. |
| `generated/authority-manifest.json` | Authority order, active registry versions, activation gates, and complete-release validation. |
| `generated/document-index.json` | Document identity, class, scope, dependencies, decision projections, and active-path registration. |
| `contracts/terminology.contract.json` | Canonical meanings of owner decision, acceptance, activation, impact, semantic change, conflict, supersession, and blocked result. |
| `generated/requirements-index.json` | Active obligations and their accepted source decisions. |
| `generated/assertion-index.json` | Cross-file invariants and the decisions authorizing them. |
| `generated/decision-index.json` | ADR identity, lifecycle, owner-decision linkage, scope, canonical references, and succession. |
| `generated/traceability.json` | Decision relationships to requirements, locks, documents, profiles, components, artifacts, toolchains, tests, evidence, exceptions, releases, and migration records. |
| `generated/exception-index.json` | Bounded deviations from active requirements and their accepted exception authority. |
| `generated/test-catalog.json` | Decision-record, scope, conflict, supersession, impact, projection, activation-order, and negative-path tests. |
| `generated/evidence-catalog.json` | Decision review, approval, impact, validation, activation, migration, and conformance evidence. |
| `generated/profile-catalog.json` | Active profile and overlay identifiers used by decision scope and impact. |
| `generated/component-catalog.json` | Active component identifiers, responsibilities, ownership, and boundaries affected by decisions. |
| `contracts/artifact-classes.contract.json` | Active artifact classes, lifecycle behavior, release channels, compatibility, and activation effects affected by decisions. |
| `generated/artifact-catalog.json` | Active artifact schemas and contracts affected by decision changes. |
| `contracts/release-channels.contract.json` | Independent release-channel identities and publication authority. |

Decision closure is validated against the complete active graph rather than by reading only a decision record.

## 4. Model and Responsibilities

### 4.1 Owner decision

An owner decision is the canonical record of one selected architectural outcome.

It identifies:

- the matter being decided;
- the accountable owner;
- the exact scope;
- the selected outcome;
- the authority effect;
- affected canonical facts;
- semantic change class;
- direct and transitive impact obligations;
- validation;
- effective transition;
- historical relationships.

The decision record is concise and machine-resolvable.

Detailed rationale belongs to an ADR when the decision class requires one.

### 4.2 Decision identity

A decision identifier remains stable across:

- document moves;
- registry reformatting;
- ADR renaming;
- generated projection changes;
- implementation file moves;
- test reorganization;
- profile or component display reordering.

A decision version changes when interpretation-affecting fields change.

A material replacement receives a new decision identifier and records succession.

An allocated decision identifier is never reused for another outcome.

### 4.3 Decision states

The canonical state enum belongs to the decision registry.

The shared interpretation is:

| State | Authority effect |
| --- | --- |
| `proposed` | Reviewable candidate with no active authority. |
| `accepted` | Eligible to support active authority after complete validation and activation. |
| `rejected` | Preserved alternative with no active authority. |
| `deprecated` | Existing compatibility use can continue within a declared interval, but new adoption is blocked. |
| `superseded` | Replaced by one or more accepted decisions and retained for history. |
| `archived` | Historical record with no current authority. |

Only `accepted` decisions can support new active authority.

An accepted decision can still fail activation when its dependent graph is incomplete or invalid.

### 4.4 Acceptance and activation

Acceptance records that the accountable owner selected the outcome.

Activation records that the accepted outcome and every affected authoritative object passed the applicable validation pipeline and became part of the active authority release.

The sequence is:

```text
proposed
reviewed
accepted
implemented in canonical objects
validated as a complete graph
activated through authority registry
```

The repository does not publish partially applied authority.

A decision can be accepted while the implementation change remains inactive.

### 4.5 Accountable owner

Every decision has one accountable owner role.

The owner is responsible for:

- defining the question;
- selecting the outcome;
- defining scope;
- identifying authority effects;
- classifying semantic change;
- resolving conflict;
- approving impact dispositions;
- approving supersession;
- ensuring required validation and evidence.

Contributors, reviewers, implementers, AI agents, and validators can assist.

They do not become the accountable owner by drafting or implementing the change.

Multi-party review can be required without removing the single accountable owner field.

### 4.6 Decision scope

Scope uses the same strict classes as requirements and canonical objects:

| Scope kind | Interpretation |
| --- | --- |
| `global` | Applies to every conforming composition unless an active bounded exception affects one instance. |
| `profile` | Applies only to named profiles. |
| `profile_overlay` | Applies only when named overlays are active. |
| `component` | Applies only to named first-class components or component contracts. |
| `artifact` | Applies only to named artifact classes or artifact contracts. |
| `toolchain` | Applies only to named toolchain contracts. |
| `migration` | Applies only to a declared migration or cutover disposition and does not become current runtime authority. |

Scope overlap is computed from scope kind, identifiers, effective dates, and compatibility intervals.

A global decision overlaps every narrower decision in the affected domain unless the global outcome explicitly permits scoped specialization.

A profile and profile-overlay decision overlap only for compositions containing both.

A component decision does not become global because several profiles include the component.

### 4.7 Selected outcome

The selected outcome is precise enough to answer every affected architectural question.

Depending on the decision, it can define:

- canonical owner;
- included and excluded scope;
- component responsibility;
- data owner;
- interface boundary;
- baseline default;
- profile specialization;
- artifact class;
- release channel;
- activation behavior;
- compatibility;
- migration;
- rollback or forward repair;
- degradation;
- security and privilege;
- validation;
- retirement.

A selected outcome can reference canonical records rather than copying all values.

A reference is insufficient when it does not identify which value or behavior is selected.

### 4.8 Rejected alternatives

Rejected alternatives preserve decision boundaries.

They are recorded when omission could make a later reader believe that another option remains valid.

Useful rejected-alternative records identify:

- alternative;
- reason for rejection;
- affected scope;
- safety, compatibility, authority, or operational consequence;
- conditions under which reconsideration would require a new decision.

Rejected alternatives have no active authority.

They can appear in review and historical contexts but not as implementation choices.

### 4.9 Semantic change class

The decision registry defines the canonical semantic-change classification.

A typical interpretation is:

| Class | Meaning |
| --- | --- |
| `patch` | Clarifies or corrects without changing compatible authority or required behavior. |
| `minor` | Adds compatible capability, scope, artifact, profile option, or validation without breaking existing conforming behavior. |
| `major` | Changes authority, ownership, required behavior, compatibility, profile composition, security, data model, lifecycle, release behavior, or another incompatible semantic dimension. |

Classification controls:

- version changes;
- ADR requirement;
- migration;
- compatibility;
- release notes;
- test breadth;
- evidence;
- deprecation interval;
- supersession.

A change is not a patch because its textual diff is small.

### 4.10 Direct impact

Direct impact includes every object explicitly referenced or modified by the decision.

Examples include:

- registry entry;
- schema;
- requirement;
- lock;
- profile;
- component contract;
- artifact contract;
- toolchain contract;
- document;
- ADR;
- test;
- evidence expectation;
- exception;
- release set;
- migration unit.

The impact report identifies the relationship and required disposition for each object.

### 4.11 Transitive impact

Transitive impact follows the canonical relationship graph.

Examples include:

```text
decision
  → component ownership
  → component contract
  → profile membership
  → deployment topology
  → integration contract
  → health checks
  → tests
  → evidence
  → conformance claim
```

and:

```text
decision
  → artifact class
  → artifact schema
  → release channel
  → Release Set
  → activation procedure
  → rollback evidence
```

Validation continues until no required dependent remains without a disposition.

An unchanged dependent is still recorded as validated unchanged when the decision could reasonably affect it.

### 4.12 Impact disposition

Every affected object receives one explicit disposition:

| Disposition | Meaning |
| --- | --- |
| `changed` | The object is updated as part of the decision. |
| `validated_unchanged` | Analysis and tests prove that no change is required. |
| `superseded` | A replacement object becomes authoritative. |
| `retired` | The object leaves active authority and remains historical. |
| `migrated` | Existing state or references move through an explicit migration. |
| `regenerated` | A derived projection is rebuilt from canonical authority. |
| `not_applicable` | The relationship is examined and excluded with rationale. |

Silence is not a disposition.

### 4.13 Decision conflict

A decision conflict exists when two accepted decisions prescribe incompatible outcomes for overlapping scope and effective time.

Conflict dimensions include:

- canonical owner;
- data owner;
- required or prohibited capability;
- default;
- component boundary;
- profile membership;
- artifact class or channel;
- privilege;
- security control;
- AI boundary;
- failure behavior;
- compatibility;
- migration;
- activation;
- validation.

Different outcomes are not conflicts when their scopes do not overlap or when one decision explicitly defines a permitted specialization.

### 4.14 Conflict detection

Conflict validation compares:

- affected domains;
- scope kinds and identifiers;
- effective intervals;
- selected outcomes;
- canonical references;
- owner;
- authority effect;
- supersession;
- compatibility rules.

The result identifies the smallest affected scope.

The validator does not select a winner from:

- file order;
- modification time;
- identifier order;
- document detail;
- implementation prevalence;
- deployment count;
- majority of prose;
- generator preference.

### 4.15 Conflict resolution

Conflict resolution requires an accepted superseding decision.

The superseding decision identifies:

- every conflicting decision;
- exact overlapping scope;
- selected surviving outcome;
- scope transition;
- compatibility;
- migration;
- dependent changes;
- effective date;
- evidence.

Both prior decisions remain preserved.

Affected activation remains blocked until the complete superseding change passes validation.

### 4.16 Supersession

Supersession is explicit and bidirectional.

The replacing decision lists every decision it supersedes.

Each replaced decision lists its replacement.

Supersession validation checks:

- identifiers resolve;
- replacement is accepted;
- scopes are compatible with the stated transition;
- effective dates are ordered;
- changed semantics are described;
- dependent references are migrated;
- compatibility and migration are complete;
- historical interpretation remains possible.

Deprecation can precede supersession for a declared compatibility interval.

### 4.17 Relationship to requirements

A requirement is an atomic normative obligation.

A decision is the accepted owner outcome from which the obligation derives.

Decision closure verifies:

- the source decision is accepted;
- requirement scope fits decision scope;
- requirement owner is compatible;
- requirement statement does not add a new architectural result;
- requirement strength fits the selected outcome;
- requirement validation covers the intended behavior;
- supersession lineage remains aligned.

A requirement cannot repair an incomplete decision by embedding the missing outcome.

### 4.18 Relationship to locks

A lock protects an invariant across several objects.

Decision closure verifies:

- the lock references an accepted source decision;
- lock scope fits decision scope;
- assertions implement the selected outcome;
- mutation policy reflects the semantic change class;
- affected locks are changed or validated unchanged;
- failed lock assertions block activation.

A lock is not an alternate decision record.

### 4.19 Relationship to ADRs

The decision record owns the authoritative outcome.

The ADR owns:

- context;
- problem framing;
- considered alternatives;
- rationale;
- consequences;
- tradeoffs;
- migration implications;
- operational implications;
- follow-up triggers.

A major decision requires an accepted ADR.

Decision and ADR records reference each other and have compatible scope and lifecycle.

An accepted ADR linked only to a proposed or missing decision does not activate authority.

A decision can remain accepted after its ADR is superseded only when the decision registry explicitly records the surviving rationale relationship and validation permits it.

### 4.20 Relationship to exceptions

An exception is a bounded deviation from an active requirement.

It is not a substitute for decision closure.

Decision-closure validation confirms that:

- the exception mechanism has accepted authority;
- the exception references exact active requirements and versions;
- the baseline decision remains accepted;
- affected scope is bounded;
- compensating controls exist;
- expiry or closure is machine-readable;
- non-waivable locks remain intact.

A missing architectural choice requires a decision, not an exception.

### 4.21 Open-authority detection

Active authority cannot contain language or structured values that indicate an implementation-affecting choice remains open.

Detection applies to:

- lifecycle fields;
- selected outcome;
- scope;
- owner;
- defaults;
- failure behavior;
- compatibility;
- migration;
- requirement statements;
- lock assertions;
- profile claims;
- component contracts;
- artifact contracts;
- generated contexts.

The detector is syntax- and document-class-aware.

Historical evidence, test fixtures, migration quotations, and this explanatory document can describe the validation category without making the quoted source authoritative.

The active replacement or final disposition remains explicit.


Migration can preserve source lineage without preserving source authority.

Every migration unit that adapts, excludes, reconciles, or resolves conflicting source behavior identifies an accepted decision.

Final dispositions include:

- adopted;
- adapted;
- superseded;
- excluded;
- historical-only;
- merged through an accepted replacement.

A migration record cannot leave the active destination dependent on an undecided source choice.

### 4.23 Generated projections and AI contexts

Generated contexts select decisions by:

- active status;
- applicable scope;
- effective time;
- target profile;
- target component;
- artifact or toolchain relevance;
- requested task context.

Implementation contexts exclude proposed, rejected, deprecated for new adoption, superseded, archived, and migration-only outcomes.

Review contexts can include alternatives and history when clearly labeled.

Generated output preserves canonical decision identifiers and does not create independent authority.

### 4.24 Machine-readable validation result

A decision-closure result identifies:

- validation status;
- reason code;
- decision identifiers and versions;
- required owner;
- required scope;
- affected objects;
- conflict set;
- missing fields;
- invalid references;
- impact gaps;
- prohibited inference flag;
- remediation category;
- evidence references.

Common statuses include:

- `pass`;
- `fail`;
- `blocked`;
- `not_applicable`.

A blocked result differs from a failed implementation test.

It means the authority needed to determine or activate the expected behavior is absent or incomplete.

### 4.25 Authority activation gate

The authority registry activates a complete compatible set of registries and documents.

The gate verifies:

1. decision closure;
2. schema validity;
3. reference resolution;
4. canonical ownership;
5. requirement integrity;
6. lock assertions;
7. profile and component consistency;
8. artifact and toolchain consistency;
9. lifecycle and release compatibility;
10. traceability;
11. generated projections;
12. tests and evidence;
13. exception validity;
14. migration and archive disposition.

Decision acceptance occurs before this gate.

Authority activation occurs after it.

### 4.26 Clean-graph validation

Decision closure runs from a clean declared repository state.

The validator does not rely on:

- untracked generated files;
- stale local caches;
- prior passing results for changed dependencies;
- implementation state outside the declared source tree;
- hidden environment defaults;
- operator memory.

The validation report identifies the source-tree identity, tool versions, registry versions, selected profiles, and applicable scopes.

### 4.27 Safe blocked behavior

When decision closure cannot be established:

- new affected authority remains inactive;
- generated implementation contexts omit the invalid outcome;
- releases and conformance claims exclude or fail the affected scope;
- existing last-known-valid authority can remain readable;
- unaffected scopes can continue;
- a proposed decision and impact report can be drafted;
- no default is invented.

Blocked authority does not imply that the entire system must stop when the affected scope is isolated.

## 5. Applicable Normative Requirements

- **REQ-CONF-DEC-001 — SHALL:** Every active implementation-affecting object shall derive its authority from at least one accepted owner decision applicable to the object's exact scope.
- **REQ-CONF-DEC-002 — SHALL:** Every decision shall have one stable unique identifier, one version, one lifecycle state, one accountable owner, and one permanent historical record.
- **REQ-CONF-DEC-003 — SHALL:** Every accepted decision shall declare its problem, owner, scope, selected outcome, authority effect, affected canonical references, semantic change class, impact obligations, validation obligations, and effective transition.
- **REQ-CONF-DEC-004 — SHALL NOT:** A proposed, rejected, deprecated, superseded, archived, missing, malformed, or scope-inapplicable decision shall support new active authority.
- **REQ-CONF-DEC-005 — SHALL:** Decision acceptance and authority activation shall remain separate transitions, and activation shall occur only after the complete affected authority graph passes validation.
- **REQ-CONF-DEC-006 — SHALL:** Every decision scope shall use the canonical global, profile, profile-overlay, component, artifact, toolchain, or migration scope model and shall identify every applicable scoped object.
- **REQ-CONF-DEC-007 — SHALL NOT:** A decision shall acquire broader scope through omission, document placement, implementation prevalence, repeated prose, physical consolidation, generated projection, or similarity to another profile or component.
- **REQ-CONF-DEC-008 — SHALL:** Every accepted decision shall state one selected outcome with enough precision to determine ownership, defaults, boundaries, compatibility, failure behavior, migration, and validation where those dimensions are affected.
- **REQ-CONF-DEC-009 — SHALL:** Materially viable rejected alternatives shall be recorded when their omission could permit a future reader, validator, generator, or implementation to select a different outcome.
- **REQ-CONF-DEC-010 — SHALL NOT:** An AI agent, generator, validator, maintainer, recipe, implementation, test, issue, prompt, or migration tool shall infer, invent, normalize, or activate a missing architectural decision.
- **REQ-CONF-DEC-011 — SHALL:** Every active requirement, lock, normative document, profile, profile overlay, component contract, artifact contract, toolchain contract, release claim, exception mechanism, and conformance claim shall declare the accepted decisions on which its authority depends.
- **REQ-CONF-DEC-012 — SHALL:** Every active requirement shall reference an accepted source decision, and the requirement statement shall not introduce an architectural outcome absent from that decision.
- **REQ-CONF-DEC-013 — SHALL:** Every active alignment lock shall reference the accepted decision that authorizes its invariant and shall follow that decision's mutation and supersession path.
- **REQ-CONF-DEC-014 — SHALL:** Every major decision shall have an accepted ADR that records context, alternatives, rationale, consequences, compatibility, migration, and recovery implications while leaving the owner decision as the canonical outcome.
- **REQ-CONF-DEC-015 — SHALL:** Decision-to-ADR relationships shall be bidirectional, scope-compatible, lifecycle-compatible, and complete for every decision class that requires an ADR.
- **REQ-CONF-DEC-016 — SHALL:** Every accepted decision shall classify its semantic change and shall apply the versioning, migration, release, compatibility, and evidence obligations required by that class.
- **REQ-CONF-DEC-017 — SHALL:** Decision validation shall calculate direct and transitive impact across canonical registries, schemas, requirements, locks, profiles, components, artifacts, toolchains, documents, ADRs, tests, evidence, exceptions, releases, migration records, and generated contexts.
- **REQ-CONF-DEC-018 — SHALL:** Every affected object in a decision impact set shall have an explicit disposition of changed, validated unchanged, superseded, retired, migrated, regenerated, or not applicable with rationale.
- **REQ-CONF-DEC-019 — SHALL NOT:** Two accepted decisions shall prescribe incompatible outcomes for overlapping scope without an accepted superseding decision that resolves the overlap.
- **REQ-CONF-DEC-020 — SHALL:** A detected conflict among accepted decisions shall block affected activation, preserve every decision, produce a conflict report, and require owner-approved supersession before authority resumes.
- **REQ-CONF-DEC-021 — SHALL:** A superseding decision shall identify every replaced decision, changed semantic dimension, scope transition, compatibility effect, migration obligation, affected dependent, and required evidence.
- **REQ-CONF-DEC-022 — SHALL:** Superseded, deprecated, rejected, and archived decisions shall remain resolvable with their prior versions, scopes, outcomes, relationships, effective dates, and historical evidence.
- **REQ-CONF-DEC-024 — SHALL:** Every active exception mechanism shall derive from an accepted decision and shall remain separate from the decision that defines the baseline obligation.
- **REQ-CONF-DEC-025 — SHALL NOT:** Active authority shall contain a placeholder, open-authority marker, ambiguous status, missing selected outcome, undefined scope, undefined owner, undefined default, undefined failure behavior, or undefined compatibility behavior.
- **REQ-CONF-DEC-027 — SHALL:** Generated implementation contexts, AI contexts, matrices, indexes, manifests, and reports shall include only accepted applicable decisions and shall preserve their identifiers, versions, scopes, and canonical references.
- **REQ-CONF-DEC-028 — SHALL:** A change shall be treated as editorial without a new decision only when validation proves that authority, meaning, scope, ownership, strength, defaults, boundaries, state, failure behavior, compatibility, migration, release behavior, and identifier semantics remain unchanged.
- **REQ-CONF-DEC-029 — SHALL:** Decision-closure validation shall run against the complete clean active authority graph and shall not pass a change solely because its edited files are individually valid.
- **REQ-CONF-DEC-030 — SHALL:** A missing, inactive, incomplete, conflicting, or inapplicable decision shall produce a machine-readable blocked result that identifies the reason, required owner and scope, affected objects, prohibited inference, and remediation path.
- **REQ-CONF-DEC-031 — SHALL:** The authority registry shall activate a registry or documentation release only after decision closure, reference resolution, ownership, requirements, locks, profiles, contracts, artifacts, traceability, generated content, tests, evidence, and exception validation pass.
- **REQ-CONF-DEC-032 — SHALL:** A complete decision-closure conformance claim shall include decision-record, lifecycle, scope, ownership, outcome, conflict, supersession, ADR, impact, dependency, projection, migration, blocked-result, activation-order, and negative-path tests with evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Creating a proposed decision

A proposed decision follows this order:

1. assign a stable decision identifier;
2. record the problem and implementation-affecting question;
3. identify the accountable owner;
4. define the exact scope;
5. enumerate materially viable alternatives;
6. record the proposed selected outcome;
7. identify authority effects;
8. classify the semantic change;
9. identify direct impact;
10. initialize transitive impact analysis;
11. identify ADR applicability;
12. define validation and evidence;
13. validate the proposed record;
14. retain status as proposed until owner approval.

The proposal can support review and planning.

It cannot support active implementation authority.

### 6.2 Reviewing a decision

Review:

1. verifies owner authority;
2. verifies scope precision;
3. verifies selected-outcome completeness;
4. verifies alternatives and rationale;
5. verifies canonical ownership;
6. compares existing accepted decisions;
7. detects scope overlap and conflict;
8. reviews semantic change classification;
9. reviews direct and transitive impact;
10. reviews migration and compatibility;
11. reviews required ADR;
12. reviews tests and evidence;
13. records review findings;
14. returns the proposal for revision, rejection, or acceptance.

### 6.3 Accepting a decision

Acceptance:

1. confirms the accountable owner;
2. confirms required co-review or governance approval;
3. confirms one selected outcome;
4. confirms exact scope;
5. confirms conflict disposition;
6. confirms semantic change class;
7. confirms impact obligations;
8. confirms ADR status where required;
9. confirms validation plan;
10. records acceptance evidence;
11. changes decision status to accepted;
12. leaves authority activation pending.

Acceptance does not assert that all affected implementation and documentation changes already pass.

### 6.4 Implementing an accepted decision

Implementation:

1. freezes the accepted decision version;
2. updates canonical registries;
3. updates schemas;
4. updates requirements and locks;
5. updates profile and component contracts;
6. updates artifact and toolchain contracts;
7. updates lifecycle and release records;
8. updates normative and explanatory documents;
9. updates ADR and migration records;
10. updates tests and evidence expectations;
11. regenerates derived projections;
12. records every impact disposition.

The implementation does not alter the selected outcome without returning to decision review.

### 6.5 Validating decision closure

Validation:

1. load the complete active and candidate authority graph from a clean source tree;
2. validate the decision registry schema;
3. resolve every decision identifier and version;
4. validate lifecycle transitions;
5. verify accepted status for every active dependency;
6. verify owner and scope;
7. verify selected-outcome completeness;
8. verify references;
9. calculate direct and transitive impact;
10. verify every impact disposition;
11. detect overlapping conflicting decisions;
12. verify supersession;
13. verify ADR relationships;
14. verify requirements and locks;
15. verify profiles, components, artifacts, and toolchains;
17. verify generated projections and AI contexts;
18. execute tests;
19. verify evidence;
20. produce pass, fail, blocked, or not-applicable results.

### 6.6 Activating authority

Activation:

1. receives a passing full-graph validation result;
2. verifies the exact source-tree and registry identities;
3. verifies no relevant input changed after validation;
4. verifies required signatures or approvals;
5. selects the complete compatible authority set;
6. updates the authority registry;
7. publishes the documentation or registry release;
8. produces an activation receipt;
9. makes the accepted decision effective for active consumers;
10. preserves the previous authority set for rollback or historical interpretation as required.

### 6.7 Handling a missing decision

When an active change needs a decision that does not exist:

1. identify the architectural question;
2. identify the likely accountable owner without assigning the outcome;
3. identify affected scopes and objects;
4. emit a blocked result;
5. set prohibited inference to true;
6. exclude the affected candidate authority from activation;
7. allow creation of a proposed decision and impact report;
8. continue validation of unaffected scopes where useful.

The validator does not supply a default answer.

### 6.8 Handling an inactive decision

When an active object references a non-accepted decision:

1. preserve the referenced decision;
2. identify the active object and relationship;
3. classify the lifecycle incompatibility;
4. block the object's authority;
5. exclude the relationship from implementation contexts;
6. require acceptance, replacement, or reference correction;
7. rerun transitive impact validation.

### 6.9 Handling conflicting accepted decisions

Conflict handling:

1. preserve all conflicting decisions;
2. identify exact overlap;
3. identify incompatible outcome dimensions;
4. block affected activation;
5. generate a conflict report;
6. identify the accountable resolving owner;
7. create a proposed superseding decision;
8. update affected objects only after acceptance;
9. validate the complete superseding change;
10. activate the replacement last.

### 6.10 Superseding a decision

Supersession:

1. create and accept the replacement decision;
2. identify every replaced decision;
3. record changed semantics and scope;
4. define compatibility and migration;
5. update bidirectional succession links;
6. migrate requirement, lock, profile, component, artifact, document, test, evidence, exception, release, and context relationships;
7. validate historical resolvability;
8. validate the complete replacement graph;
9. activate the replacement;
10. mark prior decisions superseded or deprecated according to the transition.

### 6.11 Validating an editorial change

Editorial validation:

1. compare old and new canonical records;
2. compare authority and owner;
3. compare scope;
4. compare selected outcome;
5. compare normative strength and behavior;
6. compare defaults and boundaries;
7. compare state, failure, compatibility, migration, and release effects;
8. compare identifiers;
9. prove no interpretation-affecting change;
10. retain decision identity and update only the applicable record version.

When proof is insufficient, the change returns to semantic decision review.


Cutover validation:

1. inventory every source decision and decision-like source statement;
2. map each source item to adopted, adapted, superseded, excluded, historical-only, or merged disposition;
3. require accepted decisions for adaptation and conflict resolution;
4. verify destination canonical references;
5. verify no active destination depends on a non-final source choice;
6. verify migration evidence preserves source lineage;
7. verify generated contexts exclude historical non-authority;
8. activate the destination authority only after complete disposition coverage.

## 7. Failure States and Safe Degradation

| Failure state | Required conformance response |
| --- | --- |
| Decision identifier is missing or invalid | The record remains inactive and dependent authority is blocked. |
| Decision owner is missing | Closure fails and the validator identifies the required authority domain. |
| Decision scope is absent or ambiguous | Closure fails; scope does not default to global or inherit from document placement. |
| Selected outcome is incomplete | Closure fails and the missing semantic dimensions are reported. |
| Decision status is not accepted | New dependent authority remains inactive. |
| Accepted decision has invalid references | Activation remains blocked until references resolve or the decision is superseded. |
| Active requirement lacks an accepted source decision | The requirement is invalid for active conformance. |
| Requirement adds an outcome absent from its decision | Decision closure fails and the obligation returns to owner review. |
| Lock lacks an accepted source decision | The lock is invalid and affected activation remains blocked. |
| Major decision lacks an accepted ADR | Closure remains incomplete. |
| ADR and decision scope differ incompatibly | The relationship is rejected and the major decision remains incomplete. |
| Impact analysis omits a direct dependent | Closure fails and the missing disposition is reported. |
| Transitive impact traversal is incomplete | Activation remains blocked even when edited files pass. |
| Affected object has no disposition | Closure fails because silence cannot establish compatibility. |
| Accepted decisions conflict | The overlapping authority is blocked until supersession. |
| Supersession link is one-way | Succession validation fails. |
| Replacement scope leaves an unexplained gap | Supersession remains incomplete. |
| Historical decision version cannot be resolved | Claims and receipts depending on that version remain unverifiable. |
| Exception is used to avoid a decision | The exception is rejected and the missing-decision result remains blocked. |
| Active authority contains an open-authority marker | Validation fails at the exact field or source location. |
| Migration source has no final disposition | Cutover remains blocked. |
| Generated implementation context includes a proposal | The context is rejected and regenerated. |
| Generated projection omits an applicable accepted decision | The projection is stale and cannot support implementation or release. |
| Editorial classification hides a semantic change | Validation fails and a new or revised decision is required. |
| Validation runs from a dirty or incomplete graph | The result is not eligible for authority activation. |
| Decision acceptance occurs after authority activation | The release is invalid and rollback or repair is required. |
| Evidence is missing | Closure remains incomplete for the affected claim. |
| Validation tooling is unavailable | No new authority release or complete conformance claim is issued. |
| Decision registry is unavailable | Last-known-valid authority can remain readable; new closure and activation remain blocked. |

Decision-system failure never grants broader behavior.

## 8. Cross-Component Interactions

### 8.1 Authority registry

The authority registry consumes the final validation result and activates only a complete compatible authority set.

It does not repair missing decisions or select conflict outcomes.

### 8.2 Decision registry

The decision registry owns decision identity, lifecycle, owner, scope, selected outcome, and succession.

The conformance validator reads these records and reports whether they can support active authority.

### 8.3 Documentation registry

The documentation registry identifies which decisions each normative document depends on.

A document with a missing, inactive, or scope-inapplicable decision dependency is invalid.

### 8.4 Requirements registry

The requirements registry links each active obligation to accepted source decisions.

Decision-closure validation verifies that the obligation is within the decision's authority and does not invent a new outcome.

### 8.5 Locks registry

The locks registry connects decisions to cross-file invariants.

Decision closure verifies that every affected assertion reflects the selected outcome across all locked objects.

### 8.6 ADR registry

The ADR registry verifies identity, accepted status, scope, decision linkage, and succession for required architectural records.

The ADR explains the decision but does not replace the decision outcome.

### 8.7 Traceability registry

Traceability provides direct and transitive relationship traversal.

The validator uses it to calculate impact and to detect orphaned or stale dependents.

### 8.8 Profile contracts

Profile and overlay contracts consume accepted decisions within exact scope.

A profile cannot inherit another profile's decision silently.

Physical consolidation does not merge decision scope or component authority.

### 8.9 Component contracts

Component contracts implement accepted responsibility, ownership, command, query, event, dependency, and degradation decisions.

A repository package or running process does not create a component decision.

### 8.10 Artifact and release contracts

Artifact classes, artifact schemas, release channels, Release Sets, activation, rollback, and recovery consume accepted lifecycle decisions.

A valid artifact cannot compensate for a missing lifecycle or compatibility decision.

### 8.11 Exception registry

The exception registry records bounded deviations from active requirements.

It cannot approve an undefined baseline or an authority conflict.

### 8.12 Test and evidence registries

Tests verify exact decision versions, scopes, relationships, and expected blocked behavior.

Evidence supports acceptance review, impact, validation, activation, migration, and conformance claims.

### 8.13 Generated contexts

Generated implementation and AI contexts include only applicable accepted decisions.

Review contexts can include proposals and history only when their non-authoritative status is explicit.

### 8.14 Migration system

Migration records preserve source lineage and final disposition.

The migration system cannot carry undecided source behavior into the active destination.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Accepted decisions

| Decision | Effect |
| --- | --- |
| `DEC-DOC-001` | Establishes one active canonical documentation corpus and machine-readable authority order. |
| `DEC-DOC-002` | Requires accepted owner decisions before implementation-affecting authority becomes active and prohibits inferred architectural outcomes. |
| `DEC-COMP-001` | Preserves explicit component identity, responsibility, ownership, and boundary decisions. |
| `DEC-PROFILE-BASELINE-001` | Preserves exact global, profile, and profile-overlay scope rather than implicit inheritance. |

### 9.2 Related ADRs

| ADR | Relevance |
| --- | --- |
| `ADR-000` | Establishes canonical registries, authority order, generated projections, and alignment controls. |
| `ADR-006` | Requires explicit first-class component decisions and boundaries. |
| `ADR-008` | Preserves independent release-channel authority. |
| `ADR-013` | Separates global behavior from profile-specific decisions. |
| `ADR-016` | Keeps generated documentation and AI contexts non-authoritative. |
| `ADR-023` | Makes overlay effects explicit. |
| `ADR-024` | Preserves logical ownership across physical deployment forms. |
| `ADR-025` | Governs canonical cutover and deprecated-authority retirement. |
| `ADR-026` | Blocks active authority that depends on a missing implementation decision. |

### 9.3 Prohibited assumptions

The following assumptions are prohibited:

- the current implementation defines intended architecture;
- the newest file wins;
- the most detailed file wins;
- the highest identifier wins;
- the longest decision record wins;
- a repeated rule becomes global;
- a recipe becomes authoritative because it is deployed;
- a profile inherits another profile's decision silently;
- physical service consolidation merges component decisions;
- an installed optional component becomes baseline;
- a validator can choose the safest-looking missing outcome;
- an AI agent can choose the most likely missing outcome;
- a missing failure rule means best-effort continuation;
- a missing security rule means permission;
- a missing profile value can be copied from a similar profile;
- a proposed decision supports temporary active implementation;
- an accepted ADR replaces an owner decision;
- a merged code change changes authority automatically;
- a passing edited-file test proves complete closure;
- an exception can define an absent baseline;
- migration evidence remains active authority after cutover;
- file order resolves conflicting accepted decisions;
- deployment prevalence resolves conflicting accepted decisions;
- a deprecated decision supports new adoption;
- a superseded decision remains current because an old component uses it;
- generated context can add or broaden decision scope;
- an editorial label can conceal a semantic change;
- authority activation can precede impact validation;
- a missing dependent disposition means validated unchanged;
- last-known-valid authority permits new decisions to be inferred.

The machine-readable conclusion for absent decision authority is a blocked result, not an invented default.

## 10. Validation Criteria

This document conforms when all of the following checks pass:

1. metadata status is `active`;
2. the registered path is `09-conformance/11-decision-closure-validation.md`;
3. the document class is `normative_markdown`;
4. all canonical references resolve;
5. all listed decisions are accepted;
6. all requirements match the requirements registry;
7. all locks resolve and pass;
8. the decision registry validates against its active schema;
9. every decision identifier is unique and permanently reserved;
10. every decision version and lifecycle transition is valid;
11. every accepted decision has one accountable owner;
12. every accepted decision has an explicit scope;
13. every accepted decision has one complete selected outcome;
14. every applicable authority effect is declared;
15. materially viable rejected alternatives are recorded where needed;
16. every active object declares applicable accepted decisions;
17. no active object depends on an inactive or missing decision;
18. requirement source-decision relationships are complete and scope-compatible;
19. locks reference accepted decisions and compatible scope;
20. every major decision has an accepted ADR;
21. decision-to-ADR relationships are bidirectional;
22. decision and ADR scopes and lifecycle states are compatible;
23. semantic change classes are valid;
24. direct impact covers every explicitly affected object;
25. transitive impact traversal reaches every dependent authority object;
26. every affected object has an explicit disposition;
27. no incompatible accepted decisions overlap;
28. conflict reports identify exact scopes and outcome dimensions;
29. superseding decisions identify every replaced decision;
30. succession links are bidirectional;
31. supersession preserves history and migration;
32. deprecated decisions do not support new adoption;
33. exceptions do not substitute for missing decisions;
34. active authority contains no placeholder or open-authority state;
36. generated implementation contexts contain only applicable accepted decisions;
37. generated projections preserve decision identifiers, versions, and scope;
38. editorial changes prove semantic equivalence;
39. full validation runs from a clean declared authority graph;
40. blocked results identify reason, owner, scope, affected objects, prohibited inference, and remediation;
41. acceptance precedes activation;
42. activation follows complete graph validation;
43. tests cover missing, inactive, incomplete, conflicting, superseded, scope-inapplicable, and orphaned decisions;
44. tests cover ADR, impact, migration, projection, exception, and activation-order failures;
45. evidence supports decision review, acceptance, impact, validation, activation, and migration;
46. requirement-to-test-to-evidence traceability is complete;
47. active content is English;
48. placeholder and open-authority markers are absent.

The validator reports focused failures, including:

```text
decision_identifier_missing
decision_identifier_collision
decision_version_invalid
decision_lifecycle_transition_invalid
decision_owner_missing
decision_scope_missing
decision_scope_object_missing
decision_selected_outcome_missing
decision_selected_outcome_incomplete
decision_authority_effect_missing
decision_rejected_alternative_gap
decision_not_accepted
decision_scope_inapplicable
decision_active_dependency_missing
decision_requirement_source_mismatch
decision_lock_source_mismatch
decision_major_adr_missing
decision_adr_link_not_bidirectional
decision_adr_scope_mismatch
decision_semantic_class_invalid
decision_direct_impact_incomplete
decision_transitive_impact_incomplete
decision_impact_disposition_missing
decision_conflicting_accepted
decision_conflict_scope_unknown
decision_supersession_incomplete
decision_supersession_link_not_bidirectional
decision_history_missing
decision_exception_substitution
decision_open_authority_state
decision_generated_context_includes_inactive
decision_generated_projection_stale
decision_editorial_change_semantic
decision_validation_graph_dirty
decision_blocked_result_incomplete
decision_activation_before_acceptance
decision_activation_before_validation
decision_evidence_missing
decision_orphaned
```

## 11. Non-Normative Examples

### 11.1 Missing component ownership decision

A proposed indexing component has a repository, database schema, and running service, but no accepted decision states whether it owns canonical data.

The validator blocks component-contract activation and reports the required owner and affected component scope.

It does not infer ownership from the database or implementation.

### 11.2 Accepted decision awaiting activation

An owner accepts a decision to add a new knowledge artifact class.

The artifact-class entry, schema, release-channel compatibility, requirements, locks, tests, and documentation are not complete.

The decision is accepted, but the new artifact class remains inactive until full-graph validation passes.

### 11.3 Scoped decisions that do not conflict

One accepted decision permits GNOME in developer profiles.

Another forbids GNOME in a high-assurance appliance overlay.

The validator finds no conflict when the scopes and composition rule are explicit. The overlay narrows the applicable profile composition.

### 11.4 Conflicting component decisions

Two accepted decisions assign authoritative ownership of the same civic record to different components in the same profile scope.

The validator blocks both affected ownership projections, preserves the decisions, and requires a superseding owner decision.

File age and implementation prevalence do not select a winner.

### 11.5 Requirement exceeds its source decision

A decision requires per-workspace service isolation.

A proposed requirement also mandates a specific container runtime, although the decision does not select one.

Decision closure rejects the requirement because it introduces a new architectural outcome.

### 11.6 Major decision without ADR

A decision changes trust-root custody and recovery authority.

The decision record is accepted, but no accepted ADR records alternatives, consequences, and migration.

Closure remains incomplete because the decision class requires an ADR.

### 11.7 Complete supersession

A new decision replaces an earlier release-channel rule.

It identifies the prior decision, changed compatibility semantics, migration interval, affected artifact classes, Release Sets, locks, tests, and releases. Both records link to each other, and historical releases retain the old decision version.

### 11.8 Migration quotation

A migration evidence file quotes a historical source that did not select a final profile behavior.

The migration unit links that source to an accepted final disposition. Generated implementation contexts include the final decision, not the historical quotation.

### 11.9 Generated AI implementation context

A component implementation context is built for Konnaxion on a sovereign offline profile.

The generator selects only accepted decisions applicable to Konnaxion, the selected profile, and active overlays. Proposed alternatives and superseded outcomes remain outside the implementation context.

### 11.10 Blocked result

A profile contract references a decision identifier that does not exist.

The validator emits a blocked result containing the missing decision reference, required profile-architecture owner, profile scope, affected contract and documents, prohibited inference flag, and proposed-decision remediation path.
