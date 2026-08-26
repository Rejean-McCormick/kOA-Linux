#![forbid(unsafe_code)]

#[path = "../src/adapters/mod.rs"]
mod adapters;
#[path = "../src/domain/mod.rs"]
mod domain;
#[path = "../src/ports/mod.rs"]
mod ports;

use std::fs;
use std::io::Cursor;
use std::os::unix::net::UnixStream;
use std::path::PathBuf;
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::{Duration, SystemTime, UNIX_EPOCH};

use adapters::{
    exchange, read_frame, write_frame, ExactUidAuthenticator, PeerCredentialSource,
    PeerCredentials, SocketProtocolError, SocketProtocolErrorCode, UnixSocketConfig,
    UnixSocketServer, DEFAULT_MAX_FRAME_BYTES,
};

#[derive(Clone, Copy)]
struct ContractPeerCredentialSource {
    credentials: PeerCredentials,
}

impl PeerCredentialSource for ContractPeerCredentialSource {
    fn peer_credentials(
        &self,
        _stream: &UnixStream,
    ) -> Result<PeerCredentials, SocketProtocolError> {
        Ok(self.credentials)
    }
}

fn temporary_directory(label: &str) -> PathBuf {
    let nonce = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .expect("test clock is after Unix epoch")
        .as_nanos();
    let path = std::env::temp_dir().join(format!(
        "koa-node-agent-{label}-{}-{nonce}",
        std::process::id()
    ));
    fs::create_dir(&path).expect("temporary runtime directory is created");
    path
}

fn current_uid() -> u32 {
    let status = fs::read_to_string("/proc/self/status").expect("Linux proc status is readable");
    let line = status
        .lines()
        .find(|line| line.starts_with("Uid:"))
        .expect("proc status exposes Uid");
    line.split_whitespace()
        .nth(1)
        .expect("Uid has a real value")
        .parse()
        .expect("Uid is numeric")
}

#[test]
fn frame_codec_is_big_endian_bounded_and_utf8() {
    let mut bytes = Vec::new();
    write_frame(&mut bytes, br#"{"request_id":"request-1"}"#, 1024)
        .expect("valid bounded frame is written");
    assert_eq!(&bytes[..4], &(26_u32.to_be_bytes()));
    let decoded = read_frame(&mut Cursor::new(bytes), 1024).expect("frame round-trips");
    assert_eq!(decoded, br#"{"request_id":"request-1"}"#);

    let error = write_frame(&mut Vec::new(), &[], 1024).unwrap_err();
    assert_eq!(error.code(), SocketProtocolErrorCode::FrameSizeInvalid);
    let error = write_frame(&mut Vec::new(), &[0xff], 1024).unwrap_err();
    assert_eq!(error.code(), SocketProtocolErrorCode::FrameNotUtf8);
}

#[test]
fn oversized_declared_frame_is_rejected_before_allocation() {
    let mut bytes = Vec::from(((DEFAULT_MAX_FRAME_BYTES + 1) as u32).to_be_bytes());
    bytes.extend_from_slice(b"not-read");
    let error = read_frame(&mut Cursor::new(bytes), DEFAULT_MAX_FRAME_BYTES).unwrap_err();
    assert_eq!(error.code(), SocketProtocolErrorCode::FrameSizeInvalid);
}

#[test]
fn socket_round_trip_uses_peer_credentials_and_exact_uid_allowlist() {
    let runtime = temporary_directory("round-trip");
    let socket = runtime.join("node-agent.sock");
    let observed_peer = Arc::new(Mutex::new(None::<PeerCredentials>));
    let handler_peer = Arc::clone(&observed_peer);
    let server = UnixSocketServer::bind(
        UnixSocketConfig {
            runtime_root: runtime.clone(),
            socket_path: socket.clone(),
            max_frame_bytes: 4096,
            io_timeout: Duration::from_secs(2),
        },
        ExactUidAuthenticator::new(
            ContractPeerCredentialSource {
                credentials: PeerCredentials {
                    process_id: Some(std::process::id() as i32),
                    user_id: current_uid(),
                    group_id: 0,
                },
            },
            [current_uid()],
        )
        .expect("UID allowlist is valid"),
        move |peer: PeerCredentials, request: &[u8]| -> Result<Vec<u8>, SocketProtocolError> {
            *handler_peer.lock().expect("peer record lock") = Some(peer);
            let mut response = b"ack:".to_vec();
            response.extend_from_slice(request);
            Ok(response)
        },
    )
    .expect("bounded socket server binds");

    let worker = thread::spawn(move || server.serve_once());
    let response = exchange(
        &socket,
        br#"{"operation":"inspect_node_state"}"#,
        4096,
        Duration::from_secs(2),
    )
    .expect("client exchange succeeds");
    worker
        .join()
        .expect("server thread joins")
        .expect("server handles one request");

    assert_eq!(response, br#"ack:{"operation":"inspect_node_state"}"#);
    let peer = observed_peer
        .lock()
        .expect("peer record lock")
        .expect("server observed peer credentials");
    assert_eq!(peer.user_id, current_uid());
    assert!(peer.process_id.is_some());
    assert!(!socket.exists(), "server drop removes only its socket node");
    fs::remove_dir(runtime).expect("temporary runtime directory is removed");
}

#[test]
fn unauthorized_peer_is_rejected_without_invoking_handler() {
    let runtime = temporary_directory("unauthorized");
    let socket = runtime.join("node-agent.sock");
    let invoked = Arc::new(Mutex::new(false));
    let handler_invoked = Arc::clone(&invoked);
    let denied_uid = current_uid()
        .checked_add(1)
        .expect("UID increment is bounded");
    let server = UnixSocketServer::bind(
        UnixSocketConfig {
            runtime_root: runtime.clone(),
            socket_path: socket.clone(),
            max_frame_bytes: 4096,
            io_timeout: Duration::from_secs(2),
        },
        ExactUidAuthenticator::new(
            ContractPeerCredentialSource {
                credentials: PeerCredentials {
                    process_id: Some(std::process::id() as i32),
                    user_id: current_uid(),
                    group_id: 0,
                },
            },
            [denied_uid],
        )
        .expect("UID allowlist is valid"),
        move |_peer: PeerCredentials, _request: &[u8]| -> Result<Vec<u8>, SocketProtocolError> {
            *handler_invoked.lock().expect("handler flag lock") = true;
            Ok(b"unexpected".to_vec())
        },
    )
    .expect("bounded socket server binds");

    let worker = thread::spawn(move || server.serve_once());
    let client_result = exchange(
        &socket,
        br#"{"operation":"inspect_node_state"}"#,
        4096,
        Duration::from_secs(2),
    );
    let server_error = worker
        .join()
        .expect("server thread joins")
        .expect_err("server rejects unallowlisted peer");
    assert_eq!(
        server_error.code(),
        SocketProtocolErrorCode::PeerUnauthorized
    );
    assert!(
        client_result.is_err(),
        "connection closes without a success frame"
    );
    assert!(!*invoked.lock().expect("handler flag lock"));
    fs::remove_dir(runtime).expect("temporary runtime directory is removed");
}

#[test]
fn socket_path_must_remain_below_existing_non_symlink_runtime_root() {
    let runtime = temporary_directory("path-boundary");
    let outside = std::env::temp_dir().join("koa-node-agent-outside.sock");
    let error = UnixSocketConfig {
        runtime_root: runtime.clone(),
        socket_path: outside,
        max_frame_bytes: 4096,
        io_timeout: Duration::from_secs(2),
    }
    .validate()
    .unwrap_err();
    assert_eq!(error.code(), SocketProtocolErrorCode::UnsafePath);
    fs::remove_dir(runtime).expect("temporary runtime directory is removed");
}

#[derive(Clone, Default)]
struct SystemdManagerDouble {
    states: Arc<Mutex<std::collections::BTreeMap<String, adapters::UnitState>>>,
}

impl adapters::SystemdManager for SystemdManagerDouble {
    fn unit_state(&self, unit: &str) -> Result<adapters::UnitState, adapters::SystemdManagerError> {
        Ok(*self
            .states
            .lock()
            .expect("systemd state lock")
            .get(unit)
            .unwrap_or(&adapters::UnitState::Unknown))
    }

    fn restart_unit(&self, unit: &str) -> Result<(), adapters::SystemdManagerError> {
        self.states
            .lock()
            .expect("systemd state lock")
            .insert(unit.to_owned(), adapters::UnitState::Active);
        Ok(())
    }
}

#[derive(Clone, Default)]
struct MountManagerDouble {
    mounts: Arc<Mutex<std::collections::BTreeMap<PathBuf, String>>>,
}

impl adapters::MountManager for MountManagerDouble {
    fn mounted_source(
        &self,
        target: &std::path::Path,
    ) -> Result<Option<String>, adapters::MountManagerError> {
        Ok(self
            .mounts
            .lock()
            .expect("mount state lock")
            .get(target)
            .cloned())
    }

    fn mount(
        &self,
        source: &std::path::Path,
        target: &std::path::Path,
        _filesystem_type: &str,
        _read_only: bool,
    ) -> Result<(), adapters::MountManagerError> {
        self.mounts
            .lock()
            .expect("mount state lock")
            .insert(target.to_path_buf(), source.to_string_lossy().into_owned());
        Ok(())
    }

    fn unmount(&self, target: &std::path::Path) -> Result<(), adapters::MountManagerError> {
        self.mounts.lock().expect("mount state lock").remove(target);
        Ok(())
    }
}

#[derive(Clone)]
struct NetworkManagerDouble {
    active: Arc<Mutex<String>>,
}

impl adapters::NetworkManager for NetworkManagerDouble {
    fn active_policy_ref(&self) -> Result<String, adapters::NetworkManagerError> {
        Ok(self.active.lock().expect("network state lock").clone())
    }

    fn activate_policy_ref(&self, policy_ref: &str) -> Result<(), adapters::NetworkManagerError> {
        *self.active.lock().expect("network state lock") = policy_ref.to_owned();
        Ok(())
    }
}

#[test]
fn immutable_receipt_store_is_idempotent_and_conflict_detecting() {
    use ports::{ReceiptRecord, ReceiptStore, ReceiptStoreErrorCode, ReceiptWriteDisposition};

    let root = temporary_directory("receipt-store");
    let store = adapters::FilesystemReceiptStore::open(&root).expect("receipt root is safe");
    let record = ReceiptRecord::new(
        "receipt-1",
        "request-1",
        br#"{"result":"completed"}"#.to_vec(),
    )
    .expect("receipt is valid");
    assert_eq!(
        store.append(&record).expect("first append succeeds"),
        ReceiptWriteDisposition::Created
    );
    assert_eq!(
        store.append(&record).expect("equivalent replay succeeds"),
        ReceiptWriteDisposition::EquivalentReplay
    );
    let conflicting =
        ReceiptRecord::new("receipt-1", "request-1", br#"{"result":"failed"}"#.to_vec())
            .expect("conflicting receipt is structurally valid");
    assert_eq!(
        store.append(&conflicting).unwrap_err().code(),
        ReceiptStoreErrorCode::Conflict
    );
    assert_eq!(
        store.read("receipt-1").expect("stored receipt is readable"),
        Some(record)
    );
    fs::remove_dir_all(root).expect("receipt test directory is removed");
}

#[test]
fn systemd_adapter_uses_only_units_bound_to_the_declared_group() {
    use ports::{BackendErrorCode, BackendIdentifier, ServiceGroupRequest, SystemdBackend};

    let manager = SystemdManagerDouble::default();
    manager
        .states
        .lock()
        .expect("systemd state lock")
        .insert("koa-a.service".to_owned(), adapters::UnitState::Inactive);
    let adapter = adapters::SystemdBackendAdapter::new(
        manager,
        [
            adapters::ServiceGroupBinding::new("core-services", ["koa-a.service".to_owned()])
                .expect("service group binding is valid"),
        ],
    )
    .expect("systemd adapter configuration is valid");
    let result = adapter
        .restart_service_group(&ServiceGroupRequest {
            service_group: BackendIdentifier::new("core-services").expect("identifier is valid"),
        })
        .expect("declared group restarts");
    assert_eq!(
        result.after_state.get("koa-a.service").map(String::as_str),
        Some("active")
    );
    let error = adapter
        .restart_service_group(&ServiceGroupRequest {
            service_group: BackendIdentifier::new("caller-supplied").expect("identifier is valid"),
        })
        .unwrap_err();
    assert_eq!(error.code(), BackendErrorCode::NotAllowlisted);
}

#[test]
fn mount_adapter_resolves_only_the_declared_volume() {
    use domain::{AllowedRoot, EncryptedVolumeAction, SafePath};
    use ports::{BackendErrorCode, BackendIdentifier, DeclaredVolume, MountBackend, VolumeRequest};

    let runtime = temporary_directory("mount-backend");
    let source_root_path = runtime.join("devices");
    let target_root_path = runtime.join("mounts");
    fs::create_dir(&source_root_path).expect("source root is created");
    fs::create_dir(&target_root_path).expect("target root is created");
    let source_root = AllowedRoot::new("devices", &source_root_path).expect("source root is safe");
    let target_root = AllowedRoot::new("mounts", &target_root_path).expect("target root is safe");
    let volume = DeclaredVolume {
        volume_id: BackendIdentifier::new("vault").expect("volume id is valid"),
        source: SafePath::new(&source_root, "vault-device").expect("source path is safe"),
        target: SafePath::new(&target_root, "vault").expect("target path is safe"),
        filesystem_type: BackendIdentifier::new("ext4").expect("filesystem id is valid"),
        read_only: false,
    };
    let adapter = adapters::MountBackendAdapter::new(MountManagerDouble::default(), [volume])
        .expect("mount adapter configuration is valid");
    let result = adapter
        .apply_volume_action(&VolumeRequest {
            volume_id: BackendIdentifier::new("vault").expect("volume id is valid"),
            action: EncryptedVolumeAction::Mount,
        })
        .expect("declared volume mounts");
    assert_eq!(
        result.after_state.get("mounted").map(String::as_str),
        Some("true")
    );
    let error = adapter
        .apply_volume_action(&VolumeRequest {
            volume_id: BackendIdentifier::new("vault").expect("volume id is valid"),
            action: EncryptedVolumeAction::Rotate,
        })
        .unwrap_err();
    assert_eq!(error.code(), BackendErrorCode::UnsupportedOperation);
    fs::remove_dir_all(runtime).expect("mount test directory is removed");
}

#[test]
fn network_adapter_activates_only_a_bound_policy_after_expected_state_check() {
    use ports::{BackendErrorCode, BackendIdentifier, NetworkBackend, NetworkPolicyRequest};

    let active = Arc::new(Mutex::new("network-policy:old".to_owned()));
    let manager = NetworkManagerDouble {
        active: Arc::clone(&active),
    };
    let adapter = adapters::NetworkBackendAdapter::new(
        manager,
        [
            adapters::NetworkPolicyBinding::new("locked-down", "network-policy:new")
                .expect("policy binding is valid"),
        ],
    )
    .expect("network adapter configuration is valid");
    let result = adapter
        .activate_network_policy(&NetworkPolicyRequest {
            policy_id: BackendIdentifier::new("locked-down").expect("policy id is valid"),
            expected_state_ref: "network-policy:old".to_owned(),
        })
        .expect("declared network policy activates");
    assert_eq!(
        result
            .after_state
            .get("active_policy_ref")
            .map(String::as_str),
        Some("network-policy:new")
    );
    let error = adapter
        .activate_network_policy(&NetworkPolicyRequest {
            policy_id: BackendIdentifier::new("locked-down").expect("policy id is valid"),
            expected_state_ref: "network-policy:stale".to_owned(),
        })
        .unwrap_err();
    assert_eq!(error.code(), BackendErrorCode::Conflict);
}

#[test]
fn policy_decision_must_remain_bound_and_current() {
    use domain::{AuthorizationClass, Operation};
    use ports::{
        PolicyClientErrorCode, PolicyDecisionRecord, PolicyDecisionStatus, PolicyEvaluationRequest,
    };

    let request = PolicyEvaluationRequest {
        request_id: "request-1".to_owned(),
        operation: Operation::ActivateSystemArtifact,
        authorization_class: AuthorizationClass::SystemArtifactActivation,
        caller_identity_ref: "identity:operator".to_owned(),
        service_identity_ref: "service:lifecycle".to_owned(),
        profile_context_ref: "profile:sovereign-node".to_owned(),
        target_refs: ["artifact:system-1".to_owned()].into_iter().collect(),
        expected_state_ref: Some("state:stable".to_owned()),
        requested_at: 100,
        expires_at: 200,
    };
    let decision = PolicyDecisionRecord {
        decision_ref: "decision:1".to_owned(),
        request_id: "request-1".to_owned(),
        operation: Operation::ActivateSystemArtifact,
        status: PolicyDecisionStatus::Approved,
        reason_codes: ["POLICY_APPROVED".to_owned()].into_iter().collect(),
        not_before: 100,
        expires_at: 180,
        authority_refs: ["authority:governance-policy-runtime".to_owned()]
            .into_iter()
            .collect(),
    };
    decision
        .validate_for(&request, 120)
        .expect("current bound decision is accepted");
    assert_eq!(
        decision.validate_for(&request, 180).unwrap_err().code(),
        PolicyClientErrorCode::DecisionExpired
    );
}

#[test]
fn system_clock_port_returns_a_unix_reading() {
    use ports::Clock;
    assert!(
        adapters::SystemClock
            .now_unix_seconds()
            .expect("system clock is representable")
            > 0
    );
}
