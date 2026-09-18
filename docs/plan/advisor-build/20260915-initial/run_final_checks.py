"""Retain exact final authoring commands and outputs in a fresh directory."""
import json
from pathlib import Path
import platform
import subprocess
import sys

root = Path(__file__).resolve().parents[4]
evidence = Path(__file__).parent / "final-checks"
evidence.mkdir(exist_ok=False)
python = [sys.executable, "-B", "-X", "utf8"]
package = root / "src/agents/skills/advisor"
commands = [
    ("tests", python + ["-m", "coverage", "run", "--branch", "--source=" + str(package / "scripts") + "," + str(package / "evals"), "--data-file=" + str(evidence / "coverage.data"), "-m", "unittest", "discover", "-s", str(package / "tests"), "-v"]),
    ("coverage-json", python + ["-m", "coverage", "json", "--data-file=" + str(evidence / "coverage.data"), "-o", str(evidence / "coverage.json")]),
    ("coverage-report", python + ["-m", "coverage", "report", "--data-file=" + str(evidence / "coverage.data"), "-m"]),
    ("jsonl", python + [str(package / "evals/run_evaluation.py"), "--output", str(evidence / "evaluation")]),
    ("skill-metadata", python + ["C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py", str(package)]),
]
records = []
for name, command in commands:
    process = subprocess.run(command, cwd=root, capture_output=True, timeout=60, shell=False)
    (evidence / (name + ".stdout.txt")).write_bytes(process.stdout)
    (evidence / (name + ".stderr.txt")).write_bytes(process.stderr)
    records.append({"name": name, "command": command, "cwd": str(root), "exit_code": process.returncode})
    print(name, process.returncode)
report = {"os": platform.platform(), "python": sys.version, "executable": sys.executable, "launcher_shell": "PowerShell", "filesystem": "Windows C: native", "checks": records}
(evidence / "commands.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
totals = json.loads((evidence / "coverage.json").read_text())["totals"]
line_rate = 100 * totals["covered_lines"] / totals["num_statements"]
branch_rate = 100 * totals["covered_branches"] / totals["num_branches"]
print(json.dumps({"line_rate": line_rate, "branch_rate": branch_rate, "totals": totals}))
sys.exit(0 if all(r["exit_code"] == 0 for r in records) and line_rate >= 95 else 1)
