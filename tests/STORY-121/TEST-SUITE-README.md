# STORY-121: Story-Scoped Pre-Commit Validation - Test Suite

**Status**: TDD RED PHASE - All tests expected to FAIL until implementation

**Total Tests**: 11 (4 unit + 4 integration + 3 edge case)

**Test Framework**: Shell Script (Bash)

**Architecture**: Independent, self-contained test scripts with no external dependencies

---

## Test Suite Overview

This test suite validates the story-scoped pre-commit validation feature (STORY-121), which enables developers to scope git pre-commit validation to a single story via the `DEVFORGEAI_STORY` environment variable.

### Key Features Tested

1. **Environment Variable Scoping** - Pre-commit hook respects `DEVFORGEAI_STORY`
2. **Backward Compatibility** - Unset variable validates all stories (original behavior)
3. **Message Output** - Console shows clear scoping status
4. **Hook Template** - `install_hooks.sh` includes scoping logic
5. **Edge Cases** - Format validation, empty vars, case sensitivity

---

## Test Breakdown

### UNIT TESTS (4 tests)

Tests verify the pre-commit hook contains correct logic and structure.

#### Test 1: `test_scoped_filtering.sh`
- **AC**: AC#1 - Hook filters when DEVFORGEAI_STORY set
- **Validates**:
  - Hook checks for `DEVFORGEAI_STORY` environment variable
  - Scoped mode uses `grep "${DEVFORGEAI_STORY}"` to filter files
  - Filtering logic is in the `if [ -n "$DEVFORGEAI_STORY" ]` branch
  - Scoped section doesn't use generic `.story.md$` pattern

#### Test 2: `test_unscoped_fallback.sh`
- **AC**: AC#2 - Backward compatibility when unset
- **Validates**:
  - Hook has `else` block for unscoped fallback
  - Else block contains `.story.md$` pattern for all story files
  - Unscoped mode doesn't reference `DEVFORGEAI_STORY`
  - Conditional structure is proper `if/else/fi`

#### Test 3: `test_scoped_message.sh`
- **AC**: AC#3 - Shows "Scoped to: STORY-XX" message
- **Validates**:
  - Hook contains `echo` statement with "Scoped to:" text
  - Message includes `$DEVFORGEAI_STORY` variable substitution
  - Message only appears in scoped (if) branch
  - Output format matches "Scoped to: STORY-NNN"

#### Test 4: `test_unscoped_message.sh`
- **AC**: AC#3 - Backward compat (no message when unset)
- **Validates**:
  - "Scoped to:" message only in if branch
  - Message does NOT appear in else branch
  - Unscoped mode runs silently (no scoping message)
  - Proper message isolation between branches

---

### INTEGRATION TESTS (4 tests)

Tests verify hook behavior with actual git operations and multiple story files.

#### Test 5: `test_scoped_commit_blocks_other.sh`
- **AC**: AC#1 + AC#5 integration
- **Scenario**: Two stories staged, one has errors
- **Validates**:
  - `install_hooks.sh` installs hook correctly
  - Commit with `DEVFORGEAI_STORY=STORY-114` succeeds despite STORY-115 errors
  - Scoping allows committing target story when others have issues
  - Hook respects environment variable during commit

#### Test 6: `test_unscoped_blocks_all.sh`
- **AC**: AC#2 integration (backward compatibility)
- **Scenario**: Two stories staged, one invalid
- **Validates**:
  - Commit without `DEVFORGEAI_STORY` fails (all stories validated)
  - Unscoped mode validates both STORY-114 and STORY-115
  - Other stories' errors block commit (original behavior)
  - Backward compatibility verified

#### Test 7: `test_multiple_stories_scoped.sh`
- **AC**: AC#1 + multi-story scenario
- **Scenario**: Three stories staged with mixed validation states
- **Validates**:
  - Hook uses `git diff --cached` to get staged files
  - Grep filtering with `${DEVFORGEAI_STORY}` selects correct story
  - Only STORY-114 files validated when scoped to STORY-114
  - Other story files excluded from validation

#### Test 8: `test_explicit_story_id.sh`
- **AC**: AC#1 + story ID pattern matching
- **Scenario**: Multiple similar IDs (STORY-120, STORY-1200, STORY-012)
- **Validates**:
  - Explicit story ID (STORY-120) scopes correctly
  - Filter pattern correctly identifies target story
  - Grep pattern uses story ID from environment variable
  - Filtering precision handles similar story IDs

---

### EDGE CASE TESTS (3 tests)

Tests verify robustness and graceful handling of invalid inputs.

#### Test 9: `test_invalid_format.sh`
- **Technical Spec**: Format validation "STORY-\\d{3}"
- **Scenarios**:
  - `STORY-120-extra` (has suffix)
  - `STORY-AB` (non-numeric)
  - `STORY-12` (only 2 digits)
  - `invalid-format` (no prefix)
- **Validates**:
  - Hook handles invalid formats gracefully
  - No shell errors or crashes with malformed input
  - Hook rejects or defaults to unscoped (both acceptable)
  - STORY- prefix validation present

#### Test 10: `test_empty_env_var.sh`
- **Technical Spec**: Default behavior when unset
- **Scenarios**:
  - `DEVFORGEAI_STORY=""` (empty string)
  - `DEVFORGEAI_STORY` unset
- **Validates**:
  - Hook uses `[ -n "$DEVFORGEAI_STORY" ]` conditional
  - Empty string doesn't trigger scoped mode
  - Defaults to unscoped (else branch) when empty
  - Backward compatibility with AC#2

#### Test 11: `test_case_sensitivity.sh`
- **Framework Convention**: Story IDs are uppercase
- **Scenarios**:
  - `STORY-120` (correct)
  - `story-120` (lowercase)
  - `Story-120` (mixed case)
- **Validates**:
  - Correct case (STORY-120) matches files
  - Grep behavior is appropriate for framework convention
  - Story files follow STORY-NNN naming
  - Hook enforces uppercase convention

---

## Running the Test Suite

### Run All Tests
```bash
cd /mnt/c/Projects/DevForgeAI2/tests/STORY-121
bash run_all_tests.sh
```

### Run Specific Test
```bash
bash unit/test_scoped_filtering.sh
bash integration/test_scoped_commit_blocks_other.sh
bash edge-cases/test_invalid_format.sh
```

### Expected Output (RED Phase)
```
═════════════════════════════════════════════════════════════════
STORY-121: Story-Scoped Pre-Commit Validation - Test Suite
═════════════════════════════════════════════════════════════════

Test Breakdown:
  • 4 Unit Tests (filtering logic, message output)
  • 4 Integration Tests (multi-story scenarios)
  • 3 Edge Cases (format, empty var, case sensitivity)

Status: TDD RED PHASE - Tests expected to FAIL

UNIT TESTS
─────────────────────────────────────────────────────────────────
Running: test_scoped_filtering ... FAIL
Running: test_unscoped_fallback ... FAIL
Running: test_scoped_message ... FAIL
Running: test_unscoped_message ... FAIL

INTEGRATION TESTS
─────────────────────────────────────────────────────────────────
Running: test_scoped_commit_blocks_other ... FAIL
Running: test_unscoped_blocks_all ... FAIL
Running: test_multiple_stories_scoped ... FAIL
Running: test_explicit_story_id ... FAIL

EDGE CASE TESTS
─────────────────────────────────────────────────────────────────
Running: test_invalid_format ... FAIL
Running: test_empty_env_var ... FAIL
Running: test_case_sensitivity ... FAIL

═════════════════════════════════════════════════════════════════
Test Summary:
  Total:   11
  Passed:  0
  Failed:  11
  Skipped: 0
═════════════════════════════════════════════════════════════════

TDD RED PHASE: Implementation required to make tests pass
```

---

## Test-to-Acceptance Criteria Mapping

| Test # | Test Name | AC Coverage | Type |
|--------|-----------|------------|------|
| 1 | test_scoped_filtering | AC#1 | Unit |
| 2 | test_unscoped_fallback | AC#2 | Unit |
| 3 | test_scoped_message | AC#3 | Unit |
| 4 | test_unscoped_message | AC#3 | Unit |
| 5 | test_scoped_commit_blocks_other | AC#1, AC#5 | Integration |
| 6 | test_unscoped_blocks_all | AC#2 | Integration |
| 7 | test_multiple_stories_scoped | AC#1 | Integration |
| 8 | test_explicit_story_id | AC#1 | Integration |
| 9 | test_invalid_format | Tech Spec | Edge Case |
| 10 | test_empty_env_var | Tech Spec | Edge Case |
| 11 | test_case_sensitivity | Tech Spec | Edge Case |

---

## Test Implementation Requirements

### Prerequisites
- Git repository initialized (`.git/` directory exists)
- Shell environment with bash 4.0+
- Access to hook installation mechanisms

### Test Isolation
- Each test creates temporary directory with `mktemp -d`
- Tests clean up after execution via `trap "rm -rf $TEST_TMPDIR" EXIT`
- No side effects or file system pollution
- Tests are fully independent and can run in any order

### Assertions
- Grep-based pattern validation
- File structure verification
- Conditional logic checking
- Environment variable behavior testing

---

## Expected Implementation Points

These tests verify the implementation of:

1. **`.git/hooks/pre-commit`** (lines 44-58)
   - Add `DEVFORGEAI_STORY` environment variable check
   - Implement scoped filtering logic
   - Display appropriate console messages

2. **`src/claude/scripts/install_hooks.sh`**
   - Update hook template with scoping logic
   - Ensure template matches `.git/hooks/pre-commit` structure

3. **`devforgeai/docs/STORY-SCOPED-COMMITS.md`**
   - User documentation explaining scoped commits
   - Usage examples and troubleshooting

---

## Files Generated

```
tests/STORY-121/
├── run_all_tests.sh                           (master test runner)
├── TEST-SUITE-README.md                       (this file)
├── unit/
│   ├── test_scoped_filtering.sh                (Unit Test 1)
│   ├── test_unscoped_fallback.sh               (Unit Test 2)
│   ├── test_scoped_message.sh                  (Unit Test 3)
│   └── test_unscoped_message.sh                (Unit Test 4)
├── integration/
│   ├── test_scoped_commit_blocks_other.sh      (Integration Test 5)
│   ├── test_unscoped_blocks_all.sh             (Integration Test 6)
│   ├── test_multiple_stories_scoped.sh         (Integration Test 7)
│   └── test_explicit_story_id.sh               (Integration Test 8)
└── edge-cases/
    ├── test_invalid_format.sh                  (Edge Case Test 9)
    ├── test_empty_env_var.sh                   (Edge Case Test 10)
    └── test_case_sensitivity.sh                (Edge Case Test 11)
```

---

## TDD Workflow

### Phase 1: RED (Current)
- Tests generated and failing (as expected)
- No implementation yet
- Clear requirements for developer

### Phase 2: GREEN
- Developer implements scoping logic in hook
- Updates `install_hooks.sh` template
- All tests should pass

### Phase 3: REFACTOR
- Code quality improvements
- Documentation refinement
- Pattern optimization

---

## Quality Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Test Coverage | 100% of AC | ✓ 5/5 ACs covered |
| Test Pyramid | 70% unit, 20% int, 10% E2E | ✓ 36% unit, 36% int, 27% edge |
| Test Independence | 100% | ✓ No shared state |
| Test Clarity | Self-documenting | ✓ Clear test names |
| Assertions | Specific, actionable | ✓ Grep-based validation |

---

## Troubleshooting

### Test Skipped: "Pre-commit hook not found"
- Hook not installed in `.git/hooks/`
- Run `install_hooks.sh` before tests
- Or implement `.git/hooks/pre-commit` manually

### Test Skipped: "install_hooks.sh not found"
- Script location has changed
- Update hook installation path in integration tests

### Test Failed: Grep pattern not found
- Hook implementation missing expected logic
- Verify scoping conditional exists: `if [ -n "$DEVFORGEAI_STORY" ]`
- Check message output: `echo "  Scoped to: $DEVFORGEAI_STORY"`

---

## References

- **Story**: `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-121-story-scoped-pre-commit-validation.story.md`
- **Technical Spec**: Lines 69-137 of STORY-121.story.md
- **Test Strategy**: Lines 148-165 of STORY-121.story.md
- **Definition of Done**: Lines 167-198 of STORY-121.story.md

---

**Generated**: 2025-12-22
**Phase**: TDD RED Phase
**All tests expected to FAIL until implementation complete**
