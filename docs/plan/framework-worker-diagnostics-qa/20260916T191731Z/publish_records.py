"""Publish completed QA record indexes; evidence bookkeeping, no framework authority."""
import json
from datetime import datetime, timezone
from pathlib import Path
from intake import RUN, MANIFEST, binding


def read(name):
    return json.loads((RUN / name).read_text())


def write(name, value):
    with (RUN / name).open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2)
        stream.write("\n")


def main():
    cases = read("case-results.json")
    coverage = read("coverage-analysis.json")
    assert len(cases) == 146 and all(r["status"] == "PASS" for r in cases)
    assert coverage["covered"] == 3334 and coverage["count"] == 3497 and coverage["floor_met"]
    assert read("process-readback.json")["matching_count"] == 0
    assert all(r["matches"] for r in read("candidate-readback-after.json"))
    assert all(r["matches"] for r in read("input-readback-after.json"))
    attempts = []
    for path in sorted((RUN / "attempts").glob("*/receipt.json")):
        row = json.loads(path.read_text())
        assert row["exit_code"] == (101 if row["attempt"] == "05-harness-inventory" else 0)
        assert not row["timeout"]
        attempts.append({"attempt": row["attempt"], "argv": row["argv"], "cwd": row["cwd"],
                         "start_utc": row["start_utc"], "end_utc": row["end_utc"],
                         "exit_code": row["exit_code"], "elapsed_seconds": row["elapsed_seconds"],
                         "receipt": binding(path), "stdout": row["stdout"], "stderr": row["stderr"]})
    assert len(attempts) == 13
    write("execution-ledger.json", attempts)
    issues = [
        {"id": "HG-01", "class": "PREREQUISITE_OR_HARNESS_GAP", "owner": "QA harness author",
         "status": "RESOLVED", "product_defect": False, "terminal_stop": False,
         "observation": "Attempt 05 E0425 on QA-only JOB_OBJECT_TERMINATE symbol; no test executed",
         "resolution": "Retain failed inputs; use installed SDK's 0x0008 constant in QA helper; successful fresh compilation 06 and initial behavior execution 07",
         "evidence": ["attempts/05-harness-inventory/receipt.json", "attempts/05-harness-inventory/assessment.md", "attempts/05-harness-inventory/input-snapshot", "attempts/06-harness-inventory/receipt.json", "attempts/07-independent-cases/receipt.json"]},
        {"id": "ME-01", "class": "MEASUREMENT_PREREQUISITE", "owner": "User-selected future scope, if needed",
         "status": "NOT_RUN", "product_defect": False, "terminal_stop": False,
         "observation": "Branch collector requires nightly; installed toolchains stable only",
         "impact": "Branch value unavailable, disclosed under addendum A5; no branch numeric floor or installation selected",
         "evidence": ["attempts/01-branch-capability/stderr.bin", "environment.json"]}
    ]
    write("findings.json", {"confirmed_product_defects": [], "unresolved_required_offline_cases": [], "records": issues})
    checkpoint_path = RUN / "checkpoint.json"
    with (RUN / "checkpoint-initial.json").open("xb") as stream:
        stream.write(checkpoint_path.read_bytes())
    checkpoint = {"intent": "run", "plan_readiness": "READY", "execution": "COMPLETED", "verdict": "PASS",
        "scope": "Independent offline Windows x64 QA of frozen diagnostic candidate",
        "recorded_utc": datetime.now(timezone.utc).isoformat(), "candidate": binding(MANIFEST),
        "plan": binding(RUN/"test-plan.md"), "input_bindings": binding(RUN/"input-bindings.json"),
        "cases": {"required":146,"passed":146,"units_required":46,"units_passed":46},
        "executed_lines": {"covered":3334,"total":3497,"percentage":coverage["percentage"]},
        "branch_coverage":"NOT_RUN", "branch_prerequisite":"Installed collector requires nightly, which is not installed",
        "query_failed_runtime":"PASS, four mapped-source real Windows query-error subfixtures",
        "completed_attempts":[r["attempt"] for r in attempts], "issue_ids":[r["id"] for r in issues],
        "whole_run_stop_trigger":None,"owned_processes":[],"remaining_required_offline_work":[],
        "retained_fixtures":"fixtures/ and six fresh trial roots in trial-ownership.json; no evidence deletion",
        "process_observation":binding(RUN/"process-readback.json"),
        "framework_acceptance":"NOT_EVALUATED","native_codex_permitted":False,"native_attempts":0,
        "next_owner":"User/operator separately selects bounded native diagnostic task",
        "next_safe_action":"Return report and native-diagnostic-handoff.md; do not launch native Codex in QA",
        "artifact_delivery":"Final literal-path readback recorded separately in publication-readback.json",
        "report_path":str(RUN/"qa-report.md"), "fix_packet":None,
        "external_manifest_path":str(RUN/"artifact-index.json")}
    checkpoint_path.write_text(json.dumps(checkpoint,indent=2)+"\n",encoding="utf-8",newline="\n")
    print(json.dumps({"ledger_attempts":len(attempts),"issues":len(issues),"checkpoint":binding(checkpoint_path)},indent=2))


if __name__ == "__main__":
    main()
