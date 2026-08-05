<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SEC-001",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "security",
  "scope": [
    "global",
    "profile_conditioned_security"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-AI-001",
    "DEC-SENT-001",
    "DEC-MEDIATHEQUE-001",
    "DEC-UCKK-EXT-001",
    "DEC-ARI-001",
    "DEC-PROFILE-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-GATE-001",
    "DEC-CONTAINER-001",
    "DEC-K8S-001",
    "DEC-REL-001",
    "DEC-DOC-CHANGE-001"
  ],
  "requirement_ids": [
    "REQ-SEC-BASE-001",
    "REQ-SEC-BASE-002",
    "REQ-SEC-BASE-003",
    "REQ-SEC-BASE-004",
    "REQ-SEC-BASE-005",
    "REQ-SEC-BASE-006",
    "REQ-SEC-BASE-007",
    "REQ-SEC-BASE-008",
    "REQ-SEC-BASE-009",
    "REQ-SEC-BASE-010",
    "REQ-SEC-BASE-011",
    "REQ-SEC-BASE-012",
    "REQ-SEC-BASE-013",
    "REQ-SEC-BASE-014",
    "REQ-SEC-BASE-015",
    "REQ-SEC-BASE-016",
    "REQ-SEC-BASE-017",
    "REQ-SEC-BASE-018",
    "REQ-SEC-BASE-019",
    "REQ-SEC-BASE-020",
    "REQ-SEC-BASE-021",
    "REQ-SEC-BASE-022",
    "REQ-SEC-BASE-023",
    "REQ-SEC-BASE-024",
    "REQ-SEC-BASE-025",
    "REQ-SEC-BASE-026",
    "REQ-SEC-BASE-027",
    "REQ-SEC-BASE-028",
    "REQ-SEC-BASE-029",
    "REQ-SEC-BASE-030",
    "REQ-SEC-BASE-031",
    "REQ-SEC-BASE-032",
    "REQ-SEC-BASE-033",
    "REQ-SEC-BASE-034",
    "REQ-SEC-BASE-035",
    "REQ-SEC-BASE-036",
    "REQ-SEC-BASE-037",
    "REQ-SEC-BASE-038",
    "REQ-SEC-BASE-039",
    "REQ-SEC-BASE-040",
    "REQ-SEC-BASE-041",
    "REQ-SEC-BASE-042",
    "REQ-SEC-BASE-043",
    "REQ-SEC-BASE-044",
    "REQ-SEC-BASE-045",
    "REQ-SEC-BASE-046",
    "REQ-SEC-BASE-047",
    "REQ-SEC-BASE-048"
  ],
  "lock_ids": [
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SENT-001",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-MEDIATHEQUE-002",
    "LOCK-UCKK-EXT-001",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-PROFILE-001",
    "LOCK-DEV-001",
    "LOCK-DEV-002",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DEV-005",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-UCKK-EXT-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-CONST-011",
    "DOC-CONST-012",
    "DOC-SYS-002",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-007",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-010",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-016",
    "DOC-SYS-017",
    "DOC-SYS-019",
    "DOC-SYS-020",
    "DOC-SEC-000"
  ],
  "tags": [
    "security",
    "baseline",
    "identity",
    "trust",
    "least-privilege",
    "secrets",
    "network",
    "storage",
    "supply-chain",
    "external-ai",
    "audit",
    "offline",
    "recovery",
    "profile-conditioned"
  ]
}
KOA:DOC-META:END -->

# Security Baseline

## 1. Purpose

This document defines the minimum security properties of every active kOA deployment and the profile-conditioned controls that strengthen those properties.

The baseline protects:

- people, safety, due process, and recourse;
- component-owned authoritative data;
- identity, delegation, credentials, and trust;
- governance policy and its history;
- artifact, release, and migration integrity;
- private workflows and restricted evidence;
- public accountability without total surveillance;
- cultural rights, consent, and community authority;
- local continuity, recovery, and credible exit;
- availability under resource pressure and external dependency failure.

Security is an architectural property rather than a host-hardening checklist.

The controlling sequence is:

`text
explicit identity and scope
 ↓
verified trust and policy
 ↓
bounded interface and resource authority
 ↓
component-owned operation
 ↓
state verification and selective evidence
`

No layer silently supplies authority missing from another layer.

A valid identity does not imply authorization.

Policy approval does not imply resource availability.

Resource availability does not imply privilege.

Privilege approval does not imply execution success.

A receipt does not imply that every downstream obligation completed.

### 1.1 Security objectives

The security objectives are ordered as follows:

1. prevent fabricated or implicit authority;
2. contain compromise and lateral movement;
3. preserve confidentiality and cultural restrictions;
4. preserve integrity, provenance, and compatible lifecycle state;
5. maintain required local capability;
6. preserve accountability, recourse, and review;
7. retain restore, portability, and exit capability.

### 1.2 Security model

The baseline assumes that any of these can fail or become hostile:

- a remote caller;
- a legitimate but malicious user;
- a tenant administrator;
- a host operator;
- a service process;
- a build worker;
- a dependency or artifact repository;
- a removable medium;
- an external integration;
- an external AI service;
- a federation peer;
- a policy author;
- an update or recovery workflow;
- a resource-intensive workload.

The architecture therefore uses explicit authority, separation, least privilege, bounded execution, fail-closed decisions, immutable artifacts, selective evidence, and recoverable state.

## 2. Scope

### 2.1 Included systems

This baseline applies to:

- all primary profiles and overlays;
- all native components;
- optional workbenches;
- user and operator interfaces;
- build, test, release, and migration workflows;
- service containers and host services;
- databases, queues, indexes, caches, object stores, and file stores;
- privileged node operations;
- local and external integrations;
- external AI surfaces;
- offline imports and exports;
- backups, restores, and recovery environments;
- release artifacts and Release Sets;
- documentation tooling and generated implementation context.

### 2.2 Baseline and profile strengthening

The baseline fixes global boundaries.

Profiles can strengthen controls for:

- isolation;
- authentication assurance;
- trust roots;
- dual control;
- local artifact retention;
- offline operation;
- measured or verified boot;
- encrypted storage;
- network exposure;
- audit detail;
- recovery custody;
- release activation;
- evidence.

Profile strengthening does not transfer component ownership or weaken a global prohibition.

### 2.3 Profile interpretation

| Profile or overlay | Baseline interpretation |
| --- | --- |
| `user_lightweight` | Minimum local capability, limited service footprint, optional containers, no native AI dependency, and user-scale isolation |
| `developer_linux_workstation` | Isolated workspaces, rootless containers preferred, UV and `.venv` isolation, test-only credentials, and no production authority |
| `developer_windows_wsl` | Equivalent workspace and secret isolation using profile-permitted Docker or Podman behavior |
| `sovereign_linux_node` | Local trust, policy, audit, recovery, encrypted storage, signed image lifecycle, narrow privilege, and known-good rollback |
| `sovereign_hub` | Sovereign controls plus multi-node, multi-tenant, federation, and higher-capacity boundary enforcement |
| `build_farm` | Clean reproducible workers, isolated jobs, no unrestricted signing authority, OCI runtime, provenance, and disposable mutable state |
| `control_plane` | Administrative and orchestration interfaces separated from workload and data authority; Kubernetes only where the profile selects it |
| `high_assurance` | Stronger authentication, control separation, boot and trust evidence, dual control, restricted evidence, and recovery review |
| `sovereign_offline` | Local authority closure, no Internet dependency, signed offline imports, local revocation state, and local recovery material |
| `appliance_shell` | Restricted user shell and narrower interaction surface without changing component authority |

### 2.4 Excluded subjects

This document does not define:

- one universal cryptographic algorithm;
- one universal identity provider;
- one universal operating system;
- one universal container runtime;
- one universal network product;
- jurisdiction-specific legal requirements;
- exact retention durations;
- implementation commands;
- exact firewall rules;
- exact file-system paths;
- exact secrets-store product.

Those details belong to active profiles, component contracts, artifact contracts, security subdocuments, operations documents, or non-normative recipes.

## 3. Canonical References

### 3.1 Authority and invariants

`text
generated/authority-manifest.json
generated/decision-index.json
generated/requirements-index.json
generated/assertion-index.json
generated/decision-index.json
`

### 3.2 System and component boundaries

`text
contracts/system.contract.json
generated/component-catalog.json
generated/component-catalog.json
contracts/components/*.component.json
`

### 3.3 Profiles

`text
generated/profile-catalog.json
contracts/profiles/*.profile.json
`

### 3.4 Artifacts and releases

`text
contracts/release-channels.contract.json
contracts/artifact-classes.contract.json
contracts/artifact-contracts/*.schema.json
`

### 3.5 Integrations and evidence

`text
contracts/integration-types.contract.json
generated/exception-index.json
generated/traceability.json
generated/test-catalog.json
generated/evidence-catalog.json
`

### 3.6 Related security documents

`text
07-security/00-threat-model.md
07-security/02-security-domains.md
07-security/03-identity-trust-and-signatures.md
07-security/04-trust-root-scoping.md
07-security/05-privilege-boundaries.md
07-security/06-privileged-broker.md
07-security/07-secrets-and-keys.md
07-security/08-network-boundaries.md
07-security/09-storage-boundaries.md
07-security/10-data-at-rest.md
07-security/11-ai-boundaries.md
07-security/12-external-integration-classification.md
07-security/13-privacy-and-disclosure.md
07-security/14-cultural-rights-and-consent.md
07-security/15-selective-audit.md
07-security/16-public-evidence-and-private-proof.md
07-security/17-cross-domain-publication.md
07-security/18-offline-import-security.md
07-security/19-software-supply-chain.md
07-security/20-break-glass-security.md
`

The specialized documents refine this baseline without changing its ownership rules.

## 4. Model and Responsibilities

### 4.1 Explicit security authority

Security authority is distributed among registered owners.

| Security fact | Canonical owner |
| --- | --- |
| Component identity and responsibility | Component registry |
| Component interfaces, states, failures, and data boundaries | Component contract |
| Profile inclusion and strengthening | Profile contract |
| Authentication and trust assertions | Identity and Trust |
| Governance decisions and obligations | Governance Policy Runtime |
| CPU, memory, I/O, queue, and concurrency admission | Resource Governor |
| Privileged node-operation coordination | kOA Node Agent and registered privileged boundary |
| Cross-domain external publication | Publication Gateway |
| kOA Mediatheque admission | kOA Mediatheque |
| Publication to external UCKK Moodle | Publication Gateway with UCKK Publication Bridge |
| Artifact identity and lifecycle | Artifact class and release contracts |
| Integration permissions and data classes | Integration registry and manifest |
| Selective evidence handling | Audit Broker and evidence contracts |
| Authoritative application state | Owning component |

A security tool can observe or enforce its contract.

It does not become the canonical owner of every object it scans, signs, encrypts, schedules, or records.

### 4.2 Identity and request context

Every security-sensitive request resolves enough context to evaluate its contract.

Applicable context can include:

- actor identity;
- component identity;
- workload identity;
- tenant or security domain;
- active profile and overlays;
- requested action;
- target;
- purpose;
- data classes;
- consent;
- policy set;
- exception;
- correlation identity;
- validity period;
- artifact or release identity.

Context remains bounded.

The caller does not send unrestricted application state merely because a policy engine, audit service, or integration could inspect it.

### 4.3 Trust assertions

Trust is explicit and scoped.

A trust assertion identifies:

- issuer;
- subject;
- assertion class;
- scope;
- environment;
- tenant or security domain;
- artifact class or release channel where relevant;
- issue and expiry;
- revocation state;
- verification path.

A trust root valid for one tenant, channel, environment, or artifact class does not silently authorize another.

Historical verification material can remain retained without becoming active for new assertions.

### 4.4 Authentication

Authentication proves a bounded identity claim.

It does not prove:

- permission;
- consent;
- profile membership;
- release compatibility;
- publication approval;
- resource availability;
- cultural authority;
- execution success.

Authentication methods are selected by profile and risk.

High-assurance or recovery operations can require stronger methods and control separation than routine user actions.

### 4.5 Authorization and policy

The owning component enforces authorization at its boundary.

Governance Policy Runtime can evaluate authorization, disclosure, consent, privilege, or exception decisions when the active profile selects it.

The result remains bounded to:

- requester;
- action;
- target;
- scope;
- policy version;
- authority version;
- context;
- validity;
- obligations.

A result is not a standing credential.

A caller that cannot satisfy an obligation treats the operation as blocked.

### 4.6 Security domains

At minimum, deployments separate security domains where selected components are active.

Typical domains include:

- user session and graphical shell;
- Orgo;
- Konnaxion;
- Kristal Runtime;
- SemantiK Architect Runtime;
- Ariane Runtime;
- kOA Mediatheque;
- external UCKK Moodle publication integration;
- Governance Policy Runtime;
- Identity and Trust;
- Audit Broker;
- Publication Gateway;
- kOA Node Agent;
- Resource Governor;
- optional workbenches;
- build and update;
- recovery.

Separation can use:

- operating-system identities;
- containers or process namespaces;
- storage identities;
- database users and schemas;
- network policy;
- mandatory access control;
- resource limits;
- secret scopes;
- service-manager restrictions.

The exact mechanism remains profile-specific.

### 4.7 Least privilege

Least privilege applies to:

- files;
- sockets;
- devices;
- processes;
- databases;
- queues;
- indexes;
- APIs;
- networks;
- secrets;
- artifacts;
- administrative operations.

A service receives only the permissions required for its active interfaces.

Convenience, shared hosting, administrator access, or container co-location does not justify foreign data or privilege access.

### 4.8 Privilege hierarchy

The normal privileged path is:

`text
unprivileged caller
 ↓
registered component interface
 ↓
governance policy decision when required
 ↓
kOA Node Agent request
 ↓
closed privileged operation
 ↓
before-and-after verification
 ↓
operation receipt
`

The privileged boundary accepts closed operation types rather than arbitrary commands.

Inputs such as paths, unit names, devices, containers, release identifiers, and configuration values are validated against the operation contract.

### 4.9 Break-glass authority

Break-glass behavior remains exceptional.

It identifies:

- triggering condition;
- authorized actors;
- duration;
- exact capability;
- stronger authentication;
- evidence;
- notification;
- review;
- closure;
- key and credential handling;
- state reconciliation.

Break-glass authority does not become a permanent alternate administration API.

### 4.10 Secrets and key classes

Security material is separated by authority class.

Examples include:

- system release signing;
- service artifact signing;
- governance-policy signing;
- knowledge and language artifact signing;
- node identity;
- workload identity;
- integration credentials;
- tenant encryption;
- restricted evidence encryption;
- offline export encryption;
- audit anchoring;
- recovery.

Different classes use different scopes and lifecycle decisions.

Build workers produce candidate artifacts, digests, and attestations without receiving unrestricted release-signing authority.

### 4.11 Secret delivery

Secret values remain outside ordinary configuration and source.

Approved delivery can use:

- protected credential files;
- operating-system credential APIs;
- a registered secrets service;
- hardware-backed access;
- short-lived scoped tokens;
- task-scoped secret injection.

General process environments are avoided where they expose values too broadly.

A component that loses a required secret becomes unavailable or degraded rather than inventing a substitute identity.

### 4.12 Rotation and compromise

Rotation supports a declared overlap period without accepting old authority indefinitely.

A suspected compromise can trigger:

- credential revocation;
- key-class freeze;
- artifact or channel freeze;
- replacement identity;
- trust update;
- review of affected artifacts and decisions;
- offline revocation distribution;
- incident evidence;
- recovery or reissuance.

Recovering secret bytes does not automatically authorize continued use.

### 4.13 Host baseline

A profile that owns a host baseline addresses:

- maintained kernel, firmware, and system software;
- minimal installed packages;
- declared boot and release identity;
- signed image or package verification;
- durable-state encryption;
- restricted console and recovery;
- mandatory access control or equivalent confinement;
- update, rollback, and known-good state;
- inventory of active artifacts and services;
- drift detection;
- bounded resources.

Secure Boot, measured boot, TPM use, and similar mechanisms remain profile-conditioned rather than universal.

### 4.14 Service baseline

A service deployment uses:

- dedicated identity;
- explicit dependencies;
- minimal file-system access;
- explicit writable paths;
- restricted capabilities;
- confinement permitted by the profile;
- default-deny network policy;
- secret references;
- health and readiness;
- structured minimized logs;
- resource budgets;
- bounded retries and queues.

Rootless containers are preferred where the selected Linux profile adopts them.

Containerization does not replace authorization, data ownership, or service identity.

### 4.15 Application baseline

Applications protect their own interfaces.

Applicable controls include:

- secure session handling;
- tenant and domain context;
- authorization;
- origin and request-forgery controls;
- output encoding and scripting protections;
- injection protections;
- server-side request protections;
- bounded file and archive handling;
- idempotency for retryable writes;
- rate and abuse limits;
- safe errors;
- security headers;
- explicit upload and download contracts.

The exact control set depends on interface type.

### 4.16 Network baseline

Network connectivity is denied until permitted.

A permitted flow identifies:

- source identity;
- destination identity;
- direction;
- protocol;
- port or endpoint;
- purpose;
- data classes;
- authentication;
- encryption;
- profile;
- logging and evidence;
- failure behavior.

Network reachability is not authorization.

Internal service discovery does not create a component dependency or permission.

### 4.17 External network and integration boundary

Every external integration is classified.

An integration contract identifies:

- provider or peer;
- capability;
- profiles;
- data transferred;
- purpose;
- identity and credentials;
- endpoints;
- retention and terms;
- candidate or authoritative result class;
- adoption path;
- receipts;
- offline behavior;
- removal behavior.

External egress remains explicit and minimized.

An unavailable optional integration removes only its own capability.

### 4.18 Storage baseline

Storage access follows data ownership.

Each authoritative domain identifies:

- owner;
- storage identity;
- database or schema identity;
- encryption;
- backup;
- restore;
- migration;
- retention;
- deletion;
- access evidence.

Co-location in one database process does not remove logical ownership.

Sovereign and high-assurance profiles prefer stronger physical or service-instance separation where their contracts require it.

### 4.19 Data at rest

Sensitive durable state uses encryption and access controls appropriate to its classification.

The encryption relationship includes:

- data owner;
- key owner;
- key class;
- profile;
- recovery;
- rotation;
- backup;
- deletion;
- evidence.

Encryption does not replace authorization or data minimization.

A key unavailable during restore makes the affected recovery state blocked, not silently downgraded.

### 4.20 Untrusted inputs

Untrusted input categories include:

- user text and files;
- media;
- archives;
- structured imports;
- removable media;
- federation messages;
- external API responses;
- external AI output;
- generated code;
- dependency packages;
- manifests;
- configuration;
- recovery media.

Validation occurs before authoritative use.

Validation can include:

- schema;
- size;
- depth;
- content type;
- path safety;
- archive inventory;
- integrity;
- signature;
- provenance;
- policy;
- malware or safety scanning where selected;
- compatibility;
- destination authority.

### 4.21 Resource and denial-of-service controls

Security includes resource containment.

The architecture bounds:

- requests;
- payload sizes;
- file counts;
- archive expansion;
- parser depth;
- concurrent operations;
- retries;
- queues;
- CPU;
- memory;
- I/O;
- storage;
- process count;
- external calls.

Timeouts, backoff, circuit breaking, bulkheads, and task cancellation remain explicit.

Heavy optional engines cannot starve identity, policy, recovery, critical workflows, active knowledge, or local navigation.

### 4.22 Supply-chain baseline

Release-grade artifacts use:

- exact source identity;
- accepted change authority;
- locked or immutable dependencies;
- identified toolchains;
- clean build environments;
- reproducibility or independent verification;
- provenance;
- applicable SBOM or dependency inventory;
- artifact integrity;
- signatures or trust evidence;
- tests;
- evidence;
- profile and Release Set compatibility.

Signing keys remain outside ordinary build workers.

A signature confirms a signing event.

It does not prove semantic correctness, compatibility, or complete tests.

### 4.23 Artifact verification

Before use, an artifact is checked for:

- identity;
- class;
- version;
- integrity;
- provenance;
- signature and trust;
- revocation;
- compatibility;
- profile;
- lifecycle state;
- required companion artifacts;
- migration and recovery state.

A retained, staged, cached, or previously active artifact does not bypass current verification.

### 4.24 Release activation

Publication and activation remain separate.

Activation preserves the previous compatible known-good state.

The complete compatible Release Set is staged before the active pointer changes.

Post-activation checks verify:

- service readiness;
- policy authority;
- data and schema state;
- artifact identity;
- profile behavior;
- local recovery;
- critical workflows.

Failure restores known-good state or enters tested forward repair.

### 4.25 AI boundary

The native baseline contains no AI authority.

Approved external surfaces are limited by accepted integration decisions.

Their operations remain:

- explicit;
- user-triggered;
- capability-scoped;
- transparent about transferred data;
- removable;
- non-authoritative;
- unable to write directly to canonical stores.

Suno and Gamma remain user-triggered external adapters for candidate media workflows. Candidate output is admitted to the kOA Mediatheque before any separately authorized publication to UCKK.

Ariane external voice remains optional and separate from local navigation.

SenTient remains an isolated optional workbench in developer and build profiles.

### 4.26 Candidate-output adoption

An external or workbench output follows this pattern:

`text
explicit authorized export
 ↓
external or isolated processing
 ↓
candidate artifact + provenance
 ↓
controlled import
 ↓
destination validation and review
 ↓
explicit acceptance or rejection
`

The destination component owns the final state change.

No candidate receives authority from provider confidence, popularity, tool identity, or successful generation.

### 4.27 Privacy and disclosure

Privacy controls apply to:

- collection;
- access;
- search;
- rendering;
- export;
- publication;
- integration;
- AI use;
- audit;
- backup;
- restore;
- support.

Disclosure is explicit about:

- source;
- audience;
- destination;
- purpose;
- fields;
- consent;
- retention;
- evidence.

Publication Gateway performs governed external publication.

Governance Policy Runtime evaluates disclosure where selected.

The two authorities remain separate.

### 4.28 Cultural rights and consent

Cultural rights and community authority can restrict:

- ingest;
- reading;
- rendering;
- copying;
- export;
- publication;
- translation;
- AI transfer;
- model use;
- retention;
- withdrawal.

Restrictions are enforced at technical boundaries, not only documented in prose.

Restricted material does not enter an external AI or public evidence path without explicit applicable authority.

### 4.29 Selective audit

Audit is divided by purpose and audience.

| Audit class | Purpose |
| --- | --- |
| Public transparency receipt | Public proof of a bounded decision or event |
| Tenant or domain audit | Operational accountability inside an authorized domain |
| Restricted evidence | Sensitive evidence available to approved reviewers |
| Privacy record | Records access, disclosure, consent, or data-subject events |
| Security audit | Security-relevant identities, decisions, failures, and administrative actions |

One universal public log would create surveillance and disclosure risk.

One universal private log would erase public accountability.

Selective audit preserves both separation and linkage.

### 4.30 Evidence access

Access to restricted evidence is itself sensitive.

The evidence-access workflow can require:

- strong identity;
- declared purpose;
- policy decision;
- time-bounded access;
- field minimization;
- access receipt;
- notification or review;
- recourse.

Audit systems do not receive unrestricted payloads by default.

### 4.31 Offline security

An offline-capable deployment maintains local:

- identities and trust;
- revocation state;
- governance policy;
- active artifacts and Release Sets;
- previous known-good artifacts;
- migration and repair material;
- receipts;
- recovery environment;
- operator documentation.

Clock confidence, expiry, monotonic version state, and downgrade protection are considered during disconnected verification.

Stale or unverifiable trust becomes explicit degraded or blocked state.

### 4.32 Offline import

Offline import uses:

- controlled media receipt;
- quarantine;
- no auto-execution;
- bounded archive and parser behavior;
- inventory;
- integrity and signature verification;
- provenance;
- revocation and downgrade checks;
- profile and Release Set compatibility;
- staged validation;
- explicit activation;
- receipts.

Imported data or artifacts remain inactive until the owning lifecycle completes.

### 4.33 Backup, restore, and recovery

Backup preserves component ownership and encryption relationships.

Restore treats retained material as candidate recovery input.

Before activation, restore verifies:

- identity;
- integrity;
- trust;
- profile;
- Release Set;
- component compatibility;
- migration state;
- data ownership;
- key availability;
- evidence.

Recovery uses a reduced and isolated environment.

Trust-root changes and destructive recovery can require dual control under assurance profiles.

### 4.34 Development security

Development uses:

- isolated workspaces;
- UV and workspace-local `.venv` for Python;
- locked dependencies;
- separate services, ports, databases, secrets, and temporary state;
- code review;
- protected release inputs;
- secret scanning;
- static analysis;
- dependency and artifact scanning;
- component and profile tests;
- clean release builds.

Developer convenience does not create production authority.

Production keys, production data, and unrestricted production credentials remain outside development workspaces.

### 4.35 Vulnerability management

Every component and artifact class has:

- owner;
- supported versions;
- update path;
- severity process;
- disclosure path;
- mitigation;
- revocation or freeze behavior;
- evidence;
- terminal disposition.

A vulnerability can trigger:

- configuration mitigation;
- capability disablement;
- artifact revocation;
- release-channel freeze;
- emergency release;
- policy update;
- key rotation;
- rollback;
- forward repair.

A vulnerability exception remains explicit, scoped, time-bounded, controlled, and evidenced.

### 4.36 Security exceptions

An exception identifies:

- exact requirement or lock;
- owner;
- scope;
- affected profiles and components;
- reason;
- activation and closure conditions;
- expiry;
- compensating controls;
- tests;
- evidence.

An exception does not rewrite its underlying requirement.

An expired, missing, or unverifiable exception cannot authorize continued deviation.

### 4.37 Security receipts

Security-relevant receipts can cover:

- identity verification;
- policy decisions;
- privileged operations;
- artifact verification;
- publication;
- activation;
- rollback;
- recovery;
- key rotation;
- revocation;
- integration transfer;
- evidence access;
- exception use.

Receipts use references and minimized data where possible.

They exclude secret values and unrestricted protected payloads.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SEC-BASE-001,REQ-SEC-BASE-002,REQ-SEC-BASE-003,REQ-SEC-BASE-004,REQ-SEC-BASE-005,REQ-SEC-BASE-006,REQ-SEC-BASE-007,REQ-SEC-BASE-008,REQ-SEC-BASE-009,REQ-SEC-BASE-010,REQ-SEC-BASE-011,REQ-SEC-BASE-012,REQ-SEC-BASE-013,REQ-SEC-BASE-014,REQ-SEC-BASE-015,REQ-SEC-BASE-016,REQ-SEC-BASE-017,REQ-SEC-BASE-018,REQ-SEC-BASE-019,REQ-SEC-BASE-020,REQ-SEC-BASE-021,REQ-SEC-BASE-022,REQ-SEC-BASE-023,REQ-SEC-BASE-024,REQ-SEC-BASE-025,REQ-SEC-BASE-026,REQ-SEC-BASE-027,REQ-SEC-BASE-028,REQ-SEC-BASE-029,REQ-SEC-BASE-030,REQ-SEC-BASE-031,REQ-SEC-BASE-032,REQ-SEC-BASE-033,REQ-SEC-BASE-034,REQ-SEC-BASE-035,REQ-SEC-BASE-036,REQ-SEC-BASE-037,REQ-SEC-BASE-038,REQ-SEC-BASE-039,REQ-SEC-BASE-040,REQ-SEC-BASE-041,REQ-SEC-BASE-042,REQ-SEC-BASE-043,REQ-SEC-BASE-044,REQ-SEC-BASE-045,REQ-SEC-BASE-046,REQ-SEC-BASE-047,REQ-SEC-BASE-048 -->
- **REQ-SEC-BASE-001 — SHALL:** Every active component, service, workload, user session, build worker, integration adapter, and privileged operation have an explicit identity and bounded authority.
- **REQ-SEC-BASE-002 — SHALL:** Authentication, authorization, consent, disclosure, privilege, resource admission, and execution remain separate decisions when their contracts define separate authorities.
- **REQ-SEC-BASE-003 — SHALL NOT:** Administrator, root, operator, network, storage, or repository access create undocumented product, policy, data, release, or publication authority.
- **REQ-SEC-BASE-004 — SHALL:** Every component enforce authorization at its registered interface boundary before accessing or mutating authoritative state.
- **REQ-SEC-BASE-005 — SHALL:** Every request carry the tenant, security-domain, profile, actor, component, correlation, and purpose context required by the active contract.
- **REQ-SEC-BASE-006 — SHALL NOT:** Missing, stale, incompatible, unverifiable, or indeterminate identity, trust, policy, consent, exception, or compatibility state default to authority.
- **REQ-SEC-BASE-007 — SHALL:** Services, workloads, workspaces, databases, queues, indexes, secrets, networks, storage, and temporary state use least-privilege identities and explicit isolation.
- **REQ-SEC-BASE-008 — SHALL NOT:** A component write directly to another component's authoritative source tables or equivalent mutable source state.
- **REQ-SEC-BASE-009 — SHALL:** Cross-component communication use registered interfaces, commands, events, artifacts, user-authorized transfers, or governed gateways.
- **REQ-SEC-BASE-010 — SHALL:** Normal privileged node mutations pass through a narrow registered broker with closed input schemas, allowlists, policy binding, replay protection, idempotency, state verification, and receipts.
- **REQ-SEC-BASE-011 — SHALL NOT:** An ordinary component, user interface, integration, workbench, or external AI surface receive unrestricted shell, root, host, device, service-manager, firewall, release, or storage authority.
- **REQ-SEC-BASE-012 — SHALL:** Critical trust-root, release-signing, destructive recovery, and high-impact privilege operations use the approvals and control separation required by the effective assurance profile.
- **REQ-SEC-BASE-013 — SHALL:** Every secret and key belong to one declared class, owner, scope, environment, lifecycle, and recovery policy.
- **REQ-SEC-BASE-014 — SHALL NOT:** Keys of different authority classes be reused merely for operational convenience.
- **REQ-SEC-BASE-015 — SHALL NOT:** Secrets, raw tokens, private keys, unrestricted credentials, or recovery material enter source control, ordinary images, ordinary manifests, general logs, routine receipts, crash reports, or unprotected exports.
- **REQ-SEC-BASE-016 — SHALL:** Services receive secrets by protected reference or an approved credential mechanism and only for the duration and scope required by their contract.
- **REQ-SEC-BASE-017 — SHALL:** Key and credential lifecycles define issuance, activation, overlap, rotation, revocation, compromise, archival, recovery, and destruction.
- **REQ-SEC-BASE-018 — SHALL:** Durable sensitive state be encrypted at rest when required by its data classification, profile, or component contract.
- **REQ-SEC-BASE-019 — SHALL:** Network policy default to deny across security domains and permit only registered directions, protocols, endpoints, identities, and purposes.
- **REQ-SEC-BASE-020 — SHALL:** External egress be explicit, capability-scoped, profile-permitted, observable, and removable without breaking required local operation.
- **REQ-SEC-BASE-021 — SHALL NOT:** Inbound external connectivity, webhook exposure, remote administration, or federation trust exist without an explicit integration, security, and profile contract.
- **REQ-SEC-BASE-022 — SHALL:** Inputs from users, files, archives, removable media, networks, integrations, federation peers, external AI, and lower-trust domains be treated as untrusted until applicable validation completes.
- **REQ-SEC-BASE-023 — SHALL:** Parsers, uploads, archives, decompression, media processing, requests, queues, retries, and concurrency be bounded by explicit size, time, count, depth, and resource limits.
- **REQ-SEC-BASE-024 — SHALL:** Web and API surfaces apply applicable session, origin, request-forgery, injection, scripting, server-side request, upload, abuse, rate, and error-disclosure protections.
- **REQ-SEC-BASE-025 — SHALL:** Error messages and existence checks avoid disclosing foreign tenant, domain, identity, object, policy, or evidence existence.
- **REQ-SEC-BASE-026 — SHALL:** Host and service runtime hardening use maintained software, minimal packages, dedicated identities, explicit writable paths, restricted capabilities, resource limits, and profile-permitted confinement.
- **REQ-SEC-BASE-027 — SHALL NOT:** Privileged containers, broad host mounts, host PID, host IPC, host networking, unrestricted devices, or disabled confinement be used without an active scoped exception and compensating controls.
- **REQ-SEC-BASE-028 — SHALL:** Release artifacts, policy bundles, language packs, runtime packs, offline bundles, and other executable or authoritative artifacts be verified for identity, integrity, provenance, trust, compatibility, and lifecycle state before use.
- **REQ-SEC-BASE-029 — SHALL:** Builds and releases use declared source, locked dependencies, identified toolchains, reproducible environments, provenance, applicable dependency inventories, tests, and evidence.
- **REQ-SEC-BASE-030 — SHALL NOT:** A mutable tag, floating dependency, undeclared local file, unverified remote response, or mutable shared workspace state support a release or security claim.
- **REQ-SEC-BASE-031 — SHALL:** Published artifacts remain inactive until complete compatible staging and atomic activation succeed.
- **REQ-SEC-BASE-032 — SHALL:** Every activation preserve a previous compatible known-good state or provide a tested forward-repair path when rollback is unsafe.
- **REQ-SEC-BASE-033 — SHALL:** The global baseline contain no native generative AI, classifier, summarizer, embedding model, autonomous routing model, autonomous agent, or AI-based ingestion authority.
- **REQ-SEC-BASE-034 — SHALL:** Approved external AI operations be explicit, user-triggered, data-minimized, capability-scoped, profile-permitted, non-authoritative, and unable to write directly to canonical state.
- **REQ-SEC-BASE-035 — SHALL:** External AI and SenTient outputs remain candidate inputs until provenance, review, controlled import, destination validation, and explicit authoritative acceptance complete.
- **REQ-SEC-BASE-036 — SHALL NOT:** AI output grant privilege, activate releases, create policy authority, determine final consent or cultural rights, publish binding results, or become the only path to core correctness or recovery.
- **REQ-SEC-BASE-037 — SHALL:** Cultural rights, consent, privacy, audience, purpose, and disclosure constraints be enforced at every applicable ingest, read, export, render, publication, integration, AI, backup, and restore boundary.
- **REQ-SEC-BASE-038 — SHALL:** Publication Gateway remain the controlled cross-domain publication boundary and remain separate from policy evaluation and kOA Mediatheque admission; UCKK publication shall use a destination-specific adapter under that gateway.
- **REQ-SEC-BASE-039 — SHALL:** Audit be selective, classified, access-controlled, minimized, integrity-protected, and separated into public receipts, tenant audit, restricted evidence, privacy records, and security audit as applicable.
- **REQ-SEC-BASE-040 — SHALL NOT:** Audit, observability, support, diagnostics, or evidence systems become unrestricted replicas of application data, secrets, private content, or protected cultural material.
- **REQ-SEC-BASE-041 — SHALL:** Access to restricted evidence, secret material, recovery authority, quarantine, and high-impact administrative functions itself produce protected audit evidence.
- **REQ-SEC-BASE-042 — SHALL:** Security failure and dependency loss degrade only affected capabilities while preserving unrelated local identity, policy, navigation, language, data, recovery, and core workflow capability.
- **REQ-SEC-BASE-043 — SHALL NOT:** Failure activate a silent provider, policy, privilege, AI, publication, trust, network, or data-authority substitute.
- **REQ-SEC-BASE-044 — SHALL:** Offline-capable profiles retain local trust, revocation, policy, artifact, release, receipt, recovery, and operator material sufficient for their declared disconnected envelope.
- **REQ-SEC-BASE-045 — SHALL:** Offline imports use quarantine, bounded parsing, inventory checks, signature and provenance verification, downgrade protection, compatibility validation, controlled staging, and explicit activation.
- **REQ-SEC-BASE-046 — SHALL:** Backup, restore, recovery, and credible-exit workflows preserve identity, ownership, encryption, trust, Release Set, migration, evidence, and current compatibility boundaries.
- **REQ-SEC-BASE-047 — SHALL:** Security controls, exceptions, vulnerabilities, incidents, revocations, compensating controls, tests, and evidence have explicit owners and terminal lifecycle states.
- **REQ-SEC-BASE-048 — SHALL:** A semantic change to identity, trust, privilege, secrets, network, storage, artifact verification, AI boundaries, audit, offline security, recovery, or security degradation use an accepted owner decision and complete impact analysis.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Admit a component request

1. Identify the caller, component, tenant or security domain, profile, action, target, purpose, and correlation identity.
2. authenticate the caller.
3. verify required trust assertions.
4. validate the request contract, size, and context.
5. evaluate authorization and applicable governance decisions.
6. resolve consent, disclosure, cultural-rights, and exception state where relevant.
7. verify resource admission where the operation is resource-sensitive.
8. invoke the owning component operation.
9. verify the resulting state.
10. record selected evidence.
11. return a minimized result.

### 6.2 Execute a privileged operation

1. Receive a closed operation request.
2. verify requester and component identity.
3. verify the exact operation schema.
4. resolve the applicable policy decision and obligations.
5. verify replay and idempotency state.
6. verify target and before-state.
7. enforce timeout and cancellation.
8. execute only the allowlisted operation.
9. verify after-state.
10. record decision and operation receipts.
11. close temporary authority.

### 6.3 Provision a service

1. Resolve the component contract and active profile.
2. create a dedicated service identity.
3. allocate owned storage and database identity.
4. apply network policy.
5. apply file-system and process confinement.
6. apply resource limits.
7. resolve secrets by reference.
8. verify artifact identity and compatibility.
9. start the service.
10. evaluate health and readiness.
11. expose registered interfaces only after readiness passes.

### 6.4 Rotate a credential or key

1. Identify key class, owner, scope, and dependents.
2. create or obtain replacement material through the approved custody process.
3. stage verification and trust updates.
4. define overlap.
5. update dependents without exposing raw material.
6. verify new use.
7. stop new use of old material.
8. distribute revocation or retirement state, including offline paths where required.
9. retain historical verification material according to policy.
10. destroy obsolete private material only after all obligations close.
11. produce rotation evidence.

### 6.5 Handle suspected key compromise

1. Identify affected key class and scope.
2. freeze affected signing, publication, integration, or trust activity.
3. revoke or quarantine affected authority.
4. identify artifacts, decisions, nodes, and releases that depend on it.
5. preserve investigation evidence.
6. issue replacement trust material.
7. publish and distribute revocation state.
8. reverify or replace affected artifacts.
9. recover active environments.
10. close the incident only after verification and evidence complete.

### 6.6 Approve an external integration request

1. Resolve the integration and operation.
2. verify profile applicability.
3. identify the user and requesting component.
4. present purpose and transferred data.
5. minimize and classify the payload.
6. resolve policy, consent, and cultural-rights constraints.
7. obtain explicit user confirmation.
8. resolve scoped credentials and endpoint policy.
9. perform the bounded request.
10. treat the response as untrusted candidate input.
11. create provenance.
12. send the candidate through controlled destination adoption.

### 6.7 Import an offline artifact

1. Receive media through the approved physical boundary.
2. create a transfer and custody record.
3. quarantine the media and contents.
4. inspect inventory and enforce parser limits.
5. verify identity, integrity, provenance, signatures, and revocation.
6. verify downgrade and monotonic version rules.
7. verify profile, component, artifact, and Release Set compatibility.
8. stage the complete inactive artifact set.
9. verify rollback or forward-repair readiness.
10. obtain required activation authority.
11. activate atomically.
12. record import and activation evidence.

### 6.8 Restore a node or service

1. Enter the isolated recovery environment.
2. authenticate recovery actors.
3. resolve recovery policy and control separation.
4. identify the target profile and known-good Release Set.
5. verify recovery artifacts, trust, keys, and backups.
6. restore component-owned state through component recovery contracts.
7. verify migrations and ownership boundaries.
8. stage the complete authority set.
9. activate atomically.
10. run acceptance checks.
11. revoke temporary recovery authority.
12. produce recovery evidence and post-event review.

### 6.9 Respond to a vulnerability

1. Record the affected component, artifact, dependency, profile, and versions.
2. classify severity and exploitability.
3. identify active and retained deployments.
4. choose mitigation, disablement, revocation, rollback, or repair.
5. update policy and integration controls where needed.
6. build and validate corrective artifacts.
7. distribute connected and offline updates.
8. verify recovery.
9. retain incident, release, and exception evidence.
10. close only after affected authority states are reconciled.

### 6.10 Grant restricted-evidence access

1. Identify requester, evidence class, subject, purpose, and duration.
2. authenticate with the assurance required by the evidence policy.
3. evaluate access policy and applicable consent.
4. minimize fields and time range.
5. expose only the approved representation.
6. prevent bulk export unless separately authorized.
7. record access evidence.
8. close access at expiry.
9. provide review or recourse where required.

### 6.11 Apply a security exception

1. Resolve the registered exception.
2. verify owner, scope, affected requirement, profiles, and components.
3. verify active period and closure condition.
4. verify compensating controls.
5. execute exception-specific tests.
6. collect required evidence.
7. apply the bounded exception.
8. monitor expiry and closure.
9. remove the exception when its condition ends.
10. retain history without changing the underlying requirement.

### 6.12 Decommission a security-sensitive integration

1. Stop new requests.
2. revoke provider credentials.
3. remove network allowlists and endpoints.
4. preserve required receipts and candidate dispositions.
5. remove adapter services and secrets.
6. verify that no authoritative state depends on the integration.
7. verify core and local capabilities.
8. update profile and integration catalogs.
9. produce decommission evidence.

## 7. Failure States and Safe Degradation

| Failure condition | Required response | Preserved behavior | Blocked behavior |
| --- | --- | --- | --- |
| Identity cannot be verified | Block affected operation | Existing valid sessions and unrelated local capability | New identity-dependent action |
| Trust or revocation state is stale | Mark affected trust state degraded or blocked | Unaffected trust domains | New trust-dependent authority |
| Policy runtime is unavailable where required | Block governed transitions | Unaffected non-governed capability | New governed action |
| Resource Governor is unavailable | Defer or block new resource-sensitive work | Existing authoritative state and lightweight capability | New heavy work |
| Privileged broker is unavailable | Block host mutation | Unprivileged product capability | New privileged operation |
| Secret cannot be resolved | Mark dependent service not ready | Other services and stored state | Secret-dependent operation |
| Key compromise is suspected | Freeze affected authority and start incident response | Unaffected key classes and known-good state | New use of affected key |
| Network dependency is unavailable | Disable affected external or distributed capability | Local core and offline-capable functions | External request |
| External AI is unavailable | Disable that assistance capability | Native local operation | External AI assistance |
| External response fails validation | Reject or quarantine candidate | Destination authoritative state | Adoption |
| Publication Gateway is unavailable | Block new external publication | Source-owned state and internal workflows | Publication |
| kOA Mediatheque admission is unavailable | Block new local media admission | Existing local media reads, export, backup, and unrelated capability | New local admission |
| External UCKK is unavailable | Queue or reject authorized publication according to policy | Local kOA Mediatheque operation | New remote delivery |
| Audit path is unavailable | Apply evidence policy and block receipt-critical transitions | Existing state and locally buffered evidence where permitted | Evidence-required critical transition |
| Storage encryption key is unavailable | Mark affected data inaccessible and start recovery | Unaffected domains | Access or restore of affected data |
| Artifact verification fails | Quarantine artifact | Active known-good artifact | Staging or activation |
| Release compatibility is unknown | Reject candidate Release Set | Active release | Activation |
| Migration preflight fails | Preserve current state | Known-good release | Migration and activation |
| Post-activation readiness fails | Roll back or forward repair | Recoverable prior or repaired state | Release acceptance |
| Offline bundle is incomplete | Reject import | Current local authority | Staging |
| Recovery authority is incomplete | Keep recovery blocked | Current or safely stopped state | Trust-changing recovery |
| Evidence-access policy is unresolved | Deny restricted evidence access | Evidence confidentiality | Restricted disclosure |
| Security exception expires | Remove exception authority | Underlying requirement | Continued deviation |
| Resource exhaustion occurs | Shed optional and low-priority work first | Identity, policy, recovery, and critical workflows | New optional heavy work |
| Complete security validation cannot run | Keep previous active authority | Existing known-good state | New conformance or release claim |

Failure does not authorize:

- a default allow;
- direct database access;
- unrestricted root;
- a silent external provider;
- a local AI substitute;
- a stale artifact;
- a partial Release Set;
- a shared secret;
- a foreign data write;
- total audit;
- suppressed evidence;
- identifier reuse.

## 8. Cross-Component Interactions

### 8.1 Identity and Trust

Identity and Trust owns verified identities, artifact trust assertions, signer verification, and trust status.

Other components consume bounded assertions.

They do not mutate identity or trust stores directly.

### 8.2 Governance Policy Runtime

Governance Policy Runtime evaluates governed decisions.

It does not:

- execute application actions;
- allocate resources;
- publish;
- issue credentials;
- perform privileged host mutation.

Callers enforce results and own state transitions.

### 8.3 Resource Governor

Resource Governor controls resource admission and scheduling.

It does not make authorization, disclosure, consent, privilege, or exception decisions.

Security-sensitive work can require both governance approval and resource admission.

### 8.4 kOA Node Agent

kOA Node Agent coordinates exact node-local operations.

It remains behind authenticated, policy-bound, closed interfaces.

The privileged executor remains narrow and does not expose an arbitrary shell.

### 8.5 Audit Broker

Audit Broker handles selected evidence according to class and audience.

It does not become:

- an application database;
- a secret store;
- a public log of private content;
- the owner of audited events.

### 8.6 Publication Gateway

Publication Gateway is the external publication executor.

It verifies disclosure authority and obligations, prepares the permitted representation, performs transport, and records publication results.

It does not decide governance policy or own source data.

### 8.7 kOA Mediatheque admission and UCKK publication

The kOA Mediatheque controls explicit selected-media admission into its own local authority domain.

It does not publish externally, invoke Suno or Gamma, infer consent, or write directly to external UCKK storage.

For external publication, Publication Gateway authorizes disclosure and the UCKK adapter performs authenticated Moodle delivery. UCKK remains the final authority for acceptance into its own separate platform.

### 8.8 Ariane Runtime

Ariane local navigation remains deterministic and locally available.

External voice is optional and profile-permitted.

Loss of voice preserves keyboard, pointer, touch, menus, shortcuts, accessibility controls, and deterministic commands.

### 8.9 SenTient

SenTient remains isolated, optional, task-activated, and non-authoritative.

It is limited to developer and build profiles.

Its outputs require provenance, review, controlled import, and destination acceptance.

### 8.10 Build farm

Build workers use clean isolated jobs and declared inputs.

They produce candidate artifacts, provenance, and validation evidence.

They do not receive unrestricted production signing, activation, or application-data authority.

### 8.11 Profile and lifecycle authority

Profiles strengthen controls.

Artifact and release contracts govern published executable authority.

Security validation confirms both without turning profile implementation or repository state into product authority.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Closed decisions

| Decision | Closed choice |
| --- | --- |
| `DEC-AI-001` | No native AI baseline; approved external surfaces are explicit, removable, and non-authoritative |
| `DEC-SENT-001` | SenTient is an optional isolated workbench outside the user baseline |
| `DEC-MEDIATHEQUE-001` | kOA Mediatheque behavior is deterministic and local |
| `DEC-UCKK-EXT-001` | UCKK is an external online Moodle and Mediatheque interchange target |
| `DEC-ARI-001` | Ariane local navigation is independent of optional external voice |
| `DEC-PROFILE-001` | Security strengthening and implementation remain profile-specific |
| `DEC-DATA-001` | Component data ownership is exclusive and cross-component source writes are prohibited |
| `DEC-GOV-001` | Governance Policy Runtime and Resource Governor are separate authorities |
| `DEC-GATE-001` | Local Mediatheque admission and external publication remain separate |
| `DEC-CONTAINER-001` | Container choices remain profile-scoped |
| `DEC-K8S-001` | Kubernetes is not an endpoint requirement |
| `DEC-REL-001` | Four release channels retain independent identity and Release Set compatibility |
| `DEC-DOC-CHANGE-001` | Security semantics change through accepted decisions and transitive impact analysis |

### 9.2 Protected locks

| Lock group | Protected boundary |
| --- | --- |
| `LOCK-AI-001`, `LOCK-AI-002` | No native AI authority and no direct authoritative mutation by external AI |
| `LOCK-SENT-001` | SenTient remains optional, isolated, and non-authoritative |
| `LOCK-MEDIATHEQUE-001`, `LOCK-MEDIATHEQUE-002` | kOA Mediatheque remains deterministic; Suno and Gamma remain explicit candidate-producing adapters |
| `LOCK-UCKK-EXT-001` | UCKK publication and import remain explicit, external, and unable to claim authority over the other Mediatheque |
| `LOCK-ARI-001`, `LOCK-ARI-002` | Local navigation remains independent of voice |
| `LOCK-DATA-001` | No direct foreign authoritative write |
| `LOCK-GOV-001` | Resource and policy authority remain separate |
| `LOCK-GATE-001` | Local media admission and cross-domain publication remain separate |
| `LOCK-COMP-001`, `LOCK-COMP-002` | Kristal identity and language build/runtime boundaries remain intact |
| `LOCK-PROFILE-001` | Profile strengthening does not become global |
| `LOCK-DEV-001` to `LOCK-DEV-005` | Development dependencies and mutable state remain isolated |
| `LOCK-LIFE-001` to `LOCK-LIFE-004` | Artifact activation, recovery, Release Sets, and channel compatibility remain controlled |
| `LOCK-IMPL-001`, `LOCK-IMPL-002` | Recipes and profile-specific Linux mechanisms do not become universal architecture |

### 9.3 Prohibited assumptions

The following assumptions are invalid:

- root access creates policy authority;
- an administrator can bypass component ownership;
- authentication implies authorization;
- authorization implies consent or disclosure;
- policy approval implies resource availability;
- a privilege decision is a reusable credential;
- a receipt proves every downstream action;
- one service identity can safely serve every component;
- one database user preserves component ownership;
- internal network access is trusted by default;
- encryption removes the need for authorization;
- containerization creates isolation automatically;
- root inside a container is harmless;
- development secrets are acceptable in test artifacts;
- a signature proves semantic correctness;
- a valid signature overrides revocation;
- a previously active artifact remains compatible forever;
- publication implies activation;
- a partial Release Set is temporarily acceptable;
- rollback is always safe;
- an external AI output is trustworthy because it is well written;
- prompts are sufficient security boundaries;
- local AI would automatically be safer or authoritative;
- SenTient can update canonical stores because it is local;
- Suno or Gamma can be called automatically by kOA Mediatheque ingestion or UCKK publication;
- Ariane voice can silently replace local navigation;
- audit requires total transparency;
- logs can contain secrets because access is restricted;
- support tooling can read all tenant data;
- offline operation can ignore revocation or downgrade;
- removable media is trusted because it is physically delivered;
- recovery authority can bypass trust controls;
- high assurance changes global component ownership;
- a Kubernetes control plane grants application authority;
- current implementation behavior overrides active contracts;
- a recipe creates a security exception;
- an expired exception remains effective;
- security failure permits silent fallback;
- unavailable validation can be recorded as passing.

Missing identity, trust, policy, profile, compatibility, exception, migration, recovery, or evidence blocks the affected authority transition.

## 10. Validation Criteria

This document is conformant when:

1. the document is registered as `DOC-SEC-001`;
2. the path is `07-security/01-security-baseline.md`;
3. the active language is English;
4. all security-sensitive actors and workloads have explicit identities;
5. authority classes remain separate;
6. missing or indeterminate authority fails closed;
7. every active component enforces authorization at its interface;
8. tenant and security-domain context is preserved;
9. service, storage, network, database, queue, index, and secret identities are isolated;
10. direct foreign authoritative writes are rejected;
11. privileged operations use closed schemas and a narrow broker;
12. ordinary components lack unrestricted root and host authority;
13. high-impact operations apply profile-required control separation;
14. key classes are not reused across authority domains;
15. secrets are absent from source, images, general logs, and routine receipts;
16. credential delivery is protected and scoped;
17. rotation, revocation, recovery, and compromise procedures exist;
18. required durable sensitive state is encrypted;
19. inter-domain networking defaults to deny;
20. external egress is explicit and removable;
21. external inbound connectivity has an active contract;
22. untrusted inputs receive bounded validation;
23. parsers, archives, requests, retries, queues, and resources are bounded;
24. applicable application-interface protections pass;
25. errors do not disclose foreign object existence;
26. host and service hardening match the active profile;
27. overprivileged container and host access is rejected without an exception;
28. artifacts verify identity, integrity, provenance, trust, compatibility, and lifecycle;
29. builds use declared reproducible inputs;
30. mutable tags and undeclared state do not support release claims;
31. artifact publication and activation remain separate;
32. known-good rollback or tested forward repair exists;
33. no native AI baseline capability is present;
34. external AI is explicit, minimized, removable, and non-authoritative;
35. candidate-output adoption remains controlled;
36. AI cannot grant privilege or release authority;
37. privacy, disclosure, consent, and cultural-rights controls apply at each relevant boundary;
38. Publication Gateway remains separate from policy and local Mediatheque admission, and UCKK delivery uses its controlled adapter;
39. audit remains selective and classified;
40. evidence stores do not replicate unrestricted application content;
41. restricted-evidence access is audited;
42. dependency failure degrades only affected capability;
43. no silent provider or authority fallback occurs;
44. offline profiles retain local authority and recovery closure;
45. offline imports use quarantine and complete verification;
46. restore verifies complete current compatibility;
47. vulnerabilities and exceptions have explicit lifecycle ownership;
48. semantic changes include accepted decisions and impact analysis;
49. all 48 linked requirements resolve;
50. all required security tests execute;
51. all required evidence validates;
52. no unresolved security authority remains;
53. generated security catalogs and AI context match canonical authority;
54. complete documentation validation passes.

Expected test coverage includes:

`text
TEST-SEC-BASE-001 Explicit identity and authority context
TEST-SEC-BASE-002 Fail-closed missing trust or policy
TEST-SEC-BASE-003 Component-interface authorization
TEST-SEC-BASE-004 Tenant and security-domain isolation
TEST-SEC-BASE-005 Direct foreign-write rejection
TEST-SEC-BASE-006 Narrow privileged broker
TEST-SEC-BASE-007 Privileged-operation replay and idempotency
TEST-SEC-BASE-008 Secret and key-class separation
TEST-SEC-BASE-009 Secret exclusion from artifacts and logs
TEST-SEC-BASE-010 Credential rotation and revocation
TEST-SEC-BASE-011 Default-deny network policy
TEST-SEC-BASE-012 External egress classification
TEST-SEC-BASE-013 Bounded parser and archive handling
TEST-SEC-BASE-014 Web and API security controls
TEST-SEC-BASE-015 Profile-conditioned host hardening
TEST-SEC-BASE-016 Least-privilege service isolation
TEST-SEC-BASE-017 Artifact trust and compatibility verification
TEST-SEC-BASE-018 Reproducible supply-chain validation
TEST-SEC-BASE-019 Atomic activation and known-good recovery
TEST-SEC-BASE-020 No native AI capability
TEST-SEC-BASE-021 External AI candidate boundary
TEST-SEC-BASE-022 Cultural-rights and consent enforcement
TEST-SEC-BASE-023 Publication Gateway separation
TEST-SEC-BASE-024 Selective audit classification
TEST-SEC-BASE-025 Restricted-evidence access audit
TEST-SEC-BASE-026 Capability-scoped degradation
TEST-SEC-BASE-027 Offline trust and revocation closure
TEST-SEC-BASE-028 Quarantined offline import
TEST-SEC-BASE-029 Recovery boundary and control separation
TEST-SEC-BASE-030 Security exception lifecycle
`

The test catalog and evidence registry own executable controls and evidence definitions.

This document does not claim that those tests have already executed.

## 11. Non-Normative Examples

> **Non-normative example:** These examples illustrate valid security behavior. They do not redefine component, profile, security, or artifact contracts.

### 11.1 Routine component request

An Orgo request arrives with an actor, tenant, action, target, purpose, and correlation identity.

Orgo authenticates the caller, evaluates applicable policy, validates the request, performs the Orgo-owned state transition, and emits selected evidence.

No other service writes to the Orgo database.

### 11.2 Privileged release activation

An operator requests activation of a signed Release Set on a sovereign node.

Governance Policy Runtime evaluates privilege.

kOA Node Agent validates the closed operation and coordinates the privileged executor.

The node verifies the staged Release Set, changes authority atomically, evaluates readiness, and records decision and operation receipts.

### 11.3 Optional ChatGPT assistance

A user explicitly selects text and requests draft assistance.

The integration presents the transferred data, minimizes it, and sends one bounded request.

The response returns as a candidate with provenance.

The destination component reviews and accepts or rejects it.

Loss of the external service preserves all native workflows.

### 11.4 kOA Mediatheque, UCKK, and Suno

A user selects a media item and explicitly requests a Suno workflow.

The system performs a controlled export through the registered adapter.

The returned output is untrusted candidate media.

It enters controlled re-import and user approval.

kOA Mediatheque ingestion never calls Suno automatically. Publication to UCKK is a separate explicit operation.

### 11.5 Ariane voice failure

The external voice path becomes unavailable.

Voice controls report unavailable status.

Keyboard, pointer, touch, menus, shortcuts, accessibility controls, and deterministic local commands remain operational.

No local or alternate AI model starts silently.

### 11.6 Restricted evidence

An investigator requests access to sensitive incident evidence.

The system verifies identity and purpose, evaluates access policy, exposes a minimized representation for a bounded period, and records the evidence-access event.

The evidence does not enter a public transparency log.

### 11.7 Offline import

A sovereign-offline node receives a signed bundle on removable media.

The node quarantines the media, checks inventory and parser limits, verifies signatures and revocation, checks downgrade and compatibility, stages the complete Release Set, and activates atomically.

The media contents never execute automatically.

### 11.8 Compromised signing key

A governance signing key is suspected compromised.

Governance publication freezes.

Trust state is revoked and distributed through connected and offline paths.

Affected policy bundles and Release Sets are reviewed.

Replacement keys and artifacts receive new identity, validation, and evidence.

### 11.9 Resource exhaustion

A heavy optional workbench consumes its resource envelope.

Resource Governor stops or delays that workload.

Identity, local policy, recovery, local navigation, and critical component workflows retain their reserved capacity.

### 11.10 Invalid merged authority

A proposed administrative service owns user authorization, root credentials, release signing, policy decisions, audit, publication, and product databases.

The design is invalid because it removes independent authority, containment, review, and recovery boundaries.
