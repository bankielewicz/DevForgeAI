---
name: devforgeai-qa
description: Validates code quality through hybrid progressive validation (light checks during development, deep analysis after completion). Enforces test coverage (95%/85%/80% strict thresholds), detects anti-patterns, validates spec compliance, and analyzes code quality metrics. Use when validating implementations, ensuring quality standards, or preparing for release.
tools: AskUserQuestion, Read, Write, Edit, Glob, Grep, Bash, Task
model: claude-opus-4-6
---

# DevForgeAI QA Skill

Quality validation enforcing architectural constraints, coverage thresholds, and code standards through progressive validation.

Do not skip any phases in the devforgeai-qa skill.

---

## EXECUTION MODEL: This Skill Expands Inline

**After invocation, YOU (Claude) execute these instructions phase by phase.**

**When you invoke this skill:**
1. This SKILL.md content is now in your conversation
2. You execute each phase sequentially
3. You display results as you work through phases
4. You complete with success/failure report

**Do NOT:**
- Wait passively for skill to "return results"
- Assume skill is executing elsewhere
- Stop workflow after invocation

**Proceed to "Parameter Extraction" section below and begin execution.**

---

## Parameter Extraction

Extracts story ID and mode (light/deep) from conversation context.

**See `references/parameter-extraction.md`** for extraction algorithm (YAML frontmatter, file reference, explicit statement, status inference).
    Read(file_path=".claude/skills/devforgeai-qa/references/parameter-extraction.md")

---

## CRITICAL: Definition of Done Protocol

**Deferral Validation CANNOT be skipped.**

Deferred DoD items MUST have user approval, story/ADR references, and deferral-validator subagent validation.

**PROHIBITED:** Autonomous deferrals, manual validation shortcuts, token optimization bypasses.

**Rationale:** RCA-007 - Manual validation missed STORY-004→005→006 chain, causing work loss.

**See `references/dod-protocol.md`** for protocol requirements and enforcement.
    Read(file_path=".claude/skills/devforgeai-qa/references/dod-protocol.md")

---

## Validation Modes

### Light (~10K tokens, 2-3 min)
- Build/syntax checks
- Test execution (100% pass required)
- Critical anti-patterns only
- Deferral validation (if deferrals exist)

### Deep (~35K tokens, 8-12 min)
- Complete coverage analysis (95%/85%/80% thresholds)
- Comprehensive anti-pattern detection
- Full spec compliance (AC, API, NFRs)
- Code quality metrics
- Security scanning (OWASP Top 10)
- Deferral validation (if deferrals exist)

---

## QA Workflow (5 Phases)

**EXECUTION STARTS HERE - You are now executing the skill's workflow.**

**Progressive Disclosure:** Workflow references are loaded when each phase executes (not before) to optimize token usage.

**IMPORTANT:** "On-demand" means "load when phase starts" - NOT "loading is optional."

**Execution Pattern:**
1. Reach phase (e.g., Phase 2: Analysis)
2. See "⚠️ CHECKPOINT" marker
3. Load reference file (REQUIRED)
4. Execute ALL steps from reference file
5. Complete phase marker write
6. Proceed to next phase

**IF you skip loading a reference:** You will execute the phase incorrectly and miss mandatory steps.

---

## Phase 0: Setup

**Purpose:** Initialize QA environment - validate CWD, create test isolation, acquire locks.

**Create execution tracker at Phase 0 start:**

```
TodoWrite({
  todos: [
    { content: "Phase 0: Setup", status: "in_progress", activeForm: "Running Phase 0: Setup" },
    { content: "Phase 1: Validation", status: "pending", activeForm: "Running Phase 1: Validation" },
    { content: "Phase 2: Analysis", status: "pending", activeForm: "Running Phase 2: Analysis" },
    { content: "Phase 3: Reporting", status: "pending", activeForm: "Running Phase 3: Reporting" },
    { content: "Phase 4: Cleanup", status: "pending", activeForm: "Running Phase 4: Cleanup" }
  ]
})
```

### Phase 0 Detailed Steps

**Reference:** `references/phase-0-setup-workflow.md`
    Read(file_path=".claude/skills/devforgeai-qa/references/phase-0-setup-workflow.md")

Steps 0.0-0.6: Session checkpoint detection, CWD validation, test isolation config, story-scoped directories, lock acquisition, deep mode workflow loading, story type extraction for adaptive validation.

**Phase 0 Completion Checklist:**
- [ ] CWD validated
- [ ] Test isolation config loaded
- [ ] Story directories created
- [ ] Lock acquired (if enabled)
- [ ] Deep workflow loaded (if deep mode)
- [ ] Story type extracted for adaptive validation

**Display:**
```
✓ Phase 0 Complete: Setup
  Project root: ✓ Validated
  Test isolation: ✓ Configured
  Lock: ✓ Acquired
  Mode: [light/deep]
```

### Phase 0 CLI Gate (STORY-517)

```
# Initialize QA phase state (first call in Phase 0)
devforgeai-validate phase-init {STORY_ID} --workflow=qa --project-root=.

# Complete Phase 0 gate
devforgeai-validate phase-complete {STORY_ID} --workflow=qa --phase=00 --checkpoint-passed --project-root=.

Display: "✓ Phase 0 CLI gate passed"
Display: "Phase 0 ✓ | Setup | Lock acquired"
```

**Update execution tracker:**

```
TodoWrite({
  todos: [
    { content: "Phase 0: Setup", status: "completed", activeForm: "Phase 0 complete" },
    { content: "Phase 1: Validation", status: "in_progress", activeForm: "Running Phase 1: Validation" },
    { content: "Phase 2: Analysis", status: "pending", activeForm: "Running Phase 2: Analysis" },
    { content: "Phase 3: Reporting", status: "pending", activeForm: "Running Phase 3: Reporting" },
    { content: "Phase 4: Cleanup", status: "pending", activeForm: "Running Phase 4: Cleanup" }
  ]
})
```

### Phase 0 Completion Enforcement

**Verify deep-validation-workflow.md was loaded (deep mode only):**

```
IF mode == "deep":
    IF "deep-validation-workflow.md" NOT loaded in conversation:
        Display: "❌ CRITICAL ERROR: Phase 0 Step 0.5 incomplete"
        Display: "   Deep validation workflow reference file was not loaded"
        Display: "   Load file: .claude/skills/devforgeai-qa/references/deep-validation-workflow.md"
        HALT: "Cannot proceed to Phase 1 without deep workflow reference"
        Instruction: "Load the reference file manually, then resume /qa {STORY_ID} deep"
    ELSE:
        Display: "✓ Deep mode workflow reference verified loaded"
```

This enforcement prevents Phase 1-3 from executing without complete initialization.

---
## Phase Marker Protocol [STORY-126 Enhancement]

**Reference:** `references/phase-marker-protocol.md`
    Read(file_path=".claude/skills/devforgeai-qa/references/phase-marker-protocol.md")

CLI gates enforce phase completion via devforgeai-validate --workflow=qa. Pre-flight verification at start of Phases 1-4.

---

---

## Phase 1: Validation

### Pre-Flight: Verify Phase 0 Complete

```
devforgeai-validate phase-status {STORY_ID} --workflow=qa --project-root=.
# Verify phase 00 is completed in qa-phase-state.json

IF phase 00 NOT completed:
    CRITICAL ERROR: "Phase 0 not verified complete"
    HALT: "Phase 1 cannot execute without Phase 0 completion"
    Display: "Previous phase (Phase 0) must complete successfully before starting Phase 1"
    Instruction: "Start workflow from Phase 0. Run setup first."
    Exit: Code 1 (phase sequencing violation)

Display: "✓ Phase 0 verified complete - Phase 1 preconditions met"
```

### ⚠️ CHECKPOINT: Phase 1 Reference Loading [MANDATORY]

**You MUST execute ALL steps before proceeding to phase content.**

**Step 1.0: Load Workflow Reference (REQUIRED)**
```
Read(file_path=".claude/skills/devforgeai-qa/references/traceability-validation-algorithm.md")
```

**This reference contains the complete workflow. Execute ALL steps from the reference file.**

**After loading:** Proceed to Step 1.1 (in reference file)

**IF you skip this step:** You will execute the phase incorrectly and miss mandatory steps.

---

**Purpose:** Execute tests, analyze coverage, validate traceability.

### Step 1.1: AC-DoD Traceability Validation

**Reference:** `references/traceability-validation-algorithm.md`
**Templates:** `assets/traceability-report-template.md`
    Read(file_path=".claude/skills/devforgeai-qa/references/traceability-validation-algorithm.md")
    Read(file_path=".claude/skills/devforgeai-qa/assets/traceability-report-template.md")

```
# Extract AC Requirements
ac_headers = grep count "^### AC#[0-9]+" story_file
FOR each AC section:
    Extract: Then/And clauses, bullet requirements, metrics
    Store: ac_requirements[]

# Extract DoD Items
dod_section = extract_between("^## Definition of Done", "^## Workflow")
FOR each subsection in [Implementation, Quality, Testing, Documentation]:
    Parse: checkbox lines
    Store: dod_items[]

# Map AC → DoD
FOR each ac_req in ac_requirements:
    best_match = find_best_dod_match(ac_keywords, dod_items)
    IF match_score >= 0.5:
        traceability_map[ac_req] = best_match
    ELSE:
        missing_traceability.append(ac_req)

# Calculate Score
traceability_score = ((total - missing.length) / total) × 100

IF traceability_score < 100:
    Display: "QA WORKFLOW HALTED - Fix traceability issues"
    EXIT
```

### Step 1.2: Test Coverage Analysis

**Reference:** `references/coverage-analysis-workflow.md`
**Guide:** `references/coverage-analysis.md`
    Read(file_path=".claude/skills/devforgeai-qa/references/coverage-analysis-workflow.md")
    Read(file_path=".claude/skills/devforgeai-qa/references/coverage-analysis.md")

Execute the 7-step coverage workflow:
1. Load coverage thresholds (95%/85%/80%)
2. Generate coverage reports (language-specific command)
3. Classify files by layer (Business Logic, Application, Infrastructure)
4. Calculate coverage percentage for each layer
5. Validate against thresholds
6. Identify coverage gaps with test suggestions
7. Analyze test quality (assertions, mocking, pyramid)

**Blocks on:** Business <95%, Application <85%, Overall <80%

**Display:**
```
✓ Phase 1 Complete: Validation
  Traceability: {traceability_score}%
  Business Logic: [X]% (threshold: 95%)
  Application: [X]% (threshold: 85%)
  Infrastructure: [X]% (threshold: 80%)
  Overall: [X]%
```

### Phase 1 Completion Checklist

**Before writing Phase 1 marker, verify you have:**

- [ ] Loaded traceability-validation-algorithm.md (Step 1.0)
- [ ] Validated AC-DoD traceability (Step 1.1)
- [ ] Executed test runner (Step 1.2)
- [ ] Analyzed coverage results (Step 1.3)
- [ ] Verified critical threshold (100% pass required)
- [ ] Displayed Phase 1 completion summary

**IF any checkbox unchecked:** HALT and complete missing steps before Phase 2.

**Display to user:**
```
✓ Phase 1 Complete: Validation | {traceability_score}% traceability
```

### Phase 1 CLI Gate (STORY-517)

```
devforgeai-validate phase-complete {STORY_ID} --workflow=qa --phase=01 --checkpoint-passed --project-root=.

Display: "✓ Phase 1 CLI gate passed"
Display: "Phase 1 ✓ | Validation | {traceability_score}% traceability"
```

**Update execution tracker:**

```
TodoWrite({
  todos: [
    { content: "Phase 0: Setup", status: "completed", activeForm: "Phase 0 complete" },
    { content: "Phase 1: Validation", status: "completed", activeForm: "Phase 1 complete" },
    { content: "Phase 2: Analysis", status: "in_progress", activeForm: "Running Phase 2: Analysis" },
    { content: "Phase 3: Reporting", status: "pending", activeForm: "Running Phase 3: Reporting" },
    { content: "Phase 4: Cleanup", status: "pending", activeForm: "Running Phase 4: Cleanup" }
  ]
})
```

---

## Phase 1.5: Diff Regression Detection

### Pre-Flight: Verify Phase 1 Complete

Phase 1 marker must exist before diff regression analysis begins.

### Purpose

Analyze `git diff main...HEAD` to detect production code regressions before deep analysis. Scans only non-test production files — excludes test files to skip test-only changes from regression scanning.

### ⚠️ CHECKPOINT: Load Reference (REQUIRED)

```
Read(file_path=".claude/skills/devforgeai-qa/references/diff-regression-detection.md")
```

### Step 1.5.1: Execute Git Diff

Execute `git diff main...HEAD` (or `HEAD~1`) and parse unified diff output into structured hunks.

### Step 1.5.2: Apply File Exclusion Patterns

Exclude test files from production regression scan: `**/tests/**`, `**/*.test.*`, `**/*.spec.*`, `test_*.py`, `*_test.py`

### Step 1.5.3: Scan for Diff Regressions

Scan remaining production file diffs using detection patterns from reference file (function deletion, error handler removal, signature changes, simplified logic).

### Step 1.5.4: Test Integrity Verification (STORY-502) [MANDATORY if snapshot exists]

```
Glob(pattern="devforgeai/qa/snapshots/{STORY_ID}/red-phase-checksums.json")

IF snapshot found:
    Read(file_path="devforgeai/qa/snapshots/{STORY_ID}/red-phase-checksums.json")

    FOR each file in snapshot.test_files:
        Bash(command="sha256sum {file_path}")

        IF actual_sha256 != expected_sha256:
            Finding: CRITICAL: TEST TAMPERING
            overall_verdict = FAIL (no override, no deferral)

    IF all checksums match:
        Display: "✓ Test integrity verified — all checksums match red-phase snapshot"
        Record: test_integrity: PASS
    ELSE:
        Display: "❌ CRITICAL: TEST TAMPERING DETECTED — checksums do not match"
        HALT: QA approval blocked unconditionally

ELSE:
    Display: "⚠️ WARNING: Test integrity snapshot not found — skipping integrity verification (graceful degradation for pre-STORY-502 stories)"
    # Continue without blocking
```

**Step Recording:** After test integrity verification completes (PASS, FAIL, or skip), record `test_integrity_verification` in qa-phase-state.json `steps_completed` array:
```
# Record step completion in qa-phase-state.json
steps_completed.append("test_integrity_verification")
```

**Reference:** `references/diff-regression-detection.md` Section 8 (Test Integrity Verification)

### Step 1.5.5: Classify Findings

Classify all findings by severity (CRITICAL, HIGH, MEDIUM) using precedence rules from reference file.

### Step 1.5.6: Determine Phase Result

- Any CRITICAL or HIGH finding → **BLOCKED** (QA cannot approve)
- MEDIUM-only findings → **WARN** (QA continues with warnings)
- No findings → **PASS** (clean, proceed to Phase 2)

### Blocking Behavior

- **CRITICAL/HIGH findings block QA approval** with exit message
- **MEDIUM findings produce warnings** without blocking
- **Graceful degradation:** If git diff fails, phase result = PASS with warning logged
- **Test tampering findings block unconditionally** — no override mechanism (STORY-502)

### Phase 1.5 Completion Checklist

**Before proceeding to Phase 2, verify you have:**

- [ ] Diff regression detection executed (Steps 1.5.1–1.5.3)
- [ ] Test integrity snapshot read (if exists) (Step 1.5.4)
- [ ] Checksum comparison completed (if snapshot exists) (Step 1.5.4)
- [ ] All findings classified by severity (Step 1.5.5)
- [ ] Phase result determined (PASS/BLOCKED/WARN) (Step 1.5.6)

**IF any checkbox unchecked:** HALT and complete missing steps before Phase 2.

**Reference:** `references/diff-regression-detection.md`

### Phase 1.5 CLI Gate (STORY-517)

```
devforgeai-validate phase-complete {STORY_ID} --workflow=qa --phase=1.5 --checkpoint-passed --project-root=.

Display: "✓ Phase 1.5 CLI gate passed"
Display: "Phase 1.5 ✓ | Diff Regression Detection | {phase_result}"
```

---

## Phase 2: Analysis

### Pre-Flight: Verify Phase 1 Complete

```
devforgeai-validate phase-status {STORY_ID} --workflow=qa --project-root=.
# Verify phase 01 is completed in qa-phase-state.json

IF phase 01 NOT completed:
    CRITICAL ERROR: "Phase 1 not verified complete"
    HALT: "Phase 2 cannot execute without Phase 1 completion"
    Display: "Previous phase (Phase 1) must complete successfully before starting Phase 2"
    Instruction: "Start workflow from Phase 0. Run setup first."
    Exit: Code 1 (phase sequencing violation)

Display: "✓ Phase 1 verified complete - Phase 2 preconditions met"
```

### ⚠️ CHECKPOINT: Phase 2 Reference Loading [MANDATORY]

**You MUST execute ALL steps before proceeding to phase content.**

**Step 2.0: Load Workflow References (REQUIRED)**
```
Read(file_path=".claude/skills/devforgeai-qa/references/anti-pattern-detection-workflow.md")
Read(file_path=".claude/skills/devforgeai-qa/references/parallel-validation.md")
Read(file_path=".claude/skills/devforgeai-qa/references/spec-compliance-workflow.md")
Read(file_path=".claude/skills/devforgeai-qa/references/code-quality-workflow.md")
```

**These references contain the complete workflows. Execute ALL steps from the reference files.**

**After loading:** Proceed to Step 2.1 (Anti-Pattern Detection)

**IF you skip this step:** You will execute the phase incorrectly and miss mandatory steps.

---

**Purpose:** Detect anti-patterns, run parallel validators, check spec compliance, measure quality.

### Step 2.1: Anti-Pattern Detection

**Reference:** `references/anti-pattern-detection-workflow.md`
**Subagent:** anti-pattern-scanner
    Read(file_path=".claude/skills/devforgeai-qa/references/anti-pattern-detection-workflow.md")

```
# Load ALL 6 context files
Read: tech-stack.md, source-tree.md, dependencies.md,
      coding-standards.md, architecture-constraints.md, anti-patterns.md

# Invoke scanner
Task(subagent_type="anti-pattern-scanner",
     prompt="Scan {changed_files} for violations against 6 context files")

# Parse results
violations = parse_json_response()
```

**Blocks on:** CRITICAL (security, library substitution), HIGH (structure, layer)

### Step 2.2: Parallel Validation (Deep Mode Only)

**Reference:** `references/parallel-validation.md`
    Read(file_path=".claude/skills/devforgeai-qa/references/parallel-validation.md")

Execute 3 validators in SINGLE message (parallel):
```
Task(subagent_type="test-automator", prompt="Analyze test coverage...", description="Run tests")
Task(subagent_type="code-reviewer", prompt="Review code changes...", description="Review code")
Task(subagent_type="security-auditor", prompt="Scan for security issues...", description="Security scan")
```

**Success Threshold:** 66% (2 of 3 must pass)

### Step 2.3: Spec Compliance Validation

**Reference:** `references/spec-compliance-workflow.md`
**Subagent:** deferral-validator (MANDATORY if deferrals exist)
    Read(file_path=".claude/skills/devforgeai-qa/references/spec-compliance-workflow.md")

1. Validate story documentation (Implementation Notes, DoD Status, Test Results)
2. Validate acceptance criteria (tests exist and pass for each)
3. Validate deferred DoD items (invoke deferral-validator if deferrals exist)
4. Validate API contracts (endpoints match spec)
5. Validate NFRs (performance, security)
6. Generate traceability matrix

### Step 2.4: Code Quality Metrics

**Reference:** `references/code-quality-workflow.md`
    Read(file_path=".claude/skills/devforgeai-qa/references/code-quality-workflow.md")

1. Analyze cyclomatic complexity (tool: radon/complexity-report)
2. Calculate maintainability index (MI <70 = MEDIUM, <50 = HIGH)
3. Detect code duplication (jscpd, >20% = HIGH)
4. Measure documentation coverage (target: 80%)
5. Analyze dependency coupling

### Step 2.5: Diagnostic Hook on Analysis Failures (STORY-496)

```
# BR-001: Only fires when coverage-analyzer or anti-pattern-scanner report failures
IF coverage_failures OR antipattern_critical_high_violations:
    Display: "Analysis failures detected - invoking diagnostic-analyst"

    # BR-003: Graceful skip when diagnostic-analyst unavailable
    TRY:
        Task(
          subagent_type="diagnostic-analyst",
          description="Diagnose QA analysis failures for ${STORY_ID}",
          prompt="""
          Investigate QA analysis failures.

          Story: ${STORY_ID}
          Phase: QA Phase 2 (Analysis)
          Coverage failures: ${coverage_report}
          Anti-pattern violations: ${antipattern_results}

          Analyze coverage gaps and anti-pattern violations against context files.
          Provide root cause diagnosis with specific file paths and recommendations.
          """
        )
        # AC#3/AC#5: Passes coverage and anti-pattern results as failure context

        # Attach diagnosis output to gaps.json alongside original failure data
        Edit gaps.json to include:
        {
            "diagnostic_analysis": {
                "timestamp": "${ISO_8601}",
                "diagnosis": "${diagnosis_output}",
                "coverage_failures": ${coverage_failures},
                "antipattern_violations": ${antipattern_results}
            }
        }
    CATCH:
        Display: "⚠️ diagnostic-analyst unavailable - proceeding without diagnosis"
        # Graceful degradation
```

**Blocks on:** Duplication >20%, MI <50

**Display:**
```
✓ Phase 2 Complete: Analysis
  Anti-patterns: [X] CRITICAL, [X] HIGH, [X] MEDIUM
  Parallel validators: [X]/3 passed (threshold: 2/3)
  Spec compliance: [X]/[Y] criteria validated
  Quality metrics: Complexity avg [X], MI [X]%, Duplication [X]%
```

### Phase 2 Completion Checklist

**Before writing Phase 2 marker, verify you have:**

- [ ] Loaded anti-pattern-detection-workflow.md (Step 2.0)
- [ ] Invoked anti-pattern-scanner subagent (Step 2.1)
- [ ] Ran parallel validators (Step 2.2) - deep mode only
- [ ] Executed spec compliance validation (Step 2.3)
- [ ] Analyzed code quality metrics (Step 2.4)
- [ ] Checked blocking violations (CRITICAL/HIGH)
- [ ] Displayed Phase 2 completion summary

**IF any checkbox unchecked:** HALT and complete missing steps before Phase 3.

**Display to user:**
```
✓ Phase 2 Complete: Analysis | {validator_count}/3 validators
```

### Phase 2 CLI Gate (STORY-517)

```
devforgeai-validate phase-complete {STORY_ID} --workflow=qa --phase=02 --checkpoint-passed --project-root=.

Display: "✓ Phase 2 CLI gate passed"
Display: "Phase 2 ✓ | Analysis | {validator_count}/3 validators"
```

**Update execution tracker:**

```
TodoWrite({
  todos: [
    { content: "Phase 0: Setup", status: "completed", activeForm: "Phase 0 complete" },
    { content: "Phase 1: Validation", status: "completed", activeForm: "Phase 1 complete" },
    { content: "Phase 2: Analysis", status: "completed", activeForm: "Phase 2 complete" },
    { content: "Phase 3: Reporting", status: "in_progress", activeForm: "Running Phase 3: Reporting" },
    { content: "Phase 4: Cleanup", status: "pending", activeForm: "Running Phase 4: Cleanup" }
  ]
})
```

---

## Phase 3: Reporting

### Pre-Flight: Verify Phase 2 Complete

```
devforgeai-validate phase-status {STORY_ID} --workflow=qa --project-root=.
# Verify phase 02 is completed in qa-phase-state.json

IF phase 02 NOT completed:
    CRITICAL ERROR: "Phase 2 not verified complete"
    HALT: "Phase 3 cannot execute without Phase 2 completion"
    Display: "Previous phase (Phase 2) must complete successfully before starting Phase 3"
    Instruction: "Start workflow from Phase 0. Run setup first."
    Exit: Code 1 (phase sequencing violation)

Display: "✓ Phase 2 verified complete - Phase 3 preconditions met"
```

### ⚠️ CHECKPOINT: Phase 3 Reference Loading [MANDATORY]

**You MUST execute ALL steps before proceeding to phase content.**

**Step 3.0: Load Workflow Reference (REQUIRED)**
```
Read(file_path=".claude/skills/devforgeai-qa/references/qa-result-formatting-guide.md")
```

**This reference contains the complete workflow. Execute ALL steps from the reference file.**

**After loading:** Proceed to Step 3.1 (Result Determination)

**IF you skip this step:** You will execute the phase incorrectly and miss mandatory steps.

---

**Purpose:** Generate QA report, update story status, create gaps.json if failed.

### Steps 3.1-3.4: Result Determination, Report Generation, Story Update

**Reference:** `references/phase-3-reporting-workflow.md`
    Read(file_path=".claude/skills/devforgeai-qa/references/phase-3-reporting-workflow.md")

Determines QA result (PASSED/FAILED/PASS WITH WARNINGS), generates QA report (deep mode), creates gaps.json (RCA-002), updates story file via Atomic Update Protocol (STORY-177). Coverage below thresholds = FAILED (ADR-010, non-negotiable).


### Step 3.5: Invoke qa-result-interpreter

```
Task(subagent_type="qa-result-interpreter",
     prompt="Format QA results for display: {qa_data}")
```

**Display:**
```
✓ Phase 3 Complete: Reporting
  Result: [PASSED ✅ / FAILED ❌ / PASS WITH WARNINGS ⚠️]
  Report: [path / Not generated (light mode)]
  Story status: [Updated to QA Approved / QA Failed]
```

### Phase 3 Completion Checklist

**Before writing Phase 3 marker, verify you have:**

- [ ] Loaded qa-result-formatting.md (Step 3.0)
- [ ] Aggregated results from Phases 1-2 (Step 3.1)
- [ ] Invoked qa-result-interpreter subagent (Step 3.2)
- [ ] Generated QA report (Step 3.3)
- [ ] Updated story file if applicable (Step 3.4)
- [ ] Displayed final QA status to user

**IF any checkbox unchecked:** HALT and complete missing steps before Phase 4.

**Display to user:**
```
✓ Phase 3 Complete: Reporting | {overall_status}
```

### Phase 3 CLI Gate (STORY-517)

```
devforgeai-validate phase-complete {STORY_ID} --workflow=qa --phase=03 --checkpoint-passed --project-root=.

Display: "✓ Phase 3 CLI gate passed"
Display: "Phase 3 ✓ | Reporting | {overall_status}"
```

**Update execution tracker:**

```
TodoWrite({
  todos: [
    { content: "Phase 0: Setup", status: "completed", activeForm: "Phase 0 complete" },
    { content: "Phase 1: Validation", status: "completed", activeForm: "Phase 1 complete" },
    { content: "Phase 2: Analysis", status: "completed", activeForm: "Phase 2 complete" },
    { content: "Phase 3: Reporting", status: "completed", activeForm: "Phase 3 complete" },
    { content: "Phase 4: Cleanup", status: "in_progress", activeForm: "Running Phase 4: Cleanup" }
  ]
})
```

---

## Phase 4: Cleanup

### Pre-Flight: Verify Phase 3 Complete

```
devforgeai-validate phase-status {STORY_ID} --workflow=qa --project-root=.
# Verify phase 03 is completed in qa-phase-state.json

IF phase 03 NOT completed:
    CRITICAL ERROR: "Phase 3 not verified complete"
    HALT: "Phase 4 cannot execute without Phase 3 completion"
    Display: "Previous phase (Phase 3) must complete successfully before starting Phase 4"
    Instruction: "Start workflow from Phase 0. Run setup first."
    Exit: Code 1 (phase sequencing violation)

Display: "✓ Phase 3 verified complete - Phase 4 preconditions met"
```

### ⚠️ CHECKPOINT: Phase 4 Reference Loading [MANDATORY]

**You MUST execute ALL steps before proceeding to phase content.**

**Step 4.0: Load Workflow Reference (REQUIRED)**
```
Read(file_path=".claude/skills/devforgeai-qa/references/feedback-hooks-workflow.md")
```

**This reference contains the complete workflow. Execute ALL steps from the reference file.**

**After loading:** Proceed to Step 4.1 (Release Lock File)

**IF you skip this step:** You will execute the phase incorrectly and miss mandatory steps.

---

**Reference:** `references/phase-4-cleanup-workflow.md`
    Read(file_path=".claude/skills/devforgeai-qa/references/phase-4-cleanup-workflow.md")

Steps 4.1-4.5: Release lock file, invoke feedback hooks (non-blocking), display execution summary (MANDATORY), display final QA validation summary, marker cleanup (PASSED only).

### Phase 4 Completion Checklist

**Before writing Phase 4 marker, verify you have:**

- [ ] Released lock file (Step 4.1)
- [ ] Cleaned up temporary files (Step 4.2)
- [ ] Archived session checkpoint (Step 4.3)
- [ ] Displayed cleanup confirmation

**IF any checkbox unchecked:** HALT and complete missing steps before QA completion.

**Display to user:**
```
✓ Phase 4 Complete: Cleanup | Complete
```

### Phase 4 CLI Gate (STORY-517)

```
devforgeai-validate phase-complete {STORY_ID} --workflow=qa --phase=04 --checkpoint-passed --project-root=.

Display: "✓ Phase 4 CLI gate passed"
Display: "Phase 4 ✓ | Cleanup | Complete"
Display: "✓ QA workflow complete - all phase gates passed (qa-phase-state.json preserved)"
```

**Update execution tracker:**

```
TodoWrite({
  todos: [
    { content: "Phase 0: Setup", status: "completed", activeForm: "Phase 0 complete" },
    { content: "Phase 1: Validation", status: "completed", activeForm: "Phase 1 complete" },
    { content: "Phase 2: Analysis", status: "completed", activeForm: "Phase 2 complete" },
    { content: "Phase 3: Reporting", status: "completed", activeForm: "Phase 3 complete" },
    { content: "Phase 4: Cleanup", status: "completed", activeForm: "Phase 4 complete" }
  ]
})
```

### Step 4.5: Marker Cleanup [CONDITIONAL - QA PASSED ONLY]

**Rules:**
- **DO NOT delete qa-phase-state.json** — preserve it as the permanent audit trail
- **DELETE legacy .qa-phase-N.marker files** (superseded by qa-phase-state.json)
- **qa-phase-state.json IS the permanent audit trail** — matches /dev workflow behavior

**Reference:** `references/phase-4-cleanup-workflow.md` (Step 4.5: Marker Cleanup)

---

## Automation Scripts

**6 Python scripts** in `scripts/`:
1. generate_coverage_report.py
2. detect_duplicates.py
3. analyze_complexity.py
4. security_scan.py
5. validate_spec_compliance.py
6. generate_test_stubs.py

**See `references/automation-scripts.md`** for usage.
    Read(file_path=".claude/skills/devforgeai-qa/references/automation-scripts.md")

---

## Subagents

| Subagent | Phase | Purpose |
|----------|-------|---------|
| anti-pattern-scanner | 2.1 | Detect 6 violation categories |
| test-automator | 2.2 | Coverage and quality analysis |
| code-reviewer | 2.2 | Code quality review |
| security-auditor | 2.2 | Security vulnerability scan |
| deferral-validator | 2.3 | Validate DoD deferrals |
| qa-result-interpreter | 3.5 | Format display output |

---

## Treelint Integration

Phase 2 of the QA workflow invokes Treelint-enabled subagents for AST-aware semantic code search, providing 40-80% token reduction in code search operations.

**Phase-to-Subagent Mapping:**

| Step | Subagent | Treelint Feature |
|------|----------|------------------|
| Step 2.1 | anti-pattern-scanner | Architecture violation detection with AST patterns |
| Step 2.2 | test-automator | Coverage analysis with semantic test discovery |
| Step 2.2 | code-reviewer | Code quality patterns with structural matching |
| Step 2.2 | security-auditor | Security vulnerability detection with semantic search |
| Step 2.4 | coverage-analyzer | Test-to-source mapping with AST-aware analysis |

**Automatic Detection:** Each subagent automatically detects Treelint availability and falls back to Grep-based search when unavailable. No workflow changes required when Treelint is not installed.

**Reference:** `.claude/agents/references/treelint-search-patterns.md`

---

## Integration

**Invoked by:** implementing-stories, /qa command, devforgeai-orchestration
**Invokes:** 6 subagents listed above
**Outputs to:** implementing-stories (via gaps.json), devforgeai-release, user

---

## Success Criteria

**Light:** Build passes, tests pass, no CRITICAL, deferrals valid, <10K tokens
**Deep:** Coverage thresholds met, no CRITICAL/HIGH, spec compliant, quality acceptable, deferrals valid, status="QA Approved", <35K tokens

---

## Reference Files

**Single consolidated workflow (deep mode):** `references/deep-validation-workflow.md`
    Read(file_path=".claude/skills/devforgeai-qa/references/deep-validation-workflow.md")

**Individual references (21 total):**
- Workflows: parameter-extraction, dod-protocol, coverage-analysis-workflow, anti-pattern-detection-workflow, parallel-validation, spec-compliance-workflow, code-quality-workflow, report-generation, feedback-hooks-workflow, story-update-workflow, marker-operations
- Guides: coverage-analysis, anti-pattern-detection, deferral-decision-tree, language-specific-tooling, qa-result-formatting-guide, quality-metrics, security-scanning, spec-validation, traceability-validation-algorithm, test-isolation-service

---

**Token efficiency:** Entry ~1.5K, Light ~3.8K, Deep ~8K (improved via phase consolidation and single workflow file)
