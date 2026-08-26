//! Closed privileged-operation catalog for the kOA Node Agent.
//!
//! This module intentionally contains no dynamic registration mechanism. Adding an
//! operation requires a canonical contract change and a source change here.

use std::collections::BTreeSet;
use std::fmt;
use std::str::FromStr;

/// Canonical privileged operations declared by the Node Agent component contract.
#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub enum OperationId {
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

impl OperationId {
    /// Stable canonical identifier used on the public interface and in receipts.
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

impl fmt::Display for OperationId {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(self.as_str())
    }
}

impl FromStr for OperationId {
    type Err = CatalogError;

    fn from_str(value: &str) -> Result<Self, Self::Err> {
        let operation = match value {
            "inspect_node_state" => Self::InspectNodeState,
            "stage_system_artifact" => Self::StageSystemArtifact,
            "activate_system_artifact" => Self::ActivateSystemArtifact,
            "activate_service_bundle" => Self::ActivateServiceBundle,
            "activate_governance_bundle" => Self::ActivateGovernanceBundle,
            "manage_knowledge_artifact" => Self::ManageKnowledgeArtifact,
            "import_offline_bundle" => Self::ImportOfflineBundle,
            "manage_declared_encrypted_volume" => Self::ManageDeclaredEncryptedVolume,
            "restart_allowlisted_service_group" => Self::RestartAllowlistedServiceGroup,
            "rotate_node_scoped_key" => Self::RotateNodeScopedKey,
            "export_node_evidence" => Self::ExportNodeEvidence,
            "enter_recovery_target" => Self::EnterRecoveryTarget,
            "execute_rollback_or_forward_repair" => Self::ExecuteRollbackOrForwardRepair,
            _ => return Err(CatalogError::UnknownOperation(value.to_owned())),
        };
        Ok(operation)
    }
}

/// Idempotency rule projected from the canonical component contract.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum IdempotencyRule {
    RepeatableRead,
    RequestAndArtifactIdentity,
    RequestExpectedStateAndArtifactIdentity,
    RequestExpectedStateAndBundleIdentity,
    RequestExpectedStateArtifactIdentityAndAction,
    RequestBundleIdentityAndTargetState,
    RequestVolumeIdentityExpectedStateAndAction,
    RequestServiceGroupExpectedState,
    RequestKeyIdentityExpectedVersion,
    RequestEvidenceScopeAndPolicyDecision,
    RequestExpectedStateAndRecoveryTarget,
    RequestFailedTransitionAndRecoveryPlan,
}

impl IdempotencyRule {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::RepeatableRead => "repeatable_read",
            Self::RequestAndArtifactIdentity => "request_id_and_artifact_identity",
            Self::RequestExpectedStateAndArtifactIdentity => {
                "request_id_expected_state_and_artifact_identity"
            },
            Self::RequestExpectedStateAndBundleIdentity => {
                "request_id_expected_state_and_bundle_identity"
            },
            Self::RequestExpectedStateArtifactIdentityAndAction => {
                "request_id_expected_state_artifact_identity_and_action"
            },
            Self::RequestBundleIdentityAndTargetState => {
                "request_id_bundle_identity_and_target_state"
            },
            Self::RequestVolumeIdentityExpectedStateAndAction => {
                "request_id_volume_identity_expected_state_and_action"
            },
            Self::RequestServiceGroupExpectedState => "request_id_service_group_expected_state",
            Self::RequestKeyIdentityExpectedVersion => "request_id_key_identity_expected_version",
            Self::RequestEvidenceScopeAndPolicyDecision => {
                "request_id_evidence_scope_and_policy_decision"
            },
            Self::RequestExpectedStateAndRecoveryTarget => {
                "request_id_expected_state_and_recovery_target"
            },
            Self::RequestFailedTransitionAndRecoveryPlan => {
                "request_id_failed_transition_and_recovery_plan"
            },
        }
    }
}

/// Receipt rule projected from the canonical component contract.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum ReceiptPolicy {
    OptionalUnlessRequired,
    Required,
    RequiredForActivationQuarantineOrRevert,
    RequiredWhenCritical,
}

impl ReceiptPolicy {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::OptionalUnlessRequired => "optional_unless_profile_or_security_policy_requires",
            Self::Required => "required",
            Self::RequiredForActivationQuarantineOrRevert => {
                "required_for_activation_quarantine_or_revert"
            },
            Self::RequiredWhenCritical => "required_when_critical",
        }
    }

    /// Whether a terminal successful result must carry a durable receipt.
    pub fn requires_receipt(self, parameters: &std::collections::BTreeMap<String, String>) -> bool {
        match self {
            Self::OptionalUnlessRequired => false,
            Self::Required => true,
            Self::RequiredWhenCritical => parameters
                .get("critical")
                .map(|value| value == "true")
                .unwrap_or(true),
            Self::RequiredForActivationQuarantineOrRevert => parameters
                .get("action")
                .map(|action| matches!(action.as_str(), "activate" | "quarantine" | "revert"))
                .unwrap_or(true),
        }
    }
}

/// Closed parameter policy. Unknown keys are rejected.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum ParameterPolicy {
    None,
    KnowledgeAction,
    OfflineTargetState,
    EncryptedVolumeAction,
    ServiceGroupCriticality,
}

impl ParameterPolicy {
    pub const fn allowed_keys(self) -> &'static [&'static str] {
        match self {
            Self::None => &[],
            Self::KnowledgeAction => &["action"],
            Self::OfflineTargetState => &["target_state"],
            Self::EncryptedVolumeAction => &["action"],
            Self::ServiceGroupCriticality => &["critical"],
        }
    }

    pub fn validate_value(self, key: &str, value: &str) -> bool {
        match (self, key) {
            (Self::KnowledgeAction, "action") => matches!(
                value,
                "install" | "activate" | "pin" | "unpin" | "quarantine" | "revert"
            ),
            (Self::OfflineTargetState, "target_state") => {
                matches!(value, "quarantine" | "staging")
            },
            (Self::EncryptedVolumeAction, "action") => {
                matches!(
                    value,
                    "create" | "unlock" | "mount" | "unmount" | "rotate" | "retire"
                )
            },
            (Self::ServiceGroupCriticality, "critical") => matches!(value, "true" | "false"),
            (Self::None, _) => false,
            _ => false,
        }
    }
}

/// Immutable metadata for one closed operation class.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct OperationSpec {
    pub id: OperationId,
    pub purpose: &'static str,
    pub authorization_class: &'static str,
    pub mutates_host: bool,
    pub idempotency: IdempotencyRule,
    pub receipt: ReceiptPolicy,
    pub minimum_references: usize,
    pub maximum_references: usize,
    pub parameters: ParameterPolicy,
}

const OPERATIONS: [OperationSpec; 13] = [
    OperationSpec {
        id: OperationId::InspectNodeState,
        purpose: "Return bounded node identity, active profile, booted release, active Release Set, health, readiness, and recovery state.",
        authorization_class: "node_inspection",
        mutates_host: false,
        idempotency: IdempotencyRule::RepeatableRead,
        receipt: ReceiptPolicy::OptionalUnlessRequired,
        minimum_references: 0,
        maximum_references: 0,
        parameters: ParameterPolicy::None,
    },
    OperationSpec {
        id: OperationId::StageSystemArtifact,
        purpose: "Stage a validated system image or equivalent system-channel artifact without activating it.",
        authorization_class: "system_artifact_staging",
        mutates_host: true,
        idempotency: IdempotencyRule::RequestAndArtifactIdentity,
        receipt: ReceiptPolicy::Required,
        minimum_references: 1,
        maximum_references: 1,
        parameters: ParameterPolicy::None,
    },
    OperationSpec {
        id: OperationId::ActivateSystemArtifact,
        purpose: "Activate a staged verified system artifact through an atomic boot slot, pointer, or equivalent profile-defined transition.",
        authorization_class: "system_artifact_activation",
        mutates_host: true,
        idempotency: IdempotencyRule::RequestExpectedStateAndArtifactIdentity,
        receipt: ReceiptPolicy::Required,
        minimum_references: 1,
        maximum_references: 1,
        parameters: ParameterPolicy::None,
    },
    OperationSpec {
        id: OperationId::ActivateServiceBundle,
        purpose: "Activate a compatible services-channel bundle using a complete profile-authorized transition.",
        authorization_class: "service_bundle_activation",
        mutates_host: true,
        idempotency: IdempotencyRule::RequestExpectedStateAndBundleIdentity,
        receipt: ReceiptPolicy::Required,
        minimum_references: 1,
        maximum_references: 1,
        parameters: ParameterPolicy::None,
    },
    OperationSpec {
        id: OperationId::ActivateGovernanceBundle,
        purpose: "Activate an accepted and compatible governance policy bundle without creating or changing policy authority.",
        authorization_class: "governance_bundle_activation",
        mutates_host: true,
        idempotency: IdempotencyRule::RequestExpectedStateAndBundleIdentity,
        receipt: ReceiptPolicy::Required,
        minimum_references: 1,
        maximum_references: 1,
        parameters: ParameterPolicy::None,
    },
    OperationSpec {
        id: OperationId::ManageKnowledgeArtifact,
        purpose: "Install, activate, pin, unpin, quarantine, or revert a registered knowledge artifact when permitted by its class and profile.",
        authorization_class: "knowledge_artifact_lifecycle",
        mutates_host: true,
        idempotency: IdempotencyRule::RequestExpectedStateArtifactIdentityAndAction,
        receipt: ReceiptPolicy::RequiredForActivationQuarantineOrRevert,
        minimum_references: 1,
        maximum_references: 1,
        parameters: ParameterPolicy::KnowledgeAction,
    },
    OperationSpec {
        id: OperationId::ImportOfflineBundle,
        purpose: "Admit a verified offline bundle into quarantine or staging for controlled local validation and activation.",
        authorization_class: "offline_bundle_import",
        mutates_host: true,
        idempotency: IdempotencyRule::RequestBundleIdentityAndTargetState,
        receipt: ReceiptPolicy::Required,
        minimum_references: 1,
        maximum_references: 1,
        parameters: ParameterPolicy::OfflineTargetState,
    },
    OperationSpec {
        id: OperationId::ManageDeclaredEncryptedVolume,
        purpose: "Create, unlock, mount, unmount, rotate, or retire a profile-declared encrypted volume through a closed operation schema.",
        authorization_class: "encrypted_volume_lifecycle",
        mutates_host: true,
        idempotency: IdempotencyRule::RequestVolumeIdentityExpectedStateAndAction,
        receipt: ReceiptPolicy::Required,
        minimum_references: 1,
        maximum_references: 1,
        parameters: ParameterPolicy::EncryptedVolumeAction,
    },
    OperationSpec {
        id: OperationId::RestartAllowlistedServiceGroup,
        purpose: "Restart one profile-declared service group after validation of current state, dependency conditions, and authorization.",
        authorization_class: "service_group_control",
        mutates_host: true,
        idempotency: IdempotencyRule::RequestServiceGroupExpectedState,
        receipt: ReceiptPolicy::RequiredWhenCritical,
        minimum_references: 1,
        maximum_references: 1,
        parameters: ParameterPolicy::ServiceGroupCriticality,
    },
    OperationSpec {
        id: OperationId::RotateNodeScopedKey,
        purpose: "Perform a governed rotation of one node-scoped key without exporting raw private-key material.",
        authorization_class: "node_key_rotation",
        mutates_host: true,
        idempotency: IdempotencyRule::RequestKeyIdentityExpectedVersion,
        receipt: ReceiptPolicy::Required,
        minimum_references: 1,
        maximum_references: 1,
        parameters: ParameterPolicy::None,
    },
    OperationSpec {
        id: OperationId::ExportNodeEvidence,
        purpose: "Export an authorized bounded node-evidence package through the applicable audit and disclosure path.",
        authorization_class: "node_evidence_export",
        mutates_host: false,
        idempotency: IdempotencyRule::RequestEvidenceScopeAndPolicyDecision,
        receipt: ReceiptPolicy::Required,
        minimum_references: 1,
        maximum_references: 1,
        parameters: ParameterPolicy::None,
    },
    OperationSpec {
        id: OperationId::EnterRecoveryTarget,
        purpose: "Transition the node into a profile-defined recovery environment or mode.",
        authorization_class: "node_recovery",
        mutates_host: true,
        idempotency: IdempotencyRule::RequestExpectedStateAndRecoveryTarget,
        receipt: ReceiptPolicy::Required,
        minimum_references: 1,
        maximum_references: 1,
        parameters: ParameterPolicy::None,
    },
    OperationSpec {
        id: OperationId::ExecuteRollbackOrForwardRepair,
        purpose: "Apply the declared recovery strategy for a failed activation or migration.",
        authorization_class: "node_recovery",
        mutates_host: true,
        idempotency: IdempotencyRule::RequestFailedTransitionAndRecoveryPlan,
        receipt: ReceiptPolicy::Required,
        minimum_references: 1,
        maximum_references: 1,
        parameters: ParameterPolicy::None,
    },
];

/// All operations in canonical order.
pub const fn operations() -> &'static [OperationSpec] {
    &OPERATIONS
}

/// Return the immutable metadata for one operation.
pub fn operation_spec(id: OperationId) -> &'static OperationSpec {
    OPERATIONS
        .iter()
        .find(|spec| spec.id == id)
        .expect("every OperationId must be represented in the closed catalog")
}

/// Verify source-level catalog invariants without executing a privileged effect.
pub fn validate_catalog() -> Result<(), CatalogError> {
    if OPERATIONS.len() != 13 {
        return Err(CatalogError::InvariantViolation(
            "the canonical catalog must contain exactly 13 operations",
        ));
    }

    let mut identifiers = BTreeSet::new();
    let mut authorization_classes = BTreeSet::new();
    for spec in OPERATIONS {
        if !identifiers.insert(spec.id.as_str()) {
            return Err(CatalogError::InvariantViolation(
                "operation identifiers must be unique",
            ));
        }
        authorization_classes.insert(spec.authorization_class);
        if spec.minimum_references > spec.maximum_references {
            return Err(CatalogError::InvariantViolation(
                "minimum reference count cannot exceed maximum reference count",
            ));
        }
        if spec.id.as_str().parse::<OperationId>()? != spec.id {
            return Err(CatalogError::InvariantViolation(
                "operation identifier round trip failed",
            ));
        }
    }

    if authorization_classes.is_empty() {
        return Err(CatalogError::InvariantViolation(
            "every catalog requires authorization classes",
        ));
    }
    Ok(())
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum CatalogError {
    UnknownOperation(String),
    InvariantViolation(&'static str),
}

impl fmt::Display for CatalogError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::UnknownOperation(value) => {
                write!(formatter, "unknown privileged operation: {value}")
            },
            Self::InvariantViolation(message) => formatter.write_str(message),
        }
    }
}

impl std::error::Error for CatalogError {}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn catalog_is_closed_and_valid() {
        validate_catalog().expect("canonical catalog must be valid");
        assert!("run_command".parse::<OperationId>().is_err());
        assert!("restart_allowlisted_service_group"
            .parse::<OperationId>()
            .is_ok());
    }

    #[test]
    fn action_policies_are_closed() {
        assert!(ParameterPolicy::KnowledgeAction.validate_value("action", "quarantine"));
        assert!(!ParameterPolicy::KnowledgeAction.validate_value("action", "delete"));
        assert!(!ParameterPolicy::None.validate_value("command", "sh"));
    }
}
