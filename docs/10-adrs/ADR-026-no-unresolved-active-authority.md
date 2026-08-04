<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ADR-026",
  "document_class": "adr",
  "status": "accepted",
  "language": "en",
  "layer": "architecture_decision",
  "scope": [
    "global",
    "authority",
    "decision_closure"
  ],
  "canonical_refs": [
    "generated/decision-index.json#/decisions/DEC-DOC-002",
    "generated/decision-index.json#/decision_closure_policy",
    "generated/authority-manifest.json",
    "generated/document-index.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/decision-index.json",
    "generated/exception-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "contracts/ai-navigation.contract.json"
  ],
  "decision_ids": [
    "DEC-DOC-002",
    "DEC-DOC-003",
    "DEC-DOC-004",
    "DEC-DOC-005",
    "DEC-AUTH-001",
    "DEC-IDENT-001",
    "DEC-DATA-001",
    "DEC-COMP-001",
    "DEC-GOV-001",
    "DEC-AI-001",
    "DEC-LIFE-001"
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
    "LOCK-DOC-001",
    "LOCK-DOC-002",
    "LOCK-DOC-003",
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
    "LOCK-DOC-014",
    "LOCK-DOC-015",
    "LOCK-DOC-016",
    "LOCK-DOC-017",
    "LOCK-DOC-018",
    "LOCK-DOC-019",
    "LOCK-DOC-020",
    "LOCK-DOC-021",
    "LOCK-DOC-022",
    "LOCK-AUTH-001",
    "LOCK-AUTH-002",
    "LOCK-AUTH-003",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-004",
    "DOC-GOV-005",
    "DOC-GOV-007",
    "DOC-GOV-009",
    "DOC-GOV-010",
    "DOC-GOV-011",
    "DOC-GOV-012",
    "DOC-GOV-013",
    "DOC-GOV-015",
    "DOC-CONST-004",
    "DOC-CONF-009",
    "DOC-SEC-000",
    "DOC-SEC-011"
  ],
  "tags": [
    "architecture-decision",
    "active-authority",
    "decision-closure",
    "fail-closed",
    "prohibited-ambiguity",
    "canonical-ownership",
    "authority-activation",
    "validation",
    "exceptions",
    "ai-authoring",
    "traceability"
  ]
}
KOA:DOC-META:END -->

# ADR-026 — No Unresolved Active Authority

**ADR ID:** `ADR-026`  
**Status:** `accepted`  
**Decision class:** `major`  
**Decision owner:** `owner:documentation-architecture`  
**Owner decision:** `DEC-DOC-002`  
**Change packet:** `CHG-2026-0026`  
**Created:** `2026-08-03`  
**Accepted:** `2026-08-03`  
**Effective:** `2026-08-03`  
**Supersedes:** Not applicable.  
**Superseded by:** Not applicable.

## 1. Decision Summary

Active kOA authority contains no unresolved implementation-affecting matter.

Every architectural fact needed to implement, validate, deploy, operate, secure, migrate, recover, or claim conformance has:

- one canonical owner;
- an accepted owner decision when a choice is required;
- exact scope;
- a selected outcome;
- defined defaults and prohibited assumptions;
- defined failure and degradation behavior;
- defined compatibility and migration behavior where applicable;
- requirements and locks;
- tests and evidence;
- an active authority reference.

A missing required decision is represented as `blocked` with reason `missing_owner_decision`.

It is not represented as a permissive default, an inferred convention, an implementation choice, a draft accepted by repetition, or an AI-generated answer.

Explicit runtime uncertainty, epistemic disagreement, stale trust, pending workflow state, or dependency unavailability remains valid when an accepted canonical contract defines how that state is represented and handled.

## 2. Scope

### 2.1 Included scope

- owner decisions and ADRs;
- authority manifests;
- canonical registries and JSON Schemas;
- requirements and Interfile Alignment Locks;
- profiles and overlays;
- component, toolchain, artifact, release, operations, and migration contracts;
- normative and explanatory documents;
- generated projections and AI context packages;
- exceptions and waivers;
- tests, manual controls, evidence, and conformance claims;
- documentation releases and authority activation;
- AI-assisted authoring and implementation derivation.

### 2.2 Excluded scope

This decision does not prohibit:

- explicit runtime `unknown`, `stale`, `unavailable`, `degraded`, `pending`, or `contested` states defined by an accepted contract;
- research alternatives and uncertainty retained as candidate material;
- proposals outside active authority;
- rejected alternatives preserved in ADRs;
- archived historical ambiguity;
- test fixtures that exercise prohibited-marker detection;
- migration records that quote non-authoritative content;
- unresolved scientific or social questions represented without fabricated authority.

### 2.3 Applicability

The decision applies whenever an object can affect:

- implementation;
- authority;
- profile behavior;
- component or data ownership;
- security or privacy;
- privilege;
- AI boundaries;
- release or activation;
- failure or recovery;
- migration or exit;
- validation or conformance.

The decision is non-waivable.

A bounded exception can deviate from an active requirement when the exception policy permits it. It cannot replace a missing architectural decision.

## 3. Canonical References

### 3.1 Owner decision

- `generated/decision-index.json#/decisions/DEC-DOC-002`
- `DEC-DOC-002`

### 3.2 Canonical closure policy

- `generated/decision-index.json#/decision_closure_policy`
- `generated/authority-manifest.json`
- `generated/requirements-index.json#/requirements`
- `generated/assertion-index.json#/locks`
- `generated/exception-index.json#/exceptions`
- `generated/traceability.json#/links`
- `generated/test-catalog.json#/tests`
- `generated/evidence-catalog.json#/evidence`

### 3.3 Related documents

- `DOC-GOV-004` — `00-governance/04-change-protocol.md`
- `DOC-GOV-005` — `00-governance/05-decision-closure-and-prohibited-ambiguity.md`
- `DOC-GOV-007` — `00-governance/07-ai-read-write-protocol.md`
- `DOC-GOV-009` — `00-governance/09-canonical-ownership.md`
- `DOC-GOV-010` — `00-governance/10-interfile-alignment-locks.md`
- `DOC-GOV-011` — `00-governance/11-change-impact-and-versioning.md`
- `DOC-GOV-012` — `00-governance/12-document-lifecycle.md`
- `DOC-GOV-013` — `00-governance/13-validation-pipeline.md`
- `DOC-GOV-015` — `00-governance/15-exceptions-and-waivers.md`
- `DOC-CONST-004` — `01-constitution/04-explicit-authority.md`
- `DOC-CONF-009` — `09-conformance/09-interfile-lock-validation.md`
- `DOC-SEC-000` — `07-security/00-threat-model.md`
- `DOC-SEC-011` — `07-security/11-ai-boundaries.md`

### 3.4 Related requirements

- `REQ-DOC-DEC-001` through `REQ-DOC-DEC-012`

### 3.5 Principal locks

- `LOCK-DOC-011`
- `LOCK-DOC-012`
- `LOCK-DOC-013`
- `LOCK-DOC-014`

### 3.6 Related exceptions

Not applicable.

The prohibition on unresolved active authority is listed as non-waivable authority.

## 4. Context and Problem

### 4.1 Current state

The kOA architecture is intended primarily for deterministic consumption by humans, validators, generators, and AI agents.

The corpus contains many object types and relationships:

- decisions;
- requirements;
- locks;
- profiles;
- components;
- data domains;
- artifacts;
- releases;
- documents;
- tests;
- evidence;
- exceptions;
- migrations;
- authority manifests.

A gap in one object can silently affect many dependent objects.

Examples include:

- a component whose failure behavior is not decided;
- a profile whose overlay compatibility is not closed;
- a data domain without one owner;
- a release without rollback behavior;
- a privileged operation without an authority owner;
- a generated projection with a missing canonical source;
- a conformance claim without current evidence;
- a proposal referenced as if accepted;
- an AI agent filling a missing architecture choice from convention.

### 4.2 Problem statement

A conventional documentation process can leave gaps visible as notes, pending choices, ambiguous defaults, contradictory prose, or implicit implementation decisions.

That approach is unsafe for kOA because downstream systems can:

- implement different assumptions;
- expand authority;
- collapse component boundaries;
- expose data;
- activate incompatible artifacts;
- create false conformance claims;
- hide migration risk;
- make recovery impossible;
- turn AI-generated guesses into apparent policy.

The architecture needs a global decision that makes unresolved implementation-affecting authority impossible to activate.

### 4.3 Why a decision is required

The rule changes the meaning of:

- active;
- accepted;
- valid;
- conformant;
- release ready;
- migration complete;
- authority activated.

It also defines:

- fail-closed behavior;
- AI authoring constraints;
- exception boundaries;
- decision and activation separation;
- full-graph validation;
- rollback to a complete authority state.

This is a major authority-order decision and requires an ADR.

### 4.4 Distinguishing uncertainty from missing authority

kOA can represent uncertainty.

It cannot leave the behavior for uncertainty undecided.

| Case | Valid explicit representation | Invalid authority gap |
| --- | --- | --- |
| Runtime fact not yet observed | Valid explicit representation | Invalid authority gap | An absent architectural rule for how the runtime handles the state. |
| Epistemic disagreement | Valid explicit representation | Invalid authority gap | No owner for recognition, query visibility, or conflict handling. |
| Pending workflow result | Valid explicit representation | Invalid authority gap | An undefined transition or unowned decision. |
| Offline freshness uncertainty | Valid explicit representation | Invalid authority gap | Assuming current authority while freshness is unknown. |
| External dependency unavailable | Valid explicit representation | Invalid authority gap | An unspecified fallback or silent authority expansion. |
| Research alternative | Valid explicit representation | Invalid authority gap | Treating the candidate as accepted authority. |

### 4.5 Threat model

Unresolved active authority creates risks including:

- fabricated authority;
- permissive fallback;
- inconsistent implementation;
- silent profile promotion;
- duplicate ownership;
- cross-component writes;
- AI overreach;
- incomplete release activation;
- unsafe migration;
- incomplete backup or recovery;
- false assurance and conformance;
- operator dependence and exit lock-in.

## 5. Decision Drivers

1. Prevent authority fabrication and silent permissive defaults.
2. Give humans, validators, and AI agents one deterministic response to missing authority.
3. Keep canonical ownership unique.
4. Ensure active objects depend only on accepted decisions.
5. Separate proposal, acceptance, validation, and activation.
6. Preserve explicit uncertainty without confusing it with architectural omission.
7. Require complete impact, tests, evidence, migration, and rollback.
8. Keep exceptions separate from decision closure.
9. Preserve prior complete authority during candidate failure.
10. Support offline deterministic validation and reproducible authority releases.

## 6. Considered Options

### 6.1 Option A — Block Every Unresolved Implementation-Affecting Matter

**Description**

Keep unresolved proposals outside active authority. Require accepted owner decisions, canonical representation, complete impact, validation, evidence, and authority activation last.

A missing required decision returns `blocked`.

**Advantages**

- Prevents implicit and fabricated authority.
- Produces deterministic behavior for humans, tools, and AI agents.
- Preserves one canonical owner.
- Makes partial authority releases invalid.
- Supports precise diagnostics and remediation.
- Preserves runtime uncertainty through explicit state models.
- Keeps exceptions bounded and distinct.

**Disadvantages and costs**

- More decisions and impact reports are required.
- Work can remain blocked while owners resolve choices.
- Validators and registries require more structure.
- Migration from informal deprecated documents requires explicit classification.
- Small implementation choices need careful scope analysis.

**Constraint fit**

This option directly implements `DEC-DOC-002` and `LOCK-DOC-011` through `LOCK-DOC-014`.

### 6.2 Option B — Permit Active Placeholder States with Warnings

**Description**

Allow active objects to contain pending decisions or placeholder values while emitting warnings.

**Advantages**

- Faster apparent document completion.
- Fewer blocked changes.
- Allows implementation to proceed before governance catches up.

**Disadvantages and costs**

- Warnings become de facto defaults.
- Different implementers choose different behavior.
- AI agents can normalize incomplete authority.
- Conformance and release claims become misleading.
- Partial authority can activate.
- Later closure can require incompatible migration.

**Reason rejected**

A warning cannot support active authority.

An implementation-affecting gap is a blocking condition.

### 6.3 Option C — Infer Missing Decisions from Existing Implementation

**Description**

Treat current code, deployed behavior, package choices, or operational convention as the implied decision.

**Advantages**

- Aligns documentation quickly with observed implementation.
- Reduces formal decision work.

**Disadvantages and costs**

- Reverses authority order.
- Converts accidental behavior into architecture.
- Hides profile and environment differences.
- Makes insecure or transitional behavior normative.
- Prevents clear ownership and rationale.
- Undermines migration and rollback.

**Reason rejected**

Implementation is evidence and a conformance target.

It is not automatic architectural authority.

### 6.4 Option D — Allow AI Agents to Choose Low-Risk Defaults

**Description**

Permit AI agents to resolve missing decisions when the agent estimates low impact.

**Advantages**

- High authoring throughput.
- Fewer human review interruptions.
- Consistent formatting and likely defaults.

**Disadvantages and costs**

- Risk estimates are not owner authority.
- The agent can miss transitive impact.
- Repeated generated choices can look canonical.
- Sensitive defaults can expand privilege, disclosure, or dependency.
- Accountability and recourse become unclear.

**Reason rejected**

AI can identify, draft, compare, and validate candidate decisions.

It cannot accept or activate missing authority.

## 7. Decision

### 7.1 Selected option

`Option A — Block Every Unresolved Implementation-Affecting Matter`

### 7.2 Normative effect

`DEC-DOC-002` confirms that:

- active authority contains no unresolved implementation-affecting matter;
- only accepted owner decisions support active authority;
- missing owner decisions block dependent objects;
- decision acceptance and authority activation are separate;
- major decisions have ADRs and impact reports;
- conflicts require an explicit superseding decision;
- prohibited unresolved markers are absent from active authority;
- exceptions cannot replace decision closure;
- AI agents report missing authority and do not infer it;
- authority activation occurs after complete validation.

### 7.3 Required behavior

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

### 7.4 Authority-object closure

| Authority object | Closure conditions | Blocking conditions |
| --- | --- | --- |
| Owner decisions | Closure conditions | Blocking conditions | Proposed or missing decision; contradictory accepted outcomes; absent owner or scope. |
| Requirements | Closure conditions | Blocking conditions | Freehand requirement, missing source decision, undefined profile applicability, or stale projection. |
| Interfile Alignment Locks | Closure conditions | Blocking conditions | Prose-only lock, unresolved canonical reference, missing assertion, or inactive owner decision. |
| Profiles and overlays | Closure conditions | Blocking conditions | Implicit inheritance, package-presence activation, unsupported composition, or missing profile owner. |
| Components and data domains | Closure conditions | Blocking conditions | Duplicate ownership, direct cross-component writes, inferred component membership, or undefined mutation path. |
| Artifacts, releases, and Release Sets | Closure conditions | Blocking conditions | Filename-based identity, publication treated as activation, unknown compatibility, or missing rollback behavior. |
| Exceptions and waivers | Closure conditions | Blocking conditions | Implicit deviation, expired record, wildcard scope, missing evidence, or use to avoid a decision. |
| Tests and evidence | Closure conditions | Blocking conditions | Test definition treated as execution, stale evidence, missing environment identity, or unsupported passing claim. |
| Generated projections and AI contexts | Closure conditions | Blocking conditions | Manual semantic edits, stale generation, proposed authority included as active, or generated output treated as owner. |
| Authority release | Closure conditions | Blocking conditions | Partial activation, mixed authority versions, skipped required phase, or activation before validation. |

### 7.5 Closure dimensions

| Dimension | Closed meaning |
| --- | --- |
| `identity` | A stable non-reused identifier exists and resolves. |
| `owner` | One accountable owner role is named. |
| `scope` | Global, profile, overlay, component, artifact, release, environment, tenant, or migration scope is exact. |
| `selected outcome` | The chosen behavior is explicit rather than inferred from implementation. |
| `canonical owner` | One machine-readable object owns each architectural fact. |
| `status and lifecycle` | The object has a valid current state and valid predecessor or replacement relationships. |
| `defaults` | Default behavior, denial behavior, and inactive behavior are explicit where implementation depends on them. |
| `failure and degradation` | Failure result, safe state, rollback or forward repair, and unaffected capabilities are defined. |
| `compatibility` | Profile, component, artifact, schema, release, and environment compatibility is explicit. |
| `security and privacy` | Authority, identity, data, privilege, evidence, rights, consent, audience, and AI boundaries are closed. |
| `migration and exit` | deprecated disposition, cutover, rollback, export, restore, and identifier preservation are defined where applicable. |
| `validation and evidence` | Applicable tests, manual controls, evidence, exceptions, and claim effects are identified. |
| `activation` | The complete candidate is activated through the Authority Registry only after all required checks pass. |

### 7.6 Validation outcomes

| Outcome | Meaning | Authority effect |
| --- | --- | --- |
| `pass` | All required closure, alignment, validation, and evidence conditions completed successfully. | Authority effect | The candidate can proceed to the next controlled transition. |
| `fail` | A required authoritative assertion is false. | Authority effect | The affected merge, release, migration, conformance, or activation remains prohibited. |
| `blocked` | Required authority, decision, owner, input, dependency, evidence, tool state, or review is missing. | Authority effect | Work proceeds only to resolve the blocking condition. |
| `not_applicable` | The rule does not apply to the exact resolved scope. | Authority effect | The result supports no broader claim. |
| `internal_error` | The validator did not complete reliably. | Authority effect | The run has no authority effect and is repeated after tool repair. |

### 7.7 Prohibited behavior

The selected architecture excludes:

- active placeholder decisions;
- active requirements with missing source decisions;
- contradictory accepted outcomes without supersession;
- inferred owners or scopes;
- proposal status treated as acceptance;
- implementation behavior promoted to architecture automatically;
- exception records used to avoid a decision;
- missing evidence treated as a pass;
- skipped validation treated as a pass;
- internal validator failure treated as a pass;
- generated content treated as canonical owner;
- AI agents silently filling architecture gaps;
- partial or mixed authority activation.

### 7.8 Defaults

- Missing required authority returns `blocked`.
- A false authoritative assertion returns `fail`.
- A validator defect returns `internal_error`.
- Non-applicability is exact and does not broaden a claim.
- No permissive default is inferred.
- The previous complete authority release remains active after candidate failure.
- The Authority Registry changes last.
- Historical and proposed objects remain preserved but inactive.
- Runtime uncertainty is valid only through an accepted explicit state model.

## 8. Canonical Ownership and Authority Graph

### 8.1 Decision Registry

The Decisions Registry owns:

- decision identity;
- state;
- owner;
- scope;
- selected outcome;
- rationale summary;
- affected canonical references;
- semantic change class;
- supersession;
- validation obligations;
- activation eligibility.

An ADR records context and consequences.

It does not replace the decision record as authority pointer.

### 8.2 Authority Registry

The Authority Registry owns:

- active authority release identity;
- exact active registry and schema versions;
- validation order;
- current documentation release;
- generated projections;
- migration and cutover state;
- activation and rollback references.

It activates one complete compatible set.

### 8.3 Requirements, locks, and traceability

The Requirements Registry owns normative statements.

The Locks Registry owns cross-object invariants.

The Traceability Registry owns typed relationships.

A Markdown document can project these objects but cannot define an alternative owner or relationship.

### 8.4 Evidence and conformance

A test definition is not evidence.

A passing claim identifies exact executed evidence for the evaluated source, profile, artifact, environment, release, authority, and exception state.

Stale or unrelated evidence blocks the claim.

### 8.5 AI context

AI context packages contain only accepted active objects applicable to the task.

They exclude:

- proposals;
- rejected decisions;
- superseded current authority;
- archives;
- expired exceptions;
- failing claims;
- unvalidated generated content.

An AI context remains a generated projection.

## 9. Status, Lifecycle, and Activation

### 9.1 Decision lifecycle

A proposal can become:

- accepted;
- rejected;
- archived.

An accepted decision can become:

- deprecated;
- superseded.

A superseded decision remains historical and linked to its replacement.

Only accepted decisions can support a candidate active authority set.

### 9.2 Acceptance and activation

Acceptance means the owner selected an outcome.

Activation means the complete dependent authority graph passed validation and the Authority Registry references the accepted state.

These transitions remain separate.

### 9.3 Active object eligibility

An object is eligible for active authority only when:

1. its schema and references validate;
2. its owner and scope resolve;
3. every required decision is accepted;
4. no conflicting accepted decision remains unresolved;
5. requirements and locks align;
6. impact dispositions are complete;
7. generated projections are current;
8. migration and compatibility obligations pass;
9. required tests and evidence pass;
10. active exceptions are valid;
11. the Authority Registry activates the complete set.

### 9.4 Supersession

Supersession preserves:

- predecessor;
- replacement;
- owner;
- rationale;
- scope;
- compatibility interval;
- migration;
- rollback;
- impact;
- tests;
- evidence;
- historical claims.

A replacement does not erase the meaning of a prior release.

### 9.5 Non-waivable status

No exception or waiver can permit unresolved active authority.

A deviation from an active requirement remains possible only through the separate exception policy and only when the requirement is otherwise defined and the protected invariant is waivable.

## 10. Security, Privacy, Rights, and AI Effects

### 10.1 Authority security

Missing or ambiguous authority fails closed.

Authentication, access, implementation presence, operator habit, or provider capability does not create authorization.

### 10.2 Data and component security

A missing data owner or mutation boundary blocks the affected component or workflow.

It does not create shared ownership or permission for direct database access.

### 10.3 Privacy and rights

Missing classification, audience, consent, attribution, no-AI, withdrawal, export, retention, or cultural-authority behavior does not default to disclosure or use.

The affected transfer, publication, AI operation, backup, restore, or query remains blocked until the owner contract defines the behavior.

### 10.4 AI behavior

AI agents can:

- locate missing authority;
- summarize relevant accepted sources;
- draft a proposal, decision record, ADR, impact report, requirements, locks, tests, and evidence plan;
- compare alternatives;
- identify affected objects;
- validate completeness.

AI agents cannot:

- choose the accepted outcome without owner authority;
- mark their own proposal accepted;
- infer a permissive default;
- activate authority;
- use generated repetition as evidence of acceptance;
- hide the block by rewriting language.

### 10.5 Threat containment

The decision limits:

- policy capture through undocumented defaults;
- privilege expansion;
- data leakage through missing classification;
- release substitution through unclear identity;
- recovery capture;
- AI overreach;
- false conformance;
- migration cutover with missing dependencies.

## 11. Operational and Failure Effects

### 11.1 Blocking behavior

A blocked object identifies:

- object ID and class;
- missing decision, owner, scope, dependency, evidence, or validation phase;
- affected profiles, components, artifacts, releases, environments, and claims;
- safe state;
- remediation owner;
- required next transition.

### 11.2 Previous active authority

A failed candidate does not alter the active authority release.

The previous complete release remains active unless separately revoked or unsafe under an accepted emergency procedure.

### 11.3 Failure modes

| Failure ID | Failure | Safe behavior | Recovery |
| --- | --- | --- | --- |
| `AUTHCLOSE-FAIL-001` | Failure | Safe behavior | Recovery |
| `AUTHCLOSE-FAIL-002` | Failure | Safe behavior | Recovery |
| `AUTHCLOSE-FAIL-003` | Failure | Safe behavior | Recovery |
| `AUTHCLOSE-FAIL-004` | Failure | Safe behavior | Recovery |
| `AUTHCLOSE-FAIL-005` | Failure | Safe behavior | Recovery |
| `AUTHCLOSE-FAIL-006` | Failure | Safe behavior | Recovery |
| `AUTHCLOSE-FAIL-007` | Failure | Safe behavior | Recovery |
| `AUTHCLOSE-FAIL-008` | Failure | Safe behavior | Recovery |
| `AUTHCLOSE-FAIL-009` | Failure | Safe behavior | Recovery |
| `AUTHCLOSE-FAIL-010` | Failure | Safe behavior | Recovery |

### 11.4 Capability-scoped impact

A missing profile-overlay decision can block one overlay claim without invalidating an unrelated primary profile.

A missing global authority-order decision can block the complete authority release because its declared scope is global.

The validator computes scope from canonical relationships rather than file proximity.

### 11.5 Incident response

When active authority is found to contain an unresolved or fabricated decision:

1. stop affected activation and publication;
2. preserve the active and candidate authority identities;
3. identify affected objects and environments;
4. isolate unsafe capabilities;
5. restore a prior complete authority state when required;
6. create the owner decision and impact report;
7. migrate or forward repair affected state;
8. rerun complete validation;
9. activate authority last;
10. preserve incident evidence.

## 12. Compatibility and Lifecycle

### 12.1 Compatibility class

`global_foundational`

Every active profile, component, artifact, release, operation, migration, and conformance claim remains compatible only when required authority is closed.

### 12.2 Affected release channels

- `system`
- `services`
- `governance`
- `knowledge`
- documentation authority release

The decision does not merge these channels.

It prevents activation of a channel selection whose required authority is unresolved.

### 12.3 Backward compatibility

Existing accepted decisions and active authority remain valid when they already meet closure and traceability requirements.

deprecated informal decisions require migration into canonical records before they can support the active corpus.

### 12.4 Schema and tool compatibility

Validators, generators, and registries treat unknown required fields, assertion types, decision states, or object classes as blocked or incompatible rather than permissive.

Release-grade validation uses local schemas and locked tool identities.

### 12.5 Retirement

A decision, requirement, lock, profile, component, artifact, or document can retire only through its declared lifecycle.

Retirement preserves identifier reservation and historical references.

## 13. Migration Plan

### 13.1 Preconditions

- `DEC-DOC-002` is accepted.
- the Decisions Registry and decision schema exist;
- the Authority Registry defines activation order;
- requirements, locks, documentation, traceability, exceptions, tests, and evidence registries exist;
- the active documentation root is `docs/`;
- non-authoritative sources remain migration-only.

### 13.2 Migration steps

1. Inventory every active object and implementation-affecting statement.
2. identify missing decisions, owners, scopes, defaults, failures, compatibility, migration, validation, and evidence.
3. classify each issue as a proposal, accepted decision, rejected alternative, explicit runtime uncertainty, migration evidence, archive content, or invalid active gap.
4. create stable decision IDs and accountable owners for every required choice.
5. accept or reject every implementation-affecting proposal.
6. create ADRs for major changes.
7. update canonical registries and schemas.
8. update requirements, locks, profiles, components, artifacts, and lifecycle contracts.
9. compute direct and transitive impact.
10. migrate explanatory documents and generated projections.
11. update tests, evidence, exceptions, and AI contexts.
12. validate the complete candidate corpus.
13. activate the new authority release last.
14. archive deprecated ambiguity with lineage and redirects.

### 13.3 deprecated disposition

removed source files can retain:

- undecided discussion;
- obsolete alternatives;
- incomplete design notes;
- quoted marker tokens;
- historical contradictions.

They remain outside active authority.

No active document or registry depends on a deprecated unresolved outcome.

### 13.4 Cutover rule

The cutover manifest proves:

- one active documentation corpus;
- every active object has a final disposition;
- required decisions are accepted;
- no unresolved active authority remains;
- generated projections are current;
- required tests and evidence pass;
- rollback restores one complete prior authority release.

## 14. Rollback and Forward Repair

### 14.1 Rollback trigger

Rollback is required when a candidate authority release contains:

- a missing owner decision;
- conflicting accepted decisions;
- undefined owner or scope;
- an active prohibited unresolved marker;
- a proposal referenced as current authority;
- an invalid exception used to avoid closure;
- stale generated authority;
- incomplete impact, migration, test, or evidence;
- a validator internal error in a required phase;
- partial Authority Registry activation.

### 14.2 Rollback unit

The rollback unit is the complete previous authority release, including:

- authority registry;
- decisions;
- requirements;
- locks;
- documentation;
- profiles;
- components;
- schemas;
- artifacts and release references;
- traceability;
- exceptions;
- tests;
- evidence;
- generated projections;
- AI contexts;
- migration and cutover records.

A mixture of versions is not a valid rollback unit.

### 14.3 Rollback procedure

1. Freeze the failed candidate.
2. preserve diagnostics and evidence.
3. restore the previous complete authority release.
4. regenerate projections from the restored canonical sources.
5. validate the restored state read only.
6. verify dependent environments and claims reference the restored authority.
7. record rollback evidence.

### 14.4 Forward repair

Forward repair is used when runtime, migration, or published external effects already depend on the candidate and direct rollback would create a less coherent state.

The repair requires:

- an accepted owner decision;
- exact affected scope;
- migration and compatibility plan;
- tests and evidence;
- no permissive interim authority;
- activation of one complete repaired authority state.

### 14.5 Last known valid state

- Authority release: `generated/authority-manifest.json#/active_authority_release`
- Decision closure policy: `generated/decision-index.json#/decision_closure_policy`
- Validation evidence: exact evidence records referenced by the active authority manifest

## 15. Interfile Alignment Impact

### 15.1 Impact report

- `generated/impact/IMPACT-2026-08-03-DEC-DOC-002.json`

### 15.2 Modified or confirmed canonical references

- `generated/decision-index.json#/decisions/DEC-DOC-002`
- `generated/decision-index.json#/decision_closure_policy`
- `generated/authority-manifest.json`
- `generated/requirements-index.json#/requirements/REQ-DOC-DEC-001`
- `generated/requirements-index.json#/requirements/REQ-DOC-DEC-012`
- `generated/assertion-index.json#/locks/LOCK-DOC-011`
- `generated/assertion-index.json#/locks/LOCK-DOC-014`
- `generated/decision-index.json#/adrs/ADR-026`

### 15.3 Affected documents

| Document ID | Disposition | Reason |
| --- | --- | --- |
| `DOC-GOV-004` | `reviewed_no_change` | The change protocol continues to require accepted decisions and complete impact before activation. |
| `DOC-GOV-005` | `confirmed_canonical_policy` | Owns decision closure, prohibited ambiguity, decision lifecycle, and missing-decision behavior. |
| `DOC-GOV-007` | `reviewed_no_change` | AI agents continue to report missing authority rather than infer it. |
| `DOC-GOV-009` | `reviewed_no_change` | Canonical ownership remains a prerequisite for closure. |
| `DOC-GOV-010` | `reviewed_no_change` | The four principal decision-closure locks remain active. |
| `DOC-GOV-011` | `reviewed_no_change` | Impact analysis and semantic versioning remain part of closure. |
| `DOC-GOV-012` | `reviewed_no_change` | Inactive, superseded, and archived objects remain outside current authority. |
| `DOC-GOV-013` | `reviewed_no_change` | Validation remains fail-closed and authority activation remains last. |
| `DOC-GOV-015` | `confirmed_non_waivable` | Decision closure and prohibition on unresolved active authority remain non-waivable. |
| `DOC-CONST-004` | `reviewed_no_change` | Explicit authority continues to block fabricated or inferred authority. |
| `DOC-CONF-009` | `reviewed_no_change` | Interfile lock validation continues to distinguish fail, blocked, not-applicable, and internal error. |
| `DOC-SEC-000` | `reviewed_no_change` | Missing or ambiguous authority remains a security threat and fail-closed condition. |
| `DOC-SEC-011` | `reviewed_no_change` | AI remains unable to fill authority gaps or mutate active authority directly. |
| `DOC-ADR-026` | `introduced` | Records context, alternatives, rationale, consequences, migration, and historical integrity for `DEC-DOC-002`. |

### 15.4 Affected locks

| Lock ID | Disposition | Validation effect |
| --- | --- | --- |
| `LOCK-DOC-011` | `confirmed_active` | Active architectural authority contains no undecided implementation-affecting matter. |
| `LOCK-DOC-012` | `confirmed_active` | Every implementation-affecting proposal is accepted or rejected before activation. |
| `LOCK-DOC-013` | `confirmed_active` | An object with a missing required owner decision remains inactive. |
| `LOCK-DOC-014` | `confirmed_active` | AI agents cannot replace missing authority with inferred decisions. |
| `LOCK-DOC-001` | `reviewed_no_change` | Canonical ownership remains unique. |
| `LOCK-DOC-003` | `reviewed_no_change` | Markdown and ADRs remain projections rather than registry-value owners. |
| `LOCK-DOC-015` | `reviewed_no_change` | Scope alignment remains explicit across global, profile, component, artifact, and migration layers. |
| `LOCK-DOC-016` | `reviewed_no_change` | Traceability remains complete for active claims. |
| `LOCK-AUTH-001` | `reviewed_no_change` | Authority remains explicit and operation bound. |
| `LOCK-PROFILE-001` | `reviewed_no_change` | Profile-specific decisions cannot be inferred as global. |
| `LOCK-COMP-001` | `reviewed_no_change` | Component boundaries cannot be inferred or silently collapsed. |
| `LOCK-DATA-001` | `reviewed_no_change` | Authoritative data ownership remains explicit. |
| `LOCK-AI-002` | `reviewed_no_change` | External AI output remains candidate material without authority. |
| `LOCK-LIFE-004` | `reviewed_no_change` | Authority activation and artifact activation remain complete controlled transitions. |

### 15.5 Affected requirements

| Requirement ID | Disposition | Validation effect |
| --- | --- | --- |
| `REQ-DOC-DEC-001` | `confirmed_active` | The existing decision-closure requirement remains owned by `generated/requirements-index.json` and projected by this ADR. |
| `REQ-DOC-DEC-002` | `confirmed_active` | The existing decision-closure requirement remains owned by `generated/requirements-index.json` and projected by this ADR. |
| `REQ-DOC-DEC-003` | `confirmed_active` | The existing decision-closure requirement remains owned by `generated/requirements-index.json` and projected by this ADR. |
| `REQ-DOC-DEC-004` | `confirmed_active` | The existing decision-closure requirement remains owned by `generated/requirements-index.json` and projected by this ADR. |
| `REQ-DOC-DEC-005` | `confirmed_active` | The existing decision-closure requirement remains owned by `generated/requirements-index.json` and projected by this ADR. |
| `REQ-DOC-DEC-006` | `confirmed_active` | The existing decision-closure requirement remains owned by `generated/requirements-index.json` and projected by this ADR. |
| `REQ-DOC-DEC-007` | `confirmed_active` | The existing decision-closure requirement remains owned by `generated/requirements-index.json` and projected by this ADR. |
| `REQ-DOC-DEC-008` | `confirmed_active` | The existing decision-closure requirement remains owned by `generated/requirements-index.json` and projected by this ADR. |
| `REQ-DOC-DEC-009` | `confirmed_active` | The existing decision-closure requirement remains owned by `generated/requirements-index.json` and projected by this ADR. |
| `REQ-DOC-DEC-010` | `confirmed_active` | The existing decision-closure requirement remains owned by `generated/requirements-index.json` and projected by this ADR. |
| `REQ-DOC-DEC-011` | `confirmed_active` | The existing decision-closure requirement remains owned by `generated/requirements-index.json` and projected by this ADR. |
| `REQ-DOC-DEC-012` | `confirmed_active` | The existing decision-closure requirement remains owned by `generated/requirements-index.json` and projected by this ADR. |

### 15.6 Generated artifacts

Regeneration includes:

- documentation metadata;
- decision and ADR indexes;
- requirement projections;
- lock projections;
- traceability graph;
- decision-closure report;
- unresolved-marker report;
- impact report;
- conformance matrix;
- active AI context packages;
- documentation release manifest;
- authority manifest.

## 16. Validation and Evidence

### 16.1 Required tests

| Test ID | Purpose | Required result |
| --- | --- | --- |
| `TEST-DOC-DEC-001` | Proposed decisions cannot support active requirements | `pass` |
| `TEST-DOC-DEC-002` | Missing decisions block active profiles | `pass` |
| `TEST-DOC-DEC-003` | Conflicting accepted decisions are detected | `pass` |
| `TEST-DOC-DEC-004` | Prohibited unresolved markers are detected | `pass` |
| `TEST-DOC-DEC-005` | Ambiguous decision scope is rejected | `pass` |
| `TEST-DOC-DEC-006` | Decision supersession links are complete | `pass` |
| `TEST-DOC-DEC-007` | Validation precedes authority activation | `pass` |
| `TEST-DOC-DEC-008` | AI contexts exclude proposals | `pass` |
| `TEST-DOC-DEC-009` | Historical quotations do not create false positives | `pass` |
| `TEST-DOC-DEC-010` | Missing decisions produce blocked machine output | `pass` |
| `TEST-DOC-VAL-001` | JSON syntax is valid | `pass` |
| `TEST-DOC-VAL-002` | Schema conformance succeeds | `pass` |
| `TEST-DOC-VAL-003` | Canonical references resolve | `pass` |
| `TEST-DOC-VAL-004` | Stable identifiers are unique | `pass` |
| `TEST-DOC-VAL-005` | Canonical ownership is exclusive | `pass` |
| `TEST-DOC-VAL-006` | Decision references are accepted | `pass` |
| `TEST-DOC-VAL-007` | Alignment lock references are active | `pass` |
| `TEST-DOC-VAL-008` | Required document sections exist | `pass` |
| `TEST-DOC-VAL-009` | Active documentation is English | `pass` |
| `TEST-DOC-VAL-010` | Unresolved authority markers are absent | `pass` |
| `TEST-DOC-VAL-011` | Only one active documentation corpus exists | `pass` |
| `TEST-DOC-VAL-012` | Generated content is reproducible | `pass` |
| `TEST-DOC-VAL-013` | Documentation dependency graph is acyclic | `pass` |
| `TEST-DOC-VAL-014` | Document class and path agree | `pass` |
| `TEST-DOC-VAL-015` | Remote schema references are rejected | `pass` |
| `TEST-DOC-VAL-016` | Traceability is complete | `pass` |
| `TEST-DOC-VAL-017` | Authority activation occurs last | `pass` |
| `TEST-DOC-VAL-018` | Validation uses a clean repository state | `pass` |
| `TEST-DOC-VAL-019` | Registry and schema versions are compatible | `pass` |
| `TEST-DOC-VAL-020` | Validation performs no semantic auto-fix | `pass` |
| `TEST-AI-DOC-001` | AI task classification requires explicit scope | `pass` |
| `TEST-AI-DOC-002` | Stale AI context packages are rejected | `pass` |
| `TEST-AI-DOC-003` | Missing decisions block AI semantic writes | `pass` |
| `TEST-AI-DOC-004` | Markdown-only canonical changes are rejected | `pass` |
| `TEST-AI-DOC-005` | Manual edits to generated files are rejected | `pass` |
| `TEST-AI-DOC-006` | Profile rules are not generalized | `pass` |
| `TEST-AI-DOC-007` | Claimed validation requires execution evidence | `pass` |
| `TEST-AI-DOC-008` | Change summaries contain applicable identifiers | `pass` |
| `TEST-AI-DOC-009` | Retired identifiers are not reused | `pass` |
| `TEST-AI-DOC-010` | Conflicting sources block dependent output | `pass` |
| `TEST-MIG-009` | Authority registry activation occurs last | `pass` |
| `TEST-MIG-012` | Rollback restores a complete authority state | `pass` |
| `TEST-MIG-013` | Failed cutover evidence is retained | `pass` |
| `TEST-SYS-004` | Authority fails closed | `pass` |
| `TEST-SEC-001` | Arbitrary privileged commands are rejected | `pass` |
| `TEST-SEC-002` | Privileged operation schemas are enforced | `pass` |
| `TEST-SEC-003` | Policy binding and replay protection succeed | `pass` |
| `TEST-SEC-004` | Break-glass authority expires | `pass` |
| `TEST-SEC-005` | Unknown policy facts fail closed | `pass` |
| `TEST-SEC-006` | Separation of duties is enforced | `pass` |
| `TEST-CROSS-007` | Node Agent rejects arbitrary privileged execution | `pass` |
| `TEST-CROSS-008` | Policy decision precedes governed privilege | `pass` |
| `TEST-CROSS-009` | Audit Broker does not become an authorization engine | `pass` |
| `TEST-CROSS-013` | External AI cannot directly mutate authority | `pass` |
| `TEST-CROSS-014` | Identity layers remain distinct | `pass` |
| `TEST-CROSS-015` | All cross-component mutations are contract-bound | `pass` |
| `TEST-LIFE-003` | Artifact verification precedes activation | `pass` |
| `TEST-LIFE-004` | Activation is atomic for the artifact class | `pass` |
| `TEST-LIFE-012` | Policy bundles activate independently | `pass` |
| `TEST-OPS-004` | Backup completes with evidence | `pass` |
| `TEST-OPS-007` | Incident response preserves authority boundaries | `pass` |
| `TEST-EXIT-002` | Export is independently verifiable | `pass` |
| `TEST-EXIT-003` | Clean restore succeeds | `pass` |
| `TEST-EXIT-006` | Exit does not require a single operator | `pass` |

### 16.2 Required evidence

| Evidence ID | Evidence type | Location |
| --- | --- | --- |
| `EVID-ADR-026-DECISION` | Accepted owner decision and activation eligibility | `generated/evidence-catalog.json#/evidence/EVID-ADR-026-DECISION` |
| `EVID-ADR-026-CLOSURE` | Complete active-object decision-closure report | `generated/evidence-catalog.json#/evidence/EVID-ADR-026-CLOSURE` |
| `EVID-ADR-026-MARKERS` | Syntax-aware active unresolved-marker scan | `generated/evidence-catalog.json#/evidence/EVID-ADR-026-MARKERS` |
| `EVID-ADR-026-LOCKS` | Interfile lock evaluation for closure locks | `generated/evidence-catalog.json#/evidence/EVID-ADR-026-LOCKS` |
| `EVID-ADR-026-IMPACT` | Complete transitive impact and disposition report | `generated/evidence-catalog.json#/evidence/EVID-ADR-026-IMPACT` |
| `EVID-ADR-026-AI` | AI authoring and context exclusion tests | `generated/evidence-catalog.json#/evidence/EVID-ADR-026-AI` |
| `EVID-ADR-026-MIGRATION` | deprecated ambiguity classification and cutover coverage | `generated/evidence-catalog.json#/evidence/EVID-ADR-026-MIGRATION` |
| `EVID-ADR-026-ROLLBACK` | Complete authority-state rollback test | `generated/evidence-catalog.json#/evidence/EVID-ADR-026-ROLLBACK` |
| `EVID-ADR-026-DOCS` | Documentation, schema, generated, traceability, and clean-tree validation | `generated/evidence-catalog.json#/evidence/EVID-ADR-026-DOCS` |

### 16.3 Required validation commands

```bash
python docs/tools/generate_docs.py --check
python docs/tools/check_normative_language.py
python docs/tools/check_language.py
python docs/tools/check_canonical_ownership.py
python docs/tools/check_decision_closure.py
python docs/tools/check_no_unresolved_state.py
python docs/tools/check_interfile_locks.py
python docs/tools/check_document_graph.py
python docs/tools/check_generated_content.py
python docs/tools/check_traceability.py
python docs/tools/compute_impact.py --check-clean
python docs/tools/build_ai_context.py --check
python docs/tools/check_clean_repository.py
python docs/tools/validate_docs.py
```

### 16.4 Decision-specific validation

- validate every active object against its schema;
- validate every required decision reference and accepted state;
- validate one owner and exact scope;
- validate selected outcome, defaults, failure, compatibility, migration, and validation behavior;
- validate the four principal decision-closure locks;
- validate syntax-aware exclusion of active unresolved markers;
- validate that proposals, archives, rejected decisions, and superseded authority do not support active claims;
- validate that explicit runtime uncertainty has an accepted owner contract;
- validate that exceptions do not replace decision closure;
- validate that AI contexts exclude inactive and unresolved authority;
- validate complete impact dispositions;
- validate exact tests and evidence;
- validate rollback to one complete authority release;
- validate Authority Registry activation last.

### 16.5 Acceptance criteria

1. `DEC-DOC-002` is accepted.
2. Every active implementation-affecting object resolves to accepted owner decisions.
3. Every accepted decision has owner, scope, outcome, impact, validation, and activation state.
4. No conflicting accepted decisions remain in the same active scope.
5. Missing decisions return `blocked` with `missing_owner_decision`.
6. No prohibited unresolved marker appears as active status, normative content, or generated authority.
7. Runtime uncertainty is represented by accepted explicit state behavior.
8. No exception suppresses a missing decision.
9. AI agents and AI contexts cannot fill or conceal authority gaps.
10. Every active claim has complete lock, test, evidence, and traceability support.
11. Failed candidates preserve the prior complete authority release.
12. Every required validation completes successfully.
13. Authority activation occurs last.

## 17. Consequences

### 17.1 Positive consequences

- Active architecture is deterministic and implementable.
- Missing authority is visible and machine actionable.
- AI agents cannot turn guesses into policy.
- Canonical ownership remains stable.
- Profiles, components, data, artifacts, and releases have explicit boundaries.
- Conformance claims become evidence backed.
- Runtime uncertainty can remain honest without becoming an architecture gap.
- Migration and rollback operate on complete authority states.
- Historical proposals and alternatives remain preserved without contaminating current authority.
- Operators receive clear safe behavior during incomplete changes.

### 17.2 Negative consequences and costs

- More work becomes blocked pending owner decisions.
- Decision, ADR, impact, traceability, test, and evidence maintenance increases.
- deprecated migration requires explicit classification of many ambiguous statements.
- Validators need syntax-aware context handling.
- Owners need to distinguish architecture choices from implementation details.
- Major changes take longer because activation waits for complete graph closure.
- Experimental implementations cannot claim active authority before review.

### 17.3 Operational obligations

- Monitor blocked decision and evidence states.
- Assign accountable owners promptly.
- Keep the previous complete authority release restorable.
- Validate AI contexts and generated projections.
- Review exception misuse.
- Exercise authority rollback.
- Expose blocking diagnostics without leaking protected content.
- Preserve decision and supersession history.

### 17.4 Documentation obligations

- Register every active document.
- Declare dependencies and scope.
- Keep normative statements in registered generated requirement blocks.
- Use canonical references.
- Keep proposals and archives outside active authority.
- Generate decision, requirement, lock, traceability, impact, conformance, and AI-context projections.
- Preserve stable identifiers and redirects.
- Recompute impact after closure-policy changes.

### 17.5 Technical debt explicitly accepted

The decision accepts governance and validation complexity to prevent implicit architecture.

The debt is reduced through deterministic registries, generators, diagnostics, and templates rather than through permissive unresolved authority.

## 18. Rejected Alternatives

| Alternative | Reason rejected | Reconsideration trigger |
| --- | --- | --- |
| Active placeholders with warnings | Warnings become de facto defaults and can support false active claims. | None while active authority remains deterministic. |
| Implementation as implicit authority | Reverses authority order and normalizes accidental or transitional behavior. | A specific implementation is adopted through an accepted owner decision and contract. |
| AI-selected low-risk defaults | AI risk estimates do not provide accountable authority or complete impact knowledge. | An explicit authority mechanism records a competent owner's accepted decision. |
| Exceptions for missing decisions | An exception requires an existing active requirement and cannot define missing architecture. | None; this invariant is non-waivable. |
| Partial authority activation | Produces mixed versions and undefined compatibility. | None; activation remains atomic at the authority-release level. |
| Informal human consensus | Meetings and conversations lack stable scope, owner, migration, tests, evidence, and activation. | Consensus is recorded as an accepted canonical decision. |

Rejected alternatives remain historical rationale and have no active authority.

## 19. Exceptions and Waivers

Not applicable.

The following are distinct and remain valid:

- a bounded exception from an active waivable requirement;
- a runtime unknown state defined by an accepted contract;
- a contested epistemic state;
- a pending workflow state;
- a proposal outside active authority;
- historical ambiguous source material in the archive.

None of these allows an implementation-affecting active authority gap.

A requested semantic deviation from this decision requires a superseding accepted global decision and ADR rather than an exception.

## 20. Implementation Guidance

This section is non-normative.

A decision-closure validator can:

1. load active canonical registries locally;
2. enumerate every active object;
3. resolve required decisions;
4. verify accepted state, owner, scope, and selected outcome;
5. verify canonical ownership;
6. verify requirements, locks, profiles, components, artifacts, releases, exceptions, tests, and evidence;
7. scan active fields and normative projections using syntax-aware contexts;
8. distinguish explicit runtime uncertainty from missing architecture;
9. compute direct and transitive affected objects;
10. assign `pass`, `fail`, `blocked`, `not_applicable`, or `internal_error`;
11. emit deterministic diagnostics;
12. block unsupported claims;
13. preserve the previous authority release;
14. activate the candidate Authority Registry last.

A diagnostic can contain:

```text
diagnostic_id
outcome
reason_code
object_id
object_class
path
json_pointer
required_decision_id
owner
scope
affected_claims
canonical_references
remediation_class
```

The validator reads authority.

It does not decide architecture or rewrite canonical meaning.

## 21. Decision Record

### 21.1 Decision authority record

- Decision ID: `DEC-DOC-002`
- Decision status: `accepted`
- Decision owner: `owner:documentation-architecture`
- Decision registry reference: `generated/decision-index.json#/decisions/DEC-DOC-002`

### 21.2 Review record

| Role | Identifier | Result | Date |
| --- | --- | --- | --- |
| Author | `actor:documentation-generation` | `submitted` | `2026-08-03` |
| Canonical owner | `owner:documentation-architecture` | `approved` | `2026-08-03` |
| Authority reviewer | `owner:authority-architecture` | `approved` | `2026-08-03` |
| Security reviewer | `owner:security-architecture` | `approved` | `2026-08-03` |
| Validation pipeline | `automated` | `pass` | `2026-08-03` |
| Authority activator | `authority:documentation-release` | `activated` | `2026-08-03` |

### 21.3 Machine-readable change summary

```json
{
  "change_id": "CHG-2026-0026",
  "decision_ids": [
    "DEC-DOC-002"
  ],
  "modified_or_confirmed_canonical_refs": [
    "generated/decision-index.json#/decisions/DEC-DOC-002",
    "generated/decision-index.json#/decision_closure_policy",
    "generated/authority-manifest.json",
    "generated/requirements-index.json#/requirements/REQ-DOC-DEC-001",
    "generated/requirements-index.json#/requirements/REQ-DOC-DEC-012",
    "generated/assertion-index.json#/locks/LOCK-DOC-011",
    "generated/assertion-index.json#/locks/LOCK-DOC-014",
    "generated/decision-index.json#/adrs/ADR-026"
  ],
  "affected_document_ids": [
    "DOC-GOV-004",
    "DOC-GOV-005",
    "DOC-GOV-007",
    "DOC-GOV-009",
    "DOC-GOV-010",
    "DOC-GOV-011",
    "DOC-GOV-012",
    "DOC-GOV-013",
    "DOC-GOV-015",
    "DOC-CONST-004",
    "DOC-CONF-009",
    "DOC-SEC-000",
    "DOC-SEC-011",
    "DOC-ADR-026"
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
  "principal_lock_ids": [
    "LOCK-DOC-011",
    "LOCK-DOC-012",
    "LOCK-DOC-013",
    "LOCK-DOC-014"
  ],
  "exception_ids": [],
  "adr_ids": [
    "ADR-026"
  ],
  "test_ids": [
    "TEST-DOC-DEC-001",
    "TEST-DOC-DEC-002",
    "TEST-DOC-DEC-003",
    "TEST-DOC-DEC-004",
    "TEST-DOC-DEC-005",
    "TEST-DOC-DEC-006",
    "TEST-DOC-DEC-007",
    "TEST-DOC-DEC-008",
    "TEST-DOC-DEC-009",
    "TEST-DOC-DEC-010",
    "TEST-DOC-VAL-001",
    "TEST-DOC-VAL-002",
    "TEST-DOC-VAL-003",
    "TEST-DOC-VAL-004",
    "TEST-DOC-VAL-005",
    "TEST-DOC-VAL-006",
    "TEST-DOC-VAL-007",
    "TEST-DOC-VAL-008",
    "TEST-DOC-VAL-009",
    "TEST-DOC-VAL-010",
    "TEST-DOC-VAL-011",
    "TEST-DOC-VAL-012",
    "TEST-DOC-VAL-013",
    "TEST-DOC-VAL-014",
    "TEST-DOC-VAL-015",
    "TEST-DOC-VAL-016",
    "TEST-DOC-VAL-017",
    "TEST-DOC-VAL-018",
    "TEST-DOC-VAL-019",
    "TEST-DOC-VAL-020",
    "TEST-AI-DOC-001",
    "TEST-AI-DOC-002",
    "TEST-AI-DOC-003",
    "TEST-AI-DOC-004",
    "TEST-AI-DOC-005",
    "TEST-AI-DOC-006",
    "TEST-AI-DOC-007",
    "TEST-AI-DOC-008",
    "TEST-AI-DOC-009",
    "TEST-AI-DOC-010",
    "TEST-MIG-009",
    "TEST-MIG-012",
    "TEST-MIG-013",
    "TEST-SYS-004",
    "TEST-SEC-001",
    "TEST-SEC-002",
    "TEST-SEC-003",
    "TEST-SEC-004",
    "TEST-SEC-005",
    "TEST-SEC-006",
    "TEST-CROSS-007",
    "TEST-CROSS-008",
    "TEST-CROSS-009",
    "TEST-CROSS-013",
    "TEST-CROSS-014",
    "TEST-CROSS-015",
    "TEST-LIFE-003",
    "TEST-LIFE-004",
    "TEST-LIFE-012",
    "TEST-OPS-004",
    "TEST-OPS-007",
    "TEST-EXIT-002",
    "TEST-EXIT-003",
    "TEST-EXIT-006"
],
  "evidence_ids": [
    "EVID-ADR-026-DECISION",
    "EVID-ADR-026-CLOSURE",
    "EVID-ADR-026-MARKERS",
    "EVID-ADR-026-LOCKS",
    "EVID-ADR-026-IMPACT",
    "EVID-ADR-026-AI",
    "EVID-ADR-026-MIGRATION",
    "EVID-ADR-026-ROLLBACK",
    "EVID-ADR-026-DOCS"
  ],
  "impact_report": "generated/impact/IMPACT-2026-08-03-DEC-DOC-002.json",
  "validation_status": "pass"
}
```

## 22. Supersession and Historical Integrity

When this ADR is superseded:

1. its status changes to `superseded`;
2. `superseded_by` references the replacement ADR;
3. the replacement ADR references `ADR-026` through `supersedes`;
4. `DEC-DOC-002` follows its declared decision lifecycle;
5. the non-waivable authority list changes only through an accepted global authority decision;
6. prior authority releases preserve the exact decision-closure policy under which they were validated;
7. decision, requirement, lock, exception, test, evidence, impact, migration, rollback, and conformance history remains available;
8. generated indexes, reports, manifests, and AI contexts are regenerated;
9. active authority changes only after complete validation.

This ADR remains in the corpus after acceptance, deprecation, rejection, retirement, or supersession.
