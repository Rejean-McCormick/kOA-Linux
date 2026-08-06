#!/usr/bin/env python3
"""Invoke one declared public integration operation with an injected transport."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Mapping, Sequence

from koa_interfaces import (
    Correlation,
    InterfaceValidationError,
    ProtocolError,
    RemoteError,
    TransportError,
    UnixHttpClient,
)

EXIT_OK = 0
EXIT_BLOCKED = 1


def _absolute_socket(value: str) -> str:
    path = Path(value)
    if not path.is_absolute():
        raise argparse.ArgumentTypeError("socket path must be absolute")
    return str(path)


def _operation_path(value: str) -> str:
    if not value.startswith("/") or value.startswith("//") or ".." in value.split("/"):
        raise argparse.ArgumentTypeError(
            "operation path must be an absolute origin-form path without traversal"
        )
    return value


def _read_body(path: str) -> Mapping[str, Any]:
    if path == "-":
        text = sys.stdin.read()
    else:
        text = Path(path).read_text(encoding="utf-8")
    value = json.loads(text)
    if not isinstance(value, dict):
        raise InterfaceValidationError("integration request body must be a JSON object")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Send a request only to an operation path declared by an integration's "
            "public module interface. No operation is inferred or simulated."
        )
    )
    parser.add_argument("--socket", required=True, type=_absolute_socket)
    parser.add_argument("--sender", required=True)
    parser.add_argument("--operation-path", required=True, type=_operation_path)
    parser.add_argument("--body", required=True, help="JSON object file, or '-' for stdin")
    parser.add_argument("--correlation-id", required=True)
    parser.add_argument("--request-id", required=True)
    parser.add_argument("--idempotency-key", required=True)
    parser.add_argument("--interface-version", default="1.0.0")
    parser.add_argument("--timeout", type=float, default=10.0)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        body = _read_body(args.body)
        client = UnixHttpClient(
            args.socket,
            args.sender,
            timeout_seconds=args.timeout,
            interface_version=args.interface_version,
        )
        response = client.request(
            "POST",
            args.operation_path,
            body=body,
            correlation=Correlation(
                correlation_id=args.correlation_id,
                request_id=args.request_id,
            ),
            idempotency_key=args.idempotency_key,
            expected_status=(200, 202),
        )
        if response is None:
            raise ProtocolError("integration operation returned an empty success response")
    except (
        OSError,
        json.JSONDecodeError,
        InterfaceValidationError,
        ProtocolError,
        RemoteError,
        TransportError,
    ) as exc:
        print(
            json.dumps(
                {"result": "blocked", "error": type(exc).__name__, "message": str(exc)},
                ensure_ascii=False,
                sort_keys=True,
                indent=2,
            ),
            file=sys.stderr,
        )
        return EXIT_BLOCKED

    print(
        json.dumps(
            {"result": "accepted", "response": dict(response)},
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
        )
    )
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
