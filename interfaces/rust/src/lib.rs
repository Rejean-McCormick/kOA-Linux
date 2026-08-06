//! Stable Rust bindings for the common kOA implementation interfaces.
//!
//! These types represent transport envelopes and shared operational records.
//! They do not confer business authority and do not replace component-owned
//! domain contracts.

#![forbid(unsafe_code)]

use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::collections::BTreeMap;

pub mod client;
pub mod error;
pub mod health;
pub mod receipt;

pub use client::{InterfaceClient, Transport};
pub use error::{ClientError, ErrorCategory, ErrorEnvelope, TransportError};
pub use health::{
    CapabilityReadiness, DependencyHealth, DependencyRequirement, Freshness,
    HealthStatus, OperationalState, ReadinessClass, ReadinessStatus,
};
pub use receipt::{
    CommitState, DecisionState, DisclosureClass, ReceiptClass, ReceiptEnvelope,
    ReceiptOutcome,
};

/// Canonical repository-relative schema identifiers consumed by this crate.
pub mod schema {
    pub const EVENT_ENVELOPE: &str = "interfaces/transport/event-envelope.schema.json";
    pub const ERROR_ENVELOPE: &str = "interfaces/transport/error-envelope.schema.json";
    pub const IDEMPOTENCY: &str = "interfaces/transport/idempotency.schema.json";
    pub const VERSION_NEGOTIATION: &str =
        "interfaces/transport/version-negotiation.schema.json";
    pub const HEALTH_STATUS: &str = "interfaces/health/health-status.schema.json";
    pub const READINESS: &str = "interfaces/health/readiness.schema.json";
    pub const RECEIPT_ENVELOPE: &str = "interfaces/receipts/receipt-envelope.schema.json";
    pub const CORRELATION: &str = "interfaces/receipts/correlation.schema.json";
    pub const JOB_REQUEST: &str = "interfaces/jobs/job-request.schema.json";
    pub const JOB_STATUS: &str = "interfaces/jobs/job-status.schema.json";
    pub const IDENTITY_CONTEXT: &str = "interfaces/identity/identity-context.schema.json";
    pub const CAPABILITY_SNAPSHOT: &str =
        "interfaces/capabilities/capability-snapshot.schema.json";
}


/// A versioned interaction class crossing an ownership boundary.
#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum InteractionClass {
    Command,
    Query,
    DomainEvent,
    AsynchronousJob,
    ArtifactTransfer,
    ControlledReadModel,
    PolicyDecisionRequest,
    ResourceRequest,
    GatewayTransfer,
    ExternalIntegrationCall,
}

/// Correlation and causal identity shared by linked component-local records.
#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct CorrelationContext {
    pub schema: String,
    pub schema_version: String,
    pub request_id: String,
    pub correlation_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub causation_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub trace_id: Option<String>,
}

impl CorrelationContext {
    #[must_use]
    pub fn new(
        schema_version: impl Into<String>,
        request_id: impl Into<String>,
        correlation_id: impl Into<String>,
    ) -> Self {
        Self {
            schema: schema::CORRELATION.to_owned(),
            schema_version: schema_version.into(),
            request_id: request_id.into(),
            correlation_id: correlation_id.into(),
            causation_id: None,
            trace_id: None,
        }
    }

    pub fn validate(&self) -> Result<(), BindingValidationError> {
        if self.schema != schema::CORRELATION {
            return Err(BindingValidationError::new(
                "schema",
                "must identify the common correlation schema",
            ));
        }
        require_non_empty("schema_version", &self.schema_version)?;
        require_non_empty("request_id", &self.request_id)?;
        require_non_empty("correlation_id", &self.correlation_id)?;
        optional_non_empty("causation_id", self.causation_id.as_deref())?;
        optional_non_empty("trace_id", self.trace_id.as_deref())
    }
}

/// Identity and authority references required to evaluate a request.
#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct IdentityContext {
    pub schema: String,
    pub schema_version: String,
    pub actor_ref: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub subject_ref: Option<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub authority_refs: Vec<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub delegation_refs: Vec<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub consent_refs: Vec<String>,
    #[serde(default, skip_serializing_if = "BTreeMap::is_empty")]
    pub attributes: BTreeMap<String, String>,
}

impl IdentityContext {
    #[must_use]
    pub fn new(
        schema_version: impl Into<String>,
        actor_ref: impl Into<String>,
    ) -> Self {
        Self {
            schema: schema::IDENTITY_CONTEXT.to_owned(),
            schema_version: schema_version.into(),
            actor_ref: actor_ref.into(),
            subject_ref: None,
            authority_refs: Vec::new(),
            delegation_refs: Vec::new(),
            consent_refs: Vec::new(),
            attributes: BTreeMap::new(),
        }
    }

    pub fn validate(&self) -> Result<(), BindingValidationError> {
        if self.schema != schema::IDENTITY_CONTEXT {
            return Err(BindingValidationError::new(
                "schema",
                "must identify the common identity-context schema",
            ));
        }
        require_non_empty("schema_version", &self.schema_version)?;
        require_non_empty("actor_ref", &self.actor_ref)?;
        optional_non_empty("subject_ref", self.subject_ref.as_deref())?;
        validate_non_empty_values("authority_refs", &self.authority_refs)?;
        validate_non_empty_values("delegation_refs", &self.delegation_refs)?;
        validate_non_empty_values("consent_refs", &self.consent_refs)
    }
}

/// Stable retry identity bound to one canonical request body.
#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct IdempotencyContext {
    pub schema: String,
    pub schema_version: String,
    pub idempotency_key: String,
    pub request_digest: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub namespace: Option<String>,
}

impl IdempotencyContext {
    pub fn validate(&self) -> Result<(), BindingValidationError> {
        if self.schema != schema::IDEMPOTENCY {
            return Err(BindingValidationError::new(
                "schema",
                "must identify the common idempotency schema",
            ));
        }
        require_non_empty("schema_version", &self.schema_version)?;
        require_non_empty("idempotency_key", &self.idempotency_key)?;
        require_non_empty("request_digest", &self.request_digest)?;
        optional_non_empty("namespace", self.namespace.as_deref())
    }
}

/// Interface-version offer and optional selected version.
#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct VersionNegotiation {
    pub schema: String,
    pub schema_version: String,
    pub interface_id: String,
    pub supported_versions: Vec<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub selected_version: Option<String>,
}

impl VersionNegotiation {
    pub fn validate(&self) -> Result<(), BindingValidationError> {
        if self.schema != schema::VERSION_NEGOTIATION {
            return Err(BindingValidationError::new(
                "schema",
                "must identify the common version-negotiation schema",
            ));
        }
        require_non_empty("schema_version", &self.schema_version)?;
        require_non_empty("interface_id", &self.interface_id)?;
        if self.supported_versions.is_empty() {
            return Err(BindingValidationError::new(
                "supported_versions",
                "must contain at least one version",
            ));
        }
        validate_non_empty_values("supported_versions", &self.supported_versions)?;
        if let Some(selected) = &self.selected_version {
            require_non_empty("selected_version", selected)?;
            if !self.supported_versions.iter().any(|version| version == selected) {
                return Err(BindingValidationError::new(
                    "selected_version",
                    "must be present in supported_versions",
                ));
            }
        }
        Ok(())
    }
}

/// Versioned common message envelope. The payload remains owned by its
/// component or artifact contract.
#[derive(Clone, Debug, Deserialize, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct EventEnvelope<T = Value> {
    pub schema: String,
    pub schema_version: String,
    pub interface_id: String,
    pub interface_version: String,
    pub message_id: String,
    pub interaction_class: InteractionClass,
    pub sender_component_id: String,
    pub receiver_component_id: String,
    pub operation: String,
    pub correlation: CorrelationContext,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub identity: Option<IdentityContext>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub idempotency: Option<IdempotencyContext>,
    pub payload_schema: String,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub expires_at: Option<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub authority_refs: Vec<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub evidence_refs: Vec<String>,
    pub payload: T,
}

impl<T> EventEnvelope<T> {
    pub fn validate_metadata(&self) -> Result<(), BindingValidationError> {
        if self.schema != schema::EVENT_ENVELOPE {
            return Err(BindingValidationError::new(
                "schema",
                "must identify the common event-envelope schema",
            ));
        }
        require_non_empty("schema_version", &self.schema_version)?;
        require_non_empty("interface_id", &self.interface_id)?;
        require_non_empty("interface_version", &self.interface_version)?;
        require_non_empty("message_id", &self.message_id)?;
        require_non_empty("sender_component_id", &self.sender_component_id)?;
        require_non_empty("receiver_component_id", &self.receiver_component_id)?;
        require_non_empty("operation", &self.operation)?;
        require_non_empty("payload_schema", &self.payload_schema)?;
        require_non_empty("created_at", &self.created_at)?;
        optional_non_empty("expires_at", self.expires_at.as_deref())?;
        validate_non_empty_values("authority_refs", &self.authority_refs)?;
        validate_non_empty_values("evidence_refs", &self.evidence_refs)?;
        self.correlation.validate()?;
        if let Some(identity) = &self.identity {
            identity.validate()?;
        }
        if let Some(idempotency) = &self.idempotency {
            idempotency.validate()?;
        }
        Ok(())
    }
}

/// Availability is independent from execution and authoritative outcome.
#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum CapabilityAvailability {
    Available,
    Degraded,
    DeferredOnly,
    Blocked,
    Unavailable,
}

/// Shared execution-state vocabulary.
#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum ExecutionState {
    NotStarted,
    Accepted,
    Queued,
    Running,
    AwaitingDependency,
    AwaitingAuthority,
    Completed,
    Cancelled,
    Failed,
    Conflicted,
    Expired,
}

/// Shared authoritative-outcome vocabulary.
#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum AuthoritativeOutcome {
    NoEffect,
    CandidateCreated,
    RequestRecorded,
    ChangeCommitted,
    PolicyDecisionRecorded,
    EvidenceRecorded,
    ExternalEffectConfirmed,
    RolledBack,
}

/// One capability state in a point-in-time component snapshot.
#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct CapabilitySnapshotEntry {
    pub capability_id: String,
    pub owner_component_ref: String,
    pub availability: CapabilityAvailability,
    pub execution_state: ExecutionState,
    pub authoritative_outcome: AuthoritativeOutcome,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub reason_codes: Vec<String>,
}

impl CapabilitySnapshotEntry {
    pub fn validate(&self) -> Result<(), BindingValidationError> {
        require_non_empty("capability_id", &self.capability_id)?;
        require_non_empty("owner_component_ref", &self.owner_component_ref)?;
        validate_non_empty_values("reason_codes", &self.reason_codes)
    }
}

/// Point-in-time capability state without transferring component authority.
#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct CapabilitySnapshot {
    pub schema: String,
    pub schema_version: String,
    pub snapshot_id: String,
    pub component_id: String,
    pub observed_at: String,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub profile_refs: Vec<String>,
    pub capabilities: Vec<CapabilitySnapshotEntry>,
}

impl CapabilitySnapshot {
    pub fn validate(&self) -> Result<(), BindingValidationError> {
        if self.schema != schema::CAPABILITY_SNAPSHOT {
            return Err(BindingValidationError::new(
                "schema",
                "must identify the common capability-snapshot schema",
            ));
        }
        require_non_empty("schema_version", &self.schema_version)?;
        require_non_empty("snapshot_id", &self.snapshot_id)?;
        require_non_empty("component_id", &self.component_id)?;
        require_non_empty("observed_at", &self.observed_at)?;
        validate_non_empty_values("profile_refs", &self.profile_refs)?;
        if self.capabilities.is_empty() {
            return Err(BindingValidationError::new(
                "capabilities",
                "must contain at least one capability",
            ));
        }
        for capability in &self.capabilities {
            capability.validate()?;
        }
        Ok(())
    }
}

#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum JobTerminality {
    Pending,
    Terminal,
    Indeterminate,
}

/// Request for deferred work. Acceptance does not imply completion.
#[derive(Clone, Debug, Deserialize, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct JobRequest<T = Value> {
    pub schema: String,
    pub schema_version: String,
    pub job_id: String,
    pub job_type: String,
    pub owner_component_id: String,
    pub correlation: CorrelationContext,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub identity: Option<IdentityContext>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub idempotency: Option<IdempotencyContext>,
    pub requested_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub expires_at: Option<String>,
    pub payload_schema: String,
    pub payload: T,
}

impl<T> JobRequest<T> {
    pub fn validate_metadata(&self) -> Result<(), BindingValidationError> {
        if self.schema != schema::JOB_REQUEST {
            return Err(BindingValidationError::new(
                "schema",
                "must identify the common job-request schema",
            ));
        }
        require_non_empty("schema_version", &self.schema_version)?;
        require_non_empty("job_id", &self.job_id)?;
        require_non_empty("job_type", &self.job_type)?;
        require_non_empty("owner_component_id", &self.owner_component_id)?;
        require_non_empty("requested_at", &self.requested_at)?;
        require_non_empty("payload_schema", &self.payload_schema)?;
        optional_non_empty("expires_at", self.expires_at.as_deref())?;
        self.correlation.validate()?;
        if let Some(identity) = &self.identity {
            identity.validate()?;
        }
        if let Some(idempotency) = &self.idempotency {
            idempotency.validate()?;
        }
        Ok(())
    }
}

/// Observable state of a deferred job.
#[derive(Clone, Debug, Deserialize, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct JobStatus<T = Value> {
    pub schema: String,
    pub schema_version: String,
    pub job_id: String,
    pub owner_component_id: String,
    pub availability: CapabilityAvailability,
    pub execution_state: ExecutionState,
    pub authoritative_outcome: AuthoritativeOutcome,
    pub terminality: JobTerminality,
    pub observed_at: String,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub reason_codes: Vec<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub result_schema: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub result: Option<T>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub receipt_refs: Vec<String>,
}

impl<T> JobStatus<T> {
    pub fn validate_metadata(&self) -> Result<(), BindingValidationError> {
        if self.schema != schema::JOB_STATUS {
            return Err(BindingValidationError::new(
                "schema",
                "must identify the common job-status schema",
            ));
        }
        require_non_empty("schema_version", &self.schema_version)?;
        require_non_empty("job_id", &self.job_id)?;
        require_non_empty("owner_component_id", &self.owner_component_id)?;
        require_non_empty("observed_at", &self.observed_at)?;
        validate_non_empty_values("reason_codes", &self.reason_codes)?;
        validate_non_empty_values("receipt_refs", &self.receipt_refs)?;
        match (&self.result_schema, &self.result) {
            (Some(schema), Some(_)) => require_non_empty("result_schema", schema),
            (None, None) => Ok(()),
            _ => Err(BindingValidationError::new(
                "result",
                "result and result_schema must be present or absent together",
            )),
        }
    }
}

/// A stable, human-readable validation error for local binding checks.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct BindingValidationError {
    field: &'static str,
    message: &'static str,
}

impl BindingValidationError {
    #[must_use]
    pub const fn new(field: &'static str, message: &'static str) -> Self {
        Self { field, message }
    }

    #[must_use]
    pub const fn field(&self) -> &'static str {
        self.field
    }

    #[must_use]
    pub const fn message(&self) -> &'static str {
        self.message
    }
}

impl std::fmt::Display for BindingValidationError {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{}: {}", self.field, self.message)
    }
}

impl std::error::Error for BindingValidationError {}

pub(crate) fn require_non_empty(
    field: &'static str,
    value: &str,
) -> Result<(), BindingValidationError> {
    if value.trim().is_empty() {
        Err(BindingValidationError::new(field, "must not be empty"))
    } else {
        Ok(())
    }
}

pub(crate) fn optional_non_empty(
    field: &'static str,
    value: Option<&str>,
) -> Result<(), BindingValidationError> {
    if let Some(value) = value {
        require_non_empty(field, value)?;
    }
    Ok(())
}

pub(crate) fn validate_non_empty_values(
    field: &'static str,
    values: &[String],
) -> Result<(), BindingValidationError> {
    if values.iter().any(|value| value.trim().is_empty()) {
        Err(BindingValidationError::new(
            field,
            "must not contain empty values",
        ))
    } else {
        Ok(())
    }
}
