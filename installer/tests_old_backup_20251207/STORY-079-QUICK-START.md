# STORY-079: Quick Start Guide

## Test Suite Status

**Status:** RED PHASE (TDD) - All tests expected to FAIL
**Test Count:** 77 tests across 4 modules
**Coverage:** 100% of acceptance criteria + technical specifications

---

## File Locations

```
installer/tests/
├── test_installation_validator.py      (647 lines, 16 tests)
├── test_repair_service.py              (559 lines, 16 tests)
├── test_manifest_manager.py            (593 lines, 16 tests)
├── integration/
│   └── test_fix_workflow.py            (730 lines, 29 tests)
├── conftest.py                         (UPDATED: +200 lines, +5 fixtures)
├── STORY-079-TEST-SUITE.md             (Complete documentation)
└── STORY-079-QUICK-START.md            (This file)
```

---

## Quick Test Execution

### Run All STORY-079 Tests
```bash
cd /mnt/c/Projects/DevForgeAI2
pytest installer/tests/test_installation_validator.py \
        installer/tests/test_repair_service.py \
        installer/tests/test_manifest_manager.py \
        installer/tests/integration/test_fix_workflow.py -v
```

### Expected Output (RED PHASE)
```
FAILED installer/tests/test_installation_validator.py::...
FAILED installer/tests/test_repair_service.py::...
...
======================== 77 failed in 2.34s ========================
```

### Run Specific Module
```bash
pytest installer/tests/test_installation_validator.py -v    # 16 tests
pytest installer/tests/test_repair_service.py -v           # 16 tests
pytest installer/tests/test_manifest_manager.py -v         # 16 tests
pytest installer/tests/integration/test_fix_workflow.py -v # 29 tests
```

### Run with Coverage
```bash
pytest installer/tests/test_installation_validator.py \
        installer/tests/test_repair_service.py \
        installer/tests/test_manifest_manager.py \
        installer/tests/integration/test_fix_workflow.py \
        --cov=installer --cov-report=html
```

---

## Test Organization

### 1. InstallationValidator Tests (16 tests)
**Purpose:** Validate installation integrity

**Key Tests:**
- File existence checking
- Checksum verification
- Missing/corrupted file detection
- User-modified file detection
- Performance: 500 files < 30 seconds

**File:** `/mnt/c/Projects/DevForgeAI2/installer/tests/test_installation_validator.py`

### 2. ManifestManager Tests (16 tests)
**Purpose:** Manage installation manifest

**Key Tests:**
- Load valid manifest
- Handle missing manifest
- Regenerate from current files
- Update manifest checksums
- Atomic write protection

**File:** `/mnt/c/Projects/DevForgeAI2/installer/tests/test_manifest_manager.py`

### 3. RepairService Tests (16 tests)
**Purpose:** Repair corrupted/missing files

**Key Tests:**
- Restore missing files
- Replace corrupted files
- Preserve user-modified files
- Backup before overwrite
- Security constraints (no mods outside DevForgeAI dirs)

**File:** `/mnt/c/Projects/DevForgeAI2/installer/tests/test_repair_service.py`

### 4. Integration Tests (29 tests)
**Purpose:** End-to-end fix command workflow

**Key Tests:**
- Detect all issue types
- Repair workflow
- Report generation
- Exit codes (0, 1, 2, 3, 4, 5)
- Missing manifest handling
- User-modified file handling

**File:** `/mnt/c/Projects/DevForgeAI2/installer/tests/integration/test_fix_workflow.py`

---

## New Test Fixtures

Added to `/mnt/c/Projects/DevForgeAI2/installer/tests/conftest.py`:

1. **corrupted_installation** - Installation with wrong checksums
2. **user_modified_installation** - Installation with user-modified files
3. **missing_manifest_installation** - Installation without manifest
4. **healthy_installation** - Valid installation with matching files
5. **mock_source_package** - Source files for repair operations

Usage:
```python
def test_something(corrupted_installation):
    files = corrupted_installation["corrupted_files"]
    root = corrupted_installation["root"]
```

---

## Acceptance Criteria Coverage

| AC | Tests | Status |
|----|-------|--------|
| AC#1: Installation Integrity Validation | 10 | RED |
| AC#2: Issue Detection | 2 | RED |
| AC#3: User-Modified File Detection | 6 | RED |
| AC#4: Automatic Repair | 10 | RED |
| AC#5: Non-Destructive Mode | 9 | RED |
| AC#6: Repair Report Display | 3 | RED |
| AC#7: Exit Codes | 6 | RED |
| AC#8: Missing Manifest Handling | 5 | RED |

---

## Service Requirements Coverage

| Service | Tests | Status |
|---------|-------|--------|
| SVC-001: Validate all files | 1 | RED |
| SVC-002: Detect missing files | 1 | RED |
| SVC-003: Detect corrupted files | 1 | RED |
| SVC-004: Detect user-modified files | 4 | RED |
| SVC-005: Restore missing files | 2 | RED |
| SVC-006: Replace corrupted files | 2 | RED |
| SVC-007: Preserve user-modified files | 2 | RED |
| SVC-008: Backup user files | 1 | RED |
| SVC-009: Calculate SHA256 | 2 | RED |
| SVC-010: Handle large files | 1 | RED |
| SVC-011: Load manifest | 6 | RED |
| SVC-012: Regenerate manifest | 9 | RED |
| SVC-013: Update manifest | 6 | RED |

---

## Key Test Patterns

### Pattern 1: Arrange-Act-Assert
```python
def test_should_detect_missing_files(self, tmp_project):
    # Arrange: Set up test data
    manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
    manifest_path.write_text(json.dumps(manifest_data))

    # Act: Execute behavior
    validator = InstallationValidator(str(tmp_project["root"]))
    issues = validator.validate()

    # Assert: Verify outcome
    assert len(missing_issues) == 1
    assert missing_issues[0].issue_type == "MISSING"
```

### Pattern 2: Using Fixtures
```python
def test_something(self, corrupted_installation):
    root = corrupted_installation["root"]
    files = corrupted_installation["corrupted_files"]
    # Use fixture data in test
```

### Pattern 3: Mocking (for UI/async)
```python
def test_user_prompt(self, tmp_project):
    with patch.object(fix_cmd, '_prompt_user') as mock_prompt:
        mock_prompt.return_value = "keep"
        # Execute code that uses mock
```

---

## Data Models (Before Implementation)

Tests use these temporary dataclasses:

```python
@dataclass
class FileEntry:
    path: str                      # "file.txt" (relative)
    checksum: str                  # SHA256 (64 hex chars)
    size: int                      # Bytes
    is_user_modifiable: bool       # User can edit?

@dataclass
class InstallManifest:
    version: str                   # "1.0.0"
    created_at: str                # ISO8601 timestamp
    files: list                    # List[FileEntry]
    schema_version: int = 1        # Always 1

@dataclass
class ValidationIssue:
    path: str
    issue_type: str                # MISSING, CORRUPTED, WRONG_VERSION, EXTRA
    expected: str = None           # Expected value
    actual: str = None             # Actual value
    severity: str = None           # CRITICAL, HIGH, MEDIUM, LOW
    is_user_modified: bool = False

@dataclass
class RepairReport:
    timestamp: str
    total_files_checked: int
    issues_found: int
    issues_fixed: int
    issues_skipped: int
    issues_remaining: int
    exit_code: int                 # 0, 1, 2, 3, 4, or 5
```

---

## Expected Exit Codes

Tests validate these exit codes:

| Code | Meaning | Test |
|------|---------|------|
| 0 | Success | test_should_exit_with_code_0_on_success |
| 1 | Missing source | test_should_exit_with_code_1_when_source_missing |
| 2 | Permission denied | test_should_exit_with_code_2_on_permission_denied |
| 3 | Partial repair | test_should_exit_with_code_3_on_partial_repair |
| 4 | Validation failed | test_should_exit_with_code_4_on_post_repair_validation_failure |
| 5 | Manual merge needed | test_should_exit_with_code_5_on_manual_merge_needed |

---

## Performance Targets (Validated by Tests)

| Requirement | Target | Test |
|-------------|--------|------|
| Validate 500 files | < 30 seconds | test_should_complete_validation_within_30_seconds |
| Checksum 100MB file | < 5 seconds | test_should_handle_large_file_checksums |

---

## Failure Reasons (Expected in RED Phase)

When you run tests before implementation, you'll see:

```
ModuleNotFoundError: No module named 'installer.installation_validator'
ImportError: cannot import name 'InstallationValidator' from 'installer'
AttributeError: 'NoneType' object has no attribute 'validate'
AssertionError: No issues should be found for valid installation
```

These are EXPECTED in RED phase - they mean the services aren't implemented yet.

---

## TDD Workflow

1. **RED PHASE** (current)
   - All 77 tests FAIL
   - No implementation exists
   - Tests define requirements

2. **GREEN PHASE** (next)
   - Implement services
   - Tests start PASSING
   - One by one, failures become passes

3. **REFACTOR PHASE**
   - Improve code quality
   - Keep tests passing
   - Optimize performance

---

## Next Steps

1. **Review tests** to understand requirements
2. **Implement services** in order:
   - ChecksumCalculator (needed by all)
   - InstallationValidator (needed by fix command)
   - ManifestManager (needed by fix command)
   - RepairService (needed by fix command)
   - FixCommand (orchestrates all)
3. **Run tests** after each service
4. **Fix failures** until all tests pass (GREEN)
5. **Refactor** while keeping tests green

---

## Commands Reference

```bash
# Run ALL tests (expect ~77 failures)
pytest installer/tests/test_*.py installer/tests/integration/test_*.py -v

# Run by category
pytest installer/tests/test_installation_validator.py -v
pytest installer/tests/test_manifest_manager.py -v
pytest installer/tests/test_repair_service.py -v
pytest installer/tests/integration/test_fix_workflow.py -v

# Run single test
pytest installer/tests/test_installation_validator.py::TestInstallationValidatorBasics::test_should_detect_missing_files -v

# Run with coverage
pytest installer/tests/ --cov=installer --cov-report=html

# Run with output (print statements visible)
pytest installer/tests/ -v -s

# Run only failures (after some pass)
pytest installer/tests/ --lf -v

# Run tests matching pattern
pytest installer/tests/ -k "checksum" -v
pytest installer/tests/ -k "manifest" -v
pytest installer/tests/ -k "repair" -v
```

---

## Summary

- ✅ **77 comprehensive failing tests** created
- ✅ **4 test modules** covering all aspects
- ✅ **5 new fixtures** for test data
- ✅ **100% AC coverage** (8/8 acceptance criteria)
- ✅ **100% SVC coverage** (13/13 service requirements)
- ✅ **All tests RED** (expecting failures)
- ✅ **Documentation complete** with quick reference

**Ready for TDD implementation!**

---

**Document Version:** 1.0
**Created:** 2025-12-06
**For:** STORY-079 - Fix/Repair Installation Mode
**Phase:** Red (Test First - Before Implementation)
