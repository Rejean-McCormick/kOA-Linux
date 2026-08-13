#!/usr/bin/env python3
"""Entry point for the ordinary restricted kOA appliance session."""

from session_runtime import main_for_mode


if __name__ == "__main__":
    raise SystemExit(main_for_mode("interactive_user"))
