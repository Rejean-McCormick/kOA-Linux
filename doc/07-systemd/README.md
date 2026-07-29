# systemd and Podman Quadlet Examples

These files illustrate the intended trust boundaries and hardening posture. They are not production-ready units to copy unchanged. Paths, executables, SELinux labels, capabilities, versions, credentials, and health checks must be adapted and verified on the selected base distribution.

## Placement

- critical host services: native systemd units;
- application services: rootless Podman with Quadlet where feasible;
- system identities: `sysusers.d`;
- persistent/runtime directories: `tmpfiles.d`;
- targets: startup ordering and recovery modes.

## Important limitation

The sample `koa-node-agent.service` runs as root because it represents a privileged broker. Production implementations should split high-risk mechanisms into narrower helpers or system services where this reduces privilege without creating an ungoverned generic control surface.
