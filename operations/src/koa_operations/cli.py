"""Command-line interface for explicit operational backup transitions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from .backup.plan import BackupPlanError, create_plan, load_plan, write_plan
from .backup.run import BackupExecutionError, run_backup
from .backup.verify import BackupVerificationError, verify_backup
from .config import ConfigurationError, load_mapping, write_json_atomic
from .evidence import EvidenceError, EvidenceJournal


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="koa-operations")
    parser.add_argument("--version", action="version", version="koa-operations 0.1.0")
    commands = parser.add_subparsers(dest="command", required=True)
    backup = commands.add_parser("backup", help="plan, run, or verify a backup")
    stages = backup.add_subparsers(dest="backup_command", required=True)

    plan = stages.add_parser("plan", help="validate and write an immutable backup plan")
    plan.add_argument("--config", required=True, type=Path)
    plan.add_argument("--output", required=True, type=Path)
    plan.add_argument("--evidence-dir", required=True, type=Path)

    run = stages.add_parser("run", help="execute a validated backup plan")
    run.add_argument("--plan", required=True, type=Path)
    run.add_argument("--output", required=True, type=Path)
    run.add_argument("--evidence-dir", required=True, type=Path)

    verify = stages.add_parser("verify", help="verify a completed backup")
    verify.add_argument("--plan", required=True, type=Path)
    verify.add_argument("--run-result", required=True, type=Path)
    verify.add_argument("--output", required=True, type=Path)
    verify.add_argument("--evidence-dir", required=True, type=Path)
    verify.add_argument("--canonical-schema", type=Path)
    return parser


def _emit_error(kind: str, message: str, *, details: object | None = None) -> None:
    payload: dict[str, object] = {"error": kind, "message": message}
    if details is not None:
        payload["details"] = details
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True), file=sys.stderr)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        journal = EvidenceJournal(args.evidence_dir)
        if args.command == "backup" and args.backup_command == "plan":
            config = load_mapping(args.config)
            plan = create_plan(config)
            write_plan(args.output, plan)
            record = journal.record(
                operation_id=str(plan.payload["operation_id"]),
                correlation_id=str(plan.payload["correlation_id"]),
                phase="backup_plan",
                outcome="succeeded",
                subject_ref=f"backup-set:{plan.payload['backup_set_id']}",
                details={"plan_digest": plan.digest, "plan_state": "planned"},
            )
            print(json.dumps({"plan": str(args.output), "plan_digest": plan.digest, "evidence": str(record.path)}, sort_keys=True))
            return 0
        if args.command == "backup" and args.backup_command == "run":
            plan = load_plan(args.plan)
            result = run_backup(plan, evidence_journal=journal)
            write_json_atomic(args.output, result)
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
            return 0
        if args.command == "backup" and args.backup_command == "verify":
            plan = load_plan(args.plan)
            run_result = load_mapping(args.run_result)
            report = verify_backup(
                plan,
                run_result,
                evidence_journal=journal,
                canonical_schema_path=args.canonical_schema,
            )
            write_json_atomic(args.output, report)
            print(json.dumps(report, ensure_ascii=False, sort_keys=True))
            return 0
        _emit_error("unsupported_command", "unsupported command")
        return 2
    except BackupExecutionError as exc:
        try:
            write_json_atomic(args.output, exc.result)
        except Exception:
            pass
        _emit_error("backup_execution_failed", str(exc), details=exc.result)
        return 4
    except BackupVerificationError as exc:
        try:
            write_json_atomic(args.output, exc.report)
        except Exception:
            pass
        _emit_error("backup_verification_failed", str(exc), details=exc.report)
        return 5 if exc.report.get("verification_state") == "blocked" else 4
    except (BackupPlanError, ConfigurationError, EvidenceError, OSError) as exc:
        _emit_error("invalid_operational_input", str(exc))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
