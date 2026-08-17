"""Public client for profile-declared Node Agent resource-control operations."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

_ALLOWED_RESOURCE_COMMANDS = frozenset(
    {
        "apply_limits",
        "update_limits",
        "throttle",
        "suspend",
        "resume",
        "terminate",
        "release",
    }
)
_NODE_AGENT_RESULTS = frozenset(
    {
        "accepted",
        "completed",
        "rejected",
        "conflict",
        "timed_out",
        "failed",
        "recovery_required",
    }
)


class NodeAgentError(RuntimeError):
    """Base error for Node Agent boundary failures."""


class NodeAgentUnavailable(NodeAgentError):
    """Raised when the declared Node Agent transport is unavailable."""


class NodeAgentCommandRejected(NodeAgentError):
    """Raised when the Node Agent rejects or cannot complete a command."""


class NodeAgentProtocolError(NodeAgentError):
    """Raised when a response violates the public Node Agent contract."""


@runtime_checkable
class NodeAgentTransport(Protocol):
    """Public ``execute_node_operation`` transport boundary."""

    def execute_node_operation(self, request: Mapping[str, object]) -> Mapping[str, object]: ...


@dataclass(frozen=True, slots=True)
class NodeAgentResult:
    """Bounded result that never conflates acceptance with completion."""

    request_id: str
    status: str
    operation_ref: str | None
    receipt_ref: str | None
    current_state: Mapping[str, object] | None

    @property
    def terminal(self) -> bool:
        return self.status in {"completed", "rejected", "conflict", "timed_out", "failed", "recovery_required"}

    @property
    def completed(self) -> bool:
        return self.status == "completed"


class NodeAgentClient:
    """Translate RG-IF-007 records to a declared Node Agent operation.

    The Node Agent operation identifier is mandatory constructor input. This
    adapter therefore cannot invent or widen the broker's closed allowlist.
    """

    def __init__(
        self,
        transport: NodeAgentTransport,
        *,
        operation_id: str,
        caller_identity: str,
        profile_context_ref: str,
        timeout_seconds: int = 30,
    ) -> None:
        if not operation_id.strip():
            raise ValueError("a profile-declared Node Agent operation_id is required")
        if not caller_identity.strip() or not profile_context_ref.strip():
            raise ValueError("caller_identity and profile_context_ref are required")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        self._transport = transport
        self._operation_id = operation_id
        self._caller_identity = caller_identity
        self._profile_context_ref = profile_context_ref
        self._timeout_seconds = timeout_seconds

    def execute(
        self,
        command_record: Mapping[str, object],
        *,
        expected_current_state: Mapping[str, object],
        policy_decision_ref: str | None = None,
        receipt_required: bool = False,
    ) -> NodeAgentResult:
        """Execute one bounded resource-control command through the public API."""

        if not expected_current_state:
            raise ValueError("expected_current_state must identify the state being controlled")
        normalized = _validate_command_record(command_record)
        command_id = normalized["command_id"]
        target_execution_ref = normalized["target_execution_ref"]
        request: dict[str, object] = {
            "interface_id": "execute_node_operation",
            "version": "1.0.0",
            "operation": self._operation_id,
            "request_id": command_id,
            "caller_identity": self._caller_identity,
            "profile_context_ref": self._profile_context_ref,
            "artifact_or_target_refs": [target_execution_ref],
            "expected_current_state": dict(expected_current_state),
            "parameters": normalized,
            "deadline_or_timeout": self._timeout_seconds,
            "correlation_id": command_id,
            "idempotency_key": command_id,
        }
        if policy_decision_ref is not None:
            if not policy_decision_ref.strip():
                raise ValueError("policy_decision_ref cannot be blank")
            request["policy_decision_ref_when_required"] = policy_decision_ref

        try:
            response = self._transport.execute_node_operation(request)
        except Exception as exc:
            raise NodeAgentUnavailable("node_agent_transport_unavailable") from exc

        result = _parse_result(response, command_id)
        if result.status in {"rejected", "conflict", "timed_out", "failed", "recovery_required"}:
            raise NodeAgentCommandRejected(f"node agent result: {result.status}")
        if receipt_required and result.completed and result.receipt_ref is None:
            raise NodeAgentProtocolError("completed critical control lacks receipt_ref")
        return result

    def apply_resource_control(
        self,
        command_record: Mapping[str, object],
        *,
        expected_current_state: Mapping[str, object],
        policy_decision_ref: str | None = None,
        receipt_required: bool = False,
    ) -> NodeAgentResult:
        """Port-friendly name for one bounded resource-control operation."""

        return self.execute(
            command_record,
            expected_current_state=expected_current_state,
            policy_decision_ref=policy_decision_ref,
            receipt_required=receipt_required,
        )

    def apply_control(
        self,
        command_record: Mapping[str, object],
        *,
        expected_current_state: Mapping[str, object],
        policy_decision_ref: str | None = None,
        receipt_required: bool = False,
    ) -> NodeAgentResult:
        """Alias matching a typical Resource Governor node-agent port."""

        return self.execute(
            command_record,
            expected_current_state=expected_current_state,
            policy_decision_ref=policy_decision_ref,
            receipt_required=receipt_required,
        )


def _validate_command_record(record: Mapping[str, object]) -> dict[str, object]:
    required = (
        "command_id",
        "target_execution_ref",
        "command",
        "reason",
        "expected_result",
        "issued_at",
    )
    missing = [name for name in required if name not in record]
    if missing:
        raise ValueError(f"resource control command missing fields: {', '.join(missing)}")

    normalized = dict(record)
    for name in required:
        value = normalized[name]
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"resource control command field {name} must be a non-empty string")
    command = normalized["command"]
    if command not in _ALLOWED_RESOURCE_COMMANDS:
        raise ValueError(f"unsupported RG-IF-007 command: {command}")
    return normalized


def _parse_result(response: Mapping[str, object], request_id: str) -> NodeAgentResult:
    status = response.get("status")
    if not isinstance(status, str) or status not in _NODE_AGENT_RESULTS:
        raise NodeAgentProtocolError("node agent returned an invalid status")

    response_request_id = response.get("request_id", request_id)
    if response_request_id != request_id:
        raise NodeAgentProtocolError("node agent response request_id mismatch")

    operation_ref = response.get("operation_ref")
    receipt_ref = response.get("receipt_ref")
    current_state = response.get("current_state")
    if operation_ref is not None and (not isinstance(operation_ref, str) or not operation_ref.strip()):
        raise NodeAgentProtocolError("operation_ref must be a non-empty string")
    if receipt_ref is not None and (not isinstance(receipt_ref, str) or not receipt_ref.strip()):
        raise NodeAgentProtocolError("receipt_ref must be a non-empty string")
    if current_state is not None and not isinstance(current_state, Mapping):
        raise NodeAgentProtocolError("current_state must be an object")
    if status == "accepted" and operation_ref is None:
        raise NodeAgentProtocolError("accepted asynchronous operation lacks operation_ref")

    return NodeAgentResult(
        request_id=request_id,
        status=status,
        operation_ref=operation_ref,
        receipt_ref=receipt_ref,
        current_state=dict(current_state) if isinstance(current_state, Mapping) else None,
    )
