//! Node Agent adapters implementing only public component ports.

pub mod clock;
pub mod filesystem_receipt_store;
pub mod mount_backend;
pub mod network_backend;
pub mod systemd_backend;
pub mod unix_socket;

pub use clock::SystemClock;
pub use filesystem_receipt_store::FilesystemReceiptStore;
pub use mount_backend::{MountBackendAdapter, MountManager, MountManagerError};
pub use network_backend::{
    NetworkBackendAdapter, NetworkManager, NetworkManagerError, NetworkPolicyBinding,
};
pub use systemd_backend::{
    ServiceGroupBinding, SystemdBackendAdapter, SystemdManager, SystemdManagerError, UnitState,
};
pub use unix_socket::{
    exchange, read_frame, write_frame, ExactUidAuthenticator, PeerAuthenticator,
    PeerCredentialSource, PeerCredentials, SocketProtocolError, SocketProtocolErrorCode,
    SocketRequestHandler, UnixSocketConfig,
    UnixSocketServer, DEFAULT_MAX_FRAME_BYTES, SOCKET_PROTOCOL_VERSION,
};
