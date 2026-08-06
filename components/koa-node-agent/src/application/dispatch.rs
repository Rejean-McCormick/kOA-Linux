//! Closed dispatch from a validated operation to a fixed handler identity.

use crate::domain::{AuthorizationDecision, NodeOperationRequest, Operation};

use super::validate_request::{
    validate_request, RequestValidationError, ValidatedRequest, ValidationContext,
};

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub enum DispatchRoute {
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

impl DispatchRoute {
    pub const fn from_operation(operation: Operation) -> Self {
        match operation {
            Operation::InspectNodeState => Self::InspectNodeState,
            Operation::StageSystemArtifact => Self::StageSystemArtifact,
            Operation::ActivateSystemArtifact => Self::ActivateSystemArtifact,
            Operation::ActivateServiceBundle => Self::ActivateServiceBundle,
            Operation::ActivateGovernanceBundle => Self::ActivateGovernanceBundle,
            Operation::ManageKnowledgeArtifact => Self::ManageKnowledgeArtifact,
            Operation::ImportOfflineBundle => Self::ImportOfflineBundle,
            Operation::ManageDeclaredEncryptedVolume => Self::ManageDeclaredEncryptedVolume,
            Operation::RestartAllowlistedServiceGroup => Self::RestartAllowlistedServiceGroup,
            Operation::RotateNodeScopedKey => Self::RotateNodeScopedKey,
            Operation::ExportNodeEvidence => Self::ExportNodeEvidence,
            Operation::EnterRecoveryTarget => Self::EnterRecoveryTarget,
            Operation::ExecuteRollbackOrForwardRepair => {
                Self::ExecuteRollbackOrForwardRepair
            }
        }
    }

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
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct DispatchPlan {
    route: DispatchRoute,
    validated_request: ValidatedRequest,
}

impl DispatchPlan {
    pub const fn route(&self) -> DispatchRoute {
        self.route
    }

    pub fn validated_request(&self) -> &ValidatedRequest {
        &self.validated_request
    }

    pub fn into_validated_request(self) -> ValidatedRequest {
        self.validated_request
    }
}

pub fn dispatch(
    request: NodeOperationRequest,
    authorization: AuthorizationDecision,
    context: &ValidationContext,
) -> Result<DispatchPlan, RequestValidationError> {
    let validated_request = validate_request(request, authorization, context)?;
    let route = DispatchRoute::from_operation(validated_request.request().operation());
    Ok(DispatchPlan {
        route,
        validated_request,
    })
}
