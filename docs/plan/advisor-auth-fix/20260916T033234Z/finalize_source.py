"""Bind reviewed source bytes and summarize already executed checks; no authority."""
import ast
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[4]
EVIDENCE = Path(__file__).resolve().parent
SOURCE = ROOT / "src/agents/skills/advisor"
INSTALLED = ROOT / ".agents/skills/advisor"
CONTRACT = Path("C:/Users/bryan/.codex/advisor/contract.md")
REVIEWED_CONTRACT = "eec3af8fa530175c1da9f31fcf05cab59c591dd30456be13ee9deb2ba234934e"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def files(root):
    return {p.relative_to(root).as_posix(): p for p in root.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"}


assert sha(CONTRACT) == REVIEWED_CONTRACT, "External contract changed since review"
source_files = files(SOURCE)
installed_files = files(INSTALLED)
backup_files = files(EVIDENCE / "installed-before")
assert {k: sha(p) for k, p in installed_files.items()} == {k: sha(p) for k, p in backup_files.items()}, "Installed package changed before publication"
for name, path in source_files.items():
    if path.suffix == ".py":
        ast.parse(path.read_text(encoding="utf-8"), filename=name)
    elif path.suffix == ".json":
        json.loads(path.read_text(encoding="utf-8"))
    elif path.suffix == ".jsonl":
        for line in path.read_text(encoding="utf-8").splitlines():
            json.loads(line)
    elif path.suffix == ".md":
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if ":" not in target and not target.startswith("#"):
                assert (path.parent / target.split("#")[0]).is_file(), (name, target)

manifest_path = SOURCE / "artifact-manifest.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
manifest["files"] = {name: sha(path) for name, path in sorted(source_files.items()) if name != "artifact-manifest.json"}
manifest["external_contract"]["sha256"] = REVIEWED_CONTRACT
manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")
for name, expected in manifest["files"].items():
    assert sha(SOURCE / name) == expected

baseline = files(EVIDENCE / "source-before")
changed = [name for name, path in source_files.items() if name not in baseline or sha(path) != sha(baseline[name])]
coverage = json.loads((EVIDENCE / "coverage.json").read_text(encoding="utf-8"))
totals = coverage["totals"]
line_rate = 100 * totals["covered_lines"] / totals["num_statements"]
branch_rate = 100 * totals["covered_branches"] / totals["num_branches"]
assert set(k.replace("\\", "/") for k in coverage["files"]) == {
    "src/agents/skills/advisor/scripts/advisor_run.py", "src/agents/skills/advisor/evals/run_evaluation.py"}
assert totals["excluded_lines"] == 0 and line_rate >= 95
test_log = (EVIDENCE / "qa-tests.txt").read_text(encoding="utf-8-sig")
test_ids = re.findall(r"^(test_\S+ \([^)]+\)) \.\.\. ok$", test_log, re.M)
assert len(test_ids) == len(set(test_ids)) == 51
evaluation = json.loads((EVIDENCE / "evaluation-001/summary.json").read_text())
assert evaluation["required"] == evaluation["passed"] == 27
report = {"schema": "advisor-auth-repair-checks-v1", "source_root": str(SOURCE),
          "changed_files": sorted(changed), "unit_cases": 51, "unit_passed": 51,
          "jsonl_cases": 27, "jsonl_passed": 27, "required_cases": 78, "passed": 78,
          "pass_rate": 100, "covered_lines": totals["covered_lines"],
          "required_lines": totals["num_statements"], "line_coverage_percent": line_rate,
          "covered_branches": totals["covered_branches"], "required_branches": totals["num_branches"],
          "branch_coverage_percent": branch_rate, "excluded_lines": 0,
          "source_manifest_sha256": sha(manifest_path), "contract_sha256": REVIEWED_CONTRACT,
          "native_qualification": "NOT_RUN", "framework_acceptance": "NOT_EVALUATED",
          "note": "Red/green and repeated corpus executions do not add cases to this denominator."}
with (EVIDENCE / "source-checks.json").open("x", encoding="utf-8") as stream:
    json.dump(report, stream, indent=2)
print(json.dumps(report, indent=2))
