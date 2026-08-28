<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-RECIPE-UL-001",
  "document_class": "recipe",
  "status": "active",
  "language": "en",
  "layer": "implementation_recipe",
  "scope": [
    "profile:user_lightweight"
  ],
  "canonical_refs": [
    "contracts/profiles/user-lightweight.profile.json",
    "generated/profile-catalog.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-PROFILE-001",
    "DEC-SYS-001",
    "DEC-AUTH-001",
    "DEC-IDENT-001",
    "DEC-DATA-001",
    "DEC-COMP-001",
    "DEC-GOV-001",
    "DEC-AI-001",
    "DEC-SENT-001",
    "DEC-MEDIATHEQUE-001",
    "DEC-UCKK-EXT-001",
    "DEC-ARI-001",
    "DEC-LANG-001",
    "DEC-LIFE-001"
  ],
  "requirement_ids": [
    "REQ-PROF-MODEL-005",
    "REQ-PROF-MODEL-009",
    "REQ-PROF-MODEL-012",
    "REQ-PROF-MODEL-014",
    "REQ-PROF-MODEL-016",
    "REQ-PROF-MODEL-018",
    "REQ-PROF-MODEL-019",
    "REQ-PROF-MODEL-022",
    "REQ-PROF-MODEL-023",
    "REQ-PROF-MODEL-024",
    "REQ-PROF-MODEL-026",
    "REQ-SEC-AI-001",
    "REQ-SEC-AI-002",
    "REQ-SEC-AI-007",
    "REQ-SEC-AI-018",
    "REQ-SEC-AI-023",
    "REQ-SEC-AI-024",
    "REQ-OPS-BACKUP-001",
    "REQ-OPS-BACKUP-002",
    "REQ-OPS-BACKUP-009",
    "REQ-OPS-BACKUP-011",
    "REQ-OPS-BACKUP-018",
    "REQ-OPS-BACKUP-026",
    "REQ-OPS-BACKUP-028",
    "REQ-OPS-BACKUP-030",
    "REQ-OPS-BACKUP-035",
    "REQ-OPS-BACKUP-036",
    "REQ-OPS-BACKUP-037",
    "REQ-OPS-BACKUP-039"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-DOC-003",
    "LOCK-DOC-016",
    "LOCK-DOC-021",
    "LOCK-DOC-022",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SENT-001",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-UCKK-EXT-001",
    "LOCK-MEDIATHEQUE-002",
    "LOCK-UCKK-EXT-002",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-001",
    "DOC-SEC-000",
    "DOC-SEC-011",
    "DOC-OPS-008",
    "DOC-CONF-009"
  ],
  "tags": [
    "recipe",
    "user-lightweight",
    "minimal-installation",
    "systemd",
    "rootless-containers",
    "cgroups-v2",
    "zram",
    "offline",
    "task-activation",
    "resource-bounds",
    "non-normative"
  ]
}
KOA:DOC-META:END -->

# Minimal Installation for `user_lightweight`

## Recipe Identity

| Field | Value |
| --- | --- |
| Recipe ID | `RECIPE-UL-001` |
| Title | Minimal Installation for `user_lightweight` |
| Status | `active` |
| Version | `1.0.0` |
| Owner | `owner:user-profile-operations` |
| Last reviewed | `2026-08-03` |
| Applies to profiles | `user_lightweight` |
| Applies to components | `identity_and_trust`, `governance_policy_runtime`, `audit_broker`, `koa_node_agent`, `resource_governor`, `orgo`, `kristal_runtime`, `konnaxion`, `semantik_architect_runtime`, `koa_mediatheque`, `ariane_runtime`, `publication_gateway`; optional integrations: `uckk-publication`, `uckk-import` |
| Applies to toolchains | `none` |
| Supported platforms | systemd-based Linux with cgroup v2 and a profile-supported rootless OCI runtime |
| Supersedes | `none` |
| Replaced by | `none` |

## 1. Purpose

This recipe installs a lightweight local kOA environment for the `user_lightweight` primary profile.

The implementation targets a modest current-generation or refurbished computer with:

- four or more general-purpose CPU threads;
- 16 GiB of memory;
- a solid-state system disk with at least 80 GiB free before installation;
- cgroup v2;
- compressed RAM swap such as zram;
- one maintained browser or profile-approved local product shell;
- one PostgreSQL process with component-separated identities and databases or schemas;
- rootless OCI application services managed by systemd where feasible.

Successful completion produces:

- one active `user_lightweight` profile;
- one exact active Release Set;
- local identity, governance, audit, resource, and recovery control;
- local Orgo, Kristal, Konnaxion, SemantiK, kOA Mediatheque, and Ariane capability;
- no mandatory external AI, central control plane, cluster orchestrator, heavy research workbench, or permanent virtual machine;
- an idle memory target of approximately 5–8 GiB;
- an encrypted protected backup and a tested restore path.

This recipe does not define the profile contract, component membership, security policy, artifact format, or conformance rules.

## 2. Non-Normative Status

This file explains one implementation method.

Canonical authority remains with the referenced decisions, registries, profile contracts, component contracts, requirements, locks, artifact contracts, tests, and evidence.

This recipe does not:

- create a global system requirement;
- make systemd, Podman, cgroup v2, zram, PostgreSQL, GNOME, KDE Plasma, or a browser universal;
- redefine the `user_lightweight` component set;
- weaken a global authority, identity, privacy, data, AI, release, backup, or recovery invariant;
- make an example value a canonical default;
- resolve a missing owner decision;
- establish conformance by itself.

A conflict with active canonical authority makes this recipe invalid for the affected installation.

## 3. Scope

### 3.1 Included

- host preflight and resource checks;
- resolution of the exact active profile, authority release, and Release Set;
- installation of the local control foundation;
- installation of lightweight application services;
- one shared PostgreSQL process with component-isolated identities;
- task activation and resource limits;
- one normally active SemantiK language pack;
- local browser or approved product-shell access;
- offline operation;
- initial protected backup;
- functional, profile, security, lifecycle, operations, and exit validation.

### 3.2 Excluded

- operating-system installation;
- disk partitioning or full-disk-encryption setup;
- high-assurance overlay controls;
- sovereign-offline overlay controls;
- appliance-shell overlay installation;
- developer workspaces;
- GF Wordbench and grammar compilation;
- SenTient;
- local generative AI;
- Solr, Elasticsearch, OpenRefine, or similar heavy services;
- public Internet exposure;
- multi-node high availability;
- Kubernetes;
- production release signing;
- complete organization or tenant exit beyond the initial restore-readiness checks.

### 3.3 Supported profiles

Supported:

- `user_lightweight`

Not claimed by this recipe:

- `developer_linux_workstation`
- `developer_windows_wsl`
- `sovereign_linux_node`
- `sovereign_hub`
- `build_farm`
- `control_plane`
- any overlay composition

A compatible overlay requires its own procedure and additional evidence.

### 3.4 Supported platforms and versions

| Platform or tool | Supported version or range | Canonical source |
| --- | --- | --- |
| Linux host | version selected by the active profile and system Release Set | `contracts/profiles/user-lightweight.profile.json` |
| systemd | version supplied by the active system release | active system-channel artifact |
| cgroup | unified cgroup v2 hierarchy | `contracts/profiles/user-lightweight.profile.json#/hardware_envelope/enforcement` |
| OCI runtime | rootless runtime accepted by the profile | `contracts/profiles/user-lightweight.profile.json#/capabilities/rootless_container_runtime` |
| PostgreSQL | version selected by the services Release Set | active services-channel artifacts |
| browser or product shell | version selected by the system or services Release Set | active system and services artifacts |

The recipe does not substitute newer versions by assumption.

## 4. Canonical References

### 4.1 Decisions

- `DEC-PROFILE-001`
- `DEC-SYS-001`
- `DEC-AUTH-001`
- `DEC-IDENT-001`
- `DEC-DATA-001`
- `DEC-COMP-001`
- `DEC-GOV-001`
- `DEC-AI-001`
- `DEC-SENT-001`
- `DEC-UCKK-EXT-001`
- `DEC-ARI-001`
- `DEC-LANG-001`
- `DEC-LIFE-001`

### 4.2 Requirements

- `REQ-PROF-MODEL-005`
- `REQ-PROF-MODEL-009`
- `REQ-PROF-MODEL-012`
- `REQ-PROF-MODEL-014`
- `REQ-PROF-MODEL-016`
- `REQ-PROF-MODEL-018`
- `REQ-PROF-MODEL-019`
- `REQ-PROF-MODEL-022`
- `REQ-PROF-MODEL-023`
- `REQ-PROF-MODEL-024`
- `REQ-PROF-MODEL-026`
- `REQ-SEC-AI-001`
- `REQ-SEC-AI-002`
- `REQ-SEC-AI-007`
- `REQ-SEC-AI-018`
- `REQ-SEC-AI-023`
- `REQ-SEC-AI-024`
- `REQ-OPS-BACKUP-001`
- `REQ-OPS-BACKUP-002`
- `REQ-OPS-BACKUP-009`
- `REQ-OPS-BACKUP-011`
- `REQ-OPS-BACKUP-018`
- `REQ-OPS-BACKUP-026`
- `REQ-OPS-BACKUP-028`
- `REQ-OPS-BACKUP-030`
- `REQ-OPS-BACKUP-035`
- `REQ-OPS-BACKUP-036`
- `REQ-OPS-BACKUP-037`
- `REQ-OPS-BACKUP-039`

### 4.3 Locks

- `LOCK-PROFILE-001`
- `LOCK-PROFILE-002`
- `LOCK-IMPL-001`
- `LOCK-IMPL-002`
- `LOCK-DOC-003`
- `LOCK-DOC-016`
- `LOCK-DOC-021`
- `LOCK-DOC-022`
- `LOCK-COMP-001`
- `LOCK-COMP-002`
- `LOCK-DATA-001`
- `LOCK-GOV-001`
- `LOCK-AI-001`
- `LOCK-AI-002`
- `LOCK-SENT-001`
- `LOCK-UCKK-EXT-001`
- `LOCK-UCKK-EXT-002`
- `LOCK-ARI-001`
- `LOCK-ARI-002`
- `LOCK-LIFE-001`
- `LOCK-LIFE-002`
- `LOCK-LIFE-003`
- `LOCK-LIFE-004`

### 4.4 Profiles

- `contracts/profiles/user-lightweight.profile.json`
- `generated/profile-catalog.json`

### 4.5 Component contracts

- `contracts/components/identity-and-trust.component.json`
- `contracts/components/governance-policy-runtime.component.json`
- `contracts/components/audit-broker.component.json`
- `contracts/components/koa-node-agent.component.json`
- `contracts/components/resource-governor.component.json`
- `contracts/components/orgo.component.json`
- `contracts/components/kristal-runtime.component.json`
- `contracts/components/konnaxion.component.json`
- `contracts/components/semantik-architect-runtime.component.json`
- `contracts/components/koa-mediatheque.component.json`
- `contracts/integrations/uckk-publication.integration.json`
- `contracts/integrations/uckk-import.integration.json`
- `contracts/artifact-contracts/uckk-learning-package.schema.json`
- `contracts/artifact-contracts/uckk-import-receipt.schema.json`
- `contracts/components/ariane-runtime.component.json`
- `contracts/components/publication-gateway.component.json`

### 4.6 Artifact and lifecycle contracts

- `contracts/release-channels.contract.json`
- `contracts/artifact-classes.contract.json`
- active system, services, governance, and knowledge Release Set manifests
- component artifact contracts referenced by the active Release Set

### 4.7 Related documentation

- `DOC-SYS-001`
- `DOC-SEC-000`
- `DOC-SEC-011`
- `DOC-OPS-008`
- `DOC-CONF-009`

## 5. Preconditions

### 5.1 Authority preconditions

Before state changes begin:

- the active authority release resolves;
- `user_lightweight` is active;
- no overlay is selected by this recipe;
- the exact Release Set resolves;
- every required component artifact is verified or available for verified import;
- every applicable lock passes;
- no applicable exception is expired;
- the previous locally valid state and rollback path are identified.

### 5.2 Environment preconditions

The reference target has:

- Linux;
- systemd;
- cgroup v2;
- a profile-supported rootless OCI runtime;
- a profile-supported PostgreSQL package or verified service artifact;
- `jq`;
- at least four CPU threads;
- at least 16 GiB of memory;
- at least 80 GiB free storage;
- working local clock and filesystem permissions;
- a local administrative account capable of invoking the approved privileged path;
- zram or another profile-approved compressed swap implementation;
- no active Kubernetes requirement;
- no undeclared public listener.

### 5.3 Data preconditions

- existing kOA data has a current protected backup;
- a new installation target has no unmanaged conflicting kOA state;
- retained previous artifacts are identifiable when this is an upgrade;
- database and schema versions match the candidate migration plan;
- encryption and credential references resolve without exposing key material;
- quarantine has capacity for imported artifacts.

### 5.4 Safe preflight commands

```bash
set -eu

test "$(uname -s)" = "Linux"
systemctl --version >/dev/null
test -r /sys/fs/cgroup/cgroup.controllers
podman version >/dev/null
jq --version >/dev/null
psql --version >/dev/null

test "$(getconf _NPROCESSORS_ONLN)" -ge 4
test "$(awk '/MemTotal/ {print int($2/1024/1024)}' /proc/meminfo)" -ge 15
test "$(df --output=avail -BG /var/lib | tail -1 | tr -dc '0-9')" -ge 80

swapon --show --noheadings | grep -Eq 'zram|swap'
```

These commands are read only.

A failed command blocks the recipe until the condition is corrected or a different valid profile is selected.

## 6. Inputs and Outputs

### 6.1 Inputs

| Input | Type | Source | Required | Sensitive |
| --- | --- | --- | ---: | ---: |
| active authority release | signed registry set | `generated/authority-manifest.json` | yes | no |
| `user_lightweight` profile contract | JSON contract | `contracts/profiles/user-lightweight.profile.json` | yes | no |
| exact Release Set | signed manifest | active release authority | yes | no |
| component artifacts | signed system or services artifacts | verified repository, mirror, or offline bundle | yes | no |
| governance bundle | signed governance artifact | governance release channel | yes | restricted |
| knowledge artifacts | signed language, Kristal, and Ariane artifacts | knowledge release channel | yes | classification dependent |
| node and workload enrollment | protected identity material | Identity and Trust | yes | yes |
| component credentials | protected references | profile-approved credential source | yes | yes |
| prior backup or clean-install declaration | evidence | operations owner | yes | classification dependent |

### 6.2 Outputs

| Output | Type | Destination | Canonical contract |
| --- | --- | --- | --- |
| effective profile | generated JSON | `/var/lib/koa/node/effective-profile.json` | profile composition contract |
| active Release Set record | activation state | `/var/lib/koa/releases/` | release lifecycle contract |
| installed component artifacts | immutable artifacts | profile-declared artifact stores | component and artifact contracts |
| component operational state | authoritative state | component-owned locations | component contracts |
| local evidence | classified receipts | `/var/lib/koa/audit/` | Audit Broker contract |
| initial backup | encrypted backup set | protected target | backup artifact contract |
| installation execution summary | JSON evidence | evidence registry or local protected evidence | recipe execution summary |

### 6.3 Mutable state

| Path | Purpose | Owner | Backup behavior | Rollback behavior |
| --- | --- | --- | --- | --- |
| `/etc/koa/` | profile configuration, trust references, service configuration | root and canonical service owners | backed up when non-regenerable | restored from verified configuration and profile state |
| `/var/lib/koa/node/` | effective profile, node identity references, activation state | control foundation | included | restore before dependent services |
| `/var/lib/koa/releases/` | immutable Release Sets and activation records | artifact lifecycle owners | included or independently referenced | verify before activation |
| `/var/lib/koa/policies/` | installed governance policy bundles | governance_policy_runtime | included | activate independently |
| `/var/lib/koa/orgo/` | private operational state | orgo | included | component-owned restore |
| `/var/lib/koa/konnaxion/` | public or local participation state | konnaxion | included | component-owned restore |
| `/var/lib/koa/kristal/` | verified Runtime Packs, provenance, active and last-known-good state | kristal_runtime | included or independently referenced | verify and activate independently |
| `/var/lib/koa/mediatheque/` | local media records, versions, managed content, rights, metadata, provenance, and rendition references | koa_mediatheque | authoritative records and managed content included; derived caches regenerable | verify records and rebuild reproducible derivatives |
| `/var/lib/koa/ariane/` | Atlas, driver, local navigation, and bounded session state | ariane_runtime | authoritative state included; caches regenerable | verify local navigation |
| `/var/lib/koa/audit/` | classified receipts and evidence | audit_broker | included according to retention | protected restore and access |
| `/var/lib/koa/quarantine/` | untrusted imports | import owners | not included unless incident policy requires | delete after disposition |
| `/var/lib/koa/backups/` | local encrypted backup staging | backup workflow | not backed up into itself | recreate from protected copies |
| `/run/koa/` | sockets, locks, and runtime state | runtime owners | not backed up | recreated on startup |
| `/var/cache/koa/` | regenerable caches and indexes | component owners | excluded | rebuild from authoritative sources |

No mutable state is shared merely for convenience when its owner contract requires isolation.

## 7. Safety and Security Boundaries

### 7.1 Privilege model

Ordinary application services run unprivileged or inside rootless containers.

Host mutation uses:

```text
narrow privileged broker
```

The approved path is kOA Node Agent or an independently equivalent profile-approved operation broker.

The recipe does not use arbitrary root commands as the product governance interface.

### 7.2 Secret handling

Approved sources can include:

- systemd credentials;
- protected files readable only by the owning service;
- Identity and Trust references;
- a profile-approved local secret service.

The recipe does not place secrets in:

- command history;
- environment dumps;
- container images;
- unit files;
- logs;
- receipts;
- support bundles;
- examples.

Database roles are separate by component.

No component receives another component's database credential.

### 7.3 Network boundaries

Default behavior:

- product UI listens on loopback or a declared local Unix socket;
- component ports remain local or inside the profile-defined service network;
- no public Internet listener is enabled;
- outbound Internet is not required after prerequisite artifact acquisition;
- synchronization, federation, remote support, publication, and external AI remain disabled until explicitly enabled;
- artifact mirrors and backup targets use declared identities and destinations;
- DNS or network loss does not remove local core readiness.

### 7.4 Data authority

One PostgreSQL process can be shared in this reference implementation.

Each stateful component receives:

- a separate database or schema;
- a separate database role;
- owner-only mutation privileges;
- explicit migration ownership;
- no cross-component write grants.

Cross-component mutations use component APIs, events, or gateways.

### 7.5 External integrations

The minimal installation enables none by default.

ChatGPT, Suno, Gamma, Ariane external voice, UCKK publication, remote synchronization, federation, remote support, and external storage require separately registered integrations, user or workflow initiation, data eligibility, policy authorization, provenance, and removal behavior.

External AI output remains candidate material.

### 7.6 Component activation set

| Component | Installation state | Purpose and boundary |
| --- | --- | --- |
| `identity_and_trust` | `installed_and_enabled` | Provides scoped human, organization, tenant, role, node, workload, publisher, signer, authority-channel, and artifact identity and trust foundations. |
| `governance_policy_runtime` | `installed_and_enabled` | Evaluates versioned sociotechnical policy deterministically for authorization, disclosure, consent, privilege, activation, export, and governed exception decisions. |
| `audit_broker` | `installed_and_enabled` | Receives, validates, classifies, sequences, stores, and exports audit events and decision receipts without turning auditability into indiscriminate surveillance. |
| `koa_node_agent` | `installed_and_enabled` | Provides the sole narrow privileged broker for normal kOA node management through fixed, high-level, schema-bound operations. |
| `resource_governor` | `installed_and_enabled` | Applies deterministic resource profiles, quotas, priorities, concurrency limits, task activation, and idle shutdown behavior. |
| `orgo` | `installed_and_enabled` | Converts signals into structured, accountable operational work and preserves execution continuity across online, intermittent, and hermetic environments. |
| `kristal_runtime` | `installed_and_enabled` | Verifies, stores, activates, queries, and exposes portable epistemic artifacts for predictable offline use. |
| `konnaxion` | `installed_and_enabled` | Provides public and commons-oriented discovery, education, collaboration, deliberation, cultural exchange, participation, curation, and distribution. |
| `semantik_architect_runtime` | `installed_and_enabled` | Produces deterministic text from structured data using validated precompiled language artifacts. |
| `koa_mediatheque` | `installed_and_enabled` | Owns local multimedia records, versions, managed content, metadata, rights, provenance, deterministic renditions, lifecycle, export, backup, and restore. |
| `uckk-publication` | `not_installed_by_default` | Optional outbound Moodle publication integration. It is enabled only with Publication Gateway authorization and never owns local media. |
| `uckk-import` | `not_installed_by_default` | Optional inbound learning-package integration. It retrieves or receives selected complete packages into quarantine; local acceptance remains with kOA Mediatheque. |
| `ariane_runtime` | `installed_and_enabled` | Provides deterministic application navigation from validated Atlases, with observation, planning, execution, verification, and safe user control. |
| `publication_gateway` | `not_installed_by_default` | Controls disclosure and publication between private operational domains and public or commons-oriented surfaces. It is added only when the user enables the publication capability through the profile contract. |
| `sentient` | `excluded` | Provides isolated, explicit semantic research, reconciliation, and enrichment that produces candidate artifacts for review. The minimal installation does not deploy it. |
| `gf_wordbench` | `excluded` | Develops, compiles, validates, and publishes deterministic language artifacts for runtime consumption. The minimal installation does not deploy it. |

The profile contract remains authoritative when it differs from this recipe.

## 8. Resource Envelope

### 8.1 Host target

| Resource | Reference target | Minimum preflight | Enforcement or verification |
| --- | ---: | ---: | --- |
| CPU threads | 4–8 | 4 | Resource Governor and cgroup v2 |
| Physical memory | 16 GiB | 16 GiB | cgroup v2 and service limits |
| Compressed swap | 4–8 GiB | active profile-supported swap | zram or equivalent |
| Free storage before install | 120 GiB preferred | 80 GiB | filesystem quota and capacity monitoring |
| Heavy media jobs | 1 | 1 | task queue and concurrency limit |
| SemantiK workers | 1 | 1 | service configuration |
| Normally active language packs | 1 | 1 | SemantiK activation state |
| Permanent virtual machines | 0 | 0 | profile exclusion |
| Heavy Java search services | 0 | 0 | profile exclusion |
| Local AI runtimes | 0 | 0 | profile exclusion |

### 8.2 Service memory budget

| Resource group | Expected | Maximum | Enforcement mechanism |
| --- | ---: | ---: | --- |
| Control foundation | 1.5–2.5 GiB | 3.0 GiB | systemd slices and per-service limits |
| Shared PostgreSQL process | 0.4–0.8 GiB | 1.0 GiB | database service cgroup and connection limits |
| Orgo | 0.2–0.4 GiB | 0.6 GiB | service memory and process limits |
| Kristal Runtime | 0.2–0.5 GiB | 0.75 GiB | service memory and query limits |
| Konnaxion core | 0.3–0.7 GiB | 1.0 GiB | service memory and request limits |
| SemantiK runtime | 0.1–0.3 GiB | 0.5 GiB | one worker and one normally active language pack |
| kOA Mediatheque | 0.5–1.0 GiB | 1.5 GiB | one heavy media job and task-worker cgroups |
| Optional UCKK publication integration | 0–0.2 GiB | 0.3 GiB | task-activated outbound packaging and transport; absent when integration is disabled |
| Optional UCKK import integration | 0–0.3 GiB | 0.5 GiB | task-activated retrieval, quarantine, scanning, and validation; accepted content is stored by kOA Mediatheque |
| Ariane Runtime | 0.2–0.6 GiB | 1.0 GiB | local deterministic navigation limits |
| Browser and user applications | 2.0–4.0 GiB | 6.0 GiB | desktop and browser process controls |
| Combined idle target | 5.0–8.0 GiB | 10.0 GiB | Resource Governor and cgroup v2 |

The browser and active media task can temporarily raise total memory use.

Resource Governor stops or throttles optional jobs before protected services approach unsafe pressure.

### 8.3 Activation strategy

| Activation mode | Workload | Behavior |
| --- | --- | --- |
| `Always on` | Workload | Behavior | Started after local trust and governance; each service retains independent readiness. |
| `Socket or request activated` | Workload | Behavior | Starts only on declared local requests and stops after inactivity where supported. |
| `Task activated` | Workload | Behavior | One heavy media job at a time; bounded queue, timeout, cancellation, and idle shutdown. |
| `Conditional` | Workload | Behavior | Absent or disabled until the exact capability and policy are enabled. |
| `Excluded` | Workload | Behavior | Not installed by this recipe. |

## 9. Naming and Isolation

### 9.1 Canonical naming inputs

```text
profile_id=user_lightweight
environment_id
tenant_id
component_id
artifact_id
release_id
```

The effective profile records every resolved value.

### 9.2 Service and state naming

Reference names use:

```text
koa-<component-id>
koa_<component_id>
/var/lib/koa/<component-id>/
```

The actual names come from active component and profile artifacts.

Database, role, socket, volume, unit, and service identities remain unique by component and environment.

### 9.3 Collision behavior

When a managed resource already exists:

- verify and reuse it only when identity, owner, version, profile, and configuration match;
- migrate it through the component's declared transition when compatible;
- stop with an explicit conflict when ownership or identity differs;
- never overwrite unknown data;
- never reuse a database role across component owners.

## 10. Procedure

### Step 1 — Resolve the exact installation authority

**Objective**

Bind the installation to one accepted authority release, one `user_lightweight` profile version, and one exact Release Set.

**Action**

- load the active authority release;
- select `user_lightweight`;
- confirm that no overlay is being claimed by this recipe;
- resolve the exact system, services, governance, and knowledge artifacts;
- create the installation operation identity.

**Verification**

```bash
jq -e '.primary_profile.id == "user_lightweight"'   /var/lib/koa/node/effective-profile.json
jq -e '.overlays == []'   /var/lib/koa/node/effective-profile.json
jq -e '.release_set_id | type == "string" and length > 0'   /var/lib/koa/node/effective-profile.json
```

**Failure behavior**

No component installation or activation begins.

**Rollback effect**

None; this step is read only apart from the operation record.

---

### Step 2 — Create an installation checkpoint

**Objective**

Preserve a clean rollback and recovery point.

**Action**

- for an upgrade, create a component-owned backup set;
- for a clean install, record that no prior managed state exists;
- verify protected independent storage;
- reserve quarantine, release, database, and component-state capacity.

**Verification**

```bash
jq -e '.result == "pass"' /var/lib/koa/node/backup-readiness.json
test -d /var/lib/koa/quarantine
test -d /var/lib/koa/releases
```

**Failure behavior**

Installation remains blocked.

**Rollback effect**

The prior verified backup remains the recovery source.

---

### Step 3 — Install the control foundation

**Objective**

Establish identity, governance, evidence, privilege, and resource control before application services.

**Action**

Use the profile-approved system artifact importer to install and start:

- Identity and Trust;
- Governance Policy Runtime;
- Audit Broker;
- kOA Node Agent;
- Resource Governor.

The importer identity and exact artifacts are recorded in evidence.

**Verification**

```bash
jq -r '
  .effective_components[]
  | select(.component_id == "identity_and_trust"
        or .component_id == "governance_policy_runtime"
        or .component_id == "audit_broker"
        or .component_id == "koa_node_agent"
        or .component_id == "resource_governor")
  | .service_unit
' /var/lib/koa/node/effective-profile.json |
while IFS= read -r unit; do
  systemctl is-active --quiet "$unit"
done
```

**Failure behavior**

Application services remain stopped.

**Rollback effect**

Deactivate the candidate control artifacts and restore the previous verified control foundation.

---

### Step 4 — Configure component-isolated persistence

**Objective**

Provide one lightweight PostgreSQL process without collapsing component data ownership.

**Action**

- start the profile-approved PostgreSQL service;
- create only the databases or schemas declared by stateful component contracts;
- create one role per component;
- grant mutation only to the owning component;
- apply owner migrations;
- record schema and migration identities.

**Verification**

```bash
psql --no-psqlrc --tuples-only --command="
SELECT datname
FROM pg_database
WHERE datname LIKE 'koa_%'
ORDER BY datname;
"

psql --no-psqlrc --tuples-only --command="
SELECT rolname
FROM pg_roles
WHERE rolname LIKE 'koa_%'
ORDER BY rolname;
"
```

A separate policy check verifies that no component role can write another component's authoritative database or schema.

**Failure behavior**

Stateful application services remain stopped.

**Rollback effect**

Drop only newly created empty managed databases or restore the pre-install checkpoint.

---

### Step 5 — Import and stage application artifacts

**Objective**

Place exact verified application artifacts in quarantine and staging without activating them.

**Action**

Import the services-channel artifacts for:

- Orgo;
- Kristal Runtime;
- Konnaxion;
- SemantiK Architect Runtime;
- kOA Mediatheque;
- Ariane Runtime.

Import through the profile-approved artifact verifier.

**Verification**

```bash
jq -e '
  [.effective_components[]
   | select(.activation == "always_on")
   | .component_id]
  | all(. as $id
      | ["identity_and_trust",
         "governance_policy_runtime",
         "audit_broker",
         "koa_node_agent",
         "resource_governor",
         "orgo",
         "kristal_runtime",
         "konnaxion",
         "semantik_architect_runtime",
         "koa_mediatheque",
         "ariane_runtime"]
        | index($id))
' /var/lib/koa/node/effective-profile.json
```

**Failure behavior**

The failed artifact remains quarantined and no application activation occurs.

**Rollback effect**

Remove only inactive staged candidates.

---

### Step 6 — Apply resource limits and task activation

**Objective**

Keep idle use within the lightweight envelope and prevent heavy work from destabilizing protected services.

**Action**

- assign protected and application service slices;
- apply memory, CPU, I/O, process, queue, and timeout limits;
- limit SemantiK to one worker;
- activate one language pack normally;
- limit kOA Mediatheque to one heavy media job;
- configure thumbnail, preview, extraction, indexing, backup, and synchronization workers for task activation and idle shutdown;
- keep low-priority background I/O below interactive and integrity-critical work.

**Verification**

```bash
systemctl show koa-protected.slice   --property=MemoryHigh,MemoryMax,CPUWeight,IOWeight
systemctl show koa-applications.slice   --property=MemoryHigh,MemoryMax,CPUWeight,IOWeight
systemctl show koa-tasks.slice   --property=MemoryHigh,MemoryMax,CPUWeight,IOWeight
```

```bash
jq -e '
  .resource_policy.heavy_media_concurrency == 1
  and .resource_policy.semantik_workers == 1
  and .resource_policy.normal_active_language_packs == 1
' /var/lib/koa/node/effective-profile.json
```

**Failure behavior**

Application activation remains blocked or the affected optional capability is disabled.

**Rollback effect**

Restore the previous validated resource policy.

---

### Step 7 — Activate application services

**Objective**

Activate the verified services atomically according to component and Release Set dependencies.

**Action**

- start the always-on component services;
- keep optional and task workers inactive until requested;
- run component readiness checks;
- retain the previous compatible non-revoked services selection until health passes.

**Verification**

```bash
jq -r '
  .effective_components[]
  | select(.activation == "always_on")
  | .service_unit
' /var/lib/koa/node/effective-profile.json |
while IFS= read -r unit; do
  systemctl is-enabled --quiet "$unit"
  systemctl is-active --quiet "$unit"
done
```

```bash
systemctl --failed --no-legend
```

**Failure behavior**

Only dependent capabilities remain unavailable, and the services activation reports failure.

**Rollback effect**

Restore the last-known-good services selection.

---

### Step 8 — Install governance and knowledge artifacts

**Objective**

Install and independently activate the governance bundle, one SemantiK language pack, required Kristal Runtime Packs, and Ariane Atlas and driver artifacts.

**Action**

- verify exact artifact identities;
- verify publisher, signer, trust, revocation, audience, compatibility, and profile;
- stage each artifact class independently;
- obtain the required activation decisions;
- activate atomically;
- run language, Kristal, and Ariane vectors.

**Verification**

```bash
jq -e '
  .governance.status == "active"
  and .language.active_count == 1
  and .kristal.active_pack_count >= 1
  and .ariane.local_navigation == "ready"
' /var/lib/koa/node/active-artifacts.json
```

**Failure behavior**

The failed artifact class remains inactive while unrelated valid artifact classes remain available.

**Rollback effect**

Restore the compatible non-revoked predecessor for the failed artifact class.

---

### Step 9 — Configure the local user surface

**Objective**

Provide one lightweight local user workspace without multiple permanent Electron clients.

**Action**

- expose product workspaces through one maintained browser or profile-approved local shell;
- bind local endpoints to loopback or declared local sockets;
- enable keyboard, pointer, touch, shortcuts, and deterministic Ariane navigation;
- keep external voice and external AI disabled;
- prevent public listeners and arbitrary desktop administration through product routes.

**Verification**

```bash
ss --tcp --udp --listening --numeric --process
```

Review confirms that every listener is declared by the effective profile and that product listeners are local only.

```bash
jq -e '
  .ariane.local_navigation == true
  and .ariane.external_voice == false
  and .external_ai.enabled == false
' /var/lib/koa/node/effective-profile.json
```

**Failure behavior**

The user surface remains unavailable while control, backup, and recovery functions remain intact.

**Rollback effect**

Restore the previous browser or shell configuration without changing component data.

---

### Step 10 — Prove offline behavior

**Objective**

Show that local core operation does not require Internet, a control plane, external AI, or a heavy workbench.

**Action**

- disable external network connectivity using the profile-approved test method;
- authenticate locally;
- open Orgo and Konnaxion local workspaces;
- query an active Kristal Runtime Pack;
- render through SemantiK;
- ingest a small local file into the kOA Mediatheque through the deterministic path;
- navigate using Ariane without voice;
- verify audit receipts and local cancellation.

**Verification**

Run the exact profile test implementations for:

- `TEST-SYS-001`
- `TEST-SYS-002`
- `TEST-SYS-005`
- `TEST-SYS-006`
- `TEST-SYS-009`
- `TEST-SYS-012`
- `TEST-PROF-006`
- `TEST-PROF-010`

**Failure behavior**

The installation does not receive a conformant `user_lightweight` claim.

**Rollback effect**

No data rollback is required; repair the dependency or profile composition and repeat the tests.

---

### Step 11 — Create and test the initial backup

**Objective**

Establish continuity before the installation is declared complete.

**Action**

- create component-owned checkpoints;
- assemble an encrypted backup set;
- write a protected independent copy;
- verify inventory, rights, revocation, artifacts, and provenance;
- perform an isolated or clean restore test according to the active backup policy.

**Verification**

```bash
jq -e '
  .backup_result == "pass"
  and .independent_copy == "verified"
  and .restore_test == "pass"
' /var/lib/koa/node/backup-readiness.json
```

**Failure behavior**

The installation can remain locally usable but is not described as continuity ready.

**Rollback effect**

The previous verified backup remains available.

---

### Step 12 — Finalize evidence and installation state

**Objective**

Produce one reproducible installation result.

**Action**

- run all required tests;
- collect classified evidence;
- record the exact profile, Release Set, authority release, artifacts, component states, resource policy, backup, and exceptions;
- mark installation complete only after required results pass.

**Verification**

```bash
jq -e '
  .recipe_id == "RECIPE-UL-001"
  and .recipe_version == "1.0.0"
  and .profile_ids == ["user_lightweight"]
  and .rollback_available == true
  and .result == "pass"
' /var/lib/koa/audit/recipe-ul-001-execution.json
```

**Failure behavior**

The result remains `fail` or `blocked`, with the exact failed step and retained safe state.

**Rollback effect**

Follow Section 14 when the failure affects active state.

## 11. Idempotency

```text
Idempotent: conditional
```

Repeated execution is safe when:

- the authority release is unchanged;
- the profile version is unchanged;
- the exact Release Set is unchanged;
- managed resources have matching identity and owner;
- no migration is pending;
- no conflicting unmanaged resource exists.

Repeated execution:

- verifies existing correct state;
- does not duplicate component data;
- does not rotate secrets or certificates unless the active operation explicitly requests rotation;
- does not create new database identities when the declared identities already exist;
- does not activate new artifacts when the current selection already matches;
- stops on identity, ownership, version, or configuration conflict.

## 12. Validation

### 12.1 Functional validation

```bash
systemctl --failed --no-legend
```

Expected result: no failed required unit.

```bash
jq -e '.primary_profile.id == "user_lightweight"'   /var/lib/koa/node/effective-profile.json
```

Expected result: exit status zero.

```bash
jq -e '.status == "ready_local"'   /var/lib/koa/node/operational-status.json
```

Expected result: exit status zero while external connectivity is unavailable.

### 12.2 Contract validation

Validate:

- effective profile;
- active Release Set;
- component contracts;
- governance bundle;
- language pack;
- Kristal Runtime Packs;
- Ariane artifacts;
- backup set;
- evidence objects.

The exact validator commands are supplied by the active artifact and profile toolchain.

This recipe does not invent a validator executable when the canonical toolchain has not declared one.

### 12.3 Lock validation

```bash
python docs/tools/check_interfile_locks.py
```

Expected locks include:

- `LOCK-PROFILE-001`
- `LOCK-PROFILE-002`
- `LOCK-IMPL-001`
- `LOCK-IMPL-002`
- `LOCK-DOC-003`
- `LOCK-DOC-016`
- `LOCK-DOC-021`
- `LOCK-DOC-022`
- `LOCK-COMP-001`
- `LOCK-COMP-002`
- `LOCK-DATA-001`
- `LOCK-GOV-001`
- `LOCK-AI-001`
- `LOCK-AI-002`
- `LOCK-SENT-001`
- `LOCK-UCKK-EXT-001`
- `LOCK-UCKK-EXT-002`
- `LOCK-ARI-001`
- `LOCK-ARI-002`
- `LOCK-LIFE-001`
- `LOCK-LIFE-002`
- `LOCK-LIFE-003`
- `LOCK-LIFE-004`

### 12.4 Profile and system validation

Required test evidence includes:

| Test ID | Purpose | Required result |
| --- | --- | --- |
| `TEST-PROF-001` | Profile identities are unique | `pass` |
| `TEST-PROF-002` | Profile inheritance is explicit | `pass` |
| `TEST-PROF-004` | Profile exclusions are explicit | `pass` |
| `TEST-PROF-005` | Profile resource envelopes are complete | `pass` |
| `TEST-PROF-006` | Profile offline envelopes are tested | `pass` |
| `TEST-PROF-008` | Profile component membership resolves | `pass` |
| `TEST-PROF-010` | User lightweight profile excludes heavy workbenches | `pass` |
| `TEST-PROF-014` | Endpoint profiles do not require Kubernetes | `pass` |
| `TEST-SYS-001` | Core operation remains available offline | `pass` |
| `TEST-SYS-002` | No native AI dependency exists | `pass` |
| `TEST-SYS-003` | External AI surfaces are user initiated | `pass` |
| `TEST-SYS-004` | Authority fails closed | `pass` |
| `TEST-SYS-005` | Safe degradation is capability scoped | `pass` |
| `TEST-SYS-006` | Ariane navigation works without voice | `pass` |
| `TEST-SYS-009` | SemantiK runtime is deterministic | `pass` |
| `TEST-SYS-010` | Resource governance is deterministic | `pass` |
| `TEST-SYS-011` | Critical transitions produce receipts | `pass` |
| `TEST-SYS-012` | External integrations are removable | `pass` |
| `TEST-SYS-013` | Component stores remain isolated | `pass` |
| `TEST-SYS-015` | Optional heavy work is task activated | `pass` |
| `TEST-SEC-001` | Arbitrary privileged commands are rejected | `pass` |
| `TEST-SEC-003` | Policy binding and replay protection succeed | `pass` |
| `TEST-SEC-005` | Unknown policy facts fail closed | `pass` |
| `TEST-SEC-008` | Private keys are not normally exportable | `pass` |
| `TEST-SEC-009` | Tenant and domain separation is enforced | `pass` |
| `TEST-SEC-011` | Protected audit access is audited | `pass` |
| `TEST-SEC-012` | No-AI data remains outside external AI surfaces | `pass` |
| `TEST-SEC-013` | Cultural withdrawal propagates | `pass` |
| `TEST-SEC-014` | Audience-scoped artifacts enforce audience restrictions | `pass` |
| `TEST-SEC-015` | Software supply-chain evidence is verifiable | `pass` |
| `TEST-CROSS-004` | Resource and governance authorities remain separate | `pass` |
| `TEST-CROSS-005` | Language build and runtime remain separate | `pass` |
| `TEST-CROSS-006` | SenTient remains isolated and non-authoritative | `pass` |
| `TEST-CROSS-007` | Node Agent rejects arbitrary privileged execution | `pass` |
| `TEST-CROSS-008` | Policy decision precedes governed privilege | `pass` |
| `TEST-CROSS-009` | Audit Broker does not become an authorization engine | `pass` |
| `TEST-CROSS-011` | Ariane voice remains externally optional | `pass` |
| `TEST-CROSS-012` | kOA Mediatheque ingestion remains deterministic; UCKK publication and import remain external, separate, governed, and non-synchronizing | `pass` |
| `TEST-CROSS-013` | External AI cannot directly mutate authority | `pass` |
| `TEST-CROSS-014` | Identity layers remain distinct | `pass` |
| `TEST-CROSS-015` | All cross-component mutations are contract-bound | `pass` |
| `TEST-LIFE-003` | Artifact verification precedes activation | `pass` |
| `TEST-LIFE-004` | Activation is atomic for the artifact class | `pass` |
| `TEST-LIFE-005` | Rollback restores a valid predecessor | `pass` |
| `TEST-LIFE-008` | Offline bundle parsing is bounded | `pass` |
| `TEST-LIFE-011` | Last-known-good artifacts are retained | `pass` |
| `TEST-LIFE-012` | Policy bundles activate independently | `pass` |
| `TEST-LIFE-013` | Language artifacts activate independently | `pass` |
| `TEST-LIFE-014` | Kristal runtime packs activate independently | `pass` |
| `TEST-LIFE-015` | Release evidence is complete | `pass` |
| `TEST-OPS-001` | Health and readiness are distinct | `pass` |
| `TEST-OPS-002` | Observability avoids sensitive overcollection | `pass` |
| `TEST-OPS-003` | Resource pressure preserves critical work | `pass` |
| `TEST-OPS-004` | Backup completes with evidence | `pass` |
| `TEST-OPS-005` | Restore is tested | `pass` |
| `TEST-OPS-006` | Offline operations remain manageable | `pass` |
| `TEST-OPS-008` | Maintenance does not create partial activation | `pass` |
| `TEST-OPS-009` | Support bundles are sanitized | `pass` |
| `TEST-OPS-010` | Capacity limits produce explicit degradation | `pass` |
| `TEST-EXIT-001` | Full export is available | `pass` |
| `TEST-EXIT-002` | Export is independently verifiable | `pass` |
| `TEST-EXIT-003` | Clean restore succeeds | `pass` |
| `TEST-EXIT-005` | Restored artifacts preserve provenance | `pass` |
| `TEST-EXIT-006` | Exit does not require a single operator | `pass` |
| `TEST-EXIT-008` | External integration removal preserves core data | `pass` |
| `TEST-DOC-VAL-003` | Canonical references resolve | `pass` |
| `TEST-DOC-VAL-005` | Canonical ownership is exclusive | `pass` |
| `TEST-DOC-VAL-006` | Decision references are accepted | `pass` |
| `TEST-DOC-VAL-012` | Generated content is reproducible | `pass` |
| `TEST-DOC-VAL-016` | Traceability is complete | `pass` |
| `TEST-DOC-VAL-017` | Authority activation occurs last | `pass` |
| `TEST-DOC-VAL-019` | Registry and schema versions are compatible | `pass` |
| `TEST-DOC-VAL-020` | Validation performs no semantic auto-fix | `pass` |

### 12.5 Documentation validation

When this recipe or a generated example changes:

```bash
python docs/tools/validate_docs.py
```

### 12.6 Success criteria

The recipe succeeds only when:

- one active primary profile is `user_lightweight`;
- no overlay claim is implied;
- all required components and artifacts resolve;
- excluded heavy workbenches remain absent;
- every required service is ready;
- one PostgreSQL process preserves component identity and mutation separation;
- idle resource use remains within the reference envelope during the measured validation interval;
- one heavy media job limit is enforced;
- one SemantiK worker and one normal active language pack are enforced;
- core local workflows pass without external connectivity;
- external AI remains disabled;
- backup and clean restore pass;
- rollback remains available;
- all required tests and evidence pass;
- no secret appears in logs or output.

## 13. Failure Handling

| Failure | Detection | Safe state | Required action |
| --- | --- | --- | --- |
| Host prerequisite missing | Preflight command fails. | No kOA state changes. | Install or enable the missing profile-supported prerequisite and rerun preflight. |
| Authority or Release Set unresolved | Canonical input or signature verification cannot complete. | Installation remains blocked; staged files remain quarantined. | Obtain the exact accepted authority and Release Set. |
| Insufficient memory or storage | Resource check or installation reservation fails. | Existing services remain unchanged. | Free space, add capacity, or select a different valid profile. |
| Component artifact verification fails | Artifact verifier rejects identity, trust, inventory, compatibility, or revocation. | Candidate remains inactive. | Replace the candidate with a verified compatible artifact. |
| Database isolation validation fails | Cross-component grants or shared owner credentials are detected. | Application services remain stopped. | Create separate roles and databases or schemas, then revalidate. |
| Service readiness fails | A required service does not satisfy its declared readiness contract. | Only dependent capabilities remain unavailable; no whole-node success is reported. | Inspect bounded logs and owner diagnostics, repair, then rerun readiness. |
| Resource pressure | Memory, CPU, I/O, queue, or storage threshold is reached. | Optional and heavy work stops before protected services. | Cancel heavy jobs, clear regenerable caches, or add capacity. |
| Offline verification fails | A core operation contacts an undeclared remote destination or cannot complete locally. | The affected profile claim fails. | Remove the dependency or correct local artifact availability. |
| Backup validation fails | No independent protected copy or restore test is current. | Installation can remain locally operational, but continuity is not claimed. | Complete backup and clean restore testing. |
| Rollback validation fails | The predecessor cannot be verified or restored. | New activation remains blocked. | Repair the predecessor or define accepted forward repair before activation. |

Retries remain bounded.

A failure after activation does not leave a mixed Release Set or partially active artifact class.

When verification cannot complete, the result is `blocked`.

## 14. Rollback

### 14.1 Rollback triggers

Rollback is required when:

- a control-foundation service cannot satisfy readiness;
- a services activation creates an incompatible or unhealthy selection;
- a migration cannot complete safely;
- resource limits cannot protect integrity-critical work;
- an artifact fails post-activation vectors;
- database isolation is violated;
- local offline operation regresses;
- recovery or backup becomes unusable because of the change.

### 14.2 Rollback prerequisites

- previous verified Release Set;
- previous active authority release or compatible retained governance state;
- component-owned backup checkpoints;
- last-known-good language, Kristal, and Ariane artifacts;
- kOA Node Agent or recovery-environment authority;
- classified rollback evidence path.

### 14.3 Rollback procedure

1. stop new application work;
2. cancel or checkpoint task workers;
3. preserve local evidence;
4. enter maintenance or recovery when required;
5. select the previous compatible non-revoked Release Set;
6. restore component state only when migration changed authoritative data;
7. activate previous system, services, governance, and knowledge artifacts through their separate lifecycle owners;
8. run health, offline, database-isolation, and workflow tests;
9. retain the failed candidate in quarantine;
10. record rollback evidence.

### 14.4 Rollback verification

```bash
jq -e '
  .rollback_result == "pass"
  and .status == "ready_local"
  and .mixed_release_state == false
' /var/lib/koa/node/operational-status.json
```

### 14.5 Irreversible changes

No irreversible change is permitted by this recipe.

A component migration that cannot roll back requires an accepted forward-repair plan, a verified backup, and owner evidence before activation.

## 15. Cleanup and Removal

To remove this installation safely:

1. create and verify the required backup or Sovereignty Bundle;
2. stop new component work;
3. export or transfer governed data through owner contracts;
4. revoke or transfer node, workload, user, and target credentials;
5. disable external integrations and synchronization;
6. remove active services through the profile-approved lifecycle;
7. remove only component-owned managed state after retention and exit authority;
8. remove rootless images, volumes, networks, sockets, and caches associated with this environment;
9. preserve required audit, deletion, migration, and exit evidence;
10. verify that no listener, service identity, credential, or managed state remains.

Cleanup does not remove:

- another environment's state;
- shared verified artifacts still referenced by another active environment;
- protected backups before retention and exit permit deletion;
- required historical evidence;
- global rootless image cache entries still referenced elsewhere.

## 16. Observability and Evidence

### 16.1 Logs

Logs are owner scoped and can reside under:

```text
/var/log/koa/
/var/lib/koa/audit/
```

They include:

- operation and correlation identity;
- component identity;
- environment identity;
- profile identity;
- release and artifact identity;
- bounded status and error information.

They exclude secrets and minimize protected data.

### 16.2 Metrics

Relevant metrics include:

- total and per-slice memory;
- CPU and I/O pressure;
- task queue length;
- heavy media concurrency;
- task idle-shutdown count;
- disk capacity;
- database connections by component role;
- service health and readiness;
- local request latency;
- active language-pack count;
- active and last-known-good artifact identities;
- backup age and independent-copy state;
- external network dependency attempts;
- failed policy or privilege decisions.

### 16.3 Receipts

```text
Receipt required: yes
Receipt contract: Audit Broker critical-transition evidence
```

Receipts cover:

- profile resolution;
- artifact verification;
- control-foundation activation;
- services activation;
- governance and knowledge activation;
- database isolation validation;
- offline test;
- backup and restore test;
- rollback when used;
- cleanup or removal.

### 16.4 Evidence

Required evidence includes the test IDs in Section 12 and:

- `EVID-RECIPE-UL-001-AUTHORITY`
- `EVID-RECIPE-UL-001-PREFLIGHT`
- `EVID-RECIPE-UL-001-COMPONENTS`
- `EVID-RECIPE-UL-001-DATABASE`
- `EVID-RECIPE-UL-001-RESOURCES`
- `EVID-RECIPE-UL-001-OFFLINE`
- `EVID-RECIPE-UL-001-BACKUP`
- `EVID-RECIPE-UL-001-RESTORE`
- `EVID-RECIPE-UL-001-ROLLBACK`
- `EVID-RECIPE-UL-001-EXECUTION`

Evidence is sufficient to verify the installation without conversational context.

## 17. Offline Behavior

```text
offline_after_prerequisite_download
```

Prerequisite acquisition includes:

- exact system Release Set artifacts;
- exact services Release Set artifacts;
- governance bundle;
- one active SemantiK language pack;
- required Kristal Runtime Packs;
- Ariane Atlas and driver artifacts;
- profile, schema, trust, and revocation material;
- recovery artifacts.

The source can be a verified repository, local mirror, or bounded offline bundle.

After acquisition:

- local operation does not contact external services silently;
- external AI remains disabled;
- synchronization queues remain bounded;
- local backups continue;
- stale trust and revocation state remains visible;
- imported media enters quarantine;
- queued outbound work is revalidated before later transmission.

## 18. Compatibility and Versioning

| Dependency | Compatible range | Incompatible range | Migration action |
| --- | --- | --- | --- |
| `user_lightweight` profile | exact active compatible version | retired, superseded without migration, or unresolved version | apply profile migration and rerun full recipe validation |
| system Release Set | exact profile-compatible selection | incompatible kernel, host runtime, or recovery contract | retain predecessor or perform accepted system migration |
| services Release Set | exact component-compatible selection | missing required component or unsupported store migration | stage corrected selection or forward repair |
| governance release | active compatible authority floor | revoked, expired, incompatible, or unresolved | activate a verified compatible governance bundle |
| knowledge release | compatible language, Kristal, and Ariane artifacts | incompatible runtime contract, audience, or revocation state | retain predecessor and import compatible artifacts |
| PostgreSQL | range declared by component contracts and services artifacts | unsupported schema or migration state | component-owned database migration |
| recipe | `1.x` | future breaking procedure | use the major-version migration and rollback instructions |

A breaking recipe change requires:

- new major recipe version;
- accepted decision when architecture changes;
- impact analysis;
- updated tests and evidence;
- updated rollback or migration steps.

## 19. AI Execution Protocol

An AI agent executing this recipe:

1. loads active canonical context;
2. verifies recipe status `active`;
3. verifies `user_lightweight` is the selected primary profile;
4. verifies that this recipe claims no overlay;
5. resolves all canonical references;
6. verifies accepted decisions and applicable locks;
7. records the exact Release Set and authority release;
8. executes one atomic step at a time;
9. runs each verification immediately;
10. stops on unexpected state;
11. does not invent artifact identities, versions, commands, service units, paths, ports, credentials, or database ownership;
12. uses the active profile and artifact toolchain for state-changing operations;
13. does not expose secrets;
14. does not repair unrelated state;
15. reports `blocked` when authority, artifacts, evidence, or tools do not resolve.

The agent does not treat this recipe as independent authority.

### 19.1 Required execution summary

```json
{
  "recipe_id": "RECIPE-UL-001",
  "recipe_version": "1.0.0",
  "profile_ids": [
    "user_lightweight"
  ],
  "component_ids": [
    "identity_and_trust",
    "governance_policy_runtime",
    "audit_broker",
    "koa_node_agent",
    "resource_governor",
    "orgo",
    "kristal_runtime",
    "konnaxion",
    "semantik_architect_runtime",
    "koa_mediatheque",
    "ariane_runtime"
],
  "workspace_id": null,
  "decision_ids": [
    "DEC-PROFILE-001",
    "DEC-SYS-001",
    "DEC-AUTH-001",
    "DEC-IDENT-001",
    "DEC-DATA-001",
    "DEC-COMP-001",
    "DEC-GOV-001",
    "DEC-AI-001",
    "DEC-SENT-001",
    "DEC-UCKK-EXT-001",
    "DEC-ARI-001",
    "DEC-LANG-001",
    "DEC-LIFE-001"
],
  "requirement_ids": [
    "REQ-PROF-MODEL-005",
    "REQ-PROF-MODEL-009",
    "REQ-PROF-MODEL-012",
    "REQ-PROF-MODEL-014",
    "REQ-PROF-MODEL-016",
    "REQ-PROF-MODEL-018",
    "REQ-PROF-MODEL-019",
    "REQ-PROF-MODEL-022",
    "REQ-PROF-MODEL-023",
    "REQ-PROF-MODEL-024",
    "REQ-PROF-MODEL-026",
    "REQ-SEC-AI-001",
    "REQ-SEC-AI-002",
    "REQ-SEC-AI-007",
    "REQ-SEC-AI-018",
    "REQ-SEC-AI-023",
    "REQ-SEC-AI-024",
    "REQ-OPS-BACKUP-001",
    "REQ-OPS-BACKUP-002",
    "REQ-OPS-BACKUP-009",
    "REQ-OPS-BACKUP-011",
    "REQ-OPS-BACKUP-018",
    "REQ-OPS-BACKUP-026",
    "REQ-OPS-BACKUP-028",
    "REQ-OPS-BACKUP-030",
    "REQ-OPS-BACKUP-035",
    "REQ-OPS-BACKUP-036",
    "REQ-OPS-BACKUP-037",
    "REQ-OPS-BACKUP-039"
],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-DOC-003",
    "LOCK-DOC-016",
    "LOCK-DOC-021",
    "LOCK-DOC-022",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SENT-001",
    "LOCK-UCKK-EXT-001",
    "LOCK-UCKK-EXT-002",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004"
],
  "exception_ids": [],
  "commands_executed": [],
  "tests_run": [
    "TEST-PROF-001",
    "TEST-PROF-002",
    "TEST-PROF-004",
    "TEST-PROF-005",
    "TEST-PROF-006",
    "TEST-PROF-008",
    "TEST-PROF-010",
    "TEST-PROF-014",
    "TEST-SYS-001",
    "TEST-SYS-002",
    "TEST-SYS-003",
    "TEST-SYS-004",
    "TEST-SYS-005",
    "TEST-SYS-006",
    "TEST-SYS-009",
    "TEST-SYS-010",
    "TEST-SYS-011",
    "TEST-SYS-012",
    "TEST-SYS-013",
    "TEST-SYS-015",
    "TEST-SEC-001",
    "TEST-SEC-003",
    "TEST-SEC-005",
    "TEST-SEC-008",
    "TEST-SEC-009",
    "TEST-SEC-011",
    "TEST-SEC-012",
    "TEST-SEC-013",
    "TEST-SEC-014",
    "TEST-SEC-015",
    "TEST-CROSS-004",
    "TEST-CROSS-005",
    "TEST-CROSS-006",
    "TEST-CROSS-007",
    "TEST-CROSS-008",
    "TEST-CROSS-009",
    "TEST-CROSS-011",
    "TEST-CROSS-012",
    "TEST-CROSS-013",
    "TEST-CROSS-014",
    "TEST-CROSS-015",
    "TEST-LIFE-003",
    "TEST-LIFE-004",
    "TEST-LIFE-005",
    "TEST-LIFE-008",
    "TEST-LIFE-011",
    "TEST-LIFE-012",
    "TEST-LIFE-013",
    "TEST-LIFE-014",
    "TEST-LIFE-015",
    "TEST-OPS-001",
    "TEST-OPS-002",
    "TEST-OPS-003",
    "TEST-OPS-004",
    "TEST-OPS-005",
    "TEST-OPS-006",
    "TEST-OPS-008",
    "TEST-OPS-009",
    "TEST-OPS-010",
    "TEST-EXIT-001",
    "TEST-EXIT-002",
    "TEST-EXIT-003",
    "TEST-EXIT-005",
    "TEST-EXIT-006",
    "TEST-EXIT-008",
    "TEST-DOC-VAL-003",
    "TEST-DOC-VAL-005",
    "TEST-DOC-VAL-006",
    "TEST-DOC-VAL-012",
    "TEST-DOC-VAL-016",
    "TEST-DOC-VAL-017",
    "TEST-DOC-VAL-019",
    "TEST-DOC-VAL-020"
],
  "evidence_ids": [
    "EVID-RECIPE-UL-001-AUTHORITY",
    "EVID-RECIPE-UL-001-PREFLIGHT",
    "EVID-RECIPE-UL-001-COMPONENTS",
    "EVID-RECIPE-UL-001-DATABASE",
    "EVID-RECIPE-UL-001-RESOURCES",
    "EVID-RECIPE-UL-001-OFFLINE",
    "EVID-RECIPE-UL-001-BACKUP",
    "EVID-RECIPE-UL-001-RESTORE",
    "EVID-RECIPE-UL-001-EXECUTION"
  ],
  "rollback_available": true,
  "result": "pass"
}
```

The runtime execution record replaces the empty command list and changes the result when execution does not pass.

## 20. Troubleshooting

### Local readiness fails after services start

**Observed signal**

```text
operational status is degraded or one required service is not ready
```

**Likely bounded causes**

- a required artifact is incompatible;
- database migration or ownership is incomplete;
- memory or storage pressure blocks readiness;
- a required local socket or dependency is unavailable.

**Diagnostic commands**

```bash
systemctl --failed --no-legend
journalctl --priority=warning --boot --no-pager
jq '.' /var/lib/koa/node/operational-status.json
```

**Corrective action**

Use the failing component's owner diagnostics, correct only the declared dependency, and repeat its readiness and dependent tests.

**Escalation condition**

Escalate when the owner contract, migration state, or authority decision is ambiguous.

---

### Idle memory exceeds the reference envelope

**Observed signal**

```text
combined idle memory remains above 10 GiB after task workers should have stopped
```

**Likely bounded causes**

- a task worker did not exit;
- multiple browser or media processes remain active;
- a service limit was not applied;
- an excluded heavy service was installed.

**Diagnostic commands**

```bash
systemd-cgtop --depth=3
systemctl list-units --state=running
podman ps --format '{{.Names}}	{{.Status}}'
```

**Corrective action**

Stop undeclared or completed task workers, restore validated cgroup limits, and remove excluded services through managed cleanup.

**Escalation condition**

Escalate when a required service cannot satisfy its contract within the profile resource envelope.

---

### Offline test attempts an external connection

**Observed signal**

```text
network policy or packet capture records an undeclared outbound request during a core local workflow
```

**Likely bounded causes**

- an external integration was enabled;
- a local artifact is missing;
- a browser or service uses an undeclared remote asset;
- an update or telemetry function is active.

**Diagnostic commands**

```bash
ss --tcp --udp --all --numeric --process
journalctl --boot --grep='network\|connect\|dns' --no-pager
```

**Corrective action**

Disable the undeclared integration, install the required local artifact, or correct the component configuration and rerun the offline test.

**Escalation condition**

Escalate when the dependency is embedded in a required artifact or component contract.

---

### Database isolation test fails

**Observed signal**

```text
a component role can modify another component's database or schema
```

**Likely bounded causes**

- shared owner credential;
- broad database grants;
- migration executed under the wrong role;
- unmanaged unsupported schema.

**Diagnostic command**

```bash
psql --no-psqlrc --command='\du+'
```

**Corrective action**

Revoke cross-component grants, create owner-specific roles, repair ownership, and rerun component mutation-boundary tests.

**Escalation condition**

Escalate before changing authoritative ownership or merging schemas.

---

### Backup exists but restore test fails

**Observed signal**

```text
backup result passes while clean restore or workflow-resume result fails
```

**Likely bounded causes**

- missing dependency artifact;
- incomplete component checkpoint;
- missing trust or revocation context;
- index rebuild or migration failure;
- undocumented operator knowledge.

**Diagnostic action**

Inspect the backup manifest, component checkpoints, restore contract, test evidence, and exact failed restore phase.

**Corrective action**

Recreate the backup after correcting scope, dependencies, migration, or restore instructions, then repeat the clean restore.

**Escalation condition**

Escalate when the source component cannot produce a complete owner export.

## 21. Non-Normative Example

A user installs kOA on a four-core computer with 16 GiB of memory and a 512 GiB SSD.

The active `user_lightweight` Release Set includes:

- the control foundation;
- Orgo;
- Kristal Runtime;
- Konnaxion core;
- SemantiK runtime;
- kOA Mediatheque;
- Ariane Runtime;
- one French language pack;
- one local Kristal Runtime Pack.

The installation excludes SenTient, GF Wordbench, Elasticsearch, Solr, OpenRefine, development containers, permanent virtual machines, and local generative AI.

At idle:

- the control and application services use 6.4 GiB;
- the browser uses 1.8 GiB;
- no media task is active;
- no external connection is required.

The user imports a video.

One kOA Mediatheque task worker starts, produces a preview, records provenance, and exits after completion. A second heavy media request remains queued until the first finishes.

The user disconnects the network and can still authenticate, use local Orgo and Konnaxion workspaces, query Kristal, render French through SemantiK, navigate with Ariane, and inspect local receipts.

The initial encrypted backup restores successfully on a clean compatible test environment.

These example values demonstrate the recipe and are not global profile defaults.

## 22. Maintenance

The recipe owner reviews this file when any referenced:

- decision;
- profile;
- component membership;
- component contract;
- resource envelope;
- system or services artifact;
- governance or knowledge artifact;
- database compatibility rule;
- AI boundary;
- backup or restore contract;
- test;
- evidence;
- implementation technology

changes.

Impact analysis assigns one of:

```text
updated
reviewed_no_change
regenerated
deprecated
blocked
```

The recipe is deprecated when the implementation remains usable but is no longer recommended.

It is superseded when another active recipe replaces it.

It is archived when no active supported installation uses it.

## 23. Author Checklist

- [x] All template markers are removed.
- [x] `DOC-RECIPE-UL-001` and `RECIPE-UL-001` are assigned.
- [x] The file is classified as a non-normative recipe.
- [x] Status is `active`.
- [x] Canonical references are explicit.
- [x] Decisions and locks are listed.
- [x] `user_lightweight` is the only supported profile claim.
- [x] Unsupported profiles and overlays are explicit.
- [x] Preconditions are testable.
- [x] Inputs, outputs, and mutable state are declared.
- [x] Privilege is minimized.
- [x] Secrets are protected.
- [x] Network and offline behavior are explicit.
- [x] Resource targets and limits are explicit.
- [x] Heavy services and workbenches are excluded.
- [x] Task activation and idle shutdown are explicit.
- [x] Database ownership remains separated.
- [x] Procedure steps are atomic and verifiable.
- [x] Idempotency is declared.
- [x] Failure behavior and rollback are complete.
- [x] Cleanup is scoped.
- [x] Observability and evidence are explicit.
- [x] AI execution behavior is bounded.
- [x] No recipe choice is presented as a global architectural default.
