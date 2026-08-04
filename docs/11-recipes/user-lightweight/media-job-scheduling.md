<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "RECIPE-USER-LIGHT-003",
  "document_class": "non_normative_recipe",
  "status": "active",
  "language": "en",
  "layer": "recipes",
  "scope": [
    "user_lightweight"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/capability_model",
    "contracts/system.contract.json#/resource_model",
    "generated/component-catalog.json",
    "contracts/profiles/user-lightweight.profile.json",
    "generated/profile-catalog.json",
    "contracts/artifact-classes.contract.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-PROFILE-USER-LIGHT-001",
    "DEC-SYS-RESOURCE-001",
    "DEC-SYS-COMP-001",
    "DEC-SYS-OFFLINE-001",
    "DEC-SYS-AUDIT-001",
    "DEC-LIFE-001"
  ],
  "requirement_ids": [
    "REQ-USER-LIGHT-001",
    "REQ-USER-LIGHT-002",
    "REQ-USER-LIGHT-003",
    "REQ-USER-LIGHT-004",
    "REQ-USER-LIGHT-005",
    "REQ-USER-LIGHT-006",
    "REQ-USER-LIGHT-007",
    "REQ-USER-LIGHT-008",
    "REQ-USER-LIGHT-009",
    "REQ-USER-LIGHT-010",
    "REQ-OPS-SLO-003",
    "REQ-OPS-SLO-008",
    "REQ-OPS-SLO-014",
    "REQ-OPS-SLO-021",
    "REQ-OPS-SLO-035",
    "REQ-OPS-SLO-036",
    "REQ-OPS-DR-017",
    "REQ-OPS-DR-028",
    "REQ-COMP-BOUNDARY-001",
    "REQ-COMP-BOUNDARY-002",
    "REQ-SEC-EVIDENCE-016",
    "REQ-SEC-EVIDENCE-037",
    "REQ-LIFE-ACT-001",
    "REQ-LIFE-ACT-002"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-OPS-001",
    "LOCK-OPS-002",
    "LOCK-OPS-003",
    "LOCK-OPS-004",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-AI-001",
    "LOCK-AI-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-PROFILE-001",
    "DOC-PROFILE-002",
    "DOC-SYS-006",
    "DOC-SYS-010",
    "DOC-SYS-011",
    "DOC-COMP-001",
    "DOC-OPS-003",
    "DOC-OPS-013",
    "DOC-SEC-016",
    "DOC-LIFE-013"
  ],
  "tags": [
    "recipe",
    "user-lightweight",
    "media",
    "background-jobs",
    "resource-governor",
    "scheduling",
    "offline",
    "pause-resume",
    "idempotency",
    "recovery",
    "safe-cleanup"
  ]
}
KOA:DOC-META:END -->

# Media Job Scheduling

## 1. Purpose

This recipe shows one practical way to schedule media work on a `user_lightweight` node without starving interactive navigation, playback, identity, policy, audit, or recovery functions.

The worked model uses a durable local queue, immutable job specifications, Resource Governor admission, bounded worker concurrency, explicit checkpoints, and resumable outputs.

Typical media jobs include:

- thumbnail generation;
- waveform generation;
- audio normalization;
- image resizing;
- preview generation;
- metadata extraction;
- media indexing;
- local format conversion;
- packaging for a governed export;
- verification of a downloaded or transferred media artifact.

This recipe is non-normative. The active user-lightweight profile, component contracts, Resource Governor contract, artifact contracts, and operations policies remain authoritative.

The target result is:

```text
interactive work remains responsive
+ background media work is bounded
+ queued intent is durable
+ repeated execution is duplicate-safe
+ interrupted work is resumable or safely restartable
+ external services are optional
+ final artifacts are validated before acceptance
```

## 2. Use This Recipe When

Use this recipe when:

- a lightweight device needs to process media in the background;
- several media operations could otherwise compete for CPU, memory, storage, or I/O;
- work needs to survive logout, restart, sleep, or temporary disconnection;
- an interactive action should submit work without waiting for the full conversion;
- expensive work needs to pause while the user is active;
- a job needs a visible state, progress, cancellation, and recovery path;
- a remote media or AI service is optional rather than part of the local baseline.

Do not use this recipe to:

- bypass Resource Governor admission;
- execute arbitrary shell commands from a job payload;
- let a media worker write directly to another component's authoritative store;
- treat an external provider acknowledgement as local completion;
- place raw credentials or private keys in a job;
- run an unbounded transcoding farm on the user-lightweight profile;
- make Suno or another external AI surface a required media-processing dependency;
- publish media directly without the Publication Gateway workflow.

## 3. Prerequisites and Local Layout

The node needs:

- an active `user_lightweight` profile;
- a registered media-owning component;
- an `application_instance_id`;
- a Resource Governor client;
- a durable local job store;
- a component-owned staging directory;
- a component-owned accepted-output directory;
- a component-owned quarantine directory;
- a registered media toolchain;
- enough local storage for the input, temporary output, and recovery reserve;
- current artifact and media validation rules.

A practical component-owned layout is:

```text
var/lib/koa-media/
  jobs/
    queue.sqlite3
    receipts/
  staging/
    inputs/
    work/
    outputs/
  accepted/
  quarantine/
  cache/
```

Example local identities:

```bash
export KOA_PROFILE_ID="user_lightweight"
export KOA_COMPONENT_ID="media_library"
export KOA_INSTANCE_ID="appinst_media_01"
export KOA_JOB_ROOT="${HOME}/.local/share/koa-media"
export KOA_JOB_DB="${KOA_JOB_ROOT}/jobs/queue.sqlite3"
```

The example path is suitable for a user-scoped implementation. A system-scoped implementation uses the paths and ownership defined by its component and profile contracts.

Create the directories with restrictive default permissions:

```bash
umask 077

install -d -m 700 \
  "${KOA_JOB_ROOT}/jobs/receipts" \
  "${KOA_JOB_ROOT}/staging/inputs" \
  "${KOA_JOB_ROOT}/staging/work" \
  "${KOA_JOB_ROOT}/staging/outputs" \
  "${KOA_JOB_ROOT}/accepted" \
  "${KOA_JOB_ROOT}/quarantine" \
  "${KOA_JOB_ROOT}/cache"
```

The worker identity receives access only to its component-owned paths.

## 4. Define the Job Model

### 4.1 Immutable job request

A submitted job request is immutable.

A practical request contains:

```json
{
  "job_id": "mediajob_01J4G6RRM2QJMX1Y9A0N8K3C7F",
  "job_type": "thumbnail_set",
  "component_id": "media_library",
  "application_instance_id": "appinst_media_01",
  "profile_id": "user_lightweight",
  "priority_class": "user_visible_background",
  "source_artifact_ref": "media/items/item_01J4G4D6/source",
  "source_version": "7",
  "source_expected_state": "accepted",
  "output_class": "media_preview_set",
  "parameters": {
    "widths": [256, 512, 1024],
    "format": "webp",
    "quality": 82
  },
  "resource_class": "media_light",
  "deadline_at": "2026-08-04T02:00:00-04:00",
  "idempotency_id": "idem_media_preview_item_01J4G4D6_v7",
  "requested_at": "2026-08-03T19:52:00-04:00"
}
```

The request contains references and bounded parameters. It does not contain:

- arbitrary commands;
- arbitrary executable paths;
- credentials;
- unrestricted source payloads;
- destination passwords;
- provider tokens;
- raw private keys.

### 4.2 Job types

Register a closed set of job types.

Example local set:

| Job type | Purpose | Default resource class |
| --- | --- | --- |
| `metadata_extract` | Read bounded technical metadata | `media_tiny` |
| `thumbnail_set` | Create deterministic image previews | `media_light` |
| `waveform_generate` | Create a compact waveform artifact | `media_light` |
| `audio_normalize` | Produce a normalized candidate audio file | `media_medium` |
| `image_resize` | Produce bounded image variants | `media_light` |
| `preview_transcode` | Produce a short local preview | `media_medium` |
| `full_transcode` | Produce a complete alternate encoding | `media_heavy` |
| `integrity_verify` | Verify a functional content-integrity record | `media_tiny` |
| `package_export_candidate` | Assemble a candidate publication package | `media_medium` |

The worker maps each job type to one fixed adapter.

The request cannot select an arbitrary binary or add arbitrary command-line arguments.

### 4.3 Priority classes

Use a small stable priority vocabulary:

```text
interactive_follow_up
user_visible_background
maintenance
bulk_deferred
```

`interactive_follow_up` is for short work that completes an action the user is waiting to inspect.

`user_visible_background` is for work the user explicitly started but does not need immediately.

`maintenance` is for local indexing, verification, or regeneration.

`bulk_deferred` is for long or numerous jobs that can pause readily.

Priority influences queue order. It does not override authorization, resource admission, deadline, storage reserve, or profile restrictions.

### 4.4 Resource classes

Example resource classes:

| Resource class | CPU | Memory | Storage and I/O | Default concurrency |
| --- | --- | --- | --- | --- |
| `media_tiny` | Low | Low | Small reads | 2 |
| `media_light` | Low to moderate | Low | Bounded sequential I/O | 1 |
| `media_medium` | Moderate | Moderate | Temporary output required | 1 |
| `media_heavy` | High for lightweight hardware | Moderate to high | Large temporary output | 0 or 1 when explicitly admitted |

A `media_heavy` job can remain queued indefinitely on a profile whose current resource envelope does not admit it.

Do not convert an admission denial into a lower-quality output silently. Submit a separately identified job with explicitly accepted parameters when a lower-cost variant is desired.

### 4.5 Job states

Use explicit states:

```text
queued
admission_pending
admitted
running
pause_requested
paused
cancel_requested
cancelled
completed_candidate
accepted
rejected
failed
expired
quarantined
recovery_required
```

`completed_candidate` means the adapter produced output.

`accepted` means the component validated and committed the output to its owned accepted state.

A worker process exit does not imply `failed` or `completed_candidate`; recovery first inspects the durable job and checkpoint state.

## 5. Submit a Job Safely

### 5.1 Stage the input

Resolve the source through the owning component.

Copy or link only through a registered component-owned staging operation.

Record:

- source artifact reference;
- source owner;
- source version;
- expected state;
- classification;
- selected media stream or page range;
- source size;
- functional integrity reference where required.

Do not let the worker traverse another component's filesystem.

### 5.2 Check available storage

Before queueing a job that creates output, estimate:

```text
input staging size
+ temporary work size
+ final candidate size
+ receipt and journal reserve
+ profile recovery reserve
```

Example local check:

```bash
uv run python - <<'PY'
from __future__ import annotations

import os
import shutil
from pathlib import Path

root = Path(os.environ["KOA_JOB_ROOT"])
input_bytes = 480 * 1024 * 1024
estimated_work_bytes = 900 * 1024 * 1024
estimated_output_bytes = 220 * 1024 * 1024
recovery_reserve_bytes = 2 * 1024 * 1024 * 1024

free_bytes = shutil.disk_usage(root).free
required_bytes = (
    input_bytes
    + estimated_work_bytes
    + estimated_output_bytes
    + recovery_reserve_bytes
)

if free_bytes < required_bytes:
    raise SystemExit(
        f"Insufficient storage: free={free_bytes}, required={required_bytes}"
    )

print("Storage preflight passed.")
PY
```

The component's real estimator should derive values from the media and adapter contract rather than fixed numbers.

### 5.3 Create the request file

Write the immutable request atomically:

```bash
export KOA_JOB_ID="mediajob_01J4G6RRM2QJMX1Y9A0N8K3C7F"
export KOA_JOB_REQUEST="${KOA_JOB_ROOT}/staging/work/${KOA_JOB_ID}.request.json"

umask 077
temp_request="${KOA_JOB_REQUEST}.tmp"

cat > "${temp_request}" <<'JSON'
{
  "job_id": "mediajob_01J4G6RRM2QJMX1Y9A0N8K3C7F",
  "job_type": "thumbnail_set",
  "component_id": "media_library",
  "application_instance_id": "appinst_media_01",
  "profile_id": "user_lightweight",
  "priority_class": "user_visible_background",
  "source_artifact_ref": "media/items/item_01J4G4D6/source",
  "source_version": "7",
  "source_expected_state": "accepted",
  "output_class": "media_preview_set",
  "parameters": {
    "widths": [256, 512, 1024],
    "format": "webp",
    "quality": 82
  },
  "resource_class": "media_light",
  "deadline_at": "2026-08-04T02:00:00-04:00",
  "idempotency_id": "idem_media_preview_item_01J4G4D6_v7",
  "requested_at": "2026-08-03T19:52:00-04:00"
}
JSON

chmod 600 "${temp_request}"
mv "${temp_request}" "${KOA_JOB_REQUEST}"
```

The queue submission command validates the schema before inserting the job.

### 5.4 Submit through the component interface

Example:

```bash
uv run python -m media_jobs.cli submit \
  --request "${KOA_JOB_REQUEST}"
```

`media_jobs.cli` is an illustrative component-owned command name. Use the command registered by the active media component.

Submission should:

1. validate the request;
2. verify the source reference and expected state;
3. bind the idempotency identity to the canonical request body;
4. reject conflicting reuse;
5. persist the request and initial state;
6. create a submission receipt;
7. return the durable job identity.

Equivalent retry returns the existing job identity without creating another effect.

## 6. Run the Lightweight Scheduler

### 6.1 Scheduler cycle

A scheduler cycle performs:

```text
load durable queue
recover nonterminal jobs
expire overdue queued jobs
read current user activity
read power and thermal state
request Resource Governor admission
select one eligible job
start or resume one worker
observe progress and checkpoints
accept, pause, cancel, fail, or quarantine
persist state and receipt
```

The queue does not need a busy polling loop. A local event, timer, or bounded wake interval is sufficient.

### 6.2 Admission inputs

Resource Governor admission can consider:

- current profile;
- CPU utilization;
- memory pressure;
- free storage;
- I/O pressure;
- thermal state;
- battery or power state;
- current interactive activity;
- active playback;
- recovery reserve;
- job resource class;
- job deadline;
- current worker count.

Resource Governor decides resource admission.

It does not decide whether the media may be processed, disclosed, published, or exported.

### 6.3 Suggested lightweight policy

A practical starting policy is:

| Condition | Scheduler behavior |
| --- | --- |
| User actively navigating | Run only `media_tiny`; pause heavy jobs at checkpoints |
| Local media playback active | Avoid I/O-heavy and CPU-heavy work |
| Device on battery below profile threshold | Run only urgent short jobs or pause |
| Thermal pressure elevated | Pause medium and heavy jobs |
| Memory pressure elevated | Do not start new jobs; checkpoint current resumable work |
| Recovery reserve threatened | Cancel disposable temporary output and stop new work |
| Idle and externally powered | Admit one medium or heavy job if the profile allows |
| Offline | Continue local jobs; defer external steps |
| External integration unavailable | Keep local work and mark external substep deferred |

These are example policy inputs, not universal numeric thresholds.

### 6.4 User-scoped service example

A user-scoped service can run a single scheduler process.

Example `~/.config/systemd/user/koa-media-scheduler.service`:

```ini
[Unit]
Description=kOA lightweight media scheduler
After=default.target

[Service]
Type=simple
Environment=KOA_PROFILE_ID=user_lightweight
Environment=KOA_COMPONENT_ID=media_library
Environment=KOA_INSTANCE_ID=appinst_media_01
Environment=KOA_JOB_ROOT=%h/.local/share/koa-media
ExecStart=%h/.local/bin/uv run python -m media_jobs.scheduler
Restart=on-failure
RestartSec=5
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=%h/.local/share/koa-media
RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6

[Install]
WantedBy=default.target
```

The exact hardening and executable path are profile-owned.

Enable only after verifying the installed command and paths:

```bash
systemctl --user daemon-reload
systemctl --user enable --now koa-media-scheduler.service
```

A profile without systemd user services can use its registered local service manager.

### 6.5 One worker per admitted slot

The scheduler starts at most the admitted worker count.

Do not let each submitted job launch its own unmanaged process.

A worker receives:

- immutable job request;
- owned input path;
- owned work directory;
- owned output directory;
- resource envelope;
- cancellation handle;
- checkpoint path;
- result path.

## 7. Checkpoints, Cancellation, and Recovery

### 7.1 Checkpoint strategy

A job is either:

- restart-safe from the beginning;
- resumable from explicit checkpoints;
- non-resumable and safely discardable before acceptance.

The job adapter declares which model applies.

Useful checkpoints include:

- completed page number;
- completed frame range;
- completed media segment;
- completed output variant;
- input and adapter version;
- temporary artifact references;
- observed progress;
- last verified output boundary.

Do not infer resumability from the presence of a temporary file.

### 7.2 Pause

A pause request:

1. changes durable job intent to `pause_requested`;
2. signals the worker;
3. waits for a bounded checkpoint;
4. records the checkpoint;
5. terminates or suspends the worker safely;
6. records `paused`.

A non-checkpointable job can finish its current bounded unit or cancel according to the adapter contract.

### 7.3 Cancel

Cancellation distinguishes:

- queued cancellation;
- pre-output cancellation;
- temporary-output cleanup;
- post-candidate rejection;
- accepted-output removal request.

Cancelling an accepted artifact is a component lifecycle operation, not deletion of a queue row.

Example:

```bash
uv run python -m media_jobs.cli cancel \
  --job-id "mediajob_01J4G6RRM2QJMX1Y9A0N8K3C7F" \
  --reason "user_cancelled"
```

### 7.4 Restart recovery

At scheduler startup:

1. find jobs in `admitted`, `running`, `pause_requested`, or `cancel_requested`;
2. inspect worker liveness;
3. inspect checkpoint and output state;
4. verify the source version and expected state;
5. classify the prior effect;
6. resume, restart, reject, quarantine, or mark `recovery_required`;
7. record the reconciliation result.

Never mark every former `running` job as queued without inspecting its output and checkpoint state.

### 7.5 Unknown outcome

A job enters `recovery_required` when:

- the worker may have created a complete candidate but did not record it;
- the output directory contains an unrecognized file;
- the checkpoint and output disagree;
- the source changed during execution;
- an external substep outcome is unknown;
- acceptance may have occurred but the receipt is missing.

Recovery verifies actual state before retry.

## 8. Validate and Accept Media Outputs

### 8.1 Candidate validation

A media candidate can require:

- expected output count;
- expected dimensions;
- expected duration;
- allowed codecs and containers;
- bounded file size;
- MIME verification;
- decoder read test;
- metadata policy;
- no unexpected streams;
- functional integrity where required;
- source and transformation provenance;
- classification;
- accessibility metadata;
- profile compatibility.

A tool exit code alone is insufficient.

### 8.2 Atomic acceptance

Accept outputs by:

1. validating every required candidate file;
2. writing the output manifest;
3. recording provenance;
4. creating functional integrity records where required;
5. moving or committing the complete output set atomically;
6. updating the owning component's state through its interface;
7. creating an acceptance receipt;
8. marking the job `accepted`.

Do not expose a partially completed preview set as the accepted set.

### 8.3 Rejected and quarantined output

Use `rejected` for a normal validation failure.

Use `quarantined` when the output is suspicious, malformed, policy-incompatible, unexpectedly large, mislabeled, or potentially hostile.

Quarantine retains minimum evidence and blocks ordinary use.

### 8.4 External media and AI steps

An optional external step can use a registered integration.

For example, a user-selected Suno workflow can return a candidate audio artifact.

The external step remains separate from the local scheduling baseline.

The returned artifact needs:

- destination and request binding;
- provenance;
- classification;
- validation;
- rights and consent review;
- local acceptance;
- publication controls where applicable.

The scheduler does not treat provider completion as accepted local media.

### 8.5 Receipts and observability

Record meaningful transitions:

- submission;
- admission;
- start;
- pause;
- resume;
- cancellation;
- candidate completion;
- rejection;
- quarantine;
- acceptance;
- recovery;
- expiration.

Metrics can include:

- queued jobs by resource and priority class;
- oldest queue age;
- active workers;
- admission denials;
- pause count;
- cancellation count;
- candidate validation failures;
- recovery-required jobs;
- temporary storage use;
- accepted output rate.

Do not place media payloads, credentials, raw private evidence, or unrestricted transcripts in logs or receipts.

## 9. User Controls and Operating Modes

### 9.1 Queue inspection

Example:

```bash
uv run python -m media_jobs.cli list \
  --states queued,admission_pending,admitted,running,paused,recovery_required
```

A user-facing view should show:

- job purpose;
- source display reference;
- current state;
- progress;
- estimated resource class;
- reason for deferral;
- deadline;
- pause or cancel availability;
- candidate or accepted result.

Do not show secret paths or sensitive source details outside the authorized UI.

### 9.2 Pause background work

Example:

```bash
uv run python -m media_jobs.cli pause-all \
  --classes media_medium,media_heavy \
  --reason "user_active"
```

This changes scheduler intent. It does not kill processes without checkpoint handling.

### 9.3 Resume eligible work

Example:

```bash
uv run python -m media_jobs.cli resume-eligible
```

Resource Governor re-evaluates each job.

A previously admitted job does not retain permanent admission.

### 9.4 Low-resource mode

A low-resource mode can:

- stop new medium and heavy admissions;
- pause resumable active work;
- preserve queue durability;
- preserve receipts and checkpoints;
- retain only bounded temporary data;
- continue tiny verification and cleanup jobs;
- keep interactive capabilities responsive.

The mode does not delete accepted media.

### 9.5 Offline mode

Offline behavior:

- local jobs continue;
- remote fetch, provider, publication, and export substeps become deferred or blocked;
- durable queue state remains local;
- accepted local outputs remain available;
- retries wait for explicit or policy-governed reconnection;
- provider result reconciliation remains duplicate-safe.

The UI distinguishes local completion from remote completion.

### 9.6 Maintenance window

A maintenance window can admit deferred jobs when:

- the user requested or accepted the window;
- the profile permits the work;
- power, thermal, storage, and recovery reserves pass;
- the window has a stop time;
- active work can checkpoint before the stop time.

Maintenance does not create broader data or publication authority.

## 10. Cleanup and Troubleshooting

### 10.1 Remove disposable work files

Cleanup selects files by exact job identity and owned path.

Example:

```bash
uv run python -m media_jobs.cli cleanup \
  --job-id "mediajob_01J4G6RRM2QJMX1Y9A0N8K3C7F" \
  --scope disposable-work
```

The cleanup command verifies:

- job ownership;
- component identity;
- path containment;
- current state;
- accepted-output references;
- retention;
- active recovery need.

Do not use broad wildcard deletion under the job root.

### 10.2 Expire queued work

A queued job can expire after its deadline.

Expiration:

- preserves the immutable request;
- records the reason;
- releases reservations;
- removes disposable staged input according to retention;
- creates an expiration receipt;
- leaves the source artifact unchanged.

### 10.3 Retire the scheduler

Before retiring the scheduler:

1. stop new submissions;
2. inspect nonterminal jobs;
3. complete, pause, cancel, or transfer each job;
4. preserve required receipts and candidate provenance;
5. revoke optional integration credentials;
6. remove the service;
7. remove disposable staging data;
8. preserve accepted component-owned outputs;
9. verify interactive media functions;
10. record retirement.

### 10.4 Troubleshooting matrix

| Symptom | Likely cause | Safe response |
| --- | --- | --- |
| Interface becomes sluggish | Worker admitted during active use or resource class too small | Pause at checkpoint and correct the job or profile resource classification |
| Queue never drains | Admission conditions never pass | Inspect reason codes, power, thermal, storage, and profile limits; do not bypass Resource Governor |
| Job restarts from zero repeatedly | Missing or invalid checkpoints | Mark the adapter restart-safe or add verified checkpoint support |
| Duplicate output appears | Missing idempotency or acceptance binding | Quarantine duplicates, inspect canonical request binding, and repair the adapter |
| Storage fills during conversion | Estimate or cleanup policy too weak | Pause, protect recovery reserve, remove only verified disposable work, then revise estimates |
| Completed file cannot be opened | Exit code was treated as validation | Reject the candidate and add decoder or format validation |
| Worker accesses unrelated files | Adapter path allowlist failure | Stop and quarantine the job, revoke access, and correct the component boundary |
| External provider says complete but no local output exists | Provider acknowledgement was mistaken for acceptance | Reconcile the request and perform local validation before acceptance |
| Job remains `running` after restart | Startup reconciliation did not classify prior state | Inspect worker, checkpoint, output, and receipts; move to the correct recovery state |
| Cancellation deletes accepted media | Queue cleanup crossed the component lifecycle boundary | Restore if possible, record the incident, and separate job cleanup from accepted-artifact removal |
| Heavy work starts on battery | Power state absent from admission | Add the active profile's power policy to Resource Governor input |
| Offline mode retries continuously | Retry policy ignores integration state | Defer the remote substep and keep local work duplicate-safe |

## 11. Completion Checklist

The recipe is complete when:

- [ ] the media component owns the queue, staging, accepted, quarantine, and cache paths;
- [ ] job types and parameters are closed and validated;
- [ ] every job has a stable identity and idempotency identity;
- [ ] one canonical request body binds to one idempotency identity;
- [ ] source references include version and expected state;
- [ ] priority and resource classes are explicit;
- [ ] Resource Governor admits every worker start or resume;
- [ ] interactive activity, playback, power, thermal, memory, storage, and recovery reserve affect admission;
- [ ] worker concurrency is bounded;
- [ ] arbitrary shell and arbitrary path execution are absent;
- [ ] nonterminal job state survives restart;
- [ ] checkpoints are explicit and verified;
- [ ] cancellation does not delete accepted component state;
- [ ] unknown outcomes enter reconciliation;
- [ ] output validation checks the actual media result;
- [ ] output acceptance is atomic;
- [ ] provider acknowledgement remains separate from local acceptance;
- [ ] logs and receipts exclude payloads and secrets;
- [ ] offline local processing works without an external service;
- [ ] cleanup uses exact job and ownership identities;
- [ ] low-resource mode preserves queue, receipts, checkpoints, and recovery reserve;
- [ ] removing the scheduler leaves accepted media and core user functions intact;
- [ ] tests cover admission denial, pause, resume, restart recovery, duplicate submission, cancellation, low storage, malformed output, and offline behavior;
- [ ] the result is represented only as a user-lightweight recipe, not as a production or sovereign conformance claim.
