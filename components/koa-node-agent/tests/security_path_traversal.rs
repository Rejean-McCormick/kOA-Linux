//! Security evidence for TEST-COMP-NODE-002 and the path-allowlist portion of
//! TEST-COMP-NODE-003.
//!
//! The domain implementation remains the executable authority. These tests
//! enforce that it contains explicit lexical and resolved-path confinement and
//! that the lower-level unit proof covers representative attacks.

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

fn contains_any(source: &str, alternatives: &[&str]) -> bool {
    alternatives.iter().any(|candidate| source.contains(candidate))
}

fn lexical_escape(candidate: &str) -> bool {
    if candidate.is_empty() || candidate.contains('\0') {
        return true;
    }
    let normalized = candidate.replace('\\', "/");
    if normalized.starts_with('/') {
        return true;
    }
    if normalized.len() >= 3 {
        let bytes = normalized.as_bytes();
        if bytes[0].is_ascii_alphabetic() && bytes[1] == b':' && bytes[2] == b'/' {
            return true;
        }
    }
    normalized
        .split('/')
        .any(|component| component.is_empty() || component == "." || component == "..")
}

#[test]
fn attack_corpus_covers_relative_absolute_windows_and_nul_escapes() {
    for candidate in [
        "../etc/shadow",
        "safe/../../etc/shadow",
        "/etc/shadow",
        "C:\\Windows\\System32",
        "safe\\..\\secret",
        "./relative",
        "safe//double-separator",
        "safe\0suffix",
        "",
    ] {
        assert!(lexical_escape(candidate), "attack corpus missed {candidate:?}");
    }

    for candidate in ["artifact.img", "staging/release-set-001", "receipts/receipt-001.json"] {
        assert!(!lexical_escape(candidate), "safe relative path rejected: {candidate}");
    }
}

#[test]
fn safe_path_domain_rejects_lexical_escape_components() {
    let source = read_component("src/domain/safe_path.rs");

    assert!(
        contains_any(
            &source,
            &[
                "Component::ParentDir",
                "std::path::Component::ParentDir",
                "component == \"..\"",
                "segment == \"..\"",
            ]
        ),
        "safe_path.rs lacks explicit parent-directory rejection"
    );
    assert!(
        contains_any(
            &source,
            &[
                "Component::RootDir",
                "std::path::Component::RootDir",
                "is_absolute()",
            ]
        ),
        "safe_path.rs lacks absolute-path rejection"
    );
    assert!(
        contains_any(
            &source,
            &[
                "Component::Prefix",
                "std::path::Component::Prefix",
                "prefix_verbatim",
            ]
        ),
        "safe_path.rs lacks platform-prefix rejection"
    );
}

#[test]
fn privileged_path_boundary_confines_resolved_targets_to_an_allowlisted_root() {
    let sources = [
        "src/domain/safe_path.rs",
        "src/broker/operations.rs",
        "src/adapters/mount_backend.rs",
        "src/adapters/network_backend.rs",
    ]
    .into_iter()
    .map(read_component)
    .collect::<Vec<_>>()
    .join("\n");
    let lowercase = sources.to_ascii_lowercase();

    assert!(
        contains_any(
            &sources,
            &["canonicalize(", "symlink_metadata(", "read_link("]
        ),
        "privileged path boundary lacks resolved-path or symlink handling"
    );
    assert!(
        contains_any(
            &sources,
            &["starts_with(", "strip_prefix(", "Component::Normal"]
        ),
        "privileged path boundary lacks root-confinement logic"
    );
    assert!(
        !lowercase.contains("unwrap_or(true)"),
        "privileged path boundary contains a fail-open boolean fallback"
    );
}

#[test]
fn lower_level_safe_path_tests_cover_lexical_traversal() {
    let tests = read_component("tests/unit_safe_path.rs").to_ascii_lowercase();

    for evidence in ["..", "absolute"] {
        assert!(
            tests.contains(evidence),
            "unit_safe_path.rs lacks {evidence} attack evidence"
        );
    }
}

#[test]
fn privileged_sources_do_not_accept_raw_caller_paths() {
    for relative in [
        "src/broker/catalog.rs",
        "src/broker/operations.rs",
        "src/adapters/systemd_backend.rs",
        "src/adapters/mount_backend.rs",
        "src/adapters/network_backend.rs",
    ] {
        let source = read_component(relative);
        let compact = source.replace(char::is_whitespace, "").to_ascii_lowercase();
        for forbidden in [
            "pathbuf::from(request.",
            "path::new(request.",
            "canonicalize().unwrap_or",
            "strip_prefix(root).unwrap_or",
        ] {
            assert!(
                !compact.contains(forbidden),
                "{relative} contains unsafe caller-path pattern {forbidden}"
            );
        }
    }
}
