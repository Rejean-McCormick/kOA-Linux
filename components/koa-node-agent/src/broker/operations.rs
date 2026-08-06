//! Admission, idempotency, serialization, execution, and terminal result handling.
//!
//! Host-specific mutation is delegated to a fixed backend supplied by the Node Agent
//! adapter layer. This module never invokes a shell, service manager, package manager,
//! container runtime, device, or filesystem path directly.

use super::catalog::{operation_spec, OperationId, OperationSpec};
use super::sandbox::{SandboxError, SandboxPolicy};
use std::collections::{BTreeMap, BTreeSet};
use std::fmt;
use std::panic::{catch_unwind, AssertUnwindSafe};
use std::str::FromStr;
use std::sync::Mutex;

/// Canonical high-level request accepted by the broker boundary.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct BrokerRequest {
    pub operation: String,
    pub request_id: String,
    pub caller_identity: String,
    pub profile_context_ref: String,
    pub policy_decision_ref_when_required: Option<String>,
    pub artifact_or_target_refs: Vec<String>,
    pub expected_current_state: String,
    pub parameters: BTreeMap<String, String>,
    pub deadline_unix_millis: u64,
    pub correlation_id: String,
}

/// Request after closed-catalog and sandbox validation.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ValidatedRequest {
    pub operation: OperationId,
    pub request_id: String,
    pub caller_identity: String,
    pub profile_context_ref: String,
    pub policy_decision_ref: Option<String>,
    pub artifact_or_target_refs: Vec<String>,
    pub expected_current_state: String,
    pub parameters: BTreeMap<String, String>,
    pub deadline_unix_millis: u64,
    pub correlation_id: String,
    pub canonical_fingerprint: String,
}

impl ValidatedRequest {
    pub fn spec(&self) -> &'static OperationSpec {
        operation_spec(self.operation)
    }
}

/// Terminal and non-terminal states exposed by the command interface.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum BrokerStatus {
    Accepted,
    Completed,
    Rejected,
    Conflict,
    TimedOut,
    Failed,
    RecoveryRequired,
}

impl BrokerStatus {
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

    pub const fn is_terminal(self) -> bool {
        !matches!(self, Self::Accepted)
    }
}

/// Result returned by a fixed, profile-scoped adapter.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum BackendOutcome {
    /// The adapter committed and verified the declared effect.
    Completed {
        verified_after_state: String,
        durable_receipt_ref: Option<String>,
    },
    /// The adapter accepted work that remains explicitly in progress.
    Accepted { operation_ref: String },
    /// The adapter rejected or failed before an unknown host effect could occur.
    Failed { code: String, message: String },
    /// A mutation may have occurred but its actual state is not yet reconciled.
    UnknownEffect { code: String, message: String },
}

/// Narrow implementation boundary for one already validated operation.
pub trait OperationBackend: Send + Sync {
    fn execute(&self, request: &ValidatedRequest) -> BackendOutcome;
}

/// Machine-readable bounded result. It deliberately carries references, not secrets.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct BrokerResult {
    pub status: BrokerStatus,
    pub code: String,
    pub message: String,
    pub request_id: String,
    pub operation: String,
    pub canonical_fingerprint: String,
    pub operation_ref: Option<String>,
    pub verified_after_state: Option<String>,
    pub receipt_ref: Option<String>,
}

impl BrokerResult {
    pub fn to_json(&self) -> String {
        format!(
            "{{\"status\":\"{}\",\"code\":\"{}\",\"message\":\"{}\",\"request_id\":\"{}\",\"operation\":\"{}\",\"canonical_fingerprint\":\"{}\",\"operation_ref\":{},\"verified_after_state\":{},\"receipt_ref\":{}}}",
            self.status.as_str(),
            json_escape(&self.code),
            json_escape(&self.message),
            json_escape(&self.request_id),
            json_escape(&self.operation),
            json_escape(&self.canonical_fingerprint),
            json_option(self.operation_ref.as_deref()),
            json_option(self.verified_after_state.as_deref()),
            json_option(self.receipt_ref.as_deref()),
        )
    }
}

#[derive(Default)]
struct BrokerState {
    records: BTreeMap<String, StoredRecord>,
    active_scopes: BTreeSet<String>,
}

#[derive(Clone, Debug)]
struct StoredRecord {
    fingerprint: String,
    request: ValidatedRequest,
    scopes: BTreeSet<String>,
    result: BrokerResult,
}

/// Closed broker with in-process replay protection and target serialization.
///
/// Durable persistence is supplied by the Node Agent port bundle; this in-memory state
/// prevents duplicate execution within one broker process and never claims persistence
/// across a restart.
pub struct PrivilegedBroker {
    sandbox: SandboxPolicy,
    state: Mutex<BrokerState>,
}

impl Default for PrivilegedBroker {
    fn default() -> Self {
        Self::new(SandboxPolicy::default())
    }
}

impl PrivilegedBroker {
    pub fn new(sandbox: SandboxPolicy) -> Self {
        Self {
            sandbox,
            state: Mutex::new(BrokerState::default()),
        }
    }

    /// Validate and canonicalize without executing a privileged adapter.
    pub fn validate(
        &self,
        request: BrokerRequest,
        now_unix_millis: u64,
    ) -> Result<ValidatedRequest, AdmissionError> {
        let operation = OperationId::from_str(&request.operation)
            .map_err(|_| AdmissionError::new("unknown_operation", "operation is not registered"))?;
        let spec = operation_spec(operation);

        self.sandbox
            .validate_token("request_id", &request.request_id)?;
        self.sandbox
            .validate_token("caller_identity", &request.caller_identity)?;
        self.sandbox
            .validate_profile_reference(&request.profile_context_ref)?;
        self.sandbox
            .validate_token("correlation_id", &request.correlation_id)?;

        if request.deadline_unix_millis <= now_unix_millis {
            return Err(AdmissionError::new(
                "deadline_expired",
                "request deadline has already expired",
            ));
        }

        if request.artifact_or_target_refs.len() < spec.minimum_references
            || request.artifact_or_target_refs.len() > spec.maximum_references
        {
            return Err(AdmissionError::new(
                "invalid_reference_count",
                format!(
                    "{} requires between {} and {} managed references",
                    operation, spec.minimum_references, spec.maximum_references
                ),
            ));
        }
        if request.artifact_or_target_refs.len() > self.sandbox.bounds().maximum_references {
            return Err(AdmissionError::new(
                "too_many_references",
                "request exceeds the global reference bound",
            ));
        }
        for reference in &request.artifact_or_target_refs {
            self.sandbox
                .validate_managed_reference("artifact_or_target_ref", reference)?;
        }

        let policy_required = operation != OperationId::InspectNodeState;
        match request.policy_decision_ref_when_required.as_deref() {
            Some(reference) => self
                .sandbox
                .validate_managed_reference("policy_decision_ref", reference)?,
            None if policy_required => {
                return Err(AdmissionError::new(
                    "policy_decision_required",
                    "this operation requires a bound policy decision reference",
                ));
            }
            None => {}
        }

        if request.expected_current_state.is_empty() {
            return Err(AdmissionError::new(
                "expected_state_required",
                "expected_current_state must be explicit",
            ));
        }
        self.sandbox
            .validate_parameter_value(&request.expected_current_state)?;

        if request.parameters.len() > self.sandbox.bounds().maximum_parameters {
            return Err(AdmissionError::new(
                "too_many_parameters",
                "request exceeds the global parameter bound",
            ));
        }
        let allowed_keys = spec.parameters.allowed_keys();
        for (key, value) in &request.parameters {
            self.sandbox.validate_parameter_key(key)?;
            self.sandbox.validate_parameter_value(value)?;
            if !allowed_keys.contains(&key.as_str()) {
                return Err(AdmissionError::new(
                    "unknown_parameter",
                    format!("parameter {key} is not allowed for {operation}"),
                ));
            }
            if !spec.parameters.validate_value(key, value) {
                return Err(AdmissionError::new(
                    "invalid_parameter_value",
                    format!("parameter {key} has an unregistered value"),
                ));
            }
        }
        for required_key in allowed_keys {
            if !request.parameters.contains_key(*required_key) {
                return Err(AdmissionError::new(
                    "required_parameter_missing",
                    format!("parameter {required_key} is required for {operation}"),
                ));
            }
        }

        let canonical = canonical_request_bytes(&request, operation);
        if canonical.len() > self.sandbox.bounds().maximum_canonical_request_bytes {
            return Err(AdmissionError::new(
                "request_too_large",
                "canonical request exceeds the broker limit",
            ));
        }
        let canonical_fingerprint = stable_fingerprint(&canonical);

        Ok(ValidatedRequest {
            operation,
            request_id: request.request_id,
            caller_identity: request.caller_identity,
            profile_context_ref: request.profile_context_ref,
            policy_decision_ref: request.policy_decision_ref_when_required,
            artifact_or_target_refs: request.artifact_or_target_refs,
            expected_current_state: request.expected_current_state,
            parameters: request.parameters,
            deadline_unix_millis: request.deadline_unix_millis,
            correlation_id: request.correlation_id,
            canonical_fingerprint,
        })
    }

    /// Validate, serialize by target scope, invoke one fixed adapter, and verify the
    /// terminal result contract.
    pub fn execute(
        &self,
        request: BrokerRequest,
        now_unix_millis: u64,
        backend: &dyn OperationBackend,
    ) -> BrokerResult {
        let request_id = request.request_id.clone();
        let operation_text = request.operation.clone();
        let validated = match self.validate(request, now_unix_millis) {
            Ok(validated) => validated,
            Err(error) => {
                return BrokerResult {
                    status: if error.code == "deadline_expired" {
                        BrokerStatus::TimedOut
                    } else {
                        BrokerStatus::Rejected
                    },
                    code: error.code.to_owned(),
                    message: error.message,
                    request_id,
                    operation: operation_text,
                    canonical_fingerprint: String::new(),
                    operation_ref: None,
                    verified_after_state: None,
                    receipt_ref: None,
                };
            }
        };

        let scopes = conflict_scopes(&validated);
        {
            let mut state = self.state.lock().unwrap_or_else(|poisoned| poisoned.into_inner());
            if let Some(record) = state.records.get(&validated.request_id) {
                if record.fingerprint == validated.canonical_fingerprint {
                    return record.result.clone();
                }
                return conflict_result(
                    &validated,
                    "request_identity_conflict",
                    "request identity was already bound to a different canonical body",
                );
            }
            if scopes.iter().any(|scope| state.active_scopes.contains(scope)) {
                return conflict_result(
                    &validated,
                    "target_scope_busy",
                    "a conflicting privileged operation is already active",
                );
            }
            for scope in &scopes {
                state.active_scopes.insert(scope.clone());
            }
        }

        let outcome = catch_unwind(AssertUnwindSafe(|| backend.execute(&validated)));
        let result = match outcome {
            Ok(outcome) => self.translate_outcome(&validated, outcome),
            Err(_) => BrokerResult {
                status: BrokerStatus::Failed,
                code: "adapter_panicked".to_owned(),
                message: "fixed privileged adapter terminated unexpectedly".to_owned(),
                request_id: validated.request_id.clone(),
                operation: validated.operation.to_string(),
                canonical_fingerprint: validated.canonical_fingerprint.clone(),
                operation_ref: None,
                verified_after_state: None,
                receipt_ref: None,
            },
        };

        let mut state = self.state.lock().unwrap_or_else(|poisoned| poisoned.into_inner());
        if result.status.is_terminal() {
            for scope in &scopes {
                state.active_scopes.remove(scope);
            }
        }
        state.records.insert(
            validated.request_id.clone(),
            StoredRecord {
                fingerprint: validated.canonical_fingerprint.clone(),
                request: validated,
                scopes,
                result: result.clone(),
            },
        );
        result
    }

    /// Replace one accepted in-progress result with a verified terminal adapter outcome.
    /// The target scope remains serialized until this method records a terminal state.
    pub fn finalize_accepted(
        &self,
        request_id: &str,
        outcome: BackendOutcome,
    ) -> Result<BrokerResult, AdmissionError> {
        let stored = {
            let state = self.state.lock().unwrap_or_else(|poisoned| poisoned.into_inner());
            state
                .records
                .get(request_id)
                .cloned()
                .ok_or_else(|| AdmissionError::new("request_not_found", "accepted request is unknown"))?
        };
        if stored.result.status != BrokerStatus::Accepted {
            return Err(AdmissionError::new(
                "request_not_accepted",
                "only an accepted in-progress request can be finalized",
            ));
        }

        let result = self.translate_outcome(&stored.request, outcome);
        if !result.status.is_terminal() {
            return Err(AdmissionError::new(
                "terminal_result_required",
                "finalization requires a terminal adapter outcome",
            ));
        }

        let mut state = self.state.lock().unwrap_or_else(|poisoned| poisoned.into_inner());
        let current = state
            .records
            .get(request_id)
            .ok_or_else(|| AdmissionError::new("request_not_found", "accepted request disappeared"))?;
        if current.fingerprint != stored.fingerprint || current.result.status != BrokerStatus::Accepted {
            return Err(AdmissionError::new(
                "request_state_conflict",
                "accepted request changed while it was being finalized",
            ));
        }
        for scope in &stored.scopes {
            state.active_scopes.remove(scope);
        }
        state.records.insert(
            request_id.to_owned(),
            StoredRecord {
                fingerprint: stored.fingerprint,
                request: stored.request,
                scopes: stored.scopes,
                result: result.clone(),
            },
        );
        Ok(result)
    }

    fn translate_outcome(
        &self,
        request: &ValidatedRequest,
        outcome: BackendOutcome,
    ) -> BrokerResult {
        let base = |status, code: &str, message: String| BrokerResult {
            status,
            code: code.to_owned(),
            message,
            request_id: request.request_id.clone(),
            operation: request.operation.to_string(),
            canonical_fingerprint: request.canonical_fingerprint.clone(),
            operation_ref: None,
            verified_after_state: None,
            receipt_ref: None,
        };

        match outcome {
            BackendOutcome::Completed {
                verified_after_state,
                durable_receipt_ref,
            } => {
                if verified_after_state.is_empty() {
                    return base(
                        BrokerStatus::RecoveryRequired,
                        "after_state_unverified",
                        "adapter reported completion without verified after state".to_owned(),
                    );
                }
                if operation_spec(request.operation)
                    .receipt
                    .requires_receipt(&request.parameters)
                    && durable_receipt_ref.is_none()
                {
                    return base(
                        BrokerStatus::RecoveryRequired,
                        "durable_receipt_missing",
                        "critical effect cannot be reported complete without a durable receipt"
                            .to_owned(),
                    );
                }
                BrokerResult {
                    status: BrokerStatus::Completed,
                    code: "completed".to_owned(),
                    message: "adapter effect committed and verified".to_owned(),
                    request_id: request.request_id.clone(),
                    operation: request.operation.to_string(),
                    canonical_fingerprint: request.canonical_fingerprint.clone(),
                    operation_ref: None,
                    verified_after_state: Some(verified_after_state),
                    receipt_ref: durable_receipt_ref,
                }
            }
            BackendOutcome::Accepted { operation_ref } => {
                if operation_ref.is_empty() {
                    return base(
                        BrokerStatus::Failed,
                        "operation_reference_missing",
                        "accepted work requires a bounded operation reference".to_owned(),
                    );
                }
                BrokerResult {
                    status: BrokerStatus::Accepted,
                    code: "accepted".to_owned(),
                    message: "operation accepted; no terminal success is claimed".to_owned(),
                    request_id: request.request_id.clone(),
                    operation: request.operation.to_string(),
                    canonical_fingerprint: request.canonical_fingerprint.clone(),
                    operation_ref: Some(operation_ref),
                    verified_after_state: None,
                    receipt_ref: None,
                }
            }
            BackendOutcome::Failed { code, message } => {
                base(BrokerStatus::Failed, &bounded_code(&code), bounded_message(&message))
            }
            BackendOutcome::UnknownEffect { code, message } => base(
                BrokerStatus::RecoveryRequired,
                &bounded_code(&code),
                bounded_message(&message),
            ),
        }
    }
}

fn conflict_result(request: &ValidatedRequest, code: &str, message: &str) -> BrokerResult {
    BrokerResult {
        status: BrokerStatus::Conflict,
        code: code.to_owned(),
        message: message.to_owned(),
        request_id: request.request_id.clone(),
        operation: request.operation.to_string(),
        canonical_fingerprint: request.canonical_fingerprint.clone(),
        operation_ref: None,
        verified_after_state: None,
        receipt_ref: None,
    }
}

fn conflict_scopes(request: &ValidatedRequest) -> BTreeSet<String> {
    let mut scopes = BTreeSet::new();
    if request.artifact_or_target_refs.is_empty() {
        scopes.insert(format!("operation:{}", request.operation));
    } else {
        for target in &request.artifact_or_target_refs {
            scopes.insert(format!("target:{target}"));
        }
    }
    scopes
}

fn canonical_request_bytes(request: &BrokerRequest, operation: OperationId) -> Vec<u8> {
    let mut output = Vec::new();
    push_field(&mut output, "operation", operation.as_str());
    push_field(&mut output, "request_id", &request.request_id);
    push_field(&mut output, "caller_identity", &request.caller_identity);
    push_field(&mut output, "profile_context_ref", &request.profile_context_ref);
    push_field(
        &mut output,
        "policy_decision_ref",
        request
            .policy_decision_ref_when_required
            .as_deref()
            .unwrap_or(""),
    );
    for reference in &request.artifact_or_target_refs {
        push_field(&mut output, "artifact_or_target_ref", reference);
    }
    push_field(
        &mut output,
        "expected_current_state",
        &request.expected_current_state,
    );
    for (key, value) in &request.parameters {
        push_field(&mut output, key, value);
    }
    push_field(
        &mut output,
        "deadline_unix_millis",
        &request.deadline_unix_millis.to_string(),
    );
    push_field(&mut output, "correlation_id", &request.correlation_id);
    output
}

fn push_field(output: &mut Vec<u8>, key: &str, value: &str) {
    output.extend_from_slice(key.len().to_string().as_bytes());
    output.push(b':');
    output.extend_from_slice(key.as_bytes());
    output.push(b'=');
    output.extend_from_slice(value.len().to_string().as_bytes());
    output.push(b':');
    output.extend_from_slice(value.as_bytes());
    output.push(b'\n');
}

/// Stable FNV-1a fingerprint. This is an idempotency fingerprint, not a signature.
fn stable_fingerprint(bytes: &[u8]) -> String {
    let mut hash = 0xcbf29ce484222325_u64;
    for byte in bytes {
        hash ^= u64::from(*byte);
        hash = hash.wrapping_mul(0x100000001b3);
    }
    format!("fnv1a64:{hash:016x}")
}

fn bounded_code(value: &str) -> String {
    let value = value
        .bytes()
        .filter(|byte| byte.is_ascii_lowercase() || byte.is_ascii_digit() || *byte == b'_')
        .take(64)
        .map(char::from)
        .collect::<String>();
    if value.is_empty() {
        "adapter_failure".to_owned()
    } else {
        value
    }
}

fn bounded_message(value: &str) -> String {
    value
        .chars()
        .filter(|character| !character.is_control())
        .take(512)
        .collect()
}

fn json_option(value: Option<&str>) -> String {
    value
        .map(|value| format!("\"{}\"", json_escape(value)))
        .unwrap_or_else(|| "null".to_owned())
}

fn json_escape(value: &str) -> String {
    let mut escaped = String::with_capacity(value.len());
    for character in value.chars() {
        match character {
            '"' => escaped.push_str("\\\""),
            '\\' => escaped.push_str("\\\\"),
            '\n' => escaped.push_str("\\n"),
            '\r' => escaped.push_str("\\r"),
            '\t' => escaped.push_str("\\t"),
            character if character.is_control() => {
                escaped.push_str(&format!("\\u{:04x}", character as u32));
            }
            character => escaped.push(character),
        }
    }
    escaped
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct AdmissionError {
    pub code: &'static str,
    pub message: String,
}

impl AdmissionError {
    pub fn new(code: &'static str, message: impl Into<String>) -> Self {
        Self {
            code,
            message: message.into(),
        }
    }
}

impl From<SandboxError> for AdmissionError {
    fn from(error: SandboxError) -> Self {
        Self::new(error.code, format!("{}: {}", error.field, error.message))
    }
}

impl fmt::Display for AdmissionError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "{}: {}", self.code, self.message)
    }
}

impl std::error::Error for AdmissionError {}

#[cfg(test)]
mod tests {
    use super::*;

    struct CompletingBackend;

    impl OperationBackend for CompletingBackend {
        fn execute(&self, request: &ValidatedRequest) -> BackendOutcome {
            BackendOutcome::Completed {
                verified_after_state: format!("verified:{}", request.operation),
                durable_receipt_ref: Some(format!("receipt:{}", request.request_id)),
            }
        }
    }

    fn request(operation: &str) -> BrokerRequest {
        let mut parameters = BTreeMap::new();
        let refs = match operation {
            "inspect_node_state" => Vec::new(),
            "manage_knowledge_artifact" => {
                parameters.insert("action".to_owned(), "quarantine".to_owned());
                vec!["artifact:knowledge:example".to_owned()]
            }
            "import_offline_bundle" => {
                parameters.insert("target_state".to_owned(), "quarantine".to_owned());
                vec!["bundle:offline:example".to_owned()]
            }
            "manage_declared_encrypted_volume" => {
                parameters.insert("action".to_owned(), "mount".to_owned());
                vec!["volume:declared:example".to_owned()]
            }
            "restart_allowlisted_service_group" => {
                parameters.insert("critical".to_owned(), "true".to_owned());
                vec!["service-group:example".to_owned()]
            }
            _ => vec!["artifact:example".to_owned()],
        };
        BrokerRequest {
            operation: operation.to_owned(),
            request_id: format!("request-{operation}"),
            caller_identity: "component:test".to_owned(),
            profile_context_ref: "contracts/profiles/sovereign-linux-node.profile.json".to_owned(),
            policy_decision_ref_when_required: if operation == "inspect_node_state" {
                None
            } else {
                Some("decision:policy:example".to_owned())
            },
            artifact_or_target_refs: refs,
            expected_current_state: "state:expected".to_owned(),
            parameters,
            deadline_unix_millis: 2_000,
            correlation_id: "correlation-test".to_owned(),
        }
    }

    #[test]
    fn unknown_operations_and_parameters_fail_closed() {
        let broker = PrivilegedBroker::default();
        let result = broker.execute(request("run_command"), 1_000, &CompletingBackend);
        assert_eq!(result.status, BrokerStatus::Rejected);

        let mut invalid = request("activate_service_bundle");
        invalid.parameters.insert("command".to_owned(), "shutdown".to_owned());
        let result = broker.execute(invalid, 1_000, &CompletingBackend);
        assert_eq!(result.status, BrokerStatus::Rejected);
    }

    #[test]
    fn equivalent_replay_returns_recorded_result_and_changed_body_conflicts() {
        let broker = PrivilegedBroker::default();
        let original = request("activate_service_bundle");
        let first = broker.execute(original.clone(), 1_000, &CompletingBackend);
        let replay = broker.execute(original.clone(), 1_000, &CompletingBackend);
        assert_eq!(first, replay);

        let mut changed = original;
        changed.expected_current_state = "state:different".to_owned();
        let conflict = broker.execute(changed, 1_000, &CompletingBackend);
        assert_eq!(conflict.status, BrokerStatus::Conflict);
    }

    #[test]
    fn terminal_critical_success_requires_a_durable_receipt() {
        struct MissingReceipt;
        impl OperationBackend for MissingReceipt {
            fn execute(&self, _: &ValidatedRequest) -> BackendOutcome {
                BackendOutcome::Completed {
                    verified_after_state: "state:verified".to_owned(),
                    durable_receipt_ref: None,
                }
            }
        }

        let broker = PrivilegedBroker::default();
        let result = broker.execute(
            request("activate_system_artifact"),
            1_000,
            &MissingReceipt,
        );
        assert_eq!(result.status, BrokerStatus::RecoveryRequired);
    }
}
