---
id: STORY-203
title: Add source-tree.md Validation to test-automator Phase 2
type: enhancement
epic: EPIC-033-framework-enhancement-triage-q4-2025
sprint: Backlog
status: Backlog
points: 1
depends_on: []
priority: High
assigned_to: Unassigned
created: 2026-01-01
source_rca: RCA-017
source_recommendation: REC-1
format_version: "2.5"
---

# Story: Add source-tree.md Validation to test-automator Phase 2

## Description

**As a** DevForgeAI framework developer,
**I want** the test-automator subagent to read and validate against source-tree.md before generating test files,
**so that** tests are always generated in the correct directory locations as defined by the framework's immutable architectural constraints.

**Context from RCA-017:**
test-automator generated tests in `tests/installer/` instead of `installer/tests/` per source-tree.md line 378. The subagent has no logic to validate test file locations against framework constraints. This is a CRITICAL violation of the context file enforcement pattern (Source: devforgeai/specs/context/architecture-constraints.md, lines 81-100).

**Root Cause:**
test-automator reads tech-stack.md for framework choice but does NOT read source-tree.md for file location validation. This selective reading pattern caused STORY-077 to create tests in the wrong location, which was only discovered during STORY-078 QA validation (reactive, not proactive enforcement).

## Acceptance Criteria

### AC#1: source-tree.md Reading Step Added

**Given** the test-automator subagent specification (`.claude/agents/test-automator.md`)
**When** the Phase 2 workflow is executed (Generate Failing Tests)
**Then** a new Step 4.5 is added after Step 4 (Read Tech Stack) that reads source-tree.md

**Implementation Location:** `.claude/agents/test-automator.md` lines 377-379 (after Step 4, before Step 5)

---

### AC#2: Test Directory Extraction from source-tree.md

**Given** the test-automator reads source-tree.md
**When** generating tests for a module (e.g., `installer/`)
**Then** the correct test directory is extracted from source-tree.md (e.g., `installer/tests/` per line 395-397)

**Extraction Logic:**
```markdown
IF module in "installer/":
    test_directory = "installer/tests/"  # Per source-tree.md lines 395-397
ELSE IF module in ".claude/":
    test_directory = determine from source-tree.md pattern
ELSE:
    test_directory = "tests/{module}/"  # Default pattern if not specified
```

---

### AC#3: Test Path Validation Before Write

**Given** planned test file paths
**When** test-automator prepares to generate tests
**Then** ALL test file paths are validated against the extracted test_directory BEFORE any Write() calls

**Validation Logic:**
```markdown
FOR each test_file_path in planned_test_outputs:
    IF NOT test_file_path.startswith(test_directory):
        HALT test generation
        Return error with:
        - Expected directory: {test_directory}
        - Attempted location: {test_file_path}
        - Relevant source-tree.md constraint excerpt
```

---

### AC#4: Error Message with Fix Guidance

**Given** a test path validation failure
**When** the HALT is triggered
**Then** the error message includes:
1. Clear identification of the constraint violation
2. The expected directory from source-tree.md
3. The attempted (wrong) location
4. Instructions to fix (update test paths OR update source-tree.md)
5. Excerpt from source-tree.md showing the constraint

---

### AC#5: References Section Updated

**Given** the test-automator subagent specification
**When** the enhancement is complete
**Then** source-tree.md is added to the References section (lines 851-856)

**Addition:**
```markdown
## References
- **Source Tree:** `devforgeai/specs/context/source-tree.md` (test file location constraints)
```

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "test-automator.md"
      file_path: ".claude/agents/test-automator.md"
      requirements:
        - id: "CFG-001"
          description: "Add Step 4.5 for source-tree.md reading after line 377"
          testable: true
          test_requirement: "Test: Grep for 'Read.*source-tree.md' in test-automator.md"
          priority: "Critical"
        - id: "CFG-002"
          description: "Add test directory extraction logic"
          testable: true
          test_requirement: "Test: Extract installer/tests/ from source-tree.md"
          priority: "Critical"
        - id: "CFG-003"
          description: "Add test path validation with HALT pattern"
          testable: true
          test_requirement: "Test: Wrong path triggers HALT with error message"
          priority: "Critical"
        - id: "CFG-004"
          description: "Add source-tree.md to References section"
          testable: true
          test_requirement: "Test: Grep for 'source-tree.md' in References section"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "source-tree.md is an immutable architectural constraint"
      trigger: "Before any test file Write() operation"
      validation: "All test paths must match source-tree.md patterns"
      error_handling: "HALT with clear error message and fix guidance"
      test_requirement: "Test: Verify HALT occurs on path mismatch"
      priority: "Critical"

    - id: "BR-002"
      rule: "Proactive validation prevents reactive QA discovery"
      trigger: "Phase 2 Step 4.5"
      validation: "Validation runs BEFORE any Write() calls, not after"
      error_handling: "Log validation checkpoint in execution"
      test_requirement: "Test: Verify validation runs before Write()"
      priority: "High"

    - id: "BR-003"
      rule: "Use native Read() tool, not Bash"
      trigger: "Reading source-tree.md"
      validation: "Read(file_path='devforgeai/specs/context/source-tree.md')"
      error_handling: "Token-efficient native tool usage"
      test_requirement: "Test: No Bash(command='cat source-tree.md') in spec"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "source-tree.md reading adds minimal overhead"
      metric: "< 500ms additional latency per test generation"
      test_requirement: "Test: Time test generation with and without validation"
      priority: "Low"

    - id: "NFR-002"
      category: "Reliability"
      requirement: "Validation prevents 100% of source-tree.md violations"
      metric: "Zero test files created in wrong directories"
      test_requirement: "Test: Attempt wrong path, verify blocked"
      priority: "Critical"
```

---

## Technical Limitations

```yaml
technical_limitations: []
# No known limitations for this enhancement
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- source-tree.md reading: < 500ms overhead
- Path validation: < 100ms per test file

### Security

**No Security Impact:**
- Read-only operation on source-tree.md
- No new external dependencies

### Reliability

**Error Handling:**
- Clear HALT messages with actionable guidance
- No silent failures or partial validations

---

## Dependencies

### Prerequisite Stories

None - this is an independent enhancement to test-automator.

### External Dependencies

- source-tree.md must exist at `devforgeai/specs/context/source-tree.md`
- Pattern relies on source-tree.md having documented test directory locations

### Technology Dependencies

- Claude Code Terminal Read() tool (native, no external packages)
- Markdown editing (no language-specific code)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 100% of new validation logic

**Test Scenarios:**
1. **Happy Path:** Module in `installer/` → tests go to `installer/tests/`
2. **Happy Path:** Module in `.claude/` → tests go to appropriate location per source-tree.md
3. **Error Case:** Attempted path `tests/installer/` → HALT with error
4. **Edge Case:** Module not defined in source-tree.md → default pattern applied
5. **Edge Case:** source-tree.md missing → HALT with "Run /create-context first"

**Test File Location:** `tests/STORY-203/test-source-tree-validation.sh`

---

### Integration Tests

**Coverage Target:** Verify end-to-end path enforcement

**Test Scenarios:**
1. Create test story for installer module
2. Run `/dev STORY-X`
3. Verify tests generated in `installer/tests/` (correct)
4. Verify no files in `tests/installer/` (wrong location blocked)

---

## Acceptance Criteria Verification Checklist

### AC#1: source-tree.md Reading Step Added

- [ ] Step 4.5 added to Phase 2 workflow - **Phase:** 3 - **Evidence:** test-automator.md diff
- [ ] Read() call for source-tree.md present - **Phase:** 3 - **Evidence:** grep verification
- [ ] Step positioned correctly (after Step 4, before Step 5) - **Phase:** 3 - **Evidence:** line number check

### AC#2: Test Directory Extraction from source-tree.md

- [ ] Extraction logic documented - **Phase:** 3 - **Evidence:** Step 4.5 content
- [ ] installer/tests/ pattern recognized - **Phase:** 5 - **Evidence:** test output
- [ ] Default pattern for undefined modules - **Phase:** 5 - **Evidence:** test output

### AC#3: Test Path Validation Before Write

- [ ] Validation loop over planned paths - **Phase:** 3 - **Evidence:** Step 4.5 content
- [ ] HALT pattern for violations - **Phase:** 3 - **Evidence:** grep "HALT" in step
- [ ] Validation before Write() confirmed - **Phase:** 5 - **Evidence:** execution log

### AC#4: Error Message with Fix Guidance

- [ ] Error message template defined - **Phase:** 3 - **Evidence:** Step 4.5 content
- [ ] Expected/attempted locations shown - **Phase:** 5 - **Evidence:** error output
- [ ] source-tree.md excerpt included - **Phase:** 5 - **Evidence:** error output

### AC#5: References Section Updated

- [ ] source-tree.md added to References - **Phase:** 3 - **Evidence:** grep verification

---

**Checklist Progress:** 0/13 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] Step 4.5 added to test-automator.md Phase 2 workflow
- [ ] Step reads source-tree.md using native Read() tool
- [ ] Test directory extraction logic implemented
- [ ] Path validation loop with HALT pattern implemented
- [ ] Error message template with fix guidance defined
- [ ] source-tree.md added to References section

### Quality
- [ ] All 5 acceptance criteria have passing tests
- [ ] Edge cases covered (missing source-tree.md, undefined modules)
- [ ] No Bash commands for file operations (native tools only)
- [ ] HALT messages provide actionable guidance

### Testing
- [ ] Unit tests for path validation logic
- [ ] Integration test with sample installer story
- [ ] Regression test for existing test-automator functionality

### Documentation
- [ ] Step 4.5 includes "Why This Step" rationale
- [ ] References section updated with source-tree.md
- [ ] RCA-017 reference noted in change log

---

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-01 12:00 | claude/devforgeai-story-creation | Created | Story created from RCA-017 REC-1 | STORY-203-test-automator-source-tree-validation.story.md |

## Notes

**Design Decisions:**
- Validation occurs BEFORE Write() calls (proactive enforcement)
- Uses native Read() tool per tech-stack.md constraints (lines 196-211)
- HALT pattern follows architecture-constraints.md error handling pattern (lines 116-132)

**Source RCA:**
- RCA-017: test-automator Source Tree Constraint Violation
- Recommendation: REC-1 (CRITICAL priority)
- Expected Impact: Prevents future source-tree.md violations by test-automator

**Related Evidence:**
- STORY-077 created tests in `tests/installer/` (wrong location)
- STORY-078 QA discovered violation (reactive)
- source-tree.md line 395-397 defines `installer/tests/` as correct location

**Architecture Compliance:**
- Follows Context File Enforcement pattern (architecture-constraints.md lines 81-100)
- Uses Markdown documentation only (no executable code per source-tree.md lines 471, 608)
- Native tools over Bash (anti-patterns.md Category 1)

---

**Story Template Version:** 2.5
**Last Updated:** 2026-01-01
