# Contract fixtures and tests

This directory contains deterministic repository-level contract tests. The suite validates:

- the exact inventories and stable identities of component, subsystem, and profile contracts;
- the four independent release channels and a minimal valid Release Set;
- all artifact-contract JSON Schemas as Draft 2020-12 schemas;
- a minimal valid offline bundle;
- the public Python bindings and, when B-0014 through B-0016 are present, every binding payload against its dependency-owned schema.

## Fixtures

- `minimal-profile-plan.json` is a deterministic discovery fixture. It is not a new profile authority.
- `minimal-release-set.json` validates against `release-set.schema.json`.
- `offline-bundle.json` validates against `offline-bundle.schema.json`.
- `invalid-signature.json` is intentionally invalid only because `verification_status` is outside the schema enum. The test asserts that exact failure path and keyword.

## Running

```sh
PYTHONPATH=interfaces/python/src pytest -q tests/contracts
```

The tests perform no network access and do not mutate repository files. A missing dependency schema is reported as an explicit skip only in the binding-to-schema test; it becomes executable automatically when the dependency bundle is integrated.
