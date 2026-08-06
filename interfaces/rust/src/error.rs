use crate::{
    require_non_empty, schema, validate_non_empty_values,
    BindingValidationError, CorrelationContext,
};
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::collections::BTreeMap;

/// Stable error classes shared by component interfaces.
#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum ErrorCategory {
    InvalidRequest,
    AuthenticationRequired,
    AuthorizationDenied,
    NotFound,
    Conflict,
    ContractIncompatible,
    DependencyUnavailable,
    ResourceConstrained,
    Timeout,
    Cancelled,
    Expired,
    IndeterminateOutcome,
    InternalFailure,
}

/// Whether the receiver knows the final business outcome.
#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum OutcomeKnowledge {
    KnownNoEffect,
    KnownFinalEffect,
    Indeterminate,
}

/// Machine-readable, data-minimized error envelope.
#[derive(Clone, Debug, Deserialize, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct ErrorEnvelope {
    pub schema: String,
    pub schema_version: String,
    pub error_id: String,
    pub error_code: String,
    pub category: ErrorCategory,
    pub message: String,
    pub correlation: CorrelationContext,
    pub retryable: bool,
    pub outcome_knowledge: OutcomeKnowledge,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub retry_after_seconds: Option<u64>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub reason_codes: Vec<String>,
    #[serde(default, skip_serializing_if = "BTreeMap::is_empty")]
    pub details: BTreeMap<String, Value>,
    pub recorded_at: String,
}

impl ErrorEnvelope {
    pub fn validate(&self) -> Result<(), BindingValidationError> {
        if self.schema != schema::ERROR_ENVELOPE {
            return Err(BindingValidationError::new(
                "schema",
                "must identify the common error-envelope schema",
            ));
        }
        require_non_empty("schema_version", &self.schema_version)?;
        require_non_empty("error_id", &self.error_id)?;
        require_non_empty("error_code", &self.error_code)?;
        require_non_empty("message", &self.message)?;
        require_non_empty("recorded_at", &self.recorded_at)?;
        validate_non_empty_values("reason_codes", &self.reason_codes)?;
        self.correlation.validate()?;

        if self.retry_after_seconds.is_some() && !self.retryable {
            return Err(BindingValidationError::new(
                "retry_after_seconds",
                "requires retryable=true",
            ));
        }
        Ok(())
    }
}

/// Transport failure before a valid remote envelope is available.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct TransportError {
    kind: TransportErrorKind,
    message: String,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum TransportErrorKind {
    Unavailable,
    Timeout,
    Protocol,
    Io,
}

impl TransportError {
    #[must_use]
    pub fn new(kind: TransportErrorKind, message: impl Into<String>) -> Self {
        Self {
            kind,
            message: message.into(),
        }
    }

    #[must_use]
    pub const fn kind(&self) -> TransportErrorKind {
        self.kind
    }

    #[must_use]
    pub fn message(&self) -> &str {
        &self.message
    }
}

impl std::fmt::Display for TransportError {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{:?}: {}", self.kind, self.message)
    }
}

impl std::error::Error for TransportError {}

/// Failures returned by the minimal interface client.
#[derive(Debug)]
pub enum ClientError {
    RequestValidation(BindingValidationError),
    Serialization(serde_json::Error),
    Transport(TransportError),
    InvalidResponse(String),
    Remote(ErrorEnvelope),
}

impl std::fmt::Display for ClientError {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::RequestValidation(error) => write!(formatter, "invalid request: {error}"),
            Self::Serialization(error) => write!(formatter, "serialization failure: {error}"),
            Self::Transport(error) => write!(formatter, "transport failure: {error}"),
            Self::InvalidResponse(message) => write!(formatter, "invalid response: {message}"),
            Self::Remote(error) => write!(
                formatter,
                "remote error {} ({:?}): {}",
                error.error_code, error.category, error.message
            ),
        }
    }
}

impl std::error::Error for ClientError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::RequestValidation(error) => Some(error),
            Self::Serialization(error) => Some(error),
            Self::Transport(error) => Some(error),
            Self::InvalidResponse(_) | Self::Remote(_) => None,
        }
    }
}

impl From<BindingValidationError> for ClientError {
    fn from(value: BindingValidationError) -> Self {
        Self::RequestValidation(value)
    }
}

impl From<serde_json::Error> for ClientError {
    fn from(value: serde_json::Error) -> Self {
        Self::Serialization(value)
    }
}

impl From<TransportError> for ClientError {
    fn from(value: TransportError) -> Self {
        Self::Transport(value)
    }
}
