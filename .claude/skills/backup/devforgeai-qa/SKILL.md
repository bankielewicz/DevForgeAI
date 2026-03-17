---
name: devforgeai-qa
description: Validates code quality through hybrid progressive validation (light checks during development, deep analysis after completion). Enforces test coverage (95%/85%/80% strict thresholds), detects anti-patterns, validates spec compliance, and analyzes code quality metrics. Use when validating implementations, ensuring quality standards, or preparing for release. Always use this skill when the user runs /qa or mentions QA validation, quality checks, or coverage analysis.
tools: AskUserQuestion, Read, Write, Edit, Glob, Grep, Bash, Agent
model: claude-opus-4-6
---

# DevForgeAI QA Skill v3.0

Quality validation enforcing architectural constraints, coverage thresholds, and code standards through progressive validation. Six phases, executed sequentially — no skipping.

---

## Execution Model

After invocation, YOU execute these phases sequentially. This skill expands inline — you are not waiting for external results.

1. Read this SKILL.md (already in context)
2. Load `references/shared-protocols.md` for pre-flight, CLI gates, and task tracking patterns
3. Execute Phases 1-6 in order, loading each phase's reference files on demand
4. Complete with success/failure report

---

## Shared Protocols

Load once at the start — covers pre-flight verification, CLI gates, and task tracking for all phases:

```
Read(file_path=".claude/skills/devforgeai-qa/references/shared-protocols.md")
```

This file defines:
- **Pre-flight template** — verify previous phase completed before starting current phase (Phases 2-6)
- **CLI gate template** — record phase completion via `devforgeai-validate phase-complete`
- **Task tracking** — TaskCreate at Phase 1, TaskUpdate at each transition

---

## Definition of Done Protocol

Deferral validation CANNOT be skipped (RCA-007). Deferred DoD items require user approval, story/ADR references, and deferral-validator subagent validation.

Load protocol details when needed:
```
Read(file_path=".claude/skills/devforgeai-qa/references/dod-protocol.md")
```

---

## Validation Modes

### Light (~10K tokens, 2-3 min)
- Build/syntax checks
- Test execution (100% pass required)
- Critical anti-patterns only
- Deferral validation (if deferrals exist)

### Deep (~35K tokens, 8-12 min)
- Complete coverage analysis (95%/85%/80% thresholds — ADR-010, non-negotiable)
- Comprehensive anti-pattern detection
- Full spec compliance (AC, API, NFRs)
- Code quality metrics
- Security scanning (OWASP Top 10)
- Deferral validation (if deferrals exist)

---

## Phase Overview

| Phase | Name | Purpose | Key Reference |
|-------|------|---------|---------------|
| 1 | Setup | Initialize QA environment, validate CWD, acquire locks | `phase-0-setup-workflow.md` |
| 2 | Validation | Execute tests, analyze coverage, validate traceability | `coverage-analysis.md`, `traceability-validation-algorithm.md` |
| 3 | Diff Regression | Analyze git diff for production code regressions, test integrity | `diff-regression-detection.md` |
| 4 | Analysis | Anti-patterns, parallel validators, spec compliance, quality metrics | `anti-pattern-detection.md`, `spec-compliance-validation.md` |
| 5 | Reporting | Determine QA result, generate report, update story file | `qa-result-formatting-guide.md`, `phase-3-reporting-workflow.md` |
| 6 | Cleanup | Release locks, invoke feedback hooks, display summary | `phase-4-cleanup-workflow.md` |

---

## Phase 1: Setup

**Purpose:** Initialize QA environment — validate CWD, create test isolation, acquire locks.

**Reference:** Load and execute all steps from:
```
Read(file_path=".claude/skills/devforgeai-qa/references/phase-0-setup-workflow.md")
```

**Steps:**
- 1.1: Session checkpoint detection (resume interrupted QA)
- 1.2: Validate project root (CLAUDE.md check)
- 1.3: Load test isolation configuration
- 1.4: Create story-scoped directories
- 1.5: Acquire lock file (concurrency control)
- 1.6: Load deep mode workflow reference (deep mode only)
- 1.7: Extract story type for adaptive validation (STORY-183)
- 1.8: Detect deliverable type (`code` / `non-code` / `mixed`)

**Step 1.8: Deliverable Type Detection**
Check if the story's implementation files are executable code or Markdown/config. Read the story's "Files Created/Modified" section and classify:
- **code** — `.py`, `.ts`, `.cs`, `.go`, `.rs`, `.java`, `.cpp` files present
- **non-code** — only `.md`, `.yaml`, `.json`, `.xml` files (skills, subagents, reference docs)
- **mixed** — both code and non-code files

Store result as `$DELIVERABLE_TYPE`. This affects Phases 2 and 4:
- `non-code` → skip language-specific coverage tooling (Phase 2) and code quality metrics (Phase 4)
- `code` or `mixed` → execute all steps normally

**Deep mode only — load consolidated workflow (covers Phases 2-5 content):**
```
Read(file_path=".claude/skills/devforgeai-qa/references/deep-validation-workflow.md")
```

**Reference loading strategy:** In deep mode, this consolidated file contains the workflow steps for Phases 2-5 (coverage, anti-patterns, spec compliance, quality, reporting). When you reach those phases, use the content already loaded here — do NOT re-load the individual reference files listed in those phases. The individual files exist for light mode or targeted reference, not for double-loading in deep mode.

**Initialize phase tracking and CLI gate:**
```
devforgeai-validate phase-init {STORY_ID} --workflow=qa --project-root=.
devforgeai-validate phase-complete {STORY_ID} --workflow=qa --phase=01 --checkpoint-passed --project-root=.
```

**Display:**
```
Phase 1 Complete: Setup
  Project root: Validated
  Test isolation: Configured
  Lock: Acquired
  Mode: [light/deep]
```

---

## Phase 2: Validation

**Purpose:** Execute tests, analyze coverage, validate AC-DoD traceability.

**Pre-flight:** Verify Phase 1 complete (see shared-protocols.md).

**References:** Load before executing:
```
Read(file_path=".claude/skills/devforgeai-qa/references/traceability-validation-algorithm.md")
Read(file_path=".claude/skills/devforgeai-qa/assets/traceability-report-template.md")
Read(file_path=".claude/skills/devforgeai-qa/references/coverage-analysis.md")
```

**Steps:**

**2.1: AC-DoD Traceability Validation**
Extract AC requirements and DoD items from story file. Map each AC to its corresponding DoD item. Calculate traceability score. If score < 100%, halt and report missing traceability.

**2.2: Test Coverage Analysis**
**If `$DELIVERABLE_TYPE == non-code` (from Step 1.8):** Skip language-specific coverage tooling. Instead, verify structural test coverage — confirm test files exist, assertions validate content structure, and all ACs have corresponding tests. Report coverage as "N/A (non-code implementation, structural tests only)." Proceed to CLI gate.

**If `$DELIVERABLE_TYPE == code` or `mixed`:** Execute 7-step workflow from coverage-analysis.md:
1. Load coverage thresholds (95%/85%/80%)
2. Generate coverage reports (language-specific command)
3. Classify files by layer (Business Logic, Application, Infrastructure)
4. Calculate coverage percentage for each layer
5. Validate against thresholds — violations are CRITICAL blockers (ADR-010)
6. Identify coverage gaps with test suggestions
7. Analyze test quality (assertions, mocking, pyramid)

**Blocks on (code only):** Business <95%, Application <85%, Overall <80%

**CLI gate:**
```
devforgeai-validate phase-complete {STORY_ID} --workflow=qa --phase=02 --checkpoint-passed --project-root=.
```

**Display:**
```
Phase 2 Complete: Validation
  Traceability: {score}%
  Business Logic: {X}% (threshold: 95%)
  Application: {X}% (threshold: 85%)
  Infrastructure: {X}% (threshold: 80%)
```

---

## Phase 3: Diff Regression Detection

**Purpose:** Analyze `git diff main...HEAD` for production code regressions and verify test integrity.

**Pre-flight:** Verify Phase 2 complete.

**Reference:**
```
Read(file_path=".claude/skills/devforgeai-qa/references/diff-regression-detection.md")
```

**Steps:**

**3.1: Execute Git Diff** — Parse unified diff output into structured hunks.

**3.2: Apply File Exclusion** — Exclude test files (`**/tests/**`, `**/*.test.*`, `**/*.spec.*`, `test_*.py`, `*_test.py`).

**3.3: Scan for Regressions** — Detect function deletion, error handler removal, signature changes, simplified logic.

**3.4: Test Integrity Verification (STORY-502)**
If red-phase checksum snapshot exists at `devforgeai/qa/snapshots/{STORY_ID}/red-phase-checksums.json`:
- Compare current test file SHA256 checksums against snapshot
- Checksum mismatch = CRITICAL: TEST TAMPERING (blocks unconditionally, no override)
- All match = test integrity verified
- No snapshot = graceful degradation (warning, continue)

Record `test_integrity_verification` in qa-phase-state.json steps_completed.

**3.5: Classify and Determine Result**
- CRITICAL/HIGH findings → BLOCKED (QA cannot approve)
- MEDIUM-only → WARN (QA continues)
- No findings → PASS
- Test tampering → BLOCKED (no override)

**CLI gate:**
```
devforgeai-validate phase-complete {STORY_ID} --workflow=qa --phase=03 --checkpoint-passed --project-root=.
```

**Display:**
```
Phase 3 Complete: Diff Regression
  Result: {PASS/BLOCKED/WARN}
  Test integrity: {PASS/FAIL/skipped}
```

---

## Phase 4: Analysis

**Purpose:** Detect anti-patterns, run parallel validators, check spec compliance, measure quality.

**Pre-flight:** Verify Phase 3 complete.

**References:**
```
Read(file_path=".claude/skills/devforgeai-qa/references/anti-pattern-detection.md")
Read(file_path=".claude/skills/devforgeai-qa/references/parallel-validation.md")
Read(file_path=".claude/skills/devforgeai-qa/references/spec-compliance-validation.md")
Read(file_path=".claude/skills/devforgeai-qa/references/code-quality-workflow.md")
```

**Steps:**

**4.1: Anti-Pattern Detection**
Load all 6 context files. Invoke anti-pattern-scanner subagent to scan changed files for violations across 6 categories. Parse JSON response. CRITICAL/HIGH violations block QA.

**4.2: Parallel Validation (Deep Mode Only)**
Validator count and success threshold depend on story type (STORY-183 adaptive validation):

| Story Type | Validators | Threshold | Which Validators |
|-----------|-----------|-----------|-----------------|
| Feature/bugfix | 3 | 66% (2/3) | test-automator, code-reviewer, security-auditor |
| Refactor | 2 | 50% (1/2) | code-reviewer, security-auditor |
| Documentation | 1 | 100% (1/1) | code-reviewer |

Execute the selected validators in a single message (parallel). The story type was extracted in Phase 1, Step 1.7.

**4.3: Spec Compliance Validation**
Validate story documentation, acceptance criteria, deferred DoD items (invoke deferral-validator if deferrals exist — MANDATORY per RCA-007), API contracts, NFRs, and generate traceability matrix.

**4.4: Code Quality Metrics**
**If `$DELIVERABLE_TYPE == non-code` (from Step 1.8):** Skip cyclomatic complexity, maintainability index, and duplication tooling. Report as "N/A (non-code implementation)." Documentation coverage still applies.

**If `$DELIVERABLE_TYPE == code` or `mixed`:** Analyze cyclomatic complexity (>10 = warning), maintainability index (MI <70 = MEDIUM, <50 = HIGH), code duplication (>20% = HIGH), documentation coverage (target: 80%).

**4.5: Diagnostic Hook on Failures (STORY-496)**
If coverage-analyzer or anti-pattern-scanner report failures, invoke diagnostic-analyst subagent for root cause diagnosis. Attach diagnosis to gaps.json. Graceful degradation if diagnostic-analyst unavailable.

**Blocks on:** CRITICAL anti-patterns, HIGH violations, duplication >20%, MI <50

**CLI gate:**
```
devforgeai-validate phase-complete {STORY_ID} --workflow=qa --phase=04 --checkpoint-passed --project-root=.
```

**Display:**
```
Phase 4 Complete: Analysis
  Anti-patterns: {X} CRITICAL, {X} HIGH, {X} MEDIUM
  Parallel validators: {X}/{N} passed (threshold: {T}) [adaptive: {story_type}]
  Spec compliance: {X}/{Y} criteria validated
  Quality: Complexity avg {X}, MI {X}%, Duplication {X}% [or N/A for non-code]
```

---

## Phase 5: Reporting

**Purpose:** Determine QA result, generate report, update story file.

**Pre-flight:** Verify Phase 4 complete.

**References:**
```
Read(file_path=".claude/skills/devforgeai-qa/references/qa-result-formatting-guide.md")
Read(file_path=".claude/skills/devforgeai-qa/references/phase-3-reporting-workflow.md")
```

**Steps:**

**5.1: Result Determination**
Aggregate results from Phases 2-4. Apply ADR-010: coverage below thresholds = FAILED (not "PASS WITH WARNINGS").

| Condition | Result |
|-----------|--------|
| All pass, no blocking violations | PASSED |
| Only MEDIUM/LOW violations | PASS WITH WARNINGS |
| Any CRITICAL/HIGH or coverage below threshold | FAILED |

**5.2: Report Generation (deep mode)**
Generate QA report file. Invoke qa-result-interpreter subagent for formatted display.

**5.3: Story Update**
Update story file status via Atomic Update Protocol (STORY-177). If PASSED: status → "QA Approved". If FAILED: create gaps.json with failure context (RCA-002).

**5.4: Format Display**
Invoke qa-result-interpreter subagent:
```
Agent(subagent_type="qa-result-interpreter",
      prompt="Format QA results for display: {qa_data}")
```

**CLI gate:**
```
devforgeai-validate phase-complete {STORY_ID} --workflow=qa --phase=05 --checkpoint-passed --project-root=.
```

**Display:**
```
Phase 5 Complete: Reporting
  Result: [PASSED / FAILED / PASS WITH WARNINGS]
  Report: [path / Not generated (light mode)]
  Story status: [Updated to QA Approved / QA Failed]
```

---

## Phase 6: Cleanup

**Purpose:** Release locks, invoke feedback hooks, display execution summary.

**Pre-flight:** Verify Phase 5 complete.

**Reference:**
```
Read(file_path=".claude/skills/devforgeai-qa/references/phase-4-cleanup-workflow.md")
Read(file_path=".claude/skills/devforgeai-qa/references/feedback-hooks-workflow.md")
```

**Steps:**

**6.1: Release Lock File**

**6.2: Invoke Feedback Hooks (non-blocking)**
Capture AI architectural analysis observations. Failures in hooks do not block QA completion.

**6.3: Display Execution Summary (MANDATORY)**
Show phase-by-phase completion status with timing and token usage.

**6.4: Display Final QA Validation Summary**

**6.5: Marker Cleanup (PASSED only)**
- Preserve qa-phase-state.json as permanent audit trail
- Delete legacy QA marker files if present (superseded by qa-phase-state.json)

**CLI gate:**
```
devforgeai-validate phase-complete {STORY_ID} --workflow=qa --phase=06 --checkpoint-passed --project-root=.
```

**Display:**
```
Phase 6 Complete: Cleanup
  QA workflow complete — all phase gates passed
```

---

## Parameter Extraction

Load at Phase 1 to extract story ID and mode from conversation context:
```
Read(file_path=".claude/skills/devforgeai-qa/references/parameter-extraction.md")
```

Extraction methods: YAML frontmatter, file reference, explicit statement, status inference.
Default mode: deep (if unable to determine).

---

## Subagents

| Subagent | Phase | Purpose |
|----------|-------|---------|
| anti-pattern-scanner | 4.1 | Detect 6 violation categories against context files |
| test-automator | 4.2 | Coverage and quality analysis |
| code-reviewer | 4.2 | Code quality review |
| security-auditor | 4.2 | Security vulnerability scan (OWASP Top 10) |
| deferral-validator | 4.3 | Validate DoD deferrals (MANDATORY if deferrals exist) |
| qa-result-interpreter | 5.4 | Format display output |
| diagnostic-analyst | 4.5 | Diagnose analysis failures (graceful degradation) |

---

## Automation Scripts

Six Python scripts in `scripts/` for deterministic analysis:
1. `generate_coverage_report.py` — coverage data extraction
2. `detect_duplicates.py` — code duplication analysis
3. `analyze_complexity.py` — cyclomatic complexity calculation
4. `security_scan.py` — pattern-based security scanning
5. `validate_spec_compliance.py` — spec validation automation
6. `generate_test_stubs.py` — test stub generation

Usage details: `references/automation-scripts.md`

---

## Integration

**Invoked by:** `/qa` command, implementing-stories (light), devforgeai-orchestration (deep)
**Invokes:** 7 subagents listed above
**Outputs to:** implementing-stories (via gaps.json), devforgeai-release, user display
**Gates:** Gate 2 (Test Passing), Gate 3 (QA Approval)

---

## Success Criteria

**Light:** Build passes, tests pass, no CRITICAL, deferrals valid, <10K tokens
**Deep:** Coverage thresholds met, no CRITICAL/HIGH, spec compliant, quality acceptable, deferrals valid, status="QA Approved", <35K tokens

---

## Reference Files Index

**Loaded at start:**
- `shared-protocols.md` — pre-flight, CLI gates, task tracking

**Loaded per phase (on demand):**

| Phase | Reference Files |
|-------|----------------|
| 1 | `parameter-extraction.md`, `phase-0-setup-workflow.md`, `deep-validation-workflow.md` (deep only) |
| 2 | `traceability-validation-algorithm.md`, `coverage-analysis.md` |
| 3 | `diff-regression-detection.md` |
| 4 | `anti-pattern-detection.md`, `parallel-validation.md`, `spec-compliance-validation.md`, `code-quality-workflow.md` |
| 5 | `qa-result-formatting-guide.md`, `phase-3-reporting-workflow.md` |
| 6 | `phase-4-cleanup-workflow.md`, `feedback-hooks-workflow.md` |

**Supporting references (loaded by phase references as needed):**
- `dod-protocol.md` — deferral validation protocol
- `deferral-decision-tree.md` — deferral classification
- `language-specific-tooling.md` — coverage commands by language
- `test-isolation-service.md` — test isolation configuration
- `story-update-workflow.md` — atomic story file updates
- `marker-operations.md` — phase marker file operations
- `automation-scripts.md` — Python script documentation
- `quality-metrics.md` — metric thresholds
- `security-scanning.md` — OWASP patterns
- `test-tampering-heuristics.md` — test tampering patterns
- `subagent-prompt-templates.md` — prompt templates for subagents
- `coverage-analyzer-integration-guide.md` — coverage analyzer subagent guide
