<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-RECIPE-BUILD-REPRO-001",
  "document_class": "recipe",
  "status": "active",
  "language": "en",
  "layer": "recipe",
  "scope": [
    "build_farm"
  ],
  "canonical_refs": [
    "generated/decision-index.json",
    "generated/profile-catalog.json",
    "contracts/profiles/build-farm.profile.json",
    "contracts/components/resource-governor.component.json",
    "contracts/artifact-classes.contract.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-contracts/resource-envelope.schema.json",
    "contracts/artifact-contracts/provenance-receipt.schema.json",
    "contracts/artifact-contracts/decision-receipt.schema.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-PROFILE-001",
    "DEC-HW-001",
    "DEC-CONTAINER-001",
    "DEC-K8S-001",
    "DEC-DEV-001",
    "DEC-DEV-002",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-SYS-RG-001",
    "REQ-SYS-RG-002",
    "REQ-SYS-RG-003",
    "REQ-SYS-RG-004",
    "REQ-SYS-RG-005",
    "REQ-SYS-RG-006",
    "REQ-SYS-RG-007",
    "REQ-SYS-RG-008",
    "REQ-SYS-RG-009",
    "REQ-SYS-RG-010",
    "REQ-SYS-RG-011",
    "REQ-SYS-RG-012",
    "REQ-SYS-RG-013",
    "REQ-SYS-RG-014",
    "REQ-SYS-RG-015",
    "REQ-SYS-RG-016",
    "REQ-SYS-RG-017",
    "REQ-SYS-RG-018",
    "REQ-SYS-RG-019",
    "REQ-SYS-RG-020",
    "REQ-SYS-RG-021",
    "REQ-LIFE-REL-001",
    "REQ-LIFE-REL-002",
    "REQ-LIFE-REL-003",
    "REQ-LIFE-REL-005",
    "REQ-LIFE-REL-006",
    "REQ-LIFE-REL-010",
    "REQ-LIFE-REL-012",
    "REQ-LIFE-REL-016",
    "REQ-LIFE-REL-019",
    "REQ-LIFE-REL-022",
    "REQ-LIFE-REL-025",
    "REQ-LIFE-REL-026",
    "REQ-LIFE-VERIFY-001",
    "REQ-LIFE-VERIFY-002",
    "REQ-LIFE-VERIFY-003",
    "REQ-LIFE-VERIFY-005",
    "REQ-LIFE-VERIFY-006",
    "REQ-LIFE-VERIFY-007",
    "REQ-LIFE-VERIFY-010",
    "REQ-LIFE-VERIFY-012",
    "REQ-LIFE-VERIFY-013",
    "REQ-LIFE-VERIFY-016",
    "REQ-LIFE-VERIFY-018",
    "REQ-LIFE-VERIFY-019",
    "REQ-LIFE-VERIFY-020",
    "REQ-LIFE-VERIFY-023",
    "REQ-LIFE-VERIFY-024",
    "REQ-LIFE-VERIFY-025",
    "REQ-LIFE-VERIFY-026",
    "REQ-LIFE-VERIFY-027",
    "REQ-OPS-OBS-024",
    "REQ-OPS-OBS-025",
    "REQ-OPS-OBS-026",
    "REQ-OPS-INC-014",
    "REQ-OPS-INC-016",
    "REQ-OPS-INC-023",
    "REQ-OPS-INC-026"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-DEV-001",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-IMPL-001",
    "LOCK-DOC-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-005",
    "DOC-SYS-014",
    "DOC-PROFILE-001",
    "DOC-LIFE-002",
    "DOC-LIFE-012",
    "DOC-SEC-004",
    "DOC-SEC-015",
    "DOC-OPS-001",
    "DOC-OPS-012",
    "DOC-CONF-002",
    "DOC-CONF-007"
  ],
  "tags": [
    "recipe",
    "build-farm",
    "reproducible-build",
    "clean-worker",
    "oci",
    "network-isolation",
    "artifact-cache",
    "provenance",
    "sbom",
    "supply-chain"
  ],
  "normative": false
}
KOA:DOC-META:END -->

# Reproducible Build-Farm Worker

> **Recipe status:** Non-normative implementation guidance.
> The active build-farm profile, toolchain, artifact, release, resource, security, test, and evidence contracts take precedence.

## 1. Purpose

This recipe shows one implementation of a clean reproducible worker for the `build_farm` profile.

The worker:

- runs each build in a new OCI container;
- uses an image pinned by digest;
- receives source and dependencies as immutable verified inputs;
- has no network during the build phase;
- has no release-signing key or production credential;
- uses bounded CPU, memory, input-output, process, temporary-storage, queue, retry, and duration controls;
- writes only to a job-specific output directory;
- emits payload digests, an SBOM, provenance, logs, and resource evidence;
- verifies reproducibility through an independent second build when the artifact contract requires it;
- removes all writable worker state before reuse.

The recipe separates fetching, building, verification, signing, publication, and activation. A successful build does not authorize a release or activate an artifact.

## 2. Applicability and Preconditions

Use this recipe when:

- the active primary profile is `build_farm`;
- the host meets the profile-owned hardware envelope;
- an OCI-compatible runtime is installed;
- rootless Podman is permitted by the local toolchain contract;
- an artifact cache is available;
- worker images and build inputs can be addressed by immutable digests;
- the source commit and lockfiles are available;
- the artifact class and release channel are registered;
- Resource Governor admission is available;
- sufficient temporary and evidence storage is available;
- the build can complete without network access after input hydration.

The retained build-farm envelope includes:

`text
CPU: 16 cores minimum
RAM: 64 GiB minimum
Storage: 2 TB SSD minimum
Artifact cache: required
Reproducible clean workers: required
`

The active profile contract remains the owner of these values.

This recipe does not cover:

- release-key custody;
- artifact signing;
- release publication;
- target activation;
- online dependency resolution during the build phase;
- privileged containers;
- mutable shared dependency environments;
- unbounded caches;
- unverified reuse of a previous job directory;
- one universal build command for every artifact class.

Kubernetes is permitted for a build farm but is not required by this recipe.

## 3. Worker Model and Directory Layout

### 3.1 Separation of phases

The implementation uses these phases:

| Phase | Network | Writable state | Authority |
| --- | --- | --- | --- |
| Request validation | Local control interfaces only | Request record | Build scheduler |
| Input hydration | Restricted fetcher network | Content-addressed cache | Input fetcher |
| Worker build | Disabled | Job output and temporary files | Build worker |
| Reproducibility check | Disabled | Independent second output | Reproducibility verifier |
| Artifact verification | Disabled or contract-declared | Verification receipts | Artifact verifier |
| Signing | Separate protected service | Signing receipts | Release signing authority |
| Publication | Release-channel interface | Publication records | Channel authority |
| Activation | Target owner interface | Target active state | Component or lifecycle owner |

The build worker never receives release-signing keys or target activation credentials.

### 3.2 Host directories

This recipe uses:

`text
/var/lib/koa/build-farm/
├── requests/
├── jobs/
├── source-cache/
├── dependency-cache/
├── worker-images/
├── outputs/
├── receipts/
├── evidence/
├── rejected/
└── locks/
`

The caches are content-addressed and treated as immutable after admission.

Each job uses:

`text
jobs/<build_id>/
├── request/
├── source/
├── dependencies/
├── work/
├── output-a/
├── output-b/
├── logs/
└── evidence/
`

No job mounts another job's writable directory.

### 3.3 Build request

The active request contract owns exact fields. The recipe expects at least:

- build identity;
- source repository and commit;
- source-tree digest;
- artifact class;
- release channel;
- target profiles and platforms;
- worker image reference pinned by digest;
- toolchain and lockfile identities;
- dependency-cache manifest;
- resource envelope;
- build command or registered build adapter;
- reproducibility policy;
- expected output paths;
- required SBOM and provenance formats.

## 4. Prepare the Host and Build Service Account

Create a dedicated unprivileged account according to the host identity-management policy.

Example directory preparation:

`bash
set -euo pipefail

BUILD_ROOT="/var/lib/koa/build-farm"

sudo install -d -o root -g koa-build -m 0750 \
 "$BUILD_ROOT" \
 "$BUILD_ROOT/requests" \
 "$BUILD_ROOT/jobs" \
 "$BUILD_ROOT/source-cache" \
 "$BUILD_ROOT/dependency-cache" \
 "$BUILD_ROOT/worker-images" \
 "$BUILD_ROOT/outputs" \
 "$BUILD_ROOT/receipts" \
 "$BUILD_ROOT/evidence" \
 "$BUILD_ROOT/rejected" \
 "$BUILD_ROOT/locks"
`

Confirm rootless OCI operation for the build account:

`bash
BUILD_UID="$(
 id -u koa-build
)"

sudo loginctl enable-linger koa-build

sudo -u koa-build \
 env "XDG_RUNTIME_DIR=/run/user/$BUILD_UID" \
 podman info >/dev/null

sudo -u koa-build \
 env "XDG_RUNTIME_DIR=/run/user/$BUILD_UID" \
 podman unshare true
`

Confirm cgroup v2 and required controllers:

`bash
test "$(
 stat -fc '%T' /sys/fs/cgroup
)" = "cgroup2fs"

cat /sys/fs/cgroup/cgroup.controllers
`

Do not grant the build account:

- passwordless unrestricted `sudo`;
- access to release-signing devices or sockets;
- production secrets;
- container-runtime administrator sockets;
- host-network privileges;
- target activation credentials;
- write access to canonical source repositories;
- write access to admitted content-addressed cache objects.

## 5. Validate the Request and Hydrate Immutable Inputs

### 5.1 Validate request identity and ownership

Assume the scheduler placed a validated request at:

`text
/var/lib/koa/build-farm/requests/<build_id>.json
`

Load the exact build identity:

`bash
set -euo pipefail

REQUEST_FILE="${1:?usage: worker request.json}"

test -r "$REQUEST_FILE"

BUILD_ID="$(
 jq -er '.build_id' "$REQUEST_FILE"
)"

SOURCE_REPOSITORY="$(
 jq -er '.source.repository_path' "$REQUEST_FILE"
)"

SOURCE_COMMIT="$(
 jq -er '.source.commit' "$REQUEST_FILE"
)"

SOURCE_TREE_DIGEST="$(
 jq -er '.source.tree_digest' "$REQUEST_FILE"
)"

WORKER_IMAGE="$(
 jq -er '.worker.image_reference' "$REQUEST_FILE"
)"

ARTIFACT_CLASS="$(
 jq -er '.output.artifact_class' "$REQUEST_FILE"
)"

RELEASE_CHANNEL="$(
 jq -er '.output.release_channel' "$REQUEST_FILE"
)"

case "$WORKER_IMAGE" in
 *@sha256:*) ;;
 *)
 printf '%s\n' \
 "Worker image is not pinned by sha256 digest." >&2
 exit 65
 ;;
esac
`

Reject a request when:

- its identity is duplicated or active already;
- the artifact class is unknown;
- the release channel does not match the artifact class;
- the source commit is unresolved;
- the source-tree digest differs;
- the worker image is not approved for the artifact class and profile;
- the resource envelope is absent or exceeds worker capacity;
- the build adapter is unknown;
- required tests or evidence are unresolved.

### 5.2 Create a clean job directory

`bash
JOB_DIR="$BUILD_ROOT/jobs/$BUILD_ID"
JOB_LOCK="$BUILD_ROOT/locks/$BUILD_ID.lock"

exec 9>"$JOB_LOCK"

if ! flock -n 9; then
 printf '%s\n' "Build is already active." >&2
 exit 75
fi

if [ -e "$JOB_DIR" ]; then
 printf '%s\n' \
 "A pre-existing job directory requires explicit disposition." >&2
 exit 65
fi

sudo install -d -o koa-build -g koa-build -m 0750 \
 "$JOB_DIR" \
 "$JOB_DIR/request" \
 "$JOB_DIR/source" \
 "$JOB_DIR/dependencies" \
 "$JOB_DIR/work" \
 "$JOB_DIR/output-a" \
 "$JOB_DIR/output-b" \
 "$JOB_DIR/logs" \
 "$JOB_DIR/evidence"

sudo install -o koa-build -g koa-build -m 0640 \
 "$REQUEST_FILE" \
 "$JOB_DIR/request/build-request.json"
`

### 5.3 Materialize source from an exact commit

Create the source archive from the local admitted source repository:

`bash
test -d "$SOURCE_REPOSITORY/.git" ||
 git -C "$SOURCE_REPOSITORY" rev-parse --git-dir >/dev/null

git -C "$SOURCE_REPOSITORY" \
 cat-file -e "${SOURCE_COMMIT}^{commit}"

SOURCE_DATE_EPOCH="$(
 git -C "$SOURCE_REPOSITORY" \
 show -s --format=%ct "$SOURCE_COMMIT"
)"

ACTUAL_TREE_DIGEST="$(
 git -C "$SOURCE_REPOSITORY" \
 rev-parse "${SOURCE_COMMIT}^{tree}"
)"

test "$ACTUAL_TREE_DIGEST" = "$SOURCE_TREE_DIGEST"

sudo -u koa-build \
 git -C "$SOURCE_REPOSITORY" \
 archive \
 --format=tar \
 --prefix=src/ \
 "$SOURCE_COMMIT" |
 sudo -u koa-build \
 tar -xf - -C "$JOB_DIR/source"
`

The build source contains no untracked file, developer-local configuration, branch worktree state, or mutable `.git` directory.

### 5.4 Hydrate dependencies through a separate fetcher

The input fetcher resolves the lockfiles and creates a content-addressed dependency bundle before the worker starts.

Example adapter:

`bash
INPUT_FETCHER="/usr/libexec/koa/build-farm/fetch-build-inputs"

test -x "$INPUT_FETCHER"

sudo -u koa-build \
 "$INPUT_FETCHER" \
 --request "$JOB_DIR/request/build-request.json" \
 --source "$JOB_DIR/source/src" \
 --cache-root "$BUILD_ROOT/dependency-cache" \
 --materialize "$JOB_DIR/dependencies" \
 --receipt-dir "$BUILD_ROOT/receipts"
`

The fetcher:

- uses only approved repositories and mirrors;
- verifies every lockfile, package identity, digest, signature, and provenance required by the toolchain;
- records misses, downloads, and cache admissions;
- writes new objects atomically;
- never modifies an admitted cache object;
- produces an input receipt.

After hydration, make inputs read only:

`bash
sudo chmod -R a-w "$JOB_DIR/source" "$JOB_DIR/dependencies"
`

A dependency cache improves performance but does not replace lockfiles, verification, or provenance.

## 6. Run the Network-Isolated Worker

### 6.1 Resolve resource limits

Example request fields:

`bash
BUILD_CPUS="$(
 jq -er '.resources.cpus' \
 "$JOB_DIR/request/build-request.json"
)"

BUILD_MEMORY="$(
 jq -er '.resources.memory' \
 "$JOB_DIR/request/build-request.json"
)"

BUILD_PIDS="$(
 jq -er '.resources.pids' \
 "$JOB_DIR/request/build-request.json"
)"

BUILD_TMPFS="$(
 jq -er '.resources.temporary_storage' \
 "$JOB_DIR/request/build-request.json"
)"
`

Validate these values against the active Resource Governor decision before using them.

### 6.2 Prepare a minimal deterministic environment

`bash
BUILD_ENV_FILE="$JOB_DIR/request/build.env"

sudo -u koa-build \
 env -i \
 LC_ALL=C.UTF-8 \
 LANG=C.UTF-8 \
 TZ=UTC \
 SOURCE_DATE_EPOCH="$SOURCE_DATE_EPOCH" \
 PYTHONHASHSEED=0 \
 ZERO_AR_DATE=1 \
 umask 022 \
 sh -c '
 umask 022
 {
 printf "LC_ALL=C.UTF-8\n"
 printf "LANG=C.UTF-8\n"
 printf "TZ=UTC\n"
 printf "SOURCE_DATE_EPOCH=%s\n" "$SOURCE_DATE_EPOCH"
 printf "PYTHONHASHSEED=0\n"
 printf "ZERO_AR_DATE=1\n"
 printf "HOME=/work/home\n"
 printf "TMPDIR=/work/tmp\n"
 printf "XDG_CACHE_HOME=/work/cache\n"
 } > "$BUILD_ENV_FILE"
 '
`

No general host environment file is passed into the worker.

### 6.3 Run build A

`bash
BUILD_ADAPTER="$(
 jq -er '.worker.build_adapter' \
 "$JOB_DIR/request/build-request.json"
)"

CONTAINER_NAME="${BUILD_ID}-a"

sudo -u koa-build \
 env "XDG_RUNTIME_DIR=/run/user/$BUILD_UID" \
 podman run \
 --rm \
 --name "$CONTAINER_NAME" \
 --network none \
 --read-only \
 --cap-drop all \
 --security-opt no-new-privileges \
 --pids-limit "$BUILD_PIDS" \
 --cpus "$BUILD_CPUS" \
 --memory "$BUILD_MEMORY" \
 --memory-swap "$BUILD_MEMORY" \
 --env-file "$BUILD_ENV_FILE" \
 --tmpfs "/work/home:rw,nosuid,nodev,size=256m" \
 --tmpfs "/work/tmp:rw,nosuid,nodev,size=$BUILD_TMPFS" \
 --tmpfs "/work/cache:rw,nosuid,nodev,size=1g" \
 --volume "$JOB_DIR/source/src:/work/src:ro,z" \
 --volume "$JOB_DIR/dependencies:/work/dependencies:ro,z" \
 --volume "$JOB_DIR/request:/work/request:ro,z" \
 --volume "$JOB_DIR/output-a:/work/output:rw,z" \
 --workdir /work/src \
 --label "io.koa.build_id=$BUILD_ID" \
 --label "io.koa.artifact_class=$ARTIFACT_CLASS" \
 --label "io.koa.release_channel=$RELEASE_CHANNEL" \
 "$WORKER_IMAGE" \
 "$BUILD_ADAPTER" \
 --request /work/request/build-request.json \
 --dependencies /work/dependencies \
 --output /work/output \
 >"$JOB_DIR/logs/build-a.stdout" \
 2>"$JOB_DIR/logs/build-a.stderr"
`

The worker has:

- no network;
- no writable source or dependency cache;
- no host runtime socket;
- no release key;
- no production credential;
- no host device;
- no privileged capability;
- no access to another job's directory.

### 6.4 Record output digests

The artifact contract identifies which files constitute reproducible payload and which are non-reproducible receipts.

Example payload manifest:

`bash
PAYLOAD_LIST="$(
 jq -er '.output.reproducible_paths[]' \
 "$JOB_DIR/request/build-request.json"
)"

: > "$JOB_DIR/evidence/build-a.manifest.sha256"

while IFS= read -r relative_path; do
 test -f "$JOB_DIR/output-a/$relative_path"

 (
 cd "$JOB_DIR/output-a"
 sha256sum -- "$relative_path"
 ) >> "$JOB_DIR/evidence/build-a.manifest.sha256"
done <<EOF
$PAYLOAD_LIST
EOF

LC_ALL=C sort -o \
 "$JOB_DIR/evidence/build-a.manifest.sha256" \
 "$JOB_DIR/evidence/build-a.manifest.sha256"
`

Do not include build receipts containing execution times or worker identities in the payload-equivalence manifest unless their contract defines a reproducible representation.

## 7. Perform an Independent Reproducibility Build

### 7.1 Reset writable state

Build B uses a new container and separate writable directories.

`bash
sudo rm -rf \
 "$JOB_DIR/work/build-b" \
 "$JOB_DIR/output-b"

sudo install -d -o koa-build -g koa-build -m 0750 \
 "$JOB_DIR/work/build-b" \
 "$JOB_DIR/output-b"
`

### 7.2 Run build B

Run the same pinned worker, source, dependencies, request, environment, and resource envelope with a different container identity:

`bash
CONTAINER_NAME="${BUILD_ID}-b"

sudo -u koa-build \
 env "XDG_RUNTIME_DIR=/run/user/$BUILD_UID" \
 podman run \
 --rm \
 --name "$CONTAINER_NAME" \
 --network none \
 --read-only \
 --cap-drop all \
 --security-opt no-new-privileges \
 --pids-limit "$BUILD_PIDS" \
 --cpus "$BUILD_CPUS" \
 --memory "$BUILD_MEMORY" \
 --memory-swap "$BUILD_MEMORY" \
 --env-file "$BUILD_ENV_FILE" \
 --tmpfs "/work/home:rw,nosuid,nodev,size=256m" \
 --tmpfs "/work/tmp:rw,nosuid,nodev,size=$BUILD_TMPFS" \
 --tmpfs "/work/cache:rw,nosuid,nodev,size=1g" \
 --volume "$JOB_DIR/source/src:/work/src:ro,z" \
 --volume "$JOB_DIR/dependencies:/work/dependencies:ro,z" \
 --volume "$JOB_DIR/request:/work/request:ro,z" \
 --volume "$JOB_DIR/output-b:/work/output:rw,z" \
 --workdir /work/src \
 --label "io.koa.build_id=$BUILD_ID" \
 --label "io.koa.reproducibility_run=b" \
 "$WORKER_IMAGE" \
 "$BUILD_ADAPTER" \
 --request /work/request/build-request.json \
 --dependencies /work/dependencies \
 --output /work/output \
 >"$JOB_DIR/logs/build-b.stdout" \
 2>"$JOB_DIR/logs/build-b.stderr"
`

### 7.3 Compare payloads

`bash
: > "$JOB_DIR/evidence/build-b.manifest.sha256"

while IFS= read -r relative_path; do
 test -f "$JOB_DIR/output-b/$relative_path"

 (
 cd "$JOB_DIR/output-b"
 sha256sum -- "$relative_path"
 ) >> "$JOB_DIR/evidence/build-b.manifest.sha256"
done <<EOF
$PAYLOAD_LIST
EOF

LC_ALL=C sort -o \
 "$JOB_DIR/evidence/build-b.manifest.sha256" \
 "$JOB_DIR/evidence/build-b.manifest.sha256"

diff -u \
 "$JOB_DIR/evidence/build-a.manifest.sha256" \
 "$JOB_DIR/evidence/build-b.manifest.sha256" \
 > "$JOB_DIR/evidence/reproducibility.diff"
`

A zero-length diff supports payload reproducibility for the exact inputs and environment.

When payloads differ:

- keep both output sets quarantined;
- record the differing paths and digests;
- use a contract-approved binary-difference tool;
- do not choose one output by convenience;
- do not sign or publish either output;
- open an investigation when required.

Cross-worker or cross-host reproduction can be required by the artifact class or high-assurance composition. This recipe's two local clean runs do not replace that stronger requirement.

## 8. Generate SBOM, Provenance, and Verification Evidence

### 8.1 Generate an SBOM

Use the registered SBOM generator:

`bash
SBOM_GENERATOR="/usr/libexec/koa/build-farm/generate-sbom"

test -x "$SBOM_GENERATOR"

sudo -u koa-build \
 "$SBOM_GENERATOR" \
 --request "$JOB_DIR/request/build-request.json" \
 --source "$JOB_DIR/source/src" \
 --dependencies "$JOB_DIR/dependencies" \
 --artifacts "$JOB_DIR/output-a" \
 --output "$JOB_DIR/evidence/sbom.json"
`

The SBOM belongs to the exact output and records its generator identity and version.

### 8.2 Generate provenance

`bash
PROVENANCE_GENERATOR="/usr/libexec/koa/build-farm/generate-provenance"

test -x "$PROVENANCE_GENERATOR"

sudo -u koa-build \
 "$PROVENANCE_GENERATOR" \
 --request "$JOB_DIR/request/build-request.json" \
 --worker-image "$WORKER_IMAGE" \
 --source-commit "$SOURCE_COMMIT" \
 --source-tree "$SOURCE_TREE_DIGEST" \
 --source-date-epoch "$SOURCE_DATE_EPOCH" \
 --input-receipts "$BUILD_ROOT/receipts" \
 --payload-manifest "$JOB_DIR/evidence/build-a.manifest.sha256" \
 --reproducibility-manifest "$JOB_DIR/evidence/build-b.manifest.sha256" \
 --network-mode none \
 --resource-envelope "$JOB_DIR/request/build-request.json" \
 --output "$JOB_DIR/evidence/provenance.json"
`

Provenance identifies:

- build request;
- source commit and tree;
- lockfiles and dependency digests;
- worker image digest;
- toolchain identities;
- build adapter;
- deterministic environment;
- network state;
- resource envelope;
- payload digests;
- SBOM;
- reproducibility result;
- worker and scheduler identities as permitted;
- time and custody.

### 8.3 Run artifact verification

`bash
ARTIFACT_VERIFIER="/usr/libexec/koa/verify-build-output"

test -x "$ARTIFACT_VERIFIER"

VERIFICATION_RECEIPT="$(
 sudo -u koa-build \
 "$ARTIFACT_VERIFIER" \
 --request "$JOB_DIR/request/build-request.json" \
 --artifacts "$JOB_DIR/output-a" \
 --sbom "$JOB_DIR/evidence/sbom.json" \
 --provenance "$JOB_DIR/evidence/provenance.json" \
 --reproducibility-diff \
 "$JOB_DIR/evidence/reproducibility.diff" \
 --receipt-dir "$BUILD_ROOT/receipts"
)"
`

Verification covers identity, artifact class, release channel, integrity, provenance, target, profile, compatibility, policy, class-specific checks, and evidence completeness.

A build receipt is not a signature, publication authorization, or activation decision.

## 9. Transfer Outputs to Signing and Publication Authorities

Only verified output leaves the worker boundary.

Create a read-only candidate directory:

`bash
CANDIDATE_DIR="$BUILD_ROOT/outputs/$BUILD_ID"

sudo install -d -o root -g koa-release -m 0750 \
 "$CANDIDATE_DIR"

sudo cp -a \
 --no-preserve=ownership \
 "$JOB_DIR/output-a/." \
 "$CANDIDATE_DIR/"

sudo install -o root -g koa-release -m 0640 \
 "$JOB_DIR/evidence/sbom.json" \
 "$JOB_DIR/evidence/provenance.json" \
 "$JOB_DIR/evidence/build-a.manifest.sha256" \
 "$JOB_DIR/evidence/build-b.manifest.sha256" \
 "$JOB_DIR/evidence/reproducibility.diff" \
 "$CANDIDATE_DIR/"

sudo find "$CANDIDATE_DIR" -type d -exec chmod 0750 {} +
sudo find "$CANDIDATE_DIR" -type f -exec chmod 0640 {} +
sudo chmod -R a-w "$CANDIDATE_DIR"
`

Submit the candidate through the protected signing or release interface:

`bash
/usr/libexec/koa/submit-release-candidate \
 --build-id "$BUILD_ID" \
 --candidate "$CANDIDATE_DIR" \
 --verification-receipt "$VERIFICATION_RECEIPT"
`

The signing authority independently verifies:

- candidate identity and digests;
- artifact class and release channel;
- provenance and SBOM;
- reproducibility outcome;
- signer authorization;
- policy and approval;
- target profiles;
- release compatibility;
- required evidence.

The worker never reads or controls the release private key.

Publication and Release Set creation remain separate from signing. Target activation remains separate from publication.

## 10. Failure Handling and Clean-Worker Reset

### 10.1 Failure behavior

| Condition | Response |
| --- | --- |
| Request identity is duplicated | Keep the new request blocked. |
| Worker image is not digest pinned | Reject before container creation. |
| Source commit or tree differs | Reject and preserve source-resolution evidence. |
| Lockfile or dependency verification fails | Reject hydration and do not start the worker. |
| Cache object changes after admission | Quarantine the cache object and affected builds. |
| Build attempts network access | The request fails because the worker has no network; investigate the undeclared dependency. |
| Resource limit is reached | Stop or fail the job and preserve bounded evidence. |
| Output path escapes the job directory | Reject the build and investigate the worker image or adapter. |
| Build A fails | Do not run signing or publication. |
| Build B differs | Quarantine both output sets. |
| SBOM or provenance generation fails | Keep the candidate blocked. |
| Artifact verification fails or is blocked | Keep output quarantined. |
| Signing service is unavailable | Preserve the verified unsigned candidate; do not expose a signing key to the worker. |
| Evidence custody is unavailable | Apply the artifact contract's fail or bounded-queue behavior. |
| Worker compromise is suspected | Preserve evidence, remove the worker from service, invalidate affected reusable results, and enter incident response. |

### 10.2 Preserve required evidence

Before cleanup, transfer required logs and evidence:

`bash
EVIDENCE_DIR="$BUILD_ROOT/evidence/$BUILD_ID"

sudo install -d -o root -g koa-audit -m 0750 \
 "$EVIDENCE_DIR"

sudo cp -a \
 --no-preserve=ownership \
 "$JOB_DIR/evidence/." \
 "$EVIDENCE_DIR/"

sudo cp -a \
 --no-preserve=ownership \
 "$JOB_DIR/logs/." \
 "$EVIDENCE_DIR/logs/"

sudo find "$EVIDENCE_DIR" -type d -exec chmod 0750 {} +
sudo find "$EVIDENCE_DIR" -type f -exec chmod 0640 {} +
`

Review logs for secrets, credentials, restricted source, personal data, and excessive content before wider disclosure.

### 10.3 Remove writable job state

`bash
sudo -u koa-build \
 env "XDG_RUNTIME_DIR=/run/user/$BUILD_UID" \
 podman ps -aq \
 --filter "label=io.koa.build_id=$BUILD_ID" |
 xargs -r \
 sudo -u koa-build \
 env "XDG_RUNTIME_DIR=/run/user/$BUILD_UID" \
 podman rm -f

sudo rm -rf --one-file-system "$JOB_DIR"
`

Verify no job-specific writable state remains:

`bash
test ! -e "$JOB_DIR"

sudo -u koa-build \
 env "XDG_RUNTIME_DIR=/run/user/$BUILD_UID" \
 podman ps -a \
 --filter "label=io.koa.build_id=$BUILD_ID"
`

Do not prune the complete shared image or dependency cache as part of ordinary job cleanup. Cache retention and garbage collection use a separate content-addressed policy that preserves objects referenced by active or retained evidence.

### 10.4 Worker health after reset

A worker returns to the ready pool only after validation confirms:

- no job container remains;
- no writable job directory remains;
- no unexpected mount remains;
- disk and inode reserves remain above thresholds;
- cache integrity remains valid;
- cgroup limits are available;
- runtime health is valid;
- no incident hold is active.

## 11. Validation and Adaptation Checklist

Before adopting or changing this recipe, confirm:

- `build_farm` is the active primary profile;
- the host meets the profile-owned CPU, memory, storage, artifact-cache, and clean-worker requirements;
- the OCI runtime and worker image are approved;
- the worker image is pinned by digest;
- every build request identifies source, artifact class, release channel, target, toolchain, resources, outputs, tests, and evidence;
- source input is an exact commit and tree;
- untracked developer files never enter the worker;
- dependencies are selected by lockfiles and verified before admission;
- the content-addressed artifact cache is required, bounded, immutable after admission, and garbage-collected through a separate policy;
- fetching and building are separate phases;
- the build phase has no network;
- source and dependency inputs are read only;
- every job receives new writable directories and a new container;
- no runtime socket, host device, production credential, activation credential, or signing key enters the worker;
- environment variables, locale, timezone, timestamps, archive behavior, and file ordering are deterministic;
- CPU, memory, input-output, process, temporary-storage, queue, retry, and duration bounds are enforced;
- payload files are distinguished from time-varying receipts;
- a second independent clean build is performed when required;
- differing outputs remain quarantined;
- SBOM and provenance identify exact inputs, tools, environment, resources, outputs, and reproducibility results;
- artifact verification precedes submission to signing;
- signing, publication, Release Set creation, and activation remain separate authorities;
- every critical transition produces a receipt;
- evidence is retained without leaking secrets or restricted source;
- job cleanup removes all writable worker state;
- cache cleanup cannot remove evidence-referenced objects;
- compromised workers and affected reusable results enter incident response;
- tests and evidence apply to the exact request, source, worker image, dependencies, resources, artifact, channel, target, and verifier versions.

An adaptation is ready only after clean validation confirms reproducibility, isolation, resource bounds, provenance, artifact verification, evidence custody, and complete worker reset.
