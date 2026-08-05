<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-GOV-015",
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
    "generated/exception-index.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json"
  ],
  "decision_ids": [
    "DEC-DOC-001",
    "DEC-DOC-EXC-001"
  ],
  "requirement_ids": [
    "REQ-DOC-EXC-001",
    "REQ-DOC-EXC-002",
    "REQ-DOC-EXC-003",
    "REQ-DOC-EXC-004",
    "REQ-DOC-EXC-005",
    "REQ-DOC-EXC-006",
    "REQ-DOC-EXC-007",
    "REQ-DOC-EXC-008",
    "REQ-DOC-EXC-009",
    "REQ-DOC-EXC-010",
    "REQ-DOC-EXC-011",
    "REQ-DOC-EXC-012",
    "REQ-DOC-EXC-013",
    "REQ-DOC-EXC-014",
    "REQ-DOC-EXC-015",
    "REQ-DOC-EXC-016",
    "REQ-DOC-EXC-017",
    "REQ-DOC-EXC-018",
    "REQ-DOC-EXC-019",
    "REQ-DOC-EXC-020",
    "REQ-DOC-EXC-021",
    "REQ-DOC-EXC-022",
    "REQ-DOC-EXC-023",
    "REQ-DOC-EXC-024",
    "REQ-DOC-EXC-025",
    "REQ-DOC-EXC-026"
  ],
  "lock_ids": [
    "LOCK-DOC-001",
    "LOCK-DOC-002",
    "LOCK-DOC-011",
    "LOCK-DOC-012",
    "LOCK-DOC-013",
    "LOCK-DOC-014",
    "LOCK-DOC-015",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-IMPL-001",
    "LOCK-DATA-001",
    "LOCK-AI-001",
    "LOCK-AI-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-003",
    "DOC-GOV-004",
    "DOC-GOV-005",
    "DOC-GOV-009",
    "DOC-GOV-010",
    "DOC-GOV-011",
    "DOC-GOV-013"
  ],
  "tags": [
    "exceptions",
    "waivers",
    "risk-acceptance",
    "conformance",
    "governance",
    "change-control"
  ]
}
KOA:DOC-META:END -->

# Exceptions and Waivers

## 1. Purpose

This document defines the only permitted mechanism for approving a bounded deviation from an active kOA requirement.

Exceptions and waivers exist to handle constrained, documented, and temporary situations without silently weakening the architecture.

They are not a substitute for changing an incorrect requirement, resolving a missing architectural decision, creating a deployment profile, recording an implementation choice, correcting a defective component contract, updating an obsolete security control, bypassing validation, or accepting undocumented technical debt.

Every approved deviation is machine-readable, explicitly scoped, time-bounded, attributable to a human authority, linked to compensating controls, and visible in conformance evidence.

No deviation exists unless it is registered in `generated/exception-index.json`.

---

## 2. Scope

This policy applies to deviations involving normative, profile, component, artifact, development-toolchain, security, operational, lifecycle, conformance, release-gate, migration, and profile-adopted implementation requirements.

It applies to documentation authors, component maintainers, release managers, security owners, profile owners, conformance reviewers, AI agents, and automated validators.

It does not permit deviations from non-waivable authority or constitutional protections defined in Section 4.8.

---

## 3. Canonical References

Canonical sources:

`text
generated/exception-index.json
generated/decision-index.json
generated/requirements-index.json
generated/assertion-index.json
generated/traceability.json
generated/document-index.json
`

Governing schemas:

`text
schemas/exception.schema.json
schemas/test-evidence.schema.json
`

Principal validators:

`text
tools/check_traceability.py
tools/check_interfile_locks.py
tools/check_decision_closure.py
tools/check_profile_inheritance.py
tools/validate_docs.py
`

Markdown summaries, generated exception indexes, tickets, comments, or release notes do not create an exception.

---

## 4. Model and Responsibilities

### 4.1 Exception

An exception is an approved, bounded alternative to the literal implementation of an active requirement. It is appropriate only when the requirement’s intent remains satisfied, the standard implementation is unsuitable in a specific scope, an alternative control provides equivalent or stronger protection, the deviation is measurable and verifiable, and it does not alter global architecture.

An exception does not suspend the requirement’s architectural intent.

### 4.2 Waiver

A waiver is a temporary approval not to satisfy a requirement fully. It is appropriate only when immediate compliance is not technically achievable, the affected capability can operate inside a documented risk envelope, compensating controls reduce exposure, a remediation plan exists, an expiration date is enforced, and a responsible human accepts residual risk.

A waiver acknowledges incomplete compliance and cannot be described as equivalent conformance.

### 4.3 Exception versus requirement change

A deviation is not an exception when it should apply broadly or permanently. The canonical requirement is changed instead when the same deviation is needed across unrelated deployments, has no meaningful expiration, should become a supported implementation, corrects an incorrect requirement, changes requirement intent, changes authority, or changes global/profile architecture.

Global exceptions are prohibited.

### 4.4 Scope

Every exception or waiver has one exact scope. Permitted kinds are:

`text
deployment_instance
release
profile_claim
component_instance
component_release
artifact_instance
development_workspace
migration_action
`

Concrete target identifiers are mandatory. Global, all-deployment, all-profile, all-future-release, wildcard, or indefinite scopes are prohibited.

### 4.5 No implicit inheritance

An exception granted to one object does not apply to another deployment, release, component, profile, child profile, overlay, replacement artifact, or cloned workspace. Every additional target requires its own registered exception or an explicit bounded multi-target risk unit.

### 4.6 Human authority

Only a named human owner may accept residual risk.

An AI agent may identify the need, draft a proposal, calculate impact, identify affected requirements and locks, recommend controls, and validate completeness. It SHALL NOT approve an exception, accept risk, extend expiration, activate a waiver, change the risk rating, or attest control effectiveness without evidence.

### 4.7 Owners

Every deviation has a requester, requirement owner, risk owner, control owner, remediation owner, and approver. One person may hold multiple roles only where separation-of-duty rules allow it. High-assurance and security-sensitive deviations require distinct requester and approver identities.

### 4.8 Non-waivable authority

The following cannot be waived or excepted:

1. authority order;
2. single canonical ownership;
3. decision closure;
4. prohibition on unresolved active authority;
5. prohibition on manual edits to generated authority;
6. permanent identifier reservation;
7. requirement traceability;
8. Interfile Alignment Lock enforcement;
9. prohibition on direct writes to another component’s authoritative source tables;
10. separation of Resource Governor and Governance Policy Runtime;
11. separation of Publication Gateway, UCKK Publication Bridge, and UCKK Import Bridge responsibilities;
12. global absence of native AI capabilities;
13. non-authoritative status of external AI output;
14. explicit profile scoping;
15. prohibition on treating recipes as implicit normative authority;
16. prohibition on false conformance claims;
17. prohibition on secret inclusion in ordinary logs, receipts, images, or exports;
18. accepted human risk ownership.

The canonical list is owned by `generated/exception-index.json#/non_waivable_authority`.

### 4.9 Compensating controls

Every waiver and every non-equivalent exception has concrete, implementable, assigned, testable, evidenced, and proportionate controls.

Invalid controls include “monitor carefully,” “use best efforts,” “be cautious,” and “review later.”

### 4.10 Duration

Permanent waivers are prohibited.

A waiver may remain active for no more than 90 calendar days and may be renewed once for at most another 90 days. Renewal requires a new accepted decision, updated risk assessment and evidence, a new expiration, and demonstrated remediation progress.

An exception may remain active for no more than 365 calendar days or one major documentation version, whichever occurs first. Permanent alternatives are incorporated into canonical requirements or profile contracts.

### 4.11 Conformance effect

An active exception may support a conformance claim only when it preserves requirement intent, demonstrates equivalent or stronger controls, is permitted by the conformance model, has evidence, and is disclosed.

A waiver means the requirement is not fully satisfied. The claim is labeled `conformant_with_active_waiver`, never simply `conformant`. A waiver affecting a mandatory sovereign or high-assurance control may block that profile claim entirely.

---

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-DOC-EXC-001,REQ-DOC-EXC-002,REQ-DOC-EXC-003,REQ-DOC-EXC-004,REQ-DOC-EXC-005,REQ-DOC-EXC-006,REQ-DOC-EXC-007,REQ-DOC-EXC-008,REQ-DOC-EXC-009,REQ-DOC-EXC-010,REQ-DOC-EXC-011,REQ-DOC-EXC-012,REQ-DOC-EXC-013,REQ-DOC-EXC-014,REQ-DOC-EXC-015,REQ-DOC-EXC-016,REQ-DOC-EXC-017,REQ-DOC-EXC-018,REQ-DOC-EXC-019,REQ-DOC-EXC-020,REQ-DOC-EXC-021,REQ-DOC-EXC-022,REQ-DOC-EXC-023,REQ-DOC-EXC-024,REQ-DOC-EXC-025,REQ-DOC-EXC-026 -->
- **REQ-DOC-EXC-001 — SHALL:** Every exception and waiver be registered in `generated/exception-index.json`.
- **REQ-DOC-EXC-002 — SHALL:** Every exception and waiver reference an accepted owner decision.
- **REQ-DOC-EXC-003 — SHALL:** Every exception and waiver identify exact affected requirements, locks, profiles, components, releases, artifacts, or workspaces.
- **REQ-DOC-EXC-004 — SHALL:** Every exception and waiver have a concrete bounded scope.
- **REQ-DOC-EXC-005 — SHALL NOT:** An exception or waiver use global or indefinite scope.
- **REQ-DOC-EXC-006 — SHALL NOT:** An exception or waiver be inherited implicitly by another object.
- **REQ-DOC-EXC-007 — SHALL:** Every exception and waiver identify a named human risk owner.
- **REQ-DOC-EXC-008 — SHALL NOT:** An AI agent approve an exception, accept residual risk, or extend an expiration.
- **REQ-DOC-EXC-009 — SHALL:** Every waiver define compensating controls.
- **REQ-DOC-EXC-010 — SHALL:** Every waiver define a remediation plan, remediation owner, milestones, and expiration date.
- **REQ-DOC-EXC-011 — SHALL:** Every exception demonstrate equivalent or stronger satisfaction of the affected requirement’s intent.
- **REQ-DOC-EXC-012 — SHALL:** Every active exception and waiver have validation evidence for its controls.
- **REQ-DOC-EXC-013 — SHALL NOT:** Non-waivable authority be bypassed through an exception or waiver.
- **REQ-DOC-EXC-014 — SHALL NOT:** A waiver remain active for more than 90 calendar days without one explicitly approved renewal.
- **REQ-DOC-EXC-015 — SHALL NOT:** A waiver be renewed more than once.
- **REQ-DOC-EXC-016 — SHALL NOT:** An exception remain active beyond 365 calendar days or one major documentation version, whichever occurs first.
- **REQ-DOC-EXC-017 — SHALL:** An exception or waiver expire automatically at its declared expiration time.
- **REQ-DOC-EXC-018 — SHALL:** Expiration revoke the deviation before the affected object may continue as compliant.
- **REQ-DOC-EXC-019 — SHALL:** Every release and conformance claim disclose applicable active exceptions and waivers.
- **REQ-DOC-EXC-020 — SHALL NOT:** A release with an undisclosed active waiver claim unqualified conformance.
- **REQ-DOC-EXC-021 — SHALL:** Every exception and waiver be included in impact analysis and traceability.
- **REQ-DOC-EXC-022 — SHALL:** Every exception and waiver record approval, activation, renewal, revocation, expiration, and closure events.
- **REQ-DOC-EXC-023 — SHALL:** Revocation or expiration trigger revalidation of affected objects and claims.
- **REQ-DOC-EXC-024 — SHALL NOT:** A ticket, comment, prompt, ADR draft, or prose note function as an active exception.
- **REQ-DOC-EXC-025 — SHALL:** Repeated or broadly required deviations trigger review of the canonical requirement rather than repeated exception issuance.
- **REQ-DOC-EXC-026 — MAY:** An exception be closed before expiration when the target becomes compliant or the affected capability is removed.
<!-- GENERATED:REQUIREMENTS:END -->

---

## 6. Procedures or State Transitions

Lifecycle states:

`text
proposed
under_review
approved
active
suspended
expired
revoked
superseded
closed
rejected
`

A proposal has no authority. Review evaluates scope, requirements, risk, controls, evidence, remediation, and conformance effect. Approval requires accepted decisions, owner reviews, risk acceptance, control and remediation ownership, traceability, successful validation, and no non-waivable lock violation. Activation occurs only after controls and evidence exist and emits a receipt.

Only waivers may be renewed, once, through a new decision and fresh evidence. A deviation is revoked when controls fail, scope changes, risk grows, evidence becomes invalid, use exceeds scope, linked authority changes, or approval was based on incorrect information. Closure records compliance, capability removal, target retirement, canonical requirement change, or replacement by a supported alternative.

---

## 7. Failure States and Safe Degradation

An unregistered deviation is invalid and causes the requirement and conformance claim to fail.

A missing accepted decision keeps the deviation inactive.

Expiration automatically revokes applicability and triggers revalidation. The capability must comply, disable, or enter documented safe degradation.

A failed compensating control suspends the deviation and requires new evidence before reactivation.

A scope mismatch means the deviation does not apply; no wildcard, inheritance, nearest match, or naming similarity is accepted.

Missing or stale evidence blocks activation or suspends an active deviation.

If the exception registry cannot be verified, no new deviation activates and sensitive operations relying on one fail closed.

An omitted waiver invalidates a conformance claim and requires corrected evidence.

---

## 8. Cross-Component Interactions

Every exception references an accepted decision and exact requirement IDs. It does not modify the requirements registry.

Validators check non-waivable locks, profile locks, component boundaries, security, lifecycle, and development isolation.

Traceability links decision, requirement, lock, target, control, test, evidence, release, claim, and remediation.

Profile contracts may further restrict exception eligibility. Release Sets record active exception and waiver IDs. Generated conformance reports disclose IDs, dates, requirements, conformance effect, evidence status, and remediation status.

Failed controls enter incident response but are not automatically reactivated after incident closure.

AI context packages include only applicable deviations, exact scope, expiration, requirements, prohibited generalization, and conformance effect.

---

## 9. Decision Closure and Prohibited Assumptions

Prohibited assumptions include: an implementation constraint automatically creates an exception; an ADR automatically grants a waiver; a ticket is risk acceptance; an expired waiver remains valid; an exception applies to future releases or similar components; a deployment exception applies to a profile; a profile exception applies globally; a deviation can override canonical ownership; a waiver may be hidden from conformance evidence; vague controls are sufficient; repeated waivers are permanent operating policy; an AI recommendation is approval; absent approval means consent; missing expiration means indefinite validity; offline status justifies waiving security; or development convenience proves sovereign conformance.

When required information is absent, the request remains inactive. No default approval is inferred.

---

## 10. Validation Criteria

Validation confirms schema conformance, unique IDs, accepted decisions, resolvable requirements and locks, concrete targets, named owners, valid duration, permitted state transitions, prohibited-scope absence, no implicit inheritance, no non-waivable impact, valid renewal counts, machine-readable expiration, assigned controls, current evidence, accurate conformance labels, human approvals, separation of duties, and disclosure in releases and claims.

Required commands:

`bash
python docs/tools/check_decision_closure.py
python docs/tools/check_interfile_locks.py
python docs/tools/check_traceability.py
python docs/tools/check_profile_inheritance.py
python docs/tools/generate_docs.py --check
python docs/tools/validate_docs.py
`

---

## 11. Non-Normative Examples

### 11.1 Valid exception characteristics

A valid exception names one deployment or release, references an accepted decision and exact requirement, describes an equivalent alternative control, names human owners, links tests and evidence, declares an exact expiration, and discloses its conformance effect.

### 11.2 Valid temporary waiver characteristics

A valid waiver names one target, explains the temporary constraint, defines concrete compensating controls, includes a remediation plan and milestones, names human risk and approval authorities, expires within 90 days, and labels conformance accurately.

### 11.3 Invalid global exception

`json
{
 "scope": {"kind": "global", "targets": ["all"]},
 "description": "Allow all components to share databases where convenient."
}
`

This is invalid because it changes architecture and conflicts with data-authority locks.

### 11.4 Invalid indefinite waiver

`json
{"expires_at": "until_fixed"}
`

Expiration must be an exact timestamp within the permitted duration.

### 11.5 AI-generated proposal

An AI agent may draft:

`json
{
 "status": "proposed",
 "approval_status": "human_approval_required",
 "risk_acceptance": null
}
`

It may not convert that object to active approval without recorded human authorization.

---

## Final Rule

> An exception is a bounded, evidenced alternative that preserves architectural intent. A waiver is a temporary, disclosed acceptance of incomplete compliance. Neither may silently change the architecture, override non-waivable authority, or become permanent through repetition.
