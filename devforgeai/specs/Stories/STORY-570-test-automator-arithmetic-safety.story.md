---
id: STORY-570
title: Add Shell Test Arithmetic Safety Rule to Test-Automator
type: feature
epic: EPIC-087
sprint: null
status: Backlog
points: 1
depends_on: []
priority: Medium
advisory: false
source_gap: null
source_story: null
assigned_to: null
created: 2026-03-03
format_version: "2.9"
---

# Story: Add Shell Test Arithmetic Safety Rule to Test-Automator

## Description

**As a** DevForgeAI test-automator subagent,
**I want** a "Shell Test Arithmetic Safety" section in my agent definition,
**so that** I generate bash test scripts with safe arithmetic patterns (`PASSED=$((PASSED + 1))`) instead of the buggy `((PASSED++))` pattern that fails under `set -e` when the variable is 0.

**Source:** RCA-047 (REC-5) — Orchestrator Test Modification Phase Violation

**Context:** During STORY-531, test-automator generated shell tests with `((PASSED++))` under `set -euo pipefail`. When PASSED=0, `((0))` evaluates to falsy in bash arithmetic, causing immediate exit under `set -e`. This triggered the entire RCA-047 incident chain: orchestrator fixed tests directly → checksum mismatch → TEST TAMPERING → QA reverted.

## Acceptance Criteria

### AC#1: Forbidden Pattern Documented

```xml
<acceptance_criteria id="AC1" implements="REC-5">
  <given>The test-automator.md agent definition exists</given>
  <when>Reading the Shell Test Arithmetic Safety section</when>
  <then>A "FORBIDDEN" block documents `((PASSED++))` and `((FAILED++))` as forbidden patterns with explanation that they fail under set -e when variable is 0</then>
  <verification>
    <source_files>
      <file hint="Agent definition">.claude/agents/test-automator.md</file>
    </source_files>
    <test_file>tests/STORY-570/test_ac1_forbidden_pattern.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Correct Pattern Documented

```xml
<acceptance_criteria id="AC2" implements="REC-5">
  <given>The Shell Test Arithmetic Safety section exists</given>
  <when>Reading the CORRECT block</when>
  <then>`PASSED=$((PASSED + 1))` and `FAILED=$((FAILED + 1))` documented as correct patterns</then>
  <verification>
    <source_files>
      <file hint="Agent definition">.claude/agents/test-automator.md</file>
    </source_files>
    <test_file>tests/STORY-570/test_ac2_correct_pattern.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: set -e Guidance Documented

```xml
<acceptance_criteria id="AC3" implements="REC-5">
  <given>The Shell Test Arithmetic Safety section exists</given>
  <when>Reading the guidance text</when>
  <then>Guidance states to use `set -uo pipefail` instead of `set -euo pipefail` when test harness must accumulate pass/fail counts</then>
  <verification>
    <source_files>
      <file hint="Agent definition">.claude/agents/test-automator.md</file>
    </source_files>
    <test_file>tests/STORY-570/test_ac3_set_e_guidance.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: RCA-047 Referenced as Rationale

```xml
<acceptance_criteria id="AC4" implements="REC-5">
  <given>The Shell Test Arithmetic Safety section exists</given>
  <when>Reading the Rationale line</when>
  <then>RCA-047 is referenced as the rationale for this rule</then>
  <verification>
    <source_files>
      <file hint="Agent definition">.claude/agents/test-automator.md</file>
    </source_files>
    <test_file>tests/STORY-570/test_ac4_rca_reference.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

## Technical Specification

**Target File:** `.claude/agents/test-automator.md`
**Change Type:** Insert new section
**Insertion Point:** After the `**Scope Boundaries:**` list (which ends with `- Does NOT modify existing tests without explicit request`), before the next `---` separator

### Current State Context (find this in test-automator.md)

The insertion point is after this block:

```markdown
**Scope Boundaries:**
- Does NOT implement production code (delegates to backend-architect)
- Does NOT run QA validation (delegates to devforgeai-qa skill)
- Does NOT modify existing tests without explicit request
```

### Exact Content to Insert

Insert the following markdown immediately after the Scope Boundaries list, before the next `---`:

````markdown

### Shell Test Arithmetic Safety

When generating bash test scripts with `set -e`:

**FORBIDDEN:**
```bash
((PASSED++))   # Fails when PASSED=0: arithmetic evaluates to 0 (falsy), triggers set -e exit
((FAILED++))   # Same issue when FAILED=0
```

**CORRECT:**
```bash
PASSED=$((PASSED + 1))   # Always succeeds: assignment, not arithmetic evaluation
FAILED=$((FAILED + 1))
```

**Also remove `set -e` from test runner scripts** if the script is designed to continue after individual test failures. Use `set -uo pipefail` instead of `set -euo pipefail` when the test harness must accumulate pass/fail counts.

**Rationale:** RCA-047 — `((VAR++))` when VAR=0 evaluates the expression `0`, which is falsy in bash arithmetic. Under `set -e`, this causes immediate script exit before the increment occurs.
````

### Structured Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "test-automator.md"
      file_path: ".claude/agents/test-automator.md"
      required_keys:
        - key: "Shell Test Arithmetic Safety section"
          type: "object"
          example: "FORBIDDEN and CORRECT code blocks with rationale"
          required: true
          validation: "Section present after Scope Boundaries"
          test_requirement: "Test: Verify section exists in test-automator.md"

  business_rules:
    - id: "BR-001"
      rule: "((VAR++)) is forbidden under set -e"
      trigger: "When generating bash test scripts"
      validation: "FORBIDDEN block documents the pattern"
      error_handling: "N/A - documentation rule"
      test_requirement: "Test: FORBIDDEN block contains ((PASSED++))"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "Test-automator generates correct arithmetic patterns in future stories"
      metric: "Zero instances of ((VAR++)) in generated tests"
      test_requirement: "Test: Correct pattern documented"
      priority: "High"
```

---

## Technical Limitations

```yaml
technical_limitations: []
```

---

## Non-Functional Requirements (NFRs)

### Performance

N/A — documentation change

### Security

N/A

### Scalability

N/A

### Reliability

**Error Handling:** Prevents bash test infrastructure bugs at generation time

### Observability

N/A

---

## Dependencies

### Prerequisite Stories

- None

### External Dependencies

- None

### Technology Dependencies

- None

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** Section exists with forbidden and correct patterns
2. **Edge Cases:**
   - set -e guidance present
   - RCA-047 reference present
3. **Error Cases:**
   - Missing section detected

### Integration Tests

**Coverage Target:** 85%

**Test Scenarios:**
1. **Agent Definition:** test-automator.md parses correctly after addition

---

## Acceptance Criteria Verification Checklist

### AC#1: Forbidden Pattern

- [ ] FORBIDDEN block present - **Phase:** 3 - **Evidence:** test_ac1
- [ ] `((PASSED++))` in forbidden block - **Phase:** 3 - **Evidence:** test_ac1

### AC#2: Correct Pattern

- [ ] CORRECT block present - **Phase:** 3 - **Evidence:** test_ac2
- [ ] `PASSED=$((PASSED + 1))` in correct block - **Phase:** 3 - **Evidence:** test_ac2

### AC#3: set -e Guidance

- [ ] `set -uo pipefail` guidance present - **Phase:** 3 - **Evidence:** test_ac3

### AC#4: RCA Reference

- [ ] RCA-047 referenced - **Phase:** 3 - **Evidence:** test_ac4

---

**Checklist Progress:** 0/5 items complete (0%)

---

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT (Critical for pre-commit validation):
See: .claude/skills/implementing-stories/references/dod-update-workflow.md for complete details
-->

## Implementation Notes

*To be filled during development*

## Definition of Done

### Implementation
- [ ] test-automator.md contains Shell Test Arithmetic Safety section
- [ ] FORBIDDEN block with `((PASSED++))` and `((FAILED++))` patterns
- [ ] CORRECT block with `PASSED=$((PASSED + 1))` pattern
- [ ] set -e vs set -uo pipefail guidance
- [ ] RCA-047 rationale reference

### Quality
- [ ] All 4 acceptance criteria have passing tests
- [ ] No broken formatting in agent definition

### Testing
- [ ] Unit test: forbidden pattern (test_ac1)
- [ ] Unit test: correct pattern (test_ac2)
- [ ] Unit test: set -e guidance (test_ac3)
- [ ] Unit test: RCA reference (test_ac4)

### Documentation
- [ ] test-automator.md updated
- [ ] Story Implementation Notes completed

---

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|

---

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-03-03 | .claude/story-requirements-analyst | Created | Story created from RCA-047 REC-5 | STORY-570.story.md |

## Notes

**Source:** RCA-047 — Orchestrator Test Modification Phase Violation
**Source Recommendation:** REC-5 — Fix test-automator shell test template to prevent bash arithmetic bug

**Design Decisions:**
- Additive documentation to existing agent definition
- Placed after Scope Boundaries section, before next separator
- Both forbidden AND correct patterns shown for clarity
- set -e removal guidance for test runner scripts

**References:**
- RCA-047: devforgeai/RCA/RCA-047-orchestrator-test-modification-phase-violation.md
- test-automator.md: .claude/agents/test-automator.md

---

Story Template Version: 2.9
Last Updated: 2026-03-03
