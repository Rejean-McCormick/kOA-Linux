"""Narrow host-control boundary used by Resource Governor."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, runtime_checkable


@runtime_checkable
class NodeAgent(Protocol):
    """Apply one bounded RG-IF-007 command through a public node interface."""

    def apply_resource_control(
        self,
        command_record: Mapping[str, object],
        *,
        expected_current_state: Mapping[str, object],
        policy_decision_ref: str | None = None,
        receipt_required: bool = False,
    ) -> object:
        """Return a typed or mapping result; never expose a generic shell."""
        raise RuntimeError("protocol method must be implemented by an adapter")
