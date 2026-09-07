#!/usr/bin/env python3
"""Reduce frozen, evidence-bound skill check records without executing candidate code."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

OUTCOMES = {"PASS", "FAIL", "NOT_RUN", "COULD_NOT_RUN", "NOT_APPLICABLE"}
GROUPS = ("intake", "structure", "ai_review", "C", "B", "A")
MAX_JSON = 32 * 1024 * 1024

class RecordError(Exception):
    pass

def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise RecordError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result

def load_json(path):
    try:
        if path.stat().st_size > MAX_JSON:
            raise RecordError(f"JSON input exceeds {MAX_JSON} bytes: {path}")
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates)
    except (OSError, UnicodeError, ValueError) as exc:
        raise RecordError(f"Cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RecordError(f"Expected object in {path}")
    return value

def digest(path):
    value = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                value.update(block)
    except OSError as exc:
        raise RecordError(f"Cannot hash {path}: {exc}") from exc
    return value.hexdigest()

def text(value, name):
    if not isinstance(value, str) or not value.strip() or "{{" in value or "}}" in value:
        raise RecordError(f"{name} must be a populated string")
    return value

def reference(value, base):
    if not isinstance(value, dict):
        raise RecordError("Evidence reference must be an object")
    path = Path(text(value.get("path"), "reference.path"))
    if not path.is_absolute():
        path = base / path
    path = path.resolve()
    expected = value.get("sha256")
    if not isinstance(expected, str) or not re.fullmatch(r"[a-f0-9]{64}", expected):
        raise RecordError(f"Missing SHA-256 for {path}")
    if not path.is_file() or digest(path) != expected:
        raise RecordError(f"Missing or changed referenced bytes: {path}")
    return {"path": str(path), "sha256": expected}

def aggregate(values):
    values = list(values)
    if not values:
        return "NOT_RUN"
    for outcome in ("FAIL", "COULD_NOT_RUN", "NOT_RUN"):
        if outcome in values:
            return outcome
    return "PASS" if "PASS" in values else "NOT_APPLICABLE"

def under(path, root):
    return path == root or root in path.parents

def manifest_current(root, expected):
    if not isinstance(expected, dict) or not expected:
        raise RecordError("Structural report has no complete candidate file manifest")
    try:
        paths = list(root.rglob("*"))
        for path in paths:
            if path.is_symlink() and not under(path.resolve(), root):
                raise RecordError(f"Candidate symlink escapes root: {path}")
        actual = {p.relative_to(root).as_posix(): digest(p) for p in paths if p.is_file()}
    except OSError as exc:
        raise RecordError(f"Cannot inventory candidate: {exc}") from exc
    if actual != expected:
        raise RecordError("Candidate changed since its structural report; start a new affected iteration")

def summarize(plan_path, result_path, output_path):
    plan = load_json(plan_path)
    record = load_json(result_path)
    if plan.get("schema_version") != "devforge.skill-validation-plan/v1":
        raise RecordError("Unsupported validation plan schema")
    if record.get("schema_version") != "devforge.skill-validation-results/v1":
        raise RecordError("Unsupported results schema")
    run_id = text(plan.get("run_id"), "plan.run_id")
    if record.get("run_id") != run_id:
        raise RecordError("Plan and results run_id differ")
    bound_plan = reference(record.get("plan"), result_path.parent)
    if Path(bound_plan["path"]) != plan_path or bound_plan["sha256"] != digest(plan_path):
        raise RecordError("Results are not bound to the supplied plan")
    candidate_root = Path(text(plan.get("candidate_root"), "candidate_root"))
    if not candidate_root.is_absolute():
        raise RecordError("candidate_root must be absolute")
    candidate_root = candidate_root.resolve()
    if not candidate_root.is_dir() or under(output_path, candidate_root):
        raise RecordError("Candidate must exist and output must be outside the candidate")
    if plan.get("provider") != "codex":
        raise RecordError("This authored profile supports Codex only")
    source_refs = plan.get("input_refs")
    if not isinstance(source_refs, list) or not source_refs:
        raise RecordError("Plan must bind specification, rubric, cases and selected contracts")
    input_refs = [reference(item, plan_path.parent) for item in source_refs]
    required_kinds = {"specification", "rubric", "cases", "framework_contract"}
    if not required_kinds.issubset({item.get("kind") for item in source_refs}):
        raise RecordError("Plan is missing an input kind")
    baseline = plan.get("baseline")
    if not isinstance(baseline, dict) or baseline.get("kind") not in {"old_skill", "without_skill"}:
        raise RecordError("Declare old_skill or without_skill baseline")
    budget = plan.get("budget")
    if not isinstance(budget, dict) or any(
        isinstance(budget.get(k), bool) or not isinstance(budget.get(k), int) or budget[k] <= 0
        for k in ("max_attempts", "max_seconds")
    ):
        raise RecordError("Freeze positive max_attempts and max_seconds before execution")

    definitions = plan.get("checks")
    results = record.get("results")
    if not isinstance(definitions, list) or not definitions or not isinstance(results, list):
        raise RecordError("Plan checks and result records must be arrays")
    expected = {}
    for item in definitions:
        if not isinstance(item, dict):
            raise RecordError("Each planned check must be an object")
        check_id = text(item.get("id"), "check.id")
        if check_id in expected:
            raise RecordError(f"Duplicate planned check: {check_id}")
        if item.get("group") not in GROUPS:
            raise RecordError(f"Invalid evidence group: {check_id}")
        if item.get("expectation") not in {"pass", "observation", "excluded"}:
            raise RecordError(f"Invalid expectation: {check_id}")
        text(item.get("description"), f"{check_id}.description")
        if item["expectation"] == "excluded":
            text(item.get("exclusion_reason"), f"{check_id}.exclusion_reason")
        expected[check_id] = item
    for group in GROUPS:
        if not any(x["group"] == group and x["expectation"] == "pass" for x in expected.values()):
            raise RecordError(f"Required group has no passing-obligation check: {group}")
    for criterion in (f"AI-R{n:02d}" for n in range(1, 11)):
        if criterion not in expected or expected[criterion]["expectation"] not in {"pass", "excluded"}:
            raise RecordError(f"Missing required rubric check: {criterion}")
    if not any(x["group"] == "B" and x["expectation"] == "observation" for x in expected.values()):
        raise RecordError("B requires an observed baseline arm")

    found = {}
    for item in results:
        if not isinstance(item, dict):
            raise RecordError("Each check result must be an object")
        check_id = text(item.get("check_id"), "result.check_id")
        if check_id not in expected or check_id in found:
            raise RecordError(f"Unexpected or duplicate result: {check_id}")
        if item.get("outcome") not in OUTCOMES:
            raise RecordError(f"Invalid outcome: {check_id}")
        found[check_id] = item

    reduced = []
    for check_id, definition in expected.items():
        observed = found.get(check_id)
        if observed is None:
            reduced.append({"check_id": check_id, "group": definition["group"],
                            "observed_outcome": "NOT_RUN", "effective_outcome": "NOT_RUN",
                            "cause": "No result record", "evidence": []})
            continue
        outcome = observed["outcome"]
        reason = text(observed.get("reason"), f"{check_id}.reason")
        evidence = observed.get("evidence", [])
        if not isinstance(evidence, list):
            raise RecordError(f"Evidence must be an array: {check_id}")
        resolved = []
        evidence_error = None
        try:
            resolved = [reference(item, result_path.parent) for item in evidence]
        except RecordError as exc:
            evidence_error = str(exc)
        if definition["expectation"] == "excluded":
            effective = "NOT_APPLICABLE" if outcome == "NOT_APPLICABLE" else "COULD_NOT_RUN"
        elif outcome == "NOT_APPLICABLE":
            effective = "COULD_NOT_RUN"
            reason = "Required observation cannot be excluded after the plan was frozen: " + reason
        elif outcome in {"PASS", "FAIL"} and not evidence:
            effective = "COULD_NOT_RUN"
            reason = "A measured outcome requires exact evidence: " + reason
        elif definition["expectation"] == "observation" and outcome in {"PASS", "FAIL"}:
            effective = "PASS"
        else:
            effective = outcome
        if evidence_error:
            effective = "COULD_NOT_RUN"
            reason = evidence_error
        reduced.append({"check_id": check_id, "group": definition["group"],
                        "observed_outcome": outcome, "effective_outcome": effective,
                        "cause": reason, "evidence": resolved})

    structural_outcome = "COULD_NOT_RUN"
    freshness = "COULD_NOT_RUN"
    structural_ref = None
    freshness_reason = "No structural report supplied"
    if record.get("structural_report") is not None:
        try:
            structural_ref = reference(record["structural_report"], result_path.parent)
            structural = load_json(Path(structural_ref["path"]))
            if structural.get("schema_version") != "devforge.skill-structure/v1":
                raise RecordError("Unexpected structural report schema")
            if Path(structural.get("skill_root", "")).resolve() != candidate_root:
                raise RecordError("Structural report describes a different candidate")
            if structural.get("mode") != "source":
                raise RecordError("Candidate freshness requires a source structural report")
            structural_outcome = structural.get("overall")
            if structural_outcome not in {"PASS", "FAIL", "COULD_NOT_RUN"}:
                raise RecordError("Invalid structural outcome")
            manifest_current(candidate_root, structural.get("files_sha256"))
            freshness, freshness_reason = "PASS", "Current source bytes match the structural report"
        except RecordError as exc:
            freshness_reason = str(exc)

    # Match static AI declarations to their separately preserved review.
    ai_consistency = "COULD_NOT_RUN"
    ai_reason = "No independent AI review supplied"
    ai_ref = None
    if record.get("ai_review") is not None:
        try:
            ai_ref = reference(record["ai_review"], result_path.parent)
            review = load_json(Path(ai_ref["path"]))
            if review.get("schema_version") != "devforge.skill-ai-review/v1" or review.get("run_id") != run_id:
                raise RecordError("AI review has the wrong schema or run identity")
            criteria = review.get("criteria")
            if not isinstance(criteria, list):
                raise RecordError("AI criteria must be an array")
            by_id = {}
            for item in criteria:
                if not isinstance(item, dict) or item.get("id") in by_id:
                    raise RecordError("Invalid or duplicate AI criterion")
                by_id[item.get("id")] = item
            for number in range(1, 11):
                criterion_id = f"R{number:02d}"
                check_id = "AI-" + criterion_id
                item = by_id.get(criterion_id)
                observed = found.get(check_id)
                if item is None or observed is None or item.get("outcome") != observed.get("outcome"):
                    raise RecordError(f"AI criterion and result differ: {criterion_id}")
                text(item.get("reason"), f"{criterion_id}.reason")
                if item["outcome"] in {"PASS", "FAIL"}:
                    if not item.get("evidence"):
                        raise RecordError(f"AI criterion lacks evidence: {criterion_id}")
                    for evidence in item["evidence"]:
                        reference(evidence, Path(ai_ref["path"]).parent)
            ai_consistency, ai_reason = "PASS", "Result records match preserved AI criterion outcomes"
        except RecordError as exc:
            ai_reason = str(exc)

    # Native declared outcomes must agree with a case grade and a run manifest.
    # This checks records, not the truth of a claimed observation.
    for item in reduced:
        definition = expected[item["check_id"]]
        if item["group"] not in {"A", "B", "C"} or item["observed_outcome"] not in {"PASS", "FAIL"}:
            continue
        try:
            observed = found[item["check_id"]]
            grade_ref = reference(observed.get("case_grade"), result_path.parent)
            grade = load_json(Path(grade_ref["path"]))
            if grade.get("schema_version") != "devforge.skill-case-grade/v1":
                raise RecordError("Invalid case grade schema")
            for field, expected_value in (
                ("run_id", run_id), ("case_id", definition.get("case_id")),
                ("arm", definition.get("arm")), ("attempt_id", definition.get("attempt_id")),
                ("overall", observed["outcome"])
            ):
                if expected_value is None or grade.get(field) != expected_value:
                    raise RecordError(f"Case grade mismatch: {field}")
            run_ref = reference(grade.get("run_manifest"), Path(grade_ref["path"]).parent)
            manifest = load_json(Path(run_ref["path"]))
            if manifest.get("schema_version") != "devforge.skill-run/v1" or manifest.get("tier") != item["group"]:
                raise RecordError("Run manifest schema/tier mismatch")
            if manifest.get("provider") != "codex":
                raise RecordError("Run provider mismatch")
            for field in ("client_version", "model_configuration", "context_isolation"):
                text(manifest.get(field), f"run_manifest.{field}")
            if manifest.get("case_id") != definition.get("case_id") or manifest.get("arm") != definition.get("arm"):
                raise RecordError("Run manifest case/arm mismatch")
            if manifest.get("attempt_id") != definition.get("attempt_id"):
                raise RecordError("Run manifest attempt mismatch")
            if manifest.get("outcome") != observed["outcome"]:
                raise RecordError("Run manifest and grade outcomes differ")
            reference({"path": manifest.get("transcript"), "sha256": manifest.get("transcript_sha256")},
                      Path(run_ref["path"]).parent)
            if not manifest.get("execution_ref"):
                raise RecordError("Native run lacks assignment reference")
            item["case_grade"] = grade_ref
            item["run_manifest"] = run_ref
        except RecordError as exc:
            item["effective_outcome"] = "COULD_NOT_RUN"
            item["cause"] = str(exc)

    groups = {g: aggregate(x["effective_outcome"] for x in reduced if x["group"] == g) for g in GROUPS}
    groups["structure"] = aggregate([groups["structure"], structural_outcome])
    groups["ai_review"] = aggregate([groups["ai_review"], ai_consistency])
    overall = aggregate([*groups.values(), freshness])
    disposition = "revise" if overall == "FAIL" else (
        "suitable_for_stated_scope" if overall == "PASS" else "insufficient_evidence")
    return {
        "schema_version": "devforge.skill-validation-decision/v1",
        "run_id": run_id,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "plan": {"path": str(plan_path), "sha256": digest(plan_path)},
        "results": {"path": str(result_path), "sha256": digest(result_path)},
        "input_refs": input_refs, "candidate_root": str(candidate_root),
        "structural_report": structural_ref,
        "ai_review": ai_ref, "ai_record_consistency": {"outcome": ai_consistency, "reason": ai_reason},
        "candidate_freshness": {"outcome": freshness, "reason": freshness_reason},
        "groups": groups, "checks": reduced, "overall": overall,
        "coverage_complete": all(x["effective_outcome"] not in {"NOT_RUN", "COULD_NOT_RUN"} for x in reduced)
                             and freshness == "PASS" and ai_consistency == "PASS"
                             and structural_outcome != "COULD_NOT_RUN",
        "disposition": disposition, "external_acceptance": "NOT_GRANTED",
        "limits": ["Checks evidence identity and declared outcomes only.",
                   "Does not authenticate observations or establish reviewer independence.",
                   "Does not grant runtime enforcement or external acceptance.",
                   "Baseline FAIL can be an observed comparison, not a target failure."]
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--results", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    plan, results, output = (x.resolve() for x in (args.plan, args.results, args.output))
    try:
        decision = summarize(plan, results, output)
        with output.open("x", encoding="utf-8") as stream:
            json.dump(decision, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
    except (RecordError, OSError, ValueError, TypeError, KeyError) as exc:
        print(f"COULD_NOT_RUN: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"output": str(output), "overall": decision["overall"],
                      "coverage_complete": decision["coverage_complete"]}))
    return 0 if decision["overall"] == "PASS" else 1 if decision["overall"] == "FAIL" else 2

if __name__ == "__main__":
    raise SystemExit(main())
