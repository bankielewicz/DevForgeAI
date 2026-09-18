# Phase 04: Analysis

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --workflow=qa --from=03 --to=04 --project-root=.
# Exit 0: proceed | Exit 1: Phase 03 incomplete
```

## Contract

| | |
|---|---|
| **PURPOSE** | Detect anti-patterns, run parallel validators, check spec compliance, measure code quality. |
| **REQUIRED SUBAGENTS** | anti-pattern-scanner (mandatory); test-automator/code-reviewer/security-auditor (adaptive per story type); deferral-validator (conditional); diagnostic-analyst (conditional) |
| **REQUIRED ARTIFACTS** | Anti-pattern violations, validator results, spec compliance matrix, quality metrics |
| **STEP COUNT** | 5 mandatory steps |

---

## Reference Loading

```
Read(file_path=".claude/skills/spec-driven-qa/references/anti-pattern-detection.md")
Read(file_path=".claude/skills/spec-driven-qa/references/parallel-validation.md")
Read(file_path=".claude/skills/spec-driven-qa/references/spec-compliance-validation.md")
Read(file_path=".claude/skills/spec-driven-qa/references/code-quality-workflow.md")
Read(file_path=".claude/skills/spec-driven-qa/references/automation-scripts.md")
Read(file_path=".claude/skills/spec-driven-qa/references/ui-design-validation.md")
```

---

## Mandatory Steps

### Step 4.1: Anti-Pattern Detection

EXECUTE: Build the registry-protected handoff for anti-pattern-scanner, then invoke the subagent across 6 violation categories.
```
changed_files = Bash(command="git diff --name-only main...HEAD 2>/dev/null || git diff --name-only HEAD~1")

QA_CHANGED_FILES_PHASE04_ANTI_PATTERN_SCANNER="tmp/${STORY_ID}/changed-files-phase04-anti-pattern-scanner.txt"
mkdir -p "$(dirname "${QA_CHANGED_FILES_PHASE04_ANTI_PATTERN_SCANNER}")"
: > "${QA_CHANGED_FILES_PHASE04_ANTI_PATTERN_SCANNER}"
HANDOFF_OUTPUT_ANTI_PATTERN_SCANNER=$(devforgeai-validate build-subagent-handoff ${STORY_ID} \
  --workflow=spec-driven-qa --phase=04 \
  --subagent=anti-pattern-scanner \
  --changed-files-file="${QA_CHANGED_FILES_PHASE04_ANTI_PATTERN_SCANNER}" \
  --project-root=.)
HANDOFF_PATH_ANTI_PATTERN_SCANNER=$(echo "$HANDOFF_OUTPUT_ANTI_PATTERN_SCANNER" | jq -r '.handoff_md_path')
VERIFY: "$HANDOFF_PATH_ANTI_PATTERN_SCANNER" is non-empty and exists.

Task(subagent_type="anti-pattern-scanner",
     prompt="Handoff: ${HANDOFF_PATH_ANTI_PATTERN_SCANNER}

     Read the handoff first. Use its context_pack.coverage_matrix for covered constitutional domains instead of re-reading full context files. If any required domain or artifact is missing, return H-CONTEXT-MISS and do not infer missing constraints. Embed subagent-result-v1 coverage_attestation with context_pack_consumed=true and context_miss=[] in the conviction worklog payload.
     Scan the following changed files for anti-pattern violations.
     Changed files: {changed_files}
     Return JSON with violations categorized by severity: critical, high, medium, low.
     Categories: tool usage, architecture, security, coding standards, dependency, structure.")
```

**Parse JSON Response:**
```
violations_critical = result["violations"]["critical"]
violations_high     = result["violations"]["high"]
violations_medium   = result["violations"]["medium"]
violations_low      = result["violations"]["low"]

blocks_qa = blocks_qa OR result["blocks_qa"]   # OR logic

Display: "Anti-patterns: {len(violations_critical)} CRITICAL, {len(violations_high)} HIGH, {len(violations_medium)} MEDIUM, {len(violations_low)} LOW"
```

**Regression vs Pre-existing Classification (STORY-175):**
```
FOR each violation:
    IF violation.file IN changed_files: violation.classification = "REGRESSION"     # Blocking
    ELSE:                                 violation.classification = "PRE_EXISTING"  # Warning only

Display: "Regressions: {regression_count} | Pre-existing: {preexisting_count}"
```

VERIFY: Scan completed. JSON parsed. Violations classified by severity AND REGRESSION/PRE_EXISTING.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=04 --step=4.1 --subagent=anti-pattern-scanner --project-root=.`

---

### Step 4.2: Parallel Validation (Deep Mode Only)

**If `$MODE == "light"`:** Skip. Display "Parallel validation: SKIPPED (light mode)". Proceed to Step 4.3.

EXECUTE: Invoke validators in parallel. Count + threshold depend on story type (STORY-183 adaptive, extracted in Phase 01 Step 1.7).

| Story Type | Validators | Threshold |
|-----------|-----------|-----------|
| feature/bugfix | test-automator, code-reviewer, security-auditor | 66% (2/3) |
| refactor       | code-reviewer, security-auditor                  | 50% (1/2) |
| documentation  | code-reviewer                                    | 100% (1/1) |

```
# Before dispatching code-reviewer or security-auditor, build their registry-protected handoffs.
QA_CHANGED_FILES_PHASE04_CODE_REVIEWER="tmp/${STORY_ID}/changed-files-phase04-code-reviewer.txt"
mkdir -p "$(dirname "${QA_CHANGED_FILES_PHASE04_CODE_REVIEWER}")"
: > "${QA_CHANGED_FILES_PHASE04_CODE_REVIEWER}"
HANDOFF_OUTPUT_CODE_REVIEWER=$(devforgeai-validate build-subagent-handoff ${STORY_ID} \
  --workflow=spec-driven-qa --phase=04 \
  --subagent=code-reviewer \
  --changed-files-file="${QA_CHANGED_FILES_PHASE04_CODE_REVIEWER}" \
  --project-root=.)
HANDOFF_PATH_CODE_REVIEWER=$(echo "$HANDOFF_OUTPUT_CODE_REVIEWER" | jq -r '.handoff_md_path')
VERIFY: "$HANDOFF_PATH_CODE_REVIEWER" is non-empty and exists before any code-reviewer dispatch.

QA_CHANGED_FILES_PHASE04_SECURITY_AUDITOR="tmp/${STORY_ID}/changed-files-phase04-security-auditor.txt"
mkdir -p "$(dirname "${QA_CHANGED_FILES_PHASE04_SECURITY_AUDITOR}")"
: > "${QA_CHANGED_FILES_PHASE04_SECURITY_AUDITOR}"
HANDOFF_OUTPUT_SECURITY_AUDITOR=$(devforgeai-validate build-subagent-handoff ${STORY_ID} \
  --workflow=spec-driven-qa --phase=04 \
  --subagent=security-auditor \
  --changed-files-file="${QA_CHANGED_FILES_PHASE04_SECURITY_AUDITOR}" \
  --project-root=.)
HANDOFF_PATH_SECURITY_AUDITOR=$(echo "$HANDOFF_OUTPUT_SECURITY_AUDITOR" | jq -r '.handoff_md_path')
VERIFY: "$HANDOFF_PATH_SECURITY_AUDITOR" is non-empty and exists before any security-auditor dispatch.

# Dispatch selected validators in a SINGLE message (parallel)
IF $STORY_TYPE in ["feature", "bugfix"]:
    Task(subagent_type="test-automator",   prompt="Coverage and quality analysis for ${STORY_ID}...")
    Task(subagent_type="code-reviewer",    prompt="Handoff: ${HANDOFF_PATH_CODE_REVIEWER}\n\nRead the handoff first. Use its context_pack.coverage_matrix for covered constitutional domains instead of re-reading full context files. If any required domain or artifact is missing, return H-CONTEXT-MISS and do not infer missing constraints. Embed subagent-result-v1 coverage_attestation with context_pack_consumed=true and context_miss=[] in the conviction worklog payload. Code quality review for ${STORY_ID}.")
    Task(subagent_type="security-auditor", prompt="Handoff: ${HANDOFF_PATH_SECURITY_AUDITOR}\n\nRead the handoff first. Use its context_pack.coverage_matrix for covered constitutional domains instead of re-reading full context files. If any required domain or artifact is missing, return H-CONTEXT-MISS and do not infer missing constraints. Embed subagent-result-v1 coverage_attestation with context_pack_consumed=true and context_miss=[] in the conviction worklog payload. Security vulnerability scan for ${STORY_ID}.")
    threshold = 2  # 2 of 3 must pass

ELIF $STORY_TYPE == "refactor":
    Task(subagent_type="code-reviewer",    prompt="Handoff: ${HANDOFF_PATH_CODE_REVIEWER}\n\nRead the handoff first. Use its context_pack.coverage_matrix for covered constitutional domains instead of re-reading full context files. If any required domain or artifact is missing, return H-CONTEXT-MISS and do not infer missing constraints. Embed subagent-result-v1 coverage_attestation with context_pack_consumed=true and context_miss=[] in the conviction worklog payload. Code quality review for ${STORY_ID}.")
    Task(subagent_type="security-auditor", prompt="Handoff: ${HANDOFF_PATH_SECURITY_AUDITOR}\n\nRead the handoff first. Use its context_pack.coverage_matrix for covered constitutional domains instead of re-reading full context files. If any required domain or artifact is missing, return H-CONTEXT-MISS and do not infer missing constraints. Embed subagent-result-v1 coverage_attestation with context_pack_consumed=true and context_miss=[] in the conviction worklog payload. Security vulnerability scan for ${STORY_ID}.")
    threshold = 1  # 1 of 2 must pass

ELIF $STORY_TYPE == "documentation":
    Task(subagent_type="code-reviewer",    prompt="Handoff: ${HANDOFF_PATH_CODE_REVIEWER}\n\nRead the handoff first. Use its context_pack.coverage_matrix for covered constitutional domains instead of re-reading full context files. If any required domain or artifact is missing, return H-CONTEXT-MISS and do not infer missing constraints. Embed subagent-result-v1 coverage_attestation with context_pack_consumed=true and context_miss=[] in the conviction worklog payload. Code quality review for ${STORY_ID}.")
    threshold = 1  # 1 of 1 must pass

success_count = sum(1 for r in results if r.passed)
IF success_count < threshold:
    blocks_qa = true
    Display "Parallel validators: {success_count}/{total} passed — BELOW threshold ({threshold})"
ELSE:
    Display "Parallel validators: {success_count}/{total} passed — threshold met ({threshold})"
```

VERIFY: All selected validators invoked + returned. success_count >= threshold OR blocks_qa set.
RECORD: per-subagent (one per validator dispatched):
`devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=04 --step=4.2 --subagent=<name> --project-root=.`
> # LOAD-BEARING (RCA-051 via STORY-658 G2): record each parallel validator individually so the audit-gate can verify all dispatched subagents ran. A single aggregate RECORD hides individual subagent failures.

---

### Step 4.3: Spec Compliance Validation

EXECUTE: Validate story documentation, ACs, deferred DoD items, API contracts, NFRs; generate traceability matrix.

**Sub-step 4.3.1: Validate Story Documentation**
```
Required sections: Implementation Notes, Definition of Done Status (or DoD items in Implementation Notes), Test Results, Acceptance Criteria Verification.

Grep(pattern="## Implementation Notes", path="${STORY_FILE}")
IF missing: violation (MEDIUM)
```

**Sub-step 4.3.2: Validate Acceptance Criteria**
```
FOR each AC:
    test_exists = Grep(pattern="test.*ac.*{ac_number}", path="tests/", -i=true)
    IF NOT test_exists: violation (HIGH)
    IF test.status != PASSED: violation (HIGH)
```

**Sub-step 4.3.3: Validate Deferrals** (MANDATORY if exist — RCA-007)
```
IF any DoD item unchecked:
    Read(file_path=".claude/skills/spec-driven-qa/references/dod-protocol.md")

    Task(subagent_type="deferral-validator",
         prompt="Validate all deferred DoD items for ${STORY_ID}.
         Check: user approval exists, story/ADR references provided, deferral justification adequate.
         Return: validation result per deferral item.")

    IF any deferral invalid:
        blocks_qa = true
        Display "Invalid deferrals detected — QA BLOCKED"

    # LOAD-BEARING (RCA-007 via STORY-658 G9): RECORD must stay INSIDE this conditional.
    # Moving it outside re-breaks deferral-validator multi-level chain enforcement — the
    # audit-gate keys on subagent records appearing only when the subagent was actually dispatched.
    RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=04 --step=4.3 --subagent=deferral-validator --project-root=.`
```

RECORD (unconditional — deferral-check outcome, fires whether or not deferrals existed): `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=04 --step=4.3.3 --project-root=.`

**Sub-step 4.3.4: Validate API Contracts**
```
FOR each endpoint in technical specification:
    Verify implementation matches spec (method, path, params, response)
```

**Sub-step 4.3.5: Validate NFRs**
```
Check performance, security, accessibility requirements from story
```

**Sub-step 4.3.6: Generate Traceability Matrix**
```
Matrix: Requirement → Test → Implementation
Store for Phase 05 report generation
```

VERIFY: All spec-compliance checks completed. Traceability matrix generated. Deferral-validator invoked iff deferrals exist (its RECORD lives inside Sub-step 4.3.3's conditional block per the load-bearing citation above).
RECORD (unconditional — fires whether or not deferrals existed): `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=04 --step=4.3 --project-root=.`

---

### Step 4.4: Code Quality Metrics

**If `$DELIVERABLE_TYPE == "non-code"`:**
```
Display: "Code quality: N/A (non-code implementation)"
Display: "  Cyclomatic complexity: N/A"
Display: "  Maintainability index: N/A"
Display: "  Code duplication: N/A"
Display: "  Documentation coverage: Checking..."
# Documentation coverage still applies — verify deliverable files are well-documented
```
Skip to VERIFY.

**If `$DELIVERABLE_TYPE == "code" or "mixed":`**

EXECUTE: Cyclomatic complexity, maintainability index, code duplication, documentation coverage.

**Sub-step 4.4.1: Cyclomatic Complexity** (threshold: >10 = MEDIUM. Uses `analyze_complexity.py` — radon + lizard fallback, multi-language.)
```
Bash(command="PYTHONIOENCODING=utf-8 python src/claude/skills/spec-driven-qa/scripts/analyze_complexity.py src/ 2>&1")
```

**Sub-step 4.4.2: Maintainability Index** (MI < 70: MEDIUM. MI < 50: HIGH — blocks QA.)
```
Bash(command="source .venv/bin/activate && radon mi src/ -s 2>/dev/null || echo 'radon not available'")
```

**Sub-step 4.4.3: Code Duplication** (>5% MEDIUM, >20% HIGH — blocks. Uses `detect_duplicates.py` — self-contained.)
```
Bash(command="PYTHONIOENCODING=utf-8 python src/claude/skills/spec-driven-qa/scripts/detect_duplicates.py src/ 2>&1")
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=04 --step=4.4.3 --project-root=.`
> # LOAD-BEARING (STORY-658 Option C sub-step tracking): per-sub-step records prove each metric was actually computed. Without them, a silent skip of duplication detection is undetectable at audit-gate.

**Sub-step 4.4.4: Documentation Coverage** (target 80%; count documented vs undocumented public APIs)
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=04 --step=4.4.4 --project-root=.`
> # LOAD-BEARING (STORY-658 Option C).

**Sub-step 4.4.5: Dependency Coupling** (detect circular dependencies, high coupling > 10 deps/file)
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=04 --step=4.4.5 --project-root=.`
> # LOAD-BEARING (STORY-658 Option C).

VERIFY: Quality metrics collected. Violations recorded for threshold breaches.
```
IF MI < 50:          blocks_qa = true   (HIGH violation)
IF duplication > 20%: blocks_qa = true   (HIGH violation)
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=04 --step=4.4 --project-root=.`

---

### Step 4.5.5: Dead Code Detection (Advisory)

EXECUTE: Invoke dead-code-detector subagent to identify unused functions in changed files. Per ADR-016 this is read-only and advisory — findings DO NOT block QA approval (no `blocks_qa` trigger). High-confidence findings (>=0.5) surface in the QA report as MEDIUM-severity recommendations for review.
```
# changed_files reused from Step 4.1 anti-pattern-scanner

Task(subagent_type="dead-code-detector",
     prompt="Find unused functions in the following changed files using call-graph analysis.
     Changed files: {changed_files}
     Apply entry-point exclusions per the subagent's documented patterns (main(), test_*, @route, @pytest.fixture, @click.command, dunder methods, etc.).
     Return JSON with findings[]: smell_type, function_name, file, line, callers_count, confidence, evidence, remediation.
     Use treelint deps --calls for AST-aware analysis; fall back to Grep for unsupported languages (C#, Java, Go, Ruby).")
```

VERIFY: Subagent returns JSON. Filter `findings` to `confidence >= 0.5` (suppress dynamic-dispatch uncertainty per ADR-016 read-only contract).

RECORD: Append filtered findings to QA report under "Advisory Findings — Dead Code". NEVER blocking; review-only signals. Do NOT escalate to Step 4.5 diagnostic-analyst trigger (`blocks_qa` untouched by this step).
```
devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=04 --step=4.5.5 --project-root=.
```

---

### Step 4.5: Diagnostic Hook on Failures (STORY-496)

EXECUTE: If coverage-analyzer or anti-pattern-scanner reported failures, invoke diagnostic-analyst for root cause diagnosis.
```
IF blocks_qa == true OR violations_critical > 0:
    Task(subagent_type="diagnostic-analyst",
         prompt="Diagnose root cause of QA failures for ${STORY_ID}.
         Failures: {failure_summary}
         Provide diagnosis and recommended fix sequence.")

    IF Task result available:
        qa_report_data["diagnosis"] = result
        Display "Diagnostic analysis: Completed — diagnosis attached to report"
    ELSE:
        # Actionable guidance instead of null (S-003 optimization)
        qa_report_data["diagnosis"] = {
            "status": "UNAVAILABLE",
            "reason": "diagnostic-analyst subagent unavailable",
            "action": "Run /rca ${STORY_ID} manually for root cause analysis"
        }
        Display "Diagnostic analysis: UNAVAILABLE (actionable fallback recorded)"

    # LOAD-BEARING (RCA-051 via STORY-658 G2): subagent RECORD lives INSIDE the
    # conditional — only fires when diagnostic-analyst was actually dispatched.
    RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=04 --step=4.5 --subagent=diagnostic-analyst --project-root=.`
ELSE:
    Display "Diagnostic analysis: SKIPPED (no failures to diagnose)"
```

VERIFY: Diagnostic hook invoked if failures present. Result attached (or graceful degradation logged).
RECORD (unconditional — always records step 4.5 completion): `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=04 --step=4.5 --project-root=.`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --workflow=qa --phase=04 --checkpoint-passed --project-root=.
# Exit 0: proceed to Phase 05 | Exit 1: HALT
```

## Phase 04 Completion Display

```
Phase 04 Complete: Analysis
  Anti-patterns:        {critical} CRITICAL, {high} HIGH, {medium} MEDIUM  (Regressions: {reg_count} | Pre-existing: {pre_count})
  Parallel validators:  {success}/{total} passed (threshold: {threshold})  [adaptive: {$STORY_TYPE}]
  Spec compliance:      {passed}/{total} criteria validated
  Quality:              Complexity avg {X}, MI {X}%, Duplication {X}%      [or N/A for non-code]
  Diagnostic:           {status}
```

## Hook-backed OUT-Attestation

This phase has Phase-D dispatch entries in `subagent_out_attestation_registry.json`. When dispatching those named subagents, instruct them to return a `subagent-result-v1` result that includes `coverage_attestation` in the normal response. Phase completion is blocked by `subagent-out-attestation-gate.sh` when the hook-owned ledger line lacks `coverage_attestation_present:true`. This Phase-D path is OUT-attestation-only and does not require `tmp/<WORK_ID>/handoffs/`.
