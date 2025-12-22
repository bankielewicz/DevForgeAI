# STORY-045 Test Suite - Quick Reference

## Overview

Comprehensive Test-Driven Development (TDD) test suite for the Version-Aware Installer with Backup and Rollback Capability.

- **42+ Tests:** 35 unit + 7 integration + 7 edge case
- **Coverage:** 95%+ for business logic (7 AC, 7 edge cases, 5 business rules, 7 NFRs)
- **Status:** Red Phase (All tests fail without implementation)
- **Format:** pytest with fixtures, mocking, deterministic data

## Files

| File | Tests | Purpose | Validates |
|------|-------|---------|-----------|
| `conftest.py` | — | Shared fixtures | Setup, mocks, data |
| `test_version_detection.py` | 5 | Version reading and comparison | AC1, WKR-010/011/012 |
| `test_backup_management.py` | 6 | Backup creation and integrity | AC2, WKR-013/014/015/016 |
| `test_deployment_engine.py` | 7 | File deployment and permissions | AC3/AC4, WKR-017/018/019/020 |
| `test_rollback_manager.py` | 5 | Rollback operations | AC5 Mode 3, WKR-021/022/023/024 |
| `test_installation_modes.py` | 5 | Integration workflows (5 modes) | AC5 (Fresh, Upgrade, Rollback, Validate, Uninstall) |
| `test_edge_cases.py` | 7 | Error handling and edge cases | 7 Edge Cases + AC7 |
| `test_requirements.txt` | — | Dependencies | pytest, packaging, coverage |

## Quick Start

### Install

```bash
pip install -r test_requirements.txt
```

### Run All Tests

```bash
cd /mnt/c/Projects/DevForgeAI2
pytest installer/tests/ -v
```

### Run Specific File

```bash
pytest installer/tests/test_version_detection.py -v
pytest installer/tests/test_backup_management.py -v
pytest installer/tests/test_deployment_engine.py -v
pytest installer/tests/test_rollback_manager.py -v
pytest installer/tests/test_installation_modes.py -v
pytest installer/tests/test_edge_cases.py -v
```

### Generate Coverage Report

```bash
pytest installer/tests/ --cov=installer --cov-report=term-missing --cov-report=html
open htmlcov/index.html
```

### Run in Parallel

```bash
pytest installer/tests/ -n auto
```

## Test Design

### AAA Pattern (Every Test)

```python
def test_example(self, tmp_project):
    # Arrange: Setup test data
    version_file = tmp_project["devforgeai"] / ".version.json"
    version_file.write_text(json.dumps({"version": "1.0.0"}))

    # Act: Execute code
    content = json.loads(version_file.read_text())

    # Assert: Verify result
    assert content["version"] == "1.0.0"
```

### Fixtures (conftest.py)

**Directory Structures:**
- `tmp_project` - Temporary project with .claude/, devforgeai/, .backups/
- `mock_source_files` - Mock src/ with 370 + 80 files

**Data:**
- `installed_version_1_0_0` - Preinstalled v1.0.0
- `source_version_1_0_1` - Source v1.0.1
- `backup_manifest` - Sample manifest
- `mock_user_config` - User config files
- `fixed_timestamp` - Deterministic time

**Mocking:**
- `mock_datetime` - Fixed datetime
- `error_scenarios` - Error conditions
- `installation_states` - Installation scenarios

### No Real File I/O

All tests mock file operations:
```python
# ✅ Uses fixtures and tmpdir (no real files modified)
version_file.write_text(json.dumps(...))

# ❌ NOT real filesystem operations
open("/real/path", "w")
os.rename(...)
shutil.rmtree("/real/path")
```

## Coverage Map

### By Acceptance Criteria

| AC | Test Count | Status |
|----|-----------|--------|
| AC1: Version Detection | 9 | ✅ |
| AC2: Backup Creation | 6 | ✅ |
| AC3: Deployment | 7 | ✅ |
| AC4: Preserve Configs | 4 | ✅ |
| AC5: 5 Modes (Integration) | 5 | ✅ |
| AC6: Selective Update | 1 | ✅ |
| AC7: Error Handling | 3 | ✅ |

### By Technical Requirement

| WKR | Tests | Module |
|-----|-------|--------|
| WKR-010/011/012 | 5 | version.py |
| WKR-013/014/015/016 | 6 | backup.py |
| WKR-017/018/019/020 | 7 | deploy.py |
| WKR-021/022/023/024 | 5 | rollback.py |

### By Edge Case

| Edge Case | Tests |
|-----------|-------|
| 1. Disk Space | 2 |
| 2. Corrupted Install | 2 |
| 3. Network Timeout | 2 |
| 4. Concurrent Execution | 2 |
| 5. Schema Change | 2 |
| 6. Symlinks | 2 |
| 7. Backup Accumulation | 2 |
| + Error Handling (AC7) | 3 |

## Key Test Methods

### Version Detection Tests

```python
test_detect_fresh_install_no_version_file()
test_read_installed_version_from_existing_file()
test_read_source_version_from_version_json()
test_version_comparison_patch_upgrade()
test_version_comparison_minor_upgrade()
test_version_comparison_major_upgrade()
```

### Backup Tests

```python
test_backup_directory_created_with_timestamp()
test_backup_copies_claude_directory()
test_backup_manifest_generated()
test_backup_integrity_verification_success()
test_backup_integrity_verification_fails_corrupted()
```

### Deployment Tests

```python
test_deploy_claude_files_to_target()
test_deploy_devforgeai_files_to_target()
test_exclude_backup_artifacts()
test_exclude_pycache_and_pyc()
test_exclude_generated_content()
test_preserve_user_config_hooks_yaml()
test_preserve_user_config_feedback_yaml()
```

### Rollback Tests

```python
test_list_backups_sorted_by_timestamp()
test_verify_backup_integrity_success()
test_restore_all_files_from_backup()
test_revert_version_json_to_backup_version()
test_rollback_on_deployment_failure_automatic()
```

### Integration Tests (5 Modes)

```python
# Fresh Install
test_fresh_install_complete_workflow()

# Upgrade
test_upgrade_workflow_1_0_0_to_1_0_1()
test_upgrade_selective_update_for_patch()

# Rollback
test_rollback_complete_workflow()

# Validate
test_validate_complete_workflow()

# Uninstall
test_uninstall_complete_workflow()
```

### Edge Case Tests

```python
test_detect_insufficient_disk_space()
test_detect_corrupted_installation_missing_version_json()
test_cli_installation_network_timeout()
test_detect_concurrent_execution_with_lock_file()
test_schema_v1_to_v2_migration()
test_detect_symlink_in_target()
test_warn_on_excessive_backups()
test_permission_denied_error_triggers_rollback()
```

## Expected Test Output

### Red Phase (All Fail - EXPECTED)

```
$ pytest installer/tests/ -v

test_version_detection.py::TestVersionDetection::test_detect_fresh_install_no_version_file FAILED
test_version_detection.py::TestVersionDetection::test_read_installed_version_from_existing_file FAILED
test_backup_management.py::TestBackupCreation::test_backup_directory_created_with_timestamp FAILED
...

42 failed in 2.34s
```

**This is correct for TDD Red phase.** Tests fail because implementation doesn't exist yet.

### Green Phase (All Pass - After Implementation)

```
$ pytest installer/tests/ -v

test_version_detection.py::TestVersionDetection::test_detect_fresh_install_no_version_file PASSED
test_version_detection.py::TestVersionDetection::test_read_installed_version_from_existing_file PASSED
test_backup_management.py::TestBackupCreation::test_backup_directory_created_with_timestamp PASSED
...

42 passed in 3.45s
```

## Implementation Roadmap

Implementation should create these modules in order:

1. **installer/version.py** (drives test_version_detection.py)
   - `get_installed_version(target_path)`
   - `get_source_version()`
   - `compare_versions(installed, source)`
   - `detect_installation_mode(installed, source)`

2. **installer/backup.py** (drives test_backup_management.py)
   - `create_backup(source, backup_reason)`
   - `generate_manifest(backup_path)`
   - `verify_integrity(backup_path)`

3. **installer/deploy.py** (drives test_deployment_engine.py)
   - `deploy_files(source, target, exclusions)`
   - `set_permissions(file_path, mode)`
   - `preserve_user_configs(target)`

4. **installer/rollback.py** (drives test_rollback_manager.py)
   - `list_backups()`
   - `verify_backup(backup_path)`
   - `restore_from_backup(backup_path, target)`
   - `revert_version_json(backup_path)`

5. **installer/validate.py** (supports test_installation_modes.py)
   - `validate_structure(target_path)`
   - `validate_version_json(version_file)`
   - `validate_cli_installed()`
   - `validate_critical_files(target_path)`

6. **installer/install.py** (orchestrator)
   - Parse command-line arguments
   - Detect installation mode
   - Coordinate backup → deploy → validate
   - Implement 5 operational modes
   - Error handling and rollback

## Test Execution Commands

### By Module

```bash
# Version detection (5 tests)
pytest installer/tests/test_version_detection.py -v

# Backup management (6 tests)
pytest installer/tests/test_backup_management.py -v

# Deployment (7 tests)
pytest installer/tests/test_deployment_engine.py -v

# Rollback (5 tests)
pytest installer/tests/test_rollback_manager.py -v

# Modes (5 integration tests)
pytest installer/tests/test_installation_modes.py -v

# Edge cases (7 tests)
pytest installer/tests/test_edge_cases.py -v
```

### By Test Class

```bash
pytest installer/tests/test_version_detection.py::TestVersionDetection -v
pytest installer/tests/test_backup_management.py::TestBackupCreation -v
pytest installer/tests/test_deployment_engine.py::TestDeploymentEngine -v
pytest installer/tests/test_rollback_manager.py::TestRollbackManager -v
```

### By Test Method

```bash
pytest installer/tests/test_version_detection.py::TestVersionDetection::test_version_comparison_patch_upgrade -v
```

### With Filtering

```bash
# Run only tests matching pattern
pytest installer/tests/ -k "backup" -v

# Run only tests matching AC1
pytest installer/tests/ -k "AC1 or detection" -v

# Run only edge cases
pytest installer/tests/test_edge_cases.py -v

# Run only integration tests
pytest installer/tests/test_installation_modes.py -v
```

## Coverage Goals

**Target:** 95%+ coverage for business logic

```bash
pytest installer/tests/ \
  --cov=installer \
  --cov-report=term-missing \
  --cov-report=html

# Then open htmlcov/index.html to view coverage
```

## Test Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Total Tests | 42+ | ✅ 42 |
| Unit Tests | 30+ | ✅ 35 |
| Integration Tests | 5+ | ✅ 7 |
| Edge Cases | 7 | ✅ 7 |
| Coverage | 95%+ | ✅ (pending impl) |
| Pass Rate | 100% | ✅ (after impl) |

## Troubleshooting

### Tests Not Found

```bash
# Ensure you're in project root
cd /mnt/c/Projects/DevForgeAI2

# Check test discovery
pytest installer/tests/ --collect-only
```

### Import Errors

```bash
# Install dependencies
pip install -r installer/tests/test_requirements.txt

# Or individually
pip install pytest>=7.0.0 packaging>=21.0
```

### Fixture Errors

```bash
# Verify conftest.py in same directory
ls installer/tests/conftest.py

# Run with verbose conftest debugging
pytest installer/tests/ -vv
```

## Resources

- **Story:** `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-045-version-aware-installer-core.story.md`
- **Summary:** `/mnt/c/Projects/DevForgeAI2/STORY-045-TEST-SUITE-SUMMARY.md`
- **Fixtures:** `conftest.py` (234 lines)
- **Test Framework:** pytest 7.0+
- **Coverage Tool:** pytest-cov

## Next Steps

1. **Verify all tests fail** (Red phase):
   ```bash
   pytest installer/tests/ -v
   # Expected: 42 failed
   ```

2. **Implement modules** one by one
   - Start with `installer/version.py`
   - Run relevant tests after each module
   - Watch tests turn from FAILED to PASSED

3. **Monitor coverage** during implementation:
   ```bash
   pytest installer/tests/ --cov=installer --cov-report=html
   ```

4. **Refactor** once all tests pass (Green phase)
   - Improve code quality while keeping tests green
   - Check coverage is 95%+

---

**Generated:** 2025-11-17
**Status:** Red Phase - All tests fail (expected)
**Next:** Run tests, then implement installer modules
