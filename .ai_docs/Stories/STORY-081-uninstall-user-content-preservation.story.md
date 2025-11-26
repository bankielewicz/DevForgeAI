---
id: STORY-081
title: Uninstall with User Content Preservation
epic: EPIC-014
sprint: Backlog
status: Backlog
points: 10
priority: Medium
assigned_to: Unassigned
created: 2025-11-25
format_version: "2.1"
---

# Story: Uninstall with User Content Preservation

## Description

**As a** DevForgeAI user,
**I want** to uninstall DevForgeAI cleanly with the option to preserve my work,
**So that** no orphaned files remain and I don't lose my stories, epics, or custom configurations.

**Business Context:**
Clean uninstallation is critical for users who want to remove DevForgeAI from a project or switch to a different tool. This feature provides complete removal of all framework files while offering the choice to preserve user-created content. Dry-run mode allows users to preview what will be removed before committing, and backup creation ensures data safety.

## Acceptance Criteria

### AC#1: Detect All Installed Files

**Given** DevForgeAI is installed with a valid manifest,
**When** uninstall command runs,
**Then** all installed files are detected via manifest (`.devforgeai/.install-manifest.json`),
**And** framework directories are identified: `.claude/`, `.devforgeai/`, `CLAUDE.md`,
**And** user content directories are identified: `.ai_docs/`, custom context files,
**And** CLI binaries are identified (if installed to PATH).

---

### AC#2: Uninstall Modes

**Given** user runs uninstall command,
**When** mode selection is presented,
**Then** two modes are available:
  - **Complete removal:** Remove ALL DevForgeAI files (framework + user content)
  - **Preserve user content:** Remove framework files, keep user-created content
**And** default is "Preserve user content" (safer option),
**And** user must explicitly choose "Complete removal" for full deletion.

---

### AC#3: Dry-Run Mode

**Given** user runs `devforgeai uninstall --dry-run`,
**When** dry-run executes,
**Then** list of files that WOULD be removed is displayed,
**And** NO files are actually deleted or modified,
**And** summary shows: files to remove, files to preserve, disk space freed,
**And** user can review before running actual uninstall.

---

### AC#4: Confirmation Prompt

**Given** user runs uninstall (not dry-run),
**When** file list is prepared,
**Then** confirmation prompt displays:
  - "The following X files will be removed: [list]"
  - "The following Y files will be preserved: [list]"
  - "This will free Z MB of disk space"
  - "Are you sure? This cannot be undone. [y/N]"
**And** default is No (safe),
**And** --yes flag bypasses confirmation.

---

### AC#5: Pre-Uninstall Backup

**Given** user confirms uninstall,
**When** backup is created,
**Then** complete backup is created before any deletions,
**And** backup includes ALL files (framework + user content),
**And** backup is stored outside installation directory,
**And** backup location is displayed to user,
**And** user can restore from backup if needed (reinstall + restore).

---

### AC#6: File Removal

**Given** backup is complete and user has confirmed,
**When** uninstall executes,
**Then** files are removed in safe order:
  1. Framework files (skills, agents, commands)
  2. Configuration files
  3. Framework directories (.claude/, .devforgeai/)
  4. Root files (CLAUDE.md if DevForgeAI-managed)
**And** user content is preserved (if preserve mode selected),
**And** empty directories are cleaned up.

---

### AC#7: CLI Cleanup

**Given** DevForgeAI CLI is installed (in PATH or local bin),
**When** uninstall includes CLI,
**Then** CLI binaries are removed from PATH/bin,
**And** shell integration is cleaned up (aliases, completions),
**And** user is notified if manual PATH cleanup needed.

---

### AC#8: Uninstall Summary

**Given** uninstall completes,
**When** summary is displayed,
**Then** summary shows:
  - Files removed: count and list
  - Files preserved: count and list (if preserve mode)
  - Disk space freed: MB
  - Backup location: path
  - Duration: time taken
**And** summary is saved to backup directory (for reference).

---

### AC#9: User Content Detection

**Given** uninstall needs to distinguish framework vs user content,
**When** content is classified,
**Then** user content includes:
  - Files created by user (stories, epics, sprints)
  - Files modified by user (context files with user changes)
  - Custom ADRs (user-created architecture decisions)
  - Custom configuration (user preferences)
**And** framework content includes:
  - Skills, agents, commands (from DevForgeAI package)
  - Templates, assets
  - CLI scripts
  - CLAUDE.md (if unmodified from template).

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "UninstallOrchestrator"
      file_path: "installer/uninstall_orchestrator.py"
      interface: "IUninstallOrchestrator"
      lifecycle: "Singleton"
      dependencies:
        - "IManifestManager"
        - "IBackupService"
        - "IFileRemover"
        - "IContentClassifier"
      requirements:
        - id: "SVC-001"
          description: "Orchestrate complete uninstall workflow"
          testable: true
          test_requirement: "Test: Given confirmed uninstall, When execute() called, Then backup → remove → cleanup completes"
          priority: "Critical"
        - id: "SVC-002"
          description: "Support dry-run mode"
          testable: true
          test_requirement: "Test: Given dry_run=True, When execute() called, Then no files modified"
          priority: "High"
        - id: "SVC-003"
          description: "Support preserve vs complete modes"
          testable: true
          test_requirement: "Test: Given preserve_user_content=True, When execute() called, Then .ai_docs/ not removed"
          priority: "Critical"

    - type: "Service"
      name: "ContentClassifier"
      file_path: "installer/content_classifier.py"
      interface: "IContentClassifier"
      lifecycle: "Singleton"
      dependencies:
        - "IManifestManager"
        - "IFileSystem"
      requirements:
        - id: "SVC-004"
          description: "Classify files as framework or user content"
          testable: true
          test_requirement: "Test: Given .ai_docs/Stories/STORY-001.md, When classify() called, Then returns USER_CONTENT"
          priority: "Critical"
        - id: "SVC-005"
          description: "Detect user-modified framework files"
          testable: true
          test_requirement: "Test: Given modified CLAUDE.md, When classify() called, Then returns MODIFIED_FRAMEWORK"
          priority: "High"
        - id: "SVC-006"
          description: "Handle files not in manifest"
          testable: true
          test_requirement: "Test: Given new file in .devforgeai/, When classify() called, Then returns USER_CREATED"
          priority: "High"

    - type: "Service"
      name: "FileRemover"
      file_path: "installer/file_remover.py"
      interface: "IFileRemover"
      lifecycle: "Singleton"
      dependencies:
        - "IFileSystem"
      requirements:
        - id: "SVC-007"
          description: "Remove files in safe order"
          testable: true
          test_requirement: "Test: Given file list, When remove() called, Then files removed in dependency order"
          priority: "High"
        - id: "SVC-008"
          description: "Clean up empty directories"
          testable: true
          test_requirement: "Test: Given empty .claude/skills/, When cleanup() called, Then directory removed"
          priority: "Medium"
        - id: "SVC-009"
          description: "Skip files marked for preservation"
          testable: true
          test_requirement: "Test: Given file with preserve=True, When remove() called, Then file not deleted"
          priority: "Critical"
        - id: "SVC-010"
          description: "Handle permission errors gracefully"
          testable: true
          test_requirement: "Test: Given read-only file, When remove() called, Then error logged, continues"
          priority: "High"

    - type: "Service"
      name: "CLICleaner"
      file_path: "installer/cli_cleaner.py"
      interface: "ICLICleaner"
      lifecycle: "Singleton"
      dependencies:
        - "IFileSystem"
      requirements:
        - id: "SVC-011"
          description: "Remove CLI binaries from PATH/bin"
          testable: true
          test_requirement: "Test: Given devforgeai in ~/bin/, When cleanup() called, Then binary removed"
          priority: "Medium"
        - id: "SVC-012"
          description: "Detect manual PATH cleanup needed"
          testable: true
          test_requirement: "Test: Given devforgeai in system PATH, When cleanup() called, Then warning displayed"
          priority: "Low"

    - type: "Service"
      name: "UninstallReporter"
      file_path: "installer/uninstall_reporter.py"
      interface: "IUninstallReporter"
      lifecycle: "Singleton"
      dependencies: []
      requirements:
        - id: "SVC-013"
          description: "Generate uninstall summary"
          testable: true
          test_requirement: "Test: Given uninstall result, When report() called, Then summary with all fields returned"
          priority: "Medium"
        - id: "SVC-014"
          description: "Calculate disk space freed"
          testable: true
          test_requirement: "Test: Given removed files, When calculate_space() called, Then returns correct MB"
          priority: "Low"
        - id: "SVC-015"
          description: "Save report to backup directory"
          testable: true
          test_requirement: "Test: Given backup path, When save_report() called, Then report written to backup dir"
          priority: "Medium"

    - type: "DataModel"
      name: "UninstallRequest"
      table: "N/A (in-memory)"
      purpose: "Parameters for uninstall operation"
      fields:
        - name: "mode"
          type: "Enum"
          constraints: "Required"
          description: "COMPLETE or PRESERVE_USER_CONTENT"
          test_requirement: "Test: Default mode is PRESERVE_USER_CONTENT"
        - name: "dry_run"
          type: "Boolean"
          constraints: "Default false"
          description: "Whether to simulate without changes"
          test_requirement: "Test: dry_run=True prevents file deletion"
        - name: "skip_backup"
          type: "Boolean"
          constraints: "Default false"
          description: "Whether to skip backup creation"
          test_requirement: "Test: skip_backup=True skips backup step"
        - name: "skip_confirmation"
          type: "Boolean"
          constraints: "Default false"
          description: "Whether to skip confirmation prompt (--yes)"
          test_requirement: "Test: skip_confirmation=True bypasses prompt"
      indexes: []
      relationships: []

    - type: "DataModel"
      name: "UninstallPlan"
      table: "N/A (in-memory)"
      purpose: "Plan of files to remove and preserve"
      fields:
        - name: "files_to_remove"
          type: "List[FileEntry]"
          constraints: "Required"
          description: "Files that will be deleted"
          test_requirement: "Test: files_to_remove populated correctly"
        - name: "files_to_preserve"
          type: "List[FileEntry]"
          constraints: "Required"
          description: "Files that will be kept"
          test_requirement: "Test: files_to_preserve populated for preserve mode"
        - name: "directories_to_remove"
          type: "List[String]"
          constraints: "Required"
          description: "Directories to clean up"
          test_requirement: "Test: directories_to_remove includes empty dirs"
        - name: "total_size_bytes"
          type: "Int"
          constraints: "Required"
          description: "Total size of files to remove"
          test_requirement: "Test: total_size_bytes calculated correctly"
      indexes: []
      relationships: []

    - type: "DataModel"
      name: "UninstallResult"
      table: "N/A (saved to backup)"
      purpose: "Result of uninstall operation"
      fields:
        - name: "status"
          type: "Enum"
          constraints: "Required"
          description: "SUCCESS, PARTIAL, FAILED"
          test_requirement: "Test: status reflects actual outcome"
        - name: "files_removed"
          type: "Int"
          constraints: "Required"
          description: "Count of files removed"
          test_requirement: "Test: files_removed accurate"
        - name: "files_preserved"
          type: "Int"
          constraints: "Required"
          description: "Count of files preserved"
          test_requirement: "Test: files_preserved accurate"
        - name: "space_freed_mb"
          type: "Float"
          constraints: "Required"
          description: "Disk space freed in MB"
          test_requirement: "Test: space_freed_mb calculated correctly"
        - name: "backup_path"
          type: "String"
          constraints: "Optional"
          description: "Path to backup (if created)"
          test_requirement: "Test: backup_path set when backup created"
        - name: "errors"
          type: "List[String]"
          constraints: "Required"
          description: "List of errors encountered"
          test_requirement: "Test: errors populated on failures"
        - name: "duration_seconds"
          type: "Float"
          constraints: "Required"
          description: "Time taken for uninstall"
          test_requirement: "Test: duration_seconds is positive"
      indexes: []
      relationships: []

    - type: "Configuration"
      name: "uninstall-config.json"
      file_path: ".devforgeai/config/uninstall-config.json"
      required_keys:
        - key: "default_mode"
          type: "string"
          example: "PRESERVE_USER_CONTENT"
          required: false
          default: "PRESERVE_USER_CONTENT"
          validation: "Must be COMPLETE or PRESERVE_USER_CONTENT"
          test_requirement: "Test: Default mode is PRESERVE_USER_CONTENT"
        - key: "user_content_patterns"
          type: "array"
          example: "['.ai_docs/**', '.devforgeai/context/*']"
          required: false
          default: "['.ai_docs/**', '.devforgeai/context/*', '.devforgeai/adrs/*']"
          validation: "Array of glob patterns"
          test_requirement: "Test: User content patterns used for classification"
        - key: "backup_before_uninstall"
          type: "bool"
          example: "true"
          required: false
          default: "true"
          validation: "Boolean"
          test_requirement: "Test: Backup created when true"

  business_rules:
    - id: "BR-001"
      rule: "Backup must be created before any deletions (unless skipped)"
      trigger: "When uninstall confirmed"
      validation: "Backup exists before file removal"
      error_handling: "Abort uninstall if backup fails"
      test_requirement: "Test: No files deleted until backup complete"
      priority: "Critical"

    - id: "BR-002"
      rule: "User content never deleted without explicit COMPLETE mode"
      trigger: "When mode is PRESERVE_USER_CONTENT"
      validation: "Check content classification before deletion"
      error_handling: "Skip user content files"
      test_requirement: "Test: .ai_docs/ preserved in default mode"
      priority: "Critical"

    - id: "BR-003"
      rule: "Confirmation required for destructive operations"
      trigger: "When uninstall is not dry-run"
      validation: "User must confirm or use --yes flag"
      error_handling: "Abort if not confirmed"
      test_requirement: "Test: Uninstall aborted without confirmation"
      priority: "High"

    - id: "BR-004"
      rule: "Uninstall leaves no orphaned files"
      trigger: "After uninstall completes"
      validation: "Verify all framework files removed"
      error_handling: "Report remaining files in summary"
      test_requirement: "Test: No .claude/ or .devforgeai/ files remain after COMPLETE uninstall"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Uninstall completes within 30 seconds"
      metric: "< 30000ms for standard installation"
      test_requirement: "Test: uninstall() < 30s for 500 files"
      priority: "High"

    - id: "NFR-002"
      category: "Reliability"
      requirement: "Uninstall completeness 100%"
      metric: "No orphaned framework files after complete uninstall"
      test_requirement: "Test: Zero framework files remain after COMPLETE mode"
      priority: "Critical"

    - id: "NFR-003"
      category: "Security"
      requirement: "Uninstall only removes DevForgeAI files"
      metric: "0 non-DevForgeAI files affected"
      test_requirement: "Test: Files outside DevForgeAI directories unchanged"
      priority: "Critical"

    - id: "NFR-004"
      category: "Reliability"
      requirement: "User content 100% preserved in preserve mode"
      metric: "All user content files exist after preserve mode uninstall"
      test_requirement: "Test: .ai_docs/ files identical after preserve mode"
      priority: "Critical"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Uninstall: < 30 seconds for standard installation
- Dry-run: < 10 seconds (read-only)
- Backup creation: < 30 seconds

---

### Reliability

**Success Rates:**
- Uninstall completeness: 100% (no orphaned files)
- User content preservation: 100% in preserve mode

---

### Security

**Scope:**
- Only removes files within DevForgeAI directories
- Never affects user's other project files

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-078:** Upgrade Mode with Migration Scripts
  - **Why:** Provides backup infrastructure
  - **Status:** Backlog

- [ ] **STORY-079:** Fix/Repair Installation Mode
  - **Why:** Provides manifest reading infrastructure
  - **Status:** Backlog

### Technology Dependencies

None - uses existing infrastructure.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic

**Test Scenarios:**

1. **Happy Path:**
   - Dry-run mode shows correct files
   - Complete uninstall removes all files
   - Preserve mode keeps user content

2. **Edge Cases:**
   - No manifest (reinstall scenario)
   - User-modified framework files
   - Empty installation

3. **Error Cases:**
   - Permission denied on file
   - Backup creation fails
   - User cancels confirmation

---

## Acceptance Criteria Verification Checklist

### AC#1: Detect All Installed Files
- [ ] Manifest files detected - **Phase:** 2 - **Evidence:** manifest_manager_test.py
- [ ] Framework directories identified - **Phase:** 2 - **Evidence:** content_classifier_test.py
- [ ] User content directories identified - **Phase:** 2 - **Evidence:** content_classifier_test.py

### AC#2: Uninstall Modes
- [ ] Complete removal mode works - **Phase:** 2 - **Evidence:** uninstall_orchestrator_test.py
- [ ] Preserve mode works - **Phase:** 2 - **Evidence:** uninstall_orchestrator_test.py
- [ ] Default is preserve mode - **Phase:** 2 - **Evidence:** uninstall_orchestrator_test.py

### AC#3: Dry-Run Mode
- [ ] Files listed without deletion - **Phase:** 2 - **Evidence:** uninstall_orchestrator_test.py
- [ ] Summary shows accurate counts - **Phase:** 2 - **Evidence:** CLI integration test

### AC#4: Confirmation Prompt
- [ ] Prompt displayed with details - **Phase:** 2 - **Evidence:** CLI integration test
- [ ] Default is No - **Phase:** 2 - **Evidence:** CLI integration test
- [ ] --yes bypasses prompt - **Phase:** 2 - **Evidence:** CLI integration test

### AC#5: Pre-Uninstall Backup
- [ ] Backup created before deletion - **Phase:** 2 - **Evidence:** uninstall_orchestrator_test.py
- [ ] Backup includes all files - **Phase:** 2 - **Evidence:** backup_service_test.py
- [ ] Backup location displayed - **Phase:** 2 - **Evidence:** CLI integration test

### AC#6: File Removal
- [ ] Files removed in safe order - **Phase:** 2 - **Evidence:** file_remover_test.py
- [ ] User content preserved - **Phase:** 2 - **Evidence:** file_remover_test.py
- [ ] Empty directories cleaned - **Phase:** 2 - **Evidence:** file_remover_test.py

### AC#7: CLI Cleanup
- [ ] CLI binaries removed - **Phase:** 2 - **Evidence:** cli_cleaner_test.py
- [ ] Manual cleanup notification - **Phase:** 2 - **Evidence:** CLI integration test

### AC#8: Uninstall Summary
- [ ] Summary shows all details - **Phase:** 2 - **Evidence:** uninstall_reporter_test.py
- [ ] Summary saved to backup - **Phase:** 2 - **Evidence:** uninstall_reporter_test.py

### AC#9: User Content Detection
- [ ] Stories classified as user content - **Phase:** 2 - **Evidence:** content_classifier_test.py
- [ ] Framework files classified correctly - **Phase:** 2 - **Evidence:** content_classifier_test.py
- [ ] Modified files detected - **Phase:** 2 - **Evidence:** content_classifier_test.py

---

**Checklist Progress:** 0/27 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] UninstallOrchestrator service implemented
- [ ] ContentClassifier service implemented
- [ ] FileRemover service implemented
- [ ] CLICleaner service implemented
- [ ] UninstallReporter service implemented
- [ ] All data models implemented

### Quality
- [ ] All 9 acceptance criteria have passing tests
- [ ] Edge cases covered
- [ ] NFRs met (< 30s uninstall, 100% preservation)
- [ ] Code coverage > 95% for business logic

### Testing
- [ ] Unit tests for ContentClassifier
- [ ] Unit tests for FileRemover
- [ ] Unit tests for UninstallOrchestrator
- [ ] Integration test for complete uninstall
- [ ] Integration test for preserve mode
- [ ] Integration test for dry-run

### Documentation
- [ ] Uninstall command usage guide
- [ ] Recovery guide (restore from backup)

---

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Notes

**Design Decisions:**
- Default is preserve mode to prevent accidental data loss
- Backup always created (can skip with flag for power users)
- Dry-run allows preview before commitment

**Related ADRs:**
- None yet

**References:**
- EPIC-014: Version Management & Installation Lifecycle

---

**Story Template Version:** 2.1
**Last Updated:** 2025-11-25
