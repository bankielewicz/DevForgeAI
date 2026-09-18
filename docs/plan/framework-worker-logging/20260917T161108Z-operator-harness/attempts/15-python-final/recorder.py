# Derived from the preserved supervisor.py (bace72fa...363990).
# Only wait handling changes: owned-handle polling remains deadline bounded.
"""Evidence recorder, not framework policy or a native launch authorization.

There is deliberately no command-line launch entry point. The separately
selected caller supplies reviewed argv, cwd and (if authorized) a child env copy.
Forced stop uses only the live Popen handle. Rust owns its worker Job Object.
"""
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import subprocess
import time


def write_new(path, value):
    with Path(path).open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2)
        stream.write("\n")


def binding(path):
    digest = hashlib.sha256()
    size = 0
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(65536), b""):
            size += len(block)
            digest.update(block)
    return {"path": str(path), "bytes": size, "sha256": digest.hexdigest()}


def error_identity(error):
    return {"type": type(error).__name__, "errno": error.errno,
            "winerror": getattr(error, "winerror", None)}


def remaining(deadline):
    return max(0, deadline - time.monotonic())


def wait_owned(child, timeout):
    """Poll the held handle; avoid Python 3.10's interrupt-time negative wait."""
    deadline = time.monotonic() + max(0, timeout)
    while child.poll() is None:
        left = remaining(deadline)
        if left <= 0:
            raise subprocess.TimeoutExpired(child.args, timeout)
        time.sleep(min(0.02, left))
    return child.returncode


def capture(argv, cwd, attempt, *, cancel_after=135, grace=5, reap=2, finalize=3,
            hold_stdin=True, environment=None):
    budgets = (cancel_after, grace, reap, finalize)
    if not all(type(value) in (int, float) and math.isfinite(value) and value > 0 for value in budgets):
        raise ValueError("Budgets must be finite positive numbers")
    attempt = Path(attempt)
    attempt.mkdir(exist_ok=False)  # Exclusive attempt ownership; no replay over evidence.
    started = time.monotonic()
    total_budget = sum(budgets)
    receipt = {"argv": list(argv), "cwd": str(cwd),
               "started_utc": datetime.now(timezone.utc).isoformat(),
               "budgets_seconds": dict(zip(("cancel_after", "grace", "reap", "finalize"), budgets)),
               "total_budget_seconds": total_budget, "stdin_held_open": hold_stdin,
               "environment_source": "inherited" if environment is None else "caller_copy",
               "environment_values_recorded": False, "shell": False,
               "timed_out": False, "interrupted": False, "cancellation_sent": False,
               "cancellation_error": None, "forced_termination": False,
               "termination_error": None, "reap_incomplete": False,
               "spawn_error": None, "owned_pid": None,
               "worker_tree_status": "REQUIRES_RUST_EVIDENCE",
               "framework_acceptance": "NOT_EVALUATED"}
    write_new(attempt / "started.json", receipt)
    child = None
    with (attempt / "stdout.bin").open("xb") as stdout, (attempt / "stderr.bin").open("xb") as stderr:
        try:
            child = subprocess.Popen(argv, cwd=cwd, env=environment, shell=False,
                                     stdin=subprocess.PIPE if hold_stdin else subprocess.DEVNULL,
                                     stdout=stdout, stderr=stderr, bufsize=0)
        except OSError as error:
            receipt["spawn_error"] = error_identity(error)
        if child is not None:
            receipt["owned_pid"] = child.pid
            try:
                try:
                    wait_owned(child, remaining(started + cancel_after))
                except (subprocess.TimeoutExpired, KeyboardInterrupt) as error:
                    receipt["timed_out"] = isinstance(error, subprocess.TimeoutExpired)
                    receipt["interrupted"] = isinstance(error, KeyboardInterrupt)
                    if hold_stdin:
                        try:
                            child.stdin.write(b'{"op":"cancel"}\n')
                            receipt["cancellation_sent"] = True
                        except OSError as error:
                            receipt["cancellation_error"] = error_identity(error)
                    grace_end = min(time.monotonic() + grace, started + cancel_after + grace)
                    try:
                        wait_owned(child, remaining(grace_end))
                    except subprocess.TimeoutExpired:
                        receipt["forced_termination"] = True
                        try:
                            child.kill()  # Windows TerminateProcess on the held handle.
                        except OSError as error:
                            receipt["termination_error"] = error_identity(error)
                        try:
                            wait_owned(child, remaining(min(time.monotonic() + reap,
                                                            started + cancel_after + grace + reap)))
                        except subprocess.TimeoutExpired:
                            receipt["reap_incomplete"] = True
            finally:
                if child.stdin is not None:
                    child.stdin.close()
    receipt.update({"process_exit_code": None if child is None else child.poll(),
                    "owned_probe_stopped": child is None or child.poll() is not None,
                    "stdout": binding(attempt / "stdout.bin"),
                    "stderr": binding(attempt / "stderr.bin"),
                    "recorder": binding(Path(__file__)),
                    "ended_utc": datetime.now(timezone.utc).isoformat()})
    receipt["elapsed_before_receipt_write_seconds"] = time.monotonic() - started
    receipt["budget_exceeded_before_receipt_write"] = receipt["elapsed_before_receipt_write_seconds"] > total_budget
    write_new(attempt / "receipt.json", receipt)
    # The caller also measures complete invocation time, including this final file write.
    return receipt

