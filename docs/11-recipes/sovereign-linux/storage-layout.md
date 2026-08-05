<!-- KOA:DOC-META:BEGIN GENERATED
{
 "doc_id": "DOC-RECIPE-SLN-004",
 "document_class": "recipe",
 "status": "active",
 "language": "en",
 "layer": "implementation_recipe",
 "recipe_id": "RECIPE-SLN-004",
 "recipe_version": "1.0.0",
 "scope": [
 "profile:sovereign_linux_node",
 "overlay:high_assurance",
 "overlay:sovereign_offline",
 "sovereign_linux_storage_layout"
 ],
 "canonical_refs": [
 "generated/authority-manifest.json",
 "generated/decision-index.json",
 "generated/document-index.json",
 "contracts/terminology.contract.json",
 "contracts/system.contract.json",
 "generated/component-catalog.json",
 "contracts/profiles/sovereign-linux-node.profile.json",
 "contracts/profiles/high-assurance.profile.json",
 "contracts/profiles/sovereign-offline.profile.json",
 "contracts/artifact-classes.contract.json",
 "contracts/release-channels.contract.json",
 "generated/requirements-index.json",
 "generated/assertion-index.json",
 "generated/traceability.json",
 "generated/exception-index.json",
 "generated/test-catalog.json",
 "generated/evidence-catalog.json",
 "schemas/deployment-profile.schema.json",
 "schemas/test-evidence.schema.json"
 ],
 "decision_ids": [
 "DEC-DATA-001",
 "DEC-GOV-001",
 "DEC-HW-001",
 "DEC-PROFILE-001",
 "DEC-REL-001"
 ],
 "requirement_ids": [
 "REQ-SEC-STOR-001",
 "REQ-SEC-STOR-002",
 "REQ-SEC-STOR-003",
 "REQ-SEC-STOR-004",
 "REQ-SEC-STOR-005",
 "REQ-SEC-STOR-006",
 "REQ-SEC-STOR-007",
 "REQ-SEC-STOR-008",
 "REQ-SEC-STOR-009",
 "REQ-SEC-STOR-010",
 "REQ-SEC-STOR-011",
 "REQ-SEC-STOR-012",
 "REQ-SEC-STOR-013",
 "REQ-SEC-STOR-014",
 "REQ-SEC-STOR-015",
 "REQ-SEC-STOR-016",
 "REQ-SEC-STOR-017",
 "REQ-SEC-STOR-018",
 "REQ-SEC-STOR-019",
 "REQ-SEC-STOR-020",
 "REQ-SEC-STOR-021",
 "REQ-SEC-STOR-022",
 "REQ-SEC-STOR-023",
 "REQ-SEC-STOR-024",
 "REQ-SEC-STOR-025",
 "REQ-SEC-STOR-026",
 "REQ-SEC-STOR-027",
 "REQ-SEC-STOR-028",
 "REQ-SEC-STOR-029",
 "REQ-SEC-STOR-030",
 "REQ-SEC-STOR-031",
 "REQ-SEC-STOR-032",
 "REQ-SEC-STOR-033",
 "REQ-SEC-STOR-034",
 "REQ-SEC-STOR-035",
 "REQ-SEC-STOR-036",
 "REQ-SEC-STOR-037",
 "REQ-SEC-STOR-038",
 "REQ-SEC-STOR-039",
 "REQ-SEC-STOR-040",
 "REQ-SEC-STOR-041",
 "REQ-SEC-STOR-042",
 "REQ-SEC-STOR-043",
 "REQ-SEC-STOR-044",
 "REQ-SEC-STOR-045",
 "REQ-SEC-STOR-046",
 "REQ-SEC-STOR-047",
 "REQ-SEC-STOR-048",
 "REQ-SEC-STOR-049",
 "REQ-SEC-STOR-050",
 "REQ-SEC-STOR-051",
 "REQ-SEC-STOR-052",
 "REQ-SEC-STOR-053",
 "REQ-SEC-STOR-054",
 "REQ-CONF-SLN-001",
 "REQ-CONF-SLN-002",
 "REQ-CONF-SLN-003",
 "REQ-CONF-SLN-004",
 "REQ-CONF-SLN-005",
 "REQ-CONF-SLN-007",
 "REQ-CONF-SLN-008",
 "REQ-CONF-SLN-010",
 "REQ-CONF-SLN-011",
 "REQ-CONF-SLN-012",
 "REQ-CONF-SLN-013",
 "REQ-CONF-SLN-014",
 "REQ-CONF-SLN-015",
 "REQ-CONF-SLN-016",
 "REQ-CONF-SLN-017",
 "REQ-CONF-SLN-018",
 "REQ-CONF-SLN-019",
 "REQ-CONF-SLN-020",
 "REQ-CONF-SLN-021",
 "REQ-CONF-SLN-022",
 "REQ-CONF-SLN-023",
 "REQ-CONF-SLN-024",
 "REQ-CONF-SLN-025",
 "REQ-CONF-SLN-026",
 "REQ-CONF-SLN-027",
 "REQ-CONF-SLN-028",
 "REQ-CONF-SLN-029",
 "REQ-CONF-SLN-030",
 "REQ-CONF-SLN-031",
 "REQ-CONF-SLN-032",
 "REQ-CONF-SLN-033",
 "REQ-CONF-SLN-034",
 "REQ-CONF-SLN-039",
 "REQ-CONF-SLN-040",
 "REQ-CONF-SLN-041",
 "REQ-CONF-SLN-042",
 "REQ-CONF-SLN-043",
 "REQ-CONF-SLN-044",
 "REQ-CONF-SLN-047",
 "REQ-CONF-SLN-048",
 "REQ-CONF-SLN-049",
 "REQ-CONF-SLN-050",
 "REQ-CONF-SLN-051",
 "REQ-CONF-SLN-052",
 "REQ-CONF-SLN-053",
 "REQ-CONF-SLN-056",
 "REQ-CONF-SLN-057",
 "REQ-CONF-SLN-058",
 "REQ-CONF-SLN-059",
 "REQ-CONF-SLN-060"
 ],
 "lock_ids": [
 "LOCK-COMP-001",
 "LOCK-COMP-002",
 "LOCK-DATA-001",
 "LOCK-DOC-003",
 "LOCK-DOC-004",
 "LOCK-GOV-001",
 "LOCK-IMPL-001",
 "LOCK-LIFE-001",
 "LOCK-LIFE-002",
 "LOCK-LIFE-003",
 "LOCK-LIFE-004",
 "LOCK-PROFILE-001",
 "LOCK-PROFILE-002",
 "LOCK-SEC-010"
 ],
 "exception_ids": [],
 "depends_on": [
 "DOC-CONST-002",
 "DOC-CONST-013",
 "DOC-SEC-009",
 "DOC-SEC-019",
 "DOC-OPS-016",
 "DOC-CONF-005",
 "DOC-CONF-016",
 "DOC-ADR-005",
 "DOC-ADR-024"
 ],
 "tags": [
 "recipe",
 "sovereign-linux",
 "storage-layout",
 "logical-data-ownership",
 "physical-isolation",
 "encryption-at-rest",
 "artifacts",
 "evidence",
 "backup",
 "restore",
 "offline",
 "non-normative"
 ]
}
KOA:DOC-META:END -->

# Sovereign Linux Storage Layout

> **Recipe status:** Active, non-normative implementation recipe.
> **Implementation:** Profile-derived Linux mount points with one encrypted active-data boundary, owner-specific subtrees, a separate recovery target, and a backup target in a distinct failure domain.
> **Authority rule:** This recipe maps canonical storage boundaries to one practical layout. Component, profile, security, lifecycle, and conformance contracts remain authoritative.

---

## Recipe Identity

| Field | Value |
| --- | --- |
| Recipe ID | `RECIPE-SLN-004` |
| Title | Sovereign Linux Storage Layout |
| Status | Active |
| Version | `1.0.0` |
| Owner | Sovereign Linux Operations |
| Last reviewed | 2026-08-03 |
| Applies to profiles | `sovereign_linux_node` |
| Compatible overlays | `high_assurance`, `sovereign_offline` when their contracts accept this mapping |
| Applies to components | Every component included by the active profile |
| Supported platforms | Profile-admitted Linux system with already provisioned encrypted storage |
| Supersedes | None |
| Replaced by | None |

---

## 1. Purpose

This recipe creates and validates a storage layout for one `sovereign_linux_node`.

The layout separates:

- active authoritative component data;
- replicas;
- projections and indexes;
- queues and checkpoints;
- canonical release artifacts;
- audit receipts and conformance evidence;
- disposable caches;
- staging and repair state;
- local recovery artifacts;
- backup media.

The procedure preserves:

- one logical owner per authoritative data set;
- one owner-approved write path;
- component-scoped runtime identities;
- profile-dependent physical isolation;
- encrypted active storage;
- separate recovery and backup targets;
- explicit capacity and failure behavior;
- offline continuity;
- owner-approved restore validation.

Successful completion produces:

`text
profile and node identity
→ verified encrypted active-data mount
→ owner-scoped component boundaries
→ separate artifact and evidence boundaries
→ bounded cache and staging boundaries
→ verified recovery target
→ verified distinct backup target
→ registered conformance evidence
`

This recipe does not choose a universal:

- Linux distribution;
- filesystem;
- partition table;
- volume manager;
- encryption implementation;
- storage engine;
- backup product;
- database product;
- object store;
- queue;
- key-management implementation.

## 2. Non-Normative Status

This recipe is non-normative unless the active profile explicitly adopts this exact implementation.

The canonical owners remain:

| Fact | Canonical owner |
| --- | --- |
| Profile composition and physical-isolation strength | Active profile and overlays |
| Authoritative data ownership | Component and registry contracts |
| Storage security boundaries | `docs/07-security/09-storage-boundaries.md` |
| Logical versus physical isolation | `ADR-024` and `DEC-DATA-001` |
| Encryption and key custody | Data-at-rest, secrets, Identity and Trust contracts |
| Artifact identity and lifecycle | Artifact-class and release contracts |
| Backup, restore, rollback, and forward repair | Owner and lifecycle contracts |
| Exact tests and evidence | Test catalog, evidence, and traceability registries |

This recipe cannot:

- create a second data owner;
- authorize direct cross-component writes;
- make a backup or replica authoritative;
- approve a weaker isolation level than the profile;
- substitute filesystem permissions for component authorization;
- grant an operator application-level data authority;
- define a production encryption key;
- turn a directory path into a canonical component interface.

A conflict with active authority blocks this recipe.

## 3. Scope

### 3.1 Included

This recipe covers:

- resolving the exact node, profile, overlays, active Release Set, and storage inputs;
- verifying that the active-data mount is encrypted as required by the profile;
- creating fixed top-level kOA storage roots;
- creating owner-scoped component subtrees;
- separating authoritative, replica, projection, queue, checkpoint, cache, log, and staging classes;
- creating artifact-channel storage;
- creating audit and conformance-evidence storage;
- validating recovery and backup targets;
- validating mount, owner, permission, symlink, capacity, and failure-domain boundaries;
- defining cleanup and rollback for empty newly created paths;
- collecting non-sensitive evidence.

### 3.2 Excluded

This recipe does not:

- repartition a disk;
- create or format a filesystem;
- initialize a volume manager;
- generate or enroll encryption keys;
- destroy existing storage;
- provision component databases;
- create database users or schemas;
- configure replication;
- configure backup software;
- restore authoritative data;
- migrate existing authoritative data;
- modify the active Release Set;
- enable services;
- create service identities;
- handle production secret values.

Those operations require their own active procedure.

### 3.3 Required baseline

The sovereign Linux baseline includes:

`text
8 modern CPU cores minimum
32 GiB RAM minimum
1 TB encrypted SSD minimum
recovery target required
verified backup target required
`

This recipe validates storage-related facts only.

It does not fail a baseline node for having 32 GiB rather than the recommended 64 GiB.

### 3.4 Physical-layout variants

This recipe defines two compatible mappings.

**Baseline shared-encrypted-volume mapping**

- active component data, artifacts, and evidence can share one encrypted data filesystem;
- each owner and storage class remains logically separate;
- recovery uses a separate target;
- backup uses a distinct failure domain.

**Stronger physical-separation mapping**

An adopting overlay or profile can map the same logical roots to:

- separate volumes;
- separate devices;
- separate encryption keys;
- separate storage services;
- separate nodes;
- separate jurisdictions;
- separate operator custody.

The logical paths and owners remain stable.

## 4. Canonical References

### 4.1 Decisions and ADRs

- `DEC-DATA-001`
- `DEC-GOV-001`
- `DEC-HW-001`
- `DEC-PROFILE-001`
- `DEC-REL-001`
- `ADR-024`

### 4.2 Primary normative documents

- `docs/07-security/09-storage-boundaries.md`
- `docs/07-security/19-software-supply-chain.md`
- `docs/08-operations/16-break-glass.md`
- `docs/09-conformance/05-test-evidence.md`
- `docs/09-conformance/16-sovereign-linux-conformance.md`
- `docs/10-adrs/ADR-024-logical-data-ownership-with-profile-dependent-physical-isolation.md`

### 4.3 Locks

- `LOCK-COMP-001`
- `LOCK-COMP-002`
- `LOCK-DATA-001`
- `LOCK-GOV-001`
- `LOCK-IMPL-001`
- `LOCK-LIFE-001`
- `LOCK-LIFE-002`
- `LOCK-LIFE-003`
- `LOCK-LIFE-004`
- `LOCK-PROFILE-001`
- `LOCK-PROFILE-002`
- `LOCK-SEC-010`

### 4.4 Profile and registry sources

- `contracts/profiles/sovereign-linux-node.profile.json`
- `contracts/profiles/high-assurance.profile.json`
- `contracts/profiles/sovereign-offline.profile.json`
- `generated/component-catalog.json`
- `contracts/artifact-classes.contract.json`
- `contracts/release-channels.contract.json`
- `generated/test-catalog.json`
- `generated/evidence-catalog.json`
- `generated/traceability.json`

## 5. Preconditions

### 5.1 Authority preconditions

Before execution:

- the exact node profile exists and validates;
- `NODE_ID` resolves to the target node;
- the active primary profile is `sovereign_linux_node`;
- every overlay is explicit and compatible;
- the active Release Set resolves;
- every included component and service identity resolves;
- every authoritative data set has one owner;
- every storage boundary has an owner, class, capacity, retention, backup, restore, and recovery declaration;
- the selected physical mapping satisfies the profile and overlays;
- no unresolved exception is used to weaken ownership or encryption.

Failure produces `blocked`.

### 5.2 Identity preconditions

The following identities already exist:

- deployment or storage administrator;
- component runtime users and groups;
- artifact-store writer identity;
- evidence-store writer identity;
- backup identity;
- restore authority;
- applicable break-glass identities.

This recipe does not create those identities.

Verify one runtime identity:

`bash
: "${SERVICE_USER:?SERVICE_USER must resolve from the active service contract}"
: "${SERVICE_GROUP:?SERVICE_GROUP must resolve from the active service contract}"

getent passwd "$SERVICE_USER" >/dev/null
getent group "$SERVICE_GROUP" >/dev/null
`

### 5.3 Mount preconditions

The deployment authority supplies exact, already mounted paths:

`bash
export KOA_ACTIVE_ROOT="/var/lib/koa"
export KOA_RECOVERY_ROOT="/var/lib/koa-recovery"
export KOA_BACKUP_ROOT="/mnt/koa-backup"
`

Required properties:

- all paths are absolute;
- no path is a symlink;
- active and recovery roots are mounted according to the profile;
- backup root is mounted from a distinct approved target;
- the active-data mount is encrypted where required;
- the backup target meets the declared failure-domain objective;
- mount ownership and options match profile policy.

Basic verification:

`bash
set -euo pipefail

for path in "$KOA_ACTIVE_ROOT" "$KOA_RECOVERY_ROOT" "$KOA_BACKUP_ROOT"; do
 case "$path" in
 /*) ;;
 *) printf '%s
' "storage root must be absolute: $path" >&2; exit 1 ;;
 esac
 test -d "$path"
 test ! -L "$path"
 mountpoint -q "$path"
done
`

### 5.4 Encryption preconditions

The profile-approved verifier must confirm encryption of:

- the active-data SSD or volume;
- every additional storage class for which encryption is required;
- the backup target where required;
- recovery material where required.

A device-mapper example can inspect, but not independently authorize, encryption:

`bash
ACTIVE_SOURCE="$(findmnt -n -o SOURCE --target "$KOA_ACTIVE_ROOT")"
printf '%s
' "$ACTIVE_SOURCE"
`

The result is compared with the profile-owned encryption inventory and key reference.

A path name containing `crypt` is not proof of encryption.

### 5.5 Free-space preconditions

The profile or resource envelope defines required free-space thresholds.

This recipe does not invent numeric thresholds.

Verify that values resolve:

`bash
: "${ACTIVE_MIN_FREE_BYTES:?resolve from profile or resource envelope}"
: "${RECOVERY_MIN_FREE_BYTES:?resolve from recovery contract}"
: "${BACKUP_MIN_FREE_BYTES:?resolve from backup contract}"
`

The procedure blocks when any value is absent.

## 6. Inputs and Outputs

### 6.1 Inputs

| Input | Source | Required |
| --- | --- | ---: |
| `NODE_ID` | Node profile | Yes |
| Primary profile and version | Profile contract | Yes |
| Overlay IDs and versions | Profile composition | Conditional |
| Active Release Set | Release authority | Yes |
| Included component IDs | Active profile | Yes |
| Component runtime users and groups | Component and identity contracts | Yes |
| Component data classes | Component contracts | Yes |
| Active storage root | Profile storage mapping | Yes |
| Recovery root | Recovery contract | Yes |
| Backup root | Backup contract | Yes |
| Capacity and quota values | Resource envelope or profile | Yes |
| Encryption and key references | Data-at-rest and trust contracts | Yes |
| Retention and backup policies | Component and governance contracts | Yes |
| Active exceptions | Exceptions registry | Conditional |

### 6.2 Outputs

| Output | Description | Authority |
| --- | --- | --- |
| Top-level storage roots | Stable implementation paths | Recipe output |
| Component-owned directories | Filesystem boundary for owner state | Component remains authoritative |
| Artifact-channel directories | Storage for admitted immutable artifacts | Artifact lifecycle remains authoritative |
| Evidence directories | Storage for receipts and test evidence | Evidence and audit contracts remain authoritative |
| Recovery directory mapping | Location for admitted recovery material | Recovery contract |
| Backup mount verification | Evidence that approved target is present | Backup contract |
| Layout-validation result | Non-sensitive conformance evidence | Evidence registry after registration |

### 6.3 Created top-level layout

`text
/var/lib/koa/
├── components/
├── artifacts/
├── evidence/
├── cache/
├── staging/
├── lost-and-found-review/
└── layout-version

/var/lib/koa-recovery/
├── system/
├── manifests/
├── trust/
└── validation/

/mnt/koa-backup/
└── node-specific backup namespace owned by the backup procedure
`

`lost-and-found-review` is a quarantine location for unattributed recovered files.

It is not authoritative and is not the filesystem implementation's own `lost+found` directory.

## 7. Safety and Security Boundaries

### 7.1 Privilege model

Top-level provisioning requires the profile-approved privileged path.

The procedure can be executed by:

- an authorized deployment service;
- a narrow privileged broker;
- a directly authorized operator where the profile permits it.

Do not grant ordinary component services general root access.

### 7.2 Destructive-operation boundary

This recipe performs no:

- partitioning;
- formatting;
- volume deletion;
- recursive data deletion;
- database initialization;
- restore;
- migration.

Any command that would destroy an existing filesystem or volume is outside scope.

### 7.3 Symlink and mount boundary

Top-level roots and owner boundaries must not be symlinks.

The recipe verifies the mount containing each path and rejects a boundary that resolves through:

- a symlink;
- an unexpected bind mount;
- an unapproved network filesystem;
- a temporary filesystem for authoritative data;
- an external provider not admitted by the profile.

### 7.4 Ownership boundary

Runtime component users receive write access only to their own declared paths.

They do not receive write access to:

- another component subtree;
- canonical artifact directories;
- audit or conformance evidence owned by another authority;
- recovery artifacts;
- backup media;
- top-level staging outside their exact scope.

### 7.5 Secrets and keys

Secret values and private keys do not belong in ordinary component, artifact, cache, staging, log, evidence, or backup paths unless an explicit secret-storage or key-storage contract governs them.

Mounting a directory does not authorize secret storage there.

### 7.6 Artifact boundary

Presence in `/var/lib/koa/artifacts` does not make an artifact:

- admitted;
- active;
- compatible;
- trusted;
- part of the active Release Set.

Artifact identity, provenance, signatures, admission, and activation remain separate.

### 7.7 Backup boundary

The backup target is not a writable general-purpose component filesystem.

Component runtime identities do not write directly to backup media.

The approved backup authority captures owner-scoped consistent data and writes the backup.

### 7.8 Evidence minimization

Layout evidence can contain:

- path;
- owner and group names;
- mode;
- mount source identity;
- filesystem type;
- capacity values;
- boundary class;
- validation outcome.

It excludes:

- file contents;
- secret values;
- private key material;
- tenant payloads;
- database rows;
- unrestricted directory listings.

## 8. Resource Envelope

The active profile or resource envelope supplies exact capacity values.

This recipe maps them to storage classes.

| Class | Capacity authority | Exhaustion behavior |
| --- | --- | --- |
| Authoritative component data | Component plus Resource Governor | Block new writes before corruption or partial commit |
| Replicas | Owner replication contract | Throttle or rebuild without becoming authority |
| Projections and indexes | Owner component | Evict or rebuild before authoritative loss |
| Queues | Job and component contracts | Reject, defer, or block according to finite capacity |
| Artifacts | Release and artifact contracts | Prevent staging or activation when insufficient |
| Evidence | Audit and evidence contracts | Preserve receipt-before-commit behavior |
| Cache | Resource Governor | Evict safely |
| Staging | Lifecycle contract | Clean failed candidates; never promote by persistence |
| Recovery | Recovery contract | Block recovery-material update |
| Backup | Backup contract | Fail backup; do not claim success |

Resolve free space without printing file contents:

`bash
available_bytes {
 df -B1 --output=avail "$1" | awk 'NR==2 {print $1}'
}

test "$(available_bytes "$KOA_ACTIVE_ROOT")" -ge "$ACTIVE_MIN_FREE_BYTES"
test "$(available_bytes "$KOA_RECOVERY_ROOT")" -ge "$RECOVERY_MIN_FREE_BYTES"
test "$(available_bytes "$KOA_BACKUP_ROOT")" -ge "$BACKUP_MIN_FREE_BYTES"
`

A failed check blocks provisioning or the affected operation.

## 9. Naming and Isolation

### 9.1 Stable root names

This recipe uses:

`text
components
artifacts
evidence
cache
staging
lost-and-found-review
`

These are implementation directories, not new artifact or component classes.

### 9.2 Component path pattern

For a component with canonical identifier in `COMPONENT_ID`:

`text
$KOA_ACTIVE_ROOT/components/$COMPONENT_ID/
├── authoritative/
├── replicas/
├── projections/
├── queues/
├── checkpoints/
├── logs/
└── temporary/
`

Only directories declared by the component contract are created.

A component without a queue does not receive a queue merely because this recipe lists the class.

### 9.3 Artifact path pattern

`text
$KOA_ACTIVE_ROOT/artifacts/
├── system/
├── services/
├── governance/
├── knowledge/
├── manifests/
└── quarantine/
`

The four channel directories preserve release-channel identity.

`quarantine` contains rejected or unresolved candidates and is never an activation source.

### 9.4 Evidence path pattern

`text
$KOA_ACTIVE_ROOT/evidence/
├── audit/
├── conformance/
├── decisions/
├── provenance/
└── receipts/
`

Exact ownership follows Audit Broker, evidence, and artifact contracts.

### 9.5 Cache and staging pattern

`text
$KOA_ACTIVE_ROOT/cache/$COMPONENT_ID/
$KOA_ACTIVE_ROOT/staging/$COMPONENT_ID/
`

Caches are disposable and reproducible.

Staging is bounded and non-authoritative.

### 9.6 Collision behavior

Creation is permitted only when an existing path:

- has the expected type;
- is not a symlink;
- has the expected owner;
- has the expected group;
- has the expected mode;
- resides on the expected mount;
- matches the declared boundary class.

Any mismatch blocks the procedure.

## 10. Procedure

### Step 1 — Resolve node and profile identity

**Objective**

Bind execution to one exact node and profile composition.

**Command**

`bash
set -euo pipefail
set +x
umask 077

: "${NODE_ID:?NODE_ID must resolve from the active node profile}"
: "${PRIMARY_PROFILE_ID:?PRIMARY_PROFILE_ID must be set}"
: "${PRIMARY_PROFILE_VERSION:?PRIMARY_PROFILE_VERSION must be set}"
: "${ACTIVE_RELEASE_SET_ID:?ACTIVE_RELEASE_SET_ID must be set}"
: "${ACTIVE_RELEASE_SET_VERSION:?ACTIVE_RELEASE_SET_VERSION must be set}"

test "$PRIMARY_PROFILE_ID" = "sovereign_linux_node"
`

**Expected result**

The exact node, profile version, overlays, architecture, hardware class, and Release Set resolve.

**Verification**

Run the active profile and Release Set validators.

**Failure behavior**

Stop without filesystem mutation.

---

### Step 2 — Capture a bounded storage inventory

**Objective**

Identify devices, mounts, filesystem types, and capacity without scanning data contents.

**Command**

`bash
lsblk --json --bytes --output NAME,KNAME,TYPE,SIZE,FSTYPE,FSVER,MOUNTPOINTS,UUID,PARTUUID,PKNAME,ROTA,RO
findmnt --json --bytes --output TARGET,SOURCE,FSTYPE,OPTIONS,SIZE,USED,AVAIL
`

Store the output only in the approved conformance-evidence path after sanitizing device labels or identifiers classified as sensitive.

**Expected result**

The active, recovery, and backup roots resolve to declared mount sources.

**Verification**

`bash
for path in "$KOA_ACTIVE_ROOT" "$KOA_RECOVERY_ROOT" "$KOA_BACKUP_ROOT"; do
 findmnt --target "$path" >/dev/null
done
`

**Failure behavior**

Stop before creating directories.

---

### Step 3 — Verify physical separation and encryption declarations

**Objective**

Confirm that the observed topology matches the profile mapping.

**Command**

`bash
ACTIVE_SOURCE="$(findmnt -n -o SOURCE --target "$KOA_ACTIVE_ROOT")"
RECOVERY_SOURCE="$(findmnt -n -o SOURCE --target "$KOA_RECOVERY_ROOT")"
BACKUP_SOURCE="$(findmnt -n -o SOURCE --target "$KOA_BACKUP_ROOT")"

printf '%s
' "active_source=$ACTIVE_SOURCE" "recovery_source=$RECOVERY_SOURCE" "backup_source=$BACKUP_SOURCE"
`

The deployment authority compares these values with the canonical storage inventory.

**Expected result**

- active source is the declared encrypted data source;
- recovery source is the declared recovery target;
- backup source is the declared backup target;
- backup target is in the required distinct failure domain;
- overlay-required key, device, node, or jurisdiction separation passes.

**Verification**

Use the profile-approved encryption and topology validator.

A string comparison between source names is not sufficient proof of failure-domain separation.

**Failure behavior**

Mark the layout `blocked`.

---

### Step 4 — Verify clean top-level mount roots

**Objective**

Reject unsafe symlink, nested-mount, and unexpected-content conditions.

**Command**

`bash
for path in "$KOA_ACTIVE_ROOT" "$KOA_RECOVERY_ROOT" "$KOA_BACKUP_ROOT"; do
 test -d "$path"
 test ! -L "$path"
 mountpoint -q "$path"
done

test -O "$KOA_ACTIVE_ROOT" || test "$(stat -c '%U' "$KOA_ACTIVE_ROOT")" = "root"
test -O "$KOA_RECOVERY_ROOT" || test "$(stat -c '%U' "$KOA_RECOVERY_ROOT")" = "root"
`

List only top-level names:

`bash
find "$KOA_ACTIVE_ROOT" -mindepth 1 -maxdepth 1 -printf '%f
' | sort
`

**Expected result**

Existing names are attributable to this layout or an approved migration plan.

**Failure behavior**

Move no data. Unattributed existing content requires owner identification before continuing.

---

### Step 5 — Create active top-level boundaries

**Objective**

Create root-owned boundaries without granting component-wide access.

**Command**

`bash
install -d -o root -g root -m 0750 "$KOA_ACTIVE_ROOT/components"
install -d -o root -g root -m 0750 "$KOA_ACTIVE_ROOT/artifacts"
install -d -o root -g root -m 0750 "$KOA_ACTIVE_ROOT/evidence"
install -d -o root -g root -m 0750 "$KOA_ACTIVE_ROOT/cache"
install -d -o root -g root -m 0750 "$KOA_ACTIVE_ROOT/staging"
install -d -o root -g root -m 0700 "$KOA_ACTIVE_ROOT/lost-and-found-review"

printf '%s
' "RECIPE-SLN-004/1.0.0" |
 install -o root -g root -m 0644 /dev/stdin "$KOA_ACTIVE_ROOT/layout-version"
`

**Expected result**

Top-level paths are root-owned, non-symlink directories on the active-data mount.

**Verification**

`bash
for name in components artifacts evidence cache staging lost-and-found-review; do
 path="$KOA_ACTIVE_ROOT/$name"
 test -d "$path"
 test ! -L "$path"
 test "$(stat -c '%U:%G' "$path")" = "root:root"
 test "$(findmnt -n -o TARGET --target "$path")" = "$KOA_ACTIVE_ROOT"
done
`

**Failure behavior**

Stop before component paths are created.

---

### Step 6 — Create one component-owned boundary

**Objective**

Create only the classes declared by one active component.

**Inputs**

`bash
: "${COMPONENT_ID:?resolve from the active profile}"
: "${SERVICE_USER:?resolve from the active service identity}"
: "${SERVICE_GROUP:?resolve from the active service identity}"
: "${COMPONENT_STORAGE_CLASSES:?space-separated declared classes}"
`

Accepted class names for this recipe:

`text
authoritative replicas projections queues checkpoints logs temporary
`

**Command**

`bash
getent passwd "$SERVICE_USER" >/dev/null
getent group "$SERVICE_GROUP" >/dev/null

COMPONENT_ROOT="$KOA_ACTIVE_ROOT/components/$COMPONENT_ID"
install -d -o root -g "$SERVICE_GROUP" -m 0750 "$COMPONENT_ROOT"

for class_name in $COMPONENT_STORAGE_CLASSES; do
 case "$class_name" in
 authoritative)
 install -d -o "$SERVICE_USER" -g "$SERVICE_GROUP" -m 0700 "$COMPONENT_ROOT/authoritative"
 ;;
 replicas|projections|queues|checkpoints|logs|temporary)
 install -d -o "$SERVICE_USER" -g "$SERVICE_GROUP" -m 0750 "$COMPONENT_ROOT/$class_name"
 ;;
 *)
 printf '%s
' "unsupported or undeclared storage class: $class_name" >&2
 exit 1
 ;;
 esac
done
`

**Expected result**

Only the declared owner can write the authoritative directory.

**Verification**

`bash
test ! -L "$COMPONENT_ROOT"

for class_name in $COMPONENT_STORAGE_CLASSES; do
 path="$COMPONENT_ROOT/$class_name"
 test -d "$path"
 test ! -L "$path"
 test "$(stat -c '%U:%G' "$path")" = "$SERVICE_USER:$SERVICE_GROUP"
done

if test -d "$COMPONENT_ROOT/authoritative"; then
 test "$(stat -c '%a' "$COMPONENT_ROOT/authoritative")" = "700"
fi
`

**Failure behavior**

Do not start the component.

**Repetition**

Repeat this step for every component included by the active profile.

---

### Step 7 — Create artifact-channel boundaries

**Objective**

Create storage paths preserving the four release channels.

**Inputs**

`bash
: "${ARTIFACT_USER:?resolve from artifact-store authority}"
: "${ARTIFACT_GROUP:?resolve from artifact-store authority}"
`

**Command**

`bash
getent passwd "$ARTIFACT_USER" >/dev/null
getent group "$ARTIFACT_GROUP" >/dev/null

for channel in system services governance knowledge manifests quarantine; do
 install -d -o "$ARTIFACT_USER" -g "$ARTIFACT_GROUP" -m 0750 "$KOA_ACTIVE_ROOT/artifacts/$channel"
done
`

**Expected result**

Component runtime identities cannot write canonical artifact paths.

**Verification**

`bash
for channel in system services governance knowledge manifests quarantine; do
 path="$KOA_ACTIVE_ROOT/artifacts/$channel"
 test "$(stat -c '%U:%G' "$path")" = "$ARTIFACT_USER:$ARTIFACT_GROUP"
 test "$(stat -c '%a' "$path")" = "750"
done
`

**Failure behavior**

Artifact admission and activation remain blocked.

---

### Step 8 — Create evidence boundaries

**Objective**

Separate evidence writers and evidence classes from component business data.

**Inputs**

`bash
: "${EVIDENCE_USER:?resolve from evidence authority}"
: "${EVIDENCE_GROUP:?resolve from evidence authority}"
`

**Command**

`bash
getent passwd "$EVIDENCE_USER" >/dev/null
getent group "$EVIDENCE_GROUP" >/dev/null

for class_name in audit conformance decisions provenance receipts; do
 install -d -o "$EVIDENCE_USER" -g "$EVIDENCE_GROUP" -m 0750 "$KOA_ACTIVE_ROOT/evidence/$class_name"
done
`

**Expected result**

Evidence paths are separate from component authoritative stores and artifact storage.

**Verification**

`bash
for class_name in audit conformance decisions provenance receipts; do
 path="$KOA_ACTIVE_ROOT/evidence/$class_name"
 test "$(stat -c '%U:%G' "$path")" = "$EVIDENCE_USER:$EVIDENCE_GROUP"
done
`

**Failure behavior**

Receipt-before-commit transitions remain blocked when their evidence path is unavailable.

---

### Step 9 — Create cache and staging boundaries

**Objective**

Create disposable and temporary paths without granting authority.

**Command**

For one component:

`bash
CACHE_ROOT="$KOA_ACTIVE_ROOT/cache/$COMPONENT_ID"
STAGING_ROOT="$KOA_ACTIVE_ROOT/staging/$COMPONENT_ID"

install -d -o "$SERVICE_USER" -g "$SERVICE_GROUP" -m 0750 "$CACHE_ROOT"
install -d -o "$SERVICE_USER" -g "$SERVICE_GROUP" -m 0700 "$STAGING_ROOT"
`

**Expected result**

The component can rebuild cache state and can stage bounded candidate data.

**Verification**

`bash
test "$(stat -c '%U:%G' "$CACHE_ROOT")" = "$SERVICE_USER:$SERVICE_GROUP"
test "$(stat -c '%U:%G' "$STAGING_ROOT")" = "$SERVICE_USER:$SERVICE_GROUP"
test "$(stat -c '%a' "$STAGING_ROOT")" = "700"
`

**Failure behavior**

Do not redirect staging into authoritative or artifact paths.

---

### Step 10 — Create recovery-target boundaries

**Objective**

Create a read-mostly layout for admitted recovery material.

**Inputs**

`bash
: "${RECOVERY_USER:?resolve from recovery authority}"
: "${RECOVERY_GROUP:?resolve from recovery authority}"
`

**Command**

`bash
for class_name in system manifests trust validation; do
 install -d -o "$RECOVERY_USER" -g "$RECOVERY_GROUP" -m 0750 "$KOA_RECOVERY_ROOT/$class_name"
done
`

**Expected result**

Normal component runtime identities cannot write the recovery target.

**Verification**

`bash
for class_name in system manifests trust validation; do
 path="$KOA_RECOVERY_ROOT/$class_name"
 test "$(stat -c '%U:%G' "$path")" = "$RECOVERY_USER:$RECOVERY_GROUP"
done
`

Recovery artifacts still require their own admission and integrity verification.

---

### Step 11 — Verify backup target and namespace

**Objective**

Confirm the backup target is mounted and create one node-scoped root for the approved backup authority.

**Inputs**

`bash
: "${BACKUP_USER:?resolve from backup authority}"
: "${BACKUP_GROUP:?resolve from backup authority}"
`

**Command**

`bash
mountpoint -q "$KOA_BACKUP_ROOT"
getent passwd "$BACKUP_USER" >/dev/null
getent group "$BACKUP_GROUP" >/dev/null

BACKUP_NODE_ROOT="$KOA_BACKUP_ROOT/nodes/$NODE_ID"
install -d -o root -g root -m 0750 "$KOA_BACKUP_ROOT/nodes"
install -d -o "$BACKUP_USER" -g "$BACKUP_GROUP" -m 0700 "$BACKUP_NODE_ROOT"
`

**Expected result**

The backup authority has one node-scoped write boundary.

**Verification**

`bash
test "$(stat -c '%U:%G' "$BACKUP_NODE_ROOT")" = "$BACKUP_USER:$BACKUP_GROUP"
test "$(stat -c '%a' "$BACKUP_NODE_ROOT")" = "700"
test "$(findmnt -n -o TARGET --target "$BACKUP_NODE_ROOT")" = "$KOA_BACKUP_ROOT"
`

This step does not claim backup success.

A backup claim requires the separate backup procedure and owner-approved restore evidence.

---

### Step 12 — Validate cross-owner write denial

**Objective**

Prove that one component runtime identity cannot write another owner's authoritative boundary.

**Command**

Select two distinct active components whose test fixtures permit this negative test:

`bash
: "${SOURCE_SERVICE_USER:?}"
: "${TARGET_AUTHORITATIVE_PATH:?}"

test -d "$TARGET_AUTHORITATIVE_PATH"
test ! -L "$TARGET_AUTHORITATIVE_PATH"

if runuser -u "$SOURCE_SERVICE_USER" -- sh -c 'test -w "$1"' sh "$TARGET_AUTHORITATIVE_PATH"
then
 printf '%s
' "cross-owner authoritative path is writable" >&2
 exit 1
fi
`

**Expected result**

The command exits zero because the source identity cannot write the target path.

**Failure behavior**

Mark the node nonconformant and keep affected services stopped.

The test does not attempt a real write.

---

### Step 13 — Validate mount, owner, mode, and class

**Objective**

Produce one bounded machine-readable layout result.

**Command**

`bash
python3 - "$KOA_ACTIVE_ROOT" "$KOA_RECOVERY_ROOT" "$KOA_BACKUP_ROOT" <<'PY'
from pathlib import Path
import json
import os
import stat
import sys

active, recovery, backup = [Path(value).resolve for value in sys.argv[1:]]

required_active = {
 "components": 0o750,
 "artifacts": 0o750,
 "evidence": 0o750,
 "cache": 0o750,
 "staging": 0o750,
 "lost-and-found-review": 0o700,
}

result = {
 "active_root": str(active),
 "recovery_root": str(recovery),
 "backup_root": str(backup),
 "checks": [],
}

for name, expected_mode in required_active.items:
 path = active / name
 check = {
 "path": str(path),
 "exists": path.is_dir,
 "symlink": path.is_symlink,
 "owner_uid": path.stat.st_uid if path.exists else None,
 "mode": oct(stat.S_IMODE(path.stat.st_mode)) if path.exists else None,
 "expected_mode": oct(expected_mode),
 }
 check["pass"] = (
 check["exists"]
 and not check["symlink"]
 and check["owner_uid"] == 0
 and stat.S_IMODE(path.stat.st_mode) == expected_mode
 )
 result["checks"].append(check)

result["pass"] = all(item["pass"] for item in result["checks"])
print(json.dumps(result, indent=2))

if not result["pass"]:
 raise SystemExit(1)
PY
`

**Expected result**

The report contains paths, identities, modes, and outcomes only.

**Failure behavior**

Block activation of services whose boundary did not pass.

---

### Step 14 — Validate capacity and storage-exhaustion behavior

**Objective**

Verify declared minimum free space and safe failure before authoritative mutation.

**Command**

`bash
test "$(available_bytes "$KOA_ACTIVE_ROOT")" -ge "$ACTIVE_MIN_FREE_BYTES"
test "$(available_bytes "$KOA_RECOVERY_ROOT")" -ge "$RECOVERY_MIN_FREE_BYTES"
test "$(available_bytes "$KOA_BACKUP_ROOT")" -ge "$BACKUP_MIN_FREE_BYTES"
`

Run the registered storage-exhaustion test in an isolated non-authoritative test boundary.

**Expected result**

- the test boundary reaches its quota or declared limit;
- new authoritative-style test writes fail before truncation or partial commit;
- unrelated owner boundaries remain available;
- cache or staging cleanup does not delete authoritative data.

**Failure behavior**

Mark storage enforcement nonconformant.

Do not perform an exhaustion test against production authoritative data.

---

### Step 15 — Register validation evidence

**Objective**

Bind the result to the exact node and profile composition.

Evidence includes:

- `NODE_ID`;
- primary profile and version;
- overlays and versions;
- architecture and hardware class;
- active Release Set;
- active, recovery, and backup mount identities;
- encryption-validation result;
- top-level layout result;
- owner and mode checks;
- cross-owner write-denial result;
- capacity result;
- backup-target failure-domain result;
- test IDs and execution identities.

Register evidence through the canonical evidence procedure.

**Expected result**

Evidence is immutable and traceable.

**Failure behavior**

The layout can remain physically present, but the sovereign Linux conformance claim remains uncommitted.

## 11. Idempotency

`text
Idempotent: conditional
`

Idempotent operations:

- resolving identities and mount sources;
- validating paths;
- creating an absent directory with the expected owner and mode;
- validating an existing exact directory;
- recreating empty cache or staging directories;
- validating the backup namespace.

Non-idempotent or separately governed operations:

- moving existing data;
- changing directory owner for an active component;
- changing mount topology;
- changing encryption keys;
- restoring data;
- promoting a replica;
- changing an active database path;
- deleting a boundary;
- migrating from shared to dedicated physical storage.

The recipe refuses an existing path with unexpected owner, mode, type, mount, or class.

It does not repair such a mismatch automatically.

## 12. Validation

### 12.1 Profile validation

Validate:

- exact `sovereign_linux_node` profile version;
- overlays;
- compatibility;
- architecture;
- hardware class;
- active Release Set.

Use the canonical profile-composition and Release Set validators.

### 12.2 Storage-boundary validation

Validate:

- one owner per authoritative set;
- one runtime write identity;
- no direct cross-component writes;
- separate artifact and evidence authorities;
- replica, cache, projection, backup, and staging non-authority;
- owner-scoped migrations and restore;
- explicit retention and deletion;
- storage-exhaustion behavior.

### 12.3 Encryption validation

The active profile's encryption verifier confirms:

- active data encryption;
- backup encryption where required;
- recovery encryption where required;
- correct key scope;
- key rotation and recovery references;
- no ordinary storage of private key material.

### 12.4 Backup validation

A valid backup claim additionally requires:

- exact source scope;
- consistent capture;
- integrity protection;
- encryption;
- retention;
- durable storage;
- inventory completeness;
- successful owner-approved restore test into a clean compatible boundary.

This recipe verifies only layout and target availability.

### 12.5 Offline validation

For `sovereign_offline`, disconnect external network authority and verify that:

- required authoritative data remains local;
- required artifacts and Release Set remain locally available;
- local policy and identity continue;
- recovery material remains available;
- local evidence can be registered;
- backup behavior follows the offline contract;
- no unavailable external storage service is the sole source for a core capability.

### 12.6 Applicable documentation checks

`bash
python docs/tools/check_profile_composition.py
python docs/tools/check_component_boundaries.py
python docs/tools/check_release_sets.py
python docs/tools/check_artifact_contracts.py
python docs/tools/check_traceability.py
python docs/tools/check_canonical_ownership.py
python docs/tools/check_interfile_locks.py
python docs/tools/validate_docs.py
`

### 12.7 Success criteria

The recipe succeeds when:

- all three roots resolve to approved mounts;
- active storage encryption passes;
- backup failure-domain validation passes;
- top-level paths are root-owned and non-symlink;
- every included component has only declared classes;
- authoritative paths are `0700` and owner-specific;
- artifact and evidence writers are separate;
- cross-owner write denial passes;
- capacity thresholds pass;
- caches and staging remain non-authoritative;
- recovery and backup roots remain inaccessible to ordinary component writers;
- complete exact evidence is registered.

## 13. Failure Handling

| Failure | Safe state | Required response |
| --- | --- | --- |
| Profile or overlay unresolved | No layout mutation | Resolve canonical profile |
| Active Release Set unresolved | No service activation | Resolve compatible Release Set |
| Active mount not encrypted as required | Node claim blocked | Correct storage mapping through approved procedure |
| Root is a symlink | Procedure blocked | Investigate and replace through owner-approved migration |
| Unexpected existing content | No move or deletion | Attribute owner and create migration plan |
| Wrong owner or mode | Affected service stopped | Investigate before correcting |
| Component identity missing | Component boundary not created | Provision identity through canonical process |
| Shared runtime credential detected | Node nonconformant | Separate identities and rotate credentials |
| Artifact writer unavailable | Artifact activation blocked | Restore artifact authority |
| Evidence writer unavailable | Critical transitions uncommitted | Restore evidence path |
| Recovery target unavailable | Recovery claim blocked | Restore target before claim |
| Backup target unavailable | Backup claim fails | Restore approved distinct target |
| Cross-owner write possible | Affected services stopped | Correct permissions or physical mapping; assess exposure |
| Capacity below minimum | New affected writes blocked | Free disposable space or expand approved capacity |
| Storage exhaustion truncates test data | Node nonconformant | Correct quota and write-path behavior |
| Restore attempted into active path | Restore blocked | Use clean candidate boundary and owner procedure |
| Unattributed recovered file | Quarantine only | Identify owner; never place directly into authoritative path |
| Evidence registration fails | Claim uncommitted | Reconcile evidence storage |

Failures remain capability- and owner-scoped where possible.

## 14. Rollback

### 14.1 Rollback scope

Rollback is limited to empty paths created by this recipe.

The recipe never rolls back:

- a filesystem;
- encryption;
- an existing data migration;
- an active database;
- a backup;
- a restore;
- a Release Set.

### 14.2 Preconditions

Before removing a created directory:

- exact path is known;
- directory is empty;
- no service uses it;
- it belongs to the current recipe execution;
- owner and mount match;
- no authoritative data was written.

### 14.3 Remove one empty component boundary

`bash
: "${COMPONENT_ID:?}"

COMPONENT_ROOT="$KOA_ACTIVE_ROOT/components/$COMPONENT_ID"

find "$COMPONENT_ROOT" -mindepth 1 -maxdepth 1 -type d -empty -delete
rmdir "$COMPONENT_ROOT" 2>/dev/null || true
`

Do not use recursive deletion.

### 14.4 Remove empty top-level paths

Only during initial provisioning rollback:

`bash
for name in lost-and-found-review staging cache evidence artifacts components; do
 rmdir "$KOA_ACTIVE_ROOT/$name" 2>/dev/null || true
done
`

Keep `layout-version` only when the layout remains active.

### 14.5 Forward repair

When data, schema, artifacts, or active services used a new boundary, rollback may be unsafe.

Use the owner-approved migration, restore, or forward-repair procedure.

Do not move data back with ad hoc file copies.

## 15. Cleanup and Removal

### 15.1 Routine cleanup

Routine cleanup can remove:

- expired staging candidates;
- failed activation staging;
- rebuildable caches;
- expired temporary files;
- owner-approved old checkpoints;
- quarantined files after disposition.

It shall not remove:

- authoritative data;
- required replicas;
- required audit or evidence;
- active artifacts;
- backup history;
- recovery material.

### 15.2 Cache cleanup

Run under the owning component identity and within its exact cache path.

`bash
: "${COMPONENT_ID:?}"
CACHE_ROOT="$KOA_ACTIVE_ROOT/cache/$COMPONENT_ID"

test -d "$CACHE_ROOT"
test ! -L "$CACHE_ROOT"
`

Use the component's cache cleanup command.

Do not recursively delete arbitrary cache files when the component requires an index or manifest transaction.

### 15.3 Staging cleanup

The lifecycle authority identifies:

- artifact or operation owner;
- lifecycle state;
- retention;
- active lease;
- retry or repair dependency.

Only unreferenced expired staging is removed.

### 15.4 Component retirement

Component retirement requires:

1. stop owner writes;
2. export or retain required data;
3. complete retention and deletion decisions;
4. complete backup and restore evidence;
5. revoke service identities;
6. remove routing and queues;
7. verify no Release Set or recovery dependency remains;
8. remove empty boundaries through the owner-approved retirement procedure.

This recipe does not perform retirement.

## 16. Observability and Evidence

### 16.1 Permitted observations

- mount target and source identity;
- filesystem type;
- read-only state;
- capacity and available bytes;
- owner and group;
- permission mode;
- boundary class;
- directory count;
- validation result;
- active profile and Release Set identities.

### 16.2 Prohibited observations

Do not collect:

- file contents;
- secret values;
- private key material;
- unrestricted filenames inside tenant or component data;
- database rows;
- media content;
- personal or cultural content;
- full environment dumps.

### 16.3 Metrics

Useful storage metrics include:

- used and available bytes by boundary;
- inode use where relevant;
- write latency and errors;
- durability and sync failures;
- queue and checkpoint storage;
- replica lag;
- backup age and verification status;
- restore-test status;
- staging age;
- cache size;
- evidence-store write health.

Metrics remain owner- and profile-scoped.

### 16.4 Receipts

Critical operations can require receipts for:

- physical storage migration;
- replica failover;
- backup completion;
- restore selection and activation;
- emergency storage repair;
- Release Set activation affecting storage;
- deletion or cryptographic erasure;
- break-glass access.

Directory creation alone does not create application authority.

### 16.5 Evidence registration

Evidence follows `docs/09-conformance/05-test-evidence.md`.

A screenshot or directory listing without node, profile, test, subject, environment, and assertion identities is not sufficient.

## 17. Offline Behavior

`text
offline_capable
`

The layout can be provisioned and validated without Internet access when the node has locally admitted:

- profile contracts;
- component registry;
- Release Set;
- tools;
- identities;
- policies;
- trust material;
- tests;
- evidence storage.

For `sovereign_offline`:

- required authoritative data remains local;
- required recovery material remains local;
- required artifacts and policy bundles remain local;
- backup and restore use locally available approved targets;
- external storage is not the sole holder of core state;
- evidence can be retained locally and synchronized later through an authorized path.

Network loss does not authorize a weaker storage boundary.

## 18. Compatibility and Versioning

| Dependency | Compatible condition | Blocking condition |
| --- | --- | --- |
| Sovereign Linux profile | Exact active version accepts this mapping | Storage topology differs without approved mapping |
| High-assurance overlay | All added physical, key, custody, and evidence controls pass | Shared physical boundary violates overlay |
| Sovereign-offline overlay | Required data, artifacts, recovery, backup, and evidence are local | External provider is sole holder of core state |
| Component contract | Owner, classes, identity, migrations, and restore resolve | Component storage ownership unresolved |
| Artifact contracts | Channel, provenance, integrity, and lifecycle resolve | Artifact path used as authority without admission |
| Evidence contracts | Evidence writer and immutable registration resolve | Evidence path unavailable or mutable beyond contract |
| Backup contract | Distinct target and restore tests resolve | Backup target shares prohibited failure domain |
| Recipe versions | `1.x` | Major root, class, authority, or lifecycle change |

A major version is required when changing:

- top-level roots;
- owner model;
- physical-layout model;
- backup or recovery mapping;
- artifact-channel mapping;
- evidence mapping;
- rollback or cleanup safety.

## 19. AI Execution Protocol

An AI agent applying this recipe must:

1. load active AI context;
2. verify recipe status and version;
3. resolve exact node, profile, overlays, architecture, and Release Set;
4. resolve every component and service identity;
5. resolve every component storage class;
6. verify mount and encryption evidence before mutation;
7. refuse repartitioning, formatting, key generation, restore, migration, or recursive deletion under this recipe;
8. execute one atomic directory-creation step at a time;
9. verify owner, group, mode, symlink status, and mount after each step;
10. stop on unexpected existing content;
11. stop on missing capacity values;
12. run cross-owner negative tests without writing test data;
13. record only bounded structural evidence;
14. never inspect or summarize stored payloads;
15. leave services stopped when their boundary does not pass;
16. report `blocked` rather than inventing a filesystem, key, quota, device, user, or profile value.

The agent must not:

- infer ownership from directory location;
- use root access as application authority;
- correct ownership recursively;
- merge component directories;
- promote restored or replicated state;
- write directly into authoritative storage;
- store secret values;
- declare backup success without restore evidence;
- treat encryption alone as storage conformance.

### 19.1 Example execution summary

`json
{
 "recipe_id": "RECIPE-SLN-004",
 "recipe_version": "1.0.0",
 "node_id": "node-sovereign-hub-01",
 "primary_profile_id": "sovereign_linux_node",
 "overlay_ids": ["sovereign_offline"],
 "release_set_id": "release-set-sovereign-node-2026.08.03.1",
 "active_root": "/var/lib/koa",
 "recovery_root": "/var/lib/koa-recovery",
 "backup_root": "/mnt/koa-backup",
 "created_boundaries": [
 "components",
 "artifacts",
 "evidence",
 "cache",
 "staging",
 "lost-and-found-review"
 ],
 "tests_run": [
 "profile_composition",
 "storage_encryption",
 "layout_owner_and_mode",
 "cross_owner_write_denial",
 "backup_failure_domain"
 ],
 "evidence_ids": [],
 "result": "pass"
}
`

The example identifiers are illustrative and do not alter canonical profile or node records.

## 20. Troubleshooting

### Active root is not a mount point

**Signal**

`text
mountpoint reports false for /var/lib/koa
`

**Likely causes**

- the data filesystem did not mount;
- the mount unit failed;
- the path was created on the root filesystem;
- recovery boot changed the topology.

**Action**

Stop component services. Restore the profile-declared mount through the system lifecycle procedure. Do not continue and write into the fallback directory.

---

### Active storage encryption cannot be proven

**Signal**

The observed source cannot be matched to the profile encryption inventory.

**Likely causes**

- wrong mount;
- missing mapper or device identity;
- stale inventory;
- unapproved replacement disk;
- recovery environment lacks required trust material.

**Action**

Keep the node claim blocked. Resolve the storage and key inventory through the data-at-rest and Identity and Trust procedures.

Do not infer encryption from a device name.

---

### Component path has the wrong owner

**Signal**

`text
expected service identity differs from stat result
`

**Likely causes**

- component identity changed;
- data was copied by root;
- a restore preserved incorrect identity mapping;
- two components were mapped to one path.

**Action**

Stop the component, identify current data owner and migration state, then use an owner-approved migration or repair procedure.

Do not run recursive `chown`.

---

### Two components can write the same authoritative path

**Signal**

Cross-owner denial test fails.

**Likely causes**

- shared group write;
- shared service account;
- ACL grants;
- broad mount permissions;
- container process runs under the wrong host identity.

**Action**

Stop affected writers, preserve evidence, correct identity and path mapping, rotate exposed credentials where required, and rerun component-boundary tests.

---

### Backup target is on the active failure domain

**Signal**

The approved topology validator reports insufficient separation.

**Likely causes**

- backup is another directory on the same filesystem;
- backup is another partition on the same device;
- local removable media was not mounted;
- remote target resolves to local fallback storage.

**Action**

Do not claim a verified backup target. Mount or provision the profile-approved distinct target and run the backup and restore procedure.

---

### Unexpected files exist in a new boundary

**Signal**

A path expected to be empty contains unattributed files.

**Likely causes**

- prior failed deployment;
- restore or migration residue;
- wrong mount;
- component wrote before provisioning completed;
- operator copied files manually.

**Action**

Stop provisioning. Identify owner, artifact identity, lifecycle state, and provenance.

Move nothing into an authoritative path until owner admission or restore procedures approve it.

---

### Evidence storage cannot accept receipts

**Signal**

Evidence writer cannot persist required evidence.

**Likely causes**

- evidence mount full;
- wrong identity;
- read-only filesystem;
- encryption or integrity failure;
- evidence service unavailable.

**Action**

Keep receipt-before-commit transitions uncommitted. Preserve existing evidence and recover the evidence boundary.

## 21. Non-Normative Example

A sovereign node uses one profile-approved encrypted active-data filesystem mounted at:

`text
/var/lib/koa
`

The active profile includes an example component:

`text
component_id: example_component
service_user: koa-example-component
service_group: koa-example-component
declared classes: authoritative projections queues checkpoints logs temporary
`

The deployment authority creates:

`bash
export COMPONENT_ID="example_component"
export SERVICE_USER="koa-example-component"
export SERVICE_GROUP="koa-example-component"
export COMPONENT_STORAGE_CLASSES="authoritative projections queues checkpoints logs temporary"
`

The resulting path is:

`text
/var/lib/koa/components/example_component/
├── authoritative/ owned by koa-example-component, mode 0700
├── projections/ owned by koa-example-component, mode 0750
├── queues/ owned by koa-example-component, mode 0750
├── checkpoints/ owned by koa-example-component, mode 0750
├── logs/ owned by koa-example-component, mode 0750
└── temporary/ owned by koa-example-component, mode 0750
`

A `high_assurance` composition can mount the same authoritative path from a dedicated encrypted volume.

The component identifier, identity, interface, and owner remain unchanged.

## 22. Migration to Stronger Physical Isolation

This procedure does not perform the migration, but the accepted sequence is:

`text
declare target profile mapping
→ admit target storage and identities
→ quiesce owner writes
→ capture owner-consistent state
→ transfer through owner-approved migration
→ validate identity, schema, integrity, completeness, and policy
→ update owner routing atomically
→ enter restoring
→ run representative capability tests
→ commit new mapping
→ retain or retire prior boundary according to lifecycle
`

The migration shall preserve:

- owner identity;
- component interface;
- write exclusivity;
- schema and migration history;
- backup and restore behavior;
- Release Set compatibility;
- receipts and evidence.

A raw file copy is not a migration contract.

## 23. Author Checklist

- [x] Recipe identity and version are present.
- [x] Status is active and non-normative.
- [x] Exact primary profile is named.
- [x] Compatible overlays are explicit.
- [x] Baseline hardware storage requirements are preserved.
- [x] No filesystem, encryption, or volume manager is globalized.
- [x] No destructive disk operation is included.
- [x] Logical ownership is preserved.
- [x] Physical isolation remains profile-dependent.
- [x] Top-level paths are fixed and documented.
- [x] Component paths are owner-scoped.
- [x] Artifacts preserve four release channels.
- [x] Evidence is separate from business data.
- [x] Caches and staging remain non-authoritative.
- [x] Recovery and backup targets are separate.
- [x] Backup success is not claimed without restore evidence.
- [x] Symlink, mount, owner, mode, capacity, and cross-write checks are included.
- [x] Rollback removes only empty newly created paths.
- [x] AI execution forbids invented infrastructure values.
- [x] Offline behavior is explicit.

## 24. Review Checklist

- [x] One authoritative owner exists per data set.
- [x] One declared owner write path exists.
- [x] Direct cross-component writes are prohibited.
- [x] Shared physical storage does not create shared authority.
- [x] Separate physical storage does not create a second owner.
- [x] Runtime component identities cannot write artifacts, evidence, recovery, or backup.
- [x] Restored state remains candidate until owner validation.
- [x] Replica and backup promotion require owner procedures.
- [x] Resource exhaustion blocks safely.
- [x] Tenant, cultural, and sovereignty controls remain profile-owned.
- [x] Release Set compatibility remains required.
- [x] Break-glass cannot bypass owner interfaces.
- [x] Evidence is selective and payload-minimized.
- [x] Applicable locks and conformance checks are listed.

## 25. Final Recipe Rule

> This recipe maps one sovereign Linux node onto stable storage roots while preserving one logical owner and one owner-approved write path for every authoritative data set. Physical co-location is permitted only when the active profile accepts it and every identity, class, migration, backup, restore, failure, and evidence boundary remains enforceable. Stronger profiles can replace shared physical storage with separate volumes, devices, keys, nodes, or jurisdictions without changing ownership.
