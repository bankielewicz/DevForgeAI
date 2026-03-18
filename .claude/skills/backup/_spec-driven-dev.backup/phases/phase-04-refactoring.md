# Phase 04: Refactoring

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --from=03 --to=04
# Exit 0: proceed | Exit 1: Phase 03 incomplete
```

## Contract

PURPOSE: Improve code quality through refactoring, coverage validation, code review, and light QA — without changing behavior.
REQUIRED SUBAGENTS: refactoring-specialist, code-reviewer
REQUIRED ARTIFACTS: None
STEP COUNT: 7 mandatory steps

**TEST FILE IMMUTABILITY (RCA-046, RCA-047):** Do NOT modify test files in this phase.

---

## Mandatory Steps

### Step 1: Invoke Refactoring Specialist

EXECUTE: Delegate refactoring to specialist subagent.
```
Task(subagent_type="refactoring-specialist", prompt="Refactor code for ${STORY_ID}.
  Focus: Reduce cyclomatic complexity (target <10), extract reusable methods, improve naming, apply DRY.
  Constraint: ALL existing tests must still pass after refactoring.
  Do NOT change test files.")
```
VERIFY: Task result returned with refactoring summary. No test files modified.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=04 --subagent=refactoring-specialist`

### Step 2: Early Coverage Validation (BLOCKING — ADR-010)

EXECUTE: Run coverage analysis and validate against thresholds.
```bash
${COVERAGE_COMMAND}  # pytest --cov, cargo tarpaulin, npm run coverage, etc.
```
Parse coverage report. Compare against thresholds:
- Business Logic >= 95%
- Application >= 85%
- Infrastructure >= 80%

VERIFY: All thresholds met.
```
IF coverage gaps detected:
  # Remediation injection: invoke test-automator in REMEDIATION mode (max 2 cycles)
  Task(subagent_type="test-automator", prompt="Generate additional tests to cover gaps for ${STORY_ID}. Gaps: <specific uncovered lines/functions>")
  Re-run coverage.
  IF still failing after 2 remediation cycles: HALT — "Coverage thresholds not met: Business={X}% App={Y}% Infra={Z}%"

IF coverage tool unavailable: Log warning "Coverage tool not available — graceful fallback" and proceed.
```

### Step 3: Verify Tests Still GREEN

EXECUTE: Run the full test suite after refactoring.
```bash
${TEST_COMMAND}
```
VERIFY: Exit code == 0.
```
IF exit code != 0: HALT — "Refactoring broke tests. Fix regressions before proceeding."
```

### Step 4: Invoke Code Reviewer

EXECUTE: Delegate code review to specialist subagent.
```
Task(subagent_type="code-reviewer", prompt="Review code changes for ${STORY_ID}.
  Focus: Code quality, maintainability, security vulnerabilities, pattern compliance, standards adherence.
  Context files: coding-standards.md, anti-patterns.md, architecture-constraints.md.")
```
VERIFY: Task result returned with review findings. No CRITICAL blocking issues.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=04 --subagent=code-reviewer`

### Step 5: Anti-Gaming Validation (BLOCKING)

EXECUTE: Check for test gaming patterns.
```
Grep(pattern="@skip|@pytest.mark.skip|skip\\(|xfail|@ignore|@disabled", path="tests/")
Grep(pattern="assert True|assert 1|pass$", path="tests/")
# Check for excessive mocking (>2x assertions count)
```
VERIFY: No gaming patterns detected.
```
IF skip decorators found: HALT — "Test gaming detected: skip decorators on tests."
IF empty tests found: HALT — "Test gaming detected: assertion-less tests."
IF excessive mocking: HALT — "Test gaming detected: mock count exceeds 2x assertion count."
```

### Step 6: Light QA Validation (MANDATORY)

EXECUTE: Invoke QA skill in light mode.
```
Skill(command="qa --mode=light --story=${STORY_ID}")
```
VERIFY: QA returns with no CRITICAL/HIGH violations.
```
IF CRITICAL/HIGH violations: HALT — "Light QA failed. Fix violations before proceeding."
```

### Step 7: Update AC Checklist (Quality Items)

EXECUTE: Mark quality-related acceptance criteria as completed.
```
Edit(file_path="${STORY_FILE}", old_string="- [ ] <quality item>", new_string="- [x] <quality item>")
```
VERIFY: Grep confirms quality items are checked.
```
Grep(pattern="- \\[x\\].*[Qq]uality", path="${STORY_FILE}")
IF no matches: HALT — "AC checklist update was skipped (RCA-003)."
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=04 --checkpoint-passed
# Exit 0: proceed to Phase 4.5 | Exit 1: quality issues detected
```

## Optional Captures (Non-Blocking)

- Capture observations (coverage_check, refactoring patterns, code review findings)
- Update session memory with Phase 04 metrics
