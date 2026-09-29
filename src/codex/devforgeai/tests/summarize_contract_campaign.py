"""Preserve the complete frozen denominator and separate evidence from qualification."""
from __future__ import annotations
import argparse
import collections
import datetime
import hashlib
import json
from pathlib import Path


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def trial_id(row):
    return "--".join(str(row[k]) for k in ("skill", "case", "arm", "repeat"))


def native_classification(row, result):
    """Only completed behavior, or the declared question checkpoint, is assessable."""
    if row["attempt_state"] != "SEALED":
        return row["attempt_state"]
    status = result.get("status")
    if status == "completed":
        return "COMPLETED"
    if (status == "awaiting_input" and row.get("skill") == "architecture"
            and row.get("case") == "existing-arch-not-duplicated" and row.get("mode") == "plan"):
        return "EXPECTED_QUESTION_GATE"
    error = result.get("error") or {}
    code = error.get("codexErrorInfo") if isinstance(error, dict) else None
    if code == "usageLimitExceeded":
        return "PLATFORM_LIMIT"
    if status == "harness_error":
        return "HARNESS_ERROR"
    if status == "timeout":
        return "TIMEOUT"
    return "NATIVE_INTERRUPTION"


def apply_native_boundary(row, result):
    row = dict(row)
    classification = native_classification(row, result)
    row["native_classification"] = classification
    assessable = classification in {"COMPLETED", "EXPECTED_QUESTION_GATE"}
    row["behavior_assessable"] = assessable
    if assessable:
        row["behavior_status"] = "REVIEW_REQUIRED" if row["semantic_pending"] else "PASS" if row["corrected_binary"] else "FAIL"
    else:
        row["partial_artifact_diagnostics"] = {k: row.get(k) for k in (
            "original_source_score", "corrected_source_score", "original_failed_checks",
            "corrected_failed_checks", "failed_guards", "semantic_pending")}
        row.update(original_binary=False, corrected_binary=False,
                   original_source_score=None, corrected_source_score=None,
                   original_failed_checks=[], corrected_failed_checks=[], failed_guards=[],
                   semantic_pending=False, strict_current_write=False if row.get("arm") == "plugin" else None)
        row["behavior_status"] = "NOT_RUN" if classification == "NOT_RUN" else "NOT_ASSESSED_" + classification
        row["assessment_note"] = "Raw grader views are retained as partial-artifact diagnostics; an unfinished native turn is not a completed behavior test."
    return row


def case_status(rows, key):
    assert len(rows) == 3
    if any(r["attempt_state"] in {"NOT_RUN", "RUNNING", "MISSING_EVIDENCE"} for r in rows):
        return "INCOMPLETE"
    if any(r.get("behavior_assessable") is False for r in rows):
        return "INCOMPLETE_NATIVE_INTERRUPTION"
    if any(r.get("semantic_pending") for r in rows):
        return "UNASSESSED"
    return "PASS" if all(r[key] is True for r in rows) else "FAIL"


def strict_current_write(binary, identity_open, trace_signals):
    return bool(binary and identity_open is False and trace_signals == 0)


def controls():
    passed = {"attempt_state": "SEALED", "semantic_pending": False, "binary": True}
    assert case_status([passed] * 3, "binary") == "PASS"
    assert case_status([passed, passed, {**passed, "binary": False, "score": 0.99}], "binary") == "FAIL"
    assert case_status([passed, passed, {**passed, "attempt_state": "NOT_RUN"}], "binary") == "INCOMPLETE"
    assert case_status([passed, passed, {**passed, "semantic_pending": True}], "binary") == "UNASSESSED"
    assert strict_current_write(True, False, 0)
    assert not strict_current_write(True, True, 0)
    assert not strict_current_write(True, None, 0)
    assert not strict_current_write(True, False, None)
    assert not strict_current_write(True, False, 1)
    return ["3/3 passes", "2/3 cannot pass even with high source scores", "missing trial retained", "unassessed semantic rubric retained", "identity gap blocks strict qualification"]


def manual_rows(n, plan):
    assessed = {r["scenario"]: r for r in read(n / "manual/assessments.json")["scenarios"]}
    manual_plan = read(n / "manual/plan.json")
    static = read(n / "manual/static-checks.json")["checks"]
    result = []
    for obligation in plan["manual"]:
        ident = obligation["id"]
        if ident in static:
            evidence = static[ident]
            result.append({"id": ident, "status": evidence.get("status", evidence.get("source_status")),
                           "scope": "source check", "evidence": "manual/static-checks.json",
                           "installed_status": evidence.get("installed_status", "NOT_APPLICABLE")})
            continue
        scenario = next(s for s in manual_plan["scenarios"] if ident in s["obligations"])
        a = assessed.get(scenario["name"], {})
        status = a.get("mechanical_status", "NOT_RUN")
        if ident in a.get("coverage", {}):
            status = a["coverage"][ident].split(":", 1)[0]
        if ident == "PRD-BEH-10-identity-disclosure":
            status = "PASS" if a.get("checks", {}).get("unavailable_disclosed") else "FAIL"
        result.append({"id": ident, "scenario": scenario["name"], "status": status,
                       "raw_sha256": a.get("raw_sha256"), "scope": "specified manual behavior",
                       "exact_identity_open": a.get("exact_identity_open", True),
                       "unreached_branches": a.get("coverage", {}).get("requested_save_answer"),
                       "evidence": "manual/attempts/" + scenario["name"] + "/assessment.json"})
    assert len(result) == 22 and len({r["id"] for r in result}) == 22
    return result


def summarize(n):
    plan = read(n / "plan.json")
    original = {trial_id(r): r for r in read(n / "grades.json")["results"]}
    corrected_view = "grades-v5.json" if (n / "grades-v5.json").is_file() else "grades-v4.json"
    corrected = {trial_id(r): r for r in read(n / corrected_view)["results"]}
    identities = {r["attempt"]: r for r in read(n / "provenance-audit.json")["attempts"]}
    isolation = {r["attempt"]: r for r in read(n / "trace-audit.json")["attempts"]}
    rows = []
    for task in plan["trials"]:
        ident = trial_id(task)
        trial = n / "matrix" / ident
        a, b = original[ident], corrected[ident]
        result_path = trial / "result.json"
        state = "SEALED" if result_path.exists() else ("RUNNING" if trial.exists() else "NOT_RUN")
        raw = trial / "protocol.jsonl"
        required = [raw, trial / "after.json", trial / "before.json", trial / "git-after.json", trial / "git-before.json"]
        if state == "SEALED" and not all(p.is_file() for p in required):
            state = "MISSING_EVIDENCE"
        p = identities.get("matrix/" + ident)
        trace = isolation.get("matrix/" + ident)
        trace_signals = None if trace is None else sum(len(trace[k]) for k in ("cross_trial_references", "broad_tmp_commands", "primary_or_evaluator_markers"))
        identity_open = None if task["arm"] == "baseline" or p is None else p["qualification_identity_open"]
        strict = None if task["arm"] == "baseline" else strict_current_write(b["binary_conformance"], identity_open, trace_signals)
        row = {"id": ident, **{k: v for k, v in task.items() if k != "status"},
               "attempt_state": state, "native_status": a["native_status"],
               "original_binary": a["binary_conformance"], "corrected_binary": b["binary_conformance"],
               "original_source_score": a.get("source_score"), "corrected_source_score": b.get("source_score"),
               "semantic_pending": bool(a.get("semantic_pending") or b.get("semantic_pending")),
               "identity_open": identity_open, "trace_signals": trace_signals,
               "strict_current_write": strict,
               "original_failed_checks": [g["grader"] for g in a.get("source_grades", []) if g["applicable"] and g["passed"] is False],
               "corrected_failed_checks": [g["grader"] for g in b.get("source_grades", []) if g["applicable"] and g["passed"] is False],
               "failed_guards": [k for k, v in b.get("guards", {}).items() if not v],
               "evidence": "matrix/" + ident}
        if raw.is_file() and state == "SEALED":
            row["raw_sha256"] = sha(raw)
        r = read(result_path) if result_path.exists() else {}
        if result_path.exists():
            row.update(elapsed_seconds=r.get("elapsed_seconds"), native_error=r.get("error"))
        rows.append(apply_native_boundary(row, r))
    assert len(rows) == 270 and len({r["id"] for r in rows}) == 270
    cases = []
    for skill in ("prd", "architecture"):
        names = sorted({r["case"] for r in rows if r["skill"] == skill})
        assert len(names) == {"prd": 29, "architecture": 16}[skill]
        for name in names:
            case = {"skill": skill, "case": name, "arms": {}}
            for arm in ("plugin", "baseline"):
                subset = [r for r in rows if (r["skill"], r["case"], r["arm"]) == (skill, name, arm)]
                assert sorted(r["repeat"] for r in subset) == [1, 2, 3]
                case["arms"][arm] = {"sealed": sum(r["attempt_state"] == "SEALED" for r in subset),
                    "original_passes": sum(r["original_binary"] for r in subset),
                    "corrected_passes": sum(r["corrected_binary"] for r in subset),
                    "original_status": case_status(subset, "original_binary"),
                    "corrected_status": case_status(subset, "corrected_binary"),
                    "strict_status": case_status(subset, "strict_current_write") if arm == "plugin" else "NOT_APPLICABLE",
                    "identity_open_repetitions": sum(r["identity_open"] is True for r in subset),
                    "source_scores_original": [r["original_source_score"] for r in subset],
                    "source_scores_corrected": [r["corrected_source_score"] for r in subset]}
            cases.append(case)
    totals = []
    for skill in ("prd", "architecture"):
        for arm in ("plugin", "baseline"):
            subset = [r for r in rows if r["skill"] == skill and r["arm"] == arm]
            case_rows = [c["arms"][arm] for c in cases if c["skill"] == skill]
            totals.append({"skill": skill, "arm": arm, "planned": len(subset),
                           "attempt_states": dict(collections.Counter(r["attempt_state"] for r in subset)),
                           "native_statuses": dict(collections.Counter(r["native_status"] for r in subset)),
                           "native_classifications": dict(collections.Counter(r["native_classification"] for r in subset)),
                           "behavior_results": dict(collections.Counter(r["behavior_status"] for r in subset)),
                           "original_binary_passes": sum(r["original_binary"] for r in subset),
                           "corrected_binary_passes": sum(r["corrected_binary"] for r in subset),
                           "original_cases_passed": sum(c["original_status"] == "PASS" for c in case_rows),
                           "corrected_cases_passed": sum(c["corrected_status"] == "PASS" for c in case_rows),
                           "strict_cases_passed": sum(c["strict_status"] == "PASS" for c in case_rows) if arm == "plugin" else None})
    manual = manual_rows(n, plan)
    supplemental = read(n / "manual/supplemental-source-checks.json")["checks"] if (n / "manual/supplemental-source-checks.json").is_file() else []
    covered = {r["id"] for r in supplemental if r["status"] == "PASS"}
    inherited = [{"id": "ARCH-VER-12-" + part, "status": "NOT_RUN", "reason": "Not independently exercised in this contract-delta manual campaign; historical passes are not inherited."} for part in ("a", "b-yes", "b-no", "c", "d", "e", "g", "h", "j", "k", "l") if "ARCH-VER-12-" + part not in covered]
    inherited.append({"id": "ARCH-VER-13-deployed-demonstration", "status": "NOT_RUN", "reason": "Deployed-plugin custody demonstration and PR excluded from authorized scope; candidate/runtime hashes are separate evidence."})
    finished = (n / "matrix-complete.json").is_file()
    platform_stop = read(n / "platform-stop.json") if (n / "platform-stop.json").exists() else None
    report = {"generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "source_commit": plan["source_commit"], "candidate_sha256": plan["candidate_sha256"],
              "frozen_plan_sha256": sha(n / "plan.json"), "planned": 270,
              "corrected_view": corrected_view,
              "matrix_finished": finished, "platform_stop": platform_stop,
              "status": "BLOCKED_PLATFORM_LIMIT_NOT_QUALIFIED" if platform_stop else "EVALUATED_NOT_QUALIFIED" if finished else "EVALUATION_IN_PROGRESS_NOT_QUALIFIED",
              "qualification": "Source-check scores and binary behavior are distinct. Three binary repetitions need 3/3 at threshold 0.8. Strict current-write counts also require scoped identity and no trace-audit signals; they do not waive missing manual, installation, or owner acceptance obligations.",
              "controls": controls(), "totals": totals, "cases": cases, "trials": rows,
              "manual": manual, "supplemental_source_checks": supplemental, "inherited_manual_not_run": inherited,
              "not_run_trials": [r["id"] for r in rows if r["attempt_state"] == "NOT_RUN"],
              "running_trials": [r["id"] for r in rows if r["attempt_state"] == "RUNNING"],
              "native_classifications": dict(collections.Counter(r["native_classification"] for r in rows)),
              "behavior_results": dict(collections.Counter(r["behavior_status"] for r in rows)),
              "interrupted_trials": [r["id"] for r in rows if r["attempt_state"] == "SEALED" and not r["behavior_assessable"]],
              "semantic_pending_trials": [r["id"] for r in rows if r["semantic_pending"]],
              "installation": "NOT_RUN", "git_delivery": "NOT_DONE", "owner_acceptance": "PENDING"}
    (n / "summary.json").write_text(json.dumps(report, indent=2) + "\n")
    lines = ["# Frozen contract campaign results", "", report["status"], "",
             "The frozen denominator is 270 trials: 174 PRD and 96 Architecture. Each case requires three plugin and three isolated baseline repetitions. A binary case passes only at 3/3. Source-check scores are retained separately in summary.json.", "",
             "| Skill | Arm | Attempted / planned | Completed | Platform interruptions | Binary passes: original → corrected | Cases passed: original → corrected |", "|---|---|---:|---:|---:|---:|---:|"]
    for t in totals:
        lines.append(f"| {t['skill']} | {t['arm']} | {t['attempt_states'].get('SEALED', 0)}/{t['planned']} | {t['native_classifications'].get('COMPLETED', 0)} | {t['native_classifications'].get('PLATFORM_LIMIT', 0)} | {t['original_binary_passes']} → {t['corrected_binary_passes']} | {t['original_cases_passed']} → {t['corrected_cases_passed']} |")
    if platform_stop:
        counts = report["native_classifications"]
        lines += ["", f"The native host stopped on usageLimitExceeded: {counts.get('COMPLETED', 0)} turns completed, {counts.get('PLATFORM_LIMIT', 0)} attempts were interrupted, and {counts.get('NOT_RUN', 0)} planned trials remain NOT_RUN. Interrupted attempts are NOT_ASSESSED_PLATFORM_LIMIT, not behavior failures. Their raw grader views and partial artifacts remain available as diagnostics. No interrupted attempt was retried.", "", "[Platform interruption receipt](platform-interruptions.json) binds all interrupted results and raw traces. No third repetition ran, so no automated case can establish the required 3/3 result."]
    lines += ["", "The corrected view fixes the current-row Codex tool literal and applies unscoped positive activation assertions to plugin trials. Explicit arm metadata and negative activation assertions are unchanged; baseline plugin access still fails its guard. Original definitions, original grades and the earlier v4 view remain available. The authors-list conflict is not relaxed. Strict identity, trace review, manual obligations and owner acceptance remain separate from these behavior counts.", "", "## Complete case denominator", "", "Each arm shows original passes → corrected passes out of 3, followed by corrected case status.", "", "| Skill / case | Plugin | Baseline | Plugin strict current-write |", "|---|---|---|---|"]
    for c in cases:
        arms = [f"{c['arms'][a]['original_passes']} → {c['arms'][a]['corrected_passes']}/3 {c['arms'][a]['corrected_status']}" for a in ("plugin", "baseline")]
        lines.append(f"| {c['skill']} / {c['case']} | {arms[0]} | {arms[1]} | {c['arms']['plugin']['strict_status']} |")
    lines += ["", "## Current manual obligations", "", "| Obligation | Recorded result | Evidence |", "|---|---|---|"]
    for r in manual:
        lines.append(f"| {r['id']} | {r['status']} | [{r.get('scenario', 'source check')}]({r['evidence']}) |")
    lines += ["", "Both cancellation actors failed to offer a save choice; their yes/no branches remain NOT_RUN. The approved-extension manual scenario also retains the recommendation mismatch and BEH-10/VER-32 author-list conflict. Successful identity disclosure leaves exact identity open. Installed parity and owner acceptance are not established.", "", "## Remaining evidence", "", "[summary.json](summary.json) lists every scheduled trial, raw native status, semantic-review gap, failed source check and guard, scoped identity result, NOT_RUN trial and inherited unrun manual obligation. Raw traces, trial workspaces and intermediate turns stay local; per-attempt hashes bind their retained evidence.", "", "No push, PR, merge, installation, deployment or marketplace change was performed."]
    (n / "RESULTS.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({"matrix_finished": finished, "states": dict(collections.Counter(r["attempt_state"] for r in rows)), "semantic_pending": len(report["semantic_pending_trials"]), "manual": dict(collections.Counter(r["status"] for r in manual))}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args()
    summarize(args.evidence.resolve())
