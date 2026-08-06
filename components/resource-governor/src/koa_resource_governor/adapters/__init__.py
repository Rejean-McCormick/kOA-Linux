"""Infrastructure adapters for the Resource Governor component.

Only component-local adapters are exported. Cross-component actions use injected
public transports, and host observations are read-only and payload-blind.
"""

from .audit_client import AuditClient, AuditDeliveryError, AuditTransport
from .node_agent_client import (
    NodeAgentClient,
    NodeAgentCommandRejected,
    NodeAgentError,
    NodeAgentProtocolError,
    NodeAgentResult,
    NodeAgentTransport,
    NodeAgentUnavailable,
)
from .proc_usage_probe import ProcUsageProbe, ProcessObservationUnavailable, UsageObservationError
from .profile_file_provider import (
    ProfileFileError,
    ProfileFileInvalid,
    ProfileFileMissing,
    ProfileFileProvider,
)
from .system_clock import SystemClock
from .systemd_usage_probe import (
    SystemctlPropertyReader,
    SystemdObservationError,
    SystemdObservationUnavailable,
    SystemdPropertyReader,
    SystemdUsageProbe,
)

__all__ = [
    "AuditClient",
    "AuditDeliveryError",
    "AuditTransport",
    "NodeAgentClient",
    "NodeAgentCommandRejected",
    "NodeAgentError",
    "NodeAgentProtocolError",
    "NodeAgentResult",
    "NodeAgentTransport",
    "NodeAgentUnavailable",
    "ProcUsageProbe",
    "ProcessObservationUnavailable",
    "ProfileFileError",
    "ProfileFileInvalid",
    "ProfileFileMissing",
    "ProfileFileProvider",
    "SystemClock",
    "SystemctlPropertyReader",
    "SystemdObservationError",
    "SystemdObservationUnavailable",
    "SystemdPropertyReader",
    "SystemdUsageProbe",
    "UsageObservationError",
]
