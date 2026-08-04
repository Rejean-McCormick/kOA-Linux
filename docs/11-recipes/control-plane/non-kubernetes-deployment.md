<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-RECIPE-CP-NOK8S-001",
  "document_class": "non_normative_recipe",
  "status": "active",
  "language": "en",
  "layer": "recipes",
  "scope": [
    "profile:control_plane",
    "deployment_mode:non_kubernetes",
    "profile_conditioned_operations"
  ],
  "canonical_refs": [
    "generated/profile-catalog.json",
    "contracts/profiles/control-plane.profile.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "generated/component-catalog.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json#/locks/LOCK-PROFILE-001",
    "generated/assertion-index.json#/locks/LOCK-IMPL-002",
    "generated/assertion-index.json#/locks/LOCK-LIFE-001",
    "generated/assertion-index.json#/locks/LOCK-LIFE-003",
    "generated/decision-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-PROFILE-001",
    "DEC-CONTAINER-001",
    "DEC-K8S-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-GATE-001",
    "DEC-AI-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-RECIPES-000",
    "DOC-SYS-002",
    "DOC-SYS-004",
    "DOC-SYS-007",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-016",
    "DOC-SYS-017",
    "DOC-DEV-006",
    "DOC-DEV-016",
    "DOC-SEC-001",
    "DOC-SEC-008",
    "DOC-OPS-000",
    "DOC-OPS-009",
    "DOC-CONF-010",
    "ADR-014"
  ],
  "tags": [
    "recipe",
    "control-plane",
    "non-kubernetes",
    "systemd",
    "oci-runtime",
    "podman",
    "docker",
    "atomic-activation",
    "rollback",
    "service-readiness",
    "data-isolation",
    "non-normative"
  ]
}
KOA:DOC-META:END -->

# Non-Kubernetes Control-Plane Deployment

> **Recipe classification:** Non-authoritative implementation guidance.  
> **Risk class:** `operational_change`.  
> **Primary profile:** `control_plane`.  
> **Deployment mode:** `non_kubernetes`.  
> **Authority rule:** The active profile, component contracts, Release Set, security policy, operating authority, and conformance catalog take precedence over this recipe.

## 1. Purpose

This recipe deploys a kOA control plane without Kubernetes.

The reference model uses:

- systemd-managed services;
- a profile-selected OCI runtime where containers are used;
- immutable Release Set directories;
- one active and one previous compatible Release Set;
- explicit service identities;
- independently owned data stores;
- declared local or network endpoints;
- readiness checks;
- bounded resources;
- atomic activation and rollback.

The recipe demonstrates that Kubernetes is optional for the control-plane profile rather than an architectural requirement.

The deployment model is:

```text
verified control-plane profile
        ↓
complete compatible Release Set
        ↓
inactive staged artifacts and configuration
        ↓
systemd units and OCI runtime selected by profile
        ↓
atomic active-release switch
        ↓
service restart and readiness validation
        ↓
accepted control-plane capability
```

### 1.1 Result

A successful execution produces:

- one active non-Kubernetes control-plane Release Set;
- one retained previous compatible Release Set;
- profile-declared systemd services;
- local or distributed service endpoints defined outside Kubernetes;
- separate service, database, queue, storage, and secret identities;
- component readiness results;
- activation or rollback evidence;
- no dependency on `kubectl`, `kubelet`, `kubeadm`, Helm, Kustomize, a Kubernetes API server, or a kubeconfig.

### 1.2 Non-goals

This recipe does not:

- prohibit Kubernetes for every control-plane deployment;
- redefine `DEC-K8S-001`;
- create a new profile;
- approve a container runtime;
- create or sign artifacts;
- create a Release Set;
- define component data ownership;
- merge Governance Policy Runtime and Resource Governor;
- merge Publication Gateway and UCKK Dimension Gateway;
- create a shared database owner;
- grant unrestricted root or production credentials;
- configure arbitrary Internet ingress;
- enable external AI;
- replace production backup, restore, incident, or decommissioning runbooks;
- claim deployment conformance without registered tests and evidence.

## 2. Applicability

### 2.1 Supported scope

This recipe applies when:

```text
primary_profile: control_plane
orchestration_mode: non_kubernetes
```

The active profile can select:

- native systemd services;
- OCI containers under systemd;
- rootless Podman;
- Docker Engine under a profile-approved service boundary;
- another OCI-compatible runtime;
- one node;
- several statically managed nodes;
- a profile-approved reverse proxy or load balancer;
- local or external profile-owned databases and queues.

### 2.2 Unsupported scope

Use another deployment path when the effective profile selects:

- Kubernetes;
- a managed Kubernetes service;
- Kubernetes-native operators;
- Kubernetes service discovery;
- Kubernetes secrets;
- Kubernetes persistent volumes;
- Kubernetes network policy;
- Helm or Kustomize as the active deployment authority.

Do not mix Kubernetes-managed and non-Kubernetes-managed ownership for the same component instance.

### 2.3 Reference implementation assumptions

The executable examples assume:

- Linux;
- systemd;
- Python 3;
- `curl`;
- `flock`;
- immutable release directories;
- profile-owned service units;
- optional OCI containers launched by those units;
- one active-link mechanism shared by the relevant units.

These assumptions are profile-scoped implementation choices.

### 2.4 Deployment topologies

This recipe can support:

| Topology | Description |
| --- | --- |
| Single-node control plane | All selected control-plane services run on one profile-compliant node |
| Split-service control plane | Services run on several statically declared nodes |
| External-state topology | Profile-owned databases, queues, or object stores run on separate nodes or managed infrastructure |
| Offline administration topology | Control-plane authority and required artifacts remain locally available without Internet dependence |
| High-assurance topology | Stronger identity, privilege, storage, review, and evidence controls are composed through an active overlay |

The exact topology remains in the active profile and component contracts.

## 3. Preconditions

### 3.1 Accepted authority

Resolve before deployment:

- `DEC-PROFILE-001`;
- `DEC-CONTAINER-001`;
- `DEC-K8S-001`;
- `DEC-DATA-001`;
- `DEC-GOV-001`;
- `DEC-GATE-001`;
- `DEC-AI-001`;
- `DEC-REL-001`;
- the active control-plane profile;
- selected overlays;
- target Release Set;
- component contracts;
- resource envelopes;
- network boundaries;
- backup and restore readiness;
- activation authority;
- evidence requirements.

Installed unit files, container images, or open ports do not create deployment authority.

### 3.2 Required deployment inventory

Inventory:

- nodes;
- effective profile and overlays;
- service identities;
- systemd units;
- OCI runtime;
- images or native artifacts;
- databases;
- schemas;
- queues;
- object stores;
- secrets;
- network endpoints;
- trust and policy artifacts;
- backup targets;
- previous known-good Release Set;
- monitoring and evidence paths.

### 3.3 Exact Release Set

The Release Set is already:

- published;
- immutable;
- integrity-verified;
- provenance-verified;
- trust-verified;
- revocation-checked;
- component-compatible;
- profile-compatible;
- migration-compatible;
- staged inactive;
- accompanied by required tests and evidence.

The Release Set includes compatible identities for:

- `system`;
- `services`;
- `governance`;
- `knowledge`.

### 3.4 Service ownership

Every service resolves to one active component contract.

Every component has:

- one workload or service identity;
- owned storage;
- owned database or schema identity;
- owned migration path;
- owned backup and restore path;
- declared interfaces;
- declared readiness;
- declared failures;
- no direct foreign write.

### 3.5 Control separation

Verify:

- Governance Policy Runtime evaluates policy;
- Resource Governor controls resource admission;
- kOA Node Agent or the profile-approved privileged boundary executes closed host operations;
- Publication Gateway executes external publication;
- UCKK Dimension Gateway coordinates UCKK admission;
- Audit Broker handles selected evidence.

The non-Kubernetes deployment does not merge these responsibilities into one service or administrator account.

### 3.6 Required commands

The reference helper uses:

```text
bash
python3
systemctl
readlink
stat
find
flock
curl
ln
mv
grep
```

Verify:

```bash
for command_name in \
  bash python3 systemctl readlink stat find flock curl ln mv grep; do
  command -v "$command_name" >/dev/null ||
    printf 'missing: %s\n' "$command_name"
done
```

### 3.7 Runtime selection

When containers are used, resolve one profile-approved OCI runtime.

Example checks:

```bash
command -v podman >/dev/null && podman version
command -v docker >/dev/null && docker version
```

Do not run both runtimes for the same component instance unless the active profile explicitly defines that split.

### 3.8 Previous known-good state

Before risk-bearing activation, verify:

- `previous` resolves to a complete compatible Release Set;
- previous artifacts remain available;
- previous configuration remains interpretable;
- rollback has been tested;
- migrations have a safe rollback boundary or tested forward repair;
- backup and restore remain available.

## 4. Inputs

### 4.1 Required variables

The reference helper uses:

| Variable | Meaning |
| --- | --- |
| `KOA_PROFILE_MANIFEST` | Active control-plane profile artifact |
| `KOA_RELEASE_ROOT` | Parent directory of immutable Release Sets |
| `KOA_RELEASE_SET_ID` | Exact staged Release Set identity |
| `KOA_ACTIVE_LINK` | Active Release Set link consumed by units |
| `KOA_PREVIOUS_LINK` | Previous compatible Release Set link |
| `KOA_LOCK_FILE` | Exclusive activation lock |
| `KOA_SYSTEMCTL_SCOPE` | `system` or `user` |
| `KOA_UNITS` | Space-separated systemd units |
| `KOA_READY_URLS` | Space-separated readiness URLs |
| `KOA_READY_TIMEOUT_SECONDS` | Timeout for each readiness request |

### 4.2 Reference environment file

Create a reviewed environment file such as:

```bash
KOA_PROFILE_MANIFEST=/etc/koa/authority/control-plane-profile.json
KOA_RELEASE_ROOT=/var/lib/koa/releases
KOA_RELEASE_SET_ID=rs-2026.08.03-cp-001

KOA_ACTIVE_LINK=/var/lib/koa/control-plane/active
KOA_PREVIOUS_LINK=/var/lib/koa/control-plane/previous
KOA_LOCK_FILE=/run/lock/koa/control-plane-deploy.lock

KOA_SYSTEMCTL_SCOPE=system

KOA_UNITS="\
koa-identity-trust.service \
koa-governance-policy-runtime.service \
koa-resource-governor.service \
koa-audit-broker.service \
koa-publication-gateway.service"

KOA_READY_URLS="\
https://127.0.0.1:9441/ready \
https://127.0.0.1:9442/ready \
https://127.0.0.1:9443/ready \
https://127.0.0.1:9444/ready \
https://127.0.0.1:9445/ready"

KOA_READY_TIMEOUT_SECONDS=10
```

The units and URLs are examples.

The active profile and component contracts own the actual service set and endpoints.

### 4.3 Reference release layout

```text
/var/lib/koa/releases/
└── rs-2026.08.03-cp-001/
    ├── release-set.json
    ├── system/
    ├── services/
    ├── governance/
    └── knowledge/
```

The active and previous links are mutable selectors outside immutable release content:

```text
/var/lib/koa/control-plane/active
/var/lib/koa/control-plane/previous
```

### 4.4 Reference service model

A systemd unit can run:

- a native service binary;
- a rootless or system-scoped OCI container;
- a profile-approved wrapper that resolves the active Release Set.

The unit does not use a mutable image tag as release identity.

The resolved immutable artifact identity remains in the Release Set and service evidence.

### 4.5 Reference endpoint model

Without Kubernetes, endpoints can use:

- loopback;
- statically declared private addresses;
- profile-owned DNS;
- a profile-approved reverse proxy;
- mutual TLS;
- registered component interfaces.

Service discovery remains explicit.

A component cannot discover authority merely because another process listens on a port.

## 5. Safety and Authority Boundaries

### 5.1 No Kubernetes dependency

A valid non-Kubernetes deployment does not require:

- Kubernetes API access;
- kubeconfig;
- pods;
- Deployments;
- StatefulSets;
- DaemonSets;
- Services;
- Ingress;
- Kubernetes Secrets;
- ConfigMaps;
- persistent-volume claims;
- Kubernetes network policies;
- Helm releases;
- Kustomize overlays;
- operators or custom resources.

A systemd service can still run an OCI container.

That does not make the deployment Kubernetes-based.

### 5.2 Component data ownership

Each component retains its own:

- database identity;
- schema or database;
- file or object namespace;
- queue or topic permissions;
- migration user;
- backup and restore contract;
- authoritative state transitions.

A shared database server can be used only when the profile preserves enforceable logical separation.

A shared unrestricted database owner does not support conformance.

### 5.3 Service identities

Every service uses a dedicated identity.

Do not deploy all units as:

```text
root
koa
platform-admin
```

unless the active profile and component contracts explicitly define a bounded identity model that preserves independent permissions.

### 5.4 Privilege

Use system services only when the profile requires system scope.

Rootless services can use:

```text
KOA_SYSTEMCTL_SCOPE=user
```

with a dedicated service account and persistent user manager where the profile permits it.

Privileged operations use a closed allowlist.

A general root shell is not the normal deployment interface.

### 5.5 Network

Network policy defaults to deny.

Permit only declared:

- source identities;
- destination identities;
- addresses;
- ports;
- protocols;
- purposes;
- directions.

A local reverse proxy does not become a component owner.

TLS termination does not create application authorization.

### 5.6 Secrets

Environment files used by this recipe contain references and non-secret configuration only.

Secret values remain in:

- profile-approved credentials;
- protected files;
- service-manager credentials;
- secret stores;
- hardware-backed or local protected stores.

Do not place secrets in:

- unit files;
- Compose files;
- images;
- command lines;
- release manifests;
- logs;
- evidence.

### 5.7 Containers

When using Podman or Docker:

- image identity is immutable;
- writable storage is component-scoped;
- networks are profile-scoped;
- secrets are dedicated;
- resource limits are explicit;
- health and readiness are distinct;
- host networking is avoided unless explicitly required;
- privileged mode is avoided;
- broad host mounts are avoided.

A container runtime does not define component authority.

### 5.8 AI boundary

The control plane contains no native AI baseline.

External AI is not used for:

- policy;
- resource scheduling;
- deployment selection;
- release activation;
- migration;
- restore;
- incident containment;
- canonical data repair.

Approved external AI remains explicit, optional, candidate-only, and profile-conditioned under `ADR-014`.

### 5.9 Release boundary

The deployment activates one complete compatible Release Set.

It does not activate a subset of:

- service artifacts;
- system artifacts;
- governance artifacts;
- knowledge artifacts;
- schemas;
- policies;
- migrations.

Independent updates are allowed only when compatibility remains valid.

## 6. Procedure

### 6.1 Create a local deployment-tool directory

Reference location:

```bash
sudo install \
  --directory \
  --owner root \
  --group root \
  --mode 0750 \
  /var/lib/koa/recipe-tools/control-plane
```

For user-scoped services, use the dedicated service account's protected state directory instead.

### 6.2 Install the reference helper

```bash
sudo tee \
  /var/lib/koa/recipe-tools/control-plane/koa-control-plane-deploy \
  >/dev/null <<'BASH'
#!/usr/bin/env bash
set -euo pipefail

fail() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

usage() {
  cat >&2 <<'USAGE'
Usage:
  koa-control-plane-deploy preflight <environment-file>
  koa-control-plane-deploy activate  <environment-file>
  koa-control-plane-deploy status    <environment-file>
  koa-control-plane-deploy rollback  <environment-file>
USAGE
  exit 2
}

require_command() {
  command -v "$1" >/dev/null 2>&1 ||
    fail "required command not found: $1"
}

require_variable() {
  local name=$1
  [ -n "${!name:-}" ] ||
    fail "required variable is unset or empty: $name"
}

require_file() {
  [ -f "$1" ] || fail "required file not found: $1"
}

require_directory() {
  [ -d "$1" ] || fail "required directory not found: $1"
}

load_environment() {
  local environment_file=$1

  require_file "$environment_file"

  # The environment file contains non-secret deployment references.
  # shellcheck disable=SC1090
  . "$environment_file"

  require_variable KOA_PROFILE_MANIFEST
  require_variable KOA_RELEASE_ROOT
  require_variable KOA_RELEASE_SET_ID
  require_variable KOA_ACTIVE_LINK
  require_variable KOA_PREVIOUS_LINK
  require_variable KOA_LOCK_FILE
  require_variable KOA_SYSTEMCTL_SCOPE
  require_variable KOA_UNITS
  require_variable KOA_READY_URLS

  case "$KOA_SYSTEMCTL_SCOPE" in
    system|user)
      ;;
    *)
      fail "KOA_SYSTEMCTL_SCOPE must be system or user"
      ;;
  esac

  KOA_RELEASE_DIRECTORY="${KOA_RELEASE_ROOT%/}/${KOA_RELEASE_SET_ID}"
  KOA_RELEASE_MANIFEST="${KOA_RELEASE_DIRECTORY%/}/release-set.json"

  export KOA_RELEASE_DIRECTORY
  export KOA_RELEASE_MANIFEST
}

systemctl_command() {
  if [ "$KOA_SYSTEMCTL_SCOPE" = "user" ]; then
    systemctl --user "$@"
  else
    systemctl "$@"
  fi
}

check_manifest_content() {
  python3 - "$KOA_PROFILE_MANIFEST" "$KOA_RELEASE_MANIFEST" <<'PY'
import json
import sys
from pathlib import Path

profile_path = Path(sys.argv[1])
release_path = Path(sys.argv[2])

profile = json.loads(profile_path.read_text(encoding="utf-8"))
release = json.loads(release_path.read_text(encoding="utf-8"))

def strings(value):
    if isinstance(value, dict):
        for item in value.values():
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)
    elif isinstance(value, str):
        yield value

profile_strings = set(strings(profile))
release_strings = set(strings(release))

if "control_plane" not in profile_strings:
    raise SystemExit(
        "profile manifest does not identify control_plane"
    )

if "kubernetes" in profile_strings:
    raise SystemExit(
        "profile manifest selects Kubernetes; use the Kubernetes deployment path"
    )

required_channels = {
    "system",
    "services",
    "governance",
    "knowledge",
}
missing = sorted(required_channels - release_strings)
if missing:
    raise SystemExit(
        "release manifest is missing required channels: "
        + ", ".join(missing)
    )
PY
}

check_environment_file_permissions() {
  local environment_file=$1
  local mode

  mode=$(stat -c '%a' "$environment_file")

  case "$mode" in
    *[2367][0-7]|??[2367])
      fail "environment file is group- or world-writable: $environment_file"
      ;;
  esac
}

check_release_permissions() {
  local first_writable

  first_writable=$(
    find -L "$KOA_RELEASE_DIRECTORY" -xdev -perm /022 -print -quit
  )

  [ -z "$first_writable" ] ||
    fail "release content is group- or world-writable: $first_writable"
}

check_profile_and_release() {
  require_file "$KOA_PROFILE_MANIFEST"
  require_file "$KOA_RELEASE_MANIFEST"
  check_manifest_content ||
    fail "profile or Release Set manifest validation failed"
}

check_tools() {
  require_command python3
  require_command systemctl
  require_command readlink
  require_command stat
  require_command find
  require_command flock
  require_command curl
  require_command ln
  require_command mv
}

check_units() {
  local unit
  for unit in $KOA_UNITS; do
    systemctl_command cat "$unit" >/dev/null 2>&1 ||
      fail "unit is not installed or readable: $unit"
  done
}

check_no_kubernetes_commands() {
  local unit rendered

  for unit in $KOA_UNITS; do
    rendered=$(systemctl_command cat "$unit")
    if printf '%s\n' "$rendered" |
      grep -Eiq '(^|[[:space:]/])(kubectl|kubelet|kubeadm|helm|kustomize)([[:space:]]|$)|kubeconfig|/var/lib/kubelet'; then
      fail "Kubernetes-specific command or path found in unit: $unit"
    fi
  done
}

ready_check() {
  local url
  for url in $KOA_READY_URLS; do
    curl \
      --fail \
      --silent \
      --show-error \
      --max-time "${KOA_READY_TIMEOUT_SECONDS:-10}" \
      "$url" >/dev/null ||
      fail "readiness check failed: $url"
  done
}

check_active_units() {
  local unit
  for unit in $KOA_UNITS; do
    systemctl_command is-active --quiet "$unit" ||
      fail "unit is not active: $unit"
  done
}

atomic_link() {
  local target=$1
  local link=$2
  local parent temporary

  parent=$(dirname "$link")
  mkdir -p "$parent"

  temporary="${link}.new.$$"
  rm -f "$temporary"
  ln -s "$target" "$temporary"
  mv -Tf "$temporary" "$link"
}

record_previous_target() {
  local current

  if [ -L "$KOA_ACTIVE_LINK" ]; then
    current=$(readlink -f "$KOA_ACTIVE_LINK")
    [ -n "$current" ] ||
      fail "active link cannot be resolved: $KOA_ACTIVE_LINK"
    atomic_link "$current" "$KOA_PREVIOUS_LINK"
  fi
}

restart_units() {
  local unit

  systemctl_command daemon-reload

  for unit in $KOA_UNITS; do
    systemctl_command restart "$unit"
  done
}

preflight() {
  local environment_file=$1

  check_tools
  check_environment_file_permissions "$environment_file"
  require_directory "$KOA_RELEASE_DIRECTORY"
  check_release_permissions
  check_profile_and_release
  check_units
  check_no_kubernetes_commands

  printf 'preflight: pass\n'
  printf 'release_set_id=%s\n' "$KOA_RELEASE_SET_ID"
  printf 'release_directory=%s\n' "$KOA_RELEASE_DIRECTORY"
  printf 'systemctl_scope=%s\n' "$KOA_SYSTEMCTL_SCOPE"
}

activate() {
  local environment_file=$1
  local old_target=''

  preflight "$environment_file"

  mkdir -p "$(dirname "$KOA_LOCK_FILE")"
  exec 9>"$KOA_LOCK_FILE"
  flock -x 9

  if [ -L "$KOA_ACTIVE_LINK" ]; then
    old_target=$(readlink -f "$KOA_ACTIVE_LINK")
  fi

  record_previous_target
  atomic_link "$KOA_RELEASE_DIRECTORY" "$KOA_ACTIVE_LINK"

  if ! restart_units; then
    if [ -n "$old_target" ] && [ -d "$old_target" ]; then
      atomic_link "$old_target" "$KOA_ACTIVE_LINK"
      systemctl_command daemon-reload
      restart_units || true
    fi
    fail "unit restart failed during activation"
  fi

  if ! check_active_units || ! ready_check; then
    if [ -n "$old_target" ] && [ -d "$old_target" ]; then
      atomic_link "$old_target" "$KOA_ACTIVE_LINK"
      systemctl_command daemon-reload
      restart_units || true
    fi
    fail "initial acceptance failed during activation"
  fi

  printf 'activation: pass\n'
  printf 'active_release=%s\n' "$(readlink -f "$KOA_ACTIVE_LINK")"
  if [ -L "$KOA_PREVIOUS_LINK" ]; then
    printf 'previous_release=%s\n' \
      "$(readlink -f "$KOA_PREVIOUS_LINK")"
  fi
}

status() {
  check_profile_and_release
  check_units
  check_no_kubernetes_commands

  printf 'active_release=%s\n' \
    "$(readlink -f "$KOA_ACTIVE_LINK" 2>/dev/null || true)"
  printf 'previous_release=%s\n' \
    "$(readlink -f "$KOA_PREVIOUS_LINK" 2>/dev/null || true)"

  local unit
  for unit in $KOA_UNITS; do
    printf '%s=' "$unit"
    systemctl_command is-active "$unit" 2>/dev/null || true
  done

  ready_check
  printf 'readiness=pass\n'
}

rollback() {
  local previous_target current_target=''

  [ -L "$KOA_PREVIOUS_LINK" ] ||
    fail "previous release link does not exist: $KOA_PREVIOUS_LINK"

  previous_target=$(readlink -f "$KOA_PREVIOUS_LINK")
  require_directory "$previous_target"

  mkdir -p "$(dirname "$KOA_LOCK_FILE")"
  exec 9>"$KOA_LOCK_FILE"
  flock -x 9

  if [ -L "$KOA_ACTIVE_LINK" ]; then
    current_target=$(readlink -f "$KOA_ACTIVE_LINK")
  fi

  atomic_link "$previous_target" "$KOA_ACTIVE_LINK"

  if ! restart_units; then
    if [ -n "$current_target" ] && [ -d "$current_target" ]; then
      atomic_link "$current_target" "$KOA_ACTIVE_LINK"
      systemctl_command daemon-reload
      restart_units || true
    fi
    fail "unit restart failed during rollback"
  fi

  check_active_units
  ready_check

  printf 'rollback: pass\n'
  printf 'active_release=%s\n' "$(readlink -f "$KOA_ACTIVE_LINK")"
}

main() {
  [ "$#" -eq 2 ] || usage

  local command_name=$1
  local environment_file=$2

  load_environment "$environment_file"

  case "$command_name" in
    preflight)
      preflight "$environment_file"
      ;;
    activate)
      activate "$environment_file"
      ;;
    status)
      status
      ;;
    rollback)
      rollback
      ;;
    *)
      usage
      ;;
  esac
}

main "$@"
BASH

sudo chown root:root \
  /var/lib/koa/recipe-tools/control-plane/koa-control-plane-deploy

sudo chmod 0750 \
  /var/lib/koa/recipe-tools/control-plane/koa-control-plane-deploy

sudo bash -n \
  /var/lib/koa/recipe-tools/control-plane/koa-control-plane-deploy
```

Review the helper before operational use.

It is an example, not deployment authority.

### 6.3 Install the environment file

```bash
sudo install \
  --owner root \
  --group root \
  --mode 0640 \
  ./control-plane-deploy.env \
  /etc/koa/control-plane-deploy.env
```

Check for accidental secret values:

```bash
sudo grep -nEi \
  '(password|private[_-]?key|secret[[:space:]]*=|token[[:space:]]*=)' \
  /etc/koa/control-plane-deploy.env && {
    printf '%s\n' 'possible secret material detected' >&2
    exit 1
  } || true
```

Review all matches manually.

### 6.4 Validate the active profile and Release Set

Run the canonical profile, artifact, trust, migration, and Release Set validators.

Confirm:

- primary profile is `control_plane`;
- orchestration mode is non-Kubernetes;
- overlays are compatible;
- all selected component contracts resolve;
- artifact integrity and provenance pass;
- signatures and trust pass;
- revocation passes;
- migrations and forward repair resolve;
- previous known-good state exists;
- resources and storage capacity are sufficient;
- required evidence paths are available.

The helper performs only recipe-level sanity checks.

### 6.5 Inspect unit definitions

For each unit:

```bash
sudo systemctl cat koa-governance-policy-runtime.service
sudo systemctl show koa-governance-policy-runtime.service \
  --property=User \
  --property=Group \
  --property=NoNewPrivileges \
  --property=ProtectSystem \
  --property=ProtectHome \
  --property=PrivateTmp \
  --property=PrivateDevices \
  --property=CapabilityBoundingSet \
  --property=RestrictAddressFamilies \
  --property=IPAddressDeny \
  --property=IPAddressAllow \
  --property=ReadOnlyPaths \
  --property=ReadWritePaths
```

Repeat for all selected units.

Confirm each unit:

- resolves artifacts through the active Release Set;
- uses its own identity;
- has only required writable paths;
- has only required network access;
- has only required secrets;
- has bounded resources;
- does not use Kubernetes commands or kubeconfig;
- does not write another component's storage.

### 6.6 Inspect OCI runtime configuration

Podman examples:

```bash
podman info
podman ps --all
podman network ls
podman volume ls
```

Docker examples:

```bash
docker info
docker ps --all
docker network ls
docker volume ls
```

Use only the runtime selected by the profile.

Verify no container uses:

- mutable release tags as authority;
- unrestricted host networking;
- broad root filesystem mounts;
- foreign component data volumes;
- shared production credentials;
- privileged mode without an explicit contract.

### 6.7 Validate storage ownership

Inventory database and storage identities.

Example PostgreSQL inspection:

```bash
sudo -u postgres psql --no-psqlrc --command '\du'
sudo -u postgres psql --no-psqlrc --command '\l'
```

For each component, verify:

- runtime user;
- migration user;
- backup user;
- restore user;
- owned database or schema;
- foreign grants;
- tenant or domain scope.

Do not change grants through this recipe without the active storage and migration authority.

### 6.8 Validate network listeners

```bash
sudo ss --listening --tcp --udp --numeric --process
```

Map every listener to:

- component;
- service identity;
- profile;
- interface;
- port;
- protocol;
- purpose;
- authentication;
- network policy.

Unknown listeners block activation.

### 6.9 Run preflight

```bash
sudo \
  /var/lib/koa/recipe-tools/control-plane/koa-control-plane-deploy \
  preflight \
  /etc/koa/control-plane-deploy.env
```

Expected result:

```text
preflight: pass
```

The helper checks:

- commands;
- environment-file permissions;
- staged Release Set;
- required release-channel names;
- control-plane profile identity;
- absence of a `kubernetes` profile selection;
- unit availability;
- absence of Kubernetes-specific commands and paths in the selected units;
- release-directory permissions.

### 6.10 Activate atomically

```bash
sudo \
  /var/lib/koa/recipe-tools/control-plane/koa-control-plane-deploy \
  activate \
  /etc/koa/control-plane-deploy.env
```

The helper:

1. repeats preflight;
2. takes an exclusive lock;
3. records the current active target as `previous`;
4. atomically switches `active`;
5. reloads systemd;
6. restarts selected units;
7. checks unit active state;
8. checks every readiness URL;
9. attempts rollback on initial failure.

The helper does not perform database migrations.

Migrations occur through each owning component's migration contract before the activation point defined by the Release Set.

### 6.11 Inspect deployment status

```bash
sudo \
  /var/lib/koa/recipe-tools/control-plane/koa-control-plane-deploy \
  status \
  /etc/koa/control-plane-deploy.env
```

Inspect bounded service state:

```bash
sudo systemctl show \
  koa-identity-trust.service \
  koa-governance-policy-runtime.service \
  koa-resource-governor.service \
  koa-audit-broker.service \
  koa-publication-gateway.service \
  --property=ActiveState \
  --property=SubState \
  --property=Result \
  --property=NRestarts \
  --property=ExecMainStatus
```

### 6.12 Validate control separation

Run registered tests demonstrating:

- Governance Policy Runtime does not allocate CPU, memory, queues, or worker placement;
- Resource Governor does not grant application or policy authority;
- Publication Gateway does not mutate source component data;
- UCKK Dimension Gateway remains distinct where selected;
- Audit Broker remains evidence infrastructure;
- privileged operations use the closed broker;
- no service shares unrestricted foreign credentials.

### 6.13 Validate service readiness

For each readiness URL, validate:

- identity;
- trust;
- policy dependencies;
- storage access;
- migration state;
- queue state;
- evidence path;
- required local artifacts;
- degraded behavior.

A running process or container is not readiness.

### 6.14 Validate failure isolation

Stop one non-critical selected service in a controlled test:

```bash
sudo systemctl stop koa-publication-gateway.service
```

Verify:

- unrelated control-plane services remain available;
- source component data remains unchanged;
- publication becomes explicitly unavailable;
- no direct publication fallback appears;
- no external AI fallback appears;
- alerts and evidence identify the affected capability.

Restore the service:

```bash
sudo systemctl start koa-publication-gateway.service
```

Then rerun its readiness test.

### 6.15 Validate no Kubernetes dependency

Inspect processes and files:

```bash
ps -ef |
  grep -E '[k]ube(apiserver|let|proxy|scheduler|controller)|[k]ubectl|[h]elm' &&
  {
    printf '%s\n' 'unexpected Kubernetes process or command found' >&2
    exit 1
  } || true
```

Inspect units and configuration for:

```text
kubeconfig
/var/lib/kubelet
/etc/kubernetes
kubectl
kubelet
kubeadm
helm
kustomize
```

Matches in documentation or historical evidence are not runtime dependencies. Review matches in active units, scripts, environment, and profile configuration.

### 6.16 Record evidence

Record references to:

- effective profile;
- target and previous Release Sets;
- artifact verification;
- unit inventory;
- runtime inventory;
- service identities;
- storage permissions;
- network listeners;
- readiness results;
- control-separation tests;
- failure-isolation test;
- non-Kubernetes dependency test;
- activation or rollback;
- final disposition.

Do not place secrets or unrestricted payloads in receipts.

## 7. Validation

### 7.1 Acceptance matrix

| Control | Expected result |
| --- | --- |
| Primary profile is `control_plane` | pass |
| Orchestration mode is non-Kubernetes | pass |
| Selected overlays are compatible | pass |
| Exact Release Set is verified | pass |
| All four release channels are compatible | pass |
| Previous known-good Release Set exists | pass |
| Selected units are installed | pass |
| Units contain no Kubernetes runtime dependency | pass |
| Each service has a distinct identity | pass |
| Storage and database ownership are enforceable | pass |
| Network listeners are declared | pass |
| Secrets remain outside units and manifests | pass |
| OCI images use immutable identities | pass or not applicable |
| Governance and resource authority remain separate | pass |
| Publication and UCKK gateways remain separate | pass or not applicable |
| Component readiness passes | pass |
| Failure isolation passes | pass |
| Atomic activation passes | pass |
| Rollback passes | pass |
| Required evidence validates | pass |

### 7.2 Expected test coverage

The active test catalog owns exact identifiers.

Expected coverage includes:

```text
TEST-CP-NOK8S-001  Control-plane profile resolution
TEST-CP-NOK8S-002  Non-Kubernetes orchestration selection
TEST-CP-NOK8S-003  Exact Release Set closure
TEST-CP-NOK8S-004  Unit and artifact identity
TEST-CP-NOK8S-005  No Kubernetes runtime dependency
TEST-CP-NOK8S-006  Distinct service identities
TEST-CP-NOK8S-007  Database and storage ownership
TEST-CP-NOK8S-008  Default-deny network behavior
TEST-CP-NOK8S-009  Secret isolation
TEST-CP-NOK8S-010  OCI runtime profile compliance
TEST-CP-NOK8S-011  Governance and resource separation
TEST-CP-NOK8S-012  Gateway separation
TEST-CP-NOK8S-013  Component readiness
TEST-CP-NOK8S-014  Capability-scoped failure
TEST-CP-NOK8S-015  Atomic activation
TEST-CP-NOK8S-016  Known-good rollback
TEST-CP-NOK8S-017  Backup and restore readiness
TEST-CP-NOK8S-018  Evidence completeness
```

### 7.3 Negative tests

Negative validation includes:

- foreign database write denied;
- foreign queue access denied;
- undeclared listener denied;
- broad service credential rejected;
- Kubernetes-specific unit rejected;
- incomplete Release Set rejected;
- missing previous Release Set blocks activation;
- failed readiness triggers rollback;
- external AI does not enter deployment or recovery;
- skipped checks remain non-passing.

### 7.4 Terminal results

Use:

```text
pass
fail
blocked
unavailable
incomplete
not applicable
```

Do not report `pass` when:

- Kubernetes dependency detection was skipped;
- one component readiness check is unavailable;
- database grants were not inspected;
- a required migration is unresolved;
- rollback was not demonstrated;
- backup and restore readiness are unknown;
- evidence is incomplete.

### 7.5 Observation period

After activation, monitor for the profile-defined interval:

- unit restarts;
- readiness;
- latency;
- queue age;
- resource pressure;
- database errors;
- foreign-access denials;
- evidence delivery;
- unexpected network connections;
- configuration drift;
- Release Set identity drift.

The previous Release Set remains retained until the rollback window closes.

## 8. Cleanup

### 8.1 Inactive failed candidate

When activation never completed:

1. verify `active` does not point to the candidate;
2. preserve validation and failure evidence;
3. keep the prior Release Set active;
4. remove temporary credentials and network allowances;
5. retain or retire the candidate through artifact lifecycle.

### 8.2 Temporary deployment helper

Remove the helper when it was created only for this recipe:

```bash
sudo rm -f \
  /var/lib/koa/recipe-tools/control-plane/koa-control-plane-deploy
```

Keep it only when it becomes a reviewed, managed operational tool.

### 8.3 Temporary service overrides

Remove temporary drop-ins and overrides created during testing:

```bash
sudo systemctl revert <unit-name>
sudo systemctl daemon-reload
```

Replace `<unit-name>` only after resolving the exact target.

Do not revert production configuration blindly.

### 8.4 Temporary OCI resources

Remove only workspace- or deployment-scoped resources that are no longer referenced.

Podman examples:

```bash
podman ps --all
podman network ls
podman volume ls
```

Docker examples:

```bash
docker ps --all
docker network ls
docker volume ls
```

Do not delete component-owned durable volumes through a generic cleanup command.

### 8.5 Temporary credentials and access

After activation or rollback:

- close temporary privilege;
- revoke temporary tokens;
- remove temporary mounts;
- close temporary firewall rules;
- remove temporary database grants;
- remove temporary debug endpoints;
- remove temporary operator accounts.

### 8.6 Cleanup verification

Verify:

- no `.new.*` active-link files remain;
- `active` and `previous` resolve;
- no undeclared unit override remains;
- no temporary container, network, or volume remains;
- no temporary credential remains;
- no debug listener remains;
- no Kubernetes runtime or configuration was introduced;
- retained artifacts and evidence are intentional.

## 9. Rollback or Safe Exit

### 9.1 Rollback conditions

Rollback when:

- one required unit fails;
- one readiness check fails;
- control separation fails;
- foreign data access succeeds;
- a required listener is missing or undeclared;
- a Kubernetes dependency appears;
- resource pressure removes critical capability;
- migration compatibility is disproved;
- Release Set identity is inconsistent;
- evidence-critical transitions cannot be recorded.

### 9.2 Execute rollback

```bash
sudo \
  /var/lib/koa/recipe-tools/control-plane/koa-control-plane-deploy \
  rollback \
  /etc/koa/control-plane-deploy.env
```

The helper atomically restores `previous`, restarts units, and checks readiness.

### 9.3 Verify rollback

Repeat:

- Release Set identity;
- unit active state;
- readiness;
- storage and database compatibility;
- policy and resource separation;
- gateway separation;
- network listeners;
- failure isolation;
- evidence delivery.

Quarantine the failed candidate.

### 9.4 Rollback failure

When rollback fails:

1. stop normal traffic admission;
2. preserve evidence;
3. isolate affected services;
4. enter the profile-owned recovery procedure;
5. verify active and previous Release Set artifacts;
6. restore trust, policy, storage, and component state as required;
7. run migrations or forward repair;
8. rerun complete readiness;
9. keep the control plane blocked until acceptance.

### 9.5 Forward repair

Use forward repair when an irreversible migration or state change prevents rollback.

The forward-repair path already exists and has been tested before activation.

Do not perform ad hoc direct database edits.

### 9.6 Safe exit before activation

Before activation:

- leave the candidate inactive;
- leave `active` and `previous` unchanged;
- remove temporary access;
- preserve validation evidence;
- close the change record with the actual terminal result.

## 10. Failure Handling

| Failure | Required response |
| --- | --- |
| Active profile is not `control_plane` | Stop and use the correct profile recipe |
| Profile selects Kubernetes | Stop and use the Kubernetes deployment path |
| Release Set is incomplete | Keep it inactive |
| Previous Release Set is missing | Block risk-bearing activation |
| Unit is missing | Keep activation blocked |
| Unit invokes Kubernetes tooling | Reject the non-Kubernetes deployment |
| Service identity is shared broadly | Replace it with scoped identities |
| Foreign database grant exists | Revoke or isolate and investigate |
| Unknown listener exists | Block acceptance and resolve ownership |
| Secret appears in unit or environment file | Remove and rotate through protected secret delivery |
| Mutable image tag is the only identity | Resolve immutable artifact identity |
| Readiness fails | Attempt rollback |
| Process is active but readiness fails | Keep capability unavailable |
| Governance Policy Runtime allocates resources | Reject deployment boundary |
| Resource Governor grants application authority | Reject deployment boundary |
| Publication Gateway writes source data | Isolate path and block conformance |
| External AI appears in deployment control | Disable it and block acceptance |
| OCI runtime fails | Degrade affected services and preserve non-containerized capabilities |
| Database migration fails | Stop at the owner-defined checkpoint |
| Rollback is unsafe | Execute tested forward repair |
| Rollback fails | Enter profile-owned recovery |
| Evidence path is unavailable | Preserve bounded local evidence and block evidence-critical closure |
| Validation is incomplete | Preserve the prior valid state and report the actual result |

### 10.1 Unexpected Kubernetes dependency

When active configuration contains Kubernetes-specific behavior:

1. stop the affected activation;
2. identify the unit, script, package, or profile source;
3. preserve evidence;
4. determine whether the profile was misclassified;
5. either remove the dependency or select the Kubernetes deployment path;
6. rerun profile and Release Set validation.

Do not hide a Kubernetes dependency behind a shell wrapper.

### 10.2 Unexpected cross-component write

When one service can write another component's storage:

1. isolate the service;
2. revoke the credential or grant;
3. preserve evidence;
4. verify whether unauthorized mutation occurred;
5. restore owner-controlled state if required;
6. rerun canonical ownership tests;
7. keep the Release Set nonconformant until closure.

### 10.3 Runtime drift

Drift can include:

- changed unit files;
- changed image identity;
- changed service user;
- changed network rule;
- changed database grant;
- changed volume mount;
- changed secret reference;
- changed active link;
- changed profile manifest.

Block new conformance claims until drift is reconciled through accepted change or restored canonical configuration.

### 10.4 Failed cleanup

A failed cleanup leaves the deployment change open.

Record:

- residual unit override;
- residual container;
- residual network;
- residual volume;
- residual credential;
- residual database grant;
- residual listener;
- retained Release Set;
- next safe action.

Do not present the environment as clean until residual state is resolved.

## 11. References

### 11.1 Canonical references

```text
generated/profile-catalog.json
contracts/profiles/control-plane.profile.json
contracts/release-channels.contract.json
contracts/artifact-classes.contract.json
generated/component-catalog.json
contracts/integration-types.contract.json
generated/test-catalog.json
generated/evidence-catalog.json
```

### 11.2 Decisions and locks

```text
DEC-PROFILE-001
DEC-CONTAINER-001
DEC-K8S-001
DEC-DATA-001
DEC-GOV-001
DEC-GATE-001
DEC-AI-001
DEC-REL-001

LOCK-PROFILE-001
LOCK-IMPL-001
LOCK-IMPL-002
LOCK-DATA-001
LOCK-GOV-001
LOCK-GATE-001
LOCK-AI-001
LOCK-AI-002
LOCK-LIFE-001
LOCK-LIFE-002
LOCK-LIFE-003
LOCK-LIFE-004
```

### 11.3 Related documents

```text
11-recipes/README.md
02-system/02-logical-architecture.md
02-system/04-component-boundaries.md
02-system/07-communication-model.md
02-system/14-resource-governor.md
02-system/15-governance-policy-runtime.md
02-system/16-external-integrations.md
02-system/17-capability-degradation.md
05-development/06-service-containers.md
05-development/16-development-to-release-transition.md
07-security/01-security-baseline.md
07-security/08-network-boundaries.md
08-operations/00-operating-model.md
08-operations/09-restore.md
09-conformance/10-canonical-ownership-validation.md
10-adrs/ADR-014-strict-external-ai-boundary.md
```

### 11.4 Recipe validation status

During generation:

- the metadata block was parsed;
- all 11 recipe sections were found;
- the embedded helper passed Bash syntax validation;
- helper preflight, atomic activation, status, and rollback were exercised against disposable profile, Release Set, unit, and readiness fixtures;
- the test fixture used simulated `systemctl` and `curl`;
- the document does not claim that deployment-specific systemd, OCI runtime, database, network, migration, backup, restore, or component-readiness tests executed.

The active test catalog and evidence registry determine deployment conformance.
