---
name: devforgeai-qa
description: Validates code quality through hybrid progressive validation (light checks during development, deep analysis after completion). Enforces test coverage (95%/85%/80% strict thresholds), detects anti-patterns, validates spec compliance, and analyzes code quality metrics. Use when validating implementations, ensuring quality standards, or preparing for release.
tools: Read, Write, Edit, Glob, Grep, Bash, Task
model: claude-haiku-4-5-20251001
---

# DevForgeAI QA Skill

Quality validation enforcing architectural constraints, coverage thresholds, and code standards through progressive validation.

---

## ⚠️ EXECUTION MODEL: This Skill Expands Inline

**After invocation, YOU (Claude) execute these instructions phase by phase.**

**When you invoke this skill:**
1. This SKILL.md content is now in your conversation
2. You execute each phase sequentially
3. You display results as you work through phases
4. You complete with success/failure report

**Do NOT:**
- ❌ Wait passively for skill to "return results"
- ❌ Assume skill is executing elsewhere
- ❌ Stop workflow after invocation

**Proceed to "Parameter Extraction" section below and begin execution.**

---

## Parameter Extraction

Extracts story ID and mode (light/deep) from conversation context.

**See `references/parameter-extraction.md`** for extraction algorithm (YAML frontmatter, file reference, explicit statement, status inference).

---

## CRITICAL: Definition of Done Protocol

**Step 2.5 (Deferral Validation) CANNOT be skipped.**

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

### Deep (~65K tokens, 8-12 min)
- Complete coverage analysis (95%/85%/80% thresholds)
- Comprehensive anti-pattern detection
- Full spec compliance (AC, API, NFRs)
- Code quality metrics
- Security scanning (OWASP Top 10)
- Deferral validation (if deferrals exist)

---

## QA Workflow (7 Phases)

**⚠️ EXECUTION STARTS HERE - You are now executing the skill's workflow.**

**Progressive Disclosure:** Workflow references are loaded when each phase executes (not before) to optimize token usage.

**IMPORTANT:** "On-demand" means "load when phase starts" - NOT "loading is optional."

**Execution Pattern:**
1. Reach phase (e.g., Phase 2: Anti-Pattern Detection)
2. See "⚠️ CHECKPOINT" marker
3. Load reference file (REQUIRED)
4. Execute ALL steps from reference file
5. Complete phase checklist
6. Proceed to next phase

**IF you skip loading a reference:** You will execute the phase incorrectly and miss mandatory steps.

---

### Phase 0.0: Validate Project Root [MANDATORY - FIRST STEP]

**Purpose:** Ensure CWD is DevForgeAI project root before ANY file operations.

**Execute BEFORE Phase 0.5 (Test Isolation):**

```
# Step 1: Check project marker file
result = Read(file_path="CLAUDE.md")

IF result.success:
    content = result.content

    # Step 2: Validate it's a DevForgeAI project
    IF content_contains("DevForgeAI") OR content_contains("devforgeai"):
        CWD_VALID = true
        Display: "✓ Project root validated"
    ELSE:
        CWD_VALID = false
        Display: "⚠ CLAUDE.md found but not a DevForgeAI project"
        HALT: Use AskUserQuestion to get correct path
ELSE:
    # Step 3: Try secondary markers
    dir_check = Glob(pattern=".claude/skills/*.md")

    IF dir_check.has_results:
        CWD_VALID = true
        Display: "✓ Project root validated via .claude/skills/ structure"
    ELSE:
        CWD_VALID = false
        Display: "❌ CWD Validation Failed"
        Display: "   Not in DevForgeAI project root."
        Display: "   Expected: CLAUDE.md with DevForgeAI configuration"
        HALT: Use AskUserQuestion: "Provide project root path?"
```

**CRITICAL:** Do NOT proceed to Phase 0.5 if CWD validation fails.

---

### Phase 0.5: Load Test Isolation Configuration (STORY-092)

**Purpose:** Load story-scoped test output paths to enable concurrent QA validations without data corruption.

**Reference:** `references/test-isolation-service.md` (path resolution, directory creation, locking)

**Step 0.5.1: Load Configuration**
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

**Step 0.5.2: Resolve Story-Scoped Paths**
```
story_paths = {
    results_dir: "{config.paths.results_base}/{STORY_ID}",
    coverage_dir: "{config.paths.coverage_base}/{STORY_ID}",
    logs_dir: "{config.paths.logs_base}/{STORY_ID}"
}

# Store for use in Phase 1 test commands
test_isolation_paths = story_paths
```

**Output:** `test_isolation_paths` variable available for Phase 1 test commands

---

### Phase 0.6: Create Story-Scoped Directories (STORY-092)

**Purpose:** Ensure story-specific output directories exist before test execution.

**Prerequisite:** Phase 0.5 completed (config loaded)

**Step 0.6.1: Check Auto-Create Setting**
```
IF config.directory.auto_create == false:
    Display: "ℹ️ Directory auto-creation disabled, skipping"
    SKIP to Phase 0.7
```

**Step 0.6.2: Create Directories**
```
# Create all three story-scoped directories
Bash(command="mkdir -p {test_isolation_paths.results_dir}")
Bash(command="mkdir -p {test_isolation_paths.coverage_dir}")
Bash(command="mkdir -p {test_isolation_paths.logs_dir}")

# Apply permissions (Linux/Mac only, ignored on Windows)
IF platform != "windows":
    Bash(command="chmod {config.directory.permissions} {test_isolation_paths.results_dir}")
    Bash(command="chmod {config.directory.permissions} {test_isolation_paths.coverage_dir}")
    Bash(command="chmod {config.directory.permissions} {test_isolation_paths.logs_dir}")
```

**Step 0.6.3: Validate Creation**
```
# Verify directories exist
FOR dir in [results_dir, coverage_dir, logs_dir]:
    IF NOT exists(dir):
        Display: "❌ ERROR: Failed to create {dir}"
        Display: "Check write permissions on tests/ directory"
        HALT workflow
```

**Step 0.6.4: Write Timestamp**
```
Write(file_path="{test_isolation_paths.results_dir}/timestamp.txt",
      content="{ISO_8601_TIMESTAMP}")

Display: "✓ Story directories created: {STORY_ID}"
```

---

### Phase 0.7: Acquire Lock File (STORY-092)

**Purpose:** Prevent concurrent QA validations from corrupting test outputs.

**Prerequisite:** Phase 0.6 completed (directories exist)

**Step 0.7.1: Check Locking Setting**
```
IF config.concurrency.locking_enabled == false:
    Display: "ℹ️ File locking disabled, skipping"
    SKIP to Phase 0.9
```

**Step 0.7.2: Check for Existing Lock**
```
lock_file = "{test_isolation_paths.results_dir}/.qa-lock"

IF exists(lock_file):
    lock_age = now() - file_mtime(lock_file)
    stale_threshold = config.concurrency.stale_lock_threshold_seconds (default: 3600)

    IF lock_age > stale_threshold:
        Display: "⚠️ Removing stale lock file (age: {lock_age}s)"
        Remove(file_path=lock_file)
    ELSE:
        Display: "⚠️ Lock file exists (another QA may be running)"
        AskUserQuestion:
            - "Wait and retry" - Wait 60 seconds and check again
            - "Force proceed" - Continue without lock (risk of data corruption)
            - "Cancel" - Abort QA validation
```

**Step 0.7.3: Create Lock File**
```
Write(file_path="{lock_file}",
      content="timestamp: {ISO_8601_TIMESTAMP}\nstory: {STORY_ID}\npid: {process_id}")

Display: "✓ Lock acquired for {STORY_ID}"
```

**Final Step (end of QA workflow):** Release lock file
```
# Add to Phase 7 cleanup:
IF config.concurrency.locking_enabled:
    Remove(file_path="{test_isolation_paths.results_dir}/.qa-lock")
    Display: "✓ Lock released for {STORY_ID}"
```

---

### Phase 0.9: AC-DoD Traceability Validation (NEW - RCA-012)

**Purpose:** Verify every Acceptance Criterion requirement has corresponding Definition of Done coverage. Prevents quality gate bypass (STORY-038 pattern) and ensures complete work validation.

**Priority:** Execute BEFORE expensive validations (Phases 1-6) to fail fast on structural issues

**Token Cost:** ~2K tokens (lightweight validation)
**Token Savings:** ~60K tokens if catches issue (avoid Phases 1-6)

**Reference:** `references/traceability-validation-algorithm.md` (complete 5-step algorithm)
**Templates:** `assets/traceability-report-template.md` (PASS/FAIL display formatting)

---

#### Step 0.9.1: Load Traceability Algorithm

```
Read(file_path="src/claude/skills/devforgeai-qa/references/traceability-validation-algorithm.md")
```

**Algorithm provides:**
- Step 1: Extract AC requirements (parse AC headers, Given/When/Then, bullets, metrics)
- Step 2: Extract DoD items (count checkboxes, parse text, calculate completion)
- Step 3: Map AC → DoD (keyword matching, ≥50% overlap required)
- Step 4: Calculate traceability score (covered / total × 100, target: 100%)
- Step 5: Validate deferrals (check "Approved Deferrals" section if DoD incomplete)

**Edge Cases Handled:**
- Multiple DoD items covering single AC requirement (collective validation)
- Single DoD item covering multiple ACs (rollup validation)
- Test-based validation (one test validates multiple requirements)
- Design-phase stories (implementation deferred with documentation)

---

#### Step 0.9.2: Execute 5-Step Validation

**Execute algorithm from reference file:**

```
# Step 1: Extract AC Requirements
IF template_version == "v2.1+":
  ac_headers = grep count "^### AC#[0-9]+" story_file
ELSE:
  ac_headers = grep count "^### [0-9]+\. \[" story_file

FOR each AC section:
  Extract: Then clauses, And clauses, bullet requirements, measurable criteria
  Store: ac_requirements[] (all granular requirements)

total_ac_requirements = ac_requirements.length

# Step 2: Extract DoD Items
dod_section = extract_between("^## Definition of Done", "^## Workflow|^## Notes")

FOR each subsection in [Implementation, Quality, Testing, Documentation]:
  Parse: checkbox lines "^- \[(x| )\] (.+)$"
  Store: dod_items[] (with section, status, text)

dod_total = dod_items.length
dod_checked = count(items where checked == true)
dod_unchecked = dod_total - dod_checked
dod_completion_pct = (dod_checked / dod_total) × 100

# Step 3: Map AC → DoD
FOR each ac_req in ac_requirements:
  ac_keywords = extract_keywords(ac_req.text)

  best_match = find_best_dod_match(ac_keywords, dod_items)
  match_score = calculate_overlap(ac_keywords, best_match.keywords)

  IF match_score >= 0.5:
    traceability_map[ac_req] = best_match
  ELSE:
    missing_traceability.append(ac_req)

# Step 4: Calculate Score
traceability_score = ((total_ac_requirements - missing_traceability.length) / total_ac_requirements) × 100

# Step 5: Validate Deferrals (if needed)
IF dod_unchecked > 0:
  Check for "## Approved Deferrals" in Implementation Notes
  IF exists:
    Extract: user_approval_timestamp, deferred_items_list
    Match: unchecked DoD items to deferred_items_list
    IF all matched:
      deferral_status = "VALID"
    ELSE:
      deferral_status = "INVALID (some items undocumented)"
  ELSE:
    deferral_status = "INVALID (no section)"
ELSE:
  deferral_status = "N/A (DoD 100% complete)"
```

**Results:**
- `traceability_score`: 0-100%
- `dod_completion_pct`: 0-100%
- `deferral_status`: "VALID" / "INVALID" / "N/A"
- `missing_traceability[]`: Unmapped requirements
- `undocumented_deferrals[]`: Incomplete items without approval

---

#### Step 0.9.3: Load and Populate Display Template

```
Read(file_path="src/claude/skills/devforgeai-qa/assets/traceability-report-template.md")
```

**Select template:**
```
IF traceability_score == 100 AND (dod_unchecked == 0 OR deferral_status == "VALID"):
  template = PASS_TEMPLATE

ELSE IF traceability_score < 100:
  template = FAIL_TEMPLATE_TRACEABILITY

ELSE IF dod_unchecked > 0 AND deferral_status contains "INVALID":
  template = FAIL_TEMPLATE_DEFERRALS
```

**Populate variables:**
```
populated_template = template

# Substitute all variables
populated_template = replace(populated_template, "{ac_count}", ac_count)
populated_template = replace(populated_template, "{total_ac_requirements}", total_ac_requirements)
populated_template = replace(populated_template, "{traceability_score}", traceability_score)
populated_template = replace(populated_template, "{dod_total}", dod_total)
populated_template = replace(populated_template, "{dod_checked}", dod_checked)
populated_template = replace(populated_template, "{dod_unchecked}", dod_unchecked)
populated_template = replace(populated_template, "{dod_completion_pct}", dod_completion_pct)
populated_template = replace(populated_template, "{deferral_status}", deferral_status)
{... substitute all variables ...}

# Add dynamic lists
IF missing_traceability.length > 0:
  FOR each missing_req in missing_traceability:
    Add line: "  • AC#{missing_req.ac_number}: {missing_req.text}"

IF undocumented_deferrals.length > 0:
  FOR each undoc_item in undocumented_deferrals:
    Add line: "  • {undoc_item.section}: {undoc_item.text}"
```

**Display:**
```
Display: {populated_template}
```

---

#### Step 0.9.4: Quality Gate Decision

**Apply gate rules:**

```
IF traceability_score < 100:
  Display: "QA WORKFLOW HALTED - Fix traceability issues before proceeding"
  EXIT Phase 0.9 (do NOT proceed to Phase 1)

IF dod_unchecked > 0 AND deferral_status == "INVALID":
  Display: "QA WORKFLOW HALTED - Add deferral documentation before proceeding"
  EXIT Phase 0.9 (do NOT proceed to Phase 1)

IF all checks PASS:
  Display: "Proceeding to Phase 1 (Validation Mode Selection)..."
  Continue to Phase 1
```

**Checkpoint Validation:**
- [ ] Traceability score calculated
- [ ] DoD completion checked
- [ ] Deferrals validated (if applicable)
- [ ] Display template selected and populated
- [ ] Quality gate decision made (PASS/HALT)
- [ ] Workflow proceeds or halts appropriately

---

### Phase 1: Test Coverage Analysis

**⚠️ CHECKPOINT: You MUST load the reference file and execute ALL steps before proceeding**

**Step 1.0: Load Workflow Reference (REQUIRED)**
```
Read(file_path=".claude/skills/devforgeai-qa/references/coverage-analysis-workflow.md")
```

**After loading:** The reference file contains a complete 7-step workflow. Execute ALL 7 steps before proceeding to Phase 2.

**Ref:** `references/coverage-analysis-workflow.md` (7 steps)
**Guide:** `references/coverage-analysis.md`
**Blocks on:** Business <95%, Application <85%, Overall <80%

**Phase 1 Completion Checklist:**
Before proceeding to Phase 2, verify you executed ALL 7 steps:
- [ ] Loaded coverage-analysis-workflow.md (Step 1.0)
- [ ] Step 1: Loaded coverage thresholds (95%/85%/80% or from config)
- [ ] Step 2: Generated coverage reports using language-specific command
- [ ] Step 3: Classified files by layer (Business Logic, Application, Infrastructure)
- [ ] Step 4: Calculated coverage percentage for each layer
- [ ] Step 5: Validated against thresholds (identified CRITICAL/HIGH violations if below)
- [ ] Step 6: Identified coverage gaps with test suggestions
- [ ] Step 7: Analyzed test quality (assertion count, over-mocking, test pyramid)
- [ ] Displayed coverage results to user with layer breakdown

**Display to user:**
```
✓ Phase 1 Complete: Test coverage analysis
  Business Logic: [X]% (threshold: 95%)
  Application: [X]% (threshold: 85%)
  Infrastructure: [X]% (threshold: 80%)
  Overall: [X]%
  Gaps identified: [X] | Test quality: [PASS/WARN]
```

**IF any checkbox unchecked:** HALT and complete missing steps.

### Phase 2: Anti-Pattern Detection

**⚠️ CHECKPOINT: You MUST load the reference file and execute ALL steps before proceeding**

**Step 2.0: Load Workflow Reference (REQUIRED)**
```
Read(file_path=".claude/skills/devforgeai-qa/references/anti-pattern-detection-workflow.md")
```

**After loading:** The reference file contains a complete 6-step workflow. Execute ALL 6 steps before proceeding to Phase 3.

**Subagent:** anti-pattern-scanner (MANDATORY - detects 6 violation categories)
**Model:** claude-haiku-4-5-20251001 (cost-efficient pattern matching)
**Token Efficiency:** 73% reduction (8K → 3K tokens) vs inline pattern matching
**Blocks on:** CRITICAL violations (security, library substitution) and HIGH violations (structure, layer)

**Phase 2 Completion Checklist:**
Before proceeding to Phase 3, verify you executed ALL 6 steps:
- [ ] Loaded anti-pattern-detection-workflow.md (Step 2.0)
- [ ] Step 1: Loaded ALL 6 context files into conversation
  - [ ] tech-stack.md
  - [ ] source-tree.md
  - [ ] dependencies.md
  - [ ] coding-standards.md
  - [ ] architecture-constraints.md
  - [ ] anti-patterns.md
- [ ] Step 2: Invoked anti-pattern-scanner subagent with complete context
- [ ] Step 3: Parsed JSON response (extracted violations by severity)
- [ ] Step 4: Updated blocks_qa state using OR logic with Phase 1
- [ ] Step 5: Displayed violations summary with severity categorization
- [ ] Step 6: Stored violations in qa_report_data for final report

**Display to user:**
```
✓ Phase 2 Complete: Anti-pattern detection
  Total violations: [X]
  CRITICAL: [X] | HIGH: [X] | MEDIUM: [X] | LOW: [X]
  Blocking: [Yes/No]
```

**IF any checkbox unchecked:** HALT and complete missing steps.

### Phase 3: Spec Compliance Validation

**⚠️ CHECKPOINT: You MUST load the reference file and execute ALL steps before proceeding**

**Step 3.0: Load Workflow Reference (REQUIRED)**
```
Read(file_path=".claude/skills/devforgeai-qa/references/spec-compliance-workflow.md")
```

**After loading:** The reference file contains a complete 6-step workflow including Step 2.5 (Deferral Validation). Execute ALL steps before proceeding to Phase 4.

**Subagent:** deferral-validator (Step 2.5 - MANDATORY if deferrals exist in story)
**Guides:** `references/spec-validation.md`, `references/deferral-decision-tree.md`, `references/dod-protocol.md`
**Blocks on:** Missing AC tests, API violations, CRITICAL/HIGH deferral violations

**Phase 3 Completion Checklist:**
Before proceeding to Phase 4, verify you executed ALL 7 steps:
- [ ] Loaded spec-compliance-workflow.md (Step 3.0)
- [ ] Step 0: Validated story documentation exists
  - [ ] Implementation Notes section present
  - [ ] Definition of Done Status documented
  - [ ] Test Results recorded
  - [ ] Acceptance Criteria Verification present
- [ ] Step 1: Loaded story specification (AC, API contracts, NFRs)
- [ ] Step 2: Validated acceptance criteria (tests exist and pass for each)
- [ ] Step 2.5: Validated deferred DoD items (MANDATORY if deferrals exist)
  - [ ] IF deferrals exist: Invoked deferral-validator subagent
  - [ ] IF no deferrals: Confirmed no incomplete DoD items (`[ ]`)
- [ ] Step 3: Validated API contracts (endpoints match spec)
- [ ] Step 4: Validated non-functional requirements (performance, security, etc.)
- [ ] Step 5: Generated traceability matrix (Requirement → Tests → Implementation)
- [ ] Displayed spec compliance results to user

**Display to user:**
```
✓ Phase 3 Complete: Spec compliance validation
  Story documentation: ✓ Complete
  AC coverage: [X] of [Y] criteria validated
  API contracts: [X] endpoints verified
  NFRs: [X] requirements checked
  Deferrals: [X validated / No deferrals]
  Traceability: [X]% complete
```

**IF any checkbox unchecked:** HALT and complete missing steps.

### Phase 4: Code Quality Metrics

**⚠️ CHECKPOINT: You MUST load the reference file and execute ALL steps before proceeding**

**Step 4.0: Load Workflow Reference (REQUIRED)**
```
Read(file_path=".claude/skills/devforgeai-qa/references/code-quality-workflow.md")
```

**After loading:** The reference file contains a complete 5-step workflow. Execute ALL steps before proceeding to Phase 5.

**Guide:** `references/quality-metrics.md`
**Blocks on:** Extreme violations (duplication >20%, MI <50)

**Phase 4 Completion Checklist:**
Before proceeding to Phase 5, verify you executed ALL 5 steps:
- [ ] Loaded code-quality-workflow.md (Step 4.0)
- [ ] Step 1: Analyzed cyclomatic complexity
  - [ ] Used language-specific tool (radon/complexity-report/metrics)
  - [ ] Identified methods with complexity >10 (MEDIUM violations)
- [ ] Step 2: Calculated maintainability index
  - [ ] Identified files with MI <70 (MEDIUM violations)
  - [ ] Identified files with MI <50 (HIGH violations - blocks QA)
- [ ] Step 3: Detected code duplication
  - [ ] Used jscpd or equivalent tool
  - [ ] Calculated duplication percentage
  - [ ] Identified if >20% (HIGH violation - blocks QA)
- [ ] Step 4: Measured documentation coverage
  - [ ] Counted documented vs undocumented public APIs
  - [ ] Calculated percentage (target: 80%)
- [ ] Step 5: Analyzed dependency coupling
  - [ ] Detected circular dependencies
  - [ ] Identified high coupling (>10 dependencies per file)
- [ ] Displayed quality metrics to user

**Display to user:**
```
✓ Phase 4 Complete: Code quality metrics
  Cyclomatic Complexity: avg [X] (max [X], threshold: ≤10)
  Maintainability Index: [X]% (threshold: ≥70)
  Code Duplication: [X]% (threshold: <5%)
  Documentation Coverage: [X]% (threshold: ≥80%)
  Coupling Issues: [X] circular deps, [X] high coupling files
  Violations: [X] HIGH, [X] MEDIUM, [X] LOW
```

**IF any checkbox unchecked:** HALT and complete missing steps.

### Phase 5: QA Report Generation

**⚠️ CHECKPOINT: You MUST generate the complete QA report before proceeding**

**Step 5.0: Load Report Generation Reference (REQUIRED)**
```
Read(file_path=".claude/skills/devforgeai-qa/references/report-generation.md")
```

**Ref:** `references/report-generation.md` (6 steps)
**Guide:** `references/qa-result-formatting-guide.md`
**Subagent:** qa-result-interpreter (formats display)
**Output:** Report, story status update, formatted display

**Phase 5 Completion Checklist:**
Before proceeding to Phase 6, verify you executed ALL 7 steps:
- [ ] Step 1: Collected all results from Phases 0.9, 1, 2, 3, 4
  - [ ] Traceability score from Phase 0.9
  - [ ] Coverage metrics from Phase 1
  - [ ] Anti-pattern violations from Phase 2
  - [ ] Spec compliance status from Phase 3
  - [ ] Quality metrics from Phase 4
- [ ] Step 2: Determined overall QA result (PASSED/FAILED/PARTIAL)
- [ ] Step 3: Generated QA report file (deep mode only)
  - [ ] IF deep mode: Created `devforgeai/qa/reports/{STORY-ID}-qa-report.md`
  - [ ] IF light mode: Skipped report file (this is correct)
- [ ] Step 3.5: Generated gaps.json (MANDATORY if FAILED)
  - [ ] IF FAILED: Created `devforgeai/qa/reports/{STORY-ID}-gaps.json`
  - [ ] Contains: coverage_gaps (files, layers, percentages, uncovered lines)
  - [ ] Contains: anti_pattern_violations (CRITICAL and HIGH only)
  - [ ] Contains: deferral_issues (violations from deferral-validator)
  - [ ] Contains: remediation_sequence (phases 02R→06R)
  - [ ] IF PASSED: Skipped (gaps.json only created on failure)
- [ ] Step 3.6: Archived resolved gaps (if PASSED after previous FAIL)
  - [ ] IF previous gaps.json existed: Moved to `devforgeai/qa/resolved/`
  - [ ] IF no previous gaps: Skipped (first pass)
- [ ] Step 4: **UPDATED STORY STATUS** ⭐ CRITICAL
  - [ ] IF PASSED: `status: Dev Complete` → `status: QA Approved ✅`
  - [ ] IF FAILED: `status: Dev Complete` → `status: QA Failed ❌`
  - [ ] Appended workflow history entry
- [ ] Step 5: Tracked QA iteration history (QA Validation History section)
- [ ] Step 6: Invoked qa-result-interpreter subagent for formatted display
- [ ] Step 7: Documented blocking violations and prepared next steps
- [ ] Displayed complete QA report to user

**Display to user:**
```
✓ Phase 5 Complete: QA Report Generated
  Result: [PASSED ✅ / FAILED ❌ / PARTIAL ⚠️]
  Report: [devforgeai/qa/reports/{STORY-ID}-qa-report.md / Not generated (light mode)]
  Blocking violations: [X]
  Next steps: [Listed below]
```

**IF any checkbox unchecked:** HALT and complete missing steps.

---

### ⚠️ MANDATORY: Step 3.5 Execution (FAILED status only)

**IF overall_status == "FAILED", you MUST execute this Write() command:**

```
Write(
  file_path="devforgeai/qa/reports/{STORY-ID}-gaps.json",
  content=JSON containing:
    - story_id
    - qa_result: "FAILED"
    - coverage_gaps: [{file, layer, current_coverage, target_coverage, gap_percentage, suggested_tests}]
    - anti_pattern_violations: [{file, line, type, severity, remediation}]
    - deferral_issues: [{item, violation_type, severity, remediation}]
    - remediation_sequence: [{phase, name, target_files, gap_count}]
)
```

**Validation Checkpoint:**
```
IF overall_status == "FAILED":
  Glob(pattern="devforgeai/qa/reports/{STORY-ID}-gaps.json")

  IF file NOT found:
    ❌ HALT - gaps.json not created
    You MUST create gaps.json before proceeding
    This file enables /dev remediation mode

  IF file found:
    ✓ gaps.json created for dev agent consumption
```

**Purpose:** The dev skill Step 0.8.5 reads this file to enter remediation mode with targeted fixes.

---

### ⚠️ MANDATORY: Step 4 - Story Status Update (RCA-013)

**You MUST update the story status based on QA result:**

```
Read(file_path="devforgeai/specs/Stories/{STORY-ID}.story.md")

IF overall_status == "PASS" OR overall_status == "PASS WITH WARNINGS":
    Edit(file_path="devforgeai/specs/Stories/{STORY-ID}.story.md",
         old_string="status: Dev Complete",
         new_string="status: QA Approved ✅")

    # Add QA completion to workflow history
    workflow_history_entry = """
- **{timestamp}**: QA validation PASSED ({mode} mode)
  - Coverage: {overall_coverage}%
  - Violations: {violation_summary}
  - Report: `devforgeai/qa/reports/{STORY-ID}-qa-report.md`
"""
    Append workflow_history_entry to story Workflow History section

IF overall_status == "FAIL":
    Edit(file_path="devforgeai/specs/Stories/{STORY-ID}.story.md",
         old_string="status: Dev Complete",
         new_string="status: QA Failed ❌")

    # Add failure details to workflow history
    workflow_history_entry = """
- **{timestamp}**: QA validation FAILED ({mode} mode)
  - Blocking issues: {blocking_issues}
  - Report: `devforgeai/qa/reports/{STORY-ID}-qa-report.md`
  - Action required: Fix issues and re-run `/qa {STORY-ID}`
"""
    Append workflow_history_entry to story Workflow History section
```

**Status transitions:**
- "Dev Complete" → "QA Approved ✅" (if PASS)
- "Dev Complete" → "QA Failed ❌" (if FAIL)
- "QA Failed" → "QA Approved ✅" (if re-validation PASS)

---

### Phase 5 Post-Validation (Enforcement)

**Before proceeding to Phase 6, execute this validation:**

```
# Read story file
Read(file_path="devforgeai/specs/Stories/{STORY-ID}.story.md")

# Extract current status
status_line = grep "^status:" in story file

# Validate status matches QA result
IF overall_status == "PASS" AND status_line NOT contains "QA Approved":
    ❌ ERROR: Story status not updated to QA Approved
    Execute Step 4 now

IF overall_status == "FAIL" AND status_line NOT contains "QA Failed":
    ❌ ERROR: Story status not updated to QA Failed
    Execute Step 4 now

IF validation passes:
    ✅ Story status correctly updated
    Proceed to Phase 6
```

---

### Phase 6: Invoke Feedback Hooks

**⚠️ CHECKPOINT: You MUST execute this phase before proceeding to Phase 7**

**Step 6.0: Load Workflow Reference (REQUIRED)**
```
Read(file_path=".claude/skills/devforgeai-qa/references/feedback-hooks-workflow.md")
```

**After loading:** Execute the feedback hook workflow. This phase is non-blocking (hook failures don't affect QA result).

**Purpose:** Trigger retrospective feedback based on QA result

**Implementation:**
```bash
# Map QA result to hook status
if [ "$QA_RESULT" = "PASSED" ]; then
  STATUS="success"
elif [ "$QA_RESULT" = "FAILED" ]; then
  STATUS="failure"
else
  STATUS="partial"
fi

# Check and invoke hooks
devforgeai-validate check-hooks --operation=qa --status=$STATUS
if [ $? -eq 0 ]; then
  devforgeai-validate invoke-hooks --operation=qa --story=$STORY_ID || {
    echo "⚠️ Feedback hook failed, QA result unchanged"
  }
fi
```

**Phase 6 Completion Checklist:**
Before proceeding to Phase 7, verify you executed ALL 5 steps:
- [ ] Loaded feedback-hooks-workflow.md (Step 6.0)
- [ ] Step 6.1: Determined QA status for hooks
  - [ ] Mapped: PASSED→completed, FAILED→failed, PARTIAL→partial
- [ ] Step 6.2: Checked if hooks should trigger
  - [ ] Called: `devforgeai-validate check-hooks --operation=qa --status=$STATUS`
  - [ ] Noted exit code: 0=trigger, 1=skip
- [ ] Step 6.3: Invoked feedback hooks (only if exit code was 0)
  - [ ] IF exit code 0: Called `devforgeai-validate invoke-hooks --operation=qa --story=$STORY_ID`
  - [ ] IF exit code 1: Noted hooks skipped (configuration blocked)
- [ ] Step 6.4: Recorded hook status (triggered/skipped/failed)
- [ ] Step 6.5: Included hook status in result object for command

**Display to user:**
```
✓ Phase 6 Complete: Feedback hooks
  Hook status: [triggered / skipped / failed]
  [If triggered: Feedback session created]
  [If skipped: Hooks disabled or mode didn't match trigger_on config]
  [If failed: Warning displayed, QA result unchanged]
```

**IF any checkbox unchecked:** HALT and complete missing steps.

### Phase 7: Update Story File (Deep Mode Pass Only)

**⚠️ CHECKPOINT: You MUST execute this phase to complete deep QA validation**

**Conditional:** Only executes if mode="deep" AND result="PASSED"

**Step 7.0: Load Workflow Reference (REQUIRED if updating story)**
```
Read(file_path=".claude/skills/devforgeai-qa/references/story-update-workflow.md")
```

**After loading:** Execute the story update workflow to mark story as QA Approved.

**Implementation:**
```
IF mode == "deep" AND result == "PASSED":
  Read(file_path=story_file)

  Edit(file_path=story_file, old_string="status: Dev Complete", new_string="status: QA Approved")

  Edit(file_path=story_file, old_string="updated: {old_date}", new_string="updated: {current_date}")

  Edit: Mark "- [ ] QA phase complete" as "- [x] QA phase complete" in Workflow Status

  Display: "✅ Story updated to QA Approved"
```

**Phase 7 Completion Checklist (Deep Mode PASSED Only):**
Before completing QA workflow, verify you executed ALL 6 steps:
- [ ] Loaded story-update-workflow.md (Step 7.0)
- [ ] Step 7.1: Read current story file
  - [ ] Extracted current status from YAML frontmatter
  - [ ] Extracted current `updated:` timestamp
- [ ] Step 7.2: Updated story status
  - [ ] Changed: `status: Dev Complete` → `status: QA Approved`
- [ ] Step 7.3: Updated YAML frontmatter timestamp
  - [ ] Changed: `updated: [old_date]` → `updated: [current_date]`
- [ ] Step 7.4: Inserted QA Validation History section
  - [ ] Added complete validation details (coverage, violations, test results)
  - [ ] Inserted before "## Workflow History"
- [ ] Step 7.5: Appended workflow history entry
  - [ ] Added: `- **[DATE]:** QA validation passed (deep mode) - Status: QA Approved`
- [ ] Step 7.6: Displayed confirmation message to user

**Display to user:**
```
✓ Phase 7 Complete: Story file updated
  Status: Dev Complete → QA Approved
  Timestamp: [old_date] → [current_date]
  QA Validation History: ✓ Added
  Workflow History: ✓ Entry appended
```

**IF deep mode passed but any checkbox unchecked:** HALT and complete missing steps.
**IF light mode or QA not passed:** Phase 7 skips - this is correct behavior.

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

**deferral-validator** (Phase 3 Step 2.5): Validates deferrals (MANDATORY)
**qa-result-interpreter** (Phase 5 Step 6): Generates formatted display

---

## Integration

**Invoked by:** devforgeai-development, /qa command, devforgeai-orchestration
**Invokes:** deferral-validator, qa-result-interpreter
**Outputs to:** devforgeai-development, devforgeai-release, user

---

## Success Criteria

**Light:** Build passes, tests pass, no CRITICAL, deferrals valid, <10K tokens
**Deep:** Coverage thresholds met, no CRITICAL/HIGH, spec compliant, quality acceptable, deferrals valid, status="QA Approved", <65K tokens

---

## Reference Files (19 total)

**Workflows (10):** parameter-extraction, dod-protocol, coverage-analysis-workflow, anti-pattern-detection-workflow, spec-compliance-workflow, code-quality-workflow, report-generation, automation-scripts, feedback-hooks-workflow, story-update-workflow

**Guides (9):** coverage-analysis, anti-pattern-detection, deferral-decision-tree, language-specific-tooling, qa-result-formatting-guide, quality-metrics, security-scanning, spec-validation, validation-procedures

---

**Token efficiency:** Entry ~1.5K, Light ~3.8K, Deep ~11K (7x improvement via progressive disclosure)
