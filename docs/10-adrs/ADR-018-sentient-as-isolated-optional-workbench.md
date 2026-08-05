<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "ADR-018",
  "document_class": "architecture_decision_record",
  "status": "active",
  "adr_status": "accepted",
  "language": "en",
  "layer": "architecture_decisions",
  "scope": [
    "global",
    "development",
    "build"
  ],
  "decision_date": "2026-08-03",
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/ai_model",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/profiles/developer-linux-workstation.profile.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "contracts/profiles/build-farm.profile.json",
    "contracts/integration-types.contract.json",
    "contracts/artifact-classes.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-SENT-001",
    "DEC-SYS-AI-001",
    "DEC-SYS-COMP-001",
    "DEC-PROFILE-001",
    "DEC-PROFILE-002",
    "DEC-DEV-001",
    "DEC-INT-001"
  ],
  "requirement_ids": [
    "REQ-SENT-001",
    "REQ-SENT-002",
    "REQ-SENT-003",
    "REQ-SENT-004",
    "REQ-SENT-005",
    "REQ-SENT-006",
    "REQ-SENT-007",
    "REQ-SENT-008",
    "REQ-SENT-009",
    "REQ-SENT-010",
    "REQ-SENT-011",
    "REQ-SENT-012",
    "REQ-SENT-013",
    "REQ-SENT-014",
    "REQ-SENT-015",
    "REQ-SENT-016",
    "REQ-SENT-017",
    "REQ-SENT-018",
    "REQ-SENT-019",
    "REQ-SENT-020",
    "REQ-SENT-021",
    "REQ-SENT-022",
    "REQ-SENT-023",
    "REQ-SENT-024",
    "REQ-SENT-025",
    "REQ-SENT-026",
    "REQ-SENT-027",
    "REQ-SENT-028",
    "REQ-SENT-029",
    "REQ-SENT-030",
    "REQ-SENT-031",
    "REQ-SENT-032",
    "REQ-SENT-033",
    "REQ-SENT-034",
    "REQ-SENT-035",
    "REQ-SENT-036",
    "REQ-SENT-037",
    "REQ-SENT-038",
    "REQ-SENT-039",
    "REQ-SENT-040"
  ],
  "lock_ids": [
    "LOCK-SENT-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-DEV-001",
    "LOCK-DEV-002",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DEV-005",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-003",
    "DOC-GOV-004",
    "DOC-GOV-005",
    "DOC-GOV-006",
    "DOC-GOV-007",
    "DOC-GOV-008",
    "DOC-CONST-002",
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-SYS-000",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-006",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-010",
    "DOC-SYS-011",
    "DOC-SYS-012",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-016",
    "DOC-SYS-017",
    "DOC-SYS-018",
    "DOC-SYS-019",
    "DOC-PROFILE-001",
    "DOC-PROFILE-002",
    "DOC-COMP-000",
    "DOC-COMP-001",
    "DOC-DEV-000",
    "DOC-SEC-005",
    "DOC-SEC-006",
    "DOC-SEC-016",
    "DOC-CONF-003",
    "DOC-CONF-013",
    "DOC-CONF-019"
  ],
  "supersedes": [],
  "superseded_by": [],
  "tags": [
    "adr",
    "sentient",
    "optional-workbench",
    "isolated",
    "non-authoritative",
    "development",
    "build",
    "ai-boundary",
    "candidate-artifacts",
    "removable",
    "accepted-decision"
  ]
}
KOA:DOC-META:END -->

# ADR-018: SenTient as an Isolated Optional Workbench

## 1. Status

**Accepted**

Decision date: **2026-08-03**

This ADR records the accepted architectural decision that SenTient is an optional, isolated, non-authoritative workbench.

SenTient can support development, build, experimentation, evaluation, candidate generation, and analysis. It is not part of the mandatory kOA runtime baseline and is not an authority for identity, governance, data ownership, publication, release, security, recovery, or conformance.

The machine-readable system, profile, component, integration, requirement, and lock registries own the active facts. This ADR records the rationale, consequences, and rejected alternatives behind those facts.

## 2. Context

kOA benefits from a bounded environment in which developers and build workflows can experiment with:

- local models;
- analytical pipelines;
- code generation;
- evaluation harnesses;
- indexing strategies;
- model and prompt comparisons;
- candidate configuration;
- candidate documentation;
- candidate component artifacts;
- reproducibility and benchmark work.

Such a workbench can improve development velocity and make experimental work more observable.

Embedding the workbench into the core runtime would create unacceptable coupling.

A required AI or model workbench could make core startup depend on:

- large model artifacts;
- accelerated hardware;
- mutable model caches;
- external providers;
- experimental dependencies;
- privileged devices;
- high resource consumption;
- non-deterministic behavior;
- rapidly changing toolchains.

It could also blur authority boundaries. Model output could be mistaken for a decision, policy, publication, release approval, migration plan, or conformance result.

A shared mutable workbench could cross component boundaries by reading databases directly, sharing queues or indexes, or writing generated content into authoritative stores.

The architecture therefore needs a place for experimentation that does not become a hidden runtime dependency or a route around ordinary governance.

## 3. Decision

SenTient is implemented and governed as:

```text
optional
isolated
disabled_by_default
development_or_build_scoped
non_authoritative
candidate_output_only
resource_bounded
removable
```

SenTient is available only in explicitly compatible development or build profiles.

It is not part of:

- core user operation;
- sovereign runtime authority;
- control-plane authority;
- high-assurance runtime authority;
- appliance operation;
- disaster-recovery authority;
- publication authority;
- release-signing authority.

A SenTient workflow begins with an explicit user or authorized local trigger.

The workflow selects bounded inputs through registered interfaces or controlled exports, executes inside isolated workbench resources, records provenance, and emits candidate outputs.

Those outputs enter the same ordinary validation and acceptance paths as equivalent outputs produced by a human, build tool, deterministic generator, or approved external AI surface.

Local hosting does not make SenTient authoritative.

Deterministic output does not make SenTient authoritative.

High benchmark performance does not make SenTient authoritative.

## 4. Isolation and Authority Boundaries

### 4.1 Runtime isolation

SenTient uses isolated:

- process identities;
- service identities;
- workspaces;
- virtual environments;
- containers where applicable;
- networks;
- volumes;
- databases and schemas;
- queues and topics;
- consumer groups;
- indexes;
- caches;
- object prefixes;
- temporary storage;
- generated-artifact roots.

No ordinary SenTient path shares mutable authoritative state with another component.

### 4.2 Data boundary

SenTient can receive data through:

- registered component APIs;
- controlled exports;
- candidate artifacts;
- governed references;
- synthetic or approved test data;
- protected context workflows where explicitly authorized.

It cannot read another component's database or filesystem directly merely because the workbench runs on the same host.

### 4.3 Write boundary

SenTient can write only to:

- its isolated mutable state;
- its isolated caches and indexes;
- candidate artifact storage;
- workbench evidence storage;
- explicitly registered output interfaces.

It cannot write directly to:

- canonical registries;
- accepted decisions;
- requirements or locks;
- profile contracts;
- component contracts;
- active policy stores;
- component authoritative databases;
- Publication Gateway destination state;
- Audit Broker protected stores;
- active Release Set pointers.

### 4.4 Authority separation

| Responsibility | Owner |
| --- | --- |
| User, service, node, signer, key, and artifact identity | Identity and Trust |
| Authorization and obligations | Governance Policy Runtime or another registered authority |
| Resource admission | Resource Governor |
| Privileged host effects | kOA Node Agent |
| Source business data | Owning component |
| Public disclosure | Publication Gateway |
| Audit and protected evidence | Audit Broker |
| Release compatibility and approval | Release-channel and release authorities |
| SenTient experiment state | SenTient workbench |
| Acceptance of a candidate output | Owning local workflow |

SenTient can propose. It cannot accept its own proposal into authority.

### 4.5 Privilege boundary

SenTient runs without general administrator, root, privileged-container, device-management, container-daemon, package-manager, signing, or publication privilege.

A workbench operation needing a registered host effect uses the ordinary bounded privileged-broker workflow and remains subject to profile and policy restrictions.

### 4.6 Network boundary

Network access is disabled by default.

An enabled path is:

- integration-specific;
- destination-bound;
- purpose-bound;
- authenticated;
- data-minimized;
- rate- and cost-bounded;
- observable;
- removable.

SenTient exposes no public management listener.

## 5. Inputs, Outputs, and Acceptance

### 5.1 Input selection

Every input selection identifies:

```text
workflow_id
purpose
requesting_identity
source_owner
source_refs
data_classes
selected_fields
classification
retention
expiry
integration_refs
authority_refs
```

The workbench does not treat repository visibility or host access as data permission.

### 5.2 Candidate outputs

Output classes can include:

```text
candidate_code
candidate_documentation
candidate_configuration
candidate_model
candidate_dataset
candidate_index
candidate_test
candidate_evaluation
candidate_artifact
candidate_change_request
analysis_report
experiment_result
```

Every output remains non-authoritative until the owning workflow accepts it through its ordinary process.

### 5.3 Provenance

Provenance records:

- input source references;
- input selection;
- source revisions;
- model identities and versions;
- dependency and toolchain versions;
- prompts or configuration where policy permits;
- execution environment;
- transformations;
- evaluations;
- producing identity;
- time;
- output references;
- limitations;
- acceptance state.

### 5.4 Validation

A candidate uses the same validators as an equivalent non-SenTient artifact.

Examples include:

- source and dependency validation;
- schema validation;
- type and static checks;
- unit and contract tests;
- component-boundary checks;
- profile checks;
- artifact-contract checks;
- AI-boundary checks;
- security checks;
- secret scanning;
- reproducibility checks;
- release gates;
- human review.

The candidate source does not weaken a gate.

### 5.5 Acceptance

Acceptance requires an authority outside SenTient.

The accepting workflow records:

- candidate identity;
- owning component or authority;
- intended artifact or change class;
- validation result;
- test and evidence references;
- reviewer or decision authority;
- accepted version;
- destination;
- resulting lifecycle state.

Rejection leaves the candidate non-authoritative.

### 5.6 External AI surfaces

A SenTient workflow can use only the approved external surfaces:

```text
chatgpt
suno
gamma
approved_ariane_voice_adapter
```

Use of those surfaces remains a controlled export and reimport operation.

An external provider does not gain access to SenTient's full workspace, source stores, secret stores, or protected proof by default.

## 6. Resource, Lifecycle, and Failure Model

### 6.1 Resource envelope

The active profile owns:

- CPU limits;
- memory limits;
- accelerator access;
- storage limits;
- I/O limits;
- network limits;
- queue bounds;
- concurrency;
- scheduling priority;
- cache limits;
- maximum experiment duration.

Resource Governor enforces the declared envelope.

Core services and recovery reserves have priority over workbench activity.

### 6.2 Activation

Activation requires:

- a compatible profile;
- explicit enablement;
- validated workbench artifacts;
- isolated namespaces;
- resource admission;
- integration configuration;
- managed secret references;
- logging and evidence;
- cleanup policy.

Activation does not create core-service dependency.

### 6.3 Normal work states

Work items use states such as:

```text
created
admitted
running
paused
cancelled
completed
failed
quarantined
expired
retired
```

Candidate output lifecycle remains separate from work-item lifecycle.

### 6.4 Failure behavior

| Failure | Required behavior |
| --- | --- |
| SenTient unavailable | Core kOA behavior continues. |
| Model artifact missing | Block the affected work item only. |
| Workbench dependency invalid | Block activation or the affected work item. |
| Resource admission denied | Defer or reject workbench work. |
| Network unavailable | Continue local eligible work or block the external step. |
| External provider unavailable | Preserve local state and report the bounded failure. |
| Input authority invalid | Reject the input selection. |
| Secret detected | Quarantine the affected input or output. |
| Candidate validation fails | Keep the output non-authoritative. |
| Output destination rejects import | Preserve the candidate and rejection evidence. |
| Work item outcome unknown | Reconcile isolated workbench state before retry. |
| Cache corruption | Rebuild or discard the isolated cache. |
| Workbench database corruption | Restore or recreate workbench state without affecting core stores. |
| SenTient removal | Core services and canonical authority remain intact. |

### 6.5 Offline behavior

SenTient can operate offline when its profile provides local:

- models;
- dependencies;
- source inputs;
- toolchain;
- validation tools;
- resource capacity;
- trust material;
- candidate storage.

Offline operation does not require or emulate an external provider.

### 6.6 Removal

Removal includes:

1. stop or cancel active work;
2. preserve required candidate provenance and evidence;
3. revoke workbench credentials;
4. disable integrations;
5. remove workbench service identities where appropriate;
6. delete or retire isolated mutable state;
7. remove optional model and cache artifacts;
8. verify core startup and operation;
9. create a removal receipt.

Removal does not mutate another component's state.

## 7. Consequences

### 7.1 Positive consequences

The decision provides:

- a safe place for experimentation;
- optional local model use;
- reproducible candidate generation;
- clear provenance;
- profile-scoped resource control;
- no core dependency;
- no implicit authority;
- no direct component-store writes;
- clean removal;
- offline-capable local experimentation;
- compatibility with controlled external AI surfaces;
- a consistent validation path for human-, tool-, and model-produced candidates.

### 7.2 Costs

The decision requires:

- duplicate isolated storage and caches;
- explicit data export and import;
- provenance records;
- candidate lifecycle management;
- profile-specific setup;
- resource admission;
- cleanup;
- integration registration;
- repeated validation outside the workbench.

These costs are intentional. They preserve component and authority boundaries.

### 7.3 Development implications

Developers can use SenTient for analysis and candidate work without making it a hidden prerequisite.

A developer workspace remains valid when SenTient is absent.

A successful experiment does not create a production claim.

### 7.4 Build implications

Build-farm use remains bounded to workbench or candidate stages unless a distinct registered build operation accepts the output.

Production signing and release approval remain outside SenTient.

### 7.5 Operations implications

Operations do not monitor SenTient as a core service unless the active development or build profile explicitly declares a workbench SLO.

Failure of such an SLO does not imply failure of core runtime capabilities.

### 7.6 Security implications

The strongest security property is removability.

A compromised or untrusted SenTient environment can be isolated and removed while preserving canonical authority, component data, release state, recovery state, and core operation.

## 8. Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Workbench output is mistaken for authority | Candidate-only artifact classes, external acceptance, labels, receipts, and gates |
| SenTient becomes a hidden core dependency | Default-off profile rules, core-without-SenTient tests, removability tests |
| Direct database access bypasses ownership | Registered APIs and exports only, isolated credentials, component-boundary tests |
| Resource starvation affects core services | Resource Governor admission, priority separation, hard limits, cancellation |
| Sensitive data enters prompts or artifacts | Data classification, minimization, secret scanning, protected-context workflow |
| External AI receives excessive data | Destination-bound controlled export and explicit integration contracts |
| Local hosting is treated as authority | Explicit non-authoritative classification independent of hosting location |
| Generated code bypasses review | Ordinary code, security, test, evidence, and release gates |
| Workbench state leaks across projects | Dedicated workspace, namespace, cache, queue, index, and storage identities |
| Privileged devices broaden authority | Profile allowlists and brokered bounded operations |
| Experiment cleanup deletes shared state | Positive ownership labels and workbench-only deletion scope |
| A benchmark becomes a release decision | Separate evaluation evidence and release authority |
| SenTient is installed in a sovereign runtime | Profile prohibition and conformance checks |
| Removal loses required provenance | Retention policy and removal receipt preserve accepted evidence references |

## 9. Alternatives Considered

### 9.1 SenTient as a mandatory core component

**Rejected.**

This would make startup, operation, recovery, resource planning, security, and offline continuity depend on an experimental workbench.

It would also weaken the native non-AI baseline.

### 9.2 SenTient as an authoritative AI subsystem

**Rejected.**

Model or workbench output cannot own identity, policy, data, publication, release, security, or conformance decisions.

### 9.3 SenTient embedded inside every component

**Rejected.**

Embedding it would duplicate heavy dependencies, obscure data boundaries, complicate removal, and create direct-write pressure.

### 9.4 SenTient with shared component databases

**Rejected.**

Shared mutable authority would violate component ownership and make cleanup or compromise containment unsafe.

### 9.5 SenTient with unrestricted host and network access

**Rejected.**

Broad access would turn a workbench into a privileged control surface and increase secret, data, and supply-chain risk.

### 9.6 SenTient as an external hosted service only

**Rejected.**

External hosting would make local development and offline work dependent on a provider and would not eliminate local authority and data-boundary requirements.

### 9.7 SenTient as a production sidecar

**Rejected.**

A production sidecar would create runtime dependency, resource coupling, and ambiguous operational authority.

### 9.8 No SenTient support

**Rejected.**

A governed optional workbench is preferable to unregistered local experimentation with weaker isolation, provenance, and cleanup.

## 10. Conformance and Reconsideration

### 10.1 Conformance conditions

This decision is correctly implemented when:

1. SenTient is optional and disabled by default;
2. only compatible development or build profiles can activate it;
3. core startup and operation pass without it;
4. service, workspace, network, storage, queue, index, cache, and artifact namespaces are isolated;
5. no direct cross-component authoritative-store access exists;
6. no canonical registry or active Release Set write exists;
7. every output is explicitly non-authoritative;
8. candidate provenance is complete;
9. acceptance occurs outside SenTient;
10. ordinary validators and release gates apply;
11. Resource Governor bounds workbench use;
12. privileged host effects use the ordinary narrow broker;
13. network access is default-off and integration-scoped;
14. secrets and protected content are controlled;
15. external AI surfaces remain the approved set;
16. SenTient is removable without core failure;
17. failure affects only workbench-scoped activity;
18. offline operation remains local and candidate-only;
19. deactivation and removal clean isolated state safely;
20. development and build claims expose explicit non-claims;
21. all profiles, components, integrations, artifacts, tests, evidence, receipts, and exceptions resolve;
22. no prohibited open-state marker enters active authority.

The principal validation entry point is:

```bash
uv run python docs/tools/validate_docs.py
```

Supporting checks include:

```text
docs/tools/check_ai_boundary.py
docs/tools/check_component_boundaries.py
docs/tools/check_profile_inheritance.py
docs/tools/check_artifact_contracts.py
docs/tools/check_interfile_locks.py
docs/tools/check_traceability.py
docs/tools/check_decision_closure.py
docs/tools/check_no_unresolved_state.py
```

### 10.2 Reconsideration triggers

This ADR can be reconsidered when:

- a future accepted system architecture defines an authoritative native AI capability with a distinct owner and proof model;
- a production profile needs a bounded analytical component that cannot be represented as an optional workbench;
- isolation technology cannot provide the declared data, resource, network, and privilege boundaries;
- repeated evidence shows that removability is not achievable;
- candidate provenance and acceptance cannot be made reliable;
- a new offline requirement needs a different local model lifecycle;
- SenTient ceases to be experimental and receives a separately governed component contract.

Reconsideration requires a new accepted ADR and canonical registry changes.

Existing decisions and evidence remain historically interpretable under this ADR.

## 11. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SENT-001,REQ-SENT-002,REQ-SENT-003,REQ-SENT-004,REQ-SENT-005,REQ-SENT-006,REQ-SENT-007,REQ-SENT-008,REQ-SENT-009,REQ-SENT-010,REQ-SENT-011,REQ-SENT-012,REQ-SENT-013,REQ-SENT-014,REQ-SENT-015,REQ-SENT-016,REQ-SENT-017,REQ-SENT-018,REQ-SENT-019,REQ-SENT-020,REQ-SENT-021,REQ-SENT-022,REQ-SENT-023,REQ-SENT-024,REQ-SENT-025,REQ-SENT-026,REQ-SENT-027,REQ-SENT-028,REQ-SENT-029,REQ-SENT-030,REQ-SENT-031,REQ-SENT-032,REQ-SENT-033,REQ-SENT-034,REQ-SENT-035,REQ-SENT-036,REQ-SENT-037,REQ-SENT-038,REQ-SENT-039,REQ-SENT-040 -->
- **REQ-SENT-001 — SHALL:** SenTient remain an optional isolated workbench rather than a required kOA runtime component.
- **REQ-SENT-002 — SHALL:** SenTient be disabled by default in every profile and activated only through an explicit profile-scoped development or build configuration.
- **REQ-SENT-003 — SHALL NOT:** SenTient be required for core startup, local navigation, identity, authorization, governance, audit, publication, accepted offline learning-content access, UCKK interchange, recovery, or offline continuity.
- **REQ-SENT-004 — SHALL:** SenTient activation be limited to explicitly compatible development or build profiles.
- **REQ-SENT-005 — SHALL NOT:** SenTient be activated in user-lightweight, sovereign runtime, control-plane, appliance, production operational, or recovery profiles unless a later accepted decision defines a distinct bounded profile.
- **REQ-SENT-006 — SHALL:** SenTient execute under a dedicated service or workspace identity with no inherited administrator, root, privileged-container, signing, publication, or release authority.
- **REQ-SENT-007 — SHALL:** SenTient use isolated compute, process, network, storage, queue, cache, index, model, and artifact namespaces.
- **REQ-SENT-008 — SHALL NOT:** SenTient share mutable authoritative state, databases, schemas, queues, topics, consumer identities, indexes, caches, object prefixes, or work directories with another component.
- **REQ-SENT-009 — SHALL:** Every input to SenTient use an explicit user or authorized workflow trigger, a declared purpose, selected source references, data classification, provenance, and retention.
- **REQ-SENT-010 — SHALL NOT:** SenTient receive unrestricted filesystem, database, message-bus, audit-store, private-proof, secret-store, or host access.
- **REQ-SENT-011 — SHALL:** SenTient access component-owned data only through registered APIs, controlled exports, candidate artifacts, or governed references.
- **REQ-SENT-012 — SHALL NOT:** SenTient write directly to another component's authoritative store or mutate canonical registries, accepted decisions, requirements, locks, policies, profiles, component contracts, or active Release Sets.
- **REQ-SENT-013 — SHALL:** Every SenTient output be classified as candidate, analysis, experiment result, evaluation result, model artifact, proposed change, or other explicitly non-authoritative artifact class.
- **REQ-SENT-014 — SHALL NOT:** A SenTient output become an accepted decision, release artifact, production configuration, policy, publication, conformance result, security finding, or recovery instruction without the ordinary local validation and acceptance path.
- **REQ-SENT-015 — SHALL:** SenTient outputs preserve source references, input selection, tool and model versions, configuration, execution environment, time, transformations, evaluations, and producing identity.
- **REQ-SENT-016 — SHALL:** Every candidate artifact intended for a release channel pass the same owner, schema, provenance, integrity, compatibility, test, evidence, approval, signing, and release-gate requirements as a candidate produced without SenTient.
- **REQ-SENT-017 — SHALL NOT:** Model confidence, benchmark score, experiment score, evaluator score, provider acknowledgement, or operator preference substitute for canonical validation.
- **REQ-SENT-018 — SHALL:** SenTient remain removable without preventing kOA core build, test, startup, operation, recovery, or conformance.
- **REQ-SENT-019 — SHALL:** The absence, failure, corruption, incompatibility, or deletion of SenTient preserve the last validated authoritative state and affect only workbench-scoped candidate activity.
- **REQ-SENT-020 — SHALL NOT:** SenTient failure trigger degradation of core user, governance, audit, security, publication, recovery, or offline capabilities.
- **REQ-SENT-021 — SHALL:** SenTient resource use be admitted and bounded by the Resource Governor according to the active development or build profile.
- **REQ-SENT-022 — SHALL NOT:** Resource availability or workbench ownership grant SenTient governance, authorization, disclosure, publication, cultural-rights, or data-ownership authority.
- **REQ-SENT-023 — SHALL:** SenTient network access be disabled by default and enabled only through registered destination-scoped integrations required by an approved experiment or build workflow.
- **REQ-SENT-024 — SHALL:** Every enabled SenTient integration declare endpoint, authentication, purpose, selected data, destination, retention, cost boundary, retry behavior, removal, provenance, and local acceptance.
- **REQ-SENT-025 — SHALL NOT:** SenTient expose a public listener, direct privileged-broker interface, unrestricted outbound network path, or provider-controlled command channel.
- **REQ-SENT-026 — SHALL:** SenTient use managed secret references and prevent secret values, raw private keys, credentials, unrestricted sensitive evidence, and protected personal or cultural content from entering ordinary logs, prompts, artifacts, metrics, or receipts.
- **REQ-SENT-027 — SHALL:** Protected input to SenTient require a distinct governed selection, explicit audience and purpose, current access authority, minimization, retention, expiry, export restrictions, and access receipts.
- **REQ-SENT-028 — SHALL:** SenTient native processing remain non-authoritative even when it is deterministic, locally hosted, disconnected, or operated entirely on kOA-owned hardware.
- **REQ-SENT-029 — SHALL:** External AI surfaces used by a SenTient workflow remain limited to ChatGPT, Suno, Gamma, and the approved Ariane voice adapter unless the integrations registry and an accepted decision authorize another surface.
- **REQ-SENT-030 — SHALL NOT:** SenTient route data to an external AI surface implicitly, automatically, or outside the controlled export and reimport boundary.
- **REQ-SENT-031 — SHALL:** Every SenTient experiment define success criteria, stop conditions, resource limits, data scope, output disposition, cleanup, tests, and evidence before execution.
- **REQ-SENT-032 — SHALL:** Every long-running or repeated SenTient workload use bounded queues, deadlines, cancellation, idempotency where effects can repeat, and durable workbench-state receipts.
- **REQ-SENT-033 — SHALL:** SenTient-generated code, models, indexes, datasets, prompts, evaluations, and build outputs remain isolated until their owning workflow explicitly imports and validates them.
- **REQ-SENT-034 — SHALL NOT:** A successful local experiment establish production, sovereign, high-assurance, release-signing, publication, control-plane, or operational profile conformance.
- **REQ-SENT-035 — SHALL:** SenTient development and build claims identify the exact profile, workspace, source revision, toolchain, model and dependency versions, resource envelope, integrations, tests, evidence, and explicit non-claims.
- **REQ-SENT-036 — SHALL:** SenTient offline operation preserve local isolation, provenance, resource limits, secret controls, candidate-only outputs, and cleanup without creating a remote-service dependency.
- **REQ-SENT-037 — SHALL:** SenTient deactivation and removal stop workloads, revoke workbench credentials, remove integrations, preserve required candidate provenance and evidence, and delete or retire isolated mutable state according to policy.
- **REQ-SENT-038 — SHALL NOT:** Removal of SenTient delete another component's data, shared platform authority, release evidence, protected audit records, or canonical documentation.
- **REQ-SENT-039 — SHALL:** Every exception affecting SenTient be profile-scoped, time-bounded, non-authoritative, supported by compensating controls, tests, evidence, cleanup, and explicit non-claims.
- **REQ-SENT-040 — SHALL:** SenTient conformance include default-off behavior, compatible profile scope, namespace isolation, candidate-only outputs, direct-write prohibition, managed integrations, secret and rights controls, bounded resources, removability, offline independence, lifecycle cleanup, reference resolution, and absence of prohibited open-state markers.
<!-- GENERATED:REQUIREMENTS:END -->
