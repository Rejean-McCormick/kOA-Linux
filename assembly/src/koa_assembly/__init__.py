"""Contract-driven assembly primitives for kOA-Linux."""

from .contract_loader import ContractLoader, LoadOutcome, LoadPolicy
from .diagnostics import (
    AssemblyDiagnosticError,
    Diagnostic,
    DiagnosticBag,
    Severity,
)
from .model import (
    AssemblyInputSet,
    AssemblyRequest,
    AssemblyResult,
    CompositionStatus,
    ContractFormat,
    ContractIdentity,
    ContractReference,
    ContractSource,
    DocumentClass,
    LoadedContract,
    canonical_json_bytes,
    resolve_json_pointer,
)

__all__ = [
    "AssemblyDiagnosticError",
    "AssemblyInputSet",
    "AssemblyRequest",
    "AssemblyResult",
    "CompositionStatus",
    "ContractFormat",
    "ContractIdentity",
    "ContractLoader",
    "ContractReference",
    "ContractSource",
    "Diagnostic",
    "DiagnosticBag",
    "DocumentClass",
    "LoadedContract",
    "LoadOutcome",
    "LoadPolicy",
    "Severity",
    "canonical_json_bytes",
    "resolve_json_pointer",
]

__version__ = "0.1.0"
