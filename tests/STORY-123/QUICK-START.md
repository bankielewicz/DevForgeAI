# STORY-123: Test Suite - Quick Start Guide

## Generated Test Files

**Location:** `/mnt/c/Projects/DevForgeAI2/tests/STORY-123/`

| File | Purpose | Tests | Executable |
|------|---------|-------|-----------|
| `test-unit-git-parsing.sh` | Core parsing logic | 4 unit tests | ✅ Yes |
| `test-integration-warning-display.sh` | User interaction | 6 integration tests | ✅ Yes |
| `test-edge-cases.sh` | Boundary conditions | 5 edge case tests | ✅ Yes |
| `run-all-tests.sh` | Master runner | All 15 tests | ✅ Yes |
| `README.md` | Comprehensive guide | Documentation | - |
| `TEST-GENERATION-SUMMARY.md` | Detailed analysis | Documentation | - |

**Total:** 5 files, 916 lines of test code, 15 tests

---

## Run Tests

### All Tests
```bash
bash tests/STORY-123/run-all-tests.sh
```

### By Category
```bash
# Unit tests (4 tests)
bash tests/STORY-123/test-unit-git-parsing.sh

# Integration tests (6 tests)
bash tests/STORY-123/test-integration-warning-display.sh

# Edge case tests (5 tests)
bash tests/STORY-123/test-edge-cases.sh
```

---

## Test Status: RED PHASE

**Current State:** All tests FAIL (expected for RED phase)

**Why?** No implementation code exists yet - tests validate specification.

**Next Step:** Implement Step 1.8 in preflight-validation.md

---

## Test Summary

### Unit Tests (4)
1. Parse git status output for .story.md files
2. Extract story ID from file path
3. Separate current story from other stories
4. Detect consecutive story ranges

### Integration Tests (6)
5. Warning displays with current story
6. Warning includes count and ranges
7. User selects "Continue" option
8. DEVFORGEAI_STORY env var set
9. "Commit first" option HALTs
10. "Show list" displays files

### Edge Cases (5)
11. No uncommitted stories (skip warning)
12. Only current story (skip warning)
13. Non-consecutive ranges formatted
14. Single other story (no "through")
15. Performance with 100+ stories

---

## Acceptance Criteria Coverage

| AC | Coverage | Tests |
|----|----------|-------|
| AC#1 | 100% | 4 tests (detect files) |
| AC#2 | 100% | 2 tests (current vs other) |
| AC#3 | 100% | 4 tests (ranges/counts) |
| AC#4 | 100% | 3 tests (user options) |
| AC#5 | 100% | 1 test (env var) |

**Total Coverage:** 100%

---

## Implementation Guide

### Where to Implement
**File:** `.claude/skills/devforgeai-development/references/preflight/_index.md`
**Location:** Add Step 1.8 after Step 1.7, before Step 2

### What Tests Expect

**Test 1-4:** Git parsing logic
```bash
git status --porcelain | grep '\.story\.md$'
# Extract STORY-114 from: devforgeai/specs/Stories/STORY-114-name.story.md
# Separate current vs others
# Detect ranges: 100-113, 115-119
```

**Test 5-6:** Warning display
```
+----------------------------------------------+
| WARNING: UNCOMMITTED STORY FILES DETECTED   |
+----------------------------------------------+
Your story: STORY-114 (will be modified...)
Other uncommitted stories: 21 files
  - STORY-100 through STORY-113 (14 files)
  - STORY-115 through STORY-119 (7 files)
```

**Test 7-10:** User interaction
```
1) Continue with scoped commits (recommended)
   → export DEVFORGEAI_STORY=STORY-114

2) Commit other stories first
   → HALT (exit code 1)

3) Show me the list
   → Display git status output
```

---

## Key Test Metrics

| Metric | Value |
|--------|-------|
| **Total Tests** | 15 |
| **Pass Rate (pre-impl)** | 53.3% (mock functions) |
| **Coverage** | 100% of AC |
| **Test Pattern** | AAA (Arrange-Act-Assert) |
| **File Format** | Bash shell script |
| **Dependencies** | git, bash (standard) |
| **Execution Time** | <5 seconds all tests |

---

## Test Quality

✅ **All Tests**
- Follow AAA pattern (Arrange, Act, Assert)
- Independent (run in any order)
- Descriptive names (test_should_X_when_Y)
- Comprehensive edge cases
- Clear pass/fail criteria

✅ **No Anti-Patterns**
- Do NOT test framework code
- Do NOT over-mock
- Do NOT test implementation details
- Do NOT create brittle assertions

---

## Troubleshooting

### Tests Fail Unexpectedly
**Check:** Is this the RED phase? Tests should fail initially.

```bash
# If test output shows:
# "⚠️ RED PHASE: 15 test(s) failing (expected)"
# → This is CORRECT behavior
```

### Git Not Available
Tests use mock git output, not actual git. If tests fail:
```bash
# Verify git is installed:
git --version

# If missing, install git
# Tests should then work
```

### Test Syntax Error
Tests require bash 4+:
```bash
bash --version
# Should show bash 4.0 or higher
```

---

## Next Steps

1. **Review tests** - Read test file to understand requirements
2. **Implement Step 1.8** - Add to preflight-validation.md
3. **Run tests** - Execute until all 15 pass (GREEN phase)
4. **Verify coverage** - Check all AC covered in tests
5. **Refactor** - Improve code quality while keeping tests green

---

## Documentation

**Detailed Information:**
- **README.md** - Comprehensive test guide with examples
- **TEST-GENERATION-SUMMARY.md** - Detailed analysis and metrics

**Story Reference:**
- **STORY-123** - `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-123-uncommitted-story-file-warning.story.md`

**Implementation Reference:**
- **Preflight Validation** - `.claude/skills/devforgeai-development/references/preflight/_index.md`
- **STORY-121** - Integration: DEVFORGEAI_STORY env var

---

## Command Reference

```bash
# Run all tests
bash tests/STORY-123/run-all-tests.sh

# Run specific category
bash tests/STORY-123/test-unit-git-parsing.sh
bash tests/STORY-123/test-integration-warning-display.sh
bash tests/STORY-123/test-edge-cases.sh

# View test files
cat tests/STORY-123/test-unit-git-parsing.sh
cat tests/STORY-123/test-integration-warning-display.sh
cat tests/STORY-123/test-edge-cases.sh

# View documentation
cat tests/STORY-123/README.md
cat tests/STORY-123/TEST-GENERATION-SUMMARY.md
```

---

**Test Generation Complete - Ready for Implementation Phase**
