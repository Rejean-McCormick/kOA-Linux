# kOA-Linux development environments

This directory contains optional, profile-scoped development aids. It does not
make containers a universal kOA runtime requirement and it does not grant
release, activation, publication, policy, or conformance authority.

## Current dependency state

The snapshot contains the public Python bindings under `interfaces/python/` and
the `koa_tools` implementation under `tools/`. The common root Python workspace
owned by B-0001 is incomplete because these required files are absent:

```text
pyproject.toml
uv.lock
.python-version
```

For that reason, both manifests in `dev/workspaces/` are deterministic
`suspended` fixtures. Their `reproducible_dependency_sync` check is `blocked`.
They must not be treated as active workspaces until B-0001 is integrated and
`uv sync --frozen` succeeds.

## Workspace manifests

- `workspaces/default.workspace.json` selects
  `developer_linux_workstation` and rootless containers.
- `workspaces/wsl.workspace.json` selects `developer_windows_wsl` and a
  profile-approved mixed-equivalent isolation mechanism.

The fixture identifiers are stable examples. Before activation, allocate a new
suffix and update every derived namespace consistently. Validation uses:

```text
docs/schemas/developer-workspace.schema.json
```

A workspace owns its `.venv`, mutable state, service names, networks, volumes,
databases, queues, sockets, logs, temporary paths, identities, secrets, ports,
and resource envelope. Cleanup is based on positive workspace ownership labels;
global container or volume pruning is not an ordinary cleanup mechanism.

## Optional container workspace

`containers/compose.yaml` starts one non-authoritative development shell. It:

- requires an explicitly selected base image through `KOA_DEV_BASE_IMAGE`;
- uses no privileged mode, host network, host PID, host IPC, or broad device access;
- drops all Linux capabilities and enables `no-new-privileges`;
- namespaces the project, network, and disposable UV cache by workspace identity;
- mounts the selected source checkout at `/workspaces/koa-linux`;
- applies explicit CPU, memory, and process limits;
- publishes no host port.

The base image is supplied by the active profile or toolchain and should use an
immutable digest. This repository does not invent a universal image identity.

Required environment variables:

```text
KOA_WORKSPACE_ID
KOA_COMPOSE_PROJECT_NAME
KOA_ACTIVE_PROFILE
KOA_DEV_BASE_IMAGE
```

Example startup after B-0001 is available:

```bash
export KOA_WORKSPACE_ID=koa-linux-feature-local001
export KOA_COMPOSE_PROJECT_NAME="$KOA_WORKSPACE_ID"
export KOA_ACTIVE_PROFILE=developer_linux_workstation
export KOA_DEV_BASE_IMAGE='<profile-approved-image>@sha256:<digest>'
podman compose -f dev/containers/compose.yaml up --build
```

Docker or another OCI-compatible backend may be selected only when the active
profile permits it. Kubernetes is not required for this development workflow.

## Public-interface examples

The scripts under `examples/` import only the public `koa_interfaces` package.
They do not import component internals or integration implementation modules.
Run them from a dependency environment where `koa-interfaces` is installed, or
from the public bindings project during development:

```bash
PYTHONPATH=interfaces/python/src python dev/examples/health-probe.py --help
PYTHONPATH=interfaces/python/src python dev/examples/component-client.py --help
PYTHONPATH=interfaces/python/src python dev/examples/integration-adapter.py --help
```

`integration-adapter.py` requires the operation path to be supplied from the
integration's public module-interface declaration. It does not infer, duplicate,
or simulate an external subsystem operation.
