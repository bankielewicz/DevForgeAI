# Deep Validation Workflow (Consolidated)

Single-load reference for deep QA validation. Contains all workflow steps for Phases 1-3.

---

## Overview

This file consolidates the following workflows for single-load efficiency:
- Coverage Analysis (7 steps)
- Traceability Validation (5 steps)
- Runtime Smoke Test (6 steps) - NEW (STORY-266)
- Documentation Accuracy Validation (4 steps)
- Anti-Pattern Detection (6 steps)
- Spec Compliance (6 steps)
- Code Quality Metrics (5 steps)
- Report Generation (6 steps)

**Token savings:** ~3.5K tokens (load once vs 7 separate files at ~500 each)

---

## Phase 1: Validation Workflows

### 1.1 Coverage Analysis (7 Steps)

**Step 1: Load Thresholds**
```
Thresholds (strict defaults):
- Business Logic: 95%
- Application: 85%
- Infrastructure: 80%
- Overall: 80%

Optional: Read(file_path=".claude/skills/devforgeai-qa/assets/config/coverage-thresholds.md")
```

**Step 2: Generate Coverage Reports**
```
Language-specific commands (use test_isolation_paths from Phase 0):

.NET:    dotnet test --collect:'XPlat Code Coverage' --results-directory={results_dir}
Python:  pytest --cov=src --cov-report=json:{coverage_dir}/coverage.json
Node.js: npm test -- --coverage --coverageDirectory={coverage_dir}
Go:      go test ./... -coverprofile={coverage_dir}/coverage.out
Rust:    cargo tarpaulin --out Json --output-dir {coverage_dir}
Java:    mvn test jacoco:report -Djacoco.destFile={coverage_dir}/jacoco.exec
```

**Step 3: Classify Files by Layer**
```
Read: devforgeai/specs/context/source-tree.md

Layer patterns (from source-tree):
- Business Logic: src/domain/*, src/core/*, src/services/*
- Application: src/api/*, src/controllers/*, src/handlers/*
- Infrastructure: src/data/*, src/repositories/*, src/external/*
```

**Step 4: Calculate Coverage by Layer**
```
FOR each file in coverage_report:
    layer = classify_file(file, source_tree_patterns)
    layer_coverage[layer].add(file.coverage)

Calculate: business_avg, application_avg, infrastructure_avg, overall_avg
```

**Step 5: Validate Against Thresholds**
```
IF business_coverage < 95%: CRITICAL violation
IF application_coverage < 85%: CRITICAL violation
IF infrastructure_coverage < 80%: HIGH violation
IF overall_coverage < 80%: CRITICAL violation
```

**Step 6: Identify Coverage Gaps**
```
FOR each uncovered_block:
    test_suggestion = {
        file, function, lines,
        suggested_test: generate_test_name(),
        priority: HIGH (business) | MEDIUM (app) | LOW (infra)
    }
```

**Step 7: Analyze Test Quality**
```
Checks:
- Assertion ratio (target: ≥1.5 per test)
- Over-mocking (mocks > tests * 2)
- Test pyramid (70% unit, 20% integration, 10% E2E)
```

---

### 1.2 Traceability Validation (5 Steps)

**Step 1: Extract AC Requirements**
```
ac_headers = grep "^### AC#[0-9]+" story_file
Extract: Then/And clauses, bullet requirements, metrics
Store: ac_requirements[]
```

**Step 2: Extract DoD Items**
```
dod_section = extract_between("^## Definition of Done", "^## Workflow")
Parse: checkbox lines "^- \[(x| )\] (.+)$"
Store: dod_items[] with section, status, text
```

**Step 3: Map AC → DoD**
```
FOR each ac_req:
    best_match = find_dod_match(ac_keywords, dod_items)
    IF match_score >= 0.5: mapped
    ELSE: missing_traceability
```

**Step 4: Calculate Score**
```
traceability_score = (covered / total) × 100
IF < 100: HALT workflow
```

**Step 5: Validate Deferrals**
```
IF dod_unchecked > 0:
    Check "## Approved Deferrals" section
    Match unchecked items to approved list
    IF unmatched: deferral_status = "INVALID"
```

---

### 1.3 Runtime Smoke Test (6 Steps) - STORY-266

**Purpose:** Verify that implemented deliverables actually execute at runtime. Prevents stories from being falsely marked "QA Approved" when the CLI/API fails to run.

**Framework-Agnostic:** Detects language from `tech-stack.md` and executes appropriate smoke test.

**Detailed Reference:** `phases/phase-01-deep-validation.md`

**Quick Summary:**
```
Step 1: Detect language from tech-stack.md (Python, Node.js, .NET, Go, Java, Rust)
Step 2: Load language config from assets/language-smoke-tests.yaml
Step 3: Extract entry point (pyproject.toml, package.json, *.csproj, etc.)
Step 4: Execute smoke test command with 10s timeout
Step 5: Process results (exit code 0 = PASS, != 0 = CRITICAL violation)
Step 6: Handle edge cases (missing files, timeout, library projects)
```

**Failure Behavior:**
- Exit code != 0: Create CRITICAL violation (type: RUNTIME_EXECUTION_FAILURE)
- Set overall_status = "FAILED"
- Include in gaps.json for remediation

**Load Full Reference:**
```
Read(file_path=".claude/skills/devforgeai-qa/phases/phase-01-deep-validation.md")
```

---

### 1.4 Documentation Accuracy Validation (4 Steps)

**Purpose:** Validate that SKILL.md file claims match actual filesystem state.

**Step 1: Extract Documentation Claims**
```
FOR each SKILL.md in .claude/skills/:
    file_count_claims = grep "Total: (\d+) reference files"
    line_count_claims = grep "(\d+) lines"
    section_claims = grep "(\d+) (sections|phases)"

    Store: {skill_name, claim_type, claimed_count}
```

**Step 2: Count Actual Resources**
```
FOR each skill with claims:
    actual_file_count = Glob(pattern=".claude/skills/{skill}/references/*.md").count()
    actual_line_count = sum(Read(file).line_count for file in references/)
    actual_section_count = grep "^## " SKILL.md | count
```

**Step 3: Compare and Generate Violations**
```
FOR each claim in claims:
    IF claimed_count != actual_count:
        violations.append({
            severity: "MEDIUM",
            type: "documentation_drift",
            file: skill_path,
            message: "Claims {claimed_count} files, found {actual_count}",
            remediation: "Update SKILL.md count or add/remove files"
        })
```

**Step 4: Aggregate Results**
```
doc_accuracy_result = {
    claims_validated: total_claims,
    discrepancies: violations.length,
    details: violations
}
```

**Claim Types Validated:**

| Claim Type | Pattern | Validation Method |
|------------|---------|-------------------|
| file_count | "Total: N reference files" | Glob count |
| line_count | "N lines" | Sum of file lines |
| section_count | "N sections/phases" | Grep header count |

---

## Phase 2: Analysis Workflows

### 2.1 Anti-Pattern Detection (6 Steps)

**Step 1: Load ALL 6 Context Files**
```
Read: tech-stack.md, source-tree.md, dependencies.md,
      coding-standards.md, architecture-constraints.md, anti-patterns.md

IF ANY missing: HALT "Run /create-context"
```

**Step 2: Invoke anti-pattern-scanner Subagent**
```
Task(subagent_type="anti-pattern-scanner",
     prompt="Scan {changed_files} with 6 context files loaded")
```

**Step 3: Parse JSON Response**
```
violations_critical = result["violations"]["critical"]
violations_high = result["violations"]["high"]
violations_medium = result["violations"]["medium"]
violations_low = result["violations"]["low"]
```

**Step 4: Update blocks_qa State (OR Logic)**
```
blocks_qa = blocks_qa OR result["blocks_qa"]
```

**Step 5: Display Summary**
```
CRITICAL: blocks immediately
HIGH: blocks QA approval
MEDIUM: warning only
LOW: advisory only
```

**Step 6: Store for Report**
```
qa_report_data["anti_pattern_violations"] = {...}
```

---

### 2.1.5 Regression vs Pre-existing Classification (STORY-175)

**Purpose:** Classify violations as REGRESSION or PRE_EXISTING based on changed files.

**Step 1: Identify Changed Files**
```
changed_files = git diff --name-only HEAD~1

Edge cases:
- First commit: Use `git diff --name-only origin/main...HEAD`
- No git repo: Fallback to all REGRESSION (blocking)
```

**Step 2: Classify Each Violation**
```
FOR each violation:
    IF violation.file IN changed_files:
        classification = "REGRESSION"
    ELSE:
        classification = "PRE_EXISTING"
```

**Step 3: Set Blocking Status**
```
REGRESSION violations:
    blocking = true  (blocks QA approval)

PRE_EXISTING violations:
    blocking = false (warning only, does not block)
```

**Step 4: Display Breakdown**
```
Format: "Regressions: {count} | Pre-existing: {count}"

Example output:
Regressions: 3 | Pre-existing: 7
Blocking: 3 | Warnings: 7
```

**Implementation Module:** `devforgeai/qa/regression_classifier.py`

**Key Functions:**
- `get_changed_files()` - Execute git diff
- `classify_violations()` - Classify batch of violations
- `set_all_blocking_status()` - Set blocking for all
- `should_block_qa()` - Check if any blocking violations
- `get_breakdown()` - Format display string

**Edge Case Handling:**
| Scenario | Behavior |
|----------|----------|
| No git repository | All REGRESSION (blocking) |
| First commit | Use `origin/main...HEAD` |
| Empty changed files | All PRE_EXISTING (non-blocking) |
| Permission/Timeout errors | Return empty list safely |

---

### 2.2 Parallel Validation (3 Validators)

**Execute in SINGLE message:**
```
Task(subagent_type="test-automator", prompt="Coverage analysis...")
Task(subagent_type="code-reviewer", prompt="Code quality review...")
Task(subagent_type="security-auditor", prompt="Security scan...")
```

**Success Threshold:** 66% (2 of 3 must pass)

**Aggregate Results:**
```
success_count = sum(1 for r in results if r.passed)
IF success_count < 2: HALT
```

---

### 2.3 Spec Compliance (6 Steps)

**Step 0: Validate Story Documentation**
```
Required sections:
- Implementation Notes
- Definition of Done Status
- Test Results
- Acceptance Criteria Verification

IF missing: HALT
```

**Step 1: Load Story Specification**
```
Read: story file
Extract: AC list, API contracts, NFRs
```

**Step 2: Validate Acceptance Criteria**
```
FOR each AC:
    test_exists = Grep(pattern="test_{ac_id}")
    IF NOT test_exists: violation
    IF test.status != PASSED: violation
```

**Step 3: Validate Deferrals (MANDATORY if exist)**
```
IF any DoD item unchecked:
    Task(subagent_type="deferral-validator", ...)
    Validate: user approval, story/ADR references
```

**Step 4: Validate API Contracts**
```
FOR each endpoint in spec:
    Verify: implementation matches spec (method, path, params, response)
```

**Step 5: Validate NFRs**
```
Check: performance, security, accessibility requirements
```

**Step 6: Generate Traceability Matrix**
```
Matrix: Requirement → Test → Implementation
```

---

### 2.4 Code Quality Metrics (5 Steps)

**Step 1: Cyclomatic Complexity**
```
Tools: radon (Python), complexity-report (JS), metrics (Java)
Threshold: >10 = MEDIUM violation

Bash(command="radon cc src/ -a -nc")
```

**Step 2: Maintainability Index**
```
MI < 70: MEDIUM violation
MI < 50: HIGH violation (blocks QA)

Bash(command="radon mi src/ -s")
```

**Step 3: Code Duplication**
```
Tool: jscpd
Threshold: >5% = MEDIUM, >20% = HIGH (blocks)

Bash(command="npx jscpd --reporters consoleFull ./src")
```

**Step 4: Documentation Coverage**
```
Target: 80%
Count: documented vs undocumented public APIs
```

**Step 5: Dependency Coupling**
```
Detect: circular dependencies, high coupling (>10 deps/file)
```

---

## Phase 3: Reporting Workflows

### 3.1 Determine Overall Result

```
IF any CRITICAL OR coverage < thresholds OR parallel < 66%:
    overall_status = "FAILED"
ELIF any HIGH:
    overall_status = "PASS WITH WARNINGS"
ELSE:
    overall_status = "PASSED"
```

### 3.2 Generate QA Report (Deep Mode Only)

```
Write(file_path="devforgeai/qa/reports/{STORY-ID}-qa-report.md")

Sections:
- Executive Summary
- Coverage Analysis
- Violation Details
- Traceability Matrix
- Recommendations
```

### 3.3 Generate gaps.json (FAILED Only)

**MANDATORY if FAILED:**
```json
{
  "story_id": "STORY-XXX",
  "qa_result": "FAILED",
  "coverage_gaps": [...],
  "anti_pattern_violations": [...],
  "deferral_issues": [...],
  "remediation_sequence": [
    {"phase": "02R", "name": "Fix tests", "target_files": [...], "gap_count": X}
  ]
}
```

**Verify creation:**
```
Glob(pattern="devforgeai/qa/reports/{STORY-ID}-gaps.json")
IF NOT found: HALT
```

### 3.4 Update Story Status

```
IF PASSED/PASS WITH WARNINGS:
    Edit: "status: Dev Complete" → "status: QA Approved ✅"

IF FAILED:
    Edit: "status: Dev Complete" → "status: QA Failed ❌"

Append workflow history entry
```

### 3.5 Format Display

```
Task(subagent_type="qa-result-interpreter", prompt="Format results")
```

### 3.6 Invoke Feedback Hooks

```
Bash: devforgeai-validate check-hooks --operation=qa --status={status}
IF exit 0: devforgeai-validate invoke-hooks --operation=qa --story={STORY_ID}
```

---

## Quick Reference: Blocking Violations

| Phase | Check | Severity | Blocks QA |
|-------|-------|----------|-----------|
| 1 | Business coverage <95% | CRITICAL | Yes |
| 1 | Application coverage <85% | CRITICAL | Yes |
| 1 | Infrastructure coverage <80% | HIGH | Yes |
| 1 | Traceability <100% | CRITICAL | Yes |
| 2 | Security vulnerabilities | CRITICAL | Yes |
| 2 | Library substitution | CRITICAL | Yes |
| 2 | Structure violations | HIGH | Yes |
| 2 | Parallel validators <66% | HIGH | Yes |
| 2 | Duplication >20% | HIGH | Yes |
| 2 | MI <50 | HIGH | Yes |
| 2 | Undocumented deferrals | HIGH | Yes |

---

## Subagent Summary

| Subagent | Phase | Invocation |
|----------|-------|------------|
| anti-pattern-scanner | 2.1 | Single Task() |
| test-automator | 2.2 | Parallel with 2 others |
| code-reviewer | 2.2 | Parallel with 2 others |
| security-auditor | 2.2 | Parallel with 2 others |
| deferral-validator | 2.3 | Conditional (if deferrals) |
| qa-result-interpreter | 3.5 | Display formatting |

---

## Phase Marker Protocol [STORY-126 Enhancement]

**Purpose:** Write marker files after each phase to enable sequential verification and resume capability.

### Marker Write Template (End of Each Phase)

```
Write(file_path="devforgeai/qa/reports/{STORY_ID}/.qa-phase-{N}.marker",
      content="phase: {N}\nstory_id: {STORY_ID}\nmode: {MODE}\ntimestamp: {TIMESTAMP}\nstatus: complete")
```

### Pre-Flight Verification Template (Start of Phases 1-4)

```
Glob(pattern="devforgeai/qa/reports/{STORY_ID}/.qa-phase-{N-1}.marker")
IF NOT found: HALT: "Phase {N-1} not completed - run in sequence"
```

### Marker Locations

| Phase | Marker File |
|-------|-------------|
| 0 | `.qa-phase-0.marker` |
| 1 | `.qa-phase-1.marker` |
| 2 | `.qa-phase-2.marker` |
| 3 | `.qa-phase-3.marker` |
| 4 | `.qa-phase-4.marker` |

**Location:** `devforgeai/qa/reports/{STORY_ID}/`

---

**Token efficiency:** ~2.5K tokens (single load) vs ~5K+ (5 separate loads)
