"""Diagnostic-only command line entry point for kOA Mediatheque."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from . import __version__
from .bootstrap import bootstrap
from .config import ConfigurationError, MediathequeConfig


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="koa-mediatheque")
    parser.add_argument("--config", type=Path, help="absolute path to a component TOML file")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("describe", help="print immutable component identity")
    sub.add_parser("check-config", help="parse and validate configuration without mutation")
    health = sub.add_parser("health", help="evaluate local health without creating paths")
    health.add_argument("--view", choices=("public", "operational"), default="operational")
    readiness = sub.add_parser("readiness", help="evaluate readiness without starting workers")
    readiness.add_argument("--view", choices=("public", "operational"), default="operational")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "describe":
        print(json.dumps({"component_id": "koa_mediatheque", "version": __version__}, sort_keys=True))
        return 0
    try:
        config = MediathequeConfig.from_sources(config_path=args.config)
    except ConfigurationError as exc:
        print(json.dumps({"error": "configuration_invalid", "message": str(exc)}, sort_keys=True))
        return 2
    if args.command == "check-config":
        print(json.dumps(config.public_dict(), sort_keys=True))
        return 0
    result = bootstrap(config)
    payload = result.status.to_dict(view=args.view)
    if args.command == "readiness":
        payload = {"component_id": payload["component_id"], "readiness": payload["readiness"], "blocked_capabilities": payload["blocked_capabilities"]}
    print(json.dumps(payload, sort_keys=True))
    return 0 if result.status.readiness.value == "ready" else 1


if __name__ == "__main__":
    raise SystemExit(main())
