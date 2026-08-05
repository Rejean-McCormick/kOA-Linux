<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-PROFILE-004",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "profile",
  "scope": [
    "profile:user_lightweight"
  ],
  "canonical_refs": [
    "contracts/profiles/user-lightweight.profile.json",
    "generated/profile-catalog.json",
    "contracts/system.contract.json",
    "contracts/integrations/uckk-import.integration.json",
    "contracts/artifact-contracts/uckk-learning-package.schema.json",
    "contracts/artifact-contracts/uckk-import-receipt.schema.json"
  ],
  "decision_ids": [
    "DEC-PROFILE-001",
    "DEC-USER-001",
    "DEC-AI-001",
    "DEC-SENT-001",
    "DEC-UCKK-EXT-001",
    "DEC-ARI-001",
    "DEC-GOV-001",
    "DEC-GATE-001",
    "DEC-DATA-001",
    "DEC-OFFLINE-001",
    "DEC-HW-001",
    "DEC-CONTAINER-001",
    "DEC-K8S-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-USER-001",
    "REQ-USER-002",
    "REQ-USER-003",
    "REQ-USER-004",
    "REQ-USER-005",
    "REQ-USER-006",
    "REQ-USER-007",
    "REQ-USER-008",
    "REQ-USER-009",
    "REQ-USER-010",
    "REQ-USER-011",
    "REQ-USER-012",
    "REQ-USER-013",
    "REQ-USER-014",
    "REQ-USER-015",
    "REQ-USER-016",
    "REQ-USER-017",
    "REQ-USER-018",
    "REQ-USER-019",
    "REQ-USER-020",
    "REQ-USER-021",
    "REQ-USER-022",
    "REQ-USER-023",
    "REQ-USER-024"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-USER-001",
    "LOCK-USER-002",
    "LOCK-USER-003",
    "LOCK-USER-004",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SENT-001",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-MEDIATHEQUE-002",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-DATA-001",
    "LOCK-OFFLINE-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-SYS-000"
  ],
  "tags": [
    "profile",
    "user",
    "lightweight",
    "offline",
    "local-first",
    "resource-bounded"
  ]
}
KOA:DOC-META:END -->

# User Lightweight Profile

## 1. Purpose

The User Lightweight profile defines a small, locally operable kOA endpoint for ordinary personal or limited shared use. It provides essential user-facing capabilities without requiring a developer toolchain, a sovereign hub, a control plane, a local AI stack, a permanent Internet connection, or orchestration infrastructure.

The profile is intended for devices where simplicity, predictable resource use, local continuity, understandable administration, and recoverability are more important than hosting every kOA component.

Its objectives are to:

- provide a coherent local user experience on maintained Linux hardware;
- preserve useful local operation during network loss;
- support deterministic local knowledge and media handling;
- preserve Ariane navigation without external voice services;
- keep external AI and creative services optional and explicitly invoked;
- prevent optional components from consuming resources continuously;
- separate local user data from caches, generated derivatives, and external-service outputs;
- support safe update, backup, restore, export, and removal;
- avoid silently claiming developer, hub, production, sovereign-node, or high-assurance conformance.

This document explains the profile. Canonical profile membership and machine-readable values are owned by `contracts/profiles/user-lightweight.profile.json`.

## 2. Scope

### 2.1 Included deployment class

The profile applies to a maintained Linux endpoint used primarily by one person or a small explicitly configured local user group.

Typical deployments include:

- a personal laptop;
- a compact desktop;
- a low-power home or community terminal;
- an offline-capable field endpoint;
- a local knowledge and media station;
- a user-facing appliance that does not adopt the separate appliance-shell profile;
- a client endpoint connected occasionally to a sovereign hub.

### 2.2 Included capabilities

The profile can include:

- local authentication and user session management;
- local navigation and accessibility;
- a lightweight local interface;
- local Kristal reading and bounded knowledge storage;
- deterministic kOA Mediatheque ingestion, preview, export, backup, and offline retrieval;
- bounded validation and explicit acceptance of selected UCKK learning packages;
- local Ariane navigation and action verification;
- controlled access to remote or local hub services;
- optional user-triggered external integrations;
- local audit and diagnostic records appropriate to the endpoint;
- local backup, restore, and sovereignty export;
- safe update and rollback.

A deployment is not required to activate every capability.

### 2.3 Excluded profile claims

This profile does not establish:

- a development workstation;
- a build farm;
- a sovereign hub;
- a sovereign Linux node;
- a control plane;
- a high-assurance environment;
- an unrestricted public server;
- a multi-tenant institutional service;
- a production database cluster;
- a Kubernetes cluster;
- a native AI workstation;
- a mandatory SenTient installation;
- a complete offline mirror of every remote service.

### 2.4 Profile boundaries

Profile rules apply only to deployments that explicitly adopt `user_lightweight`.

A deployment can communicate with a sovereign hub without inheriting the hub profile. A deployment can run on a node that independently conforms to another profile, but one profile does not silently prove another.

An overlay applies only when the deployment contract explicitly adopts that overlay and passes the related validation.

### 2.5 Resource philosophy

The profile does not define a universal processor, memory, storage, or accelerator minimum. Hardware suitability depends on the selected capabilities, local data volume, accessibility needs, display environment, and offline retention target.

The machine-readable profile owns the selected capacity envelope. Conformance depends on measured responsiveness, storage reserve, recovery capacity, and bounded background resource use rather than a marketing hardware class.

## 3. Canonical References

| Canonical reference | Responsibility |
| --- | --- |
| `contracts/profiles/user-lightweight.profile.json` | Owns machine-readable profile membership, selected components, resource policy, hardware envelope, security claims, offline claims, lifecycle behavior, and conformance requirements. |
| `generated/profile-catalog.json` | Owns profile identity, classification, relationships, and discoverability. |
| `contracts/system.contract.json` | Owns global component boundaries, data ownership, external-integration boundaries, safe degradation, and system-wide behavior. |

Supporting authority is owned by:

- `generated/decision-index.json`;
- `generated/requirements-index.json`;
- `generated/assertion-index.json`;
- `generated/component-catalog.json`;
- `contracts/integration-types.contract.json`;
- `contracts/release-channels.contract.json`;
- `contracts/artifact-classes.contract.json`;
- `generated/test-catalog.json`;
- `generated/evidence-catalog.json`;
- `generated/exception-index.json`.

Narrative examples and implementation recipes do not override the machine-readable profile.

## 4. Model and Responsibilities

### 4.1 Profile model

The User Lightweight profile is a primary deployment profile with explicit component selection.

A conforming deployment records:

- profile identity and version;
- host operating-system family;
- selected components;
- selected optional integrations;
- local data locations;
- external data movements;
- local resource limits;
- offline-capability claims;
- backup and restore targets;
- active Release Set;
- profile-specific test and evidence references;
- adopted overlays;
- active exceptions.

Undeclared components, overlays, integrations, or profile capabilities do not become part of the conformance claim.

### 4.2 User interface responsibility

The local interface presents:

- available local capabilities;
- unavailable remote capabilities;
- degraded or offline state;
- pending operations;
- active external-service boundaries;
- the current user and local authority context;
- storage and backup status;
- update and recovery status;
- consent and publication checkpoints;
- actionable errors.

The interface does not hide network dependence or substitute a different service silently.

### 4.3 Ariane responsibility

Ariane provides local navigation, structured controls, local Atlas interaction, and action verification without requiring external voice processing.

External voice can extend Ariane through an approved integration. Failure or removal of the external voice surface leaves local navigation available.

### 4.4 UCKK responsibility

UCKK performs native ingestion through deterministic local operations, including file intake, integrity checks, user-provided metadata, preview generation, supported transcoding, deterministic text extraction, storage, export, backup, and restore.

External creative services such as Suno or Gamma remain optional adapters. They are not part of native ingestion and are invoked only through an explicit user action and controlled re-import.

UCKK Import Bridge controls inbound retrieval and quarantine; the kOA Mediatheque controls local acceptance. Publication Gateway controls governed outbound release, followed by the UCKK Publication Bridge. The directional responsibilities remain separate.

### 4.5 Kristal responsibility

Kristal provides local access to approved knowledge artifacts and metadata. The endpoint can retain a bounded local working set and distribution cache.

Kristal does not own user workflow state, publication approval, access-control decisions, or application-specific mutable records.

### 4.6 External-service responsibility

An external surface is optional. Each invocation identifies:

- the provider or surface;
- the selected input;
- the purpose;
- the expected output;
- relevant retention and reuse conditions;
- the receiving component;
- the re-import and acceptance step.

Returned output remains candidate material until accepted by the responsible component.

### 4.7 SenTient responsibility

SenTient is optional, isolated, task-activated, and non-authoritative.

The profile does not require SenTient for:

- startup;
- navigation;
- local knowledge access;
- deterministic kOA Mediatheque processing and UCKK package validation;
- backup;
- restore;
- offline operation;
- profile conformance.

When installed, SenTient uses isolated dependencies, storage, temporary data, service identity, network policy, CPU, and memory. It cannot write component-owned authoritative data directly.

### 4.8 Governance responsibility

Governance Policy Runtime is required only when the selected deployment capabilities need local governed authorization, publication, consent, or privilege evaluation.

Resource Governor remains a separate authority. It controls resources and does not decide disclosure, consent, identity, or publication.

When a required governance service is unavailable, affected governed operations stop while unrelated local capabilities continue where safe.

### 4.9 Data responsibility

Each component owns its authoritative data.

The endpoint separates:

- user-authored or imported authoritative data;
- component operational state;
- configuration;
- credentials and secrets;
- caches;
- previews and reproducible derivatives;
- diagnostic records;
- external-service candidate outputs;
- backup data;
- quarantine data.

Cross-component authoritative writes occur only through a declared API, event, gateway, or governed import contract.

### 4.10 Operator responsibility

The endpoint operator is responsible for:

- selecting profile capabilities;
- protecting local credentials;
- maintaining supported software;
- reviewing storage and backup status;
- applying validated updates;
- resolving visible degraded states;
- controlling external integrations;
- preserving user exit and export capability.

Operator access does not automatically grant cultural, publication, or data authority.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-USER-001,REQ-USER-002,REQ-USER-003,REQ-USER-004,REQ-USER-005,REQ-USER-006,REQ-USER-007,REQ-USER-008,REQ-USER-009,REQ-USER-010,REQ-USER-011,REQ-USER-012,REQ-USER-013,REQ-USER-014,REQ-USER-015,REQ-USER-016,REQ-USER-017,REQ-USER-018,REQ-USER-019,REQ-USER-020,REQ-USER-021,REQ-USER-022,REQ-USER-023,REQ-USER-024 -->
- **REQ-USER-001 — SHALL:** A User Lightweight deployment declare its profile version, selected capabilities, components, integrations, data locations, resource limits, Release Set, overlays, exceptions, tests, and evidence.
- **REQ-USER-002 — SHALL NOT:** Adoption of this profile imply developer, hub, sovereign-node, control-plane, build-farm, production-cluster, or high-assurance conformance.
- **REQ-USER-003 — SHALL:** The endpoint provide useful local operation without an Internet connection, external AI surface, central control plane, or remote voice service.
- **REQ-USER-004 — SHALL:** The interface display offline, degraded, queued, external, and blocked states in a form understandable to the local user.
- **REQ-USER-005 — SHALL NOT:** The endpoint silently replace an unavailable local or external capability with another provider, model, service, or data path.
- **REQ-USER-006 — SHALL:** Ariane local navigation and action verification remain available without external voice processing.
- **REQ-USER-007 — SHALL:** Local kOA Mediatheque processing and offline validation of complete UCKK learning packages remain deterministic and locally operable.
- **REQ-USER-008 — SHALL NOT:** kOA Mediatheque ingestion or UCKK learning-package import automatically invoke Suno, Gamma, ChatGPT, Ariane external voice, SenTient, or another AI service.
- **REQ-USER-009 — SHALL:** Every external-service invocation be explicit, minimized, attributable, reviewable, and bound to controlled re-import and component acceptance.
- **REQ-USER-010 — SHALL NOT:** External output become authoritative or mutate authoritative component data directly.
- **REQ-USER-011 — SHALL:** SenTient, when present, remain optional, stopped by default, task-activated, resource-isolated, and non-authoritative.
- **REQ-USER-012 — SHALL NOT:** Profile conformance depend on SenTient, Kubernetes, a GPU, a local model runtime, a public cloud, or a permanent network connection.
- **REQ-USER-013 — SHALL:** Each component retain logical ownership of its authoritative data.
- **REQ-USER-014 — SHALL NOT:** Components write directly into another component’s authoritative storage.
- **REQ-USER-015 — SHALL:** UCKK Import Bridge, UCKK Publication Bridge, Publication Gateway, and kOA Mediatheque acceptance remain separate authorities and execution boundaries.
- **REQ-USER-016 — SHALL:** Governed publication, disclosure, consent, and privilege decisions fail closed when required authority cannot be verified.
- **REQ-USER-017 — SHALL:** Resource Governor preserve essential local capabilities by limiting, delaying, or denying optional heavy work under resource pressure.
- **REQ-USER-018 — SHALL:** Background services and optional components use bounded CPU, memory, storage, process, queue, and network resources.
- **REQ-USER-019 — SHALL:** Authoritative user data, secrets, caches, generated derivatives, external outputs, diagnostics, quarantine, and backups remain distinguishable.
- **REQ-USER-020 — SHALL:** Updates validate identity, compatibility, trust, migration, evidence, and rollback or forward-repair behavior before activation.
- **REQ-USER-021 — SHALL NOT:** A failed candidate update replace the last known good active state.
- **REQ-USER-022 — SHALL:** Backup, restore, export, and profile removal preserve user control and avoid dependence on an unavailable external provider.
- **REQ-USER-023 — SHALL:** Queued remote actions be revalidated after reconnection before transmission or publication.
- **REQ-USER-024 — SHALL NOT:** A generated context, example, recipe, migration record, implementation convenience, or undeclared overlay silently broaden this profile.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Initial profile activation

The activation procedure is:

1. Verify the host is a maintained Linux environment.
2. Select the exact profile version.
3. Select required and optional capabilities.
4. Resolve component contracts.
5. Resolve explicit overlays and exceptions.
6. Create component-owned data locations.
7. Create secret and credential references.
8. Configure local resource budgets.
9. Configure network and external-service policies.
10. Configure backup and restore targets.
11. Install a compatible Release Set.
12. Run profile tests.
13. Record evidence.
14. Activate only after validation passes.

### 6.2 Local session startup

At session startup:

1. Verify the active Release Set.
2. Verify local data and configuration compatibility.
3. Start essential local services.
4. Apply resource budgets.
5. Load local identity and authority state.
6. Determine network and remote-service availability.
7. Mark unavailable capabilities visibly.
8. Keep external and heavy optional services stopped.
9. Restore pending-operation state without releasing it.
10. Present the local interface.

A missing optional service does not prevent startup.

### 6.3 Optional capability activation

An optional capability activation includes:

1. Identify the requested capability.
2. Resolve its component or integration contract.
3. Check local resources.
4. Check user authority and consent.
5. Check network and credential state where relevant.
6. Start only the bounded capability.
7. expose its external or non-authoritative status;
8. Record the invocation where required.
9. Stop and release resources when the task ends.

### 6.4 Offline transition

When connectivity is lost:

1. Mark remote capabilities unavailable.
2. Preserve local sessions and data.
3. Stop new remote transmissions.
4. Retain eligible pending requests in durable local queues.
5. Continue deterministic local processing.
6. Continue Ariane local navigation.
7. Continue local Kristal and UCKK access.
8. Record time or trust uncertainty.
9. Block operations that require fresh remote authority.
10. Expose the degraded state.

### 6.5 Reconnection transition

When connectivity returns:

1. Confirm stable network availability.
2. Refresh trust and revocation state where required.
3. Revalidate credentials.
4. Revalidate consent and authority.
5. Revalidate target and integration contracts.
6. Revalidate queued payload identity and minimization.
7. Detect local and remote conflicts.
8. Present conflicts or changed conditions to the user.
9. Release only operations that still pass.
10. Retain, cancel, or replace invalidated operations.
11. Record transmission and publication receipts.

Reconnection is not an automatic authorization event.

### 6.6 Update transition

The update sequence is:

`text
discovered
 -> downloaded_or_imported
 -> verified
 -> staged
 -> tested
 -> compatible
 -> activated
 -> observed
 -> retained_or_repaired
`

A candidate that fails verification, compatibility, migration, testing, or activation returns the deployment to the last known good state or enters the documented forward-repair path.

### 6.7 Backup and restore

Backup preparation includes:

1. Classify authoritative, sensitive, reproducible, and transient data.
2. Select the authorized backup scope.
3. Verify target availability and access control.
4. Produce an integrity-protected backup bundle.
5. Record profile and Release Set versions.
6. Record included data authorities.
7. Test restoration on a compatible clean environment.
8. Record restoration evidence.

Restore includes identity, authority, schema, migration, profile, Release Set, and post-restore health validation.

### 6.8 Profile removal

Removal includes:

1. Export user-controlled authoritative data.
2. Export active consent, provenance, and publication records where applicable.
3. Verify the export.
4. Stop optional and essential services.
5. Remove credentials and local service identities.
6. Remove component data according to the chosen exit policy.
7. Preserve or remove backups according to explicit user choice and policy.
8. Record systems or providers outside local control.
9. Verify that removal does not affect another profile or deployment.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Preserved capability | Denied capability |
| --- | --- | --- | --- |
| Internet unavailable | Enter visible offline state. | Local navigation, knowledge, deterministic media handling, backup, export | Remote synchronization and external services |
| External AI unavailable | Disable that assistance only. | Native local operation | Requested external assistance |
| External voice unavailable | Continue local Ariane controls. | Keyboard, pointer, structured controls, local action verification | Remote voice interaction |
| SenTient unavailable | Continue without substitution. | All baseline profile capabilities | SenTient task |
| Resource pressure | Protect essential services and user data. | Local session, storage, navigation, recovery | New optional heavy work |
| Storage reserve too low | Stop non-essential ingestion and generation. | Read access, export, cleanup, recovery | New large writes |
| Governance runtime unavailable when required | Block new governed decisions. | Existing safe local reads where policy permits | New publication, disclosure, or privilege decision |
| Publication Gateway unavailable | Keep publication local and pending. | Local editing and storage | Cross-domain publication |
| UCKK Import Bridge unavailable | Preserve existing local and previously accepted content. | Reading, local adaptation, export, backup | New UCKK retrieval and import |
| Identity status stale | Apply declared expiry policy. | Non-sensitive local functions | Operations requiring fresh authority |
| Clock uncertain | Mark time uncertainty. | Non-time-sensitive local work | Expiry-sensitive authority and release decisions |
| Backup target unavailable | Report degraded protection. | Active local state | Claim of current protected backup |
| Candidate update invalid | Retain current active version. | Existing validated capabilities | Candidate activation |
| Component database unavailable | Degrade only the affected component. | Unrelated component capabilities | Affected authoritative writes |
| Cache corrupt | Rebuild or discard the cache. | Authoritative source data | Use of corrupted derivative |
| External output invalid | Quarantine or reject it. | Original local data | Authoritative import |
| Consent missing | Block affected governed operation. | Unrelated local use | Disclosure, external transfer, or publication |
| Overlay unresolved | Ignore no rules and activate no implicit overlay. | Base profile | Overlay-dependent claim |
| Restore validation fails | Keep restored state inactive. | Existing active state or recovery tools | Restored-state activation |

Safe degradation narrows the affected capability. It does not route around gateways, invent authority, expose secrets, merge component databases, substitute external providers, or discard the last known good state.

## 8. Cross-Component Interactions

### 8.1 Local interface and components

The local interface invokes component APIs with explicit user, action, and data scope. It does not access component databases directly.

A component returns user-facing status that distinguishes success, failure, blocked state, offline state, and queued state.

### 8.2 Ariane and application components

Ariane can request a bounded application action through an approved local interface. The receiving component validates the action and remains the authority for its data.

Action confirmation is required where the application contract classifies the action as consequential.

### 8.3 UCKK and publication

UCKK stores and processes admitted material. A publication request identifies an exact source or bounded derivative and goes through Publication Gateway.

A successful UCKK admission does not imply publication approval.

### 8.4 Kristal and application state

Kristal artifacts can be referenced by local applications. Application-specific workflow and user state remain in the owning component.

A cache of a Kristal artifact does not become the authoritative source unless an explicit artifact contract says otherwise.

### 8.5 Governance and resources

Governance Policy Runtime evaluates authorization, disclosure, consent, and privilege policy where required.

Resource Governor applies CPU, memory, process, storage, queue, and optional-service limits.

Neither authority substitutes for the other.

### 8.6 Local endpoint and sovereign hub

The endpoint can synchronize with a sovereign hub through explicit integration and trust scopes.

The endpoint preserves local identity, data ownership, queueing, consent, and conflict state. The hub does not gain unrestricted local authority merely because it provides synchronization or storage.

### 8.7 External integrations

External integrations receive only minimized, authorized input. Their outputs return through controlled import.

Loss of one integration does not disable unrelated local capabilities or trigger use of another integration without user action.

### 8.8 Backup and migration tools

Backup and migration tools operate through declared data-authority and artifact contracts. They preserve profile version, Release Set, provenance, restrictions, and component ownership.

A restore or migration does not silently reactivate expired or revoked authority.

## 9. Decision Closure and Prohibited Assumptions

The decisions referenced in this document close the profile baseline.

The following assumptions are prohibited:

1. A lightweight user profile is a reduced developer workstation.
2. Every kOA component must be installed.
3. Every installed optional component must start at login.
4. Internet connectivity is required for local correctness.
5. External AI is native functionality.
6. External AI output is authoritative.
7. Failure of external voice disables Ariane.
8. SenTient is required for navigation, knowledge access, media handling, or conformance.
9. SenTient can write authoritative data directly.
10. kOA Mediatheque ingestion or UCKK package import can invoke AI automatically.
11. UCKK admission authorizes publication.
12. Publication Gateway, UCKK Publication Bridge, and UCKK Import Bridge are interchangeable.
13. Resource Governor can decide consent or publication.
14. Governance Policy Runtime can allocate resources.
15. All component data belongs in one database.
16. A local interface can read component databases directly.
17. A shared cache is authoritative data.
18. Reconnection authorizes pending transmission.
19. A candidate update can replace the active version before validation.
20. A lightweight device requires Kubernetes.
21. A GPU is required.
22. One hardware minimum fits every selected capability.
23. A hub connection transfers unrestricted authority to the hub.
24. An undeclared overlay applies automatically.
25. A recipe, example, generated context, or migration note changes profile authority.

When a requested capability depends on unresolved authority, missing consent, incompatible releases, insufficient resources, unavailable trust state, or an undeclared overlay, that capability remains blocked while unrelated local functions continue where safe.

## 10. Validation Criteria

This document is conformant when:

1. It is registered as `DOC-PROFILE-004`.
2. Its path is `03-profiles/04-user-lightweight.md`.
3. Its class is `normative_markdown`.
4. Its status is `active`.
5. Its language is `en`.
6. Its layer is `profile`.
7. Its scope is `profile:user_lightweight`.
8. Its metadata matches `generated/document-index.json`.
9. The machine-readable profile exists and validates.
10. The profile index resolves `user_lightweight`.
11. Every canonical reference resolves.
12. Every listed accepted decision resolves.
13. Every listed requirement resolves and matches the generated block.
14. Every listed lock resolves and passes.
15. The eleven mandatory sections exist in the required order.
16. Normative keywords occur only in the generated requirement block.
17. The profile starts and remains useful without Internet or external AI.
18. Ariane local navigation passes without external voice.
19. Deterministic kOA Mediatheque operations and UCKK learning-package validation pass without AI; accepted content remains available offline.
20. SenTient absence does not affect baseline conformance.
21. Optional heavy services remain stopped until explicitly activated.
22. Resource pressure preserves essential capabilities.
23. Component authoritative data remains isolated by ownership.
24. Direct cross-component authoritative writes fail validation.
25. Publication Gateway, UCKK Publication Bridge, and UCKK Import Bridge remain separate.
26. External-service output requires controlled acceptance.
27. Queued operations are revalidated after reconnection.
28. Update failure preserves the last known good state.
29. Backup, restore, export, and removal tests pass.
30. The selected capacity envelope passes responsiveness, storage-reserve, and recovery tests.
31. No undeclared overlay affects the result.
32. Traceability and active evidence are complete.
33. No unresolved marker, provisional value, parallel authority, or file-content hash requirement appears.
34. Complete documentation validation returns `pass`.

## 11. Non-Normative Examples

### 11.1 Offline personal laptop

A user reads local Kristal material, imports photographs into UCKK, creates previews, and navigates through Ariane while disconnected. Remote synchronization and external creative services are marked unavailable.

### 11.2 Optional external translation

The user selects one paragraph and explicitly sends it to an approved external translation surface. The provider, purpose, selected input, and return path are shown. The result returns as candidate content and is accepted only after review.

### 11.3 Resource pressure

The device has limited free memory. Resource Governor keeps the user session, local storage, and navigation responsive while denying a new SenTient task and pausing non-essential preview generation.

### 11.4 Hub reconnection

The endpoint reconnects to a sovereign hub with several queued changes. Identity, trust, consent, target versions, and conflicts are checked before synchronization. A conflicting edit remains local until the user resolves it.

### 11.5 External voice failure

A remote voice provider is unavailable. Ariane continues with keyboard, pointer, structured controls, and local action verification.

### 11.6 Candidate update failure

A downloaded services-channel candidate fails a migration test. The endpoint retains the active Release Set and records the failed candidate without partially activating it.

### 11.7 Bounded local installation

The user installs only the local interface, Ariane runtime, Kristal runtime, the private offline kOA Mediatheque, Resource Governor, and backup tooling. Optional UCKK publication and import integrations can be enabled independently; the profile does not install or operate the online UCKK Moodle platform. The profile does not require the developer toolchain, SenTient, Kubernetes, or a hub.

### 11.8 Controlled publication

A user prepares an item in UCKK and requests publication to a hub-hosted Konnaxion domain. Publication Gateway verifies consent, audience, policy, and evidence before release. UCKK admission alone is insufficient.

### 11.9 Safe storage exhaustion behavior

Available storage falls below the declared reserve. New large media ingestion stops. Existing material remains readable, and the interface offers export, cleanup, and backup actions.

### 11.10 Profile removal

The user exports authoritative data and provenance, verifies the export, removes local credentials and component data, and records that one external provider may retain prior submitted material under its separate policy.
