use crate::{
    BindingValidationError, CapabilityAvailability, require_non_empty, schema,
    validate_non_empty_values,
};
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::collections::BTreeMap;

/// Shared operational-state vocabulary.
#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum OperationalState {
    Starting,
    Healthy,
    Constrained,
    ReadOnly,
    AdvisoryOnly,
    Degraded,
    Unavailable,
    Recovering,
    Maintenance,
    Stopping,
    Failed,
}

/// Work-specific readiness classes. Liveness is intentionally not one of them.
#[derive(Clone, Copy, Debug, Deserialize, Eq, Ord, PartialEq, PartialOrd, Serialize)]
pub enum ReadinessClass {
    #[serde(rename = "readiness.local_read")]
    LocalRead,
    #[serde(rename = "readiness.authoritative_write")]
    AuthoritativeWrite,
    #[serde(rename = "readiness.background_work")]
    BackgroundWork,
    #[serde(rename = "readiness.publication")]
    Publication,
    #[serde(rename = "readiness.activation")]
    Activation,
    #[serde(rename = "readiness.recovery")]
    Recovery,
}

#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum ReadinessStatus {
    Ready,
    Constrained,
    ReadOnly,
    AdvisoryOnly,
    Blocked,
    Unavailable,
}

#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum DependencyRequirement {
    RequiredForComponent,
    RequiredForCapability,
    Conditional,
    Optional,
    ExternalIntegrationOnly,
}

#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum DependencyState {
    Available,
    Constrained,
    Stale,
    Unavailable,
    Unknown,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct DependencyHealth {
    pub dependency_ref: String,
    pub requirement: DependencyRequirement,
    pub state: DependencyState,
    pub observed_at: String,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub reason_codes: Vec<String>,
}

impl DependencyHealth {
    pub fn validate(&self) -> Result<(), BindingValidationError> {
        require_non_empty("dependency_ref", &self.dependency_ref)?;
        require_non_empty("observed_at", &self.observed_at)?;
        validate_non_empty_values("reason_codes", &self.reason_codes)
    }
}

#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum StalenessState {
    Current,
    ApproachingLimit,
    Stale,
    Unknown,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct Freshness {
    pub source: String,
    pub observed_at: String,
    pub expected_refresh_seconds: u64,
    pub age_seconds: u64,
    pub staleness: StalenessState,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub effect_on_capability: Option<String>,
}

impl Freshness {
    pub fn validate(&self) -> Result<(), BindingValidationError> {
        require_non_empty("source", &self.source)?;
        require_non_empty("observed_at", &self.observed_at)?;
        if let Some(effect) = &self.effect_on_capability {
            require_non_empty("effect_on_capability", effect)?;
        }
        Ok(())
    }
}

/// Capability-specific readiness vector.
#[derive(Clone, Debug, Deserialize, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct CapabilityReadiness {
    pub schema: String,
    pub schema_version: String,
    pub capability_id: String,
    pub owner_component_id: String,
    pub availability: CapabilityAvailability,
    pub observed_state: OperationalState,
    pub observed_at: String,
    pub readiness: BTreeMap<ReadinessClass, ReadinessStatus>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub usable_operation_classes: Vec<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub denied_operation_classes: Vec<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub dependencies: Vec<DependencyHealth>,
    pub active_contract_id: String,
    pub active_contract_version: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub active_schema_version: Option<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub active_artifact_refs: Vec<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub reason_codes: Vec<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub recovery_conditions: Vec<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub evidence_refs: Vec<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub freshness: Vec<Freshness>,
}

impl CapabilityReadiness {
    pub fn validate(&self) -> Result<(), BindingValidationError> {
        if self.schema != schema::READINESS {
            return Err(BindingValidationError::new(
                "schema",
                "must identify the common readiness schema",
            ));
        }
        require_non_empty("schema_version", &self.schema_version)?;
        require_non_empty("capability_id", &self.capability_id)?;
        require_non_empty("owner_component_id", &self.owner_component_id)?;
        require_non_empty("observed_at", &self.observed_at)?;
        require_non_empty("active_contract_id", &self.active_contract_id)?;
        require_non_empty("active_contract_version", &self.active_contract_version)?;
        if let Some(version) = &self.active_schema_version {
            require_non_empty("active_schema_version", version)?;
        }
        validate_non_empty_values("usable_operation_classes", &self.usable_operation_classes)?;
        validate_non_empty_values("denied_operation_classes", &self.denied_operation_classes)?;
        validate_non_empty_values("active_artifact_refs", &self.active_artifact_refs)?;
        validate_non_empty_values("reason_codes", &self.reason_codes)?;
        validate_non_empty_values("recovery_conditions", &self.recovery_conditions)?;
        validate_non_empty_values("evidence_refs", &self.evidence_refs)?;
        for dependency in &self.dependencies {
            dependency.validate()?;
        }
        for freshness in &self.freshness {
            freshness.validate()?;
        }
        Ok(())
    }
}

/// Process-level liveness is intentionally separate from work readiness.
#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum HealthLivenessState {
    Alive,
    Stopping,
    Failed,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct HealthLiveness {
    pub state: HealthLivenessState,
    pub observed_at: String,
    pub reason_codes: Vec<String>,
}

impl HealthLiveness {
    pub fn validate(&self) -> Result<(), BindingValidationError> {
        require_non_empty("process_liveness.observed_at", &self.observed_at)?;
        validate_non_empty_values("process_liveness.reason_codes", &self.reason_codes)?;
        if matches!(
            self.state,
            HealthLivenessState::Stopping | HealthLivenessState::Failed
        ) && self.reason_codes.is_empty()
        {
            return Err(BindingValidationError::new(
                "process_liveness.reason_codes",
                "must identify why a non-alive process state was reported",
            ));
        }
        Ok(())
    }
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct HealthStartup {
    pub state: OperationalState,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub stage: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub started_at: Option<String>,
    pub observed_at: String,
    pub reason_codes: Vec<String>,
}

impl HealthStartup {
    pub fn validate(&self) -> Result<(), BindingValidationError> {
        require_non_empty("startup.observed_at", &self.observed_at)?;
        if let Some(stage) = &self.stage {
            require_non_empty("startup.stage", stage)?;
        }
        if let Some(started_at) = &self.started_at {
            require_non_empty("startup.started_at", started_at)?;
        }
        validate_non_empty_values("startup.reason_codes", &self.reason_codes)?;
        if self.state != OperationalState::Healthy && self.reason_codes.is_empty() {
            return Err(BindingValidationError::new(
                "startup.reason_codes",
                "must identify why startup is not healthy",
            ));
        }
        Ok(())
    }
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct HealthLimitation {
    pub capability_id: String,
    pub state: OperationalState,
    pub reason_codes: Vec<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub denied_operation_classes: Vec<String>,
}

impl HealthLimitation {
    pub fn validate(&self) -> Result<(), BindingValidationError> {
        require_non_empty("limitations.capability_id", &self.capability_id)?;
        if self.reason_codes.is_empty() {
            return Err(BindingValidationError::new(
                "limitations.reason_codes",
                "must contain at least one reason code",
            ));
        }
        validate_non_empty_values("limitations.reason_codes", &self.reason_codes)?;
        validate_non_empty_values(
            "limitations.denied_operation_classes",
            &self.denied_operation_classes,
        )
    }
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct HealthFreshness {
    pub source: String,
    pub confidence: String,
    pub staleness_state: String,
    pub observed_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub valid_until: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub expected_refresh_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub age_seconds: Option<u64>,
}

impl HealthFreshness {
    pub fn validate(&self) -> Result<(), BindingValidationError> {
        require_non_empty("freshness.source", &self.source)?;
        require_non_empty("freshness.observed_at", &self.observed_at)?;
        if !matches!(
            self.confidence.as_str(),
            "direct" | "derived" | "reported" | "unknown"
        ) {
            return Err(BindingValidationError::new(
                "freshness.confidence",
                "must be direct, derived, reported, or unknown",
            ));
        }
        if !matches!(
            self.staleness_state.as_str(),
            "current" | "stale" | "unknown"
        ) {
            return Err(BindingValidationError::new(
                "freshness.staleness_state",
                "must be current, stale, or unknown",
            ));
        }
        if let Some(value) = &self.valid_until {
            require_non_empty("freshness.valid_until", value)?;
        }
        if let Some(value) = &self.expected_refresh_at {
            require_non_empty("freshness.expected_refresh_at", value)?;
        }
        Ok(())
    }
}

/// Canonical component-level health vector.  Readiness entries remain opaque
/// here because their schema is independently owned by readiness.schema.json.
#[derive(Clone, Debug, Deserialize, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct HealthStatus {
    pub schema_version: String,
    pub health_report_id: String,
    pub component_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub component_instance_id: Option<String>,
    pub component_contract_ref: String,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub profile_refs: Vec<String>,
    pub process_liveness: HealthLiveness,
    pub startup: HealthStartup,
    pub overall_state: OperationalState,
    pub readiness: Vec<Value>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub limitations: Vec<HealthLimitation>,
    pub freshness: HealthFreshness,
    pub observed_at: String,
    pub reason_codes: Vec<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub recovery_conditions: Vec<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub evidence_refs: Vec<String>,
    pub disclosure_class: String,
}

impl HealthStatus {
    pub fn validate(&self) -> Result<(), BindingValidationError> {
        require_non_empty("schema_version", &self.schema_version)?;
        require_non_empty("health_report_id", &self.health_report_id)?;
        if !self.health_report_id.starts_with("health:") {
            return Err(BindingValidationError::new(
                "health_report_id",
                "must start with health:",
            ));
        }
        require_non_empty("component_id", &self.component_id)?;
        if let Some(instance_id) = &self.component_instance_id {
            require_non_empty("component_instance_id", instance_id)?;
        }
        require_non_empty("component_contract_ref", &self.component_contract_ref)?;
        require_non_empty("observed_at", &self.observed_at)?;
        validate_non_empty_values("profile_refs", &self.profile_refs)?;
        validate_non_empty_values("reason_codes", &self.reason_codes)?;
        validate_non_empty_values("recovery_conditions", &self.recovery_conditions)?;
        validate_non_empty_values("evidence_refs", &self.evidence_refs)?;

        self.process_liveness.validate()?;
        self.startup.validate()?;
        self.freshness.validate()?;
        for limitation in &self.limitations {
            limitation.validate()?;
        }
        if self.readiness.is_empty() {
            return Err(BindingValidationError::new(
                "readiness",
                "must contain at least one readiness result",
            ));
        }
        if self.readiness.iter().any(|item| !item.is_object()) {
            return Err(BindingValidationError::new(
                "readiness",
                "must contain JSON objects",
            ));
        }
        match self.process_liveness.state {
            HealthLivenessState::Failed if self.overall_state != OperationalState::Failed => {
                return Err(BindingValidationError::new(
                    "overall_state",
                    "failed liveness requires failed aggregate state",
                ));
            },
            HealthLivenessState::Stopping if self.overall_state != OperationalState::Stopping => {
                return Err(BindingValidationError::new(
                    "overall_state",
                    "stopping liveness requires stopping aggregate state",
                ));
            },
            _ => {},
        }
        if self.overall_state != OperationalState::Healthy && self.reason_codes.is_empty() {
            return Err(BindingValidationError::new(
                "reason_codes",
                "non-healthy aggregate state requires a reason code",
            ));
        }
        if self.freshness.staleness_state == "stale"
            && self.overall_state == OperationalState::Healthy
        {
            return Err(BindingValidationError::new(
                "overall_state",
                "stale freshness cannot report healthy aggregate state",
            ));
        }
        if !matches!(
            self.disclosure_class.as_str(),
            "minimal_public"
                | "authenticated_operational"
                | "restricted_diagnostic"
                | "machine_readable_local"
        ) {
            return Err(BindingValidationError::new(
                "disclosure_class",
                "unsupported disclosure class",
            ));
        }
        Ok(())
    }
}
