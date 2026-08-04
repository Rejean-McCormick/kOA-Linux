<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONST-004",
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
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/profile-catalog.json"
  ],
  "decision_ids": [
    "DEC-CONST-001",
    "DEC-AUTH-001",
    "DEC-IDENT-001",
    "DEC-GOV-001",
    "DEC-PRIV-001",
    "DEC-AI-001",
    "DEC-DATA-001"
  ],
  "requirement_ids": [
    "REQ-CONST-AUTH-001",
    "REQ-CONST-AUTH-002",
    "REQ-CONST-AUTH-003",
    "REQ-CONST-AUTH-004",
    "REQ-CONST-AUTH-005",
    "REQ-CONST-AUTH-006",
    "REQ-CONST-AUTH-007",
    "REQ-CONST-AUTH-008",
    "REQ-CONST-AUTH-009",
    "REQ-CONST-AUTH-010",
    "REQ-CONST-AUTH-011",
    "REQ-CONST-AUTH-012",
    "REQ-CONST-AUTH-013",
    "REQ-CONST-AUTH-014",
    "REQ-CONST-AUTH-015",
    "REQ-CONST-AUTH-016",
    "REQ-CONST-AUTH-017",
    "REQ-CONST-AUTH-018",
    "REQ-CONST-AUTH-019",
    "REQ-CONST-AUTH-020"
  ],
  "lock_ids": [
    "LOCK-AUTH-001",
    "LOCK-AUTH-002",
    "LOCK-AUTH-003",
    "LOCK-AUTH-004",
    "LOCK-AUTH-005",
    "LOCK-GOV-001",
    "LOCK-PRIV-001",
    "LOCK-DATA-001",
    "LOCK-COMP-001",
    "LOCK-AI-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-005",
    "DOC-GOV-009",
    "DOC-GOV-010",
    "DOC-CONST-000",
    "DOC-CONST-002",
    "DOC-CONST-003"
  ],
  "tags": [
    "constitution",
    "explicit-authority",
    "authorization",
    "identity",
    "privilege",
    "governance",
    "fail-closed",
    "receipts"
  ]
}
KOA:DOC-META:END -->

# Explicit Authority

## 1. Purpose

This document defines the constitutional model for explicit authority across the kOA operating environment.

It explains how authority is granted, resolved, constrained, delegated, exercised, evidenced, revoked, and denied. It establishes a common model for governance decisions, operational actions, system privilege, data ownership, disclosure, publication, artifact activation, and conformance claims.

The intended outcome is deterministic authority resolution: an actor or component can determine whether a specific capability is permitted for a specific target and scope without relying on convention, reputation, implementation prevalence, hidden inference, or unrestricted administrator access.

This document explains canonical authority objects. It does not replace their machine-readable owners.

## 2. Scope

This document applies globally to:

- human users, organizations, tenants, roles, delegates, operators, reviewers, auditors, nodes, workloads, services, publishers, signers, artifacts, and external integrations;
- governance authorization, disclosure, consent, exception, and privilege decisions;
- component commands, APIs, events, gateways, data stores, workflows, and state transitions;
- operating-system and host mutations performed through the privileged broker;
- cross-domain publication and withdrawal;
- artifact verification, activation, rollback, revocation, and release;
- emergency and break-glass operations;
- offline operation and synchronization of authority state;
- conformance, release, and evidence claims.

The document applies to every primary deployment profile and overlay. Profile contracts may narrow available capabilities, component presence, resource envelopes, topology, and network exposure. They do not weaken the global authority rules.

This document does not grant authority to any subject. Grants exist only in active canonical objects such as identity and delegation records, profile contracts, policy bundles, component contracts, accepted decisions, artifact contracts, and validated authority releases.

## 3. Canonical References

| Canonical reference | Responsibility in this document |
| --- | --- |
| `generated/authority-manifest.json` | Activates authority releases, registry versions, ownership mappings, and authority order. |
| `generated/decision-index.json` | Owns accepted architectural and owner decisions. |
| `contracts/system.contract.json` | Owns the global authority, trust, offline, AI, and degradation model. |
| `generated/component-catalog.json` | Owns component identities, responsibility boundaries, and authoritative data-domain assignments. |
| `generated/profile-catalog.json` and `contracts/profiles/*.profile.json` | Own component membership, activation mode, overlays, topology, and profile-specific envelopes. |
| `contracts/components/*.component.json` | Own detailed component interfaces, state transitions, stores, workflows, and enforcement points. |
| `generated/requirements-index.json` | Owns the normative statements displayed in section 5. |
| `generated/assertion-index.json` | Owns cross-file authority invariants. |
| `generated/traceability.json` | Owns decision, requirement, lock, test, evidence, exception, and claim relationships. |
| `generated/exception-index.json` | Owns approved, bounded deviations and compensating controls. |
| `generated/test-catalog.json` | Owns test definitions for authority and conformance behavior. |
| `generated/evidence-catalog.json` | Owns test results, receipts, verification records, and claim evidence. |

Repository-relative paths and stable identifiers are the only canonical references used by this document.

## 4. Model and Responsibilities

### 4.1 Authority definition

Authority is a verified permission to perform or determine a bounded action within a declared scope.

A complete authority grant resolves these dimensions:

| Dimension | Meaning |
| --- | --- |
| Subject | The human, role, tenant, organization, node, workload, service, publisher, signer, artifact, or integration exercising the capability. |
| Capability | The permitted read, propose, approve, execute, publish, activate, administer, audit, review, delegate, revoke, or recover action. |
| Target | The object, component, data domain, artifact, node, tenant, audience, release channel, or workflow affected by the action. |
| Scope | The global, profile, overlay, component, artifact-class, toolchain, tenant, environment, or migration boundary. |
| Authority source | The active decision, policy, delegation, profile, contract, trust record, or release that grants the capability. |
| Version | The exact applicable authority version or compatibility range. |
| Conditions | Preconditions, separation-of-duties constraints, consent, classification, resource, network, or review conditions. |
| Validity | Activation time, expiry, revocation state, suspension state, and synchronization status. |
| Obligations | Required confirmation, redaction, evidence, notification, review, retention, or recovery behavior. |
| Evidence | The decision receipt, operation receipt, publication record, activation record, or conformance evidence proving what occurred. |

An incomplete grant is not upgraded through inference. The affected capability remains unavailable until authority is resolvable.

### 4.2 Authority layers

kOA separates the following layers:

1. **Constitutional constraints** define boundaries that ordinary governance cannot bypass.
2. **Owner decisions** define accepted architectural and governance choices.
3. **Identity and trust** establish who or what is acting and which trust domain applies.
4. **Governance policy decisions** determine authorization, disclosure, consent, privilege, activation, and exception outcomes.
5. **Operational authority** permits a component or workflow to initiate and manage bounded work.
6. **System privilege** permits a narrow enforcement mechanism to mutate protected machine state.
7. **Epistemic status** describes whether content is candidate, verified, disputed, recognized, revoked, or historical.
8. **Data ownership** identifies the component that may authoritatively create and mutate a data domain.
9. **Evidence and audit** prove decisions and transitions without becoming authorization sources.

No single component owns every layer.

### 4.3 Explicit grant sources

An active grant may be derived from one or more compatible canonical sources:

- an accepted owner decision;
- an active identity, role, or delegation record;
- an active governance policy decision;
- an active component contract;
- an active deployment profile or overlay;
- an active artifact or release contract;
- an active exception with valid compensating controls;
- a locally verified authority state permitted for offline use.

A chat message, issue, code comment, filesystem permission, process owner, repeated implementation pattern, generated answer, historical document, or recipe is not an authority source.

### 4.4 Separation of roles

The authority model distinguishes:

| Role | Responsibility |
| --- | --- |
| Requester | Proposes or initiates an action. |
| Decision authority | Evaluates policy and returns a bounded decision. |
| Approver or reviewer | Performs required human or institutional review. |
| Owning component | Validates domain invariants and performs authoritative domain mutation. |
| Privileged broker | Performs narrow protected machine mutations after authorization. |
| Audit Broker | Records controlled evidence and receipts. |
| Evidence consumer | Verifies a claim without receiving mutation authority. |
| Recourse authority | Reviews, corrects, revokes, supersedes, or remediates a contested result. |

A deployment may combine compatible roles only when the active policy and profile explicitly permit the combination.

### 4.5 Authentication and authorization

Authentication establishes identity. Authorization establishes permission.

Operating-system identity, root access, service identity, API authentication, device ownership, physical access, and network location are inputs to authority resolution. None is a complete authorization decision by itself.

The Identity and Trust component owns identity, delegation, trust-root, key-metadata, and revocation context. The Governance Policy Runtime evaluates governed decisions. Owning components enforce domain invariants. The kOA Node Agent enforces narrow privileged operations.

### 4.6 Data and component authority

Each authoritative data domain has one owning component.

Other components interact through:

- versioned APIs;
- bounded commands;
- validated events;
- declared gateways;
- signed or verified artifacts;
- explicit export and import contracts.

Read access does not imply write access. Write access does not imply disclosure authority. Data ownership does not imply the ability to bypass consent, rights, retention, publication, or audit policy.

### 4.7 Delegation and revocation

Delegation creates a bounded grant from a recognized authority to a delegate.

A delegation records:

- delegator and delegate;
- capability and target;
- applicable scope;
- activation and expiry;
- further-delegation policy;
- obligations and separation-of-duties constraints;
- revocation mechanism;
- evidence requirements.

Revocation, suspension, supersession, and expiry affect future authority. Historical evidence remains available according to retention and disclosure policy.

### 4.8 Offline authority

Offline operation uses locally available authority only when the active profile permits it.

The local authority state includes:

- active identities and trust roots;
- authority and policy versions;
- revocation epochs or equivalent freshness state;
- delegation validity;
- profile and component contract versions;
- artifact and release compatibility;
- declared stale-authority behavior.

Offline unavailability of a remote service does not silently broaden local authority. Capabilities that require unavailable or stale authority enter their declared blocked, read-only, queued, deferred, or degraded state.

### 4.9 Advisory and external outputs

Recommendations, scores, rankings, model output, voice transcription, semantic candidates, and external integration responses remain non-authoritative inputs.

They may be reviewed, validated, transformed, or admitted through an owning component's contract. They do not directly grant privilege, approve publication, change policy, activate artifacts, or mutate authoritative stores.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-CONST-AUTH-001,REQ-CONST-AUTH-002,REQ-CONST-AUTH-003,REQ-CONST-AUTH-004,REQ-CONST-AUTH-005,REQ-CONST-AUTH-006,REQ-CONST-AUTH-007,REQ-CONST-AUTH-008,REQ-CONST-AUTH-009,REQ-CONST-AUTH-010,REQ-CONST-AUTH-011,REQ-CONST-AUTH-012,REQ-CONST-AUTH-013,REQ-CONST-AUTH-014,REQ-CONST-AUTH-015,REQ-CONST-AUTH-016,REQ-CONST-AUTH-017,REQ-CONST-AUTH-018,REQ-CONST-AUTH-019,REQ-CONST-AUTH-020 -->
- **REQ-CONST-AUTH-001 — SHALL:** Every authoritative operation has a resolvable grant that identifies the acting subject, capability or action, target object, scope, authority source, authority version, applicable conditions, and expiry when expiry applies.
- **REQ-CONST-AUTH-002 — SHALL NOT:** Absence, ambiguity, incompatibility, expiry, revocation, or failed verification of required authority produces an authoritative success result.
- **REQ-CONST-AUTH-003 — SHALL NOT:** Authentication alone, possession of an operating-system account, group membership, administrative role name, network location, or process identity is treated as sufficient authorization.
- **REQ-CONST-AUTH-004 — SHALL:** A governed privileged operation receives a valid policy decision before the privileged broker executes the operation.
- **REQ-CONST-AUTH-005 — SHALL:** A privileged operation is bound to the authorizing decision by subject, operation, target, scope, authority version, obligations, expiry, and replay-protection data.
- **REQ-CONST-AUTH-006 — SHALL NOT:** A component expands its own responsibilities, data ownership, profile membership, network exposure, privilege, or disclosure authority beyond active canonical contracts.
- **REQ-CONST-AUTH-007 — SHALL NOT:** A component writes directly to another component's authoritative data store.
- **REQ-CONST-AUTH-008 — SHALL:** Delegation identifies the delegator, delegate, delegated capability, target scope, validity period, revocation mechanism, and whether further delegation is permitted.
- **REQ-CONST-AUTH-009 — SHALL NOT:** Authority is transitively delegated unless the active delegation contract explicitly permits and bounds further delegation.
- **REQ-CONST-AUTH-010 — SHALL:** Revocation, suspension, supersession, and expiry remove future authority according to the active authority and trust state.
- **REQ-CONST-AUTH-011 — SHALL:** Offline authority uses locally available, verified, active authority objects and applies the declared stale-authority, revocation, and synchronization policy.
- **REQ-CONST-AUTH-012 — SHALL:** Read, propose, approve, execute, publish, activate, administer, audit, and review capabilities remain separately grantable.
- **REQ-CONST-AUTH-013 — SHALL NOT:** Advisory output, candidate content, model output, recommendation, score, ranking, receipt, log entry, or repeated implementation practice becomes authority by itself.
- **REQ-CONST-AUTH-014 — SHALL NOT:** An external AI service directly grants authority, approves a governed action, executes system privilege, or mutates authoritative component state.
- **REQ-CONST-AUTH-015 — SHALL:** Policy decisions, privileged mutations, artifact activations, cross-domain publications, releases, emergency actions, and other declared critical transitions produce machine-readable evidence.
- **REQ-CONST-AUTH-016 — SHALL:** Authority evidence discloses only the information required for verification, accountability, recourse, and applicable audit rights.
- **REQ-CONST-AUTH-017 — SHALL:** Emergency authority is explicit, capability-scoped, target-scoped, time-bounded, attributable, reviewable, and automatically expires.
- **REQ-CONST-AUTH-018 — SHALL:** Canonical ownership determines who may define an architectural or operational fact; copied prose, generated projections, recipes, and historical sources do not create competing authority.
- **REQ-CONST-AUTH-019 — SHALL:** Deployment profiles own component membership, activation mode, topology, hardware placement, and profile-specific resource or network envelopes.
- **REQ-CONST-AUTH-020 — SHALL:** Every active authority, privilege, publication, activation, release, exception, and conformance claim has applicable validation and evidence traceability.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Authority resolution procedure

A component resolves authority in this order:

1. Identify the requested capability and target.
2. Resolve the authenticated subject and applicable identity layers.
3. Resolve the active profile, overlay, tenant, environment, component, artifact, and release scope.
4. Locate the canonical owner of the affected fact or data domain.
5. Resolve the active authority source, version, delegation, validity, and obligations.
6. Evaluate governance policy when the capability requires authorization, disclosure, consent, privilege, activation, publication, or an exception.
7. Validate component-domain invariants and interface preconditions.
8. Bind the decision to the exact operation, target, scope, expiry, and replay-protection value.
9. Execute through the owning component or the narrow privileged broker.
10. Verify the resulting state.
11. Emit required receipts and controlled evidence.
12. Complete, reject, queue, defer, or recover according to the declared outcome.

An authority resolution is complete only when every required input is available and compatible.

### 6.2 Delegation lifecycle

A delegation moves through these conceptual states:

```text
created -> validated -> active -> expired
                        |      |
                        |      +-> revoked
                        +--------> suspended
```

The delegation becomes active after:

1. the delegator's authority is verified;
2. the delegated capability is within the delegator's grant;
3. the target and scope are explicit;
4. obligations and expiry are present;
5. prohibited role combinations are rejected;
6. the delegation record is validated and activated.

Revoked, expired, or suspended delegations remain historical evidence but cannot support a new authoritative operation.

### 6.3 Governed privilege procedure

A protected host mutation follows this sequence:

1. A requester submits a high-level schema-bound operation.
2. Identity and Trust provides subject, node, workload, artifact, and trust context.
3. Governance Policy Runtime evaluates the operation.
4. Required approval, consent, or separation-of-duties steps complete.
5. The decision is bound to the exact operation and replay-protection data.
6. The kOA Node Agent verifies the decision, preconditions, target, and active authority versions.
7. The Node Agent executes only the allowlisted operation.
8. The resulting state is verified.
9. A privileged-operation receipt is emitted.
10. Audit Broker stores the applicable evidence class.

General shell access is outside this normal procedure.

### 6.4 Cross-domain publication procedure

A private-to-public publication follows this sequence:

1. Orgo or another authorized private domain creates a publication candidate.
2. Publication Gateway validates classification, rights, consent, audience, provenance, and transformation requirements.
3. Governance Policy Runtime returns the disclosure and publication decision.
4. Required review or approval completes.
5. Publication Gateway creates the approved publication bundle.
6. Konnaxion accepts the bundle through its public-domain contract.
7. Publication and delivery receipts are recorded.
8. Withdrawal or supersession remains available through an explicit transition.

Failure blocks disclosure and leaves the originating private workflow intact.

### 6.5 Authority release activation

A documentation or product authority release activates after:

1. accepted decisions exist;
2. canonical registries and contracts are complete;
3. references and ownership resolve;
4. requirements and locks are active;
5. applicable tests pass;
6. evidence is registered;
7. exceptions are valid;
8. generated projections are current;
9. the authority registry activates the release last.

Partial authority activation is not a valid release state.

### 6.6 Emergency authority

Emergency authority follows a separate controlled path:

1. identify the emergency condition;
2. authenticate the emergency actor;
3. resolve the permitted emergency capability and target;
4. activate a time-bounded emergency grant;
5. require confirmation or multi-party approval when the policy specifies it;
6. execute only the bounded operation;
7. emit immediate evidence;
8. automatically expire the grant;
9. perform mandatory post-action review and remediation.

Emergency authority does not become an unrestricted administrator role.

## 7. Failure and Degradation

### 7.1 Missing or ambiguous authority

When required identity, policy, delegation, scope, ownership, version, or trust information is missing or ambiguous:

- the affected authoritative mutation is blocked;
- a stable reason code is returned;
- unrelated capabilities remain available when safe;
- read-only or advisory access may remain available when its own authority resolves;
- no default grant is inferred.

### 7.2 Conflicting authority

When active sources appear to conflict:

1. the strict authority order is applied;
2. canonical ownership and scope are resolved;
3. supersession and version applicability are checked;
4. applicable locks and accepted decisions are evaluated;
5. dependent activation remains blocked when the conflict cannot be resolved mechanically.

Implementation prevalence and stronger wording are not conflict-resolution mechanisms.

### 7.3 Expired, revoked, or stale authority

Expired or revoked authority cannot support a new action.

When local offline authority freshness exceeds the profile's permitted window:

- governed mutations enter the declared blocked or restricted state;
- safe local consultation may continue when authorized;
- queued operations retain their original request identity and do not execute until revalidated;
- synchronization does not retroactively authorize an operation that lacked authority at execution time.

### 7.4 Policy runtime failure

When Governance Policy Runtime is unavailable:

- operations requiring a new governed decision are blocked or queued according to their contract;
- previously completed decisions remain usable only within their validity, target, scope, and replay rules;
- components do not substitute local heuristics for policy;
- emergency operation uses only the separately authorized emergency procedure.

### 7.5 Audit or evidence failure

Loss of an audit destination does not automatically stop unrelated safe work.

A critical transition whose contract requires durable evidence:

- does not report authoritative completion until required local evidence is secured;
- preserves diagnostic state;
- retries forwarding through a bounded queue;
- blocks further transitions when loss of evidence would prevent accountability, recovery, or recourse.

### 7.6 Enforcement failure

When an owning component or the privileged broker cannot verify the requested result:

- authoritative completion is withheld;
- the last verified state is preserved;
- rollback or forward repair follows the applicable component or artifact contract;
- partial success is reported as failure or blocked state, not as success.

## 8. Cross-Component Interactions

| Interaction | Decision owner | Enforcement owner | Evidence owner | Boundary |
| --- | --- | --- | --- | --- |
| Identity and delegation | Identity and Trust | Consuming component | Audit Broker when required | Identity context does not grant permission by itself. |
| Governance authorization | Governance Policy Runtime | Owning component | Audit Broker | The policy runtime decides; it does not perform domain or host mutation. |
| Privileged host mutation | Governance Policy Runtime | kOA Node Agent | Audit Broker | The Node Agent executes only a bound allowlisted operation. |
| Component data mutation | Governance Policy Runtime when governed | Owning component | Owning component and Audit Broker | Other components cannot write the authoritative store directly. |
| Private-to-public publication | Governance Policy Runtime | Publication Gateway and Konnaxion | Audit Broker | Publication Gateway controls disclosure; Konnaxion owns accepted public state. |
| UCKK local ingestion | Owning user and UCKK contracts | UCKK Dimension Gateway and UCKK Platform | Audit Broker when required | Ingestion does not automatically publish or infer categories. |
| Artifact activation | Governance Policy Runtime when governed | Owning runtime or kOA Node Agent | Evidence Registry and Audit Broker | Verification precedes atomic activation. |
| Ariane navigation | Owning application and Ariane contracts | Ariane Runtime | Audit Broker when required | External voice output remains an untrusted structured input. |
| SenTient candidate production | Owning review workflow | SenTient only within its isolated workspace | Audit Broker when required | Candidate output has no direct authority in another component. |
| Resource control | Resource Governor | Resource Governor and runtime mechanisms | Operational evidence | Resource decisions do not become governance authorization. |

Every interaction preserves the target component's canonical ownership and the applicable profile boundary.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Accepted decisions explained by this document

| Decision | Closed rule |
| --- | --- |
| `DEC-CONST-001` | Explicit, inspectable, replaceable authority is a global constitutional principle. |
| `DEC-AUTH-001` | Authority is capability-, target-, scope-, version-, and condition-bound. |
| `DEC-IDENT-001` | Identity layers remain distinct; authentication is not authorization. |
| `DEC-GOV-001` | Governance Policy Runtime and Resource Governor are separate authorities. |
| `DEC-PRIV-001` | Normal privileged host mutation uses one narrow schema-bound broker. |
| `DEC-AI-001` | External AI surfaces are optional, user initiated, and non-authoritative. |
| `DEC-DATA-001` | Each authoritative data domain has one owning component; direct cross-store writes are prohibited. |

### 9.2 Prohibited assumptions

Authors, implementations, validators, and AI agents do not assume that:

- root access is governance authority;
- an authenticated user is authorized for every action;
- an administrator role is universal;
- a component owns data because it can read it;
- a service owns a capability because it is installed or running;
- network reachability implies permission;
- a policy receipt can authorize a different subject, target, operation, or time;
- an audit record is itself an authorization decision;
- a recommendation, score, vote, model output, or ranking grants privilege;
- repeated use converts a recipe into a requirement;
- a profile-specific permission applies globally;
- silence or missing configuration means allow;
- emergency authority persists after its expiry;
- offline mode permits bypassing revocation or stale-authority rules;
- historical or migration documentation governs current behavior;
- generated projections override their canonical source.

A new implementation-affecting authority question is resolved through an accepted decision before dependent authority becomes active.

## 10. Validation Criteria

This document is conformant when all applicable checks pass.

| Validation objective | Required evidence or test |
| --- | --- |
| Authority objects and references resolve | `TEST-DOC-VAL-003`, `TEST-DOC-VAL-005`, `TEST-DOC-VAL-006`, `TEST-DOC-VAL-019` |
| Missing authority fails closed | `TEST-SYS-004`, `TEST-SEC-005`, `TEST-DOC-DEC-010` |
| Authentication remains distinct from authorization | `TEST-CROSS-014`, `TEST-SEC-003` |
| Policy decision precedes privilege | `TEST-CROSS-008`, `TEST-SEC-001`, `TEST-SEC-002`, `TEST-SEC-003` |
| Direct cross-component writes are rejected | `TEST-COMP-REG-010`, `TEST-CROSS-015`, component-specific `TEST-COMP-<COMPONENT>-004` tests |
| Governance and resource authority remain separate | `TEST-CROSS-004` |
| Publication and ingestion gateways remain separate | `TEST-CROSS-003` |
| External AI cannot mutate authority | `TEST-CROSS-013`, `TEST-SYS-002`, `TEST-SYS-003` |
| Offline authority and degradation are bounded | `TEST-SYS-001`, `TEST-SYS-005`, `TEST-PROF-006` |
| Emergency authority expires and remains attributable | `TEST-SEC-004`, `TEST-SEC-006` |
| Critical transitions produce evidence | `TEST-SYS-011`, `TEST-LIFE-015`, `TEST-DOC-VAL-016` |
| Authority activation occurs last | `TEST-DOC-VAL-017`, `TEST-DOC-DEC-007`, `TEST-MIG-009` |
| Active claims have complete traceability | `TEST-DOC-VAL-016`, `TEST-PROF-009`, `TEST-LIFE-015` |

Additional validation confirms:

1. all metadata identifiers are unique and active;
2. every requirement in section 5 exists in `generated/requirements-index.json`;
3. every decision and lock reference resolves and applies to global scope;
4. the authority model does not duplicate canonical values owned by another registry;
5. generated requirement text matches the active requirements registry;
6. no profile-specific implementation choice has been generalized;
7. no unresolved authority marker exists;
8. all active prose is in English.

A failed required test prevents the affected authority or conformance claim from becoming active.

## 11. Non-Normative Examples

### 11.1 Local read access

A user opens an active locally verified Kristal Runtime Pack while offline.

The relevant authority may include:

- authenticated local user identity;
- profile permission for offline consultation;
- valid local artifact and trust state;
- active reader and audience policy.

This read does not grant permission to publish, modify the artifact, or administer the node.

### 11.2 Governed host update

An operator requests activation of a verified service bundle.

A compliant flow:

1. authenticates the operator and node;
2. verifies the artifact, channel, environment, and compatibility;
3. obtains the governance decision;
4. binds the decision to the exact activation;
5. executes through the kOA Node Agent;
6. verifies the resulting state;
7. records activation evidence.

Possession of root credentials alone is not the authority model.

### 11.3 Ariane voice request

An external voice service returns a structured command to open a settings panel.

The command is an input. Ariane Runtime validates the current application state, resolves the user's capability, requests confirmation when required, executes through the application contract, and verifies the result.

The voice service does not receive application authority.

### 11.4 SenTient candidate

SenTient produces a candidate entity mapping.

The candidate remains inside the isolated workbench until an owning workflow reviews provenance, uncertainty, rights, and target-domain invariants. Acceptance creates a new owning-component action; SenTient does not mutate the canonical store directly.

### 11.5 Publication from Orgo to Konnaxion

Orgo produces a candidate public report from a completed private workflow.

Publication Gateway applies classification, rights, consent, redaction, audience, and approval rules. Konnaxion receives only the approved publication bundle. The originating private workflow and the accepted public object remain separate authoritative records.

### 11.6 Offline stale authority

A node remains offline beyond the permitted authority-freshness interval.

Local consultation that is still authorized may remain available. New privilege, publication, or activation operations remain blocked until authority freshness is restored or a separately valid emergency procedure applies.
