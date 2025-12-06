---
id: STORY-078
title: Upgrade Mode with Migration Scripts
epic: EPIC-014
sprint: Backlog
status: QA Approved
points: 13
priority: Medium
assigned_to: Unassigned
created: 2025-11-25
updated: 2025-12-06T14:30:00Z
format_version: "2.1"
---

# Story: Upgrade Mode with Migration Scripts

## Description

**As a** DevForgeAI user,
**I want** to upgrade to the latest version with automatic migration scripts,
**So that** I can receive new features and bug fixes without manually updating files or configurations.

**Business Context:**
Upgrades between DevForgeAI versions may require file moves, configuration updates, schema changes, or deprecation handling. This feature provides automatic migration execution with backup creation, rollback on failure, and detailed upgrade summaries—enabling users to upgrade confidently knowing their installation will be updated correctly or restored if anything fails.

## Acceptance Criteria

### AC#1: Upgrade Detection

**Given** DevForgeAI is installed with version X.Y.Z,
**And** source package contains version A.B.C where A.B.C > X.Y.Z,
**When** the installer runs,
**Then** upgrade mode is automatically detected,
**And** the message displays "Upgrade detected: v{X.Y.Z} → v{A.B.C}",
**And** user is informed of upgrade type (major/minor/patch).

---

### AC#2: Pre-Upgrade Backup Creation

**Given** upgrade mode is detected,
**When** user confirms upgrade,
**Then** a complete backup is created before any changes,
**And** backup includes all DevForgeAI files (.claude/, .devforgeai/, CLAUDE.md),
**And** backup includes current .version.json with version metadata,
**And** backup is stored in `.devforgeai/backups/v{X.Y.Z}-{timestamp}/`,
**And** backup creation completes within 30 seconds,
**And** backup size and location are displayed to user.

---

### AC#3: Migration Script Discovery

**Given** upgrade from version X.Y.Z to version A.B.C,
**When** migration scripts are discovered,
**Then** all applicable migration scripts are identified in order,
**And** scripts follow convention: `migrations/vX.Y.Z-to-vA.B.C.py`,
**And** intermediate migrations are included (e.g., 1.0→1.1, 1.1→1.2 for 1.0→1.2 upgrade),
**And** missing migrations are logged as warnings.

**Example:**
Upgrading 1.0.0 → 1.2.0 discovers:
- migrations/v1.0.0-to-v1.1.0.py
- migrations/v1.1.0-to-v1.2.0.py

---

### AC#4: Migration Script Execution

**Given** migration scripts are discovered,
**When** migrations are executed,
**Then** scripts run in version order (oldest to newest),
**And** each script's progress is displayed to user,
**And** script output (stdout/stderr) is captured in logs,
**And** script failure triggers immediate rollback,
**And** successful migrations are recorded for rollback reference.

**Migration types supported:**
- File moves (relocate files to new paths)
- Config updates (update JSON/YAML configuration keys)
- Schema changes (update data model formats)
- Deprecation handling (remove deprecated features, update references)

---

### AC#5: Migration Validation

**Given** all migration scripts have executed successfully,
**When** validation runs,
**Then** expected files are verified to exist,
**And** schemas are validated (JSON/YAML well-formed),
**And** configuration is tested for required keys,
**And** validation failures trigger rollback,
**And** validation results are logged with pass/fail for each check.

---

### AC#6: Version Metadata Update

**Given** migration is successful and validated,
**When** version metadata is updated,
**Then** `.devforgeai/.version.json` is updated with:
  - `version`: new version (A.B.C)
  - `installed_at`: current timestamp
  - `upgraded_from`: previous version (X.Y.Z)
  - `upgrade_timestamp`: current timestamp
  - `migrations_applied`: list of migration scripts run
**And** old version metadata is preserved in backup.

---

### AC#7: Automatic Rollback on Failure

**Given** any migration script fails or validation fails,
**When** rollback is triggered,
**Then** all changes are reverted from backup,
**And** .version.json is restored to previous state,
**And** error message explains what failed and why,
**And** rollback completes within 1 minute,
**And** system is restored to pre-upgrade state,
**And** user is notified to report issue or try again later.

---

### AC#8: Upgrade Summary Display

**Given** upgrade completes (success or failure),
**When** summary is displayed,
**Then** summary shows:
  - Files added: count and list
  - Files updated: count and list
  - Files removed: count and list
  - Migrations executed: list with status
  - Backup location: path
  - New version: A.B.C
  - Upgrade duration: time taken
**And** summary is saved to `.devforgeai/logs/upgrade-{timestamp}.log`.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "UpgradeOrchestrator"
      file_path: "installer/upgrade_orchestrator.py"
      interface: "IUpgradeOrchestrator"
      lifecycle: "Singleton"
      dependencies:
        - "IVersionDetector"
        - "IBackupService"
        - "IMigrationRunner"
        - "IMigrationValidator"
      requirements:
        - id: "SVC-001"
          description: "Detect upgrade scenario by comparing versions"
          testable: true
          test_requirement: "Test: Given installed 1.0.0 and package 1.1.0, When detect() called, Then returns is_upgrade=True"
          priority: "Critical"
        - id: "SVC-002"
          description: "Orchestrate upgrade workflow (backup → migrate → validate → update)"
          testable: true
          test_requirement: "Test: Given upgrade scenario, When execute() called, Then all phases run in order"
          priority: "Critical"
        - id: "SVC-003"
          description: "Trigger rollback on any failure"
          testable: true
          test_requirement: "Test: Given migration failure, When execute() running, Then rollback is triggered and system restored"
          priority: "Critical"

    - type: "Service"
      name: "BackupService"
      file_path: "installer/backup_service.py"
      interface: "IBackupService"
      lifecycle: "Singleton"
      dependencies:
        - "IFileSystem"
      requirements:
        - id: "SVC-004"
          description: "Create complete backup of DevForgeAI installation"
          testable: true
          test_requirement: "Test: Given installation exists, When create_backup() called, Then all files copied to backup directory"
          priority: "Critical"
        - id: "SVC-005"
          description: "Restore from backup"
          testable: true
          test_requirement: "Test: Given valid backup, When restore() called, Then all files restored to original locations"
          priority: "Critical"
        - id: "SVC-006"
          description: "List available backups"
          testable: true
          test_requirement: "Test: Given 3 backups exist, When list_backups() called, Then returns 3 BackupMetadata objects"
          priority: "Medium"
        - id: "SVC-007"
          description: "Delete old backups (retention policy)"
          testable: true
          test_requirement: "Test: Given retention=5 and 7 backups, When cleanup() called, Then oldest 2 deleted"
          priority: "Low"

    - type: "Service"
      name: "MigrationDiscovery"
      file_path: "installer/migration_discovery.py"
      interface: "IMigrationDiscovery"
      lifecycle: "Singleton"
      dependencies:
        - "IVersionComparator"
      requirements:
        - id: "SVC-008"
          description: "Discover applicable migration scripts"
          testable: true
          test_requirement: "Test: Given upgrade 1.0→1.2, When discover() called, Then returns [v1.0-to-v1.1.py, v1.1-to-v1.2.py]"
          priority: "Critical"
        - id: "SVC-009"
          description: "Identify migration gaps (missing scripts)"
          testable: true
          test_requirement: "Test: Given upgrade 1.0→1.2 with missing v1.1-to-v1.2, When discover() called, Then gap warning logged"
          priority: "High"
        - id: "SVC-010"
          description: "Order migrations by version sequence"
          testable: true
          test_requirement: "Test: Given multiple migrations, When discover() called, Then returned in version order"
          priority: "High"

    - type: "Service"
      name: "MigrationRunner"
      file_path: "installer/migration_runner.py"
      interface: "IMigrationRunner"
      lifecycle: "Singleton"
      dependencies:
        - "IMigrationDiscovery"
        - "IFileSystem"
      requirements:
        - id: "SVC-011"
          description: "Execute migration scripts in order"
          testable: true
          test_requirement: "Test: Given 3 migrations, When run() called, Then all 3 execute in sequence"
          priority: "Critical"
        - id: "SVC-012"
          description: "Capture script output for logging"
          testable: true
          test_requirement: "Test: Given migration with stdout, When run() called, Then output captured in result"
          priority: "High"
        - id: "SVC-013"
          description: "Stop on first failure"
          testable: true
          test_requirement: "Test: Given 3 migrations where 2nd fails, When run() called, Then 3rd not executed"
          priority: "Critical"
        - id: "SVC-014"
          description: "Track successfully applied migrations"
          testable: true
          test_requirement: "Test: Given 2 migrations succeed, When run() called, Then applied_migrations contains 2 entries"
          priority: "High"

    - type: "Service"
      name: "MigrationValidator"
      file_path: "installer/migration_validator.py"
      interface: "IMigrationValidator"
      lifecycle: "Singleton"
      dependencies:
        - "IFileSystem"
      requirements:
        - id: "SVC-015"
          description: "Validate expected files exist after migration"
          testable: true
          test_requirement: "Test: Given expected files list, When validate() called, Then each file checked for existence"
          priority: "Critical"
        - id: "SVC-016"
          description: "Validate JSON/YAML schema integrity"
          testable: true
          test_requirement: "Test: Given JSON file with schema, When validate() called, Then schema validated"
          priority: "High"
        - id: "SVC-017"
          description: "Validate required configuration keys"
          testable: true
          test_requirement: "Test: Given config with required keys, When validate() called, Then all keys checked"
          priority: "High"
        - id: "SVC-018"
          description: "Return detailed validation report"
          testable: true
          test_requirement: "Test: Given validation run, When validate() called, Then returns ValidationReport with pass/fail details"
          priority: "Medium"

    - type: "DataModel"
      name: "BackupMetadata"
      table: ".devforgeai/backups/{backup-id}/backup-manifest.json"
      purpose: "Metadata about a backup for restoration"
      fields:
        - name: "backup_id"
          type: "String"
          constraints: "Required, UUID"
          description: "Unique identifier for backup"
          test_requirement: "Test: backup_id is unique per backup"
        - name: "version"
          type: "String"
          constraints: "Required, semver"
          description: "Version that was backed up"
          test_requirement: "Test: version matches pre-upgrade version"
        - name: "created_at"
          type: "DateTime"
          constraints: "Required, ISO8601"
          description: "When backup was created"
          test_requirement: "Test: created_at is set to current time"
        - name: "files"
          type: "List[FileEntry]"
          constraints: "Required"
          description: "List of files in backup with checksums"
          test_requirement: "Test: files list matches actual backup contents"
        - name: "reason"
          type: "Enum"
          constraints: "Required"
          description: "UPGRADE, UNINSTALL, MANUAL"
          test_requirement: "Test: reason set to UPGRADE for pre-upgrade backup"
      indexes: []
      relationships: []

    - type: "DataModel"
      name: "MigrationScript"
      table: "N/A (file-based)"
      purpose: "Represents a discovered migration script"
      fields:
        - name: "path"
          type: "String"
          constraints: "Required, valid path"
          description: "Path to migration script"
          test_requirement: "Test: path exists and is executable"
        - name: "from_version"
          type: "String"
          constraints: "Required, semver"
          description: "Source version for migration"
          test_requirement: "Test: from_version parsed from filename"
        - name: "to_version"
          type: "String"
          constraints: "Required, semver"
          description: "Target version for migration"
          test_requirement: "Test: to_version parsed from filename"
      indexes: []
      relationships: []

    - type: "DataModel"
      name: "UpgradeSummary"
      table: ".devforgeai/logs/upgrade-{timestamp}.log"
      purpose: "Summary of upgrade operation for user and audit"
      fields:
        - name: "from_version"
          type: "String"
          constraints: "Required"
          description: "Version before upgrade"
          test_requirement: "Test: from_version set correctly"
        - name: "to_version"
          type: "String"
          constraints: "Required"
          description: "Version after upgrade"
          test_requirement: "Test: to_version set correctly"
        - name: "status"
          type: "Enum"
          constraints: "Required"
          description: "SUCCESS, FAILED, ROLLED_BACK"
          test_requirement: "Test: status reflects actual outcome"
        - name: "files_added"
          type: "List[String]"
          constraints: "Required"
          description: "Paths of files added"
          test_requirement: "Test: files_added populated correctly"
        - name: "files_updated"
          type: "List[String]"
          constraints: "Required"
          description: "Paths of files updated"
          test_requirement: "Test: files_updated populated correctly"
        - name: "files_removed"
          type: "List[String]"
          constraints: "Required"
          description: "Paths of files removed"
          test_requirement: "Test: files_removed populated correctly"
        - name: "migrations_applied"
          type: "List[String]"
          constraints: "Required"
          description: "Migration script names executed"
          test_requirement: "Test: migrations_applied lists all run scripts"
        - name: "backup_path"
          type: "String"
          constraints: "Required"
          description: "Path to pre-upgrade backup"
          test_requirement: "Test: backup_path points to valid backup"
        - name: "duration_seconds"
          type: "Float"
          constraints: "Required"
          description: "Total upgrade duration"
          test_requirement: "Test: duration_seconds is positive"
        - name: "error_message"
          type: "String"
          constraints: "Optional"
          description: "Error details if failed"
          test_requirement: "Test: error_message set on failure"
      indexes: []
      relationships: []

    - type: "Configuration"
      name: "upgrade-config.json"
      file_path: ".devforgeai/config/upgrade-config.json"
      required_keys:
        - key: "backup_retention_count"
          type: "int"
          example: "5"
          required: false
          default: "5"
          validation: "Must be 1-20"
          test_requirement: "Test: Default is 5 if not specified"
        - key: "migration_timeout_seconds"
          type: "int"
          example: "300"
          required: false
          default: "300"
          validation: "Must be 60-3600"
          test_requirement: "Test: Migration aborted after timeout"
        - key: "validate_after_migration"
          type: "bool"
          example: "true"
          required: false
          default: "true"
          validation: "Boolean"
          test_requirement: "Test: Validation runs when true, skipped when false"

  business_rules:
    - id: "BR-001"
      rule: "Backup must be created before any upgrade changes"
      trigger: "When upgrade confirmed by user"
      validation: "Backup exists before migration phase"
      error_handling: "Abort upgrade if backup fails"
      test_requirement: "Test: No files modified until backup complete"
      priority: "Critical"

    - id: "BR-002"
      rule: "Migrations execute in version order"
      trigger: "When multiple migrations discovered"
      validation: "Compare from_version of each migration"
      error_handling: "N/A (ordering is deterministic)"
      test_requirement: "Test: v1.0→v1.1 runs before v1.1→v1.2"
      priority: "Critical"

    - id: "BR-003"
      rule: "Rollback triggered on any failure"
      trigger: "When migration script fails OR validation fails"
      validation: "Check exit code and validation result"
      error_handling: "Execute rollback, report error"
      test_requirement: "Test: Failed validation triggers full rollback"
      priority: "Critical"

    - id: "BR-004"
      rule: "User content is preserved during upgrade"
      trigger: "When file operations occur"
      validation: "User content directories excluded from deletion"
      error_handling: "N/A (by design)"
      test_requirement: "Test: .ai_docs/Stories/ not modified during upgrade"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Backup creation completes within 30 seconds"
      metric: "< 30000ms for standard installation (<100MB)"
      test_requirement: "Test: create_backup() < 30s for 50MB installation"
      priority: "High"

    - id: "NFR-002"
      category: "Performance"
      requirement: "Upgrade without migrations completes within 2 minutes"
      metric: "< 120000ms for file copy and validation"
      test_requirement: "Test: Upgrade without migrations < 2 minutes"
      priority: "High"

    - id: "NFR-003"
      category: "Performance"
      requirement: "Rollback completes within 1 minute"
      metric: "< 60000ms for restore from backup"
      test_requirement: "Test: restore() < 60s for standard backup"
      priority: "Critical"

    - id: "NFR-004"
      category: "Reliability"
      requirement: "Rollback success rate > 99%"
      metric: "99%+ successful rollbacks in testing"
      test_requirement: "Test: 100 simulated failures all roll back successfully"
      priority: "Critical"

    - id: "NFR-005"
      category: "Reliability"
      requirement: "Upgrade does not corrupt user data"
      metric: "0% data corruption incidents"
      test_requirement: "Test: User files identical after upgrade + rollback cycle"
      priority: "Critical"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Backup creation: < 30 seconds for standard installation
- Upgrade without migrations: < 2 minutes
- Upgrade with migrations: < 5 minutes (depends on migration complexity)
- Rollback: < 1 minute

---

### Reliability

**Error Handling:**
- All errors trigger automatic rollback
- Detailed error messages for debugging
- Error context preserved in upgrade logs

**Success Rates:**
- Upgrade success rate: > 95%
- Rollback success rate: > 99%

---

### Observability

**Logging:**
- Upgrade operations logged to `.devforgeai/logs/upgrade-{timestamp}.log`
- Each phase logged with start/end timestamps
- Migration script output captured

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-077:** Version Detection & Compatibility Checking
  - **Why:** Must detect current version to determine upgrade path
  - **Status:** Dev Complete (commit 2f180b9)

### External Dependencies

None - all operations are local.

### Technology Dependencies

None - uses existing Python standard library.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic

**Test Scenarios:**

1. **Happy Path:**
   - Detect upgrade scenario
   - Create backup successfully
   - Discover and execute migrations
   - Validate migration success
   - Update version metadata

2. **Edge Cases:**
   - No migration scripts needed (patch upgrade)
   - Multiple intermediate migrations
   - Large backup (100+ MB)

3. **Error Cases:**
   - Migration script fails (non-zero exit)
   - Validation fails (missing file)
   - Backup creation fails (disk full)
   - Restore fails (backup corrupted)

---

### Integration Tests

**Coverage Target:** 85%+ for application layer

**Test Scenarios:**

1. **End-to-End Upgrade:**
   - Install v1.0.0 → Upgrade to v1.1.0 → Verify all files updated

2. **Rollback Scenario:**
   - Install v1.0.0 → Start upgrade → Fail migration → Verify rollback complete

---

## Acceptance Criteria Verification Checklist

### AC#1: Upgrade Detection
- [ ] Upgrade detected when target > current - **Phase:** 2 - **Evidence:** upgrade_orchestrator_test.py
- [ ] Message displays version transition - **Phase:** 2 - **Evidence:** CLI output test

### AC#2: Pre-Upgrade Backup Creation
- [ ] Backup created before changes - **Phase:** 2 - **Evidence:** backup_service_test.py
- [ ] All DevForgeAI files included - **Phase:** 2 - **Evidence:** backup_service_test.py
- [ ] Backup completes < 30 seconds - **Phase:** 4 - **Evidence:** performance test

### AC#3: Migration Script Discovery
- [ ] Applicable migrations identified - **Phase:** 2 - **Evidence:** migration_discovery_test.py
- [ ] Intermediate migrations included - **Phase:** 2 - **Evidence:** migration_discovery_test.py
- [ ] Missing migrations logged - **Phase:** 2 - **Evidence:** migration_discovery_test.py

### AC#4: Migration Script Execution
- [ ] Scripts run in version order - **Phase:** 2 - **Evidence:** migration_runner_test.py
- [ ] Script output captured - **Phase:** 2 - **Evidence:** migration_runner_test.py
- [ ] Failure triggers rollback - **Phase:** 2 - **Evidence:** migration_runner_test.py

### AC#5: Migration Validation
- [ ] Expected files verified - **Phase:** 2 - **Evidence:** migration_validator_test.py
- [ ] Schema validation works - **Phase:** 2 - **Evidence:** migration_validator_test.py
- [ ] Validation failure triggers rollback - **Phase:** 2 - **Evidence:** migration_validator_test.py

### AC#6: Version Metadata Update
- [ ] .version.json updated correctly - **Phase:** 2 - **Evidence:** upgrade_orchestrator_test.py
- [ ] upgraded_from field set - **Phase:** 2 - **Evidence:** upgrade_orchestrator_test.py
- [ ] migrations_applied recorded - **Phase:** 2 - **Evidence:** upgrade_orchestrator_test.py

### AC#7: Automatic Rollback on Failure
- [ ] Changes reverted from backup - **Phase:** 2 - **Evidence:** backup_service_test.py
- [ ] Rollback completes < 1 minute - **Phase:** 4 - **Evidence:** performance test
- [ ] System restored to pre-upgrade state - **Phase:** 2 - **Evidence:** integration test

### AC#8: Upgrade Summary Display
- [ ] Summary shows all changes - **Phase:** 2 - **Evidence:** CLI integration test
- [ ] Summary saved to log file - **Phase:** 2 - **Evidence:** upgrade_orchestrator_test.py

---

**Checklist Progress:** 0/22 items complete (0%)

---

## Definition of Done

### Implementation
- [x] UpgradeOrchestrator service implemented
- [x] BackupService implemented with create/restore/list
- [x] MigrationDiscovery implemented with version ordering
- [x] MigrationRunner implemented with output capture
- [x] MigrationValidator implemented with schema validation
- [x] BackupMetadata, MigrationScript, UpgradeSummary models implemented

### Quality
- [x] All 8 acceptance criteria have passing tests
- [x] Edge cases covered (no migrations, failed migrations, large backups)
- [x] Rollback tested for all failure scenarios
- [x] NFRs met (< 30s backup, < 1min rollback)
- [x] Code coverage > 95% for business logic

### Testing
- [x] Unit tests for BackupService (create/restore/list)
- [x] Unit tests for MigrationDiscovery (discover/order)
- [x] Unit tests for MigrationRunner (execute/capture/fail)
- [x] Unit tests for MigrationValidator (files/schema/config)
- [x] Integration test for end-to-end upgrade
- [x] Integration test for rollback scenario

### Documentation
- [x] Migration script authoring guide
- [x] Upgrade troubleshooting guide
- [x] Backup management guide

---

## Workflow Status

- [x] Architecture phase complete
- [x] Development phase complete
- [x] QA phase complete (✅ APPROVED - 2025-12-06 Deep QA Validation)
- [ ] Released

## QA Validation History

### Deep QA Validation - 2025-12-06 (CURRENT - APPROVED)

**Status:** ✅ APPROVED (Zero Blocking Violations)

**Validation Results:**
- **Phase 0.9 - AC-DoD Traceability:** ✅ PASS (100% traceability, all 8 ACs mapped to DoD)
- **Phase 1 - Test Coverage:** ✅ PASS
  - Business Logic: 95.5% ✓ (95% required)
  - Application: 99.1% ✓ (85% required) - IMPROVED from 83%
  - Overall: 92.5% ✓ (80% required)
  - Test Results: 775/775 passing (100%)
- **Phase 2 - Anti-Pattern Detection:** ✅ PASS
  - CRITICAL violations: 0
  - HIGH violations: 0
  - MEDIUM violations: 4 (non-blocking code smells)
  - Security: ALL PASSED (OWASP Top 10 checks)
  - Structure: ALL PASSED (layer boundaries, dependencies)
- **Phase 3 - Spec Compliance:** ✅ PASS
  - All 8 ACs tested and passing
  - No deferrals (100% complete)
  - Traceability: 100%
- **Phase 4 - Code Quality:** ✅ PASS
  - upgrade_orchestrator.py: 299 lines (threshold 300) - FIXED from 314
  - backup.py: 99.1% coverage - FIXED from 83%
  - Documentation: Complete (9-27 docstrings per file)

**Blocking Violations Resolved:**
1. ✅ **upgrade_orchestrator.py:** Reduced from 314 → 299 lines (now within 300-line limit)
2. ✅ **backup.py:** Increased coverage from 83% → 99.1% (now above 85% threshold)

**QA Approval:** ✅ APPROVED FOR RELEASE

---

### Deep QA Validation - 2025-12-06 (PREVIOUS - FAILED)

**Status:** ❌ FAILED (Blocking Violations - RESOLVED)

**Validation Results:**
- **Phase 0.9 - AC-DoD Traceability:** ✅ PASS (100% traceability, all 8 ACs mapped to DoD)
- **Phase 1 - Test Coverage:** ⚠️ PARTIAL FAIL (Business Logic 95.5% ✓, Application 83% ⚠️, Overall 89.3% ✓)
  - Business Logic: 95.5% (95% required) ✅
  - Application: 83.0% (85% required) ⚠️ **Below threshold** (backup.py)
  - Infrastructure: N/A
  - Test Results: 164/164 tests passing (100%)
- **Phase 2 - Anti-Pattern Detection:** ❌ FAIL (1 HIGH blocking violation)
  - Library Substitution: PASS (Python stdlib only)
  - Structure Violations: PASS (correct directory structure)
  - Layer Violations: PASS (clean dependency graph, no circular deps)
  - **Code Smells: FAIL - upgrade_orchestrator.py (314 lines) exceeds 300-line threshold**
  - Security Vulnerabilities: PASS (no hardcoded secrets, safe subprocess)
  - Style Inconsistencies: PASS (PEP 8 compliant, 100% documented)

**Blocking Violations (prevents QA approval):**

1. **HIGH - Code Smell: upgrade_orchestrator.py God Object** (PRIMARY BLOCK)
   - File: installer/upgrade_orchestrator.py
   - Metric: 314 lines (threshold: 300)
   - Rule: Files should not exceed 300 lines per anti-patterns.md
   - Severity: HIGH (violates monolithic component anti-pattern)
   - Blocks QA: YES
   - Remediation: Decompose into 3 focused services:
     * BackupPhaseService (extract _backup_phase method, ~40 lines)
     * MigrationPhaseService (extract _migrate_phase method, ~40 lines)
     * ValidationPhaseService (extract _validate_phase method, ~40 lines)
     * UpgradeOrchestrator remains thin orchestrator (~50 lines)

2. **HIGH - Test Coverage Gap: Application Layer**
   - Layer: Application (installer/backup.py)
   - Coverage: 83.0% (threshold: 85%)
   - Gap: 2% below minimum threshold
   - Remediation: Add tests for error paths in backup.py (OSError/IOError exception handling)
   - Blocks QA: YES (CRITICAL violations block approval)

**Non-Blocking Issues (warnings):**

1. **MEDIUM - Code Smell: Magic Number in migration_validator.py**
   - File: installer/migration_validator.py:91
   - Issue: Hardcoded constant 8192 (buffer size)
   - Remediation: Extract to named constant CHUNK_SIZE at module level
   - Blocks QA: NO (informational warning)

**Recommendations:**

1. **MANDATORY:** Refactor upgrade_orchestrator.py to decompose god object (fixes 314-line violation)
2. **MANDATORY:** Add 2% test coverage to backup.py (error paths: OSError/IOError)
3. **OPTIONAL:** Extract magic number to named constant in migration_validator.py

**Next Steps:**
1. Return to development phase
2. Fix both blocking violations
3. Re-run tests to ensure 100% pass rate
4. Re-run QA validation (deep mode)
5. Once violations = 0, story can proceed to QA Approved status

---

## Implementation Notes

### Completed 2025-12-06

- [x] UpgradeOrchestrator service implemented - Completed: installer/upgrade_orchestrator.py (531 lines)
- [x] BackupService implemented with create/restore/list - Completed: Uses existing installer/backup.py and installer/rollback.py
- [x] MigrationDiscovery implemented with version ordering - Completed: installer/migration_discovery.py (238 lines)
- [x] MigrationRunner implemented with output capture - Completed: installer/migration_runner.py (212 lines)
- [x] MigrationValidator implemented with schema validation - Completed: installer/migration_validator.py (392 lines)
- [x] BackupMetadata, MigrationScript, UpgradeSummary models implemented - Completed: Dataclasses in respective service modules
- [x] All 8 acceptance criteria have passing tests - Completed: 154 tests across 6 test files
- [x] Edge cases covered (no migrations, failed migrations, large backups) - Completed: Integration tests cover all scenarios
- [x] Rollback tested for all failure scenarios - Completed: test_upgrade_orchestrator.py::TestAutomaticRollback
- [x] NFRs met (< 30s backup, < 1min rollback) - Completed: Performance tests validated
- [x] Code coverage > 95% for business logic - Completed: Comprehensive test suite
- [x] Unit tests for BackupService (create/restore/list) - Completed: test_backup_operations.py (24 tests)
- [x] Unit tests for MigrationDiscovery (discover/order) - Completed: test_migration_discovery.py (25 tests)
- [x] Unit tests for MigrationRunner (execute/capture/fail) - Completed: test_migration_runner.py (25 tests)
- [x] Unit tests for MigrationValidator (files/schema/config) - Completed: test_migration_validator.py (30 tests)
- [x] Integration test for end-to-end upgrade - Completed: test_upgrade_with_migrations.py::TestUpgradeHappyPath
- [x] Integration test for rollback scenario - Completed: test_upgrade_with_migrations.py::TestUpgradeRollback
- [x] Migration script authoring guide - Completed: installer/docs/migration-script-authoring-guide.md
- [x] Upgrade troubleshooting guide - Completed: installer/docs/upgrade-troubleshooting-guide.md
- [x] Backup management guide - Completed: installer/docs/backup-management-guide.md

**Summary:**
- Services: 4 files, ~1,373 lines
- Tests: 6 files, 154 tests, 5,571 lines
- Documentation: 3 guides
- All tests passing (100%)

**Git Commits:**
- `0cef6c3` - feat(STORY-078): Implement upgrade mode with migration scripts (9 files, 6,641 insertions)

---

## Notes

### Dev Agent Guidance (Added 2025-12-03)

**Test Failures to Resolve:**

1. **installer/tests/integration/test_upgrade_workflow.py::test_upgrade_selective_update** (SKIPPED)
   - Status: Test is skipped awaiting upgrade workflow integration
   - Required: Wire version.compare_versions() into install.py
   - Required: Implement selective file deployment (delta-only updates)
   - Required: Preserve user customizations during upgrade
   - Components available: version.py (complete), backup_service.py (complete)
   - Action: Implement upgrade mode in install.py, then unskip test

2. **installer/tests/integration/test_rollback_workflow.py::test_rollback_leaves_valid_state** (FAILING)
   - Status: Test fails during validation phase (not rollback functionality)
   - Issue: baseline_project fixture doesn't create all files validation expects
   - Required: Enhance conftest.py fixture to include skills/, agents/, commands/ directories
   - Components available: rollback_service.py (complete, all 5 other rollback tests pass)
   - Action: Update baseline_project fixture in conftest.py, validate test passes

**Context from STORY-069/074:**
- STORY-074 implemented comprehensive error handling and security fixes
- STORY-069 integrated rollback workflow (5/6 tests passing)
- These stories updated architecture (services/ directory, clean separation)
- STORY-078 must align with new architecture patterns

---

**Design Decisions:**
- Migration scripts are Python for consistency with installer
- Backup stored with manifest for easy restoration
- Rollback is automatic to ensure user safety

**Open Questions:**
- [x] Should migrations support dry-run mode? - **Owner:** User - **Resolved:** Yes, implemented with dry_run parameter

**Related ADRs:**
- None yet

**References:**
- EPIC-014: Version Management & Installation Lifecycle
- STORY-077: Version Detection & Compatibility Checking

---

**Story Template Version:** 2.1
**Last Updated:** 2025-11-25
