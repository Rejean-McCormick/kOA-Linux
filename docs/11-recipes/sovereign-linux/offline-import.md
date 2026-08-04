<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-RECIPE-SOV-OFFLINE-001",
  "document_class": "recipe",
  "status": "active",
  "language": "en",
  "layer": "recipe",
  "scope": [
    "sovereign_linux_node",
    "sovereign_offline"
  ],
  "canonical_refs": [
    "generated/decision-index.json",
    "generated/profile-catalog.json",
    "contracts/profiles/sovereign-linux-node.profile.json",
    "contracts/profiles/sovereign-offline.profile.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "contracts/artifact-contracts/offline-bundle.schema.json",
    "contracts/artifact-contracts/release-set.schema.json",
    "contracts/artifact-contracts/decision-receipt.schema.json",
    "contracts/artifact-contracts/provenance-receipt.schema.json",
    "contracts/components/identity-and-trust.component.json",
    "contracts/components/resource-governor.component.json",
    "contracts/components/audit-broker.component.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-PROFILE-001",
    "DEC-REL-001",
    "DEC-DATA-001",
    "DEC-GOV-001"
  ],
  "requirement_ids": [
    "REQ-LIFE-VERIFY-001",
    "REQ-LIFE-VERIFY-002",
    "REQ-LIFE-VERIFY-003",
    "REQ-LIFE-VERIFY-005",
    "REQ-LIFE-VERIFY-007",
    "REQ-LIFE-VERIFY-008",
    "REQ-LIFE-VERIFY-010",
    "REQ-LIFE-VERIFY-012",
    "REQ-LIFE-VERIFY-013",
    "REQ-LIFE-VERIFY-016",
    "REQ-LIFE-VERIFY-018",
    "REQ-LIFE-VERIFY-019",
    "REQ-LIFE-VERIFY-021",
    "REQ-LIFE-VERIFY-022",
    "REQ-LIFE-VERIFY-023",
    "REQ-LIFE-VERIFY-024",
    "REQ-LIFE-VERIFY-025",
    "REQ-LIFE-VERIFY-026",
    "REQ-LIFE-VERIFY-027",
    "REQ-LIFE-VERIFY-028",
    "REQ-LIFE-REL-005",
    "REQ-LIFE-REL-006",
    "REQ-LIFE-REL-010",
    "REQ-LIFE-REL-012",
    "REQ-LIFE-REL-013",
    "REQ-LIFE-REL-014",
    "REQ-LIFE-REL-015",
    "REQ-LIFE-REL-016",
    "REQ-LIFE-REL-019",
    "REQ-LIFE-REL-021",
    "REQ-LIFE-REL-022",
    "REQ-LIFE-REL-025",
    "REQ-LIFE-REL-026",
    "REQ-SEC-TRUST-009",
    "REQ-SEC-TRUST-010",
    "REQ-SEC-TRUST-011",
    "REQ-SEC-TRUST-012",
    "REQ-SEC-TRUST-017",
    "REQ-SEC-TRUST-021",
    "REQ-SEC-TRUST-022",
    "REQ-SEC-TRUST-023",
    "REQ-SEC-TRUST-025",
    "REQ-SEC-TRUST-027",
    "REQ-OPS-INC-014",
    "REQ-OPS-INC-015",
    "REQ-OPS-INC-016",
    "REQ-OPS-INC-023",
    "REQ-OPS-INC-024",
    "REQ-OPS-INC-026"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
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
    "sovereign-linux",
    "sovereign-offline",
    "offline-import",
    "quarantine",
    "artifact-verification",
    "release-set",
    "trust-roots",
    "atomic-activation",
    "receipts"
  ],
  "normative": false
}
KOA:DOC-META:END -->

# Offline Import for Sovereign Linux

> **Recipe status:** Non-normative implementation guidance.  
> The active profile, artifact, release, trust, component, resource, evidence, and incident contracts take precedence.

## 1. Purpose

This recipe shows one way to transfer and import signed release artifacts into a sovereign Linux node that cannot rely on an online repository or live control plane.

The procedure separates:

1. removable-media transport;
2. read-only acquisition;
3. local quarantine;
4. bundle and artifact verification;
5. compatibility and Release Set evaluation;
6. owner-controlled staging;
7. owner-controlled activation;
8. receipt and evidence custody;
9. rollback or forward repair.

An offline bundle is a transport and distribution object. It does not become release authority, component-data authority, trust authority, policy authority, or activation authority merely because it is signed or physically controlled.

## 2. Applicability and Preconditions

Use this recipe when:

- the primary profile is `sovereign_linux_node`;
- the `sovereign_offline` overlay is active, or the profile contract explicitly permits the same offline-import behavior;
- the target already contains a valid bootstrap trust set for offline release verification;
- the active artifact contracts, release-channel definitions, and verifier are installed locally;
- sufficient quarantine, staging, rollback, and evidence storage is available;
- the node has a usable local time source or an approved signed-time procedure;
- the operator can identify the intended removable-media partition through a stable device path;
- an offline-import authorization exists when the effective profile requires one;
- recovery media and the last valid release state are available.

Additional controls can apply when `high_assurance` is composed, including dual control, hardware-backed verification, independent custody, or witnessed media handling.

This recipe does not cover:

- creating or signing an offline bundle;
- accepting an unregistered artifact class;
- bootstrapping arbitrary new trust from ordinary bundle contents;
- bypassing component-owned migration or import interfaces;
- activating every artifact through one shared database transaction;
- copying files directly into live component storage;
- importing production secrets from removable media;
- mounting untrusted media with execution enabled;
- partial import of an invalid or incomplete bundle.

## 3. Bundle, Trust, and Directory Model

### 3.1 Example bundle layout

The transport directory can use a layout such as:

```text
offline-bundle/
├── bundle.json
├── manifest.sha256
├── manifest.sha256.sig
├── release-set.json
├── revocation-snapshot.json
├── artifacts/
│   ├── system/
│   ├── services/
│   ├── governance/
│   └── knowledge/
├── receipts/
└── metadata/
    └── transfer-provenance.json
```

The exact fields and required members remain owned by the active offline-bundle and artifact contracts.

The manifest covers every bundle member except the detached signature file itself. Each artifact retains its own identity, class, channel, integrity, provenance, trust, compatibility, and lifecycle records.

### 3.2 Local directory layout

This recipe uses:

```text
/var/lib/koa/offline-import/
├── quarantine/
├── verified/
├── staging/
├── receipts/
├── evidence/
└── rejected/
```

Suggested ownership:

```text
root:koa-import
```

Suggested permissions:

```text
0750 directories
0640 ordinary records
0600 restricted evidence
```

The verifier and activation services receive only the directories required by their contracts.

### 3.3 Trust model

The node begins with a previously trusted local release-verification context.

Example implementation paths:

```text
/etc/koa/trust/offline-release-keyring.gpg
/etc/koa/trust/trust-set.json
/etc/koa/trust/revocation-state.json
```

The offline bundle can carry certificates, signer chains, revocation snapshots, and proposed trust-update artifacts for validation. An ordinary bundle does not modify the active trust store.

A trust-store update follows a separate authorized trust-update contract with complete quarantine, validation, atomic replacement, last-valid-set preservation, and recovery receipts.

## 4. Prepare the Node and Lock the Import Session

Create the service group and directories according to the host's identity-management recipe. Then create the import tree:

```bash
set -euo pipefail

IMPORT_ROOT="/var/lib/koa/offline-import"

sudo install -d -o root -g koa-import -m 0750 \
  "$IMPORT_ROOT" \
  "$IMPORT_ROOT/quarantine" \
  "$IMPORT_ROOT/verified" \
  "$IMPORT_ROOT/staging" \
  "$IMPORT_ROOT/receipts" \
  "$IMPORT_ROOT/evidence" \
  "$IMPORT_ROOT/rejected"

sudo install -d -o root -g root -m 0755 /run/koa
```

Use a host-wide lock so two import sessions cannot stage or activate overlapping artifacts concurrently:

```bash
exec 9>/run/koa/offline-import.lock

if ! flock -n 9; then
  printf '%s\n' "Another offline import is active." >&2
  exit 75
fi
```

Record the target context before touching the transport:

```bash
TARGET_PROFILE="sovereign_linux_node+sovereign_offline"
TARGET_NODE_ID="$(
  cat /etc/koa/node-id
)"

ACTIVE_AUTHORITY_SET="$(
  cat /etc/koa/authority-set-id
)"

ACTIVE_RELEASE_SET="$(
  cat /var/lib/koa/releases/active-release-set-id
)"

export TARGET_PROFILE TARGET_NODE_ID
export ACTIVE_AUTHORITY_SET ACTIVE_RELEASE_SET

printf '%s\n' \
  "target_node=$TARGET_NODE_ID" \
  "target_profile=$TARGET_PROFILE" \
  "active_authority_set=$ACTIVE_AUTHORITY_SET" \
  "active_release_set=$ACTIVE_RELEASE_SET"
```

Stop when any required identity or active-state record cannot be resolved.

## 5. Mount the Transport Read Only and Copy to Quarantine

Identify the intended partition through a stable path such as:

```text
/dev/disk/by-id/usb-VENDOR_PRODUCT_SERIAL-part1
```

Set the exact path manually after comparing serial number, size, filesystem, and custody record:

```bash
TRANSPORT_DEVICE="/dev/disk/by-id/usb-VENDOR_PRODUCT_SERIAL-part1"
MEDIA_MOUNT="/mnt/koa-offline-import"

test -b "$TRANSPORT_DEVICE"

lsblk \
  --paths \
  --output NAME,SIZE,FSTYPE,RO,MOUNTPOINTS,SERIAL \
  "$TRANSPORT_DEVICE"
```

Mount without executable or device semantics:

```bash
sudo install -d -m 0750 "$MEDIA_MOUNT"

sudo mount \
  -o ro,nosuid,nodev,noexec \
  "$TRANSPORT_DEVICE" \
  "$MEDIA_MOUNT"

findmnt --target "$MEDIA_MOUNT"
```

Resolve the bundle directory and create a local import identity:

```bash
SOURCE_BUNDLE="$MEDIA_MOUNT/offline-bundle"

test -d "$SOURCE_BUNDLE"
test -f "$SOURCE_BUNDLE/bundle.json"
test -f "$SOURCE_BUNDLE/manifest.sha256"
test -f "$SOURCE_BUNDLE/manifest.sha256.sig"

BUNDLE_ID="$(
  jq -er '.bundle_id' "$SOURCE_BUNDLE/bundle.json"
)"

BUNDLE_VERSION="$(
  jq -er '.version' "$SOURCE_BUNDLE/bundle.json"
)"

IMPORT_SUFFIX="$(
  od -An -N4 -tx1 /dev/urandom |
    tr -d ' \n'
)"

IMPORT_ID="${BUNDLE_ID}-${BUNDLE_VERSION}-${IMPORT_SUFFIX}"
QUARANTINE_DIR="$IMPORT_ROOT/quarantine/$IMPORT_ID"

sudo install -d -o root -g koa-import -m 0750 \
  "$QUARANTINE_DIR"
```

Reject unsafe source structure before copying:

```bash
if find "$SOURCE_BUNDLE" -xdev -type l -print -quit |
   grep -q .; then
  printf '%s\n' "Symbolic links are not accepted." >&2
  exit 65
fi

if find "$SOURCE_BUNDLE" -xdev -type f -links +1 -print -quit |
   grep -q .; then
  printf '%s\n' "Hard-linked files are not accepted." >&2
  exit 65
fi

if find "$SOURCE_BUNDLE" -xdev \
     \( -type b -o -type c -o -type p -o -type s \) \
     -print -quit |
   grep -q .; then
  printf '%s\n' "Special files are not accepted." >&2
  exit 65
fi
```

Copy without preserving untrusted ownership or special metadata:

```bash
sudo cp -a \
  --no-preserve=ownership \
  "$SOURCE_BUNDLE/." \
  "$QUARANTINE_DIR/"

sudo chown -R root:koa-import "$QUARANTINE_DIR"
sudo find "$QUARANTINE_DIR" -type d -exec chmod 0750 {} +
sudo find "$QUARANTINE_DIR" -type f -exec chmod 0640 {} +
sudo sync
```

Unmount and physically remove the transport before verification:

```bash
sudo umount "$MEDIA_MOUNT"
sudo rmdir "$MEDIA_MOUNT"

printf '%s\n' \
  "Remove the transport medium and complete the custody record."
```

Verification operates only on the immutable local quarantine copy.

## 6. Verify Bundle Structure, Integrity, Trust, and Compatibility

### 6.1 Apply input and resource bounds

Before parsing detailed content, enforce locally configured limits for:

- total bundle bytes;
- member count;
- maximum individual file size;
- path depth;
- manifest line length;
- verifier CPU time;
- verifier memory;
- temporary storage;
- receipt and evidence size.

Example basic limits:

```bash
MAX_BUNDLE_BYTES=$((64 * 1024 * 1024 * 1024))
MAX_MEMBERS=10000
MAX_MEMBER_BYTES=$((16 * 1024 * 1024 * 1024))

BUNDLE_BYTES="$(
  sudo du -sb "$QUARANTINE_DIR" |
    awk '{print $1}'
)"

MEMBER_COUNT="$(
  sudo find "$QUARANTINE_DIR" -xdev -type f |
    wc -l
)"

test "$BUNDLE_BYTES" -le "$MAX_BUNDLE_BYTES"
test "$MEMBER_COUNT" -le "$MAX_MEMBERS"

if sudo find "$QUARANTINE_DIR" -xdev -type f \
     -size "+${MAX_MEMBER_BYTES}c" -print -quit |
   grep -q .; then
  printf '%s\n' "A bundle member exceeds the local limit." >&2
  exit 65
fi
```

These are example implementation limits. The active profile and artifact contracts remain authoritative.

### 6.2 Verify the detached manifest signature

Use a verifier that reads only the dedicated offline release keyring:

```bash
OFFLINE_KEYRING="/etc/koa/trust/offline-release-keyring.gpg"

test -r "$OFFLINE_KEYRING"

sudo -u koa-import \
  gpgv \
  --keyring "$OFFLINE_KEYRING" \
  "$QUARANTINE_DIR/manifest.sha256.sig" \
  "$QUARANTINE_DIR/manifest.sha256"
```

Do not use the operator's personal keyring, a browser trust store, the operating-system web trust store, or a key embedded only in the bundle as the authority for this check.

### 6.3 Verify every manifest digest

```bash
sudo -u koa-import \
  sh -c '
    set -euo pipefail
    cd "$1"
    sha256sum --check --strict manifest.sha256
  ' sh "$QUARANTINE_DIR"
```

Confirm that the manifest:

- contains every required bundle member;
- contains no absolute path;
- contains no `..` traversal;
- contains no duplicate path;
- uses the algorithm and scope declared by the bundle contract;
- agrees with the bundle identity and version.

### 6.4 Run the active bundle verifier

The following executable paths are illustrative deployment adapters. Bind them to the installed contract-owned verifier and compatibility engine:

```bash
BUNDLE_VERIFIER="/usr/libexec/koa/verify-offline-bundle"
COMPATIBILITY_CHECKER="/usr/libexec/koa/check-release-compatibility"

test -x "$BUNDLE_VERIFIER"
test -x "$COMPATIBILITY_CHECKER"

VERIFICATION_RECEIPT="$(
  sudo -u koa-import \
  "$BUNDLE_VERIFIER" \
    --bundle "$QUARANTINE_DIR" \
    --target-node "$TARGET_NODE_ID" \
    --effective-profile "$TARGET_PROFILE" \
    --authority-set "$ACTIVE_AUTHORITY_SET" \
    --trust-set /etc/koa/trust/trust-set.json \
    --revocation-state /etc/koa/trust/revocation-state.json \
    --output-dir "$IMPORT_ROOT/receipts"
)"

COMPATIBILITY_RECEIPT="$(
  sudo -u koa-import \
  "$COMPATIBILITY_CHECKER" \
    --release-set "$QUARANTINE_DIR/release-set.json" \
    --bundle "$QUARANTINE_DIR" \
    --active-release-set "$ACTIVE_RELEASE_SET" \
    --effective-profile "$TARGET_PROFILE" \
    --output-dir "$IMPORT_ROOT/receipts"
)"
```

The verifier evaluates:

- bundle identity and contract;
- manifest completeness;
- every artifact identity, version, class, and channel;
- artifact-specific schemas;
- exact integrity scopes;
- provenance and custody;
- signer identity and authorization scope;
- validity and offline revocation state;
- target node and profile;
- composed overlays;
- Release Set membership and compatibility;
- required system, services, governance, and knowledge channels;
- migration declarations;
- profile-specific assurance and evidence;
- prohibited trust additions;
- final bundle and artifact outcomes.

The complete bundle stays quarantined when one required member or relationship is failed, blocked, quarantined, revoked, ambiguous, or missing.

### 6.5 Handle time and revocation uncertainty

When the local clock, signed-time evidence, or revocation snapshot does not satisfy the active trust contract, keep the result blocked.

Do not:

- set the clock to make a certificate valid;
- ignore an expired revocation snapshot;
- accept a signer through a weaker root;
- fall back to public web trust;
- use operator familiarity as trust evidence.

## 7. Stage Through Component-Owned Import Boundaries

Verification completion does not install, import, migrate, publish, or activate artifacts.

Create a staging plan from the verified Release Set:

```bash
IMPORT_PLANNER="/usr/libexec/koa/plan-offline-import"
STAGING_PLAN="$IMPORT_ROOT/staging/$IMPORT_ID-plan.json"

test -x "$IMPORT_PLANNER"

sudo -u koa-import \
  "$IMPORT_PLANNER" \
    --bundle "$QUARANTINE_DIR" \
    --verification-receipt "$VERIFICATION_RECEIPT" \
    --compatibility-receipt "$COMPATIBILITY_RECEIPT" \
    --current-release-set "$ACTIVE_RELEASE_SET" \
    --output "$STAGING_PLAN"
```

Review that the plan identifies:

- every artifact and channel;
- owning component or lifecycle authority;
- destination staging boundary;
- required policy decision;
- required Resource Governor admission;
- migration steps;
- ordered activation;
- rollback or forward-repair path;
- last-valid state;
- expected receipts;
- operator or multi-party approvals.

Stage only through owner adapters:

```bash
SYSTEM_STAGER="/usr/libexec/koa/stage-system-artifact"
SERVICE_STAGER="/usr/libexec/koa/stage-service-artifact"
GOVERNANCE_STAGER="/usr/libexec/koa/stage-governance-artifact"
KNOWLEDGE_STAGER="/usr/libexec/koa/stage-knowledge-artifact"

for adapter in \
  "$SYSTEM_STAGER" \
  "$SERVICE_STAGER" \
  "$GOVERNANCE_STAGER" \
  "$KNOWLEDGE_STAGER"
do
  test -x "$adapter"
done
```

Each adapter receives only artifacts that belong to its release channel and component boundary.

Do not copy bundle members into live databases, active configuration directories, active policy stores, active Runtime Pack directories, or another component's private files.

## 8. Activate Atomically and Preserve the Last Valid State

Activation follows the Release Set plan and each owner's activation contract.

A typical sequence is:

1. preserve the current active identities and recovery pointers;
2. confirm the verification and compatibility receipts remain valid;
3. confirm policy authorization where required;
4. obtain resource admission;
5. apply any declared reversible preparation;
6. activate one owner's atomic boundary;
7. validate health, readiness, data integrity, and receipts;
8. continue to the next owner only when the ordered plan permits it;
9. stop and recover when a required transition fails;
10. record the resulting Release Set state.

Example orchestrator adapter:

```bash
ACTIVATOR="/usr/libexec/koa/activate-offline-release-set"
ACTIVATION_RECEIPT_DIR="$IMPORT_ROOT/receipts/$IMPORT_ID"

sudo install -d -o root -g koa-import -m 0750 \
  "$ACTIVATION_RECEIPT_DIR"

test -x "$ACTIVATOR"

sudo "$ACTIVATOR" \
  --plan "$STAGING_PLAN" \
  --verification-receipt "$VERIFICATION_RECEIPT" \
  --compatibility-receipt "$COMPATIBILITY_RECEIPT" \
  --preserve-last-valid \
  --receipt-dir "$ACTIVATION_RECEIPT_DIR"
```

The orchestrator coordinates owner adapters. It does not acquire ownership of their data or activation boundaries.

After activation:

```bash
cat /var/lib/koa/releases/active-release-set-id

systemctl is-system-running || true

/usr/libexec/koa/validate-active-release \
  --effective-profile "$TARGET_PROFILE" \
  --receipt-dir "$ACTIVATION_RECEIPT_DIR"
```

A successful file copy, package installation, service startup, or signature check does not by itself prove activation success.

## 9. Preserve Receipts, Evidence, and Import Custody

Record:

- import identity;
- source media identity and custody;
- bundle identity and version;
- source and target;
- operator identities;
- import authorization;
- local authority set;
- active and candidate Release Sets;
- bundle and artifact verification results;
- trust roots and scopes without secret material;
- revocation and time context;
- staging results;
- owner activation results;
- health and readiness validation;
- rollback or forward-repair state;
- rejected or quarantined reasons;
- final disposition.

Example custody record:

```bash
CUSTODY_RECORD="$IMPORT_ROOT/evidence/$IMPORT_ID-custody.json"

sudo -u koa-import \
  jq -n \
    --arg import_id "$IMPORT_ID" \
    --arg node_id "$TARGET_NODE_ID" \
    --arg profile "$TARGET_PROFILE" \
    --arg bundle_id "$BUNDLE_ID" \
    --arg bundle_version "$BUNDLE_VERSION" \
    --arg authority_set "$ACTIVE_AUTHORITY_SET" \
    --arg previous_release_set "$ACTIVE_RELEASE_SET" \
    --arg verification_receipt "$VERIFICATION_RECEIPT" \
    --arg compatibility_receipt "$COMPATIBILITY_RECEIPT" \
    --arg created_at "$(date --iso-8601=seconds)" \
    '{
      import_id: $import_id,
      target_node_id: $node_id,
      effective_profile: $profile,
      bundle: {
        bundle_id: $bundle_id,
        version: $bundle_version
      },
      authority_set_id: $authority_set,
      previous_release_set_id: $previous_release_set,
      verification_receipt: $verification_receipt,
      compatibility_receipt: $compatibility_receipt,
      created_at: $created_at,
      disposition: "pending_finalization"
    }' |
  sudo tee "$CUSTODY_RECORD" >/dev/null

sudo chown root:koa-import "$CUSTODY_RECORD"
sudo chmod 0640 "$CUSTODY_RECORD"
```

Transfer receipts and restricted evidence to the active evidence authority after successful validation. Public or operator-visible summaries remain separate from private proof.

Do not include:

- private keys;
- recovery secrets;
- bearer credentials;
- unrestricted personal data;
- full restricted payloads;
- unnecessary signer or operator identity detail.

## 10. Failure, Rejection, Rollback, and Cleanup

### 10.1 Failure handling

| Condition | Response |
| --- | --- |
| Media identity is uncertain | Do not mount; resolve custody first. |
| Media cannot mount read only | Reject the transport or use an approved forensic acquisition procedure. |
| Unsafe path, link, or special file appears | Reject the complete bundle. |
| Detached signature fails | Keep the complete bundle quarantined. |
| Manifest digest fails | Keep the complete bundle quarantined. |
| Bundle contract is unavailable | Record a blocked result and keep quarantine. |
| Required member is absent | Reject partial import and keep the bundle together. |
| Artifact class or channel mismatches | Reject the affected bundle result. |
| Trust root or signer scope fails | Reject without trying another trust domain. |
| Revocation or time context is stale | Keep the import blocked. |
| Release Set is incompatible | Preserve the current active Release Set. |
| Staging fails | Remove the candidate staging area through the owner adapter. |
| Activation fails | Restore the last valid owner state or enter declared forward repair. |
| Receipt or evidence path is unavailable | Apply the profile-owned fail or bounded-queue behavior. |
| Incident indicators appear | Preserve evidence and enter incident response. |

### 10.2 Move rejected material

```bash
REJECTED_DIR="$IMPORT_ROOT/rejected/$IMPORT_ID"

sudo mv "$QUARANTINE_DIR" "$REJECTED_DIR"
sudo chmod -R go-rwx "$REJECTED_DIR"
```

Retain rejected material only for the period required by incident, audit, or disposal policy.

### 10.3 Roll back a failed activation

Use only owner-controlled rollback commands identified in the staging plan:

```bash
ROLLBACK="/usr/libexec/koa/rollback-offline-release-set"

test -x "$ROLLBACK"

sudo "$ROLLBACK" \
  --plan "$STAGING_PLAN" \
  --restore-release-set "$ACTIVE_RELEASE_SET" \
  --receipt-dir "$ACTIVATION_RECEIPT_DIR"
```

Validate the restored state before resuming ordinary operation.

### 10.4 Final cleanup

After a successful import and evidence transfer:

```bash
sudo /usr/libexec/koa/finalize-offline-import \
  --import-id "$IMPORT_ID" \
  --retain-receipts \
  --retain-required-evidence \
  --remove-temporary-staging
```

Do not delete:

- active artifacts;
- last-valid recovery state;
- required verification and activation receipts;
- incident evidence;
- historical artifact identities;
- required custody records.

## 11. Validation and Adaptation Checklist

Before adopting this recipe, confirm:

- the effective configuration contains one active primary profile and the applicable offline overlay;
- the target node and authority-set identities resolve;
- the local bootstrap trust set is active and previously approved;
- ordinary bundles cannot modify trust stores;
- removable media is mounted read only with `nosuid`, `nodev`, and `noexec`;
- the bundle is copied to local quarantine before detailed verification;
- untrusted archives, links, special files, path traversal, and excessive input are rejected;
- manifest signatures use the dedicated scoped release keyring;
- every manifest digest is recomputed;
- bundle and artifact contracts resolve locally;
- every artifact class and release channel matches canonical contracts;
- provenance, trust, revocation, time, target, profile, overlays, and authorization are checked;
- Release Set completeness and compatibility are checked;
- failed, blocked, quarantined, or revoked material cannot leave quarantine;
- no artifact code, migration, macro, or plugin runs during verification;
- verification tools have bounded CPU, memory, storage, input, and duration;
- verification and activation remain separate transitions;
- each owner stages and activates only its boundary;
- no direct write reaches another component's authoritative data;
- policy and resource decisions remain separate from verification;
- the current active state and last-valid recovery state are preserved;
- activation is atomic within each owner boundary;
- every critical transition produces a receipt;
- private proof is separated from public or operator summaries;
- rollback and forward repair are tested;
- media, quarantine, staging, receipts, evidence, and rejected-material retention have explicit cleanup policies;
- offline incident handling works without central connectivity;
- tests and evidence apply to the exact node, profile, authority set, bundle, artifacts, Release Set, verifier, trust context, and activation request.

An adaptation is ready only after the active profile, artifact, trust, release, component, resource, test, and evidence owners approve its observable behavior.
