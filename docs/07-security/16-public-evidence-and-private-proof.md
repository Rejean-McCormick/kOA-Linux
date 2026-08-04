<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SEC-016",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "security",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/selective_audit_and_recourse",
    "generated/component-catalog.json#/components/audit_broker",
    "contracts/components/audit-broker.component.json",
    "generated/component-catalog.json#/components/publication_gateway",
    "contracts/components/publication-gateway.component.json",
    "contracts/artifact-classes.contract.json",
    "contracts/artifact-contracts/decision-receipt.schema.json",
    "contracts/artifact-contracts/provenance-receipt.schema.json",
    "contracts/artifact-contracts/publication-request.schema.json",
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
    "DEC-CULT-001",
    "DEC-SEC-EVIDENCE-001",
    "DEC-SYS-COMP-001",
    "DEC-SYS-OFFLINE-001",
    "DEC-SYS-AUDIT-001"
  ],
  "requirement_ids": [
    "REQ-SEC-EVIDENCE-001",
    "REQ-SEC-EVIDENCE-002",
    "REQ-SEC-EVIDENCE-003",
    "REQ-SEC-EVIDENCE-004",
    "REQ-SEC-EVIDENCE-005",
    "REQ-SEC-EVIDENCE-006",
    "REQ-SEC-EVIDENCE-007",
    "REQ-SEC-EVIDENCE-008",
    "REQ-SEC-EVIDENCE-009",
    "REQ-SEC-EVIDENCE-010",
    "REQ-SEC-EVIDENCE-011",
    "REQ-SEC-EVIDENCE-012",
    "REQ-SEC-EVIDENCE-013",
    "REQ-SEC-EVIDENCE-014",
    "REQ-SEC-EVIDENCE-015",
    "REQ-SEC-EVIDENCE-016",
    "REQ-SEC-EVIDENCE-017",
    "REQ-SEC-EVIDENCE-018",
    "REQ-SEC-EVIDENCE-019",
    "REQ-SEC-EVIDENCE-020",
    "REQ-SEC-EVIDENCE-021",
    "REQ-SEC-EVIDENCE-022",
    "REQ-SEC-EVIDENCE-023",
    "REQ-SEC-EVIDENCE-024",
    "REQ-SEC-EVIDENCE-025",
    "REQ-SEC-EVIDENCE-026",
    "REQ-SEC-EVIDENCE-027",
    "REQ-SEC-EVIDENCE-028",
    "REQ-SEC-EVIDENCE-029",
    "REQ-SEC-EVIDENCE-030",
    "REQ-SEC-EVIDENCE-031",
    "REQ-SEC-EVIDENCE-032",
    "REQ-SEC-EVIDENCE-033",
    "REQ-SEC-EVIDENCE-034",
    "REQ-SEC-EVIDENCE-035",
    "REQ-SEC-EVIDENCE-036",
    "REQ-SEC-EVIDENCE-037",
    "REQ-SEC-EVIDENCE-038",
    "REQ-SEC-EVIDENCE-039",
    "REQ-SEC-EVIDENCE-040"
  ],
  "lock_ids": [
    "LOCK-OPS-001",
    "LOCK-OPS-002",
    "LOCK-OPS-003",
    "LOCK-OPS-004",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-CULT-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-GATE-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-002",
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-SYS-000",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-006",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-010",
    "DOC-SYS-011",
    "DOC-SYS-012",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-016",
    "DOC-SYS-017",
    "DOC-SYS-018",
    "DOC-SYS-019",
    "DOC-PROFILE-001",
    "DOC-PROFILE-002",
    "DOC-COMP-000",
    "DOC-COMP-001",
    "DOC-SEC-000",
    "DOC-SEC-001",
    "DOC-SEC-002",
    "DOC-SEC-003",
    "DOC-SEC-004",
    "DOC-SEC-005",
    "DOC-SEC-006"
  ],
  "tags": [
    "public-evidence",
    "private-proof",
    "selective-audit",
    "minimum-disclosure",
    "transparency-receipts",
    "restricted-evidence",
    "pseudonymization",
    "aggregation",
    "integrity",
    "recourse",
    "cultural-rights",
    "offline-audit",
    "conformance"
  ]
}
KOA:DOC-META:END -->

# Public Evidence and Private Proof

## 1. Purpose

This document defines how kOA demonstrates accountability without converting protected evidence into universal public data.

Public evidence is the minimum audience-appropriate proof that a governed event, process, decision, publication, activation, remedy, or institutional obligation occurred under a known authority and reached a stated result.

Private proof is the protected evidence needed to substantiate that statement for authorized investigation, review, adjudication, correction, recourse, security response, cultural-rights review, or conformance verification.

The two forms remain linked but distinct. Public evidence supports verification. Private proof supports deeper substantiation. Neither form automatically grants access to the other.

The model avoids two failures:

- opaque authority, where no one can verify consequential action;
- total transparency, where accountability exposes people, communities, protected content, security details, and restricted evidence.

## 2. Scope

This document applies globally to:

- public transparency receipts;
- tenant operational audit projections;
- restricted evidence;
- personal privacy records;
- security and node evidence;
- public decision and provenance receipts;
- publication, activation, privilege, trust, identity, import, export, withdrawal, and remedy evidence;
- public summaries and aggregate accountability records;
- pseudonymous and redacted records;
- evidence signatures, digests, manifests, and cryptographic proofs;
- access to protected audit records;
- evidence export;
- correction, supersession, withdrawal, and deletion proof;
- recourse;
- offline evidence capture and later reconciliation;
- profile-specific retention and review controls;
- evidence tests and conformance.

This document does not require every user action to become an audit event. The applicable requirements, component contracts, audit policies, and profiles identify critical transitions.

This document does not authorize publication. Public evidence crosses an authority boundary only through the applicable publication and disclosure workflow.

## 3. Canonical References

Canonical ownership is distributed as follows:

| Subject | Canonical owner |
| --- | --- |
| Selective audit and recourse model | `contracts/system.contract.json#/selective_audit_and_recourse` |
| Audit Broker identity | `generated/component-catalog.json#/components/audit_broker` |
| Audit Broker behavior | `contracts/components/audit-broker.component.json` |
| Publication Gateway identity and behavior | Publication Gateway component and component contract |
| Receipt, proof, export, and evidence artifact classes | `contracts/artifact-classes.contract.json` |
| Decision-receipt serialization | `contracts/artifact-contracts/decision-receipt.schema.json` |
| Provenance-receipt serialization | `contracts/artifact-contracts/provenance-receipt.schema.json` |
| Publication-request serialization | `contracts/artifact-contracts/publication-request.schema.json` |
| Profile-specific retention, access, integrity, and offline controls | `contracts/profiles/*.profile.json` |
| Requirement statements and strength | `generated/requirements-index.json` |
| Audit, disclosure, cultural-rights, and lifecycle invariants | `generated/assertion-index.json` |
| Evidence, decision, test, remedy, and publication relationships | `generated/traceability.json` |
| Conformance tests | `generated/test-catalog.json` |
| Accepted conformance evidence | `generated/evidence-catalog.json` |
| Approved bounded deviations | `generated/exception-index.json` |
| Accepted architectural decisions | `generated/decision-index.json` |
| Active versions and authority order | `generated/authority-manifest.json` |

The Audit Broker owns protected audit state. Publication Gateway owns cross-domain publication. Source components retain ownership of their business records.

## 4. Evidence Model and Responsibilities

### 4.1 Five audit classes

The selective-audit model uses five primary classes:

| Audit class | Purpose | Normal audience |
| --- | --- | --- |
| `public_transparency_receipts` | Demonstrate process, authority, integrity, outcome, correction, or remedy | Public or explicitly scoped audience |
| `tenant_operational_audit` | Support governed local operation and administration | Tenant-authorized readers |
| `restricted_evidence_audit` | Preserve protected evidence for investigation, review, adjudication, or recourse | Explicitly authorized reviewers |
| `personal_privacy_records` | Record access, consent, correction, restriction, withdrawal, and privacy processing | Subject- and policy-governed readers |
| `security_and_node_audit` | Record authentication, privilege, trust, host, security, and incident transitions | Security-authorized readers |

Every source event has one primary class. A public view derived from another class remains a projection, not a reclassification of the protected source.

### 4.2 Evidence layers

The model distinguishes five layers:

| Layer | Meaning |
| --- | --- |
| Source event | The component-owned authoritative transition or observation |
| Private proof | Protected receipt, record, artifact, testimony, journal, or manifest supporting the event |
| Public projection | Minimum audience-appropriate claim derived from private proof |
| Access receipt | Protected record of who accessed, exported, reviewed, or transformed private proof |
| Recourse case | Governed challenge, review, remedy, and verification linked to evidence |

Each layer has its own owner, classification, schema, retention, access rules, and lifecycle.

### 4.3 Public evidence

Public evidence can disclose:

- process or rule identity;
- authority class;
- decision or transition type;
- result;
- reason-code references;
- validation status;
- artifact or release version;
- aggregate participation;
- pseudonymous participation;
- correction or withdrawal status;
- remedy completion status;
- integrity or signature verification status.

It excludes protected detail unless explicit disclosure authority requires the detail.

### 4.4 Private proof

Private proof can contain:

- authenticated source receipts;
- protected identities;
- source records;
- policy inputs;
- review evidence;
- testimony;
- detailed diagnostics;
- security observations;
- cultural context;
- privacy records;
- transaction journals;
- recovery evidence;
- restricted attachments.

Private proof remains protected even when a related public projection exists.

### 4.5 Governed linkage

A governed link between public evidence and private proof identifies:

```text
public_artifact_ref
private_proof_ref
source_event_ref
projection_rule_ref
policy_decision_ref
classification_ref
provenance_ref
integrity_ref
access_policy_ref
retention_policy_ref
recourse_ref
```

The public artifact does not reveal the protected reference when even the reference would expose sensitive information. In that case, Audit Broker retains the link and publishes a non-sensitive verification handle.

### 4.6 Component responsibilities

| Responsibility | Owner |
| --- | --- |
| Authoritative business event | Source component |
| Critical-transition receipt creation | Producing component under its contract |
| Audit validation, classification, sequencing, and protected storage | Audit Broker |
| Public projection request | Authorized workflow or evidence owner |
| Publication and destination reconciliation | Publication Gateway |
| Identity and trust | Identity and Trust |
| Disclosure, consent, privacy, and cultural-rights decisions | Governance Policy Runtime or registered authority |
| Resource admission | Resource Governor |
| Recourse case ownership | Registered recourse authority |
| Remedy execution | Owning component or lifecycle authority |

Transport, storage, publication, and review do not transfer source ownership.

### 4.7 Evidence forms

Evidence can use:

- machine-readable receipts;
- authenticated manifests;
- signed artifacts;
- functional integrity digests;
- redacted views;
- pseudonymous views;
- aggregates;
- audience-specific projections;
- cryptographic inclusion or existence proofs;
- controlled references;
- protected exports.

The artifact contract determines the required form.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SEC-EVIDENCE-001,REQ-SEC-EVIDENCE-002,REQ-SEC-EVIDENCE-003,REQ-SEC-EVIDENCE-004,REQ-SEC-EVIDENCE-005,REQ-SEC-EVIDENCE-006,REQ-SEC-EVIDENCE-007,REQ-SEC-EVIDENCE-008,REQ-SEC-EVIDENCE-009,REQ-SEC-EVIDENCE-010,REQ-SEC-EVIDENCE-011,REQ-SEC-EVIDENCE-012,REQ-SEC-EVIDENCE-013,REQ-SEC-EVIDENCE-014,REQ-SEC-EVIDENCE-015,REQ-SEC-EVIDENCE-016,REQ-SEC-EVIDENCE-017,REQ-SEC-EVIDENCE-018,REQ-SEC-EVIDENCE-019,REQ-SEC-EVIDENCE-020,REQ-SEC-EVIDENCE-021,REQ-SEC-EVIDENCE-022,REQ-SEC-EVIDENCE-023,REQ-SEC-EVIDENCE-024,REQ-SEC-EVIDENCE-025,REQ-SEC-EVIDENCE-026,REQ-SEC-EVIDENCE-027,REQ-SEC-EVIDENCE-028,REQ-SEC-EVIDENCE-029,REQ-SEC-EVIDENCE-030,REQ-SEC-EVIDENCE-031,REQ-SEC-EVIDENCE-032,REQ-SEC-EVIDENCE-033,REQ-SEC-EVIDENCE-034,REQ-SEC-EVIDENCE-035,REQ-SEC-EVIDENCE-036,REQ-SEC-EVIDENCE-037,REQ-SEC-EVIDENCE-038,REQ-SEC-EVIDENCE-039,REQ-SEC-EVIDENCE-040 -->
- **REQ-SEC-EVIDENCE-001 — SHALL:** kOA separate public evidence, tenant operational audit, restricted evidence, personal privacy records, and security and node audit into distinct policy classes.
- **REQ-SEC-EVIDENCE-002 — SHALL NOT:** Accountability be implemented as universal public logging, unrestricted event collection, indiscriminate disclosure, or automatic publication of protected evidence.
- **REQ-SEC-EVIDENCE-003 — SHALL:** Every public evidence artifact identify the governed event, process or rule reference, outcome, reason-code references, time, integrity status, and audience without exposing unnecessary protected data.
- **REQ-SEC-EVIDENCE-004 — SHALL:** Every private proof record preserve the minimum protected evidence required to substantiate a related public claim, support authorized review, and verify remedy.
- **REQ-SEC-EVIDENCE-005 — SHALL NOT:** A public receipt substitute for protected source evidence when the protected evidence is required for investigation, adjudication, correction, or recourse.
- **REQ-SEC-EVIDENCE-006 — SHALL NOT:** The existence of private proof create permission to publish, export, copy, index, train on, or otherwise disclose that proof.
- **REQ-SEC-EVIDENCE-007 — SHALL:** Every link between public evidence and private proof use a governed reference that preserves audit class, ownership, policy version, retention, and access controls.
- **REQ-SEC-EVIDENCE-008 — SHALL:** Public evidence use aggregate, pseudonymous, redacted, delayed, audience-scoped, or cryptographic forms whenever those forms satisfy the accountability purpose.
- **REQ-SEC-EVIDENCE-009 — SHALL NOT:** Named identities, precise locations, private content, cultural context, security topology, secret material, raw keys, credentials, or unrestricted diagnostics appear in public evidence without explicit disclosure authority.
- **REQ-SEC-EVIDENCE-010 — SHALL:** Every public projection record the source proof reference, projection rule, transformation identity, policy decision, provenance, output classification, and publication receipt.
- **REQ-SEC-EVIDENCE-011 — SHALL:** Public projections be reproducible from the applicable protected proof or use a reviewed non-deterministic candidate transformation with preserved provenance and explicit human acceptance.
- **REQ-SEC-EVIDENCE-012 — SHALL NOT:** External AI output become public evidence, private proof, an audit finding, or a recourse determination without local validation and authorized acceptance.
- **REQ-SEC-EVIDENCE-013 — SHALL:** The Audit Broker remain authoritative for audit classification, protected receipt storage, controlled proof access, evidence sequencing, integrity, retention, and governed export.
- **REQ-SEC-EVIDENCE-014 — SHALL:** Publication Gateway remain authoritative for cross-domain publication of approved public evidence.
- **REQ-SEC-EVIDENCE-015 — SHALL NOT:** Audit Broker publication functions and Publication Gateway disclosure functions merge into one implicit authority.
- **REQ-SEC-EVIDENCE-016 — SHALL:** Every critical authoritative transition emit or durably stage a machine-readable protected receipt before completion is reported.
- **REQ-SEC-EVIDENCE-017 — SHALL:** Every protected receipt identify the acting subject or service, action, governed resource, authority or rule, decision, reason codes, correlation identity, time, result, obligations, and applicable recovery or remedy references.
- **REQ-SEC-EVIDENCE-018 — SHALL NOT:** Ordinary passive viewing, navigation, or non-authoritative presentation generate constitutional decision receipts unless a registered policy classifies the action as sensitive.
- **REQ-SEC-EVIDENCE-019 — SHALL:** Access to restricted evidence, privacy records, recourse files, protected exports, transaction journals, or security proof produce a separate protected access event.
- **REQ-SEC-EVIDENCE-020 — SHALL:** Every restricted-evidence access request identify requester, authority scope, purpose, case or review reference, selected evidence, minimization, expiry, and export restrictions.
- **REQ-SEC-EVIDENCE-021 — SHALL NOT:** Administrator status, root access, employment role, physical possession, local storage access, or system ownership alone authorize private proof access.
- **REQ-SEC-EVIDENCE-022 — SHALL:** Private proof access return a minimized view, governed reference, redacted record, aggregate, authenticated manifest, or protected export appropriate to the approved purpose.
- **REQ-SEC-EVIDENCE-023 — SHALL:** Every private proof export be destination-bound, purpose-bound, time-bound, integrity-protected, attributable, and recorded by a durable receipt.
- **REQ-SEC-EVIDENCE-024 — SHALL NOT:** A proof export be an unrestricted database dump, filesystem copy, log archive, screen capture, memory image, or payload collection outside an approved evidence contract.
- **REQ-SEC-EVIDENCE-025 — SHALL:** Integrity signatures, digests, authenticated manifests, and cryptographic proofs be used for public-evidence or private-proof artifacts when their functional contracts require tamper evidence or selective verification.
- **REQ-SEC-EVIDENCE-026 — SHALL NOT:** Ordinary Markdown documentation require file-content hashes as a public-evidence or private-proof control.
- **REQ-SEC-EVIDENCE-027 — SHALL:** Every public evidence and private proof artifact retain the schema, policy, classification, producer, and provenance versions needed for historical interpretation.
- **REQ-SEC-EVIDENCE-028 — SHALL NOT:** Supersession, correction, withdrawal, remedy, or policy change rewrite the original protected receipt or erase its original decision context.
- **REQ-SEC-EVIDENCE-029 — SHALL:** Corrections, withdrawals, supersessions, and remedies create linked records that state what changed, under which authority, when, and with which verified result.
- **REQ-SEC-EVIDENCE-030 — SHALL:** Public correction records disclose only the minimum information needed to prevent continued reliance on the replaced or withdrawn public evidence.
- **REQ-SEC-EVIDENCE-031 — SHALL:** Cultural-rights, consent, privacy, legal, security, and community-authority decisions govern evidence collection, retention, access, projection, publication, withdrawal, and destruction.
- **REQ-SEC-EVIDENCE-032 — SHALL NOT:** A public-interest claim, audit purpose, incident response, or conformance need automatically override cultural restrictions, consent, privacy, legal privilege, or security classification.
- **REQ-SEC-EVIDENCE-033 — SHALL:** Every consequential public evidence artifact expose a recourse path appropriate to its authority, audience, risk, affected parties, and applicable collective or individual rights.
- **REQ-SEC-EVIDENCE-034 — SHALL:** Recourse preserve the challenged public artifact, related private-proof references, claimant or authorized representative, requested remedy, review authority, deadlines, decision, and remedy status.
- **REQ-SEC-EVIDENCE-035 — SHALL NOT:** Recourse require protected evidence to become public or require an affected party to disclose more personal or cultural information than the review purpose requires.
- **REQ-SEC-EVIDENCE-036 — SHALL:** Offline operation preserve local critical-event capture, proof integrity, receipt sequencing, access-control state, recourse intake, and deferred export or publication status.
- **REQ-SEC-EVIDENCE-037 — SHALL:** Reconnection export and publication use duplicate-safe reconciliation and revalidate policy, consent, cultural rights, trust, destination, and retention before crossing the local boundary.
- **REQ-SEC-EVIDENCE-038 — SHALL:** Resource pressure preserve critical receipts, protected proof, access receipts, recourse state, integrity material, and recovery records before optional analytics or public projections.
- **REQ-SEC-EVIDENCE-039 — SHALL NOT:** Resource state determine disclosure authority, proof access, public-interest balancing, consent, cultural rights, recourse outcome, or evidence destruction.
- **REQ-SEC-EVIDENCE-040 — SHALL:** Public-evidence and private-proof conformance include audit-class separation, minimum disclosure, source-to-projection traceability, restricted access auditing, tamper evidence, historical interpretation, correction and withdrawal, recourse, offline capture, duplicate-safe export, cultural and privacy controls, reference resolution, and absence of prohibited open-state markers.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Evidence Creation and Publication Procedures

### 6.1 Capturing a critical event

A critical event proceeds through:

```text
authoritative_transition_prepared
receipt_fields_constructed
producer_authenticated
schema_validated
audit_class_validated
classification_applied
local_receipt_durable
authoritative_transition_completed
audit_broker_delivery_pending
audit_broker_accepted
```

A component reports completion only after the contractually required local receipt state is durable.

A malformed or rejected event creates an observable failure path. It does not disappear.

### 6.2 Creating private proof

Private proof creation:

1. identifies the source event and owner;
2. selects the minimum supporting records;
3. applies the primary audit class;
4. records classification and policy versions;
5. preserves provenance;
6. applies required integrity protection;
7. stores the proof in the protected location;
8. creates the protected proof receipt;
9. records retention and destruction rules;
10. registers applicable recourse relationships.

A proof package can consist of governed references rather than copied content.

### 6.3 Creating a public projection

A public projection workflow:

1. identifies the accountability purpose;
2. identifies the intended audience;
3. selects the public claim;
4. identifies the protected proof supporting the claim;
5. evaluates classification, privacy, consent, cultural rights, legal, security, and re-identification risk;
6. tests whether an aggregate, pseudonymous, redacted, delayed, or cryptographic form is sufficient;
7. applies the approved projection rule;
8. validates the output deterministically;
9. obtains required approvals;
10. submits a publication request through Publication Gateway;
11. reconciles the destination result;
12. stores public and restricted receipts separately.

The public projection remains a distinct artifact from its source proof.

### 6.4 Projection transformations

Projection transformations include:

```text
field_projection
redaction
pseudonymization
aggregation
generalization
time_delay
format_conversion
cryptographic_proof
watermark
signature
packaging
```

An external AI transformation remains candidate-only. The workflow preserves provenance, performs deterministic validation where possible, requires human review, and publishes only the accepted output.

### 6.5 Public receipt fields

A public receipt normally identifies:

```text
receipt_id
event_or_process_class
authority_or_rule_ref
public_subject_ref_or_aggregate
outcome
reason_code_refs
artifact_or_version_refs
occurred_at
verification_status
correction_or_withdrawal_status
public_recourse_ref
```

It omits protected actor identity and detailed evidence unless disclosure authority requires them.

### 6.6 Publishing public evidence

Publication uses the registered publication-request contract.

The request identifies:

- selected public content;
- source owner;
- audience;
- destination;
- purpose;
- policy decision;
- consent and cultural-rights decisions;
- classification;
- projection transformations;
- approvals;
- provenance;
- integrity;
- withdrawal and supersession behavior.

Publication success requires destination confirmation, local reconciliation, and durable receipts.

### 6.7 Correcting and superseding public evidence

A correction or supersession:

1. preserves the original public artifact;
2. identifies the reason;
3. creates a replacement artifact where required;
4. updates discoverability and reliance status;
5. links original and replacement;
6. records the approving authority;
7. verifies destination state;
8. creates public and restricted receipts;
9. keeps the original private proof under its retention policy.

Historical truth is preserved without continuing to present the old artifact as current.

### 6.8 Withdrawing public evidence

Withdrawal:

1. records the withdrawal authority and reason;
2. stops new publication or access where applicable;
3. submits destination removal, unpublish, expiry, or replacement actions;
4. verifies the destination result;
5. updates indexes and authorized caches;
6. preserves the minimum withdrawal receipt;
7. protects the private proof according to rights and retention policy;
8. keeps the recourse path available.

A withdrawal receipt does not reproduce the withdrawn protected content.

## 7. Private Proof Access and Safe Failure

### 7.1 Access request

A private proof access request includes:

```text
request_id
requester_identity_ref
authority_scope_ref
purpose_ref
case_or_review_ref
selected_proof_refs
requested_view
minimization_rule_ref
policy_decision_ref
requested_at
expires_at
destination_ref
export_restrictions
```

The request uses a closed schema.

### 7.2 Access decision

Before access, the system verifies:

- requester identity;
- reviewing role;
- authority scope;
- purpose;
- case or review relationship;
- policy decision;
- consent and cultural rights;
- privacy and legal restrictions;
- security classification;
- time and expiry;
- requested fields;
- destination;
- export restrictions;
- conflict of interest and separation of duties where applicable.

A denial returns reason codes without revealing protected content.

### 7.3 Minimized access views

Approved access can return:

- a field-limited view;
- a redacted record;
- an aggregate;
- a pseudonymous record;
- a signed manifest;
- a cryptographic proof;
- a controlled viewing session;
- a destination-bound protected export;
- a governed reference resolved inside the authorized review environment.

The access view is attributable and expires according to policy.

### 7.4 Access receipt

Access to private proof creates a protected receipt identifying:

- requester;
- approving authority;
- purpose;
- proof selection;
- view or export type;
- destination;
- access time;
- expiry;
- result;
- reason codes;
- correlation identity;
- subsequent deletion or return obligation.

The receipt does not contain the proof payload.

### 7.5 Export

A protected export includes:

- manifest;
- selected evidence references or payloads;
- classification;
- destination;
- purpose;
- expiry;
- policy and approval references;
- provenance;
- functional integrity;
- signature where required;
- recipient obligations;
- destruction or return rules.

An export remains private proof and does not become public evidence.

### 7.6 Failure behavior

| Failure | Required behavior |
| --- | --- |
| Evidence classification unknown | Restrict or reject access and projection. |
| Producer identity invalid | Quarantine the event or proof. |
| Receipt schema incompatible | Reject or migrate through a validated path. |
| Integrity verification fails | Quarantine and preserve tamper evidence. |
| Public projection risks re-identification | Aggregate, pseudonymize, delay, restrict, or withhold. |
| Consent or cultural-rights authority absent | Block the affected access or disclosure. |
| Access purpose outside scope | Reject. |
| Destination outside authority | Reject export or publication. |
| Proof unavailable | Record the evidence gap and avoid invented findings. |
| Audit Broker unavailable | Preserve local durable capture and retry. |
| Publication Gateway unavailable | Preserve approved projection as deferred. |
| Destination outcome unknown | Reconcile before retry. |
| Withdrawal incomplete | Keep the public status explicit and continue verified remediation. |
| Remedy execution fails | Record failed remedy and escalate. |
| Resource pressure | Preserve critical proof and receipts before projections or analytics. |
| Network unavailable | Continue local capture, access where authorized, and recourse intake; defer boundary crossing. |

A failure does not create disclosure permission.

## 8. Security, Privacy, and Trust Boundaries

### 8.1 Data minimization

Evidence collection, proof construction, access, export, and publication each apply minimum-necessary selection separately.

A broad source record can support a narrow public statement without copying the full record into the public artifact.

### 8.2 Identity exposure

Public receipts favor:

- aggregate counts;
- role identifiers;
- pseudonymous identifiers;
- organization or authority identifiers;
- non-identifying verification handles.

Named identity appears only when the accountability purpose and disclosure authority require it.

### 8.3 Re-identification

Re-identification review considers:

- rare event combinations;
- small groups;
- precise time;
- precise location;
- linked public datasets;
- unique artifact versions;
- cultural context;
- sequence of actions;
- security details;
- repeated pseudonyms.

A technically redacted artifact can remain unsafe when surrounding facts identify a person or community.

### 8.4 Cultural rights and collective authority

Cultural-rights controls apply to:

- sacred or restricted content;
- community-held knowledge;
- collective identity;
- culturally sensitive locations;
- language and interpretation context;
- community authority;
- withdrawal and redistribution;
- retention and destruction.

A community can require a restricted proof process even when a generic public disclosure rule would otherwise permit publication.

### 8.5 Secrets and security details

Public evidence excludes:

- credentials;
- private keys;
- recovery material;
- secret references that reveal protected topology;
- exploit details;
- unrestricted host diagnostics;
- sensitive network configuration;
- device identifiers;
- protected logs.

Private proof access to these data remains separately authorized.

### 8.6 Integrity and authenticity

Evidence artifacts use functional integrity and authenticity controls according to their contracts.

Controls can include:

- signed receipts;
- authenticated manifests;
- artifact digests;
- sequence records;
- append-only or tamper-evident storage;
- trusted timestamps;
- cryptographic proof;
- signer and trust references.

Integrity proves that the artifact has not changed under the stated mechanism. It does not prove that the underlying decision was fair or authorized.

### 8.7 AI boundary

Native audit capture and proof verification remain deterministic and non-AI.

External AI can assist with candidate redaction, summarization, or review preparation only through controlled export and return. It has no direct access to private proof unless the disclosure authority explicitly permits the selected input, and it cannot issue final findings or recourse decisions.

### 8.8 Component boundaries

Audit Broker does not publish directly outside its governed audit interfaces.

Publication Gateway does not gain unrestricted access to private proof. It receives only the approved public projection and its governed metadata.

Source components do not write Audit Broker stores directly except through registered receipt interfaces.

## 9. Recourse, Offline Operation, and Exceptions

### 9.1 Recourse path

A consequential public artifact exposes a recourse path that can support:

- correction;
- explanation;
- evidence submission;
- identity correction;
- classification review;
- access restriction;
- withdrawal;
- supersession;
- republication;
- restoration;
- deletion where permitted;
- another policy-authorized remedy.

The public recourse entry can be minimal while the case remains protected.

### 9.2 Recourse evidence

A recourse case preserves:

```text
case_id
challenged_public_artifact_ref
challenged_decision_or_receipt_ref
private_proof_refs
claimant_or_representative_ref
requested_remedy
review_authority_ref
deadlines
submitted_evidence_refs
decision
reason_codes
remedy_ref
remedy_status
closure_ref
```

High-impact or conflict-sensitive cases use independent human review when the applicable policy requires separation.

### 9.3 Remedy verification

A remedy reaches completion only when the system verifies the authoritative effect.

Examples include:

- corrected public artifact present;
- withdrawn artifact no longer available under the governed destination;
- access restriction active;
- restored record readable;
- replacement publication reconciled;
- affected cache or index updated;
- failed decision re-executed;
- required notice delivered.

A planned remedy is not a completed remedy.

### 9.4 Offline operation

Offline-capable profiles preserve:

- local receipt capture;
- local sequencing;
- integrity protection;
- private proof storage;
- access-control state;
- recourse intake;
- withdrawal requests;
- deferred publication and export queues;
- duplicate-safe reconciliation metadata.

On reconnection, each boundary-crossing action is revalidated.

### 9.5 Exceptions

A bounded exception can adjust:

- a retention period;
- an evidence view;
- a redaction implementation;
- a cryptographic proof mechanism;
- an access environment;
- a review role;
- a profile-specific offline export interval;
- an evidence test environment.

An exception cannot:

- collapse public and private evidence;
- create universal public logging;
- remove audit-class separation;
- exempt protected evidence access from auditing;
- permit secret material in public receipts;
- bypass consent, cultural rights, privacy, legal, or security controls;
- make external AI authoritative;
- remove recourse for a consequential public artifact;
- rewrite historical receipts;
- create an unrestricted proof export;
- support an unqualified conformance claim outside its scope.

## 10. Validation Criteria

This document is conformant when validation confirms:

1. the five audit classes remain distinct;
2. every critical source event maps to a registered producer, receipt schema, class, retention policy, and owner;
3. public evidence uses minimum-necessary fields;
4. public projections preserve source-to-proof traceability without exposing protected references improperly;
5. public and private artifacts have separate classifications, schemas, stores, access rules, and lifecycle;
6. named identity appears only under explicit disclosure authority;
7. aggregate, pseudonymous, redacted, delayed, and cryptographic alternatives are evaluated;
8. re-identification risk is reviewed;
9. every projection records rule, policy, provenance, integrity, and publication receipt;
10. non-deterministic candidate transformations receive provenance and human acceptance;
11. external AI cannot publish or adjudicate directly;
12. Audit Broker and Publication Gateway remain separate;
13. protected receipt capture precedes reported completion where required;
14. ordinary passive interface activity does not create excessive constitutional receipts;
15. private proof access uses a closed request and current authority;
16. each restricted access creates an access receipt;
17. exports are purpose-, destination-, and time-bound;
18. unrestricted dumps and raw proof copies are absent;
19. integrity and signature controls match artifact contracts;
20. ordinary Markdown hashes are absent as a requirement;
21. historical schema, policy, classification, producer, and provenance versions remain interpretable;
22. correction, supersession, withdrawal, and remedy preserve the original record and add linked history;
23. cultural-rights, consent, privacy, legal, and security controls apply at every evidence transition;
24. public-interest claims do not silently override protected rights;
25. consequential public artifacts expose recourse;
26. recourse does not force protected proof into public disclosure;
27. remedies are verified before completion;
28. offline capture, intake, and deferred queues remain durable;
29. reconnection uses duplicate-safe reconciliation and authority revalidation;
30. resource pressure preserves critical evidence before optional projection;
31. all decisions, components, profiles, artifacts, tests, evidence, receipts, cases, remedies, and exceptions resolve;
32. no prohibited open-state marker enters active security authority.

The principal validation entry point is:

```bash
python docs/tools/validate_docs.py
```

Supporting checks include:

```text
tools/check_component_boundaries.py
tools/check_artifact_contracts.py
tools/check_interfile_locks.py
tools/check_profile_inheritance.py
tools/check_ai_boundary.py
tools/check_traceability.py
tools/check_decision_closure.py
tools/check_no_unresolved_state.py
```

A failed evidence-boundary check blocks the affected public projection, proof access, export, publication, recourse closure, remedy completion, or conformance claim.

## 11. Non-Normative Examples

### 11.1 Release activation

A public receipt states that Release Set 1.1.0 was activated, lists the four channel versions, time, compatibility result, and outcome. Private proof retains node identity, operator identity, detailed tests, journal references, and failure diagnostics.

### 11.2 Restricted testimony

A recourse reviewer receives a redacted protected view of testimony. The public case status shows that protected evidence was reviewed without disclosing the testimony or witness identity.

### 11.3 Aggregate participation

A governance process publishes participation counts and approval outcome. Private proof retains eligible-member records, authenticated ballots, conflict checks, and review evidence.

### 11.4 Cultural withdrawal

A community authority withdraws distribution permission for a cultural object. The public receipt states that distribution was withdrawn. Private proof preserves the protected authority decision and cultural context under restricted access.

### 11.5 Security incident

A public incident notice states affected capability class, time range, containment status, and recovery status. Private proof retains host identifiers, exploit details, credentials affected, forensic evidence, and operator actions.

### 11.6 Cryptographic verification

A public artifact includes a signed manifest and proof that one protected receipt belongs to an authenticated evidence set. The protected receipt itself remains inaccessible.

### 11.7 Publication correction

A published record is corrected. The old public artifact remains marked superseded, the replacement becomes current, and private proof preserves the correction request, review, policy decision, and destination reconciliation.

### 11.8 Offline event

A sovereign-offline node captures a critical receipt and its proof locally. Public projection and remote export remain deferred. On reconnection, policy and rights are revalidated before publication.

### 11.9 AI-assisted redaction

An authorized reviewer sends selected non-secret text through the approved ChatGPT surface for candidate redaction. The result retains provenance, receives deterministic checks and human review, and remains separate from the protected source.

### 11.10 Failed remedy

A recourse decision orders restoration, but the backup cannot be restored. The case records failed remedy evidence and escalation rather than reporting completion.
