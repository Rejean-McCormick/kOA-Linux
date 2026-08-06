# Subsystem Documentation Mounts

These stable locations are reserved for authoritative documentation of independently owned kOA ecosystem systems integrated with or hosted by kOA-Linux Operating System:

- `subsystems/ariane/` — Ariane
- `subsystems/konnaxion/` — Konnaxion
- `subsystems/orgo/` — Orgo
- `subsystems/sentient/` — SenTient
- `subsystems/semantik-architect/` — SemantiK Architect
- `subsystems/koa-spaces/` — kOA Spaces

Each location may remain absent until its documentation is available. kOA Spaces remains optional even when its mount is present; the mount provides internal subsystem documentation, not runtime authority. Install a directory junction or symbolic link at the reserved path. Do not use Windows `.lnk` shortcut files.

## UCKK exclusion

`subsystems/uckk/` is not a reserved mount and must not be created as an active subsystem documentation path.

UCKK is an external online Moodle platform outside kOA-Linux. It has its own Mediatheque, authority, storage, lifecycle, identity, access control, and operational documentation. kOA-Linux documents two separate controlled integrations: publication from the private kOA Mediatheque to UCKK, and import of selected UCKK learning packages for explicit local acceptance and offline use. The shared Mediatheque frame does not create a subsystem mount, shared database, or synchronization authority.

The kOA Mediatheque is an internal kOA-Linux component. Its documentation belongs in the kOA-Linux component and contract trees, not under `subsystems/`.
