<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-RECIPE-DEV-001",
  "document_class": "recipe",
  "version": "1.0.0",
  "status": "active",
  "language": "en",
  "layer": "development",
  "owner": "development-architecture",
  "scope": [
    "profile:developer_linux_workstation",
    "profile:developer_windows_wsl"
  ],
  "canonical_refs": [
    "schemas/developer-workspace.schema.json",
    "contracts/toolchains/python-uv.toolchain.json",
    "contracts/artifact-contracts/developer-workspace.schema.json",
    "contracts/artifact-contracts/workspace-port-allocation.schema.json",
    "contracts/artifact-contracts/resource-envelope.schema.json",
    "contracts/profiles/developer-linux-workstation.profile.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "generated/assertion-index.json"
  ],
  "decision_ids": [
    "DEC-DEV-001",
    "DEC-DEV-002",
    "DEC-CONTAINER-001"
  ],
  "requirement_ids": [
    "REQ-DEV-UV-001",
    "REQ-DEV-UV-002",
    "REQ-DEV-UV-003",
    "REQ-DEV-STATE-001",
    "REQ-DEV-PARALLEL-001"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-DEV-001",
    "LOCK-DEV-002",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DEV-005"
  ],
  "adr_ids": [
    "ADR-005",
    "ADR-015"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-ADR-005",
    "DOC-ADR-015",
    "DOC-DEV-002",
    "DOC-DEV-003",
    "DOC-DEV-004",
    "DOC-DEV-005",
    "DOC-DEV-006",
    "DOC-DEV-007",
    "DOC-DEV-008",
    "DOC-DEV-009",
    "DOC-DEV-010",
    "DOC-DEV-011",
    "DOC-DEV-012",
    "DOC-DEV-013",
    "DOC-DEV-014",
    "DOC-DEV-016",
    "DOC-CONF-017"
  ],
  "tags": [
    "recipe",
    "development",
    "python",
    "uv",
    "workspace",
    "virtual-environment",
    "parallel-branches",
    "ports",
    "networks",
    "databases",
    "secrets",
    "resources",
    "teardown"
  ],
  "effective_at": "2026-08-03T19:45:00-04:00"
}
KOA:DOC-META:END -->

# Python UV Workspace

> **Recipe status:** active and non-normative. Canonical requirements remain in the referenced decisions, contracts, schemas, locks, and profile documents.

This recipe creates one isolated Python workspace for either:

- `developer_linux_workstation`;
- `developer_windows_wsl`.

It implements the architecture described by `ADR-015`:

`text
component + branch_or_purpose + unique_suffix
 → stable workspace_id
 → workspace-local .venv
 → namespaced mutable state
 → frozen validation
 → independent teardown
`

The example workspace is:

`text
konnaxion-feature-voting-92cd
`

Adapt component, purpose, suffix, Python version, ports, database identities, service names, resource limits, and runtime commands to the active profile and component contract.

## Outcome

At completion, the workspace has:

- a stable `workspace_id`;
- a Git worktree or equivalent source-control workspace;
- versioned `pyproject.toml`;
- versioned `uv.lock`;
- versioned `.python-version`;
- one workspace-local `.venv`;
- `uv sync --frozen` validation;
- workspace-scoped runtime directories;
- a validated `developer_workspace` contract;
- unique services, databases, ports, network, sockets, secrets, and resource limits;
- a repeatable parallel-workspace check;
- an independent teardown path.

UV isolates the Python dependency environment. It does not isolate databases, queues, search services, host ports, networks, volumes, sockets, secrets, system libraries, or resource use. Those domains remain explicit in the workspace contract.

## Prerequisites

The workstation needs:

`text
git
uv
python available through UV
a JSON Schema validator
the selected profile runtime for local services
`

For Linux development, rootless Podman is preferred when containers are used.

For Windows WSL, Docker or Podman is permitted. Run the Linux workspace commands inside the declared WSL distribution and record which services or ports cross the Windows boundary.

Do not use production credentials, production mutable data, production trust roots, or unrestricted protected data in this recipe.

## 1. Choose the workspace identity

Use a lowercase component, a lowercase branch or purpose slug, and a unique suffix of four to twelve lowercase alphanumeric characters.

`bash
export COMPONENT=konnaxion
export PURPOSE=feature-voting
export SUFFIX=92cd
export WORKSPACE_ID="${COMPONENT}-${PURPOSE}-${SUFFIX}"
export WORKSPACE_ROOT="$HOME/workspaces/${WORKSPACE_ID}"

printf '%s\n' "${WORKSPACE_ID}"
`

Expected value:

`text
konnaxion-feature-voting-92cd
`

Do not use only the branch name. The stable identifier owns the mutable namespace.

## 2. Create the worktree and Python environment

Save the following script as `scripts/create-python-workspace.sh`, make it executable, and run it from an existing repository checkout.

`bash
#!/usr/bin/env bash
set -euo pipefail

COMPONENT="${COMPONENT:-konnaxion}"
PURPOSE="${PURPOSE:-feature-voting}"
SUFFIX="${SUFFIX:-92cd}"
PYTHON_VERSION="${PYTHON_VERSION:-3.13}"
BASE_REF="${BASE_REF:-main}"
REPOSITORY_ROOT="${REPOSITORY_ROOT:-$(git rev-parse --show-toplevel)}"
WORKSPACES_ROOT="${WORKSPACES_ROOT:-$HOME/workspaces}"

WORKSPACE_ID="${COMPONENT}-${PURPOSE}-${SUFFIX}"
WORKSPACE_ROOT="${WORKSPACES_ROOT}/${WORKSPACE_ID}"

case "${WORKSPACE_ID}" in
 [a-z]*-[a-z0-9]*-[a-z0-9][a-z0-9][a-z0-9][a-z0-9]*) ;;
 *)
 printf 'Invalid workspace identity: %s\n' "${WORKSPACE_ID}" >&2
 exit 1
 ;;
esac

mkdir -p "${WORKSPACES_ROOT}"

if [[ ! -d "${WORKSPACE_ROOT}/.git" && ! -f "${WORKSPACE_ROOT}/.git" ]]; then
 git -C "${REPOSITORY_ROOT}" worktree add \
 -b "${PURPOSE}-${SUFFIX}" \
 "${WORKSPACE_ROOT}" \
 "${BASE_REF}"
fi

cd "${WORKSPACE_ROOT}"

printf '%s\n' "${PYTHON_VERSION}" > .python-version
mkdir -p .workspace/tmp .workspace/logs .workspace/run .koa

if [[ ! -f pyproject.toml ]]; then
 cat > pyproject.toml <<'TOML'
[project]
name = "koa-workspace"
version = "0.1.0"
requires-python = ">=3.13,<3.14"
dependencies = []

[dependency-groups]
dev = [
 "pytest>=8,<9",
 "ruff>=0.12,<1"
]

[tool.pytest.ini_options]
testpaths = ["tests"]
TOML
fi

if [[ ! -f uv.lock ]]; then
 uv lock
fi

uv sync --frozen

printf 'Workspace ready: %s\n' "${WORKSPACE_ID}"
printf 'Root: %s\n' "${WORKSPACE_ROOT}"
printf 'Python: %s\n' "$(uv run python --version)"

`

Run:

`bash
chmod +x scripts/create-python-workspace.sh

COMPONENT=konnaxion \
PURPOSE=feature-voting \
SUFFIX=92cd \
PYTHON_VERSION=3.13 \
BASE_REF=main \
scripts/create-python-workspace.sh
`

The first bootstrap can run `uv lock` because the lockfile does not yet exist. Routine validation uses only `uv sync --frozen`.

When changing dependencies later:

1. edit `pyproject.toml`;
2. refresh `uv.lock` explicitly;
3. review the lockfile;
4. run impact tests;
5. commit the manifest and lockfile together.

## 3. Use the standard workspace layout

Use this local layout:

`text
.
├── .koa/
│ └── developer-workspace.json
├── .python-version
├── .venv/
├── .workspace/
│ ├── logs/
│ ├── run/
│ └── tmp/
├── pyproject.toml
├── uv.lock
├── src/
└── tests/
`

Keep `.venv`, `.workspace/tmp`, and `.workspace/run` outside version control.

A typical `.gitignore` addition is:

`gitignore
.venv/
.workspace/tmp/
.workspace/run/
__pycache__/
.pytest_cache/
.ruff_cache/
`

Log retention is component- and profile-dependent. Do not ignore evidence that the active contract requires to be retained.

## 4. Create the workspace contract

Save this example as `.koa/developer-workspace.json` and replace the example identities and allocations with values reserved for the actual workspace.

`json
{
 "$schema": "docs/schemas/developer-workspace.schema.json",
 "contract_type": "developer_workspace",
 "workspace_id": "konnaxion-feature-voting-92cd",
 "version": "1.0.0",
 "status": "active",
 "profile_id": "developer_linux_workstation",
 "owner": "konnaxion-development",
 "description": "Isolated Python workspace for the Konnaxion feature-voting branch.",
 "created_at": "2026-08-03T19:45:00-04:00",
 "updated_at": "2026-08-03T19:45:00-04:00",
 "identity": {
 "component": "konnaxion",
 "branch_or_purpose": "feature-voting",
 "unique_suffix": "92cd",
 "derivation_template": "{component}-{branch_or_purpose}-{unique_suffix}",
 "namespace_prefix": "konnaxion-feature-voting-92cd",
 "workspace_id_matches_derivation": true,
 "display_name": "Konnaxion feature-voting workspace"
 },
 "source_control": {
 "repository_id": "koa-platform",
 "workspace_kind": "worktree",
 "ref_name": "feature/voting",
 "workspace_root": ".",
 "clean_repository_required_for_validation": true
 },
 "isolation": {
 "dependency_environment": {
 "strategy": "per_workspace",
 "toolchains": [
 "python"
 ],
 "mutable_environment_shared": false,
 "workspace_removal_is_independent": true,
 "python": {
 "manager": "uv",
 "project_file": "pyproject.toml",
 "lock_file": "uv.lock",
 "python_version_file": ".python-version",
 "declared_python_version": "3.13",
 "virtual_environment_path": ".venv",
 "per_workspace_virtual_environment": true,
 "validation_sync_command": "uv sync --frozen",
 "global_application_installation_allowed": false,
 "shared_mutable_virtual_environment_allowed": false,
 "shared_content_addressed_download_cache_allowed": true,
 "lockfile_refresh_requires_explicit_action": true
 }
 },
 "services": {
 "mechanism": "rootless_containers",
 "service_names_prefixed": true,
 "container_names_prefixed": true,
 "shared_mutable_service_identity_allowed": false,
 "services": [
 {
 "service_id": "app",
 "runtime_name": "konnaxion-feature-voting-92cd-app",
 "activation": "manual",
 "stateful": false,
 "internal_ports": [
 8000
 ]
 },
 {
 "service_id": "postgres",
 "runtime_name": "konnaxion-feature-voting-92cd-postgres",
 "activation": "manual",
 "stateful": true,
 "internal_ports": [
 5432
 ]
 }
 ]
 },
 "state": {
 "namespace_prefix": "konnaxion-feature-voting-92cd",
 "namespaced_resources": [
 "dependency_environment",
 "containers",
 "networks",
 "volumes",
 "database_names",
 "database_users",
 "database_schemas",
 "unix_sockets",
 "temporary_directories",
 "log_directories",
 "pid_files",
 "service_names",
 "secret_names",
 "local_certificates",
 "development_queues",
 "host_ports"
 ],
 "shared_mutable_state_allowed": false,
 "workspace_local_directories": {
 "temporary": ".workspace/tmp",
 "logs": ".workspace/logs",
 "runtime": ".workspace/run"
 }
 },
 "databases": {
 "isolation_model": "separate_database",
 "workspace_scoped_database_identity": true,
 "cross_workspace_mutable_sharing_allowed": false,
 "cross_component_direct_writes_allowed": false,
 "databases": [
 {
 "component_id": "konnaxion",
 "database_name": "konnaxion_feature_voting_92cd",
 "database_user": "konnaxion_feature_voting_92cd",
 "schema_name": "konnaxion",
 "connection_secret_ref": "secret://workspace-konnaxion-feature-voting-92cd/postgres-url"
 }
 ]
 },
 "secrets": {
 "namespace_prefix": "konnaxion-feature-voting-92cd",
 "secret_values_embedded": false,
 "cross_workspace_secret_reuse_allowed": false,
 "references": [
 "secret://workspace-konnaxion-feature-voting-92cd/postgres-url",
 "secret://workspace-konnaxion-feature-voting-92cd/app-signing-key"
 ],
 "generated_local_certificates_namespaced": true
 },
 "ports": {
 "host_allocation_strategy": "workspace_scoped_allocation_registry",
 "fixed_internal_ports_allowed": true,
 "host_port_collisions_allowed": false,
 "allocation_registry_ref": "contracts/artifact-contracts/workspace-port-allocation.schema.json",
 "allocations": [
 {
 "service_id": "app",
 "container_port": 8000,
 "host_port": 18092,
 "protocol": "tcp"
 },
 {
 "service_id": "postgres",
 "container_port": 5432,
 "host_port": 15492,
 "protocol": "tcp"
 }
 ]
 },
 "network": {
 "isolated_logical_network": true,
 "network_names_prefixed": true,
 "cross_workspace_default_connectivity": false,
 "network_name": "konnaxion-feature-voting-92cd-net"
 },
 "parallel_execution": {
 "simultaneous_workspaces_supported": true,
 "collision_free": true,
 "collision_domains": [
 "host_ports",
 "process_names",
 "service_names",
 "database_names",
 "database_users",
 "database_schemas",
 "networks",
 "volumes",
 "secrets",
 "sockets",
 "temporary_files",
 "logs"
 ],
 "minimum_concurrent_workspaces": 2
 }
 },
 "resource_budget": {
 "cpu": {
 "maximum_cores": 4,
 "weight": 100
 },
 "memory": {
 "maximum_mb": 4096,
 "swap_maximum_mb": 1024
 },
 "processes": {
 "maximum": 256
 },
 "io": {
 "priority": "normal"
 },
 "queues": {
 "maximum_pending_jobs": 32
 },
 "heavy_jobs": {
 "maximum_concurrent": 1,
 "default_activation": "task_activated",
 "services": [
 "uckk_package_validation_job"
 ]
 }
 },
 "reproducibility": {
 "declared_runtime_versions": true,
 "versioned_project_manifests": true,
 "versioned_lockfiles": true,
 "frozen_validation_sync": true,
 "clean_environment_rebuild_supported": true,
 "dependency_upgrade_requires_impact_and_tests": true,
 "shared_cache_is_not_installed_environment": true,
 "validation_commands": [
 "uv sync --frozen",
 "uv run python -m pytest",
 "uv run ruff check ."
 ]
 },
 "lifecycle": {
 "creation_is_explicit": true,
 "activation_is_explicit": true,
 "teardown_is_explicit": true,
 "removal_does_not_affect_other_workspaces": true,
 "shared_download_cache_may_be_retained": true,
 "orphan_cleanup_required": true,
 "retained_resources": [
 "shared_content_addressed_download_cache"
 ]
 },
 "canonical_refs": [
 "schemas/developer-workspace.schema.json",
 "contracts/toolchains/python-uv.toolchain.json",
 "contracts/artifact-contracts/workspace-port-allocation.schema.json",
 "contracts/artifact-contracts/resource-envelope.schema.json"
 ],
 "decision_ids": [
 "DEC-DEV-001",
 "DEC-DEV-002"
 ],
 "requirement_ids": [
 "REQ-DEV-UV-001",
 "REQ-DEV-UV-002",
 "REQ-DEV-UV-003",
 "REQ-DEV-STATE-001",
 "REQ-DEV-PARALLEL-001"
 ],
 "lock_ids": [
 "LOCK-DEV-001",
 "LOCK-DEV-002",
 "LOCK-DEV-003",
 "LOCK-DEV-004",
 "LOCK-DEV-005"
 ],
 "exception_ids": [],
 "tags": [
 "python",
 "uv",
 "konnaxion",
 "feature-voting"
 ],
 "validation": {
 "required_checks": [
 "workspace_id_derivation",
 "dependency_environment_isolation",
 "workspace_state_namespacing",
 "parallel_workspace_collision_check",
 "reproducible_dependency_sync",
 "resource_budget_validation",
 "secret_reference_validation",
 "independent_teardown_validation"
 ],
 "activation_requires": "pass",
 "results": [
 {
 "check_id": "workspace_id_derivation",
 "result": "pass",
 "message": "Workspace identity matches the declared derivation."
 },
 {
 "check_id": "dependency_environment_isolation",
 "result": "pass",
 "message": "The installed Python environment is workspace-local."
 },
 {
 "check_id": "workspace_state_namespacing",
 "result": "pass",
 "message": "Mutable state uses the workspace namespace."
 },
 {
 "check_id": "parallel_workspace_collision_check",
 "result": "pass",
 "message": "The workspace passed the two-workspace collision test."
 },
 {
 "check_id": "reproducible_dependency_sync",
 "result": "pass",
 "message": "Frozen UV synchronization completed without lock changes."
 },
 {
 "check_id": "resource_budget_validation",
 "result": "pass",
 "message": "The resource envelope is complete and bounded."
 },
 {
 "check_id": "secret_reference_validation",
 "result": "pass",
 "message": "Only workspace-scoped secret references are present."
 },
 {
 "check_id": "independent_teardown_validation",
 "result": "pass",
 "message": "Teardown did not affect the peer workspace."
 }
 ],
 "validated_at": "2026-08-03T19:45:00-04:00",
 "validator_version": "1.0.0"
 }
}
`

Important adjustments:

- set `profile_id` to the actual primary profile;
- allocate host ports through the workspace allocation registry;
- use component-owned database names and users;
- keep secret values outside the JSON document;
- declare only the services used by this workspace;
- select resource limits that fit the workstation and active profile;
- replace validation results with actual results produced for this workspace.

The JSON shown here is a completed example. During creation, a validation result can remain `blocked`; activation occurs only after every required check passes.

## 5. Validate the contract

From the repository root, validate the instance against the canonical schema.

Example with Python and `jsonschema` installed in a dedicated validation environment:

`bash
python - <<'PY'
import json
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

root = Path.cwd
common_path = root / "docs/schemas/common-metadata.schema.json"
schema_path = root / "docs/schemas/developer-workspace.schema.json"
instance_path = root / ".koa/developer-workspace.json"

common = json.loads(common_path.read_text(encoding="utf-8"))
schema = json.loads(schema_path.read_text(encoding="utf-8"))
instance = json.loads(instance_path.read_text(encoding="utf-8"))

registry = (
 Registry
 .with_resource(common["$id"], Resource.from_contents(common))
 .with_resource(schema["$id"], Resource.from_contents(schema))
)

validator = Draft202012Validator(schema, registry=registry)
errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.path))

if errors:
 for error in errors:
 print(f"{list(error.path)}: {error.message}")
 raise SystemExit(1)

print("developer_workspace contract passed JSON Schema validation")
PY
`

Schema validity is necessary but not sufficient. The parallel, resource, secret, teardown, reference, and profile checks remain behavioral.

## 6. Validate frozen Python dependencies

Save as `scripts/validate-python-workspace.sh`:

`bash
#!/usr/bin/env bash
set -euo pipefail

git diff --exit-code -- pyproject.toml uv.lock .python-version
git diff --cached --exit-code -- pyproject.toml uv.lock .python-version

test -f pyproject.toml
test -f uv.lock
test -f .python-version
test -d .venv

uv sync --frozen
uv run python -m pytest
uv run ruff check .

git diff --exit-code -- uv.lock
test "$(realpath .venv)" = "$(realpath "$PWD/.venv")"

printf 'Frozen UV workspace validation passed.\n'

`

Run:

`bash
chmod +x scripts/validate-python-workspace.sh
scripts/validate-python-workspace.sh
`

The command verifies that:

- the required files exist;
- `.venv` belongs to the current workspace;
- frozen synchronization succeeds;
- tests and static checks pass;
- `uv.lock` is unchanged by validation.

A shared UV download cache is compatible with this flow. The installed `.venv` remains local.

## 7. Namespace infrastructure services

Use `WORKSPACE_ID` as the prefix for every mutable runtime object.

Example environment values:

`bash
export APP_SERVICE="${WORKSPACE_ID}-app"
export DB_SERVICE="${WORKSPACE_ID}-postgres"
export NETWORK_NAME="${WORKSPACE_ID}-net"
export DATABASE_NAME="konnaxion_feature_voting_92cd"
export DATABASE_USER="konnaxion_feature_voting_92cd"
export APP_SOCKET="${WORKSPACE_ROOT}/.workspace/run/app.sock"
export APP_LOG_DIR="${WORKSPACE_ROOT}/.workspace/logs"
export APP_TMP_DIR="${WORKSPACE_ROOT}/.workspace/tmp"
`

Fixed internal ports are allowed inside the isolated workspace network:

`text
application: 8000/tcp
PostgreSQL: 5432/tcp
`

Host-exposed ports must be reserved separately:

`text
application: 18092/tcp
PostgreSQL: 15492/tcp
`

Do not derive host ports by an uncoordinated arithmetic convention. Record the actual reservation through the workspace port-allocation contract.

Default cross-workspace connectivity remains disabled. Add a cross-workspace link only through a bounded, attributable, revocable configuration.

## 8. Reference secrets without embedding values

The workspace contract stores references such as:

`text
secret://workspace-konnaxion-feature-voting-92cd/postgres-url
secret://workspace-konnaxion-feature-voting-92cd/app-signing-key
`

Resolve values at activation time through the selected development secret provider.

Do not place secret values in:

- `.koa/developer-workspace.json`;
- `pyproject.toml`;
- `uv.lock`;
- container definitions committed to the repository;
- command history;
- ordinary logs;
- conformance reports.

Generated local certificates use the workspace namespace and are revoked or removed during teardown.

## 9. Run the parallel-workspace check

Create a second workspace with a different purpose and suffix, for example:

`text
konnaxion-main-a31f
konnaxion-feature-voting-92cd
`

Save the following as `scripts/check-parallel-workspaces.sh`:

`bash
#!/usr/bin/env bash
set -euo pipefail

FIRST_ID="${FIRST_ID:-konnaxion-main-a31f}"
SECOND_ID="${SECOND_ID:-konnaxion-feature-voting-92cd}"
FIRST_ROOT="${FIRST_ROOT:-$HOME/workspaces/$FIRST_ID}"
SECOND_ROOT="${SECOND_ROOT:-$HOME/workspaces/$SECOND_ID}"

test "$FIRST_ID" != "$SECOND_ID"
test -d "$FIRST_ROOT/.venv"
test -d "$SECOND_ROOT/.venv"
test "$(realpath "$FIRST_ROOT/.venv")" != "$(realpath "$SECOND_ROOT/.venv")"

FIRST_PORT="${FIRST_PORT:-18031}"
SECOND_PORT="${SECOND_PORT:-18092}"
test "$FIRST_PORT" != "$SECOND_PORT"

FIRST_DB="${FIRST_DB:-konnaxion_main_a31f}"
SECOND_DB="${SECOND_DB:-konnaxion_feature_voting_92cd}"
test "$FIRST_DB" != "$SECOND_DB"

FIRST_NETWORK="${FIRST_NETWORK:-konnaxion-main-a31f-net}"
SECOND_NETWORK="${SECOND_NETWORK:-konnaxion-feature-voting-92cd-net}"
test "$FIRST_NETWORK" != "$SECOND_NETWORK"

FIRST_SOCKET="${FIRST_SOCKET:-$FIRST_ROOT/.workspace/run/app.sock}"
SECOND_SOCKET="${SECOND_SOCKET:-$SECOND_ROOT/.workspace/run/app.sock}"
test "$FIRST_SOCKET" != "$SECOND_SOCKET"

printf 'Parallel namespace checks passed for %s and %s.\n' \
 "$FIRST_ID" "$SECOND_ID"

`

Run:

`bash
chmod +x scripts/check-parallel-workspaces.sh
scripts/check-parallel-workspaces.sh
`

The script verifies basic namespace separation. The complete behavioral test also starts both workspaces and confirms:

- no host-port collision;
- no shared mutable `.venv`;
- no process or service-name collision;
- no database, user, or schema collision;
- no network or volume collision;
- no socket-path collision;
- no secret-reference reuse;
- no temporary-file or log collision;
- no default cross-workspace network path;
- bounded resource use;
- one workspace remains operational when the other is removed.

## 10. Apply resource limits

The example contract limits the workspace to:

`text
CPU: 4 cores
memory: 4096 MiB
swap: 1024 MiB
processes: 256
I/O priority: normal
pending jobs: 32
concurrent heavy jobs: 1
`

Map these values to the active profile's Resource Governor implementation.

Task-activate heavy services and intensive jobs. Do not leave optional search engines, model runtimes, SenTient, or intensive kOA Mediatheque processing and UCKK package-validation or transport jobs running merely because the workstation has spare capacity.

Resource admission does not grant component authorization.

## 11. WSL adjustments

For `developer_windows_wsl`, record:

`text
Windows host version class
WSL distribution and version
Linux workspace path
Windows-visible path, when used
container or service runtime
host-port forwarding behavior
DNS and name-resolution behavior
time behavior
service start and stop behavior
secret boundary
editor or host-tool integration
`

Prefer keeping the mutable Linux workspace, `.venv`, sockets, databases, and service state inside the declared Linux filesystem boundary.

Do not silently attribute a Windows-host service, credential, port, or filesystem behavior to the Linux workspace.

Use either Docker or Podman as selected by the profile. Keep application commands and contracts runtime-independent.

## 12. Teardown independently

Save the following as `scripts/remove-python-workspace.sh`:

`bash
#!/usr/bin/env bash
set -euo pipefail

WORKSPACE_ID="${WORKSPACE_ID:-konnaxion-feature-voting-92cd}"
WORKSPACE_ROOT="${WORKSPACE_ROOT:-$HOME/workspaces/$WORKSPACE_ID}"
REPOSITORY_ROOT="${REPOSITORY_ROOT:-$(git rev-parse --show-toplevel)}"

# Stop only services whose runtime identity begins with WORKSPACE_ID.
# Replace the following command with the selected profile runtime.
if command -v podman >/dev/null 2>&1; then
 podman ps -aq --filter "name=^${WORKSPACE_ID}-" \
 | xargs -r podman rm -f
fi

rm -rf \
 "${WORKSPACE_ROOT}/.venv" \
 "${WORKSPACE_ROOT}/.workspace/tmp" \
 "${WORKSPACE_ROOT}/.workspace/run"

git -C "${REPOSITORY_ROOT}" worktree remove "${WORKSPACE_ROOT}"

printf 'Removed workspace %s.\n' "${WORKSPACE_ID}"
printf 'Shared content-addressed UV downloads were retained.\n'

`

The Podman command is an implementation example. Replace it with the active profile runtime while preserving the workspace prefix and independent lifecycle.

Before removal, also:

- release registered host ports;
- remove workspace databases and users through the database owner;
- revoke generated local credentials;
- delete workspace queues and volumes according to their owner contracts;
- retain required logs or evidence;
- confirm that peer workspaces remain active.

Never use an unscoped cleanup such as deleting every development container, database, network, or volume on the workstation.

## 13. Troubleshooting

### `uv sync --frozen` reports a stale lockfile

The manifest and lockfile differ.

Use an explicit dependency-change workflow:

`bash
uv lock
uv sync --frozen
uv run python -m pytest
uv run ruff check .
git diff -- pyproject.toml uv.lock
`

Commit the reviewed change and its test evidence together.

### `.venv` resolves outside the workspace

Remove the external or shared environment and recreate `.venv` inside the workspace:

`bash
rm -rf .venv
uv sync --frozen
`

### A host port is already in use

Do not change it only in a local shell variable. Release or replace the reservation in the workspace-scoped port-allocation registry, then update the workspace contract.

### Two branches see the same database data

Verify database name, user, schema, connection secret reference, and service runtime name. Separate the mutable database identity before continuing.

### Teardown affects another workspace

Stop the teardown and treat the result as a failed isolation claim. Review every command for an exact `WORKSPACE_ID` prefix and restore the affected peer through its own owner contract.

## 14. Completion checklist

The recipe is complete when:

- [ ] `workspace_id` matches the canonical derivation;
- [ ] `.koa/developer-workspace.json` validates;
- [ ] `pyproject.toml`, `uv.lock`, and `.python-version` are versioned;
- [ ] `.venv` is workspace-local;
- [ ] `uv sync --frozen` does not alter `uv.lock`;
- [ ] services and mutable state use the workspace prefix;
- [ ] host ports are registered and collision-free;
- [ ] the logical network is isolated;
- [ ] database identities are workspace-scoped;
- [ ] secret values remain outside contracts and logs;
- [ ] resource limits are enforced;
- [ ] two workspaces run concurrently;
- [ ] teardown leaves the peer workspace unaffected;
- [ ] release candidates are immutable artifacts rather than copied workspace state.

## Conformance mapping

| Recipe step | Canonical intent |
| --- | --- |
| Stable identity | `DEC-DEV-002`, workspace identity schema |
| One local `.venv` | `DEC-DEV-001`, `LOCK-DEV-001`, `LOCK-DEV-002` |
| Frozen UV sync | Reproducible dependency validation |
| Shared download cache only | `LOCK-DEV-005` |
| Namespaced mutable state | `LOCK-DEV-003` |
| Parallel branch test | `LOCK-DEV-004` |
| Component-owned databases | `LOCK-DATA-001` |
| Resource budget | Resource Governor boundary |
| Runtime choice by profile | `DEC-CONTAINER-001`, `LOCK-IMPL-001`, `LOCK-IMPL-002` |
| Immutable release transition | Artifact and Release Set lifecycle |
