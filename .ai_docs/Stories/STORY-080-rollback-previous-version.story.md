---
id: STORY-080
title: Rollback to Previous Version
epic: EPIC-014
sprint: Backlog
status: Backlog
points: 12
priority: Medium
assigned_to: Unassigned
created: 2025-11-25
format_version: "2.1"
---

# Story: Rollback to Previous Version

## Description

**As a** DevForgeAI user,
**I want** to rollback to a previous version if an upgrade fails or I want to revert,
**So that** I can restore my installation to a known working state without losing my work.

**Business Context:**
This feature provides both automatic rollback (triggered when upgrades fail) and manual rollback (`devforgeai rollback` command). Users can view available backup versions, select which one to restore, and have confidence that rollback will preserve their user-created content (stories, epics, context files). This is a critical safety net that enables confident upgrades.

## Acceptance Criteria

### AC#1: Automatic Rollback on Upgrade Failure

**Given** an upgrade is in progress,
**When** a migration script fails OR validation fails,
**Then** automatic rollback is triggered immediately,
**And** all changes made during upgrade are reverted,
**And** pre-upgrade backup is restored,
**And** .version.json is restored to previous state,
**And** user is notified with clear error message explaining what failed,
**And** rollback completes within 1 minute.

---

### AC#2: Manual Rollback Command

**Given** at least one backup exists,
**When** user runs `devforgeai rollback`,
**Then** available backups are listed with version and date,
**And** user can select which backup to restore,
**And** selected backup is restored,
**And** current version is backed up before rollback (safety),
**And** success message confirms restored version.

---

### AC#3: List Available Backups

**Given** user wants to see rollback options,
**When** user runs `devforgeai rollback --list`,
**Then** all available backups are displayed with:
  - Version number (e.g., v1.0.0)
  - Backup date and time
  - Backup size (MB)
  - Reason (UPGRADE, UNINSTALL, MANUAL)
  - Backup path
**And** backups are sorted by date (newest first).

---

### AC#4: Restore from Backup

**Given** user selects a backup to restore,
**When** rollback executes,
**Then** all files from backup are copied to their original locations,
**And** .version.json is reverted to backed-up version,
**And** files not in backup but added since are optionally removed,
**And** rollback validation confirms restoration success,
**And** user content is preserved (not overwritten from backup).

---

### AC#5: User Content Preservation

**Given** rollback is in progress,
**When** files are being restored,
**Then** user-created content is NOT overwritten:
  - Stories: `.ai_docs/Stories/*`
  - Epics: `.ai_docs/Epics/*`
  - Sprints: `.ai_docs/Sprints/*`
  - Context files: `.devforgeai/context/*` (if user-modified)
  - Custom ADRs: `.devforgeai/adrs/*` (if user-created)
**And** user is shown list of preserved files,
**And** user can optionally include user content in rollback with --include-user-content flag.

---

### AC#6: Rollback Validation

**Given** rollback has completed,
**When** validation runs,
**Then** restored version is verified to match backup,
**And** critical files are checked for existence,
**And** file checksums are verified against backup manifest,
**And** validation results displayed to user,
**And** validation failure triggers warning (not automatic re-rollback).

---

### AC#7: Rollback Summary Display

**Given** rollback completes,
**When** summary is displayed,
**Then** summary shows:
  - Restored from: backup version and date
  - Restored to: previous version number
  - Files restored: count
  - Files preserved: count (user content)
  - Validation status: PASSED/FAILED
  - Duration: time taken
**And** summary is saved to `.devforgeai/logs/rollback-{timestamp}.log`.

---

### AC#8: Backup Cleanup

**Given** multiple backups exist,
**When** retention limit is reached (default: 5 backups),
**Then** oldest backups are automatically deleted,
**And** user is notified which backups were removed,
**And** retention limit is configurable in settings,
**And** cleanup only happens after successful rollback.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "RollbackOrchestrator"
      file_path: "installer/rollback_orchestrator.py"
      interface: "IRollbackOrchestrator"
      lifecycle: "Singleton"
      dependencies:
        - "IBackupService"
        - "IVersionDetector"
        - "IFileSystem"
      requirements:
        - id: "SVC-001"
          description: "Orchestrate automatic rollback on failure"
          testable: true
          test_requirement: "Test: Given upgrade failure signal, When triggered, Then full rollback executes"
          priority: "Critical"
        - id: "SVC-002"
          description: "Orchestrate manual rollback with user selection"
          testable: true
          test_requirement: "Test: Given backup selection, When execute() called, Then backup restored"
          priority: "Critical"
        - id: "SVC-003"
          description: "Create safety backup before manual rollback"
          testable: true
          test_requirement: "Test: Given manual rollback, When execute() called, Then current state backed up first"
          priority: "High"
        - id: "SVC-004"
          description: "Preserve user content during rollback"
          testable: true
          test_requirement: "Test: Given user stories exist, When rollback() called, Then stories NOT overwritten"
          priority: "Critical"

    - type: "Service"
      name: "BackupRestorer"
      file_path: "installer/backup_restorer.py"
      interface: "IBackupRestorer"
      lifecycle: "Singleton"
      dependencies:
        - "IFileSystem"
        - "IChecksumCalculator"
      requirements:
        - id: "SVC-005"
          description: "Restore all files from backup"
          testable: true
          test_requirement: "Test: Given backup with 100 files, When restore() called, Then all 100 files restored"
          priority: "Critical"
        - id: "SVC-006"
          description: "Skip user-content directories by default"
          testable: true
          test_requirement: "Test: Given .ai_docs/Stories/ in backup, When restore() called, Then directory skipped"
          priority: "Critical"
        - id: "SVC-007"
          description: "Include user content when flag set"
          testable: true
          test_requirement: "Test: Given --include-user-content flag, When restore() called, Then user content included"
          priority: "Medium"
        - id: "SVC-008"
          description: "Verify file checksums after restore"
          testable: true
          test_requirement: "Test: Given restored file, When verify() called, Then checksum matches backup manifest"
          priority: "High"

    - type: "Service"
      name: "BackupSelector"
      file_path: "installer/backup_selector.py"
      interface: "IBackupSelector"
      lifecycle: "Singleton"
      dependencies:
        - "IBackupService"
      requirements:
        - id: "SVC-009"
          description: "List available backups sorted by date"
          testable: true
          test_requirement: "Test: Given 5 backups, When list() called, Then returns 5 sorted newest first"
          priority: "High"
        - id: "SVC-010"
          description: "Format backup info for display"
          testable: true
          test_requirement: "Test: Given backup, When format() called, Then returns version, date, size, reason"
          priority: "Medium"
        - id: "SVC-011"
          description: "Select backup interactively or by ID"
          testable: true
          test_requirement: "Test: Given backup ID, When select() called, Then correct backup returned"
          priority: "High"

    - type: "Service"
      name: "BackupCleaner"
      file_path: "installer/backup_cleaner.py"
      interface: "IBackupCleaner"
      lifecycle: "Singleton"
      dependencies:
        - "IBackupService"
        - "IFileSystem"
      requirements:
        - id: "SVC-012"
          description: "Delete backups exceeding retention limit"
          testable: true
          test_requirement: "Test: Given retention=5 and 7 backups, When cleanup() called, Then oldest 2 deleted"
          priority: "Medium"
        - id: "SVC-013"
          description: "Never delete backup being restored"
          testable: true
          test_requirement: "Test: Given active restore, When cleanup() called, Then active backup preserved"
          priority: "Critical"

    - type: "Service"
      name: "RollbackValidator"
      file_path: "installer/rollback_validator.py"
      interface: "IRollbackValidator"
      lifecycle: "Singleton"
      dependencies:
        - "IChecksumCalculator"
      requirements:
        - id: "SVC-014"
          description: "Validate restored files match backup"
          testable: true
          test_requirement: "Test: Given restored backup, When validate() called, Then all checksums match"
          priority: "Critical"
        - id: "SVC-015"
          description: "Check critical files exist"
          testable: true
          test_requirement: "Test: Given rollback, When validate() called, Then CLAUDE.md, .devforgeai/ exist"
          priority: "Critical"
        - id: "SVC-016"
          description: "Return validation report"
          testable: true
          test_requirement: "Test: Given validation run, When complete, Then ValidationReport returned"
          priority: "Medium"

    - type: "DataModel"
      name: "RollbackRequest"
      table: "N/A (in-memory)"
      purpose: "Request parameters for rollback operation"
      fields:
        - name: "backup_id"
          type: "String"
          constraints: "Required"
          description: "ID of backup to restore"
          test_requirement: "Test: backup_id resolves to valid backup"
        - name: "include_user_content"
          type: "Boolean"
          constraints: "Default false"
          description: "Whether to restore user content from backup"
          test_requirement: "Test: Default is false"
        - name: "is_automatic"
          type: "Boolean"
          constraints: "Required"
          description: "Whether rollback was triggered automatically"
          test_requirement: "Test: Automatic rollback sets is_automatic=True"
        - name: "failure_reason"
          type: "String"
          constraints: "Optional"
          description: "Why rollback was triggered (for automatic)"
          test_requirement: "Test: failure_reason set for automatic rollback"
      indexes: []
      relationships: []

    - type: "DataModel"
      name: "RollbackResult"
      table: ".devforgeai/logs/rollback-{timestamp}.log"
      purpose: "Result of rollback operation"
      fields:
        - name: "status"
          type: "Enum"
          constraints: "Required"
          description: "SUCCESS, PARTIAL, FAILED"
          test_requirement: "Test: status reflects actual outcome"
        - name: "from_version"
          type: "String"
          constraints: "Required"
          description: "Version before rollback"
          test_requirement: "Test: from_version is current version"
        - name: "to_version"
          type: "String"
          constraints: "Required"
          description: "Version after rollback"
          test_requirement: "Test: to_version matches backup version"
        - name: "files_restored"
          type: "Int"
          constraints: "Required"
          description: "Count of files restored"
          test_requirement: "Test: files_restored accurate"
        - name: "files_preserved"
          type: "Int"
          constraints: "Required"
          description: "Count of user files preserved"
          test_requirement: "Test: files_preserved accurate"
        - name: "validation_passed"
          type: "Boolean"
          constraints: "Required"
          description: "Whether post-rollback validation passed"
          test_requirement: "Test: validation_passed reflects validation result"
        - name: "duration_seconds"
          type: "Float"
          constraints: "Required"
          description: "Time taken for rollback"
          test_requirement: "Test: duration_seconds is positive"
      indexes: []
      relationships: []

    - type: "Configuration"
      name: "rollback-config.json"
      file_path: ".devforgeai/config/rollback-config.json"
      required_keys:
        - key: "backup_retention_count"
          type: "int"
          example: "5"
          required: false
          default: "5"
          validation: "Must be 1-20"
          test_requirement: "Test: Default is 5 if not specified"
        - key: "user_content_paths"
          type: "array"
          example: "['.ai_docs/Stories/', '.ai_docs/Epics/']"
          required: false
          default: "['.ai_docs/Stories/', '.ai_docs/Epics/', '.ai_docs/Sprints/', '.devforgeai/context/', '.devforgeai/adrs/']"
          validation: "Array of valid paths"
          test_requirement: "Test: User content paths are skipped during rollback"
        - key: "validate_after_rollback"
          type: "bool"
          example: "true"
          required: false
          default: "true"
          validation: "Boolean"
          test_requirement: "Test: Validation runs when true"

  business_rules:
    - id: "BR-001"
      rule: "Automatic rollback triggered on any upgrade failure"
      trigger: "When migration script exits non-zero OR validation fails"
      validation: "Check exit codes and validation results"
      error_handling: "Log error, execute rollback"
      test_requirement: "Test: Migration exit code 1 triggers automatic rollback"
      priority: "Critical"

    - id: "BR-002"
      rule: "User content is never overwritten without explicit flag"
      trigger: "When restoring files to user content directories"
      validation: "Check path against user_content_paths config"
      error_handling: "Skip file, add to preserved count"
      test_requirement: "Test: .ai_docs/Stories/ files not overwritten"
      priority: "Critical"

    - id: "BR-003"
      rule: "Rollback completes within 1 minute"
      trigger: "All rollback operations"
      validation: "Time tracking"
      error_handling: "Warning if exceeds 1 minute (don't fail)"
      test_requirement: "Test: Standard rollback < 60 seconds"
      priority: "High"

    - id: "BR-004"
      rule: "Safety backup created before manual rollback"
      trigger: "When manual rollback initiated"
      validation: "Backup creation completes before restore"
      error_handling: "Abort rollback if backup fails"
      test_requirement: "Test: Manual rollback creates backup first"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Rollback completes within 1 minute"
      metric: "< 60000ms for standard installation"
      test_requirement: "Test: restore() < 60s for 50MB backup"
      priority: "Critical"

    - id: "NFR-002"
      category: "Reliability"
      requirement: "Rollback success rate > 99%"
      metric: "99%+ successful rollbacks"
      test_requirement: "Test: 100 rollback simulations all succeed"
      priority: "Critical"

    - id: "NFR-003"
      category: "Reliability"
      requirement: "User content never lost during rollback"
      metric: "0% user content loss"
      test_requirement: "Test: User files identical before and after rollback cycle"
      priority: "Critical"

    - id: "NFR-004"
      category: "Security"
      requirement: "Rollback does not expose sensitive data"
      metric: "No secrets in logs"
      test_requirement: "Test: Rollback logs contain no passwords or tokens"
      priority: "High"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Rollback: < 1 minute for standard installation
- Backup listing: < 5 seconds
- Validation: < 30 seconds

---

### Reliability

**Success Rates:**
- Rollback success rate: > 99%
- User content preservation: 100%

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-078:** Upgrade Mode with Migration Scripts
  - **Why:** Creates backups that rollback restores from
  - **Status:** Backlog

### Technology Dependencies

None - uses existing backup infrastructure from STORY-078.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic

**Test Scenarios:**

1. **Happy Path:**
   - List available backups
   - Select and restore backup
   - Validate restoration success

2. **Edge Cases:**
   - Single backup available
   - No backups available
   - Backup with user content

3. **Error Cases:**
   - Corrupted backup
   - Permission denied during restore
   - Validation fails after restore

---

## Acceptance Criteria Verification Checklist

### AC#1: Automatic Rollback on Upgrade Failure
- [ ] Automatic rollback triggered on failure - **Phase:** 2 - **Evidence:** rollback_orchestrator_test.py
- [ ] Pre-upgrade backup restored - **Phase:** 2 - **Evidence:** backup_restorer_test.py
- [ ] Rollback < 1 minute - **Phase:** 4 - **Evidence:** performance test

### AC#2: Manual Rollback Command
- [ ] Backups listed for selection - **Phase:** 2 - **Evidence:** backup_selector_test.py
- [ ] Selected backup restored - **Phase:** 2 - **Evidence:** backup_restorer_test.py
- [ ] Safety backup created first - **Phase:** 2 - **Evidence:** rollback_orchestrator_test.py

### AC#3: List Available Backups
- [ ] All backups displayed - **Phase:** 2 - **Evidence:** backup_selector_test.py
- [ ] Sorted by date (newest first) - **Phase:** 2 - **Evidence:** backup_selector_test.py
- [ ] Details shown (version, date, size, reason) - **Phase:** 2 - **Evidence:** backup_selector_test.py

### AC#4: Restore from Backup
- [ ] Files restored to original locations - **Phase:** 2 - **Evidence:** backup_restorer_test.py
- [ ] .version.json reverted - **Phase:** 2 - **Evidence:** backup_restorer_test.py
- [ ] Validation confirms success - **Phase:** 2 - **Evidence:** rollback_validator_test.py

### AC#5: User Content Preservation
- [ ] Stories NOT overwritten - **Phase:** 2 - **Evidence:** backup_restorer_test.py
- [ ] Epics NOT overwritten - **Phase:** 2 - **Evidence:** backup_restorer_test.py
- [ ] Context files preserved - **Phase:** 2 - **Evidence:** backup_restorer_test.py
- [ ] --include-user-content flag works - **Phase:** 2 - **Evidence:** backup_restorer_test.py

### AC#6: Rollback Validation
- [ ] Checksums verified - **Phase:** 2 - **Evidence:** rollback_validator_test.py
- [ ] Critical files checked - **Phase:** 2 - **Evidence:** rollback_validator_test.py
- [ ] Validation results displayed - **Phase:** 2 - **Evidence:** CLI integration test

### AC#7: Rollback Summary Display
- [ ] Summary shows all details - **Phase:** 2 - **Evidence:** CLI integration test
- [ ] Summary saved to log - **Phase:** 2 - **Evidence:** file existence test

### AC#8: Backup Cleanup
- [ ] Oldest backups deleted at limit - **Phase:** 2 - **Evidence:** backup_cleaner_test.py
- [ ] Active backup never deleted - **Phase:** 2 - **Evidence:** backup_cleaner_test.py

---

**Checklist Progress:** 0/22 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] RollbackOrchestrator service implemented
- [ ] BackupRestorer service implemented
- [ ] BackupSelector service implemented
- [ ] BackupCleaner service implemented
- [ ] RollbackValidator service implemented
- [ ] All data models implemented

### Quality
- [ ] All 8 acceptance criteria have passing tests
- [ ] Edge cases covered
- [ ] NFRs met (< 1min rollback, 99%+ success)
- [ ] Code coverage > 95% for business logic

### Testing
- [ ] Unit tests for RollbackOrchestrator
- [ ] Unit tests for BackupRestorer
- [ ] Unit tests for BackupSelector
- [ ] Unit tests for BackupCleaner
- [ ] Unit tests for RollbackValidator
- [ ] Integration test for automatic rollback
- [ ] Integration test for manual rollback

### Documentation
- [ ] Rollback command usage guide
- [ ] Backup management guide

---

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Notes

**Design Decisions:**
- Safety backup before manual rollback prevents data loss
- User content preserved by default (can override with flag)
- Validation after rollback ensures success

**Related ADRs:**
- None yet

**References:**
- EPIC-014: Version Management & Installation Lifecycle
- STORY-078: Upgrade Mode with Migration Scripts

---

**Story Template Version:** 2.1
**Last Updated:** 2025-11-25
