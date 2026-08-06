<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SEC-022",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "security",
  "scope": [
    "global",
    "profile_conditioned_security"
  ],
  "canonical_refs": [
    "contracts/security-controls.contract.json",
    "schemas/security-controls.contract.schema.json",
    "contracts/artifact-contracts/security-evidence.schema.json",
    "07-security/21-security-control-architecture.md",
    "03-profiles/00-profile-model.md",
    "09-conformance/04-profile-test-matrices.md",
    "09-conformance/05-test-evidence.md"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-SEC-CTRL-002",
    "LOCK-SEC-CTRL-003",
    "LOCK-SEC-CTRL-006",
    "LOCK-SEC-CTRL-008"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SEC-021",
    "DOC-PRO-000",
    "DOC-CONF-004",
    "DOC-CONF-005"
  ],
  "tags": [
    "security",
    "control-matrix",
    "profiles",
    "applicability",
    "conformance"
  ]
}
KOA:DOC-META:END -->

# Security Control Profile Matrix

## 1. Purpose

This document is the human-readable profile projection of `contracts/security-controls.contract.json`. The contract is the canonical owner of control identity and applicability. This matrix does not independently change a control state.

## 2. Legend

| Code | State | Meaning |
| --- | --- | --- |
| `R` | `required` | Passing evidence is mandatory for the profile claim. |
| `C` | `recommended` | Expected unless an accepted architecture decision bounds the risk. |
| `O` | `optional` | May be enabled; when enabled, the complete control applies. |
| `P` | `prohibited` | The represented behavior is forbidden for the profile. |
| `N` | `not_applicable` | The profile does not own or expose the controlled surface. |

Profile codes:

| Code | Profile contract |
| --- | --- |
| `UL` | `user_lightweight` — User Lightweight |
| `DL` | `developer_linux_workstation` — Developer Linux Workstation |
| `DW` | `developer_windows_wsl` — Developer Windows WSL |
| `SL` | `sovereign_linux_node` — Sovereign Linux Node |
| `SH` | `sovereign_hub` — Sovereign Hub |
| `BF` | `build_farm` — Build Farm |
| `CP` | `control_plane` — Control Plane |
| `HA` | `high_assurance` — High Assurance |
| `SO` | `sovereign_offline` — Sovereign Offline Overlay |
| `AS` | `appliance_shell` — Appliance Shell Overlay |

## 3. Composition Rules

- A base profile SHALL include every control classified `R` for that profile.
- An overlay SHALL preserve or strengthen required controls from its base profile.
- `N` requires evidence that the controlled surface is absent or owned outside the profile boundary.
- A control marked `C` that is omitted from a production, sovereign, or high-assurance deployment requires an accepted risk rationale.
- A control marked `O` becomes fully normative when the feature or surface is enabled.
- A profile SHALL NOT claim conformance while a `P` behavior is present.
- This matrix does not make hardware unavailable by policy. Applicability conditions in the contract determine whether the deployment owns the relevant surface.

## 4. Control Matrix

### 4.1 Security governance and control architecture

| Control | Objective | UL | DL | DW | SL | SH | BF | CP | HA | SO | AS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SEC-GOV-001` | Current scoped threat model | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |
| `SEC-GOV-002` | Explicit control applicability by profile | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |
| `SEC-GOV-003` | Control implementation validation and evidence binding | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |
| `SEC-GOV-004` | Bounded security exceptions | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |

### 4.2 Platform integrity and activation

| Control | Objective | UL | DL | DW | SL | SH | BF | CP | HA | SO | AS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SEC-PLATFORM-001` | Verified boot chain | `R` | `C` | `N` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |
| `SEC-PLATFORM-002` | Immutable verified system root | `R` | `C` | `N` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |
| `SEC-PLATFORM-003` | Atomic update and last-known-good rollback | `R` | `C` | `N` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |
| `SEC-PLATFORM-004` | Separate verified recovery environment | `C` | `C` | `N` | `R` | `R` | `O` | `R` | `R` | `R` | `C` |
| `SEC-PLATFORM-005` | Hardware-rooted platform evidence by assurance level | `O` | `O` | `N` | `C` | `C` | `C` | `C` | `R` | `C` | `O` |

### 4.3 Identity and authorization

| Control | Objective | UL | DL | DW | SL | SH | BF | CP | HA | SO | AS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SEC-ID-001` | Distinct human device service artifact and release identities | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |
| `SEC-ID-002` | Phishing-resistant privileged and remote authentication | `O` | `O` | `O` | `C` | `R` | `R` | `R` | `R` | `C` | `O` |
| `SEC-ID-003` | Bounded revocable credentials | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |
| `SEC-ID-004` | Authorization at the authoritative owner | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |

### 4.4 Privilege boundaries

| Control | Objective | UL | DL | DW | SL | SH | BF | CP | HA | SO | AS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SEC-PRIV-001` | Default deny and least privilege | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |
| `SEC-PRIV-002` | Closed typed privileged broker | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |
| `SEC-PRIV-003` | No arbitrary command path or unit through privilege boundary | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |

### 4.5 Service isolation

| Control | Objective | UL | DL | DW | SL | SH | BF | CP | HA | SO | AS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SEC-ISO-001` | Per-service principal and bounded runtime access | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |
| `SEC-ISO-002` | Mandatory access control sandboxing and resource bounds | `R` | `C` | `N` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |

### 4.6 Keys and secrets

| Control | Objective | UL | DL | DW | SL | SH | BF | CP | HA | SO | AS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SEC-KEY-001` | Secrets excluded from source images logs receipts and ordinary exports | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |
| `SEC-KEY-002` | Scoped offline root trust | `O` | `O` | `O` | `C` | `C` | `R` | `R` | `R` | `R` | `O` |
| `SEC-KEY-003` | Key rotation revocation and compromise response | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |
| `SEC-KEY-004` | Separated or threshold release signing by risk | `N` | `N` | `N` | `N` | `O` | `C` | `R` | `R` | `C` | `N` |

### 4.7 Network security

| Control | Objective | UL | DL | DW | SL | SH | BF | CP | HA | SO | AS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SEC-NET-001` | Inbound network deny by default | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |
| `SEC-NET-002` | Security-zone separation | `C` | `O` | `O` | `R` | `R` | `R` | `R` | `R` | `R` | `C` |
| `SEC-NET-003` | Declared outbound destinations for external integrations | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |
| `SEC-NET-004` | Authenticated encrypted cross-node communication | `O` | `O` | `O` | `C` | `R` | `C` | `R` | `R` | `R` | `O` |

### 4.8 Data security

| Control | Objective | UL | DL | DW | SL | SH | BF | CP | HA | SO | AS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SEC-DATA-001` | Data ownership classification retention and disclosure | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |
| `SEC-DATA-002` | Encryption and integrity for sensitive durable state | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |
| `SEC-DATA-003` | No direct cross-owner state access | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |

### 4.9 Offline import security

| Control | Objective | UL | DL | DW | SL | SH | BF | CP | HA | SO | AS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SEC-OFFLINE-001` | Quarantine for removable and offline imports | `C` | `O` | `N` | `C` | `C` | `O` | `O` | `R` | `R` | `C` |
| `SEC-OFFLINE-002` | Bounded parsing signature provenance and import receipts | `C` | `O` | `N` | `C` | `C` | `O` | `O` | `R` | `R` | `C` |

### 4.10 Software supply chain

| Control | Objective | UL | DL | DW | SL | SH | BF | CP | HA | SO | AS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SEC-SUPPLY-001` | Pinned source dependencies and images by digest | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |
| `SEC-SUPPLY-002` | Software bill of materials for released artifacts | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |
| `SEC-SUPPLY-003` | Build provenance for released artifacts | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |
| `SEC-SUPPLY-004` | Separated build approval signing and publication | `N` | `N` | `N` | `N` | `O` | `R` | `R` | `R` | `C` | `N` |
| `SEC-SUPPLY-005` | Vulnerability response revocation and anti-rollback metadata | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |

### 4.11 Secure development

| Control | Objective | UL | DL | DW | SL | SH | BF | CP | HA | SO | AS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SEC-DEV-001` | Mandatory review static dependency and secret analysis | `O` | `R` | `R` | `C` | `C` | `R` | `R` | `R` | `C` | `O` |
| `SEC-DEV-002` | Negative testing and fuzzing of parsers and privileged protocols | `O` | `C` | `C` | `C` | `C` | `R` | `R` | `R` | `C` | `O` |

### 4.12 Audit and detection

| Control | Objective | UL | DL | DW | SL | SH | BF | CP | HA | SO | AS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SEC-AUDIT-001` | Structured security event records | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |
| `SEC-AUDIT-002` | Tamper-evident bounded audit retention | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |
| `SEC-AUDIT-003` | Local audit continuity during network loss | `R` | `O` | `O` | `R` | `R` | `C` | `C` | `R` | `R` | `R` |
| `SEC-AUDIT-004` | Privacy-minimized selective security evidence | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |

### 4.13 Incident response

| Control | Objective | UL | DL | DW | SL | SH | BF | CP | HA | SO | AS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SEC-INC-001` | Detection alerting and containment ownership | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |
| `SEC-INC-002` | Incident evidence preservation and coordinated response | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |

### 4.14 Backup and recovery

| Control | Objective | UL | DL | DW | SL | SH | BF | CP | HA | SO | AS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SEC-REC-001` | Encrypted offline or immutable backup | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |
| `SEC-REC-002` | Regular restoration exercises | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |
| `SEC-REC-003` | Clean-room recovery and compromise reintroduction checks | `C` | `O` | `O` | `R` | `R` | `R` | `R` | `R` | `R` | `C` |
| `SEC-REC-004` | Profile-specific recovery objectives and evidence | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` | `R` |

## 5. Control Notes

The following conditions constrain interpretation of the compact matrix:

- `SEC-PLATFORM-001` — Not applicable when the profile does not own the host boot chain.
- `SEC-ID-002` applies to privileged or remote administrative access. A local profile with no administrative surface does not gain one merely to satisfy the control.
- `SEC-KEY-004` applies to release-signing authority. Endpoint profiles consume verified releases and do not become signing authorities.
- `SEC-NET-004` applies to cross-node sensitive communication. Same-host communication SHOULD prefer a bounded local interface such as a Unix socket when that provides the required identity and authorization properties.
- `SEC-OFFLINE-001` and `SEC-OFFLINE-002` apply when the deployment admits removable-media or offline packages. A profile SHALL NOT mark them not applicable while exposing such an import path.
- `SEC-PLATFORM-005` does not make attestation an ordinary application authorization mechanism.

## 6. Evidence Requirements

For each `R` control, the profile conformance set SHALL contain current evidence conforming to `contracts/artifact-contracts/security-evidence.schema.json`. Evidence scope SHALL match the profile, implementation version, release or subject, and active exception set.

Evidence for `C` controls SHALL be retained when the control is implemented. An omitted `C` control requires an accepted rationale before a production, sovereign, or high-assurance claim.

`O` controls SHALL NOT be reported as passing when the feature is disabled. The evidence result SHALL be `not_applicable`, or the control SHALL be absent from the enabled-feature claim, according to the owning conformance procedure.

## 7. Profile Summaries

### 7.1 `user_lightweight`

User Lightweight classification: **35 required**, **5 recommended**, **6 optional**, **0 prohibited**, and **2 not applicable** controls.

### 7.2 `developer_linux_workstation`

Developer Linux Workstation classification: **31 required**, **6 recommended**, **9 optional**, **0 prohibited**, and **2 not applicable** controls.

### 7.3 `developer_windows_wsl`

Developer Windows WSL classification: **31 required**, **1 recommended**, **6 optional**, **0 prohibited**, and **10 not applicable** controls.

### 7.4 `sovereign_linux_node`

Sovereign Linux Node classification: **38 required**, **8 recommended**, **0 optional**, **0 prohibited**, and **2 not applicable** controls.

### 7.5 `sovereign_hub`

Sovereign Hub classification: **40 required**, **6 recommended**, **2 optional**, **0 prohibited**, and **0 not applicable** controls.

### 7.6 `build_farm`

Build Farm classification: **41 required**, **4 recommended**, **3 optional**, **0 prohibited**, and **0 not applicable** controls.

### 7.7 `control_plane`

Control Plane classification: **44 required**, **2 recommended**, **2 optional**, **0 prohibited**, and **0 not applicable** controls.

### 7.8 `high_assurance`

High Assurance classification: **48 required**, **0 recommended**, **0 optional**, **0 prohibited**, and **0 not applicable** controls.

### 7.9 `sovereign_offline`

Sovereign Offline Overlay classification: **42 required**, **6 recommended**, **0 optional**, **0 prohibited**, and **0 not applicable** controls.

### 7.10 `appliance_shell`

Appliance Shell Overlay classification: **35 required**, **5 recommended**, **6 optional**, **0 prohibited**, and **2 not applicable** controls.

## 8. Validation

`tools/check_security_architecture.py` compares every table control identifier with the canonical contract, validates all profile references and applicability mappings, and rejects an omitted, duplicated, invented, or malformed control.
