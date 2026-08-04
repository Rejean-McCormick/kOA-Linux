<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ADR-007",
  "document_class": "adr",
  "status": "accepted",
  "language": "en",
  "layer": "architecture_decision",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/decision-index.json",
    "generated/component-catalog.json",
    "contracts/components/kristal-runtime.component.json",
    "generated/profile-catalog.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "contracts/artifact-contracts/runtime-pack.schema.json",
    "contracts/artifact-contracts/decision-receipt.schema.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-SYS-KRISTAL-001",
    "DEC-DATA-001",
    "DEC-AI-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-COMP-KRISTAL-001",
    "REQ-COMP-KRISTAL-002",
    "REQ-COMP-KRISTAL-003",
    "REQ-COMP-KRISTAL-004",
    "REQ-COMP-KRISTAL-005",
    "REQ-COMP-KRISTAL-006",
    "REQ-COMP-KRISTAL-007",
    "REQ-COMP-KRISTAL-008",
    "REQ-COMP-KRISTAL-009",
    "REQ-COMP-KRISTAL-010",
    "REQ-COMP-KRISTAL-011",
    "REQ-COMP-KRISTAL-012",
    "REQ-CONST-COMP-009",
    "REQ-SYS-DATA-017"
  ],
  "lock_ids": [
    "LOCK-COMP-001",
    "LOCK-DATA-001",
    "LOCK-AI-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-004",
    "DOC-GOV-005",
    "DOC-GOV-009",
    "DOC-GOV-010",
    "DOC-CONST-007",
    "DOC-SYS-005",
    "DOC-PROFILE-001",
    "DOC-COMP-000",
    "DOC-COMP-KRISTAL-001",
    "DOC-LIFE-002",
    "DOC-LIFE-012",
    "DOC-SEC-004",
    "DOC-SEC-015",
    "DOC-CONF-002",
    "DOC-CONF-007"
  ],
  "tags": [
    "architecture-decision",
    "kristal",
    "epistemic-foundation",
    "transversal",
    "runtime-pack",
    "knowledge-channel",
    "component-separation",
    "offline-knowledge",
    "provenance",
    "portable-identity"
  ]
}
KOA:DOC-META:END -->

# ADR-007 — Kristal as a Transversal Foundation

**ADR ID:** `ADR-007`  
**Status:** `accepted`  
**Decision class:** `major`  
**Decision owner:** `system-architecture`  
**Owner decision:** `DEC-SYS-KRISTAL-001`  
**Historical source status:** `Accepted`  
**Canonicalized:** `2026-08-03`  
**Original acceptance date:** Not recorded in the retained source  
**Supersedes:** Not applicable  
**Superseded by:** Not applicable

## 1. Decision Summary

Kristal is adopted as a transversal epistemic foundation across build, governance, distribution, and runtime planes. It provides portable epistemic identity, provenance, validation, recognition, federation, offline query artifacts, verified Runtime Pack consumption, and recoverable runtime activation. Kristal does not become a universal workflow engine, universal operational database, shared component state store, policy authority, resource authority, privilege broker, release authority, or external artificial-intelligence service.

## 2. Scope

### 2.1 Included scope

This decision applies globally to:

- Kristal content identity and epistemic artifact semantics;
- Kristal Runtime and its active component contract;
- Runtime Packs and other registered Kristal artifacts;
- the `knowledge` release channel;
- build-time production and verification of Kristal artifacts;
- distribution, offline transfer, federation, and runtime consumption;
- provenance, trust, compatibility, activation, rollback, and evidence;
- every component and profile that explicitly consumes Kristal artifacts.

### 2.2 Excluded scope

This decision does not assign:

- profile membership for Kristal Runtime;
- application workflow state;
- component business data;
- user-interface state;
- universal query access to component-owned records;
- governance-policy decisions;
- resource scheduling;
- privileged host operations;
- release-channel ownership;
- native or external artificial-intelligence processing;
- publication authority.

### 2.3 Activation boundary

The decision applies when an active component, profile, artifact contract, or release definition references Kristal identity, Kristal artifacts, Kristal Runtime, or Runtime Packs. Actual runtime membership remains controlled by the effective profile and component contracts.

## 3. Canonical References

### 3.1 Owner decision

- `generated/decision-index.json`
- `DEC-SYS-KRISTAL-001`

### 3.2 Canonical objects changed or constrained

- `generated/component-catalog.json`
- `contracts/components/kristal-runtime.component.json`
- `contracts/artifact-contracts/runtime-pack.schema.json`
- `contracts/release-channels.contract.json`
- `contracts/artifact-classes.contract.json`
- `generated/profile-catalog.json`

### 3.3 Related documents

- `DOC-CONST-007` — `01-constitution/07-component-separation.md`
- `DOC-SYS-005` — `02-system/05-data-authority-and-ownership.md`
- `DOC-COMP-000` — `04-components/00-component-model.md`
- `DOC-COMP-KRISTAL-001` — `04-components/kristal-runtime.md`
- `DOC-LIFE-002` — `06-lifecycle/02-release-model.md`
- `DOC-LIFE-012` — `06-lifecycle/12-artifact-verification.md`

### 3.4 Related requirements

- `REQ-COMP-KRISTAL-001` through `REQ-COMP-KRISTAL-012`
- `REQ-CONST-COMP-009`
- `REQ-SYS-DATA-017`

### 3.5 Related locks

- `LOCK-COMP-001`
- `LOCK-DATA-001`
- `LOCK-AI-001`
- `LOCK-LIFE-001`
- `LOCK-LIFE-002`
- `LOCK-LIFE-003`
- `LOCK-LIFE-004`

### 3.6 Related exceptions

Not applicable.

## 4. Context and Problem

### 4.1 Current state

kOA contains several components and deployment profiles that need consistent epistemic identity, provenance, validation, recognition, federation, distribution, and offline knowledge behavior.

Without a shared foundation, each component could invent its own content identity, provenance shape, validation semantics, federation model, and portable knowledge format. Those parallel definitions would make equivalent knowledge difficult to compare, transfer, verify, restore, or consume across component and deployment boundaries.

Kristal already exists in the retained architecture as a transversal epistemic foundation. The current component model also provides a narrow Kristal Runtime boundary for verified Runtime Packs.

### 4.2 Problem statement

The architecture needs a common epistemic layer without creating a central operational component that absorbs application workflow, business state, governance, resource control, or data ownership.

The same mechanism that reduces semantic duplication could become an architectural bottleneck or authority collapse if Kristal were treated as:

- the workflow engine for every application;
- the database for every component;
- the owner of tenant or user state;
- a universal integration bus;
- an automatic artificial-intelligence layer;
- the authority deciding which artifacts or content become operational state.

### 4.3 Why a decision is required

This boundary affects system architecture, component ownership, data authority, profiles, release channels, artifact contracts, offline behavior, security, lifecycle, and conformance.

A local implementation choice cannot safely determine whether Kristal is a shared foundation or a universal operational system. The distinction requires one accepted global decision and explicit alignment locks.

### 4.4 Constraints

The decision remains within these constraints:

- every component retains exclusive logical ownership of its authoritative data;
- cross-component direct writes remain prohibited;
- the native system baseline contains no artificial-intelligence authority;
- profile membership remains explicit;
- the four release channels remain independent;
- Runtime Packs belong to the `knowledge` release channel;
- publication, installation, verification, staging, and activation remain distinct;
- activation remains atomic within the Kristal Runtime owner boundary;
- the last valid Runtime Pack remains recoverable;
- offline verification and use remain possible;
- resource-consuming work remains bounded;
- receipts and evidence do not become mutation authority.

## 5. Decision Drivers

1. Preserve one portable epistemic identity and provenance model across products and deployment forms.
2. Prevent semantic duplication without collapsing component data and workflow ownership.
3. Support offline verification, distribution, query artifacts, restoration, and credible exit.
4. Preserve strict component boundaries and explicit contracts.
5. Keep runtime activation recoverable and independently verifiable.
6. Avoid native artificial-intelligence dependence.
7. Keep profile membership and assurance requirements explicitly scoped.
8. Allow future federation without creating universal operational storage.

## 6. Considered Options

### 6.1 Option A — Transversal epistemic foundation with narrow runtime ownership

**Description**

Kristal defines common epistemic identity, provenance, validation, recognition, federation, and portable artifacts. Kristal Runtime owns only content-identity resolution, Runtime Pack verification and compatibility state, active Runtime Pack selection, activation state, receipts, and runtime health.

Components consume Kristal outputs through declared contracts and decide independently whether candidate content becomes component-owned state.

**Advantages**

- reduces semantic duplication;
- supports portable and offline knowledge artifacts;
- preserves component data ownership;
- supports one verified Runtime Pack lifecycle;
- permits multiple consumers without shared operational state;
- allows bounded federation and exit;
- remains independent from artificial intelligence.

**Disadvantages and costs**

- requires explicit contracts between Kristal and every consumer;
- requires artifact, release, trust, compatibility, and receipt discipline;
- prevents convenient direct access to consumer databases;
- requires owners to distinguish epistemic identity from workflow and interface state;
- creates additional conformance and lifecycle tests.

**Constraint fit**

This option satisfies the global component-separation, data-authority, artificial-intelligence, release, and lifecycle constraints.

### 6.2 Option B — Separate epistemic model inside every component

**Description**

Every application and service defines its own knowledge identity, provenance, validation, federation, and offline artifact behavior.

**Advantages**

- maximizes local implementation freedom;
- reduces the number of shared contracts;
- permits component-specific optimization.

**Disadvantages and costs**

- duplicates semantics and validation;
- makes cross-component equivalence unreliable;
- complicates offline transfer and restoration;
- increases migration and integration costs;
- weakens portable provenance and federation;
- creates inconsistent trust and lifecycle behavior.

**Reason rejected**

The option fails the need for a transversal portable epistemic foundation and would recreate incompatible knowledge models across components.

### 6.3 Option C — Kristal as universal workflow engine and operational database

**Description**

Kristal becomes the central workflow engine, common operational database, event state owner, and universal query layer for every component.

**Advantages**

- centralizes implementation;
- permits one operational query surface;
- can simplify some cross-application workflows;
- can reduce short-term integration work.

**Disadvantages and costs**

- destroys component data authority;
- creates direct or hidden cross-component coupling;
- makes Kristal a single operational bottleneck;
- conflates epistemic identity with mutable workflow state;
- broadens security and privacy impact;
- complicates profile-specific deployment;
- increases migration and recovery blast radius;
- encourages universal schemas and access.

**Reason rejected**

The option violates component separation, data ownership, safe degradation, profile scope, and recoverability.

## 7. Decision

### 7.1 Selected option

`transversal_epistemic_foundation_with_narrow_runtime_ownership`

### 7.2 Normative effect

The accepted architecture:

- retains Kristal as a global transversal foundation;
- establishes Kristal Runtime as a first-class but narrow component;
- assigns Runtime Packs and Kristal artifacts to the `knowledge` release channel;
- preserves component-owned workflow and business state;
- requires explicit consumer contracts and acceptance;
- requires independent identity, integrity, provenance, trust, compatibility, authorization, resource, and lifecycle checks;
- prohibits universal operational ownership.

### 7.3 Required behavior

Implementations and canonical documentation preserve:

- content-derived or contract-defined epistemic identity independent from tenant workflow and interface state;
- verified immutable Kristal artifacts;
- explicit provenance and trust context;
- profile-scoped runtime membership;
- consumer-owned acceptance of candidate content;
- atomic Runtime Pack activation;
- last-valid-state preservation;
- bounded resource use;
- machine-readable verification and transition receipts;
- offline-capable validation and consumption where the profile declares it.

### 7.4 Prohibited behavior

The architecture excludes:

- universal workflow execution by Kristal;
- universal operational database ownership;
- storage of every component's mutable state in Kristal;
- direct writes to consumer-owned data;
- implicit profile inclusion;
- Runtime Pack activation from an unverified candidate;
- Runtime Pack use through the wrong release channel;
- implicit downgrade or artifact substitution;
- partial authoritative activation;
- native artificial-intelligence dependence;
- treating a receipt or successful signature as application acceptance.

### 7.5 Defaults

No global profile-membership default is introduced. Each profile explicitly declares Kristal Runtime as required, optional, or absent.

The default architectural interpretation is that Kristal artifacts are candidate inputs to a consumer until the consumer accepts them through its own contract.

### 7.6 Failure and safe-degradation behavior

When Kristal identity, trust, artifact integrity, compatibility, authorization, resource admission, or profile membership cannot be established, the affected new operation remains blocked.

An existing valid Runtime Pack remains active when a candidate fails verification or activation. Optional consumers can remain unavailable without invalidating unrelated consumers or component-owned state. Recovery uses rollback to the last valid pack or an explicitly declared forward-repair state.

## 8. Canonical Ownership and Data Boundaries

### 8.1 Canonical owner

- Owner decision: `DEC-SYS-KRISTAL-001`
- Component boundary: `contracts/components/kristal-runtime.component.json`
- Artifact format: `contracts/artifact-contracts/runtime-pack.schema.json`
- Release-channel identity: `contracts/release-channels.contract.json`
- Profile membership: `contracts/profiles/*.profile.json`

### 8.2 Produced authoritative data

Kristal Runtime owns only:

- Kristal content-identity resolution records;
- Runtime Pack verification records;
- Runtime Pack compatibility state;
- active Runtime Pack record;
- activation and rollback state;
- runtime health state;
- component-owned transition receipts before evidence custody transfer.

### 8.3 Consumed authoritative data

Kristal Runtime consumes through contracts:

- artifact identity and class definitions;
- Runtime Pack manifests and payloads;
- release-channel membership;
- profile membership and overlays;
- trust and revocation context;
- policy decisions when a governed transition requires them;
- resource-admission decisions;
- Release Set and compatibility context;
- consumer requests.

### 8.4 Forbidden direct access

Kristal and Kristal Runtime do not:

- write directly to another component's database, schema, table, object namespace, files, or private queue;
- read unrestricted component-private state to construct universal views;
- bypass Publication Gateway or another declared gateway;
- assume host privilege;
- mutate policy or resource authority;
- control another component's workflow.

### 8.5 Gateways and contracts

Required boundaries include:

- Kristal Runtime component interfaces;
- Runtime Pack artifact contract;
- release-channel and Release Set contracts;
- Identity and Trust verification;
- Governance Policy Runtime where a governed transition applies;
- Resource Governor admission;
- Audit Broker or active evidence authority for custody;
- explicit consumer commands, events, imports, or artifact acceptance.

## 9. Profile and Deployment Effects

| Profile or overlay | Effect | Conformance impact |
| --- | --- | --- |
| `user_lightweight` | Membership is selected only by its profile contract; the ADR adds no implicit requirement. | Validate declared membership, bounded resources, offline behavior, and consumer boundaries. |
| `developer_linux_workstation` | Can build, test, validate, and consume Kristal artifacts when declared. | Development isolation does not change Kristal authority. |
| `developer_windows_wsl` | Can build, test, validate, and consume Kristal artifacts when declared. | Equivalent contract behavior is required without assuming Linux-only paths. |
| `sovereign_linux_node` | Can use verified local Runtime Packs and offline artifacts when declared. | Offline verification, recovery, trust, and evidence receive profile-owned controls. |
| `sovereign_hub` | Can distribute or federate Kristal artifacts when declared. | Distribution does not create universal application state ownership. |
| `build_farm` | Can produce and verify Kristal artifacts and Runtime Packs. | Build provenance does not grant runtime activation authority. |
| `control_plane` | Can coordinate catalog, release, or fleet information when declared. | Control-plane state does not replace node-local activation authority. |
| `high_assurance` | Adds only explicitly composed trust, custody, approval, and evidence requirements. | The overlay can strengthen verification but cannot broaden Kristal ownership. |
| `sovereign_offline` | Adds explicitly composed offline custody, transfer, and synchronization controls. | Local operation remains possible without trusting embedded new roots automatically. |
| `appliance_shell` | Changes user-interface deployment only when composed. | It does not change Kristal identity, data ownership, or Runtime Pack semantics. |

## 10. Security, Privacy, Rights, and AI Effects

### 10.1 Security effects

Runtime Packs and Kristal artifacts use class-specific integrity, provenance, trust, compatibility, authorization, and activation checks.

Artifact signing trust remains scoped to the `knowledge` release channel and declared artifact classes. A valid signature does not establish application acceptance, policy authorization, or component mutation authority.

Kristal Runtime retains the last valid pack and rejects unverified execution, unauthorized downgrade, and substitution.

### 10.2 Privacy and disclosure effects

Portable epistemic artifacts can contain classified or rights-constrained content. Their artifact contracts and consumer workflows define allowed fields, audiences, retention, export, and disclosure.

Kristal's transversal role does not create universal read access. Public receipts can prove bounded outcomes without exposing private proof or consumer-owned content.

### 10.3 Cultural rights and consent effects

Kristal can preserve provenance, rights, consent, use restrictions, and withdrawal relationships when their active artifact and domain contracts define them.

Kristal does not decide cultural-rights or consent policy. A receiving component accepts content only after the applicable rights and policy conditions pass.

### 10.4 AI-boundary effects

This decision introduces no native artificial-intelligence capability.

Kristal identity resolution, Runtime Pack verification, activation, rollback, federation, and offline query behavior remain deterministic and independent from external artificial-intelligence services.

Any externally generated candidate content remains a candidate input with provenance until an authoritative consumer accepts it.

## 11. Offline, Resource, and Operational Effects

### 11.1 Offline behavior

Kristal supports portable epistemic identity, provenance, validation, distribution, federation, and query artifacts without requiring Internet access.

Offline profiles use previously trusted roots, local artifact verification, local Runtime Pack activation, bounded local evidence, and later reconciliation where declared.

### 11.2 Resource envelope

Kristal build, validation, indexing, federation, query, and activation work consumes bounded CPU, memory, storage, input-output, concurrency, queue, and retry budgets.

The Resource Governor controls admission where required. The ADR introduces no unbounded background indexing or universal ingestion obligation.

### 11.3 Observability

Operational signals include:

- active Runtime Pack identity and version;
- verification state;
- activation state;
- health and work-class readiness;
- compatibility failure;
- trust and channel failure;
- rollback or forward-repair state;
- bounded resource and queue state;
- verification, activation, rollback, and failure receipts.

Signals do not become artifact or workflow authority.

### 11.4 Backup, restore, and exit

Backup and export preserve:

- Kristal artifacts;
- Runtime Pack manifests and payloads;
- provenance and verification records;
- active-pack identity;
- required receipts;
- consumer-owned acceptance relationships where applicable.

Restore verifies artifacts and compatibility before activation. Portable artifacts and explicit contracts support independent exit without requiring a universal proprietary database.

### 11.5 Incident and recovery behavior

Artifact, trust, compatibility, or activation incidents preserve the current valid pack where safe.

Recovery can:

- reject or quarantine a candidate;
- restore the last valid pack;
- revoke affected trust;
- withdraw an artifact;
- replace a Runtime Pack;
- enter forward repair;
- revalidate dependent consumers.

Incident response does not modify consumer databases through Kristal Runtime.

## 12. Compatibility and Lifecycle

### 12.1 Compatibility class

`conditionally_compatible`

The decision is compatible with components that keep operational ownership and consume Kristal through contracts. It is incompatible with designs that assign universal workflow or operational database authority to Kristal.

### 12.2 Affected release channels

- `knowledge`

The `system`, `services`, and `governance` channels remain independent. Their artifacts can reference Kristal artifacts through explicit compatibility relationships without changing channel ownership.

### 12.3 Artifact and schema effects

Affected artifacts and contracts include:

- Runtime Packs;
- registered Kristal artifact classes;
- Release Sets that bind compatible knowledge artifacts;
- provenance and verification receipts;
- activation and rollback receipts;
- offline bundles containing Kristal artifacts;
- Kristal Runtime component contracts.

### 12.4 Deprecation effects

Any design or document that treats Kristal as a universal workflow engine, universal operational database, or replacement for component-owned data is incompatible and requires removal, migration, or supersession.

No canonical identifier is deprecated by this retained decision record.

### 12.5 Identifier preservation

`ADR-007` and `DEC-SYS-KRISTAL-001` remain reserved.

Future semantic replacement uses new decision and ADR identifiers with explicit `supersedes` and `superseded_by` relationships. Historical artifact, requirement, test, evidence, and authority records retain their original identifiers.

## 13. Migration Plan

### 13.1 Preconditions

- the retained deprecated ADR is classified as accepted;
- `DEC-SYS-KRISTAL-001` exists as the owner decision;
- the Kristal Runtime component boundary is defined;
- Runtime Pack and release-channel contracts are available;
- related requirements, locks, tests, and evidence are registered.

### 13.2 Migration steps

1. Retain the deprecated architectural intent under `ADR-007`.
2. Register the ADR and owner decision in the canonical registries.
3. Align component, data, profile, artifact, release, security, lifecycle, and conformance objects.
4. Preserve or redirect the deprecated path.
5. Regenerate ADR indexes, component catalogs, artifact catalogs, traceability matrices, impact reports, and AI contexts.
6. Run complete validation.
7. Activate the exact validated registry versions last.

### 13.3 deprecated disposition

The removed source file:

`doc/08-adrs/ADR-007-kristal-transversal-epistemic-foundation.md`

is retained and adapted into:

`docs/10-adrs/ADR-007-kristal-as-transversal-foundation.md`

The original three-part context, decision, and consequence statement remains the historical basis. The expanded ADR adds explicit ownership, profile, security, lifecycle, migration, validation, and evidence boundaries without changing the selected architecture.

### 13.4 Redirects and compatibility period

The migration path registry retains a permanent historical redirect from the deprecated ADR path to the canonical ADR path.

## 14. Rollback and Forward Repair

### 14.1 Rollback trigger

Rollback or containment is required when an implementation activated under this ADR:

- creates universal workflow or database ownership;
- introduces cross-component direct writes;
- activates an unverified Runtime Pack;
- uses the wrong release channel;
- breaks recoverability;
- makes artificial intelligence a runtime prerequisite;
- broadens profile membership implicitly.

### 14.2 Rollback unit

The rollback unit contains the complete aligned set of:

- owner decision and ADR version;
- Kristal Runtime component contract;
- Runtime Pack artifact contract;
- affected profile declarations;
- release and compatibility declarations;
- requirements and locks;
- generated projections and AI contexts;
- active Runtime Pack pointer where runtime state is affected.

### 14.3 Rollback procedure

1. Block new incompatible transitions and preserve evidence.
2. Restore the last valid canonical authority set and compatible Runtime Pack state.
3. Remove or disable unauthorized direct dependencies.
4. Revalidate component-owned data and consumer contracts.
5. Regenerate projections and record rollback evidence.

### 14.4 Forward repair

Forward repair is preferred when operational data or artifact history has already been created under a newer compatible contract and reverting would lose valid provenance or accepted consumer state.

Forward repair introduces a corrected component, artifact, profile, or migration contract while preserving historical identities and evidence.

### 14.5 Last known valid state

- Authority manifest: the last active validated entry in `generated/authority-manifest.json`
- Release Set: the last compatible active Release Set for the affected target
- Runtime state: the last verified compatible active Runtime Pack record

## 15. Interfile Alignment Impact

### 15.1 Impact report


### 15.2 Modified canonical references

Initial canonical registration affects:

- `generated/decision-index.json`
- `generated/decision-index.json`
- `generated/component-catalog.json`
- `contracts/components/kristal-runtime.component.json`
- `contracts/artifact-classes.contract.json`
- `contracts/release-channels.contract.json`
- `generated/traceability.json`

### 15.3 Affected documents

| Document ID | Disposition | Reason |
| --- | --- | --- |
| `DOC-CONST-007` | `reviewed_no_change` | Already preserves Kristal as transversal without universal ownership. |
| `DOC-SYS-005` | `reviewed_no_change` | Already prohibits Kristal as universal operational storage or workflow state. |
| `DOC-COMP-000` | `reviewed_no_change` | Component model already preserves the narrow runtime boundary. |
| `DOC-COMP-KRISTAL-001` | `reviewed_no_change` | Component responsibilities and exclusions already implement this decision. |
| `DOC-LIFE-002` | `reviewed_no_change` | Release model already assigns knowledge artifacts and Runtime Packs correctly. |
| `DOC-LIFE-012` | `reviewed_no_change` | Verification model already separates verification from activation. |

### 15.4 Affected locks

| Lock ID | Disposition | Validation effect |
| --- | --- | --- |
| `LOCK-COMP-001` | `unchanged` | Preserves component separation and narrow ownership. |
| `LOCK-DATA-001` | `unchanged` | Prohibits direct cross-component writes and universal data ownership. |
| `LOCK-AI-001` | `unchanged` | Preserves the no-native-AI baseline. |
| `LOCK-LIFE-001` | `unchanged` | Preserves release-channel separation. |
| `LOCK-LIFE-002` | `unchanged` | Preserves verification before activation. |
| `LOCK-LIFE-003` | `unchanged` | Preserves atomic activation and last-valid state. |
| `LOCK-LIFE-004` | `unchanged` | Preserves rollback or forward repair and blocks substitution. |

### 15.5 Affected requirements

| Requirement set | Disposition | Validation effect |
| --- | --- | --- |
| `REQ-COMP-KRISTAL-001..012` | `unchanged` | Defines runtime ownership, artifact, lifecycle, profile, AI, and evidence behavior. |
| `REQ-CONST-COMP-009` | `unchanged` | Preserves the transversal foundation without operational authority collapse. |
| `REQ-SYS-DATA-017` | `unchanged` | Prohibits universal operational database and workflow-state use. |

### 15.6 Generated artifacts

Canonical activation requires regeneration of:

- ADR index;
- decision index;
- document index;
- requirements index;
- locks index;
- component catalog;
- artifact catalog;
- release-channel matrix;
- traceability matrix;
- profile test matrix;
- system and profile AI context packages.

## 16. Validation and Evidence

### 16.1 Required tests

| Test ID | Purpose | Required result |
| --- | --- | --- |
| `TEST-COMP-KRISTAL-001` | Validate component-contract identity, ownership, and canonical references. | `pass` |
| `TEST-COMP-KRISTAL-002` | Validate independence of Kristal identity from workflow and interface state. | `pass` |
| `TEST-COMP-KRISTAL-003` | Reject universal workflow and operational database ownership. | `pass` |
| `TEST-COMP-KRISTAL-004` | Reject cross-component direct writes. | `pass` |
| `TEST-COMP-KRISTAL-005` | Validate Runtime Pack identity, digest, provenance, trust, and compatibility. | `pass` |
| `TEST-COMP-KRISTAL-006` | Validate `knowledge` channel membership and replacement policy. | `pass` |
| `TEST-COMP-KRISTAL-007` | Validate atomic activation and last-valid-state recovery. | `pass` |
| `TEST-COMP-KRISTAL-008` | Validate no-native-AI behavior and critical receipt traceability. | `pass` |

### 16.2 Required evidence

| Evidence ID | Evidence type | Subject |
| --- | --- | --- |
| `EVID-COMP-KRISTAL-001` | Component-contract validation | Kristal Runtime identity and ownership |
| `EVID-COMP-KRISTAL-002` | Boundary validation | Epistemic identity independence |
| `EVID-COMP-KRISTAL-003` | Negative ownership validation | Universal workflow and database rejection |
| `EVID-COMP-KRISTAL-004` | Data-boundary validation | No direct cross-component writes |
| `EVID-COMP-KRISTAL-005` | Artifact verification evidence | Runtime Pack validation |
| `EVID-COMP-KRISTAL-006` | Release evidence | Knowledge-channel and replacement policy |
| `EVID-COMP-KRISTAL-007` | Lifecycle evidence | Atomic activation and recovery |
| `EVID-COMP-KRISTAL-008` | AI and traceability evidence | No-native-AI and receipts |

### 16.3 Required validation commands

```bash
python docs/tools/generate_docs.py --check
python docs/tools/check_normative_language.py
python docs/tools/check_language.py
python docs/tools/check_canonical_ownership.py
python docs/tools/check_interfile_locks.py
python docs/tools/check_generated_content.py
python docs/tools/check_document_graph.py
python docs/tools/check_traceability.py
python docs/tools/check_decision_closure.py
python docs/tools/check_no_unresolved_state.py
python docs/tools/compute_impact.py --check-clean
python docs/tools/build_ai_context.py --check
python docs/tools/check_clean_repository.py
python docs/tools/validate_docs.py
```

### 16.4 Decision-specific validation

Decision-specific validation covers:

- one active Kristal canonical owner;
- narrow Kristal Runtime data ownership;
- no universal workflow or database ownership;
- no cross-component direct writes;
- profile membership resolution;
- Runtime Pack identity, integrity, provenance, trust, and compatibility;
- `knowledge` release-channel membership;
- atomic activation;
- last-valid-state preservation;
- unauthorized downgrade and substitution rejection;
- no-native-AI operation;
- critical receipt traceability;
- offline verification where the profile declares it.

### 16.5 Acceptance criteria

1. The owner decision and ADR both resolve as accepted.
2. Kristal remains transversal across relevant planes without owning application workflow or business state.
3. Kristal Runtime owns only the records declared in its component contract.
4. Runtime Packs validate and activate through the `knowledge` channel.
5. Consumer components retain independent acceptance and data ownership.
6. Offline and recoverable operation remains possible where profiles declare it.
7. All eight decision-specific tests pass and all eight evidence items resolve.
8. Every affected object receives a final impact disposition.
9. The active authority index references the exact validated canonical versions.

## 17. Consequences

### 17.1 Positive consequences

- one portable epistemic identity and provenance model;
- less semantic duplication;
- consistent Runtime Pack verification and activation;
- improved offline knowledge integrity;
- clearer federation and transfer boundaries;
- preserved component autonomy;
- stronger portability and credible exit;
- narrower security and recovery blast radius than a universal database;
- deterministic operation without artificial-intelligence dependence.

### 17.2 Negative consequences and costs

- more explicit contracts and adapters;
- additional artifact and lifecycle validation;
- consumer-specific acceptance workflows;
- duplicated operational projections where components need local views;
- no universal ad hoc query across all component state;
- ongoing discipline to prevent boundary erosion.

### 17.3 Operational obligations

Operators maintain:

- valid Runtime Packs;
- trust and revocation context;
- compatibility evidence;
- resource bounds;
- last-valid-state recovery;
- receipts and evidence;
- offline transfer and restore procedures where applicable.

### 17.4 Documentation obligations

Maintainers keep the owner decision, ADR, component contract, data-boundary documents, artifact contracts, release definitions, profiles, requirements, locks, tests, evidence, and generated contexts aligned.

### 17.5 Technical debt explicitly accepted

Consumer-specific mappings and acceptance adapters can duplicate some transformation work. This debt is accepted to preserve component ownership and can be reduced only through shared non-authoritative libraries or artifact conventions that do not create universal state authority.

## 18. Rejected Alternatives

| Alternative | Reason rejected | Reconsideration trigger |
| --- | --- | --- |
| Component-local epistemic models only | Creates semantic duplication and weakens portable provenance, federation, and offline restore. | Reconsider only if no cross-component or portable epistemic behavior remains in scope. |
| Universal Kristal workflow engine | Collapses component workflow ownership and creates broad coupling. | None under the current constitutional component-separation model. |
| Universal Kristal operational database | Violates logical data ownership and increases security and recovery blast radius. | None under the current data-authority model. |
| External artificial-intelligence service as the epistemic core | Violates deterministic local and offline operation and introduces external authority dependence. | None under the current AI boundary. |
| Artifact library without a runtime boundary | Cannot provide verified atomic Runtime Pack selection, health, rollback, and recovery. | Reconsider only if Runtime Pack activation is removed from the architecture. |

Rejected alternatives require a new accepted owner decision and superseding ADR before implementation.

## 19. Exceptions and Waivers

Not applicable.

A future exception cannot change Kristal's canonical ownership or create universal workflow, database, or direct-write authority. Such a semantic change requires a new accepted owner decision and a superseding ADR.

## 20. Implementation Guidance

This section is non-normative.

Useful implementation patterns include:

- content-addressed or canonical-content-derived identities;
- immutable Runtime Pack directories or object graphs;
- a single active-pack pointer switched atomically;
- separate verification and activation records;
- consumer-specific import or query adapters;
- read-only runtime access to pack payloads;
- bounded indexes and caches;
- offline manifests and verification material;
- explicit provenance and compatibility receipts;
- separate operational databases for consuming components.

Implementations should prefer shared libraries for parsing and verification over shared mutable operational state.

## 21. Decision Record

### 21.1 Decision authority record

- Decision ID: `DEC-SYS-KRISTAL-001`
- Decision status: `accepted`
- Decision owner: `system-architecture`
- Decision registry reference: `generated/decision-index.json`
- ADR registry reference: `generated/decision-index.json`

Supporting decisions:

- `DEC-DATA-001`
- `DEC-AI-001`
- `DEC-REL-001`

### 21.2 Review record

| Role | Identifier | Result | Date |
| --- | --- | --- | --- |
| Historical ADR source | `doc/08-adrs/ADR-007-kristal-transversal-epistemic-foundation.md` | `accepted` | Original date not recorded |
| Reconciliation authority | `reconciliation-reference` | `retained_global` | Source record retained |
| Canonical owner | `system-architecture` | `accepted` | Historical decision |
| Local structural validation | `automated` | `pass` | `2026-08-03` |
| Canonical registry activation | `authority-registry` | `pending_registration` | `2026-08-03` |

### 21.3 Machine-readable change summary

```json
{
  "change_class": "retained_legacy_decision",
  "decision_ids": [
    "DEC-SYS-KRISTAL-001",
    "DEC-DATA-001",
    "DEC-AI-001",
    "DEC-REL-001"
  ],
  "modified_canonical_refs": [
    "generated/decision-index.json",
    "generated/decision-index.json",
    "generated/component-catalog.json",
    "contracts/components/kristal-runtime.component.json",
    "contracts/artifact-contracts/runtime-pack.schema.json",
    "generated/traceability.json"
  ],
  "affected_document_ids": [
    "DOC-ADR-007",
    "DOC-CONST-007",
    "DOC-SYS-005",
    "DOC-COMP-000",
    "DOC-COMP-KRISTAL-001",
    "DOC-LIFE-002",
    "DOC-LIFE-012"
  ],
  "requirement_ids": ["REQ-COMP-KRISTAL-001", "REQ-COMP-KRISTAL-002", "REQ-COMP-KRISTAL-003", "REQ-COMP-KRISTAL-004", "REQ-COMP-KRISTAL-005", "REQ-COMP-KRISTAL-006", "REQ-COMP-KRISTAL-007", "REQ-COMP-KRISTAL-008", "REQ-COMP-KRISTAL-009", "REQ-COMP-KRISTAL-010", "REQ-COMP-KRISTAL-011", "REQ-COMP-KRISTAL-012", "REQ-CONST-COMP-009", "REQ-SYS-DATA-017"],
  "lock_ids": ["LOCK-COMP-001", "LOCK-DATA-001", "LOCK-AI-001", "LOCK-LIFE-001", "LOCK-LIFE-002", "LOCK-LIFE-003", "LOCK-LIFE-004"],
  "exception_ids": [],
  "adr_ids": [
    "ADR-007"
  ],
  "test_ids": ["TEST-COMP-KRISTAL-001", "TEST-COMP-KRISTAL-002", "TEST-COMP-KRISTAL-003", "TEST-COMP-KRISTAL-004", "TEST-COMP-KRISTAL-005", "TEST-COMP-KRISTAL-006", "TEST-COMP-KRISTAL-007", "TEST-COMP-KRISTAL-008"],
  "evidence_ids": ["EVID-COMP-KRISTAL-001", "EVID-COMP-KRISTAL-002", "EVID-COMP-KRISTAL-003", "EVID-COMP-KRISTAL-004", "EVID-COMP-KRISTAL-005", "EVID-COMP-KRISTAL-006", "EVID-COMP-KRISTAL-007", "EVID-COMP-KRISTAL-008"],
  "impact_report": null,
  "local_validation_status": "pass",
  "canonical_registry_status": "pending_registration"
}
```

## 22. Supersession and Historical Integrity

When this ADR is superseded:

1. its status changes to `superseded`;
2. `superseded_by` references the replacement ADR;
3. the replacement ADR references `ADR-007` through `supersedes`;
4. the original identifier and path remain reserved;
5. historical decisions, migration sources, impact reports, validation evidence, artifact evidence, and authority manifests remain available;
6. generated indexes and AI contexts are regenerated;
7. active contexts stop treating this ADR as current authority after replacement activation.

This ADR remains preserved after acceptance, deprecation, rejection of a future replacement, or supersession.
