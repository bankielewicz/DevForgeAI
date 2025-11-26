---
id: STORY-072
title: Pre-Flight Validation Checks
epic: EPIC-013
sprint: Sprint-4
status: Backlog
points: 10
priority: Medium
assigned_to: TBD
created: 2025-11-25
format_version: "2.1"
---

# Story: Pre-Flight Validation Checks

## Description

**As a** developer setting up DevForgeAI for the first time,
**I want** the installer to validate my environment before making any changes,
**so that** installation issues are caught early and I receive clear guidance on resolving problems before the system enters a broken state.

## Acceptance Criteria

### AC#1: Python Version Validation

**Given** the pre-flight validation is running
**When** the installer checks for Python availability
**Then** the system verifies Python 3.10+ is installed, displays version found (e.g., "Python 3.11.4"), marks check as ✓ PASS if ≥3.10, or ⚠ WARN if missing/older with message "Python 3.10+ recommended for CLI validators (optional)"

---

### AC#2: Disk Space Validation

**Given** the pre-flight validation is running
**When** the installer checks available disk space in the target directory
**Then** the system calculates free space in MB, marks check as ✓ PASS if ≥100MB available, or ✗ FAIL if <100MB with message "Insufficient disk space: {X}MB available, 100MB required. Free up space and retry."

---

### AC#3: Existing Installation Detection

**Given** the pre-flight validation is running
**When** the installer checks for previous DevForgeAI installations
**Then** the system detects existing `.claude/` directory or `.devforgeai/` directory, marks check as ⚠ WARN if found, displays message "Existing DevForgeAI installation detected at {path}. Choose: [U]pgrade existing, [F]resh install (removes old files), [C]ancel", and prompts user for selection

---

### AC#4: Write Permission Validation

**Given** the pre-flight validation is running
**When** the installer checks write permissions on the target directory
**Then** the system attempts to create a temporary test file `.devforgeai-write-test`, marks check as ✓ PASS if file creation succeeds (and deletes test file), or ✗ FAIL if permission denied with message "Write permission denied on {path}. Run installer with appropriate permissions or choose different directory."

---

### AC#5: Validation Summary Display

**Given** all pre-flight checks have completed
**When** the installer displays the validation summary
**Then** the system shows a formatted table with each check name, status (✓ PASS / ⚠ WARN / ✗ FAIL), and description, followed by overall result: "All checks passed" (all ✓), "Warnings present (can proceed)" (any ⚠, no ✗), or "Critical failures (cannot proceed)" (any ✗)

---

### AC#6: Blocking Error Enforcement

**Given** the validation summary shows one or more ✗ FAIL checks
**When** the installer attempts to proceed with installation
**Then** the system halts with exit code 1, displays message "Installation blocked due to critical failures. Resolve issues above and retry.", and prevents any file modifications

---

### AC#7: Force Flag Override

**Given** the validation summary shows ⚠ WARN checks but no ✗ FAIL checks
**When** the installer is invoked with `--force` flag
**Then** the system bypasses user prompts for warnings, logs "Force flag enabled: skipping warning prompts" to console, and proceeds directly to installation without user interaction for non-critical issues

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    # Pre-Flight Validator Orchestrator
    - type: "Service"
      name: "PreFlightValidator"
      file_path: "src/installer/validators/pre_flight_validator.py"
      interface: "IPreFlightValidator"
      lifecycle: "Singleton"
      dependencies:
        - "IPythonVersionChecker"
        - "IDiskSpaceChecker"
        - "IExistingInstallationDetector"
        - "IPermissionChecker"
      requirements:
        - id: "SVC-001"
          description: "Orchestrate 4 validation checks and return structured ValidationResult"
          testable: true
          test_requirement: "Test: ValidationResult contains 4 CheckResult objects with correct status"
          priority: "Critical"
        - id: "SVC-002"
          description: "Determine overall outcome (all_pass, warnings_present, critical_failures)"
          testable: true
          test_requirement: "Test: Any FAIL → critical_failures=True, any WARN → warnings_present=True"
          priority: "Critical"
        - id: "SVC-003"
          description: "Format validation summary as human-readable table"
          testable: true
          test_requirement: "Test: format_summary() returns string with table headers and 4 rows"
          priority: "High"
        - id: "SVC-004"
          description: "Handle --force flag to bypass warning prompts"
          testable: true
          test_requirement: "Test: With --force, WARN checks don't prompt user"
          priority: "High"

    # Python Version Checker
    - type: "Service"
      name: "PythonVersionChecker"
      file_path: "src/installer/validators/python_checker.py"
      interface: "IPythonVersionChecker"
      lifecycle: "Singleton"
      dependencies:
        - "subprocess"
        - "re"
      requirements:
        - id: "SVC-005"
          description: "Detect Python version by calling python3/python subprocess"
          testable: true
          test_requirement: "Test: Returns version string '3.11.4', WARN if <3.10 or missing"
          priority: "Critical"
        - id: "SVC-006"
          description: "Parse version using regex and compare against 3.10 minimum"
          testable: true
          test_requirement: "Test: '3.10.0' → PASS, '3.9.18' → WARN, invalid → WARN"
          priority: "High"
        - id: "SVC-007"
          description: "Try multiple Python executables in priority order"
          testable: true
          test_requirement: "Test: Try python3, python, python3.11, python3.10 in order"
          priority: "Medium"

    # Disk Space Checker
    - type: "Service"
      name: "DiskSpaceChecker"
      file_path: "src/installer/validators/disk_space_checker.py"
      interface: "IDiskSpaceChecker"
      lifecycle: "Singleton"
      dependencies:
        - "shutil"
        - "pathlib"
      requirements:
        - id: "SVC-008"
          description: "Calculate free space using shutil.disk_usage and compare against 100MB"
          testable: true
          test_requirement: "Test: PASS if ≥100MB free, FAIL if less"
          priority: "Critical"
        - id: "SVC-009"
          description: "Handle exceptions gracefully with WARN status"
          testable: true
          test_requirement: "Test: Exception returns WARN with error context"
          priority: "High"

    # Existing Installation Detector
    - type: "Service"
      name: "ExistingInstallationDetector"
      file_path: "src/installer/validators/installation_detector.py"
      interface: "IExistingInstallationDetector"
      lifecycle: "Singleton"
      dependencies:
        - "pathlib"
        - "json"
      requirements:
        - id: "SVC-010"
          description: "Detect existing installation by checking for .claude/ or .devforgeai/ directories"
          testable: true
          test_requirement: "Test: WARN if either directory exists, PASS if neither"
          priority: "Critical"
        - id: "SVC-011"
          description: "Read version.json if present and include version in message"
          testable: true
          test_requirement: "Test: Message includes 'DevForgeAI v1.0.0' if version.json exists"
          priority: "Medium"

    # Permission Checker
    - type: "Service"
      name: "PermissionChecker"
      file_path: "src/installer/validators/permission_checker.py"
      interface: "IPermissionChecker"
      lifecycle: "Singleton"
      dependencies:
        - "pathlib"
      requirements:
        - id: "SVC-012"
          description: "Verify write permissions by creating temporary test file"
          testable: true
          test_requirement: "Test: PASS if file creation succeeds, FAIL if PermissionError"
          priority: "Critical"
        - id: "SVC-013"
          description: "Clean up test file immediately after creation"
          testable: true
          test_requirement: "Test: .devforgeai-write-test does not exist after check"
          priority: "High"
        - id: "SVC-014"
          description: "Handle missing target directory"
          testable: true
          test_requirement: "Test: FAIL with message if target directory doesn't exist"
          priority: "High"

    # Validation Result Data Model
    - type: "DataModel"
      name: "ValidationResult"
      table: "N/A (in-memory)"
      purpose: "Stores validation check results and overall status"
      fields:
        - name: "checks"
          type: "List[CheckResult]"
          constraints: "Required, 4 elements"
          description: "List of individual check results"
          test_requirement: "Test: Contains exactly 4 CheckResult objects"
        - name: "all_pass"
          type: "Boolean"
          constraints: "Computed"
          description: "True if all checks passed"
          test_requirement: "Test: True only when all 4 checks are PASS"
        - name: "warnings_present"
          type: "Boolean"
          constraints: "Computed"
          description: "True if any warnings (no failures)"
          test_requirement: "Test: True when any WARN and no FAIL"
        - name: "critical_failures"
          type: "Boolean"
          constraints: "Computed"
          description: "True if any critical failures"
          test_requirement: "Test: True when any FAIL"

    # Check Result Data Model
    - type: "DataModel"
      name: "CheckResult"
      table: "N/A (in-memory)"
      purpose: "Stores individual validation check result"
      fields:
        - name: "check_name"
          type: "String"
          constraints: "Required"
          description: "Name of the check (e.g., 'Python Version')"
          test_requirement: "Test: Non-empty string"
        - name: "status"
          type: "Enum(PASS, WARN, FAIL)"
          constraints: "Required"
          description: "Check result status"
          test_requirement: "Test: Must be one of PASS, WARN, FAIL"
        - name: "message"
          type: "String"
          constraints: "Required"
          description: "Human-readable result message"
          test_requirement: "Test: Non-empty string with context"

    # Configuration
    - type: "Configuration"
      name: "ValidationConfig"
      file_path: "src/installer/config/validation_config.py"
      required_keys:
        - key: "MIN_PYTHON_VERSION"
          type: "string"
          example: "3.10"
          required: true
          default: "3.10"
          validation: "Valid semver major.minor"
          test_requirement: "Test: Config value is '3.10'"
        - key: "MIN_DISK_SPACE_MB"
          type: "int"
          example: 100
          required: true
          default: 100
          validation: "Positive integer"
          test_requirement: "Test: Config value is 100"
        - key: "CHECK_TIMEOUT_SECONDS"
          type: "int"
          example: 5
          required: true
          default: 5
          validation: "Positive integer"
          test_requirement: "Test: Config value is 5"
        - key: "PYTHON_EXECUTABLES"
          type: "array"
          example: ["python3", "python", "python3.11", "python3.10"]
          required: true
          default: ["python3", "python", "python3.11", "python3.10"]
          validation: "Non-empty array of strings"
          test_requirement: "Test: Contains 4 Python executable names"

  business_rules:
    - id: "BR-001"
      rule: "Critical failures (✗ FAIL) block installation"
      trigger: "Any check returns CheckStatus.FAIL"
      validation: "Check critical_failures flag on ValidationResult"
      error_handling: "Halt with exit code 1, display resolution steps"
      test_requirement: "Test: FAIL check prevents any file modifications"
      priority: "Critical"

    - id: "BR-002"
      rule: "Warnings (⚠ WARN) allow continuation but prompt user"
      trigger: "Any check returns CheckStatus.WARN"
      validation: "Prompt user unless --force flag set"
      error_handling: "Display warning, ask to continue or cancel"
      test_requirement: "Test: WARN prompts user (interactive), proceeds with --force"
      priority: "High"

    - id: "BR-003"
      rule: "--force flag bypasses warning prompts only"
      trigger: "--force flag present and warnings_present=True"
      validation: "Force applies only to WARN, never FAIL"
      error_handling: "Log force mode, skip prompts, proceed"
      test_requirement: "Test: --force skips WARN prompts but not FAIL blocks"
      priority: "High"

    - id: "BR-004"
      rule: "All checks must complete before summary display"
      trigger: "Pre-flight validation starts"
      validation: "Run all 4 checks even if early check fails"
      error_handling: "Collect all results, display complete summary"
      test_requirement: "Test: If Python check fails, disk/permission checks still run"
      priority: "Medium"

    - id: "BR-005"
      rule: "Python is optional (WARN, not FAIL)"
      trigger: "Python check cannot find Python 3.10+"
      validation: "Return WARN status, not FAIL"
      error_handling: "Display 'CLI validators disabled' message"
      test_requirement: "Test: Missing Python returns WARN, not FAIL"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "All pre-flight checks complete in <5 seconds"
      metric: "< 5 seconds total execution time (p95)"
      test_requirement: "Test: Time validation from start to summary display"
      priority: "High"

    - id: "NFR-002"
      category: "Performance"
      requirement: "Python version check completes in <500ms"
      metric: "< 500ms for subprocess call"
      test_requirement: "Test: Measure time for Python detection"
      priority: "Medium"

    - id: "NFR-003"
      category: "Performance"
      requirement: "Disk space check completes in <200ms"
      metric: "< 200ms for filesystem stat"
      test_requirement: "Test: Measure time for disk_usage call"
      priority: "Medium"

    - id: "NFR-004"
      category: "Reliability"
      requirement: "Accurate Python detection across platforms"
      metric: "Works on Ubuntu, macOS, Windows"
      test_requirement: "Test: CI matrix with Linux, macOS, Windows"
      priority: "Critical"

    - id: "NFR-005"
      category: "Reliability"
      requirement: "Zero false positives for blocking errors"
      metric: "FAIL only when installation genuinely cannot proceed"
      test_requirement: "Test: Verify each FAIL condition is truly blocking"
      priority: "Critical"

    - id: "NFR-006"
      category: "Usability"
      requirement: "Error messages include actionable resolution steps"
      metric: "Minimum 2 steps per error (what to check, how to fix)"
      test_requirement: "Test: Each FAIL/WARN message contains resolution guidance"
      priority: "High"

    - id: "NFR-007"
      category: "Security"
      requirement: "No privilege escalation attempts"
      metric: "Never attempt sudo or Run as Administrator"
      test_requirement: "Test: Permission denied returns FAIL, not sudo prompt"
      priority: "Critical"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Total Execution:**
- All 4 checks complete in < 5 seconds (p95)

**Individual Checks:**
- Python version check: < 500ms
- Disk space check: < 200ms
- Permission check: < 100ms
- Existing installation detection: < 1 second

---

### Security

**Safe Subprocess:**
- All subprocess calls use `shell=False` (no shell injection)
- No privilege escalation (never attempt sudo)

**File Cleanup:**
- Write permission test file deleted immediately
- No orphaned files on validation failure

---

### Reliability

**Cross-Platform:**
- Works on Linux (Ubuntu 22.04+), macOS (13+), Windows (10+)
- Handles different filesystem types (ext4, NTFS, APFS)

**Graceful Degradation:**
- If one check fails, remaining checks still execute
- Complete summary always displayed

---

### Usability

**Clear Messages:**
- Each error includes resolution steps (what to check, how to fix)
- Validation summary shows actual vs. required values
- Color-coded status indicators

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-071:** Wizard-Driven Interactive UI
  - **Why:** Uses OutputFormatter for color-coded messages
  - **Status:** Backlog

### Technology Dependencies

- [ ] **shutil:** Standard library (disk space)
- [ ] **pathlib:** Standard library (file operations)
- [ ] **subprocess:** Standard library (Python detection)
- [ ] **dataclasses:** Standard library (data models)

No external packages required.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for validator services

**Test Scenarios:**
1. **Python Check:** Valid version, old version, missing Python, invalid output
2. **Disk Space:** Sufficient space, insufficient space, calculation failure
3. **Permission Check:** Writable, read-only, missing directory
4. **Existing Install:** Fresh install, existing .claude/, partial installation

---

### Integration Tests

**Coverage Target:** 85%+

**Test Scenarios:**
1. **Full Validation Flow:** All checks pass
2. **Mixed Results:** Some WARN, some PASS
3. **Critical Failure:** At least one FAIL blocks installation

---

## Edge Cases

1. **Python installed but wrong version (e.g., Python 3.9):** Mark as ⚠ WARN. Display "Python 3.9 found (3.10+ recommended). CLI validators disabled."

2. **Multiple Python versions available:** Check in priority order: python3, python, python3.11, python3.10. Use highest version found.

3. **Read-only filesystem:** Write permission check fails with ✗ FAIL. Suggest writable alternative directory.

4. **Partial previous installation:** Detect incomplete structure. Mark as ⚠ WARN with recommendation for fresh install.

5. **Disk space check on network mount:** Catch exceptions, mark as ⚠ WARN if calculation fails.

6. **Container environment (Docker):** Python check finds virtual environment Python. Display environment type in summary.

---

## Data Validation Rules

1. **Python version format:** Regex `Python (\d+)\.(\d+)\.(\d+)`. Compare major.minor against 3.10.

2. **Disk space calculation:** `shutil.disk_usage(path).free` in bytes. Convert to MB. Threshold: 100MB.

3. **Existing installation detection:** Check for `.claude/skills/` or `.devforgeai/context/` directories.

4. **Permission check:** Create temp file `.devforgeai-write-test`. Delete immediately.

5. **Force flag:** Accept `--force`, `-f`, `--skip-warnings`. Bypasses WARN only, never FAIL.

---

## Acceptance Criteria Verification Checklist

### AC#1: Python Version Validation

- [ ] Python 3.10+ detected - **Phase:** 2 - **Evidence:** python_checker.test.py
- [ ] WARN for missing/old Python - **Phase:** 2 - **Evidence:** python_checker.test.py
- [ ] Version displayed in message - **Phase:** 2 - **Evidence:** python_checker.test.py

### AC#2: Disk Space Validation

- [ ] Free space calculated - **Phase:** 2 - **Evidence:** disk_space_checker.test.py
- [ ] FAIL for <100MB - **Phase:** 2 - **Evidence:** disk_space_checker.test.py
- [ ] PASS for ≥100MB - **Phase:** 2 - **Evidence:** disk_space_checker.test.py

### AC#3: Existing Installation Detection

- [ ] .claude/ detected - **Phase:** 2 - **Evidence:** installation_detector.test.py
- [ ] .devforgeai/ detected - **Phase:** 2 - **Evidence:** installation_detector.test.py
- [ ] Version read if present - **Phase:** 2 - **Evidence:** installation_detector.test.py

### AC#4: Write Permission Validation

- [ ] Test file created - **Phase:** 2 - **Evidence:** permission_checker.test.py
- [ ] Test file deleted - **Phase:** 2 - **Evidence:** permission_checker.test.py
- [ ] FAIL for permission denied - **Phase:** 2 - **Evidence:** permission_checker.test.py

### AC#5: Validation Summary Display

- [ ] Table formatted correctly - **Phase:** 2 - **Evidence:** pre_flight_validator.test.py
- [ ] Status indicators displayed - **Phase:** 2 - **Evidence:** pre_flight_validator.test.py
- [ ] Overall result shown - **Phase:** 2 - **Evidence:** pre_flight_validator.test.py

### AC#6: Blocking Error Enforcement

- [ ] FAIL blocks installation - **Phase:** 2 - **Evidence:** pre_flight_validator.test.py
- [ ] Exit code 1 - **Phase:** 4 - **Evidence:** E2E test

### AC#7: Force Flag Override

- [ ] --force bypasses WARN - **Phase:** 2 - **Evidence:** pre_flight_validator.test.py
- [ ] --force doesn't bypass FAIL - **Phase:** 2 - **Evidence:** pre_flight_validator.test.py

---

**Checklist Progress:** 0/19 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] PreFlightValidator orchestrates 4 checks
- [ ] PythonVersionChecker detects Python 3.10+
- [ ] DiskSpaceChecker verifies 100MB+ free
- [ ] ExistingInstallationDetector finds previous installs
- [ ] PermissionChecker verifies write access
- [ ] ValidationResult model stores check results
- [ ] --force flag bypasses warning prompts
- [ ] Blocking errors halt installation

### Quality
- [ ] All 7 acceptance criteria have passing tests
- [ ] Edge cases covered (wrong version, read-only, partial install)
- [ ] Cross-platform validation (Linux, macOS, Windows)
- [ ] NFRs met (<5s total, <500ms Python check)
- [ ] Code coverage >95% for validators

### Testing
- [ ] Unit tests for PythonVersionChecker
- [ ] Unit tests for DiskSpaceChecker
- [ ] Unit tests for ExistingInstallationDetector
- [ ] Unit tests for PermissionChecker
- [ ] Unit tests for PreFlightValidator
- [ ] Integration tests for validation flow
- [ ] E2E test: all checks pass
- [ ] E2E test: critical failure blocks

### Documentation
- [ ] Docstrings for all public methods
- [ ] README section for validation checks
- [ ] Error resolution guide

---

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Notes

**Design Decisions:**
- Python is optional (WARN) because CLI validators are not required for core framework
- All checks run even if early check fails (complete picture for user)
- --force bypasses WARN only, never FAIL (safety first)

**Related ADRs:**
- ADR-004: NPM Package Distribution

**References:**
- EPIC-013: Interactive Installer & Validation

---

**Story Template Version:** 2.1
**Last Updated:** 2025-11-25
