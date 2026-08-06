"""Bounded Publication Gateway configuration and health CLI."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from collections.abc import Sequence

from .bootstrap import RuntimeObservation, bootstrap
from .config import ConfigurationError, PublicationGatewayConfig
from .health import CheckState


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="koa-publication-gateway")
    parser.add_argument(
        "--config",
        type=Path,
        help="optional TOML configuration; environment loading is used when omitted",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("check-config", help="validate non-sensitive configuration")
    health = subparsers.add_parser("health", help="print health and publication readiness")
    health.add_argument(
        "--assume-local-paths-ready",
        action="store_true",
        help="development observation only; does not bind dependencies or adapters",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        config = (
            PublicationGatewayConfig.from_toml(args.config)
            if args.config is not None
            else PublicationGatewayConfig.from_environment(os.environ)
        )
        if args.command == "check-config":
            print(json.dumps(config.as_public_dict(), sort_keys=True, separators=(",", ":")))
            return 0
        observation = RuntimeObservation.unknown()
        if args.assume_local_paths_ready:
            observation = RuntimeObservation(
                configuration_valid=CheckState.PASS,
                process_responsive=CheckState.PASS,
                state_directory_accessible=CheckState.PASS,
                runtime_directory_accessible=CheckState.PASS,
                receipt_directory_accessible=CheckState.PASS,
                staging_directory_accessible=CheckState.PASS,
                schema_versions_supported=CheckState.PASS,
                trusted_time_ready=CheckState.UNKNOWN,
            )
        result = bootstrap(config=config, observation=observation)
        print(json.dumps(result.as_dict(), sort_keys=True, separators=(",", ":")))
        return 0 if result.status.healthy else 1
    except (ConfigurationError, OSError, ValueError) as exc:
        print(
            json.dumps(
                {
                    "component_id": "publication_gateway",
                    "error": "configuration_invalid",
                    "message": str(exc),
                },
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
