<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-RECIPE-DEV-PORT-001",
  "document_class": "non_normative_recipe",
  "status": "active",
  "language": "en",
  "layer": "recipes",
  "scope": [
    "profile:developer_linux_workstation",
    "profile:developer_windows_wsl",
    "development_port_allocation"
  ],
  "canonical_refs": [
    "generated/profile-catalog.json",
    "contracts/profiles/developer-linux-workstation.profile.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "generated/toolchain-catalog.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json#/locks/LOCK-DEV-003",
    "generated/assertion-index.json#/locks/LOCK-DEV-004",
    "generated/assertion-index.json#/locks/LOCK-IMPL-002"
  ],
  "decision_ids": [
    "DEC-PROFILE-001",
    "DEC-CONTAINER-001",
    "DEC-K8S-001",
    "DEC-DATA-001"
  ],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DATA-001",
    "LOCK-PROFILE-001",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-RECIPES-000",
    "DOC-DEV-006",
    "DOC-OPS-000",
    "DOC-SEC-001",
    "DOC-CONF-010"
  ],
  "tags": [
    "recipe",
    "development",
    "ports",
    "workspace-isolation",
    "collision-avoidance",
    "podman",
    "docker",
    "wsl",
    "cleanup",
    "non-normative"
  ]
}
KOA:DOC-META:END -->

# Development Port Allocation

> **Recipe classification:** Non-authoritative implementation guidance.
> **Risk class:** `local_persistent` because the cooperative reservation registry persists outside one process.
> **Applies to:** `developer_linux_workstation` and `developer_windows_wsl`.
> **Does not apply to:** production, sovereign, control-plane, user, or build-farm port management unless their active profile explicitly adopts an equivalent mechanism.

## 1. Purpose

This recipe allocates non-colliding host TCP ports to parallel local development workspaces.

It supports the development invariant that two branches, worktrees, or applications can run concurrently without collisions in:

- services;
- processes;
- host ports;
- databases;
- volumes;
- networks;
- secrets;
- sockets;
- logs;
- temporary state.

Container-internal ports remain stable when a service contract expects them. Host ports are local workspace allocations.

Example:

`text
Orgo container port: 8080
Workspace A host port: 24831
Workspace B host port: 27604
`

The port allocator in this recipe is cooperative. It prevents collisions among processes that use the same registry and user account. The operating-system bind performed by the service runtime remains the final authority because an unrelated process can claim a port after allocation.

### 1.1 Result

After completing the recipe, one workspace has:

- a stable `workspace_id`;
- one reservation per service-facing host port;
- a local environment file containing allocated values;
- no globally hard-coded development host port;
- a cleanup command that releases all workspace reservations.

### 1.2 Non-goals

This recipe does not:

- assign production ports;
- change a firewall;
- expose services beyond the loopback interface;
- reserve UDP ports;
- coordinate different host machines;
- coordinate different operating-system users;
- configure Kubernetes Services or ingress;
- define component interfaces;
- create network authority;
- replace runtime health and readiness;
- prove application conformance.

## 2. Applicability

### 2.1 Supported profiles

| Profile | Applicability | Runtime notes |
| --- | --- | --- |
| `developer_linux_workstation` | Supported | Rootless Podman is preferred; Docker-compatible tooling can be used when selected by the profile |
| `developer_windows_wsl` | Supported inside WSL | Docker or Podman can be used according to the active profile |
| `build_farm` | Not this recipe | The scheduler and worker profile allocate ports and networks per job |
| `user_lightweight` | Not this recipe | User installation ports belong to the active profile and installer |
| `sovereign_linux_node` | Not this recipe | Profile-owned service and Quadlet configuration controls ports |
| `sovereign_hub` | Not this recipe | Hub networking belongs to the deployment profile |
| `control_plane` | Not this recipe | Orchestrator and profile networking own allocation |

### 2.2 Supported operating environments

The allocator uses:

- Python 3.11 or later;
- Linux file locking through `fcntl`;
- Linux or WSL TCP sockets;
- a per-user state directory;
- loopback binding to `127.0.0.1`.

Native Windows execution is outside this recipe. Run it inside WSL for `developer_windows_wsl`.

### 2.3 Runtime independence

The allocation result is a host port number.

The same result can be supplied to:

- `podman run`;
- `podman compose`;
- `docker run`;
- `docker compose`;
- a local non-containerized development service.

Runtime-specific commands remain examples. The application contract does not depend on Podman, Docker, Compose, or Kubernetes behavior.

## 3. Preconditions

### 3.1 Repository and workspace

Run the recipe from a Git worktree containing the target development workspace.

Verify:

`bash
set -euo pipefail

git rev-parse --show-toplevel
git status --short
`

A dirty worktree does not prevent local port allocation, but it cannot support a clean release or conformance claim.

### 3.2 Python

Verify Python:

`bash
python3 --version
`

A project Python workspace still uses UV and its workspace-local `.venv`. The allocator itself uses only the Python standard library and can run with the host Python or through the active workspace toolchain.

### 3.3 State directory

The default registry is:

`text
${XDG_STATE_HOME:-$HOME/.local/state}/koa/dev-ports.json
`

Override it only when all cooperating workspaces use the same replacement:

`bash
export KOA_PORT_REGISTRY="$HOME/.local/state/koa/dev-ports.json"
`

Do not place the registry in the repository or commit it.

### 3.4 Port range

This recipe defaults to:

`text
20000-29999
`

Inspect the local ephemeral range:

`bash
cat /proc/sys/net/ipv4/ip_local_port_range
`

When the configured allocation range overlaps an unsuitable local or organization-reserved range, choose a permitted range before allocating:

`bash
export KOA_PORT_RANGE_START=20000
export KOA_PORT_RANGE_END=29999
`

The range must remain between ports `1024` and `65535`.

### 3.5 Loopback exposure

The examples bind to:

`text
127.0.0.1
`

This limits access to the local host. A recipe that exposes a service on another interface requires separate profile, security, and network authority.

### 3.6 Required repository exclusions

Add local runtime state to `.gitignore` when not already excluded:

`bash
mkdir -p .koa/runtime

grep -qxF '.koa/runtime/' .gitignore 2>/dev/null || \
 printf '%s\n' '.koa/runtime/' >> .gitignore
`

Changing `.gitignore` is a repository change. Review and commit it through the normal source process when it is intended to be shared.

## 4. Inputs

### 4.1 Workspace identity

The allocation key starts with a stable workspace identity.

The following command derives an identity from:

- repository name;
- current branch or detached revision;
- canonical worktree path.

`bash
set -euo pipefail

repo_root=$(git rev-parse --show-toplevel)
repo_slug=$(
 basename "$repo_root" |
 tr '[:upper:]' '[:lower:]' |
 sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g'
)

branch_raw=$(git branch --show-current)
if [ -z "$branch_raw" ]; then
 branch_raw=$(git rev-parse --short HEAD)
fi

branch_slug=$(
 printf '%s' "$branch_raw" |
 tr '[:upper:]' '[:lower:]' |
 sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g'
)

path_tag=$(printf '%s' "$repo_root" | cksum | awk '{print $1}')
workspace_prefix=$(printf 'koa-%s-%s' "$repo_slug" "$branch_slug" | cut -c1-48)

export WORKSPACE_ID="${workspace_prefix}-${path_tag}"
printf 'WORKSPACE_ID=%s\n' "$WORKSPACE_ID"
`

The resulting identity uses only lowercase letters, numbers, and hyphens and remains within 63 characters.

Moving the worktree changes `path_tag` and therefore creates a new workspace identity. Release the old workspace reservations before or after moving it.

### 4.2 Service identity

Each published host port uses one stable service-purpose identity.

Examples:

`text
orgo-http
orgo-debug
konnaxion-http
postgres
redis
test-fixture-http
`

Use separate identities for separate host ports.

Do not use only the internal port number as the service identity.

### 4.3 Internal port

When a container or local service listens on a stable internal port, record that port with the reservation.

Examples:

`text
orgo-http -> container port 8080
postgres -> container port 5432
redis -> container port 6379
`

The allocator does not validate component contracts. The recipe author resolves the internal port from the active service definition.

### 4.4 Allocation environment

The commands use:

`bash
export KOA_PORT_REGISTRY="${XDG_STATE_HOME:-$HOME/.local/state}/koa/dev-ports.json"
export KOA_PORT_RANGE_START=20000
export KOA_PORT_RANGE_END=29999
`

All cooperating workspaces for one user use the same registry and range.

## 5. Safety and Authority Boundaries

### 5.1 Cooperative reservation

The registry serializes allocations with a file lock.

It prevents two cooperating allocators from selecting the same host and port.

It does not prevent:

- an unrelated process from binding after allocation;
- another operating-system user from using the same range;
- a privileged process from ignoring the registry;
- another host from selecting the same port;
- a runtime from publishing a different interface or protocol.

Start the service soon after allocation and handle bind failure explicitly.

### 5.2 Final bind authority

A successful runtime bind is the final local port-use result.

When the bind fails:

1. stop the failed service attempt;
2. verify that no same-workspace process already owns the port;
3. replace the reservation;
4. update the environment file;
5. restart the service;
6. validate readiness.

Do not terminate an unknown process automatically.

### 5.3 Network scope

The recipe allocates loopback TCP ports only.

A container example uses:

`text
127.0.0.1:<allocated-host-port>:<container-port>
`

Do not replace `127.0.0.1` with `0.0.0.0` merely to simplify access. External exposure requires an explicit development-network decision and applicable security controls.

### 5.4 Data ownership

Port allocation grants no component or data authority.

A service that becomes reachable still requires:

- its own identity;
- authorization;
- storage identity;
- database permissions;
- secret scope;
- component contract;
- health and readiness.

The recipe cannot justify direct foreign database access.

### 5.5 Registry sensitivity

The registry contains local operational metadata:

- workspace identity;
- service identity;
- host;
- host port;
- internal port;
- allocation time.

It contains no secret values and no application payloads.

Use normal user-private file permissions when local policy requires them:

`bash
umask 077
`

### 5.6 No production transfer

The registry and generated `.koa/runtime/ports.env` are mutable development state.

They do not cross the development-to-release boundary.

Release artifacts and manifests use profile-owned networking contracts rather than copied local host-port allocations.

## 6. Procedure

### 6.1 Install the local allocator

Create the local tool:

`bash
set -euo pipefail

mkdir -p tools
cat > tools/koa-port.py <<'PY'
#!/usr/bin/env python3
"""Cooperative host-port allocator for Linux and WSL development workspaces."""

from __future__ import annotations

import argparse
import contextlib
import fcntl
import hashlib
import json
import os
import re
import socket
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")
DEFAULT_RANGE_START = 20000
DEFAULT_RANGE_END = 29999
REGISTRY_VERSION = 1


def fail(message: str, exit_code: int = 2) -> "NoReturn":
 print(f"error: {message}", file=sys.stderr)
 raise SystemExit(exit_code)


def validate_id(value: str, label: str) -> str:
 if not ID_PATTERN.fullmatch(value):
 fail(
 f"{label} must match {ID_PATTERN.pattern}; received {value!r}"
 )
 return value


def registry_path -> Path:
 configured = os.environ.get("KOA_PORT_REGISTRY")
 if configured:
 return Path(configured).expanduser

 state_home = os.environ.get("XDG_STATE_HOME")
 if state_home:
 return Path(state_home).expanduser / "koa" / "dev-ports.json"

 return Path.home / ".local" / "state" / "koa" / "dev-ports.json"


def configured_range -> tuple[int, int]:
 try:
 start = int(
 os.environ.get("KOA_PORT_RANGE_START", DEFAULT_RANGE_START)
 )
 end = int(
 os.environ.get("KOA_PORT_RANGE_END", DEFAULT_RANGE_END)
 )
 except ValueError as exc:
 fail(f"port range values must be integers: {exc}")

 if start < 1024 or end > 65535 or start > end:
 fail(
 "port range must satisfy 1024 <= start <= end <= 65535"
 )

 return start, end


def empty_registry -> dict[str, object]:
 return {
 "version": REGISTRY_VERSION,
 "reservations": [],
 }


def read_registry(path: Path) -> dict[str, object]:
 if not path.exists:
 return empty_registry

 try:
 data = json.loads(path.read_text(encoding="utf-8"))
 except (OSError, json.JSONDecodeError) as exc:
 fail(f"cannot read registry {path}: {exc}")

 if data.get("version") != REGISTRY_VERSION:
 fail(
 f"unsupported registry version in {path}: "
 f"{data.get('version')!r}"
 )

 reservations = data.get("reservations")
 if not isinstance(reservations, list):
 fail(f"registry {path} has no valid reservations list")

 return data


def write_registry(path: Path, data: dict[str, object]) -> None:
 path.parent.mkdir(parents=True, exist_ok=True)
 payload = json.dumps(data, indent=2, sort_keys=True) + "\n"

 temporary_name: str | None = None
 try:
 with tempfile.NamedTemporaryFile(
 mode="w",
 encoding="utf-8",
 dir=path.parent,
 prefix=f".{path.name}.",
 suffix=".tmp",
 delete=False,
 ) as handle:
 temporary_name = handle.name
 handle.write(payload)
 handle.flush
 os.fsync(handle.fileno)

 os.replace(temporary_name, path)
 temporary_name = None
 finally:
 if temporary_name:
 Path(temporary_name).unlink(missing_ok=True)


@contextlib.contextmanager
def locked_registry(
 path: Path,
) -> Iterator[dict[str, object]]:
 path.parent.mkdir(parents=True, exist_ok=True)
 lock_path = path.with_name(f"{path.name}.lock")

 with lock_path.open("a+", encoding="utf-8") as lock_handle:
 fcntl.flock(lock_handle.fileno, fcntl.LOCK_EX)
 data = read_registry(path)
 yield data
 write_registry(path, data)
 fcntl.flock(lock_handle.fileno, fcntl.LOCK_UN)


def port_is_free(host: str, port: int) -> bool:
 family = socket.AF_INET6 if ":" in host else socket.AF_INET
 with socket.socket(family, socket.SOCK_STREAM) as candidate:
 candidate.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
 try:
 candidate.bind((host, port))
 except OSError:
 return False
 return True


def deterministic_offset(
 workspace_id: str,
 service_id: str,
 range_size: int,
) -> int:
 material = f"{workspace_id}:{service_id}".encode("utf-8")
 digest = hashlib.blake2s(material, digest_size=4).digest
 return int.from_bytes(digest, "big") % range_size


def find_reservation(
 reservations: list[dict[str, object]],
 workspace_id: str,
 service_id: str,
 host: str,
) -> dict[str, object] | None:
 for reservation in reservations:
 if (
 reservation.get("workspace_id") == workspace_id
 and reservation.get("service_id") == service_id
 and reservation.get("host") == host
 ):
 return reservation
 return None


def allocate(args: argparse.Namespace) -> int:
 workspace_id = validate_id(args.workspace, "workspace id")
 service_id = validate_id(args.service, "service id")
 host = args.host
 start, end = configured_range
 range_size = end - start + 1
 path = registry_path

 with locked_registry(path) as data:
 reservations = data["reservations"]
 assert isinstance(reservations, list)

 existing = find_reservation(
 reservations,
 workspace_id,
 service_id,
 host,
 )

 excluded_for_this_call: set[int] = set
 if existing and not args.replace:
 print(existing["host_port"])
 return 0

 if existing:
 excluded_for_this_call.add(int(existing["host_port"]))
 reservations.remove(existing)

 reserved_ports = {
 int(item["host_port"])
 for item in reservations
 if item.get("host") == host
 }

 offset = deterministic_offset(
 workspace_id,
 service_id,
 range_size,
 )

 for attempt in range(range_size):
 port = start + ((offset + attempt) % range_size)

 if port in excluded_for_this_call:
 continue
 if port in reserved_ports:
 continue
 if not port_is_free(host, port):
 continue

 reservations.append(
 {
 "workspace_id": workspace_id,
 "service_id": service_id,
 "host": host,
 "host_port": port,
 "container_port": args.container_port,
 "allocated_at": datetime.now(
 timezone.utc
 ).isoformat,
 }
 )
 print(port)
 return 0

 fail(
 f"no free port available in configured range {start}-{end}",
 exit_code=1,
 )


def release(args: argparse.Namespace) -> int:
 workspace_id = validate_id(args.workspace, "workspace id")
 service_id = validate_id(args.service, "service id")
 path = registry_path

 with locked_registry(path) as data:
 reservations = data["reservations"]
 assert isinstance(reservations, list)

 before = len(reservations)
 reservations[:] = [
 item
 for item in reservations
 if not (
 item.get("workspace_id") == workspace_id
 and item.get("service_id") == service_id
 and item.get("host") == args.host
 )
 ]

 removed = before - len(reservations)

 print(removed)
 return 0


def release_workspace(args: argparse.Namespace) -> int:
 workspace_id = validate_id(args.workspace, "workspace id")
 path = registry_path

 with locked_registry(path) as data:
 reservations = data["reservations"]
 assert isinstance(reservations, list)

 before = len(reservations)
 reservations[:] = [
 item
 for item in reservations
 if item.get("workspace_id") != workspace_id
 ]

 removed = before - len(reservations)

 print(removed)
 return 0


def list_reservations(args: argparse.Namespace) -> int:
 path = registry_path

 with locked_registry(path) as data:
 reservations = data["reservations"]
 assert isinstance(reservations, list)
 rows = sorted(
 reservations,
 key=lambda item: (
 str(item.get("workspace_id")),
 str(item.get("service_id")),
 int(item.get("host_port", 0)),
 ),
 )

 if args.json:
 print(json.dumps(rows, indent=2, sort_keys=True))
 return 0

 print(
 "workspace_id\tservice_id\thost\thost_port\t"
 "container_port\tallocated_at"
 )
 for row in rows:
 print(
 f"{row.get('workspace_id')}\t"
 f"{row.get('service_id')}\t"
 f"{row.get('host')}\t"
 f"{row.get('host_port')}\t"
 f"{row.get('container_port')}\t"
 f"{row.get('allocated_at')}"
 )

 return 0


def probe(args: argparse.Namespace) -> int:
 free = port_is_free(args.host, args.port)
 print("free" if free else "bound")
 return 0 if free else 1


def build_parser -> argparse.ArgumentParser:
 parser = argparse.ArgumentParser(
 description=(
 "Allocate cooperative development host ports by workspace "
 "and service identity."
 )
 )
 subparsers = parser.add_subparsers(dest="command", required=True)

 allocate_parser = subparsers.add_parser("allocate")
 allocate_parser.add_argument("--workspace", required=True)
 allocate_parser.add_argument("--service", required=True)
 allocate_parser.add_argument(
 "--host",
 default="127.0.0.1",
 )
 allocate_parser.add_argument(
 "--container-port",
 type=int,
 default=None,
 )
 allocate_parser.add_argument(
 "--replace",
 action="store_true",
 help=(
 "replace an existing reservation and avoid its prior port "
 "during this allocation"
 ),
 )
 allocate_parser.set_defaults(handler=allocate)

 release_parser = subparsers.add_parser("release")
 release_parser.add_argument("--workspace", required=True)
 release_parser.add_argument("--service", required=True)
 release_parser.add_argument(
 "--host",
 default="127.0.0.1",
 )
 release_parser.set_defaults(handler=release)

 release_workspace_parser = subparsers.add_parser(
 "release-workspace"
 )
 release_workspace_parser.add_argument(
 "--workspace",
 required=True,
 )
 release_workspace_parser.set_defaults(
 handler=release_workspace
 )

 list_parser = subparsers.add_parser("list")
 list_parser.add_argument("--json", action="store_true")
 list_parser.set_defaults(handler=list_reservations)

 probe_parser = subparsers.add_parser("probe")
 probe_parser.add_argument("--port", required=True, type=int)
 probe_parser.add_argument(
 "--host",
 default="127.0.0.1",
 )
 probe_parser.set_defaults(handler=probe)

 return parser


def main -> int:
 parser = build_parser
 args = parser.parse_args
 return int(args.handler(args))


if __name__ == "__main__":
 raise SystemExit(main)
PY

chmod 0755 tools/koa-port.py
python3 -m py_compile tools/koa-port.py
`

The tool is suitable for local recipe use. Adding it permanently to the repository requires normal source review.

### 6.2 Derive the workspace identity

Run the identity commands from section 4.1, then verify:

`bash
printf '%s\n' "$WORKSPACE_ID" |
 grep -Eq '^[a-z0-9][a-z0-9-]{0,62}$'
`

### 6.3 Configure the registry and range

`bash
export KOA_PORT_REGISTRY="${XDG_STATE_HOME:-$HOME/.local/state}/koa/dev-ports.json"
export KOA_PORT_RANGE_START=20000
export KOA_PORT_RANGE_END=29999
`

### 6.4 Allocate ports

Allocate an Orgo HTTP port and a PostgreSQL port:

`bash
set -euo pipefail

ORGO_HTTP_PORT=$(
 python3 tools/koa-port.py allocate \
 --workspace "$WORKSPACE_ID" \
 --service orgo-http \
 --container-port 8080
)

POSTGRES_PORT=$(
 python3 tools/koa-port.py allocate \
 --workspace "$WORKSPACE_ID" \
 --service postgres \
 --container-port 5432
)

export ORGO_HTTP_PORT
export POSTGRES_PORT

printf 'ORGO_HTTP_PORT=%s\n' "$ORGO_HTTP_PORT"
printf 'POSTGRES_PORT=%s\n' "$POSTGRES_PORT"
`

Repeating the same allocation returns the existing reservation.

### 6.5 Persist the workspace environment

`bash
set -euo pipefail

mkdir -p .koa/runtime

cat > .koa/runtime/ports.env <<EOF
WORKSPACE_ID=$WORKSPACE_ID
ORGO_HTTP_PORT=$ORGO_HTTP_PORT
POSTGRES_PORT=$POSTGRES_PORT
EOF

chmod 0600 .koa/runtime/ports.env
`

Load it in a later shell:

`bash
set -a
. .koa/runtime/ports.env
set +a
`

### 6.6 Use a Compose-compatible service definition

The following fragment is illustrative and requires the actual component image and service contract used by the workspace:

`yaml
services:
 orgo:
 image: localhost/koa/orgo:development
 ports:
 - "127.0.0.1:${ORGO_HTTP_PORT:?allocate ORGO_HTTP_PORT first}:8080"

 postgres:
 image: docker.io/library/postgres:17
 ports:
 - "127.0.0.1:${POSTGRES_PORT:?allocate POSTGRES_PORT first}:5432"
`

The image references are examples, not approved release artifacts.

The same environment values can be supplied to Podman Compose or Docker Compose according to the active developer profile.

### 6.7 Use a direct runtime command

Podman example:

`bash
podman run --rm \
 --name "${WORKSPACE_ID}-http-demo" \
 --publish "127.0.0.1:${ORGO_HTTP_PORT}:8080" \
 docker.io/library/python:3.13-alpine \
 python -m http.server 8080 --bind 0.0.0.0
`

Docker example:

`bash
docker run --rm \
 --name "${WORKSPACE_ID}-http-demo" \
 --publish "127.0.0.1:${ORGO_HTTP_PORT}:8080" \
 docker.io/library/python:3.13-alpine \
 python -m http.server 8080 --bind 0.0.0.0
`

Use only the runtime selected by the active profile.

The external image is an example and requires normal dependency, trust, and network controls before use.

### 6.8 Replace a reservation after bind failure

First stop the failed service attempt.

Then replace the reservation:

`bash
set -euo pipefail

ORGO_HTTP_PORT=$(
 python3 tools/koa-port.py allocate \
 --workspace "$WORKSPACE_ID" \
 --service orgo-http \
 --container-port 8080 \
 --replace
)

export ORGO_HTTP_PORT

python3 - <<'PY'
from pathlib import Path
import os

path = Path(".koa/runtime/ports.env")
lines = path.read_text(encoding="utf-8").splitlines
values = {}

for line in lines:
 key, value = line.split("=", 1)
 values[key] = value

values["ORGO_HTTP_PORT"] = os.environ["ORGO_HTTP_PORT"]

path.write_text(
 "\n".join(f"{key}={value}" for key, value in values.items) + "\n",
 encoding="utf-8",
)
PY
`

A replacement deliberately avoids the prior reservation for that allocation.

### 6.9 Inspect reservations

Human-readable output:

`bash
python3 tools/koa-port.py list
`

JSON output:

`bash
python3 tools/koa-port.py list --json
`

### 6.10 Probe one port

Before starting a service:

`bash
python3 tools/koa-port.py probe --port "$ORGO_HTTP_PORT"
`

Expected output before bind:

`text
free
`

After a service binds the port, the command returns `bound` and exits non-zero.

That result alone does not prove the expected service owns the port.

## 7. Validation

### 7.1 Validate deterministic reuse

`bash
set -euo pipefail

first=$(
 python3 tools/koa-port.py allocate \
 --workspace "$WORKSPACE_ID" \
 --service orgo-http \
 --container-port 8080
)

second=$(
 python3 tools/koa-port.py allocate \
 --workspace "$WORKSPACE_ID" \
 --service orgo-http \
 --container-port 8080
)

test "$first" = "$second"
printf 'deterministic reuse: pass (%s)\n' "$first"
`

### 7.2 Validate two-workspace separation

This test uses disposable identities and a disposable registry:

`bash
set -euo pipefail

temporary_registry=$(mktemp)
rm -f "$temporary_registry"

cleanup_port_test {
 rm -f "$temporary_registry" "$temporary_registry.lock"
}
trap cleanup_port_test EXIT

export KOA_PORT_REGISTRY="$temporary_registry"
export KOA_PORT_RANGE_START=25000
export KOA_PORT_RANGE_END=25020

port_a=$(
 python3 tools/koa-port.py allocate \
 --workspace koa-port-demo-a \
 --service orgo-http \
 --container-port 8080
)

port_b=$(
 python3 tools/koa-port.py allocate \
 --workspace koa-port-demo-b \
 --service orgo-http \
 --container-port 8080
)

test "$port_a" != "$port_b"
printf 'workspace separation: pass (%s, %s)\n' "$port_a" "$port_b"
`

### 7.3 Validate actual simultaneous binds

`bash
set -euo pipefail

temporary_registry=$(mktemp)
rm -f "$temporary_registry"

cleanup_servers {
 if [ -n "${server_a_pid:-}" ]; then
 kill "$server_a_pid" 2>/dev/null || true
 wait "$server_a_pid" 2>/dev/null || true
 fi
 if [ -n "${server_b_pid:-}" ]; then
 kill "$server_b_pid" 2>/dev/null || true
 wait "$server_b_pid" 2>/dev/null || true
 fi
 rm -f "$temporary_registry" "$temporary_registry.lock"
}
trap cleanup_servers EXIT

port_a=$(
 KOA_PORT_REGISTRY="$temporary_registry" \
 KOA_PORT_RANGE_START=25100 \
 KOA_PORT_RANGE_END=25120 \
 python3 tools/koa-port.py allocate \
 --workspace koa-port-bind-a \
 --service http \
 --container-port 8000
)

port_b=$(
 KOA_PORT_REGISTRY="$temporary_registry" \
 KOA_PORT_RANGE_START=25100 \
 KOA_PORT_RANGE_END=25120 \
 python3 tools/koa-port.py allocate \
 --workspace koa-port-bind-b \
 --service http \
 --container-port 8000
)

python3 -m http.server "$port_a" \
 --bind 127.0.0.1 \
 --directory . \
 > .koa/runtime/http-a.log 2>&1 &
server_a_pid=$!

python3 -m http.server "$port_b" \
 --bind 127.0.0.1 \
 --directory . \
 > .koa/runtime/http-b.log 2>&1 &
server_b_pid=$!

sleep 1

curl --fail --silent --show-error \
 "http://127.0.0.1:${port_a}/" >/dev/null

curl --fail --silent --show-error \
 "http://127.0.0.1:${port_b}/" >/dev/null

printf 'simultaneous binds: pass (%s, %s)\n' "$port_a" "$port_b"
`

This validation proves local port separation for the two disposable workspaces. It does not validate Orgo, Konnaxion, PostgreSQL, or another component contract.

### 7.4 Validate no global fixed port in Compose inputs

For an expected Compose file named `compose.yaml`:

`bash
grep -nE '127\.0\.0\.1:[0-9]+:' compose.yaml && {
 printf '%s\n' 'unexpected fixed loopback host port found' >&2
 exit 1
} || true
`

Review matches manually. Some intentionally isolated fixtures can use fixed ports when their recipe proves collision handling.

### 7.5 Validate registry contents

`bash
python3 tools/koa-port.py list --json |
 python3 -m json.tool
`

Check that:

- each workspace and service pair is unique;
- no two active reservations use the same host port;
- service identifiers describe purpose;
- no secret value is present;
- retired workspaces have no reservation.

### 7.6 Validate service readiness separately

After starting the real service, use its component-defined readiness check.

Examples include:

`bash
curl --fail --silent --show-error \
 "http://127.0.0.1:${ORGO_HTTP_PORT}/ready"
`

A successful TCP bind is not component readiness.

Use the actual registered readiness path and expected response for the component.

### 7.7 Validation result classification

Record one actual result:

`text
pass
fail
blocked
unavailable
incomplete
not applicable
`

Do not report `pass` when:

- Python is missing;
- the configured range is exhausted;
- the runtime bind fails;
- a test is skipped;
- the service readiness check is unavailable;
- cleanup remains incomplete.

## 8. Cleanup

### 8.1 Stop services first

Stop every process or container that uses the workspace ports.

Podman example:

`bash
podman rm --force "${WORKSPACE_ID}-http-demo" 2>/dev/null || true
`

Docker example:

`bash
docker rm --force "${WORKSPACE_ID}-http-demo" 2>/dev/null || true
`

Use only the selected runtime and exact workspace-scoped names.

### 8.2 Release one reservation

`bash
python3 tools/koa-port.py release \
 --workspace "$WORKSPACE_ID" \
 --service orgo-http
`

The output is the number of removed reservations.

Repeating the command is safe and returns `0`.

### 8.3 Release the complete workspace

After every workspace service is stopped:

`bash
python3 tools/koa-port.py release-workspace \
 --workspace "$WORKSPACE_ID"
`

### 8.4 Remove generated local state

`bash
rm -f .koa/runtime/ports.env
rm -f .koa/runtime/http-a.log
rm -f .koa/runtime/http-b.log
`

Remove `tools/koa-port.py` only when it was created as disposable recipe state and is not a reviewed repository tool:

`bash
rm -f tools/koa-port.py
`

### 8.5 Verify cleanup

`bash
python3 tools/koa-port.py list --json |
 python3 -c '
import json
import os
import sys

workspace = os.environ["WORKSPACE_ID"]
rows = json.load(sys.stdin)
remaining = [
 row for row in rows
 if row.get("workspace_id") == workspace
]

if remaining:
 print(json.dumps(remaining, indent=2), file=sys.stderr)
 raise SystemExit(1)
'
`

Also verify that no workspace service still listens on the released ports.

Do not delete or terminate an unrelated process solely because it uses a prior port number.

## 9. Rollback or Safe Exit

### 9.1 Before service start

Before a service starts, rollback consists of releasing the reservation and removing the local environment file.

No application state should exist.

### 9.2 After service start

After a service starts:

1. stop the exact workspace-scoped service;
2. verify its cleanup contract;
3. release the reservation;
4. remove generated environment state;
5. retain logs only when the workspace policy requires them.

Port release does not delete databases, volumes, queues, or component data.

Clean those resources through their owning recipe and contract.

### 9.3 After changing a port

When a replacement port causes a problem:

1. stop the service;
2. release the new reservation;
3. allocate again or restore the prior reservation only when it is free;
4. update `.koa/runtime/ports.env`;
5. restart;
6. validate readiness.

A host port has no release identity and does not need to remain stable across disposable workspace recreation.

### 9.4 Safe exit on uncertainty

When the owner of a bound port is uncertain:

- do not kill the process;
- do not delete another workspace reservation;
- stop the current recipe;
- inspect local processes and container runtime state;
- select a replacement reservation;
- document unresolved local state before reuse.

## 10. Failure Handling

### 10.1 Range exhaustion

Symptom:

`text
error: no free port available in configured range
`

Response:

1. inspect the registry;
2. release retired workspaces;
3. inspect bound ports;
4. enlarge or move the configured range within local policy;
5. retry allocation.

Do not silently use a privileged or externally exposed port.

### 10.2 Existing reservation but bind fails

Possible causes:

- a non-cooperating process claimed the port;
- another user claimed the port;
- the service from a prior run still exists;
- the environment file is stale;
- a container runtime retained the bind.

Response:

`bash
python3 tools/koa-port.py allocate \
 --workspace "$WORKSPACE_ID" \
 --service orgo-http \
 --container-port 8080 \
 --replace
`

Then update the environment file and restart.

### 10.3 Corrupt registry

The allocator stops rather than replacing an unreadable registry automatically.

Response:

1. stop all cooperating workspace services or inventory their active ports;
2. preserve the corrupt registry for diagnostics;
3. move it aside;
4. reconstruct reservations from active workspace state;
5. validate each bind;
6. resume allocation.

Do not discard the registry while active workspaces depend on it without reconciliation.

### 10.4 Lock file remains

The `.lock` file can remain after normal execution. File existence does not mean the lock is held.

Do not delete it routinely.

The operating system releases the lock when the process exits.

### 10.5 Permission denied

Verify ownership and permissions of:

`text
${XDG_STATE_HOME:-$HOME/.local/state}/koa/
`

The registry should be writable by the current development user and should not require root.

Do not run the allocator with `sudo` to bypass a user-state permission problem.

### 10.6 Port appears free but runtime cannot bind

Possible causes include:

- IPv4 and IPv6 wildcard behavior;
- a runtime publishing another interface;
- a race after allocation;
- a platform-specific proxy;
- a security policy;
- a duplicate runtime declaration.

Keep loopback binding explicit, inspect the runtime error, replace the reservation when appropriate, and validate the final runtime bind.

### 10.7 WSL and host forwarding

WSL, Docker Desktop, or another host integration can add forwarding or proxy behavior beyond the Linux bind visible inside WSL.

This recipe validates the WSL-side port.

When host-side accessibility matters, validate it separately from the Windows host without weakening loopback and profile restrictions.

### 10.8 Failed cleanup

A failed cleanup leaves the workspace operational state open.

Record:

- workspace identity;
- retained reservation;
- bound port;
- process or container;
- reason;
- next safe action.

Do not reuse the workspace identity for a clean conformance or release claim until residual state is reconciled.

## 11. References

### 11.1 Canonical references

`text
generated/profile-catalog.json
contracts/profiles/developer-linux-workstation.profile.json
contracts/profiles/developer-windows-wsl.profile.json
generated/assertion-index.json#/locks/LOCK-DEV-003
generated/assertion-index.json#/locks/LOCK-DEV-004
generated/assertion-index.json#/locks/LOCK-IMPL-002
`

### 11.2 Related documents

`text
11-recipes/README.md
05-development/01-workspace-isolation.md
05-development/05-ports-volumes-secrets-and-data.md
05-development/06-service-containers.md
05-development/06-parallel-workspaces.md
07-security/01-security-baseline.md
08-operations/00-operating-model.md
09-conformance/10-canonical-ownership-validation.md
`

The exact numbering of related development documents follows the active repository file list. The canonical references and active document metadata take precedence over historical numbering.

### 11.3 Decisions and locks

`text
DEC-PROFILE-001
DEC-CONTAINER-001
DEC-K8S-001
DEC-DATA-001

LOCK-DEV-003
LOCK-DEV-004
LOCK-DATA-001
LOCK-PROFILE-001
LOCK-IMPL-001
LOCK-IMPL-002
`

### 11.4 Recipe validation status

The documentation artifact and embedded allocator source have been syntax- and behavior-checked during generation.

This recipe does not claim that:

- Podman or Docker is installed;
- the example images are approved or available;
- a real component readiness test has executed;
- profile conformance has executed;
- release or production networking has been validated.
