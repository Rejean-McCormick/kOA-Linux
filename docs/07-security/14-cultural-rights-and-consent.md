<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SEC-014",
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
    "contracts/system.contract.json#/data_authority",
    "contracts/system.contract.json#/ai_boundary",
    "generated/component-catalog.json",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/components/publication-gateway.component.json",
    "contracts/components/identity-and-trust.component.json",
    "contracts/components/audit-broker.component.json",
    "contracts/artifact-contracts/cultural-rights-policy.schema.json",
    "contracts/artifact-contracts/policy-bundle.schema.json",
    "contracts/artifact-contracts/decision-receipt.schema.json",
    "generated/profile-catalog.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-COMP-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-GATE-001",
    "DEC-AI-001",
    "DEC-SENT-001",
    "DEC-REL-001",
    "DEC-PROFILE-BASELINE-001"
  ],
  "requirement_ids": [
    "REQ-SEC-CULT-001",
    "REQ-SEC-CULT-002",
    "REQ-SEC-CULT-003",
    "REQ-SEC-CULT-004",
    "REQ-SEC-CULT-005",
    "REQ-SEC-CULT-006",
    "REQ-SEC-CULT-007",
    "REQ-SEC-CULT-008",
    "REQ-SEC-CULT-009",
    "REQ-SEC-CULT-010",
    "REQ-SEC-CULT-011",
    "REQ-SEC-CULT-012",
    "REQ-SEC-CULT-013",
    "REQ-SEC-CULT-014",
    "REQ-SEC-CULT-015",
    "REQ-SEC-CULT-016",
    "REQ-SEC-CULT-017",
    "REQ-SEC-CULT-018",
    "REQ-SEC-CULT-019",
    "REQ-SEC-CULT-020",
    "REQ-SEC-CULT-021",
    "REQ-SEC-CULT-022",
    "REQ-SEC-CULT-023",
    "REQ-SEC-CULT-024",
    "REQ-SEC-CULT-025",
    "REQ-SEC-CULT-026",
    "REQ-SEC-CULT-027",
    "REQ-SEC-CULT-028",
    "REQ-SEC-CULT-029",
    "REQ-SEC-CULT-030",
    "REQ-SEC-CULT-031",
    "REQ-SEC-CULT-032"
  ],
  "lock_ids": [
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SENT-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CON-006",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-006",
    "DOC-SYS-007",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-017",
    "DOC-SYS-018",
    "DOC-SYS-019",
    "DOC-PRO-000",
    "DOC-LIFE-001",
    "DOC-LIFE-007",
    "DOC-LIFE-011",
    "DOC-SEC-003"
  ],
  "tags": [
    "cultural-rights",
    "consent",
    "community-authority",
    "indigenous-authority",
    "access",
    "reuse",
    "withdrawal",
    "dissent",
    "recourse",
    "ai-boundary",
    "publication",
    "private-proof"
  ]
}
KOA:DOC-META:END -->

# Cultural Rights and Consent

## 1. Purpose

This document defines the global security model for cultural rights, community authority, consent, restricted use, distribution, withdrawal, dissent, review, and recourse in kOA.

Cultural sovereignty is not achieved by storage locality alone. A system can keep data on a sovereign node and still violate cultural authority through inappropriate discovery, interpretation, reuse, export, publication, AI processing, or retention.

The model therefore treats cultural rights as enforceable policy attached to identifiable subjects and evaluated at every relevant action boundary.

It preserves the distinction between:

- subject data ownership and cultural authority;
- creator rights and community authority;
- stewardship and ownership;
- identity verification and cultural approval;
- consent and technical accessibility;
- access and reuse;
- discovery and disclosure;
- source content and derivatives;
- publication intent and completed publication;
- policy decisions and machine privilege;
- public receipts and private evidence;
- withdrawal and historical erasure;
- automated suggestions and authoritative decisions.

The canonical machine-readable contract is:

```text
contracts/artifact-contracts/cultural-rights-policy.schema.json
```

A policy that conforms to that schema can be packaged as a module of a governance policy bundle, as a standalone signed policy, or as an embedded object policy where the owning component contract permits it.

The policy remains a governance artifact. It does not transfer the source component's data ownership.

## 2. Scope

This document applies to protected subjects of these schema-defined types:

<!-- GENERATED:SUBJECT-TYPES:BEGIN source=contracts/artifact-contracts/cultural-rights-policy.schema.json#/$defs/subject/properties/subject_type -->
`object`, `collection`, `record`, `artifact`, `media`, `knowledge`, `cultural_expression`, `dataset`, `metadata`, `derived_representation`
<!-- GENERATED:SUBJECT-TYPES:END -->

It applies to subjects held or referenced by:

- Konnaxion;
- Kristal Runtime and Kristal source workflows;
- kOA Mediatheque and the external UCKK publication integration;
- Orgo workflows that carry protected references;
- Ariane presentation and navigation;
- language and knowledge artifacts;
- publication and synchronization boundaries;
- backup, restore, preservation, and credible-exit processes;
- developer, test, sovereign, hub, control-plane, and offline profiles;
- approved external integrations.

It applies to these data classifications:

<!-- GENERATED:DATA-CLASSIFICATIONS:BEGIN source=contracts/artifact-contracts/cultural-rights-policy.schema.json#/$defs/subject/properties/data_classification -->
`public`, `community`, `restricted`, `confidential`, `sealed`, `sacred_or_ceremonial`
<!-- GENERATED:DATA-CLASSIFICATIONS:END -->

It governs:

- authority identification;
- community protocols;
- cultural context;
- interpretation restrictions;
- discovery;
- access;
- display;
- download;
- reuse;
- adaptation;
- translation;
- research;
- commercial use;
- preservation copying;
- attribution;
- consent;
- AI restrictions;
- audience-scoped distribution;
- publication;
- synchronization;
- backup;
- export;
- withdrawal;
- purge;
- dissent;
- dispute resolution;
- review;
- appeal;
- receipts;
- private proof;
- offline behavior.

It does not define one universal cultural protocol or replace community, Indigenous, collective, creator, legal, institutional, or jurisdictional authority.

It does not make kOA the source of cultural authority. kOA records and enforces the authority and rules declared through accepted governance processes.

## 3. Canonical References

| Canonical reference | Responsibility |
| --- | --- |
| `contracts/artifact-contracts/cultural-rights-policy.schema.json` | Policy structure, subject and authority types, access, reuse, consent, action decisions, AI rules, distribution, withdrawal, dissent, review, enforcement, provenance, governance, receipts, and validation. |
| `contracts/artifact-contracts/policy-bundle.schema.json` | Packaging, signing, approval, activation, rollback, and compatibility of governance policy modules. |
| `contracts/artifact-contracts/decision-receipt.schema.json` | Bounded public decision receipts and protected evidence references. |
| `contracts/components/governance-policy-runtime.component.json` | Evaluation of cultural-rights, consent, disclosure, obligation, and exception decisions. |
| `contracts/components/publication-gateway.component.json` | Governed cross-domain disclosure and publication. |
| `contracts/components/identity-and-trust.component.json` | Verification of actors, cultural authorities, delegates, recipients, and relying context. |
| `contracts/components/audit-broker.component.json` | Selective routing of public audit events and private evidence references. |
| `generated/component-catalog.json` | Logical ownership of protected subject records and component boundaries. |
| `generated/profile-catalog.json` | Profile-specific policy-runtime availability, offline behavior, encryption, storage, trust, evidence, and recovery. |
| `contracts/integration-types.contract.json` | External AI, publication, federation, research, identity, preservation, and transfer integrations. |
| `generated/test-catalog.json` | Authority, consent, access, AI, distribution, withdrawal, dissent, recourse, offline, and attack-resistance tests. |
| `generated/evidence-catalog.json` | Approval, decision, access, publication, withdrawal, purge, dispute, review, and conformance evidence. |
| `generated/requirements-index.json` | Normative statements displayed in Section 5. |
| `generated/assertion-index.json` | Component, data, governance, publication, AI, profile, and lifecycle invariants. |
| `generated/traceability.json` | Links among policies, authorities, subjects, decisions, requirements, tests, evidence, components, and profiles. |
| `generated/exception-index.json` | Approved bounded deviations and compensating controls. |

The policy schema owns the field structure. This document explains how the fields operate together.

## 4. Model and Responsibilities

### 4.1 Protected subject

A protected subject is a specific object, collection, record, artifact, media item, knowledge object, cultural expression, dataset, metadata set, or derived representation governed by a cultural-rights policy.

Every subject records:

- stable subject identity;
- subject type;
- owning component;
- community references;
- creator authority references;
- rights-holder authority references;
- steward authority references;
- data classification;
- source provenance;
- optional canonical reference and title.

The owning component remains the logical writer of the subject record.

A cultural-rights policy constrains actions involving that subject. It does not move the record into a universal policy database or permit the policy runtime to write the subject directly.

### 4.2 Cultural authority

The schema recognizes these authority types:

<!-- GENERATED:AUTHORITY-TYPES:BEGIN source=contracts/artifact-contracts/cultural-rights-policy.schema.json#/$defs/authority/properties/authority_type -->
`creator`, `rights_holder`, `community`, `collective`, `indigenous_authority`, `steward`, `custodian`, `institution`, `legal_guardian`, `delegate`, `multi_party_body`
<!-- GENERATED:AUTHORITY-TYPES:END -->

An authority record identifies:

- authority identity;
- name;
- authority type;
- roles;
- decision-right model;
- scope;
- communities;
- delegation;
- effective interval;
- contact;
- evidence.

Decision-right models can be individual, joint, quorum, consultative, veto, delegated, or notice-only.

A technical operator can also be a cultural authority only when a separate authority record and accepted evidence establish that role.

### 4.3 Roles and decision rights

Cultural roles can include:

- approval of access;
- approval of reuse;
- approval of external AI access;
- approval of export;
- approval of publication;
- approval of preservation;
- request for withdrawal;
- dispute resolution;
- receipt of notice;
- delegation;
- stewardship;
- access to private evidence.

The role required by an action is part of the action decision.

The system does not infer approval power from a general title such as administrator, curator, owner, maintainer, or publisher.

### 4.4 Communities and jurisdiction

A policy identifies each community by:

- stable community identity;
- self-chosen name and description where available;
- authority references;
- language tags;
- jurisdiction references;
- evidence.

Jurisdictional basis can include:

- community protocol;
- customary law;
- statutory law;
- contract;
- institutional policy;
- multiple sources.

The policy records applicable references without asserting that one basis universally overrides another.

A conflict enters the declared dispute or authority-review path.

### 4.5 Cultural context and protocol

Cultural context can classify sensitivity as ordinary, sensitive, restricted, confidential, sealed, or sacred or ceremonial.

Interpretation can be open, context-required, authority-reviewed, restricted, or prohibited.

A protocol defines:

- protocol identity;
- title;
- authority;
- description;
- trigger conditions;
- required notices;
- languages;
- jurisdiction;
- references.

Context can also declare prohibited inferences.

For example, a policy can forbid an application, researcher, or AI service from inferring sacred, ceremonial, kinship, identity, or restricted meaning from incomplete metadata.

### 4.6 Audiences

The schema recognizes these audience kinds:

<!-- GENERATED:AUDIENCE-TYPES:BEGIN source=contracts/artifact-contracts/cultural-rights-policy.schema.json#/$defs/audience/properties/kind -->
`public`, `community`, `research`, `institution`, `exhibition`, `preservation`, `private`, `custom`
<!-- GENERATED:AUDIENCE-TYPES:END -->

An audience record identifies:

- audience identity;
- kind;
- description;
- qualification;
- verifying authorities;
- encryption requirement;
- redistribution rule;
- export eligibility;
- membership evidence.

Audience qualification is evaluated for the current request.

A person who belongs to one audience does not gain access intended for another audience.

### 4.7 Access and discovery

Access policy separates:

- discovery;
- search indexing;
- metadata visibility;
- anonymous access;
- authentication strength;
- access duration;
- session export.

Discovery can expose public metadata, audience-scoped metadata, authority-only metadata, or no discoverable record.

Search indexing can be full, metadata-only, audience-scoped, or prohibited.

A hidden payload is not protected when unrestricted metadata, embeddings, thumbnails, transcripts, or search terms reveal the restricted content.

### 4.8 Reuse rights

Reuse terms independently govern:

- display;
- download;
- reproduction;
- adaptation;
- translation;
- commercial use;
- research use;
- preservation copy;
- attribution.

A right can be allowed, allowed with obligations, approval-required, consent-required, prohibited, or not applicable.

Conditions can include:

- purpose limits;
- audience limits;
- attribution;
- encryption;
- review;
- language conditions;
- retention;
- non-redistribution;
- return or destruction;
- publication restrictions.

A preservation copy can be permitted while public display remains prohibited.

A research use can be approved while commercial use remains prohibited.

### 4.9 Consent

Consent records bind:

```text
authority
subject
action
purpose
audience
scope
effective interval
withdrawal state
evidence
receipt
```

The supported consent models are individual, collective, institutional, multi-party, delegated, jurisdictional, and combined.

Consent is not portable across unrelated actions or purposes.

Consent to preserve a copy does not imply consent to publish it.

Consent to display to a community audience does not imply consent to download or train a model.

Consent to use one version does not automatically apply to a materially changed derivative.

### 4.10 Action policy matrix

The active schema requires a decision at each of these enforcement points:

<!-- GENERATED:ACTION-POLICIES:BEGIN source=contracts/artifact-contracts/cultural-rights-policy.schema.json#/$defs/actionPolicies/properties -->
| Action | Boundary |
| --- | --- |
| `ingestion` | Admission of a subject, record, artifact, media object, dataset, or knowledge item into a component domain. |
| `metadata_edit` | Creation or alteration of descriptive, contextual, authority, rights, provenance, or discovery metadata. |
| `discovery` | Exposure of existence, title, summary, indexing terms, or other discovery information. |
| `read` | Retrieval of protected source content or records. |
| `query` | Structured querying, aggregation, filtering, or interpretation of protected content or metadata. |
| `render` | Transformation into a view, preview, thumbnail, waveform, page, transcript display, or other presentation. |
| `display` | Presentation to a person, audience, exhibition, application, or device. |
| `download` | Delivery of a copy to a recipient-controlled location. |
| `reproduction` | Creation of another copy or representation beyond bounded runtime rendering. |
| `reuse` | Use in another work, collection, product, research process, or purpose. |
| `publication` | Cross-domain disclosure or release to a declared audience. |
| `synchronization` | Transfer between nodes, hubs, tenants, environments, or component instances. |
| `backup` | Creation of protected recovery material. |
| `export` | Creation of a portable representation for transfer, research, preservation, or exit. |
| `ai_access` | Transfer, mounting, querying, or processing through an external AI or advisory workbench boundary. |
| `federation` | Exposure through a federated catalog, query, identity, or content relationship. |
| `withdrawal` | Governed removal from new access, distribution, or use. |
| `purge` | Controlled deletion or cryptographic destruction where permitted. |
<!-- GENERATED:ACTION-POLICIES:END -->

Each action returns a decision such as allow, allow with obligations, deny, require consent, require authority review, or not applicable.

The result carries reason codes and obligations.

The component performing the action enforces the result and remains responsible for its state transition.

### 4.11 Obligations

An obligation can require:

- attribution;
- redaction;
- encryption;
- notification;
- watermarking;
- time limits;
- audience limits;
- no-AI handling;
- return or destruction;
- cache purge;
- logging;
- private evidence;
- review;
- another declared control.

Obligations have an enforcement point such as before action, during action, after action, continuously, on expiry, or on withdrawal.

An allow-with-obligations result is not satisfied until all required pre-action obligations pass.

Post-action obligations remain tracked through receipts and evidence.

### 4.12 External AI boundary

The schema separately governs these external-AI activities:

<!-- GENERATED:AI-ACTIONS:BEGIN source=contracts/artifact-contracts/cultural-rights-policy.schema.json#/$defs/aiPolicy/properties/actions/properties -->
| AI activity | Meaning |
| --- | --- |
| `training` | Use as model-training data. |
| `fine_tuning` | Use to alter a model through supervised or preference-based adaptation. |
| `embedding` | Creation of vector or semantic representations. |
| `indexing` | Inclusion in an AI-oriented semantic or retrieval index. |
| `inference` | Submission to a model for prediction or interpretation. |
| `classification` | Automated categorization, labeling, ranking, or routing. |
| `summarization` | Automated condensation or abstract creation. |
| `translation` | Automated language conversion. |
| `transcription` | Automated conversion of audio or video speech into text. |
| `generation` | Creation of new text, image, audio, video, code, or mixed content using the subject. |
| `semantic_enrichment` | Automated extraction or addition of entities, concepts, relationships, or interpretations. |
<!-- GENERATED:AI-ACTIONS:END -->

The baseline records:

- no native AI authority;
- external AI output as candidate-only;
- direct mounting into an AI domain as prohibited;
- unreviewed inference over sacred or restricted material as prohibited;
- provenance as required;
- human or authority review as required;
- owning-component acceptance as required.

An approved external AI integration can receive a bounded input only after the action-specific cultural-rights decision passes.

The result re-enters through the owning component's candidate-import boundary.

### 4.13 SenTient

SenTient remains optional, isolated, task-activated, and non-authoritative.

A cultural-rights decision can deny SenTient access entirely or allow a narrowly bounded research task with:

- declared subjects;
- declared purpose;
- authority;
- consent;
- input minimization;
- isolation;
- no direct source mount;
- provenance;
- review;
- deletion or return obligations;
- receipt.

SenTient cannot write an owning component's authoritative state.

### 4.14 Distribution and publication

Restricted content is distributed through audience-aware controls.

Available patterns include:

- audience-scoped artifacts;
- encrypted recipient-scoped artifacts;
- separate restricted shards;
- no-cache delivery;
- encrypted and audience-scoped caches;
- download expiry;
- watermarking where approved.

Cross-domain publication uses the Publication Gateway.

The source component remains the owner.

The gateway owns disclosure and publication execution, not cultural authority or source data.

### 4.15 Lineage and derivatives

Rights lineage follows:

- source records;
- metadata;
- thumbnails;
- previews;
- transcripts;
- translations;
- embeddings;
- indexes;
- summaries;
- runtime packs;
- exports;
- backups;
- published copies;
- synchronized copies;
- derived media.

A derivative records its source provenance and applicable policy identity.

A derivative can receive a narrower policy.

A broader policy requires accepted authority and cannot arise merely because the transformation changed format or removed obvious identifiers.

### 4.16 Withdrawal and purge

Withdrawal is a governed transition.

It can require:

- stop of new distribution;
- access denial;
- search and discovery update;
- publication withdrawal;
- controlled-cache purge;
- notification;
- derivative withdrawal;
- rebuild without the subject;
- restriction;
- review;
- minimal retained proof.

Purge is distinct from withdrawal.

Withdrawal can remove active availability while retaining minimal lawful or policy-required evidence.

Purge can delete or cryptographically destroy selected controlled copies when the policy and owning component permit it.

### 4.17 Dissent and dispute

Dissent status can be none, declared, active, or resolved.

A dissent position records:

- position identity;
- authorities;
- position text;
- evidence;
- time.

The policy defines whether active dissent causes denial, authority review, or an allow result with a dissent notice.

Resolution records the resolving authorities and receipt.

Resolution does not erase the historical positions.

### 4.18 Review, appeal, and recourse

Every policy defines:

- effective date;
- review date;
- optional expiry;
- review authorities;
- appeal location;
- complaint channels;
- reversal support;
- reviewability of automated suggestions;
- decision receipts;
- review triggers.

Review triggers can include:

- scheduled review;
- authority change;
- community request;
- dissent;
- security event;
- distribution change;
- new external AI capability;
- jurisdiction change;
- withdrawal request;
- policy supersession.

A policy can be active and still subject to appeal.

### 4.19 Enforcement boundary

The Governance Policy Runtime evaluates the cultural-rights policy when required by the active profile.

The performing component supplies:

- actor and authority context;
- subject;
- action;
- purpose;
- audience;
- consent evidence;
- current policy identity;
- profile;
- environment;
- requested obligations.

The runtime returns:

- decision;
- reason codes;
- obligations;
- validity;
- policy identity;
- evidence references;
- receipt reference.

The performing component enforces the result.

The runtime does not write the subject or perform publication, export, deletion, or AI transfer directly.

### 4.20 Governance and activation

A policy records:

- proposing authorities;
- approving authorities;
- community approval model;
- separation of duties;
- activation mode;
- rollback or forward repair;
- approval evidence;
- recourse;
- bundle reference.

Policy activation selects one verified identity atomically.

Existing decision receipts preserve the prior policy identity used at decision time.

Superseding a policy does not rewrite earlier decisions.

### 4.21 Decision behavior

The policy defines default behavior for:

- missing authority;
- missing consent;
- conflicting authority;
- active dissent;
- stale policy;
- missing evidence.

The decision includes reason codes and obligations.

A policy error does not silently fall back to public access, unrestricted reuse, universal distribution, or AI availability.

### 4.22 Receipts and private proof

Public receipts contain bounded fields such as:

- receipt identity;
- time;
- decision;
- policy identity and version;
- action;
- resource reference;
- reason codes;
- obligations;
- validity;
- correlation.

Private evidence can contain:

- authority evidence;
- consent evidence;
- community protocols;
- dissent positions;
- restricted subject details;
- identity evidence;
- approval evidence;
- withdrawal evidence.

Secret material is excluded from both ordinary public receipts and ordinary private evidence records.

### 4.23 Offline behavior

An offline profile can evaluate a locally verified policy when the required local identity, authority, consent, trust, evidence, and policy state are available.

The decision exposes:

- policy identity;
- policy freshness;
- trust freshness;
- evidence freshness;
- offline limitation;
- synchronization requirement.

Actions requiring current external authority remain blocked.

Offline continuity does not reduce cultural-rights protection.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SEC-CULT-001,REQ-SEC-CULT-002,REQ-SEC-CULT-003,REQ-SEC-CULT-004,REQ-SEC-CULT-005,REQ-SEC-CULT-006,REQ-SEC-CULT-007,REQ-SEC-CULT-008,REQ-SEC-CULT-009,REQ-SEC-CULT-010,REQ-SEC-CULT-011,REQ-SEC-CULT-012,REQ-SEC-CULT-013,REQ-SEC-CULT-014,REQ-SEC-CULT-015,REQ-SEC-CULT-016,REQ-SEC-CULT-017,REQ-SEC-CULT-018,REQ-SEC-CULT-019,REQ-SEC-CULT-020,REQ-SEC-CULT-021,REQ-SEC-CULT-022,REQ-SEC-CULT-023,REQ-SEC-CULT-024,REQ-SEC-CULT-025,REQ-SEC-CULT-026,REQ-SEC-CULT-027,REQ-SEC-CULT-028,REQ-SEC-CULT-029,REQ-SEC-CULT-030,REQ-SEC-CULT-031,REQ-SEC-CULT-032 -->
- **REQ-SEC-CULT-001 — SHALL:** Every protected subject shall identify its owning component, subject type, cultural communities, data classification, and applicable cultural-rights policy before a governed action is evaluated.
- **REQ-SEC-CULT-002 — SHALL:** Cultural authority shall be represented explicitly as creator, rights holder, community, collective, Indigenous authority, steward, custodian, institution, legal guardian, delegate, or multi-party body with declared scope and decision rights.
- **REQ-SEC-CULT-003 — SHALL NOT:** Storage custody, technical administration, metadata editing, hosting, publication execution, or component operation shall be interpreted as cultural authority or rights ownership.
- **REQ-SEC-CULT-004 — SHALL:** A delegated cultural authority shall identify the delegating authority, delegation scope, effective period, permitted roles, and delegation evidence.
- **REQ-SEC-CULT-005 — SHALL:** Cultural context shall preserve required community protocols, notices, language, jurisdictional basis, sensitivity, interpretation conditions, and prohibited inferences.
- **REQ-SEC-CULT-006 — SHALL:** Access policy shall declare audiences, qualification, authentication strength, discovery behavior, search-index behavior, metadata visibility, redistribution, export eligibility, encryption, and access duration as applicable.
- **REQ-SEC-CULT-007 — SHALL NOT:** Restricted, confidential, sealed, sacred, or ceremonial material shall be placed in a universal unencrypted artifact and hidden only through user-interface controls.
- **REQ-SEC-CULT-008 — SHALL:** Reuse policy shall independently govern display, download, reproduction, adaptation, translation, commercial use, research use, preservation copying, licensing, and attribution.
- **REQ-SEC-CULT-009 — SHALL:** Consent shall be explicit, attributable, action-specific, purpose-specific, audience-specific, scope-specific, reviewable, withdrawable, and supported by declared evidence.
- **REQ-SEC-CULT-010 — SHALL NOT:** Silence, absence of a denial, prior unrelated consent, technical accessibility, public discoverability, or possession of a copy shall be interpreted as consent.
- **REQ-SEC-CULT-011 — SHALL:** Missing authority, missing required evidence, and missing consent shall produce denial or an explicit authority-review state according to the active policy.
- **REQ-SEC-CULT-012 — SHALL:** Conflicting authority or consent records shall preserve the conflict and follow the declared denial or authority-review behavior without selecting a winner implicitly.
- **REQ-SEC-CULT-013 — SHALL:** The active cultural-rights policy shall be evaluated at ingestion, metadata editing, discovery, read, query, rendering, display, download, reproduction, reuse, publication, synchronization, backup, export, AI access, federation, withdrawal, and purge boundaries.
- **REQ-SEC-CULT-014 — SHALL:** Each action decision shall identify allowed audiences, required authority roles, consent requirements, purpose limits, obligations, reason codes, offline behavior, and review timing as applicable.
- **REQ-SEC-CULT-015 — SHALL:** Obligations such as attribution, redaction, encryption, notice, watermarking, time limits, audience limits, no-AI handling, return or destruction, cache purge, logging, private evidence, and review shall be enforced at their declared boundary.
- **REQ-SEC-CULT-016 — SHALL NOT:** A cultural-rights decision, consent record, community approval, civic response, or policy receipt shall grant machine privilege or direct host privilege.
- **REQ-SEC-CULT-017 — SHALL:** Cross-domain publication of protected material shall use the Publication Gateway and applicable Governance Policy Runtime decisions while preserving the source component's data ownership.
- **REQ-SEC-CULT-018 — SHALL:** Restricted distribution shall use audience-scoped artifacts, encrypted recipient-scoped delivery, separate shards, or another declared control that prevents unauthorized payload possession.
- **REQ-SEC-CULT-019 — SHALL:** Cultural-rights restrictions shall propagate to derived artifacts, indexes, caches, exports, backups, synchronization payloads, runtime packs, and published representations according to their lineage and policy.
- **REQ-SEC-CULT-020 — SHALL NOT:** A derivative, translation, summary, embedding, index, thumbnail, transcription, metadata record, or format conversion shall erase cultural-rights lineage or receive broader authority by default.
- **REQ-SEC-CULT-021 — SHALL NOT:** Native AI authority, direct mounting into an AI domain, or unreviewed inference over restricted, sacred, or ceremonial material shall be permitted by the cultural-rights baseline.
- **REQ-SEC-CULT-022 — SHALL:** External AI processing shall remain an explicitly approved integration path with action-specific authority, consent, purpose, provenance, obligations, and owning-component acceptance of candidate output.
- **REQ-SEC-CULT-023 — SHALL:** SenTient and other advisory workbenches shall receive only explicitly approved bounded inputs and shall return non-authoritative candidate output with provenance.
- **REQ-SEC-CULT-024 — SHALL:** Withdrawal shall stop new distribution, update discovery and indexes, address publications, purge controlled caches where authorized, propagate to derivatives, and retain only the minimal lawful or policy-required proof.
- **REQ-SEC-CULT-025 — SHALL:** Withdrawal, purge, and derived-artifact actions shall identify the authorized requester, target scope, completion objective, notifications, exceptions, retained proof, receipts, and evidence.
- **REQ-SEC-CULT-026 — SHALL:** Dissent and disputes shall preserve each declared position, authority, evidence, decision effect, notice, resolution authority, and resolution receipt without rewriting the historical record.
- **REQ-SEC-CULT-027 — SHALL:** Every active cultural-rights policy shall define its effective date, review date, review authorities, appeal path, complaint channels, reversal behavior, review triggers, and receipt requirements.
- **REQ-SEC-CULT-028 — SHALL:** Policy activation shall be atomic or use an equivalent no-partial-state transition and shall preserve rollback or forward-repair capability with the prior policy identity and decision-receipt lineage.
- **REQ-SEC-CULT-029 — SHALL:** Public receipts shall disclose only bounded decision information while authority evidence, consent evidence, community protocols, dissent positions, restricted subject details, and withdrawal evidence remain private proof.
- **REQ-SEC-CULT-030 — SHALL:** Offline evaluation shall use the active locally verified policy, identity, consent, authority, trust, and evidence state and shall expose policy freshness and any resulting limitation.
- **REQ-SEC-CULT-031 — SHALL NOT:** A component, importer, exporter, publisher, AI integration, cache, index, or lifecycle tool shall write another component's authoritative cultural-rights or subject records directly.
- **REQ-SEC-CULT-032 — SHALL:** A complete cultural-rights conformance claim shall include schema, authority, consent, audience, action, AI, distribution, withdrawal, dissent, recourse, offline, publication, lineage, receipt, privacy, and negative-path tests with evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Creating a cultural-rights policy

Policy creation follows this order:

1. identify the protected subjects and owning components;
2. identify communities and jurisdictions;
3. identify creators, rights holders, stewards, delegates, and decision bodies;
4. collect authority and delegation evidence;
5. define cultural context and protocols;
6. define audiences and qualifications;
7. define access and discovery behavior;
8. define independent reuse rights;
9. define the consent model and evidence;
10. define all action decisions;
11. define external AI and SenTient restrictions;
12. define distribution and publication behavior;
13. define withdrawal and purge behavior;
14. record dissent or disputes;
15. define review and recourse;
16. define enforcement components and offline behavior;
17. define receipts and private proof;
18. complete approval and separation of duties;
19. validate the policy;
20. package, sign, and activate it through the governance artifact lifecycle.

### 6.2 Evaluating an action

Action evaluation:

1. receives the actor, subject, action, purpose, audience, profile, and environment;
2. verifies actor and authority identities;
3. resolves the active subject owner and cultural-rights policy;
4. verifies policy status and freshness;
5. resolves applicable community protocols;
6. resolves consent and evidence;
7. evaluates dissent and conflict;
8. evaluates action-specific rules;
9. calculates obligations;
10. returns the bounded decision and reason codes;
11. creates the decision receipt;
12. leaves execution to the performing component.

### 6.3 Access or display

Access or display:

1. evaluates discovery and metadata visibility;
2. verifies audience qualification;
3. verifies authentication strength;
4. verifies action-specific consent;
5. applies redaction;
6. presents required context and attribution;
7. restricts download, copying, or session export as declared;
8. records access evidence when required;
9. expires the access context at the declared boundary.

### 6.4 Export

Export:

1. selects subjects and derivatives;
2. resolves source ownership and policy lineage;
3. identifies export purpose and audience;
4. verifies export authority and consent;
5. verifies redistribution and retention terms;
6. constructs an audience-scoped payload;
7. applies redaction and encryption;
8. includes context, attribution, policy, and provenance;
9. creates the export manifest;
10. records the decision and export receipts;
11. delivers through the declared boundary.

### 6.5 Publication

Publication:

1. identifies the source records and owning component;
2. selects the intended audience and purpose;
3. evaluates cultural authority, consent, context, reuse, dissent, and distribution;
4. applies minimization, redaction, encryption, notice, and attribution;
5. creates a publication intent;
6. submits the bounded payload to the Publication Gateway;
7. records the gateway result;
8. presents completed publication only after verification;
9. retains source ownership and policy lineage.

### 6.6 External AI request

External AI request:

1. identifies the precise AI activity;
2. identifies the approved integration;
3. selects the minimum required subject content;
4. evaluates cultural authority and consent for that AI activity;
5. verifies purpose, audience, retention, training, and provider restrictions;
6. creates an isolated export or request payload;
7. records provenance and obligations;
8. performs the external request;
9. receives candidate output;
10. deletes or retains provider-side material according to the contract;
11. returns the candidate to the owning component;
12. completes human or authority review;
13. accepts selected values through the owning component's command;
14. records the full evidence chain.

### 6.7 Withdrawal

Withdrawal:

1. verifies the requester and withdrawal authority;
2. identifies subjects, copies, derivatives, indexes, caches, exports, and publications;
3. identifies legal or policy retention constraints;
4. stops new distribution;
5. updates access, discovery, and indexes;
6. requests publication withdrawal;
7. purges controlled caches where authorized;
8. withdraws, restricts, or rebuilds derivatives;
9. notifies declared authorities;
10. preserves minimal required proof;
11. validates completion;
12. creates the withdrawal receipt.

### 6.8 Dispute resolution

Dispute resolution:

1. records each position and authority;
2. preserves supporting evidence;
3. applies the active decision effect;
4. routes review to the declared resolution authority;
5. records deliberation without exposing protected private proof publicly;
6. records the resolution;
7. applies policy amendment, continued restriction, or another governed result;
8. creates the resolution receipt;
9. preserves prior positions.

### 6.9 Policy review and supersession

Review:

1. identifies the review trigger;
2. loads the active policy and decision history;
3. verifies current authorities and communities;
4. reviews changes in subjects, use, distribution, jurisdiction, AI capability, or risk;
5. reviews dissent, complaints, withdrawals, and incidents;
6. proposes a new version when needed;
7. obtains required approvals;
8. validates the new policy;
9. stages and activates it atomically;
10. retains the previous policy and receipt lineage;
11. marks supersession explicitly.

### 6.10 Offline synchronization

Offline synchronization:

1. exports policy, authority, consent, trust, and revocation updates through a verified offline bundle;
2. imports them into quarantine;
3. validates each artifact independently;
4. stages eligible policy material;
5. activates the policy through the governance lifecycle;
6. records local policy freshness;
7. evaluates queued actions against the now-active state;
8. exports local decisions, withdrawals, disputes, and receipts back through a protected result bundle.

## 7. Failure States and Safe Degradation

| Failure state | Required behavior |
| --- | --- |
| Cultural-rights policy is missing | Governed access, reuse, export, publication, AI access, synchronization, withdrawal, and purge remain blocked. |
| Policy schema is invalid | The candidate policy is rejected; the prior verified policy remains active. |
| Subject ownership cannot be resolved | The action is blocked and no component is selected implicitly. |
| Cultural authority cannot be resolved | The action is denied or enters declared authority review. |
| Delegation evidence is absent or expired | The delegate is not accepted for the requested decision. |
| Consent is missing | The action follows the policy's denial or authority-review result. |
| Consent conflicts | The conflict is preserved and the declared conflict behavior applies. |
| Consent is withdrawn | New covered actions stop and withdrawal propagation begins. |
| Audience qualification fails | Access or distribution is denied for that audience. |
| Required context cannot be rendered | Display or publication remains blocked when context is a precondition. |
| Required obligation cannot be enforced | The allow result is not executed. |
| Publication Gateway is unavailable | Source state remains local; publication intent can remain queued, but publication is not claimed. |
| Governance Policy Runtime is unavailable | Policy-bound actions requiring a new decision remain blocked. |
| Identity and Trust is unavailable | New authority- and consent-bound decisions remain blocked unless valid local evidence reuse is explicitly permitted. |
| Policy is stale offline | Freshness is exposed; actions outside the permitted stale-policy behavior remain blocked. |
| External AI integration is unavailable | Core local access and deterministic operation continue; no substitute provider is selected. |
| SenTient is unavailable | Core operation continues without advisory enrichment. |
| External AI provider terms conflict with policy | The request is denied. |
| Restricted content enters an unapproved AI domain | Processing stops, incident handling begins, and affected copies and outputs are traced. |
| Derived-artifact lineage is missing | Distribution, publication, reuse, and AI processing of the derivative remain blocked. |
| Withdrawal cannot reach an external copy | The failure is recorded, new controlled distribution stops, and recourse or notification follows the policy. |
| Cache purge cannot be verified | The cache remains treated as potentially containing the subject and is isolated or expired. |
| Dissent is active | The declared denial, authority-review, or dissent-notice behavior applies. |
| Appeal channel is unavailable | The decision remains reviewable and an alternate declared recourse mechanism is used; rights are not silently removed. |
| Policy activation fails | The prior verified policy remains active or forward repair begins. |
| Receipt storage is unavailable | Receipt-required actions remain blocked or uncommitted. |
| Private evidence store is unavailable | Decisions requiring that evidence remain blocked; public logs do not absorb the private data. |
| Resource pressure occurs | Optional work can queue or stop, but cultural-rights checks are not bypassed. |
| Purge safety cannot be established | Destructive deletion remains blocked while withdrawal or restriction can continue. |

Safe degradation retains restrictions rather than widening access.

## 8. Cross-Component Interactions

### 8.1 Data-owning components

The owning component stores the protected subject and authoritative policy attachment or reference assigned by its contract.

It requests decisions and enforces them.

It does not delegate its data ownership to the policy runtime.

### 8.2 Governance Policy Runtime

The Governance Policy Runtime evaluates cultural-rights policy, consent, obligations, dissent, and decision behavior.

It returns a bounded decision and receipt.

It does not publish, export, delete, or mutate another component's subject directly.

### 8.3 Identity and Trust

Identity and Trust verifies actors, cultural authorities, delegates, recipients, communities, and relying context.

Identity verification does not establish consent or cultural approval by itself.

### 8.4 Publication Gateway

The Publication Gateway performs governed cross-domain disclosure and publication.

It consumes the cultural-rights decision and obligations.

It does not become the rights holder or source-data owner.

### 8.5 Audit Broker

The Audit Broker routes declared public events and private evidence references.

It does not place restricted authority or consent evidence into a public audit stream.

### 8.6 Konnaxion

Konnaxion applies cultural-rights policy to civic spaces, proposals, responses, candidate imports, civic readings, exports, and publication intents when protected subjects are involved.

A civic decision does not override community authority.

### 8.7 Kristal Runtime

Kristal preserves epistemic identity and lineage.

Cultural-rights policy controls discovery, query, rendering, distribution, and Runtime Pack composition without merging workflow state into Kristal content identity.

### 8.8 kOA Mediatheque and external UCKK publication

The kOA Mediatheque preserves source and derivative media lineage. Publication to external UCKK carries only authorized metadata, rights, restrictions, provenance, and content.

Native processing remains deterministic.

External Suno or Gamma use requires explicit action-specific cultural authority, consent, provenance, and controlled candidate re-import.

### 8.9 Ariane Runtime

Ariane presents context notices, access limitations, obligations, decisions, and recourse.

Ariane cannot hide a denied or restricted result through alternate navigation.

External voice receives only content approved for that integration boundary.

### 8.10 SemantiK Architect Runtime

The language runtime can render approved language artifacts and context notices.

Translation rights remain distinct from runtime capability.

Availability of a language pack does not grant permission to translate protected content.

### 8.11 SenTient

SenTient accepts only explicitly approved bounded inputs.

It remains isolated and non-authoritative.

Its outputs return as candidates with provenance.

### 8.12 Resource Governor

The Resource Governor can limit or queue expensive rendering, indexing, export, purge, and AI-related work.

It cannot bypass cultural-rights policy because capacity is available or deny cultural authority because a workload is expensive.

### 8.13 Offline bundle importer

The importer verifies policy and subject artifacts independently.

Import does not activate the policy or authorize payload use.

Policy activation and subject import remain separate transitions.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Accepted decisions

| Decision | Effect |
| --- | --- |
| `DEC-COMP-001` | Keeps cultural-rights evaluation, publication, identity, audit, resource control, and data ownership in separate component boundaries. |
| `DEC-DATA-001` | Preserves the logical owner of protected subjects and derivatives across physical consolidation, export, backup, restore, and synchronization. |
| `DEC-GOV-001` | Places cultural-rights and consent decisions in the Governance Policy Runtime while keeping Resource Governor separate. |
| `DEC-GATE-001` | Requires cross-domain publication through the Publication Gateway and keeps ingestion separate from publication. |
| `DEC-AI-001` | Excludes native AI authority and treats approved external output as candidate input. |
| `DEC-SENT-001` | Keeps SenTient optional, isolated, task-activated, and non-authoritative. |
| `DEC-REL-001` | Places policy bundles and protected knowledge artifacts in independently governed release channels and compatibility sets. |
| `DEC-PROFILE-BASELINE-001` | Keeps profile-specific offline, encryption, trust, retention, and enforcement topology out of the global baseline. |

### 9.2 Related ADRs

| ADR | Relevance |
| --- | --- |
| `ADR-006` | Preserves first-class component boundaries. |
| `ADR-008` | Separates governance and knowledge release channels. |
| `ADR-009` | Establishes policy-runtime evaluation for authorization, consent, disclosure, and recourse. |
| `ADR-010` | Preserves selective audit and private proof. |
| `ADR-013` | Separates global rules from profile implementation. |
| `ADR-014` | Establishes the strict external AI boundary. |
| `ADR-018` | Keeps SenTient isolated and advisory. |
| `ADR-019` | Separates resource control from governance policy. |
| `ADR-030` | Establishes local kOA Mediatheque ownership. |
| `ADR-021` | Keeps Ariane local operation independent from external voice. |
| `ADR-031` | Keeps UCKK external and publication explicit. |
| `ADR-023` | Makes offline and high-assurance overlay behavior explicit. |
| `ADR-024` | Preserves logical ownership across physical deployment forms. |

### 9.3 Prohibited assumptions

The following assumptions are prohibited:

- local storage alone proves cultural sovereignty;
- a repository administrator is a cultural authority;
- a custodian owns the cultural rights;
- a creator is the only possible authority;
- one community representative can satisfy a quorum automatically;
- possession of a copy proves consent;
- public metadata proves public content;
- discovery permission proves download permission;
- display permission proves reuse permission;
- preservation permission proves publication permission;
- lack of a denial is consent;
- prior consent applies to every future purpose;
- a translation has no cultural-rights lineage;
- a thumbnail or transcript is harmless metadata;
- de-identification always removes cultural sensitivity;
- a signed policy is active;
- an imported policy is active;
- a policy receipt performs the action it describes;
- a Publication Gateway request proves publication;
- a UI restriction protects an unrestricted universal artifact;
- encryption changes cultural authority;
- a backup is exempt from cultural-rights policy;
- an external AI provider can retain data because its terms allow it;
- a model output is authoritative because a person reviewed the prompt;
- SenTient can read a component database directly;
- a civic vote overrides community authority;
- a resource limit can disable required rights checks;
- withdrawal always means deletion of all evidence;
- resolution can erase dissent history;
- offline operation permits weaker consent or authority;
- a derivative receives broader rights because it changed format.

## 10. Validation Criteria

This document conforms when all of the following checks pass:

1. metadata status is `active`;
2. the registered path is `07-security/14-cultural-rights-and-consent.md`;
3. all canonical references resolve;
4. all listed decisions are accepted;
5. all requirements match the requirements registry;
6. all locks resolve and pass;
7. the cultural-rights policy schema is Draft 2020-12 valid;
8. every active policy has a unique policy identity and version;
9. every subject resolves to one owning component;
10. every subject type and data classification is valid;
11. every community reference resolves;
12. every cultural authority reference resolves;
13. every delegation resolves to an effective delegating authority and evidence;
14. every protocol resolves to declared authorities and jurisdictions;
15. every audience has qualification, redistribution, encryption, and export behavior;
16. access, discovery, indexing, and metadata visibility are aligned;
17. display, download, reproduction, adaptation, translation, commercial, research, preservation, and attribution rules are complete;
18. consent records are explicit and action-, purpose-, audience-, scope-, and time-bound;
19. silence cannot satisfy consent;
20. missing and conflicting authority behavior is explicit;
21. all 18 action enforcement points are present;
22. action decisions contain audiences, roles, consent, purposes, obligations, reason codes, and offline behavior;
23. all 11 external-AI activities are explicitly governed;
24. native AI authority and direct AI-domain mounting remain prohibited;
25. SenTient remains candidate-only and cannot write authoritative state;
26. distribution rules prevent unrestricted universal packaging of restricted content;
27. Publication Gateway use is required for cross-domain publication;
28. source and derivative lineage is complete;
29. withdrawal propagation covers distribution, indexes, publications, caches, derivatives, and retained proof;
30. purge tests preserve ownership and evidence constraints;
31. dissent positions and resolution history remain intact;
32. review, appeal, complaint, reversal, and trigger fields are complete;
33. policy activation is atomic or equivalent;
34. rollback or forward repair is defined;
35. existing receipts preserve the policy identity used at decision time;
36. public receipt fields exclude private authority, consent, dissent, and subject evidence;
37. private evidence remains access-controlled;
38. offline evaluation exposes policy, trust, consent, and evidence freshness;
39. stale or missing required policy state does not widen access;
40. direct cross-component writes are absent;
41. resource pressure cannot bypass rights checks;
42. negative tests cover missing policy, missing authority, missing consent, conflict, wrong audience, obligation failure, publication bypass, AI bypass, lineage loss, withdrawal failure, and receipt failure;
43. requirement-to-test-to-evidence traceability is complete;
44. active content is English;
45. placeholder and open-authority markers are absent.

The validator reports focused failures, including:

```text
cultural_policy_schema_invalid
cultural_policy_identity_collision
cultural_subject_owner_missing
cultural_subject_type_invalid
cultural_community_ref_missing
cultural_authority_ref_missing
cultural_delegation_invalid
cultural_protocol_ref_missing
cultural_audience_ref_missing
cultural_access_rule_inconsistent
cultural_reuse_rule_incomplete
cultural_consent_missing
cultural_consent_conflict_unhandled
cultural_silence_used_as_consent
cultural_action_policy_missing
cultural_obligation_unenforced
cultural_ai_action_missing
cultural_ai_boundary_violation
cultural_sentient_direct_write
cultural_distribution_not_scoped
cultural_publication_gateway_bypassed
cultural_derivative_lineage_missing
cultural_withdrawal_not_propagated
cultural_purge_owner_unverified
cultural_dissent_history_lost
cultural_recourse_missing
cultural_policy_activation_partial
cultural_receipt_private_data_exposed
cultural_offline_freshness_missing
cultural_rights_check_bypassed
```

## 11. Non-Normative Examples

### 11.1 Community-only collection

A collection is discoverable only to verified community members.

Its metadata is redacted outside that audience, its payload is encrypted to approved recipients, redistribution is prohibited, and display includes the community context notice.

### 11.2 Preservation without publication

A community approves an encrypted preservation copy held by designated stewards.

The policy still prohibits public display, download, commercial use, and publication. Preservation authority does not become publication authority.

### 11.3 Research access

A researcher requests access for a stated non-commercial project.

The policy verifies audience qualification, community and creator consent, purpose, retention, encryption, attribution, no-redistribution, and return-or-destroy obligations. The approval expires at the declared review boundary.

### 11.4 Translation review

A protected oral-history transcript can be translated only for community use.

The translation is reviewed by the declared authority, carries source lineage and context, and receives the same or narrower distribution policy.

### 11.5 AI summarization denied

A user requests external summarization of a restricted ceremonial record.

The AI action policy forbids summarization. The system does not send the text, an excerpt, an embedding, or a derived transcript to the provider.

### 11.6 Approved external transcription

A community approves external transcription of selected non-sacred audio for one preservation purpose.

The request uses an approved integration, sends only the selected audio, prohibits training and retention, records provenance, receives candidate text, and requires community review before acceptance into the kOA Mediatheque. Any later UCKK publication requires a separate rights and disclosure decision.

### 11.7 Publication through the gateway

Konnaxion prepares a public description of a protected proposal.

The source record remains restricted. The approved payload contains only authorized fields, context, attribution, and audience. The Publication Gateway records the completed publication separately from the Konnaxion intent.

### 11.8 Withdrawal from a Runtime Pack

A rights holder submits an authorized withdrawal for one knowledge item included in a Kristal Runtime Pack.

New distribution stops, discovery is updated, controlled caches are purged, and a replacement pack is built without the subject. The minimal withdrawal receipt remains protected.

### 11.9 Active dissent

Two recognized authorities disagree about research access.

The policy records both positions and requires authority review. The system does not infer approval from the larger number of ordinary users or from prior access.

### 11.10 Offline node

A sovereign offline node has a verified policy and current local consent evidence for community display, but lacks current authority for export.

Local display continues with the required context. Export remains blocked until an approved policy or consent update is imported.
