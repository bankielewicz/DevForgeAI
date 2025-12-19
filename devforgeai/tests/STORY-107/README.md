# STORY-107 Test Suite: Documentation and User Guide Updates

**Test Suite Status:** RED (Failing) - TDD Phase 1 (Red Phase)
**Story ID:** STORY-107
**Story Title:** Documentation and User Guide Updates
**Epic:** EPIC-006 - Feedback Hook System
**Test Framework:** Bash Shell Scripts

## Overview

This test suite validates the documentation and user guide requirements for STORY-107. Tests are designed to fail initially (Red phase of TDD), and will pass once the required documentation files are created and populated with the specified content.

## Test Files

### Individual Acceptance Criteria Tests

| Test File | Acceptance Criteria | Purpose |
|-----------|-------------------|---------|
| `test-ac1-user-guide.sh` | AC1 | Verify User Guide documentation completeness |
| `test-ac2-architecture-doc.sh` | AC2 | Verify Architecture Documentation completeness |
| `test-ac3-troubleshooting.sh` | AC3 | Verify Troubleshooting Guide completeness |
| `test-ac4-migration-guide.sh` | AC4 | Verify Migration Guide completeness |
| `test-ac5-inline-docs.sh` | AC5 | Verify Inline Code Documentation completeness |
| `test-links-verification.sh` | Cross-doc | Verify no broken internal links between documents |

### Test Runner

| File | Purpose |
|------|---------|
| `run-all-tests.sh` | Execute all test files and generate summary report |

## Test Details

### AC1: User Guide (`test-ac1-user-guide.sh`)

**Required File:** `docs/guides/feedback-system-user-guide.md`

**Tests:**
1. File exists at specified path
2. Contains enable/disable hooks documentation
3. Contains configuration options documentation (trigger modes, conversation settings)
4. Contains common use cases examples
5. Contains feedback conversation flow explanation

**Current Status:** ✗ FAIL (File does not exist)

---

### AC2: Architecture Documentation (`test-ac2-architecture-doc.sh`)

**Required File:** `docs/architecture/hook-system-design.md`

**Tests:**
1. File exists at specified path
2. Contains Mermaid diagram code block (```mermaid)
3. Contains hook invocation flow diagram/documentation
4. Contains context extraction architecture documentation
5. Contains integration points documentation
6. Contains data flow documentation

**Current Status:** ✗ FAIL (File does not exist)

---

### AC3: Troubleshooting Guide (`test-ac3-troubleshooting.sh`)

**Required File:** `docs/guides/feedback-troubleshooting.md`

**Tests:**
1. File exists at specified path
2. Contains common issues section
3. Contains hook enable check documentation
4. Contains hook invocation logs documentation
5. Contains FAQ section with minimum 10 entries

**Current Status:** ✗ FAIL (File does not exist)

---

### AC4: Migration Guide (`test-ac4-migration-guide.sh`)

**Required File:** `docs/guides/feedback-migration-guide.md`

**Tests:**
1. File exists at specified path
2. Contains prerequisites section
3. Contains step-by-step setup instructions
4. Contains config file locations documentation
5. Contains upgrade path documentation (manual to automatic hooks)
6. Contains rollback instructions

**Current Status:** ✗ FAIL (File does not exist)

---

### AC5: Inline Code Documentation (`test-ac5-inline-docs.sh`)

**Required Files:**
- `.claude/skills/devforgeai-feedback/README.md`
- `src/context_extraction.py` (public functions)
- `.claude/scripts/devforgeai_cli/feedback/adaptive_questioning_engine.py` (public methods)

**Tests:**
1. Skill README exists at specified path
2. README contains quick start section
3. README contains feature overview
4. `context_extraction.py` contains docstrings for public functions
5. `adaptive_questioning_engine.py` contains docstrings for public methods

**Current Status:** ✗ FAIL (Files do not exist)

---

### Links Verification (`test-links-verification.sh`)

**Purpose:** Verify that all internal markdown links point to existing files

**Tests:**
1. Scan documentation files for internal links
2. Check for broken internal links
3. Verify cross-references between documents

**Current Status:** ⊘ SKIP (Documentation files not created yet)

---

## How to Run Tests

### Run All Tests

```bash
bash devforgeai/tests/STORY-107/run-all-tests.sh
```

### Run Individual Test

```bash
bash devforgeai/tests/STORY-107/test-ac1-user-guide.sh
bash devforgeai/tests/STORY-107/test-ac2-architecture-doc.sh
bash devforgeai/tests/STORY-107/test-ac3-troubleshooting.sh
bash devforgeai/tests/STORY-107/test-ac4-migration-guide.sh
bash devforgeai/tests/STORY-107/test-ac5-inline-docs.sh
bash devforgeai/tests/STORY-107/test-links-verification.sh
```

### Capture Test Results

```bash
bash devforgeai/tests/STORY-107/run-all-tests.sh 2>&1 | tee test-results.log
```

## Test Results Format

Each test produces a JSON results file:
- `test-ac1-results.json` - AC1 test results
- `test-ac2-results.json` - AC2 test results
- `test-ac3-results.json` - AC3 test results
- `test-ac4-results.json` - AC4 test results
- `test-ac5-results.json` - AC5 test results
- `test-links-results.json` - Links verification results
- `test-summary.json` - Overall test suite summary

Example JSON result structure:
```json
{
  "test_name": "AC1: User Guide",
  "total_tests": 5,
  "passed": 0,
  "failed": 5,
  "exit_code": 1,
  "timestamp": "2025-12-19T11:06:53Z"
}
```

## Test Assertions

### File Existence Checks

Tests use bash conditional statements to verify file existence:
```bash
if [ -f "${FILE_PATH}" ]; then
    # File exists - PASS
else
    # File does not exist - FAIL
fi
```

### Content Validation

Tests use grep patterns to verify required content:
```bash
if grep -qi "pattern" "${FILE_PATH}"; then
    # Content found - PASS
else
    # Content not found - FAIL
fi
```

### Counting Tests

Some tests count occurrences (e.g., FAQ entries):
```bash
FAQ_COUNT=$(grep -E "^[-*] |^[0-9]+\." "${FILE_PATH}" | wc -l)
if [ "${FAQ_COUNT}" -ge 10 ]; then
    # At least 10 FAQ entries - PASS
fi
```

## Expected Behavior

### RED Phase (Current)

All tests are **expected to FAIL** in the RED phase because:
1. Documentation files do not exist yet
2. Code does not contain required docstrings yet
3. This is normal for TDD workflow

**Expected Exit Code:** 1 (failure)

### GREEN Phase (After Implementation)

Tests should **PASS** once:
1. All documentation files are created
2. Content is added to each documentation file
3. Required code docstrings are added
4. All file paths are correct

**Expected Exit Code:** 0 (success)

## Test Coverage

### Documentation Files Tested

| Path | Purpose |
|------|---------|
| `docs/guides/feedback-system-user-guide.md` | User-facing documentation |
| `docs/architecture/hook-system-design.md` | Architecture and design documentation |
| `docs/guides/feedback-troubleshooting.md` | Troubleshooting and FAQ documentation |
| `docs/guides/feedback-migration-guide.md` | Migration and setup documentation |
| `.claude/skills/devforgeai-feedback/README.md` | Skill documentation |
| `src/context_extraction.py` | Python module (inline docstrings) |
| `.claude/scripts/devforgeai_cli/feedback/adaptive_questioning_engine.py` | Python module (inline docstrings) |

### Content Patterns Tested

#### Documentation Content
- "enable", "disable" (hooks)
- "config", "configuration", "trigger mode", "conversation setting"
- "example", "use case", "scenario", "how to"
- "flow", "conversation flow", "feedback flow"
- "common issue", "problem", "troubleshoot"
- "check", "verify", "enabled", "hook status"
- "log", "debug", "view log"
- "FAQ", "frequently asked"
- "prerequisite", "requirement"
- "step", "instruction", "setup"
- "upgrade", "manual", "automatic", "transition"
- "rollback", "revert", "undo"

#### Code Documentation
- Python docstrings (""" ... """)
- Public functions/methods (not starting with underscore)

## Test Maintenance

### Adding New Tests

To add a new test:
1. Create `test-ac[N]-description.sh` in this directory
2. Follow the existing test structure
3. Add test to `TEST_FILES` array in `run-all-tests.sh`
4. Update this README with test details

### Modifying Tests

When updating test requirements:
1. Edit the relevant test file
2. Update pattern matching if content criteria change
3. Update this README
4. Re-run tests to verify changes

### Debugging Failed Tests

To debug a failing test:
1. Run individual test: `bash test-ac1-user-guide.sh`
2. Check the generated JSON results file
3. Verify the file path is correct
4. Verify the grep pattern matches the expected content
5. Check file encoding (should be UTF-8)

## Integration with STORY-107 Development

### TDD Workflow

```
RED (Tests Fail)
  ↓
Implementation: Create documentation files
  ↓
GREEN (Tests Pass)
  ↓
Refactor: Improve documentation quality
  ↓
COMPLETE
```

### Development Steps

1. **Red Phase (CURRENT):** Tests written, all failing ✓ Complete
2. **Green Phase:** Developer creates documentation files to pass tests
3. **Refactor Phase:** Review and improve documentation
4. **Integration:** Cross-link documentation, verify links
5. **Validation:** Run all tests to confirm completion

## Dependencies

### Required System Tools
- Bash 4.0+
- grep with POSIX extended regex support
- Standard POSIX utilities (test, echo, date, sed)

### No External Dependencies
- Tests use only bash built-ins and standard Unix utilities
- No Python, Node.js, or other runtime dependencies
- Works on Linux, macOS, and WSL

## Troubleshooting

### Issue: Tests hang or timeout

**Cause:** May be waiting for user input
**Solution:** Ensure `set -e` is removed from test scripts (auto-fixed)

### Issue: Tests report wrong count

**Cause:** Pattern matching not matching actual content
**Solution:** Verify grep patterns in test files match documentation content

### Issue: File not found errors

**Cause:** Incorrect file paths
**Solution:** Verify file paths in test match actual documentation file locations

## References

- **Story:** `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-107-documentation-user-guide.story.md`
- **Acceptance Criteria:** Lines 27-61 of story file
- **Technical Specification:** Lines 62-81 of story file
- **Definition of Done:** Lines 83-90 of story file

## Test Execution Checklist

Before declaring STORY-107 complete:

- [ ] Run `bash run-all-tests.sh` - All tests pass
- [ ] AC1: User Guide file exists and contains all required sections
- [ ] AC2: Architecture doc exists with Mermaid diagrams
- [ ] AC3: Troubleshooting guide exists with 10+ FAQ entries
- [ ] AC4: Migration guide exists with complete setup instructions
- [ ] AC5: Code has docstrings and skill README exists
- [ ] Links: All internal cross-references work
- [ ] Manual Review: Documentation is clear and complete

---

**Generated:** 2025-12-19
**Test Format:** Bash Shell Scripts (Framework-agnostic, no external dependencies)
**Test Status:** RED PHASE (All tests expected to fail until implementation complete)
