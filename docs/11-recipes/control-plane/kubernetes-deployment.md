<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-RECIPE-CP-001",
  "document_class": "recipe",
  "status": "active",
  "language": "en",
  "layer": "implementation_recipe",
  "recipe_id": "RECIPE-CP-001",
  "recipe_version": "1.0.0",
  "scope": [
    "profile:control_plane",
    "kubernetes_deployment",
    "cluster_scoped_service_activation",
    "release_set_deployment"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "generated/document-index.json",
    "contracts/terminology.contract.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "contracts/profiles/control-plane.profile.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "contracts/artifact-contracts/integration-manifest.schema.json",
    "schemas/deployment-profile.schema.json",
    "schemas/test-evidence.schema.json"
  ],
  "decision_ids": [
    "DEC-CONTAINER-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-K8S-001",
    "DEC-PROFILE-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-LIFE-SVC-001",
    "REQ-LIFE-SVC-002",
    "REQ-LIFE-SVC-003",
    "REQ-LIFE-SVC-004",
    "REQ-LIFE-SVC-005",
    "REQ-LIFE-SVC-006",
    "REQ-LIFE-SVC-007",
    "REQ-LIFE-SVC-008",
    "REQ-LIFE-SVC-009",
    "REQ-LIFE-SVC-010",
    "REQ-LIFE-SVC-011",
    "REQ-LIFE-SVC-012",
    "REQ-LIFE-SVC-013",
    "REQ-LIFE-SVC-014",
    "REQ-LIFE-SVC-015",
    "REQ-LIFE-SVC-016",
    "REQ-LIFE-SVC-017",
    "REQ-LIFE-SVC-018",
    "REQ-LIFE-SVC-019",
    "REQ-LIFE-SVC-020",
    "REQ-LIFE-SVC-021",
    "REQ-LIFE-SVC-022",
    "REQ-LIFE-SVC-023",
    "REQ-LIFE-SVC-024",
    "REQ-LIFE-SVC-025",
    "REQ-LIFE-SVC-026",
    "REQ-LIFE-SVC-027",
    "REQ-LIFE-SVC-028",
    "REQ-LIFE-SVC-029",
    "REQ-LIFE-SVC-030",
    "REQ-LIFE-SVC-031",
    "REQ-LIFE-SVC-032",
    "REQ-LIFE-SVC-033",
    "REQ-LIFE-SVC-034",
    "REQ-LIFE-SVC-035",
    "REQ-LIFE-SVC-036",
    "REQ-LIFE-SVC-037",
    "REQ-LIFE-SVC-038",
    "REQ-LIFE-SVC-039",
    "REQ-LIFE-SVC-040",
    "REQ-LIFE-SVC-041",
    "REQ-LIFE-SVC-042",
    "REQ-LIFE-SVC-043",
    "REQ-LIFE-SVC-044",
    "REQ-LIFE-SVC-045",
    "REQ-LIFE-SVC-046",
    "REQ-LIFE-SVC-047",
    "REQ-LIFE-SVC-048",
    "REQ-LIFE-SVC-049",
    "REQ-LIFE-SVC-050",
    "REQ-LIFE-SVC-051",
    "REQ-LIFE-SVC-052",
    "REQ-OPS-JOB-001",
    "REQ-OPS-JOB-003",
    "REQ-OPS-JOB-004",
    "REQ-OPS-JOB-012",
    "REQ-OPS-JOB-013",
    "REQ-OPS-JOB-032",
    "REQ-OPS-JOB-033",
    "REQ-OPS-JOB-034",
    "REQ-OPS-JOB-040",
    "REQ-OPS-JOB-041",
    "REQ-OPS-JOB-043",
    "REQ-OPS-JOB-044",
    "REQ-OPS-JOB-045",
    "REQ-OPS-JOB-048",
    "REQ-OPS-JOB-049",
    "REQ-OPS-JOB-051",
    "REQ-OPS-JOB-052",
    "REQ-OPS-JOB-053",
    "REQ-OPS-JOB-054",
    "REQ-SEC-SC-017",
    "REQ-SEC-SC-020",
    "REQ-SEC-SC-021",
    "REQ-SEC-SC-022",
    "REQ-SEC-SC-023",
    "REQ-SEC-SC-024",
    "REQ-SEC-SC-028",
    "REQ-SEC-SC-030",
    "REQ-SEC-SC-031",
    "REQ-SEC-SC-032",
    "REQ-SEC-SC-033",
    "REQ-SEC-SC-034",
    "REQ-SEC-SC-035",
    "REQ-SEC-SC-036",
    "REQ-SEC-SC-037",
    "REQ-SEC-SC-038",
    "REQ-SEC-SC-039",
    "REQ-SEC-SC-040",
    "REQ-SEC-SC-041",
    "REQ-SEC-SC-042",
    "REQ-SEC-SC-043",
    "REQ-SEC-SC-044",
    "REQ-SEC-SC-045",
    "REQ-SEC-SC-048",
    "REQ-SEC-SC-049",
    "REQ-SEC-SC-050",
    "REQ-SEC-SC-051",
    "REQ-SEC-SC-052",
    "REQ-SEC-SC-053",
    "REQ-SEC-SC-054",
    "REQ-SEC-SC-055",
    "REQ-SEC-SC-056"
  ],
  "lock_ids": [
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-DOC-003",
    "LOCK-DOC-004",
    "LOCK-GOV-001",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-SEC-010"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-002",
    "DOC-CONST-013",
    "DOC-SYS-017",
    "DOC-DEV-013",
    "DOC-LIFE-006",
    "DOC-LIFE-016",
    "DOC-SEC-009",
    "DOC-SEC-019",
    "DOC-OPS-006",
    "DOC-OPS-016",
    "DOC-CONF-005",
    "DOC-ADR-001",
    "DOC-ADR-011",
    "DOC-ADR-024"
  ],
  "tags": [
    "recipe",
    "control-plane",
    "kubernetes",
    "deployment",
    "server-side-apply",
    "release-set",
    "resource-governor",
    "governance-policy-runtime",
    "network-policy",
    "service-updates",
    "offline",
    "non-normative"
  ]
}
KOA:DOC-META:END -->

# Control-Plane Kubernetes Deployment

> **Recipe status:** Active, non-normative implementation recipe.  
> **Implementation:** Deploy verified Kubernetes projections into a profile-admitted cluster by server-side validation, staged apply, capability verification, and explicit authoritative-route activation.  
> **Authority rule:** Kubernetes is an enforcement and orchestration adapter for the `control_plane` profile. It does not become the canonical owner of kOA components, policy, identities, data, resources, releases, or conformance.

---

## Recipe Identity

| Field | Value |
| --- | --- |
| Recipe ID | `RECIPE-CP-001` |
| Title | Control-Plane Kubernetes Deployment |
| Status | Active |
| Version | `1.0.0` |
| Owner | Control-Plane Operations |
| Last reviewed | 2026-08-03 |
| Applies to profile | `control_plane` |
| Applies to components | Components explicitly included by the active control-plane profile |
| Deployment mechanism | Profile-admitted Kubernetes cluster |
| Supersedes | None |
| Replaced by | None |

---

## 1. Purpose

This recipe deploys one exact kOA Release Set into an already admitted Kubernetes cluster selected by the `control_plane` profile.

It covers:

- cluster identity and profile validation;
- local verification of deployment projections;
- exact image and artifact identity;
- namespace and service-account boundaries;
- network and storage policy;
- resource-envelope projection;
- staged server-side apply;
- database or owner-data migration coordination;
- readiness and representative capability tests;
- explicit authoritative-route activation;
- rollback or forward repair;
- evidence registration;
- connected and disconnected operation.

Successful execution produces:

```text
admitted cluster
→ verified Release Set
→ validated deployment projections
→ staged Kubernetes resources
→ ready component instances
→ representative capability verification
→ explicit authoritative-route activation
→ registered deployment evidence
```

This recipe does not install Kubernetes or create a cluster.

## 2. Non-Normative Status

This recipe is one implementation of the active control-plane profile.

It is not the canonical owner of:

- component responsibilities;
- profile composition;
- Kubernetes version and support policy;
- cluster topology;
- node identities;
- component data;
- Resource Governor envelopes;
- Governance Policy Runtime decisions;
- release-channel identities;
- Release Set compatibility;
- service migration semantics;
- rollback or forward-repair safety;
- test definitions or evidence.

The active profile must explicitly adopt Kubernetes.

A control plane using another admitted mechanism follows its own recipe.

This recipe shall not be used to introduce Kubernetes into:

- `developer_linux_workstation`;
- `developer_windows_wsl`;
- `user_lightweight`;
- `sovereign_linux_node`;
- `appliance_shell`.

Those endpoint profiles remain governed by `ADR-011`.

## 3. Scope

### 3.1 Included

This recipe covers Kubernetes resources that project active kOA contracts, including:

- namespaces;
- service accounts;
- workload controllers;
- Services;
- internal routing resources;
- ConfigMaps containing non-secret configuration;
- secret references;
- NetworkPolicies;
- persistent-volume claims when explicitly selected by the profile;
- jobs and migrations;
- resource requests and limits;
- disruption and availability controls;
- health probes;
- autoscaling when explicitly declared;
- admission-policy projections;
- monitoring and evidence references.

### 3.2 Excluded

This recipe does not:

- bootstrap or upgrade the Kubernetes control plane;
- initialize or restore cluster consensus state;
- select a CNI, CSI, ingress implementation, or service mesh;
- issue cluster certificates;
- create canonical component secrets;
- create production signing keys;
- create component databases or schemas outside owner migrations;
- define a Kubernetes version;
- choose a managed Kubernetes provider;
- migrate from a non-Kubernetes deployment;
- destroy a cluster;
- delete persistent volumes;
- change component data ownership;
- make Kubernetes RBAC the canonical governance model.

### 3.3 Deployment unit

The deployment unit is the exact service activation group declared by the Release Set and component lifecycle contracts.

A Kubernetes namespace is not automatically an activation unit.

A Helm release, Kustomize directory, Deployment, StatefulSet, or operator custom resource is not automatically an activation unit.

### 3.4 Supported operating modes

| Mode | Description |
| --- | --- |
| Connected | Cluster can reach admitted internal artifact and evidence services |
| Disconnected | Cluster uses locally mirrored admitted artifacts, trust material, policy, schemas, and test tools |
| Staged | New resources exist but authoritative routing remains on the prior verified release |
| Active | The new release passed required capability verification and routing activation |
| Restoring | Cluster and component state are being reconciled after failure |

## 4. Canonical References

### 4.1 Primary decisions

- `DEC-K8S-001`
- `DEC-CONTAINER-001`
- `DEC-DATA-001`
- `DEC-GOV-001`
- `DEC-PROFILE-001`
- `DEC-REL-001`

### 4.2 Primary architecture records

- `docs/10-adrs/ADR-011-no-kubernetes-requirement-on-endpoints.md`
- `docs/10-adrs/ADR-024-logical-data-ownership-with-profile-dependent-physical-isolation.md`

### 4.3 Primary lifecycle and operations documents

- `docs/06-lifecycle/06-service-updates.md`
- `docs/06-lifecycle/16-forward-repair.md`
- `docs/08-operations/06-job-scheduling.md`
- `docs/08-operations/16-break-glass.md`

### 4.4 Primary security and evidence documents

- `docs/07-security/09-storage-boundaries.md`
- `docs/07-security/19-software-supply-chain.md`
- `docs/09-conformance/05-test-evidence.md`

### 4.5 Authority mapping

| Kubernetes mechanism | Canonical kOA authority |
| --- | --- |
| Namespace and workload labels | Deployment projection of profile and component identity |
| ServiceAccount | Runtime credential binding from Identity and Trust |
| RBAC | Profile-scoped enforcement adapter; not Governance Policy Runtime |
| Resource requests and limits | Enforcement projection of Resource Governor envelopes |
| NetworkPolicy | Enforcement projection of declared network boundaries |
| Secret reference | Delivery adapter for an already authorized secret |
| ConfigMap | Non-secret configuration projection |
| Deployment strategy | Lifecycle adapter subject to component update contract |
| PersistentVolumeClaim | Storage projection subject to component data ownership |
| Scheduler placement | Cluster adapter subject to profile and Resource Governor constraints |
| Admission controller | Enforcement adapter for declared security and governance rules |
| Kubernetes status | Operational observation, not canonical component readiness by itself |

## 5. Preconditions

### 5.1 Profile preconditions

Before execution:

- `control_plane` profile and version resolve;
- the profile explicitly adopts Kubernetes;
- the exact cluster topology and support policy resolve;
- CNI, CSI, ingress, DNS, time, identity, certificate, backup, and disaster-recovery mechanisms resolve;
- required cluster and workload identities resolve;
- every included component contract resolves;
- every required integration manifest resolves;
- every active exception is exact-scope and unexpired;
- the active Release Set resolves across all four channels.

Missing authority produces `blocked`.

### 5.2 Cluster preconditions

The cluster is already admitted and healthy enough for deployment.

Required checks:

```bash
set -euo pipefail
set +x

: "${KUBECONFIG:?KUBECONFIG must reference the admitted control-plane cluster}"
: "${KUBE_CONTEXT:?KUBE_CONTEXT must identify the admitted cluster context}"

kubectl --context "$KUBE_CONTEXT" cluster-info
kubectl --context "$KUBE_CONTEXT" get --raw='/readyz'
kubectl --context "$KUBE_CONTEXT" get nodes
```

The deployment authority verifies that:

- returned cluster identity matches the profile;
- every required control-plane and worker node identity is admitted;
- required API extensions are present;
- cluster time and certificate validity are acceptable;
- storage and network adapters are healthy;
- no unresolved restoring or split-brain condition exists.

### 5.3 Release inputs

Required variables:

```bash
: "${RELEASE_SET_ID:?RELEASE_SET_ID must be set}"
: "${RELEASE_SET_VERSION:?RELEASE_SET_VERSION must be set}"
: "${RELEASE_BUNDLE_ROOT:?RELEASE_BUNDLE_ROOT must be set}"
: "${DEPLOYMENT_PROJECTION_ROOT:?DEPLOYMENT_PROJECTION_ROOT must be set}"
```

`RELEASE_BUNDLE_ROOT` contains the admitted Release Set, artifacts, evidence, and trust material.

`DEPLOYMENT_PROJECTION_ROOT` contains the Kubernetes projection generated from the active contracts.

### 5.4 Tool preconditions

Required tools are selected and versioned by the profile or deployment toolchain.

This recipe uses these command names without defining versions:

```bash
command -v kubectl
command -v python3
command -v find
command -v sort
command -v sha256sum
```

`sha256sum` is used only for intrinsic artifact and manifest integrity checks.

### 5.5 Write authority

The deployment identity has:

- read access to cluster state required for preflight;
- bounded server-side apply rights for declared namespaces and resource kinds;
- no general component-data write authority;
- no production signing-key access;
- no permission to modify unrelated namespaces;
- no permission to bypass admission enforcement;
- explicit permission for route activation when it is a separate operation.

## 6. Inputs and Outputs

### 6.1 Inputs

| Input | Canonical source | Required |
| --- | --- | ---: |
| Cluster identity and context | Control-plane profile | Yes |
| Release Set ID and version | Release authority | Yes |
| Kubernetes projection | Profile and component deployment projections | Yes |
| Exact image digests | Services-channel artifacts | Yes |
| System dependencies | System-channel release | Yes |
| Policy and resource envelopes | Governance-channel release | Yes |
| Knowledge dependencies | Knowledge-channel release | Conditional |
| Component data migrations | Owning component lifecycle | Conditional |
| Secret references | Identity and Trust and component contracts | Conditional |
| Test matrix | Test-catalog and traceability registries | Yes |
| Exceptions | Exceptions registry | Conditional |

### 6.2 Outputs

| Output | Description | Authority effect |
| --- | --- | --- |
| Applied Kubernetes objects | Deployment projection | No independent canonical authority |
| Staged component instances | Candidate runtime instances | Non-authoritative until activation |
| Migration results | Owner-controlled schema or data transitions | Component authority |
| Readiness and capability results | Deployment evidence | Supports activation decision |
| Route activation | Switch to verified service instances | Lifecycle authority |
| Deployment receipts | Immutable transition evidence | Audit and evidence authority |
| Rollback or forward-repair result | Recovery transition | Lifecycle authority |

### 6.3 Required projection inventory

The projection root contains a machine-readable inventory identifying:

- profile and version;
- Release Set ID and version;
- namespace set;
- component IDs and versions;
- exact container images by digest;
- Kubernetes resource files;
- expected resource kinds;
- required CRDs or API extensions;
- policy and envelope references;
- migration and activation groups;
- test IDs;
- rollback and forward-repair references.

The inventory format remains owned by the active deployment-projection contract.

## 7. Safety and Security Boundaries

### 7.1 Context safety

Every `kubectl` command in this recipe includes:

```text
--context "$KUBE_CONTEXT"
```

Do not rely on the current default context.

Before every mutation, print and verify:

```bash
kubectl --context "$KUBE_CONTEXT" config current-context
kubectl --context "$KUBE_CONTEXT" get namespace
```

### 7.2 Namespace boundary

Each profile-declared namespace has:

- stable identity;
- owner;
- allowed component set;
- allowed service accounts;
- default-deny network posture where the profile requires it;
- resource and storage boundaries;
- evidence and lifecycle classification.

A namespace does not become a component owner.

### 7.3 Secret boundary

This recipe applies secret references but does not create or display secret values.

Do not use:

```text
kubectl create secret --from-literal
kubectl set env with a secret value
inline Secret manifests containing plaintext values
shell variables containing secret values
```

The profile-approved secret-delivery adapter supplies references or encrypted sealed material according to its contract.

### 7.4 Data ownership boundary

Kubernetes workloads, init containers, operators, Jobs, sidecars, backup tools, CSI drivers, and deployment controllers shall not write directly into another component's authoritative store.

A migration Job runs under the owning component's identity and approved migration interface.

### 7.5 Privilege boundary

Workloads use the least privilege declared by the component and profile.

The projection shall reject or explicitly justify:

- privileged containers;
- host PID, IPC, or network namespace;
- hostPath mounts;
- writable root filesystem;
- unrestricted Linux capabilities;
- host container-runtime sockets;
- host device access;
- cluster-admin bindings;
- wildcard RBAC;
- broad cross-namespace secret access.

### 7.6 Image boundary

Every deployable image uses an immutable digest.

Mutable tags can appear as non-authoritative display metadata but cannot select the deployed bytes.

### 7.7 Admission boundary

The cluster admission path enforces the profile's declared controls.

The deployment authority shall not use an alternative API path, disabled webhook, privileged override, or direct consensus-store write to bypass admission.

### 7.8 Evidence boundary

Logs and deployment evidence exclude:

- secret values;
- unrestricted manifests containing secret material;
- tenant payloads;
- database contents;
- cultural content;
- full environment dumps;
- service-account tokens.

## 8. Resource Envelope

Resource Governor remains the canonical authority for:

- workload classes;
- admission;
- CPU and memory envelopes;
- I/O;
- worker and process limits;
- queues;
- concurrency;
- priority;
- suspension;
- pressure degradation.

Kubernetes requests, limits, quotas, priorities, and placement rules are projections of those decisions.

### 8.1 Required mapping

Each workload projection declares:

- workload class;
- criticality;
- Resource Governor envelope reference;
- CPU request and hard limit;
- memory request and hard limit;
- ephemeral-storage request and hard limit where applicable;
- concurrency or replica bounds;
- termination grace period;
- priority class selected by the profile;
- disruption behavior;
- task activation or idle expiry where applicable.

### 8.2 Missing values

This recipe does not invent numeric resource values.

A missing canonical envelope blocks deployment.

### 8.3 Pressure behavior

The projection shall preserve:

1. required control-plane capabilities;
2. higher-criticality components;
3. current authoritative transitions;
4. safe recovery work;
5. optional, heavy, or task-activated work last.

Kubernetes eviction or autoscaling behavior cannot reverse this ordering.

## 9. Naming and Isolation

### 9.1 Namespace naming

Namespace names are supplied by the active profile.

This recipe does not invent a universal prefix.

Every namespace is labeled with stable non-secret references for:

- profile ID and version;
- release-set ID and version;
- authority owner;
- lifecycle environment;
- tenant or sovereignty scope where applicable.

### 9.2 Workload naming

Workload resource names use the component's canonical identifier and an explicit projection-specific suffix only when required.

A Kubernetes object name does not replace the component ID.

### 9.3 Labels and annotations

Labels are used for stable selectable identity.

Annotations are used for non-secret references that are not selectors.

Permitted references can include:

- component ID;
- component version;
- profile ID;
- release-set ID;
- resource-envelope ID;
- policy-bundle ID;
- test-matrix ID;
- lifecycle group.

Do not place credentials, personal data, tenant payloads, or arbitrary user content in labels or annotations.

### 9.4 Field ownership

Server-side apply uses a stable field manager:

```text
koa-deployment-authority
```

Component operators or other controllers must have explicitly non-overlapping field ownership or a declared reconciliation contract.

Unexpected field conflicts block apply.

## 10. Procedure

### Step 1 — Bind execution to the admitted cluster

**Objective**

Prevent mutation of the wrong cluster.

**Command**

```bash
set -euo pipefail
set +x

kubectl --context "$KUBE_CONTEXT" config current-context
kubectl --context "$KUBE_CONTEXT" cluster-info
kubectl --context "$KUBE_CONTEXT" get --raw='/readyz'
```

**Expected result**

The context, cluster endpoint, certificate identity, and node inventory match the active profile.

**Failure behavior**

Stop without applying resources.

---

### Step 2 — Verify the Release Set and bundle

**Objective**

Confirm that the exact four-channel Release Set and its evidence are admitted.

**Command**

Run the canonical Release Set and artifact validators against:

```bash
printf '%s
'   "$RELEASE_BUNDLE_ROOT"   "$RELEASE_SET_ID"   "$RELEASE_SET_VERSION"
```

Verify exact versions for:

```text
system
services
governance
knowledge
```

**Expected result**

- Release Set compatibility passes;
- required artifacts are present;
- signatures and provenance pass;
- SBOM and vulnerability dispositions pass;
- no artifact is revoked;
- target profile matches.

**Failure behavior**

Do not contact the cluster with deployment mutations.

---

### Step 3 — Verify the projection inventory

**Objective**

Ensure the Kubernetes projection matches the Release Set and profile.

**Command**

```bash
test -d "$DEPLOYMENT_PROJECTION_ROOT"
test ! -L "$DEPLOYMENT_PROJECTION_ROOT"

find "$DEPLOYMENT_PROJECTION_ROOT"   -type l -print -quit |
  grep -q . && {
    printf '%s
' "symlink found in deployment projection" >&2
    exit 1
  } || true
```

Run the canonical projection validator.

**Expected result**

Every resource file, image digest, namespace, component, API extension, migration, activation group, and test reference resolves.

**Failure behavior**

Projection remains a rejected candidate.

---

### Step 4 — Verify exact images and local availability

**Objective**

Ensure every image selected by the projection is immutable and locally retrievable through an admitted registry path.

**Command**

The projection validator rejects image references lacking a digest.

Extract and inspect only image references:

```bash
kubectl --context "$KUBE_CONTEXT" create   --dry-run=client   -f "$DEPLOYMENT_PROJECTION_ROOT"   -o json |
python3 -c '
import json
import sys

data = json.load(sys.stdin)
items = data.get("items", [data])

def walk(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "image" and isinstance(child, str):
                print(child)
            walk(child)
    elif isinstance(value, list):
        for child in value:
            walk(child)

walk(items)
' | sort -u
```

**Expected result**

Every image reference contains an intrinsic digest and resolves to an admitted artifact.

**Failure behavior**

Block deployment. Do not substitute a mutable tag.

---

### Step 5 — Perform client and server validation

**Objective**

Validate structure and cluster-side admission without persisting resources.

**Command**

```bash
kubectl --context "$KUBE_CONTEXT" apply   --dry-run=client   --server-side   --field-manager=koa-deployment-authority   -f "$DEPLOYMENT_PROJECTION_ROOT"

kubectl --context "$KUBE_CONTEXT" apply   --dry-run=server   --server-side   --field-manager=koa-deployment-authority   -f "$DEPLOYMENT_PROJECTION_ROOT"
```

**Expected result**

Schema, API availability, admission policy, field ownership, and authorization pass.

**Failure behavior**

No objects are persisted.

---

### Step 6 — Validate namespace, identity, and RBAC projections

**Objective**

Verify least-privilege boundaries before apply.

**Command**

Run the registered control-plane identity and RBAC tests.

At minimum, verify:

- every service account maps to one declared workload identity;
- no service uses the default service account unintentionally;
- no component workload receives cluster-admin;
- wildcard verbs and resources are absent unless exact policy permits them;
- cross-namespace access is explicit;
- deployment authority cannot read component secret values by default;
- component identities cannot mutate deployment authority resources.

**Expected result**

Every permission is attributable and within profile scope.

**Failure behavior**

Block deployment.

---

### Step 7 — Validate network and storage projections

**Objective**

Verify component and data boundaries.

**Command**

Run the registered projection tests for:

- default-deny network behavior where required;
- declared ingress and egress only;
- DNS and time access;
- explicit external integration routes;
- persistent storage ownership;
- storage class and topology compatibility;
- backup and restore integration;
- prohibition of undeclared hostPath;
- owner-scoped PVC and volume mounts;
- no shared writable authoritative volume between unrelated owners.

**Expected result**

Network and storage projections match component and profile contracts.

**Failure behavior**

Block deployment.

---

### Step 8 — Validate resource projections

**Objective**

Prove that every workload maps to an active Resource Governor envelope.

**Command**

Run the canonical resource-envelope projection validator.

Verify that each workload has:

- envelope reference;
- workload class;
- criticality;
- CPU and memory request;
- hard limits where required;
- replica or concurrency bound;
- termination and disruption behavior;
- queue or task-activation behavior where applicable.

**Expected result**

No workload relies on Kubernetes defaults for a required kOA resource decision.

**Failure behavior**

Block deployment.

---

### Step 9 — Stage namespaces and non-running prerequisites

**Objective**

Create the bounded target context without activating new service instances.

**Command**

Apply only the projection phase classified as `prerequisites`:

```bash
PREREQUISITES_ROOT="$DEPLOYMENT_PROJECTION_ROOT/phases/prerequisites"

kubectl --context "$KUBE_CONTEXT" apply   --server-side   --field-manager=koa-deployment-authority   -f "$PREREQUISITES_ROOT"
```

Prerequisites can include:

- namespaces;
- service accounts;
- RBAC;
- non-secret ConfigMaps;
- NetworkPolicies;
- quotas;
- disruption controls;
- storage claims that do not mutate owner data;
- admission-policy projections.

**Expected result**

Prerequisites become ready without starting the new service activation group.

**Failure behavior**

Remove only newly created unused prerequisites through the rollback inventory.

---

### Step 10 — Run owner-controlled migrations

**Objective**

Prepare schemas or data only through owning component procedures.

**Command**

For every migration group:

1. resolve the owning component;
2. verify migration artifact identity;
3. verify current data and schema version;
4. verify backup or checkpoint requirements;
5. verify rollback compatibility or predeclared forward repair;
6. apply the owner migration Job or interface;
7. wait for its terminal result;
8. register migration evidence.

Example observation:

```bash
kubectl --context "$KUBE_CONTEXT"   -n "$MIGRATION_NAMESPACE"   wait   --for=condition=complete   --timeout="$MIGRATION_WAIT"   "job/$MIGRATION_JOB_NAME"
```

The exact namespace, timeout, and Job name come from the migration contract.

**Expected result**

The owner verifies the new schema or data state.

**Failure behavior**

Stop service activation and select the declared rollback or forward-repair path.

---

### Step 11 — Apply the staged service activation group

**Objective**

Start candidate service instances without changing authoritative routing.

**Command**

```bash
SERVICES_ROOT="$DEPLOYMENT_PROJECTION_ROOT/phases/services"

kubectl --context "$KUBE_CONTEXT" apply   --server-side   --field-manager=koa-deployment-authority   -f "$SERVICES_ROOT"
```

**Expected result**

Candidate instances start under the new exact artifacts while authoritative routing remains unchanged where the lifecycle contract requires staging.

**Failure behavior**

Keep prior verified release active.

---

### Step 12 — Verify readiness and representative capabilities

**Objective**

Prove component behavior beyond Kubernetes process status.

**Command**

Run registered tests for:

- workload identity;
- exact image digest;
- component dependencies;
- readiness;
- owner data compatibility;
- queue and job behavior;
- Resource Governor enforcement;
- Governance Policy Runtime decisions;
- receipts;
- network and storage boundaries;
- representative user or system capabilities;
- degraded and restoring behavior.

Kubernetes observations can support diagnosis:

```bash
kubectl --context "$KUBE_CONTEXT" get workloads -A
kubectl --context "$KUBE_CONTEXT" get pods -A
kubectl --context "$KUBE_CONTEXT" get events -A
```

The exact workload query can be narrowed by profile labels.

**Expected result**

Every required activation assertion passes.

**Failure behavior**

Do not activate authoritative routing.

---

### Step 13 — Activate authoritative routing

**Objective**

Switch traffic or authority only after complete verification.

**Command**

Apply only the activation phase:

```bash
ACTIVATION_ROOT="$DEPLOYMENT_PROJECTION_ROOT/phases/activation"

kubectl --context "$KUBE_CONTEXT" apply   --server-side   --field-manager=koa-deployment-authority   -f "$ACTIVATION_ROOT"
```

Activation resources can project:

- Service selectors;
- internal route selectors;
- gateway routing;
- leader or active-revision references;
- another declared routing mechanism.

**Expected result**

The new verified activation group becomes authoritative atomically according to the lifecycle contract.

**Failure behavior**

Restore the prior route when safe or enter forward repair.

---

### Step 14 — Verify post-activation state and retire prior instances

**Objective**

Ensure the active route and runtime state match the Release Set.

**Command**

Run post-activation tests, then drain and retire prior instances through their component contracts.

Verify:

- no mixed-version state outside declared compatibility;
- no old writer remains active;
- queues and leases are reconciled;
- new receipts persist;
- prior artifacts remain available for declared rollback;
- obsolete candidate resources are removed only after commit.

**Expected result**

The active Release Set is coherent and the prior activation group is safely retired or retained as recovery state.

**Failure behavior**

Use rollback when proven safe; otherwise follow forward repair.

---

### Step 15 — Register deployment evidence

**Objective**

Create the exact conformance record for this deployment.

Evidence binds:

- cluster identity;
- profile and version;
- Release Set ID and version;
- projection inventory version;
- image digests;
- namespaces;
- migration results;
- dry-run and admission results;
- identity, RBAC, network, storage, and resource tests;
- readiness and capability tests;
- route activation;
- rollback availability;
- final active revisions;
- receipts.

**Expected result**

Evidence is immutable, registered, and traceable.

**Failure behavior**

When evidence is required receipt-before-commit, keep activation uncommitted or enter the declared recovery path.

## 11. Idempotency

```text
Idempotent: conditional
```

Idempotent operations:

- cluster and Release Set validation;
- projection validation;
- client and server dry-run;
- server-side apply when field ownership and desired state are unchanged;
- readiness observation;
- evidence lookup;
- applying unchanged network, RBAC, quota, and service projections.

Conditionally idempotent operations:

- database migrations;
- Jobs;
- route activation;
- certificate rotation;
- backup hooks;
- one-time initialization;
- operator-managed resources.

Those operations require their owner-specific idempotency and retry contracts.

A rerun shall not:

- recreate a completed non-idempotent migration;
- erase a failed attempt;
- change image bytes under the same identity;
- force field ownership;
- broaden permissions;
- bypass current-state verification.

## 12. Validation

### 12.1 Projection validation

Validate:

- no unresolved template values;
- no symlinks;
- exact namespaces and component IDs;
- exact image digests;
- supported API versions;
- expected resource kinds only;
- no undeclared custom resources;
- no plaintext secret values;
- no broad host access;
- no mutable artifact references.

### 12.2 Profile validation

Validate:

- Kubernetes adoption by `control_plane`;
- cluster topology;
- node and workload identity;
- CNI, CSI, ingress, DNS, time, certificate, backup, and recovery mechanisms;
- disconnected behavior where required;
- support and upgrade policy.

### 12.3 Component-boundary validation

Validate:

- separate component identities;
- owner-only authoritative writes;
- declared interfaces;
- no cross-component writable volume;
- no controller or operator gaining domain ownership;
- no sidecar bypassing component interfaces.

### 12.4 Lifecycle validation

Validate:

- preflight;
- staging;
- drain;
- migration;
- readiness;
- representative capability tests;
- atomic route activation;
- post-activation verification;
- rollback;
- forward repair;
- prior-state retention;
- receipts.

### 12.5 Applicable documentation checks

```bash
python docs/tools/check_profile_composition.py
python docs/tools/check_component_boundaries.py
python docs/tools/check_release_sets.py
python docs/tools/check_artifact_contracts.py
python docs/tools/check_traceability.py
python docs/tools/check_canonical_ownership.py
python docs/tools/check_interfile_locks.py
python docs/tools/validate_docs.py
```

### 12.6 Success criteria

The recipe succeeds only when:

- the exact cluster matches `control_plane`;
- all four Release Set channels pass;
- every image is digest-bound and admitted;
- server-side dry-run passes;
- identity, RBAC, network, storage, and resource tests pass;
- migrations complete under owner authority;
- staged instances pass component readiness and representative capability tests;
- authoritative routing activates through its declared contract;
- old writers are retired or safely retained;
- complete evidence and receipts register.

## 13. Failure Handling

| Failure | Safe state | Required response |
| --- | --- | --- |
| Wrong context or cluster identity | No mutation | Correct context and revalidate |
| Profile does not adopt Kubernetes | No deployment | Use the profile-selected mechanism |
| Release Set mismatch | Prior release remains active | Resolve compatible Release Set |
| Missing image digest | Candidate rejected | Publish an immutable admitted artifact |
| Image unavailable offline | Candidate blocked | Restore admitted local mirror |
| Client validation fails | No mutation | Correct projection |
| Server dry-run fails | No mutation | Correct schema, policy, RBAC, or API compatibility |
| Field ownership conflict | No forced takeover | Reconcile controller ownership contract |
| RBAC too broad | Candidate rejected | Narrow permissions |
| Network or storage boundary fails | Candidate rejected | Correct profile projection |
| Resource envelope unresolved | Candidate blocked | Resolve canonical envelope |
| Migration fails before irreversible boundary | Prior service remains active | Apply owner rollback |
| Migration crosses irreversible boundary | Affected capability blocked or restoring | Apply predeclared forward repair |
| Candidate readiness fails | Prior route remains active | Diagnose or remove candidate |
| Capability test fails | Prior route remains active | Correct candidate |
| Route activation partially applies | Enter restoring | Reconcile exact authoritative route |
| Receipt persistence fails | Critical commit uncommitted | Restore evidence path |
| Old writer remains active | New commit blocked | Fence old writer and reconcile |
| Cluster control plane degrades | Stop new changes | Preserve safely running verified workloads |
| Recovery cannot identify actual state | Remain restoring | Reconcile API, workloads, routes, leases, and owner data |

Do not use `--force-conflicts` as a generic recovery mechanism.

## 14. Rollback

### 14.1 Rollback eligibility

Rollback is allowed only when:

- the prior component and Release Set versions remain compatible with current data;
- prior artifacts remain admitted;
- prior routing state is known;
- no irreversible migration boundary was crossed;
- owner contracts permit rollback;
- required receipts can persist.

### 14.2 Route rollback

Apply the prior verified activation projection:

```bash
kubectl --context "$KUBE_CONTEXT" apply   --server-side   --field-manager=koa-deployment-authority   -f "$PRIOR_ACTIVATION_ROOT"
```

Then verify the prior representative capabilities.

### 14.3 Workload rollback

Reapply the prior verified service projection only after route and data compatibility are proven.

Do not rely solely on a Kubernetes controller's revision history.

The canonical rollback input is the prior admitted projection and Release Set.

### 14.4 Migration rollback

Use only the owning component's declared down-migration, snapshot restore, compensation, or recovery procedure.

A generic Kubernetes rollback cannot reverse owner data mutations.

### 14.5 Forward repair

When rollback is unsafe:

1. preserve the verified post-boundary state;
2. block or degrade affected capabilities;
3. apply the admitted forward-repair artifact;
4. use ordered idempotent checkpoints;
5. reconcile queues, leases, caches, indexes, and replicas;
6. verify representative capabilities;
7. commit atomically;
8. retain complete evidence.

## 15. Cleanup and Removal

### 15.1 Candidate cleanup

After a failed pre-activation candidate:

- remove only resources identified by the deployment inventory;
- preserve migration evidence;
- preserve logs required for bounded diagnosis;
- preserve artifacts needed for investigation;
- do not delete persistent data;
- do not delete shared namespaces;
- do not remove controllers owned by another field manager.

### 15.2 Prior-release cleanup

After successful commit and retention expiry:

- verify no rollback dependency remains;
- verify no queue, lease, route, or data dependency remains;
- remove prior workload resources;
- retain required artifacts and evidence;
- release unused capacity;
- preserve owner data.

### 15.3 Full control-plane removal

Full removal requires a separate retirement procedure covering:

- data export and retention;
- component shutdown;
- route removal;
- certificate and identity revocation;
- backup;
- evidence retention;
- persistent-volume disposition;
- cluster or namespace retirement;
- external integration removal;
- credible exit.

This recipe does not delete a cluster or persistent volumes.

## 16. Observability and Evidence

### 16.1 Required observations

- cluster identity and readiness;
- node and workload identity;
- component and image identity;
- namespace and service-account identity;
- resource-envelope reference;
- workload readiness;
- capability-test outcomes;
- routing revision;
- migration state;
- queue and lease reconciliation;
- evidence and receipt health;
- current Release Set.

### 16.2 Kubernetes status interpretation

Kubernetes status is necessary operational evidence but not sufficient for kOA activation.

Examples:

| Kubernetes observation | kOA interpretation |
| --- | --- |
| Pod `Running` | Process exists; capability not yet proven |
| Readiness probe passes | Declared endpoint responds; representative capability still required |
| Deployment available | Desired pod count available; data and route compatibility still required |
| Job complete | Process exited successfully; owner result still requires validation |
| Rollout complete | Kubernetes desired state reached; kOA activation still requires full lifecycle checks |
| PVC bound | Storage attached; owner schema, durability, and restore behavior still unresolved |

### 16.3 Logs

Logs exclude:

- secret values;
- tokens;
- complete Secret objects;
- unrestricted environment variables;
- tenant or cultural payloads;
- database rows;
- private key material.

### 16.4 Receipts

Receipts can be required for:

- artifact admission;
- migration start and completion;
- governed override;
- route activation;
- rollback;
- forward repair;
- break-glass;
- Release Set commit;
- revocation;
- retirement.

### 16.5 Evidence

Evidence follows `docs/09-conformance/05-test-evidence.md`.

It includes exact execution and subject identities and does not rely on screenshots or dashboard state alone.

## 17. Offline Behavior

```text
offline_capable_when_profile_admitted
```

Disconnected deployment requires locally available admitted:

- container images by digest;
- Kubernetes projections;
- Release Set;
- system, services, governance, and knowledge artifacts;
- schemas;
- trust roots;
- policy bundles;
- resource envelopes;
- identity and certificate material;
- test tools;
- evidence storage;
- rollback and forward-repair artifacts.

The cluster shall not require a remote managed control plane for the declared offline mode.

External integrations degrade independently.

Network unavailability does not justify:

- mutable image tags;
- bypassed signatures;
- disabled admission;
- missing receipts;
- unbounded credentials;
- direct component-data writes;
- skipped compatibility checks.

## 18. Compatibility and Versioning

| Dependency | Compatible condition | Blocking condition |
| --- | --- | --- |
| Control-plane profile | Exact version explicitly adopts Kubernetes | Kubernetes absent from profile |
| Kubernetes cluster | Version and extensions inside profile support policy | Unsupported or unresolved cluster |
| CNI and CSI | Exact admitted profile selections | Unresolved network or storage behavior |
| Component contracts | Kubernetes projection matches component interfaces and lifecycle | Kubernetes-only behavior changes component authority |
| Release Set | All four channels compatible | Independent unresolved channel |
| Image artifacts | Exact digest, provenance, SBOM, signature, admission | Mutable tag or revoked artifact |
| Resource envelopes | Every workload maps to current envelope | Missing numeric or policy values |
| Governance policy | Required decisions and admission controls resolve | Bypass or unavailable required policy |
| Recipe versions | `1.x` | Major phase, authority, or activation-model change |

A major recipe version is required when changing:

- deployment phases;
- field manager;
- activation model;
- namespace ownership;
- route model;
- migration coordination;
- rollback or cleanup safety;
- offline assumptions.

## 19. AI Execution Protocol

An AI agent applying this recipe must:

1. load active AI context;
2. verify recipe status and version;
3. resolve the exact control-plane profile;
4. verify Kubernetes is explicitly adopted;
5. verify exact cluster context and identity;
6. verify the complete Release Set;
7. validate every deployment artifact and image digest;
8. run client and server dry-run before apply;
9. inspect permission, network, storage, and resource projections structurally;
10. execute phases separately;
11. stop before authoritative routing when any assertion fails;
12. never display Secret values;
13. never use mutable tags;
14. never use `--force-conflicts` without a separate owner-approved recovery decision;
15. never create or delete persistent data under this recipe;
16. never infer migration safety from Kubernetes rollout state;
17. register bounded evidence after each critical phase;
18. report `blocked` when profile, cluster, Release Set, identity, envelope, policy, or evidence authority cannot resolve.

The agent must not:

- select a Kubernetes distribution;
- install or upgrade the cluster;
- invent numeric resources;
- grant cluster-admin;
- create plaintext secrets;
- broaden NetworkPolicy;
- bypass admission;
- force delete stateful workloads;
- delete PVCs;
- treat Kubernetes as Governance Policy Runtime;
- treat the Kubernetes scheduler as Resource Governor;
- treat a controller as component owner;
- deploy to endpoints under this recipe.

### 19.1 Example execution summary

```json
{
  "recipe_id": "RECIPE-CP-001",
  "recipe_version": "1.0.0",
  "profile_id": "control_plane",
  "cluster_id": "control-plane-cluster-primary",
  "release_set_id": "release-set-control-plane-2026.08.03.1",
  "phases": [
    "preflight",
    "prerequisites",
    "migrations",
    "services",
    "capability_verification",
    "activation",
    "post_activation"
  ],
  "images_verified_by_digest": true,
  "server_dry_run": "pass",
  "authoritative_route_activated": true,
  "rollback_available": true,
  "evidence_ids": [],
  "result": "pass"
}
```

The example values are illustrative and do not establish canonical cluster or release identities.

## 20. Troubleshooting

### Server-side dry-run reports an unknown resource kind

**Signal**

The API server rejects a resource kind or version.

**Likely causes**

- required CRD or extension is absent;
- projection targets a different cluster version;
- profile extension inventory is stale;
- resource belongs to an undeclared operator.

**Action**

Block deployment. Resolve the profile and extension contract. Do not install an arbitrary CRD from the Internet.

---

### Server-side apply reports a field conflict

**Signal**

Another field manager owns a projected field.

**Likely causes**

- operator and deployment authority overlap;
- manual mutation changed managed fields;
- projection ownership contract changed;
- previous deployment used a different field manager.

**Action**

Identify the owning controller and reconcile the field-ownership contract.

Do not use `--force-conflicts` merely to complete deployment.

---

### Workload is running but capability tests fail

**Signal**

Pods are `Running` or ready while representative tests fail.

**Likely causes**

- incompatible data or policy;
- wrong route;
- missing knowledge artifact;
- dependency failure;
- identity or secret binding error;
- incorrect Release Set;
- readiness probe is too shallow.

**Action**

Keep authoritative routing on the prior release. Diagnose through component interfaces and bounded logs.

---

### Resource limits differ from the active envelope

**Signal**

Projection validator reports missing or inconsistent requests, limits, priority, or replica bounds.

**Likely causes**

- generated projection is stale;
- envelope changed after projection generation;
- manual manifest edit;
- operator applies defaults.

**Action**

Regenerate the projection from the canonical envelope and rerun validation.

Do not edit numeric values ad hoc.

---

### A migration Job completed but the component cannot read the schema

**Signal**

Kubernetes reports Job success while owner validation fails.

**Likely causes**

- script exited zero before full verification;
- wrong database target;
- incompatible service artifact;
- irreversible boundary crossed;
- another writer remained active.

**Action**

Treat the migration as failed. Inspect owner state, writer fencing, and checkpoints. Use rollback only when proven safe; otherwise forward repair.

---

### Disconnected cluster cannot pull an image

**Signal**

Image pull fails for an exact digest.

**Likely causes**

- local mirror is incomplete;
- trust or registry credentials expired;
- projection points to an external registry;
- offline bundle omitted the artifact.

**Action**

Keep the prior release active. Repair the admitted local artifact path and revalidate the bundle.

Do not replace the digest with a local mutable tag.

---

### Prior and new writers are both active

**Signal**

Two revisions can mutate one authoritative data set.

**Likely causes**

- route activation did not fence the old writer;
- lease reconciliation failed;
- rollout strategy permits unsafe overlap;
- leader identity is unresolved.

**Action**

Enter `restoring`, stop new mutations where safe, fence the invalid writer, reconcile owner state, and emit required receipts.

## 21. Non-Normative Example

A control-plane profile declares:

```text
cluster_id: control-plane-cluster-primary
primary_profile_id: control_plane
release_set_id: release-set-control-plane-2026.08.03.1
deployment_strategy: staged_then_activate
```

The admitted projection contains:

```text
phases/prerequisites
phases/migrations
phases/services
phases/activation
inventory.json
```

The deployment authority performs:

```bash
kubectl --context "$KUBE_CONTEXT" apply   --dry-run=server   --server-side   --field-manager=koa-deployment-authority   -f "$DEPLOYMENT_PROJECTION_ROOT"

kubectl --context "$KUBE_CONTEXT" apply   --server-side   --field-manager=koa-deployment-authority   -f "$DEPLOYMENT_PROJECTION_ROOT/phases/prerequisites"

kubectl --context "$KUBE_CONTEXT" apply   --server-side   --field-manager=koa-deployment-authority   -f "$DEPLOYMENT_PROJECTION_ROOT/phases/services"
```

After representative capability tests pass, the activation phase changes the declared authoritative route.

The example does not make these cluster or Release Set identifiers canonical.

## 22. Migration from a Non-Kubernetes Control Plane

This recipe does not perform the migration.

The accepted migration sequence is:

```text
declare Kubernetes-adopting profile version
→ admit cluster and extensions
→ generate deployment projections
→ verify supply-chain and Release Set compatibility
→ stage replicated or migrated owner data through owner contracts
→ verify identities, policies, resources, network, storage, and recovery
→ stage service instances
→ run representative capabilities
→ switch authoritative routing atomically
→ enter restoring
→ reconcile queues, leases, writes, and receipts
→ retire prior deployment after retention and rollback conditions
```

A migration shall preserve:

- component identities and authority;
- data ownership;
- exact artifacts;
- policy decisions;
- resource envelopes;
- receipts;
- rollback or forward-repair behavior;
- credible exit back to a non-Kubernetes deployment.

## 23. Author Checklist

- [x] Recipe identity and version are present.
- [x] Status is active and non-normative.
- [x] Kubernetes is limited to `control_plane`.
- [x] Cluster installation and upgrade are excluded.
- [x] No Kubernetes version or provider is invented.
- [x] Release Set and four-channel compatibility are required.
- [x] Images are digest-bound.
- [x] Server-side client and server dry-runs are included.
- [x] Field ownership is explicit.
- [x] Secrets are reference-only.
- [x] Component data ownership is preserved.
- [x] Resource Governor and Governance Policy Runtime remain canonical.
- [x] Staging and activation are separate.
- [x] Kubernetes readiness is not treated as full capability readiness.
- [x] Rollback and forward repair are explicit.
- [x] Offline behavior is explicit.
- [x] PVC and cluster deletion are excluded.
- [x] Evidence and receipts are required.
- [x] AI execution fails closed.

## 24. Review Checklist

- [x] The recipe does not create normative profile authority.
- [x] The recipe does not globalize Kubernetes.
- [x] Endpoints remain Kubernetes-independent.
- [x] Kubernetes RBAC does not replace governance authority.
- [x] Kubernetes scheduling does not replace resource authority.
- [x] Operators and controllers do not become component owners.
- [x] Cross-component authoritative writes remain prohibited.
- [x] Mutable image tags are rejected.
- [x] Admission cannot be bypassed.
- [x] Migration Jobs remain owner-controlled.
- [x] Activation is explicit and atomic.
- [x] Failed evidence persistence cannot silently commit.
- [x] Recovery reconciles actual state.
- [x] Cleanup preserves persistent data.
- [x] Applicable locks and documentation checks are listed.

## 25. Final Recipe Rule

> Deploy Kubernetes projections only into a profile-admitted `control_plane` cluster, using exact Release Set artifacts, immutable image digests, least-privilege identities, declared network and storage boundaries, Resource Governor envelope projections, and separate staged and authoritative activation phases. Kubernetes remains an implementation adapter and never becomes the canonical owner of kOA authority, data, policy, resources, releases, or conformance.
