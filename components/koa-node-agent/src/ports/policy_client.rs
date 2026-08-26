//! Public port for consuming an externally owned policy decision.
//!
//! The Node Agent asks for or verifies a decision; it never creates policy
//! authority and never treats transport success as authorization.

use core::fmt;
use std::collections::BTreeSet;

use crate::domain::{AuthorizationClass, Operation};

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct PolicyEvaluationRequest {
    pub request_id: String,
    pub operation: Operation,
    pub authorization_class: AuthorizationClass,
    pub caller_identity_ref: String,
    pub service_identity_ref: String,
    pub profile_context_ref: String,
    pub target_refs: BTreeSet<String>,
    pub expected_state_ref: Option<String>,
    pub requested_at: u64,
    pub expires_at: u64,
}

impl PolicyEvaluationRequest {
    pub fn validate(&self) -> Result<(), PolicyClientError> {
        validate_token("request_id", &self.request_id)?;
        validate_reference("caller_identity_ref", &self.caller_identity_ref)?;
        validate_reference("service_identity_ref", &self.service_identity_ref)?;
        validate_reference("profile_context_ref", &self.profile_context_ref)?;
        if self.authorization_class != self.operation.authorization_class() {
            return Err(PolicyClientError::invalid(
                "authorization_class does not match the closed operation catalog",
            ));
        }
        if self.expires_at <= self.requested_at {
            return Err(PolicyClientError::invalid(
                "expires_at must be later than requested_at",
            ));
        }
        if self.target_refs.len() > 32 {
            return Err(PolicyClientError::invalid(
                "target_refs exceeds the closed request bound",
            ));
        }
        for target in &self.target_refs {
            validate_reference("target_ref", target)?;
        }
        if let Some(expected) = &self.expected_state_ref {
            validate_reference("expected_state_ref", expected)?;
        }
        if self.operation.mutates_host() && self.expected_state_ref.is_none() {
            return Err(PolicyClientError::invalid(
                "mutating operations require expected_state_ref",
            ));
        }
        Ok(())
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum PolicyDecisionStatus {
    Approved,
    Denied,
    Revoked,
    Indeterminate,
}

impl PolicyDecisionStatus {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::Approved => "approved",
            Self::Denied => "denied",
            Self::Revoked => "revoked",
            Self::Indeterminate => "indeterminate",
        }
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct PolicyDecisionRecord {
    pub decision_ref: String,
    pub request_id: String,
    pub operation: Operation,
    pub status: PolicyDecisionStatus,
    pub reason_codes: BTreeSet<String>,
    pub not_before: u64,
    pub expires_at: u64,
    pub authority_refs: BTreeSet<String>,
}

impl PolicyDecisionRecord {
    pub fn validate_for(
        &self,
        request: &PolicyEvaluationRequest,
        now: u64,
    ) -> Result<(), PolicyClientError> {
        request.validate()?;
        validate_reference("decision_ref", &self.decision_ref)?;
        if self.request_id != request.request_id {
            return Err(PolicyClientError::invalid(
                "policy request identity mismatch",
            ));
        }
        if self.operation != request.operation {
            return Err(PolicyClientError::invalid("policy operation mismatch"));
        }
        if self.reason_codes.is_empty() {
            return Err(PolicyClientError::invalid(
                "policy decision requires at least one reason code",
            ));
        }
        for reason in &self.reason_codes {
            validate_token("reason_code", reason)?;
        }
        if self.authority_refs.is_empty() {
            return Err(PolicyClientError::invalid(
                "policy decision requires an authority reference",
            ));
        }
        for authority in &self.authority_refs {
            validate_reference("authority_ref", authority)?;
        }
        if self.expires_at <= self.not_before {
            return Err(PolicyClientError::invalid(
                "policy decision validity window is empty",
            ));
        }
        if now < self.not_before || now >= self.expires_at {
            return Err(PolicyClientError::new(
                PolicyClientErrorCode::DecisionExpired,
                "policy decision is not valid at the execution instant",
            ));
        }
        if self.status != PolicyDecisionStatus::Approved {
            return Err(PolicyClientError::new(
                PolicyClientErrorCode::DecisionNotApproved,
                format!("policy decision status is {}", self.status.as_str()),
            ));
        }
        Ok(())
    }
}

pub trait PolicyClient: Send + Sync {
    fn evaluate(
        &self,
        request: &PolicyEvaluationRequest,
    ) -> Result<PolicyDecisionRecord, PolicyClientError>;
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum PolicyClientErrorCode {
    InvalidRequest,
    DependencyUnavailable,
    ProtocolViolation,
    DecisionExpired,
    DecisionNotApproved,
}

impl PolicyClientErrorCode {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::InvalidRequest => "invalid_request",
            Self::DependencyUnavailable => "dependency_unavailable",
            Self::ProtocolViolation => "protocol_violation",
            Self::DecisionExpired => "decision_expired",
            Self::DecisionNotApproved => "decision_not_approved",
        }
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct PolicyClientError {
    code: PolicyClientErrorCode,
    detail: String,
}

impl PolicyClientError {
    pub fn new(code: PolicyClientErrorCode, detail: impl Into<String>) -> Self {
        Self {
            code,
            detail: detail.into(),
        }
    }

    fn invalid(detail: impl Into<String>) -> Self {
        Self::new(PolicyClientErrorCode::InvalidRequest, detail)
    }

    pub const fn code(&self) -> PolicyClientErrorCode {
        self.code
    }

    pub fn detail(&self) -> &str {
        &self.detail
    }
}

impl fmt::Display for PolicyClientError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "{}: {}", self.code.as_str(), self.detail)
    }
}

impl std::error::Error for PolicyClientError {}

fn validate_token(name: &str, value: &str) -> Result<(), PolicyClientError> {
    if value.is_empty() || value.len() > 256 || value.chars().any(char::is_whitespace) {
        return Err(PolicyClientError::invalid(format!(
            "{name} must be a non-empty bounded token without whitespace"
        )));
    }
    if value.chars().any(char::is_control) {
        return Err(PolicyClientError::invalid(format!(
            "{name} may not contain control characters"
        )));
    }
    Ok(())
}

fn validate_reference(name: &str, value: &str) -> Result<(), PolicyClientError> {
    if value.is_empty() || value.len() > 1024 || value.trim() != value {
        return Err(PolicyClientError::invalid(format!(
            "{name} must be a non-empty bounded canonical reference"
        )));
    }
    if value.chars().any(char::is_control) {
        return Err(PolicyClientError::invalid(format!(
            "{name} may not contain control characters"
        )));
    }
    Ok(())
}
