---
id: STORY-079
title: Fix/Repair Installation Mode
epic: EPIC-014
sprint: Backlog
status: Backlog
points: 10
priority: Medium
assigned_to: Unassigned
created: 2025-11-25
format_version: "2.1"
---

# Story: Fix/Repair Installation Mode

## Description

**As a** DevForgeAI user,
**I want** to run a repair command to detect and fix corrupted or incomplete installations,
**So that** I can restore my installation to a working state without manually identifying and fixing issues.

**Business Context:**
Installations can become corrupted through incomplete upgrades, manual file deletions, disk errors, or file conflicts. This feature provides a `devforgeai fix` command that validates installation integrity against the manifest, detects issues (missing files, corrupted checksums, wrong versions), and repairs them automatically while preserving user-modified files.

## Acceptance Criteria

### AC#1: Installation Integrity Validation

**Given** DevForgeAI is installed with a valid manifest (`.devforgeai/.install-manifest.json`),
**When** the fix command runs,
**Then** all files in the manifest are checked for existence,
**And** file checksums are verified against manifest values,
**And** file sizes are compared to expected values,
**And** validation completes within 30 seconds for standard installation.

---

### AC#2: Issue Detection

**Given** the fix command is validating installation,
**When** issues are found,
**Then** issues are categorized by type:
  - **Missing files:** File in manifest but not on disk
  - **Corrupted files:** File exists but checksum doesn't match
  - **Wrong version:** File version doesn't match expected
  - **Extra files:** Files in DevForgeAI directories not in manifest (warning only)
**And** each issue includes: file path, expected value, actual value, severity.

---

### AC#3: User-Modified File Detection

**Given** a file exists but has different checksum than manifest,
**When** the fix command detects this,
**Then** the file is checked for user modifications,
**And** user-modified files are flagged separately from corrupted files,
**And** user is prompted before overwriting user-modified files,
**And** prompt shows diff preview if file is text-based.

**Detection heuristics:**
- File in user-modifiable location (.ai_docs/, .devforgeai/context/)
- File modified more recently than installation timestamp
- File contains user-specific content patterns

---

### AC#4: Automatic Repair

**Given** issues are detected (missing or corrupted files),
**When** user confirms repair,
**Then** missing files are restored from source package,
**And** corrupted files are replaced with correct versions,
**And** restored files have correct permissions,
**And** manifest is updated with new checksums,
**And** repair operations are logged.

---

### AC#5: Non-Destructive Mode (Default)

**Given** fix command runs without --force flag,
**When** user-modified files are detected,
**Then** those files are NOT overwritten,
**And** user is prompted for each user-modified file:
  - "Keep my version" (skip repair)
  - "Restore original" (overwrite with source)
  - "Show diff" (display differences)
  - "Backup and restore" (save user version, restore original)
**And** user's choice is respected for each file.

---

### AC#6: Repair Report Display

**Given** fix command completes,
**When** report is displayed,
**Then** report shows:
  - Total files checked: count
  - Issues found: count by type
  - Issues fixed: count
  - Issues skipped: count (user choice)
  - Issues remaining: count (manual intervention needed)
  - Time taken: duration
**And** detailed issue list is available with --verbose flag,
**And** report is saved to `.devforgeai/logs/fix-{timestamp}.log`.

---

### AC#7: Exit Codes

**Given** fix command completes,
**When** exit code is set,
**Then** exit codes are:
  - 0: Success - all issues fixed or no issues found
  - 1: Missing source - repair files not available
  - 2: Permission denied - cannot write to installation directory
  - 3: Partial repair - some issues fixed, some skipped/failed
  - 4: Validation failed - post-repair validation failed
  - 5: Manual merge needed - user-modified files require manual attention

---

### AC#8: Missing Manifest Handling

**Given** `.devforgeai/.install-manifest.json` does not exist,
**When** fix command runs,
**Then** user is notified that manifest is missing,
**And** user is offered options:
  - "Regenerate manifest from current files" (treat as source of truth)
  - "Reinstall DevForgeAI" (fresh install)
  - "Abort" (exit without changes)
**And** regenerated manifest includes all DevForgeAI files with current checksums.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "InstallationValidator"
      file_path: "installer/installation_validator.py"
      interface: "IInstallationValidator"
      lifecycle: "Singleton"
      dependencies:
        - "IFileSystem"
        - "IChecksumCalculator"
      requirements:
        - id: "SVC-001"
          description: "Validate all files against manifest"
          testable: true
          test_requirement: "Test: Given manifest with 50 files, When validate() called, Then all 50 files checked"
          priority: "Critical"
        - id: "SVC-002"
          description: "Detect missing files"
          testable: true
          test_requirement: "Test: Given file in manifest but not on disk, When validate() called, Then issue type=MISSING"
          priority: "Critical"
        - id: "SVC-003"
          description: "Detect corrupted files via checksum"
          testable: true
          test_requirement: "Test: Given file with wrong checksum, When validate() called, Then issue type=CORRUPTED"
          priority: "Critical"
        - id: "SVC-004"
          description: "Detect user-modified files"
          testable: true
          test_requirement: "Test: Given user-modified .ai_docs file, When validate() called, Then is_user_modified=True"
          priority: "High"

    - type: "Service"
      name: "RepairService"
      file_path: "installer/repair_service.py"
      interface: "IRepairService"
      lifecycle: "Singleton"
      dependencies:
        - "IInstallationValidator"
        - "IFileSystem"
        - "ISourceProvider"
      requirements:
        - id: "SVC-005"
          description: "Restore missing files from source"
          testable: true
          test_requirement: "Test: Given missing file and source package, When repair() called, Then file restored"
          priority: "Critical"
        - id: "SVC-006"
          description: "Replace corrupted files with correct versions"
          testable: true
          test_requirement: "Test: Given corrupted file, When repair() called, Then file replaced with source version"
          priority: "Critical"
        - id: "SVC-007"
          description: "Preserve user-modified files unless forced"
          testable: true
          test_requirement: "Test: Given user-modified file without force, When repair() called, Then file NOT overwritten"
          priority: "Critical"
        - id: "SVC-008"
          description: "Backup user files before overwrite"
          testable: true
          test_requirement: "Test: Given user chooses 'backup and restore', When repair() called, Then user version saved to .backup/"
          priority: "High"

    - type: "Service"
      name: "ChecksumCalculator"
      file_path: "installer/checksum_calculator.py"
      interface: "IChecksumCalculator"
      lifecycle: "Singleton"
      dependencies: []
      requirements:
        - id: "SVC-009"
          description: "Calculate SHA256 checksum for file"
          testable: true
          test_requirement: "Test: Given file content, When calculate() called, Then returns correct SHA256 hash"
          priority: "Critical"
        - id: "SVC-010"
          description: "Handle large files efficiently"
          testable: true
          test_requirement: "Test: Given 100MB file, When calculate() called, Then completes < 5 seconds"
          priority: "Medium"

    - type: "Service"
      name: "ManifestManager"
      file_path: "installer/manifest_manager.py"
      interface: "IManifestManager"
      lifecycle: "Singleton"
      dependencies:
        - "IFileSystem"
        - "IChecksumCalculator"
      requirements:
        - id: "SVC-011"
          description: "Load installation manifest"
          testable: true
          test_requirement: "Test: Given valid manifest JSON, When load() called, Then InstallManifest returned"
          priority: "Critical"
        - id: "SVC-012"
          description: "Regenerate manifest from current files"
          testable: true
          test_requirement: "Test: Given installation directory, When regenerate() called, Then manifest created with all files"
          priority: "High"
        - id: "SVC-013"
          description: "Update manifest after repair"
          testable: true
          test_requirement: "Test: Given repaired file, When update() called, Then manifest checksum updated"
          priority: "High"

    - type: "DataModel"
      name: "InstallManifest"
      table: ".devforgeai/.install-manifest.json"
      purpose: "Tracks all installed files for integrity validation"
      fields:
        - name: "version"
          type: "String"
          constraints: "Required, semver"
          description: "DevForgeAI version this manifest represents"
          test_requirement: "Test: version field matches installed version"
        - name: "created_at"
          type: "DateTime"
          constraints: "Required, ISO8601"
          description: "When manifest was created/updated"
          test_requirement: "Test: created_at is valid datetime"
        - name: "files"
          type: "List[FileEntry]"
          constraints: "Required"
          description: "List of all tracked files"
          test_requirement: "Test: files list is non-empty for valid installation"
        - name: "schema_version"
          type: "Int"
          constraints: "Required, default 1"
          description: "Manifest schema version"
          test_requirement: "Test: schema_version defaults to 1"
      indexes: []
      relationships: []

    - type: "DataModel"
      name: "FileEntry"
      table: "N/A (embedded in InstallManifest)"
      purpose: "Individual file tracking data"
      fields:
        - name: "path"
          type: "String"
          constraints: "Required, relative path"
          description: "Relative path from installation root"
          test_requirement: "Test: path is relative, not absolute"
        - name: "checksum"
          type: "String"
          constraints: "Required, SHA256"
          description: "SHA256 hash of file contents"
          test_requirement: "Test: checksum is 64-character hex string"
        - name: "size"
          type: "Int"
          constraints: "Required, >= 0"
          description: "File size in bytes"
          test_requirement: "Test: size matches actual file size"
        - name: "is_user_modifiable"
          type: "Boolean"
          constraints: "Required"
          description: "Whether user is expected to modify this file"
          test_requirement: "Test: .ai_docs files have is_user_modifiable=True"
      indexes: []
      relationships: []

    - type: "DataModel"
      name: "ValidationIssue"
      table: "N/A (in-memory)"
      purpose: "Represents a detected integrity issue"
      fields:
        - name: "path"
          type: "String"
          constraints: "Required"
          description: "File path with issue"
          test_requirement: "Test: path is populated for all issues"
        - name: "issue_type"
          type: "Enum"
          constraints: "Required"
          description: "MISSING, CORRUPTED, WRONG_VERSION, EXTRA"
          test_requirement: "Test: issue_type is one of defined values"
        - name: "expected"
          type: "String"
          constraints: "Optional"
          description: "Expected value (checksum, size, version)"
          test_requirement: "Test: expected populated for CORRUPTED type"
        - name: "actual"
          type: "String"
          constraints: "Optional"
          description: "Actual value found"
          test_requirement: "Test: actual populated for CORRUPTED type"
        - name: "severity"
          type: "Enum"
          constraints: "Required"
          description: "CRITICAL, HIGH, MEDIUM, LOW"
          test_requirement: "Test: MISSING files have severity CRITICAL"
        - name: "is_user_modified"
          type: "Boolean"
          constraints: "Required"
          description: "Whether file appears to be user-modified"
          test_requirement: "Test: is_user_modified correctly detected"
      indexes: []
      relationships: []

    - type: "DataModel"
      name: "RepairReport"
      table: ".devforgeai/logs/fix-{timestamp}.log"
      purpose: "Summary of repair operation"
      fields:
        - name: "timestamp"
          type: "DateTime"
          constraints: "Required"
          description: "When repair was run"
          test_requirement: "Test: timestamp is set correctly"
        - name: "files_checked"
          type: "Int"
          constraints: "Required"
          description: "Total files validated"
          test_requirement: "Test: files_checked matches manifest count"
        - name: "issues_found"
          type: "Int"
          constraints: "Required"
          description: "Number of issues detected"
          test_requirement: "Test: issues_found accurate"
        - name: "issues_fixed"
          type: "Int"
          constraints: "Required"
          description: "Number of issues repaired"
          test_requirement: "Test: issues_fixed <= issues_found"
        - name: "issues_skipped"
          type: "Int"
          constraints: "Required"
          description: "Issues skipped by user choice"
          test_requirement: "Test: issues_skipped tracked correctly"
        - name: "exit_code"
          type: "Int"
          constraints: "Required"
          description: "Exit code for command"
          test_requirement: "Test: exit_code matches documented values"
      indexes: []
      relationships: []

  business_rules:
    - id: "BR-001"
      rule: "User-modified files are never overwritten without consent"
      trigger: "When corrupted file is detected as user-modified"
      validation: "Check is_user_modifiable flag and modification timestamp"
      error_handling: "Prompt user for action"
      test_requirement: "Test: User-modified file skipped without --force"
      priority: "Critical"

    - id: "BR-002"
      rule: "Missing critical files cause repair to fail if source unavailable"
      trigger: "When MISSING issue detected and source package not available"
      validation: "Check source package exists"
      error_handling: "Exit code 1, error message"
      test_requirement: "Test: Missing source returns exit code 1"
      priority: "Critical"

    - id: "BR-003"
      rule: "Post-repair validation ensures fixes were successful"
      trigger: "After repair operations complete"
      validation: "Re-run validation on repaired files"
      error_handling: "Exit code 4 if validation still fails"
      test_requirement: "Test: Post-repair validation runs automatically"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Validation completes within 30 seconds"
      metric: "< 30000ms for 500 file installation"
      test_requirement: "Test: validate() < 30s for 500 files"
      priority: "High"

    - id: "NFR-002"
      category: "Performance"
      requirement: "Checksum calculation is efficient"
      metric: "< 5 seconds for 100MB file"
      test_requirement: "Test: calculate_checksum() < 5s for 100MB"
      priority: "Medium"

    - id: "NFR-003"
      category: "Reliability"
      requirement: "Fix mode success rate > 90%"
      metric: "90%+ of common issues automatically repaired"
      test_requirement: "Test: 90% of test scenarios repaired successfully"
      priority: "High"

    - id: "NFR-004"
      category: "Security"
      requirement: "Repair does not modify files outside DevForgeAI directories"
      metric: "0 modifications outside .claude/, .devforgeai/, CLAUDE.md"
      test_requirement: "Test: Files outside DevForgeAI directories unchanged"
      priority: "Critical"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Validation: < 30 seconds for standard installation
- Checksum calculation: < 5 seconds per 100MB file
- Repair (single file): < 2 seconds

---

### Reliability

**Success Rates:**
- Fix mode success rate: > 90% for common issues
- No data loss during repair operations

---

### Security

**Scope:**
- Repair only modifies files within DevForgeAI directories
- User content in .ai_docs/ protected by default

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-077:** Version Detection & Compatibility Checking
  - **Why:** Needs version info for proper repair
  - **Status:** Backlog

### Technology Dependencies

None - uses Python standard library (hashlib for checksums).

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic

**Test Scenarios:**

1. **Happy Path:**
   - Validate installation with no issues
   - Detect missing files
   - Repair missing files

2. **Edge Cases:**
   - All files user-modified
   - Manifest missing
   - Empty installation

3. **Error Cases:**
   - Source package unavailable
   - Permission denied
   - Post-repair validation fails

---

## Acceptance Criteria Verification Checklist

### AC#1: Installation Integrity Validation
- [ ] All manifest files checked - **Phase:** 2 - **Evidence:** installation_validator_test.py
- [ ] Checksums verified - **Phase:** 2 - **Evidence:** checksum_calculator_test.py
- [ ] Validation < 30 seconds - **Phase:** 4 - **Evidence:** performance test

### AC#2: Issue Detection
- [ ] Missing files detected - **Phase:** 2 - **Evidence:** installation_validator_test.py
- [ ] Corrupted files detected - **Phase:** 2 - **Evidence:** installation_validator_test.py
- [ ] Issue details populated - **Phase:** 2 - **Evidence:** installation_validator_test.py

### AC#3: User-Modified File Detection
- [ ] User-modified files flagged separately - **Phase:** 2 - **Evidence:** installation_validator_test.py
- [ ] Prompt shown for user files - **Phase:** 2 - **Evidence:** CLI integration test

### AC#4: Automatic Repair
- [ ] Missing files restored - **Phase:** 2 - **Evidence:** repair_service_test.py
- [ ] Corrupted files replaced - **Phase:** 2 - **Evidence:** repair_service_test.py
- [ ] Manifest updated after repair - **Phase:** 2 - **Evidence:** manifest_manager_test.py

### AC#5: Non-Destructive Mode
- [ ] User files NOT overwritten by default - **Phase:** 2 - **Evidence:** repair_service_test.py
- [ ] User prompted for each file - **Phase:** 2 - **Evidence:** CLI integration test

### AC#6: Repair Report Display
- [ ] Report shows all statistics - **Phase:** 2 - **Evidence:** CLI integration test
- [ ] Report saved to log file - **Phase:** 2 - **Evidence:** file existence test

### AC#7: Exit Codes
- [ ] Exit code 0 on success - **Phase:** 2 - **Evidence:** CLI integration test
- [ ] Exit code 1 on missing source - **Phase:** 2 - **Evidence:** CLI integration test
- [ ] Exit code 3 on partial repair - **Phase:** 2 - **Evidence:** CLI integration test

### AC#8: Missing Manifest Handling
- [ ] User notified of missing manifest - **Phase:** 2 - **Evidence:** manifest_manager_test.py
- [ ] Regeneration option works - **Phase:** 2 - **Evidence:** manifest_manager_test.py

---

**Checklist Progress:** 0/20 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] InstallationValidator service implemented
- [ ] RepairService implemented
- [ ] ChecksumCalculator implemented
- [ ] ManifestManager implemented
- [ ] All data models implemented

### Quality
- [ ] All 8 acceptance criteria have passing tests
- [ ] Edge cases covered
- [ ] NFRs met (< 30s validation)
- [ ] Code coverage > 95% for business logic

### Testing
- [ ] Unit tests for InstallationValidator
- [ ] Unit tests for RepairService
- [ ] Unit tests for ChecksumCalculator
- [ ] Unit tests for ManifestManager
- [ ] Integration test for end-to-end fix workflow

### Documentation
- [ ] Fix command usage guide
- [ ] Troubleshooting guide for common issues

---

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Notes

**Design Decisions:**
- SHA256 chosen for checksums (security + performance balance)
- User-modified files protected by default (non-destructive)
- Manifest regeneration available as recovery option

**Related ADRs:**
- None yet

**References:**
- EPIC-014: Version Management & Installation Lifecycle

---

**Story Template Version:** 2.1
**Last Updated:** 2025-11-25
