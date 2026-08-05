<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ADR-005",
  "document_class": "adr",
  "version": "1.0.0",
  "status": "accepted",
  "language": "en",
  "layer": "architecture_decision",
  "owner": "profile-architecture",
  "scope": [
    "global",
    "profile:developer_linux_workstation",
    "profile:developer_windows_wsl",
    "profile:user_lightweight",
    "profile:sovereign_linux_node",
    "profile:sovereign_hub",
    "profile:build_farm",
    "profile:control_plane",
    "overlay:appliance_shell",
    "endpoint_runtime"
  ],
  "canonical_refs": [
    "contracts/profiles/developer-linux-workstation.profile.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "contracts/profiles/user-lightweight.profile.json",
    "contracts/profiles/sovereign-linux-node.profile.json",
    "contracts/profiles/sovereign-hub.profile.json",
    "contracts/profiles/build-farm.profile.json",
    "contracts/profiles/control-plane.profile.json",
    "contracts/terminology.contract.json",
    "contracts/system.contract.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json"
  ],
  "decision_ids": [
    "DEC-CONTAINER-001",
    "DEC-K8S-001",
    "DEC-PROFILE-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-IMPL-002",
    "REQ-PROFILE-001",
    "REQ-CONF-SLN-033",
    "REQ-CONF-SLN-034",
    "REQ-CONF-SLN-035",
    "REQ-CONF-SLN-036",
    "REQ-CONF-SLN-037",
    "REQ-CONF-SLN-038",
    "REQ-CONF-SLN-039",
    "REQ-CONF-SLN-040",
    "REQ-LIFE-SVC-013",
    "REQ-LIFE-SVC-014",
    "REQ-LIFE-SVC-015",
    "REQ-LIFE-SVC-017",
    "REQ-LIFE-SVC-031",
    "REQ-LIFE-SVC-033",
    "REQ-LIFE-SVC-034",
    "REQ-LIFE-SVC-035",
    "REQ-LIFE-SVC-044",
    "REQ-OPS-JOB-032",
    "REQ-OPS-JOB-043",
    "REQ-OPS-JOB-054"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-GOV-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002"
  ],
  "adr_ids": [
    "ADR-005"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-PROFILE-001",
    "DOC-PROFILE-002",
    "DOC-PROFILE-005",
    "DOC-PROFILE-006",
    "DOC-PROFILE-007",
    "DOC-PROFILE-008",
    "DOC-PROFILE-010",
    "DOC-DEV-006",
    "DOC-CONF-017",
    "DOC-CONST-002",
    "DOC-CONST-013",
    "DOC-SYS-017",
    "DOC-LIFE-006",
    "DOC-OPS-006",
    "DOC-CONF-016"
  ],
  "tags": [
    "adr",
    "containers",
    "podman",
    "rootless",
    "quadlet",
    "systemd",
    "oci",
    "linux",
    "sovereign-linux",
    "development",
    "profile-scoped",
    "kubernetes",
    "endpoints",
    "profiles",
    "orchestration",
    "developer-workstation",
    "operational-complexity",
    "resource-efficiency"
  ],
  "effective_at": "2026-08-03T19:29:00-04:00"
}
KOA:DOC-META:END -->

# ADR-005 — Rootless Endpoint Containers Without a Kubernetes Requirement

**Status:** `accepted`

## Problem

Using the same orchestrator everywhere appears simpler, but Kubernetes on endpoints adds control-plane, networking, storage, upgrade, and operational complexity that the endpoint does not need. Plain host services alone, however, lose useful isolation and declarative lifecycle management.

## Decision

Linux endpoints prefer rootless Podman for OCI workloads and Quadlet for declarative systemd integration. Kubernetes is not required on endpoints. Windows/WSL development may use Docker or Podman. Build farms and control-plane profiles may use a different conformant orchestrator when their profile declares it.

## Why this ADR exists

The non-obvious choice is to keep OCI compatibility while refusing a universal Kubernetes baseline. A future maintainer may otherwise add Kubernetes for uniformity and unintentionally increase minimum hardware, failure modes, and operator burden.

## Guardrail

Component contracts remain runtime-independent. Endpoint recipes must not assume cluster APIs. Privileged host work stays outside ordinary containers and passes through the narrow host-operation boundary.

## Reconsider when

Reconsider when the endpoint genuinely needs cluster scheduling or when a maintained orchestration layer has lower total complexity than the rootless Podman and systemd model on the supported hardware.

## Canonical system description

- `contracts/profiles/sovereign-linux-node.profile.json`
- `contracts/profiles/developer-linux-workstation.profile.json`
- `05-development/06-service-containers.md`
- `06-lifecycle/06-service-updates.md`

The canonical contracts and system documents define the current behavior. This ADR only preserves the reason for the non-obvious implementation choice.
