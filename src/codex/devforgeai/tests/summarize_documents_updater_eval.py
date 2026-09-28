"""Summarize a completed, fully graded Documents Updater native matrix."""
import argparse
import json
import statistics
from pathlib import Path
from make_documents_updater_evals import CASES

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence",type=Path)
    args=parser.parse_args()
    e=args.evidence
    plan=json.loads((e/"matrix-plan.json").read_text())
    grades=json.loads((e/"matrix-grades.json").read_text())
    expected={(t["case"],t["arm"],t["repeat"]) for t in plan["trials"]}
    actual={(t["case"],t["arm"],t["repeat"]) for t in grades}
    if expected!=actual or len(grades)!=48:
        raise SystemExit(f"Incomplete matrix: {len(grades)}/48; missing={sorted(expected-actual)}")
    if any(t["score"] is None for t in grades):
        raise SystemExit("Semantic grades remain REVIEW_REQUIRED")
    cases=[]
    for case,info in CASES.items():
        arms={arm:[t for t in grades if t["case"]==case and t["arm"]==arm] for arm in ("plugin","baseline")}
        row={"case":case,"verification":"VER-"+info["ver"]}
        for arm,trials in arms.items():
            row[arm]={"scores":[t["score"] for t in sorted(trials,key=lambda t:t["repeat"])],
                      "mean":statistics.mean(t["score"] for t in trials),
                      "strict_passes":sum(t["strict_pass"] for t in trials)}
        row["status"]="PASS" if all(t["strict_pass"] for t in arms["plugin"]) else "FAIL"
        cases.append(row)
    models=sorted({json.loads(p.read_text())["model"] for p in (e/"matrix").glob("*/result.json") if "model" in json.loads(p.read_text())})
    out={"candidate_sha256":plan["candidate_sha256"],"runtime":plan["codex_version"],"models":models,
         "total_trials":48,"cases":cases,
         "plugin_mean":statistics.mean(t["score"] for t in grades if t["arm"]=="plugin"),
         "baseline_mean":statistics.mean(t["score"] for t in grades if t["arm"]=="baseline"),
         "plugin_strict_passes":sum(t["strict_pass"] for t in grades if t["arm"]=="plugin"),
         "baseline_strict_passes":sum(t["strict_pass"] for t in grades if t["arm"]=="baseline"),
         "run_errors":[t for t in grades if t["status"] not in ("completed","awaiting_input")],
         "obligations":{row["verification"]:row["status"] for row in cases},
         "qualification":"Source evaluation; installation and owner manual acceptance not performed."}
    out["obligations"].update({"VER-09":"PASS (23 checker unit tests)","VER-10":"NOT_RUN","VER-11":"NOT_RUN","VER-12":"NOT_RUN"})
    out["mean_delta"]=out["plugin_mean"]-out["baseline_mean"]
    (e/"evaluation-summary.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({k:v for k,v in out.items() if k!="cases"},indent=2))
if __name__=="__main__":
    main()
