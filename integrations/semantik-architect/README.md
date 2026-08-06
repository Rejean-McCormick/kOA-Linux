# SemantiK Architect kOA integration boundary

This directory contains only the kOA-owned integration boundary for the separately owned
SemantiK Architect subsystem. It does not vendor or reproduce the subsystem implementation,
internal domain model, workflow, state machine, API, validation logic, or user interface.

## Current admission state

The supplied corpus does not contain the required official documentation mount at
`subsystems/semantik-architect/`, nor an authoritative repository, commit, source digest,
license declaration, or documentation release for the subsystem implementation.
Consequently, `source.lock.json` is deliberately fail-closed and the integration status is
`preparation_only`. No build, activation, release admission, or claim of final alignment is
permitted until every required source field is populated from authoritative subsystem
materials and validated.

## kOA-owned boundary

kOA owns deployment profile membership, adapter lifecycle, resources, trust boundaries,
network and storage exposure, artifact admission, declared cross-subsystem interactions,
health integration, backup coordination, and safe degradation. The subsystem continues to own
its internal behavior and authoritative state.

The adapter communicates through the declared HTTP-over-Unix transport. It may submit bounded
compiler jobs, read their status, and export candidate runtime packs through declared artifacts.
It may not write directly to another subsystem or component store, activate a runtime pack,
grant a capability, or infer authorization from interface visibility.

## Presentation contribution

The files under `interface/` expose only a status route and status widget for kOA Spaces. They
are presentation-only. The module, sidebar, and widget manifests do not grant authority and do
not duplicate the subsystem's internal user interface.

## File responsibilities

- `source.lock.json`: source-admission gate and required immutable pin fields.
- `compatibility.json`: exact kOA contract compatibility and fail-closed defaults.
- `integration.toml`: identity, capabilities, transport, authority, and interface ownership.
- `deployment.toml`: admitted profiles, process boundary, network policy, and sandboxing.
- `resource-envelope.toml`: profile-resolved resource admission and degradation order.
- `health.toml`: liveness/readiness semantics without authority inference.
- `storage.toml`: kOA adapter-owned state and artifact hand-off restrictions.
- `backup.toml`: backup/restore boundaries excluding source, caches, secrets, and subsystem state.
- `degradation.toml`: explicit behavior for missing, incompatible, offline, or uncertain states.
- `adapter/pyproject.toml`: package metadata for the separately implemented adapter bundle.
- `interface/`: validated presentation-only manifests.
