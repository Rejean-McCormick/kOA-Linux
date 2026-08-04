<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-RECIPE-USER-ZRAM-001",
  "document_class": "recipe",
  "status": "active",
  "language": "en",
  "layer": "recipe",
  "scope": [
    "user_lightweight"
  ],
  "canonical_refs": [
    "generated/decision-index.json",
    "generated/profile-catalog.json",
    "contracts/profiles/user-lightweight.profile.json",
    "contracts/components/resource-governor.component.json",
    "contracts/artifact-contracts/resource-envelope.schema.json",
    "contracts/artifact-contracts/decision-receipt.schema.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-HW-001",
    "DEC-PROFILE-001",
    "DEC-GOV-001"
  ],
  "requirement_ids": [
    "REQ-CONF-USER-004",
    "REQ-CONF-USER-005",
    "REQ-CONF-USER-006",
    "REQ-CONF-USER-007",
    "REQ-CONF-USER-009",
    "REQ-CONF-USER-027",
    "REQ-CONF-USER-029",
    "REQ-SYS-RG-001",
    "REQ-SYS-RG-002",
    "REQ-SYS-RG-005",
    "REQ-SYS-RG-012",
    "REQ-SYS-RG-013",
    "REQ-SYS-RG-015",
    "REQ-SYS-RG-021",
    "REQ-OPS-OBS-024",
    "REQ-OPS-OBS-025"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-GOV-001",
    "LOCK-OPS-001",
    "LOCK-OPS-002",
    "LOCK-IMPL-001",
    "LOCK-DOC-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-014",
    "DOC-PROFILE-001",
    "DOC-PROFILE-004",
    "DOC-OPS-001",
    "DOC-OPS-012",
    "DOC-CONF-002",
    "DOC-CONF-007",
    "DOC-CONF-018",
    "DOC-ADR-017"
  ],
  "tags": [
    "recipe",
    "user-lightweight",
    "zram",
    "cgroup-v2",
    "systemd",
    "resource-limits",
    "memory-pressure",
    "heavy-job",
    "safe-degradation",
    "resource-governor"
  ],
  "normative": false
}
KOA:DOC-META:END -->

# zram and cgroup Limits for User Lightweight

> **Recipe status:** Non-normative implementation guidance.  
> The active profile, Resource Governor, component, operations, and conformance contracts take precedence.

## 1. Purpose

This recipe shows one Linux implementation of the `user_lightweight` resource envelope using:

- `systemd-zram-generator` for compressed-memory swap;
- cgroup v2 through systemd slices;
- bounded CPU, memory, input-output, and process limits;
- one fixed transient unit for heavy-job admission;
- observable validation and rollback steps.

The recipe targets a single-user endpoint. It is designed to preserve interactive use and authoritative component state while background or heavy work is delayed, throttled, rejected, or stopped under pressure.

It does not redefine the hardware envelope. The active profile contract remains the owner of minimum hardware, required zram behavior, and heavy-job concurrency.

## 2. Applicability and Preconditions

Use this recipe when:

- the active primary profile is `user_lightweight`;
- the host uses Linux with systemd;
- the unified cgroup v2 hierarchy is available;
- the host has at least the profile-owned minimum physical memory and storage;
- the implementation permits `systemd-zram-generator` or an equivalent profile-approved mechanism;
- Resource Governor decisions can be mapped to systemd slices or equivalent controls;
- the operator can make system configuration changes and reboot or restart affected services.

This recipe assumes:

- one ordinary interactive user;
- core operating-system and desktop processes remain outside the kOA background slice unless their contracts explicitly place them there;
- kOA background services can be assigned to `koa-background.slice`;
- resource-intensive jobs are launched through the heavy-job wrapper.

This recipe does not require:

- containers;
- Kubernetes;
- a discrete GPU;
- a cluster scheduler;
- a specific Linux distribution.

Before changing the host, create a recovery path for the current boot and systemd configuration.

## 3. Resource Model and Example Tuning

The implementation uses three resource classes:

| Resource class | Purpose | Example behavior |
| --- | --- | --- |
| Core and interactive | Navigation, ordinary application access, authority verification, critical local services | Not placed under the background ceiling by this recipe |
| Background | Indexing, synchronization, previews, maintenance, ordinary asynchronous workers | Lower CPU and I/O weight with bounded memory |
| Heavy job | Transcoding, large indexing, restore, or another component-declared heavy operation | One active unit, lower scheduling weight, explicit memory ceiling |

The example derives limits from total physical memory:

| Setting | Formula used by this recipe |
| --- | --- |
| zram logical size | 50% of physical RAM |
| Background `MemoryHigh` | 35% of physical RAM |
| Background `MemoryMax` | 50% of physical RAM |
| Heavy-job `MemoryHigh` | 25% of physical RAM |
| Heavy-job `MemoryMax` | 40% of physical RAM |

These percentages are recipe values, not canonical profile values. Review them against the active component budgets and measured workload before adoption.

The heavy-job maximum remains one because the active user-lightweight decision owns that concurrency limit.

## 4. Inspect and Record the Existing Host State

Run the checks before making changes:

```bash
set -euo pipefail

printf '%s\n' "systemd version:"
systemd --version | head -1

printf '%s\n' "cgroup filesystem:"
stat -fc '%T' /sys/fs/cgroup

printf '%s\n' "available controllers:"
cat /sys/fs/cgroup/cgroup.controllers

printf '%s\n' "memory:"
free -h

printf '%s\n' "existing swap:"
swapon --show --bytes --output=NAME,TYPE,SIZE,USED,PRIO

printf '%s\n' "existing zram devices:"
zramctl || true

printf '%s\n' "current pressure:"
cat /proc/pressure/cpu
cat /proc/pressure/memory
cat /proc/pressure/io
```

Expected cgroup filesystem:

```text
cgroup2fs
```

Required controllers for this recipe:

```text
cpu io memory pids
```

Record the current state:

```bash
sudo install -d -m 0750 /var/lib/koa/resource-baseline

sudo sh -c '
  {
    date --iso-8601=seconds
    systemd --version | head -1
    printf "\nMEMINFO\n"
    cat /proc/meminfo
    printf "\nSWAP\n"
    swapon --show --bytes
    printf "\nCGROUP CONTROLLERS\n"
    cat /sys/fs/cgroup/cgroup.controllers
    printf "\nZRAM\n"
    zramctl
  } > /var/lib/koa/resource-baseline/before-zram-cgroups.txt
'
```

Stop when the unified hierarchy or required controllers are unavailable. Use another profile-approved mechanism rather than partially applying the recipe.

## 5. Configure zram

### 5.1 Install the generator

Install `systemd-zram-generator` using the host's maintained package source. Package names can vary, so confirm the package and service ownership for the selected distribution.

Verify that the generator exists:

```bash
command -v zram-generator >/dev/null 2>&1 ||
  test -x /usr/lib/systemd/system-generators/zram-generator ||
  test -x /usr/lib/systemd/system-generators/systemd-zram-generator
```

### 5.2 Write the generator configuration

Create:

```text
/etc/systemd/zram-generator.conf
```

```bash
sudo install -d -m 0755 /etc/systemd

sudo tee /etc/systemd/zram-generator.conf >/dev/null <<'EOF'
[zram0]
zram-size = ram / 2
compression-algorithm = zstd
swap-priority = 100
fs-type = swap
EOF
```

This configures a logical zram device equal to half of physical memory. Actual compressed memory consumption remains workload dependent.

### 5.3 Activate

The safest activation path is a reboot after confirming the configuration and recovery method.

For a controlled maintenance window:

```bash
sudo systemctl daemon-reload
sudo reboot
```

After restart:

```bash
swapon --show --bytes --output=NAME,TYPE,SIZE,USED,PRIO
zramctl
```

Confirm:

- one active zram swap device;
- compression algorithm `zstd`, or the profile-approved equivalent;
- priority `100`;
- no duplicate unmanaged zram swap device;
- no unexpected disk swap priority above the zram device.

Do not disable an existing encrypted disk-swap recovery arrangement without reviewing the active profile and security contracts.

## 6. Create the cgroup v2 Slices

### 6.1 Calculate host-relative memory values

Create a small generator for the systemd drop-ins:

```bash
sudo install -d -m 0755 /usr/local/libexec

sudo tee /usr/local/libexec/koa-generate-user-lightweight-limits >/dev/null <<'PY'
#!/usr/bin/env python3
from pathlib import Path

mem_kib = None
for line in Path("/proc/meminfo").read_text().splitlines():
    if line.startswith("MemTotal:"):
        mem_kib = int(line.split()[1])
        break

if mem_kib is None:
    raise SystemExit("MemTotal not found")

total_bytes = mem_kib * 1024

def gib_fraction(numerator: int, denominator: int) -> str:
    value = total_bytes * numerator // denominator
    mebibytes = max(256, value // (1024 * 1024))
    return f"{mebibytes}M"

values = {
    "BACKGROUND_HIGH": gib_fraction(35, 100),
    "BACKGROUND_MAX": gib_fraction(50, 100),
    "HEAVY_HIGH": gib_fraction(25, 100),
    "HEAVY_MAX": gib_fraction(40, 100),
}

for key, value in values.items():
    print(f"{key}={value}")
PY

sudo chmod 0755 /usr/local/libexec/koa-generate-user-lightweight-limits
```

Generate the values:

```bash
eval "$(
  sudo /usr/local/libexec/koa-generate-user-lightweight-limits
)"

printf '%s\n' \
  "background_high=$BACKGROUND_HIGH" \
  "background_max=$BACKGROUND_MAX" \
  "heavy_high=$HEAVY_HIGH" \
  "heavy_max=$HEAVY_MAX"
```

### 6.2 Configure the background slice

```bash
sudo install -d -m 0755 \
  /etc/systemd/system/koa-background.slice.d

sudo tee \
  /etc/systemd/system/koa-background.slice.d/limits.conf \
  >/dev/null <<EOF
[Slice]
CPUWeight=100
IOWeight=100
MemoryHigh=$BACKGROUND_HIGH
MemoryMax=$BACKGROUND_MAX
TasksMax=2048
EOF
```

### 6.3 Configure the heavy-job slice

```bash
sudo install -d -m 0755 \
  /etc/systemd/system/koa-heavy.slice.d

sudo tee \
  /etc/systemd/system/koa-heavy.slice.d/limits.conf \
  >/dev/null <<EOF
[Slice]
CPUWeight=50
IOWeight=50
MemoryHigh=$HEAVY_HIGH
MemoryMax=$HEAVY_MAX
TasksMax=512
EOF
```

### 6.4 Activate the slice definitions

```bash
sudo systemctl daemon-reload

sudo systemctl start koa-background.slice
sudo systemctl start koa-heavy.slice

systemctl show koa-background.slice \
  -p CPUWeight \
  -p IOWeight \
  -p MemoryHigh \
  -p MemoryMax \
  -p TasksMax

systemctl show koa-heavy.slice \
  -p CPUWeight \
  -p IOWeight \
  -p MemoryHigh \
  -p MemoryMax \
  -p TasksMax
```

The slices are enforcement mechanisms, not independent Resource Governor authority. The canonical profile and component budgets still determine which work belongs in each class.

## 7. Assign Services and Enforce One Heavy Job

### 7.1 Assign a background service

For a system service named `koa-preview-worker.service`:

```bash
sudo systemctl edit koa-preview-worker.service
```

Add:

```ini
[Service]
Slice=koa-background.slice
CPUAccounting=yes
MemoryAccounting=yes
IOAccounting=yes
TasksAccounting=yes
```

Then apply:

```bash
sudo systemctl daemon-reload
sudo systemctl restart koa-preview-worker.service

systemctl show koa-preview-worker.service \
  -p Slice \
  -p ControlGroup \
  -p MemoryCurrent \
  -p TasksCurrent
```

Repeat only for services whose active component contract classifies them as background work.

### 7.2 Install the heavy-job launcher

The fixed transient unit name causes systemd to reject a second simultaneous start.

```bash
sudo install -d -m 0755 /usr/local/sbin

sudo tee /usr/local/sbin/koa-heavy-run >/dev/null <<'SH'
#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -eq 0 ]; then
  printf 'usage: %s command [argument ...]\n' "$0" >&2
  exit 64
fi

UNIT="koa-heavy-job.service"

if systemctl is-active --quiet "$UNIT"; then
  printf '%s\n' \
    "A heavy job is already active; queue or retry later." >&2
  exit 75
fi

exec systemd-run \
  --unit="$UNIT" \
  --slice=koa-heavy.slice \
  --property=CPUAccounting=yes \
  --property=MemoryAccounting=yes \
  --property=IOAccounting=yes \
  --property=TasksAccounting=yes \
  --property=Nice=10 \
  --property=IOSchedulingClass=best-effort \
  --property=IOSchedulingPriority=7 \
  --collect \
  --wait \
  --pipe \
  -- "$@"
SH

sudo chmod 0755 /usr/local/sbin/koa-heavy-run
```

Example:

```bash
sudo koa-heavy-run \
  /usr/local/libexec/koa-media-transcode \
  --input /srv/koa/inbox/example.mkv
```

A second invocation while the first remains active exits with a temporary-failure status.

Every supported heavy-job entry point needs to call the Resource Governor or this approved enforcement adapter. Directly invoking the underlying heavy command bypasses the recipe and invalidates its concurrency evidence.

### 7.3 Inspect current admission state

```bash
systemctl status koa-heavy-job.service || true

systemctl show koa-heavy-job.service \
  -p ActiveState \
  -p SubState \
  -p Slice \
  -p MemoryCurrent \
  -p CPUUsageNSec \
  -p IOReadBytes \
  -p IOWriteBytes \
  -p TasksCurrent || true
```

## 8. Validate Pressure, Degradation, and Observability

### 8.1 Validate zram

```bash
swapon --show --bytes --output=NAME,TYPE,SIZE,USED,PRIO
zramctl --output NAME,DISKSIZE,DATA,COMPR,TOTAL,ALGORITHM
```

Record:

- physical memory;
- zram logical size;
- compression algorithm;
- active priority;
- compressed and uncompressed use during the test;
- any disk-swap relationship.

### 8.2 Validate cgroup placement

```bash
systemd-cgls /koa-background.slice
systemd-cgls /koa-heavy.slice

systemctl show koa-background.slice \
  -p MemoryCurrent \
  -p MemoryPeak \
  -p MemoryEvents \
  -p CPUUsageNSec \
  -p TasksCurrent

systemctl show koa-heavy.slice \
  -p MemoryCurrent \
  -p MemoryPeak \
  -p MemoryEvents \
  -p CPUUsageNSec \
  -p TasksCurrent
```

### 8.3 Validate the one-heavy-job limit

Start one controlled test job:

```bash
sudo koa-heavy-run /usr/bin/sleep 60
```

While it is active, run from another terminal:

```bash
sudo koa-heavy-run /usr/bin/sleep 10
```

Expected behavior:

- the first unit remains active;
- the second request is rejected or queued by the higher-level Resource Governor;
- no second heavy transient service becomes active.

### 8.4 Validate bounded degradation

Use an approved synthetic load or component test. Keep the load within the test catalog and stop conditions.

Observe:

```bash
watch -n 2 '
  printf "\nMEMORY\n"
  free -h
  printf "\nSWAP\n"
  swapon --show
  printf "\nPRESSURE\n"
  cat /proc/pressure/memory
  printf "\nHEAVY SLICE\n"
  systemctl show koa-heavy.slice \
    -p MemoryCurrent \
    -p MemoryHigh \
    -p MemoryMax \
    -p MemoryEvents
'
```

The expected operational pattern is:

- interactive navigation remains responsive where the active test defines it;
- background and heavy work slow, queue, stop, or fail before authoritative state is endangered;
- memory-pressure state is visible;
- health and readiness expose the affected work class;
- no resource limit is removed automatically;
- no optional external service becomes an undeclared substitute.

### 8.5 Capture bounded evidence

```bash
sudo install -d -m 0750 /var/lib/koa/resource-evidence

sudo sh -c '
  {
    date --iso-8601=seconds
    printf "\nMEMORY\n"
    free -b
    printf "\nSWAP\n"
    swapon --show --bytes
    printf "\nZRAM\n"
    zramctl
    printf "\nBACKGROUND SLICE\n"
    systemctl show koa-background.slice
    printf "\nHEAVY SLICE\n"
    systemctl show koa-heavy.slice
    printf "\nPRESSURE\n"
    cat /proc/pressure/cpu
    cat /proc/pressure/memory
    cat /proc/pressure/io
  } > /var/lib/koa/resource-evidence/user-lightweight-resource-state.txt
'
```

Review and minimize the evidence before export. Do not include secret values, unrestricted process environments, personal data, or unrelated diagnostics.

## 9. Failure Handling

| Failure | Response |
| --- | --- |
| cgroup v2 is unavailable | Stop; use another profile-approved enforcement mechanism. |
| `memory`, `cpu`, `io`, or `pids` controller is unavailable | Keep the affected resource claim blocked. |
| zram generator is unavailable | Select an equivalent approved implementation; do not omit required zram silently. |
| zram activation fails | Preserve the previous bootable state and keep the hardware/profile claim blocked. |
| duplicate zram devices appear | Stop and reconcile generators before pressure testing. |
| `MemoryHigh` is reached | Expect throttling and reclaim; observe health, readiness, and job state. |
| `MemoryMax` is reached | Treat resulting job failure or termination as an operational event; preserve authoritative state. |
| the heavy-job unit is already active | Reject or queue the new request. |
| a service bypasses its assigned slice | Stop the service and correct its unit or launch path. |
| interactive use becomes unresponsive | Stop the synthetic load and lower background/heavy budgets after review. |
| evidence collection becomes excessive | Reduce frequency and field scope; observability remains bounded. |
| systemd configuration prevents boot | Use the recorded recovery path, remove the candidate drop-ins, and restore the last valid configuration. |

Do not respond to pressure by:

- disabling required verification;
- increasing limits without review;
- starting another heavy job outside Resource Governor control;
- deleting component data;
- exposing secrets in diagnostics;
- replacing local work silently with external processing.

## 10. Rollback and Cleanup

### 10.1 Remove service assignments

For each modified service:

```bash
sudo systemctl revert koa-preview-worker.service
```

Review the resulting unit before restart.

### 10.2 Remove the launcher and slice drop-ins

```bash
sudo rm -f /usr/local/sbin/koa-heavy-run
sudo rm -f /usr/local/libexec/koa-generate-user-lightweight-limits

sudo rm -rf /etc/systemd/system/koa-background.slice.d
sudo rm -rf /etc/systemd/system/koa-heavy.slice.d

sudo systemctl daemon-reload
sudo systemctl stop koa-heavy.slice || true
sudo systemctl stop koa-background.slice || true
```

### 10.3 Remove the zram configuration

Only remove zram after reviewing active swap use and confirming a safe reboot path.

```bash
sudo rm -f /etc/systemd/zram-generator.conf
sudo systemctl daemon-reload
sudo reboot
```

After restart:

```bash
swapon --show
zramctl
```

### 10.4 Verify rollback

Confirm:

- no service references the removed slices;
- no heavy-job wrapper remains in use;
- expected swap behavior matches the restored profile configuration;
- the system remains healthy and ready;
- the previous complete evidence set is retained as historical evidence;
- a new conformance claim is not issued until revalidation passes.

## 11. Adaptation Checklist

Before adopting or modifying this recipe, confirm:

- `user_lightweight` is the effective primary profile;
- the profile contract owns the hardware and resource values;
- the host meets the minimum hardware envelope;
- cgroup v2 and required controllers are available;
- zram is active and observable;
- zram sizing and compression are tested for the host;
- background and heavy services are classified by active component contracts;
- core and interactive capabilities are protected from background pressure;
- every heavy-job entry point passes through Resource Governor enforcement;
- no more than one heavy job can become active;
- CPU, memory, input-output, process, queue, retry, and duration bounds exist;
- health and readiness distinguish resource classes;
- pressure and rejection states are observable;
- evidence collection is bounded and free of secrets;
- backup, restore, update, and recovery retain enough capacity;
- containers and Kubernetes remain optional;
- overlay requirements are added only through explicit compatible composition;
- rollback restores a known bootable and bounded state;
- tests and evidence apply to the exact host, profile version, components, artifacts, and authority set.

A tuning change is ready for use only after clean validation confirms profile ownership, safe degradation, one-heavy-job admission, observability, rollback, and evidence completeness.
