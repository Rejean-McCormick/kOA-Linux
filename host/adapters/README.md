# Host recovery adapters

These modules are deliberately thin wrappers around fixed host interfaces. They do not decide recovery authority, select a Release Set, interpret component data, or grant break-glass access.

## Boundary

- `filesystem.py` confines reads and atomic writes beneath an explicit authority root, rejects symlink traversal, verifies SHA-256 digests, and provides exclusive recovery locks.
- `systemd.py` permits only `inspect`, `start`, `stop`, and `restart` for profile-admitted units.
- `podman.py` permits only `inspect`, `start`, `stop`, `pause`, and `unpause` for profile-admitted containers.
- `network.py` permits only link inspection, isolation, and restoration for profile-admitted interfaces.
- `storage.py` mounts only profile-admitted sources onto profile-admitted targets and always uses `ro,nosuid,nodev,noexec`.

Every subprocess call uses an argument vector, a fixed absolute binary, a bounded timeout, a minimal environment, and `shell=False`. There is no generic command runner exposed to recovery plans.

## Authority and evidence

Callers must establish identity, policy, target scope, purpose, expiry, and required approvals before invoking a mutating adapter. Adapter success is only a physical observation. It is not proof of completed recovery. Recovery controllers must preserve evidence, verify the candidate, activate authority last, and persist a terminal receipt or evidence record.

## Dependency on B-0081

Boot-slot selection, Release Set verification, boot-success marking, and entry into last-known-good are owned by B-0081. The recovery controllers in B-0082 depend on that public boundary and fail closed when it is unavailable; they do not duplicate boot logic.

## Data ownership

These adapters never write directly into a component-owned database. Component restore, migration, validation, and activation remain the responsibility of each component's declared interface. A shared device or mount does not create shared authority.
