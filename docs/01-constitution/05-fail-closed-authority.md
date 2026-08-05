<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONST-005",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "constitution",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/authority_model/fail_closed",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/exception-index.json",
    "generated/traceability.json"
  ],
  "decision_ids": [
    "DEC-CONST-002"
  ],
  "requirement_ids": [
    "REQ-CONST-FCA-001",
    "REQ-CONST-FCA-002",
    "REQ-CONST-FCA-003",
    "REQ-CONST-FCA-004",
    "REQ-CONST-FCA-005",
    "REQ-CONST-FCA-006",
    "REQ-CONST-FCA-007",
    "REQ-CONST-FCA-008",
    "REQ-CONST-FCA-009",
    "REQ-CONST-FCA-010",
    "REQ-CONST-FCA-011",
    "REQ-CONST-FCA-012",
    "REQ-CONST-FCA-013",
    "REQ-CONST-FCA-014",
    "REQ-CONST-FCA-015"
  ],
  "lock_ids": [
    "LOCK-DOC-001",
    "LOCK-DOC-002",
    "LOCK-DOC-011",
    "LOCK-DOC-013",
    "LOCK-DOC-014",
    "LOCK-AI-002",
    "LOCK-DATA-001",
    "LOCK-LIFE-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-000",
    "DOC-CONST-002",
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-005"
  ],
  "tags": [
    "constitution",
    "authority",
    "fail-closed",
    "safe-degradation",
    "offline-continuity",
    "privilege",
    "disclosure",
    "activation"
  ]
}
KOA:DOC-META:END -->

# Fail-Closed Authority

## 1. Purpose

This document defines the constitutional fail-closed authority rule for kOA.

Fail-closed authority means that an action with authoritative effect proceeds only when the applicable authority can be positively established. Missing, invalid, expired, revoked, incompatible, conflicting, or ambiguous authority does not become permission.

The rule protects system integrity while preserving useful operation where safe. It therefore distinguishes:

- denial of an authority-bearing effect;
- containment of the affected capability;
- continuation of unrelated capabilities;
- safe read-only or local operation;
- explicit offline authority;
- controlled recovery and break-glass operation.

Fail-closed authority complements explicit authority and safe degradation. Explicit authority defines where permission originates. Fail-closed authority defines the result when that permission cannot be established. Safe degradation defines which reduced behaviors remain available without increasing authority.

## 2. Scope

This document applies globally across every profile, overlay, component, artifact class, release channel, integration, and operational mode.

It applies whenever an operation can:

- create, modify, delete, activate, restore, or supersede authoritative state;
- disclose information outside its current authority domain;
- publish or transfer content across a component, tenant, profile, trust, or governance boundary;
- acquire or exercise privilege;
- activate a release, artifact, policy, runtime pack, system image, or configuration;
- establish, delegate, renew, revoke, or interpret authority;
- invoke an external integration with authoritative effect;
- convert an AI-produced candidate into authoritative state;
- use a recovery, emergency, or break-glass path;
- rely on cached authority during degraded or offline operation.

This document does not require a total system shutdown after every authority failure. The denial boundary is the smallest capability boundary that prevents the unauthorized effect. Unrelated functions can continue when their own authority remains valid and their operation does not recreate the denied effect indirectly.

## 3. Canonical References

The canonical sources for this document are:

`text
generated/authority-manifest.json
generated/decision-index.json
contracts/system.contract.json#/authority_model/fail_closed
generated/requirements-index.json
generated/assertion-index.json
generated/exception-index.json
generated/traceability.json
`

Their ownership roles are:

| Canonical source | Ownership |
| --- | --- |
| `authority.registry.json` | Active authority order and active registry set |
| `decisions.registry.json` | Accepted constitutional and architectural decisions |
| `system.registry.json#/authority_model/fail_closed` | Canonical system model for fail-closed authority |
| `requirements.registry.json` | Normative requirement text, strength, scope, ownership, and validation |
| `locks.registry.json` | Cross-file invariants that prevent authority drift |
| `exceptions.registry.json` | Bounded exceptions and waivers that cannot create missing authority |
| `traceability.registry.json` | Requirement, lock, test, evidence, component, profile, and document relationships |

This Markdown document explains the constitutional model and operating consequences. It does not become a second owner of registry values.

## 4. Model and Responsibilities

### 4.1 Authority tuple

An authority decision is evaluated against a complete tuple:

`text
actor
action
target
scope
conditions
authority owner
authority evidence
validity interval
contract version
decision provenance
`

A positive result applies only to the tuple that was evaluated. Permission for one actor, action, target, scope, or condition does not imply permission for another.

### 4.2 Decision states

An authority evaluation has three semantic results:

| Result | Meaning | Permitted effect |
| --- | --- | --- |
| `authorized` | A current canonical grant matches the complete authority tuple | The declared effect can proceed within the grant |
| `denied` | A current canonical rule rejects the effect | No protected effect occurs |
| `indeterminate` | Required authority cannot be established conclusively | No protected effect occurs |

The indeterminate state remains distinct for diagnostics and recovery, but it has the same execution consequence as denial for the protected action.

### 4.3 Sources of indeterminate authority

Authority is indeterminate when any required element is unavailable or inconclusive, including:

- missing canonical owner;
- conflicting ownership claims;
- missing accepted decision;
- unresolved canonical reference;
- unavailable required policy or trust source;
- invalid, expired, revoked, or unverifiable evidence;
- actor, action, target, or scope mismatch;
- unsupported contract or schema version;
- partial authority data;
- ambiguous profile or overlay applicability;
- incomplete delegation chain;
- incomplete exception or waiver record;
- inconsistent component or release state.

### 4.4 Capability containment

Fail-closed behavior is capability-scoped.

Examples of containment include:

- a publication failure leaves the draft locally available;
- a privilege failure leaves non-privileged inspection available;
- an activation failure leaves the previous valid artifact active;
- an external integration failure leaves local processing available;
- an authority lookup failure leaves non-authoritative navigation and explanation available;
- a cross-domain transfer failure leaves source data unchanged in its owning domain.

Containment ends where continued behavior would reproduce the denied effect through another route.

### 4.5 Responsibilities

| Participant | Responsibility |
| --- | --- |
| Requesting actor or component | Declare the intended actor, action, target, scope, and conditions |
| Canonical authority owner | Define the applicable grant, prohibition, delegation, and validity rules |
| Identity and trust services | Establish identity and evidence provenance without inventing authorization |
| Governance Policy Runtime | Evaluate applicable governance authorization where deployed |
| Owning component | Enforce its data and state-transition contract |
| Resource Governor | Enforce resource allocation without becoming a policy authorization owner |
| Publication and dimension gateways | Enforce their distinct disclosure and ingestion boundaries |
| Lifecycle services | Preserve atomic activation, rollback, and forward-repair guarantees |
| Audit Broker or receipt producer | Record critical decisions and transitions with selective disclosure |
| User experience layer | Report the actual outcome and available safe recovery actions |
| AI adapter or agent | Produce candidate input only and never fill missing authority |

No participant can broaden another participant's canonical grant.

### 4.6 Cached and offline authority

Offline continuity uses explicit offline authority, not an outage exception.

A cached grant is usable only when its canonical contract defines:

- the capability covered;
- the permitted actor and target;
- the offline scope;
- the starting and ending validity times;
- the evidence required at use time;
- the actions permitted while disconnected;
- the revocation and reconciliation behavior;
- the result after expiration.

The offline path cannot renew itself, widen its scope, create a new delegation, or authorize an action that was not included before disconnection.

### 4.7 Break-glass authority

Break-glass operation is an explicit authority mechanism rather than a bypass.

A valid break-glass design includes:

- a predefined protected capability;
- identified human invocation;
- narrow action and target scope;
- short validity;
- independent recording;
- visible degraded or emergency state;
- post-action review;
- revocation and closure;
- rollback or remediation where relevant.

A generic administrator role, root access, physical access, or operational urgency is not a complete break-glass authority grant.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-CONST-FCA-001,REQ-CONST-FCA-002,REQ-CONST-FCA-003,REQ-CONST-FCA-004,REQ-CONST-FCA-005,REQ-CONST-FCA-006,REQ-CONST-FCA-007,REQ-CONST-FCA-008,REQ-CONST-FCA-009,REQ-CONST-FCA-010,REQ-CONST-FCA-011,REQ-CONST-FCA-012,REQ-CONST-FCA-013,REQ-CONST-FCA-014,REQ-CONST-FCA-015 -->
- **REQ-CONST-FCA-001 — SHALL:** Every authority-bearing action require an explicit positive grant from the canonical authority applicable to the actor, action, target, scope, and current conditions.
- **REQ-CONST-FCA-002 — SHALL:** An indeterminate authority result be treated as denied for the affected authority-bearing action.
- **REQ-CONST-FCA-003 — SHALL:** A fail-closed result be contained to the affected capability unless continued operation would create an equivalent unauthorized effect.
- **REQ-CONST-FCA-004 — SHALL NOT:** Identity, role, physical access, previous success, implementation default, user intent, operational urgency, or AI output substitute for an explicit authority grant.
- **REQ-CONST-FCA-005 — SHALL:** Authority validation verify provenance, owner, actor, action, target, scope, conditions, status, validity interval, and applicable contract version before effect.
- **REQ-CONST-FCA-006 — SHALL:** Cached or offline authority be accepted only when an active canonical contract explicitly permits offline use and the grant remains within its declared scope and validity interval.
- **REQ-CONST-FCA-007 — SHALL NOT:** Unavailable verification infrastructure expand, renew, or create authority.
- **REQ-CONST-FCA-008 — MAY:** A capability continue in read-only, local, advisory, or queued form when that degraded behavior performs no unauthorized mutation, disclosure, publication, activation, privilege use, or cross-domain transfer.
- **REQ-CONST-FCA-009 — SHALL:** A component modify authoritative state owned by another component only through the owning component's declared contract and authorization path.
- **REQ-CONST-FCA-010 — SHALL NOT:** External AI output directly authorize or execute an authoritative state transition.
- **REQ-CONST-FCA-011 — SHALL:** Release activation, artifact activation, publication, and other critical commits complete atomically or preserve the last valid authoritative state through rollback or declared forward repair.
- **REQ-CONST-FCA-012 — SHALL:** A break-glass path be pre-authorized, narrowly scoped, time-bounded, human-invoked, independently recorded, and subject to mandatory review.
- **REQ-CONST-FCA-013 — SHALL:** A denied or indeterminate authority result produce a stable machine-readable reason code and a truthful user-facing outcome without reporting success.
- **REQ-CONST-FCA-014 — SHALL:** Critical authority decisions and protected transitions emit a machine-readable receipt that records the decision context without disclosing protected content unnecessarily.
- **REQ-CONST-FCA-015 — SHALL NOT:** An exception or waiver convert absent, ambiguous, expired, revoked, or invalid authority into permission.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Standard authority evaluation

An authority-bearing request follows this sequence:

1. identify the requesting actor and responsible component;
2. classify the intended action and authoritative effect;
3. identify the canonical owner of the target state or disclosure boundary;
4. resolve the active profile, overlay, component contract, policy, release, and exception context;
5. collect the required authority evidence;
6. validate provenance, version, scope, conditions, validity, and delegation;
7. produce `authorized`, `denied`, or `indeterminate`;
8. execute only an authorized effect;
9. commit the effect atomically where the operation changes authoritative state;
10. emit the applicable receipt and user-facing result.

A denied or indeterminate request leaves protected state unchanged.

### 6.2 Safe degraded transition

After denial or an indeterminate result, the system evaluates a separate degraded behavior:

1. identify a behavior that does not require the failed authority;
2. verify that it creates no equivalent mutation, disclosure, publication, activation, privilege, or transfer;
3. verify that it does not widen cached or offline authority;
4. enter the declared degraded state;
5. report which capability is unavailable and which capabilities remain available;
6. retry the protected operation only after new valid authority evidence or restored canonical authority.

Queued work remains non-authoritative until reevaluated at execution time.

### 6.3 Offline transition

When a required online authority source becomes unavailable:

1. resolve the active offline-authority contract;
2. validate the cached grant and its validity interval;
3. restrict execution to the declared offline capability set;
4. record actions requiring later reconciliation;
5. stop the protected operation when the grant expires or its conditions fail;
6. reconcile without silently broadening or retroactively fabricating authority.

Absence of an offline-authority contract results in denial of the affected authority-bearing action.

### 6.4 Revocation transition

Revocation immediately prevents new effects within the revoked scope.

Operations already committed remain historical facts. Pending, queued, retrying, or partially prepared operations are reevaluated before effect. Where a committed state must be reversed, the owning lifecycle contract defines rollback, forward repair, or compensating action.

### 6.5 Break-glass transition

A break-glass operation follows this sequence:

1. verify that the capability has a predefined break-glass contract;
2. identify and authenticate the human invoker;
3. verify the declared emergency condition;
4. constrain the action, target, duration, and available interfaces;
5. activate the temporary grant;
6. record each protected transition;
7. expire the grant automatically;
8. review the action and evidence;
9. close, revoke, remediate, or escalate the event.

## 7. Failure States and Safe Degradation

| Failure code | Condition | Protected result | Safe degraded result |
| --- | --- | --- | --- |
| `authority_source_unavailable` | A required canonical authority source cannot be reached | Affected authoritative effect is denied | Declared offline or non-authoritative behavior only |
| `authority_reference_not_found` | Required path, identifier, or JSON Pointer does not resolve | Affected object remains inactive | Inspection and repair workflow |
| `authority_owner_conflict` | More than one active owner claims the same fact | Neither claim authorizes effect | Read-only conflict reporting |
| `authority_decision_missing` | A required accepted decision is absent | Dependent effect remains inactive | Proposal or review activity only |
| `authority_evidence_invalid` | Evidence provenance or structure is invalid | Effect is denied | Evidence replacement workflow |
| `authority_evidence_expired` | Grant validity has ended | New effect is denied | Read-only access where separately authorized |
| `authority_evidence_revoked` | Grant or delegation has been revoked | New effect is denied | Revocation reporting and remediation |
| `authority_scope_mismatch` | Actor, target, action, profile, or condition is outside the grant | Out-of-scope effect is denied | Operation within an independently valid scope |
| `authority_contract_incompatible` | Contract or schema version is unsupported | Effect is denied | Compatibility negotiation or retained prior version |
| `authority_result_ambiguous` | Evaluation cannot produce one conclusive result | Effect is denied | Diagnostic reporting without mutation |
| `authority_commit_partial` | A critical transition cannot commit atomically | Partial state does not become authoritative | Rollback or declared forward repair |
| `break_glass_contract_missing` | Emergency access is requested without a canonical emergency contract | Emergency effect is denied | Escalation and recovery procedure |

Safe degradation never changes a denied result into authorization. It exposes a different capability whose own authority is valid or whose operation has no authoritative effect.

## 8. Cross-Component Interactions

### 8.1 Identity and authorization

Identity services establish who or what is acting. They do not independently determine every action the identity can perform. Authorization remains with the canonical owner and applicable policy contract.

### 8.2 Governance Policy Runtime and Resource Governor

The Governance Policy Runtime evaluates authorization, disclosure, and privilege where its profile deploys that component. The Resource Governor controls resource allocation and scheduling. Resource availability does not imply policy authorization, and policy authorization does not guarantee resource availability.

### 8.3 Component data ownership

Each component enforces transitions over its authoritative data. Another component uses the declared interface, event, artifact, or gateway contract instead of direct writes to the owner's source tables.

### 8.4 Publication Gateway and UCKK Import Bridge

Publication Gateway controls governed outbound disclosure. The UCKK Import Bridge controls inbound retrieval and quarantine, while the kOA Mediatheque owns local acceptance. Authority for one direction does not authorize the other.

### 8.5 Lifecycle and release services

Artifact and release activation use fail-closed verification and atomic state transitions. Verification failure preserves the last valid active state. Compatibility uncertainty blocks activation rather than selecting an unverified combination.

### 8.6 AI and Ariane

External AI output remains candidate input. It cannot authorize an action, resolve an ownership conflict, or replace missing policy. Ariane local navigation remains available without external AI when its local authority and dependencies remain valid. An unavailable voice or AI adapter affects only the adapter-dependent capability.

### 8.7 Audit and receipts

Critical decisions and protected transitions produce receipts sufficient for accountability, review, and recovery. Receipt content follows selective-disclosure rules and does not require indiscriminate exposure of protected data.

## 9. Decision Closure and Prohibited Assumptions

This document closes the constitutional interpretation of fail-closed authority as follows:

- `indeterminate` never means permitted;
- fail-closed behavior is capability-scoped rather than automatically system-wide;
- safe degradation is a separately valid behavior, not weakened authorization;
- offline continuity requires a predeclared offline grant;
- break-glass is explicit temporary authority, not a bypass;
- identity and privilege level do not replace action-specific authority;
- AI cannot create, infer, or repair missing authority;
- an exception cannot create permission where authority is absent or invalid;
- partial critical state does not become authoritative.

The following assumptions are prohibited:

- authentication implies authorization;
- an administrator or root identity has universal authority;
- physical possession implies permission;
- previous approval remains valid indefinitely;
- cached authority is valid without an offline contract;
- an outage justifies bypassing authority;
- user intent alone authorizes disclosure or mutation;
- a high-confidence AI answer establishes permission;
- local or offline execution is unrestricted;
- absence of an explicit denial means permission;
- a partially completed activation is acceptable;
- a recipe, example, ticket, prompt, or code comment creates authority;
- emergency conditions remove the need for a canonical break-glass path.

A new authority mode, delegation model, offline rule, or break-glass mechanism requires an accepted owner decision, updated canonical requirements, impact analysis, applicable lock updates, and complete validation before activation.

## 10. Validation Criteria

This document is conformant when all of the following checks pass:

1. the metadata block is valid, first in the file, and declares status `active`;
2. the document uses the required 11-section normative structure;
3. every canonical reference resolves to its registered owner;
4. `DEC-CONST-002` is accepted before this document participates in active authority;
5. all 15 requirement identifiers are unique and registered with global scope;
6. each registered requirement identifies its owner, decision source, strength, and validation method;
7. every declared lock exists and is active;
8. authority tests cover `authorized`, `denied`, and `indeterminate` outcomes;
9. protected state remains unchanged after denied and indeterminate test cases;
10. offline tests reject expired, out-of-scope, and self-renewed cached grants;
11. degraded-mode tests prove the absence of unauthorized mutation, disclosure, publication, activation, privilege, and cross-domain transfer;
12. lifecycle tests prove atomic activation, rollback, or declared forward repair;
13. break-glass tests prove narrow scope, human invocation, automatic expiration, receipts, and review;
14. AI integration tests prove that AI output remains non-authoritative;
15. user-facing tests prove that failure is not reported as success;
16. no unresolved-authority marker, duplicate requirement identifier, or unregistered normative statement exists;
17. active prose is English;
18. ordinary Markdown validation does not depend on file-content hashes.

Expected validator failure codes include:

`text
missing_owner_decision
canonical_reference_not_found
canonical_ownership_conflict
interfile_alignment_lock_failed
authority_test_missing
offline_authority_contract_invalid
safe_degradation_expands_authority
atomic_transition_not_proven
break_glass_control_incomplete
ai_output_authority_violation
false_success_result
`

## 11. Non-Normative Examples

### 11.1 Publication policy unavailable

A user prepares content for publication while the required disclosure policy service is unavailable. The draft remains locally available, but publication is not performed. The interface reports that the publication authority cannot be established and offers retry or local export where separately permitted.

### 11.2 External AI suggestion

An external AI service suggests tags and a destination for a document. The suggestions remain candidate input. The owning component and applicable disclosure policy reevaluate the final action before any authoritative metadata change or transfer occurs.

### 11.3 Offline local use

A disconnected device has a valid offline grant for reading local material until a declared expiration time. Reading continues within that scope. Cross-domain publication, new delegation, and renewal remain unavailable until the applicable authority sources return.

### 11.4 Release activation failure

A new service artifact passes download but fails compatibility verification during activation. The current valid service version remains active. The failed artifact is retained only as non-active diagnostic material or removed according to lifecycle policy.

### 11.5 Break-glass recovery

A predefined recovery contract permits a named operator to unlock one recovery action for fifteen minutes. The operation is recorded, the grant expires automatically, and the event enters mandatory review. The temporary grant does not provide general administrative authority.
