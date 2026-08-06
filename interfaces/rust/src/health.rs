use crate::{
    require_non_empty, schema, validate_non_empty_values, BindingValidationError,
    CapabilityAvailability,
};
use serde::{Deserialize, Serialize};
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
        validate_non_empty_values(
            "usable_operation_classes",
            &self.usable_operation_classes,
        )?;
        validate_non_empty_values(
            "denied_operation_classes",
            &self.denied_operation_classes,
        )?;
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

/// Component-level health vector. It never derives write readiness from liveness.
#[derive(Clone, Debug, Deserialize, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct HealthStatus {
    pub schema: String,
    pub schema_version: String,
    pub component_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub instance_id: Option<String>,
    pub state: OperationalState,
    pub liveness: bool,
    pub startup_complete: bool,
    pub observed_at: String,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub capabilities: Vec<CapabilityReadiness>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub reason_codes: Vec<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub evidence_refs: Vec<String>,
}

impl HealthStatus {
    pub fn validate(&self) -> Result<(), BindingValidationError> {
        if self.schema != schema::HEALTH_STATUS {
            return Err(BindingValidationError::new(
                "schema",
                "must identify the common health-status schema",
            ));
        }
        require_non_empty("schema_version", &self.schema_version)?;
        require_non_empty("component_id", &self.component_id)?;
        if let Some(instance_id) = &self.instance_id {
            require_non_empty("instance_id", instance_id)?;
        }
        require_non_empty("observed_at", &self.observed_at)?;
        validate_non_empty_values("reason_codes", &self.reason_codes)?;
        validate_non_empty_values("evidence_refs", &self.evidence_refs)?;
        for capability in &self.capabilities {
            capability.validate()?;
        }
        Ok(())
    }
}
