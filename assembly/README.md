# kOA Assembly

`koa-assembly` is the contract-loading and immutable-model foundation for the
kOA-Linux assembly pipeline.  It reads authority; it does not invent deployment
membership.

## Authority boundary

The assembly engine follows this order:

1. global system baseline;
2. exactly one primary profile;
3. zero or more explicitly compatible overlays;
4. applicable component, artifact, toolchain, security, lifecycle, operations,
   and conformance contracts.

This bundle implements only the core model, strict local loader, diagnostics,
and command-line entry point.  Profile resolution, overlay ordering, membership,
capability closure, plans, renderers, and release-set construction belong to
later bundles.

The model deliberately contains no hand-maintained component or service list.
Those facts must be obtained from canonical contracts and generated plans.

## Strict loading

The loader:

- accepts only normalized repository-relative references;
- restricts reads to configured authority roots;
- resolves symlinks and rejects repository escapes;
- requires UTF-8 and a bounded file size;
- supports JSON, TOML, and YAML;
- rejects duplicate object keys and non-finite numbers;
- requires JSON-compatible values;
- requires a declared local schema by default;
- never downloads a remote schema;
- validates local schemas and instances with JSON Schema 2020-12 support;
- emits deterministic diagnostics containing their source authority;
- returns no contract when any error is present.

JSON Schema dialect URIs such as `https://json-schema.org/draft/2020-12/schema`
identify a schema dialect and are not fetched.  Canonical kOA contract instances
must point to a local repository schema.

## CLI

From the repository root:

```bash
PYTHONPATH=assembly/src python -m koa_assembly doctor
PYTHONPATH=assembly/src python -m koa_assembly validate \
  docs/contracts/system.contract.json \
  docs/contracts/ai-navigation.contract.json
PYTHONPATH=assembly/src python -m koa_assembly inspect \
  docs/contracts/system.contract.json
PYTHONPATH=assembly/src python -m koa_assembly --format json scan docs/contracts
```

Exit codes:

| Code | Meaning |
|---:|---|
| `0` | Every requested authority loaded and validated. |
| `1` | Validation was blocked. |
| `2` | Invalid command-line usage. |
| `3` | Repository environment could not be initialized. |

## Diagnostics

Every diagnostic includes:

- stable code;
- severity;
- message;
- source path and optional JSON pointer;
- canonical authority responsible for the rule;
- optional remediation hint and deterministic context.

Text and JSON output are sorted by severity, source, pointer, code, and message.
A missing source, unresolved schema, schema violation, unsupported format, or
ambiguous contract identity blocks the result.

## Development

```bash
cd assembly
python -m compileall -q src tests
pytest
```

The current bundle supplies shared fixtures in `tests/conftest.py`.  Concrete
profile-resolution and planning tests are owned by later assembly bundles.
