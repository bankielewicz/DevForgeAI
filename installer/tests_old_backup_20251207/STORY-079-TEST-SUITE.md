# STORY-079: Fix/Repair Installation Mode - Test Suite

## Overview

Comprehensive failing test suite for STORY-079 (Fix/Repair Installation Mode) following Test-Driven Development (TDD) Red phase. This document describes the test modules, fixtures, and execution instructions.

**Status:** All tests are designed to FAIL initially (Red phase). After implementation, they will PASS (Green phase).

---

## Test Modules

### 1. Unit Tests: InstallationValidator

**File:** `/mnt/c/Projects/DevForgeAI2/installer/tests/test_installation_validator.py`

**Purpose:** Validate installation integrity against manifest (AC#1, AC#2, AC#3)

**Test Classes:**

- **TestInstallationValidatorBasics** (10 tests)
  - `test_should_validate_all_files_when_manifest_valid` - SVC-001
  - `test_should_detect_missing_files` - SVC-002
  - `test_should_detect_corrupted_files` - SVC-003
  - `test_should_detect_user_modified_files` - SVC-004
  - `test_should_detect_extra_files_with_warning_severity` - AC#2
  - `test_should_populate_issue_details` - AC#2
  - `test_should_complete_validation_within_30_seconds` - NFR-001 (500 files)
  - `test_should_handle_empty_manifest` - Edge case
  - `test_should_handle_large_file_checksums` - NFR-002 (100MB file)
  - `test_should_validate_file_size_mismatch` - AC#1

- **TestUserModifiedFileDetection** (4 tests)
  - `test_should_flag_user_modifiable_location_files` - AC#3
  - `test_should_detect_recent_modifications` - AC#3
  - `test_should_detect_user_specific_content_patterns` - AC#3
  - `test_should_provide_diff_preview_for_text_files` - AC#3

- **TestManifestValidation** (2 tests)
  - `test_should_validate_manifest_structure` - Data model validation
  - `test_should_validate_checksums_are_sha256` - Data model validation

**Coverage Targets:**
- InstallationValidator service: 95%+
- Checksum calculation: 95%+
- File detection logic: 95%+

---

### 2. Unit Tests: ManifestManager

**File:** `/mnt/c/Projects/DevForgeAI2/installer/tests/test_manifest_manager.py`

**Purpose:** Manage installation manifest (SVC-011, SVC-012, SVC-013)

**Test Classes:**

- **TestManifestManagerLoading** (6 tests)
  - `test_should_load_valid_manifest` - SVC-011
  - `test_should_return_none_when_manifest_missing` - SVC-011
  - `test_should_validate_manifest_structure` - Data validation
  - `test_should_parse_file_entries_correctly` - Data validation
  - `test_should_handle_corrupted_manifest_json` - Error handling
  - `test_should_validate_checksum_format` - Data validation

- **TestManifestManagerRegeneration** (8 tests)
  - `test_should_regenerate_manifest_from_current_files` - SVC-012, AC#8
  - `test_should_calculate_correct_checksums_during_regeneration` - AC#8
  - `test_should_calculate_correct_file_sizes_during_regeneration` - AC#8
  - `test_should_mark_user_modifiable_files_during_regeneration` - AC#8
  - `test_should_set_created_at_timestamp` - Data model
  - `test_should_exclude_manifest_file_from_regeneration` - AC#8
  - `test_should_exclude_backup_files_from_regeneration` - AC#8
  - `test_should_handle_empty_directory_during_regeneration` - Edge case

- **TestManifestManagerUpdating** (6 tests)
  - `test_should_update_manifest_checksum_after_repair` - SVC-013, AC#4
  - `test_should_update_file_size_in_manifest` - SVC-013
  - `test_should_preserve_is_user_modifiable_flag_during_update` - AC#4
  - `test_should_save_updated_manifest_to_disk` - SVC-013
  - `test_should_handle_atomic_write_protection` - Reliability
  - `test_should_handle_very_large_manifest` - Performance (10K+ files)

- **TestManifestManagerEdgeCases** (2 tests)
  - `test_should_handle_special_characters_in_paths` - Edge case

**Coverage Targets:**
- ManifestManager service: 95%+
- Manifest I/O operations: 95%+
- Data validation: 95%+

---

### 3. Unit Tests: RepairService

**File:** `/mnt/c/Projects/DevForgeAI2/installer/tests/test_repair_service.py`

**Purpose:** Repair installation issues (AC#4, AC#5, SVC-005-008)

**Test Classes:**

- **TestRepairServiceBasics** (7 tests)
  - `test_should_restore_missing_file_from_source` - SVC-005, AC#4
  - `test_should_replace_corrupted_file_with_source_version` - SVC-006, AC#4
  - `test_should_preserve_user_modified_files_without_force_flag` - SVC-007, AC#5
  - `test_should_backup_user_file_before_overwrite` - SVC-008, AC#5
  - `test_should_skip_file_when_user_chooses_keep` - AC#5
  - `test_should_restore_original_when_user_chooses_restore` - AC#5
  - `test_should_show_diff_for_text_files` - AC#5

- **TestRepairServiceSecurityConstraints** (2 tests)
  - `test_should_not_modify_files_outside_devforgeai_directories` - NFR-004
  - `test_should_only_repair_recognized_devforgeai_files` - NFR-004

- **TestRepairServiceUserInteraction** (4 tests)
  - `test_should_prompt_user_for_each_user_modified_file` - AC#5
  - `test_should_offer_four_user_options_for_modified_files` - AC#5
  - `test_should_respect_user_choice_for_each_file` - AC#5
  - `test_should_force_repair_all_files_with_force_flag` - AC#5

- **TestRepairServiceEdgeCases** (3 tests)
  - `test_should_handle_symlinks_appropriately` - Edge case
  - `test_should_handle_directories_in_manifest` - Edge case
  - `test_should_handle_empty_source_package` - Error case

**Coverage Targets:**
- RepairService: 95%+
- File restoration logic: 95%+
- User interaction: 85%+ (UI mocking)

---

### 4. Integration Tests: Fix Workflow

**File:** `/mnt/c/Projects/DevForgeAI2/installer/tests/integration/test_fix_workflow.py`

**Purpose:** End-to-end fix command workflow (AC#1-8, all SVC requirements)

**Test Classes:**

- **TestFixWorkflowHealthyInstallation** (2 tests)
  - `test_should_detect_no_issues_in_healthy_installation` - AC#1, AC#6
  - `test_should_exit_with_0_when_no_issues_found` - AC#7

- **TestFixWorkflowIssueDetection** (2 tests)
  - `test_should_detect_all_issue_types_during_fix` - AC#2
  - `test_should_display_issue_details` - AC#2

- **TestFixWorkflowRepairOperations** (4 tests)
  - `test_should_repair_missing_files` - AC#4, SVC-005
  - `test_should_replace_corrupted_files` - AC#4, SVC-006
  - `test_should_update_manifest_after_repair` - AC#4, SVC-013
  - `test_should_log_repair_operations` - AC#4, AC#6

- **TestFixWorkflowReporting** (3 tests)
  - `test_should_generate_repair_report` - AC#6
  - `test_should_save_log_file` - AC#6
  - `test_should_display_summary_statistics` - AC#6

- **TestFixWorkflowExitCodes** (6 tests)
  - `test_should_exit_with_code_0_on_success` - AC#7
  - `test_should_exit_with_code_1_when_source_missing` - AC#7, BR-002
  - `test_should_exit_with_code_2_on_permission_denied` - AC#7
  - `test_should_exit_with_code_3_on_partial_repair` - AC#7
  - `test_should_exit_with_code_4_on_post_repair_validation_failure` - AC#7, BR-003
  - `test_should_exit_with_code_5_on_manual_merge_needed` - AC#7

- **TestFixWorkflowMissingManifest** (5 tests)
  - `test_should_detect_missing_manifest` - AC#8
  - `test_should_offer_regenerate_option_for_missing_manifest` - AC#8
  - `test_should_regenerate_manifest_from_current_files` - AC#8, SVC-012
  - `test_should_offer_reinstall_option_for_missing_manifest` - AC#8
  - `test_should_abort_without_changes_when_user_chooses_abort` - AC#8

- **TestFixWorkflowUserModifiedFiles** (2 tests)
  - `test_should_prompt_user_for_modified_files` - AC#3, AC#5
  - `test_should_preserve_user_files_with_keep_choice` - AC#5, BR-001

**Coverage Targets:**
- FixCommand orchestrator: 85%+
- End-to-end workflows: 90%+
- Integration scenarios: 90%+

---

## Test Fixtures

New fixtures added to `/mnt/c/Projects/DevForgeAI2/installer/tests/conftest.py`:

### Fixture: corrupted_installation
Creates installation with corrupted files (checksums don't match manifest).

**Returns:**
```python
{
    "manifest_path": Path,
    "corrupted_files": [str, str, ...],
    "root": Path,
}
```

**Usage:**
```python
def test_something(corrupted_installation):
    files = corrupted_installation["corrupted_files"]
    root = corrupted_installation["root"]
```

---

### Fixture: user_modified_installation
Creates installation with user-modified files (devforgeai/specs/, devforgeai/specs/context/).

**Returns:**
```python
{
    "manifest_path": Path,
    "user_modified_files": [str, str, ...],
    "root": Path,
}
```

---

### Fixture: missing_manifest_installation
Creates installation without manifest file.

**Returns:**
```python
{
    "root": Path,
    "expected_manifest_path": Path,
    "existing_files": [str, str, ...],
}
```

---

### Fixture: healthy_installation
Creates healthy installation with valid manifest and matching files.

**Returns:**
```python
{
    "manifest_path": Path,
    "root": Path,
    "file_count": int,
}
```

---

### Fixture: mock_source_package
Creates mock source package with repair files.

**Returns:**
```python
{
    "root": Path,
    "files": [(path, content), (path, content), ...],
}
```

---

## Acceptance Criteria Coverage

| AC | Requirement | Test Module | Test Count |
|----|-----------|----|-----|
| AC#1 | Installation Integrity Validation | test_installation_validator.py | 10 |
| AC#2 | Issue Detection | test_installation_validator.py | 2 |
| AC#3 | User-Modified File Detection | test_installation_validator.py + integration | 6 |
| AC#4 | Automatic Repair | test_repair_service.py + integration | 10 |
| AC#5 | Non-Destructive Mode | test_repair_service.py + integration | 9 |
| AC#6 | Repair Report Display | integration/test_fix_workflow.py | 3 |
| AC#7 | Exit Codes | integration/test_fix_workflow.py | 6 |
| AC#8 | Missing Manifest Handling | integration/test_fix_workflow.py | 5 |

---

## Service Requirements Coverage

| SVC-ID | Description | Test Count | Test Files |
|--------|------------|-----|-----|
| SVC-001 | Validate all files against manifest | 1 | test_installation_validator.py |
| SVC-002 | Detect missing files | 1 | test_installation_validator.py |
| SVC-003 | Detect corrupted files via checksum | 1 | test_installation_validator.py |
| SVC-004 | Detect user-modified files | 4 | test_installation_validator.py |
| SVC-005 | Restore missing files from source | 2 | test_repair_service.py + integration |
| SVC-006 | Replace corrupted files | 2 | test_repair_service.py + integration |
| SVC-007 | Preserve user-modified files unless forced | 2 | test_repair_service.py |
| SVC-008 | Backup user files before overwrite | 1 | test_repair_service.py |
| SVC-009 | Calculate SHA256 checksum | 2 | test_installation_validator.py |
| SVC-010 | Handle large files efficiently | 1 | test_installation_validator.py |
| SVC-011 | Load installation manifest | 6 | test_manifest_manager.py |
| SVC-012 | Regenerate manifest from current files | 9 | test_manifest_manager.py + integration |
| SVC-013 | Update manifest after repair | 6 | test_manifest_manager.py |

**Total Service Requirements Tests:** 41

---

## Test Execution

### Run All Tests

```bash
cd /mnt/c/Projects/DevForgeAI2

# Run all STORY-079 tests
pytest installer/tests/test_installation_validator.py \
        installer/tests/test_repair_service.py \
        installer/tests/test_manifest_manager.py \
        installer/tests/integration/test_fix_workflow.py \
        -v

# Expected: All tests FAIL (Red phase - before implementation)
```

### Run by Module

```bash
# Unit tests - InstallationValidator (16 tests)
pytest installer/tests/test_installation_validator.py -v

# Unit tests - ManifestManager (16 tests)
pytest installer/tests/test_manifest_manager.py -v

# Unit tests - RepairService (16 tests)
pytest installer/tests/test_repair_service.py -v

# Integration tests - Fix Workflow (29 tests)
pytest installer/tests/integration/test_fix_workflow.py -v
```

### Run Specific Test Class

```bash
# Run installation validation basics
pytest installer/tests/test_installation_validator.py::TestInstallationValidatorBasics -v

# Run repair service user interaction
pytest installer/tests/test_repair_service.py::TestRepairServiceUserInteraction -v

# Run fix workflow exit codes
pytest installer/tests/integration/test_fix_workflow.py::TestFixWorkflowExitCodes -v
```

### Run Single Test

```bash
# Run specific test
pytest installer/tests/test_installation_validator.py::TestInstallationValidatorBasics::test_should_detect_missing_files -v

# Run with output capture disabled (see print statements)
pytest installer/tests/test_installation_validator.py::TestInstallationValidatorBasics::test_should_detect_missing_files -v -s
```

### Run with Coverage

```bash
# Generate coverage report
pytest installer/tests/test_installation_validator.py \
        installer/tests/test_repair_service.py \
        installer/tests/test_manifest_manager.py \
        installer/tests/integration/test_fix_workflow.py \
        --cov=installer \
        --cov-report=term-missing \
        --cov-report=html

# Open coverage report
open htmlcov/index.html  # macOS
# or
xdg-open htmlcov/index.html  # Linux
```

---

## Expected Test Results (Red Phase)

**When running before implementation:**

```
FAILED installer/tests/test_installation_validator.py::TestInstallationValidatorBasics::test_should_validate_all_files_when_manifest_valid
FAILED installer/tests/test_installation_validator.py::TestInstallationValidatorBasics::test_should_detect_missing_files
FAILED installer/tests/test_installation_validator.py::TestInstallationValidatorBasics::test_should_detect_corrupted_files
...
FAILED installer/tests/integration/test_fix_workflow.py::TestFixWorkflowExitCodes::test_should_exit_with_code_5_on_manual_merge_needed

======================== 77 failed in 2.34s ========================
```

**Failure reasons (typical):**
- `ModuleNotFoundError: No module named 'installer.installation_validator'` - Service not implemented
- `ImportError: cannot import name 'InstallationValidator'` - Class not defined
- `AttributeError: 'NoneType' object has no attribute 'validate'` - Methods not implemented

---

## Test Coverage Targets

| Component | Target Coverage | Current |
|-----------|-----------------|---------|
| InstallationValidator | 95%+ | TBD |
| ManifestManager | 95%+ | TBD |
| RepairService | 95%+ | TBD |
| FixCommand | 85%+ | TBD |
| ChecksumCalculator | 95%+ | TBD |
| Overall (business logic) | 95%+ | TBD |

---

## Test Design Principles

### 1. AAA Pattern (Arrange, Act, Assert)

All tests follow the Arrange-Act-Assert pattern:

```python
def test_example(self, tmp_project):
    # Arrange: Set up test preconditions
    manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
    manifest_data = {"version": "1.0.0", "files": []}
    manifest_path.write_text(json.dumps(manifest_data))

    # Act: Execute the behavior being tested
    validator = InstallationValidator(str(tmp_project["root"]))
    issues = validator.validate()

    # Assert: Verify the outcome
    assert len(issues) == 0
```

### 2. One Assertion Per Test (When Possible)

Tests focus on a single behavior to make failures clear:

```python
# Good: One assertion, clear intent
assert exit_code == 0

# Avoid: Multiple unrelated assertions
assert exit_code == 0 and report is not None and log_file.exists()
```

### 3. Descriptive Test Names

Test names explain what is being tested and expected outcome:

```python
# Clear: Test name describes scenario and expectation
def test_should_detect_missing_files(self):
    ...

# Avoid: Unclear test names
def test_validation(self):
    ...
```

### 4. Isolated Tests

Each test is independent and can run in any order:

```python
# Each test sets up its own data
def test_case_1(self, tmp_project):
    # Setup specific to test_case_1

def test_case_2(self, tmp_project):
    # Setup specific to test_case_2
    # Does not depend on test_case_1
```

---

## Data Models Being Tested

Tests validate these data structures (used in tests before implementation):

```python
@dataclass
class FileEntry:
    path: str                      # Relative path
    checksum: str                  # SHA256 hash (64 hex chars)
    size: int                      # File size in bytes
    is_user_modifiable: bool       # User can modify this file

@dataclass
class InstallManifest:
    version: str                   # Semantic version
    created_at: str                # ISO8601 datetime
    files: list                    # List of FileEntry dicts
    schema_version: int = 1        # Schema version

@dataclass
class ValidationIssue:
    path: str                      # File with issue
    issue_type: str                # MISSING, CORRUPTED, WRONG_VERSION, EXTRA
    expected: str = None           # Expected value (checksum, size)
    actual: str = None             # Actual value found
    severity: str = None           # CRITICAL, HIGH, MEDIUM, LOW
    is_user_modified: bool = False # Appears to be user-modified

@dataclass
class RepairReport:
    timestamp: str                 # When repair was run
    total_files_checked: int       # Files validated
    issues_found: int              # Issues detected
    issues_fixed: int              # Issues repaired
    issues_skipped: int            # Issues skipped by user
    issues_remaining: int          # Issues requiring manual intervention
    exit_code: int                 # 0, 1, 2, 3, 4, or 5
```

---

## Performance Requirements

Tests validate these performance targets:

| Requirement | Target | Test |
|-------------|--------|------|
| Validation for 500 files | < 30 seconds | test_should_complete_validation_within_30_seconds |
| Large file checksum (100MB) | < 5 seconds | test_should_handle_large_file_checksums |
| Healthy installation detection | Quick (no issues) | test_should_detect_no_issues_in_healthy_installation |

---

## Notes for Implementation

1. **Manifest Location:** `devforgeai/.install-manifest.json` (required)

2. **Checksum Algorithm:** SHA256 (64 hex character string)

3. **User-Modifiable Paths:**
   - `devforgeai/specs/` (all files)
   - `devforgeai/specs/context/` (all files)
   - Other paths in manifest with `is_user_modifiable: true`

4. **Issue Severity Levels:**
   - `CRITICAL`: Missing files (required for function)
   - `HIGH`: Corrupted core files
   - `MEDIUM`: Corrupted optional files
   - `LOW`: Extra files, warnings

5. **Exit Codes:**
   - `0`: Success (no issues or all fixed)
   - `1`: Missing source package
   - `2`: Permission denied
   - `3`: Partial repair (some issues remain)
   - `4`: Post-repair validation failed
   - `5`: Manual merge needed (user-modified files)

---

## Summary

- **Total Tests:** 77
- **Test Modules:** 4
- **Test Classes:** 18
- **Fixtures:** 5 new
- **AC Coverage:** 8/8 acceptance criteria
- **SVC Coverage:** 13/13 service requirements
- **Expected Status:** ALL FAILING (Red phase - before implementation)

---

**Document Version:** 1.0
**Last Updated:** 2025-12-06
**Story:** STORY-079 - Fix/Repair Installation Mode
