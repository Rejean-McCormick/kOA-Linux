<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-OPS-012",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "operations",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/decision-index.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/components/audit-broker.component.json",
    "contracts/components/resource-governor.component.json",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/components/identity-and-trust.component.json",
    "contracts/components/publication-gateway.component.json",
    "contracts/artifact-contracts/decision-receipt.schema.json",
    "contracts/artifact-contracts/provenance-receipt.schema.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-OPS-INC-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-AUD-001",
    "DEC-PROFILE-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-OPS-INC-001",
    "REQ-OPS-INC-002",
    "REQ-OPS-INC-003",
    "REQ-OPS-INC-004",
    "REQ-OPS-INC-005",
    "REQ-OPS-INC-006",
    "REQ-OPS-INC-007",
    "REQ-OPS-INC-008",
    "REQ-OPS-INC-009",
    "REQ-OPS-INC-010",
    "REQ-OPS-INC-011",
    "REQ-OPS-INC-012",
    "REQ-OPS-INC-013",
    "REQ-OPS-INC-014",
    "REQ-OPS-INC-015",
    "REQ-OPS-INC-016",
    "REQ-OPS-INC-017",
    "REQ-OPS-INC-018",
    "REQ-OPS-INC-019",
    "REQ-OPS-INC-020",
    "REQ-OPS-INC-021",
    "REQ-OPS-INC-022",
    "REQ-OPS-INC-023",
    "REQ-OPS-INC-024",
    "REQ-OPS-INC-025",
    "REQ-OPS-INC-026",
    "REQ-OPS-INC-027",
    "REQ-OPS-INC-028",
    "REQ-OPS-INC-029",
    "REQ-OPS-INC-030"
  ],
  "lock_ids": [
    "LOCK-OPS-004",
    "LOCK-OPS-005",
    "LOCK-OPS-006",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-PROFILE-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-DOC-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-009",
    "DOC-GOV-010",
    "DOC-CONST-002",
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-SYS-002",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-006",
    "DOC-SYS-007",
    "DOC-SYS-008",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-017",
    "DOC-SYS-019",
    "DOC-SYS-020",
    "DOC-PROFILE-001",
    "DOC-PROFILE-003",
    "DOC-COMP-000",
    "DOC-LIFE-002",
    "DOC-LIFE-012",
    "DOC-LIFE-013",
    "DOC-LIFE-014",
    "DOC-SEC-004",
    "DOC-SEC-015",
    "DOC-SEC-020",
    "DOC-OPS-000",
    "DOC-OPS-001",
    "DOC-OPS-002",
    "DOC-OPS-007",
    "DOC-OPS-008",
    "DOC-OPS-009",
    "DOC-OPS-011",
    "DOC-OPS-013",
    "DOC-OPS-016"
  ],
  "tags": [
    "operations",
    "incident-response",
    "containment",
    "recovery",
    "incident-command",
    "security-incidents",
    "data-incidents",
    "release-incidents",
    "trust-incidents",
    "evidence"
  ]
}
KOA:DOC-META:END -->

# Incident Response

## 1. Purpose

This document defines the incident-response model for the kOA operating environment.

Incident response coordinates detection, qualification, containment, evidence preservation, recovery, communication, recourse, and corrective action without collapsing component, policy, resource, trust, lifecycle, publication, or data authority into a temporary incident role.

The model treats an incident as a controlled operating state. Urgency can change cadence and priority, but it does not erase authority boundaries, evidence requirements, tenant isolation, selective disclosure, or the need to preserve a valid recoverable state.

## 2. Scope

This document applies to:

- operational availability and performance incidents;
- security and privilege incidents;
- identity, credential, key, and trust-root incidents;
- privacy, disclosure, consent, and cultural-rights incidents;
- data-integrity, migration, backup, and restore incidents;
- artifact, release, verification, activation, rollback, and supply-chain incidents;
- publication and external-integration incidents;
- resource exhaustion and scheduling incidents;
- node, hub, build-farm, control-plane, development, user, sovereign, and offline profiles;
- detection, triage, declaration, classification, command, containment, investigation, evidence, communication, recovery, validation, closure, recourse, and corrective action;
- break-glass use during an incident;
- public, tenant, operator, rights-holder, partner, and regulator communication where applicable.

This document does not:

- make every alert an incident;
- replace disaster recovery, backup, restore, maintenance, or break-glass contracts;
- grant a universal incident administrator identity;
- authorize direct writes to component-owned state;
- prescribe one ticketing, paging, messaging, forensics, case-management, or communication platform;
- require every profile to use the same incident team or communication mechanism;
- permit disclosure of restricted evidence merely because an incident is severe;
- make an incident record the canonical owner of component state or root-cause facts.

## 3. Canonical References

| Canonical reference | Ownership role |
| --- | --- |
| `generated/component-catalog.json` and component contracts | Own component state, failure behavior, containment interfaces, repair, recovery, and prohibited direct writes. |
| `contracts/profiles/*.profile.json` | Own profile-specific command topology, offline behavior, escalation, retention, assurance, and communication requirements. |
| `contracts/components/governance-policy-runtime.component.json` | Owns policy decisions for restricted access, emergency changes, disclosure, exceptions, and break-glass use. |
| `contracts/components/resource-governor.component.json` | Owns resource admission, priority, queues, throttling, and response-work limits. |
| `contracts/components/identity-and-trust.component.json` | Owns responder, service, signer, credential, trust, validity, and revocation verification. |
| `contracts/components/audit-broker.component.json` | Owns declared incident-evidence custody, restricted views, access records, and receipts. |
| `contracts/components/publication-gateway.component.json` | Owns public and cross-domain incident publication boundaries. |
| `contracts/artifact-contracts/decision-receipt.schema.json` | Defines machine-readable incident decisions, actions, access, and transition receipts. |
| `contracts/artifact-contracts/provenance-receipt.schema.json` | Defines provenance evidence for affected artifacts and derived diagnostic material. |
| `generated/requirements-index.json` | Owns the normative statements displayed in Section 5. |
| `generated/assertion-index.json` | Owns incident command, evidence, recovery, data, governance, profile, lifecycle, and canonical-ownership assertions. |
| `generated/traceability.json` | Owns decision, requirement, lock, incident class, component, profile, test, and evidence relationships. |
| `generated/test-catalog.json` and `generated/evidence-catalog.json` | Own incident-response test and evidence identities. |

This Markdown document explains incident-response behavior. Exact incident classes, severity values, role identities, escalation paths, time targets, communication routes, and profile assignments remain machine-readable canonical data.

## 4. Model and Responsibilities

### 4.1 Incident, problem, change, and disaster

The model distinguishes:

| Object | Meaning |
| --- | --- |
| Incident | Active or recent harmful deviation requiring coordinated response |
| Problem | Underlying condition or causal pattern requiring analysis and correction |
| Emergency change | Urgent authorized modification intended to contain or recover |
| Disaster | Incident whose scope requires disaster-recovery activation |
| Security case | Restricted investigation with security evidence and access controls |
| Recourse case | Challenge, correction, or review related to incident impact or response |

One event can create several linked objects. Their owners and lifecycle states remain separate.

### 4.2 Incident classes

The following classes explain common response domains and can coexist:

- operational availability;
- performance or resource exhaustion;
- security compromise;
- privilege misuse;
- identity or credential compromise;
- trust-root or signer compromise;
- privacy or disclosure;
- cultural rights or consent;
- data corruption or loss;
- artifact or release integrity;
- publication error;
- external integration failure;
- infrastructure or environmental failure;
- disaster-recovery activation.

Classification remains evidence-based and can be refined as new facts are validated.

### 4.3 Incident command

Incident command coordinates the response.

Core responsibilities include:

- maintain incident identity and current objective;
- declare command roles;
- establish decision cadence;
- maintain the confirmed-fact record;
- identify affected and unaffected scope;
- coordinate component owners;
- resolve dependencies and priorities;
- track actions and evidence;
- coordinate communications;
- determine readiness for transition or closure.

Incident command cannot execute an action that belongs to another authority merely by recording it in the incident plan.

### 4.4 Roles

Common roles include:

| Role | Responsibility |
| --- | --- |
| Incident commander | Coordinates objectives, priorities, cadence, and role assignments |
| Component owner | Determines and executes component-specific containment and recovery |
| Operations lead | Coordinates operational state, capacity, dependencies, and restoration |
| Security lead | Coordinates compromise analysis, containment, trust, and restricted evidence |
| Evidence lead | Preserves custody, access records, and proof relationships |
| Communications lead | Produces authorized internal, tenant, partner, and public updates |
| Rights or privacy lead | Protects personal, consent, cultural-rights, and recourse obligations |
| Recovery lead | Coordinates restore, rollback, forward repair, and validation |
| Scribe | Maintains timeline, decisions, actions, uncertainties, and receipts |

One person can hold several roles in a small profile, but each authority remains explicit.

### 4.5 Incident state

The explanatory state sequence is:

```text
detected
under_assessment
declared
contained
recovery_in_progress
monitoring
resolved
closed
```

An incident can also be `blocked`, `escalated`, `merged`, `split`, or transferred to disaster recovery according to its canonical contract.

Resolution means harmful behavior is stopped and required capability is restored or replaced. Closure additionally requires evidence, communication, recourse, ownership, and corrective-action completion or transfer.

### 4.6 Severity and impact

Severity considers:

- human or community safety;
- confidentiality;
- integrity;
- availability;
- authority or trust compromise;
- affected tenant and user count;
- public or external exposure;
- cultural-rights impact;
- release or supply-chain scope;
- recovery complexity;
- duration and propagation;
- availability of safe degraded operation.

Severity is a coordination and escalation input. It is not a substitute for authorization.

### 4.7 Containment

Containment limits harm while preserving evidence and unaffected capabilities.

Containment can include:

- rejecting new requests;
- isolating a component, node, tenant, workspace, credential, artifact, integration, or release channel;
- pausing jobs;
- applying resource throttles;
- revoking credentials;
- blocking publication;
- freezing an artifact transition;
- switching to a known valid state;
- disabling a bounded optional capability;
- preserving a snapshot or evidence view.

Each action uses the owner interface for the affected boundary.

### 4.8 Evidence and timeline

The incident timeline distinguishes:

- observed signal;
- reported claim;
- working hypothesis;
- confirmed fact;
- authority decision;
- executed action;
- result;
- communication;
- correction or supersession.

Evidence records classification, source, custody, time quality, integrity, transformation, access, export, retention, and disposition. Restricted proof does not become public incident content.

### 4.9 Communications

Communication audiences can include:

- responders;
- affected component owners;
- tenant administrators;
- affected users or rights holders;
- partners and integration owners;
- public audiences;
- regulators or designated authorities;
- maintainers and release owners.

Each update identifies what is confirmed, what remains unknown, current impact, protective actions, and the condition for the next update.

### 4.10 Recovery and corrective action

Recovery restores a valid operating state.

It can use:

- restart or replacement;
- rollback;
- forward repair;
- restore;
- data repair;
- credential rotation;
- trust-store replacement;
- artifact withdrawal;
- publication correction or withdrawal;
- integration isolation;
- resource reallocation;
- disaster recovery.

Corrective action addresses causes and control gaps after immediate recovery. It remains assigned to canonical owners and is tracked separately from incident closure when necessary.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-OPS-INC-001,REQ-OPS-INC-002,REQ-OPS-INC-003,REQ-OPS-INC-004,REQ-OPS-INC-005,REQ-OPS-INC-006,REQ-OPS-INC-007,REQ-OPS-INC-008,REQ-OPS-INC-009,REQ-OPS-INC-010,REQ-OPS-INC-011,REQ-OPS-INC-012,REQ-OPS-INC-013,REQ-OPS-INC-014,REQ-OPS-INC-015,REQ-OPS-INC-016,REQ-OPS-INC-017,REQ-OPS-INC-018,REQ-OPS-INC-019,REQ-OPS-INC-020,REQ-OPS-INC-021,REQ-OPS-INC-022,REQ-OPS-INC-023,REQ-OPS-INC-024,REQ-OPS-INC-025,REQ-OPS-INC-026,REQ-OPS-INC-027,REQ-OPS-INC-028,REQ-OPS-INC-029,REQ-OPS-INC-030 -->
- **REQ-OPS-INC-001 — SHALL:** Every incident has a stable incident identity, incident class, severity, status, owner, commander, affected scope, detection time, declaration time, source evidence, and current response objective.
- **REQ-OPS-INC-002 — SHALL:** Incident classification distinguishes operational, security, privacy, cultural-rights, data-integrity, trust, release, publication, resource, external-integration, and disaster-recovery concerns when applicable.
- **REQ-OPS-INC-003 — SHALL:** An incident declares affected components, tenants, profiles, nodes, workspaces, artifacts, release channels, data domains, capabilities, integrations, and audiences only to the extent currently supported by evidence.
- **REQ-OPS-INC-004 — SHALL NOT:** Unverified assumptions, incomplete alerts, public reports, or operator intuition are represented as confirmed incident facts.
- **REQ-OPS-INC-005 — SHALL:** Incident command coordinates objectives, priorities, dependencies, communications, evidence, and decision cadence without acquiring component data ownership or execution authority.
- **REQ-OPS-INC-006 — SHALL NOT:** An incident commander, communications role, investigator, observer, dashboard, or ticketing system writes directly to component-owned authoritative state.
- **REQ-OPS-INC-007 — SHALL:** Containment, isolation, revocation, rollback, shutdown, throttling, data repair, publication withdrawal, and recovery actions execute only through the active authority that owns the affected boundary.
- **REQ-OPS-INC-008 — SHALL:** Every response action records the requesting authority, executing authority, target, purpose, authorization, resource admission when applicable, start time, completion state, result, and evidence references.
- **REQ-OPS-INC-009 — SHALL:** Incident severity is determined from declared impact dimensions including safety, confidentiality, integrity, availability, authority, tenant scope, public exposure, recovery complexity, and time sensitivity.
- **REQ-OPS-INC-010 — SHALL NOT:** Severity alone grants privileged access, broad disclosure, irreversible action, policy override, or bypass of required evidence.
- **REQ-OPS-INC-011 — SHALL:** A response objective identifies the desired protected state, success criteria, time horizon, prohibited side effects, and authority responsible for confirming completion.
- **REQ-OPS-INC-012 — SHALL:** Containment preserves unaffected capabilities, tenants, profiles, components, data, and release channels whenever the active contracts permit bounded isolation.
- **REQ-OPS-INC-013 — SHALL NOT:** Containment silently destroys evidence, overwrites source state, broadens trust, weakens policy, substitutes artifacts, or disables unrelated capabilities.
- **REQ-OPS-INC-014 — SHALL:** Evidence preservation begins at declaration or earlier when a signal is placed under investigation and records source identity, custody, classification, integrity, time quality, transformations, access, and disposition.
- **REQ-OPS-INC-015 — SHALL:** Restricted incident evidence, diagnostics, personal data, secrets, private keys, exploit details, cultural-rights material, and tenant-confidential data remain selectively disclosed.
- **REQ-OPS-INC-016 — SHALL:** Every access to restricted incident evidence and every export, diagnostic package, disclosure, legal hold, redaction, correction, withdrawal, or destruction action produces a machine-readable receipt.
- **REQ-OPS-INC-017 — SHALL:** External and public communications identify confirmed facts, current impact, affected audience, protective actions, uncertainty, next update condition, and responsible communication authority.
- **REQ-OPS-INC-018 — SHALL NOT:** Incident communications expose secret values, private keys, unrestricted personal data, protected cultural material, private proof, exploit-enabling details, or unverified attribution.
- **REQ-OPS-INC-019 — SHALL:** A break-glass action is used only through the active break-glass contract and records activation basis, scope, actor, duration, safeguards, performed actions, review, revocation, and follow-up evidence.
- **REQ-OPS-INC-020 — SHALL:** A trust or credential incident triggers scoped revocation, cached-result invalidation, dependent artifact and session review, replacement, and recovery according to the affected trust contracts.
- **REQ-OPS-INC-021 — SHALL:** A release or artifact incident identifies affected artifact identities, versions, classes, channels, Release Sets, targets, active states, verification results, rollback options, and forward-repair options.
- **REQ-OPS-INC-022 — SHALL:** A data-integrity incident preserves source-component authority and applies repair, restore, migration, rollback, or forward-repair only through the owning component's active contract.
- **REQ-OPS-INC-023 — SHALL:** Incident queues, evidence capture, diagnostics, retries, communications, investigations, exports, and recovery work remain bounded by active contracts and effective profile resource envelopes.
- **REQ-OPS-INC-024 — SHALL:** Offline and disconnected profiles maintain local incident identity, command, evidence, containment, communication, trust, and recovery procedures and define later synchronization or reconciliation.
- **REQ-OPS-INC-025 — SHALL:** An incident transitions through declared states and cannot close until containment, recovery, validation, evidence, communication, ownership, and follow-up conditions are resolved or explicitly transferred.
- **REQ-OPS-INC-026 — SHALL:** Recovery validation confirms the restored capability, authoritative state, trust context, artifact state, policy state, resource state, data integrity, observability, and residual risk within the affected scope.
- **REQ-OPS-INC-027 — SHALL:** Incident closure records final classification, timeline, impact, affected scope, root cause or causal findings, actions, evidence, recovery, residual risk, notifications, recourse, and assigned corrective work.
- **REQ-OPS-INC-028 — SHALL NOT:** A post-incident review silently rewrites the incident timeline, source evidence, decisions, attribution, or response receipts.
- **REQ-OPS-INC-029 — SHALL:** Validation detects undeclared incidents, duplicate identities, missing command roles, stale severity, unauthorized actions, evidence gaps, disclosure violations, unbounded response work, incomplete recovery, and closure without assigned corrective ownership.
- **REQ-OPS-INC-030 — SHALL:** Every active incident-response requirement is traceable to accepted decisions, applicable locks, validation tests, and required evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Detecting and declaring an incident

Declaration:

1. records the initiating signal or report;
2. assigns an incident identity;
3. verifies source and available evidence;
4. distinguishes confirmed facts from hypotheses;
5. identifies initial affected scope;
6. assigns provisional class and severity;
7. appoints command roles;
8. establishes the first response objective;
9. starts evidence preservation and communication cadence;
10. emits the declaration receipt.

### 6.2 Triage and containment

Triage and containment:

1. identify active harm and propagation paths;
2. identify unaffected capabilities and tenants;
3. prioritize safety, authority, integrity, confidentiality, and continuity;
4. propose bounded containment actions;
5. resolve the owner, authorization, and resource requirements for each action;
6. execute through owner interfaces;
7. verify results and unintended effects;
8. update incident scope, facts, and severity;
9. preserve action receipts and evidence;
10. repeat within bounded cadence.

### 6.3 Investigating

Investigation:

1. defines questions and evidence scope;
2. obtains restricted-access authorization;
3. preserves relevant source and derived evidence;
4. validates timeline, identity, trust, artifact, data, policy, and resource context;
5. records hypotheses separately from findings;
6. tests causal explanations without mutating source evidence;
7. identifies containment and recovery implications;
8. records causal findings and confidence;
9. closes temporary access and investigation material when no longer required.

### 6.4 Communicating

Communication:

1. selects the audience and disclosure contract;
2. resolves confirmed facts and authorized fields;
3. identifies current impact and protective action;
4. records uncertainty and excluded speculation;
5. applies privacy, security, rights, and tenant boundaries;
6. publishes through the appropriate authorized route;
7. records the communication and approval receipt;
8. corrects or supersedes prior updates visibly when facts change.

### 6.5 Recovering and validating

Recovery:

1. identifies the desired valid target state;
2. selects rollback, restore, replacement, repair, or forward-repair path;
3. validates artifacts, data, trust, policy, resource, and profile prerequisites;
4. executes through owning authorities;
5. verifies health, readiness, data integrity, trust, compatibility, and evidence;
6. monitors for recurrence and residual effects;
7. transitions the incident to monitoring or resolved;
8. records recovery and validation receipts.

### 6.6 Closing and reviewing

Closure:

1. confirms that harmful behavior is contained;
2. confirms recovery or accepted degraded operation;
3. confirms required communications and notifications;
4. confirms evidence and custody completeness;
5. records residual risk and open corrective work;
6. assigns every corrective action to an owner and due condition;
7. records recourse and affected-subject handling;
8. publishes authorized lessons and restricted findings separately;
9. records the final timeline and closure decision;
10. transitions the incident to closed.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Preserved authority | Blocked or degraded behavior | Evidence |
| --- | --- | --- | --- | --- |
| Detection signal is ambiguous | Keep the case under assessment and preserve evidence | Existing operating authority | Premature confirmed classification | Assessment record |
| Incident commander is unavailable | Activate declared alternate command | Component and local authority | Central coordination | Role-transfer receipt |
| Component owner is unavailable | Use declared escalation or local safe-state contract | Existing component state where safe | Owner-dependent change | Escalation record |
| Policy authority is unavailable | Keep gated access and irreversible action blocked unless active break-glass terms apply | Existing policy state | New gated action | Policy-path state |
| Resource admission is constrained | Prioritize declared incident work and bound diagnostics | Core affected capability | Lower-priority response work | Resource-decision receipt |
| Evidence path is unavailable | Apply local receipt, bounded queue, or synchronous-fail behavior | Source-component authority | Central evidence custody | Evidence-path state |
| Trust or credentials are compromised | Use independent trusted channels and scoped revocation | Unaffected trust domains | Compromised identities and sessions | Trust-incident receipt |
| Communication route is unavailable | Use declared alternate route and record gaps | Confirmed facts and internal command | Audience delivery | Communication-path state |
| Containment increases impact | Stop, roll back, or enter forward repair through owner contract | Last valid recoverable state | Failed containment path | Action and recovery receipt |
| Recovery validation fails | Return to containment or select another recovery path | Preserved evidence and last valid state | Incident resolution | Validation failure |
| Offline node cannot reach central command | Continue local profile-owned incident command and evidence | Local component authority | Central coordination | Offline incident record |
| Public information is incorrect | Publish a visible correction or supersession | Original communication history | Reliance on stale update | Correction receipt |
| Incident scope expands | Reclassify severity, roles, objectives, and affected authorities | Existing confirmed facts | Obsolete response plan | Scope-change receipt |
| Legal or rights obligations are unresolved | Keep affected disclosure or disposition blocked | Protected evidence and affected rights | Closure of relevant obligations | Obligation record |
| Corrective owner is missing | Keep closure blocked or assign through the declared authority | Recovered system state | Final incident closure | Ownership gap |
| Disaster criteria are met | Transfer coordination to disaster recovery without losing incident identity or evidence | Incident history and component authority | Ordinary incident-only process | Transfer receipt |

## 8. Cross-Component Interactions

### 8.1 Component owners

Component owners expose containment, status, repair, rollback, restore, and recovery operations through active contracts.

Incident command requests and coordinates these actions. It does not bypass their interfaces or write to private storage.

### 8.2 Governance Policy Runtime

Governance Policy Runtime evaluates:

- restricted evidence access;
- emergency changes;
- disclosure;
- cross-tenant actions;
- retention or legal hold;
- exceptions;
- break-glass use.

The policy result does not perform the action.

### 8.3 Resource Governor

Resource Governor can prioritize and admit incident diagnostics, containment, recovery, communication, and evidence work within bounded envelopes.

Resource priority does not grant access, privilege, or component mutation authority.

### 8.4 Identity and Trust

Identity and Trust verifies responders, owners, signers, communication authorities, external recipients, and replacement credentials.

A compromised trust path is isolated from incident command and replaced through the applicable trust contract.

### 8.5 Audit Broker

Audit Broker preserves incident decisions, restricted evidence, access records, communications, and action receipts.

Operational views can display authorized outcomes while private proof remains restricted.

### 8.6 Publication Gateway

Public and cross-domain incident updates use Publication Gateway when they cross a disclosure or authority boundary.

The gateway controls publication and withdrawal. It does not own the incident, source evidence, or component recovery.

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Effect |
| --- | --- |
| `DEC-OPS-INC-001` | Establishes explicit incident command, evidence, containment, communication, recovery, validation, and closure without temporary authority collapse. |
| `DEC-DATA-001` | Preserves component data ownership throughout containment, investigation, repair, restore, and recovery. |
| `DEC-GOV-001` | Preserves the distinction between policy authorization, resource admission, and execution authority. |
| `DEC-AUD-001` | Keeps public incident evidence separate from restricted private proof and records restricted evidence access. |
| `DEC-PROFILE-001` | Keeps escalation, offline command, assurance, retention, and implementation mechanisms profile-scoped. |
| `DEC-REL-001` | Preserves artifact identity, verification, channel ownership, rollback, and forward-repair during release incidents. |

### Prohibited assumptions

- every alert is an incident;
- incident severity creates universal administrator authority;
- incident command owns component state;
- urgency permits direct database changes;
- a dashboard state is confirmed incident fact;
- containment can destroy evidence for convenience;
- a shutdown is always safer than bounded degradation;
- rollback is always possible;
- a public update can include private proof;
- an investigator can inspect every tenant;
- a compromised credential can authorize its own replacement;
- break-glass action can remain open-ended;
- central command is required for local offline containment;
- recovery is complete when a process restarts;
- incident resolution automatically satisfies recourse and notification;
- post-incident review can rewrite history;
- a ticketing tool is the canonical authority for component state;
- one profile's escalation times and roles apply globally;
- a severe incident permits unbounded diagnostics or telemetry;
- corrective work can remain ownerless after closure.

## 10. Validation Criteria

This document is conformant when:

1. `DOC-OPS-012` is active at `08-operations/12-incident-response.md`.
2. Every canonical reference resolves.
3. Every listed decision exists with status `accepted`.
4. Every requirement in Section 5 exists with identical strength, statement, scope, owner, source decision, and validation mapping.
5. Every listed lock exists and is active.
6. Every incident has a unique identity, class, severity, status, owner, commander, scope, timeline, evidence, and objective.
7. Confirmed facts, hypotheses, decisions, actions, results, and communications remain distinguishable.
8. Incident command cannot mutate component-owned state directly.
9. Every containment and recovery action resolves owner, authorization, resource admission, target, and receipt.
10. Severity does not grant privilege or disclosure authority.
11. Containment preserves unaffected capability and evidence where contracts permit.
12. Restricted evidence and diagnostics enforce classification and selective access.
13. Every restricted access, export, hold, redaction, correction, and disposition action maps to a receipt.
14. Public communications contain only confirmed and authorized information.
15. Break-glass use remains scoped, time-bounded, reviewable, and revocable.
16. Trust incidents invalidate affected reusable trust and verification results.
17. Release incidents preserve artifact identities, channels, active state, verification, and recovery relationships.
18. Data incidents use only owner-controlled repair, restore, migration, rollback, or forward repair.
19. Incident work and diagnostics remain bounded.
20. Offline profiles define local command, evidence, containment, communication, and reconciliation.
21. Recovery validation covers state, data, trust, artifacts, policy, resources, health, readiness, and residual risk.
22. Closure cannot occur with unresolved containment, evidence, communication, recourse, or corrective ownership.
23. Original evidence and timelines remain immutable while corrections and supersession remain visible.
24. Disaster-recovery transfer preserves incident identity and evidence.
25. Critical incident paths map to tests and evidence.
26. Active prose is English and contains no unresolved-authority marker.
27. No normative keyword appears outside the generated requirement block.
28. The documentation dependency graph remains acyclic.

The validation entry point is:

```bash
python docs/tools/validate_docs.py
```

## 11. Non-Normative Examples

> **Non-normative example:** This example illustrates command without authority transfer.

An incident commander can prioritize isolation of a compromised Orgo worker. The Orgo owner performs the isolation through the component contract; the commander does not edit Orgo storage.

> **Non-normative example:** This example illustrates scoped trust response.

When one release signer is compromised, new signatures within that signer's scope are rejected and affected artifacts are reviewed. Unrelated user-identity and development trust domains remain active.

> **Non-normative example:** This example illustrates public and private evidence separation.

A public update can state that a publication error was contained and corrected. The restricted proof package can retain affected record references, reviewer identities, private communications, and forensic details.

> **Non-normative example:** This example illustrates offline incident command.

A sovereign-offline node can declare and contain a local incident without central connectivity. It retains local receipts and reconciles the timeline after reconnecting.

> **Non-normative example:** This example illustrates recovery validation.

Restarting a service does not resolve a data-integrity incident. The owner also verifies authoritative data, active artifact identity, trust state, health, readiness, and residual risk before resolution.
