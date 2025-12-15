# STORY-042: File Migration Test Suite - Quick Reference

## Overview

Comprehensive test suite for STORY-042 (Copy Framework Files from Operational Folders to src/).

- **Total Tests:** ~101 test cases
- **Organization:** 4 test files by concern (AC, Business Rules, Edge Cases, Configuration)
- **Status:** All tests RED (failing) - ready for Phase 2 implementation
- **Expected Results:** All tests will fail initially until implementation code is written

## Running Tests

### Quick Start
```bash
# Run all tests
bash tests/STORY-042/run-tests.sh

# Run with verbose output
bash tests/STORY-042/run-tests.sh --verbose

# Run specific suite
bash tests/STORY-042/run-tests.sh --suite=ac
```

### Test Suite Files

| File | Tests | Purpose |
|------|-------|---------|
| `test-ac-migration-files.sh` | 25 | Acceptance Criteria validation |
| `test-business-rules.sh` | 17 | Business rule enforcement |
| `test-edge-cases.sh` | 28 | Edge case and error handling |
| `test-migration-config.sh` | 31 | Configuration and component validation |

## Test Coverage Breakdown

### Acceptance Criteria (25 tests)

**AC-1: Copy .claude/ to src/claude/ (~370 files)**
- src/claude/ directory exists
- All subdirectories preserved (agents, commands, memory, scripts, skills)
- File count approximately 370 (±10)
- Nested structure preserved
- Original .claude/ unchanged

**AC-2: Copy .devforgeai/ config/docs/protocols/specs/tests (~80 files)**
- src/devforgeai/ directory exists
- Excluded directories not present (qa/reports, RCA, adrs, etc.)
- Required subdirectories present
- File count approximately 80 (±10)
- Subdirectory file counts within tolerance

**AC-3: Copy CLAUDE.md as template**
- src/CLAUDE.md file exists
- SHA256 checksum matches exactly
- File size matches
- Original CLAUDE.md unchanged
- Template marker comment present

**AC-4: Validate file integrity with checksum verification**
- checksums.txt manifest created
- ~450 checksum lines (±10)
- SHA256 format valid
- shasum verification successful
- Migration report generated

**AC-5: Exclude backup files and build artifacts**
- No .backup* files
- No .tmp/.temp files
- No Python bytecode
- No egg-info
- No coverage artifacts
- No node_modules
- No .git directories

**AC-6: Git track all copied files**
- Git repository initialized
- ~450 files staged (±10)
- No binary files >1MB
- Git status shows additions

**AC-7: Preserve original operational directories**
- Original .claude/ exists
- Original .devforgeai/ exists
- File counts unchanged
- No symlinks in src/
- Commands still work

### Business Rules (17 tests)

**BR-001: Original operational folders remain completely unchanged**
- Original folders exist
- File count unchanged
- Directory structure intact
- No modifications to files

**BR-002: Only framework source files copied (no generated content)**
- No qa/reports/
- No RCA/
- No adrs/
- No feedback/imported/
- No logs/
- Source files only

**BR-003: File integrity must be 100% (no corruption tolerated)**
- No truncated files
- All checksums valid
- No empty files incorrectly copied
- Sample checksum verified

**BR-004: Exclusion patterns must prevent backup/artifact pollution**
- Backup patterns excluded
- Artifact patterns excluded
- Log files excluded
- __pycache__ excluded

**BR-005: Migration must be idempotent (safe to run multiple times)**
- Safe to re-run
- Skip unchanged files
- Handle conflicts

**BR-006: Script must fail fast on first corruption/error**
- Corruption detection enabled
- Atomic per directory
- Error logging

### Edge Cases (28 tests)

**EC-1: Existing files in src/ directories**
- Detects existing files
- Compares checksums for existing
- Handles modified files
- Skips matching files

**EC-2: Permission errors during copy**
- Handles unreadable source
- Handles unwritable destination
- Reports permission errors
- Continues after error

**EC-3: Partial copy due to interruption**
- Detects incomplete copy
- Creates checkpoint file
- Provides resume command
- Skips completed files on resume

**EC-4: File corruption detection**
- Detects corruption immediately
- Halts on first corruption
- Reports corruption details
- Provides rollback command

**EC-5: Symlink handling**
- Detects symlinks
- Follows symlink targets
- Logs symlink operations
- No broken links in destination

**EC-6: Large file handling (>10MB)**
- Detects large files
- Uses streaming copy
- Shows progress reporting
- Chunked checksum validation

**EC-7: Case-sensitive filesystem conflicts**
- Detects case conflicts
- Provides conflict resolution
- Prevents silent overwrite
- Logs resolution choice

### Configuration & Components (31 tests)

**Component 1: MigrationScript (Worker) - 7 tests**
- Script exists and executable
- Has bash shebang
- Copy function implemented
- Exclusion function implemented
- Checksum function implemented
- Git function implemented

**Component 2: MigrationConfig (Configuration) - 6 tests**
- Configuration file exists
- Valid JSON format
- Sources defined (3)
- Exclusion patterns defined (≥8)
- Validation thresholds defined
- File count expectations set

**Component 3: ChecksumManifest (DataModel) - 5 tests**
- Checksums file exists
- Line count ~450
- SHA256 format valid
- Verifiable with shasum
- All checksums unique

**Component 4: MigrationLogger (Logging) - 6 tests**
- Log file exists
- Copy entries logged
- Validation entries logged
- Exclusion entries logged
- Summary statistics logged
- Timestamps in log

**Non-Functional Requirements - 5 tests**
- NFR-001: Performance < 2 min
- NFR-002: Checksums < 1 min
- NFR-003: Memory < 50 MB
- NFR-004: Atomic per directory
- NFR-007: Permissions preserved

## Expected Test Results

### Initially (RED - All Failing)
```
Tests run:    101
Tests passed: 0
Tests failed: 101
```

This is correct for TDD! Tests should fail because implementation doesn't exist yet.

### After Implementation (GREEN - All Passing)
```
Tests run:    101
Tests passed: 101
Tests failed: 0
```

## Implementation Roadmap

### Phase 2A: Core Migration Script
- Create `migrate-framework-files.sh`
- Implement .claude/ copy
- Implement .devforgeai/ copy with exclusions
- Generate checksums

**Expected to pass:** AC-1, AC-2, AC-4, BR-001, BR-002, BR-003, BR-004 (partial)

### Phase 2B: Git Integration & Validation
- Git staging
- Validation report generation
- Migration logging
- Checksum verification

**Expected to pass:** AC-6, AC-4, CONFIG tests (partial)

### Phase 2C: Configuration & Error Handling
- Create migration-config.json
- Implement error handling for edge cases
- Permission error handling
- Corruption detection

**Expected to pass:** CONFIG, EC-2, EC-4, BR-006

### Phase 2D: Idempotency & Recovery
- Checkpoint file creation
- Resume capability
- Conflict detection
- Rollback functionality

**Expected to pass:** EC-1, EC-3, BR-005

### Phase 2E: Advanced Features
- Symlink handling (EC-5)
- Large file streaming (EC-6)
- Case-sensitive conflict detection (EC-7)

**Expected to pass:** Remaining edge case tests

## Test Organization

```
tests/STORY-042/
├── test-ac-migration-files.sh       # 25 AC tests
├── test-business-rules.sh           # 17 BR tests
├── test-edge-cases.sh               # 28 EC tests
├── test-migration-config.sh         # 31 CONF tests
├── run-tests.sh                     # Master runner
├── QUICK-REFERENCE.md               # This file
└── reports/
    ├── test-summary.txt             # Generated summary
    └── test-results.json            # Generated JSON results
```

## Test Patterns Used

### Assertion Helpers
Each test file includes helpers for:
- File count validation (with tolerance)
- Checksum verification
- File size matching
- Directory existence checks
- File existence checks
- Pattern matching (exclusion verification)
- Git staging validation

### Setup/Teardown
- Temporary directory creation
- Test environment cleanup
- Log file management

### Error Handling
- Graceful degradation when tools unavailable
- Skipping (⊘) vs failing (✗) appropriately
- Clear error messages

## Key Testing Insights

### Tolerance Levels
- File counts: ±10 files (accounts for development variance)
- Directory sizes: ±3 files per subdirectory
- This prevents brittle tests while still validating behavior

### Idempotency Testing
- Tests validate second-run behavior
- Checksum-based skip verification
- Conflict handling mechanisms

### Performance Baselines
- Copy: <2 minutes for 450 files
- Checksums: <1 minute with parallel processing
- Memory: <50 MB footprint

## Debugging Failed Tests

### Common Issues

**Test Timeout**
- Increase timeout if testing on slow hardware
- Check for permission errors in logs

**File Count Mismatch**
- Verify tolerance levels (±10 default)
- Check for excluded patterns affecting count

**Checksum Mismatch**
- Verify no file corruption during copy
- Check line endings (LF vs CRLF)

**Permission Errors**
- Verify source file readability
- Check destination directory writability

## References

- Story: `devforgeai/specs/Stories/STORY-042-copy-framework-files-to-src.story.md`
- Tech Stack: `devforgeai/context/tech-stack.md`
- TDD Principles: CLAUDE.md - Test-Driven Development section

## Test Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| Total Test Cases | 101 | Organized in 4 files |
| AC Coverage | 25/7 AC | 3-5 tests per AC |
| BR Coverage | 17/6 BR | 2-6 tests per BR |
| EC Coverage | 28/7 EC | 4 tests per EC |
| Component Tests | 31 | 4 components + 5 NFRs |
| Pass Rate (Initial) | 0% | All RED - expected |
| Pass Rate (Target) | 100% | All GREEN - after implementation |
| Estimated Execution Time | ~2-3 minutes | Full suite with all tests |

## Next Steps

1. **Phase 2 Implementation**
   - Use these tests to drive implementation (TDD)
   - Write minimal code to pass failing tests
   - Refactor while keeping tests green

2. **Test Review**
   - Run tests after each implementation phase
   - Check pass rate increases
   - Validate no regressions

3. **Coverage Validation**
   - Run: `bash tests/STORY-042/run-tests.sh --verbose`
   - Review: `tests/STORY-042/reports/test-summary.txt`
   - Iterate: Fix failures in implementation

4. **Acceptance**
   - All 101 tests passing ✓
   - Migration report generated ✓
   - Original folders unchanged ✓
   - Git staging complete ✓
   - Ready for Phase 3 (QA)
