<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONST-012",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "constitution",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/system.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json"
  ],
  "decision_ids": [
    "DEC-CULT-001",
    "DEC-CULT-002",
    "DEC-CULT-003",
    "DEC-CULT-004",
    "DEC-CULT-005",
    "DEC-DATA-001",
    "DEC-GATE-001",
    "DEC-GOV-001"
  ],
  "requirement_ids": [
    "REQ-CULT-001",
    "REQ-CULT-002",
    "REQ-CULT-003",
    "REQ-CULT-004",
    "REQ-CULT-005",
    "REQ-CULT-006",
    "REQ-CULT-007",
    "REQ-CULT-008",
    "REQ-CULT-009",
    "REQ-CULT-010",
    "REQ-CULT-011",
    "REQ-CULT-012",
    "REQ-CULT-013",
    "REQ-CULT-014",
    "REQ-CULT-015",
    "REQ-CULT-016",
    "REQ-CULT-017",
    "REQ-CULT-018",
    "REQ-CULT-019",
    "REQ-CULT-020",
    "REQ-CULT-021",
    "REQ-CULT-022",
    "REQ-CULT-023",
    "REQ-CULT-024"
  ],
  "lock_ids": [
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
    "LOCK-DATA-001",
    "LOCK-GATE-001",
    "LOCK-GOV-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-CONST-000"
  ],
  "tags": [
    "constitution",
    "cultural-rights",
    "consent",
    "provenance",
    "disclosure",
    "publication",
    "selective-audit",
    "recourse"
  ]
}
KOA:DOC-META:END -->

# Cultural Rights and Consent

## 1. Purpose

This document defines the constitutional protections that apply when kOA stores, transforms, presents, transfers, publishes, audits, or exports material associated with personal, family, community, linguistic, artistic, historical, ceremonial, territorial, or other cultural meaning.

Its purpose is to ensure that technical possession does not silently become cultural authority, that access does not silently become permission to disclose, and that one approved use does not silently authorize every later use.

The document establishes a global baseline for:

- explicit and purpose-bound consent;
- recognition of individual and collective authority;
- provenance, attribution, and contextual integrity;
- restrictions on disclosure, publication, transformation, and external transfer;
- revocation, refusal, recourse, correction, and contested authority;
- selective audit and private proof;
- safe degradation when consent or authority cannot be verified;
- separation between ingestion, storage, access, publication, and external processing.

This document does not determine statutory ownership, copyright, privacy, Indigenous rights, moral rights, contract rights, or other legal rights for a jurisdiction. Those matters remain subject to applicable law and competent human authority. The constitutional baseline defined here is an architectural protection and does not reduce any stronger legal, contractual, community, or ethical obligation.

## 2. Scope

### 2.1 Global applicability

This document applies globally to active kOA components, profiles, overlays, artifact classes, integrations, user interfaces, administrative workflows, publication paths, exports, backups, migration tools, evidence systems, and generated contexts whenever culturally meaningful material or related authority metadata is handled.

It applies to:

- content created by a user;
- content received from another person or community;
- content describing or representing a person, group, language, tradition, place, ceremony, history, identity, or cultural practice;
- voice, image, likeness, name, narrative, translation, transcription, annotation, metadata, and derived material;
- collective, family, institutional, community, or delegated authority;
- public, private, restricted, sacred, ceremonial, confidential, or context-sensitive material;
- local processing and approved external processing;
- publication to another domain or audience;
- training, enrichment, classification, indexing, summarization, translation, synthesis, and derivative generation where such operations are authorized;
- evidence proving that an operation was authorized without exposing the protected material itself.

### 2.2 Protected authority dimensions

The system recognizes that authority can be divided across several dimensions:

| Dimension | Meaning |
| --- | --- |
| Custody | Who physically or logically stores the material. |
| Authorship | Who created or expressed the material. |
| Subject authority | Who is represented, described, recorded, or affected. |
| Cultural authority | Who is recognized as able to authorize culturally governed use. |
| Administrative authority | Who operates the system or account. |
| Legal authority | Who has rights under applicable law or agreement. |
| Publication authority | Who may authorize release to a defined audience. |
| Transformation authority | Who may authorize translation, editing, derivation, synthesis, or other modification. |
| Delegated authority | Who acts under a documented mandate from another authority holder. |

These dimensions may belong to different parties. Control of an account, device, database, workspace, or encryption key does not by itself establish every authority dimension.

### 2.3 Consent-covered operations

Consent and authority evaluation apply separately to at least these operation classes:

- collection;
- ingestion;
- storage;
- local access;
- internal sharing;
- cross-component transfer;
- cross-domain disclosure;
- external-service transfer;
- publication;
- republication;
- translation;
- transcription;
- annotation;
- indexing;
- classification;
- summarization;
- adaptation;
- derivative creation;
- voice or likeness synthesis;
- commercial use;
- research use;
- training or model improvement;
- retention;
- archival preservation;
- backup;
- restoration;
- export;
- deletion;
- public evidence creation.

Permission for one operation class does not automatically authorize another.

### 2.4 Explicit non-goals

The constitutional baseline is not intended to:

- declare one universal model of cultural authority;
- replace community-specific protocols;
- assign cultural identity by automated inference;
- decide legal ownership through software;
- treat public availability as unrestricted permission;
- treat possession, custody, or administrative access as consent;
- treat silence, inactivity, interface abandonment, or unavailable contact as approval;
- make external AI a cultural authority;
- make automated classification a substitute for human cultural judgment;
- force public disclosure as the price of audit or conformance;
- promise deletion from systems or audiences outside kOA control;
- erase legitimate historical evidence of a completed governed action;
- prevent a lawful preservation duty from being recorded and reviewed;
- convert recipes, examples, or historical practice into universal consent rules.

### 2.5 Stronger local protections

A profile, community policy, contract, artifact policy, or applicable law may impose stronger controls than this document. Stronger controls remain bounded to their declared authority and scope unless an accepted global decision promotes them.

A weaker local rule cannot override the active global protections described here.

## 3. Canonical References

| Canonical reference | Responsibility in this document |
| --- | --- |
| `contracts/system.contract.json` | Owns the global authority boundaries, disclosure model, data ownership model, external integration boundaries, safe-degradation behavior, and relevant component roles. |
| `generated/requirements-index.json` | Owns the normative requirement statements rendered in Section 5. |
| `generated/assertion-index.json` | Owns the cross-file assertions that keep consent, authority, publication, provenance, audit, and data boundaries aligned. |

The accepted decisions listed in the metadata are owned by `generated/decision-index.json`. This document explains their constitutional effect without becoming a competing owner of their lifecycle or status.

Detailed data structures are expected to be owned by the appropriate artifact contracts, including the cultural-rights policy contract, publication request and receipt contracts, provenance receipt contract, integration manifest contract, and evidence contracts.

## 4. Model and Responsibilities

### 4.1 Rights and authority model

A cultural-rights record associates protected material with the authority claims, consent grants, restrictions, provenance, permitted purposes, audiences, operation classes, review conditions, expiration conditions, and recourse paths that govern its use.

The record does not establish truth merely because it exists. It is an explicit claim that remains subject to verification, challenge, correction, supersession, and conflict handling.

The model distinguishes:

- who submitted the material;
- who controls storage;
- who created the material;
- who or what is represented;
- who claims cultural authority;
- who granted consent;
- who reviewed the authority claim;
- who may receive the material;
- what operations are permitted;
- for what purpose;
- for what duration;
- under what restrictions;
- what proof exists;
- how consent can be withdrawn;
- how a dispute is raised and handled.

### 4.2 Consent model

Valid consent is:

- affirmative;
- understandable;
- specific to a purpose;
- specific to an operation class;
- specific to an audience or recipient class;
- attributable to an identified authority holder or documented delegate;
- recorded with time and applicable scope;
- reviewable before execution;
- revocable for future operations where revocation is legally and technically possible;
- distinguishable from mandatory processing performed under another explicit authority.

Consent is not inferred from:

- prior publication;
- prior access;
- prior consent for a different purpose;
- possession of a copy;
- metadata visibility;
- a default-enabled control;
- bundled acceptance of unrelated operations;
- silence;
- inactivity;
- inability to contact an authority holder;
- an AI-generated recommendation;
- an administrator’s technical capability.

### 4.3 Individual and collective authority

The system accommodates individual, joint, delegated, organizational, family, and collective authority.

A material item may require more than one approval when authority is shared. The governing policy identifies whether approval is:

- individual;
- unanimous;
- threshold-based;
- role-based;
- delegated;
- community-reviewed;
- subject to an external agreement.

The platform does not invent a collective decision rule. A missing rule results in a blocked governed operation.

### 4.4 Contextual integrity

Context is part of protected meaning. A technically accurate copy can still be an unacceptable disclosure when it changes the audience, purpose, framing, sequence, attribution, language, or cultural setting.

Contextual restrictions may include:

- approved title or description;
- required attribution;
- prohibited attribution;
- approved language;
- required warning or contextual note;
- audience limitation;
- geographic limitation;
- ceremonial or seasonal limitation;
- prohibition on excerpting;
- prohibition on recombination;
- prohibition on commercial use;
- prohibition on training or model improvement;
- prohibition on synthetic voice or likeness;
- requirement for review before republication;
- requirement to preserve provenance and related material.

### 4.5 Provenance and attribution

Provenance records where the material came from, how it entered kOA, what transformations occurred, which authority records applied, and which publication or transfer decisions were made.

Attribution is represented separately from custody and technical authorship. The model supports attribution to:

- a named person;
- multiple named contributors;
- a community or collective;
- an organization;
- an anonymous or protected identity;
- a source record without public disclosure of the identity.

A privacy-preserving or culturally required attribution choice is not treated as missing provenance.

### 4.6 Disclosure and publication boundary

Publication is distinct from ingestion, storage, local use, and internal transfer.

Publication Gateway mediates governed release to another domain or external audience. It evaluates the active publication request, consent and authority records, audience, purpose, restrictions, required transformations, evidence, and applicable exceptions before release.

The UCKK Import Bridge controls retrieval and quarantine of user-selected UCKK learning packages. Local acceptance does not authorize publication or external transfer of local content.

A component that stores or processes material cannot bypass Publication Gateway by invoking an external integration directly.

### 4.7 External processing

External processing is a separate governed operation. The transfer record identifies:

- the external surface;
- the exact material or bounded excerpt;
- the purpose;
- the expected output;
- the permitted retention;
- the applicable confidentiality level;
- whether provider reuse or training is permitted;
- the return and acceptance workflow;
- the deletion or termination capability where available;
- the inability to guarantee external deletion where such guarantee is unavailable.

External output remains non-authoritative until accepted by the responsible kOA component.

### 4.8 Selective audit and private proof

Accountability does not require indiscriminate disclosure of protected content.

The evidence system may prove:

- that an authority check occurred;
- that consent was valid at execution time;
- that a named policy version applied;
- that a publication request matched its approved scope;
- that required reviewers approved;
- that a transformation remained within the authorized class;
- that a receipt was produced;
- that a later revocation was received;
- that restricted evidence exists under an access policy.

Public evidence can disclose a result, policy identity, time, scope, and verifier while keeping private content, identities, or culturally restricted details protected.

### 4.9 Revocation, withdrawal, and refusal

An authority holder may refuse a proposed operation. A refusal is a final negative decision for that request and does not require publication of a justification.

Revocation affects future governed operations and any still-reversible pending operation. It also initiates removal, access restriction, or downstream notice actions within kOA control according to the applicable contract.

Revocation does not falsify historical receipts. Historical evidence records that the earlier operation occurred under the authority valid at that time and that the authority later changed.

When material has already reached an external audience or system outside kOA control, the system records the limitation, stops further authorized transfer, issues supported downstream notices, and does not claim guaranteed erasure.

### 4.10 Disputes and recourse

A person or recognized authority holder can challenge:

- identity;
- authorship;
- attribution;
- authority;
- consent validity;
- audience;
- purpose;
- transformation;
- publication;
- retention;
- a claimed exception;
- a refusal to correct or restrict material.

A dispute places affected new operations into the applicable restricted or blocked state until competent human review resolves the conflict. Existing local access may continue only when the active policy explicitly permits it and the continued access does not expand disclosure or harm.

Recourse records the issue, parties, evidence, interim controls, reviewer, decision, remedy, and appeal path without requiring public exposure of the protected material.

### 4.11 Roles

| Role | Responsibility |
| --- | --- |
| Submitter | Provides material and declares known authority, provenance, restrictions, and uncertainties. |
| Custodian | Protects stored material and enforces access and retention controls. |
| Cultural authority holder | Grants, refuses, limits, or revokes culturally governed permission within documented authority. |
| Subject or represented person | Exercises applicable rights related to representation, identity, voice, likeness, or personal impact. |
| Delegate | Acts under a documented and bounded mandate. |
| Component owner | Ensures component behavior respects active authority and data boundaries. |
| Governance reviewer | Evaluates authority conflicts, exceptions, and high-impact operations where the active policy requires review. |
| Publication authority | Approves or rejects a defined publication request. |
| Evidence custodian | Protects proof and exposes only the evidence appropriate to each audience. |
| Appeal reviewer | Reviews a contested outcome independently where the active recourse policy requires separation. |

An AI system may assist with drafting, indexing, comparison, or validation under an approved workflow. It is not an authority holder, consent grantor, final cultural reviewer, or exception approver.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-CULT-001,REQ-CULT-002,REQ-CULT-003,REQ-CULT-004,REQ-CULT-005,REQ-CULT-006,REQ-CULT-007,REQ-CULT-008,REQ-CULT-009,REQ-CULT-010,REQ-CULT-011,REQ-CULT-012,REQ-CULT-013,REQ-CULT-014,REQ-CULT-015,REQ-CULT-016,REQ-CULT-017,REQ-CULT-018,REQ-CULT-019,REQ-CULT-020,REQ-CULT-021,REQ-CULT-022,REQ-CULT-023,REQ-CULT-024 -->
- **REQ-CULT-001 — SHALL:** kOA distinguish technical custody, authorship, subject authority, cultural authority, administrative authority, legal authority, publication authority, transformation authority, and delegated authority.
- **REQ-CULT-002 — SHALL NOT:** Possession, custody, account control, system administration, public availability, silence, inactivity, or prior access be treated as consent.
- **REQ-CULT-003 — SHALL:** Consent identify the authority holder or documented delegate, purpose, operation class, audience or recipient class, scope, time, and applicable restrictions.
- **REQ-CULT-004 — SHALL:** Consent for collection, storage, access, transfer, external processing, publication, transformation, training, commercial use, retention, and archival preservation be evaluated as distinct permissions.
- **REQ-CULT-005 — SHALL NOT:** Consent for one purpose, audience, operation, component, profile, or artifact authorize a different purpose, audience, operation, component, profile, or artifact.
- **REQ-CULT-006 — SHALL:** A culturally governed operation fail closed when applicable authority, consent, decision rule, scope, or evidence cannot be resolved.
- **REQ-CULT-007 — SHALL:** Collective or shared authority use an explicit decision rule and identified participants or roles.
- **REQ-CULT-008 — SHALL NOT:** kOA infer cultural identity, community membership, collective authority, or consent from content analysis, language, location, metadata, or model output.
- **REQ-CULT-009 — SHALL:** Provenance record source, authority basis, transformations, transfers, publication decisions, and applicable restrictions without requiring public disclosure of protected identities.
- **REQ-CULT-010 — SHALL:** Required attribution, anonymity, contextual notes, language restrictions, audience restrictions, and transformation restrictions remain attached to governed material and its authorized derivatives.
- **REQ-CULT-011 — SHALL:** Publication be authorized independently from ingestion, storage, local access, internal processing, and backup.
- **REQ-CULT-012 — SHALL:** Publication Gateway mediate governed cross-domain disclosure and external publication.
- **REQ-CULT-013 — SHALL NOT:** UCKK Import Bridge, UCKK Publication Bridge, a component runtime, a recipe, or another external integration substitute for Publication Gateway authorization of outbound disclosure.
- **REQ-CULT-014 — SHALL:** External processing disclose the external surface, transferred material, purpose, expected output, retention conditions, provider-reuse conditions, and acceptance workflow before transfer.
- **REQ-CULT-015 — SHALL NOT:** An external service, AI system, automated classifier, translator, summarizer, or generator become a cultural authority, consent grantor, final reviewer, or canonical data owner.
- **REQ-CULT-016 — SHALL:** Selective audit permit proof of authorization, scope, execution, review, and policy application without indiscriminate disclosure of protected material or identities.
- **REQ-CULT-017 — SHALL:** Refusal block the requested operation without requiring the authority holder to publish a justification.
- **REQ-CULT-018 — SHALL:** Revocation stop future authorized operations and any reversible pending operation within its scope.
- **REQ-CULT-019 — SHALL:** Revocation preserve truthful historical evidence while recording the changed authority state and supported downstream remediation.
- **REQ-CULT-020 — SHALL NOT:** kOA claim guaranteed deletion from an external system or audience that is outside kOA control.
- **REQ-CULT-021 — SHALL:** A contested authority, consent, attribution, transformation, or publication decision enter a restricted or blocked state until competent human review resolves it.
- **REQ-CULT-022 — SHALL:** Recourse provide a recorded challenge, interim protection, human review, remedy, and applicable appeal path.
- **REQ-CULT-023 — SHALL:** Stronger applicable legal, contractual, community, profile, or artifact protections remain enforceable within their declared scope.
- **REQ-CULT-024 — SHALL NOT:** An exception, migration record, generated context, implementation example, or current technical capability silently weaken cultural-rights or consent protections.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Authority and consent establishment

The establishment workflow is:

1. Identify the material and its canonical owning component.
2. Record the submitter and source provenance.
3. Identify known authors, subjects, authority holders, delegates, and communities.
4. Record uncertainty rather than assigning an inferred authority.
5. Identify the proposed operation classes, purposes, audiences, recipients, duration, and transformations.
6. Identify applicable law, contract, community protocol, profile policy, artifact policy, and component policy.
7. Resolve the required decision rule for individual, shared, delegated, or collective authority.
8. Present the proposed use in understandable form.
9. Record affirmative grants, refusals, restrictions, expiration, review requirements, and evidence.
10. Bind the resulting authority record to the governed material.
11. Validate the authority record before the first governed operation.
12. Keep the operation blocked when validation does not pass.

### 6.2 Governed operation evaluation

Before a governed operation executes:

1. Resolve the exact material and derivative chain.
2. Resolve the active authority and consent records.
3. Resolve the requested purpose, operation class, audience, recipient, external surface, and duration.
4. Check restrictions and contextual requirements.
5. Check whether authority is individual, shared, delegated, or collective.
6. Check for disputes, revocations, suspensions, expiration, or supersession.
7. Check required human review and evidence.
8. Check applicable exceptions without allowing scope expansion.
9. Produce a decision result.
10. Execute only the authorized operation.
11. Produce a receipt or evidence record where the operation is critical.
12. Preserve failure information without exposing protected content unnecessarily.

### 6.3 Publication workflow

The publication workflow is:

1. Create a publication request for exact material or a bounded derivative.
2. Declare the audience, purpose, channel, duration, attribution, contextual framing, and permitted redistribution.
3. Resolve authority and consent for publication as a distinct operation.
4. Resolve authority for every required transformation.
5. Apply required minimization, redaction, pseudonymization, contextual notes, or access controls.
6. Validate Publication Gateway policy.
7. Obtain required human approval.
8. Produce a publication decision and receipt.
9. Release only the approved representation.
10. Record the public or private evidence appropriate to the audience.
11. Monitor expiration, revocation, dispute, and downstream obligations.

### 6.4 External-processing workflow

The external-processing workflow is:

1. Identify the approved external integration.
2. Minimize the material to the smallest sufficient input.
3. disclose the provider, purpose, transfer, retention, reuse, and return conditions to the authorizing party;
4. Resolve permission for external processing separately from local processing.
5. Resolve permission for provider training or reuse; absence of permission is represented as prohibition.
6. Execute through the approved integration boundary.
7. Record the transfer and provider response.
8. Treat the response as non-authoritative candidate material.
9. Require component-level acceptance before authoritative use.
10. Apply retention, deletion-request, and downstream-notice actions supported by the integration contract.

### 6.5 Revocation workflow

When a valid revocation is received:

1. Authenticate the requesting authority or delegate.
2. Resolve the revocation scope.
3. Stop new governed operations in that scope.
4. Cancel reversible pending operations.
5. Restrict or remove access within kOA control as required.
6. Identify derivatives, publications, exports, integrations, caches, and backups affected by the revocation.
7. Initiate supported remediation and downstream notices.
8. Record systems and audiences outside kOA control.
9. Preserve historical receipts without presenting old consent as current.
10. Update generated contexts, access decisions, and conformance evidence.
11. Provide the requesting party with the recorded outcome and remaining limitations.

### 6.6 Dispute and recourse workflow

The dispute workflow is:

1. Record the challenge without requiring public disclosure.
2. Identify affected material, decisions, authority records, and pending operations.
3. Apply interim restrictions proportionate to the alleged harm and authority uncertainty.
4. Preserve evidence.
5. Assign a competent human reviewer.
6. Notify affected parties where allowed and appropriate.
7. Evaluate identity, mandate, provenance, consent, context, restrictions, transformations, and publication history.
8. Record the decision and rationale.
9. Apply correction, restriction, withdrawal, attribution change, access change, republication, downstream notice, or other supported remedy.
10. Provide the applicable appeal path.
11. Keep unresolved high-impact operations blocked.

### 6.7 Consent state model

The conceptual state progression is:

`text
unrecorded
 -> proposed
 -> granted | refused
 -> active
 -> suspended
 -> revoked | expired | superseded
`

A dispute may move an affected grant into `suspended`. A replacement grant uses a new version and preserves lineage. Refused, revoked, expired, suspended, or superseded authority does not authorize a new governed operation.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Preserved capability | Denied capability | Evidence |
| --- | --- | --- | --- | --- |
| Authority holder cannot be identified | Record uncertainty and block governed disclosure or transformation. | Protected local custody and permitted private access | New governed operation | Authority-resolution result |
| Collective decision rule is missing | Block the request and request competent human resolution. | Existing authorized state | New collective authorization | Decision-closure evidence |
| Consent record is missing or invalid | Fail closed for the affected operation. | Unrelated local capabilities | Requested operation | Consent-validation result |
| Consent scope does not match the request | Deny the unmatched purpose, audience, recipient, or operation. | Operations already covered by active consent | Scope expansion | Policy-decision receipt |
| Consent expires | Stop new operations after expiration and update active contexts. | Historical evidence and independently authorized access | New expired-scope operation | Expiration event |
| Consent is revoked | Stop future and reversible pending operations; begin supported remediation. | Truthful historical receipts | Further revoked-scope use | Revocation receipt |
| Authority is disputed | Restrict or block affected operations pending human review. | Evidence preservation and safe local custody | New high-impact operation | Dispute record |
| Publication Gateway is unavailable | Queue or deny publication without routing around the gateway. | Local storage and permitted local use | External publication | Gateway health and denial record |
| Governance Policy Runtime is unavailable in a profile that requires it | Block governed authorization decisions. | Previously authorized local read-only use where policy permits | New disclosure or privilege decision | Runtime status |
| External service is unavailable | Disable the external operation only. | Local deterministic operation | External processing | Integration health record |
| External service cannot provide required retention or reuse controls | Deny transfer to that service. | Local processing and alternate authorized paths | Non-conforming external transfer | Integration-policy result |
| Protected evidence cannot be disclosed publicly | Provide an authorized public summary or private verification path. | Accountability and private proof | Indiscriminate disclosure | Evidence-access record |
| Downstream deletion cannot be guaranteed | Stop further transfer, issue supported notices, and record the limitation. | Local remediation and accurate evidence | False deletion claim | Remediation record |
| Attribution conflict exists | Suspend new publication or transformation involving disputed attribution. | Evidence preservation and restricted review | New disputed publication | Dispute outcome |
| Contextual restriction cannot be preserved | Deny the operation rather than publish a decontextualized result. | Original protected material | Context-breaking derivative or release | Validation result |
| Cultural-rights policy is incompatible with the artifact or profile | Block activation or publication until compatible authority exists. | Previously active compatible state | Candidate activation | Compatibility evidence |

Safe degradation narrows access or disables the affected operation. It does not invent consent, substitute an administrator for an authority holder, route around Publication Gateway, publish a less protected representation, or expose private evidence as a convenience fallback.

## 8. Cross-Component Interactions

### 8.1 Owning component

The component that owns the authoritative material remains responsible for:

- binding the applicable cultural-rights record;
- enforcing local access and transformation decisions;
- preserving provenance;
- rejecting direct mutation by another component;
- identifying the exact material submitted to a gateway or integration;
- accepting or rejecting returned candidate outputs.

The owning component does not gain publication authority merely because it owns the data.

### 8.2 Governance Policy Runtime

Where deployed, Governance Policy Runtime evaluates active authorization, disclosure, consent, privilege, and exception policy. It returns a governed decision and applicable obligations.

It does not own the material, assign cultural identity, decide semantic truth, allocate resources, or become the authority holder.

### 8.3 Publication Gateway

Publication Gateway receives a bounded publication request, resolves the applicable decision and evidence, applies release obligations, and produces a publication receipt.

It does not ingest user media into UCKK, own the source material, or silently broaden the approved audience.

### 8.4 UCKK Import Bridge

UCKK Import Bridge receives selected UCKK learning packages for quarantine and controlled local acceptance. It preserves source provenance, license, restrictions, consent references, and applicable cultural-rights conditions.

It does not authorize publication, external processing, training, commercial use, or unrelated transformation.

### 8.5 External integrations

An integration receives only the minimized input authorized for its declared capability. The integration manifest identifies data movement, provider behavior, retention, reuse, deletion support, failure behavior, and removal behavior.

Removing an optional integration leaves unrelated local capabilities operational.

### 8.6 Evidence and audit systems

Evidence systems store or reference the smallest proof sufficient for validation and recourse. Access to private evidence follows explicit policy.

Audit systems do not receive unrestricted content merely because they record that a governed operation occurred.

### 8.7 Backup, restore, and migration

Backups and migration packages preserve cultural-rights records, provenance, restrictions, revocations, disputes, and lineage with the protected material.

Restoration does not reactivate expired, revoked, suspended, or superseded consent. Migration does not promote historical permission into current authority.

### 8.8 Generated AI contexts

Generated AI contexts include only the authority required for their declared scope. They can identify restrictions and required workflows but do not become authority holders or permission grants.

A context omission does not prove that unrestricted use is allowed.

## 9. Decision Closure and Prohibited Assumptions

The decisions listed in the metadata close the constitutional model used by this document.

The following assumptions are prohibited:

1. The uploader owns every right associated with the uploaded material.
2. Account ownership establishes cultural authority.
3. Publicly accessible material is free of cultural or consent restrictions.
4. A person can authorize every use of material associated with a community.
5. A community name identifies a valid collective decision rule.
6. Silence or failure to respond is approval.
7. Consent for storage includes consent for publication.
8. Consent for translation includes consent for synthetic voice or derivative generation.
9. Consent for one external provider includes consent for another provider.
10. Consent for a private audience includes consent for a public audience.
11. Prior publication permanently removes the possibility of later restriction.
12. Revocation can erase truthful historical evidence.
13. A deletion request guarantees removal from systems outside kOA control.
14. An administrator may bypass consent because the administrator can access the data.
15. An AI output can identify cultural authority or community membership conclusively.
16. Automated translation preserves contextual meaning without review.
17. Attribution is unnecessary when provenance exists privately.
18. Publication Gateway, UCKK Publication Bridge, and UCKK Import Bridge are interchangeable.
19. A component may publish directly because it owns the source data.
20. Audit requires full disclosure of protected material.
21. A private evidence record may be made public to simplify conformance.
22. An exception silently changes the global cultural-rights baseline.
23. A migration record reactivates historical consent.
24. Absence of a restriction means unrestricted permission.
25. A generated AI context contains every relevant cultural rule beyond its declared scope.

When the requested action depends on a missing authority rule, unresolved conflict, absent consent, unavailable evidence, or undefined collective decision procedure, the action remains blocked until active authority resolves it.

## 10. Validation Criteria

This document is conformant when all of the following checks pass:

1. The file is registered as `DOC-CONST-012` at `01-constitution/12-cultural-rights-and-consent.md`.
2. The document class is `normative_markdown`, status is `active`, language is `en`, layer is `constitution`, and scope is `global`.
3. The metadata matches `generated/document-index.json`.
4. Every canonical reference resolves.
5. Every listed decision exists with accepted status before this document participates in active authority.
6. Every listed requirement exists with the exact rendered text, strength, scope, owner, source decision, lock mapping, and validation method.
7. Every listed lock exists and its applicable assertions pass.
8. The document contains all eleven mandatory sections in the required order.
9. Normative keywords appear only inside the generated requirements block.
10. No file-content hash is required for this Markdown document.
11. Custody, authorship, subject authority, cultural authority, administrative authority, legal authority, publication authority, transformation authority, and delegated authority remain distinguishable.
12. Consent records identify purpose, operation class, audience or recipient, scope, time, authority, and restrictions.
13. Consent is not inferred from possession, public availability, silence, prior access, defaults, model output, or administrator capability.
14. Collective authority depends on an explicit decision rule.
15. Cultural identity and authority are not assigned through automated inference.
16. Publication remains separate from ingestion, storage, backup, and local processing.
17. Publication Gateway cannot be bypassed by a component, UCKK Publication Bridge, UCKK Import Bridge, recipe, or external integration when outbound disclosure is requested.
18. External processing is separately authorized and fully disclosed before transfer.
19. External outputs remain non-authoritative until accepted by the responsible component.
20. Selective audit can prove authorization without exposing protected content indiscriminately.
21. Revocation stops future and reversible pending operations without falsifying historical evidence.
22. The system does not claim guaranteed deletion outside its control.
23. Disputed high-impact operations remain restricted or blocked pending competent human review.
24. Recourse includes interim protection, review, remedy, and an applicable appeal path.
25. Stronger applicable protections are not weakened.
26. Migration, restore, generated context, example, recipe, or exception processing cannot silently reactivate or broaden permission.
27. No unresolved marker, provisional value, implicit default, or parallel authority appears.
28. Complete documentation validation returns `pass` before authority activation.

## 11. Non-Normative Examples

### 11.1 Storage without publication authority

A user uploads a community recording to a private UCKK dimension for preservation. The user has authority to store the recording but does not have authority to publish it. UCKK accepts the material with its provenance and restrictions. A later public-release request remains blocked until the required community authority is recorded.

### 11.2 Purpose-bound translation

An authority holder permits translation into French for private educational review by a named group. The grant does not authorize public publication, commercial use, synthetic narration, model training, or translation into additional languages.

### 11.3 Selective public evidence

A public conformance report states that a publication was authorized under policy version `1.0.0`, reviewed by the required roles, and released to a defined audience. The protected source material, private identities, and restricted cultural details remain accessible only through the approved private-proof path.

### 11.4 Collective decision rule

A community policy identifies three recognized roles and requires two approvals, including one designated cultural reviewer, before ceremonial material can be published. The platform evaluates that rule exactly. It does not replace it with a simple majority or the approval of the uploader.

### 11.5 Revocation after external publication

An authority holder revokes future republication after material was already released to an external audience. kOA stops new release operations, removes controlled copies where required, issues supported downstream notices, records audiences outside its control, and preserves the original publication and revocation receipts.

### 11.6 Contested attribution

Two parties dispute attribution for an artifact scheduled for publication. The source material remains preserved, but the publication is suspended. A human review records evidence, decides the attribution treatment, applies the remedy, and provides the applicable appeal path.

### 11.7 External AI processing

A user requests an external translation service for a bounded excerpt. The interface identifies the provider, data transferred, purpose, retention conditions, and reuse conditions. The authority holder grants that exact transfer. The returned translation remains candidate material until reviewed and accepted.

### 11.8 Incorrect administrative override

An administrator can technically export a restricted collection. Technical capability does not create publication authority. The export remains denied when the required consent and publication decision are absent.

### 11.9 Contextual integrity

A photograph is permitted in a complete educational exhibit with a required caption and community context. Cropping the image and using it in unrelated advertising is a different operation and requires separate authority.

### 11.10 Safe failure

The consent service is unavailable during a publication request. Publication remains blocked. Local protected storage and previously authorized private access continue where the active policy permits them.
