import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "synthetic-repo" / "src" / "limit_cli.py"


def run(value):
    environment = dict(os.environ)
    if value is None:
        environment.pop("LIMIT", None)
    else:
        environment["LIMIT"] = value
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True,
        text=True,
        env=environment,
        check=False,
    )
    return {
        "value": value,
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def main():
    observed = [run(value) for value in ("7", " 7", "007", None)]
    expected = [
        {"value": "7", "exit_code": 0, "stdout": "limit=7\n", "stderr": ""},
        {"value": " 7", "exit_code": 2, "stdout": "", "stderr": "error: invalid limit\n"},
        {"value": "007", "exit_code": 2, "stdout": "", "stderr": "error: invalid limit\n"},
        {"value": None, "exit_code": 2, "stdout": "", "stderr": "error: invalid limit\n"},
    ]
    for actual, wanted in zip(observed, expected):
        status = "PASS" if actual == wanted else "FAIL"
        print({"status": status, "actual": actual, "expected": wanted})
    failures = sum(actual != wanted for actual, wanted in zip(observed, expected))
    print({"required": len(expected), "passed": len(expected) - failures, "failed": failures})
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
