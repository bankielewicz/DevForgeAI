"""Summarize a completed and independently graded Architecture native matrix."""
from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path

from native_architecture_eval import CASE_VER


def build_summary(evidence):
    plan = json.loads((evidence / "matrix-plan.json").read_text())
    grades = json.loads((evidence / "matrix-grades.json").read_text())
    expected = {(r["case"], r["arm"], r["repeat"]) for r in plan["trials"]}
    actual = {(r["case"], r["arm"], r["repeat"]) for r in grades}
    if expected != actual or len(grades) != 84:
        raise SystemExit(f"Incomplete matrix: {len(grades)}/84; missing={sorted(expected-actual)}; unexpected={sorted(actual-expected)}")
    if any(r["source_score"] is None for r in grades):
        raise SystemExit("Semantic grades remain REVIEW_REQUIRED")
    cases, obligations = [], {}
    for case, verification in CASE_VER.items():
        arms = {arm: [r for r in grades if r["case"] == case and r["arm"] == arm]
                for arm in ("plugin", "baseline")}
        row = {"case": case, "verification": verification}
        for arm, trials in arms.items():
            ordered = sorted(trials, key=lambda r: r["repeat"])
            row[arm] = {
                "scores": [r["source_score"] for r in ordered],
                "mean": statistics.mean(r["source_score"] for r in trials),
                "threshold_passes": sum(r["threshold_pass"] for r in trials),
                "strict_passes": sum(r["strict_pass"] for r in trials),
                "activation_passes": sum(r["activation"]["expected"] == r["activation"]["observed"]
                                         for r in trials),
            }
        row["status"] = "PASS" if all(r["strict_pass"] for r in arms["plugin"]) else "FAIL"
        obligations[verification] = row["status"]
        cases.append(row)
    obligations.update({"VER-12": "NOT_RUN", "VER-13": "NOT_RUN"})
    runtime_rows = [json.loads(p.read_text()) for p in (evidence / "matrix").glob("*/result.json")]
    models = sorted({r.get("model") for r in runtime_rows if r.get("model")})
    plugin = [r for r in grades if r["arm"] == "plugin"]
    baseline = [r for r in grades if r["arm"] == "baseline"]
    plugin_mean = statistics.mean(r["source_score"] for r in plugin)
    baseline_mean = statistics.mean(r["source_score"] for r in baseline)
    return {
        "candidate_sha256": plan["candidate_sha256"], "definitions_sha256": plan["definitions_sha256"],
        "runtime": plan["codex_version"], "models": models, "total_trials": 84, "cases": cases,
        "plugin_mean": plugin_mean, "baseline_mean": baseline_mean, "mean_delta": plugin_mean-baseline_mean,
        "plugin_threshold_passes": sum(r["threshold_pass"] for r in plugin),
        "plugin_strict_passes": sum(r["strict_pass"] for r in plugin),
        "baseline_strict_passes": sum(r["strict_pass"] for r in baseline),
        "plugin_activation_passes": sum(r["activation"]["expected"] == r["activation"]["observed"] for r in plugin),
        "baseline_activation_passes": sum(r["activation"]["expected"] == r["activation"]["observed"] for r in baseline),
        "run_errors": [r for r in grades if r["status"] not in ("completed", "awaiting_input")],
        "obligations": obligations,
        "qualification": "Source evaluation only. VER-12 and VER-13 owner/manual acceptance, installation, deployment and framework acceptance were not performed.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args()
    output = build_summary(args.evidence)
    (args.evidence / "evaluation-summary.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({k: v for k, v in output.items() if k != "cases"}, indent=2))


if __name__ == "__main__":
    main()
