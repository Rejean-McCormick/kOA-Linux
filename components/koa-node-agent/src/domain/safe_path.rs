//! Lexically safe, profile-declared filesystem targets.
//!
//! `SafePath` does not canonicalize the filesystem and therefore cannot by
//! itself prove that a later-created symlink remains beneath a root. Adapters
//! must perform descriptor-based or equivalent no-follow checks at execution
//! time. This type prevents absolute-path injection and lexical traversal before
//! any privileged adapter is reached.

use core::fmt;
use std::path::{Component, Path, PathBuf};

const MAX_ROOT_ID_BYTES: usize = 128;
const MAX_PATH_BYTES: usize = 4096;

#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct AllowedRoot {
    id: String,
    path: PathBuf,
}

impl AllowedRoot {
    pub fn new(id: impl Into<String>, path: impl Into<PathBuf>) -> Result<Self, SafePathError> {
        let id = id.into();
        validate_root_id(&id)?;
        let path = path.into();
        validate_absolute_root(&path)?;
        Ok(Self { id, path })
    }

    pub fn id(&self) -> &str {
        &self.id
    }

    pub fn path(&self) -> &Path {
        &self.path
    }
}

#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct SafePath {
    root: AllowedRoot,
    relative: PathBuf,
}

impl SafePath {
    pub fn new(root: &AllowedRoot, relative: impl Into<PathBuf>) -> Result<Self, SafePathError> {
        let relative = relative.into();
        validate_relative_path(&relative)?;
        Ok(Self {
            root: root.clone(),
            relative,
        })
    }

    pub fn root(&self) -> &AllowedRoot {
        &self.root
    }

    pub fn relative(&self) -> &Path {
        &self.relative
    }

    pub fn resolved(&self) -> PathBuf {
        self.root.path.join(&self.relative)
    }

    pub fn belongs_to(&self, allowed_root: &AllowedRoot) -> bool {
        &self.root == allowed_root
    }

    /// Stable representation suitable for request canonicalization.
    pub fn canonical(&self) -> String {
        format!("{}:{}", self.root.id, self.relative.to_string_lossy())
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum SafePathErrorCode {
    EmptyRootId,
    InvalidRootId,
    RootIdTooLong,
    RootMustBeAbsolute,
    RootMustBeBounded,
    RootContainsTraversal,
    PathMustBeRelative,
    PathMustNotBeEmpty,
    PathContainsTraversal,
    PathContainsControlCharacter,
    PathIsNotUtf8,
    PathTooLong,
}

impl SafePathErrorCode {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::EmptyRootId => "empty_root_id",
            Self::InvalidRootId => "invalid_root_id",
            Self::RootIdTooLong => "root_id_too_long",
            Self::RootMustBeAbsolute => "root_must_be_absolute",
            Self::RootMustBeBounded => "root_must_be_bounded",
            Self::RootContainsTraversal => "root_contains_traversal",
            Self::PathMustBeRelative => "path_must_be_relative",
            Self::PathMustNotBeEmpty => "path_must_not_be_empty",
            Self::PathContainsTraversal => "path_contains_traversal",
            Self::PathContainsControlCharacter => "path_contains_control_character",
            Self::PathIsNotUtf8 => "path_is_not_utf8",
            Self::PathTooLong => "path_too_long",
        }
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct SafePathError {
    code: SafePathErrorCode,
    detail: String,
}

impl SafePathError {
    fn new(code: SafePathErrorCode, detail: impl Into<String>) -> Self {
        Self {
            code,
            detail: detail.into(),
        }
    }

    pub const fn code(&self) -> SafePathErrorCode {
        self.code
    }

    pub fn detail(&self) -> &str {
        &self.detail
    }
}

impl fmt::Display for SafePathError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "{}: {}", self.code.as_str(), self.detail)
    }
}

impl std::error::Error for SafePathError {}

fn validate_root_id(id: &str) -> Result<(), SafePathError> {
    if id.is_empty() {
        return Err(SafePathError::new(
            SafePathErrorCode::EmptyRootId,
            "an allowlisted root requires a stable identifier",
        ));
    }
    if id.len() > MAX_ROOT_ID_BYTES {
        return Err(SafePathError::new(
            SafePathErrorCode::RootIdTooLong,
            format!("root identifier exceeds {MAX_ROOT_ID_BYTES} bytes"),
        ));
    }
    if !id
        .bytes()
        .all(|byte| byte.is_ascii_alphanumeric() || matches!(byte, b'-' | b'_' | b'.'))
    {
        return Err(SafePathError::new(
            SafePathErrorCode::InvalidRootId,
            "root identifiers permit only ASCII letters, digits, '-', '_' and '.'",
        ));
    }
    Ok(())
}

fn validate_absolute_root(path: &Path) -> Result<(), SafePathError> {
    if !path.is_absolute() {
        return Err(SafePathError::new(
            SafePathErrorCode::RootMustBeAbsolute,
            "allowlisted roots must be absolute",
        ));
    }
    if path == Path::new("/") {
        return Err(SafePathError::new(
            SafePathErrorCode::RootMustBeBounded,
            "the filesystem root cannot be an allowlisted operation root",
        ));
    }
    validate_utf8_and_length(path)?;
    for component in path.components() {
        if matches!(component, Component::CurDir | Component::ParentDir) {
            return Err(SafePathError::new(
                SafePathErrorCode::RootContainsTraversal,
                "allowlisted roots must be lexically normalized",
            ));
        }
    }
    Ok(())
}

fn validate_relative_path(path: &Path) -> Result<(), SafePathError> {
    if path.as_os_str().is_empty() {
        return Err(SafePathError::new(
            SafePathErrorCode::PathMustNotBeEmpty,
            "a safe path requires at least one relative component",
        ));
    }
    if path.is_absolute() {
        return Err(SafePathError::new(
            SafePathErrorCode::PathMustBeRelative,
            "callers may not provide absolute operation paths",
        ));
    }
    validate_utf8_and_length(path)?;
    for component in path.components() {
        match component {
            Component::Normal(_) => {},
            Component::Prefix(_) | Component::RootDir => {
                return Err(SafePathError::new(
                    SafePathErrorCode::PathMustBeRelative,
                    "platform-prefixed or rooted operation paths are not permitted",
                ));
            },
            Component::CurDir | Component::ParentDir => {
                return Err(SafePathError::new(
                    SafePathErrorCode::PathContainsTraversal,
                    "only normal relative path components are permitted",
                ));
            },
        }
    }
    Ok(())
}

fn validate_utf8_and_length(path: &Path) -> Result<(), SafePathError> {
    let value = path.to_str().ok_or_else(|| {
        SafePathError::new(
            SafePathErrorCode::PathIsNotUtf8,
            "operation paths must have a deterministic UTF-8 representation",
        )
    })?;
    if value.len() > MAX_PATH_BYTES {
        return Err(SafePathError::new(
            SafePathErrorCode::PathTooLong,
            format!("path exceeds {MAX_PATH_BYTES} bytes"),
        ));
    }
    if value.chars().any(char::is_control) {
        return Err(SafePathError::new(
            SafePathErrorCode::PathContainsControlCharacter,
            "operation paths may not contain control characters",
        ));
    }

    // std::path interprets path syntax according to the host platform.
    // Koali artifacts must reject Windows prefixes even when validated on
    // a Linux build host, where Component::Prefix is never produced.
    let bytes = value.as_bytes();
    let has_windows_drive_prefix =
        bytes.len() >= 2 && bytes[0].is_ascii_alphabetic() && bytes[1] == b':';

    if has_windows_drive_prefix || value.starts_with("\\\\") {
        return Err(SafePathError::new(
            SafePathErrorCode::PathMustBeRelative,
            "platform-prefixed operation paths are not permitted",
        ));
    }

    // Backslash is a Windows path separator. Reject it rather than allowing
    // a host-dependent interpretation of the same canonical request.
    if value.contains('\\') {
        return Err(SafePathError::new(
            SafePathErrorCode::PathContainsTraversal,
            "operation paths may not contain platform-specific separators",
        ));
    }

    if value
        .split('/')
        .any(|component| component == "." || component == "..")
    {
        return Err(SafePathError::new(
            SafePathErrorCode::PathContainsTraversal,
            "operation paths may not contain '.' or '..' components",
        ));
    }
    Ok(())
}
