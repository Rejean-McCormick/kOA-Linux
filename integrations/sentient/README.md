# SenTient integration boundary

This directory declares the kOA-owned integration boundary for the independently
owned SenTient subsystem. It does not vendor SenTient source, duplicate its
internal domain model, define its complete API, or claim ownership of its user
interface.

## Current alignment state

The official subsystem documentation mount `subsystems/sentient/` and an
upstream repository, release, or immutable commit pin were not present in the
supplied source set. The boundary is therefore prepared but deliberately
non-activable. `source.lock.json` records the unresolved source state and blocks
activation rather than fabricating a repository, revision, digest, license, or
documentation release.

Final alignment requires all of the following:

1. mount the official SenTient documentation at `subsystems/sentient/`;
2. replace the unresolved source record with an immutable source revision and a
   verified source digest;
3. resolve license metadata and the matching documentation release;
4. validate compatibility and the adapter contract against that source;
5. execute boundary, health, degradation, removability, and no-direct-write
   tests.

## Authority boundary

SenTient is an optional isolated research and enrichment workbench. It is not a
required kOA runtime component and has no authority over identity, governance,
data ownership, publication, release, security, recovery, conformance, or any
component's canonical state.

Every input requires an explicit task or authorized workflow trigger. Every
output remains candidate material with provenance until an owning local workflow
validates and accepts it through a declared interface. Visibility of a route,
sidebar item, or widget grants no capability and is never authorization or
acceptance evidence.

Direct writes to another component or subsystem's authoritative state are
prohibited. SenTient may access selected inputs only through registered APIs,
controlled exports, governed references, or candidate-artifact interfaces.

## Operating boundary

- disabled and stopped by default;
- activated only by an explicit task in a compatible development or build
  profile;
- isolated service/workspace identity, dependencies, storage, temporary data,
  queues, indexes, caches, models, artifacts, CPU, memory, and network;
- no public listener, unrestricted egress, direct privileged-broker interface,
  signing authority, publication authority, or release authority;
- network disabled by default and enabled only through registered,
  destination-scoped integrations;
- stopped or rejected before protected and required platform services under
  resource pressure;
- removable without core failure.

## Presentation contribution

The files under `interface/` contribute presentation-only kOA Spaces entry
points for an admitted workbench, its bounded jobs, and candidate artifacts. The
routes refer to SenTient-owned surfaces and do not reproduce its internal UI or
workflow catalog. The interface is unavailable when the source, profile,
resource, isolation, or health preconditions are unresolved.

## Files

- `source.lock.json` — immutable-source requirement and current blocked state;
- `compatibility.json` — accepted kOA contracts and explicit rejection rules;
- `integration.toml` — identity, adapter entrypoint, capabilities, and ownership;
- `deployment.toml` — task activation and isolation boundary;
- `resource-envelope.toml` — Resource Governor envelope;
- `health.toml` — liveness, readiness, and dependency health contract;
- `storage.toml` — storage ownership and direct-write prohibitions;
- `backup.toml` — backup coordination boundary;
- `degradation.toml` — capability-scoped failure behavior;
- `interface/` — presentation-only kOA Spaces contributions;
- `adapter/pyproject.toml` — package declaration for the following adapter
  bundle.

Canonical contract digest used for this prepared boundary:
`sha256:7cb105bc9fac01b6a10c13cea07faf84097f5134491dd68c5a9a7e0a817b7c32`.
