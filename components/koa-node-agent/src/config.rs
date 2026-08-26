//! Strict, secret-free configuration for the kOA Node Agent.

use std::collections::{BTreeMap, BTreeSet};
use std::env;
use std::error::Error;
use std::fmt;
use std::fs;
use std::path::{Component, Path, PathBuf};
use std::str::FromStr;

pub const COMPONENT_ID: &str = "koa_node_agent";
pub const COMPONENT_VERSION: &str = "1.0.0";
const ENV_PREFIX: &str = "KOA_NODE_AGENT_";

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum DependencyMode {
    Available,
    Degraded,
    Unavailable,
}

impl DependencyMode {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::Available => "available",
            Self::Degraded => "degraded",
            Self::Unavailable => "unavailable",
        }
    }
}

impl FromStr for DependencyMode {
    type Err = ConfigurationError;

    fn from_str(value: &str) -> Result<Self, Self::Err> {
        match value.trim().to_ascii_lowercase().as_str() {
            "available" => Ok(Self::Available),
            "degraded" => Ok(Self::Degraded),
            "unavailable" => Ok(Self::Unavailable),
            _ => Err(ConfigurationError::new(
                "dependency mode must be available, degraded, or unavailable",
            )),
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum StoreMode {
    Durable,
    ReadOnly,
    Buffered,
    Unavailable,
}

impl StoreMode {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::Durable => "durable",
            Self::ReadOnly => "read_only",
            Self::Buffered => "buffered",
            Self::Unavailable => "unavailable",
        }
    }

    pub const fn supports_mutation(self) -> bool {
        matches!(self, Self::Durable)
    }
}

impl FromStr for StoreMode {
    type Err = ConfigurationError;

    fn from_str(value: &str) -> Result<Self, Self::Err> {
        match value.trim().to_ascii_lowercase().as_str() {
            "durable" => Ok(Self::Durable),
            "read_only" => Ok(Self::ReadOnly),
            "buffered" => Ok(Self::Buffered),
            "unavailable" => Ok(Self::Unavailable),
            _ => Err(ConfigurationError::new(
                "store mode must be durable, read_only, buffered, or unavailable",
            )),
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum StagingCapacityState {
    Available,
    Pressure,
    Exhausted,
    Unknown,
}

impl StagingCapacityState {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::Available => "available",
            Self::Pressure => "pressure",
            Self::Exhausted => "exhausted",
            Self::Unknown => "unknown",
        }
    }
}

impl FromStr for StagingCapacityState {
    type Err = ConfigurationError;

    fn from_str(value: &str) -> Result<Self, Self::Err> {
        match value.trim().to_ascii_lowercase().as_str() {
            "available" => Ok(Self::Available),
            "pressure" => Ok(Self::Pressure),
            "exhausted" => Ok(Self::Exhausted),
            "unknown" => Ok(Self::Unknown),
            _ => Err(ConfigurationError::new(
                "staging capacity must be available, pressure, exhausted, or unknown",
            )),
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum RecoveryPathState {
    Verified,
    Degraded,
    Unavailable,
}

impl RecoveryPathState {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::Verified => "verified",
            Self::Degraded => "degraded",
            Self::Unavailable => "unavailable",
        }
    }
}

impl FromStr for RecoveryPathState {
    type Err = ConfigurationError;

    fn from_str(value: &str) -> Result<Self, Self::Err> {
        match value.trim().to_ascii_lowercase().as_str() {
            "verified" => Ok(Self::Verified),
            "degraded" => Ok(Self::Degraded),
            "unavailable" => Ok(Self::Unavailable),
            _ => Err(ConfigurationError::new(
                "recovery path must be verified, degraded, or unavailable",
            )),
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum ResourcePressureState {
    Normal,
    Constrained,
    Critical,
    Unknown,
}

impl ResourcePressureState {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::Normal => "normal",
            Self::Constrained => "constrained",
            Self::Critical => "critical",
            Self::Unknown => "unknown",
        }
    }
}

impl FromStr for ResourcePressureState {
    type Err = ConfigurationError;

    fn from_str(value: &str) -> Result<Self, Self::Err> {
        match value.trim().to_ascii_lowercase().as_str() {
            "normal" => Ok(Self::Normal),
            "constrained" => Ok(Self::Constrained),
            "critical" => Ok(Self::Critical),
            "unknown" => Ok(Self::Unknown),
            _ => Err(ConfigurationError::new(
                "resource pressure must be normal, constrained, critical, or unknown",
            )),
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum OperationClass {
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

impl OperationClass {
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

    pub const fn mutates_host(self) -> bool {
        !matches!(self, Self::InspectNodeState | Self::ExportNodeEvidence)
    }

    pub const fn requires_policy_runtime(self) -> bool {
        !matches!(self, Self::InspectNodeState)
    }

    pub const fn requires_artifact_verification(self) -> bool {
        matches!(
            self,
            Self::StageSystemArtifact
                | Self::ActivateSystemArtifact
                | Self::ActivateServiceBundle
                | Self::ActivateGovernanceBundle
                | Self::ManageKnowledgeArtifact
                | Self::ImportOfflineBundle
                | Self::ExecuteRollbackOrForwardRepair
        )
    }

    pub const fn requires_recovery_path(self) -> bool {
        self.mutates_host()
    }

    pub const fn receipt_required(self) -> bool {
        !matches!(self, Self::InspectNodeState)
    }
}

impl FromStr for OperationClass {
    type Err = ConfigurationError;

    fn from_str(value: &str) -> Result<Self, Self::Err> {
        match value.trim() {
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
            _ => Err(ConfigurationError::new(format!(
                "unknown operation class: {value}"
            ))),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ConfigurationError {
    message: String,
}

impl ConfigurationError {
    pub fn new(message: impl Into<String>) -> Self {
        Self {
            message: message.into(),
        }
    }
}

impl fmt::Display for ConfigurationError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(&self.message)
    }
}

impl Error for ConfigurationError {}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NodeAgentConfig {
    pub instance_id: String,
    pub environment: String,
    pub profile_context_ref: Option<String>,
    pub state_root: PathBuf,
    pub runtime_root: PathBuf,
    pub socket_path: PathBuf,
    pub staging_root: PathBuf,
    pub recovery_root: PathBuf,
    pub enabled_operation_classes: BTreeSet<OperationClass>,
    pub identity_verification_mode: DependencyMode,
    pub profile_validation_mode: DependencyMode,
    pub policy_runtime_mode: DependencyMode,
    pub artifact_verification_mode: DependencyMode,
    pub resource_envelope_mode: DependencyMode,
    pub control_plane_mode: DependencyMode,
    pub receipt_store_mode: StoreMode,
    pub idempotency_store_mode: StoreMode,
    pub staging_capacity_state: StagingCapacityState,
    pub recovery_path_state: RecoveryPathState,
    pub resource_pressure_state: ResourcePressureState,
}

impl Default for NodeAgentConfig {
    fn default() -> Self {
        Self {
            instance_id: "koa-node-agent-1".to_owned(),
            environment: "development".to_owned(),
            profile_context_ref: None,
            state_root: PathBuf::from("/var/lib/koa/node-agent"),
            runtime_root: PathBuf::from("/run/koa/node-agent"),
            socket_path: PathBuf::from("/run/koa/node-agent/node-agent.sock"),
            staging_root: PathBuf::from("/var/lib/koa/node-agent/staging"),
            recovery_root: PathBuf::from("/var/lib/koa/node-agent/recovery"),
            enabled_operation_classes: BTreeSet::new(),
            identity_verification_mode: DependencyMode::Unavailable,
            profile_validation_mode: DependencyMode::Unavailable,
            policy_runtime_mode: DependencyMode::Unavailable,
            artifact_verification_mode: DependencyMode::Unavailable,
            resource_envelope_mode: DependencyMode::Unavailable,
            control_plane_mode: DependencyMode::Unavailable,
            receipt_store_mode: StoreMode::Unavailable,
            idempotency_store_mode: StoreMode::Unavailable,
            staging_capacity_state: StagingCapacityState::Unknown,
            recovery_path_state: RecoveryPathState::Unavailable,
            resource_pressure_state: ResourcePressureState::Unknown,
        }
    }
}

impl NodeAgentConfig {
    pub fn load(path: Option<&Path>) -> Result<Self, ConfigurationError> {
        Self::load_with_environment(path, env::vars())
    }

    pub fn load_with_environment<I, K, V>(
        path: Option<&Path>,
        environment: I,
    ) -> Result<Self, ConfigurationError>
    where
        I: IntoIterator<Item = (K, V)>,
        K: Into<String>,
        V: Into<String>,
    {
        let env_map: BTreeMap<String, String> = environment
            .into_iter()
            .map(|(key, value)| (key.into(), value.into()))
            .collect();
        reject_unknown_environment(&env_map)?;

        let selected_path = match path {
            Some(value) => Some(value.to_path_buf()),
            None => env_map.get("KOA_NODE_AGENT_CONFIG_PATH").map(PathBuf::from),
        };
        if let Some(value) = selected_path.as_deref() {
            validate_absolute_normalized_path(value, "config_path")?;
        }
        let mut config = match selected_path {
            Some(ref value) => {
                let raw = fs::read_to_string(value).map_err(|error| {
                    ConfigurationError::new(format!(
                        "cannot read configuration {}: {error}",
                        value.display()
                    ))
                })?;
                Self::from_toml_str(&raw)?
            },
            None => Self::default(),
        };
        config.apply_environment(&env_map)?;
        config.validate()?;
        Ok(config)
    }

    pub fn from_toml_str(raw: &str) -> Result<Self, ConfigurationError> {
        let values = parse_component_table(raw)?;
        let mut config = Self::default();
        for (key, value) in values {
            config.apply_value(&key, &value, ValueOrigin::Toml)?;
        }
        config.validate()?;
        Ok(config)
    }

    pub fn validate(&self) -> Result<(), ConfigurationError> {
        validate_identifier(&self.instance_id, "instance_id")?;
        validate_identifier(&self.environment, "environment")?;
        if let Some(reference) = &self.profile_context_ref {
            validate_profile_reference(reference)?;
        }
        for (name, path) in [
            ("state_root", &self.state_root),
            ("runtime_root", &self.runtime_root),
            ("socket_path", &self.socket_path),
            ("staging_root", &self.staging_root),
            ("recovery_root", &self.recovery_root),
        ] {
            validate_absolute_normalized_path(path, name)?;
        }
        if self.state_root == self.runtime_root
            || is_descendant(&self.state_root, &self.runtime_root)
            || is_descendant(&self.runtime_root, &self.state_root)
        {
            return Err(ConfigurationError::new(
                "state_root and runtime_root must be disjoint",
            ));
        }
        if !is_descendant(&self.socket_path, &self.runtime_root) {
            return Err(ConfigurationError::new(
                "socket_path must be inside runtime_root",
            ));
        }
        if !is_descendant(&self.staging_root, &self.state_root)
            || !is_descendant(&self.recovery_root, &self.state_root)
        {
            return Err(ConfigurationError::new(
                "staging_root and recovery_root must be inside state_root",
            ));
        }
        if self.staging_root == self.recovery_root
            || is_descendant(&self.staging_root, &self.recovery_root)
            || is_descendant(&self.recovery_root, &self.staging_root)
        {
            return Err(ConfigurationError::new(
                "staging_root and recovery_root must be disjoint",
            ));
        }
        Ok(())
    }

    pub fn critical_transitions_configured(&self) -> bool {
        self.receipt_store_mode == StoreMode::Durable
            && self.idempotency_store_mode == StoreMode::Durable
            && self.recovery_path_state == RecoveryPathState::Verified
            && self.resource_envelope_mode == DependencyMode::Available
    }

    fn apply_environment(
        &mut self,
        environment: &BTreeMap<String, String>,
    ) -> Result<(), ConfigurationError> {
        for (key, value) in environment {
            if let Some(config_key) = key.strip_prefix(ENV_PREFIX) {
                if config_key == "CONFIG_PATH" {
                    continue;
                }
                self.apply_value(
                    &config_key.to_ascii_lowercase(),
                    value,
                    ValueOrigin::Environment,
                )?;
            }
        }
        Ok(())
    }

    fn apply_value(
        &mut self,
        key: &str,
        raw_value: &str,
        origin: ValueOrigin,
    ) -> Result<(), ConfigurationError> {
        match key {
            "instance_id" => self.instance_id = parse_string(raw_value, origin)?,
            "environment" => self.environment = parse_string(raw_value, origin)?,
            "profile_context_ref" => {
                let value = parse_string(raw_value, origin)?;
                self.profile_context_ref = if value.is_empty() { None } else { Some(value) };
            },
            "state_root" => self.state_root = PathBuf::from(parse_string(raw_value, origin)?),
            "runtime_root" => self.runtime_root = PathBuf::from(parse_string(raw_value, origin)?),
            "socket_path" => self.socket_path = PathBuf::from(parse_string(raw_value, origin)?),
            "staging_root" => self.staging_root = PathBuf::from(parse_string(raw_value, origin)?),
            "recovery_root" => self.recovery_root = PathBuf::from(parse_string(raw_value, origin)?),
            "enabled_operation_classes" => {
                self.enabled_operation_classes = parse_string_list(raw_value, origin)?
                    .into_iter()
                    .map(|value| value.parse())
                    .collect::<Result<_, _>>()?;
            },
            "identity_verification_mode" => {
                self.identity_verification_mode = parse_string(raw_value, origin)?.parse()?;
            },
            "profile_validation_mode" => {
                self.profile_validation_mode = parse_string(raw_value, origin)?.parse()?;
            },
            "policy_runtime_mode" => {
                self.policy_runtime_mode = parse_string(raw_value, origin)?.parse()?;
            },
            "artifact_verification_mode" => {
                self.artifact_verification_mode = parse_string(raw_value, origin)?.parse()?;
            },
            "resource_envelope_mode" => {
                self.resource_envelope_mode = parse_string(raw_value, origin)?.parse()?;
            },
            "control_plane_mode" => {
                self.control_plane_mode = parse_string(raw_value, origin)?.parse()?;
            },
            "receipt_store_mode" => {
                self.receipt_store_mode = parse_string(raw_value, origin)?.parse()?;
            },
            "idempotency_store_mode" => {
                self.idempotency_store_mode = parse_string(raw_value, origin)?.parse()?;
            },
            "staging_capacity_state" => {
                self.staging_capacity_state = parse_string(raw_value, origin)?.parse()?;
            },
            "recovery_path_state" => {
                self.recovery_path_state = parse_string(raw_value, origin)?.parse()?;
            },
            "resource_pressure_state" => {
                self.resource_pressure_state = parse_string(raw_value, origin)?.parse()?;
            },
            _ => {
                return Err(ConfigurationError::new(format!(
                    "unknown configuration key: {key}"
                )))
            },
        }
        Ok(())
    }
}

fn reject_unknown_environment(
    environment: &BTreeMap<String, String>,
) -> Result<(), ConfigurationError> {
    const ALLOWED: [&str; 20] = [
        "KOA_NODE_AGENT_CONFIG_PATH",
        "KOA_NODE_AGENT_INSTANCE_ID",
        "KOA_NODE_AGENT_ENVIRONMENT",
        "KOA_NODE_AGENT_PROFILE_CONTEXT_REF",
        "KOA_NODE_AGENT_STATE_ROOT",
        "KOA_NODE_AGENT_RUNTIME_ROOT",
        "KOA_NODE_AGENT_SOCKET_PATH",
        "KOA_NODE_AGENT_STAGING_ROOT",
        "KOA_NODE_AGENT_RECOVERY_ROOT",
        "KOA_NODE_AGENT_ENABLED_OPERATION_CLASSES",
        "KOA_NODE_AGENT_IDENTITY_VERIFICATION_MODE",
        "KOA_NODE_AGENT_PROFILE_VALIDATION_MODE",
        "KOA_NODE_AGENT_POLICY_RUNTIME_MODE",
        "KOA_NODE_AGENT_ARTIFACT_VERIFICATION_MODE",
        "KOA_NODE_AGENT_RESOURCE_ENVELOPE_MODE",
        "KOA_NODE_AGENT_CONTROL_PLANE_MODE",
        "KOA_NODE_AGENT_RECEIPT_STORE_MODE",
        "KOA_NODE_AGENT_IDEMPOTENCY_STORE_MODE",
        "KOA_NODE_AGENT_STAGING_CAPACITY_STATE",
        "KOA_NODE_AGENT_RECOVERY_PATH_STATE",
    ];
    let allowed: BTreeSet<&str> = ALLOWED.into_iter().collect();
    for key in environment.keys().filter(|key| key.starts_with(ENV_PREFIX)) {
        if !allowed.contains(key.as_str()) && key != "KOA_NODE_AGENT_RESOURCE_PRESSURE_STATE" {
            return Err(ConfigurationError::new(format!(
                "unknown kOA Node Agent environment variable: {key}"
            )));
        }
        if contains_secret_name(key) {
            return Err(ConfigurationError::new(format!(
                "secrets are prohibited in kOA Node Agent configuration: {key}"
            )));
        }
    }
    Ok(())
}

fn contains_secret_name(value: &str) -> bool {
    let lowercase = value.to_ascii_lowercase();
    [
        "password",
        "passphrase",
        "private_key",
        "secret",
        "token",
        "credential",
        "key_material",
    ]
    .iter()
    .any(|marker| lowercase.contains(marker))
}

fn validate_identifier(value: &str, name: &str) -> Result<(), ConfigurationError> {
    if value.is_empty() || value.len() > 256 {
        return Err(ConfigurationError::new(format!(
            "{name} must be a bounded non-empty identifier"
        )));
    }
    if !value.chars().all(|character| {
        character.is_ascii_alphanumeric()
            || matches!(character, '_' | '-' | '.' | ':' | '@' | '/' | '+')
    }) {
        return Err(ConfigurationError::new(format!(
            "{name} contains unsupported characters"
        )));
    }
    Ok(())
}

fn validate_profile_reference(value: &str) -> Result<(), ConfigurationError> {
    validate_identifier(value, "profile_context_ref")?;
    if !value.starts_with("contracts/profiles/") || !value.ends_with(".profile.json") {
        return Err(ConfigurationError::new(
            "profile_context_ref must reference contracts/profiles/*.profile.json",
        ));
    }
    Ok(())
}

fn validate_absolute_normalized_path(path: &Path, name: &str) -> Result<(), ConfigurationError> {
    if !path.is_absolute() {
        return Err(ConfigurationError::new(format!(
            "{name} must be an absolute path"
        )));
    }
    for component in path.components() {
        if matches!(component, Component::ParentDir | Component::CurDir) {
            return Err(ConfigurationError::new(format!(
                "{name} must be normalized and cannot contain traversal"
            )));
        }
    }
    Ok(())
}

fn is_descendant(path: &Path, root: &Path) -> bool {
    path != root && path.starts_with(root)
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum ValueOrigin {
    Toml,
    Environment,
}

fn parse_component_table(raw: &str) -> Result<BTreeMap<String, String>, ConfigurationError> {
    let mut values = BTreeMap::new();
    let mut in_component_table = false;
    for (index, source_line) in raw.lines().enumerate() {
        let line = strip_comment(source_line).trim();
        if line.is_empty() {
            continue;
        }
        if line.starts_with('[') {
            if line != "[koa_node_agent]" {
                return Err(ConfigurationError::new(format!(
                    "unknown TOML table on line {}: {line}",
                    index + 1
                )));
            }
            if in_component_table {
                return Err(ConfigurationError::new("duplicate [koa_node_agent] table"));
            }
            in_component_table = true;
            continue;
        }
        if !in_component_table {
            return Err(ConfigurationError::new(format!(
                "configuration value outside [koa_node_agent] on line {}",
                index + 1
            )));
        }
        let (key, value) = line.split_once('=').ok_or_else(|| {
            ConfigurationError::new(format!("invalid TOML assignment on line {}", index + 1))
        })?;
        let key = key.trim();
        if key.is_empty() || values.contains_key(key) {
            return Err(ConfigurationError::new(format!(
                "empty or duplicate configuration key on line {}",
                index + 1
            )));
        }
        values.insert(key.to_owned(), value.trim().to_owned());
    }
    if !in_component_table {
        return Err(ConfigurationError::new(
            "missing [koa_node_agent] TOML table",
        ));
    }
    Ok(values)
}

fn strip_comment(line: &str) -> &str {
    let mut quoted = false;
    let mut escaped = false;
    for (index, character) in line.char_indices() {
        if escaped {
            escaped = false;
            continue;
        }
        match character {
            '\\' if quoted => escaped = true,
            '"' => quoted = !quoted,
            '#' if !quoted => return &line[..index],
            _ => {},
        }
    }
    line
}

fn parse_string(raw: &str, origin: ValueOrigin) -> Result<String, ConfigurationError> {
    let value = raw.trim();
    if value.starts_with('"') && value.ends_with('"') && value.len() >= 2 {
        let inner = &value[1..value.len() - 1];
        if inner.contains('"') || inner.contains('\\') {
            return Err(ConfigurationError::new(
                "escaped TOML strings are not supported in this closed configuration",
            ));
        }
        return Ok(inner.to_owned());
    }
    if origin == ValueOrigin::Toml {
        return Err(ConfigurationError::new(
            "TOML string values must use double quotes",
        ));
    }
    Ok(value.to_owned())
}

fn parse_string_list(raw: &str, origin: ValueOrigin) -> Result<Vec<String>, ConfigurationError> {
    let value = raw.trim();
    if value.starts_with('[') && value.ends_with(']') {
        let inner = &value[1..value.len() - 1];
        if inner.trim().is_empty() {
            return Ok(Vec::new());
        }
        return inner
            .split(',')
            .map(|item| parse_string(item, ValueOrigin::Toml))
            .collect();
    }
    if origin == ValueOrigin::Toml {
        return Err(ConfigurationError::new(
            "TOML list values must use an array of quoted strings",
        ));
    }
    if value.is_empty() {
        return Ok(Vec::new());
    }
    value
        .split(',')
        .map(|item| parse_string(item, ValueOrigin::Environment))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

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
        .expect("valid configuration")
    }

    #[test]
    fn defaults_fail_closed() {
        let config = NodeAgentConfig::default();
        assert!(config.enabled_operation_classes.is_empty());
        assert!(!config.critical_transitions_configured());
    }

    #[test]
    fn accepts_closed_operation_classes() {
        let config = ready_config();
        assert!(config
            .enabled_operation_classes
            .contains(&OperationClass::ActivateSystemArtifact));
        assert!(config.critical_transitions_configured());
    }

    #[test]
    fn rejects_unknown_operation_class() {
        let result = NodeAgentConfig::from_toml_str(
            "[koa_node_agent]\nenabled_operation_classes = [\"shell\"]\n",
        );
        assert!(result.is_err());
    }

    #[test]
    fn rejects_unknown_environment_variable() {
        let result = NodeAgentConfig::load_with_environment(
            None,
            [("KOA_NODE_AGENT_ARBITRARY_SHELL", "true")],
        );
        assert!(result.is_err());
    }

    #[test]
    fn rejects_path_traversal_and_overlaps() {
        let traversal = NodeAgentConfig::from_toml_str(
            "[koa_node_agent]\nstate_root = \"/var/lib/koa/../escape\"\n",
        );
        assert!(traversal.is_err());
        let overlap = NodeAgentConfig::from_toml_str(
            "[koa_node_agent]\nstaging_root = \"/var/lib/koa/node-agent/recovery/child\"\n",
        );
        assert!(overlap.is_err());
    }
}
