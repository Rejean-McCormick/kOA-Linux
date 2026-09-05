# Koali Spaces integration boundary

This directory is the kOA-Linux-owned boundary for the optional, replaceable
`koa_spaces` experience subsystem.  The executable Koali Spaces implementation
remains in its own source repository and is never vendored into this boundary.

The boundary now closes the complete presentation path required by the current
Koali Spaces contracts: Space definitions, module manifests, themes, local asset
manifests, responsive shell state, health/readiness, HTTP-over-Unix transport,
atomic activation, rollback, and evidence-bound receipts.

## Authority boundary

Koali Spaces owns presentation composition only: the global frame, module
selector, shared top bar, active sidebar, route composition, local presentation
preferences, admitted interface assets and activation receipts.  It does not
own identity, authorization, policy, business workflows, learning progress,
media authority, resource admission, release activation, or privileged host
operations.

Konnaxion remains an independent subsystem.  The reference shell implementation
was structurally aligned with the existing Konnaxion frontend patterns
(responsive fixed sider/drawer, module selector, shared header, Ant Design theme
mapping and PageShell convention), but no Konnaxion business page, workflow,
validation rule, service, database model, or authority is copied into kOA
Spaces.

## Source admission

`source.lock.json` intentionally remains fail-closed.  This passive pack does
not fabricate an upstream repository URI, immutable revision, source digest,
license record or release identity.  Those fields are populated only after the
new Koali Spaces repository is created and reviewed.

## Runtime boundary

The reference implementation uses two local-only listeners in one unprivileged
process:

- presentation HTTP on loopback only (`127.0.0.1:4173` by default);
- control HTTP over `/run/koa/sockets/koa-spaces.sock`.

No public listener or public CDN is required.  The Python boundary adapter ships
a concrete HTTP-over-Unix transport for the control channel.

## Activation

Activation requires a valid Space definition, a valid local interface theme,
all required module manifests, all asset manifests referenced by admitted
modules, the local Koali Spaces shell asset manifest, route/capability/offline
closure, and a receipt binding all of those digests.  Missing optional module
assets disable only that optional contribution.  Missing required assets block
activation or preserve the previous validated Space.
## Capability projection

Koali Spaces never derives or grants capabilities from module manifests. The active capability list is a presentation projection supplied by Koali, bound into activation evidence, and may be refreshed independently through the local control channel. Menu visibility remains presentation-only.

## Interface-first baseline

`community-space.json` and `school-space.json` retain future module slots as disabled templates. Only `space_home` is enabled by the passive interface baseline. Konnaxion, Ariane, Orgo and other independent subsystem contributions appear only after their own source and interface admission succeeds.
