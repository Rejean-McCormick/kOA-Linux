<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-REC-DEV-002",
  "document_class": "recipe",
  "status": "active",
  "language": "en",
  "layer": "implementation_recipe",
  "scope": [
    "profile:developer_linux_workstation",
    "profile:developer_windows_wsl",
    "toolchain:python_uv"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/development_isolation",
    "schemas/developer-workspace.schema.json",
    "contracts/profiles/developer-linux-workstation.profile.json#/capabilities/workspace_isolation",
    "contracts/profiles/developer-windows-wsl.profile.json#/capabilities/workspace_isolation",
    "contracts/toolchains/python-uv.toolchain.json",
    "generated/component-catalog.json",
    "contracts/artifact-classes.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "05-development/02-workspace-identity.md",
    "05-development/03-workspace-isolation.md",
    "05-development/04-dependency-isolation.md",
    "05-development/05-python-uv.md",
    "05-development/08-volumes-and-persistent-data.md",
    "05-development/09-secrets-and-local-identities.md",
    "05-development/10-parallel-applications-and-branches.md",
    "05-development/11-local-databases-and-migrations.md",
    "05-development/14-build-test-and-validation.md",
    "08-operations/02-health-and-readiness.md",
    "10-adrs/ADR-015-development-workspace-isolation-with-uv.md"
  ],
  "decision_ids": [
    "DEC-DEV-001",
    "DEC-DEV-002",
    "DEC-DATA-001",
    "DEC-PROFILE-BASELINE-001"
  ],
  "requirement_ids": [
    "REQ-DEV-UV-001",
    "REQ-DEV-UV-002",
    "REQ-DEV-UV-003",
    "REQ-DEV-UV-004",
    "REQ-DEV-UV-005",
    "REQ-DEV-UV-006",
    "REQ-DEV-UV-007",
    "REQ-DEV-UV-008",
    "REQ-DEV-UV-009",
    "REQ-DEV-UV-010",
    "REQ-DEV-UV-011",
    "REQ-DEV-UV-012",
    "REQ-DEV-UV-013",
    "REQ-DEV-UV-014",
    "REQ-DEV-UV-015",
    "REQ-DEV-VOL-001",
    "REQ-DEV-VOL-002",
    "REQ-DEV-VOL-003",
    "REQ-DEV-VOL-004",
    "REQ-DEV-VOL-005",
    "REQ-DEV-VOL-007",
    "REQ-DEV-VOL-008",
    "REQ-DEV-VOL-009",
    "REQ-DEV-VOL-010",
    "REQ-DEV-VOL-011",
    "REQ-DEV-VOL-012",
    "REQ-DEV-VOL-013",
    "REQ-DEV-VOL-014",
    "REQ-DEV-VOL-018",
    "REQ-DEV-VOL-020",
    "REQ-DEV-VOL-021",
    "REQ-DEV-VOL-022"
  ],
  "lock_ids": [
    "LOCK-DEV-001",
    "LOCK-DEV-002",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DEV-005",
    "LOCK-DATA-001",
    "LOCK-COMP-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-DEV-008",
    "DOC-PRO-000",
    "DOC-SEC-003",
    "DOC-OPS-002",
    "DOC-ADR-015"
  ],
  "tags": [
    "recipe",
    "development",
    "git-worktree",
    "parallel-workspaces",
    "workspace-isolation",
    "uv",
    "python",
    "ports",
    "containers",
    "databases",
    "secrets",
    "cleanup",
    "non-normative"
  ]
}
KOA:DOC-META:END -->

# Parallel Git Worktrees

> **Recipe status:** Active, non-normative implementation guidance.
> **Authority rule:** This recipe implements one supported workspace-isolation method. Canonical decisions, profiles, toolchain contracts, requirements, locks, component contracts, and schemas remain authoritative.

## Recipe Identity

| Field | Value |
| --- | --- |
| Recipe ID | `RECIPE-DEV-002` |
| Title | Parallel Git Worktrees |
| Status | `active` |
| Version | `1.0.0` |
| Owner | `development-architecture` |
| Last reviewed | `2026-08-03` |
| Applies to profiles | `developer_linux_workstation`, `developer_windows_wsl` |
| Applies to components | Any component repository using the `python_uv` toolchain |
| Applies to toolchains | `python_uv` |
| Supported platforms | Native Linux and Linux filesystems inside WSL2 |
| Supersedes | None |
| Replaced by | None |

## 1. Purpose

This recipe creates several Git worktrees from one repository and gives each worktree an isolated development workspace.

Successful completion produces, for every worktree:

- one stable `workspace_id`;
- one branch checkout;
- one workspace-local `.venv`;
- one frozen UV synchronization result;
- one distinct block of host ports;
- one distinct Compose project name;
- one distinct database name and database identity;
- one workspace-local runtime, log, temporary, data, artifact, backup, and restore directory;
- one workspace-local secret directory;
- one machine-readable workspace manifest;
- no shared mutable application or service state.

The only shared mutable location used by this recipe is a content-addressed UV download cache. That cache is non-authoritative and can be deleted without changing dependency authority or another workspace's installed environment.

This recipe prepares identifiers and directories for service, database, secret, and container recipes. It does not define the repository's service topology, component data model, database migrations, publication flow, release process, or production deployment.

## 2. Non-Normative Status

This recipe does not create a global development requirement or redefine a profile.

When this recipe conflicts with an active canonical source, the canonical source wins and this recipe is corrected.

The recipe does not:

- change the selected Python or UV toolchain;
- update `uv.lock`;
- invent package sources;
- make a shared `.venv` acceptable;
- make a shared database directory acceptable;
- assign component data ownership;
- create a new profile;
- grant host privilege;
- establish release conformance;
- resolve a missing architectural decision.

The commands are an implementation method for the active workspace-isolation architecture.

## 3. Scope

### 3.1 Included

The recipe covers:

- creating or reusing a Git linked worktree;
- generating and recording a stable workspace identity;
- allocating a distinct host-port block;
- generating distinct service, database, and Compose names;
- creating workspace-local mutable directories;
- generating a workspace-local development secret;
- synchronizing a workspace-local `.venv` with UV;
- validating simultaneous worktree isolation;
- optionally starting repository-defined rootless Compose services;
- removing one worktree without changing another worktree or the shared UV cache.

### 3.2 Excluded

The recipe does not cover:

- production worktrees;
- bare-repository server administration;
- Windows-native Python outside WSL2;
- a shared `.venv`;
- a shared mutable PostgreSQL data directory;
- cross-worktree database cloning from a live service;
- production credentials;
- release signing;
- artifact publication;
- irreversible data migration without the database-migration recipe;
- assignment of fixed profile-wide port values;
- direct writes to another component's authoritative state.

### 3.3 Supported profiles

Supported:

- `developer_linux_workstation`
- `developer_windows_wsl`

The recipe can be used inside a disposable build worker for investigation, but build-farm jobs use the build-farm contract rather than this persistent developer workflow.

Unsupported:

- production and sovereign runtime profiles that do not include developer workspace tooling;
- Windows-native checkouts outside WSL2;
- filesystems that cannot preserve Linux permissions for `.koa/secrets`.

### 3.4 Supported tools

| Tool | Required behavior | Canonical source |
| --- | --- | --- |
| Git | Linked worktrees and branch validation | Repository development contract |
| UV | Frozen lock verification, workspace-local `.venv`, command execution | `contracts/toolchains/python-uv.toolchain.json` |
| Python 3 | Workspace manifest generation and isolation validation | `contracts/toolchains/python-uv.toolchain.json` |
| OpenSSL | Local development-secret generation | Profile secret implementation |
| Rootless Docker Compose | Optional repository-defined services | Rootless service-container recipe and selected profile |
| Bash | Recipe helper scripts | Supported Linux and WSL2 environment |

This recipe does not pin tool versions independently. The active profile and toolchain contract own supported versions.

## 4. Canonical References

### 4.1 Decisions

- `DEC-DEV-001`
- `DEC-DEV-002`
- `DEC-DATA-001`
- `DEC-PROFILE-BASELINE-001`

### 4.2 Requirements

The applicable requirement identities are listed in the generated document metadata. The most directly exercised families are:

- `REQ-DEV-UV-001` through `REQ-DEV-UV-015`;
- workspace storage and cleanup requirements under `REQ-DEV-VOL-*`;
- `REQ-DEV-VOL-018` for collision-free parallel branches and worktrees.

The requirements registry owns the exact statements.

### 4.3 Locks

- `LOCK-DEV-001`
- `LOCK-DEV-002`
- `LOCK-DEV-003`
- `LOCK-DEV-004`
- `LOCK-DEV-005`
- `LOCK-DATA-001`
- `LOCK-COMP-001`
- `LOCK-PROFILE-001`
- `LOCK-PROFILE-002`

### 4.4 Profiles

- `contracts/profiles/developer-linux-workstation.profile.json#/capabilities/workspace_isolation`
- `contracts/profiles/developer-windows-wsl.profile.json#/capabilities/workspace_isolation`

### 4.5 Toolchain

- `contracts/toolchains/python-uv.toolchain.json`

### 4.6 Related documentation

- `05-development/02-workspace-identity.md`
- `05-development/03-workspace-isolation.md`
- `05-development/04-dependency-isolation.md`
- `05-development/05-python-uv.md`
- `05-development/08-volumes-and-persistent-data.md`
- `05-development/09-secrets-and-local-identities.md`
- `05-development/10-parallel-applications-and-branches.md`
- `05-development/11-local-databases-and-migrations.md`
- `05-development/14-build-test-and-validation.md`
- `08-operations/02-health-and-readiness.md`
- `10-adrs/ADR-015-development-workspace-isolation-with-uv.md`

## 5. Preconditions

### 5.1 Authority preconditions

Before execution:

- the selected developer profile is active;
- the Python UV toolchain contract is active;
- `DEC-DEV-001` and `DEC-DEV-002` are accepted;
- applicable development and data locks pass;
- no active exception changes workspace isolation;
- the repository's canonical ignore policy excludes `.venv/` and `.koa/`.

### 5.2 Repository preconditions

The primary worktree contains:

`text
pyproject.toml
uv.lock
.python-version
`

The requested branch name passes `git check-ref-format --branch`.

The primary checkout and planned worktree parent are on a Linux filesystem. Under WSL2, place active source and worktrees inside the WSL filesystem rather than under `/mnt/c` when file-watching, permissions, sockets, or database performance matter.

The source checkout has no operation in progress that would make branch creation unsafe.

### 5.3 Host preconditions

Required commands:

`bash
git
uv
python3
sha256sum
realpath
openssl
bash
`

Optional service startup uses rootless Docker Compose.

No root privilege is required.

### 5.4 Verification commands

Run from an existing checkout:

`bash
set -euo pipefail

git rev-parse --show-toplevel
git worktree list --porcelain
git status --short
git check-ref-format --branch feature/parallel-worktree-check
git check-ignore -q --no-index .venv/
git check-ignore -q --no-index .koa/

command -v uv
command -v python3
command -v sha256sum
command -v realpath
command -v openssl

uv lock --check
`

All commands are non-mutating except for ordinary command-access metadata maintained by the operating system.

## 6. Inputs and Outputs

### 6.1 Inputs

| Input | Type | Source | Required | Sensitive |
| --- | --- | --- | ---: | ---: |
| Branch name | Git branch reference | Developer selection | Yes | No |
| Start reference | Commit-ish | Existing local Git object | No; defaults to `HEAD` | No |
| Primary checkout | Path | Git worktree registry | Yes | No |
| Worktree parent | Path | `KOA_WORKTREES_ROOT` or deterministic sibling path | No | No |
| UV cache path | Path | `UV_CACHE_DIR` or XDG cache default | No | No |
| Offline synchronization flag | Boolean | `KOA_UV_OFFLINE=1` | No | No |

### 6.2 Outputs

| Output | Type | Destination | Owner |
| --- | --- | --- | --- |
| Linked worktree | Git checkout | Sibling worktree directory | Workspace |
| Workspace identity | Text | `.koa/workspace-id` | Workspace controller state |
| Workspace environment | Shell environment file | `.koa/workspace.env` | Workspace |
| Compose environment | Environment file | `.koa/compose.env` | Workspace |
| Workspace manifest | JSON | `.koa/workspace.json` | Workspace |
| Python environment | Directory | `.venv/` | Python UV toolchain for that workspace |
| Local secret | Protected file | `.koa/secrets/db-password` | Workspace secret boundary |
| Mutable directories | Directories | `.koa/run`, `.koa/logs`, `.koa/tmp`, `.koa/data`, `.koa/artifacts`, `.koa/backups`, `.koa/restore` | Workspace and declared component owners |
| Shared UV cache | Content-addressed cache | XDG cache path or `UV_CACHE_DIR` | Toolchain cache, non-authoritative |

### 6.3 Mutable state

The recipe creates or changes:

- Git worktree registration;
- one branch when the branch does not already exist;
- the target checkout;
- `.koa/` workspace state;
- `.venv/`;
- one local secret;
- UV download-cache entries;
- optional rootless Compose containers, networks, and volumes when the repository defines them.

It does not create a shared mutable application database or installed Python environment.

## 7. Safety and Security Boundaries

### 7.1 Privilege model

Run as the ordinary development user.

Rootless container services remain under that user's container runtime.

Do not prefix recipe commands with `sudo`.

Host-wide service installation, firewall changes, or privileged port binding belong to a separate profile-approved procedure.

### 7.2 Secret handling

The recipe creates one random local development database secret at:

`text
.koa/secrets/db-password
`

The directory uses mode `0700`; the secret file uses mode `0600`.

The secret is never printed, committed, copied into `.koa/workspace.json`, placed in Compose command arguments, or stored in the shared UV cache.

Services receive the path through `KOA_DB_PASSWORD_FILE`.

Production or shared environment credentials are outside this recipe.

### 7.3 Network boundaries

The recipe allocates eight loopback-oriented host ports per workspace:

| Offset | Purpose |
| ---: | --- |
| `+0` | Application |
| `+1` | API |
| `+2` | Database |
| `+3` | Queue |
| `+4` | Search |
| `+5` | Metrics |
| `+6` | Debug |
| `+7` | Test service |

The repository's service contract decides which ports are used.

Port allocation does not grant network exposure. Bind development listeners to loopback unless the selected profile and service contract explicitly require another interface.

The creation script tests candidate TCP ports before recording a block. Service startup remains responsible for failing visibly if another process wins a later race.

### 7.4 Data authority

Every component and workspace retains separate authoritative data.

A shared PostgreSQL process can host several workspace and component databases only when database names, database identities, schemas or databases, permissions, migrations, backups, and restore mappings remain separate.

The recipe does not copy a live database directory.

Cross-component changes use component contracts rather than direct SQL writes.

### 7.5 External integrations

This recipe has no required external AI, publication, voice, search, or synchronization integration.

UV can contact only the package sources declared by the active toolchain when the shared cache lacks required artifacts.

Set `KOA_UV_OFFLINE=1` to prohibit UV network access during workspace synchronization.

## 8. Resource Envelope

Exact values belong to the developer profile and resource-envelope implementation.

This recipe creates one independently attributable resource namespace per worktree:

| Resource | Expected behavior | Maximum behavior | Enforcement |
| --- | --- | --- | --- |
| CPU | Shared fairly among active development workspaces | Profile-defined | Resource Governor, container runtime, or host scheduler |
| Memory | Accounted per workspace service group | Profile-defined | Resource envelope and rootless service limits |
| Storage | Separate `.venv`, mutable state, logs, and data | Workspace quota | Filesystem and resource envelope |
| I/O | Separate application and database state | Workspace limits | Resource envelope and storage configuration |
| Processes | Separate service and test process group | Workspace limit | Supervisor, cgroup, or container runtime |
| Concurrent jobs | Bounded per workspace | Profile-defined | Test runner and Resource Governor |
| Ports | Eight-port block | One recorded block per workspace | Workspace manifest and collision validation |

Stopping or removing one workspace does not reclaim or delete another workspace's resources.

## 9. Naming and Isolation

### 9.1 Workspace identity

The helper derives an initial identity from:

`text
repository slug
branch slug
hash of primary and target paths
`

It records the result in `.koa/workspace-id`.

After recording, the file is the local identity source for that worktree. Moving a worktree requires preserving or explicitly migrating that identity rather than deriving a second identity silently.

### 9.2 Worktree path

The default parent is a sibling directory:

`text
<repository-parent>/<repository-slug>-worktrees
`

The target is:

`text
<worktrees-root>/<branch-slug>
`

The helper rejects whitespace in the target path to keep shell, Compose, database, and service tooling predictable.

Set `KOA_WORKTREES_ROOT` before creation to select a different declared parent.

### 9.3 Workspace-scoped names

The generated manifest contains distinct values for:

- `workspace_id`;
- Compose project name;
- port block;
- database name;
- database user;
- runtime directory;
- logs;
- temporary data;
- application data;
- artifacts;
- backup staging;
- restore staging;
- secrets;
- Python environment.

Container and volume names inherit the Compose project name when the repository uses Compose.

### 9.4 Shared resource

Only this resource is shared by default:

`text
UV_CACHE_DIR
`

It is a non-authoritative content-addressed download cache.

The following remain workspace-local:

`text
.venv
service volumes
database state
database identity
queues
logs
temporary files
runtime sockets
PID files
secrets
generated local certificates
build outputs
test artifacts
`

### 9.5 Collision behavior

The helper:

- reuses an existing target only when it is a Git worktree on the requested branch;
- rejects a target that is an unrelated directory;
- rejects a duplicate workspace identity;
- preserves an existing recorded port block;
- selects another free candidate block for a new workspace;
- rejects unsupported identity characters;
- rejects an absent canonical ignore rule;
- never overwrites another workspace's manifest, secret, database, or `.venv`.

## 10. Procedure

### Step 1 — Install the worktree creation helper

**Objective**

Install one user-local, non-privileged helper that creates and configures a worktree.

**Command**

`bash
install -d -m 0755 "$HOME/.local/bin"

cat >"$HOME/.local/bin/koa-worktree-create" <<'KOA_WORKTREE_CREATE'
#!/usr/bin/env bash
set -Eeuo pipefail

die {
 printf 'error: %s\n' "$*" >&2
 exit 1
}

note {
 printf '%s\n' "$*"
}

slug {
 printf '%s' "$1" |
 tr '[:upper:]' '[:lower:]' |
 sed -E 's#[^a-z0-9]+#-#g; s#^-+##; s#-+$##; s#-+#-#g'
}

quote {
 printf '%q' "$1"
}

require_command {
 command -v "$1" >/dev/null 2>&1 ||
 die "required command not found: $1"
}

port_block_free {
 python3 - "$1" <<'PY'
import socket
import sys

base = int(sys.argv[1])
ports = [base + offset for offset in range(8)]
sockets = []

try:
 for port in ports:
 sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
 sock.bind(("127.0.0.1", port))
 sockets.append(sock)
except OSError:
 raise SystemExit(1)
finally:
 for sock in sockets:
 sock.close
PY
}

existing_port_base {
 local worktrees_root=$1
 local candidate=$2
 python3 - "$worktrees_root" "$candidate" <<'PY'
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
candidate = int(sys.argv[2])

for path in root.glob("*/.koa/workspace.json"):
 try:
 data = json.loads(path.read_text(encoding="utf-8"))
 except (OSError, json.JSONDecodeError):
 continue
 if data.get("port_base") == candidate:
 raise SystemExit(0)

raise SystemExit(1)
PY
}

write_export {
 local file=$1
 local name=$2
 local value=$3
 printf 'export %s=%s\n' "$name" "$(quote "$value")" >>"$file"
}

require_command git
require_command uv
require_command python3
require_command sha256sum
require_command sed
require_command find
require_command realpath
require_command openssl

branch=${1:-}
start_ref=${2:-HEAD}

test -n "$branch" ||
 die "usage: koa-worktree-create BRANCH [START_REF]"

git check-ref-format --branch "$branch" >/dev/null 2>&1 ||
 die "invalid branch name: $branch"

current_root=$(git rev-parse --show-toplevel 2>/dev/null) ||
 die "run this command from an existing checkout"

primary_root=$(
 git -C "$current_root" worktree list --porcelain |
 sed -n 's/^worktree //p' |
 sed -n '1p'
)
test -n "$primary_root" ||
 die "could not identify the primary worktree"

for required_file in pyproject.toml uv.lock .python-version; do
 test -f "$primary_root/$required_file" ||
 die "required project file is missing: $required_file"
done

for ignored_path in .venv/ .koa/; do
 git -C "$primary_root" check-ignore -q --no-index "$ignored_path" ||
 die "$ignored_path is not ignored; update the canonical ignore policy first"
done

repo_slug=$(slug "$(basename "$primary_root")" | cut -c1-16)
branch_slug=$(slug "$branch" | cut -c1-28)

test -n "$repo_slug" || die "repository name produced an empty slug"
test -n "$branch_slug" || die "branch name produced an empty slug"

default_worktrees_root="$(dirname "$primary_root")/${repo_slug}-worktrees"
worktrees_root=${KOA_WORKTREES_ROOT:-$default_worktrees_root}
target="$worktrees_root/$branch_slug"

case "$target" in
 *[[:space:]]*)
 die "the worktree target path contains whitespace: $target"
 ;;
esac

mkdir -p "$worktrees_root"

if test -e "$target"; then
 git -C "$target" rev-parse --is-inside-work-tree >/dev/null 2>&1 ||
 die "target exists but is not a Git worktree: $target"

 actual_branch=$(git -C "$target" branch --show-current)
 test "$actual_branch" = "$branch" ||
 die "target belongs to branch '$actual_branch', not '$branch'"

 note "reusing existing worktree: $target"
else
 if git -C "$primary_root" show-ref --verify --quiet "refs/heads/$branch"; then
 git -C "$primary_root" worktree add "$target" "$branch"
 else
 git -C "$primary_root" rev-parse --verify "${start_ref}^{commit}" >/dev/null
 git -C "$primary_root" worktree add -b "$branch" "$target" "$start_ref"
 fi
fi

mkdir -p \
 "$target/.koa/run" \
 "$target/.koa/logs" \
 "$target/.koa/tmp" \
 "$target/.koa/secrets" \
 "$target/.koa/data" \
 "$target/.koa/artifacts" \
 "$target/.koa/backups" \
 "$target/.koa/restore"

chmod 700 "$target/.koa" "$target/.koa/secrets"

workspace_id_file="$target/.koa/workspace-id"
if test -f "$workspace_id_file"; then
 workspace_id=$(cat "$workspace_id_file")
else
 path_hash=$(
 printf '%s\0%s' "$primary_root" "$target" |
 sha256sum |
 cut -c1-10
 )
 workspace_id="koa-${repo_slug}-${branch_slug}-${path_hash}"
 printf '%s\n' "$workspace_id" >"$workspace_id_file"
 chmod 600 "$workspace_id_file"
fi

case "$workspace_id" in
 *[!a-z0-9-]* | '')
 die "workspace identity contains unsupported characters: $workspace_id"
 ;;
esac

while IFS= read -r other_id_file; do
 test "$other_id_file" = "$workspace_id_file" && continue
 other_id=$(cat "$other_id_file" 2>/dev/null || true)
 test "$other_id" != "$workspace_id" ||
 die "workspace identity collision with $other_id_file"
done < <(
 find "$worktrees_root" \
 -path '*/.koa/workspace-id' \
 -type f \
 -print 2>/dev/null
)

workspace_env="$target/.koa/workspace.env"
compose_env="$target/.koa/compose.env"
workspace_json="$target/.koa/workspace.json"

port_base=
if test -f "$workspace_json"; then
 port_base=$(
 python3 - "$workspace_json" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
 data = json.load(handle)
print(data["port_base"])
PY
 )
fi

if test -z "$port_base"; then
 seed_hex=$(
 printf '%s' "$workspace_id" |
 sha256sum |
 cut -c1-8
 )
 seed=$((16#$seed_hex))

 for ((attempt = 0; attempt < 2500; attempt += 1)); do
 candidate=$((20000 + ((seed + attempt) % 2500) * 10))

 if existing_port_base "$worktrees_root" "$candidate"; then
 continue
 fi

 if port_block_free "$candidate"; then
 port_base=$candidate
 break
 fi
 done
fi

test -n "$port_base" ||
 die "no free workspace port block was found"

case "$port_base" in
 *[!0-9]* | '')
 die "invalid recorded port base: $port_base"
 ;;
esac

app_port=$((port_base + 0))
api_port=$((port_base + 1))
db_port=$((port_base + 2))
queue_port=$((port_base + 3))
search_port=$((port_base + 4))
metrics_port=$((port_base + 5))
debug_port=$((port_base + 6))
test_port=$((port_base + 7))

compose_project=$(printf '%s' "$workspace_id" | cut -c1-63)
db_suffix=$(
 printf '%s' "$workspace_id" |
 sha256sum |
 cut -c1-12
)
db_name="koa_${db_suffix}"
db_user="koa_${db_suffix}"
uv_cache=${UV_CACHE_DIR:-${XDG_CACHE_HOME:-$HOME/.cache}/uv}

secret_file="$target/.koa/secrets/db-password"
if ! test -f "$secret_file"; then
 umask 077
 openssl rand -hex 24 >"$secret_file"
fi
chmod 600 "$secret_file"

: >"$workspace_env"
write_export "$workspace_env" KOA_WORKSPACE_ID "$workspace_id"
write_export "$workspace_env" KOA_WORKSPACE_ROOT "$target"
write_export "$workspace_env" KOA_PRIMARY_WORKTREE "$primary_root"
write_export "$workspace_env" KOA_WORKTREES_ROOT "$worktrees_root"
write_export "$workspace_env" KOA_COMPOSE_PROJECT_NAME "$compose_project"
write_export "$workspace_env" COMPOSE_PROJECT_NAME "$compose_project"
write_export "$workspace_env" UV_PROJECT_ENVIRONMENT ".venv"
write_export "$workspace_env" UV_CACHE_DIR "$uv_cache"
write_export "$workspace_env" KOA_PORT_BASE "$port_base"
write_export "$workspace_env" KOA_APP_PORT "$app_port"
write_export "$workspace_env" KOA_API_PORT "$api_port"
write_export "$workspace_env" KOA_DB_PORT "$db_port"
write_export "$workspace_env" KOA_QUEUE_PORT "$queue_port"
write_export "$workspace_env" KOA_SEARCH_PORT "$search_port"
write_export "$workspace_env" KOA_METRICS_PORT "$metrics_port"
write_export "$workspace_env" KOA_DEBUG_PORT "$debug_port"
write_export "$workspace_env" KOA_TEST_PORT "$test_port"
write_export "$workspace_env" KOA_DB_NAME "$db_name"
write_export "$workspace_env" KOA_DB_USER "$db_user"
write_export "$workspace_env" KOA_DB_PASSWORD_FILE "$secret_file"
write_export "$workspace_env" KOA_RUNTIME_DIR "$target/.koa/run"
write_export "$workspace_env" KOA_LOG_DIR "$target/.koa/logs"
write_export "$workspace_env" KOA_TMP_DIR "$target/.koa/tmp"
write_export "$workspace_env" KOA_DATA_DIR "$target/.koa/data"
write_export "$workspace_env" KOA_ARTIFACT_DIR "$target/.koa/artifacts"
write_export "$workspace_env" KOA_BACKUP_DIR "$target/.koa/backups"
write_export "$workspace_env" KOA_RESTORE_DIR "$target/.koa/restore"
chmod 600 "$workspace_env"

cat >"$compose_env" <<EOF
KOA_WORKSPACE_ID=$workspace_id
COMPOSE_PROJECT_NAME=$compose_project
KOA_APP_PORT=$app_port
KOA_API_PORT=$api_port
KOA_DB_PORT=$db_port
KOA_QUEUE_PORT=$queue_port
KOA_SEARCH_PORT=$search_port
KOA_METRICS_PORT=$metrics_port
KOA_DEBUG_PORT=$debug_port
KOA_TEST_PORT=$test_port
KOA_DB_NAME=$db_name
KOA_DB_USER=$db_user
KOA_DB_PASSWORD_FILE=$secret_file
KOA_RUNTIME_DIR=$target/.koa/run
KOA_LOG_DIR=$target/.koa/logs
KOA_TMP_DIR=$target/.koa/tmp
KOA_DATA_DIR=$target/.koa/data
EOF
chmod 600 "$compose_env"

python3 - \
 "$workspace_json" \
 "$workspace_id" \
 "$primary_root" \
 "$target" \
 "$branch" \
 "$start_ref" \
 "$worktrees_root" \
 "$compose_project" \
 "$db_name" \
 "$db_user" \
 "$port_base" \
 "$uv_cache" <<'PY'
import json
import os
import sys
from pathlib import Path

(
 output,
 workspace_id,
 primary_root,
 target,
 branch,
 start_ref,
 worktrees_root,
 compose_project,
 db_name,
 db_user,
 port_base,
 uv_cache,
) = sys.argv[1:]

data = {
 "schema_version": "1.0.0",
 "workspace_id": workspace_id,
 "profile_ids": [
 "developer_linux_workstation",
 "developer_windows_wsl",
 ],
 "toolchain_id": "python_uv",
 "primary_worktree": primary_root,
 "worktree_root": target,
 "worktrees_root": worktrees_root,
 "branch": branch,
 "start_ref": start_ref,
 "compose_project_name": compose_project,
 "database_name": db_name,
 "database_user": db_user,
 "port_base": int(port_base),
 "ports": {
 "application": int(port_base) + 0,
 "api": int(port_base) + 1,
 "database": int(port_base) + 2,
 "queue": int(port_base) + 3,
 "search": int(port_base) + 4,
 "metrics": int(port_base) + 5,
 "debug": int(port_base) + 6,
 "test": int(port_base) + 7,
 },
 "paths": {
 "python_environment": str(Path(target) / ".venv"),
 "runtime": str(Path(target) / ".koa" / "run"),
 "logs": str(Path(target) / ".koa" / "logs"),
 "temporary": str(Path(target) / ".koa" / "tmp"),
 "secrets": str(Path(target) / ".koa" / "secrets"),
 "data": str(Path(target) / ".koa" / "data"),
 "artifacts": str(Path(target) / ".koa" / "artifacts"),
 "backups": str(Path(target) / ".koa" / "backups"),
 "restore": str(Path(target) / ".koa" / "restore"),
 },
 "shared_resources": {
 "uv_cache": uv_cache,
 },
 "mutable_sharing": "prohibited",
}

tmp = Path(output + ".tmp")
tmp.write_text(
 json.dumps(data, indent=2, sort_keys=True) + "\n",
 encoding="utf-8",
)
os.chmod(tmp, 0o600)
tmp.replace(output)
PY

(
 cd "$target"
 export UV_CACHE_DIR="$uv_cache"

 if test "${KOA_UV_OFFLINE:-0}" = "1"; then
 export UV_OFFLINE=1
 fi

 uv lock --check
 uv sync --frozen --all-groups

 test -d .venv || die "UV did not create the workspace .venv"
 test ! -L .venv || die "the workspace .venv is a symbolic link"

 venv_real=$(realpath .venv)
 expected_venv=$(realpath "$target/.venv")
 test "$venv_real" = "$expected_venv" ||
 die "the Python environment is outside the workspace"

 uv run --frozen python -c \
 'import pathlib,sys; print(pathlib.Path(sys.prefix).resolve)'
)

note ""
note "workspace configured"
note " id: $workspace_id"
note " branch: $branch"
note " path: $target"
note " ports: $port_base-$((port_base + 7))"
note " database: $db_name"
note ""
note "enter the workspace with:"
note " cd $(quote "$target")"
note " source .koa/workspace.env"

KOA_WORKTREE_CREATE

chmod 0755 "$HOME/.local/bin/koa-worktree-create"
bash -n "$HOME/.local/bin/koa-worktree-create"
`

**Expected result**

`text
$HOME/.local/bin/koa-worktree-create
`

exists, is executable, and passes Bash syntax validation.

**Verification**

`bash
command -v koa-worktree-create ||
 printf 'Add %s to PATH
' "$HOME/.local/bin"
`

**Failure behavior**

No worktree or workspace resource changes when script installation or syntax validation fails.

**Rollback effect**

Remove only the installed helper:

`bash
rm -f "$HOME/.local/bin/koa-worktree-create"
`

### Step 2 — Create a worktree

**Objective**

Create a branch worktree and assign a stable workspace identity and port block.

**Command**

`bash
cd /path/to/existing/koa-checkout

koa-worktree-create feature/civic-readings-v2 main
`

`/path/to/existing/koa-checkout` is an example shell argument, not a canonical repository path.

To use a specific sibling parent:

`bash
export KOA_WORKTREES_ROOT="$HOME/src/koa-worktrees"

koa-worktree-create feature/civic-readings-v2 main
`

For offline UV synchronization from the existing cache:

`bash
export KOA_UV_OFFLINE=1

koa-worktree-create feature/civic-readings-v2 main
`

**Expected result**

The helper reports the workspace identity, target path, port range, and database name.

The worktree contains:

`text
.koa/workspace-id
.koa/workspace.env
.koa/compose.env
.koa/workspace.json
.koa/secrets/db-password
.venv/
`

**Verification**

`bash
target="$HOME/src/koa-worktrees/feature-civic-readings-v2"

git -C "$target" branch --show-current
test -f "$target/.koa/workspace.json"
test -d "$target/.venv"
test ! -L "$target/.venv"
`

Adjust `target` to the path printed by the helper.

**Failure behavior**

A failed Git creation leaves no active workspace state when Git itself rolls back. A failure after worktree creation leaves a registered but non-ready worktree. Do not start services. Correct the reported condition or remove the worktree through Step 12.

**Rollback effect**

The cleanup procedure removes only the incomplete target and its Git worktree registration after reviewing source changes.

### Step 3 — Enter the workspace context

**Objective**

Load workspace-scoped names and paths into the current shell.

**Command**

`bash
cd "$HOME/src/koa-worktrees/feature-civic-readings-v2"
source .koa/workspace.env
`

**Expected result**

`bash
printf '%s
' "$KOA_WORKSPACE_ID" "$KOA_WORKSPACE_ROOT" "$KOA_PORT_BASE" "$KOA_DB_NAME" "$COMPOSE_PROJECT_NAME"
`

prints the values recorded for this workspace.

**Verification**

`bash
test "$PWD" = "$KOA_WORKSPACE_ROOT"
test -d "$KOA_WORKSPACE_ROOT/.venv"
test "$UV_PROJECT_ENVIRONMENT" = ".venv"
`

**Failure behavior**

Do not source an environment file from another worktree. If `PWD` and `KOA_WORKSPACE_ROOT` differ, start a fresh shell and source the correct file.

**Rollback effect**

Exit the shell or unset the exported variables.

### Step 4 — Verify frozen dependency authority

**Objective**

Confirm that the branch's dependency manifest and lockfile agree without updating dependency resolution.

**Command**

`bash
cd "$KOA_WORKSPACE_ROOT"

uv lock --check
uv sync --frozen --all-groups
`

**Expected result**

The existing `uv.lock` remains unchanged and `.venv` reflects the locked dependency groups.

**Verification**

`bash
git diff --exit-code -- uv.lock pyproject.toml .python-version

uv run --frozen python -c '
import pathlib
import sys

environment = pathlib.Path(".venv").resolve
prefix = pathlib.Path(sys.prefix).resolve
assert prefix == environment
print(prefix)
'
`

**Failure behavior**

A lock mismatch blocks the workspace from being considered ready. Refreshing the lockfile is a separate explicit dependency-change workflow.

**Rollback effect**

Delete only this workspace's `.venv` and repeat frozen synchronization:

`bash
rm -rf -- .venv
uv sync --frozen --all-groups
`

The shared UV cache remains intact.

### Step 5 — Verify the workspace manifest

**Objective**

Confirm that mutable names and paths belong to the current worktree.

**Command**

`bash
python3 -m json.tool .koa/workspace.json
`

**Expected result**

The manifest identifies the current branch, worktree path, workspace identity, port block, database identity, local paths, and shared UV cache.

**Verification**

`bash
python3 - <<'PY'
import json
from pathlib import Path

manifest = json.loads(
 Path(".koa/workspace.json").read_text(encoding="utf-8")
)
root = Path(manifest["worktree_root"]).resolve

assert root == Path.cwd.resolve
assert Path(manifest["paths"]["python_environment"]).resolve == (
 root / ".venv"
).resolve
assert manifest["mutable_sharing"] == "prohibited"
assert set(manifest["shared_resources"]) == {"uv_cache"}
assert len(set(manifest["ports"].values)) == 8

print(manifest["workspace_id"])
PY
`

**Failure behavior**

Do not start services from a manifest that points outside the current worktree or permits unsupported sharing.

**Rollback effect**

Regenerate the workspace state by rerunning `koa-worktree-create` for the same branch after preserving any required workspace-local data.

### Step 6 — Prepare a repository-defined service environment

**Objective**

Use the generated names and ports without hard-coding one workspace's values in source files.

**Command**

For a repository with `compose.yaml`:

`bash
cd "$KOA_WORKSPACE_ROOT"

docker compose --env-file .koa/compose.env --project-name "$KOA_COMPOSE_PROJECT_NAME" config --quiet
`

A Compose service can consume variables such as:

`text
KOA_APP_PORT
KOA_API_PORT
KOA_DB_PORT
KOA_QUEUE_PORT
KOA_SEARCH_PORT
KOA_DB_NAME
KOA_DB_USER
KOA_DB_PASSWORD_FILE
KOA_DATA_DIR
KOA_LOG_DIR
KOA_TMP_DIR
`

The repository's Compose file remains the owner of service definitions.

**Expected result**

The Compose configuration validates with workspace-scoped names.

**Verification**

`bash
docker compose --env-file .koa/compose.env --project-name "$KOA_COMPOSE_PROJECT_NAME" config |
 grep -F "$KOA_COMPOSE_PROJECT_NAME" >/dev/null || true
`

Compose output formats vary, so the definitive checks occur after startup through project and port inspection.

**Failure behavior**

A missing variable or invalid service definition blocks service startup. Do not replace it with another workspace's environment file.

**Rollback effect**

No service state exists after configuration-only validation.

### Step 7 — Start optional rootless services

**Objective**

Start only the services declared by the repository and selected developer profile.

**Command**

`bash
cd "$KOA_WORKSPACE_ROOT"

docker compose --env-file .koa/compose.env --project-name "$KOA_COMPOSE_PROJECT_NAME" up -d
`

**Expected result**

Containers, networks, and volumes are scoped by the Compose project name.

**Verification**

`bash
docker compose --env-file .koa/compose.env --project-name "$KOA_COMPOSE_PROJECT_NAME" ps

docker ps --filter "label=com.docker.compose.project=$KOA_COMPOSE_PROJECT_NAME"
`

Verify application health through the repository's capability-specific health checks rather than container existence alone.

**Failure behavior**

A port or volume collision stops service startup. Do not change another workspace's resources. Select a new workspace port block by removing the incomplete workspace state and recreating the worktree, or repair the undeclared external collision.

**Rollback effect**

`bash
docker compose --env-file .koa/compose.env --project-name "$KOA_COMPOSE_PROJECT_NAME" down --volumes --remove-orphans
`

This command is scoped to the current Compose project.

### Step 8 — Create a second worktree

**Objective**

Prove that two branches can run concurrently.

**Command**

From any existing checkout of the same repository:

`bash
koa-worktree-create fix/offline-replay-ledger main
`

Enter the second target and source its environment:

`bash
cd "$HOME/src/koa-worktrees/fix-offline-replay-ledger"
source .koa/workspace.env
`

**Expected result**

The second workspace has distinct identity, ports, database identity, `.venv`, mutable paths, and secret.

**Verification**

Use the cross-worktree validator installed in Step 9.

**Failure behavior**

An identity, port, database, or path collision blocks the validation result. Neither worktree is treated as a conforming parallel workspace until repaired.

**Rollback effect**

Remove only the second worktree through Step 12.

### Step 9 — Install the cross-worktree validator

**Objective**

Validate every sibling workspace without sourcing their environment files.

**Command**

`bash
cat >"$HOME/.local/bin/koa-worktree-check" <<'KOA_WORKTREE_CHECK'
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


def fail(message: str) -> None:
 print(f"error: {message}", file=sys.stderr)
 raise SystemExit(1)


def load_json(path: Path) -> dict[str, Any]:
 try:
 return json.loads(path.read_text(encoding="utf-8"))
 except (OSError, json.JSONDecodeError) as exc:
 fail(f"cannot read {path}: {exc}")


def git_worktrees(primary: Path) -> set[Path]:
 result = subprocess.run(
 ["git", "-C", str(primary), "worktree", "list", "--porcelain"],
 check=True,
 capture_output=True,
 text=True,
 )
 values: set[Path] = set
 for line in result.stdout.splitlines:
 if line.startswith("worktree "):
 values.add(Path(line.removeprefix("worktree ")).resolve)
 return values


def main -> None:
 parser = argparse.ArgumentParser
 parser.add_argument(
 "worktrees_root",
 type=Path,
 help="Directory containing sibling worktrees",
 )
 parser.add_argument(
 "--run-uv",
 action="store_true",
 help="Run frozen UV checks in every worktree",
 )
 args = parser.parse_args

 root = args.worktrees_root.expanduser.resolve
 manifests = sorted(root.glob("*/.koa/workspace.json"))
 if not manifests:
 fail(f"no workspace manifests found under {root}")

 identities: dict[str, Path] = {}
 compose_names: dict[str, Path] = {}
 database_names: dict[str, Path] = {}
 port_owners: dict[int, Path] = {}
 records: list[dict[str, Any]] = []

 for manifest in manifests:
 data = load_json(manifest)
 records.append(data)

 workspace_id = data.get("workspace_id")
 if not isinstance(workspace_id, str) or not workspace_id:
 fail(f"workspace_id is missing in {manifest}")
 if workspace_id in identities:
 fail(
 f"workspace identity collision: {workspace_id} in "
 f"{manifest} and {identities[workspace_id]}"
 )
 identities[workspace_id] = manifest

 worktree = Path(data["worktree_root"]).resolve
 expected_manifest = worktree / ".koa" / "workspace.json"
 if expected_manifest != manifest.resolve:
 fail(f"manifest path does not match worktree_root: {manifest}")

 if not worktree.is_dir:
 fail(f"worktree path is missing: {worktree}")

 python_environment = Path(
 data["paths"]["python_environment"]
 ).resolve
 expected_environment = (worktree / ".venv").resolve
 if python_environment != expected_environment:
 fail(f"Python environment is not workspace-local: {manifest}")
 if not python_environment.is_dir:
 fail(f"Python environment is missing: {python_environment}")
 if (worktree / ".venv").is_symlink:
 fail(f"Python environment is a symbolic link: {worktree}")

 compose_name = data["compose_project_name"]
 if compose_name in compose_names:
 fail(
 f"Compose project collision: {compose_name} in "
 f"{manifest} and {compose_names[compose_name]}"
 )
 compose_names[compose_name] = manifest

 database_name = data["database_name"]
 if database_name in database_names:
 fail(
 f"database-name collision: {database_name} in "
 f"{manifest} and {database_names[database_name]}"
 )
 database_names[database_name] = manifest

 ports = data.get("ports", {})
 if set(ports) != {
 "application",
 "api",
 "database",
 "queue",
 "search",
 "metrics",
 "debug",
 "test",
 }:
 fail(f"port manifest is incomplete: {manifest}")

 for name, value in ports.items:
 if not isinstance(value, int):
 fail(f"port {name} is not an integer in {manifest}")
 if value in port_owners:
 fail(
 f"port collision: {value} in "
 f"{manifest} and {port_owners[value]}"
 )
 port_owners[value] = manifest

 secret_dir = Path(data["paths"]["secrets"])
 mode = secret_dir.stat.st_mode & 0o777
 if mode & 0o077:
 fail(
 f"workspace secret directory is too permissive "
 f"({mode:o}): {secret_dir}"
 )

 shared = data.get("shared_resources", {})
 if set(shared) - {"uv_cache"}:
 fail(f"unsupported shared mutable resource in {manifest}")

 if data.get("mutable_sharing") != "prohibited":
 fail(f"mutable_sharing is not prohibited in {manifest}")

 primary = Path(records[0]["primary_worktree"]).resolve
 registered = git_worktrees(primary)
 for data in records:
 worktree = Path(data["worktree_root"]).resolve
 if worktree not in registered:
 fail(f"worktree is not registered with Git: {worktree}")

 if args.run_uv:
 for data in records:
 worktree = Path(data["worktree_root"]).resolve
 environment = os.environ.copy
 environment["UV_CACHE_DIR"] = data["shared_resources"]["uv_cache"]

 subprocess.run(
 ["uv", "lock", "--check"],
 cwd=worktree,
 env=environment,
 check=True,
 capture_output=True,
 text=True,
 )
 subprocess.run(
 [
 "uv",
 "run",
 "--frozen",
 "python",
 "-c",
 "import pathlib,sys;"
 "print(pathlib.Path(sys.prefix).resolve)",
 ],
 cwd=worktree,
 env=environment,
 check=True,
 capture_output=True,
 text=True,
 )

 print(
 json.dumps(
 {
 "result": "pass",
 "worktrees_root": str(root),
 "workspace_count": len(records),
 "workspace_ids": sorted(identities),
 "port_count": len(port_owners),
 "shared_resource_classes": ["uv_cache"],
 },
 indent=2,
 )
 )


if __name__ == "__main__":
 main

KOA_WORKTREE_CHECK

chmod 0755 "$HOME/.local/bin/koa-worktree-check"
python3 -m py_compile "$HOME/.local/bin/koa-worktree-check"
`

**Expected result**

The validator is executable and Python syntax is valid.

**Verification**

`bash
koa-worktree-check "$HOME/src/koa-worktrees"
`

Use the actual worktree parent printed by the creation helper.

**Failure behavior**

The validator reports the exact manifest, identity, path, port, Compose project, database name, secret-permission, or Git-registration conflict.

**Rollback effect**

Remove only the validator:

`bash
rm -f "$HOME/.local/bin/koa-worktree-check"
`

### Step 10 — Run full parallel isolation validation

**Objective**

Confirm that Git, UV, identities, paths, ports, database names, and secret boundaries are distinct.

**Command**

`bash
koa-worktree-check "$HOME/src/koa-worktrees" --run-uv
`

For every active worktree, also run the repository test gates from its own shell:

`bash
uv run --frozen pytest
uv run --frozen ruff check .
uv run --frozen ruff format --check .
uv run --frozen mypy .
`

**Expected result**

The validator returns JSON with:

`json
{
 "result": "pass",
 "workspace_count": 2,
 "port_count": 16,
 "shared_resource_classes": [
 "uv_cache"
 ]
}
`

The workspace identifiers in actual output depend on repository, branch, and path.

**Verification**

Run both branches' intended application or integration tests simultaneously and confirm that each result references its own workspace identity and state.

**Failure behavior**

A failed test remains attributable to one workspace. Do not repair it by mounting or connecting to another workspace's environment, service volume, database, or secret.

**Rollback effect**

Stop only the affected workspace's services and repair or recreate that workspace.

### Step 11 — Perform ordinary development

**Objective**

Keep every command inside the selected workspace authority and environment.

**Command**

`bash
cd "$KOA_WORKSPACE_ROOT"
source .koa/workspace.env

uv run --frozen python -m your_project
`

Use repository-defined commands for application startup, migrations, and tests.

**Expected result**

Python resolves through this worktree's `.venv`; services use this worktree's names and ports; data remains in this worktree's declared resources.

**Verification**

`bash
uv run --frozen python - <<'PY'
import os
import pathlib
import sys

root = pathlib.Path(os.environ["KOA_WORKSPACE_ROOT"]).resolve
environment = (root / ".venv").resolve
prefix = pathlib.Path(sys.prefix).resolve

assert pathlib.Path.cwd.resolve == root
assert prefix == environment

print(os.environ["KOA_WORKSPACE_ID"])
print(prefix)
PY
`

**Failure behavior**

Stop when a command resolves a Python interpreter, socket, port, database, secret, or data path outside the workspace declaration.

**Rollback effect**

Stop the affected process. No other workspace requires restart.

### Step 12 — Install and use the removal helper

**Objective**

Remove one worktree and its mutable state without changing another worktree or the shared UV cache.

**Command**

Install the helper:

`bash
cat >"$HOME/.local/bin/koa-worktree-remove" <<'KOA_WORKTREE_REMOVE'
#!/usr/bin/env bash
set -Eeuo pipefail

die {
 printf 'error: %s\n' "$*" >&2
 exit 1
}

target=${1:-}
confirmation=${2:-}

test -n "$target" && test -n "$confirmation" ||
 die "usage: koa-worktree-remove WORKTREE_PATH WORKSPACE_ID"

target=$(realpath "$target")
manifest="$target/.koa/workspace.json"

test -f "$manifest" ||
 die "workspace manifest is missing: $manifest"

readarray -t values < <(
 python3 - "$manifest" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
 data = json.load(handle)

print(data["workspace_id"])
print(data["primary_worktree"])
print(data["compose_project_name"])
print(data["shared_resources"]["uv_cache"])
PY
)

workspace_id=${values[0]}
primary_root=${values[1]}
compose_project=${values[2]}
uv_cache=${values[3]}

test "$confirmation" = "$workspace_id" ||
 die "confirmation does not match workspace identity: $workspace_id"

actual_branch=$(git -C "$target" branch --show-current)
test -n "$actual_branch" ||
 die "the target is not on a named branch"

if test -f "$target/compose.yaml" || test -f "$target/compose.yml"; then
 if command -v docker >/dev/null 2>&1 &&
 docker compose version >/dev/null 2>&1; then
 (
 cd "$target"
 docker compose \
 --env-file .koa/compose.env \
 --project-name "$compose_project" \
 down --volumes --remove-orphans
 )
 else
 die "workspace has a Compose file, but Docker Compose is unavailable"
 fi
fi

git -C "$target" diff --quiet
git -C "$target" diff --cached --quiet

untracked=$(
 git -C "$target" ls-files --others --exclude-standard
)
test -z "$untracked" ||
 die "untracked non-ignored files remain; review them before removal"

rm -rf -- \
 "$target/.venv" \
 "$target/.koa"

git -C "$primary_root" worktree remove "$target"
git -C "$primary_root" worktree prune

printf 'removed workspace %s from branch %s\n' \
 "$workspace_id" "$actual_branch"
printf 'shared UV cache retained: %s\n' "$uv_cache"

KOA_WORKTREE_REMOVE

chmod 0755 "$HOME/.local/bin/koa-worktree-remove"
bash -n "$HOME/.local/bin/koa-worktree-remove"
`

Inspect the workspace identity:

`bash
python3 -c '
import json
print(json.load(open(".koa/workspace.json"))["workspace_id"])
'
`

From outside the target worktree, remove it with an exact identity confirmation:

`bash
koa-worktree-remove "$HOME/src/koa-worktrees/feature-civic-readings-v2" koa-koa-feature-civic-readings-v2-7d3a9c52e1
`

The final identity above is illustrative. Use the exact value printed from the target manifest.

**Expected result**

The helper:

- stops the workspace's Compose project when present;
- rejects modified or non-ignored untracked source state;
- removes only the workspace `.venv` and `.koa`;
- removes the Git worktree;
- prunes stale Git worktree metadata;
- retains the shared UV cache.

**Verification**

`bash
git worktree list
test ! -e "$HOME/src/koa-worktrees/feature-civic-readings-v2"
`

Run the cross-worktree validator for remaining workspaces.

**Failure behavior**

The helper stops before deletion when confirmation, source cleanliness, Compose availability, or manifest validation fails.

**Rollback effect**

Worktree removal is destructive for disposable workspace state. Preserve or export required component data and backups before confirmation. The branch and committed Git history remain available.

## 11. Idempotency

`text
Idempotent: conditional
`

The creation helper is idempotent when:

- the target already belongs to the requested branch;
- `.koa/workspace-id` is valid;
- the recorded workspace manifest is compatible;
- the branch's lockfile remains valid;
- the workspace's `.venv` can be synchronized from the same lockfile.

Repeated execution:

- preserves the recorded workspace identity;
- preserves the recorded port base;
- preserves an existing database secret;
- rewrites environment and manifest projections deterministically from the recorded identity and port base;
- resynchronizes only the current workspace `.venv`;
- does not update `uv.lock`;
- does not duplicate Git worktree registration;
- does not change another workspace.

The helper stops on incompatible existing state instead of silently migrating it.

The removal helper is intentionally non-idempotent after successful removal because the target no longer exists. A second invocation reports the missing manifest.

## 12. Validation

### 12.1 Functional validation

Run:

`bash
koa-worktree-check "$KOA_WORKTREES_ROOT" --run-uv
`

Then execute the repository's frozen quality gates separately in each worktree:

`bash
uv lock --check
uv run --frozen pytest
uv run --frozen ruff check .
uv run --frozen ruff format --check .
uv run --frozen mypy .
`

### 12.2 Isolation validation

Confirm that every workspace has a unique:

`text
workspace_id
worktree_root
compose_project_name
database_name
database_user
port block
.venv path
secret directory
data directory
log directory
temporary directory
`

Confirm that the only declared shared resource class is:

`text
uv_cache
`

### 12.3 Git validation

`bash
git worktree list --porcelain
git -C "$KOA_WORKSPACE_ROOT" status --short
git -C "$KOA_WORKSPACE_ROOT" branch --show-current
`

Each worktree appears once and is on the intended branch.

### 12.4 Toolchain validation

`bash
test -f pyproject.toml
test -f uv.lock
test -f .python-version
test -d .venv
test ! -L .venv

uv lock --check
uv run --frozen python -c 'import pathlib,sys; print(pathlib.Path(sys.prefix).resolve)'
`

The interpreter path is inside the current worktree's `.venv`.

### 12.5 Secret validation

`bash
test -d .koa/secrets
test "$(stat -c '%a' .koa/secrets)" = "700"
test "$(stat -c '%a' .koa/secrets/db-password)" = "600"
`

Do not print the secret.

### 12.6 Service validation

For repositories with Compose:

`bash
docker compose --env-file .koa/compose.env --project-name "$KOA_COMPOSE_PROJECT_NAME" ps
`

Use component-specific readiness checks. Container liveness alone is insufficient.

### 12.7 Success criteria

The recipe succeeds when:

- every worktree has one stable identity;
- no two worktrees share a mutable Python environment;
- no port blocks overlap;
- no Compose project names overlap;
- no database names or identities overlap;
- no mutable service or application path overlaps;
- secret permissions pass;
- frozen UV checks pass;
- repository tests pass in each workspace;
- simultaneous operation succeeds;
- removal of one test workspace leaves another workspace healthy;
- the shared UV cache remains non-authoritative.

## 13. Failure Handling

| Failure | Detection | Safe state | Required action |
| --- | --- | --- | --- |
| Invalid branch name | `git check-ref-format` fails | No worktree created | Correct the branch name |
| Target directory belongs to another branch | Helper comparison fails | Existing target unchanged | Select another target or remove the old worktree safely |
| `.venv/` or `.koa/` is not ignored | Precondition check fails | Repository unchanged | Update and review the canonical ignore policy |
| Required project marker is missing | File check fails | No new worktree | Correct repository or toolchain scope |
| Lockfile is inconsistent | `uv lock --check` fails | Worktree exists but is not ready | Use the explicit dependency-change workflow |
| Shared `.venv` detected | Path or symlink validation fails | Services remain stopped | Delete the invalid environment and run frozen sync locally |
| Workspace identity collision | Cross-worktree check fails | Both worktrees remain isolated from startup | Correct the duplicate workspace state through controlled recreation |
| Port block collision | Creation or service bind fails | Services remain stopped | Remove undeclared listener or recreate the new workspace block |
| Database name collision | Manifest validator fails | Databases remain unchanged | Recreate the new workspace identity and database resources |
| Secret permissions too broad | Validator fails | Service startup remains blocked | Restore `0700` directory and `0600` file modes |
| UV cache unavailable | UV reports missing artifacts | Existing workspaces remain valid | Restore cache access or permit declared-source download |
| Offline cache incomplete | UV fails with offline mode | No dependency substitution | Import approved dependencies or reconnect to declared sources |
| Compose configuration invalid | `docker compose config` fails | No services start | Repair repository service configuration |
| One service fails | Capability health fails | Other workspace remains independent | Repair or stop only the affected workspace |
| Database migration fails | Migration validation fails | Original workspace remains untouched | Restore or forward-repair only the isolated target |
| Cleanup confirmation mismatch | Removal helper fails | Workspace unchanged | Use the exact manifest identity |
| Modified source exists during cleanup | Git checks fail | Workspace unchanged | Commit, stash, export, or discard explicitly |
| Untracked non-ignored source exists | Removal helper fails | Workspace unchanged | Review and classify the files |
| Shared cache deletion attempted | Review detects broad cleanup | Cache and workspaces remain protected | Remove only workspace-owned paths |
| Manifest is missing or invalid | Validator or removal helper fails | No destructive action | Recover the manifest from workspace evidence or remove manually after owner review |

Retries remain bounded by the failing operation. Repeated service startup does not trigger branch creation, lock refresh, or database migration.

## 14. Rollback

### 14.1 Rollback triggers

Rollback or workspace recreation is appropriate when:

- workspace identity or manifest state is invalid;
- a port or name collision cannot be repaired safely;
- `.venv` points outside the worktree;
- service state was created under the wrong Compose project;
- database or volume ownership is uncertain;
- a destructive migration has not crossed its irreversible boundary.

### 14.2 Rollback prerequisites

Before removal:

- stop application and test processes;
- preserve committed source;
- export required uncommitted changes;
- stop the workspace's Compose project;
- back up durable component data that must survive;
- verify the exact workspace identity;
- verify another workspace does not depend on the target's data.

### 14.3 Rollback procedure

For dependency-only rollback:

`bash
cd "$KOA_WORKSPACE_ROOT"
rm -rf -- .venv
uv sync --frozen --all-groups
`

For service-state rollback:

`bash
docker compose --env-file .koa/compose.env --project-name "$KOA_COMPOSE_PROJECT_NAME" down --volumes --remove-orphans
`

For full workspace removal, use the removal helper with exact identity confirmation.

### 14.4 Rollback verification

`bash
git worktree list
koa-worktree-check "$KOA_WORKTREES_ROOT" --run-uv
`

Remaining workspaces continue to pass.

### 14.5 Irreversible changes

Git worktree removal deletes disposable uncommitted and ignored workspace state after explicit cleanup.

Committed branch history remains.

Database migrations, destructive data reset, secret rotation, and artifact publication are outside this recipe and require their own backup, forward-repair, and evidence procedures.

## 15. Cleanup and Removal

Workspace cleanup order:

1. stop new work;
2. stop repository-defined services;
3. preserve or export required component data;
4. verify source cleanliness;
5. remove workspace-local containers, networks, and volumes;
6. remove `.venv`;
7. remove `.koa`;
8. remove the Git worktree;
9. prune stale Git worktree metadata;
10. validate remaining workspaces.

Do not use:

`bash
docker system prune
docker volume prune
rm -rf "$KOA_WORKTREES_ROOT"
rm -rf "$UV_CACHE_DIR"
`

as a substitute for workspace-scoped cleanup.

Those commands can affect unrelated workspaces or shared non-authoritative caches.

Intentionally retained state:

- the branch and committed Git history;
- the primary checkout;
- other worktrees;
- the shared UV cache;
- explicitly exported backups and evidence;
- user-local helper scripts until removed separately.

## 16. Observability and Evidence

### 16.1 Logs

Workspace logs use:

`text
.koa/logs
`

Service logs include the workspace identity or Compose project name.

Logs exclude secrets and protected application payloads.

### 16.2 Metrics

Useful development metrics include:

- active workspace count;
- allocated port blocks;
- workspace storage usage;
- `.venv` size;
- UV cache hits and misses;
- running service count by workspace;
- workspace queue depth;
- workspace health state;
- cleanup failures;
- orphaned workspace-resource count.

### 16.3 Receipts

`text
Receipt required: no
`

This recipe does not activate production authority.

For migration, backup, restore, trust, publication, or release tests executed inside a worktree, the applicable operation receipt remains required by its own contract.

### 16.4 Evidence

Recommended evidence for this recipe:

- `git worktree list --porcelain`;
- `.koa/workspace.json` for each test workspace;
- cross-worktree validator output;
- frozen UV check output;
- repository test output from each workspace;
- rootless service listing by Compose project;
- database and volume ownership checks;
- cleanup validation showing the remaining workspace is unaffected.

Evidence avoids secret values.

## 17. Offline Behavior

`text
offline_after_prerequisite_download
`

Git worktree creation is fully local when the requested start reference and branch objects already exist.

UV synchronization is fully offline when:

- the required Python runtime is available;
- all locked packages are present in the declared UV cache or approved offline source;
- `KOA_UV_OFFLINE=1` is set.

Offline execution:

`bash
export KOA_UV_OFFLINE=1
koa-worktree-create feature/offline-validation main
`

The helper does not contact external AI, publication, voice, search, or telemetry services.

A missing package in offline mode produces failure rather than dependency substitution or lock modification.

## 18. Compatibility and Versioning

| Dependency | Compatible behavior | Incompatible behavior | Migration action |
| --- | --- | --- | --- |
| `python_uv` toolchain | Workspace-local `.venv`, frozen lock, shared non-authoritative cache | Shared mutable environment or implicit global packages | Remove shared environment and synchronize each workspace |
| Git worktrees | Linked checkout with stable branch ownership | Copying a checkout without workspace registration | Register a new worktree and workspace identity |
| Developer profiles | Linux or WSL2 workspace isolation | Production or Windows-native assumptions | Use the profile-specific development recipe |
| Compose services | Project-scoped rootless resources | Global fixed container or volume names | Parameterize through generated workspace values |
| Databases | Workspace- and component-scoped names and identities | Shared mutable database identity or data directory | Use isolated migration and database recipe |
| Recipe `1.x` | Same manifest fields and eight-port allocation model | Changed identity or manifest semantics | Publish a major recipe revision and migration guidance |

A formatting-only recipe correction can remain within version `1.x`.

Changing workspace identity semantics, shared-resource policy, port-block semantics, cleanup authority, or required mutable-state boundaries requires a major recipe revision and accepted architectural impact when canonical behavior changes.

## 19. AI Execution Protocol

An AI agent executing this recipe:

1. loads the active developer profile and `python_uv` toolchain context;
2. verifies the recipe status and target platform;
3. verifies Git, UV, Python, and ignore preconditions;
4. uses the exact branch and start reference supplied for the task;
5. installs helper scripts only at the declared user-local path;
6. executes one numbered step at a time;
7. runs each verification before continuing;
8. records the actual worktree path and workspace identity;
9. avoids printing or reading secret contents;
10. stops on path, identity, port, database, service, or source-state conflict;
11. never updates `uv.lock` through this recipe;
12. never reuses another workspace's `.venv`, environment file, database, volume, secret, or service project;
13. reports a blocked result when canonical authority, required source state, or safe cleanup evidence is absent.

The agent does not infer a branch name, delete modified source, force-remove a worktree, run a broad container prune, or repair a database by direct cross-component writes.

Execution summary format:

`json
{
 "recipe_id": "RECIPE-DEV-002",
 "recipe_version": "1.0.0",
 "profile_ids": [
 "developer_linux_workstation"
 ],
 "component_ids": [],
 "workspace_id": "recorded-at-runtime",
 "decision_ids": [
 "DEC-DEV-001",
 "DEC-DEV-002",
 "DEC-DATA-001",
 "DEC-PROFILE-BASELINE-001"
 ],
 "lock_ids": [
 "LOCK-DEV-001",
 "LOCK-DEV-002",
 "LOCK-DEV-003",
 "LOCK-DEV-004",
 "LOCK-DEV-005",
 "LOCK-DATA-001"
 ],
 "commands_executed": [],
 "tests_run": [],
 "rollback_available": true,
 "result": "pass"
}
`

Runtime identifiers replace the illustrative string before the summary is used as evidence.

## 20. Troubleshooting

### Worktree target already exists

**Observed signal**

`text
error: target exists but is not a Git worktree
`

**Bounded causes**

- a stale ordinary directory uses the branch slug;
- the intended worktree was copied rather than registered;
- `KOA_WORKTREES_ROOT` points to the wrong parent.

**Diagnostic commands**

`bash
git worktree list --porcelain
ls -la "$KOA_WORKTREES_ROOT"
`

**Corrective action**

Move or remove the unrelated directory after verifying ownership, or select the correct declared parent.

### Branch already belongs to another worktree

**Observed signal**

Git reports that the branch is already checked out.

**Bounded causes**

- the same named branch is active in another linked worktree;
- the primary checkout is on that branch.

**Diagnostic command**

`bash
git worktree list
`

**Corrective action**

Use the existing worktree or create a distinct branch. Do not use Git force options to make the same branch writable in several worktrees.

### UV lock check fails

**Observed signal**

`text
uv lock --check
`

returns non-zero.

**Bounded causes**

- `pyproject.toml` changed without an explicit lock refresh;
- `uv.lock` belongs to another source state;
- the branch contains an incomplete dependency change.

**Corrective action**

Use the repository's dependency-update workflow. Do not run an unconstrained sync through this recipe.

### Interpreter resolves outside `.venv`

**Observed signal**

The printed Python path is outside the current worktree.

**Bounded causes**

- `UV_PROJECT_ENVIRONMENT` was overridden;
- `.venv` is a symbolic link;
- a shell alias bypasses UV;
- the wrong workspace environment was sourced.

**Diagnostic commands**

`bash
type -a uv python python3
printf '%s
' "${UV_PROJECT_ENVIRONMENT:-}"
realpath .venv
uv run --frozen python -c 'import pathlib,sys; print(pathlib.Path(sys.prefix).resolve)'
`

**Corrective action**

Start a clean shell, source the current `.koa/workspace.env`, remove only the current `.venv`, and run frozen synchronization.

### Port block is unavailable

**Observed signal**

The helper cannot find a free block, or a service cannot bind a recorded port.

**Bounded causes**

- an undeclared host process occupies the block;
- another worktree was created without the workspace manifest;
- a service from a removed workspace still runs;
- a port was bound after allocation.

**Diagnostic commands**

`bash
ss -ltn
git worktree list
docker ps
`

The Docker format braces above belong to Docker's command syntax and do not represent documentation placeholders.

**Corrective action**

Stop the verified stale process or recreate the new workspace so it receives another recorded block. Do not change the ports of an already active workspace without updating all of its declared resources.

### Compose project collision

**Observed signal**

Containers or volumes appear under another workspace's project.

**Bounded causes**

- `COMPOSE_PROJECT_NAME` was overridden;
- `.koa/compose.env` from another worktree was used;
- commands were run outside `KOA_WORKSPACE_ROOT`.

**Diagnostic commands**

`bash
printf '%s
' "$PWD" "$KOA_WORKSPACE_ROOT" "$KOA_COMPOSE_PROJECT_NAME"

docker compose ls
`

**Corrective action**

Stop only the incorrectly named project after verifying ownership, source the correct workspace environment, and restart with the explicit `--project-name` argument.

### Database state appears shared

**Observed signal**

Changes from one worktree appear in another.

**Bounded causes**

- both services use the same database URL;
- a global environment variable overrides generated names;
- the Compose file uses a global volume name;
- one worktree mounted another worktree's data path.

**Diagnostic commands**

`bash
printf '%s
' "$KOA_DB_NAME" "$KOA_DB_USER" "$KOA_DATA_DIR"

docker compose --env-file .koa/compose.env --project-name "$KOA_COMPOSE_PROJECT_NAME" config
`

**Corrective action**

Stop both affected service instances, preserve evidence, and repair the service or database configuration through the component and local-database isolation contracts. Do not continue writing to shared state.

### Cleanup refuses modified source

**Observed signal**

The removal helper exits before deleting the worktree.

**Bounded causes**

- tracked source is modified;
- staged changes exist;
- non-ignored untracked files exist.

**Diagnostic commands**

`bash
git status --short
git diff
git diff --cached
git ls-files --others --exclude-standard
`

**Corrective action**

Commit, export, stash, or discard each item explicitly. Rerun removal only when the source disposition is clear.

## 21. Non-Normative Example

A developer has a primary checkout at:

`text
/home/alex/src/koa
`

The developer creates two branches:

`bash
cd /home/alex/src/koa

koa-worktree-create feature/civic-readings-v2 main
koa-worktree-create fix/offline-replay-ledger main
`

The resulting paths are:

`text
/home/alex/src/koa-worktrees/feature-civic-readings-v2
/home/alex/src/koa-worktrees/fix-offline-replay-ledger
`

Illustrative generated state:

| Property | Civic branch | Replay branch |
| --- | --- | --- |
| Workspace ID | `koa-koa-feature-civic-readings-v2-7d3a9c52e1` | `koa-koa-fix-offline-replay-ledger-31a84f809d` |
| Port block | `28420-28427` | `39610-39617` |
| Compose project | First workspace ID | Second workspace ID |
| Database | `koa_f47a12496e8d` | `koa_97a5d2b7ca09` |
| Python environment | First worktree `.venv` | Second worktree `.venv` |
| Mutable data | First worktree `.koa/data` | Second worktree `.koa/data` |
| Shared resource | UV cache | Same UV cache |

The exact identities and ports are derived and recorded at runtime.

The developer starts services in each shell with its own environment and Compose project. Both branches run simultaneously. Deleting the civic worktree removes only its `.venv`, `.koa`, containers, network, volumes, and Git worktree registration. The replay worktree and shared UV cache remain intact.

## 22. Maintenance

Review this recipe when any referenced:

- development decision changes;
- developer profile changes;
- workspace schema changes;
- Python UV toolchain changes;
- workspace identity or naming rule changes;
- port-allocation contract changes;
- service-container recipe changes;
- database or secret isolation rule changes;
- storage cleanup rule changes;
- WSL support policy changes;
- relevant lock changes;
- Git or UV behavior changes incompatibly.

The recipe disposition after impact analysis is one of:

`text
updated
reviewed_no_change
deprecated
superseded
blocked
`

Deprecate this recipe when the method remains usable but is no longer recommended.

Supersede it when a replacement recipe has an active identity and migration path.

Archive it when no supported profile uses this implementation method.

## 23. Author and Operator Checklist

Before using the recipe:

- [ ] The selected profile is active.
- [ ] `DEC-DEV-001` and `DEC-DEV-002` are accepted.
- [ ] Applicable locks pass.
- [ ] Git, UV, Python, Bash, `sha256sum`, `realpath`, and OpenSSL are available.
- [ ] `.venv/` and `.koa/` are ignored.
- [ ] `pyproject.toml`, `uv.lock`, and `.python-version` exist.
- [ ] The branch name is valid.
- [ ] The target parent is on a Linux filesystem.
- [ ] Required package artifacts are available for offline mode.
- [ ] No production credential is present.

After creating each worktree:

- [ ] The workspace manifest parses.
- [ ] The workspace identity is unique.
- [ ] The port block is unique.
- [ ] The Compose project name is unique.
- [ ] The database name and identity are unique.
- [ ] `.venv` is local and not a symbolic link.
- [ ] Frozen UV checks pass.
- [ ] Secret permissions pass.
- [ ] Repository tests pass.
- [ ] Simultaneous operation passes.
- [ ] Health reports remain workspace- and capability-specific.

Before removal:

- [ ] Required source changes are committed or exported.
- [ ] Required component data is backed up.
- [ ] Services are stopped.
- [ ] The exact workspace identity is known.
- [ ] No other workspace depends on the target's mutable state.
- [ ] The shared UV cache is excluded from cleanup.
- [ ] Remaining workspaces are validated after removal.
