"""Positive reviewed handoff and READY-without-review negative observations."""
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
evidence = Path(__file__).resolve().parent
package = evidence.parents[2] / "src/agents/skills/skill-builder"
sys.path.insert(0, str(package / "tests"))
from adoption_fixture import build_adoption
from fixture_data import file_ref, sha, write, write_json

batch = evidence / ("handoff-profile-checks-release" if "--release" in sys.argv else "handoff-profile-checks")
batch.mkdir(exist_ok=False)
for reviewed in (True, False):
    run = batch / ("reviewed-positive" if reviewed else "ready-unreviewed-negative")
    root = run / "candidate"
    record = build_adoption(root)
    packet = {"schema_version": "1", "target_root": record["target_root"],
              "target_manifest_sha256": record["snapshot_manifest"]["sha256"],
              "managed_manifest_sha256": record["managed_manifest"]["sha256"], "origin_spec_sha256": record["origin_spec"]["sha256"],
              "review_policy": "review-before-repair", "review_state": "reviewed" if reviewed else "unreviewed", "builder_readiness": "READY",
              "selected_references": [record["origin_spec"], *record["quality_evidence"]]}
    write_json(root / "adoption/evidence/handoff.json", packet)
    record["handoff"] = file_ref(root, root / "adoption/evidence/handoff.json")
    write_json(root / "adoption/evidence/adoption-record.json", record)
    case = {"case_id": run.name, "grader_id": "adoption_consistency", "params": {"evidence": "adoption/evidence", "destination": "adoption/destination"},
            "expected": "PASS" if reviewed else "FAIL"}
    write(run / "cases.jsonl", json.dumps(case) + "\n")
    command = [sys.executable, "-B", "-X", "utf8", str(package / "scripts/run_evaluation.py"), "--package-root", str(package),
               "--candidate-root", str(root), "--cases", str(run / "cases.jsonl"), "--output", str(run / "evaluation.jsonl"),
               "--run-id", run.name, "--profile", "adoption-v1"]
    proc = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", timeout=30)
    write_json(run / "command.json", {"command": command, "exit_code": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr})
    result = json.loads((run / "evaluation.jsonl").read_text())
    assert proc.returncode == 0 and result["expectation_met"]
    for p, d in result["candidate_digests"].items():
        assert sha((root / p).read_bytes()) == d
    assert sha((run / "cases.jsonl").read_bytes()) == result["cases_sha256"]
    print(json.dumps({"run": run.name, "status": result["status"], "observations": result["observations"], "exit_code": proc.returncode, "readback": "PASS"}))
