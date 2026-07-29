# System Context

## 1. Context statement

kOA Linux sits between maintained hardware/Linux mechanisms and the kOA product ecosystem. It provides an appliance-grade runtime rather than a new social application.

```text
People and institutions
        |
        v
koa-session-shell
  |             |
  v             v
Konnaxion      Orgo
       \       /
        v     v
     Kristal Runtime
           |
           v
kOA Governance and Node Runtime
           |
           v
Linux + hardware
```

## 2. External actors

- **participant**: learns, contributes, deliberates, votes, creates, or collaborates;
- **operator**: maintains node availability without owning civic meaning;
- **tenant administrator**: manages tenant policy within delegated authority;
- **reviewer/approver**: performs workflow decisions;
- **auditor**: inspects selected receipts and evidence;
- **authority channel**: validates or recognizes artifacts within a scope;
- **external system**: submits signals or consumes approved outputs;
- **release authority**: signs compatible release artifacts;
- **recovery custodian**: restores nodes and trust under a defined break-glass process.

## 3. Principal product relationships

### 3.1 Konnaxion

Konnaxion is the open/global plane. It consumes Kristal artifacts for search, navigation, education, civic workflows, curation, and offline access. It produces public contributions, deliberation outputs, and requests that may become Orgo work.

### 3.2 Orgo

Orgo is the private/organizational plane. It receives signals, creates Cases and Tasks, routes responsibility, executes approvals, manages sensitive workflows, and records operational outcomes. It orchestrates work around Kristal but does not own Kristal semantics.

### 3.3 Kristal

Kristal is the shared epistemic substrate. It carries portable state, provenance, validation, authority recognition, federation, reader-policy metadata, query contracts, and Runtime Packs.

### 3.4 Specialized engines

SenTient resolves ambiguity when resolution is required. Architect renders deterministic, traceable output from validated query results. Neither engine is required on every endpoint.

## 4. Context boundaries

The system MUST distinguish:

- local node state from federated state;
- tenant state from global content identity;
- operational workflow from epistemic payload;
- public disclosure from private evidence;
- advisory computation from binding decisions;
- governance authorization from Linux privilege;
- active artifacts from installed, cached, quarantined, revoked, or expired artifacts.

## 5. Trust assumptions

The architecture assumes that:

- networks fail and may be hostile;
- services become slow, unavailable, or compromised;
- administrators can make mistakes or abuse privilege;
- signing keys can be lost or revoked;
- governance rules can drift or be captured;
- AI can hallucinate, bias, or overreach;
- storage can corrupt;
- clocks can be wrong;
- federation peers may disagree legitimately.

No design may rely on the opposite assumptions for correctness.
