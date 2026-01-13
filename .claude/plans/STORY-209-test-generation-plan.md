# STORY-209: Document Phase Resumption Protocol - Test Generation Plan

**Story ID**: STORY-209
**Story Title**: Document Phase Resumption Protocol for Interrupted Workflows
**Test Type**: Documentation Specification Tests (Bash/Grep validation)
**Status**: Test Generation Complete (TDD Red Phase)

---

## Overview

This plan tracks the test generation process for STORY-209, which documents how users and Claude can detect and recover from interrupted /dev workflows.

The story implements documentation for:
1. How users detect workflow interruptions
2. Recovery commands users can run
3. Steps Claude follows to resume workflows
4. Pre-flight validation checklist
5. Decision guidance (fresh start vs resume)

---

## Acceptance Criteria Under Test

### AC#1: User Detection Indicators Documented
- [ ] Section "User Detection Indicators" exists in SKILL.md
- [ ] Includes TodoWrite status indicator (pending/in_progress)
- [ ] Includes DoD completion percentage indicator
- [ ] Includes story status update indicator
- [ ] Includes git commit detection indicator

**Test Coverage**: 5 tests (AC#1.1 through AC#1.5)
**Current Status**: 2/5 passing, 3/5 failing

### AC#2: User Recovery Command Documented
- [ ] Section "User Recovery Command" exists
- [ ] Contains code block with template command
- [ ] References pending phases list
- [ ] Includes "Resume execution now" action phrase

**Test Coverage**: 4 tests (AC#2.1 through AC#2.4)
**Current Status**: 1/4 passing, 3/4 failing

### AC#3: Claude Resumption Steps Documented
- [ ] Section "Claude Resumption Steps" exists
- [ ] Step 1: Check TodoWrite State
- [ ] Step 2: Verify Previous Phases
- [ ] Step 3: Load Phase Reference
- [ ] Step 4: Execute Remaining Phases
- [ ] Step 5: Final Validation
- [ ] 6 total numbered steps documented

**Test Coverage**: 7 tests (AC#3.1 through AC#3.7)
**Current Status**: 6/7 passing, 1/7 failing

### AC#4: Resumption Validation Checklist
- [ ] Checklist section exists
- [ ] User confirmed resumption item
- [ ] Previous phases completion evidence item
- [ ] No conflicting git changes item
- [ ] Story file readable item

**Test Coverage**: 5 tests (AC#4.1 through AC#4.5)
**Current Status**: 3/5 passing, 2/5 failing

### AC#5: Fresh Start vs Resume Recommendation
- [ ] Decision guidance section exists
- [ ] "Start fresh" recommendation documented
- [ ] Recommendation for unclear state
- [ ] Table/matrix format with scenarios

**Test Coverage**: 4 tests (AC#5.1 through AC#5.4)
**Current Status**: 1/4 passing, 3/4 failing

---

## Test File Details

### File Location
```
/mnt/c/Projects/DevForgeAI2/tests/STORY-209-phase-resumption-protocol-tests.sh
```

### File Structure
- **Total tests**: 25
- **Test framework**: Bash with grep/pattern validation
- **Test pattern**: Documentation specification validation
- **Pass rate (initial)**: 13/25 (52%) - TDD Red Phase expected

### Test Execution
```bash
chmod +x /mnt/c/Projects/DevForgeAI2/tests/STORY-209-phase-resumption-protocol-tests.sh
/mnt/c/Projects/DevForgeAI2/tests/STORY-209-phase-resumption-protocol-tests.sh
```

### Test Output Format
- Color-coded output (GREEN pass, RED fail, YELLOW test marker)
- Detailed failure reasons for debugging
- Summary statistics (tests run, passed, failed)
- Actionable guidance for missing sections

---

## Helper Functions in Test File

| Function | Purpose | Example |
|----------|---------|---------|
| `test_start()` | Mark test as started | `test_start "AC#1.1: Section exists"` |
| `test_pass()` | Record passing test | `test_pass "AC#1.1: Section exists"` |
| `test_fail()` | Record failing test with reason | `test_fail "AC#1.1" "Section header not found"` |
| `section_exists()` | Check if Markdown section header exists | `section_exists "User Detection" "$TARGET_FILE"` |
| `contains_pattern()` | Case-insensitive pattern match | `contains_pattern "pending\|in_progress" "$FILE"` |
| `contains_text()` | Case-sensitive text match | `contains_text "exact text" "$FILE"` |
| `count_matches()` | Count matching lines | `count_matches "pattern" "$FILE"` |

---

## Current Test Results (TDD Red Phase)

```
Tests run:     25
Tests passed:  13
Tests failed:  12

Failure Summary by AC:
- AC#1: 3 failures (DoD completion, git commits, section header)
- AC#2: 3 failures (section header, template, action phrase)
- AC#3: 1 failure (section header - content already present in SKILL.md)
- AC#4: 2 failures (user confirmation, file readability)
- AC#5: 3 failures (section header, fresh start recommendation, unclear state)

Total failures: 12/25 (48%)
```

---

## Implementation Tasks (TDD Green Phase)

To make all tests pass, add these sections to `.claude/skills/devforgeai-development/SKILL.md`:

### Task 1: Add User Detection Indicators Section
**Location**: SKILL.md, after "Phase Orchestration Loop" section
**Content to add**:
- Section header: `## User Detection Indicators`
- List of 5 indicators:
  1. TodoWrite list shows phases as "pending" or "in_progress"
  2. DoD completion <100% but workflow declared complete
  3. Story status not updated to expected value
  4. No git commit of story file
  5. Phase state file timestamp doesn't match current session

**Tests fixed**: AC#1.1, AC#1.3, AC#1.5

### Task 2: Add User Recovery Command Section
**Location**: SKILL.md, after User Detection Indicators
**Content to add**:
- Section header: `## User Recovery Command`
- Code block with template:
  ```
  Continue /dev workflow for STORY-XXX from Phase Y

  Pending phases: Phase Y, Phase Y+1, ..., Phase 10

  Resume execution now: /dev STORY-XXX --resume
  ```

**Tests fixed**: AC#2.1, AC#2.2, AC#2.4

### Task 3: Add Claude Resumption Steps Section
**Location**: SKILL.md, after User Recovery Command
**Content to add**:
- Section header: `## Claude Resumption Steps`
- 6 numbered steps:
  1. Check TodoWrite State
  2. Verify Previous Phases
  3. Load Phase Reference
  4. Execute Remaining Phases
  5. Final Validation
  6. Record Resumption in Changelog

**Tests fixed**: AC#3.1

### Task 4: Add Resumption Validation Checklist
**Location**: SKILL.md, after Claude Resumption Steps
**Content to add**:
- Section header: `## Resumption Pre-Flight Checklist`
- Checklist items:
  - [ ] User confirmed resumption intent
  - [ ] Previous phases have completion evidence
  - [ ] No conflicting git changes
  - [ ] Story file exists and is readable
  - [ ] Phase state file is not corrupted

**Tests fixed**: AC#4.2, AC#4.5

### Task 5: Add Fresh Start vs Resume Decision Matrix
**Location**: SKILL.md, after Resumption Validation Checklist
**Content to add**:
- Section header: `## Fresh Start vs Resume Decision Matrix`
- Table with:
  - Column 1: Scenario
  - Column 2: Condition
  - Column 3: Recommendation
  - Rows include:
    - Workflow interrupted cleanly → Resume
    - Phase state file corrupted → Start fresh
    - Git conflicts detected → Start fresh
    - State unclear → Start fresh
    - All previous phases completed → Resume

**Tests fixed**: AC#5.1, AC#5.2, AC#5.3

---

## Test Validation Strategy

### TDD Red Phase (Current)
1. Write failing tests (✓ Complete - 12 failures)
2. Tests validate that documentation sections don't exist yet
3. Tests provide clear feedback on what to implement

### TDD Green Phase (Next)
1. Implement documentation sections in SKILL.md
2. Run tests to verify sections are added correctly
3. All 25 tests should pass

### TDD Refactor Phase
1. Review documentation clarity and completeness
2. Improve examples and guidance
3. Add cross-references to related sections
4. Ensure consistency with other workflow documentation

---

## Pattern Detection Strategy

The tests use grep patterns to validate documentation structure:

| AC | Validation Pattern | Rationale |
|----|--------------------|-----------|
| AC#1.1 | `grep -qiE "^(#{1,4}) .*(User Detection)"` | Validates section header |
| AC#1.2 | `grep -qi "TodoWrite.*pending\|in_progress"` | Validates indicator mention |
| AC#1.3 | `grep -qi "DoD.*completion\|100%"` | Validates DoD completion check |
| AC#2.1 | `grep -qiE "^(#{1,4}) .*(User Recovery)"` | Validates section header |
| AC#2.2 | `grep -qi "Continue.*\/dev\|Resume.*execution"` | Validates command template |
| AC#3.1 | `grep -qiE "^(#{1,4}) .*(Claude Resumption)"` | Validates section header |
| AC#4.1 | `grep -qi "checklist\|pre-flight"` | Validates checklist section |
| AC#5.1 | `grep -qi "fresh.*start\|decision.*matrix"` | Validates decision guidance |

---

## Dependencies

- **Target file**: `.claude/skills/devforgeai-development/SKILL.md`
- **Test framework**: Bash (no external dependencies)
- **Pattern tool**: Grep (standard Unix utility)
- **Line endings**: LF (per tech-stack.md WSL compatibility rules)

---

## Success Criteria

- [x] Test file created and executable
- [x] All 25 tests run successfully
- [x] Tests produce clear failure messages
- [x] TDD Red phase confirmed (12/25 failing)
- [ ] All documentation sections added (TDD Green - not yet done)
- [ ] All tests passing (TDD Green - not yet done)
- [ ] Documentation complete and clear (TDD Refactor - not yet done)

---

## Next Steps

1. **Immediate**: Run tests to confirm TDD Red phase (✓ Done)
2. **Phase 02 (Green)**: Implement documentation sections
3. **Phase 04 (Refactor)**: Improve clarity and consistency
4. **Phase 07**: Update Definition of Done with documentation updates
5. **Phase 08**: Commit changes with conventional message

---

## References

- **Test file**: `/mnt/c/Projects/DevForgeAI2/tests/STORY-209-phase-resumption-protocol-tests.sh`
- **Target**: `.claude/skills/devforgeai-development/SKILL.md`
- **Test framework**: Bash documentation validation
- **Framework**: DevForgeAI TDD workflow (Red → Green → Refactor)

---

## Change Log

| Date | Event | Details |
|------|-------|---------|
| 2026-01-13 | Test generation | 25 tests created, 13/25 passing (TDD Red phase) |
| 2026-01-13 | Plan creation | Plan document created for tracking implementation |

