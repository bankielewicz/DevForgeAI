---
name: devforgeai-qa
description: Validates code quality through hybrid progressive validation (light checks during development, deep analysis after completion). Enforces test coverage (95%/85%/80% strict thresholds), detects anti-patterns, validates spec compliance, and analyzes code quality metrics. Use when validating implementations, ensuring quality standards, or preparing for release.
tools: Read, Write, Edit, Glob, Grep, Bash, Task
model: claude-haiku-4-5-20251001
---

# DevForgeAI QA Skill

Quality validation enforcing architectural constraints, coverage thresholds, and code standards through progressive validation.

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

---

## CRITICAL: Definition of Done Protocol

**Deferral Validation CANNOT be skipped.**

Deferred DoD items MUST have user approval, story/ADR references, and deferral-validator subagent validation.

**PROHIBITED:** Autonomous deferrals, manual validation shortcuts, token optimization bypasses.

**Rationale:** RCA-007 - Manual validation missed STORY-004→005→006 chain, causing work loss.

**See `references/dod-protocol.md`** for protocol requirements and enforcement.

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

**Progressive Disclosure:** Load `references/deep-validation-workflow.md` once at Phase 0 for deep mode (contains all workflow details).

**Execution Pattern:**
1. Complete Phase 0 (Setup)
2. Execute Phase 1-3 per mode requirements
3. Complete Phase 4 (Cleanup)
4. Display final results

---

## Phase 0: Setup

**Purpose:** Initialize QA environment - validate CWD, create test isolation, acquire locks.

### Step 0.1: Validate Project Root [MANDATORY - FIRST STEP]

```
# Check project marker file
result = Read(file_path="CLAUDE.md")

IF result.success:
    content = result.content
    IF content_contains("DevForgeAI") OR content_contains("devforgeai"):
        CWD_VALID = true
        Display: "✓ Project root validated"
    ELSE:
        CWD_VALID = false
        HALT: Use AskUserQuestion to get correct path
ELSE:
    # Try secondary markers
    dir_check = Glob(pattern=".claude/skills/*.md")
    IF dir_check.has_results:
        CWD_VALID = true
        Display: "✓ Project root validated via .claude/skills/ structure"
    ELSE:
        CWD_VALID = false
        HALT: Use AskUserQuestion: "Provide project root path?"
```

**CRITICAL:** Do NOT proceed if CWD validation fails.

### Step 0.2: Load Test Isolation Configuration

**Reference:** `references/test-isolation-service.md`

```
Read(file_path="devforgeai/config/test-isolation.yaml")

IF file not found:
    Display: "ℹ️ Test isolation config not found, using defaults"
    config = {
        enabled: true,
        paths: {
            results_base: "tests/results",
            coverage_base: "tests/coverage",
            logs_base: "tests/logs"
        },
        directory: { auto_create: true, permissions: 755 },
        concurrency: { locking_enabled: true, lock_timeout_seconds: 300 }
    }
ELSE:
    config = parsed YAML content
    Display: "✓ Test isolation config loaded"
```

### Step 0.3: Create Story-Scoped Directories

```
story_paths = {
    results_dir: "{config.paths.results_base}/{STORY_ID}",
    coverage_dir: "{config.paths.coverage_base}/{STORY_ID}",
    logs_dir: "{config.paths.logs_base}/{STORY_ID}"
}

IF config.directory.auto_create:
    Bash(command="mkdir -p {story_paths.results_dir} {story_paths.coverage_dir} {story_paths.logs_dir}")
    Write(file_path="{story_paths.results_dir}/timestamp.txt", content="{ISO_8601_TIMESTAMP}")
    Display: "✓ Story directories created: {STORY_ID}"
```

### Step 0.4: Acquire Lock File

```
IF config.concurrency.locking_enabled:
    lock_file = "{story_paths.results_dir}/.qa-lock"

    IF exists(lock_file):
        lock_age = now() - file_mtime(lock_file)
        IF lock_age > config.concurrency.stale_lock_threshold_seconds:
            Display: "⚠️ Removing stale lock file"
            Remove(file_path=lock_file)
        ELSE:
            AskUserQuestion: "Lock exists. Wait/Force/Cancel?"

    Write(file_path=lock_file, content="timestamp: {ISO_8601}\nstory: {STORY_ID}")
    Display: "✓ Lock acquired for {STORY_ID}"
```

### Step 0.5: Load Deep Mode Workflow (Deep Mode Only)

```
IF mode == "deep":
    Read(file_path=".claude/skills/devforgeai-qa/references/deep-validation-workflow.md")
    Display: "✓ Deep validation workflow loaded"
```

**Phase 0 Completion Checklist:**
- [ ] CWD validated
- [ ] Test isolation config loaded
- [ ] Story directories created
- [ ] Lock acquired (if enabled)
- [ ] Deep workflow loaded (if deep mode)

**Display:**
```
✓ Phase 0 Complete: Setup
  Project root: ✓ Validated
  Test isolation: ✓ Configured
  Lock: ✓ Acquired
  Mode: [light/deep]
```

---

## Phase 1: Validation

**Purpose:** Execute tests, analyze coverage, validate traceability.

### Step 1.1: AC-DoD Traceability Validation

**Reference:** `references/traceability-validation-algorithm.md`
**Templates:** `assets/traceability-report-template.md`

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

---

## Phase 2: Analysis

**Purpose:** Detect anti-patterns, run parallel validators, check spec compliance, measure quality.

### Step 2.1: Anti-Pattern Detection

**Reference:** `references/anti-pattern-detection-workflow.md`
**Subagent:** anti-pattern-scanner

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

1. Validate story documentation (Implementation Notes, DoD Status, Test Results)
2. Validate acceptance criteria (tests exist and pass for each)
3. Validate deferred DoD items (invoke deferral-validator if deferrals exist)
4. Validate API contracts (endpoints match spec)
5. Validate NFRs (performance, security)
6. Generate traceability matrix

### Step 2.4: Code Quality Metrics

**Reference:** `references/code-quality-workflow.md`

1. Analyze cyclomatic complexity (tool: radon/complexity-report)
2. Calculate maintainability index (MI <70 = MEDIUM, <50 = HIGH)
3. Detect code duplication (jscpd, >20% = HIGH)
4. Measure documentation coverage (target: 80%)
5. Analyze dependency coupling

**Blocks on:** Duplication >20%, MI <50

**Display:**
```
✓ Phase 2 Complete: Analysis
  Anti-patterns: [X] CRITICAL, [X] HIGH, [X] MEDIUM
  Parallel validators: [X]/3 passed (threshold: 2/3)
  Spec compliance: [X]/[Y] criteria validated
  Quality metrics: Complexity avg [X], MI [X]%, Duplication [X]%
```

---

## Phase 3: Reporting

**Purpose:** Generate QA report, update story status, create gaps.json if failed.

### Step 3.1: Determine Overall Result

```
IF any CRITICAL violations OR coverage < thresholds OR parallel < 66%:
    overall_status = "FAILED"
ELIF any HIGH violations:
    overall_status = "PASS WITH WARNINGS"
ELSE:
    overall_status = "PASSED"
```

### Step 3.2: Generate QA Report (Deep Mode Only)

```
IF mode == "deep":
    Write(file_path="devforgeai/qa/reports/{STORY-ID}-qa-report.md",
          content=formatted_report)
    Display: "✓ QA report generated"
```

### Step 3.3: Generate gaps.json (FAILED Only)

**MANDATORY if overall_status == "FAILED":**

```
Write(file_path="devforgeai/qa/reports/{STORY-ID}-gaps.json",
      content=JSON containing:
        - story_id
        - qa_result: "FAILED"
        - coverage_gaps: [{file, layer, current, target, gap, suggested_tests}]
        - anti_pattern_violations: [{file, line, type, severity, remediation}]
        - deferral_issues: [{item, violation_type, severity, remediation}]
        - remediation_sequence: [{phase, name, target_files, gap_count}]
)

# Verify creation
Glob(pattern="devforgeai/qa/reports/{STORY-ID}-gaps.json")
IF NOT found:
    HALT: "gaps.json not created - required for /dev remediation mode"
```

### Step 3.4: Update Story Status

```
Read(file_path="devforgeai/specs/Stories/{STORY-ID}.story.md")

IF overall_status == "PASSED" OR overall_status == "PASS WITH WARNINGS":
    Edit(old_string="status: Dev Complete", new_string="status: QA Approved ✅")

IF overall_status == "FAILED":
    Edit(old_string="status: Dev Complete", new_string="status: QA Failed ❌")

# Add workflow history entry
Append: "- **{timestamp}**: QA validation {result} ({mode} mode)"
```

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

---

## Phase 4: Cleanup

**Purpose:** Release locks, invoke feedback hooks, display final summary.

### Step 4.1: Release Lock File

```
IF config.concurrency.locking_enabled:
    Remove(file_path="{story_paths.results_dir}/.qa-lock")
    Display: "✓ Lock released for {STORY_ID}"
```

### Step 4.2: Invoke Feedback Hooks

**Reference:** `references/feedback-hooks-workflow.md`

```
# Map QA result to hook status
IF overall_status == "PASSED": STATUS = "success"
ELIF overall_status == "FAILED": STATUS = "failure"
ELSE: STATUS = "partial"

# Check and invoke hooks (non-blocking)
Bash(command="devforgeai-validate check-hooks --operation=qa --status=$STATUS")
IF exit_code == 0:
    Bash(command="devforgeai-validate invoke-hooks --operation=qa --story=$STORY_ID")
```

### Step 4.3: Display Final Summary

```
Display:
╔════════════════════════════════════════════════════════╗
║                    QA VALIDATION COMPLETE              ║
╠════════════════════════════════════════════════════════╣
║ Story: {STORY_ID}                                      ║
║ Mode: {mode}                                           ║
║ Result: {overall_status}                               ║
╠════════════════════════════════════════════════════════╣
║ Coverage:                                              ║
║   Business Logic: {biz}% | Application: {app}%         ║
║   Infrastructure: {infra}% | Overall: {overall}%       ║
╠════════════════════════════════════════════════════════╣
║ Violations: {critical} CRITICAL | {high} HIGH          ║
║             {medium} MEDIUM | {low} LOW                ║
╠════════════════════════════════════════════════════════╣
║ Next Steps:                                            ║
║   [If PASSED] Ready for /release {STORY_ID}            ║
║   [If FAILED] Run /dev {STORY_ID} for remediation      ║
╚════════════════════════════════════════════════════════╝
```

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

## Integration

**Invoked by:** devforgeai-development, /qa command, devforgeai-orchestration
**Invokes:** 6 subagents listed above
**Outputs to:** devforgeai-development (via gaps.json), devforgeai-release, user

---

## Success Criteria

**Light:** Build passes, tests pass, no CRITICAL, deferrals valid, <10K tokens
**Deep:** Coverage thresholds met, no CRITICAL/HIGH, spec compliant, quality acceptable, deferrals valid, status="QA Approved", <35K tokens

---

## Reference Files

**Single consolidated workflow (deep mode):** `references/deep-validation-workflow.md`

**Individual references (20 total):**
- Workflows: parameter-extraction, dod-protocol, coverage-analysis-workflow, anti-pattern-detection-workflow, parallel-validation, spec-compliance-workflow, code-quality-workflow, report-generation, feedback-hooks-workflow, story-update-workflow
- Guides: coverage-analysis, anti-pattern-detection, deferral-decision-tree, language-specific-tooling, qa-result-formatting-guide, quality-metrics, security-scanning, spec-validation, traceability-validation-algorithm, test-isolation-service

---

**Token efficiency:** Entry ~1.5K, Light ~3.8K, Deep ~8K (improved via phase consolidation and single workflow file)
