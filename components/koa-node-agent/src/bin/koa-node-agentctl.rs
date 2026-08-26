//! Non-privileged inspection client for the Node Agent catalog.
//!
//! It performs no host mutation and exposes no generic command passthrough.

#[path = "../broker/mod.rs"]
mod broker;

use std::env;
use std::process::ExitCode;
use std::str::FromStr;

fn main() -> ExitCode {
    let mut arguments = env::args().skip(1);
    match arguments.next().as_deref() {
        Some("list-operations") if arguments.next().is_none() => {
            for spec in broker::operations() {
                println!("{}", spec.id);
            }
            ExitCode::SUCCESS
        },
        Some("describe") => {
            let operation = arguments.next();
            if operation.is_none() || arguments.next().is_some() {
                eprintln!("usage: koa-node-agentctl describe OPERATION");
                return ExitCode::from(64);
            }
            describe(operation.expect("checked above"))
        },
        Some("self-check") if arguments.next().is_none() => match broker::self_check() {
            Ok(()) => {
                println!("catalog and sandbox invariants are valid");
                ExitCode::SUCCESS
            },
            Err(error) => {
                eprintln!("self-check failed: {error}");
                ExitCode::from(70)
            },
        },
        _ => {
            eprintln!("usage: koa-node-agentctl <list-operations|describe OPERATION|self-check>");
            ExitCode::from(64)
        },
    }
}

fn describe(value: String) -> ExitCode {
    let operation = match broker::OperationId::from_str(&value) {
        Ok(operation) => operation,
        Err(error) => {
            eprintln!("{error}");
            return ExitCode::from(65);
        },
    };
    let spec = broker::operation_spec(operation);
    println!(
        "{{\"operation\":\"{}\",\"purpose\":\"{}\",\"authorization_class\":\"{}\",\"mutates_host\":{},\"idempotency\":\"{}\",\"receipt\":\"{}\"}}",
        spec.id,
        escape_json(spec.purpose),
        spec.authorization_class,
        spec.mutates_host,
        spec.idempotency.as_str(),
        spec.receipt.as_str(),
    );
    ExitCode::SUCCESS
}

fn escape_json(value: &str) -> String {
    value
        .replace('\\', "\\\\")
        .replace('"', "\\\"")
        .replace('\n', "\\n")
        .replace('\r', "\\r")
}
