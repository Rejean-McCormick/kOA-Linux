//! Allowlisted systemd service-group adapter.
//!
//! The adapter delegates to a typed manager API and never accepts a
//! caller-supplied unit name. The concrete systemctl manager invokes only the
//! fixed systemctl executable with a bounded argument vector and never a shell.

use std::collections::{BTreeMap, BTreeSet};
use std::process::Command;

use crate::ports::{
    BackendError, BackendErrorCode, BackendOperationResult, ServiceGroupRequest, SystemdBackend,
};

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum UnitState {
    Active,
    Inactive,
    Failed,
    Activating,
    Deactivating,
    Unknown,
}

impl UnitState {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::Active => "active",
            Self::Inactive => "inactive",
            Self::Failed => "failed",
            Self::Activating => "activating",
            Self::Deactivating => "deactivating",
            Self::Unknown => "unknown",
        }
    }
}

pub trait SystemdManager: Send + Sync {
    fn unit_state(&self, unit: &str) -> Result<UnitState, SystemdManagerError>;
    fn restart_unit(&self, unit: &str) -> Result<(), SystemdManagerError>;
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct SystemdManagerError {
    detail: String,
}

impl SystemdManagerError {
    pub fn new(detail: impl Into<String>) -> Self {
        Self {
            detail: detail.into(),
        }
    }
}

impl std::fmt::Display for SystemdManagerError {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        formatter.write_str(&self.detail)
    }
}

impl std::error::Error for SystemdManagerError {}

const SYSTEMCTL: &str = "/usr/bin/systemctl";

/// Concrete systemd manager using only a fixed systemctl executable.
///
/// Unit names are validated before invocation. Commands are passed as a
/// bounded argument vector; no shell interpreter is involved.
#[derive(Clone, Copy, Debug, Default)]
pub struct SystemctlManager;

impl SystemdManager for SystemctlManager {
    fn unit_state(&self, unit: &str) -> Result<UnitState, SystemdManagerError> {
        validate_unit_name(unit).map_err(|error| SystemdManagerError::new(error.to_string()))?;

        let output = Command::new(SYSTEMCTL)
            .args(["show", "--property=ActiveState", "--value", "--", unit])
            .output()
            .map_err(|error| {
                SystemdManagerError::new(format!(
                    "cannot execute fixed systemctl state query: {error}"
                ))
            })?;

        if !output.status.success() {
            return Err(SystemdManagerError::new(format!(
                "systemctl state query failed with status {}",
                output.status
            )));
        }

        let state = String::from_utf8(output.stdout).map_err(|_| {
            SystemdManagerError::new("systemctl ActiveState output is not valid UTF-8")
        })?;

        Ok(match state.trim() {
            "active" => UnitState::Active,
            "inactive" => UnitState::Inactive,
            "failed" => UnitState::Failed,
            "activating" => UnitState::Activating,
            "deactivating" => UnitState::Deactivating,
            _ => UnitState::Unknown,
        })
    }

    fn restart_unit(&self, unit: &str) -> Result<(), SystemdManagerError> {
        validate_unit_name(unit).map_err(|error| SystemdManagerError::new(error.to_string()))?;

        let status = Command::new(SYSTEMCTL)
            .args(["restart", "--", unit])
            .status()
            .map_err(|error| {
                SystemdManagerError::new(format!("cannot execute fixed systemctl restart: {error}"))
            })?;

        if !status.success() {
            return Err(SystemdManagerError::new(format!(
                "systemctl restart failed with status {status}"
            )));
        }

        Ok(())
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ServiceGroupBinding {
    group_id: String,
    units: Vec<String>,
}

impl ServiceGroupBinding {
    pub fn new(
        group_id: impl Into<String>,
        units: impl IntoIterator<Item = String>,
    ) -> Result<Self, BackendError> {
        let group_id = group_id.into();
        validate_group_id(&group_id)?;
        let mut units: Vec<String> = units.into_iter().collect();
        if units.is_empty() || units.len() > 64 {
            return Err(BackendError::invalid(
                "a service group must contain 1 through 64 units",
            ));
        }
        for unit in &units {
            validate_unit_name(unit)?;
        }
        units.sort();
        if units.windows(2).any(|pair| pair[0] == pair[1]) {
            return Err(BackendError::invalid(
                "a service group cannot contain duplicate units",
            ));
        }
        Ok(Self { group_id, units })
    }
}

pub struct SystemdBackendAdapter<M> {
    manager: M,
    groups: BTreeMap<String, Vec<String>>,
}

impl<M> SystemdBackendAdapter<M> {
    pub fn new(
        manager: M,
        bindings: impl IntoIterator<Item = ServiceGroupBinding>,
    ) -> Result<Self, BackendError> {
        let mut groups = BTreeMap::new();
        for binding in bindings {
            if groups
                .insert(binding.group_id.clone(), binding.units)
                .is_some()
            {
                return Err(BackendError::invalid("duplicate service-group binding"));
            }
        }
        if groups.is_empty() {
            return Err(BackendError::invalid(
                "systemd adapter requires at least one declared service group",
            ));
        }
        Ok(Self { manager, groups })
    }

    fn units_for(&self, request: &ServiceGroupRequest) -> Result<&[String], BackendError> {
        self.groups
            .get(request.service_group.as_str())
            .map(Vec::as_slice)
            .ok_or_else(|| {
                BackendError::new(
                    BackendErrorCode::NotAllowlisted,
                    "service group is not declared by the active profile",
                )
            })
    }

    fn read_states(&self, units: &[String]) -> Result<BTreeMap<String, String>, BackendError>
    where
        M: SystemdManager,
    {
        let mut states = BTreeMap::new();
        for unit in units {
            let state = self.manager.unit_state(unit).map_err(manager_unavailable)?;
            states.insert(unit.clone(), state.as_str().to_owned());
        }
        Ok(states)
    }
}

impl<M: SystemdManager> SystemdBackend for SystemdBackendAdapter<M> {
    fn inspect_service_group(
        &self,
        request: &ServiceGroupRequest,
    ) -> Result<BackendOperationResult, BackendError> {
        let units = self.units_for(request)?;
        let state = self.read_states(units)?;
        let result = BackendOperationResult {
            before_state: state.clone(),
            after_state: state,
            changed: false,
            reason_code: "SERVICE_GROUP_INSPECTED".to_owned(),
            recovery_token: None,
        };
        result.validate()?;
        Ok(result)
    }

    fn restart_service_group(
        &self,
        request: &ServiceGroupRequest,
    ) -> Result<BackendOperationResult, BackendError> {
        let units = self.units_for(request)?;
        let before = self.read_states(units)?;
        let mut restarted = BTreeSet::new();
        for unit in units {
            self.manager.restart_unit(unit).map_err(|error| {
                BackendError::new(
                    BackendErrorCode::IndeterminateOutcome,
                    format!(
                        "service-group restart stopped after {:?}: {error}",
                        restarted
                    ),
                )
            })?;
            restarted.insert(unit.clone());
        }
        let after = self.read_states(units)?;
        if after
            .values()
            .any(|state| state != UnitState::Active.as_str())
        {
            return Err(BackendError::new(
                BackendErrorCode::VerificationFailed,
                "one or more allowlisted units are not active after restart",
            ));
        }
        let result = BackendOperationResult {
            changed: before != after,
            before_state: before,
            after_state: after,
            reason_code: "SERVICE_GROUP_RESTART_VERIFIED".to_owned(),
            recovery_token: None,
        };
        result.validate()?;
        Ok(result)
    }
}

fn validate_group_id(value: &str) -> Result<(), BackendError> {
    if value.is_empty()
        || value.len() > 128
        || !value
            .bytes()
            .all(|byte| byte.is_ascii_alphanumeric() || matches!(byte, b'-' | b'_' | b'.'))
    {
        return Err(BackendError::invalid("invalid service-group identifier"));
    }
    Ok(())
}

fn validate_unit_name(value: &str) -> Result<(), BackendError> {
    if value.is_empty()
        || value.len() > 256
        || !value.bytes().all(|byte| {
            byte.is_ascii_alphanumeric() || matches!(byte, b'-' | b'_' | b'.' | b'@' | b':')
        })
        || !value.ends_with(".service")
    {
        return Err(BackendError::invalid(
            "systemd unit must be a bounded literal .service name",
        ));
    }
    Ok(())
}

fn manager_unavailable(error: SystemdManagerError) -> BackendError {
    BackendError::new(BackendErrorCode::DependencyUnavailable, error.to_string())
}
