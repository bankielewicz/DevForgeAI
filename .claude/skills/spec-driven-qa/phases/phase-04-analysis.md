# Phase 04: Analysis

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --workflow=qa --from=03 --to=04 --project-root=.
# Exit 0: proceed | Exit 1: Phase 03 incomplete
```

## Contract

PURPOSE: Detect anti-patterns, run parallel validators, check spec compliance, measure code quality.
REQUIRED SUBAGENTS: anti-pattern-scanner (mandatory), test-automator/code-reviewer/security-auditor (adaptive), deferral-validator (conditional), diagnostic-analyst (conditional)
REQUIRED ARTIFACTS: Anti-pattern violations, validator results, spec compliance matrix, quality metrics
STEP COUNT: 5 mandatory steps

---

## Reference Loading

Load BEFORE executing steps:
```
Read(file_path=".claude/skills/spec-driven-qa/references/anti-pattern-detection.md")
Read(file_path=".claude/skills/spec-driven-qa/references/parallel-validation.md")
Read(file_path=".claude/skills/spec-driven-qa/references/spec-compliance-validation.md")
Read(file_path=".claude/skills/spec-driven-qa/references/code-quality-workflow.md")
```

---

## Mandatory Steps

### Step 4.1: Anti-Pattern Detection

EXECUTE: Load all 6 context files. Invoke anti-pattern-scanner subagent to scan changed files for violations across 6 categories.
```
# Load ALL 6 context files (constitutional)
Read(file_path="devforgeai/specs/context/tech-stack.md")
Read(file_path="devforgeai/specs/context/source-tree.md")
Read(file_path="devforgeai/specs/context/dependencies.md")
Read(file_path="devforgeai/specs/context/coding-standards.md")
Read(file_path="devforgeai/specs/context/architecture-constraints.md")
Read(file_path="devforgeai/specs/context/anti-patterns.md")

IF ANY missing: HALT "Run /create-context first"

# Get changed files
changed_files = Bash(command="git diff --name-only main...HEAD 2>/dev/null || git diff --name-only HEAD~1")

# Invoke anti-pattern-scanner subagent
Task(subagent_type="anti-pattern-scanner",
     prompt="Scan the following changed files against all 6 context files for anti-pattern violations.
     Changed files: {changed_files}
     Context files loaded in context.
     Return JSON with violations categorized by severity: critical, high, medium, low.
     Categories: tool usage, architecture, security, coding standards, dependency, structure.")
```

**Parse JSON Response:**
```
violations_critical = result["violations"]["critical"]
violations_high = result["violations"]["high"]
violations_medium = result["violations"]["medium"]
violations_low = result["violations"]["low"]

# Update blocking state (OR logic)
blocks_qa = blocks_qa OR result["blocks_qa"]

Display: "Anti-patterns: {len(violations_critical)} CRITICAL, {len(violations_high)} HIGH, {len(violations_medium)} MEDIUM, {len(violations_low)} LOW"
```

**Regression vs Pre-existing Classification (STORY-175):**
```
FOR each violation:
    IF violation.file IN changed_files:
        violation.classification = "REGRESSION"  # Blocking
    ELSE:
        violation.classification = "PRE_EXISTING"  # Warning only

Display: "Regressions: {regression_count} | Pre-existing: {preexisting_count}"
```

VERIFY: Anti-pattern scan completed. JSON response parsed. Violations classified by severity and REGRESSION/PRE_EXISTING.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=04 --step=4.1 --subagent=anti-pattern-scanner --project-root=.`

---

### Step 4.2: Parallel Validation (Deep Mode Only)

**If $MODE == "light":** Skip this step. Display "Parallel validation: SKIPPED (light mode)". Proceed to Step 4.3.

EXECUTE: Invoke validators in parallel. Count and threshold depend on story type (STORY-183 adaptive validation, extracted in Phase 01 Step 1.7).

**Validator Selection:**

| Story Type | Validators | Threshold |
|-----------|-----------|-----------|
| feature/bugfix | test-automator, code-reviewer, security-auditor | 66% (2/3) |
| refactor | code-reviewer, security-auditor | 50% (1/2) |
| documentation | code-reviewer | 100% (1/1) |

```
# Execute selected validators in a SINGLE message (parallel)
IF $STORY_TYPE in ["feature", "bugfix"]:
    Task(subagent_type="test-automator", prompt="Coverage and quality analysis for ${STORY_ID}...")
    Task(subagent_type="code-reviewer", prompt="Code quality review for ${STORY_ID}...")
    Task(subagent_type="security-auditor", prompt="Security vulnerability scan for ${STORY_ID}...")
    threshold = 2  # 2 of 3 must pass

ELIF $STORY_TYPE == "refactor":
    Task(subagent_type="code-reviewer", prompt="Code quality review for ${STORY_ID}...")
    Task(subagent_type="security-auditor", prompt="Security vulnerability scan for ${STORY_ID}...")
    threshold = 1  # 1 of 2 must pass

ELIF $STORY_TYPE == "documentation":
    Task(subagent_type="code-reviewer", prompt="Code quality review for ${STORY_ID}...")
    threshold = 1  # 1 of 1 must pass

# Aggregate results
success_count = sum(1 for r in results if r.passed)
IF success_count < threshold:
    blocks_qa = true
    Display: "Parallel validators: {success_count}/{total} passed -- BELOW threshold ({threshold})"
ELSE:
    Display: "Parallel validators: {success_count}/{total} passed -- threshold met ({threshold})"
```

VERIFY: All selected validators invoked and returned results. success_count >= threshold OR blocks_qa set.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=04 --step=4.2 --project-root=.`

---

### Step 4.3: Spec Compliance Validation

EXECUTE: Validate story documentation, acceptance criteria, deferred DoD items, API contracts, NFRs, and generate traceability matrix.

**Sub-step 4.3.1: Validate Story Documentation**
```
Required sections in story file:
- Implementation Notes
- Definition of Done Status (or DoD items in Implementation Notes)
- Test Results
- Acceptance Criteria Verification

Grep(pattern="## Implementation Notes", path="${STORY_FILE}")
IF missing: violation (MEDIUM)
```

**Sub-step 4.3.2: Validate Acceptance Criteria**
```
FOR each AC:
    # Check test exists for this AC
    test_exists = Grep(pattern="test.*ac.*{ac_number}", path="tests/", -i=true)
    IF NOT test_exists: violation (HIGH)

    # Check test status
    IF test.status != PASSED: violation (HIGH)
```

**Sub-step 4.3.3: Validate Deferrals (MANDATORY if exist -- RCA-007)**
```
IF any DoD item unchecked:
    Read(file_path=".claude/skills/spec-driven-qa/references/dod-protocol.md")

    Task(subagent_type="deferral-validator",
         prompt="Validate all deferred DoD items for ${STORY_ID}.
         Check: user approval exists, story/ADR references provided, deferral justification adequate.
         Return: validation result per deferral item.")

    IF any deferral invalid:
        blocks_qa = true
        Display: "Invalid deferrals detected -- QA BLOCKED"
```

**Sub-step 4.3.4: Validate API Contracts**
```
FOR each endpoint in technical specification:
    Verify: implementation matches spec (method, path, params, response)
```

**Sub-step 4.3.5: Validate NFRs**
```
Check: performance, security, accessibility requirements from story
```

**Sub-step 4.3.6: Generate Traceability Matrix**
```
Matrix: Requirement -> Test -> Implementation
Store for Phase 05 report generation
```

VERIFY: All spec compliance checks completed. Traceability matrix generated. Deferral-validator invoked if deferrals exist.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=04 --step=4.3 --project-root=.`

---

### Step 4.4: Code Quality Metrics

**If $DELIVERABLE_TYPE == "non-code":**
```
Display: "Code quality: N/A (non-code implementation)"
Display: "  Cyclomatic complexity: N/A"
Display: "  Maintainability index: N/A"
Display: "  Code duplication: N/A"
Display: "  Documentation coverage: Checking..."

# Documentation coverage still applies for non-code
# Verify deliverable files are well-documented
```
Skip to VERIFY.

**If $DELIVERABLE_TYPE == "code" or "mixed":**

EXECUTE: Analyze cyclomatic complexity, maintainability index, code duplication, documentation coverage.

**Sub-step 4.4.1: Cyclomatic Complexity**
```
# Language-specific tools: radon (Python), complexity-report (JS), metrics (Java)
# Threshold: >10 = MEDIUM violation

Bash(command="source .venv/bin/activate && radon cc src/ -a -nc 2>/dev/null || echo 'radon not available'")
```

**Sub-step 4.4.2: Maintainability Index**
```
# MI < 70: MEDIUM violation
# MI < 50: HIGH violation (blocks QA)

Bash(command="source .venv/bin/activate && radon mi src/ -s 2>/dev/null || echo 'radon not available'")
```

**Sub-step 4.4.3: Code Duplication**
```
# >5% = MEDIUM, >20% = HIGH (blocks)

Bash(command="npx jscpd --reporters consoleFull ./src 2>/dev/null || echo 'jscpd not available'")
```

**Sub-step 4.4.4: Documentation Coverage**
```
# Target: 80%
# Count: documented vs undocumented public APIs
```

**Sub-step 4.4.5: Dependency Coupling**
```
# Detect: circular dependencies, high coupling (>10 deps/file)
```

VERIFY: Quality metrics collected. Violations recorded for any threshold breaches.
```
IF MI < 50: blocks_qa = true (HIGH violation)
IF duplication > 20%: blocks_qa = true (HIGH violation)
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=04 --step=4.4 --project-root=.`

---

### Step 4.5: Diagnostic Hook on Failures (STORY-496)

EXECUTE: If coverage-analyzer or anti-pattern-scanner reported failures in earlier steps, invoke diagnostic-analyst subagent for root cause diagnosis.
```
IF blocks_qa == true OR violations_critical > 0:
    Task(subagent_type="diagnostic-analyst",
         prompt="Diagnose root cause of QA failures for ${STORY_ID}.
         Failures: {failure_summary}
         Provide diagnosis and recommended fix sequence.")

    IF Task result available:
        diagnosis = result
        # Attach diagnosis to gaps.json for remediation context
        qa_report_data["diagnosis"] = diagnosis
        Display: "Diagnostic analysis: Completed -- diagnosis attached to report"
    ELSE:
        Display: "Diagnostic analysis: SKIPPED (diagnostic-analyst unavailable -- graceful degradation)"
ELSE:
    Display: "Diagnostic analysis: SKIPPED (no failures to diagnose)"
```

VERIFY: Diagnostic hook invoked if failures present. Result attached to report data (or graceful degradation logged).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=04 --step=4.5 --project-root=.`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --workflow=qa --phase=04 --checkpoint-passed --project-root=.
# Exit 0: proceed to Phase 05 | Exit 1: HALT
```

## Phase 04 Completion Display

```
Phase 04 Complete: Analysis
  Anti-patterns: {critical} CRITICAL, {high} HIGH, {medium} MEDIUM (Regressions: {reg_count} | Pre-existing: {pre_count})
  Parallel validators: {success}/{total} passed (threshold: {threshold}) [adaptive: {$STORY_TYPE}]
  Spec compliance: {passed}/{total} criteria validated
  Quality: Complexity avg {X}, MI {X}%, Duplication {X}% [or N/A for non-code]
  Diagnostic: {status}
```
