<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-GOV-TPL-ADR-001",
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
    "adr",
    "ai-authoring"
  ]
}
KOA:DOC-META:END -->

<!--
TEMPLATE FILE

Purpose:
- Create one Architecture Decision Record under docs/10-adrs/.
- Preserve alignment between owner decisions, canonical registries, locks,
  requirements, implementation, validation, and evidence.

Usage rules:
1. Copy this file to docs/10-adrs/ADR-NNN-short-title.md.
2. Replace every {{REQUIRED:...}} token.
3. Replace optional tokens or write "Not applicable." in the related section.
4. Delete all TEMPLATE-INSTRUCTION comments from the completed ADR.
5. Do not activate the ADR until its linked owner decision is accepted and all
   required validation passes.
6. Do not use open-decision placeholder, TODO, FIXME, UNKNOWN, or equivalent unresolved markers.
7. If a required decision does not exist, keep the ADR status "proposed" and
   block dependent authority from activation.

This template is non-normative. The governing rules are defined by the active
kOA documentation governance contracts and registries.
-->

<!-- KOA:TARGET-DOC-META:BEGIN
{
  "doc_id": "{{REQUIRED:DOC_ID}}",
  "document_class": "adr",
  "status": "{{REQUIRED:proposed|accepted|rejected|deprecated|superseded|archived}}",
  "language": "en",
  "layer": "architecture_decision",
  "scope": [
    "{{REQUIRED:SCOPE_ID}}"
  ],
  "canonical_refs": [
    "{{REQUIRED:REPO_RELATIVE_PATH#JSON_POINTER}}"
  ],
  "decision_ids": [
    "{{REQUIRED:DEC_ID}}"
  ],
  "requirement_ids": [],
  "lock_ids": [],
  "exception_ids": [],
  "depends_on": [],
  "tags": [
    "architecture-decision"
  ]
}
KOA:TARGET-DOC-META:END -->

# ADR-{{REQUIRED:NNN}} — {{REQUIRED:Short Decision Title}}

**ADR ID:** `ADR-{{REQUIRED:NNN}}`  
**Status:** `{{REQUIRED:proposed|accepted|rejected|deprecated|superseded|archived}}`  
**Decision class:** `{{REQUIRED:minor|major}}`  
**Decision owner:** `{{REQUIRED:OWNER_ID}}`  
**Owner decision:** `{{REQUIRED:DEC_ID}}`  
**Change packet:** `{{REQUIRED:CHG-YYYY-NNNN}}`  
**Created:** `{{REQUIRED:YYYY-MM-DD}}`  
**Accepted:** `{{OPTIONAL:YYYY-MM-DD_OR_NOT_APPLICABLE}}`  
**Effective:** `{{OPTIONAL:YYYY-MM-DD_OR_NOT_APPLICABLE}}`  
**Supersedes:** `{{OPTIONAL:ADR_IDS_OR_NOT_APPLICABLE}}`  
**Superseded by:** `{{OPTIONAL:ADR_ID_OR_NOT_APPLICABLE}}`

<!-- TEMPLATE-INSTRUCTION
Status rules:
- proposed: rationale may be reviewed, but the ADR has no active authority.
- accepted: the linked owner decision is accepted and required validation passed.
- rejected: the option was considered and explicitly not adopted.
- deprecated: still historical authority, but no longer preferred for new work.
- superseded: replaced by another ADR and retained for traceability.
- archived: historical record with no current authority.

An ADR records rationale and consequences. The linked DEC object authorizes the
active decision. An ADR cannot override decisions.registry.json.
-->

## 1. Decision Summary

{{REQUIRED:State the selected architectural decision in one precise paragraph. Identify what is chosen, where it applies, and the principal behavior that is excluded.}}

## 2. Scope

### 2.1 Included scope

- `{{REQUIRED:global|profile|profile_overlay|component|artifact_class|development_toolchain|migration_only}}`
- {{REQUIRED:List every affected profile, component, artifact class, toolchain, or governance domain.}}

### 2.2 Excluded scope

- {{REQUIRED:List scopes to which this decision does not apply.}}

### 2.3 Activation boundary

{{REQUIRED:Describe the exact boundary at which this ADR becomes applicable. Use canonical identifiers rather than informal names.}}

## 3. Canonical References

### 3.1 Owner decision

- `{{REQUIRED:generated/decision-index.json#/decisions/...}}`
- `{{REQUIRED:DEC_ID}}`

### 3.2 Canonical objects changed or constrained

- `{{REQUIRED:REPO_RELATIVE_PATH#JSON_POINTER}}`

### 3.3 Related documents

- `{{REQUIRED:DOC_ID}}` — `{{REQUIRED:repo-relative-path}}`

### 3.4 Related requirements

- `{{OPTIONAL:REQ_ID_OR_NOT_APPLICABLE}}`

### 3.5 Related locks

- `{{OPTIONAL:LOCK_ID_OR_NOT_APPLICABLE}}`

### 3.6 Related exceptions

- `{{OPTIONAL:EXC_ID_OR_NOT_APPLICABLE}}`

## 4. Context and Problem

### 4.1 Current state

{{REQUIRED:Describe the authoritative state before this decision. Reference canonical objects and active profiles. Do not rely on implementation behavior alone.}}

### 4.2 Problem statement

{{REQUIRED:Describe the architectural problem, inconsistency, limitation, or required capability.}}

### 4.3 Why a decision is required

{{REQUIRED:Explain why existing authority is insufficient and why a local implementation choice cannot safely resolve the matter.}}

### 4.4 Constraints

- {{REQUIRED:List constitutional invariants, profile limits, compatibility constraints, resource limits, offline requirements, security boundaries, or migration constraints.}}

## 5. Decision Drivers

Rank the decision drivers from highest to lowest priority.

1. {{REQUIRED:Highest-priority driver.}}
2. {{REQUIRED:Second driver.}}
3. {{REQUIRED:Additional driver.}}

<!-- TEMPLATE-INSTRUCTION
Decision drivers should be stable architectural concerns, for example:
- canonical ownership;
- offline continuity;
- fail-closed authority;
- safe degradation;
- component isolation;
- reproducibility;
- portability and exit;
- resource envelope;
- operational recoverability;
- AI boundary;
- profile-specific conformance.
-->

## 6. Considered Options

### 6.1 Option A — {{REQUIRED:Selected Option Name}}

**Description**

{{REQUIRED:Describe the option precisely.}}

**Advantages**

- {{REQUIRED:Advantage.}}

**Disadvantages and costs**

- {{REQUIRED:Disadvantage or cost.}}

**Constraint fit**

{{REQUIRED:Explain how this option satisfies or conflicts with the decision drivers and active locks.}}

### 6.2 Option B — {{REQUIRED:Rejected Option Name}}

**Description**

{{REQUIRED:Describe the option precisely.}}

**Advantages**

- {{REQUIRED:Advantage.}}

**Disadvantages and costs**

- {{REQUIRED:Disadvantage or cost.}}

**Reason rejected**

{{REQUIRED:Explain the decisive reason this option was rejected.}}

### 6.3 Option C — {{OPTIONAL:Additional Option Name Or Not applicable}}

{{OPTIONAL:Complete this option using the same structure, or write "Not applicable."}}

## 7. Decision

### 7.1 Selected option

`{{REQUIRED:OPTION_ID_OR_NAME}}`

### 7.2 Normative effect

{{REQUIRED:Describe which canonical objects, requirements, locks, profiles, or contracts are added, changed, superseded, or prohibited.}}

### 7.3 Required behavior

- {{REQUIRED:Behavior that implementations and documentation must preserve.}}

### 7.4 Prohibited behavior

- {{REQUIRED:Behavior that is explicitly disallowed.}}

### 7.5 Defaults

- {{REQUIRED:State every default introduced by the decision, or write "Not applicable."}}

### 7.6 Failure and safe-degradation behavior

{{REQUIRED:Define what happens when required authority, verification, compatibility, dependencies, resources, or integrations are unavailable.}}

## 8. Canonical Ownership and Data Boundaries

### 8.1 Canonical owner

- Owner registry or contract: `{{REQUIRED:REPO_RELATIVE_PATH}}`
- Owned JSON Pointer: `{{REQUIRED:#/JSON/POINTER}}`

### 8.2 Produced authoritative data

- {{REQUIRED:List authoritative data owned by the affected component or registry, or write "Not applicable."}}

### 8.3 Consumed authoritative data

- {{REQUIRED:List external authoritative data consumed through contracts, or write "Not applicable."}}

### 8.4 Forbidden direct access

- {{REQUIRED:List direct writes, reads, privilege paths, or cross-domain operations prohibited by the decision.}}

### 8.5 Gateways and contracts

- {{REQUIRED:List required gateway, API, event, manifest, or artifact contracts, or write "Not applicable."}}

## 9. Profile and Deployment Effects

| Profile or overlay | Effect | Required | Permitted | Prohibited | Conformance impact |
| --- | --- | ---: | ---: | ---: | --- |
| `{{REQUIRED:PROFILE_ID}}` | {{REQUIRED:Effect}} | {{REQUIRED:true|false}} | {{REQUIRED:true|false}} | {{REQUIRED:true|false}} | {{REQUIRED:Impact}} |

<!-- TEMPLATE-INSTRUCTION
Every active profile affected directly or transitively should appear. Explicitly
state "No semantic effect" for reviewed profiles that remain unchanged.
-->

## 10. Security, Privacy, Rights, and AI Effects

### 10.1 Security effects

{{REQUIRED:Describe changes to trust, privilege, secrets, network, storage, signatures, supply chain, or audit. Write "Not applicable." only after explicit review.}}

### 10.2 Privacy and disclosure effects

{{REQUIRED:Describe data exposure, disclosure boundaries, retention, export, or user notice effects.}}

### 10.3 Cultural rights and consent effects

{{REQUIRED:Describe cultural-rights and consent effects, or write "Not applicable." after explicit review.}}

### 10.4 AI-boundary effects

{{REQUIRED:State whether the decision introduces, removes, or changes native or external AI capability. Confirm user initiation, data transfer, authoritative-write restrictions, provenance, and optional-removal behavior where applicable.}}

## 11. Offline, Resource, and Operational Effects

### 11.1 Offline behavior

{{REQUIRED:Describe behavior without Internet access and the minimum preserved capability.}}

### 11.2 Resource envelope

{{REQUIRED:Describe CPU, memory, storage, I/O, concurrency, and heavy-job effects.}}

### 11.3 Observability

{{REQUIRED:Define health, readiness, metrics, logs, receipts, and diagnostic evidence introduced or changed.}}

### 11.4 Backup, restore, and exit

{{REQUIRED:Describe effects on backup, verified restore, portability, and independent exit.}}

### 11.5 Incident and recovery behavior

{{REQUIRED:Describe operational failure handling, rollback, forward repair, and recovery.}}

## 12. Compatibility and Lifecycle

### 12.1 Compatibility class

`{{REQUIRED:backward_compatible|conditionally_compatible|breaking}}`

### 12.2 Affected release channels

- `{{REQUIRED:system|services|governance|knowledge}}`

### 12.3 Artifact and schema effects

- {{REQUIRED:List changed artifact classes, schemas, manifests, receipts, or release-set constraints.}}

### 12.4 Deprecation effects

- {{REQUIRED:List deprecated objects and replacement identifiers, or write "Not applicable."}}

### 12.5 Identifier preservation

{{REQUIRED:State how retired identifiers remain reserved and how supersedes/replaced_by links are preserved.}}

## 13. Migration Plan

### 13.1 Preconditions

- {{REQUIRED:Precondition.}}

### 13.2 Migration steps

1. {{REQUIRED:Canonical-first migration step.}}
2. {{REQUIRED:Dependent update step.}}
3. {{REQUIRED:Regeneration and validation step.}}
4. {{REQUIRED:Authority activation step.}}


### 13.4 Redirects and compatibility period

- {{REQUIRED:List path or identifier redirects and their retention period, or write "Not applicable."}}

## 14. Rollback and Forward Repair

### 14.1 Rollback trigger

{{REQUIRED:Define objective conditions that require rollback.}}

### 14.2 Rollback unit

{{REQUIRED:Define the complete authority, release, artifact, schema, and data unit restored atomically.}}

### 14.3 Rollback procedure

1. {{REQUIRED:Procedure step.}}
2. {{REQUIRED:Procedure step.}}

### 14.4 Forward repair

{{REQUIRED:Describe when forward repair is permitted and why rollback may be unsafe, or write "Not applicable."}}

### 14.5 Last known valid state

- Authority manifest: `{{REQUIRED:REFERENCE_OR_GENERATED_AT_ACTIVATION}}`
- Release Set: `{{OPTIONAL:REFERENCE_OR_NOT_APPLICABLE}}`
- Data or artifact snapshot: `{{OPTIONAL:REFERENCE_OR_NOT_APPLICABLE}}`

## 15. Interfile Alignment Impact

### 15.1 Impact report

- `{{REQUIRED:generated/impact/IMPACT-YYYY-MM-DD-DEC-ID.json}}`

### 15.2 Modified canonical references

- `{{REQUIRED:REPO_RELATIVE_PATH#JSON_POINTER}}`

### 15.3 Affected documents

| Document ID | Disposition | Reason |
| --- | --- | --- |
| `{{REQUIRED:DOC_ID}}` | `{{REQUIRED:updated|reviewed_no_change|regenerated|deprecated|blocked}}` | {{REQUIRED:Reason}} |

### 15.4 Affected locks

| Lock ID | Disposition | Validation effect |
| --- | --- | --- |
| `{{REQUIRED:LOCK_ID}}` | `{{REQUIRED:unchanged|updated|superseded|introduced}}` | {{REQUIRED:Effect}} |

### 15.5 Affected requirements

| Requirement ID | Disposition | Validation effect |
| --- | --- | --- |
| `{{REQUIRED:REQ_ID}}` | `{{REQUIRED:unchanged|updated|superseded|introduced}}` | {{REQUIRED:Effect}} |

### 15.6 Generated artifacts

- {{REQUIRED:List catalogs, matrices, manifests, metadata blocks, and AI contexts that must be regenerated.}}

## 16. Validation and Evidence

### 16.1 Required tests

| Test ID | Purpose | Required result |
| --- | --- | --- |
| `{{REQUIRED:TEST_ID}}` | {{REQUIRED:Purpose}} | `pass` |

### 16.2 Required evidence

| Evidence ID | Evidence type | Location |
| --- | --- | --- |
| `{{REQUIRED:EVID_ID}}` | {{REQUIRED:Type}} | `{{REQUIRED:REPO_RELATIVE_PATH_OR_MANIFEST_REF}}` |

### 16.3 Required validation commands

```bash
python docs/tools/generate_docs.py --check
python docs/tools/check_normative_language.py
python docs/tools/check_language.py
python docs/tools/check_canonical_ownership.py
python docs/tools/check_interfile_locks.py
python docs/tools/check_generated_content.py
python docs/tools/check_document_graph.py
python docs/tools/check_traceability.py
python docs/tools/check_decision_closure.py
python docs/tools/check_no_unresolved_state.py
python docs/tools/compute_impact.py --check-clean
python docs/tools/build_ai_context.py --check
python docs/tools/check_clean_repository.py
python docs/tools/validate_docs.py
```

### 16.4 Decision-specific validation

- {{REQUIRED:List profile, component, security, AI-boundary, lifecycle, migration, or development-isolation validators required by this ADR.}}

### 16.5 Acceptance criteria

1. {{REQUIRED:Objectively testable criterion.}}
2. {{REQUIRED:Objectively testable criterion.}}
3. All affected objects have a final impact disposition.
4. All required checks complete successfully.
5. `authority.registry.json` references the exact validated paths, versions, and statuses.

## 17. Consequences

### 17.1 Positive consequences

- {{REQUIRED:Positive consequence.}}

### 17.2 Negative consequences and costs

- {{REQUIRED:Negative consequence or ongoing cost.}}

### 17.3 Operational obligations

- {{REQUIRED:Ongoing operational obligation.}}

### 17.4 Documentation obligations

- {{REQUIRED:Ongoing documentation, generation, validation, or review obligation.}}

### 17.5 Technical debt explicitly accepted

{{REQUIRED:List accepted technical debt with bounded scope and removal condition, or write "Not applicable."}}

## 18. Rejected Alternatives

| Alternative | Reason rejected | Reconsideration trigger |
| --- | --- | --- |
| {{REQUIRED:Alternative}} | {{REQUIRED:Reason}} | {{REQUIRED:Objective trigger or "None"}} |

Rejected alternatives SHALL NOT be implemented as undocumented exceptions.

## 19. Exceptions and Waivers

{{REQUIRED:List accepted EXC identifiers and exact bounded scope, or write "Not applicable."}}

An exception does not change this ADR. A semantic exception requires its own accepted decision and, when architectural, a superseding ADR.

## 20. Implementation Guidance

<!-- TEMPLATE-INSTRUCTION
This section is non-normative unless a canonical profile or contract explicitly
adopts a referenced implementation detail. Do not place canonical enums,
defaults, or required behavior only in this section.
-->

{{REQUIRED:Provide implementation guidance, sequencing hints, or reference patterns, or write "Not applicable."}}

## 21. Decision Record

### 21.1 Decision authority record

- Decision ID: `{{REQUIRED:DEC_ID}}`
- Decision status: `{{REQUIRED:accepted|rejected|deprecated|superseded|archived}}`
- Decision owner: `{{REQUIRED:OWNER_ID}}`
- Decision registry reference: `{{REQUIRED:generated/decision-index.json#/decisions/...}}`

### 21.2 Review record

| Role | Identifier | Result | Date |
| --- | --- | --- | --- |
| Author | `{{REQUIRED:ACTOR_ID}}` | `submitted` | `{{REQUIRED:YYYY-MM-DD}}` |
| Canonical owner | `{{REQUIRED:ACTOR_ID}}` | `approved|rejected` | `{{REQUIRED:YYYY-MM-DD}}` |
| Architecture reviewer | `{{REQUIRED:ACTOR_ID}}` | `approved|rejected` | `{{REQUIRED:YYYY-MM-DD}}` |
| Validation pipeline | `automated` | `pass|fail|blocked` | `{{REQUIRED:YYYY-MM-DD}}` |
| Authority activator | `{{REQUIRED:ACTOR_ID}}` | `activated|not_activated` | `{{REQUIRED:YYYY-MM-DD}}` |

### 21.3 Machine-readable change summary

```json
{
  "change_id": "{{REQUIRED:CHG-YYYY-NNNN}}",
  "decision_ids": [
    "{{REQUIRED:DEC_ID}}"
  ],
  "modified_canonical_refs": [
    "{{REQUIRED:REPO_RELATIVE_PATH#JSON_POINTER}}"
  ],
  "affected_document_ids": [
    "{{REQUIRED:DOC_ID}}"
  ],
  "requirement_ids": [],
  "lock_ids": [],
  "exception_ids": [],
  "adr_ids": [
    "ADR-{{REQUIRED:NNN}}"
  ],
  "test_ids": [],
  "evidence_ids": [],
  "tests_run": [],
  "impact_report": "{{REQUIRED:generated/impact/IMPACT-YYYY-MM-DD-DEC-ID.json}}",
  "validation_status": "{{REQUIRED:pass|fail|blocked}}"
}
```

## 22. Supersession and Historical Integrity

When this ADR is superseded:

1. its status changes to `superseded`;
2. `superseded_by` references the replacement ADR;
3. the replacement ADR references this ADR through `supersedes`;
4. the original identifier and path remain reserved;
5. historical decisions, impact reports, validation evidence, and authority manifests remain available;
6. generated indexes are regenerated;
7. AI context packages stop treating this ADR as active authority.

This ADR SHALL NOT be deleted after acceptance, rejection, deprecation, or supersession.
