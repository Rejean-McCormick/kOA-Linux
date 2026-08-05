<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-RECIPE-DEV-006",
  "document_class": "recipe",
  "status": "active",
  "language": "en",
  "layer": "implementation_recipe",
  "recipe_id": "RECIPE-DEV-006",
  "recipe_version": "1.0.0",
  "scope": [
    "profile:developer_linux_workstation",
    "profile:developer_windows_wsl",
    "development_secret_isolation",
    "workspace_secret_lifecycle"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "generated/document-index.json",
    "contracts/terminology.contract.json",
    "contracts/profiles/developer-linux-workstation.profile.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "contracts/artifact-contracts/developer-workspace.schema.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-DATA-001",
    "DEC-DEV-001",
    "DEC-DEV-002",
    "DEC-GOV-001",
    "DEC-PROFILE-001"
  ],
  "requirement_ids": [
    "REQ-DEV-WS-001",
    "REQ-DEV-WS-002",
    "REQ-DEV-WS-005",
    "REQ-DEV-WS-007",
    "REQ-DEV-WS-008",
    "REQ-DEV-WS-010",
    "REQ-DEV-WS-011",
    "REQ-DEV-WS-012",
    "REQ-DEV-WS-026",
    "REQ-DEV-WS-027",
    "REQ-DEV-WS-028",
    "REQ-DEV-WS-029",
    "REQ-DEV-WS-034",
    "REQ-DEV-WS-035",
    "REQ-DEV-WS-036",
    "REQ-DEV-WS-037",
    "REQ-DEV-WS-038",
    "REQ-DEV-WS-040",
    "REQ-DEV-WS-041",
    "REQ-DEV-WS-042",
    "REQ-DEV-SEC-001",
    "REQ-DEV-SEC-002",
    "REQ-DEV-SEC-003",
    "REQ-DEV-SEC-004",
    "REQ-DEV-SEC-005",
    "REQ-DEV-SEC-006",
    "REQ-DEV-SEC-008",
    "REQ-DEV-SEC-009",
    "REQ-DEV-SEC-010",
    "REQ-DEV-SEC-011",
    "REQ-DEV-SEC-012",
    "REQ-DEV-SEC-013",
    "REQ-DEV-SEC-020",
    "REQ-DEV-SEC-021",
    "REQ-DEV-SEC-022",
    "REQ-DEV-SEC-023",
    "REQ-DEV-SEC-024",
    "REQ-DEV-SEC-026",
    "REQ-DEV-SEC-027",
    "REQ-DEV-SEC-028",
    "REQ-DEV-SEC-031",
    "REQ-DEV-SEC-032",
    "REQ-DEV-SEC-033",
    "REQ-DEV-SEC-034",
    "REQ-DEV-SEC-041",
    "REQ-DEV-SEC-042",
    "REQ-DEV-SEC-043",
    "REQ-DEV-SEC-044",
    "REQ-DEV-SEC-045",
    "REQ-DEV-SEC-046",
    "REQ-DEV-SEC-047",
    "REQ-DEV-SEC-048",
    "REQ-SEC-STOR-002",
    "REQ-SEC-STOR-003",
    "REQ-SEC-STOR-004",
    "REQ-SEC-STOR-005",
    "REQ-SEC-STOR-007",
    "REQ-SEC-STOR-010",
    "REQ-SEC-STOR-014",
    "REQ-SEC-STOR-015"
  ],
  "lock_ids": [
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-DEV-001",
    "LOCK-DEV-002",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DEV-005",
    "LOCK-DOC-003",
    "LOCK-DOC-004",
    "LOCK-GOV-001",
    "LOCK-IMPL-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-SEC-010"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-002",
    "DOC-CONST-013",
    "DOC-PROFILE-005",
    "DOC-DEV-003",
    "DOC-DEV-013",
    "DOC-SEC-009",
    "DOC-ADR-024"
  ],
  "tags": [
    "recipe",
    "development",
    "secrets",
    "workspace-isolation",
    "linux",
    "wsl",
    "least-privilege",
    "runtime-files",
    "cleanup",
    "non-normative"
  ]
}
KOA:DOC-META:END -->

# Development Secret Isolation

> **Recipe status:** Active, non-normative implementation recipe.
> **Implementation:** Workspace-scoped protected files outside the repository, with runtime-only copies and file-reference injection.
> **Authority rule:** This recipe demonstrates one compliant method. Active contracts and profiles remain authoritative.

---

## Recipe Identity

| Field | Value |
| --- | --- |
| Recipe ID | `RECIPE-DEV-006` |
| Title | Development Secret Isolation |
| Status | Active |
| Version | `1.0.0` |
| Owner | Development Security |
| Last reviewed | 2026-08-03 |
| Applies to profiles | `developer_linux_workstation`, `developer_windows_wsl` |
| Applies to components | Any development component with declared workspace-scoped secrets |
| Applies to toolchains | POSIX-compatible development shell and profile-selected local service or container runtime |
| Supported platforms | Native Linux; Linux environment inside WSL |
| Supersedes | None |
| Replaced by | None |

---

## 1. Purpose

This recipe configures workspace-scoped development secrets so that:

- secret values remain outside the source repository;
- persistent development values are stored in a user-owned protected directory;
- services receive runtime-only copies by file reference;
- values do not appear in command arguments, committed configuration, general logs, container images, or shared mutable caches;
- cleanup removes runtime copies without affecting another workspace;
- rotation and suspected exposure have explicit procedures.

Successful completion produces a workspace with:

`text
persistent protected secret files
→ runtime-only protected copies
→ service-specific file references
→ verified repository and permission boundaries
`

This recipe does not define:

- canonical secret field names;
- a production secret manager;
- production credentials;
- component authorization;
- a privileged host mechanism;
- a new profile requirement;
- an artifact or release contract.

## 2. Non-Normative Status

This recipe is non-normative unless an active profile explicitly adopts this exact implementation.

The following remain authoritative:

- workspace identity and isolation contracts;
- development-security requirements;
- component secret declarations;
- profile-specific credential-store mechanisms;
- Identity and Trust;
- Governance Policy Runtime;
- component data ownership;
- applicable exceptions and locks.

This recipe does not authorize:

- creating a secret that the workspace contract does not declare;
- using production credentials locally;
- sharing a secret between workspaces;
- bypassing an external provider's credential issuance and revocation process;
- granting a process broader access because the developer owns the host;
- placing values in an environment file committed to source control.

A conflict with active authority invalidates this recipe.

## 3. Scope

### 3.1 Included

This recipe covers:

- resolving one existing `workspace_id`;
- creating persistent and runtime secret roots;
- adding local repository exclusions;
- creating a secret interactively without placing its value in shell history;
- rotating a development secret atomically;
- copying a secret into runtime-only storage;
- injecting a secret into a local process through a file-reference variable;
- mounting a runtime secret read-only into a rootless container when the active toolchain supports it;
- validating ownership, permissions, path separation, and repository exclusion;
- clearing runtime copies;
- revoking and removing workspace-local development values.

### 3.2 Excluded

This recipe does not cover:

- production, governance, root, recovery, or signing keys;
- production service credentials;
- staging credentials unless an active staging workflow explicitly permits them;
- centralized team secret-manager deployment;
- hardware-backed key custody;
- operating-system keyring configuration;
- issuing provider credentials;
- component authorization decisions;
- database-user creation;
- certificate-authority operation;
- host privilege escalation;
- secret synchronization between people or machines.

### 3.3 Supported profiles

Supported:

- `developer_linux_workstation`
- `developer_windows_wsl`

For WSL, all secret files remain inside the Linux filesystem and not under a Windows-mounted source path.

Unsupported:

| Profile | Reason |
| --- | --- |
| `user_lightweight` | User deployment uses its own active profile secret mechanism |
| `sovereign_linux_node` | Production sovereign operation requires the profile-approved production mechanism |
| `sovereign_hub` | Shared sovereign services require stronger operational and custody controls |
| `build_farm` | Clean workers require ephemeral build-authority credential delivery |
| `control_plane` | Control-plane secrets require its explicit identity and orchestration contracts |

### 3.4 Supported platforms and versions

| Platform or tool | Supported version | Canonical source |
| --- | --- | --- |
| Native Linux user session | Version selected by active profile | Developer Linux profile |
| WSL Linux environment | Version selected by active profile | Developer Windows/WSL profile |
| Bash-compatible shell | Profile-installed version | Active profile |
| Git | Profile-installed version | Active development toolchain |
| Python | Declared workspace or profile version | Active workspace and toolchain |
| Rootless container runtime | Only when selected by active profile | Container-runtime toolchain |

No version absent from canonical authority is invented by this recipe.

## 4. Canonical References

### 4.1 Decisions

- `DEC-DATA-001`
- `DEC-DEV-001`
- `DEC-DEV-002`
- `DEC-GOV-001`
- `DEC-PROFILE-001`

### 4.2 Primary requirements

- `REQ-DEV-WS-028`
- `REQ-DEV-WS-029`
- `REQ-DEV-SEC-008`
- `REQ-DEV-SEC-009`
- `REQ-DEV-SEC-010`
- `REQ-DEV-SEC-011`
- `REQ-DEV-SEC-012`
- `REQ-DEV-SEC-013`
- `REQ-DEV-SEC-022`
- `REQ-DEV-SEC-027`
- `REQ-DEV-SEC-032`
- `REQ-DEV-SEC-042`
- `REQ-DEV-SEC-044`
- `REQ-DEV-SEC-045`
- `REQ-DEV-SEC-046`

The metadata block contains the complete referenced requirement set.

### 4.3 Locks

- `LOCK-DATA-001`
- `LOCK-DEV-001`
- `LOCK-DEV-002`
- `LOCK-DEV-003`
- `LOCK-DEV-004`
- `LOCK-DEV-005`
- `LOCK-IMPL-001`
- `LOCK-PROFILE-001`
- `LOCK-PROFILE-002`
- `LOCK-SEC-010`

### 4.4 Profiles and artifact contracts

- `contracts/profiles/developer-linux-workstation.profile.json`
- `contracts/profiles/developer-windows-wsl.profile.json`
- `contracts/artifact-contracts/developer-workspace.schema.json`

### 4.5 Related documentation

- `docs/03-profiles/05-developer-linux-workstation.md`
- `docs/05-development/03-workspace-isolation.md`
- `docs/05-development/13-development-security.md`
- `docs/07-security/09-storage-boundaries.md`
- `docs/10-adrs/ADR-024-logical-data-ownership-with-profile-dependent-physical-isolation.md`

## 5. Preconditions

### 5.1 Authority preconditions

Before execution:

- the workspace declaration exists and validates;
- the workspace has a stable unique `workspace_id`;
- every required secret is declared by name, owner, purpose, component, environment, and capability;
- no production signing, root, recovery, or unrestricted production service credential is requested;
- the active profile permits protected-file secret storage for development;
- any shared development credential has separate authorization;
- applicable exceptions are active and exact-scope;
- the target service supports a file reference or protected file mount.

If any condition fails, the result is `blocked`.

### 5.2 Environment preconditions

The shell session has:

- `WORKSPACE_ID` set to the exact workspace identifier;
- `WORKSPACE_ROOT` resolved from the workspace repository;
- a user-owned Linux home directory;
- a user-owned `XDG_RUNTIME_DIR`;
- `bash`, `git`, `python3`, `install`, `find`, and `stat`;
- no root requirement;
- no repository checkout located inside the planned secret directory.

Verification:

`bash
set -euo pipefail

: "${WORKSPACE_ID:?WORKSPACE_ID must be set from the workspace declaration}"

WORKSPACE_ROOT="$(git rev-parse --show-toplevel)"
test -d "$WORKSPACE_ROOT/.git" || test -f "$WORKSPACE_ROOT/.git"

: "${XDG_RUNTIME_DIR:?XDG_RUNTIME_DIR must be provided by the Linux user session}"
test -d "$XDG_RUNTIME_DIR"
test -O "$XDG_RUNTIME_DIR"

command -v bash
command -v git
command -v python3
command -v install
command -v find
command -v stat
`

### 5.3 Secret-name preconditions

This recipe uses lowercase secret names with underscores:

`text
^[a-z][a-z0-9_]*$
`

Each name identifies one value.

Names do not contain:

- tenant data;
- usernames;
- provider account numbers;
- secret fragments;
- environment values;
- timestamps used as rotation state.

Validation:

`bash
SECRET_NAME="${SECRET_NAME:?SECRET_NAME must be set}"

python3 - "$SECRET_NAME" <<'PY'
import re
import sys

name = sys.argv[1]
if not re.fullmatch(r"[a-z][a-z0-9_]*", name):
 raise SystemExit("invalid secret name")
PY
`

### 5.4 Filesystem preconditions

Persistent state is placed under:

`text
${XDG_STATE_HOME:-$HOME/.local/state}/koa/workspaces/$WORKSPACE_ID/secrets
`

Runtime copies are placed under:

`text
$XDG_RUNTIME_DIR/koa/workspaces/$WORKSPACE_ID/secrets
`

Both paths must be outside the repository.

`bash
STATE_HOME="${XDG_STATE_HOME:-$HOME/.local/state}"
SECRET_ROOT="$STATE_HOME/koa/workspaces/$WORKSPACE_ID/secrets"
RUNTIME_SECRET_ROOT="$XDG_RUNTIME_DIR/koa/workspaces/$WORKSPACE_ID/secrets"

case "$SECRET_ROOT/" in
 "$WORKSPACE_ROOT/"*) printf '%s
' "persistent secret root is inside repository" >&2; exit 1 ;;
esac

case "$RUNTIME_SECRET_ROOT/" in
 "$WORKSPACE_ROOT/"*) printf '%s
' "runtime secret root is inside repository" >&2; exit 1 ;;
esac
`

## 6. Inputs and Outputs

### 6.1 Inputs

| Input | Type | Source | Required | Sensitive |
| --- | --- | --- | ---: | ---: |
| `WORKSPACE_ID` | Identifier | Validated workspace declaration | Yes | No |
| `WORKSPACE_ROOT` | Filesystem path | Git repository resolution | Yes | No |
| `SECRET_NAME` | Identifier | Component or workspace secret declaration | Yes | No |
| Secret value | Opaque byte string without terminal newline | Interactive terminal or approved issuer flow | Yes | Yes |
| Service file-reference variable | Identifier | Component configuration contract | Yes for local process injection | No |
| Container target path | Path | Component or container contract | Conditional | No |
| Expiry and rotation rule | Policy metadata | Secret declaration or issuer | Yes when applicable | No |

### 6.2 Outputs

| Output | Type | Destination | Authority |
| --- | --- | --- | --- |
| Persistent development value | Protected file | `$SECRET_ROOT/$SECRET_NAME` | Workspace-scoped local development state |
| Runtime copy | Protected file | `$RUNTIME_SECRET_ROOT/$SECRET_NAME` | Ephemeral execution state |
| Repository exclusions | Local Git metadata | `$WORKSPACE_ROOT/.git/info/exclude` or resolved common Git directory | Local safety control |
| Verification result | Structured text | Terminal or authorized evidence collector | Non-authoritative recipe result |
| Exposure response record | Incident evidence | Applicable security workflow | Development security contract |

### 6.3 Mutable state

This recipe can create or modify:

- persistent secret-root directories;
- runtime secret-root directories;
- secret files;
- local Git exclusion metadata;
- running service environment containing secret file paths;
- read-only container mounts;
- security evidence about permission or leak checks.

It does not modify:

- source-controlled application files;
- another workspace's state;
- production secret stores;
- canonical registries;
- component authoritative data;
- release artifacts.

## 7. Safety and Security Boundaries

### 7.1 Privilege model

`text
unprivileged user
`

Do not run this recipe with `sudo`.

The persistent and runtime roots must be owned by the current Linux user.

A service that requires a different identity needs a profile-approved delivery mechanism rather than relaxed file permissions.

### 7.2 Secret handling

Secret values are:

- read without terminal echo;
- written with `0600` permissions;
- stored outside the repository;
- copied to a runtime directory with `0600` permissions;
- referenced by path rather than placed in process arguments;
- excluded from diagnostics;
- removed from shell variables immediately after writing;
- never displayed by validation commands.

Do not use:

`text
command --password=value
export PASSWORD=value
echo value > file
cat secret-file
set -x
docker build --build-arg secret=value
`

Do not enable shell tracing during secret operations.

### 7.3 Persistent versus runtime state

Persistent development values survive a user-session restart.

Runtime copies exist only for active service execution and should disappear when the user session or workspace stops.

The persistent root is the local development source for staging a runtime copy. It is not a canonical secret manager and is not suitable for production.

### 7.4 Network boundaries

This recipe requires no network access.

Credential issuance or rotation by an external provider is a separate explicit action.

The secret value is not transmitted by the recipe.

### 7.5 Data authority

Secret storage does not grant component or business authority.

A valid credential can authenticate a request but does not bypass:

- component interfaces;
- Governance Policy Runtime;
- tenant scope;
- data ownership;
- publication rules;
- artifact admission;
- release activation.

### 7.6 External integrations and AI

Do not send:

- secret values;
- private key material;
- complete environment files;
- unrestricted workspace configuration;
- credential-store screenshots;
- terminal output containing values

to an external integration or AI surface.

An AI agent may execute structural checks and protected write procedures. It must not request the value in conversational text or include the value in its execution summary.

## 8. Resource Envelope

Secret isolation has negligible resource demand relative to the active workspace.

| Resource | Expected | Maximum | Enforcement |
| --- | --- | --- | --- |
| CPU | Short bounded local operations | Active workspace envelope | Resource Governor or profile controls |
| Memory | One entered value plus command overhead | Active workspace envelope | Process and workspace limits |
| Persistent storage | Declared development values only | Workspace storage allocation | Filesystem quota or profile control |
| Runtime storage | Active service values only | Workspace runtime allocation | Runtime directory and workspace cleanup |
| I/O | Small local file operations | Active workspace envelope | Filesystem and workspace limits |
| Processes | Shell and bounded helper process | Active workspace process limit | Resource Governor or profile controls |
| Concurrent secret operations | One per secret name | Workspace policy | Operator sequencing |

Secret files must not be used for large fixtures, certificates chains with unrelated content, database exports, or arbitrary configuration bundles.

## 9. Naming and Isolation

### 9.1 Canonical naming inputs

This recipe uses:

`text
workspace_id
secret_name
component_id
`

The directory path includes `workspace_id`.

The filename includes only `secret_name`.

### 9.2 Workspace-scoped resources

`bash
STATE_HOME="${XDG_STATE_HOME:-$HOME/.local/state}"
SECRET_ROOT="$STATE_HOME/koa/workspaces/$WORKSPACE_ID/secrets"
RUNTIME_SECRET_ROOT="$XDG_RUNTIME_DIR/koa/workspaces/$WORKSPACE_ID/secrets"
`

Two workspaces with the same secret name receive different paths because their `workspace_id` values differ.

### 9.3 Collision behavior

Allowed behavior:

- reuse an existing directory only after ownership and permissions pass;
- refuse creation when a secret file already exists;
- rotate through an explicit atomic replacement;
- stop when a path is a symlink, non-regular file, wrong owner, or wrong permission.

Silent overwrite during creation is prohibited.

### 9.4 Symlink boundary

Secret roots and files must not be symlinks.

A symlink can redirect a write into:

- source control;
- another workspace;
- shared state;
- an attacker-controlled path.

Verification rejects any symlink before use.

## 10. Procedure

### Step 1 — Resolve the workspace and secret roots

**Objective**

Create stable shell variables from the already validated workspace identity.

**Command**

`bash
set -euo pipefail
set +x
umask 077

: "${WORKSPACE_ID:?WORKSPACE_ID must be set}"

WORKSPACE_ROOT="$(git rev-parse --show-toplevel)"
STATE_HOME="${XDG_STATE_HOME:-$HOME/.local/state}"
SECRET_ROOT="$STATE_HOME/koa/workspaces/$WORKSPACE_ID/secrets"
RUNTIME_SECRET_ROOT="${XDG_RUNTIME_DIR:?}/koa/workspaces/$WORKSPACE_ID/secrets"

export WORKSPACE_ROOT STATE_HOME SECRET_ROOT RUNTIME_SECRET_ROOT
`

**Expected result**

All four variables resolve to absolute paths. Secret roots are outside the repository.

**Verification**

`bash
python3 - "$WORKSPACE_ROOT" "$SECRET_ROOT" "$RUNTIME_SECRET_ROOT" <<'PY'
from pathlib import Path
import sys

workspace, persistent, runtime = map(lambda value: Path(value).resolve, sys.argv[1:])
for candidate in (persistent, runtime):
 if candidate == workspace or workspace in candidate.parents:
 raise SystemExit(f"secret path inside repository: {candidate}")
PY
`

**Failure behavior**

No directory or file is created.

**Rollback effect**

None.

---

### Step 2 — Create protected directories

**Objective**

Create user-owned `0700` persistent and runtime directories without following an existing symlink.

**Command**

`bash
test ! -L "$STATE_HOME/koa" || { printf '%s
' "state path is a symlink" >&2; exit 1; }
test ! -L "$STATE_HOME/koa/workspaces" || { printf '%s
' "workspace state path is a symlink" >&2; exit 1; }
test ! -L "$RUNTIME_SECRET_ROOT" || { printf '%s
' "runtime secret root is a symlink" >&2; exit 1; }

install -d -m 0700 "$STATE_HOME/koa"
install -d -m 0700 "$STATE_HOME/koa/workspaces"
install -d -m 0700 "$STATE_HOME/koa/workspaces/$WORKSPACE_ID"
install -d -m 0700 "$SECRET_ROOT"

install -d -m 0700 "$XDG_RUNTIME_DIR/koa"
install -d -m 0700 "$XDG_RUNTIME_DIR/koa/workspaces"
install -d -m 0700 "$XDG_RUNTIME_DIR/koa/workspaces/$WORKSPACE_ID"
install -d -m 0700 "$RUNTIME_SECRET_ROOT"
`

**Expected result**

Every created directory is owned by the current user and has mode `0700`.

**Verification**

`bash
for directory in "$SECRET_ROOT" "$RUNTIME_SECRET_ROOT"; do
 test -d "$directory"
 test ! -L "$directory"
 test -O "$directory"
 test "$(stat -c '%a' "$directory")" = "700"
done
`

**Failure behavior**

Stop before writing any secret.

**Rollback effect**

Empty directories created by this step can be removed from deepest to shallowest.

---

### Step 3 — Add local repository exclusions

**Objective**

Prevent common local secret filenames from being accidentally tracked while leaving shared repository policy unchanged.

**Command**

`bash
GIT_DIR="$(git -C "$WORKSPACE_ROOT" rev-parse --git-dir)"
case "$GIT_DIR" in
 /*) ;;
 *) GIT_DIR="$WORKSPACE_ROOT/$GIT_DIR" ;;
esac

EXCLUDE_FILE="$GIT_DIR/info/exclude"
install -d -m 0700 "$(dirname "$EXCLUDE_FILE")"
touch "$EXCLUDE_FILE"
chmod 0600 "$EXCLUDE_FILE"

for pattern in ".env" ".env.*" ".secrets/" "secrets.local/" "*.private.pem" "*.private.key" "*.p12" "*.pfx"
do
 grep -Fqx "$pattern" "$EXCLUDE_FILE" || printf '%s
' "$pattern" >> "$EXCLUDE_FILE"
done
`

**Expected result**

Local secret-like files are ignored in this checkout without changing repository-controlled `.gitignore`.

**Verification**

`bash
grep -Fqx ".env" "$EXCLUDE_FILE"
grep -Fqx ".secrets/" "$EXCLUDE_FILE"
test "$(stat -c '%a' "$EXCLUDE_FILE")" = "600"
`

**Failure behavior**

No secret is created until the local exclusion file passes.

**Rollback effect**

Remove only lines added by this recipe if rollback is required.

---

### Step 4 — Create one persistent development secret

**Objective**

Create a new value without terminal echo, command-line exposure, or overwrite.

**Command**

`bash
: "${SECRET_NAME:?SECRET_NAME must be set}"

python3 - "$SECRET_ROOT" "$SECRET_NAME" <<'PY'
from getpass import getpass
from pathlib import Path
import os
import re
import stat
import sys

root = Path(sys.argv[1])
name = sys.argv[2]

if not re.fullmatch(r"[a-z][a-z0-9_]*", name):
 raise SystemExit("invalid secret name")
if root.is_symlink or not root.is_dir:
 raise SystemExit("invalid secret root")
if root.stat.st_uid != os.getuid:
 raise SystemExit("secret root not owned by current user")
if stat.S_IMODE(root.stat.st_mode) != 0o700:
 raise SystemExit("secret root mode must be 0700")

target = root / name
if target.exists or target.is_symlink:
 raise SystemExit("secret already exists; use the rotation procedure")

value = getpass("Secret value: ")
if not value:
 raise SystemExit("empty secret rejected")

flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
fd = os.open(target, flags, 0o600)
try:
 os.write(fd, value.encode("utf-8"))
 os.fsync(fd)
finally:
 os.close(fd)

value = ""
PY
`

**Expected result**

`$SECRET_ROOT/$SECRET_NAME` exists as a regular `0600` file owned by the current user.

**Verification**

`bash
SECRET_PATH="$SECRET_ROOT/$SECRET_NAME"

test -f "$SECRET_PATH"
test ! -L "$SECRET_PATH"
test -O "$SECRET_PATH"
test "$(stat -c '%a' "$SECRET_PATH")" = "600"
test -s "$SECRET_PATH"
`

**Failure behavior**

The target remains absent if validation or writing fails.

**Rollback effect**

Delete the newly created value and revoke it at its issuer when it was already activated externally.

---

### Step 5 — Stage a runtime-only copy

**Objective**

Copy the persistent value into the user-session runtime directory for one active workspace.

**Command**

`bash
SECRET_PATH="$SECRET_ROOT/$SECRET_NAME"
RUNTIME_SECRET_PATH="$RUNTIME_SECRET_ROOT/$SECRET_NAME"

test -f "$SECRET_PATH"
test ! -L "$SECRET_PATH"
test -O "$SECRET_PATH"
test "$(stat -c '%a' "$SECRET_PATH")" = "600"

install -m 0600 "$SECRET_PATH" "$RUNTIME_SECRET_PATH"
`

**Expected result**

A runtime copy exists with the same opaque value and protected permissions.

**Verification**

`bash
test -f "$RUNTIME_SECRET_PATH"
test ! -L "$RUNTIME_SECRET_PATH"
test -O "$RUNTIME_SECRET_PATH"
test "$(stat -c '%a' "$RUNTIME_SECRET_PATH")" = "600"

python3 - "$SECRET_PATH" "$RUNTIME_SECRET_PATH" <<'PY'
from pathlib import Path
import hmac
import sys

left = Path(sys.argv[1]).read_bytes
right = Path(sys.argv[2]).read_bytes
if not hmac.compare_digest(left, right):
 raise SystemExit("runtime copy differs")
PY
`

The comparison does not print the value and does not create a retained digest.

**Failure behavior**

Do not start the dependent service.

**Rollback effect**

Remove the incomplete runtime copy.

---

### Step 6 — Inject the secret into a local process by file reference

**Objective**

Expose only the protected path through the service environment.

**Command**

The component contract supplies the file-reference variable name. This example uses a fictional local service variable:

`bash
export EXAMPLE_SERVICE_TOKEN_FILE="$RUNTIME_SECRET_PATH"
exec ./scripts/run-development-service
`

**Expected result**

The service reads the value from the file. The process argument list contains no value.

**Verification**

From another shell, verify the service command line does not contain the secret filename's contents and that its configured file path belongs to the active workspace.

Use the component's health command to prove service readiness.

**Failure behavior**

Stop the service. Do not fall back to an inline command argument or committed environment file.

**Rollback effect**

Unset the file-reference variable and remove the runtime copy after the process exits.

---

### Step 7 — Inject into a rootless container when adopted

**Objective**

Mount one runtime secret read-only without embedding it in an image or container command.

**Command**

When the active container toolchain supports an OCI read-only bind mount:

`bash
podman run --rm --name "${WORKSPACE_ID}-example-service" --mount "type=bind,src=$RUNTIME_SECRET_PATH,dst=/run/secrets/$SECRET_NAME,ro" --env "EXAMPLE_SERVICE_TOKEN_FILE=/run/secrets/$SECRET_NAME" example-service-development-image
`

The image name above is illustrative and must be replaced by the exact admitted development image identity already declared by the workspace.

**Expected result**

The container can read `/run/secrets/$SECRET_NAME`; the file is read-only; the host value remains outside the image and repository.

**Verification**

Use the component's health test and the runtime's inspect command to confirm:

- rootless execution;
- one explicit read-only mount;
- no secret-value environment variable;
- no unrelated home or credential-store mount;
- no host container-control socket.

**Failure behavior**

Do not add broader mounts, privileged mode, inline environment values, or image build arguments.

**Rollback effect**

Stop and remove the container, then remove the runtime copy.

---

### Step 8 — Validate the workspace secret boundary

**Objective**

Prove path, ownership, permission, repository, and workspace isolation.

**Command**

`bash
python3 - "$WORKSPACE_ROOT" "$SECRET_ROOT" "$RUNTIME_SECRET_ROOT" "$WORKSPACE_ID" <<'PY'
from pathlib import Path
import os
import stat
import sys

workspace = Path(sys.argv[1]).resolve
roots = [Path(sys.argv[2]).resolve, Path(sys.argv[3]).resolve]
workspace_id = sys.argv[4]

for root in roots:
 if root == workspace or workspace in root.parents:
 raise SystemExit("secret root inside repository")
 if workspace_id not in root.parts:
 raise SystemExit("workspace_id absent from secret path")
 if root.is_symlink or not root.is_dir:
 raise SystemExit("invalid secret root")
 if root.stat.st_uid != os.getuid:
 raise SystemExit("wrong secret-root owner")
 if stat.S_IMODE(root.stat.st_mode) != 0o700:
 raise SystemExit("wrong secret-root mode")
 for item in root.iterdir:
 if item.is_symlink or not item.is_file:
 raise SystemExit(f"invalid secret entry: {item.name}")
 if item.stat.st_uid != os.getuid:
 raise SystemExit(f"wrong owner: {item.name}")
 if stat.S_IMODE(item.stat.st_mode) != 0o600:
 raise SystemExit(f"wrong mode: {item.name}")
PY
`

Check tracked filenames:

`bash
if git -C "$WORKSPACE_ROOT" ls-files | grep -E '(^|/)(\.env($|\.)|\.secrets/|secrets\.local/)|\.(private\.pem|private\.key|p12|pfx)$'
then
 printf '%s
' "tracked secret-like path detected" >&2
 exit 1
fi
`

Check for a private-key marker in tracked content, excluding this recipe text:

`bash
if git -C "$WORKSPACE_ROOT" grep -I -n -e 'BEGIN PRIVATE KEY' -e 'BEGIN RSA PRIVATE KEY' -e 'BEGIN EC PRIVATE KEY' -- . ':!docs/11-recipes/development/secret-isolation.md'
then
 printf '%s
' "private-key marker detected in tracked content" >&2
 exit 1
fi
`

**Expected result**

Every check exits zero and prints no secret value.

**Failure behavior**

Mark workspace activation or sharing as `blocked`. Investigate before continuing.

**Rollback effect**

None; validation is read-only.

---

### Step 9 — Rotate a development secret

**Objective**

Atomically replace the local development value without retaining the old value.

**Command**

`bash
: "${SECRET_NAME:?SECRET_NAME must be set}"

python3 - "$SECRET_ROOT" "$SECRET_NAME" <<'PY'
from getpass import getpass
from pathlib import Path
import os
import re
import stat
import sys
import tempfile

root = Path(sys.argv[1])
name = sys.argv[2]

if not re.fullmatch(r"[a-z][a-z0-9_]*", name):
 raise SystemExit("invalid secret name")

target = root / name
if target.is_symlink or not target.is_file:
 raise SystemExit("existing regular secret required")
if target.stat.st_uid != os.getuid:
 raise SystemExit("wrong secret owner")
if stat.S_IMODE(target.stat.st_mode) != 0o600:
 raise SystemExit("wrong secret mode")

first = getpass("New secret value: ")
second = getpass("Repeat new secret value: ")
if not first or first != second:
 raise SystemExit("new values do not match")

fd, temporary_name = tempfile.mkstemp(prefix=f".{name}.", dir=root)
temporary = Path(temporary_name)
try:
 os.fchmod(fd, 0o600)
 os.write(fd, first.encode("utf-8"))
 os.fsync(fd)
 os.close(fd)
 fd = -1
 os.replace(temporary, target)
 directory_fd = os.open(root, os.O_RDONLY)
 try:
 os.fsync(directory_fd)
 finally:
 os.close(directory_fd)
finally:
 if fd >= 0:
 os.close(fd)
 temporary.unlink(missing_ok=True)

first = ""
second = ""
PY
`

Restage the runtime copy and restart only the dependent service.

**Expected result**

The persistent file is atomically replaced. No old value is retained by this recipe.

**Verification**

Repeat the permission and service-readiness checks.

**Failure behavior**

If replacement fails before `os.replace`, the old value remains. If the issuer already revoked the old credential, complete rotation through forward repair by issuing and installing another new value.

**Rollback effect**

Old values are not restored from local backup. Use the credential issuer's declared dual-validity or reissuance procedure.

---

### Step 10 — Clear runtime secret copies

**Objective**

Remove ephemeral values after dependent services stop.

**Command**

`bash
test -d "$RUNTIME_SECRET_ROOT"
find "$RUNTIME_SECRET_ROOT" -mindepth 1 -maxdepth 1 -type f -exec chmod 0600 {} +
find "$RUNTIME_SECRET_ROOT" -mindepth 1 -maxdepth 1 -type f -delete
`

**Expected result**

The runtime root is empty.

**Verification**

`bash
test -z "$(find "$RUNTIME_SECRET_ROOT" -mindepth 1 -maxdepth 1 -print -quit)"
`

**Failure behavior**

Mark workspace shutdown incomplete and prevent handoff of the machine or workspace until cleanup succeeds.

**Rollback effect**

None. Runtime copies are reconstructible from persistent workspace values.

## 11. Idempotency

`text
Idempotent: conditional
`

Idempotent operations:

- resolving paths;
- creating already-correct directories;
- adding an already-present local exclusion;
- staging a runtime copy from the current persistent value;
- validating permissions and repository state;
- clearing an already-empty runtime directory.

Non-idempotent operations:

- initial secret creation, which refuses an existing target;
- rotation, which intentionally replaces the current value;
- external credential issuance or revocation;
- permanent removal of a persistent value.

Repeated execution never creates a second identifier for the same `workspace_id` and `secret_name`.

Creation and rotation are separate procedures so rerunning initialization cannot rotate a credential accidentally.

## 12. Validation

### 12.1 Functional validation

`bash
test -d "$SECRET_ROOT"
test -d "$RUNTIME_SECRET_ROOT"
test "$(stat -c '%a' "$SECRET_ROOT")" = "700"
test "$(stat -c '%a' "$RUNTIME_SECRET_ROOT")" = "700"

find "$SECRET_ROOT" -mindepth 1 -maxdepth 1 -type f ! -perm 0600 -print -quit |
 grep -q . && exit 1 || true

find "$RUNTIME_SECRET_ROOT" -mindepth 1 -maxdepth 1 -type f ! -perm 0600 -print -quit |
 grep -q . && exit 1 || true
`

Expected result:

`text
All roots and files are current-user owned, workspace-scoped, and protected.
`

### 12.2 Contract validation

Validate the workspace declaration through the active workspace validation tool.

The validation must confirm that:

- `workspace_id` matches;
- the secret reference is declared;
- the component and capability scope match;
- the active profile matches;
- the workspace is not using a production credential class.

If the canonical validator is unavailable, the result is `blocked`.

### 12.3 Secret-detection validation

Before sharing source, logs, diagnostics, screenshots, or artifacts:

1. run the active registered secret scanner;
2. run the structural filename and private-key checks in Step 8;
3. inspect staged Git changes;
4. sanitize diagnostics;
5. block sharing on an unresolved finding.

A scanner finding is reviewed without printing the full detected value.

### 12.4 Lock validation

`bash
python docs/tools/check_interfile_locks.py
`

Expected locks include:

- `LOCK-DATA-001`
- `LOCK-DEV-001`
- `LOCK-DEV-002`
- `LOCK-DEV-003`
- `LOCK-DEV-004`
- `LOCK-DEV-005`
- `LOCK-IMPL-001`
- `LOCK-PROFILE-001`
- `LOCK-PROFILE-002`
- `LOCK-SEC-010`

### 12.5 Documentation validation

`bash
python docs/tools/validate_docs.py
`

### 12.6 Success criteria

The recipe succeeds only when:

- roots are outside the repository;
- roots are `0700`;
- secret files are regular, non-symlink, current-user-owned, and `0600`;
- persistent and runtime paths contain the exact `workspace_id`;
- no production credential class is present;
- no secret value appears in source control, command arguments, logs, images, receipts, or diagnostics;
- dependent services use file references or read-only file mounts;
- unrelated workspaces cannot resolve or access the paths;
- the active scanner and structural checks pass;
- runtime cleanup passes;
- applicable locks pass.

## 13. Failure Handling

| Failure | Detection | Safe state | Required action |
| --- | --- | --- | --- |
| Missing workspace identity | Required-variable check fails | No state created | Resolve the validated workspace declaration |
| Secret root inside repository | Path validation fails | No value written | Correct the state-root configuration |
| Root or file is a symlink | Symlink check fails | Operation blocked | Remove only after ownership investigation |
| Wrong directory permission | `stat` differs from `0700` | No service start | Correct ownership and permission |
| Wrong file permission | `stat` differs from `0600` | Secret not staged | Correct permission and assess exposure |
| Existing value during creation | Exclusive create fails | Existing value unchanged | Use explicit rotation |
| Runtime copy mismatch | Constant-time comparison fails | Service remains stopped | Delete runtime copy and restage |
| Secret-like tracked path | Git check reports path | Sharing blocked | Remove from tracking, rotate if exposed |
| Private-key marker in tracked content | Git content check reports file | Sharing blocked | Remove, revoke, rotate, inspect history |
| Secret scanner unavailable | Required tool cannot run | Sharing blocked | Restore admitted scanner or use approved equivalent |
| Service lacks file-reference support | Component configuration cannot consume file | Activation blocked | Add owner-approved support; do not inline value |
| Container needs broad host mount | Runtime configuration requests broad mount | Container remains stopped | Define a narrow secret mount |
| Runtime cleanup fails | Runtime directory remains non-empty | Workspace shutdown incomplete | Stop processes, correct ownership, remove copies |
| Suspected external exposure | Incident signal or scanner finding | Affected credential treated as compromised | Revoke, rotate, preserve bounded evidence, assess scope |

Retries are bounded to the failed local operation.

Repeated retries must not display the value or broaden permissions.

## 14. Rollback

### 14.1 Rollback triggers

Rollback applies when:

- initialization created unused empty directories;
- local exclusions were added to the wrong checkout;
- a runtime copy was staged for a service that did not start;
- a newly created credential is rejected before use;
- validation detects an unsafe path or permission.

### 14.2 Rollback prerequisites

- dependent services are stopped;
- exact `workspace_id` is confirmed;
- exact secret root is outside the repository;
- external issuer revocation is available when the value was issued externally.

### 14.3 Rollback procedure

Remove runtime copies:

`bash
find "$RUNTIME_SECRET_ROOT" -mindepth 1 -maxdepth 1 -type f -delete
`

Remove one newly created unused value:

`bash
: "${SECRET_NAME:?}"
test -f "$SECRET_ROOT/$SECRET_NAME"
test ! -L "$SECRET_ROOT/$SECRET_NAME"
rm -- "$SECRET_ROOT/$SECRET_NAME"
`

Remove empty roots:

`bash
rmdir "$RUNTIME_SECRET_ROOT" 2>/dev/null || true
rmdir "$XDG_RUNTIME_DIR/koa/workspaces/$WORKSPACE_ID" 2>/dev/null || true
rmdir "$SECRET_ROOT" 2>/dev/null || true
rmdir "$STATE_HOME/koa/workspaces/$WORKSPACE_ID" 2>/dev/null || true
`

### 14.4 Rollback verification

`bash
test ! -e "$RUNTIME_SECRET_ROOT/$SECRET_NAME"
test ! -e "$SECRET_ROOT/$SECRET_NAME"
`

When an external credential was created, verify revocation with the issuer's approved procedure.

### 14.5 Irreversible changes

Local deletion of a secret value is irreversible by design.

Rotation also discards the old local value.

Recovery uses issuer-side reissuance or another new value. The recipe does not retain old secret backups.

## 15. Cleanup and Removal

### 15.1 Routine workspace stop

1. stop dependent services;
2. clear runtime copies;
3. preserve persistent development values only when the workspace remains active;
4. clear exported file-reference variables;
5. verify no orphan process holds a deleted runtime file.

### 15.2 Workspace retirement

Require exact confirmation:

`bash
: "${WORKSPACE_ID:?}"
: "${CONFIRM_WORKSPACE_ID:?CONFIRM_WORKSPACE_ID must be set}"
test "$CONFIRM_WORKSPACE_ID" = "$WORKSPACE_ID"
`

Then:

1. revoke externally issued credentials;
2. stop all workspace services;
3. remove runtime copies;
4. remove persistent values;
5. remove empty workspace secret directories;
6. remove only recipe-added local exclusions if the checkout remains;
7. preserve incident evidence without secret values;
8. verify other workspace roots remain unchanged.

Example scoped deletion:

`bash
test -d "$SECRET_ROOT"
test ! -L "$SECRET_ROOT"

find "$SECRET_ROOT" -mindepth 1 -maxdepth 1 -type f -delete
rmdir "$SECRET_ROOT"
rmdir "$STATE_HOME/koa/workspaces/$WORKSPACE_ID" 2>/dev/null || true
`

Do not recursively remove `$STATE_HOME/koa/workspaces`.

## 16. Observability and Evidence

### 16.1 Logs

Permitted logs include:

- recipe ID and version;
- `workspace_id`;
- secret name;
- operation class: create, stage, validate, rotate, revoke, cleanup;
- result;
- permission and ownership status;
- service restart result;
- incident or correlation ID.

Logs exclude:

- values;
- value length when it can disclose sensitive information;
- file contents;
- private keys;
- full provider responses;
- unrestricted environment dumps.

### 16.2 Metrics

Useful local metrics:

- number of declared secret references;
- number of persistent files;
- number of active runtime copies;
- number of permission failures;
- number of unresolved scanner findings;
- number of expired or revoked references;
- runtime cleanup success.

Metrics remain workspace-scoped.

### 16.3 Receipts

`text
Receipt required: no for ordinary local file creation and staging.
`

A structured receipt or security event is required when applicable policy classifies:

- suspected exposure;
- use of a shared credential;
- privileged secret delivery;
- emergency revocation;
- security incident recovery.

### 16.4 Evidence

Required evidence can include:

- workspace declaration validation;
- path-separation result;
- ownership and mode result;
- tracked-file structural scan;
- registered secret-scanner result;
- service file-reference configuration result;
- runtime cleanup result;
- incident revocation evidence when applicable.

Evidence contains references and outcomes, not values.

## 17. Offline Behavior

`text
fully_offline
`

The file-isolation, creation, staging, injection, validation, rotation, and cleanup procedure requires no network access.

External credential issuance or revocation can require network access according to the issuer.

When an issuer is unavailable:

- do not invent a local substitute for an external credential;
- continue with already admitted non-expired development values when policy permits;
- block operations requiring a new or revoked credential;
- preserve local isolation and scanner checks.

This recipe never silently contacts an external service.

## 18. Compatibility and Versioning

| Dependency | Compatible range | Incompatible condition | Action |
| --- | --- | --- | --- |
| Developer workspace contract | Active version declaring workspace secrets | Missing or invalid workspace declaration | Block |
| Native Linux profile | Active profile supporting protected user files | Profile requires another secret store | Use profile mechanism |
| Windows/WSL profile | Active Linux environment with Linux filesystem storage | Secret root on Windows-mounted source path | Move to Linux state directory |
| Component configuration | Supports file reference or protected mount | Requires command-line value or committed file | Change component configuration |
| Container runtime | Active rootless runtime supporting narrow read-only mount | Requires privileged or broad host access | Block container path |
| Python helper | Active declared Python capable of standard-library operations used here | Python unavailable or untrusted | Use approved equivalent |
| Recipe versions | `1.x` | Major path, authority, or lifecycle change | Follow replacement recipe |

A breaking change to:

- secret-root semantics;
- supported profiles;
- ownership;
- injection model;
- cleanup;
- exposure response

requires a major recipe version and impact review.

## 19. AI Execution Protocol

An AI agent using this recipe must:

1. load active AI context;
2. verify recipe status and version;
3. resolve the workspace contract;
4. verify exact `workspace_id`;
5. verify the requested secret class is permitted;
6. refuse production signing, root, recovery, or unrestricted production credentials;
7. use interactive terminal entry or an approved non-conversational issuer path;
8. never ask the user to paste a value into chat;
9. disable shell tracing;
10. execute one atomic step at a time;
11. run verification after every step;
12. stop on symlink, owner, permission, path, scanner, or service-consumption mismatch;
13. record only names, paths, outcomes, and evidence references;
14. clear runtime copies after dependent processes stop;
15. report `blocked` when canonical authority, scanner, issuer, or file-reference support is absent.

The agent must not:

- print or summarize a value;
- include a value in tool arguments visible to logs when avoidable;
- store a value in repository files;
- use inline environment values for convenience;
- broaden file permissions;
- use root;
- inspect unrelated workspace secret roots;
- rotate an existing value during initialization;
- remove persistent values without exact workspace confirmation;
- treat this recipe as authorization.

### 19.1 Example execution summary

`json
{
 "recipe_id": "RECIPE-DEV-006",
 "recipe_version": "1.0.0",
 "profile_ids": ["developer_linux_workstation"],
 "component_ids": ["example_service"],
 "workspace_id": "example-service-feature-auth-a1b2",
 "secret_names": ["example_service_token"],
 "commands_executed": [
 "resolve_workspace",
 "create_protected_roots",
 "create_secret",
 "stage_runtime_copy",
 "validate_boundary"
 ],
 "tests_run": [
 "workspace_contract_validation",
 "secret_path_and_permission_validation",
 "tracked_file_secret_scan"
 ],
 "evidence_ids": [],
 "rollback_available": true,
 "result": "pass"
}
`

The example contains no credential value.

## 20. Troubleshooting

### Secret root is inside the repository

**Observed signal**

`text
secret path inside repository
`

**Likely bounded causes**

- `XDG_STATE_HOME` points into the checkout;
- the repository is located under a custom state root;
- a wrapper supplied an unsafe path.

**Diagnostic command**

`bash
printf '%s
' "$WORKSPACE_ROOT" "$SECRET_ROOT" "$RUNTIME_SECRET_ROOT"
`

**Corrective action**

Set a user-state root outside the repository and repeat path validation.

**Escalation condition**

The active profile mandates a path that conflicts with workspace isolation.

---

### Secret file has incorrect permissions

**Observed signal**

`text
wrong secret mode
`

**Likely bounded causes**

- file was copied by another tool;
- a restore preserved broad permissions;
- manual modification changed the mode.

**Diagnostic command**

`bash
stat -c '%U %G %a %n' "$SECRET_ROOT/$SECRET_NAME"
`

**Corrective action**

When ownership is correct and no exposure is suspected:

`bash
chmod 0600 "$SECRET_ROOT/$SECRET_NAME"
`

If another user could read it, revoke and rotate the credential.

**Escalation condition**

Ownership differs or exposure scope is uncertain.

---

### Service accepts only an inline value

**Observed signal**

`text
service configuration has no file-reference or protected-file input
`

**Likely bounded causes**

- component configuration lacks a `_FILE`-style option;
- wrapper translates configuration incorrectly;
- container entrypoint assumes inline environment values.

**Diagnostic action**

Review the owning component configuration contract.

**Corrective action**

Add an owner-approved file-reference mechanism or narrow startup wrapper that reads the file inside the process boundary.

**Escalation condition**

The component would require command-line exposure, committed `.env`, or broad environment export.

---

### Secret-like file is tracked

**Observed signal**

`text
tracked secret-like path detected
`

**Likely bounded causes**

- local exclusion was added after the file was tracked;
- a secret was created in the repository;
- a generated certificate used an unsafe filename or path.

**Diagnostic command**

`bash
git -C "$WORKSPACE_ROOT" ls-files |
 grep -E '(^|/)(\.env($|\.)|\.secrets/|secrets\.local/)|\.(private\.pem|private\.key|p12|pfx)$'
`

**Corrective action**

Remove the file from tracking without deleting unrelated files, revoke and rotate any exposed value, inspect repository history, and run the registered scanner.

**Escalation condition**

The value reached a remote repository, artifact, diagnostic bundle, external AI surface, or shared log.

---

### Runtime copy remains after service stop

**Observed signal**

`text
runtime secret directory is not empty
`

**Likely bounded causes**

- cleanup was skipped;
- process still uses the file;
- ownership changed;
- another undeclared service created state in the directory.

**Diagnostic command**

`bash
find "$RUNTIME_SECRET_ROOT" -mindepth 1 -maxdepth 1 -printf '%u %m %f
'
`

**Corrective action**

Stop the exact workspace services, investigate unexpected files, and run Step 10.

**Escalation condition**

The file is owned by another user, belongs to another workspace, or cannot be attributed.

## 21. Non-Normative Example

A workspace has:

`text
workspace_id: example-service-feature-auth-a1b2
component_id: example_service
secret_name: example_service_token
`

The developer runs:

`bash
export WORKSPACE_ID="example-service-feature-auth-a1b2"
export SECRET_NAME="example_service_token"

WORKSPACE_ROOT="$(git rev-parse --show-toplevel)"
STATE_HOME="${XDG_STATE_HOME:-$HOME/.local/state}"
SECRET_ROOT="$STATE_HOME/koa/workspaces/$WORKSPACE_ID/secrets"
RUNTIME_SECRET_ROOT="${XDG_RUNTIME_DIR:?}/koa/workspaces/$WORKSPACE_ID/secrets"
`

The value is entered interactively through Step 4.

The service receives:

`bash
export EXAMPLE_SERVICE_TOKEN_FILE="$RUNTIME_SECRET_ROOT/$SECRET_NAME"
exec ./scripts/run-development-service
`

After the service stops:

`bash
find "$RUNTIME_SECRET_ROOT" -mindepth 1 -maxdepth 1 -type f -delete
`

The example identifiers and variable names are illustrative, not canonical defaults.

## 22. Maintenance

Review this recipe when any referenced:

- workspace contract changes;
- development profile changes;
- secret requirement changes;
- storage-boundary decision changes;
- container-runtime contract changes;
- component secret-consumption interface changes;
- WSL filesystem guidance changes;
- secret scanner changes;
- incident-response process changes;
- applicable lock changes.

Maintenance outcomes are:

`text
updated
reviewed_no_change
regenerated
deprecated
blocked
`

Deprecate this recipe when protected files are no longer the recommended development method.

Supersede it when an active replacement recipe provides a migration path.

## 23. Author Checklist

- [x] Recipe identity and version are present.
- [x] Status is active and non-normative.
- [x] Supported and unsupported profiles are explicit.
- [x] Canonical decisions, requirements, locks, and documentation are referenced.
- [x] No version absent from authority is invented.
- [x] Preconditions are testable.
- [x] Persistent and runtime state are declared.
- [x] Privilege is unprivileged.
- [x] Values remain outside source control.
- [x] Paths include `workspace_id`.
- [x] Creation and rotation are separate.
- [x] Symlinks and collisions fail closed.
- [x] File-reference and read-only-mount injection are documented.
- [x] Validation prints no value.
- [x] Cleanup is workspace-scoped.
- [x] Offline behavior is explicit.
- [x] AI execution does not request conversational values.
- [x] Failure, rollback, exposure response, and maintenance are complete.

## 24. Review Checklist

- [x] The recipe creates no independent normative authority.
- [x] The recipe does not define production secret storage.
- [x] The recipe does not globalize Linux or WSL implementation choices.
- [x] The recipe does not use root.
- [x] The recipe does not copy values into source-controlled configuration.
- [x] The recipe preserves workspace and component isolation.
- [x] The recipe preserves logical data ownership.
- [x] The recipe does not treat possession of a credential as business authority.
- [x] The recipe does not weaken controls when offline.
- [x] The recipe includes bounded diagnostics.
- [x] The recipe requires rotation after exposure.
- [x] The recipe preserves other workspaces during cleanup.
- [x] Applicable locks and documentation checks are listed.

## 25. Final Recipe Rule

> This recipe stores development secret values outside the repository, scopes them by `workspace_id`, stages only protected runtime copies, and injects them by file reference. It remains one implementation method. Active profiles, component contracts, security requirements, decisions, and locks define the required outcome.
