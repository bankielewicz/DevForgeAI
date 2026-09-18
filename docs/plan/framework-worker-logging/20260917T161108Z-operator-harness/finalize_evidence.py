"""Bind the actual delivery and evidence; does not grant acceptance or launch."""
import ast
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
WORKSPACE = Path(r"C:\Projects\DevForgeAI")
TRIAL = WORKSPACE / "docs/plan/framework-worker-trials/20260917T122229Z-logging-diagnostic"
PACKAGE = TRIAL / "operator-harness-001"
QA = WORKSPACE / "docs/plan/framework-worker-logging/20260917T105456Z-qa-retest"
sys.path.insert(0, str(PACKAGE))
from recorder import binding, write_new


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


runtime = [PACKAGE / "diagnostic.py", PACKAGE / "recorder.py", WORKSPACE / "Invoke-CodexWorkerDiagnostic.ps1"]
config = read(PACKAGE / "configuration.json")
identities = {
    "runtime_source": [binding(path) for path in runtime],
    "runtime_manifest": binding(PACKAGE / "runtime-manifest.json"),
    "active_configuration": binding(PACKAGE / "configuration.json"),
    "proposed_configuration": binding(ROOT / "current-source-review/configuration.proposed.json"),
    "proposed_input_manifest": binding(ROOT / "current-source-review/prepared-proposal/inputs/input-manifest.json"),
    "corrected_rust_candidate_manifest": binding(QA / "candidate-manifest.json"),
    "corrected_rust_source_files": len(read(QA / "candidate-manifest.json")),
    "qa_handoff": binding(QA / "handoff-manifest.json"),
    "bound_specifications": binding(QA / "specification-bindings.json"),
    "origin_specification": binding(WORKSPACE / "docs/plan/devforgeai-index-query-cli-spec.md"),
    "qa_built_probe": binding(config["probe"]["path"]),
    "native_worker": binding(config["worker"]["path"]),
    "native_codex": "NOT_RUN", "framework_acceptance": "NOT_EVALUATED",
}
assert identities["qa_built_probe"] == config["probe"]
assert identities["native_worker"] == config["worker"]
write_new(ROOT / "source-identities.json", identities)
python_result = read(ROOT / "attempts/15-python-final/test-results.json")
ps_result = read(ROOT / "attempts/16-powershell-final/test-results.json")
coverage = read(ROOT / "attempts/15-python-final/coverage.json")["totals"]
xml = ET.parse(ROOT / "attempts/16-powershell-final/coverage.xml")
ps_line = next(row for row in xml.getroot().findall("counter") if row.attrib["type"] == "LINE")
ps_covered = int(ps_line.attrib["covered"])
ps_total = ps_covered + int(ps_line.attrib["missed"])
passed = python_result["passing"] + ps_result["Passed"]
lines = coverage["covered_lines"] + ps_covered
denominator = coverage["num_statements"] + ps_total
write_new(ROOT / "quality-summary.json", {
    "development_status": "PARTIAL", "required_platform": "native Windows",
    "python": {"passed": python_result["passing"], "required": python_result["required"],
               "covered_lines": coverage["covered_lines"], "executable_lines": coverage["num_statements"],
               "line_percent": 100 * coverage["covered_lines"] / coverage["num_statements"],
               "covered_branches": coverage["covered_branches"], "branches": coverage["num_branches"]},
    "powershell": {"passed": ps_result["Passed"], "required": ps_result["Total"],
                   "covered_lines": ps_covered, "executable_lines": ps_total, "line_percent": 100 * ps_covered / ps_total},
    "overall": {"passing_required_cases": passed, "required_cases": passed + 2, "blocked_required_cases": 2,
                "pass_rate": 100 * passed / (passed + 2), "covered_lines": lines,
                "executable_lines": denominator, "line_percent": 100 * lines / denominator,
                "mandatory_readiness_complete": False},
    "runtime_denominator": [str(path) for path in runtime], "uncovered_runtime_exclusions": [],
    "excluded_test_infrastructure": "Tests, fixtures, evidence-only runners; historical supervisor is not imported by operator runtime",
    "native_codex": "NOT_RUN", "framework_acceptance": "NOT_EVALUATED",
})

# Snapshot final test and runtime identities without replacing earlier attempts.
for label in ("15-python-final", "16-powershell-final"):
    destination = ROOT / "attempts" / label / "final-bindings.json"
    write_new(destination, {"runtime": [binding(path) for path in runtime],
                           "tests": [binding(path) for path in sorted((ROOT / "tests").iterdir()) if path.is_file()]})

files = set()
for directory in (ROOT, PACKAGE):
    files.update(path for path in directory.rglob("*") if path.is_file())
files.add(WORKSPACE / "Invoke-CodexWorkerDiagnostic.ps1")
files.add(TRIAL / "launch-invocation.json")
# Test fixtures are retained outside the new package by the unchanged inherited
# suite. Include the fresh directories by the declared implementation start.
cutoff = datetime(2026, 9, 17, 16, 11, 8, tzinfo=timezone.utc).timestamp()
fixture_dirs = [path for path in (TRIAL / "recorder-fixtures").iterdir()
                if path.is_dir() and path.stat().st_ctime >= cutoff]
for directory in fixture_dirs:
    files.update(path for path in directory.rglob("*") if path.is_file())
write_new(ROOT / "changed-file-manifest.json", {
    "schema_version": 1,
    "scope": "New runtime/support/evidence files and fresh inherited-test fixture directories; no pre-existing product file edits",
    "root_entrypoint": binding(WORKSPACE / "Invoke-CodexWorkerDiagnostic.ps1"),
    "fresh_inherited_fixture_directories": [str(path) for path in sorted(fixture_dirs)],
    "files": [binding(path) for path in sorted(files)],
    "exclusions": "This manifest cannot bind itself or later verification/seal files; those are in the handoff",
})

links = []
for name in ("operator-handoff.md", "traceability-final.md"):
    path = ROOT / name
    text = path.read_text(encoding="utf-8")
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
        if not target.startswith(("http:", "https:")):
            destination = (path.parent / target.split("#")[0]).resolve()
            assert destination.exists(), str(destination)
            links.append({"source": str(path), "target": str(destination), "exists": True})
destinations = [WORKSPACE / "Invoke-CodexWorkerDiagnostic.ps1", PACKAGE / "diagnostic.py",
                PACKAGE / "recorder.py", ROOT / "operator-handoff.md",
                ROOT / "source-identities.json", ROOT / "changed-file-manifest.json",
                ROOT / "current-source-review/prepared-proposal/inputs/request.json"]
write_new(ROOT / "delivery-verification.json", {
    "utc": datetime.now(timezone.utc).isoformat(), "local_links_checked": len(links), "links": links,
    "required_destination_readbacks": [{"required": str(path), "actual": binding(path)} for path in destinations],
    "original_selected_document": binding(WORKSPACE / "docs/plan/framework-worker-diagnostic-outstanding-work.md"),
    "preservation_receipt": binding(ROOT / "preservation-final.json"),
    "native_attempt_exists": (TRIAL / "native-001").exists(), "native_run_exists": (TRIAL / "run").exists(),
    "new_reservation_exists": (PACKAGE / "launch-invocation-after-preparation-stop.json").exists(),
    "source_review": "PENDING_BRYAN", "framework_acceptance": "NOT_EVALUATED",
})
handoff_paths = [ROOT / name for name in (
    "operator-handoff.md", "source-identities.json", "quality-summary.json", "traceability-final.md",
    "checkpoint-003.md", "changed-file-manifest.json", "delivery-verification.json", "preservation-final.json",
    "config-drift.json", "current-source-review/operator-selection.proposed.md",
    "current-source-review/configuration.proposed.json", "current-source-review/proposal-result.json",
    "current-source-review/comparison.json", "current-source-review/permission-rule-addition.json",
    "attempts/15-python-final/test-results.json", "attempts/15-python-final/coverage.json",
    "attempts/16-powershell-final/test-results.json", "attempts/16-powershell-final/coverage.xml",
    "attempts/17-readiness-review-blocked/interpretation.json")]
handoff_paths += runtime + [PACKAGE / "configuration.json", PACKAGE / "runtime-manifest.json"]
write_new(ROOT / "handoff-manifest.json", {"schema_version": 1,
    "status": "PREPARATION_REVIEW_REQUIRED", "native_codex": "NOT_RUN", "framework_acceptance": "NOT_EVALUATED",
    "entries": {str(index): binding(path) for index, path in enumerate(handoff_paths)}})
seal = ROOT / "handoff-manifest.json"
for expected in read(seal)["entries"].values():
    assert binding(expected["path"]) == expected
write_new(ROOT / "handoff-verification.json", {"handoff": binding(seal), "entries_verified": len(handoff_paths)})
print(json.dumps({"handoff": binding(seal), "quality": read(ROOT / "quality-summary.json")["overall"],
                  "links_verified": len(links), "changed_manifest_entries": len(files)}, indent=2))
