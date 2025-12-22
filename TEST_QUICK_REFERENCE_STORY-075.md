# STORY-075: Test Suite Quick Reference

**Quick Start:** Run all tests with coverage report

```bash
python3 -m pytest installer/tests/test_*.py --cov=installer --cov-report=term -v
```

---

## Test Files Overview

### test_reporter.py (33 tests)
**Module:** `installer.reporter.InstallationReporter`

| Test Class | Count | Purpose |
|-----------|-------|---------|
| TestConsoleReportGeneration | 4 | AC#1 - Console output |
| TestLogFileCreation | 9 | AC#2 - Log file creation |
| TestJSONOutputMode | 6 | AC#3 - JSON output |
| TestErrorCategorization | 8 | AC#6 - Error types |
| TestAuditTrail | 2 | AC#7 - Audit trail |
| TestPerformanceNFRs | 2 | NFR-001, NFR-002 |
| TestSecurityNFRs | 2 | NFR-006, NFR-007 |

**Key Tests:**
- Console report has 7 fields: status, version, files_installed, files_failed, duration, target_directory, log_file
- Log file: devforgeai/install.log with ISO 8601 timestamps
- JSON valid: all 11 required fields, compact format
- Error types: PERMISSION_DENIED, FILE_NOT_FOUND, CHECKSUM_MISMATCH, GIT_ERROR, VALIDATION_ERROR, DEPENDENCY_ERROR, UNKNOWN_ERROR

---

### test_manifest_generator.py (24 tests)
**Module:** `installer.manifest_generator.ManifestGenerator`

| Test Class | Count | Purpose |
|-----------|-------|---------|
| TestManifestGeneration | 6 | AC#4 - Manifest creation |
| TestChecksumGeneration | 3 | SHA256 checksums |
| TestManifestEntryFields | 4 | Entry structure |
| TestFileCategorization | 4 | File categories |
| TestAtomicManifestWrites | 2 | Atomic writes |
| TestManifestPerformance | 1 | NFR-003 |
| TestEdgeCases | 3 | Special scenarios |

**Key Tests:**
- Manifest: devforgeai/.install-manifest.json with version, timestamp, installer_version, files array
- Checksums: SHA256, 64 hex characters, matches file content
- Categories: skill, agent, command, memory, script, config
- Entry fields: path (relative), source, checksum, size_bytes, category
- Atomic: write to .tmp, validate, rename

---

### test_console_formatter.py (31 tests)
**Module:** `installer.console_formatter.ConsoleFormatter`

| Test Class | Count | Purpose |
|-----------|-------|---------|
| TestConsoleFormattingBasics | 3 | Terminal width, 80 chars |
| TestANSIColorSupport | 5 | ANSI colors (isatty detection) |
| TestProgressDisplay | 4 | Progress bar (>100 files) |
| TestReportFormatting | 6 | Report sections |
| TestErrorFormatting | 2 | Error display |
| TestBoxDrawing | 1 | Visual borders |
| TestEdgeCases | 3 | Long paths, large counts |

**Key Tests:**
- Terminal width: 80 chars (auto-detect)
- ANSI: Green for success (32m), Red for failure (31m)
- Progress: Shown when >100 files, displays percentage
- Report: Header, summary, footer with paths
- Performance: <100ms console report

---

### test_integration_reporting.py (21 tests)
**Module:** Integration across InstallationReporter, ManifestGenerator, ConsoleFormatter

| Test Class | Count | Purpose |
|-----------|-------|---------|
| TestMultiModeOutputBehavior | 5 | AC#5 - Interactive/JSON/Quiet |
| TestPartialInstallationReporting | 3 | Edge case 2 - 50% files |
| TestPermissionDeniedEdgeCase | 1 | Edge case 1 - Permission fallback |
| TestLargeInstallationReporting | 2 | NFR-008 - 500+ files |
| TestLogFileRotation | 1 | Edge case 5 - >10MB rotation |
| TestConcurrentInstallations | 1 | Edge case 6 - Lock file |
| TestDataValidation | 6 | Data validation rules |

**Key Tests:**
- Interactive: console + log + manifest
- JSON: JSON to stdout + log + manifest
- Quiet: log + manifest (no console)
- Log always created, manifest on success

---

## Coverage by Acceptance Criterion

### AC#1: Console Summary (4 tests)
```python
# Required fields (7 total):
- status: "SUCCESS" or "FAILURE"
- version: "1.0.0"
- files_installed: 450
- files_failed: 0
- duration_seconds: 2.5
- target_directory: "/path/to/target"
- log_file: "/path/to/install.log"
```
**Tests:** test_console_report_contains_*

### AC#2: Log File (9 tests)
```python
# Log file location: devforgeai/install.log
# Contents:
- ISO 8601 timestamps (YYYY-MM-DDTHH:MM:SSZ)
- File operations (copy, create, modify)
- Validation checks
- Errors with stack traces
- Warnings
- Phase markers (Pre-flight, Core, Post-install, Validation)
- Append mode (never overwrites)
- UTF-8 + LF endings
```
**Tests:** test_log_file_contains_*

### AC#3: JSON Output (6 tests)
```python
# Mode: --json flag
# Output: Valid JSON only (no text before/after)
# Fields (11 total):
{
  "status": "success|failure",
  "version": "1.0.0",
  "exit_code": 0,
  "files_installed": 450,
  "files_failed": 0,
  "errors": [],
  "warnings": [],
  "duration_seconds": 2.456,  # 3 decimal places
  "target_directory": "/path",
  "log_file": "/path",
  "manifest_file": "/path",
  "timestamp": "2025-11-20T10:30:00Z"
}
```
**Tests:** test_json_output_*

### AC#4: Manifest (13 tests)
```python
# Location: devforgeai/.install-manifest.json
# Structure:
{
  "version": "1.0.0",
  "timestamp": "2025-11-20T10:30:00Z",
  "installer_version": "1.2.0",
  "files": [
    {
      "path": ".claude/skills/test.md",     # relative
      "source": "src/...",
      "checksum": "[SHA256, 64 hex chars]",
      "size_bytes": 1024,
      "category": "skill|agent|command|memory|script|config"
    }
  ]
}
```
**Tests:** test_manifest_*, test_checksum_*, test_*_categorized_*

### AC#5: Multi-Mode (5 tests)
```python
# Interactive (default): console + log + manifest
# JSON (--json):         JSON stdout + log + manifest
# Quiet (--quiet):       log + manifest only

# Always:
- Log file created (all modes)
- Manifest created (on success)
```
**Tests:** test_*_mode_*

### AC#6: Error Categorization (8 tests)
```python
# 7 error types:
errors = [
  {"type": "PERMISSION_DENIED", "message": "...", "file": "..."},
  {"type": "FILE_NOT_FOUND", ...},
  {"type": "CHECKSUM_MISMATCH", ...},
  {"type": "GIT_ERROR", ...},
  {"type": "VALIDATION_ERROR", ...},
  {"type": "DEPENDENCY_ERROR", ...},
  {"type": "UNKNOWN_ERROR", ...}
]
```
**Tests:** test_error_type_*

### AC#7: Audit Trail (2 tests)
```python
# Every file operation traceable
# No sensitive info (password, token, secret, api_key)
# Permissions: 644 (rw-r--r--)
```
**Tests:** test_audit_trail_*

---

## Coverage by Non-Functional Requirement

### NFR-001: Report Generation <100ms
```python
test_console_report_generation_under_100ms
```

### NFR-002: JSON Serialization <50ms
```python
test_json_serialization_under_50ms  # with 500 files
```

### NFR-003: Manifest Generation <200ms
```python
test_manifest_generation_under_200ms_for_100_files
```

### NFR-004: Atomic Manifest Writes
```python
test_manifest_written_atomically_to_tmp_then_renamed
test_manifest_survives_interrupted_write
```

### NFR-006: Log File Permissions 644
```python
test_log_file_permissions_644
test_manifest_file_permissions_644
```

### NFR-007: No Credential Logging
```python
test_audit_trail_no_sensitive_information_logged
```

### NFR-008: Handle 1000+ Files
```python
test_report_generation_with_500_files
test_json_output_with_500_error_entries
```

---

## Edge Cases Covered

| # | Edge Case | Test |
|---|-----------|------|
| 1 | Permission denied on devforgeai | test_log_creation_falls_back_to_tmpdir_if_permission_denied |
| 2 | Partial install (50% files) | test_partial_installation_50_percent_files_reports_partial_success |
| 3 | JSON with failure status | test_json_with_failure_status |
| 4 | Manifest corruption recovery | test_manifest_survives_interrupted_write |
| 5 | Log file >10MB rotation | test_log_file_rotation_when_exceeds_10mb |
| 6 | Concurrent installations | test_lock_file_prevents_concurrent_installations |
| 7 | Very long paths | test_console_formatter_handles_very_long_paths |
| 8 | Large file counts (10000) | test_console_formatter_handles_large_file_counts |
| 9 | Zero files | test_console_formatter_handles_zero_files |

---

## Running Tests by Category

### Unit Tests Only
```bash
python3 -m pytest installer/tests/test_reporter.py \
                   installer/tests/test_manifest_generator.py \
                   installer/tests/test_console_formatter.py -v
```

### Integration Tests Only
```bash
python3 -m pytest installer/tests/test_integration_reporting.py -v
```

### Specific Acceptance Criterion
```bash
# AC#1 - Console Report
python3 -m pytest installer/tests/test_reporter.py::TestConsoleReportGeneration -v

# AC#2 - Log File
python3 -m pytest installer/tests/test_reporter.py::TestLogFileCreation -v

# AC#3 - JSON
python3 -m pytest installer/tests/test_reporter.py::TestJSONOutputMode -v

# AC#4 - Manifest
python3 -m pytest installer/tests/test_manifest_generator.py::TestManifestGeneration -v

# AC#5 - Multi-Mode
python3 -m pytest installer/tests/test_integration_reporting.py::TestMultiModeOutputBehavior -v

# AC#6 - Error Categorization
python3 -m pytest installer/tests/test_reporter.py::TestErrorCategorization -v

# AC#7 - Audit Trail
python3 -m pytest installer/tests/test_reporter.py::TestAuditTrail -v
```

### Performance Tests
```bash
python3 -m pytest installer/tests/ -k "performance or Performance" -v
```

### Security Tests
```bash
python3 -m pytest installer/tests/ -k "security or Security or permission" -v
```

### Edge Cases
```bash
python3 -m pytest installer/tests/test_integration_reporting.py -k "edge or Edge" -v
```

---

## Expected Test Results

### Before Implementation (RED phase)
```
============================= test session starts =============================
collected 99 items

installer/tests/test_reporter.py::TestConsoleReportGeneration::test_console_report_contains_success_status FAILED
installer/tests/test_reporter.py::TestConsoleReportGeneration::test_console_report_contains_failure_status FAILED
...
======================== 99 FAILED in X.XXs ========================
```

### After Implementation (GREEN phase)
```
======================== 99 PASSED in X.XXs ========================
```

---

## Module Structure to Implement

```python
# installer/reporter.py
class InstallationReporter:
    def generate_console_report(self, data: dict) -> str
    def generate_json_output(self, data: dict) -> str
    def create_log_file(self, target_directory: Path) -> Path
    def log_operation(self, operation_type: str, file_path: str, status: str)
    def log_validation(self, check_name: str, result: str)
    def log_error(self, operation: str, error: str)
    def log_warning(self, component: str, message: str)
    def log_phase_start(self, phase_name: str)
    def categorize_error(self, error: Exception, error_context: str = None) -> dict

# installer/manifest_generator.py
class ManifestGenerator:
    def generate_manifest(self, target_directory: Path, installed_files: list,
                         version: str, installer_version: str) -> Path
    def _calculate_checksum(self, file_path: Path) -> str
    def _categorize_file(self, file_path: Path) -> str

# installer/console_formatter.py
class ConsoleFormatter:
    def format_report(self, status: str, version: str, files_installed: int,
                     files_failed: int, duration_seconds: float,
                     target_directory: str, log_file: str, **kwargs) -> str
    def format_progress(self, files_processed: int, total_files: int) -> str
    def should_show_progress(self, total_files: int) -> bool
```

---

## Coverage Metrics

**Expected:** 95%+ of business logic

```
InstallationReporter:  33 tests × 3-5 methods = 95%+ coverage
ManifestGenerator:     24 tests × 2-3 methods = 95%+ coverage
ConsoleFormatter:      31 tests × 3-4 methods = 95%+ coverage
Integration:           11 tests × multiple classes = 85%+ coverage
```

**Estimated Code:** ~1,050 LOC
**Test Code:** ~2,148 lines
**Test-to-Code Ratio:** 2.04

---

## Imports Required

```python
# In test files
import pytest
import json
import hashlib
import time
import re
from unittest.mock import Mock, patch
from pathlib import Path
from datetime import datetime

# In implementation
import json
import logging
import hashlib
from pathlib import Path
from datetime import datetime, timezone
import sys
import shutil
```

---

## Key Fixtures Used

```python
@pytest.fixture
def tmp_path: Path  # Temporary directory (pytest built-in)
```

## Common Test Patterns

### Arrange-Act-Assert
```python
def test_example(tmp_path):
    # Arrange
    reporter = InstallationReporter()

    # Act
    result = reporter.generate_console_report({"status": "success"})

    # Assert
    assert "success" in result.lower()
```

### Testing File Operations
```python
def test_log_file_created(tmp_path):
    devforgeai_dir = tmp_path / "devforgeai"
    devforgeai_dir.mkdir()

    reporter = InstallationReporter()
    log_file = reporter.create_log_file(target_directory=tmp_path)

    assert log_file.exists()
```

### Testing JSON Output
```python
def test_json_valid(tmp_path):
    reporter = InstallationReporter()
    json_output = reporter.generate_json_output({...})

    parsed = json.loads(json_output)
    assert parsed["status"] in ["success", "failure"]
```

---

## Debugging Failed Tests

### View Full Test Output
```bash
python3 -m pytest installer/tests/test_reporter.py::TestConsoleReportGeneration::test_console_report_contains_success_status -vv
```

### Show Print Statements
```bash
python3 -m pytest installer/tests/test_reporter.py -s
```

### Run Single Test
```bash
python3 -m pytest installer/tests/test_reporter.py::TestConsoleReportGeneration::test_console_report_contains_success_status
```

### Generate Coverage Report
```bash
python3 -m pytest installer/tests/ --cov=installer --cov-report=html
# Open htmlcov/index.html in browser
```

---

**Test Suite Status:** ✓ COMPLETE - Ready for Implementation
**TDD Phase:** RED - All tests FAILING (waiting for implementation)
