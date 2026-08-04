<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-RECIPE-USER-002",
  "document_class": "recipe",
  "version": "1.0.0",
  "status": "active",
  "language": "en",
  "layer": "operations",
  "owner": "user-experience-architecture",
  "scope": [
    "profile:user_lightweight"
  ],
  "canonical_refs": [
    "contracts/profiles/user-lightweight.profile.json",
    "contracts/system.contract.json#/operating_modes",
    "contracts/system.contract.json#/resource_governance",
    "generated/component-catalog.json",
    "contracts/components/resource-governor.component.json",
    "contracts/components/identity-and-trust.component.json",
    "contracts/subsystems/ariane.subsystem.json",
    "contracts/subsystems/uckk.subsystem.json",
    "contracts/artifact-contracts/resource-envelope.schema.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-PROFILE-001",
    "DEC-HW-001",
    "DEC-CONTAINER-001",
    "DEC-GOV-001",
    "DEC-ARI-001",
    "DEC-UCKK-001",
    "DEC-AI-001",
    "DEC-SENT-001",
    "DEC-DATA-001",
    "DEC-LIFE-001"
  ],
  "requirement_ids": [
    "REQ-SYS-MODE-001",
    "REQ-SYS-MODE-002",
    "REQ-SYS-MODE-004",
    "REQ-SYS-MODE-007",
    "REQ-SYS-MODE-014",
    "REQ-SYS-MODE-015",
    "REQ-SYS-MODE-016",
    "REQ-SYS-MODE-017",
    "REQ-SYS-MODE-018",
    "REQ-SYS-MODE-019",
    "REQ-COMP-RG-001",
    "REQ-COMP-RG-002",
    "REQ-COMP-RG-004",
    "REQ-COMP-RG-005",
    "REQ-COMP-RG-006",
    "REQ-COMP-RG-008",
    "REQ-COMP-RG-010",
    "REQ-COMP-RG-011",
    "REQ-COMP-RG-012",
    "REQ-COMP-RG-015",
    "REQ-COMP-RG-016",
    "REQ-COMP-RG-019",
    "REQ-COMP-RG-020",
    "REQ-COMP-RG-022"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-SENT-001",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002"
  ],
  "adr_ids": [
    "ADR-005",
    "ADR-019"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-ADR-005",
    "DOC-ADR-019",
    "DOC-SYS-003",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-011",
    "DOC-SYS-012",
    "DOC-SYS-014",
    "DOC-SYS-017",
    "DOC-COMP-RG-001",
    "DOC-LIFE-000",
    "DOC-SEC-002",
    "DOC-CONF-000"
  ],
  "tags": [
    "recipe",
    "user-lightweight",
    "service-activation",
    "interactive-user",
    "ariane",
    "resource-governor",
    "readiness",
    "on-demand",
    "heavy-job",
    "external-optional",
    "shutdown",
    "recovery"
  ],
  "effective_at": "2026-08-03T19:52:00-04:00"
}
KOA:DOC-META:END -->

# User-Lightweight Service Activation

> **Recipe status:** active and non-normative. Canonical service membership, commands, identities, resource envelopes, interfaces, and lifecycle behavior remain owned by the referenced profile and component contracts.

This recipe activates a minimal local service set for the `user_lightweight` primary profile.

```text
start only the native services needed now
    → verify readiness
    → expose truthful status
    → admit heavy work explicitly
    → keep external capabilities optional
    → stop cleanly
```

The recipe does not require containers, Kubernetes, a build toolchain, external AI, external voice, SenTient, continuous external connectivity, or unrestricted administrator access.

Container technology can be used by a profile adapter, but the activation contract remains runtime-independent.

## Outcome

At completion:

- the Resource Governor is active before governed workloads;
- local identity and trust support is ready for protected actions;
- Ariane local navigation is available without external AI;
- optional external voice remains disabled unless activated explicitly;
- SenTient remains absent;
- no more than one heavy UCKK job runs concurrently;
- process start and service readiness remain distinct;
- status reports identify active, degraded, failed, and unavailable capabilities;
- shutdown is ordered and idempotent;
- native local use remains available when optional external services fail.

## Service classes

| Class | Activation | Failure effect |
| --- | --- | --- |
| `essential` | Activated for the interactive user session | The affected native capability is unavailable or degraded |
| `on_demand` | Started only for a requested foreground job | Only the requested job fails |
| `optional_external` | Activated explicitly with external-transfer approval | The external feature is unavailable; the native baseline continues |

Each adapter exposes separate `start`, `ready`, `status`, and `stop` actions. A heavy foreground adapter also exposes `run`.

## 1. Create the activation plan

Save as `.koa/user-lightweight-services.json`.

```json
{
  "recipe_type": "user_lightweight_service_activation",
  "version": "1.0.0",
  "status": "active",
  "profile_id": "user_lightweight",
  "operating_mode": "interactive_user",
  "containers_required": false,
  "kubernetes_required": false,
  "external_connectivity_required_for_native_baseline": false,
  "state_root": "~/.local/state/koa/user-lightweight",
  "resource_policy": {
    "interactive_responsiveness_protected": true,
    "max_concurrent_heavy_jobs": 1,
    "unbounded_retries_allowed": false,
    "unbounded_queues_allowed": false,
    "unbounded_timeouts_allowed": false
  },
  "activation_order": [
    "resource_governor",
    "identity_and_trust",
    "ariane_local_navigation"
  ],
  "services": [
    {
      "service_id": "resource_governor",
      "service_class": "essential",
      "activation": "startup",
      "adapter": ".koa/service-adapters/resource-governor",
      "dependencies": [],
      "ready_timeout_seconds": 30,
      "heavy": false,
      "external": false,
      "enabled_by_default": true,
      "failure_effect": "block_new_governed_workloads"
    },
    {
      "service_id": "identity_and_trust",
      "service_class": "essential",
      "activation": "startup",
      "adapter": ".koa/service-adapters/identity-and-trust",
      "dependencies": [
        "resource_governor"
      ],
      "ready_timeout_seconds": 30,
      "heavy": false,
      "external": false,
      "enabled_by_default": true,
      "failure_effect": "protected_actions_unavailable"
    },
    {
      "service_id": "ariane_local_navigation",
      "service_class": "essential",
      "activation": "startup",
      "adapter": ".koa/service-adapters/ariane-local-navigation",
      "dependencies": [
        "resource_governor",
        "identity_and_trust"
      ],
      "ready_timeout_seconds": 30,
      "heavy": false,
      "external": false,
      "enabled_by_default": true,
      "failure_effect": "interactive_session_degraded"
    },
    {
      "service_id": "uckk_local_worker",
      "service_class": "on_demand",
      "activation": "foreground_job",
      "adapter": ".koa/service-adapters/uckk-local-worker",
      "dependencies": [
        "resource_governor"
      ],
      "ready_timeout_seconds": 0,
      "heavy": true,
      "external": false,
      "enabled_by_default": false,
      "failure_effect": "requested_uckk_job_fails"
    },
    {
      "service_id": "ariane_external_voice",
      "service_class": "optional_external",
      "activation": "explicit",
      "adapter": ".koa/service-adapters/ariane-external-voice",
      "dependencies": [
        "resource_governor",
        "identity_and_trust",
        "ariane_local_navigation"
      ],
      "ready_timeout_seconds": 30,
      "heavy": false,
      "external": true,
      "enabled_by_default": false,
      "failure_effect": "voice_unavailable_local_navigation_continues"
    }
  ],
  "excluded_services": [
    "sentient"
  ],
  "shutdown_order": [
    "ariane_external_voice",
    "ariane_local_navigation",
    "identity_and_trust",
    "resource_governor"
  ],
  "validation": {
    "required_checks": [
      "plan_semantics",
      "adapter_presence",
      "startup_readiness",
      "essential_failure_scope",
      "heavy_concurrency",
      "optional_external_removal",
      "shutdown_idempotence",
      "native_baseline_without_network"
    ],
    "activation_requires": "pass"
  }
}
```

The plan includes three startup services, one local heavy job, one external optional service, and no SenTient service.

## 2. Create the service controller

Save as `scripts/user-lightweight-service.py`.

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import Any

SERVICE_CLASSES = {"essential", "on_demand", "optional_external"}
ACTIVATION_TYPES = {"startup", "foreground_job", "explicit"}

def load_plan(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"Activation plan not found: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid activation plan JSON: {exc}")
    validate_plan(data)
    return data

def service_map(plan: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {service["service_id"]: service for service in plan["services"]}

def validate_plan(plan: dict[str, Any]) -> None:
    required = {
        "recipe_type",
        "version",
        "status",
        "profile_id",
        "operating_mode",
        "containers_required",
        "kubernetes_required",
        "external_connectivity_required_for_native_baseline",
        "state_root",
        "resource_policy",
        "activation_order",
        "services",
        "excluded_services",
        "shutdown_order",
        "validation",
    }
    missing = sorted(required - set(plan))
    if missing:
        raise SystemExit(f"Missing plan keys: {', '.join(missing)}")

    if plan["recipe_type"] != "user_lightweight_service_activation":
        raise SystemExit("Unexpected recipe_type")
    if plan["status"] != "active":
        raise SystemExit("Activation plan must be active")
    if plan["profile_id"] != "user_lightweight":
        raise SystemExit("This recipe only supports user_lightweight")
    if plan["operating_mode"] != "interactive_user":
        raise SystemExit("Initial mode must be interactive_user")
    if plan["containers_required"]:
        raise SystemExit("Containers cannot be required")
    if plan["kubernetes_required"]:
        raise SystemExit("Kubernetes cannot be required")
    if plan["external_connectivity_required_for_native_baseline"]:
        raise SystemExit("The native baseline cannot require connectivity")

    policy = plan["resource_policy"]
    if policy.get("max_concurrent_heavy_jobs") != 1:
        raise SystemExit("user_lightweight permits one heavy job")
    for key in (
        "unbounded_retries_allowed",
        "unbounded_queues_allowed",
        "unbounded_timeouts_allowed",
    ):
        if policy.get(key) is not False:
            raise SystemExit(f"{key} must be false")

    services = plan["services"]
    if not isinstance(services, list) or not services:
        raise SystemExit("At least one service is required")

    ids: list[str] = []
    adapters: list[str] = []
    for service in services:
        service_id = service.get("service_id")
        adapter = service.get("adapter")
        if not isinstance(service_id, str) or not service_id:
            raise SystemExit("Every service needs service_id")
        if not isinstance(adapter, str) or not adapter:
            raise SystemExit(f"{service_id} needs an adapter")
        ids.append(service_id)
        adapters.append(adapter)

        if service.get("service_class") not in SERVICE_CLASSES:
            raise SystemExit(f"{service_id} has invalid service_class")
        if service.get("activation") not in ACTIVATION_TYPES:
            raise SystemExit(f"{service_id} has invalid activation")
        if not isinstance(service.get("dependencies"), list):
            raise SystemExit(f"{service_id} dependencies must be a list")
        if not isinstance(service.get("ready_timeout_seconds"), int):
            raise SystemExit(f"{service_id} needs an integer timeout")

        if service["service_class"] == "essential":
            if not service.get("enabled_by_default"):
                raise SystemExit(f"Essential service {service_id} is disabled")
            if service.get("external"):
                raise SystemExit(f"Essential service {service_id} is external")

        if service["service_class"] == "optional_external":
            if service.get("enabled_by_default"):
                raise SystemExit(
                    f"Optional external service {service_id} defaults on"
                )
            if not service.get("external"):
                raise SystemExit(
                    f"Optional external service {service_id} is not external"
                )

        if service.get("heavy"):
            if service["activation"] != "foreground_job":
                raise SystemExit(
                    f"Heavy service {service_id} must be foreground_job"
                )
            if service.get("enabled_by_default"):
                raise SystemExit(
                    f"Heavy service {service_id} cannot default on"
                )

    if len(ids) != len(set(ids)):
        raise SystemExit("Duplicate service_id values")
    if len(adapters) != len(set(adapters)):
        raise SystemExit("Duplicate adapter paths")

    known = set(ids)
    for service in services:
        unknown = sorted(set(service["dependencies"]) - known)
        if unknown:
            raise SystemExit(
                f"{service['service_id']} has unknown dependencies: "
                + ", ".join(unknown)
            )

    startup = [
        service["service_id"]
        for service in services
        if service["activation"] == "startup"
    ]
    if plan["activation_order"] != startup:
        raise SystemExit("activation_order does not match startup services")
    if set(plan["shutdown_order"]) - known:
        raise SystemExit("shutdown_order contains an unknown service")

    excluded = set(plan["excluded_services"])
    if "sentient" not in excluded:
        raise SystemExit("Sentient must be excluded")
    if excluded & known:
        raise SystemExit("Excluded services cannot be activated")

def resolve_adapter(root: Path, adapter_value: str) -> Path:
    adapter = Path(adapter_value)
    if not adapter.is_absolute():
        adapter = root / adapter
    return adapter.resolve()

def require_adapter(adapter: Path) -> None:
    if not adapter.is_file():
        raise SystemExit(f"Adapter not found: {adapter}")
    if not os.access(adapter, os.X_OK):
        raise SystemExit(f"Adapter is not executable: {adapter}")

def run_adapter(
    adapter: Path,
    action: str,
    *,
    capture: bool = False,
) -> subprocess.CompletedProcess[str]:
    require_adapter(adapter)
    return subprocess.run(
        [str(adapter), action],
        check=False,
        text=True,
        capture_output=capture,
    )

def state_root(plan: dict[str, Any]) -> Path:
    return Path(os.path.expanduser(plan["state_root"])).resolve()

def active_marker(plan: dict[str, Any], service_id: str) -> Path:
    return state_root(plan) / "active" / service_id

def mark_active(plan: dict[str, Any], service_id: str) -> None:
    marker = active_marker(plan, service_id)
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(
        json.dumps(
            {
                "service_id": service_id,
                "activated_at": int(time.time()),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

def clear_active(plan: dict[str, Any], service_id: str) -> None:
    active_marker(plan, service_id).unlink(missing_ok=True)

def is_marked_active(plan: dict[str, Any], service_id: str) -> bool:
    return active_marker(plan, service_id).is_file()

def wait_ready(adapter: Path, timeout_seconds: int) -> None:
    if timeout_seconds <= 0:
        return
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        result = run_adapter(adapter, "ready", capture=True)
        if result.returncode == 0:
            return
        time.sleep(0.5)
    raise SystemExit(
        f"Service did not become ready within {timeout_seconds}s: {adapter}"
    )

def verify_dependencies(
    plan: dict[str, Any],
    service: dict[str, Any],
) -> None:
    missing = [
        dependency
        for dependency in service["dependencies"]
        if not is_marked_active(plan, dependency)
    ]
    if missing:
        raise SystemExit(
            f"{service['service_id']} dependencies are not active: "
            + ", ".join(missing)
        )

def start_service(
    plan: dict[str, Any],
    root: Path,
    services: dict[str, dict[str, Any]],
    service_id: str,
) -> None:
    service = services[service_id]
    if is_marked_active(plan, service_id):
        return
    verify_dependencies(plan, service)
    adapter = resolve_adapter(root, service["adapter"])
    result = run_adapter(adapter, "start", capture=True)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise SystemExit(f"Start failed for {service_id}: {detail}")
    wait_ready(adapter, service["ready_timeout_seconds"])
    mark_active(plan, service_id)

def activate_startup(plan: dict[str, Any], root: Path) -> None:
    services = service_map(plan)
    for service_id in plan["activation_order"]:
        start_service(plan, root, services, service_id)

def activate_optional(
    plan: dict[str, Any],
    root: Path,
    service_id: str,
    allow_external: bool,
) -> None:
    services = service_map(plan)
    if service_id not in services:
        raise SystemExit(f"Unknown service: {service_id}")
    service = services[service_id]
    if service["service_class"] != "optional_external":
        raise SystemExit(f"{service_id} is not optional_external")
    if service["external"] and not allow_external:
        raise SystemExit("External activation requires --allow-external")
    start_service(plan, root, services, service_id)

def run_heavy(
    plan: dict[str, Any],
    root: Path,
    service_id: str,
) -> None:
    services = service_map(plan)
    if service_id not in services:
        raise SystemExit(f"Unknown service: {service_id}")
    service = services[service_id]
    if not service.get("heavy"):
        raise SystemExit(f"{service_id} is not a heavy job")
    verify_dependencies(plan, service)

    lock_path = state_root(plan) / "locks" / "heavy-job.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("w", encoding="utf-8") as lock_file:
        try:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise SystemExit(
                "Another user_lightweight heavy job is already running"
            )
        adapter = resolve_adapter(root, service["adapter"])
        result = run_adapter(adapter, "run")
        if result.returncode != 0:
            raise SystemExit(
                f"Heavy job failed for {service_id} "
                f"with exit code {result.returncode}"
            )

def stop_all(plan: dict[str, Any], root: Path) -> None:
    services = service_map(plan)
    failures: list[str] = []
    for service_id in plan["shutdown_order"]:
        service = services[service_id]
        adapter = resolve_adapter(root, service["adapter"])
        if adapter.is_file() and os.access(adapter, os.X_OK):
            result = run_adapter(adapter, "stop", capture=True)
            if result.returncode != 0:
                failures.append(service_id)
            else:
                clear_active(plan, service_id)
        else:
            clear_active(plan, service_id)
    if failures:
        raise SystemExit("Stop failed for: " + ", ".join(failures))

def report_status(plan: dict[str, Any], root: Path) -> None:
    report: list[dict[str, Any]] = []
    for service in plan["services"]:
        service_id = service["service_id"]
        adapter = resolve_adapter(root, service["adapter"])
        adapter_present = adapter.is_file() and os.access(adapter, os.X_OK)
        status_result = None
        if adapter_present:
            status_result = run_adapter(adapter, "status", capture=True)
        report.append(
            {
                "service_id": service_id,
                "service_class": service["service_class"],
                "marked_active": is_marked_active(plan, service_id),
                "adapter_present": adapter_present,
                "adapter_status": (
                    status_result.returncode
                    if status_result is not None
                    else None
                ),
                "detail": (
                    status_result.stdout.strip()
                    or status_result.stderr.strip()
                    if status_result is not None
                    else ""
                ),
            }
        )
    print(json.dumps(report, indent=2))

def check_adapters(plan: dict[str, Any], root: Path) -> None:
    missing: list[str] = []
    for service in plan["services"]:
        adapter = resolve_adapter(root, service["adapter"])
        if not adapter.is_file() or not os.access(adapter, os.X_OK):
            missing.append(f"{service['service_id']}={adapter}")
    if missing:
        raise SystemExit(
            "Missing or non-executable adapters:\n" + "\n".join(missing)
        )

def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    result.add_argument(
        "--plan",
        type=Path,
        default=Path(".koa/user-lightweight-services.json"),
    )
    result.add_argument("--root", type=Path, default=Path.cwd())
    commands = result.add_subparsers(dest="command", required=True)
    commands.add_parser("validate")
    commands.add_parser("check-adapters")
    commands.add_parser("activate")
    commands.add_parser("status")
    commands.add_parser("stop")

    optional = commands.add_parser("activate-optional")
    optional.add_argument("service_id")
    optional.add_argument("--allow-external", action="store_true")

    heavy = commands.add_parser("run-heavy")
    heavy.add_argument("service_id")
    return result

def main() -> int:
    args = parser().parse_args()
    plan = load_plan(args.plan.resolve())
    root = args.root.resolve()

    if args.command == "validate":
        print("user_lightweight activation plan passed semantic validation")
    elif args.command == "check-adapters":
        check_adapters(plan, root)
        print("all service adapters are present and executable")
    elif args.command == "activate":
        check_adapters(plan, root)
        activate_startup(plan, root)
        report_status(plan, root)
    elif args.command == "activate-optional":
        check_adapters(plan, root)
        activate_optional(
            plan,
            root,
            args.service_id,
            args.allow_external,
        )
        report_status(plan, root)
    elif args.command == "run-heavy":
        check_adapters(plan, root)
        run_heavy(plan, root, args.service_id)
    elif args.command == "status":
        report_status(plan, root)
    elif args.command == "stop":
        stop_all(plan, root)
        report_status(plan, root)
    return 0

if __name__ == "__main__":
    sys.exit(main())

```

Then run:

```bash
chmod +x scripts/user-lightweight-service.py
```

The controller validates the plan, verifies adapters, activates startup services, waits for readiness, records operational active markers, limits heavy jobs, requires explicit external activation, stops services in order, and reports status.

An active marker is not the authoritative readiness source. The component adapter remains authoritative for the actual lifecycle state.

## 3. Implement component-owned adapters

Create executable adapters:

```text
.koa/service-adapters/resource-governor
.koa/service-adapters/identity-and-trust
.koa/service-adapters/ariane-local-navigation
.koa/service-adapters/uckk-local-worker
.koa/service-adapters/ariane-external-voice
```

Use this interface template:

```bash
#!/usr/bin/env bash
set -euo pipefail

ACTION="${1:-}"

case "$ACTION" in
  start)
    # Connect this action to the canonical component launcher.
    exit 64
    ;;
  ready)
    # Exit zero only when the declared capability is ready.
    exit 64
    ;;
  status)
    printf '{"status":"adapter_not_configured"}\n'
    exit 64
    ;;
  stop)
    # Stop only this component instance. Keep this action idempotent.
    exit 64
    ;;
  run)
    # Foreground action used only by an on-demand heavy-job adapter.
    exit 64
    ;;
  *)
    printf 'Usage: %s {start|ready|status|stop|run}\n' "$0" >&2
    exit 64
    ;;
esac

```

The template intentionally exits with code `64` until connected to the component's canonical launcher.

| Action | Meaning |
| --- | --- |
| `start` | Request activation and return after the request is accepted |
| `ready` | Return zero only when the declared capability is ready |
| `status` | Return state without changing it |
| `stop` | Stop only this component instance; repeated calls remain safe |
| `run` | Run one foreground on-demand job and return when it finishes |

Do not implement an adapter by starting every host service, deleting unscoped runtime objects, writing to another component's data, reporting readiness early, silently activating an external integration, or treating resource admission as authorization.

## 4. Validate the plan

Run:

```bash
python3 scripts/user-lightweight-service.py validate
python3 scripts/user-lightweight-service.py check-adapters
```

The validator rejects required containers, required Kubernetes, required external connectivity, more than one heavy job, unbounded queues or timeouts, external essential services, enabled optional external services, missing dependencies, duplicate identities, and SenTient activation.

## 5. Activate the interactive user baseline

Save as `scripts/activate-user-lightweight.sh`.

```bash
#!/usr/bin/env bash
set -euo pipefail

REPOSITORY_ROOT="${REPOSITORY_ROOT:-$(pwd)}"
PLAN="${PLAN:-$REPOSITORY_ROOT/.koa/user-lightweight-services.json}"
CONTROLLER="${CONTROLLER:-$REPOSITORY_ROOT/scripts/user-lightweight-service.py}"

python3 "$CONTROLLER" --root "$REPOSITORY_ROOT" --plan "$PLAN" validate
python3 "$CONTROLLER" --root "$REPOSITORY_ROOT" --plan "$PLAN" check-adapters
python3 "$CONTROLLER" --root "$REPOSITORY_ROOT" --plan "$PLAN" activate

```

Run:

```bash
chmod +x scripts/activate-user-lightweight.sh
scripts/activate-user-lightweight.sh
```

Activation order:

```text
resource_governor
    → identity_and_trust
    → ariane_local_navigation
```

The controller waits for readiness after each accepted start. A failed start or readiness timeout is not reported as ready.

## 6. Check status

Run:

```bash
python3 scripts/user-lightweight-service.py status
```

Interpretation remains explicit:

```text
adapter present
does not mean active

start accepted
does not mean ready

ready
does not mean every optional capability is active

process success
does not mean an authoritative component commit
```

Ariane should expose equivalent truthful user-facing status.

## 7. Run one heavy UCKK job

Save as `scripts/run-user-lightweight-heavy-job.sh`.

```bash
#!/usr/bin/env bash
set -euo pipefail

REPOSITORY_ROOT="${REPOSITORY_ROOT:-$(pwd)}"
PLAN="${PLAN:-$REPOSITORY_ROOT/.koa/user-lightweight-services.json}"
CONTROLLER="${CONTROLLER:-$REPOSITORY_ROOT/scripts/user-lightweight-service.py}"
SERVICE_ID="${1:-uckk_local_worker}"

python3 "$CONTROLLER" \
  --root "$REPOSITORY_ROOT" \
  --plan "$PLAN" \
  run-heavy "$SERVICE_ID"

```

Run:

```bash
chmod +x scripts/run-user-lightweight-heavy-job.sh
scripts/run-user-lightweight-heavy-job.sh uckk_local_worker
```

The controller acquires one local heavy-job lock before calling `run`.

A second concurrent request fails without disabling the baseline.

The lock enforces concurrency. It does not authorize the UCKK operation. The component still validates the request, authority, resource decision, cancellation, result, and required receipts.

## 8. Activate optional external voice

Run only after local navigation is active:

```bash
python3 scripts/user-lightweight-service.py   activate-optional   ariane_external_voice   --allow-external
```

Before activation, identify destination, transferred data classes, purpose, capability, validity, and failure behavior.

When external voice is unavailable, local keyboard, pointer, touch, menus, deterministic commands, accessibility controls, and shortcuts continue. No silent substitute activates.

## 9. Native baseline without network access

Test startup services with external connectivity disabled or restricted.

Verify that:

- Resource Governor enforces local envelopes;
- identity and trust use valid local state;
- Ariane local navigation becomes ready;
- disconnected status is truthful;
- external voice remains inactive;
- deterministic local UCKK work remains available subject to resources;
- no external AI is required;
- optional integration failure does not disable the baseline.

Connected testing does not prove disconnected behavior.

## 10. Resource controls

The exact `user_lightweight` envelope is profile-owned.

This recipe assumes protected interactive responsiveness, optional background services that can stop, at most one heavy UCKK job, and bounded queues, retries, and timeouts.

Resource Governor can admit, queue, throttle, pause, reject, expire, or cancel a workload.

A resource decision does not create data access, governance authorization, publication authority, component permission, or machine privilege.

## 11. Optional container adapter

Containers are optional for `user_lightweight`.

An adapter can map to a native process, user service, rootless container, or another profile-approved service manager.

Do not require Podman, Docker, Quadlet, systemd, or Kubernetes merely because one implementation uses it.

Runtime-specific names, sockets, networks, volumes, and credentials remain inside the adapter or profile-owned configuration.

## 12. Stop services cleanly

Save as `scripts/stop-user-lightweight.sh`.

```bash
#!/usr/bin/env bash
set -euo pipefail

REPOSITORY_ROOT="${REPOSITORY_ROOT:-$(pwd)}"
PLAN="${PLAN:-$REPOSITORY_ROOT/.koa/user-lightweight-services.json}"
CONTROLLER="${CONTROLLER:-$REPOSITORY_ROOT/scripts/user-lightweight-service.py}"

python3 "$CONTROLLER" --root "$REPOSITORY_ROOT" --plan "$PLAN" stop

```

Run:

```bash
chmod +x scripts/stop-user-lightweight.sh
scripts/stop-user-lightweight.sh
```

Shutdown order:

```text
ariane_external_voice
    → ariane_local_navigation
    → identity_and_trust
    → resource_governor
```

Before final shutdown, components handle pending work, cancellation, local receipts, state flush, temporary resources, connections, and authoritative commit or non-commit truth.

A stop failure remains visible and does not become a false clean-shutdown result.

## 13. Failure handling

| Failure | Recipe response |
| --- | --- |
| Resource Governor unavailable | Block new governed workloads and report capacity authority unavailable |
| Identity and Trust unavailable | Keep protected actions unavailable |
| Ariane local navigation unavailable | Report the interactive session degraded |
| Heavy UCKK job rejected | Preserve the baseline and report the requested job failure |
| External voice unavailable | Continue local Ariane navigation |
| Adapter missing | Block activation of the affected service |
| Readiness timeout | Do not create an active marker |
| Shutdown failure | Preserve visible failure state and continue bounded cleanup |
| External network unavailable | Keep native local services and report the optional capability unavailable |
| Critical receipt path unavailable | Block the critical action according to its component contract |

Failure remains scoped to the affected capability.

## 14. Activation and release boundary

This recipe activates already installed and verified service artifacts.

It does not build services, compile language artifacts, publish artifacts, select a Release Set, migrate authoritative data implicitly, or activate a release merely by starting a process.

Release installation remains a lifecycle operation with artifact verification, compatibility, authority, explicit deployment commit, rollback, forward repair, recovery, and receipts.

## 15. Completion checklist

- [ ] the activation plan passes semantic validation;
- [ ] all component-owned adapters exist and are executable;
- [ ] Resource Governor is ready before governed workloads;
- [ ] Identity and Trust is ready before protected actions;
- [ ] Ariane local navigation is ready without external AI;
- [ ] external voice is disabled by default;
- [ ] SenTient is absent;
- [ ] no native service requires external connectivity;
- [ ] no native service requires containers or Kubernetes;
- [ ] at most one heavy UCKK job runs;
- [ ] status distinguishes start, readiness, failure, and optional absence;
- [ ] optional external failure does not disable local navigation;
- [ ] shutdown is ordered and idempotent;
- [ ] failures remain capability-scoped;
- [ ] service startup is not reported as release activation.

## Conformance mapping

| Recipe element | Canonical intent |
| --- | --- |
| Minimal interactive baseline | `REQ-SYS-MODE-004` |
| Bounded unattended behavior | `REQ-SYS-MODE-007` |
| Truthful status | `REQ-SYS-MODE-015` |
| External AI optional | `REQ-SYS-MODE-016`, `LOCK-AI-001`, `LOCK-AI-002` |
| Local Ariane navigation | `REQ-SYS-MODE-017`, `LOCK-ARI-001`, `LOCK-ARI-002` |
| SenTient absent | `REQ-SYS-MODE-018`, `LOCK-SENT-001` |
| One heavy UCKK job | `REQ-COMP-RG-010` |
| Optional heavy services removable | `REQ-COMP-RG-011` |
| Bounded resource use | `REQ-COMP-RG-001`, `REQ-COMP-RG-005`, `REQ-COMP-RG-012` |
| Separate resource and policy authority | `DEC-GOV-001`, `LOCK-GOV-001`, `ADR-019` |
| Containers optional | `DEC-CONTAINER-001`, `ADR-005` |
| Runtime-independent activation | `LOCK-IMPL-001`, `LOCK-IMPL-002` |
| Component-owned state | `LOCK-DATA-001` |
| Startup is not release commit | `LOCK-LIFE-001`, `LOCK-LIFE-002` |
