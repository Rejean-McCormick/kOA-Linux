<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "RECIPE-DEV-004",
  "document_class": "non_normative_recipe",
  "status": "active",
  "language": "en",
  "layer": "recipes",
  "scope": [
    "development_toolchain"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/development_model",
    "generated/component-catalog.json",
    "contracts/profiles/developer-linux-workstation.profile.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "contracts/profiles/build-farm.profile.json",
    "contracts/toolchains/python-uv.toolchain.json",
    "contracts/artifact-classes.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-DEV-001",
    "DEC-DEV-PAR-001",
    "DEC-SYS-COMP-001",
    "DEC-SYS-RESOURCE-001"
  ],
  "requirement_ids": [
    "REQ-DEV-PAR-001",
    "REQ-DEV-PAR-002",
    "REQ-DEV-PAR-003",
    "REQ-DEV-PAR-009",
    "REQ-DEV-PAR-010",
    "REQ-DEV-PAR-011",
    "REQ-DEV-PAR-012",
    "REQ-DEV-PAR-013",
    "REQ-DEV-PAR-014",
    "REQ-DEV-PAR-015",
    "REQ-DEV-PAR-016",
    "REQ-DEV-PAR-017",
    "REQ-DEV-PAR-018",
    "REQ-DEV-PAR-019",
    "REQ-DEV-PAR-020",
    "REQ-DEV-PAR-024",
    "REQ-DEV-PAR-028",
    "REQ-DEV-PAR-031",
    "REQ-DEV-PAR-032",
    "REQ-DEV-PAR-033",
    "REQ-DEV-PAR-034",
    "REQ-DEV-PAR-035",
    "REQ-DEV-PAR-037",
    "REQ-DEV-PAR-038",
    "REQ-DEV-PAR-040"
  ],
  "lock_ids": [
    "LOCK-DEV-001",
    "LOCK-DEV-002",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DEV-005",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-OPS-001",
    "LOCK-OPS-002",
    "LOCK-OPS-003"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-DEV-000",
    "DOC-DEV-010",
    "DOC-PROFILE-001",
    "DOC-PROFILE-002",
    "DOC-COMP-001",
    "DOC-SEC-005",
    "DOC-SEC-006"
  ],
  "tags": [
    "recipe",
    "development",
    "database-isolation",
    "postgresql",
    "workspace-isolation",
    "application-instance",
    "rootless-containers",
    "migrations",
    "fixtures",
    "safe-cleanup"
  ]
}
KOA:DOC-META:END -->

# Local Database Isolation

## 1. Purpose

This recipe shows one practical way to give each local kOA component instance its own database boundary.

The worked example uses a rootless PostgreSQL container for each workspace, component, and application instance. The same ownership model applies to another relational database, an embedded database, or a profile-approved shared development server.

This recipe is non-normative. The development model, parallel-application rules, component contracts, profile contracts, and workspace manifest remain authoritative.

The target result is:

`text
one workspace identity
+ one application-instance identity
+ one component identity
+ one database identity
+ one database user
+ one owned volume
+ one allocated loopback port
+ one migration history
`

The database remains disposable development state. It is not a production database, release artifact, evidence store, or substitute for component-owned backup and recovery contracts.

## 2. Use This Recipe When

Use this recipe when:

- two branches or worktrees need to run concurrently;
- one workspace runs multiple instances of the same component;
- integration tests need persistent local state;
- migrations differ across branches;
- a developer needs to reset one component without affecting another;
- a local stack needs reproducible ownership and cleanup;
- database access needs a clear component and workspace boundary.

Do not use this recipe to connect a development branch to:

- a production database;
- a sovereign-node authoritative database;
- a shared integration database without a registered test contract;
- another workspace's mutable database;
- a backup or recovery repository;
- Audit Broker protected evidence storage.

## 3. Prerequisites

The workspace needs:

- an active developer profile;
- a stable `workspace_id`;
- a stable `application_instance_id`;
- the owning `component_id`;
- the exact source revision;
- a workspace manifest;
- a loopback port allocation;
- a rootless container engine or another profile-approved database runtime;
- the component's registered migration command;
- UV and the workspace's committed `uv.lock`.

This recipe uses these local paths:

`text
.koa/
 runtime/
 <application-instance-id>/
 database.env
 database.identity.env
 compose.database.yaml
 migration-state.json
 fixtures/
`

Add this rule to the workspace `.gitignore`:

`gitignore
.koa/runtime/
`

The runtime directory contains mutable state and local credentials. It is not canonical source.

## 4. Choose the Isolation Strategy

Use the strongest practical strategy supported by the profile.

| Strategy | Boundary | Typical use |
| --- | --- | --- |
| Separate database server instance | Process, port, storage, account, and database | Preferred for parallel local work |
| Separate database in a shared server | Database and account | Acceptable when server administration is centralized |
| Separate schema in a shared database | Schema and account | Use only when permissions prevent cross-schema access |
| Separate tenant or engine namespace | Engine-defined logical boundary | Use only with tested isolation |
| Separate embedded database file | File and process ownership | Suitable for components designed for embedded storage |

The worked example uses a separate PostgreSQL server instance in a workspace-owned container.

The isolation boundary is complete only when the following values are distinct:

`text
container project
container name
network
volume
host port
database name
database role
migration history
fixture namespace
`

A different branch name alone does not provide database isolation.

## 5. Derive Stable Local Identities

### 5.1 Set canonical local inputs

Export values already present in the workspace manifest:

`bash
export KOA_WORKSPACE_ID="ws_4d3a8c71"
export KOA_INSTANCE_ID="appinst_orders_01"
export KOA_COMPONENT_ID="orders"
export KOA_SOURCE_REVISION="$(git rev-parse HEAD)"
export KOA_DB_HOST_PORT="55431"
export KOA_POSTGRES_IMAGE="postgres:16.4-bookworm"
`

`KOA_DB_HOST_PORT` comes from the workspace port-allocation record. Allocation occurs before database startup and checks that the loopback port is unused.

The image value is an example for this recipe. An active profile or build workflow can replace it with its approved immutable image identity.

### 5.2 Generate bounded names

PostgreSQL identifiers have practical length limits. Generate short stable names from the three ownership identities rather than using a raw branch name or path.

`bash
mkdir -p ".koa/runtime/${KOA_INSTANCE_ID}"

uv run python - <<'PY' > ".koa/runtime/${KOA_INSTANCE_ID}/database.identity.env"
from __future__ import annotations

import hashlib
import os
import re

workspace = os.environ["KOA_WORKSPACE_ID"]
instance = os.environ["KOA_INSTANCE_ID"]
component = os.environ["KOA_COMPONENT_ID"]

def compact(value: str, limit: int = 12) -> str:
 normalized = re.sub(r"[^a-z0-9]+", "_", value.lower).strip("_")
 digest = hashlib.sha256(value.encode("utf-8")).hexdigest[:8]
 prefix = normalized[:limit].rstrip("_") or "id"
 return f"{prefix}_{digest}"

workspace_key = compact(workspace)
instance_key = compact(instance)
component_key = compact(component)
base = f"koa_{workspace_key}_{component_key}_{instance_key}"

values = {
 "KOA_DB_NAME": base,
 "KOA_DB_USER": f"{base}_rw",
 "KOA_DB_CONTAINER": f"{base}_db",
 "KOA_DB_VOLUME": f"{base}_pgdata",
 "KOA_DB_NETWORK": f"koa_{workspace_key}_net",
 "KOA_CONTAINER_PROJECT": f"koa_{workspace_key}",
}

for key, value in values.items:
 print(f"{key}={value}")
PY
`

Review the generated non-secret identities:

`bash
cat ".koa/runtime/${KOA_INSTANCE_ID}/database.identity.env"
`

Record these identities in the workspace manifest or its generated runtime projection.

### 5.3 Create local credentials

Create credentials with restrictive permissions:

`bash
umask 077

uv run python - <<'PY' > ".koa/runtime/${KOA_INSTANCE_ID}/database.env"
from __future__ import annotations

import secrets

print(f"POSTGRES_PASSWORD={secrets.token_urlsafe(32)}")
PY

chmod 600 ".koa/runtime/${KOA_INSTANCE_ID}/database.env"
`

Do not print the password during normal operation. Do not add the credential file to Git, logs, receipts, screenshots, test evidence, or shell history.

## 6. Provision the Isolated PostgreSQL Instance

### 6.1 Create the compose definition

Create `.koa/runtime/<application-instance-id>/compose.database.yaml`:

`yaml
services:
 database:
 image: ${KOA_POSTGRES_IMAGE}
 container_name: ${KOA_DB_CONTAINER}
 restart: "no"
 environment:
 POSTGRES_DB: ${KOA_DB_NAME}
 POSTGRES_USER: ${KOA_DB_USER}
 POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
 ports:
 - "127.0.0.1:${KOA_DB_HOST_PORT}:5432"
 volumes:
 - database_data:/var/lib/postgresql/data
 networks:
 - workspace
 labels:
 koa.workspace.id: ${KOA_WORKSPACE_ID}
 koa.instance.id: ${KOA_INSTANCE_ID}
 koa.component.id: ${KOA_COMPONENT_ID}
 koa.profile.id: developer
 koa.source.revision: ${KOA_SOURCE_REVISION}
 koa.created.by: local-database-isolation-recipe
 healthcheck:
 test:
 - CMD-SHELL
 - pg_isready -U "$${POSTGRES_USER}" -d "$${POSTGRES_DB}"
 interval: 2s
 timeout: 3s
 retries: 30
 security_opt:
 - no-new-privileges:true

volumes:
 database_data:
 name: ${KOA_DB_VOLUME}
 labels:
 koa.workspace.id: ${KOA_WORKSPACE_ID}
 koa.instance.id: ${KOA_INSTANCE_ID}
 koa.component.id: ${KOA_COMPONENT_ID}

networks:
 workspace:
 name: ${KOA_DB_NETWORK}
 labels:
 koa.workspace.id: ${KOA_WORKSPACE_ID}
 koa.instance.id: ${KOA_INSTANCE_ID}
`

The explicit volume and network names make ownership inspectable. The loopback bind prevents accidental LAN exposure.

### 6.2 Load the runtime environment

Use a subshell so credentials do not remain in the parent shell longer than needed:

`bash
(
 set -a
 . ".koa/runtime/${KOA_INSTANCE_ID}/database.identity.env"
 . ".koa/runtime/${KOA_INSTANCE_ID}/database.env"
 set +a

 podman compose --project-name "${KOA_CONTAINER_PROJECT}" --file ".koa/runtime/${KOA_INSTANCE_ID}/compose.database.yaml" up --detach
)
`

A rootless Docker-compatible environment can use `docker compose` with the same project and file arguments.

### 6.3 Wait for readiness

`bash
(
 set -a
 . ".koa/runtime/${KOA_INSTANCE_ID}/database.identity.env"
 . ".koa/runtime/${KOA_INSTANCE_ID}/database.env"
 set +a

 for attempt in $(seq 1 30); do
 if podman exec "${KOA_DB_CONTAINER}" pg_isready -U "${KOA_DB_USER}" -d "${KOA_DB_NAME}" >/dev/null 2>&1
 then
 exit 0
 fi
 sleep 1
 done

 echo "Database did not become ready." >&2
 exit 1
)
`

Readiness confirms that the isolated server accepts its intended database and role. It does not confirm that migrations or component invariants are valid.

## 7. Connect the Component and Apply Migrations

### 7.1 Build the component environment

Prefer discrete PostgreSQL variables over a logged connection URL:

`bash
export PGHOST="127.0.0.1"
export PGPORT="${KOA_DB_HOST_PORT}"
export PGDATABASE="${KOA_DB_NAME}"
export PGUSER="${KOA_DB_USER}"
export PGPASSWORD="$(sed -n 's/^POSTGRES_PASSWORD=//p' ".koa/runtime/${KOA_INSTANCE_ID}/database.env")"
`

Pass these values through the component's registered local configuration mechanism.

Do not store `PGPASSWORD` in the workspace manifest.

### 7.2 Verify database identity before migration

Before applying migrations, connect and verify the current target:

`bash
uv run python - <<'PY'
from __future__ import annotations

import os
import psycopg

expected_database = os.environ["KOA_DB_NAME"]
expected_user = os.environ["KOA_DB_USER"]

with psycopg.connect(
 host=os.environ["PGHOST"],
 port=int(os.environ["PGPORT"]),
 dbname=os.environ["PGDATABASE"],
 user=os.environ["PGUSER"],
 password=os.environ["PGPASSWORD"],
) as connection:
 with connection.cursor as cursor:
 cursor.execute("select current_database, current_user")
 actual_database, actual_user = cursor.fetchone

if actual_database != expected_database or actual_user != expected_user:
 raise SystemExit(
 f"Target mismatch: database={actual_database!r}, user={actual_user!r}"
 )

print("Database identity verified.")
PY
`

The example uses `psycopg`. A component can use its own registered database driver or migration tool for the same identity check.

### 7.3 Apply the component migration command

Run the component's canonical migration command inside the workspace's UV environment.

For an Alembic-based component, an example is:

`bash
uv run alembic upgrade head
`

For another migration system, use the component contract or development documentation.

Record:

- workspace identity;
- application-instance identity;
- component identity;
- source revision;
- migration-set identity;
- expected prior state;
- resulting state;
- execution time;
- result;
- rollback or forward-repair classification.

A simple local record can be written to:

`text
.koa/runtime/<application-instance-id>/migration-state.json
`

This local record is runtime metadata, not canonical evidence.

### 7.4 Load fixtures

Fixtures use the same component and workspace boundary.

A fixture loader should:

- connect only to the isolated database;
- use deterministic fixture identities;
- label records with test correlation identities where the schema supports them;
- avoid external or production data;
- preserve the source revision and fixture-set identity;
- be safe to replay or explicitly reject replay.

Example:

`bash
uv run python -m orders.tools.load_dev_fixtures --fixture-set minimal-local --workspace "${KOA_WORKSPACE_ID}" --instance "${KOA_INSTANCE_ID}"
`

Use the actual component-owned fixture command. Do not copy another workspace's mutable database as a fixture shortcut.

## 8. Validate Isolation

### 8.1 Inspect ownership

`bash
(
 set -a
 . ".koa/runtime/${KOA_INSTANCE_ID}/database.identity.env"
 set +a

 podman inspect "${KOA_DB_CONTAINER}" | jq '.[0].Config.Labels'
 podman volume inspect "${KOA_DB_VOLUME}" | jq '.[0].Labels'
 podman network inspect "${KOA_DB_NETWORK}" | jq '.[0].Labels'
)
`

The labels should match the current workspace, component, and application instance.

### 8.2 Confirm loopback binding

`bash
ss -ltn | grep -F "127.0.0.1:${KOA_DB_HOST_PORT}"
`

The listener should not appear on `0.0.0.0`, the LAN address, or an undeclared interface.

### 8.3 Run the two-workspace test

Start two workspaces or instances with distinct identities and allocations.

Verify that they have different:

- container projects;
- container names;
- volumes;
- ports;
- database names;
- database users;
- migration histories.

Write a sentinel record in workspace A. Confirm it is absent in workspace B.

Then attempt to connect with workspace A's role to workspace B's database. The attempt should fail because the role is not present or lacks access in the other server.

### 8.4 Test collision handling

Reserve a port for workspace A, then attempt to allocate the same port to workspace B.

The allocator should reject workspace B before startup.

Do not stop or reconfigure workspace A to make the second startup pass.

### 8.5 Test migration divergence

Create two branches with different migration graphs.

Run each branch against its own database.

After merge or rebase, recreate or explicitly reconcile the receiving workspace database and rerun the complete migration graph from the resulting source revision.

A successful migration in one branch does not validate another branch's database state.

### 8.6 Run component and contract tests

Run the component's registered tests, for example:

`bash
uv run pytest tests/component/orders
uv run pytest tests/contracts/orders
uv run python docs/tools/validate_docs.py
`

Use the actual test paths registered for the component.

Test evidence identifies the workspace, source revision, profile, component, database identity, migration state, and dependency lock.

## 9. Common Development Workflows

### 9.1 Branch switch in the same workspace

Before switching:

1. stop the component;
2. record the current source revision and migration state;
3. preserve required local evidence;
4. switch source;
5. run `uv sync --frozen`;
6. compare the migration graph;
7. recreate or reconcile the database when compatibility changed;
8. restart;
9. rerun affected tests.

A branch switch does not make the old database compatible with the new source automatically.

### 9.2 Parallel worktrees

Each worktree gets:

`text
distinct workspace_id
distinct application_instance_id
distinct port
distinct database name
distinct database user
distinct volume
distinct migration history
`

The image cache can be shared when the image identity is immutable and compatible. The mutable data volume cannot be shared.

### 9.3 Multiple component instances

Two instances of the same component in one workspace use distinct `application_instance_id` values.

They can share immutable source and image layers. They use separate database, role, volume, port, and migration state.

### 9.4 Rebuild after merge or rebase

Recreate the database when:

- migration history was rewritten;
- an earlier migration changed;
- schema ownership changed;
- fixture semantics changed materially;
- the active component contract changed the storage boundary;
- the receiving state cannot prove compatibility.

A local development database is disposable. Prefer a clean rebuild over ambiguous reconciliation.

### 9.5 Intentional data exchange

Use a declared fixture, export artifact, or test contract.

The exchange records:

- source workspace and revision;
- destination workspace and revision;
- selected data class;
- purpose;
- schema;
- integrity where functionally required;
- acceptance;
- cleanup.

Do not grant one workspace direct access to another workspace's database.

## 10. Safe Reset, Cleanup, and Recovery

### 10.1 Stop without deleting data

`bash
(
 set -a
 . ".koa/runtime/${KOA_INSTANCE_ID}/database.identity.env"
 . ".koa/runtime/${KOA_INSTANCE_ID}/database.env"
 set +a

 podman compose --project-name "${KOA_CONTAINER_PROJECT}" --file ".koa/runtime/${KOA_INSTANCE_ID}/compose.database.yaml" stop
)
`

### 10.2 Recreate one isolated database

First verify that the recorded identities match the current workspace and component.

Then:

`bash
(
 set -a
 . ".koa/runtime/${KOA_INSTANCE_ID}/database.identity.env"
 . ".koa/runtime/${KOA_INSTANCE_ID}/database.env"
 set +a

 podman compose --project-name "${KOA_CONTAINER_PROJECT}" --file ".koa/runtime/${KOA_INSTANCE_ID}/compose.database.yaml" down

 podman volume inspect "${KOA_DB_VOLUME}" | jq -r '.[0].Labels["koa.workspace.id"]' | grep -Fx "${KOA_WORKSPACE_ID}"

 podman volume inspect "${KOA_DB_VOLUME}" | jq -r '.[0].Labels["koa.component.id"]' | grep -Fx "${KOA_COMPONENT_ID}"

 podman volume rm "${KOA_DB_VOLUME}"

 podman compose --project-name "${KOA_CONTAINER_PROJECT}" --file ".koa/runtime/${KOA_INSTANCE_ID}/compose.database.yaml" up --detach
)
`

The positive label checks occur before deletion.

Do not use a global volume prune or a wildcard deletion.

### 10.3 Retire the instance

Before retirement:

1. stop new component work;
2. complete or cancel tests;
3. preserve required candidate artifacts and evidence;
4. record whether local data is discarded or exported;
5. stop the owned container;
6. verify ownership labels;
7. remove the owned container, volume, and network when no other owned instance uses it;
8. release the port allocation;
9. remove local credential files;
10. archive or remove the instance record according to workspace policy.

### 10.4 Recover after host or container failure

After a crash:

1. load the workspace manifest;
2. inspect the owned container, volume, network, and port;
3. verify source revision and migration compatibility;
4. determine whether the database stopped cleanly;
5. start the same owned instance or recreate it;
6. run database consistency and component invariant checks;
7. reconcile incomplete tests and operations;
8. create new evidence for the recovered state.

Do not attach the volume to a different branch or component merely because it exists.

### 10.5 Troubleshooting matrix

| Symptom | Likely cause | Safe response |
| --- | --- | --- |
| Port already in use | Allocation collision or stale owned process | Inspect the manifest and owner; allocate another port or stop only the positively matched owned process |
| Migration fails after rebase | Migration graph changed | Recreate the isolated database or run the component's explicit reconciliation path |
| Records appear from another branch | Shared database, schema, volume, or fixture namespace | Stop both instances, inspect identities, separate mutable resources, rebuild databases |
| Role can access another workspace | Shared server permissions too broad | Revoke access, create per-workspace roles, test negative access |
| Database starts with unexpected data | Reused or misnamed volume | Inspect labels, quarantine the volume, create a correctly named owned volume |
| Cleanup would remove multiple workspaces | Broad project or volume selection | Cancel cleanup and select resources by exact manifest identity and labels |
| Test passes only when another stack runs | Hidden shared dependency | Isolate the dependency and rerun with workspace-scoped data |
| Database connection appears in logs | Credential-bearing URL logging | Switch to managed discrete settings and redact connection configuration |
| Container is rootful | Runtime does not match the profile | Stop it and reprovision with the profile-approved rootless runtime |
| Source switched but state was retained | Compatibility was assumed | Reconcile or recreate the database and rerun migrations and tests |

## 11. Completion Checklist

The recipe is complete for one local component instance when:

- [ ] the workspace manifest contains the workspace, component, instance, database, volume, network, and port identities;
- [ ] the database listens only on the allocated loopback port;
- [ ] the container, volume, and network carry matching ownership labels;
- [ ] the database and role names are unique to the workspace, component, and instance;
- [ ] credentials are local, mode-restricted, ignored by Git, and absent from logs;
- [ ] the component verifies its database target before migration;
- [ ] migration state matches the current source revision;
- [ ] fixtures are workspace-scoped and replay-safe or explicitly single-use;
- [ ] another workspace cannot read or mutate the database;
- [ ] port collisions fail before startup;
- [ ] a branch switch or rebase triggers migration compatibility review;
- [ ] tests and evidence identify the exact workspace and database boundary;
- [ ] reset and cleanup use exact identities and positive label checks;
- [ ] no global container, network, or volume prune is part of the normal workflow;
- [ ] removing the database does not affect another workspace or component;
- [ ] the local database is not represented as production or release state.
