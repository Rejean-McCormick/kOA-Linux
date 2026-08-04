<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-GOV-005",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "governance",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/decision-index.json#/decision_closure_policy",
    "generated/authority-manifest.json#/authority_order",
    "generated/requirements-index.json#/requirements",
    "generated/assertion-index.json#/locks"
  ],
  "decision_ids": [
    "DEC-DOC-002"
  ],
  "requirement_ids": [
    "REQ-DOC-DEC-001",
    "REQ-DOC-DEC-002",
    "REQ-DOC-DEC-003",
    "REQ-DOC-DEC-004",
    "REQ-DOC-DEC-005",
    "REQ-DOC-DEC-006",
    "REQ-DOC-DEC-007",
    "REQ-DOC-DEC-008",
    "REQ-DOC-DEC-009",
    "REQ-DOC-DEC-010",
    "REQ-DOC-DEC-011",
    "REQ-DOC-DEC-012"
  ],
  "lock_ids": [
    "LOCK-DOC-011",
    "LOCK-DOC-012",
    "LOCK-DOC-013",
    "LOCK-DOC-014"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-003",
    "DOC-GOV-004"
  ],
  "tags": [
    "decision-closure",
    "authority",
    "ambiguity",
    "ai-authoring",
    "validation"
  ]
}
KOA:DOC-META:END -->

# Decision Closure and Prohibited Ambiguity

## 1. Purpose

This document defines how kOA closes architectural decisions before they become active authority.

Its purpose is to prevent AI agents, maintainers, generators, implementation code, and downstream documentation from filling architectural gaps through inference.

The active documentation system does not use unresolved architectural placeholders. Any matter that affects implementation, conformance, security, profile behavior, component ownership, data authority, release behavior, failure behavior, or validation must have an accepted owner decision before dependent objects become active.

A missing decision is a blocking condition, not an invitation to guess.

## 2. Scope

This policy applies globally to:

- owner decisions;
- authority manifests;
- canonical registries;
- JSON Schemas;
- normative Markdown;
- deployment profiles and overlays;
- component contracts;
- toolchain contracts;
- artifact contracts;
- ADRs;
- requirements;
- Interfile Alignment Locks;
- exceptions and waivers;
- generated projections;
- AI context packages;
- conformance claims;
- implementation work derived from active documentation.

This policy does not grant authority to drafts, proposals, archived documents, migration evidence, informal discussions, issue descriptions, prompts, code comments, or generated suggestions.

A proposal may exist for review, but no active object may depend on it.

## 3. Canonical References

The canonical sources for this policy are:

- `generated/decision-index.json#/decision_closure_policy`;
- `generated/decision-index.json#/decisions`;
- `generated/authority-manifest.json#/authority_order`;
- `generated/document-index.json#/documents`;
- `generated/requirements-index.json#/requirements`;
- `generated/assertion-index.json#/locks`;
- `generated/decision-index.json#/adrs`;
- `generated/exception-index.json#/exceptions`;
- `generated/traceability.json#/links`;

The accepted owner decision authorizing this policy is:

- `DEC-DOC-002` — No unresolved implementation-affecting matter may enter active authority.

The principal alignment locks are:

- `LOCK-DOC-011` — Active architectural authority contains no undecided implementation-affecting matter.
- `LOCK-DOC-012` — Every proposal affecting implementation is accepted or rejected before activation.
- `LOCK-DOC-013` — An object with a missing required decision remains inactive.
- `LOCK-DOC-014` — AI agents may not replace missing authority with inferred architectural decisions.

## 4. Model and Responsibilities

### 4.1 Decision closure principle

An architectural matter is closed only when all of the following are true:

1. a stable decision identifier exists;
2. the decision has a named owner;
3. the decision states its scope;
4. the decision states the selected outcome;
5. rejected alternatives are recorded when they materially affect interpretation;
6. affected canonical references are identified;
7. affected requirements and locks are identified;
8. validation and evidence obligations are defined;
9. the decision status is `accepted`;
10. the decision is activated through `authority.registry.json`.

A meeting conclusion, prompt response, implementation choice, merged code change, or repeated convention does not close a decision by itself.

### 4.2 Decision ownership

Every decision has exactly one accountable owner role.

The owner is responsible for:

- selecting the outcome;
- defining scope;
- ensuring that the decision is internally complete;
- resolving conflicts with existing accepted decisions;
- approving semantic classification;
- approving replacement or retirement;
- ensuring that validation evidence exists.

An AI agent may draft a decision record, impact report, ADR, or implementation plan. It may not self-approve an owner decision unless the agent is operating under an explicit authority mechanism that records the human or institutional owner’s approval.

### 4.3 Decision states

The canonical decision-state enum is owned by `generated/decision-index.json`.

<!-- GENERATED:BEGIN
source=generated/decision-index.json#/decision_states
renderer=canonical-table-v1
-->
| State | Authority effect |
| --- | --- |
| `proposed` | Reviewable draft. It has no effect on active authority. |
| `accepted` | May authorize active requirements, locks, profiles, contracts, and documentation. |
| `rejected` | Preserved as a considered alternative. It has no active authority. |
| `deprecated` | Still valid for a declared compatibility interval but not for new adoption. |
| `superseded` | Replaced by another accepted decision. It has no current authority except historical interpretation. |
| `archived` | Historical record with no current authority. |
<!-- GENERATED:END -->

Only `accepted` decisions may support active authority.

### 4.4 Activation boundary

Acceptance and activation are separate operations.

A decision becomes active only when:

1. its record is schema-valid;
2. all required impact dispositions are complete;
3. linked requirements, locks, schemas, profiles, contracts, and documents are valid;
4. generated projections are current;
5. required tests pass;
6. `authority.registry.json` references the accepted decision or the registry version containing it.

This separation prevents partially applied decisions.

### 4.5 Ambiguity classes

The following ambiguity classes are prohibited in active authority:

- missing owner;
- missing selected outcome;
- contradictory selected outcomes;
- undefined scope;
- undefined profile applicability;
- undefined component ownership;
- undefined data authority;
- undefined capability membership;
- undefined release-channel ownership;
- undefined default behavior;
- undefined failure behavior;
- undefined fallback behavior;
- undefined validation behavior;
- undefined compatibility behavior;
- a reference to a non-existent decision;
- a reference to a decision that is not accepted;
- an implementation choice presented as a system rule without profile adoption;
- a proposal presented as current architecture.

### 4.6 Prohibited unresolved markers

The canonical prohibited-marker list is owned by `generated/decision-index.json#/decision_closure_policy/prohibited_markers`.

The validator SHALL detect these markers in active status fields, metadata fields, normative headings, requirement statements, lock statements, profile claims, component contracts, and generated authority projections.

```policy-literal
open-decision placeholder
TO DECIDE
UNRESOLVED
UNKNOWN BEHAVIOR
PENDING DEFINITION
PLACEHOLDER DECISION
TEMPORARY DECISION
FIXME
XXX
```

The checker SHALL be syntax-aware. It SHALL NOT fail merely because this policy, a validation test fixture, migration evidence, or an archive quotes a prohibited marker for explanatory purposes.

### 4.7 Relationship to ADRs

A decision registry record states the authoritative outcome.

An ADR records the architectural context, alternatives, rationale, consequences, and migration implications of a significant decision.

An ADR is required when a decision:

- changes authority order;
- changes canonical ownership;
- changes a global invariant;
- changes a component boundary;
- changes profile composition;
- changes security or privilege behavior;
- changes the AI boundary;
- changes data authority;
- changes release or rollback semantics;
- changes an Interfile Alignment Lock;
- is classified as a major semantic change.

The decision record remains the canonical authority pointer. The ADR remains the detailed rationale.

### 4.8 Relationship to exceptions

An exception does not represent an undecided matter.

An exception is a bounded, accepted deviation from an active requirement. It must declare:

- an `EXC-ID`;
- the exact requirement being waived;
- affected scope;
- owner;
- rationale;
- compensating controls;
- start date;
- expiry date or explicit permanent status;
- validation evidence;
- revocation conditions.

An exception may not be used to avoid making an architectural decision.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-DOC-DEC-001,REQ-DOC-DEC-002,REQ-DOC-DEC-003,REQ-DOC-DEC-004,REQ-DOC-DEC-005,REQ-DOC-DEC-006,REQ-DOC-DEC-007,REQ-DOC-DEC-008,REQ-DOC-DEC-009,REQ-DOC-DEC-010,REQ-DOC-DEC-011,REQ-DOC-DEC-012 -->
- **REQ-DOC-DEC-001 — SHALL:** Every implementation-affecting architectural matter has an accepted owner decision before dependent objects become active.
- **REQ-DOC-DEC-002 — SHALL NOT:** An active requirement, profile, component contract, artifact contract, lock, release, or conformance claim depend on a proposed, rejected, superseded, archived, or missing decision.
- **REQ-DOC-DEC-003 — SHALL:** Every accepted decision declares its owner, scope, selected outcome, affected canonical references, semantic change class, and validation obligations.
- **REQ-DOC-DEC-004 — SHALL:** Conflicting accepted decisions are resolved by an explicit superseding decision before activation of affected changes.
- **REQ-DOC-DEC-005 — SHALL NOT:** An AI agent infer, invent, silently normalize, or implement a missing architectural decision.
- **REQ-DOC-DEC-006 — SHALL:** A missing required decision produces a blocked validation result with machine-readable reason `missing_owner_decision`.
- **REQ-DOC-DEC-007 — SHALL:** Only accepted decisions may be activated through `authority.registry.json`.
- **REQ-DOC-DEC-008 — SHALL:** Major decisions have an accepted ADR, a transitive impact report, updated traceability, and passing validation.
- **REQ-DOC-DEC-009 — SHALL:** A superseded or retired decision remains preserved and linked to its replacement.
- **REQ-DOC-DEC-010 — SHALL NOT:** Prohibited unresolved markers appear as active architectural status, active normative content, or active generated authority.
- **REQ-DOC-DEC-011 — SHALL:** Exceptions are explicit, bounded, owned, validated, and separate from decision closure.
- **REQ-DOC-DEC-012 — SHALL:** Decision acceptance and authority activation occur as separate validated transitions.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 New decision procedure

A new architectural decision follows this sequence:

1. create a stable `DEC-ID`;
2. record the problem and target scope;
3. identify the owner;
4. enumerate materially viable alternatives;
5. select one outcome;
6. record rejected alternatives when omission could create ambiguity;
7. classify the change as `patch`, `minor`, or `major`;
8. identify affected canonical references;
9. identify affected locks and requirements;
10. create an ADR when required;
11. compute direct and transitive impact;
12. update affected canonical registries;
13. update schemas when needed;
14. update explanatory Markdown;
15. regenerate projections and AI contexts;
16. update tests and evidence;
17. validate the complete change;
18. mark the decision `accepted`;
19. activate the new authority version last.

### 6.2 Proposal transition

A proposed decision may transition to:

- `accepted`;
- `rejected`;
- `archived`.

It may not transition directly to `deprecated` or `superseded`, because it never held active authority.

### 6.3 Accepted decision transition

An accepted decision may transition to:

- `deprecated`;
- `superseded`.

An accepted decision SHALL NOT be deleted.

A superseding decision SHALL identify:

- the replaced decision;
- changed semantics;
- compatibility impact;
- migration obligations;
- affected locks;
- affected profiles and components;
- required version changes.

### 6.4 Missing-decision handling

When a validator or AI agent discovers that active work requires an absent decision, it emits:

```json
{
  "validation_status": "blocked",
  "reason": "missing_owner_decision",
  "required_decision_scope": "",
  "affected_canonical_refs": [],
  "affected_document_ids": [],
  "prohibited_inference": true
}
```

The affected change remains inactive.

The agent may draft a proposed decision record and impact analysis. It may not continue as though the draft were accepted.

### 6.5 Conflict handling

When two accepted decisions conflict:

1. both remain preserved;
2. affected activation is blocked;
3. a conflict report identifies the incompatible statements and scopes;
4. the owner issues a superseding decision;
5. the superseding decision explicitly selects the surviving behavior;
6. all affected requirements, locks, profiles, contracts, tests, and documents are updated;
7. authority activation occurs only after full validation.

File order, newer modification time, implementation prevalence, and agent preference SHALL NOT resolve the conflict.

### 6.6 Editorial clarification

A purely editorial clarification may proceed without a new decision only when it changes none of the following:

- meaning;
- scope;
- ownership;
- requirement strength;
- default behavior;
- component boundary;
- profile applicability;
- state model;
- capability classification;
- failure behavior;
- validation behavior;
- release behavior;
- identifier semantics.

If a reviewer cannot prove that meaning is unchanged, the change is semantic and requires decision review.

## 7. Failure States and Safe Degradation

### 7.1 `missing_owner_decision`

Condition:

- an active or proposed change requires a decision that does not exist.

Required behavior:

- block activation;
- identify affected objects;
- allow drafting of a proposal;
- prohibit inferred implementation.

### 7.2 `decision_not_accepted`

Condition:

- an active object references a decision whose state is not `accepted`.

Required behavior:

- mark the active object invalid;
- exclude it from generated AI context;
- fail conformance and release validation.

### 7.3 `conflicting_accepted_decisions`

Condition:

- two accepted decisions prescribe incompatible outcomes for overlapping scope.

Required behavior:

- fail closed for affected authority;
- generate a conflict report;
- require an explicit superseding decision.

### 7.4 `ambiguous_scope`

Condition:

- a rule does not distinguish global, profile, overlay, component, artifact, toolchain, or migration-only scope.

Required behavior:

- reject the rule;
- prohibit profile inheritance;
- require scope correction through canonical authority.

### 7.5 `orphaned_decision`

Condition:

- an accepted decision has no canonical references, linked requirements, locks, ADR, or documented effect.

Required behavior:

- fail traceability validation;
- require explicit disposition as active, deprecated, superseded, or archived.

### 7.6 `stale_decision_projection`

Condition:

- Markdown, generated indexes, AI contexts, or manifests do not match the active decision registry version.

Required behavior:

- reject generated outputs;
- regenerate;
- prevent release until versions align.

### 7.7 `prohibited_ambiguity_marker`

Condition:

- a prohibited unresolved marker appears in active authority outside an allowed literal or historical context.

Required behavior:

- fail validation;
- report exact path and location;
- require a closed decision or removal of the invalid marker.

### 7.8 Safe degradation rule

Decision-system failure never authorizes broader behavior.

When decision authority cannot be verified:

- no new authority is activated;
- existing last-known-valid authority may remain readable;
- implementation work requiring the missing authority is blocked;
- unaffected scopes may continue;
- no silent default is selected.

## 8. Cross-Component Interactions

### 8.1 Authority registry

`authority.registry.json` activates only schema-valid registry versions whose required decisions are accepted.

### 8.2 Requirements registry

Every active requirement references an accepted source decision.

A requirement cannot compensate for a missing decision by embedding a new architectural outcome in its statement.

### 8.3 Lock registry

Every active lock references the decision that authorizes its canonical assertion.

Changing a lock requires decision review according to its mutation policy.

### 8.4 Documentation registry

Every normative document declares applicable decision identifiers.

A document with a missing or inactive decision reference is invalid.

### 8.5 ADR registry

Every accepted major ADR links to at least one accepted decision.

An ADR without a decision record provides rationale but does not activate authority.

### 8.6 Exception registry

Every exception references an active requirement and an accepted decision authorizing the exception mechanism.

An expired exception is invalid and cannot silently continue.

### 8.7 Traceability registry

Traceability links decisions to:

- requirements;
- locks;
- profiles;
- components;
- documents;
- tests;
- evidence;
- releases.

Missing required links fail validation.

### 8.8 AI context registry

Generated AI contexts include only accepted decisions applicable to their declared scope.

Proposals, rejected alternatives, and historical decisions may appear only in an explicitly requested review context, never in an implementation context.


non-authoritative source entries that were previously unresolved must receive accepted final dispositions before cutover.

Migration evidence may quote historical unresolved wording, but the active replacement must be explicit.

## 9. Decision Closure and Prohibited Assumptions

The following assumptions are prohibited:

- “The current implementation probably defines the intended architecture.”
- “The newest file wins.”
- “The most detailed file wins.”
- “A repeated rule is automatically global.”
- “A recipe is authoritative because it is already deployed.”
- “A profile inherits another profile unless stated otherwise.”
- “An optional component may become baseline because it is installed.”
- “An AI agent may choose the most reasonable unresolved option.”
- “A missing failure rule implies best-effort continuation.”
- “A missing security rule implies permission.”
- “A missing profile value may be copied from a similar profile.”
- “A draft ADR is enough to authorize implementation.”
- “A merged code change automatically changes the documentation contract.”
- “A generated context package may override its source registry.”
- “An exception may remain active after expiry.”
- “Migration evidence remains current authority after cutover.”

When none of the active canonical sources defines the required behavior, the only permitted conclusion is:

```text
BLOCKED: MISSING OWNER DECISION
```

## 10. Validation Criteria

This document is conformant only when all of the following checks pass.

### 10.1 Schema checks

- `decisions.registry.json` validates against its schema.
- Every decision uses a canonical state.
- Every accepted decision contains all mandatory fields.
- Every superseded decision has a replacement reference.
- Every decision reference resolves.

### 10.2 Authority checks

- Only accepted decisions support active authority.
- The authority index references the expected decision-registry path, version, and status.
- Acceptance and activation timestamps are distinct and ordered.
- No active object depends on a proposed or missing decision.

### 10.3 Alignment checks

- Every active requirement has an accepted source decision.
- Every mandatory lock has an accepted source decision.
- Every normative document declares applicable decisions.
- Every major ADR links to an accepted decision.
- Every exception references valid active authority.
- Every generated AI context contains only applicable accepted decisions.

### 10.4 Ambiguity checks

- No prohibited unresolved marker appears in active authority.
- No active rule has undefined scope.
- No active capability has undefined profile membership.
- No active component has undefined data ownership.
- No active artifact class has undefined activation or failure behavior.
- No conflicting accepted decisions overlap without a superseding decision.

### 10.5 Required test identifiers

The initial conformance suite SHALL include:

- `TEST-DOC-DEC-001` — reject an active requirement linked to a proposed decision;
- `TEST-DOC-DEC-002` — reject an active profile linked to a missing decision;
- `TEST-DOC-DEC-003` — detect conflicting accepted decisions;
- `TEST-DOC-DEC-004` — detect prohibited unresolved markers;
- `TEST-DOC-DEC-005` — detect ambiguous scope;
- `TEST-DOC-DEC-006` — verify supersession links;
- `TEST-DOC-DEC-007` — verify authority activation occurs after validation;
- `TEST-DOC-DEC-008` — verify generated AI contexts exclude proposals;
- `TEST-DOC-DEC-009` — verify archived and migration quotations do not produce false positives;
- `TEST-DOC-DEC-010` — verify blocked machine-readable output for a missing decision.

## 11. Non-Normative Examples

### 11.1 New component with undefined authority

A developer proposes a new indexing component but does not define whether it owns canonical data.

Incorrect behavior:

- infer ownership from its database schema;
- document it as authoritative;
- implement direct writes from another component.

Correct behavior:

- block activation;
- create a proposed owner decision;
- define ownership, scope, interfaces, and failure behavior;
- accept the decision;
- update component, requirement, lock, and traceability registries;
- validate before activation.

### 11.2 Conflicting profile rules

One accepted decision permits GNOME in standard developer profiles. Another accepted decision forbids GNOME for an appliance overlay.

This is not a conflict when scope is explicit.

It becomes a conflict only if the appliance rule is incorrectly generalized to all Linux profiles.

The correct resolution is to preserve profile scope, not to select one desktop rule globally.

### 11.3 AI-generated “reasonable default”

An AI agent finds no declared host-port allocation policy for parallel workspaces.

Incorrect response:

- select a common port range and implement it as though authoritative.

Correct response:

- report `missing_owner_decision`;
- draft a proposed allocation decision and impact report;
- wait for acceptance before activating the rule.

### 11.4 Migration record containing historical unresolved wording

A migration evidence file quotes an old source that used an unresolved marker.

The quote may remain as historical evidence when:

- the file class is `migration_evidence`;
- the quoted range is marked non-normative;
- the active replacement disposition is accepted and explicit;
- generated implementation contexts exclude the historical wording.
