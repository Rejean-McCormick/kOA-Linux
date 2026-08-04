<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-DEV-009",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "development",
  "scope": [
    "developer_linux_workstation",
    "developer_windows_wsl"
  ],
  "canonical_refs": [
    "generated/decision-index.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/profiles/developer-linux-workstation.profile.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "contracts/toolchains/python-uv.toolchain.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "contracts/artifact-contracts/developer-workspace.schema.json"
  ],
  "decision_ids": [
    "DEC-DEV-001",
    "DEC-DEV-002",
    "DEC-DATA-001",
    "DEC-PROFILE-001"
  ],
  "requirement_ids": [
    "REQ-DEV-IDENT-001",
    "REQ-DEV-IDENT-002",
    "REQ-DEV-IDENT-003",
    "REQ-DEV-IDENT-004",
    "REQ-DEV-IDENT-005",
    "REQ-DEV-IDENT-006",
    "REQ-DEV-IDENT-007",
    "REQ-DEV-IDENT-008",
    "REQ-DEV-IDENT-009",
    "REQ-DEV-IDENT-010",
    "REQ-DEV-IDENT-011",
    "REQ-DEV-IDENT-012",
    "REQ-DEV-IDENT-013",
    "REQ-DEV-IDENT-014",
    "REQ-DEV-IDENT-015",
    "REQ-DEV-IDENT-016",
    "REQ-DEV-IDENT-017",
    "REQ-DEV-IDENT-018",
    "REQ-DEV-IDENT-019",
    "REQ-DEV-IDENT-020",
    "REQ-DEV-IDENT-021",
    "REQ-DEV-IDENT-022",
    "REQ-DEV-IDENT-023",
    "REQ-DEV-IDENT-024"
  ],
  "lock_ids": [
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DATA-001",
    "LOCK-PROFILE-001",
    "LOCK-IMPL-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-009",
    "DOC-GOV-010",
    "DOC-CONST-002",
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-007",
    "DOC-SYS-014",
    "DOC-PROFILE-001",
    "DOC-COMP-000",
    "DOC-DEV-000",
    "DOC-DEV-001",
    "DOC-DEV-002",
    "DOC-DEV-003",
    "DOC-DEV-004",
    "DOC-DEV-005",
    "DOC-DEV-006",
    "DOC-DEV-007",
    "DOC-DEV-008"
  ],
  "tags": [
    "development",
    "workspace-isolation",
    "secrets",
    "local-identities",
    "service-identities",
    "local-certificates",
    "credential-hygiene",
    "parallel-workspaces"
  ]
}
KOA:DOC-META:END -->

# Secrets and Local Identities

## 1. Purpose

This document defines development handling for workspace-scoped secrets and local identities.

Each development workspace has a stable `workspace_id`. That identity namespaces credentials, service identities, database identities, generated local certificates, trust material, and secret-bearing temporary state so that applications, branches, and worktrees can run in parallel without credential collision or unintended authority sharing.

The model keeps sensitive values outside version-controlled content while preserving deterministic naming, reproducible setup, bounded authority, and complete cleanup.

## 2. Scope

This document applies to:

- `developer_linux_workstation`;
- `developer_windows_wsl`;
- repositories, branches, worktrees, and temporary development workspaces;
- local component and service identities;
- database users and passwords;
- queue, broker, cache, and search-service credentials;
- local API keys, client identities, tokens, and session credentials;
- generated local certificates, private keys, and trust roots;
- secret injection into processes, containers, tests, and development services;
- secret references in configuration;
- logs, diagnostics, tests, generated output, images, and artifacts that could expose sensitive values;
- creation, rotation, revocation, and workspace cleanup;
- parallel workspace isolation and validation.

This document does not:

- define production or sovereign secret storage;
- define release-signing or artifact-signing keys;
- authorize reuse of user or production credentials;
- prescribe one secret manager, operating-system keyring, container runtime, file format, or certificate tool;
- own component-specific secret requirements;
- make an implementation recipe canonical;
- permit secret values in documentation or examples.

The applicable profile, component, integration, and workspace contracts remain the owners of required secret names, consumer scopes, privileges, and identity relationships.

## 3. Canonical References

| Canonical reference | Ownership role |
| --- | --- |
| `contracts/profiles/developer-linux-workstation.profile.json` | Owns Linux development-profile membership, isolation, and profile-scoped controls. |
| `contracts/profiles/developer-windows-wsl.profile.json` | Owns Windows/WSL development-profile membership, isolation, and profile-scoped controls. |
| `contracts/artifact-contracts/developer-workspace.schema.json` | Defines the machine-readable workspace identity and declared local-resource relationships. |
| `generated/component-catalog.json` | Owns component identities and high-level data and authority boundaries. |
| `contracts/components/*.component.json` | Owns component-specific required identities, accepted secret references, and permitted operations. |
| `contracts/integration-types.contract.json` | Owns integration identities, transfer boundaries, and integration-specific credential requirements. |
| `contracts/toolchains/python-uv.toolchain.json` | Owns Python dependency behavior but does not own infrastructure secrets or service identities. |
| `generated/requirements-index.json` | Owns the normative statements displayed in Section 5. |
| `generated/assertion-index.json` | Owns workspace state, collision, data-authority, profile-scope, and implementation-boundary assertions. |
| `generated/traceability.json` | Owns decision, requirement, lock, test, and evidence relationships. |
| `generated/test-catalog.json` and `generated/evidence-catalog.json` | Own validation-test and evidence identities. |

This document explains the development model. It does not store secret values or redefine component and profile contracts.

## 4. Model and Responsibilities

### 4.1 Workspace identity

Every active workspace has one stable `workspace_id`.

That identifier namespaces or deterministically resolves:

- secret namespace;
- component service identities;
- database identities;
- queue and broker identities;
- local API clients;
- generated certificate subjects;
- generated local trust roots;
- secret-bearing temporary directories;
- process and container secret mounts;
- test identities;
- cleanup records.

A workspace can be moved on disk without changing its logical identity. An absolute developer path is not the canonical identity.

### 4.2 Secret and identity classes

| Class | Examples | Canonical owner |
| --- | --- | --- |
| Secret declaration | Required key name, type, consumer, purpose | Component, integration, profile, or workspace contract |
| Secret value | Password, token, API key, symmetric key | Workspace-scoped secret store or injection mechanism |
| Service identity | Local component, worker, queue, or API client identity | Workspace declaration plus owning component contract |
| Database identity | Component-specific local database user or role | Workspace and database-development contract |
| Local certificate | Development TLS or mutual-authentication certificate | Workspace or explicit shared development trust domain |
| Local trust root | Development-only certificate authority or trust anchor | Workspace or explicit shared development trust domain |
| Personal developer identity | Developer account or local interactive identity | External to component service authority |
| Production identity | Production, sovereign, release, publication, or governance credential | Production authority; excluded from development reuse |
| Secret reference | Non-sensitive lookup name or identifier | Versioned or generated configuration where permitted |
| Secret-bearing temporary state | Rendered file, socket credential, token cache | Workspace-scoped runtime state |

### 4.3 Naming

Local identity names are deterministic and collision-resistant.

A canonical local name is derived from:

```text
workspace_id + component_or_service_id + identity_purpose
```

A platform-specific representation can shorten or encode that name while retaining a reversible mapping in workspace state.

Secret values are not used as names. Repository paths, branch names alone, usernames alone, and fixed global service names are insufficient isolation identifiers.

### 4.4 Storage and injection

The model distinguishes:

- non-sensitive declaration;
- sensitive value storage;
- execution-time injection;
- temporary runtime representation.

Version-controlled files can declare required secret names and lookup references. Sensitive values remain in a workspace-scoped store, protected local file, operating-system facility, container secret mechanism, or equivalent profile-supported mechanism.

Injection provides each service only its declared values. The mechanism does not expose the complete workspace namespace to every process.

### 4.5 Local service identities

A local component identity has:

- workspace scope;
- component or service identity;
- purpose;
- permitted resources and operations;
- credential form;
- creation owner;
- rotation and revocation behavior;
- cleanup behavior;
- validation evidence.

Administrative convenience does not grant one service the identities of another component. Shared database servers, queues, containers, hosts, or process supervisors do not create shared semantic authority.

### 4.6 Local certificates and trust

Generated development certificates are local trust artifacts.

They identify:

- workspace or declared development trust domain;
- subject service;
- permitted usage;
- validity period;
- issuer;
- revocation or replacement method.

Development trust roots do not establish production, release, publication, governance, or user trust. A local certificate can secure a development connection without supporting a production conformance claim.

### 4.7 Personal and machine identities

A developer's interactive identity can authorize creation or access to local workspace material. It does not become the component service identity exposed to another component.

Host administrator or container-runtime access is custody or platform authority. It does not grant component data ownership or justify sharing credentials between workspaces.

### 4.8 Shared development dependencies

A credential or trust domain can be shared only when sharing is an explicit property of an active development contract.

The declaration identifies:

- shared scope;
- allowed workspaces and consumers;
- authority retained by the shared service;
- privileges;
- owner;
- rotation and revocation;
- outage behavior;
- cleanup behavior;
- tests and evidence.

A content-addressed dependency download cache can be shared without sharing an installed environment or application secret namespace.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-DEV-IDENT-001,REQ-DEV-IDENT-002,REQ-DEV-IDENT-003,REQ-DEV-IDENT-004,REQ-DEV-IDENT-005,REQ-DEV-IDENT-006,REQ-DEV-IDENT-007,REQ-DEV-IDENT-008,REQ-DEV-IDENT-009,REQ-DEV-IDENT-010,REQ-DEV-IDENT-011,REQ-DEV-IDENT-012,REQ-DEV-IDENT-013,REQ-DEV-IDENT-014,REQ-DEV-IDENT-015,REQ-DEV-IDENT-016,REQ-DEV-IDENT-017,REQ-DEV-IDENT-018,REQ-DEV-IDENT-019,REQ-DEV-IDENT-020,REQ-DEV-IDENT-021,REQ-DEV-IDENT-022,REQ-DEV-IDENT-023,REQ-DEV-IDENT-024 -->
- **REQ-DEV-IDENT-001 — SHALL:** Every active development workspace has one secret namespace derived from its stable workspace_id.
- **REQ-DEV-IDENT-002 — SHALL:** Every local service, database, queue, gateway, and component process that requires an identity uses a workspace-scoped identity distinct from equivalent services in other workspaces.
- **REQ-DEV-IDENT-003 — SHALL NOT:** Two development workspaces share a mutable secret namespace, service credential, database credential, private key, client identity, or generated local certificate by default.
- **REQ-DEV-IDENT-004 — SHALL:** Workspace-scoped identity names include or deterministically resolve from the workspace_id.
- **REQ-DEV-IDENT-005 — SHALL:** Secret values, private keys, access tokens, passwords, and credential-bearing configuration remain outside version-controlled repository content.
- **REQ-DEV-IDENT-006 — SHALL NOT:** A committed example, fixture, generated document, log, receipt, test snapshot, container image, or build artifact contains an active secret value.
- **REQ-DEV-IDENT-007 — SHALL:** Version-controlled configuration contains secret names, required fields, lookup references, or non-sensitive examples rather than active secret values.
- **REQ-DEV-IDENT-008 — SHALL NOT:** Production, sovereign, release-signing, governance, publication, or user credentials are reused as development credentials.
- **REQ-DEV-IDENT-009 — SHALL:** Local credentials have the minimum privileges, resources, operations, and lifetime required for the workspace task.
- **REQ-DEV-IDENT-010 — SHALL:** Local database identities are distinct by workspace and component and do not grant direct write access to another component's authoritative development state.
- **REQ-DEV-IDENT-011 — SHALL:** Generated local certificates and trust roots are scoped to the workspace or an explicitly declared development trust domain.
- **REQ-DEV-IDENT-012 — SHALL NOT:** A local development trust root, certificate, private key, or service identity is represented as production trust or release authority.
- **REQ-DEV-IDENT-013 — SHALL:** A service receives only the secrets and identities declared by its active component, integration, profile, and workspace contracts.
- **REQ-DEV-IDENT-014 — SHALL NOT:** A general-purpose environment file or process environment silently grants every local service access to every workspace secret.
- **REQ-DEV-IDENT-015 — SHALL:** Secret injection occurs at execution or service-start time through a workspace-scoped mechanism that does not copy the value into source files or generated documentation.
- **REQ-DEV-IDENT-016 — SHALL:** Logs, command output, traces, error reports, receipts, diagnostics, and test results redact credential values and sensitive identity material.
- **REQ-DEV-IDENT-017 — SHALL:** Secret creation, replacement, rotation, revocation, and cleanup preserve the workspace identity and do not mutate another workspace.
- **REQ-DEV-IDENT-018 — SHALL:** Workspace removal revokes or removes its local credentials, private keys, generated certificates, identity records, and secret-bearing temporary files without affecting another workspace.
- **REQ-DEV-IDENT-019 — SHALL:** A shared development credential or trust domain exists only when an active contract declares the shared scope, consumers, privileges, rotation owner, revocation behavior, and validation evidence.
- **REQ-DEV-IDENT-020 — SHALL:** Missing, unreadable, expired, revoked, ambiguous, or incorrectly scoped credentials block the affected operation without substituting another workspace or production identity.
- **REQ-DEV-IDENT-021 — SHALL:** Local identity and secret handling remains reproducible from non-sensitive declarations and setup procedures without requiring committed secret values.
- **REQ-DEV-IDENT-022 — SHALL:** Tests use workspace-scoped test identities and disposable secret material rather than developer-personal or production credentials.
- **REQ-DEV-IDENT-023 — SHALL:** Validation detects committed credential material, secret-namespace collisions, identity collisions, excessive permissions, unredacted output, unresolved secret references, and incomplete cleanup.
- **REQ-DEV-IDENT-024 — SHALL:** Every active development secret and local-identity requirement is traceable to accepted decisions, applicable locks, validation tests, and required evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Creating a workspace secret namespace

Workspace initialization:

1. resolves the stable `workspace_id`;
2. resolves active profile and component contracts;
3. lists required secret declarations and local identities;
4. creates the workspace secret namespace;
5. creates component-scoped service and database identities;
6. generates local certificates only when declared;
7. assigns minimum privileges and validity;
8. writes only non-sensitive references into workspace configuration;
9. validates collision freedom and access boundaries;
10. records non-sensitive setup evidence.

### 6.2 Starting a local service

Service startup:

1. resolves the workspace and service identities;
2. resolves declared secret references;
3. verifies value availability, scope, validity, and permissions;
4. prepares a service-specific injection view;
5. starts the service with only its permitted identities and values;
6. prevents values from entering command history, logs, or generated documentation;
7. records a redacted startup outcome.

A missing or invalid value leaves the affected service blocked.

### 6.3 Rotating or revoking a local credential

Rotation or revocation:

1. identifies the workspace, consumer, and credential purpose;
2. creates or selects the replacement when rotating;
3. updates the workspace-scoped secret store;
4. restarts or reloads only affected consumers;
5. verifies the previous credential no longer authorizes access;
6. removes obsolete temporary copies;
7. records non-sensitive evidence.

### 6.4 Running tests

A test environment:

1. creates disposable workspace-scoped identities;
2. provisions only required permissions;
3. injects test secret material at execution time;
4. redacts test output;
5. verifies expected access and denial behavior;
6. revokes and removes disposable values after the run;
7. confirms that cleanup did not affect another workspace.

### 6.5 Removing a workspace

Workspace cleanup:

1. stops workspace services and workers;
2. revokes local service and database credentials;
3. removes private keys, certificates, token caches, and secret-bearing temporary files;
4. removes workspace identity records and mounts;
5. verifies shared dependencies remain intact;
6. verifies another workspace remains operational;
7. records a redacted cleanup result.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Preserved state | Blocked or degraded behavior | Evidence |
| --- | --- | --- | --- | --- |
| Workspace identity is missing or ambiguous | Block secret provisioning and service startup | Existing valid workspaces | Affected workspace | Identity-resolution failure |
| Secret declaration is unresolved | Keep the consuming service blocked | Other services and workspaces | Dependent capability | Reference-resolution failure |
| Credential is missing, expired, or revoked | Reject authentication | Existing unrelated authority | Affected operation | Authentication failure |
| Credential scope is incorrect | Reject access without broader substitution | Correctly scoped identities | Mis-scoped operation | Scope-validation outcome |
| Secret namespace collides | Block workspace activation | Existing workspace namespaces | Conflicting workspace | Collision report |
| Local certificate is invalid | Reject the protected connection | Other valid local connections | Affected endpoint | Certificate-validation outcome |
| Production credential is detected | Quarantine the value and block its use | Local development identities | Affected setup or test | Credential-classification incident |
| Active secret appears in repository content | Fail validation and require revocation when exposure is credible | Unaffected credentials | Merge, publication, or release | Secret-scan evidence |
| Redaction fails | Restrict the output and treat exposure according to the incident procedure | Source service state | Distribution of affected output | Redaction failure |
| Secret store or injection mechanism is unavailable | Keep affected services stopped or degraded | Services not requiring the unavailable values | Secret-dependent services | Secret-service health record |
| Rotation partially succeeds | Keep the transition blocked or restore the last valid credential state | Last verified credential state | Ambiguous mixed credential state | Rotation outcome |
| Cleanup is incomplete | Mark the workspace cleanup nonconformant and continue targeted removal | Other workspaces | Reuse of the workspace identity | Cleanup report |

## 8. Cross-Component Interactions

### 8.1 Components and services

Each component contract declares the identity and secret references required by its local services.

The workspace supplies scoped values and identities. It does not broaden the component's permissions or allow one component to use another component's database or service credential.

### 8.2 Databases, queues, and shared infrastructure

A shared local database server or broker can host several workspaces and components.

Isolation remains explicit through:

- workspace-scoped names;
- component-scoped users or roles;
- separate passwords or keys;
- separate databases, schemas, virtual hosts, or equivalent namespaces;
- access-control boundaries;
- cleanup ownership.

Infrastructure administration does not replace application ownership.

### 8.3 Containers and process supervisors

A container runtime or process supervisor can inject a service-specific secret view.

Container names, mounts, service units, generated environment, and local identities remain workspace-scoped. The runtime mechanism is an implementation choice unless an active profile adopts it.

### 8.4 Identity and trust services

A development workspace can interact with Identity and Trust through an active component contract.

Local test or development identities remain distinguishable from production identities and cannot make production trust claims.

### 8.5 External integrations

A local integration uses a workspace-specific development client or an explicitly approved shared development identity.

The integration contract declares transferred data, permitted operations, credential owner, revocation, and failure behavior. Developer-personal or production credentials are not an implicit substitute.

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Effect |
| --- | --- |
| `DEC-DEV-001` | Establishes one secret namespace, service namespace, database identity set, and other isolated resources per development workspace. |
| `DEC-DEV-002` | Requires applications and branches to run concurrently without mutable-state and identity collisions. |
| `DEC-DATA-001` | Preserves logical component data ownership even when development infrastructure is shared. |
| `DEC-PROFILE-001` | Keeps development isolation and implementation choices scoped to active development profiles. |

### Prohibited assumptions

- a branch name alone is a stable secret namespace;
- all local services can use one global development password;
- one database administrator credential is an acceptable application identity;
- a process environment is private merely because the process is local;
- a `.env` filename makes its contents safe or workspace-scoped;
- ignored files cannot leak or be copied into images and artifacts;
- test credentials can be production credentials because tests are temporary;
- a developer's personal identity is a component service identity;
- a local trust root establishes production trust;
- container isolation automatically scopes secrets;
- an administrator owns component data because the administrator can read it;
- a shared cache permits a shared application secret namespace;
- deleting the source tree removes every credential and generated certificate;
- a missing credential can be replaced with another workspace's value;
- redaction can be deferred until publication;
- an implementation recipe defines the canonical secret manager.

## 10. Validation Criteria

This document is conformant when:

1. `DOC-DEV-009` is active at `05-development/09-secrets-and-local-identities.md`.
2. Every canonical reference resolves.
3. Every listed decision exists with status `accepted`.
4. Every requirement in Section 5 exists with identical strength, statement, scope, owner, source decision, and validation mapping.
5. Every listed lock exists and is active.
6. Every active development workspace resolves one stable `workspace_id`.
7. Every workspace resolves one distinct secret namespace.
8. Service, database, queue, client, and certificate identities are collision-free across active workspaces.
9. Every secret consumer has a declared purpose and minimum permission set.
10. Version-controlled content contains declarations and references rather than active secret values.
11. Repository, generated-file, image, artifact, log, diagnostic, receipt, and test-output scans detect exposed credential material.
12. Production, sovereign, signing, publication, governance, and user credentials are absent from development use.
13. Database identities preserve component data ownership and prohibit cross-component direct writes.
14. Local certificate trust is distinguishable from production trust.
15. Each service receives only its declared secret view.
16. Missing or invalid credentials block only affected capabilities.
17. Rotation and revocation tests invalidate predecessor credentials.
18. Cleanup removes workspace credentials and secret-bearing temporary state without affecting another workspace.
19. Shared credentials or trust domains have an explicit active contract.
20. Test identities are workspace-scoped and disposable.
21. Validation output and evidence are redacted.
22. Setup remains reproducible from non-sensitive declarations.
23. Active prose is English and contains no unresolved-authority marker.
24. No normative keyword appears outside the generated requirement block.
25. The documentation dependency graph remains acyclic.

The validation entry point is:

```bash
python docs/tools/validate_docs.py
```

## 11. Non-Normative Examples

> **Non-normative example:** This example illustrates namespacing and does not prescribe one secret manager.

A workspace named `orgo-feature-voting-92cd` can provision a database identity derived from that workspace and the Orgo component identity. Another Orgo workspace receives a different database identity.

> **Non-normative example:** This example illustrates service-specific injection.

A local API process can receive its database password and signing test key without receiving the queue administrator credential used by a separate maintenance process.

> **Non-normative example:** This example illustrates local trust.

A workspace can generate a local certificate authority and certificates for its internal services. The authority is trusted only inside that declared development scope and is removed during workspace cleanup.

> **Non-normative example:** This example illustrates reproducible setup.

A repository can version a file listing required secret names and purposes. A setup procedure then creates random local values outside the repository and injects them into the workspace at runtime.

> **Non-normative example:** This example illustrates fail-closed identity handling.

When a required local integration token expires, the integration remains unavailable. The system does not substitute a token from another branch or a production account.
