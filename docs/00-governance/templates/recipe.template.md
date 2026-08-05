<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-GOV-TPL-RECIPE-001",
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
    "recipe",
    "ai-authoring"
  ]
}
KOA:DOC-META:END -->

<!-- KOA:TARGET-DOC-META:BEGIN
{
 "doc_id": "DOC-RECIPE-TEMPLATE",
 "document_class": "recipe",
 "status": "template",
 "language": "en",
 "layer": "implementation_recipe",
 "scope": ["global"],
 "canonical_refs": [
 "generated/document-index.json",
 "generated/requirements-index.json",
 "generated/assertion-index.json",
 "generated/profile-catalog.json"
 ],
 "decision_ids": [],
 "requirement_ids": [],
 "lock_ids": [
 "LOCK-IMPL-001",
 "LOCK-IMPL-002",
 "LOCK-DOC-003",
 "LOCK-DOC-004",
 "LOCK-DOC-005",
 "LOCK-DOC-016"
 ],
 "exception_ids": [],
 "depends_on": [
 "DOC-GOV-000",
 "DOC-GOV-002",
 "DOC-GOV-003",
 "DOC-GOV-007",
 "DOC-GOV-010"
 ],
 "tags": [
 "template",
 "recipe",
 "implementation",
 "non-normative"
 ]
}
KOA:TARGET-DOC-META:END -->

# Recipe Template

> **Template status:** Non-normative authoring template.
> **Required action:** Replace every placeholder enclosed in `<...>` before activating a recipe.
> **Authority rule:** A recipe explains one implementation method. It does not create system, profile, component, security, lifecycle, or conformance requirements.

---

## Recipe Identity

| Field | Value |
| --- | --- |
| Recipe ID | `<RECIPE-DOMAIN-NNN>` |
| Title | `<Concise implementation-oriented title>` |
| Status | `<draft|review|active|deprecated|superseded|archived>` |
| Version | `<MAJOR.MINOR.PATCH>` |
| Owner | `<Owning team or architectural role>` |
| Last reviewed | `<YYYY-MM-DD>` |
| Applies to profiles | `<profile IDs or "none">` |
| Applies to components | `<component IDs or "none">` |
| Applies to toolchains | `<toolchain IDs or "none">` |
| Supported platforms | `<platform list>` |
| Supersedes | `<recipe IDs or "none">` |
| Replaced by | `<recipe ID or "none">` |

---

## 1. Purpose

Describe the concrete implementation outcome produced by this recipe.

The purpose must identify:

- what is installed, configured, started, migrated, tested, recovered, or removed;
- which active profile or component context the recipe targets;
- what successful completion looks like;
- what the recipe intentionally does not cover.

Example structure:

> This recipe configures `<implementation>` for `<profile or component>` so that `<observable result>`. It does not define the canonical requirement, interface, profile membership, or security policy.

---

## 2. Non-Normative Status

This recipe is non-normative unless an active profile contract explicitly adopts a specific implementation choice from it.

The canonical requirements, locks, profiles, interfaces, and artifact formats referenced by this recipe remain authoritative in their owning registries and contracts.

This recipe SHALL NOT be used to:

- create a new global requirement;
- redefine a canonical value;
- broaden a profile-specific requirement;
- replace a component contract;
- replace a security control;
- replace a lifecycle contract;
- establish conformance by itself;
- resolve a missing owner decision;
- override an Interfile Alignment Lock.

When this recipe conflicts with active canonical authority, the recipe is invalid and must be corrected.

---

## 3. Scope

### 3.1 Included

List the exact implementation activities covered.

- `<Included activity 1>`
- `<Included activity 2>`
- `<Included activity 3>`

### 3.2 Excluded

List adjacent activities that are intentionally outside this recipe.

- `<Excluded activity 1>`
- `<Excluded activity 2>`
- `<Excluded activity 3>`

### 3.3 Supported profiles

Reference active profile contracts by canonical path.

`text
contracts/profiles/<profile>.profile.json
`

Supported profiles:

- `<profile_id>`

Unsupported profiles:

- `<profile_id and reason>`

### 3.4 Supported platforms and versions

| Platform or tool | Supported version or range | Canonical source |
| --- | --- | --- |
| `<platform>` | `<version>` | `<canonical reference>` |
| `<tool>` | `<version>` | `<canonical reference>` |

Do not invent versions that are absent from canonical authority.

---

## 4. Canonical References

List every canonical source that constrains this recipe.

### 4.1 Decisions

- `<DEC-DOMAIN-NNN>`

### 4.2 Requirements

- `<REQ-DOMAIN-NNN>`

### 4.3 Locks

- `<LOCK-DOMAIN-NNN>`

### 4.4 Profiles

- `contracts/profiles/<profile>.profile.json#<json-pointer>`

### 4.5 Component contracts

- `contracts/components/<component>.component.json#<json-pointer>`

### 4.6 Toolchain contracts

- `contracts/toolchains/<toolchain>.toolchain.json#<json-pointer>`

### 4.7 Artifact contracts

- `contracts/artifact-contracts/<artifact>.schema.json#<json-pointer>`

### 4.8 Related documentation

- `<DOC-DOMAIN-NNN>`

A hyperlink alone does not declare a semantic dependency. Dependencies must also be registered in `generated/document-index.json`.

---

## 5. Preconditions

All preconditions must be testable or explicitly verifiable.

### 5.1 Authority preconditions

- The referenced decisions are accepted.
- The referenced profiles are active.
- The referenced requirements are active.
- The referenced locks pass.
- No applicable exception is expired.
- The active authority index matches the expected registry versions.

### 5.2 Environment preconditions

- `<Required operating system or distribution>`
- `<Required architecture>`
- `<Required storage>`
- `<Required memory>`
- `<Required network state>`
- `<Required user privileges>`
- `<Required package manager>`
- `<Required runtime>`
- `<Required workspace state>`

### 5.3 Data preconditions

- `<Required backup state>`
- `<Required database state>`
- `<Required migration state>`
- `<Required free-space threshold>`
- `<Required encryption or key availability>`

### 5.4 Verification commands

`bash
# Replace with commands that verify each precondition.
<command>
`

Each command must:

- be safe to run repeatedly;
- avoid changing state unless explicitly documented;
- return a non-zero status on failure;
- avoid printing secrets.

---

## 6. Inputs and Outputs

### 6.1 Inputs

| Input | Type | Source | Required | Sensitive |
| --- | --- | --- | ---: | ---: |
| `<input>` | `<type>` | `<source>` | `<yes|no>` | `<yes|no>` |

### 6.2 Outputs

| Output | Type | Destination | Canonical contract |
| --- | --- | --- | --- |
| `<output>` | `<type>` | `<path or service>` | `<reference>` |

### 6.3 Mutable state

List every stateful resource the recipe creates or modifies.

- files;
- directories;
- services;
- containers;
- networks;
- volumes;
- databases;
- users;
- groups;
- sockets;
- ports;
- secrets;
- certificates;
- caches;
- queues;
- generated artifacts.

For each mutable resource, declare:

- owner;
- location;
- lifecycle;
- backup behavior;
- cleanup behavior;
- rollback behavior.

---

## 7. Safety and Security Boundaries

### 7.1 Privilege model

State the minimum required privilege.

`text
<unprivileged user|rootless container|narrow privileged broker|root>
`

Root must not be used as the ordinary governance API.

When host mutation requires privilege, use the profile-approved privileged path.

### 7.2 Secret handling

This recipe must not:

- embed secrets in commands;
- write secrets to logs;
- include secrets in examples;
- store secrets in images;
- store secrets in receipts;
- export secrets through ordinary diagnostics.

Declare the approved secret source:

`text
<secret manager, environment injection, protected file, or profile-defined source>
`

### 7.3 Network boundaries

Declare:

- required outbound destinations;
- required inbound listeners;
- local-only ports;
- inter-component connections;
- prohibited connections;
- offline behavior.

Default-deny applies where required by the active profile.

### 7.4 Data authority

This recipe must not cause one component to write directly to another component's authoritative source tables.

Any cross-component mutation must use an active contract, gateway, event, or publication workflow.

### 7.5 External integrations

For every external integration, declare:

- integration ID;
- capability;
- data transferred;
- user initiation requirement;
- failure behavior;
- removal behavior;
- provenance or receipt behavior.

External AI outputs remain candidate inputs until accepted by an authoritative component workflow.

---

## 8. Resource Envelope

Declare the expected and maximum resource usage.

| Resource | Expected | Maximum | Enforcement mechanism |
| --- | ---: | ---: | --- |
| CPU | `<value>` | `<value>` | `<cgroup, scheduler, runtime limit>` |
| Memory | `<value>` | `<value>` | `<mechanism>` |
| Storage | `<value>` | `<value>` | `<mechanism>` |
| I/O | `<value>` | `<value>` | `<mechanism>` |
| Processes | `<value>` | `<value>` | `<mechanism>` |
| Concurrent jobs | `<value>` | `<value>` | `<mechanism>` |

For development recipes, resource names and mutable state must be scoped by `workspace_id`.

For `user_lightweight`, heavy services should be task-activated and bounded.

---

## 9. Naming and Isolation

### 9.1 Canonical naming inputs

Use only declared identifiers.

`text
profile_id
component_id
workspace_id
artifact_id
release_id
`

### 9.2 Workspace-scoped resources

When the recipe applies to development, namespace these resources with `workspace_id`:

- virtual environments;
- containers;
- networks;
- volumes;
- database names;
- database users;
- sockets;
- temporary directories;
- log directories;
- PID files;
- service names;
- secret names;
- host-port allocations.

### 9.3 Collision behavior

State how the recipe behaves when a target name, port, path, database, or volume already exists.

Allowed behaviors:

- verify and reuse an identical managed resource;
- allocate a new deterministic name;
- stop with an explicit conflict;
- migrate through a documented state transition.

Silent overwrite is prohibited.

---

## 10. Procedure

Use numbered, atomic steps.

Each step must include:

- objective;
- command or action;
- expected result;
- verification;
- failure behavior;
- rollback effect.

### Step 1 — `<Step title>`

**Objective**

`<What this step establishes>`

**Command**

`bash
<command>
`

**Expected result**

`text
<observable result>
`

**Verification**

`bash
<verification command>
`

**Failure behavior**

`<How failure is detected and what remains unchanged>`

**Rollback effect**

`<What this step requires during rollback>`

---

### Step 2 — `<Step title>`

**Objective**

`<What this step establishes>`

**Command**

`bash
<command>
`

**Expected result**

`text
<observable result>
`

**Verification**

`bash
<verification command>
`

**Failure behavior**

`<How failure is detected and what remains unchanged>`

**Rollback effect**

`<What this step requires during rollback>`

---

### Step 3 — `<Step title>`

**Objective**

`<What this step establishes>`

**Command**

`bash
<command>
`

**Expected result**

`text
<observable result>
`

**Verification**

`bash
<verification command>
`

**Failure behavior**

`<How failure is detected and what remains unchanged>`

**Rollback effect**

`<What this step requires during rollback>`

---

## 11. Idempotency

Declare whether the complete recipe is idempotent.

`text
Idempotent: <yes|no|conditional>
`

If conditional, state the exact condition.

For every command that changes state, describe:

- how an existing correct state is detected;
- how an existing incompatible state is handled;
- whether repeated execution is safe;
- whether repeated execution changes identifiers;
- whether repeated execution duplicates data;
- whether repeated execution rotates secrets or certificates.

A recipe that is not idempotent must include a checkpoint and rollback plan.

---

## 12. Validation

### 12.1 Functional validation

List commands that prove the intended outcome.

`bash
<functional validation command>
`

Expected result:

`text
<expected output or state>
`

### 12.2 Contract validation

Validate generated or modified artifacts against their canonical schemas.

`bash
<schema validation command>
`

### 12.3 Lock validation

Run applicable Interfile Alignment Locks.

`bash
python docs/tools/check_interfile_locks.py
`

List the expected lock IDs:

- `<LOCK-DOMAIN-NNN>`

### 12.4 Profile validation

Run the profile-specific conformance checks.

`bash
<profile validation command>
`

### 12.5 Documentation validation

When the recipe changes documentation or generated examples:

`bash
python docs/tools/validate_docs.py
`

### 12.6 Success criteria

The recipe succeeds only when:

- every procedure step completed;
- all expected state exists;
- no prohibited state exists;
- all applicable locks pass;
- all schema validation passes;
- all required services are healthy;
- rollback remains available where required;
- no secret appears in logs or output;
- no unrelated workspace or component changed.

---

## 13. Failure Handling

For each failure class, define:

- detection;
- containment;
- retry behavior;
- safe state;
- operator action;
- evidence produced.

| Failure | Detection | Safe state | Required action |
| --- | --- | --- | --- |
| `<failure>` | `<signal>` | `<state>` | `<action>` |

Retries must be bounded.

A failed authoritative activation must not leave partial authoritative state.

When verification cannot complete, the result is `blocked`, not `pass`.

---

## 14. Rollback

### 14.1 Rollback trigger

Rollback is required when:

- `<trigger 1>`;
- `<trigger 2>`;
- `<trigger 3>`.

### 14.2 Rollback prerequisites

- `<backup, snapshot, previous release, or retained configuration>`
- `<required privilege>`
- `<required service state>`

### 14.3 Rollback procedure

`bash
<rollback command sequence>
`

### 14.4 Rollback verification

`bash
<rollback verification command>
`

### 14.5 Irreversible changes

List every irreversible operation.

If none:

`text
None.
`

If an irreversible change exists, declare:

- exact irreversible boundary;
- accepted owner decision;
- forward-repair procedure;
- backup requirement;
- evidence requirement.

---

## 15. Cleanup and Removal

Describe how to remove every resource created by the recipe.

`bash
<cleanup commands>
`

Cleanup must not remove:

- unrelated workspace state;
- another component's data;
- shared canonical artifacts;
- shared download caches unless explicitly requested;
- required backups;
- migration evidence.

Declare residual state intentionally retained after cleanup.

---

## 16. Observability and Evidence

### 16.1 Logs

Declare:

- log locations;
- log retention;
- redaction behavior;
- correlation identifiers;
- workspace identifiers;
- release identifiers.

### 16.2 Metrics

List relevant metrics.

- `<metric>`
- `<metric>`

### 16.3 Receipts

Declare whether the recipe produces a critical-transition receipt.

`text
Receipt required: <yes|no>
Receipt contract: <canonical reference or "none">
`

### 16.4 Evidence

List required evidence objects.

- `<TEST-ID>`
- `<EVID-ID>`

Evidence must be sufficient to reproduce or verify the result without relying on conversational context.

---

## 17. Offline Behavior

Declare one of:

`text
fully_offline
offline_after_prerequisite_download
online_required
not_applicable
`

If downloads are required, declare:

- exact artifacts;
- source;
- expected versions;
- signature requirements;
- cache location;
- offline transfer format;
- quarantine behavior.

An offline-capable recipe must not silently contact external services.

---

## 18. Compatibility and Versioning

Declare compatibility with:

- profile versions;
- component versions;
- schema versions;
- operating-system versions;
- runtime versions;
- artifact versions;
- previous recipe versions.

| Dependency | Compatible range | Incompatible range | Migration action |
| --- | --- | --- | --- |
| `<dependency>` | `<range>` | `<range>` | `<action>` |

Breaking changes require:

- a major recipe version;
- an accepted decision when architecture changes;
- an impact report;
- updated tests;
- updated rollback or migration steps.

---

## 19. AI Execution Protocol

An AI agent using this recipe must:

1. load `AI_CONTEXT.md`;
2. load the task-specific generated context;
3. verify the recipe status is `active`;
4. verify all canonical references resolve;
5. verify all referenced decisions are accepted;
6. verify all applicable locks pass before execution;
7. verify the target profile and platform;
8. preserve workspace and component isolation;
9. execute one atomic step at a time;
10. run the verification after every step;
11. stop on unexpected state;
12. avoid inventing commands, paths, ports, versions, or credentials;
13. record commands actually executed;
14. record validation results;
15. report `blocked` when required authority or evidence is absent.

The AI agent must not:

- treat this recipe as independent authority;
- modify canonical registries through an undocumented side effect;
- skip safety checks for speed;
- silently repair unrelated state;
- expose secrets;
- weaken a lock;
- continue after a failed verification unless the recipe explicitly defines a safe recovery branch.

### 19.1 Required execution summary

`json
{
 "recipe_id": "<RECIPE-DOMAIN-NNN>",
 "recipe_version": "<MAJOR.MINOR.PATCH>",
 "profile_ids": [],
 "component_ids": [],
 "workspace_id": null,
 "decision_ids": [],
 "requirement_ids": [],
 "lock_ids": [],
 "exception_ids": [],
 "commands_executed": [],
 "tests_run": [],
 "evidence_ids": [],
 "rollback_available": true,
 "result": "pass|fail|blocked"
}
`

---

## 20. Troubleshooting

Troubleshooting entries must use observed conditions rather than guesses.

### `<Symptom>`

**Observed signal**

`text
<error, status, metric, or log evidence>
`

**Likely bounded causes**

- `<cause>`
- `<cause>`

**Diagnostic command**

`bash
<command>
`

**Corrective action**

`bash
<command or documented action>
`

**Escalation condition**

`<Condition requiring owner or specialist review>`

Do not include speculative corrections that bypass canonical authority or safety boundaries.

---

## 21. Non-Normative Example

This section may contain a complete worked example after the template is instantiated.

The example must:

- use fictional or non-sensitive values;
- identify every placeholder value;
- avoid real credentials;
- preserve canonical naming rules;
- preserve profile scope;
- show validation;
- show expected failure behavior;
- show rollback when applicable.

Example values must not be interpreted as canonical defaults.

---

## 22. Maintenance

The recipe owner reviews this file when any referenced:

- decision changes;
- requirement changes;
- lock changes;
- profile changes;
- component contract changes;
- toolchain contract changes;
- artifact schema changes;
- supported platform changes;
- security boundary changes;
- lifecycle rule changes.

`compute_impact.py` determines whether the recipe requires:

`text
updated
reviewed_no_change
regenerated
deprecated
blocked
`

A recipe is deprecated when its implementation method is no longer recommended but remains usable.

A recipe is superseded when a replacement recipe exists.

A recipe is archived when it has no current supported use.

---

## 23. Author Checklist

Before requesting review:

- [ ] All placeholders are replaced.
- [ ] The recipe has a registered `DOC-ID` and recipe identity.
- [ ] The recipe is classified as `recipe`.
- [ ] The recipe status is valid.
- [ ] Canonical references resolve.
- [ ] Decisions are accepted.
- [ ] Requirements are active.
- [ ] Applicable locks are listed.
- [ ] Supported profiles are explicit.
- [ ] Unsupported profiles are explicit.
- [ ] Preconditions are testable.
- [ ] Inputs and outputs are declared.
- [ ] Mutable state is declared.
- [ ] Privilege is minimized.
- [ ] Secrets are protected.
- [ ] Network behavior is explicit.
- [ ] Resource limits are explicit.
- [ ] Naming and collision behavior are explicit.
- [ ] Procedure steps are atomic.
- [ ] Every step has verification.
- [ ] Idempotency is declared.
- [ ] Failure behavior is explicit.
- [ ] Rollback is complete.
- [ ] Cleanup is scoped safely.
- [ ] Offline behavior is declared.
- [ ] Compatibility is declared.
- [ ] AI execution rules are complete.
- [ ] Troubleshooting does not bypass authority.
- [ ] Documentation validation passes.

---

## 24. Review Checklist

The reviewer verifies:

- [ ] The recipe does not create independent normative authority.
- [ ] The recipe does not duplicate canonical enums or defaults.
- [ ] The recipe does not globalize a profile rule.
- [ ] The recipe does not cross component data boundaries.
- [ ] The recipe does not bypass the privileged broker where required.
- [ ] The recipe does not expose secrets.
- [ ] The recipe preserves offline claims.
- [ ] The recipe preserves safe degradation.
- [ ] The recipe preserves rollback or forward repair.
- [ ] The recipe preserves workspace isolation.
- [ ] The recipe references current active authority.
- [ ] The recipe's examples are clearly non-normative.
- [ ] Applicable locks and tests pass.

---

## 25. Final Recipe Rule

> A recipe may explain exactly how to implement an approved outcome, but it never decides what the system is. Canonical contracts define the target, accepted decisions authorize it, requirements state what must hold, locks preserve alignment, and validation proves that the recipe remains within those boundaries.
