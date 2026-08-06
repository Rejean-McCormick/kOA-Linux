//! Privileged broker boundary for the kOA Node Agent.
//!
//! The catalog is closed, admission is fail-closed, and host mutation is delegated
//! only after validation to a fixed profile-scoped adapter.

pub mod catalog;
pub mod operations;
pub mod sandbox;

pub use catalog::{
    operation_spec, operations, validate_catalog, CatalogError, IdempotencyRule, OperationId,
    OperationSpec, ParameterPolicy, ReceiptPolicy,
};
pub use operations::{
    AdmissionError, BackendOutcome, BrokerRequest, BrokerResult, BrokerStatus, OperationBackend,
    PrivilegedBroker, ValidatedRequest,
};
pub use sandbox::{RequestBounds, SafePathRoot, SandboxError, SandboxPolicy};

/// Validate all broker-local invariants without performing a privileged effect.
pub fn self_check() -> Result<(), String> {
    validate_catalog().map_err(|error| error.to_string())?;
    let bounds = SandboxPolicy::default().bounds();
    if bounds.maximum_references == 0
        || bounds.maximum_parameters == 0
        || bounds.maximum_canonical_request_bytes == 0
    {
        return Err("sandbox bounds must be non-zero".to_owned());
    }
    Ok(())
}
