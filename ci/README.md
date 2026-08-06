# Continuous integration orchestration

This directory contains reusable CI policy and orchestration. Hosted workflows are deliberately thin: they provision the declared toolchain and call the same repository-local commands that a developer runs from the repository root.

## Required checks

`ci/policies/required-checks.json` owns the stable workflow, job, and required-context names. The required contexts are:

- `CI / Documentation / documentation`
- `CI / Contracts / contracts`
- `CI / Components / components`

All three workflows run for pull requests and merge queues without `paths` filters. This guarantees that every required context is emitted. `path-filters.json` may narrow work inside local orchestration, but it may not suppress a required workflow or turn `skipped`, `blocked`, `neutral`, or `cancelled` into passing evidence.

## Exact local commands

Run these commands from the repository root. The workflow YAML uses the same argument vectors.

### Documentation

```bash
uv sync --frozen --all-groups
uv run --frozen python docs/tools/validate_docs.py
```

### Contracts

```bash
uv sync --frozen --all-groups
uv run --frozen python ci/scripts/run-contracts.py
```

### Components

```bash
uv sync --frozen --all-groups
uv run --frozen python ci/scripts/run-components.py
```

The two `ci/scripts/run-*.py` entrypoints own suite selection and evidence formatting. Workflow YAML must not reproduce that logic. Dependency synchronization is frozen and may use only declared sources. Validation after synchronization is expected to run without network access or secrets.

## Path routing

`ci/policies/path-filters.json` is an impact-routing policy, not a source of architectural authority. It defines:

- global invalidators that affect every check;
- check-specific include sets;
- explicit coverage for every root in the frozen 1,040-path architecture;
- a fail-closed `run_all` fallback for unknown paths.

A root can map to multiple checks. This is intentional when a change can affect contracts, generated projections, component behavior, or documentation alignment at the same time.

## Workflow constraints

The workflows:

- use read-only repository permissions;
- do not use `pull_request_target`;
- do not receive credentials after checkout;
- do not contain release, signing, path-ownership, or architecture logic;
- record stable job names and bounded timeouts;
- disable the setup action's shared cache so it cannot become workspace state;
- do not publish release-authoritative evidence.

Release, security, offline, reproducibility, candidate-build, and evidence-publication gates are owned by later CI bundles and are outside this bundle.
