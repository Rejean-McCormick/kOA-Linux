<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SEC-017",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "security",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "contracts/integration-types.contract.json"
  ],
  "decision_ids": [
    "DEC-GATE-001",
    "DEC-GOV-001",
    "DEC-DATA-001",
    "DEC-CULT-001",
    "DEC-CULT-002",
    "DEC-CULT-003",
    "DEC-CULT-004",
    "DEC-CULT-005",
    "DEC-AUDIT-001",
    "DEC-OFFLINE-001",
    "DEC-AI-001",
    "DEC-REL-001",
    "DEC-SEC-001"
  ],
  "requirement_ids": [
    "REQ-SEC-PUB-001",
    "REQ-SEC-PUB-002",
    "REQ-SEC-PUB-003",
    "REQ-SEC-PUB-004",
    "REQ-SEC-PUB-005",
    "REQ-SEC-PUB-006",
    "REQ-SEC-PUB-007",
    "REQ-SEC-PUB-008",
    "REQ-SEC-PUB-009",
    "REQ-SEC-PUB-010",
    "REQ-SEC-PUB-011",
    "REQ-SEC-PUB-012",
    "REQ-SEC-PUB-013",
    "REQ-SEC-PUB-014",
    "REQ-SEC-PUB-015",
    "REQ-SEC-PUB-016",
    "REQ-SEC-PUB-017",
    "REQ-SEC-PUB-018",
    "REQ-SEC-PUB-019",
    "REQ-SEC-PUB-020",
    "REQ-SEC-PUB-021",
    "REQ-SEC-PUB-022",
    "REQ-SEC-PUB-023",
    "REQ-SEC-PUB-024",
    "REQ-SEC-PUB-025",
    "REQ-SEC-PUB-026",
    "REQ-SEC-PUB-027",
    "REQ-SEC-PUB-028",
    "REQ-SEC-PUB-029",
    "REQ-SEC-PUB-030"
  ],
  "lock_ids": [
    "LOCK-GATE-001",
    "LOCK-GOV-001",
    "LOCK-DATA-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-CULT-001",
    "LOCK-CULT-002",
    "LOCK-CULT-003",
    "LOCK-CULT-004",
    "LOCK-CULT-005",
    "LOCK-CULT-006",
    "LOCK-CULT-007",
    "LOCK-CULT-008",
    "LOCK-CULT-009",
    "LOCK-CULT-010",
    "LOCK-AUDIT-001",
    "LOCK-OFFLINE-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-SEC-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-SEC-000",
    "DOC-SEC-001"
  ],
  "tags": [
    "security",
    "normative-markdown",
    "17",
    "cross",
    "domain",
    "publication"
  ]
}
KOA:DOC-META:END -->

# Cross-Domain Publication

## 1. Purpose

This document defines the security model for publishing information from one kOA authority or disclosure domain into another.

Cross-domain publication is a governed release, not a database copy, network transfer, user-interface action, synchronization side effect, or change in storage location. It occurs when content or a derived representation becomes available to a destination, audience, tenant, component, federation peer, public domain, or external provider whose authority or disclosure scope differs from the source.

The model exists to ensure that:

- source ownership remains with the source component;
- publication authority is evaluated independently from access and storage authority;
- the exact source version is bound before a decision;
- destination, audience, purpose, duration, and redistribution scope are explicit;
- only a bounded and approved representation crosses the boundary;
- every transformation has its own authority;
- consent and cultural-rights restrictions remain enforceable;
- partial delivery cannot be reported as complete;
- publication history remains truthful after withdrawal or revocation;
- public accountability does not force indiscriminate disclosure;
- offline queueing does not become delayed automatic publication;
- external services do not become authoritative publication actors.

Publication Gateway is the execution and receipt boundary for governed cross-domain publication. This document defines the security conditions around that boundary.

## 2. Scope

### 2.1 Covered publication domains

This document applies to publication between:

- private and public component domains;
- two tenants;
- two authority domains within one tenant;
- a user endpoint and a sovereign hub;
- a sovereign hub and a configured federation peer;
- a local component and an approved external destination;
- Orgo and Konnaxion;
- the kOA Mediatheque and an external destination, including UCKK;
- Kristal and an application distribution domain;
- one geographic or community audience and another;
- one confidentiality class and a less restrictive class;
- one profile deployment and another deployment where disclosure scope changes.

A transfer that remains inside one authority and disclosure domain still uses its component integration contract, but it is not classified as cross-domain publication unless the active policy states otherwise.

### 2.2 Covered publication forms

The model covers:

- exact bounded copies;
- redacted derivatives;
- translated derivatives;
- transcoded derivatives;
- summarized derivatives;
- composite publications;
- restricted public links;
- authenticated-domain releases;
- federation exports;
- external-provider delivery;
- corrections and republications;
- withdrawal and downstream remediation.

### 2.3 Distinct operations

The following operations remain distinct:

| Operation | Security meaning |
| --- | --- |
| Ingestion | Admission of material into an owning local component, including the kOA Mediatheque. |
| Storage | Retention within an owning component’s authority. |
| Access | Reading within an already authorized domain. |
| Internal processing | Use without changing the audience or authority domain. |
| Synchronization | Contracted replication or state exchange within declared trust scopes. |
| Publication | Release to a different audience, authority, disclosure, tenant, or external domain. |
| Republication | A later publication with a new or changed destination, audience, purpose, representation, or authority context. |
| External processing | Transfer to a provider for a bounded operation, with controlled return and acceptance. |
| Export | Creation of a user- or system-controlled package; export does not itself authorize recipient disclosure. |

Approval of one operation does not authorize another.

### 2.4 Profile applicability

This document applies globally.

Profiles can select different transports and operational arrangements:

- a lightweight endpoint can publish to a configured hub;
- a sovereign hub can publish locally, to federation peers, or to approved external destinations;
- a developer workstation can exercise test publication boundaries without making a production publication claim;
- a sovereign-offline overlay can restrict publication to locally reachable approved domains;
- a high-assurance overlay can require stronger human review, separation of duties, or evidence.

A profile does not alter source ownership or bypass the Publication Gateway.

### 2.5 Excluded authority

This document does not:

- determine semantic truth;
- select content on behalf of the source owner;
- grant cultural authority;
- grant consent;
- determine legal ownership;
- define local Mediatheque admission or remote UCKK acceptance;
- replace identity and trust;
- replace Governance Policy Runtime;
- replace Audit Broker;
- define every destination protocol;
- guarantee deletion outside kOA control;
- convert public availability into unrestricted permission;
- make a successful network transfer equivalent to accepted publication.

## 3. Canonical References

| Canonical reference | Responsibility |
| --- | --- |
| `contracts/system.contract.json` | Owns the global gateway, authority, data-ownership, offline, safe-degradation, and external-integration model. |
| `generated/component-catalog.json` | Owns component identities, responsibilities, authoritative data, and primary interfaces. |
| `contracts/integration-types.contract.json` | Owns registered publication and destination integrations, their participants, direction, data movement, and lifecycle. |

Supporting canonical contracts include:

- `contracts/components/publication-gateway.component.json`;
- `contracts/artifact-contracts/publication-request.schema.json`;
- `contracts/artifact-contracts/publication-receipt.schema.json`;
- `contracts/artifact-contracts/cultural-rights-policy.schema.json`;
- `contracts/artifact-contracts/provenance-receipt.schema.json`;
- `contracts/artifact-contracts/integration-manifest.schema.json`;
- `generated/authority-manifest.json`;
- `generated/requirements-index.json`;
- `generated/assertion-index.json`;
- `generated/evidence-catalog.json`;
- `generated/exception-index.json`;
- `contracts/release-channels.contract.json`.

Related explanatory authority includes:

- `01-constitution/12-cultural-rights-and-consent.md`;
- `04-components/03-component-integration-boundaries.md`;
- `07-security/08-network-boundaries.md`;

The machine-readable contracts own the artifact fields and lifecycle values. This document explains the security model and required controls.

## 4. Model and Responsibilities

### 4.1 Publication security objects

A governed publication uses these objects:

| Object | Responsibility |
| --- | --- |
| Publication request | Declares exact source, source version, destination, audience, purpose, representation, transformations, and authority references. |
| Source binding | Fixes the object and version supplied by the owning component. |
| Publication decision | Records allow, deny, blocked, or review-required outcome and obligations. |
| Bounded representation | Contains only the approved content and context for the declared destination. |
| Staging record | Tracks inactive preparation before delivery. |
| Execution record | Tracks delivery attempts, acknowledgements, failure, and partial effects. |
| Publication receipt | Preserves immutable historical evidence of the terminal execution result. |
| Publication-state change | Records expiry, withdrawal, revocation, correction, remediation, or external limitation. |
| Evidence references | Permit selective validation without duplicating protected source material. |

### 4.2 Source component responsibility

The source component:

- owns the authoritative source object;
- supplies a stable source reference and version;
- identifies the source authority domain;
- selects or approves the content proposed for publication;
- validates any source-side transformation;
- accepts externally produced candidate material before it enters a publication representation;
- remains responsible for source lifecycle and semantic correctness.

The source component does not execute cross-domain release directly.

### 4.3 Publication Gateway responsibility

Publication Gateway:

- validates the request contract;
- binds the request to the stable source version;
- resolves identity, delegation, trust, consent, cultural authority, policy, exceptions, and time validity;
- produces a decision;
- stages only the approved representation;
- verifies decision obligations before delivery;
- delivers only to the declared destination;
- handles idempotency and bounded retries;
- records destination acknowledgement;
- produces the publication receipt;
- processes later withdrawal or remediation state.

Publication Gateway does not own source content, assign cultural authority, grant consent, determine semantic truth, or write directly into source or destination authoritative storage.

### 4.4 Destination responsibility

The destination:

- exposes a declared publication interface;
- authenticates Publication Gateway;
- validates the destination contract;
- validates tenant and authority scope;
- deduplicates repeated delivery where required;
- accepts or rejects the bounded representation;
- assigns a destination object reference after acceptance;
- preserves received restrictions and attribution;
- returns an acknowledgement;
- supports withdrawal or correction operations described by its contract.

Transport success without destination acceptance is not a completed publication.

### 4.5 Authority evaluation

Publication authority combines distinct checks:

- requester identity;
- source-component authority;
- delegation;
- tenant and authority domain;
- trust scope;
- consent;
- cultural authority;
- governance policy;
- audience;
- purpose;
- requested transformations;
- destination;
- duration;
- redistribution;
- human review;
- exception validity;
- time validity;
- evidence availability.

A missing or ambiguous check does not default to approval.

### 4.6 Bounded representation

The release representation is separate from the authoritative source.

It contains the minimum material required for the approved purpose and audience. It preserves required context, attribution, anonymity, access controls, expiry, and redistribution restrictions.

The representation can be:

- an exact bounded copy;
- a redacted derivative;
- a translated derivative;
- a transcoded derivative;
- a summarized derivative;
- a composite derivative.

Each transformation has explicit authority and provenance. A staged representation never becomes source authority merely because it was published.

### 4.7 Transformation security

A transformation record identifies:

- transformation class;
- input reference;
- output reference;
- authority;
- performer;
- tool or component;
- external integration where used;
- acceptance by the source-owning component;
- restrictions carried forward.

External AI, translation, voice, or creative output remains candidate material until component acceptance.

A transformation that cannot preserve required context or restrictions is rejected.

### 4.8 Audience and destination security

Audience and destination are independent.

The destination identifies the receiving system or domain. The audience identifies who can receive or access the representation.

A destination can host several audiences. An audience can be implemented by several destinations. Both remain explicit in the request, decision, execution, and receipt.

Audience classes can include:

- named individuals;
- named groups;
- authenticated tenants;
- authenticated domains;
- restricted public audiences;
- public audiences.

An unspecified or wildcard audience is not accepted for governed publication.

### 4.9 Network boundary

Publication traffic uses a declared route from Publication Gateway to the destination.

The route validates:

- service identities;
- transport;
- destination endpoint;
- tenant or authority scope;
- payload contract;
- size and rate limits;
- timeouts;
- retry behavior;
- acknowledgement;
- observability.

Internal location, private addressing, loopback, shared host, cluster membership, or valid transport credentials do not replace publication authorization.

### 4.10 Idempotency and delivery

Each request has a stable request identity and idempotency key.

Duplicate requests return the existing compatible state or receipt rather than create duplicate effects.

Delivery semantics are explicitly declared. Partial delivery enters remediation. A retry revalidates authority, source version, destination, representation, credentials, time, and conflict state before another effect.

### 4.11 Publication receipt

The receipt records:

- request identity;
- allow decision;
- source component, object, and version;
- destination and audience;
- purpose;
- representation and transformations;
- authority references;
- execution result;
- destination acknowledgement;
- provenance;
- evidence;
- current publication state.

The receipt is historical evidence. Withdrawal, expiry, or revocation adds a state-change record and does not erase the earlier fact.

### 4.12 Selective evidence

Public evidence can show that:

- a request was authorized;
- the required policy and consent existed;
- the approved representation was delivered;
- the destination acknowledged acceptance;
- a later withdrawal occurred.

Protected source content, private identities, restricted cultural details, and confidential decision evidence remain behind selective-audit controls unless separately authorized.

### 4.13 Revocation and withdrawal

Revocation or withdrawal:

- stops future publication under the affected authority;
- cancels reversible pending work;
- prevents queued release;
- requests local destination removal where supported;
- issues downstream notices where supported;
- records systems outside kOA control;
- preserves historical receipts;
- does not claim guaranteed external deletion without destination support.

### 4.14 Corrections and republication

A correction that changes content, source version, audience, destination, purpose, or transformation uses a new publication request and receipt.

A bounded clerical correction to receipt metadata uses explicit receipt lineage and cannot rewrite the execution result or historical publication fact silently.

### 4.15 Offline publication

Local cross-domain publication can proceed offline only when every required identity, trust, consent, cultural-rights, governance, destination, time, and evidence dependency is locally available and valid.

Remote publication work can be queued only when the request contract permits it. Reconnection triggers complete revalidation and does not authorize automatic release.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SEC-PUB-001,REQ-SEC-PUB-002,REQ-SEC-PUB-003,REQ-SEC-PUB-004,REQ-SEC-PUB-005,REQ-SEC-PUB-006,REQ-SEC-PUB-007,REQ-SEC-PUB-008,REQ-SEC-PUB-009,REQ-SEC-PUB-010,REQ-SEC-PUB-011,REQ-SEC-PUB-012,REQ-SEC-PUB-013,REQ-SEC-PUB-014,REQ-SEC-PUB-015,REQ-SEC-PUB-016,REQ-SEC-PUB-017,REQ-SEC-PUB-018,REQ-SEC-PUB-019,REQ-SEC-PUB-020,REQ-SEC-PUB-021,REQ-SEC-PUB-022,REQ-SEC-PUB-023,REQ-SEC-PUB-024,REQ-SEC-PUB-025,REQ-SEC-PUB-026,REQ-SEC-PUB-027,REQ-SEC-PUB-028,REQ-SEC-PUB-029,REQ-SEC-PUB-030 -->
- **REQ-SEC-PUB-001 — SHALL:** Every cross-domain publication execute through Publication Gateway using a valid publication request.
- **REQ-SEC-PUB-002 — SHALL NOT:** Source access, storage, ingestion, synchronization, administrative capability, public availability, network reachability, or prior publication be treated as current publication authority.
- **REQ-SEC-PUB-003 — SHALL:** A publication request identify the requester, source component, source object, source version, source authority domain, destination, audience, purpose, representation, transformations, consent, cultural-rights policy, governance context, and idempotency key.
- **REQ-SEC-PUB-004 — SHALL NOT:** Wildcard sources, implicit audiences, implicit destinations, implicit purposes, or unbounded collection publication be accepted.
- **REQ-SEC-PUB-005 — SHALL:** The source-owning component bind and validate the exact source version before publication approval.
- **REQ-SEC-PUB-006 — SHALL NOT:** Publication Gateway or a destination write directly into the source component’s authoritative storage.
- **REQ-SEC-PUB-007 — SHALL:** Identity, delegation, trust, consent, cultural authority, governance policy, exception, human review, and time validity be evaluated independently.
- **REQ-SEC-PUB-008 — SHALL:** Missing, ambiguous, expired, revoked, conflicting, or incompatible authority block, deny, or require human review for the affected request.
- **REQ-SEC-PUB-009 — SHALL:** The approved release representation be bounded, minimum-necessary, destination-specific, audience-specific, purpose-specific, and separate from source authority.
- **REQ-SEC-PUB-010 — SHALL:** Required attribution, anonymity, context, language, access, duration, geographic, redistribution, and cultural restrictions remain attached to the representation.
- **REQ-SEC-PUB-011 — SHALL NOT:** A transformation execute without explicit transformation authority and receiving-component acceptance.
- **REQ-SEC-PUB-012 — SHALL NOT:** External AI, external creative services, external translation, external voice, or SenTient output become authoritative publication content without controlled component acceptance.
- **REQ-SEC-PUB-013 — SHALL:** Publication Gateway and kOA Mediatheque admission remain separate identities, authorities, routes, decisions, data stores, and receipt producers; the UCKK adapter shall operate only within an authorized publication request.
- **REQ-SEC-PUB-014 — SHALL NOT:** Successful local Mediatheque admission authorize publication, successful UCKK delivery alter local authority, or remote UCKK acceptance be treated as local admission.
- **REQ-SEC-PUB-015 — SHALL:** Publication delivery use a declared integration and authenticated destination identity.
- **REQ-SEC-PUB-016 — SHALL NOT:** Internal network location, loopback, shared host, container network, cluster membership, valid certificate, or valid signature be treated as sufficient publication authorization.
- **REQ-SEC-PUB-017 — SHALL:** Every mutation-capable publication request use a stable request identity and idempotency key.
- **REQ-SEC-PUB-018 — SHALL:** Destination acknowledgement distinguish accepted, rejected, and unknown outcomes.
- **REQ-SEC-PUB-019 — SHALL NOT:** Transport success, request timeout, queue removal, or partial delivery be reported as completed publication.
- **REQ-SEC-PUB-020 — SHALL:** Partial delivery identify delivered and undelivered units, enter remediation, and prevent blind or silent retry.
- **REQ-SEC-PUB-021 — SHALL:** A terminal execution produce a durable publication receipt or avoid reporting success.
- **REQ-SEC-PUB-022 — SHALL:** Publication receipts preserve historical source, decision, representation, destination, audience, execution, provenance, and evidence references.
- **REQ-SEC-PUB-023 — SHALL:** Revocation, withdrawal, expiry, or correction stop applicable future operations and preserve truthful historical receipts.
- **REQ-SEC-PUB-024 — SHALL NOT:** kOA claim guaranteed deletion from an external destination that does not provide and acknowledge that capability.
- **REQ-SEC-PUB-025 — SHALL:** Public evidence use selective disclosure and exclude source content, private identities, and restricted cultural details unless separately authorized.
- **REQ-SEC-PUB-026 — SHALL:** Remote publication queues be bounded, durable where required, cancellable, expiring, and non-executing while offline.
- **REQ-SEC-PUB-027 — SHALL:** Queued publication be revalidated after reconnection against source version, identity, delegation, trust, revocation, consent, policy, destination, audience, representation, credentials, time, and conflict state.
- **REQ-SEC-PUB-028 — SHALL NOT:** Connectivity restoration automatically release, retry, broaden, or substitute a queued publication.
- **REQ-SEC-PUB-029 — SHALL:** Publication component, artifact, integration, profile, governance, and Release Set versions remain compatible at execution time.
- **REQ-SEC-PUB-030 — SHALL NOT:** A profile, recipe, generated context, migration record, administrative shortcut, external provider, or implementation convenience bypass or weaken the publication boundary.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Publication request creation

The source-side workflow is:

1. Identify the authoritative source component.
2. Identify the exact source object and version.
3. Identify the source authority domain.
4. Select the proposed destination and audience.
5. Declare purpose, duration, and redistribution conditions.
6. Select the minimum representation.
7. Declare every transformation.
8. Resolve consent and cultural-rights records.
9. Resolve requester identity and delegation.
10. Create the publication request and idempotency key.
11. Submit through the authenticated Publication Gateway interface.
12. Keep the source unchanged while the request is evaluated.

### 6.2 Admission and decision

Publication Gateway evaluates the request through:

1. Validate artifact structure and size.
2. Authenticate requester and source component.
3. Verify tenant and authority-domain scope.
4. Bind the source object and version.
5. Resolve trust and revocation.
6. Resolve consent and cultural authority.
7. Resolve governance policy and exceptions.
8. Validate destination and audience.
9. Validate representation and transformations.
10. Validate time and expiry.
11. Determine required human review.
12. Produce allow, deny, blocked, or review-required result.
13. Record obligations and supporting evidence.

Only an allow result whose obligations pass can enter staging.

### 6.3 Representation staging

Staging proceeds through:

1. Retrieve or receive the bounded source representation.
2. Confirm that the source version still matches.
3. Apply authorized redaction, translation, transcoding, summarization, or composition.
4. Record transformation provenance.
5. Require component acceptance for candidate output.
6. Attach attribution, context, access, retention, and redistribution controls.
7. Validate minimum-necessary content.
8. Validate destination media and artifact contracts.
9. Keep staged material inactive.
10. Produce the ready-for-delivery state.

### 6.4 Execution

Execution proceeds through:

`text
approved
 -> staging
 -> ready
 -> publishing
 -> published | partially_delivered | failed
 -> remediating | closed
`

Before delivery:

1. Revalidate decision obligations.
2. Revalidate source version.
3. Revalidate destination identity and contract.
4. Revalidate consent, trust, policy, and time.
5. Acquire bounded resources.
6. Open the declared route.
7. Send only the approved representation.
8. Receive destination acknowledgement.
9. Commit the execution result.
10. Produce the receipt.

### 6.5 Idempotent retry

A retry proceeds through:

1. Resolve the original request and idempotency key.
2. Inspect the existing execution and destination state.
3. Determine whether an effect could already exist.
4. Revalidate all mutable authority and compatibility dimensions.
5. Reject a payload or scope mismatch.
6. Retry only the undelivered bounded effect.
7. Preserve previous attempt history.
8. Record the new acknowledgement or failure.
9. Avoid duplicate destination objects where the destination supports deduplication.

### 6.6 Partial delivery remediation

When partial delivery occurs:

1. Stop blind retry.
2. Record delivered and undelivered units.
3. Query destination state through the declared interface.
4. Prevent new publication under the same request.
5. Notify the source owner and required reviewers.
6. Decide whether to complete, withdraw, correct, or close with limitation.
7. Execute only the approved remediation.
8. Produce remediation evidence.
9. Update publication state without rewriting history.

### 6.7 Withdrawal or revocation

The withdrawal workflow is:

1. Authenticate the requesting authority.
2. Resolve the affected publication scope.
3. Stop new and queued publication.
4. Cancel reversible pending execution.
5. Request removal or access restriction at controlled destinations.
6. Issue supported downstream notices.
7. Record unsupported external deletion.
8. Preserve the original receipt.
9. Add the publication-state change record.
10. Provide selective evidence of completion and remaining limitations.

### 6.8 Correction and republication

A content correction proceeds through a new request:

1. Bind the corrected source version.
2. identify the prior receipt;
3. Resolve authority again.
4. Rebuild the bounded representation.
5. Publish through the complete workflow.
6. Link the new receipt to the prior publication.
7. Withdraw or supersede the destination object where authorized.
8. Preserve both historical records.

### 6.9 Offline queue and reconnection

When a remote destination is unavailable:

1. Determine whether queueing is permitted.
2. Persist the exact request, source version, authority references, representation identity, destination, and expiry.
3. Mark the work as pending and non-executing.
4. Preserve user cancellation.
5. Continue unrelated local work.
6. After reconnection, refresh every mutable authority and compatibility input.
7. Detect source, destination, or remote-state conflicts.
8. Release only if the request still passes.
9. Retain, cancel, or replace invalid work.
10. Record the final outcome.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Preserved capability | Denied capability |
| --- | --- | --- | --- |
| Request contract invalid | Deny before source retrieval or staging. | Source component operation | Publication |
| Source object missing | Block the request. | Other source objects | Requested publication |
| Source version changed | Require revalidation or a new request. | Current source state | Publication of stale version |
| Requester identity invalid | Reject the request. | Gateway health | Requested action |
| Delegation invalid | Deny or block according to policy. | Directly authorized operations | Delegated publication |
| Consent missing | Block publication. | Local storage and authorized access | Disclosure |
| Consent expired or revoked | Deny publication. | Historical evidence | New publication |
| Cultural authority disputed | Require competent human review. | Protected source custody | New high-impact release |
| Governance runtime unavailable | Block new governed decisions. | Existing safe local work | New publication |
| Destination identity invalid | Stop before delivery. | Staged inactive representation | Destination release |
| Destination contract incompatible | Block execution. | Source and request history | Incompatible delivery |
| Network unavailable | Queue or deny according to request policy. | Local editing and storage | Remote delivery |
| Trusted time uncertain | Block time-sensitive publication. | Non-time-sensitive local work | Expiry-sensitive release |
| Transformation fails | Reject the representation. | Original source | Invalid derivative |
| External transformation output unaccepted | Keep as candidate or reject. | Source authority | Publication of candidate |
| Attribution or context cannot be preserved | Deny publication. | Source and evidence | Context-breaking release |
| Resource capacity unavailable | Queue or deny without partial effect. | Accepted request state | Immediate execution |
| Destination rejects | Record failure and do not report publication. | Source state | Destination publication |
| Acknowledgement unknown | Enter uncertain or remediation state. | Request and attempt evidence | Completed-success claim |
| Partial delivery | Record exact partial effect and remediate. | Historical execution state | False completion |
| Receipt persistence fails | Avoid reporting success and enter repair state. | Destination-state investigation | Successful terminal claim |
| Revocation after publication | Stop future release and begin supported remediation. | Historical receipt | Further publication |
| External deletion unsupported | Record limitation and issue supported notice. | Local remediation | Guaranteed-erasure claim |
| Audit service unavailable | Retain local evidence and block when mandatory proof is absent. | Source and request state | Unprovable required publication |
| Release compatibility fails | Keep current active state and block execution. | Existing validated publications | Candidate-version publication |

Safe degradation keeps the source protected and the representation inactive. It does not bypass Publication Gateway, publish an older version, widen the audience, remove required context, switch providers, or infer authority.

## 8. Cross-Component Interactions

### 8.1 Orgo to Konnaxion

Orgo owns private workflow and case data. Konnaxion owns its public-domain state.

Orgo prepares a bounded source representation or approves one prepared under its authority. Publication Gateway mediates release. Konnaxion accepts the representation through its declared interface and assigns its own destination reference.

Neither component writes the other’s database.

### 8.2 kOA Mediatheque to external UCKK Moodle

The kOA Mediatheque owns local accepted media objects, versions, collections, provenance, rights, and access rules. The online UCKK Moodle platform independently owns only the content it accepts into its own domain. The reverse import direction is governed by a separate contract and never weakens this publication boundary.

Publication Gateway authorizes release from the kOA Mediatheque. The UCKK Publication Bridge packages and delivers the approved material to the authenticated external Moodle target and records its result. It does not write UCKK databases directly or merge authorities.

Admission receipts do not replace publication decisions.

### 8.3 Kristal distribution

Kristal Runtime can supply a verified artifact or bounded knowledge representation.

Publication or distribution to another authority domain retains artifact identity, provenance, rights, audience, and compatibility constraints. A consuming application accepts the artifact under its own contract.

### 8.4 Identity and Trust

Publication Gateway queries Identity and Trust for identity, delegation, trust, and revocation results.

It stores references and receipts rather than becoming the master identity authority.

### 8.5 Governance Policy Runtime

Publication Gateway sends the minimum policy context required for the publication decision.

Governance Policy Runtime returns a decision and obligations. It does not stage or deliver content.

### 8.6 Audit Broker

Publication Gateway sends bounded audit events and evidence references.

Audit Broker provides selective proof. It does not require full source content merely because the publication is auditable.

### 8.7 Resource Governor

Resource Governor controls staging storage, CPU, memory, concurrency, queue depth, and network egress.

Resource capacity cannot convert a denied publication into an allowed publication.

### 8.8 External destinations

An external destination requires an active integration manifest.

The manifest describes provider identity, route, data movement, retention, reuse, deletion support, response, acceptance, failure, and removal behavior.

No external destination becomes a default fallback.

### 8.9 Offline endpoints and sovereign hubs

A lightweight endpoint can queue a publication request to a configured hub. The endpoint retains source authority and pending state.

The hub revalidates identity, consent, source version, destination, audience, and compatibility before execution. Receipt references return to the endpoint through a declared integration.

### 8.10 Release lifecycle

Publication Gateway, request and receipt contracts, destination integration, profile, governance policy, and Release Set remain compatible.

An update that changes publication semantics does not process in-flight work silently under mixed contracts.

## 9. Decision Closure and Prohibited Assumptions

The accepted decisions referenced in the metadata close the cross-domain publication model.

The following assumptions are prohibited:

1. Read access authorizes publication.
2. Storage custody authorizes publication.
3. Ingestion authorizes publication.
4. Synchronization authorizes publication.
5. Prior publication creates permanent unrestricted permission.
6. Public availability removes consent or cultural restrictions.
7. The uploader owns every publication right.
8. An administrator possesses publication authority by default.
9. A source component can publish directly because it owns the source.
10. A destination can retrieve private source data directly.
11. Local Mediatheque admission is automatically a UCKK publication decision.
12. Successful UCKK delivery becomes local Mediatheque admission or transfers local authority.
13. Internal network location establishes trust.
14. A valid certificate or signature establishes complete publication authority.
15. A successful send is a successful publication.
16. A timeout proves no publication effect occurred.
17. A retry can create another destination object.
18. A queued request remains valid indefinitely.
19. Reconnection authorizes queued release.
20. A representation can omit required context for technical convenience.
21. Translation authority includes every other transformation.
22. External AI output is publishable without component acceptance.
23. SenTient output is authoritative.
24. A partial delivery can be reported as complete.
25. Revocation deletes historical truth.
26. External deletion can be guaranteed without destination acknowledgement.
27. Audit requires publishing private evidence.
28. A profile can bypass Publication Gateway.
29. A migration or update can reinterpret an in-flight request silently.
30. A generated context or recipe can broaden publication authority.

When source identity, authority, destination, audience, purpose, representation, transformation, time, compatibility, or delivery result is uncertain, the publication remains blocked or enters explicit remediation.

## 10. Validation Criteria

This document is conformant when:

1. It is registered as `DOC-SEC-017`.
2. Its path is `07-security/17-cross-domain-publication.md`.
3. Its class is `normative_markdown`.
4. Its status is `active`.
5. Its language is `en`.
6. Its layer is `security`.
7. Its scope is `global`.
8. Its metadata matches `generated/document-index.json`.
9. Every canonical reference resolves.
10. Every listed decision resolves with accepted status.
11. Every listed requirement resolves and matches the generated block.
12. Every listed lock resolves and passes.
13. The eleven mandatory sections exist in the required order.
14. Normative keywords occur only in the generated requirements block.
15. Every cross-domain publication resolves through Publication Gateway.
16. Every request validates against the publication-request contract.
17. Every source binding resolves to one source component, object, and version.
18. Wildcard and implicit publication scopes fail validation.
19. Identity, delegation, trust, consent, cultural authority, policy, exceptions, review, and time checks pass before allow.
20. Every staged representation is bounded and inactive before execution.
21. Every transformation resolves to authority and acceptance evidence.
22. External and SenTient output remains candidate material until accepted.
23. Local Mediatheque admission and external UCKK publication-boundary tests pass.
24. Direct source or destination database writes fail.
25. Every execution uses stable request identity and idempotency.
26. Destination acknowledgement is required for a published result.
27. Partial delivery cannot produce a completed-success state.
28. A successful terminal execution produces a conforming publication receipt.
29. Revocation and withdrawal preserve historical receipt evidence.
30. External-deletion limitations remain explicit.
31. Public evidence excludes unauthorized source content and private identities.
32. Offline queues remain non-executing and bounded.
33. Reconnection revalidation tests include all mutable authority and compatibility dimensions.
34. Mixed or incompatible component, artifact, integration, profile, governance, and Release Set versions block execution.
35. Traceability and active evidence are complete.
36. No unresolved marker, provisional value, parallel authority, or file-content hash requirement appears.
37. Complete documentation validation returns `pass`.

## 11. Non-Normative Examples

### 11.1 Private workflow summary to a public site

Orgo owns a private case. A human approves a redacted summary for a public Konnaxion audience. Publication Gateway binds the source version, verifies consent and policy, stages the approved summary, delivers it to Konnaxion, receives acceptance, and issues a receipt.

### 11.2 Local admission without UCKK publication

A user imports a photograph into a private kOA Mediatheque collection. Local admission succeeds. No UCKK publication occurs because there is no publication request, target, disclosure decision, or allow result.

### 11.3 Translation for a restricted audience

A source owner authorizes translation into French for one authenticated group. The translation is accepted by the source component and published only to that group. The grant does not authorize a public audience or another language.

### 11.4 External destination

A hub publishes a bounded report to an approved external destination. The integration manifest names the provider, retention, reuse, deletion support, and delivery acknowledgement. The receipt records that external deletion is request-based rather than guaranteed.

### 11.5 Duplicate request

A client retries after a timeout with the same idempotency key. Publication Gateway finds an accepted destination acknowledgement and returns the existing receipt instead of delivering again.

### 11.6 Partial delivery

A destination accepts two of three units before failing. The gateway records the exact partial effect, blocks silent retry, and enters remediation. It does not claim complete publication.

### 11.7 Consent revocation

Consent is revoked after a successful publication. Future republication stops, the local destination removes the representation, downstream notices are recorded, and the original publication receipt remains intact.

### 11.8 Offline queue

A lightweight endpoint queues a request while the hub is unreachable. Before reconnection, the source version changes. Revalidation blocks the queued request and requires a new publication request.

### 11.9 External AI candidate

An approved external service produces a summary. The source component reviews and accepts a corrected bounded version. Publication Gateway publishes only the accepted representation, not the raw provider response.

### 11.10 Public evidence

A public evidence record shows that a publication was authorized, delivered, and later withdrawn. Source content, private reviewers, consent details, and restricted cultural evidence remain available only through selective audit.
