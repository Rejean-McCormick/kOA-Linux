#!/usr/bin/env python3
"""Probe component health and one readiness class through public bindings."""

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

EXIT_READY = 0
EXIT_NOT_READY = 1


def _absolute_socket(value: str) -> str:
    path = Path(value)
    if not path.is_absolute():
        raise argparse.ArgumentTypeError("socket path must be absolute")
    return str(path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read health and readiness without mutating component state."
    )
    parser.add_argument("--socket", required=True, type=_absolute_socket)
    parser.add_argument("--sender", default="dev.health-probe")
    parser.add_argument("--interface-version", default="1.0.0")
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument(
        "--readiness-class",
        choices=tuple(item.value for item in ReadinessClass),
        default=ReadinessClass.LOCAL_READ.value,
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        client = UnixHttpClient(
            args.socket,
            args.sender,
            timeout_seconds=args.timeout,
            interface_version=args.interface_version,
        )
        health = client.health()
        readiness = client.readiness(ReadinessClass(args.readiness_class))
    except (InterfaceValidationError, ProtocolError, RemoteError, TransportError) as exc:
        print(
            json.dumps(
                {
                    "result": "blocked",
                    "error": type(exc).__name__,
                    "message": str(exc),
                },
                ensure_ascii=False,
                sort_keys=True,
                indent=2,
            ),
            file=sys.stderr,
        )
        return EXIT_NOT_READY

    ready = health.startup_complete and readiness.accepting_work
    print(
        json.dumps(
            {
                "result": "ready" if ready else "not_ready",
                "health": health.to_dict(),
                "readiness": readiness.to_dict(),
            },
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
        )
    )
    return EXIT_READY if ready else EXIT_NOT_READY


if __name__ == "__main__":
    raise SystemExit(main())
