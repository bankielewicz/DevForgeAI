---
id: STORY-075
title: Installation Reporting & Logging
epic: EPIC-013
sprint: Sprint-4
status: Backlog
points: 6
priority: Medium
assigned_to: TBD
created: 2025-11-25
format_version: "2.1"
---

# Story: Installation Reporting & Logging

## Description

**As a** DevOps engineer or system administrator,
**I want** comprehensive installation reporting and logging with multiple output formats,
**so that** I can troubleshoot installation failures, audit deployments, integrate with automation pipelines, and maintain compliance records.

## Acceptance Criteria

### AC#1: Console Summary Report (Interactive Mode)

**Given** the installer runs without `--json` flag
**When** installation completes (success or failure)
**Then** console displays formatted summary report containing:
- Installation status (SUCCESS or FAILURE with exit code)
- Version installed (semantic version)
- Total files processed count
- Errors encountered count
- Installation duration (in seconds)
- Target directory path
- Log file location

---

### AC#2: Detailed Log File Creation

**Given** installer runs (any mode)
**When** installation starts
**Then** creates `.devforgeai/install.log` file containing:
- ISO 8601 timestamps for every operation
- File operation details (copy/create/modify with paths)
- Validation checks
- Error messages with full stack traces
- Warning messages
- Phase markers (Pre-flight → Core → Post-install → Validation)
- Log appends (never overwrites)
- UTF-8 encoding with LF line endings

---

### AC#3: JSON Output Mode

**Given** installer runs with `--json` flag
**When** installation completes
**Then** outputs single JSON object to stdout containing:
- `status`: "success" or "failure"
- `version`: semantic version string
- `exit_code`: 0 for success, 1-255 for failure
- `files_installed`: integer count
- `files_failed`: integer count
- `errors`: array of error objects
- `warnings`: array of warning objects
- `duration_seconds`: float with 3 decimal precision
- `target_directory`: absolute path
- `log_file`: absolute path
- `manifest_file`: absolute path
- `timestamp`: ISO 8601 completion time

---

### AC#4: Installation Manifest File

**Given** installer runs successfully
**When** all files copied to target directory
**Then** creates `.devforgeai/.install-manifest.json` containing:
- `version`: semantic version installed
- `timestamp`: ISO 8601 date/time
- `files`: array with path, source, checksum, size_bytes, category
- `installer_version`: version of installer script
- Total file count matches actual files installed

---

### AC#5: Multi-Mode Output Behavior

**Given** installer runs in different modes
**When** installation completes
**Then** output behavior follows:
- **Interactive (default):** Console summary + log file + manifest
- **JSON (--json):** JSON to stdout + log file + manifest (no console)
- **Quiet (--quiet):** Log file + manifest only (no console)
- Log file ALWAYS created regardless of mode
- Manifest ALWAYS created on success

---

### AC#6: Error Categorization in Reports

**Given** installation encounters errors
**When** generating reports
**Then** errors categorized with types:
- `PERMISSION_DENIED`: Cannot write to target
- `FILE_NOT_FOUND`: Source file missing
- `CHECKSUM_MISMATCH`: File integrity failed
- `GIT_ERROR`: Git operation failed
- `VALIDATION_ERROR`: Structure validation failed
- `DEPENDENCY_ERROR`: Missing dependency
- `UNKNOWN_ERROR`: Unexpected exception

---

### AC#7: Audit Trail Compliance

**Given** installation log file exists
**When** auditor reviews log
**Then** log provides complete audit trail:
- Every file operation traceable
- All errors and warnings timestamped
- Validation checkpoints documented
- No sensitive information logged
- Log file permissions 644

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    # Installation Reporter
    - type: "Service"
      name: "InstallationReporter"
      file_path: "src/installer/reporter.py"
      interface: "IInstallationReporter"
      lifecycle: "Singleton"
      dependencies:
        - "json"
        - "logging"
        - "hashlib"
        - "pathlib"
        - "datetime"
      requirements:
        - id: "SVC-001"
          description: "Generate console summary report with 7 required fields"
          testable: true
          test_requirement: "Test: Console output contains status, version, files, errors, duration, paths"
          priority: "Critical"
        - id: "SVC-002"
          description: "Create install.log with ISO 8601 timestamps"
          testable: true
          test_requirement: "Test: Log file exists with parsable timestamps"
          priority: "Critical"
        - id: "SVC-003"
          description: "Support --json flag for structured JSON output"
          testable: true
          test_requirement: "Test: JSON validates against schema, no non-JSON text"
          priority: "High"
        - id: "SVC-004"
          description: "Generate .install-manifest.json with file checksums"
          testable: true
          test_requirement: "Test: Manifest valid JSON, SHA256 checksums verify"
          priority: "High"
        - id: "SVC-005"
          description: "Categorize errors with 7 specific types"
          testable: true
          test_requirement: "Test: Error objects include correct type field"
          priority: "Medium"

    # Console Formatter
    - type: "Service"
      name: "ConsoleFormatter"
      file_path: "src/installer/console_formatter.py"
      interface: "IConsoleFormatter"
      lifecycle: "Singleton"
      dependencies:
        - "shutil"
        - "sys"
      requirements:
        - id: "SVC-006"
          description: "Format console output respecting terminal width"
          testable: true
          test_requirement: "Test: Output fits 80-column terminal"
          priority: "High"
        - id: "SVC-007"
          description: "Detect and use ANSI colors when supported"
          testable: true
          test_requirement: "Test: Color codes present when isatty() true"
          priority: "Medium"
        - id: "SVC-008"
          description: "Display progress for large installations"
          testable: true
          test_requirement: "Test: Progress shown for >100 files"
          priority: "Medium"

    # Manifest Generator
    - type: "Service"
      name: "ManifestGenerator"
      file_path: "src/installer/manifest_generator.py"
      interface: "IManifestGenerator"
      lifecycle: "Singleton"
      dependencies:
        - "hashlib"
        - "pathlib"
        - "json"
      requirements:
        - id: "SVC-009"
          description: "Calculate SHA256 checksums for all installed files"
          testable: true
          test_requirement: "Test: Checksums are 64-char hex strings"
          priority: "Critical"
        - id: "SVC-010"
          description: "Atomic manifest writes (tmp + rename)"
          testable: true
          test_requirement: "Test: Manifest survives interrupted write"
          priority: "High"
        - id: "SVC-011"
          description: "Categorize files by type (skill, agent, command, etc.)"
          testable: true
          test_requirement: "Test: Each file has valid category"
          priority: "Medium"

    # Installation Report Data Model
    - type: "DataModel"
      name: "InstallationReport"
      table: "N/A (in-memory)"
      purpose: "Stores installation summary for reporting"
      fields:
        - name: "status"
          type: "String"
          constraints: "Required, 'success' or 'failure'"
          description: "Installation outcome"
          test_requirement: "Test: One of two allowed values"
        - name: "version"
          type: "String"
          constraints: "Required, semver format"
          description: "Version installed"
          test_requirement: "Test: Matches X.Y.Z pattern"
        - name: "exit_code"
          type: "Integer"
          constraints: "Required, 0-255"
          description: "Process exit code"
          test_requirement: "Test: 0 for success, non-zero for failure"
        - name: "files_installed"
          type: "Integer"
          constraints: "Required, >= 0"
          description: "Count of successfully installed files"
          test_requirement: "Test: Matches actual file count"
        - name: "files_failed"
          type: "Integer"
          constraints: "Required, >= 0"
          description: "Count of failed file operations"
          test_requirement: "Test: 0 for full success"
        - name: "errors"
          type: "List[ErrorObject]"
          constraints: "Required, may be empty"
          description: "List of error details"
          test_requirement: "Test: Empty array for success"
        - name: "warnings"
          type: "List[WarningObject]"
          constraints: "Required, may be empty"
          description: "List of warning details"
          test_requirement: "Test: Valid warning objects"
        - name: "duration_seconds"
          type: "Float"
          constraints: "Required, >= 0, 3 decimal precision"
          description: "Installation duration"
          test_requirement: "Test: Accurate timing measurement"
        - name: "target_directory"
          type: "String"
          constraints: "Required, absolute path"
          description: "Installation target path"
          test_requirement: "Test: Path exists"
        - name: "log_file"
          type: "String"
          constraints: "Required, absolute path"
          description: "Path to log file"
          test_requirement: "Test: File exists"
        - name: "manifest_file"
          type: "String"
          constraints: "Required, absolute path"
          description: "Path to manifest file"
          test_requirement: "Test: File exists"
        - name: "timestamp"
          type: "String"
          constraints: "Required, ISO 8601"
          description: "Completion timestamp"
          test_requirement: "Test: Valid ISO 8601 format"

    # Manifest Entry Data Model
    - type: "DataModel"
      name: "ManifestEntry"
      table: "N/A (in-memory)"
      purpose: "Stores individual file information in manifest"
      fields:
        - name: "path"
          type: "String"
          constraints: "Required, relative path"
          description: "File path relative to installation root"
          test_requirement: "Test: No absolute paths"
        - name: "source"
          type: "String"
          constraints: "Required"
          description: "Original source path"
          test_requirement: "Test: Path in distribution"
        - name: "checksum"
          type: "String"
          constraints: "Required, 64-char hex"
          description: "SHA256 hash"
          test_requirement: "Test: 64 hex characters"
        - name: "size_bytes"
          type: "Integer"
          constraints: "Required, >= 0"
          description: "File size in bytes"
          test_requirement: "Test: Accurate byte count"
        - name: "category"
          type: "String"
          constraints: "Required, enum value"
          description: "File category"
          test_requirement: "Test: skill|agent|command|memory|script|config"

    # Configuration
    - type: "Configuration"
      name: "ReportingConfig"
      file_path: "src/installer/config/reporting_config.py"
      required_keys:
        - key: "LOG_FILE_PATH"
          type: "string"
          example: ".devforgeai/install.log"
          required: true
          default: ".devforgeai/install.log"
          validation: "Valid relative path"
          test_requirement: "Test: Config value is .devforgeai/install.log"
        - key: "MANIFEST_FILE_PATH"
          type: "string"
          example: ".devforgeai/.install-manifest.json"
          required: true
          default: ".devforgeai/.install-manifest.json"
          validation: "Valid relative path"
          test_requirement: "Test: Config value is .devforgeai/.install-manifest.json"
        - key: "LOG_MAX_SIZE_MB"
          type: "int"
          example: 10
          required: true
          default: 10
          validation: "Positive integer"
          test_requirement: "Test: Config value is 10"
        - key: "PROGRESS_THRESHOLD"
          type: "int"
          example: 100
          required: true
          default: 100
          validation: "Positive integer"
          test_requirement: "Test: Progress shown when files > 100"

  business_rules:
    - id: "BR-001"
      rule: "Log file ALWAYS created regardless of mode"
      trigger: "Installation starts"
      validation: "Check log file exists after any run"
      error_handling: "Fallback to $TMPDIR if .devforgeai not writable"
      test_requirement: "Test: Log exists for interactive, JSON, and quiet modes"
      priority: "Critical"

    - id: "BR-002"
      rule: "Manifest ALWAYS created on successful installation"
      trigger: "Installation completes successfully"
      validation: "Check manifest file exists after success"
      error_handling: "Log warning if manifest fails but don't fail installation"
      test_requirement: "Test: Manifest exists after successful install"
      priority: "High"

    - id: "BR-003"
      rule: "JSON mode outputs ONLY JSON to stdout"
      trigger: "--json flag present"
      validation: "Parse stdout as JSON"
      error_handling: "Redirect all non-JSON output to stderr"
      test_requirement: "Test: stdout parses as valid JSON, no text before/after"
      priority: "High"

    - id: "BR-004"
      rule: "No sensitive information in logs"
      trigger: "Any log write"
      validation: "Scan for patterns: token, password, key, secret"
      error_handling: "Replace with [REDACTED]"
      test_requirement: "Test: Grep log for sensitive patterns returns empty"
      priority: "Critical"

    - id: "BR-005"
      rule: "Atomic manifest writes prevent corruption"
      trigger: "Manifest generation"
      validation: "Write to .tmp, validate, rename"
      error_handling: "Keep old manifest if validation fails"
      test_requirement: "Test: Interrupt during write doesn't corrupt manifest"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Report generation time <100ms"
      metric: "< 100ms for console summary"
      test_requirement: "Test: Measure report generation time"
      priority: "High"

    - id: "NFR-002"
      category: "Performance"
      requirement: "JSON serialization <50ms"
      metric: "< 50ms regardless of file count"
      test_requirement: "Test: JSON output with 500 files <50ms"
      priority: "High"

    - id: "NFR-003"
      category: "Performance"
      requirement: "Manifest generation <200ms"
      metric: "< 200ms including checksums"
      test_requirement: "Test: Manifest for 100 files <200ms"
      priority: "Medium"

    - id: "NFR-004"
      category: "Reliability"
      requirement: "Atomic manifest writes"
      metric: "Zero corruption on interruption"
      test_requirement: "Test: Kill during write doesn't corrupt"
      priority: "Critical"

    - id: "NFR-005"
      category: "Reliability"
      requirement: "Log durability with fsync"
      metric: "Critical ops fsynced"
      test_requirement: "Test: Log survives power failure"
      priority: "High"

    - id: "NFR-006"
      category: "Security"
      requirement: "Log file permissions 644"
      metric: "User rw, group/other r"
      test_requirement: "Test: stat shows -rw-r--r--"
      priority: "High"

    - id: "NFR-007"
      category: "Security"
      requirement: "No credential logging"
      metric: "Zero sensitive patterns in log"
      test_requirement: "Test: Scan for token/password/key patterns"
      priority: "Critical"

    - id: "NFR-008"
      category: "Scalability"
      requirement: "Handle 1000+ files"
      metric: "No degradation at scale"
      test_requirement: "Test: 1000 file installation completes normally"
      priority: "Medium"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Report Generation:**
- Console summary: < 100ms
- JSON serialization: < 50ms
- Manifest generation: < 200ms (including checksums)

---

### Security

**File Permissions:**
- Log file: 644 (user rw, group/other r)
- Manifest file: 644

**Data Protection:**
- No credentials logged (redact sensitive patterns)
- Path traversal prevention

---

### Reliability

**Data Durability:**
- fsync after critical operations
- Atomic manifest writes (tmp + rename)
- 3 retry attempts with exponential backoff

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-074:** Comprehensive Error Handling
  - **Why:** Shares error categorization
  - **Status:** Backlog

### Technology Dependencies

No external packages required - uses standard library:
- json, logging, hashlib, pathlib, datetime

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. **Console Report:** All 7 fields present
2. **Log File:** Timestamps, operations, errors logged
3. **JSON Output:** Valid schema, no non-JSON text
4. **Manifest:** Checksums verify, file counts match

---

### Integration Tests

**Coverage Target:** 85%+

**Test Scenarios:**
1. **Multi-Mode:** Interactive, JSON, quiet all work
2. **Error Scenarios:** Partial failure reports correctly
3. **Large Installations:** 500+ files handled

---

## Edge Cases

1. **Log file permission denied:** Fallback to $TMPDIR
2. **Partial installation (50% files):** Report partial success, manifest lists successful files
3. **JSON with failure:** Valid JSON with failure status
4. **Manifest corruption recovery:** Backup old manifest before overwrite
5. **Log file >10MB:** Rotate to .log.old
6. **Concurrent installations:** Lock file prevents race

---

## Data Validation Rules

1. **Version format:** Semver regex `^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?$`
2. **Checksums:** SHA256, 64-char hex string
3. **Timestamps:** ISO 8601 UTC format
4. **JSON output:** Valid against schema, compact (no pretty-print)
5. **File paths:** Absolute in reports, relative in manifest
6. **Error sanitization:** No user-specific paths outside target
7. **Log entry size:** Max 10KB per entry

---

## Acceptance Criteria Verification Checklist

### AC#1: Console Summary Report

- [ ] Status displayed - **Phase:** 2 - **Evidence:** reporter.test.py
- [ ] Version displayed - **Phase:** 2 - **Evidence:** reporter.test.py
- [ ] Files count displayed - **Phase:** 2 - **Evidence:** reporter.test.py
- [ ] Duration displayed - **Phase:** 2 - **Evidence:** reporter.test.py
- [ ] Paths displayed - **Phase:** 2 - **Evidence:** reporter.test.py

### AC#2: Log File Creation

- [ ] ISO 8601 timestamps - **Phase:** 2 - **Evidence:** reporter.test.py
- [ ] File operations logged - **Phase:** 2 - **Evidence:** reporter.test.py
- [ ] Append mode - **Phase:** 2 - **Evidence:** reporter.test.py

### AC#3: JSON Output Mode

- [ ] Valid JSON schema - **Phase:** 2 - **Evidence:** reporter.test.py
- [ ] No non-JSON text - **Phase:** 2 - **Evidence:** reporter.test.py
- [ ] All required fields - **Phase:** 2 - **Evidence:** reporter.test.py

### AC#4: Manifest File

- [ ] SHA256 checksums - **Phase:** 2 - **Evidence:** manifest_generator.test.py
- [ ] File counts match - **Phase:** 2 - **Evidence:** manifest_generator.test.py
- [ ] Categories assigned - **Phase:** 2 - **Evidence:** manifest_generator.test.py

### AC#5: Multi-Mode Output

- [ ] Interactive mode works - **Phase:** 4 - **Evidence:** E2E test
- [ ] JSON mode works - **Phase:** 4 - **Evidence:** E2E test
- [ ] Log always created - **Phase:** 2 - **Evidence:** reporter.test.py

### AC#6: Error Categorization

- [ ] 7 error types defined - **Phase:** 2 - **Evidence:** reporter.test.py
- [ ] Errors categorized - **Phase:** 2 - **Evidence:** reporter.test.py

### AC#7: Audit Trail

- [ ] Operations traceable - **Phase:** 2 - **Evidence:** reporter.test.py
- [ ] No sensitive data - **Phase:** 2 - **Evidence:** reporter.test.py
- [ ] Permissions 644 - **Phase:** 4 - **Evidence:** E2E test

---

**Checklist Progress:** 0/22 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] InstallationReporter generates console summary
- [ ] InstallationReporter creates log file
- [ ] InstallationReporter supports --json flag
- [ ] ManifestGenerator creates manifest with checksums
- [ ] ConsoleFormatter respects terminal width
- [ ] Multi-mode output behavior implemented
- [ ] Error categorization with 7 types
- [ ] Audit trail compliance

### Quality
- [ ] All 7 acceptance criteria have passing tests
- [ ] Edge cases covered (6 documented)
- [ ] NFRs met (<100ms report, <50ms JSON)
- [ ] Code coverage >95%

### Testing
- [ ] Unit tests for InstallationReporter
- [ ] Unit tests for ManifestGenerator
- [ ] Unit tests for ConsoleFormatter
- [ ] Integration tests for multi-mode
- [ ] E2E test: interactive mode
- [ ] E2E test: JSON mode

### Documentation
- [ ] Docstrings for all public methods
- [ ] JSON schema documented
- [ ] Log format documented

---

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Notes

**Design Decisions:**
- Log file always created (even in quiet mode) for troubleshooting
- Atomic manifest writes prevent corruption
- SHA256 checksums enable verification

**Related ADRs:**
- ADR-004: NPM Package Distribution

**References:**
- EPIC-013: Interactive Installer & Validation

---

**Story Template Version:** 2.1
**Last Updated:** 2025-11-25
