use crate::{
    require_non_empty, validate_non_empty_values, BindingValidationError, ContentDigest,
    DisclosureClass, EventInterfaceReference, EventPayloadRepresentation, EventPublisher,
    EventReceiverSelector,
};
use serde::{Deserialize, Serialize};

/// Canonical error classes from `interfaces/transport/error-envelope.schema.json`.
#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum ErrorCategory {
    Validation,
    Authentication,
    Authorization,
    Policy,
    Compatibility,
    Conflict,
    NotFound,
    RateLimit,
    Resource,
    Timeout,
    Dependency,
    Transport,
    Internal,
    IndeterminateOutcome,
}

/// Historical outcome vocabulary retained for source compatibility.
///
/// The canonical error envelope now carries an explicit `outcome` object and
/// does not serialize this enum directly.
#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum OutcomeKnowledge {
    KnownNoEffect,
    KnownFinalEffect,
    Indeterminate,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct ErrorCorrelationContext {
    pub correlation_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub causation_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub request_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub trace_id: Option<String>,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct ErrorReleaseContext {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub release_set_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub sender_release: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub receiver_release: Option<String>,
}

#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum ErrorOutcomeState {
    Rejected,
    Blocked,
    Failed,
    Expired,
    Cancelled,
    Indeterminate,
}

#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum ErrorFinality {
    Final,
    NonFinal,
    Indeterminate,
}

#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum ErrorAuthoritativeEffect {
    None,
    Unchanged,
    UnknownRequiresResolution,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct ErrorOutcome {
    pub state: ErrorOutcomeState,
    pub finality: ErrorFinality,
    pub authoritative_effect: ErrorAuthoritativeEffect,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub status_ref: Option<String>,
}

#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum ErrorRetryStrategy {
    None,
    Immediate,
    BoundedBackoff,
    StatusResolution,
    ManualIntervention,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct ErrorRetry {
    pub allowed: bool,
    pub strategy: ErrorRetryStrategy,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub after_seconds: Option<u64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub maximum_attempts: Option<u64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub idempotency_required: Option<bool>,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct ErrorFieldViolation {
    pub path: String,
    pub code: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub message: Option<String>,
}

#[derive(Clone, Debug, Default, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct ErrorDetails {
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub field_violations: Vec<ErrorFieldViolation>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub dependency_ref: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub expected_version: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub received_version: Option<String>,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct ErrorDisclosure {
    pub class: DisclosureClass,
    pub payload_minimized: bool,
    pub contains_secrets: bool,
}

#[derive(Clone, Debug, Default, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct ErrorEvidence {
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub receipt_refs: Vec<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub evidence_refs: Vec<String>,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct ErrorAuthority {
    pub transport_grants_authority: bool,
    pub error_grants_authority: bool,
    pub transfers_ownership: bool,
}

/// Machine-readable, data-minimized error envelope projected directly from the
/// canonical JSON Schema. Repository paths are metadata about the binding and
/// are deliberately not serialized into the wire envelope.
#[derive(Clone, Debug, Deserialize, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct ErrorEnvelope {
    pub schema_version: String,
    pub envelope_type: String,
    pub error_id: String,
    pub error_code: String,
    pub error_class: ErrorCategory,
    pub message: String,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub reason_codes: Vec<String>,
    pub interface: EventInterfaceReference,
    pub producer: EventPublisher,
    pub intended_receiver: EventReceiverSelector,
    pub correlation: ErrorCorrelationContext,
    pub occurred_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub payload_representation: Option<EventPayloadRepresentation>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub release_context: Option<ErrorReleaseContext>,
    pub outcome: ErrorOutcome,
    pub retry: ErrorRetry,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub details: Option<ErrorDetails>,
    pub disclosure: ErrorDisclosure,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub evidence: Option<ErrorEvidence>,
    pub authority: ErrorAuthority,
}

impl ErrorEnvelope {
    pub const SCHEMA_VERSION: &'static str = "1.0.0";
    pub const ENVELOPE_TYPE: &'static str = "error";

    pub fn validate(&self) -> Result<(), BindingValidationError> {
        if self.schema_version != Self::SCHEMA_VERSION {
            return Err(BindingValidationError::new(
                "schema_version",
                "must equal the canonical error-envelope version 1.0.0",
            ));
        }
        if self.envelope_type != Self::ENVELOPE_TYPE {
            return Err(BindingValidationError::new(
                "envelope_type",
                "must equal error",
            ));
        }
        require_non_empty("error_id", &self.error_id)?;
        require_non_empty("error_code", &self.error_code)?;
        require_non_empty("message", &self.message)?;
        require_non_empty("interface.interface_id", &self.interface.interface_id)?;
        require_non_empty(
            "interface.interface_version",
            &self.interface.interface_version,
        )?;
        require_non_empty("producer.component_id", &self.producer.component_id)?;
        require_non_empty(
            "intended_receiver.identifier",
            &self.intended_receiver.identifier,
        )?;
        require_non_empty("correlation.correlation_id", &self.correlation.correlation_id)?;
        require_non_empty("occurred_at", &self.occurred_at)?;
        validate_non_empty_values("reason_codes", &self.reason_codes)?;

        if let Some(payload) = &self.payload_representation {
            require_non_empty("payload_representation.media_type", &payload.media_type)?;
            require_non_empty("payload_representation.schema_ref", &payload.schema_ref)?;
            require_non_empty(
                "payload_representation.schema_version",
                &payload.schema_version,
            )?;
            if let Some(ContentDigest { algorithm, value }) = &payload.content_digest {
                if algorithm != "sha256" {
                    return Err(BindingValidationError::new(
                        "payload_representation.content_digest.algorithm",
                        "must equal sha256",
                    ));
                }
                require_non_empty("payload_representation.content_digest.value", value)?;
            }
        }

        if matches!(self.outcome.state, ErrorOutcomeState::Indeterminate) {
            if !matches!(self.outcome.finality, ErrorFinality::Indeterminate) {
                return Err(BindingValidationError::new(
                    "outcome.finality",
                    "indeterminate outcome requires indeterminate finality",
                ));
            }
            if !matches!(
                self.outcome.authoritative_effect,
                ErrorAuthoritativeEffect::UnknownRequiresResolution
            ) {
                return Err(BindingValidationError::new(
                    "outcome.authoritative_effect",
                    "indeterminate outcome requires unknown_requires_resolution",
                ));
            }
            if self.outcome.status_ref.is_none() {
                return Err(BindingValidationError::new(
                    "outcome.status_ref",
                    "indeterminate outcome requires status_ref",
                ));
            }
        }

        if !self.retry.allowed {
            if !matches!(self.retry.strategy, ErrorRetryStrategy::None) {
                return Err(BindingValidationError::new(
                    "retry.strategy",
                    "must be none when retry.allowed=false",
                ));
            }
            if self.retry.after_seconds.is_some() || self.retry.maximum_attempts.is_some() {
                return Err(BindingValidationError::new(
                    "retry.after_seconds",
                    "disabled retry cannot define timing or attempt limits",
                ));
            }
        }
        if matches!(self.retry.strategy, ErrorRetryStrategy::BoundedBackoff)
            && (self.retry.after_seconds.is_none() || self.retry.maximum_attempts.is_none())
        {
            return Err(BindingValidationError::new(
                "retry.after_seconds",
                "bounded_backoff requires after_seconds and maximum_attempts",
            ));
        }
        if matches!(self.retry.strategy, ErrorRetryStrategy::StatusResolution)
            && self.retry.idempotency_required != Some(true)
        {
            return Err(BindingValidationError::new(
                "retry.idempotency_required",
                "status_resolution requires idempotency_required=true",
            ));
        }

        if !self.disclosure.payload_minimized {
            return Err(BindingValidationError::new(
                "disclosure.payload_minimized",
                "must be true",
            ));
        }
        if self.disclosure.contains_secrets {
            return Err(BindingValidationError::new(
                "disclosure.contains_secrets",
                "must be false",
            ));
        }
        if self.authority.transport_grants_authority
            || self.authority.error_grants_authority
            || self.authority.transfers_ownership
        {
            return Err(BindingValidationError::new(
                "authority",
                "error transport cannot grant authority or transfer ownership",
            ));
        }

        if let Some(details) = &self.details {
            if details.field_violations.is_empty()
                && details.dependency_ref.is_none()
                && details.expected_version.is_none()
                && details.received_version.is_none()
            {
                return Err(BindingValidationError::new(
                    "details",
                    "must contain at least one declared detail",
                ));
            }
        }
        if let Some(evidence) = &self.evidence {
            if evidence.receipt_refs.is_empty() && evidence.evidence_refs.is_empty() {
                return Err(BindingValidationError::new(
                    "evidence",
                    "must contain at least one evidence reference",
                ));
            }
            validate_non_empty_values("evidence.receipt_refs", &evidence.receipt_refs)?;
            validate_non_empty_values("evidence.evidence_refs", &evidence.evidence_refs)?;
        }
        if let Some(release) = &self.release_context {
            if release.release_set_id.is_none()
                && release.sender_release.is_none()
                && release.receiver_release.is_none()
            {
                return Err(BindingValidationError::new(
                    "release_context",
                    "must contain at least one release field",
                ));
            }
        }
        Ok(())
    }

    #[must_use]
    pub fn retryable(&self) -> bool {
        self.retry.allowed
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
                error.error_code, error.error_class, error.message
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
