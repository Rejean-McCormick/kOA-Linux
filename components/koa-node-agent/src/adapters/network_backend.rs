//! Adapter for profile-declared network-policy activation.
//!
//! Callers select a registered policy identifier.  The actual configuration
//! reference is resolved from immutable adapter configuration, never supplied as
//! a raw network rule by the request.

use std::collections::BTreeMap;

use crate::ports::{
    BackendError, BackendErrorCode, BackendOperationResult, NetworkBackend, NetworkPolicyRequest,
};

pub trait NetworkManager: Send + Sync {
    fn active_policy_ref(&self) -> Result<String, NetworkManagerError>;
    fn activate_policy_ref(&self, policy_ref: &str) -> Result<(), NetworkManagerError>;
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct NetworkManagerError {
    detail: String,
}

impl NetworkManagerError {
    pub fn new(detail: impl Into<String>) -> Self {
        Self {
            detail: detail.into(),
        }
    }
}

impl std::fmt::Display for NetworkManagerError {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        formatter.write_str(&self.detail)
    }
}

impl std::error::Error for NetworkManagerError {}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct NetworkPolicyBinding {
    policy_id: String,
    policy_ref: String,
}

impl NetworkPolicyBinding {
    pub fn new(
        policy_id: impl Into<String>,
        policy_ref: impl Into<String>,
    ) -> Result<Self, BackendError> {
        let policy_id = policy_id.into();
        let policy_ref = policy_ref.into();
        validate_identifier(&policy_id)?;
        validate_reference(&policy_ref)?;
        Ok(Self {
            policy_id,
            policy_ref,
        })
    }
}

pub struct NetworkBackendAdapter<M> {
    manager: M,
    policies: BTreeMap<String, String>,
}

impl<M> NetworkBackendAdapter<M> {
    pub fn new(
        manager: M,
        bindings: impl IntoIterator<Item = NetworkPolicyBinding>,
    ) -> Result<Self, BackendError> {
        let mut policies = BTreeMap::new();
        for binding in bindings {
            if policies
                .insert(binding.policy_id, binding.policy_ref)
                .is_some()
            {
                return Err(BackendError::invalid("duplicate network-policy binding"));
            }
        }
        if policies.is_empty() {
            return Err(BackendError::invalid(
                "network adapter requires at least one declared policy",
            ));
        }
        Ok(Self { manager, policies })
    }

    fn policy_ref(&self, request: &NetworkPolicyRequest) -> Result<&str, BackendError> {
        request.validate()?;
        self.policies
            .get(request.policy_id.as_str())
            .map(String::as_str)
            .ok_or_else(|| {
                BackendError::new(
                    BackendErrorCode::NotAllowlisted,
                    "network policy is not declared by the active profile",
                )
            })
    }

    fn state(&self) -> Result<BTreeMap<String, String>, BackendError>
    where
        M: NetworkManager,
    {
        let active = self.manager.active_policy_ref().map_err(manager_error)?;
        validate_reference(&active)?;
        Ok(BTreeMap::from([("active_policy_ref".to_owned(), active)]))
    }
}

impl<M: NetworkManager> NetworkBackend for NetworkBackendAdapter<M> {
    fn inspect_network_policy(
        &self,
        request: &NetworkPolicyRequest,
    ) -> Result<BackendOperationResult, BackendError> {
        self.policy_ref(request)?;
        let state = self.state()?;
        let result = BackendOperationResult {
            before_state: state.clone(),
            after_state: state,
            changed: false,
            reason_code: "NETWORK_POLICY_INSPECTED".to_owned(),
            recovery_token: None,
        };
        result.validate()?;
        Ok(result)
    }

    fn activate_network_policy(
        &self,
        request: &NetworkPolicyRequest,
    ) -> Result<BackendOperationResult, BackendError> {
        let policy_ref = self.policy_ref(request)?.to_owned();
        let before = self.state()?;
        let observed = before
            .get("active_policy_ref")
            .expect("state builder always records active_policy_ref");
        if observed != &request.expected_state_ref {
            return Err(BackendError::new(
                BackendErrorCode::Conflict,
                "active network policy differs from expected_state_ref",
            ));
        }
        self.manager
            .activate_policy_ref(&policy_ref)
            .map_err(manager_error)?;
        let after = self.state()?;
        if after.get("active_policy_ref") != Some(&policy_ref) {
            return Err(BackendError::new(
                BackendErrorCode::VerificationFailed,
                "network manager did not report the declared policy as active",
            ));
        }
        let result = BackendOperationResult {
            changed: before != after,
            before_state: before,
            after_state: after,
            reason_code: "NETWORK_POLICY_ACTIVATION_VERIFIED".to_owned(),
            recovery_token: None,
        };
        result.validate()?;
        Ok(result)
    }
}

fn validate_identifier(value: &str) -> Result<(), BackendError> {
    if value.is_empty()
        || value.len() > 128
        || !value
            .bytes()
            .all(|byte| byte.is_ascii_alphanumeric() || matches!(byte, b'-' | b'_' | b'.'))
    {
        return Err(BackendError::invalid("invalid network-policy identifier"));
    }
    Ok(())
}

fn validate_reference(value: &str) -> Result<(), BackendError> {
    if value.is_empty()
        || value.len() > 1024
        || value.trim() != value
        || value.chars().any(char::is_control)
    {
        return Err(BackendError::invalid(
            "network policy reference must be bounded and canonical",
        ));
    }
    Ok(())
}

fn manager_error(error: NetworkManagerError) -> BackendError {
    BackendError::new(BackendErrorCode::DependencyUnavailable, error.to_string())
}
