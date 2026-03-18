# Phase 05: Reporting

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --workflow=qa --from=04 --to=05 --project-root=.
# Exit 0: proceed | Exit 1: Phase 04 incomplete
```

## Contract

PURPOSE: Determine QA result, generate report, update story file.
REQUIRED SUBAGENTS: qa-result-interpreter
REQUIRED ARTIFACTS: QA report file (deep mode), story file status update, gaps.json (if FAILED)
STEP COUNT: 4 mandatory steps

---

## Reference Loading

Load BEFORE executing steps:
```
Read(file_path=".claude/skills/spec-driven-qa/references/qa-result-formatting-guide.md")
Read(file_path=".claude/skills/spec-driven-qa/references/phase-3-reporting-workflow.md")
Read(file_path=".claude/skills/spec-driven-qa/references/story-update-workflow.md")
```

---

## Mandatory Steps

### Step 5.1: Result Determination

EXECUTE: Aggregate results from Phases 02-04. Apply ADR-010: coverage below thresholds = FAILED (not "PASS WITH WARNINGS").
```
# Collect all blocking conditions
blocking_conditions = []

# From Phase 02 (Validation)
IF business_coverage < 95%: blocking_conditions.append("Business coverage below 95%")
IF application_coverage < 85%: blocking_conditions.append("Application coverage below 85%")
IF overall_coverage < 80%: blocking_conditions.append("Overall coverage below 80%")
IF traceability_score < 100%: blocking_conditions.append("Traceability below 100%")

# From Phase 03 (Diff Regression)
IF phase_3_result == "BLOCKED": blocking_conditions.append("Diff regression CRITICAL/HIGH findings")
IF test_integrity_result == "CRITICAL": blocking_conditions.append("Test tampering detected")

# From Phase 04 (Analysis)
IF violations_critical > 0: blocking_conditions.append("CRITICAL anti-pattern violations")
IF violations_high > 0 (REGRESSION only): blocking_conditions.append("HIGH anti-pattern violations (regression)")
IF parallel_validators_below_threshold: blocking_conditions.append("Parallel validators below threshold")
IF invalid_deferrals: blocking_conditions.append("Invalid DoD deferrals")
IF MI < 50: blocking_conditions.append("Maintainability index below 50")
IF duplication > 20%: blocking_conditions.append("Code duplication above 20%")

# Determine overall result
IF len(blocking_conditions) > 0:
    overall_status = "FAILED"
    Display: "QA Result: FAILED"
    FOR each condition in blocking_conditions:
        Display: "  BLOCKING: {condition}"
ELIF violations_medium > 0 OR phase_3_result == "WARN":
    overall_status = "PASS WITH WARNINGS"
    Display: "QA Result: PASS WITH WARNINGS"
ELSE:
    overall_status = "PASSED"
    Display: "QA Result: PASSED"
```

VERIFY: overall_status is set to one of: PASSED, FAILED, PASS WITH WARNINGS. ADR-010 enforced (coverage below thresholds = FAILED, not warnings).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=05 --step=5.1 --project-root=.`

---

### Step 5.2: Report Generation (Deep Mode)

**If $MODE == "light":** Display "Report generation: SKIPPED (light mode)". Proceed to Step 5.3.

EXECUTE: Generate comprehensive QA report file.
```
Read(file_path=".claude/skills/spec-driven-qa/assets/templates/qa-report-template.md")

report_content = populate_template({
    story_id: ${STORY_ID},
    date: current_date,
    status: overall_status,
    coverage: {business, application, infrastructure, overall},
    traceability: traceability_score,
    violations: {critical, high, medium, low},
    diff_regression: phase_3_result,
    test_integrity: test_integrity_result,
    parallel_validators: {success_count, total, threshold},
    quality_metrics: {complexity, MI, duplication, doc_coverage},
    traceability_matrix: matrix_data,
    recommendations: generate_recommendations(findings),
    diagnosis: qa_report_data.get("diagnosis", null)
})

report_path = "devforgeai/qa/reports/${STORY_ID}-qa-report.md"
Write(file_path=report_path, content=report_content)
```

VERIFY: Report file exists on disk.
```
Glob(pattern="devforgeai/qa/reports/${STORY_ID}-qa-report.md")
IF not found: HALT -- "QA report file was NOT created."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=05 --step=5.2 --project-root=.`

---

### Step 5.3: Story Update

EXECUTE: Update story file status via Atomic Update Protocol (STORY-177). Create gaps.json if FAILED.

**If overall_status == "PASSED" or "PASS WITH WARNINGS":**
```
Edit(file_path="${STORY_FILE}",
     old_string="status: Dev Complete",
     new_string="status: QA Approved")

# Append workflow history entry
Edit(file_path="${STORY_FILE}",
     old_string="## Workflow History",
     new_string="## Workflow History\n- QA Approved: {current_date} (spec-driven-qa, mode: ${MODE})")

Display: "Story status updated to QA Approved"
```

**If overall_status == "FAILED":**
```
Edit(file_path="${STORY_FILE}",
     old_string="status: Dev Complete",
     new_string="status: QA Failed")

# Generate gaps.json for remediation (MANDATORY -- RCA-002)
gaps_content = {
    "story_id": "${STORY_ID}",
    "qa_result": "FAILED",
    "timestamp": current_date,
    "coverage_gaps": coverage_violations,
    "anti_pattern_violations": anti_pattern_violations,
    "deferral_issues": deferral_violations,
    "regression_findings": regression_findings,
    "diagnosis": qa_report_data.get("diagnosis", null),
    "remediation_sequence": generate_remediation_sequence(all_violations)
}

gaps_path = "devforgeai/qa/reports/${STORY_ID}-gaps.json"
Write(file_path=gaps_path, content=json.dumps(gaps_content, indent=2))

Display: "Story status updated to QA Failed"
Display: "Gaps file created: {gaps_path}"
Display: "Run /dev ${STORY_ID} --fix to remediate"
```

VERIFY: Story file status updated. If FAILED, gaps.json exists.
```
Grep(pattern="status: QA (Approved|Failed)", path="${STORY_FILE}", output_mode="content")
IF overall_status == "FAILED":
    Glob(pattern="devforgeai/qa/reports/${STORY_ID}-gaps.json")
    IF not found: HALT -- "CRITICAL: gaps.json missing for FAILED QA (RCA-002)"
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=05 --step=5.3 --project-root=.`

---

### Step 5.4: Format Display

EXECUTE: Invoke qa-result-interpreter subagent to format results for display.
```
Task(subagent_type="qa-result-interpreter",
     prompt="Format QA results for display.
     Story: ${STORY_ID}
     Mode: ${MODE}
     Result: {overall_status}
     Coverage: Business={biz}%, App={app}%, Infra={infra}%, Overall={overall}%
     Violations: {critical} CRITICAL, {high} HIGH, {medium} MEDIUM, {low} LOW
     Diff Regression: {phase_3_result}
     Test Integrity: {test_integrity_result}
     Parallel Validators: {success}/{total} (threshold: {threshold})
     Quality: Complexity={complexity}, MI={MI}%, Duplication={dup}%
     Next steps: {next_steps_based_on_result}")
```

VERIFY: qa-result-interpreter returned formatted display output.
```
IF Task result is empty or null:
    # Fallback: display raw summary (graceful degradation)
    Display: "QA Result: {overall_status} for ${STORY_ID}"
    Display: "  (qa-result-interpreter unavailable -- showing raw summary)"
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=05 --step=5.4 --subagent=qa-result-interpreter --project-root=.`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --workflow=qa --phase=05 --checkpoint-passed --project-root=.
# Exit 0: proceed to Phase 06 | Exit 1: HALT
```

## Phase 05 Completion Display

```
Phase 05 Complete: Reporting
  Result: {overall_status}
  Report: {report_path or "Not generated (light mode)"}
  Story status: Updated to {QA Approved or QA Failed}
  Gaps file: {gaps_path or "N/A (passed)"}
```
