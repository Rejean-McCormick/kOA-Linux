//! Validation and filesystem confinement primitives for privileged adapters.

use std::fmt;
use std::fs;
use std::path::{Component, Path, PathBuf};

/// Fixed bounds applied before a request reaches a privileged adapter.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct RequestBounds {
    pub maximum_token_bytes: usize,
    pub maximum_reference_bytes: usize,
    pub maximum_parameter_value_bytes: usize,
    pub maximum_references: usize,
    pub maximum_parameters: usize,
    pub maximum_canonical_request_bytes: usize,
}

impl Default for RequestBounds {
    fn default() -> Self {
        Self {
            maximum_token_bytes: 256,
            maximum_reference_bytes: 2_048,
            maximum_parameter_value_bytes: 4_096,
            maximum_references: 16,
            maximum_parameters: 16,
            maximum_canonical_request_bytes: 65_536,
        }
    }
}

/// Fail-closed request and path policy shared by broker entry points.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct SandboxPolicy {
    bounds: RequestBounds,
}

impl Default for SandboxPolicy {
    fn default() -> Self {
        Self::new(RequestBounds::default())
    }
}

impl SandboxPolicy {
    pub const fn new(bounds: RequestBounds) -> Self {
        Self { bounds }
    }

    pub const fn bounds(&self) -> RequestBounds {
        self.bounds
    }

    pub fn validate_token(&self, field: &'static str, value: &str) -> Result<(), SandboxError> {
        if value.is_empty() {
            return Err(SandboxError::new("empty_field", field, "value is required"));
        }
        if value.len() > self.bounds.maximum_token_bytes {
            return Err(SandboxError::new(
                "field_too_large",
                field,
                "token exceeds limit",
            ));
        }
        if value
            .bytes()
            .any(|byte| byte.is_ascii_control() || byte == b' ' || byte == b'\\')
        {
            return Err(SandboxError::new(
                "invalid_token",
                field,
                "token contains whitespace, control characters, or a backslash",
            ));
        }
        Ok(())
    }

    /// Validate a managed reference. It may contain repository-style `/` separators,
    /// but it may not be absolute, traverse upward, contain empty segments, or contain
    /// shell/control characters.
    pub fn validate_managed_reference(
        &self,
        field: &'static str,
        value: &str,
    ) -> Result<(), SandboxError> {
        if value.is_empty() {
            return Err(SandboxError::new(
                "empty_reference",
                field,
                "reference is required",
            ));
        }
        if value.len() > self.bounds.maximum_reference_bytes {
            return Err(SandboxError::new(
                "reference_too_large",
                field,
                "reference exceeds limit",
            ));
        }
        if value.starts_with('/') || value.starts_with('\\') {
            return Err(SandboxError::new(
                "absolute_path_rejected",
                field,
                "absolute paths are not managed references",
            ));
        }
        if value.contains('\\')
            || value
                .bytes()
                .any(|byte| byte == 0 || byte.is_ascii_control())
        {
            return Err(SandboxError::new(
                "invalid_reference",
                field,
                "reference contains a forbidden character",
            ));
        }
        if value
            .split('/')
            .any(|segment| segment.is_empty() || segment == "." || segment == "..")
        {
            return Err(SandboxError::new(
                "path_traversal_rejected",
                field,
                "reference contains an empty, current, or parent segment",
            ));
        }
        if contains_shell_metacharacter(value) {
            return Err(SandboxError::new(
                "shell_metacharacter_rejected",
                field,
                "managed references cannot contain shell metacharacters",
            ));
        }
        Ok(())
    }

    pub fn validate_profile_reference(&self, value: &str) -> Result<(), SandboxError> {
        self.validate_managed_reference("profile_context_ref", value)?;
        if !value.starts_with("contracts/profiles/") || !value.ends_with(".profile.json") {
            return Err(SandboxError::new(
                "invalid_profile_reference",
                "profile_context_ref",
                "profile reference must name a canonical profile contract",
            ));
        }
        Ok(())
    }

    pub fn validate_parameter_key(&self, value: &str) -> Result<(), SandboxError> {
        self.validate_token("parameter_key", value)?;
        if !value
            .bytes()
            .all(|byte| byte.is_ascii_lowercase() || byte.is_ascii_digit() || byte == b'_')
        {
            return Err(SandboxError::new(
                "invalid_parameter_key",
                "parameter_key",
                "parameter keys must use lowercase ASCII snake_case",
            ));
        }
        if is_secret_bearing_name(value) {
            return Err(SandboxError::new(
                "secret_parameter_rejected",
                "parameter_key",
                "secret-bearing fields are forbidden on the broker request",
            ));
        }
        Ok(())
    }

    pub fn validate_parameter_value(&self, value: &str) -> Result<(), SandboxError> {
        if value.len() > self.bounds.maximum_parameter_value_bytes {
            return Err(SandboxError::new(
                "parameter_value_too_large",
                "parameter_value",
                "parameter value exceeds limit",
            ));
        }
        if value
            .bytes()
            .any(|byte| byte == 0 || byte.is_ascii_control())
            || contains_shell_metacharacter(value)
        {
            return Err(SandboxError::new(
                "invalid_parameter_value",
                "parameter_value",
                "parameter value contains control or shell characters",
            ));
        }
        Ok(())
    }
}

/// One profile-owned filesystem root available to a fixed privileged adapter.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct SafePathRoot {
    canonical_root: PathBuf,
}

impl SafePathRoot {
    /// Register an existing root after resolving symlinks.
    pub fn existing(root: impl AsRef<Path>) -> Result<Self, SandboxError> {
        let canonical_root = fs::canonicalize(root.as_ref()).map_err(|error| {
            SandboxError::new(
                "root_unavailable",
                "sandbox_root",
                format!("cannot canonicalize sandbox root: {error}"),
            )
        })?;
        if !canonical_root.is_dir() {
            return Err(SandboxError::new(
                "root_not_directory",
                "sandbox_root",
                "sandbox root is not a directory",
            ));
        }
        Ok(Self { canonical_root })
    }

    pub fn canonical_root(&self) -> &Path {
        &self.canonical_root
    }

    /// Resolve a relative lexical target under the registered root. The final target
    /// need not exist, so adapters must use directory-relative atomic APIs when
    /// creating it.
    pub fn resolve_relative(&self, relative: impl AsRef<Path>) -> Result<PathBuf, SandboxError> {
        let relative = relative.as_ref();
        if relative.as_os_str().is_empty() || relative.is_absolute() {
            return Err(SandboxError::new(
                "invalid_relative_path",
                "target_path",
                "target path must be a non-empty relative path",
            ));
        }

        let mut normalized = PathBuf::new();
        for component in relative.components() {
            match component {
                Component::Normal(segment) => normalized.push(segment),
                Component::CurDir
                | Component::ParentDir
                | Component::RootDir
                | Component::Prefix(_) => {
                    return Err(SandboxError::new(
                        "path_traversal_rejected",
                        "target_path",
                        "target path contains a non-normal component",
                    ));
                },
            }
        }
        if normalized.as_os_str().is_empty() {
            return Err(SandboxError::new(
                "invalid_relative_path",
                "target_path",
                "target path resolves to an empty path",
            ));
        }
        Ok(self.canonical_root.join(normalized))
    }

    /// Resolve an existing path and verify that no symlink escapes the registered root.
    pub fn resolve_existing(&self, relative: impl AsRef<Path>) -> Result<PathBuf, SandboxError> {
        let candidate = self.resolve_relative(relative)?;
        let canonical = fs::canonicalize(&candidate).map_err(|error| {
            SandboxError::new(
                "target_unavailable",
                "target_path",
                format!("cannot canonicalize target: {error}"),
            )
        })?;
        if !canonical.starts_with(&self.canonical_root) {
            return Err(SandboxError::new(
                "sandbox_escape_rejected",
                "target_path",
                "resolved target escapes the registered root",
            ));
        }
        Ok(canonical)
    }
}

fn contains_shell_metacharacter(value: &str) -> bool {
    value.chars().any(|character| {
        matches!(
            character,
            ';' | '|' | '&' | '`' | '$' | '<' | '>' | '\n' | '\r'
        )
    })
}

fn is_secret_bearing_name(value: &str) -> bool {
    [
        "secret",
        "password",
        "passwd",
        "credential",
        "private_key",
        "raw_key",
        "access_token",
        "refresh_token",
    ]
    .iter()
    .any(|needle| {
        let suffix = format!("_{needle}");
        value == *needle || value.ends_with(suffix.as_str())
    })
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct SandboxError {
    pub code: &'static str,
    pub field: &'static str,
    pub message: String,
}

impl SandboxError {
    pub fn new(code: &'static str, field: &'static str, message: impl Into<String>) -> Self {
        Self {
            code,
            field,
            message: message.into(),
        }
    }
}

impl fmt::Display for SandboxError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            formatter,
            "{} ({}): {}",
            self.code, self.field, self.message
        )
    }
}

impl std::error::Error for SandboxError {}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn references_reject_traversal_and_shell_fragments() {
        let policy = SandboxPolicy::default();
        assert!(policy
            .validate_managed_reference("target", "artifact:sha256:abc")
            .is_ok());
        assert!(policy
            .validate_managed_reference("target", "../../etc/shadow")
            .is_err());
        assert!(policy
            .validate_managed_reference("target", "artifact;shutdown")
            .is_err());
    }

    #[test]
    fn lexical_paths_remain_under_root() {
        let root = std::env::temp_dir();
        let safe = SafePathRoot::existing(&root).expect("temporary directory must exist");
        assert!(safe.resolve_relative("staging/candidate").is_ok());
        assert!(safe.resolve_relative("../outside").is_err());
        assert!(safe.resolve_relative("/etc/passwd").is_err());
    }
}
