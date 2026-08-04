<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-DEV-014",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "development",
  "scope": [
    "developer_linux_workstation",
    "developer_windows_wsl",
    "build_farm"
  ],
  "canonical_refs": [
    "contracts/system.contract.json#/release_and_artifact_identity",
    "contracts/system.contract.json#/critical_transitions",
    "contracts/system.contract.json#/degradation_baseline",
    "contracts/system.contract.json#/resource_governance",
    "generated/profile-catalog.json",
    "contracts/profiles/developer-linux-workstation.profile.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "contracts/profiles/build-farm.profile.json",
    "generated/toolchain-catalog.json",
    "contracts/toolchains/python-uv.toolchain.json",
    "contracts/artifact-classes.contract.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/traceability.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "schemas/test-evidence.schema.json"
  ],
  "decision_ids": [
    "DEC-DEV-001",
    "DEC-DEV-002",
    "DEC-PROFILE-001",
    "DEC-CONTAINER-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-HW-001",
    "DEC-REL-001",
    "DEC-AI-001"
  ],
  "requirement_ids": [
    "REQ-DEV-BTV-001",
    "REQ-DEV-BTV-002",
    "REQ-DEV-BTV-003",
    "REQ-DEV-BTV-004",
    "REQ-DEV-BTV-005",
    "REQ-DEV-BTV-006",
    "REQ-DEV-BTV-007",
    "REQ-DEV-BTV-008",
    "REQ-DEV-BTV-009",
    "REQ-DEV-BTV-010",
    "REQ-DEV-BTV-011",
    "REQ-DEV-BTV-012",
    "REQ-DEV-BTV-013",
    "REQ-DEV-BTV-014",
    "REQ-DEV-BTV-015",
    "REQ-DEV-BTV-016",
    "REQ-DEV-BTV-017",
    "REQ-DEV-BTV-018",
    "REQ-DEV-BTV-019",
    "REQ-DEV-BTV-020",
    "REQ-DEV-BTV-021",
    "REQ-DEV-BTV-022",
    "REQ-DEV-BTV-023",
    "REQ-DEV-BTV-024"
  ],
  "lock_ids": [
    "LOCK-DEV-001",
    "LOCK-DEV-002",
    "LOCK-PROFILE-001",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-003",
    "DOC-SYS-000",
    "DOC-SYS-018",
    "DOC-PROFILE-005",
    "DOC-PROFILE-006",
    "DOC-DEV-000",
    "DOC-DEV-001",
    "DOC-DEV-002",
    "DOC-DEV-003",
    "DOC-DEV-004",
    "DOC-DEV-012",
    "DOC-DEV-013"
  ],
  "tags": [
    "development",
    "build",
    "test",
    "validation",
    "evidence",
    "reproducibility",
    "release-gates",
    "workspace-isolation",
    "build-farm",
    "supply-chain"
  ]
}
KOA:DOC-META:END -->

# Build, Test, and Validation

## 1. Purpose

This document defines how kOA source changes are built, tested, validated, evidenced, and advanced from a developer workspace toward merge and release.

Its purpose is to prevent four distinct outcomes from being confused:

- developer feedback;
- workspace validation;
- profile or conformance evidence;
- release-authoritative evidence.

A local success is useful feedback. It becomes authoritative support only when the test is registered, the execution context is complete, the environment is valid, the result satisfies the test contract, and the resulting evidence remains active for the exact claim.

This document does not make Markdown the owner of test definitions, evidence validity, profile membership, artifact classes, release gates, or toolchain versions.

## 2. Scope

This document applies to:

- `developer_linux_workstation`;
- `developer_windows_wsl`;
- `build_farm`;
- source builds and packaging;
- repository and contract validation;
- unit, contract, integration, component, profile, security, lifecycle, offline, performance, resource, and reproducibility tests;
- test fixtures and isolated service dependencies;
- clean workers and reproducible environments;
- candidate artifacts, SBOMs, provenance, logs, reports, receipts, and test evidence;
- merge validation and release gates;
- evidence invalidation and supersession;
- development-to-release transitions.

It does not define the semantic content of a component test, profile test, artifact class, release policy, security policy, or deployment operation. Those remain owned by their canonical registries and contracts.

## 3. Canonical References

| Canonical reference | Ownership |
| --- | --- |
| `contracts/system.contract.json#/release_and_artifact_identity` | Release channels, Release Sets, compatibility, non-partial activation, and recovery |
| `contracts/system.contract.json#/critical_transitions` | Critical transitions requiring machine-readable receipts |
| `contracts/system.contract.json#/degradation_baseline` | Fail-closed validation, preserved valid state, and pressure degradation |
| `contracts/system.contract.json#/resource_governance` | Resource Governor and Governance Policy Runtime separation |
| `generated/profile-catalog.json` | Active profile and overlay identity |
| `contracts/profiles/developer-linux-workstation.profile.json` | Linux development validation scope |
| `contracts/profiles/developer-windows-wsl.profile.json` | WSL development validation and evidence boundary |
| `contracts/profiles/build-farm.profile.json` | Clean worker, artifact cache, reproducibility, and release-evidence scope |
| `generated/toolchain-catalog.json` | Registered development and build toolchains |
| `contracts/toolchains/python-uv.toolchain.json` | Python environment, lock, frozen synchronization, and command rules |
| `contracts/toolchains/container-runtime.toolchain.json` | Container and service environment identity |
| `contracts/artifact-classes.contract.json` | Artifact, SBOM, provenance, evidence, receipt, activation, and recovery classes |
| `generated/test-catalog.json` | Registered tests, subjects, expectations, execution classes, and evidence requirements |
| `generated/evidence-catalog.json` | Active evidence identity, validity, supersession, and claim support |
| `generated/traceability.json` | Decision, requirement, lock, profile, component, artifact, test, and evidence relationships |
| `generated/requirements-index.json` | Normative statements projected in Section 5 |
| `generated/assertion-index.json` | Development, profile, data, governance, lifecycle, AI, and implementation invariants |
| `schemas/test-evidence.schema.json` | Required structure of each test-evidence record |

## 4. Model and Responsibilities

### 4.1 Validation subjects

A validation subject is the exact object or composition being tested.

Examples include:

- one source revision;
- one component contract and implementation;
- one interface version;
- one primary profile with specific overlays;
- one hardware envelope;
- one artifact;
- one Release Set;
- one target deployment;
- one backup, restore, or recovery path.

A test result for one subject does not automatically apply to another branch, profile, component set, toolchain, artifact version, operating system, hardware envelope, or connectivity state.

### 4.2 Validation levels

| Validation level | Coverage | Subject | Supported claim |
| --- | --- | --- | --- |
| Unit tests | One function, module, parser, validator, transformation, or deterministic rule | Implementation unit | Local implementation correctness |
| Contract tests | Versioned request, response, event, artifact, state, error, authority, and failure behavior | One component or interface contract | Component contract compatibility |
| Integration tests | Declared cross-component interaction through APIs, commands, events, gateways, artifacts, or read models | Two or more components | Interaction correctness without authority transfer |
| Component tests | Component responsibilities, owned data, interfaces, lifecycle, resource limits, safe degradation, backup, and recovery | One deployed component | Component claim |
| Profile tests | Composition, overlays, component membership, connectivity, hardware, security, implementation choices, and capability degradation | One exact deployment profile | Profile conformance claim |
| Security tests | Identity, trust, privilege, secrets, boundaries, replay, authorization, disclosure, signing, and supply chain | Declared security scope | Security claim |
| Lifecycle tests | Build, package, verify, stage, activate, rollback, forward repair, restore, recover, and deprecate | Artifact or Release Set | Lifecycle and release claim |
| Offline tests | Declared local capabilities, bounded queues, no silent fallback, controlled import, and reconnection | Profile and component offline envelope | Offline capability claim |
| Performance and resource tests | Idle use, representative load, pressure, concurrency, storage growth, queueing, and recovery capacity | Hardware envelope and workload | Capacity or performance claim |
| Reproducibility tests | Clean independent builds from the same source, locks, configuration, and toolchain identities | Build inputs and produced artifacts | Reproducibility claim |

Each test level has a different authority scope. Passing unit tests cannot replace profile, activation, recovery, or release tests.

### 4.3 Gate model

| Gate | Minimum validation | Exact subject | Authority produced |
| --- | --- | --- | --- |
| Developer feedback | Workspace-local formatting, linting, focused unit tests, and selected contract checks | Developer workspace | No release or profile authority |
| Workspace validation | Frozen dependencies, full unit and contract suite, isolated services, integration tests, static validation | One recorded workspace | Supports a workspace validation result |
| Merge validation | Required repository checks, impact analysis, affected component and profile tests, evidence completeness | Proposed source revision | Supports merge eligibility |
| Candidate build | Clean build worker, locked inputs, complete build, packaging, SBOM and provenance when required | Candidate artifact set | Creates candidate artifacts only |
| Release validation | Compatibility, security, supported profiles, activation, rollback, recovery, offline, and release-set checks | Complete release candidate | Supports release approval when evidence is valid |
| Activation validation | Target validation, non-partial activation, health, readiness, receipt, and recovery point | Target deployment | Supports activation outcome only |

A gate does not promote itself. The release or merge workflow consumes valid evidence and makes the applicable decision through its canonical authority.

### 4.4 Execution context

Every execution records enough context to reproduce or invalidate the result:

- source revision and repository state;
- workspace or clean-worker identity;
- active profile and overlays;
- operating system, architecture, kernel, distribution, or worker image;
- toolchain and runtime versions;
- dependency declarations and lock identities;
- container images or native environment identity;
- component and service versions;
- fixtures and dataset identities;
- connectivity state;
- hardware and resource envelope;
- concurrency and scheduling;
- configuration, feature flags, and relevant policy references;
- test start, completion, timeout, and result.

Unrecorded material input makes a reproducibility, profile, or release claim incomplete.

### 4.5 Test result model

Registered outcomes include:

- `passed`;
- `failed`;
- `blocked`;
- `error`;
- `not_applicable`.

A skipped execution is not automatically `not_applicable`. Applicability is determined by the registered test and exact subject.

A retry may produce a new evidence record. It does not rewrite or hide the earlier result.

### 4.6 Static validation

Static validation evaluates authoritative structure before runtime behavior.

It includes applicable checks for:

- JSON and schema validity;
- canonical-reference resolution;
- unique identifiers;
- accepted decisions;
- active requirements;
- lock conformance;
- canonical ownership;
- generated-content alignment;
- profile composition;
- component boundaries;
- release and artifact compatibility declarations;
- English-only active content;
- absence of unresolved markers;
- traceability completeness.

A static pass does not replace runtime tests.

### 4.7 Dynamic validation

Dynamic validation executes behavior in an isolated environment.

Mutating tests use disposable, restored, or workspace-owned data. Cross-component tests use declared interfaces. Security tests do not create hidden privilege paths. Offline tests disable or constrain connectivity explicitly. Pressure tests preserve data integrity and unrelated operation.

### 4.8 Build model

A build consumes:

- committed source;
- committed dependency declarations and lockfiles;
- registered toolchain and native environment identities;
- declared build configuration;
- registered external or vendored source artifacts;
- bounded credentials when required;
- a clean isolated workspace or worker.

The build produces candidate artifacts and supporting outputs. Build success does not itself activate, publish, or approve the artifact.

### 4.9 Evidence model

A test-evidence record includes the fields required by `schemas/test-evidence.schema.json`:

- evidence identity and type;
- status, language, and recording time;
- subject;
- registered test reference;
- execution;
- environment;
- result;
- assertion results;
- produced or referenced artifacts;
- provenance;
- integrity;
- signing;
- validity;
- traceability.

Evidence may be active, invalidated, superseded, expired, or archived. Only valid active evidence supports a current claim.

### 4.10 AI boundary

ChatGPT may help a user draft test ideas, explain failures, or produce candidate code. Such output is not a test result, conformance judgment, policy decision, release gate, or evidence-validity decision.

Suno, Gamma, and the Ariane voice adapter have no build or validation authority.

All authoritative results come from registered deterministic validation and the applicable owning workflow.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-DEV-BTV-001,REQ-DEV-BTV-002,REQ-DEV-BTV-003,REQ-DEV-BTV-004,REQ-DEV-BTV-005,REQ-DEV-BTV-006,REQ-DEV-BTV-007,REQ-DEV-BTV-008,REQ-DEV-BTV-009,REQ-DEV-BTV-010,REQ-DEV-BTV-011,REQ-DEV-BTV-012,REQ-DEV-BTV-013,REQ-DEV-BTV-014,REQ-DEV-BTV-015,REQ-DEV-BTV-016,REQ-DEV-BTV-017,REQ-DEV-BTV-018,REQ-DEV-BTV-019,REQ-DEV-BTV-020,REQ-DEV-BTV-021,REQ-DEV-BTV-022,REQ-DEV-BTV-023,REQ-DEV-BTV-024 -->
- **REQ-DEV-BTV-001 — SHALL:** Every build, test, and validation execution shall identify one source revision, one workspace or clean worker, one active profile context, one declared toolchain set, and one dependency lock state.
- **REQ-DEV-BTV-002 — SHALL:** A reproducible validation run shall begin from a clean or verified isolated environment and shall install dependencies from committed frozen lock state.
- **REQ-DEV-BTV-003 — SHALL NOT:** A test or build shall rely on undeclared host packages, user-site dependencies, sibling workspaces, shared mutable environments, hidden credentials, editor state, or unrecorded service state.
- **REQ-DEV-BTV-004 — SHALL:** Each validation job shall declare its test identifier, subject, purpose, inputs, preconditions, assertions, environment, timeout, resource envelope, expected outcomes, produced artifacts, and evidence policy.
- **REQ-DEV-BTV-005 — SHALL:** Tests that mutate persistent state shall run only against workspace-scoped, disposable, restored, or explicitly isolated targets.
- **REQ-DEV-BTV-006 — SHALL NOT:** A development or test job shall write directly to another component's authoritative source tables or another workspace's mutable state.
- **REQ-DEV-BTV-007 — SHALL:** Test fixtures, seeds, clocks, random inputs, network dependencies, external endpoints, and concurrency settings shall be fixed, recorded, or explicitly classified as nondeterministic.
- **REQ-DEV-BTV-008 — SHALL:** A flaky, quarantined, skipped, blocked, errored, or nondeterministic test shall not count as passing evidence for an active conformance or release claim.
- **REQ-DEV-BTV-009 — SHALL:** Every failing assertion shall identify the tested requirement or contract condition, the observed result, the expected result, and the smallest reproducible evidence available.
- **REQ-DEV-BTV-010 — SHALL:** Static validation shall include applicable schema, reference, ownership, decision-closure, requirement-uniqueness, lock, generated-content, language, unresolved-state, migration, and traceability checks.
- **REQ-DEV-BTV-011 — SHALL:** Dynamic validation shall include applicable unit, contract, integration, component, profile, security, lifecycle, offline, recovery, performance, and resource-envelope tests.
- **REQ-DEV-BTV-012 — SHALL:** Cross-component tests shall use declared APIs, commands, events, gateways, artifacts, or read models and shall verify retained authority boundaries.
- **REQ-DEV-BTV-013 — SHALL:** Profile validation shall test the exact primary profile, overlays, component set, connectivity state, hardware envelope, implementation choices, and declared capability claims.
- **REQ-DEV-BTV-014 — SHALL:** Build outputs used beyond local development shall be produced from committed source and locked inputs and shall record toolchain, worker, source, dependency, configuration, and artifact identities.
- **REQ-DEV-BTV-015 — SHALL:** Release-authoritative builds shall run in an approved clean build-farm or equivalent release-authorized environment.
- **REQ-DEV-BTV-016 — SHALL NOT:** A successful developer-workstation or WSL build shall by itself establish release authority, sovereign Linux conformance, profile conformance, or reproducibility.
- **REQ-DEV-BTV-017 — SHALL:** A release candidate shall pass all applicable compatibility, integrity, signature, activation, rollback, forward-repair, restore, recovery, offline, and supported-profile gates before activation.
- **REQ-DEV-BTV-018 — SHALL NOT:** A failed, blocked, incomplete, expired, invalidated, superseded, or missing evidence record shall support an active release or conformance claim.
- **REQ-DEV-BTV-019 — SHALL:** Test evidence shall conform to `schemas/test-evidence.schema.json` and shall record subject, test, execution, environment, result, assertions, artifacts, provenance, integrity, signing, validity, and traceability.
- **REQ-DEV-BTV-020 — SHALL:** Evidence validity shall identify its scope, supporting environment, applicable profile and artifact versions, validity interval or invalidation conditions, and supersession relationships.
- **REQ-DEV-BTV-021 — SHALL:** A semantic source, contract, profile, toolchain, dependency, artifact, test, or environment change shall invalidate or trigger review of dependent evidence according to traceability and impact analysis.
- **REQ-DEV-BTV-022 — SHALL:** Resource Governor shall bound build and test CPU, memory, I/O, storage, concurrency, queues, execution time, logs, temporary artifacts, and retained evidence.
- **REQ-DEV-BTV-023 — SHALL NOT:** Native or external AI output shall be accepted as a test result, policy decision, conformance judgment, release gate, or evidence-validity decision without deterministic registered validation and authoritative acceptance.
- **REQ-DEV-BTV-024 — SHALL:** Every active build, validation, profile, reproducibility, conformance, and release claim shall be traceable to accepted decisions, active requirements, applicable locks, registered tests, and valid evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Developer feedback run

1. Resolve the workspace and source revision.
2. synchronize locked dependencies;
3. start only required isolated services;
4. run selected formatting, linting, unit, contract, or focused integration checks;
5. preserve output and diagnostics;
6. label the result as local developer feedback;
7. stop test-only services and clean disposable state.

This procedure does not create profile or release evidence unless the registered test and evidence requirements are also satisfied.

### 6.2 Full workspace validation

1. Record workspace, profile, source, runtime, toolchain, lock, container, service, and resource identities.
2. verify workspace isolation;
3. run frozen dependency synchronization; for Python, use `uv sync --frozen`;
4. run static repository and contract validation;
5. run the full applicable unit and contract suites;
6. start isolated service dependencies;
7. run applicable integration and component tests;
8. run affected profile and cross-platform tests;
9. collect logs, reports, and artifacts;
10. produce registered evidence for tests that require it;
11. stop services and verify cleanup.

### 6.3 Merge validation

1. Resolve the proposed revision and target branch.
2. compute direct and transitive impact;
3. resolve affected requirements, locks, profiles, components, artifacts, tests, and evidence;
4. execute required static checks;
5. execute all affected dynamic tests;
6. verify generated projections;
7. verify traceability and evidence completeness;
8. classify unresolved failures, blocks, skips, and invalid evidence;
9. block merge until required dispositions and gates pass.

### 6.4 Clean candidate build

1. Select an approved clean worker.
2. record worker, operating-system, toolchain, runtime, and image identities;
3. fetch or materialize the committed source revision;
4. verify declarations and frozen lock state;
5. install dependencies without prior mutable workspace state;
6. execute the complete build;
7. package candidate artifacts;
8. produce SBOM and provenance when required;
9. compute release-artifact integrity values where required;
10. run build-output validation;
11. register candidate artifacts and evidence without activating them.

### 6.5 Reproducibility validation

1. Select two independently clean workers or equivalent isolated executions.
2. use the same committed source, locks, build configuration, toolchain identity, and declared external inputs;
3. build independently;
4. compare canonical artifact content or the artifact-class reproducibility representation;
5. investigate any difference through recorded provenance;
6. register passed or failed reproducibility evidence;
7. block the reproducibility claim when material differences remain.

### 6.6 Release validation

1. Resolve the complete candidate Release Set.
2. verify channel membership and compatibility;
3. verify artifact schemas, manifests, integrity, signatures, provenance, SBOMs, and policy conditions;
4. run supported-profile tests;
5. run security and supply-chain tests;
6. run offline behavior tests where claimed;
7. run activation, rollback, forward-repair, restore, and recovery tests;
8. run performance and resource-envelope regression tests;
9. verify all required evidence is active and valid;
10. produce the release-gate result through the owning release workflow.

### 6.7 Evidence creation

1. Select the registered test and exact subject.
2. collect execution and environment identity;
3. record each assertion result;
4. attach or reference produced artifacts;
5. record provenance;
6. apply integrity and signing rules;
7. state validity scope and invalidation conditions;
8. link decisions, requirements, locks, profiles, components, artifacts, and release candidates;
9. validate against `schemas/test-evidence.schema.json`;
10. register the evidence.

### 6.8 Evidence invalidation or supersession

1. Detect a material source, contract, profile, toolchain, environment, artifact, test, or validity change.
2. compute impacted claims and evidence;
3. classify each evidence record as still valid, review required, invalidated, expired, or superseded;
4. preserve historical lineage;
5. remove invalid evidence from active claim support;
6. rerun affected tests;
7. register replacement evidence;
8. update traceability and release-gate state.

## 7. Failure States and Safe Degradation

| Failure state | Required behavior | Preserved state | Blocked behavior or claim |
| --- | --- | --- | --- |
| Environment identity incomplete | Block reproducibility, profile, and release claims. | Raw test output as local information | Authoritative evidence |
| Dirty or shared mutable environment | Recreate the job in a clean isolated environment. | Source revision and committed locks | Isolation and reproducibility claims |
| Dependency lock changes during validation | Fail the job and retain the original committed lock state. | Previous valid dependency graph | Frozen-validation result |
| Test timeout | Record `blocked`, `error`, or `failed` according to the registered test contract. | Completed independent assertions | Passing result |
| Flaky or nondeterministic result | Quarantine the test and block dependent claims. | Other valid tests | Pass-by-retry interpretation |
| Fixture or service isolation failure | Stop the affected test and preserve other workspaces. | Unrelated workspace state | Cross-workspace result |
| Required test skipped | Block the affected gate unless the registered test marks the case not applicable for the exact subject. | Other completed results | Complete gate claim |
| Evidence schema failure | Reject the evidence record. | Underlying logs and artifacts as non-authoritative material | Evidence-backed claim |
| Evidence expired, invalidated, or superseded | Remove it from active claim support and rerun or replace it. | Historical traceability | Current claim |
| Build artifact differs between clean workers | Fail reproducibility and investigate all material inputs. | Both candidate outputs and provenance | Reproducibility claim |
| Artifact validation or signature failure | Quarantine the candidate and preserve the previous valid release. | Existing valid release | Activation |
| Activation, rollback, or recovery test fails | Block release approval for the affected artifact class or profile. | Previous valid release evidence | Release gate |
| Resource pressure | Reduce concurrency, defer noncritical tests, preserve active-job integrity, logs, evidence, and operator control. | Completed valid results | New heavy jobs |
| External service unavailable | Skip only tests whose registered subject is that optional external capability and preserve unrelated local validation. | Core local tests | Silent provider substitution |

Validation failure preserves the last valid source, artifact, profile, release, and evidence state. It does not authorize an inferred pass, silent skip, provider substitution, or partial activation.

## 8. Cross-Component Interactions

| Producer or owner | Consumer | Interaction | Boundary |
| --- | --- | --- | --- |
| Source repository | Build and test worker | Committed source revision and declarations | Worker cannot silently modify authoritative source |
| Toolchain contract | Workspace or worker | Runtime, dependency, build, and validation commands | Recipe or host preference cannot redefine the toolchain |
| Workspace manager | Test job | Isolated dependencies, services, ports, volumes, secrets, databases, and resources | Test cannot mutate another workspace |
| Test catalog | Test runner | Test identity, subject, applicability, assertions, timeout, outputs, and evidence policy | Runner cannot redefine pass criteria |
| Component contract | Contract and component tests | Interfaces, states, authority, failures, and recovery | Test must preserve component boundaries |
| Profile contract | Profile test suite | Composition, capabilities, hardware, connectivity, security, and implementation choices | One profile result cannot support another profile |
| Resource Governor | Build and test scheduler | CPU, memory, I/O, concurrency, queue, and storage limits | Resource control does not decide test meaning |
| Governance Policy Runtime | Security or governed tests | Authorization, disclosure, consent, privilege, and exception decisions | Test runner cannot invent policy |
| Build farm | Release workflow | Candidate artifacts, SBOM, provenance, tests, and evidence | Build output remains a candidate until release approval |
| Evidence producer | Evidence registry | Validated test-evidence record | Registration does not change the test result |
| Traceability registry | Merge and release gates | Claim-to-test-and-evidence relationships | Missing links block the claim |
| kOA Node Agent | Activation and recovery tests | Target validation, activation, rollback, recovery, and receipts | Node Agent does not create release authority |
| Audit Broker | Evidence and release workflows | Selective receipts and evidence disclosure | Audit visibility does not alter source or release authority |
| External AI surface | User | Candidate assistance only | Output has no test, policy, conformance, or release authority |

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Closed question |
| --- | --- |
| `DEC-DEV-001` | Development workspaces use isolated mutable environments and reproducible frozen dependency synchronization. |
| `DEC-DEV-002` | Parallel branches and applications use stable workspace identities and isolated namespaces. |
| `DEC-PROFILE-001` | Tests and claims apply through explicit primary profiles and compatible overlays. |
| `DEC-CONTAINER-001` | Runtime-specific implementation choices do not change application test authority. |
| `DEC-DATA-001` | Test infrastructure cannot write another component's authoritative source tables. |
| `DEC-GOV-001` | Resource control and policy authority remain separate during testing. |
| `DEC-HW-001` | Capacity claims use profile-specific hardware envelopes and measured evidence. |
| `DEC-REL-001` | Release channels, Release Sets, compatibility, non-partial activation, receipts, and recovery govern release validation. |
| `DEC-AI-001` | External AI output remains candidate input and native AI has no validation authority. |

### Prohibited assumptions

- A green local command is release evidence.
- A WSL build proves native sovereign Linux behavior.
- A developer workstation proves the build-farm environment.
- Passing unit tests proves component, profile, security, lifecycle, or offline conformance.
- A skipped test is passing.
- A retry erases a prior failure.
- A flaky test may pass by majority vote.
- A moving container tag is a reproducible environment identity.
- Cached build output proves a clean build.
- An unrecorded service or database state is an acceptable fixture.
- A test may use another workspace's mutable environment.
- Test code may write another component's source tables.
- A valid signature proves compatibility or correct behavior.
- An SBOM proves reproducibility, security, or activation.
- Evidence remains valid after material inputs change automatically.
- Expired or superseded evidence can support a current claim.
- A candidate artifact is approved because it was produced by the build farm.
- Release approval implies successful target activation.
- ChatGPT analysis is a conformance decision.
- Missing tests or evidence may be replaced by engineering confidence.

## 10. Validation Criteria

1. The metadata block parses as JSON and declares `DOC-DEV-014`, status `active`, language `en`, development layer, and the three declared profile scopes.
2. All eleven required sections exist in numerical order.
3. Every decision ID is accepted in `generated/decision-index.json`.
4. Every requirement ID appears exactly once in `generated/requirements-index.json`.
5. Every lock ID resolves to an active lock.
6. `TEST-DEV-BTV-001` verifies complete source, workspace or worker, profile, toolchain, and lock identity.
7. `TEST-DEV-BTV-002` verifies clean isolated build and test environments.
8. `TEST-DEV-BTV-003` detects undeclared host, user, sibling-workspace, editor, credential, and service dependencies.
9. `TEST-DEV-BTV-004` verifies complete registered test definitions and execution context.
10. `TEST-DEV-BTV-005` verifies disposable or workspace-owned persistent test state.
11. `TEST-DEV-BTV-006` rejects cross-component source-table and cross-workspace writes.
12. `TEST-DEV-BTV-007` verifies deterministic or explicitly classified fixtures, clocks, randomness, network, and concurrency.
13. `TEST-DEV-BTV-008` verifies that flaky, skipped, blocked, errored, and nondeterministic tests do not support passing claims.
14. `TEST-DEV-BTV-009` verifies complete failing-assertion diagnostics.
15. `TEST-DEV-BTV-010` verifies the full applicable static validation suite.
16. `TEST-DEV-BTV-011` verifies the applicable dynamic validation levels.
17. `TEST-DEV-BTV-012` verifies declared cross-component interfaces and authority boundaries.
18. `TEST-DEV-BTV-013` verifies exact profile, overlay, component, connectivity, hardware, and implementation context.
19. `TEST-DEV-BTV-014` verifies clean candidate builds from committed locked inputs with complete identities.
20. `TEST-DEV-BTV-015` verifies build-farm or equivalent release-authorized execution.
21. `TEST-DEV-BTV-016` verifies that workstation and WSL results do not claim release or sovereign authority.
22. `TEST-DEV-BTV-017` verifies compatibility, integrity, signature, activation, rollback, repair, restore, recovery, offline, and profile release gates.
23. `TEST-DEV-BTV-018` verifies `schemas/test-evidence.schema.json`, evidence status, validity, supersession, and traceability.
24. `TEST-DEV-BTV-019` verifies evidence invalidation after material source, contract, profile, toolchain, dependency, artifact, test, or environment changes.
25. `TEST-DEV-BTV-020` verifies bounded build and test resources and safe pressure degradation.
26. Active prose is English and contains no unresolved marker, placeholder, metadata hash, or source hash.
27. The generated requirement block matches the canonical requirement registry.
28. Every active claim resolves to registered tests and valid evidence.

These criteria define validation requirements. They do not claim that a particular repository revision, workspace, build, artifact, profile, or release already conforms.

## 11. Non-Normative Examples

> **Non-normative example:** A developer runs focused unit tests in a workspace. The result provides immediate feedback. The merge gate later runs frozen dependency synchronization, static validation, the full contract suite, and affected integration tests in a recorded clean job.

> **Non-normative example:** The same source revision builds successfully in WSL and on a Linux developer workstation. The release contract requires clean build-farm evidence, so neither local result is release-authoritative.

> **Non-normative example:** An integration test starts isolated PostgreSQL, queue, and service dependencies for one workspace. It creates fixtures in workspace-specific databases and removes them after the test. Another branch remains operational throughout.

> **Non-normative example:** A recovery test activates a candidate artifact in an isolated target, forces the declared failure, executes rollback, verifies the previous valid state, and records the activation and rollback receipts.

> **Non-normative example:** A security dependency changes after evidence was recorded. Impact analysis marks affected security, build, and release evidence for review. The old evidence remains historical but no longer supports the new candidate automatically.

> **Non-normative example:** ChatGPT suggests an additional edge case for a parser. A developer adds it to the registered deterministic test suite. The executed test and validated evidence, not the suggestion, support the resulting claim.
