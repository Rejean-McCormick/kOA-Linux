//! Minimal Node Agent process entry point.
//!
//! Runtime transport and system adapters are supplied by the preceding ports/adapters
//! bundle. Until they are configured, this binary exposes only bounded introspection
//! and fails closed for service startup.

#[path = "../broker/mod.rs"]
mod broker;

use std::env;
use std::process::ExitCode;

fn main() -> ExitCode {
    let mut arguments = env::args().skip(1);
    match arguments.next().as_deref() {
        Some("self-check") if arguments.next().is_none() => match broker::self_check() {
            Ok(()) => {
                println!("{{\"status\":\"ok\",\"component\":\"koa_node_agent\"}}");
                ExitCode::SUCCESS
            }
            Err(error) => {
                eprintln!("broker self-check failed: {error}");
                ExitCode::from(70)
            }
        },
        Some("capabilities") if arguments.next().is_none() => {
            print_capabilities();
            ExitCode::SUCCESS
        }
        Some("health") if arguments.next().is_none() => {
            println!(
                "{{\"status\":\"not_ready\",\"component\":\"koa_node_agent\",\"reason\":\"runtime_transport_and_adapters_not_configured\"}}"
            );
            ExitCode::from(3)
        }
        Some("serve") if arguments.next().is_none() => {
            eprintln!(
                "refusing to start: authenticated local transport and fixed system adapters are not configured"
            );
            ExitCode::from(78)
        }
        _ => {
            eprintln!("usage: koa-node-agent <self-check|capabilities|health|serve>");
            ExitCode::from(64)
        }
    }
}

fn print_capabilities() {
    print!("{{\"component\":\"koa_node_agent\",\"operations\":[");
    for (index, spec) in broker::operations().iter().enumerate() {
        if index > 0 {
            print!(",");
        }
        print!(
            "{{\"operation\":\"{}\",\"authorization_class\":\"{}\",\"mutates_host\":{},\"receipt\":\"{}\"}}",
            spec.id,
            spec.authorization_class,
            spec.mutates_host,
            spec.receipt.as_str()
        );
    }
    println!("]}}");
}
