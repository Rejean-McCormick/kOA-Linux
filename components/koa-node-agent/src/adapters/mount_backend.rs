//! Adapter for profile-declared mount and unmount operations.

use std::collections::BTreeMap;
use std::fs;
use std::path::Path;

use crate::domain::EncryptedVolumeAction;
use crate::ports::{
    BackendError, BackendErrorCode, BackendOperationResult, DeclaredVolume, MountBackend,
    VolumeRequest,
};

pub trait MountManager: Send + Sync {
    fn mounted_source(&self, target: &Path) -> Result<Option<String>, MountManagerError>;
    fn mount(
        &self,
        source: &Path,
        target: &Path,
        filesystem_type: &str,
        read_only: bool,
    ) -> Result<(), MountManagerError>;
    fn unmount(&self, target: &Path) -> Result<(), MountManagerError>;
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct MountManagerError {
    detail: String,
}

impl MountManagerError {
    pub fn new(detail: impl Into<String>) -> Self {
        Self {
            detail: detail.into(),
        }
    }
}

impl std::fmt::Display for MountManagerError {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        formatter.write_str(&self.detail)
    }
}

impl std::error::Error for MountManagerError {}

pub struct MountBackendAdapter<M> {
    manager: M,
    volumes: BTreeMap<String, DeclaredVolume>,
}

impl<M> MountBackendAdapter<M> {
    pub fn new(
        manager: M,
        volumes: impl IntoIterator<Item = DeclaredVolume>,
    ) -> Result<Self, BackendError> {
        let mut declared = BTreeMap::new();
        for volume in volumes {
            let key = volume.volume_id.as_str().to_owned();
            if volume.source.root().path() == volume.target.root().path()
                && volume.source.relative() == volume.target.relative()
            {
                return Err(BackendError::invalid(
                    "declared volume source and target must be distinct",
                ));
            }
            if declared.insert(key, volume).is_some() {
                return Err(BackendError::invalid("duplicate declared volume"));
            }
        }
        if declared.is_empty() {
            return Err(BackendError::invalid(
                "mount adapter requires at least one declared volume",
            ));
        }
        Ok(Self {
            manager,
            volumes: declared,
        })
    }

    fn volume_for(&self, request: &VolumeRequest) -> Result<&DeclaredVolume, BackendError> {
        self.volumes.get(request.volume_id.as_str()).ok_or_else(|| {
            BackendError::new(
                BackendErrorCode::NotAllowlisted,
                "volume is not declared by the active profile",
            )
        })
    }
}

impl<M: MountManager> MountBackend for MountBackendAdapter<M> {
    fn inspect_volume(
        &self,
        request: &VolumeRequest,
    ) -> Result<BackendOperationResult, BackendError> {
        let volume = self.volume_for(request)?;
        verify_no_symlink_components(&volume.target.resolved())?;
        let state = mount_state(&self.manager, volume)?;
        let result = BackendOperationResult {
            before_state: state.clone(),
            after_state: state,
            changed: false,
            reason_code: "VOLUME_STATE_INSPECTED".to_owned(),
            recovery_token: None,
        };
        result.validate()?;
        Ok(result)
    }

    fn apply_volume_action(
        &self,
        request: &VolumeRequest,
    ) -> Result<BackendOperationResult, BackendError> {
        let volume = self.volume_for(request)?;
        verify_no_symlink_components(&volume.target.resolved())?;
        let before = mount_state(&self.manager, volume)?;
        match request.action {
            EncryptedVolumeAction::Mount => self
                .manager
                .mount(
                    &volume.source.resolved(),
                    &volume.target.resolved(),
                    volume.filesystem_type.as_str(),
                    volume.read_only,
                )
                .map_err(manager_error)?,
            EncryptedVolumeAction::Unmount => self
                .manager
                .unmount(&volume.target.resolved())
                .map_err(manager_error)?,
            _ => {
                return Err(BackendError::new(
                    BackendErrorCode::UnsupportedOperation,
                    "mount backend supports only mount and unmount actions",
                ))
            },
        }
        let after = mount_state(&self.manager, volume)?;
        let expected_mounted = request.action == EncryptedVolumeAction::Mount;
        let is_mounted = after.get("mounted").map(String::as_str) == Some("true");
        if expected_mounted != is_mounted {
            return Err(BackendError::new(
                BackendErrorCode::VerificationFailed,
                "mount state does not match the requested action",
            ));
        }
        let result = BackendOperationResult {
            changed: before != after,
            before_state: before,
            after_state: after,
            reason_code: if expected_mounted {
                "DECLARED_VOLUME_MOUNT_VERIFIED"
            } else {
                "DECLARED_VOLUME_UNMOUNT_VERIFIED"
            }
            .to_owned(),
            recovery_token: None,
        };
        result.validate()?;
        Ok(result)
    }
}

fn mount_state<M: MountManager>(
    manager: &M,
    volume: &DeclaredVolume,
) -> Result<BTreeMap<String, String>, BackendError> {
    let source = manager
        .mounted_source(&volume.target.resolved())
        .map_err(manager_error)?;
    let mut state = BTreeMap::new();
    state.insert("mounted".to_owned(), source.is_some().to_string());
    state.insert(
        "source".to_owned(),
        source.unwrap_or_else(|| "none".to_owned()),
    );
    state.insert(
        "target".to_owned(),
        volume.target.resolved().to_string_lossy().into_owned(),
    );
    Ok(state)
}

fn verify_no_symlink_components(path: &Path) -> Result<(), BackendError> {
    let mut current = std::path::PathBuf::new();
    for component in path.components() {
        current.push(component.as_os_str());
        match fs::symlink_metadata(&current) {
            Ok(metadata) if metadata.file_type().is_symlink() => {
                return Err(BackendError::new(
                    BackendErrorCode::UnsafePath,
                    format!("path component is a symlink: {}", current.display()),
                ));
            },
            Ok(_) => {},
            Err(error) if error.kind() == std::io::ErrorKind::NotFound => break,
            Err(error) => {
                return Err(BackendError::new(
                    BackendErrorCode::DependencyUnavailable,
                    format!("cannot inspect path component: {error}"),
                ));
            },
        }
    }
    Ok(())
}

fn manager_error(error: MountManagerError) -> BackendError {
    BackendError::new(BackendErrorCode::DependencyUnavailable, error.to_string())
}
