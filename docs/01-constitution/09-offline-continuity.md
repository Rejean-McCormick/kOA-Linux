<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONST-009",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "constitution",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/offline_continuity",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-SYS-OFFLINE-001",
    "DEC-SYS-AI-001",
    "DEC-ARI-001",
    "DEC-MEDIATHEQUE-001",
    "DEC-UCKK-EXT-001",
    "DEC-SENT-001"
  ],
  "requirement_ids": [
    "REQ-CONST-OFFLINE-001",
    "REQ-CONST-OFFLINE-002",
    "REQ-CONST-OFFLINE-003",
    "REQ-CONST-OFFLINE-004",
    "REQ-CONST-OFFLINE-005",
    "REQ-CONST-OFFLINE-006",
    "REQ-CONST-OFFLINE-007",
    "REQ-CONST-OFFLINE-008",
    "REQ-CONST-OFFLINE-009",
    "REQ-CONST-OFFLINE-010",
    "REQ-CONST-OFFLINE-011",
    "REQ-CONST-OFFLINE-012",
    "REQ-CONST-OFFLINE-013",
    "REQ-CONST-OFFLINE-014",
    "REQ-CONST-OFFLINE-015",
    "REQ-CONST-OFFLINE-016",
    "REQ-CONST-OFFLINE-017",
    "REQ-CONST-OFFLINE-018",
    "REQ-CONST-OFFLINE-019",
    "REQ-CONST-OFFLINE-020"
  ],
  "lock_ids": [
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SENT-001",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-UCKK-EXT-001",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-DATA-001",
    "LOCK-PROFILE-001",
    "LOCK-UCKK-EXT-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008"
  ],
  "tags": [
    "offline-continuity",
    "safe-degradation",
    "fail-closed",
    "external-integrations",
    "ai-boundary",
    "ariane",
    "koa_mediatheque",
    "uckk_publication",
    "sentient",
    "resilience"
  ]
}
KOA:DOC-META:END -->

# Offline Continuity

## 1. Purpose

This document establishes offline continuity as a global constitutional property of the kOA-Linux Operating System.

Offline continuity means that loss of Internet access, external providers, remote peers, external AI surfaces, or optional network services does not collapse the local core. The system continues to expose the locally available capabilities that its active profile classifies as continuous, while unavailable or unsafe operations become explicitly degraded, deferred, or blocked.

Offline continuity does not mean that every capability is available without a network. It means that every capability has declared behavior, preserved authority boundaries, observable state, safe failure behavior, and testable recovery behavior when dependencies are absent.

## 2. Scope

This document applies globally to:

- every deployment profile and profile overlay;
- every component and component contract;
- local identity, authorization, and trust evaluation;
- authoritative local data and local state transitions;
- cross-component communication;
- external integrations and federation peers;
- external AI surfaces;
- Ariane navigation and voice capabilities;
- kOA Mediatheque ingestion, indexing, retrieval, downloaded learning packages, and governed UCKK interchange;
- SenTient when installed in an eligible profile;
- pending work, synchronization, recovery, and reconciliation;
- resource governance and capability degradation;
- conformance tests and operational evidence.

Profile contracts may define a broader offline envelope. They may not narrow the global baseline while claiming unqualified conformance.

This document does not require an external-only operation to become local. It requires that the operation's unavailability be explicit and that unrelated local capabilities remain safe and usable.

## 3. Canonical References

Canonical ownership is distributed as follows:

| Subject | Canonical owner |
| --- | --- |
| Global offline model and capability behavior | `contracts/system.contract.json#/offline_continuity` |
| Component identity, responsibility, owned data, and dependencies | `generated/component-catalog.json` |
| Profile-specific offline envelopes | `contracts/profiles/*.profile.json` |
| External integration classification and removal behavior | `contracts/integration-types.contract.json` |
| Requirement statements and strength | `generated/requirements-index.json` |
| Cross-file invariants | `generated/assertion-index.json` |
| Requirement, test, and evidence relationships | `generated/traceability.json` |
| Test definitions | `generated/test-catalog.json` |
| Conformance evidence | `generated/evidence-catalog.json` |
| Accepted architectural decisions | `generated/decision-index.json` |
| Active versions and authority order | `generated/authority-manifest.json` |

This document explains the constitutional meaning of offline continuity. It does not duplicate the machine-readable capability inventory or profile envelope.

## 4. Model and Responsibilities

### 4.1 Offline behavior categories

The system registry and profile contracts classify each capability using a registered offline behavior. The categories have these meanings:

| Behavior | Meaning |
| --- | --- |
| `continuous` | The capability operates locally without Internet or an external provider. |
| `degraded` | A safe local subset remains available and unavailable functions are explicit. |
| `deferred` | The requested external effect is recorded as pending and executed only after dependencies return and validation passes. |
| `unavailable` | The capability is disabled without claiming success or changing protected authority. |
| `offline_transfer` | The capability uses a validated import or export bundle rather than a live network path. |

A capability may have different behavior in different profiles, but the profile declaration cannot contradict global locks.

### 4.2 Local core

The local core consists of the capabilities that the active system and profile registries classify as continuous. Its composition is machine-readable and profile-aware.

The local core includes no implicit dependency on:

- Internet access;
- external AI;
- external voice processing;
- optional federation peers;
- optional developer workbenches;
- SenTient;
- provider-managed storage or identity;
- remote synchronization.

A locally continuous capability may still reject an unsafe operation when required policy, trust, authorization, compatibility, or authoritative data is unavailable.

### 4.3 Authority during disconnection

Disconnection does not create new authority.

Local authoritative state remains owned by its canonical component. Cached data, replicated data, queued operations, generated suggestions, external outputs, and synchronization payloads do not become authoritative merely because the network is unavailable.

A component does not write directly to another component's authoritative source during connected or disconnected operation.

### 4.4 External integrations

Every integration declares whether it is optional or profile-conditional, which capability it provides, which data crosses the boundary, whether work can be queued, how credentials are referenced, how failure is presented, and what local behavior remains after removal.

UCKK is an optional online Moodle learning and dissemination platform. Its unavailability does not disable the kOA Mediatheque or any already accepted local package.

Two UCKK directions are classified separately:

- `publish_to_uckk` is a deferred external disclosure operation that requires current Publication Gateway authorization before delivery;
- `import_from_uckk` is a controlled acquisition operation that requires explicit selection, source and license verification, integrity and compatibility checks, quarantine, and local acceptance.

The approved external AI surfaces remain user-triggered adapters. Their outputs remain candidate inputs until accepted through an authoritative local workflow.

### 4.5 Ariane, the two Mediatheques, and SenTient

Ariane local navigation is independent of external voice and external AI. Loss of the approved voice adapter removes voice capability but not local navigation.

The kOA Mediatheque is the local, private-by-default, offline authority. It can preserve locally authored instructions and imported UCKK learning packages for disconnected use.

The UCKK Mediatheque is the online authority for UCKK courses, learning paths, activities, permissions, and remote content lifecycle. A shared Mediatheque frame makes explicit exchange possible but does not merge storage, identity, access control, lifecycle, or authority.

Suno and Gamma remain optional user-triggered integrations and do not define local media authority.

SenTient is an optional, isolated, non-authoritative workbench available only in eligible profiles. It is not part of the default user baseline and is not a continuity dependency.

### 4.6 Pending operations and reconciliation

A deferred operation has an explicit lifecycle. Outbound UCKK publication and inbound UCKK acquisition use separate records, queues, receipts, and reconciliation rules; they are never collapsed into a generic synchronization state:

`text
requested
recorded_pending
eligible_for_retry
submitted
externally_confirmed
locally_reconciled
completed
`

It may instead end as:

`text
cancelled
expired
rejected
conflicted
failed
`

No transition to `completed` occurs before the external effect and local reconciliation are verified.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-CONST-OFFLINE-001,REQ-CONST-OFFLINE-002,REQ-CONST-OFFLINE-003,REQ-CONST-OFFLINE-004,REQ-CONST-OFFLINE-005,REQ-CONST-OFFLINE-006,REQ-CONST-OFFLINE-007,REQ-CONST-OFFLINE-008,REQ-CONST-OFFLINE-009,REQ-CONST-OFFLINE-010,REQ-CONST-OFFLINE-011,REQ-CONST-OFFLINE-012,REQ-CONST-OFFLINE-013,REQ-CONST-OFFLINE-014,REQ-CONST-OFFLINE-015,REQ-CONST-OFFLINE-016,REQ-CONST-OFFLINE-017,REQ-CONST-OFFLINE-018,REQ-CONST-OFFLINE-019,REQ-CONST-OFFLINE-020 -->
- **REQ-CONST-OFFLINE-001 — SHALL:** Every active system profile preserve the global offline-continuity baseline for all capabilities classified as locally continuous.
- **REQ-CONST-OFFLINE-002 — SHALL:** Every active profile declare a machine-readable offline capability envelope and bind each declared capability to validation evidence.
- **REQ-CONST-OFFLINE-003 — SHALL NOT:** Failure, removal, misconfiguration, or unavailability of an optional external integration disable an unrelated locally continuous capability.
- **REQ-CONST-OFFLINE-004 — SHALL:** Locally available authoritative data remain readable offline when the requesting actor is locally authenticated and the applicable access policy can be evaluated.
- **REQ-CONST-OFFLINE-005 — SHALL:** A state-changing operation that requires unavailable authority, unavailable policy, unavailable trust material, or an incompatible contract fail closed.
- **REQ-CONST-OFFLINE-006 — SHALL NOT:** An operation that depends on an unavailable external system report success, completion, publication, synchronization, or acceptance before that external effect is verified.
- **REQ-CONST-OFFLINE-007 — SHALL:** A deferred external operation preserve an explicit pending state, its initiating identity, its intended destination, its payload reference, and its provenance until completion or cancellation.
- **REQ-CONST-OFFLINE-008 — SHALL:** Every offline retry mechanism be idempotent or detect and reject duplicate effects before changing authoritative state.
- **REQ-CONST-OFFLINE-009 — SHALL NOT:** Reconnection or synchronization silently overwrite divergent authoritative state, discard a conflict, or choose a winner without the applicable conflict policy.
- **REQ-CONST-OFFLINE-010 — SHALL:** ChatGPT, Suno, Gamma, and the approved Ariane voice adapter remain optional external surfaces whose unavailability does not disable the local core.
- **REQ-CONST-OFFLINE-011 — SHALL:** Ariane provide local non-voice navigation without Internet access, external AI, or the approved external voice adapter.
- **REQ-CONST-OFFLINE-012 — SHALL:** Native kOA Mediatheque ingestion, routing, local indexing, and local retrieval remain deterministic and non-AI within the capability envelope of the active profile.
- **REQ-CONST-OFFLINE-013 — SHALL NOT:** SenTient be required for the default user baseline, offline continuity, authoritative routing, policy evaluation, or activation of core kOA capabilities.
- **REQ-CONST-OFFLINE-014 — SHALL NOT:** Offline fallback copy credentials, secrets, tokens, private keys, or unrestricted sensitive payloads into ordinary logs, receipts, queues, diagnostics, or exports.
- **REQ-CONST-OFFLINE-015 — SHALL:** Cached authorization and trust material have explicit scope, provenance, validity limits, and revocation behavior; sensitive operations fail closed when current authorization cannot be established.
- **REQ-CONST-OFFLINE-016 — SHALL:** Restart, recovery, or power-loss handling preserve committed local authoritative state and recover or explicitly invalidate pending offline operations.
- **REQ-CONST-OFFLINE-017 — SHALL:** The Resource Governor remain operational offline or the system apply a documented conservative resource envelope that prevents optional work from exhausting core capability resources.
- **REQ-CONST-OFFLINE-018 — SHALL:** Offline failures and degraded capabilities produce local, machine-readable status without disclosing secrets or misrepresenting unavailable external effects as completed.
- **REQ-CONST-OFFLINE-019 — SHALL:** Every capability declare whether offline behavior is continuous, degraded, deferred, unavailable, or provided through an offline transfer mode.
- **REQ-CONST-OFFLINE-020 — SHALL:** Offline-continuity conformance include tested Internet denial, name-resolution failure, provider outage, restart while disconnected, queued-operation recovery, reconnection conflict, and optional-integration removal.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Entering disconnected operation

When a required network path becomes unavailable, the system:

1. records the dependency state;
2. recalculates affected capability availability from canonical system and profile declarations;
3. preserves continuous capabilities;
4. exposes degraded, deferred, or unavailable states explicitly;
5. blocks unsafe mutations;
6. retains already committed authoritative state;
7. protects pending work from duplication or silent loss;
8. emits local operational status;
9. avoids repeated uncontrolled retry loops.

Disconnected operation is a normal operating condition, not an implicit emergency or break-glass mode.

### 6.2 Creating deferred work

Before an external effect is deferred, the initiating component records:

- the initiating actor or local service identity;
- the requested capability;
- the destination integration or peer;
- a reference to the minimized payload;
- consent and disclosure state where applicable;
- required policy and compatibility context;
- creation and expiry times;
- retry and cancellation rules;
- provenance and expected evidence.

Secrets remain in managed secret stores and are referenced rather than copied into the queue.

### 6.3 Reconnection

After dependencies return, the system:

1. revalidates identity, authorization, trust, policy, and compatibility;
2. verifies that the operation has not expired or been cancelled;
3. detects already-applied external or local effects;
4. submits eligible work in a controlled order;
5. records external confirmation;
6. detects conflicts before local reconciliation;
7. applies the owning component's conflict policy;
8. records evidence and final status.

Reconnection does not authorize an operation that was unsafe or unauthorized while disconnected.

### 6.4 Restart and recovery

After restart while disconnected, the system reconstructs:

- committed local authoritative state;
- pending operations;
- capability availability;
- expiration and retry state;
- required resource limits;
- observable degradation status.

A pending record that cannot be validated becomes blocked or invalidated explicitly rather than being guessed or replayed.

### 6.5 Removing an optional integration

Removal validation confirms that:

- no core capability depends on the integration;
- locally owned authoritative data remains available;
- pending work is completed, cancelled, exported, or explicitly abandoned;
- credentials and provider-specific state are removed safely;
- the user-visible capability becomes disabled, degraded, or replaced by a local workflow;
- no hidden retry process remains active.

## 7. Failure Modes and Safe Degradation

| Failure | Required behavior |
| --- | --- |
| Internet unavailable | Preserve continuous capabilities and classify all affected capabilities explicitly. |
| Name resolution unavailable | Treat remote endpoints as unavailable without repeated uncontrolled retries. |
| External provider unavailable | Disable or defer only the provider-dependent capability. |
| External AI surface unavailable | Preserve local core; external generation or processing remains unavailable. |
| Ariane voice unavailable | Preserve local non-voice navigation. |
| Policy or trust cannot be evaluated | Block the affected sensitive mutation while retaining safe read-only access where authorized. |
| Local queue storage unavailable | Reject new deferred work and preserve existing committed state. |
| Duplicate retry detected | Suppress or reject the duplicate before an authoritative effect occurs. |
| Reconnection conflict detected | Preserve both relevant states and invoke the canonical conflict policy. |
| Local clock trust is insufficient | Block expiry-sensitive or authorization-sensitive operations that cannot be evaluated safely. |
| Resource pressure | Suspend or reduce optional work before core capability resources are exhausted. |
| Corrupted pending record | Quarantine the record, preserve evidence, and prevent replay. |

Safe degradation is capability-specific. A failure in one capability does not justify disabling unrelated local functions.

## 8. Security and Trust Boundaries

Offline continuity preserves the same component, identity, data, disclosure, and privilege boundaries used during connected operation.

Security rules include:

- local authentication does not imply authorization for every local mutation;
- cached authorization is bounded by declared validity and scope;
- revocation uncertainty is handled according to capability risk;
- sensitive mutations remain blocked when current authority cannot be established;
- external outputs remain non-authoritative;
- queued payloads are minimized and protected;
- secrets are referenced through managed secret mechanisms;
- logs and receipts exclude unrestricted sensitive content;
- synchronization never bypasses the owning component;
- offline imports use authenticated manifests and applicable artifact validation;
- break-glass behavior is separate, explicit, time-bounded, and auditable.

A profile may impose stricter rules, including shorter cache validity, stronger offline signatures, or complete blocking of selected mutations.

## 9. Exceptions and Compatibility

Offline continuity is a constitutional property and cannot be removed through an undocumented profile choice or implementation shortcut.

An exception may apply only to a bounded deployment, release, component instance, artifact instance, workspace, or migration action. It cannot:

- create a global dependency on an optional integration;
- make external AI authoritative;
- make Ariane local navigation depend on external voice;
- make SenTient part of the default user baseline;
- permit direct writes across component ownership boundaries;
- authorize a false conformance claim;
- convert an unavailable external effect into reported success.

Compatibility behavior is explicit for every persisted queue, synchronization record, offline bundle, and local authority format. An incompatible version blocks activation or reconciliation until rollback, migration, or forward repair is validated.

A profile with a narrower declared offline envelope may be distributed only with a qualified claim that identifies the missing constitutional capability and the active exception or waiver. Unqualified conformance remains blocked.

## 10. Validation Criteria

This document is conformant when validation confirms:

1. every active profile declares an offline capability envelope;
2. every registered capability has one offline behavior;
3. every optional integration has tested removal behavior;
4. the four approved external AI surfaces remain optional and non-authoritative;
5. Ariane local navigation passes without Internet, AI, or external voice;
6. native kOA Mediatheque paths remain deterministic and non-AI;
7. SenTient is absent from the default user baseline and is not a continuity dependency;
8. local authoritative reads and protected mutations follow declared access and policy behavior;
9. deferred operations preserve identity, provenance, state, expiry, and cancellation;
10. retry and reconciliation tests prevent duplicate or silent conflicting effects;
11. restart while disconnected preserves committed state and pending work;
12. queue, diagnostic, and receipt outputs contain no secrets;
13. resource-pressure tests protect core capabilities before optional work;
14. provider outage affects only dependent capabilities;
15. incompatible offline records fail closed;
16. conformance evidence covers the failure conditions named by the applicable requirements.

The principal validation entry point is:

`bash
python docs/tools/validate_docs.py
`

Supporting checks include:

`text
tools/check_interfile_locks.py
tools/check_ai_boundary.py
tools/check_component_boundaries.py
tools/check_profile_inheritance.py
tools/check_release_sets.py
tools/check_traceability.py
`

## 11. Non-Normative Examples

### 11.1 Ariane without network access

A user loses Internet connectivity while navigating local applications. Ariane continues to expose local non-voice navigation. The external voice control is shown as unavailable. No local navigation capability is reported as failed.

### 11.2 kOA Mediatheque local ingestion

A user imports a local media file. Native kOA Mediatheque validation, ingestion, routing, indexing, and retrieval continue through deterministic local paths. A request to use Suno or Gamma remains unavailable until the user reconnects and explicitly invokes the adapter.

### 11.3 Deferred UCKK publication

A user prepares a learning resource for UCKK while the online platform is unavailable. The local source remains private and authoritative in the kOA Mediatheque. A minimized publication request is recorded as pending, not published. After reconnection, rights, consent, authorization, source version, destination, and expiry are revalidated before packaging and delivery.

### 11.4 Authorization uncertainty

A locally authenticated user requests a sensitive mutation, but the required current authorization state cannot be established. The mutation is blocked. Locally authorized read-only access may remain available if the applicable policy permits it.

### 11.5 Optional workbench removal

SenTient is removed from a developer workspace. Core kOA services, Ariane local navigation, deterministic kOA Mediatheque paths, and authoritative component data continue. Features provided only by SenTient become unavailable without changing system authority.

### 11.6 Isolated-school learning package

An isolated school receives a verified UCKK course bundle by intermittent network or removable media. The system validates the source, license, manifest, signatures, hashes, compatibility, and required local resources. The kOA Mediatheque accepts a local copy with preserved UCKK provenance. Students consult the installed course offline. Later UCKK changes are presented as a new import candidate and never overwrite the local copy silently.

