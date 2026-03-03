# Plan: STORY-130 - Delegate Artifact Verification to /ideate Skill

**Created:** 2025-12-23
**Status:** Planning Phase
**Story ID:** STORY-130
**Type:** Skill Refactoring / Test Generation

---

## Objective

Generate comprehensive failing tests (TDD Red phase) for STORY-130: "Delegate Artifact Verification to /ideate Skill"

This story removes Phase 3 artifact verification code from the `/ideate` command and delegates it entirely to the `discovering-requirements` skill's Phase 6.4 self-validation.

---

## Story Summary

**What:** Remove artifact verification logic from `.claude/commands/ideate.md` Phase 3
**Why:** Violates Single Responsibility Principle; skill should validate its own outputs
**How:** Delete Phase 3 verification code, rely on skill Phase 6.4 validation instead
**Impact:** Reduce command file from 554 lines to ~200 lines target

---

## Acceptance Criteria (from User Request)

### AC#1: Phase 3 Verification Code Removed from /ideate Command
- Grep for Phase 3 verification patterns should return NO matches
- Patterns to verify removed:
  - "## Phase 3"
  - "Verify Skill Completion"
  - "epic_files ="
  - "req_files ="
  - "len(epic_files)"
  - "artifacts not found"
  - "YAML validity"
  - "ID format"
  - "required field"

### AC#2: Command Delegates Validation to Skill Phase 6.4
- Command invokes skill without pre-validation or post-validation
- No YAML syntax checks in command file
- No ID format validation in command file
- No required field checks in command file

### AC#3: Skill Validation Failure Halts Command with Clear Error
- When skill reports validation failure, command outputs "HALT:" prefix
- Error message includes artifact name
- Error message includes failure reason

### AC#4: Command Line Count Reduced to Target
- `wc -l ideate.md` returns ≤200 lines (target)
- At minimum, line count reduced from 554 by ~55 lines (Phase 3 removal)

### AC#5: All Artifacts Still Verified Despite Validation Removal
- Epic documents meet quality standards
- Requirements specs meet quality standards
- Validation occurs via skill Phase 6.4

---

## Test Strategy

### Test Framework
- **Bash shell scripts** (DevForgeAI framework uses shell-based testing)
- Location: `devforgeai/tests/STORY-130/`
- Execution: `bash test-*.sh`
- Exit codes: 0 = pass, non-zero = fail

### Test Files to Create (TDD Red - All Should Fail Initially)

1. **test-ac1-phase3-removed.sh** (AC#1)
   - Grep for Phase 3 patterns in ideate.md
   - Verify all patterns removed (0 matches expected)
   - Tests: 8 sub-tests (one per pattern)

2. **test-ac2-delegation.sh** (AC#2)
   - Grep for validation logic in command
   - Verify no YAML checks, ID format checks, field checks
   - Tests: 3 sub-tests (one per check type)

3. **test-ac3-error-handling.sh** (AC#3)
   - Parse skill output for "HALT:" prefix
   - Verify error includes artifact name
   - Verify error includes failure reason
   - Tests: 3 sub-tests (one per requirement)

4. **test-ac4-line-count.sh** (AC#4)
   - Count lines in ideate.md
   - Verify ≤200 lines (target)
   - Verify reduction of ~55 lines from baseline
   - Tests: 2 sub-tests (target + reduction)

5. **test-ac5-quality-maintained.sh** (AC#5)
   - Verify skill Phase 6.4 exists
   - Verify skill validation logic present
   - Verify artifacts meet quality standards
   - Tests: 3 sub-tests (existence + logic + quality)

### Test Design Pattern

Each test follows AAA pattern:

```bash
#!/bin/bash

# test-acX-description.sh
# AC#X: Test description

set -e
TEST_COUNT=0
PASS_COUNT=0
FAIL_COUNT=0

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

test_case() {
    local description="$1"
    local command="$2"

    TEST_COUNT=$((TEST_COUNT + 1))

    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}PASS${NC}: $description"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo -e "${RED}FAIL${NC}: $description"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
}

# Test cases here

echo ""
echo "Results: $PASS_COUNT/$TEST_COUNT passed"
exit $FAIL_COUNT
```

---

## Test Execution Plan

### Phase 01: Pre-Flight Validation
- [ ] Verify STORY-130 story file exists (or create from requirements)
- [ ] Validate ideate.md file exists and is readable
- [ ] Load tech-stack.md to confirm Bash testing framework
- [ ] Verify test directory structure: `devforgeai/tests/STORY-130/`

### Phase 02: Test-First Design (TDD Red)
- [ ] Create test-ac1-phase3-removed.sh - Generate FAILING tests
- [ ] Create test-ac2-delegation.sh - Generate FAILING tests
- [ ] Create test-ac3-error-handling.sh - Generate FAILING tests
- [ ] Create test-ac4-line-count.sh - Generate FAILING tests
- [ ] Create test-ac5-quality-maintained.sh - Generate FAILING tests
- [ ] Run all tests to verify they FAIL (RED phase)
- [ ] Document test results

### Phase 03: Implementation (TDD Green)
- [ ] Remove Phase 3 code from ideate.md
- [ ] Update command to delegate to skill Phase 6.4
- [ ] Add error handling for "HALT:" output
- [ ] Re-run tests until all PASS (GREEN phase)

### Phase 04: Refactoring
- [ ] Code review of modified ideate.md
- [ ] Extract common error handling patterns
- [ ] Update documentation
- [ ] Light QA validation

### Phase 05: Integration Testing
- [ ] Execute full ideate workflow
- [ ] Verify skill Phase 6.4 validation works
- [ ] Test error scenarios (corrupted YAML, missing fields)
- [ ] Verify line count reduction meets target

### Phase 06: Deferral Challenge
- [ ] Review any incomplete items
- [ ] Validate with user if deferrals needed

### Phase 07: DoD Update & Phase 08: Git Commit
- [ ] Update story Definition of Done
- [ ] Commit changes with appropriate message

---

## Dependencies

### Files to Reference
- **ideate.md** - Command file to be refactored (`.claude/commands/ideate.md`)
- **discovering-requirements SKILL.md** - Skill Phase 6.4 self-validation
- **tech-stack.md** - Confirm testing framework
- **source-tree.md** - Test file location constraints

### Subagents to Invoke
- **test-automator** (Phase 02: Generate failing tests)
- **backend-architect** or equivalent (Phase 03: Remove verification code)
- **code-reviewer** (Phase 04: Review refactoring)
- **integration-tester** (Phase 05: Full workflow testing)

### Quality Gates
- [ ] All tests RED initially (TDD Phase 1)
- [ ] All tests GREEN after implementation (TDD Phase 2)
- [ ] Light QA passes (Phase 04)
- [ ] Integration tests pass (Phase 05)
- [ ] Line count ≤200 (AC#4)
- [ ] No anti-pattern violations

---

## Success Criteria Checklist

- [ ] All 5 test files created and executable
- [ ] All tests FAIL initially (TDD Red phase verified)
- [ ] Tests follow Bash shell testing patterns
- [ ] Tests use clear PASS/FAIL output format
- [ ] Tests are independent (no execution order dependencies)
- [ ] Tests follow AAA pattern (Arrange, Act, Assert)
- [ ] Test location respects source-tree.md constraints
- [ ] All AC verified by at least one test
- [ ] Code comments explain complex test logic
- [ ] Exit codes correct (0 = pass, non-zero = fail)

---

## Token Budget

**Estimated token usage for full workflow:**
- Phase 02 (Test Generation): ~15K tokens (test-automator)
- Phase 03 (Implementation): ~10K tokens (code modification)
- Phase 04 (Refactoring): ~8K tokens (code-reviewer)
- Phase 05 (Integration): ~10K tokens (integration-tester)
- Total: ~43K tokens (within budget)

---

## Next Steps

1. **Resume Point:** After plan approval
2. **Action:** Invoke `devforgeai-development` skill with STORY-130
3. **Workflow:** Execute Phases 01-10 as defined in skill documentation
4. **Output:** Failing test suite ready for implementation

---

## References

### Framework Documentation
- CLAUDE.md - Project instructions
- `.claude/skills/devforgeai-development/SKILL.md` - Development skill phases
- `.claude/memory/skills-reference.md` - Skill invocation patterns
- devforgeai/specs/context/source-tree.md - Test file locations
- devforgeai/specs/context/tech-stack.md - Testing framework specification

### Related Stories
- STORY-031: Wire hooks into /ideate command
- STORY-055: discovering-requirements skill integration

### Test Patterns
- `.claude/skills/devforgeai-development/references/tdd-red-phase.md` - Test generation guidance
- `.claude/skills/devforgeai-development/references/tdd-patterns.md` - TDD best practices

---

## Plan Approval

**Status:** Ready for execution
**Awaiting:** User confirmation to proceed with devforgeai-development skill invocation

