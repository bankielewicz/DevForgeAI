#!/usr/bin/env python3
"""Independent compiled-CLI oracle for F-02 malformed error redaction."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
from datetime import datetime, timezone


MARKER = b"DEV_PRIVATE_SENTINEL_9201"
CASES = [*(f"WF-07-{number}" for number in range(90, 105)), *(f"WF-04-{number}" for number in range(90, 94))]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--probe", type=Path, required=True)
    parser.add_argument("--peer", type=Path, required=True)
    parser.add_argument("--task", type=Path, required=True)
    args = parser.parse_args()

    output_root = args.output_root.resolve(strict=False)
    output_root.mkdir(parents=False, exist_ok=False)
    probe = args.probe.resolve(strict=True)
    peer = args.peer.resolve(strict=True)
    task_bytes = args.task.resolve(strict=True).read_bytes()
    summary: list[dict[str, object]] = []
    failures: list[str] = []

    for case in CASES:
        case_root = output_root / case
        checkout = case_root / "fixture"
        run_dir = case_root / "run"
        checkout.mkdir(parents=True)
        (checkout / "task.json").write_bytes(task_bytes)
        (checkout / "peer-case.txt").write_text(case + "\n", encoding="ascii", newline="\n")
        request = {
            "schema_version": 1,
            "project_id": "qa-project",
            "checkout_id": "qa-checkout",
            "work_id": "qa-work",
            "run_id": "qa-run",
            "candidate_sha256": sha256(task_bytes),
            "checkout_root": str(checkout),
            "run_dir": str(run_dir),
            "worker_executable": str(peer),
            "worker_sha256": sha256(peer.read_bytes()),
            "adapter": "peer",
            "scenario": "complete",
            "profile": None,
        }
        request_path = case_root / "request-input.json"
        request_path.write_text(json.dumps(request, separators=(",", ":")), encoding="utf-8", newline="\n")
        argv = [str(probe), "run", "--request", str(request_path)]
        started = utc_now()
        before = time.monotonic_ns()
        process = subprocess.Popen(
            argv,
            cwd=checkout,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        timed_out = False
        try:
            exit_code = process.wait(timeout=15)
        except subprocess.TimeoutExpired:
            timed_out = True
            process.kill()
            exit_code = process.wait(timeout=5)
        elapsed_ns = time.monotonic_ns() - before
        ended = utc_now()
        if process.stdin is not None:
            process.stdin.close()
        stdout = process.stdout.read() if process.stdout is not None else b""
        stderr = process.stderr.read() if process.stderr is not None else b""
        (case_root / "stdout.bin").write_bytes(stdout)
        (case_root / "stderr.bin").write_bytes(stderr)
        journal_path = run_dir / "journal.jsonl"
        journal = journal_path.read_bytes() if journal_path.exists() else b""
        evidence = stdout + stderr + journal

        case_failures: list[str] = []
        if timed_out:
            case_failures.append("timeout")
        if exit_code != 4:
            case_failures.append(f"exit={exit_code}, expected=4")
        if MARKER in evidence:
            case_failures.append("private marker retained")
        if (checkout / "task.json").read_bytes() != task_bytes:
            case_failures.append("fixture changed")
        journal_lines = journal.splitlines()
        try:
            journal_events = [json.loads(line) for line in journal_lines]
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            journal_events = []
            case_failures.append(f"invalid journal: {error}")
        for event in journal_events:
            if set(event) != {"schema_version", "run_id", "seq", "observed_at", "elapsed_ms", "kind", "data"}:
                case_failures.append("journal event has unapproved top-level field")
                break
        if not journal_events:
            case_failures.append("empty journal")

        receipt = {
            "schema_version": 1,
            "case": case,
            "argv": argv,
            "cwd": str(checkout),
            "start_utc": started,
            "end_utc": ended,
            "duration_monotonic_ns": elapsed_ns,
            "native_exit_code": exit_code,
            "timed_out": timed_out,
            "stdout_bytes": len(stdout),
            "stdout_sha256": sha256(stdout),
            "stderr_bytes": len(stderr),
            "stderr_sha256": sha256(stderr),
            "journal_bytes": len(journal),
            "journal_sha256": sha256(journal),
            "private_marker_absent": MARKER not in evidence,
            "fixture_unchanged": (checkout / "task.json").read_bytes() == task_bytes,
            "journal_event_count": len(journal_events),
            "failures": case_failures,
        }
        (case_root / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8", newline="\n")
        summary.append(receipt)
        failures.extend(f"{case}: {failure}" for failure in case_failures)

    result = {
        "schema_version": 1,
        "oracle": "QA-owned exact exit, byte canary absence, closed journal envelope, immutable fixture",
        "probe": str(probe),
        "probe_sha256": sha256(probe.read_bytes()),
        "peer": str(peer),
        "peer_sha256": sha256(peer.read_bytes()),
        "required_cases": len(CASES),
        "passed_cases": len(CASES) - len({failure.split(":", 1)[0] for failure in failures}),
        "failures": failures,
        "cases": summary,
    }
    print(json.dumps(result, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
