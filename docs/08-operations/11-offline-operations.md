<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-OPS-011",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "operations",
  "scope": [
    "global",
    "profile_overlay:sovereign_offline"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/offline_behavior",
    "contracts/system.contract.json#/safe_degradation",
    "contracts/system.contract.json#/health_and_readiness",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/profiles/sovereign-offline.profile.json",
    "contracts/artifact-classes.contract.json",
    "contracts/artifact-contracts/offline-bundle.schema.json",
    "contracts/artifact-contracts/resource-envelope.schema.json",
    "contracts/artifact-contracts/decision-receipt.schema.json",
    "contracts/integration-types.contract.json",
    "contracts/release-channels.contract.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "contracts/integrations/uckk-import.integration.json",
    "contracts/artifact-contracts/shared-mediatheque-frame.schema.json",
    "contracts/artifact-contracts/uckk-learning-package.schema.json",
    "contracts/artifact-contracts/uckk-import-receipt.schema.json",
    "04-components/uckk-import-bridge.md"
  ],
  "decision_ids": [
    "DEC-PROFILE-001",
    "DEC-PROFILE-BASELINE-001",
    "DEC-COMP-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-GATE-001",
    "DEC-REL-001",
    "DEC-AI-001",
    "DEC-SENT-001",
    "DEC-ARI-001",
    "DEC-MEDIATHEQUE-001",
    "DEC-UCKK-EXT-001",
    "DEC-DEV-001",
    "DEC-DEV-002"
  ],
  "requirement_ids": [
    "REQ-OPS-OFF-001",
    "REQ-OPS-OFF-002",
    "REQ-OPS-OFF-003",
    "REQ-OPS-OFF-004",
    "REQ-OPS-OFF-005",
    "REQ-OPS-OFF-006",
    "REQ-OPS-OFF-007",
    "REQ-OPS-OFF-008",
    "REQ-OPS-OFF-009",
    "REQ-OPS-OFF-010",
    "REQ-OPS-OFF-011",
    "REQ-OPS-OFF-012",
    "REQ-OPS-OFF-013",
    "REQ-OPS-OFF-014",
    "REQ-OPS-OFF-015",
    "REQ-OPS-OFF-016",
    "REQ-OPS-OFF-017",
    "REQ-OPS-OFF-018",
    "REQ-OPS-OFF-019",
    "REQ-OPS-OFF-020",
    "REQ-OPS-OFF-021",
    "REQ-OPS-OFF-022",
    "REQ-OPS-OFF-023",
    "REQ-OPS-OFF-024",
    "REQ-OPS-OFF-025",
    "REQ-OPS-OFF-026",
    "REQ-OPS-OFF-027",
    "REQ-OPS-OFF-028",
    "REQ-OPS-OFF-029",
    "REQ-OPS-OFF-030",
    "REQ-OPS-OFF-031",
    "REQ-OPS-OFF-032",
    "REQ-UCKK-IMPORT-001",
    "REQ-UCKK-IMPORT-002",
    "REQ-UCKK-IMPORT-003",
    "REQ-UCKK-IMPORT-004",
    "REQ-UCKK-IMPORT-005",
    "REQ-UCKK-IMPORT-006"
  ],
  "lock_ids": [
    "LOCK-OPS-001",
    "LOCK-OPS-002",
    "LOCK-OPS-003",
    "LOCK-OPS-004",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-SEC-001",
    "LOCK-SEC-002",
    "LOCK-SEC-003",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SENT-001",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-MEDIATHEQUE-002",
    "LOCK-UCKK-EXT-001",
    "LOCK-DEV-001",
    "LOCK-DEV-004",
    "LOCK-UCKK-EXT-002"
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
    "DOC-SYS-020",
    "DOC-PRO-000",
    "DOC-LIFE-001",
    "DOC-LIFE-011",
    "DOC-SEC-003",
    "DOC-SEC-014",
    "DOC-OPS-002",
    "DOC-OPS-004",
    "DOC-OPS-005",
    "DOC-OPS-006",
    "DOC-OPS-007",
    "DOC-OPS-008",
    "DOC-OPS-009",
    "DOC-OPS-010",
    "DOC-COMP-UCKK-IMPORT-001"
  ],
  "tags": [
    "offline-operations",
    "disconnected-operation",
    "offline-continuity",
    "local-authority",
    "synchronization",
    "conflict-resolution",
    "outbox",
    "replay-protection",
    "offline-bundles",
    "recovery",
    "sovereign-offline",
    "import-from-uckk",
    "offline-learning"
  ]
}
KOA:DOC-META:END -->

# Offline Operations

## 1. Purpose

This document defines the operational model for running kOA when network connectivity is absent, intermittent, restricted, intentionally disabled, or insufficient for a required remote dependency.

Offline operation is a planned operating state rather than an emergency assumption.

It preserves local authority and deterministic capability only where the active profile, component contracts, trust state, policy state, data state, resource envelope, and recovery model support that capability.

The model distinguishes:

- connected operation;
- transition into disconnection;
- verified offline operation;
- offline limited operation;
- offline recovery;
- reconnection;
- staged synchronization;
- conflict review;
- return to connected readiness.

The core principle is:

`text
offline continuity
 means
declared local capability under verified local authority

offline continuity
 does not mean
permission to guess missing authority or claim remote completion
`

A node can remain useful while disconnected without pretending that every connected feature remains available.

Examples include:

- local Konnaxion reads and approved local mutations;
- Orgo critical workflow execution with valid local conditions;
- Kristal Runtime queries from verified local packs;
- SemantiK Architect Runtime operation from compiled local language packs;
- Ariane deterministic local navigation;
- native deterministic kOA Mediatheque ingestion and processing;
- local backup, restore preparation, health, and recovery;
- queueing of permitted outbound intent.

The offline baseline has no dependency on native AI.

ChatGPT, Suno, Gamma, external Ariane voice, and other approved external surfaces remain external integrations. Their absence does not replace local authority or disable unrelated deterministic local operation.

## 2. Scope

This document applies to profiles and overlays that declare offline behavior, including the `sovereign_offline` overlay and compatible sovereign node, sovereign hub, control-plane, development, test, and recovery compositions.

It applies to:

- first-class components;
- local runtimes;
- nodes and hubs;
- workspaces;
- workers and jobs;
- databases;
- queues and outboxes;
- replay ledgers;
- health and readiness;
- identity and trust;
- governance policy;
- cultural rights and consent;
- publication intent;
- synchronization;
- artifact import;
- offline bundles;
- release-channel updates;
- backup and restore;
- recovery;
- evidence and receipts;
- external integration loss.

It covers operation during:

`text
connected
disconnecting
offline_verified
offline_limited
offline_recovering
reconnecting
synchronizing
conflict_review
connected_verified
`

The exact state identifiers, transition commands, timers, network interfaces, media devices, trust values, retention periods, storage paths, and synchronization protocols belong to active profile, component, integration, artifact, and operations contracts.

This document does not:

- make every profile offline-capable;
- require an air gap for every sovereign deployment;
- define one universal synchronization protocol;
- define one universal conflict-resolution algorithm;
- turn an offline bundle into an activation authority;
- permit direct database replication across component ownership boundaries;
- authorize a component to reuse another component's queue or replay ledger;
- convert cached information into current information;
- replace required human, community, or governance decisions with local guesses.

## 3. Canonical References

| Canonical reference | Responsibility |
| --- | --- |
| `contracts/system.contract.json#/offline_behavior` | Global offline states, capability declaration, authority preservation, synchronization, and reconnection model. |
| `contracts/system.contract.json#/safe_degradation` | Lower-authority operation, fail-closed conditions, optional dependency isolation, and recovery rules. |
| `contracts/system.contract.json#/health_and_readiness` | Local liveness, capability readiness, freshness, queue, external dependency, and recovery health. |
| `contracts/profiles/sovereign-offline.profile.json` | Offline overlay requirements, local dependencies, trust, time, storage, recovery, synchronization, and evidence. |
| `contracts/profiles/*.profile.json` | Profile membership, topology, network, resource, storage, policy, trust, health, and startup behavior. |
| `generated/component-catalog.json` | Component identity, data ownership, dependencies, offline applicability, and first-class boundaries. |
| `contracts/components/*.component.json` | Per-capability offline behavior, commands, queries, queues, receipts, conflicts, degradation, and recovery. |
| `contracts/artifact-classes.contract.json` | Artifact-class identity, import, staging, activation, rollback, repair, and retention. |
| `contracts/artifact-contracts/offline-bundle.schema.json` | Signed transport envelope, quarantine, replay, payload, compatibility, confidentiality, and result structure. |
| `contracts/artifact-contracts/resource-envelope.schema.json` | Offline resource limits, queues, storage, pressure, degradation, health, and recovery. |
| `contracts/artifact-contracts/decision-receipt.schema.json` | Bounded operation, policy, synchronization, activation, and recovery receipts. |
| `contracts/release-channels.contract.json` | Independent system, services, governance, and knowledge release channels. |
| `contracts/integration-types.contract.json` | Connectivity, peer, external service, publication, AI, voice, synchronization, and transfer boundaries. |
| `generated/test-catalog.json` | Disconnect, continuity, queue, conflict, bundle, reconnection, recovery, and negative-path tests. |
| `generated/evidence-catalog.json` | Offline conformance, queue, conflict, synchronization, backup, restore, activation, and recovery evidence. |
| `generated/requirements-index.json` | Normative statements displayed in Section 5. |
| `generated/assertion-index.json` | Operations, profile, component, data, lifecycle, security, gateway, AI, Ariane, kOA Mediatheque, UCKK publication, and development invariants. |
| `generated/traceability.json` | Links among profiles, capabilities, requirements, tests, evidence, queues, artifacts, and this document. |
| `generated/exception-index.json` | Approved bounded deviations and compensating controls. |

A runtime observation or local cache does not override these canonical owners.

## 4. Model and Responsibilities

### 4.1 Offline operating states

The shared operating model uses these conceptual states:

| State | Meaning |
| --- | --- |
| `connected` | Required online peers and integrations are available, but connected readiness has not necessarily been freshly verified. |
| `disconnecting` | The node is preparing local state, draining unsafe remote work, recording queue checkpoints, and validating offline prerequisites. |
| `offline_verified` | Declared local capabilities have valid local contracts, trust, policy, data, resources, health, and recovery prerequisites. |
| `offline_limited` | Local operation remains safe only for a declared subset or lower-authority mode. |
| `offline_recovering` | Local repair, restore, queue reconciliation, trust repair, or artifact repair is in progress. |
| `reconnecting` | Network availability has returned, but remote identity, trust, time, peers, and destinations are still being verified. |
| `synchronizing` | Bounded inbound and outbound exchange is running through declared component and lifecycle interfaces. |
| `conflict_review` | One or more authoritative conflicts require deterministic or governed resolution. |
| `connected_verified` | Required connected peers, queues, trust, policy, artifacts, conflicts, and evidence have been reconciled for declared connected capabilities. |

A node can move from `reconnecting` back to `offline_verified` when the remote side cannot be trusted or synchronization cannot proceed safely.

Physical link state and operational state remain separate.

### 4.2 Offline capability declaration

Every offline-capable component declares each capability as one of:

- authoritative local;
- authoritative local with freshness limit;
- read-only local;
- advisory-only local;
- queueing-only;
- recovery-only;
- unavailable.

The declaration identifies:

- capability identity;
- local dependencies;
- required identity and trust state;
- required policy and consent state;
- required data and schema state;
- resource envelope;
- queue and outbox behavior;
- freshness limits;
- denied operations;
- conflict behavior;
- synchronization owner;
- recovery requirements.

A component with no valid offline declaration remains unavailable while disconnected.

### 4.3 Local dependency set

An offline claim identifies the local dependencies needed for each capability.

Examples include:

- local storage;
- component database;
- local identity verification;
- local trust roots and revocation state;
- local Governance Policy Runtime where required;
- local resource enforcement;
- local audit or evidence storage;
- active component contract;
- active policy bundle;
- active artifact or Runtime Pack;
- local queue and replay ledger;
- trusted local time;
- backup or recovery material;
- profile-required hardware or service.

Public DNS, a public time service, remote telemetry, ChatGPT, Suno, Gamma, external Ariane voice, or an optional remote search service is not a local dependency unless a profile explicitly and validly defines that capability as online-only.

### 4.4 Entry prerequisites

Before a node reports `offline_verified`, it checks:

- active profile and overlays;
- component membership;
- active contracts;
- data ownership;
- local identities;
- trust roots and trust epoch;
- revocation freshness;
- trusted time;
- active governance policies;
- cultural-rights and consent evidence needed locally;
- schema and migration state;
- active artifact identities;
- local storage integrity and capacity;
- queue, outbox, and replay integrity;
- resource envelopes;
- health and readiness;
- backup and recovery material;
- expected external capability loss;
- evidence storage.

A missing prerequisite narrows the capability claim or keeps the node in `offline_limited`.

### 4.5 Identity and trust while offline

Offline verification uses locally trusted state.

The result identifies:

- identity;
- credential;
- issuer;
- relying context;
- audience;
- validity;
- local trust epoch;
- local revocation state;
- trusted time source;
- freshness;
- confidence;
- permitted reuse;
- reason.

High-impact actions can require newer trust or revocation state than low-risk local reads.

A trust update imported while offline follows its dedicated artifact transition. It does not validate the same unverified envelope that carried it.

### 4.6 Trusted local time

Offline time has security and lifecycle effects.

The node records:

- wall-clock source;
- monotonic source;
- last verified synchronization;
- drift estimate;
- confidence;
- manual adjustment history;
- hardware clock state;
- time rollback detection;
- effect on credentials;
- effect on policy validity;
- effect on consent expiry;
- effect on bundle validity;
- effect on retention;
- effect on leases and queued work.

A monotonic clock can preserve ordering and duration even when wall-clock confidence is reduced.

A wall-clock uncertainty is reported rather than silently corrected from an untrusted source.

### 4.7 Policy, consent, and cultural rights

The offline node uses only locally verified policies and evidence.

For a governed action, it resolves:

- actor and authority;
- subject owner;
- active policy identity;
- consent identity and scope;
- cultural-rights policy;
- action;
- purpose;
- audience;
- obligations;
- freshness;
- offline behavior.

An action that requires current external authority remains blocked.

Withdrawal, consent revocation, or policy updates received later can affect queued or synchronized work according to the owning component's reconciliation contract.

Local offline operation does not weaken cultural-rights requirements.

### 4.8 Local reads

A local read can continue when:

- source ownership is known;
- data integrity is valid;
- schema is compatible;
- applicable access and cultural-rights decisions are valid;
- freshness is exposed;
- the requested representation is locally available;
- the component contract permits offline reads.

A locally cached projection does not appear current without its source snapshot, calculation or artifact identity, observation time, and freshness.

### 4.9 Local authoritative mutations

A local mutation can continue only when the complete local authority set is available.

The operation normally includes:

1. authenticated local actor context;
2. active component contract;
3. current target version;
4. component-local authorization;
5. Governance Policy Runtime decision where required;
6. consent and cultural-rights checks where applicable;
7. storage and schema readiness;
8. optimistic concurrency;
9. request idempotency;
10. transactional local commit;
11. transactional outbox or equivalent;
12. local receipt;
13. synchronization intent.

A mutation is not permitted merely because the database accepts writes.

### 4.10 Queue classes

Offline operation can use separate bounded queues for:

- component events;
- publication intents;
- synchronization exports;
- artifact result returns;
- audit events;
- external integration requests;
- notifications;
- backups;
- maintenance work;
- conflict review;
- retryable local work.

Each queue identifies:

- owner;
- item schema;
- authority class;
- durability;
- maximum items and bytes;
- maximum age;
- ordering;
- priority;
- retry;
- expiry;
- overflow behavior;
- dead-letter behavior;
- evidence;
- cleanup.

One generic queue does not erase component or operation authority.

### 4.11 Transactional outbox

An outbox records work that follows an authoritative local transition.

The local transition and outbox record commit atomically.

The outbox item includes:

- event or command identity;
- source component;
- source record and version;
- destination contract;
- purpose;
- payload identity;
- policy and consent context;
- delivery constraints;
- retry and expiry;
- correlation;
- local receipt.

Outbox delivery does not transfer source data ownership.

### 4.12 Replay ledger

The replay ledger protects high-impact and non-idempotent work.

It can record:

- request identity;
- bundle identity;
- object identity;
- issuer;
- target;
- sequence;
- epoch;
- nonce;
- transaction identity;
- first seen;
- reservation;
- completion;
- result receipt;
- supersession;
- conflict;
- recovery state.

A replay ledger is durable and included in recovery.

Loss of the replay ledger can block operations whose safe repetition cannot be established.

### 4.13 Retry and backoff

Retry policy is operation-specific.

Retryable work uses:

- idempotency;
- stable request identity;
- bounded attempts or bounded age;
- exponential, linear, or fixed backoff;
- jitter where appropriate;
- destination health;
- queue quotas;
- explicit failure result.

Non-idempotent work uses reconciliation before repetition.

Examples include migrations, trust updates, restore activation, publication completion, and conflict resolution.

### 4.14 Outbound intent versus remote completion

The following states remain distinct:

`text
prepared locally
queued locally
submitted to transport
received by peer
accepted by peer
executed by peer
verified locally
`

A local publication intent is not a completed publication.

A local synchronization package is not accepted remote state.

An external AI request queued offline has produced no provider result.

An offline result bundle copied to media has not been reconciled by the receiving authority.

### 4.15 Synchronization session

A synchronization session identifies:

- local and peer identities;
- component or lifecycle owner;
- session identity;
- trust and policy state;
- supported contract versions;
- source and destination versions;
- object inventory;
- deletion representation;
- consent and cultural-rights context;
- replay state;
- conflict strategy;
- quotas;
- interruption behavior;
- receipts.

Synchronization can occur over a verified network peer or through an offline bundle.

The same ownership and conflict rules apply to both transports.

### 4.16 Version and conflict model

The owning component defines its version model.

It can use:

- record versions;
- revision identifiers;
- causal metadata;
- source snapshots;
- append-only events;
- checkpoints;
- domain-specific merge rules;
- governed review.

A conflict record preserves:

- object identity;
- base version;
- local version;
- remote version;
- actor and authority;
- provenance;
- policy and consent context;
- time confidence;
- receipts;
- candidate resolutions.

The system does not discard one side because its wall-clock value is later.

### 4.17 Conflict classes

Common conflict classes include:

- concurrent edits;
- edit versus withdrawal;
- edit versus deletion;
- policy change versus queued action;
- consent withdrawal versus queued export;
- schema mismatch;
- trust-epoch mismatch;
- artifact-version mismatch;
- duplicate external result;
- incompatible state transition;
- migration boundary conflict;
- identity or authority conflict.

The owning component determines whether the conflict can be:

- rejected;
- deterministically merged;
- transformed;
- replayed;
- compensated;
- escalated to authority review;
- kept as parallel records;
- resolved through forward repair.

### 4.18 Inbound quarantine

Inbound artifacts, bundles, synchronization packages, trust updates, and result bundles enter quarantine.

Quarantine remains:

- non-authoritative;
- non-executable;
- bounded;
- isolated;
- denied ordinary component writes;
- denied unrestricted network access;
- independently cleaned;
- evidence-aware.

Envelope verification does not accept payloads.

Payload verification does not stage them.

Staging does not activate them.

Importing synchronized records does not make them authoritative until the owning component accepts them.

### 4.19 Four release channels

Offline release delivery preserves:

- `system`;
- `services`;
- `governance`;
- `knowledge`.

Each channel keeps independent:

- artifact identities;
- signers;
- approvals;
- compatibility;
- staging;
- activation;
- rollback;
- revocation;
- receipts.

A Release Set binds tested identities without combining channel authority.

A knowledge-only update can proceed independently when compatibility passes.

A system image does not activate a governance policy by implication.

### 4.20 Artifact and policy activation

Offline artifact activation follows the artifact class.

Acceptance checks include the applicable:

- identity and signature;
- trust scope;
- revocation;
- profile;
- compatibility;
- data schema;
- migration;
- resource;
- health;
- policy;
- rollback;
- forward repair;
- evidence.

A policy bundle imported offline remains inactive until policy activation.

Existing decisions keep the policy identity used when they were made.

### 4.21 External integrations

Offline status is explicit per integration.

Examples include:

| Integration | Offline behavior |
| --- | --- |
| ChatGPT | Unavailable; requests can remain local candidate intents only when a contract permits queueing. |
| Suno | Unavailable; the local kOA Mediatheque remains deterministic and no provider substitute is selected. |
| Gamma | Unavailable; local content remains local and no provider substitute is selected. |
| Ariane external voice | Unavailable; local deterministic Ariane navigation remains available. |
| Remote publication destination | Publication intent can queue when permitted; completed publication is not claimed. |
| Remote identity provider | Local verification can continue only through profile-approved local trust and cached evidence. |
| Remote telemetry | Local health and evidence remain available; missing telemetry does not define local failure. |
| Remote search | Local source data remains authoritative; search capability reports its own state. |
| SenTient | Available only when the profile includes a local isolated workbench; otherwise absent without core impact. |

An external integration does not become local authority by being cached.

### 4.22 Ariane, language, and knowledge

Ariane local navigation uses verified local artifacts and component contracts.

SemantiK Architect Runtime uses compiled local PGF and language packs.

Kristal Runtime uses verified local Runtime Packs.

Loss of connectivity does not cause runtime grammar compilation, remote model substitution, or loss of local navigation.

Knowledge freshness and pack identity remain visible.

### 4.23 kOA Mediatheque and queued UCKK publication

kOA Mediatheque operation remains deterministic and local. UCKK publication is optional, external, and may be queued while disconnected.

Offline native capabilities can include:

- local source ingestion;
- local metadata under declared rules;
- deterministic derivatives;
- local playback or presentation;
- local export preparation;
- backup and restore;
- queued publication or external candidate intent.

Suno and Gamma output cannot be produced locally by an undeclared substitute.

External candidates retain provenance and require controlled re-import and user approval.

### 4.24 Health and readiness

Offline health identifies:

- operating state;
- local liveness;
- local-read readiness;
- local-write readiness;
- policy readiness;
- trust freshness;
- time confidence;
- storage state;
- queue state;
- replay state;
- resource state;
- synchronization state;
- external integration state;
- recovery state;
- denied operations.

A disconnected network link alone does not make the node unhealthy.

A full outbound queue, stale trust state, missing policy, or failed storage can make affected capabilities limited or unavailable.

### 4.25 Storage and capacity

Offline operation depends on bounded local storage.

The profile accounts for:

- authoritative component data;
- service state;
- queues;
- outboxes;
- replay ledgers;
- receipts;
- logs;
- private evidence;
- quarantine;
- staging;
- backups;
- restore staging;
- conflict records;
- outbound bundles;
- inbound bundles;
- temporary data;
- caches.

High-water and critical-water behavior preserves authoritative data and required evidence.

Replaceable caches are evicted before authoritative state.

### 4.26 Backup and restore

Offline backup records:

- source owner;
- source resources;
- snapshot state;
- schema;
- contract;
- policy and cultural-rights context;
- encryption recipient;
- integrity;
- creation time and confidence;
- retention;
- evidence.

Restore occurs into an isolated target or verified stopped state.

The restored target remains non-authoritative until integrity, schema, ownership, policy, trust, queues, replay, representative reads, representative writes, and health pass.

### 4.27 Audit and evidence

Offline audit is locally durable and selective.

Public events can identify:

- operation class;
- component;
- result;
- reason;
- policy identity;
- receipt identity;
- observation time;
- correlation.

Private evidence can preserve:

- identity proof;
- consent;
- cultural-rights evidence;
- trust path;
- protected subject details;
- diagnostics;
- conflict payloads;
- recovery material.

Private evidence does not move into public logs because connectivity is absent.

### 4.28 Reconnection verification

When a link returns, the node does not immediately declare connected readiness.

It first verifies:

- network interface and route;
- peer identity;
- transport trust;
- trusted time;
- trust and revocation updates;
- active policy compatibility;
- peer contract versions;
- destination identities;
- release-channel state;
- queue and replay state;
- synchronization capacity;
- local health;
- recovery state.

A malicious or misconfigured peer is treated as unavailable rather than as a reason to weaken checks.

### 4.29 Synchronization order

A profile or component contract defines exact ordering.

A common safe order is:

1. establish trusted time and peer identity;
2. exchange trust and revocation state through the declared transition;
3. exchange contract and compatibility information;
4. reconcile policy artifacts;
5. reconcile identity and authority references;
6. reconcile withdrawals and revocations that can invalidate queued actions;
7. exchange inventory and version summaries;
8. transfer bounded payloads;
9. resolve conflicts;
10. apply accepted component changes;
11. deliver queued intents;
12. receive and verify remote results;
13. reconcile receipts and evidence;
14. verify health and connected capability;
15. mark `connected_verified`.

This order is explanatory. Canonical ordering belongs to the applicable synchronization contracts.

### 4.30 Reconnection throttling

Reconnection can create sudden demand.

Resource envelopes bound:

- concurrent peer sessions;
- outbound queue drain;
- inbound payload count;
- bandwidth;
- CPU;
- memory;
- storage;
- conflict workers;
- database writes;
- receipt generation;
- backup checkpoints.

Interactive local operation can retain priority over bulk synchronization.

A large backlog does not authorize dropping protected or authoritative work silently.

### 4.31 Recovery

Offline recovery can involve:

- service restart;
- queue repair;
- replay reconciliation;
- storage repair;
- backup restore;
- policy rollback;
- trust recovery;
- artifact rollback;
- migration forward repair;
- node re-enrollment;
- worker destruction and reprovisioning.

Recovery keeps affected capabilities restricted.

Full authority returns after validation and a stability interval defined by profile or component contract.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-OPS-OFF-001,REQ-OPS-OFF-002,REQ-OPS-OFF-003,REQ-OPS-OFF-004,REQ-OPS-OFF-005,REQ-OPS-OFF-006,REQ-OPS-OFF-007,REQ-OPS-OFF-008,REQ-OPS-OFF-009,REQ-OPS-OFF-010,REQ-OPS-OFF-011,REQ-OPS-OFF-012,REQ-OPS-OFF-013,REQ-OPS-OFF-014,REQ-OPS-OFF-015,REQ-OPS-OFF-016,REQ-OPS-OFF-017,REQ-OPS-OFF-018,REQ-OPS-OFF-019,REQ-OPS-OFF-020,REQ-OPS-OFF-021,REQ-OPS-OFF-022,REQ-OPS-OFF-023,REQ-OPS-OFF-024,REQ-OPS-OFF-025,REQ-OPS-OFF-026,REQ-OPS-OFF-027,REQ-OPS-OFF-028,REQ-OPS-OFF-029,REQ-OPS-OFF-030,REQ-OPS-OFF-031,REQ-OPS-OFF-032 -->
- **REQ-OPS-OFF-001 — SHALL:** Every profile claiming offline operation shall declare the local capabilities, required local dependencies, retained authority, denied operations, freshness limits, synchronization behavior, recovery behavior, and conformance evidence for that claim.
- **REQ-OPS-OFF-002 — SHALL:** Offline operation shall preserve the same component, data-owner, identity, policy, consent, trust, artifact, and privilege boundaries used during connected operation.
- **REQ-OPS-OFF-003 — SHALL NOT:** Loss of connectivity shall broaden authority, weaken consent, bypass cultural-rights policy, create machine privilege, select an undeclared provider, or permit direct cross-component writes.
- **REQ-OPS-OFF-004 — SHALL:** Each offline-capable capability shall declare whether it remains authoritative, read-only, advisory-only, queued, unavailable, or recovery-only while disconnected.
- **REQ-OPS-OFF-005 — SHALL:** A node shall enter verified offline operation only after confirming the active local contracts, identities, trust state, policy state, data integrity, artifact identities, resource envelopes, storage capacity, health, and recovery material required by its profile.
- **REQ-OPS-OFF-006 — SHALL NOT:** Network loss, public DNS failure, public time-service failure, remote monitoring loss, or external integration loss shall be represented as loss of unrelated deterministic local capabilities.
- **REQ-OPS-OFF-007 — SHALL:** Offline identity, trust, revocation, policy, consent, and authority decisions shall use the newest trusted local state available and shall expose identity, policy, trust, evidence, and time freshness.
- **REQ-OPS-OFF-008 — SHALL NOT:** Stale, missing, expired, revoked, suspended, conflicting, or unverifiable authority state shall be silently treated as current or valid.
- **REQ-OPS-OFF-009 — SHALL:** Trusted local time shall identify its source, confidence, last synchronization, monotonic context, drift status, and effect on credential, policy, bundle, lease, retention, and receipt validity.
- **REQ-OPS-OFF-010 — SHALL:** Authoritative offline mutations shall require valid local identity, policy, consent, integrity, storage, contract, concurrency, idempotency, and receipt conditions for the affected operation.
- **REQ-OPS-OFF-011 — SHALL:** Every queued outbound operation shall preserve the originating component, actor, purpose, target, payload identity, local state version, policy and consent references, request identity, ordering constraints, retry behavior, expiry, and receipt correlation.
- **REQ-OPS-OFF-012 — SHALL NOT:** A queued publication, synchronization, external AI request, external voice request, artifact upload, or remote command shall be reported as completed before a verified remote result is received.
- **REQ-OPS-OFF-013 — SHALL:** Transactional outbox, durable queue, replay ledger, and receipt state shall remain component- or service-owned, bounded, integrity-verifiable, recoverable, and isolated from unrelated workspaces and components.
- **REQ-OPS-OFF-014 — SHALL:** Offline retries shall be idempotent or explicitly reconciled, shall use bounded backoff, and shall not repeat non-idempotent migrations, trust updates, publications, restores, or authoritative mutations.
- **REQ-OPS-OFF-015 — SHALL:** Synchronization shall exchange explicit versions, object identities, provenance, deletions, policy and consent context, replay state, receipts, and conflict evidence through the owning component's declared interface.
- **REQ-OPS-OFF-016 — SHALL NOT:** Last-writer-wins shall be the default authority rule for offline conflicts.
- **REQ-OPS-OFF-017 — SHALL:** A conflict shall preserve every competing version and its authority, provenance, time confidence, policy, consent, and receipt context until the owning component applies its declared deterministic or governed resolution procedure.
- **REQ-OPS-OFF-018 — SHALL:** Inbound offline artifacts and synchronization payloads shall enter quarantine and shall remain separate from import, staging, migration, activation, and authoritative acceptance.
- **REQ-OPS-OFF-019 — SHALL:** Offline bundle, artifact, policy, migration, trust, recovery, and result payloads shall retain their own class, channel, signer, compatibility, activation, rollback, forward-repair, and evidence requirements.
- **REQ-OPS-OFF-020 — SHALL:** The system, services, governance, and knowledge release channels shall remain independently versioned, verified, staged, activated, rolled back, and receipted during offline operation.
- **REQ-OPS-OFF-021 — SHALL:** Offline health shall distinguish local liveness, local-read readiness, authoritative-write readiness, policy and trust freshness, queue state, synchronization state, external dependency state, resource pressure, and recovery state.
- **REQ-OPS-OFF-022 — SHALL:** Storage, queue, log, quarantine, staging, backup, restore, and receipt resources used offline shall have explicit owners, quotas, retention, cleanup, encryption, backup eligibility, and recovery behavior.
- **REQ-OPS-OFF-023 — SHALL:** Resource pressure or exhausted storage shall stop unsafe new work, preserve committed authoritative data, protect required receipts and replay state, and expose an accurate constrained or degraded state.
- **REQ-OPS-OFF-024 — SHALL:** Offline backup and restore shall preserve component ownership, policy and cultural-rights constraints, encryption, integrity, schema compatibility, migration requirements, isolated restore validation, and recovery evidence.
- **REQ-OPS-OFF-025 — SHALL:** Local deterministic navigation, language, civic, workflow, knowledge, and native media capabilities shall remain independent from ChatGPT, Suno, Gamma, external Ariane voice, SenTient, and other non-required external services.
- **REQ-OPS-OFF-026 — SHALL NOT:** An unavailable external AI, voice, publication, search, or synchronization integration shall be replaced by an undeclared provider or local authority expansion.
- **REQ-OPS-OFF-027 — SHALL:** Offline audit and evidence shall separate bounded public events from private identity, consent, cultural-rights, trust, diagnostic, and protected subject evidence.
- **REQ-OPS-OFF-028 — SHALL:** Return to connectivity shall begin with identity, trust, time, policy, artifact, destination, and peer verification before outbound queues or inbound updates are processed.
- **REQ-OPS-OFF-029 — SHALL:** Reconnection shall use bounded staged synchronization, shall preserve local service while independent capabilities remain valid, and shall not place the node in full connected readiness until conflicts, queues, policies, trust, artifacts, and evidence are reconciled.
- **REQ-OPS-OFF-030 — SHALL:** Offline recovery shall retain restricted authority until integrity, data ownership, schema compatibility, policy, trust, queue, replay, artifact, resource, and representative behavior checks pass.
- **REQ-OPS-OFF-031 — SHALL:** Development workspaces, parallel branches, build workers, and test nodes exercising offline behavior shall use separate identities, trust contexts, queues, volumes, databases, ports, secrets, receipts, and synchronization peers.
- **REQ-OPS-OFF-032 — SHALL:** A complete offline-operations conformance claim shall include disconnect, local continuity, time, trust, policy, consent, mutation, outbox, replay, queue pressure, conflict, bundle, release-channel, backup, restore, external-integration, reconnection, recovery, privacy, and negative-path tests with evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Preparing for planned disconnection

Preparation follows this order:

1. identify the target profile and planned duration;
2. load the offline capability declarations;
3. verify component and artifact identities;
4. verify local storage and free capacity;
5. verify queues, outboxes, replay ledgers, and receipts;
6. synchronize required trust, revocation, policy, consent, and authority state;
7. synchronize required local data and artifacts;
8. verify trusted time and confidence;
9. create required backups and recovery material;
10. drain operations that cannot continue offline;
11. mark remote-only operations unavailable or queueing-only;
12. run offline-readiness tests;
13. record readiness evidence;
14. enter `disconnecting`;
15. disable or detach the declared network path;
16. verify `offline_verified` or `offline_limited`.

### 6.2 Detecting unplanned disconnection

Unplanned disconnect handling:

1. detect loss through bounded network and peer checks;
2. avoid restarting healthy local components solely because the peer is absent;
3. freeze unsafe in-flight remote transitions;
4. preserve request and response correlation;
5. classify each affected capability;
6. verify local authority and storage;
7. enter the declared offline state;
8. expose external dependency loss separately;
9. create incident or transition evidence;
10. begin bounded retry only where permitted.

### 6.3 Executing an offline local mutation

A local mutation:

1. authenticates the local actor;
2. verifies local trust and time;
3. resolves the active component contract;
4. loads the target and expected version;
5. evaluates component authorization;
6. evaluates governance policy, consent, and cultural rights when applicable;
7. verifies storage and resource state;
8. applies optimistic concurrency;
9. commits the authoritative change and outbox atomically;
10. creates the local receipt;
11. updates health and queue metrics;
12. leaves remote delivery pending.

### 6.4 Queueing a remote operation

Queueing:

1. resolves the owning component and destination contract;
2. verifies that offline queueing is permitted;
3. validates actor, purpose, policy, consent, payload, and expiry;
4. assigns stable request and correlation identities;
5. records local source versions;
6. records ordering and retry constraints;
7. commits the queue item durably;
8. produces a queue receipt;
9. presents the operation as queued rather than completed.

### 6.5 Processing an offline bundle

Bundle processing:

1. identifies the carrier;
2. copies the candidate into quarantine;
3. verifies bounded envelope structure;
4. verifies envelope identity, signature, recipient, scope, time, sequence, and replay;
5. extracts safely into quarantine;
6. verifies each payload independently;
7. evaluates profile, compatibility, policy, and resource prerequisites;
8. records per-payload results;
9. stages eligible payloads separately;
10. hands activation to each class owner;
11. records import, staging, activation, rejection, rollback, and recovery separately;
12. cleans quarantine according to retention.

### 6.6 Creating an outbound synchronization package

Package creation:

1. identifies the synchronization peer and owner component;
2. selects a stable source snapshot;
3. selects changed objects, events, deletions, policies, receipts, and conflicts;
4. applies consent, cultural-rights, disclosure, and minimization;
5. records source versions and provenance;
6. creates a bounded inventory;
7. encrypts for the recipient when required;
8. signs the package or containing bundle;
9. verifies the finished package;
10. stores it in outbound staging;
11. creates the export receipt.

### 6.7 Reconnecting

Reconnection:

1. detect link availability;
2. enter `reconnecting`;
3. verify the peer and transport;
4. establish trusted time and confidence;
5. compare trust and revocation state;
6. compare policy and contract compatibility;
7. compare release-channel and artifact identities;
8. compare queue and replay summaries;
9. verify storage and resource capacity;
10. create a synchronization plan;
11. begin bounded synchronization;
12. keep unrelated local capabilities available.

### 6.8 Synchronizing one component

Component synchronization:

1. authenticate both peers;
2. verify component contract compatibility;
3. exchange version and inventory summaries;
4. transfer bounded candidate changes;
5. verify integrity and provenance;
6. evaluate policy, consent, cultural rights, and withdrawals;
7. detect duplicates and replay;
8. detect conflicts;
9. accept non-conflicting changes through component commands;
10. record rejected or pending changes;
11. exchange receipts;
12. verify resulting component health.

### 6.9 Resolving a conflict

Conflict resolution:

1. preserve all competing versions;
2. identify the source authority and provenance of each version;
3. identify base state and causal context;
4. identify policy, consent, withdrawal, trust, and time context;
5. apply deterministic domain rules where declared;
6. otherwise request the declared authority review;
7. create the resolution command;
8. commit the selected, merged, parallel, rejected, or compensating result;
9. preserve the conflict record;
10. create the resolution receipt;
11. continue synchronization.

### 6.10 Draining outbound queues

Queue drain:

1. select a queue by owner and priority;
2. verify destination identity and health;
3. revalidate item expiry, policy, consent, withdrawal, trust, and target compatibility;
4. reserve the item in the replay ledger;
5. submit the item;
6. receive the remote result;
7. verify result identity and signature where applicable;
8. reconcile local state;
9. mark complete, retry, reject, conflict, or expire;
10. store the result receipt;
11. release queue capacity.

### 6.11 Returning to connected readiness

Connected readiness:

1. verify that required trust and policy updates are active;
2. verify critical conflicts are resolved or explicitly isolated;
3. verify required queues are drained or inside declared bounds;
4. verify remote publication and synchronization results;
5. verify active artifacts and Release Set compatibility;
6. verify local and peer health;
7. verify evidence and receipts;
8. verify backup and recovery posture;
9. hold the result for the declared stability interval;
10. enter `connected_verified`.

### 6.12 Offline recovery

Recovery:

1. isolate the affected component or node state;
2. preserve queues, receipts, replay, and forensic evidence;
3. identify the last verified contracts, policies, trust, artifacts, and backups;
4. repair or restore into an isolated target;
5. apply declared migrations or forward repair;
6. reconcile queues and replay state;
7. validate ownership, integrity, schema, policy, trust, resources, and health;
8. run representative local reads and writes;
9. restore only the capabilities that pass;
10. record recovery evidence.

## 7. Failure States and Safe Degradation

| Failure state | Required response |
| --- | --- |
| Network link is lost | The node enters its declared offline transition and preserves independent local capability. |
| Peer identity cannot be verified after reconnection | Synchronization and remote operations remain blocked; local verified operation continues where permitted. |
| Trusted time confidence is low | Time-sensitive credentials, policies, bundles, leases, and operations follow their stricter offline behavior. |
| Revocation state is stale | Staleness is exposed; high-impact operations can remain blocked. |
| Local policy is missing or invalid | Policy-bound operations remain blocked. |
| Required consent evidence is missing | The affected action is denied or enters authority review. |
| Local database is read-only | Verified reads can continue; authoritative mutations and durable queue commits stop. |
| Storage reaches a high-water mark | Replaceable caches and expired temporary data are cleaned according to contract; new optional work is reduced. |
| Storage reaches a critical-water mark | Unsafe new writes and imports stop while committed authoritative data, replay state, and receipts are protected. |
| Outbox is full | New mutations requiring outbox atomicity remain blocked or the component enters declared constrained behavior. |
| Outbox delivery fails | Local committed state remains authoritative locally; delivery stays pending and is not reported complete. |
| Replay ledger is unavailable | Non-idempotent or replay-sensitive operations remain blocked. |
| Queue item expires | The item becomes expired, records its result, and is not sent. |
| Queued policy or consent becomes invalid | The item is rejected or enters review before transmission. |
| Duplicate remote result arrives | The prior reconciled result is returned and effects are not repeated. |
| Concurrent local and remote edits conflict | Both versions remain preserved until component-owned resolution. |
| Withdrawal conflicts with queued export | The export remains blocked and withdrawal rules take precedence according to the owning policy contract. |
| Synchronization is interrupted | Verified completed items remain complete; incomplete items resume or restart idempotently. |
| Inbound bundle fails verification | It remains quarantined or is rejected; local active state remains unchanged. |
| One bundle payload is invalid | That payload is rejected independently; valid payloads remain separately evaluated. |
| Artifact activation fails | The previous verified artifact remains active or forward repair begins. |
| Trust update fails | The prior trusted state remains active or the recovery trust procedure begins. |
| Migration is interrupted | It resumes from a checkpoint or enters forward repair; it is not repeated blindly. |
| External publication destination is unavailable | Publication intent remains local and no completion claim is made. |
| External AI is unavailable | Local deterministic capabilities continue and no alternate provider is selected. |
| Ariane external voice is unavailable | Local Ariane navigation remains available. |
| SenTient is unavailable | Core operation continues without advisory workbench capability. |
| Backup cannot be verified | It is not eligible for restore authority. |
| Restore validation fails | The restored target remains non-authoritative. |
| Audit forwarding is unavailable | Local bounded audit and evidence storage continue within quota. |
| Private evidence storage is unavailable | Evidence-dependent operations remain blocked; protected evidence is not copied into public logs. |
| Resource Governor is unavailable | New work remains within last verified limits or stops according to profile; policy authority is not inferred. |
| Reconnection backlog exceeds capacity | Synchronization is throttled and staged; local interactive and critical operation retains declared priority. |
| Cleanup ownership is uncertain | Automatic deletion stops and the resource remains protected or quarantined. |

Offline failure narrows capability and never broadens authority.

## 8. Cross-Component Interactions

### 8.1 Identity and Trust

Identity and Trust supplies local identity, credential, signer, trust, revocation, peer, and time-related verification results according to its contract.

It does not authorize component business operations or write component data.

Offline freshness is explicit.

### 8.2 Governance Policy Runtime

The Governance Policy Runtime evaluates locally available policy, consent, disclosure, privilege, obligation, and exception inputs.

It can continue only within its active local policy and evidence envelope.

A missing current decision blocks the affected action rather than creating a permissive fallback.

### 8.3 Resource Governor

The Resource Governor enforces local CPU, memory, I/O, storage, queue, concurrency, and time envelopes.

It protects local continuity under backlog and synchronization pressure.

It does not change policy or trust semantics.

### 8.4 kOA Node Agent

The Node Agent can manage network transition, service lifecycle, quarantine, artifact staging, trust-store activation, backup, restore, and recovery through its narrow privilege boundary.

It executes verified requests and does not become the owner of component data or governance policy.

### 8.5 Audit Broker

The Audit Broker stores and routes bounded local events and private evidence references.

It can queue remote forwarding.

It does not expose private evidence in public audit because remote delivery is unavailable.

### 8.6 Publication Gateway

The Publication Gateway owns cross-domain disclosure and publication execution.

While disconnected, local components can create publication intent where permitted.

The gateway result remains pending until actual gateway processing and verification occur.

### 8.7 Konnaxion

Konnaxion can preserve declared local civic spaces, proposals, responses, readings, receipts, and publication intents.

It applies optimistic concurrency and component-owned conflict resolution.

Smart Vote, EkoH, and civic results never become machine privilege online or offline.

### 8.8 Orgo

Orgo can continue declared critical local workflows with valid local identities, policy, data, queues, and resources.

Loss of Konnaxion or another optional event source affects only dependent workflow steps.

Orgo does not write Konnaxion storage during synchronization.

### 8.9 Kristal Runtime

Kristal Runtime serves verified local Runtime Packs and reports pack identity and freshness.

Recognition, distribution, and workflow status remain separate from Kristal content identity.

New packs arrive through artifact verification and activation.

### 8.10 SemantiK Architect Runtime

The language runtime consumes compiled local PGF and language packs.

Offline operation does not depend on GF Wordbench or remote compilation.

A missing language pack affects only that declared language capability.

### 8.11 Ariane Runtime

Ariane provides deterministic local navigation and commands from verified local artifacts.

External voice is a separate integration.

Local navigation remains available when voice or connectivity is absent.

### 8.12 kOA Mediatheque and external UCKK target

The kOA Mediatheque preserves local source and derivative ownership and deterministic processing. UCKK has separate remote authority and storage.

The UCKK publication integration can queue controlled outbound publication intents where permitted. The separate UCKK import integration can accept complete offline learning packages into quarantine or defer online retrieval. Neither direction queues direct remote database writes, automatic progress transfer, or implicit bidirectional synchronization.

Publication remains separate from dimension ingestion.

### 8.13 SenTient

SenTient is present only in permitted developer or build profiles and only as an isolated task-activated workbench.

Its local availability does not make its output authoritative.

Its absence has no effect on the core offline baseline.

### 8.14 Control plane and sovereign hub

A control plane or hub can coordinate peers when connectivity exists.

An offline node does not require continuous control-plane contact for locally declared capabilities.

Reconnection verifies the coordinator before accepting commands or sending protected state.

### 8.15 Build farm and development workspaces

Build workers and development workspaces can test offline behavior with isolated identities, queues, data, ports, volumes, secrets, peers, and resource envelopes.

A test peer does not use production trust or production synchronization authority.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Accepted decisions

| Decision | Effect |
| --- | --- |
| `DEC-PROFILE-001` | Defines sovereign offline behavior as an explicit profile overlay rather than a universal topology. |
| `DEC-PROFILE-BASELINE-001` | Keeps exact offline capability, storage, trust, time, health, and recovery values profile-scoped. |
| `DEC-COMP-001` | Preserves first-class component boundaries during local operation and synchronization. |
| `DEC-DATA-001` | Preserves logical data ownership across physical consolidation, queues, bundles, backup, restore, and synchronization. |
| `DEC-GOV-001` | Separates Resource Governor controls from Governance Policy Runtime decisions offline and online. |
| `DEC-GATE-001` | Keeps local Mediatheque admission separate from cross-domain publication and queued UCKK intent. |
| `DEC-REL-001` | Preserves the four independent release channels during offline import and activation. |
| `DEC-AI-001` | Excludes native AI from the baseline and keeps external outputs candidate-only. |
| `DEC-SENT-001` | Keeps SenTient optional, isolated, task-activated, and non-authoritative. |
| `DEC-ARI-001` | Keeps Ariane local navigation independent from external voice. |
| `DEC-MEDIATHEQUE-001` | Keeps kOA Mediatheque processing deterministic and non-AI. |
| `DEC-UCKK-EXT-001` | Keeps UCKK external and publication explicit, optional, and receipted. |
| `DEC-DEV-001` | Requires isolated workspace identity, services, data, queues, credentials, and resources. |
| `DEC-DEV-002` | Requires collision-free parallel workspace and branch operation. |

### 9.2 Related ADRs

| ADR | Relevance |
| --- | --- |
| `ADR-005` | Permits profile-scoped rootless runtime and local service topology. |
| `ADR-012` | Keeps privileged node transitions inside a narrow broker boundary. |
| `ADR-015` | Requires isolated development workspaces. |
| `ADR-019` | Separates resource and governance authority. |
| `ADR-021` | Preserves Ariane local navigation without external voice. |
| `ADR-024` | Preserves logical ownership across deployment forms. |

### 9.3 Prohibited assumptions

The following assumptions are prohibited:

- a network cable state defines operational readiness;
- offline means unrestricted local authority;
- a local database write is valid because no remote peer can object;
- a cached policy is current because the node is disconnected;
- an expired credential remains valid offline;
- an unavailable identity provider authorizes anonymous fallback;
- missing consent can be deferred until synchronization;
- local time is trustworthy because it is monotonic;
- later wall-clock time wins a conflict;
- last-writer-wins is a neutral merge rule;
- a queued request is a completed request;
- an outbox record proves remote receipt;
- a copied bundle is an imported bundle;
- an imported artifact is staged;
- a staged artifact is active;
- a started artifact is accepted;
- one valid bundle payload validates every payload;
- a Release Set merges release-channel authority;
- a hub or control plane owns node-local component data;
- synchronization permits direct database writes;
- a generic importer can resolve component conflicts;
- a backup can bypass cultural-rights restrictions;
- a restore target is authoritative because it is readable;
- external AI output can be generated by an undeclared local substitute;
- loss of ChatGPT disables local civic, workflow, knowledge, language, navigation, or media capability;
- loss of external voice disables Ariane;
- loss of Suno or Gamma disables local kOA Mediatheque operation;
- SenTient availability creates core authority;
- public audit storage can absorb private evidence during disconnection;
- reconnection means remote peers are trusted;
- queue drain should begin before revocation and policy reconciliation;
- backlog pressure authorizes dropping authoritative work silently;
- one workspace can reuse another workspace's offline queues or trust context;
- recovery is complete when processes restart.

## 10. Validation Criteria

This document conforms when all of the following checks pass:

1. metadata status is `active`;
2. the registered path is `08-operations/11-offline-operations.md`;
3. all canonical references resolve;
4. all listed decisions are accepted;
5. all requirements match the requirements registry;
6. all locks resolve and pass;
7. every offline-capable profile declares local capabilities and prerequisites;
8. every offline-capable component classifies each capability's offline authority;
9. offline state transitions are explicit;
10. network loss does not broaden authority;
11. optional external dependency loss does not cascade to independent local capabilities;
12. local identity, trust, policy, consent, and authority freshness is exposed;
13. trusted local time and confidence are exposed;
14. stale or invalid trust and policy state does not appear current;
15. authoritative offline mutations prove the complete local authority set;
16. every queued operation has stable identity, owner, purpose, version, policy, expiry, retry, and receipt context;
17. queued state is not reported as remote completion;
18. transactional outbox behavior is atomic with the local transition;
19. replay state survives restart and recovery;
20. retry tests do not repeat non-idempotent effects;
21. synchronization uses component-owned interfaces;
22. direct cross-component database writes are absent;
23. conflict tests preserve every competing version and context;
24. last-writer-wins is not the default conflict rule;
25. inbound payloads enter quarantine;
26. import, staging, migration, activation, and acceptance remain separate;
27. all four release channels remain independent;
28. Release Set compatibility is verified;
29. offline health distinguishes local and external capability states;
30. storage, queue, quarantine, staging, backup, restore, receipt, and evidence quotas are enforced;
31. storage pressure protects authoritative data and replay state;
32. backup and restore tests preserve ownership, policy, encryption, integrity, schema, and evidence;
33. ChatGPT, Suno, Gamma, external voice, and SenTient loss do not disable unrelated local capability;
34. no undeclared external provider or local authority substitution occurs;
35. public audit and private evidence remain separated;
36. reconnection verifies peer identity, time, trust, policy, contracts, artifacts, and destinations before queue processing;
37. revocation and withdrawal updates are reconciled before affected queued actions;
38. synchronization is bounded by resource envelopes;
39. local operation remains available during backlog processing where authority remains valid;
40. connected readiness remains withheld until critical conflicts, queues, artifacts, policies, trust, and evidence are reconciled;
41. offline recovery retains restricted authority until revalidation passes;
42. parallel workspace and test-node isolation passes;
43. disconnect and reconnect interruption tests preserve authoritative state;
44. requirement-to-test-to-evidence traceability is complete;
45. active content is English;
46. placeholder and open-authority markers are absent.

The validator reports focused failures, including:

`text
offline_profile_capability_missing
offline_component_mode_missing
offline_transition_invalid
offline_authority_broadened
offline_optional_dependency_cascade
offline_identity_freshness_missing
offline_trust_freshness_missing
offline_policy_freshness_missing
offline_time_confidence_missing
offline_mutation_authority_incomplete
offline_queue_identity_missing
offline_queue_reported_complete
offline_outbox_not_atomic
offline_replay_state_missing
offline_non_idempotent_retry
offline_component_interface_bypassed
offline_cross_component_write
offline_conflict_version_lost
offline_last_writer_wins_default
offline_quarantine_bypassed
offline_import_activation_conflated
offline_release_channel_collapsed
offline_health_external_cascade
offline_storage_quota_missing
offline_storage_pressure_data_loss
offline_backup_policy_missing
offline_restore_not_validated
offline_external_provider_substitution
offline_private_evidence_exposed
offline_peer_identity_unverified
offline_revocation_reconciled_late
offline_queue_drain_unbounded
offline_connected_ready_too_early
offline_recovery_not_revalidated
offline_workspace_identity_collision
`

## 11. Non-Normative Examples

### 11.1 Planned sovereign-node disconnection

A sovereign node is scheduled to operate disconnected for seven days.

Before disconnection, it refreshes trust and revocation state, validates local policies, synchronizes required Kristal and language packs, verifies storage capacity, creates a backup, checks queues, and records offline-readiness evidence.

Konnaxion, Orgo, Kristal, language, Ariane local navigation, and the kOA Mediatheque enter their declared local modes. UCKK publication enters queued or unavailable state.

### 11.2 Konnaxion local response

A verified participant records a response while the node is offline.

Konnaxion validates the local identity, proposal state, expected version, consent and policy conditions, commits the response and outbox atomically, and returns a local receipt.

The response is locally authoritative. Remote synchronization remains pending.

### 11.3 Publication intent

A user requests publication of a locally approved proposal description.

Konnaxion creates a publication intent and queues the bounded payload for the Publication Gateway. The interface shows `queued offline`, not `published`.

After reconnection, the gateway result is verified and the intent state changes separately.

### 11.4 Consent withdrawal before queue drain

An export was queued offline.

Before reconnection, a valid consent withdrawal is imported through a signed policy update. During queue revalidation, the export is rejected and a withdrawal-related receipt is created.

The earlier queue receipt is preserved but does not compel delivery.

### 11.5 Concurrent proposal edits

Two disconnected nodes edit the same proposal from the same base version.

Synchronization preserves both revisions, actors, policy context, and receipts. Konnaxion applies its declared conflict procedure rather than selecting the later wall-clock timestamp automatically.

### 11.6 Ariane without voice

The node loses all external connectivity.

Ariane continues local menus, navigation, accessibility, and component commands. The external voice capability reports unavailable. No alternate provider is selected.

### 11.7 kOA Mediatheque without Suno, Gamma, or UCKK

The kOA Mediatheque continues local source ingestion, deterministic derivatives, playback, backup, and export preparation. UCKK publication waits for connectivity and explicit revalidation.

Suno and Gamma actions remain unavailable. A queued external-candidate request does not produce a local candidate until an actual provider result returns.

### 11.8 Offline bundle update

An operator imports a bundle containing a service artifact, a governance policy bundle, a language pack, a trust update, and a Release Set.

The envelope and every payload are verified separately. The trust update uses its high-impact transition. The language pack activates independently. The service artifact remains staged because its migration backup is absent.

### 11.9 Storage pressure

A node's outbound synchronization queue and local logs approach the storage high-water mark.

The Resource Governor reduces optional background work, rotates logs, and evicts replaceable cache content. Committed component data, outbox entries, replay state, and required receipts remain protected.

### 11.10 Reconnection backlog

A node reconnects after thirty days.

It verifies the peer, time, trust, revocation, policies, contracts, and Release Set before draining queues. Synchronization is throttled. Local interactive operation remains available, and the node reaches `connected_verified` only after critical conflicts and receipts are reconciled.
