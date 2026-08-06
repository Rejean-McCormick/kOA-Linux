"""Command-line entry point for bounded configuration and health checks."""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections.abc import Sequence

from .bootstrap import DependencySnapshot, bootstrap
from .config import AuditBrokerConfig, ConfigurationError
from .health import DependencyState


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="koa-audit-broker")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("check-config", help="validate and print non-sensitive configuration")
    health = subparsers.add_parser("health", help="print bounded health and readiness")
    health.add_argument(
        "--assume-local-dependencies-ready",
        action="store_true",
        help="development-only probe input; does not discover or grant authority",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "check-config":
            config = AuditBrokerConfig.from_environment(os.environ)
            print(json.dumps(config.as_public_dict(), sort_keys=True, separators=(",", ":")))
            return 0

        dependencies = DependencySnapshot.unavailable()
        if args.assume_local_dependencies_ready:
            dependencies = DependencySnapshot(
                identity_and_trust=DependencyState.AVAILABLE,
                governance_policy_runtime=DependencyState.AVAILABLE,
                record_store_available=True,
                retention_policies_resolvable=True,
                resource_envelope_available=True,
                chain_of_custody_available=True,
            )
        runtime = bootstrap(environment=os.environ, dependencies=dependencies)
        snapshot = runtime.health.snapshot()
        print(json.dumps(snapshot.as_dict(), sort_keys=True, separators=(",", ":")))
        return 0 if snapshot.readiness.ready else 2
    except ConfigurationError as exc:
        print(f"configuration_error: {exc}", file=sys.stderr)
        return 64


if __name__ == "__main__":
    raise SystemExit(main())
