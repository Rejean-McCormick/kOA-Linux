//! Bounded health and readiness evaluation for the kOA Node Agent.

use crate::config::{
    DependencyMode, NodeAgentConfig, OperationClass, RecoveryPathState, ResourcePressureState,
    StagingCapacityState, StoreMode, COMPONENT_ID,
};
use std::collections::{BTreeMap, BTreeSet};

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum CheckState {
    Pass,
    Degraded,
    Fail,
    Unknown,
}

impl CheckState {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::Pass => "pass",
            Self::Degraded => "degraded",
            Self::Fail => "fail",
            Self::Unknown => "unknown",
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ComponentState {
    Uninitialized,
    Starting,
    Ready,
    Degraded,
    InspectionOnly,
    Activating,
    Recovering,
    Stopping,
    Unavailable,
}

impl ComponentState {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::Uninitialized => "uninitialized",
            Self::Starting => "starting",
            Self::Ready => "ready",
            Self::Degraded => "degraded",
            Self::InspectionOnly => "inspection_only",
            Self::Activating => "activating",
            Self::Recovering => "recovering",
            Self::Stopping => "stopping",
            Self::Unavailable => "unavailable",
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CheckResult {
    pub check_id: String,
    pub state: CheckState,
    pub reason_code: Option<String>,
}

impl CheckResult {
    pub fn pass(check_id: impl Into<String>) -> Self {
        Self {
            check_id: check_id.into(),
            state: CheckState::Pass,
            reason_code: None,
        }
    }

    pub fn non_passing(
        check_id: impl Into<String>,
        state: CheckState,
        reason_code: impl Into<String>,
    ) -> Self {
        assert!(state != CheckState::Pass, "use CheckResult::pass");
        Self {
            check_id: check_id.into(),
            state,
            reason_code: Some(reason_code.into()),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RuntimeEvidence {
    pub configuration_valid: bool,
    pub component_identity_available: bool,
    pub operation_registry_valid: bool,
    pub query_interface_ready: bool,
    pub active_request_id: Option<String>,
    pub active_operation_class: Option<OperationClass>,
    pub recovering: bool,
    pub stopping: bool,
    pub last_successful_critical_transition_at: Option<String>,
}

impl Default for RuntimeEvidence {
    fn default() -> Self {
        Self {
            configuration_valid: true,
            component_identity_available: true,
            operation_registry_valid: true,
            query_interface_ready: true,
            active_request_id: None,
            active_operation_class: None,
            recovering: false,
            stopping: false,
            last_successful_critical_transition_at: None,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct HealthSnapshot {
    pub component_id: &'static str,
    pub instance_id: String,
    pub component_state: ComponentState,
    pub liveness: &'static str,
    pub health: &'static str,
    pub readiness: &'static str,
    pub enabled_operation_classes: Vec<OperationClass>,
    pub blocked_operation_classes: Vec<OperationClass>,
    pub active_request_id: Option<String>,
    pub active_operation_class: Option<OperationClass>,
    pub staging_capacity_state: StagingCapacityState,
    pub receipt_queue_state: StoreMode,
    pub idempotency_store_state: StoreMode,
    pub artifact_verification_state: DependencyMode,
    pub recovery_path_state: RecoveryPathState,
    pub resource_pressure_state: ResourcePressureState,
    pub last_successful_critical_transition_at: Option<String>,
    pub critical_transitions_ready: bool,
    pub checks: BTreeMap<String, CheckResult>,
    pub reason_codes: Vec<String>,
}

impl HealthSnapshot {
    pub fn to_json(&self, operational_view: bool) -> String {
        let mut fields = Vec::new();
        fields.push(format!("\"component_id\":{}", quote(self.component_id)));
        fields.push(format!(
            "\"component_state\":{}",
            quote(self.component_state.as_str())
        ));
        fields.push(format!("\"liveness\":{}", quote(self.liveness)));
        fields.push(format!("\"health\":{}", quote(self.health)));
        fields.push(format!("\"readiness\":{}", quote(self.readiness)));
        fields.push(format!(
            "\"enabled_operation_classes\":{}",
            string_array(
                self.enabled_operation_classes
                    .iter()
                    .map(|operation| operation.as_str())
            )
        ));
        fields.push(format!(
            "\"blocked_operation_classes\":{}",
            string_array(
                self.blocked_operation_classes
                    .iter()
                    .map(|operation| operation.as_str())
            )
        ));
        fields.push(format!(
            "\"staging_capacity_state\":{}",
            quote(self.staging_capacity_state.as_str())
        ));
        fields.push(format!(
            "\"receipt_queue_state\":{}",
            quote(self.receipt_queue_state.as_str())
        ));
        fields.push(format!(
            "\"idempotency_store_state\":{}",
            quote(self.idempotency_store_state.as_str())
        ));
        fields.push(format!(
            "\"artifact_verification_state\":{}",
            quote(self.artifact_verification_state.as_str())
        ));
        fields.push(format!(
            "\"recovery_path_state\":{}",
            quote(self.recovery_path_state.as_str())
        ));
        fields.push(format!(
            "\"resource_pressure_state\":{}",
            quote(self.resource_pressure_state.as_str())
        ));
        fields.push(format!(
            "\"critical_transitions_ready\":{}",
            self.critical_transitions_ready
        ));
        fields.push(format!(
            "\"reason_codes\":{}",
            string_array(self.reason_codes.iter().map(String::as_str))
        ));

        if operational_view {
            fields.push(format!("\"instance_id\":{}", quote(&self.instance_id)));
            fields.push(format!(
                "\"active_request_id\":{}",
                optional_string(self.active_request_id.as_deref())
            ));
            fields.push(format!(
                "\"active_operation_class\":{}",
                optional_string(self.active_operation_class.map(OperationClass::as_str))
            ));
            fields.push(format!(
                "\"last_successful_critical_transition_at\":{}",
                optional_string(self.last_successful_critical_transition_at.as_deref())
            ));
            let checks = self
                .checks
                .iter()
                .map(|(key, result)| {
                    format!(
                        "{}:{{\"state\":{},\"reason_code\":{}}}",
                        quote(key),
                        quote(result.state.as_str()),
                        optional_string(result.reason_code.as_deref())
                    )
                })
                .collect::<Vec<_>>()
                .join(",");
            fields.push(format!("\"checks\":{{{checks}}}"));
        }
        format!("{{{}}}", fields.join(","))
    }
}

pub fn evaluate_health(config: &NodeAgentConfig, evidence: &RuntimeEvidence) -> HealthSnapshot {
    let mut checks = BTreeMap::new();
    insert_boolean_check(
        &mut checks,
        "configuration_valid",
        evidence.configuration_valid,
        "CONFIGURATION_INVALID",
    );
    insert_boolean_check(
        &mut checks,
        "component_identity_available",
        evidence.component_identity_available,
        "COMPONENT_IDENTITY_UNAVAILABLE",
    );
    insert_boolean_check(
        &mut checks,
        "operation_registry_valid",
        evidence.operation_registry_valid,
        "OPERATION_REGISTRY_INVALID",
    );
    insert_boolean_check(
        &mut checks,
        "query_interface_ready",
        evidence.query_interface_ready,
        "QUERY_INTERFACE_NOT_READY",
    );
    insert_dependency_check(
        &mut checks,
        "identity_verification_ready",
        config.identity_verification_mode,
        "IDENTITY_VERIFICATION",
    );
    insert_dependency_check(
        &mut checks,
        "profile_validation_ready",
        config.profile_validation_mode,
        "PROFILE_VALIDATION",
    );
    insert_dependency_check(
        &mut checks,
        "artifact_verification_ready_for_enabled_operations",
        config.artifact_verification_mode,
        "ARTIFACT_VERIFICATION",
    );
    insert_store_check(
        &mut checks,
        "receipt_generation_ready",
        config.receipt_store_mode,
        "RECEIPT_STORE",
    );
    insert_store_check(
        &mut checks,
        "idempotency_store_available",
        config.idempotency_store_mode,
        "IDEMPOTENCY_STORE",
    );
    insert_recovery_check(&mut checks, config.recovery_path_state);
    insert_dependency_check(
        &mut checks,
        "resource_envelope_active",
        config.resource_envelope_mode,
        "RESOURCE_ENVELOPE",
    );

    let enabled: Vec<_> = config.enabled_operation_classes.iter().copied().collect();
    let blocked: Vec<_> = enabled
        .iter()
        .copied()
        .filter(|operation| operation_is_blocked(*operation, config, evidence))
        .collect();
    let critical_transitions_ready = config.critical_transitions_configured()
        && evidence.configuration_valid
        && evidence.component_identity_available
        && evidence.operation_registry_valid
        && config.identity_verification_mode == DependencyMode::Available
        && config.profile_validation_mode == DependencyMode::Available
        && config.policy_runtime_mode == DependencyMode::Available
        && config.artifact_verification_mode == DependencyMode::Available
        && config.staging_capacity_state == StagingCapacityState::Available
        && config.resource_pressure_state == ResourcePressureState::Normal;

    let core_failed = !evidence.configuration_valid
        || !evidence.component_identity_available
        || !evidence.operation_registry_valid
        || !evidence.query_interface_ready;
    let inspection_enabled = config
        .enabled_operation_classes
        .contains(&OperationClass::InspectNodeState);
    let component_state = if evidence.stopping {
        ComponentState::Stopping
    } else if evidence.recovering {
        ComponentState::Recovering
    } else if evidence.active_operation_class.is_some() {
        ComponentState::Activating
    } else if core_failed {
        ComponentState::Unavailable
    } else if enabled.is_empty() {
        ComponentState::Uninitialized
    } else if blocked.is_empty() && critical_transitions_ready {
        ComponentState::Ready
    } else if inspection_enabled && !operation_is_blocked(OperationClass::InspectNodeState, config, evidence) {
        ComponentState::InspectionOnly
    } else {
        ComponentState::Degraded
    };

    let health = if core_failed {
        "failed"
    } else if checks.values().any(|check| {
        matches!(check.state, CheckState::Degraded | CheckState::Fail | CheckState::Unknown)
    }) || config.resource_pressure_state != ResourcePressureState::Normal
    {
        "degraded"
    } else {
        "healthy"
    };
    let readiness = if component_state == ComponentState::Ready {
        "ready"
    } else {
        "not_ready"
    };
    let mut reason_codes: BTreeSet<String> = checks
        .values()
        .filter_map(|check| check.reason_code.clone())
        .collect();
    if !blocked.is_empty() {
        reason_codes.insert("ENABLED_OPERATION_BLOCKED".to_owned());
    }
    if config.control_plane_mode == DependencyMode::Unavailable {
        reason_codes.insert("CONTROL_PLANE_UNAVAILABLE_LOCAL_AUTHORITY_PRESERVED".to_owned());
    }
    if !critical_transitions_ready {
        reason_codes.insert("CRITICAL_TRANSITIONS_NOT_READY".to_owned());
    }
    match config.staging_capacity_state {
        StagingCapacityState::Pressure => {
            reason_codes.insert("STAGING_CAPACITY_PRESSURE".to_owned());
        }
        StagingCapacityState::Exhausted => {
            reason_codes.insert("STAGING_CAPACITY_EXHAUSTED".to_owned());
        }
        StagingCapacityState::Unknown => {
            reason_codes.insert("STAGING_CAPACITY_UNKNOWN".to_owned());
        }
        StagingCapacityState::Available => {}
    }
    match config.resource_pressure_state {
        ResourcePressureState::Constrained => {
            reason_codes.insert("RESOURCE_PRESSURE_CONSTRAINED".to_owned());
        }
        ResourcePressureState::Critical => {
            reason_codes.insert("RESOURCE_PRESSURE_CRITICAL".to_owned());
        }
        ResourcePressureState::Unknown => {
            reason_codes.insert("RESOURCE_PRESSURE_UNKNOWN".to_owned());
        }
        ResourcePressureState::Normal => {}
    }

    HealthSnapshot {
        component_id: COMPONENT_ID,
        instance_id: config.instance_id.clone(),
        component_state,
        liveness: "alive",
        health,
        readiness,
        enabled_operation_classes: enabled,
        blocked_operation_classes: blocked,
        active_request_id: evidence.active_request_id.clone(),
        active_operation_class: evidence.active_operation_class,
        staging_capacity_state: config.staging_capacity_state,
        receipt_queue_state: config.receipt_store_mode,
        idempotency_store_state: config.idempotency_store_mode,
        artifact_verification_state: config.artifact_verification_mode,
        recovery_path_state: config.recovery_path_state,
        resource_pressure_state: config.resource_pressure_state,
        last_successful_critical_transition_at: evidence
            .last_successful_critical_transition_at
            .clone(),
        critical_transitions_ready,
        checks,
        reason_codes: reason_codes.into_iter().collect(),
    }
}

fn operation_is_blocked(
    operation: OperationClass,
    config: &NodeAgentConfig,
    evidence: &RuntimeEvidence,
) -> bool {
    if !evidence.configuration_valid
        || !evidence.component_identity_available
        || !evidence.operation_registry_valid
        || !evidence.query_interface_ready
        || config.identity_verification_mode != DependencyMode::Available
        || config.profile_validation_mode != DependencyMode::Available
    {
        return true;
    }
    if operation.requires_policy_runtime()
        && config.policy_runtime_mode != DependencyMode::Available
    {
        return true;
    }
    if operation.requires_artifact_verification()
        && config.artifact_verification_mode != DependencyMode::Available
    {
        return true;
    }
    if operation.receipt_required() && config.receipt_store_mode != StoreMode::Durable {
        return true;
    }
    if operation.mutates_host()
        && (config.idempotency_store_mode != StoreMode::Durable
            || config.resource_envelope_mode != DependencyMode::Available
            || config.staging_capacity_state != StagingCapacityState::Available
            || config.resource_pressure_state != ResourcePressureState::Normal)
    {
        return true;
    }
    operation.requires_recovery_path()
        && config.recovery_path_state != RecoveryPathState::Verified
}

fn insert_boolean_check(
    checks: &mut BTreeMap<String, CheckResult>,
    check_id: &str,
    passing: bool,
    reason: &str,
) {
    let result = if passing {
        CheckResult::pass(check_id)
    } else {
        CheckResult::non_passing(check_id, CheckState::Fail, reason)
    };
    checks.insert(check_id.to_owned(), result);
}

fn insert_dependency_check(
    checks: &mut BTreeMap<String, CheckResult>,
    check_id: &str,
    mode: DependencyMode,
    reason_prefix: &str,
) {
    let result = match mode {
        DependencyMode::Available => CheckResult::pass(check_id),
        DependencyMode::Degraded => CheckResult::non_passing(
            check_id,
            CheckState::Degraded,
            format!("{reason_prefix}_DEGRADED"),
        ),
        DependencyMode::Unavailable => CheckResult::non_passing(
            check_id,
            CheckState::Fail,
            format!("{reason_prefix}_UNAVAILABLE"),
        ),
    };
    checks.insert(check_id.to_owned(), result);
}

fn insert_store_check(
    checks: &mut BTreeMap<String, CheckResult>,
    check_id: &str,
    mode: StoreMode,
    reason_prefix: &str,
) {
    let result = match mode {
        StoreMode::Durable => CheckResult::pass(check_id),
        StoreMode::ReadOnly | StoreMode::Buffered => CheckResult::non_passing(
            check_id,
            CheckState::Degraded,
            format!("{reason_prefix}_NOT_DURABLE"),
        ),
        StoreMode::Unavailable => CheckResult::non_passing(
            check_id,
            CheckState::Fail,
            format!("{reason_prefix}_UNAVAILABLE"),
        ),
    };
    checks.insert(check_id.to_owned(), result);
}

fn insert_recovery_check(
    checks: &mut BTreeMap<String, CheckResult>,
    state: RecoveryPathState,
) {
    let result = match state {
        RecoveryPathState::Verified => CheckResult::pass("recovery_path_ready_for_mutating_operations"),
        RecoveryPathState::Degraded => CheckResult::non_passing(
            "recovery_path_ready_for_mutating_operations",
            CheckState::Degraded,
            "RECOVERY_PATH_DEGRADED",
        ),
        RecoveryPathState::Unavailable => CheckResult::non_passing(
            "recovery_path_ready_for_mutating_operations",
            CheckState::Fail,
            "RECOVERY_PATH_UNAVAILABLE",
        ),
    };
    checks.insert(result.check_id.clone(), result);
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
            }
            character => output.push(character),
        }
    }
    output.push('"');
    output
}

fn optional_string(value: Option<&str>) -> String {
    value.map(quote).unwrap_or_else(|| "null".to_owned())
}

fn string_array<'a>(values: impl IntoIterator<Item = &'a str>) -> String {
    format!(
        "[{}]",
        values.into_iter().map(quote).collect::<Vec<_>>().join(",")
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::config::NodeAgentConfig;

    fn ready_config() -> NodeAgentConfig {
        NodeAgentConfig::from_toml_str(
            r#"
[koa_node_agent]
profile_context_ref = "contracts/profiles/sovereign-linux-node.profile.json"
enabled_operation_classes = ["inspect_node_state", "activate_system_artifact"]
identity_verification_mode = "available"
profile_validation_mode = "available"
policy_runtime_mode = "available"
artifact_verification_mode = "available"
resource_envelope_mode = "available"
control_plane_mode = "unavailable"
receipt_store_mode = "durable"
idempotency_store_mode = "durable"
staging_capacity_state = "available"
recovery_path_state = "verified"
resource_pressure_state = "normal"
"#,
        )
        .expect("valid config")
    }

    #[test]
    fn ready_when_all_authorities_and_evidence_are_available() {
        let status = evaluate_health(&ready_config(), &RuntimeEvidence::default());
        assert_eq!(status.component_state, ComponentState::Ready);
        assert_eq!(status.readiness, "ready");
        assert!(status.critical_transitions_ready);
        assert!(status.blocked_operation_classes.is_empty());
    }

    #[test]
    fn control_plane_loss_preserves_local_readiness() {
        let status = evaluate_health(&ready_config(), &RuntimeEvidence::default());
        assert_eq!(status.readiness, "ready");
        assert!(status
            .reason_codes
            .contains(&"CONTROL_PLANE_UNAVAILABLE_LOCAL_AUTHORITY_PRESERVED".to_owned()));
    }

    #[test]
    fn missing_receipt_path_blocks_mutation_but_preserves_inspection() {
        let mut config = ready_config();
        config.receipt_store_mode = StoreMode::Unavailable;
        let status = evaluate_health(&config, &RuntimeEvidence::default());
        assert_eq!(status.component_state, ComponentState::InspectionOnly);
        assert!(status
            .blocked_operation_classes
            .contains(&OperationClass::ActivateSystemArtifact));
        assert!(!status
            .blocked_operation_classes
            .contains(&OperationClass::InspectNodeState));
    }

    #[test]
    fn policy_runtime_loss_fails_closed_for_policy_conditioned_operations() {
        let mut config = ready_config();
        config.policy_runtime_mode = DependencyMode::Unavailable;
        let status = evaluate_health(&config, &RuntimeEvidence::default());
        assert_eq!(status.component_state, ComponentState::InspectionOnly);
        assert_eq!(status.readiness, "not_ready");
    }

    #[test]
    fn public_json_does_not_expose_request_identity() {
        let mut evidence = RuntimeEvidence::default();
        evidence.active_request_id = Some("request-sensitive".to_owned());
        let status = evaluate_health(&ready_config(), &evidence);
        assert!(!status.to_json(false).contains("request-sensitive"));
        assert!(status.to_json(true).contains("request-sensitive"));
    }
}
