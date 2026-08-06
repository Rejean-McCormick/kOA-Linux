use crate::{
    require_non_empty, schema, validate_non_empty_values, BindingValidationError,
    CorrelationContext, ExecutionState,
};
use serde::{Deserialize, Serialize};

#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum ReceiptClass {
    DecisionReceipt,
    TransitionReceipt,
    VerificationReceipt,
    TransferReceipt,
    RecoveryReceipt,
    EvidenceAccessReceipt,
    CutoverReceipt,
}

#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum DecisionState {
    NotEvaluated,
    Authorized,
    Denied,
    Indeterminate,
    NotApplicable,
}

#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum CommitState {
    NotAttempted,
    Prepared,
    Committed,
    Failed,
    RolledBack,
    ForwardRepaired,
}

#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum ReceiptOutcome {
    Authorized,
    Denied,
    Indeterminate,
    Prepared,
    Committed,
    Failed,
    Cancelled,
    RolledBack,
    ForwardRepaired,
    Expired,
    Revoked,
    Superseded,
    Closed,
}

#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum DisclosureClass {
    PublicSummary,
    TenantVisible,
    OperatorRestricted,
    SecurityRestricted,
    EvidenceRestricted,
}

/// Shared receipt envelope for component-owned decisions and transitions.
#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct ReceiptEnvelope {
    pub schema: String,
    pub receipt_schema_version: String,
    pub receipt_id: String,
    pub receipt_class: ReceiptClass,
    pub transition_type: String,
    pub producer_component_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub producer_instance_id: Option<String>,
    pub subject_ref: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub actor_ref: Option<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub target_refs: Vec<String>,
    pub scope: String,
    pub correlation: CorrelationContext,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub authority_refs: Vec<String>,
    pub decision: DecisionState,
    pub execution_state: ExecutionState,
    pub commit_state: CommitState,
    pub outcome: ReceiptOutcome,
    pub reason_code: String,
    pub requested_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub decided_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub committed_at: Option<String>,
    pub recorded_at: String,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub profile_refs: Vec<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub component_contract_refs: Vec<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub artifact_refs: Vec<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub release_refs: Vec<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub exception_refs: Vec<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub test_refs: Vec<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub evidence_refs: Vec<String>,
    pub disclosure_class: DisclosureClass,
    pub retention_class: String,
}

impl ReceiptEnvelope {
    pub fn validate(&self) -> Result<(), BindingValidationError> {
        if self.schema != schema::RECEIPT_ENVELOPE {
            return Err(BindingValidationError::new(
                "schema",
                "must identify the common receipt-envelope schema",
            ));
        }
        require_non_empty("receipt_schema_version", &self.receipt_schema_version)?;
        require_non_empty("receipt_id", &self.receipt_id)?;
        require_non_empty("transition_type", &self.transition_type)?;
        require_non_empty("producer_component_id", &self.producer_component_id)?;
        if let Some(instance_id) = &self.producer_instance_id {
            require_non_empty("producer_instance_id", instance_id)?;
        }
        require_non_empty("subject_ref", &self.subject_ref)?;
        if let Some(actor_ref) = &self.actor_ref {
            require_non_empty("actor_ref", actor_ref)?;
        }
        require_non_empty("scope", &self.scope)?;
        require_non_empty("reason_code", &self.reason_code)?;
        require_non_empty("requested_at", &self.requested_at)?;
        if let Some(decided_at) = &self.decided_at {
            require_non_empty("decided_at", decided_at)?;
        }
        if let Some(committed_at) = &self.committed_at {
            require_non_empty("committed_at", committed_at)?;
        }
        require_non_empty("recorded_at", &self.recorded_at)?;
        require_non_empty("retention_class", &self.retention_class)?;
        self.correlation.validate()?;
        validate_non_empty_values("target_refs", &self.target_refs)?;
        validate_non_empty_values("authority_refs", &self.authority_refs)?;
        validate_non_empty_values("profile_refs", &self.profile_refs)?;
        validate_non_empty_values(
            "component_contract_refs",
            &self.component_contract_refs,
        )?;
        validate_non_empty_values("artifact_refs", &self.artifact_refs)?;
        validate_non_empty_values("release_refs", &self.release_refs)?;
        validate_non_empty_values("exception_refs", &self.exception_refs)?;
        validate_non_empty_values("test_refs", &self.test_refs)?;
        validate_non_empty_values("evidence_refs", &self.evidence_refs)?;

        if self.outcome == ReceiptOutcome::Committed {
            if self.commit_state != CommitState::Committed {
                return Err(BindingValidationError::new(
                    "commit_state",
                    "must be committed when outcome is committed",
                ));
            }
            if self.committed_at.is_none() {
                return Err(BindingValidationError::new(
                    "committed_at",
                    "is required for a committed outcome",
                ));
            }
        }
        if self.commit_state == CommitState::Committed
            && self.outcome != ReceiptOutcome::Committed
        {
            return Err(BindingValidationError::new(
                "outcome",
                "must be committed when commit_state is committed",
            ));
        }
        if matches!(self.decision, DecisionState::Authorized | DecisionState::Denied)
            && self.decided_at.is_none()
        {
            return Err(BindingValidationError::new(
                "decided_at",
                "is required for an authorized or denied decision",
            ));
        }
        Ok(())
    }
}
