//! Integration evidence for the profile-defined systemd adapter.
//!
//! The test keeps systemd outside the unit-test trust boundary: it inspects the
//! fixed adapter and package contract and never mutates the host running tests.

use std::fs;
use std::path::PathBuf;

fn component_root() -> PathBuf {
    PathBuf::from(option_env!("CARGO_MANIFEST_DIR").unwrap_or("."))
}

fn read_component(relative: &str) -> String {
    let path = component_root().join(relative);
    fs::read_to_string(&path)
        .unwrap_or_else(|error| panic!("required dependency file {}: {error}", path.display()))
}

fn compact_lowercase(source: &str) -> String {
    source.replace(char::is_whitespace, "").to_ascii_lowercase()
}

#[test]
fn systemd_adapter_uses_argument_vector_without_a_shell() {
    let source = read_component("src/adapters/systemd_backend.rs");
    let compact = compact_lowercase(&source);

    assert!(
        compact.contains("command::new(\"systemctl\")")
            || compact.contains("command::new(systemctl"),
        "systemd backend must invoke a fixed systemctl executable"
    );
    assert!(
        compact.contains(".arg(") || compact.contains(".args("),
        "systemd backend must construct an argument vector"
    );

    for forbidden in [
        "command::new(\"sh\")",
        "command::new(\"bash\")",
        ".arg(\"-c\")",
        "/bin/sh",
        "/bin/bash",
        "shell=true",
    ] {
        assert!(
            !compact.contains(forbidden),
            "systemd backend contains prohibited shell pattern {forbidden}"
        );
    }
}

#[test]
fn systemd_adapter_does_not_expose_generic_service_manager_control() {
    let source = read_component("src/adapters/systemd_backend.rs");

    assert!(
        source.contains("restart") || source.contains("Restart"),
        "systemd adapter lacks the declared restart transition"
    );
    let compact = compact_lowercase(&source);
    for prohibited_verb in [
        ".arg(\"start\")",
        ".arg(\"stop\")",
        ".arg(\"enable\")",
        ".arg(\"disable\")",
        ".arg(\"mask\")",
        ".arg(\"unmask\")",
        ".arg(\"isolate\")",
        ".arg(\"reboot\")",
        ".arg(\"poweroff\")",
        ".arg(\"kill\")",
    ] {
        assert!(
            !compact.contains(prohibited_verb),
            "systemd adapter exposes undeclared verb {prohibited_verb}"
        );
    }
}

#[test]
fn restart_target_is_resolved_from_the_closed_catalog() {
    let catalog = read_component("src/broker/catalog.rs");
    let operations = read_component("src/broker/operations.rs");
    let backend = read_component("src/adapters/systemd_backend.rs");
    let joined = format!("{catalog}\n{operations}\n{backend}").to_ascii_lowercase();

    assert!(
        joined.contains("restart_allowlisted_service_group"),
        "closed service-group operation is absent"
    );
    assert!(
        joined.contains("allowlist")
            || joined.contains("allowed_service")
            || joined.contains("service_group"),
        "service target is not visibly bound to a declared group"
    );
    for forbidden in [
        "request.parameters[\"unit\"]",
        "request.parameters.get(\"unit\")",
        "request.unit",
        "caller_unit",
    ] {
        assert!(
            !compact_lowercase(&joined).contains(forbidden),
            "raw caller unit reaches the systemd boundary: {forbidden}"
        );
    }
}

#[test]
fn payload_installs_three_separate_entrypoints_and_local_sockets() {
    let payload = read_component("packaging/payload.toml");

    for required in [
        "/usr/libexec/koa/koa-node-agent",
        "/usr/libexec/koa/koa-privileged-broker",
        "/usr/bin/koa-node-agentctl",
        "/run/koa/sockets/koa-node-agent.sock",
        "/run/koa/sockets/koa-privileged-broker.sock",
        "privileged_broker_is_separate_process = true",
        "local_authenticated_transport_only = true",
        "public_network_listener = false",
    ] {
        assert!(payload.contains(required), "payload omits {required}");
    }
}

#[test]
fn binaries_remain_distinct_at_the_source_boundary() {
    for relative in [
        "src/bin/koa-node-agent.rs",
        "src/bin/koa-privileged-broker.rs",
        "src/bin/koa-node-agentctl.rs",
    ] {
        let source = read_component(relative);
        assert!(
            source.contains("fn main") || source.contains("async fn main"),
            "{relative} does not define an executable entrypoint"
        );
    }
}
