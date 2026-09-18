"""Create validator records from already executed, frozen evidence."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RUN_ID = "20260916T140000Z-streaming-final"
TARGET = "advisor"


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def ref(path):
    path = Path(path)
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": digest(path)}


def write_json(name, value):
    (ROOT / name).write_text(
        json.dumps(value, ensure_ascii=True, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


manifest_ref = ref(ROOT / "source-manifest.json")
request_ref = ref(ROOT / "inputs/validation-request.json")
matrix_ref = ref(ROOT / "inputs/requirements-matrix.json")
amendment_ref = ref(ROOT / "inputs/requirements-matrix-amendment-001.json")

origin = {
    "schema_version": "1",
    "run_id": RUN_ID,
    "target_name": TARGET,
    "original_source_root": "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\advisor",
    "manifest": manifest_ref,
    "specification": request_ref,
    "origin_kind": "existing_spec",
    "history_kind": "observed",
    "prior_evidence": None,
    "completeness": "complete",
    "uncertainties": ["Historical origin before the first builder-managed edit remains unknown."],
    "source_readback_state": "UNCHANGED",
    "historical_origin": "unknown",
}
write_json("origin-record.json", origin)

sources = {
    "schema_version": "1",
    "run_id": RUN_ID,
    "target_name": TARGET,
    "sources": [
        {
            "source_id": "SRC-AUTHORING-REQUEST",
            "original_path": "docs/plan/skill-authorings/advisor/20260916T134000Z-streaming/validation-request.json",
            "retrieved_at_utc": "2026-09-16T13:59:00Z",
            "sha256": request_ref["sha256"],
            "snapshot_path": request_ref["path"],
            "sections": ["entire closed validation request"],
            "freshness": "byte-bound by authoring_intake.py",
        },
        {
            "source_id": "SRC-REQUIREMENTS",
            "original_path": "docs/plan/skill-validations/advisor/20260916T134000Z-streaming/requirements-matrix.json",
            "retrieved_at_utc": "2026-09-16T13:59:00Z",
            "sha256": matrix_ref["sha256"],
            "snapshot_path": matrix_ref["path"],
            "sections": ["requirements AS-01 through AS-15", "30-case denominator"],
            "freshness": "declared before final execution",
        },
        {
            "source_id": "SRC-REQUIREMENTS-AMENDMENT",
            "original_path": "docs/plan/skill-validations/advisor/20260916T134000Z-streaming/requirements-matrix-amendment-001.json",
            "retrieved_at_utc": "2026-09-16T13:59:00Z",
            "sha256": amendment_ref["sha256"],
            "snapshot_path": amendment_ref["path"],
            "sections": ["deadline/cleanup distinction", "PowerShell coverage denominator"],
            "freshness": "declared before final execution",
        },
    ],
}
write_json("sources.json", sources)

rule_source = {
    "path": matrix_ref["path"],
    "sha256": matrix_ref["sha256"],
    "source_id": "SRC-REQUIREMENTS",
    "locator": "requirements",
}
rules = []
for number in range(1, 16):
    rules.append({
        "rule_id": f"AS-{number:02}",
        "revision": "1+amendment-001",
        "title": f"Advisor streaming requirement AS-{number:02}",
        "source_refs": [rule_source],
        "authority_class": "user_selected_contract",
        "applicability": "applicable",
        "method": "independent deterministic/native observation",
        "expected_observation": "The mapped required cases match their independently declared expected behavior.",
        "required": True,
        "limitation": "No live Claude or installed-skill claim.",
    })
rules.extend([
    {"rule_id": "SV-STRUCTURE", "revision": "1", "title": "Skill structure and link integrity", "source_refs": [rule_source], "authority_class": "validator_rule", "applicability": "applicable", "method": "validator structure observer and installed checker", "expected_observation": "All emitted mandatory checks pass.", "required": True, "limitation": "Static structure does not prove behavior."},
    {"rule_id": "REPO-QUALITY", "revision": "2026-09-16", "title": "Required pass rate and executed-line coverage", "source_refs": [rule_source], "authority_class": "repository_policy", "applicability": "applicable", "method": "raw required-case and coverage counts", "expected_observation": "Each threshold is at least 95 percent.", "required": True, "limitation": "Branch coverage is separate."},
    {"rule_id": "SOURCE-PRESERVATION", "revision": "1", "title": "Frozen source preservation", "source_refs": [rule_source], "authority_class": "validator_rule", "applicability": "applicable", "method": "exact manifest readback", "expected_observation": "All 19 source files match the initial final snapshot.", "required": True, "limitation": "Readback is a point-in-time observation."},
])
write_json("rule-set.json", {"schema_version": "1", "run_id": RUN_ID, "target_name": TARGET, "rules": rules})

steps = [
    ("WF-01", "Prepare immutable request and complete briefing", "SKILL.md and references/briefing-rules.md", "request.json and briefing.md"),
    ("WF-02", "Preflight the selected native executable and child auth environment", "scripts/advisor_run.py", "preflight.json or blocked result"),
    ("WF-03", "Execute quiet v1 or streaming v2 reviewer process", "scripts/advisor_run.py and scripts/advisor_stream.py", "raw stdout/stderr and transport observations"),
    ("WF-04", "Validate terminal envelope and response contract", "scripts/advisor_run.py", "result.json and optional response.md"),
    ("WF-05", "Seal versioned attempt receipt", "scripts/advisor_run.py", "execution.json with bound digests"),
    ("WF-06", "Validate immutable prior history before a permitted follow-up", "scripts/advisor_run.py", "new attempt or blocked result"),
    ("WF-07", "Forward terminal operation through the thin Windows launcher", "scripts/advisor.ps1", "unchanged stdout/stderr and propagated exit code"),
]
workflow = {"schema_version": "1", "run_id": RUN_ID, "target_name": TARGET, "steps": []}
for step_id, action, executor, output in steps:
    workflow["steps"].append({
        "step_id": step_id,
        "entrypoint": action,
        "inputs": ["explicit selected paths and bounded options"],
        "executor": executor,
        "outputs": [output],
        "branches": ["quiet v1", "streaming v2", "explicit blocked/failure result"],
        "completion_evidence": "independent-cases-002.json and retained trial artifacts",
        "failure_recovery": "Preserve evidence; consume no implicit retry; use the same immutable request only when an authorized attempt remains.",
    })
write_json("workflow-map.json", workflow)

case_result = json.loads((ROOT / "independent-cases-002.json").read_text(encoding="utf-8"))
case_rule = {}
mapping = {
    "AS-01": (1, 2), "AS-02": (3, 4), "AS-03": (5, 6, 7), "AS-04": (8,),
    "AS-05": (9, 10), "AS-06": (11, 12, 13, 14), "AS-07": (15, 16),
    "AS-08": (17, 18), "AS-09": (19, 20), "AS-10": (21, 22),
    "AS-11": (23, 24, 25), "AS-12": (26,), "AS-13": (27, 28),
    "AS-14": (29,), "AS-15": (30,),
}
for rule_id, numbers in mapping.items():
    for number in numbers:
        case_rule[f"SV-SP-{number:03}"] = rule_id

checks = []
case_evidence = [ref(ROOT / "independent-cases-002.json")]
for case in case_result["cases"]:
    checks.append({
        "schema_version": "1", "run_id": RUN_ID, "check_id": case["id"],
        "rule_id": case_rule[case["id"]], "subject_path": "source/SKILL.md",
        "method": "independent black-box or native synthetic case", "required": True,
        "applicability": "applicable", "result": case["status"], "reason": case["reason"],
        "evidence": case_evidence, "dimension": "behavior",
    })

supplemental = [
    ("SUP-UNIT", "REPO-QUALITY", "source/tests/", "81/81 package unit and integration tests passed", "unit-tests.txt", "behavior"),
    ("SUP-EVAL", "REPO-QUALITY", "source/evals/cases.jsonl", "38/38 deterministic JSONL cases passed", "evaluation/summary.json", "behavior"),
    ("SUP-PY-COV", "REPO-QUALITY", "source/scripts/advisor_run.py", "604/635 executed Python lines, 95.1181 percent", "coverage/coverage.json", "behavior"),
    ("SUP-PS5-COV", "REPO-QUALITY", "source/scripts/advisor.ps1", "13/13 executable lines and 4/4 Pester cases under PowerShell 5.1", "coverage-independent/ps5.json", "behavior"),
    ("SUP-PS7-COV", "REPO-QUALITY", "source/scripts/advisor.ps1", "13/13 executable lines and 4/4 Pester cases under PowerShell 7", "coverage-independent/ps7.json", "behavior"),
    ("SUP-STRUCTURE", "SV-STRUCTURE", "source/SKILL.md", "All 14 emitted structure checks passed", "structure.json", "standards"),
    ("SUP-CHECKER", "SV-STRUCTURE", "source/SKILL.md", "Installed Skill Creator checker reported Skill is valid", "skill-creator-check.txt", "standards"),
    ("SUP-READBACK", "SOURCE-PRESERVATION", "source/SKILL.md", "Final exact readback matched 19 files and canonical package digest", "source-readback-final.json", "workflow"),
]
for check_id, rule_id, subject, reason, evidence_path, dimension in supplemental:
    checks.append({
        "schema_version": "1", "run_id": RUN_ID, "check_id": check_id,
        "rule_id": rule_id, "subject_path": subject, "method": "retained executed observation",
        "required": True, "applicability": "applicable", "result": "PASS", "reason": reason,
        "evidence": [ref(ROOT / evidence_path)], "dimension": dimension,
    })
with (ROOT / "checks.jsonl").open("w", encoding="utf-8", newline="\n") as stream:
    for check in checks:
        stream.write(json.dumps(check, ensure_ascii=True, separators=(",", ":"), allow_nan=False) + "\n")

write_json("findings.json", {"schema_version": "1", "run_id": RUN_ID, "target_name": TARGET, "findings": []})

report_ref = ref(ROOT / "validation-report.md")
findings_ref = ref(ROOT / "findings.json")
origin_ref = ref(ROOT / "origin-record.json")
write_json("handoff.json", {
    "schema_version": "1",
    "run_id": RUN_ID,
    "target_name": TARGET,
    "original_target_root": "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\advisor",
    "original_manifest": manifest_ref,
    "origin": origin_ref,
    "proposed_spec": None,
    "findings": findings_ref,
    "report": report_ref,
    "selected_finding_ids": [],
    "deferred_finding_ids": [],
    "proposal_review_state": "not_needed",
    "review_instruction": None,
    "builder_readiness": "NO_CHANGE",
    "readiness_reasons": ["All selected mandatory cases and executed-line thresholds passed; no source change is proposed."],
    "baseline_kind": None,
    "baseline_reference": None,
    "adoption_required": False,
    "adoption_capability": "not_applicable",
    "permitted_target_root": "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\advisor",
    "preservation_requirements": [
        "Preserve the exact 19-file package until a separately authorized change.",
        "Do not update the operational copy without explicit installation authorization.",
        "Do not treat this evidence as compiled-Rust framework acceptance.",
    ],
})

index_paths = [
    "source-manifest.json", "source-after-manifest.json", "source-readback-final.json",
    "inputs/validation-request.json", "inputs/requirements-matrix.json",
    "inputs/requirements-matrix-amendment-001.json", "authoring-intake.json",
    "independent-cases-001.json", "independent-cases-002.json", "independent-cases-003-coverage.json",
    "unit-tests.txt", "evaluation/summary.json", "evaluation/results.jsonl",
    "coverage/coverage.json", "coverage/coverage-report.txt", "coverage-independent/ps5.json",
    "coverage-independent/ps7.json", "coverage-independent/command-receipts.json",
    "structure.json", "skill-creator-check.txt", "validation-report.md", "command-log.md",
    "origin-record.json", "sources.json", "rule-set.json", "workflow-map.json",
    "checks.jsonl", "findings.json", "handoff.json", "enforcement-recommendations.md",
    "trials/records-audit-001.json",
]
write_json("evidence-index.json", {
    "schema_version": "advisor-streaming-validation-evidence-v1",
    "run_id": RUN_ID,
    "candidate_package_digest": "ce037407bfe1bb636b42dc468595a93b5837a2788837fc436c4bfc615f1d033f",
    "artifacts": [ref(ROOT / name) for name in index_paths],
})

print(json.dumps({"status": "COMPLETE", "checks": len(checks), "findings": 0}, ensure_ascii=True))
