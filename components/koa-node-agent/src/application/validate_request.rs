//! Pure request validation before any privileged adapter is selected.

use core::fmt;
use std::collections::BTreeSet;

use crate::domain::{
    AllowedRoot, AuthorizationDecision, AuthorizationError, Identifier, NodeOperationRequest,
    Operation, OperationParameters, NODE_OPERATION_CONTRACT_VERSION,
};

#[derive(Clone, Debug)]
pub struct ValidationContext {
    now: u64,
    maximum_deadline_horizon_seconds: u64,
    enabled_operations: BTreeSet<Operation>,
    permitted_service_identities: BTreeSet<String>,
    allowed_path_roots: BTreeSet<AllowedRoot>,
    allowlisted_service_groups: BTreeSet<Identifier>,
    allowlisted_recovery_targets: BTreeSet<Identifier>,
    policy_required_operations: BTreeSet<Operation>,
    receipt_required_operations: BTreeSet<Operation>,
}

impl ValidationContext {
    pub fn new(now: u64, maximum_deadline_horizon_seconds: u64) -> Self {
        Self {
            now,
            maximum_deadline_horizon_seconds,
            enabled_operations: BTreeSet::new(),
            permitted_service_identities: BTreeSet::new(),
            allowed_path_roots: BTreeSet::new(),
            allowlisted_service_groups: BTreeSet::new(),
            allowlisted_recovery_targets: BTreeSet::new(),
            policy_required_operations: BTreeSet::new(),
            receipt_required_operations: BTreeSet::new(),
        }
    }

    pub fn enable_operation(&mut self, operation: Operation) {
        self.enabled_operations.insert(operation);
    }

    pub fn permit_service_identity(&mut self, identity: impl Into<String>) {
        self.permitted_service_identities.insert(identity.into());
    }

    pub fn allow_path_root(&mut self, root: AllowedRoot) {
        self.allowed_path_roots.insert(root);
    }

    pub fn allow_service_group(&mut self, service_group: Identifier) {
        self.allowlisted_service_groups.insert(service_group);
    }

    pub fn allow_recovery_target(&mut self, recovery_target: Identifier) {
        self.allowlisted_recovery_targets.insert(recovery_target);
    }

    pub fn require_policy_decision(&mut self, operation: Operation) {
        self.policy_required_operations.insert(operation);
    }

    pub fn require_receipt(&mut self, operation: Operation) {
        self.receipt_required_operations.insert(operation);
    }

    pub const fn now(&self) -> u64 {
        self.now
    }

    pub fn policy_decision_required(&self, operation: Operation) -> bool {
        operation != Operation::InspectNodeState
            || self.policy_required_operations.contains(&operation)
    }

    pub fn receipt_required(&self, operation: Operation) -> bool {
        self.receipt_required_operations.contains(&operation)
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ValidatedRequest {
    request: NodeOperationRequest,
    authorization: AuthorizationDecision,
    validated_at: u64,
    receipt_required: bool,
}

impl ValidatedRequest {
    pub fn request(&self) -> &NodeOperationRequest {
        &self.request
    }

    pub fn authorization(&self) -> &AuthorizationDecision {
        &self.authorization
    }

    pub const fn validated_at(&self) -> u64 {
        self.validated_at
    }

    pub const fn receipt_required(&self) -> bool {
        self.receipt_required
    }

    pub fn into_parts(self) -> (NodeOperationRequest, AuthorizationDecision) {
        (self.request, self.authorization)
    }
}

pub fn validate_request(
    request: NodeOperationRequest,
    authorization: AuthorizationDecision,
    context: &ValidationContext,
) -> Result<ValidatedRequest, RequestValidationError> {
    if request.contract_version() != NODE_OPERATION_CONTRACT_VERSION {
        return Err(RequestValidationError::new(
            RequestValidationErrorCode::UnsupportedContractVersion,
            format!(
                "expected {}, received {}",
                NODE_OPERATION_CONTRACT_VERSION,
                request.contract_version()
            ),
        ));
    }
    if !context.enabled_operations.contains(&request.operation()) {
        return Err(RequestValidationError::new(
            RequestValidationErrorCode::OperationDisabled,
            format!(
                "operation {} is not enabled by the active profile",
                request.operation()
            ),
        ));
    }
    if !context
        .permitted_service_identities
        .contains(request.service_identity().as_str())
    {
        return Err(RequestValidationError::new(
            RequestValidationErrorCode::ServiceIdentityNotPermitted,
            "the authenticated service identity is not permitted by this profile",
        ));
    }
    if request.deadline().is_expired_at(context.now) {
        return Err(RequestValidationError::new(
            RequestValidationErrorCode::DeadlineExpired,
            "the request deadline has expired",
        ));
    }
    let horizon = request.deadline().expires_at().saturating_sub(context.now);
    if horizon > context.maximum_deadline_horizon_seconds {
        return Err(RequestValidationError::new(
            RequestValidationErrorCode::DeadlineTooFar,
            "the request deadline exceeds the profile limit",
        ));
    }
    if request.operation() != request.parameters().operation() {
        return Err(RequestValidationError::new(
            RequestValidationErrorCode::ParameterOperationMismatch,
            "the parameter schema does not match the selected operation",
        ));
    }
    if request.operation().requires_target() && request.artifact_or_target_refs().is_empty() {
        return Err(RequestValidationError::new(
            RequestValidationErrorCode::TargetRequired,
            "this operation requires at least one explicit target reference",
        ));
    }
    if !request.operation().requires_target() && !request.artifact_or_target_refs().is_empty() {
        return Err(RequestValidationError::new(
            RequestValidationErrorCode::UnexpectedTarget,
            "this operation does not accept target references",
        ));
    }
    if request.operation().mutates_host() && request.expected_current_state().is_none() {
        return Err(RequestValidationError::new(
            RequestValidationErrorCode::ExpectedStateRequired,
            "mutating operations require an expected current state",
        ));
    }

    validate_operation_parameters(&request, context)?;

    authorization
        .validate_binding(
            &request,
            context.now,
            context.policy_decision_required(request.operation()),
        )
        .map_err(RequestValidationError::authorization)?;

    let receipt_required = request
        .parameters()
        .requires_receipt(context.receipt_required(request.operation()));

    Ok(ValidatedRequest {
        request,
        authorization,
        validated_at: context.now,
        receipt_required,
    })
}

fn validate_operation_parameters(
    request: &NodeOperationRequest,
    context: &ValidationContext,
) -> Result<(), RequestValidationError> {
    for path in request.parameters().safe_paths() {
        if !context.allowed_path_roots.contains(path.root()) {
            return Err(RequestValidationError::new(
                RequestValidationErrorCode::PathRootNotAllowlisted,
                format!("path root {} is not allowlisted", path.root().id()),
            ));
        }
    }

    match request.parameters() {
        OperationParameters::RestartAllowlistedServiceGroup { service_group, .. } => {
            if !context.allowlisted_service_groups.contains(service_group) {
                return Err(RequestValidationError::new(
                    RequestValidationErrorCode::ServiceGroupNotAllowlisted,
                    format!("service group {service_group} is not allowlisted"),
                ));
            }
        },
        OperationParameters::EnterRecoveryTarget { recovery_target } => {
            if !context
                .allowlisted_recovery_targets
                .contains(recovery_target)
            {
                return Err(RequestValidationError::new(
                    RequestValidationErrorCode::RecoveryTargetNotAllowlisted,
                    format!("recovery target {recovery_target} is not allowlisted"),
                ));
            }
        },
        _ => {},
    }
    Ok(())
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum RequestValidationErrorCode {
    UnsupportedContractVersion,
    OperationDisabled,
    ServiceIdentityNotPermitted,
    DeadlineExpired,
    DeadlineTooFar,
    ParameterOperationMismatch,
    TargetRequired,
    UnexpectedTarget,
    ExpectedStateRequired,
    PathRootNotAllowlisted,
    ServiceGroupNotAllowlisted,
    RecoveryTargetNotAllowlisted,
    AuthorizationDenied,
    AuthorizationRevoked,
    AuthorizationNotYetValid,
    AuthorizationExpired,
    AuthorizationOperationMismatch,
    AuthorizationClassMismatch,
    AuthorizationCallerMismatch,
    AuthorizationServiceMismatch,
    AuthorizationProfileMismatch,
    AuthorizationTargetScopeMismatch,
    AuthorizationExpectedStateMismatch,
    AuthorizationDecisionReferenceRequired,
    AuthorizationDecisionReferenceMismatch,
}

impl RequestValidationErrorCode {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::UnsupportedContractVersion => "unsupported_contract_version",
            Self::OperationDisabled => "operation_disabled",
            Self::ServiceIdentityNotPermitted => "service_identity_not_permitted",
            Self::DeadlineExpired => "deadline_expired",
            Self::DeadlineTooFar => "deadline_too_far",
            Self::ParameterOperationMismatch => "parameter_operation_mismatch",
            Self::TargetRequired => "target_required",
            Self::UnexpectedTarget => "unexpected_target",
            Self::ExpectedStateRequired => "expected_state_required",
            Self::PathRootNotAllowlisted => "path_root_not_allowlisted",
            Self::ServiceGroupNotAllowlisted => "service_group_not_allowlisted",
            Self::RecoveryTargetNotAllowlisted => "recovery_target_not_allowlisted",
            Self::AuthorizationDenied => "authorization_denied",
            Self::AuthorizationRevoked => "authorization_revoked",
            Self::AuthorizationNotYetValid => "authorization_not_yet_valid",
            Self::AuthorizationExpired => "authorization_expired",
            Self::AuthorizationOperationMismatch => "authorization_operation_mismatch",
            Self::AuthorizationClassMismatch => "authorization_class_mismatch",
            Self::AuthorizationCallerMismatch => "authorization_caller_mismatch",
            Self::AuthorizationServiceMismatch => "authorization_service_mismatch",
            Self::AuthorizationProfileMismatch => "authorization_profile_mismatch",
            Self::AuthorizationTargetScopeMismatch => "authorization_target_scope_mismatch",
            Self::AuthorizationExpectedStateMismatch => "authorization_expected_state_mismatch",
            Self::AuthorizationDecisionReferenceRequired => {
                "authorization_decision_reference_required"
            },
            Self::AuthorizationDecisionReferenceMismatch => {
                "authorization_decision_reference_mismatch"
            },
        }
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct RequestValidationError {
    code: RequestValidationErrorCode,
    detail: String,
}

impl RequestValidationError {
    fn new(code: RequestValidationErrorCode, detail: impl Into<String>) -> Self {
        Self {
            code,
            detail: detail.into(),
        }
    }

    fn authorization(error: AuthorizationError) -> Self {
        let code = match error {
            AuthorizationError::Denied => RequestValidationErrorCode::AuthorizationDenied,
            AuthorizationError::Revoked => RequestValidationErrorCode::AuthorizationRevoked,
            AuthorizationError::NotYetValid => RequestValidationErrorCode::AuthorizationNotYetValid,
            AuthorizationError::Expired => RequestValidationErrorCode::AuthorizationExpired,
            AuthorizationError::OperationMismatch => {
                RequestValidationErrorCode::AuthorizationOperationMismatch
            },
            AuthorizationError::ClassMismatch => {
                RequestValidationErrorCode::AuthorizationClassMismatch
            },
            AuthorizationError::CallerMismatch => {
                RequestValidationErrorCode::AuthorizationCallerMismatch
            },
            AuthorizationError::ServiceMismatch => {
                RequestValidationErrorCode::AuthorizationServiceMismatch
            },
            AuthorizationError::ProfileMismatch => {
                RequestValidationErrorCode::AuthorizationProfileMismatch
            },
            AuthorizationError::TargetScopeMismatch => {
                RequestValidationErrorCode::AuthorizationTargetScopeMismatch
            },
            AuthorizationError::ExpectedStateMismatch => {
                RequestValidationErrorCode::AuthorizationExpectedStateMismatch
            },
            AuthorizationError::DecisionReferenceRequired => {
                RequestValidationErrorCode::AuthorizationDecisionReferenceRequired
            },
            AuthorizationError::DecisionReferenceMismatch => {
                RequestValidationErrorCode::AuthorizationDecisionReferenceMismatch
            },
        };
        Self::new(code, error.code())
    }

    pub const fn code(&self) -> RequestValidationErrorCode {
        self.code
    }

    pub fn detail(&self) -> &str {
        &self.detail
    }
}

impl fmt::Display for RequestValidationError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "{}: {}", self.code.as_str(), self.detail)
    }
}

impl std::error::Error for RequestValidationError {}
