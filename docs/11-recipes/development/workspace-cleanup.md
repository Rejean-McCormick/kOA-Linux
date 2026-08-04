<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "RECIPE-DEVELOPMENT-WORKSPACE-CLEANUP",
  "document_class": "recipe",
  "status": "active",
  "authority_participation": "non_authoritative",
  "language": "en",
  "layer": "implementation",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/document-index.json"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-002",
    "DOC-GOV-009"
  ],
  "tags": [
    "implementation",
    "recipe",
    "workspace",
    "cleanup"
  ],
  "edit_policy": "manual"
}
KOA:DOC-META:END -->

# Workspace Cleanup

> **Recipe status:** Active, non-authoritative implementation guidance.  
> **Canonical boundary:** This recipe does not define workspace identity, ownership, retention, profile behavior, component data boundaries, or lifecycle requirements. Resolve those facts from the active workspace, profile, component, toolchain, and data-owner contracts before applying any command.

## 1. Purpose

This recipe provides a cautious procedure for suspending, resetting, or retiring a kOA development workspace without deleting another workspace’s state, shared immutable caches, source history, published artifacts, or component-owned data.

It is designed for:

- `developer_linux_workstation`;
- `developer_windows_wsl` when commands are run inside the owning WSL distribution;
- another development profile that explicitly adopts the same workspace-isolation outcomes.

The procedure is local-first and does not require a remote control plane, Internet access, Kubernetes, or a specific container runtime.

## 2. Outcomes

Choose one outcome before starting.

| Cleanup level | Intended result | Source checkout | Workspace `.venv` | Local services | Workspace data | Workspace identity |
| --- | --- | --- | --- | --- | --- | --- |
| `suspend` | Stop active work while preserving a restartable workspace. | Preserve | Preserve | Stop | Preserve | Keep active or suspended according to the local registry. |
| `reset_transient` | Rebuild generated and transient state while preserving source and retained development data. | Preserve | Remove and rebuild | Stop, then recreate as needed | Preserve only data explicitly classified as retained | Keep active. |
| `retire` | Remove the workspace-owned mutable environment and release its allocations. | Preserve, archive, or remove separately after verification | Remove | Remove | Export, archive, or remove through owning interfaces | Mark retired only after verification. |

Do not use `retire` merely to recover disk space when the workspace is expected to resume. Use `reset_transient` instead.

## 3. Safety Boundaries

Apply these boundaries throughout the procedure:

1. Work from the exact workspace identity recorded by the local workspace registry.
2. Do not infer identity from a branch name, directory basename, process ID, port, container ID, or current working directory alone.
3. Keep the source checkout, source history, lockfiles, and accepted local changes until export and verification finish.
4. Do not remove another workspace’s process, port, database, schema, queue, bucket, volume, secret, environment, log, or temporary directory.
5. Do not remove shared immutable or content-addressed download caches as part of workspace retirement.
6. Do not issue generic database or object-store deletion commands from this recipe. Use the owning component’s bounded reset, export, archive, or removal operation.
7. Do not print secret values, complete environment blocks, private keys, tokens, connection strings, or secret-bearing process arguments.
8. Do not remove the only usable backup, rollback target, migration evidence, or support evidence.
9. Stop new work before destructive cleanup.
10. Treat an incomplete cleanup as `cleanup_incomplete`; keep the identity reserved until every owned resource is reconciled.

## 4. Preconditions

Confirm the following before changing state:

- the workspace identity record is readable;
- the workspace root is known and resolves to the intended checkout or worktree;
- the selected cleanup level is recorded;
- active work and queued jobs are known;
- component-owned development data has a declared disposition;
- required diagnostics, patches, test evidence, or migration evidence have an export destination;
- no release, publication, migration, backup, restore, or support operation still depends on the workspace;
- another workspace does not share the mutable environment or writable namespace;
- the operator has permission to stop and remove only the recorded workspace-owned resources;
- sufficient recovery capacity exists for any requested archive or export.

For `retire`, also confirm that no uncommitted or untracked work is being discarded unintentionally.

## 5. Set the Cleanup Inputs

Set the values from the local workspace registry and profile-owned allocation records. These are operator inputs, not architecture defaults.

```bash
export WORKSPACE_ID='koa-workspace-id-from-local-registry'
export WORKSPACE_ROOT='/absolute/path/to/the/workspace'
export CLEANUP_LEVEL='suspend'  # suspend | reset_transient | retire
export CLEANUP_RECORD_DIR="$HOME/.local/state/koa/workspace-cleanup/$WORKSPACE_ID"
export APPLY_CHANGES='0'        # 0 = inspect only, 1 = execute approved local removals
```

Create a protected local record directory:

```bash
umask 077
mkdir -p -- "$CLEANUP_RECORD_DIR"
printf '%s\n' "$WORKSPACE_ID" > "$CLEANUP_RECORD_DIR/workspace_id.txt"
printf '%s\n' "$WORKSPACE_ROOT" > "$CLEANUP_RECORD_DIR/workspace_root.txt"
printf '%s\n' "$CLEANUP_LEVEL" > "$CLEANUP_RECORD_DIR/cleanup_level.txt"
date -u +'%Y-%m-%dT%H:%M:%SZ' > "$CLEANUP_RECORD_DIR/started_at.txt"
```

Validate the path before proceeding:

```bash
python - "$WORKSPACE_ROOT" <<'PY'
from pathlib import Path
import sys

root = Path(sys.argv[1]).expanduser().resolve(strict=True)
if root == Path('/') or root == Path.home().resolve():
    raise SystemExit(f'refusing unsafe workspace root: {root}')
if not (root / '.git').exists() and not (root / '.git').is_file():
    raise SystemExit(f'workspace root does not appear to be a Git checkout or worktree: {root}')
print(root)
PY
```

Stop if the resolved path does not match the local workspace registry.

## 6. Create an Inventory Before Cleanup

Record resource identities, not secret values.

### 6.1 Source and checkout state

```bash
cd -- "$WORKSPACE_ROOT"
git rev-parse --show-toplevel > "$CLEANUP_RECORD_DIR/git_toplevel.txt"
git rev-parse --git-common-dir > "$CLEANUP_RECORD_DIR/git_common_dir.txt"
git rev-parse --verify HEAD > "$CLEANUP_RECORD_DIR/git_head.txt"
git status --porcelain=v1 --untracked-files=all > "$CLEANUP_RECORD_DIR/git_status.txt"
git worktree list --porcelain > "$CLEANUP_RECORD_DIR/git_worktrees.txt"
```

Review `git_status.txt` before any retirement action.

### 6.2 Python and UV state

```bash
{
  command -v uv || true
  uv --version 2>/dev/null || true
  python --version 2>/dev/null || true
  test -d .venv && printf '%s\n' "$WORKSPACE_ROOT/.venv"
} > "$CLEANUP_RECORD_DIR/python_environment.txt"
```

Do not run a host-wide `uv cache clean` as part of workspace cleanup. The shared UV download cache is not the workspace’s installed mutable environment.

### 6.3 User services

List candidate services without stopping them:

```bash
systemctl --user list-units --all --no-legend --plain 2>/dev/null \
  | grep -F -- "$WORKSPACE_ID" \
  > "$CLEANUP_RECORD_DIR/systemd_user_units.txt" || true
```

Only units whose identity is bound to this workspace belong in the action plan.

### 6.4 Rootless containers, pods, networks, and volumes

When Podman is used, prefer workspace labels over name matching:

```bash
podman ps -a --filter "label=koa.workspace_id=$WORKSPACE_ID" \
  --format '{{.ID}}\t{{.Names}}\t{{.Status}}' \
  > "$CLEANUP_RECORD_DIR/podman_containers.txt" 2>/dev/null || true

podman pod ps --filter "label=koa.workspace_id=$WORKSPACE_ID" \
  --format '{{.ID}}\t{{.Name}}\t{{.Status}}' \
  > "$CLEANUP_RECORD_DIR/podman_pods.txt" 2>/dev/null || true

podman network ls --filter "label=koa.workspace_id=$WORKSPACE_ID" \
  --format '{{.ID}}\t{{.Name}}' \
  > "$CLEANUP_RECORD_DIR/podman_networks.txt" 2>/dev/null || true

podman volume ls --filter "label=koa.workspace_id=$WORKSPACE_ID" \
  --format '{{.Name}}' \
  > "$CLEANUP_RECORD_DIR/podman_volumes.txt" 2>/dev/null || true
```

If the local runtime does not label resources, use the profile-owned workspace manifest. Name matching alone is insufficient for destructive removal.

### 6.5 Processes and open files

Use bounded inspection. Do not export full process environments.

```bash
pgrep -af -- "$WORKSPACE_ROOT" \
  > "$CLEANUP_RECORD_DIR/process_candidates.txt" 2>/dev/null || true

lsof +D "$WORKSPACE_ROOT" \
  > "$CLEANUP_RECORD_DIR/open_files.txt" 2>/dev/null || true
```

`lsof +D` can be expensive on a large tree. Skip it when the workspace manifest already provides complete process ownership.

### 6.6 Ports

Record ports from the workspace allocation registry. Use socket inspection only to confirm ownership:

```bash
ss -lntup 2>/dev/null > "$CLEANUP_RECORD_DIR/listening_sockets.txt" || true
```

Do not terminate a process solely because it uses a port formerly associated with the workspace. Confirm process, service, and workspace identity together.

### 6.7 Data services, queues, buckets, and secrets

Create an inventory from component-owned service manifests and local workspace allocation records:

```text
database or schema identity
queue or topic identity
bucket or object-store namespace
search index identity
workspace-owned volume identity
secret namespace and credential reference identifiers
retention or export requirement
owning component operation for reset, export, archive, or removal
```

Record identifiers and operation names in `owned_resources.txt`. Do not record secret material.

## 7. Preserve Work and Required Evidence

Before `reset_transient` or `retire`, preserve local work as applicable.

### 7.1 Patch tracked changes

```bash
cd -- "$WORKSPACE_ROOT"
git diff --binary > "$CLEANUP_RECORD_DIR/tracked_changes.patch"
git diff --binary --staged > "$CLEANUP_RECORD_DIR/staged_changes.patch"
```

### 7.2 Archive untracked files

Review the untracked list first:

```bash
git ls-files --others --exclude-standard \
  > "$CLEANUP_RECORD_DIR/untracked_files.txt"
```

To archive the listed files after review:

```bash
if test -s "$CLEANUP_RECORD_DIR/untracked_files.txt"; then
  tar -C "$WORKSPACE_ROOT" \
    -czf "$CLEANUP_RECORD_DIR/untracked_files.tar.gz" \
    -T "$CLEANUP_RECORD_DIR/untracked_files.txt"
fi
```

Do not archive known secret paths. Remove those entries from the reviewed list and preserve them only through the approved secret backend or recovery process.

### 7.3 Preserve diagnostics and evidence

Export only evidence required by an active test, support case, incident, migration, release, or exception record. Keep the exported package outside directories scheduled for removal and apply the applicable retention and disclosure rules.

## 8. Stop New Work and Drain Bounded Queues

Before stopping services:

1. stop admission of new tests, builds, transformations, migrations, and heavy work;
2. cancel or export queued work according to its contract;
3. prevent automatic restart;
4. preserve queue identities and terminal states in the cleanup record;
5. leave uncertain or unbound work stopped rather than adopting it.

Queueing does not require eventual execution. Retirement cancels or transfers queued work explicitly.

## 9. Stop Workspace-Owned Services

### 9.1 User systemd units

Review the unit list and stop only confirmed workspace-owned units:

```bash
while IFS= read -r line; do
  unit=${line%% *}
  test -n "$unit" || continue
  printf 'would stop and disable: %s\n' "$unit"
done < "$CLEANUP_RECORD_DIR/systemd_user_units.txt"
```

After review, replace the inspection loop with explicit unit names:

```bash
WORKSPACE_UNITS=(
  # Add only confirmed workspace-owned unit names from the inventory.
)

if test "$APPLY_CHANGES" = '1'; then
  for unit in "${WORKSPACE_UNITS[@]}"; do
    systemctl --user stop -- "$unit"
    if test "$CLEANUP_LEVEL" = 'retire'; then
      systemctl --user disable -- "$unit" 2>/dev/null || true
    fi
  done
fi
```

An empty array is safe and performs no action.

### 9.2 Rootless Podman containers and pods

Preview:

```bash
podman ps -a --filter "label=koa.workspace_id=$WORKSPACE_ID" \
  --format 'would stop container {{.ID}} {{.Names}}' 2>/dev/null || true
podman pod ps --filter "label=koa.workspace_id=$WORKSPACE_ID" \
  --format 'would stop pod {{.ID}} {{.Name}}' 2>/dev/null || true
```

Apply only after label ownership is confirmed:

```bash
if test "$APPLY_CHANGES" = '1'; then
  podman ps -aq --filter "label=koa.workspace_id=$WORKSPACE_ID" \
    | xargs -r podman stop --time 30
  podman pod ps -q --filter "label=koa.workspace_id=$WORKSPACE_ID" \
    | xargs -r podman pod stop --time 30
fi
```

Do not use broad name patterns such as `podman rm -a` or remove all unused volumes.

### 9.3 Native processes

Stop native processes through their workspace service manager or recorded process supervisor. Avoid broad `pkill` patterns. When no supervisor exists, inspect each candidate PID, verify its executable and working directory, request graceful termination, then escalate only for the same verified PID.

## 10. Apply the Selected Cleanup Level

### 10.1 Suspend

For `suspend`:

- keep the checkout and `.venv`;
- keep retained databases and service data;
- keep the workspace identity reserved;
- stop services and heavy work;
- preserve ports unless the profile releases them during suspension;
- record suspension time and restart prerequisites;
- verify no unexpected auto-restart occurs.

Do not remove data merely because services are stopped.

### 10.2 Reset transient state

For `reset_transient`, remove only workspace-owned transient state after services stop.

A guarded local-path removal helper:

```bash
remove_workspace_path() {
  target=$1
  python - "$WORKSPACE_ROOT" "$target" <<'PY'
from pathlib import Path
import sys

root = Path(sys.argv[1]).expanduser().resolve(strict=True)
target = Path(sys.argv[2]).expanduser().resolve(strict=False)
try:
    target.relative_to(root)
except ValueError:
    raise SystemExit(f'refusing path outside workspace: {target}')
if target == root:
    raise SystemExit('refusing to remove workspace root')
print(target)
PY
  if test "$APPLY_CHANGES" = '1'; then
    rm -rf --one-file-system -- "$target"
  else
    printf 'would remove: %s\n' "$target"
  fi
}
```

Candidate workspace-local transient paths can include only paths confirmed by the workspace and toolchain contracts:

```bash
for path in \
  "$WORKSPACE_ROOT/.venv" \
  "$WORKSPACE_ROOT/.pytest_cache" \
  "$WORKSPACE_ROOT/.mypy_cache" \
  "$WORKSPACE_ROOT/.ruff_cache" \
  "$WORKSPACE_ROOT/.coverage" \
  "$WORKSPACE_ROOT/htmlcov" \
  "$WORKSPACE_ROOT/build" \
  "$WORKSPACE_ROOT/dist"
do
  test -e "$path" || continue
  remove_workspace_path "$path"
done
```

Do not assume every generated directory has one of these names. Add a path only after confirming ownership and retention.

Recreate Python state from the declared lockfile rather than copying another workspace’s environment:

```bash
cd -- "$WORKSPACE_ROOT"
uv venv .venv
uv sync --frozen
```

Use the profile and toolchain contract when a different approved UV command is required.

### 10.3 Retire

For `retire`, perform every `reset_transient` action plus the following, in owner-controlled order:

1. export or archive retained component-owned development data;
2. invoke each component’s bounded removal operation;
3. verify databases, schemas, queues, topics, buckets, indexes, and object namespaces are absent or archived as intended;
4. revoke workspace-local credentials and remove secret references;
5. remove workspace-owned containers, pods, networks, and volumes;
6. release ports and service identities;
7. remove workspace-local generated files, logs, and temporary state according to retention;
8. remove workspace-specific service definitions;
9. mark cleanup complete in the local workspace registry;
10. remove the checkout or worktree only after all prior verification passes.

#### Remove confirmed Podman objects

Preview labels and identities first. After approval:

```bash
if test "$APPLY_CHANGES" = '1' && test "$CLEANUP_LEVEL" = 'retire'; then
  podman ps -aq --filter "label=koa.workspace_id=$WORKSPACE_ID" \
    | xargs -r podman rm -f
  podman pod ps -q --filter "label=koa.workspace_id=$WORKSPACE_ID" \
    | xargs -r podman pod rm -f
  podman network ls -q --filter "label=koa.workspace_id=$WORKSPACE_ID" \
    | xargs -r podman network rm
  podman volume ls -q --filter "label=koa.workspace_id=$WORKSPACE_ID" \
    | xargs -r podman volume rm
fi
```

A removal failure remains visible. Do not follow it with broad pruning.

#### Remove a Git worktree

Only after the workspace cleanup record is complete:

```bash
GIT_COMMON_DIR=$(git -C "$WORKSPACE_ROOT" rev-parse --path-format=absolute --git-common-dir)
printf 'Git common directory: %s\n' "$GIT_COMMON_DIR"
printf 'Workspace to remove: %s\n' "$WORKSPACE_ROOT"
```

From another checkout of the same repository:

```bash
git worktree remove -- "$WORKSPACE_ROOT"
git worktree prune --expire now
```

Use `--force` only after independently confirming that required uncommitted work has been preserved and the remaining cleanup is intentional.

## 11. Component-Owned Data Removal

Do not delete component storage by guessing storage paths or issuing ad hoc cross-component SQL.

For every resource in `owned_resources.txt`:

1. identify the owning component;
2. identify the bounded export, reset, archive, or remove operation;
3. record the requested operation and target identity;
4. execute through the component-owned interface;
5. capture the terminal result or receipt;
6. verify that no other workspace or tenant was affected;
7. retain the result in the cleanup record.

When an owning component is unavailable, leave the resource stopped and mark cleanup incomplete. Do not seize ownership through a lower-level storage tool.

## 12. Secret and Credential Cleanup

Use the profile-owned secret backend.

For `reset_transient`:

- rotate only credentials invalidated by the reset;
- preserve required workspace identity references;
- remove generated local credentials that will be recreated safely.

For `retire`:

- revoke workspace-local service credentials;
- revoke temporary external-provider credentials;
- remove workspace secret references;
- remove local secret-agent sessions;
- verify no credential remains bound solely to the retired workspace;
- preserve shared credentials only when separately authorized and referenced by another active owner.

Never print or archive secret values in the cleanup record.

## 13. Release Ports and Namespaces

Release allocations only after services stop and ownership is confirmed.

Reconcile:

- host ports;
- service names;
- container networks;
- database and schema names;
- queue and topic names;
- bucket names;
- search index names;
- volume names;
- secret namespaces;
- writable quota identities;
- heavy-work leases;
- queue identities.

Update the profile-owned allocation mechanism. Do not make a port available merely by editing a text note while a process still listens on it.

## 14. Verification

Run verification before marking cleanup complete.

### 14.1 Process and service verification

```bash
systemctl --user list-units --all --no-legend --plain 2>/dev/null \
  | grep -F -- "$WORKSPACE_ID" || true

podman ps -a --filter "label=koa.workspace_id=$WORKSPACE_ID" 2>/dev/null || true
podman pod ps --filter "label=koa.workspace_id=$WORKSPACE_ID" 2>/dev/null || true
pgrep -af -- "$WORKSPACE_ROOT" 2>/dev/null || true
```

For `retire`, no workspace-owned service or process should remain active.

### 14.2 Port verification

Compare the workspace port allocation record with current listening sockets:

```bash
ss -lntup 2>/dev/null > "$CLEANUP_RECORD_DIR/listening_sockets_after.txt" || true
```

A released allocation and a closed socket are separate checks.

### 14.3 Local-path verification

For `reset_transient`, verify only intended transient paths changed. For `retire`, verify workspace-owned mutable paths are absent or archived and the cleanup record remains outside the removed tree.

### 14.4 Data and secret verification

Verify through the owning interfaces that:

- retained data remains accessible to its owner;
- removed data is absent from the exact workspace scope;
- other workspaces remain unchanged;
- revoked credentials fail;
- shared authorized credentials still work for their remaining owners;
- required evidence and receipts remain available.

### 14.5 Regression verification

Confirm at least:

- another active workspace still starts;
- shared immutable caches remain usable;
- the source repository and other worktrees remain intact;
- the port allocator reports no collision;
- no unbound service starts automatically;
- the host retains cleanup, recovery, and diagnostic capacity.

## 15. Complete the Cleanup Record

Record the terminal result:

```bash
date -u +'%Y-%m-%dT%H:%M:%SZ' > "$CLEANUP_RECORD_DIR/completed_at.txt"
printf '%s\n' 'complete' > "$CLEANUP_RECORD_DIR/cleanup_status.txt"
```

Use `cleanup_incomplete` instead when any owned resource, credential, route, process, queue, or namespace cannot be reconciled:

```bash
printf '%s\n' 'cleanup_incomplete' > "$CLEANUP_RECORD_DIR/cleanup_status.txt"
```

An incomplete workspace identity remains reserved. Record the remaining owner, resource identity, reason, safe state, and next bounded action.

## 16. Recovery from an Interrupted Cleanup

After a host restart, terminal interruption, or partial failure:

1. load the cleanup record;
2. resolve the workspace identity again;
3. compare the current root and Git worktree state with the record;
4. discover surviving services, processes, containers, volumes, ports, queues, and credentials;
5. keep unbound resources stopped or quarantined;
6. do not rerun destructive commands blindly;
7. resume from the first unverified owner-controlled action;
8. regenerate transient state only from canonical source and lockfiles;
9. mark cleanup complete only after final verification.

When ownership cannot be established, preserve the resource and escalate through support or the applicable component runbook.

## 17. Windows and WSL Notes

For `developer_windows_wsl`:

- run Linux service, `.venv`, container, database, queue, and workspace-file cleanup inside the owning WSL distribution;
- do not delete a Linux-owned `.venv` through Windows Explorer or a Windows process while WSL services are active;
- resolve Windows and WSL paths before removal and record both representations;
- verify host-exposed ports from both Windows and WSL;
- stop Windows-side helper processes separately when the workspace contract assigns them to the workspace;
- keep credentials in their declared Windows or WSL secret backend;
- do not infer that `wsl.exe --shutdown` completes workspace retirement;
- verify other WSL workspaces and distributions remain unaffected.

A WSL distribution shutdown is a suspension mechanism, not proof of per-workspace cleanup.

## 18. Failure Handling

| Condition | Safe response |
| --- | --- |
| Workspace identity mismatch | Stop and reconcile the local registry before changing state. |
| Dirty checkout not reviewed | Preserve patches and untracked files; do not remove the worktree. |
| Service ownership uncertain | Leave the service stopped or unchanged and mark cleanup incomplete. |
| Port ownership uncertain | Keep the allocation reserved until process ownership is verified. |
| Database or schema ownership uncertain | Do not remove it; use the data owner’s diagnostic and removal interface. |
| Secret exposure suspected | Quarantine exported material, revoke the credential, and create a clean record. |
| Podman resource lacks a reliable workspace label | Use the workspace manifest; do not prune broadly. |
| Shared cache appears in the removal plan | Remove it from the plan unless its separate cache policy authorizes eviction. |
| Cleanup command affects another workspace | Stop immediately, preserve evidence, and invoke recovery or incident handling. |
| Required evidence is inside a removal path | Export it to approved protected storage before continuing. |
| Cleanup interrupted | Resume from recorded state and reverify ownership before each action. |
| Removal cannot complete | Preserve a stopped state and record `cleanup_incomplete`. |

## 19. Example Cleanup Sequence

The following sequence is intentionally conservative:

```text
resolve workspace identity
choose cleanup level
create protected cleanup record
inventory source, services, ports, data, secrets, and resources
preserve required changes and evidence
stop new work
cancel or export bounded queues
stop workspace-owned services
apply suspend, transient reset, or retirement actions
invoke owner-controlled data removal
revoke workspace credentials
release ports and namespaces
verify no cross-workspace impact
record complete or cleanup_incomplete
remove the Git worktree last when retiring
```

## 20. Completion Checklist

- [ ] Exact workspace identity resolved from the local registry.
- [ ] Cleanup level recorded.
- [ ] Workspace root safety check passed.
- [ ] Git status reviewed.
- [ ] Required patches, untracked files, diagnostics, and evidence preserved.
- [ ] New work admission stopped.
- [ ] Queued work cancelled, transferred, or recorded.
- [ ] User services stopped.
- [ ] Native processes stopped through bounded ownership.
- [ ] Rootless containers and pods reconciled.
- [ ] Workspace `.venv` preserved or removed according to the selected level.
- [ ] Shared immutable caches preserved.
- [ ] Component-owned data handled through owning interfaces.
- [ ] Secret references and credentials reconciled.
- [ ] Ports and service namespaces reconciled.
- [ ] Resource leases and writable quotas released or recorded.
- [ ] Other workspaces and source history verified intact.
- [ ] Removal and regression checks passed.
- [ ] Cleanup record marked `complete` or `cleanup_incomplete`.
- [ ] Git worktree removed only after successful retirement verification.

## 21. References

Use this recipe with the active versions of:

- `00-governance/02-documentation-contract.md`;
- `00-governance/09-canonical-ownership.md`;
- `05-development/02-workspace-identity.md`;
- `05-development/12-development-resource-governance.md`;
- the selected developer profile contract;
- the active Python and UV toolchain contract;
- the owning component contracts and removal procedures;
- the local workspace registry and allocation records.

Where this recipe conflicts with an active canonical contract, the canonical contract controls and this recipe must be corrected.
