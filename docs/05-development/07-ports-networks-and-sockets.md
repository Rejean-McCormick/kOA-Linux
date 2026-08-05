<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-DEV-007",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "development_toolchain",
  "scope": [
    "profile:developer_linux_workstation",
    "profile:developer_windows_wsl"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/operating_modes",
    "contracts/profiles/developer-linux-workstation.profile.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "schemas/developer-workspace.schema.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-DEV-001",
    "DEC-DEV-002",
    "DEC-PROFILE-001",
    "DEC-CONTAINER-001",
    "DEC-DATA-001",
    "DEC-GOV-001"
  ],
  "requirement_ids": [
    "REQ-DEV-NET-001",
    "REQ-DEV-NET-002",
    "REQ-DEV-NET-003",
    "REQ-DEV-NET-004",
    "REQ-DEV-NET-005",
    "REQ-DEV-NET-006",
    "REQ-DEV-NET-007",
    "REQ-DEV-NET-008",
    "REQ-DEV-NET-009",
    "REQ-DEV-NET-010",
    "REQ-DEV-NET-011",
    "REQ-DEV-NET-012",
    "REQ-DEV-NET-013",
    "REQ-DEV-NET-014",
    "REQ-DEV-NET-015",
    "REQ-DEV-NET-016",
    "REQ-DEV-NET-017",
    "REQ-DEV-NET-018",
    "REQ-DEV-NET-019",
    "REQ-DEV-NET-020",
    "REQ-DEV-NET-021",
    "REQ-DEV-NET-022",
    "REQ-DEV-NET-023",
    "REQ-DEV-NET-024"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-DEV-001",
    "LOCK-DEV-002",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DEV-005",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-007",
    "DOC-SYS-014",
    "DOC-SYS-016",
    "DOC-SYS-017",
    "DOC-PROFILE-005",
    "DOC-PROFILE-006",
    "DOC-DEV-000",
    "DOC-DEV-001",
    "DOC-DEV-002",
    "DOC-DEV-003",
    "DOC-DEV-004",
    "DOC-DEV-005",
    "DOC-DEV-006"
  ],
  "tags": [
    "development",
    "workspace-isolation",
    "ports",
    "networks",
    "sockets",
    "service-discovery",
    "parallel-workspaces",
    "containers",
    "wsl",
    "security",
    "resource-governance"
  ]
}
KOA:DOC-META:END -->

# Ports, Networks, and Sockets

## 1. Purpose

This document defines the development rules for ports, logical networks, service discovery, local IPC sockets, and endpoint lifecycle.

The goal is to allow multiple applications, branches, worktrees, and component variants to run simultaneously on one development host without collisions or hidden sharing.

The model separates three endpoint spaces:

`text
workspace-internal endpoint
host-exposed endpoint
workspace-local IPC endpoint
`

A service can use a stable internal port inside its isolated workspace network. Host exposure uses a separately allocated host port. Local IPC uses a socket path or platform-equivalent endpoint inside the workspace runtime namespace.

The workspace identity is the common namespace for all three spaces.

This model prevents:

- fixed host-port collisions;
- shared global socket paths;
- cross-workspace service discovery;
- accidental communication between branches;
- silent fallback to a different port;
- stale allocations that appear both active and free;
- endpoint reachability being mistaken for authorization;
- container or operating-system implementation choices becoming universal architecture.

## 2. Scope

This document applies to development workspaces under:

`text
developer_linux_workstation
developer_windows_wsl
`

It applies to:

- native development processes;
- rootless or system containers selected by a profile;
- Docker or Podman development environments;
- WSL-hosted development services;
- databases;
- queues;
- HTTP and HTTPS services;
- TCP and UDP listeners;
- Unix-domain sockets;
- platform-equivalent local IPC endpoints;
- development proxies;
- test harnesses;
- mock integrations;
- local service discovery;
- external endpoint exposure;
- workspace activation and teardown.

It governs mutable development communication state.

It does not define production network architecture, sovereign firewall policy, public ingress, service-mesh selection, cluster networking, or external integration authorization. Those concerns belong to system, profile, security, operations, integration, and component contracts.

A recipe can select an implementation such as Podman networks, Docker networks, systemd socket activation, a reverse proxy, or a WSL forwarding mechanism. The recipe remains non-authoritative unless the active profile adopts it.

## 3. Canonical References

The canonical sources for this document are:

`text
generated/authority-manifest.json
generated/decision-index.json
contracts/system.contract.json#/operating_modes
contracts/profiles/developer-linux-workstation.profile.json
contracts/profiles/developer-windows-wsl.profile.json
schemas/developer-workspace.schema.json
generated/requirements-index.json
generated/assertion-index.json
generated/traceability.json
generated/evidence-catalog.json
generated/exception-index.json
`

Their ownership roles are:

| Canonical source | Ownership |
| --- | --- |
| `developer-workspace.schema.json` | Workspace identity, port allocation, network isolation, parallel execution, and lifecycle structure |
| Developer profile contracts | Permitted runtimes, host behavior, capacity, security, and platform-specific implementation constraints |
| `system.registry.json#/operating_modes` | Development-workspace mode and its isolation boundary |
| `requirements.registry.json` | Normative requirement text, strength, scope, ownership, and validation |
| `locks.registry.json` | Development, profile, data, governance, and implementation invariants |
| `traceability.registry.json` | Links to decisions, profiles, schemas, tests, evidence, and dependent documents |
| `evidence.registry.json` | Port-collision, network-isolation, socket-lifecycle, and teardown evidence |
| `exceptions.registry.json` | Bounded deviations that cannot create implicit global endpoints or cross-workspace sharing |

This document explains the behavior. It does not become a second owner of schema fields, profile membership, or workspace identifiers.

## 4. Model and Responsibilities

### 4.1 Workspace namespace

The canonical workspace identifier is derived from:

`text
component + branch_or_purpose + unique_suffix
`

It prefixes or otherwise scopes:

- network names;
- container names;
- service names;
- host-port allocations;
- socket paths;
- runtime directories;
- PID files;
- temporary directories;
- logs;
- database identities;
- volume names;
- secret names.

Examples of workspace identities include:

`text
konnaxion-main-a31f
konnaxion-feature-voting-92cd
orgo-main-b114
`

The exact formatting is validated by the workspace schema.

### 4.2 Endpoint spaces

| Endpoint space | Identity | Collision boundary |
| --- | --- | --- |
| Workspace-internal network | Workspace network plus service name and internal port | One isolated logical network |
| Host-exposed endpoint | Bind address, host port, and transport protocol | Entire applicable host network namespace |
| Workspace-local IPC | Workspace runtime namespace plus socket name | Workspace runtime directory or equivalent |

The same internal port can be reused by multiple workspaces because the network boundaries are isolated. Host ports remain unique for their bind tuple.

### 4.3 Internal service ports

A component can declare stable internal ports such as:

`text
web: 8080/tcp
database: 5432/tcp
queue: 6379/tcp
metrics: 9090/tcp
`

These values remain inside the workspace network. They improve reproducibility because service-to-service configuration does not change when the host allocation changes.

An internal listener is not automatically reachable from the host or another workspace.

### 4.4 Host-port allocation

A host-port allocation is a registry object with a lifecycle.

The logical record includes:

`text
allocation_id
workspace_id
service_id
container_or_internal_port
host_port
protocol
bind_address_class
owner
state
allocated_at
activated_at
expires_at
released_at
release_condition
`

Logical states include:

`text
requested
reserved
active
release_pending
released
expired
recovery_required
`

The allocation registry is the exclusive owner of host-port availability. Process inspection is validation evidence, not a replacement registry.

### 4.5 Bind scope

Default development exposure is local-only.

Bind-address classes include:

`text
loopback
workspace_bridge
declared_lan
declared_test_interface
`

Broader exposure is explicit because it changes who can reach the endpoint. A service that needs LAN access declares the purpose, profile allowance, security context, and owning workspace.

Wildcard binding is not an implicit convenience default.

### 4.6 Network isolation

Each workspace has one isolated logical network or an equivalent boundary.

The network name is derived from `workspace_id`. Services inside the workspace use workspace-local discovery names.

The default behavior is:

`text
workspace A cannot resolve or connect to workspace B
workspace B cannot resolve or connect to workspace A
`

An explicit cross-workspace link identifies:

- both workspace identities;
- named source and destination services;
- allowed endpoint tuples;
- purpose;
- owner;
- lifetime;
- teardown behavior.

Such a link does not merge the workspaces.

### 4.7 Service discovery

Service discovery uses workspace-local names, for example:

`text
api
database
queue
worker
`

The runtime resolves those names only within the workspace boundary. Host-global aliases and manually edited global name mappings are avoided because they create collision and cleanup risks.

A host-exposed endpoint is addressed through its allocation record rather than by assuming a fixed port.

### 4.8 Local IPC sockets

Local IPC can use Unix-domain sockets or a platform-equivalent endpoint.

The logical socket identity includes:

`text
workspace_id
service_id
socket_name
endpoint_type
runtime_namespace
owner
permissions
lifecycle_state
`

A typical Linux or WSL implementation places sockets beneath a workspace-specific runtime directory. The architectural requirement is the namespace and lifecycle, not one absolute filesystem path.

Socket directories are not shared between active workspaces.

### 4.9 Socket activation

A socket-activated service has two ownership states:

1. endpoint reserved by the activation mechanism;
2. endpoint accepted by the service.

The workspace contract identifies the responsible activation mechanism and service. A socket cannot silently remain owned by a retired workspace or unrelated process.

### 4.10 Port and socket security

Endpoint reachability is not authorization.

A caller still requires:

- identity where the endpoint contract requires it;
- trust verification where applicable;
- application or governance authorization;
- component-specific data access;
- disclosure authority for external transfer.

Socket permissions and local network boundaries reduce exposure but do not replace application controls.

### 4.11 External connectivity

External connectivity remains separate from workspace-local networking.

A workspace declares:

- required external destinations;
- integration identity;
- transport;
- local egress path;
- proxy use where applicable;
- transferred data class;
- failure behavior.

External AI surfaces remain optional integrations and do not gain access merely because a development service has outbound connectivity.

### 4.12 Diagnostics

Endpoint diagnostics can expose:

- workspace identity;
- service identity;
- internal endpoint;
- host allocation;
- protocol;
- bind scope;
- network attachment;
- socket state;
- owning process or activation mechanism;
- allocation state;
- stable failure code.

Diagnostics exclude credentials, private keys, tokens, secret values, and unrestricted content payloads.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-DEV-NET-001,REQ-DEV-NET-002,REQ-DEV-NET-003,REQ-DEV-NET-004,REQ-DEV-NET-005,REQ-DEV-NET-006,REQ-DEV-NET-007,REQ-DEV-NET-008,REQ-DEV-NET-009,REQ-DEV-NET-010,REQ-DEV-NET-011,REQ-DEV-NET-012,REQ-DEV-NET-013,REQ-DEV-NET-014,REQ-DEV-NET-015,REQ-DEV-NET-016,REQ-DEV-NET-017,REQ-DEV-NET-018,REQ-DEV-NET-019,REQ-DEV-NET-020,REQ-DEV-NET-021,REQ-DEV-NET-022,REQ-DEV-NET-023,REQ-DEV-NET-024 -->
- **REQ-DEV-NET-001 — SHALL:** Every active development workspace use its stable workspace_id to namespace network names, service names, host-port allocations, sockets, runtime directories, logs, PID files, and related mutable communication state.
- **REQ-DEV-NET-002 — SHALL:** Each workspace have one isolated logical network or an explicitly equivalent isolated communication boundary.
- **REQ-DEV-NET-003 — SHALL NOT:** Cross-workspace connectivity be enabled by default.
- **REQ-DEV-NET-004 — SHALL:** Any cross-workspace communication be explicit, bounded to named endpoints, attributable to both workspaces, and removable without changing either workspace's canonical identity.
- **REQ-DEV-NET-005 — SHALL:** Fixed service ports be permitted inside an isolated workspace network when they do not create host-port collisions.
- **REQ-DEV-NET-006 — SHALL:** Every host-port binding be allocated through a workspace-scoped allocation registry before the service binds the port.
- **REQ-DEV-NET-007 — SHALL NOT:** Two active allocations use the same host address, port, and transport-protocol tuple.
- **REQ-DEV-NET-008 — SHALL:** Ordinary development host-port allocations use the range 1024 through 65535.
- **REQ-DEV-NET-009 — SHALL:** A host-port allocation record identify the workspace, service, internal port, host port, transport protocol, bind address class, lifecycle state, owner, allocation time, and release condition.
- **REQ-DEV-NET-010 — SHALL:** Host-port allocation, activation, renewal, release, and recovery be atomic with respect to the allocation registry.
- **REQ-DEV-NET-011 — SHALL NOT:** A service bind a different host port silently when its declared allocation is unavailable.
- **REQ-DEV-NET-012 — SHALL:** The default host bind scope be loopback or an equivalently local-only boundary unless an explicit profile and security decision permits broader exposure.
- **REQ-DEV-NET-013 — SHALL:** Workspace-local service discovery use names scoped to the workspace network rather than host-global aliases.
- **REQ-DEV-NET-014 — SHALL:** Local IPC sockets use workspace-scoped paths or names located in the workspace runtime namespace.
- **REQ-DEV-NET-015 — SHALL NOT:** Two active workspaces share a mutable socket endpoint, runtime socket directory, PID file, or service-control endpoint.
- **REQ-DEV-NET-016 — SHALL:** Socket creation validate owner identity, permissions, path length, parent-directory ownership, stale-endpoint state, and expected endpoint type before activation.
- **REQ-DEV-NET-017 — SHALL:** Stale socket and port cleanup verify workspace ownership and inactive service state before removing or releasing the endpoint.
- **REQ-DEV-NET-018 — SHALL:** Development services declare every listening port, socket, network attachment, and externally reachable endpoint in the workspace contract.
- **REQ-DEV-NET-019 — SHALL:** External network access follow the active profile and integration policy and remain separate from local service discovery and workspace isolation.
- **REQ-DEV-NET-020 — SHALL NOT:** Network reachability, successful connection, possession of a socket path, or access to a host port substitute for identity, authorization, data ownership, or trust verification.
- **REQ-DEV-NET-021 — SHALL:** Port, network, and socket diagnostics expose workspace identity, endpoint state, owning service, protocol, bind scope, and stable failure reason without exposing secrets or credential material.
- **REQ-DEV-NET-022 — SHALL:** Workspace teardown release host ports, disconnect and remove workspace networks, remove owned sockets, and preserve unrelated workspace endpoints.
- **REQ-DEV-NET-023 — SHALL:** Interrupted activation or teardown preserve a recoverable allocation state and prevent an endpoint from being simultaneously considered free and active.
- **REQ-DEV-NET-024 — SHALL:** Operating-system, container-runtime, firewall, proxy, and socket implementation details remain profile-scoped or recipe-scoped unless an active profile contract adopts them.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Workspace network activation

Network activation follows this sequence:

1. resolve the active workspace contract;
2. validate `workspace_id`;
3. verify that no active network uses the same runtime name;
4. create or resolve the isolated logical network;
5. attach only declared services;
6. register workspace-local service discovery;
7. validate default cross-workspace isolation;
8. expose network status;
9. continue with service and endpoint activation.

Failure leaves the workspace network inactive and does not alter another workspace.

### 6.2 Host-port allocation

Port allocation follows this sequence:

1. receive workspace, service, internal port, protocol, and bind-scope request;
2. validate the active workspace and service declaration;
3. select or validate a host port in the permitted range;
4. check the complete bind tuple against active and reserved allocations;
5. create the reservation atomically;
6. bind the service;
7. verify that the expected process owns the endpoint;
8. mark the allocation active;
9. expose the allocation to the workspace tooling.

A bind failure returns the allocation to a recoverable or released state according to the registry transaction. The service does not choose an undeclared fallback port.

### 6.3 Service startup

Service startup:

1. resolves workspace-local dependencies by service name;
2. resolves required host allocations and socket reservations;
3. validates endpoint ownership;
4. starts the process or container under the workspace identity;
5. verifies listeners and sockets;
6. records readiness;
7. reports any mismatch between declared and observed endpoints.

### 6.4 Explicit cross-workspace link

A cross-workspace link:

1. identifies both active workspaces;
2. names the exact source and destination services;
3. declares endpoint tuples and purpose;
4. verifies that both workspace owners permit the link;
5. creates the narrow communication path;
6. records its lifetime;
7. monitors endpoint identity;
8. removes the link independently during expiry or teardown.

A link does not expose unrelated services.

### 6.5 Socket creation

Socket creation:

1. resolves the workspace runtime namespace;
2. validates directory ownership and permissions;
3. checks for an existing endpoint;
4. distinguishes an active endpoint from stale state;
5. reserves the socket identity;
6. creates the endpoint;
7. verifies endpoint type and owner;
8. marks it active.

An unknown existing endpoint blocks activation.

### 6.6 Stale endpoint recovery

Stale endpoint recovery:

1. resolves the allocation or socket record;
2. verifies that the owning workspace exists;
3. verifies that the owning service is inactive;
4. verifies that no live process owns the endpoint;
5. preserves diagnostic evidence where needed;
6. removes the stale socket or releases the port;
7. updates the registry atomically;
8. retries activation only through the standard procedure.

### 6.7 Workspace teardown

Teardown:

1. stop workspace services;
2. verify listeners and socket users have exited;
3. mark active host allocations release-pending;
4. release host ports;
5. remove owned IPC endpoints;
6. disconnect and remove workspace network attachments;
7. remove the isolated network;
8. remove owned runtime and PID state;
9. verify that unrelated workspace endpoints remain active;
10. close the workspace endpoint lifecycle.

### 6.8 Interrupted teardown recovery

After interruption:

1. load the workspace and allocation records;
2. compare registry state with observed processes, listeners, networks, and sockets;
3. classify each endpoint as active, stale, released, or recovery-required;
4. avoid assigning recovery-required endpoints to another workspace;
5. complete release or restore the original active state;
6. record the recovery result.

## 7. Failure States and Safe Degradation

| Failure code | Condition | Protected result | Safe degraded result |
| --- | --- | --- | --- |
| `workspace_network_name_conflict` | Runtime network name is already owned by another active workspace | Network activation is denied | Allocate the schema-compliant workspace name |
| `workspace_network_isolation_failed` | Default cross-workspace isolation cannot be established | Workspace services remain inactive | Local non-network tooling can continue |
| `workspace_cross_link_undefined` | Cross-workspace communication lacks a complete explicit link | Connection is denied | Use independent workspace operation |
| `workspace_port_allocation_conflict` | Host bind tuple is active or reserved | Allocation is denied | Allocate a different registered host port |
| `workspace_port_out_of_range` | Host port is outside 1024 through 65535 | Allocation is denied | Request a permitted port |
| `workspace_port_registry_unavailable` | Allocation state cannot be recorded reliably | New host binding is denied | Internal-only service operation can continue where declared |
| `workspace_port_bind_failed` | Process cannot bind the reserved endpoint | Service remains unready | Preserve reservation for bounded recovery or release it |
| `workspace_port_owner_mismatch` | Observed listener does not match the declared workspace service | Endpoint activation is denied | Stop or investigate the unexpected listener |
| `workspace_port_silent_fallback_detected` | Service listens on an undeclared fallback port | Service is marked non-conformant and unready | Correct configuration and restart |
| `workspace_socket_path_conflict` | Socket path or name belongs to another active endpoint | Socket activation is denied | Use the workspace-scoped endpoint |
| `workspace_socket_owner_mismatch` | Existing socket owner or type differs from the declaration | Endpoint is not removed automatically | Perform verified stale-endpoint recovery |
| `workspace_socket_permissions_invalid` | Runtime directory or socket permissions are unsafe | Service activation is denied | Repair the workspace runtime namespace |
| `workspace_stale_endpoint_unverified` | Endpoint appears stale but ownership cannot be proven | Endpoint remains reserved | Manual or controlled recovery |
| `workspace_external_exposure_unauthorized` | Service requests broader host or LAN exposure without authority | Broad binding is denied | Use loopback or internal-only access |
| `workspace_endpoint_identity_missing` | Listener or socket lacks workspace and service attribution | Endpoint is not activated | Register the declaration and retry |
| `workspace_teardown_partial` | Ports, networks, or sockets remain after interrupted teardown | Endpoints remain unavailable for reuse | Complete recovery without affecting other workspaces |
| `workspace_diagnostic_secret_exposure` | Endpoint diagnostics contain protected material | Diagnostic output is rejected | Produce a redacted view |
| `workspace_runtime_specific_assumption` | A profile-independent contract depends on runtime-specific behavior | Validation fails | Move the choice to a profile or recipe |

Failure remains scoped to the affected workspace or endpoint. A collision in one workspace does not stop unrelated workspaces.

## 8. Cross-Component Interactions

### 8.1 Developer workspace contract

The workspace contract owns the declared services, internal ports, host allocations, network identity, sockets, resource budget, and lifecycle.

This document explains how those fields behave.

### 8.2 Resource Governor

Port allocation does not reserve CPU, memory, I/O, process count, or concurrency.

The Resource Governor separately admits services and jobs under the workspace budget. A service with a valid port allocation can still remain queued or rejected for resource reasons.

### 8.3 Identity and Trust

Identity and Trust establishes service, component, workspace, node, and developer identities where required.

Endpoint possession does not replace those identities.

### 8.4 Governance and application authorization

Governance Policy Runtime, where deployed, handles governance authorization. Each component handles its business-data and action authorization.

Network connectivity is only a transport condition.

### 8.5 Databases and queues

Workspace databases and queues use workspace-scoped service names, storage identities, users, sockets, and host allocations.

A shared physical service can be used only when the relevant development contract preserves logical identity and write boundaries.

### 8.6 Containers

A container runtime can implement isolated networks, service names, port forwarding, and endpoint lifecycle.

Linux development prefers rootless Podman where the profile adopts that choice. Windows/WSL development can use Docker or Podman. The application contract does not depend on runtime-specific behavior.

### 8.7 Host and WSL boundaries

A Windows/WSL workspace can require forwarding between WSL and the Windows host.

The profile or recipe defines the mechanism. The allocation registry still owns the exposed host tuple, and broad exposure remains explicit.

### 8.8 External integrations

Mock and real external integrations declare their endpoints independently.

A mock endpoint in one workspace does not become the default integration endpoint for another workspace.

### 8.9 Observability and receipts

Ordinary endpoint lifecycle uses structured logs and status records. A profile can classify broader exposure, privileged bind changes, or recovery operations as critical transitions requiring receipts.

## 9. Decision Closure and Prohibited Assumptions

This document closes the development endpoint model as follows:

- every workspace has an isolated logical network or equivalent boundary;
- workspace names scope networks, services, ports, sockets, and runtime state;
- fixed internal ports are valid inside isolated networks;
- host ports use a workspace-scoped allocation registry;
- host-port uniqueness includes bind address, port, and protocol;
- ordinary host ports begin at 1024;
- loopback is the default host bind scope;
- cross-workspace connectivity is disabled by default;
- explicit links remain narrow and removable;
- sockets belong to workspace runtime namespaces;
- stale cleanup requires ownership verification;
- endpoint reachability is not authorization;
- teardown preserves unrelated workspace endpoints;
- runtime-specific behavior remains profile-scoped or recipe-scoped.

The following assumptions are prohibited:

- every branch can bind the same fixed host port;
- a process can choose any available fallback port silently;
- an observed free port is free without consulting the registry;
- internal container ports must be globally unique;
- all workspaces can share one default network;
- service names are host-global;
- a socket path can be shared because only one process is expected at a time;
- an existing socket can be deleted without checking its owner;
- loopback access proves caller authorization;
- LAN reachability is harmless in development;
- a Docker or Podman implementation is universally mandatory;
- a Linux socket path is a global cross-platform contract;
- WSL forwarding can bypass the host allocation registry;
- teardown can remove endpoints by name without workspace attribution;
- external connectivity grants access to external AI or publication services;
- a port allocation grants resource capacity.

A new global endpoint class, allocation state, cross-workspace communication rule, or host-exposure default requires an accepted owner decision and complete impact validation.

## 10. Validation Criteria

This document is conformant when all of the following checks pass:

1. the metadata block is first, valid, and declares status `active`;
2. the document contains the required 11 normative sections;
3. all 24 requirement identifiers are unique and registered;
4. every declared decision is accepted;
5. every declared lock exists and is active;
6. every active workspace has a schema-valid workspace identity;
7. network names and service runtime names are workspace-scoped;
8. cross-workspace connectivity is absent by default;
9. explicit cross-workspace links identify both workspaces, named endpoints, purpose, owner, and lifetime;
10. fixed internal ports can be reused in isolated workspace networks;
11. every host binding has an active allocation record;
12. no active host address, port, and protocol tuple is duplicated;
13. ordinary host ports remain within 1024 through 65535;
14. undeclared fallback listeners fail validation;
15. broad host or LAN exposure requires explicit profile and security authority;
16. sockets and runtime directories are workspace-scoped;
17. socket owner, type, permissions, and stale state are validated before activation or removal;
18. service declarations enumerate listening ports, sockets, network attachments, and external endpoints;
19. diagnostic views exclude secrets and credentials;
20. two branches or applications run concurrently without port, network, service-name, socket, PID, or runtime-directory collisions;
21. teardown releases only the owning workspace's endpoints;
22. interrupted activation and teardown preserve recoverable allocation state;
23. development resource tests prove that port allocation does not bypass Resource Governor admission;
24. security tests prove that endpoint reachability does not bypass identity or authorization;
25. Linux, container, WSL, firewall, proxy, and socket choices remain within active profiles or recipes;
26. no unresolved-authority marker, duplicate identifier, or unregistered normative statement exists;
27. active prose is English;
28. ordinary Markdown validation does not depend on file-content hashes.

Expected validator failure codes include:

`text
workspace_network_name_conflict
workspace_network_isolation_failed
workspace_cross_link_undefined
workspace_port_allocation_conflict
workspace_port_out_of_range
workspace_port_registry_unavailable
workspace_port_bind_failed
workspace_port_owner_mismatch
workspace_port_silent_fallback_detected
workspace_socket_path_conflict
workspace_socket_owner_mismatch
workspace_socket_permissions_invalid
workspace_stale_endpoint_unverified
workspace_external_exposure_unauthorized
workspace_endpoint_identity_missing
workspace_teardown_partial
workspace_diagnostic_secret_exposure
workspace_runtime_specific_assumption
`

## 11. Non-Normative Examples

### 11.1 Two branches using the same internal port

Two Konnaxion branches both run an API on internal port `8080/tcp`. Their isolated networks and service names differ. The allocation registry assigns different loopback host ports, so both branches run simultaneously.

### 11.2 Local database socket

A workspace database creates a socket under its workspace runtime namespace. Another branch uses a different runtime namespace even though the socket filename is identical.

### 11.3 Port conflict during startup

A service requests a host tuple already reserved by another workspace. Activation stops before binding. The workspace tooling allocates a new registered port and updates the workspace view; the service never selects an undeclared fallback itself.

### 11.4 Explicit integration test link

An Orgo workspace needs to call a Konnaxion test service. The developer creates an explicit link naming both workspaces and the single destination endpoint. Teardown of either workspace removes the link without exposing other services.

### 11.5 Interrupted teardown

A workstation restarts while a workspace is being removed. On recovery, the allocation registry marks its endpoints recovery-required. Tooling verifies that no owning processes remain, then releases only that workspace's ports, sockets, and network.
