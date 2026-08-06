//! Dedicated privileged-broker binary.
//!
//! This entry point never exposes a generic shell or arbitrary command interface.
//! The authenticated Unix-socket transport and fixed host adapters are wired by the
//! preceding ports/adapters bundle; absent that wiring, `serve` fails closed.

#[path = "../broker/mod.rs"]
mod broker;

use std::collections::BTreeMap;
use std::env;
use std::process::ExitCode;
use std::time::{SystemTime, UNIX_EPOCH};

fn main() -> ExitCode {
    let mut arguments = env::args().skip(1);
    match arguments.next().as_deref() {
        Some("self-check") if arguments.next().is_none() => match broker::self_check() {
            Ok(()) => {
                println!("{{\"status\":\"ok\",\"broker\":\"koa_privileged_broker\"}}");
                ExitCode::SUCCESS
            }
            Err(error) => {
                eprintln!("broker self-check failed: {error}");
                ExitCode::from(70)
            }
        },
        Some("catalog") if arguments.next().is_none() => {
            for spec in broker::operations() {
                println!(
                    "{}\t{}\t{}\t{}",
                    spec.id,
                    spec.authorization_class,
                    spec.idempotency.as_str(),
                    spec.receipt.as_str()
                );
            }
            ExitCode::SUCCESS
        }
        Some("validate") => validate_cli_request(arguments.collect()),
        Some("serve") if arguments.next().is_none() => {
            eprintln!(
                "refusing to start: peer-authenticated local transport, durable ledger, and fixed adapters are not configured"
            );
            ExitCode::from(78)
        }
        _ => {
            eprintln!(
                "usage: koa-privileged-broker <self-check|catalog|validate OPERATION REQUEST_ID CALLER PROFILE_REF [TARGET_REF]|serve>"
            );
            ExitCode::from(64)
        }
    }
}

fn validate_cli_request(arguments: Vec<String>) -> ExitCode {
    if !(4..=5).contains(&arguments.len()) {
        eprintln!(
            "validate requires OPERATION REQUEST_ID CALLER PROFILE_REF and an optional managed TARGET_REF"
        );
        return ExitCode::from(64);
    }

    let operation = arguments[0].clone();
    let mut parameters = BTreeMap::new();
    match operation.as_str() {
        "manage_knowledge_artifact" => {
            parameters.insert("action".to_owned(), "quarantine".to_owned());
        }
        "import_offline_bundle" => {
            parameters.insert("target_state".to_owned(), "quarantine".to_owned());
        }
        "manage_declared_encrypted_volume" => {
            parameters.insert("action".to_owned(), "mount".to_owned());
        }
        "restart_allowlisted_service_group" => {
            parameters.insert("critical".to_owned(), "true".to_owned());
        }
        _ => {}
    }
    let now = now_millis();
    let request = broker::BrokerRequest {
        operation: operation.clone(),
        request_id: arguments[1].clone(),
        caller_identity: arguments[2].clone(),
        profile_context_ref: arguments[3].clone(),
        policy_decision_ref_when_required: if operation == "inspect_node_state" {
            None
        } else {
            Some("decision:cli-validation".to_owned())
        },
        artifact_or_target_refs: arguments.get(4).cloned().into_iter().collect(),
        expected_current_state: "state:explicit-cli-validation".to_owned(),
        parameters,
        deadline_unix_millis: now.saturating_add(30_000),
        correlation_id: format!("correlation-{}", arguments[1]),
    };

    match broker::PrivilegedBroker::default().validate(request, now) {
        Ok(validated) => {
            println!(
                "{{\"status\":\"accepted_for_validation_only\",\"operation\":\"{}\",\"fingerprint\":\"{}\"}}",
                validated.operation, validated.canonical_fingerprint
            );
            ExitCode::SUCCESS
        }
        Err(error) => {
            eprintln!("{}", error);
            ExitCode::from(65)
        }
    }
}

fn now_millis() -> u64 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map(|duration| duration.as_millis().min(u128::from(u64::MAX)) as u64)
        .unwrap_or(0)
}
