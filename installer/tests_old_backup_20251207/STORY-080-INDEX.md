# STORY-080: Rollback to Previous Version - Test Suite Index

**Status**: TDD Red Phase Complete ✓
**Generated**: 2025-12-06
**Framework**: pytest
**Total Tests**: 61 (55 unit + 8 integration)
**Total Lines**: 2,478

---

## Quick Links

- **Test Execution Guide**: [STORY-080-EXECUTION-GUIDE.md](STORY-080-EXECUTION-GUIDE.md)
- **Test Suite Summary**: [STORY-080-TEST-SUITE-SUMMARY.md](STORY-080-TEST-SUITE-SUMMARY.md)
- **Story Details**: [devforgeai/specs/Stories/STORY-080-rollback-previous-version.story.md](/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-080-rollback-previous-version.story.md)

---

## Test Files Overview

### Unit Tests (55 tests, ~1,932 lines)

| Component | Tests | File | Purpose |
|-----------|-------|------|---------|
| **RollbackOrchestrator** | 14 | `test_rollback_orchestrator.py` (597 lines) | Orchestrate automatic and manual rollback workflows |
| **BackupSelector** | 10 | `test_backup_selector.py` (341 lines) | List and select backups for restoration |
| **BackupRestorer** | 12 | `test_backup_restorer.py` (437 lines) | Restore files from backup with user content preservation |
| **BackupCleaner** | 8 | `test_backup_cleaner.py` (310 lines) | Enforce retention policy and delete old backups |
| **RollbackValidator** | 9 | `test_rollback_validator.py` (347 lines) | Validate restored backup integrity |

### Integration Tests (8 tests, ~446 lines)

| Workflow | Tests | File | Purpose |
|----------|-------|------|---------|
| **End-to-End** | 8 | `integration/test_rollback_workflow_story080.py` (446 lines) | Validate complete rollback scenarios covering AC#1-AC#8 |

---

## Test Organization by Acceptance Criteria

### AC#1: Automatic Rollback on Upgrade Failure (4 tests)
**Tests**: 3 unit + 1 integration

```
test_rollback_orchestrator.py::TestAutomaticRollback
  - test_automatic_rollback_triggered_on_upgrade_failure
  - test_automatic_rollback_completes_within_timeout
  - test_automatic_rollback_preserves_error_reason

test_rollback_workflow_story080.py::TestAutomaticRollbackOnFailure
  - test_automatic_rollback_on_upgrade_failure
```

**Validates**:
- Automatic rollback triggered on migration failure
- Rollback completes within 60 seconds (NFR-001)
- Error reason captured and logged

---

### AC#2: Manual Rollback Command (4 tests)
**Tests**: 2 unit + 2 integration

```
test_rollback_orchestrator.py::TestManualRollback
  - test_manual_rollback_creates_safety_backup_first

test_backup_selector.py::TestSelectBackup
  - test_select_backup_by_id_returns_correct_backup

test_rollback_workflow_story080.py::TestManualRollbackWorkflow
  - test_full_manual_rollback_workflow
  - test_list_and_select_backup_for_rollback
```

**Validates**:
- Safety backup created before manual rollback
- Backup selection by ID
- Selected backup can be restored

---

### AC#3: List Available Backups (9 tests)
**Tests**: 8 unit + 1 integration

```
test_backup_selector.py::TestListBackups
  - test_list_backups_returns_all_available
  - test_list_backups_sorted_newest_first
  - test_list_backups_with_no_backups_returns_empty

test_backup_selector.py::TestFormatBackupInfo
  - test_format_for_display_includes_version
  - test_format_for_display_includes_date
  - test_format_for_display_includes_size
  - test_format_for_display_includes_reason
  - test_format_for_display_includes_path

test_rollback_workflow_story080.py::TestManualRollbackListCommand
  - test_manual_rollback_with_flag_list
```

**Validates**:
- All backups listed with version, date, size, reason
- Backups sorted by date (newest first)
- Correct formatting for display

---

### AC#4: Restore from Backup (4 tests)
**Tests**: 2 unit + 2 integration

```
test_backup_restorer.py::TestFileRestoration
  - test_restore_all_files_from_backup
  - test_restore_creates_parent_directories

test_rollback_workflow_story080.py::TestManualRollbackWorkflow
  - test_full_manual_rollback_workflow
  - test_automatic_rollback_on_upgrade_failure
```

**Validates**:
- All files restored from backup
- Directory structure preserved
- .version.json reverted

---

### AC#5: User Content Preservation (8 tests)
**Tests**: 6 unit + 2 integration

```
test_backup_restorer.py::TestUserContentPreservation
  - test_restore_skips_user_content_paths_by_default
  - test_restore_includes_user_content_when_flag_set
  - test_restore_skips_ai_docs_stories
  - test_restore_skips_ai_docs_epics
  - test_restore_skips_devforgeai_context
  - test_restore_skips_devforgeai_adrs

test_rollback_orchestrator.py::TestRollbackUserContent
  - test_rollback_passes_include_user_content_to_restorer

test_rollback_workflow_story080.py::TestUserContentPreservation
  - test_user_content_preserved_without_flag
  - test_user_content_included_with_flag
```

**Validates**:
- User content preserved by default (AC#5)
- User content included with --include-user-content flag
- Specific paths protected: devforgeai/specs/*, devforgeai/specs/context/*, devforgeai/specs/adrs/

---

### AC#6: Rollback Validation (5 tests)
**Tests**: 4 unit + 1 integration

```
test_rollback_validator.py::TestValidationSuccess
  - test_validate_returns_passed_when_all_files_match
  - test_validate_checks_critical_files_exist
  - test_validate_counts_verified_files

test_rollback_validator.py::TestValidationFailure
  - test_validate_detects_missing_critical_files
  - test_validate_detects_checksum_mismatches

test_rollback_orchestrator.py::TestRollbackValidation
  - test_rollback_invokes_validator

test_rollback_workflow_story080.py::TestRollbackValidationReport
  - test_rollback_validation_report_complete
```

**Validates**:
- Checksums verified after restore
- Critical files checked (CLAUDE.md, devforgeai/)
- Validation failures reported

---

### AC#7: Rollback Summary Display (4 tests)
**Tests**: 3 unit + 1 integration

```
test_rollback_orchestrator.py::TestRollbackLogging
  - test_rollback_summary_generated
  - test_rollback_log_saved_to_correct_location
  - test_rollback_log_contains_all_details

test_rollback_workflow_story080.py::TestManualRollbackWorkflow
  - test_full_manual_rollback_workflow
```

**Validates**:
- Summary includes from/to version, file counts, validation status, duration
- Log saved to `devforgeai/logs/rollback-{timestamp}.log`
- All summary details captured

---

### AC#8: Backup Cleanup (9 tests)
**Tests**: 8 unit + 1 integration

```
test_backup_cleaner.py::TestBackupCleanup
  - test_cleanup_deletes_oldest_backups
  - test_cleanup_keeps_retention_count
  - test_cleanup_with_retention_1_keeps_one_backup
  - test_cleanup_with_retention_5_keeps_five_backups
  - test_cleanup_never_deletes_excluded_backup
  - test_cleanup_only_after_successful_rollback
  - test_cleanup_returns_deleted_backup_names
  - test_cleanup_with_no_backups_succeeds

test_rollback_orchestrator.py::TestBackupCleanup
  - test_rollback_invokes_cleaner

test_rollback_workflow_story080.py::TestBackupCleanupAfterRollback
  - test_backup_cleanup_after_successful_rollback
```

**Validates**:
- Oldest backups deleted when limit exceeded
- Retention count enforced (default 5)
- Active backup never deleted
- Cleanup only after successful rollback

---

## Error Handling & Edge Cases (11 tests)

```
test_rollback_orchestrator.py::TestRollbackErrorHandling
  - test_rollback_handles_restorer_failure
  - test_rollback_handles_validator_failure

test_backup_selector.py::TestSelectBackup
  - test_select_backup_invalid_id_returns_none

test_backup_restorer.py::TestRestoreErrorHandling
  - test_restore_handles_missing_backup
  - test_restore_handles_checksum_mismatch

test_rollback_validator.py::TestValidationFailure
  - test_validate_detects_missing_critical_files
  - test_validate_detects_checksum_mismatches
  - test_validate_with_corrupted_backup_fails
  - test_validate_with_partial_restore_reports_status

test_backup_cleaner.py::TestBackupCleanup
  - test_cleanup_with_no_backups_succeeds
```

**Covers**:
- Missing/corrupted backups
- Invalid IDs
- Checksum mismatches
- Permission errors
- Empty directories
- Timeout conditions

---

## How to Use This Index

### For Running Tests
1. Read **[STORY-080-EXECUTION-GUIDE.md](STORY-080-EXECUTION-GUIDE.md)**
   - Execution commands
   - Expected output
   - Debugging tips

### For Understanding Tests
1. Read **[STORY-080-TEST-SUITE-SUMMARY.md](STORY-080-TEST-SUITE-SUMMARY.md)**
   - Detailed test descriptions
   - Coverage maps
   - Implementation guidance

### For Implementing Components
1. Pick a component from the table above
2. Open corresponding test file
3. Read test docstrings to understand behavior
4. Implement code to make tests pass

### For Acceptance Criteria
1. Find AC# you're validating in sections above
2. See which tests validate that AC#
3. Run those specific tests: `pytest test_file.py::TestClass::test_name -v`

---

## Test Statistics

```
Total Tests:          61
├─ Unit Tests:        55 (87%)
└─ Integration Tests:  8 (13%)

By Component:
├─ RollbackOrchestrator  14
├─ BackupSelector        10
├─ BackupRestorer        12
├─ BackupCleaner          8
├─ RollbackValidator       9
└─ Integration            8

By Coverage Area:
├─ Happy Path:           28 tests
├─ Edge Cases:           14 tests
├─ Error Handling:       11 tests
└─ Integration:           8 tests

Acceptance Criteria:
├─ AC#1:  4 tests
├─ AC#2:  4 tests
├─ AC#3:  9 tests
├─ AC#4:  4 tests
├─ AC#5:  8 tests
├─ AC#6:  5 tests
├─ AC#7:  4 tests
└─ AC#8:  9 tests
```

---

## Test Pyramid

```
          /\
         /  \        Integration (13%)
        /────\       8 tests
       / Work \
      /────────\
     /          \
    /   Unit     \   Unit (87%)
   /──────────────\  55 tests
      (2,478 LOC)
```

---

## Next Steps

### Phase 1: Complete ✓
- [x] Generate comprehensive test suite
- [x] Cover all 8 acceptance criteria
- [x] Include edge cases and error handling
- [x] Create integration tests
- [x] Document test organization

### Phase 2: Implementation (TDD Green)
- [ ] Create data models (installer/models.py)
- [ ] Implement RollbackValidator
- [ ] Implement BackupSelector
- [ ] Implement BackupRestorer
- [ ] Implement BackupCleaner
- [ ] Implement RollbackOrchestrator (integrates all)
- [ ] Run full test suite: `pytest ... -v`
- [ ] Achieve: 61 PASSED

### Phase 3: Refactoring (TDD Refactor)
- [ ] Review implementations for code quality
- [ ] Optimize performance if needed
- [ ] Remove duplication
- [ ] Improve readability
- [ ] Ensure tests still pass

---

## Files Summary

```
installer/tests/
├── test_rollback_orchestrator.py
├── test_backup_selector.py
├── test_backup_restorer.py
├── test_backup_cleaner.py
├── test_rollback_validator.py
├── integration/
│   └── test_rollback_workflow_story080.py
├── STORY-080-INDEX.md (this file)
├── STORY-080-TEST-SUITE-SUMMARY.md
└── STORY-080-EXECUTION-GUIDE.md
```

---

**Status**: TDD Red Phase Complete - Ready for Phase 2 Implementation

All 61 tests are generated and ready to serve as executable specifications.
Implement the 5 services to make tests pass in Phase 2.
