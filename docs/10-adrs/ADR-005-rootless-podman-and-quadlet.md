<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ADR-005",
  "document_class": "adr",
  "version": "1.0.0",
  "status": "active",
  "language": "en",
  "layer": "architecture_decision",
  "owner": "profile-architecture",
  "scope": [
    "global",
    "profile:developer_linux_workstation",
    "profile:developer_windows_wsl",
    "profile:user_lightweight",
    "profile:sovereign_linux_node",
    "profile:sovereign_hub",
    "profile:build_farm",
    "profile:control_plane"
  ],
  "canonical_refs": [
    "generated/decision-index.json#/decisions/DEC-CONTAINER-001",
    "generated/profile-catalog.json",
    "contracts/profiles/developer-linux-workstation.profile.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "contracts/profiles/user-lightweight.profile.json",
    "contracts/profiles/sovereign-linux-node.profile.json",
    "contracts/profiles/sovereign-hub.profile.json",
    "contracts/profiles/build-farm.profile.json",
    "contracts/profiles/control-plane.profile.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json"
  ],
  "decision_ids": [
    "DEC-CONTAINER-001"
  ],
  "requirement_ids": [
    "REQ-IMPL-002",
    "REQ-PROFILE-001"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-DEV-003",
    "LOCK-DEV-004"
  ],
  "adr_ids": [
    "ADR-005"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-PROFILE-001",
    "DOC-PROFILE-002",
    "DOC-PROFILE-005",
    "DOC-PROFILE-006",
    "DOC-PROFILE-007",
    "DOC-PROFILE-008",
    "DOC-PROFILE-010",
    "DOC-DEV-006",
    "DOC-CONF-017"
  ],
  "tags": [
    "adr",
    "containers",
    "podman",
    "rootless",
    "quadlet",
    "systemd",
    "oci",
    "linux",
    "sovereign-linux",
    "development",
    "profile-scoped"
  ],
  "effective_at": "2026-08-03T19:29:00-04:00"
}
KOA:DOC-META:END -->

# ADR-005: Rootless Podman and Quadlet

## Status

**Accepted**

- **ADR ID:** `ADR-005`
- **Owner decision:** `DEC-CONTAINER-001`
- **Effective date:** 2026-08-03
- **Decision owner:** Profile Architecture
- **Change class:** Major when the profile adoption matrix or runtime-independence boundary changes

## Context

kOA supports primary deployment profiles with different operating-system boundaries, operational responsibilities, hardware envelopes, lifecycle requirements, and assurance needs.

A universal container-runtime mandate would create several problems:

- Windows and WSL development need implementation flexibility.
- Lightweight user deployments do not require containers as a baseline.
- Sovereign Linux deployments benefit from rootless service isolation and declarative host integration.
- Build workers need OCI-compatible execution without one globally prescribed product.
- Application contracts must remain portable across profile-approved runtimes.
- systemd and Quadlet are Linux implementation choices rather than universal component semantics.

The architecture therefore needs a profile-scoped runtime decision that provides a preferred Linux path without coupling application behavior to Podman, Quadlet, systemd, Docker, Kubernetes, or another runtime product.

## Decision

The canonical container-runtime matrix is:

| Profile or profile class | Decision |
| --- | --- |
| `developer_linux_workstation` | Rootless Podman is preferred. A profile-conformant equivalent can be used when explicitly declared and validated. |
| `sovereign_linux_node` | Rootless Podman and Quadlet are preferred for profile-managed container services. |
| `developer_windows_wsl` | Docker or Podman is permitted. The selected Windows/WSL boundary and runtime behavior must be explicit in the profile claim. |
| `user_lightweight` | Containers are optional. No user-lightweight capability depends on containers unless the active profile contract explicitly adopts them. |
| `build_farm` | An OCI-compatible runtime is required. Runtime selection remains an implementation and profile decision. |
| `sovereign_hub` | Runtime and orchestration are selected by the active profile contract and measured operational need. Rootless operation remains preferred where the selected Linux runtime supports it. |
| `control_plane` | Runtime and orchestration are selected by the active profile contract. Endpoint-specific assumptions are not inherited automatically. |

The global boundary is:

> Application and component contracts remain runtime-independent unless the relevant active profile explicitly adopts runtime-specific behavior.

Quadlet is a preferred sovereign-Linux implementation mechanism for declarative, systemd-integrated management of Podman containers. It is not part of the global application contract, component interface model, artifact identity model, or cross-platform baseline.

## Decision Drivers

The decision is driven by these architectural needs:

1. reduce ordinary dependence on root-level container daemons;
2. preserve least-privilege execution for development and sovereign Linux services;
3. provide a declarative Linux service-management path for sovereign deployments;
4. align container lifecycle with profile-owned operational controls;
5. keep application contracts portable across approved OCI runtimes;
6. support Windows/WSL without treating it as identical to native Linux;
7. avoid requiring containers for lightweight user operation;
8. permit build-farm and control-plane implementations to select suitable OCI or orchestration technology;
9. prevent recipes and prevalent implementations from becoming global requirements;
10. keep Kubernetes and container-runtime choices separate from endpoint baselines.

## Rootless Podman Rationale

Rootless Podman is preferred for applicable Linux profiles because ordinary container workloads can run without a persistent root-owned application daemon.

The preferred model provides:

- user-scoped runtime identity;
- reduced host privilege for ordinary service execution;
- OCI image and container compatibility;
- workspace and service namespacing;
- compatibility with bounded resource and network controls;
- explicit escalation only for operations that genuinely require host privilege;
- replacement of the runtime without redefining component contracts.

Rootless execution is not complete security by itself. Identity, authorization, data ownership, secret handling, network policy, storage identities, lifecycle verification, and receipts remain independent controls.

## Quadlet Rationale

Quadlet is preferred for sovereign Linux profile-managed container services because it provides a declarative bridge between Podman objects and systemd-managed lifecycle.

The intended benefits are:

- version-controlled service declarations;
- deterministic startup dependencies;
- integration with service readiness and restart behavior;
- explicit user or system service ownership;
- a clear mapping between profile configuration and running services;
- support for controlled deployment preparation and activation;
- operational inspection through the selected Linux service manager.

Quadlet files are implementation artifacts owned by an applicable profile or recipe layer. They do not define component business interfaces or canonical application behavior.

## Runtime-Independence Boundary

Application and component contracts describe observable behavior rather than runtime commands.

They can define:

- service identity;
- commands, queries, events, and artifacts;
- endpoints;
- volumes and owned data classes;
- resource requirements;
- health and readiness;
- lifecycle states;
- failure behavior;
- receipts and evidence.

They do not assume:

- Podman socket paths;
- Docker daemon behavior;
- Quadlet unit names;
- systemd-specific restart semantics;
- one container-network implementation;
- one storage driver;
- one image-builder product;
- privileged container access;
- Kubernetes availability.

A profile adapter or implementation recipe maps the portable contract to the selected runtime.

## Consequences

### Positive consequences

- Linux development receives a preferred rootless default.
- Sovereign Linux receives a coherent declarative service-management path.
- Windows/WSL retains Docker or Podman choice.
- Lightweight installations remain container-optional.
- Build farms can use any conformant OCI runtime.
- Application and component contracts remain portable.
- Runtime removal or replacement does not redefine canonical component behavior.
- Privileged host mutation remains separate from ordinary container execution.
- Profile conformance can test the exact runtime selected without promoting it globally.

### Costs and tradeoffs

- Implementations need adapters or recipes for more than one runtime.
- Runtime-specific diagnostics cannot be the only health or evidence interface.
- Quadlet and systemd behavior require sovereign-Linux-specific tests.
- Windows/WSL claims need explicit host and Linux boundary evidence.
- Rootless networking, storage, ports, and user-service lifecycle require deliberate configuration.
- Features available only in one runtime cannot enter portable contracts without a profile-scoped decision.
- Operational teams need migration paths between supported runtime implementations.

### Risks and controls

| Risk | Required control |
| --- | --- |
| Rootless operation is mistaken for complete isolation | Retain identity, authorization, network, storage, secret, and resource controls |
| Quadlet units become de facto component contracts | Keep units in profile or recipe ownership and validate portable interfaces separately |
| Runtime behavior leaks into application code | Contract and repository checks reject undeclared runtime dependencies |
| Windows/WSL behavior is inferred from Linux tests | Require separate profile claims and exact-boundary evidence |
| A recipe becomes normative by repetition | Enforce `LOCK-IMPL-001` and explicit profile adoption |
| Containers become mandatory for lightweight users | Validate the user-lightweight profile without container dependence |
| Runtime replacement breaks data ownership | Keep volumes and authoritative data under component-owned contracts |
| Rootful fallback becomes ordinary | Require explicit profile and privileged-operation authority |

## Alternatives Considered

### Universal Docker requirement

Rejected because it would impose one product and daemon model across Linux, Windows/WSL, lightweight, sovereign, build-farm, and control-plane profiles.

### Universal Podman requirement

Rejected because Windows/WSL permits Docker or Podman, build farms require OCI compatibility rather than one product, and lightweight profiles keep containers optional.

### Universal Kubernetes requirement

Rejected because Kubernetes is not an endpoint baseline and is justified only for profiles and scales that explicitly adopt it.

### Raw systemd units without container abstraction

Not selected as the preferred sovereign container path because it does not provide the same OCI packaging and runtime portability. Native system services remain possible where a component or profile selects them.

### Rootful container daemon as the default

Rejected as the preferred Linux baseline because ordinary application workloads should not require broad host privilege when rootless execution is viable.

### No preferred runtime

Rejected because Linux development and sovereign operations benefit from a documented default that can be tested, supported, and replaced through a controlled profile decision.

## Profile and Implementation Constraints

The decision preserves these constraints:

- profile-specific requirements remain profile-scoped;
- profile inheritance and overlays remain explicit;
- recipes remain non-normative unless adopted;
- Quadlet and systemd remain profile-scoped implementation choices;
- workspace mutable state remains namespaced;
- concurrent branches or applications remain collision-free;
- direct cross-component authoritative writes remain prohibited;
- Resource Governor remains separate from Governance Policy Runtime;
- artifacts retain runtime-independent identity;
- runtime selection does not create a release channel;
- an implementation change does not authorize an application action.

## Migration Guidance

unvalidated container and service material is classified before adoption.

Migration follows this order:

1. identify the source profile and intended target profile;
2. separate portable component behavior from runtime configuration;
3. move systemd and Quadlet examples into sovereign-Linux recipe or profile-owned locations;
4. create or validate portable service, endpoint, storage, resource, and lifecycle contracts;
5. adopt rootless Podman or another profile-approved runtime;
6. convert sovereign container services to Quadlet where the profile selects it;
7. validate identities, ports, networks, volumes, secrets, health, restart, shutdown, and recovery;
8. test removal and replacement of the runtime implementation;
9. preserve historical material as migration evidence rather than active authority.

A migration does not copy rootful or host-global assumptions into the active profile silently.

## Validation

Conformance evidence for this ADR includes:

1. the runtime matrix matches `DEC-CONTAINER-001`;
2. Linux-development tests cover the selected rootless runtime;
3. sovereign-Linux tests cover rootless Podman and Quadlet when adopted;
4. Windows/WSL tests identify Docker or Podman and preserve the host boundary;
5. user-lightweight tests prove containers are optional;
6. build-farm tests prove OCI compatibility;
7. application-contract tests reject undeclared runtime behavior;
8. recipe and profile checks enforce implementation scope;
9. parallel-workspace tests prove collision-free namespacing;
10. lifecycle tests cover start, readiness, stop, restart, failure, teardown, and recovery;
11. resource tests cover CPU, memory, I/O, process, queue, and concurrency limits;
12. security tests prove rootless execution does not replace authorization or data isolation;
13. release tests prove runtime configuration is packaged and activated through applicable artifact and profile contracts;
14. documentation tests reject global promotion of Quadlet, systemd, Podman, Docker, or Kubernetes.

Expected validation failure codes include:

```text
container_runtime_profile_scope_missing
container_runtime_matrix_mismatch
container_runtime_dependency_leaked
container_runtime_rootless_claim_unproven
container_runtime_quadlet_promoted_global
container_runtime_user_lightweight_mandatory
container_runtime_wsl_boundary_unresolved
container_runtime_oci_compatibility_failed
container_runtime_rootful_fallback_implicit
container_runtime_recipe_promoted_normative
container_runtime_lifecycle_unverified
container_runtime_replacement_unverified
```

## Supersession

This ADR remains active until an accepted successor changes `DEC-CONTAINER-001` or the profile-owned runtime matrix.

A successor must:

- preserve explicit profile scope;
- identify affected profiles and contracts;
- provide migration and rollback;
- update conformance tests and evidence;
- prevent runtime-specific behavior from entering portable application contracts implicitly;
- record supersession in the ADR registry.

Historical copies remain retained and the identifier `ADR-005` remains permanently reserved.
