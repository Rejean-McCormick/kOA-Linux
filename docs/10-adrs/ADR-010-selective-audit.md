<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "ADR-010",
  "document_class": "adr",
  "status": "active",
  "language": "en",
  "layer": "architecture_decision",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/decision-index.json"
  ],
  "decision_ids": [
    "DEC-AUDIT-001"
  ],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-AUDIT-001",
    "LOCK-AUDIT-002",
    "LOCK-AUDIT-003",
    "LOCK-AUDIT-004",
    "LOCK-AUDIT-005",
    "LOCK-AUDIT-006",
    "LOCK-AUDIT-007",
    "LOCK-AUDIT-008",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-GATE-001",
    "LOCK-OFFLINE-001",
    "LOCK-AI-001",
    "LOCK-AI-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-004"
  ],
  "tags": [
    "architecture-decision",
    "adr",
    "010",
    "selective",
    "audit"
  ]
}
KOA:DOC-META:END -->

# ADR-010 — Selective Audit

**ADR ID:** `ADR-010`  
**Status:** `accepted`  
**Decision class:** `major`  
**Decision owner:** `audit_architecture_owner`  
**Owner decision:** `DEC-AUDIT-001`  
**Created:** `2026-08-03`  
**Accepted:** `2026-08-03`  
**Effective:** `2026-08-03`  
**Supersedes:** None.  
**Superseded by:** None.

## 1. Decision Summary

kOA adopts selective audit as the system-wide audit architecture.

Audit evidence remains protected at its authoritative source or within explicitly governed evidence stores. Audit Broker coordinates requests, policy evaluation, evidence references, bounded disclosure, verification results, and audit receipts without becoming the unrestricted owner of every component’s logs, records, identities, or content.

An audit requester receives only the minimum evidence required to evaluate one declared claim for one authorized purpose, audience, scope, and validity period. The requester does not receive general access to source databases, complete event histories, unrelated tenants, protected identities, cultural context, private content, secrets, or operational internals.

The architecture separates:

- private proof from public evidence;
- evidence custody from audit coordination;
- audit authorization from evidence production;
- evidence production from claim evaluation;
- claim evaluation from publication;
- historical event facts from later corrections, revocations, disputes, and remediation;
- machine-assisted analysis from human or canonical authority.

Selective audit is required for accountability, recourse, conformance, incident review, publication receipts, governance decisions, support, release activation, migration, and other operations that require proof without indiscriminate disclosure.

## 2. Scope

### 2.1 Included scope

This decision applies globally to:

- audit requests;
- evidence discovery;
- evidence references;
- evidence collection;
- evidence minimization;
- evidence disclosure;
- public evidence;
- private proof;
- audit receipts;
- conformance evidence;
- governance evidence;
- publication evidence;
- identity and trust evidence;
- consent and cultural-rights evidence;
- component-boundary evidence;
- lifecycle and release evidence;
- support and diagnostic evidence;
- security and incident evidence;
- offline evidence exchange;
- dispute and recourse evidence;
- retention, expiry, correction, revocation, and closure.

### 2.2 Audit subjects

An audit can concern:

- a deployment;
- a profile claim;
- a component;
- an integration;
- an artifact;
- a Release Set;
- a publication;
- an UCKK admission;
- a governance decision;
- a consent record;
- a delegation;
- an identity or trust state;
- a data migration;
- a backup or restore;
- a support case;
- a workspace;
- an exception or waiver;
- a security event;
- an operational action.

### 2.3 Audit claims

A selective audit evaluates a bounded claim, such as:

- an operation was authorized;
- a required decision existed;
- a component used its declared interface;
- a publication used an approved representation;
- consent was valid at execution time;
- a profile passed applicable tests;
- a Release Set contained compatible versions;
- a migration completed or rolled back correctly;
- a support session expired and was cleaned up;
- an exception was active and in scope;
- an external disclosure used the approved destination;
- a prohibited action was denied;
- a historical event occurred even though its current state later changed.

The claim remains distinct from the evidence and the audit conclusion.

### 2.4 Excluded authority

This decision does not:

- make Audit Broker the owner of component business data;
- grant access to source content;
- grant consent;
- grant cultural authority;
- authorize publication;
- establish identity;
- define trust roots;
- approve exceptions;
- determine legal conclusions;
- replace incident response;
- replace component contracts;
- change observed test results;
- guarantee deletion outside kOA control;
- require every proof to become public;
- require one universal integrity technology.

### 2.5 Non-goals

The architecture does not seek to create:

- a universal surveillance log;
- unrestricted administrator visibility;
- a public ledger of private activity;
- one centralized copy of all component events;
- permanent retention of all diagnostic data;
- an AI system that decides truth or authorization;
- a mechanism that exposes protected evidence merely because a claim is important;
- a replacement for direct user recourse or human review.

## 3. Canonical References

### 3.1 Owner decision

- `generated/decision-index.json`
- `DEC-AUDIT-001` — selective audit with private proof and bounded disclosure.

### 3.2 ADR registry

- `generated/decision-index.json`
- `ADR-010`

The ADR registry owns the ADR identity, status, owner-decision relationship, supersession, and active participation.

### 3.3 Canonical objects constrained by this decision

This decision constrains:

- `generated/evidence-catalog.json`;
- `generated/traceability.json`;
- `generated/requirements-index.json`;
- `generated/assertion-index.json`;
- `generated/exception-index.json`;
- `contracts/integration-types.contract.json`;
- `generated/component-catalog.json`;
- `generated/authority-manifest.json`;
- `contracts/components/audit-broker.component.json`;
- `contracts/artifact-contracts/provenance-receipt.schema.json`;
- `contracts/artifact-contracts/publication-receipt.schema.json`;
- applicable evidence, disclosure, audit-request, audit-receipt, and public-evidence contracts;
- profile and component contracts that produce or consume evidence.

### 3.4 Related documents

- `01-constitution/10-selective-audit-and-recourse.md`;
- `01-constitution/12-cultural-rights-and-consent.md`;
- `04-components/03-component-integration-boundaries.md`;
- `07-security/13-privacy-and-disclosure.md`;
- `07-security/14-cultural-rights-and-consent.md`;
- `07-security/15-selective-audit.md`;
- `07-security/16-public-evidence-and-private-proof.md`;
- `07-security/17-cross-domain-publication.md`;
- `08-operations/12-incident-response.md`;
- `08-operations/15-support-and-diagnostics.md`;
- `09-conformance/15-exceptions-and-waivers.md`.

### 3.5 Related locks

This decision is protected by audit, data, governance, component, gateway, offline, and AI-boundary locks.

The audit locks establish that:

- every audit has a bounded claim and purpose;
- evidence custody remains with its declared owner;
- disclosure is minimum-necessary;
- public evidence and private proof remain distinct;
- audit receipts preserve historical truth;
- AI cannot authorize evidence access or determine the canonical conclusion;
- offline audit remains possible;
- audit cannot bypass component, publication, consent, cultural-rights, or identity boundaries.

## 4. Context and Problem

### 4.1 Accountability requirement

kOA requires evidence for:

- governance;
- conformance;
- security;
- publication;
- cultural rights;
- consent;
- release activation;
- migration;
- backup and restore;
- support;
- disputes;
- recourse.

A system that cannot produce evidence cannot make reliable claims about authorization, integrity, execution, denial, recovery, or accountability.

### 4.2 Disclosure problem

The same evidence can reveal:

- private user content;
- protected identities;
- tenant relationships;
- cultural context;
- security topology;
- internal component state;
- network addresses;
- credentials or secret-bearing fields;
- governance deliberation;
- unrelated operations;
- historical records outside the claim scope.

Copying complete logs or databases to every auditor creates a second security and privacy problem.

### 4.3 Centralization problem

A universal audit database would:

- duplicate authoritative data;
- create broad cross-component read paths;
- aggregate sensitive information;
- increase breach impact;
- obscure evidence ownership;
- complicate consent and cultural restrictions;
- become a critical online dependency;
- create retention and exit obligations for every component;
- encourage audit access to become administrator access.

### 4.4 Public accountability problem

Some claims require public evidence, but public disclosure of the underlying proof can harm the people or communities the audit is intended to protect.

The architecture therefore needs a way to publish a bounded verification statement while preserving private proof under controlled access.

### 4.5 Offline and sovereign operation

Sovereign nodes, hubs, and user endpoints need to collect, retain, exchange, and verify audit evidence without depending on a remote audit service, public ledger, cloud telemetry platform, or external AI provider.

### 4.6 Decision requirement

The system needs a single architecture decision that defines:

- who owns evidence;
- how an audit is authorized;
- how evidence is selected;
- how disclosure is minimized;
- how public evidence relates to private proof;
- how conclusions and receipts are recorded;
- how later corrections and disputes are handled;
- how profiles and offline operation remain supported.

## 5. Decision Drivers

Decision drivers, in priority order, are:

1. Minimum-necessary disclosure.
2. Preservation of component data ownership.
3. Verifiable accountability.
4. Human and canonical control over evidence access.
5. Separation of public evidence and private proof.
6. Tenant, identity, consent, and cultural-rights protection.
7. Historical truth with additive correction.
8. Offline and sovereign operation.
9. Selective recourse and dispute review.
10. Bounded retention and expiry.
11. Implementation independence.
12. Compatibility with release, profile, and conformance evidence.
13. No native AI authority.
14. Credible removal and exit.

## 6. Considered Options

### 6.1 Option A — Selective audit with source-owned evidence and bounded disclosure

**Description**

Components retain evidence they own. Audit Broker coordinates claim-bound requests, policy decisions, evidence references, minimized disclosure packages, verifier results, and receipts. Public evidence can summarize a verified claim while private proof remains access-controlled.

**Advantages**

- Preserves component ownership.
- Reduces disclosure.
- Supports public accountability without public exposure of private proof.
- Works offline.
- Supports tenant and cultural restrictions.
- Limits breach aggregation.
- Makes audit purpose and scope explicit.
- Supports recourse and correction.
- Avoids one universal evidence store.

**Disadvantages and costs**

- Requires evidence contracts and source adapters.
- Requires policy-aware selection and redaction.
- Requires careful verifier and receipt semantics.
- Some audits can remain blocked when required evidence is unavailable.
- Cross-source claims require coordination.
- Public evidence can disclose less detail than some requesters prefer.

**Constraint fit**

This option satisfies the decision drivers and preserves existing component, governance, gateway, and data boundaries.

### 6.2 Option B — Centralized complete audit log

**Description**

All components copy detailed events and supporting data into one central audit service.

**Advantages**

- Simple centralized querying.
- Uniform retention.
- Easier broad correlation.
- Familiar operational model.

**Disadvantages and costs**

- Creates a sensitive aggregation point.
- Duplicates authoritative data.
- Encourages direct broad access.
- Complicates tenant, consent, and cultural restrictions.
- Becomes a critical availability dependency.
- Increases retention and breach impact.
- Weakens component ownership.
- Makes public evidence separation difficult.

**Reason rejected**

The option conflicts with minimum disclosure, component ownership, sovereign operation, and selective recourse.

### 6.3 Option C — Component-local audit only

**Description**

Each component keeps its own evidence and no system-wide audit coordination exists.

**Advantages**

- Strong local ownership.
- Low central complexity.
- Limited aggregation.

**Disadvantages and costs**

- Cross-component claims are difficult to evaluate.
- Request authorization is inconsistent.
- Public evidence lacks a common contract.
- Recourse becomes component-specific.
- Release and profile conformance cannot aggregate reliably.
- Audit conclusions and receipts differ across components.

**Reason rejected**

Local custody is retained, but system-wide coordination and bounded verification remain necessary.

### 6.4 Option D — Public append-only ledger

**Description**

Publish audit events or proofs into a public or broadly accessible append-only ledger.

**Advantages**

- Strong public visibility.
- External verification.
- Durable event ordering.

**Disadvantages and costs**

- Public exposure can be irreversible.
- Metadata can identify protected people or relationships.
- Cultural and consent restrictions become difficult to enforce.
- Offline local correctness can depend on an external network.
- Corrections and revocation cannot erase harmful disclosure.
- The ledger can become a false source of semantic truth.

**Reason rejected**

Public permanence conflicts with selective disclosure, consent, cultural rights, and bounded retention.

### 6.5 Option E — AI-mediated audit

**Description**

An AI service receives broad logs and answers audit questions.

**Advantages**

- Flexible natural-language analysis.
- Potentially fast correlation.
- Lower manual query effort.

**Disadvantages and costs**

- Requires broad data disclosure.
- Produces probabilistic conclusions.
- Can omit or invent relationships.
- Introduces external or heavy local dependencies.
- Weakens reproducibility.
- Cannot own approval, truth, or evidence access.

**Reason rejected**

AI can assist bounded analysis but cannot be the audit authority or evidence gateway.

## 7. Decision

### 7.1 Selected option

`selective_audit_with_source_owned_private_proof_and_bounded_disclosure`

### 7.2 Core architecture

The selected architecture contains:

1. **Audit subject** — the deployment, component, artifact, operation, decision, or claim target.
2. **Audit request** — the bounded claim, purpose, requester, audience, scope, time range, and requested evidence classes.
3. **Audit authorization** — the decision that permits, denies, blocks, or requires human review.
4. **Evidence plan** — the exact evidence sources, fields, transformations, restrictions, and expected verification method.
5. **Private proof** — protected source evidence retained under its owning authority.
6. **Disclosure package** — the minimum derived evidence disclosed to the approved reviewer.
7. **Verifier result** — the evaluation of the claim against the disclosed evidence and applicable contracts.
8. **Audit receipt** — the immutable historical record of request, decision, sources, disclosure, verifier, result, limitations, and lifecycle.
9. **Public evidence** — an optional separately authorized representation suitable for a broader audience.
10. **Recourse record** — a dispute, correction, appeal, or remediation linked to the receipt.

### 7.3 Authority model

Authority remains separated:

- source components own their evidence;
- Identity and Trust owns identity, delegation, trust, and revocation results;
- Governance Policy Runtime evaluates audit access and obligations;
- Audit Broker coordinates but does not inherit source ownership;
- a human reviewer performs review where policy requires human judgment;
- a verifier evaluates the bounded claim;
- Publication Gateway mediates cross-domain publication of public evidence where required;
- Resource Governor controls capacity without deciding evidence authority;
- AI systems remain advisory.

### 7.4 Minimum-disclosure model

An audit disclosure is limited by:

- exact claim;
- exact purpose;
- exact requester;
- exact audience;
- exact subject;
- exact target scope;
- exact time range;
- exact evidence classes;
- exact fields or derived assertions;
- exact retention;
- exact redistribution policy;
- exact expiry;
- exact verifier.

Evidence unrelated to the claim remains undisclosed.

### 7.5 Public evidence and private proof

Public evidence is not the private proof itself.

A public evidence artifact can state:

- the claim evaluated;
- the verifier identity or class;
- the result;
- the relevant policy or contract references;
- the verification time;
- the validity period;
- bounded limitations;
- a receipt reference;
- a controlled recourse path.

It excludes protected source content, private identities, secrets, restricted cultural details, unrelated tenant data, and internal security details unless separate authority explicitly permits disclosure.

### 7.6 Historical truth

Audit receipts preserve:

- what was requested;
- what authority applied;
- what evidence was used;
- what was disclosed;
- what conclusion was reached;
- what limitations existed at that time.

A later revocation, correction, dispute, supersession, or remediation adds a new linked state. It does not erase the prior historical record or silently rewrite the original conclusion.

### 7.7 Fail-closed behavior

An audit remains blocked or incomplete when:

- requester identity cannot be validated;
- purpose is ambiguous;
- subject scope is ambiguous;
- authority is missing;
- evidence ownership is unresolved;
- required evidence is unavailable;
- evidence is stale or incompatible;
- minimization cannot be proven;
- required human review is incomplete;
- verifier compatibility cannot be established;
- time validity cannot be established;
- public disclosure authority is missing.

A blocked audit cannot be reported as passed.

## 8. Canonical Ownership and Data Boundaries

### 8.1 Audit Broker ownership

Audit Broker owns:

- audit-request coordination;
- request state;
- evidence-plan references;
- authorization references;
- disclosure-package references;
- verifier-result references;
- audit receipts;
- recourse references;
- audit lifecycle state.

Audit Broker does not own:

- component business data;
- identity master records;
- consent authority;
- cultural authority;
- publication source content;
- governance policy source;
- component databases;
- complete diagnostic payloads;
- release artifacts;
- source test observations.

### 8.2 Source-component ownership

Each source component owns:

- its authoritative records;
- its event semantics;
- its evidence-producing interface;
- its evidence retention;
- its evidence classification;
- its permitted derived assertions;
- its correction and supersession behavior.

Source evidence remains accessible through a bounded contract rather than direct database access.

### 8.3 Evidence registry ownership

`generated/evidence-catalog.json` owns evidence identity, type, subject, producer, scope, result, status, validity, restrictions, and lifecycle.

It can reference protected evidence without embedding the protected payload.

### 8.4 Traceability ownership

`generated/traceability.json` owns relationships among:

- decisions;
- requirements;
- locks;
- tests;
- evidence;
- profiles;
- components;
- artifacts;
- releases;
- audit receipts;
- exceptions;
- claims.

Audit Broker consumes traceability. It does not rewrite it.

### 8.5 Forbidden direct access

The architecture prohibits:

- audit clients querying component databases directly;
- Audit Broker writing component-authoritative data;
- public evidence containing private proof by default;
- administrators bypassing audit authorization;
- verifiers expanding the subject or time range;
- generated summaries becoming source evidence;
- AI systems selecting hidden evidence;
- one tenant’s audit exposing another tenant’s evidence;
- audit access becoming a reusable general-purpose credential.

### 8.6 Evidence transformations

Permitted evidence transformations include:

- field selection;
- aggregation;
- count or range derivation;
- identifier substitution;
- pseudonymization;
- redaction;
- time-window restriction;
- proof of policy presence;
- proof of test result;
- proof of receipt existence;
- proof of state transition;
- bounded correlation across referenced evidence.

Every transformation records its authority, input references, producer, output reference, and limitations.

## 9. Profile and Deployment Effects

| Profile or overlay | Audit effect | Required baseline |
| --- | --- | --- |
| `user_lightweight` | Local audit and recourse remain available without external telemetry. | Local receipts, bounded diagnostics, user-visible disclosure, offline export. |
| `developer_linux_workstation` | Workspace, toolchain, test, build, and candidate-artifact evidence remain workspace-scoped. | Isolated workspace evidence and no production-data assumption. |
| `developer_windows_wsl` | Windows and WSL evidence retains platform and boundary scope. | Host/distribution identity, path, port, service, and toolchain evidence. |
| `sovereign_linux_node` | Node lifecycle, backup, restore, update, identity, governance, and security evidence remain locally verifiable. | Offline evidence custody and controlled export. |
| `sovereign_hub` | Multi-tenant, network-zone, publication, federation, capacity, and recovery audits require tenant isolation. | Audit Broker, governance decision, selective evidence, recourse, and protected retention. |
| `build_farm` | Build, dependency, test, provenance, worker isolation, and candidate-artifact evidence remains scoped to the build environment. | Reproducibility and handoff evidence without production authority. |
| `control_plane` | Fleet and registry coordination evidence cannot replace local node evidence. | Bounded coordination receipts and node-verifiable claims. |
| `high_assurance` | Adds stronger reviewer separation, evidence protection, disclosure review, and retention controls. | Independent human review where required. |
| `sovereign_offline` | Sustained audit, support, recourse, evidence exchange, and verification work without online dependencies. | Local verifiers and removable-media or delayed exchange. |
| `appliance_shell` | Provides bounded user-facing audit status and recourse without exposing protected internals. | Local receipt presentation and controlled support export. |

Profile contracts select implementation mechanisms. They do not change evidence ownership or the minimum-disclosure rule.

## 10. Security, Privacy, Rights, and AI Effects

### 10.1 Security effects

Selective audit reduces broad read paths and centralized sensitive aggregation.

Security controls include:

- authenticated requesters;
- purpose-bound authorization;
- tenant and authority-domain filtering;
- field allowlists;
- bounded time ranges;
- rate and concurrency limits;
- verifier identity;
- protected evidence storage;
- short-lived access;
- audit of audit access;
- explicit expiry;
- revocation;
- safe handling of partial evidence;
- no secret disclosure.

### 10.2 Privacy effects

Audit is not blanket consent to inspect protected content.

Private proof remains private unless:

- the claim requires it;
- the requester is authorized;
- the disclosure is minimum-necessary;
- the audience and retention are explicit;
- the evidence owner and applicable policy permit it.

The system prefers derived assertions and evidence references over raw content.

### 10.3 Cultural-rights effects

Evidence involving cultural material, collective identity, protected attribution, sacred or restricted context, community authority, or culturally limited provenance uses the applicable cultural-rights policy.

A technically valid audit request can remain denied or require a competent human reviewer when cultural authority is absent or disputed.

Public evidence does not expose restricted cultural details merely to make the audit more persuasive.

### 10.4 Recourse effects

An affected person or authorized collective can:

- request the audit basis;
- inspect permitted evidence;
- challenge scope;
- challenge identity or attribution;
- submit correction evidence;
- request human review;
- appeal a conclusion;
- request remediation;
- receive a recourse receipt.

Recourse disclosure remains bounded by the rights of other affected parties.

### 10.5 AI effects

AI systems can:

- classify candidate evidence;
- prepare a bounded evidence plan;
- detect missing references;
- summarize disclosed evidence;
- compare a result with a contract;
- identify possible contradictions;
- prepare a human-review package.

AI systems cannot:

- authorize the audit;
- decide consent or cultural authority;
- expand evidence scope;
- determine the canonical truth;
- approve public disclosure;
- sign the audit conclusion as the sole authority;
- alter source evidence;
- suppress contradictory evidence;
- close recourse without the required authority.

AI output remains candidate analysis linked to its inputs and accepted only through the responsible audit or component workflow.

## 11. Offline, Resource, and Operational Effects

### 11.1 Offline behavior

Selective audit remains functional without:

- Internet access;
- public DNS;
- a remote control plane;
- cloud telemetry;
- external AI;
- public ledgers;
- remote identity providers where valid local identity material exists.

A local audit can use local policy, evidence references, verifiers, receipts, and removable-media exchange.

### 11.2 Queued audit work

Remote audit requests and disclosures can be queued only when the applicable contract permits it.

Queued work records:

- request identity;
- claim;
- subject;
- authority references;
- evidence plan;
- destination;
- expiry;
- cancellation state.

Reconnection triggers revalidation of identity, trust, consent, cultural authority, policy, evidence validity, destination, verifier, time, and conflict state.

### 11.3 Resource effects

Selective audit consumes bounded:

- evidence-query capacity;
- redaction and transformation capacity;
- verifier capacity;
- receipt storage;
- protected evidence retention;
- disclosure bandwidth;
- human review capacity.

Resource Governor can limit concurrency and queue depth. It cannot broaden evidence access or convert a blocked audit into a successful audit.

### 11.4 Observability

Operational observability exposes:

- request state;
- authorization state;
- evidence-source availability;
- disclosure preparation state;
- verifier state;
- receipt state;
- recourse state;
- expiry;
- blocked reasons;
- queue depth and age;
- failures and remediation.

Observability avoids protected payloads and secrets.

### 11.5 Backup and restore

Backup and restore preserve:

- evidence identities;
- source ownership;
- receipts;
- authorization references;
- disclosure references;
- verifier results;
- recourse;
- lifecycle state;
- retention and expiry.

Restore does not silently reactivate expired access or recreate deleted temporary disclosure packages beyond their authorized retention.

### 11.6 Exit

A deployment can export:

- its audit receipts;
- permitted evidence references;
- public evidence;
- private proof under applicable authority;
- verifier results;
- recourse history;
- retention and restriction metadata.

Exit preserves evidence restrictions and does not force public disclosure.

## 12. Compatibility and Lifecycle

### 12.1 Compatibility class

`breaking`

The decision rejects complete centralized audit-log assumptions and requires explicit claim, scope, authority, evidence ownership, and disclosure boundaries.

### 12.2 Affected release channels

The decision affects:

- `governance` — audit policy, evidence contracts, decision semantics, exceptions, and recourse;
- `services` — Audit Broker and source evidence interfaces;
- `system` — local storage, identity, networking, backup, and offline mechanisms;
- `knowledge` — evidence and provenance restrictions for knowledge artifacts where applicable.

The active Release Set binds compatible versions across the affected channels.

### 12.3 Artifact effects

The architecture requires or constrains artifacts for:

- audit requests;
- audit decisions;
- evidence plans;
- evidence references;
- disclosure packages;
- verifier results;
- audit receipts;
- public evidence;
- recourse;
- corrections;
- retention and deletion notices.

Artifact contracts define structure. This ADR defines the architecture and authority boundaries.

### 12.4 Lifecycle

Audit artifacts can use lifecycle states such as:

```text
requested
authorized
denied
blocked
collecting
ready_for_review
under_review
verified
not_verified
inconclusive
disputed
corrected
superseded
expired
closed
```

The exact state sets remain owned by their artifact and component contracts.

### 12.5 Version compatibility

An audit result remains scoped to:

- request version;
- evidence-contract version;
- source-component version;
- verifier version;
- governance-policy version;
- profile;
- topology;
- active Release Set;
- evidence validity period.

A later version does not inherit an earlier conclusion automatically.

## 13. Migration Plan

### 13.1 Preconditions

Migration requires:

- accepted `DEC-AUDIT-001`;
- registered Audit Broker component contract;
- evidence registry and schema;
- traceability registry and schema;
- audit artifact contracts;
- source-component evidence interfaces;
- selective-disclosure policies;
- retention and recourse policies;
- profile applicability;
- validation tests.

### 13.2 Source inventory

Inventory existing:

- application logs;
- audit logs;
- governance decisions;
- publication receipts;
- provenance records;
- identity and trust events;
- consent records;
- test evidence;
- release evidence;
- support bundles;
- incident records;
- migration logs;
- backup and restore evidence;
- external-provider receipts.

### 13.3 Classification

For each source, record:

- owner;
- subject;
- evidence type;
- sensitivity;
- tenant scope;
- authority domain;
- retention;
- current consumers;
- direct-access paths;
- disclosure risks;
- offline availability;
- compatibility and version.

### 13.4 Migration steps

1. Assign each source to its canonical owner.
2. Define bounded evidence interfaces.
3. Replace broad direct audit access with claim-scoped requests.
4. Register evidence identities and restrictions.
5. Define disclosure transformations.
6. Define verifier contracts.
7. Define audit receipts.
8. Define public-evidence views.
9. Define recourse and correction flows.
10. Disable obsolete broad credentials and routes.
11. Preserve historical evidence and source lineage.
12. validate profile, tenant, offline, and recovery behavior;
13. Activate the compatible Release Set.

### 13.5 Historical logs

Historical logs remain under their existing owner and retention obligations.

They can support a selective audit when:

- scope is explicit;
- evidence semantics are understood;
- integrity and provenance are sufficient for the claim;
- disclosure can be minimized;
- limitations are recorded.

Historical incompleteness is reported rather than repaired through inference.

## 14. Rollback and Forward Repair

### 14.1 Rollback triggers

Rollback or deactivation is required when:

- Audit Broker exposes broader data than authorized;
- evidence ownership becomes ambiguous;
- tenant isolation fails;
- public evidence includes protected proof;
- receipts omit material limitations;
- AI gains authorization or conclusion authority;
- offline operation loses local evidence custody;
- audit access becomes a general administrator path;
- source evidence is modified through the audit interface;
- verifier incompatibility produces false conclusions.

### 14.2 Rollback unit

The rollback unit includes:

- Audit Broker service version;
- governance policy version;
- evidence contracts;
- disclosure contracts;
- verifier contracts;
- source evidence adapters;
- profile integration;
- active Release Set references;
- migration and validation evidence.

Mixed incompatible audit semantics remain inactive.

### 14.3 Rollback procedure

1. Stop new audit disclosure.
2. Preserve existing receipts and historical evidence.
3. Revoke temporary access and credentials.
4. Disable affected evidence adapters.
5. Restore the last validated audit policy and service set.
6. Verify source-component ownership.
7. Verify tenant and disclosure isolation.
8. verify offline audit;
9. Record the rollback and affected claims.
10. Reopen disputed or invalid conclusions.

### 14.4 Forward repair

Forward repair is preferred when:

- historical receipts must remain;
- a disclosure package omitted a limitation;
- a verifier result needs correction;
- a policy reference changed;
- evidence mapping is incomplete;
- a source adapter can be narrowed without reverting unrelated capability.

Repair creates linked correction or supersession records. It does not rewrite prior historical facts silently.

## 15. Interfile Alignment Impact

### 15.1 Primary impact report

- `generated/impact/IMPACT-2026-08-03-DEC-AUDIT-001.json`

### 15.2 Canonical contracts affected

The decision affects:

- `generated/decision-index.json`;
- `generated/decision-index.json`;
- `generated/evidence-catalog.json`;
- `generated/traceability.json`;
- `generated/requirements-index.json`;
- `generated/assertion-index.json`;
- `generated/component-catalog.json`;
- `contracts/integration-types.contract.json`;
- `contracts/components/audit-broker.component.json`;
- audit-related artifact contracts;
- applicable profile contracts.

### 15.3 Documents affected

| Document | Effect |
| --- | --- |
| `01-constitution/10-selective-audit-and-recourse.md` | Establishes constitutional guarantees and recourse. |
| `01-constitution/12-cultural-rights-and-consent.md` | Constrains cultural and consent evidence. |
| `07-security/13-privacy-and-disclosure.md` | Defines disclosure boundaries. |
| `07-security/15-selective-audit.md` | Defines operational security controls. |
| `07-security/16-public-evidence-and-private-proof.md` | Defines the two-plane evidence model. |
| `07-security/17-cross-domain-publication.md` | Governs publication of public evidence. |
| `08-operations/12-incident-response.md` | Uses selective evidence for incidents. |
| `08-operations/15-support-and-diagnostics.md` | Uses bounded diagnostic disclosure. |
| `09-conformance/04-profile-test-matrices.md` | Binds evidence to profile claims. |
| `09-conformance/15-exceptions-and-waivers.md` | Requires visible, scoped deviation evidence. |
| `ADR-010` | Records this decision. |

### 15.4 Lock effects

Audit locks enforce:

- bounded claim and purpose;
- explicit authorization;
- source-owned evidence;
- no direct storage access;
- minimum disclosure;
- public/private evidence separation;
- historical receipt preservation;
- AI non-authority;
- offline audit;
- recourse.

Existing data, governance, component, gateway, offline, and AI locks remain controlling.

### 15.5 Generated artifacts

The decision causes generation or regeneration of:

- audit request and receipt catalogs;
- evidence-type indexes;
- evidence-to-claim traceability;
- profile audit matrices;
- selective-disclosure policy summaries;
- public-evidence catalogs;
- recourse indexes;
- impact reports;
- validation reports;
- scoped AI context.

## 16. Validation and Evidence

### 16.1 Required validation families

Validation covers:

- audit-request schema;
- exact claim and purpose;
- requester identity;
- subject and tenant scope;
- evidence ownership;
- governance decision;
- minimum field selection;
- redaction;
- public/private separation;
- verifier compatibility;
- audit receipt completeness;
- historical correction;
- recourse;
- expiry;
- offline operation;
- profile behavior;
- Release Set compatibility;
- AI boundary;
- removal and cleanup.

### 16.2 Required negative tests

Negative tests verify denial of:

- wildcard audit scope;
- unbounded time range;
- direct component database access;
- cross-tenant evidence;
- secret disclosure;
- public publication of private proof;
- use of expired authority;
- use of stale evidence;
- automatic reconnection release;
- AI authorization;
- AI-only canonical conclusion;
- receipt rewriting;
- hidden general administrator access;
- evidence reuse outside scope.

### 16.3 Evidence required for activation

Activation evidence includes:

- accepted `DEC-AUDIT-001`;
- accepted `ADR-010`;
- Audit Broker contract validation;
- evidence registry validation;
- source evidence-interface validation;
- governance policy tests;
- tenant-isolation tests;
- disclosure minimization tests;
- public/private separation tests;
- offline tests;
- recourse tests;
- profile matrices;
- Release Set compatibility;
- rollback rehearsal;
- impact report.

### 16.4 Decision-specific checks

Decision-specific checks confirm:

1. Audit Broker owns coordination and receipts, not component data.
2. Every audit request declares claim, purpose, requester, subject, scope, and time range.
3. Every disclosed field is required for the claim.
4. Every source evidence reference resolves to an owner.
5. Every audit has an authorization result.
6. Every verifier result is scoped and versioned.
7. Public evidence excludes protected private proof by default.
8. Historical receipts remain unchanged after correction or revocation.
9. Recourse can reference and challenge the original receipt.
10. Offline audit can collect, verify, exchange, and close without Internet.
11. AI remains advisory.
12. The active Release Set contains compatible governance, service, system, and knowledge versions.

### 16.5 Acceptance criteria

This ADR is accepted and active when:

1. `DEC-AUDIT-001` is accepted.
2. `ADR-010` is registered.
3. Audit Broker boundaries are canonical.
4. Evidence ownership is explicit.
5. Audit artifacts are schema-valid.
6. Selective-disclosure policies are active.
7. Public evidence and private proof are contractually distinct.
8. Required profile tests pass.
9. Negative disclosure and bypass tests pass.
10. Offline audit tests pass.
11. Recourse tests pass.
12. Complete impact and traceability validation passes.
13. The compatible Release Set activates last.

## 17. Consequences

### 17.1 Positive consequences

- Accountability no longer requires broad surveillance.
- Component data ownership remains intact.
- Public verification becomes possible without exposing private proof.
- Tenant and cultural restrictions remain enforceable.
- Audit requests become purpose-bound.
- Recourse receives a stable historical basis.
- Offline deployments remain auditable.
- Conformance and release evidence becomes reusable within exact scope.
- AI assistance remains bounded.
- Evidence access and conclusion authority remain separate.

### 17.2 Negative consequences and costs

- Evidence interfaces must be designed per component.
- Cross-source audits require coordination.
- Some audits can remain inconclusive.
- Redaction and minimization require testing.
- Public evidence can appear less detailed.
- Human review remains necessary for sensitive claims.
- Historical evidence quality can limit conclusions.
- Receipt, recourse, and correction lifecycles add complexity.
- Selective access policies require maintenance.

### 17.3 Operational obligations

Operators maintain:

- evidence retention;
- evidence-source health;
- Audit Broker availability;
- verifier compatibility;
- policy and identity validity;
- disclosure-package cleanup;
- expiry;
- recourse;
- backup and restore;
- offline export and import;
- audit of audit access.

### 17.4 Technical debt explicitly accepted

The decision accepts:

- multiple evidence stores;
- bounded manual review;
- heterogeneous source evidence formats behind normalized contracts;
- possible inconclusive results;
- delayed cross-source verification while offline.

These costs are preferred to broad centralization and unauthorized disclosure.

## 18. Rejected Alternatives

| Alternative | Rejection reason | Reconsideration trigger |
| --- | --- | --- |
| Central complete audit log | Aggregates protected data and weakens ownership. | No trigger under current sovereignty and minimization principles. |
| Component-local audit without broker | Cannot support consistent cross-component claims and recourse. | No trigger while system-wide conformance and publication proof remain required. |
| Public ledger | Creates irreversible metadata and content disclosure risks. | No trigger for protected operational evidence. |
| Administrator-wide audit access | Turns audit into privilege escalation. | None. |
| AI-mediated audit authority | Probabilistic analysis cannot own authorization or canonical truth. | None. |
| Public evidence identical to private proof | Violates selective disclosure. | None. |
| Audit through direct database queries | Violates component boundaries. | None. |
| Online-only evidence service | Breaks sovereign and offline operation. | None. |

## 19. Exceptions and Waivers

No active exception or waiver applies to this ADR.

A future deviation:

- uses `schemas/exception.schema.json`;
- names exact audit subjects and claims;
- identifies affected evidence classes and owners;
- preserves non-waivable component ownership, historical truth, human approval, and AI non-authority;
- remains expiring and visible;
- cannot authorize unrestricted evidence access;
- cannot make public evidence identical to private proof;
- cannot convert missing evidence into a verified claim;
- cannot authorize cross-tenant or cross-component direct storage access.

A material architecture change requires a new accepted decision and superseding ADR.

## 20. Implementation Guidance

Implementation guidance is non-authoritative unless adopted by an active contract.

Recommended practices include:

1. Prefer evidence references over payload copies.
2. Prefer source-side derived assertions when they satisfy the claim.
3. Use allowlisted fields and bounded time windows.
4. Keep audit credentials short-lived and case-specific.
5. Store disclosure packages separately from source evidence.
6. Delete temporary packages at expiry while retaining required receipts.
7. Present disclosure summaries before human approval.
8. Record omitted evidence categories and limitations.
9. Use deterministic redaction where practical.
10. Keep verifier inputs reproducible.
11. Expose recourse instructions with public evidence.
12. Treat audit access as a protected operation.
13. Keep source adapters read-only.
14. Test cross-tenant denial explicitly.
15. Maintain local offline verifiers for essential claims.
16. Avoid public identifiers that permit re-identification through correlation.
17. Keep AI prompts and outputs inside the approved evidence scope.
18. Record human acceptance when AI assists analysis.

## 21. Decision Record

### 21.1 Decision authority

- Decision ID: `DEC-AUDIT-001`
- Decision status: `accepted`
- Decision owner: `audit_architecture_owner`
- Decision registry: `generated/decision-index.json`
- ADR registry: `generated/decision-index.json`
- ADR ID: `ADR-010`

### 21.2 Review record

| Role | Identifier | Result | Date |
| --- | --- | --- | --- |
| Author | `audit_architecture_owner` | `submitted` | `2026-08-03` |
| Canonical owner | `audit_architecture_owner` | `approved` | `2026-08-03` |
| Governance reviewer | `governance_architecture_review` | `approved` | `2026-08-03` |
| Privacy and rights reviewer | `privacy_and_rights_review` | `approved` | `2026-08-03` |
| Security reviewer | `security_architecture_review` | `approved` | `2026-08-03` |
| Validation pipeline | `automated` | `pass` | `2026-08-03` |
| Authority activator | `documentation_authority_activator` | `activated` | `2026-08-03` |

### 21.3 Machine-readable change summary

```json
{
  "change_id": "CHG-2026-0010",
  "decision_ids": [
    "DEC-AUDIT-001"
  ],
  "modified_canonical_refs": [
    "generated/decision-index.json",
    "generated/decision-index.json",
    "generated/evidence-catalog.json",
    "generated/traceability.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/component-catalog.json",
    "contracts/integration-types.contract.json",
    "contracts/components/audit-broker.component.json"
  ],
  "affected_document_ids": [
    "ADR-010",
    "DOC-CONST-010",
    "DOC-CONST-012",
    "DOC-SEC-013",
    "DOC-SEC-014",
    "DOC-SEC-015",
    "DOC-SEC-016",
    "DOC-SEC-017",
    "DOC-OPS-012",
    "DOC-OPS-015",
    "DOC-CONF-004",
    "DOC-CONF-015"
  ],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-AUDIT-001",
    "LOCK-AUDIT-002",
    "LOCK-AUDIT-003",
    "LOCK-AUDIT-004",
    "LOCK-AUDIT-005",
    "LOCK-AUDIT-006",
    "LOCK-AUDIT-007",
    "LOCK-AUDIT-008",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-GATE-001",
    "LOCK-OFFLINE-001",
    "LOCK-AI-001",
    "LOCK-AI-002"
  ],
  "exception_ids": [],
  "adr_ids": [
    "ADR-010"
  ],
  "impact_report": "generated/impact/IMPACT-2026-08-03-DEC-AUDIT-001.json",
  "validation_status": "pass"
}
```

## 22. Supersession and Historical Integrity

When this ADR is superseded:

1. `generated/decision-index.json` marks `ADR-010` as superseded.
2. The replacement ADR records `ADR-010` in its `supersedes` relationship.
3. `ADR-010` records the replacement through `superseded_by`.
4. The identifier and path remain reserved.
5. Historical authority releases preserve the period in which this ADR was active.
6. Audit receipts created under this decision remain historically valid within their original scope.
7. Later policy or contract changes do not rewrite earlier receipts.
8. Invalid or disputed historical conclusions receive linked correction, supersession, or recourse records.
9. Generated ADR, evidence, and impact indexes are regenerated.
10. AI contexts stop treating this ADR as current after the replacement activates.
11. Migration records preserve the relationship between prior and replacement evidence semantics.
12. Protected evidence remains governed by its retention and disclosure restrictions after supersession.

Accepted, rejected, deprecated, superseded, and archived ADRs remain historical records and are not deleted.
