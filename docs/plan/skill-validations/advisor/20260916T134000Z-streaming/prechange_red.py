"""Independent black-box Red baseline for the advisor streaming change."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time


RESPONSE = """VERDICT: PROCEED

ASK RESTATED:
Check the synthetic candidate.

DO THIS:
1. Keep the tested behavior.

DO NOT:
- Expand the test scope.

CLAIM AUDIT:
- synthetic claim -> CONFIRMED (fixture.txt:1 -> \"ok\")

RISKS:
- none

COULD NOT VERIFY:
- live provider behavior

FLIP CONDITIONS:
- a changed contract
"""

BRIEFING_LABELS = (
    "REQUEST TYPE and ONE-LINE ASK", "REPO ROOT", "TASK AS GIVEN", "SCOPE",
    "BINDING CONSTRAINTS", "FACTS", "INFERENCES", "STATE", "ATTEMPTS",
    "CURRENT PLAN", "OPTIONS CONSIDERED", "ASSUMPTIONS", "OPEN QUESTIONS",
    "WHAT WOULD CHANGE MY MIND", "EXCERPTS",
)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, value):
    Path(path).write_text(
        json.dumps(value, ensure_ascii=True, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def make_fixture(root):
    root.mkdir(parents=True)
    repo = root / "repo"
    repo.mkdir()
    (repo / "fixture.txt").write_text("ok\n", encoding="utf-8", newline="\n")
    contract = root / "contract.md"
    contract.write_text("Synthetic response contract.\n", encoding="utf-8", newline="\n")
    briefing = root / "briefing.md"
    briefing.write_text(
        "\n\n".join("## " + label + "\nSynthetic fixture value." for label in BRIEFING_LABELS) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    fake_py = root / "fake_claude.py"
    fake_py.write_text(
        """import json, os, sys
response = """ + repr(RESPONSE) + """
if '--version' in sys.argv:
    print('synthetic-claude 1.0')
elif '--help' in sys.argv:
    print(' '.join([
        '--print','--model','--effort','--restricted','--safe-mode',
        '--strict-mcp-config','--tools','--allowedTools','--permission-mode',
        '--permission-prompts','--add-dir','--append-system-prompt-file',
        '--no-session-persistence','--max-budget-usd','--output-format'
    ]))
elif os.environ.get('ADVISOR_FAKE_MODE') == 'stream':
    print(json.dumps({'type':'system','subtype':'init','session_id':'synthetic'}), flush=True)
    print(json.dumps({'type':'result','subtype':'success','is_error':False,
                      'result':response,'total_cost_usd':0.25}), flush=True)
else:
    print(json.dumps({'type':'result','subtype':'success','is_error':False,
                      'result':response,'total_cost_usd':0.25}), flush=True)
""",
        encoding="utf-8",
        newline="\n",
    )
    fake_cmd = root / "claude.cmd"
    python_exe = str(Path(sys.executable).resolve())
    fake_cmd.write_text(
        '@echo off\r\n"' + python_exe + '" -B -X utf8 "%~dp0fake_claude.py" %*\r\n',
        encoding="ascii",
        newline="",
    )
    request = {
        "schema": "advisor-request-v1",
        "ask": "Check a synthetic candidate.",
        "type": "approach",
        "model": "opus",
        "effort": "high",
        "auth_mode": "subscription",
        "repo_root": str(repo.resolve()),
        "claude_path": str(fake_cmd.resolve()),
        "contract_path": str(contract.resolve()),
        "contract_sha256": sha256(contract.read_bytes()),
        "total_budget_usd": "2.00",
        "timeout_seconds": 10,
    }
    request_path = root / "request.json"
    write_json(request_path, request)
    return request_path, briefing


def run_case(case_id, advisor, trial_root, mode, show_progress):
    case_root = trial_root / case_id.lower()
    request, briefing = make_fixture(case_root / "fixture")
    run_dir = case_root / "run"
    command = [
        sys.executable, "-B", "-X", "utf8", str(advisor), "run",
        "--request", str(request), "--run-dir", str(run_dir),
        "--briefing", str(briefing),
    ]
    if show_progress:
        command.append("--show-progress")
    environment = dict(os.environ)
    environment["ADVISOR_FAKE_MODE"] = mode
    started = time.monotonic()
    process = subprocess.run(
        command,
        cwd=Path.cwd(),
        env=environment,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=20,
        shell=False,
    )
    duration = time.monotonic() - started
    (case_root / "command.stdout").write_bytes(process.stdout)
    (case_root / "command.stderr").write_bytes(process.stderr)
    try:
        final = json.loads(process.stdout.decode("utf-8-sig"))
    except (UnicodeError, json.JSONDecodeError):
        final = None
    actual = {
        "exit_code": process.returncode,
        "response_status": final.get("response_status") if isinstance(final, dict) else None,
        "verdict": final.get("verdict") if isinstance(final, dict) else None,
    }
    expected = {"exit_code": 0, "response_status": "VALID", "verdict": "PROCEED"}
    result = {
        "id": case_id,
        "command": command,
        "cwd": str(Path.cwd()),
        "mode": mode,
        "show_progress": show_progress,
        "duration_seconds": duration,
        "expected": expected,
        "actual": actual,
        "matched": actual == expected,
        "stdout_sha256": sha256(process.stdout),
        "stderr_sha256": sha256(process.stderr),
    }
    write_json(case_root / "result.json", result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--trial-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    candidate = args.candidate.resolve(strict=True)
    advisor = candidate / "scripts" / "advisor_run.py"
    if not advisor.is_file():
        raise SystemExit("candidate advisor_run.py missing")
    trial_root = args.trial_root.resolve()
    if trial_root.exists():
        raise SystemExit("trial root must be fresh")
    trial_root.mkdir(parents=True)
    results = [
        run_case("RED-CONTROL-JSON", advisor, trial_root, "json", False),
        run_case("RED-CLI-SHOW-PROGRESS", advisor, trial_root, "json", True),
        run_case("RED-STREAM-RESULT", advisor, trial_root, "stream", False),
    ]
    report = {
        "schema_version": "advisor-streaming-red-result-v1",
        "candidate": str(candidate),
        "cases": results,
        "matched": sum(item["matched"] for item in results),
        "total": len(results),
        "red_established": results[0]["matched"] and not results[1]["matched"] and not results[2]["matched"],
    }
    write_json(args.output, report)
    print(json.dumps(report, ensure_ascii=True, allow_nan=False))
    return 1 if report["red_established"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
