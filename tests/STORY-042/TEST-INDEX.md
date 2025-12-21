# STORY-042: Test Index - All 101 Tests

Complete list of all test functions organized by test file and category.

## AC Tests (25 tests) - test-ac-migration-files.sh

### AC-1: Copy .claude/ to src/claude/ (5 tests)
- `test_ac1_claude_directory_exists()` - src/claude/ directory created
- `test_ac1_subdirectories_preserved()` - All subdirectories preserved
- `test_ac1_file_count_approximately_370()` - ~370 files (±10)
- `test_ac1_nested_structure_preserved()` - Deep structure preserved
- `test_ac1_original_unchanged()` - Original .claude/ unchanged

### AC-2: Copy devforgeai/ content (5 tests)
- `test_ac2_devforgeai_directory_exists()` - src/devforgeai/ directory exists
- `test_ac2_allowed_subdirs_only()` - Only allowed subdirectories present
- `test_ac2_required_subdirs_present()` - Required subdirectories present
- `test_ac2_file_count_approximately_80()` - ~80 files (±10)
- `test_ac2_subdirectory_file_counts()` - Subdirectory counts correct

### AC-3: Copy CLAUDE.md template (5 tests)
- `test_ac3_claude_md_copied()` - src/CLAUDE.md file exists
- `test_ac3_checksum_matches_exactly()` - SHA256 checksum matches
- `test_ac3_file_size_matches()` - File size matches exactly
- `test_ac3_original_unchanged()` - Original CLAUDE.md still exists
- `test_ac3_template_marker_present()` - Template marker comment added

### AC-4: Checksum verification (5 tests)
- `test_ac4_checksums_file_exists()` - checksums.txt manifest created
- `test_ac4_checksum_count_approximately_450()` - ~450 checksum lines (±10)
- `test_ac4_checksum_format_valid()` - SHA256 format valid
- `test_ac4_checksums_verified_with_shasum()` - shasum verification successful
- `test_ac4_validation_report_generated()` - Migration report generated

### AC-5: Exclude backup/artifacts (7 tests)
- `test_ac5_no_backup_files()` - No .backup* files
- `test_ac5_no_temporary_files()` - No .tmp/.temp files
- `test_ac5_no_python_bytecode()` - No __pycache__//*.pyc
- `test_ac5_no_egg_info()` - No *.egg-info
- `test_ac5_no_coverage_artifacts()` - No htmlcov/.coverage
- `test_ac5_no_node_modules()` - No node_modules
- `test_ac5_no_git_directories()` - No .git directories

### AC-6: Git tracking (4 tests)
- `test_ac6_git_initialized()` - Git repository initialized
- `test_ac6_files_staged_approximately_450()` - ~450 files staged (±10)
- `test_ac6_no_binary_files_large()` - No binary files >1MB
- `test_ac6_git_status_shows_additions()` - Git status shows additions

### AC-7: Preserve originals (5 tests)
- `test_ac7_original_claude_exists()` - Original .claude/ exists
- `test_ac7_original_devforgeai_exists()` - Original devforgeai/ exists
- `test_ac7_original_claude_unchanged_filecount()` - File count unchanged
- `test_ac7_no_symlinks_in_src()` - No symlinks (true copies)
- `test_ac7_commands_still_work()` - DevForgeAI commands functional

---

## BR Tests (17 tests) - test-business-rules.sh

### BR-001: Originals unchanged (4 tests)
- `test_br001_original_folders_exist()` - Both original folders exist
- `test_br001_file_count_unchanged()` - File counts unchanged
- `test_br001_directory_structure_intact()` - All subdirectories intact
- `test_br001_no_modifications_to_files()` - Files readable and unchanged

### BR-002: Source files only (6 tests)
- `test_br002_no_qa_reports()` - qa/reports/ excluded
- `test_br002_no_rca_files()` - RCA/ excluded
- `test_br002_no_adrs()` - adrs/ excluded
- `test_br002_no_feedback_imported()` - feedback/imported/ excluded
- `test_br002_no_logs()` - logs/ excluded
- `test_br002_source_files_only()` - Source files present

### BR-003: File integrity 100% (4 tests)
- `test_br003_no_truncated_files()` - No file truncation
- `test_br003_checksums_all_valid()` - All checksums valid format
- `test_br003_no_empty_files_incorrectly_copied()` - No unexpected empty files
- `test_br003_sample_checksum_verification()` - Sample file checksum verified

### BR-004: Exclusion patterns (4 tests)
- `test_br004_backup_patterns_excluded()` - Backup patterns excluded
- `test_br004_artifact_patterns_excluded()` - Artifact patterns excluded
- `test_br004_log_files_excluded()` - Log files excluded
- `test_br004_pycache_excluded()` - __pycache__ excluded

### BR-005: Idempotent (3 tests)
- `test_br005_idempotent_safe_to_rerun()` - Safe to re-run
- `test_br005_skip_unchanged_files()` - Skip files with matching checksums
- `test_br005_detect_and_handle_conflicts()` - Handle conflicts

### BR-006: Fail fast (3 tests)
- `test_br006_corruption_detection()` - Corruption detection enabled
- `test_br006_atomic_per_directory()` - Atomic per directory
- `test_br006_error_logging()` - Error logging enabled

---

## EC Tests (28 tests) - test-edge-cases.sh

### EC-1: Existing files (4 tests)
- `test_ec1_detects_existing_files()` - Existing files detected
- `test_ec1_compares_checksums_for_existing()` - Checksums compared
- `test_ec1_handles_modified_files()` - Modified files handled
- `test_ec1_skips_matching_files()` - Matching files skipped

### EC-2: Permission errors (4 tests)
- `test_ec2_handles_unreadable_source()` - Unreadable source handled
- `test_ec2_handles_unwritable_destination()` - Unwritable destination handled
- `test_ec2_reports_permission_errors()` - Permission errors reported
- `test_ec2_continues_after_permission_error()` - Continues after error

### EC-3: Partial copy (4 tests)
- `test_ec3_detects_incomplete_copy()` - Incomplete copy detected
- `test_ec3_recovery_checkpoint_file()` - Checkpoint file created
- `test_ec3_provides_resume_command()` - Resume command provided
- `test_ec3_skip_completed_files()` - Completed files skipped

### EC-4: Corruption (4 tests)
- `test_ec4_detects_corruption_immediately()` - Corruption detected
- `test_ec4_halts_on_first_corruption()` - Halts on first corruption
- `test_ec4_reports_corruption_details()` - Corruption details reported
- `test_ec4_provides_rollback_command()` - Rollback command provided

### EC-5: Symlinks (4 tests)
- `test_ec5_detects_symlinks()` - Symlinks detected
- `test_ec5_follows_symlink_target()` - Symlink targets followed
- `test_ec5_logs_symlink_operations()` - Symlink ops logged
- `test_ec5_no_broken_links_in_destination()` - No broken links

### EC-6: Large files (4 tests)
- `test_ec6_detects_large_files()` - Large files detected
- `test_ec6_uses_streaming_copy()` - Streaming copy used
- `test_ec6_progress_reporting()` - Progress reported
- `test_ec6_chunked_checksum_validation()` - Chunked checksums

### EC-7: Case conflicts (4 tests)
- `test_ec7_detects_case_conflicts()` - Case conflicts detected
- `test_ec7_provides_conflict_resolution()` - Resolution provided
- `test_ec7_prevents_silent_overwrite()` - Silent overwrite prevented
- `test_ec7_logs_resolution_choice()` - Resolution logged

---

## CONF Tests (31 tests) - test-migration-config.sh

### MigrationScript Component (7 tests)
- `test_migration_script_exists()` - Script exists and executable
- `test_migration_script_executable()` - Script has execute permission
- `test_migration_script_has_shebang()` - Has bash shebang
- `test_migration_script_copy_function()` - Copy function implemented
- `test_migration_script_exclusion_function()` - Exclusion function implemented
- `test_migration_script_checksum_function()` - Checksum function implemented
- `test_migration_script_git_function()` - Git function implemented

### MigrationConfig Component (6 tests)
- `test_config_file_exists()` - Configuration file exists
- `test_config_valid_json()` - Valid JSON format
- `test_config_sources_defined()` - 3 sources defined
- `test_config_exclusion_patterns()` - ≥8 exclusion patterns
- `test_config_validation_thresholds()` - Validation thresholds set
- `test_config_file_count_expectations()` - File count expectations

### ChecksumManifest Component (5 tests)
- `test_checksums_file_exists()` - Checksums file created
- `test_checksums_line_count()` - ~450 lines
- `test_checksums_format_sha256()` - SHA256 format valid
- `test_checksums_verifiable()` - Verifiable with shasum
- `test_checksums_unique()` - All checksums unique

### MigrationLogger Component (6 tests)
- `test_migration_log_exists()` - Log file created
- `test_migration_log_copy_entries()` - COPY: entries logged
- `test_migration_log_validation_entries()` - VALIDATE: entries logged
- `test_migration_log_exclusion_entries()` - EXCLUDE: entries logged
- `test_migration_log_summary()` - Summary statistics logged
- `test_migration_log_timestamps()` - Timestamps in log

### NFR Tests (5 tests)
- `test_nfr_performance_copy()` - Copy <2 minutes
- `test_nfr_performance_checksums()` - Checksums <1 minute
- `test_nfr_memory_usage()` - Memory <50 MB
- `test_nfr_atomicity()` - Atomic per directory
- `test_nfr_permissions_preserved()` - Permissions preserved

---

## Test Execution

### Run All Tests
```bash
bash tests/STORY-042/run-tests.sh
```

### Run Specific Suite
```bash
# AC tests only
bash tests/STORY-042/run-tests.sh --suite=ac

# BR tests only
bash tests/STORY-042/run-tests.sh --suite=business

# EC tests only
bash tests/STORY-042/run-tests.sh --suite=edge

# CONF tests only
bash tests/STORY-042/run-tests.sh --suite=config
```

### Verbose Output
```bash
bash tests/STORY-042/run-tests.sh --verbose
```

---

## Summary

| Category | Count | File |
|----------|-------|------|
| AC (Acceptance Criteria) | 25 | test-ac-migration-files.sh |
| BR (Business Rules) | 17 | test-business-rules.sh |
| EC (Edge Cases) | 28 | test-edge-cases.sh |
| CONF (Configuration) | 31 | test-migration-config.sh |
| **TOTAL** | **101** | **4 files** |

---

**Generated:** 2025-11-18
**Status:** All tests RED (expected for TDD)
**Ready for:** Phase 2 Implementation
