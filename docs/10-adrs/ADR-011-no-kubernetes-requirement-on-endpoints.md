<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ADR-011",
  "document_class": "architecture_decision_record",
  "status": "active",
  "language": "en",
  "layer": "adrs",
  "adr_id": "ADR-011",
  "adr_status": "accepted",
  "decision_class": "major",
  "owner_decision_id": "DEC-K8S-001",
  "created_at": "2026-08-03",
  "accepted_at": "2026-08-03",
  "effective_at": "2026-08-03",
  "supersedes": [],
  "superseded_by": null,
  "scope": [
    "profile:developer_linux_workstation",
    "profile:developer_windows_wsl",
    "profile:user_lightweight",
    "profile:sovereign_linux_node",
    "overlay:appliance_shell",
    "endpoint_runtime"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json#/decisions/DEC-K8S-001",
    "generated/decision-index.json#/adrs/ADR-011",
    "contracts/terminology.contract.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/profiles/developer-linux-workstation.profile.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "contracts/profiles/user-lightweight.profile.json",
    "contracts/profiles/sovereign-linux-node.profile.json",
    "contracts/profiles/sovereign-hub.profile.json",
    "contracts/profiles/control-plane.profile.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-CONTAINER-001",
    "DEC-K8S-001",
    "DEC-PROFILE-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-CONF-SLN-033",
    "REQ-CONF-SLN-034",
    "REQ-CONF-SLN-035",
    "REQ-CONF-SLN-036",
    "REQ-CONF-SLN-037",
    "REQ-CONF-SLN-038",
    "REQ-CONF-SLN-039",
    "REQ-CONF-SLN-040",
    "REQ-LIFE-SVC-013",
    "REQ-LIFE-SVC-014",
    "REQ-LIFE-SVC-015",
    "REQ-LIFE-SVC-017",
    "REQ-LIFE-SVC-031",
    "REQ-LIFE-SVC-033",
    "REQ-LIFE-SVC-034",
    "REQ-LIFE-SVC-035",
    "REQ-LIFE-SVC-044",
    "REQ-OPS-JOB-032",
    "REQ-OPS-JOB-043",
    "REQ-OPS-JOB-054"
  ],
  "lock_ids": [
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-GOV-001",
    "LOCK-IMPL-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-002",
    "DOC-CONST-013",
    "DOC-SYS-017",
    "DOC-PROFILE-005",
    "DOC-LIFE-006",
    "DOC-OPS-006",
    "DOC-CONF-016",
    "DOC-ADR-001"
  ],
  "tags": [
    "adr",
    "kubernetes",
    "endpoints",
    "profiles",
    "containers",
    "orchestration",
    "sovereign-linux",
    "developer-workstation",
    "operational-complexity",
    "resource-efficiency"
  ]
}
KOA:DOC-META:END -->

# ADR-011 — No Kubernetes Requirement on Endpoints

| Field | Value |
| --- | --- |
| ADR | `ADR-011` |
| Owner decision | `DEC-K8S-001` |
| Status | Accepted |
| Decision class | Major |
| Accepted | 2026-08-03 |
| Effective | 2026-08-03 |
| Supersedes | None |
| Superseded by | None |

## 1. Context

kOA supports several deployment profiles with materially different operational needs.

Endpoint profiles include:

- `developer_linux_workstation`;
- `developer_windows_wsl`;
- `user_lightweight`;
- `sovereign_linux_node`;
- an endpoint composed with the `appliance_shell` overlay.

These profiles run on one user-controlled or operator-controlled machine and must preserve:

- bounded hardware requirements;
- offline-capable core operation where declared;
- simple recovery;
- local service control;
- explicit profile composition;
- component isolation;
- Resource Governor enforcement;
- deterministic lifecycle behavior;
- understandable diagnostics;
- credible removal and replacement of implementation mechanisms.

Kubernetes can provide useful orchestration at cluster scale, but it also introduces a control plane, API server, reconciliation loops, cluster identities, networking plugins, storage plugins, controllers, admission behavior, certificate and secret management, version-skew rules, and additional upgrade and recovery obligations.

Requiring those mechanisms on every endpoint would make a cluster-oriented operational model part of the endpoint baseline even when:

- there is only one node;
- the workload fits within local service management;
- high availability is not being provided by a cluster;
- Internet or remote control-plane availability cannot be assumed;
- the hardware envelope is intentionally bounded;
- the user or local operator must be able to recover the node without cluster expertise.

The architecture therefore needs a clear decision separating endpoint execution from optional cluster orchestration.

## 2. Decision

kOA shall not require Kubernetes for endpoint profiles.

An endpoint shall remain conformant without:

- a Kubernetes control plane;
- a Kubernetes API server;
- `kubelet`;
- `etcd`;
- a container network interface plugin;
- a container storage interface plugin;
- an ingress controller;
- a service mesh;
- Kubernetes operators or custom resource definitions;
- Helm;
- a remote cluster-management service;
- Kubernetes-specific identity, secret, policy, or deployment authority.

Endpoint components and services shall use the execution and service-management mechanisms explicitly selected by the active profile.

Those mechanisms can include:

- native user or system services;
- rootless containers;
- rootless Podman;
- Quadlet;
- a profile-selected service manager;
- task-activated processes;
- local queues and workers;
- WSL-compatible process or container execution;
- another declared endpoint adapter.

Kubernetes may be used by a non-endpoint profile such as a measured-scale `sovereign_hub` or `control_plane` only when that profile explicitly adopts it and owns the resulting topology, resource, identity, storage, network, lifecycle, recovery, and conformance requirements.

Kubernetes presence on an endpoint does not establish kOA authority, profile conformance, service readiness, or release compatibility.

## 3. Decision Scope

### 3.1 Endpoint profiles

This decision applies to:

| Profile or overlay | Interpretation |
| --- | --- |
| `developer_linux_workstation` | Local development must not require a cluster |
| `developer_windows_wsl` | WSL development must not require a cluster |
| `user_lightweight` | User-facing endpoint must not carry cluster obligations |
| `sovereign_linux_node` | Sovereign production endpoint must remain locally operable without Kubernetes |
| `appliance_shell` | Restricted shell behavior does not introduce Kubernetes |

A profile version can explicitly permit Kubernetes as an optional non-authoritative development or testing tool, but the endpoint profile's required capabilities shall continue to work without it.

### 3.2 Non-endpoint profiles

This ADR does not prohibit Kubernetes in:

- `sovereign_hub`;
- `control_plane`;
- a specialized build or validation environment;
- another future cluster profile.

Such use requires explicit profile adoption and does not create an endpoint requirement.

### 3.3 Included Kubernetes dependencies

The prohibition on an endpoint requirement covers direct and indirect dependencies on:

- Kubernetes resource APIs;
- controllers and operators;
- cluster DNS;
- cluster service discovery;
- Kubernetes secrets;
- Kubernetes persistent volumes;
- Kubernetes network policies;
- Kubernetes ingress;
- Kubernetes admission controllers;
- Kubernetes scheduler decisions;
- cluster-only health or readiness state;
- Kubernetes-specific deployment manifests as the sole executable specification;
- remote cluster control as the sole operational path.

### 3.4 Excluded decisions

This ADR does not select one universal endpoint runtime.

It does not decide:

- one container engine;
- one service manager;
- whether containers are mandatory;
- whether an endpoint uses virtual machines;
- one Linux distribution;
- one Windows or WSL version;
- one network namespace implementation;
- one local queue implementation;
- one storage backend.

Those decisions remain profile- and component-specific.

## 4. Definitions and Interpretation

### 4.1 Endpoint

An **endpoint** is a user-facing or node-local deployment in which the active profile expects one machine to provide its declared capabilities without depending on cluster membership.

An endpoint can communicate with other systems. It is not required to be isolated or standalone in every mode.

The defining property is that the profile's required local capability and recovery model do not depend on Kubernetes.

### 4.2 Kubernetes requirement

A **Kubernetes requirement** exists when a declared endpoint capability cannot be installed, started, operated, updated, observed, recovered, backed up, restored, or removed without Kubernetes or a Kubernetes-specific control path.

Optional compatibility with Kubernetes is not a requirement when a complete conformant non-Kubernetes path remains available.

### 4.3 Local orchestration

**Local orchestration** coordinates processes, services, containers, jobs, dependencies, health, resources, and recovery on one endpoint under its active profile.

Local orchestration can use multiple mechanisms but shall expose one coherent profile-owned operational model.

### 4.4 Cluster profile

A **cluster profile** explicitly owns multi-node scheduling, cluster membership, control-plane quorum, distributed networking, distributed storage, version skew, placement, and cluster recovery.

A set of endpoints connected to the same network does not automatically become a cluster profile.

### 4.5 Kubernetes-compatible artifact

A Kubernetes manifest or chart can be a deployment projection for a profile that adopts Kubernetes.

It is not the canonical owner of:

- component responsibility;
- component data ownership;
- profile composition;
- resource-policy authority;
- governance-policy authority;
- release-channel identity;
- Release Set compatibility.

## 5. Rationale

### 5.1 Endpoint resource efficiency

A bounded endpoint should spend CPU, memory, storage, and operational capacity on declared kOA capabilities rather than a cluster control plane that provides no required endpoint-scale property.

This is particularly important for:

- `user_lightweight`;
- `sovereign_linux_node`;
- developer machines running parallel workspaces;
- disconnected or resource-constrained environments.

### 5.2 Operational simplicity

Endpoint operators must be able to:

- understand service state;
- identify exact artifacts;
- recover failed services;
- inspect resource pressure;
- restore backups;
- rotate credentials;
- perform updates;
- use break-glass procedures where permitted.

Requiring Kubernetes would add another operational authority surface and failure model to every endpoint.

### 5.3 Offline and sovereign operation

A sovereign endpoint must not rely on:

- a remote Kubernetes control plane;
- a cloud-managed Kubernetes service;
- an external container registry at runtime;
- remote cluster admission;
- remote cluster identity;
- a remote operator reconciliation service.

Local Kubernetes can run offline, but it still introduces cluster infrastructure that is unnecessary for the endpoint baseline.

### 5.4 Profile integrity

Profiles define exact composition.

Kubernetes should appear only where the profile accepts its implications rather than entering indirectly through a component recipe, container chart, vendor package, or operator assumption.

### 5.5 Component portability

Components should expose profile-neutral contracts.

A component can be deployed as:

- a local process;
- a system service;
- a rootless container;
- a task-activated worker;
- a Kubernetes workload under a cluster profile.

The component contract remains stable while profile adapters supply deployment-specific behavior.

### 5.6 Recovery clarity

Endpoint recovery should not require restoring a cluster control plane before local component recovery can begin.

The active profile can recover services, artifacts, data, queues, identities, and Release Set state through its local lifecycle contracts.

### 5.7 Avoidance of false high availability

Installing Kubernetes on one node does not create meaningful node-level high availability.

A single-node cluster can increase complexity while retaining the same hardware, power, storage, and physical failure domain.

High availability shall be claimed only by a profile that defines and tests its actual topology and failure domains.

## 6. Required Decision Rules

### 6.1 Endpoint capability rule

Every required endpoint capability shall have a complete non-Kubernetes execution path covering:

1. installation or artifact admission;
2. configuration;
3. secret references;
4. service startup;
5. readiness;
6. resource enforcement;
7. logging and bounded diagnostics;
8. update and atomic activation;
9. rollback or forward repair;
10. backup and restore where applicable;
11. degraded operation;
12. removal.

### 6.2 Component packaging rule

A component may provide Kubernetes deployment projections.

It shall also provide, directly or through the applicable profile, the non-Kubernetes endpoint packaging required by every endpoint profile that includes it.

Kubernetes-only packaging cannot satisfy endpoint profile inclusion.

### 6.3 Service discovery rule

Required endpoint services shall not depend solely on Kubernetes DNS, Services, EndpointSlices, ingress, or cluster-only discovery.

The active endpoint profile shall define local discovery and routing.

### 6.4 Storage rule

Required endpoint data shall not depend solely on Kubernetes persistent volumes, storage classes, or CSI controllers.

Storage shall remain owned by the component and mapped through profile-declared local storage boundaries.

### 6.5 Secret and identity rule

Required endpoint secrets and identities shall not depend solely on Kubernetes Secret objects, service accounts, admission webhooks, or cluster certificate authorities.

The active profile shall supply the canonical identity and secret mechanisms.

### 6.6 Resource rule

Resource Governor remains authoritative for kOA workload admission and resource envelopes.

A Kubernetes scheduler, request, limit, quota, priority class, or eviction result can implement part of a cluster profile's enforcement but shall not replace Resource Governor's canonical policy or authority.

On endpoints, Resource Governor shall use the profile-selected local adapters.

### 6.7 Lifecycle rule

A Kubernetes rollout status is not sufficient evidence of kOA service activation.

Every profile shall preserve:

- artifact verification;
- component-specific drain;
- migration coordination;
- readiness;
- post-activation capability verification;
- atomic authoritative routing;
- receipts;
- rollback or forward repair.

### 6.8 Optional endpoint Kubernetes rule

When an endpoint profile permits optional Kubernetes for development, compatibility testing, or local experimentation:

- it shall be outside the required endpoint capability path;
- its absence shall not make the endpoint nonconformant;
- it shall not own authoritative production data by default;
- it shall not change the endpoint's canonical profile composition;
- it shall remain within the endpoint's resource and security boundaries;
- it shall be removable without losing the endpoint's required capabilities or authoritative state.

### 6.9 Cluster adoption rule

A profile adopting Kubernetes shall declare:

- control-plane topology;
- node and workload identities;
- Kubernetes version and support policy;
- API and extension compatibility;
- CNI and CSI dependencies;
- ingress and service-discovery model;
- cluster secret and certificate behavior;
- Resource Governor integration;
- Governance Policy Runtime integration;
- storage ownership;
- backup and restore;
- cluster upgrades;
- version skew;
- quorum and disaster recovery;
- disconnected operation where required;
- conformance evidence.

## 7. Consequences

### 7.1 Positive consequences

- Endpoint hardware and operational overhead remain bounded.
- Required capabilities can operate without cluster infrastructure.
- Sovereign and offline recovery remains locally understandable.
- Component contracts remain portable across endpoint and cluster profiles.
- Kubernetes cannot silently become the owner of kOA policy, identity, data, or releases.
- Endpoint installation and troubleshooting require fewer infrastructure layers.
- Single-node deployments do not claim false high availability.
- Kubernetes can still be adopted where measured scale justifies it.

### 7.2 Costs and constraints

- Components included in both endpoint and cluster profiles may require more than one deployment adapter.
- Endpoint service lifecycle must be implemented without relying solely on Kubernetes reconciliation.
- Local service discovery, routing, secret delivery, and health behavior must be defined by endpoint profiles.
- Teams cannot assume that a Helm chart is the complete product deployment contract.
- Cluster-specific observability and policy abstractions must be translated rather than treated as canonical.
- Testing must cover endpoint and cluster deployment projections separately when both are supported.

### 7.3 Operational consequences

Endpoint operations shall document the actual local mechanism for:

- process and service control;
- containers where used;
- resource enforcement;
- startup ordering;
- readiness;
- routing;
- queues and jobs;
- storage;
- secrets;
- updates;
- recovery.

Cluster operations shall document the additional Kubernetes-specific mechanisms without exporting them as endpoint requirements.

## 8. Alternatives Considered

### 8.1 Require Kubernetes everywhere

**Rejected.**

It would impose cluster complexity, resource use, operational skill, upgrade coupling, and recovery dependencies on profiles that do not need cluster scheduling or quorum.

### 8.2 Require a lightweight Kubernetes distribution on endpoints

**Rejected as a baseline.**

Reducing installation size does not remove the Kubernetes API, control-plane state, networking, storage, certificates, reconciliation, versioning, and recovery obligations.

A profile may permit such a distribution as an optional tool, but not as the required endpoint foundation.

### 8.3 Require single-node Kubernetes for consistency with hubs

**Rejected.**

Deployment-mechanism consistency is less important than preserving the correct profile boundary.

Component contracts and artifact identities provide architectural consistency without requiring the same orchestrator.

### 8.4 Prohibit Kubernetes throughout kOA

**Rejected.**

Measured-scale hubs and control planes can benefit from cluster scheduling, replacement, topology management, and distributed operations.

The correct boundary is explicit profile adoption rather than a global prohibition.

### 8.5 Use Kubernetes as the canonical configuration model but not the runtime

**Rejected.**

Kubernetes objects would still import Kubernetes-specific semantics into endpoint identity, lifecycle, storage, networking, and policy.

Canonical component and profile contracts remain runtime-neutral.

### 8.6 Allow components to choose Kubernetes independently

**Rejected.**

Component-selected orchestration would bypass profile composition and could introduce undeclared infrastructure, network, storage, identity, and recovery requirements.

Deployment mechanisms belong to profiles.

### 8.7 Treat containers as requiring Kubernetes

**Rejected.**

Containers can be executed and managed locally through rootless or system-level runtimes without a Kubernetes control plane.

## 9. Security, Lifecycle, and Profile Implications

### 9.1 Security boundary

Removing Kubernetes from the endpoint baseline reduces the number of required privileged daemons, APIs, certificates, controllers, and network surfaces.

The endpoint profile still defines:

- container and process isolation;
- least privilege;
- service identities;
- secret handling;
- network exposure;
- storage boundaries;
- privileged brokers;
- audit and receipts.

Absence of Kubernetes does not weaken those controls.

### 9.2 Supply chain

Kubernetes manifests, Helm charts, operators, container images, and cluster extensions are software supply-chain objects when a profile adopts them.

They require the same source, dependency, SBOM, provenance, signature, admission, vulnerability, revocation, and release controls as other deployable software.

Endpoint conformance does not require these artifacts unless the endpoint profile explicitly includes an optional Kubernetes mode.

### 9.3 Release channels

Kubernetes deployment projections do not create a release channel.

Executable services remain in `services`.

System-level Kubernetes packages or node images belong to `system`.

Policy artifacts belong to `governance`.

Knowledge artifacts belong to `knowledge`.

A Release Set binds compatible versions when Kubernetes is part of an adopting profile.

### 9.4 Service updates

Endpoint service updates follow the local profile's service lifecycle.

A cluster profile can implement rolling, canary, or blue-green strategies through Kubernetes only when the component contract declares mixed-version, data, drain, readiness, rollback, and forward-repair behavior.

A Kubernetes Deployment strategy does not establish those properties by itself.

### 9.5 Resource governance

On endpoints, Resource Governor uses profile-selected local enforcement.

In a Kubernetes profile, Kubernetes resource mechanisms can act as enforcement adapters, but canonical workload classes, priority, admission, and envelopes remain owned by Resource Governor.

### 9.6 Governance and identity

Kubernetes RBAC, admission policy, service accounts, and secrets can implement cluster-profile mechanisms.

They do not replace Identity and Trust or Governance Policy Runtime as canonical authorities.

### 9.7 Data ownership

Kubernetes controllers, operators, jobs, sidecars, init containers, backup tools, and storage plugins shall not write directly into another component's authoritative data outside owner-approved interfaces.

## 10. Conformance and Evidence

Endpoint conformance shall verify the absence of a Kubernetes dependency rather than merely the absence of installed Kubernetes packages.

Required conclusions include:

| Evidence area | Required conclusion |
| --- | --- |
| Profile composition | Kubernetes is not a required endpoint capability |
| Cold installation | Required endpoint capabilities install without a Kubernetes cluster |
| Startup | Required services start without Kubernetes APIs or controllers |
| Identity | Node, service, workload, and operator identities resolve without Kubernetes authority |
| Secrets | Required secrets are delivered without Kubernetes Secret dependency |
| Networking | Required discovery and routing work without cluster DNS, Service, or ingress |
| Storage | Authoritative storage works without PVC, storage class, or CSI dependency |
| Resource governance | Resource Governor enforces the endpoint envelope through local adapters |
| Service lifecycle | Update, drain, readiness, activation, rollback, and forward repair work locally |
| Offline behavior | Declared offline core operates without remote cluster control |
| Recovery | Endpoint recovery does not require restoring Kubernetes state |
| Removal | Optional Kubernetes can be removed without loss of required capability or authoritative state |
| Component boundaries | Deployment projections do not redefine component ownership |
| Release compatibility | Exact endpoint artifacts belong to a compatible Release Set |
| Negative dependency test | Loss or absence of every Kubernetes-specific interface does not break required endpoint capabilities |

The following fail endpoint conformance:

- a required service can run only as a Kubernetes workload;
- a required secret exists only as a Kubernetes Secret;
- a required data store depends only on a persistent-volume claim;
- required routing depends only on Kubernetes ingress or Service objects;
- required identity depends only on Kubernetes service accounts;
- endpoint update or recovery requires a Kubernetes API;
- a component chart introduces undeclared profile infrastructure;
- optional Kubernetes owns the only copy of authoritative endpoint data;
- Kubernetes absence causes the sovereign core to fail.

Cluster-profile conformance remains separate and shall test its declared Kubernetes topology and operations.

## 11. Decision Closure, Review, and Supersession

### 11.1 Closed decisions

This ADR closes the following questions:

- Kubernetes is not required on endpoint profiles.
- Endpoint required capabilities have complete non-Kubernetes operational paths.
- Components do not select orchestration independently of profiles.
- Kubernetes can be adopted only by explicit profiles.
- Rootless containers and local service management remain valid endpoint mechanisms.
- Kubernetes status does not replace kOA readiness or activation verification.
- Resource Governor, Governance Policy Runtime, Identity and Trust, and component ownership remain canonical.
- Kubernetes is not prohibited from measured-scale hubs or control planes.
- Kubernetes presence does not create conformance.

### 11.2 Prohibited assumptions

This ADR shall not be interpreted to mean:

- containers are prohibited on endpoints;
- every endpoint must use Podman, Quadlet, or systemd;
- Kubernetes can never be installed on a developer machine;
- a sovereign hub cannot use Kubernetes;
- a control plane must use Kubernetes;
- local process management is inherently less secure;
- absence of Kubernetes proves endpoint conformance;
- one Helm chart is a component contract;
- Kubernetes requests and limits are the Resource Governor contract;
- Kubernetes RBAC is the Governance Policy Runtime;
- Kubernetes Secrets are the canonical identity or secret store;
- a single-node Kubernetes installation provides node high availability;
- an exception can make Kubernetes a permanent endpoint baseline without a new profile decision.

### 11.3 Review triggers

This ADR shall be reviewed when:

- an endpoint requirement cannot be implemented safely without cluster orchestration;
- endpoint profiles evolve into explicit multi-node profiles;
- a Kubernetes implementation eliminates the material control-plane and recovery burden relevant to this decision;
- a new profile boundary changes the definition of endpoint;
- conformance evidence shows that non-Kubernetes endpoint adapters create unacceptable inconsistency or risk;
- Kubernetes becomes necessary for a required external platform integration and no portable adapter is feasible.

### 11.4 Supersession condition

Supersession requires a new accepted ADR that:

- identifies this ADR;
- defines the endpoint or replacement profile boundary;
- explains why Kubernetes is required rather than merely convenient;
- specifies resource, identity, governance, storage, network, lifecycle, offline, recovery, and supply-chain behavior;
- provides complete migration and credible-exit plans;
- updates `DEC-K8S-001`, profile contracts, tests, and conformance matrices.

Until superseded, this ADR remains the controlling rationale for `DEC-K8S-001`.
