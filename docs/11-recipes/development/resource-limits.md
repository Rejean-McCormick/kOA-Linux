<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-RECIPE-DEV-RESOURCE-LIMITS",
  "document_class": "recipe",
  "status": "active",
  "language": "en",
  "layer": "implementation_recipe",
  "scope": [
    "developer_linux_workstation",
    "developer_windows_wsl"
  ],
  "authority": "non_normative",
  "adopted_by_profile_ids": [],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "generated/document-index.json",
    "contracts/system.contract.json#/resource_governor",
    "generated/component-catalog.json",
    "contracts/components/resource-governor.component.json",
    "generated/profile-catalog.json",
    "contracts/profiles/developer-linux-workstation.profile.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "contracts/artifact-contracts/resource-envelope.schema.json",
    "contracts/examples/resource-envelope.example.json",
    "08-operations/04-resource-envelopes.md",
    "05-development/01-development-profile-boundaries.md",
    "05-development/02-workspace-identity.md",
    "05-development/03-workspace-isolation.md",
    "05-development/06-service-containers.md",
    "05-development/12-development-resource-governance.md",
    "05-development/14-build-test-and-validation.md",
    "10-adrs/ADR-005-rootless-podman-and-quadlet.md",
    "10-adrs/ADR-015-development-workspace-isolation-with-uv.md",
    "10-adrs/ADR-019-resource-governor-and-policy-runtime-separation.md"
  ],
  "decision_ids": [
    "DEC-DEV-001",
    "DEC-DEV-002",
    "DEC-GOV-001",
    "DEC-HW-001",
    "DEC-PROFILE-001",
    "DEC-CONTAINER-001",
    "DEC-PRIV-001",
    "DEC-SEC-001",
    "DEC-OFFLINE-001",
    "DEC-LIFE-001"
  ],
  "requirement_ids": [],
  "related_requirement_ids": [
    "REQ-OPS-RESOURCE-003",
    "REQ-OPS-RESOURCE-004",
    "REQ-OPS-RESOURCE-005",
    "REQ-OPS-RESOURCE-008",
    "REQ-OPS-RESOURCE-009",
    "REQ-OPS-RESOURCE-010",
    "REQ-OPS-RESOURCE-011",
    "REQ-OPS-RESOURCE-012",
    "REQ-OPS-RESOURCE-013",
    "REQ-OPS-RESOURCE-015",
    "REQ-OPS-RESOURCE-017",
    "REQ-OPS-RESOURCE-019",
    "REQ-OPS-RESOURCE-020",
    "REQ-OPS-RESOURCE-022",
    "REQ-OPS-RESOURCE-023",
    "REQ-OPS-RESOURCE-024",
    "REQ-OPS-RESOURCE-026",
    "REQ-OPS-RESOURCE-027",
    "REQ-OPS-RESOURCE-029",
    "REQ-OPS-RESOURCE-030",
    "REQ-OPS-RESOURCE-031",
    "REQ-OPS-RESOURCE-032"
  ],
  "lock_ids": [
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-GOV-001",
    "LOCK-COMP-001",
    "LOCK-DATA-001",
    "LOCK-SEC-001",
    "LOCK-SEC-002",
    "LOCK-OFFLINE-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-REL-001",
    "LOCK-REL-002",
    "LOCK-PORT-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-OPS-004",
    "DOC-DEV-001",
    "DOC-DEV-002",
    "DOC-DEV-003",
    "DOC-DEV-008",
    "DOC-DEV-014",
    "DOC-ADR-005",
    "DOC-ADR-015",
    "DOC-ADR-019",
    "DOC-DEV-005",
    "DOC-DEV-006",
    "DOC-DEV-012"
  ],
  "tags": [
    "recipe",
    "development",
    "resource-limits",
    "systemd",
    "cgroups-v2",
    "rootless-podman",
    "cpu",
    "memory",
    "io",
    "tasks",
    "temporary-storage",
    "concurrency",
    "pressure",
    "workspace-isolation"
  ]
}
KOA:DOC-META:END -->

# Development Resource Limits

> **Non-normative recipe.** This file demonstrates one implementation approach. It has no independent authority and is not adopted by any profile in its metadata. The active profile, Resource Governor contract, resource-envelope artifact, and operations documentation control actual limits.

## 1. Purpose

This recipe shows how a developer can place local workspace processes and rootless service containers inside explicit CPU, memory, process, I/O, temporary-storage, and concurrency bounds.

The examples are designed to:

- keep the editor, terminal, browser, and active user session responsive;
- prevent one build, test suite, database, media job, or indexing task from consuming the entire host;
- make limits visible and reproducible;
- isolate workspaces from one another;
- preserve a clear distinction between policy authorization and resource capacity;
- stop idle task workers instead of keeping maximum capacity resident;
- provide evidence that the chosen limits were applied.

The commands use common Linux mechanisms:

- systemd user scopes;
- cgroups v2;
- rootless Podman;
- bounded temporary filesystems;
- explicit workspace concurrency locks;
- operating-system pressure information.

Equivalent implementations are acceptable when they preserve the active contracts.

## 2. Scope and Non-Normative Status

This recipe targets:

- `developer_linux_workstation`;
- `developer_windows_wsl` when systemd and the required cgroup controllers are available;
- local commands launched from one development workspace;
- rootless service containers owned by that workspace;
- bounded build, test, migration, indexing, and media-processing jobs.

It does not define:

- the canonical resource envelope;
- profile minimum hardware;
- production or sovereign-node limits;
- business authorization;
- governance policy;
- component data ownership;
- host privilege;
- artifact activation;
- a Kubernetes requirement;
- global systemd, Podman, or WSL configuration.

The numeric values below are examples for a moderately provisioned developer machine. Copying them into another target does not make them valid for that target.

A profile can adopt a specific command or value only through its canonical profile and resource-envelope contracts. Until then, this file remains implementation guidance.

## 3. Canonical References

Read these sources before selecting limits:

| Source | Use |
| --- | --- |
| `08-operations/04-resource-envelopes.md` | Declared, observed, and effective resource-state model |
| `contracts/components/resource-governor.component.json` | Admission, queue, worker, pressure, and receipt contracts |
| `contracts/profiles/developer-linux-workstation.profile.json` | Linux development profile assumptions |
| `contracts/profiles/developer-windows-wsl.profile.json` | WSL development profile assumptions |
| `contracts/artifact-contracts/resource-envelope.schema.json` | Machine-readable resource-envelope structure |
| `contracts/examples/resource-envelope.example.json` | Complete example of bounded classes, workers, queues, and pressure behavior |
| `05-development/01-development-profile-boundaries.md` | Development authority and profile boundaries |
| `05-development/02-workspace-identity.md` | Workspace identity and naming |
| `05-development/03-workspace-isolation.md` | Workspace, worktree, environment, and state isolation |
| `05-development/06-service-containers.md` | Rootless development service-container boundaries |
| `05-development/12-development-resource-governance.md` | Development-specific resource classes, limits, workers, and pressure behavior |
| `05-development/14-build-test-and-validation.md` | Build, test, and validation workflow |
| `10-adrs/ADR-005-rootless-podman-and-quadlet.md` | Rootless container decision |
| `10-adrs/ADR-015-development-workspace-isolation-with-uv.md` | Workspace isolation decision |
| `10-adrs/ADR-019-resource-governor-and-policy-runtime-separation.md` | Capacity and policy-authority separation |

The Resource Governor decides whether resources are available.

Governance Policy Runtime can separately decide whether a governed action is authorized.

The owning component validates and applies its operation.

This recipe does not merge those decisions.

## 4. Choose a Workspace Budget

### 4.1 Inspect the host

Run the inspection from the development workspace:

```bash
printf 'workspace=%s\n' "$(basename "$PWD")"
printf 'user=%s uid=%s\n' "$USER" "$(id -u)"
printf 'logical_cpus=%s\n' "$(nproc)"
free -m
df -h .
printf '\nCPU pressure\n'
cat /proc/pressure/cpu
printf '\nMemory pressure\n'
cat /proc/pressure/memory
printf '\nI/O pressure\n'
cat /proc/pressure/io
```

For a cgroups v2 target:

```bash
stat -fc %T /sys/fs/cgroup
```

An expected result is:

```text
cgroup2fs
```

For systemd user scopes:

```bash
systemctl --user is-system-running
systemd-run --user --scope --quiet true
```

For rootless Podman:

```bash
podman info --format 'rootless={.Host.Security.Rootless} cgroup={.Host.CgroupsVersion}'
```

The exact output varies by host.

### 4.2 Preserve an interactive reserve

Start from the active profile and reserve enough capacity for:

- editor and language tools;
- terminal and shell;
- browser or local application shell;
- active databases needed for the current task;
- critical local services;
- evidence and logs;
- recovery and cleanup.

Do not allocate every CPU and all physical memory to workspace jobs.

On a 32-GiB example workstation, a reasonable candidate planning envelope can reserve 8 GiB for the active user session and platform, leaving at most 24 GiB for all development workloads. This is only a planning example.

### 4.3 Define resource classes

A practical development mapping is:

| Class | Example work |
| --- | --- |
| `interactive` | Editor helper, local CLI request, active preview |
| `critical_service` | Workspace identity helper, Resource Governor adapter, required database |
| `service` | Ordinary local API or component runtime |
| `build` | Compilation, package build, full static analysis |
| `heavy_compute` | Media conversion, large test corpus, restore validation |
| `background` | Indexing, synchronization, derived previews |

The class is metadata for applying the correct candidate limit. It is not business authority.

### 4.4 Example budget file

Create a workspace-local, non-secret planning file:

```bash
mkdir -p .koa/dev

cat > .koa/dev/resource-limits.env <<'EOF'
KOA_WORKSPACE_ID=workspace-alpha
KOA_CPU_QUOTA=200%
KOA_CPU_WEIGHT=200
KOA_MEMORY_HIGH=4G
KOA_MEMORY_MAX=6G
KOA_TASKS_MAX=512
KOA_IO_WEIGHT=200
KOA_TMP_MAX=2G
KOA_HEAVY_CONCURRENCY=1
EOF
```

Keep this file out of generated product artifacts unless its contract explicitly includes it.

Do not put credentials or governed payloads in the file.

## 5. Local Processes with systemd User Scopes

### 5.1 Launch an ordinary bounded command

Load the candidate values:

```bash
set -a
. .koa/dev/resource-limits.env
set +a
```

Run a test command in a transient user scope:

```bash
systemd-run   --user   --scope   --unit="koa-dev-${KOA_WORKSPACE_ID}-test"   --property="CPUQuota=${KOA_CPU_QUOTA}"   --property="CPUWeight=${KOA_CPU_WEIGHT}"   --property="MemoryHigh=${KOA_MEMORY_HIGH}"   --property="MemoryMax=${KOA_MEMORY_MAX}"   --property="TasksMax=${KOA_TASKS_MAX}"   --property="IOWeight=${KOA_IO_WEIGHT}"   bash -lc 'exec uv run pytest -q'
```

`MemoryHigh` provides pressure before the hard ceiling.

`MemoryMax` is the hard cgroup limit.

`TasksMax` bounds processes and threads.

`CPUQuota` bounds CPU time across logical processors.

`CPUWeight` and `IOWeight` influence relative treatment under contention.

### 5.2 Launch a bounded build

Use a distinct unit identity:

```bash
systemd-run   --user   --scope   --unit="koa-dev-${KOA_WORKSPACE_ID}-build"   --property="CPUQuota=300%"   --property="CPUWeight=150"   --property="MemoryHigh=6G"   --property="MemoryMax=8G"   --property="TasksMax=768"   --property="IOWeight=150"   bash -lc 'exec uv build'
```

The example allows up to three logical CPUs but keeps the job below full-host capacity.

### 5.3 Launch a single heavy job

Use a workspace-scoped lock to avoid accidental parallel heavy jobs:

```bash
lock_file="${XDG_RUNTIME_DIR}/koa-${KOA_WORKSPACE_ID}-heavy.lock"

flock --nonblock "$lock_file"   systemd-run     --user     --scope     --unit="koa-dev-${KOA_WORKSPACE_ID}-heavy"     --property="CPUQuota=400%"     --property="CPUWeight=100"     --property="MemoryHigh=8G"     --property="MemoryMax=10G"     --property="TasksMax=1024"     --property="IOWeight=100"     bash -lc 'exec ./scripts/run-heavy-validation.sh'
```

The example lock protects one workspace. A host-wide development coordinator can use a broader lock or Resource Governor queue when several workspaces share the same heavy-job pool.

### 5.4 Stop and inspect a scope

Inspect:

```bash
systemctl --user status "koa-dev-${KOA_WORKSPACE_ID}-test.scope"
systemctl --user show   "koa-dev-${KOA_WORKSPACE_ID}-test.scope"   --property=ActiveState   --property=SubState   --property=Result   --property=CPUQuotaPerSecUSec   --property=CPUWeight   --property=MemoryHigh   --property=MemoryMax   --property=TasksMax   --property=IOWeight
```

Stop a stuck candidate job:

```bash
systemctl --user stop "koa-dev-${KOA_WORKSPACE_ID}-test.scope"
```

A stopped process is not automatically a completed component operation. Check the owning tool's result and cleanup state.

### 5.5 Handle unavailable controllers

Some user sessions or WSL configurations do not delegate every cgroup controller.

Check the properties actually applied:

```bash
systemctl --user show   "koa-dev-${KOA_WORKSPACE_ID}-test.scope"   --property=ControlGroup   --property=MemoryAccounting   --property=CPUAccounting   --property=IOAccounting   --property=TasksAccounting
```

When a required controller is unavailable:

1. record the limitation;
2. use a supported outer limit such as rootless container limits or the WSL VM ceiling;
3. reduce concurrency;
4. keep the result non-conformant for any claim that requires the missing controller;
5. do not report an unapplied setting as enforced.

## 6. Rootless Service Containers

### 6.1 Use one container identity per workspace

Choose deterministic names:

```bash
workspace_id=workspace-alpha
database_name="koa-dev-${workspace_id}-database"
network_name="koa-dev-${workspace_id}"
volume_name="koa-dev-${workspace_id}-database-data"
image_ref="localhost/koa-dev-database:validated-example"
```

Create an isolated rootless network and volume:

```bash
podman network create "$network_name"
podman volume create "$volume_name"
```

### 6.2 Launch a bounded service

```bash
podman run   --detach   --replace   --name "$database_name"   --network "$network_name"   --cpus 2   --memory 3g   --memory-swap 3g   --pids-limit 256   --blkio-weight 200   --read-only   --tmpfs /tmp:rw,size=512m,mode=1777   --volume "${volume_name}:/var/lib/koa-data:Z"   --label "koa.workspace=${workspace_id}"   --label "koa.resource-class=service"   "$image_ref"
```

The example:

- uses rootless Podman;
- bounds CPU, memory, tasks, and I/O weight;
- avoids additional disk-backed swap for the container;
- keeps the container root filesystem read-only;
- bounds temporary storage;
- uses one workspace-owned data volume;
- labels the workspace and resource class.

The image reference is illustrative. Use the exact validated image identity required by the active toolchain and local-container contract.

### 6.3 Inspect limits and use

```bash
podman inspect "$database_name"   --format 'cpus={.HostConfig.NanoCpus} memory={.HostConfig.Memory} pids={.HostConfig.PidsLimit}'

podman stats   --no-stream   --format 'name={.Name} cpu={.CPU} memory={.MemUsage} pids={.PIDs}'   "$database_name"
```

Inspect the bounded temporary filesystem:

```bash
podman exec "$database_name" df -h /tmp
```

### 6.4 Stop idle services

```bash
podman stop --time 20 "$database_name"
```

Remove the container after the workspace no longer needs it:

```bash
podman rm "$database_name"
```

Retain or remove the data volume according to the workspace and component-data contract:

```bash
podman volume inspect "$volume_name"
```

Do not remove a volume merely because its container is stopped.

### 6.5 Use Quadlet when the profile adopts it

A rootless Quadlet file can express the same limits for a persistent developer service.

Example user unit path:

```text
~/.config/containers/systemd/koa-dev-workspace-alpha-database.container
```

Example content:

```ini
[Unit]
Description=kOA example bounded development database

[Container]
ContainerName=koa-dev-workspace-alpha-database
Image=localhost/koa-dev-database:validated-example
Network=koa-dev-workspace-alpha.network
Volume=koa-dev-workspace-alpha-database-data.volume:/var/lib/koa-data:Z
ReadOnly=true
Tmpfs=/tmp:rw,size=512m,mode=1777
PodmanArgs=--cpus=2
PodmanArgs=--memory=3g
PodmanArgs=--memory-swap=3g
PodmanArgs=--pids-limit=256
PodmanArgs=--blkio-weight=200
Label=koa.workspace=workspace-alpha
Label=koa.resource-class=service

[Service]
Restart=no
TimeoutStopSec=30

[Install]
WantedBy=default.target
```

Reload and inspect:

```bash
systemctl --user daemon-reload
systemctl --user start koa-dev-workspace-alpha-database.service
systemctl --user status koa-dev-workspace-alpha-database.service
```

A Quadlet example remains a recipe until a profile explicitly adopts it.

## 7. Temporary Storage, Queues, and Concurrency

### 7.1 Bound temporary storage

Prefer a bounded temporary directory per job:

```bash
runtime_root="${XDG_RUNTIME_DIR}/koa-${KOA_WORKSPACE_ID}"
mkdir -p "$runtime_root"

systemd-run   --user   --scope   --unit="koa-dev-${KOA_WORKSPACE_ID}-temporary-job"   --property="MemoryMax=2G"   --property="TasksMax=256"   bash -lc '
    export TMPDIR="${XDG_RUNTIME_DIR}/koa-workspace-alpha"
    exec uv run python scripts/create-derived-preview.py
  '
```

For containers, use `--tmpfs` with an explicit size.

Do not place authoritative component data in an ephemeral temporary directory.

### 7.2 Bound work queues

A workspace queue record can use a small JSON file or local database owned by the workspace tool.

Example planning record:

```json
{
  "queue_id": "queue.workspace-alpha.heavy",
  "resource_class": "heavy_compute",
  "maximum_items": 4,
  "maximum_age_seconds": 86400,
  "concurrency": 1,
  "overflow_behavior": "reject_new_with_existing_job_reference"
}
```

The queue implementation should expose:

- queued item count;
- oldest item age;
- running item;
- cancellation;
- result;
- overflow reason.

The record is an implementation example, not a canonical queue contract.

### 7.3 Serialize heavy commands

A reusable helper:

```bash
#!/usr/bin/env bash
set -euo pipefail

workspace_id=${KOA_WORKSPACE_ID:-workspace-alpha}
lock_file="${XDG_RUNTIME_DIR}/koa-${workspace_id}-heavy.lock"

exec flock --nonblock "$lock_file" "$@"
```

Save it as:

```text
scripts/run-one-heavy-job
```

Example use:

```bash
scripts/run-one-heavy-job   systemd-run     --user     --scope     --unit="koa-dev-workspace-alpha-restore-validation"     --property="CPUQuota=400%"     --property="MemoryHigh=8G"     --property="MemoryMax=10G"     --property="TasksMax=1024"     bash -lc 'exec uv run python scripts/validate-restore.py'
```

### 7.4 Stop idle workers

Workers started for indexing, previews, extraction, or test shards should exit when their queue is empty.

For a transient systemd scope, process exit removes the scope.

For a container, use a one-shot process or explicit idle timeout rather than a permanently sleeping worker.

### 7.5 Avoid duplicate effects

Give every queued job a stable job identity and store its last result.

A repeated submission can return the existing job reference rather than create a second build, migration, backup, or media conversion.

## 8. WSL and Cross-Platform Notes

### 8.1 Use the WSL VM as an outer envelope

A Windows WSL installation can define an outer VM ceiling in the user's Windows configuration.

Illustrative configuration:

```ini
[wsl2]
memory=16GB
processors=8
swap=4GB
```

This bounds the entire WSL virtual machine, not one workspace.

Inside WSL, continue to use per-process or per-container limits when supported.

### 8.2 Confirm systemd and cgroup behavior

Inside WSL:

```bash
ps -p 1 -o comm=
stat -fc %T /sys/fs/cgroup
systemctl --user is-system-running
```

When systemd user scopes are unavailable, prefer:

- rootless Podman limits;
- tool-specific worker counts;
- build-system concurrency;
- one-heavy-job serialization;
- explicit temporary-storage limits;
- the outer WSL VM ceiling.

Record which controls are enforced and which are only requested.

### 8.3 Bound common build tools

Examples:

```bash
export CARGO_BUILD_JOBS=4
export MAKEFLAGS=-j4
export NINJAFLAGS=-j4
export UV_CONCURRENT_DOWNLOADS=4
export UV_CONCURRENT_BUILDS=2
```

These tool-level controls complement the outer cgroup or container envelope.

They do not replace memory, process, storage, or I/O limits.

### 8.4 Keep workspace identities portable

Use the same workspace identifier in:

- worktree metadata;
- virtual-environment path;
- container names;
- network names;
- volume names;
- scope units;
- queue IDs;
- port allocations;
- evidence records.

Avoid embedding host-specific absolute paths in portable workspace records.

## 9. Validation and Observability

### 9.1 Capture the candidate configuration

Record:

```bash
cat .koa/dev/resource-limits.env
systemctl --user --version
podman --version
stat -fc %T /sys/fs/cgroup
```

Do not include credentials, tokens, private keys, or governed payloads in the evidence.

### 9.2 Validate a systemd scope

Launch a harmless short command:

```bash
systemd-run   --user   --scope   --unit=koa-dev-resource-limit-check   --property=CPUQuota=50%   --property=MemoryHigh=128M   --property=MemoryMax=256M   --property=TasksMax=64   --property=IOWeight=100   bash -lc 'sleep 5'
```

While it runs:

```bash
systemctl --user show   koa-dev-resource-limit-check.scope   --property=ControlGroup   --property=CPUQuotaPerSecUSec   --property=MemoryHigh   --property=MemoryMax   --property=TasksMax   --property=IOWeight   --property=ActiveState
```

The expected evidence shows the requested values or clearly reports an unsupported property.

### 9.3 Validate a container

For the running example service:

```bash
podman inspect "$database_name"
podman stats --no-stream "$database_name"
podman top "$database_name" pid hpid pcpu pmem comm
```

Validate:

- rootless execution;
- expected container identity;
- expected network and volume;
- CPU and memory limits;
- task limit;
- bounded temporary filesystem;
- read-only root filesystem;
- workspace labels.

### 9.4 Observe host pressure

```bash
watch -n 2 '
  echo "CPU"
  cat /proc/pressure/cpu
  echo
  echo "MEMORY"
  cat /proc/pressure/memory
  echo
  echo "IO"
  cat /proc/pressure/io
'
```

Pressure information helps determine whether effective limits should be narrowed or work deferred.

It does not increase the declared envelope.

### 9.5 Validation checklist

| Check | Expected result |
| --- | --- |
| Workspace identity is explicit | One deterministic workspace ID |
| User scope or container is rootless | No general host-root requirement |
| CPU limit is visible | Requested ceiling is applied or limitation is recorded |
| Memory high and hard limits are visible | Pressure and hard ceiling are distinct |
| Tasks are bounded | Process or thread explosion is contained |
| Temporary storage is bounded | Job cannot fill unrestricted temporary space |
| Heavy concurrency is bounded | Only the intended number of heavy jobs run |
| Queue is bounded | Overflow has an explicit result |
| Idle workers stop | No permanent idle heavy worker |
| Interactive reserve remains | Editor and active session remain usable |
| Pressure is observable | CPU, memory, and I/O states are visible |
| Cleanup is complete | Scope, container, mount, and temporary files are removed |
| No authority collision exists | Resource limits do not grant business or data authority |
| Evidence is minimized | No secret or governed payload is captured |

### 9.6 Suggested evidence record

```json
{
  "evidence_id": "evidence.workspace-alpha.resource-limits.2026-08-03",
  "workspace_id": "workspace-alpha",
  "profile_id": "developer_linux_workstation",
  "mechanisms": [
    "systemd_user_scope",
    "cgroups_v2",
    "rootless_podman",
    "workspace_concurrency_lock"
  ],
  "checks": [
    "cpu_limit_visible",
    "memory_limits_visible",
    "tasks_limit_visible",
    "temporary_storage_bounded",
    "heavy_concurrency_bounded",
    "cleanup_complete"
  ],
  "result": "pass"
}
```

This example records implementation evidence only. It does not create a profile conformance claim.

## 10. Failure Handling, Cleanup, and Prohibited Assumptions

### 10.1 Common failures

| Condition | Response |
| --- | --- |
| systemd user scope cannot start | Use a supported container or tool-level outer limit and record the missing control |
| cgroups v2 is unavailable | Do not claim cgroup enforcement; use the active profile's supported mechanism |
| memory ceiling terminates a job | Preserve the owning tool's failure result, reduce concurrency or data size, and retry through a new job identity |
| task ceiling is reached | Investigate worker or thread count before raising the candidate limit |
| I/O control is unavailable | Reduce concurrency and use bounded temporary storage; record that I/O weight was not enforced |
| rootless container cannot apply a limit | Stop the service and repair the runtime or choose a supported mechanism |
| heavy-job lock is held | Return the existing job reference or defer the new job |
| pressure becomes critical | Pause or stop background and heavy work before interactive and critical services |
| temporary storage fills | Stop the affected job, preserve attributable failure evidence, and clean its temporary state |
| workspace cleanup is incomplete | Keep the workspace in a restricted cleanup state rather than claiming completion |

### 10.2 Cleanup commands

Stop transient scopes:

```bash
systemctl --user stop 'koa-dev-workspace-alpha-*.scope'
```

List remaining user units:

```bash
systemctl --user list-units 'koa-dev-workspace-alpha-*'
```

Stop and remove workspace containers:

```bash
podman ps --filter label=koa.workspace=workspace-alpha
podman stop --filter label=koa.workspace=workspace-alpha
podman rm --filter label=koa.workspace=workspace-alpha
```

Inspect volumes before removal:

```bash
podman volume ls --filter label=koa.workspace=workspace-alpha
```

Remove transient runtime files:

```bash
rm -rf "${XDG_RUNTIME_DIR}/koa-workspace-alpha"
rm -f "${XDG_RUNTIME_DIR}/koa-workspace-alpha-heavy.lock"
```

Data volumes and component state follow their owner contracts and are not removed by a generic cleanup command.

### 10.3 Prohibited assumptions

Do not assume that:

- free memory authorizes a higher limit;
- an idle CPU is reserved for a new job;
- swap is guaranteed primary memory;
- zram replaces physical-memory planning;
- tool-level worker count replaces cgroup limits;
- a container limit creates component or policy authority;
- a policy approval guarantees capacity;
- a successful command proves the owning operation completed;
- a stopped process completed cleanup;
- one workspace can use another workspace's queue, volume, network, or lock;
- rootless execution removes the need for data and secret boundaries;
- a read-only container root makes its mounted data safe automatically;
- pressure information can increase the active envelope;
- WSL VM limits provide per-workspace isolation;
- example values are profile requirements;
- this recipe becomes normative because several teams use it;
- an unsupported controller can be reported as enforced;
- a manual runtime limit is an activated resource-envelope artifact;
- external compute or AI can substitute silently for unavailable local capacity;
- resource pressure permits deletion of another component's authoritative data.

### 10.4 Adoption

A profile that adopts part of this recipe records:

- exact adopted mechanism;
- exact version or compatibility range;
- adopted values or calculation rules;
- target scope;
- validation tests;
- failure behavior;
- rollback or removal;
- evidence;
- relationship to the canonical resource envelope.

The profile contract, not this recipe, owns the adopted requirement.

## 11. Worked Examples

### Example 1 — Bounded unit tests

A developer runs the full test suite inside a systemd user scope with two logical CPUs, a six-GiB memory ceiling, bounded tasks, and a deterministic unit name.

The editor and browser remain outside the test scope and retain host capacity.

### Example 2 — One heavy restore-validation job

A workspace launches restore validation through the heavy-job helper.

A second heavy request receives the existing lock condition and is deferred rather than starting a competing process.

### Example 3 — Rootless local database

A workspace starts one rootless database container with two CPUs, three GiB of memory, a bounded task count, a read-only root filesystem, a bounded temporary filesystem, and a workspace-owned volume.

Stopping the container does not delete the volume.

### Example 4 — Memory-pressure response

Host memory pressure rises while indexing and a build are running.

The developer pauses indexing, stops the background container, lowers build concurrency, and preserves the active editor, database, and current authoritative write.

### Example 5 — WSL outer and inner limits

A WSL VM has a sixteen-GiB outer ceiling.

Inside the VM, rootless containers and build-tool worker limits divide that capacity among workspaces. The VM ceiling is not reported as per-workspace isolation.

### Example 6 — Unsupported I/O controller

A systemd user scope applies CPU, memory, and task limits but reports that I/O accounting is unavailable.

The evidence records the limitation. The developer reduces concurrency and avoids claiming complete I/O enforcement.

### Example 7 — Offline development

A developer loses network access.

Local tests, services, builds using available dependencies, and validation continue under the same resource limits. Synchronization and other declared remote-dependent jobs are deferred without launching an undeclared provider substitute.

### Example 8 — Recipe adoption

A future developer profile adopts a rootless Podman memory and process-limit pattern from this file.

The profile contract records the exact adopted settings and tests. This recipe remains explanatory, while the profile contract becomes the authoritative requirement.
