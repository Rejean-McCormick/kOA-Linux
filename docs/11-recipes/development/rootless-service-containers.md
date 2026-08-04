<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-RECIPE-DEV-ROOTLESS-001",
  "document_class": "recipe",
  "status": "active",
  "language": "en",
  "layer": "recipe",
  "scope": [
    "developer_linux_workstation",
    "developer_windows_wsl"
  ],
  "canonical_refs": [
    "generated/decision-index.json",
    "generated/profile-catalog.json",
    "contracts/profiles/developer-linux-workstation.profile.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "contracts/artifact-contracts/workspace-port-allocation.schema.json",
    "contracts/artifact-contracts/resource-envelope.schema.json",
    "contracts/components/resource-governor.component.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json"
  ],
  "decision_ids": [
    "DEC-DEV-001",
    "DEC-DEV-002",
    "DEC-CONTAINER-001",
    "DEC-DATA-001",
    "DEC-GOV-001"
  ],
  "requirement_ids": [
    "REQ-DEV-IDENT-001",
    "REQ-DEV-IDENT-002",
    "REQ-DEV-IDENT-003",
    "REQ-DEV-IDENT-004",
    "REQ-DEV-IDENT-005",
    "REQ-DEV-IDENT-006",
    "REQ-DEV-IDENT-009",
    "REQ-DEV-IDENT-010",
    "REQ-DEV-IDENT-013",
    "REQ-DEV-IDENT-014",
    "REQ-DEV-IDENT-015",
    "REQ-DEV-IDENT-016",
    "REQ-DEV-IDENT-017",
    "REQ-DEV-IDENT-018",
    "REQ-DEV-IDENT-020",
    "REQ-DEV-IDENT-021",
    "REQ-DEV-IDENT-023"
  ],
  "lock_ids": [
    "LOCK-DEV-001",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DEV-005",
    "LOCK-DATA-001",
    "LOCK-PROFILE-001",
    "LOCK-IMPL-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-PROFILE-001",
    "DOC-SYS-005",
    "DOC-SYS-014",
    "DOC-DEV-009",
    "DOC-OPS-001",
    "DOC-CONF-002"
  ],
  "tags": [
    "recipe",
    "development",
    "rootless-containers",
    "podman",
    "workspace-isolation",
    "service-containers",
    "ports",
    "secrets",
    "volumes",
    "cleanup"
  ],
  "normative": false
}
KOA:DOC-META:END -->

# Rootless Service Containers for Development

> **Recipe status:** Non-normative implementation guidance.  
> Canonical profile, component, toolchain, artifact, security, and resource contracts take precedence.

## 1. Purpose

This recipe shows one way to run mutable development infrastructure in rootless service containers while preserving workspace isolation.

The example uses Podman and two services:

- PostgreSQL;
- Redis.

The same naming, isolation, secret, port, resource, and cleanup model can be adapted to Solr, Elasticsearch, queues, OpenRefine, or other development services after their component and resource contracts are reviewed.

This recipe demonstrates:

- one stable `workspace_id`;
- deterministic names for containers, networks, volumes, secrets, databases, and users;
- fixed service ports inside an isolated workspace network;
- host ports obtained from a workspace allocation artifact;
- loopback-only host exposure;
- service-specific secret injection;
- bounded resources;
- explicit cleanup that does not affect another workspace.

## 2. Applicability and Preconditions

Use this recipe when:

- the effective profile is `developer_linux_workstation`, or `developer_windows_wsl` with a supported rootless Podman setup;
- the application contract permits OCI service containers;
- a stable workspace identity exists or can be created locally;
- host ports are reserved through a workspace-scoped allocation artifact;
- service data is development-only or has an explicit backup requirement;
- the host provides user namespaces and rootless container support;
- Podman, `jq`, `git`, `openssl`, and standard POSIX shell tools are available.

This recipe does not cover:

- rootful container daemons;
- Docker Desktop-specific behavior;
- Kubernetes;
- production or sovereign deployment;
- release signing;
- production credentials;
- shared mutable databases across workspaces;
- privileged containers;
- host-network containers;
- automatic exposure to the local network.

For Windows/WSL, use this recipe only when the toolchain contract confirms rootless Podman behavior. Validate loopback publication from both the WSL distribution and Windows host. When rootless mode is unavailable, select another approved development recipe rather than silently changing the security model.

## 3. Canonical References and Boundaries

This recipe implements one possible mechanism for existing architecture decisions.

| Concern | Canonical owner |
| --- | --- |
| Developer profile membership | `contracts/profiles/*.profile.json` |
| Rootless runtime preference and permitted alternatives | Container-runtime toolchain contract |
| Workspace port artifact | `contracts/artifact-contracts/workspace-port-allocation.schema.json` |
| Component data ownership | Component contracts and `DEC-DATA-001` |
| Resource limits | Profile, component contracts, and Resource Governor |
| Secret and local-identity behavior | `DOC-DEV-009` and requirement registry |
| Exact tests and evidence | Test, evidence, and traceability registries |

The recipe does not create architecture authority. In particular:

- Podman is preferred for native Linux development, while application contracts remain runtime-neutral unless a profile adopts runtime-specific behavior;
- container isolation does not replace database, identity, secret, port, or volume isolation;
- a rootless runtime does not grant cross-component data access;
- labels and names help cleanup but do not replace canonical ownership records;
- successful container startup is not a conformance result.

## 4. Create and Load the Workspace Identity

Run these commands from the repository or worktree root.

The example generates the identifier once and stores it in local uncommitted state. Set `KOA_COMPONENT_ID` to the component or product identity before first use.

```bash
set -euo pipefail

WORKSPACE_ROOT="$(git rev-parse --show-toplevel)"
cd "$WORKSPACE_ROOT"

KOA_COMPONENT_ID="${KOA_COMPONENT_ID:-orgo}"
WORKSPACE_STATE_DIR="$WORKSPACE_ROOT/.koa"
WORKSPACE_ID_FILE="$WORKSPACE_STATE_DIR/workspace-id"

mkdir -p "$WORKSPACE_STATE_DIR"
chmod 700 "$WORKSPACE_STATE_DIR"

GIT_EXCLUDE="$(git rev-parse --git-path info/exclude)"
grep -qxF ".koa/" "$GIT_EXCLUDE" ||
  printf '\n.koa/\n' >> "$GIT_EXCLUDE"

if [ ! -s "$WORKSPACE_ID_FILE" ]; then
  PURPOSE="$(git branch --show-current)"
  if [ -z "$PURPOSE" ]; then
    PURPOSE="detached"
  fi

  PURPOSE="$(
    printf '%s' "$PURPOSE" |
      tr '[:upper:]' '[:lower:]' |
      sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g' |
      cut -c1-32
  )"

  UNIQUE_SUFFIX="$(
    od -An -N2 -tx1 /dev/urandom |
      tr -d ' \n'
  )"

  printf '%s-%s-%s\n' \
    "$KOA_COMPONENT_ID" \
    "$PURPOSE" \
    "$UNIQUE_SUFFIX" \
    > "$WORKSPACE_ID_FILE"

  chmod 600 "$WORKSPACE_ID_FILE"
fi

WORKSPACE_ID="$(cat "$WORKSPACE_ID_FILE")"
export WORKSPACE_ID

printf 'workspace_id=%s\n' "$WORKSPACE_ID"
```

The resulting identifier follows:

```text
component + branch_or_purpose + unique_suffix
```

Do not regenerate it during ordinary updates. A different worktree or parallel branch receives its own identifier and isolated resources.

## 5. Verify Rootless Runtime and Prepare Namespaces

Confirm that the command is running as a non-root user and that Podman can enter its rootless user namespace.

```bash
set -euo pipefail

if [ "$(id -u)" -eq 0 ]; then
  printf '%s\n' "Run this recipe as the development user, not root." >&2
  exit 1
fi

podman info >/dev/null
podman unshare true

CONTAINER_PREFIX="${WORKSPACE_ID}-svc"
NETWORK_NAME="${WORKSPACE_ID}-svc-net"
POSTGRES_CONTAINER="${CONTAINER_PREFIX}-postgres"
REDIS_CONTAINER="${CONTAINER_PREFIX}-redis"
POSTGRES_VOLUME="${WORKSPACE_ID}-postgres-data"
REDIS_VOLUME="${WORKSPACE_ID}-redis-data"

XDG_STATE_HOME="${XDG_STATE_HOME:-$HOME/.local/state}"
WORKSPACE_RUNTIME_DIR="$XDG_STATE_HOME/koa/workspaces/$WORKSPACE_ID"
SECRET_DIR="$WORKSPACE_RUNTIME_DIR/secrets"

mkdir -p "$SECRET_DIR"
chmod 700 "$WORKSPACE_RUNTIME_DIR" "$SECRET_DIR"

podman network inspect "$NETWORK_NAME" >/dev/null 2>&1 ||
  podman network create \
    --label "io.koa.workspace_id=$WORKSPACE_ID" \
    --label "io.koa.purpose=development-services" \
    "$NETWORK_NAME"

podman volume inspect "$POSTGRES_VOLUME" >/dev/null 2>&1 ||
  podman volume create \
    --label "io.koa.workspace_id=$WORKSPACE_ID" \
    --label "io.koa.component=postgres" \
    "$POSTGRES_VOLUME"

podman volume inspect "$REDIS_VOLUME" >/dev/null 2>&1 ||
  podman volume create \
    --label "io.koa.workspace_id=$WORKSPACE_ID" \
    --label "io.koa.component=redis" \
    "$REDIS_VOLUME"
```

Avoid:

- `sudo podman`;
- `--privileged`;
- `--network host`;
- mounting the runtime socket into application containers;
- reusing another workspace's network or volume;
- assigning generic names such as `postgres`, `redis`, `db`, or `cache`;
- placing service data in an unscoped shared host directory.

## 6. Resolve Ports, Secrets, and Service Identities

### 6.1 Resolve allocated host ports

This example expects:

```text
.koa/runtime/workspace-port-allocation.json
```

It contains bindings whose endpoint names are `postgres` and `redis`.

```bash
set -euo pipefail

PORT_ALLOCATION_FILE="$WORKSPACE_ROOT/.koa/runtime/workspace-port-allocation.json"

if [ ! -r "$PORT_ALLOCATION_FILE" ]; then
  printf 'Missing port allocation artifact: %s\n' \
    "$PORT_ALLOCATION_FILE" >&2
  exit 1
fi

jq -e \
  --arg workspace_id "$WORKSPACE_ID" \
  '.workspace_id == $workspace_id' \
  "$PORT_ALLOCATION_FILE" >/dev/null

POSTGRES_HOST_PORT="$(
  jq -er \
    '.bindings[] |
     select(.endpoint_name == "postgres") |
     select(.protocol == "tcp") |
     select(.exposure_scope == "loopback_only") |
     .host_port' \
    "$PORT_ALLOCATION_FILE"
)"

REDIS_HOST_PORT="$(
  jq -er \
    '.bindings[] |
     select(.endpoint_name == "redis") |
     select(.protocol == "tcp") |
     select(.exposure_scope == "loopback_only") |
     .host_port' \
    "$PORT_ALLOCATION_FILE"
)"

export POSTGRES_HOST_PORT REDIS_HOST_PORT
```

Do not scan for a different port after a collision. Treat the conflict as an allocation failure and correct the allocation artifact through its owning allocator.

### 6.2 Create a workspace-scoped database identity

```bash
PG_SCOPE="$(
  printf '%s' "$WORKSPACE_ID" |
    tr '-' '_' |
    cut -c1-40
)"

PG_DATABASE="${PG_SCOPE}_app"
PG_USER="${PG_SCOPE}_app"

export PG_DATABASE PG_USER
```

A second component in the same workspace receives a different database and identity. A second workspace receives a different scope.

### 6.3 Create the PostgreSQL secret

Generate the value outside the repository. Do not print it or place it in a general environment file.

```bash
set -euo pipefail

POSTGRES_PASSWORD_FILE="$SECRET_DIR/postgres-password"
POSTGRES_SECRET="${WORKSPACE_ID}-postgres-password"

if [ ! -s "$POSTGRES_PASSWORD_FILE" ]; then
  umask 077
  openssl rand -base64 36 > "$POSTGRES_PASSWORD_FILE"
fi

chmod 600 "$POSTGRES_PASSWORD_FILE"

if podman secret inspect "$POSTGRES_SECRET" >/dev/null 2>&1; then
  podman secret rm "$POSTGRES_SECRET"
fi

podman secret create \
  "$POSTGRES_SECRET" \
  "$POSTGRES_PASSWORD_FILE" >/dev/null
```

The secret remains workspace-scoped local state. Each container receives only its declared secret.

## 7. Start and Operate the Service Containers

Use immutable image references owned by the active toolchain or project lock. The tags below are illustrative moving tags and need replacement by project-approved references before a reproducibility or conformance claim.

```bash
POSTGRES_IMAGE="docker.io/library/postgres:16"
REDIS_IMAGE="docker.io/library/redis:7"
```

Remove only containers with exact workspace-derived names:

```bash
podman rm -f \
  "$POSTGRES_CONTAINER" \
  "$REDIS_CONTAINER" \
  >/dev/null 2>&1 || true
```

Start PostgreSQL:

```bash
podman run -d \
  --name "$POSTGRES_CONTAINER" \
  --network "$NETWORK_NAME" \
  --label "io.koa.workspace_id=$WORKSPACE_ID" \
  --label "io.koa.component=postgres" \
  --label "io.koa.lifecycle=development" \
  --pids-limit 256 \
  --memory 2g \
  --cpus 1.5 \
  --restart on-failure:3 \
  --secret "$POSTGRES_SECRET,target=postgres-password" \
  -e "POSTGRES_DB=$PG_DATABASE" \
  -e "POSTGRES_USER=$PG_USER" \
  -e "POSTGRES_PASSWORD_FILE=/run/secrets/postgres-password" \
  -v "$POSTGRES_VOLUME:/var/lib/postgresql/data" \
  -p "127.0.0.1:${POSTGRES_HOST_PORT}:5432/tcp" \
  --health-cmd "pg_isready -U $PG_USER -d $PG_DATABASE" \
  --health-interval 5s \
  --health-timeout 3s \
  --health-retries 12 \
  "$POSTGRES_IMAGE"
```

Start Redis:

```bash
podman run -d \
  --name "$REDIS_CONTAINER" \
  --network "$NETWORK_NAME" \
  --label "io.koa.workspace_id=$WORKSPACE_ID" \
  --label "io.koa.component=redis" \
  --label "io.koa.lifecycle=development" \
  --pids-limit 128 \
  --memory 512m \
  --cpus 0.5 \
  --restart on-failure:3 \
  -v "$REDIS_VOLUME:/data" \
  -p "127.0.0.1:${REDIS_HOST_PORT}:6379/tcp" \
  --health-cmd "redis-cli ping" \
  --health-interval 5s \
  --health-timeout 3s \
  --health-retries 12 \
  "$REDIS_IMAGE" \
  redis-server \
  --appendonly yes \
  --save 60 1000
```

Application processes can use either:

- allocated loopback ports from the host;
- fixed internal ports and workspace-scoped DNS names from another container on the same workspace network.

An application container can reach:

```text
orgo-feature-voting-92cd-svc-postgres:5432
orgo-feature-voting-92cd-svc-redis:6379
```

The actual prefix comes from the current workspace identity.

## 8. Verify Isolation and Readiness

### 8.1 Verify workspace ownership

```bash
podman ps \
  --filter "label=io.koa.workspace_id=$WORKSPACE_ID"
```

### 8.2 Verify health

```bash
for container in "$POSTGRES_CONTAINER" "$REDIS_CONTAINER"; do
  state="$(
    podman inspect "$container" |
      jq -er '.[0].State.Health.Status'
  )"
  printf '%s %s\n' "$container" "$state"
  test "$state" = "healthy"
done
```

### 8.3 Verify database identity

```bash
podman exec "$POSTGRES_CONTAINER" \
  psql \
  -U "$PG_USER" \
  -d "$PG_DATABASE" \
  -Atc 'select current_database(), current_user;'
```

The database and identity both need to match the workspace-derived values.

### 8.4 Verify Redis

```bash
podman exec "$REDIS_CONTAINER" redis-cli ping
```

Expected result:

```text
PONG
```

### 8.5 Verify loopback-only publication

```bash
podman port "$POSTGRES_CONTAINER"
podman port "$REDIS_CONTAINER"

ss -ltn |
  grep -E "127\.0\.0\.1:(${POSTGRES_HOST_PORT}|${REDIS_HOST_PORT})\b"
```

No binding for these services should appear on `0.0.0.0`, `::`, a LAN address, or a public interface unless an active exposure authorization permits it.

### 8.6 Verify parallel workspaces

Run the recipe in another worktree with another workspace identity, then compare:

```bash
podman ps -a
podman volume ls
podman network ls
```

Container names, volumes, networks, database identities, secrets, and host ports need to differ. Stopping or deleting one workspace must leave the other operational.

## 9. Stop, Restart, and Clean Up

Stop without deleting data:

```bash
podman stop "$POSTGRES_CONTAINER" "$REDIS_CONTAINER"
```

Restart:

```bash
podman start "$POSTGRES_CONTAINER" "$REDIS_CONTAINER"
```

Remove containers while retaining data:

```bash
podman rm -f "$POSTGRES_CONTAINER" "$REDIS_CONTAINER"
```

Full cleanup is explicit:

```bash
set -euo pipefail

podman ps -aq \
  --filter "label=io.koa.workspace_id=$WORKSPACE_ID" |
  xargs -r podman rm -f

podman secret rm "$POSTGRES_SECRET" >/dev/null 2>&1 || true
podman network rm "$NETWORK_NAME" >/dev/null 2>&1 || true

if [ "${PURGE_WORKSPACE_DATA:-0}" = "1" ]; then
  podman volume rm \
    "$POSTGRES_VOLUME" \
    "$REDIS_VOLUME"

  rm -rf "$WORKSPACE_RUNTIME_DIR"
  rm -rf "$WORKSPACE_ROOT/.koa/runtime"
  rm -f "$WORKSPACE_ID_FILE"
else
  printf '%s\n' \
    "Data retained. Set PURGE_WORKSPACE_DATA=1 for explicit deletion."
fi
```

Port reservations are released through the owning workspace allocator. Do not claim cleanup complete merely because containers stopped or the local allocation file was deleted.

Create any required backup before deleting persistent volumes.

## 10. Failure Handling and Safety Checks

| Condition | Response |
| --- | --- |
| Rootless Podman is unavailable | Stop and select another profile-approved recipe; do not switch silently to rootful execution. |
| Port artifact is absent or invalid | Keep services stopped until allocation succeeds. |
| Allocated host port is occupied | Treat it as a collision; do not substitute another port automatically. |
| Secret is missing or unreadable | Keep PostgreSQL stopped; do not borrow another workspace secret. |
| Container health remains failed | Inspect bounded logs, correct resource or service state, and recreate only the affected service. |
| Memory or process limit is reached | Queue, defer, or stop optional work; do not remove limits to hide the failure. |
| Volume ownership is incorrect | Repair through rootless namespace-aware tooling; do not run the service as a privileged host user. |
| Another workspace resource is detected | Stop cleanup and resolve the collision before deletion. |
| Host or LAN exposure appears | Stop the service and correct the allocation and bind address. |
| Secret appears in logs or history | Rotate it, remove exposed local artifacts, and record the development incident where required. |
| WSL forwarding differs from expected loopback behavior | Keep Windows-side access disabled until both scopes are validated. |

Useful bounded diagnostics:

```bash
podman logs --tail 100 "$POSTGRES_CONTAINER"
podman logs --tail 100 "$REDIS_CONTAINER"

podman stats --no-stream \
  "$POSTGRES_CONTAINER" \
  "$REDIS_CONTAINER"

podman inspect "$POSTGRES_CONTAINER" |
  jq '.[0] | {
    name: .Name,
    state: .State.Status,
    health: .State.Health.Status,
    labels: .Config.Labels,
    network: .NetworkSettings.Networks
  }'
```

Do not print secret files, unrestricted environment blocks, authentication tokens, or complete unrestricted diagnostics into issue reports.

## 11. Adaptation Checklist

Before adapting this recipe to another service, confirm:

- the service belongs in the effective developer profile;
- the component or integration contract identifies its owner and data boundary;
- image identity is pinned by the active toolchain or project lock;
- internal ports are fixed only inside the isolated workspace network;
- host ports come from the workspace allocation artifact;
- the host bind address matches the approved exposure scope;
- container, network, volume, secret, service, database, queue, socket, log, and temporary names resolve from the workspace identity;
- each component receives a distinct service and database identity;
- secret values remain outside version control and general environment files;
- persistent and temporary data use separate workspace-scoped storage;
- CPU, memory, process, input-output, queue, retry, and heavy-job limits are defined;
- health and readiness checks describe the service contract;
- cleanup can target one workspace without matching another;
- data deletion is explicit;
- backup and restore behavior is tested where required;
- rootless operation is verified;
- no privileged mode, host network, shared runtime socket, direct cross-component write, or automatic host-port substitution is introduced.

An adaptation becomes eligible for use only after its canonical references, profile scope, component boundaries, tests, and evidence have been reviewed.
