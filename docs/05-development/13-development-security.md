<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-DEV-013",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "development",
  "scope": [
    "development_toolchain",
    "profile:developer_linux_workstation",
    "profile:developer_windows_wsl",
    "profile:build_farm"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/terminology.contract.json",
    "contracts/system.contract.json#/ai_boundary",
    "contracts/system.contract.json#/capability_degradation",
    "generated/component-catalog.json#/components/identity_and_trust",
    "generated/component-catalog.json#/components/governance_policy_runtime",
    "generated/component-catalog.json#/components/resource_governor",
    "generated/component-catalog.json#/components/audit_broker",
    "contracts/profiles/developer-linux-workstation.profile.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "contracts/profiles/build-farm.profile.json",
    "contracts/toolchains/python-uv.toolchain.json",
    "contracts/artifact-classes.contract.json",
    "contracts/release-channels.contract.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-AI-001",
    "DEC-CONTAINER-001",
    "DEC-DATA-001",
    "DEC-DEV-001",
    "DEC-DEV-002",
    "DEC-GOV-001",
    "DEC-HW-001",
    "DEC-PROFILE-001",
    "DEC-REL-001",
    "DEC-SENT-001"
  ],
  "requirement_ids": [
    "REQ-DEV-SEC-001",
    "REQ-DEV-SEC-002",
    "REQ-DEV-SEC-003",
    "REQ-DEV-SEC-004",
    "REQ-DEV-SEC-005",
    "REQ-DEV-SEC-006",
    "REQ-DEV-SEC-007",
    "REQ-DEV-SEC-008",
    "REQ-DEV-SEC-009",
    "REQ-DEV-SEC-010",
    "REQ-DEV-SEC-011",
    "REQ-DEV-SEC-012",
    "REQ-DEV-SEC-013",
    "REQ-DEV-SEC-014",
    "REQ-DEV-SEC-015",
    "REQ-DEV-SEC-016",
    "REQ-DEV-SEC-017",
    "REQ-DEV-SEC-018",
    "REQ-DEV-SEC-019",
    "REQ-DEV-SEC-020",
    "REQ-DEV-SEC-021",
    "REQ-DEV-SEC-022",
    "REQ-DEV-SEC-023",
    "REQ-DEV-SEC-024",
    "REQ-DEV-SEC-025",
    "REQ-DEV-SEC-026",
    "REQ-DEV-SEC-027",
    "REQ-DEV-SEC-028",
    "REQ-DEV-SEC-029",
    "REQ-DEV-SEC-030",
    "REQ-DEV-SEC-031",
    "REQ-DEV-SEC-032",
    "REQ-DEV-SEC-033",
    "REQ-DEV-SEC-034",
    "REQ-DEV-SEC-035",
    "REQ-DEV-SEC-036",
    "REQ-DEV-SEC-037",
    "REQ-DEV-SEC-038",
    "REQ-DEV-SEC-039",
    "REQ-DEV-SEC-040",
    "REQ-DEV-SEC-041",
    "REQ-DEV-SEC-042",
    "REQ-DEV-SEC-043",
    "REQ-DEV-SEC-044",
    "REQ-DEV-SEC-045",
    "REQ-DEV-SEC-046",
    "REQ-DEV-SEC-047",
    "REQ-DEV-SEC-048"
  ],
  "lock_ids": [
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-DEV-001",
    "LOCK-DEV-002",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DEV-005",
    "LOCK-GOV-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-SEC-010",
    "LOCK-SENT-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-002",
    "DOC-CONST-013",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-017",
    "DOC-SYS-019",
    "DOC-PROFILE-005",
    "DOC-DEV-000",
    "DOC-DEV-001",
    "DOC-DEV-002",
    "DOC-DEV-003",
    "DOC-DEV-004",
    "DOC-DEV-005",
    "DOC-DEV-006",
    "DOC-DEV-007",
    "DOC-DEV-008",
    "DOC-DEV-009",
    "DOC-DEV-010",
    "DOC-DEV-011",
    "DOC-DEV-012"
  ],
  "tags": [
    "development",
    "security",
    "least-privilege",
    "secrets",
    "dependencies",
    "supply-chain",
    "containers",
    "test-data",
    "provenance",
    "sbom",
    "signing",
    "external-ai",
    "workspace-isolation"
  ]
}
KOA:DOC-META:END -->

# Development Security

> **Document status:** Normative development architecture.  
> **Security objective:** Permit rapid, parallel, reproducible development without granting undeclared authority or weakening production, component, data, identity, or release boundaries.  
> **Authority rule:** Profiles, toolchains, component contracts, artifact classes, integrations, and canonical registries own structured values. This document defines the development-security behavior they must preserve.

## 1. Purpose

This document defines security requirements for kOA development workspaces, developer profiles, local services, toolchains, builds, tests, diagnostics, integrations, and candidate artifacts.

Development security protects:

- developer and service identities;
- source and dependency integrity;
- workspace isolation;
- secrets and cryptographic material;
- component-owned data;
- test and diagnostic data;
- local host integrity;
- build and test execution;
- artifact provenance;
- release and production boundaries;
- offline development continuity;
- incident containment and recovery.

The development environment is trusted only for the capabilities explicitly granted to its actor, workspace, profile, component, toolchain, and artifact workflow.

## 2. Scope

### 2.1 Included scope

This document applies to:

- `developer_linux_workstation`;
- `developer_windows_wsl`;
- build-farm development and validation workspaces;
- source repositories, branches, worktrees, and workspace declarations;
- editors, language servers, extensions, plugins, hooks, generators, and scripts;
- Python, container, and other registered toolchains;
- local databases, queues, caches, search services, and service containers;
- credentials, tokens, keys, certificates, and secret stores;
- fixtures, test databases, snapshots, logs, crash dumps, and diagnostics;
- dependency download, resolution, locking, update, and vulnerability handling;
- local build, test, package, SBOM, provenance, and signing workflows;
- optional external integrations and AI-assisted development;
- development incidents and recovery.

### 2.2 Excluded authority

Development security does not grant:

- production deployment authority;
- production signing authority;
- production secret access;
- policy-bundle activation authority;
- Release Set activation authority;
- publication authority;
- another component's data ownership;
- identity or governance-policy authority;
- permission to bypass profile or workspace boundaries.

### 2.3 Profile-specific mechanisms

The active profile owns implementation mechanisms such as:

- operating-system hardening;
- local firewall and endpoint controls;
- Linux namespaces, cgroups, seccomp, or MAC policies;
- Windows and WSL isolation;
- virtual machines or sandboxes;
- rootless container runtime;
- key-store implementation;
- privileged broker;
- service manager;
- network topology.

This document owns the required security outcome, not one universal mechanism.

## 3. Canonical References

### 3.1 Canonical ownership

| Information | Canonical owner |
| --- | --- |
| Actor identity, authentication, trust, and credential authority | Identity and Trust contract |
| Governed privilege, disclosure, consent, and security exceptions | Governance Policy Runtime contract |
| CPU, memory, I/O, process, worker, queue, and workload limits | Resource Governor contract |
| Cross-component receipts and retained audit evidence | Audit Broker contract |
| Workspace identity and isolation | Developer workspace and workspace-allocation contracts |
| Python dependency and environment rules | `python-uv.toolchain.json` |
| Container-runtime behavior | `container-runtime.toolchain.json` |
| Profile-specific security implementation | Active profile contract |
| External integration and AI data boundaries | `integrations.registry.json` |
| Artifact lifecycle, integrity, signing, and provenance behavior | Artifact classes and artifact contracts |
| Release compatibility and activation | Release-channel and Release Set contracts |
| Normative statements and locks | Requirements and locks registries |
| Approved deviations | Exceptions registry |

### 3.2 Development trust boundaries

The relevant trust boundaries are:

```text
developer actor
→ local host and profile
→ workspace
→ toolchain and build execution
→ component service and data boundary
→ optional integration boundary
→ candidate artifact boundary
→ build and signing authorities
→ release and production authorities
```

Crossing a boundary requires the contract and authority applicable to that boundary.

### 3.3 Integrity material

Digests, signatures, SBOMs, attestations, and provenance receipts are intrinsic to dependency, image, build, and artifact integrity where their owning contracts require them.

They do not authorize an artifact by themselves.

## 4. Model and Responsibilities

### 4.1 Security responsibility model

| Actor or component | Responsibility |
| --- | --- |
| Developer | Uses an identified workspace, protects credentials, reviews changes, and reports suspected compromise |
| Workspace owner | Declares source, services, data, secrets, ports, resources, and cleanup behavior |
| Active profile | Supplies host, isolation, privileged-path, network, and secret-store mechanisms |
| Toolchain contract | Defines dependency, runtime, environment, lock, and reproducibility rules |
| Component owner | Defines component interfaces, data ownership, migrations, and permitted development access |
| Identity and Trust | Resolves actors, services, devices, and trust material |
| Governance Policy Runtime | Decides governed privilege, disclosure, exceptions, and sensitive access |
| Resource Governor | Limits untrusted or heavy execution |
| Audit Broker | Records required security evidence and receipts |
| Build Farm | Produces controlled reproducible candidate artifacts and evidence |
| Release and signing authorities | Admit, sign, bind, and activate release artifacts |
| Integration adapter | Enforces capability and data boundaries for external services |

### 4.2 Least-privilege model

Ordinary development uses:

- unprivileged user processes;
- workspace-scoped credentials;
- rootless services where practical;
- bounded service accounts;
- explicit file and database ownership;
- narrow network exposure;
- profile-approved resource controls.

A sensitive host mutation follows:

```text
identified request
→ applicable policy decision
→ narrow privileged mechanism
→ bounded mutation
→ postcondition verification
→ required receipt
```

Persistent unrestricted administrative shells are not an architectural development dependency.

### 4.3 Secret classes

| Secret class | Development rule |
| --- | --- |
| Workspace-local development secret | Stored in the profile-approved workspace secret store |
| Shared development service credential | Separately authorized, purpose-bound, rotated, and access-controlled |
| Test cryptographic key | Clearly identified as non-production and scoped to test use |
| Staging credential | Used only in approved staging workflows and never generalized to local workspaces |
| Production service credential | Excluded from ordinary developer workstations |
| Production signing or root key | Excluded from ordinary developer workstations and local build scripts |
| Short-lived integration token | Minimum scope, explicit use, expiry, revocation, and no source or log persistence |
| Generated local certificate | Workspace identity, protected private key, explicit expiry, and cleanup |

Secret references can appear in workspace contracts. Secret values do not.

### 4.4 Dependency and toolchain integrity

A reproducible dependency state includes:

- declared source repositories;
- declared package sources;
- version constraints;
- versioned lock state;
- verified package or image identity;
- declared runtime version;
- toolchain identity;
- reviewed update history.

For Python workspaces, `pyproject.toml`, `uv.lock`, the Python version, and a dedicated `.venv` form the installed environment boundary.

A dependency cache can be shared only when content-addressed, non-authoritative, and unable to mutate an installed workspace environment.

### 4.5 Untrusted execution model

Development executes code before that code is trusted for release.

Potentially untrusted execution includes:

- repository hooks;
- dependency installation hooks;
- build backends;
- code generators;
- test fixtures;
- editor extensions;
- language-server plugins;
- imported notebooks;
- database migrations;
- container entrypoints;
- downloaded tools;
- AI-generated scripts or commands.

The active profile applies isolation, resource limits, network restrictions, secret exclusion, and filesystem boundaries appropriate to the risk.

### 4.6 Container security

Containerized development uses:

- rootless execution where supported;
- least capabilities;
- explicit mounts;
- workspace-scoped networks and volumes;
- immutable image identity for reproducible inputs;
- declared ports;
- bounded devices;
- no unrestricted host-control socket;
- no implicit access to user credentials or unrelated workspaces.

A container is not a complete security boundary when host mounts, sockets, privileges, or credentials bypass it.

### 4.7 Development-data model

The preferred order is:

```text
synthetic data
→ generated representative fixtures
→ de-identified or minimized data
→ explicitly authorized sensitive data as a last resort
```

Sensitive development data has:

- documented purpose;
- minimum fields;
- approved actors and workspaces;
- encryption and access control;
- retention deadline;
- deletion and verification procedure;
- export and diagnostic restrictions;
- incident-response classification.

### 4.8 External integration and AI model

An external integration receives one explicit capability request and minimum necessary context.

AI-generated output is untrusted candidate input. It cannot:

- approve its own change;
- access undeclared secrets;
- bypass review;
- change policy;
- sign a production artifact;
- activate a release;
- publish content;
- write directly into component-owned authoritative stores.

### 4.9 Candidate-artifact boundary

A development output can include:

- source revision;
- dependency identity;
- toolchain identity;
- build-environment identity;
- tests;
- SBOM;
- provenance;
- signatures where permitted;
- evidence;
- candidate artifact.

The output remains a candidate.

Production promotion requires the separate authorities assigned to build, signing, artifact admission, Release Set compatibility, and activation.

### 4.10 Security evidence

Security evidence is selective and purpose-bound.

Examples include:

- secret-scan result;
- dependency vulnerability disposition;
- locked dependency validation;
- image-digest resolution;
- least-privilege test;
- container-capability test;
- data-sanitization result;
- SBOM;
- provenance receipt;
- review result;
- incident containment receipt.

Evidence records the result. It does not replace the authority that permitted the underlying operation.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN
source=generated/requirements-index.json#/requirements
ids=REQ-DEV-SEC-001,REQ-DEV-SEC-002,REQ-DEV-SEC-003,REQ-DEV-SEC-004,REQ-DEV-SEC-005,REQ-DEV-SEC-006,REQ-DEV-SEC-007,REQ-DEV-SEC-008,REQ-DEV-SEC-009,REQ-DEV-SEC-010,REQ-DEV-SEC-011,REQ-DEV-SEC-012,REQ-DEV-SEC-013,REQ-DEV-SEC-014,REQ-DEV-SEC-015,REQ-DEV-SEC-016,REQ-DEV-SEC-017,REQ-DEV-SEC-018,REQ-DEV-SEC-019,REQ-DEV-SEC-020,REQ-DEV-SEC-021,REQ-DEV-SEC-022,REQ-DEV-SEC-023,REQ-DEV-SEC-024,REQ-DEV-SEC-025,REQ-DEV-SEC-026,REQ-DEV-SEC-027,REQ-DEV-SEC-028,REQ-DEV-SEC-029,REQ-DEV-SEC-030,REQ-DEV-SEC-031,REQ-DEV-SEC-032,REQ-DEV-SEC-033,REQ-DEV-SEC-034,REQ-DEV-SEC-035,REQ-DEV-SEC-036,REQ-DEV-SEC-037,REQ-DEV-SEC-038,REQ-DEV-SEC-039,REQ-DEV-SEC-040,REQ-DEV-SEC-041,REQ-DEV-SEC-042,REQ-DEV-SEC-043,REQ-DEV-SEC-044,REQ-DEV-SEC-045,REQ-DEV-SEC-046,REQ-DEV-SEC-047,REQ-DEV-SEC-048
renderer=requirements-list-v1
-->
- **REQ-DEV-SEC-001 — SHALL:** Development security preserve explicit authority, least privilege, workspace isolation, component data ownership, and safe degradation.
- **REQ-DEV-SEC-002 — SHALL:** Every development operation execute under an identified actor, workspace, profile, component scope, and declared toolchain.
- **REQ-DEV-SEC-003 — SHALL NOT:** Developer convenience, local administrator access, container access, or repository access be treated as authority over production, governance, publication, signing, or another component's data.
- **REQ-DEV-SEC-004 — SHALL:** Ordinary development run without host-wide administrative or root privilege.
- **REQ-DEV-SEC-005 — SHALL:** A sensitive host mutation use the profile-approved narrow privileged path and an applicable policy decision before execution.
- **REQ-DEV-SEC-006 — SHALL NOT:** A development process, editor extension, build script, container, or AI tool receive unrestricted host privilege by default.
- **REQ-DEV-SEC-007 — SHALL:** Privileged development actions be bounded, attributable, observable, and reversible or recoverable.
- **REQ-DEV-SEC-008 — SHALL:** Every development secret, key, token, credential, and certificate have an owner, purpose, scope, storage mechanism, rotation rule, revocation rule, and expiry where applicable.
- **REQ-DEV-SEC-009 — SHALL NOT:** Secrets be committed to source control, embedded in images, placed in shared mutable caches, written to general logs, or passed through broadly visible process arguments.
- **REQ-DEV-SEC-010 — SHALL:** Development secrets remain scoped to the workspace, component, environment, and capability that require them.
- **REQ-DEV-SEC-011 — SHALL NOT:** Production signing keys, production root credentials, production recovery keys, or unrestricted production service credentials be stored on ordinary developer workstations.
- **REQ-DEV-SEC-012 — SHALL:** Development, test, staging, and production identities and cryptographic keys remain distinct.
- **REQ-DEV-SEC-013 — SHALL:** Secret detection run before source, artifact, log, or diagnostic material is shared outside its authorized boundary.
- **REQ-DEV-SEC-014 — SHALL:** Dependencies be declared through the applicable toolchain contract and resolved from versioned lock state for reproducible validation.
- **REQ-DEV-SEC-015 — SHALL:** Dependency sources, packages, container images, and tool downloads be verified using their applicable integrity, signature, provenance, or trusted-source controls.
- **REQ-DEV-SEC-016 — SHALL NOT:** An unpinned mutable tag, unreviewed install script, or undeclared package source be treated as a reproducible release input.
- **REQ-DEV-SEC-017 — SHALL:** Dependency updates be explicit changes with diff review, impact analysis, vulnerability review, and applicable tests.
- **REQ-DEV-SEC-018 — SHALL:** Known dependency or toolchain vulnerabilities be dispositioned through remediation, bounded mitigation, rejection, or an active exception with owner and expiry.
- **REQ-DEV-SEC-019 — SHALL NOT:** A vulnerability exception silently apply to another workspace, profile, release, artifact, dependency version, or cloned environment.
- **REQ-DEV-SEC-020 — SHALL:** Build and test execution treat repository code, dependency hooks, generators, fixtures, plugins, extensions, and imported artifacts as potentially untrusted execution.
- **REQ-DEV-SEC-021 — SHALL:** Untrusted or newly introduced build-time execution run within the profile-approved isolation and resource envelope.
- **REQ-DEV-SEC-022 — SHALL NOT:** A build or test process access unrelated workspace secrets, user credentials, host sockets, authoritative databases, or external networks unless the test contract explicitly requires and authorizes that access.
- **REQ-DEV-SEC-023 — SHALL:** Containerized development prefer rootless execution and the least required capabilities.
- **REQ-DEV-SEC-024 — SHALL NOT:** A development container mount a host container-control socket, unrestricted home directory, device set, credential store, or sensitive host path without an explicit bounded requirement and active exception or profile authority.
- **REQ-DEV-SEC-025 — SHALL:** Container images used as reproducible build or test inputs resolve to immutable digests or an equivalent verified immutable identity.
- **REQ-DEV-SEC-026 — SHALL:** Local services bind only to interfaces required by their workspace contract and remain inaccessible outside the intended boundary by default.
- **REQ-DEV-SEC-027 — SHALL:** Ports, networks, sockets, databases, queues, volumes, process names, secrets, and credentials remain workspace-scoped and collision-free.
- **REQ-DEV-SEC-028 — SHALL NOT:** A shared infrastructure process create shared authoritative data ownership or unrestricted cross-workspace access.
- **REQ-DEV-SEC-029 — SHALL:** Development and test data be synthetic, generated, minimized, or de-identified by default.
- **REQ-DEV-SEC-030 — SHALL NOT:** Production personal, tenant, cultural, security-sensitive, or operational data be copied into a development workspace without explicit purpose, minimization, approval, controls, retention, and deletion behavior.
- **REQ-DEV-SEC-031 — SHALL:** Fixtures, snapshots, logs, crash dumps, database exports, screenshots, and diagnostic bundles be classified and sanitized before retention or sharing.
- **REQ-DEV-SEC-032 — SHALL:** Development telemetry and logs exclude secrets and minimize user, tenant, cultural, and application-content data.
- **REQ-DEV-SEC-033 — SHALL:** External integrations and AI surfaces receive only explicitly selected, permitted, minimum necessary development context.
- **REQ-DEV-SEC-034 — SHALL NOT:** Source repositories, unrestricted workspaces, secrets, private keys, production data, or unrelated component context be sent wholesale to an external AI surface.
- **REQ-DEV-SEC-035 — SHALL:** AI-generated code, tests, documentation, configuration, queries, migrations, media, and policy remain candidate inputs and pass normal review, validation, provenance, and activation controls.
- **REQ-DEV-SEC-036 — SHALL NOT:** An AI tool, editor extension, or external integration approve its own generated change, bypass branch or review policy, execute privileged mutations, or activate an artifact.
- **REQ-DEV-SEC-037 — SHALL:** Development outputs intended for promotion include applicable tests, SBOM, provenance, dependency identity, toolchain identity, source revision, and build-environment evidence.
- **REQ-DEV-SEC-038 — SHALL:** Artifact signatures, digests, and provenance receipts be used where required by the artifact class and release workflow.
- **REQ-DEV-SEC-039 — SHALL NOT:** Local build success, a local signature, or developer approval grant production artifact, release, policy, publication, or conformance authority.
- **REQ-DEV-SEC-040 — SHALL:** Production promotion use separate build, signing, evidence, artifact-admission, Release Set, and activation authorities.
- **REQ-DEV-SEC-041 — SHALL:** Security-relevant development events and critical transitions emit structured evidence or receipts according to applicable policy without indiscriminate monitoring.
- **REQ-DEV-SEC-042 — SHALL:** A suspected secret exposure, dependency compromise, malicious extension, unauthorized privilege use, or corrupted development artifact trigger containment, credential revocation, evidence preservation, scope analysis, and controlled recovery.
- **REQ-DEV-SEC-043 — SHALL:** Development security failure degrade or block only affected capabilities while preserving unrelated verified workspaces and authoritative state.
- **REQ-DEV-SEC-044 — SHALL:** Recovery revalidate actor identity, profile, workspace, source revision, dependency lock, secrets, services, data ownership, resource controls, artifacts, queued work, and evidence before unrestricted execution resumes.
- **REQ-DEV-SEC-045 — SHALL:** Security controls remain enforceable during disconnected development for admitted source, dependencies, tools, identities, and artifacts.
- **REQ-DEV-SEC-046 — SHALL NOT:** Internet unavailability justify disabling integrity checks, secret isolation, provenance, least privilege, or component ownership controls.
- **REQ-DEV-SEC-047 — SHALL:** Profile-specific operating-system, sandbox, container, virtualization, firewall, key-store, endpoint-protection, or service-manager mechanisms remain scoped to the profile that adopts them.
- **REQ-DEV-SEC-048 — SHALL:** Development security conformance test least privilege, secret handling, dependency integrity, untrusted execution isolation, data minimization, AI boundaries, artifact provenance, independent workspace failure, incident containment, and prohibited side effects.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Secure workspace activation

Workspace activation follows:

1. resolve the actor, profile, workspace, component, and toolchain;
2. validate workspace identity and isolation declarations;
3. verify source origin and revision;
4. resolve dependency lock state and trusted package sources;
5. allocate ports, networks, services, data, secrets, and resource controls;
6. scan source and configuration for exposed secrets;
7. verify that production credentials and keys are absent;
8. apply least-privilege and network boundaries;
9. start declared services;
10. run health, isolation, and security checks;
11. mark the workspace active only after every required check passes.

### 6.2 Introduce or update a dependency

A dependency change follows:

1. identify the business and technical purpose;
2. verify the source and maintainership context;
3. review license and policy compatibility where applicable;
4. update declarations;
5. regenerate the lock state;
6. inspect direct and transitive changes;
7. resolve integrity and provenance information;
8. evaluate known vulnerabilities;
9. run applicable tests and impact analysis;
10. record remediation or exception disposition;
11. commit declarations and lock state together.

A dependency is not approved because it installs successfully.

### 6.3 Execute untrusted build or test code

Before execution:

1. classify the code or hook;
2. select the profile-approved isolation;
3. exclude unrelated secrets and data;
4. restrict network access to declared needs;
5. restrict writable paths and host interfaces;
6. apply Resource Governor limits;
7. run the operation;
8. capture bounded diagnostics;
9. verify outputs before import;
10. destroy or reset disposable execution state.

### 6.4 Use a development secret

Secret use follows:

1. resolve the actor, workspace, capability, and secret reference;
2. verify purpose and scope;
3. obtain the secret through the approved store or broker;
4. expose it only to the intended process or interface;
5. avoid command-line, log, source, image, and cache persistence;
6. revoke or release temporary access;
7. rotate or revoke after suspected exposure;
8. emit required evidence without recording the secret value.

### 6.5 Use sensitive test data

Before sensitive data enters development:

1. show that synthetic or de-identified data is insufficient;
2. identify exact fields and records required;
3. resolve owner, purpose, approval, and policy;
4. minimize and transform the data;
5. select authorized workspaces and actors;
6. define retention and deletion;
7. prevent external integration and AI transfer unless separately permitted;
8. audit access according to policy;
9. verify deletion at expiry or completion.

### 6.6 Use an external AI or integration

The request follows:

1. explicit user action;
2. declared integration capability;
3. context selection;
4. secret and sensitive-data screening;
5. disclosure, consent, and cultural-rights evaluation where applicable;
6. minimum-context transfer;
7. untrusted-result validation;
8. human or component review;
9. import through the owning repository or component interface;
10. provenance recording.

### 6.7 Produce a candidate artifact

Candidate production follows:

```text
clean source revision
→ locked dependencies
→ declared toolchain
→ isolated build
→ tests and validation
→ SBOM
→ provenance
→ candidate integrity material
→ evidence bundle
→ candidate publication to the development boundary
```

The candidate remains inactive until downstream authorities complete admission and release procedures.

### 6.8 Respond to a development-security incident

Incident response follows:

1. stop or isolate affected capabilities;
2. preserve bounded evidence;
3. revoke exposed credentials and tokens;
4. suspend affected workspaces, integrations, dependencies, or artifacts;
5. identify affected source revisions, caches, builds, and outputs;
6. determine component, profile, and release exposure;
7. remove or replace compromised inputs;
8. rebuild from verified source and lock state;
9. revalidate workspaces and artifacts;
10. document remediation and residual risk;
11. restore capabilities through the global `restoring` state.

## 7. Failure States and Safe Degradation

| Failure condition | Required response | Preserved behavior |
| --- | --- | --- |
| Actor identity unresolved | Block privileged, secret, or sensitive-data action | Non-sensitive local inspection permitted by existing authority |
| Privileged broker unavailable | Block sensitive host mutation | Unprivileged workspace operation |
| Secret store unavailable | Block dependent capability | Work not requiring that secret |
| Suspected secret exposure | Revoke and isolate | Unaffected workspaces and credentials |
| Secret scan fails | Block sharing or candidate promotion | Local remediation |
| Dependency integrity unresolved | Block synchronization, build, or candidate promotion | Existing verified environments |
| Vulnerability disposition missing | Block promotion; local use only when a declared bounded policy permits | Unaffected dependencies |
| Package source unavailable | Use admitted verified cache or block affected resolution | Existing frozen environments |
| Untrusted build isolation unavailable | Block execution | Source review and unrelated work |
| Container runtime unavailable | Block container-dependent capability | Native tools and independent work |
| Rootless or bounded execution unavailable | Block risky container execution unless an explicit approved profile path exists | Low-risk non-container work |
| Sensitive data approval unresolved | Block data import | Synthetic and de-identified workflows |
| External AI unavailable | Disable AI-assisted capability | Deterministic local development |
| Internet unavailable | Use admitted source, dependencies, tools, and artifacts | Offline development envelope |
| SBOM or provenance generation fails | Block candidate promotion requiring that evidence | Source and local diagnostics |
| Signing authority unavailable | Keep artifact unsigned or development-signed according to its class; block production promotion | Candidate artifact |
| Audit receipt persistence unavailable | Keep receipt-before-commit security transition uncommitted | Previous authoritative state |
| Resource pressure | Throttle, queue, suspend, or reject untrusted or heavy work | Required host and workspace capabilities |
| Workspace compromise suspected | Suspend and isolate the workspace | Other verified workspaces |
| Shared cache compromise suspected | Quarantine and rebuild cache from verified inputs | Installed verified workspace environments |
| Candidate artifact verification fails | Reject and quarantine candidate | Source and previous admitted artifacts |
| Recovery evidence incomplete | Remain `restoring` or `blocked` | Last verified state |

Safe degradation does not disable integrity checks, expose secrets, grant privilege, share mutable state, or promote unverifiable output.

## 8. Cross-Component Interactions

### 8.1 Identity and Trust

Identity and Trust supplies actor, service, device, certificate, and session results.

Development tools consume those results. They do not issue production identities or trust roots.

### 8.2 Governance Policy Runtime

Governance Policy Runtime decides sensitive privilege, secret access, data disclosure, exceptional network access, and bounded security exceptions where required.

A development tool cannot infer approval from local administrator access.

### 8.3 Resource Governor

Resource Governor constrains builds, tests, containers, scanners, dependency resolution, model tools, databases, and background workers.

Resource capacity is not permission to run an unauthorized operation.

### 8.4 Audit Broker

Audit Broker receives required receipts and security evidence.

It does not indiscriminately capture source, prompts, payloads, secrets, or test data.

### 8.5 Component runtimes and data owners

Component contracts define development interfaces and data ownership.

A developer workspace accesses component state only through declared development interfaces, migrations, fixtures, or explicitly authorized maintenance procedures.

### 8.6 Build Farm

Build Farm receives admitted source, lock state, toolchains, and build policy.

It produces reproducible candidate artifacts and evidence in clean workers. It does not trust mutable workstation state as a release input without declared transfer and verification.

### 8.7 Signing and release authorities

Signing and release authorities verify candidate identity, evidence, artifact class, compatibility, and authorization.

Development keys and local success do not substitute for production authority.

### 8.8 External integrations

Each integration declares authentication, data classes, retention, deletion, failure, and removal behavior.

Removal of an optional integration preserves local source, export, backup, restore, and credible exit.

## 9. Decision Closure and Prohibited Assumptions

The following decisions are closed:

- development uses least privilege;
- sensitive host mutations use a narrow authorized path;
- production keys and unrestricted production credentials are excluded from ordinary developer workstations;
- development identities and keys are distinct from production;
- dependencies use declared sources and versioned lock state;
- reproducible images use immutable identities;
- build and test code is potentially untrusted;
- rootless containers are preferred where supported;
- workspace services and data remain isolated;
- synthetic or minimized test data is preferred;
- external AI receives minimum selected context;
- AI output remains candidate input;
- SBOM, provenance, and integrity material accompany promoted candidates where required;
- local success does not grant production authority;
- security incidents trigger containment, revocation, evidence, rebuild, and controlled recovery;
- profile-specific security mechanisms do not become universal requirements.

Prohibited assumptions include:

- treating local root or administrator access as production authority;
- storing production signing keys in a workspace;
- committing a `.env` file containing secrets;
- trusting an install command because it appears in upstream documentation;
- using an unpinned image tag as a reproducible build input;
- mounting a host container socket for convenience;
- giving an editor extension access to every repository and secret;
- copying production databases into development by default;
- sending a repository or workspace wholesale to an AI provider;
- executing AI-generated commands without review;
- accepting a dependency because vulnerability scanning is temporarily unavailable;
- marking an artifact releasable because it has a digest;
- allowing a local developer signature to replace release signing authority;
- allowing a security exception to propagate to cloned workspaces or newer dependency versions;
- disabling checks because the workstation is offline;
- interpreting a clean scan as proof that code is safe;
- interpreting encryption as permission to disclose data.

## 10. Validation Criteria

Development security validates when:

1. all actors, workspaces, profiles, toolchains, components, and artifacts resolve;
2. ordinary development runs without host-wide privilege;
3. privileged operations use the active profile's bounded path;
4. production keys and unrestricted production credentials are absent;
5. secret scanning finds no active secret exposure;
6. secret values are absent from source, images, logs, caches, and broad process arguments;
7. development, staging, and production identities remain distinct;
8. dependency declarations and lock state are versioned and reproducible;
9. dependency sources and integrity controls resolve;
10. vulnerability findings have explicit dispositions;
11. active exceptions identify exact scope, owner, risk, mitigation, and expiry;
12. untrusted build and test code cannot access unrelated secrets or data;
13. container execution uses least capability and explicit mounts;
14. reproducible container inputs use immutable identities;
15. local services are not unintentionally exposed beyond workspace boundaries;
16. workspace ports, networks, data, queues, volumes, secrets, and processes remain isolated;
17. test data follows minimization, approval, retention, and deletion rules;
18. logs, fixtures, dumps, screenshots, and diagnostics are sanitized;
19. external integrations and AI receive only permitted minimum context;
20. AI-generated changes pass normal review and validation;
21. candidate artifacts contain required tests, SBOM, provenance, and integrity evidence;
22. local builds and signatures cannot activate production artifacts;
23. build, signing, artifact-admission, release, and activation authorities remain separate;
24. security events produce required selective evidence and receipts;
25. incident exercises verify containment, revocation, rebuild, and recovery;
26. disconnected validation preserves security controls;
27. profile-specific mechanisms remain profile-scoped;
28. failure of one workspace does not compromise another;
29. no unresolved marker, placeholder, duplicate owner, or non-intrinsic documentation hash appears;
30. `CHECK-DEV-001`, applicable security checks, and Interfile Alignment Locks pass.

Applicable checks include:

```bash
python docs/tools/check_ai_boundary.py
python docs/tools/check_component_boundaries.py
python docs/tools/check_canonical_ownership.py
python docs/tools/check_profile_composition.py
python docs/tools/check_interfile_locks.py
python docs/tools/check_traceability.py
python docs/tools/validate_docs.py
```

## 11. Non-Normative Examples

### 11.1 Local database credentials

A workspace starts PostgreSQL with workspace-specific credentials stored in the approved local secret store.

The credential does not appear in source, the container image, the workspace declaration, or process arguments.

### 11.2 Dependency update

A developer adds a library.

The package source is verified, `uv.lock` changes are reviewed, vulnerabilities are dispositioned, tests pass, and the project plus lock state are committed together.

### 11.3 Untrusted repository hook

A newly cloned repository contains an automatic setup hook.

The hook is reviewed and executed only inside a bounded workspace without unrelated secrets, unrestricted host mounts, or undeclared network access.

### 11.4 AI-generated migration

An external AI surface proposes a database migration.

The migration remains a candidate. It is reviewed against the component's ownership and migration rules, tested on disposable fixtures, and cannot access production credentials or activate itself.

### 11.5 Sensitive diagnostic bundle

A crash bundle contains paths, logs, and a test database snapshot.

Before external sharing, the bundle is classified, secrets are removed, sensitive records are minimized, and the destination and retention policy are approved.

### 11.6 Candidate image

A local build produces a container image identified by an immutable digest, with an SBOM and provenance.

The image remains a development candidate. Build Farm, signing authority, artifact admission, Release Set compatibility, and activation still apply.

### 11.7 Offline development

The Internet is unavailable.

A workspace uses admitted source, locked dependencies, verified cached packages, local tests, and local secret stores. Integrity and isolation checks remain active; unresolved new downloads are blocked.
