<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "RECIPE-SOV-LINUX-001",
  "document_class": "non_normative_recipe",
  "status": "active",
  "language": "en",
  "layer": "recipes",
  "scope": [
    "sovereign_linux_node"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/capability_model",
    "contracts/system.contract.json#/operations_model",
    "generated/component-catalog.json",
    "contracts/components/koa-node-agent.component.json",
    "contracts/profiles/sovereign-linux-node.profile.json",
    "contracts/profiles/sovereign-offline.profile.json",
    "contracts/profiles/high-assurance.profile.json",
    "generated/profile-catalog.json",
    "contracts/artifact-classes.contract.json",
    "contracts/release-channels.contract.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json",
    "contracts/integrations/uckk-import.integration.json",
    "contracts/artifact-contracts/uckk-learning-package.schema.json",
    "contracts/artifact-contracts/uckk-import-receipt.schema.json"
  ],
  "decision_ids": [
    "DEC-PROFILE-SOV-LINUX-001",
    "DEC-SYS-COMP-001",
    "DEC-SYS-RESOURCE-001",
    "DEC-SYS-AUDIT-001",
    "DEC-SYS-OFFLINE-001",
    "DEC-LIFE-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-COMP-BOUNDARY-001",
    "REQ-COMP-BOUNDARY-002",
    "REQ-SEC-BROKER-001",
    "REQ-SEC-BROKER-002",
    "REQ-SEC-BROKER-003",
    "REQ-SEC-BROKER-004",
    "REQ-SEC-BROKER-005",
    "REQ-SEC-BROKER-006",
    "REQ-SEC-BROKER-008",
    "REQ-SEC-BROKER-009",
    "REQ-SEC-BROKER-013",
    "REQ-SEC-BROKER-016",
    "REQ-SEC-BROKER-020",
    "REQ-SEC-BROKER-025",
    "REQ-SEC-BROKER-026",
    "REQ-SEC-BROKER-027",
    "REQ-SEC-BROKER-028",
    "REQ-SEC-BROKER-029",
    "REQ-SEC-BROKER-036",
    "REQ-OPS-SLO-003",
    "REQ-OPS-SLO-008",
    "REQ-OPS-SLO-021",
    "REQ-OPS-SLO-036",
    "REQ-OPS-DR-017",
    "REQ-OPS-DR-019",
    "REQ-OPS-DR-021",
    "REQ-OPS-DR-028",
    "REQ-OPS-DR-034",
    "REQ-OPS-DR-036",
    "REQ-CONF-GATE-036"
  ],
  "lock_ids": [
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
    "LOCK-OPS-001",
    "LOCK-OPS-002",
    "LOCK-OPS-003",
    "LOCK-OPS-004",
    "LOCK-AI-001",
    "LOCK-AI-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-PROFILE-001",
    "DOC-PROFILE-002",
    "DOC-PROFILE-012",
    "DOC-SYS-005",
    "DOC-SYS-006",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-010",
    "DOC-SYS-011",
    "DOC-SYS-012",
    "DOC-COMP-001",
    "DOC-LIFE-003",
    "DOC-LIFE-013",
    "DOC-SEC-005",
    "DOC-SEC-006",
    "DOC-OPS-003",
    "DOC-OPS-013",
    "DOC-CONF-003",
    "DOC-CONF-019"
  ],
  "tags": [
    "recipe",
    "sovereign-linux",
    "systemd",
    "service-layout",
    "targets",
    "sockets",
    "service-identities",
    "hardening",
    "resource-control",
    "offline",
    "recovery"
  ]
}
KOA:DOC-META:END -->

# systemd Layout

## 1. Purpose

This recipe shows one practical systemd layout for a sovereign Linux node.

The layout gives each kOA component:

- a dedicated operating-system identity;
- a narrow unit boundary;
- explicit local dependencies;
- bounded writable paths;
- local sockets instead of public listeners where possible;
- profile-owned resource controls;
- restart and failure behavior;
- observable activation and recovery state;
- compatibility with offline startup;
- a clean relationship to complete Release Set activation.

This recipe is non-normative. Component contracts, profile contracts, Release Set authority, privilege boundaries, Resource Governor decisions, and operations requirements remain authoritative.

systemd manages process lifecycle and local ordering. It does not become an identity authority, policy authority, resource-admission authority, publication authority, data owner, or release-compatibility authority.

The worked layout uses:

```text
koa-node.target
koa-critical.target
koa-core.target
koa-background.target
koa-optional.target
koa-recovery.target
```

The names are examples. A deployment can use different names when the same boundaries and lifecycle are preserved.

## 2. Design Principles

### 2.1 Dedicated identities

Give each long-running component a dedicated account.

Example identities:

```text
koa-identity
koa-policy
koa-resource
koa-audit
koa-publication
koa-ariane
koa-mediatheque
koa-node-agent
```

Do not run unrelated components under one shared account.

A shared group can grant narrowly selected access to one socket or read-only artifact directory. It does not grant broad cross-component filesystem access.

### 2.2 Component-owned state

Each component receives write access only to its own authoritative state and declared runtime paths.

Examples:

```text
/var/lib/koa/identity/
/var/lib/koa/policy/
/var/lib/koa/resource/
/var/lib/koa/audit/
/var/lib/koa/publication/
/var/lib/koa/ariane/
/var/lib/koa/mediatheque/
```

A component reaches another component through a registered API, event, socket, or governed export.

### 2.3 Local sockets by default

Prefer:

```text
/run/koa/<component>/<interface>.sock
```

over loopback TCP when both endpoints live on one node.

A public listener needs a distinct network, authentication, policy, rate, evidence, and lifecycle design.

### 2.4 Targets group lifecycle

Targets express operational groups.

They do not imply shared authority or data access among members.

### 2.5 Resource ownership

systemd cgroup controls can enforce static or generated limits.

Resource Governor owns admission and current allocation decisions.

### 2.6 Complete Release Set activation

Units load files selected by the active Release Set.

They do not independently select the newest package or one newer release channel.

## 3. Filesystem and Identity Layout

### 3.1 Recommended paths

Use a stable hierarchy:

```text
/etc/koa/
  node/
  profile/
  active/
  components/
  integrations/
  secrets.d/

/usr/lib/koa/
  release-sets/
  tools/
  recovery/

/var/lib/koa/
  <component>/
  recovery/

/var/cache/koa/
  <component>/

/run/koa/
  <component>/
  activation/
  recovery/
```

Suggested ownership:

| Path | Owner | Purpose |
| --- | --- | --- |
| `/etc/koa/node/` | root | Node identity references and host-local configuration |
| `/etc/koa/profile/` | root | Active profile projection |
| `/etc/koa/active/` | root | Active Release Set references |
| `/etc/koa/components/<id>/` | root | Component static configuration |
| `/etc/koa/secrets.d/` | root | Managed credential sources or references |
| `/usr/lib/koa/release-sets/` | root | Immutable staged Release Set material |
| `/usr/lib/koa/tools/` | root | Validated operational tools |
| `/var/lib/koa/<id>/` | component account | Component-owned authoritative state |
| `/var/cache/koa/<id>/` | component account | Regenerable cache |
| `/run/koa/<id>/` | component account | Runtime sockets and ephemeral state |
| `/run/koa/activation/` | activation authority | Activation transaction state |
| `/run/koa/recovery/` | recovery authority | Recovery runtime state |

Mutable component state does not live under `/usr/lib/koa/release-sets/`.

### 3.2 sysusers example

Example `/usr/lib/sysusers.d/koa-components.conf`:

```text
u koa-identity    - "kOA Identity and Trust"          /var/lib/koa/identity
u koa-policy      - "kOA Governance Policy Runtime"  /var/lib/koa/policy
u koa-resource    - "kOA Resource Governor"           /var/lib/koa/resource
u koa-audit       - "kOA Audit Broker"                /var/lib/koa/audit
u koa-publication - "kOA Publication Gateway"         /var/lib/koa/publication
u koa-ariane      - "kOA Ariane"                      /var/lib/koa/ariane
u koa-mediatheque - "kOA Mediatheque"                /var/lib/koa/mediatheque
u koa-node-agent  - "kOA Node Agent"                  /var/lib/koa/node-agent
```

Provisioning verifies any existing account before reuse.

### 3.3 tmpfiles example

Example `/usr/lib/tmpfiles.d/koa-components.conf`:

```text
d /var/lib/koa/identity      0750 koa-identity    koa-identity    -
d /var/lib/koa/policy        0750 koa-policy      koa-policy      -
d /var/lib/koa/resource      0750 koa-resource    koa-resource    -
d /var/lib/koa/audit         0750 koa-audit       koa-audit       -
d /var/lib/koa/publication   0750 koa-publication koa-publication -
d /var/lib/koa/ariane        0750 koa-ariane      koa-ariane      -
d /var/lib/koa/mediatheque   0750 koa-mediatheque koa-mediatheque -
d /var/lib/koa/node-agent    0750 koa-node-agent  koa-node-agent  -

d /run/koa                    0755 root            root            -
d /run/koa/identity           0750 koa-identity    koa-identity    -
d /run/koa/policy             0750 koa-policy      koa-policy      -
d /run/koa/resource           0750 koa-resource    koa-resource    -
d /run/koa/audit              0750 koa-audit       koa-audit       -
d /run/koa/publication        0750 koa-publication koa-publication -
d /run/koa/ariane             0750 koa-ariane      koa-ariane      -
d /run/koa/mediatheque        0750 koa-mediatheque koa-mediatheque -
d /run/koa/node-agent         0750 koa-node-agent  koa-node-agent  -
d /run/koa/activation         0750 root            root            -
d /run/koa/recovery           0750 root            root            -
```

Add shared runtime paths only when an interface contract requires them.

## 4. Target Structure and Startup Order

### 4.1 Node target

Example `/usr/lib/systemd/system/koa-node.target`:

```ini
[Unit]
Description=kOA sovereign node
Requires=koa-critical.target
Wants=koa-core.target koa-background.target
After=local-fs.target
Before=multi-user.target
AllowIsolate=yes

[Install]
WantedBy=multi-user.target
```

### 4.2 Critical target

Example `/usr/lib/systemd/system/koa-critical.target`:

```ini
[Unit]
Description=kOA critical authority services
Requires=koa-identity.service
Requires=koa-policy.service
Requires=koa-resource.service
Requires=koa-audit.service
After=local-fs.target
After=systemd-tmpfiles-setup.service
After=koa-release-set-verify.service
Before=koa-core.target
```

### 4.3 Core target

Example `/usr/lib/systemd/system/koa-core.target`:

```ini
[Unit]
Description=kOA core local services
Requires=koa-critical.target
Wants=koa-ariane.service
Wants=koa-mediatheque.service
After=koa-critical.target
```

Ariane local navigation remains available without external AI or voice.

kOA Mediatheque native processing remains deterministic. UCKK publication and online retrieval are optional external integrations and are not part of the core-local target. A learning package already received through an approved offline carrier can be quarantined, validated, explicitly accepted, and consulted without network access.

### 4.3.1 Optional directional UCKK services

Deploy outbound and inbound services separately when selected by the active profile:

`text
koa-uckk-publication-bridge.service
koa-uckk-import-bridge.service
`

The publication service depends on Publication Gateway authorization. The import service owns retrieval and quarantine only; accepted local records are created by kOA Mediatheque. Neither service belongs to the core-local target, and neither starts a reconnect-triggered synchronization sweep.

### 4.4 Background target

Example `/usr/lib/systemd/system/koa-background.target`:

```ini
[Unit]
Description=kOA required background services
Requires=koa-critical.target
Wants=koa-publication.service
Wants=koa-mediatheque-scheduler.service
After=koa-critical.target
```

Publication Gateway can remain active while remote destinations are offline. Boundary-crossing work becomes deferred according to contract.

### 4.5 Optional target

Example `/usr/lib/systemd/system/koa-optional.target`:

```ini
[Unit]
Description=kOA optional profile-enabled services
After=koa-core.target
```

Profile generation adds only compatible services.

SenTient is not added to this target on a sovereign runtime profile.

### 4.6 Recovery target

Example `/usr/lib/systemd/system/koa-recovery.target`:

```ini
[Unit]
Description=kOA recovery environment
Requires=local-fs.target
Wants=network-pre.target
After=local-fs.target
AllowIsolate=yes
Conflicts=koa-node.target
```

Normal authoritative writers do not remain active as hidden competitors during recovery.

### 4.7 Dependency guidance

Use:

- `Requires=` when failure invalidates the dependent unit;
- `Wants=` for useful but nonfatal companions;
- `After=` only for actual ordering;
- socket activation or retry for runtime availability;
- explicit readiness for authoritative dependencies.

Avoid encoding the whole component graph as one serial chain.

## 5. Component Service Baseline

### 5.1 Generic service shape

Example `/usr/lib/systemd/system/koa-component@.service`:

```ini
[Unit]
Description=kOA component %i
Documentation=file:/usr/share/doc/koa/components/%i.md
After=local-fs.target
After=koa-release-set-verify.service
RequiresMountsFor=/var/lib/koa/%i
ConditionPathExists=/etc/koa/active/release-set.json
ConditionPathExists=/etc/koa/components/%i/component.env

[Service]
Type=notify
User=koa-%i
Group=koa-%i
EnvironmentFile=/etc/koa/components/%i/component.env
ExecStart=/usr/lib/koa/active/services/%i/bin/%i serve
ExecReload=/usr/lib/koa/tools/koa-component-reload %i
Restart=on-failure
RestartSec=5s
TimeoutStartSec=90s
TimeoutStopSec=45s
KillSignal=SIGTERM
KillMode=mixed
NotifyAccess=main
RuntimeDirectory=koa/%i
RuntimeDirectoryMode=0750
StateDirectory=koa/%i
StateDirectoryMode=0750
CacheDirectory=koa/%i
CacheDirectoryMode=0750
LogsDirectory=koa/%i
LogsDirectoryMode=0750
UMask=0027

NoNewPrivileges=yes
PrivateTmp=yes
PrivateDevices=yes
ProtectSystem=strict
ProtectHome=yes
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectKernelLogs=yes
ProtectControlGroups=yes
ProtectClock=yes
ProtectHostname=yes
ProtectProc=invisible
ProcSubset=pid
RestrictSUIDSGID=yes
RestrictRealtime=yes
LockPersonality=yes
MemoryDenyWriteExecute=yes
RemoveIPC=yes
RestrictNamespaces=yes
RestrictAddressFamilies=AF_UNIX
SystemCallArchitectures=native
SystemCallFilter=@system-service
CapabilityBoundingSet=
AmbientCapabilities=

ReadWritePaths=/var/lib/koa/%i
ReadWritePaths=/var/cache/koa/%i
ReadWritePaths=/run/koa/%i
ReadOnlyPaths=/etc/koa/active
ReadOnlyPaths=/etc/koa/components/%i
ReadOnlyPaths=/usr/lib/koa/active

StandardOutput=journal
StandardError=journal
SyslogIdentifier=koa-%i

[Install]
WantedBy=koa-core.target
```

This is a baseline, not a universal final unit.

Address families, syscall filters, device access, and executable-memory restrictions remain component-specific.

### 5.2 Component-specific units

Use a dedicated unit when a template would hide important behavior.

Example Audit Broker additions:

```ini
[Unit]
Before=koa-core.target

[Service]
User=koa-audit
Group=koa-audit
ExecStart=/usr/lib/koa/active/services/audit/bin/audit-broker serve
RuntimeDirectory=koa/audit
StateDirectory=koa/audit
CacheDirectory=koa/audit
ReadWritePaths=/var/lib/koa/audit
ReadWritePaths=/var/cache/koa/audit
ReadWritePaths=/run/koa/audit
```

The actual ordering follows the component contract rather than a preferred visual boot sequence.

### 5.3 Readiness

A component reports ready only after:

- configuration validation;
- active Release Set verification;
- local state open or recovery;
- required schema and migration validation;
- socket or interface readiness;
- critical receipt path readiness;
- component invariant checks.

`Type=notify` is useful when the service can report this state.

### 5.4 Bounded restart

Use rate limits for persistent failures:

```ini
[Unit]
StartLimitIntervalSec=5min
StartLimitBurst=5

[Service]
Restart=on-failure
RestartSec=10s
```

A restart loop does not count as service recovery.

## 6. Socket Activation and Privileged Broker

### 6.1 Node Agent socket

Example `/usr/lib/systemd/system/koa-node-agent.socket`:

```ini
[Unit]
Description=kOA Node Agent local socket
PartOf=koa-node-agent.service

[Socket]
ListenStream=/run/koa/node-agent/broker.sock
SocketUser=koa-node-agent
SocketGroup=koa-broker-clients
SocketMode=0660
DirectoryMode=0750
RemoveOnStop=yes

[Install]
WantedBy=sockets.target
```

Socket access permits connection only.

Each request still carries caller identity, policy decision, scope, expected state, idempotency identity, deadline, and bounded parameters.

### 6.2 Node Agent service

Example `/usr/lib/systemd/system/koa-node-agent.service`:

```ini
[Unit]
Description=kOA Node Agent privileged broker
Requires=koa-node-agent.socket
After=local-fs.target
After=koa-release-set-verify.service
ConditionPathExists=/etc/koa/components/node-agent/component.env

[Service]
Type=notify
User=root
Group=root
EnvironmentFile=/etc/koa/components/node-agent/component.env
ExecStart=/usr/lib/koa/active/system/node-agent/bin/koa-node-agent serve   --socket /run/koa/node-agent/broker.sock
Restart=on-failure
RestartSec=3s
RuntimeDirectory=koa/node-agent
StateDirectory=koa/node-agent
UMask=0027

PrivateTmp=yes
PrivateDevices=yes
ProtectSystem=strict
ProtectHome=yes
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectKernelLogs=yes
ProtectControlGroups=yes
ProtectClock=yes
ProtectHostname=yes
ProtectProc=invisible
ProcSubset=pid
RestrictSUIDSGID=yes
RestrictRealtime=yes
LockPersonality=yes
RemoveIPC=yes
RestrictNamespaces=yes
RestrictAddressFamilies=AF_UNIX
SystemCallArchitectures=native
SystemCallFilter=@system-service
CapabilityBoundingSet=CAP_CHOWN CAP_DAC_OVERRIDE CAP_FOWNER CAP_SETGID CAP_SETUID
AmbientCapabilities=

ReadWritePaths=/var/lib/koa/node-agent
ReadWritePaths=/run/koa/node-agent
ReadWritePaths=/run/koa/activation
ReadOnlyPaths=/etc/koa
ReadOnlyPaths=/usr/lib/koa
```

The capability set is illustrative.

The active broker contract determines exact adapters, capabilities, paths, devices, and system calls.

A generic command runner is not added.

### 6.3 Narrow socket groups

Create narrow groups only for actual clients.

Example:

```text
g koa-broker-clients -
m koa-broker-clients koa-resource
m koa-broker-clients koa-publication
```

Do not add every service.

Prefer a separate group per component interface over one broad global services group.

## 7. Configuration, Credentials, and Release Binding

### 7.1 Static configuration

Use root-owned component configuration:

```text
/etc/koa/components/<component>/component.env
/etc/koa/components/<component>/component.json
```

Environment files contain bounded non-secret values:

```text
KOA_COMPONENT_ID=publication_gateway
KOA_PROFILE_ID=sovereign_linux_node
KOA_ACTIVE_RELEASE_SET=/etc/koa/active/release-set.json
KOA_RUNTIME_DIR=/run/koa/publication
KOA_STATE_DIR=/var/lib/koa/publication
```

Do not place passwords, private keys, bearer tokens, or recovery secrets in ordinary environment files.

### 7.2 Managed credentials

Use the registered credential mechanism.

Illustrative drop-in:

```ini
[Service]
LoadCredential=integration-token:/etc/koa/secrets.d/publication-token
```

The executable reads the credential from the service credential directory.

Identity and Trust owns secret lifecycle, rotation, revocation, and access evidence.

### 7.3 Active Release Set paths

Use stable active paths:

```text
/etc/koa/active/release-set.json
/usr/lib/koa/active/system/
/usr/lib/koa/active/services/
/usr/lib/koa/active/governance/
/usr/lib/koa/active/knowledge/
```

Units do not search for the highest version or newest modification time.

The complete active set always binds system, services, governance, and knowledge.

### 7.4 Verification unit

Example `/usr/lib/systemd/system/koa-release-set-verify.service`:

```ini
[Unit]
Description=Verify active kOA Release Set
DefaultDependencies=no
After=local-fs.target
Before=koa-critical.target
ConditionPathExists=/etc/koa/active/release-set.json

[Service]
Type=oneshot
ExecStart=/usr/lib/koa/tools/koa-verify-release-set   --manifest /etc/koa/active/release-set.json   --profile /etc/koa/profile/active-profile.json
RemainAfterExit=yes
NoNewPrivileges=yes
PrivateTmp=yes
PrivateDevices=yes
ProtectSystem=strict
ProtectHome=yes
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectKernelLogs=yes
ProtectControlGroups=yes
ProtectClock=yes
ProtectHostname=yes
RestrictAddressFamilies=AF_UNIX
CapabilityBoundingSet=
AmbientCapabilities=
ReadOnlyPaths=/etc/koa
ReadOnlyPaths=/usr/lib/koa
```

Verification covers four-channel compatibility, signatures, trust, revocation, profile, and required artifacts.

### 7.5 Reload behavior

Prefer restart or a component-defined validated reload.

A reload path:

1. validates new configuration;
2. verifies expected active Release Set;
3. stages it;
4. commits atomically;
5. verifies actual state;
6. records a receipt when required.

Do not send one generic reload signal to every service.

## 8. Resource Control, Logs, and Health

### 8.1 Profile baseline

Example resource drop-in:

```ini
[Service]
CPUWeight=25
IOWeight=25
MemoryHigh=768M
MemoryMax=1G
TasksMax=128
```

Values are examples.

The active profile owns actual limits.

### 8.2 Resource Governor updates

Resource Governor can produce a validated drop-in under:

```text
/run/systemd/system/<unit>.service.d/50-resource-admission.conf
```

Example:

```ini
[Service]
CPUQuota=50%
MemoryHigh=640M
IOWeight=20
```

Resource Governor owns admission. systemd applies the cgroup properties.

After applying a change:

```bash
systemctl daemon-reload
systemctl show koa-mediatheque.service   --property=CPUQuotaPerSecUSec   --property=MemoryHigh   --property=IOWeight
```

Verify actual state and record the result.

### 8.3 Operational logs

Useful structured fields include:

```text
KOA_COMPONENT_ID
KOA_INSTANCE_ID
KOA_RELEASE_SET_ID
KOA_PROFILE_ID
KOA_CORRELATION_ID
KOA_OPERATION
KOA_RESULT_CLASS
```

Do not log secret values, raw private keys, private proof payloads, unrestricted personal data, or full media payloads.

### 8.4 Audit distinction

journald is an operational log store.

It is not the authoritative critical-transition receipt store.

Critical receipts still follow the Audit Broker contract.

### 8.5 Watchdogs

Use a watchdog only when the component has a meaningful liveness signal:

```ini
[Service]
WatchdogSec=30s
Restart=on-failure
```

A watchdog ping does not prove correctness, durable state, dependency health, or user-visible success.

## 9. Offline Startup, Activation, and Recovery

### 9.1 Offline startup

A sovereign-offline node starts from local:

- identity and trust;
- profile;
- complete active Release Set;
- system, services, governance, and knowledge artifacts;
- component state;
- journals and receipts;
- recovery tools.

Do not add `network-online.target` to every kOA service.

Only an integration-specific unit waits for network readiness.

### 9.2 Optional connector ordering

Example connector-only drop-in:

```ini
[Unit]
Wants=network-online.target
After=network-online.target
```

Core local targets remain independent of Internet access.

### 9.3 Activation target

Example `/usr/lib/systemd/system/koa-activation.target`:

```ini
[Unit]
Description=kOA Release Set activation helpers
Requires=koa-release-set-verify.service
After=koa-release-set-verify.service
StopWhenUnneeded=yes
```

Activation is a separate transaction:

1. verify expected active Release Set;
2. stage all four selected channels;
3. verify compatibility, signatures, trust, and resources;
4. quiesce affected components;
5. apply migrations and dependent state;
6. commit the active authority pointer last;
7. start affected components;
8. run post-activation validation;
9. store activation receipts.

Individual units do not self-update.

### 9.4 Last-known-good behavior

When the active Release Set is invalid, policy can:

- block normal startup;
- isolate the recovery target;
- select one registered last-known-good Release Set;
- require recovery authority.

Individual services do not fall back to unrelated versions.

### 9.5 Component recovery

Example template:

```ini
[Unit]
Description=Recover kOA component %i
Conflicts=koa-component@%i.service
After=local-fs.target
ConditionPathExists=/usr/lib/koa/tools/koa-component-recover

[Service]
Type=oneshot
User=koa-%i
Group=koa-%i
ExecStart=/usr/lib/koa/tools/koa-component-recover   --component %i   --profile /etc/koa/profile/active-profile.json   --release-set /etc/koa/active/release-set.json
NoNewPrivileges=yes
PrivateTmp=yes
PrivateDevices=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=/var/lib/koa/%i
ReadWritePaths=/run/koa/%i
ReadOnlyPaths=/etc/koa
ReadOnlyPaths=/usr/lib/koa
```

The owning component defines restore, journal, migration, and evidence semantics.

### 9.6 Node recovery

A full recovery uses `koa-recovery.target` or a separate recovery boot.

It verifies:

- node identity and trust;
- complete Release Set;
- component state;
- receipts and journals;
- no dual authority;
- post-recovery capability state.

Starting the target alone does not establish completed disaster recovery.

## 10. Validation and Troubleshooting

### 10.1 Unit verification

Run:

```bash
systemd-analyze verify   /usr/lib/systemd/system/koa-*.service   /usr/lib/systemd/system/koa-*.socket   /usr/lib/systemd/system/koa-*.target
```

Inspect effective configuration:

```bash
systemctl cat koa-audit.service
systemctl show koa-audit.service
```

### 10.2 Security review

Run:

```bash
systemd-analyze security koa-audit.service
systemd-analyze security koa-publication.service
systemd-analyze security koa-node-agent.service
```

Treat scores as review input, not proof of conformance.

### 10.3 Required tests

Test in an isolated node or virtual machine:

- startup without network;
- critical and noncritical component failure;
- bounded restart;
- direct-write denial between component accounts;
- socket access and request authorization;
- Node Agent adapter allowlists;
- Resource Governor cgroup updates;
- secret non-disclosure;
- complete Release Set activation;
- last-known-good recovery;
- recovery target fencing;
- optional integration removal.

### 10.4 Troubleshooting matrix

| Symptom | Likely cause | Safe response |
| --- | --- | --- |
| Unit waits forever for network | Broad network-online dependency | Move the dependency to the connector and preserve local deferred state |
| Component cannot write its state | Missing owned path or overstrict sandbox | Verify the component contract and add only the exact path |
| Component can read another store | Broad group, ACL, home, or path rule | Revoke access and rerun negative boundary tests |
| Service starts before Release Set verification | Missing verification dependency | Add the dependency and block readiness |
| Restart loop consumes resources | Persistent fault or unbounded rate | Stop the loop, preserve evidence, and enter recovery |
| Node Agent adapter fails | Capability or path allowlist mismatch | Correct the registered adapter; do not grant generic root access |
| Journal contains a secret | Application logging or environment leak | Revoke, remediate, and verify redaction |
| Optional connector blocks startup | Wrong target or dependency | Move it to background or optional scope |
| Recovery starts with normal writers active | Missing conflict or fencing | Stop and correct target isolation before recovery |
| One channel updates independently | Unit points to a mutable package path | Restore Release Set-bound paths and repeat activation |

### 10.5 Repository validation

Run from a validated workspace:

```bash
uv run python docs/tools/validate_docs.py
uv run python docs/tools/check_component_boundaries.py
uv run python docs/tools/check_profile_inheritance.py
uv run python docs/tools/check_release_sets.py
uv run python docs/tools/check_interfile_locks.py
uv run python docs/tools/check_traceability.py
uv run python docs/tools/check_no_unresolved_state.py
```

Deployment-specific unit tests still run in the target environment.

## 11. Completion Checklist

The layout is ready when:

- [ ] every long-running component has a dedicated identity;
- [ ] every component writes only to owned paths;
- [ ] local interfaces use narrow sockets or registered endpoints;
- [ ] socket access remains separate from operation authorization;
- [ ] Node Agent exposes only registered privileged adapters;
- [ ] no generic root command interface exists;
- [ ] targets distinguish critical, core, background, optional, activation, and recovery lifecycle;
- [ ] offline-capable services do not depend globally on network readiness;
- [ ] the active Release Set is verified before critical startup;
- [ ] units use active Release Set paths rather than newest-version discovery;
- [ ] system, services, governance, and knowledge remain bound in one active Release Set;
- [ ] activation commits the active authority pointer last;
- [ ] recovery conflicts with ordinary authoritative writers;
- [ ] static limits match the profile;
- [ ] dynamic limits remain attributable to Resource Governor admission;
- [ ] readiness includes state, migration, interface, and receipt checks;
- [ ] journald is not represented as the authoritative audit store;
- [ ] secrets use managed credential references;
- [ ] hardening exceptions are component-specific and tested;
- [ ] restart policies are bounded;
- [ ] startup, failure, offline, activation, recovery, and removal tests pass;
- [ ] `systemd-analyze verify` passes;
- [ ] direct-write negative tests pass for every component identity;
- [ ] optional integration removal leaves core local operation intact;
- [ ] the result remains a sovereign Linux recipe rather than a deployment conformance claim.
