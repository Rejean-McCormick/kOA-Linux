"""CLI for bounded Kristal Runtime configuration and health probes."""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections.abc import Sequence

from .bootstrap import DependencySnapshot, bootstrap
from .config import ConfigurationError, KristalRuntimeConfig


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="koa-kristal-runtime")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("check-config", help="validate and print non-sensitive configuration")
    health = subparsers.add_parser("health", help="print bounded health and readiness")
    health.add_argument(
        "--assume-local-prerequisites-ready",
        action="store_true",
        help="development-only probe input; does not grant trust, policy, resources, channel membership, or activation",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "check-config":
            config = KristalRuntimeConfig.from_environment(os.environ)
            print(json.dumps(config.as_public_dict(), separators=(",", ":"), sort_keys=True))
            return 0
        dependencies = DependencySnapshot.ready_for_local_probe() if args.assume_local_prerequisites_ready else DependencySnapshot.unavailable()
        runtime = bootstrap(environment=os.environ, dependencies=dependencies)
        snapshot = runtime.health.snapshot()
        print(json.dumps(snapshot.as_dict(), separators=(",", ":"), sort_keys=True))
        return 0 if snapshot.ready else 2
    except ConfigurationError as exc:
        print(f"configuration_error: {exc}", file=sys.stderr)
        return 64


if __name__ == "__main__":
    raise SystemExit(main())
