<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONF-015",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "conformance",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-DOC-001",
    "DEC-GOV-001",
    "DEC-PROFILE-001",
    "DEC-DATA-001",
    "DEC-REL-001",
    "DEC-SEC-001",
    "DEC-OFFLINE-001"
  ],
  "requirement_ids": [
    "REQ-CONF-EXC-001",
    "REQ-CONF-EXC-002",
    "REQ-CONF-EXC-003",
    "REQ-CONF-EXC-004",
    "REQ-CONF-EXC-005",
    "REQ-CONF-EXC-006",
    "REQ-CONF-EXC-007",
    "REQ-CONF-EXC-008",
    "REQ-CONF-EXC-009",
    "REQ-CONF-EXC-010",
    "REQ-CONF-EXC-011",
    "REQ-CONF-EXC-012",
    "REQ-CONF-EXC-013",
    "REQ-CONF-EXC-014",
    "REQ-CONF-EXC-015",
    "REQ-CONF-EXC-016",
    "REQ-CONF-EXC-017",
    "REQ-CONF-EXC-018",
    "REQ-CONF-EXC-019",
    "REQ-CONF-EXC-020",
    "REQ-CONF-EXC-021",
    "REQ-CONF-EXC-022",
    "REQ-CONF-EXC-023",
    "REQ-CONF-EXC-024",
    "REQ-CONF-EXC-025",
    "REQ-CONF-EXC-026",
    "REQ-CONF-EXC-027",
    "REQ-CONF-EXC-028",
    "REQ-CONF-EXC-029",
    "REQ-CONF-EXC-030"
  ],
  "lock_ids": [
    "LOCK-DOC-001",
    "LOCK-DOC-002",
    "LOCK-DOC-003",
    "LOCK-DOC-005",
    "LOCK-DOC-008",
    "LOCK-DOC-009",
    "LOCK-DOC-010",
    "LOCK-DOC-011",
    "LOCK-DOC-013",
    "LOCK-DOC-014",
    "LOCK-DOC-017",
    "LOCK-DOC-022",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-013",
    "DOC-CONF-000"
  ],
  "tags": [
    "conformance",
    "normative-markdown",
    "15",
    "exceptions",
    "and",
    "waivers"
  ]
}
KOA:DOC-META:END -->

# Exceptions and Waivers

## 1. Purpose

This document defines the conformance treatment, lifecycle, authority, evidence, disclosure, and closure rules for kOA exceptions and waivers.

An exception or waiver is a bounded record for one concrete deviation context. It is not a mechanism for weakening canonical requirements globally, altering a lock silently, hiding a failed test, changing observed evidence, or transferring authority from a canonical owner.

The model exists to ensure that:

- deviations remain explicit and machine-readable;
- each affected requirement and lock remains visible;
- scope is concrete and does not inherit implicitly;
- non-waivable authority remains protected;
- risk ownership and approval remain human;
- controls are specific, testable, and evidenced;
- exceptions demonstrate equivalent satisfaction of normative intent;
- waivers remain temporary and include remediation;
- expiry is automatic and exact;
- conformance claims disclose active deviations;
- renewals are rare, bounded, and independently approved;
- expired or revoked records stop authorizing operation;
- repeated deviations trigger review of the canonical requirement;
- historical records remain traceable after closure.

The canonical exception object is validated by `schemas/exception.schema.json`. The canonical registry of active and historical records is `generated/exception-index.json`.

## 2. Scope

### 2.1 Covered deviation kinds

The model recognizes two deviation kinds:

| Deviation kind | Meaning |
| --- | --- |
| `exception` | A bounded case that satisfies the intent of affected authority through an equivalent control, produces a blocked claim, or establishes that the authority is not applicable to the concrete target. |
| `waiver` | A temporary approved deviation from an applicable requirement or lock while remediation proceeds, with qualified disclosure and no unqualified conformance claim. |

An exception is not a temporary waiver without remediation. A waiver is not an equivalent-control exception.

### 2.2 Covered targets

An exception or waiver can apply to one concrete target set of these kinds:

- deployment instance;
- release;
- profile claim;
- component instance;
- component release;
- artifact instance;
- development workspace;
- migration action.

The target list remains bounded and explicit. Scope does not include wildcard targets, unnamed future systems, all deployments, or implicit descendants.

### 2.3 Covered authority

A deviation can identify affected:

- requirement IDs;
- lock IDs;
- profile contracts;
- component contracts;
- artifact contracts;
- release references;
- workspace references;
- traceability records;
- tests;
- conformance claims.

At least one affected requirement is identified. Affected locks and contracts remain references to their canonical owners.

### 2.4 Non-waivable authority

The following classes remain non-waivable unless a new canonical decision explicitly changes the architecture:

- human-only approval for exceptions and waivers;
- prohibition on AI approval;
- concrete non-inheriting scope;
- canonical data ownership;
- prohibition on direct cross-component authoritative writes;
- requirement to preserve truthful evidence and observed test outcomes;
- prohibition on secret or hidden authority;
- automatic expiry;
- release and claim disclosure;
- preservation of current valid recovery state;
- separation of Publication Gateway, UCKK Publication Bridge, and UCKK Import Bridge responsibilities;
- prohibition on external AI becoming native authority;
- prohibition on an exception record redefining canonical requirements or locks.

A deviation that affects non-waivable authority is invalid rather than approvable.

### 2.5 Lifecycle states

The recognized lifecycle states are:

`text
proposed
 -> under_review
 -> approved
 -> active
 -> suspended
 -> active
 -> expired | revoked | superseded | closed
`

Alternative terminal paths include:

`text
proposed -> rejected
under_review -> rejected
approved -> revoked
active -> revoked
`

A terminal record remains historical and cannot return to active state.

### 2.6 Conformance effects

The recognized conformance effects are:

| Effect | Applicable deviation kind | Claim meaning |
| --- | --- | --- |
| `equivalent_control` | Exception | The requirement intent is satisfied through an approved equivalent control and supporting evidence. |
| `conformant_with_active_waiver` | Waiver | Operation is approved temporarily with explicit disclosure; unqualified conformance remains unavailable. |
| `claim_blocked` | Exception or waiver | The affected conformance claim cannot be made while the record applies. |
| `not_applicable` | Exception or waiver | The requirement is demonstrated not to apply to the concrete target, with traceable reasoning and evidence. |

An exception or waiver does not transform a failed test result into a pass.

### 2.7 Duration limits

Duration limits are:

- a waiver approval period of no more than 90 calendar days;
- at most one waiver renewal;
- an exception period of no more than 365 calendar days or one major documentation version, whichever boundary is reached first;
- exact automatic expiry at the recorded time.

A shorter limit in an affected requirement, profile, component, security policy, release policy, or legal obligation remains controlling.

### 2.8 Excluded uses

This document does not permit exceptions or waivers to:

- create a new canonical owner;
- change requirement text;
- change lock text;
- change an accepted decision;
- approve themselves;
- approve through AI;
- conceal a profile mismatch;
- conceal a Release Set incompatibility;
- redefine a failed test as successful;
- authorize indefinite technical debt;
- authorize broad future targets;
- authorize a missing remediation plan for a waiver;
- bypass release, migration, backup, or recovery controls;
- replace incident response;
- replace a new decision where the architecture itself must change.

## 3. Canonical References

| Canonical reference | Responsibility |
| --- | --- |
| `generated/requirements-index.json` | Owns the requirements affected by a deviation and their active status, owner, scope, strength, and validation. |
| `generated/assertion-index.json` | Owns alignment assertions and executable or manual controls that cannot be redefined by a deviation record. |
| `generated/traceability.json` | Owns links among decisions, requirements, locks, tests, evidence, claims, exceptions, releases, profiles, and artifacts. |
| `generated/test-catalog.json` | Owns test identity, procedure, expected result, applicability, evidence type, and cleanup behavior. |
| `generated/evidence-catalog.json` | Owns evidence identity, subject, producer, scope, result, validity, and lifecycle. |

Additional canonical authority includes:

- `generated/exception-index.json`;
- `schemas/exception.schema.json`;
- `generated/decision-index.json`;
- `generated/authority-manifest.json`;
- `generated/document-index.json`;
- profile, component, artifact, integration, and release contracts referenced by the deviation;
- the active signed Release Set.

This document explains the process. The exception schema and registry own the machine-readable record.

## 4. Model and Responsibilities

### 4.1 Exception record identity

Every record contains:

- stable `exception_id`;
- semantic version;
- deviation kind;
- lifecycle status;
- title and summary;
- justification where approval is sought;
- accepted decision references;
- exact target scope;
- affected authority;
- human owners;
- risk assessment;
- compensating controls;
- remediation for waivers;
- timing;
- approval;
- conformance effect;
- evidence;
- traceability;
- impact analysis;
- release disclosures where applicable;
- lifecycle events;
- renewal state;
- supersession state;
- closure state where terminal.

The identifier remains unique and is never reused.

### 4.2 Scope model

Scope includes:

- one scope kind;
- one or more concrete targets;
- a bounded description;
- explicit denial of implicit inheritance.

A profile-claim waiver does not apply automatically to deployments using the profile. A component-release waiver does not apply to another release. A workspace waiver does not apply to sibling workspaces.

### 4.3 Affected authority

Affected authority records:

- at least one requirement ID;
- zero or more lock IDs;
- profile references;
- component references;
- artifact references;
- release references;
- workspace references;
- confirmation that non-waivable authority is unaffected.

The canonical requirement and lock remain unchanged.

### 4.4 Human ownership

The record identifies distinct human roles for:

- requester;
- requirement owner;
- risk owner;
- control owner;
- remediation owner;
- approver.

The risk owner and approver are named human identities. Separation of duties is verified for high-risk, critical-risk, security-sensitive, high-assurance, publication, identity, governance, cultural-rights, release, and recovery deviations.

An AI system can prepare analysis or a proposal. It cannot approve, activate, renew, revoke, or close a deviation.

### 4.5 Risk assessment

The risk assessment records:

- bounded risk summary;
- inherent risk;
- residual risk after controls;
- risk-acceptance statement;
- assessment reference.

Risk levels are:

- `low`;
- `moderate`;
- `high`;
- `critical`.

High or critical residual risk requires verified separation of duties and cannot be hidden by an exception label.

### 4.6 Controls

Each compensating control has:

- stable control ID;
- concrete description;
- human owner;
- status;
- one or more test IDs;
- evidence IDs.

Control statuses are:

- `planned`;
- `implemented`;
- `verified`;
- `failed`;
- `retired`.

An active deviation includes current evidence and at least one implemented or verified control. A failed required control suspends or revokes authority according to the affected risk.

### 4.7 Exception model

An exception demonstrates one of:

- an equivalent or stronger control satisfies the requirement intent;
- the affected claim remains blocked;
- the requirement is not applicable to the concrete target.

An exception:

- has no renewal;
- records renewal count zero;
- remains bounded by expiry or one major documentation version;
- does not require a remediation plan when equivalent compliance is permanent for the concrete target;
- closes when the target becomes compliant, retires, changes scope, or the canonical authority changes.

An exception is inappropriate when the target simply cannot comply and intends to remediate later. That condition uses a waiver.

### 4.8 Waiver model

A waiver:

- permits a temporary declared deviation;
- includes a remediation owner;
- includes one or more dated milestones;
- includes completion criteria;
- has a maximum 90-day approval period;
- can be renewed at most once;
- requires progress evidence for renewal;
- prevents unqualified conformance;
- expires automatically;
- closes when remediation completes, the capability is removed, the target retires, or a supported alternative activates.

A waiver is inappropriate when no credible remediation plan exists.

### 4.9 Approval model

Approval records:

- approval status;
- mandatory human approval;
- prohibition on AI approval;
- approver identity;
- approval time;
- approval decision reference;
- separation-of-duties result.

Approval considers:

- affected authority;
- scope;
- risk;
- controls;
- evidence;
- remediation;
- duration;
- release effect;
- conformance effect;
- operational alternatives;
- exit and recovery;
- repeated-deviation history.

Approved state does not authorize operation until activation conditions and evidence are satisfied.

### 4.10 Activation model

Activation requires:

- approved status;
- complete justification;
- exact target scope;
- current risk assessment;
- implemented or verified controls;
- current evidence;
- approved activation time;
- future expiry;
- valid traceability;
- release and claim disclosure where applicable;
- no affected non-waivable authority.

The active record authorizes only the declared scope and effect.

### 4.11 Suspension, revocation, and expiry

Suspension is used when:

- evidence becomes stale;
- a control fails;
- scope becomes uncertain;
- risk changes;
- a required owner is unavailable;
- a related incident is under investigation;
- release or compatibility state changes.

Revocation is used when continuing authority is unacceptable.

Expiry occurs automatically at the recorded time. No manual closure is needed to end authorization.

Suspended, revoked, expired, superseded, closed, and rejected records do not authorize continued deviation.

### 4.12 Renewal

Only a waiver can be renewed.

Renewal requires:

- a new accepted decision;
- updated risk assessment;
- fresh evidence;
- verified controls;
- remediation progress;
- revised milestones;
- a new expiry within 90 calendar days;
- explicit disclosure;
- confirmation that no supported alternative is already available.

A second renewal is invalid.

### 4.13 Supersession

Supersession links records bidirectionally and without cycles.

A superseding record uses a new identifier and complete approval. The previous record becomes terminal. Supersession does not extend authorization retroactively or conceal a lapse.

### 4.14 Closure

Terminal records include closure details:

- closure reason;
- summary;
- human closer;
- closure time;
- evidence.

Closure reasons include:

- target became compliant;
- capability removed;
- target retired;
- canonical requirement changed;
- supported alternative activated;
- superseded by a new deviation;
- request rejected.

Closure preserves the historical risk, approval, evidence, and operational effect.

### 4.15 Repeated deviations

Repeated or broadly required deviations indicate one of:

- a poorly scoped requirement;
- an unsupported profile composition;
- an incomplete implementation;
- an architecture decision needing review;
- an unavailable supported alternative;
- an operational practice that has become permanent.

The canonical owner reviews repeated patterns rather than normalizing them through recurring waivers.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-CONF-EXC-001,REQ-CONF-EXC-002,REQ-CONF-EXC-003,REQ-CONF-EXC-004,REQ-CONF-EXC-005,REQ-CONF-EXC-006,REQ-CONF-EXC-007,REQ-CONF-EXC-008,REQ-CONF-EXC-009,REQ-CONF-EXC-010,REQ-CONF-EXC-011,REQ-CONF-EXC-012,REQ-CONF-EXC-013,REQ-CONF-EXC-014,REQ-CONF-EXC-015,REQ-CONF-EXC-016,REQ-CONF-EXC-017,REQ-CONF-EXC-018,REQ-CONF-EXC-019,REQ-CONF-EXC-020,REQ-CONF-EXC-021,REQ-CONF-EXC-022,REQ-CONF-EXC-023,REQ-CONF-EXC-024,REQ-CONF-EXC-025,REQ-CONF-EXC-026,REQ-CONF-EXC-027,REQ-CONF-EXC-028,REQ-CONF-EXC-029,REQ-CONF-EXC-030 -->
- **REQ-CONF-EXC-001 — SHALL:** Every exception or waiver be represented by one schema-valid record in `generated/exception-index.json` with a unique, non-reused identifier.
- **REQ-CONF-EXC-002 — SHALL:** Every deviation identify one concrete scope kind, explicit targets, a bounded description, and disabled implicit inheritance.
- **REQ-CONF-EXC-003 — SHALL NOT:** Wildcard, global, future, unnamed, inherited, or indefinite targets be authorized by an exception or waiver.
- **REQ-CONF-EXC-004 — SHALL:** Every deviation identify affected requirement IDs, applicable lock IDs, contracts, releases, workspaces, tests, evidence, and conformance claims.
- **REQ-CONF-EXC-005 — SHALL NOT:** A deviation affect authority classified as non-waivable or redefine a canonical requirement, lock, decision, contract, test result, or evidence result.
- **REQ-CONF-EXC-006 — SHALL:** Requester, requirement owner, risk owner, control owner, remediation owner, and approver be identified as human roles.
- **REQ-CONF-EXC-007 — SHALL NOT:** AI approve, activate, renew, revoke, close, or independently authorize an exception or waiver.
- **REQ-CONF-EXC-008 — SHALL:** High-risk, critical-risk, security-sensitive, high-assurance, publication, identity, governance, cultural-rights, release, and recovery deviations verify separation of duties.
- **REQ-CONF-EXC-009 — SHALL:** Every deviation include a current risk assessment with inherent risk, residual risk, risk acceptance, and assessment evidence.
- **REQ-CONF-EXC-010 — SHALL:** Every compensating control be concrete, assigned, testable, status-bearing, and linked to tests and evidence.
- **REQ-CONF-EXC-011 — SHALL:** An active deviation have current evidence and at least one implemented or verified compensating control.
- **REQ-CONF-EXC-012 — SHALL:** A failed required control suspend or revoke the affected deviation until new approval and evidence restore validity.
- **REQ-CONF-EXC-013 — SHALL:** An exception demonstrate equivalent or stronger satisfaction of requirement intent, block the claim, or prove non-applicability for the exact target.
- **REQ-CONF-EXC-014 — SHALL NOT:** An exception authorize temporary non-compliance without equivalent control or a blocked claim.
- **REQ-CONF-EXC-015 — SHALL:** An exception have no renewal, a renewal count of zero, and an expiry no later than 365 calendar days or the next major documentation version boundary.
- **REQ-CONF-EXC-016 — SHALL:** A waiver include a remediation plan, human owner, dated milestones, completion criteria, and progress evidence.
- **REQ-CONF-EXC-017 — SHALL:** A waiver approval period be no longer than 90 calendar days.
- **REQ-CONF-EXC-018 — SHALL NOT:** A waiver receive more than one renewal.
- **REQ-CONF-EXC-019 — SHALL:** Waiver renewal require a new accepted decision, updated risk assessment, fresh evidence, verified controls, remediation progress, revised milestones, and a new exact expiry.
- **REQ-CONF-EXC-020 — SHALL:** Every deviation require explicit human approval and record the approver, approval decision, approval time, and separation-of-duties result.
- **REQ-CONF-EXC-021 — SHALL:** Activation require approved status, complete justification, valid scope, current risk, current evidence, effective controls, traceability, disclosure, and a future expiry.
- **REQ-CONF-EXC-022 — SHALL:** Expiry be automatic and terminate authorization exactly at the recorded time.
- **REQ-CONF-EXC-023 — SHALL NOT:** Expired, suspended, revoked, superseded, closed, rejected, or unapproved records authorize continued deviation.
- **REQ-CONF-EXC-024 — SHALL:** Every affected release, profile, artifact, deployment, and conformance claim disclose applicable active deviations.
- **REQ-CONF-EXC-025 — SHALL NOT:** A waiver permit an unqualified conformance claim or transform a failed, blocked, invalid, cancelled, stale, or not-run test into a pass.
- **REQ-CONF-EXC-026 — SHALL:** Supersession use a new complete record, bidirectional links, an acyclic relationship, and no retroactive extension of authority.
- **REQ-CONF-EXC-027 — SHALL:** Terminal records include a closure reason, summary, human closer, closure time, and evidence while preserving historical facts.
- **REQ-CONF-EXC-028 — SHALL:** Material changes to scope, risk, control, release, profile, component, evidence, remediation, or authority trigger review, suspension, replacement, or closure.
- **REQ-CONF-EXC-029 — SHALL:** Repeated, renewed, or broadly required deviations trigger review by the canonical requirement or architecture owner.
- **REQ-CONF-EXC-030 — SHALL NOT:** A profile, recipe, dashboard, migration record, release note, generated context, test runner, or implementation convenience silently create, broaden, prolong, or conceal an exception or waiver.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Proposal

A proposal proceeds through:

1. Identify the affected target.
2. Identify the unmet or differently satisfied requirement.
3. Identify affected locks and contracts.
4. Confirm that no non-waivable authority is affected.
5. Determine whether the condition is an exception or waiver.
6. Identify all human owners.
7. Create the initial risk assessment.
8. define compensating controls;
9. Define remediation when the record is a waiver.
10. Define the requested duration.
11. Define conformance and release effects.
12. Create the schema-valid record in `proposed` state.
13. Add the initial lifecycle event.
14. Link impact-analysis and traceability records.

### 6.2 Review

Review proceeds through:

1. Validate the record against `schemas/exception.schema.json`.
2. Validate all referenced IDs.
3. Validate exact scope and non-inheritance.
4. Validate deviation-kind classification.
5. Validate non-waivable authority.
6. Review risk and alternatives.
7. Review controls and tests.
8. Review evidence.
9. Review remediation and milestones for a waiver.
10. Review duration.
11. Review disclosure and claim effects.
12. Review Release Set and profile effects.
13. Verify separation of duties.
14. Produce approval or rejection decision.

### 6.3 Approval

Approval proceeds through:

1. Record the human approver.
2. Record the accepted approval decision.
3. Record approval time.
4. Confirm requester and approver separation where required.
5. Confirm exact expiry.
6. Confirm automatic expiration.
7. Confirm active evidence requirements.
8. Confirm release and claim disclosure.
9. Set status to `approved`.
10. Record the approval lifecycle event.

Approval alone does not start the deviation.

### 6.4 Activation

Activation proceeds through:

1. Confirm status is approved.
2. Confirm the target still matches.
3. Confirm risk has not increased.
4. Confirm controls are implemented or verified.
5. Confirm evidence is current.
6. Confirm remediation has started for a waiver.
7. Confirm compatibility with the active Release Set.
8. Confirm disclosures are ready.
9. Record activation time.
10. Set status to `active`.
11. Publish the applicable qualified claim or blocked-claim state.
12. Start automated expiry and milestone monitoring.

### 6.5 Active monitoring

Active monitoring includes:

1. Revalidate control status.
2. Revalidate evidence validity.
3. Revalidate target identity.
4. Revalidate profile, component, artifact, and release versions.
5. Revalidate risk.
6. Track waiver milestones.
7. Track expiry.
8. Track incidents and security events.
9. Track repeated-deviation patterns.
10. Record lifecycle events and evidence.

A material adverse change moves the record to suspension, revocation, or replacement.

### 6.6 Suspension

Suspension proceeds through:

1. Identify stale evidence, failed control, changed risk, changed target, changed release, or unresolved incident.
2. Stop relying on the deviation.
3. Block affected claims and operations where required.
4. Record suspension time and actor.
5. Preserve historical evidence.
6. Define conditions for re-review.
7. return to active only through renewed validation within the original approval period;
8. Revoke or close when conditions cannot be restored.

Suspension does not pause the expiry clock.

### 6.7 Automatic expiry

At expiry:

1. Mark the record expired.
2. Stop authorization.
3. Stop affected qualified claims.
4. Block continued deviation.
5. Preserve historical execution and evidence.
6. Trigger remediation, rollback, shutdown, or supported alternative according to the approved plan.
7. Create the expiry lifecycle event.
8. Create the closure record when the target state is known.

No grace period is implied.

### 6.8 Waiver renewal

A first and only waiver renewal proceeds through:

1. Start review before expiry.
2. demonstrate remediation progress;
3. Explain why completion did not occur.
4. Update risk.
5. Refresh evidence.
6. Reverify controls.
7. Review alternatives.
8. Create a new accepted renewal decision.
9. Define revised milestones.
10. Define a new expiry within 90 calendar days.
11. Update disclosure.
12. Record renewal count one.
13. Record the renewal event.
14. Activate the renewed period before the previous period expires.

A lapse between periods remains a lapse in authorization.

### 6.9 Supersession

Supersession proceeds through:

1. Create a new record with a new identifier.
2. Complete full proposal, review, approval, and activation.
3. Link the new record to the prior record.
4. Link the prior record to the replacement.
5. Verify the relationship is acyclic.
6. Set the prior record to superseded.
7. Stop authority from the prior record.
8. preserve both records and their distinct periods;
9. Update disclosures and traceability.

### 6.10 Closure

Closure proceeds through:

1. Verify the terminal reason.
2. Verify target compliance, removal, retirement, replacement, requirement change, or rejection.
3. Verify no active operation relies on the record.
4. Verify temporary controls and credentials are retired appropriately.
5. Verify remediation evidence.
6. Verify release and claim disclosures are updated.
7. Record human closer and time.
8. Record closure evidence.
9. Set the terminal status.
10. Preserve the record according to retention policy.

### 6.11 Canonical review trigger

Repeated-deviation review proceeds through:

1. Aggregate records by requirement, lock, profile, component, and cause.
2. Identify repeated, renewed, or broad use.
3. Determine whether implementation, profile support, requirement scope, or architecture is incorrect.
4. Assign the canonical owner.
5. Create an impact analysis.
6. Decide whether to remediate implementation, add supported profile behavior, amend authority, or reject the recurring pattern.
7. Keep existing deviations independently bounded during review.
8. Record the outcome and affected closures.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Preserved capability | Denied capability |
| --- | --- | --- | --- |
| Record fails schema validation | Reject or block the record. | Canonical requirements and current compliant operation | Deviation authority |
| Scope contains wildcard or inheritance | Reject the record. | Concrete unaffected targets | Broad authorization |
| Requirement or lock reference missing | Block review. | Existing authority | Approval |
| Non-waivable authority affected | Reject the request. | Canonical protected boundary | Deviation |
| Deviation kind misclassified | Return for correction before approval. | Proposal history | Activation |
| Human owner missing | Block review. | Existing operation where compliant | Approval |
| AI approval recorded | Treat approval as invalid. | Proposal analysis | Authorization |
| Separation of duties fails | Block high-risk approval. | Independent review | Activation |
| Risk assessment stale | Suspend or block. | Historical assessment | Continued reliance |
| Control only planned | Keep record inactive. | Planned remediation | Deviation operation |
| Required control fails | Suspend or revoke. | Recovery and unaffected capability | Affected deviation |
| Evidence missing or stale | Block activation or suspend. | Raw observations | Qualified claim |
| Waiver has no remediation | Reject the waiver. | Proposal evidence | Temporary non-compliance |
| Milestone missed | Escalate, reassess risk, and suspend or revoke where required. | Historical progress | Automatic continuation |
| Exception requests renewal | Reject the renewal. | Existing period until expiry | Extended period |
| Waiver requests second renewal | Reject it. | Historical waiver | Further extension |
| Expiry reached | Terminate authorization automatically. | Canonical compliant paths | Continued deviation |
| Release or profile changes | Suspend pending impact review. | Last valid claim history | Automatic transfer |
| Supersession link incomplete | Block replacement activation or mark invalid. | Prior valid state until its own expiry | Ambiguous authority |
| Closure evidence missing | Keep cleanup incomplete and authority inactive. | Historical record | Complete-closure claim |
| Registry unavailable | Use no inferred active deviation; fail closed for new reliance. | Existing compliant operation | Unverifiable waiver use |
| Repeated waiver pattern | Trigger canonical review. | Individually valid current period | Indefinite normalization |

Safe degradation preserves canonical requirements, truthful evidence, compliant operation, and recovery paths. It does not infer approval, extend expiry, broaden scope, reuse another target’s record, or treat silence as authorization.

## 8. Cross-Component Interactions

### 8.1 Requirements registry

The requirements registry remains the canonical source of requirement text, scope, owner, strength, and validation.

An exception or waiver references a requirement. It does not edit the requirement.

### 8.2 Locks registry

The locks registry remains the canonical source of alignment assertions.

A record can identify an affected lock only where the lock is waivable and the impact analysis explains the bounded effect. Non-waivable locks reject the record.

### 8.3 Traceability registry

Traceability links:

- deviation;
- affected decisions;
- requirements;
- locks;
- profiles;
- components;
- artifacts;
- releases;
- tests;
- evidence;
- claims;
- remediation.

The deviation record does not become a parallel traceability authority.

### 8.4 Test catalog and evidence registry

Tests continue to report observed results.

Evidence continues to report observed facts and scope.

An exception or waiver can explain the conformance effect of those facts. It cannot alter a failed result into a pass or make stale evidence current.

### 8.5 Profile contracts

A profile deviation applies only to the named profile claim or deployment target.

It does not change the profile contract or all deployments using the profile. Repeated profile waivers trigger supported-profile review.

### 8.6 Component contracts

A component deviation preserves component identity, responsibilities, non-responsibilities, and data ownership.

Direct cross-component authoritative writes remain prohibited. A waiver cannot authorize one component to become the owner of another component’s data.

### 8.7 Release lifecycle

A release or deployment with an active deviation discloses it in the applicable release and conformance records.

A new Release Set triggers impact review. Deviation validity does not transfer automatically to new versions.

### 8.8 Governance Policy Runtime

Governance Policy Runtime can evaluate whether an operation is permitted under an active deviation reference.

It validates status, scope, expiry, affected authority, and obligations. It does not approve the deviation.

### 8.9 Resource Governor

Resource Governor can enforce compensating controls involving limits, queues, isolation, or disabled capabilities.

Resource controls do not replace human approval, risk acceptance, evidence, or remediation.

### 8.10 Audit Broker

Audit Broker receives bounded lifecycle events and evidence references.

Selective audit can prove approval, scope, controls, expiry, and closure without exposing protected operational or cultural details publicly.

### 8.11 AI systems

AI systems can:

- identify candidate deviations;
- assemble references;
- summarize risk evidence;
- prepare a proposal;
- detect expiry or missing fields;
- compare records for repeated patterns.

AI systems remain unable to approve or activate the record and cannot create missing authority.

## 9. Decision Closure and Prohibited Assumptions

The accepted decisions referenced in the metadata close the exception and waiver model.

The following assumptions are prohibited:

1. An exception and a waiver are interchangeable.
2. A waiver can be permanent.
3. An exception can be renewed.
4. A waiver can be renewed repeatedly.
5. Approval can omit an exact expiry.
6. Expiry waits for manual action.
7. Suspension pauses expiry.
8. A broad target description is sufficiently concrete.
9. A profile waiver applies to every profile deployment.
10. A release waiver applies to later releases.
11. A workspace waiver applies to sibling workspaces.
12. An AI-generated approval is valid.
13. A risk-owner role can be anonymous.
14. High residual risk can omit separation of duties.
15. A planned control supports active deviation.
16. A vague promise is a compensating control.
17. An untested control is equivalent evidence.
18. A waiver without remediation is acceptable.
19. Missing evidence can be supplied after activation.
20. A failed test becomes a pass under a waiver.
21. An exception changes the canonical requirement.
22. An exception changes an accepted decision.
23. A waiver can affect non-waivable authority.
24. A closed record can be reactivated.
25. Supersession extends authority retroactively.
26. A new Release Set inherits prior deviation validity.
27. Non-disclosure preserves an unqualified conformance claim.
28. Repeated waivers are ordinary long-term operation.
29. A dashboard or release note is the canonical record.
30. Operational urgency creates implicit approval.

When classification, scope, authority, risk, control, evidence, ownership, duration, or lifecycle state is uncertain, the deviation remains inactive or the affected claim remains blocked.

## 10. Validation Criteria

This document is conformant when:

1. It is registered as `DOC-CONF-015`.
2. Its path is `09-conformance/15-exceptions-and-waivers.md`.
3. Its class is `normative_markdown`.
4. Its status is `active`.
5. Its language is `en`.
6. Its layer is `conformance`.
7. Its scope is `global`.
8. Its metadata matches `generated/document-index.json`.
9. Every canonical reference resolves.
10. Every listed decision resolves with accepted status.
11. Every listed requirement resolves and matches the generated block.
12. Every listed lock resolves and passes.
13. The eleven mandatory sections exist in the required order.
14. Normative keywords occur only in the generated requirements block.
15. Every deviation validates against `schemas/exception.schema.json`.
16. Every deviation identifier is unique and never reused.
17. Every scope is concrete, bounded, and non-inheriting.
18. Every affected requirement, lock, contract, release, workspace, test, evidence, and claim reference resolves.
19. No record affects non-waivable authority.
20. Human ownership and approval are complete.
21. AI approval remains disabled.
22. Required separation of duties is verified.
23. Risk assessment and impact analysis are current.
24. Active controls are implemented or verified and linked to tests and evidence.
25. Exception records use only permitted conformance effects and have no renewal.
26. Waiver records include remediation, remain within 90 days, and have no more than one renewal.
27. Expiry timestamps and lifecycle-event ordering are consistent.
28. Expired, suspended, revoked, superseded, closed, rejected, and unapproved records authorize no continued deviation.
29. Release and conformance disclosures list every applicable active record.
30. Test and evidence results remain unchanged by deviation records.
31. Supersession relationships are bidirectional and acyclic.
32. Terminal records contain complete closure evidence.
33. Repeated deviations trigger canonical-owner review.
34. Traceability from decisions, requirements, locks, targets, tests, evidence, claims, releases, controls, remediation, and closure is complete.
35. No unresolved marker, provisional value, parallel authority, or file-content hash requirement appears.
36. Complete documentation validation returns `pass`.

## 11. Non-Normative Examples

### 11.1 Equivalent-control exception

A profile requires a specific isolation outcome. One deployment uses a different mechanism that produces equal or stronger isolation and passes all outcome tests. A concrete exception records the equivalent control for that deployment and expires at the next major documentation-version boundary.

### 11.2 Temporary waiver

A sovereign hub cannot complete a storage migration before a required maintenance event. A 45-day waiver records the affected requirement, protected backup and restore controls, remediation milestones, human approval, qualified claim, and exact expiry.

### 11.3 Failed control

An active waiver relies on a queue-depth control. The control test fails. The waiver is suspended immediately, new affected work stops, and the system retains only compliant or recovery operation.

### 11.4 Non-applicable exception

A component-release requirement refers to a capability that the concrete artifact does not contain and cannot activate. An exception records the bounded non-applicability with contract and test evidence. It does not alter the requirement for other artifacts.

### 11.5 Waiver renewal

A waiver approaches expiry with verified remediation progress but an external hardware delivery delay. A new human decision, refreshed risk assessment, updated evidence, revised milestones, and one final period of less than 90 days are recorded. No further renewal is available.

### 11.6 Expired waiver

The exact expiry time passes before remediation finishes. Authorization ends automatically. The affected claim becomes blocked and the system follows the approved stop, rollback, or restricted-operation path.

### 11.7 New Release Set

A deployment updates the services channel. The active waiver is suspended until impact analysis confirms that controls, tests, evidence, and remediation remain valid for the new Release Set.

### 11.8 Supersession

A target’s scope changes materially. A new deviation record is approved for the new target. The prior record becomes superseded and retains its historical period without authorizing the changed target retroactively.

### 11.9 Repeated profile waiver

Several deployments request the same waiver for one profile requirement. The profile owner reviews whether the implementation is incomplete or whether a supported profile variant is needed. Individual records remain independently scoped and expiring.

### 11.10 AI-prepared proposal

An AI agent detects a missing conformance control and drafts a proposal with references and risk questions. The proposal remains unapproved until named humans review, decide, approve, and activate it.
