//! Authenticated local Unix-socket transport with bounded length-prefixed frames.

use std::collections::BTreeSet;
use std::fs;
use std::io::{Read, Write};
use std::os::unix::fs::{FileTypeExt, PermissionsExt};
use std::os::unix::net::{UnixListener, UnixStream};
use std::path::{Path, PathBuf};
use std::time::Duration;

pub const SOCKET_PROTOCOL_VERSION: &str = "1.0.0";
pub const DEFAULT_MAX_FRAME_BYTES: usize = 1024 * 1024;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct PeerCredentials {
    pub process_id: Option<i32>,
    pub user_id: u32,
    pub group_id: u32,
}

/// Source of authenticated kernel peer credentials.
///
/// Stable Rust 1.74 does not expose Linux `SO_PEERCRED` without either an
/// external system crate or unsafe code.  The adapter therefore requires this
/// dependency explicitly instead of silently treating a connected socket as
/// authenticated.
pub trait PeerCredentialSource: Send + Sync {
    fn peer_credentials(
        &self,
        stream: &UnixStream,
    ) -> Result<PeerCredentials, SocketProtocolError>;
}

#[derive(Clone, Debug)]
pub struct ExactUidAuthenticator<S> {
    source: S,
    allowed_uids: BTreeSet<u32>,
}

impl<S> ExactUidAuthenticator<S> {
    pub fn new(
        source: S,
        allowed_uids: impl IntoIterator<Item = u32>,
    ) -> Result<Self, SocketProtocolError> {
        let allowed_uids: BTreeSet<u32> = allowed_uids.into_iter().collect();
        if allowed_uids.is_empty() {
            return Err(SocketProtocolError::new(
                SocketProtocolErrorCode::InvalidConfiguration,
                "at least one peer UID must be allowlisted",
            ));
        }
        Ok(Self {
            source,
            allowed_uids,
        })
    }
}

pub trait PeerAuthenticator: Send + Sync {
    fn authenticate(
        &self,
        stream: &UnixStream,
    ) -> Result<PeerCredentials, SocketProtocolError>;
}

impl<S: PeerCredentialSource> PeerAuthenticator for ExactUidAuthenticator<S> {
    fn authenticate(
        &self,
        stream: &UnixStream,
    ) -> Result<PeerCredentials, SocketProtocolError> {
        let peer = self.source.peer_credentials(stream)?;
        if self.allowed_uids.contains(&peer.user_id) {
            Ok(peer)
        } else {
            Err(SocketProtocolError::new(
                SocketProtocolErrorCode::PeerUnauthorized,
                format!("peer UID {} is not allowlisted", peer.user_id),
            ))
        }
    }
}

pub trait SocketRequestHandler: Send + Sync {
    fn handle(
        &self,
        peer: PeerCredentials,
        request: &[u8],
    ) -> Result<Vec<u8>, SocketProtocolError>;
}

impl<F> SocketRequestHandler for F
where
    F: Fn(PeerCredentials, &[u8]) -> Result<Vec<u8>, SocketProtocolError> + Send + Sync,
{
    fn handle(
        &self,
        peer: PeerCredentials,
        request: &[u8],
    ) -> Result<Vec<u8>, SocketProtocolError> {
        self(peer, request)
    }
}

#[derive(Clone, Debug)]
pub struct UnixSocketConfig {
    pub runtime_root: PathBuf,
    pub socket_path: PathBuf,
    pub max_frame_bytes: usize,
    pub io_timeout: Duration,
}

impl UnixSocketConfig {
    pub fn validate(&self) -> Result<(), SocketProtocolError> {
        validate_bounded_absolute_path("runtime_root", &self.runtime_root)?;
        validate_bounded_absolute_path("socket_path", &self.socket_path)?;
        if !self.socket_path.starts_with(&self.runtime_root) {
            return Err(SocketProtocolError::new(
                SocketProtocolErrorCode::UnsafePath,
                "socket path must remain below the declared runtime root",
            ));
        }
        if self.max_frame_bytes == 0 || self.max_frame_bytes > 16 * 1024 * 1024 {
            return Err(SocketProtocolError::new(
                SocketProtocolErrorCode::InvalidConfiguration,
                "max_frame_bytes must be between 1 byte and 16 MiB",
            ));
        }
        if self.io_timeout.is_zero() {
            return Err(SocketProtocolError::new(
                SocketProtocolErrorCode::InvalidConfiguration,
                "io_timeout must be positive",
            ));
        }
        let root_metadata = fs::symlink_metadata(&self.runtime_root).map_err(io_error)?;
        if root_metadata.file_type().is_symlink() || !root_metadata.is_dir() {
            return Err(SocketProtocolError::new(
                SocketProtocolErrorCode::UnsafePath,
                "runtime root must be an existing non-symlink directory",
            ));
        }
        let parent = self.socket_path.parent().ok_or_else(|| {
            SocketProtocolError::new(
                SocketProtocolErrorCode::UnsafePath,
                "socket path must have a parent directory",
            )
        })?;
        let parent_metadata = fs::symlink_metadata(parent).map_err(io_error)?;
        if parent_metadata.file_type().is_symlink() || !parent_metadata.is_dir() {
            return Err(SocketProtocolError::new(
                SocketProtocolErrorCode::UnsafePath,
                "socket parent must be an existing non-symlink directory",
            ));
        }
        Ok(())
    }
}

pub struct UnixSocketServer<A, H> {
    listener: UnixListener,
    config: UnixSocketConfig,
    authorizer: A,
    handler: H,
}

impl<A: PeerAuthenticator, H: SocketRequestHandler> UnixSocketServer<A, H> {
    pub fn bind(
        config: UnixSocketConfig,
        authorizer: A,
        handler: H,
    ) -> Result<Self, SocketProtocolError> {
        config.validate()?;
        if config.socket_path.exists() {
            return Err(SocketProtocolError::new(
                SocketProtocolErrorCode::SocketAlreadyExists,
                "refusing to replace an existing socket path",
            ));
        }
        let listener = UnixListener::bind(&config.socket_path).map_err(io_error)?;
        fs::set_permissions(&config.socket_path, fs::Permissions::from_mode(0o600))
            .map_err(io_error)?;
        Ok(Self {
            listener,
            config,
            authorizer,
            handler,
        })
    }

    pub fn serve_once(&self) -> Result<(), SocketProtocolError> {
        let (mut stream, _) = self.listener.accept().map_err(io_error)?;
        stream
            .set_read_timeout(Some(self.config.io_timeout))
            .map_err(io_error)?;
        stream
            .set_write_timeout(Some(self.config.io_timeout))
            .map_err(io_error)?;
        let peer = self.authorizer.authenticate(&stream)?;
        let request = read_frame(&mut stream, self.config.max_frame_bytes)?;
        let response = self.handler.handle(peer, &request)?;
        write_frame(&mut stream, &response, self.config.max_frame_bytes)
    }

    pub fn socket_path(&self) -> &Path {
        &self.config.socket_path
    }
}

impl<A, H> Drop for UnixSocketServer<A, H> {
    fn drop(&mut self) {
        if let Ok(metadata) = fs::symlink_metadata(&self.config.socket_path) {
            if metadata.file_type().is_socket() {
                let _ = fs::remove_file(&self.config.socket_path);
            }
        }
    }
}

pub fn exchange(
    socket_path: &Path,
    request: &[u8],
    max_frame_bytes: usize,
    io_timeout: Duration,
) -> Result<Vec<u8>, SocketProtocolError> {
    validate_bounded_absolute_path("socket_path", socket_path)?;
    if io_timeout.is_zero() {
        return Err(SocketProtocolError::new(
            SocketProtocolErrorCode::InvalidConfiguration,
            "io_timeout must be positive",
        ));
    }
    let mut stream = UnixStream::connect(socket_path).map_err(io_error)?;
    stream
        .set_read_timeout(Some(io_timeout))
        .map_err(io_error)?;
    stream
        .set_write_timeout(Some(io_timeout))
        .map_err(io_error)?;
    write_frame(&mut stream, request, max_frame_bytes)?;
    read_frame(&mut stream, max_frame_bytes)
}

pub fn read_frame(
    reader: &mut impl Read,
    max_frame_bytes: usize,
) -> Result<Vec<u8>, SocketProtocolError> {
    validate_frame_limit(max_frame_bytes)?;
    let mut length_bytes = [0_u8; 4];
    reader.read_exact(&mut length_bytes).map_err(io_error)?;
    let length = u32::from_be_bytes(length_bytes) as usize;
    if length == 0 || length > max_frame_bytes {
        return Err(SocketProtocolError::new(
            SocketProtocolErrorCode::FrameSizeInvalid,
            format!("frame length {length} is outside the configured bound"),
        ));
    }
    let mut payload = vec![0_u8; length];
    reader.read_exact(&mut payload).map_err(io_error)?;
    std::str::from_utf8(&payload).map_err(|_| {
        SocketProtocolError::new(
            SocketProtocolErrorCode::FrameNotUtf8,
            "socket frame must have a deterministic UTF-8 representation",
        )
    })?;
    Ok(payload)
}

pub fn write_frame(
    writer: &mut impl Write,
    payload: &[u8],
    max_frame_bytes: usize,
) -> Result<(), SocketProtocolError> {
    validate_frame_limit(max_frame_bytes)?;
    if payload.is_empty() || payload.len() > max_frame_bytes || payload.len() > u32::MAX as usize {
        return Err(SocketProtocolError::new(
            SocketProtocolErrorCode::FrameSizeInvalid,
            "payload is empty or exceeds the configured frame bound",
        ));
    }
    std::str::from_utf8(payload).map_err(|_| {
        SocketProtocolError::new(
            SocketProtocolErrorCode::FrameNotUtf8,
            "socket frame must have a deterministic UTF-8 representation",
        )
    })?;
    writer
        .write_all(&(payload.len() as u32).to_be_bytes())
        .map_err(io_error)?;
    writer.write_all(payload).map_err(io_error)?;
    writer.flush().map_err(io_error)
}

fn validate_frame_limit(maximum: usize) -> Result<(), SocketProtocolError> {
    if maximum == 0 || maximum > 16 * 1024 * 1024 {
        return Err(SocketProtocolError::new(
            SocketProtocolErrorCode::InvalidConfiguration,
            "frame limit must be between 1 byte and 16 MiB",
        ));
    }
    Ok(())
}

fn validate_bounded_absolute_path(
    name: &str,
    path: &Path,
) -> Result<(), SocketProtocolError> {
    if !path.is_absolute() || path == Path::new("/") {
        return Err(SocketProtocolError::new(
            SocketProtocolErrorCode::UnsafePath,
            format!("{name} must be an absolute bounded path"),
        ));
    }
    let value = path.to_str().ok_or_else(|| {
        SocketProtocolError::new(
            SocketProtocolErrorCode::UnsafePath,
            format!("{name} must be valid UTF-8"),
        )
    })?;
    if value.len() > 4096 || value.chars().any(char::is_control) {
        return Err(SocketProtocolError::new(
            SocketProtocolErrorCode::UnsafePath,
            format!("{name} exceeds the path bound or contains control characters"),
        ));
    }
    if path.components().any(|component| {
        matches!(
            component,
            std::path::Component::CurDir | std::path::Component::ParentDir
        )
    }) {
        return Err(SocketProtocolError::new(
            SocketProtocolErrorCode::UnsafePath,
            format!("{name} may not contain traversal components"),
        ));
    }
    Ok(())
}

fn io_error(error: std::io::Error) -> SocketProtocolError {
    SocketProtocolError::new(SocketProtocolErrorCode::Io, error.to_string())
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum SocketProtocolErrorCode {
    InvalidConfiguration,
    UnsafePath,
    SocketAlreadyExists,
    PeerUnauthorized,
    FrameSizeInvalid,
    FrameNotUtf8,
    Io,
}

impl SocketProtocolErrorCode {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::InvalidConfiguration => "invalid_configuration",
            Self::UnsafePath => "unsafe_path",
            Self::SocketAlreadyExists => "socket_already_exists",
            Self::PeerUnauthorized => "peer_unauthorized",
            Self::FrameSizeInvalid => "frame_size_invalid",
            Self::FrameNotUtf8 => "frame_not_utf8",
            Self::Io => "io",
        }
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct SocketProtocolError {
    code: SocketProtocolErrorCode,
    detail: String,
}

impl SocketProtocolError {
    pub fn new(code: SocketProtocolErrorCode, detail: impl Into<String>) -> Self {
        Self {
            code,
            detail: detail.into(),
        }
    }

    pub const fn code(&self) -> SocketProtocolErrorCode {
        self.code
    }

    pub fn detail(&self) -> &str {
        &self.detail
    }
}

impl std::fmt::Display for SocketProtocolError {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{}: {}", self.code.as_str(), self.detail)
    }
}

impl std::error::Error for SocketProtocolError {}
