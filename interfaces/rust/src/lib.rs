//! Stable Rust bindings for the common kOA implementation interfaces.
//!
//! These types represent transport envelopes and shared operational records.
//! They do not confer business authority and do not replace component-owned
//! domain contracts.

#![forbid(unsafe_code)]

use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::collections::{BTreeMap, BTreeSet};

pub mod client;
pub mod error;
pub mod health;
pub mod receipt;

pub use client::{InterfaceClient, Transport};
pub use error::{ClientError, ErrorCategory, ErrorEnvelope, TransportError};
pub use health::{
    CapabilityReadiness, DependencyHealth, DependencyRequirement, Freshness, HealthStatus,
    OperationalState, ReadinessClass, ReadinessStatus,
};
pub use receipt::{
    CommitState, DecisionState, DisclosureClass, ReceiptClass, ReceiptEnvelope, ReceiptOutcome,
};

/// Canonical repository-relative schema identifiers consumed by this crate.
pub mod schema {
    pub const EVENT_ENVELOPE: &str = "interfaces/transport/event-envelope.schema.json";
    pub const ERROR_ENVELOPE: &str = "interfaces/transport/error-envelope.schema.json";
    pub const IDEMPOTENCY: &str = "interfaces/transport/idempotency.schema.json";
    pub const VERSION_NEGOTIATION: &str = "interfaces/transport/version-negotiation.schema.json";
    pub const HEALTH_STATUS: &str = "interfaces/health/health-status.schema.json";
    pub const READINESS: &str = "interfaces/health/readiness.schema.json";
    pub const RECEIPT_ENVELOPE: &str = "interfaces/receipts/receipt-envelope.schema.json";
    pub const CORRELATION: &str = "interfaces/receipts/correlation.schema.json";
    pub const JOB_REQUEST: &str = "interfaces/jobs/job-request.schema.json";
    pub const JOB_STATUS: &str = "interfaces/jobs/job-status.schema.json";
    pub const IDENTITY_CONTEXT: &str = "interfaces/identity/identity-context.schema.json";
    pub const CAPABILITY_SNAPSHOT: &str = "interfaces/capabilities/capability-snapshot.schema.json";
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
    pub fn new(schema_version: impl Into<String>, actor_ref: impl Into<String>) -> Self {
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

/// Scope of one canonical idempotency identity.
#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct IdempotencyScope {
    pub kind: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub target_ref: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub workflow_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub step_id: Option<String>,
}

/// Canonical request fingerprint protected by the idempotency key.
#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct IdempotencyCanonicalRequest {
    pub algorithm: String,
    pub digest: String,
    pub media_type: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub schema_ref: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub schema_version: Option<String>,
}

/// Optional expected owner state associated with a retry.
#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct IdempotencyExpectedState {
    pub kind: String,
    pub value: String,
}

/// Declared duplicate behavior enforced by the receiving owner.
#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct IdempotencyDuplicateHandling {
    pub action: String,
    pub result_consistency: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub terminal_result_ref_required: Option<bool>,
}

/// Validity and terminal-result retention for the idempotency identity.
#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct IdempotencyValidity {
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub expires_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub retain_terminal_result_seconds: Option<u64>,
}

/// Optional replay-resistant material.
#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct IdempotencyAntiReplay {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub nonce: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub sequence: Option<u64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub challenge_ref: Option<String>,
}

/// Authority invariants carried with every canonical idempotency identity.
#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct IdempotencyAuthority {
    pub receiving_owner_enforces: bool,
    pub transport_grants_authority: bool,
    pub duplicate_effects_permitted: bool,
}

/// Stable retry identity bound to one canonical request body.
#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct IdempotencyContext {
    pub schema_version: String,
    pub idempotency_key: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub request_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub correlation_id: Option<String>,
    pub operation: String,
    pub owner_component_id: String,
    pub scope: IdempotencyScope,
    pub canonical_request: IdempotencyCanonicalRequest,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub expected_state: Option<IdempotencyExpectedState>,
    pub duplicate_handling: IdempotencyDuplicateHandling,
    pub validity: IdempotencyValidity,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub anti_replay: Option<IdempotencyAntiReplay>,
    pub authority: IdempotencyAuthority,
}

impl IdempotencyContext {
    pub fn validate(&self) -> Result<(), BindingValidationError> {
        if self.schema_version != "1.0.0" {
            return Err(BindingValidationError::new(
                "schema_version",
                "must be 1.0.0",
            ));
        }
        require_non_empty("idempotency_key", &self.idempotency_key)?;
        optional_non_empty("request_id", self.request_id.as_deref())?;
        optional_non_empty("correlation_id", self.correlation_id.as_deref())?;
        require_non_empty("operation", &self.operation)?;
        require_non_empty("owner_component_id", &self.owner_component_id)?;

        match self.scope.kind.as_str() {
            "owner_operation" => {},
            "owner_operation_target" => {
                if self.scope.target_ref.as_deref().unwrap_or("").is_empty() {
                    return Err(BindingValidationError::new(
                        "scope.target_ref",
                        "is required for owner_operation_target",
                    ));
                }
            },
            "workflow_step" => {
                if self.scope.workflow_id.as_deref().unwrap_or("").is_empty() {
                    return Err(BindingValidationError::new(
                        "scope.workflow_id",
                        "is required for workflow_step",
                    ));
                }
                if self.scope.step_id.as_deref().unwrap_or("").is_empty() {
                    return Err(BindingValidationError::new(
                        "scope.step_id",
                        "is required for workflow_step",
                    ));
                }
            },
            _ => {
                return Err(BindingValidationError::new(
                    "scope.kind",
                    "must be owner_operation, owner_operation_target, or workflow_step",
                ));
            },
        }
        optional_non_empty("scope.target_ref", self.scope.target_ref.as_deref())?;
        optional_non_empty("scope.workflow_id", self.scope.workflow_id.as_deref())?;
        optional_non_empty("scope.step_id", self.scope.step_id.as_deref())?;

        if self.canonical_request.algorithm != "sha256" {
            return Err(BindingValidationError::new(
                "canonical_request.algorithm",
                "must be sha256",
            ));
        }
        if self.canonical_request.digest.len() != 64
            || !self
                .canonical_request
                .digest
                .bytes()
                .all(|byte| byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte))
        {
            return Err(BindingValidationError::new(
                "canonical_request.digest",
                "must be 64 lowercase hexadecimal characters",
            ));
        }
        require_non_empty(
            "canonical_request.media_type",
            &self.canonical_request.media_type,
        )?;
        match (
            self.canonical_request.schema_ref.as_deref(),
            self.canonical_request.schema_version.as_deref(),
        ) {
            (Some(schema_ref), Some(schema_version)) => {
                require_non_empty("canonical_request.schema_ref", schema_ref)?;
                require_non_empty("canonical_request.schema_version", schema_version)?;
            },
            (None, None) => {},
            _ => {
                return Err(BindingValidationError::new(
                    "canonical_request.schema_ref",
                    "schema_ref and schema_version must be provided together",
                ));
            },
        }

        if let Some(expected_state) = &self.expected_state {
            if !matches!(
                expected_state.kind.as_str(),
                "version" | "etag" | "digest" | "state_id"
            ) {
                return Err(BindingValidationError::new(
                    "expected_state.kind",
                    "must be version, etag, digest, or state_id",
                ));
            }
            require_non_empty("expected_state.value", &expected_state.value)?;
        }

        let expected_consistency = match self.duplicate_handling.action.as_str() {
            "return_prior_result" => Some("exact_prior_result"),
            "resume_existing_operation" => Some("current_status"),
            "reject_duplicate" => None,
            "reconcile_before_retry" => Some("reconciled_result"),
            _ => {
                return Err(BindingValidationError::new(
                    "duplicate_handling.action",
                    "contains an unsupported duplicate action",
                ));
            },
        };
        if !matches!(
            self.duplicate_handling.result_consistency.as_str(),
            "exact_prior_result" | "current_status" | "reconciled_result"
        ) {
            return Err(BindingValidationError::new(
                "duplicate_handling.result_consistency",
                "contains an unsupported consistency mode",
            ));
        }
        if let Some(expected) = expected_consistency {
            if self.duplicate_handling.result_consistency != expected {
                return Err(BindingValidationError::new(
                    "duplicate_handling.result_consistency",
                    "does not match duplicate_handling.action",
                ));
            }
        }
        if self.duplicate_handling.action == "return_prior_result"
            && self.duplicate_handling.terminal_result_ref_required != Some(true)
        {
            return Err(BindingValidationError::new(
                "duplicate_handling.terminal_result_ref_required",
                "must be true for return_prior_result",
            ));
        }

        require_non_empty("validity.created_at", &self.validity.created_at)?;
        optional_non_empty("validity.expires_at", self.validity.expires_at.as_deref())?;

        if let Some(anti_replay) = &self.anti_replay {
            if anti_replay.nonce.is_none()
                && anti_replay.sequence.is_none()
                && anti_replay.challenge_ref.is_none()
            {
                return Err(BindingValidationError::new(
                    "anti_replay",
                    "must contain at least one replay-resistant value",
                ));
            }
            optional_non_empty("anti_replay.nonce", anti_replay.nonce.as_deref())?;
            optional_non_empty(
                "anti_replay.challenge_ref",
                anti_replay.challenge_ref.as_deref(),
            )?;
        }

        if !self.authority.receiving_owner_enforces {
            return Err(BindingValidationError::new(
                "authority.receiving_owner_enforces",
                "must be true",
            ));
        }
        if self.authority.transport_grants_authority {
            return Err(BindingValidationError::new(
                "authority.transport_grants_authority",
                "must be false",
            ));
        }
        if self.authority.duplicate_effects_permitted {
            return Err(BindingValidationError::new(
                "authority.duplicate_effects_permitted",
                "must be false",
            ));
        }
        Ok(())
    }
}

/// Explicit message class for interface-version negotiation.
#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum VersionNegotiationMessageType {
    VersionOffer,
    VersionSelection,
    VersionRejection,
}

/// Component endpoint participating in a version negotiation.
#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct VersionNegotiationSender {
    pub component_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub instance_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub profile_id: Option<String>,
}

/// Receiver selector kind admitted by the canonical negotiation schema.
#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum VersionReceiverKind {
    Component,
    Capability,
    Subscription,
    Topic,
}

/// Intended receiver of one version-negotiation message.
#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct VersionReceiverSelector {
    pub kind: VersionReceiverKind,
    pub identifier: String,
}

/// Compatibility interpretation attached to an explicit selection.
#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum VersionCompatibilityMode {
    Exact,
    BackwardCompatible,
    CoordinatedTransitionRequired,
}

/// Closed reason vocabulary for explicit version rejection.
#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum VersionRejectionReason {
    NoCommonVersion,
    InterfaceUnknown,
    ContractInactive,
    ContractInvalid,
    ReleaseIncompatible,
    CoordinatedTransitionRequired,
}

/// Explicit rejection preserving the previously valid state.
#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct VersionRejection {
    pub reason_code: VersionRejectionReason,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub message: Option<String>,
    pub existing_valid_state_preserved: bool,
}

/// Optional release context carried during negotiation.
#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct VersionReleaseContext {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub release_set_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub sender_release: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub receiver_release: Option<String>,
}

/// Authority invariants carried by every version-negotiation message.
#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct VersionNegotiationAuthority {
    pub transport_grants_authority: bool,
    pub selection_changes_domain_authority: bool,
    pub receiving_contract_remains_authoritative: bool,
}

/// Canonical offer, selection, or rejection for one declared interface.
#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct VersionNegotiation {
    pub schema_version: String,
    pub message_type: VersionNegotiationMessageType,
    pub negotiation_id: String,
    pub interface_id: String,
    pub sender: VersionNegotiationSender,
    pub intended_receiver: VersionReceiverSelector,
    pub correlation_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub offered_versions: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub preferred_version: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub selected_version: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub compatibility_mode: Option<VersionCompatibilityMode>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub rejection: Option<VersionRejection>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub release_context: Option<VersionReleaseContext>,
    pub automatic_schema_guessing: bool,
    pub authority: VersionNegotiationAuthority,
}

impl VersionNegotiation {
    pub fn validate(&self) -> Result<(), BindingValidationError> {
        if self.schema_version != "1.0.0" {
            return Err(BindingValidationError::new(
                "schema_version",
                "must be 1.0.0",
            ));
        }
        require_non_empty("negotiation_id", &self.negotiation_id)?;
        require_non_empty("interface_id", &self.interface_id)?;
        require_non_empty("sender.component_id", &self.sender.component_id)?;
        optional_non_empty("sender.instance_id", self.sender.instance_id.as_deref())?;
        optional_non_empty("sender.profile_id", self.sender.profile_id.as_deref())?;
        require_non_empty(
            "intended_receiver.identifier",
            &self.intended_receiver.identifier,
        )?;
        require_non_empty("correlation_id", &self.correlation_id)?;

        if let Some(offered_versions) = &self.offered_versions {
            if offered_versions.is_empty() {
                return Err(BindingValidationError::new(
                    "offered_versions",
                    "must contain at least one version",
                ));
            }
            validate_non_empty_values("offered_versions", offered_versions)?;
            let mut seen = BTreeSet::new();
            for version in offered_versions {
                if !seen.insert(version) {
                    return Err(BindingValidationError::new(
                        "offered_versions",
                        "must not contain duplicates",
                    ));
                }
            }
        }
        optional_non_empty("preferred_version", self.preferred_version.as_deref())?;
        optional_non_empty("selected_version", self.selected_version.as_deref())?;

        if let (Some(preferred), Some(offered)) = (
            self.preferred_version.as_deref(),
            self.offered_versions.as_ref(),
        ) {
            if !offered.iter().any(|version| version == preferred) {
                return Err(BindingValidationError::new(
                    "preferred_version",
                    "must be present in offered_versions",
                ));
            }
        }
        if let (Some(selected), Some(offered)) = (
            self.selected_version.as_deref(),
            self.offered_versions.as_ref(),
        ) {
            if !offered.iter().any(|version| version == selected) {
                return Err(BindingValidationError::new(
                    "selected_version",
                    "must be present in offered_versions",
                ));
            }
        }

        if let Some(rejection) = &self.rejection {
            optional_non_empty("rejection.message", rejection.message.as_deref())?;
            if !rejection.existing_valid_state_preserved {
                return Err(BindingValidationError::new(
                    "rejection.existing_valid_state_preserved",
                    "must be true",
                ));
            }
        }

        if let Some(release_context) = &self.release_context {
            if release_context.release_set_id.is_none()
                && release_context.sender_release.is_none()
                && release_context.receiver_release.is_none()
            {
                return Err(BindingValidationError::new(
                    "release_context",
                    "must contain at least one release value",
                ));
            }
            optional_non_empty(
                "release_context.release_set_id",
                release_context.release_set_id.as_deref(),
            )?;
            optional_non_empty(
                "release_context.sender_release",
                release_context.sender_release.as_deref(),
            )?;
            optional_non_empty(
                "release_context.receiver_release",
                release_context.receiver_release.as_deref(),
            )?;
        }

        if self.automatic_schema_guessing {
            return Err(BindingValidationError::new(
                "automatic_schema_guessing",
                "must be false",
            ));
        }
        if self.authority.transport_grants_authority {
            return Err(BindingValidationError::new(
                "authority.transport_grants_authority",
                "must be false",
            ));
        }
        if self.authority.selection_changes_domain_authority {
            return Err(BindingValidationError::new(
                "authority.selection_changes_domain_authority",
                "must be false",
            ));
        }
        if !self.authority.receiving_contract_remains_authoritative {
            return Err(BindingValidationError::new(
                "authority.receiving_contract_remains_authoritative",
                "must be true",
            ));
        }

        match self.message_type {
            VersionNegotiationMessageType::VersionOffer => {
                if self.offered_versions.is_none() || self.preferred_version.is_none() {
                    return Err(BindingValidationError::new(
                        "message_type",
                        "version_offer requires offered_versions and preferred_version",
                    ));
                }
                if self.selected_version.is_some() || self.rejection.is_some() {
                    return Err(BindingValidationError::new(
                        "message_type",
                        "version_offer must omit selected_version and rejection",
                    ));
                }
            },
            VersionNegotiationMessageType::VersionSelection => {
                if self.offered_versions.is_none()
                    || self.selected_version.is_none()
                    || self.compatibility_mode.is_none()
                {
                    return Err(BindingValidationError::new(
                        "message_type",
                        "version_selection requires offered_versions, selected_version and compatibility_mode",
                    ));
                }
                if self.rejection.is_some() {
                    return Err(BindingValidationError::new(
                        "message_type",
                        "version_selection must omit rejection",
                    ));
                }
            },
            VersionNegotiationMessageType::VersionRejection => {
                if self.rejection.is_none() {
                    return Err(BindingValidationError::new(
                        "message_type",
                        "version_rejection requires rejection",
                    ));
                }
                if self.selected_version.is_some() {
                    return Err(BindingValidationError::new(
                        "message_type",
                        "version_rejection must omit selected_version",
                    ));
                }
            },
        }
        Ok(())
    }
}

/// Interface identity carried by the canonical domain-event envelope.
#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct EventInterfaceReference {
    pub interface_id: String,
    pub interface_version: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub contract_ref: Option<String>,
}

/// Publishing component endpoint for a committed domain event.
#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct EventPublisher {
    pub component_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub instance_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub profile_id: Option<String>,
}

#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum EventReceiverKind {
    Component,
    Capability,
    Subscription,
    Topic,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct EventReceiverSelector {
    pub kind: EventReceiverKind,
    pub identifier: String,
}

/// Event-local correlation projection. Request identity remains required by the
/// synchronous client even though the canonical event schema permits it to be omitted.
#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct EventCorrelationContext {
    pub correlation_id: String,
    pub request_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub causation_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub trace_id: Option<String>,
}

#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum PayloadEncoding {
    Identity,
    Base64,
    UriReference,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct ContentDigest {
    pub algorithm: String,
    pub value: String,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct EventPayloadRepresentation {
    pub media_type: String,
    pub schema_ref: String,
    pub schema_version: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub encoding: Option<PayloadEncoding>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub content_digest: Option<ContentDigest>,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct EventOrdering {
    pub scope: String,
    pub sequence: u64,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub partition_key: Option<String>,
}

#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum ReplayMode {
    Original,
    Replay,
}

#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum DuplicateHandling {
    IgnoreIfApplied,
    ReturnCurrentState,
    RebuildProjection,
    RejectDuplicate,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct EventReplay {
    pub mode: ReplayMode,
    pub duplicate_handling: DuplicateHandling,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub original_message_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub replayed_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub replay_reason: Option<String>,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct EventReleaseContext {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub release_set_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub sender_release: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub receiver_release: Option<String>,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct EventCompatibility {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub minimum_consumer_version: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub release_context: Option<EventReleaseContext>,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct EventDisclosure {
    pub class: DisclosureClass,
    pub payload_minimized: bool,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub redaction_applied: Option<bool>,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct EventEvidence {
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub receipt_refs: Vec<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub evidence_refs: Vec<String>,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct EventAuthority {
    pub effect: String,
    pub publisher_owns_fact: bool,
    pub grants_mutation_authority: bool,
    pub transfers_ownership: bool,
}

/// Canonical domain-event envelope projected from event-envelope.schema.json.
#[derive(Clone, Debug, Deserialize, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct EventEnvelope<T = Value> {
    pub schema_version: String,
    pub envelope_type: String,
    pub message_id: String,
    pub event_id: String,
    pub event_type: String,
    pub event_version: String,
    pub interface: EventInterfaceReference,
    pub publisher: EventPublisher,
    pub intended_receivers: Vec<EventReceiverSelector>,
    pub correlation: EventCorrelationContext,
    pub occurred_at: String,
    pub committed_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub expires_at: Option<String>,
    pub payload_representation: EventPayloadRepresentation,
    pub payload: T,
    pub ordering: EventOrdering,
    pub replay: EventReplay,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub compatibility: Option<EventCompatibility>,
    pub disclosure: EventDisclosure,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub evidence: Option<EventEvidence>,
    pub authority: EventAuthority,
}

impl<T> EventEnvelope<T> {
    pub fn validate_metadata(&self) -> Result<(), BindingValidationError> {
        if self.schema_version != "1.0.0" {
            return Err(BindingValidationError::new(
                "schema_version",
                "must equal the canonical event-envelope schema version 1.0.0",
            ));
        }
        if self.envelope_type != "domain_event" {
            return Err(BindingValidationError::new(
                "envelope_type",
                "must be domain_event",
            ));
        }
        require_non_empty("message_id", &self.message_id)?;
        require_non_empty("event_id", &self.event_id)?;
        require_non_empty("event_type", &self.event_type)?;
        require_non_empty("event_version", &self.event_version)?;
        require_non_empty("interface.interface_id", &self.interface.interface_id)?;
        require_non_empty(
            "interface.interface_version",
            &self.interface.interface_version,
        )?;
        optional_non_empty(
            "interface.contract_ref",
            self.interface.contract_ref.as_deref(),
        )?;
        require_non_empty("publisher.component_id", &self.publisher.component_id)?;
        optional_non_empty(
            "publisher.instance_id",
            self.publisher.instance_id.as_deref(),
        )?;
        optional_non_empty("publisher.profile_id", self.publisher.profile_id.as_deref())?;
        if self.intended_receivers.is_empty() {
            return Err(BindingValidationError::new(
                "intended_receivers",
                "must contain at least one receiver",
            ));
        }
        for receiver in &self.intended_receivers {
            require_non_empty("intended_receivers.identifier", &receiver.identifier)?;
        }
        require_non_empty(
            "correlation.correlation_id",
            &self.correlation.correlation_id,
        )?;
        require_non_empty("correlation.request_id", &self.correlation.request_id)?;
        optional_non_empty(
            "correlation.causation_id",
            self.correlation.causation_id.as_deref(),
        )?;
        optional_non_empty("correlation.trace_id", self.correlation.trace_id.as_deref())?;
        require_non_empty("occurred_at", &self.occurred_at)?;
        require_non_empty("committed_at", &self.committed_at)?;
        optional_non_empty("expires_at", self.expires_at.as_deref())?;
        require_non_empty(
            "payload_representation.media_type",
            &self.payload_representation.media_type,
        )?;
        require_non_empty(
            "payload_representation.schema_ref",
            &self.payload_representation.schema_ref,
        )?;
        require_non_empty(
            "payload_representation.schema_version",
            &self.payload_representation.schema_version,
        )?;
        if let Some(digest) = &self.payload_representation.content_digest {
            if digest.algorithm != "sha256" {
                return Err(BindingValidationError::new(
                    "payload_representation.content_digest.algorithm",
                    "must be sha256",
                ));
            }
            if digest.value.len() != 64
                || !digest
                    .value
                    .bytes()
                    .all(|byte| byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte))
            {
                return Err(BindingValidationError::new(
                    "payload_representation.content_digest.value",
                    "must be lowercase sha256 hexadecimal",
                ));
            }
        }
        require_non_empty("ordering.scope", &self.ordering.scope)?;
        optional_non_empty(
            "ordering.partition_key",
            self.ordering.partition_key.as_deref(),
        )?;
        match self.replay.mode {
            ReplayMode::Original => {
                if self.replay.original_message_id.is_some()
                    || self.replay.replayed_at.is_some()
                    || self.replay.replay_reason.is_some()
                {
                    return Err(BindingValidationError::new(
                        "replay",
                        "original mode must omit replay-only fields",
                    ));
                }
            },
            ReplayMode::Replay => {
                if self.replay.original_message_id.is_none() || self.replay.replayed_at.is_none() {
                    return Err(BindingValidationError::new(
                        "replay",
                        "replay mode requires original_message_id and replayed_at",
                    ));
                }
                optional_non_empty(
                    "replay.original_message_id",
                    self.replay.original_message_id.as_deref(),
                )?;
                optional_non_empty("replay.replayed_at", self.replay.replayed_at.as_deref())?;
                optional_non_empty("replay.replay_reason", self.replay.replay_reason.as_deref())?;
            },
        }
        if !self.disclosure.payload_minimized {
            return Err(BindingValidationError::new(
                "disclosure.payload_minimized",
                "must be true",
            ));
        }
        if let Some(compatibility) = &self.compatibility {
            if compatibility.minimum_consumer_version.is_none()
                && compatibility.release_context.is_none()
            {
                return Err(BindingValidationError::new(
                    "compatibility",
                    "must contain at least one property",
                ));
            }
        }
        if let Some(evidence) = &self.evidence {
            if evidence.receipt_refs.is_empty() && evidence.evidence_refs.is_empty() {
                return Err(BindingValidationError::new(
                    "evidence",
                    "must contain at least one reference",
                ));
            }
            validate_non_empty_values("evidence.receipt_refs", &evidence.receipt_refs)?;
            validate_non_empty_values("evidence.evidence_refs", &evidence.evidence_refs)?;
        }
        if self.authority.effect != "committed_fact_evidence"
            || !self.authority.publisher_owns_fact
            || self.authority.grants_mutation_authority
            || self.authority.transfers_ownership
        {
            return Err(BindingValidationError::new(
                "authority",
                "must preserve committed-fact ownership semantics",
            ));
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
