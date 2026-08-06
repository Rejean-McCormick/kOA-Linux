#!/usr/bin/env python3
"""Query common public component interfaces over HTTP on a Unix socket."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Sequence

from koa_interfaces import (
    InterfaceValidationError,
    ProtocolError,
    ReadinessClass,
    RemoteError,
    TransportError,
    UnixHttpClient,
)

EXIT_OK = 0
EXIT_BLOCKED = 1
EXIT_USAGE = 2


def _absolute_socket(value: str) -> str:
    path = Path(value)
    if not path.is_absolute():
        raise argparse.ArgumentTypeError("socket path must be absolute")
    return str(path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Use only the common public kOA component interfaces."
    )
    parser.add_argument("--socket", required=True, type=_absolute_socket)
    parser.add_argument("--sender", required=True)
    parser.add_argument("--interface-version", default="1.0.0")
    parser.add_argument("--timeout", type=float, default=5.0)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("health", help="Read the public /health interface")
    readiness = commands.add_parser(
        "readiness", help="Read the public /readiness interface"
    )
    readiness.add_argument(
        "--class",
        dest="readiness_class",
        choices=tuple(item.value for item in ReadinessClass),
    )
    job = commands.add_parser("job-status", help="Read one public job status")
    job.add_argument("job_id")
    return parser


def _emit(payload: object, *, stream: object = sys.stdout) -> None:
    print(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2),
        file=stream,
    )


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        client = UnixHttpClient(
            args.socket,
            args.sender,
            timeout_seconds=args.timeout,
            interface_version=args.interface_version,
        )
        if args.command == "health":
            payload = client.health().to_dict()
        elif args.command == "readiness":
            selected = (
                ReadinessClass(args.readiness_class)
                if args.readiness_class is not None
                else None
            )
            payload = client.readiness(selected).to_dict()
        elif args.command == "job-status":
            payload = client.job_status(args.job_id).to_dict()
        else:
            raise InterfaceValidationError(f"unsupported command: {args.command}")
    except (InterfaceValidationError, ProtocolError, RemoteError, TransportError) as exc:
        _emit(
            {"result": "blocked", "error": type(exc).__name__, "message": str(exc)},
            stream=sys.stderr,
        )
        return EXIT_BLOCKED
    _emit({"result": "pass", "response": payload})
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
