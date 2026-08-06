//! Execution gate for an already validated dispatch plan.
//!
//! The actual privileged backend is intentionally not defined here; it belongs
//! to the ports and adapters bundle. A caller supplies one fixed typed invoker,
//! and this function performs immediate deadline and authorization revalidation
//! before allowing it to run.

use core::fmt;

use crate::domain::{AuthorizationStatus, ExecuteResponse, Operation, OperationParameters};

use super::dispatch::{DispatchPlan, DispatchRoute};

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ExecutionDirective {
    route: DispatchRoute,
    operation: Operation,
    request_id: String,
    idempotency_id: String,
    correlation_id: String,
    profile_context_ref: String,
    target_refs: Vec<String>,
    expected_state_ref: Option<String>,
    parameters: OperationParameters,
    mutates_host: bool,
    receipt_required: bool,
}

impl ExecutionDirective {
    pub const fn route(&self) -> DispatchRoute {
        self.route
    }

    pub const fn operation(&self) -> Operation {
        self.operation
    }

    pub fn request_id(&self) -> &str {
        &self.request_id
    }

    pub fn idempotency_id(&self) -> &str {
        &self.idempotency_id
    }

    pub fn correlation_id(&self) -> &str {
        &self.correlation_id
    }

    pub fn profile_context_ref(&self) -> &str {
        &self.profile_context_ref
    }

    pub fn target_refs(&self) -> &[String] {
        &self.target_refs
    }

    pub fn expected_state_ref(&self) -> Option<&str> {
        self.expected_state_ref.as_deref()
    }

    pub fn parameters(&self) -> &OperationParameters {
        &self.parameters
    }

    pub const fn mutates_host(&self) -> bool {
        self.mutates_host
    }

    pub const fn receipt_required(&self) -> bool {
        self.receipt_required
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ExecutionSuccess<T> {
    value: T,
    response: ExecuteResponse,
    receipt_required: bool,
}

impl<T> ExecutionSuccess<T> {
    pub fn value(&self) -> &T {
        &self.value
    }

    pub fn into_value(self) -> T {
        self.value
    }

    pub const fn response(&self) -> ExecuteResponse {
        self.response
    }

    pub const fn receipt_required(&self) -> bool {
        self.receipt_required
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum ExecutionFailureCode {
    DeadlineExpired,
    AuthorizationNotApproved,
    AuthorizationNotYetValid,
    AuthorizationExpired,
    BackendRejected,
    BackendConflict,
    BackendFailed,
    RecoveryRequired,
}

impl ExecutionFailureCode {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::DeadlineExpired => "deadline_expired",
            Self::AuthorizationNotApproved => "authorization_not_approved",
            Self::AuthorizationNotYetValid => "authorization_not_yet_valid",
            Self::AuthorizationExpired => "authorization_expired",
            Self::BackendRejected => "backend_rejected",
            Self::BackendConflict => "backend_conflict",
            Self::BackendFailed => "backend_failed",
            Self::RecoveryRequired => "recovery_required",
        }
    }

    pub const fn response(self) -> ExecuteResponse {
        match self {
            Self::DeadlineExpired => ExecuteResponse::TimedOut,
            Self::AuthorizationNotApproved
            | Self::AuthorizationNotYetValid
            | Self::AuthorizationExpired
            | Self::BackendRejected => ExecuteResponse::Rejected,
            Self::BackendConflict => ExecuteResponse::Conflict,
            Self::BackendFailed => ExecuteResponse::Failed,
            Self::RecoveryRequired => ExecuteResponse::RecoveryRequired,
        }
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ExecutionFailure {
    code: ExecutionFailureCode,
    detail: String,
}

impl ExecutionFailure {
    pub fn new(code: ExecutionFailureCode, detail: impl Into<String>) -> Self {
        Self {
            code,
            detail: detail.into(),
        }
    }

    pub const fn code(&self) -> ExecutionFailureCode {
        self.code
    }

    pub fn detail(&self) -> &str {
        &self.detail
    }

    pub const fn response(&self) -> ExecuteResponse {
        self.code.response()
    }
}

impl fmt::Display for ExecutionFailure {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "{}: {}", self.code.as_str(), self.detail)
    }
}

impl std::error::Error for ExecutionFailure {}

pub fn execute_operation<T, F>(
    plan: &DispatchPlan,
    now: u64,
    invoke_fixed_adapter: F,
) -> Result<ExecutionSuccess<T>, ExecutionFailure>
where
    F: FnOnce(&ExecutionDirective) -> Result<T, ExecutionFailure>,
{
    let validated = plan.validated_request();
    let request = validated.request();
    let authorization = validated.authorization();

    if request.deadline().is_expired_at(now) {
        return Err(ExecutionFailure::new(
            ExecutionFailureCode::DeadlineExpired,
            "request expired before the privileged adapter was invoked",
        ));
    }
    if authorization.status() != AuthorizationStatus::Approved {
        return Err(ExecutionFailure::new(
            ExecutionFailureCode::AuthorizationNotApproved,
            "authorization is no longer approved",
        ));
    }
    if now < authorization.not_before() {
        return Err(ExecutionFailure::new(
            ExecutionFailureCode::AuthorizationNotYetValid,
            "authorization is not yet valid at execution time",
        ));
    }
    if now >= authorization.expires_at() {
        return Err(ExecutionFailure::new(
            ExecutionFailureCode::AuthorizationExpired,
            "authorization expired before authoritative execution",
        ));
    }

    let directive = ExecutionDirective {
        route: plan.route(),
        operation: request.operation(),
        request_id: request.request_id().as_str().to_owned(),
        idempotency_id: request.idempotency_id().as_str().to_owned(),
        correlation_id: request.correlation_id().as_str().to_owned(),
        profile_context_ref: request.profile_context_ref().as_str().to_owned(),
        target_refs: request
            .artifact_or_target_refs()
            .iter()
            .map(|target| target.as_str().to_owned())
            .collect(),
        expected_state_ref: request
            .expected_current_state()
            .map(|state| state.state_ref().as_str().to_owned()),
        parameters: request.parameters().clone(),
        mutates_host: request.operation().mutates_host(),
        receipt_required: validated.receipt_required(),
    };
    let value = invoke_fixed_adapter(&directive)?;
    Ok(ExecutionSuccess {
        value,
        response: ExecuteResponse::Completed,
        receipt_required: directive.receipt_required,
    })
}
