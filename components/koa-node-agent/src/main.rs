#![forbid(unsafe_code)]

use koa_node_agent::config::NodeAgentConfig;
use koa_node_agent::health::{evaluate_health, RuntimeEvidence};
use koa_node_agent::{bootstrap, describe_json};
use std::env;
use std::path::PathBuf;
use std::process::ExitCode;

fn main() -> ExitCode {
    match run(env::args().skip(1).collect()) {
        Ok(code) => code,
        Err(message) => {
            eprintln!("koa-node-agent: {message}");
            ExitCode::from(2)
        },
    }
}

fn run(arguments: Vec<String>) -> Result<ExitCode, String> {
    let mut config_path = None;
    let mut command = None;
    let mut operational_view = false;
    let mut index = 0;
    while index < arguments.len() {
        match arguments[index].as_str() {
            "--config" => {
                index += 1;
                let value = arguments
                    .get(index)
                    .ok_or_else(|| "--config requires an absolute path".to_owned())?;
                let path = PathBuf::from(value);
                if !path.is_absolute() {
                    return Err("--config requires an absolute path".to_owned());
                }
                config_path = Some(path);
            },
            "--operational" => operational_view = true,
            "--help" | "-h" => {
                print_help();
                return Ok(ExitCode::SUCCESS);
            },
            value if command.is_none() => command = Some(value.to_owned()),
            value => return Err(format!("unexpected argument: {value}")),
        }
        index += 1;
    }

    match command.as_deref().unwrap_or("health") {
        "describe" => {
            println!("{}", describe_json());
            Ok(ExitCode::SUCCESS)
        },
        "check-config" => {
            let config =
                NodeAgentConfig::load(config_path.as_deref()).map_err(|error| error.to_string())?;
            config.validate().map_err(|error| error.to_string())?;
            println!("{{\"component_id\":\"koa_node_agent\",\"configuration\":\"valid\"}}");
            Ok(ExitCode::SUCCESS)
        },
        "health" => {
            let runtime = bootstrap(config_path.as_deref(), RuntimeEvidence::default())
                .map_err(|error| error.to_string())?;
            println!("{}", runtime.status().to_json(operational_view));
            if runtime.status().health == "failed" {
                Ok(ExitCode::from(2))
            } else if runtime.status().health == "degraded" {
                Ok(ExitCode::from(1))
            } else {
                Ok(ExitCode::SUCCESS)
            }
        },
        "readiness" => {
            let config =
                NodeAgentConfig::load(config_path.as_deref()).map_err(|error| error.to_string())?;
            let status = evaluate_health(&config, &RuntimeEvidence::default());
            println!("{}", status.to_json(operational_view));
            if status.readiness == "ready" {
                Ok(ExitCode::SUCCESS)
            } else {
                Ok(ExitCode::from(3))
            }
        },
        other => Err(format!(
            "unknown command {other}; expected describe, check-config, health, or readiness"
        )),
    }
}

fn print_help() {
    println!(
        "kOA Node Agent foundation\n\nUSAGE:\n  koa-node-agent [--config ABSOLUTE_PATH] [--operational] <COMMAND>\n\nCOMMANDS:\n  describe      Print bounded component metadata\n  check-config  Validate configuration without mutating host state\n  health        Print bounded health status\n  readiness     Print readiness and return a non-zero status when blocked\n\nThis binary exposes no privileged operation execution in bundle B-0039."
    );
}
