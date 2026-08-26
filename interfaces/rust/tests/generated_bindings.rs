use koa_interfaces::client::{ResponseDisposition, ResponseEnvelope};
use koa_interfaces::error::{
    ErrorAuthoritativeEffect, ErrorAuthority, ErrorCategory, ErrorCorrelationContext,
    ErrorDisclosure, ErrorFinality, ErrorOutcome, ErrorOutcomeState, ErrorRetry,
    ErrorRetryStrategy, TransportErrorKind,
};
use koa_interfaces::health::{HealthFreshness, HealthLiveness, HealthLivenessState, HealthStartup};
use koa_interfaces::{
    AuthoritativeOutcome, CapabilityAvailability, CapabilitySnapshot, CapabilitySnapshotEntry,
    CommitState, CorrelationContext, DecisionState, DisclosureClass, DuplicateHandling,
    ErrorEnvelope, EventAuthority, EventCorrelationContext, EventDisclosure, EventEnvelope,
    EventEvidence, EventInterfaceReference, EventOrdering, EventPayloadRepresentation,
    EventPublisher, EventReceiverKind, EventReceiverSelector, EventReplay, ExecutionState,
    HealthStatus, IdempotencyAntiReplay, IdempotencyAuthority, IdempotencyCanonicalRequest,
    IdempotencyContext, IdempotencyDuplicateHandling, IdempotencyExpectedState, IdempotencyScope,
    IdempotencyValidity, IdentityContext, InterfaceClient, JobRequest, JobStatus, JobTerminality,
    OperationalState, PayloadEncoding, ReceiptClass, ReceiptEnvelope, ReceiptOutcome, ReplayMode,
    Transport, TransportError, VersionCompatibilityMode, VersionNegotiation,
    VersionNegotiationAuthority, VersionNegotiationMessageType, VersionNegotiationSender,
    VersionReceiverKind, VersionReceiverSelector, schema,
};
use serde_json::{Value, json};

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
        schema_version: FIXTURE_SCHEMA_VERSION.to_owned(),
        envelope_type: "domain_event".to_owned(),
        message_id: "message-001".to_owned(),
        event_id: "event-001".to_owned(),
        event_type: "example.change_committed".to_owned(),
        event_version: "1.0.0".to_owned(),
        interface: EventInterfaceReference {
            interface_id: "example.events".to_owned(),
            interface_version: "1.0.0".to_owned(),
            contract_ref: Some("docs/contracts/components/example.component.json".to_owned()),
        },
        publisher: EventPublisher {
            component_id: "owning_component".to_owned(),
            instance_id: None,
            profile_id: None,
        },
        intended_receivers: vec![EventReceiverSelector {
            kind: EventReceiverKind::Component,
            identifier: "requesting_component".to_owned(),
        }],
        correlation: EventCorrelationContext {
            correlation_id: "workflow-001".to_owned(),
            request_id: "request-001".to_owned(),
            causation_id: None,
            trace_id: None,
        },
        occurred_at: "2026-08-06T12:00:00Z".to_owned(),
        committed_at: "2026-08-06T12:00:01Z".to_owned(),
        expires_at: None,
        payload_representation: EventPayloadRepresentation {
            media_type: "application/json".to_owned(),
            schema_ref: "components/example/change-event.schema.json".to_owned(),
            schema_version: "1.0.0".to_owned(),
            encoding: Some(PayloadEncoding::Identity),
            content_digest: None,
        },
        payload: json!({"expected_state": "old", "target_state": "new"}),
        ordering: EventOrdering {
            scope: "example.record".to_owned(),
            sequence: 1,
            partition_key: Some("record-001".to_owned()),
        },
        replay: EventReplay {
            mode: ReplayMode::Original,
            duplicate_handling: DuplicateHandling::IgnoreIfApplied,
            original_message_id: None,
            replayed_at: None,
            replay_reason: None,
        },
        compatibility: None,
        disclosure: EventDisclosure {
            class: DisclosureClass::OperatorRestricted,
            payload_minimized: true,
            redaction_applied: None,
        },
        evidence: Some(EventEvidence {
            receipt_refs: vec!["receipt-001".to_owned()],
            evidence_refs: Vec::new(),
        }),
        authority: EventAuthority {
            effect: "committed_fact_evidence".to_owned(),
            publisher_owns_fact: true,
            grants_mutation_authority: false,
            transfers_ownership: false,
        },
    }
}

fn remote_error() -> ErrorEnvelope {
    ErrorEnvelope {
        schema_version: FIXTURE_SCHEMA_VERSION.to_owned(),
        envelope_type: "error".to_owned(),
        error_id: "error-001".to_owned(),
        error_code: "policy_denied".to_owned(),
        error_class: ErrorCategory::Authorization,
        message: "The requested operation is not authorized.".to_owned(),
        reason_codes: vec!["POLICY_DENIED".to_owned()],
        interface: EventInterfaceReference {
            interface_id: "example.command".to_owned(),
            interface_version: "1.0.0".to_owned(),
            contract_ref: Some("docs/contracts/components/example.component.json".to_owned()),
        },
        producer: EventPublisher {
            component_id: "owning_component".to_owned(),
            instance_id: None,
            profile_id: None,
        },
        intended_receiver: EventReceiverSelector {
            kind: EventReceiverKind::Component,
            identifier: "requesting_component".to_owned(),
        },
        correlation: ErrorCorrelationContext {
            correlation_id: "workflow-001".to_owned(),
            causation_id: None,
            request_id: Some("request-001".to_owned()),
            trace_id: None,
        },
        occurred_at: "2026-08-06T12:00:01Z".to_owned(),
        payload_representation: None,
        release_context: None,
        outcome: ErrorOutcome {
            state: ErrorOutcomeState::Rejected,
            finality: ErrorFinality::Final,
            authoritative_effect: ErrorAuthoritativeEffect::None,
            status_ref: None,
        },
        retry: ErrorRetry {
            allowed: false,
            strategy: ErrorRetryStrategy::None,
            after_seconds: None,
            maximum_attempts: None,
            idempotency_required: None,
        },
        details: None,
        disclosure: ErrorDisclosure {
            class: DisclosureClass::OperatorRestricted,
            payload_minimized: true,
            contains_secrets: false,
        },
        evidence: None,
        authority: ErrorAuthority {
            transport_grants_authority: false,
            error_grants_authority: false,
            transfers_ownership: false,
        },
    }
}

#[test]
fn schema_identifiers_are_repository_relative_and_stable() {
    assert_eq!(
        schema::EVENT_ENVELOPE,
        "interfaces/transport/event-envelope.schema.json"
    );
    assert_eq!(
        schema::ERROR_ENVELOPE,
        "interfaces/transport/error-envelope.schema.json"
    );
    assert_eq!(
        schema::IDEMPOTENCY,
        "interfaces/transport/idempotency.schema.json"
    );
    assert_eq!(
        schema::VERSION_NEGOTIATION,
        "interfaces/transport/version-negotiation.schema.json"
    );
    assert_eq!(
        schema::HEALTH_STATUS,
        "interfaces/health/health-status.schema.json"
    );
    assert_eq!(schema::READINESS, "interfaces/health/readiness.schema.json");
    assert_eq!(
        schema::RECEIPT_ENVELOPE,
        "interfaces/receipts/receipt-envelope.schema.json"
    );
    assert_eq!(
        schema::CORRELATION,
        "interfaces/receipts/correlation.schema.json"
    );
    assert_eq!(
        schema::JOB_REQUEST,
        "interfaces/jobs/job-request.schema.json"
    );
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
fn version_selection_must_be_explicit_and_offered() {
    let valid = VersionNegotiation {
        schema_version: FIXTURE_SCHEMA_VERSION.to_owned(),
        message_type: VersionNegotiationMessageType::VersionSelection,
        negotiation_id: "negotiation-001".to_owned(),
        interface_id: "example.command".to_owned(),
        sender: VersionNegotiationSender {
            component_id: "example_client".to_owned(),
            instance_id: None,
            profile_id: None,
        },
        intended_receiver: VersionReceiverSelector {
            kind: VersionReceiverKind::Component,
            identifier: "example_server".to_owned(),
        },
        correlation_id: "correlation-001".to_owned(),
        offered_versions: Some(vec!["1.0.0".to_owned(), "1.1.0".to_owned()]),
        preferred_version: None,
        selected_version: Some("1.1.0".to_owned()),
        compatibility_mode: Some(VersionCompatibilityMode::Exact),
        rejection: None,
        release_context: None,
        automatic_schema_guessing: false,
        authority: VersionNegotiationAuthority {
            transport_grants_authority: false,
            selection_changes_domain_authority: false,
            receiving_contract_remains_authoritative: true,
        },
    };
    assert!(valid.validate().is_ok());
    let encoded = serde_json::to_value(&valid).expect("serialize version negotiation");
    assert_eq!(encoded["message_type"], "version_selection");
    assert_eq!(encoded["automatic_schema_guessing"], false);

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
    assert_eq!(encoded["envelope_type"], "domain_event");
    assert_eq!(encoded["interface"]["interface_version"], "1.0.0");
    assert_eq!(encoded["authority"]["grants_mutation_authority"], false);
    let decoded: EventEnvelope<Value> =
        serde_json::from_value(encoded).expect("deserialize request");
    assert_eq!(decoded, original);
}

#[test]
fn unknown_receiver_kind_is_rejected() {
    let mut encoded = serde_json::to_value(request()).expect("serialize request");
    encoded["intended_receivers"][0]["kind"] = json!("invented_fallback");
    assert!(serde_json::from_value::<EventEnvelope<Value>>(encoded).is_err());
}

#[test]
fn health_preserves_liveness_and_readiness_separation() {
    let readiness = json!({
        "schema_version": "1.0.0",
        "readiness_id": "readiness:example_component:local_read:001",
        "component_id": "example_component",
        "component_contract_ref": "docs/contracts/components/example.component.json",
        "capability_id": "local_read",
        "readiness_class": "readiness.local_read",
        "ready": true,
        "operational_state": "healthy",
        "usable_operation_classes": ["read"],
        "denied_operation_classes": [],
        "conditions": [{
            "condition_id": "process_alive",
            "category": "process_liveness",
            "required": true,
            "status": "satisfied",
            "observed_at": "2026-08-06T12:00:00Z"
        }],
        "freshness": {
            "source": "health:example_component",
            "confidence": "direct",
            "staleness_state": "current",
            "observed_at": "2026-08-06T12:00:00Z",
            "age_seconds": 0
        },
        "observed_at": "2026-08-06T12:00:00Z",
        "reason_codes": []
    });
    let status = HealthStatus {
        schema_version: FIXTURE_SCHEMA_VERSION.to_owned(),
        health_report_id: "health:example_component:001".to_owned(),
        component_id: "example_component".to_owned(),
        component_instance_id: Some("example-1".to_owned()),
        component_contract_ref: "docs/contracts/components/example.component.json".to_owned(),
        profile_refs: Vec::new(),
        process_liveness: HealthLiveness {
            state: HealthLivenessState::Alive,
            observed_at: "2026-08-06T12:00:00Z".to_owned(),
            reason_codes: Vec::new(),
        },
        startup: HealthStartup {
            state: OperationalState::Healthy,
            stage: None,
            started_at: Some("2026-08-06T11:59:00Z".to_owned()),
            observed_at: "2026-08-06T12:00:00Z".to_owned(),
            reason_codes: Vec::new(),
        },
        overall_state: OperationalState::Healthy,
        readiness: vec![readiness],
        limitations: Vec::new(),
        freshness: HealthFreshness {
            source: "health:example_component".to_owned(),
            confidence: "direct".to_owned(),
            staleness_state: "current".to_owned(),
            observed_at: "2026-08-06T12:00:00Z".to_owned(),
            valid_until: None,
            expected_refresh_at: None,
            age_seconds: Some(0),
        },
        observed_at: "2026-08-06T12:00:00Z".to_owned(),
        reason_codes: Vec::new(),
        recovery_conditions: Vec::new(),
        evidence_refs: Vec::new(),
        disclosure_class: "machine_readable_local".to_owned(),
    };
    status.validate().expect("health status");
    let value = serde_json::to_value(status).expect("serialize health");
    assert_eq!(value["process_liveness"]["state"], "alive");
    assert_eq!(value["overall_state"], "healthy");
    assert_eq!(
        value["readiness"][0]["readiness_class"],
        "readiness.local_read"
    );
    assert_eq!(value["disclosure_class"], "machine_readable_local");
    assert!(value.get("capabilities").is_none());
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
fn error_retry_object_enforces_canonical_constraints() {
    let mut error = remote_error();
    error.retry.after_seconds = Some(5);
    assert_eq!(
        error
            .validate()
            .expect_err("disabled retry timing must fail")
            .field(),
        "retry.after_seconds"
    );

    error.retry = ErrorRetry {
        allowed: true,
        strategy: ErrorRetryStrategy::BoundedBackoff,
        after_seconds: Some(5),
        maximum_attempts: Some(3),
        idempotency_required: Some(true),
    };
    assert!(error.validate().is_ok());

    let encoded = serde_json::to_value(&error).expect("serialize canonical error");
    assert_eq!(encoded["envelope_type"], "error");
    assert_eq!(encoded["error_class"], "authorization");
    assert!(encoded.get("schema").is_none());
    assert!(encoded.get("category").is_none());
    assert!(encoded.get("retryable").is_none());
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
        identity: Some(IdentityContext::new(
            FIXTURE_SCHEMA_VERSION,
            "identity:operator-1",
        )),
        idempotency: Some(IdempotencyContext {
            schema_version: FIXTURE_SCHEMA_VERSION.to_owned(),
            idempotency_key: "workspace-1:job-001".to_owned(),
            request_id: Some("request-001".to_owned()),
            correlation_id: Some("workflow-001".to_owned()),
            operation: "example.deferred_work".to_owned(),
            owner_component_id: "owning_component".to_owned(),
            scope: IdempotencyScope {
                kind: "owner_operation".to_owned(),
                target_ref: None,
                workflow_id: None,
                step_id: None,
            },
            canonical_request: IdempotencyCanonicalRequest {
                algorithm: "sha256".to_owned(),
                digest: "0".repeat(64),
                media_type: "application/json".to_owned(),
                schema_ref: None,
                schema_version: None,
            },
            expected_state: None::<IdempotencyExpectedState>,
            duplicate_handling: IdempotencyDuplicateHandling {
                action: "return_prior_result".to_owned(),
                result_consistency: "exact_prior_result".to_owned(),
                terminal_result_ref_required: Some(true),
            },
            validity: IdempotencyValidity {
                created_at: "2026-08-06T12:00:00Z".to_owned(),
                expires_at: None,
                retain_terminal_result_seconds: Some(3600),
            },
            anti_replay: None::<IdempotencyAntiReplay>,
            authority: IdempotencyAuthority {
                receiving_owner_enforces: true,
                transport_grants_authority: false,
                duplicate_effects_permitted: false,
            },
        }),
        requested_at: "2026-08-06T12:00:00Z".to_owned(),
        expires_at: None,
        payload_schema: "components/example/job-request.schema.json".to_owned(),
        payload: json!({"task": "rebuild_projection"}),
    };
    job.validate_metadata().expect("job request");
    let value = serde_json::to_value(&job).expect("serialize job request");
    assert_eq!(value["correlation"]["correlation_id"], "workflow-001");
    assert_eq!(
        value["idempotency"]["idempotency_key"],
        "workspace-1:job-001"
    );
    assert_eq!(
        value["idempotency"]["duplicate_handling"]["action"],
        "return_prior_result"
    );
    assert!(value["idempotency"].get("schema").is_none());
    assert!(value["idempotency"].get("request_digest").is_none());
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
    assert_eq!(
        value["capabilities"][0]["authoritative_outcome"],
        "no_effect"
    );
}

#[test]
fn transport_error_kind_is_preserved() {
    let error = TransportError::new(TransportErrorKind::Timeout, "deadline exceeded");
    assert_eq!(error.kind(), TransportErrorKind::Timeout);
    assert_eq!(error.message(), "deadline exceeded");
}
