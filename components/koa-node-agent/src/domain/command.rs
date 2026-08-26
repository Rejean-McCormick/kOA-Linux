//! Closed command and operation identities for the kOA Node Agent.
//!
//! This module deliberately contains no free-form command representation. Every
//! privileged effect must map to one of the operation identifiers frozen by the
//! component contract.

use core::fmt;
use core::str::FromStr;

/// Version of the public command contract implemented by this bundle.
pub const NODE_OPERATION_CONTRACT_VERSION: &str = "1.0.0";

/// The complete closed operation allowlist owned by the kOA Node Agent contract.
#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub enum Operation {
    InspectNodeState,
    StageSystemArtifact,
    ActivateSystemArtifact,
    ActivateServiceBundle,
    ActivateGovernanceBundle,
    ManageKnowledgeArtifact,
    ImportOfflineBundle,
    ManageDeclaredEncryptedVolume,
    RestartAllowlistedServiceGroup,
    RotateNodeScopedKey,
    ExportNodeEvidence,
    EnterRecoveryTarget,
    ExecuteRollbackOrForwardRepair,
}

impl Operation {
    /// All registered operations, in canonical contract order.
    pub const ALL: [Self; 13] = [
        Self::InspectNodeState,
        Self::StageSystemArtifact,
        Self::ActivateSystemArtifact,
        Self::ActivateServiceBundle,
        Self::ActivateGovernanceBundle,
        Self::ManageKnowledgeArtifact,
        Self::ImportOfflineBundle,
        Self::ManageDeclaredEncryptedVolume,
        Self::RestartAllowlistedServiceGroup,
        Self::RotateNodeScopedKey,
        Self::ExportNodeEvidence,
        Self::EnterRecoveryTarget,
        Self::ExecuteRollbackOrForwardRepair,
    ];

    pub const fn as_str(self) -> &'static str {
        match self {
            Self::InspectNodeState => "inspect_node_state",
            Self::StageSystemArtifact => "stage_system_artifact",
            Self::ActivateSystemArtifact => "activate_system_artifact",
            Self::ActivateServiceBundle => "activate_service_bundle",
            Self::ActivateGovernanceBundle => "activate_governance_bundle",
            Self::ManageKnowledgeArtifact => "manage_knowledge_artifact",
            Self::ImportOfflineBundle => "import_offline_bundle",
            Self::ManageDeclaredEncryptedVolume => "manage_declared_encrypted_volume",
            Self::RestartAllowlistedServiceGroup => "restart_allowlisted_service_group",
            Self::RotateNodeScopedKey => "rotate_node_scoped_key",
            Self::ExportNodeEvidence => "export_node_evidence",
            Self::EnterRecoveryTarget => "enter_recovery_target",
            Self::ExecuteRollbackOrForwardRepair => "execute_rollback_or_forward_repair",
        }
    }

    pub const fn authorization_class(self) -> AuthorizationClass {
        match self {
            Self::InspectNodeState => AuthorizationClass::NodeInspection,
            Self::StageSystemArtifact => AuthorizationClass::SystemArtifactStaging,
            Self::ActivateSystemArtifact => AuthorizationClass::SystemArtifactActivation,
            Self::ActivateServiceBundle => AuthorizationClass::ServiceBundleActivation,
            Self::ActivateGovernanceBundle => AuthorizationClass::GovernanceBundleActivation,
            Self::ManageKnowledgeArtifact => AuthorizationClass::KnowledgeArtifactLifecycle,
            Self::ImportOfflineBundle => AuthorizationClass::OfflineBundleImport,
            Self::ManageDeclaredEncryptedVolume => AuthorizationClass::EncryptedVolumeLifecycle,
            Self::RestartAllowlistedServiceGroup => AuthorizationClass::ServiceGroupControl,
            Self::RotateNodeScopedKey => AuthorizationClass::NodeKeyRotation,
            Self::ExportNodeEvidence => AuthorizationClass::NodeEvidenceExport,
            Self::EnterRecoveryTarget | Self::ExecuteRollbackOrForwardRepair => {
                AuthorizationClass::NodeRecovery
            },
        }
    }

    pub const fn mutates_host(self) -> bool {
        !matches!(self, Self::InspectNodeState | Self::ExportNodeEvidence)
    }

    pub const fn idempotency_rule(self) -> IdempotencyRule {
        match self {
            Self::InspectNodeState => IdempotencyRule::RepeatableRead,
            Self::StageSystemArtifact => IdempotencyRule::RequestIdAndArtifactIdentity,
            Self::ActivateSystemArtifact => {
                IdempotencyRule::RequestIdExpectedStateAndArtifactIdentity
            },
            Self::ActivateServiceBundle => IdempotencyRule::RequestIdExpectedStateAndBundleIdentity,
            Self::ActivateGovernanceBundle => {
                IdempotencyRule::RequestIdExpectedStateAndBundleIdentity
            },
            Self::ManageKnowledgeArtifact => {
                IdempotencyRule::RequestIdExpectedStateArtifactIdentityAndAction
            },
            Self::ImportOfflineBundle => IdempotencyRule::RequestIdBundleIdentityAndTargetState,
            Self::ManageDeclaredEncryptedVolume => {
                IdempotencyRule::RequestIdVolumeIdentityExpectedStateAndAction
            },
            Self::RestartAllowlistedServiceGroup => {
                IdempotencyRule::RequestIdServiceGroupExpectedState
            },
            Self::RotateNodeScopedKey => IdempotencyRule::RequestIdKeyIdentityExpectedVersion,
            Self::ExportNodeEvidence => IdempotencyRule::RequestIdEvidenceScopeAndPolicyDecision,
            Self::EnterRecoveryTarget => IdempotencyRule::RequestIdExpectedStateAndRecoveryTarget,
            Self::ExecuteRollbackOrForwardRepair => {
                IdempotencyRule::RequestIdFailedTransitionAndRecoveryPlan
            },
        }
    }

    pub const fn receipt_policy(self) -> ReceiptPolicy {
        match self {
            Self::InspectNodeState => ReceiptPolicy::OptionalUnlessRequired,
            Self::ManageKnowledgeArtifact => ReceiptPolicy::KnowledgeLifecycleConditional,
            Self::RestartAllowlistedServiceGroup => ReceiptPolicy::CriticalOperationConditional,
            _ => ReceiptPolicy::Required,
        }
    }

    /// Whether the request schema requires one or more explicit target references.
    pub const fn requires_target(self) -> bool {
        !matches!(self, Self::InspectNodeState)
    }
}

impl fmt::Display for Operation {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(self.as_str())
    }
}

impl FromStr for Operation {
    type Err = UnknownOperation;

    fn from_str(value: &str) -> Result<Self, Self::Err> {
        match value {
            "inspect_node_state" => Ok(Self::InspectNodeState),
            "stage_system_artifact" => Ok(Self::StageSystemArtifact),
            "activate_system_artifact" => Ok(Self::ActivateSystemArtifact),
            "activate_service_bundle" => Ok(Self::ActivateServiceBundle),
            "activate_governance_bundle" => Ok(Self::ActivateGovernanceBundle),
            "manage_knowledge_artifact" => Ok(Self::ManageKnowledgeArtifact),
            "import_offline_bundle" => Ok(Self::ImportOfflineBundle),
            "manage_declared_encrypted_volume" => Ok(Self::ManageDeclaredEncryptedVolume),
            "restart_allowlisted_service_group" => Ok(Self::RestartAllowlistedServiceGroup),
            "rotate_node_scoped_key" => Ok(Self::RotateNodeScopedKey),
            "export_node_evidence" => Ok(Self::ExportNodeEvidence),
            "enter_recovery_target" => Ok(Self::EnterRecoveryTarget),
            "execute_rollback_or_forward_repair" => Ok(Self::ExecuteRollbackOrForwardRepair),
            _ => Err(UnknownOperation::new(value)),
        }
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct UnknownOperation {
    value: String,
}

impl UnknownOperation {
    fn new(value: &str) -> Self {
        Self {
            value: value.to_owned(),
        }
    }

    pub fn value(&self) -> &str {
        &self.value
    }

    pub const fn code(&self) -> &'static str {
        "unknown_operation"
    }
}

impl fmt::Display for UnknownOperation {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "unregistered node operation: {}", self.value)
    }
}

impl std::error::Error for UnknownOperation {}

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub enum AuthorizationClass {
    NodeInspection,
    SystemArtifactStaging,
    SystemArtifactActivation,
    ServiceBundleActivation,
    GovernanceBundleActivation,
    KnowledgeArtifactLifecycle,
    OfflineBundleImport,
    EncryptedVolumeLifecycle,
    ServiceGroupControl,
    NodeKeyRotation,
    NodeEvidenceExport,
    NodeRecovery,
}

impl AuthorizationClass {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::NodeInspection => "node_inspection",
            Self::SystemArtifactStaging => "system_artifact_staging",
            Self::SystemArtifactActivation => "system_artifact_activation",
            Self::ServiceBundleActivation => "service_bundle_activation",
            Self::GovernanceBundleActivation => "governance_bundle_activation",
            Self::KnowledgeArtifactLifecycle => "knowledge_artifact_lifecycle",
            Self::OfflineBundleImport => "offline_bundle_import",
            Self::EncryptedVolumeLifecycle => "encrypted_volume_lifecycle",
            Self::ServiceGroupControl => "service_group_control",
            Self::NodeKeyRotation => "node_key_rotation",
            Self::NodeEvidenceExport => "node_evidence_export",
            Self::NodeRecovery => "node_recovery",
        }
    }
}

impl fmt::Display for AuthorizationClass {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(self.as_str())
    }
}

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub enum IdempotencyRule {
    RepeatableRead,
    RequestIdAndArtifactIdentity,
    RequestIdExpectedStateAndArtifactIdentity,
    RequestIdExpectedStateAndBundleIdentity,
    RequestIdExpectedStateArtifactIdentityAndAction,
    RequestIdBundleIdentityAndTargetState,
    RequestIdVolumeIdentityExpectedStateAndAction,
    RequestIdServiceGroupExpectedState,
    RequestIdKeyIdentityExpectedVersion,
    RequestIdEvidenceScopeAndPolicyDecision,
    RequestIdExpectedStateAndRecoveryTarget,
    RequestIdFailedTransitionAndRecoveryPlan,
}

impl IdempotencyRule {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::RepeatableRead => "repeatable_read",
            Self::RequestIdAndArtifactIdentity => "request_id_and_artifact_identity",
            Self::RequestIdExpectedStateAndArtifactIdentity => {
                "request_id_expected_state_and_artifact_identity"
            },
            Self::RequestIdExpectedStateAndBundleIdentity => {
                "request_id_expected_state_and_bundle_identity"
            },
            Self::RequestIdExpectedStateArtifactIdentityAndAction => {
                "request_id_expected_state_artifact_identity_and_action"
            },
            Self::RequestIdBundleIdentityAndTargetState => {
                "request_id_bundle_identity_and_target_state"
            },
            Self::RequestIdVolumeIdentityExpectedStateAndAction => {
                "request_id_volume_identity_expected_state_and_action"
            },
            Self::RequestIdServiceGroupExpectedState => "request_id_service_group_expected_state",
            Self::RequestIdKeyIdentityExpectedVersion => "request_id_key_identity_expected_version",
            Self::RequestIdEvidenceScopeAndPolicyDecision => {
                "request_id_evidence_scope_and_policy_decision"
            },
            Self::RequestIdExpectedStateAndRecoveryTarget => {
                "request_id_expected_state_and_recovery_target"
            },
            Self::RequestIdFailedTransitionAndRecoveryPlan => {
                "request_id_failed_transition_and_recovery_plan"
            },
        }
    }
}

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub enum ReceiptPolicy {
    OptionalUnlessRequired,
    Required,
    KnowledgeLifecycleConditional,
    CriticalOperationConditional,
}

impl ReceiptPolicy {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::OptionalUnlessRequired => "optional_unless_profile_or_security_policy_requires",
            Self::Required => "required",
            Self::KnowledgeLifecycleConditional => "required_for_activation_quarantine_or_revert",
            Self::CriticalOperationConditional => "required_when_critical",
        }
    }
}

/// Closed public command interface names.
#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub enum CommandInterface {
    ExecuteNodeOperation,
    CancelNodeOperation,
    AcknowledgeRecoveryResult,
}

impl CommandInterface {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::ExecuteNodeOperation => "execute_node_operation",
            Self::CancelNodeOperation => "cancel_node_operation",
            Self::AcknowledgeRecoveryResult => "acknowledge_recovery_result",
        }
    }
}

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub enum ExecuteResponse {
    Accepted,
    Completed,
    Rejected,
    Conflict,
    TimedOut,
    Failed,
    RecoveryRequired,
}

impl ExecuteResponse {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::Accepted => "accepted",
            Self::Completed => "completed",
            Self::Rejected => "rejected",
            Self::Conflict => "conflict",
            Self::TimedOut => "timed_out",
            Self::Failed => "failed",
            Self::RecoveryRequired => "recovery_required",
        }
    }
}
