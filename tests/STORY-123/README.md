# STORY-123: Uncommitted Story File Warning - Test Suite

## Overview

Comprehensive test suite for STORY-123: Uncommitted Story File Warning, implementing Preflight Step 1.8 to detect uncommitted story files and warn developers about potential conflicts.

**Test Status:** RED PHASE (All tests fail - no implementation yet)

**Framework:** Bash shell scripting with AAA (Arrange-Act-Assert) pattern

**Total Tests:** 15
- Unit Tests: 4
- Integration Tests: 6
- Edge Cases: 5

---

## Test Organization

### Test Files

#### 1. `test-unit-git-parsing.sh` (4 tests)
**Purpose:** Unit tests for fundamental git status parsing logic

| Test | AC | Purpose | Assertion |
|------|-------|---------|-----------|
| **Test 1** | AC#1 | Parse git status for .story.md files | Extract .story.md files from git output |
| **Test 2** | AC#1 | Extract story ID from file path | Convert `STORY-123-name.story.md` → `STORY-123` |
| **Test 3** | AC#2 | Separate current from other stories | Filter out current story from list |
| **Test 4** | AC#3 | Detect consecutive ranges | Identify ranges like 100-113, 115-119 |

**Run individually:**
```bash
bash tests/STORY-123/test-unit-git-parsing.sh
```

---

#### 2. `test-integration-warning-display.sh` (6 tests)
**Purpose:** Integration tests for warning display and user interaction

| Test | AC | Purpose | Assertion |
|------|-------|---------|-----------|
| **Test 5** | AC#2 | Warning shows current story | Display "Your story: STORY-114" |
| **Test 6** | AC#3 | Include count and ranges | Show "21 files" with "STORY-100 through STORY-113 (14 files)" |
| **Test 7** | AC#4 | User selects "Continue" option | Option available in AskUserQuestion |
| **Test 8** | AC#5 | DEVFORGEAI_STORY env var set | Export `DEVFORGEAI_STORY=STORY-114` |
| **Test 9** | AC#4 | "Commit first" option HALTs | Exit code 1 when selected |
| **Test 10** | AC#4 | "Show list" displays git status | Show full uncommitted story files |

**Run individually:**
```bash
bash tests/STORY-123/test-integration-warning-display.sh
```

---

#### 3. `test-edge-cases.sh` (5 tests)
**Purpose:** Edge case and boundary condition testing

| Test | Purpose | Scenario | Assertion |
|------|---------|----------|-----------|
| **Test 11** | Skip warning when no stories uncommitted | Clean working directory | No warning displayed |
| **Test 12** | Skip warning when only current story uncommitted | STORY-114 modified, no others | No warning displayed |
| **Test 13** | Format non-consecutive ranges correctly | STORY-100-105, STORY-110-115 | Two ranges detected |
| **Test 14** | Single other story (not range format) | Only STORY-115 uncommitted | Show "STORY-115" not "through" |
| **Test 15** | Performance with large story count | 100+ uncommitted stories | Process in <100ms |

**Run individually:**
```bash
bash tests/STORY-123/test-edge-cases.sh
```

---

### Master Test Runner

#### `run-all-tests.sh`
Orchestrates all three test suites and provides unified reporting

**Run all tests:**
```bash
bash tests/STORY-123/run-all-tests.sh
```

---

## Acceptance Criteria Coverage Matrix

| AC | Requirement | Tests | Coverage |
|----|-------------|-------|----------|
| **AC#1** | Detect uncommitted .story.md files via git status | Unit-1, Integration-5, Edge-11, Edge-12 | 100% |
| **AC#2** | Distinguish current vs other stories in warning | Unit-3, Integration-5 | 100% |
| **AC#3** | Show ranges with file counts (e.g., "STORY-100 through STORY-113 (14 files)") | Integration-6, Edge-13, Edge-14 | 100% |
| **AC#4** | Present 3 user options in AskUserQuestion | Integration-7, Integration-8, Integration-9, Integration-10 | 100% |
| **AC#5** | Set DEVFORGEAI_STORY env var (STORY-121 integration) | Integration-8 | 100% |

---

## Test Pattern: AAA (Arrange-Act-Assert)

All tests follow the AAA pattern for clarity:

```bash
test_example() {
    # Arrange: Set up test preconditions and data
    local git_status_output=" M devforgeai/specs/Stories/STORY-114.story.md"
    local current_story="STORY-114"

    # Act: Execute the behavior being tested
    local story_files=$(echo "$git_status_output" | grep '\.story\.md$')

    # Assert: Verify the outcome
    if [ -n "$story_files" ]; then
        echo "✅"
    else
        echo "❌ Did not find story file"
    fi
}
```

---

## Red Phase: Expected Behavior

All tests FAIL when run before implementation. This is correct behavior:

**RED PHASE (Current State):**
```
Test 1: Parse git status output for .story.md files
  ❌ FAILED (expected at RED phase)

Test 2: Extract story ID from file path
  ❌ FAILED (expected at RED phase)

... [all tests fail] ...

⚠️  RED PHASE: 15 test(s) failing (expected - implementation pending)
```

**Why Tests Fail Now:**
- No implementation code exists yet
- Preflight Step 1.8 not added to preflight-validation.md
- git status parsing logic not implemented
- Range detection algorithm not implemented
- Warning display function not implemented

**Next Phase (GREEN - Implementation):**
After implementation is added, tests will pass when you:
1. Add Step 1.8 to preflight-validation.md
2. Implement git status parsing
3. Implement range detection
4. Implement warning display
5. Integrate AskUserQuestion
6. Set DEVFORGEAI_STORY env var

---

## Implementation Guide

### File Locations

**Test Files Location:**
```
tests/STORY-123/
├── test-unit-git-parsing.sh           # 4 unit tests
├── test-integration-warning-display.sh # 6 integration tests
├── test-edge-cases.sh                 # 5 edge case tests
├── run-all-tests.sh                   # Master test runner
└── README.md                          # This file
```

**Implementation Locations:**
```
.claude/skills/devforgeai-development/
└── references/
    └── preflight-validation.md        # Add Step 1.8 here (after Step 1.7)
```

### Step 1.8 Implementation Pseudocode

```bash
# Step 1.8: Story File Isolation Check (NEW - STORY-123)

# Get current story ID from /dev argument
CURRENT_STORY=$1  # e.g., STORY-114

# Find all uncommitted .story.md files
UNCOMMITTED_STORIES=$(git status --porcelain | \
  grep '\.story\.md$' | \
  awk '{print $2}' | \
  sed 's|devforgeai/specs/Stories/STORY-||' | \
  sed 's|-.*||')

# Separate current vs other stories
OTHER_STORIES=$(echo "$UNCOMMITTED_STORIES" | \
  grep -v "^${CURRENT_STORY}$" || true)

OTHER_COUNT=$(echo "$OTHER_STORIES" | grep -c . || true)

# Only display warning if other stories exist (not current story only)
if [ "$OTHER_COUNT" -gt 0 ]; then
    # 1. Display warning with ranges
    # 2. Present AskUserQuestion with 3 options
    # 3. Handle user selection:
    #    a) Continue → export DEVFORGEAI_STORY env var
    #    b) Commit first → HALT workflow
    #    c) Show list → display git status
fi
```

### Implementation Checklist

- [ ] Add Step 1.8 heading to preflight-validation.md after Step 1.7
- [ ] Implement git status parsing (grep for .story.md, extract story IDs)
- [ ] Implement story separation logic (current vs other)
- [ ] Implement range detection (consecutive numbers: 100-113, 115-119)
- [ ] Implement warning display (box format with visual separation)
- [ ] Implement AskUserQuestion integration (3 options)
- [ ] Implement DEVFORGEAI_STORY env var setting (on "Continue")
- [ ] Implement HALT for "Commit other stories" option
- [ ] Implement "Show list" display
- [ ] Run all tests: `bash tests/STORY-123/run-all-tests.sh`
- [ ] All 15 tests should PASS (GREEN phase)

---

## Performance Requirements

Per AC Non-Functional Requirements:

| Requirement | Target | Test |
|-------------|--------|------|
| Detection latency | <100ms | Edge Case Test 15 |
| Accuracy | 100% for story file detection | All tests verify accuracy |
| User clarity | Clear visual separation | Integration Tests 5-6 |

---

## Dependencies & Integrations

### Depends On
- **STORY-121:** Uses DEVFORGEAI_STORY environment variable for scoped commits
- **Git:** Must have git available (checked by Phase 01 Step a: git-validator)

### Integration Points
- **preflight-validation.md:** Step 1.8 inserted into Phase 01 Pre-Flight Validation
- **devforgeai-development skill:** Invoked from Phase 01 pre-flight checks
- **AskUserQuestion:** Called to present 3 user options
- **DEVFORGEAI_STORY env var:** Set when user selects "Continue"

---

## Test Execution Patterns

### Run All Tests
```bash
bash tests/STORY-123/run-all-tests.sh
```

### Run Single Test Category
```bash
# Unit tests only
bash tests/STORY-123/test-unit-git-parsing.sh

# Integration tests only
bash tests/STORY-123/test-integration-warning-display.sh

# Edge case tests only
bash tests/STORY-123/test-edge-cases.sh
```

### Run Individual Test
Tests are organized by category. To run a specific test, modify the test file to comment out others:

```bash
# Edit test-unit-git-parsing.sh and comment out other tests
# Keep only the test you want to run
bash tests/STORY-123/test-unit-git-parsing.sh
```

### Expected Output Format

**RED Phase (Current):**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Test Results:
  Total Tests: 4
  Passed: 0
  Failed: 4
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  RED PHASE: 4 test(s) failing (expected - implementation pending)
```

**GREEN Phase (After Implementation):**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Test Results:
  Total Tests: 4
  Passed: 4
  Failed: 0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ All tests passed!
```

---

## Test Quality Metrics

### Coverage by Component

| Component | Tests | Coverage |
|-----------|-------|----------|
| Git Status Parsing | 1, 2 | 2/2 (100%) |
| Story Separation | 3, 5 | 2/2 (100%) |
| Range Detection | 4, 13, 14 | 3/3 (100%) |
| Warning Display | 5, 6 | 2/2 (100%) |
| User Interaction | 7, 8, 9, 10 | 4/4 (100%) |
| Edge Cases | 11, 12, 13, 14, 15 | 5/5 (100%) |

### Mutation Testing Readiness

Each test is designed to catch common mutations:
- **String mutations:** Test verifies exact story IDs and ranges
- **Logic mutations:** Test verifies separation logic and counting
- **Off-by-one errors:** Test verifies exact counts and ranges
- **Missing features:** Test verifies all 3 user options present

---

## Troubleshooting

### Test Fails Unexpectedly (Before Implementation)

**This is correct** - tests should fail during RED phase.

**Expected:** All 15 tests FAIL
**Actual:** Some tests FAIL, some PASS

**Possible causes:**
1. Partial implementation already exists
2. Mock functions in tests have syntax errors
3. Bash version incompatibility

**Solution:** Remove any partial implementation and re-run tests

### Test Cannot Find Fixtures

If tests fail looking for fixtures:
```bash
# Tests use temporary directories (mktemp)
# No external fixtures required
# All test data generated within test functions
```

### Git Status Parsing Issues

If git status parsing tests fail due to git not available:
```bash
# Tests use mock git output, not actual git
# Verify git is installed: git --version
# Tests should work on systems with git installed
```

---

## Test Maintenance

### Adding New Tests

To add a new test case:

1. Create test function following AAA pattern:
```bash
test_new_feature() {
    # Arrange
    local input_data="..."

    # Act
    local result=$()

    # Assert
    if [ condition ]; then
        echo "✅"
    else
        echo "❌ Expected X, got Y"
    fi
}
```

2. Add `run_test` invocation in execution section
3. Update test count in headers
4. Update AC coverage matrix
5. Document in README

### Test File Organization

Each test file is independent:
- Can be run in any order
- No shared state between files
- Can be run individually without others

### Version Control

Tests are committed to git as specification documentation:
- Tests should NOT change (they define spec)
- Only implementation code changes
- If spec changes, tests updated by story creation skill

---

## References

### Story Files
- **Story:** `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-123-uncommitted-story-file-warning.story.md`
- **Depends On:** STORY-121 (DEVFORGEAI_STORY env var)
- **Tech Spec:** Lines 70-128 of story file

### Skill Files
- **devforgeai-development:** `.claude/skills/devforgeai-development/SKILL.md`
- **Preflight Validation:** `.claude/skills/devforgeai-development/references/preflight/_index.md`

### Framework Documentation
- **Tech Stack:** `devforgeai/specs/context/tech-stack.md` (Bash scripting)
- **Source Tree:** `devforgeai/specs/context/source-tree.md` (test location: tests/)
- **Coding Standards:** `devforgeai/specs/context/coding-standards.md` (shell script patterns)

---

## Quick Start

### First Run (RED Phase)
```bash
# Navigate to project root
cd /mnt/c/Projects/DevForgeAI2

# Run all tests (all should fail)
bash tests/STORY-123/run-all-tests.sh

# Expected output: 15 tests FAIL (correct for RED phase)
```

### During Implementation (GREEN Phase)
```bash
# After implementing Step 1.8 in preflight-validation.md:
bash tests/STORY-123/run-all-tests.sh

# Expected output: 15 tests PASS (all should pass)
```

### Test-Driven Development Workflow
1. **RED:** Run tests (all fail) ✅ RED phase complete
2. **GREEN:** Implement Step 1.8 (run tests until all pass) → GREEN phase complete
3. **REFACTOR:** Improve code quality while keeping tests green → REFACTOR complete

---

## Summary

**Test Suite for STORY-123 Complete:**
- 15 comprehensive tests covering all acceptance criteria
- Bash shell scripting with AAA pattern
- Tests for unit logic, integration behavior, and edge cases
- Ready for RED phase (all tests fail) before implementation
- Tests will guide implementation in GREEN phase
- Clear pass/fail criteria for validation

**Next Step:** Proceed to GREEN phase by implementing Step 1.8 in preflight-validation.md
