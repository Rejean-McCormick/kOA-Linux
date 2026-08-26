//! Canonical, typed node-operation requests.

use core::fmt;
use std::collections::BTreeSet;

use super::command::{Operation, NODE_OPERATION_CONTRACT_VERSION};
use super::safe_path::SafePath;

const MAX_IDENTIFIER_BYTES: usize = 256;
const MAX_REFERENCE_BYTES: usize = 1024;
const MAX_TARGET_REFERENCES: usize = 32;

#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct Identifier(String);

impl Identifier {
    pub fn new(value: impl Into<String>) -> Result<Self, RequestBuildError> {
        let value = value.into();
        validate_bounded_value(&value, MAX_IDENTIFIER_BYTES, "identifier")?;
        if value.chars().any(char::is_whitespace) {
            return Err(RequestBuildError::new(
                RequestBuildErrorCode::InvalidIdentifier,
                "identifiers may not contain whitespace",
            ));
        }
        Ok(Self(value))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

impl fmt::Display for Identifier {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(&self.0)
    }
}

#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct CanonicalReference(String);

impl CanonicalReference {
    pub fn new(value: impl Into<String>) -> Result<Self, RequestBuildError> {
        let value = value.into();
        validate_bounded_value(&value, MAX_REFERENCE_BYTES, "reference")?;
        Ok(Self(value))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

impl fmt::Display for CanonicalReference {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(&self.0)
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ExpectedState {
    state_ref: CanonicalReference,
    version: Option<Identifier>,
}

impl ExpectedState {
    pub fn new(state_ref: CanonicalReference, version: Option<Identifier>) -> Self {
        Self { state_ref, version }
    }

    pub fn state_ref(&self) -> &CanonicalReference {
        &self.state_ref
    }

    pub fn version(&self) -> Option<&Identifier> {
        self.version.as_ref()
    }

    fn canonical(&self) -> String {
        match &self.version {
            Some(version) => format!("{}@{}", self.state_ref, version),
            None => self.state_ref.to_string(),
        }
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct RequestDeadline {
    submitted_at: u64,
    expires_at: u64,
}

impl RequestDeadline {
    pub fn new(submitted_at: u64, expires_at: u64) -> Result<Self, RequestBuildError> {
        if expires_at <= submitted_at {
            return Err(RequestBuildError::new(
                RequestBuildErrorCode::InvalidDeadline,
                "request expiry must be later than submission time",
            ));
        }
        Ok(Self {
            submitted_at,
            expires_at,
        })
    }

    pub const fn submitted_at(self) -> u64 {
        self.submitted_at
    }

    pub const fn expires_at(self) -> u64 {
        self.expires_at
    }

    pub const fn is_expired_at(self, now: u64) -> bool {
        now >= self.expires_at
    }
}

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub enum KnowledgeArtifactAction {
    Install,
    Activate,
    Pin,
    Unpin,
    Quarantine,
    Revert,
}

impl KnowledgeArtifactAction {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::Install => "install",
            Self::Activate => "activate",
            Self::Pin => "pin",
            Self::Unpin => "unpin",
            Self::Quarantine => "quarantine",
            Self::Revert => "revert",
        }
    }

    pub const fn requires_receipt(self) -> bool {
        matches!(self, Self::Activate | Self::Quarantine | Self::Revert)
    }
}

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub enum OfflineImportTarget {
    Quarantine,
    Staging,
}

impl OfflineImportTarget {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::Quarantine => "quarantine",
            Self::Staging => "staging",
        }
    }
}

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub enum EncryptedVolumeAction {
    Create,
    Unlock,
    Mount,
    Unmount,
    Rotate,
    Retire,
}

impl EncryptedVolumeAction {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::Create => "create",
            Self::Unlock => "unlock",
            Self::Mount => "mount",
            Self::Unmount => "unmount",
            Self::Rotate => "rotate",
            Self::Retire => "retire",
        }
    }
}

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub enum RecoveryStrategy {
    Rollback,
    Revert,
    Restore,
    ForwardRepair,
    ReconstructionFromVerifiedArtifacts,
}

impl RecoveryStrategy {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::Rollback => "rollback",
            Self::Revert => "revert",
            Self::Restore => "restore",
            Self::ForwardRepair => "forward_repair",
            Self::ReconstructionFromVerifiedArtifacts => "reconstruction_from_verified_artifacts",
        }
    }
}

/// Closed parameter schemas. Unknown fields cannot enter this representation.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum OperationParameters {
    InspectNodeState,
    StageSystemArtifact {
        staging_path: SafePath,
    },
    ActivateSystemArtifact,
    ActivateServiceBundle,
    ActivateGovernanceBundle,
    ManageKnowledgeArtifact {
        action: KnowledgeArtifactAction,
    },
    ImportOfflineBundle {
        destination: SafePath,
        target_state: OfflineImportTarget,
    },
    ManageDeclaredEncryptedVolume {
        action: EncryptedVolumeAction,
        mount_path: Option<SafePath>,
    },
    RestartAllowlistedServiceGroup {
        service_group: Identifier,
        critical: bool,
    },
    RotateNodeScopedKey {
        expected_key_version: Identifier,
    },
    ExportNodeEvidence {
        evidence_scope_ref: CanonicalReference,
        destination: SafePath,
    },
    EnterRecoveryTarget {
        recovery_target: Identifier,
    },
    ExecuteRollbackOrForwardRepair {
        failed_request_id: Identifier,
        recovery_plan_ref: CanonicalReference,
        strategy: RecoveryStrategy,
    },
}

impl OperationParameters {
    pub const fn operation(&self) -> Operation {
        match self {
            Self::InspectNodeState => Operation::InspectNodeState,
            Self::StageSystemArtifact { .. } => Operation::StageSystemArtifact,
            Self::ActivateSystemArtifact => Operation::ActivateSystemArtifact,
            Self::ActivateServiceBundle => Operation::ActivateServiceBundle,
            Self::ActivateGovernanceBundle => Operation::ActivateGovernanceBundle,
            Self::ManageKnowledgeArtifact { .. } => Operation::ManageKnowledgeArtifact,
            Self::ImportOfflineBundle { .. } => Operation::ImportOfflineBundle,
            Self::ManageDeclaredEncryptedVolume { .. } => Operation::ManageDeclaredEncryptedVolume,
            Self::RestartAllowlistedServiceGroup { .. } => {
                Operation::RestartAllowlistedServiceGroup
            },
            Self::RotateNodeScopedKey { .. } => Operation::RotateNodeScopedKey,
            Self::ExportNodeEvidence { .. } => Operation::ExportNodeEvidence,
            Self::EnterRecoveryTarget { .. } => Operation::EnterRecoveryTarget,
            Self::ExecuteRollbackOrForwardRepair { .. } => {
                Operation::ExecuteRollbackOrForwardRepair
            },
        }
    }

    pub fn safe_paths(&self) -> Vec<&SafePath> {
        match self {
            Self::StageSystemArtifact { staging_path } => vec![staging_path],
            Self::ImportOfflineBundle { destination, .. }
            | Self::ExportNodeEvidence { destination, .. } => vec![destination],
            Self::ManageDeclaredEncryptedVolume {
                mount_path: Some(path),
                ..
            } => vec![path],
            _ => Vec::new(),
        }
    }

    pub const fn requires_receipt(&self, policy_requires_receipt: bool) -> bool {
        match self {
            Self::InspectNodeState => policy_requires_receipt,
            Self::ManageKnowledgeArtifact { action } => action.requires_receipt(),
            Self::RestartAllowlistedServiceGroup { critical, .. } => *critical,
            _ => true,
        }
    }

    fn canonical(&self) -> String {
        match self {
            Self::InspectNodeState => "inspect_node_state".to_owned(),
            Self::StageSystemArtifact { staging_path } => {
                format!("stage_system_artifact|{}", staging_path.canonical())
            },
            Self::ActivateSystemArtifact => "activate_system_artifact".to_owned(),
            Self::ActivateServiceBundle => "activate_service_bundle".to_owned(),
            Self::ActivateGovernanceBundle => "activate_governance_bundle".to_owned(),
            Self::ManageKnowledgeArtifact { action } => {
                format!("manage_knowledge_artifact|{}", action.as_str())
            },
            Self::ImportOfflineBundle {
                destination,
                target_state,
            } => format!(
                "import_offline_bundle|{}|{}",
                target_state.as_str(),
                destination.canonical()
            ),
            Self::ManageDeclaredEncryptedVolume { action, mount_path } => format!(
                "manage_declared_encrypted_volume|{}|{}",
                action.as_str(),
                mount_path
                    .as_ref()
                    .map(SafePath::canonical)
                    .unwrap_or_else(|| "none".to_owned())
            ),
            Self::RestartAllowlistedServiceGroup {
                service_group,
                critical,
            } => format!(
                "restart_allowlisted_service_group|{}|{}",
                service_group, critical
            ),
            Self::RotateNodeScopedKey {
                expected_key_version,
            } => format!("rotate_node_scoped_key|{expected_key_version}"),
            Self::ExportNodeEvidence {
                evidence_scope_ref,
                destination,
            } => format!(
                "export_node_evidence|{}|{}",
                evidence_scope_ref,
                destination.canonical()
            ),
            Self::EnterRecoveryTarget { recovery_target } => {
                format!("enter_recovery_target|{recovery_target}")
            },
            Self::ExecuteRollbackOrForwardRepair {
                failed_request_id,
                recovery_plan_ref,
                strategy,
            } => format!(
                "execute_rollback_or_forward_repair|{}|{}|{}",
                failed_request_id,
                recovery_plan_ref,
                strategy.as_str()
            ),
        }
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct NodeOperationRequestParts {
    pub contract_version: String,
    pub operation: Operation,
    pub request_id: Identifier,
    pub idempotency_id: Identifier,
    pub caller_identity: CanonicalReference,
    pub service_identity: CanonicalReference,
    pub profile_context_ref: CanonicalReference,
    pub policy_decision_ref: Option<CanonicalReference>,
    pub artifact_or_target_refs: Vec<CanonicalReference>,
    pub expected_current_state: Option<ExpectedState>,
    pub parameters: OperationParameters,
    pub deadline: RequestDeadline,
    pub correlation_id: Identifier,
}

impl NodeOperationRequestParts {
    pub fn version_1(
        operation: Operation,
        request_id: Identifier,
        idempotency_id: Identifier,
        caller_identity: CanonicalReference,
        service_identity: CanonicalReference,
        profile_context_ref: CanonicalReference,
        policy_decision_ref: Option<CanonicalReference>,
        artifact_or_target_refs: Vec<CanonicalReference>,
        expected_current_state: Option<ExpectedState>,
        parameters: OperationParameters,
        deadline: RequestDeadline,
        correlation_id: Identifier,
    ) -> Self {
        Self {
            contract_version: NODE_OPERATION_CONTRACT_VERSION.to_owned(),
            operation,
            request_id,
            idempotency_id,
            caller_identity,
            service_identity,
            profile_context_ref,
            policy_decision_ref,
            artifact_or_target_refs,
            expected_current_state,
            parameters,
            deadline,
            correlation_id,
        }
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct NodeOperationRequest {
    contract_version: String,
    operation: Operation,
    request_id: Identifier,
    idempotency_id: Identifier,
    caller_identity: CanonicalReference,
    service_identity: CanonicalReference,
    profile_context_ref: CanonicalReference,
    policy_decision_ref: Option<CanonicalReference>,
    artifact_or_target_refs: BTreeSet<CanonicalReference>,
    expected_current_state: Option<ExpectedState>,
    parameters: OperationParameters,
    deadline: RequestDeadline,
    correlation_id: Identifier,
}

impl NodeOperationRequest {
    pub fn new(parts: NodeOperationRequestParts) -> Result<Self, RequestBuildError> {
        validate_bounded_value(
            &parts.contract_version,
            32,
            "node operation contract version",
        )?;
        if parts.operation != parts.parameters.operation() {
            return Err(RequestBuildError::new(
                RequestBuildErrorCode::ParameterOperationMismatch,
                format!(
                    "operation {} cannot use parameter schema for {}",
                    parts.operation,
                    parts.parameters.operation()
                ),
            ));
        }
        validate_volume_parameters(&parts.parameters)?;

        let original_target_count = parts.artifact_or_target_refs.len();
        if original_target_count > MAX_TARGET_REFERENCES {
            return Err(RequestBuildError::new(
                RequestBuildErrorCode::TooManyTargets,
                format!("a request may contain at most {MAX_TARGET_REFERENCES} target references"),
            ));
        }
        let artifact_or_target_refs: BTreeSet<_> =
            parts.artifact_or_target_refs.into_iter().collect();
        if artifact_or_target_refs.len() != original_target_count {
            return Err(RequestBuildError::new(
                RequestBuildErrorCode::DuplicateTarget,
                "target references must be unique",
            ));
        }

        Ok(Self {
            contract_version: parts.contract_version,
            operation: parts.operation,
            request_id: parts.request_id,
            idempotency_id: parts.idempotency_id,
            caller_identity: parts.caller_identity,
            service_identity: parts.service_identity,
            profile_context_ref: parts.profile_context_ref,
            policy_decision_ref: parts.policy_decision_ref,
            artifact_or_target_refs,
            expected_current_state: parts.expected_current_state,
            parameters: parts.parameters,
            deadline: parts.deadline,
            correlation_id: parts.correlation_id,
        })
    }

    pub fn contract_version(&self) -> &str {
        &self.contract_version
    }

    pub const fn operation(&self) -> Operation {
        self.operation
    }

    pub fn request_id(&self) -> &Identifier {
        &self.request_id
    }

    pub fn idempotency_id(&self) -> &Identifier {
        &self.idempotency_id
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

    pub fn policy_decision_ref(&self) -> Option<&CanonicalReference> {
        self.policy_decision_ref.as_ref()
    }

    pub fn artifact_or_target_refs(&self) -> &BTreeSet<CanonicalReference> {
        &self.artifact_or_target_refs
    }

    pub fn expected_current_state(&self) -> Option<&ExpectedState> {
        self.expected_current_state.as_ref()
    }

    pub fn parameters(&self) -> &OperationParameters {
        &self.parameters
    }

    pub const fn deadline(&self) -> RequestDeadline {
        self.deadline
    }

    pub fn correlation_id(&self) -> &Identifier {
        &self.correlation_id
    }

    /// Deterministic length-prefixed request representation for replay binding.
    pub fn canonical_body(&self) -> String {
        let mut output = String::new();
        append_field(&mut output, "contract_version", &self.contract_version);
        append_field(&mut output, "operation", self.operation.as_str());
        append_field(&mut output, "request_id", self.request_id.as_str());
        append_field(&mut output, "idempotency_id", self.idempotency_id.as_str());
        append_field(
            &mut output,
            "caller_identity",
            self.caller_identity.as_str(),
        );
        append_field(
            &mut output,
            "service_identity",
            self.service_identity.as_str(),
        );
        append_field(
            &mut output,
            "profile_context_ref",
            self.profile_context_ref.as_str(),
        );
        append_field(
            &mut output,
            "policy_decision_ref",
            self.policy_decision_ref
                .as_ref()
                .map(CanonicalReference::as_str)
                .unwrap_or("none"),
        );
        for target in &self.artifact_or_target_refs {
            append_field(&mut output, "target", target.as_str());
        }
        append_field(
            &mut output,
            "expected_current_state",
            &self
                .expected_current_state
                .as_ref()
                .map(ExpectedState::canonical)
                .unwrap_or_else(|| "none".to_owned()),
        );
        append_field(&mut output, "parameters", &self.parameters.canonical());
        append_field(
            &mut output,
            "submitted_at",
            &self.deadline.submitted_at().to_string(),
        );
        append_field(
            &mut output,
            "expires_at",
            &self.deadline.expires_at().to_string(),
        );
        append_field(&mut output, "correlation_id", self.correlation_id.as_str());
        output
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct RequestIdentityBinding {
    request_id: Identifier,
    idempotency_id: Identifier,
    canonical_body: String,
}

impl RequestIdentityBinding {
    pub fn from_request(request: &NodeOperationRequest) -> Self {
        Self {
            request_id: request.request_id.clone(),
            idempotency_id: request.idempotency_id.clone(),
            canonical_body: request.canonical_body(),
        }
    }

    pub fn compare(&self, candidate: &NodeOperationRequest) -> ReplayDisposition {
        if self.request_id != candidate.request_id
            || self.idempotency_id != candidate.idempotency_id
        {
            ReplayDisposition::UnrelatedIdentity
        } else if self.canonical_body == candidate.canonical_body() {
            ReplayDisposition::EquivalentReplay
        } else {
            ReplayDisposition::IdentityConflict
        }
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum ReplayDisposition {
    EquivalentReplay,
    IdentityConflict,
    UnrelatedIdentity,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum RequestBuildErrorCode {
    EmptyValue,
    ValueTooLong,
    ValueContainsControlCharacter,
    ValueHasOuterWhitespace,
    InvalidIdentifier,
    InvalidDeadline,
    ParameterOperationMismatch,
    DuplicateTarget,
    TooManyTargets,
    InvalidVolumeParameters,
}

impl RequestBuildErrorCode {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::EmptyValue => "empty_value",
            Self::ValueTooLong => "value_too_long",
            Self::ValueContainsControlCharacter => "value_contains_control_character",
            Self::ValueHasOuterWhitespace => "value_has_outer_whitespace",
            Self::InvalidIdentifier => "invalid_identifier",
            Self::InvalidDeadline => "invalid_deadline",
            Self::ParameterOperationMismatch => "parameter_operation_mismatch",
            Self::DuplicateTarget => "duplicate_target",
            Self::TooManyTargets => "too_many_targets",
            Self::InvalidVolumeParameters => "invalid_volume_parameters",
        }
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct RequestBuildError {
    code: RequestBuildErrorCode,
    detail: String,
}

impl RequestBuildError {
    fn new(code: RequestBuildErrorCode, detail: impl Into<String>) -> Self {
        Self {
            code,
            detail: detail.into(),
        }
    }

    pub const fn code(&self) -> RequestBuildErrorCode {
        self.code
    }

    pub fn detail(&self) -> &str {
        &self.detail
    }
}

impl fmt::Display for RequestBuildError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "{}: {}", self.code.as_str(), self.detail)
    }
}

impl std::error::Error for RequestBuildError {}

fn validate_bounded_value(
    value: &str,
    maximum_bytes: usize,
    name: &str,
) -> Result<(), RequestBuildError> {
    if value.is_empty() {
        return Err(RequestBuildError::new(
            RequestBuildErrorCode::EmptyValue,
            format!("{name} must not be empty"),
        ));
    }
    if value.len() > maximum_bytes {
        return Err(RequestBuildError::new(
            RequestBuildErrorCode::ValueTooLong,
            format!("{name} exceeds {maximum_bytes} bytes"),
        ));
    }
    if value.trim() != value {
        return Err(RequestBuildError::new(
            RequestBuildErrorCode::ValueHasOuterWhitespace,
            format!("{name} may not have leading or trailing whitespace"),
        ));
    }
    if value.chars().any(char::is_control) {
        return Err(RequestBuildError::new(
            RequestBuildErrorCode::ValueContainsControlCharacter,
            format!("{name} may not contain control characters"),
        ));
    }
    Ok(())
}

fn validate_volume_parameters(parameters: &OperationParameters) -> Result<(), RequestBuildError> {
    let OperationParameters::ManageDeclaredEncryptedVolume { action, mount_path } = parameters
    else {
        return Ok(());
    };
    match (action, mount_path) {
        (EncryptedVolumeAction::Mount, None) => Err(RequestBuildError::new(
            RequestBuildErrorCode::InvalidVolumeParameters,
            "mount requires one allowlisted mount path",
        )),
        (EncryptedVolumeAction::Mount, Some(_)) => Ok(()),
        (_, Some(_)) => Err(RequestBuildError::new(
            RequestBuildErrorCode::InvalidVolumeParameters,
            "only the mount action accepts a mount path",
        )),
        (_, None) => Ok(()),
    }
}

fn append_field(output: &mut String, name: &str, value: &str) {
    output.push_str(name);
    output.push('=');
    output.push_str(&value.len().to_string());
    output.push(':');
    output.push_str(value);
    output.push(';');
}
