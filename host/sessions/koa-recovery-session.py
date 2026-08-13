#!/usr/bin/env python3
"""Entry point for the separately authorized kOA recovery session."""

from session_runtime import main_for_mode


if __name__ == "__main__":
    raise SystemExit(main_for_mode("recovery"))
