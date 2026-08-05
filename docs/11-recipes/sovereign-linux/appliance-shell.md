<!-- KOA:DOC-META:BEGIN GENERATED
{
 "doc_id": "DOC-RECIPE-SLN-APPLIANCE-001",
 "document_class": "non_normative_recipe",
 "status": "active",
 "language": "en",
 "layer": "recipes",
 "scope": [
 "profile:sovereign_linux_node",
 "profile_overlay:appliance_shell",
 "sovereign_linux_appliance_session"
 ],
 "canonical_refs": [
 "generated/profile-catalog.json",
 "contracts/profiles/sovereign-linux-node.profile.json",
 "contracts/profiles/appliance-shell.profile.json",
 "contracts/profiles/high-assurance.profile.json",
 "contracts/profiles/sovereign-offline.profile.json",
 "contracts/release-channels.contract.json",
 "contracts/artifact-classes.contract.json",
 "generated/component-catalog.json",
 "contracts/integration-types.contract.json",
 "generated/assertion-index.json#/locks/LOCK-IMPL-002",
 "generated/assertion-index.json#/locks/LOCK-LIFE-001",
 "generated/assertion-index.json#/locks/LOCK-LIFE-003",
 "generated/decision-index.json#/adrs/ADR-003",
 "generated/decision-index.json#/adrs/",
 "generated/test-catalog.json",
 "generated/evidence-catalog.json"
 ],
 "decision_ids": [
 "DEC-SHELL-001",
 "DEC-PROFILE-001",
 "DEC-ARI-001",
 "DEC-AI-001",
 "DEC-DATA-001",
 "DEC-GOV-001",
 "DEC-GATE-001",
 "DEC-CONTAINER-001",
 "DEC-HW-001",
 "DEC-REL-001"
 ],
 "requirement_ids": [],
 "lock_ids": [
 "LOCK-PROFILE-001",
 "LOCK-IMPL-001",
 "LOCK-IMPL-002",
 "LOCK-ARI-001",
 "LOCK-ARI-002",
 "LOCK-AI-001",
 "LOCK-AI-002",
 "LOCK-DATA-001",
 "LOCK-GOV-001",
 "LOCK-GATE-001",
 "LOCK-LIFE-001",
 "LOCK-LIFE-002",
 "LOCK-LIFE-003",
 "LOCK-LIFE-004"
 ],
 "exception_ids": [],
 "depends_on": [
 "DOC-RECIPES-000",
 "DOC-PROFILE-007",
 "DOC-SYS-002",
 "DOC-SYS-011",
 "DOC-SYS-017",
 "DOC-SEC-001",
 "DOC-SEC-008",
 "DOC-SEC-011",
 "DOC-OPS-000",
 "DOC-OPS-009",
 "DOC-CONF-010",
 "DOC-ADR-003"
 ],
 "tags": [
 "recipe",
 "sovereign-linux",
 "appliance-shell",
 "wayland",
 "embedded-web-engine",
 "systemd",
 "atomic-activation",
 "rollback",
 "offline",
 "recovery",
 "accessibility",
 "non-normative"
 ]
}
KOA:DOC-META:END -->

# Sovereign Linux Appliance Shell

> **Recipe classification:** Non-authoritative implementation guidance.
> **Risk class:** `operational_change`.
> **Primary profile:** `sovereign_linux_node`.
> **Required overlay:** `appliance_shell`.
> **Compatible strengthening overlays:** `high_assurance` and `sovereign_offline` only when the active profile registry permits the complete composition.
> **Authority rule:** `ADR-003`, the active profile contracts, artifact contracts, Release Set, security policy, and operating authority take precedence over this recipe.

## 1. Purpose

This recipe stages, activates, validates, rolls back, and safely degrades a restricted appliance session on a sovereign Linux node.

The appliance session combines:

- a maintained minimal Wayland compositor selected by the active profile;
- a focused native kOA session shell;
- a maintained embedded web engine for approved local product workspaces;
- local status, accessibility, session, and recovery surfaces;
- local Konnaxion, Orgo, or other registered workspace origins;
- profile-owned resource, security, lifecycle, and evidence controls.

The recipe preserves this boundary:

`text
verified composed profile
 ↓
complete compatible Release Set
 ↓
inactive staged shell artifacts
 ↓
native recovery and status checks
 ↓
atomic active-release switch
 ↓
service readiness and restricted-session tests
 ↓
accepted appliance session
`

The shell remains a presentation and session boundary.

It does not become the owner of component data, policy, identity, trust, UCKK state, publication state, release authority, or host privilege.

### 1.1 Result

A successful execution produces:

- an active `sovereign_linux_node + appliance_shell` composition;
- exact active and previous Release Set links;
- running local-origin, compositor, shell, and embedded-engine units;
- an independently available native recovery unit;
- a local readiness result;
- restricted navigation and permission results;
- offline or online behavior matching the active overlays;
- activation or rollback evidence.

### 1.2 Non-goals

This recipe does not:

- enable `appliance_shell` on an unregistered profile;
- impose Wayland minimalism on standard Linux desktops; this recipe does not impose that behavior outside the active overlay;
- prohibit GNOME, KDE Plasma, or another maintained desktop globally;
- select one mandatory compositor or web engine;
- install an unverified operating system;
- create a Release Set;
- approve artifacts;
- grant privilege;
- define application URLs or credentials;
- expose a general-purpose browser;
- enable external AI;
- make external voice required for navigation;
- replace profile-specific recovery runbooks;
- claim deployment conformance without the registered tests and evidence.

## 2. Applicability

### 2.1 Required effective composition

This recipe applies only when the effective composed profile contains:

`text
primary_profile: sovereign_linux_node
overlay: appliance_shell
`

Additional overlays can include:

`text
high_assurance
sovereign_offline
`

only when the active profile registry declares the combination compatible.

### 2.2 Profile effects

| Profile or overlay | Recipe effect |
| --- | --- |
| `sovereign_linux_node` | Supplies the signed Linux node, local authority, privileged broker, resource envelope, recovery, and Release Set behavior |
| `appliance_shell` | Activates the restricted Wayland session and embedded presentation boundary |
| `high_assurance` | Can add stronger identity, control separation, boot evidence, audit, session, and recovery controls |
| `sovereign_offline` | Requires complete local artifact, policy, trust, revocation, language, workspace, and recovery closure without Internet dependence |
| `user_lightweight` | Outside this recipe |
| `developer_linux_workstation` | Outside this recipe; a general maintained desktop remains permitted |
| `developer_windows_wsl` | Outside this recipe |
| `build_farm` | Outside this recipe |
| `control_plane` | Outside this recipe unless a separate profile composition defines a local console |

### 2.3 Reference implementation assumptions

The executable examples assume:

- Linux;
- systemd;
- a profile-approved privileged path;
- a Wayland compositor;
- a native shell;
- an embedded web engine;
- local workspace services;
- immutable Release Set directories;
- atomic symbolic-link selection of `active` and `previous`;
- `jq`, `curl`, `flock`, and standard GNU userland.

These are recipe assumptions, not global architecture.

A profile using another service manager or activation mechanism keeps the same authority, staging, verification, recovery, and rollback semantics.

### 2.4 Operational states

The recipe uses these explanatory states:

| State | Meaning |
| --- | --- |
| `staged` | Complete artifacts exist but are inactive |
| `preflight_passed` | Profile, Release Set, permissions, units, and local inputs passed recipe sanity checks |
| `activating` | The active pointer and units are changing under an exclusive lock |
| `accepting` | Readiness and restricted-session checks are running |
| `active` | Required checks passed |
| `degraded` | One bounded capability failed while native recovery remains available |
| `rolling_back` | The previous compatible Release Set is being restored |
| `blocked` | Required authority, compatibility, recovery, or evidence is unresolved |

Canonical lifecycle states remain in the artifact and profile contracts.

## 3. Preconditions

### 3.1 Accepted authority

Before executing state-changing steps, resolve:

- `DEC-SHELL-001`;
- `ADR-003`;
- the active `sovereign_linux_node` profile contract;
- the active `appliance_shell` overlay contract;
- any active `high_assurance` or `sovereign_offline` overlay;
- the target Release Set;
- the affected system, services, governance, and knowledge artifacts;
- the operating change record;
- activation authority;
- rollback or forward-repair behavior;
- evidence requirements.

Repository files, unit files, installed packages, or a compositor executable do not activate the overlay by themselves.

### 3.2 Local console and recovery

Perform first activation and recovery tests from an authorized local console.

Before changing the session:

- verify the profile-defined recovery environment;
- verify recovery media or recovery partition;
- verify local operator identity;
- verify the recovery unit or target;
- verify the previous known-good Release Set;
- verify a path to stop the shell and return to recovery;
- verify remote administration is not the only recovery path.

Do not perform the first offline or compositor-failure test over the only remote connection.

### 3.3 Node capacity

Resolve capacity from the active profile.

The current sovereign-node baseline expects at least:

- 8 CPU cores;
- 32 GiB memory;
- 1 TB encrypted SSD storage;
- retained active and previous Release Sets;
- staging capacity;
- recovery and backup capacity.

The profile can strengthen these values.

Check the actual node:

`bash
nproc
awk '/MemTotal/ { printf "%.1f GiB\n", $2 / 1024 / 1024 }' /proc/meminfo
lsblk --output NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS
findmnt --target /
`

A recipe check does not replace the active resource-envelope validator.

### 3.4 Artifact and Release Set readiness

The target Release Set is already:

- published;
- immutable;
- integrity-verified;
- provenance-verified;
- trust-verified;
- revocation-checked;
- profile-compatible;
- migration-compatible;
- staged as inactive content;
- accompanied by required tests and evidence.

The Release Set contains compatible identities for:

- `system`;
- `services`;
- `governance`;
- `knowledge`.

This recipe does not publish or sign artifacts.

### 3.5 Required local capabilities

Before activation, verify local availability of:

- identity and trust;
- revocation state;
- Governance Policy Runtime when selected;
- Resource Governor;
- kOA Node Agent and privileged broker;
- Audit Broker and evidence path;
- local language resources;
- local navigation;
- local Konnaxion and Orgo workspace services where selected;
- recovery;
- current and previous Release Sets.

Under `sovereign_offline`, every required item is locally available.

### 3.6 Required commands

The reference helper uses:

`text
bash
jq
systemctl
readlink
stat
find
flock
curl
ln
mv
`

Verify:

`bash
for command_name in \
 bash jq systemctl readlink stat find flock curl ln mv; do
 command -v "$command_name" >/dev/null ||
 printf 'missing: %s\n' "$command_name"
done
`

### 3.7 Environment-file location

Use a root-owned local environment file outside the Release Set.

Recommended reference location:

`text
/etc/koa/appliance-shell.env
`

The file contains paths, unit names, and local URLs.

It does not contain secret values.

Credentials remain protected references delivered through the selected service mechanism.

## 4. Inputs

### 4.1 Required values

The recipe requires:

| Variable | Meaning |
| --- | --- |
| `KOA_PROFILE_MANIFEST` | Active composed node-profile artifact |
| `KOA_RELEASE_ROOT` | Parent directory containing immutable Release Set directories |
| `KOA_RELEASE_SET_ID` | Exact staged Release Set identity |
| `KOA_ACTIVE_LINK` | Atomic link used by appliance units to resolve active artifacts |
| `KOA_PREVIOUS_LINK` | Link to the previous compatible Release Set |
| `KOA_LOCK_FILE` | Exclusive activation lock |
| `KOA_LOCAL_ORIGIN_UNIT` | Local application-origin service unit |
| `KOA_COMPOSITOR_UNIT` | Wayland compositor unit |
| `KOA_SHELL_UNIT` | Native kOA shell unit |
| `KOA_ENGINE_UNIT` | Embedded web-engine unit |
| `KOA_RECOVERY_UNIT` | Native recovery unit or target |
| `KOA_READY_URL` | Local readiness URL |
| `KOA_LOCAL_CA_FILE` | Optional local CA used by the readiness URL |
| `KOA_READY_TIMEOUT_SECONDS` | Readiness request timeout |

### 4.2 Reference environment file

Create `/etc/koa/appliance-shell.env` through the active configuration and privileged-change process:

`bash
KOA_PROFILE_MANIFEST=/etc/koa/authority/node-profile.json
KOA_RELEASE_ROOT=/var/lib/koa/releases
KOA_RELEASE_SET_ID=rs-2026.08.03-001

KOA_ACTIVE_LINK=/var/lib/koa/appliance-shell/active
KOA_PREVIOUS_LINK=/var/lib/koa/appliance-shell/previous
KOA_LOCK_FILE=/run/lock/koa/appliance-shell.lock

KOA_LOCAL_ORIGIN_UNIT=koa-local-workspaces.service
KOA_COMPOSITOR_UNIT=koa-wayland-compositor.service
KOA_SHELL_UNIT=koa-appliance-shell.service
KOA_ENGINE_UNIT=koa-embedded-web-engine.service
KOA_RECOVERY_UNIT=koa-appliance-recovery.target

KOA_READY_URL=https://127.0.0.1:8443/ready
KOA_LOCAL_CA_FILE=/etc/koa/trust/local-workspace-ca.pem
KOA_READY_TIMEOUT_SECONDS=10
`

The identifiers and paths are reference values.

The active profile, unit definitions, artifact contracts, and local operating configuration own deployment-specific values.

### 4.3 Reference staged layout

The helper expects this reference layout:

`text
/var/lib/koa/releases/
└── rs-2026.08.03-001/
 ├── release-set.json
 ├── system/
 ├── services/
 ├── governance/
 └── knowledge/
`

The active and previous links remain outside the immutable Release Set:

`text
/var/lib/koa/appliance-shell/active
/var/lib/koa/appliance-shell/previous
`

Units resolve artifacts through the active link.

They do not read mutable files from an operator home directory or development workspace.

### 4.4 Unit responsibility map

| Unit | Responsibility |
| --- | --- |
| Local-origin unit | Serves approved local product workspaces through registered component interfaces |
| Compositor unit | Owns the restricted Wayland display session |
| Shell unit | Owns native session, workspace selection, status, accessibility entry, and recovery entry |
| Engine unit | Presents approved local web workspaces under bounded policy |
| Recovery unit | Provides native status, recovery, and safe maintenance independently of the engine |

The unit names do not change component ownership.

### 4.5 Readiness URL

The readiness URL checks the local-origin capability used by the embedded engine.

It is:

- local;
- authenticated or locally protected as defined by the profile;
- bounded;
- free of secret and unrestricted diagnostic data;
- distinct from a general health endpoint;
- unavailable to external networks unless another active contract permits it.

## 5. Safety and Authority Boundaries

### 5.1 Profile scope

This recipe never applies automatically to:

- `user_lightweight`;
- `developer_linux_workstation`;
- `developer_windows_wsl`;
- `build_farm`;
- `control_plane`;
- `sovereign_hub`.

Standard Linux desktop profiles can continue using GNOME, KDE Plasma, or another maintained desktop.

No-GNOME behavior belongs only to the active appliance overlay.

### 5.2 Native recovery boundary

Native recovery remains independent from:

- the embedded web engine;
- Konnaxion rendering;
- Orgo rendering;
- external voice;
- external AI;
- Internet connectivity.

A failed engine can remove web presentation.

It cannot remove local status, recovery entry, session termination, accessibility entry, or safe maintenance.

### 5.3 Component and data ownership

The shell, compositor, and engine have no direct write access to:

- Konnaxion databases;
- Orgo databases;
- Kristal state;
- UCKK storage;
- Governance Policy Runtime stores;
- Identity and Trust stores;
- Audit Broker evidence stores;
- release stores;
- Publication Gateway state;
- foreign component source files.

State-changing actions use registered component interfaces and applicable policy.

### 5.4 Privilege

The shell does not receive unrestricted root or host administration.

Privileged node changes use:

- an authorized operator;
- Governance Policy Runtime where selected;
- kOA Node Agent;
- a closed privileged operation;
- before-and-after verification;
- receipts.

The reference helper requires root only for the activation pointer and service lifecycle.

Use the profile-approved privilege path rather than an ordinary unrestricted root shell.

### 5.5 Embedded-engine restrictions

The active engine policy restricts:

- origins;
- URLs;
- external navigation;
- downloads;
- browser extensions;
- developer tools;
- file selection;
- drag and drop;
- clipboard;
- printing;
- screenshots;
- protocol handlers;
- media capture;
- geolocation;
- notifications;
- device access;
- persistent storage;
- popups and new windows.

Each allowed capability is explicit and profile-controlled.

A kiosk command-line option alone is not the security boundary.

### 5.6 Network boundary

The local-origin service binds only to the interface and port selected by the profile.

A reference local-only bind is:

`text
127.0.0.1:8443
`

The embedded engine reaches approved local origins.

External egress remains denied unless an active integration contract permits one bounded action.

Under `sovereign_offline`, Internet-dependent paths remain prohibited.

### 5.7 Ariane and AI boundary

Local Ariane navigation remains deterministic and locally available.

External voice is optional.

The appliance shell does not invoke ChatGPT, Suno, Gamma, external voice, SenTient, or another AI surface during:

- startup;
- page load;
- navigation;
- readiness;
- recovery;
- ingestion;
- profile activation.

Failure of external voice preserves keyboard, pointer, touch, menus, shortcuts, accessibility controls, and local commands.

### 5.8 Release boundary

The shell activates only a complete compatible Release Set.

It does not activate individual compositor, engine, shell, service, policy, or language artifacts independently when the Release Set requires coordinated versions.

The previous compatible Release Set remains available until acceptance and the applicable rollback window complete.

### 5.9 Evidence boundary

Logs and receipts avoid:

- secret values;
- raw protected page content;
- unrestricted screenshots;
- private workspace payloads;
- provider credentials;
- recovery secrets.

Evidence records identities, versions, profile, units, results, timing, failures, activation, rollback, and final disposition.

## 6. Procedure

### 6.1 Create the local recipe workspace

Use an operator-controlled temporary directory:

`bash
sudo install \
 --directory \
 --owner root \
 --group root \
 --mode 0750 \
 /var/lib/koa/recipe-tools/appliance-shell
`

Do not place mutable activation tools inside the immutable Release Set.

### 6.2 Install the reference helper

Create `/var/lib/koa/recipe-tools/appliance-shell/appliance-shellctl`:

`bash
sudo tee \
 /var/lib/koa/recipe-tools/appliance-shell/appliance-shellctl \
 >/dev/null <<'BASH'
#!/usr/bin/env bash
set -euo pipefail

fail {
 printf 'error: %s\n' "$*" >&2
 exit 1
}

usage {
 cat >&2 <<'USAGE'
Usage:
 appliance-shellctl preflight <environment-file>
 appliance-shellctl activate <environment-file>
 appliance-shellctl status <environment-file>
 appliance-shellctl rollback <environment-file>
USAGE
 exit 2
}

require_command {
 command -v "$1" >/dev/null 2>&1 ||
 fail "required command not found: $1"
}

require_variable {
 local name=$1
 [ -n "${!name:-}" ] ||
 fail "required variable is unset or empty: $name"
}

require_file {
 [ -f "$1" ] || fail "required file not found: $1"
}

require_directory {
 [ -d "$1" ] || fail "required directory not found: $1"
}

require_root {
 [ "$(id -u)" -eq 0 ] ||
 fail "activate and rollback require root; use the approved privilege path"
}

load_environment {
 local environment_file=$1

 require_file "$environment_file"

 # The environment file is an operator-controlled local input.
 # It contains paths, unit names, and URLs, not secret values.
 # shellcheck disable=SC1090
 . "$environment_file"

 require_variable KOA_PROFILE_MANIFEST
 require_variable KOA_RELEASE_ROOT
 require_variable KOA_RELEASE_SET_ID
 require_variable KOA_ACTIVE_LINK
 require_variable KOA_PREVIOUS_LINK
 require_variable KOA_LOCK_FILE
 require_variable KOA_LOCAL_ORIGIN_UNIT
 require_variable KOA_COMPOSITOR_UNIT
 require_variable KOA_SHELL_UNIT
 require_variable KOA_ENGINE_UNIT
 require_variable KOA_RECOVERY_UNIT
 require_variable KOA_READY_URL

 KOA_RELEASE_DIRECTORY="${KOA_RELEASE_ROOT%/}/${KOA_RELEASE_SET_ID}"
 KOA_RELEASE_MANIFEST="${KOA_RELEASE_DIRECTORY%/}/release-set.json"

 export KOA_RELEASE_DIRECTORY
 export KOA_RELEASE_MANIFEST
}

json_contains_string {
 local file=$1
 local expected=$2

 jq -e --arg expected "$expected" '
 [
 .. |
 strings |
 select(. == $expected)
 ] |
 length > 0
 ' "$file" >/dev/null
}

check_unit_exists {
 systemctl cat "$1" >/dev/null 2>&1 ||
 fail "systemd unit is not installed or readable: $1"
}

check_environment_file_permissions {
 local environment_file=$1
 local mode owner

 mode=$(stat -c '%a' "$environment_file")
 owner=$(stat -c '%U' "$environment_file")

 case "$mode" in
 *[2367][0-7]|??[2367])
 fail "environment file is group- or world-writable: $environment_file"
 ;;
 esac

 if [ "$(id -u)" -eq 0 ] && [ "$owner" != "root" ]; then
 fail "root activation requires a root-owned environment file"
 fi
}

check_release_permissions {
 local first_writable

 first_writable=$(
 find -L "$KOA_RELEASE_DIRECTORY" -xdev -perm /022 -print -quit
 )

 [ -z "$first_writable" ] ||
 fail "release content is group- or world-writable: $first_writable"
}

check_manifest_sanity {
 require_file "$KOA_PROFILE_MANIFEST"
 require_file "$KOA_RELEASE_MANIFEST"

 json_contains_string \
 "$KOA_PROFILE_MANIFEST" \
 "sovereign_linux_node" ||
 fail "profile manifest does not identify sovereign_linux_node"

 json_contains_string \
 "$KOA_PROFILE_MANIFEST" \
 "appliance_shell" ||
 fail "profile manifest does not include appliance_shell"

 local channel
 for channel in system services governance knowledge; do
 json_contains_string "$KOA_RELEASE_MANIFEST" "$channel" ||
 fail "release manifest does not mention required channel: $channel"
 done
}

check_tools {
 require_command jq
 require_command systemctl
 require_command readlink
 require_command stat
 require_command find
 require_command flock
 require_command curl
 require_command ln
 require_command mv
}

check_units {
 check_unit_exists "$KOA_LOCAL_ORIGIN_UNIT"
 check_unit_exists "$KOA_COMPOSITOR_UNIT"
 check_unit_exists "$KOA_SHELL_UNIT"
 check_unit_exists "$KOA_ENGINE_UNIT"
 check_unit_exists "$KOA_RECOVERY_UNIT"
}

ready_check {
 if [ -n "${KOA_LOCAL_CA_FILE:-}" ]; then
 require_file "$KOA_LOCAL_CA_FILE"
 curl \
 --fail \
 --silent \
 --show-error \
 --max-time "${KOA_READY_TIMEOUT_SECONDS:-10}" \
 --cacert "$KOA_LOCAL_CA_FILE" \
 "$KOA_READY_URL" >/dev/null
 else
 curl \
 --fail \
 --silent \
 --show-error \
 --max-time "${KOA_READY_TIMEOUT_SECONDS:-10}" \
 "$KOA_READY_URL" >/dev/null
 fi
}

check_active_units {
 systemctl is-active --quiet "$KOA_LOCAL_ORIGIN_UNIT"
 systemctl is-active --quiet "$KOA_COMPOSITOR_UNIT"
 systemctl is-active --quiet "$KOA_SHELL_UNIT"
 systemctl is-active --quiet "$KOA_ENGINE_UNIT"
}

atomic_link {
 local target=$1
 local link=$2
 local parent temporary

 parent=$(dirname "$link")
 mkdir -p "$parent"

 temporary="${link}.new.$$"
 rm -f "$temporary"
 ln -s "$target" "$temporary"
 mv -Tf "$temporary" "$link"
}

record_previous_target {
 local current

 if [ -L "$KOA_ACTIVE_LINK" ]; then
 current=$(readlink -f "$KOA_ACTIVE_LINK")
 [ -n "$current" ] ||
 fail "active link cannot be resolved: $KOA_ACTIVE_LINK"

 atomic_link "$current" "$KOA_PREVIOUS_LINK"
 fi
}

restart_appliance_units {
 systemctl daemon-reload

 systemctl restart "$KOA_LOCAL_ORIGIN_UNIT"
 systemctl restart "$KOA_COMPOSITOR_UNIT"
 systemctl restart "$KOA_SHELL_UNIT"
 systemctl restart "$KOA_ENGINE_UNIT"
}

preflight {
 local environment_file=$1

 check_tools
 check_environment_file_permissions "$environment_file"
 require_directory "$KOA_RELEASE_DIRECTORY"
 check_release_permissions
 check_manifest_sanity
 check_units

 printf 'preflight: pass\n'
 printf 'profile_manifest=%s\n' "$KOA_PROFILE_MANIFEST"
 printf 'release_set_id=%s\n' "$KOA_RELEASE_SET_ID"
 printf 'release_directory=%s\n' "$KOA_RELEASE_DIRECTORY"
}

activate {
 local environment_file=$1
 local old_target=''

 require_root
 preflight "$environment_file"

 mkdir -p "$(dirname "$KOA_LOCK_FILE")"
 exec 9>"$KOA_LOCK_FILE"
 flock -x 9

 if [ -L "$KOA_ACTIVE_LINK" ]; then
 old_target=$(readlink -f "$KOA_ACTIVE_LINK")
 fi

 record_previous_target
 atomic_link "$KOA_RELEASE_DIRECTORY" "$KOA_ACTIVE_LINK"

 if ! restart_appliance_units; then
 printf 'activation failed; attempting rollback\n' >&2

 if [ -n "$old_target" ] && [ -d "$old_target" ]; then
 atomic_link "$old_target" "$KOA_ACTIVE_LINK"
 systemctl daemon-reload
 restart_appliance_units || true
 fi

 fail "activation did not complete"
 fi

 if ! check_active_units || ! ready_check; then
 printf 'acceptance failed; attempting rollback\n' >&2

 if [ -n "$old_target" ] && [ -d "$old_target" ]; then
 atomic_link "$old_target" "$KOA_ACTIVE_LINK"
 systemctl daemon-reload
 restart_appliance_units || true
 fi

 fail "appliance shell did not pass initial acceptance"
 fi

 printf 'activation: pass\n'
 printf 'active_release=%s\n' "$(readlink -f "$KOA_ACTIVE_LINK")"
 if [ -L "$KOA_PREVIOUS_LINK" ]; then
 printf 'previous_release=%s\n' \
 "$(readlink -f "$KOA_PREVIOUS_LINK")"
 fi
}

status {
 check_tools
 check_manifest_sanity
 check_units

 printf 'active_release=%s\n' \
 "$(readlink -f "$KOA_ACTIVE_LINK" 2>/dev/null || true)"
 printf 'previous_release=%s\n' \
 "$(readlink -f "$KOA_PREVIOUS_LINK" 2>/dev/null || true)"

 local unit
 for unit in \
 "$KOA_LOCAL_ORIGIN_UNIT" \
 "$KOA_COMPOSITOR_UNIT" \
 "$KOA_SHELL_UNIT" \
 "$KOA_ENGINE_UNIT" \
 "$KOA_RECOVERY_UNIT"; do
 printf '%s=' "$unit"
 systemctl is-active "$unit" 2>/dev/null || true
 done

 if ready_check; then
 printf 'ready_url=pass\n'
 else
 printf 'ready_url=fail\n'
 return 1
 fi
}

rollback {
 local environment_file=$1
 local previous_target current_target

 require_root
 check_tools
 check_environment_file_permissions "$environment_file"
 check_units

 mkdir -p "$(dirname "$KOA_LOCK_FILE")"
 exec 9>"$KOA_LOCK_FILE"
 flock -x 9

 [ -L "$KOA_PREVIOUS_LINK" ] ||
 fail "previous release link does not exist: $KOA_PREVIOUS_LINK"

 previous_target=$(readlink -f "$KOA_PREVIOUS_LINK")
 require_directory "$previous_target"

 current_target=''
 if [ -L "$KOA_ACTIVE_LINK" ]; then
 current_target=$(readlink -f "$KOA_ACTIVE_LINK")
 fi

 atomic_link "$previous_target" "$KOA_ACTIVE_LINK"

 if ! restart_appliance_units; then
 if [ -n "$current_target" ] && [ -d "$current_target" ]; then
 atomic_link "$current_target" "$KOA_ACTIVE_LINK"
 systemctl daemon-reload
 restart_appliance_units || true
 fi

 fail "rollback service restart failed"
 fi

 check_active_units
 ready_check

 printf 'rollback: pass\n'
 printf 'active_release=%s\n' "$(readlink -f "$KOA_ACTIVE_LINK")"
}

main {
 [ "$#" -eq 2 ] || usage

 local command_name=$1
 local environment_file=$2

 load_environment "$environment_file"

 case "$command_name" in
 preflight)
 preflight "$environment_file"
 ;;
 activate)
 activate "$environment_file"
 ;;
 status)
 status
 ;;
 rollback)
 rollback "$environment_file"
 ;;
 *)
 usage
 ;;
 esac
}

main "$@"
BASH

sudo chown root:root \
 /var/lib/koa/recipe-tools/appliance-shell/appliance-shellctl

sudo chmod 0750 \
 /var/lib/koa/recipe-tools/appliance-shell/appliance-shellctl

sudo bash -n \
 /var/lib/koa/recipe-tools/appliance-shell/appliance-shellctl
`

The helper is a reference implementation.

Review it against the active profile, unit names, release layout, and privilege model before operational use.

### 6.3 Install the environment file

Install the active, reviewed environment file:

`bash
sudo install \
 --owner root \
 --group root \
 --mode 0640 \
 ./appliance-shell.env \
 /etc/koa/appliance-shell.env
`

Verify that it contains no secret values:

`bash
sudo grep -nEi \
 '(password|private[_-]?key|secret[[:space:]]*=|token[[:space:]]*=)' \
 /etc/koa/appliance-shell.env && {
 printf '%s\n' 'possible secret material detected' >&2
 exit 1
 } || true
`

Review every match manually.

### 6.4 Run canonical profile and artifact validation

Before the helper preflight, run the active profile and artifact validators defined by the deployment lifecycle.

Validation covers:

- composed profile compatibility;
- exact Release Set identity;
- system, services, governance, and knowledge closure;
- artifact integrity and provenance;
- signatures and trust;
- revocation;
- migrations;
- resource envelope;
- previous known-good state;
- required tests and evidence.

The helper performs only recipe-level sanity checks.

It does not replace canonical schema, signature, trust, or compatibility validation.

### 6.5 Run helper preflight

`bash
sudo \
 /var/lib/koa/recipe-tools/appliance-shell/appliance-shellctl \
 preflight \
 /etc/koa/appliance-shell.env
`

Expected terminal result:

`text
preflight: pass
`

The preflight confirms:

- required tools;
- environment-file permissions;
- Release Set directory;
- no group- or world-writable release content;
- presence of the primary profile and overlay identifiers;
- presence of all four release-channel identifiers;
- required systemd units.

It does not prove semantic compatibility.

### 6.6 Inspect service sandboxing

Inspect the active unit definitions:

`bash
for unit_name in \
 koa-local-workspaces.service \
 koa-wayland-compositor.service \
 koa-appliance-shell.service \
 koa-embedded-web-engine.service; do
 sudo systemctl show "$unit_name" \
 --property=User \
 --property=Group \
 --property=NoNewPrivileges \
 --property=ProtectSystem \
 --property=ProtectHome \
 --property=PrivateTmp \
 --property=PrivateDevices \
 --property=DevicePolicy \
 --property=CapabilityBoundingSet \
 --property=RestrictAddressFamilies \
 --property=IPAddressDeny \
 --property=IPAddressAllow \
 --property=ReadOnlyPaths \
 --property=ReadWritePaths
done
`

Compare the result with the active profile and security contract.

A property being absent or weak is not automatically acceptable because the unit is local.

### 6.7 Verify local-origin exposure

Before activation, inspect configured listeners:

`bash
sudo ss --listening --tcp --numeric --process
`

Verify that the local workspace origin is not exposed beyond the profile-selected interface.

For the reference environment, expected local exposure is:

`text
127.0.0.1:8443
`

Do not accept `0.0.0.0:8443` or `[::]:8443` unless an active network and security contract explicitly permits that exposure.

### 6.8 Verify native recovery independently

Verify the recovery unit exists:

`bash
sudo systemctl cat koa-appliance-recovery.target
`

Enter and leave the recovery path according to the active runbook before the first appliance activation.

The test confirms that recovery does not depend on:

- the embedded engine;
- the local-origin service;
- external network;
- external voice;
- external AI.

Do not use this recipe to invent the recovery command sequence. The profile-owned recovery runbook controls entry and exit.

### 6.9 Activate atomically

Run activation from an authorized local console:

`bash
sudo \
 /var/lib/koa/recipe-tools/appliance-shell/appliance-shellctl \
 activate \
 /etc/koa/appliance-shell.env
`

The helper:

1. repeats preflight;
2. takes an exclusive activation lock;
3. records the current active target as `previous`;
4. atomically switches `active` to the staged Release Set;
5. reloads systemd;
6. restarts local-origin, compositor, shell, and engine units;
7. verifies active state;
8. verifies the local readiness URL;
9. attempts rollback when restart or initial acceptance fails.

The helper does not mark the overall deployment conformant.

### 6.10 Inspect status

`bash
sudo \
 /var/lib/koa/recipe-tools/appliance-shell/appliance-shellctl \
 status \
 /etc/koa/appliance-shell.env
`

Also inspect bounded service state:

`bash
for unit_name in \
 koa-local-workspaces.service \
 koa-wayland-compositor.service \
 koa-appliance-shell.service \
 koa-embedded-web-engine.service \
 koa-appliance-recovery.target; do
 sudo systemctl show "$unit_name" \
 --property=ActiveState \
 --property=SubState \
 --property=Result \
 --property=NRestarts \
 --property=ExecMainStatus
done
`

Review recent logs without copying unrestricted page content:

`bash
sudo journalctl \
 --since '-15 minutes' \
 --unit koa-local-workspaces.service \
 --unit koa-wayland-compositor.service \
 --unit koa-appliance-shell.service \
 --unit koa-embedded-web-engine.service \
 --priority notice
`

### 6.11 Validate local workspaces

From the appliance session, validate each selected workspace:

- correct local origin;
- correct language resources;
- login and session behavior;
- component-defined readiness;
- keyboard;
- pointer;
- touch where selected;
- accessibility entry and navigation;
- controlled file selection where selected;
- clipboard policy;
- session termination;
- return to shell;
- no direct component-storage access.

Konnaxion and Orgo tests use their registered interfaces and test fixtures.

The shell is not validated by writing directly to their databases.

### 6.12 Validate restricted navigation

Use the active appliance-shell conformance harness to test:

- approved local origin accepted;
- unapproved local origin denied;
- external HTTP and HTTPS navigation denied;
- popup or new-window request denied or contained;
- general download denied unless explicitly enabled;
- unknown protocol handler denied;
- browser extension loading denied;
- production developer tools unavailable to ordinary users;
- file access limited to declared workflows;
- persistent storage isolated by application and profile.

A manual visual check alone is insufficient for a release-blocking claim.

### 6.13 Validate engine failure

From the authorized local console:

`bash
sudo systemctl stop koa-embedded-web-engine.service
`

Verify:

- the native shell remains visible or reachable;
- local status remains available;
- recovery entry remains available;
- session termination remains available;
- the failure is visible;
- no general-purpose browser starts;
- no full desktop starts;
- no external AI or provider starts;
- component data remains unchanged.

Restore the engine:

`bash
sudo systemctl start koa-embedded-web-engine.service
`

Then repeat readiness and workspace validation.

### 6.14 Validate local navigation without external voice

Disable the external voice integration through its registered integration lifecycle.

Verify:

- keyboard navigation;
- pointer navigation;
- touch navigation where selected;
- menus;
- shortcuts;
- accessibility controls;
- deterministic local Ariane commands;
- recovery entry.

The test does not disable local Ariane navigation.

### 6.15 Validate offline behavior

Run this test only with local-console access and the profile-approved network-isolation procedure.

Under `sovereign_offline`, verify:

- the node starts without Internet;
- local identity and trust resolve;
- local revocation state resolves;
- local policy resolves;
- the appliance shell starts;
- local workspaces load;
- local language resources load;
- local navigation works;
- recovery works;
- active and previous Release Sets remain available;
- external AI and voice integrations report unavailable or prohibited;
- no request is queued for silent future transmission;
- no remote font, script, stylesheet, telemetry, or crash service is required.

Restore network state only through the profile-approved procedure.

### 6.16 Validate resource containment

Apply representative workspace load and inspect:

`bash
systemd-cgtop
`

Inspect unit resource accounting:

`bash
for unit_name in \
 koa-local-workspaces.service \
 koa-wayland-compositor.service \
 koa-appliance-shell.service \
 koa-embedded-web-engine.service; do
 sudo systemctl show "$unit_name" \
 --property=CPUAccounting \
 --property=MemoryAccounting \
 --property=TasksAccounting \
 --property=MemoryCurrent \
 --property=MemoryPeak \
 --property=TasksCurrent \
 --property=CPUUsageNSec
done
`

Verify that a renderer or workspace reaching its resource limit does not remove:

- identity;
- policy;
- native shell;
- recovery;
- local navigation;
- required evidence durability.

### 6.17 Record evidence

Record references to:

- composed profile;
- target Release Set;
- previous Release Set;
- artifact validation;
- activation actor and decision;
- unit identities;
- readiness result;
- origin and permission tests;
- engine-failure result;
- accessibility result;
- offline result where applicable;
- resource result;
- rollback result;
- final disposition.

Do not store secret values or unrestricted page content in ordinary receipts.

## 7. Validation

### 7.1 Acceptance matrix

| Control | Expected result |
| --- | --- |
| Effective primary profile is `sovereign_linux_node` | pass |
| `appliance_shell` overlay is active | pass |
| Additional overlays are compatible | pass |
| Exact Release Set is verified | pass |
| All four release channels are present and compatible | pass |
| Release directory is immutable to non-owner identities | pass |
| Previous compatible Release Set exists | pass |
| Local-origin unit is ready | pass |
| Compositor unit is ready | pass |
| Native shell unit is ready | pass |
| Embedded engine unit is ready | pass |
| Recovery unit is independently available | pass |
| Local approved origins load | pass |
| External and undeclared origins are denied | pass |
| General browsing and application launch remain restricted | pass |
| Component-storage direct access is denied | pass |
| Engine failure preserves native recovery | pass |
| External voice failure preserves local navigation | pass |
| Offline behavior matches the active overlay | pass or not applicable |
| Resource limits preserve critical local capability | pass |
| Atomic activation and rollback are demonstrated | pass |
| Required evidence validates | pass |

### 7.2 Profile-specific expected tests

The active test catalog owns exact definitions.

Expected coverage includes:

`text
TEST-ADR-003-001
TEST-ADR-003-003
TEST-ADR-003-004
TEST-ADR-003-005
TEST-ADR-003-006
TEST-ADR-003-007
TEST-ADR-003-008
TEST-ADR-003-009
TEST-ADR-003-010
TEST-ADR-003-011
TEST-ADR-003-012
TEST-ADR-003-013
TEST-ADR-003-014
`

The profile can require additional:

- high-assurance tests;
- offline tests;
- boot and trust tests;
- tenant-isolation tests;
- accessibility tests;
- hardware tests;
- recovery tests.

### 7.3 Canonical ownership validation

Ownership validation confirms:

- shell and engine identities have no component database credentials;
- local-origin services call registered component interfaces;
- Publication Gateway remains separate;
- UCKK Import Bridge and UCKK Publication Bridge remain separate;
- Governance Policy Runtime remains non-mutating for application data;
- Resource Governor remains authority-neutral for application state;
- Audit Broker remains evidence infrastructure;
- external integrations remain candidate or bounded-result paths.

### 7.4 Terminal results

Record actual results as:

`text
pass
fail
blocked
unavailable
incomplete
not applicable
`

Do not report `pass` when:

- an overlay is unresolved;
- a required artifact is missing;
- a validation command was unavailable;
- an offline test was skipped but required;
- native recovery was not exercised;
- rollback was not demonstrated when required;
- readiness was inferred from process status;
- evidence remains incomplete.

### 7.5 Initial observation period

After activation, retain enhanced observation for the interval defined by the active profile.

Monitor:

- compositor restarts;
- engine renderer failures;
- local-origin errors;
- readiness;
- memory and process growth;
- denied navigation;
- permission denials;
- accessibility failures;
- recovery availability;
- artifact identity drift;
- unexpected external connections.

The Release Set remains within its rollback window until the observation and evidence conditions close.

## 8. Cleanup

### 8.1 Staged but inactive release

When the Release Set never became active:

1. verify that neither `active` nor `previous` points to it;
2. verify no unit references it;
3. preserve failed validation evidence;
4. remove it only through the artifact-retention lifecycle;
5. remove temporary recipe files.

Do not delete a retained artifact merely because the recipe did not activate it.

### 8.2 Temporary recipe helper

After the site adopts a reviewed operational tool or runbook, remove the disposable helper:

`bash
sudo rm -f \
 /var/lib/koa/recipe-tools/appliance-shell/appliance-shellctl
`

Keep the helper when it is the reviewed active local tool.

Its lifecycle then belongs to local operations and configuration management.

### 8.3 Temporary logs and captures

Remove temporary unrestricted captures after required evidence is extracted and validated.

Examples include:

- temporary screenshots;
- browser diagnostic exports;
- temporary network captures;
- copied journal output;
- temporary accessibility traces.

Do not delete incident or required conformance evidence.

### 8.4 Temporary credentials and privilege

After activation or rollback:

- close the operator privilege session;
- remove temporary credentials;
- remove temporary mounts;
- remove temporary staging access;
- close temporary network allowances;
- verify that shell and engine units have only normal runtime credentials.

### 8.5 Cleanup verification

Verify:

`bash
sudo \
 /var/lib/koa/recipe-tools/appliance-shell/appliance-shellctl \
 status \
 /etc/koa/appliance-shell.env
`

Also verify:

- `active` resolves to the accepted Release Set;
- `previous` resolves to a retained compatible Release Set;
- no `.new.*` activation links remain;
- no unreviewed override unit remains;
- no general browser process remains;
- no temporary external network allowance remains;
- no temporary root-owned file exists in an operator home directory.

## 9. Rollback or Safe Exit

### 9.1 Rollback conditions

Rollback is appropriate when:

- compositor readiness fails;
- native shell readiness fails;
- local-origin readiness fails;
- embedded-engine readiness fails;
- approved workspaces do not load;
- restricted navigation fails;
- direct component-storage access is possible;
- accessibility or recovery fails;
- offline closure fails;
- resource containment fails;
- unexpected external traffic appears;
- Release Set compatibility is disproved.

### 9.2 Execute rollback

From an authorized local console:

`bash
sudo \
 /var/lib/koa/recipe-tools/appliance-shell/appliance-shellctl \
 rollback \
 /etc/koa/appliance-shell.env
`

The helper:

1. takes the activation lock;
2. resolves `previous`;
3. atomically switches `active`;
4. reloads systemd;
5. restarts appliance units;
6. verifies active state and readiness;
7. reports the restored active Release Set.

### 9.3 Verify rollback

After rollback, repeat:

- profile and Release Set identity;
- unit readiness;
- local workspaces;
- restricted navigation;
- recovery;
- local navigation;
- offline behavior where applicable;
- evidence path.

Quarantine the failed Release Set and preserve diagnostics.

### 9.4 Rollback failure

When rollback fails:

1. stop normal appliance readiness;
2. enter the native recovery environment;
3. preserve diagnostics;
4. verify active and previous link targets;
5. verify retained Release Set artifacts;
6. verify trust, policy, keys, and storage;
7. restore through the profile-owned recovery runbook;
8. keep normal traffic and user session blocked;
9. record the recovery result.

Do not launch a full desktop or general browser as a silent substitute.

### 9.5 Forward repair

Use forward repair when a profile-owned shell-state or workspace-storage change cannot be interpreted safely by the previous Release Set.

The forward-repair artifact and procedure already exist before irreversible activation.

Forward repair does not authorize:

- shell writes to component databases;
- manual policy edits;
- direct release-store mutation;
- external AI repair;
- untracked browser-profile manipulation.

### 9.6 Safe exit before activation

Before activation, safe exit consists of:

- leaving the staged Release Set inactive;
- removing temporary recipe tooling when appropriate;
- preserving validation evidence;
- closing temporary privilege;
- leaving `active` and `previous` unchanged.

## 10. Failure Handling

| Failure | Response |
| --- | --- |
| Primary profile is not `sovereign_linux_node` | Stop; use the recipe for the active profile |
| `appliance_shell` overlay is absent | Stop; do not infer activation from installed packages |
| Overlay composition is incompatible | Stop; obtain an accepted profile change |
| Release Set is incomplete | Keep it inactive |
| One release channel is missing | Keep the complete Release Set inactive |
| Release content is writable by broad identities | Correct permissions through the artifact lifecycle and repeat verification |
| Environment file contains secret values | Remove the values and use protected credential delivery |
| Required unit is missing | Keep activation blocked |
| Local origin binds externally without authority | Stop the service and restore profile network policy |
| Compositor fails | Enter native recovery or restore previous Release Set |
| Native shell fails | Enter native recovery and keep appliance readiness blocked |
| Embedded engine fails | Preserve native shell and recovery; mark web workspaces degraded |
| Local workspace fails | Preserve shell and unrelated workspaces; repair through the owning component |
| External navigation succeeds | Block acceptance and correct engine policy |
| General browser or desktop starts | Block acceptance and remove the undeclared fallback |
| Direct component-storage access succeeds | Isolate the shell, open an incident, and block conformance |
| External voice fails | Preserve local navigation and mark voice unavailable |
| External AI appears in startup or navigation | Disable the integration, preserve evidence, and block acceptance |
| Offline test contacts a remote dependency | Block offline conformance and restore local closure |
| Resource pressure removes recovery | Block profile conformance and correct the resource envelope |
| Readiness URL fails | Attempt rollback; do not accept process liveness as success |
| Activation lock cannot be acquired | Wait for or investigate the existing operation; do not bypass the lock |
| Previous Release Set is missing | Block risk-bearing activation |
| Rollback fails | Enter the profile-owned recovery environment |
| Evidence path is unavailable | Preserve bounded local evidence and keep evidence-critical closure blocked |
| Validation is unavailable or incomplete | Keep the prior valid state and report the actual terminal result |

### 10.1 Unexpected external connections

Inspect active connections:

`bash
sudo ss --tcp --udp --process --numeric
`

When an appliance process opens an undeclared external connection:

1. preserve the process and connection identity;
2. block the network path through the profile-approved control;
3. isolate the affected unit;
4. preserve evidence;
5. identify the artifact and configuration;
6. review provider, telemetry, font, script, update, and crash-report dependencies;
7. restore a known-good Release Set when needed.

### 10.2 Crash loops

Inspect:

`bash
sudo systemctl show \
 koa-wayland-compositor.service \
 koa-appliance-shell.service \
 koa-embedded-web-engine.service \
 --property=NRestarts \
 --property=Result \
 --property=ExecMainStatus
`

A crash loop is not readiness.

Stop the affected capability, preserve native recovery, and roll back or repair.

### 10.3 Lost local display

Use the profile-owned local recovery path.

Do not improvise by enabling an unrestricted remote desktop, broad SSH forwarding, or a general display manager.

Any temporary access follows an active break-glass contract and closes after recovery.

### 10.4 Corrupt active link

When `active` cannot be resolved:

1. stop appliance units;
2. enter recovery;
3. verify the Release Set inventory;
4. atomically restore a verified target;
5. run complete acceptance;
6. preserve the corrupt-link diagnostics.

Do not point `active` at an arbitrary directory.

### 10.5 Failed cleanup

A failed cleanup leaves the change record open.

Record:

- retained privilege;
- temporary files;
- unit overrides;
- network allowances;
- active sessions;
- failed Release Set;
- evidence;
- next safe action.

Do not treat the node as clean until the residual state is reconciled.

## 11. References

### 11.1 Canonical references

`text
generated/profile-catalog.json
contracts/profiles/sovereign-linux-node.profile.json
contracts/profiles/appliance-shell.profile.json
contracts/profiles/high-assurance.profile.json
contracts/profiles/sovereign-offline.profile.json
contracts/release-channels.contract.json
contracts/artifact-classes.contract.json
generated/component-catalog.json
contracts/integration-types.contract.json
generated/test-catalog.json
generated/evidence-catalog.json
`

### 11.2 Decisions and locks

`text
DEC-SHELL-001
DEC-PROFILE-001
DEC-ARI-001
DEC-AI-001
DEC-DATA-001
DEC-GOV-001
DEC-GATE-001
DEC-CONTAINER-001
DEC-HW-001
DEC-REL-001

LOCK-PROFILE-001
LOCK-IMPL-001
LOCK-IMPL-002
LOCK-ARI-001
LOCK-ARI-002
LOCK-AI-001
LOCK-AI-002
LOCK-DATA-001
LOCK-GOV-001
LOCK-GATE-001
LOCK-LIFE-001
LOCK-LIFE-002
LOCK-LIFE-003
LOCK-LIFE-004
`

### 11.3 Related documents

`text
11-recipes/README.md
03-profiles/07-sovereign-linux-node.md
02-system/02-logical-architecture.md
02-system/11-ariane.md
02-system/17-capability-degradation.md
07-security/01-security-baseline.md
07-security/08-network-boundaries.md
07-security/11-ai-boundaries.md
08-operations/00-operating-model.md
08-operations/09-restore.md
09-conformance/10-canonical-ownership-validation.md
10-adrs/ADR-003-appliance-shell-without-gnome.md
`

### 11.4 Recipe validation status

During generation:

- the metadata block was parsed;
- all 11 recipe sections were found;
- the embedded helper passed Bash syntax validation;
- the helper preflight was exercised against a disposable composed-profile and Release Set fixture;
- atomic active and previous link behavior was exercised in a disposable environment;
- helper rollback behavior was exercised in a disposable environment;
- the document does not claim that deployment-specific systemd, compositor, engine, workspace, offline, accessibility, or recovery tests executed.

The active test catalog and evidence registry determine deployment conformance.
