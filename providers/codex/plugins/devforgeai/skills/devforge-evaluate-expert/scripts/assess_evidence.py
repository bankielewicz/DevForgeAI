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

def no_constant(value):
    raise RecordError(f"Nonfinite JSON constant: {value}")

def load_json(path):
    try:
        if path.stat().st_size > MAX_JSON:
            raise RecordError(f"JSON input exceeds {MAX_JSON} bytes: {path}")
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates,
                           parse_constant=no_constant)
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

def summarize_v1(plan_path, result_path, output_path):
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

V2_ADDITIONS = set("task_results assertion_results report_completion validation_disposition routine_adoption_eligible lineage owner_acceptance_ref receiving_transfer".split())
PLAN_KEYS = set("schema_version run_id provider candidate_root input_refs baseline assignment runtime budget checks findings_from_previous_iteration criteria_freeze_record scope_exclusions plan_scope validation_policy".split())
RESULT_KEYS = set("schema_version run_id plan structural_report ai_review results findings".split()) | V2_ADDITIONS
POLICY_KEYS = set("version policy_ref acceptance_ref mode requested_claim accepted_scope_ref baseline_identity candidate_identity lineage impact compatibility catalog_refs catalog_assertions assertions task_selection observations call_graph selection_reviewer".split())
TASKS = tuple(f"T{i:02}" for i in range(1, 13))
SELECTIONS = {"REQUIRED", "NOT_SELECTED", "NOT_APPLICABLE"}
INVARIANTS = {f"R{i:02}" for i in range(1, 11)}
CONDITIONS = set("identity input_refs prompt_ref arm variant repetition invocation visibility_ref freshness_ref before_task".split())
RUN_KEYS = set("schema_version run_id tier provider client_version model_configuration installation_mode source_files_sha256 installed_files_sha256 baseline specification_files_sha256 case_files_sha256 fixture_files_sha256 execution_ref context_isolation sibling_availability output_directory transcript outcome cause metrics grading_evidence case_id attempt_id arm transcript_sha256 installation_path native_observations boundary_refs authentication_observation_ref client_state_observation_ref process_ownership_ref effective_configuration_ref worker_visible_input_refs operator_only_input_refs deviations environment_setup_ref validation_plan_ref workspace_allocation_ref workspace_id client_state_directory observation_id assertion_ids selection evidence_kind conditions integrity raw_output_refs".split())
GRADE_KEYS = set("schema_version run_id case_id attempt_id arm run_manifest case_definition grader dimensions overall cause finding_ids limitations assertion_judgments".split())


def require(condition, reason):
    if not condition:
        raise RecordError(reason)


def exact(value, keys, name):
    require(isinstance(value, dict) and set(value) == set(keys), f"{name}: unknown or missing keys")
    return value


def rows(value, name):
    require(isinstance(value, list) and len(value) <= 256, f"{name}: expected bounded array")
    return value


def unique(value, name):
    value = rows(value, name)
    for item in value:
        text(item, name)
    require(len(set(value)) == len(value), f"{name}: duplicate identity")
    return set(value)


def indexed(value, key, fields, name):
    result = {}
    for row in rows(value, name):
        exact(row, fields.split(), name)
        identity = text(row[key], name)
        require(identity not in result, f"{name}: duplicate {identity}")
        result[identity] = row
    return result


def pin(value):
    exact(value, {"path", "sha256"}, "v2 pin")
    path = Path(text(value["path"], "pin.path"))
    require(path.is_absolute() and str(path.resolve()) == value["path"], "Noncanonical v2 pin path")
    return reference(value, path.parent)


def walk_pins(value):
    if isinstance(value, dict):
        if "path" in value and "sha256" in value:
            pin({k: value[k] for k in ("path", "sha256")})
        else:
            for child in value.values():
                walk_pins(child)
    elif isinstance(value, list):
        for child in rows(value, "v2 collection"):
            walk_pins(child)
    elif isinstance(value, float):
        require(value == value and abs(value) != float("inf"), "Nonfinite JSON number")


def identity(value, nullable=False):
    if value is None and nullable:
        return
    exact(value, {"candidate", "environment"}, "identity")
    pin(value["candidate"])
    pin(value["environment"])


def selection_plan(plan):
    """Check portable record bindings; external admission remains runtime-owned."""
    exact(plan, PLAN_KEYS, "v2 plan")
    require(plan["provider"] == "codex", "Unsupported provider")
    p = exact(plan["validation_policy"], POLICY_KEYS, "validation_policy")
    require(p["version"] == "VPR-2" and p["mode"] in {"Routine", "Full"}, "Unsupported policy/mode")
    walk_pins(p)
    pin(p["policy_ref"])
    pin(p["acceptance_ref"])
    for ref in rows(plan["input_refs"], "input refs"):
        exact(ref, {"kind", "path", "sha256"}, "input ref")
        pin({k: ref[k] for k in ("path", "sha256")})
    require({r["kind"] for r in plan["input_refs"]} >= {"specification", "rubric", "cases", "framework_contract"}, "Missing original input kind")
    claim = exact(p["requested_claim"], {"kind", "text", "requires_full", "contract_ref"}, "claim")
    require(claim["kind"] in {"scoped_update", "qualification", "release_support", "diagnostic"} and type(claim["requires_full"]) is bool, "Invalid claim")
    text(claim["text"], "actual requested claim")
    require(claim["kind"] != "qualification" or claim["requires_full"], "Qualification requires Full")
    identity(p["candidate_identity"])
    identity(p["baseline_identity"], True)
    lineage = exact(p["lineage"], {"qualified_anchor", "accepted_unqualified_baseline", "current_routinely_accepted", "previous_acceptance", "acceptance_chain"}, "lineage")
    anchor = exact(lineage["qualified_anchor"], {"status", "identity", "evidence"}, "anchor")
    require(anchor["status"] in {"QUALIFIED", "ABSENT", "UNKNOWN"}, "Unknown qualification status")
    if anchor["status"] == "QUALIFIED":
        identity(anchor["identity"])
        pin(anchor["evidence"])
    else:
        require(anchor["identity"] is None and anchor["evidence"] is None, "Invented qualified identity")
    for key in ("accepted_unqualified_baseline", "current_routinely_accepted"):
        identity(lineage[key], True)
    chain = rows(lineage["acceptance_chain"], "acceptance chain")
    require(len({(r["path"], r["sha256"]) for r in chain}) == len(chain), "Duplicate acceptance")
    if p["mode"] == "Routine":
        require(p["baseline_identity"] is not None and lineage["current_routinely_accepted"] == p["baseline_identity"], "Routine baseline differs from carried acceptance")
        require(lineage["previous_acceptance"] is not None and chain and chain[-1] == lineage["previous_acceptance"], "Routine needs previous acceptance chain")
        require(anchor["status"] == "QUALIFIED" or lineage["accepted_unqualified_baseline"] is not None, "Missing fixed cumulative anchor")
        previous = load_json(Path(lineage["previous_acceptance"]["path"]))
        require(previous.get("candidate_identity") == p["baseline_identity"] and previous.get("accepted_scope_ref") == p["accepted_scope_ref"], "Previous acceptance mismatch")
        old = previous.get("lineage", {})
        require(old.get("qualified_anchor") == anchor and old.get("accepted_unqualified_baseline") == lineage["accepted_unqualified_baseline"], "Cumulative anchor changed")
        require(chain[:-1] == old.get("acceptance_chain"), "Acceptance predecessor chain changed")
    impact = exact(p["impact"], set("immediate_diff cumulative_diff immediate_requirements cumulative_requirements dependency_closure matched_rules bounded full_triggers".split()), "impact")
    require(type(impact["bounded"]) is bool, "Impact bounded must be boolean")
    for key in ("immediate_requirements", "cumulative_requirements", "dependency_closure", "matched_rules", "full_triggers"):
        unique(impact[key], key)
    require(set(impact["matched_rules"]) <= {f"CI-{i:02}" for i in range(1, 10)}, "Unknown impact rule")
    require(set(impact["full_triggers"]) <= set("FIRST_QUALIFICATION EXPLICIT_QUALIFICATION NEW_CAPABILITY_ENVIRONMENT CONTROL_AUTHORITY_CHANGE TRANSFER_CHANGE FULL_CLAIM_CONTRACT UNBOUNDED_IMPACT".split()), "Unknown Full trigger")
    cp = indexed(p["compatibility"], "id", "id disposition old_environment new_environment used_capabilities affected_assertions evidence reason", "compatibility")
    require(set(cp) == {f"CP-{i:02}" for i in range(1, 5)}, "Missing compatibility rule")
    for item in cp.values():
        require(item["disposition"] in {"UNCHANGED", "EVIDENCED", "UNRESOLVED", "NOT_APPLICABLE"}, "Unknown compatibility disposition")
        text(item["reason"], "compatibility reason")
        unique(item["used_capabilities"], "used capabilities")
        unique(item["affected_assertions"], "affected assertions")
        require(item["new_environment"] == p["candidate_identity"]["environment"], "Compatibility candidate environment differs")
        old_environment = p["baseline_identity"]["environment"] if p["baseline_identity"] is not None else None
        require(item["old_environment"] == old_environment, "Compatibility baseline environment differs")
        if item["disposition"] == "UNCHANGED":
            require(item["old_environment"] == item["new_environment"] and item["evidence"], "Equality needs exact evidence")
    require(rows(p["catalog_refs"], "catalog refs"), "Missing original catalog")
    catalog = indexed(p["catalog_assertions"], "assertion_id", "assertion_id case_id source_ref source_pointer variant arm repetition requirement_ids evidence_kinds", "catalog")
    require(catalog, "Missing assertion inventory")
    selected = indexed(p["assertions"], "assertion_id", "assertion_id task_id tier selection rule_ids reason expectation dependency_ids observation_ids", "assertions")
    require(set(catalog) == set(selected), "Selection must account for entire catalog")
    tasks = indexed(p["task_selection"], "task_id", "task_id classification selection assertion_ids reason", "task selection")
    require(tuple(tasks) == TASKS, "All twelve ordered tasks are required")
    assigned = []
    for tid, task in tasks.items():
        require(task["classification"] == "Enforced" and task["selection"] in SELECTIONS, "Task classification/selection changed")
        require(p["mode"] == "Routine" or task["selection"] != "NOT_SELECTED", "Full cannot unselect a native task")
        if tid not in {"T05", "T06", "T07", "T08"}:
            require(task["selection"] == "REQUIRED", "Non-native task cannot be unselected")
        unique(task["assertion_ids"], "task assertions")
        text(task["reason"], "task selection reason")
        assigned.extend(task["assertion_ids"])
    require(len(assigned) == len(set(assigned)) and set(assigned) == set(catalog), "Task assertion inventory mismatch")
    for aid, source in catalog.items():
        require(source["source_ref"] in p["catalog_refs"], "Assertion source is not an original catalog")
        text(source["case_id"], "case id")
        text(source["variant"], "variant")
        require(source["arm"] in {"candidate", "baseline", "none"} and type(source["repetition"]) is int and source["repetition"] > 0, "Invalid arm/repetition")
        require(unique(source["evidence_kinds"], "evidence kinds") and set(source["evidence_kinds"]) <= {"D", "S", "N"}, "Unknown evidence kind")
        unique(source["requirement_ids"], "requirements")
        locator = text(source["source_pointer"], "source pointer")
        if Path(source["source_ref"]["path"]).suffix == ".json":
            node = load_json(Path(source["source_ref"]["path"]))
            require(locator.startswith("/"), "Expected RFC 6901 pointer")
            try:
                for part in locator[1:].split("/"):
                    part = part.replace("~1", "/").replace("~0", "~")
                    node = node[int(part)] if isinstance(node, list) else node[part]
            except (KeyError, ValueError, IndexError, TypeError) as exc:
                raise RecordError("Original assertion locator does not resolve") from exc
        else:
            require(locator in Path(source["source_ref"]["path"]).read_text(), "Original requirement locator missing")
        row = selected[aid]
        require(row["task_id"] in tasks and aid in tasks[row["task_id"]]["assertion_ids"], "Assertion task mismatch")
        require(row["selection"] in SELECTIONS and row["tier"] in {"D", "S", "C", "B", "A"} and row["expectation"] in {"pass", "observation"}, "Invalid assertion selection")
        require(p["mode"] == "Routine" or row["selection"] != "NOT_SELECTED", "Full cannot unselect applicable assertions")
        text(row["reason"], "selection reason")
        require(unique(row["dependency_ids"], "dependencies") <= set(catalog), "Unknown assertion dependency")
        unique(row["observation_ids"], "observation ids")
        rules = unique(row["rule_ids"], "rule ids")
        require(rules <= {f"CI-{i:02}" for i in range(1, 10)} | set(cp), "Unknown selection rule")
        require(tasks[row["task_id"]]["selection"] == "REQUIRED" or row["selection"] == tasks[row["task_id"]]["selection"], "Task hides required assertion")
    for item in cp.values():
        require(set(item["affected_assertions"]) <= set(catalog), "Compatibility references unknown assertions")
    affected = set(impact["immediate_requirements"] + impact["cumulative_requirements"] + impact["dependency_closure"])
    covered = {r for aid, row in selected.items() if row["selection"] != "NOT_SELECTED" for r in catalog[aid]["requirement_ids"]}
    require(affected <= covered, "Immediate/cumulative dependency omitted")
    observations = indexed(p["observations"], "observation_id", "observation_id evidence_kind assertion_ids conditions prerequisite_observation_ids reuse_ref", "observations")
    for oid, obs in observations.items():
        require(obs["evidence_kind"] in {"D", "S", "N"}, "Unknown observation kind")
        aids = unique(obs["assertion_ids"], "observation assertions")
        require(aids and aids <= set(catalog), "Orphan observation")
        c = exact(obs["conditions"], CONDITIONS, "observation conditions")
        identity(c["identity"])
        require(type(c["repetition"]) is int and c["repetition"] > 0, "Invalid condition repetition")
        require(c["invocation"] in {"explicit", "implicit", "loaded", "none"} and c["before_task"] in TASKS, "Invalid observation conditions")
        pin(c["visibility_ref"]); pin(c["freshness_ref"])
        require(unique(obs["prerequisite_observation_ids"], "observation prerequisites") <= set(observations), "Unknown observation prerequisite")
        for aid in aids:
            require(oid in selected[aid]["observation_ids"] and obs["evidence_kind"] in catalog[aid]["evidence_kinds"], "Observation selection/kind mismatch")
            require(all(c[k] == catalog[aid][k] for k in ("arm", "variant", "repetition")), "Cross-arm/variant observation reuse")
            expected_identity = p["baseline_identity"] if c["arm"] == "baseline" else p["candidate_identity"]
            require(c["identity"] == expected_identity, "Observation identity mismatch")
        if obs["evidence_kind"] in {"S", "N"}:
            pin(c["prompt_ref"])
    for row in selected.values():
        require(set(row["observation_ids"]) <= set(observations), "Missing observation mapping")
    calls = indexed(p["call_graph"], "call_id", "call_id kind parent_call_id attempt_id assertion_ids observation_ids depends_on producer reviewer review_path interaction managed_worker_required max_seconds", "call graph")
    for cid, call in calls.items():
        require(call["kind"] in {"native_worker", "static_review", "grader", "parent_return", "continuation", "control", "probe", "receiving"}, "Unknown call kind")
        require(type(call["max_seconds"]) is int and call["max_seconds"] > 0 and type(call["managed_worker_required"]) is bool, "Invalid call limits")
        require(call["interaction"] in {"single-turn", "awaiting-user"}, "Unknown interaction")
        text(call["producer"], "call producer")
        require(unique(call["assertion_ids"], "call assertions") <= set(catalog) and unique(call["observation_ids"], "call observations") <= set(observations), "Orphan call references")
        require(call["assertion_ids"] or call["observation_ids"], "Orphan call")
        require(unique(call["depends_on"], "call dependencies") <= set(calls), "Unknown call dependency")
        require((call["parent_call_id"] in calls) if call["kind"] == "continuation" else call["parent_call_id"] is None, "Invalid continuation parent")
    for graph, field in ((selected, "dependency_ids"), (observations, "prerequisite_observation_ids"), (calls, "depends_on")):
        done, active = set(), set()
        def visit(node):
            require(node not in active, "Cyclic dependency graph")
            if node not in done:
                active.add(node)
                for dep in graph[node][field]:
                    visit(dep)
                active.remove(node); done.add(node)
        for node in graph:
            visit(node)
    text(p["selection_reviewer"], "selection reviewer")
    require(any(c["kind"] == "static_review" and c["producer"] == p["selection_reviewer"] and set(tasks["T04"]["assertion_ids"]) <= set(c["assertion_ids"]) for c in calls.values()), "Missing charged independent T04 selection review")
    require(not any(c["kind"] == "native_worker" and c["producer"] == p["selection_reviewer"] for c in calls.values()), "Measured worker cannot review selection")
    native = any(selected[a]["selection"] == "REQUIRED" and "N" in catalog[a]["evidence_kinds"] for a in catalog)
    if native:
        require(isinstance(plan["runtime"], dict) and isinstance(plan["budget"], dict), "Selected native work needs runtime/budget")
        for key in ("max_attempts", "max_seconds", "repeats_per_case"):
            require(type(plan["budget"].get(key)) is int and plan["budget"][key] > 0, "Selected native budget incomplete")
    return p, catalog, selected, tasks, observations


def summarize_v2(plan_path, result_path, output_path):
    plan, record = load_json(plan_path), load_json(result_path)
    p, catalog, selected, tasks, observations = selection_plan(plan)
    exact(record, RESULT_KEYS, "v2 results")
    require(record["schema_version"] == "devforge.skill-validation-results/v2", "Mixed results version")
    run_id = text(plan["run_id"], "run id")
    require(record["run_id"] == run_id, "Run identity mismatch")
    plan_ref = {"path": str(plan_path), "sha256": digest(plan_path)}
    require(pin(record["plan"]) == plan_ref, "Result plan binding differs")
    root = Path(text(plan["candidate_root"], "candidate root"))
    require(root.is_absolute() and str(root.resolve()) == str(root) and root.is_dir() and not under(output_path, root), "Candidate/output boundary invalid")
    require(record["lineage"] == p["lineage"], "Results changed frozen lineage")
    if record["owner_acceptance_ref"] is not None:
        pin(record["owner_acceptance_ref"])
        require(record["owner_acceptance_ref"] in p["lineage"]["acceptance_chain"], "Results cannot manufacture successor owner acceptance")
    require(record["report_completion"] in {"COMPLETE", "PARTIAL", "BLOCKED"} and record["validation_disposition"] in {"ROUTINE_PASS", "FULL_PASS", "FAIL", "INSUFFICIENT_EVIDENCE"} and type(record["routine_adoption_eligible"]) is bool, "Unknown summary vocabulary")
    # Summaries are not evidence. Legacy display rows may accompany the assertion map.
    definitions = {}
    for check in rows(plan["checks"], "plan checks"):
        require(isinstance(check, dict), "Invalid check")
        cid = text(check.get("id"), "check id")
        require(cid not in definitions and cid in catalog, "Duplicate/orphan v2 check")
        require(set(check) <= set("id group expectation description requirement_ids case_id arm attempt_id exclusion_reason".split()) and {"id", "group", "expectation", "description"} <= set(check), "Unknown/missing check keys")
        require(check["expectation"] == selected[cid]["expectation"], "Check expectation differs from selected assertion")
        definitions[cid] = check
    check_ids = set()
    for row in rows(record["results"], "legacy result rows"):
        require(isinstance(row, dict) and set(row) in ({"check_id", "outcome", "reason", "evidence"}, {"check_id", "outcome", "reason", "evidence", "case_grade"}), "Unknown/missing check result keys")
        require(row["check_id"] in definitions and row["check_id"] not in check_ids and row["outcome"] in OUTCOMES, "Duplicate/orphan check result")
        check_ids.add(row["check_id"])
        text(row["reason"], "check reason")
    rows(record["findings"], "findings")
    task_results = indexed(record["task_results"], "task_id", "task_id classification selection disposition outcome reason evidence", "task results")
    require(tuple(task_results) == TASKS, "Missing ordered task results")
    for tid, row in task_results.items():
        require(row["classification"] == "Enforced" and row["selection"] == tasks[tid]["selection"], "Changed task selection")
        require(row["outcome"] in OUTCOMES and row["disposition"] in {"SATISFIED", "SATISFIED_BY_REVIEWED_SELECTION", "BLOCKED", "NOT_RUN"}, "Invalid task result")
        text(row["reason"], "task reason")
        refs = rows(row["evidence"], "task evidence")
        for ref in refs:
            pin(ref)
        if row["selection"] != "REQUIRED":
            expected = "NOT_RUN" if row["selection"] == "NOT_SELECTED" else "NOT_APPLICABLE"
            require(row["outcome"] == expected and row["disposition"] in {"SATISFIED_BY_REVIEWED_SELECTION", "BLOCKED", "NOT_RUN"}, "Selection is not an observation PASS")
        require(row["disposition"] != "SATISFIED" or bool(refs), "Satisfied task lacks obligation evidence")
    results = indexed(record["assertion_results"], "assertion_id", "assertion_id selection outcome integrity observation_refs grade_refs reason", "assertion results")
    require(set(results) == set(catalog), "Missing/extra assertion results")
    review_ref, review_status, review_reason = None, "NOT_RUN", "No independent T04 review supplied"
    if record["ai_review"] is not None:
        try:
            review_ref = pin(record["ai_review"])
            review = load_json(Path(review_ref["path"]))
            exact(review, set("schema_version run_id candidate_ref reviewer input_refs criteria disagreements additional_reviewer_refs overall plan selection_review".split()), "AI review")
            require(review["schema_version"] == "devforge.skill-ai-review/v2" and review["run_id"] == run_id and pin(review["plan"]) == plan_ref, "Review version/plan/run mismatch")
            require(review["candidate_ref"] == p["candidate_identity"]["candidate"], "Review candidate mismatch")
            exact(review["reviewer"], {"identity", "model", "runtime", "independence_evidence", "limits"}, "reviewer")
            require(review["reviewer"]["identity"] == p["selection_reviewer"], "Wrong selection reviewer")
            require(review["reviewer"]["identity"] != plan["assignment"].get("owner"), "Owner cannot self-review")
            text(review["reviewer"]["independence_evidence"], "review independence evidence")
            walk_pins(review)
            deliveries = [ref for ref in rows(review["input_refs"], "review inputs") if isinstance(ref, dict) and ref.get("kind") == "delivery"]
            require(len(deliveries) == 1, "T04 needs its exact pre-review delivery binding")
            delivery = load_json(Path(deliveries[0]["path"]))
            selection = {"version": "VPR-2", "policy_ref": p["policy_ref"], "acceptance_ref": p["acceptance_ref"], "plan": plan_ref}
            if delivery.get("schema_version") == "devforge.manual-review-context/v1":
                exact(delivery, {"schema_version", "validation_policy", "owner", "reviewer", "mode"}, "manual review context")
                require(delivery["mode"] == "manual" and delivery["owner"] == plan["assignment"].get("owner")
                        and delivery["reviewer"] == p["selection_reviewer"], "Manual review assignment mismatch")
            else:
                require(delivery.get("schema_version") == "devforge.utility-delivery/v2", "Unsupported review context")
            require(delivery.get("validation_policy") == selection, "T04 delivery selection mismatch")
            criteria = indexed(review["criteria"], "id", "id outcome reason evidence finding_ids applicability", "review criteria")
            require(set(criteria) == INVARIANTS, "R01-R10 inventory changed")
            sr = exact(review["selection_review"], set("outcome reason evidence reviewed_assertion_ids reviewed_rule_ids invariant_ids".split()), "selection review")
            require(unique(sr["invariant_ids"], "review invariants") == INVARIANTS and unique(sr["reviewed_assertion_ids"], "review assertions") == set(catalog), "Review omits catalog/invariants")
            required_rules = set(p["impact"]["matched_rules"]) | {f"CP-{i:02}" for i in range(1, 5)} | {rule for row in selected.values() for rule in row["rule_ids"]}
            require(unique(sr["reviewed_rule_ids"], "review rules") == required_rules, "Review omits selected rules")
            values = [sr, *criteria.values()]
            for item in values:
                require(item["outcome"] in OUTCOMES, "Unknown review outcome")
                text(item["reason"], "review reason")
                require(item["outcome"] not in {"PASS", "FAIL"} or bool(item["evidence"]), "Review lacks actual output")
            review_status = aggregate(item["outcome"] for item in values)
            require(review["overall"] in OUTCOMES and (review["overall"] != "PASS" or all(item["outcome"] == "PASS" for item in values)), "Review summary hides criterion outcome")
            review_status = aggregate([review_status, review["overall"]])
            review_reason = "Pinned independent review records retain all criterion judgments; independence truth requires external observation"
        except RecordError as exc:
            review_status, review_reason = "COULD_NOT_RUN", str(exc)
    structural_ref, freshness, fresh_reason = None, "NOT_RUN", "No source structural observation supplied"
    if record["structural_report"] is not None:
        try:
            structural_ref = pin(record["structural_report"])
            structural = load_json(Path(structural_ref["path"]))
            require(structural.get("schema_version") == "devforge.skill-structure/v1" and structural.get("mode") == "source" and structural.get("skill_root") == str(root), "Source structural record mismatch")
            manifest_current(root, structural.get("files_sha256"))
            freshness, fresh_reason = "PASS", "Source bytes match complete structural manifest"
        except RecordError as exc:
            freshness, fresh_reason = "COULD_NOT_RUN", str(exc)
    reduced, effective, observed = [], {}, {}
    for aid, row in results.items():
        definition, source = selected[aid], catalog[aid]
        require(row["selection"] == definition["selection"] and row["outcome"] in OUTCOMES, "Assertion selection/outcome mismatch")
        require(row["integrity"] in {"INTACT", "UNOBTAINABLE", "CONTAMINATED", "NOT_OBSERVED"}, "Unknown evidence integrity")
        reason = text(row["reason"], "assertion reason")
        rows(row["observation_refs"], "observation refs")
        rows(row["grade_refs"], "grade refs")
        value = row["outcome"]
        if row["selection"] == "NOT_SELECTED":
            require(value == "NOT_RUN" and row["integrity"] == "NOT_OBSERVED" and not row["observation_refs"] and not row["grade_refs"], "Unselected observation was invented")
        elif row["selection"] == "NOT_APPLICABLE":
            require(value == "NOT_APPLICABLE", "Scope exclusion outcome mismatch")
        elif value in {"PASS", "FAIL"}:
            try:
                require(row["integrity"] == "INTACT" and row["observation_refs"], "Observed result needs intact evidence")
                kinds, seen, raw_refs = set(), set(), []
                for ref in rows(row["observation_refs"], "assertion observations"):
                    pin(ref)
                    raw = load_json(Path(ref["path"]))
                    exact(raw, RUN_KEYS, "v2 observation")
                    require(raw.get("schema_version") == "devforge.skill-run/v2" and raw.get("run_id") == run_id and raw.get("validation_plan_ref") == plan_ref, "Observation version/plan/run mismatch")
                    oid = raw.get("observation_id")
                    require(oid in definition["observation_ids"] and oid not in seen, "Unexpected/duplicate observation")
                    seen.add(oid); frozen = observations[oid]
                    require(raw.get("conditions") == frozen["conditions"] and raw.get("evidence_kind") == frozen["evidence_kind"], "Observation conditions/kind differ")
                    require(raw.get("integrity") == "INTACT" and raw.get("selection") == "REQUIRED" and raw.get("assertion_ids") == frozen["assertion_ids"], "Observation integrity/assertions differ")
                    require(raw.get("outcome") in {"PASS", "FAIL"} and raw.get("raw_output_refs"), "Observation outcome/raw output absent")
                    require(raw["case_id"] == source["case_id"] and raw["arm"] == source["arm"] and raw["tier"] == definition["tier"] and raw["provider"] == "codex", "Observation case/arm/tier/provider mismatch")
                    require(all(dep in observed for dep in frozen["prerequisite_observation_ids"]), "Observation precedes required predecessor")
                    require(oid not in observed or observed[oid] == raw, "Shared observation bytes differ")
                    if frozen["reuse_ref"] is not None:
                        require(ref == frozen["reuse_ref"], "Reused observation differs from selected original")
                    walk_pins(raw)
                    kinds.add(raw["evidence_kind"])
                    raw_refs.extend(raw["raw_output_refs"])
                    if raw["evidence_kind"] == "N":
                        require(any(c["attempt_id"] == raw["attempt_id"] and oid in c["observation_ids"] for c in p["call_graph"]), "Native attempt not in selected graph")
                        for field in ("client_version", "model_configuration", "context_isolation", "execution_ref"):
                            text(raw[field], "native " + field)
                        pin({"path": raw["transcript"], "sha256": raw["transcript_sha256"]})
                        require(raw["boundary_refs"] and raw["installed_files_sha256"], "Native boundary/installed observation missing")
                        for field in ("authentication_observation_ref", "client_state_observation_ref", "process_ownership_ref", "effective_configuration_ref", "environment_setup_ref"):
                            pin(raw[field])
                        native = raw["native_observations"]
                        require(isinstance(native, dict) and native.get("terminal_completed") is True and native.get("terminal_status") == "PASS" and native.get("terminal_completion_refs"), "Native terminal incomplete")
                        # A declared record is not authenticated here; runtime must independently
                        # match its actual importer, producer, boundary and temporal observations.
                        for output_ref in raw["raw_output_refs"]:
                            try:
                                output_record = load_json(Path(output_ref["path"]))
                            except RecordError:
                                continue  # Transcripts are not necessarily JSON objects.
                            require(output_record.get("synthetic") is not True, "Synthetic output cannot supply native evidence")
                    observed[oid] = raw
                require(kinds >= set(source["evidence_kinds"]), "Required D/S/N evidence missing")
                if set(source["evidence_kinds"]) & {"S", "N"}:
                    require(row["grade_refs"], "Semantic assertion lacks independent judgment")
                for ref in rows(row["grade_refs"], "assertion grades"):
                    pin(ref); grade = load_json(Path(ref["path"]))
                    exact(grade, GRADE_KEYS, "v2 grade")
                    require(grade.get("schema_version") == "devforge.skill-case-grade/v2" and grade.get("run_id") == run_id and grade.get("case_id") == source["case_id"] and grade.get("arm") == source["arm"], "Grade identity/arm mismatch")
                    exact(grade["grader"], {"identity", "model", "independence_evidence"}, "grader")
                    allowed = {c["reviewer"] for c in p["call_graph"] if aid in c["assertion_ids"]} | {c["producer"] for c in p["call_graph"] if c["kind"] in {"grader", "static_review"} and aid in c["assertion_ids"]}
                    require(grade["grader"]["identity"] is not None and grade["grader"]["identity"] in allowed, "Independent grade producer mismatch")
                    require(not any(c["producer"] == grade["grader"]["identity"] and c["kind"] == "native_worker" for c in p["call_graph"]), "Measured worker cannot grade itself")
                    text(grade["grader"]["independence_evidence"], "grader independence")
                    require(grade["case_definition"] == source["source_ref"], "Grade changed original case")
                    walk_pins(grade)
                    judgments = indexed(grade.get("assertion_judgments"), "assertion_id", "assertion_id outcome reason evidence", "assertion judgments")
                    require(aid in judgments and judgments[aid]["outcome"] == value and judgments[aid]["evidence"], "Missing separate arm/assertion judgment")
                    require(all(ref in judgments[aid]["evidence"] for ref in raw_refs), "Grade omits complete raw output/arm")
                    require(grade.get("run_manifest") in row["observation_refs"], "Grade binds different observation")
                if definition["expectation"] == "observation":
                    value = "PASS"
            except RecordError as exc:
                value, reason = "COULD_NOT_RUN", str(exc)
        elif value == "NOT_APPLICABLE":
            value, reason = "COULD_NOT_RUN", "Required observation cannot become a post-hoc scope exclusion"
        effective[aid] = value
        reduced.append({"check_id": aid, "group": definition["tier"], "observed_outcome": row["outcome"], "effective_outcome": value, "cause": reason, "evidence": row["observation_refs"]})
    required = [effective[aid] for aid in catalog if selected[aid]["selection"] == "REQUIRED"]
    # Merely unattempted assertions remain NOT_RUN even if no usable structure exists yet.
    has_observation = any(row["outcome"] in {"PASS", "FAIL", "COULD_NOT_RUN"} for row in results.values() if row["selection"] == "REQUIRED")
    prerequisites = [review_status] + ([freshness] if has_observation else [])
    coverage = all(v in {"PASS", "FAIL"} for v in required) and review_status == "PASS" and freshness == "PASS"
    full_required = p["requested_claim"]["requires_full"] or bool(p["impact"]["full_triggers"]) or not p["impact"]["bounded"] or bool(set(p["impact"]["matched_rules"]) & {"CI-05", "CI-06", "CI-09"})
    policy_sufficient = not (p["mode"] == "Routine" and (full_required or p["accepted_scope_ref"] is None))
    policy_sufficient = policy_sufficient and all(c["disposition"] != "UNRESOLVED" for c in p["compatibility"])
    for cp in p["compatibility"]:
        if cp["disposition"] == "EVIDENCED":
            policy_sufficient = policy_sufficient and bool(cp["evidence"]) and all(effective.get(a) == "PASS" for a in cp["affected_assertions"])
            if cp["id"] == "CP-03":
                policy_sufficient = policy_sufficient and bool(cp["affected_assertions"]) and any("N" in catalog[a]["evidence_kinds"] and effective[a] == "PASS" for a in cp["affected_assertions"])
    transfer = exact(record["receiving_transfer"], set("selection outcome target_output receiver_contract receiver_observation completed_action observed_at_utc reason".split()), "receiving transfer")
    require(transfer["selection"] in SELECTIONS and transfer["outcome"] in OUTCOMES, "Unknown receiving disposition")
    text(transfer["reason"], "receiving reason")
    if transfer["selection"] == "NOT_SELECTED":
        require(transfer["outcome"] == "NOT_RUN" and all(transfer[k] is None for k in ("target_output", "receiver_contract", "receiver_observation", "completed_action", "observed_at_utc")), "Invented receiving observation")
    receiving_required = p["mode"] == "Full" and any(a["task_id"] == "T09" and a["selection"] == "REQUIRED" and "N" in catalog[aid]["evidence_kinds"] for aid, a in selected.items())
    if receiving_required:
        require(transfer["selection"] == "REQUIRED", "Full receiving cannot be replaced by a prepared handoff")
    if transfer["selection"] == "NOT_APPLICABLE":
        require(transfer["outcome"] == "NOT_APPLICABLE", "Receiving scope exclusion mismatch")
    if transfer["selection"] == "REQUIRED":
        transfer_outcome = transfer["outcome"]
        if transfer_outcome in {"PASS", "FAIL"}:
            try:
                for key in ("target_output", "receiver_contract", "receiver_observation", "completed_action"):
                    pin(transfer[key])
                stamp = datetime.fromisoformat(text(transfer["observed_at_utc"], "receiving UTC").replace("Z", "+00:00"))
                require(stamp.utcoffset() is not None and stamp.utcoffset().total_seconds() == 0, "Receiving time must be UTC")
                require(any(transfer["receiver_observation"] in row["raw_output_refs"] and row["evidence_kind"] == "N" and row["conditions"]["before_task"] <= "T09" for row in observed.values()), "Receiving lacks selected pre-T09 native observation")
            except (RecordError, ValueError) as exc:
                transfer_outcome = "COULD_NOT_RUN"
        elif transfer_outcome == "NOT_APPLICABLE":
            transfer_outcome = "COULD_NOT_RUN"
        required.append(transfer_outcome)
    overall = aggregate(required + prerequisites)
    if overall == "PASS" and not (coverage and policy_sufficient):
        overall = "COULD_NOT_RUN"
    disposition = "FAIL" if overall == "FAIL" else ("ROUTINE_PASS" if p["mode"] == "Routine" else "FULL_PASS") if overall == "PASS" else "INSUFFICIENT_EVIDENCE"
    coverage = coverage and all(v in {"PASS", "FAIL"} for v in required)
    groups = {tier: aggregate(results[aid]["outcome"] for aid in catalog if selected[aid]["tier"] == tier) for tier in ("D", "S", "C", "B", "A")}
    completion = "COMPLETE" if all(t["disposition"] in {"SATISFIED", "SATISFIED_BY_REVIEWED_SELECTION"} for t in task_results.values()) else "BLOCKED" if any(t["disposition"] == "BLOCKED" for t in task_results.values()) else "PARTIAL"
    return {"schema_version": "devforge.skill-validation-decision/v2", "run_id": run_id,
            "created_at_utc": datetime.now(timezone.utc).isoformat(), "plan": plan_ref,
            "results": {"path": str(result_path), "sha256": digest(result_path)}, "input_refs": plan["input_refs"],
            "candidate_root": str(root), "structural_report": structural_ref, "ai_review": review_ref,
            "ai_record_consistency": {"outcome": review_status, "reason": review_reason},
            "candidate_freshness": {"outcome": freshness, "reason": fresh_reason}, "groups": groups, "checks": reduced,
            "overall": overall, "coverage_complete": coverage, "disposition": "revise" if overall == "FAIL" else "suitable_for_stated_scope" if overall == "PASS" else "insufficient_evidence",
            "external_acceptance": "NOT_GRANTED", "limits": ["Advisory mechanical reduction of declared records; no protected receipt or owner decision.", "A matching native record is not authentication: collector origin, actual freshness/order, boundaries and receiving truth require independent protected runtime adjudication.", "Independent semantic adequacy and complete original projection require actual T04 review; hashes do not prove them."],
            "task_results": record["task_results"], "assertion_results": record["assertion_results"],
            "report_completion": completion, "validation_disposition": disposition,
            "routine_adoption_eligible": disposition == "ROUTINE_PASS" and policy_sufficient,
            "lineage": p["lineage"], "owner_acceptance_ref": record["owner_acceptance_ref"], "receiving_transfer": transfer}


def summarize(plan_path, result_path, output_path):
    plan, record = load_json(plan_path), load_json(result_path)
    version = plan.get("schema_version")
    if version == "devforge.skill-validation-plan/v1":
        exact(plan, PLAN_KEYS - {"validation_policy"}, "legacy v1 plan")
        exact(record, RESULT_KEYS - V2_ADDITIONS, "legacy v1 results")
        return summarize_v1(plan_path, result_path, output_path)
    if version == "devforge.skill-validation-plan/v2":
        return summarize_v2(plan_path, result_path, output_path)
    raise RecordError("Unsupported validation plan schema")


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
