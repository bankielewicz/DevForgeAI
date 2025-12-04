# Integration Test Suite - Quick Reference

## File Location
```
/mnt/c/Projects/DevForgeAI2/tests/integration/test_application_layer_coverage.py
```

## Quick Stats
- **Tests:** 24
- **Pass Rate:** 100% (24/24)
- **Execution Time:** 0.34 seconds
- **File Size:** 31 KB (920 lines)
- **Coverage Target:** 79% → 85% (+6%)

## Run All Tests
```bash
python3 -m pytest tests/integration/test_application_layer_coverage.py -v
```

## Run by Module

### install.py (4 tests)
```bash
python3 -m pytest tests/integration/test_application_layer_coverage.py::TestInstallMissingVersionFile -v
python3 -m pytest tests/integration/test_application_layer_coverage.py::TestInstallDeploymentFailures -v
python3 -m pytest tests/integration/test_application_layer_coverage.py::TestInstallBackupCleanup -v
```

### deploy.py (5 tests)
```bash
python3 -m pytest tests/integration/test_application_layer_coverage.py::TestDeployDiskFull -v
python3 -m pytest tests/integration/test_application_layer_coverage.py::TestDeployPermissionErrors -v
python3 -m pytest tests/integration/test_application_layer_coverage.py::TestDeployFileConflicts -v
python3 -m pytest tests/integration/test_application_layer_coverage.py::TestDeploySymlinks -v
python3 -m pytest tests/integration/test_application_layer_coverage.py::TestDeploySpecialCharacters -v
```

### claude_parser.py (6 tests)
```bash
python3 -m pytest tests/integration/test_application_layer_coverage.py::TestCLAUDEParserMalformedFrontmatter -v
python3 -m pytest tests/integration/test_application_layer_coverage.py::TestCLAUDEParserEdgeCases -v
```

### offline.py (5 tests)
```bash
python3 -m pytest tests/integration/test_application_layer_coverage.py::TestOfflineChecksumMismatches -v
python3 -m pytest tests/integration/test_application_layer_coverage.py::TestOfflineMissingWheels -v
python3 -m pytest tests/integration/test_application_layer_coverage.py::TestOfflineCorruptedBundle -v
```

### Integration Tests (4 tests)
```bash
python3 -m pytest tests/integration/test_application_layer_coverage.py::TestFullErrorRecovery -v
```

## Generate Coverage Report
```bash
python3 -m pytest tests/integration/test_application_layer_coverage.py \
  --cov=installer --cov-report=html --cov-report=term
```

## Run Single Test
```bash
python3 -m pytest tests/integration/test_application_layer_coverage.py::TestInstallMissingVersionFile::test_should_handle_missing_version_json_during_upgrade -v
```

## Test Coverage Matrix

| Module | Tests | Coverage Area |
|--------|-------|---------------|
| install.py | 4 | Version file, backups, deployment errors |
| deploy.py | 5 | Disk full, permissions, file conflicts |
| claude_parser.py | 6 | Malformed content, unicode, edge cases |
| offline.py | 5 | Checksums, wheels, bundle validation |
| Integration | 4 | Error recovery, state validation |

## Key Test Scenarios

### Error Paths Covered
- Permission errors (read-only directories, denied access)
- Disk full errors (ENOSPC/errno 28)
- Missing files and directories
- File conflicts and preservation
- Deployment failures and recovery

### Edge Cases Covered
- Unicode characters (emoji, non-ASCII, special chars)
- Malformed YAML and markdown
- Empty content and missing sections
- Symlinks in deployment
- Special characters in file paths (spaces)

## Expected Results

All tests should pass immediately:
```
============================== 24 passed in 0.34s ===============================
```

## Supporting Documents

1. **COVERAGE_GAP_ANALYSIS.md** - Detailed coverage analysis
2. **TEST_GENERATION_REPORT.md** - Complete test generation report

## Dependencies

- pytest (v7.4.4+)
- Python 3.8+
- Standard library only (no external deps)

## What's Tested

✓ Error handling in installer.install module
✓ Deployment error scenarios in installer.deploy module
✓ CLAUDE.md parsing with malformed content in installer.claude_parser
✓ Bundle and checksum validation in installer.offline
✓ Multi-component error recovery scenarios
✓ Edge cases and boundary conditions

## Integration with CI/CD

Add to your CI/CD pipeline:
```bash
python3 -m pytest tests/integration/test_application_layer_coverage.py --tb=short
```

## Notes

- All tests use real file I/O (tmp_path fixtures)
- No network calls or external dependencies
- Tests are independent and can run in any order
- Fast execution (~14ms per test average)
- Comprehensive error injection for edge cases

