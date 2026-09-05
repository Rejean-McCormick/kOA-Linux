<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-RECIPES-000",
  "document_class": "non_normative_readme",
  "status": "active",
  "language": "en",
  "layer": "recipes",
  "scope": [
    "non_normative_implementation_guidance",
    "profile_conditioned_examples"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "generated/toolchain-catalog.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json",
    "contracts/architecture-patterns.contract.json",
    "02-system/34-architecture-patterns.md",
    "06-lifecycle/20-resilience-and-projection-artifacts.md",
    "08-operations/20-architecture-pattern-operations.md",
    "09-conformance/22-architecture-pattern-conformance.md",
    "contracts/subsystems/koa-spaces.subsystem.json",
    "02-system/21-koa-spaces-experience-layer.md",
    "02-system/22-koa-spaces-interface-composition.md",
    "02-system/24-koa-spaces-design-system.md",
    "03-profiles/14-koa-spaces-deployment.md"
  ],
  "decision_ids": [
    "DEC-PROFILE-001",
    "DEC-CONTAINER-001",
    "DEC-K8S-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-GATE-001",
    "DEC-AI-001",
    "DEC-SENT-001",
    "DEC-REL-001",
    "DEC-DOC-CHANGE-001"
  ],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-PROFILE-001",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SENT-001",
    "LOCK-DEV-001",
    "LOCK-DEV-002",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DEV-005",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-SPACES-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-DEV-006",
    "DOC-DEV-016",
    "DOC-LIFE-013",
    "DOC-LIFE-015",
    "DOC-LIFE-016",
    "DOC-LIFE-019",
    "DOC-SEC-001",
    "DOC-SEC-012",
    "DOC-OPS-000",
    "DOC-OPS-009",
    "DOC-OPS-019",
    "DOC-CONF-010",
    "DOC-ADR-003",
    "DOC-SYS-021",
    "DOC-SYS-022",
    "DOC-SYS-035",
    "DOC-PROFILE-014"
  ],
  "tags": [
    "recipes",
    "readme",
    "non-normative",
    "implementation-guidance",
    "profiles",
    "development",
    "operations",
    "recovery",
    "build-farm",
    "validation",
    "cleanup",
    "safe-examples",
    "architecture-patterns",
    "koa-spaces",
    "experience-layer"
  ]
}
KOA:DOC-META:END -->

# kOA Recipes

## 1. Purpose

This directory contains practical, non-authoritative implementation guidance for common kOA development, deployment, validation, operations, recovery, and maintenance tasks.

Recipes translate active contracts into bounded examples.

They do not define:

- architecture;
- component authority;
- data ownership;
- profile composition;
- security policy;
- release compatibility;
- artifact identity;
- operational approval;
- exceptions;
- conformance.

The authority chain remains:

`text
accepted decisions and locks
 ↓
canonical registries
 ↓
active component, profile, artifact, and integration contracts
 ↓
normative system, security, lifecycle, operations, and conformance documents
 ↓
runbooks and approved local configuration
 ↓
recipes and examples
`

A recipe is usable only when every authority above it remains compatible.

### 1.1 What a recipe provides

A useful recipe provides:

- one bounded objective;
- applicable profiles and overlays;
- prerequisites;
- exact source contracts;
- expected inputs;
- example commands or configuration;
- state changes;
- validation;
- cleanup;
- rollback or safe exit;
- known limitations;
- related tests and evidence.

### 1.2 What a recipe cannot provide

A recipe cannot:

- approve a profile;
- create a component;
- create an authoritative data domain;
- grant a service identity;
- grant privilege;
- authorize a network path;
- authorize an external integration;
- approve an AI provider;
- create a release;
- approve a migration;
- approve a restore;
- create an exception;
- claim conformance.

### 1.3 Reader rule

Before executing a recipe, resolve:

1. the active primary profile and overlays;
2. the active component contracts;
3. the active Release Set;
4. the target environment;
5. the applicable data and security boundaries;
6. the required operator or developer authority;
7. the expected evidence;
8. the cleanup or recovery path.

When those facts cannot be resolved, stop before performing a state-changing step.

## 2. Scope

### 2.1 Included recipe classes

Recipes can cover:

- developer workspace creation;
- UV and `.venv` setup;
- local service containers;
- workspace-specific ports, networks, volumes, secrets, and databases;
- local build and validation;
- toolchain use;
- artifact candidate creation;
- profile-scoped service startup;
- local readiness checks;
- offline bundle inspection;
- backup verification;
- clean restore exercises;
- build-farm worker and job examples;
- integration-manifest examples;
- evidence collection;
- troubleshooting and cleanup;
- decommissioning examples.

### 2.2 Excluded content

Recipes are not the correct location for:

- new requirements;
- new decision authority;
- component responsibility changes;
- ownership changes;
- permanent security exceptions;
- provider approval;
- profile definitions;
- artifact schemas;
- release-channel definitions;
- production credentials;
- private keys;
- customer or tenant data;
- unrestricted diagnostic exports;
- generated conformance claims.

### 2.3 Environment classes

A recipe identifies one or more explicit environment classes.

Common environment classes include:

| Environment class | Typical use |
| --- | --- |
| `developer_linux_workstation` | Local development and component testing |
| `developer_windows_wsl` | Local development through WSL |
| `build_farm` | Reproducible build and validation jobs |
| `user_lightweight` | User-scale local installation examples |
| `sovereign_linux_node` | Profile-controlled local sovereign node procedures |
| `sovereign_hub` | Hub-level deployment and operations examples |
| `control_plane` | Profile-selected orchestration and administrative examples |
| `recovery_environment` | Clean backup, restore, rollback, or credible-exit exercises |
| `documentation_environment` | Documentation generation and validation |

A recipe written for one environment does not automatically apply to another.

### 2.4 Risk classes

Every recipe identifies one risk class.

| Risk class | Meaning |
| --- | --- |
| `read_only` | Observes state without mutation |
| `local_disposable` | Mutates only isolated disposable local state |
| `local_persistent` | Mutates profile-owned local persistent state |
| `artifact_candidate` | Produces a candidate artifact without publication or activation |
| `operational_change` | Changes an active service or profile-owned configuration |
| `privileged_operation` | Requires a closed privileged operation |
| `migration` | Changes persistent component-owned state |
| `restore` | Reconstructs authority from retained recovery material |
| `publication_request` | Requests artifact or content publication through its owner boundary |
| `decommissioning` | Removes a service, worker, integration, or environment |

Higher-risk classes require stronger prerequisites, validation, evidence, and cleanup.

## 3. Canonical References

### 3.1 Authority and decisions

`text
generated/authority-manifest.json
generated/decision-index.json
generated/requirements-index.json
generated/assertion-index.json
generated/decision-index.json
`

Recipes always defer to active authority.

### 3.2 Components and profiles

`text
contracts/system.contract.json
generated/component-catalog.json
generated/component-catalog.json
contracts/components/*.component.json
generated/profile-catalog.json
contracts/profiles/*.profile.json
`

A recipe cannot infer component or profile behavior from a container name, process name, directory name, or prior deployment.

### 3.3 Toolchains and development

`text
generated/toolchain-catalog.json
contracts/toolchains/*.toolchain.json
`

Python recipes use the active UV toolchain contract and a workspace-local `.venv`.

### 3.4 Artifacts and releases

`text
contracts/release-channels.contract.json
contracts/artifact-classes.contract.json
contracts/artifact-contracts/*.schema.json
`

Recipes can produce candidate artifacts.

Publication and activation remain separate lifecycle transitions.

### 3.5 Integrations

`text
contracts/integration-types.contract.json
contracts/artifact-contracts/integration-manifest.schema.json
contracts/examples/integration-manifest.example.yaml
`

An example integration manifest is not provider approval or production configuration.

### 3.6 Evidence and validation

`text
generated/traceability.json
generated/test-catalog.json
generated/evidence-catalog.json
generated/exception-index.json
`

Tests and evidence referenced by a recipe remain owned by these registries.

## 4. Recipe Model

### 4.1 Recipe identity

Each recipe uses a stable path and a descriptive lowercase filename.

Recommended format:

`text
NN-action-object.md
`

Examples:

`text
01-create-python-workspace.md
02-start-isolated-service-stack.md
03-run-component-contract-tests.md
04-stage-offline-bundle.md
05-verify-clean-restore.md
`

A filename is not a canonical identifier.

When a recipe has metadata, use a stable `DOC-RECIPE-*` identifier registered by the documentation authority.

### 4.2 Recipe state

A recipe can have one of these documentation states:

- `active`;
- `deprecated`;
- `superseded`;
- `retired`.

The state describes the guidance.

It does not describe the state of a component, artifact, release, migration, restore, or integration.

### 4.3 Required recipe header

A complete recipe begins with a compact declaration such as:

`yaml
recipe:
 title: Create an isolated Python workspace
 status: active
 language: en
 risk_class: local_disposable
 primary_profiles:
 - developer_linux_workstation
 - developer_windows_wsl
 compatible_overlays: []
 prohibited_profiles:
 - sovereign_offline
 owner: development-tooling
 canonical_refs:
 - contracts/toolchains/python-uv.toolchain.json
 - 05-development/03-python-uv.md
 expected_tests:
 - TEST-DEV-UV-001
 expected_evidence: []
`

Exact metadata structure can be standardized later by an active schema.

Until then, the human-readable declaration remains non-authoritative.

### 4.4 Required recipe sections

A complete recipe contains these sections:

1. Purpose
2. Applicability
3. Preconditions
4. Inputs
5. Safety and authority boundaries
6. Procedure
7. Validation
8. Cleanup
9. Rollback or safe exit
10. Failure handling
11. References

A read-only recipe can state that cleanup and rollback are not applicable.

### 4.5 Preconditions

Preconditions identify:

- current directory;
- workspace identity;
- active profile;
- selected overlays;
- required component or toolchain versions;
- required services;
- required role;
- required secrets by reference;
- expected network mode;
- free ports or namespaced port allocation;
- storage capacity;
- backup or known-good state;
- test fixtures;
- commands used to verify readiness.

Preconditions are executable checks where practical.

### 4.6 Inputs

Inputs distinguish:

- user-supplied values;
- environment-derived values;
- canonical references;
- generated temporary values;
- secret references;
- artifact identities;
- paths;
- ports;
- database names;
- workspace names.

Examples use clearly disposable identities.

They do not use real production secrets, real tenant data, or unexplained values.

### 4.7 Procedure steps

Procedure steps are:

- ordered;
- bounded;
- reversible where possible;
- explicit about state changes;
- explicit about current directory;
- explicit about shell and platform assumptions;
- explicit about profile applicability;
- explicit about user and privilege context;
- safe to stop at declared checkpoints.

Commands do not silently depend on state established outside the recipe.

### 4.8 Validation

Validation proves the recipe objective rather than merely checking process existence.

Examples include:

- exact UV environment and lock resolution;
- isolated port and database names;
- service readiness;
- component contract tests;
- artifact schema validation;
- negative access tests;
- restore acceptance;
- no foreign authoritative write;
- expected candidate identity;
- cleanup verification.

A command returning exit code zero is not always sufficient validation.

### 4.9 Cleanup

Cleanup addresses every mutable resource created by the recipe:

- processes;
- containers;
- networks;
- volumes;
- databases;
- schemas;
- users;
- queues;
- indexes;
- secrets;
- credentials;
- ports;
- sockets;
- temporary files;
- `.venv`;
- caches;
- staging areas;
- test artifacts;
- logs.

A recipe that retains state identifies the owner, retention reason, location, and later cleanup path.

### 4.10 Rollback or safe exit

Rollback or safe exit identifies:

- last safe checkpoint;
- state that can be deleted;
- state that must be preserved;
- known-good artifact or configuration;
- owner-controlled restore or repair path;
- commands that are safe to repeat;
- commands that are not safe to repeat;
- evidence to retain.

A recipe does not improvise rollback for irreversible migration or restore stages.

## 5. Directory and Naming Conventions

### 5.1 Recommended category grouping

Recipes can be grouped by topic when the directory grows.

Recommended category names include:

`text
development/
containers/
databases/
build/
artifacts/
profiles/
operations/
backup/
restore/
offline/
security/
integrations/
build-farm/
documentation/
troubleshooting/
decommissioning/
`

Category creation should follow actual content rather than creating empty directory structure.

### 5.2 Filename rules

Use filenames that are:

- lowercase;
- hyphen-separated;
- action-oriented;
- specific;
- stable;
- free of provider credentials, hostnames, tenant names, or dates unless the recipe is intentionally historical.

Good:

`text
verify-offline-bundle.md
create-isolated-postgres.md
run-language-pack-validation.md
reset-build-worker.md
`

Avoid:

`text
misc.md
new-setup.md
prod-fix.md
final-final.md
customer-a-recovery.md
`

### 5.3 Command formatting

Use fenced code blocks with an explicit language.

Examples:

`bash
uv sync --frozen
`

`powershell
uv sync --frozen
`

`yaml
services:
 example:
 image: example.invalid/immutable-reference
`

Commands with destructive effects include a warning immediately before the block.

### 5.4 Placeholder formatting

Use visible example placeholders only inside explicitly marked example blocks.

Preferred style:

`text
<workspace-id>
<component-id>
<artifact-id>
<profile-id>
`

A recipe explains how to resolve each placeholder.

Unresolved placeholders are not permitted in commands presented as directly executable.

### 5.5 Paths

Repository-relative paths use forward slashes.

Examples:

`text
docs/generated/profile-catalog.json
generated/evidence/
`

Host-specific absolute paths appear only when the recipe explicitly targets that host and profile.

### 5.6 Port and service names

Examples derive names from a stable workspace identity.

Example pattern:

`text
workspace_id: koa-dev-42
service_name: koa-dev-42-orgo
database_name: koa_dev_42_orgo
volume_name: koa-dev-42-orgo-data
`

Hard-coded common ports are acceptable only for isolated examples that prove collision handling or reserve the port through the active workspace contract.

## 6. Profile and Implementation Boundaries

### 6.1 Profile-first interpretation

A recipe begins by identifying the effective profile.

The same objective can have different implementations.

Examples:

- Linux development can prefer rootless Podman;
- Windows/WSL can use Docker or Podman;
- sovereign Linux can prefer rootless Podman and Quadlet;
- a build farm requires OCI compatibility;
- Kubernetes can be used by selected `control_plane`, `build_farm`, or `sovereign_hub` profiles;
- Kubernetes is not required on endpoints;
- `appliance_shell` can use minimal Wayland and an embedded web engine;
- standard user and developer Linux profiles can use maintained GNOME, KDE Plasma, or another desktop.

A recipe states the selected implementation instead of presenting it as global architecture.

### 6.2 Container boundary

A container recipe preserves:

- component identity;
- network boundaries;
- storage ownership;
- database identities;
- secret scopes;
- health and readiness;
- resource limits;
- artifact identity;
- cleanup.

Containerization does not create authorization or data ownership.

### 6.3 systemd and Quadlet boundary

A systemd or Quadlet recipe applies only where the active profile selects that mechanism.

The recipe does not convert systemd or Quadlet into a component contract.

Unit names, restart behavior, credentials, writable paths, and privileges remain profile- and service-specific.

### 6.4 Kubernetes boundary

A Kubernetes recipe identifies:

- selected profile;
- cluster authority;
- namespace and tenant boundary;
- workload identity;
- network policy;
- persistent storage;
- secrets;
- artifact identity;
- resource envelope;
- release relationship;
- cleanup.

Kubernetes object status does not replace component readiness.

### 6.5 Wayland and appliance boundary

An appliance-shell recipe applies only to the `appliance_shell` overlay.

It preserves:

- native recovery;
- local navigation;
- approved local origins;
- restricted general browsing;
- component ownership;
- profile-specific activation;
- known-good rollback.

It does not impose no-GNOME behavior globally.

### 6.6 Developer workspace boundary

A development recipe uses one workspace identity to namespace:

- `.venv`;
- services;
- ports;
- networks;
- volumes;
- databases;
- schemas;
- users;
- queues;
- indexes;
- secrets;
- logs;
- temporary state.

Two branches or worktrees can run concurrently without collisions.

### 6.7 Build-farm boundary

A build-farm recipe preserves:

- immutable job request;
- clean worker;
- isolated workspace;
- exact toolchains;
- exact dependencies;
- candidate identity;
- provenance;
- tests;
- evidence;
- worker cleanup;
- no signing or activation authority.

## 7. Security, Data, AI, and Lifecycle Safeguards

### 7.1 Identity and privilege

Recipes identify the expected user and service identity.

A privileged step uses a closed profile-approved operation.

Avoid examples that use:

- unrestricted root shells;
- broad database administrator accounts;
- shared service credentials;
- disabled confinement;
- host networking;
- broad host mounts;
- unrestricted device access.

When a privileged example is unavoidable, document:

- exact capability;
- reason;
- profile;
- duration;
- verification;
- cleanup;
- evidence;
- active exception when required.

### 7.2 Secrets

Recipe files never contain real secrets.

Use protected references such as:

`text
secret://development/example-service/token
`

Examples do not place secrets in:

- command history;
- source;
- images;
- build arguments;
- manifests;
- logs;
- receipts;
- screenshots;
- copied terminal output.

### 7.3 Data authority

A recipe cannot repair one component by writing into another component's storage.

Valid cross-component examples use:

- registered APIs;
- commands;
- events;
- artifacts;
- controlled import;
- owner-controlled migration;
- owner-controlled restore;
- Publication Gateway;
- UCKK Import Bridge and UCKK Publication Bridge.

### 7.4 Databases

Database recipes identify:

- owning component;
- database or schema;
- runtime user;
- migration user;
- backup user;
- restore user;
- read-only consumers;
- profile;
- cleanup.

A shared database server can host several components only with independently enforceable identities and permissions.

### 7.5 Backups and restore

A backup recipe proves:

- inventory;
- ownership;
- encryption;
- artifact and Release Set relationship;
- retention;
- readability;
- restore metadata.

A restore recipe uses:

- a clean compatible target;
- component-owned restore interfaces;
- migrations;
- derived-state rebuild;
- readiness;
- critical workflows;
- evidence.

Backup bytes alone do not establish restore success.

### 7.6 Artifacts and releases

A recipe can:

- build a candidate;
- validate a candidate;
- generate provenance;
- create an SBOM;
- stage inactive artifacts;
- request publication.

A recipe cannot mark an artifact active without the registered lifecycle and release authority.

Promotion does not rebuild content under the same identity.

### 7.7 External integrations

Integration recipes identify:

- provider or peer;
- registered capability;
- active profile;
- user or operator trigger;
- data classes;
- credential reference;
- endpoint policy;
- timeout and retry;
- response class;
- candidate or action handling;
- receipts;
- removal.

Reachability and credentials do not imply provider approval.

### 7.8 External AI

AI-related recipes preserve .

They use only approved capability-specific surfaces.

They include:

- explicit user initiation;
- selected and minimized data;
- provider disclosure;
- confirmation;
- prohibited-data checks;
- candidate identity;
- provenance;
- destination adoption;
- no direct canonical write;
- offline unavailability;
- no silent provider or local AI fallback.

### 7.9 SenTient

SenTient recipes apply only to:

- `developer_linux_workstation`;
- `developer_windows_wsl`;
- `build_farm`.

They isolate:

- workspace;
- dependencies;
- `.venv`;
- storage;
- services;
- secrets;
- network;
- resources;
- inputs;
- outputs;
- evidence.

SenTient output remains candidate material.

### 7.10 UCKK and publication

A UCKK recipe keeps these boundaries separate:

- the online UCKK platform owns final UCKK objects;
- UCKK Import Bridge coordinates explicit inbound retrieval and quarantine;
- Suno and Gamma are optional external-processing adapters;
- Publication Gateway authorizes external publication and the UCKK Publication Bridge performs UCKK-specific transport.

A recipe does not substitute one path for another.

## 8. Execution and Validation

### 8.1 Preflight

A recipe preflight can verify:

`text
repository state
workspace identity
profile and overlays
component and contract versions
Release Set
toolchain versions
required commands
available resources
port and service allocation
secret references
network mode
backup or known-good state
`

Preflight failure stops state-changing execution.

### 8.2 Dry-run and preview

Risk-bearing recipes provide a preview or dry-run when the underlying tool safely supports it.

A preview shows:

- affected resources;
- intended state changes;
- deletions;
- migrations;
- artifact identities;
- network changes;
- privilege use;
- cleanup.

A dry-run is not evidence that the real operation will succeed.

### 8.3 Idempotency

A repeatable recipe identifies its idempotency behavior.

Possible classes include:

- safe to repeat;
- safe to resume from named checkpoints;
- safe only after cleanup;
- one-time migration;
- destructive and not repeatable.

A recipe does not imply idempotency from a tool's declarative syntax alone.

### 8.4 Terminal results

Recipe validation records an actual terminal result such as:

- pass;
- fail;
- blocked;
- unavailable;
- skipped;
- incomplete;
- not applicable.

Only a passing executed check supports a passing claim.

A skipped or unavailable check remains visible.

### 8.5 Evidence

Evidence produced by a recipe identifies:

- recipe path and version;
- profile;
- environment;
- component or artifact;
- command or step;
- result;
- actor;
- time;
- correlation identity;
- test;
- evidence reference;
- cleanup state.

Recipe output is not automatically canonical evidence.

The active evidence schema and registry determine admissibility.

### 8.6 Negative tests

Security, ownership, integration, migration, and restore recipes include negative tests where applicable.

Examples:

- foreign database write denied;
- undeclared endpoint denied;
- prohibited data transfer denied;
- direct AI adoption denied;
- cross-tenant read denied;
- partial Release Set activation denied;
- stale artifact denied;
- invalid restore source denied.

Negative tests also verify that authoritative state remained unchanged.

### 8.7 Clean-state validation

A recipe that claims reproducibility, restore, migration, or conformance uses a clean environment where the active contract requires it.

Local residue cannot support the claim.

Clean-state validation includes:

- isolated workspace;
- declared inputs;
- declared toolchains;
- isolated services;
- explicit network behavior;
- cleanup verification.

### 8.8 Example output

Example output is labelled clearly:

`text
Example output
--------------
profile: developer_linux_workstation
workspace_id: koa-example-01
result: pass
`

Do not present fabricated output as captured execution evidence.

## 9. Failure Handling and Cleanup

### 9.1 Stop conditions

A recipe identifies stop conditions such as:

- profile mismatch;
- missing owner;
- unresolved Release Set;
- missing backup;
- incompatible schema;
- unknown artifact identity;
- broad credential;
- undeclared network access;
- foreign-write path;
- failed negative test;
- missing evidence;
- ambiguous destructive target;
- failed cleanup;
- incomplete readiness.

### 9.2 Failure response

On failure:

1. stop new mutations;
2. preserve relevant diagnostics;
3. preserve authoritative source state;
4. identify partial changes;
5. revoke temporary credentials or privilege;
6. isolate affected services or staging;
7. use the declared cleanup, rollback, clean retry, or forward-repair path;
8. record the terminal result accurately.

### 9.3 Cleanup verification

Cleanup is verified rather than assumed.

Checks can confirm:

- no process remains;
- no container remains;
- no writable volume remains;
- no database or schema remains;
- no port is held;
- no temporary credential remains;
- no network or endpoint remains;
- no `.venv` remains when disposable;
- no staging pointer is active;
- retained artifacts and evidence are intentional.

### 9.4 Failed cleanup

Failed cleanup leaves the recipe state open.

The affected workspace, worker, service, or environment can require quarantine.

Do not reuse potentially contaminated state for a conformance or release claim.

### 9.5 Destructive commands

Destructive commands are:

- explicit;
- narrowly scoped;
- preceded by target verification;
- separated from observation commands;
- not hidden in command substitution;
- not combined with broad wildcard expansion;
- accompanied by cleanup or restore expectations.

Avoid examples such as:

`bash
rm -rf /
`

or broad database, volume, queue, or namespace deletion without exact target resolution.

## 10. Contribution, Review, and Lifecycle

### 10.1 Adding a recipe

A new recipe contribution includes:

- bounded purpose;
- owner;
- profile applicability;
- canonical references;
- risk class;
- complete prerequisites;
- reproducible commands;
- validation;
- cleanup;
- failure behavior;
- tested example environment;
- review record.

### 10.2 Review roles

Reviewers depend on recipe scope.

Possible reviewers include:

- component owner;
- profile owner;
- development tooling owner;
- operations owner;
- security owner;
- data owner;
- release owner;
- integration owner;
- recovery owner;
- documentation owner.

A documentation review cannot substitute for the required technical owner.

### 10.3 Review triggers

Review a recipe when any referenced item changes semantically:

- profile;
- component contract;
- toolchain;
- artifact schema;
- release model;
- security boundary;
- integration;
- privilege path;
- migration;
- backup or restore;
- cleanup;
- operating system or container mechanism;
- ADR.

### 10.4 Deprecation

A deprecated recipe states:

- reason;
- replacement;
- affected profiles;
- last compatible versions;
- migration guidance;
- removal condition.

The path remains reserved according to documentation lifecycle rules.

### 10.5 Supersession

A superseding recipe links the prior recipe.

The prior recipe remains available for historical Release Sets and older supported environments when retention requires it.

### 10.6 Recipe validation

Documentation validation checks:

- metadata JSON;
- active language;
- references;
- no unresolved placeholders;
- no real secrets;
- no unsupported normative requirement block;
- no hidden global profile assumptions;
- no direct foreign-write guidance;
- no false conformance claim;
- no ordinary Markdown hash fields.

Technical validation runs in the environments declared by the recipe.

### 10.7 Change authority

Changing a recipe does not automatically require an architecture decision.

A recipe change requires a semantic owner decision when it changes or reveals a change to:

- component authority;
- data ownership;
- profile semantics;
- security boundary;
- integration authority;
- release compatibility;
- migration behavior;
- restore authority;
- lifecycle semantics.

The canonical change occurs first.

The recipe follows.

## 11. Examples and Anti-Patterns

### 11.1 Valid development recipe

A valid Python workspace recipe:

- applies to developer profiles;
- creates a stable workspace identity;
- uses UV;
- creates a workspace-local `.venv`;
- allocates namespaced services and ports;
- uses test credentials;
- validates isolation;
- removes disposable state.

It does not reuse a global virtual environment.

### 11.2 Valid service-container recipe

A valid service-container recipe:

- selects a profile-permitted OCI runtime;
- resolves immutable image identity;
- uses rootless execution where the selected profile requires or prefers it;
- declares network and volume ownership;
- defines health and readiness;
- sets resource limits;
- validates no foreign database access;
- cleans all workspace resources.

It does not make Podman, Docker, or Kubernetes a global application contract.

### 11.3 Valid artifact recipe

A valid artifact recipe:

- uses exact source and toolchains;
- builds in a clean environment;
- assigns a candidate identity;
- generates provenance;
- generates the required dependency inventory;
- runs applicable tests;
- keeps the candidate inactive;
- requests publication through the registered boundary.

It does not activate the artifact.

### 11.4 Valid restore recipe

A valid restore recipe:

- selects a verified source;
- uses a clean compatible target;
- restores trust, policy, Release Set, and component-owned data in declared order;
- runs migrations;
- rebuilds derived state;
- validates readiness and critical workflows;
- removes temporary recovery authority.

It does not write directly across component boundaries.

### 11.5 Valid external AI recipe

A valid ChatGPT assistance recipe:

- applies only where the active profile permits it;
- requires explicit user action;
- presents selected data;
- removes prohibited information;
- uses a scoped credential reference;
- sends one bounded request;
- creates a candidate;
- records provenance;
- imports through the destination component;
- remains unavailable offline.

It does not update canonical state directly.

### 11.6 Valid appliance-shell recipe

A valid appliance-shell recipe:

- activates only under the overlay;
- uses the selected maintained Wayland and embedded-engine artifacts;
- limits local origins and browser permissions;
- preserves native recovery;
- validates offline behavior;
- validates rollback;
- leaves standard Linux desktop profiles unchanged.

### 11.7 Invalid global implementation rule

A recipe says:

> All kOA Linux installations use the same compositor, prohibit GNOME, run Podman with Quadlet, and require Kubernetes.

The recipe is invalid because these are profile-scoped decisions and Kubernetes is not an endpoint requirement.

### 11.8 Invalid authority shortcut

A troubleshooting recipe says:

> Connect with the database administrator account and edit the affected component tables directly.

The recipe is invalid because administrator access does not create component data authority.

Use the owning component's repair, migration, or restore contract.

### 11.9 Invalid secret example

A recipe contains:

`text
API_TOKEN=real-provider-secret
`

The recipe is invalid.

Use a protected example reference and document how the runtime resolves it.

### 11.10 Invalid false validation

A recipe says:

> The service process is running, therefore the deployment is conformant.

The statement is invalid.

Process health does not prove contract readiness, profile conformance, ownership, migration, security, or evidence.

### 11.11 Invalid cleanup

A recipe stops containers but leaves:

- volumes;
- database users;
- secrets;
- ports;
- queues;
- network routes;
- temporary credentials.

The recipe is incomplete and the environment remains contaminated.

### 11.12 Invalid AI fallback

A recipe says:

> When ChatGPT is unavailable, start a local model automatically.

The recipe is invalid under .

The external capability becomes unavailable while native local operation remains available.

## Architecture pattern implementation

Recipes that implement remote calls, asynchronous workers, multi-owner workflows, media transfer, experience aggregation, projections, or caches must begin from `contracts/architecture-patterns.contract.json` and the matching artifact contract. Recipe values may tighten profile limits but cannot weaken authority, retention, quarantine, staleness, or terminal-evidence rules.

## kOA Spaces Recipes

Recipes under `11-recipes/user-lightweight/` illustrate activation, contextual Space composition, and the current reference frontend stack. `koa-spaces-reference-frontend.md` records the Next.js, React, TypeScript, Ant Design, Pro Components, and pnpm reference implementation while keeping those technologies non-authoritative at the global architecture level. They remain non-authoritative implementation guidance. They cannot redefine profile membership, artifact schemas, authorization, subsystem ownership, or the canonical kOA Spaces boundary.
