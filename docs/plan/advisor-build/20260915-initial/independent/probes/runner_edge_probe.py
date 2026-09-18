import hashlib
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[4]
SCRIPT = WORKSPACE / "src" / "agents" / "skills" / "advisor" / "scripts" / "advisor_run.py"
SPEC = importlib.util.spec_from_file_location("advisor_run_edge", SCRIPT)
advisor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(advisor)

CONTRACT = Path("C:/Users/bryan/.codex/advisor/contract.md")
BASE = {
    "schema": "advisor-request-v1",
    "ask": "Check the candidate.",
    "repo_root": str(ROOT / "synthetic-repo"),
    "claude_path": "C:/Users/bryan/.local/bin/claude.exe",
    "contract_path": str(CONTRACT),
    "contract_sha256": hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
}


def valid_response():
    return """VERDICT: PROCEED

ASK RESTATED:
Check the candidate.

DO THIS:
1. Continue.

DO NOT:
- Expand scope.

CLAIM AUDIT:
- candidate -> CONFIRMED (src/limit_cli.py:6)

RISKS:
none

COULD NOT VERIFY:
none

FLIP CONDITIONS:
- Candidate bytes change.
"""


def main():
    observed = []

    try:
        advisor.validate_request(dict(BASE, total_budget_usd="9" * 1000))
        observed.append({"case": "oversized-budget", "status": "ACCEPTED"})
    except Exception as error:
        observed.append({
            "case": "oversized-budget",
            "status": "REJECTED",
            "exception": type(error).__name__,
            "structured_value_error": isinstance(error, ValueError),
        })

    invalid_dir = ROOT / "edge-inputs"
    invalid_dir.mkdir(exist_ok=True)
    bad_request = invalid_dir / "request-invalid-utf8.json"
    bad_request.write_bytes(b"\xff")
    process = advisor.execute_process(
        [
            sys.executable,
            str(SCRIPT),
            "run",
            "--request",
            str(bad_request),
            "--briefing",
            str(ROOT / "intake" / "briefing.md"),
            "--run-dir",
            str(invalid_dir / "never-started"),
        ],
        WORKSPACE,
        10,
    )
    stderr_lines = process["stderr"].decode("utf-8", errors="replace").splitlines()
    observed.append({
        "case": "invalid-utf8-request-cli",
        "exit_code": process["exit_code"],
        "stdout": process["stdout"].decode("utf-8", errors="replace"),
        "stderr_has_traceback": b"Traceback" in process["stderr"],
        "stderr_tail": stderr_lines[-1] if stderr_lines else "",
    })

    missing_none = valid_response().replace(
        "VERDICT: PROCEED",
        "VERDICT: INSUFFICIENT_CONTEXT",
    ) + "\nMISSING:\n- none\n"
    try:
        parsed = advisor.parse_response(missing_none)
        observed.append({
            "case": "missing-list-none",
            "status": "ACCEPTED",
            "verdict": parsed["verdict"],
        })
    except ValueError as error:
        observed.append({"case": "missing-list-none", "status": "REJECTED", "error": str(error)})

    interstitial = valid_response().replace(
        "VERDICT: PROCEED\n\nASK RESTATED:",
        "VERDICT: PROCEED\n\nUNLABELED TEXT\n\nASK RESTATED:",
    )
    try:
        parsed = advisor.parse_response(interstitial)
        observed.append({
            "case": "unlabeled-interstitial-text",
            "status": "ACCEPTED",
            "verdict": parsed["verdict"],
        })
    except ValueError as error:
        observed.append({"case": "unlabeled-interstitial-text", "status": "REJECTED", "error": str(error)})

    print(json.dumps(observed, indent=2))


if __name__ == "__main__":
    main()
