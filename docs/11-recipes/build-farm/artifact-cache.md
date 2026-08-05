<!-- KOA:DOC-META:BEGIN GENERATED
{
 "doc_id": "RECIPE-BUILD-FARM-001",
 "document_class": "non_normative_recipe",
 "status": "active",
 "language": "en",
 "layer": "recipes",
 "scope": [
 "build_farm"
 ],
 "canonical_refs": [
 "generated/authority-manifest.json",
 "generated/decision-index.json",
 "contracts/system.contract.json#/development_model",
 "contracts/system.contract.json#/resource_model",
 "generated/component-catalog.json",
 "contracts/profiles/build-farm.profile.json",
 "generated/profile-catalog.json",
 "contracts/toolchains/python-uv.toolchain.json",
 "contracts/artifact-classes.contract.json",
 "contracts/release-channels.contract.json",
 "contracts/integration-types.contract.json",
 "generated/requirements-index.json",
 "generated/assertion-index.json",
 "generated/traceability.json",
 "generated/test-catalog.json",
 "generated/evidence-catalog.json",
 "generated/exception-index.json"
 ],
 "decision_ids": [
 "DEC-PROFILE-BUILD-FARM-001",
 "DEC-DEV-001",
 "DEC-SYS-RESOURCE-001",
 "DEC-SYS-COMP-001",
 "DEC-LIFE-001",
 "DEC-REL-001"
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
 "REQ-DEV-PAR-040",
 "REQ-CONF-GATE-010",
 "REQ-CONF-GATE-011",
 "REQ-CONF-GATE-012",
 "REQ-CONF-GATE-016",
 "REQ-CONF-GATE-018"
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
 "LOCK-LIFE-001",
 "LOCK-LIFE-002",
 "LOCK-LIFE-003",
 "LOCK-LIFE-004",
 "LOCK-OPS-001",
 "LOCK-OPS-002",
 "LOCK-OPS-003",
 "LOCK-OPS-004"
 ],
 "exception_ids": [],
 "depends_on": [
 "DOC-DEV-000",
 "DOC-DEV-010",
 "DOC-PROFILE-001",
 "DOC-PROFILE-002",
 "DOC-COMP-001",
 "DOC-LIFE-003",
 "DOC-LIFE-013",
 "DOC-SEC-005",
 "DOC-SEC-016",
 "DOC-OPS-003",
 "DOC-OPS-013",
 "DOC-CONF-003",
 "DOC-CONF-019"
 ],
 "tags": [
 "recipe",
 "build-farm",
 "artifact-cache",
 "content-addressed",
 "cache-poisoning",
 "provenance",
 "immutable-keys",
 "eviction",
 "offline-build",
 "reproducibility",
 "safe-cleanup"
 ]
}
KOA:DOC-META:END -->

# Artifact Cache

## 1. Purpose

This recipe shows one practical artifact-cache layout for a kOA build farm.

The cache accelerates repeatable work while remaining disposable and non-authoritative.

It can store:

- verified dependency blobs;
- source-package mirrors;
- compiler outputs;
- container layers;
- generated intermediates;
- test fixtures;
- deterministic indexes;
- candidate build objects;
- validated reusable test results when equivalence is exact.

It does not replace:

- canonical source control;
- dependency lock files;
- the artifact repository;
- provenance records;
- the evidence registry;
- release-channel manifests;
- Release Set signatures;
- backup and recovery artifacts;
- component-owned authoritative state.

The target result is:

`text
exact input identity
+ deterministic cache key
+ isolated namespace
+ verified cache object
+ bounded reuse
+ attributable hit or miss
+ safe eviction
+ clean rebuild on loss
`

This recipe is non-normative. The build-farm profile, artifact contracts, toolchain contracts, component contracts, release-channel registry, and release gates remain authoritative.

## 2. Cache Classes and Trust Zones

### 2.1 Recommended cache classes

Use separate namespaces for different trust and lifecycle properties.

| Cache class | Typical content | Reuse boundary |
| --- | --- | --- |
| `dependency_blob` | Immutable package archives, wheels, source distributions, OS packages | Exact package identity and verified content |
| `source_mirror` | Verified repository objects or source archives | Exact source object identity |
| `toolchain_blob` | Compilers, interpreters, build tools, base images | Exact toolchain artifact identity |
| `build_intermediate` | Object files, generated code, compiled modules | Exact build-input and environment identity |
| `container_layer` | OCI-compatible build layers | Exact layer and build context identity |
| `test_fixture` | Immutable generated or approved fixture artifacts | Exact fixture contract and version |
| `test_result` | Reusable deterministic test output | Exact test, environment, input, and validity identity |
| `candidate_artifact` | Non-authoritative build candidate | Exact build invocation and provenance identity |
| `index_snapshot` | Regenerable dependency or artifact index | Exact source set and generator identity |

Do not combine all classes into one anonymous directory.

### 2.2 Trust zones

A practical build-farm design uses:

`text
bootstrap_read_only
worker_local
shared_verified
quarantine
`

`bootstrap_read_only` contains preloaded objects admitted during image or node provisioning.

`worker_local` is writable by one worker identity and disposable with that worker.

`shared_verified` accepts only objects that pass the shared-cache admission path.

`quarantine` holds malformed, mismatched, suspicious, or incompletely verified objects.

A worker does not promote its own local object by moving it directly into `shared_verified`.

### 2.3 Candidate versus accepted artifacts

A cached candidate remains a candidate.

Copying a candidate from cache does not:

- publish it to a release channel;
- sign it;
- approve it;
- make it immutable authority;
- establish profile conformance;
- establish deployment readiness.

Accepted release artifacts belong in the registered artifact repository or release store.

The cache can retain a copy for acceleration, but the repository remains the distribution and lifecycle authority.

## 3. Directory and Namespace Layout

### 3.1 Example paths

A system-scoped build-farm node can use:

`text
/var/cache/koa-build/
 bootstrap/
 workers/
 <worker-id>/
 shared/
 dependency-blob/
 source-mirror/
 toolchain-blob/
 build-intermediate/
 container-layer/
 test-fixture/
 test-result/
 candidate-artifact/
 index-snapshot/
 quarantine/
 manifests/
 leases/
 receipts/
`

Suggested ownership:

| Path | Owner | Write access |
| --- | --- | --- |
| `/var/cache/koa-build/bootstrap/` | provisioning authority | read-only to workers |
| `/var/cache/koa-build/workers/<id>/` | one worker account | one worker |
| `/var/cache/koa-build/shared/` | cache service | cache service only |
| `/var/cache/koa-build/quarantine/` | cache service | cache service and security review |
| `/var/cache/koa-build/manifests/` | cache service | cache service |
| `/var/cache/koa-build/leases/` | cache service | cache service |
| `/var/cache/koa-build/receipts/` | cache service | cache service |

Build workers interact with the shared cache through a registered local API or socket.

They do not receive write permission to the shared object directory.

### 3.2 Namespace identity

Every object namespace includes applicable:

`text
cache_class
project_or_component_id
target_profile
target_platform
target_architecture
toolchain_family
toolchain_version
build_mode
trust_domain
`

Branch names are display metadata, not sufficient identity.

Two branches with different source trees cannot share a build-intermediate key merely because they have the same branch name.

### 3.3 Worker isolation

Each worker has:

- a dedicated service identity;
- one work root;
- one local cache root;
- one temporary root;
- one build invocation identity;
- bounded resource controls;
- no direct access to another worker's mutable directory.

A worker can share immutable verified objects through the cache service.

It cannot inspect or mutate another worker's in-progress build.

## 4. Construct Deterministic Cache Keys

### 4.1 Key inputs

A build-intermediate key commonly includes:

`text
cache schema version
cache class
project or component identity
source tree digest
dependency lock identity
toolchain artifact identity
compiler and linker versions
build configuration
target profile
target platform
target architecture
feature set
environment contract version
generator versions
declared input artifact digests
`

A test-result key additionally includes:

`text
test identity
test version
test configuration
fixture identities
runtime environment class
required service versions
clock or locale constraints
random-seed policy
validity policy
`

A candidate-artifact key additionally includes the output artifact class and build recipe identity.

### 4.2 Canonical key document

Build the key from a canonical JSON document.

Example:

`json
{
 "cache_schema_version": "1.0.0",
 "cache_class": "build_intermediate",
 "component_id": "publication_gateway",
 "source_tree_digest": "sha256:4ea8c6d6...",
 "dependency_lock": {
 "toolchain": "uv",
 "lockfile": "uv.lock",
 "lock_version": "1"
 },
 "toolchain": {
 "python": "3.13.5",
 "uv": "0.8.4",
 "compiler_image": "artifact://toolchains/python-build/3.13.5-2"
 },
 "target": {
 "profile": "build_farm",
 "platform": "linux",
 "architecture": "x86_64"
 },
 "build": {
 "recipe": "python-wheel-v3",
 "mode": "release",
 "features": []
 }
}
`

Serialize with:

- UTF-8;
- sorted object keys;
- no insignificant whitespace;
- canonical numeric representation;
- normalized path references;
- no host-specific absolute paths.

Derive the cache key from the canonical bytes with the content-integrity algorithm owned by the cache artifact contract.

### 4.3 Exclude unstable inputs

Do not include values that change without changing the build meaning, such as:

- worker hostname;
- process identifier;
- temporary directory;
- wall-clock start time;
- branch display name;
- CI job number;
- scheduler attempt number.

Do include them in provenance and receipts when useful.

### 4.4 Detect undeclared inputs

A cache key is safe only when all build-affecting inputs are declared.

Use sandboxing and tracing to detect:

- reads outside the workspace and toolchain roots;
- undeclared environment variables;
- host package access;
- network downloads;
- time-dependent generation;
- locale dependence;
- random input;
- mutable shared services;
- hidden configuration.

An undeclared input invalidates reuse.

### 4.5 Key-version changes

Change `cache_schema_version` when key semantics change.

Do not reinterpret old keys under a new rule.

A new version can coexist with the old namespace until eviction removes old objects.

## 5. Read and Write Workflow

### 5.1 Read order

A worker checks caches in this order:

1. worker-local verified object;
2. bootstrap read-only object;
3. shared verified object;
4. ordinary build path.

Each hit still verifies:

- cache class;
- key;
- manifest;
- object size;
- content integrity;
- schema;
- compatibility;
- quarantine or revocation state.

### 5.2 Local cache hit

A worker-local hit is usable only by the same worker trust domain unless it passes shared admission.

The worker records:

`text
cache_result: hit
cache_zone: worker_local
object_key
manifest_ref
verification_result
`

### 5.3 Shared cache hit

The cache service returns:

- immutable object bytes or a read-only object reference;
- object manifest;
- content-integrity record;
- producer provenance reference;
- admission receipt;
- compatibility metadata;
- expiry or revocation status.

The worker verifies the response before use.

### 5.4 Cache miss

A miss is a normal result.

The build runs inside the declared isolated environment.

The worker writes output to a temporary local path, validates it, and creates a candidate cache manifest.

The build does not write directly into the final cache path.

### 5.5 Shared admission

Shared admission proceeds through:

`text
candidate_received
request_authenticated
namespace_authorized
manifest_validated
key_recomputed
object_integrity_verified
artifact_class_validated
provenance_validated
malware_and_secret_checks
compatibility_validated
duplicate_checked
object_committed
admission_receipt_durable
`

Commit uses an atomic rename, object-store conditional put, or validated equivalent.

A failed admission leaves the existing shared object unchanged.

### 5.6 Duplicate key

When the key already exists:

- identical verified content returns the existing object;
- different content enters quarantine;
- the cache records a collision or nondeterminism event;
- the new object is not allowed to replace the existing object silently.

Different output for the same complete key indicates missing inputs, nondeterminism, corruption, or malicious activity.

## 6. Cache Service Example

### 6.1 Local socket

Expose a local cache service through:

`text
/run/koa/build-cache/cache.sock
`

The socket authenticates the worker identity.

Request authorization is separate from socket access.

### 6.2 Example request

`json
{
 "request_id": "cachereq_01J4H19P82R2F6X7N32JY7M8KD",
 "worker_id": "buildworker_07",
 "operation": "get",
 "cache_class": "build_intermediate",
 "object_key": "sha256:8d3164f7...",
 "target_profile": "build_farm",
 "deadline_at": "2026-08-03T20:10:00-04:00"
}
`

The operation vocabulary remains closed:

`text
get
put_candidate
verify
lease
release_lease
quarantine
`

No operation accepts an arbitrary filesystem path or shell command.

### 6.3 Example service unit

Illustrative `/usr/lib/systemd/system/koa-build-cache.service`:

`ini
[Unit]
Description=kOA build-farm artifact cache
After=local-fs.target
RequiresMountsFor=/var/cache/koa-build

[Service]
Type=notify
User=koa-build-cache
Group=koa-build-cache
ExecStart=/usr/lib/koa/active/services/build-cache/bin/build-cache serve \
 --socket /run/koa/build-cache/cache.sock
Restart=on-failure
RestartSec=5s
RuntimeDirectory=koa/build-cache
StateDirectory=koa/build-cache
CacheDirectory=koa-build
UMask=0027

NoNewPrivileges=yes
PrivateTmp=yes
PrivateDevices=yes
ProtectSystem=strict
ProtectHome=yes
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectKernelLogs=yes
ProtectControlGroups=yes
ProtectClock=yes
ProtectHostname=yes
ProtectProc=invisible
ProcSubset=pid
RestrictSUIDSGID=yes
RestrictRealtime=yes
LockPersonality=yes
RemoveIPC=yes
RestrictNamespaces=yes
RestrictAddressFamilies=AF_UNIX
CapabilityBoundingSet=
AmbientCapabilities=

ReadWritePaths=/var/cache/koa-build
ReadWritePaths=/run/koa/build-cache
ReadOnlyPaths=/etc/koa
ReadOnlyPaths=/usr/lib/koa/active
`

The active build-farm profile owns exact hardening and resource limits.

### 6.4 Worker environment

Workers receive cache references without storage credentials:

`bash
export KOA_CACHE_SOCKET="/run/koa/build-cache/cache.sock"
export KOA_CACHE_NAMESPACE="publication_gateway/linux/x86_64"
export KOA_CACHE_MODE="read-write-candidate"
`

The cache client authenticates through the local service identity or another registered mechanism.

## 7. Reproducibility and Poisoning Defense

### 7.1 Rebuild comparison

Periodically select cached objects and rebuild them from declared inputs.

Compare:

- output artifact manifest;
- content integrity;
- file list;
- normalized metadata;
- provenance;
- test result.

A mismatch removes the object from normal use and starts investigation.

### 7.2 Trusted bootstrap objects

Bootstrap objects are admitted during image or node creation.

Their manifest identifies:

- provisioning Release Set;
- source repository or artifact repository;
- signer;
- content integrity;
- target profile and platform;
- admission evidence.

Workers mount bootstrap storage read-only.

### 7.3 Dependency verification

For dependency blobs:

1. resolve only from the locked dependency identity;
2. verify package name and version;
3. verify expected content integrity where the lock or artifact contract provides it;
4. verify signature or repository trust where required;
5. reject mutable aliases;
6. store immutable bytes under the derived object key.

A cached package does not alter `uv.lock`.

Python builds still use:

`bash
uv sync --frozen
`

The cache accelerates retrieval. It does not permit dependency resolution drift.

### 7.4 Secret scanning

Before shared admission, scan candidate cache objects and manifests for:

- credentials;
- bearer tokens;
- private keys;
- signing material;
- environment files;
- local absolute paths containing sensitive identities;
- unrestricted protected evidence;
- personal or cultural-restricted data outside the artifact contract.

A detected secret quarantines the object.

Revocation and incident handling follow the owning security procedure.

### 7.5 Archive extraction

Treat archives as hostile input.

Validate:

- no path traversal;
- no absolute paths;
- no device nodes;
- no unsafe links;
- bounded file count;
- bounded expanded size;
- allowed file types;
- normalized permissions.

Extract into an isolated temporary directory.

### 7.6 Container layers

A container-layer hit still verifies:

- base image identity;
- build recipe;
- build context digest;
- target platform;
- layer integrity;
- manifest compatibility;
- signature or attestation where required.

A mutable image tag is not a complete cache key.

### 7.7 Test-result reuse

Reuse a test result only when exact equivalence is demonstrated for:

- source and dependency inputs;
- toolchain;
- environment;
- profile;
- platform and architecture;
- test definition;
- fixture set;
- service versions;
- configuration;
- validity interval.

Do not reuse results for nondeterministic, timing-sensitive, hardware-sensitive, security-sensitive, migration, recovery, or release-gate tests unless their contracts explicitly permit it.

## 8. Capacity, Leases, and Eviction

### 8.1 Resource admission

Resource Governor controls:

- total cache capacity;
- class quotas;
- worker-local quotas;
- shared-write admission;
- compaction;
- eviction work;
- I/O rate;
- memory use;
- recovery reserve.

The cache service does not consume the node's recovery reserve to preserve optional intermediates.

### 8.2 Class quotas

Example policy:

| Cache class | Relative retention |
| --- | --- |
| `dependency_blob` | High when locked and frequently reused |
| `toolchain_blob` | High for active toolchains |
| `source_mirror` | Moderate; canonical source remains elsewhere |
| `build_intermediate` | Bounded by recency and reuse |
| `container_layer` | Bounded by platform and active builds |
| `test_fixture` | Moderate when expensive to generate |
| `test_result` | Short and validity-bound |
| `candidate_artifact` | Short unless referenced by an active workflow |
| `index_snapshot` | Low because it is regenerable |

Actual quotas remain profile-owned.

### 8.3 Leases

A lease protects an object while a build uses it.

A lease includes:

`text
lease_id
object_key
worker_id
build_invocation_id
created_at
expires_at
renewal_policy
`

A crashed worker does not create a permanent lease.

Expired leases are reconciled before eviction.

### 8.4 Eviction order

Evict in this general order:

1. invalid and rejected objects after evidence preservation;
2. expired test results;
3. old index snapshots;
4. unreferenced candidate artifacts;
5. low-value build intermediates;
6. old container layers;
7. source mirrors;
8. dependency and toolchain blobs not required by active or recovery-supported builds.

Do not delete an object with an active lease.

### 8.5 Safe deletion

Deletion verifies:

- exact object key;
- cache class;
- namespace;
- current lease state;
- quarantine or evidence hold;
- artifact-repository relationship;
- active build references;
- recovery policy.

Delete by exact identity.

Do not use global wildcard deletion or filesystem-age deletion without manifest checks.

### 8.6 Cache loss

Cache loss is an availability and performance event, not loss of canonical authority.

Recovery:

1. stops shared writes if integrity is uncertain;
2. preserves manifests and receipts where available;
3. discards corrupt disposable objects;
4. recreates directories and service state;
5. reloads trusted bootstrap objects;
6. warms from canonical repositories as allowed;
7. resumes builds;
8. records performance and SLO impact.

A build that cannot run after complete cache loss has an undeclared cache dependency.

## 9. Offline and Disconnected Build Operation

### 9.1 Offline readiness

A disconnected build farm needs local verified copies of:

- source objects;
- `uv.lock`;
- Python distributions;
- locked dependency blobs;
- toolchain artifacts;
- base images;
- schemas;
- generators;
- test fixtures;
- trust material;
- revocation state;
- candidate output storage.

The cache can provide these bytes, but offline readiness is established by an approved build input bundle or repository snapshot, not by assuming the cache happens to contain them.

### 9.2 Offline bundle admission

An offline build bundle verifies:

- source;
- signer;
- trust and revocation;
- destination scope;
- profile;
- platform;
- content integrity;
- replay;
- downgrade;
- artifact classes;
- complete manifest.

Admitted objects enter `bootstrap_read_only` or `shared_verified` through the ordinary admission path.

### 9.3 Disconnected writes

Disconnected workers can write to worker-local cache.

Shared writes continue only when the local cache service and trust inputs remain available.

Remote replication becomes deferred.

### 9.4 Reconnection

On reconnection:

1. refresh trust and revocation;
2. reconcile remote repository state;
3. verify queued uploads;
4. reject revoked or superseded objects;
5. upload only authorized cache classes;
6. deduplicate by object identity;
7. preserve provenance and admission receipts.

Remote cache acceptance does not publish a release artifact.

## 10. Cleanup, Validation, and Troubleshooting

### 10.1 Inspect cache state

Example:

`bash
uv run python -m build_cache.cli stats \
 --by-class \
 --by-namespace \
 --include-leases
`

A useful report shows:

- object count;
- byte count;
- hit and miss count;
- verification failures;
- quarantine count;
- active leases;
- oldest and newest access;
- eviction candidates;
- admission denials;
- rebuild mismatches.

### 10.2 Verify one object

Example:

`bash
uv run python -m build_cache.cli verify \
 --cache-class build_intermediate \
 --object-key "sha256:8d3164f7..."
`

Verification reads the manifest and recomputes required integrity.

It does not rewrite the object on failure.

### 10.3 Evict one namespace

Example:

`bash
uv run python -m build_cache.cli evict \
 --namespace "publication_gateway/linux/x86_64" \
 --cache-class build_intermediate \
 --policy unleased-low-value
`

The command lists selected objects, checks leases, and records the result.

Do not run a recursive remove against `/var/cache/koa-build/shared`.

### 10.4 Troubleshooting matrix

| Symptom | Likely cause | Safe response |
| --- | --- | --- |
| Same key produces different bytes | Missing key input, nondeterminism, corruption, or poisoning | Quarantine both candidates, block reuse, compare complete inputs and environment |
| Cache hit fails at runtime | Compatibility or environment identity incomplete | Expand the key contract and invalidate the affected namespace |
| Dependency differs from lock | Mutable alias or missing verification | Reject the object, restore locked identity, and rebuild |
| Workers can modify shared files | Filesystem permissions bypass the cache service | Revoke direct writes and restore service-mediated admission |
| Cache fills recovery storage | Quotas or reserve enforcement missing | Stop writes, preserve recovery reserve, and evict by verified policy |
| Eviction breaks active build | Lease tracking incomplete | Reconcile the build, repair lease handling, and rerun |
| Test result hides a regression | Reuse equivalence too broad or validity too long | Disable reuse for that test class and rerun current tests |
| Cache object contains a secret | Build output or scanner boundary failed | Quarantine, revoke the secret, investigate, and correct the build |
| Offline build misses one dependency | Offline manifest incomplete | Block the build and regenerate the governed offline input bundle |
| Candidate cache is treated as release store | Lifecycle boundary collapsed | Restore repository publication, signing, and release gates |
| Worker relies on host package | Sandbox permits undeclared input | Isolate the worker and include the toolchain artifact in the build contract |
| Global cleanup removes bootstrap objects | Namespace and trust-zone selection absent | Restore from provisioning artifacts and require exact-zone deletion |

### 10.5 Validation commands

Run repository validation:

`bash
uv run python docs/tools/validate_docs.py
uv run python docs/tools/check_artifact_contracts.py
uv run python docs/tools/check_component_boundaries.py
uv run python docs/tools/check_profile_inheritance.py
uv run python docs/tools/check_release_sets.py
uv run python docs/tools/check_interfile_locks.py
uv run python docs/tools/check_traceability.py
uv run python docs/tools/check_no_unresolved_state.py
`

Run build-farm tests for:

- cold-cache build;
- warm-cache build;
- complete cache loss;
- same-key reproducibility;
- mismatched-content quarantine;
- expired lease;
- concurrent put;
- dependency verification;
- secret detection;
- archive traversal rejection;
- offline bootstrap;
- capacity pressure;
- exact-identity eviction.

## 11. Completion Checklist

The cache layout is ready when:

- [ ] cache classes and trust zones are explicit;
- [ ] workers have isolated local cache directories;
- [ ] workers cannot write shared object storage directly;
- [ ] every object has a canonical key document;
- [ ] all build-affecting inputs are represented in the key;
- [ ] unstable execution metadata is excluded from key semantics;
- [ ] cache-schema changes create a new key namespace;
- [ ] shared admission recomputes the key and verifies the object;
- [ ] identical keys with different content enter quarantine;
- [ ] dependency reuse remains bound to committed lock files;
- [ ] `uv sync --frozen` remains the Python dependency rule;
- [ ] cache objects preserve provenance and admission receipts;
- [ ] candidate cache objects remain non-authoritative;
- [ ] signing keys and secret values never enter the cache;
- [ ] archive extraction is isolated and bounded;
- [ ] test-result reuse requires exact validated equivalence;
- [ ] Resource Governor controls capacity and cache work;
- [ ] leases protect active builds and expire safely;
- [ ] eviction uses exact identities and manifest checks;
- [ ] no global wildcard deletion is part of normal operation;
- [ ] complete cache loss still permits a clean build from canonical inputs;
- [ ] offline readiness uses a governed manifest rather than accidental cache contents;
- [ ] reconnection revalidates trust, revocation, and authorization;
- [ ] release artifacts still pass repository publication, signing, evidence, and release gates;
- [ ] cold, warm, poisoned, offline, capacity, and recovery tests pass;
- [ ] the result remains a build-farm recipe rather than a release or conformance claim.
