#![forbid(unsafe_code)]

use std::env;
use std::fs;
use std::path::Path;

const COMPONENT_ID: &str = "koa_node_agent";
const COMPONENT_VERSION: &str = "1.0.0";

fn main() {
    println!("cargo:rerun-if-changed=component.toml");
    println!("cargo:rerun-if-changed=README.md");
    println!("cargo:rustc-env=KOA_COMPONENT_ID={COMPONENT_ID}");
    println!("cargo:rustc-env=KOA_COMPONENT_VERSION={COMPONENT_VERSION}");

    let manifest_dir = env::var("CARGO_MANIFEST_DIR").expect("CARGO_MANIFEST_DIR is set by Cargo");
    let component_path = Path::new(&manifest_dir).join("component.toml");
    let content = fs::read_to_string(&component_path)
        .unwrap_or_else(|error| panic!("cannot read {}: {error}", component_path.display()));

    let required = [
        format!("component_id = \"{COMPONENT_ID}\""),
        format!("version = \"{COMPONENT_VERSION}\""),
        "operation_allowlist_is_closed = true".to_owned(),
        "partial_authoritative_activation = false".to_owned(),
        "critical_transition_requires_receipt = true".to_owned(),
    ];
    for marker in required {
        assert!(
            content.lines().any(|line| line.trim() == marker),
            "component.toml is missing required marker: {marker}"
        );
    }
}
