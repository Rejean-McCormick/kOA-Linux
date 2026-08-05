<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "RECIPE-BUILD-FARM-SBOM-AND-PROVENANCE",
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
    "sbom",
    "and",
    "provenance"
  ],
  "edit_policy": "manual"
}
KOA:DOC-META:END -->

# SBOM and Provenance

> **Recipe status:** Active, non-authoritative implementation guidance.
> **Canonical boundary:** This recipe does not define artifact classes, release authority, signature formats, evidence semantics, toolchain versions, dependency policy, component ownership, or Release Set membership. Resolve those facts from the active build-farm profile, toolchain contracts, artifact contracts, release-channel registry, component contracts, test catalog, evidence registry, and release authority before executing the procedure.

## 1. Purpose

This recipe provides a cautious build-farm procedure for producing a software bill of materials and a provenance record for a candidate kOA artifact.

The procedure separates:

- source and dependency inputs;
- the clean build environment;
- the candidate output;
- the SBOM describing included components;
- the provenance record describing the build;
- test and evidence records;
- signature and verification references;
- release-authority acceptance;
- Release Set activation.

The build farm produces candidate artifacts and evidence. It does not activate releases, publish directly into an authoritative release channel, change component-owned data, or declare a candidate deployable.

The procedure supports local or mirrored operation and does not require external AI, public Internet access, a cloud build service, containers, Kubernetes, or a GPU.

## 2. Intended Result

A completed build handoff contains:

1. one stable build-run identity;
2. one clean source snapshot reference;
3. one active toolchain-contract reference;
4. one frozen dependency-resolution reference;
5. one candidate artifact identity and version;
6. one normalized SBOM;
7. one provenance record;
8. one environment record;
9. one test-evidence set;
10. one signature artifact or signing-service receipt where required;
11. one verification result;
12. one candidate handoff manifest;
13. one cleanup result;
14. no production credentials;
15. no direct release activation;
16. no ordinary file-integrity fields in kOA metadata.

The candidate remains non-authoritative until the applicable artifact, release, governance, and Release Set procedures accept it.

## 3. Safety Boundaries

Apply these boundaries throughout the procedure:

1. Run the build in a clean worker, isolated workspace, or equivalent controlled environment.
2. Bind every mutable environment to one build run.
3. Use the toolchain and dependency operation selected by the active build-farm profile.
4. Use UV for Python workspace creation, dependency synchronization, and frozen validation where Python participates.
5. Do not use a developer’s mutable `.venv` as a build input.
6. Do not use global Python package installation as part of the build contract.
7. Do not use production credentials, production user data, production databases, or production service accounts.
8. Do not permit unrestricted network access.
9. Use only declared mirrors, registries, repositories, and signing services.
10. Do not install a missing dependency silently during an offline or frozen build.
11. Do not mutate source after the source snapshot is selected.
12. Do not rewrite dependency lockfiles during the candidate build.
13. Do not treat the SBOM as proof that the build followed the declared procedure.
14. Do not treat provenance as proof that every listed component is safe or approved.
15. Do not treat a signature as release acceptance.
16. Do not make generated SBOM or provenance files canonical component data.
17. Do not publish a candidate directly to `system`, `services`, `governance`, or `knowledge`.
18. Do not copy secrets, private keys, tokens, credential files, or secret-bearing environment values into evidence.
19. Do not record raw shell history when a bounded build-script reference is sufficient.
20. Do not include ordinary file-hash fields in kOA metadata or handoff manifests.
21. Do not remove the worker until evidence and cleanup results are recorded.
22. Keep failed and rejected candidate records available according to the active retention policy.
23. Treat missing source identity, toolchain identity, dependency closure, test evidence, signature verification, or artifact contract as a blocked handoff.
24. Keep the last accepted release and Release Set unchanged during candidate production.

## 4. Preconditions

Confirm these conditions before starting:

- the active base profile is `build_farm`;
- selected overlays are explicit;
- the active build-farm profile contract is materialized and valid;
- the selected toolchain contract is materialized and valid;
- the candidate artifact class is known;
- the artifact contract is materialized and valid;
- the intended release channel is known;
- the source snapshot is immutable for the duration of the build;
- the dependency lock or equivalent closure record is present;
- required dependency mirrors are available locally or through approved bounded egress;
- the clean-worker mechanism is available;
- test fixtures are synthetic, public, or separately authorized;
- the evidence producer identity is available;
- the signing identity or signing-service integration is available where required;
- the candidate output location is isolated from active release storage;
- the release authority handoff path is known;
- rollback and cleanup procedures are available;
- system time is sufficiently trustworthy for time-sensitive evidence;
- storage capacity exists for source, build, candidate, SBOM, provenance, tests, and cleanup evidence.

When an artifact or provenance schema is scheduled but not materialized, produce only a clearly marked candidate record and block release handoff until schema validation becomes possible.

## 5. Artifact Set

Use distinct identities and files for each artifact.

| Artifact | Purpose | Authority participation |
| --- | --- | --- |
| Candidate payload | The build output proposed for release. | Candidate only. |
| SBOM | Describes included packages, components, versions, licenses, and dependency relationships. | Evidence input; not release authority. |
| Provenance record | Describes source, builder, toolchain, inputs, steps, outputs, and result. | Evidence input; not release authority. |
| Environment record | Describes the controlled worker and relevant implementation selections. | Evidence input. |
| Test-evidence set | Records applicable test identities, results, subjects, and limitations. | Evidence according to the evidence contract. |
| Signature artifact | Binds the selected artifact identity to an approved signer or signing service. | Verification input; not release acceptance. |
| Verification result | Records signature and contract validation. | Evidence input. |
| Candidate handoff manifest | Lists the exact candidate artifact set submitted to release authority. | Handoff record. |
| Cleanup result | Records worker teardown, credential revocation, and residual state. | Operational evidence. |
| Release record | Records release-authority acceptance or rejection. | Produced by release authority, not build farm. |
| Release Set | Binds one tested-compatible release from each canonical channel. | Produced and activated through the release process. |

Do not collapse these artifacts into one mutable record.

## 6. Working Directory Layout

Create one build-run directory outside active release storage.

`bash
export BUILD_RUN_ID='build-run-id-from-the-build-farm-scheduler'
export BUILD_ROOT="/var/lib/koa-build/runs/$BUILD_RUN_ID"
export SOURCE_DIR="$BUILD_ROOT/source"
export WORKSPACE_DIR="$BUILD_ROOT/workspace"
export STAGE_DIR="$BUILD_ROOT/stage"
export CANDIDATE_DIR="$BUILD_ROOT/candidate"
export EVIDENCE_DIR="$BUILD_ROOT/evidence"
export HANDOFF_DIR="$BUILD_ROOT/handoff"
export LOG_DIR="$BUILD_ROOT/logs"
export APPLY_BUILD='0' # 0 = inspect and prepare; 1 = execute after validation

install -d -m 0700 -- \
 "$BUILD_ROOT" \
 "$SOURCE_DIR" \
 "$WORKSPACE_DIR" \
 "$STAGE_DIR" \
 "$CANDIDATE_DIR" \
 "$EVIDENCE_DIR" \
 "$HANDOFF_DIR" \
 "$LOG_DIR"

printf '%s\n' "$BUILD_RUN_ID" > "$EVIDENCE_DIR/build_run_id.txt"
date -u +'%Y-%m-%dT%H:%M:%SZ' > "$EVIDENCE_DIR/started_at.txt"
`

The build worker account should own only this run’s mutable directories and approved shared read-only caches.

## 7. Record Build Inputs

Set values from canonical contracts and the build scheduler.

`bash
export ARTIFACT_ID='candidate-artifact-id'
export ARTIFACT_CLASS='artifact-class-from-active-contract'
export ARTIFACT_VERSION='candidate-semantic-version'
export RELEASE_CHANNEL='system|services|governance|knowledge'
export SOURCE_SNAPSHOT_ID='immutable-source-snapshot-id'
export SOURCE_REFERENCE='repository-relative-or-source-control-reference'
export TOOLCHAIN_ID='toolchain-id-from-active-contract'
export TOOLCHAIN_VERSION='toolchain-contract-version'
export LOCKFILE_REFERENCE='repository-relative-lockfile-reference'
export BUILD_SCRIPT_REFERENCE='repository-relative-build-script-reference'
export PROFILE_ID='build_farm'
export PROFILE_VERSION='active-profile-version'
export RELEASE_SET_CANDIDATE_ID='candidate-release-set-reference-if-assigned'
`

Record the non-secret inputs:

`bash
env \
 | grep -E '^(BUILD_RUN_ID|ARTIFACT_ID|ARTIFACT_CLASS|ARTIFACT_VERSION|RELEASE_CHANNEL|SOURCE_SNAPSHOT_ID|SOURCE_REFERENCE|TOOLCHAIN_ID|TOOLCHAIN_VERSION|LOCKFILE_REFERENCE|BUILD_SCRIPT_REFERENCE|PROFILE_ID|PROFILE_VERSION|RELEASE_SET_CANDIDATE_ID)=' \
 | sort \
 > "$EVIDENCE_DIR/build_inputs.env"
`

Review the record before execution.

## 8. Validate Worker Isolation

Record the worker identity and mutable boundaries.

`bash
id > "$EVIDENCE_DIR/worker_identity.txt"
uname -a > "$EVIDENCE_DIR/kernel_environment.txt"
printf '%s\n' "$PATH" > "$EVIDENCE_DIR/executable_search_path.txt"
findmnt -rno TARGET,SOURCE,FSTYPE,OPTIONS \
 > "$EVIDENCE_DIR/mounts.txt"
`

When a container or virtual machine is used, record:

- runtime identity and version;
- image or template identity;
- network mode;
- mounted paths;
- resource limits;
- user identity;
- privilege mode;
- cleanup mechanism.

Do not infer isolation merely because a container exists.

Validate path containment:

`bash
python - "$BUILD_ROOT" "$SOURCE_DIR" "$WORKSPACE_DIR" "$STAGE_DIR" "$CANDIDATE_DIR" "$EVIDENCE_DIR" "$HANDOFF_DIR" <<'PY'
from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve
for raw in sys.argv[2:]:
 path = Path(raw).resolve
 if path == root or root not in path.parents:
 raise SystemExit(f"path escapes build root: {path}")
print("build paths are contained")
PY
`

## 9. Acquire the Source Snapshot

Acquire source through the approved source adapter.

The source snapshot record includes:

- snapshot ID;
- source repository or archive reference;
- selected revision or release tag;
- acquisition method;
- acquisition time;
- source owner;
- submodule or nested-source references;
- patch-set references;
- license and notice files;
- generated-source policy;
- source-access limitations.

Do not copy an uncommitted developer workspace into the build worker.

After acquisition:

`bash
test -d "$SOURCE_DIR"
test -r "$SOURCE_DIR"

find "$SOURCE_DIR" -xdev -type f -print \
 | LC_ALL=C sort \
 > "$EVIDENCE_DIR/source_file_paths.txt"
`

The path list supports inventory and review. It is not an ordinary file-integrity manifest.

Record source-control status when applicable:

`bash
if git -C "$SOURCE_DIR" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
 git -C "$SOURCE_DIR" status --short \
 > "$EVIDENCE_DIR/source_status.txt"
 git -C "$SOURCE_DIR" submodule status --recursive \
 > "$EVIDENCE_DIR/source_submodules.txt" 2>/dev/null || true
fi
`

The source should be clean unless the active source contract explicitly identifies a patch set.

## 10. Validate Dependency Closure

### 10.1 General rules

Dependency closure is valid when:

- every direct dependency is declared;
- every resolved dependency has an identity and version;
- lock or resolution records are frozen;
- undeclared network retrieval is blocked;
- optional dependency groups are explicit;
- build-only and runtime dependencies remain distinguishable;
- platform-specific dependencies are scoped;
- local path dependencies resolve inside approved source inputs;
- private dependencies use approved credentials without evidence disclosure;
- missing dependencies block the build.

### 10.2 Python with UV

When Python participates:

`bash
cd "$SOURCE_DIR"

uv lock --check

UV_PROJECT_ENVIRONMENT="$WORKSPACE_DIR/.venv" \
 uv sync --frozen --no-dev
`

Add the exact dependency groups and extras selected by the active toolchain contract. Do not invent them from local developer preferences.

Record the installed package inventory without secret-bearing environment values:

`bash
UV_PROJECT_ENVIRONMENT="$WORKSPACE_DIR/.venv" \
 uv pip list --format json \
 > "$EVIDENCE_DIR/python_packages.json"
`

Do not publish the workspace `.venv` as a runtime artifact unless a separate artifact contract explicitly defines such packaging.

### 10.3 Other ecosystems

For other ecosystems, use the frozen operation selected by the active toolchain contract.

Record:

- package-manager identity;
- package-manager version;
- lockfile reference;
- selected dependency groups;
- registry or mirror references;
- offline or frozen flags;
- resolved package inventory;
- missing or substituted dependencies.

A recipe does not select a new package manager.

## 11. Validate Network and Mirror Use

The build worker begins with no unrestricted egress.

Permit only:

- approved source retrieval;
- approved dependency mirrors;
- approved artifact registry staging;
- approved signing service;
- approved evidence destination;
- required local DNS and time.

Record network decisions:

`bash
ss -lntup > "$EVIDENCE_DIR/listening_sockets_before_build.txt"
ip route show table all > "$EVIDENCE_DIR/routes_before_build.txt"
`

After dependency synchronization, disable retrieval egress where the build contract supports a fully closed build phase.

A build that unexpectedly reaches an undeclared destination is rejected or quarantined.

## 12. Execute the Build

The default remains inspection-only.

`bash
if [ "$APPLY_BUILD" != '1' ]; then
 printf '%s\n' 'Inspection complete. Candidate build was not executed.'
 exit 0
fi
`

Execute only the reviewed build script:

`bash
cd "$SOURCE_DIR"

test -f "$BUILD_SCRIPT_REFERENCE"
test -r "$BUILD_SCRIPT_REFERENCE"

env -i \
 HOME="$WORKSPACE_DIR/home" \
 PATH="$PATH" \
 BUILD_RUN_ID="$BUILD_RUN_ID" \
 ARTIFACT_ID="$ARTIFACT_ID" \
 ARTIFACT_VERSION="$ARTIFACT_VERSION" \
 SOURCE_DIR="$SOURCE_DIR" \
 WORKSPACE_DIR="$WORKSPACE_DIR" \
 STAGE_DIR="$STAGE_DIR" \
 CANDIDATE_DIR="$CANDIDATE_DIR" \
 EVIDENCE_DIR="$EVIDENCE_DIR" \
 sh "$BUILD_SCRIPT_REFERENCE" \
 > "$LOG_DIR/build.stdout.log" \
 2> "$LOG_DIR/build.stderr.log"
`

The active toolchain contract can permit additional bounded environment values. Do not pass the host environment wholesale.

Record the terminal result:

`bash
printf '%s\n' 'build_completed' > "$EVIDENCE_DIR/build_result.txt"
date -u +'%Y-%m-%dT%H:%M:%SZ' > "$EVIDENCE_DIR/build_completed_at.txt"
`

If the build fails, preserve bounded logs and continue to failure handling rather than generating a successful provenance record.

## 13. Stage and Identify Candidate Outputs

Move or copy only expected outputs into the candidate directory through the build script or an approved staging step.

Create a path inventory:

`bash
find "$CANDIDATE_DIR" -xdev -type f -print \
 | LC_ALL=C sort \
 > "$EVIDENCE_DIR/candidate_file_paths.txt"
`

Validate:

- every output belongs to the selected artifact class;
- no source-control metadata is included unless the artifact contract requires it;
- no `.venv`, package cache, build cache, test cache, or temporary directory is included;
- no credential, token, private key, environment file, or production configuration is included;
- no unrelated artifact is included;
- executable permissions are intentional;
- ownership and mode are appropriate;
- artifact identity and version are internally consistent where the format supports them.

The file-path inventory is descriptive and does not establish artifact integrity by itself.

## 14. Generate the SBOM

### 14.1 Generator interface

Use the SBOM generator selected by the active toolchain or artifact contract.

This recipe assumes the build-farm implementation exposes a wrapper with the following logical interface:

`text
generate-sbom
 --artifact-id
 --artifact-class
 --artifact-version
 --input-root
 --dependency-inventory
 --format
 --output
 --evidence-output
`

Map this interface to the approved implementation. Do not silently select another generator when the configured generator is unavailable.

Example invocation pattern:

`bash
export SBOM_FORMAT='format-selected-by-artifact-contract'
export SBOM_PATH="$EVIDENCE_DIR/sbom.json"
export SBOM_GENERATOR_BIN='/path/from-active-toolchain-contract'

test -x "$SBOM_GENERATOR_BIN"

"$SBOM_GENERATOR_BIN" generate-sbom \
 --artifact-id "$ARTIFACT_ID" \
 --artifact-class "$ARTIFACT_CLASS" \
 --artifact-version "$ARTIFACT_VERSION" \
 --input-root "$CANDIDATE_DIR" \
 --dependency-inventory "$EVIDENCE_DIR/python_packages.json" \
 --format "$SBOM_FORMAT" \
 --output "$SBOM_PATH" \
 --evidence-output "$EVIDENCE_DIR/sbom_generation.json"
`

Use the relevant dependency inventory when Python is not part of the artifact.

### 14.2 Minimum SBOM content

The normalized SBOM should identify:

- SBOM identity and version;
- artifact identity, class, and version;
- generating tool identity and version;
- generation time;
- included components;
- package or component identifiers;
- versions;
- suppliers or publishers where known;
- declared licenses and notices;
- dependency relationships;
- direct versus transitive relationship;
- runtime versus build-only scope where supported;
- optional or feature-gated components;
- externally provided components;
- incomplete or unavailable metadata;
- source and artifact contract references;
- evidence references;
- limitations.

### 14.3 Prohibited SBOM assumptions

Do not assume:

- an installed package is included in the candidate;
- every source dependency is a runtime dependency;
- every file belongs to a third-party package;
- missing license data means unrestricted use;
- one package name uniquely identifies a component;
- a package version proves the origin;
- SBOM generation proves build reproducibility;
- a scanner result is release approval.

## 15. Normalize and Validate the SBOM

Normalize the SBOM through the active artifact contract.

At minimum:

1. validate JSON structure;
2. validate the selected SBOM schema;
3. reject duplicate component identities within the same declared scope;
4. reject missing artifact identity;
5. reject unresolved dependency references;
6. require an explicit unavailable-license or unavailable-metadata state rather than omission where the contract requires it;
7. distinguish build-only and runtime scope where known;
8. preserve generator identity;
9. preserve limitations;
10. remove secret-bearing fields;
11. reject ordinary file-integrity fields in kOA metadata;
12. ensure the SBOM references the exact candidate artifact identity.

A generic local check can verify JSON parsing and prohibited fields:

`bash
python - "$SBOM_PATH" <<'PY'
from pathlib import Path
import json
import sys

path = Path(sys.argv[1])
data = json.loads(path.read_text(encoding="utf-8"))

prohibited_keys = {
 "metadata_hash",
 "source_hash",
 "content_hash",
 "sha256",
}

def walk(value, location="$"):
 if isinstance(value, dict):
 for key, child in value.items:
 if key.lower in prohibited_keys:
 raise SystemExit(f"prohibited key at {location}.{key}")
 walk(child, f"{location}.{key}")
 elif isinstance(value, list):
 for index, child in enumerate(value):
 walk(child, f"{location}[{index}]")

walk(data)
print("SBOM JSON and metadata-field check passed")
PY
`

A standard-specific validator remains required when the artifact contract selects a standard format.

## 16. Generate the Provenance Record

### 16.1 Provenance purpose

The provenance record explains how the candidate was produced. It does not claim that the candidate is secure, conformant, released, deployed, or compatible with every profile.

### 16.2 Minimum provenance content

Record:

- provenance identity and version;
- candidate artifact identity, class, and version;
- build-run identity;
- builder identity;
- build-farm profile and overlays;
- source snapshot identity and source reference;
- toolchain identity and version;
- lockfile or dependency-closure reference;
- build-script reference;
- input artifact references;
- environment-record reference;
- dependency-inventory reference;
- SBOM reference;
- test-evidence references;
- start and completion time;
- result;
- network and mirror declarations;
- isolation declaration;
- output artifact references;
- signing and verification references;
- limitations;
- cleanup-record reference.

Use references rather than duplicating full logs or protected evidence.

### 16.3 Candidate provenance example

The exact schema remains owned by the active provenance artifact contract. A candidate record can follow this shape before schema validation:

`json
{
 "artifact_class": "provenance_receipt",
 "provenance_id": "provenance-receipt-id",
 "version": "1.0.0",
 "record_status": "candidate",
 "language": "en",
 "issued_at": "2026-08-03T20:00:00-04:00",
 "subject": {
 "artifact_id": "candidate-artifact-id",
 "artifact_class": "artifact-class-from-active-contract",
 "artifact_version": "candidate-semantic-version",
 "release_channel": "services"
 },
 "build": {
 "build_run_id": "build-run-id-from-the-build-farm-scheduler",
 "builder_id": "build-worker-identity",
 "profile_id": "build_farm",
 "source_snapshot_id": "immutable-source-snapshot-id",
 "source_ref": "source-control-or-archive-reference",
 "toolchain_id": "toolchain-id-from-active-contract",
 "toolchain_version": "toolchain-contract-version",
 "lockfile_ref": "repository-relative-lockfile-reference",
 "build_script_ref": "repository-relative-build-script-reference",
 "result": "succeeded"
 },
 "inputs": {
 "artifact_refs": [],
 "dependency_inventory_ref": "evidence/python-packages.json",
 "environment_record_ref": "evidence/environment.json"
 },
 "outputs": {
 "candidate_artifact_refs": [
 "candidate/candidate-artifact"
 ],
 "sbom_ref": "evidence/sbom.json",
 "test_evidence_refs": [
 "evidence/test-results.json"
 ]
 },
 "verification": {
 "signature_artifact_ref": "handoff/signature-artifact",
 "verification_result_ref": "evidence/signature-verification.json"
 },
 "cleanup_record_ref": "evidence/cleanup-result.json",
 "limitations": [
 "Candidate record remains non-authoritative until the active provenance schema and release process accept it."
 ]
}
`

Replace example identities with the active build records.

## 17. Record the Build Environment

The environment record includes only information needed to interpret and reproduce the build.

Record:

- worker identity;
- base image, virtual-machine template, or host profile reference;
- operating-system release reference;
- architecture;
- kernel or runtime reference where relevant;
- container or isolation mechanism;
- user and privilege mode;
- resource limits;
- network mode;
- mounted input and output paths;
- toolchain references;
- locale and timezone;
- approved environment variables by name and non-secret value;
- mirror references;
- time source status;
- active overlays;
- known deviations.

Do not record:

- secrets;
- full credential paths;
- private key material;
- arbitrary host environment;
- unrelated processes;
- unrelated tenant data;
- production topology.

Example environment record creation:

`bash
python - "$EVIDENCE_DIR/environment.json" <<'PY'
from pathlib import Path
import json
import os
import platform
import sys
from datetime import datetime, timezone

output = Path(sys.argv[1])
record = {
 "record_type": "build_environment",
 "version": "1.0.0",
 "recorded_at": datetime.now(timezone.utc).isoformat,
 "build_run_id": os.environ["BUILD_RUN_ID"],
 "profile_id": os.environ["PROFILE_ID"],
 "profile_version": os.environ["PROFILE_VERSION"],
 "platform": {
 "system": platform.system,
 "release": platform.release,
 "machine": platform.machine,
 "python": platform.python_version,
 },
 "toolchain": {
 "toolchain_id": os.environ["TOOLCHAIN_ID"],
 "toolchain_version": os.environ["TOOLCHAIN_VERSION"],
 },
 "network": {
 "unrestricted_egress": False,
 "approved_destinations_record_ref": "evidence/network-destinations.json",
 },
 "secrets_included": False,
}
output.write_text(
 json.dumps(record, indent=2, sort_keys=True) + "\n",
 encoding="utf-8",
)
PY
`

This example is an implementation record and not a canonical environment schema.

## 18. Run Applicable Tests

Resolve tests from:

- artifact contract;
- component contract;
- build-farm profile;
- toolchain contract;
- selected release channel;
- profile test matrix;
- test catalog;
- traceability registry.

Test classes can include:

- schema validation;
- package installation;
- unit tests;
- integration tests;
- interface tests;
- negative boundary tests;
- reproducibility tests where required;
- license and notice checks;
- secret scanning;
- malware or policy scanning where selected;
- SBOM validation;
- provenance validation;
- signature verification;
- startup and shutdown;
- offline behavior;
- rollback or uninstall;
- component data ownership;
- profile compatibility;
- release-channel compatibility.

Record exact test identities and results.

A test summary should distinguish:

- `pass`;
- `fail`;
- `blocked`;
- `not_run`;
- `invalid`;
- `cancelled`;
- `not_applicable`.

Do not count a non-pass result as a pass.

## 19. Bind Evidence and Limitations

Create an evidence index that references rather than duplicates each evidence object.

Example:

`json
{
 "evidence_set_id": "build-evidence-set-id",
 "build_run_id": "build-run-id-from-the-build-farm-scheduler",
 "subject_artifact_id": "candidate-artifact-id",
 "profile_id": "build_farm",
 "evidence_refs": [
 "evidence/build_inputs.env",
 "evidence/environment.json",
 "evidence/python_packages.json",
 "evidence/sbom.json",
 "evidence/provenance.json",
 "evidence/test-results.json",
 "evidence/signature-verification.json",
 "evidence/cleanup-result.json"
 ],
 "limitations": [
 "Build-farm evidence does not prove deployment behavior on an untested profile.",
 "Candidate status does not imply release acceptance.",
 "SBOM completeness remains bounded by the active generator and artifact contract."
 ]
}
`

Evidence remains scoped to:

- the exact candidate;
- the exact build run;
- the exact source snapshot;
- the exact toolchain;
- the exact worker environment;
- the exact test set;
- the exact time period.

## 20. Sign and Verify

### 20.1 Signing boundary

Use the signer selected by the active release or artifact contract.

The build worker should not retain long-lived release private keys.

Preferred patterns include:

- an isolated signing service;
- a hardware-backed signing operation;
- a short-lived delegated signing identity;
- a separate release-authority signing step.

The build farm submits the candidate artifact identity and approved evidence references. It does not silently sign on behalf of release authority.

### 20.2 Signature artifact

Keep the signature as a separate artifact or service receipt.

The handoff records:

- signer identity;
- signer authority reference;
- subject artifact identity;
- signing time;
- signature-artifact reference;
- verification-policy reference;
- verification result;
- revocation state where applicable;
- limitations.

Cryptographic implementations can use internal digest algorithms. Do not add ordinary file-hash fields to kOA documentation, candidate metadata, or handoff manifests.

### 20.3 Verification

Verify:

- signer identity;
- signer authority;
- subject artifact identity;
- signature format;
- verification policy;
- revocation state;
- time validity;
- artifact-contract compatibility;
- evidence-set identity;
- candidate status.

A valid signature does not make an artifact released, compatible, safe, or active.

## 21. Create the Candidate Handoff Manifest

The handoff manifest lists the exact candidate package.

Example:

`json
{
 "handoff_id": "candidate-handoff-id",
 "handoff_type": "release_candidate",
 "status": "ready_for_release_review",
 "build_run_id": "build-run-id-from-the-build-farm-scheduler",
 "candidate": {
 "artifact_id": "candidate-artifact-id",
 "artifact_class": "artifact-class-from-active-contract",
 "artifact_version": "candidate-semantic-version",
 "intended_release_channel": "services"
 },
 "artifact_refs": {
 "payload": "candidate/candidate-artifact",
 "sbom": "evidence/sbom.json",
 "provenance": "evidence/provenance.json",
 "environment": "evidence/environment.json",
 "tests": "evidence/test-results.json",
 "signature": "handoff/signature-artifact",
 "signature_verification": "evidence/signature-verification.json",
 "evidence_index": "evidence/evidence-index.json",
 "cleanup": "evidence/cleanup-result.json"
 },
 "release_authority": {
 "authority_ref": "release-authority-reference",
 "acceptance_required": true,
 "direct_activation_permitted": false
 },
 "release_set": {
 "replacement_release_set_required": true,
 "activation_permitted_before_compatibility_passes": false
 }
}
`

Validate that every referenced file exists and belongs to the same build run.

## 22. Release-Channel and Release Set Handoff

The release authority performs:

1. artifact-contract validation;
2. SBOM validation;
3. provenance validation;
4. test-evidence validation;
5. signer and signature validation;
6. policy and exception evaluation;
7. release-channel membership validation;
8. profile compatibility validation;
9. cross-channel compatibility tests;
10. issue or update of the channel release;
11. issue of a replacement signed Release Set;
12. activation only after all required validation passes.

The build farm cannot:

- write directly to active channel storage;
- mark a release active;
- replace the active Release Set;
- skip an omitted channel;
- assert tested compatibility without evidence;
- reuse evidence outside its scope;
- silently replace a failed candidate.

Rejected candidates retain their record and reason according to retention policy.

## 23. Offline and Mirrored Operation

A build farm can operate without public Internet when:

- source snapshots are locally available;
- dependency mirrors are locally available;
- toolchain runtimes are installed;
- schemas and validators are local;
- signing can occur locally or be deferred;
- release handoff can use delayed or removable transport.

Offline behavior:

- missing uncached dependencies block the affected build;
- no alternate public registry is selected silently;
- the SBOM records the selected local mirror or source registry reference;
- provenance records offline mode;
- signing can remain pending;
- the candidate remains inactive;
- later network restoration does not release the candidate automatically;
- source, dependency, evidence, signer, policy, and Release Set compatibility are revalidated before handoff.

## 24. Multi-Platform and Multi-Architecture Builds

Produce separate candidate identities or explicitly related variants for different:

- operating systems;
- architectures;
- libc or runtime families;
- package formats;
- feature sets;
- optional dependency groups;
- hardware acceleration;
- profile targets.

Each variant receives:

- its own SBOM;
- its own provenance;
- its own environment record;
- its own tests;
- its own signature and verification result where required.

A combined release can reference several validated variants through an artifact contract. Do not merge variant evidence into an ambiguous universal claim.

## 25. Secret and Sensitive-Data Review

Before handoff, inspect:

- build logs;
- test logs;
- environment records;
- SBOM metadata;
- provenance;
- source paths;
- package-registry configuration;
- signing receipts;
- support attachments;
- candidate payload.

Reject or quarantine the build when any artifact contains:

- credentials;
- tokens;
- private keys;
- recovery material;
- production connection strings;
- production user data;
- private identities not required by evidence;
- restricted cultural content;
- hidden service endpoints;
- unrestricted shell history.

Record remediation through a new build run when source or generated output changes materially.

## 26. Cleanup

Cleanup occurs after evidence is committed to the candidate handoff or after failure records are preserved.

### 26.1 Stop active processes

`bash
if [ -f "$EVIDENCE_DIR/worker_processes.txt" ]; then
 cat "$EVIDENCE_DIR/worker_processes.txt"
fi
`

Stop only processes owned by the build run.

### 26.2 Revoke temporary credentials

Revoke:

- source retrieval credentials;
- private registry credentials;
- signing delegation;
- temporary service tokens;
- temporary network grants;
- worker login credentials.

Record revocation results without secret values.

### 26.3 Remove mutable state

Remove only paths confirmed inside the build root:

`bash
python - "$BUILD_ROOT" "$WORKSPACE_DIR" "$STAGE_DIR" <<'PY'
from pathlib import Path
import shutil
import sys

root = Path(sys.argv[1]).resolve
targets = [Path(value).resolve for value in sys.argv[2:]]

for target in targets:
 if root not in target.parents:
 raise SystemExit(f"refusing path outside build root: {target}")
 if target.exists:
 shutil.rmtree(target)
 target.mkdir(mode=0o700)
print("mutable build paths reset")
PY
`

Preserve candidate and evidence paths until release authority or retention policy permits deletion.

### 26.4 Record cleanup

`bash
python - "$EVIDENCE_DIR/cleanup-result.json" <<'PY'
from pathlib import Path
import json
import os
import sys
from datetime import datetime, timezone

output = Path(sys.argv[1])
record = {
 "record_type": "build_cleanup_result",
 "version": "1.0.0",
 "build_run_id": os.environ["BUILD_RUN_ID"],
 "completed_at": datetime.now(timezone.utc).isoformat,
 "temporary_credentials_revoked": True,
 "temporary_network_access_removed": True,
 "mutable_workspace_removed": True,
 "candidate_preserved_for_handoff": True,
 "evidence_preserved_for_handoff": True,
 "result": "complete",
}
output.write_text(
 json.dumps(record, indent=2, sort_keys=True) + "\n",
 encoding="utf-8",
)
PY
`

When any step is incomplete, set the result to `cleanup_incomplete` and block worker reuse.

## 27. Final Validation

Run these checks before setting the handoff to ready:

### 27.1 File presence

`bash
test -s "$EVIDENCE_DIR/sbom.json"
test -s "$EVIDENCE_DIR/provenance.json"
test -s "$EVIDENCE_DIR/environment.json"
test -s "$EVIDENCE_DIR/test-results.json"
test -s "$EVIDENCE_DIR/signature-verification.json"
test -s "$EVIDENCE_DIR/cleanup-result.json"
test -s "$HANDOFF_DIR/candidate-handoff.json"
`

### 27.2 JSON parsing

`bash
python - \
 "$EVIDENCE_DIR/sbom.json" \
 "$EVIDENCE_DIR/provenance.json" \
 "$EVIDENCE_DIR/environment.json" \
 "$EVIDENCE_DIR/test-results.json" \
 "$EVIDENCE_DIR/signature-verification.json" \
 "$EVIDENCE_DIR/cleanup-result.json" \
 "$HANDOFF_DIR/candidate-handoff.json" <<'PY'
from pathlib import Path
import json
import sys

for raw in sys.argv[1:]:
 path = Path(raw)
 json.loads(path.read_text(encoding="utf-8"))
 print(f"valid JSON: {path}")
PY
`

### 27.3 Cross-record consistency

Validate:

- one build-run ID across all records;
- one artifact ID and version;
- one intended release channel;
- one source snapshot;
- one toolchain version;
- one candidate status;
- all references resolve;
- all required tests have valid terminal results;
- signature verification targets the candidate;
- cleanup is complete;
- no direct activation is permitted;
- replacement Release Set is required;
- no prohibited metadata field exists.

### 27.4 Prohibited-field scan

`bash
python - "$EVIDENCE_DIR" "$HANDOFF_DIR" <<'PY'
from pathlib import Path
import json
import sys

prohibited = {
 "metadata_hash",
 "source_hash",
 "content_hash",
 "sha256",
}

def inspect(value, location):
 if isinstance(value, dict):
 for key, child in value.items:
 if key.lower in prohibited:
 raise SystemExit(f"prohibited field: {location}.{key}")
 inspect(child, f"{location}.{key}")
 elif isinstance(value, list):
 for index, child in enumerate(value):
 inspect(child, f"{location}[{index}]")

for root_raw in sys.argv[1:]:
 root = Path(root_raw)
 for path in sorted(root.rglob("*.json")):
 data = json.loads(path.read_text(encoding="utf-8"))
 inspect(data, str(path))
print("prohibited-field scan passed")
PY
`

### 27.5 Secret review

Use the approved secret-scanning mechanism and review results through the active evidence contract.

A clean automated result does not replace review of:

- logs;
- environment records;
- registry configuration;
- package URLs;
- source paths;
- signing responses;
- candidate configuration.

## 28. Failure Handling

| Failure condition | Safe response |
| --- | --- |
| Source snapshot is mutable or dirty | Stop and acquire a new immutable snapshot. |
| Lock or dependency closure changes | Stop and create a new build run. |
| Undeclared dependency retrieval occurs | Quarantine the candidate and inspect network and toolchain configuration. |
| Required dependency is unavailable offline | Block the build; do not select another source silently. |
| Build script differs from the declared reference | Stop and review the source or toolchain change. |
| Build fails | Preserve bounded logs and issue a failed build-run record. |
| Candidate contains an unexpected file | Quarantine and review staging rules. |
| Secret or credential is detected | Quarantine, revoke affected credentials, and produce a new build run. |
| SBOM schema fails | Keep candidate inactive and regenerate after fixing the generator or inputs. |
| SBOM omits a required component | Reject or block the candidate. |
| Provenance schema fails | Keep candidate inactive and repair through a new provenance record or build run as applicable. |
| Provenance references another candidate | Reject the handoff. |
| Required test fails | Mark candidate rejected or blocked according to release policy. |
| Required test is not run or evidence is stale | Keep handoff blocked. |
| Signature verification fails | Quarantine and investigate signer, subject, policy, and transport. |
| Signing service is unavailable | Keep candidate unsigned and inactive; do not substitute another signer. |
| Release-channel membership is ambiguous | Block release review. |
| Cross-channel compatibility fails | Do not issue or activate a replacement Release Set. |
| Cleanup is incomplete | Block worker reuse and enter build-farm recovery. |
| Evidence destination is unavailable | Preserve local bounded evidence and keep handoff pending. |
| System time is uncertain | Block time-sensitive signing and acceptance. |
| External AI suggests a correction | Treat it as candidate analysis and rerun the controlled build after human and canonical acceptance. |

## 29. Example Execution Sequence

`text
resolve build_farm profile, overlays, toolchain, artifact contract, and release channel
allocate one isolated build run
record non-secret build inputs
validate worker identity, paths, mounts, network, and resource limits
acquire one immutable source snapshot
validate frozen dependency closure
create the UV workspace environment when Python participates
disable undeclared network retrieval
execute the reviewed build script
stage only expected candidate outputs
inventory candidate paths
generate the SBOM with the selected generator
validate and normalize the SBOM
generate the provenance record
record the controlled environment
run all applicable tests
bind test evidence and limitations
sign through the approved signer where required
verify the signature and subject identity
create the candidate handoff manifest
revoke temporary credentials and remove mutable build state
validate cross-record consistency
submit the complete candidate set to release authority
keep the active release and Release Set unchanged until acceptance
`

## 30. Completion Checklist

- [ ] Active `build_farm` profile resolved.
- [ ] Selected overlays explicit.
- [ ] Active toolchain contract resolved.
- [ ] Artifact class and artifact contract resolved.
- [ ] Intended release channel resolved.
- [ ] Build-run identity unique.
- [ ] Clean worker allocated.
- [ ] Source snapshot immutable.
- [ ] Source status reviewed.
- [ ] Dependency closure frozen.
- [ ] UV used for Python workspace management.
- [ ] No global Python installation used.
- [ ] Network destinations bounded.
- [ ] No production credentials or production data present.
- [ ] Build script reference reviewed.
- [ ] Candidate output staged separately.
- [ ] Candidate path inventory reviewed.
- [ ] SBOM generated.
- [ ] SBOM schema validation passed.
- [ ] Component identities and dependency references resolve.
- [ ] Provenance generated.
- [ ] Provenance schema validation passed or handoff remains blocked.
- [ ] Environment record generated.
- [ ] Applicable test identities resolved.
- [ ] Required tests have valid evidence.
- [ ] Signature artifact generated where required.
- [ ] Signature verification passed.
- [ ] Candidate handoff manifest generated.
- [ ] No direct release activation permitted.
- [ ] Replacement Release Set required.
- [ ] Offline behavior recorded.
- [ ] Variant scope explicit.
- [ ] Secret review passed.
- [ ] Prohibited metadata-field scan passed.
- [ ] Temporary credentials revoked.
- [ ] Mutable build state removed.
- [ ] Cleanup result is `complete`.
- [ ] Candidate and evidence retained according to policy.
- [ ] Release authority received the exact candidate set.
- [ ] Active release and Release Set remained unchanged during the build.

## 31. References

Use this recipe with the active versions of:

- `00-governance/02-documentation-contract.md`;
- `00-governance/09-recipes-and-implementation-guidance.md`;
- `05-development/02-workspace-identity.md`;
- `05-development/12-development-resource-governance.md`;
- `06-lifecycle/18-sbom-provenance-and-signing.md`;
- `08-operations/05-capacity-management.md`;
- `08-operations/15-support-and-diagnostics.md`;
- `09-conformance/04-profile-test-matrices.md`;
- `contracts/profiles/build-farm.profile.json`;
- `generated/toolchain-catalog.json`;
- the active toolchain contract;
- `contracts/artifact-classes.contract.json`;
- the applicable artifact contract;
- `contracts/release-channels.contract.json`;
- `contracts/artifact-contracts/release-set.schema.json`;
- `contracts/artifact-contracts/provenance-receipt.schema.json`;
- `generated/test-catalog.json`;
- `generated/evidence-catalog.json`;
- the active signed Release Set.

Where this recipe conflicts with an active canonical contract, the canonical contract controls and this recipe must be corrected.
