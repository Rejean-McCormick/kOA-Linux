<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONST-010",
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
    "contracts/system.contract.json#/selective_audit_and_recourse",
    "generated/component-catalog.json",
    "contracts/components/audit-broker.component.json",
    "contracts/artifact-classes.contract.json",
    "contracts/artifact-contracts/decision-receipt.schema.json",
    "contracts/artifact-contracts/provenance-receipt.schema.json",
    "generated/profile-catalog.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-SYS-AUDIT-001",
    "DEC-SYS-RECOURSE-001",
    "DEC-DATA-DISCLOSURE-001",
    "DEC-CULT-001"
  ],
  "requirement_ids": [
    "REQ-CONST-AUDIT-001",
    "REQ-CONST-AUDIT-002",
    "REQ-CONST-AUDIT-003",
    "REQ-CONST-AUDIT-004",
    "REQ-CONST-AUDIT-005",
    "REQ-CONST-AUDIT-006",
    "REQ-CONST-AUDIT-007",
    "REQ-CONST-AUDIT-008",
    "REQ-CONST-AUDIT-009",
    "REQ-CONST-AUDIT-010",
    "REQ-CONST-AUDIT-011",
    "REQ-CONST-AUDIT-012",
    "REQ-CONST-AUDIT-013",
    "REQ-CONST-AUDIT-014",
    "REQ-CONST-AUDIT-015",
    "REQ-CONST-AUDIT-016",
    "REQ-CONST-AUDIT-017",
    "REQ-CONST-AUDIT-018",
    "REQ-CONST-AUDIT-019",
    "REQ-CONST-AUDIT-020",
    "REQ-CONST-AUDIT-021",
    "REQ-CONST-AUDIT-022",
    "REQ-CONST-AUDIT-023",
    "REQ-CONST-AUDIT-024"
  ],
  "lock_ids": [
    "LOCK-OPS-001",
    "LOCK-OPS-002",
    "LOCK-OPS-003",
    "LOCK-OPS-004",
    "LOCK-DATA-001",
    "LOCK-AI-002",
    "LOCK-CULT-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-CONST-009"
  ],
  "tags": [
    "selective-audit",
    "recourse",
    "accountability",
    "privacy",
    "public-evidence",
    "private-proof",
    "decision-receipts",
    "audit-broker",
    "critical-transitions",
    "remedy"
  ]
}
KOA:DOC-META:END -->

# Selective Audit and Recourse

## 1. Purpose

This document establishes selective audit and effective recourse as global constitutional properties of the kOA operating environment.

Selective audit provides accountability for consequential authority, policy, publication, activation, privilege, access, and lifecycle transitions without turning the system into a mechanism for unrestricted observation. It records enough evidence to establish what happened, under which authority, with which outcome, while limiting exposure of people, communities, protected content, security details, and restricted evidence.

Recourse provides a governed path to challenge, review, correct, reverse, restrict, withdraw, or otherwise remedy a consequential decision. Audit without recourse records harm without providing a path to address it. Recourse without reliable evidence cannot establish what occurred or whether a remedy was completed. The two properties therefore operate together.

## 2. Scope

This document applies globally to:

- authoritative state transitions;
- policy and authorization decisions;
- privilege and break-glass actions;
- identity, trust-root, and key transitions;
- artifact verification, publication, activation, rollback, revocation, and withdrawal;
- cross-domain disclosure and publication;
- imports, exports, backup, restore, portability, and exit;
- access to restricted evidence;
- cultural-rights and consent decisions;
- external integration and external AI boundary crossings;
- security and node events;
- operational incidents and governed overrides;
- recourse intake, review, decision, escalation, remedy, and closure;
- audit exports, public evidence, private proof, and conformance evidence.

This document does not require every user interaction to become an audit event. Event selection follows registered risk, authority, disclosure, security, lifecycle, and recourse policies.

Profile contracts may impose stronger retention, integrity, separation-of-duty, private-proof, or review requirements. They do not replace the global prohibition on indiscriminate disclosure.

## 3. Canonical References

Canonical ownership is distributed as follows:

| Subject | Canonical owner |
| --- | --- |
| Global selective-audit and recourse model | `contracts/system.contract.json#/selective_audit_and_recourse` |
| Audit Broker identity and responsibility | `generated/component-catalog.json` |
| Audit Broker observable contract | `contracts/components/audit-broker.component.json` |
| Receipt and proof artifact classes | `contracts/artifact-classes.contract.json` |
| Decision-receipt serialization | `contracts/artifact-contracts/decision-receipt.schema.json` |
| Provenance-receipt serialization | `contracts/artifact-contracts/provenance-receipt.schema.json` |
| Profile-specific audit and review controls | `contracts/profiles/*.profile.json` |
| Requirement statements and strength | `generated/requirements-index.json` |
| Cross-file audit and recourse invariants | `generated/assertion-index.json` |
| Requirement, test, evidence, and remedy relationships | `generated/traceability.json` |
| Conformance tests | `generated/test-catalog.json` |
| Audit and recourse evidence | `generated/evidence-catalog.json` |
| Approved bounded deviations | `generated/exception-index.json` |
| Accepted architectural decisions | `generated/decision-index.json` |
| Active versions and authority order | `generated/authority-manifest.json` |

This document defines constitutional meaning and boundaries. It does not duplicate registry inventories, artifact schemas, profile-specific retention periods, or component-local storage layouts.

## 4. Model and Responsibilities

### 4.1 Accountability without a panopticon

kOA uses selective evidence rather than universal observability.

The accountability question is not “What can be collected?” It is “What minimum evidence is required to verify this governed event, protect affected parties, support review, and prove any remedy?”

Collection, retention, access, derivation, export, and publication remain separate decisions. Permission to record an event does not automatically permit public disclosure or unrestricted secondary use.

### 4.2 Canonical audit classes

The global model contains five audit classes:

| Audit class | Primary purpose | Typical visibility |
| --- | --- | --- |
| `public_transparency_receipts` | Demonstrate public or institutional process, authority, integrity, and outcome | Public or audience-scoped |
| `tenant_operational_audit` | Support local operation, administration, troubleshooting, and governed workflow review | Tenant-authorized |
| `restricted_evidence_audit` | Preserve protected evidence for authorized investigation, review, or adjudication | Restricted |
| `personal_privacy_records` | Record access, consent, correction, restriction, withdrawal, and privacy-relevant processing | Subject- and policy-governed |
| `security_and_node_audit` | Record authentication, privilege, trust, host, security, and incident transitions | Security-authorized |

Each event belongs to one primary audit class. Derived views can present selected fields to another audience without changing the source class or ownership.

### 4.3 Critical transitions

Critical transitions include:

- authentication or privilege changes;
- policy decisions affecting protected actions;
- workflow approvals, denials, overrides, and escalations;
- release, artifact, policy, or configuration activation;
- publication, cross-domain disclosure, revocation, or withdrawal;
- trust-root, signature, key, or node-identity changes;
- import, export, backup, restore, and exit operations;
- break-glass activation and termination;
- access to restricted evidence;
- recourse decisions and completed remedies.

The canonical requirements registry owns the precise event obligations. Component contracts identify the producer, and artifact contracts define the receipt format.

### 4.4 Public evidence and private proof

Public evidence can include:

- policy or rule identity;
- process stage;
- decision outcome;
- reason-code references;
- artifact or release integrity status;
- pseudonymous or aggregate participation;
- publication, activation, or remedy status;
- dissent or contested state when disclosure is authorized.

Private proof retains the protected evidence needed to substantiate the public statement. It can use controlled references, redaction, audience-specific views, authenticated manifests, signatures, integrity digests, or cryptographic proof.

A public receipt is not a substitute for protected source evidence, and a protected source record is not automatically publishable.

### 4.5 Audit Broker responsibilities

The Audit Broker receives, validates, classifies, sequences, stores, and exports audit events and decision receipts.

Its responsibility includes:

- schema validation;
- event-class assignment validation;
- producer authentication;
- ordering and correlation;
- integrity protection;
- protected storage routing;
- policy-governed retention;
- asynchronous forwarding;
- redacted or audience-scoped export;
- detectable error and gap recording;
- access-event generation for protected evidence.

The Audit Broker does not become the authoritative owner of the business state described by an event. It owns the audit record and evidence references associated with that event.

### 4.6 Recourse roles

A recourse process distinguishes:

- claimant or authorized representative;
- original decision authority;
- evidence custodian;
- recourse case owner;
- reviewer;
- remedy owner;
- escalation authority;
- affected community or collective authority where applicable.

One actor can hold multiple roles only where the applicable policy permits it. High-impact and conflict-sensitive cases can require separation.

### 4.7 Recourse case states

A recourse case uses explicit states:

`text
initiated
acknowledged
evidence_preserved
eligibility_assessed
under_review
decision_issued
remedy_pending
remedied
closed
`

Alternative terminal or transfer states are:

`text
withdrawn
rejected_out_of_scope
escalated
superseded
`

Every state transition records the responsible authority, time, reason, and evidence reference.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-CONST-AUDIT-001,REQ-CONST-AUDIT-002,REQ-CONST-AUDIT-003,REQ-CONST-AUDIT-004,REQ-CONST-AUDIT-005,REQ-CONST-AUDIT-006,REQ-CONST-AUDIT-007,REQ-CONST-AUDIT-008,REQ-CONST-AUDIT-009,REQ-CONST-AUDIT-010,REQ-CONST-AUDIT-011,REQ-CONST-AUDIT-012,REQ-CONST-AUDIT-013,REQ-CONST-AUDIT-014,REQ-CONST-AUDIT-015,REQ-CONST-AUDIT-016,REQ-CONST-AUDIT-017,REQ-CONST-AUDIT-018,REQ-CONST-AUDIT-019,REQ-CONST-AUDIT-020,REQ-CONST-AUDIT-021,REQ-CONST-AUDIT-022,REQ-CONST-AUDIT-023,REQ-CONST-AUDIT-024 -->
- **REQ-CONST-AUDIT-001 — SHALL:** kOA separate public transparency receipts, tenant operational audit, restricted evidence audit, personal privacy records, and security and node audit into distinct policy classes.
- **REQ-CONST-AUDIT-002 — SHALL NOT:** Accountability be implemented as total transparency, unrestricted event collection, indiscriminate disclosure, or a universal public log.
- **REQ-CONST-AUDIT-003 — SHALL:** Every audit class declare its purpose, authorized readers, event types, data fields, retention, deletion, export, encryption, integrity, and disclosure rules.
- **REQ-CONST-AUDIT-004 — SHALL:** Unknown or unclassified audit data receive restricted handling until an authorized classification decision is recorded.
- **REQ-CONST-AUDIT-005 — SHALL:** Every critical authoritative transition emit or durably stage a machine-readable receipt before the transition is reported as completed.
- **REQ-CONST-AUDIT-006 — SHALL NOT:** Ordinary interface navigation, passive viewing, or non-authoritative presentation generate constitutional decision receipts unless a registered policy classifies the action as sensitive.
- **REQ-CONST-AUDIT-007 — SHALL:** Critical-transition receipts identify the acting subject, action, governed resource, policy or rule reference, decision, reason codes, correlation identifier, time, outcome, and applicable obligations.
- **REQ-CONST-AUDIT-008 — SHALL NOT:** Ordinary logs, receipts, diagnostics, exports, or public evidence contain credentials, secret material, unrestricted private content, or unnecessary sensitive payloads.
- **REQ-CONST-AUDIT-009 — SHALL:** Public accountability expose only the minimum evidence required to verify process, authority, integrity, outcome, and applicable rationale.
- **REQ-CONST-AUDIT-010 — SHALL:** Restricted evidence remain in protected storage and be disclosed through governed references, redacted views, aggregates, pseudonymous records, or private proof where those forms satisfy the accountability purpose.
- **REQ-CONST-AUDIT-011 — SHALL:** Access to restricted audit evidence, privacy records, recourse files, or protected exports itself produce an access event within the applicable protected audit class.
- **REQ-CONST-AUDIT-012 — SHALL:** Audit integrity controls make unauthorized alteration, deletion, reordering, substitution, or silent event loss detectable.
- **REQ-CONST-AUDIT-013 — SHALL:** Malformed or rejected critical audit events produce an explicit gap or error record and never disappear silently.
- **REQ-CONST-AUDIT-014 — SHALL:** Local capture of critical audit events continue during network loss, with asynchronous, resumable, and duplicate-safe forwarding when a remote destination is configured.
- **REQ-CONST-AUDIT-015 — SHALL NOT:** Correctness of a local authoritative operation depend on immediate delivery to a central audit service when durable local critical-event capture is available.
- **REQ-CONST-AUDIT-016 — SHALL:** Every consequential decision expose a recourse path appropriate to its scope, authority, affected parties, risk, and applicable rights.
- **REQ-CONST-AUDIT-017 — SHALL:** A recourse case preserve the challenged decision or receipt reference, claimant or authorized representative, requested remedy, relevant evidence, reviewing authority, state, deadlines, outcome, and remedy status.
- **REQ-CONST-AUDIT-018 — SHALL:** Recourse provide notice, a meaningful explanation, an opportunity to submit or correct evidence, review by authorized human authority, and a recorded outcome.
- **REQ-CONST-AUDIT-019 — SHALL:** High-impact or conflict-sensitive recourse receive review by an authority distinct from the original automated process or original decision maker where the active policy requires separation.
- **REQ-CONST-AUDIT-020 — SHALL NOT:** An AI system, automated suggestion, missing response, or absence of recorded denial constitute acceptance of risk, consent, final adjudication, or closure of recourse.
- **REQ-CONST-AUDIT-021 — SHALL:** A successful recourse outcome produce a traceable remedy such as correction, reversal, re-execution, access restriction, withdrawal, republication, restoration, or another policy-authorized remediation.
- **REQ-CONST-AUDIT-022 — SHALL:** Withdrawal, deletion, correction, or sealing of protected material retain only the minimum lawful and operational proof needed to demonstrate that the governed transition occurred.
- **REQ-CONST-AUDIT-023 — SHALL:** Recourse remain available to applicable individual, collective, community, institutional, or authorized representative authorities without converting protected evidence into public data.
- **REQ-CONST-AUDIT-024 — SHALL:** Conformance testing cover audit-class separation, minimum-necessary disclosure, critical receipt durability, restricted evidence access, offline event capture, tamper detection, recourse progression, independent review where applicable, and remedy verification.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Producing a critical-transition receipt

The producing component:

1. identifies the governed action and authoritative resource;
2. evaluates identity, authorization, policy, consent, compatibility, and trust requirements;
3. assigns the applicable audit class;
4. constructs the minimum receipt fields;
5. replaces protected payloads with governed references where possible;
6. submits the receipt to durable local capture;
7. receives acceptance or an explicit rejection;
8. completes the authoritative transition only under the registered durability policy;
9. records the observed outcome and any obligations;
10. forwards or exports the event according to class policy.

A rejected or malformed receipt creates an observable error path. It does not disappear as if the event had been accepted.

### 6.2 Accessing restricted evidence

Before releasing restricted evidence, the system:

1. authenticates the requester;
2. evaluates purpose, role, scope, consent, cultural rights, legal basis, and retention conditions;
3. selects the minimum necessary representation;
4. applies redaction or private-proof mechanisms;
5. records the access decision;
6. records the actual access or export;
7. binds the result to the requesting case, investigation, or authorized purpose.

Repeated access does not inherit authority from an earlier access unless the applicable policy explicitly grants a bounded session or case authorization.

### 6.3 Opening recourse

A recourse case starts from:

- a challenged receipt or decision;
- an affected data object or publication;
- a denied or restricted action;
- an alleged policy, consent, attribution, or cultural-rights failure;
- a security, identity, or access incident;
- an incomplete or ineffective prior remedy.

The intake record captures the challenge, requested outcome, relevant authority, claimant relationship, urgency, representation, and evidence-preservation needs.

### 6.4 Reviewing recourse

The reviewing authority:

1. verifies case eligibility and scope;
2. preserves the challenged evidence;
3. discloses a meaningful explanation at the appropriate classification level;
4. permits correction or supplementation of evidence;
5. identifies conflicts of interest;
6. assigns independent review when required;
7. applies the active policy and rights context;
8. records findings, dissent, limitations, and the decision;
9. assigns any remedy to a named owner;
10. communicates the outcome through an authorized channel.

External AI output can support drafting or analysis only as non-authoritative candidate material. It does not decide the case.

### 6.5 Executing a remedy

A remedy moves through:

`text
assigned
accepted_by_owner
in_progress
verified
completed
`

It can instead move to:

`text
blocked
failed
escalated
superseded
`

Completion requires evidence that the authoritative state, publication, access rule, artifact, record, or operational condition changed as directed. A written promise without verified effect is not a completed remedy.

### 6.6 Closing a case

Closure records:

- the final decision;
- applied policy and authority;
- evidence considered;
- remedy result;
- remaining limitations;
- appeal or escalation status;
- retained proof;
- retention and sealing rules;
- notifications issued.

Closure does not erase dissent, an unresolved external dependency, or a failed remedy. Those conditions remain explicit.

## 7. Failure Modes and Safe Degradation

| Failure | Required behavior |
| --- | --- |
| Audit Broker temporarily unavailable | Use durable local staging for eligible critical events; block transitions whose registered policy requires confirmed capture and lacks a safe staging path. |
| Event malformed | Reject it, preserve an explicit error or gap record, and prevent silent completion where the event is required. |
| Audit classification absent | Apply restricted handling and block public export until classification is resolved. |
| Central forwarding unavailable | Continue local capture and retry asynchronously without duplicate events. |
| Integrity verification fails | Quarantine affected records, preserve evidence, and block reliance on them until resolution. |
| Restricted evidence unavailable | Preserve the case and record the evidence gap; avoid inventing findings or treating absence as consent. |
| Reviewer conflict discovered | Reassign or escalate according to policy while preserving the case history. |
| Remedy cannot be executed | Mark the remedy blocked or failed, notify the applicable authority, and keep the case open or escalated. |
| Retention conflict | Apply the controlling authority, document the disposition, and retain only the minimum permitted proof. |
| Public disclosure risks re-identification | Reduce, aggregate, pseudonymize, delay, restrict, or withhold the public view while preserving private evidence. |
| Offline operation | Preserve local critical-event capture and local recourse intake; defer external forwarding or review dependencies explicitly. |
| Audit storage pressure | Apply class-aware retention and resource controls; never discard required critical events silently. |

A degraded audit path does not create permission to bypass policy, disclosure controls, evidence preservation, or recourse.

## 8. Security, Privacy, and Trust Boundaries

Audit data can be more sensitive than the source operation because it correlates identities, actions, locations, resources, decisions, and time. It therefore receives explicit classification and access controls.

Security and privacy boundaries include:

- producer authentication;
- per-class storage and encryption;
- purpose- and role-bound access;
- field-level minimization;
- protected identity handling;
- separate public and private views;
- reader-access auditing;
- controlled export;
- bounded retention and deletion;
- legal or policy holds;
- cultural-rights and collective-authority restrictions;
- integrity verification;
- secure key and signing identity management;
- no secrets in ordinary event payloads;
- no automatic transfer to external AI surfaces.

Unknown classification defaults to restricted handling.

Public receipts favor aggregate or pseudonymous identifiers when accountability does not require a named identity. Restricted evidence remains protected even when a related public outcome is disclosed.

Access, correction, restriction, withdrawal, deletion, and objection workflows use the applicable identity, privacy, cultural-rights, and recourse policies. A system record can preserve minimal proof of a governed deletion or withdrawal without retaining the withdrawn content itself.

## 9. Exceptions and Compatibility

An exception or waiver cannot:

- create a universal public audit log;
- permit secret material in ordinary logs or receipts;
- remove recourse for a consequential decision while claiming unqualified conformance;
- treat AI output as final adjudication;
- hide an active waiver from conformance evidence;
- exempt access to restricted evidence from access auditing;
- permit silent event loss;
- permit a completed-remedy claim without verification;
- override cultural-rights or consent authority;
- convert protected evidence into unrestricted public data.

A bounded exception can adjust retention, export, review routing, evidence format, or operational implementation only within the exception registry's scope and non-waivable authority.

Receipt, event, case, and remedy schemas carry explicit compatibility versions. An incompatible event is rejected or migrated through a validated path. A reader does not silently reinterpret an unknown field, decision code, audit class, or case state.

Historical audit and recourse records remain interpretable through their registered schema and policy versions. Supersession preserves the prior record rather than rewriting its original decision context.

## 10. Validation Criteria

This document is conformant when validation confirms:

1. exactly five canonical audit classes exist and remain policy-separated;
2. every critical event maps to a registered producer, audit class, receipt schema, and retention policy;
3. ordinary non-sensitive interface activity does not create constitutional receipt volume;
4. public evidence excludes protected identities and payloads unless explicit authority permits disclosure;
5. restricted evidence access creates protected access events;
6. malformed events produce explicit errors or gaps;
7. event integrity detects unauthorized alteration, deletion, substitution, and reordering;
8. local critical-event capture survives network loss and restart;
9. forwarding is resumable and duplicate-safe;
10. every consequential decision class has a registered recourse path;
11. recourse records preserve challenged decisions, evidence, authority, deadlines, outcomes, and remedies;
12. separation of review is enforced where policy requires it;
13. AI and automated suggestions remain non-authoritative;
14. successful cases link to verified remedy evidence;
15. withdrawal and deletion preserve only minimum authorized proof;
16. protected evidence, public evidence, and recourse exports honor cultural-rights and consent controls;
17. exceptions remain bounded and visible;
18. requirement, lock, test, and evidence references resolve.

The principal validation entry point is:

`bash
python docs/tools/validate_docs.py
`

Supporting checks include:

`text
tools/check_interfile_locks.py
tools/check_traceability.py
tools/check_component_boundaries.py
tools/check_artifact_contracts.py
tools/check_decision_closure.py
tools/check_no_unresolved_state.py
`

## 11. Non-Normative Examples

### 11.1 Public activation receipt

A policy bundle is activated. The public receipt identifies the bundle class, policy version, activation time, validation result, and outcome. The protected operational audit retains the node identity, operator identity, detailed diagnostics, and restricted evidence references.

### 11.2 Restricted testimony

A review uses protected testimony. The public record states that authorized evidence was considered and records the outcome. It does not disclose the testimony, protected identity, or details that enable re-identification. Access to the protected testimony is itself recorded.

### 11.3 Correcting a publication

A person challenges a published record. The case links to the publication receipt, accepts corrected evidence, records the review, assigns a republication remedy, verifies the replacement publication, and preserves a minimal correction trail.

### 11.4 Cultural withdrawal

A community authority withdraws permission for distribution of a cultural object. New publication stops, indexes and audience packs are updated, authorized caches are purged, and a minimal withdrawal receipt remains. Restricted cultural context does not become public through the audit record.

### 11.5 Offline security event

A sovereign node loses network connectivity during a privileged transition. The local Audit Broker records the critical event durably. Remote forwarding resumes later and detects duplicate submission. The operation does not depend on immediate central log delivery.

### 11.6 AI-assisted case drafting

An authorized reviewer uses an approved external AI surface to draft a summary from a minimized, user-approved export. The returned text is candidate material with provenance. The reviewer verifies, edits, and accepts the final case note through the local authoritative workflow.

### 11.7 Failed remedy

A recourse decision orders restoration of a record, but the required backup is damaged. The remedy is marked failed rather than completed. The case escalates with evidence of the failed restore and a new authorized remediation path.
