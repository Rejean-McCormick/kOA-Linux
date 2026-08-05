<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-RECIPE-SOV-QUADLET-LAYOUT",
  "document_class": "recipe",
  "status": "active",
  "language": "en",
  "layer": "implementation_recipe",
  "scope": [
    "sovereign_linux_node"
  ],
  "authority": "non_normative",
  "adopted_by_profile_ids": [],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "generated/document-index.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "contracts/components/resource-governor.component.json",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/components/koa-node-agent.component.json",
    "generated/profile-catalog.json",
    "contracts/profiles/sovereign-linux-node.profile.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "contracts/artifact-contracts/resource-envelope.schema.json",
    "contracts/examples/resource-envelope.example.json",
    "03-profiles/07-sovereign-linux-node.md",
    "06-lifecycle/04-release-sets.md",
    "06-lifecycle/06-service-updates.md",
    "06-lifecycle/13-activation-and-verification.md",
    "07-security/05-privilege-boundaries.md",
    "07-security/06-privileged-broker.md",
    "07-security/07-secrets-and-keys.md",
    "07-security/08-network-boundaries.md",
    "07-security/09-storage-boundaries.md",
    "08-operations/04-resource-envelopes.md",
    "08-operations/14-maintenance.md",
    "08-operations/18-sovereign-node-operations.md",
    "10-adrs/ADR-005-rootless-podman-and-quadlet.md",
    "10-adrs/ADR-012-single-narrow-privileged-broker.md",
    "10-adrs/ADR-019-resource-governor-and-policy-runtime-separation.md",
    "contracts/integrations/uckk-import.integration.json",
    "contracts/artifact-contracts/uckk-learning-package.schema.json",
    "contracts/artifact-contracts/uckk-import-receipt.schema.json"
  ],
  "decision_ids": [
    "DEC-CONTAINER-001",
    "DEC-PROFILE-001",
    "DEC-OS-001",
    "DEC-IMAGE-001",
    "DEC-PRIV-001",
    "DEC-SEC-001",
    "DEC-OFFLINE-001",
    "DEC-LIFE-001",
    "DEC-REL-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-GATE-001",
    "DEC-AI-001",
    "DEC-COMP-001",
    "DEC-HW-001"
  ],
  "requirement_ids": [],
  "related_requirement_ids": [
    "REQ-PROFILE-SOV-001",
    "REQ-PROFILE-SOV-002",
    "REQ-PROFILE-SOV-003",
    "REQ-PROFILE-SOV-004",
    "REQ-PROFILE-SOV-005",
    "REQ-PROFILE-SOV-006",
    "REQ-PROFILE-SOV-007",
    "REQ-PROFILE-SOV-008",
    "REQ-PROFILE-SOV-009",
    "REQ-PROFILE-SOV-010",
    "REQ-PROFILE-SOV-011",
    "REQ-PROFILE-SOV-012",
    "REQ-PROFILE-SOV-013",
    "REQ-PROFILE-SOV-014",
    "REQ-PROFILE-SOV-015",
    "REQ-PROFILE-SOV-016",
    "REQ-PROFILE-SOV-017",
    "REQ-PROFILE-SOV-018",
    "REQ-PROFILE-SOV-019",
    "REQ-PROFILE-SOV-020",
    "REQ-PROFILE-SOV-021",
    "REQ-PROFILE-SOV-022",
    "REQ-PROFILE-SOV-023",
    "REQ-PROFILE-SOV-024",
    "REQ-PROFILE-SOV-025",
    "REQ-PROFILE-SOV-026",
    "REQ-PROFILE-SOV-027",
    "REQ-PROFILE-SOV-028",
    "REQ-PROFILE-SOV-029",
    "REQ-PROFILE-SOV-030",
    "REQ-PROFILE-SOV-031",
    "REQ-PROFILE-SOV-032",
    "REQ-OPS-RESOURCE-005",
    "REQ-OPS-RESOURCE-011",
    "REQ-OPS-RESOURCE-013",
    "REQ-OPS-RESOURCE-015",
    "REQ-OPS-RESOURCE-017",
    "REQ-OPS-RESOURCE-019",
    "REQ-OPS-RESOURCE-020",
    "REQ-OPS-RESOURCE-022",
    "REQ-OPS-RESOURCE-023",
    "REQ-OPS-RESOURCE-025",
    "REQ-OPS-RESOURCE-026",
    "REQ-OPS-RESOURCE-027",
    "REQ-OPS-RESOURCE-029",
    "REQ-OPS-RESOURCE-030",
    "REQ-OPS-RESOURCE-031",
    "REQ-OPS-RESOURCE-032"
  ],
  "lock_ids": [
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SEC-001",
    "LOCK-SEC-002",
    "LOCK-OFFLINE-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-REL-001",
    "LOCK-REL-002",
    "LOCK-PORT-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-PROFILE-007",
    "DOC-OPS-004",
    "DOC-OPS-014",
    "DOC-OPS-018",
    "DOC-LIFE-004",
    "DOC-LIFE-006",
    "DOC-LIFE-013",
    "DOC-SEC-005",
    "DOC-SEC-006",
    "DOC-SEC-007",
    "DOC-SEC-008",
    "DOC-SEC-009",
    "DOC-ADR-005",
    "DOC-ADR-012",
    "DOC-ADR-019"
  ],
  "tags": [
    "recipe",
    "sovereign-linux",
    "quadlet",
    "rootless-podman",
    "systemd-user",
    "service-identities",
    "networks",
    "volumes",
    "secrets",
    "resource-limits",
    "release-activation",
    "offline",
    "recovery",
    "single-node"
  ]
}
KOA:DOC-META:END -->

# Sovereign Linux Quadlet Layout

> **Non-normative recipe.** This document shows one profile-scoped implementation approach. The sovereign Linux profile permits rootless Podman and Quadlet but does not require Quadlet. The active profile manifest, component contracts, Release Set, resource envelope, security contracts, and lifecycle authority control the deployed result.

## 1. Purpose

This recipe demonstrates a rootless Podman and systemd Quadlet layout for application services on one `sovereign_linux_node`.

The layout aims to provide:

- one explicit service identity;
- rootless container execution;
- systemd user supervision;
- one file per network, volume, container, or optional pod;
- read-only container root filesystems;
- explicit writable state paths;
- closed-by-default networking;
- scoped secret references;
- bounded CPU, memory, process, I/O, and temporary storage;
- deterministic startup and shutdown ordering;
- release-specific unit sets;
- separate staging and activation;
- offline startup from locally available validated images;
- observable health and failure;
- clean rollback and recovery.

Quadlet translates declarative files into systemd units. It does not become product authority. Canonical component, artifact, profile, and lifecycle contracts still define what each service can do.

## 2. Scope and Non-Normative Status

This recipe targets:

- a single `sovereign_linux_node`;
- a maintained Linux host;
- a verified immutable system image;
- rootless Podman;
- a dedicated non-interactive service account;
- systemd user services;
- services supplied through a compatible services release;
- local startup without Internet access;
- application services that do not require host privilege.

It does not define:

- a global Podman or Quadlet requirement;
- Kubernetes deployment;
- privileged containers;
- host package installation;
- the canonical component inventory;
- image build, signing, or provenance;
- business authorization;
- data ownership;
- publication authority;
- service-update authority;
- host-network policy;
- secret generation;
- system-image activation;
- an appliance-shell requirement.

The active sovereign Linux profile currently records:

`text
containers required: false
containers permitted: true
preferred runtime when used: Podman
preferred mode: rootless
Quadlet permitted: true
Quadlet required: false
privileged application containers: not permitted
host network mode by default: not permitted
read-only root filesystem: preferred
`

A deployment that adopts this recipe records exact versions, service-account boundaries, paths, units, networks, storage, secrets, resource limits, tests, and rollback behavior in its profile manifest or deployment contract.

## 3. Canonical References

| Source | Role |
| --- | --- |
| `contracts/profiles/sovereign-linux-node.profile.json` | Profile authority, privilege, network, offline, recovery, and conformance |
| `generated/component-catalog.json` | Component identities and ownership |
| `generated/component-catalog.json` | Component interfaces, health, dependencies, data, backup, restore, and failure |
| `contracts/components/resource-governor.component.json` | Resource admission and effective limits |
| `contracts/components/governance-policy-runtime.component.json` | Governed authorization kept separate from capacity |
| `contracts/components/koa-node-agent.component.json` | Narrow host operations and node lifecycle |
| `contracts/release-channels.contract.json` | System, services, governance, and knowledge identities |
| `contracts/artifact-classes.contract.json` | Artifact validation, activation, rollback, and retention |
| `contracts/examples/resource-envelope.example.json` | Example classes, workers, queues, pressure modes, and limits |
| `03-profiles/07-sovereign-linux-node.md` | Profile explanation |
| `06-lifecycle/04-release-sets.md` | Complete four-channel compatibility |
| `06-lifecycle/06-service-updates.md` | Service staging and update operations |
| `06-lifecycle/13-activation-and-verification.md` | Atomic activation and last-known-good rollback |
| `07-security/05-privilege-boundaries.md` | Application and host-privilege separation |
| `07-security/06-privileged-broker.md` | Narrow privileged operation path |
| `07-security/07-secrets-and-keys.md` | Secret references, rotation, and revocation |
| `07-security/08-network-boundaries.md` | Closed-by-default and segmented networking |
| `07-security/09-storage-boundaries.md` | Authoritative state, cache, temporary data, backup, and recovery |
| `08-operations/04-resource-envelopes.md` | Declared, observed, and effective resource limits |
| `08-operations/14-maintenance.md` | Controlled service maintenance |
| `08-operations/18-sovereign-node-operations.md` | Sovereign-node operating procedures |
| `10-adrs/ADR-005-rootless-podman-and-quadlet.md` | Profile-scoped rootless container choice |
| `10-adrs/ADR-012-single-narrow-privileged-broker.md` | No general application host privilege |
| `10-adrs/ADR-019-resource-governor-and-policy-runtime-separation.md` | Capacity and governance separation |

Image identity, service identity, Release Set identity, policy approval, and Resource Governor admission remain separate.

## 4. Layout Model

### 4.1 Dedicated service account

Use a dedicated non-login account for the rootless application-service boundary.

Illustrative identity:

`text
account: koa-runtime
home: /var/lib/koa/runtime
runtime root: /run/user/<uid>
Quadlet source: /var/lib/koa/runtime/.config/containers/systemd
container storage: profile-managed rootless Podman storage
`

The account does not receive an interactive password, sudo access, a general login shell, unrelated component data, unrestricted host mounts, arbitrary devices, or privileged containers.

Enabling a persistent user manager at boot is a host operation. Perform it through the deployment's approved image-build or narrow broker path, not from an application container.

### 4.2 Recommended directory tree

`text
/var/lib/koa/
├── runtime/
│ ├── .config/
│ │ └── containers/
│ │ └── systemd/
│ │ ├── active/
│ │ ├── koa-internal.network
│ │ ├── koa-publication.network
│ │ └── koa-cache.volume
│ ├── config/
│ │ ├── common.env
│ │ └── components/
│ ├── releases/
│ │ └── services-<release-id>/
│ │ ├── units/
│ │ ├── inventory.json
│ │ └── validation/
│ └── state/
│ ├── activation/
│ └── sockets/
├── data/
│ ├── orgo/
│ ├── konnaxion/
│ ├── kristal/
│ ├── mediatheque/
│ ├── uckk-import-quarantine/
│ └── receipts/
├── cache/
│ ├── previews/
│ ├── indexes/
│ └── image-layers/
├── backup-staging/
└── recovery/
`

This is an example path layout. The active deployment manifest can choose different locations.

### 4.3 Release-specific unit sets

Keep every validated services release in a separate directory:

`text
/var/lib/koa/runtime/releases/services-2026.08.03-1/units/
`

An illustrative set can contain:

`text
koa-internal.network
koa-publication.network
koa-cache.volume
koa-identity.container
koa-resource-governor.container
koa-governance-policy-runtime.container
koa-audit-broker.container
koa-ariane.container
koa-orgo.container
koa-konnaxion.container
koa-kristal.container
koa-mediatheque.container
koa-uckk-import-bridge.container
koa-uckk-publication-bridge.container
koa-publication-gateway.container
`

The actual set comes from the active profile and component registry.

### 4.4 Active projection

One implementation can keep current files in:

`text
/var/lib/koa/runtime/.config/containers/systemd/active/
`

Each file links to the selected validated release:

`text
active/koa-orgo.container
 -> /var/lib/koa/runtime/releases/services-2026.08.03-1/units/koa-orgo.container
`

Validate that the deployed Quadlet generator reads the selected subdirectory and link arrangement. Another deployment can atomically replace a complete unit set in the rootless Quadlet search path.

### 4.5 Naming

Use deterministic names:

`text
koa-<component>.container
koa-<network-purpose>.network
koa-<storage-purpose>.volume
koa-<lifecycle-group>.pod
`

Generated services normally appear as:

`text
koa-<component>.service
`

Keep component names aligned with canonical IDs.

### 4.6 Component boundary

Prefer one primary container per component runtime. This keeps identity, health, resources, logs, networks, storage, lifecycle, and failure isolation visible.

Use a pod or sidecar only when the component contract declares a shared lifecycle and the shared namespaces do not weaken ownership or isolation.

### 4.7 Mutable and release-controlled state

Release-controlled material includes unit files, image identities, environment-key names, networks, mount declarations, health commands, resources, and dependency ordering.

Mutable owner-controlled state includes authoritative data, receipt buffers, selected caches, runtime sockets, temporary files, and rotation-managed secret material.

Unit files never embed authoritative application data.

## 5. Prepare the Rootless Boundary

### 5.1 Create the service identity

Illustrative host preparation:

`bash
useradd \
 --system \
 --create-home \
 --home-dir /var/lib/koa/runtime \
 --shell /usr/sbin/nologin \
 koa-runtime
`

This is a host mutation example. Application components do not execute it.

The deployment assigns subordinate user and group ID ranges required by rootless Podman.

Inspect:

`bash
getent passwd koa-runtime
grep '^koa-runtime:' /etc/subuid /etc/subgid
`

### 5.2 Enable the user manager

Illustrative preparation:

`bash
loginctl enable-linger koa-runtime
`

Verify:

`bash
loginctl show-user koa-runtime \
 --property=Linger \
 --property=RuntimePath \
 --property=State
`

The approved host path records this operation.

### 5.3 Create directories

`bash
install -d -o koa-runtime -g koa-runtime -m 0700 \
 /var/lib/koa/runtime/.config/containers/systemd \
 /var/lib/koa/runtime/config \
 /var/lib/koa/runtime/releases \
 /var/lib/koa/runtime/state

install -d -o koa-runtime -g koa-runtime -m 0750 \
 /var/lib/koa/data \
 /var/lib/koa/cache \
 /var/lib/koa/backup-staging \
 /var/lib/koa/recovery
`

Create component data directories according to each owner contract. A shared parent directory does not create shared data ownership.

### 5.4 Confirm rootless Podman

`bash
sudo -u koa-runtime \
 env HOME=/var/lib/koa/runtime \
 podman info \
 --format 'rootless={{.Host.Security.Rootless}} cgroup={{.Host.CgroupsVersion}}'
`

The deployed privileged model can use a controlled service action instead of operator `sudo`.

### 5.5 Confirm the systemd user manager

`bash
uid="$(id -u koa-runtime)"
runtime_dir="/run/user/${uid}"

sudo -u koa-runtime \
 env \
 HOME=/var/lib/koa/runtime \
 XDG_RUNTIME_DIR="$runtime_dir" \
 DBUS_SESSION_BUS_ADDRESS="unix:path=${runtime_dir}/bus" \
 systemctl --user is-system-running
`

A missing user manager is a preparation failure, not a reason to run application containers as root.

### 5.6 Stage a release

`bash
release_id=services-2026.08.03-1
release_root="/var/lib/koa/runtime/releases/${release_id}"

install -d -o koa-runtime -g koa-runtime -m 0750 \
 "${release_root}/units" \
 "${release_root}/validation"
`

Place only files listed by the validated services-release inventory in the directory. Staging does not start or reload services.

## 6. Quadlet Unit Patterns

### 6.1 Internal network

`koa-internal.network`:

`ini
[Unit]
Description=kOA internal component network

[Network]
NetworkName=koa-internal
Driver=bridge
Internal=true
IPv6=false
Label=koa.network-purpose=internal
Label=koa.profile=sovereign_linux_node
`

Components needing external access use a separate declared path rather than weakening this network.

### 6.2 Publication network

`koa-publication.network`:

`ini
[Unit]
Description=kOA governed publication network

[Network]
NetworkName=koa-publication
Driver=bridge
Internal=false
IPv6=false
Label=koa.network-purpose=publication
Label=koa.profile=sovereign_linux_node
`

The network does not authorize egress. Firewall, destination, protocol, identity, policy, and integration controls still apply.

### 6.3 Reproducible cache volume

`koa-cache.volume`:

`ini
[Unit]
Description=kOA reproducible cache volume

[Volume]
VolumeName=koa-cache
Label=koa.storage-class=reproducible-cache
Label=koa.profile=sovereign_linux_node
`

Use named volumes for reproducible data when owner and retention contracts permit them. Explicit bind paths are clearer for authoritative data.

### 6.4 Ordinary internal component

`koa-orgo.container`:

`ini
[Unit]
Description=kOA Orgo component
Requires=koa-internal-network.service
After=koa-internal-network.service
Wants=koa-resource-governor.service
After=koa-resource-governor.service

[Container]
ContainerName=koa-orgo
Image=localhost/koa/orgo:services-2026.08.03-1
Network=koa-internal.network
ReadOnly=true
NoNewPrivileges=true
DropCapability=all
UserNS=keep-id
Volume=/var/lib/koa/data/orgo:/var/lib/koa/data:Z
Tmpfs=/tmp:rw,size=256m,mode=1777
EnvironmentFile=/var/lib/koa/runtime/config/common.env
EnvironmentFile=/var/lib/koa/runtime/config/components/orgo.env
Label=koa.component=orgo
Label=koa.release=services-2026.08.03-1
Label=koa.resource-class=service
HealthCmd=/usr/local/bin/koa-health --component orgo
HealthInterval=30s
HealthTimeout=5s
HealthRetries=3
Notify=healthy

[Service]
Restart=on-failure
RestartSec=5s
TimeoutStartSec=90s
TimeoutStopSec=45s
KillMode=mixed
LimitNOFILE=8192
TasksMax=512
MemoryHigh=2G
MemoryMax=3G
CPUQuota=150%
CPUWeight=200
IOWeight=200

[Install]
WantedBy=default.target
`

The values are illustrative. The active resource envelope supplies actual limits.

### 6.5 Governed outbound component

`koa-publication-gateway.container`:

`ini
[Unit]
Description=kOA Publication Gateway
Requires=koa-internal-network.service
Requires=koa-publication-network.service
After=koa-internal-network.service
After=koa-publication-network.service
Wants=koa-governance-policy-runtime.service
After=koa-governance-policy-runtime.service

[Container]
ContainerName=koa-publication-gateway
Image=localhost/koa/publication-gateway:services-2026.08.03-1
Network=koa-internal.network
Network=koa-publication.network
ReadOnly=true
NoNewPrivileges=true
DropCapability=all
UserNS=keep-id
Tmpfs=/tmp:rw,size=128m,mode=1777
EnvironmentFile=/var/lib/koa/runtime/config/common.env
EnvironmentFile=/var/lib/koa/runtime/config/components/publication-gateway.env
Secret=koa-publication-credential,type=mount,target=/run/secrets/publication-credential
Label=koa.component=publication-gateway
Label=koa.release=services-2026.08.03-1
Label=koa.resource-class=service
HealthCmd=/usr/local/bin/koa-health --component publication-gateway
HealthInterval=30s
HealthTimeout=5s
HealthRetries=3
Notify=healthy

[Service]
Restart=on-failure
RestartSec=10s
TimeoutStartSec=90s
TimeoutStopSec=60s
TasksMax=256
MemoryHigh=1G
MemoryMax=2G
CPUQuota=100%
CPUWeight=200
IOWeight=150

[Install]
WantedBy=default.target
`

The secret name is a reference. Provision its value through the approved secret lifecycle.

### 6.6 Critical authority service

`koa-resource-governor.container`:

`ini
[Unit]
Description=kOA Resource Governor
Requires=koa-internal-network.service
After=koa-internal-network.service
Before=koa-orgo.service
Before=koa-konnaxion.service
Before=koa-mediatheque.service
Before=koa-uckk-import-bridge.service
Before=koa-uckk-publication-bridge.service

[Container]
ContainerName=koa-resource-governor
Image=localhost/koa/resource-governor:services-2026.08.03-1
Network=koa-internal.network
ReadOnly=true
NoNewPrivileges=true
DropCapability=all
UserNS=keep-id
Volume=/var/lib/koa/data/resource-governor:/var/lib/koa/data:Z
Tmpfs=/tmp:rw,size=64m,mode=1777
EnvironmentFile=/var/lib/koa/runtime/config/common.env
EnvironmentFile=/var/lib/koa/runtime/config/components/resource-governor.env
Label=koa.component=resource-governor
Label=koa.release=services-2026.08.03-1
Label=koa.resource-class=critical_service
HealthCmd=/usr/local/bin/koa-health --component resource-governor
HealthInterval=15s
HealthTimeout=3s
HealthRetries=2
Notify=healthy

[Service]
Restart=always
RestartSec=2s
TimeoutStartSec=60s
TimeoutStopSec=30s
TasksMax=256
MemoryHigh=768M
MemoryMax=1G
CPUQuota=75%
CPUWeight=900
IOWeight=900

[Install]
WantedBy=default.target
`

Containerizing Resource Governor does not grant it arbitrary host control. Host operations remain behind the profile-approved privileged boundary.

### 6.7 Local sockets

Bind only a declared socket directory:

`ini
Volume=/var/lib/koa/runtime/state/sockets/resource-governor:/run/koa/resource-governor:Z
`

Do not mount the entire Podman socket, host `/run`, or the host filesystem for convenience.

### 6.8 Optional pod

`koa-component-group.pod`:

`ini
[Unit]
Description=kOA example tightly coupled component group

[Pod]
PodName=koa-component-group
Network=koa-internal.network
Label=koa.lifecycle-group=example
`

Avoid grouping unrelated components. Shared network, IPC, process, or lifecycle namespaces can weaken isolation.

## 7. Network, Storage, Secrets, and Resources

### 7.1 Network split

A practical logical split is:

`text
koa-internal
 component traffic only

koa-publication
 Publication Gateway and declared external adapters

host management path
 Node Agent and narrow privileged broker

local sockets
 selected local-only component interfaces
`

Avoid `Network=host` by default.

### 7.2 Port publishing

For a local interface:

`ini
PublishPort=127.0.0.1:8080:8080
`

A management or public interface uses the exact declared address, protocol, port, identity, policy, and firewall rule.

### 7.3 Authoritative data

Use one path per owner:

`text
/var/lib/koa/data/orgo
/var/lib/koa/data/konnaxion
/var/lib/koa/data/kristal
/var/lib/koa/data/mediatheque
/var/lib/koa/data/uckk-import-quarantine
`

A container receives only its own authoritative path. Shared read-only reference artifacts use a separate declared path. Cross-component mutation uses contracts, not shared writable volumes.

### 7.3.1 Directional UCKK bridge storage

`koa-mediatheque.container` receives the authoritative local Mediatheque path. The UCKK Publication Bridge receives only outbound staging and receipt paths. The UCKK Import Bridge receives only inbound quarantine, validation, and receipt paths until the kOA Mediatheque accepts a package through its declared interface.

Neither bridge mounts the Mediatheque authoritative path as writable. No Quadlet unit represents a local UCKK database or a generic bidirectional synchronization daemon.

### 7.4 Reproducible caches

Use distinct cache paths and record owner plus rebuild behavior:

`text
/var/lib/koa/cache/previews
/var/lib/koa/cache/indexes
/var/lib/koa/cache/image-layers
`

Under pressure, Resource Governor can request owner-controlled pruning. It does not delete another component's data directly.

### 7.5 Temporary storage

Use bounded `Tmpfs=` entries. Larger jobs use job-specific staging with owner, job identity, size bound, cleanup, failure evidence, and no authoritative-source status.

Avoid unbounded writes to the container layer.

### 7.6 Secrets

Keep secret values out of unit and environment files.

Reference a provisioned secret:

`ini
Secret=koa-component-token,type=mount,target=/run/secrets/component-token
`

Do not put secret values in:

- `Environment=`;
- image layers;
- command arguments;
- labels;
- health output;
- logs;
- unit files;
- Release Set manifests.

### 7.7 Non-secret environment

Example `common.env`:

`bash
KOA_PROFILE_ID=sovereign_linux_node
KOA_RELEASE_SET_ID=release-set-2026.08.03-1
KOA_LOG_FORMAT=json
KOA_OFFLINE_MODE=auto
`

Component files add non-secret component-specific configuration.

### 7.8 Resource controls

Useful service and container controls include:

`ini
CPUQuota=
CPUWeight=
MemoryHigh=
MemoryMax=
IOWeight=
TasksMax=
LimitNOFILE=
Tmpfs=
PidsLimit=
`

Supported keys vary by the deployed versions. Inspect generated units and runtime state instead of assuming every property applied.

Actual values come from the active resource envelope.

### 7.9 Pressure ordering

Classify services as `critical_service`, `service`, `background`, or `heavy_compute`.

Under pressure, pause optional integrations, synchronization, derivatives, indexing, and media conversion before identity, governance, Resource Governor, Audit Broker, authoritative stores, local Ariane functions, receipts, and recovery.

## 8. Dependencies, Activation, Updates, and Recovery

### 8.1 Dependency meaning

Use systemd dependencies for technical startup order only.

They do not grant data ownership, policy authorization, resource admission, publication authority, or host privilege.

Use `Wants=` for optional dependencies and `Requires=` only when safe operation is impossible without the dependency.

Avoid broad `network-online.target` ordering when a service needs only a local Quadlet network.

### 8.2 Health and semantic readiness

Container health covers local process health.

Component readiness additionally checks schema state, Release Set compatibility, policy, trust, receipt buffering, local dependencies, migrations, and recovery blocks.

A healthy process can remain semantically unready.

### 8.3 Staging procedure

For a new services release:

1. import validated OCI artifacts;
2. verify the services-release inventory;
3. verify complete Release Set compatibility;
4. stage release-specific Quadlet files;
5. validate syntax and generated units;
6. validate local image availability;
7. validate networks, mounts, secrets, resources, and dependencies;
8. run inactive or isolated checks;
9. preserve the current active unit set;
10. record staging evidence.

Staging does not change active authority.

### 8.4 Activation procedure

Illustrative operator sequence:

`bash
systemctl --user daemon-reload
systemctl --user start koa-resource-governor.service
systemctl --user start koa-governance-policy-runtime.service
systemctl --user start koa-audit-broker.service
systemctl --user start koa-orgo.service koa-konnaxion.service koa-kristal.service
`

The real order comes from generated dependencies and lifecycle contracts.

Activation selects the validated unit set, reloads the user manager, transitions affected services, validates semantic health, confirms the complete Release Set, and records the active identity and receipts.

### 8.5 No automatic registry activation

Do not use `AutoUpdate=registry` as a substitute for services-release activation.

Timer-driven pulls cannot change running product state outside the Release Set lifecycle.

Prefetching validated images is separate from selection and activation.

### 8.6 Restart behavior

Use `Restart=on-failure` for ordinary services unless the component contract defines another model.

Use `Restart=always` only for continuously resident critical services with bounded and observable failure loops.

Example:

`ini
[Unit]
StartLimitIntervalSec=300
StartLimitBurst=5

[Service]
Restart=on-failure
RestartSec=10s
`

### 8.7 Offline startup

Offline startup uses locally available images, units, profile state, trust and revocation, policy bundles, knowledge artifacts, secrets, local networks, authoritative data, and receipt buffers.

A missing optional remote integration disables only that integration.

Ordinary offline boot does not pull from a registry.

### 8.8 Rollback

Rollback selects a complete previous services release compatible with the current system, governance, and knowledge releases.

Validate images, units, schemas, component data compatibility, secrets, networks, resources, recovery, and the complete Release Set.

Do not copy one old unit into a new active release.

### 8.9 Recovery

Recovery can use a last-known-good services release, recovery runtime pack, verified offline bundle, component-owned restore, or restricted service set.

The rootless service account remains separate from the privileged recovery path.

## 9. Validation and Observability

### 9.1 Validate generation

Run as the service account:

`bash
uid="$(id -u koa-runtime)"
runtime_dir="/run/user/${uid}"

sudo -u koa-runtime \
 env \
 HOME=/var/lib/koa/runtime \
 XDG_RUNTIME_DIR="$runtime_dir" \
 DBUS_SESSION_BUS_ADDRESS="unix:path=${runtime_dir}/bus" \
 /usr/lib/systemd/system-generators/podman-system-generator \
 --user \
 /tmp/koa-quadlet-output \
 /tmp/koa-quadlet-early \
 /tmp/koa-quadlet-late
`

The generator path differs across distributions. Record the deployed path in the profile manifest or package inventory.

### 9.2 Inspect generated units

`bash
systemctl --user cat koa-orgo.service
systemctl --user show koa-orgo.service \
 --property=CPUQuotaPerSecUSec \
 --property=CPUWeight \
 --property=MemoryHigh \
 --property=MemoryMax \
 --property=TasksMax \
 --property=IOWeight \
 --property=Restart \
 --property=After \
 --property=Requires \
 --property=Wants
`

Confirm requested limits and ordering.

### 9.3 Inspect isolation

`bash
podman inspect koa-orgo
podman top koa-orgo user pid hpid pcpu pmem comm
podman stats --no-stream koa-orgo
podman network inspect koa-internal
`

Check rootless execution, expected image, no privilege, no host network, dropped capabilities, read-only root, expected mounts, expected networks, labels, and limits.

### 9.4 Inspect storage

`bash
podman inspect koa-orgo --format '{{json .Mounts}}'
findmnt /var/lib/koa/data/orgo
stat -c '%U %G %a %n' /var/lib/koa/data/orgo
`

The service receives only declared writable paths.

### 9.5 Inspect secret references

`bash
podman secret ls
podman exec koa-publication-gateway \
 test -r /run/secrets/publication-credential
`

Do not print the secret.

Check absence from environment and labels:

`bash
podman inspect koa-publication-gateway \
 --format '{{json .Config.Env}}'

podman inspect koa-publication-gateway \
 --format '{{json .Config.Labels}}'
`

### 9.6 Test offline behavior

In a controlled test, block external access and confirm:

- local services start from local images;
- internal networks operate;
- policy and knowledge artifacts load;
- receipts buffer locally;
- optional remote adapters degrade as declared;
- no undeclared pull or provider substitution occurs.

### 9.7 Observe services

`bash
systemctl --user list-units 'koa-*.service'
systemctl --user --failed
podman ps --format 'table {{.Names}}\t{{.Status}}\t{{.Networks}}'
journalctl --user -u koa-orgo.service --since -30min
`

Logs exclude secrets and governed payloads.

### 9.8 Validation checklist

| Check | Expected result |
| --- | --- |
| Service identity | Dedicated non-login rootless account |
| Quadlet adoption | Explicit in deployment, not inferred from profile |
| Active unit set | One validated services release |
| Image inventory | Matches services release and Release Set |
| Privilege | Rootless and non-privileged |
| Host network | Absent unless explicitly authorized |
| Capabilities | Dropped to declared minimum |
| Root filesystem | Read-only where component permits |
| Writable mounts | Explicit and owner-scoped |
| Secrets | Absent from unit, image, environment, labels, and logs |
| Networks | Internal, publication, and management paths separated |
| Resources | Match active envelope |
| Health | Process and semantic readiness pass |
| Offline | Starts without remote registry access |
| Update | Staging separate from activation |
| Automatic update | Does not bypass Release Set |
| Rollback | Complete compatible services unit |
| Recovery | Preserves evidence and privilege separation |

### 9.9 Suggested evidence

`json
{
 "evidence_id": "evidence.sovereign-node.quadlet.services-2026.08.03-1",
 "profile_id": "sovereign_linux_node",
 "service_release_id": "services-2026.08.03-1",
 "runtime": "rootless_podman",
 "supervision": "systemd_user_quadlet",
 "checks": [
 "service_identity_valid",
 "quadlet_generation_valid",
 "images_available_locally",
 "rootless_isolation_valid",
 "network_boundaries_valid",
 "storage_ownership_valid",
 "secret_references_valid",
 "resource_limits_valid",
 "offline_start_valid",
 "rollback_candidate_valid"
 ],
 "result": "pass"
}
`

This supports an implementation result but does not create a profile conformance claim.

## 10. Failure Handling, Cleanup, and Prohibited Assumptions

### 10.1 Failure table

| Condition | Response |
| --- | --- |
| User manager unavailable | Keep application services inactive and repair the service boundary |
| Quadlet generation fails | Reject the candidate and retain the active release |
| Image unavailable locally | Block offline activation; do not pull an undeclared substitute |
| Image or release mismatch | Reject activation |
| Required secret unavailable | Fail only the dependent service or governed capability |
| Network unit fails | Keep dependent services stopped |
| Authoritative mount missing | Keep the owner component stopped; do not create an empty replacement silently |
| Resource control unsupported | Record it and reject a claim requiring that control |
| Process health fails | Keep the service unready and invoke restart, rollback, or repair |
| Semantic readiness fails | Do not report health from process state alone |
| Receipt buffer unavailable | Block critical transitions requiring durable evidence |
| Storage pressure | Stop growth and background work before authoritative data and recovery |
| Restart loop | Stop the unit, preserve evidence, and enter repair |
| Partial candidate activation | Restore the previous complete compatible services release |
| Rollback candidate incompatible | Use forward repair or recovery |

### 10.2 Cleanup

Stop a component:

`bash
systemctl --user stop koa-orgo.service
`

Inspect and remove an obsolete container instance after lifecycle closure:

`bash
podman ps --all --filter name=koa-
podman rm koa-orgo
`

Container removal does not delete authoritative data.

Inspect volumes before owner-controlled removal:

`bash
podman volume ls
podman volume inspect koa-cache
`

### 10.3 Release retention

Retain the active release, a validated last-known-good release, recovery-required releases, and evidence required by retention contracts.

Remove older staged releases only after they are inactive, not rollback-eligible, not required by recovery, and cleared by owner retention.

### 10.4 Prohibited assumptions

Do not assume that:

- sovereign Linux requires Quadlet globally;
- a file in the Quadlet directory is authorized;
- `daemon-reload` activates a Release Set;
- a running container proves semantic readiness;
- a valid image proves release compatibility;
- labels create canonical identity;
- rootless execution removes all risk;
- `NoNewPrivileges=true` replaces network, storage, secret, and capability controls;
- a read-only root protects writable mounts;
- several components can share one writable authoritative volume;
- a shared network creates ownership;
- systemd ordering grants business authorization;
- resource admission grants governance authority;
- governance approval creates capacity;
- the Podman socket is a general integration interface;
- host network mode is acceptable for convenience;
- automatic registry updates equal lifecycle activation;
- Internet access is required for ordinary boot;
- remote failure permits provider substitution;
- a privileged container can replace the narrow broker;
- the service account can mutate the host;
- manual unit edits form a valid services release;
- example values are profile requirements;
- repeated use makes this recipe authoritative.

### 10.5 Adoption record

A deployment adopting this layout records:

- Podman, systemd, and Quadlet generator versions;
- service-account identity and subordinate ID ranges;
- Quadlet search path;
- release staging and activation paths;
- component unit inventory;
- networks;
- storage;
- secret references;
- resource limits;
- health and readiness;
- offline test;
- rollback candidate;
- recovery procedure;
- evidence.

The deployment or profile contract owns the adopted values.

## 11. Worked Examples

### Example 1 — Internal-only component

Orgo runs under `koa-runtime`, joins only `koa-internal`, mounts only its own data, has a read-only root, receives bounded resources, and exposes no host port.

### Example 2 — Publication Gateway

Publication Gateway joins internal and publication networks and receives a mounted secret reference. Host egress, governance approval, and network availability remain separate.

### Example 3 — Offline restart

The node reboots without Internet access. The systemd user manager starts the selected validated unit set from local images, receipts buffer locally, and remote adapters degrade explicitly.

### Example 4 — Failed candidate generation

A candidate release contains an unsupported Quadlet key. Generation fails during staging, the active release remains unchanged, and evidence identifies the file and generator version.

### Example 5 — Storage pressure

Preview and index caches approach the free-space floor. Background services stop, owners prune reproducible caches, and authoritative data, Release Set state, receipts, evidence, and recovery remain protected.

### Example 6 — Secret rotation

A publication credential rotates. The owner provisions the replacement, the dependent service restarts through maintenance, the old credential is revoked, and the stable unit reference remains unchanged.

### Example 7 — Services rollback

A new Orgo image passes process health but fails schema readiness. Lifecycle restores the complete previous services release instead of copying only the old Orgo unit.

### Example 8 — Alternative supervisor

Another sovereign Linux deployment uses a different rootless single-node supervisor. It can conform when it preserves identities, privilege, networks, storage, secrets, resources, lifecycle, offline operation, rollback, recovery, and evidence.
