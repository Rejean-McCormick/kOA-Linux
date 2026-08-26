use std::str::FromStr;

use koa_node_agent::application::{
    dispatch, execute_operation, ExecutionFailureCode, RequestValidationErrorCode,
    ValidationContext,
};
use koa_node_agent::domain::{
    AllowedRoot, AuthorizationDecision, AuthorizationDecisionParts, AuthorizationStatus,
    CanonicalReference, ExpectedState, Identifier, NodeOperationRequest, NodeOperationRequestParts,
    Operation, OperationParameters, ReplayDisposition, RequestDeadline, RequestIdentityBinding,
    SafePath,
};

fn identifier(value: &str) -> Identifier {
    Identifier::new(value).unwrap()
}

fn reference(value: &str) -> CanonicalReference {
    CanonicalReference::new(value).unwrap()
}

fn stage_request(targets: Vec<&str>, expires_at: u64) -> NodeOperationRequest {
    let root = AllowedRoot::new("staging", "/var/lib/koa/staging").unwrap();
    let path = SafePath::new(&root, "system/candidate.raw").unwrap();
    NodeOperationRequest::new(NodeOperationRequestParts::version_1(
        Operation::StageSystemArtifact,
        identifier("request-001"),
        identifier("idem-001"),
        reference("identity:operator-1"),
        reference("service:lifecycle-manager"),
        reference("contracts/profiles/sovereign-linux-node.profile.json"),
        Some(reference("decision:001")),
        targets.into_iter().map(reference).collect(),
        Some(ExpectedState::new(reference("node-state:stable"), None)),
        OperationParameters::StageSystemArtifact { staging_path: path },
        RequestDeadline::new(100, expires_at).unwrap(),
        identifier("correlation-001"),
    ))
    .unwrap()
}

fn stage_authorization(expires_at: u64) -> AuthorizationDecision {
    AuthorizationDecision::new(AuthorizationDecisionParts {
        decision_ref: Some(reference("decision:001")),
        status: AuthorizationStatus::Approved,
        operation: Operation::StageSystemArtifact,
        authorization_class: Operation::StageSystemArtifact.authorization_class(),
        caller_identity: reference("identity:operator-1"),
        service_identity: reference("service:lifecycle-manager"),
        profile_context_ref: reference("contracts/profiles/sovereign-linux-node.profile.json"),
        target_scope: vec![reference("artifact:system-1")],
        expected_state_ref: Some(reference("node-state:stable")),
        not_before: 90,
        expires_at,
    })
    .unwrap()
}

fn validation_context(now: u64) -> ValidationContext {
    let mut context = ValidationContext::new(now, 600);
    context.enable_operation(Operation::StageSystemArtifact);
    context.permit_service_identity("service:lifecycle-manager");
    context.allow_path_root(AllowedRoot::new("staging", "/var/lib/koa/staging").unwrap());
    context.require_policy_decision(Operation::StageSystemArtifact);
    context
}

#[test]
fn operation_catalog_is_closed_and_complete() {
    let identifiers: Vec<_> = Operation::ALL
        .iter()
        .map(|operation| operation.as_str())
        .collect();
    assert_eq!(identifiers.len(), 13);
    assert_eq!(identifiers[0], "inspect_node_state");
    assert_eq!(identifiers[12], "execute_rollback_or_forward_repair");
    assert!(Operation::from_str("run_shell").is_err());
    assert!(Operation::from_str("restart_systemd_unit").is_err());
}

#[test]
fn operation_metadata_matches_the_contract() {
    assert!(!Operation::InspectNodeState.mutates_host());
    assert!(!Operation::ExportNodeEvidence.mutates_host());
    assert!(Operation::ActivateSystemArtifact.mutates_host());
    assert_eq!(
        Operation::RestartAllowlistedServiceGroup
            .authorization_class()
            .as_str(),
        "service_group_control"
    );
    assert_eq!(
        Operation::ExecuteRollbackOrForwardRepair
            .authorization_class()
            .as_str(),
        "node_recovery"
    );
}

#[test]
fn request_rejects_a_parameter_schema_for_another_operation() {
    let result = NodeOperationRequest::new(NodeOperationRequestParts::version_1(
        Operation::ActivateSystemArtifact,
        identifier("request-001"),
        identifier("idem-001"),
        reference("identity:operator-1"),
        reference("service:lifecycle-manager"),
        reference("profile:node"),
        Some(reference("decision:001")),
        vec![reference("artifact:system-1")],
        Some(ExpectedState::new(reference("state:stable"), None)),
        OperationParameters::ActivateServiceBundle,
        RequestDeadline::new(100, 200).unwrap(),
        identifier("correlation-001"),
    ));
    assert!(result.is_err());
}

#[test]
fn canonical_request_body_is_independent_of_target_input_order() {
    let first = stage_request(vec!["artifact:system-1", "artifact:dependency-1"], 200);
    let second = stage_request(vec!["artifact:dependency-1", "artifact:system-1"], 200);
    assert_eq!(first.canonical_body(), second.canonical_body());
}

#[test]
fn idempotency_binding_rejects_same_identity_with_different_body() {
    let original = stage_request(vec!["artifact:system-1"], 200);
    let changed = stage_request(vec!["artifact:system-1"], 201);
    let binding = RequestIdentityBinding::from_request(&original);

    assert_eq!(
        binding.compare(&original),
        ReplayDisposition::EquivalentReplay
    );
    assert_eq!(
        binding.compare(&changed),
        ReplayDisposition::IdentityConflict
    );
}

#[test]
fn valid_request_dispatches_to_one_fixed_route() {
    let plan = dispatch(
        stage_request(vec!["artifact:system-1"], 200),
        stage_authorization(190),
        &validation_context(120),
    )
    .unwrap();

    assert_eq!(plan.route().as_str(), "stage_system_artifact");
    assert!(plan.validated_request().receipt_required());
}

#[test]
fn disabled_operation_is_rejected_before_execution() {
    let context = ValidationContext::new(120, 600);
    let error = dispatch(
        stage_request(vec!["artifact:system-1"], 200),
        stage_authorization(190),
        &context,
    )
    .unwrap_err();
    assert_eq!(error.code(), RequestValidationErrorCode::OperationDisabled);
}

#[test]
fn unallowlisted_path_root_is_rejected() {
    let error = dispatch(
        stage_request(vec!["artifact:system-1"], 200),
        stage_authorization(190),
        &{
            let mut no_staging = ValidationContext::new(120, 600);
            no_staging.enable_operation(Operation::StageSystemArtifact);
            no_staging.permit_service_identity("service:lifecycle-manager");
            no_staging.allow_path_root(AllowedRoot::new("other", "/srv/other").unwrap());
            no_staging.require_policy_decision(Operation::StageSystemArtifact);
            no_staging
        },
    )
    .unwrap_err();
    assert_eq!(
        error.code(),
        RequestValidationErrorCode::PathRootNotAllowlisted
    );
}

#[test]
fn authorization_scope_must_cover_every_target() {
    let error = dispatch(
        stage_request(vec!["artifact:system-1", "artifact:dependency-1"], 200),
        stage_authorization(190),
        &validation_context(120),
    )
    .unwrap_err();
    assert_eq!(
        error.code(),
        RequestValidationErrorCode::AuthorizationTargetScopeMismatch
    );
}

#[test]
fn policy_decision_reference_is_mandatory_for_mutation_when_configured() {
    let request = NodeOperationRequest::new(NodeOperationRequestParts::version_1(
        Operation::StageSystemArtifact,
        identifier("request-001"),
        identifier("idem-001"),
        reference("identity:operator-1"),
        reference("service:lifecycle-manager"),
        reference("contracts/profiles/sovereign-linux-node.profile.json"),
        None,
        vec![reference("artifact:system-1")],
        Some(ExpectedState::new(reference("node-state:stable"), None)),
        OperationParameters::StageSystemArtifact {
            staging_path: SafePath::new(
                &AllowedRoot::new("staging", "/var/lib/koa/staging").unwrap(),
                "system/candidate.raw",
            )
            .unwrap(),
        },
        RequestDeadline::new(100, 200).unwrap(),
        identifier("correlation-001"),
    ))
    .unwrap();

    let mut context = ValidationContext::new(120, 600);
    context.enable_operation(Operation::StageSystemArtifact);
    context.permit_service_identity("service:lifecycle-manager");
    context.allow_path_root(AllowedRoot::new("staging", "/var/lib/koa/staging").unwrap());

    let error = dispatch(request, stage_authorization(190), &context).unwrap_err();
    assert_eq!(
        error.code(),
        RequestValidationErrorCode::AuthorizationDecisionReferenceRequired
    );
}

#[test]
fn expired_request_never_invokes_the_adapter() {
    let plan = dispatch(
        stage_request(vec!["artifact:system-1"], 200),
        stage_authorization(190),
        &validation_context(120),
    )
    .unwrap();
    let mut invoked = false;
    let result = execute_operation(&plan, 200, |_| {
        invoked = true;
        Ok::<_, koa_node_agent::application::ExecutionFailure>(())
    });

    assert!(!invoked);
    assert_eq!(
        result.unwrap_err().code(),
        ExecutionFailureCode::DeadlineExpired
    );
}

#[test]
fn authorization_is_revalidated_immediately_before_execution() {
    let plan = dispatch(
        stage_request(vec!["artifact:system-1"], 220),
        stage_authorization(150),
        &validation_context(120),
    )
    .unwrap();
    let mut invoked = false;
    let result = execute_operation(&plan, 150, |_| {
        invoked = true;
        Ok::<_, koa_node_agent::application::ExecutionFailure>(())
    });

    assert!(!invoked);
    assert_eq!(
        result.unwrap_err().code(),
        ExecutionFailureCode::AuthorizationExpired
    );
}

#[test]
fn fixed_adapter_receives_only_a_typed_directive() {
    let plan = dispatch(
        stage_request(vec!["artifact:system-1"], 200),
        stage_authorization(190),
        &validation_context(120),
    )
    .unwrap();
    let result = execute_operation(&plan, 130, |directive| {
        assert_eq!(directive.route().as_str(), "stage_system_artifact");
        assert_eq!(directive.request_id(), "request-001");
        assert_eq!(directive.target_refs(), &["artifact:system-1".to_owned()]);
        assert_eq!(directive.expected_state_ref(), Some("node-state:stable"));
        assert!(matches!(
            directive.parameters(),
            OperationParameters::StageSystemArtifact { .. }
        ));
        assert!(directive.mutates_host());
        assert!(directive.receipt_required());
        Ok::<_, koa_node_agent::application::ExecutionFailure>("staged")
    })
    .unwrap();

    assert_eq!(*result.value(), "staged");
    assert_eq!(result.response().as_str(), "completed");
    assert!(result.receipt_required());
}
