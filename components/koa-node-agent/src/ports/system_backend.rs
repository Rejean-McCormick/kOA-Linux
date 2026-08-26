//! Typed host-backend ports for profile-declared system effects.
//!
//! These ports expose no executable string, shell command, arbitrary unit name,
//! raw mount option, network rule, or unrestricted host path.

use core::fmt;
use std::collections::BTreeMap;

use crate::domain::{EncryptedVolumeAction, SafePath};

#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct BackendIdentifier(String);

impl BackendIdentifier {
    pub fn new(value: impl Into<String>) -> Result<Self, BackendError> {
        let value = value.into();
        if value.is_empty() || value.len() > 128 {
            return Err(BackendError::invalid(
                "backend identifier must contain 1 through 128 bytes",
            ));
        }
        if !value
            .bytes()
            .all(|byte| byte.is_ascii_alphanumeric() || matches!(byte, b'-' | b'_' | b'.'))
        {
            return Err(BackendError::invalid(
                "backend identifier contains a character outside the closed alphabet",
            ));
        }
        Ok(Self(value))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

impl fmt::Display for BackendIdentifier {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(&self.0)
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ServiceGroupRequest {
    pub service_group: BackendIdentifier,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct VolumeRequest {
    pub volume_id: BackendIdentifier,
    pub action: EncryptedVolumeAction,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct NetworkPolicyRequest {
    pub policy_id: BackendIdentifier,
    pub expected_state_ref: String,
}

impl NetworkPolicyRequest {
    pub fn validate(&self) -> Result<(), BackendError> {
        if self.expected_state_ref.is_empty()
            || self.expected_state_ref.len() > 1024
            || self.expected_state_ref.trim() != self.expected_state_ref
            || self.expected_state_ref.chars().any(char::is_control)
        {
            return Err(BackendError::invalid(
                "expected_state_ref must be a bounded canonical reference",
            ));
        }
        Ok(())
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct DeclaredVolume {
    pub volume_id: BackendIdentifier,
    pub source: SafePath,
    pub target: SafePath,
    pub filesystem_type: BackendIdentifier,
    pub read_only: bool,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct BackendOperationResult {
    pub before_state: BTreeMap<String, String>,
    pub after_state: BTreeMap<String, String>,
    pub changed: bool,
    pub reason_code: String,
    pub recovery_token: Option<String>,
}

impl BackendOperationResult {
    pub fn validate(&self) -> Result<(), BackendError> {
        validate_reason_code(&self.reason_code)?;
        validate_state_map("before_state", &self.before_state)?;
        validate_state_map("after_state", &self.after_state)?;
        if self.changed && self.before_state == self.after_state {
            return Err(BackendError::invalid(
                "changed backend result must expose different before and after state",
            ));
        }
        if !self.changed && self.before_state != self.after_state {
            return Err(BackendError::invalid(
                "unchanged backend result cannot expose different states",
            ));
        }
        if let Some(token) = &self.recovery_token {
            if token.is_empty() || token.len() > 256 || token.chars().any(char::is_whitespace) {
                return Err(BackendError::invalid(
                    "recovery token must be a bounded token without whitespace",
                ));
            }
        }
        Ok(())
    }
}

pub trait SystemdBackend: Send + Sync {
    fn inspect_service_group(
        &self,
        request: &ServiceGroupRequest,
    ) -> Result<BackendOperationResult, BackendError>;

    fn restart_service_group(
        &self,
        request: &ServiceGroupRequest,
    ) -> Result<BackendOperationResult, BackendError>;
}

pub trait MountBackend: Send + Sync {
    fn inspect_volume(
        &self,
        request: &VolumeRequest,
    ) -> Result<BackendOperationResult, BackendError>;

    fn apply_volume_action(
        &self,
        request: &VolumeRequest,
    ) -> Result<BackendOperationResult, BackendError>;
}

pub trait NetworkBackend: Send + Sync {
    fn inspect_network_policy(
        &self,
        request: &NetworkPolicyRequest,
    ) -> Result<BackendOperationResult, BackendError>;

    fn activate_network_policy(
        &self,
        request: &NetworkPolicyRequest,
    ) -> Result<BackendOperationResult, BackendError>;
}

pub trait SystemBackend: SystemdBackend + MountBackend + NetworkBackend {}
impl<T> SystemBackend for T where T: SystemdBackend + MountBackend + NetworkBackend {}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum BackendErrorCode {
    InvalidRequest,
    NotAllowlisted,
    UnsupportedOperation,
    DependencyUnavailable,
    Conflict,
    VerificationFailed,
    IndeterminateOutcome,
    UnsafePath,
}

impl BackendErrorCode {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::InvalidRequest => "invalid_request",
            Self::NotAllowlisted => "not_allowlisted",
            Self::UnsupportedOperation => "unsupported_operation",
            Self::DependencyUnavailable => "dependency_unavailable",
            Self::Conflict => "conflict",
            Self::VerificationFailed => "verification_failed",
            Self::IndeterminateOutcome => "indeterminate_outcome",
            Self::UnsafePath => "unsafe_path",
        }
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct BackendError {
    code: BackendErrorCode,
    detail: String,
}

impl BackendError {
    pub fn new(code: BackendErrorCode, detail: impl Into<String>) -> Self {
        Self {
            code,
            detail: detail.into(),
        }
    }

    pub fn invalid(detail: impl Into<String>) -> Self {
        Self::new(BackendErrorCode::InvalidRequest, detail)
    }

    pub const fn code(&self) -> BackendErrorCode {
        self.code
    }

    pub fn detail(&self) -> &str {
        &self.detail
    }
}

impl fmt::Display for BackendError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "{}: {}", self.code.as_str(), self.detail)
    }
}

impl std::error::Error for BackendError {}

fn validate_reason_code(value: &str) -> Result<(), BackendError> {
    if value.is_empty()
        || value.len() > 128
        || !value
            .bytes()
            .all(|byte| byte.is_ascii_uppercase() || byte.is_ascii_digit() || byte == b'_')
    {
        return Err(BackendError::invalid(
            "reason_code must use the closed upper-snake-case alphabet",
        ));
    }
    Ok(())
}

fn validate_state_map(name: &str, values: &BTreeMap<String, String>) -> Result<(), BackendError> {
    if values.len() > 64 {
        return Err(BackendError::invalid(format!(
            "{name} exceeds the bounded state-entry limit"
        )));
    }
    for (key, value) in values {
        if key.is_empty()
            || key.len() > 128
            || value.is_empty()
            || value.len() > 1024
            || key.chars().any(char::is_control)
            || value.chars().any(char::is_control)
        {
            return Err(BackendError::invalid(format!(
                "{name} contains an invalid key or value"
            )));
        }
    }
    Ok(())
}
