# kOA Spaces integration boundary

This directory contains only the kOA-Linux-owned boundary for the optional and
replaceable `koa_spaces` subsystem. It does not contain the kOA Spaces internal
implementation, business state, database migrations, or authoritative internal
documentation.

## Authority

The applicable kOA authorities are:

- `docs/contracts/subsystems/koa-spaces.subsystem.json`;
- `docs/04-components/subsystems/koa-spaces.md`;
- `docs/02-system/21-koa-spaces-experience-layer.md`;
- `docs/02-system/22-koa-spaces-interface-composition.md`;
- `docs/03-profiles/14-koa-spaces-deployment.md`.

The subsystem's future internal documentation is expected at
`subsystems/koa-spaces/` as a mounted independent repository. That mount is not
present in the supplied source corpus. Consequently, `source.lock.json` is
fail-closed: it pins the available boundary artifacts and prohibits build or
activation until an immutable upstream repository revision is recorded.

## Boundary

kOA-Linux owns deployment membership, lifecycle activation, network and storage
exposure, resource limits, health integration, backup coordination, admitted
Space definitions, admitted module interface manifests, degradation behavior,
and activation evidence.

kOA Spaces owns only its presentation implementation and validated local
presentation state. It does not own authorization, identity, policy, resource
admission, host privilege, release activation, business workflows, learning
progress, media authority, or data owned by another subsystem.

Space definitions and module manifests are declarative artifacts. They cannot
contain executable extensions, grant capabilities, bypass authorization, or
perform direct cross-subsystem writes.

## Files

- `source.lock.json` — source and local boundary pins with a fail-closed upstream gate;
- `compatibility.json` — supported contract, profile, and artifact versions;
- `integration.toml` — integration identity and authority boundary;
- `deployment.toml` — profile-conditioned process and exposure model;
- `resource-envelope.toml` — implementation defaults for bounded runtime use;
- `health.toml` — health and readiness checks;
- `storage.toml` — owned mutable paths and excluded authority;
- `backup.toml` — presentation-state backup and restore scope;
- `degradation.toml` — explicit failure and removal behavior;
- `interface/*.json` — admitted declarative Space and interface artifacts;
- `adapter/pyproject.toml` — adapter package metadata for the subsequent bundle.

## Activation gate

Activation requires all of the following:

1. a verified immutable upstream source revision in `source.lock.json`;
2. schema-valid Space definitions and module manifests;
3. verified signatures or hashes required by the active profile;
4. resolution of every required module, route, widget, icon, localization, and page reference;
5. route-collision, capability, offline, accessibility, and readiness checks;
6. an atomic activation receipt and a verified previous Space for rollback.

Missing optional modules are omitted without substitution. A missing required
module, invalid required manifest, unresolved default module, or unavailable
receipt path blocks activation.
