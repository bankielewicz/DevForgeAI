---
id: STORY-491
title: Create Root-Cause-Diagnosis Skill, Diagnostic-Analyst Subagent, and Diagnosis-Before-Fix Rule
type: feature
epic: EPIC-084
sprint: Backlog
status: QA Approved
points: 3
depends_on: []
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: null
created: 2026-02-23
format_version: "2.9"
---

# Story: Create Root-Cause-Diagnosis Skill, Diagnostic-Analyst Subagent, and Diagnosis-Before-Fix Rule

## Description

**As a** DevForgeAI framework developer,
**I want** structured diagnostic capabilities that enforce investigation before fix attempts,
**so that** root causes are identified systematically rather than symptoms being patched repeatedly, reducing fix cycles and preventing regression from blind retries.

**Example:**
When tests fail during Phase 03 (Green), instead of blindly re-invoking backend-architect, the framework first invokes the root-cause-diagnosis skill to identify whether the failure is caused by spec drift, test assertion errors, import failures, or anti-pattern violations — then prescribes a targeted fix.

## Acceptance Criteria

Define testable, specific conditions that must be met for story completion. Use XML format with `<acceptance_criteria>` blocks for machine-parseable verification.

> **IMPORTANT:** XML acceptance criteria format is REQUIRED for automated verification by the ac-compliance-verifier subagent. Legacy markdown format (Given/When/Then bullets) is NOT supported by verification tools.

### XML Acceptance Criteria Format

Use the following XML schema for each acceptance criterion:

```xml
<acceptance_criteria id="AC1" implements="COMP-001,COMP-002,COMP-003">
  <given>Initial context or precondition</given>
  <when>Action or event being tested</when>
  <then>Expected outcome or result</then>
  <verification>
    <source_files>
      <file hint="Main implementation">path/to/source.py</file>
    </source_files>
    <test_file>path/to/test.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### AC#1: root-cause-diagnosis Skill Enforces 4-Phase Investigation Methodology

```xml
<acceptance_criteria id="AC1" implements="COMP-001">
  <given>A failure, bug, or unexpected behavior is reported in the DevForgeAI framework</given>
  <when>The root-cause-diagnosis skill at .claude/skills/root-cause-diagnosis/SKILL.md is invoked</when>
  <then>The skill enforces execution of all 4 phases in strict order — CAPTURE (collect failure artifacts), INVESTIGATE (cross-reference against context files), HYPOTHESIZE (generate ranked hypotheses), PRESCRIBE (recommend targeted fixes) — and blocks any fix attempt until all 4 phases complete</then>
  <verification>
    <source_files>
      <file hint="Skill definition">src/claude/skills/root-cause-diagnosis/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-491/test_ac1_skill_phases.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: diagnostic-analyst Subagent Detects Spec Drift Against All 6 Constitutional Context Files

```xml
<acceptance_criteria id="AC2" implements="COMP-004">
  <given>The diagnostic-analyst subagent at .claude/agents/diagnostic-analyst.md is invoked during an investigation</given>
  <when>The subagent executes its cross-reference analysis</when>
  <then>It reads all 6 constitutional context files (tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md), compares implementation artifacts against each file's constraints, and produces a spec-drift report identifying which constraints are violated with file path and line number citations for each violation found</then>
  <verification>
    <source_files>
      <file hint="Subagent definition">src/claude/agents/diagnostic-analyst.md</file>
    </source_files>
    <test_file>tests/STORY-491/test_ac2_spec_drift.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: diagnosis-before-fix Rule Defines the Blocking Principle

```xml
<acceptance_criteria id="AC3" implements="COMP-005">
  <given>A failure occurs during any DevForgeAI workflow phase</given>
  <when>.claude/rules/workflow/diagnosis-before-fix.md is evaluated by the framework</when>
  <then>The rule file exists at the specified path, contains a clearly defined HALT trigger that blocks fix attempts until diagnosis is complete, and references the root-cause-diagnosis skill as the required diagnostic path</then>
  <verification>
    <source_files>
      <file hint="Rule definition">src/claude/rules/workflow/diagnosis-before-fix.md</file>
    </source_files>
    <test_file>tests/STORY-491/test_ac3_rule_halt.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: root-cause-diagnosis Skill Includes Investigation Patterns in references/

```xml
<acceptance_criteria id="AC4" implements="COMP-002,COMP-003">
  <given>The root-cause-diagnosis skill directory is created</given>
  <when>A developer or subagent loads the skill for investigation</when>
  <then>The references/ subdirectory exists under .claude/skills/root-cause-diagnosis/ and contains investigation-patterns.md (6 failure categories) and workflow-integration.md (integration pseudocode for /dev and /qa hooks)</then>
  <verification>
    <source_files>
      <file hint="Investigation patterns">src/claude/skills/root-cause-diagnosis/references/investigation-patterns.md</file>
      <file hint="Workflow integration">src/claude/skills/root-cause-diagnosis/references/workflow-integration.md</file>
    </source_files>
    <test_file>tests/STORY-491/test_ac4_references.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: diagnostic-analyst Subagent Is Read-Only with Correct Tool Restrictions

```xml
<acceptance_criteria id="AC5" implements="COMP-004">
  <given>The diagnostic-analyst subagent is defined at .claude/agents/diagnostic-analyst.md</given>
  <when>The subagent specification is read</when>
  <then>The allowed tools list contains only [Read, Grep, Glob] (no Write, Edit, Bash, or other mutating tools), confirming read-only enforcement by design</then>
  <verification>
    <source_files>
      <file hint="Subagent definition">src/claude/agents/diagnostic-analyst.md</file>
    </source_files>
    <test_file>tests/STORY-491/test_ac5_readonly.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### Source Files Guidance

The `<source_files>` element provides hints to the ac-compliance-verifier about where implementation code is located.

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "root-cause-diagnosis SKILL.md"
      file_path: "src/claude/skills/root-cause-diagnosis/SKILL.md"
      required_keys:
        - key: "name"
          type: "string"
          example: "root-cause-diagnosis"
          required: true
          test_requirement: "Test: YAML frontmatter contains name: root-cause-diagnosis"
        - key: "allowed-tools"
          type: "string"
          example: "Read Grep Glob Task"
          required: true
          test_requirement: "Test: YAML frontmatter contains allowed-tools field"
      requirements:
        - id: "COMP-001"
          description: "Must define 4-phase methodology (CAPTURE, INVESTIGATE, HYPOTHESIZE, PRESCRIBE) in strict sequential order"
          implements_ac: ["AC#1"]
          testable: true
          test_requirement: "Test: All 4 phase names appear in SKILL.md in correct order"
          priority: "Critical"

    - type: "Configuration"
      name: "investigation-patterns.md"
      file_path: "src/claude/skills/root-cause-diagnosis/references/investigation-patterns.md"
      required_keys:
        - key: "Spec Drift category"
          type: "string"
          required: true
          test_requirement: "Test: File contains Spec Drift as first investigation category"
        - key: "6 failure categories"
          type: "string"
          required: true
          test_requirement: "Test: File documents all 6 failure categories (Spec Drift, Test Assertion, Import/Dependency, Coverage Gaps, Anti-Pattern Violations, DoD/Commit Validation)"
      requirements:
        - id: "COMP-002"
          description: "Must document 6 categorized failure patterns: Spec Drift, Test Assertion Failures, Import/Dependency Failures, Coverage Gaps, Anti-Pattern Violations, DoD/Commit Validation Failures"
          implements_ac: ["AC#4"]
          testable: true
          test_requirement: "Test: Grep for all 6 category headers in investigation-patterns.md"
          priority: "High"

    - type: "Configuration"
      name: "workflow-integration.md"
      file_path: "src/claude/skills/root-cause-diagnosis/references/workflow-integration.md"
      required_keys:
        - key: "Phase 03 integration"
          type: "string"
          required: true
          test_requirement: "Test: File contains Phase 03 (Green) integration pseudocode"
        - key: "Phase 05 integration"
          type: "string"
          required: true
          test_requirement: "Test: File contains Phase 05 (Integration) integration pseudocode"
        - key: "QA Phase 2 integration"
          type: "string"
          required: true
          test_requirement: "Test: File contains QA Phase 2 integration pseudocode"
      requirements:
        - id: "COMP-003"
          description: "Must document exact integration pseudocode for Phase 03, Phase 05, and QA Phase 2 hooks"
          implements_ac: ["AC#4"]
          testable: true
          test_requirement: "Test: File contains integration blocks for all 3 workflow phases"
          priority: "High"

    - type: "Configuration"
      name: "diagnostic-analyst.md"
      file_path: "src/claude/agents/diagnostic-analyst.md"
      required_keys:
        - key: "name"
          type: "string"
          example: "diagnostic-analyst"
          required: true
          test_requirement: "Test: YAML frontmatter contains name: diagnostic-analyst"
        - key: "tools"
          type: "array"
          example: "[Read, Grep, Glob]"
          required: true
          validation: "Must contain exactly Read, Grep, Glob — no Write, Edit, or Bash"
          test_requirement: "Test: Tools array is exactly [Read, Grep, Glob]"
      requirements:
        - id: "COMP-004"
          description: "Must define read-only subagent with tools restricted to [Read, Grep, Glob] and constitutional context file awareness for spec drift detection"
          implements_ac: ["AC#2", "AC#5"]
          testable: true
          test_requirement: "Test: Subagent references all 6 context files and has read-only tool restrictions"
          priority: "Critical"

    - type: "Configuration"
      name: "diagnosis-before-fix.md"
      file_path: "src/claude/rules/workflow/diagnosis-before-fix.md"
      required_keys:
        - key: "HALT trigger"
          type: "string"
          required: true
          test_requirement: "Test: Rule file contains HALT trigger keyword"
        - key: "root-cause-diagnosis reference"
          type: "string"
          required: true
          test_requirement: "Test: Rule references .claude/skills/root-cause-diagnosis/SKILL.md"
      requirements:
        - id: "COMP-005"
          description: "Must establish blocking principle: diagnose before retrying, with HALT trigger and skill reference"
          implements_ac: ["AC#3"]
          testable: true
          test_requirement: "Test: Rule contains HALT trigger and references root-cause-diagnosis skill"
          priority: "Critical"

  business_rules:
    - id: "BR-001"
      rule: "NO FIX ATTEMPTS UNTIL PHASE 2 (INVESTIGATE) COMPLETES — this is the core principle preventing shotgun debugging"
      trigger: "When any workflow failure occurs and diagnosis is invoked"
      validation: "Verify SKILL.md contains explicit blocking language between Phase 1 and Phase 2"
      error_handling: "HALT workflow if fix attempted before investigation"
      test_requirement: "Test: SKILL.md contains 'NO FIX ATTEMPTS' blocking statement"
      priority: "Critical"

    - id: "BR-002"
      rule: "Spec drift must be checked FIRST in INVESTIGATE phase (Step 2a) before code-level tracing (Step 2b)"
      trigger: "When INVESTIGATE phase executes"
      validation: "Verify Step 2a (spec compliance check) precedes Step 2b (code tracing)"
      error_handling: "Enforce spec check ordering in SKILL.md phase documentation"
      test_requirement: "Test: INVESTIGATE phase shows Step 2a before Step 2b"
      priority: "High"

    - id: "BR-003"
      rule: "Diagnostic-analyst subagent must be read-only — diagnosis NEVER modifies code"
      trigger: "When diagnostic-analyst subagent is invoked"
      validation: "Verify tools array contains no Write, Edit, or Bash tools"
      error_handling: "Reject subagent definition if mutating tools detected"
      test_requirement: "Test: No Write/Edit/Bash in diagnostic-analyst tools array"
      priority: "Critical"

    - id: "BR-004"
      rule: "If 3+ fix attempts fail without diagnosis, HALT and escalate to user"
      trigger: "When fix retry count exceeds threshold"
      validation: "Verify rule file documents the 3-attempt escalation threshold"
      error_handling: "HALT with user-facing escalation message"
      test_requirement: "Test: Rule file mentions 3+ failure escalation"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "SKILL.md under 500 lines per Anthropic Agent Skills Specification progressive disclosure compliance"
      metric: "Line count < 500"
      test_requirement: "Test: wc -l SKILL.md returns value under 500"
      priority: "High"

    - id: "NFR-002"
      category: "Performance"
      requirement: "diagnostic-analyst subagent under 500 lines per source-tree.md agent size limit"
      metric: "Line count < 500"
      test_requirement: "Test: wc -l diagnostic-analyst.md returns value under 500"
      priority: "High"

    - id: "NFR-003"
      category: "Performance"
      requirement: "diagnosis-before-fix rule under 200 lines per conditional rule budget"
      metric: "Line count < 200"
      test_requirement: "Test: wc -l diagnosis-before-fix.md returns value under 200"
      priority: "Medium"

    - id: "NFR-004"
      category: "Performance"
      requirement: "CAPTURE phase must complete evidence collection within 30 seconds"
      metric: "Execution time < 30s measured from invocation to phase-complete marker"
      test_requirement: "Test: Time CAPTURE phase execution, assert < 30 seconds"
      priority: "High"

    - id: "NFR-005"
      category: "Performance"
      requirement: "Spec-drift analysis across all 6 context files must complete within 60 seconds"
      metric: "Analysis time < 60s for codebase up to 500 source files"
      test_requirement: "Test: Time diagnostic-analyst cross-reference, assert < 60 seconds"
      priority: "Medium"

    - id: "NFR-006"
      category: "Security"
      requirement: "diagnostic-analyst enforces read-only access by design — no mutating tools"
      metric: "Zero Write/Edit/Bash tools in allowed tools list"
      test_requirement: "Test: Parse tools array, assert no mutating tools present"
      priority: "Critical"

    - id: "NFR-007"
      category: "Reliability"
      requirement: "Diagnosis produces structured output or partial-result document — never terminates silently"
      metric: "100% of invocations produce output (complete or partial)"
      test_requirement: "Test: Invoke with missing artifacts, verify structured partial output returned"
      priority: "High"
```

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "diagnostic-analyst subagent"
    limitation: "Cannot detect runtime-only spec drift (e.g., configuration loaded from environment variables at runtime)"
    decision: "workaround:Focuses on static analysis of source files against context files; runtime validation deferred"
    discovered_phase: "Architecture"
    impact: "Some spec drift may only be detectable during actual execution, not during diagnosis"
```

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- CAPTURE phase: < 30s evidence collection (p95)
- INVESTIGATE phase (spec drift analysis): < 60s for 500-file codebase (p95)
- diagnosis-before-fix rule evaluation: < 100ms overhead per phase transition

**Throughput:**
- Single diagnostic session per failure (sequential, not parallel)

**Size Constraints:**
- SKILL.md < 500 lines (Anthropic Agent Skills Spec compliance)
- diagnostic-analyst.md < 500 lines (source-tree.md limit)
- diagnosis-before-fix.md < 200 lines (conditional rule budget)

---

### Security

**Authentication:**
- None (framework-internal artifacts)

**Authorization:**
- diagnostic-analyst subagent restricted to read-only tools [Read, Grep, Glob]
- No secrets, credentials, or .env file contents in diagnostic reports

**Data Protection:**
- Skip files matching `*secret*`, `*credential*`, `*.env`, `*password*` patterns during analysis
- Diagnostic output scoped to `devforgeai/feedback/` or `devforgeai/RCA/` directories

**Security Testing:**
- [ ] No Write/Edit/Bash tools in diagnostic-analyst
- [ ] No hardcoded secrets in any created files
- [ ] Proper input validation on phase inputs

---

### Scalability

**Horizontal Scaling:**
- Not applicable (single-agent invocation model)

**Codebase Size:**
- diagnostic-analyst supports up to 10,000 files using Grep pattern matching
- Investigation patterns individually loadable (< 8,000 tokens per phase)

**Extension:**
- 4-phase structure supports addition of future phases (e.g., VERIFY) without modifying existing phases

---

### Reliability

**Error Handling:**
- Skill completes all 4 phases or produces structured partial-result
- Missing context files → degraded analysis with "INCOMPLETE" flag
- Unreadable files → log path, continue with remaining files

**Retry Logic:**
- Not applicable (diagnosis is single-pass by design)
- If 3+ fix attempts fail post-diagnosis → HALT and escalate

---

### Observability

**Logging:**
- Each phase outputs structured XML blocks (`<diagnosis>`, `<prescription>`)
- Phase completion markers for workflow tracking

**Metrics:**
- Diagnosis invocation count per story
- Spec drift detection rate (violations found / analyses performed)
- Phase completion rate (4/4 vs partial)

---

## Dependencies

### Prerequisite Stories

Stories that must complete BEFORE this story can start:

- None — this story creates foundational artifacts with no prerequisites

### External Dependencies

- None (all artifacts are framework-internal configuration files)

### Technology Dependencies

- None — all deliverables are markdown/YAML files requiring no new packages

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic

**Test Scenarios:**
1. **Happy Path:** All 5 files created at correct paths with correct content
2. **Edge Cases:**
   - SKILL.md contains all 4 phase names in order
   - diagnostic-analyst tools array is exactly [Read, Grep, Glob]
   - diagnosis-before-fix.md contains HALT trigger
   - investigation-patterns.md has all 6 failure categories
   - workflow-integration.md has all 3 integration blocks
3. **Error Cases:**
   - SKILL.md exceeds 500 lines → validation fails
   - diagnostic-analyst contains Write tool → validation fails
   - diagnosis-before-fix.md missing HALT trigger → validation fails

---

### Integration Tests

**Coverage Target:** 85%+ for application layer

**Test Scenarios:**
1. **End-to-End Skill Load:** Invoke root-cause-diagnosis skill, verify 4 phases execute
2. **Subagent Invocation:** Task(subagent_type="diagnostic-analyst"), verify read-only behavior

---

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation. Check off items as each sub-task completes.

**Usage:** The implementing-stories skill updates this checklist at the end of each TDD phase (Phases 1-5), providing granular visibility into AC completion progress.

**Tracking Mechanisms:**
- **TodoWrite:** Phase-level tracking (AI monitors workflow position)
- **AC Checklist:** AC sub-item tracking (user sees granular progress) ← YOU ARE HERE
- **Definition of Done:** Official completion record (quality gate validation)

### AC#1: root-cause-diagnosis Skill Enforces 4-Phase Investigation Methodology

- [ ] SKILL.md created at .claude/skills/root-cause-diagnosis/SKILL.md - **Phase:** 2 - **Evidence:** src/claude/skills/root-cause-diagnosis/SKILL.md
- [ ] YAML frontmatter contains name, description, allowed-tools - **Phase:** 2 - **Evidence:** Grep for frontmatter fields
- [ ] All 4 phases (CAPTURE, INVESTIGATE, HYPOTHESIZE, PRESCRIBE) present in order - **Phase:** 2 - **Evidence:** Grep for phase names
- [ ] Blocking language prevents fix attempts before Phase 2 completes - **Phase:** 2 - **Evidence:** Grep for blocking statement
- [ ] SKILL.md under 500 lines - **Phase:** 3 - **Evidence:** wc -l

### AC#2: diagnostic-analyst Subagent Detects Spec Drift

- [ ] diagnostic-analyst.md created at .claude/agents/diagnostic-analyst.md - **Phase:** 2 - **Evidence:** src/claude/agents/diagnostic-analyst.md
- [ ] All 6 context files referenced by canonical path - **Phase:** 2 - **Evidence:** Grep for context file paths
- [ ] Spec drift detection methodology documented - **Phase:** 2 - **Evidence:** Read subagent content
- [ ] Structured XML output format defined (<diagnosis>, <prescription>) - **Phase:** 2 - **Evidence:** Grep for XML tags

### AC#3: diagnosis-before-fix Rule Defines Blocking Principle

- [ ] diagnosis-before-fix.md created at .claude/rules/workflow/ - **Phase:** 2 - **Evidence:** src/claude/rules/workflow/diagnosis-before-fix.md
- [ ] HALT trigger present in rule file - **Phase:** 2 - **Evidence:** Grep for HALT
- [ ] References root-cause-diagnosis skill path - **Phase:** 2 - **Evidence:** Grep for skill path

### AC#4: Investigation Patterns in references/

- [ ] investigation-patterns.md created in references/ - **Phase:** 2 - **Evidence:** File exists check
- [ ] All 6 failure categories documented - **Phase:** 2 - **Evidence:** Grep for category headers
- [ ] workflow-integration.md created in references/ - **Phase:** 2 - **Evidence:** File exists check
- [ ] Phase 03, Phase 05, QA Phase 2 integration documented - **Phase:** 2 - **Evidence:** Grep for integration blocks

### AC#5: diagnostic-analyst Is Read-Only

- [ ] Tools array contains only [Read, Grep, Glob] - **Phase:** 2 - **Evidence:** Grep for tools field
- [ ] No Write, Edit, or Bash in tools list - **Phase:** 2 - **Evidence:** Grep -v for prohibited tools

---

**Checklist Progress:** 0/17 items complete (0%)

---

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT (Critical for pre-commit validation):
When filling in the Implementation Notes section during /dev workflow:
1. DoD items MUST be placed DIRECTLY under "## Implementation Notes" header
2. NO ### subsection headers (like "### Definition of Done Status") before DoD items
3. The extract_section() validator stops at the first ### header it encounters
4. If DoD items are under a ### subsection, the validator cannot find them → commit blocked
5. The ### Additional Notes subsection is OK because it comes AFTER DoD items
See: src/claude/skills/implementing-stories/references/dod-update-workflow.md for complete details
-->

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-23

- [x] SKILL.md created at .claude/skills/root-cause-diagnosis/SKILL.md with 4-phase methodology - Completed: Created 376-line skill with CAPTURE, INVESTIGATE, HYPOTHESIZE, PRESCRIBE phases and HALT enforcement
- [x] investigation-patterns.md created at .claude/skills/root-cause-diagnosis/references/investigation-patterns.md with 6 failure categories - Completed: Documented all 6 categories with symptoms, investigation steps, and resolution patterns
- [x] workflow-integration.md created at .claude/skills/root-cause-diagnosis/references/workflow-integration.md with integration pseudocode - Completed: Integration hooks for Phase 03, Phase 05, and QA Phase 2 with pseudocode
- [x] diagnostic-analyst.md created at .claude/agents/diagnostic-analyst.md with read-only tools and context file awareness - Completed: Read-only subagent [Read, Grep, Glob] referencing all 6 context files with spec drift methodology
- [x] diagnosis-before-fix.md created at .claude/rules/workflow/diagnosis-before-fix.md with HALT trigger - Completed: Rule with HALT trigger, skill reference, and 3-attempt escalation
- [x] All 5 acceptance criteria have passing tests - Completed: 42/42 test assertions pass across 5 test files
- [x] SKILL.md < 500 lines (Anthropic Agent Skills Spec) - Completed: 376 lines
- [x] diagnostic-analyst.md < 500 lines (source-tree.md limit) - Completed: 297 lines
- [x] diagnosis-before-fix.md < 200 lines (rule budget) - Completed: 124 lines
- [x] No anti-patterns from anti-patterns.md - Completed: Code review confirmed no violations
- [x] Unit tests for SKILL.md structure validation - Completed: test_ac1_skill_phases.sh (9 assertions)
- [x] Unit tests for diagnostic-analyst tool restrictions - Completed: test_ac5_readonly.sh (7 assertions)
- [x] Unit tests for diagnosis-before-fix HALT trigger - Completed: test_ac3_rule_halt.sh (5 assertions)
- [x] Unit tests for investigation-patterns.md 6 categories - Completed: test_ac4_references.sh (12 assertions)
- [x] Unit tests for workflow-integration.md 3 integration blocks - Completed: test_ac4_references.sh (included)
- [x] Integration test: skill load and phase verification - Completed: 32 integration checks passed
- [x] SKILL.md contains YAML frontmatter with description field - Completed: Verified
- [x] diagnostic-analyst.md contains description field - Completed: Verified
- [x] All files follow Anthropic Agent Skills Specification v1.0 - Completed: Verified

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| 01 Pre-Flight | ✅ Complete | Git validated, context files loaded, tech-stack confirmed |
| 02 Red | ✅ Complete | 42 assertions written, all failing (RED) |
| 03 Green | ✅ Complete | 5 files created, 42/42 assertions passing |
| 04 Refactor | ✅ Complete | Code review approved, no refactoring needed |
| 4.5 AC Verify | ✅ Complete | 5/5 ACs verified PASS |
| 05 Integration | ✅ Complete | 32 integration checks passed |
| 5.5 AC Verify | ✅ Complete | Post-integration AC verification passed |
| 06 Deferral | ✅ Complete | No deferrals |
| 07 DoD Update | ✅ Complete | All DoD items marked complete |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/skills/root-cause-diagnosis/SKILL.md | Created | 376 |
| src/claude/skills/root-cause-diagnosis/references/investigation-patterns.md | Created | ~200 |
| src/claude/skills/root-cause-diagnosis/references/workflow-integration.md | Created | ~220 |
| src/claude/agents/diagnostic-analyst.md | Created | 297 |
| src/claude/rules/workflow/diagnosis-before-fix.md | Created | 124 |
| tests/STORY-491/test_ac1_skill_phases.sh | Created | 77 |
| tests/STORY-491/test_ac2_spec_drift.sh | Created | 46 |
| tests/STORY-491/test_ac3_rule_halt.sh | Created | 47 |
| tests/STORY-491/test_ac4_references.sh | Created | 64 |
| tests/STORY-491/test_ac5_readonly.sh | Created | 75 |
| tests/STORY-491/run_all_tests.sh | Created | 30 |

---

## Definition of Done

### Implementation
- [x] SKILL.md created at .claude/skills/root-cause-diagnosis/SKILL.md with 4-phase methodology
- [x] investigation-patterns.md created at .claude/skills/root-cause-diagnosis/references/investigation-patterns.md with 6 failure categories
- [x] workflow-integration.md created at .claude/skills/root-cause-diagnosis/references/workflow-integration.md with integration pseudocode
- [x] diagnostic-analyst.md created at .claude/agents/diagnostic-analyst.md with read-only tools and context file awareness
- [x] diagnosis-before-fix.md created at .claude/rules/workflow/diagnosis-before-fix.md with HALT trigger

### Quality
- [x] All 5 acceptance criteria have passing tests
- [x] SKILL.md < 500 lines (Anthropic Agent Skills Spec)
- [x] diagnostic-analyst.md < 500 lines (source-tree.md limit)
- [x] diagnosis-before-fix.md < 200 lines (rule budget)
- [x] No anti-patterns from anti-patterns.md

### Testing
- [x] Unit tests for SKILL.md structure validation
- [x] Unit tests for diagnostic-analyst tool restrictions
- [x] Unit tests for diagnosis-before-fix HALT trigger
- [x] Unit tests for investigation-patterns.md 6 categories
- [x] Unit tests for workflow-integration.md 3 integration blocks
- [x] Integration test: skill load and phase verification

### Documentation
- [x] SKILL.md contains YAML frontmatter with description field
- [x] diagnostic-analyst.md contains description field
- [x] All files follow Anthropic Agent Skills Specification v1.0

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-23 12:00 | .claude/story-requirements-analyst | Created | Story created from EPIC-084 Feature 1-3 | STORY-491.story.md |
| 2026-02-23 | .claude/qa-result-interpreter | QA Deep | PASSED: 42/42 tests, 0 violations | - |

## Notes

**Design Decisions:**
- Skill follows Anthropic Agent Skills Specification v1.0: kebab-case name, ≤1024 char description, SKILL.md <500 lines, progressive disclosure via references/
- Subagent is read-only by design: tools restricted to [Read, Grep, Glob] per least-privilege principle
- XML output format (`<diagnosis>` and `<prescription>` blocks) per Anthropic prompt engineering best practices
- Spec drift checked FIRST (Step 2a) because it's the most common hidden root cause category

**Backward Compatibility - Acceptance Criteria Format:**
> **Legacy markdown AC format (Given/When/Then bullets) is NOT supported by automated verification.**
> The ac-compliance-verifier subagent requires XML `<acceptance_criteria>` blocks to parse and verify ACs.

**Open Questions:**
- None

**Related ADRs:**
- None

**References:**
- EPIC-084: Structured Diagnostic Capabilities
- [Superpowers framework](https://github.com/obra/superpowers) - Inspiration for systematic-debugging skill
- Anthropic Agent Skills Specification v1.0

---

Story Template Version: 2.9
Last Updated: 2026-02-23
