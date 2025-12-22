# STORY-079: Test Generation - Complete Index

This index provides a complete roadmap to all STORY-079 test files, fixtures, and documentation.

**Generated:** 2025-12-06
**Status:** RED PHASE (TDD) - All 77 tests failing, ready for implementation
**Framework:** pytest
**Language:** Python 3.9+

---

## Navigation

### For Quick Start
👉 **Start here:** [`STORY-079-QUICK-START.md`](./STORY-079-QUICK-START.md)
- Quick test execution commands
- Expected results
- Key patterns

### For Complete Test Documentation
👉 **Full reference:** [`STORY-079-TEST-SUITE.md`](./STORY-079-TEST-SUITE.md)
- All 77 tests documented
- Test class descriptions
- Fixture specifications
- Coverage matrices

### For Implementation Guidance
👉 **Summary & metrics:** [`devforgeai/qa/STORY-079-TEST-GENERATION-SUMMARY.md`](../../devforgeai/qa/STORY-079-TEST-GENERATION-SUMMARY.md)
- Service implementation order
- Coverage analysis
- Quality metrics

---

## Test Files

### 1. Unit Tests: InstallationValidator
**File:** `test_installation_validator.py` (647 lines)

**Purpose:** Test installation integrity validation
- File existence checking
- Checksum verification (SHA256)
- Missing/corrupted file detection
- User-modified file detection
- Performance validation (500 files < 30s)
- Large file handling (100MB < 5s)

**Test Classes:**
```
TestInstallationValidatorBasics (10 tests)
  ✓ test_should_validate_all_files_when_manifest_valid
  ✓ test_should_detect_missing_files
  ✓ test_should_detect_corrupted_files
  ✓ test_should_detect_user_modified_files
  ✓ test_should_detect_extra_files_with_warning_severity
  ✓ test_should_populate_issue_details
  ✓ test_should_complete_validation_within_30_seconds
  ✓ test_should_handle_empty_manifest
  ✓ test_should_handle_large_file_checksums
  ✓ test_should_validate_file_size_mismatch

TestUserModifiedFileDetection (4 tests)
  ✓ test_should_flag_user_modifiable_location_files
  ✓ test_should_detect_recent_modifications
  ✓ test_should_detect_user_specific_content_patterns
  ✓ test_should_provide_diff_preview_for_text_files

TestManifestValidation (2 tests)
  ✓ test_should_validate_manifest_structure
  ✓ test_should_validate_checksums_are_sha256
```

**Covers:** AC#1, AC#2, AC#3, SVC-001-004, SVC-009-010, NFR-001-002

---

### 2. Unit Tests: ManifestManager
**File:** `test_manifest_manager.py` (593 lines)

**Purpose:** Test manifest loading, regeneration, and updating
- Load manifest from JSON
- Handle missing manifest
- Regenerate from current files
- Update checksums after repair
- Atomic write protection
- Large manifest handling (10K+ files)

**Test Classes:**
```
TestManifestManagerLoading (6 tests)
  ✓ test_should_load_valid_manifest
  ✓ test_should_return_none_when_manifest_missing
  ✓ test_should_validate_manifest_structure
  ✓ test_should_parse_file_entries_correctly
  ✓ test_should_handle_corrupted_manifest_json
  ✓ test_should_validate_checksum_format

TestManifestManagerRegeneration (8 tests)
  ✓ test_should_regenerate_manifest_from_current_files
  ✓ test_should_calculate_correct_checksums_during_regeneration
  ✓ test_should_calculate_correct_file_sizes_during_regeneration
  ✓ test_should_mark_user_modifiable_files_during_regeneration
  ✓ test_should_set_created_at_timestamp
  ✓ test_should_exclude_manifest_file_from_regeneration
  ✓ test_should_exclude_backup_files_from_regeneration
  ✓ test_should_handle_empty_directory_during_regeneration

TestManifestManagerUpdating (6 tests)
  ✓ test_should_update_manifest_checksum_after_repair
  ✓ test_should_update_file_size_in_manifest
  ✓ test_should_preserve_is_user_modifiable_flag_during_update
  ✓ test_should_save_updated_manifest_to_disk
  ✓ test_should_handle_atomic_write_protection
  ✓ test_should_handle_very_large_manifest

TestManifestManagerEdgeCases (2 tests - partial)
  ✓ test_should_handle_special_characters_in_paths
```

**Covers:** AC#8, SVC-011-013

---

### 3. Unit Tests: RepairService
**File:** `test_repair_service.py` (559 lines)

**Purpose:** Test repair operations (restore, replace, preserve)
- Restore missing files from source
- Replace corrupted files
- Preserve user-modified files
- Backup before overwrite
- User interaction (4 options)
- Security constraints

**Test Classes:**
```
TestRepairServiceBasics (7 tests)
  ✓ test_should_restore_missing_file_from_source
  ✓ test_should_replace_corrupted_file_with_source_version
  ✓ test_should_preserve_user_modified_files_without_force_flag
  ✓ test_should_backup_user_file_before_overwrite
  ✓ test_should_skip_file_when_user_chooses_keep
  ✓ test_should_restore_original_when_user_chooses_restore
  ✓ test_should_show_diff_for_text_files

TestRepairServiceSecurityConstraints (2 tests)
  ✓ test_should_not_modify_files_outside_devforgeai_directories
  ✓ test_should_only_repair_recognized_devforgeai_files

TestRepairServiceUserInteraction (4 tests)
  ✓ test_should_prompt_user_for_each_user_modified_file
  ✓ test_should_offer_four_user_options_for_modified_files
  ✓ test_should_respect_user_choice_for_each_file
  ✓ test_should_force_repair_all_files_with_force_flag

TestRepairServiceEdgeCases (3 tests)
  ✓ test_should_handle_symlinks_appropriately
  ✓ test_should_handle_directories_in_manifest
  ✓ test_should_handle_empty_source_package
```

**Covers:** AC#4-5, AC#7, SVC-005-008, NFR-004, BR-001

---

### 4. Integration Tests: Fix Workflow
**File:** `integration/test_fix_workflow.py` (730 lines)

**Purpose:** Test end-to-end fix command workflow
- Detect all issue types
- Repair and update manifest
- Generate reports with exit codes
- Handle missing manifest with user options
- User-modified file handling

**Test Classes:**
```
TestFixWorkflowHealthyInstallation (2 tests)
  ✓ test_should_detect_no_issues_in_healthy_installation
  ✓ test_should_exit_with_0_when_no_issues_found

TestFixWorkflowIssueDetection (2 tests)
  ✓ test_should_detect_all_issue_types_during_fix
  ✓ test_should_display_issue_details

TestFixWorkflowRepairOperations (4 tests)
  ✓ test_should_repair_missing_files
  ✓ test_should_replace_corrupted_files
  ✓ test_should_update_manifest_after_repair
  ✓ test_should_log_repair_operations

TestFixWorkflowReporting (3 tests)
  ✓ test_should_generate_repair_report
  ✓ test_should_save_log_file
  ✓ test_should_display_summary_statistics

TestFixWorkflowExitCodes (6 tests)
  ✓ test_should_exit_with_code_0_on_success
  ✓ test_should_exit_with_code_1_when_source_missing
  ✓ test_should_exit_with_code_2_on_permission_denied
  ✓ test_should_exit_with_code_3_on_partial_repair
  ✓ test_should_exit_with_code_4_on_post_repair_validation_failure
  ✓ test_should_exit_with_code_5_on_manual_merge_needed

TestFixWorkflowMissingManifest (5 tests)
  ✓ test_should_detect_missing_manifest
  ✓ test_should_offer_regenerate_option_for_missing_manifest
  ✓ test_should_regenerate_manifest_from_current_files
  ✓ test_should_offer_reinstall_option_for_missing_manifest
  ✓ test_should_abort_without_changes_when_user_chooses_abort

TestFixWorkflowUserModifiedFiles (2 tests)
  ✓ test_should_prompt_user_for_modified_files
  ✓ test_should_preserve_user_files_with_keep_choice
```

**Covers:** AC#1-8 (all), SVC-001-013 (all), NFR-001-004, BR-002-003

---

## Test Fixtures

**File:** `conftest.py` (updated)

All fixtures use `tmp_project` and `tmp_path` pytest built-ins.

### 1. corrupted_installation
```python
{
    "manifest_path": Path,
    "corrupted_files": [str, ...],
    "root": Path,
}
```
Creates installation with wrong checksums.

### 2. user_modified_installation
```python
{
    "manifest_path": Path,
    "user_modified_files": [str, ...],
    "root": Path,
}
```
Creates devforgeai/specs/ and context files with user modifications.

### 3. missing_manifest_installation
```python
{
    "root": Path,
    "expected_manifest_path": Path,
    "existing_files": [str, ...],
}
```
Creates installation without manifest file.

### 4. healthy_installation
```python
{
    "manifest_path": Path,
    "root": Path,
    "file_count": int,
}
```
Valid installation with matching files (10 files).

### 5. mock_source_package
```python
{
    "root": Path,
    "files": [(path, content), ...],
}
```
Mock source files for repair operations.

---

## Documentation Files

### 1. Quick Start Guide
**File:** `STORY-079-QUICK-START.md`

Rapid reference for:
- Test execution commands
- Expected output (RED phase)
- Key test patterns
- Performance targets
- Quick navigation

### 2. Complete Test Suite Documentation
**File:** `STORY-079-TEST-SUITE.md`

Comprehensive reference including:
- All 77 tests documented
- Test class descriptions
- Fixture details
- AC/SVC coverage matrices
- Execution instructions
- Test design principles
- Data models

### 3. Generation Summary
**File:** `devforgeai/qa/STORY-079-TEST-GENERATION-SUMMARY.md`

Analysis document with:
- Test metrics and statistics
- Coverage analysis
- Quality assessment
- Service implementation order
- Compliance checklist

### 4. This Index
**File:** `STORY-079-INDEX.md` (this file)

Navigation and quick reference to all files.

---

## Quick Execution

### All Tests (RED phase - expect failures)
```bash
pytest installer/tests/test_*.py installer/tests/integration/test_*.py -v
# Expected: 77 failed
```

### By Module
```bash
pytest installer/tests/test_installation_validator.py -v      # 16 tests
pytest installer/tests/test_manifest_manager.py -v            # 16 tests
pytest installer/tests/test_repair_service.py -v              # 16 tests
pytest installer/tests/integration/test_fix_workflow.py -v    # 29 tests
```

### With Coverage
```bash
pytest installer/tests/ --cov=installer --cov-report=html
```

### Single Test
```bash
pytest installer/tests/test_installation_validator.py::TestInstallationValidatorBasics::test_should_detect_missing_files -v
```

---

## Coverage Summary

### Acceptance Criteria
| AC# | Tests | Status |
|-----|-------|--------|
| AC#1 | 10 | RED |
| AC#2 | 2 | RED |
| AC#3 | 6 | RED |
| AC#4 | 10 | RED |
| AC#5 | 9 | RED |
| AC#6 | 3 | RED |
| AC#7 | 6 | RED |
| AC#8 | 5 | RED |
| **TOTAL** | **51** | **100%** |

### Service Requirements
| Service | Tests | Status |
|---------|-------|--------|
| SVC-001-004 | 8 | RED |
| SVC-005-008 | 8 | RED |
| SVC-009-010 | 3 | RED |
| SVC-011-013 | 21 | RED |
| **TOTAL** | **40** | **100%** |

### Quality Requirements
| Type | Tests | Status |
|------|-------|--------|
| Non-Functional (NFR) | 4 | RED |
| Business Rules (BR) | 3 | RED |
| **TOTAL** | **7** | **100%** |

### Overall Coverage
```
Total Tests:     77
AC Coverage:     8/8 (100%)
SVC Coverage:    13/13 (100%)
NFR Coverage:    4/4 (100%)
BR Coverage:     3/3 (100%)
```

---

## Implementation Roadmap

### Phase 1: Implement Core Services
1. **ChecksumCalculator**
   - SVC-009, SVC-010
   - File: `installer/checksum_calculator.py`
   - Tests will start passing: 2/77

2. **ManifestManager**
   - SVC-011, SVC-012, SVC-013
   - File: `installer/manifest_manager.py`
   - Tests will start passing: 16/77 total

3. **InstallationValidator**
   - SVC-001-004, SVC-009-010
   - File: `installer/installation_validator.py`
   - Tests will start passing: 32/77 total

### Phase 2: Implement Repair Logic
4. **RepairService**
   - SVC-005-008
   - File: `installer/repair_service.py`
   - Tests will start passing: 48/77 total

### Phase 3: Implement Orchestrator
5. **FixCommand**
   - AC#1-8, all exit codes
   - File: `installer/fix_command.py`
   - Tests will start passing: 77/77 (all passing!)

---

## Expected Test Results

### Initial Run (RED phase)
```
FAILED installer/tests/test_installation_validator.py::...
FAILED installer/tests/test_manifest_manager.py::...
FAILED installer/tests/test_repair_service.py::...
FAILED installer/tests/integration/test_fix_workflow.py::...

======================== 77 failed in 2.34s ========================
```

### After Implementation (GREEN phase)
```
PASSED installer/tests/test_installation_validator.py::...
PASSED installer/tests/test_manifest_manager.py::...
PASSED installer/tests/test_repair_service.py::...
PASSED installer/tests/integration/test_fix_workflow.py::...

======================== 77 passed in 2.45s ========================
```

---

## File Organization

```
installer/tests/
├── test_installation_validator.py      (647 lines, 16 tests)
├── test_repair_service.py              (559 lines, 16 tests)
├── test_manifest_manager.py            (593 lines, 16 tests)
├── integration/
│   └── test_fix_workflow.py            (730 lines, 29 tests)
├── conftest.py                         (UPDATED: +5 fixtures)
├── STORY-079-TEST-SUITE.md             (Complete docs)
├── STORY-079-QUICK-START.md            (Quick ref)
└── STORY-079-INDEX.md                  (This file)

devforgeai/qa/
└── STORY-079-TEST-GENERATION-SUMMARY.md (Metrics & analysis)
```

---

## Related Files

### Story Definition
- `devforgeai/specs/Stories/STORY-079-fix-repair-installation-mode.story.md`

### Context Files
- `devforgeai/specs/context/tech-stack.md` - Framework specification
- `devforgeai/specs/context/source-tree.md` - File structure rules
- `devforgeai/specs/context/coding-standards.md` - Code quality

### Implementation Files (To be created)
- `installer/checksum_calculator.py` - SHA256 calculation
- `installer/installation_validator.py` - Validation logic
- `installer/manifest_manager.py` - Manifest management
- `installer/repair_service.py` - Repair operations
- `installer/fix_command.py` - Command orchestration

---

## Key Concepts

### Installation Manifest
Located at: `devforgeai/.install-manifest.json`

Structure:
```json
{
  "version": "1.0.0",
  "created_at": "2025-11-25T10:00:00Z",
  "schema_version": 1,
  "files": [
    {
      "path": "relative/path.txt",
      "checksum": "sha256_hash_64_chars",
      "size": 12345,
      "is_user_modifiable": false
    }
  ]
}
```

### User-Modifiable Paths
- `devforgeai/specs/**/*` - User stories and documents
- `devforgeai/specs/context/**/*` - Configuration
- Any file marked `is_user_modifiable: true`

### Issue Types
- `MISSING` - File in manifest but not on disk
- `CORRUPTED` - Checksum mismatch
- `WRONG_VERSION` - Version mismatch
- `EXTRA` - File on disk but not in manifest

### Exit Codes
- `0` - Success
- `1` - Missing source
- `2` - Permission denied
- `3` - Partial repair
- `4` - Post-repair validation failed
- `5` - Manual merge needed

---

## TDD Workflow

### Phase 1: RED (Current)
✓ Write failing tests first
✓ Tests define requirements
✓ All 77 tests FAIL (no implementation)

### Phase 2: GREEN
- Implement services
- Tests start PASSING
- One by one, turn RED→GREEN

### Phase 3: REFACTOR
- Improve code quality
- Keep tests PASSING
- Final cleanup and optimization

---

## Support & Next Steps

### To Get Started
1. Read: `STORY-079-QUICK-START.md`
2. Review: `STORY-079-TEST-SUITE.md`
3. Run: `pytest installer/tests/ -v`
4. Read: Implementation guidance in summary

### To Implement
1. Follow implementation roadmap above
2. Run tests after each service
3. Fix failures incrementally
4. Keep tests passing during refactoring

### For Questions
- Check test files for expected behavior
- Review story AC and tech spec
- Look at test fixtures for examples

---

**Document Version:** 1.0
**Created:** 2025-12-06
**For Story:** STORY-079 - Fix/Repair Installation Mode
**Phase:** Red (Test-First Development)
**Status:** Complete & Ready for Implementation

---

**Quick Links:**
- 📖 [Quick Start](./STORY-079-QUICK-START.md)
- 📚 [Full Test Suite Docs](./STORY-079-TEST-SUITE.md)
- 📊 [Generation Summary](./devforgeai/qa/STORY-079-TEST-GENERATION-SUMMARY.md)
- 🎯 [Run All Tests](#quick-execution)
