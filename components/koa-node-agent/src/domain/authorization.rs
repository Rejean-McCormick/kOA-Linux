//! Time-bound authorization evidence consumed by the Node Agent.
//!
//! The Node Agent validates this evidence but never creates a policy decision.

use core::fmt;
use std::collections::BTreeSet;

use super::command::{AuthorizationClass, Operation};
use super::request::{CanonicalReference, NodeOperationRequest};

const MAX_AUTHORIZED_TARGETS: usize = 64;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum AuthorizationStatus {
    Approved,
    Denied,
    Revoked,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct AuthorizationDecision {
    decision_ref: Option<CanonicalReference>,
    status: AuthorizationStatus,
    operation: Operation,
    authorization_class: AuthorizationClass,
    caller_identity: CanonicalReference,
    service_identity: CanonicalReference,
    profile_context_ref: CanonicalReference,
    target_scope: BTreeSet<CanonicalReference>,
    expected_state_ref: Option<CanonicalReference>,
    not_before: u64,
    expires_at: u64,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct AuthorizationDecisionParts {
    pub decision_ref: Option<CanonicalReference>,
    pub status: AuthorizationStatus,
    pub operation: Operation,
    pub authorization_class: AuthorizationClass,
    pub caller_identity: CanonicalReference,
    pub service_identity: CanonicalReference,
    pub profile_context_ref: CanonicalReference,
    pub target_scope: Vec<CanonicalReference>,
    pub expected_state_ref: Option<CanonicalReference>,
    pub not_before: u64,
    pub expires_at: u64,
}

impl AuthorizationDecision {
    pub fn new(parts: AuthorizationDecisionParts) -> Result<Self, AuthorizationBuildError> {
        if parts.expires_at <= parts.not_before {
            return Err(AuthorizationBuildError::InvalidValidityWindow);
        }
        let target_count = parts.target_scope.len();
        if target_count > MAX_AUTHORIZED_TARGETS {
            return Err(AuthorizationBuildError::TooManyTargetScopeEntries);
        }
        let target_scope: BTreeSet<_> = parts.target_scope.into_iter().collect();
        if target_scope.len() != target_count {
            return Err(AuthorizationBuildError::DuplicateTargetScope);
        }
        Ok(Self {
            decision_ref: parts.decision_ref,
            status: parts.status,
            operation: parts.operation,
            authorization_class: parts.authorization_class,
            caller_identity: parts.caller_identity,
            service_identity: parts.service_identity,
            profile_context_ref: parts.profile_context_ref,
            target_scope,
            expected_state_ref: parts.expected_state_ref,
            not_before: parts.not_before,
            expires_at: parts.expires_at,
        })
    }

    pub fn decision_ref(&self) -> Option<&CanonicalReference> {
        self.decision_ref.as_ref()
    }

    pub const fn status(&self) -> AuthorizationStatus {
        self.status
    }

    pub const fn operation(&self) -> Operation {
        self.operation
    }

    pub const fn authorization_class(&self) -> AuthorizationClass {
        self.authorization_class
    }

    pub fn caller_identity(&self) -> &CanonicalReference {
        &self.caller_identity
    }

    pub fn service_identity(&self) -> &CanonicalReference {
        &self.service_identity
    }

    pub fn profile_context_ref(&self) -> &CanonicalReference {
        &self.profile_context_ref
    }

    pub fn target_scope(&self) -> &BTreeSet<CanonicalReference> {
        &self.target_scope
    }

    pub fn expected_state_ref(&self) -> Option<&CanonicalReference> {
        self.expected_state_ref.as_ref()
    }

    pub const fn not_before(&self) -> u64 {
        self.not_before
    }

    pub const fn expires_at(&self) -> u64 {
        self.expires_at
    }

    pub const fn is_temporally_valid_at(&self, now: u64) -> bool {
        now >= self.not_before && now < self.expires_at
    }

    pub fn validate_binding(
        &self,
        request: &NodeOperationRequest,
        now: u64,
        policy_decision_required: bool,
    ) -> Result<(), AuthorizationError> {
        match self.status {
            AuthorizationStatus::Approved => {}
            AuthorizationStatus::Denied => return Err(AuthorizationError::Denied),
            AuthorizationStatus::Revoked => return Err(AuthorizationError::Revoked),
        }
        if now < self.not_before {
            return Err(AuthorizationError::NotYetValid);
        }
        if now >= self.expires_at {
            return Err(AuthorizationError::Expired);
        }
        if self.operation != request.operation() {
            return Err(AuthorizationError::OperationMismatch);
        }
        if self.authorization_class != request.operation().authorization_class() {
            return Err(AuthorizationError::ClassMismatch);
        }
        if &self.caller_identity != request.caller_identity() {
            return Err(AuthorizationError::CallerMismatch);
        }
        if &self.service_identity != request.service_identity() {
            return Err(AuthorizationError::ServiceMismatch);
        }
        if &self.profile_context_ref != request.profile_context_ref() {
            return Err(AuthorizationError::ProfileMismatch);
        }
        if !request
            .artifact_or_target_refs()
            .is_subset(&self.target_scope)
        {
            return Err(AuthorizationError::TargetScopeMismatch);
        }

        if request.operation().mutates_host() {
            let requested_state = request
                .expected_current_state()
                .ok_or(AuthorizationError::ExpectedStateMismatch)?;
            if self.expected_state_ref.as_ref() != Some(requested_state.state_ref()) {
                return Err(AuthorizationError::ExpectedStateMismatch);
            }
        }

        if policy_decision_required {
            let request_ref = request
                .policy_decision_ref()
                .ok_or(AuthorizationError::DecisionReferenceRequired)?;
            if self.decision_ref.as_ref() != Some(request_ref) {
                return Err(AuthorizationError::DecisionReferenceMismatch);
            }
        } else if let Some(request_ref) = request.policy_decision_ref() {
            if self.decision_ref.as_ref() != Some(request_ref) {
                return Err(AuthorizationError::DecisionReferenceMismatch);
            }
        }

        Ok(())
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum AuthorizationBuildError {
    InvalidValidityWindow,
    DuplicateTargetScope,
    TooManyTargetScopeEntries,
}

impl fmt::Display for AuthorizationBuildError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(match self {
            Self::InvalidValidityWindow => {
                "authorization expiry must be later than its not-before time"
            }
            Self::DuplicateTargetScope => "authorization target scope contains duplicates",
            Self::TooManyTargetScopeEntries => {
                "authorization target scope exceeds the bounded entry limit"
            }
        })
    }
}

impl std::error::Error for AuthorizationBuildError {}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum AuthorizationError {
    Denied,
    Revoked,
    NotYetValid,
    Expired,
    OperationMismatch,
    ClassMismatch,
    CallerMismatch,
    ServiceMismatch,
    ProfileMismatch,
    TargetScopeMismatch,
    ExpectedStateMismatch,
    DecisionReferenceRequired,
    DecisionReferenceMismatch,
}

impl AuthorizationError {
    pub const fn code(self) -> &'static str {
        match self {
            Self::Denied => "authorization_denied",
            Self::Revoked => "authorization_revoked",
            Self::NotYetValid => "authorization_not_yet_valid",
            Self::Expired => "authorization_expired",
            Self::OperationMismatch => "authorization_operation_mismatch",
            Self::ClassMismatch => "authorization_class_mismatch",
            Self::CallerMismatch => "authorization_caller_mismatch",
            Self::ServiceMismatch => "authorization_service_mismatch",
            Self::ProfileMismatch => "authorization_profile_mismatch",
            Self::TargetScopeMismatch => "authorization_target_scope_mismatch",
            Self::ExpectedStateMismatch => "authorization_expected_state_mismatch",
            Self::DecisionReferenceRequired => "authorization_decision_reference_required",
            Self::DecisionReferenceMismatch => "authorization_decision_reference_mismatch",
        }
    }
}

impl fmt::Display for AuthorizationError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(self.code())
    }
}

impl std::error::Error for AuthorizationError {}
