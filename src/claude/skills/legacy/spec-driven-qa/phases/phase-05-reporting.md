# Phase 05: Reporting

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --workflow=qa --from=04 --to=05 --project-root=.
# Exit 0: proceed | Exit 1: Phase 04 incomplete
```

## Contract

| | |
|---|---|
| **PURPOSE** | Determine QA result, generate report, update story file. |
| **REQUIRED SUBAGENTS** | qa-result-interpreter |
| **REQUIRED ARTIFACTS** | QA report file (deep mode), story file status update, gaps.json (if FAILED), qa-recommendations.md (always), next-steps sidecar (conditional) |
| **STEP COUNT** | 5 mandatory steps + 2 sidecar steps (5.3b, 5.6) |

---

## Reference Loading

```
Read(file_path=".claude/skills/spec-driven-qa/references/qa-result-formatting-guide.md")
Read(file_path=".claude/skills/spec-driven-qa/references/phase-3-reporting-workflow.md")
Read(file_path=".claude/skills/spec-driven-qa/references/story-update-workflow.md")
```

---

## Mandatory Steps

### Step 5.1: Result Determination

**CLI Consolidation (OPT-004):** pure boolean logic; replaceable by:
```bash
devforgeai-validate result-determination --input-json='{"business_coverage": ${biz}, "application_coverage": ${app}, "infrastructure_coverage": ${infra}, "overall_coverage": ${overall}, "traceability_score": ${trace}, "phase_3_result": "${p3}", "test_integrity_result": "${ti}", "violations_critical": ${crit}, "violations_high_regression": ${high_reg}, "parallel_below_threshold": ${pbt}, "invalid_deferrals": ${idf}, "mi_below_50": ${mi50}, "duplication_above_20": ${dup20}, "violations_medium": ${med}}'
# Sprint 7 D7 (KI-014): Exit 0 = valid result (parse `overall_status` from JSON to
# distinguish PASSED / PASS WITH WARNINGS / FAILED). Exit 1 = CLI malformation.
# Prior (pre-Sprint-7): Exit 0=PASSED | 1=FAILED | 3=PASS_WITH_WARNINGS.
# JSON output: { "overall_status": str, "blocking_conditions": [...], "warning_conditions": [...] }
```
If CLI unavailable, fall back to the inline logic below.

EXECUTE: Aggregate Phases 02-04. ADR-010: coverage below thresholds = FAILED (NOT "PASS WITH WARNINGS").
```
blocking_conditions = []

# Phase 02 — Validation (thresholds from coverage-thresholds.md)
IF business_coverage      < 95%:  blocking_conditions.append("Business coverage below 95%")
IF application_coverage   < 85%:  blocking_conditions.append("Application coverage below 85%")
IF overall_coverage       < 80%:  blocking_conditions.append("Overall coverage below 80%")
IF traceability_score     < 100%: blocking_conditions.append("Traceability below 100%")

# Phase 03 — Diff Regression
IF phase_3_result == "BLOCKED":             blocking_conditions.append("Diff regression CRITICAL/HIGH findings")
IF test_integrity_result == "CRITICAL":     blocking_conditions.append("Test tampering detected")

# Phase 04 — Analysis
IF violations_critical > 0:                  blocking_conditions.append("CRITICAL anti-pattern violations")
IF violations_high > 0 (REGRESSION only):    blocking_conditions.append("HIGH anti-pattern violations (regression)")
IF parallel_validators_below_threshold:      blocking_conditions.append("Parallel validators below threshold")
IF invalid_deferrals:                        blocking_conditions.append("Invalid DoD deferrals")
IF MI < 50:                                  blocking_conditions.append("Maintainability index below 50")
IF duplication > 20%:                        blocking_conditions.append("Code duplication above 20%")

IF len(blocking_conditions) > 0:
    overall_status = "FAILED"
    Display "QA Result: FAILED"
    FOR each c in blocking_conditions: Display "  BLOCKING: {c}"
ELIF violations_medium > 0 OR phase_3_result == "WARN" OR len(qa_report_data.get("test_quality", {}).get("violations", [])) > 0:
    overall_status = "PASS WITH WARNINGS"
    Display "QA Result: PASS WITH WARNINGS"
    FOR each tq_v in qa_report_data.get("test_quality", {}).get("violations", []): Display "  WARNING: {tq_v}"
ELSE:
    overall_status = "PASSED"
    Display "QA Result: PASSED"
```

VERIFY: overall_status ∈ {PASSED, FAILED, PASS WITH WARNINGS}. ADR-010 enforced.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=05 --step=5.1 --project-root=.`

---

### Step 5.2: Report Generation (mode-dependent path)

Both light and deep mode emit a report, to DISTINCT paths so a deep (`/qa`) run never overwrites the dev-time (light, `/dev`) report (Issue #717). Set `report_path` from `$MODE`:
- **light** → `devforgeai/qa/reports/${STORY_ID}-qa-report.dev.md` — the dev-time report; overwritten on each `/dev` re-run.
- **deep** → `devforgeai/qa/reports/${STORY_ID}-qa-report.md` — the canonical report its downstream consumers read.

```
report_path = ("devforgeai/qa/reports/${STORY_ID}-qa-report.dev.md"
               if $MODE == "light"
               else "devforgeai/qa/reports/${STORY_ID}-qa-report.md")
```

EXECUTE: Generate comprehensive QA report file.
```
Read(file_path=".claude/skills/spec-driven-qa/assets/templates/qa-report-template.md")

report_content = populate_template({
    story_id: ${STORY_ID},
    date: current_date,
    status: overall_status,
    validation_mode: ${MODE},
    coverage: {business, application, infrastructure, overall},
    traceability: traceability_score,
    violations: {critical, high, medium, low},
    diff_regression: phase_3_result,
    test_integrity: test_integrity_result,
    parallel_validators: {success_count, total, threshold},
    quality_metrics: {complexity, MI, duplication, doc_coverage},
    test_quality: qa_report_data.get("test_quality", {}),
    traceability_matrix: matrix_data,
    recommendations: generate_recommendations(findings),
    diagnosis: qa_report_data.get("diagnosis", null)
})
```

**HALT Gate (AC#2 — qa-report.md Output Fidelity) — DEEP MODE ONLY.** This fidelity gate guards the authoritative deep report. The light `.dev.md` report is intermediate/informational and is NOT subject to this gate — running it in light mode would inject a new HALT into the `/dev` happy path (light mode runs the anti-pattern-scanner and tolerates HIGH findings; Issue #717). No hook enforces this on `qa-report.md` (the `pre-qa-output-fidelity.sh` hook scopes only to `*-gaps.json`). The check IS the enforcement — do not collapse to prose:
```
IF $MODE == "deep":
  FOR each critical_violation in findings.critical:
    IF missing ANY of: file, line, code_snippet, fix_code:
      HALT with: "HALT: QA output fidelity check failed: {missing_field} missing for CRITICAL violation in {file}. Phase {originating_phase} did not collect this data. Re-run Phase {originating_phase} with verbose output before proceeding."
      DO NOT call Write() for qa-report.md

  FOR each high_violation in findings.high:
    IF missing ANY of: file, line, issue, fix_description:
      HALT with: "HALT: QA output fidelity check failed: {missing_field} missing for HIGH violation in {file}. Phase {originating_phase} did not collect this data."
      DO NOT call Write() for qa-report.md

  FOR each prohibited_pattern in [file=="various files", line==null, remediation length < 10]:
    HALT with: "HALT: Prohibited pattern detected in entry[{index}]: '{field}' is '{value}'. Required: {replacement} (see qa-output-fidelity.md)."
    DO NOT call Write() for qa-report.md
```
IF all validations pass (or `$MODE == "light"`): proceed.

```
Write(file_path=report_path, content=report_content)
```

VERIFY: Report file exists.
```
Glob(pattern=report_path)
IF not found: HALT — "QA report file was NOT created."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=05 --step=5.2 --project-root=.`

---

### Step 5.3: Story Update

EXECUTE: Update story file status via Atomic Update Protocol (STORY-177). Create gaps.json if FAILED.

**If `overall_status ∈ {PASSED, PASS WITH WARNINGS}`:**
```
Edit(file_path="${STORY_FILE}", old_string="status: Dev Complete", new_string="status: QA Approved")
Edit(file_path="${STORY_FILE}", old_string="## Workflow History",
     new_string="## Workflow History\n- QA Approved: {current_date} (spec-driven-qa, mode: ${MODE})")
Display "Story status updated to QA Approved"
```

**If `overall_status == "FAILED"`:**
```
Edit(file_path="${STORY_FILE}", old_string="status: Dev Complete", new_string="status: QA Failed")

# Generate gaps.json for remediation (MANDATORY — RCA-002)
gaps_content = {
    "story_id": "${STORY_ID}",
    "qa_result": "FAILED",
    "timestamp": current_date,
    "coverage_gaps": coverage_violations,
    "anti_pattern_violations": anti_pattern_violations,
    "deferral_issues": deferral_violations,
    "regression_findings": regression_findings,
    "test_quality": qa_report_data.get("test_quality", null),
    "diagnosis": qa_report_data.get("diagnosis", null),
    "remediation_sequence": generate_remediation_sequence(all_violations)
}

# gaps.json Rule-16 fidelity is enforced by pre-qa-output-fidelity.sh PreToolUse[Write]
# (exit 2 on any entry missing required fields). Build every entry with its full
# required field set per `.claude/skills/spec-driven-qa/assets/schemas/gaps-schema.json`
# and `.claude/rules/workflow/qa-output-fidelity.md` so the Write is not rejected.

gaps_path = "devforgeai/qa/reports/${STORY_ID}-gaps.json"
Write(file_path=gaps_path, content=json.dumps(gaps_content, indent=2))

Display "Story status updated to QA Failed"
Display "Gaps file: {gaps_path}"
Display "Run /dev ${STORY_ID} --fix to remediate"
```

VERIFY: Story file status updated. If FAILED, gaps.json exists.
```
Grep(pattern="status: QA (Approved|Failed)", path="${STORY_FILE}", output_mode="content")
IF overall_status == "FAILED":
    Glob(pattern="devforgeai/qa/reports/${STORY_ID}-gaps.json")
    IF not found: HALT — "CRITICAL: gaps.json missing for FAILED QA (RCA-002)"
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=05 --step=5.3 --project-root=.`

---

### Step 5.3b: Append QA Cycle to Iteration Log (Non-Blocking)

EXECUTE: Record completed QA cycle. Non-blocking — if CLI fails, WARN and continue.
```bash
devforgeai-validate iteration-log-append-qa ${STORY_ID} \
  --outcome=${overall_status} \
  --mode=${MODE} \
  --blocking-issues=${blocking_conditions} \
  --coverage=${overall_coverage} \
  --gaps-ref=${gaps_path} \
  --project-root=.
```
VERIFY: If exit != 0, display "WARNING: Iteration log append-qa failed — continuing workflow."

**Spinning-Wheels Recommendation:** if CLI output contains a `spinning_wheels` field with medium/high confidence, display it:
```
IF spinning_wheels.confidence in ["medium", "high"]:
    Display "Spinning Wheels Recommendation: ${spinning_wheels.recommendation}"
    Display "  Confidence: ${spinning_wheels.confidence}"
```

RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=05 --step=5.3b --project-root=.`

---

### Step 5.4: Format Display

EXECUTE: Invoke qa-result-interpreter subagent to format results.
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
     Test Quality: Assertion ratio={assertion_ratio}, Unit%={unit_pct}%, Mocking ratio={mocks_per_test}
     Test Quality Warnings: {test_quality_violations_summary}
     Next steps: {next_steps_based_on_result}")
```

VERIFY: subagent returned formatted display output.
```
IF Task result is empty or null:
    # Fallback: raw summary (graceful degradation)
    Display "QA Result: {overall_status} for ${STORY_ID}"
    Display "  (qa-result-interpreter unavailable — showing raw summary)"
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=05 --step=5.4 --subagent=qa-result-interpreter --project-root=.`

---

### Step 5.4.5: Archive Prior qa-recommendations.md (Sprint 5)

**Purpose:** Move any existing workflow-scoped qa-recommendations file to its matching archive lane so the Sprint 2 generator's "refuse to overwrite" safeguard passes in Step 5.5.

**Applies when:** ALWAYS. CLI is a no-op (exit 0) if the file is absent.

**EXECUTE:**
```
QA_ARTIFACT_WORKFLOW = ("dev" if $MODE == "light" else "qa")
recommendations_path = ("devforgeai/qa/recommendations/${STORY_ID}-qa-recommendations.dev.md"
                        if QA_ARTIFACT_WORKFLOW == "dev"
                        else "devforgeai/qa/recommendations/${STORY_ID}-qa-recommendations.md")

devforgeai-validate archive-qa-recommendations \
    --story-id=${STORY_ID} \
    --workflow=${QA_ARTIFACT_WORKFLOW} \
    --project-root=${PROJECT_ROOT} \
    --format=json
```

**VERIFY:** Exit 0. Succeeds whether file was present (archived) or absent (no-op).
- Exit 1 with `"Archive target already exists"` → HALT. `archive/` already has a cycle-N archive for a prior failed run — inspect and resolve manually.
- Exit 2 → HALT with IO error verbatim.

IF `payload.archived == true`: Display `"Archived prior cycle ${payload.cycle} to ${payload.to}"`

RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=05 --step=5.4.5 --project-root=.`

---

### Step 5.5: Generate QA Recommendations Artifact

**Purpose:** Emit the workflow-scoped qa-recommendations artifact. Deep `/qa` keeps the canonical `devforgeai/qa/recommendations/${STORY_ID}-qa-recommendations.md` path for downstream `/dev` remediation; embedded light-QA writes `devforgeai/qa/recommendations/${STORY_ID}-qa-recommendations.dev.md` so it cannot overwrite or archive standalone `/qa` evidence. Complements `qa-report.md` (Step 5.2 — human prose) and `gaps.json` (Step 5.3 — FAILED-only CI). Covers ALL QA statuses including PASS_WITH_WARNINGS where `gaps.json` is deliberately absent.

**Applies when:** ALWAYS. File is emitted on every /qa completion regardless of `overall_status`. Zero findings → file still has empty Blocking/Advisory sections (`_None._`) plus a Cycle History entry (contract for Sprint 4 `/dev` preflight).

**Required inputs:** `${overall_status}` (Step 5.1), `${qa_report_data}` in-memory dict (Phases 02-04), `${STORY_ID}`, `${phase_start_timestamp}` (phase-init + Phase 02 start).

**EXECUTE:**

```
# 1. Bind workflow-scoped scratch/output paths.
QA_ARTIFACT_WORKFLOW = ("dev" if $MODE == "light" else "qa")
findings_input_path = f"tmp/${STORY_ID}/qa-report/findings-input.{QA_ARTIFACT_WORKFLOW}.json"
# light/dev -> tmp/${STORY_ID}/qa-report/findings-input.dev.json
# deep/qa   -> tmp/${STORY_ID}/qa-report/findings-input.qa.json
recommendations_path = ("devforgeai/qa/recommendations/${STORY_ID}-qa-recommendations.dev.md"
                        if QA_ARTIFACT_WORKFLOW == "dev"
                        else "devforgeai/qa/recommendations/${STORY_ID}-qa-recommendations.md")

# 2. Build findings_input JSON from qa_report_data. Per-finding enumeration rules:
#
#   Coverage gaps  → source_phase: "Phase-03-Coverage"; category: "coverage";
#                    severity from threshold comparison (biz<95% CRITICAL, app<85% HIGH, infra<80% MEDIUM)
#   Anti-pattern   → source_phase: "Phase-04-Code-Review"; category: "anti_pattern";
#                    classification from violation entry (REGRESSION | PRE_EXISTING)
#   Test quality   → source_phase: "Phase-02-Test-Quality"; category: "test_quality"
#   Spec compliance→ source_phase: "Phase-04-Code-Review"; category: "correctness" or "documentation"
#
#   Every finding MUST populate:
#     - verification.command  (deterministic shell command or pytest invocation)
#     - verification.expected (exact expected output)
#     - before_code + after_code (code changes) OR remediation_steps (non-code)
#     - estimated_effort_minutes (integer)
#     - provenance + derived_justification (if DERIVED) or inconclusive_reason (if INCONCLUSIVE)
#     - positive_control: true ONLY for audit-only invariant verifications (yaml.safe_load, etc.);
#       such findings are excluded from the recommendations output but remain in qa-report.md

findings_input = {
    "story_id": "${STORY_ID}",
    "qa_result": "${overall_status}",
    "cycle_number": 1,
    "generated_at": "<ISO8601 now()>",
    "phase_start_timestamp": "${phase_start_timestamp}",
    "findings": [<list built from qa_report_data per enumeration rules above>]
}

# 3. Write findings_input to project-scoped tmp (operational-safety.md Rule 2)
mkdir -p tmp/${STORY_ID}/qa-report
Write(file_path=findings_input_path,
      content=json.dumps(findings_input, indent=2))

# 4. Invoke generator CLI
cli_result = Bash("devforgeai-validate generate-qa-recommendations \
    --findings-file=${findings_input_path} \
    --output-file=${recommendations_path} \
    --project-root=. \
    --format=json 2>&1")

# 5. Dispatch on exit code
IF cli_result.exit_code == 0:
    Display "qa-recommendations.md generated: ${recommendations_path}"

ELIF cli_result.exit_code == 1:
    # Input schema / output validation failure. HALT — auto-retry out of scope for Sprint 2.
    parsed = json.loads(cli_result.stdout)
    Display "HALT: generate-qa-recommendations failed with {len(parsed.violations)} violations:"
    FOR v in parsed.violations:
        Display "  [{v.severity}] {v.category}: {v.description}"
        Display "    Remediation: {v.remediation}"
    HALT "Phase 05 Step 5.5 rejected findings-input. Fix upstream and re-run."

ELIF cli_result.exit_code == 2:
    Display "HALT: generate-qa-recommendations IO error:"
    Display cli_result.stdout
    HALT "Phase 05 Step 5.5 could not write output. Check template path and output directory."

ELIF cli_result.exit_code == 127:
    # CLI not installed. WARN and continue; downstream /dev --fix falls back to legacy gaps.json path.
    Display "WARNING: generate-qa-recommendations CLI not installed. Skipping qa-recommendations.md; /dev --fix will use legacy gaps.json path."

ELSE:
    HALT "generate-qa-recommendations unexpected exit code ${cli_result.exit_code}: ${cli_result.stdout}"
```

**VERIFY:**
```
IF cli_result.exit_code == 0:
    matches = Grep(pattern="^## Summary",
                   path=recommendations_path,
                   output_mode="count")
    IF matches != 1:
        HALT "Phase 05 Step 5.5 VERIFY failed: qa-recommendations.md missing '## Summary' header (got ${matches} matches)."

IF cli_result.exit_code == 127:
    pass  # CLI unavailable fallback — nothing to verify on disk
```

**RECORD:** `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=05 --step=5.5 --project-root=.`

---

### Step 5.6: Next-Steps Sidecar Persistence (cold-start handoff)

**Purpose:** Emit `devforgeai/qa/reports/${STORY_ID}-next-steps.md` containing a copy-pastable `/create-story --from-recommendations=...` command block. A user in a fresh Claude Code session (days later, context window exhausted) can `cat` the file and copy-paste the command to continue without re-running `/qa`.

**Applies when:** `overall_status ∈ {PASS_WITH_WARNINGS, FAILED}` AND `qa-recommendations-status.open_count > 0` AND at least one MEDIUM or LOW rec is open.

**Skip when:** `PASSED` (nothing to defer); `open_count == 0` (all recs closed); only Blocking recs open (use `/dev ${STORY_ID} --fix`, not a new story).

Template + substitution rules live authoritatively in `references/qa-result-formatting-guide.md` § "Next-Steps Emission Contract". The sidecar MUST be **byte-identical** to the inline Next-Steps block emitted by qa-result-interpreter in Step 5.4.

**EXECUTE:**
```
# RECORD below fires UNCONDITIONALLY (even on skip) — Step 5.6 is registry-required.
# Only the Write() side-effect is gated.
sidecar_emitted = false

status_result = Bash(
  command="devforgeai-validate qa-recommendations-status --story-id=${STORY_ID} --workflow=${QA_ARTIFACT_WORKFLOW} --project-root=. --format=json 2>&1"
)

IF status_result.exit_code != 0:
    Display "WARNING: Step 5.6 qa-recommendations-status failed; skipping sidecar."
    Skip to RECORD.

parsed = json.loads(status_result.stdout) if status_result.exit_code == 0 else null

IF parsed is null OR NOT parsed.exists OR parsed.open_count == 0:
    Display "Step 5.6: No recommendations to hand off — skipping sidecar."
    Skip to RECORD.

# Partition open rec IDs by severity (encoded in REC-ID initial: C/H/M/L)
medium_low_rec_ids = [r for r in parsed.open_rec_ids if severity_initial_of(r) in ("M", "L")]
blocking_count     = parsed.by_severity.get("CRITICAL", 0) + parsed.by_severity.get("HIGH", 0)

IF len(medium_low_rec_ids) == 0:
    Display "Step 5.6: Skipping sidecar (only Blocking recs open — use /dev ${STORY_ID} --fix)."
    Skip to RECORD.

medium_count = parsed.by_severity.get("MEDIUM", 0)
low_count    = parsed.by_severity.get("LOW", 0)
rec_id_csv   = ",".join(medium_low_rec_ids)

# Template per qa-result-formatting-guide.md — byte-identical to inline emission.
next_steps_content = f"""# QA Next Steps — {STORY_ID}

## Next Steps

To convert the {medium_count} MEDIUM + {low_count} LOW advisory recommendations into a follow-up story,
run ONE of the following in your current session OR a fresh session:

  # Variant 1 — Default (bundle MEDIUM + LOW, auto-filled --rec-ids):
  /create-story --from-recommendations={STORY_ID} --rec-ids={rec_id_csv}

  # Variant 2 — Interactive (skill prompts you to select):
  /create-story --from-recommendations={STORY_ID}

  # Variant 3 — Include Blocking (NOT RECOMMENDED; fix in-cycle via /dev {STORY_ID} --fix instead):
  /create-story --from-recommendations={STORY_ID} --include-blocking

See devforgeai/qa/reports/{STORY_ID}-next-steps.md for the persisted copy (safe to run from a new session).
"""

# Write idempotently — overwrites prior cycle's sidecar; reflects CURRENT cycle's open recs only.
Write(file_path="devforgeai/qa/reports/${STORY_ID}-next-steps.md", content=next_steps_content)
sidecar_emitted = true

Display "Step 5.6: Wrote devforgeai/qa/reports/${STORY_ID}-next-steps.md (${medium_count} MEDIUM + ${low_count} LOW recs)"
IF blocking_count > 0:
    Display "  Note: ${blocking_count} Blocking rec(s) also open — not bundled (use --include-blocking to override)."
```

**VERIFY:**
```
IF sidecar_emitted == true:
    Glob(pattern="devforgeai/qa/reports/${STORY_ID}-next-steps.md")
    IF not found: HALT "Step 5.6 VERIFY failed: sidecar file not written despite emission."
    Grep(pattern="^## Next Steps", path="...", output_mode="count")             MUST equal 1
    Grep(pattern="--from-recommendations=${STORY_ID}", path="...", output_mode="count") MUST equal 3   # three variants
```

**RECORD (unconditional — fires even on skip so phase-complete can verify):**
```bash
devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=05 --step=5.6 --project-root=.
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --workflow=qa --phase=05 --checkpoint-passed --project-root=.
# Exit 0: proceed to Phase 06 | Exit 1: HALT
```

## Phase 05 Completion Display

```
Phase 05 Complete: Reporting
  Result:              {overall_status}
  Report:              {report_path or "Not generated (light mode)"}
  Story status:        Updated to {QA Approved or QA Failed}
  Gaps file:           {gaps_path or "N/A (passed)"}
  Recommendations:     {qa-recommendations.md path or "N/A (CLI unavailable)"}
  Next-Steps sidecar:  {next-steps.md path or "N/A (all closed / only Blocking / passed)"}
```

## Hook-backed OUT-Attestation

This phase has Phase-D dispatch entries in `subagent_out_attestation_registry.json`. When dispatching those named subagents, instruct them to return a `subagent-result-v1` result that includes `coverage_attestation` in the normal response. Phase completion is blocked by `subagent-out-attestation-gate.sh` when the hook-owned ledger line lacks `coverage_attestation_present:true`. This Phase-D path is OUT-attestation-only and does not require `tmp/<WORK_ID>/handoffs/`.
