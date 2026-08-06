"""Local diagnostic command for Identity and Trust."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Sequence

from . import COMPONENT_CONTRACT_VERSION, COMPONENT_ID, __version__
from .bootstrap import bootstrap
from .config import ConfigurationError, IdentityTrustConfig


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="koa-identity-and-trust",
        description="Inspect the Identity and Trust bootstrap state without authoritative mutation.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("describe", help="Print stable package and contract identity.")
    for name, help_text in (
        ("check-config", "Validate configuration and print its public view."),
        ("health", "Evaluate bounded local health."),
        ("readiness", "Evaluate bounded local readiness."),
    ):
        command = subparsers.add_parser(name, help=help_text)
        command.add_argument("--config", type=Path, help="Absolute TOML configuration path.")
        command.add_argument("--public", action="store_true", help="Emit the minimal public status view.")
    return parser


def _print(payload: object) -> None:
    print(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False))


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "describe":
            _print(
                {
                    "component_id": COMPONENT_ID,
                    "component_version": __version__,
                    "contract_version": COMPONENT_CONTRACT_VERSION,
                    "authority": "authentication_and_trust_evidence_only",
                    "authorization_owned": False,
                }
            )
            return 0

        config = IdentityTrustConfig.load(path=args.config)
        if args.command == "check-config":
            _print(config.public_dict())
            return 0

        result = bootstrap(config)
        view = "public" if args.public else "operational"
        status = result.status.to_dict(view=view)
        if args.command == "health":
            _print({"health": status["health"], "status": status})
            return 0 if status["health"] not in {"failed", "unavailable"} else 2
        if args.command == "readiness":
            _print({"readiness": status["readiness"], "status": status})
            return 0 if status["readiness"] == "healthy" else 3
        raise AssertionError("argparse admitted an unknown command")
    except (ConfigurationError, ValueError) as exc:
        _print({"error": "invalid_configuration_or_state", "message": str(exc)})
        return 64


if __name__ == "__main__":
    sys.exit(main())
