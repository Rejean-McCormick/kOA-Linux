## Summary

<!-- State the bounded result delivered by this pull request. Do not describe planned future work as completed. -->

## Change identity and scope

- Bundle or CHG-ID:
- Semantic class: `patch` / `minor` / `major` / `ordinary implementation`
- Canonical owner(s):
- Exact paths created or modified:
- Explicitly out of scope:

## Authority consulted

- `docs/AI_CONTEXT.md`
- Owning contract(s):
- Normative document(s):
- Decision, requirement, lock, exception, and schema references:

## Impact and compatibility

- Authority or ownership impact:
- Public interface and dependency impact:
- Profile, deployment, offline, security, privacy, and resource impact:
- Compatibility or migration requirements:
- Generated outputs and their canonical sources:

## Validation performed

| Command | Exit code | Result | Evidence or notes |
| --- | ---: | --- | --- |
|  |  | `pass` / `fail` / `blocked` |  |

<!-- Never report a skipped, unavailable, incomplete, or failing required check as passed. -->

## Tests and evidence

- Success cases:
- Failure and degradation cases:
- Contract, boundary, ownership, dependency, and generated-content checks:
- Evidence or receipt references:

## Recovery

- Rollback plan:
- Forward-repair plan when rollback is unsafe:
- Last known valid state preserved:

## Review checklist

- [ ] The change is limited to one bounded responsibility and the listed paths.
- [ ] Every changed path is admitted by `.koa/file-architecture.lock.json` and resolves to one canonical owner.
- [ ] No private cross-component import, direct foreign-store write, undeclared authority transfer, fallback, substitution, synchronization, or privilege was introduced.
- [ ] Canonical sources were updated before explanatory or generated projections.
- [ ] Generated files and generated blocks were rebuilt rather than edited manually.
- [ ] Compatibility, migration, rollback, forward repair, and safe degradation were addressed where applicable.
- [ ] Tests cover both success and explicit failure behavior.
- [ ] Exact commands, exit codes, failures, skipped checks, assumptions, and blockers are reported truthfully.
- [ ] No secret, private key, production credential, governed payload, or unrestricted production identity is included.
