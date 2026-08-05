<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONF-005",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "conformance",
  "scope": [
    "test_evidence",
    "conformance_validation",
    "profile_claims",
    "release_claims",
    "artifact_admission"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "generated/document-index.json",
    "contracts/terminology.contract.json",
    "contracts/system.contract.json#/capability_degradation",
    "generated/component-catalog.json#/components/audit_broker",
    "generated/component-catalog.json#/components/identity_and_trust",
    "generated/component-catalog.json#/components/governance_policy_runtime",
    "generated/component-catalog.json#/components/resource_governor",
    "generated/profile-catalog.json",
    "contracts/artifact-classes.contract.json",
    "contracts/release-channels.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "schemas/test-evidence.schema.json"
  ],
  "decision_ids": [
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-PROFILE-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-CONF-EVD-001",
    "REQ-CONF-EVD-002",
    "REQ-CONF-EVD-003",
    "REQ-CONF-EVD-004",
    "REQ-CONF-EVD-005",
    "REQ-CONF-EVD-006",
    "REQ-CONF-EVD-007",
    "REQ-CONF-EVD-008",
    "REQ-CONF-EVD-009",
    "REQ-CONF-EVD-010",
    "REQ-CONF-EVD-011",
    "REQ-CONF-EVD-012",
    "REQ-CONF-EVD-013",
    "REQ-CONF-EVD-014",
    "REQ-CONF-EVD-015",
    "REQ-CONF-EVD-016",
    "REQ-CONF-EVD-017",
    "REQ-CONF-EVD-018",
    "REQ-CONF-EVD-019",
    "REQ-CONF-EVD-020",
    "REQ-CONF-EVD-021",
    "REQ-CONF-EVD-022",
    "REQ-CONF-EVD-023",
    "REQ-CONF-EVD-024",
    "REQ-CONF-EVD-025",
    "REQ-CONF-EVD-026",
    "REQ-CONF-EVD-027",
    "REQ-CONF-EVD-028",
    "REQ-CONF-EVD-029",
    "REQ-CONF-EVD-030",
    "REQ-CONF-EVD-031",
    "REQ-CONF-EVD-032",
    "REQ-CONF-EVD-033",
    "REQ-CONF-EVD-034",
    "REQ-CONF-EVD-035",
    "REQ-CONF-EVD-036",
    "REQ-CONF-EVD-037",
    "REQ-CONF-EVD-038",
    "REQ-CONF-EVD-039",
    "REQ-CONF-EVD-040",
    "REQ-CONF-EVD-041",
    "REQ-CONF-EVD-042",
    "REQ-CONF-EVD-043",
    "REQ-CONF-EVD-044",
    "REQ-CONF-EVD-045",
    "REQ-CONF-EVD-046",
    "REQ-CONF-EVD-047",
    "REQ-CONF-EVD-048",
    "REQ-CONF-EVD-049",
    "REQ-CONF-EVD-050",
    "REQ-CONF-EVD-051",
    "REQ-CONF-EVD-052",
    "REQ-CONF-EVD-053",
    "REQ-CONF-EVD-054",
    "REQ-CONF-EVD-055",
    "REQ-CONF-EVD-056"
  ],
  "lock_ids": [
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-DOC-001",
    "LOCK-DOC-002",
    "LOCK-DOC-003",
    "LOCK-DOC-004",
    "LOCK-GOV-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-002",
    "DOC-CONST-013",
    "DOC-SYS-017",
    "DOC-DEV-013",
    "DOC-LIFE-006",
    "DOC-LIFE-016",
    "DOC-SEC-009",
    "DOC-SEC-019",
    "DOC-OPS-006",
    "DOC-OPS-016",
    "DOC-CONF-000",
    "DOC-CONF-001",
    "DOC-CONF-002",
    "DOC-CONF-003",
    "DOC-CONF-004"
  ],
  "tags": [
    "conformance",
    "test-evidence",
    "test-catalog",
    "traceability",
    "profile-claims",
    "release-evidence",
    "provenance",
    "selective-audit",
    "retention",
    "revocation"
  ]
}
KOA:DOC-META:END -->

# Test Evidence

> **Document status:** Normative conformance architecture.
> **Definition:** Test evidence is a registered, immutable record of one declared test execution, its exact subjects, its assertions, its outcome, and the material required to validate that conclusion.
> **Authority rule:** The test catalog defines what must be tested; the evidence registry records what occurred; traceability determines which claims the evidence can support.

## 1. Purpose

This document defines how kOA creates, validates, registers, reuses, aggregates, revokes, supersedes, retains, and audits test evidence.

Test evidence supports:

- requirement conformance;
- Interfile Alignment Lock validation;
- profile and overlay claims;
- component-boundary claims;
- security and operations claims;
- artifact admission;
- release-channel and Release Set claims;
- migration and recovery claims;
- exception compensating controls;
- sovereign and offline conformance;
- documentation and contract validation.

Evidence must prove the declared result for exact subjects under exact conditions.

A passing result is not a general statement that the system is safe, correct, or conformant outside the evidence scope.

## 2. Scope

### 2.1 Included scope

This document applies to evidence from:

- automated tests;
- deterministic validators;
- schema validation;
- static analysis;
- component and integration tests;
- security tests;
- profile test matrices;
- resource and degradation tests;
- lifecycle, rollback, and forward-repair tests;
- artifact and release verification;
- reproducibility tests;
- manual inspections;
- witnessed exercises;
- break-glass and recovery exercises;
- performance, load, sampling, fuzzing, and statistical tests;
- connected and disconnected environments.

### 2.2 Excluded objects

The following are not test evidence by themselves:

- a test definition;
- a requirement reference;
- a checklist;
- an issue or ticket;
- a build status badge;
- an unregistered log;
- a screenshot without execution context;
- an AI summary;
- an operator statement;
- a signature without assertion results;
- an artifact digest without a test result;
- an exception approval;
- a release note.

They can be referenced by evidence when the evidence contract permits them.

### 2.3 Evidence does not own domain state

Evidence observes and records.

It does not become:

- component-owned business data;
- profile authority;
- an artifact release;
- a policy decision;
- a Release Set;
- a migration checkpoint;
- a queue result;
- an operational receipt;
- an activation decision.

Evidence can reference those objects without replacing them.

### 2.4 Evidence classes

Operationally, evidence can be:

| Class | Description |
| --- | --- |
| Automated | Produced by an admitted executable validator or test implementation |
| Manual | Produced by a declared human procedure |
| Witnessed | Manual or operational exercise requiring a separate observer |
| Composite | A conformance aggregate referencing registered atomic evidence |
| Continuous | Repeated observation with declared validity and sampling rules |
| Release-grade | Evidence satisfying the stricter provenance, identity, environment, and retention rules of a release claim |

The test catalog owns the allowed class for each test.

## 3. Canonical References

### 3.1 Canonical ownership

| Information | Canonical owner |
| --- | --- |
| Test identity, purpose, execution class, assertions, and applicability | `generated/test-catalog.json` |
| Test execution record, outcome, validity, and evidence references | `generated/evidence-catalog.json` |
| Evidence structure | `schemas/test-evidence.schema.json` |
| Requirement, lock, profile, component, artifact, test, and evidence links | `generated/traceability.json` |
| Normative statements | `generated/requirements-index.json` |
| Cross-file invariants | `generated/assertion-index.json` |
| Active exceptions and compensating controls | `generated/exception-index.json` |
| Profile composition and claims | Profile contracts |
| Component ownership and interfaces | Component contracts |
| Artifact identity, integrity, and admission | Artifact classes and artifact contracts |
| Release-channel compatibility | Release-channel registry and Release Set |
| Evidence access and selective disclosure | Audit Broker and applicable policy |
| Identity, trust, signing, and revocation | Identity and Trust |
| Governed authorization | Governance Policy Runtime |

### 3.2 Expected registry relationship

`text
requirement or lock
→ traceability link
→ test catalog entry
→ test execution
→ evidence registry entry
→ conformance or release claim
`

A direct prose link from a claim to a test name is insufficient.

### 3.3 Subject binding

Evidence binds to subjects through canonical identifiers such as:

`text
requirement_id
lock_id
decision_id
profile_id and profile_version
component_id and component_contract_version
artifact_id and artifact_version
release_set_id and release_set_version
source_revision
schema_id and schema_version
toolchain_id and toolchain_version
test_id and test_version
exception_id
`

Cryptographic digests are added when intrinsic to an artifact, signed manifest, release bundle, provenance chain, or content-addressed object.

Ordinary Markdown and generated prose are identified by their canonical document identity and versioned repository revision rather than mandatory per-document metadata or source hashes.

## 4. Model and Responsibilities

### 4.1 Test and evidence distinction

| Object | Question answered |
| --- | --- |
| Requirement | What behavior is required? |
| Lock | Which facts must remain aligned across files? |
| Test definition | How is the required behavior evaluated? |
| Test execution | What procedure actually ran? |
| Evidence | What exact result was observed and validated? |
| Traceability link | Which authority and claim can use the evidence? |
| Conformance claim | Does the complete required evidence set support the declared scope? |

### 4.2 Evidence identity model

A test execution uses distinct identities:

| Identity | Purpose |
| --- | --- |
| Test ID | Stable catalog identity |
| Test version | Exact definition and assertion version |
| Execution ID | Identity of one run or witnessed procedure |
| Evidence ID | Identity of the registered immutable result |
| Attachment ID | Identity of a retained diagnostic or supporting object |
| Claim ID | Identity of a conformance, profile, artifact, or release claim |
| Receipt ID | Identity of required evidence lifecycle receipts |

One execution produces one terminal evidence outcome.

A composite claim references multiple evidence IDs rather than merging their atomic records.

### 4.3 Execution lifecycle

The execution lifecycle is:

`text
scheduled
→ preparing
→ running
→ evaluating
→ finalized
`

Alternative terminal states are:

`text
cancelled
blocked
internal_error
`

The evidence lifecycle is:

`text
candidate
→ validated
→ registered
`

Later states can be:

`text
revoked
superseded
expired
`

Registered evidence is immutable.

### 4.4 Outcome model

The test catalog defines allowed outcomes.

The common outcomes are:

| Outcome | Meaning | Claim effect |
| --- | --- | --- |
| `pass` | All required assertions ran and passed | Can support a claim within scope |
| `fail` | At least one assertion failed or a prohibited effect occurred | Blocks the affected claim |
| `blocked` | A required precondition prevented a valid conclusion | Blocks the affected claim |
| `internal_error` | The test or collector failed | No conformance effect; blocks required claim |
| `cancelled` | Execution intentionally stopped before a valid conclusion | No conformance effect |
| `not_applicable` | Applicability model excludes the test from this scope | Recorded as applicability disposition, not fabricated pass |

A required test without valid applicable evidence is `missing`.

### 4.5 Minimum evidence record

A registered evidence object includes:

- evidence ID;
- execution ID;
- test ID and version;
- execution class;
- terminal outcome;
- subject bindings;
- profile and overlay context;
- architecture or hardware/resource class where applicable;
- environment and toolchain identity;
- fixtures and dependency identity;
- policy and exception context;
- start and completion timestamps;
- executor and applicable witness identities;
- assertion-level results;
- prohibited-side-effect results;
- diagnostic attachment references;
- provenance and signature references where required;
- validity and invalidation rules;
- retention classification;
- traceability references.

The schema owns exact field names and enumerations.

### 4.6 Assertion model

Each assertion result identifies:

- assertion ID from the test definition;
- expected criterion;
- observed result;
- pass or fail;
- measurement and unit where applicable;
- tolerance or threshold where applicable;
- diagnostic reference where needed.

A test passes only if every required assertion passes.

Optional diagnostics cannot compensate for a missing required assertion.

### 4.7 Environment model

The execution environment identifies material factors such as:

- active profile and overlays;
- operating-system or runtime identity;
- component and service versions;
- toolchain versions;
- architecture;
- hardware or resource class;
- resource envelope;
- dependency versions;
- network mode;
- storage mode;
- locale and timezone where relevant;
- deterministic seed or sampling configuration;
- active policy and exception state.

Host-specific details not material to applicability are excluded or normalized.

### 4.8 Automated evidence

Automated evidence is produced by an admitted test implementation.

It records:

- implementation identity and version;
- invocation entry point;
- normalized parameters;
- assertion results;
- exit status;
- start and completion times;
- environment identity;
- retained diagnostic references.

A successful process exit is not automatically a passing test unless the catalog explicitly defines it as the complete assertion.

### 4.9 Manual and witnessed evidence

Manual evidence follows a versioned procedure.

It records:

- operator identity;
- witness or approver identity when required;
- exact procedural steps;
- observations;
- assertion judgments;
- deviations;
- supporting references;
- completion and review timestamps.

An AI-generated summary can assist preparation but cannot replace accountable human judgment.

### 4.10 Evidence attachments

Attachments can include:

- machine-readable reports;
- bounded logs;
- traces;
- screenshots;
- measurements;
- packet or event captures;
- SBOMs;
- provenance receipts;
- decision receipts;
- migration verification;
- conformance matrices.

Attachments remain subordinate to the registered assertion record.

They use intrinsic digests and signatures when their artifact contracts require them.

### 4.11 Validity and reuse

Evidence reuse is allowed only when:

- the test catalog permits reuse;
- every subject binding still matches;
- applicability conditions remain true;
- the test version remains accepted;
- material dependencies and environment remain compatible;
- required freshness remains valid;
- no relevant key, tool, source, artifact, exception, or evidence object is revoked;
- the claim scope is no broader than the evidence scope.

Permanent evidence validity is explicit rather than assumed.

### 4.12 Composite claims

A composite conformance or release claim records:

- claim identity and scope;
- complete applicable requirement and lock set;
- complete required test set;
- passing evidence IDs;
- failing, blocked, expired, revoked, and missing items;
- applicability dispositions;
- active exception and compensating-control evidence;
- final claim outcome;
- claim authority and time.

A composite claim does not rewrite atomic evidence.

### 4.13 Selective audit

Evidence access follows selective audit.

A reviewer receives the minimum evidence needed for the declared purpose.

Sensitive attachments can remain protected while a private proof or verified assertion record demonstrates the required property.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN
source=generated/requirements-index.json#/requirements
ids=REQ-CONF-EVD-001,REQ-CONF-EVD-002,REQ-CONF-EVD-003,REQ-CONF-EVD-004,REQ-CONF-EVD-005,REQ-CONF-EVD-006,REQ-CONF-EVD-007,REQ-CONF-EVD-008,REQ-CONF-EVD-009,REQ-CONF-EVD-010,REQ-CONF-EVD-011,REQ-CONF-EVD-012,REQ-CONF-EVD-013,REQ-CONF-EVD-014,REQ-CONF-EVD-015,REQ-CONF-EVD-016,REQ-CONF-EVD-017,REQ-CONF-EVD-018,REQ-CONF-EVD-019,REQ-CONF-EVD-020,REQ-CONF-EVD-021,REQ-CONF-EVD-022,REQ-CONF-EVD-023,REQ-CONF-EVD-024,REQ-CONF-EVD-025,REQ-CONF-EVD-026,REQ-CONF-EVD-027,REQ-CONF-EVD-028,REQ-CONF-EVD-029,REQ-CONF-EVD-030,REQ-CONF-EVD-031,REQ-CONF-EVD-032,REQ-CONF-EVD-033,REQ-CONF-EVD-034,REQ-CONF-EVD-035,REQ-CONF-EVD-036,REQ-CONF-EVD-037,REQ-CONF-EVD-038,REQ-CONF-EVD-039,REQ-CONF-EVD-040,REQ-CONF-EVD-041,REQ-CONF-EVD-042,REQ-CONF-EVD-043,REQ-CONF-EVD-044,REQ-CONF-EVD-045,REQ-CONF-EVD-046,REQ-CONF-EVD-047,REQ-CONF-EVD-048,REQ-CONF-EVD-049,REQ-CONF-EVD-050,REQ-CONF-EVD-051,REQ-CONF-EVD-052,REQ-CONF-EVD-053,REQ-CONF-EVD-054,REQ-CONF-EVD-055,REQ-CONF-EVD-056
renderer=requirements-list-v1
-->
- **REQ-CONF-EVD-001 — SHALL:** Every conformance, profile, artifact, release, security, migration, and operational claim rely on registered evidence from declared tests.
- **REQ-CONF-EVD-002 — SHALL:** The test catalog remain the canonical owner of test identity, purpose, method, applicability, assertions, required inputs, expected outputs, and execution class.
- **REQ-CONF-EVD-003 — SHALL:** The evidence registry remain the canonical owner of recorded test executions, outcomes, subject bindings, validity, revocation, and retained evidence references.
- **REQ-CONF-EVD-004 — SHALL:** The traceability registry remain the canonical owner of links among requirements, locks, decisions, profiles, components, artifacts, tests, and evidence.
- **REQ-CONF-EVD-005 — SHALL NOT:** A test name in prose, checklist mark, issue comment, build badge, screenshot, or unregistered log be treated as conformance evidence by itself.
- **REQ-CONF-EVD-006 — SHALL:** Every evidence object have a unique evidence identity and reference exactly one test execution identity.
- **REQ-CONF-EVD-007 — SHALL:** Every execution identify the test definition and test-definition version used.
- **REQ-CONF-EVD-008 — SHALL:** Every execution bind to exact subjects through stable identifiers, versions, revisions, profile identities, component identities, artifact identities, Release Set identities, or intrinsic content digests as applicable.
- **REQ-CONF-EVD-009 — SHALL NOT:** Evidence for one version, profile, architecture, scope, Release Set, artifact, or environment silently apply to another.
- **REQ-CONF-EVD-010 — SHALL:** Cryptographic digests be recorded when intrinsic to artifact integrity, signed manifests, content-addressed objects, release bundles, provenance, or the applicable evidence contract.
- **REQ-CONF-EVD-011 — SHALL NOT:** Test evidence require metadata hashes, source hashes, or ordinary Markdown or generated-prose hashes as general documentation fields.
- **REQ-CONF-EVD-012 — SHALL:** Every execution identify the executor, tool or procedure version, execution environment, active profile, applicable overlays, start time, completion time, and clock basis.
- **REQ-CONF-EVD-013 — SHALL:** Every execution identify required fixtures, input classes, dependency versions, resource envelope, relevant policy state, and active exception references.
- **REQ-CONF-EVD-014 — SHALL:** Every evidence object record one terminal outcome from the test catalog's allowed outcomes.
- **REQ-CONF-EVD-015 — SHALL:** A `pass` outcome mean that every required assertion executed and satisfied its declared acceptance criterion.
- **REQ-CONF-EVD-016 — SHALL:** A `fail` outcome identify at least one false assertion or prohibited observed effect.
- **REQ-CONF-EVD-017 — SHALL:** A `blocked` outcome identify the missing authority, input, dependency, environment, evidence, or capability that prevented a valid test conclusion.
- **REQ-CONF-EVD-018 — SHALL:** An `internal_error` outcome identify a failure of the test implementation or evidence collector and have no passing authority effect.
- **REQ-CONF-EVD-019 — SHALL NOT:** A skipped, cancelled, not-run, inconclusive, blocked, or internal-error execution be counted as a pass.
- **REQ-CONF-EVD-020 — SHALL:** Not-applicable disposition occur through the registered applicability and traceability model rather than a fabricated passing execution.
- **REQ-CONF-EVD-021 — SHALL:** Automated evidence record the invoked test entry point, normalized parameters, assertion results, exit status, and retained diagnostic references.
- **REQ-CONF-EVD-022 — SHALL:** Manual evidence be permitted only when the test catalog declares a manual or witnessed execution class.
- **REQ-CONF-EVD-023 — SHALL:** Manual evidence record the operator, applicable witness or approver, exact procedure version, observations, assertion decisions, and supporting references.
- **REQ-CONF-EVD-024 — SHALL NOT:** An AI system, external integration, test generator, or evidence collector approve its own output or independently create a passing manual judgment.
- **REQ-CONF-EVD-025 — SHALL:** Test execution preserve component data ownership and use declared test, maintenance, simulation, or component-owner interfaces.
- **REQ-CONF-EVD-026 — SHALL NOT:** A conformance test write directly into another component's authoritative store unless it executes the owning component's approved interface under declared test authority.
- **REQ-CONF-EVD-027 — SHALL:** Destructive, privileged, disclosure-sensitive, cross-domain, or production-adjacent tests require explicit scope, policy, isolation, restoration, and evidence controls.
- **REQ-CONF-EVD-028 — SHALL:** Test inputs and retained evidence minimize secrets, personal data, tenant data, cultural material, proprietary payloads, and unrelated operational content.
- **REQ-CONF-EVD-029 — SHALL NOT:** Logs, screenshots, traces, dumps, recordings, or fixtures retain secret values or unnecessary sensitive payloads for evidence completeness.
- **REQ-CONF-EVD-030 — SHALL:** Evidence distinguish the compact assertion record from optional diagnostic attachments and preserve only references needed to reproduce or audit the conclusion.
- **REQ-CONF-EVD-031 — SHALL:** Evidence be immutable after registration; a correction, reinterpretation, or added result shall create a new evidence object linked to the prior object.
- **REQ-CONF-EVD-032 — SHALL:** Evidence status distinguish at least candidate, validated, registered, revoked, superseded, and expired states where applicable.
- **REQ-CONF-EVD-033 — SHALL:** Evidence validation verify schema, test identity, execution identity, subject bindings, outcome rules, required assertions, provenance, signatures where required, attachments, and traceability.
- **REQ-CONF-EVD-034 — SHALL:** Evidence requiring a signature or provenance receipt use the applicable artifact, trust, and signing contracts.
- **REQ-CONF-EVD-035 — SHALL NOT:** A valid evidence signature prove that the underlying test passed, that the test was applicable, or that the subject remains unchanged.
- **REQ-CONF-EVD-036 — SHALL:** Evidence validity declare reuse conditions, applicability scope, and freshness or invalidation triggers where the result is not permanently valid.
- **REQ-CONF-EVD-037 — SHALL:** A changed subject, changed test definition, changed relevant dependency, changed profile, changed authority, expired exception, revoked key, compromised tool, or invalid environment revoke or supersede affected evidence when applicability no longer holds.
- **REQ-CONF-EVD-038 — SHALL:** Flaky or repeated tests retain every material attempt and the reason for rerun.
- **REQ-CONF-EVD-039 — SHALL NOT:** Repeated execution until one pass erase prior failures or establish a passing claim without the catalog's declared stability rule.
- **REQ-CONF-EVD-040 — SHALL:** Sampling, statistical tests, fuzzing, load tests, and nondeterministic tests declare seed handling, sample population, confidence or threshold rule, run count, and acceptance method.
- **REQ-CONF-EVD-041 — SHALL:** Deterministic tests produce equivalent semantic assertion results for equivalent admitted inputs and environment.
- **REQ-CONF-EVD-042 — SHALL:** A profile claim reference the exact profile version, overlays, architecture, hardware class or resource class, and all required passing evidence from its test matrix.
- **REQ-CONF-EVD-043 — SHALL:** A release claim reference the exact Release Set and all required evidence for its system, services, governance, and knowledge versions.
- **REQ-CONF-EVD-044 — SHALL:** Artifact-admission evidence bind to the exact admitted artifact identity and applicable schema, integrity, provenance, SBOM, vulnerability, profile, and compatibility results.
- **REQ-CONF-EVD-045 — SHALL:** Exception-dependent evidence identify the exact active exception and compensating-control results.
- **REQ-CONF-EVD-046 — SHALL NOT:** Expired, revoked, out-of-scope, or superseded exceptions support a passing claim.
- **REQ-CONF-EVD-047 — SHALL:** A conformance aggregate distinguish required, passing, failing, blocked, not-applicable, expired, revoked, and missing evidence.
- **REQ-CONF-EVD-048 — SHALL NOT:** A partial passing subset be represented as complete conformance.
- **REQ-CONF-EVD-049 — SHALL:** Critical evidence registration, revocation, supersession, and claim activation emit required machine-readable receipts when the governing contract requires them.
- **REQ-CONF-EVD-050 — SHALL:** If required receipt or evidence persistence fails under receipt-before-commit semantics, the associated claim remain uncommitted.
- **REQ-CONF-EVD-051 — SHALL:** Offline evidence collection use admitted local tests, schemas, fixtures, identities, clocks, tools, trust material, and storage and preserve equivalent validation and registration controls.
- **REQ-CONF-EVD-052 — SHALL NOT:** Network unavailability justify missing assertions, unverifiable tools, absent identities, unregistered evidence, or weakened privacy and integrity controls.
- **REQ-CONF-EVD-053 — SHALL:** Evidence-storage or registry failure degrade or block only affected claims while preserving existing valid evidence and unrelated active authority.
- **REQ-CONF-EVD-054 — SHALL:** Recovery reconcile pending executions, partial attachments, evidence identities, registry writes, signatures, receipts, revocations, supersessions, and claim state before registration resumes.
- **REQ-CONF-EVD-055 — SHALL:** Retention preserve evidence, test-definition identity, assertion records, required attachments, provenance, signatures, receipts, exceptions, revocations, and claim links for the longest applicable recovery, audit, release, or policy period.
- **REQ-CONF-EVD-056 — SHALL:** Test-evidence conformance test schema validation, exact subject binding, outcomes, automated and manual evidence, privacy, immutability, validity, reruns, aggregation, profile and release claims, offline collection, recovery, retention, and prohibited side effects.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Select applicable tests

1. resolve the claim scope;
2. resolve applicable requirements, locks, decisions, profiles, components, artifacts, and exceptions;
3. resolve traceability links;
4. select the exact test catalog entries;
5. evaluate applicability;
6. record not-applicable dispositions with their canonical rule;
7. block the claim if a required authority has no declared test or controlled manual validation.

### 6.2 Prepare an execution

1. assign the execution ID;
2. resolve the exact test and implementation versions;
3. resolve subject identities and versions;
4. resolve profile, overlays, architecture, and environment;
5. resolve fixtures, dependencies, policy, exceptions, and resource envelope;
6. validate executor and worker identity;
7. establish isolation and restoration behavior;
8. confirm evidence and attachment storage;
9. begin only after every required precondition passes.

### 6.3 Run an automated test

1. invoke the declared entry point;
2. apply normalized parameters;
3. record material environment identity;
4. collect assertion-level results;
5. detect prohibited side effects;
6. collect bounded diagnostics;
7. classify terminal outcome;
8. clean or restore test state;
9. construct the candidate evidence object.

### 6.4 Run a manual or witnessed test

1. present the versioned procedure;
2. resolve operator and witness identities;
3. verify target and environment;
4. execute each required step;
5. record observations at the assertion level;
6. record deviations;
7. collect bounded supporting material;
8. obtain required witness or reviewer attestation;
9. construct the candidate evidence object.

### 6.5 Validate evidence

1. validate against `schemas/test-evidence.schema.json`;
2. resolve test and test version;
3. verify execution identity uniqueness;
4. verify exact subject bindings;
5. verify every required assertion result;
6. verify outcome consistency;
7. verify environment and applicability;
8. verify attachments and intrinsic integrity material;
9. verify provenance and signatures where required;
10. verify privacy and minimization;
11. verify traceability and retention;
12. accept, reject, or block the candidate.

### 6.6 Register evidence

1. allocate or confirm the evidence ID;
2. persist the immutable evidence object;
3. persist required attachments or references;
4. persist required receipts;
5. update the evidence registry atomically;
6. make the evidence available to traceability and claim evaluation;
7. leave the evidence unregistered when any required persistence fails.

### 6.7 Rerun a test

1. preserve every prior material attempt;
2. identify the reason for rerun;
3. determine whether the subject or environment changed;
4. allocate a new execution ID;
5. run the complete applicable procedure;
6. register the new result independently;
7. apply the catalog's stability or flakiness rule;
8. do not erase or hide prior failures.

### 6.8 Revoke, supersede, or expire evidence

1. identify the invalidation trigger;
2. identify affected evidence and claims;
3. prevent new claims from using invalid evidence;
4. preserve the original immutable record;
5. register revocation, supersession, or expiry state;
6. emit required receipt;
7. re-evaluate affected profile, artifact, release, and conformance claims;
8. schedule or require replacement tests.

### 6.9 Build a conformance aggregate

1. resolve the complete claim scope;
2. enumerate applicable requirements and locks;
3. enumerate required tests;
4. retrieve valid evidence;
5. classify pass, fail, blocked, missing, expired, revoked, and not-applicable items;
6. verify exception and compensating-control evidence;
7. verify scope and freshness;
8. compute the claim outcome without hiding incomplete categories;
9. persist the claim and required receipt.

### 6.10 Collect evidence offline

1. use locally admitted schemas, test definitions, tools, fixtures, and trust material;
2. resolve local identities and time;
3. run the same assertion procedure;
4. validate and register evidence locally;
5. protect evidence and receipts from alteration or loss;
6. synchronize through an authorized path when available;
7. resolve duplicate or conflicting evidence identities without overwriting either record.

### 6.11 Recover evidence services

1. stop new registration when consistency is uncertain;
2. enter `restoring`;
3. reconcile pending executions and terminal outcomes;
4. reconcile candidate and registered evidence identities;
5. verify partial attachments;
6. verify signatures, provenance, and receipts;
7. reconcile revocations, supersessions, and expiries;
8. re-evaluate affected claims;
9. resume registration only after registry and storage consistency pass.

## 7. Failure States and Safe Degradation

| Failure condition | Required response | Preserved behavior |
| --- | --- | --- |
| Test definition missing | Mark claim blocked | Existing unrelated evidence |
| Traceability link missing | Mark affected claim blocked | Other complete claim scopes |
| Subject identity unresolved | Do not run or register | Existing subject state |
| Environment cannot be identified | Block release-grade conclusion | Non-authoritative diagnostics |
| Test implementation unavailable | Mark required test blocked | Previously valid in-scope evidence |
| Test implementation crashes | Record `internal_error` | Subject remains unchanged |
| Required assertion not executed | Do not record pass | Available diagnostics |
| Required fixture unavailable | Record `blocked` | Other independent tests |
| Sensitive attachment cannot be sanitized | Omit attachment or block evidence if essential | Compact assertion result where sufficient |
| Evidence schema validation fails | Reject candidate evidence | Prior registered evidence |
| Evidence registry unavailable | Retain validated candidate safely; do not claim registration | Existing registered evidence |
| Attachment storage unavailable | Block registration when attachment is required | Existing evidence |
| Required signature invalid | Reject or block evidence | Unsigned diagnostics where non-authoritative |
| Required receipt cannot persist | Keep claim or evidence transition uncommitted | Prior state |
| Evidence validity expires | Mark expired and re-evaluate claims | Historical record |
| Relevant exception expires | Revoke support for dependent claim | Unrelated evidence |
| Test tool compromise suspected | Revoke affected evidence and block reuse | Evidence from unaffected tools |
| Conflicting subject versions detected | Block aggregation | Atomic evidence records |
| Rerun disagrees with prior pass | Expose instability and apply catalog rule | Both immutable results |
| Offline synchronization conflict | Preserve both records and resolve identities | Local validated records |
| Recovery reconciliation incomplete | Remain `restoring` or `blocked` | Last consistent registry state |

Evidence failure never changes the tested component's authoritative state.

## 8. Cross-Component Interactions

### 8.1 Test catalog

The test catalog defines tests and assertions.

It does not record executions or claim results.

### 8.2 Evidence registry

The evidence registry records immutable execution evidence and lifecycle state.

It does not define requirements or tests.

### 8.3 Traceability registry

Traceability determines which evidence can support which authority and claim.

It does not convert invalid evidence into valid evidence.

### 8.4 Audit Broker

Audit Broker coordinates selective evidence access and retains applicable cross-component receipts.

It does not become the canonical owner of test definitions or component data.

### 8.5 Identity and Trust

Identity and Trust resolves executors, witnesses, workers, signers, tools, nodes, and trust material.

Unresolved identity blocks the applicable evidence authority.

### 8.6 Governance Policy Runtime

Governance Policy Runtime evaluates sensitive tests, disclosures, exceptions, and evidence access.

Policy authorization does not change a failed assertion into a pass.

### 8.7 Resource Governor

Resource Governor constrains test workers, scanners, load tests, fuzzing, queues, storage, and execution time.

Resource admission does not authorize the domain action being tested.

### 8.8 Components and profiles

Component contracts define test interfaces and prohibited side effects.

Profile contracts define applicable mechanisms, environments, resource classes, and required profile claims.

### 8.9 Artifact and release authorities

Artifact verification and release authorities consume valid evidence for exact artifacts and Release Sets.

They remain responsible for admission and activation decisions.

### 8.10 External integrations and AI

External test services and AI tools operate through registered integrations.

Their outputs remain candidate observations until validated and registered under the same evidence rules.

## 9. Decision Closure and Prohibited Assumptions

The following decisions are closed:

- the test catalog owns test definitions;
- the evidence registry owns execution evidence;
- traceability owns claim links;
- one evidence object represents one exact execution;
- subject binding is explicit and exact;
- intrinsic artifact digests are used where required;
- ordinary Markdown and generated prose do not receive general metadata or source-hash requirements;
- a pass requires every required assertion;
- skipped, blocked, cancelled, and internal-error runs are not passes;
- manual evidence is allowed only when declared;
- AI cannot make accountable passing judgments;
- registered evidence is immutable;
- reruns preserve prior attempts;
- claims expose missing and invalid evidence;
- offline evidence uses equivalent controls;
- evidence access is selective and minimized.

Prohibited assumptions include:

- treating a test filename as evidence;
- treating a green dashboard as complete conformance;
- reusing evidence because two deployments appear similar;
- applying workstation evidence to Build Farm;
- applying one architecture's result to another;
- accepting a screenshot without subject and execution identity;
- using process exit zero as an undeclared complete assertion;
- recording a pass when a required assertion did not run;
- deleting a failed attempt after a successful rerun;
- treating a signature as proof of test correctness;
- treating a digest as proof of applicability;
- treating an exception as passing evidence;
- treating missing evidence as not applicable;
- copying secret-bearing logs into evidence storage;
- allowing test tooling direct writes into another component's authoritative store;
- allowing an AI-generated summary to certify a manual test;
- requiring ordinary documentation hashes as generic evidence fields;
- treating local evidence as release-grade without the declared release environment;
- treating offline operation as a reason to weaken registration.

## 10. Validation Criteria

Test-evidence conformance validates when:

1. every active claim resolves through traceability to declared tests;
2. every test ID and version resolves in the test catalog;
3. every evidence ID and execution ID is unique;
4. each evidence object references one execution;
5. exact subjects and versions resolve;
6. intrinsic artifact digests are present where required;
7. ordinary Markdown metadata and source hashes are absent as generic fields;
8. executor, environment, profile, overlays, tools, fixtures, and times resolve;
9. every required assertion has one valid result;
10. outcome classification matches assertion results;
11. skipped, blocked, cancelled, and internal-error executions cannot count as passes;
12. not-applicable disposition resolves through applicability rules;
13. automated invocation and tool identities resolve;
14. manual and witnessed evidence contains accountable identities and procedures;
15. AI output cannot create an authoritative manual judgment;
16. component data ownership and declared test interfaces remain intact;
17. destructive and privileged tests have isolation and restoration;
18. sensitive evidence is minimized and protected;
19. attachments remain subordinate and verifiable;
20. registered evidence is immutable;
21. signatures and provenance validate where required;
22. freshness and invalidation rules are enforced;
23. reruns retain prior material attempts;
24. nondeterministic tests declare seeds, populations, thresholds, and run counts;
25. profile claims match exact profile matrices;
26. release claims bind exact four-channel Release Sets;
27. artifact evidence binds exact artifact identities;
28. exception-dependent evidence includes current compensating controls;
29. aggregates expose fail, blocked, missing, expired, revoked, and not-applicable states;
30. required receipts persist before commit;
31. offline collection passes equivalent validation;
32. recovery reconciles evidence and claim state;
33. retention satisfies recovery, audit, release, and policy periods;
34. all decisions, requirements, locks, exceptions, tests, evidence, and traceability references resolve;
35. no unresolved marker, placeholder, duplicate canonical owner, or non-intrinsic documentation hash appears;
36. conformance, profile, artifact, release, security, lifecycle, and Interfile Alignment Lock checks pass.

Applicable checks include:

`bash
python docs/tools/check_traceability.py
python docs/tools/check_artifact_contracts.py
python docs/tools/check_profile_composition.py
python docs/tools/check_release_sets.py
python docs/tools/check_component_boundaries.py
python docs/tools/check_canonical_ownership.py
python docs/tools/check_interfile_locks.py
python docs/tools/validate_docs.py
`

## 11. Non-Normative Examples

### 11.1 Automated profile test

A test verifies that a `developer_linux_workstation` workspace cannot read another workspace's secrets.

The evidence identifies the profile version, both workspace IDs, test version, runtime and tool versions, assertion results, and bounded diagnostic references.

### 11.2 Blocked test

A Release Set compatibility test cannot resolve the governance-channel release.

The execution records `blocked`. It does not record a pass based on the other three channels.

### 11.3 Rerun after failure

A service-update rollback test fails because a prior service remains connected to the test queue.

The failed execution is retained. After the environment is repaired, a new execution ID records the rerun. The claim applies the catalog's stability rule to both results.

### 11.4 Manual break-glass exercise

A high-assurance profile requires a witnessed emergency-access exercise.

The evidence records two approvers, the executor, observer, exact procedure version, temporary grant scope, revocation result, restoration assertions, and receipt references.

### 11.5 Artifact evidence

A services artifact is tested for schema validity, signature, provenance, SBOM, vulnerability disposition, profile compatibility, and Release Set compatibility.

The evidence binds to the artifact's intrinsic digest because the artifact is content-identified. It does not add a generic hash to explanatory Markdown.

### 11.6 Offline sovereign-node evidence

A disconnected node runs an admitted recovery test with local schemas, tools, identities, fixtures, and trust material.

The evidence is validated and registered locally, protected against alteration, and later synchronized without overwriting either side's immutable records.

### 11.7 Selective disclosure

An external auditor must verify that a sensitive retention test passed.

The auditor receives the assertion record, identities, validity, and a private proof or sanitized attachment rather than the underlying tenant records.
