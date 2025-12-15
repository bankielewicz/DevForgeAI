# STORY-042: File Migration Test Suite

Comprehensive test suite for STORY-042: Copy Framework Files from Operational Folders to src/

## Quick Start

```bash
# Run all tests
bash tests/STORY-042/run-tests.sh

# Run with verbose output
bash tests/STORY-042/run-tests.sh --verbose

# Run specific test suite
bash tests/STORY-042/run-tests.sh --suite=ac
```

## Test Files Overview

| File | Tests | Purpose | Lines |
|------|-------|---------|-------|
| `test-ac-migration-files.sh` | 25 | Acceptance Criteria validation | 675 |
| `test-business-rules.sh` | 17 | Business rule enforcement | 533 |
| `test-edge-cases.sh` | 28 | Edge case handling | 486 |
| `test-migration-config.sh` | 31 | Configuration & components | 630 |
| `run-tests.sh` | — | Master test runner | 344 |
| **TOTAL** | **101** | **Complete test suite** | **2,668** |

## Test Coverage

### Acceptance Criteria (25 tests)
- AC-1: Copy .claude/ to src/claude/ (5 tests)
- AC-2: Copy .devforgeai/ content (5 tests)
- AC-3: Copy CLAUDE.md template (5 tests)
- AC-4: Checksum verification (5 tests)
- AC-5: Exclude backup/artifacts (7 tests)
- AC-6: Git tracking (4 tests)
- AC-7: Preserve originals (5 tests)

### Business Rules (17 tests)
- BR-001: Originals unchanged (4 tests)
- BR-002: Source files only (6 tests)
- BR-003: File integrity 100% (4 tests)
- BR-004: Exclusion patterns (4 tests)
- BR-005: Idempotency (3 tests)
- BR-006: Fail fast (3 tests)

### Edge Cases (28 tests)
- EC-1: Existing files (4 tests)
- EC-2: Permission errors (4 tests)
- EC-3: Partial copy (4 tests)
- EC-4: Corruption (4 tests)
- EC-5: Symlinks (4 tests)
- EC-6: Large files (4 tests)
- EC-7: Case conflicts (4 tests)

### Configuration & Components (31 tests)
- MigrationScript (Worker): 7 tests
- MigrationConfig (Configuration): 6 tests
- ChecksumManifest (DataModel): 5 tests
- MigrationLogger (Logging): 6 tests
- NFRs (Non-Functional): 5 tests

## Current Status

```
Tests Generated:  101
Expected Results: 0 passing (all RED - no implementation yet)
Expected Results: 101 failing (correct for TDD Red phase)
Pass Rate:        0% (expected - drives implementation)
```

## Directory Structure

```
tests/STORY-042/
├── README.md                      # This file
├── QUICK-REFERENCE.md             # Quick guide (385 lines)
├── TEST-GENERATION-SUMMARY.md     # Complete documentation (681 lines)
├── test-ac-migration-files.sh     # AC tests (675 lines)
├── test-business-rules.sh         # BR tests (533 lines)
├── test-edge-cases.sh             # EC tests (486 lines)
├── test-migration-config.sh       # CONFIG tests (630 lines)
├── run-tests.sh                   # Master runner (344 lines)
└── reports/                       # Generated on test run
    ├── test-summary.txt
    └── test-results.json
```

## Usage Examples

### Run All Tests (Default)
```bash
bash tests/STORY-042/run-tests.sh
```
Output: Summary of all 101 tests with pass/fail counts

### Run with Verbose Output
```bash
bash tests/STORY-042/run-tests.sh --verbose
```
Output: Each test result with details

### Run Single Suite
```bash
# Run AC tests only
bash tests/STORY-042/run-tests.sh --suite=ac

# Run BR tests only
bash tests/STORY-042/run-tests.sh --suite=business

# Run EC tests only
bash tests/STORY-042/run-tests.sh --suite=edge

# Run CONFIG tests only
bash tests/STORY-042/run-tests.sh --suite=config
```

### Run Without Test Execution
```bash
bash tests/STORY-042/run-tests.sh --report-only
```
Output: Generated summary and JSON report only

## Test Framework Features

### Assertion Helpers
- `assert_file_count()` - Validate file count with tolerance
- `assert_file_exists()` - Check if file exists
- `assert_checksum_match()` - Compare SHA256 checksums
- `assert_file_size_match()` - Verify file sizes match
- `assert_directory_exists()` - Check directory presence
- `assert_no_matches()` - Ensure exclusion patterns work
- `assert_git_added_count()` - Verify git staging

### Test Patterns
- **AAA Pattern:** Arrange, Act, Assert
- **Setup/Teardown:** Temporary directory management
- **Graceful Degradation:** Skip tests if tools unavailable
- **Clear Output:** Color-coded results with descriptions

### Error Handling
Tests validate:
- Permission errors
- Corruption detection
- Recovery mechanisms
- Conflict resolution
- Error logging
- Rollback capability

## Test Metrics

| Metric | Value |
|--------|-------|
| Total Tests | 101 |
| Total Lines | 2,668 |
| AC Coverage | 25/7 ACs |
| BR Coverage | 17/6 BRs |
| EC Coverage | 28/7 Edge Cases |
| Component Coverage | 31 (4 components + 5 NFRs) |
| Pass Rate (Expected) | 0% (RED phase) |
| Execution Time | 2-3 minutes |
| Test Independence | 100% |

## TDD Workflow

### Phase 1: RED (Test First) ✓ COMPLETE
Tests written before implementation. All 101 tests currently failing.

### Phase 2: GREEN (Implementation) — NEXT
- Implement migration script to pass tests
- Run tests iteratively
- Increase pass rate from 0% to 100%

### Phase 3: REFACTOR (Quality)
- Improve code quality while keeping tests green
- Optimize performance
- Add documentation

## Implementation Roadmap

### Milestone 1: Basic Copy (10-15 tests passing)
Copy operations for .claude/ and .devforgeai/

### Milestone 2: Validation (30-40 tests passing)
Checksums, file integrity, and migration reports

### Milestone 3: Git Integration (50-60 tests passing)
Git staging and pre-commit validation

### Milestone 4: Error Handling (80-90 tests passing)
Permission errors, corruption detection, logging

### Milestone 5: Advanced Features (101 tests passing)
Symlinks, large files, case conflicts

## Expected Test Results (Initially)

```
══════════════════════════════════════════════════════════
STORY-042: File Migration - Complete Test Suite
══════════════════════════════════════════════════════════

Tests run:    101
Tests passed: 0 ← All RED (expected for TDD)
Tests failed: 101

══════════════════════════════════════════════════════════
```

This is correct! Tests should fail because implementation doesn't exist yet.

## Expected Test Results (After Implementation)

```
══════════════════════════════════════════════════════════
STORY-042: File Migration - Complete Test Suite
══════════════════════════════════════════════════════════

Tests run:    101
Tests passed: 101 ← All GREEN
Tests failed: 0

══════════════════════════════════════════════════════════
✓ ALL TESTS PASSED - Ready for Phase 2 completion
══════════════════════════════════════════════════════════
```

## Key Files to Implement

### Required Components

1. **MigrationScript**
   - File: `src/scripts/migrate-framework-files.sh`
   - Purpose: Core migration logic
   - Tests: 7 CONF tests + related AC/BR/EC tests

2. **MigrationConfig**
   - File: `src/scripts/migration-config.json`
   - Purpose: Configuration data
   - Tests: 6 CONF tests

3. **ChecksumManifest**
   - File: `checksums.txt`
   - Purpose: File integrity validation
   - Tests: 5 CONF tests + related AC tests

4. **MigrationLogger**
   - File: `migration.log` or `src/scripts/migration.log`
   - Purpose: Operation logging
   - Tests: 6 CONF tests

## Documentation Files

- **QUICK-REFERENCE.md** - Fast guide to tests and running them
- **TEST-GENERATION-SUMMARY.md** - Complete test documentation
- **README.md** - This file (overview)

## Validation Checklist

Before considering implementation complete:

- [ ] All 101 tests pass
- [ ] No tests skipped
- [ ] Coverage report shows 100%
- [ ] Original folders unchanged
- [ ] Git staging complete
- [ ] Checksums verified
- [ ] No excluded files in src/
- [ ] Error cases handled
- [ ] Logs generated
- [ ] Reports created

## Troubleshooting

### Tests Won't Run
```bash
# Make scripts executable
chmod +x tests/STORY-042/*.sh

# Run directly with bash
bash tests/STORY-042/run-tests.sh
```

### Tests Are Passing Unexpectedly
Check if implementation already exists in src/scripts/

### Can't Find Test Results
```bash
# Check reports directory
ls -la tests/STORY-042/reports/

# View summary
cat tests/STORY-042/reports/test-summary.txt

# View JSON results
cat tests/STORY-042/reports/test-results.json
```

### Individual Test Failures
Run with verbose mode to see details:
```bash
bash tests/STORY-042/run-tests.sh --verbose --suite=ac
```

## References

### Story Documentation
- Story: `devforgeai/specs/Stories/STORY-042-copy-framework-files-to-src.story.md`

### Test Framework
- Framework: Bash with TAP output
- Tested: File operations, checksums, git, logging

### Quality Standards
- TDD: Tests first, implementation follows
- Pass Rate: Target 0% initially (RED), 100% finally (GREEN)
- Coverage: 100% of requirements

## Support

For test-related questions:
1. Check QUICK-REFERENCE.md for quick answers
2. Review TEST-GENERATION-SUMMARY.md for detailed information
3. Examine specific test file source code
4. Run tests with --verbose flag for detailed output

## Version History

- **v1.0** (2025-11-18): Initial test suite generation
  - 101 tests across 4 files
  - Complete coverage of all requirements
  - Ready for Phase 2 implementation

---

**Status:** Test Generation Complete ✓
**Ready for:** Phase 2 Green Phase (Implementation)
**Next Step:** Implement migrate-framework-files.sh following TDD
