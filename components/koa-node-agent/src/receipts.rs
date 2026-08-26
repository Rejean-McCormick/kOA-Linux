//! Deterministic, secret-free node-operation receipts.

use crate::config::{OperationClass, StoreMode};
use std::collections::{BTreeMap, BTreeSet};
use std::error::Error;
use std::fmt;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ReceiptResult {
    Accepted,
    Completed,
    Rejected,
    Conflict,
    TimedOut,
    Failed,
    RecoveryRequired,
    Cancelled,
    Acknowledged,
}

impl ReceiptResult {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::Accepted => "accepted",
            Self::Completed => "completed",
            Self::Rejected => "rejected",
            Self::Conflict => "conflict",
            Self::TimedOut => "timed_out",
            Self::Failed => "failed",
            Self::RecoveryRequired => "recovery_required",
            Self::Cancelled => "cancelled",
            Self::Acknowledged => "acknowledged",
        }
    }

    pub const fn claims_success(self) -> bool {
        matches!(self, Self::Completed | Self::Acknowledged)
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ReceiptView {
    Public,
    Operational,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ReceiptError {
    message: String,
}

impl ReceiptError {
    fn new(message: impl Into<String>) -> Self {
        Self {
            message: message.into(),
        }
    }
}

impl fmt::Display for ReceiptError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(&self.message)
    }
}

impl Error for ReceiptError {}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ReceiptDraft {
    pub request_id: String,
    pub operation: OperationClass,
    pub authenticated_caller: String,
    pub profile_context_ref: String,
    pub policy_decision_ref_when_required: Option<String>,
    pub before_state: BTreeMap<String, String>,
    pub after_state: BTreeMap<String, String>,
    pub artifact_or_target_identities: Vec<String>,
    pub result: ReceiptResult,
    pub reason_codes: Vec<String>,
    pub started_at: String,
    pub completed_at: String,
    pub duration_millis: u64,
    pub recovery_or_rollback_token_when_applicable: Option<String>,
    pub correlation_id: String,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NodeOperationReceipt {
    pub receipt_id: String,
    pub request_id: String,
    pub operation: OperationClass,
    pub authenticated_caller: String,
    pub profile_context_ref: String,
    pub policy_decision_ref_when_required: Option<String>,
    pub before_state: BTreeMap<String, String>,
    pub after_state: BTreeMap<String, String>,
    pub artifact_or_target_identities: Vec<String>,
    pub result: ReceiptResult,
    pub reason_codes: Vec<String>,
    pub started_at: String,
    pub completed_at: String,
    pub duration_millis: u64,
    pub recovery_or_rollback_token_when_applicable: Option<String>,
    pub correlation_id: String,
}

impl NodeOperationReceipt {
    pub fn from_draft(
        mut draft: ReceiptDraft,
        receipt_store_mode: StoreMode,
    ) -> Result<Self, ReceiptError> {
        validate_identifier(&draft.request_id, "request_id")?;
        validate_identifier(&draft.authenticated_caller, "authenticated_caller")?;
        validate_profile_ref(&draft.profile_context_ref)?;
        validate_optional_identifier(
            draft.policy_decision_ref_when_required.as_deref(),
            "policy_decision_ref_when_required",
        )?;
        validate_timestamp(&draft.started_at, "started_at")?;
        validate_timestamp(&draft.completed_at, "completed_at")?;
        validate_identifier(&draft.correlation_id, "correlation_id")?;
        validate_optional_identifier(
            draft.recovery_or_rollback_token_when_applicable.as_deref(),
            "recovery_or_rollback_token_when_applicable",
        )?;
        validate_state(&draft.before_state, "before_state")?;
        validate_state(&draft.after_state, "after_state")?;
        if draft.artifact_or_target_identities.len() > 64 {
            return Err(ReceiptError::new(
                "artifact_or_target_identities exceeds the bounded limit",
            ));
        }
        for identity in &draft.artifact_or_target_identities {
            validate_identifier(identity, "artifact_or_target_identity")?;
        }
        for reason in &draft.reason_codes {
            validate_reason_code(reason)?;
        }
        draft.artifact_or_target_identities.sort();
        draft.artifact_or_target_identities.dedup();
        draft.reason_codes.sort();
        draft.reason_codes.dedup();

        if draft.operation.requires_policy_runtime()
            && draft.policy_decision_ref_when_required.is_none()
        {
            return Err(ReceiptError::new(
                "policy-conditioned operations require a policy decision reference",
            ));
        }
        if draft.result.claims_success()
            && draft.operation.receipt_required()
            && receipt_store_mode != StoreMode::Durable
        {
            return Err(ReceiptError::new(
                "a critical transition cannot be claimed successful without a durable receipt path",
            ));
        }
        if draft.operation.mutates_host()
            && draft.result.claims_success()
            && draft.before_state == draft.after_state
        {
            return Err(ReceiptError::new(
                "a completed host mutation must record a changed authoritative state",
            ));
        }
        if draft.result == ReceiptResult::RecoveryRequired
            && draft.recovery_or_rollback_token_when_applicable.is_none()
        {
            return Err(ReceiptError::new(
                "recovery_required receipts require a recovery or rollback token",
            ));
        }

        let canonical = canonical_body(&draft);
        let receipt_id = format!("node-receipt-{}", stable_fingerprint(&canonical));
        Ok(Self {
            receipt_id,
            request_id: draft.request_id,
            operation: draft.operation,
            authenticated_caller: draft.authenticated_caller,
            profile_context_ref: draft.profile_context_ref,
            policy_decision_ref_when_required: draft.policy_decision_ref_when_required,
            before_state: draft.before_state,
            after_state: draft.after_state,
            artifact_or_target_identities: draft.artifact_or_target_identities,
            result: draft.result,
            reason_codes: draft.reason_codes,
            started_at: draft.started_at,
            completed_at: draft.completed_at,
            duration_millis: draft.duration_millis,
            recovery_or_rollback_token_when_applicable: draft
                .recovery_or_rollback_token_when_applicable,
            correlation_id: draft.correlation_id,
        })
    }

    pub fn to_json(&self, view: ReceiptView) -> String {
        let mut fields = vec![
            format!("\"receipt_id\":{}", quote(&self.receipt_id)),
            format!("\"request_id\":{}", quote(&self.request_id)),
            format!("\"operation\":{}", quote(self.operation.as_str())),
            format!(
                "\"authenticated_caller\":{}",
                quote(&self.authenticated_caller)
            ),
            format!(
                "\"profile_context_ref\":{}",
                quote(&self.profile_context_ref)
            ),
            format!("\"before_state\":{}", map_json(&self.before_state)),
            format!("\"after_state\":{}", map_json(&self.after_state)),
            format!(
                "\"artifact_or_target_identities\":{}",
                string_array(
                    self.artifact_or_target_identities
                        .iter()
                        .map(String::as_str)
                )
            ),
            format!("\"result\":{}", quote(self.result.as_str())),
            format!(
                "\"reason_codes\":{}",
                string_array(self.reason_codes.iter().map(String::as_str))
            ),
            format!("\"started_at\":{}", quote(&self.started_at)),
            format!("\"completed_at\":{}", quote(&self.completed_at)),
            format!("\"duration\":{}", self.duration_millis),
            format!("\"correlation_id\":{}", quote(&self.correlation_id)),
        ];
        if view == ReceiptView::Operational {
            fields.push(format!(
                "\"policy_decision_ref_when_required\":{}",
                optional_string(self.policy_decision_ref_when_required.as_deref())
            ));
            fields.push(format!(
                "\"recovery_or_rollback_token_when_applicable\":{}",
                optional_string(self.recovery_or_rollback_token_when_applicable.as_deref())
            ));
        }
        format!("{{{}}}", fields.join(","))
    }
}

fn canonical_body(draft: &ReceiptDraft) -> String {
    [
        draft.request_id.clone(),
        draft.operation.as_str().to_owned(),
        draft.authenticated_caller.clone(),
        draft.profile_context_ref.clone(),
        draft
            .policy_decision_ref_when_required
            .clone()
            .unwrap_or_default(),
        map_json(&draft.before_state),
        map_json(&draft.after_state),
        draft.artifact_or_target_identities.join("\u{001f}"),
        draft.result.as_str().to_owned(),
        draft.reason_codes.join("\u{001f}"),
        draft.started_at.clone(),
        draft.completed_at.clone(),
        draft.duration_millis.to_string(),
        draft
            .recovery_or_rollback_token_when_applicable
            .clone()
            .unwrap_or_default(),
        draft.correlation_id.clone(),
    ]
    .join("\u{001e}")
}

fn stable_fingerprint(value: &str) -> String {
    fn fnv1a(seed: u64, bytes: impl Iterator<Item = u8>) -> u64 {
        bytes.fold(seed, |hash, byte| {
            (hash ^ u64::from(byte)).wrapping_mul(0x0000_0100_0000_01b3)
        })
    }
    let first = fnv1a(0xcbf2_9ce4_8422_2325, value.bytes());
    let second = fnv1a(0x8422_2325_cbf2_9ce4, value.bytes().rev());
    format!("{first:016x}{second:016x}")
}

fn validate_identifier(value: &str, name: &str) -> Result<(), ReceiptError> {
    if value.is_empty() || value.len() > 512 {
        return Err(ReceiptError::new(format!(
            "{name} must be a bounded non-empty identifier"
        )));
    }
    if contains_secret_marker(value) {
        return Err(ReceiptError::new(format!(
            "{name} contains prohibited secret-like material"
        )));
    }
    if value.chars().any(char::is_control) {
        return Err(ReceiptError::new(format!(
            "{name} cannot contain control characters"
        )));
    }
    Ok(())
}

fn validate_optional_identifier(value: Option<&str>, name: &str) -> Result<(), ReceiptError> {
    if let Some(value) = value {
        validate_identifier(value, name)?;
    }
    Ok(())
}

fn validate_profile_ref(value: &str) -> Result<(), ReceiptError> {
    validate_identifier(value, "profile_context_ref")?;
    if !value.starts_with("contracts/profiles/") || !value.ends_with(".profile.json") {
        return Err(ReceiptError::new(
            "profile_context_ref must reference contracts/profiles/*.profile.json",
        ));
    }
    Ok(())
}

fn validate_timestamp(value: &str, name: &str) -> Result<(), ReceiptError> {
    if value.len() < 20
        || !value.contains('T')
        || !(value.ends_with('Z')
            || value
                .get(11..)
                .is_some_and(|suffix| suffix.contains('+') || suffix.contains('-')))
    {
        return Err(ReceiptError::new(format!(
            "{name} must be an explicit RFC 3339 timestamp"
        )));
    }
    Ok(())
}

fn validate_reason_code(value: &str) -> Result<(), ReceiptError> {
    if value.is_empty()
        || value.len() > 128
        || !value.chars().all(|character| {
            character.is_ascii_uppercase() || character.is_ascii_digit() || character == '_'
        })
    {
        return Err(ReceiptError::new(
            "reason codes must be bounded upper-snake-case identifiers",
        ));
    }
    Ok(())
}

fn validate_state(state: &BTreeMap<String, String>, name: &str) -> Result<(), ReceiptError> {
    if state.len() > 128 {
        return Err(ReceiptError::new(format!(
            "{name} exceeds the bounded field limit"
        )));
    }
    for (key, value) in state {
        validate_identifier(key, &format!("{name} key"))?;
        validate_identifier(value, &format!("{name} value"))?;
    }
    Ok(())
}

fn contains_secret_marker(value: &str) -> bool {
    let lowercase = value.to_ascii_lowercase();
    [
        "private_key",
        "passphrase",
        "password=",
        "secret=",
        "token=",
        "credential=",
        "key_material",
    ]
    .iter()
    .any(|marker| lowercase.contains(marker))
}

fn map_json(map: &BTreeMap<String, String>) -> String {
    let values = map
        .iter()
        .map(|(key, value)| format!("{}:{}", quote(key), quote(value)))
        .collect::<Vec<_>>()
        .join(",");
    format!("{{{values}}}")
}

fn string_array<'a>(values: impl IntoIterator<Item = &'a str>) -> String {
    format!(
        "[{}]",
        values.into_iter().map(quote).collect::<Vec<_>>().join(",")
    )
}

fn optional_string(value: Option<&str>) -> String {
    value.map(quote).unwrap_or_else(|| "null".to_owned())
}

fn quote(value: &str) -> String {
    let mut output = String::with_capacity(value.len() + 2);
    output.push('"');
    for character in value.chars() {
        match character {
            '"' => output.push_str("\\\""),
            '\\' => output.push_str("\\\\"),
            '\n' => output.push_str("\\n"),
            '\r' => output.push_str("\\r"),
            '\t' => output.push_str("\\t"),
            character if character.is_control() => {
                output.push_str(&format!("\\u{:04x}", character as u32));
            },
            character => output.push(character),
        }
    }
    output.push('"');
    output
}

#[cfg(test)]
mod tests {
    use super::*;

    fn completed_draft() -> ReceiptDraft {
        ReceiptDraft {
            request_id: "request-1".to_owned(),
            operation: OperationClass::ActivateSystemArtifact,
            authenticated_caller: "component:lifecycle".to_owned(),
            profile_context_ref: "contracts/profiles/sovereign-linux-node.profile.json".to_owned(),
            policy_decision_ref_when_required: Some("decision:123".to_owned()),
            before_state: BTreeMap::from([("active_slot".to_owned(), "slot-a".to_owned())]),
            after_state: BTreeMap::from([("active_slot".to_owned(), "slot-b".to_owned())]),
            artifact_or_target_identities: vec!["artifact:system:abc".to_owned()],
            result: ReceiptResult::Completed,
            reason_codes: Vec::new(),
            started_at: "2026-08-06T12:00:00Z".to_owned(),
            completed_at: "2026-08-06T12:00:05Z".to_owned(),
            duration_millis: 5_000,
            recovery_or_rollback_token_when_applicable: Some("recovery:slot-a".to_owned()),
            correlation_id: "correlation-1".to_owned(),
        }
    }

    #[test]
    fn completed_critical_transition_requires_durable_receipt_path() {
        let result = NodeOperationReceipt::from_draft(completed_draft(), StoreMode::Buffered);
        assert!(result.is_err());
    }

    #[test]
    fn receipt_identifier_is_deterministic() {
        let first = NodeOperationReceipt::from_draft(completed_draft(), StoreMode::Durable)
            .expect("valid receipt");
        let second = NodeOperationReceipt::from_draft(completed_draft(), StoreMode::Durable)
            .expect("valid receipt");
        assert_eq!(first.receipt_id, second.receipt_id);
        assert_eq!(
            first.to_json(ReceiptView::Operational),
            second.to_json(ReceiptView::Operational)
        );
    }

    #[test]
    fn policy_conditioned_operation_requires_decision_reference() {
        let mut draft = completed_draft();
        draft.policy_decision_ref_when_required = None;
        assert!(NodeOperationReceipt::from_draft(draft, StoreMode::Durable).is_err());
    }

    #[test]
    fn recovery_required_result_requires_token() {
        let mut draft = completed_draft();
        draft.result = ReceiptResult::RecoveryRequired;
        draft.recovery_or_rollback_token_when_applicable = None;
        assert!(NodeOperationReceipt::from_draft(draft, StoreMode::Durable).is_err());
    }

    #[test]
    fn public_view_omits_policy_and_recovery_references() {
        let receipt = NodeOperationReceipt::from_draft(completed_draft(), StoreMode::Durable)
            .expect("valid receipt");
        let public = receipt.to_json(ReceiptView::Public);
        assert!(!public.contains("decision:123"));
        assert!(!public.contains("recovery:slot-a"));
    }
}
