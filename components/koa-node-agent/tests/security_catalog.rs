//! Security evidence for TEST-COMP-NODE-001, TEST-COMP-NODE-002, and
//! TEST-COMP-NODE-012.
//!
//! These tests deliberately inspect the canonical contract and the broker
//! boundary. They do not execute privileged operations.

use std::collections::BTreeSet;
use std::fs;
use std::path::{Path, PathBuf};

const EXPECTED_OPERATIONS: &[&str] = &[
    "inspect_node_state",
    "stage_system_artifact",
    "activate_system_artifact",
    "activate_service_bundle",
    "activate_governance_bundle",
    "manage_knowledge_artifact",
    "import_offline_bundle",
    "manage_declared_encrypted_volume",
    "restart_allowlisted_service_group",
    "rotate_node_scoped_key",
    "export_node_evidence",
    "enter_recovery_target",
    "execute_rollback_or_forward_repair",
];

const PROHIBITED_OPERATION_NAMES: &[&str] = &[
    "run_command",
    "execute_shell",
    "exec_shell",
    "systemctl",
    "manage_service",
    "copy_file",
    "write_file",
    "run_container",
    "install_package",
    "export_private_key",
];

fn component_root() -> PathBuf {
    PathBuf::from(option_env!("CARGO_MANIFEST_DIR").unwrap_or("."))
}

fn repository_root() -> PathBuf {
    component_root()
        .parent()
        .and_then(Path::parent)
        .expect("component must be located below components/koa-node-agent")
        .to_path_buf()
}

fn read_component(relative: &str) -> String {
    let path = component_root().join(relative);
    fs::read_to_string(&path)
        .unwrap_or_else(|error| panic!("required dependency file {}: {error}", path.display()))
}

fn read_repository(relative: &str) -> String {
    let path = repository_root().join(relative);
    fs::read_to_string(&path)
        .unwrap_or_else(|error| panic!("required authority file {}: {error}", path.display()))
}

fn json_string_values_for_key(document: &str, key: &str) -> Vec<String> {
    let needle = format!("\"{key}\"");
    let mut values = Vec::new();
    let mut remaining = document;

    while let Some(key_offset) = remaining.find(&needle) {
        remaining = &remaining[key_offset + needle.len()..];
        let colon = remaining
            .find(':')
            .expect("JSON key must be followed by a colon");
        remaining = &remaining[colon + 1..];
        let quote = remaining
            .find('"')
            .expect("operation_id must be a JSON string");
        remaining = &remaining[quote + 1..];

        let bytes = remaining.as_bytes();
        let mut end = 0;
        let mut escaped = false;
        for (index, byte) in bytes.iter().enumerate() {
            if escaped {
                escaped = false;
                continue;
            }
            match byte {
                b'\\' => escaped = true,
                b'"' => {
                    end = index;
                    break;
                }
                _ => {}
            }
        }
        assert!(end > 0, "unterminated JSON string for {key}");
        values.push(remaining[..end].to_owned());
        remaining = &remaining[end + 1..];
    }

    values
}

fn count_quoted_literal(source: &str, value: &str) -> usize {
    source.matches(&format!("\"{value}\"")).count()
}

fn assert_no_shell_bridge(source_name: &str, source: &str) {
    let compact = source.replace(char::is_whitespace, "").to_ascii_lowercase();
    for forbidden in [
        "command::new(\"sh\")",
        "command::new(\"bash\")",
        "command::new(\"zsh\")",
        ".arg(\"-c\")",
        "shell=true",
        "/bin/sh",
        "/bin/bash",
    ] {
        assert!(
            !compact.contains(forbidden),
            "{source_name} contains prohibited shell bridge {forbidden}"
        );
    }
}

#[test]
fn canonical_contract_defines_exact_closed_operation_set() {
    let contract = read_repository("docs/contracts/components/koa-node-agent.component.json");
    let discovered: BTreeSet<_> = json_string_values_for_key(&contract, "operation_id")
        .into_iter()
        .collect();
    let expected: BTreeSet<_> = EXPECTED_OPERATIONS
        .iter()
        .map(|operation| (*operation).to_owned())
        .collect();

    assert_eq!(discovered, expected, "canonical operation set drifted");
    assert!(contract.contains("\"closed_allowlist\": true"));
    assert!(contract.contains("\"unregistered_operation_result\": \"rejected\""));
}

#[test]
fn broker_catalog_contains_every_canonical_operation() {
    let catalog = read_component("src/broker/catalog.rs");

    for operation in EXPECTED_OPERATIONS {
        assert!(
            count_quoted_literal(&catalog, operation) >= 1,
            "catalog omits canonical operation {operation}"
        );
    }

    for prohibited in PROHIBITED_OPERATION_NAMES {
        assert_eq!(
            count_quoted_literal(&catalog, prohibited),
            0,
            "catalog exposes prohibited generic operation {prohibited}"
        );
    }
}

#[test]
fn privileged_boundary_does_not_bridge_to_a_shell_or_ai() {
    for relative in [
        "src/broker/catalog.rs",
        "src/broker/operations.rs",
        "src/broker/sandbox.rs",
        "src/bin/koa-privileged-broker.rs",
    ] {
        let source = read_component(relative);
        assert_no_shell_bridge(relative, &source);
        let lowercase = source.to_ascii_lowercase();
        for forbidden in ["openai", "chatgpt", "anthropic", "ollama", "llm"] {
            assert!(
                !lowercase.contains(forbidden),
                "{relative} contains prohibited AI authority marker {forbidden}"
            );
        }
    }
}

#[test]
fn package_manifest_preserves_the_closed_privilege_boundary() {
    let payload = read_component("packaging/payload.toml");

    for assertion in [
        "closed = true",
        "unregistered_operation_result = \"rejected\"",
        "caller_supplied_executable = false",
        "caller_supplied_service_unit = false",
        "caller_supplied_host_path = false",
        "arbitrary_shell_execution = false",
        "arbitrary_service_manager_control = false",
        "path_traversal = false",
        "raw_private_key_export = false",
        "public_network_listener = false",
    ] {
        assert!(payload.contains(assertion), "payload omits {assertion}");
    }
}
