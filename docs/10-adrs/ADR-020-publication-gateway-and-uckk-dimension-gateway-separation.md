<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ADR-020",
  "document_class": "architecture_decision_record",
  "status": "active",
  "language": "en",
  "layer": "adrs",
  "adr_id": "ADR-020",
  "adr_status": "accepted",
  "decision_class": "major",
  "owner_decision_id": "DEC-GATE-001",
  "created_at": "2026-08-03",
  "accepted_at": "2026-08-03",
  "effective_at": "2026-08-03",
  "supersedes": [],
  "superseded_by": null,
  "scope": [
    "component:publication_gateway",
    "component:uckk_dimension_gateway",
    "component:uckk_platform",
    "cross_domain_publication",
    "uckk_media_admission"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json#/decisions/DEC-GATE-001",
    "generated/decision-index.json#/adrs/ADR-020",
    "contracts/terminology.contract.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json#/components/publication_gateway",
    "generated/component-catalog.json#/components/uckk_dimension_gateway",
    "generated/component-catalog.json#/components/uckk_platform",
    "contracts/artifact-classes.contract.json#/artifact_classes/publication_request",
    "contracts/artifact-classes.contract.json#/artifact_classes/publication_receipt",
    "contracts/integration-types.contract.json",
    "contracts/release-channels.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-AI-001",
    "DEC-DATA-001",
    "DEC-GATE-001",
    "DEC-GOV-001",
    "DEC-PROFILE-001",
    "DEC-REL-001",
    "DEC-UCKK-001"
  ],
  "requirement_ids": [
    "REQ-CONST-026",
    "REQ-CONST-027",
    "REQ-DEG-027",
    "REQ-DEG-028",
    "REQ-ORGO-025",
    "REQ-ORGO-027",
    "REQ-ORGO-028"
  ],
  "lock_ids": [
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GATE-001",
    "LOCK-GOV-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-UCKK-001",
    "LOCK-UCKK-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-002",
    "DOC-CONST-013",
    "DOC-SYS-009",
    "DOC-SYS-017"
  ],
  "tags": [
    "adr",
    "publication-gateway",
    "uckk-dimension-gateway",
    "uckk-platform",
    "gateway-separation",
    "cross-domain-publication",
    "media-ingestion",
    "disclosure",
    "component-boundaries",
    "data-ownership"
  ]
}
KOA:DOC-META:END -->

# ADR-020 — Separate Publication Gateway and UCKK Dimension Gateway

| Field | Value |
| --- | --- |
| ADR | `ADR-020` |
| Owner decision | `DEC-GATE-001` |
| Status | Accepted |
| Decision class | Major |
| Accepted | 2026-08-03 |
| Effective | 2026-08-03 |
| Supersedes | None |
| Superseded by | None |

## 1. Context

kOA requires controlled boundaries for two operations that can both involve moving content but have different meanings, authorities, risks, and outcomes:

1. releasing selected information across an authority or security boundary; and
2. importing user-selected media into a declared UCKK dimension.

The first operation is publication.

The second operation is media admission.

They can appear similar at an implementation level because both can:

- receive a request;
- inspect an artifact;
- verify content identity;
- evaluate policy;
- produce a result;
- emit evidence;
- move or copy content.

Those similarities do not make them one architectural responsibility.

Cross-domain publication determines whether selected information can leave its current authority or security domain and reach a declared audience or destination.

UCKK dimension admission determines whether selected media can enter one declared UCKK dimension under UCKK's deterministic ingestion and storage rules.

Combining both responsibilities into one gateway would create ambiguity over:

- whether an import is also a disclosure;
- whether UCKK admission grants publication permission;
- whether publication grants UCKK ownership;
- which component owns the source record;
- which policy applies;
- which receipt proves which transition;
- whether gateway failure blocks publication, ingestion, or both;
- whether an external adapter can bypass one boundary through the other;
- whether a shared implementation can write into unrelated authoritative stores.

The architecture therefore requires two separate component contracts.

## 2. Decision

Publication Gateway and UCKK Dimension Gateway shall remain separate components with separate contracts, interfaces, authority, state, failure behavior, receipts, tests, and lifecycle.

Publication Gateway controls:

- cross-domain disclosure;
- governed publication;
- release to an external or differently governed audience;
- destination and audience validation;
- disclosure, redaction, rights, consent, approval, and policy conditions;
- publication outcome and publication receipt.

UCKK Dimension Gateway controls:

- explicit user-selected media admission;
- dimension-targeted transfer;
- content and intrinsic hash verification;
- format and admission validation;
- controlled handoff to the UCKK Platform;
- admission outcome for the declared UCKK dimension.

Neither component substitutes for the other.

A successful UCKK admission does not authorize publication.

A successful publication does not authorize UCKK admission.

A workflow requiring both boundaries shall invoke both through explicit independent transitions in the required order.

The UCKK Platform remains separate from UCKK Dimension Gateway. The platform owns admitted UCKK media and deterministic media operations after successful admission. The gateway owns the admission boundary, not the platform's authoritative storage or media lifecycle.

## 3. Decision Scope

### 3.1 Publication Gateway scope

Publication Gateway applies when selected information crosses:

- a component authority boundary for public or external release;
- a private-to-public boundary;
- a tenant or organizational disclosure boundary;
- a security domain;
- a sovereignty or jurisdictional boundary;
- another boundary classified as governed publication by active policy.

It applies regardless of whether the source content originated in:

- Orgo;
- Kristal;
- Konnaxion;
- UCKK;
- an external integration;
- another component.

### 3.2 UCKK Dimension Gateway scope

UCKK Dimension Gateway applies when a user explicitly selects media for admission into a declared UCKK dimension.

The media can originate from:

- a local file;
- an authorized component export;
- a removable medium;
- an approved integration;
- a controlled re-import from Suno, Gamma, or another approved external adapter;
- another declared source.

Its scope is admission into UCKK, not release from the source domain to an audience.

### 3.3 Operations requiring both gateways

A workflow requires both gateways when content is:

- admitted into UCKK and later published outside its authorized UCKK context;
- published from another domain and separately admitted into UCKK;
- exported to an external processor, re-imported into UCKK, and later released to an external audience;
- moved through a sequence containing both an ingestion boundary and a publication boundary.

Each transition retains its own request, decision, result, evidence, and receipt.

### 3.4 Excluded decisions

This ADR does not decide:

- the complete UCKK dimension taxonomy;
- the exact storage format of UCKK media;
- one universal publication destination;
- one universal disclosure policy;
- one external media provider;
- one transport protocol;
- one user-interface flow;
- one queue or service implementation;
- one profile membership set.

Those facts remain owned by component, profile, integration, policy, artifact, and release contracts.

## 4. Definitions and Interpretation

### 4.1 Publication Gateway

**Publication Gateway** is the controlled boundary for cross-domain disclosure and publication.

Its canonical identifier is `publication_gateway`.

Its successful outcome is a governed release to the exact approved audience or destination.

### 4.2 UCKK Dimension Gateway

**UCKK Dimension Gateway** is the controlled boundary that imports user-selected media into a declared UCKK dimension.

Its canonical identifier is `uckk_dimension_gateway`.

The term `UCKK gateway` is forbidden because it can incorrectly collapse the UCKK Platform and UCKK Dimension Gateway.

### 4.3 UCKK Platform

**UCKK Platform** is the authoritative media platform for deterministic ingestion, storage, transformation, export, backup, and restore after admission.

Its canonical identifier is `uckk_platform`.

UCKK Dimension Gateway is not the authoritative platform merely because it performs admission.

### 4.4 Publication request

A **publication request** is the canonical request artifact submitted to Publication Gateway for controlled release across an authority or security boundary.

It is not an UCKK admission request.

### 4.5 Publication receipt

A **publication receipt** is the immutable record of a Publication Gateway decision, released content identity, applied policy, destination, and outcome.

It does not prove UCKK admission.

### 4.6 Media admission

Media admission is the controlled transition by which explicit user-selected media becomes admitted to one declared UCKK dimension.

The exact request and result interface is owned by the UCKK Dimension Gateway component contract.

This ADR does not create an additional artifact class or invent its field structure.

### 4.7 Cross-domain publication

Cross-domain publication occurs when content is intentionally released beyond its current authority or security boundary to a declared destination or audience.

A local copy, deterministic transcode, thumbnail, backup, or internal UCKK dimension move is not automatically publication.

## 5. Rationale

### 5.1 Different authority questions

Publication asks:

> May this selected information be disclosed to this audience or destination under the applicable rights, consent, policy, and approval conditions?

UCKK admission asks:

> May this user-selected media be admitted into this declared UCKK dimension under its format, identity, provenance, ownership, and admission rules?

One decision cannot safely answer both questions.

### 5.2 Different ownership boundaries

Publication Gateway never becomes the owner of the source component's authoritative record.

UCKK Dimension Gateway never becomes the owner of all UCKK media.

The requesting component retains source-domain authority.

The UCKK Platform owns admitted UCKK media according to its contract after admission completes.

### 5.3 Different artifact contracts

Publication already has canonical artifact classes:

- `publication_request`;
- `publication_receipt`.

Reusing those artifacts for UCKK admission would falsely characterize ingestion as disclosure and would contaminate publication evidence with media-platform semantics.

### 5.4 Different policy dimensions

Publication can require evaluation of:

- audience;
- destination;
- disclosure;
- redaction;
- consent;
- cultural rights;
- tenant policy;
- legal or sovereignty restrictions;
- approval;
- revocation and correction.

UCKK admission can require evaluation of:

- explicit user selection;
- target dimension;
- source and content identity;
- accepted media type;
- intrinsic hash verification;
- duplicate behavior;
- provenance;
- available storage;
- deterministic processing compatibility.

Some policies can apply to both, but the decisions remain distinct.

### 5.5 Different failure effects

Publication Gateway failure shall queue or reject publication without disclosing content or changing source-domain authority.

UCKK Dimension Gateway failure shall reject or defer new media admission without affecting existing UCKK content.

Combining the gateways would create an unnecessary shared failure domain.

### 5.6 Different lifecycle and recovery

A failed publication leaves the source content unpublished.

A failed admission leaves the media outside the target UCKK dimension.

Publication correction can require revocation and reissue of a publication receipt or destination action.

Admission recovery can require retry, deduplication, cleanup of staged media, or controlled re-import.

### 5.7 External-adapter safety

Suno and Gamma are optional user-triggered external adapters.

Their outputs return as candidate external artifacts.

Controlled re-import uses UCKK Dimension Gateway when the user selects the result for a UCKK dimension.

Optional later release uses Publication Gateway.

A single combined gateway would make it easier to confuse provider return with approval for public release.

## 6. Required Decision Rules

### 6.1 Separate component contracts

The component registry shall contain separate entries for:

```text
publication_gateway
uckk_dimension_gateway
uckk_platform
```

Each shall define its own:

- purpose;
- capabilities;
- interfaces;
- data authority;
- dependencies;
- policies;
- failure states;
- recovery;
- profile inclusion;
- release compatibility;
- tests and evidence.

### 6.2 Publication request rule

Cross-domain publication shall begin with a valid `publication_request`.

The request shall identify, according to its canonical schema:

- requester;
- source reference;
- selected information or artifact;
- intended audience or destination;
- purpose;
- applicable policy context;
- required approvals;
- provenance where applicable.

UCKK Dimension Gateway shall not accept a publication request as an instruction to admit media.

### 6.3 Publication execution rule

Publication Gateway shall:

1. validate the request;
2. resolve requester, source, destination, and content identity;
3. verify source-component authority;
4. evaluate required disclosure and publication policy;
5. apply declared redaction or transformation through authorized paths;
6. verify final released content identity;
7. execute or coordinate the exact approved release;
8. emit the required publication receipt;
9. leave source-domain ownership unchanged.

### 6.4 UCKK admission rule

UCKK Dimension Gateway shall:

1. require explicit user selection;
2. resolve the target UCKK dimension;
3. resolve source and media identity;
4. verify intrinsic content identity where required;
5. validate media format and declared provenance;
6. evaluate admission and dimension policy;
7. prevent undeclared duplicate or conflicting admission;
8. transfer the admitted media through the UCKK Platform's declared interface;
9. verify the resulting admitted identity;
10. return the admission outcome.

The gateway shall not publish the media merely because admission succeeds.

### 6.5 Data-write rule

Publication Gateway shall not write directly into the authoritative store of:

- the requesting component;
- a destination component;
- UCKK Platform;
- UCKK Dimension Gateway.

UCKK Dimension Gateway shall not write directly into the source component's authoritative store or bypass the UCKK Platform's owner interface.

Any destination or UCKK mutation occurs through the owning component's declared interface.

### 6.6 Policy rule

Governance Policy Runtime remains authoritative for governed disclosure, consent, rights, privilege, and exceptions where applicable.

Neither gateway can infer approval from:

- user possession of a file;
- source-component access;
- successful hash verification;
- available storage;
- a Resource Governor admission;
- an external-provider result;
- a prior unrelated decision.

### 6.7 Resource rule

Resource Governor controls CPU, memory, I/O, process, worker, queue, concurrency, and timeout limits for both gateways.

A resource-admission result does not approve publication or UCKK admission.

### 6.8 Receipt and evidence rule

Publication Gateway produces `publication_receipt` artifacts as defined by the artifact-class registry.

UCKK Dimension Gateway produces its contract-defined admission outcome and required evidence.

The two records shall have distinct identities and shall not be represented as one generic gateway receipt.

### 6.9 Queue rule

Publication and UCKK admission queues, when used, shall remain distinct logical queues with separate:

- request identities;
- ordering and priority rules;
- expiry;
- policy context;
- retry behavior;
- cancellation;
- deduplication;
- result types.

A queue item cannot cross from one gateway to the other without a new explicit request.

### 6.10 User-intent rule

User selection for UCKK admission is not consent to publication.

User approval for publication is not selection of a UCKK dimension.

Interfaces shall present those actions distinctly.

### 6.11 External-adapter sequence

The accepted optional external-media workflow is:

```text
explicit user selection
→ controlled export
→ external processing
→ controlled candidate return
→ UCKK Dimension Gateway re-import when selected
→ provenance receipt
→ user review and approval
→ optional publication request
→ Publication Gateway
```

External processing shall not invoke either gateway automatically for authoritative mutation.

### 6.12 Shared implementation rule

The two components can share non-authoritative libraries, transport adapters, schema utilities, or infrastructure when that sharing does not merge:

- component identity;
- authority;
- interfaces;
- queues;
- authoritative state;
- policy decisions;
- receipts;
- failure state;
- release or conformance claims.

A shared process deployment does not make them one component.

## 7. Consequences

### 7.1 Positive consequences

- Publication and ingestion authority remain understandable.
- Source-domain ownership is preserved.
- UCKK Platform authority remains distinct from its admission boundary.
- User intent is not silently broadened.
- Publication requests and receipts retain precise semantics.
- Existing UCKK content remains available during admission-gateway failure.
- Source components remain usable during publication-gateway failure.
- External-adapter return cannot silently become public content.
- Policy, resource, lifecycle, and evidence responsibilities remain testable.
- Each gateway can evolve and scale independently.

### 7.2 Costs and constraints

- Workflows needing both transitions require two explicit requests.
- User interfaces must distinguish admission from publication.
- Components and integrations must implement separate client contracts.
- Traceability and evidence must cover both transitions.
- Some shared validation work can occur twice under different authority questions.
- Operations must monitor separate health and queue states.
- Release compatibility must account for both component contracts.

### 7.3 Operational consequences

Operations shall expose separate status for:

- publication availability;
- publication queue and failures;
- UCKK admission availability;
- UCKK admission queue and failures;
- UCKK Platform health;
- external-adapter availability.

An operator shall be able to determine which boundary failed without inspecting private content.

## 8. Alternatives Considered

### 8.1 One generic content gateway

**Rejected.**

A generic gateway would obscure whether a request is an import, publication, export, transformation, or destination write.

It would create an authority concentration point and ambiguous evidence.

### 8.2 Make Publication Gateway the only gateway

**Rejected.**

UCKK admission is not necessarily disclosure to an external audience.

Using publication artifacts for local media admission would introduce inappropriate destination, audience, and disclosure semantics.

### 8.3 Make UCKK Dimension Gateway handle publication

**Rejected.**

UCKK-specific admission policy cannot replace general cross-domain disclosure, consent, cultural-rights, audience, destination, and revocation policy.

It would also incorrectly imply that all publishable information must pass through UCKK.

### 8.4 Put both responsibilities in UCKK Platform

**Rejected.**

The UCKK Platform is the authoritative media platform after admission.

It is not the global publication authority for other components and should not own cross-domain disclosure policy.

### 8.5 Let every component publish directly

**Rejected.**

Direct publication would duplicate policy, redaction, destination, receipt, revocation, and audit behavior and create inconsistent disclosure boundaries.

### 8.6 Let integrations decide the boundary

**Rejected.**

External providers and adapters are non-authoritative.

Their APIs, storage, or return formats cannot determine whether content is admitted or published.

### 8.7 Use one deployed service with internal modules

**Conditionally acceptable as an implementation, not as an architecture.**

A profile can deploy one process containing both adapters only if the separate component contracts, identities, interfaces, state, policy decisions, queues, receipts, failure isolation, and conformance remain enforceable.

The shared process cannot become the canonical component boundary.

## 9. Security, Data, Lifecycle, and Release Implications

### 9.1 Security boundary

Publication Gateway is a disclosure-sensitive boundary.

UCKK Dimension Gateway is an ingestion-sensitive boundary.

Both require:

- resolved identity;
- minimum data access;
- bounded secrets;
- explicit policy where applicable;
- selective evidence;
- secure failure;
- profile-scoped execution.

Their threat models differ and shall be tested separately.

### 9.2 Data ownership

The requesting component retains authority over the source object.

Publication Gateway can create or transmit an approved publication representation but cannot mutate the source record directly.

UCKK Dimension Gateway can stage and validate candidate media but cannot become the authoritative UCKK store.

UCKK Platform owns the admitted media after its owner transaction commits.

### 9.3 Artifact implications

`publication_request` and `publication_receipt` remain publication-only artifacts.

The UCKK Dimension Gateway contract shall define its required request and outcome interfaces without reusing publication artifacts merely for convenience.

Artifacts intrinsic to content identity can use cryptographic digests.

No ordinary documentation or generic gateway metadata hash is introduced by this ADR.

### 9.4 Lifecycle

Gateway service updates belong to the `services` release channel.

Policy bundles governing disclosure or admission belong to `governance`.

UCKK runtime packs, language packs, Atlases, and approved knowledge artifacts belong to `knowledge` as defined by their classes.

System dependencies belong to `system`.

A Release Set binds compatible versions across all affected channels.

### 9.5 Failure and degradation

When Publication Gateway is unavailable:

- new publication is queued, deferred, or rejected according to contract;
- no disclosure occurs;
- source-domain data remains authoritative;
- local source-component use continues when dependencies permit.

When UCKK Dimension Gateway is unavailable:

- new media admission is rejected or deferred;
- existing UCKK content remains available;
- UCKK Platform does not infer admission;
- unrelated publication can continue.

When UCKK Platform is unavailable:

- the gateway cannot complete admission;
- staged candidate media remains non-authoritative;
- Publication Gateway remains independently available for non-UCKK sources.

### 9.6 Rollback and repair

Publication correction follows publication revocation, correction, and reissue behavior.

UCKK admission failure follows admission cleanup, duplicate reconciliation, owner-approved rollback, or forward repair.

One gateway's recovery procedure shall not modify the other's authoritative state.

## 10. Conformance and Evidence

Conformance shall prove both positive behavior and separation.

Required conclusions include:

| Evidence area | Required conclusion |
| --- | --- |
| Component identity | Both gateways and UCKK Platform resolve as separate components |
| Interface identity | Publication and admission use distinct interfaces |
| Request semantics | A publication request cannot trigger UCKK admission |
| Admission semantics | UCKK selection cannot trigger publication |
| User intent | Admission and publication require separate explicit actions |
| Data ownership | Source and UCKK owner stores are written only through owner interfaces |
| Policy | Disclosure policy and admission policy are evaluated for their own transitions |
| Resource governance | Resource Governor remains separate from authorization |
| Publication receipt | Successful publication produces the canonical publication receipt |
| Admission result | UCKK admission produces its separate contract-defined result |
| Queue isolation | Queue items cannot silently migrate between gateways |
| Failure isolation | Failure of one gateway preserves the other's unrelated capabilities |
| Existing content | UCKK admission failure does not disable existing UCKK content |
| No disclosure | Publication failure releases no information |
| External adapters | Candidate return requires controlled re-import and separate optional publication |
| UCKK Platform boundary | Dimension Gateway does not become the media platform owner |
| Release compatibility | Services and policy versions belong to a compatible Release Set |
| Terminology | Forbidden ambiguous term `UCKK gateway` is rejected |
| Traceability | `DEC-GATE-001` and `LOCK-GATE-001` resolve to tests and evidence |

The following fail conformance:

- one component registry entry for both gateways;
- one request type that ambiguously authorizes both transitions;
- publication caused solely by successful UCKK admission;
- UCKK admission caused solely by publication approval;
- a shared authoritative database owned by both gateways;
- direct writes to source or destination component stores;
- one generic receipt represented as proof of both transitions;
- shared failure that unnecessarily blocks both capabilities;
- an external adapter publishing its returned artifact automatically;
- UCKK Dimension Gateway treated as UCKK Platform;
- Publication Gateway treated as a media-ingestion service;
- missing `LOCK-GATE-001` traceability.

Evidence shall follow `docs/09-conformance/05-test-evidence.md`.

## 11. Decision Closure, Review, and Supersession

### 11.1 Closed decisions

This ADR closes the following questions:

- Publication Gateway and UCKK Dimension Gateway are separate components.
- Publication Gateway owns cross-domain publication execution.
- UCKK Dimension Gateway owns explicit dimension-targeted media admission.
- UCKK Platform remains separate from its admission gateway.
- Neither gateway substitutes for the other.
- Publication and admission require separate user intent and authority.
- Publication request and receipt artifacts are not generic gateway artifacts.
- A workflow requiring both boundaries performs two explicit transitions.
- Failure and recovery remain capability-scoped.
- External media processing returns candidate artifacts rather than publication authority.

### 11.2 Prohibited assumptions

This ADR shall not be interpreted to mean:

- every UCKK admission is publication;
- every publication is UCKK admission;
- content inside UCKK is automatically public;
- public content is automatically valid UCKK media;
- a content hash grants disclosure permission;
- user selection of a file grants destination consent;
- Publication Gateway owns source data;
- UCKK Dimension Gateway owns all UCKK media;
- UCKK Platform owns publication policy;
- Resource Governor can approve either transition;
- an external provider can approve re-import or publication;
- a shared process permits merged contracts;
- a shared library permits shared authoritative state;
- a profile can remove the separation through implementation convenience;
- an exception can establish a permanent merged-gateway architecture.

### 11.3 Review triggers

This ADR shall be reviewed when:

- a new content workflow appears to require both boundaries atomically;
- policy or user research shows the distinction cannot be presented safely;
- a profile proposes one deployed process for both components;
- the UCKK Platform authority model changes;
- publication expands to new destination or sovereignty classes;
- UCKK admission expands beyond media;
- evidence shows that the separation creates an unacceptable safety or operability failure;
- a formal transaction model can preserve both authorities while changing deployment structure.

### 11.4 Supersession condition

Supersession requires a new accepted major ADR that:

- identifies this ADR;
- explains why two contracts no longer preserve the required authority model;
- defines replacement component, data, policy, user-intent, failure, receipt, and lifecycle boundaries;
- preserves source ownership and UCKK Platform ownership;
- migrates publication requests and receipts without ambiguity;
- updates `DEC-GATE-001`, `LOCK-GATE-001`, component contracts, artifact contracts, tests, evidence, and Release Set compatibility;
- provides rollback, recovery, and credible-exit behavior.

Until superseded, this ADR remains the controlling rationale for `DEC-GATE-001`.
