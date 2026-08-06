use koa_interfaces::client::{ResponseDisposition, ResponseEnvelope};
use koa_interfaces::error::{ErrorCategory, OutcomeKnowledge, TransportErrorKind};
use koa_interfaces::health::{DependencyState, StalenessState};
use koa_interfaces::{
    schema, AuthoritativeOutcome, CapabilityAvailability, CapabilityReadiness,
    CapabilitySnapshot, CapabilitySnapshotEntry,
    CommitState, CorrelationContext, DecisionState, DependencyHealth,
    DependencyRequirement, DisclosureClass, ErrorEnvelope, EventEnvelope,
    ExecutionState, Freshness, HealthStatus, IdempotencyContext, IdentityContext,
    InteractionClass, InterfaceClient, JobRequest, JobStatus, JobTerminality, OperationalState,
    ReadinessStatus, ReceiptClass, ReceiptEnvelope, ReceiptOutcome, Transport,
    TransportError, VersionNegotiation,
};
use serde_json::{json, Value};
use std::collections::BTreeMap;

const FIXTURE_SCHEMA_VERSION: &str = "1.0.0";

#[derive(Clone)]
struct StaticTransport {
    response: Vec<u8>,
}

impl Transport for StaticTransport {
    fn exchange(&self, _request: &[u8]) -> Result<Vec<u8>, TransportError> {
        Ok(self.response.clone())
    }
}

fn correlation() -> CorrelationContext {
    CorrelationContext::new(FIXTURE_SCHEMA_VERSION, "request-001", "workflow-001")
}

fn request() -> EventEnvelope<Value> {
    EventEnvelope {
        schema: schema::EVENT_ENVELOPE.to_owned(),
        schema_version: FIXTURE_SCHEMA_VERSION.to_owned(),
        interface_id: "example.command".to_owned(),
        interface_version: "1.0.0".to_owned(),
        message_id: "message-001".to_owned(),
        interaction_class: InteractionClass::Command,
        sender_component_id: "requesting_component".to_owned(),
        receiver_component_id: "owning_component".to_owned(),
        operation: "change_owned_state".to_owned(),
        correlation: correlation(),
        identity: Some(IdentityContext {
            subject_ref: Some("subject:record-1".to_owned()),
            authority_refs: vec!["policy:decision-1".to_owned()],
            ..IdentityContext::new(FIXTURE_SCHEMA_VERSION, "identity:operator-1")
        }),
        idempotency: Some(IdempotencyContext {
            schema: schema::IDEMPOTENCY.to_owned(),
            schema_version: FIXTURE_SCHEMA_VERSION.to_owned(),
            idempotency_key: "workspace-1:change-1".to_owned(),
            request_digest: "sha256:0123456789abcdef".to_owned(),
            namespace: Some("workspace-1".to_owned()),
        }),
        payload_schema: "components/example/change-request.schema.json".to_owned(),
        created_at: "2026-08-06T12:00:00Z".to_owned(),
        expires_at: None,
        authority_refs: vec!["policy:decision-1".to_owned()],
        evidence_refs: Vec::new(),
        payload: json!({"expected_state": "old", "target_state": "new"}),
    }
}

fn remote_error() -> ErrorEnvelope {
    ErrorEnvelope {
        schema: schema::ERROR_ENVELOPE.to_owned(),
        schema_version: FIXTURE_SCHEMA_VERSION.to_owned(),
        error_id: "error-001".to_owned(),
        error_code: "policy_denied".to_owned(),
        category: ErrorCategory::AuthorizationDenied,
        message: "The requested operation is not authorized.".to_owned(),
        correlation: correlation(),
        retryable: false,
        outcome_knowledge: OutcomeKnowledge::KnownNoEffect,
        retry_after_seconds: None,
        reason_codes: vec!["policy_denied".to_owned()],
        details: BTreeMap::new(),
        recorded_at: "2026-08-06T12:00:01Z".to_owned(),
    }
}

#[test]
fn schema_identifiers_are_repository_relative_and_stable() {
    assert_eq!(schema::EVENT_ENVELOPE, "interfaces/transport/event-envelope.schema.json");
    assert_eq!(schema::ERROR_ENVELOPE, "interfaces/transport/error-envelope.schema.json");
    assert_eq!(schema::IDEMPOTENCY, "interfaces/transport/idempotency.schema.json");
    assert_eq!(
        schema::VERSION_NEGOTIATION,
        "interfaces/transport/version-negotiation.schema.json"
    );
    assert_eq!(schema::HEALTH_STATUS, "interfaces/health/health-status.schema.json");
    assert_eq!(schema::READINESS, "interfaces/health/readiness.schema.json");
    assert_eq!(
        schema::RECEIPT_ENVELOPE,
        "interfaces/receipts/receipt-envelope.schema.json"
    );
    assert_eq!(schema::CORRELATION, "interfaces/receipts/correlation.schema.json");
    assert_eq!(schema::JOB_REQUEST, "interfaces/jobs/job-request.schema.json");
    assert_eq!(schema::JOB_STATUS, "interfaces/jobs/job-status.schema.json");
    assert_eq!(
        schema::IDENTITY_CONTEXT,
        "interfaces/identity/identity-context.schema.json"
    );
    assert_eq!(
        schema::CAPABILITY_SNAPSHOT,
        "interfaces/capabilities/capability-snapshot.schema.json"
    );
}

#[test]
fn version_selection_must_be_offered() {
    let valid = VersionNegotiation {
        schema: schema::VERSION_NEGOTIATION.to_owned(),
        schema_version: FIXTURE_SCHEMA_VERSION.to_owned(),
        interface_id: "example.command".to_owned(),
        supported_versions: vec!["1.0.0".to_owned(), "1.1.0".to_owned()],
        selected_version: Some("1.1.0".to_owned()),
    };
    assert!(valid.validate().is_ok());

    let invalid = VersionNegotiation {
        selected_version: Some("2.0.0".to_owned()),
        ..valid
    };
    assert_eq!(
        invalid.validate().expect_err("selection must fail").field(),
        "selected_version"
    );
}

#[test]
fn event_envelope_round_trips_without_changing_contract_values() {
    let original = request();
    original.validate_metadata().expect("request metadata");
    let encoded = serde_json::to_value(&original).expect("serialize request");
    assert_eq!(encoded["interaction_class"], "command");
    assert_eq!(encoded["schema"], schema::EVENT_ENVELOPE);
    let decoded: EventEnvelope<Value> =
        serde_json::from_value(encoded).expect("deserialize request");
    assert_eq!(decoded, original);
}

#[test]
fn unknown_interaction_class_is_rejected() {
    let mut encoded = serde_json::to_value(request()).expect("serialize request");
    encoded["interaction_class"] = json!("invented_fallback");
    assert!(serde_json::from_value::<EventEnvelope<Value>>(encoded).is_err());
}

#[test]
fn health_preserves_liveness_and_readiness_separation() {
    let mut readiness = BTreeMap::new();
    readiness.insert(koa_interfaces::ReadinessClass::LocalRead, ReadinessStatus::Ready);
    readiness.insert(
        koa_interfaces::ReadinessClass::AuthoritativeWrite,
        ReadinessStatus::Blocked,
    );
    let status = HealthStatus {
        schema: schema::HEALTH_STATUS.to_owned(),
        schema_version: FIXTURE_SCHEMA_VERSION.to_owned(),
        component_id: "example_component".to_owned(),
        instance_id: Some("example-1".to_owned()),
        state: OperationalState::ReadOnly,
        liveness: true,
        startup_complete: true,
        observed_at: "2026-08-06T12:00:00Z".to_owned(),
        capabilities: vec![CapabilityReadiness {
            schema: schema::READINESS.to_owned(),
            schema_version: FIXTURE_SCHEMA_VERSION.to_owned(),
            capability_id: "example.read".to_owned(),
            owner_component_id: "example_component".to_owned(),
            availability: CapabilityAvailability::Degraded,
            observed_state: OperationalState::ReadOnly,
            observed_at: "2026-08-06T12:00:00Z".to_owned(),
            readiness,
            usable_operation_classes: vec!["local_read".to_owned()],
            denied_operation_classes: vec!["authoritative_write".to_owned()],
            dependencies: vec![DependencyHealth {
                dependency_ref: "governance_policy_runtime".to_owned(),
                requirement: DependencyRequirement::RequiredForCapability,
                state: DependencyState::Unavailable,
                observed_at: "2026-08-06T12:00:00Z".to_owned(),
                reason_codes: vec!["dependency_unavailable".to_owned()],
            }],
            active_contract_id: "example-component".to_owned(),
            active_contract_version: "1.0.0".to_owned(),
            active_schema_version: Some("1.0.0".to_owned()),
            active_artifact_refs: Vec::new(),
            reason_codes: vec!["write_policy_unavailable".to_owned()],
            recovery_conditions: vec!["policy_runtime_ready".to_owned()],
            evidence_refs: Vec::new(),
            freshness: vec![Freshness {
                source: "policy_runtime".to_owned(),
                observed_at: "2026-08-06T12:00:00Z".to_owned(),
                expected_refresh_seconds: 30,
                age_seconds: 4,
                staleness: StalenessState::Current,
                effect_on_capability: None,
            }],
        }],
        reason_codes: vec!["write_policy_unavailable".to_owned()],
        evidence_refs: Vec::new(),
    };
    status.validate().expect("health status");
    let value = serde_json::to_value(status).expect("serialize health");
    assert_eq!(value["liveness"], true);
    assert_eq!(value["state"], "read_only");
    assert_eq!(
        value["capabilities"][0]["readiness"]["readiness.authoritative_write"],
        "blocked"
    );
}

#[test]
fn committed_receipt_requires_matching_commit_state_and_timestamp() {
    let mut receipt = ReceiptEnvelope {
        schema: schema::RECEIPT_ENVELOPE.to_owned(),
        receipt_schema_version: FIXTURE_SCHEMA_VERSION.to_owned(),
        receipt_id: "receipt-001".to_owned(),
        receipt_class: ReceiptClass::TransitionReceipt,
        transition_type: "example_change".to_owned(),
        producer_component_id: "owning_component".to_owned(),
        producer_instance_id: Some("owning-component-1".to_owned()),
        subject_ref: "subject:record-1".to_owned(),
        actor_ref: Some("identity:operator-1".to_owned()),
        target_refs: vec!["record:1".to_owned()],
        scope: "component:owning_component".to_owned(),
        correlation: correlation(),
        authority_refs: vec!["policy:decision-1".to_owned()],
        decision: DecisionState::Authorized,
        execution_state: ExecutionState::Completed,
        commit_state: CommitState::Committed,
        outcome: ReceiptOutcome::Committed,
        reason_code: "change_committed".to_owned(),
        requested_at: "2026-08-06T12:00:00Z".to_owned(),
        decided_at: Some("2026-08-06T12:00:01Z".to_owned()),
        committed_at: Some("2026-08-06T12:00:02Z".to_owned()),
        recorded_at: "2026-08-06T12:00:03Z".to_owned(),
        profile_refs: Vec::new(),
        component_contract_refs: vec!["components/owning-component".to_owned()],
        artifact_refs: Vec::new(),
        release_refs: Vec::new(),
        exception_refs: Vec::new(),
        test_refs: Vec::new(),
        evidence_refs: Vec::new(),
        disclosure_class: DisclosureClass::OperatorRestricted,
        retention_class: "critical_transition".to_owned(),
    };
    receipt.validate().expect("valid committed receipt");
    receipt.committed_at = None;
    assert_eq!(
        receipt
            .validate()
            .expect_err("missing commit time must fail")
            .field(),
        "committed_at"
    );
}

#[test]
fn error_retry_delay_requires_retryable_error() {
    let mut error = remote_error();
    error.retry_after_seconds = Some(5);
    assert_eq!(
        error
            .validate()
            .expect_err("non-retryable delay must fail")
            .field(),
        "retry_after_seconds"
    );
    error.retryable = true;
    assert!(error.validate().is_ok());
}

#[test]
fn client_returns_completed_payload() {
    let response = ResponseEnvelope {
        request_id: "request-001".to_owned(),
        correlation_id: "workflow-001".to_owned(),
        disposition: ResponseDisposition::Completed,
        payload: Some(json!({"result": "committed"})),
        error: None,
    };
    let transport = StaticTransport {
        response: serde_json::to_vec(&response).expect("serialize response"),
    };
    let client = InterfaceClient::new(transport);
    let result: Value = client.execute(&request()).expect("completed response");
    assert_eq!(result["result"], "committed");
}

#[test]
fn client_does_not_treat_transport_or_remote_failure_as_success() {
    let response = ResponseEnvelope::<Value> {
        request_id: "request-001".to_owned(),
        correlation_id: "workflow-001".to_owned(),
        disposition: ResponseDisposition::Rejected,
        payload: None,
        error: Some(remote_error()),
    };
    let transport = StaticTransport {
        response: serde_json::to_vec(&response).expect("serialize response"),
    };
    let error = InterfaceClient::new(transport)
        .execute::<_, Value>(&request())
        .expect_err("rejection must remain an error");
    assert!(matches!(error, koa_interfaces::ClientError::Remote(_)));
}

#[test]
fn client_rejects_correlation_mismatch() {
    let response = ResponseEnvelope {
        request_id: "different-request".to_owned(),
        correlation_id: "workflow-001".to_owned(),
        disposition: ResponseDisposition::Completed,
        payload: Some(json!({"result": "committed"})),
        error: None,
    };
    let transport = StaticTransport {
        response: serde_json::to_vec(&response).expect("serialize response"),
    };
    let error = InterfaceClient::new(transport)
        .execute::<_, Value>(&request())
        .expect_err("mismatch must fail");
    assert!(matches!(
        error,
        koa_interfaces::ClientError::InvalidResponse(_)
    ));
}

#[test]
fn job_request_round_trips_with_stable_correlation_and_idempotency() {
    let job = JobRequest {
        schema: schema::JOB_REQUEST.to_owned(),
        schema_version: FIXTURE_SCHEMA_VERSION.to_owned(),
        job_id: "job-001".to_owned(),
        job_type: "example.deferred_work".to_owned(),
        owner_component_id: "owning_component".to_owned(),
        correlation: correlation(),
        identity: Some(IdentityContext::new(FIXTURE_SCHEMA_VERSION, "identity:operator-1")),
        idempotency: Some(IdempotencyContext {
            schema: schema::IDEMPOTENCY.to_owned(),
            schema_version: FIXTURE_SCHEMA_VERSION.to_owned(),
            idempotency_key: "workspace-1:job-001".to_owned(),
            request_digest: "sha256:0123456789abcdef".to_owned(),
            namespace: Some("workspace-1".to_owned()),
        }),
        requested_at: "2026-08-06T12:00:00Z".to_owned(),
        expires_at: None,
        payload_schema: "components/example/job-request.schema.json".to_owned(),
        payload: json!({"task": "rebuild_projection"}),
    };
    job.validate_metadata().expect("job request");
    let value = serde_json::to_value(&job).expect("serialize job request");
    assert_eq!(value["correlation"]["correlation_id"], "workflow-001");
    let decoded: JobRequest<Value> =
        serde_json::from_value(value).expect("deserialize job request");
    assert_eq!(decoded, job);
}

#[test]
fn job_status_keeps_availability_execution_and_outcome_independent() {
    let status = JobStatus::<Value> {
        schema: schema::JOB_STATUS.to_owned(),
        schema_version: FIXTURE_SCHEMA_VERSION.to_owned(),
        job_id: "job-001".to_owned(),
        owner_component_id: "owning_component".to_owned(),
        availability: CapabilityAvailability::DeferredOnly,
        execution_state: ExecutionState::AwaitingDependency,
        authoritative_outcome: AuthoritativeOutcome::NoEffect,
        terminality: JobTerminality::Pending,
        observed_at: "2026-08-06T12:00:00Z".to_owned(),
        reason_codes: vec!["dependency_unavailable".to_owned()],
        result_schema: None,
        result: None,
        receipt_refs: Vec::new(),
    };
    status.validate_metadata().expect("job status");
    let value = serde_json::to_value(status).expect("serialize job status");
    assert_eq!(value["availability"], "deferred_only");
    assert_eq!(value["execution_state"], "awaiting_dependency");
    assert_eq!(value["authoritative_outcome"], "no_effect");
}

#[test]
fn capability_snapshot_preserves_three_independent_state_dimensions() {
    let snapshot = CapabilitySnapshot {
        schema: schema::CAPABILITY_SNAPSHOT.to_owned(),
        schema_version: FIXTURE_SCHEMA_VERSION.to_owned(),
        snapshot_id: "snapshot-001".to_owned(),
        component_id: "owning_component".to_owned(),
        observed_at: "2026-08-06T12:00:00Z".to_owned(),
        profile_refs: vec!["profile:sovereign-linux-node".to_owned()],
        capabilities: vec![CapabilitySnapshotEntry {
            capability_id: "example.publish".to_owned(),
            owner_component_ref: "component:owning_component".to_owned(),
            availability: CapabilityAvailability::Blocked,
            execution_state: ExecutionState::NotStarted,
            authoritative_outcome: AuthoritativeOutcome::NoEffect,
            reason_codes: vec!["policy_unavailable".to_owned()],
        }],
    };
    snapshot.validate().expect("capability snapshot");
    let value = serde_json::to_value(snapshot).expect("serialize snapshot");
    assert_eq!(value["capabilities"][0]["availability"], "blocked");
    assert_eq!(value["capabilities"][0]["execution_state"], "not_started");
    assert_eq!(value["capabilities"][0]["authoritative_outcome"], "no_effect");
}

#[test]
fn transport_error_kind_is_preserved() {
    let error = TransportError::new(TransportErrorKind::Timeout, "deadline exceeded");
    assert_eq!(error.kind(), TransportErrorKind::Timeout);
    assert_eq!(error.message(), "deadline exceeded");
}
