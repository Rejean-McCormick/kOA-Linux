<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-GOV-TPL-COMP-001",
  "document_class": "template",
  "status": "active",
  "language": "en",
  "layer": "governance",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "00-governance/02-documentation-contract.md",
    "00-governance/03-normative-language.md",
    "00-governance/08-generated-content-policy.md"
  ],
  "decision_ids": [
    "DEC-DOC-001"
  ],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-DOC-003",
    "LOCK-DOC-005",
    "LOCK-DOC-016"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-002",
    "DOC-GOV-003",
    "DOC-GOV-008"
  ],
  "tags": [
    "template",
    "component",
    "ai-authoring"
  ]
}
KOA:DOC-META:END -->

# <Component Display Name>

<!--
TEMPLATE FILE
Target path pattern: docs/04-components/<component-slug>.md
Target document class: normative_markdown

Instructions for AI agents:
1. Replace every angle-bracket placeholder.
2. Remove all TEMPLATE NOTE comments.
3. Do not edit generated blocks manually.
4. Register the target document in generated/document-index.json.
5. Register or update the component in generated/component-catalog.json.
6. Create or update contracts/components/<component-slug>.component.json.
7. Link all applicable accepted decisions, requirements, locks, tests, and evidence.
8. Do not leave placeholders, undefined behavior, or unresolved architectural questions.
9. Do not introduce normative statements outside generated requirement blocks.
10. Run the complete documentation validation pipeline.
-->

<!-- KOA:TARGET-DOC-META:BEGIN
{
 "doc_id": "<DOC-COMP-NNN>",
 "document_class": "normative_markdown",
 "status": "active",
 "language": "en",
 "layer": "component",
 "scope": [
 "component:<component_id>"
 ],
 "canonical_refs": [
 "generated/component-catalog.json#/components/<component_id>",
 "contracts/components/<component-slug>.component.json"
 ],
 "decision_ids": [
 "<DEC-COMP-NNN>"
 ],
 "requirement_ids": [
 "<REQ-COMP-NNN>"
 ],
 "lock_ids": [
 "<LOCK-COMP-NNN>"
 ],
 "exception_ids": [],
 "depends_on": [
 "DOC-COMP-000",
 "<DOC-SYS-NNN>"
 ],
 "tags": [
 "component",
 "<component-slug>",
 "<domain-tag>"
 ]
}
KOA:TARGET-DOC-META:END -->

## 1. Purpose

<!-- TEMPLATE NOTE
Describe why the component exists.

State:
- the user or system problem it solves;
- its architectural role;
- the result it owns;
- why this responsibility is not assigned to another component.

Do not repeat canonical enums or interface lists here.
Reference the canonical contract instead.
-->

<Component Display Name> is the kOA component responsible for <single primary responsibility>.

It exists to <purpose statement>.

Its authoritative result is <owned result or state>.

It is not responsible for <closest adjacent responsibility>, which belongs to <other component or system authority>.

---

## 2. Scope

### 2.1 Included responsibilities

<!-- TEMPLATE NOTE
List conceptual responsibilities only.
Canonical capability identifiers belong in the component contract.
-->

The component covers:

- <responsibility>;
- <responsibility>;
- <responsibility>.

### 2.2 Excluded responsibilities

The component does not own:

- <excluded responsibility and owning component>;
- <excluded responsibility and owning component>;
- <excluded responsibility and owning component>.

### 2.3 Applicable profiles

<!-- TEMPLATE NOTE
Do not infer profile membership.
Profile membership is canonical in contracts/profiles/*.profile.json.
Use a generated block when listing profiles.
-->

<!-- GENERATED:BEGIN
source=generated/component-catalog.json#/components/<component_id>/applicable_profiles
renderer=canonical-list-v1
-->
- <profile_id>
<!-- GENERATED:END -->

### 2.4 Optionality and activation

The component is <required|optional|overlay_required> in its applicable profiles.

Its activation mode is <always_on|socket_activated|task_activated|manual|external_only>.

Absence or deactivation of this component causes <defined capability impact> and does not cause <explicitly unaffected capability> to fail.

---

## 3. Canonical References

### 3.1 Primary canonical references

`text
generated/component-catalog.json#/components/<component_id>
contracts/components/<component-slug>.component.json
`

### 3.2 Related profile contracts

`text
contracts/profiles/<profile>.profile.json
`

### 3.3 Related artifact contracts

`text
contracts/artifact-contracts/<artifact>.schema.json
`

### 3.4 Related integration contracts

`text
contracts/integration-types.contract.json#/integrations/<integration_id>
`

### 3.5 Related decisions and ADRs

`text
DEC-<DOMAIN>-<NUMBER>
ADR-<NUMBER>
`

### 3.6 Related requirements and locks

`text
REQ-<DOMAIN>-<NUMBER>
LOCK-<DOMAIN>-<NUMBER>
`

---

## 4. Model and Responsibilities

### 4.1 Component identity

<!-- GENERATED:BEGIN
source=generated/component-catalog.json#/components/<component_id>/identity
renderer=component-identity-v1
-->
| Field | Value |
| --- | --- |
| Component ID | `<component_id>` |
| Display name | `<Component Display Name>` |
| Component class | `<runtime|gateway|broker|workbench|platform|agent|service>` |
| Authority class | `<authoritative|derived|advisory|non_authoritative>` |
| Primary domain | `<domain>` |
<!-- GENERATED:END -->

### 4.2 Primary responsibility

The component owns <precise responsibility>.

This ownership includes:

- <owned behavior>;
- <owned state>;
- <owned transition>;
- <owned evidence or receipt>.

### 4.3 Responsibilities owned elsewhere

| Responsibility | Owning authority |
| --- | --- |
| <responsibility> | `<component_id or system authority>` |
| <responsibility> | `<component_id or system authority>` |
| <responsibility> | `<component_id or system authority>` |

### 4.4 Authority level

The component is authoritative for:

- <authoritative state>;
- <authoritative decision>;
- <authoritative artifact>.

The component is non-authoritative for:

- <external or candidate input>;
- <derived projection>;
- <another component's data>;
- <host privilege or policy decision, when applicable>.

### 4.5 Internal submodules

<!-- TEMPLATE NOTE
List only architecturally relevant submodules.
Implementation packages and class names belong in implementation documentation.
-->

| Submodule | Responsibility | Authoritative state |
| --- | --- | --- |
| `<submodule_id>` | <responsibility> | <state or `none`> |
| `<submodule_id>` | <responsibility> | <state or `none`> |

### 4.6 Trust boundaries

The component operates across these trust boundaries:

| Boundary | Source | Destination | Required control |
| --- | --- | --- | --- |
| `<boundary_id>` | `<source>` | `<destination>` | <validation, authorization, signature, consent, or gateway> |

---

## 5. Applicable Normative Requirements

<!-- TEMPLATE NOTE
All normative requirements must be generated from
generated/requirements-index.json.

Do not write SHALL, SHALL NOT, SHOULD, SHOULD NOT, or MAY manually outside
generated requirement blocks.
-->

<!-- GENERATED:REQUIREMENTS:BEGIN ids=<REQ-COMP-NNN>,<REQ-COMP-NNN> -->
- **<REQ-COMP-NNN> — SHALL:** <Generated requirement statement.>
- **<REQ-COMP-NNN> — SHALL NOT:** <Generated requirement statement.>
<!-- GENERATED:REQUIREMENTS:END -->

---

## 6. Data Authority and Ownership

### 6.1 Authoritative data

<!-- GENERATED:BEGIN
source=contracts/components/<component-slug>.component.json#/data_authority/authoritative_stores
renderer=data-store-table-v1
-->
| Store ID | Data class | Ownership | Persistence | Encryption |
| --- | --- | --- | --- | --- |
| `<store_id>` | `<data_class>` | `authoritative` | `<durable|ephemeral>` | `<required|profile_dependent|not_applicable>` |
<!-- GENERATED:END -->

### 6.2 Derived data

Derived data includes:

- <derived projection>;
- <cache>;
- <index>;
- <temporary transformation>.

Derived data can be regenerated from <canonical source>.

Loss of derived data causes <defined operational impact> but does not destroy <authoritative state>.

### 6.3 Candidate inputs

Candidate inputs include:

- <external AI output, when applicable>;
- <user-submitted artifact>;
- <external integration result>;
- <unverified import>.

Candidate inputs are non-authoritative until accepted through <validation and admission process>.

### 6.4 Prohibited data access

The component does not:

- write directly to another component's authoritative source tables;
- bypass a required gateway;
- treat a cache as authoritative;
- accept unverified external data as canonical state;
- store secrets in ordinary logs, receipts, exports, or images.

### 6.5 Data retention

<!-- GENERATED:BEGIN
source=contracts/components/<component-slug>.component.json#/data_authority/retention
renderer=retention-table-v1
-->
| Data class | Retention rule | Deletion authority | Export rule |
| --- | --- | --- | --- |
| `<data_class>` | `<rule>` | `<authority>` | `<rule>` |
<!-- GENERATED:END -->

---

## 7. Interfaces

### 7.1 Inbound interfaces

<!-- GENERATED:BEGIN
source=contracts/components/<component-slug>.component.json#/interfaces/inbound
renderer=interface-table-v1
-->
| Interface ID | Type | Caller | Input contract | Authentication | Idempotency |
| --- | --- | --- | --- | --- | --- |
| `<interface_id>` | `<api|event|file|socket|command|gateway>` | `<caller>` | `<contract_ref>` | `<method>` | `<required|not_applicable>` |
<!-- GENERATED:END -->

### 7.2 Outbound interfaces

<!-- GENERATED:BEGIN
source=contracts/components/<component-slug>.component.json#/interfaces/outbound
renderer=interface-table-v1
-->
| Interface ID | Type | Destination | Output contract | Delivery | Failure handling |
| --- | --- | --- | --- | --- | --- |
| `<interface_id>` | `<api|event|file|socket|command|gateway>` | `<destination>` | `<contract_ref>` | `<sync|async|batch>` | `<rule>` |
<!-- GENERATED:END -->

### 7.3 User-facing interfaces

The component exposes these user-facing capabilities:

- <capability>;
- <capability>.

User-facing interface behavior is governed by <Ariane, web shell, application UI, or other owner>.

### 7.4 Administrative interfaces

Administrative operations include:

- <operation>;
- <operation>.

Administrative interfaces require <authorization and privilege boundary>.

Root access is not an ordinary component API.

### 7.5 Interface compatibility

The component declares compatibility using:

- semantic interface version;
- artifact schema version;
- minimum compatible caller version;
- minimum compatible destination version;
- explicit incompatible-version behavior.

An incompatible contract is rejected before authoritative mutation.

---

## 8. Events and Messaging

### 8.1 Emitted events

<!-- GENERATED:BEGIN
source=contracts/components/<component-slug>.component.json#/events/emitted
renderer=event-table-v1
-->
| Event ID | Trigger | Payload contract | Delivery guarantee | Sensitive fields |
| --- | --- | --- | --- | --- |
| `<event_id>` | `<trigger>` | `<contract_ref>` | `<at_least_once|at_most_once|best_effort>` | `<classification>` |
<!-- GENERATED:END -->

### 8.2 Consumed events

<!-- GENERATED:BEGIN
source=contracts/components/<component-slug>.component.json#/events/consumed
renderer=event-table-v1
-->
| Event ID | Source | Consumer behavior | Idempotency key | Poison-message handling |
| --- | --- | --- | --- | --- |
| `<event_id>` | `<source_component>` | `<behavior>` | `<field>` | `<quarantine or review rule>` |
<!-- GENERATED:END -->

### 8.3 Transactional consistency

When a local authoritative commit emits an external event, the component uses <Transactional Outbox or accepted equivalent>.

Consumers are idempotent where delivery can repeat.

Poison messages remain inspectable and do not block the complete queue indefinitely.

---

## 9. Procedures or State Transitions

### 9.1 Canonical state model

<!-- GENERATED:BEGIN
source=contracts/components/<component-slug>.component.json#/state_model
renderer=state-model-v1
-->
| State | Meaning | Entry condition | Allowed next states |
| --- | --- | --- | --- |
| `<state_id>` | <meaning> | <condition> | `<state_id>` |
<!-- GENERATED:END -->

### 9.2 Primary workflow

The primary workflow is:

1. <receive or initiate>;
2. <validate>;
3. <authorize>;
4. <process>;
5. <commit authoritative state>;
6. <emit receipt or event>;
7. <publish or return result>.

### 9.3 Admission workflow

Inputs enter authoritative state only after:

1. identity verification;
2. schema validation;
3. capability authorization;
4. policy or consent evaluation where applicable;
5. duplicate and replay checks;
6. provenance recording;
7. atomic commit.

### 9.4 Activation workflow

When the component activates a versioned artifact:

1. verify identity and signature;
2. verify artifact class;
3. verify channel;
4. verify compatibility;
5. stage the artifact;
6. activate without partial authoritative state;
7. record the active identity;
8. preserve the last valid state;
9. emit activation evidence.

### 9.5 Deactivation workflow

Deactivation:

1. stops new work;
2. drains or safely suspends accepted work;
3. preserves authoritative state;
4. records unfinished work;
5. releases ephemeral resources;
6. emits operational status.

---

## 10. Failure States and Safe Degradation

### 10.1 Failure taxonomy

<!-- GENERATED:BEGIN
source=contracts/components/<component-slug>.component.json#/failure_model
renderer=failure-table-v1
-->
| Failure ID | Cause | Authority impact | Safe behavior | Recovery |
| --- | --- | --- | --- | --- |
| `<failure_id>` | <cause> | `<none|read_only|blocked>` | <behavior> | <procedure> |
<!-- GENERATED:END -->

### 10.2 Verification failure

When required identity, signature, schema, compatibility, or authorization verification fails:

- authoritative mutation is blocked;
- the invalid input is rejected or quarantined;
- the previous valid state remains active;
- diagnostic evidence is recorded without exposing secrets.

### 10.3 Dependency failure

When a required dependency is unavailable:

- the affected capability enters its declared degraded state;
- unrelated capabilities remain available;
- retries are bounded;
- queue growth is bounded;
- resource consumption remains inside the active profile envelope.

### 10.4 Network loss

The component's offline behavior is defined per profile.

It declares:

- capabilities that remain available;
- capabilities that become read-only;
- capabilities that stop;
- queued work behavior;
- synchronization behavior after recovery.

### 10.5 Storage pressure

Under storage pressure, the component:

- preserves authoritative data;
- limits or removes regenerable caches first;
- pauses non-critical ingestion or generation;
- exposes a health condition;
- does not silently discard authoritative state.

### 10.6 Resource pressure

The Resource Governor may:

- reduce concurrency;
- pause background work;
- lower job priority;
- reject new heavy jobs;
- stop task-activated workers after completion.

Resource control does not alter component authorization or governance policy.

### 10.7 Recovery and rollback

The component defines:

- restart behavior;
- replay behavior;
- state reconstruction;
- artifact rollback;
- forward repair for irreversible migrations;
- operator evidence required for recovery.

---

## 11. Security and Privacy

### 11.1 Identity and authentication

The component authenticates:

- users through <identity authority>;
- services through <service identity mechanism>;
- artifacts through <declared integrity or signature mechanism>;
- external integrations through <integration-specific mechanism>.

### 11.2 Authorization

Authorization is evaluated by <component authorization or Governance Policy Runtime>.

The component does not treat authentication as authorization.

### 11.3 Privilege boundary

Host mutations, when required, pass through <narrow privileged broker>.

The component does not expose general root execution.

### 11.4 Secrets

Secrets are:

- stored through the approved secret mechanism;
- scoped by environment and workspace where applicable;
- excluded from logs;
- excluded from receipts;
- excluded from ordinary exports;
- rotated through the declared lifecycle.

### 11.5 Privacy and disclosure

The component classifies:

- personal data;
- sensitive data;
- restricted evidence;
- public data;
- cultural-rights-restricted content.

Disclosure uses explicit contracts and approved gateways.

### 11.6 Audit

The component records critical events defined by its audit contract.

Public accountability data is separated from restricted evidence.

Access to restricted evidence is itself audited.

### 11.7 Cultural rights and consent

When relevant, the component enforces:

- audience restrictions;
- consent;
- attribution;
- export limitations;
- community or steward authority;
- revocation behavior.

---

## 12. Resource and Performance Model

### 12.1 Resource envelope

<!-- GENERATED:BEGIN
source=contracts/components/<component-slug>.component.json#/resource_envelope
renderer=resource-envelope-v1
-->
| Profile | CPU | Memory | Storage | Concurrency | Activation |
| --- | ---: | ---: | ---: | ---: | --- |
| `<profile_id>` | `<limit>` | `<limit>` | `<limit>` | `<limit>` | `<mode>` |
<!-- GENERATED:END -->

### 12.2 Background work

Background work includes:

- <job>;
- <job>.

Each job declares:

- queue limit;
- retry limit;
- timeout;
- CPU priority;
- I/O priority;
- cancellation behavior;
- shutdown behavior.

### 12.3 Heavy jobs

Heavy jobs are <task-activated or profile-controlled>.

The component does not start more than the profile's permitted heavy-job concurrency.

### 12.4 Performance objectives

Performance objectives are defined through:

- latency target;
- throughput target;
- startup target;
- queue-drain target;
- memory target;
- recovery target.

Measured performance evidence belongs in conformance and operations records, not in manually maintained canonical tables.

---

## 13. Observability and Operations

### 13.1 Health signals

The component exposes:

- liveness;
- readiness;
- dependency health;
- queue depth;
- resource saturation;
- active artifact identity;
- degraded capability state.

### 13.2 Logs

Logs are:

- structured;
- bounded;
- classified;
- free of secrets;
- correlated through stable request, job, or receipt identifiers.

### 13.3 Metrics

Metrics include:

- request or job count;
- success and failure count;
- latency;
- queue depth;
- retry count;
- resource use;
- rejected authoritative mutations;
- degraded-state duration.

### 13.4 Traces

Distributed traces are used only where supported by the selected profile and privacy policy.

Trace propagation does not disclose restricted content.

### 13.5 Backup and restore

The component declares:

- authoritative backup scope;
- excluded regenerable data;
- backup consistency mechanism;
- encryption;
- retention;
- restore validation;
- independent restore procedure.

### 13.6 Maintenance

Maintenance operations include:

- schema migration;
- artifact update;
- index rebuild;
- cache cleanup;
- key rotation;
- integrity verification.

Maintenance preserves declared availability and authority behavior.

---

## 14. Cross-Component Interactions

### 14.1 Interaction matrix

<!-- GENERATED:BEGIN
source=contracts/components/<component-slug>.component.json#/interactions
renderer=interaction-table-v1
-->
| Component | Direction | Contract | Purpose | Direct database access |
| --- | --- | --- | --- | --- |
| `<component_id>` | `<inbound|outbound|bidirectional>` | `<contract_ref>` | <purpose> | `prohibited` |
<!-- GENERATED:END -->

### 14.2 Required separations

The component remains separate from:

- <adjacent component and reason>;
- <adjacent authority and reason>;
- <gateway and reason>.

### 14.3 Publication and ingestion

Cross-domain publication uses the Publication Gateway.

Selected local media publication to UCKK uses Publication Gateway authorization followed by the UCKK Publication Bridge. Selected UCKK learning packages enter kOA through the separate UCKK Import Bridge.

These contracts are not interchangeable.

### 14.4 Resource and policy decisions

Resource Governor controls resource allocation and scheduling.

Governance Policy Runtime controls authorization, disclosure, consent, privilege, and governed exceptions where the active profile deploys it.

The component does not merge these authorities.

### 14.5 Language artifacts

User runtimes consume compiled language artifacts.

Language construction and compilation belong to the designated language workbench.

---

## 15. Decision Closure and Prohibited Assumptions

The component document does not leave implementation-affecting behavior undefined.

The following assumptions are prohibited unless explicit active authority states otherwise:

- the component is global because it exists in the repository;
- the component is active in every profile;
- the component owns data because it reads that data;
- a cache is authoritative;
- an external AI output is authoritative;
- an API permits direct database mutation;
- a recipe defines mandatory deployment;
- a service dependency may retry without bounds;
- failure of one optional integration may disable the core;
- administrative access implies unrestricted host privilege;
- current implementation behavior supersedes the component contract;
- similar components may be merged;
- omitted behavior may be selected by the implementing AI agent.

Any missing implementation-affecting decision blocks activation of the affected contract.

---

## 16. Validation Criteria

The component document is conformant when:

1. it is registered in `generated/document-index.json`;
2. its `DOC-ID` is unique;
3. the component exists in `generated/component-catalog.json`;
4. the component contract exists and validates;
5. every canonical reference resolves;
6. every applicable profile is declared canonically;
7. every normative statement has a registered requirement;
8. every requirement has source, scope, owner, strength, and validation;
9. every applicable lock is declared and passes;
10. data ownership is explicit;
11. direct writes to another component's authoritative stores are prohibited;
12. inbound and outbound interfaces have contracts;
13. state transitions are complete;
14. failure and degradation behavior is explicit;
15. resource envelopes exist for applicable profiles;
16. security, secrets, audit, and privacy behavior are defined;
17. generated blocks match their canonical sources;
18. no placeholder remains;
19. active prose is English;
20. the documentation graph remains acyclic;
21. AI context packages are regenerated;
22. the complete documentation validator passes.

Recommended component tests:

`text
TEST-COMP-<NNN>-001 Component registry and contract identity match.
TEST-COMP-<NNN>-002 Canonical references resolve.
TEST-COMP-<NNN>-003 Data ownership has no conflict.
TEST-COMP-<NNN>-004 Cross-component direct writes are rejected.
TEST-COMP-<NNN>-005 Interfaces reference valid contracts.
TEST-COMP-<NNN>-006 State transitions are complete.
TEST-COMP-<NNN>-007 Failure states define safe behavior.
TEST-COMP-<NNN>-008 Applicable profile envelopes exist.
TEST-COMP-<NNN>-009 Requirements map to tests or manual controls.
TEST-COMP-<NNN>-010 Generated projections are current.
`

Recommended commands:

`bash
python docs/tools/generate_docs.py --check
python docs/tools/check_canonical_ownership.py
python docs/tools/check_interfile_locks.py
python docs/tools/check_component_boundaries.py
python docs/tools/check_artifact_contracts.py
python docs/tools/check_traceability.py
python docs/tools/check_generated_content.py
python docs/tools/check_document_graph.py
python docs/tools/build_ai_context.py --check
python docs/tools/validate_docs.py
`

---

## 17. Non-Normative Examples

### 17.1 Correct authority statement

`text
kOA Mediatheque is authoritative for accepted local media records and their offline availability.
`

This statement is valid only when the canonical component contract assigns that local ownership. Remote UCKK authority belongs to the online UCKK Mediatheque and is described by integration contracts rather than reassigned to a local component.

### 17.2 Incorrect authority statement

`text
UCKK Import Bridge owns accepted local media because it transports a package.
`

An ingestion gateway may transfer and validate candidate input without owning the destination's authoritative state.

### 17.3 Correct external AI boundary

`text
An external AI result is stored as a candidate artifact with provenance and requires controlled acceptance.
`

### 17.4 Incorrect external AI boundary

`text
The external AI result is written directly into canonical component records.
`

### 17.5 Correct profile scoping

`text
The component is task-activated in user_lightweight and may be always-on in build_farm.
`

### 17.6 Incorrect profile scoping

`text
The component is always-on because one deployment runs it continuously.
`

---

## 18. Final Component Summary

<!-- TEMPLATE NOTE
This section is intentionally concise.
It helps AI agents confirm the component boundary after reading the document.
-->

| Question | Answer |
| --- | --- |
| What does the component own? | <authoritative responsibility> |
| What does it not own? | <adjacent responsibilities> |
| Which profiles include it? | <canonical profile reference> |
| What data is authoritative? | <canonical data reference> |
| Which interfaces are allowed? | <canonical interface reference> |
| What happens when it fails? | <safe degradation summary> |
| Which locks protect its boundary? | <LOCK-IDs> |
| Which decision authorizes it? | <DEC-IDs> |

---

## 19. Final Rule

> A component document explains one bounded authority. Its canonical contract defines its identity, data, interfaces, states, and limits. The document does not absorb neighboring responsibilities, does not redefine canonical values, and does not leave implementation-affecting behavior to inference.
