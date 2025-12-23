# STORY-127: Plan File Resume Convention - Test Suite

**Status**: RED Phase (All tests failing - TDD)
**Test Framework**: Bash (native to DevForgeAI)
**Total Tests**: 31 across 5 test files
**Test Location**: `/mnt/c/Projects/DevForgeAI2/devforgeai/tests/STORY-127/`

---

## Quick Start

### Run All Tests
```bash
cd /mnt/c/Projects/DevForgeAI2

# Run all 5 test files
bash devforgeai/tests/STORY-127/test-ac1-claude-md-section.sh
bash devforgeai/tests/STORY-127/test-ac2-phase0-search.sh
bash devforgeai/tests/STORY-127/test-ac3-story-id-priority.sh
bash devforgeai/tests/STORY-127/test-ac4-new-plan-naming.sh
bash devforgeai/tests/STORY-127/test-ac5-backward-compat.sh
```

### Run with Exit Code Check
```bash
for test in devforgeai/tests/STORY-127/test-*.sh; do
  bash "$test"
  if [ $? -ne 0 ]; then
    echo "$(basename $test): FAILED"
  else
    echo "$(basename $test): PASSED"
  fi
done
```

---

## Test Files

### 1. test-ac1-claude-md-section.sh
**Acceptance Criteria**: AC#1 - CLAUDE.md Includes Plan File Convention Section
**Test Cases**: 5
**Status**: FAILING ✗

Verifies that CLAUDE.md contains:
- Plan File Convention section header
- Documentation of checking for existing plans
- Search algorithm documentation (glob + grep)
- Naming convention with story ID
- Resume vs create decision logic

**Run**:
```bash
bash devforgeai/tests/STORY-127/test-ac1-claude-md-section.sh
```

---

### 2. test-ac2-phase0-search.sh
**Acceptance Criteria**: AC#2 - /dev Phase 0 Checks for Existing Plans
**Test Cases**: 6
**Status**: FAILING ✗

Verifies that devforgeai-development SKILL.md Phase 0 includes:
- Plan file search logic in preflight validation
- Glob pattern to list `.claude/plans/*.md`
- Grep pattern to find story ID in files
- Resume prompt text documentation
- AskUserQuestion for user interaction
- Search executes BEFORE creating new plan

**Run**:
```bash
bash devforgeai/tests/STORY-127/test-ac2-phase0-search.sh
```

---

### 3. test-ac3-story-id-priority.sh
**Acceptance Criteria**: AC#3 - Plan Files with Story ID Are Prioritized
**Test Cases**: 6
**Status**: FAILING ✗

Verifies that:
- Prioritization strategy is documented
- Random-named files are deprioritized
- Story ID files are prioritized in search results
- Word boundary matching prevents false positives (STORY-11 vs STORY-114)
- Multiple matches are handled gracefully
- Practical algorithm correctly categorizes matches

**Run**:
```bash
bash devforgeai/tests/STORY-127/test-ac3-story-id-priority.sh
```

---

### 4. test-ac4-new-plan-naming.sh
**Acceptance Criteria**: AC#4 - New Plans Use Story ID in Filename
**Test Cases**: 7
**Status**: FAILING ✗

Verifies that:
- CLAUDE.md documents story ID naming convention
- Good vs bad naming examples are contrasted
- Random adjective-noun combinations are avoided
- Phase 0 creates new plans with story ID in filename
- Naming pattern is documented (STORY-XXX-description.md)
- Regex validation confirms pattern compliance
- Exception documented for exploratory work (optional)

**Run**:
```bash
bash devforgeai/tests/STORY-127/test-ac4-new-plan-naming.sh
```

---

### 5. test-ac5-backward-compat.sh
**Acceptance Criteria**: AC#5 - Backward Compatibility
**Test Cases**: 7
**Status**: FAILING ✗

Verifies that:
- Backward compatibility is explicitly documented
- Random-named files with story ID are detected
- No errors occur with mixed naming conventions
- Search algorithm handles both naming styles
- STORY-114 scenario (multiple random plans) is addressed
- Practical detection works with mixed fixtures
- Resume prompt works with random-named files

**Run**:
```bash
bash devforgeai/tests/STORY-127/test-ac5-backward-compat.sh
```

---

## Test Design

### Testing Approach

1. **Documentation Testing** (80% of tests)
   - Verify sections exist in CLAUDE.md
   - Check for required keywords in documentation
   - Validate pattern descriptions

2. **Logic Testing** (15% of tests)
   - Verify algorithm behavior
   - Test prioritization order
   - Validate naming patterns with regex

3. **Practical Testing** (5% of tests)
   - Create test fixtures with real files
   - Test actual grep/glob patterns
   - Verify detection works end-to-end

### Test Fixtures

Some tests create temporary directories and files to validate logic:

- **test-ac3-story-id-priority.sh**: Creates STORY-127-plan-file-resume.md, clever-snuggling-otter.md, enchanted-booping-pizza.md
- **test-ac5-backward-compat.sh**: Creates mix of old random-named and new STORY-XXX files

All fixtures are cleaned up automatically after test completion.

---

## Test Results Summary

### Current Status (RED Phase)

```
Test Suite: STORY-127 Plan File Resume Convention
Framework: Bash
Status: ALL TESTS FAILING (as expected in RED phase)

test-ac1-claude-md-section.sh:     0 passed, 5 failed
test-ac2-phase0-search.sh:         0 passed, 6 failed
test-ac3-story-id-priority.sh:     0 passed, 6 failed
test-ac4-new-plan-naming.sh:       0 passed, 7 failed
test-ac5-backward-compat.sh:       0 passed, 7 failed

TOTAL:                             0 passed, 31 failed
```

### Success Criteria (GREEN Phase)

All tests will pass when implementation includes:

1. **CLAUDE.md additions** (~40 lines)
   - New section: `## Plan File Convention`
   - Document detection algorithm
   - Document naming convention
   - Document resume logic

2. **SKILL.md additions** (~50 lines)
   - Phase 01 (Pre-Flight) plan file search
   - Glob + Grep patterns
   - AskUserQuestion integration
   - Prioritization logic

---

## Implementation Checklist

### For Implementation Phase

- [ ] Add Plan File Convention section to CLAUDE.md
- [ ] Document search algorithm (Glob + Grep)
- [ ] Document naming convention (STORY-XXX-description.md)
- [ ] Document good vs bad naming examples
- [ ] Document resume vs create decision
- [ ] Add plan file search to devforgeai-development SKILL.md Phase 01
- [ ] Implement Glob pattern for `.claude/plans/*.md`
- [ ] Implement Grep with word boundary matching
- [ ] Implement prioritization logic (name match > content match)
- [ ] Implement resume prompt with AskUserQuestion
- [ ] Ensure backward compatibility with random-named files
- [ ] Add error handling for edge cases

### For Testing Phase

- [ ] Run all 31 tests
- [ ] Verify all tests pass (GREEN phase)
- [ ] Verify no false positives in detection
- [ ] Test with STORY-114 existing plan files
- [ ] Test with new STORY-127 naming convention
- [ ] Test prioritization order
- [ ] Test word boundary matching (STORY-11 vs STORY-114)

---

## File Paths

### Test Files
- AC#1: `/mnt/c/Projects/DevForgeAI2/devforgeai/tests/STORY-127/test-ac1-claude-md-section.sh`
- AC#2: `/mnt/c/Projects/DevForgeAI2/devforgeai/tests/STORY-127/test-ac2-phase0-search.sh`
- AC#3: `/mnt/c/Projects/DevForgeAI2/devforgeai/tests/STORY-127/test-ac3-story-id-priority.sh`
- AC#4: `/mnt/c/Projects/DevForgeAI2/devforgeai/tests/STORY-127/test-ac4-new-plan-naming.sh`
- AC#5: `/mnt/c/Projects/DevForgeAI2/devforgeai/tests/STORY-127/test-ac5-backward-compat.sh`

### Documentation
- Summary: `/mnt/c/Projects/DevForgeAI2/devforgeai/tests/STORY-127/TEST-SUITE-SUMMARY.md`
- README: `/mnt/c/Projects/DevForgeAI2/devforgeai/tests/STORY-127/README.md` (this file)

### Story File
- Spec: `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-127-plan-file-resume.story.md`

### Files to Modify
- CLAUDE.md: `/mnt/c/Projects/DevForgeAI2/CLAUDE.md`
- SKILL.md: `/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-development/SKILL.md`

---

## Test Framework Details

### Bash Testing Pattern

All tests follow this structure:

```bash
#!/bin/bash
set -euo pipefail

# Setup
TEST_NAME="Test name"
TEST_PASSED=0
TEST_FAILED=0

# Test case function
test_case_name() {
  echo "Test description"
  if [ condition ]; then
    echo "✓ PASS"
    ((TEST_PASSED++))
  else
    echo "✗ FAIL"
    ((TEST_FAILED++))
  fi
}

# Execution
test_case_name
# ... more test cases ...

# Summary
if [[ $TEST_FAILED -gt 0 ]]; then
  exit 1  # FAILED
else
  exit 0  # PASSED
fi
```

### Color Output

- `GREEN`: ✓ PASS
- `RED`: ✗ FAIL
- `YELLOW`: Test description header
- `NC`: Color reset

### Running Tests with Unix Line Endings

Some systems require line ending conversion:

```bash
# If scripts have Windows line endings (CRLF):
dos2unix devforgeai/tests/STORY-127/*.sh

# Then run:
bash devforgeai/tests/STORY-127/test-ac1-claude-md-section.sh
```

---

## Troubleshooting

### Test Fails with "command not found"
**Cause**: Windows line endings (CRLF) in script
**Fix**:
```bash
dos2unix devforgeai/tests/STORY-127/*.sh
```

### Test Fails with "file not found"
**Cause**: Working directory not set correctly
**Fix**:
```bash
cd /mnt/c/Projects/DevForgeAI2
bash devforgeai/tests/STORY-127/test-ac1-claude-md-section.sh
```

### Test Passes but Implementation Not Working
**Cause**: Test verifies documentation, not actual functionality
**Note**: Tests check that requirements are documented. Implementation phase will create the actual logic.

---

## Links

- **Story File**: [STORY-127-plan-file-resume.story.md](../../../devforgeai/specs/Stories/STORY-127-plan-file-resume.story.md)
- **Full Test Summary**: [TEST-SUITE-SUMMARY.md](TEST-SUITE-SUMMARY.md)
- **Framework**: [Claude Code Terminal](https://docs.claude.com/en/docs/claude-code/)
- **Coding Standards**: [devforgeai/specs/context/coding-standards.md](../../../devforgeai/specs/context/coding-standards.md)

---

## Generated

- **Date**: 2025-12-23
- **Generator**: test-automator (TDD Red Phase)
- **Framework**: Bash (native to DevForgeAI)
- **Status**: RED Phase - All tests failing as expected
- **Next Phase**: Implementation (GREEN) - Write code to pass tests

---

**For detailed information about each test case, see [TEST-SUITE-SUMMARY.md](TEST-SUITE-SUMMARY.md)**
