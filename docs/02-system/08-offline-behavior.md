<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-008",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "system",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/requirements-index.json"
  ],
  "decision_ids": [
    "DEC-AI-001",
    "DEC-ARI-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-HW-001",
    "DEC-PROFILE-001",
    "DEC-SENT-001",
    "DEC-MEDIATHEQUE-001",
    "DEC-UCKK-EXT-001"
  ],
  "requirement_ids": [
    "REQ-OFFLINE-001",
    "REQ-OFFLINE-002",
    "REQ-OFFLINE-003",
    "REQ-OFFLINE-004",
    "REQ-OFFLINE-005",
    "REQ-OFFLINE-006",
    "REQ-OFFLINE-007",
    "REQ-OFFLINE-008",
    "REQ-OFFLINE-009",
    "REQ-OFFLINE-010",
    "REQ-OFFLINE-011",
    "REQ-OFFLINE-012",
    "REQ-OFFLINE-013",
    "REQ-OFFLINE-014",
    "REQ-OFFLINE-015",
    "REQ-OFFLINE-016",
    "REQ-OFFLINE-017",
    "REQ-OFFLINE-018",
    "REQ-OFFLINE-019",
    "REQ-OFFLINE-020",
    "REQ-OFFLINE-021",
    "REQ-OFFLINE-022",
    "REQ-OFFLINE-023",
    "REQ-OFFLINE-024",
    "REQ-OFFLINE-025",
    "REQ-OFFLINE-026",
    "REQ-OFFLINE-027",
    "REQ-OFFLINE-028"
  ],
  "lock_ids": [
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-SENT-001",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-UCKK-EXT-001",
    "LOCK-UCKK-EXT-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-CONST-000",
    "DOC-CONST-002",
    "DOC-SYS-000"
  ],
  "tags": [
    "system",
    "offline",
    "continuity",
    "safe-degradation",
    "external-ai",
    "reconnection",
    "local-authority",
    "deterministic-operation"
  ]
}
KOA:DOC-META:END -->

# Offline Behavior

## 1. Purpose

This document defines the global offline behavior of the kOA operating environment.

Offline operation is a normal supported state, not an exceptional recovery mode. The native system remains useful when Internet access, external AI surfaces, remote synchronization, remote publication targets, online update services, or other external dependencies are unavailable.

The offline contract has five objectives:

1. preserve local user work and authoritative local data;
2. preserve deterministic native capabilities that have all required local artifacts;
3. disable or narrow only the capabilities that depend on unavailable external services;
4. prevent connectivity loss from creating implicit authority, unsafe fallback, partial publication, or silent data loss;
5. make reconnection a controlled transition with revalidation rather than an automatic replay of stale intent.

The canonical capability model, offline boundary, operating modes, degradation model, and external-service classification are owned by `contracts/system.contract.json`. Component responsibilities are owned by `generated/component-catalog.json`. The normative statements rendered in this document are owned by `generated/requirements-index.json`.

## 2. Scope

### 2.1 Global applicability

This document applies to:

- all active kOA deployment profiles and profile overlays;
- user and developer operating modes;
- local services and component runtimes;
- local data stores, queues, caches, indexes, and artifact stores;
- local authentication and trust evaluation;
- Ariane guidance and automation;
- kOA Mediatheque ingestion, storage, versioning, and deterministic media processing;
- Kristal and language runtime consumption of installed artifacts;
- local Orgo and Konnaxion capabilities;
- Resource Governor decisions;
- Governance Policy Runtime where a profile deploys it;
- Publication Gateway and other governed transfer paths;
- external integrations, including approved external AI surfaces;
- backup, restore, diagnostics, audit, update, synchronization, and recovery behavior;
- reconnect processing after external availability returns.

### 2.2 Meaning of offline

For this document, offline means that a deployment cannot rely on one or more external network services required by an optional capability.

Offline can result from:

- no physical network;
- no Internet route;
- unavailable name resolution;
- blocked outbound policy;
- unavailable external provider;
- failed authentication to an external provider;
- expired or unavailable remote authorization;
- an intentionally isolated profile;
- a local-only operating policy;
- a temporary outage affecting only one integration.

The system does not treat all network loss as equivalent. A local network can remain available while the Internet is unavailable. One provider can be unavailable while another remains reachable. Capability evaluation uses the exact dependency that is unavailable.

### 2.3 Native capability boundary

A native capability is part of the local kOA execution boundary and has a defined offline behavior.

A capability is not native merely because:

- its interface appears inside a kOA application;
- a browser can display it;
- an external provider has been configured;
- a recipe demonstrates it;
- a developer workstation can reach it;
- a previous result has been cached;
- an external AI response is shown in a local workflow.

ChatGPT, Suno, Gamma, and the external voice-understanding path used by Ariane are optional external surfaces. Their unavailability does not make the native system unavailable.

### 2.4 Profile-specific strengthening

A profile can strengthen the global offline baseline by requiring:

- complete network isolation;
- offline update bundles;
- local trust roots;
- local policy evaluation;
- longer autonomous operation;
- locally available recovery media;
- stricter outbound queue controls;
- stronger evidence for imported artifacts;
- local mirrors or package repositories;
- local time and identity services.

A profile-specific strengthening remains inside that profile or overlay unless an accepted decision promotes it globally.

### 2.5 Non-goals

This document does not:

- guarantee that every optional integration works without its provider;
- guarantee remote synchronization while remote endpoints are unavailable;
- make external AI local or native;
- require a local AI substitute;
- guarantee fresh remote data while disconnected;
- authorize queued publication merely because connectivity returns;
- define one universal network topology;
- require every deployment to host every component;
- define a universal maximum offline duration;
- make SenTient part of the native baseline;
- allow stale identity, consent, policy, trust, or time data to be treated as current without an applicable rule;
- turn cached external output into canonical authority;
- make a recipe or a profile implementation choice a global requirement.

## 3. Canonical References

| Canonical reference | Ownership applied by this document |
| --- | --- |
| `contracts/system.contract.json` | Global offline principle, operating modes, capability classifications, external AI boundary, degradation behavior, reconnection policy, and profile applicability. |
| `generated/component-catalog.json` | Component identity, responsibility, dependencies, authoritative data ownership, and allowed interaction boundaries. |
| `generated/requirements-index.json` | Normative requirement statements, strength, scope, source decisions, validation methods, and linked controls. |

The decision and lock identifiers in the metadata resolve through the active authority release. This document explains their system-level effect without redefining their canonical content.

Profile contracts can strengthen the baseline for a named profile. Component contracts can define narrower behavior for a component. Neither can silently weaken the global offline guarantees or broaden an external capability into the native baseline.

## 4. Model and Responsibilities

### 4.1 Offline capability model

Each capability has an explicit dependency envelope. The envelope identifies:

- local executable dependencies;
- local data dependencies;
- installed artifact dependencies;
- local identity and trust dependencies;
- policy dependencies;
- external network dependencies;
- external provider dependencies;
- time-sensitive authority dependencies;
- optional acceleration dependencies;
- queueing and replay behavior;
- degraded behavior;
- unavailable behavior;
- recovery and reconnection behavior.

A capability remains available offline when every dependency required for that capability is locally satisfied.

A capability narrows when a non-critical dependency is unavailable but a safe local subset remains. A capability becomes unavailable when its defining operation requires an unavailable external dependency. A governed operation becomes blocked when required authority, trust, consent, policy, freshness, or evidence cannot be verified.

### 4.2 System health and connectivity

Connectivity is a capability input, not the sole system-health signal.

The system can be healthy while offline when:

- local authoritative stores are consistent;
- required local runtimes are available;
- installed artifacts validate;
- local authorization can be evaluated;
- local queues are durable;
- backup and diagnostics remain functional;
- external-dependent capabilities are clearly marked unavailable or narrowed.

An external provider outage does not cause unrelated local components to report global failure.

### 4.3 Baseline component behavior

The following table describes the system-level offline envelope. Exact implementation details remain owned by component and profile contracts.

| Component or surface | Offline behavior | Boundary |
| --- | --- | --- |
| Resource Governor | Continues deterministic resource allocation, admission, throttling, suspension, and protection of local critical work. | It does not use AI and remains separate from governance authorization. |
| Orgo | Continues locally available work management and orchestration using authoritative local data and installed integrations. | Remote-only actions remain queued, unavailable, or blocked according to their contract. |
| Kristal Runtime | Continues serving installed, validated Exchange and Runtime Packs. | It does not fetch missing packs or treat cached external output as an active pack. |
| Konnaxion | Continues local capabilities backed by installed modules, local data, and available local services. | Remote data and remote-only modules are not fabricated or silently substituted. |
| SemantiK Architect Runtime | Continues rendering with installed compiled PGF and local runtime assets. | Missing languages or build outputs remain unavailable; runtime mode does not invoke compilers implicitly. |
| GF Wordbench | Can operate only when its developer profile, local toolchain, sources, and dependencies are available. | It is not required for normal user-mode runtime operation. |
| kOA Mediatheque | Continues local media storage, identity, versioning, provenance, visibility enforcement, collections, and deterministic local processing supported by installed tools. | It does not infer categories, summarize content, select publication channels, or invoke external AI automatically. |
| UCKK publication queue | Can preserve an explicitly requested publication draft and selected source references locally. | No external delivery occurs offline; authorization must be revalidated before bridge transport. |
| Ariane Runtime | Continues Atlas-based observation, structured-goal selection, guidance, approved local automation, action verification, and local receipts. | External voice understanding is unavailable when its external path is unavailable. |
| Governance Policy Runtime | Continues local authorization and disclosure evaluation only when the active profile deploys it with the required local policy artifacts. | If required policy authority cannot be evaluated, affected governed operations remain blocked. |
| Publication Gateway | Continues local validation and preparation of publication requests where local authority is sufficient. | Delivery to an unavailable external target does not complete; queued requests require revalidation before release. |
| Audit Broker | Continues local structured event capture and protected evidence handling. | It does not require disclosure of complete private content. |
| Identity and Trust | Continues local identity and trust decisions supported by active local credentials, trust roots, and permitted cached status. | Operations requiring fresh remote status remain blocked when that status is unavailable. |
| kOA Node Agent | Continues profile-authorized local health, lifecycle, and node coordination functions. | It does not treat unreachable remote control planes as authorization to self-broaden. |
| SenTient | Remains optional, isolated, on demand, and non-authoritative. Its exact offline envelope belongs to its component and profile contracts. | Its absence or failure does not remove a native baseline capability. |
| ChatGPT | Unavailable as an external surface when its service or route is unavailable. | No local substitute is inferred. |
| Suno | Unavailable as an external surface when its service or route is unavailable. | No native media generation is implied. |
| Gamma | Unavailable as an external surface when its service or route is unavailable. | No native presentation generation is implied. |
| Ariane external voice path | Voice input is disabled or shown unavailable. | Structured local Ariane operation remains available. |

### 4.4 Local authoritative data

Each component continues to own its authoritative data offline. Connectivity loss does not merge data ownership or permit direct writes into another component’s authoritative store.

Cross-component work uses declared contracts, local events, queues, receipts, or gateways. A temporary inability to deliver an event does not authorize a direct database write as a fallback.

Durable pending work records:

- origin;
- intended recipient;
- operation;
- payload reference;
- authority context;
- consent context where applicable;
- creation time;
- expiration or revalidation rule;
- retry state;
- final result.

### 4.5 External AI boundary

The native baseline does not depend on AI.

Offline behavior therefore does not include:

- automatic local classification;
- automatic local summarization;
- automatic local translation through an unspecified model;
- automatic category selection;
- automatic channel selection;
- automatic visibility decisions;
- automatic voice-intent inference;
- automatic replacement of ChatGPT, Suno, or Gamma;
- automatic use of SenTient as a substitute for unavailable external AI.

A user can continue a workflow manually by entering selected information, choosing a category, selecting an action, or importing an externally produced result after review. Manual continuation does not make the external system native.

### 4.6 Ariane offline behavior

Ariane separates structured navigation from optional voice input.

Offline Ariane can use:

- predefined goals;
- local structured commands;
- Atlas routes;
- operator-selected actions;
- step-by-step guidance;
- locally authorized automation;
- local observation and verification;
- local safety policy;
- local receipts.

The external voice path converts speech into a candidate structured command. It does not own the Atlas, authorize actions, or execute interface operations directly. When unavailable, the voice control is disabled without disabling local Ariane navigation.

### 4.7 kOA Mediatheque offline behavior

kOA Mediatheque remains user-directed and deterministic offline.

The local workflow can include:

```text
user selects material
  -> user chooses category or unclassified state
  -> user chooses local visibility
  -> gateway verifies and transfers
  -> kOA Mediatheque creates media identity and initial version
  -> original and provenance are preserved
  -> deterministic local derivatives are scheduled
  -> user receives local confirmation
```

Installed deterministic tools can generate thumbnails, previews, transcodes, text extraction, checksums, and other reproducible derivatives defined by active contracts. These operations do not constitute AI content understanding.

Publication is never an automatic consequence of ingestion. External publication and external processing remain separately governed.

### 4.8 Installed artifact behavior

Offline operation relies on activated local artifacts such as:

- system and service releases;
- governance policy bundles;
- Kristal artifacts;
- compiled PGF;
- language runtime packs;
- Ariane Atlases and Runtime Packs;
- kOA Mediatheque processing tools;
- profile contracts;
- trust roots;
- schemas;
- local recovery artifacts.

A missing optional artifact removes only the capability that depends on it. A missing artifact required by the active profile blocks activation or narrows the affected capability according to the profile contract.

The system does not download an unverified replacement automatically when reconnecting.

### 4.9 Time, identity, and trust

Offline operation can make time-sensitive authority uncertain.

Examples include:

- expired credentials;
- certificate status;
- consent expiration;
- exception expiration;
- policy validity;
- release validity;
- remote revocation status;
- lease or delegation expiration.

When a decision requires current time or fresh remote status and the required confidence is unavailable, the affected operation remains blocked or restricted. Existing local read-only access can continue only when active policy explicitly permits it.

The system records clock uncertainty rather than silently extending authority.

### 4.10 Local backup, restore, and diagnostics

Offline deployments can:

- create local backups;
- verify locally available backup manifests;
- restore through the active recovery procedure;
- inspect local health and readiness;
- export support bundles under active privacy policy;
- inspect logs and receipts;
- verify installed artifacts;
- diagnose storage, queue, resource, and component state.

Remote support, remote evidence submission, and cloud backup remain optional external capabilities. Their absence does not disable local backup or diagnostics.

### 4.11 Update and release behavior

Loss of connectivity does not invalidate the currently activated compatible release set solely because a newer release may exist.

While offline:

- update discovery can be unavailable;
- remote package retrieval can be unavailable;
- current active releases continue according to their validity and profile policy;
- an offline bundle can be imported when the profile supports that mechanism;
- candidate artifacts remain inactive until verification and compatibility checks pass;
- partial update state is not accepted as authority.

Reconnection does not trigger unreviewed update installation.

### 4.12 Reconnection model

Reconnection is a controlled state transition.

The system:

1. detects the availability of each exact external dependency;
2. stabilizes connectivity before enabling dependent operations;
3. refreshes only the authority and status information allowed by policy;
4. validates queued operations against current decisions, consent, identity, trust, policy, versions, destinations, and expiration;
5. identifies conflicts between local and remote state;
6. presents or applies the declared conflict-resolution procedure;
7. resumes only eligible operations;
8. records results and permanent failures;
9. keeps unrelated local work available throughout the transition.

A queued request records historical user intent. It is not permanent authorization to execute later.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-OFFLINE-001,REQ-OFFLINE-002,REQ-OFFLINE-003,REQ-OFFLINE-004,REQ-OFFLINE-005,REQ-OFFLINE-006,REQ-OFFLINE-007,REQ-OFFLINE-008,REQ-OFFLINE-009,REQ-OFFLINE-010,REQ-OFFLINE-011,REQ-OFFLINE-012,REQ-OFFLINE-013,REQ-OFFLINE-014,REQ-OFFLINE-015,REQ-OFFLINE-016,REQ-OFFLINE-017,REQ-OFFLINE-018,REQ-OFFLINE-019,REQ-OFFLINE-020,REQ-OFFLINE-021,REQ-OFFLINE-022,REQ-OFFLINE-023,REQ-OFFLINE-024,REQ-OFFLINE-025,REQ-OFFLINE-026,REQ-OFFLINE-027,REQ-OFFLINE-028 -->
- **REQ-OFFLINE-001 — SHALL:** The active native kOA baseline start, operate, preserve authoritative local data, create local backups, restore through local recovery procedures, and provide local diagnostics without Internet access or external AI.
- **REQ-OFFLINE-002 — SHALL NOT:** Loss of an optional external service make unrelated native local capabilities unavailable.
- **REQ-OFFLINE-003 — SHALL:** Every capability declare its local, artifact, authority, trust, time, network, provider, queueing, degradation, and reconnection dependencies.
- **REQ-OFFLINE-004 — SHALL:** Offline capability evaluation use the exact unavailable dependency rather than treating all connectivity loss as global system failure.
- **REQ-OFFLINE-005 — SHALL:** A capability remain available offline only when all dependencies required for that capability are locally satisfied and valid.
- **REQ-OFFLINE-006 — SHALL:** A governed operation remain blocked when required identity, trust, consent, policy, time, freshness, decision, exception, or evidence cannot be verified.
- **REQ-OFFLINE-007 — SHALL NOT:** kOA infer or activate a local AI substitute when ChatGPT, Suno, Gamma, the Ariane external voice path, or another external AI surface is unavailable.
- **REQ-OFFLINE-008 — SHALL:** Ariane retain structured local guidance and authorized automation independently from external voice availability.
- **REQ-OFFLINE-009 — SHALL NOT:** The Ariane external voice path authorize actions, execute interface operations directly, replace the Atlas, or disable structured local navigation when unavailable.
- **REQ-OFFLINE-010 — SHALL:** kOA Mediatheque retain local user-directed ingestion, identity, versioning, provenance, visibility enforcement, and deterministic processing supported by installed artifacts.
- **REQ-OFFLINE-011 — SHALL NOT:** kOA Mediatheque infer categories, summarize content, select channels, choose visibility, publish material, or invoke an external AI surface automatically during offline operation.
- **REQ-OFFLINE-012 — SHALL:** SenTient remain optional, isolated, on demand, and non-authoritative, and its absence shall not remove a native baseline capability.
- **REQ-OFFLINE-013 — SHALL:** Resource Governor continue deterministic local admission, prioritization, throttling, suspension, and resource protection while offline.
- **REQ-OFFLINE-014 — SHALL NOT:** Resource Governor become a substitute for Governance Policy Runtime or make authorization, disclosure, consent, or privilege decisions.
- **REQ-OFFLINE-015 — SHALL:** Each component preserve exclusive ownership of its authoritative data while offline.
- **REQ-OFFLINE-016 — SHALL NOT:** Connectivity loss authorize direct writes to another component’s authoritative store or bypass an active gateway or contract.
- **REQ-OFFLINE-017 — SHALL:** Pending cross-component and external operations use durable records with origin, destination, operation, authority context, creation time, revalidation rule, retry state, and final result.
- **REQ-OFFLINE-018 — SHALL NOT:** A queued request execute after reconnection without revalidation against current authority, consent, trust, policy, destination, compatibility, and expiration.
- **REQ-OFFLINE-019 — SHALL:** Publication remain distinct from ingestion, local storage, backup, synchronization, and deterministic local transformation.
- **REQ-OFFLINE-020 — SHALL NOT:** Publication Gateway report successful delivery to an unavailable destination or route around required authorization because connectivity is degraded.
- **REQ-OFFLINE-021 — SHALL:** Installed active artifacts remain the basis of offline execution, and missing optional artifacts shall affect only their dependent capabilities.
- **REQ-OFFLINE-022 — SHALL NOT:** Reconnection automatically download, activate, publish, synchronize, or send an unverified candidate artifact or stale queued operation.
- **REQ-OFFLINE-023 — SHALL:** Time-sensitive authority use the applicable local time-confidence and freshness policy, and affected operations shall remain blocked when required confidence is unavailable.
- **REQ-OFFLINE-024 — SHALL:** Offline backups, restores, exports, and migration operations preserve component ownership, provenance, restrictions, revocations, and active authority state.
- **REQ-OFFLINE-025 — SHALL:** External integrations expose unavailable, narrowed, queued, failed, and restored behavior without representing external output as native authority.
- **REQ-OFFLINE-026 — SHALL:** Reconnection identify conflicts and apply the declared conflict-resolution procedure before replacing authoritative local or remote state.
- **REQ-OFFLINE-027 — SHALL:** Offline failure and reconnect processing produce structured evidence for critical transitions without indiscriminate disclosure of private content.
- **REQ-OFFLINE-028 — SHALL NOT:** A profile, component contract, recipe, cache, migration record, generated context, or current implementation silently weaken the global offline baseline or broaden an external capability into the native baseline.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Offline startup

The offline startup procedure is:

1. Load the active profile and its required local authority.
2. Load the active compatible release identities and installed artifacts.
3. Validate local component stores, queues, trust roots, policy bundles, and required runtime assets.
4. Start critical local services in dependency order.
5. Classify each exact external dependency as reachable, unreachable, unauthorized, incompatible, or not configured.
6. Start native components without waiting indefinitely for optional external dependencies.
7. Mark each capability according to its satisfied dependency envelope.
8. Disable external-only controls that cannot execute.
9. preserve structured local alternatives where they exist;
10. expose actionable local diagnostics without requiring remote telemetry;
11. record the startup result and any blocked profile requirement.

An optional provider does not delay the usable local system through repeated blocking retries.

### 6.2 Transition from connected to offline

When an active external dependency becomes unavailable:

1. Identify the affected integration and in-flight operations.
2. Stop creating new operations that require that dependency unless durable queueing is explicitly allowed.
3. Complete locally safe atomic work or roll it back according to its contract.
4. Mark remote delivery as unconfirmed until an authoritative receipt exists.
5. Persist eligible pending work with its authority and revalidation context.
6. Disable or narrow the affected interface control.
7. keep unrelated local components available;
8. protect local authoritative data and in-progress local writes;
9. reduce retry pressure through deterministic backoff or suspension;
10. record the transition without copying sensitive payloads into logs.

### 6.3 Steady offline operation

During steady offline operation:

1. Local health is evaluated independently from provider reachability.
2. Native services use local authoritative data and active installed artifacts.
3. External-only operations remain unavailable, narrowed, or durably queued according to contract.
4. Resource Governor protects interactive and critical local work.
5. kOA Mediatheque background derivatives can be delayed without blocking ingestion or local access.
6. SenTient remains stopped unless an allowed local profile explicitly activates it.
7. Ariane uses structured local input and local Atlas execution.
8. Backup, restore preparation, evidence capture, and diagnostics remain local.
9. Time and trust uncertainty are surfaced to affected authority checks.
10. No unavailable external capability is silently replaced by inferred behavior.

### 6.4 Local queue admission

Before an external or cross-boundary operation enters a durable queue:

1. Resolve the owning component.
2. Identify the exact intended operation and destination.
3. Verify that queueing is permitted for that operation class.
4. Record the user or system intent.
5. Record the authority, consent, decision, policy, and exception context.
6. Record the source version and payload reference without duplicating authoritative data unnecessarily.
7. Record expiration and mandatory revalidation conditions.
8. identify whether later human confirmation is required;
9. reject queueing when delayed execution would be unsafe or semantically invalid;
10. return a local receipt that distinguishes queue acceptance from final completion.

### 6.5 Reconnection

The reconnection procedure is:

1. Detect and stabilize each recovered dependency independently.
2. Avoid enabling dependent controls on a single transient success.
3. Refresh required remote identity, trust, consent, policy, destination, compatibility, and provider-status information.
4. Compare active local and remote versions.
5. Classify conflicts before mutation.
6. Revalidate every pending operation using current authority.
7. Request renewed human confirmation where the operation, elapsed time, destination, content, policy, or risk requires it.
8. Execute eligible operations in a bounded and resource-governed order.
9. Record authoritative completion receipts.
10. Retain permanent failure and rejection evidence.
11. Remove completed queue entries through the applicable retention policy.
12. Keep local native capabilities available during reconciliation.

### 6.6 Synchronization conflict handling

A synchronization conflict is handled by:

1. preserving both candidate states;
2. identifying canonical ownership for each field or object;
3. comparing versions, lineage, receipts, and applicable policy;
4. applying an automatic merge only when the contract defines a deterministic merge;
5. escalating an ambiguous or authority-sensitive conflict to human review;
6. avoiding last-writer-wins when it could overwrite authoritative work silently;
7. recording the selected result and rejected alternative;
8. regenerating affected indexes, projections, and contexts after authority is stable.

### 6.7 Offline update import

When a profile supports offline update bundles:

1. Receive the bundle through the approved import boundary.
2. Preserve the currently active release.
3. Verify bundle structure, identity, provenance, signatures, compatibility, and profile applicability.
4. inspect required system, services, governance, and knowledge channel relationships;
5. stage candidate artifacts separately from active artifacts;
6. execute applicable tests;
7. create activation evidence;
8. activate atomically according to the artifact class;
9. retain rollback or forward-repair capability;
10. reject incomplete, incompatible, unauthorized, or unverifiable bundles.

### 6.8 Recovery after local failure

Offline recovery:

1. enters the profile-defined recovery environment;
2. identifies the last verified active release and data state;
3. protects authoritative user data before repair;
4. verifies available backups and recovery artifacts;
5. restores component stores through their owning contracts;
6. preserves provenance, restrictions, and queue state;
7. validates cross-component references;
8. starts only the capabilities whose dependencies validate;
9. records degraded or blocked capabilities;
10. avoids contacting external services unless the operator explicitly selects an approved recovery path.

## 7. Failure States and Safe Degradation

| Failure state | Local behavior | Unavailable or blocked behavior | Recovery evidence |
| --- | --- | --- | --- |
| Internet route unavailable | Native local services continue. | External AI, remote synchronization, remote publication, remote updates, and remote support are unavailable or queued according to contract. | Connectivity transition record |
| Name resolution unavailable | Existing local addresses and local services continue where configured. | Operations requiring unresolved external names remain unavailable. | Resolver health record |
| One external provider unavailable | Only that integration narrows or stops. | Provider-dependent operation | Integration-state record |
| External provider authentication fails | Local system continues and the integration reports authorization failure. | New transfer to that provider | Authentication failure record |
| ChatGPT unavailable | Manual local workflow remains available. | ChatGPT-dependent external step | Integration-state record |
| Suno unavailable | Local kOA Mediatheque media management remains available. | Suno-dependent external generation step | Integration-state record |
| Gamma unavailable | Local content and presentation artifacts remain available. | Gamma-dependent external generation step | Integration-state record |
| Ariane voice path unavailable | Structured goals, commands, guidance, and approved automation remain available. | Voice input | Voice-path state record |
| Atlas unavailable or incompatible | Ariane stops affected navigation safely. | Guidance or automation requiring that Atlas | Atlas validation result |
| Governance policy unavailable where required | Previously permitted read-only local access can continue only when active policy allows it. | New governed authorization, disclosure, publication, or privilege decision | Policy-runtime record |
| Trust status is stale | Low-risk local behavior can continue only when policy explicitly permits it. | Operations requiring fresh trust status | Trust-decision record |
| Clock confidence insufficient | Non-time-sensitive local work continues. | Time-sensitive authority and expiration decisions | Clock-confidence record |
| Remote destination unavailable | Local request can remain queued when allowed. | Final delivery and success receipt | Queue and destination record |
| Queue storage unavailable | Existing local authoritative work remains protected. | New delayed external operations | Queue-health record |
| Queue item expires | Local data remains intact. | Delayed execution | Expiration receipt |
| Consent or authority changes while queued | Local data remains intact and the queue item is retained as history. | Execution under stale consent or authority | Revalidation rejection |
| Remote and local state conflict | Both candidate states remain preserved. | Silent overwrite | Conflict record |
| Update service unavailable | Current active compatible release continues. | Online update discovery and retrieval | Update-service state |
| Offline bundle verification fails | Current active release continues. | Candidate activation | Verification evidence |
| Backup target unavailable | Local work continues when local durability remains safe. | Backup completion claim | Backup failure record |
| Local storage pressure rises | Resource Governor slows background work and protects critical writes. | New non-critical work when reserve would be violated | Resource decision |
| kOA Mediatheque derivative worker unavailable | Originals, versions, metadata, and visibility remain available. | New derivative generation | Worker-state record |
| SenTient unavailable | Native baseline remains available. | Requested SenTient task | Optional-component state |
| Remote support unavailable | Local diagnostics and support-bundle creation continue. | Remote session and upload | Support-state record |
| Audit export unavailable | Local protected evidence continues to accumulate within limits. | Remote evidence submission | Evidence-queue record |

Safe degradation preserves the smallest safe local capability. It does not:

- widen access;
- invent authority;
- bypass Publication Gateway;
- skip consent;
- substitute Resource Governor for policy;
- write directly across component stores;
- declare queued work complete;
- treat stale data as fresh;
- activate unverified artifacts;
- infer AI output;
- disable all local operation because one external dependency failed.

## 8. Cross-Component Interactions

### 8.1 Component ownership

Each component owns its authoritative data and decides whether a requested local operation is valid inside its contract. Offline operation does not change ownership.

A component can emit an event, request, receipt, or artifact for another component. The receiving component validates and accepts it through its own contract.

### 8.2 Resource Governor and Governance Policy Runtime

Resource Governor decides whether sufficient local resources exist and how permitted workloads are prioritized.

Governance Policy Runtime decides whether governed actions are authorized where an active profile deploys it.

An operation can require both decisions:

```text
governance authorization
  -> resource admission
  -> component execution
  -> result verification
  -> evidence
```

A positive resource decision does not authorize an operation. A positive policy decision does not guarantee resource availability.

### 8.3 Queued publication to UCKK

When offline, a UCKK publication request may be queued locally but is not delivered. On reconnection, Publication Gateway revalidates authorization before UCKK Publication Bridge packages and transports the approved representation.

Publication Gateway governs cross-domain release and external publication.

Offline ingestion can complete locally while external publication remains unavailable. A queued publication request remains distinct from the kOA Mediatheque media record and requires current revalidation before delivery.

### 8.4 Ariane and application components

Ariane uses local Atlases, component-visible state, declared actions, safety policy, and driver capabilities.

Ariane does not mutate another component’s authoritative data through hidden database access. It interacts through the supported user interface or declared component contract and verifies the observable result.

### 8.5 Identity, trust, and time

Components request identity and trust decisions through declared interfaces. They do not create their own broader fallback authority when a central or profile-required trust source is unavailable.

Where local cached status is allowed, the cache has a declared validity and scope. Expiration or uncertainty is visible to the requesting operation.

### 8.6 Backup and restore

Backup collects component-authorized snapshots or exports. Restore returns data through component-owned procedures.

Backup and restore preserve:

- data ownership;
- object identity;
- versions;
- provenance;
- visibility;
- cultural-rights restrictions;
- consent and revocation state;
- queue state;
- release identity;
- migration state.

### 8.7 External integration removal

An optional integration can be removed or disabled without breaking the native core.

Removal includes:

- disabling new requests;
- resolving or rejecting pending requests;
- preserving local source data;
- retaining required receipts;
- removing credentials according to policy;
- updating generated contexts and user-visible capability state;
- proving that unrelated local capabilities remain available.

### 8.8 Generated AI contexts

Generated AI contexts can help an agent identify the applicable offline rules for a profile or component. They remain derived projections.

When a context is missing or stale, the agent reads active canonical sources. It does not guess a fallback capability, external provider, local AI implementation, queue policy, or conflict rule.

## 9. Decision Closure and Prohibited Assumptions

The decisions listed in the metadata close the offline model used by this document.

The following assumptions are prohibited:

1. Offline means that every local network is unavailable.
2. Online means that every external provider is usable.
3. Provider reachability proves provider authorization.
4. A cached external result is current or authoritative.
5. The native baseline includes an unspecified local AI.
6. SenTient replaces unavailable external AI.
7. SenTient is required for normal user operation.
8. Voice availability defines Ariane availability.
9. Ariane requires Internet for structured local navigation.
10. kOA Mediatheque requires AI to classify, summarize, or publish content.
11. A thumbnail or transcode is AI analysis.
12. Ingestion implies publication permission.
13. A queued publication is already published.
14. A queued request remains authorized indefinitely.
15. Reconnection authorizes automatic replay.
16. The newest remote version automatically wins a conflict.
17. Last-writer-wins is safe for authoritative data.
18. Connectivity loss permits direct database writes across components.
19. Resource availability implies authorization.
20. Authorization implies resource availability.
21. Current local implementation behavior is the canonical offline contract.
22. An optional integration outage is global system failure.
23. Remote update unavailability invalidates the active local release.
24. A reconnect event authorizes automatic update installation.
25. A local backup requires cloud access.
26. Remote support unavailability removes local diagnostics.
27. A stale trust or consent record can be extended implicitly.
28. An offline profile can weaken global data-ownership or AI-boundary rules.
29. A recipe defines the universal retry, queue, network, or synchronization policy.
30. A generated context proves that omitted capabilities or restrictions do not exist.

When a requested behavior depends on an absent canonical decision, undefined conflict policy, missing profile rule, unavailable authority source, or unknown external-provider behavior, the affected behavior remains blocked until the owning registry or contract defines it.

## 10. Validation Criteria

This document is conformant when all of the following checks pass:

1. The file is registered as `DOC-SYS-008` at `02-system/08-offline-behavior.md`.
2. The document class is `normative_markdown`, status is `active`, language is `en`, layer is `system`, and scope is `global`.
3. Metadata matches `generated/document-index.json`.
4. All canonical references resolve through the active authority release.
5. Every listed decision has accepted status.
6. Every listed requirement exists with the rendered statement, strength, scope, source decision, owner, validation method, and applicable locks.
7. Every listed lock resolves and its assertions pass.
8. All eleven mandatory sections exist in the required order.
9. Normative keywords appear only inside the generated requirement block.
10. The native baseline can initialize without Internet and without external AI.
11. Loss of each optional external provider affects only its dependent capabilities.
12. Ariane structured local navigation remains available when external voice is unavailable.
13. kOA Mediatheque local ingestion and deterministic processing do not invoke AI or publish automatically.
14. SenTient remains optional, isolated, on demand, and non-authoritative.
15. Resource Governor remains deterministic and separate from Governance Policy Runtime.
16. Component data ownership remains unchanged while offline.
17. No offline fallback permits direct writes into another component’s authoritative store.
18. Durable queue records include authority and revalidation context.
19. Queue acceptance is distinguishable from final operation completion.
20. Reconnection revalidates every eligible queued operation.
21. Expired, revoked, incompatible, or unauthorized queued operations do not execute.
22. Synchronization conflicts preserve candidates until the declared resolution procedure selects a result.
23. Offline update activation rejects incomplete or unverifiable bundles.
24. Current active compatible releases remain usable when remote update discovery is unavailable.
25. Time and trust uncertainty block only the operations requiring unavailable confidence.
26. Local backup, restore, and diagnostics function without remote services.
27. Critical offline and reconnect transitions produce protected structured evidence.
28. No external output becomes canonical without component acceptance.
29. No unresolved marker, implicit local AI, silent provider substitution, or parallel authority appears.
30. Ordinary Markdown file-content hashes are not required.
31. Full documentation validation returns `pass` before authority activation.

## 11. Non-Normative Examples

### 11.1 Internet outage during normal user work

The Internet route fails while a user manages local Orgo tasks, reads installed Kristal content, organizes kOA Mediatheque media, and uses Ariane guidance. Those local capabilities continue. ChatGPT controls and Ariane voice input show unavailable. No global system-failure state is reported.

### 11.2 Offline kOA Mediatheque ingestion

A user imports a video into the kOA Mediatheque, selects local metadata and visibility, and confirms ingestion. The Mediatheque verifies the file, creates the initial version, stores provenance, and schedules a deterministic preview. It does not summarize the video, select a publication channel, or send it to an external service.

### 11.3 Ariane without voice

The external voice provider is unavailable. The user selects a predefined goal in Ariane. Ariane loads the local Atlas, presents a route, requests confirmation for a sensitive action, executes an approved local interaction, and verifies the result.

### 11.4 Queued publication

A user approves a publication request while the external destination is unavailable. The local system records a pending request, not a completed publication. After reconnection, consent has expired. Revalidation rejects the request and records the reason.

### 11.5 Stale trust status

A local credential is present, but the requested high-impact operation requires a fresh remote revocation check. Local read-only use continues under policy. The high-impact operation remains blocked until fresh status is available.

### 11.6 Optional SenTient task

A user requests an isolated SenTient task on a profile that supports it. The workbench cannot start because its local dependencies are missing. The task fails locally without affecting Orgo, Kristal, Konnaxion, kOA Mediatheque, Ariane, the language runtime, or Resource Governor.

### 11.7 Reconnection conflict

A local object and its remote counterpart were both modified while disconnected. The synchronization contract has no deterministic field-level merge for the conflict. The system preserves both versions and requests human resolution instead of applying last-writer-wins.

### 11.8 Offline update bundle

An operator imports a signed offline bundle. Verification finds that its governance channel version is incompatible with the selected services release. The current release remains active, and the candidate bundle is rejected without partial activation.

### 11.9 Remote support outage

Remote support is unavailable during a local incident. The operator still runs local diagnostics, verifies installed artifacts, exports a privacy-filtered support bundle, and stores it for later authorized transmission.

### 11.10 Resource pressure while offline

kOA Mediatheque preview generation and a developer build create storage and CPU pressure. Resource Governor delays the preview job and lowers build resources while preserving local writes and Ariane responsiveness. It does not decide whether either operation is authorized.
