use std::path::Path;

use koa_node_agent::domain::{AllowedRoot, SafePath, SafePathErrorCode};

#[test]
fn resolves_a_normal_relative_path_under_an_allowlisted_root() {
    let root = AllowedRoot::new("staging", "/var/lib/koa/staging").unwrap();
    let path = SafePath::new(&root, "system/image.raw").unwrap();

    assert_eq!(path.root(), &root);
    assert_eq!(path.relative(), Path::new("system/image.raw"));
    assert_eq!(
        path.resolved(),
        std::path::PathBuf::from("/var/lib/koa/staging/system/image.raw")
    );
    assert_eq!(path.canonical(), "staging:system/image.raw");
}

#[test]
fn rejects_a_relative_allowlisted_root() {
    let error = AllowedRoot::new("staging", "var/lib/koa/staging").unwrap_err();
    assert_eq!(error.code(), SafePathErrorCode::RootMustBeAbsolute);
}

#[test]
fn rejects_the_filesystem_root_as_unbounded() {
    let error = AllowedRoot::new("everything", "/").unwrap_err();
    assert_eq!(error.code(), SafePathErrorCode::RootMustBeBounded);
}

#[test]
fn rejects_parent_traversal() {
    let root = AllowedRoot::new("staging", "/var/lib/koa/staging").unwrap();
    let error = SafePath::new(&root, "images/../../etc/shadow").unwrap_err();
    assert_eq!(error.code(), SafePathErrorCode::PathContainsTraversal);
}

#[test]
fn rejects_absolute_request_paths() {
    let root = AllowedRoot::new("staging", "/var/lib/koa/staging").unwrap();
    let error = SafePath::new(&root, "/etc/shadow").unwrap_err();
    assert_eq!(error.code(), SafePathErrorCode::PathMustBeRelative);
}

#[test]
fn rejects_current_directory_components() {
    let root = AllowedRoot::new("staging", "/var/lib/koa/staging").unwrap();
    let error = SafePath::new(&root, "images/./candidate.raw").unwrap_err();
    assert_eq!(error.code(), SafePathErrorCode::PathContainsTraversal);
}

#[test]
fn rejects_invalid_root_identifiers() {
    let error = AllowedRoot::new("staging root", "/var/lib/koa/staging").unwrap_err();
    assert_eq!(error.code(), SafePathErrorCode::InvalidRootId);
}

#[test]
fn roots_are_compared_by_identity_and_path() {
    let first = AllowedRoot::new("staging", "/var/lib/koa/staging").unwrap();
    let same = AllowedRoot::new("staging", "/var/lib/koa/staging").unwrap();
    let different_path = AllowedRoot::new("staging", "/srv/koa/staging").unwrap();
    let safe = SafePath::new(&first, "candidate.raw").unwrap();

    assert!(safe.belongs_to(&same));
    assert!(!safe.belongs_to(&different_path));
}

#[test]
fn rejects_windows_style_paths_independently_of_host_path_syntax() {
    let root = AllowedRoot::new("staging", "/var/lib/koa/staging").unwrap();

    for candidate in [
        r"C:\Windows\System32",
        "C:/Windows/System32",
        r"\\server\share\artifact.raw",
        r"safe\..\secret",
    ] {
        let error = SafePath::new(&root, candidate).unwrap_err();
        assert!(
            matches!(
                error.code(),
                SafePathErrorCode::PathMustBeRelative | SafePathErrorCode::PathContainsTraversal
            ),
            "Windows-style escape was accepted: {candidate:?}"
        );
    }
}
