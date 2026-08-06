<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-032",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "system",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/system.contract.json",
    "contracts/ai-navigation.contract.json",
    "02-system/02-logical-architecture.md",
    "02-system/04-component-boundaries.md",
    "02-system/07-cross-component-communication.md",
    "02-system/19-release-and-artifact-identity.md",
    "04-components/04-subsystem-documentation-boundaries.md",
    "05-development/00-development-model.md",
    "06-lifecycle/02-release-model.md",
    "07-security/05-privilege-boundaries.md",
    "08-operations/00-operating-model.md",
    "contracts/subsystems/koa-spaces.subsystem.json",
    "02-system/23-code-and-filesystem-architecture.md",
    "07-security/09-storage-boundaries.md",
    "08-operations/08-backup.md",
    "08-operations/09-restore.md",
    "11-recipes/sovereign-linux/storage-layout.md",
    "11-recipes/sovereign-linux/systemd-layout.md"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-CODE-FS-005",
    "LOCK-CODE-FS-006",
    "LOCK-CODE-FS-009"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-023",
    "DOC-SEC-009",
    "DOC-OPS-008",
    "DOC-OPS-009",
    "DOC-RECIPE-SLN-004",
    "RECIPE-SOV-LINUX-001"
  ],
  "tags": [
    "runtime-filesystem",
    "fhs",
    "installed-layout",
    "state",
    "cache",
    "recovery"
  ]
}
KOA:DOC-META:END -->

# Installed Runtime Filesystem

## 1. Scope

This document freezes the installed path classes and fixed control files for kOA-Linux. It does not enumerate dynamic database pages, media blobs, receipt instances, cache objects, release versions, backup generations, or imported artifacts. Their owning roots and naming contracts are frozen; individual runtime instances are created and removed through component and lifecycle rules.

## 2. Immutable and Executable Paths

```text
/usr/bin/koa
/usr/bin/koa-node-agentctl
/usr/libexec/koa/koa-node-agent
/usr/libexec/koa/koa-privileged-broker
/usr/libexec/koa/koa-activation
/usr/libexec/koa/koa-health-aggregate
/usr/libexec/koa/koa-offline-import
/usr/libexec/koa/koa-backup
/usr/libexec/koa/koa-maintenance
/usr/lib/koa/contracts/system.contract.json
/usr/lib/koa/contracts/terminology.contract.json
/usr/lib/koa/contracts/release-channels.contract.json
/usr/lib/koa/contracts/artifact-classes.contract.json
/usr/lib/koa/contracts/components/
/usr/lib/koa/contracts/profiles/
/usr/lib/koa/contracts/subsystems/
/usr/lib/koa/contracts/integrations/
/usr/lib/koa/contracts/artifact-contracts/
/usr/lib/koa/profiles/
/usr/lib/koa/release-sets/
/usr/lib/koa/interface-bindings/python/
/usr/lib/koa/interface-bindings/rust/
/usr/share/koa/defaults/
/usr/share/koa/locales/
/usr/share/koa/appliance-shell/
/usr/share/koa/recovery/
/usr/lib/systemd/system/koa-node.target
/usr/lib/systemd/system/koa-core.target
/usr/lib/systemd/system/koa-critical.target
/usr/lib/systemd/system/koa-background.target
/usr/lib/systemd/system/koa-optional.target
/usr/lib/systemd/system/koa-activation.target
/usr/lib/systemd/system/koa-recovery.target
/usr/lib/systemd/system/koa-node-agent.service
/usr/lib/systemd/system/koa-node-agent.socket
/usr/lib/systemd/system/koa-privileged-broker.service
/usr/lib/systemd/system/koa-privileged-broker.socket
/usr/lib/systemd/system/koa-release-set-verify.service
/usr/lib/systemd/system/koa-activation.service
/usr/lib/systemd/system/koa-health-aggregate.service
/usr/lib/systemd/system/koa-offline-import.path
/usr/lib/systemd/system/koa-offline-import.service
/usr/lib/systemd/system/koa-backup.service
/usr/lib/systemd/system/koa-backup.timer
/usr/lib/systemd/system/koa-maintenance.service
/usr/lib/systemd/system/koa-maintenance.timer
/usr/lib/sysusers.d/koa-components.conf
/usr/lib/sysusers.d/koa-privileged-broker.conf
/usr/lib/tmpfiles.d/koa-components.conf
/usr/lib/tmpfiles.d/koa-runtime.conf
```
## 3. Operator Configuration Paths

```text
/etc/koa/active/profile.json
/etc/koa/active/release-set.json
/etc/koa/active/capabilities.json
/etc/koa/node/config.toml
/etc/koa/node/privileged-operation-catalog.json
/etc/koa/trust/policy.toml
/etc/koa/network/zones.toml
/etc/koa/network/service-exposure.toml
/etc/koa/storage/layout.toml
/etc/koa/storage/quotas.toml
/etc/koa/backup/policy.toml
/etc/koa/recovery/policy.toml
/etc/koa/components/audit-broker/config.toml
/etc/koa/components/governance-policy-runtime/config.toml
/etc/koa/components/identity-and-trust/config.toml
/etc/koa/components/koa-mediatheque/config.toml
/etc/koa/components/koa-node-agent/config.toml
/etc/koa/components/kristal-runtime/config.toml
/etc/koa/components/publication-gateway/config.toml
/etc/koa/components/resource-governor/config.toml
/etc/koa/integrations/ariane/config.toml
/etc/koa/integrations/koa-spaces/config.toml
/etc/koa/integrations/konnaxion/config.toml
/etc/koa/integrations/orgo/config.toml
/etc/koa/integrations/semantik-architect/config.toml
/etc/koa/integrations/sentient/config.toml
/etc/koa/integrations/uckk/config.toml
/etc/koa/secrets.d/
```
## 4. Ephemeral Runtime Paths

```text
/run/koa/activation/
/run/koa/recovery/
/run/koa/locks/
/run/koa/health/
/run/koa/sockets/koa-node-agent.sock
/run/koa/sockets/koa-privileged-broker.sock
/run/koa/sockets/audit-broker.sock
/run/koa/sockets/governance-policy-runtime.sock
/run/koa/sockets/identity-and-trust.sock
/run/koa/sockets/koa-mediatheque.sock
/run/koa/sockets/kristal-runtime.sock
/run/koa/sockets/publication-gateway.sock
/run/koa/sockets/resource-governor.sock
```
## 5. Persistent State and Recovery Paths

```text
/var/lib/koa/node/
/var/lib/koa/node/effective-profile.json
/var/lib/koa/node/activation-receipts/
/var/lib/koa/identity-and-trust/
/var/lib/koa/resource-governor/
/var/lib/koa/policies/
/var/lib/koa/audit/
/var/lib/koa/publication-gateway/
/var/lib/koa/kristal/
/var/lib/koa/mediatheque/
/var/lib/koa/ariane/
/var/lib/koa/integrations/koa-spaces/
/var/lib/koa/konnaxion/
/var/lib/koa/orgo/
/var/lib/koa/integrations/semantik-architect/
/var/lib/koa/integrations/sentient/
/var/lib/koa/integrations/uckk/
/var/lib/koa/artifacts/
/var/lib/koa/releases/
/var/lib/koa/receipts/
/var/lib/koa/quarantine/
/var/lib/koa/backups/
/var/lib/koa/offline-import/
/var/lib/koa/recovery/
/var/lib/koa/support-bundles/
/var/lib/koa-recovery/
```
## 6. Cache and Build Cache Paths

```text
/var/cache/koa/contracts/
/var/cache/koa/artifacts/
/var/cache/koa/containers/
/var/cache/koa/mediatheque/
/var/cache/koa/integrations/
/var/cache/koa/downloads/
/var/cache/koa-build/bootstrap/
/var/cache/koa-build/leases/
/var/cache/koa-build/manifests/
/var/cache/koa-build/quarantine/
/var/cache/koa-build/receipts/
/var/cache/koa-build/shared/
/var/cache/koa-build/workers/
```

## 7. Path-Class Rules

| Root | Class | Rule |
| --- | --- | --- |
| `/usr/bin`, `/usr/libexec`, `/usr/lib`, `/usr/share` | Immutable payload | Replaced only through admitted package or system-image activation |
| `/etc/koa` | Operator configuration | Contains non-secret configuration and active pointers; private secret material remains under protected secret delivery mechanisms |
| `/run/koa` | Ephemeral runtime | Recreated at boot; sockets, locks, readiness, and transition state only |
| `/var/lib/koa` | Persistent authoritative or coordinated state | Every subtree has one declared owner; no shared writable database root |
| `/var/lib/koa-recovery` | Recovery state | Separate recovery target and evidence boundary |
| `/var/cache/koa` | Rebuildable runtime cache | May be deleted without loss of authority |
| `/var/cache/koa-build` | Build-farm cache | Rebuildable and lease-controlled; never an authority source |

## 8. Dynamic File Naming

Dynamic instances SHALL be content-addressed, version-addressed, receipt-identified, or component-defined inside their owning root. A dynamic filename must not be used to bypass owner isolation. Symlinks escaping the owning root are prohibited. Shared mount devices do not create shared logical ownership.

## 9. kOA Spaces Runtime State

`/var/lib/koa/integrations/koa-spaces/` may contain validated Space definitions, interface manifests, navigation preferences, last permitted route state, cached presentation assets, activation receipts, and the previous validated Space for rollback. It SHALL NOT contain Orgo tasks, Konnaxion records, UCKK course authority, Mediatheque media authority, identity credentials, policy authority, release activation state, or privileged-operation requests.
