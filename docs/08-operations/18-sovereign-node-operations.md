<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-OPS-018",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "operations",
  "scope": [
    "profile:sovereign_linux_node",
    "operations:node",
    "operations:offline",
    "operations:maintenance",
    "operations:recovery"
  ],
  "canonical_refs": [
    "03-profiles/07-sovereign-linux-node.md",
    "03-profiles/11-high-assurance.md",
    "07-security/00-threat-model.md",
    "07-security/11-ai-boundaries.md",
    "08-operations/08-backup.md",
    "08-operations/09-restore.md",
    "08-operations/10-portability-and-exit.md",
    "contracts/profiles/sovereign-linux-node.profile.json",
    "contracts/profiles/high-assurance.profile.json",
    "generated/profile-catalog.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "contracts/integration-types.contract.json",
    "contracts/components/identity-and-trust.component.json",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/components/audit-broker.component.json",
    "contracts/components/koa-node-agent.component.json",
    "contracts/components/resource-governor.component.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-SYS-001",
    "DEC-AUTH-001",
    "DEC-IDENT-001",
    "DEC-DATA-001",
    "DEC-COMP-001",
    "DEC-GOV-001",
    "DEC-PRIV-001",
    "DEC-AI-001",
    "DEC-LIFE-001",
    "DEC-HW-001"
  ],
  "requirement_ids": [
    "REQ-OPS-SOVNODE-001",
    "REQ-OPS-SOVNODE-002",
    "REQ-OPS-SOVNODE-003",
    "REQ-OPS-SOVNODE-004",
    "REQ-OPS-SOVNODE-005",
    "REQ-OPS-SOVNODE-006",
    "REQ-OPS-SOVNODE-007",
    "REQ-OPS-SOVNODE-008",
    "REQ-OPS-SOVNODE-009",
    "REQ-OPS-SOVNODE-010",
    "REQ-OPS-SOVNODE-011",
    "REQ-OPS-SOVNODE-012",
    "REQ-OPS-SOVNODE-013",
    "REQ-OPS-SOVNODE-014",
    "REQ-OPS-SOVNODE-015",
    "REQ-OPS-SOVNODE-016",
    "REQ-OPS-SOVNODE-017",
    "REQ-OPS-SOVNODE-018",
    "REQ-OPS-SOVNODE-019",
    "REQ-OPS-SOVNODE-020",
    "REQ-OPS-SOVNODE-021",
    "REQ-OPS-SOVNODE-022",
    "REQ-OPS-SOVNODE-023",
    "REQ-OPS-SOVNODE-024",
    "REQ-OPS-SOVNODE-025",
    "REQ-OPS-SOVNODE-026",
    "REQ-OPS-SOVNODE-027",
    "REQ-OPS-SOVNODE-028",
    "REQ-OPS-SOVNODE-029",
    "REQ-OPS-SOVNODE-030",
    "REQ-OPS-SOVNODE-031",
    "REQ-OPS-SOVNODE-032",
    "REQ-OPS-SOVNODE-033",
    "REQ-OPS-SOVNODE-034",
    "REQ-OPS-SOVNODE-035",
    "REQ-OPS-SOVNODE-036",
    "REQ-OPS-SOVNODE-037",
    "REQ-OPS-SOVNODE-038",
    "REQ-OPS-SOVNODE-039",
    "REQ-OPS-SOVNODE-040",
    "REQ-OPS-SOVNODE-041",
    "REQ-OPS-SOVNODE-042"
  ],
  "lock_ids": [
    "LOCK-AUTH-001",
    "LOCK-AUTH-002",
    "LOCK-AUTH-003",
    "LOCK-DATA-001",
    "LOCK-COMP-001",
    "LOCK-GOV-001",
    "LOCK-PRIV-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-PROF-011",
    "DOC-SEC-000",
    "DOC-SEC-011",
    "DOC-OPS-008"
  ],
  "tags": [
    "sovereign-linux-node",
    "operations",
    "offline",
    "startup",
    "health",
    "maintenance",
    "release-channels",
    "removable-media",
    "backup",
    "recovery",
    "remote-support",
    "exit"
  ]
}
KOA:DOC-META:END -->

# Sovereign Node Operations

## 1. Purpose

This document defines the operating model for a kOA sovereign Linux node.

A sovereign node is a locally controlled Linux system that can preserve its declared minimum capabilities, identity, governance, evidence, active artifacts, backup, and recovery without requiring continuous Internet access or a remote control plane.

The operating model separates:

- profile composition from daily operation;
- local readiness from remote connectivity;
- health from readiness;
- publication from activation;
- component operation from host privilege;
- application service from recovery service;
- operational backup from complete sovereignty exit;
- standard Linux desktop presentation from the optional appliance shell;
- ordinary operation from high-assurance overlays.

The canonical primary-profile owner is:

```text
contracts/profiles/sovereign-linux-node.profile.json
```

This document owns the node operational states, checks, procedures, degradation, maintenance, incident, recovery, and retirement projection.

## 2. Scope

This document applies to a `sovereign_linux_node` primary profile used as:

- a personal sovereign workstation;
- an institutional or community node;
- an offline or intermittently connected node;
- a local application and artifact consumer;
- a local backup and recovery point;
- a high-assurance endpoint when the overlay is selected;
- an appliance-style node when the overlay is selected.

It covers:

- startup and shutdown;
- local readiness;
- service and component operation;
- network zones;
- identity, trust, governance, and evidence;
- resource and capacity control;
- release-channel operations;
- maintenance and configuration drift;
- backup and restore readiness;
- removable media;
- remote support;
- incident response;
- recovery;
- exit and retirement.

It does not define:

- exact hardware models;
- exact Linux distribution;
- exact desktop environment;
- exact container engine;
- exact service manager;
- exact filesystem or database technology;
- exact RPO or RTO;
- exact network addresses;
- exact update cadence;
- exact high-availability topology;
- mandatory Kubernetes deployment.

GNOME or KDE can provide the standard Linux desktop. The `appliance_shell` overlay can provide a smaller Wayland presentation. Those choices remain profile scoped.

## 3. Canonical References

| Canonical reference | Ownership |
| --- | --- |
| `contracts/profiles/sovereign-linux-node.profile.json` | Primary component membership, topology, resources, storage, network, offline envelope, desktop or service realization, backup, recovery, and operations claims. |
| `03-profiles/04-sovereign-linux-node.md` | Human-readable primary-profile projection. |
| `contracts/profiles/high-assurance.profile.json` | Hardware trust, protected key custody, measured or verified boot, attestation, separation of duties, independent evidence, immutable or offline backups, and recovery controls. |
| `03-profiles/11-high-assurance.md` | Human-readable high-assurance overlay projection. |
| `generated/component-catalog.json` | Component identities, ownership, relationships, prohibited responsibilities, and authoritative data domains. |
| `contracts/components/*.component.json` | Component stores, interfaces, events, states, failures, resources, operations, backup, restore, and conformance. |
| `contracts/release-channels.contract.json` | Independent system, services, governance, and knowledge release channels. |
| `contracts/artifact-classes.contract.json` | Artifact verification, staging, activation, rollback, revocation, retention, and evidence. |
| `contracts/integration-types.contract.json` | Federation, repository, remote support, external AI, storage, and transport boundaries. |
| `07-security/00-threat-model.md` | Threats involving host compromise, supply chain, policy capture, offline downgrade, removable media, recovery, privacy, and exit. |
| `07-security/11-ai-boundaries.md` | External AI, SenTient, voice, no-AI, candidate output, failure, removal, and incident boundaries. |
| `08-operations/08-backup.md` | Component-owned backup checkpoints, encryption, independent copies, restore testing, and retention. |
| `08-operations/09-restore.md` | Clean restore, migration, trust revalidation, index rebuild, workflow resumption, and rollback. |
| `08-operations/10-portability-and-exit.md` | Sovereignty Bundle generation, independent restore, trust handover, and operator-independent exit. |
| `generated/test-catalog.json` | Profile, system, security, lifecycle, operations, exit, and documentation tests. |
| `generated/evidence-catalog.json` | Executed startup, maintenance, activation, backup, incident, recovery, support, and retirement evidence. |

## 4. Model and Responsibilities

### 4.1 Profile composition

A sovereign node has exactly one primary profile:

```text
sovereign_linux_node
```

Compatible overlays can include:

```text
high_assurance
sovereign_offline
appliance_shell
```

Composition follows the profile registry.

Permissions intersect, obligations combine, network exposure becomes the most restrictive applicable rule, and unresolved conflicts block the affected claim.

An overlay does not silently add unrelated application authority.

### 4.2 Minimum local control foundation

The operational control foundation includes the applicable instances of:

- Identity and Trust;
- Governance Policy Runtime;
- Audit Broker;
- kOA Node Agent;
- Resource Governor;
- artifact verification;
- recovery control.

Application components are selected by the primary profile and node purpose.

A node can host Konnaxion, Orgo, Kristal Runtime, SemantiK Architect Runtime, UCKK, Ariane Runtime, Publication Gateway, and other registered components only when profile membership and resources permit them.

SenTient and build-time language tooling remain optional and are not default sovereign-node requirements.

### 4.3 Operator roles

| Role | Responsibility | Boundary |
| --- | --- | --- |
| `node_owner` | Responsibility | Boundary | Cannot bypass governance, signing, or component ownership. |
| `node_operator` | Responsibility | Boundary | Does not receive unrestricted authority or protected signing keys. |
| `security_operator` | Responsibility | Boundary | Does not unilaterally approve high-impact governance or recovery actions. |
| `release_operator` | Responsibility | Boundary | Does not build, sign, approve, and activate the same release unless policy permits the role combination. |
| `recovery_operator` | Responsibility | Boundary | Does not convert backup possession into active authority. |
| `auditor` | Responsibility | Boundary | Does not mutate operational state or grant policy authority. |
| `support_operator` | Responsibility | Boundary | Has no persistent unattended access. |

One person can hold multiple roles only when the active policy permits that combination.

### 4.4 Node states

| State | Meaning |
| --- | --- |
| `provisioned` | Meaning | Profile, identity, storage, trust, and recovery foundations exist but normal services are not ready. |
| `starting` | Meaning | Boot, storage, trust, Release Set, component, and resource verification is in progress. |
| `ready_local` | Meaning | Declared minimum local capabilities are ready without requiring remote services. |
| `connected` | Meaning | Optional remote synchronization, federation, mirrors, support, or integrations are available and authorized. |
| `degraded` | Meaning | One or more capabilities are unavailable or constrained while valid unaffected capabilities remain available. |
| `maintenance` | Meaning | Declared services are restricted for updates, migration, backup, repair, or inspection. |
| `quarantined` | Meaning | Trust, integrity, identity, compromise, or configuration uncertainty blocks normal operation. |
| `recovery` | Meaning | The reduced recovery environment is active and normal service authority is suspended or limited. |
| `retiring` | Meaning | Exports, trust transfer or revocation, credential removal, sanitization, and exit verification are in progress. |
| `retired` | Meaning | The node no longer holds active operational identity, authority, credentials, or governed tenant data. |

Connectivity is an attribute of `ready_local` rather than the definition of readiness.

A node can remain locally ready while remote services are unavailable.

### 4.5 Readiness checks

| Check ID | Check |
| --- | --- |
| `boot_integrity` | Check | Boot chain and profile-declared host integrity result. |
| `storage` | Check | Required filesystems, encryption, capacity, ownership, and integrity. |
| `node_identity` | Check | Node and workload enrollment, credential validity, and revocation. |
| `local_trust` | Check | Trust roots, authority release, policy bundle, and freshness state. |
| `release_set` | Check | Exact active system, services, governance, and knowledge selections. |
| `components` | Check | Required component membership, contracts, stores, interfaces, and migrations. |
| `resources` | Check | CPU, memory, storage, process, queue, and I/O capacity for protected operation. |
| `audit` | Check | Local durable evidence path and bounded forwarding queue. |
| `backup` | Check | Last verified backup, independent-copy state, RPO exposure, and restore-test status. |
| `recovery` | Check | Reduced recovery environment, credentials, media, instructions, and tested path. |
| `network` | Check | Zone separation, default-deny policy, local routes, and optional remote reachability. |
| `rights` | Check | Consent, withdrawal, audience, no-AI, attribution, and cultural-authority state. |

Each check produces an explicit pass, fail, blocked, degraded, stale, or not-applicable result.

### 4.6 Startup dependency order

The logical startup order is:

```text
host and encrypted storage
-> node identity and local trust
-> governance policy
-> audit and evidence
-> resource control
-> privileged operation broker
-> authoritative stores
-> component services
-> active artifact verification
-> local user and application surfaces
-> optional synchronization, federation, support, and external integrations
```

A concrete service manager can parallelize steps when dependencies and failure behavior remain correct.

### 4.7 Network model

A node uses a default-deny network posture.

Applicable zones include:

- local user or client;
- private service;
- public service when present;
- administrative;
- recovery;
- artifact and update;
- federation or synchronization;
- external-integration egress.

Public and private interfaces remain separate when both exist.

Remote administration does not listen on a public interface by default.

### 4.8 Host and process model

Components use:

- dedicated service or workload identity;
- least filesystem access;
- least secret delivery;
- declared network destinations;
- declared stores;
- bounded resources;
- read-only or verified artifacts when practical;
- no unrestricted host privilege;
- no direct cross-component database credentials.

Profile-specific isolation can use system services, rootless containers, constrained containers, virtual machines, or another declared mechanism.

The endpoint profile does not depend on Kubernetes unless explicitly declared.

### 4.9 Resource model

Resource policy distinguishes protected services from optional or heavy work.

Protected services include:

- identity;
- governance;
- audit;
- node privilege control;
- resource control;
- artifact verification;
- active workflow commit paths;
- backup finalization;
- rollback;
- recovery.

Optional heavy work can include:

- media conversion;
- thumbnails and previews;
- large index updates;
- synchronization;
- backup replication;
- SenTient tasks;
- external AI or media adapters;
- development tools.

The primary profile owns concrete CPU, memory, I/O, storage, queue, and concurrency values.

### 4.10 Release and artifact operations

The active node records exact selections for:

- system;
- services;
- governance;
- knowledge.

A candidate passes:

```text
obtain
-> quarantine
-> bounded parse
-> verify identity and inventory
-> verify publisher, signer, trust, and revocation
-> verify profile and component compatibility
-> verify resources and migration
-> obtain activation authority
-> stage
-> activate atomically
-> run health vectors
-> retain last-known-good predecessor
-> record evidence
```

Each release channel can change independently.

### 4.11 Configuration and drift

Configuration is classified as:

- profile and overlay selection;
- component membership;
- service and workload configuration;
- network and egress policy;
- storage and backup policy;
- resource limits;
- artifact selections;
- integration enablement;
- support enablement;
- local presentation.

Drift can be:

- expected runtime state;
- declared local override;
- pending approved change;
- unauthorized change;
- security-significant divergence;
- corruption.

Unknown security-significant drift moves the affected capability to quarantine or maintenance.

### 4.12 Observability and evidence

Operational views distinguish:

- node state;
- capability readiness;
- component health;
- trust and revocation freshness;
- active releases and artifacts;
- resource pressure;
- queue state;
- backup age and restore-test status;
- synchronization age;
- incidents;
- exceptions;
- remote-support sessions;
- rights and withdrawal alerts.

Public status and protected evidence are separate.

### 4.13 Operational review cadence

| Cadence | Required operational review |
| --- | --- |
| continuous | Required operational review | Protected service health, queue bounds, storage pressure, component isolation, audit durability, active artifact health, and security events. |
| at startup | Required operational review | Boot integrity, node identity, authority release, trust and revocation, Release Set, migrations, required components, backup and recovery status. |
| daily | Required operational review | Failed jobs, synchronization age, backup age, capacity trend, certificate and approval expiry, drift, security findings, and user-visible degradation. |
| weekly | Required operational review | Restore-readiness sampling, update candidates, log and evidence retention, offline-media inventory, removable credentials, external integration status, and stale exceptions. |
| monthly | Required operational review | Isolated restore exercise or profile-defined sample, recovery credentials, incident contacts, port and network exposure, dependency and artifact support status. |
| after material change | Required operational review | Threat review, profile validation, release evidence, backup, recovery, rollback, support-bundle, and exit-impact checks. |
| before retirement | Required operational review | Complete export, trust transfer or revocation, clean restore, credential removal, media inventory, sanitization, and evidence closure. |

A deployment can increase frequency according to risk and profile.

### 4.14 Backup and recovery

The node follows the global backup contract.

A recoverable node maintains:

- protected backup targets;
- at least one independent copy;
- an immutable or offline copy when required;
- tested recovery credentials;
- reduced recovery services;
- restore instructions;
- compatible installation or recovery artifacts;
- trust and revocation context;
- migration and forward-repair material;
- verified workflow-resume tests.

Protected key recovery remains separate from data backup.

### 4.15 Removable media

Removable media can carry:

- system, services, governance, or knowledge releases;
- backup sets;
- Sovereignty Bundles;
- trust and revocation updates;
- approved local media imports;
- diagnostics and evidence exports.

Media never executes or activates automatically.

### 4.16 Remote support

Remote support is an exceptional bounded capability.

A session identifies:

- requester;
- approver;
- support operator;
- node;
- tenant and environment;
- source and destination;
- permitted tools;
- permitted data;
- start and expiry;
- recording or receipt policy;
- cancellation;
- post-session review.

The session ends without leaving an unattended credential, tunnel, agent, or account.

### 4.17 Standard desktop and appliance shell

A standard sovereign Linux node can use GNOME or KDE.

The presentation layer can expose:

- system status;
- local applications;
- backup and recovery status;
- update candidates;
- removable-media workflows;
- privacy and external-integration controls;
- support authorization;
- Ariane navigation.

The `appliance_shell` overlay can replace the general desktop with a minimal Wayland surface.

It does not change component, data, authority, release, or recovery contracts.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-OPS-SOVNODE-001,REQ-OPS-SOVNODE-002,REQ-OPS-SOVNODE-003,REQ-OPS-SOVNODE-004,REQ-OPS-SOVNODE-005,REQ-OPS-SOVNODE-006,REQ-OPS-SOVNODE-007,REQ-OPS-SOVNODE-008,REQ-OPS-SOVNODE-009,REQ-OPS-SOVNODE-010,REQ-OPS-SOVNODE-011,REQ-OPS-SOVNODE-012,REQ-OPS-SOVNODE-013,REQ-OPS-SOVNODE-014,REQ-OPS-SOVNODE-015,REQ-OPS-SOVNODE-016,REQ-OPS-SOVNODE-017,REQ-OPS-SOVNODE-018,REQ-OPS-SOVNODE-019,REQ-OPS-SOVNODE-020,REQ-OPS-SOVNODE-021,REQ-OPS-SOVNODE-022,REQ-OPS-SOVNODE-023,REQ-OPS-SOVNODE-024,REQ-OPS-SOVNODE-025,REQ-OPS-SOVNODE-026,REQ-OPS-SOVNODE-027,REQ-OPS-SOVNODE-028,REQ-OPS-SOVNODE-029,REQ-OPS-SOVNODE-030,REQ-OPS-SOVNODE-031,REQ-OPS-SOVNODE-032,REQ-OPS-SOVNODE-033,REQ-OPS-SOVNODE-034,REQ-OPS-SOVNODE-035,REQ-OPS-SOVNODE-036,REQ-OPS-SOVNODE-037,REQ-OPS-SOVNODE-038,REQ-OPS-SOVNODE-039,REQ-OPS-SOVNODE-040,REQ-OPS-SOVNODE-041,REQ-OPS-SOVNODE-042 -->
- **REQ-OPS-SOVNODE-001 — SHALL:** A sovereign Linux node operates from one active `sovereign_linux_node` primary profile and any explicitly compatible overlays.
- **REQ-OPS-SOVNODE-002 — SHALL:** The active profile, overlays, Release Set, authority release, component inventory, trust state, revocation state, configuration-drift state, and node-health state remain locally inspectable.
- **REQ-OPS-SOVNODE-003 — SHALL:** Minimum local identity, governance, audit, resource control, artifact verification, recovery control, and declared application capabilities remain usable without Internet or a remote control plane.
- **REQ-OPS-SOVNODE-004 — SHALL NOT:** Loss of Internet, federation, remote support, external AI, or a central control plane expands local authority or silently changes policy.
- **REQ-OPS-SOVNODE-005 — SHALL:** Startup verifies boot, storage, node identity, local trust, active authority release, active Release Set, required components, resource envelope, and recovery availability before reporting local readiness.
- **REQ-OPS-SOVNODE-006 — SHALL:** Health, readiness, connectivity, synchronization, release currency, trust freshness, backup readiness, and recovery readiness remain separate operational states.
- **REQ-OPS-SOVNODE-007 — SHALL:** A node reports ready only for capabilities whose dependencies, stores, authority, artifacts, resources, and evidence path are currently valid.
- **REQ-OPS-SOVNODE-008 — SHALL:** Public, private-service, administrative, recovery, artifact-update, and external-integration network zones remain separated when applicable.
- **REQ-OPS-SOVNODE-009 — SHALL:** Administrative and recovery interfaces are disabled from public networks and require explicit scoped access, strong authentication, bounded sessions, and evidence.
- **REQ-OPS-SOVNODE-010 — SHALL:** Every component runs under its declared service or workload identity and accesses only its registered stores, interfaces, secrets, network destinations, and host operations.
- **REQ-OPS-SOVNODE-011 — SHALL NOT:** Routine node operations use shared database superuser credentials, arbitrary root shells, persistent unattended remote access, or direct cross-component store mutation.
- **REQ-OPS-SOVNODE-012 — SHALL:** Privileged node changes use kOA Node Agent with an allowlisted schema, operation-bound policy decision, replay protection, timeout, before-and-after verification, and receipt.
- **REQ-OPS-SOVNODE-013 — SHALL:** Resource Governor protects identity, governance, audit, artifact verification, active workflow commits, cancellation, backup finalization, rollback, and recovery during resource pressure.
- **REQ-OPS-SOVNODE-014 — SHALL:** Optional heavy work, media conversion, indexing, synchronization, backup replication, SenTient tasks, and external integrations stop or throttle before protected services.
- **REQ-OPS-SOVNODE-015 — SHALL:** The node enforces bounded queues, retries, concurrency, timeouts, temporary storage, log growth, database growth, artifact storage, and background work.
- **REQ-OPS-SOVNODE-016 — SHALL:** System, services, governance, and knowledge release channels are inventoried, verified, staged, activated, rolled back, revoked, and evidenced independently.
- **REQ-OPS-SOVNODE-017 — SHALL NOT:** Publication, download, mirroring, copying, or staging of an artifact implies installation or activation.
- **REQ-OPS-SOVNODE-018 — SHALL:** Artifact activation verifies identity, inventory, publisher and signer scope, trust, revocation, downgrade resistance, profile compatibility, resource capacity, migration state, policy authority, and rollback or forward-repair readiness.
- **REQ-OPS-SOVNODE-019 — SHALL:** Activation is atomic for the artifact class and preserves a compatible non-revoked last-known-good predecessor until post-activation health checks pass.
- **REQ-OPS-SOVNODE-020 — SHALL:** Maintenance mode preserves local identity, governance, audit, cancellation, backup, artifact verification, rollback, recovery, and operator status while restricting affected application capabilities.
- **REQ-OPS-SOVNODE-021 — SHALL:** Configuration changes are versioned, profile scoped, reviewed, validated, and associated with an operation identity and evidence.
- **REQ-OPS-SOVNODE-022 — SHALL:** Configuration drift is detected against the active profile and declared node state, classified by impact, and either reconciled, accepted through an explicit change, or isolated.
- **REQ-OPS-SOVNODE-023 — SHALL:** Logs, metrics, traces, health details, support bundles, and receipts minimize personal, sensitive, restricted, secret, and cross-tenant data.
- **REQ-OPS-SOVNODE-024 — SHALL:** Protected evidence access is authenticated, authorized, minimized, and audited.
- **REQ-OPS-SOVNODE-025 — SHALL:** Critical identity, governance, privilege, release, activation, publication, withdrawal, backup, restore, incident, exception, and recovery transitions produce durable local evidence.
- **REQ-OPS-SOVNODE-026 — SHALL:** Backup operation follows component-owned checkpoints, protected independent copies, declared RPO and RTO, restore testing, rights preservation, and the active backup contract.
- **REQ-OPS-SOVNODE-027 — SHALL:** The node maintains a separate reduced recovery environment with independently controlled recovery credentials and procedures.
- **REQ-OPS-SOVNODE-028 — SHALL:** Restore and recovery revalidate trust, authority, revocation, rights, audience, artifacts, compatibility, migration, and active-state eligibility before normal operation resumes.
- **REQ-OPS-SOVNODE-029 — SHALL:** Removable-media import uses quarantine, safe paths, bounded parsing, complete inventory checks, trust and revocation evaluation, classification, policy authorization, and no automatic execution or activation.
- **REQ-OPS-SOVNODE-030 — SHALL:** Removable-media export records source, destination, classification, rights, inventory, encryption, operator, authority, result, and receipt.
- **REQ-OPS-SOVNODE-031 — SHALL:** External integrations and external AI remain disabled until explicitly enabled by profile-compatible policy and remain removable without loss of core local operation or authoritative data.
- **REQ-OPS-SOVNODE-032 — SHALL:** No-AI, consent, cultural-rights, audience, attribution, export, withdrawal, and retention controls remain enforceable during local operation, synchronization, backup, restore, support, and external transfer.
- **REQ-OPS-SOVNODE-033 — SHALL:** Remote support is disabled by default and, when authorized, is time bounded, source and destination scoped, strongly authenticated, recorded, revocable, and unable to persist unattended access.
- **REQ-OPS-SOVNODE-034 — SHALL:** Incident response preserves authority boundaries, isolates affected capabilities, protects evidence, expires emergency authority, and retains unrelated valid local service.
- **REQ-OPS-SOVNODE-035 — SHALL:** Clock uncertainty, stale trust, stale revocation, synchronization delay, offline duration, capacity pressure, and degraded capabilities remain visible to operators and affected users.
- **REQ-OPS-SOVNODE-036 — SHALL:** A high-assurance overlay adds its required hardware trust, measured or verified boot, attestation, protected key custody, separation of duties, independent evidence, immutable or offline backup, and recovery controls without weakening the primary profile.
- **REQ-OPS-SOVNODE-037 — SHALL:** An appliance-shell overlay changes the local presentation and service surface without changing authority, component ownership, release, backup, recovery, or evidence rules.
- **REQ-OPS-SOVNODE-038 — SHALL NOT:** Kubernetes or another orchestrator is treated as an endpoint requirement unless the active profile explicitly declares and validates it.
- **REQ-OPS-SOVNODE-039 — SHALL:** Node retirement produces a complete verified Sovereignty Bundle or other applicable exit artifact, transfers or revokes trust, preserves governed rights and evidence, removes credentials, and proves clean independent restoration when claimed.
- **REQ-OPS-SOVNODE-040 — SHALL:** Operational exceptions are explicit, scoped, time bounded, approved, compensating, evidenced, and unable to silently redefine readiness, compliance, backup, trust, or recovery claims.
- **REQ-OPS-SOVNODE-041 — SHALL:** Every active sovereign-node operational claim maps to the primary profile, overlays, components, artifacts, Release Set, authority release, threat, test, evidence, exception, and current node state.
- **REQ-OPS-SOVNODE-042 — SHALL:** Ordinary Markdown sovereign-node documentation uses registry, reference, structure, language, decision, requirement, lock, and traceability validation without an automatic file-content-hash requirement.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Start the node

1. Power on through the profile-declared boot chain.
2. verify boot and host integrity.
3. unlock protected storage through the declared identity and recovery model.
4. verify node identity and local trust.
5. load and verify the active authority release and governance bundle.
6. start local durable evidence.
7. start resource and privilege controls.
8. verify authoritative stores and migrations.
9. start required components in dependency order.
10. verify active artifacts and Release Set selections.
11. run local readiness checks.
12. expose only ready capabilities.
13. start optional remote functions after local readiness and policy evaluation.

### 6.2 Review daily status

1. Confirm the node state and capability readiness.
2. inspect trust, revocation, clock, and synchronization freshness.
3. inspect failed or blocked component jobs.
4. inspect resource and storage pressure.
5. inspect backup age and independent-copy status.
6. inspect drift and unauthorized changes.
7. inspect certificate, credential, approval, and exception expiry.
8. inspect security and rights alerts.
9. resolve or assign each material issue.
10. retain the review evidence required by policy.

### 6.3 Enter maintenance mode

1. Identify the maintenance purpose, scope, owner, expected effects, and rollback.
2. create the maintenance operation identity.
3. obtain required authorization.
4. verify a current restore-eligible backup or declared alternative.
5. stop new affected work.
6. drain or checkpoint active work.
7. preserve cancellation, audit, backup, artifact verification, and recovery.
8. perform the bounded change.
9. run health and conformance checks.
10. return affected capabilities to ready state or roll back.
11. close the maintenance record.

### 6.4 Activate a release or artifact

1. Select the exact candidate identity.
2. verify the permitted channel and target profile.
3. verify manifest, inventory, supply-chain evidence, trust, revocation, and compatibility.
4. verify resource capacity and migration plan.
5. verify backup and rollback or forward-repair readiness.
6. obtain operation-specific governance authority.
7. stage the candidate.
8. activate through the owning component and kOA Node Agent when privilege is needed.
9. run declared health vectors.
10. retain or restore the predecessor according to result.
11. record activation evidence.

### 6.5 Operate offline

1. Display offline state, trust freshness, revocation epoch, clock confidence, and unavailable remote capabilities.
2. keep local identity, governance, audit, recovery, active artifacts, and declared application functions available.
3. queue permitted synchronization or evidence forwarding within bounds.
4. reject actions requiring unavailable current remote authority.
5. create local backups according to the offline target policy.
6. continue local rights and no-AI enforcement.
7. revalidate queued work before later transmission.

### 6.6 Import removable media

1. Identify the operator, media, purpose, and target capability.
2. mount or expose media through the declared restricted mechanism.
3. copy the candidate into quarantine.
4. enforce path, archive, size, recursion, decompression, object-count, and storage limits.
5. verify inventory, artifact identities, signatures, trust, revocation, classification, and compatibility.
6. obtain import or activation authority.
7. stage accepted content.
8. use the normal owner admission or artifact activation procedure.
9. record receipts.
10. remove media and clear temporary material.

### 6.7 Authorize remote support

1. Confirm that local operation cannot resolve the issue through ordinary procedures.
2. identify the support operator and organization.
3. define exact source, destination, tools, data, scope, and expiry.
4. obtain strong authentication and required approval.
5. create an ephemeral session identity and credential.
6. expose only the permitted support path.
7. display the active session locally.
8. collect minimized session evidence.
9. terminate and revoke access.
10. verify that no persistent access remains.
11. review the session.

### 6.8 Respond to resource pressure

1. Identify the constrained resource and affected capabilities.
2. protect active integrity-critical writes.
3. stop or throttle optional heavy work.
4. reject or queue new optional work explicitly.
5. preserve operator status and cancellation.
6. free regenerable caches or temporary state according to policy.
7. expand capacity or repair the cause when authorized.
8. verify recovery and record the event.

### 6.9 Respond to an incident

1. Identify the affected node, components, identities, stores, artifacts, networks, and time range.
2. preserve classified local evidence.
3. isolate affected zones, services, credentials, or artifacts.
4. retain unrelated valid local service when safe.
5. invoke bounded emergency authority only when required.
6. rotate or revoke affected trust.
7. rollback, restore, or forward repair through canonical procedures.
8. verify rights, revocation, active artifacts, and workflow state.
9. expire emergency access.
10. complete post-incident review and evidence.

### 6.10 Enter recovery

1. Stop or isolate normal service authority.
2. boot or activate the reduced recovery environment.
3. authenticate recovery operators with the stronger declared process.
4. verify recovery media, trust, backups, and restore artifacts.
5. diagnose host, storage, identity, governance, artifact, or component state.
6. select repair, rollback, restore, reinstall, trust replacement, or retirement.
7. obtain required independent approval.
8. execute the bounded recovery procedure.
9. verify the repaired node from the boot chain upward.
10. return to `starting`, `quarantined`, or `retiring`.
11. record recovery evidence.

### 6.11 Retire the node

1. Identify tenant, organization, data, trust, artifacts, credentials, media, and dependencies.
2. create and verify the required backup and Sovereignty Bundle.
3. perform an independent clean restore when the exit claim requires it.
4. transfer or revoke trust and credentials.
5. close synchronization, federation, support, and integration relationships.
6. preserve governed rights, withdrawal, provenance, and evidence.
7. remove protected data and secrets through the declared sanitization process.
8. inventory and sanitize removable media.
9. remove node identity from active inventories.
10. verify that the original node is no longer required.
11. mark it retired and preserve retirement evidence.

## 7. Failure and Degradation

| Failure ID | Failure | Safe behavior | Recovery |
| --- | --- | --- | --- |
| `SOVNODE-FAIL-001` | Failure | Safe behavior | Recovery |
| `SOVNODE-FAIL-002` | Failure | Safe behavior | Recovery |
| `SOVNODE-FAIL-003` | Failure | Safe behavior | Recovery |
| `SOVNODE-FAIL-004` | Failure | Safe behavior | Recovery |
| `SOVNODE-FAIL-005` | Failure | Safe behavior | Recovery |
| `SOVNODE-FAIL-006` | Failure | Safe behavior | Recovery |
| `SOVNODE-FAIL-007` | Failure | Safe behavior | Recovery |
| `SOVNODE-FAIL-008` | Failure | Safe behavior | Recovery |
| `SOVNODE-FAIL-009` | Failure | Safe behavior | Recovery |
| `SOVNODE-FAIL-010` | Failure | Safe behavior | Recovery |
| `SOVNODE-FAIL-011` | Failure | Safe behavior | Recovery |
| `SOVNODE-FAIL-012` | Failure | Safe behavior | Recovery |

### 7.1 Capability-scoped degradation

A degraded node identifies:

- affected capability;
- unaffected capabilities;
- cause;
- authority impact;
- data impact;
- user impact;
- workaround;
- next action;
- evidence.

A capability failure does not become a fabricated whole-node success or failure claim.

### 7.2 Local readiness without connectivity

A network-disconnected node can remain `ready_local`.

It is not described as connected, synchronized, current with remote revocation, or remotely backed up unless those independent checks pass.

### 7.3 Quarantine

Quarantine preserves:

- protected data encryption;
- evidence;
- recovery access;
- known-good backups;
- trusted artifacts;
- operator status.

Normal governed mutations and uncertain remote communication remain blocked.

### 7.4 Recovery dependency failure

Missing recovery credentials, invalid media, stale trust, or failed restore tests removes the affected recovery-readiness claim.

The node exposes the condition before an incident requires recovery.

### 7.5 High-assurance degradation

A failed high-assurance control can leave the primary sovereign-node capability valid only when policy explicitly permits operation without the overlay claim.

The interface removes the high-assurance claim and displays the missing control.

## 8. Cross-Component Interactions

| Counterparty | Operational interaction | Boundary |
| --- | --- | --- |
| Identity and Trust | Node, workload, operator, support, artifact, target, key, certificate, trust, and revocation identity. | Identity does not grant policy, privilege, activation, backup, or recovery authority. |
| Governance Policy Runtime | Operational, maintenance, support, import, activation, backup, recovery, exception, and retirement decisions. | Policy does not perform host operations or own component data. |
| Audit Broker | Local classified evidence and bounded forwarding. | Audit does not authorize operations or expose unrestricted payloads. |
| Resource Governor | Resource protection, quotas, queues, concurrency, cancellation, and pressure behavior. | It does not change component authority or release state. |
| kOA Node Agent | Narrow allowlisted privileged host operations. | It does not expose arbitrary shell access or select its own targets. |
| Application components | Component-owned readiness, stores, checkpoints, artifacts, failure, backup, and restore. | The operator and coordinator use declared interfaces rather than direct databases. |
| Release repositories and mirrors | Candidate artifact acquisition and revocation updates. | Availability does not equal trust, compatibility, or activation. |
| Backup targets | Encrypted protected continuity copies. | Possession does not grant decryption, restore, or activation authority. |
| Federation peers | Bounded synchronization and content exchange. | Peer identity and authority remain locally evaluated. |
| External integrations and AI | Optional assistive or connected capability. | They are disabled until enabled and cannot become core authority or recovery dependencies. |
| Remote support provider | Time-bounded diagnostic or repair session. | No persistent unattended access or protected-key custody. |
| Recovery environment | Reduced independently controlled repair and restore services. | Normal application authority remains suspended until revalidation. |
| Sovereignty Bundle and exit operator | Independent export and clean restoration. | Retirement does not depend on the original operator when the exit claim applies. |

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Closed decisions

| Decision | Closed operational rule |
| --- | --- |
| `DEC-SYS-001` | A sovereign node preserves declared minimum local operation and does not require continuous remote control. |
| `DEC-AUTH-001` | Operational, maintenance, support, activation, privilege, recovery, and retirement authority remains explicit and bounded. |
| `DEC-IDENT-001` | Node, workload, operator, support, artifact, tenant, environment, target, key, release, and authority identities remain distinct. |
| `DEC-DATA-001` | Components retain authoritative-store ownership during normal operation, backup, recovery, and retirement. |
| `DEC-COMP-001` | Cross-component operations use explicit interfaces and prohibit direct authoritative-store writes. |
| `DEC-GOV-001` | Governance decides operational authority; Resource Governor controls resources separately. |
| `DEC-PRIV-001` | Evidence, support, backup, transfer, and status use classification, minimization, rights, audience, and withdrawal controls. |
| `DEC-AI-001` | External AI and integrations remain optional, explicit, removable, and non-authoritative. |
| `DEC-LIFE-001` | System, services, governance, and knowledge channels activate independently with verification, rollback, revocation, and evidence. |
| `DEC-HW-001` | High-assurance hardware and attestation controls apply through the overlay rather than every sovereign node. |

### 9.2 Prohibited assumptions

Authors, implementers, validators, operators, and AI agents do not assume that:

- connected means ready;
- healthy means authorized;
- a running process is a ready component;
- a copied artifact is active;
- latest means compatible;
- a valid signature grants activation;
- a central control plane is required for local operation;
- Internet loss permits weaker policy;
- one service account can operate every component;
- root access is a normal operations interface;
- a shared database superuser is acceptable;
- a high-assurance overlay is active because hardware supports it;
- a standard desktop weakens sovereignty automatically;
- an appliance shell changes data ownership or authority;
- Kubernetes is required on an endpoint;
- a backup file proves restore readiness;
- a clean restore can depend on undocumented operator knowledge;
- removable media is trusted because it is physically controlled;
- an offline node knows current global revocation state;
- remote support can leave a permanent agent or tunnel;
- external AI can decide operations or recovery;
- a configuration change outside the profile is harmless;
- a failed optional service invalidates every local capability;
- retirement can erase the last recoverable source before exit verification;
- ordinary Markdown requires per-file content hashes.

A new implementation-affecting sovereign-node choice remains inactive until its profile, owner, authority, failure behavior, tests, recovery, and evidence are closed.

## 10. Validation Criteria

| Validation group | Required tests |
| --- | --- |
| Local readiness and offline operation | `TEST-SYS-001`, `TEST-SYS-004`, `TEST-SYS-005`, `TEST-SYS-006`, `TEST-SYS-009`, `TEST-SYS-010`, `TEST-SYS-011`, `TEST-SYS-012`, `TEST-SYS-015`, `TEST-PROF-005`, `TEST-PROF-006`, `TEST-PROF-008`, `TEST-PROF-013`, `TEST-PROF-014` |
| Profile composition and high assurance | `TEST-PROF-001`, `TEST-PROF-002`, `TEST-PROF-003`, `TEST-PROF-004`, `TEST-PROF-007`, `TEST-PROF-009`, `TEST-PROF-015`, `TEST-SEC-006`, `TEST-SEC-007`, `TEST-SEC-008`, `TEST-SEC-015` |
| Identity, privilege, networks, and stores | `TEST-SEC-001`, `TEST-SEC-002`, `TEST-SEC-003`, `TEST-SEC-004`, `TEST-SEC-005`, `TEST-SEC-009`, `TEST-SEC-010`, `TEST-CROSS-004`, `TEST-CROSS-007`, `TEST-CROSS-008`, `TEST-CROSS-009`, `TEST-CROSS-014`, `TEST-CROSS-015`, `TEST-SYS-013`, `TEST-SYS-014` |
| Artifact and release operations | `TEST-LIFE-001`, `TEST-LIFE-002`, `TEST-LIFE-003`, `TEST-LIFE-004`, `TEST-LIFE-005`, `TEST-LIFE-006`, `TEST-LIFE-007`, `TEST-LIFE-008`, `TEST-LIFE-009`, `TEST-LIFE-010`, `TEST-LIFE-011`, `TEST-LIFE-012`, `TEST-LIFE-013`, `TEST-LIFE-014`, `TEST-LIFE-015` |
| Observability, capacity, maintenance, and support | `TEST-OPS-001`, `TEST-OPS-002`, `TEST-OPS-003`, `TEST-OPS-006`, `TEST-OPS-008`, `TEST-OPS-009`, `TEST-OPS-010`, `TEST-SEC-011` |
| Backup, restore, incident, and recovery | `TEST-OPS-004`, `TEST-OPS-005`, `TEST-OPS-007`, `TEST-SEC-013`, `TEST-SEC-014`, `TEST-EXIT-007` |
| AI and integration removability | `TEST-SYS-002`, `TEST-SYS-003`, `TEST-SEC-012`, `TEST-CROSS-006`, `TEST-CROSS-011`, `TEST-CROSS-012`, `TEST-CROSS-013`, `TEST-EXIT-008` |
| Portability and retirement | `TEST-EXIT-001`, `TEST-EXIT-002`, `TEST-EXIT-003`, `TEST-EXIT-004`, `TEST-EXIT-005`, `TEST-EXIT-006` |
| Documentation and traceability | `TEST-DOC-VAL-003`, `TEST-DOC-VAL-005`, `TEST-DOC-VAL-006`, `TEST-DOC-VAL-007`, `TEST-DOC-VAL-008`, `TEST-DOC-VAL-009`, `TEST-DOC-VAL-010`, `TEST-DOC-VAL-012`, `TEST-DOC-VAL-016`, `TEST-DOC-VAL-017`, `TEST-DOC-VAL-018`, `TEST-DOC-VAL-019`, `TEST-DOC-VAL-020` |

Sovereign-node validation additionally confirms:

1. exactly one primary `sovereign_linux_node` profile resolves;
2. overlays are compatible and merge without unresolved conflict;
3. required component membership and exclusions resolve;
4. local readiness passes without Internet or control-plane connectivity;
5. health, readiness, connectivity, synchronization, trust freshness, backup, and recovery remain distinct;
6. node and workload identities are scoped and current;
7. public, private, administrative, recovery, update, and external-integration boundaries resolve;
8. direct cross-component database access and arbitrary privileged command surfaces are absent;
9. protected services retain capacity under pressure;
10. optional heavy work stops or throttles first;
11. all active channel and artifact identities, trust, revocation, compatibility, and rollback state verify;
12. activation and maintenance do not create partial active state;
13. configuration drift is visible and resolved;
14. logs, evidence, and support bundles are minimized and classified;
15. backup and clean restore tests pass according to profile;
16. removable-media imports use bounded quarantine and no automatic activation;
17. remote support leaves no persistent unattended access;
18. offline trust, revocation, clock, and synchronization uncertainty is visible;
19. high-assurance claims match the overlay controls and evidence;
20. external integrations can be removed without loss of core data or operation;
21. retirement produces the declared exit and independent-restore evidence;
22. every requirement maps to an active test or approved manual control;
23. every active claim has current traceability and evidence;
24. exceptions are explicit, compensating, approved, and expiring;
25. no unresolved authority marker exists;
26. all active prose is in English.

A failed required check blocks or narrows the affected readiness, security, continuity, high-assurance, or exit claim.

## 11. Non-Normative Examples

### 11.1 Locally ready and offline

A sovereign node boots without Internet access.

Boot integrity, storage, node identity, local policy, audit, active Release Set, required components, backup status, and recovery readiness pass. The node reports `ready_local`.

Federation, remote mirrors, external AI, and remote support remain unavailable and visibly stale.

### 11.2 Connected after local readiness

The network becomes available.

The node does not change local authority automatically. It validates remote identities, destinations, synchronization policy, trust, and revocation before enabling bounded synchronization and mirror refresh.

Local readiness remains independently visible.

### 11.3 Services-channel update

An operator stages a verified services release.

System, governance, and knowledge selections remain unchanged. The node verifies compatibility, backup, migration, capacity, authority, and rollback. It activates the services release atomically and runs component health tests.

The prior services release remains available until success is proven.

### 11.4 Governance update failure

A new governance bundle has a valid signature but fails a policy test vector.

The bundle remains inactive. Existing governance remains active, and application services continue under the previous valid authority state.

A valid signature does not override the failed compatibility check.

### 11.5 Storage pressure

UCKK media processing and backup replication fill temporary storage.

Resource Governor stops new media jobs, pauses optional replication, and protects active workflow commits, identity, governance, audit, artifact verification, cancellation, and recovery.

Regenerable caches are removed before authoritative media or provenance.

### 11.6 Removable-media knowledge update

An operator inserts media containing a Kristal Runtime Pack and a language pack.

The node copies them to quarantine, applies bounded parsing, verifies inventory, trust, revocation, channels, audience, compatibility, and resources, and stages them separately.

Kristal and language artifacts activate independently through their own owners.

### 11.7 Time-bounded support

A local operator authorizes a support session for one component and one hour.

The support operator receives an ephemeral identity and a restricted diagnostic interface. The node displays the active session and records minimized evidence.

At expiry, the credential and path are removed, and the node verifies that no persistent agent remains.

### 11.8 High-assurance overlay

A sovereign node uses the high-assurance overlay.

Measured or verified boot, hardware-bound node identity, protected key custody, dual-control recovery, independent evidence anchoring, and immutable or offline backup all pass.

If attestation later fails, the node can retain a primary local capability only when policy permits it, while the high-assurance claim is removed.

### 11.9 Recovery

A failed system update prevents normal boot.

The operator enters the separate recovery environment with stronger authentication. The environment verifies the last-known-good system artifact, local trust, backups, and active data state.

The node rolls back the system channel, verifies application and governance compatibility, and returns through normal startup.

### 11.10 Retirement and exit

An organization retires a sovereign node.

It creates a verified Sovereignty Bundle, completes an independent clean restore, revokes the old node identity, transfers required trust through the declared process, removes integrations and support access, sanitizes storage and media, and closes the node inventory.

The original node is no longer technically required.
