---
id: STORY-060
title: Operational Sync for User Input Guidance System
epic: EPIC-011
sprint: SPRINT-2
status: Superseded
points: 2
priority: Medium
assigned_to: TBD
created: 2025-01-20
updated: 2025-11-24
superseded_by: STORY-065
format_version: "2.0"
---

# Story: Operational Sync for User Input Guidance System

## Description

**As a** DevForgeAI framework operator or CI/CD pipeline,
**I want** automated synchronization of source files (src/) to operational directories (.claude/, root CLAUDE.md),
**so that** the framework uses the latest guidance documentation without manual file copying errors.

---

## Acceptance Criteria

### 1. [ ] Sync Script Created and Executable

**Given** source files in src/ need to be synchronized to operational directories for runtime use
**When** the sync script is created at `tests/user-input-guidance/validate-sync.sh`
**Then** the script file exists with executable permissions (chmod +x, mode 755)
**And** the script includes a shebang line (`#!/bin/bash`) on the first line for Bash execution
**And** the script includes a header comment block (lines 2-10) describing:
  - Purpose: "Synchronize source files (src/) to operational directories (.claude/, root) for DevForgeAI User Input Guidance System"
  - Usage: "bash tests/user-input-guidance/validate-sync.sh [--dry-run] [--force] [--help]"
  - Dependencies: "Requires: md5sum (or md5 on macOS), cp, mkdir, stat, diff utilities"
  - Exit codes: "0=success, 1=missing source, 2=permission denied, 3=sync failed with rollback, 4=validation failed, 5=manual merge required, 6=insufficient disk space, 130=interrupted"
**And** the script can be invoked from repository root: `bash tests/user-input-guidance/validate-sync.sh` or `./tests/user-input-guidance/validate-sync.sh`
**And** the script supports 3 optional flags:
  - `--dry-run`: Show what would be synced without making changes
  - `--force`: Skip conflict detection, overwrite operational files
  - `--help`: Display usage documentation

---

### 2. [ ] Source File Discovery and Validation

**Given** the sync script needs to identify all files requiring synchronization from src/ to operational directories
**When** the script executes source file discovery (Phase 1 of sync workflow)
**Then** the script identifies exactly 3 source files requiring sync:
  - `src/CLAUDE.md` → `CLAUDE.md` (repository root)
  - `src/claude/memory/commands-reference.md` → `.claude/memory/commands-reference.md`
  - `src/claude/memory/skills-reference.md` → `.claude/memory/skills-reference.md`
**And** the script defines source→operational mappings as Bash arrays:
```bash
SOURCE_FILES=(
  "src/CLAUDE.md"
  "src/claude/memory/commands-reference.md"
  "src/claude/memory/skills-reference.md"
)

OPERATIONAL_FILES=(
  "CLAUDE.md"
  ".claude/memory/commands-reference.md"
  ".claude/memory/skills-reference.md"
)
```
**And** the script verifies all 3 source files exist using test -f checks in a loop
**And** if any source file is missing:
  - Logs error to stderr: "ERROR: Missing source file: [path]. Run STORY-052-058 to create source files."
  - Exits with status code 1 (missing source files)
  - Does NOT proceed to operational directory validation (no point syncing if source incomplete)
**And** if all 3 source files exist:
  - Logs to stdout: "✓ Source file discovery complete: Found 3 files ready for sync"
  - Proceeds to Phase 2 (Operational Directory Validation)

**Test:** Delete src/CLAUDE.md, execute script, verify exit status 1 and error listing missing file; restore file, execute, verify discovery success and proceeds to next phase.

---

### 3. [ ] Operational Directory Validation

**Given** the sync script needs to verify operational directories exist before copying files
**When** the script validates operational directories (Phase 2 of sync workflow)
**Then** the script checks existence of required operational directories:
  - Root directory (always exists, no check needed)
  - `.claude/` directory
  - `.claude/memory/` directory
**And** for each directory, if missing:
  - Creates directory with `mkdir -p [directory]` (creates parent directories automatically)
  - Logs to stdout: "ℹ️ Created missing operational directory: [path]"
  - Verifies creation succeeded via test -d check
  - If creation fails (e.g., read-only filesystem, permission denied):
    - Logs error to stderr: "ERROR: Cannot create directory [path]. Check file system permissions or mount status."
    - Exits with status code 2 (permission denied)
    - Does NOT proceed to sync (cannot sync without writable directories)
**And** for each existing directory:
  - Verifies write permissions using test -w checks
  - If no write permission:
    - Logs error to stderr: "ERROR: No write permission for directory [path]. Check file system permissions (chmod +w or sudo)."
    - Exits with status code 2 (permission denied)
    - Does NOT proceed to sync
**And** if all directories exist and are writable:
  - Logs to stdout: "✓ Operational directory validation complete: All directories writable"
  - Proceeds to Phase 3 (Conflict Detection)

**Test:** Delete .claude/ directory, execute script, verify created with mkdir -p and script continues; create .claude/ with read-only permissions (chmod 555), execute script, verify error "No write permission" and exit status 2.

---

### 4. [ ] Conflict Detection via Content Hashing

**Given** operational files may have been modified independently from source files (concurrent development, manual edits, other stories)
**When** the sync script checks for conflicts before copying (Phase 3 of sync workflow)
**Then** the script calculates MD5 hashes for all 3 source files:
```bash
# Linux
SOURCE_HASHES=(
  $(md5sum "src/CLAUDE.md" | awk '{print $1}')
  $(md5sum "src/claude/memory/commands-reference.md" | awk '{print $1}')
  $(md5sum "src/claude/memory/skills-reference.md" | awk '{print $1}')
)

# macOS (uses md5 instead of md5sum)
SOURCE_HASHES=(
  $(md5 -q "src/CLAUDE.md")
  $(md5 -q "src/claude/memory/commands-reference.md")
  $(md5 -q "src/claude/memory/skills-reference.md")
)
```
**And** the script calculates MD5 hashes for all 3 operational files (if they exist, skip if doesn't exist yet):
```bash
OPERATIONAL_HASHES=()
for file in "${OPERATIONAL_FILES[@]}"; do
  if [ -f "$file" ]; then
    OPERATIONAL_HASHES+=($(md5sum "$file" | awk '{print $1}'))
  else
    OPERATIONAL_HASHES+=("NEW_FILE")  # Marker for non-existent file
  fi
done
```
**And** the script compares hashes pairwise (source[0] vs operational[0], source[1] vs operational[1], source[2] vs operational[2]):
```bash
CONFLICTS=()
for i in {0..2}; do
  if [ "${OPERATIONAL_HASHES[$i]}" != "NEW_FILE" ] && \
     [ "${SOURCE_HASHES[$i]}" != "${OPERATIONAL_HASHES[$i]}" ]; then
    CONFLICTS+=("${OPERATIONAL_FILES[$i]}")
  fi
done
```
**And** if a source file hash differs from its corresponding operational file hash (excluding NEW_FILE marker):
  - Logs warning to stdout: "⚠️ Conflict detected: ${OPERATIONAL_FILES[$i]} modified independently"
  - Logs hash details: "  Source hash: ${SOURCE_HASHES[$i]}"
  - Logs hash details: "  Operational hash: ${OPERATIONAL_HASHES[$i]}"
  - Adds file to CONFLICTS array
**And** if ≥1 conflict detected and --force flag NOT provided:
  - Presents interactive menu to user:
```
Conflicts detected (${#CONFLICTS[@]} files):
${CONFLICTS[@]}

Actions:
  [1] Overwrite operational files (sync from source)
  [2] Manual merge required (exit, resolve conflicts manually)
  [3] Show diff (display content differences)
  [4] Cancel sync operation

Select action [1-4]:
```
  - If user selects 1 (Overwrite): Sets FORCE_OVERWRITE=true, proceeds to Phase 4 (File Sync)
  - If user selects 2 (Manual merge): Logs "Manual merge required for ${#CONFLICTS[@]} files", exits with status 5 (manual merge)
  - If user selects 3 (Show diff): Displays `diff -u [source] [operational]` for each conflict, re-prompts for action
  - If user selects 4 (Cancel): Logs "Sync cancelled by user", exits with status 0 (user choice, not error)
**And** if --force flag provided:
  - Logs to stdout: "ℹ️ --force flag active: Skipping conflict detection, will overwrite operational files"
  - Skips conflict check entirely, proceeds directly to Phase 4
**And** if 0 conflicts detected:
  - Logs to stdout: "✓ No conflicts detected: Operational files match source or don't exist"
  - Proceeds to Phase 4 (File Sync)

**Test:** Modify operational CLAUDE.md (add line), run script without --force, verify conflict detected, verify menu presented; select option 3, verify diff displayed; select option 1, verify proceeds to sync; re-run with --force flag, verify skips conflict check.

---

### 5. [ ] File Synchronization Execution

**Given** no conflicts detected OR user chose overwrite option OR --force flag provided
**When** the sync script executes file synchronization (Phase 4 of sync workflow)
**Then** for each of the 3 source→operational pairs, the script:
  1. Creates backup of operational file (if exists) before overwriting: `cp [operational] [operational].bak-[timestamp]`
  2. Copies source file to operational destination: `cp -f [source] [operational]`
  3. Verifies successful copy via exit status check: `if [ $? -ne 0 ]; then error_handler; fi`
  4. Logs success for that file: "✓ Synced: [source] → [operational]"
**And** the script uses timestamp format YYYY-MM-DD-HH-MM-SS for backup filenames: `CLAUDE.md.bak-2025-01-20-15-45-32`
**And** if copy command fails for any file (exit status ≠ 0):
  - Logs error to stderr: "ERROR: Sync failed for [operational-file]: [error from cp command]"
  - Triggers rollback procedure (Phase 6 - Rollback):
    1. Restores all backups created in this sync operation (for files already copied)
    2. Deletes any partially copied files
    3. Verifies rollback via hash comparison (operational files match pre-sync hashes)
  - Generates sync report with status "FAILED (rollback completed)"
  - Exits with status code 3 (sync failure with rollback)
  - Retains backup files for manual inspection (does NOT delete backups)
**And** if all 3 copy operations succeed:
  - Logs to stdout: "✅ Successfully synchronized 3 files"
  - Proceeds to Phase 5 (Post-Sync Validation)

**Test:** Simulate copy failure by making operational directory read-only during sync, verify error logged, verify rollback executed, verify exit status 3, verify backups retained; restore permissions, re-run, verify all 3 files synced successfully.

---

### 6. [ ] Post-Sync Validation

**Given** file synchronization completed successfully (all 3 cp commands succeeded)
**When** the sync script validates post-sync state (Phase 5 of sync workflow)
**Then** the script recalculates MD5 hashes for all 3 operational files (post-sync hashes):
```bash
POST_SYNC_HASHES=(
  $(md5sum "CLAUDE.md" | awk '{print $1}')
  $(md5sum ".claude/memory/commands-reference.md" | awk '{print $1}')
  $(md5sum ".claude/memory/skills-reference.md" | awk '{print $1}')
)
```
**And** the script compares post-sync operational hashes against source hashes (SOURCE_HASHES from Phase 3):
```bash
VALIDATION_FAILURES=()
for i in {0..2}; do
  if [ "${POST_SYNC_HASHES[$i]}" != "${SOURCE_HASHES[$i]}" ]; then
    VALIDATION_FAILURES+=("${OPERATIONAL_FILES[$i]}")
  fi
done
```
**And** if all 3 hash pairs match (post-sync operational = source):
  - Logs to stdout: "✅ Post-sync validation passed: Operational files match source"
  - Proceeds to Phase 7 (Sync Report Generation)
**And** if any hash pair does NOT match:
  - Logs error to stderr: "ERROR: Post-sync validation failed for ${#VALIDATION_FAILURES[@]} files:"
  - For each failed file, logs details:
    - File: [operational-file]
    - Source hash: [source hash]
    - Operational hash (post-sync): [post-sync hash]
    - Issue: "Operational hash does not match source hash. Sync incomplete or file corrupted during copy."
  - Exits with status code 4 (post-sync validation failed)
  - Does NOT trigger rollback (files already synced, corruption detected, manual investigation needed)
**And** the script also verifies operational file sizes match source file sizes:
```bash
# Linux
SOURCE_SIZE=$(stat -c%s "src/CLAUDE.md")
OPERATIONAL_SIZE=$(stat -c%s "CLAUDE.md")

# macOS
SOURCE_SIZE=$(stat -f%z "src/CLAUDE.md")
OPERATIONAL_SIZE=$(stat -f%z "CLAUDE.md")

if [ $SOURCE_SIZE -ne $OPERATIONAL_SIZE ]; then
  echo "ERROR: File size mismatch: [operational] size $OPERATIONAL_SIZE bytes != [source] size $SOURCE_SIZE bytes"
  exit 4
fi
```
**And** if size mismatch detected:
  - Logs error: "File size mismatch detected for [file]. Possible truncation or corruption."
  - Exits with status 4 (adds to validation failure)

**Test:** After successful sync, manually corrupt one operational file (append random bytes), run post-sync validation phase, verify hash mismatch detected and exit status 4; manually truncate one operational file, verify size mismatch detected.

---

### 7. [ ] Sync Report Generation

**Given** the sync operation is complete (success, failure, or interrupted)
**When** the sync script generates a sync report (Phase 7 of sync workflow, always executes regardless of outcome)
**Then** the script creates a timestamped report file at `tests/user-input-guidance/reports/sync-report-YYYY-MM-DD-HH-MM-SS.txt` with ISO 8601 timestamp
**And** the report includes all required sections in this order:
  1. **Header:** "DevForgeAI Operational Sync Report - User Input Guidance System"
  2. **Execution Timestamp:** "Started: YYYY-MM-DD HH:MM:SS", "Completed: YYYY-MM-DD HH:MM:SS", "Duration: [N] seconds"
  3. **Source Files:** List of 3 source file paths with sizes
  4. **Operational Files:** List of 3 operational file paths with sizes (or "NEW" if didn't exist before sync)
  5. **Pre-Sync State:** Source hashes, operational hashes (or "NEW"), conflict count
  6. **Conflict Detection Results:** Number of conflicts detected, details for each conflict (source hash, operational hash, action taken)
  7. **Synchronization Results:** Per-file sync status (SUCCESS, FAILED, SKIPPED), error messages if any
  8. **Post-Sync Validation:** Hash comparisons (source vs operational post-sync), size comparisons, validation pass/fail
  9. **Backup Information:** List of backup files created with timestamps and sizes
  10. **Exit Status:** Numeric code (0-6, 130) and meaning ("0 = Success: All files synchronized and validated")
**And** the report is formatted as human-readable plain text (not JSON, not binary):
  - Section headers use "##" for major sections
  - Lists use "-" bullets
  - Tables use ASCII art: `| Column | Value |`
  - Hash values use monospace formatting
**And** the report is appended to a cumulative sync log: `tests/user-input-guidance/reports/sync-history.log`:
```bash
# Append to cumulative log (create if doesn't exist)
cat "reports/sync-report-$TIMESTAMP.txt" >> "reports/sync-history.log"
echo "---" >> "reports/sync-history.log"  # Separator between reports
```
**And** the cumulative log retains all sync operations for audit trail (no rotation, grows indefinitely)

**Test:** Execute script, verify report created with timestamp, verify contains all 10 sections, verify human-readable format, verify appended to sync-history.log; run script again, verify second report appended (cumulative log has both).

---

### 8. [ ] Rollback Capability

**Given** the sync script may encounter failures during file synchronization (copy errors, permission issues, disk full)
**When** a sync failure is detected mid-operation (e.g., copy 1 of 3 succeeds, copy 2 of 3 fails)
**Then** the script maintains backups of each operational file before overwriting:
```bash
# Before copying, create backup
TIMESTAMP=$(date +%Y-%m-%d-%H-%M-%S)

for i in {0..2}; do
  OPERATIONAL_FILE="${OPERATIONAL_FILES[$i]}"

  if [ -f "$OPERATIONAL_FILE" ]; then
    # Create backup with timestamp
    BACKUP_FILE="${OPERATIONAL_FILE}.bak-${TIMESTAMP}"
    cp "$OPERATIONAL_FILE" "$BACKUP_FILE"

    # Verify backup created successfully
    if [ ! -f "$BACKUP_FILE" ]; then
      echo "ERROR: Backup creation failed for $OPERATIONAL_FILE"
      exit 6  # Insufficient disk space or permission issue
    fi

    echo "✓ Backup created: $BACKUP_FILE"
    BACKUPS_CREATED+=("$BACKUP_FILE")
  fi
done
```
**And** if sync fails during copy operations:
  - Triggers rollback function: `rollback_sync()`
  - Restores backups for all already-synchronized files:
```bash
rollback_sync() {
  echo "⚠️ Rollback initiated: Restoring pre-sync state..."

  for backup in "${BACKUPS_CREATED[@]}"; do
    # Extract original filename (remove .bak-TIMESTAMP suffix)
    original_file=$(echo "$backup" | sed 's/\.bak-[0-9-]*$//')

    # Restore backup
    mv "$backup" "$original_file"

    echo "✓ Restored: $original_file from backup"
  done
}
```
  - Logs rollback actions to stdout: "Rollback initiated. Restoring [file] from backup [backup-file]"
  - Deletes any incomplete copied files (files copied but not yet validated)
  - After rollback completes, verifies operational files match pre-sync state via hash comparison:
```bash
# Recalculate operational hashes post-rollback
ROLLBACK_HASHES=()
for file in "${OPERATIONAL_FILES[@]}"; do
  if [ -f "$file" ]; then
    ROLLBACK_HASHES+=($(md5sum "$file" | awk '{print $1}'))
  else
    ROLLBACK_HASHES+=("DELETED")  # File was new, deleted during rollback
  fi
done

# Compare rollback hashes to pre-sync operational hashes (from Phase 3)
for i in {0..2}; do
  if [ "${ROLLBACK_HASHES[$i]}" != "${OPERATIONAL_HASHES[$i]}" ]; then
    echo "ERROR: Rollback incomplete for ${OPERATIONAL_FILES[$i]}"
    echo "  Pre-sync hash: ${OPERATIONAL_HASHES[$i]}"
    echo "  Post-rollback hash: ${ROLLBACK_HASHES[$i]}"
    exit 7  # Rollback failure (very serious - data integrity issue)
  fi
done

echo "✅ Rollback verification passed: Operational files restored to pre-sync state"
```
**And** after successful rollback:
  - Generates sync report with status "FAILED (rollback completed)"
  - Exits with status code 3 (sync failed with rollback)
  - Retains backup files in place (does NOT delete backups, allows manual inspection)
**And** if rollback itself fails (cannot restore backup, hash mismatch after restore):
  - Logs critical error: "CRITICAL: Rollback failed for [file]. Manual recovery required."
  - Exits with status code 7 (rollback failure - very serious)
  - Leaves system in partially rolled-back state (manual intervention needed)

**Test:** Simulate copy failure by removing write permission from operational directory after first copy succeeds, verify rollback triggered, verify backup restored, verify pre-sync hash matches post-rollback hash, verify exit status 3, verify backup files retained.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Script"
      name: "validate-sync"
      file_path: "tests/user-input-guidance/validate-sync.sh"
      requirements:
        - id: "SYNC-001"
          description: "Create executable Bash script with proper shebang (#!/bin/bash) and executable permissions (chmod +x, mode 755)"
          testable: true
          test_requirement: "Test: test -x validate-sync.sh returns 0 (executable), head -1 validate-sync.sh shows '#!/bin/bash'"
          priority: "Critical"

        - id: "SYNC-002"
          description: "Discover 3 source files (src/CLAUDE.md, src/claude/memory/commands-reference.md, src/claude/memory/skills-reference.md) and verify all exist via test -f checks"
          testable: true
          test_requirement: "Test: Script finds all 3 files via array iteration and test -f, exits with status 1 if any missing, logs 'Found 3 source files' if all present"
          priority: "Critical"

        - id: "SYNC-003"
          description: "Validate operational directories (.claude/, .claude/memory/) exist and are writable, create with mkdir -p if missing"
          testable: true
          test_requirement: "Test: Delete .claude/ directory, run script, verify created via mkdir -p, verify script continues; create .claude/ with read-only permissions, verify script exits with status 2 'No write permission'"
          priority: "Critical"

        - id: "SYNC-004"
          description: "Calculate MD5 hashes for all 6 files (3 source + 3 operational) for conflict detection, handle NEW_FILE marker for non-existent operational files"
          testable: true
          test_requirement: "Test: Run script with existing operational files, verify 6 hashes calculated; delete operational files, run script, verify operational hashes marked as 'NEW_FILE'"
          priority: "Critical"

        - id: "SYNC-005"
          description: "Detect conflicts by comparing source vs operational hashes, present interactive menu if conflicts found (unless --force flag provided)"
          testable: true
          test_requirement: "Test: Modify operational CLAUDE.md, run script without --force, verify conflict detected via hash mismatch, verify interactive menu presented; run with --force, verify menu skipped"
          priority: "Critical"

        - id: "SYNC-006"
          description: "Copy source files to operational destinations using cp -f, verify each copy operation's exit status, trigger rollback on any failure"
          testable: true
          test_requirement: "Test: Run script with writable operational dirs, verify all 3 files copied via cp -f; simulate copy failure (remove write permission mid-sync), verify rollback triggered"
          priority: "Critical"

        - id: "SYNC-007"
          description: "Perform post-sync validation by recalculating operational hashes and comparing to source hashes, verify file sizes also match"
          testable: true
          test_requirement: "Test: After sync, verify script recalculates hashes, compares to source, logs 'Post-sync validation passed' if match, exits with status 4 if mismatch; manually corrupt operational file post-sync, verify detection"
          priority: "Critical"

        - id: "SYNC-008"
          description: "Generate timestamped sync report (sync-report-YYYY-MM-DD-HH-MM-SS.txt) with 10 required sections, append to cumulative sync-history.log"
          testable: true
          test_requirement: "Test: Execute script, verify report created with timestamp, verify contains Header/Timestamp/SourceFiles/OperationalFiles/PreSync/Conflicts/Results/Validation/Backups/ExitStatus sections, verify appended to sync-history.log"
          priority: "High"

        - id: "SYNC-009"
          description: "Create backups of operational files before overwriting (if files exist), use timestamp in backup filename ([file].bak-YYYY-MM-DD-HH-MM-SS)"
          testable: true
          test_requirement: "Test: Run script, verify backups created for all existing operational files, verify backup filenames include timestamp, verify backups are valid copies (hash matches original)"
          priority: "Critical"

        - id: "SYNC-010"
          description: "Implement rollback capability that restores backups if sync fails, verifies restoration via hash comparison, retains backups for inspection"
          testable: true
          test_requirement: "Test: Simulate sync failure, verify rollback restores backups, verify post-rollback hashes match pre-sync hashes, verify backups not deleted (retained for inspection)"
          priority: "Critical"

        - id: "SYNC-011"
          description: "Support 3 command-line flags: --dry-run (show changes without applying), --force (skip conflict detection), --help (display usage)"
          testable: true
          test_requirement: "Test: Execute with --dry-run, verify shows sync plan but doesn't modify files; execute with --force on conflicted files, verify skips conflict menu; execute with --help, verify displays usage documentation"
          priority: "Medium"

        - id: "SYNC-012"
          description: "Implement signal handlers for SIGINT and SIGTERM to ensure graceful cleanup on interruption, restore backups, exit with status 130"
          testable: true
          test_requirement: "Test: Start script, interrupt with Ctrl+C (SIGINT) during copy phase, verify trap handler executes, verify backups restored, verify incomplete copies deleted, verify exit status 130"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Sync must be atomic (all 3 files sync successfully, or none do - no partial sync states allowed)"
      test_requirement: "Test: Simulate partial failure (file 1 copies, file 2 fails, file 3 not attempted), verify rollback restores file 1 to pre-sync state, verify file 3 never modified, verify final state = all 3 operational files unchanged from pre-sync"

    - id: "BR-002"
      rule: "Conflicts require explicit user choice or --force flag (no silent overwrites, no automatic merge logic)"
      test_requirement: "Test: Create conflict (modify operational file independently), run script without --force, verify script HALTS with interactive menu, verify does NOT proceed to sync without user choice; provide --force flag, verify skips conflict detection and overwrites"

    - id: "BR-003"
      rule: "Backups must be created BEFORE any file modifications to guarantee data preservation"
      test_requirement: "Test: Monitor script execution with strace or similar, verify backup creation (cp operational → backup) occurs before sync copy (cp source → operational), verify backup timestamp < sync timestamp"

    - id: "BR-004"
      rule: "Post-sync validation must verify BOTH hash and size match (hash alone insufficient - could have same hash with different size due to collision, though unlikely)"
      test_requirement: "Test: After sync, verify script checks both md5sum hash and stat size, verify both must match for validation to pass"

    - id: "BR-005"
      rule: "Exit status codes must be distinct and meaningful (enables automated error handling in CI/CD)"
      test_requirement: "Test: Trigger each of 7 exit scenarios (success=0, missing source=1, permission=2, sync failed=3, validation failed=4, manual merge=5, disk space=6, interrupted=130), verify correct status code returned for each"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Complete sync operation (all phases) must execute quickly for rapid deployment cycles"
      metric: "< 10 seconds to complete full sync workflow (discovery, validation, hash calculation, backup creation, file copying, post-sync validation, report generation) for all 3 files on standard hardware"
      test_requirement: "Test: Execute script with time command (time bash validate-sync.sh), measure wall-clock time, assert <10 seconds (repeat 10 times, calculate p95, verify <10s)"

    - id: "NFR-002"
      category: "Performance"
      requirement: "Hash calculation must be fast to minimize sync overhead"
      metric: "< 2 seconds to calculate MD5 hashes for all 6 files (3 source + 3 operational) using md5sum utility"
      test_requirement: "Test: Execute md5sum on all 6 files, measure execution time, assert <2 seconds (md5sum is optimized C implementation, very fast for small files <100KB)"

    - id: "NFR-003"
      category: "Performance"
      requirement: "Diff generation for conflict resolution must be fast for good UX"
      metric: "< 1 second to generate unified diff for each file pair using diff -u command"
      test_requirement: "Test: Execute diff -u [source] [operational] for each of 3 files, measure time per diff, assert <1 second each (total <3 seconds for all 3)"

    - id: "NFR-004"
      category: "Performance"
      requirement: "Rollback execution must be fast to minimize downtime if sync fails"
      metric: "< 5 seconds to restore all 3 backup files and verify restoration via hash comparison"
      test_requirement: "Test: Trigger rollback (simulate sync failure), measure rollback execution time from failure detection to verification complete, assert <5 seconds"

    - id: "NFR-005"
      category: "Reliability"
      requirement: "Sync operations must be atomic (all files synced successfully or all rolled back to original state)"
      metric: "100% atomicity: 0 partial sync states where some files synced and others didn't (measured across 100 test runs with random failure injection)"
      test_requirement: "Test: Run script 100 times with random failure injection (simulate copy failure at random file, random phase), verify 100% of failures result in complete rollback (no partial states), verify 0 data loss incidents"

    - id: "NFR-006"
      category: "Reliability"
      requirement: "Backup integrity must be guaranteed (backups must be valid copies, not corrupted or truncated)"
      metric: "100% of backups created must be valid and restorable (hash of backup = hash of original file before backup)"
      test_requirement: "Test: For each operational file, create backup, calculate md5sum of backup, compare to original file hash (before backup), assert identical; restore backup, calculate hash, compare to backup hash, assert identical"

    - id: "NFR-007"
      category: "Reliability"
      requirement: "Signal handling (SIGINT, SIGTERM) must prevent inconsistent states (no partial copies, no lost backups)"
      metric: "100% cleanup on interruption: backups restored, incomplete copies deleted, operational files in pre-sync state (tested with 50 interruptions at random phases)"
      test_requirement: "Test: Interrupt script with kill -INT at 10 random points during execution (Phase 1-7), verify cleanup handler executes within <2 seconds, verify backups restored, verify no incomplete files left, verify exit status 130 for all interruptions"

    - id: "NFR-008"
      category: "Reliability"
      requirement: "Post-sync validation must catch corruption (hash and size checks detect any data integrity issues)"
      metric: "100% detection rate for file corruption (any byte difference detected via hash mismatch OR size mismatch)"
      test_requirement: "Test: After sync, manually modify operational file (append byte, truncate byte, modify byte in middle), run post-sync validation, verify 100% detection across 30 modification scenarios"

    - id: "NFR-009"
      category: "Reliability"
      requirement: "Sync must be idempotent (running script multiple times with identical source/operational files produces no changes)"
      metric: "0 changes on repeated execution when source = operational (script detects 'already synchronized' state, exits cleanly with status 0)"
      test_requirement: "Test: Run script successfully, then immediately run again without modifying files, verify logs 'No changes detected: Operational files already synchronized', verify status 0, verify no backups created (no sync needed)"

    - id: "NFR-010"
      category: "Maintainability"
      requirement: "Script must use modular functions for reusability and testability"
      metric: "≥ 5 reusable Bash functions: calculate_hash(), create_backup(), restore_backup(), validate_post_sync(), generate_report(), plus helper functions"
      test_requirement: "Test: Grep script for 'function [name]()' or '[name]()' declarations, count function definitions, verify ≥5, verify functions are actually called (not dead code)"

    - id: "NFR-011"
      category: "Maintainability"
      requirement: "Source→operational file mappings must be centrally configured (not scattered throughout script)"
      metric: "100% of sync pairs defined in arrays at top of script (SOURCE_FILES and OPERATIONAL_FILES arrays), 0 hardcoded paths in sync logic"
      test_requirement: "Test: Grep script for SOURCE_FILES and OPERATIONAL_FILES array declarations, verify both present in first 30 lines, grep sync loop for hardcoded 'src/CLAUDE.md' or '.claude/' paths, verify 0 matches (all use array variables)"

    - id: "NFR-012"
      category: "Maintainability"
      requirement: "Script must include clear logging with prefixes for log levels (INFO, WARN, ERROR)"
      metric: "100% of log messages use prefixes: '✓' for success, 'ℹ️' for info, '⚠️' for warnings, 'ERROR:' for errors"
      test_requirement: "Test: Grep script output for log messages, verify all use prefixes, verify stderr used for errors (2>&1 redirection), stdout for info/success"

    - id: "NFR-013"
      category: "Maintainability"
      requirement: "Sync reports must be version control friendly (timestamped filenames prevent merge conflicts)"
      metric: "0 merge conflicts when multiple sync reports exist in reports/ directory (each report has unique timestamp)"
      test_requirement: "Test: Run script 5 times (1 per second), verify 5 distinct report files created (no overwrites), verify Git operations on reports/ don't show conflicts"

    - id: "NFR-014"
      category: "Quality"
      requirement: "Zero data loss must be guaranteed (backups created, rollback succeeds, no file deletions without backups)"
      metric: "0 data loss incidents: operational files always recoverable to pre-sync state if sync fails (tested with 100 failure scenarios)"
      test_requirement: "Test: Inject 100 random failures (permission errors, disk full, copy errors, interruptions), verify 100% of failures result in successful rollback OR complete sync (no data loss), verify no operational files corrupted or lost"

    - id: "NFR-015"
      category: "Quality"
      requirement: "Comprehensive testing via self-test mode (--test flag)"
      metric: "Self-test mode creates mock source/operational files, runs full sync workflow, validates results, cleans up, exits with status 0 if all assertions pass"
      test_requirement: "Test: Execute bash validate-sync.sh --test, verify creates /tmp/sync-test-* files, runs sync, validates hashes match, deletes test files, exits with status 0"

    - id: "NFR-016"
      category: "Usability"
      requirement: "Script must support --dry-run mode for safe previewing of sync operations"
      metric: "--dry-run mode shows exactly what would be synced (file pairs, conflicts, actions) without modifying any files"
      test_requirement: "Test: Modify operational file, run script with --dry-run, verify shows 'Would sync: src/CLAUDE.md → CLAUDE.md (CONFLICT)', verify operational file unchanged after script completes"

    - id: "NFR-017"
      category: "Usability"
      requirement: "Script must provide comprehensive help documentation via --help flag"
      metric: "--help output includes: purpose (what script does), usage (command syntax), flags (all 3 flags documented), exit codes (all 7 codes explained), examples (≥3 usage examples)"
      test_requirement: "Test: Execute bash validate-sync.sh --help, verify output contains 'Purpose:', 'Usage:', 'Flags:', 'Exit Codes:', 'Examples:' sections, verify all flags and exit codes documented"

    - id: "NFR-018"
      category: "Usability"
      requirement: "Conflict diff display must be readable and informative (unified format with context lines)"
      metric: "Diff output uses diff -u format with 3 context lines before/after changes for readability"
      test_requirement: "Test: Create conflict, select 'Show diff' option, verify output uses unified format (lines prefixed with -, +, or space for context), verify includes file headers (--- source, +++ operational)"

    - id: "NFR-019"
      category: "Security"
      requirement: "Script must not execute user-provided paths or filenames (no injection vulnerabilities)"
      metric: "100% of file paths are hardcoded constants or validated inputs (no eval, no dynamic execution of filenames)"
      test_requirement: "Test: Review script for eval usage (grep 'eval', expect 0 matches), review for dynamic path construction (verify all paths from SOURCE_FILES/OPERATIONAL_FILES arrays), test with filenames containing special characters (;, |, &, >, <), verify no command injection"

    - id: "NFR-020"
      category: "Security"
      requirement: "Backups must not be world-readable (preserve original file permissions, no permission escalation)"
      metric: "Backup files inherit permissions from original operational files (if CLAUDE.md is 644, backup is 644; if 600, backup is 600)"
      test_requirement: "Test: Set operational file permissions to 600, run sync (creates backup), verify backup permissions = 600 (stat -c%a), not 644 or 666"
```

---

## Edge Cases

### 1. Simultaneous Source and Operational Modifications

**Scenario:** Between STORY-052-058 completion (source files modified) and STORY-060 sync execution, both source files (src/) and operational files (CLAUDE.md, .claude/memory/*.md) are independently modified by different stories, manual edits, or concurrent developers.

**Example:**
- STORY-058 updates src/CLAUDE.md with "Learning DevForgeAI" section (line 380)
- Concurrently, another developer updates operational CLAUDE.md with custom notes (line 800)
- Both modifications are valid, but syncing would overwrite the operational custom notes

**Expected Behavior:**
- Conflict detection (AC4, Phase 3) calculates hashes:
  - src/CLAUDE.md hash: `abc123...`
  - CLAUDE.md hash: `def456...` (different due to custom notes)
  - Conflict detected: hashes don't match
- Script logs conflict:
```
⚠️ Conflict detected: CLAUDE.md modified independently
  Source hash (src/CLAUDE.md): abc123...
  Operational hash (CLAUDE.md): def456...
```
- Script presents interactive menu:
```
Conflicts detected (1 file): CLAUDE.md

Actions:
  [1] Overwrite operational (sync from source) - Custom notes will be lost
  [2] Manual merge required (exit, resolve conflicts, re-run sync)
  [3] Show diff (display content differences between source and operational)
  [4] Cancel sync operation

Select action [1-4]:
```
- If user selects 3 (Show diff):
  - Executes: `diff -u src/CLAUDE.md CLAUDE.md | less`
  - Displays unified diff showing both changes (STORY-058 section + custom notes)
  - After diff, re-prompts for action (returns to menu)
- If user selects 2 (Manual merge):
  - Logs: "Manual merge required for 1 file: CLAUDE.md. Resolve conflicts and re-run sync."
  - Exits with status code 5 (manual merge required)
  - Does NOT modify any files
  - Suggests merge strategy: "Use diff3 or git merge to combine changes, then re-run sync."
- If user selects 1 (Overwrite):
  - Logs warning: "⚠️ Overwriting operational CLAUDE.md (custom notes will be lost)"
  - Creates backup: `CLAUDE.md.bak-2025-01-20-15-45-32`
  - Proceeds to Phase 4 (File Sync) - copies source over operational
  - Custom notes lost but backed up (user can manually reintegrate from backup if needed)

**Validation:** Modify operational CLAUDE.md (add line), run script, verify conflict detected; select option 3, verify diff displayed showing both source changes and operational changes; select option 2, verify exits with status 5 and no files modified; re-run with option 1, verify operational overwritten and backup created.

**Why this matters:** Concurrent modifications are common in active development. Conflict detection prevents silent data loss. Interactive menu gives user control (overwrite, merge, or cancel).

**Recovery:** If overwrite chosen by mistake, restore from backup: `cp CLAUDE.md.bak-[timestamp] CLAUDE.md`, manually merge changes, re-run sync.

---

### 2. Missing .claude/ Directory (Fresh Repository Clone)

**Scenario:** A developer clones the DevForgeAI repository for the first time. The .claude/ operational directory doesn't exist yet because the framework hasn't been run (no /create-context executed, no skills invoked).

**Expected Behavior:**
- Operational directory validation (AC3, Phase 2) checks for `.claude/` and `.claude/memory/`
- Detects `.claude/` missing: `! test -d .claude`
- Creates missing directory: `mkdir -p .claude/memory` (creates both .claude and .claude/memory in one command)
- Logs to stdout: "ℹ️ Created missing operational directory: .claude/memory"
- Verifies creation succeeded: `test -d .claude/memory`
- If creation succeeds:
  - Proceeds to Phase 3 (Conflict Detection)
  - Note: No conflicts possible (operational files don't exist yet, all marked as NEW_FILE)
- If creation fails (e.g., filesystem is read-only, mounted as ro, permission denied):
  - Logs error to stderr: "ERROR: Cannot create directory .claude/memory. Check file system permissions or mount status."
  - Provides troubleshooting hints: "Possible causes: read-only filesystem, insufficient permissions, disk full"
  - Exits with status code 2 (permission denied / directory creation failed)

**Validation:** Delete .claude/ directory entirely, execute script, verify directory created with mkdir -p, verify sync proceeds to create all 3 files (fresh deployment); mount filesystem as read-only, execute script, verify creation fails with status 2 and clear error.

**Why this matters:** Fresh clones common scenario (new developers, CI/CD agents, deployment targets). Auto-creating directories enables zero-configuration sync. Clear errors guide troubleshooting if creation fails.

**Recovery:** If creation fails due to permissions, fix permissions (chmod +w parent directory or sudo), re-run script.

---

### 3. Symbolic Link Instead of Regular File

**Scenario:** One of the operational files (e.g., CLAUDE.md in repository root) is a symbolic link pointing to another location (e.g., symlink to a shared documentation server at `/mnt/shared-docs/CLAUDE.md` or symlink to another repo).

**Example:**
```bash
# CLAUDE.md is a symlink
ls -la CLAUDE.md
lrwxrwxrwx 1 user user 45 Jan 20 10:00 CLAUDE.md -> /mnt/shared-docs/DevForgeAI-CLAUDE.md
```

**Expected Behavior:**
- Before sync Phase 4 (File Sync), script detects symbolic links using `test -L [file]`:
```bash
for i in {0..2}; do
  OPERATIONAL_FILE="${OPERATIONAL_FILES[$i]}"

  if [ -L "$OPERATIONAL_FILE" ]; then
    # Symlink detected
    SYMLINK_TARGET=$(readlink "$OPERATIONAL_FILE")
    echo "⚠️ Warning: $OPERATIONAL_FILE is a symbolic link"
    echo "   Target: $SYMLINK_TARGET"
    echo "   Copying will replace symlink with regular file."
    echo ""
    read -p "Continue with sync for this file? [y/N]: " confirm

    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
      echo "ℹ️ Skipping sync for $OPERATIONAL_FILE (symlink preserved)"
      SYNC_RESULTS[$i]="SKIPPED (symlink)"
      continue  # Skip this file, proceed to next
    else
      echo "Replacing symlink with regular file from source..."
      rm "$OPERATIONAL_FILE"  # Delete symlink
      # Proceed to copy (next iteration will copy source to this location)
    fi
  fi
done
```
- If user declines (answer: N):
  - Script skips that file in sync operation
  - Marks as "SKIPPED (symlink)" in sync results
  - Logs: "ℹ️ Skipped CLAUDE.md (user chose to preserve symlink)"
  - Continues with remaining 2 files (partial sync allowed for symlink preservation)
  - Sync report notes: "1 file skipped (symlink), 2 files synced"
- If user confirms (answer: y):
  - Script deletes symlink: `rm CLAUDE.md`
  - Copies source file as regular file: `cp src/CLAUDE.md CLAUDE.md`
  - Logs: "✓ Replaced symlink CLAUDE.md with regular file from source"
  - Symlink target file unchanged (only symlink deleted, not target)

**Validation:** Create symlink `ln -s /tmp/test-claude.md CLAUDE.md`, run script, verify warning displayed with symlink target, answer "N", verify file skipped and symlink preserved; re-run, answer "y", verify symlink deleted and replaced with regular file.

**Why this matters:** Symlinks used for shared documentation or multi-repo setups. Replacing symlink with regular file breaks those setups. User confirmation prevents unexpected breakage.

**Alternative:** If --force flag provided, skip symlink confirmation, always replace (automated mode).

---

### 4. Insufficient Disk Space for Backups

**Scenario:** The sync script creates backups (AC8) before overwriting operational files (3 files × ~50KB each = ~150KB total backups), but disk space is insufficient to store all backups (e.g., disk 99.9% full, only 100KB available).

**Expected Behavior:**
- Before creating any backups, script checks available disk space using `df` command:
```bash
# Get available space in KB
if [ "$(uname)" = "Darwin" ]; then
  # macOS
  AVAILABLE_KB=$(df -k . | tail -1 | awk '{print $4}')
else
  # Linux
  AVAILABLE_KB=$(df -k . | tail -1 | awk '{print $4}')
fi

# Calculate total size of operational files (files to backup)
TOTAL_SIZE_KB=0
for file in "${OPERATIONAL_FILES[@]}"; do
  if [ -f "$file" ]; then
    if [ "$(uname)" = "Darwin" ]; then
      SIZE_BYTES=$(stat -f%z "$file")
    else
      SIZE_BYTES=$(stat -c%s "$file")
    fi
    SIZE_KB=$((SIZE_BYTES / 1024))
    TOTAL_SIZE_KB=$((TOTAL_SIZE_KB + SIZE_KB))
  fi
done

# Require 1.1x space (10% buffer for filesystem overhead)
REQUIRED_KB=$((TOTAL_SIZE_KB * 11 / 10))

if [ $AVAILABLE_KB -lt $REQUIRED_KB ]; then
  echo "ERROR: Insufficient disk space for backups"
  echo "  Available: ${AVAILABLE_KB}KB"
  echo "  Required: ${REQUIRED_KB}KB (110% of operational files size for backups)"
  echo "  Shortfall: $((REQUIRED_KB - AVAILABLE_KB))KB"
  echo ""
  echo "Free up space and retry: rm old files, clean temp directories, etc."
  exit 6  # Insufficient disk space
fi
```
- If disk space check fails (available < required):
  - Logs error with details (available space, required space, shortfall)
  - Provides remediation guidance (how to free space)
  - Exits with status code 6 (insufficient disk space, distinct from other failures)
  - Does NOT attempt to create backups (would fail and potentially corrupt filesystem)
- If backup creation fails despite space check passing (race condition: space consumed between check and backup):
  - Catches copy error: `cp [file] [backup] || backup_failed=true`
  - Logs error: "ERROR: Backup creation failed for [file] (disk space consumed during execution?)"
  - Immediately exits with status 6
  - Does NOT proceed with sync (no sync without backups - zero data loss guarantee)

**Validation:** Mock low disk space by filling disk to 99% capacity, run script, verify space check detects insufficient space before attempting backups, verify exit status 6 and clear error with available/required/shortfall values.

**Why this matters:** Creating backups without checking space could fill disk completely, causing filesystem corruption or system instability. Pre-flight check prevents this.

**Recovery:** Free up disk space (delete temp files, old logs, unused files), re-run script, verify space check passes and sync proceeds.

---

### 5. Sync Script Interrupted Mid-Execution (SIGINT, SIGTERM)

**Scenario:** The sync script is interrupted by user pressing Ctrl+C (SIGINT signal) or by system sending kill command (SIGTERM signal) while copying files, creating backups, or validating results.

**Expected Behavior:**
- Script registers trap handlers at startup (before any file operations):
```bash
#!/bin/bash

# Global state for cleanup
BACKUPS_CREATED=()
CLEANUP_NEEDED=false

# Cleanup function (called on interrupt or error)
cleanup_and_exit() {
  local exit_code=$1

  echo ""
  echo "⚠️ Sync interrupted or failed. Initiating cleanup..."

  # Restore all backups created so far
  if [ ${#BACKUPS_CREATED[@]} -gt 0 ]; then
    echo "Restoring ${#BACKUPS_CREATED[@]} backup(s)..."
    for backup in "${BACKUPS_CREATED[@]}"; do
      original=$(echo "$backup" | sed 's/\.bak-[0-9-]*$//')
      mv "$backup" "$original" 2>/dev/null
      echo "  ✓ Restored: $original"
    done
  fi

  # Delete any incomplete copies (files in .claude/ newer than backups)
  # (Implementation: check mtime, delete if created during sync)

  # Generate sync report with INTERRUPTED/FAILED status
  generate_report "INTERRUPTED" "$exit_code"

  echo "Cleanup complete. Operational files restored to pre-sync state."
  exit $exit_code
}

# Register trap handlers
trap 'cleanup_and_exit 130' INT   # Ctrl+C
trap 'cleanup_and_exit 130' TERM  # kill command
```
- On interrupt signal (SIGINT or SIGTERM):
  - Trap handler `cleanup_and_exit` executes immediately
  - Logs to stdout: "⚠️ Sync interrupted. Initiating cleanup..."
  - Restores all backups created so far (iterates BACKUPS_CREATED array)
  - Deletes any incomplete copied files (files modified during sync but not yet validated)
  - Verifies restoration via hash comparison (post-cleanup hashes = pre-sync hashes)
  - Generates sync report with status "INTERRUPTED" and exit code 130
  - Exits with status code 130 (standard exit code for SIGINT/SIGTERM)
- Cleanup must complete within <2 seconds (fast enough to not annoy user)
- Trap handlers must be idempotent (if called twice, no errors)
- All file operations in cleanup use 2>/dev/null to suppress errors (files may not exist)

**Validation:** Execute script, interrupt with Ctrl+C after 1st file copied but before 2nd file, verify trap handler executes, verify 1st file restored from backup, verify 2nd file never created, verify exit status 130; repeat test interrupting at different phases (backup creation, hash calculation, report generation), verify cleanup always succeeds.

**Why this matters:** Users may need to cancel sync (wrong source files, conflicts discovered, urgent interruption). Trap handlers ensure no partial state left (all files restored or none synced).

**Recovery:** Re-run sync after interruption, verify starts from clean state (no leftover partial copies, no orphaned backups).

---

### 6. macOS vs Linux Compatibility (Platform-Specific Commands)

**Scenario:** The sync script uses Linux-specific commands (md5sum, stat -c%s) but is executed on macOS which has different command syntax (md5 -q, stat -f%z).

**Expected Behavior:**
- Script detects platform at startup using `uname`:
```bash
PLATFORM=$(uname)

if [ "$PLATFORM" = "Darwin" ]; then
  # macOS detected
  HASH_CMD="md5 -q"
  STAT_SIZE_CMD="stat -f%z"
  STAT_PERMS_CMD="stat -f%p"
else
  # Linux (or other Unix)
  HASH_CMD="md5sum"
  STAT_SIZE_CMD="stat -c%s"
  STAT_PERMS_CMD="stat -c%a"
fi
```
- All hash calculations use platform-specific command:
```bash
# Calculate hash (works on both platforms)
calculate_hash() {
  local file=$1

  if [ "$PLATFORM" = "Darwin" ]; then
    md5 -q "$file"
  else
    md5sum "$file" | awk '{print $1}'
  fi
}
```
- All file size checks use platform-specific stat:
```bash
get_file_size() {
  local file=$1

  if [ "$PLATFORM" = "Darwin" ]; then
    stat -f%z "$file"
  else
    stat -c%s "$file"
  fi
}
```
- Script logs platform detected: "Platform: macOS" or "Platform: Linux"
- Script works identically on both platforms (same behavior, same output, same exit codes)

**Validation:** Execute script on Linux, verify uses md5sum and stat -c%s, verify completes successfully; execute script on macOS, verify uses md5 -q and stat -f%z, verify completes successfully; compare sync reports from both platforms, verify identical results (excluding timestamps).

**Why this matters:** DevForgeAI developers use both macOS and Linux. Platform compatibility ensures sync works for all developers without modification.

**Cross-platform commands used:**
- `cp -f`: Works identically on macOS and Linux
- `mkdir -p`: Works identically
- `test -f/-d/-L/-w`: Works identically
- `diff -u`: Works identically
- Platform detection required only for: hash calculation (md5sum vs md5), file stats (stat -c vs stat -f)

---

### 7. Rollback Verification Failure (Post-Rollback Hash Mismatch)

**Scenario:** Sync fails (copy error), rollback executes (restores backups), but post-rollback verification detects hash mismatch (operational file after rollback ≠ operational file before sync). This indicates backup corruption, restore failure, or concurrent modification during rollback.

**Expected Behavior:**
- Rollback function (triggered in AC8, Edge Case 5) restores backups: `mv [backup] [original]`
- After all restorations, rollback verification runs:
```bash
# Recalculate operational hashes post-rollback
for i in {0..2}; do
  OPERATIONAL_FILE="${OPERATIONAL_FILES[$i]}"

  if [ -f "$OPERATIONAL_FILE" ]; then
    ROLLBACK_HASH=$(calculate_hash "$OPERATIONAL_FILE")
  else
    ROLLBACK_HASH="DELETED"  # File was new in this sync, deleted during rollback
  fi

  # Compare to pre-sync hash (from Phase 3 OPERATIONAL_HASHES array)
  if [ "$ROLLBACK_HASH" != "${OPERATIONAL_HASHES[$i]}" ]; then
    # CRITICAL ERROR: Rollback verification failed
    echo "CRITICAL ERROR: Rollback verification failed for $OPERATIONAL_FILE" >&2
    echo "  Pre-sync hash: ${OPERATIONAL_HASHES[$i]}" >&2
    echo "  Post-rollback hash: $ROLLBACK_HASH" >&2
    echo "  Backup file: ${BACKUPS_CREATED[$i]}" >&2
    echo "" >&2
    echo "Manual recovery required:" >&2
    echo "  1. Verify backup file integrity: md5sum ${BACKUPS_CREATED[$i]}" >&2
    echo "  2. Compare backup to expected content" >&2
    echo "  3. Manually restore correct version" >&2
    echo "  4. Report issue: This is a data integrity problem" >&2

    # Generate sync report with ROLLBACK_FAILED status
    generate_report "ROLLBACK_FAILED" 7

    exit 7  # Rollback failure (very serious - data integrity issue)
  fi
done

echo "✅ Rollback verification passed: All operational files restored to pre-sync state"
```
- If rollback verification fails:
  - Logs CRITICAL ERROR with pre-sync hash, post-rollback hash, backup file path
  - Provides manual recovery instructions (4 steps)
  - Generates sync report documenting rollback failure
  - Exits with status code 7 (rollback failure - most serious error, indicates data integrity issue)
  - Leaves system in partially rolled-back state (some files may be correct, others may be corrupted)
  - Retains all backup files (critical for manual recovery)

**Validation:** Simulate rollback verification failure by corrupting backup file before rollback (modify backup content), trigger rollback, verify verification detects hash mismatch, verify exits with status 7 and CRITICAL ERROR message; alternatively, simulate concurrent modification during rollback (have another process modify operational file while rollback in progress), verify detection.

**Why this matters:** Rollback verification ensures rollback actually succeeded. If rollback fails, system is in unknown state (could have mix of old and new content). Critical error prevents silent data corruption.

**Recovery:** Manual investigation required - check backup file integrity, compare to Git history, restore correct version from Git or backup, investigate root cause (disk corruption? concurrent access? permission issues?).

---

### 8. Dry-Run Mode Shows Incorrect Predictions

**Scenario:** User runs script with --dry-run flag to preview sync operations. Dry-run shows "Would sync: src/CLAUDE.md → CLAUDE.md (NO CONFLICT)", but when actual sync runs (without --dry-run), a conflict is detected because operational file was modified between dry-run and actual run.

**Expected Behavior:**
- Dry-run mode (triggered by --dry-run flag) is informational only:
```bash
if [ "$DRY_RUN" = "true" ]; then
  echo "DRY-RUN MODE: Showing sync plan without making changes"
  echo ""

  # Perform all checks (source exists, dirs writable, hashes)
  # Display what WOULD happen, but don't modify any files

  echo "Source files:"
  for file in "${SOURCE_FILES[@]}"; do
    echo "  - $file ($(get_file_size "$file") bytes)"
  done

  echo ""
  echo "Operational files:"
  for i in {0..2}; do
    if [ -f "${OPERATIONAL_FILES[$i]}" ]; then
      echo "  - ${OPERATIONAL_FILES[$i]} ($(get_file_size "${OPERATIONAL_FILES[$i]}") bytes)"
      if [ "${SOURCE_HASHES[$i]}" != "${OPERATIONAL_HASHES[$i]}" ]; then
        echo "    ⚠️ CONFLICT: File modified independently"
      else
        echo "    ✓ No conflict: File matches source"
      fi
    else
      echo "  - ${OPERATIONAL_FILES[$i]} (NEW - doesn't exist yet)"
    fi
  done

  echo ""
  echo "Sync plan:"
  for i in {0..2}; do
    echo "  Would sync: ${SOURCE_FILES[$i]} → ${OPERATIONAL_FILES[$i]}"
  done

  echo ""
  echo "DRY-RUN COMPLETE: No files modified"
  exit 0
fi
```
- Dry-run disclaimer logged: "⚠️ Note: Dry-run results based on current file state. Files may change before actual sync."
- Dry-run does NOT guarantee actual sync will succeed (files could change, permissions could change, disk could fill)
- Dry-run exit status always 0 (informational, not actual operation)
- Actual sync must re-check all conditions (not assume dry-run results are current)

**Validation:** Run --dry-run, note results, modify operational file, run actual sync, verify detects changes since dry-run (conflict that wasn't predicted).

**Why this matters:** Dry-run is point-in-time snapshot. Files can change between dry-run and actual execution. Users must understand dry-run is advisory, not guaranteed.

**Mitigation:** Dry-run output includes disclaimer, README.md documents dry-run limitations.

---

## Data Validation Rules

### 1. File Path Validation

**Rule:** All source and operational file paths must be valid, repository-relative, and point to regular files (not directories or special files).

**Validation Logic:**
```bash
validate_file_path() {
  local file=$1
  local file_type=$2  # "source" or "operational"

  # Check file exists
  if [ ! -f "$file" ]; then
    if [ "$file_type" = "source" ]; then
      echo "ERROR: Source file not found: $file"
      return 1
    else
      echo "INFO: Operational file doesn't exist yet: $file (will be created)"
      return 0  # Not an error for operational files
    fi
  fi

  # Check is regular file (not directory)
  if [ -d "$file" ]; then
    echo "ERROR: Invalid file path: $file. Expected regular file, found directory."
    return 1
  fi

  # Check is not special file (device, socket, pipe)
  if [ -c "$file" ] || [ -S "$file" ] || [ -p "$file" ]; then
    echo "ERROR: Invalid file path: $file. Expected regular file, found special file (device/socket/pipe)."
    return 1
  fi

  # Check is not symlink (symlinks handled separately in Edge Case 3)
  if [ -L "$file" ]; then
    echo "WARNING: File is symbolic link: $file (will prompt for confirmation)"
    return 0  # Not error, but flagged
  fi

  return 0  # Valid
}
```

**Error Message Format:**
- "ERROR: Source file not found: [path]. Run STORY-052-058 to create source files."
- "ERROR: Invalid file path: [path]. Expected regular file, found [type: directory/special/symlink]."
- "INFO: Operational file doesn't exist yet: [path] (will be created during sync)."

**Enforcement:**
- Script validates all source paths in Phase 1 (exits if any invalid)
- Script validates operational paths in Phase 2 (creates if missing, exits if special files)
- Path arrays (SOURCE_FILES, OPERATIONAL_FILES) are constants (no user-provided paths)

---

### 2. MD5 Hash Calculation Validation

**Rule:** MD5 hashes must be calculated consistently across source and operational files for reliable conflict detection.

**Calculation Command:**
```bash
# Linux
md5sum [file] | awk '{print $1}'  # Extract hash only, ignore filename

# macOS
md5 -q [file]  # -q flag: quiet mode, output hash only

# Platform-agnostic wrapper
calculate_hash() {
  local file=$1

  if [ "$(uname)" = "Darwin" ]; then
    md5 -q "$file"
  else
    md5sum "$file" | awk '{print $1}'
  fi
}
```

**Validation Requirements:**
- **Hash format:** 32-character hexadecimal string (e.g., `a1b2c3d4e5f6...`)
- **Hash uniqueness:** Different files produce different hashes (MD5 collision probability negligible for documents <1MB)
- **Repeatability:** Same file produces same hash on multiple calculations (deterministic)
- **Case insensitive:** Hash comparison uses lowercase (macOS md5 outputs lowercase, Linux md5sum outputs lowercase)

**Error Message Format:**
- "ERROR: MD5 hash calculation failed for [file]: [error]. Ensure md5sum utility available (Linux) or md5 command available (macOS)."
- "ERROR: Hash format invalid: '[hash]'. Expected 32-character hexadecimal string."

**Platform Compatibility:**
- Linux: Uses `md5sum` from coreutils package (pre-installed on most distros)
- macOS: Uses `md5` command (pre-installed, equivalent to md5sum)
- If neither available: Script exits with status 1 and error "MD5 utility not found. Install coreutils (Linux) or use macOS built-in md5."

**Validation Test:**
```bash
# Test hash calculation
test_hash=$(calculate_hash "src/CLAUDE.md")

# Verify format (32 hex chars)
if [[ ! "$test_hash" =~ ^[a-f0-9]{32}$ ]]; then
  echo "ERROR: Hash format invalid: $test_hash"
  exit 1
fi

# Verify repeatability (calculate twice, compare)
test_hash2=$(calculate_hash "src/CLAUDE.md")
if [ "$test_hash" != "$test_hash2" ]; then
  echo "ERROR: Hash calculation not deterministic (got different hashes for same file)"
  exit 1
fi
```

---

### 3. Backup Filename Format Validation

**Rule:** Backup filenames must include original filename, .bak suffix, and ISO 8601 timestamp for uniqueness and rollback traceability.

**Format:** `[original-filename].bak-YYYY-MM-DD-HH-MM-SS`

**Examples:**
- `CLAUDE.md.bak-2025-01-20-15-45-32` ✅
- `.claude/memory/commands-reference.md.bak-2025-01-20-15-45-33` ✅
- `skills-reference.md.bak-2025-01-20-15-45-34` ✅

**Invalid Examples:**
- `CLAUDE.bak` ❌ (no timestamp, no original extension)
- `CLAUDE.md.backup` ❌ (wrong suffix, no timestamp)
- `CLAUDE.md.bak.2025-01-20` ❌ (wrong timestamp format, missing time)

**Timestamp Generation:**
```bash
TIMESTAMP=$(date +%Y-%m-%d-%H-%M-%S)
# Example: 2025-01-20-15-45-32 (24-hour format, zero-padded)
```

**Validation Requirements:**
- Timestamp uses ISO 8601 format (YYYY-MM-DD-HH-MM-SS)
- No duplicate backups for same file in same sync operation (single timestamp used for all backups in one sync)
- Old backups from previous syncs are NOT automatically deleted (manual cleanup required)
- Backup is regular file (not directory, not symlink): `test -f [backup-path]`

**Error Message Format:**
- "ERROR: Backup creation failed for [file]: [error]. Check disk space (df -h) and write permissions (ls -la)."
- "WARNING: Old backup exists: [file].bak-[old-timestamp]. Will create new backup (old backup preserved)."

**Cleanup Strategy:**
- Script does NOT auto-delete old backups (prevents accidental data loss)
- README.md documents manual cleanup: `find . -name "*.bak-*" -mtime +30 -delete` (delete backups older than 30 days)
- Sync report lists all backups created (user can review and delete if confident sync succeeded)

---

### 4. Sync Report Format Validation

**Rule:** Sync reports must be plain text, human-readable, and include all 10 required sections (AC7) for compliance and audit trail.

**Required Sections (10 total):**
1. **Header:** "DevForgeAI Operational Sync Report - User Input Guidance System"
2. **Execution Timestamp:** Start/complete/duration
3. **Source Files:** 3 paths with sizes
4. **Operational Files:** 3 paths with sizes or "NEW"
5. **Pre-Sync State:** Source/operational hashes, conflict count
6. **Conflict Detection Results:** Conflicts detected, actions taken
7. **Synchronization Results:** Per-file status (SUCCESS/FAILED/SKIPPED)
8. **Post-Sync Validation:** Hash/size comparisons, validation pass/fail
9. **Backup Information:** Backup files created with paths/timestamps/sizes
10. **Exit Status:** Numeric code and meaning

**Report Format Example:**
```
##########################################################################
# DevForgeAI Operational Sync Report - User Input Guidance System
##########################################################################

Execution Timestamp:
  Started: 2025-01-20 15:45:30
  Completed: 2025-01-20 15:45:35
  Duration: 5 seconds

Source Files:
  - src/CLAUDE.md (52,341 bytes)
  - src/claude/memory/commands-reference.md (28,942 bytes)
  - src/claude/memory/skills-reference.md (31,058 bytes)

Operational Files (Pre-Sync):
  - CLAUDE.md (50,123 bytes)
  - .claude/memory/commands-reference.md (28,942 bytes)
  - .claude/memory/skills-reference.md (NEW - doesn't exist)

Pre-Sync State:
  Source Hashes:
    - src/CLAUDE.md: a1b2c3d4...
    - src/claude/memory/commands-reference.md: e5f6g7h8...
    - src/claude/memory/skills-reference.md: i9j0k1l2...
  Operational Hashes:
    - CLAUDE.md: x9y8z7w6... (CONFLICT: different from source)
    - .claude/memory/commands-reference.md: e5f6g7h8... (MATCH: same as source)
    - .claude/memory/skills-reference.md: NEW_FILE
  Conflicts: 1 (CLAUDE.md)

Conflict Detection Results:
  Conflicts detected: 1
  Details:
    - CLAUDE.md: Source hash a1b2c3d4... vs Operational hash x9y8z7w6...
  Action taken: User selected 'Overwrite operational' (option 1)

Synchronization Results:
  - src/CLAUDE.md → CLAUDE.md: SUCCESS
  - src/claude/memory/commands-reference.md → .claude/memory/commands-reference.md: SUCCESS (no conflict, skipped backup)
  - src/claude/memory/skills-reference.md → .claude/memory/skills-reference.md: SUCCESS (new file)

Post-Sync Validation:
  Hash Comparisons:
    - CLAUDE.md: a1b2c3d4... (source) = a1b2c3d4... (operational post-sync) ✅ MATCH
    - .claude/memory/commands-reference.md: e5f6g7h8... = e5f6g7h8... ✅ MATCH
    - .claude/memory/skills-reference.md: i9j0k1l2... = i9j0k1l2... ✅ MATCH
  Size Comparisons:
    - CLAUDE.md: 52,341 bytes (source) = 52,341 bytes (operational) ✅ MATCH
    - commands-reference.md: 28,942 = 28,942 ✅ MATCH
    - skills-reference.md: 31,058 = 31,058 ✅ MATCH
  Validation: ✅ PASSED (all hashes and sizes match)

Backup Information:
  Backups created: 1
    - CLAUDE.md.bak-2025-01-20-15-45-30 (50,123 bytes, hash: x9y8z7w6...)

Exit Status: 0 (Success: All files synchronized and validated)

##########################################################################
```

**Validation Logic:**
```bash
validate_sync_report() {
  local report_file=$1

  # Check file exists
  if [ ! -f "$report_file" ]; then
    echo "ERROR: Sync report not found: $report_file"
    return 1
  fi

  # Check contains all 10 required section headers
  required_sections=(
    "DevForgeAI Operational Sync Report"
    "Execution Timestamp:"
    "Source Files:"
    "Operational Files"
    "Pre-Sync State:"
    "Conflict Detection Results:"
    "Synchronization Results:"
    "Post-Sync Validation:"
    "Backup Information:"
    "Exit Status:"
  )

  for section in "${required_sections[@]}"; do
    if ! grep -q "$section" "$report_file"; then
      echo "ERROR: Sync report missing section: '$section'"
      return 1
    fi
  done

  echo "✓ Sync report structure valid (all 10 sections present)"
  return 0
}
```

**Error Message Format:**
- "Sync report incomplete: missing section [section name]. Report may be corrupted."
- "Sync report format invalid: expected plain text, found [binary/encoded/etc.]."

---

### 5. Exit Status Code Validation

**Rule:** The sync script must exit with standardized status codes for different failure types to enable automated error handling in CI/CD pipelines.

**Exit Codes (8 total):**
- **0 = Success:** All files synchronized successfully, post-sync validation passed
- **1 = Missing Source Files:** One or more source files don't exist (STORY-052-058 incomplete)
- **2 = Permission Denied:** Cannot create operational directories or no write permission
- **3 = Sync Failed with Rollback:** Copy operation failed, rollback completed successfully, operational files restored
- **4 = Post-Sync Validation Failed:** Files copied but hash/size mismatch detected (corruption)
- **5 = Manual Merge Required:** Conflicts detected, user chose manual merge (or didn't choose at all)
- **6 = Insufficient Disk Space:** Not enough space for backups, sync aborted before modifications
- **130 = Interrupted:** SIGINT or SIGTERM received, cleanup completed, operational files restored

**Exit Code Documentation:**
```bash
# At top of script (after shebang and header comment)

# Exit codes (for automated error handling)
EXIT_SUCCESS=0
EXIT_MISSING_SOURCE=1
EXIT_PERMISSION_DENIED=2
EXIT_SYNC_FAILED=3
EXIT_VALIDATION_FAILED=4
EXIT_MANUAL_MERGE=5
EXIT_DISK_SPACE=6
EXIT_INTERRUPTED=130
```

**Validation Requirements:**
- Script calls `exit [code]` at all termination points (no implicit exits)
- Exit code is in documented range (0-6, 130, not random values)
- Each exit point logs reason before exiting: "Exiting with status [code]: [reason]"
- Exit codes are used consistently (same failure type always uses same code)

**Error Message Format:**
- "Script exited with unexpected status code: [code]. Expected: 0-6 or 130. Check script for exit [code] calls."

**CI/CD Integration:**
```bash
# Example CI/CD usage
bash tests/user-input-guidance/validate-sync.sh

case $? in
  0)
    echo "✅ Sync succeeded"
    ;;
  1)
    echo "❌ Missing source files - run STORY-052-058 first"
    exit 1
    ;;
  2)
    echo "❌ Permission denied - check file system permissions"
    exit 1
    ;;
  3)
    echo "⚠️ Sync failed but rolled back - operational files unchanged"
    exit 1
    ;;
  4)
    echo "❌ Post-sync validation failed - file corruption detected"
    exit 1
    ;;
  5)
    echo "ℹ️ Manual merge required - resolve conflicts and re-run"
    exit 0  # Not fatal in CI/CD, just needs manual step
    ;;
  6)
    echo "❌ Insufficient disk space - free up space and retry"
    exit 1
    ;;
  130)
    echo "⚠️ Sync interrupted by user - operational files restored"
    exit 130
    ;;
  *)
    echo "❌ Unknown exit code: $?"
    exit 1
    ;;
esac
```

---

### 6. File Size Comparison Validation

**Rule:** Post-sync validation (AC6) must include file size comparison in addition to hash comparison to detect truncation or corruption that might (extremely rarely) result in hash collision.

**Validation Logic:**
```bash
# Linux
SOURCE_SIZE=$(stat -c%s "$SOURCE_FILE")
OPERATIONAL_SIZE=$(stat -c%s "$OPERATIONAL_FILE")

# macOS
SOURCE_SIZE=$(stat -f%z "$SOURCE_FILE")
OPERATIONAL_SIZE=$(stat -f%z "$OPERATIONAL_FILE")

# Comparison (must match exactly, 0-byte tolerance)
if [ $SOURCE_SIZE -ne $OPERATIONAL_SIZE ]; then
  echo "ERROR: Post-sync file size mismatch: $OPERATIONAL_FILE"
  echo "  Source size: $SOURCE_SIZE bytes"
  echo "  Operational size: $OPERATIONAL_SIZE bytes"
  echo "  Difference: $((OPERATIONAL_SIZE - SOURCE_SIZE)) bytes"
  echo "  Issue: Sync incomplete or file corrupted during copy"
  exit 4  # Post-sync validation failed
fi
```

**Validation Requirements:**
- Size must match exactly (0-byte difference)
- Size checked in addition to hash (not instead of hash)
- Both hash AND size must match for validation to pass
- Size mismatch triggers same exit code as hash mismatch (status 4)

**Error Message Format:**
- "Post-sync file size mismatch: [operational-file] size [N] bytes does not match [source-file] size [M] bytes. Difference: [N-M] bytes. Sync incomplete or corrupted."

**Why both hash AND size:**
- Hash detects any content difference (even 1-bit change)
- Size detects truncation or file growth
- Together: 99.9999% detection of any data integrity issue
- Size check is fast (<10ms), adds minimal overhead

---

### 7. Diff Output Format Validation

**Rule:** When displaying diffs for conflict resolution (Edge Case 1, user selects "Show diff"), the diff output must use unified format (-u flag) with context lines for readability.

**Diff Command:**
```bash
diff -u [source-file] [operational-file]
```

**Output Format:**
- **Header lines:** `--- [source-file]` and `+++ [operational-file]`
- **Context:** 3 lines before and after changes (unified format default)
- **Changes:** Lines prefixed with `-` (removed from source, present in operational) or `+` (added in source, absent in operational)
- **Unchanged context:** Lines prefixed with space (for orientation)

**Example Output:**
```
--- src/CLAUDE.md	2025-01-20 15:00:00
+++ CLAUDE.md	2025-01-20 14:00:00
@@ -377,6 +377,10 @@
 ## Quick Reference - Progressive Disclosure

 **For detailed guidance, load reference files as needed using the Read tool:**
+
+## Learning DevForgeAI
+
+[New section from STORY-058 - source file]

 ```
 Read(file_path=".claude/memory/skills-reference.md")
@@ -800,6 +804,8 @@

 **References:**
 - Framework documentation: `ROADMAP.md`, `README.md`
+
+Custom developer notes (added manually to operational file)
```

**Diff Execution:**
```bash
show_diff() {
  local source=$1
  local operational=$2

  echo "Showing diff: $source vs $operational"
  echo ""

  # Generate diff
  diff -u "$source" "$operational"
  local diff_exit=$?

  # Handle diff exit codes
  case $diff_exit in
    0)
      echo ""
      echo "Files are identical (no differences)"
      ;;
    1)
      echo ""
      echo "Differences shown above"
      ;;
    2)
      echo ""
      echo "ERROR: Diff generation failed (file missing or unreadable)"
      ;;
  esac
}
```

**Validation Requirements:**
- diff command uses -u flag (unified format, most readable)
- diff output is not paginated (no `| less` in script, user can pipe if desired)
- diff exit status handled (0 = no differences, 1 = differences found, 2 = error)

**Error Message Format:**
- "Diff generation failed for [source] vs [operational]: [error]. Cannot display conflict details."

---

### 8. Rollback Integrity Validation

**Rule:** After rollback (AC8), operational files must be in their exact pre-sync state, verified by comparing post-rollback hashes against pre-sync hashes stored in Phase 3.

**Pre-Sync Hash Storage:**
```bash
# Phase 3: Conflict Detection
# Store pre-sync hashes in array for later comparison
PRE_SYNC_HASHES=()
for file in "${OPERATIONAL_FILES[@]}"; do
  if [ -f "$file" ]; then
    PRE_SYNC_HASHES+=($(calculate_hash "$file"))
  else
    PRE_SYNC_HASHES+=("NEW_FILE")
  fi
done
```

**Post-Rollback Verification:**
```bash
# After rollback restores all backups
# Recalculate operational file hashes
POST_ROLLBACK_HASHES=()
for file in "${OPERATIONAL_FILES[@]}"; do
  if [ -f "$file" ]; then
    POST_ROLLBACK_HASHES+=($(calculate_hash "$file"))
  else
    POST_ROLLBACK_HASHES+=("DELETED")  # File was new, deleted during rollback
  fi
done

# Compare post-rollback to pre-sync
ROLLBACK_FAILURES=()
for i in {0..2}; do
  if [ "${POST_ROLLBACK_HASHES[$i]}" != "${PRE_SYNC_HASHES[$i]}" ]; then
    ROLLBACK_FAILURES+=("${OPERATIONAL_FILES[$i]}")
  fi
done

# Validation
if [ ${#ROLLBACK_FAILURES[@]} -eq 0 ]; then
  echo "✅ Rollback verification passed: All operational files restored to pre-sync state"
  return 0
else
  echo "ERROR: Rollback incomplete for ${#ROLLBACK_FAILURES[@]} files" >&2
  for file in "${ROLLBACK_FAILURES[@]}"; do
    echo "  - $file: Hash mismatch (pre-sync ≠ post-rollback)" >&2
  done
  exit 7  # Rollback failure
fi
```

**Error Message Format:**
- "Rollback failed: [file] hash [post-rollback-hash] does not match pre-sync hash [pre-sync-hash]. Manual recovery required."
- "Rollback verification incomplete: [N] files failed verification. Files: [list]."

**Manual Recovery Guidance (if exit 7):**
1. Check backup file integrity: `md5sum [backup-file]`
2. Compare backup content to Git version: `git diff [backup-file] [git-version]`
3. Determine correct version (backup or Git)
4. Manually restore: `cp [correct-version] [operational-file]`
5. Verify restoration: `md5sum [operational-file]`, compare to known-good hash
6. Report issue: File bug report with rollback failure details (this should never happen)

---

## Non-Functional Requirements

### Performance

**Sync Execution Time Breakdown:**
- **Phase 1 (Discovery):** ~0.5 seconds (3 × test -f checks, array population)
- **Phase 2 (Directory Validation):** ~0.3 seconds (2 × test -d, potential 1 × mkdir -p)
- **Phase 3 (Conflict Detection):** ~1.5 seconds (6 × md5sum calculations, hash comparisons)
- **Phase 4 (File Sync):** ~2 seconds (3 × cp operations, each ~0.5-1s for 50KB files)
- **Phase 5 (Post-Sync Validation):** ~1.5 seconds (3 × md5sum, 3 × stat, comparisons)
- **Phase 6 (Backup Creation):** ~1 second (if conflicts: 1-3 × cp for backups)
- **Phase 7 (Report Generation):** ~0.5 seconds (file writing, log append)
- **Total:** ~7-8 seconds for full workflow (well under 10s target)

**Hardware Assumptions:**
- Standard laptop/desktop (4-core CPU, 8GB RAM)
- SSD storage (not HDD - HDD would add ~2-3s to file I/O)
- Modern Linux kernel or macOS 10.15+ (recent system utilities)
- Bash 4.0+ (for array support, modern Bash features)

**Performance Optimization Opportunities:**
- Parallel hash calculation (md5sum in background for multiple files): Could reduce Phase 3/5 from 1.5s to ~0.5s
- Not implemented: Adds complexity, 1.5s is acceptable for 3 files

---

### Reliability

**Atomicity Guarantee:**
- **Implementation:** Rollback on any failure ensures all-or-nothing behavior
- **Mechanism:** Backups created before modifications, restored on any error
- **Verification:** Post-rollback hash check confirms restoration
- **Edge cases covered:** Copy failures, validation failures, interruptions (SIGINT/SIGTERM), disk full, permission errors
- **Testing:** 100 test runs with random failure injection, verify 0 partial states

**Error Handling Comprehensiveness:**
1. **Missing source files:** Early exit with status 1, clear error (Phase 1)
2. **Permission denied:** Directory creation or write check fails, status 2 (Phase 2)
3. **Conflict detection:** User choice required or --force provided (Phase 3)
4. **Copy failure:** Rollback triggered, status 3 (Phase 4)
5. **Validation failure:** Hash or size mismatch, status 4 (Phase 5)
6. **Disk space:** Pre-flight check prevents backup creation, status 6 (Phase 6)
7. **Interruption:** Trap handlers catch signals, cleanup, status 130 (Any phase)
8. **Rollback failure:** Hash verification fails after restore, status 7 (Rollback phase)

**Graceful Degradation:**
- If md5sum unavailable on Linux: Try md5 (macOS command), if neither available: Exit with error "No MD5 utility found"
- If stat unavailable: Use ls -l and awk to parse size (fallback)
- If diff unavailable: Show conflict warning but can't display details, user must inspect files manually
- All fallbacks logged: "WARNING: [primary-tool] not found, using fallback [fallback-tool]"

---

### Maintainability

**Script Structure:**
```bash
#!/bin/bash

###############################################################################
# DevForgeAI Operational Sync Script
# Purpose: Synchronize source files (src/) to operational directories (.claude/)
# Usage: bash tests/user-input-guidance/validate-sync.sh [--dry-run] [--force] [--help]
###############################################################################

# Configuration (Lines 10-30)
SOURCE_FILES=(...)
OPERATIONAL_FILES=(...)
EXIT_SUCCESS=0
EXIT_MISSING_SOURCE=1
...

# Utility Functions (Lines 40-150)
calculate_hash() { ... }
get_file_size() { ... }
create_backup() { ... }
restore_backup() { ... }
validate_post_sync() { ... }
generate_report() { ... }
cleanup_and_exit() { ... }
show_diff() { ... }

# Signal Handlers (Lines 160-170)
trap 'cleanup_and_exit 130' INT TERM

# Main Workflow (Lines 180-400)
# Phase 1: Source File Discovery
# Phase 2: Operational Directory Validation
# Phase 3: Conflict Detection
# Phase 4: File Synchronization
# Phase 5: Post-Sync Validation
# Phase 6: Rollback (if errors)
# Phase 7: Report Generation
```

**Configuration Centralization:**
- All file paths in arrays at top (easy to add new sync pairs)
- All exit codes as named constants (easy to understand, searchable)
- All thresholds configurable (disk space buffer: 1.1x, context lines in diff: 3)

**Function Modularity:**
- Each function has single responsibility (calculate hash, create backup, etc.)
- Functions are reusable (called from multiple phases)
- Functions have clear inputs/outputs (documented in comments)
- Functions handle their own errors (return status codes, log messages)

**Version Control:**
- Sync reports use timestamps (no merge conflicts in Git)
- Reports are plain text (easy to diff in Git)
- Reports NOT committed to repo (.gitignore: `reports/*.txt`)
- Only script and fixtures committed (source, not outputs)

---

## Acceptance Criteria Verification Checklist

### AC#1: Sync Script Created

- [ ] Script file exists - **Phase:** 2 - **Evidence:** test -f tests/user-input-guidance/validate-sync.sh
- [ ] Executable permissions - **Phase:** 2 - **Evidence:** test -x validate-sync.sh, stat -c%a verify 755
- [ ] Shebang present - **Phase:** 2 - **Evidence:** head -1 validate-sync.sh | grep "^#!/bin/bash$"
- [ ] Header comment - **Phase:** 2 - **Evidence:** head -10 | grep "Purpose\|Usage\|Dependencies\|Exit codes"
- [ ] Invocable from root - **Phase:** 3 - **Evidence:** bash tests/user-input-guidance/validate-sync.sh (executes successfully)
- [ ] --dry-run flag - **Phase:** 3 - **Evidence:** bash validate-sync.sh --dry-run (shows plan, no changes)
- [ ] --force flag - **Phase:** 3 - **Evidence:** Create conflict, run with --force, verify skips menu
- [ ] --help flag - **Phase:** 3 - **Evidence:** bash validate-sync.sh --help (displays documentation)

### AC#2: Source File Discovery

- [ ] Identifies 3 source files - **Phase:** 2 - **Evidence:** Script defines SOURCE_FILES array with 3 elements
- [ ] Verifies existence - **Phase:** 3 - **Evidence:** test -f check for each, logs if missing
- [ ] Exits if missing - **Phase:** 3 - **Evidence:** Delete src/CLAUDE.md, run script, verify exit status 1
- [ ] Logs discovery - **Phase:** 3 - **Evidence:** Run script, verify logs "Found 3 source files"

### AC#3: Operational Directory Validation

- [ ] Checks .claude/ - **Phase:** 3 - **Evidence:** test -d .claude in script
- [ ] Checks .claude/memory/ - **Phase:** 3 - **Evidence:** test -d .claude/memory in script
- [ ] Creates if missing - **Phase:** 3 - **Evidence:** Delete dirs, run script, verify created via mkdir -p
- [ ] Verifies write permissions - **Phase:** 3 - **Evidence:** test -w check in script
- [ ] Exits if no write permission - **Phase:** 3 - **Evidence:** chmod 555 .claude, run script, verify exit status 2

### AC#4: Conflict Detection

- [ ] Calculates source hashes - **Phase:** 3 - **Evidence:** md5sum or md5 for all 3 source files
- [ ] Calculates operational hashes - **Phase:** 3 - **Evidence:** md5sum or md5 for existing operational files
- [ ] Detects conflicts - **Phase:** 3 - **Evidence:** Modify operational file, verify hash mismatch detected
- [ ] Logs conflict details - **Phase:** 3 - **Evidence:** Verify logs show source hash vs operational hash
- [ ] Presents menu - **Phase:** 3 - **Evidence:** Verify interactive menu with 4 options
- [ ] Handles --force - **Phase:** 3 - **Evidence:** With --force, skip menu, proceed to sync

### AC#5: File Synchronization

- [ ] Copies with cp -f - **Phase:** 3 - **Evidence:** Grep script for "cp -f" commands
- [ ] Verifies exit status - **Phase:** 3 - **Evidence:** Grep for "if [ $? -ne 0 ]" checks after cp
- [ ] Rolls back on failure - **Phase:** 3 - **Evidence:** Simulate copy failure, verify rollback triggered
- [ ] Logs success - **Phase:** 3 - **Evidence:** Successful sync logs "Successfully synchronized 3 files"

### AC#6: Post-Sync Validation

- [ ] Recalculates hashes - **Phase:** 3 - **Evidence:** md5sum called post-sync
- [ ] Compares to source - **Phase:** 3 - **Evidence:** Hash comparison logic in script
- [ ] Logs if match - **Phase:** 3 - **Evidence:** Verify logs "Post-sync validation passed"
- [ ] Exits if mismatch - **Phase:** 3 - **Evidence:** Corrupt file post-sync, verify exit status 4
- [ ] Verifies file sizes - **Phase:** 3 - **Evidence:** stat command in validation phase

### AC#7: Sync Report Generation

- [ ] Timestamped filename - **Phase:** 3 - **Evidence:** Report matches sync-report-YYYY-MM-DD-HH-MM-SS.txt
- [ ] 10 sections present - **Phase:** 3 - **Evidence:** Grep for all 10 section headers
- [ ] Human-readable text - **Phase:** 3 - **Evidence:** file command shows ASCII text, not binary
- [ ] Appended to history log - **Phase:** 3 - **Evidence:** Verify sync-history.log grows after each sync

### AC#8: Rollback Capability

- [ ] Creates backups - **Phase:** 3 - **Evidence:** Verify backup files created before sync
- [ ] Backup filename format - **Phase:** 3 - **Evidence:** Matches [file].bak-YYYY-MM-DD-HH-MM-SS
- [ ] Restores on failure - **Phase:** 3 - **Evidence:** Trigger failure, verify restoration
- [ ] Logs rollback actions - **Phase:** 3 - **Evidence:** Verify logs "Rollback initiated. Restoring..."
- [ ] Verifies restoration - **Phase:** 3 - **Evidence:** Post-rollback hash = pre-sync hash
- [ ] Retains backups - **Phase:** 3 - **Evidence:** After rollback, verify backup files still exist
- [ ] Exits with status 3 - **Phase:** 3 - **Evidence:** Rollback scenario, verify exit code

---

**Checklist Progress:** 0/54 items complete (0%)

---


## Implementation Notes

Status: Backlog - Story created and ready for development. All Definition of Done items will be completed during TDD cycle.
## Definition of Done

### Implementation
- [ ] validate-sync.sh script created at tests/user-input-guidance/ (400-500 lines, comprehensive)
- [ ] All 3 source→operational sync pairs implemented (src/CLAUDE.md, commands-reference.md, skills-reference.md)
- [ ] Conflict detection via MD5 hashing (source vs operational comparison, interactive menu)
- [ ] Backup/rollback capability (creates .bak-[timestamp] files, restores on failure)
- [ ] Post-sync validation (hash and size comparison, detects corruption)
- [ ] Sync report generation (timestamped reports, 10 required sections, cumulative log)
- [ ] Signal handling (trap handlers for SIGINT/SIGTERM, graceful cleanup)
- [ ] Platform compatibility (macOS and Linux support via uname detection)
- [ ] Command-line flags (--dry-run, --force, --help)
- [ ] Modular functions (≥5 reusable functions, clear responsibilities)

### Quality
- [ ] All 8 acceptance criteria validated with passing tests
- [ ] All 8 edge cases documented with detailed expected behavior, validation procedures, recovery steps
- [ ] All 8 data validation rules enforced with validation logic, error messages, enforcement mechanisms
- [ ] All 20 NFRs met with measured validation (performance, reliability, maintainability, quality, testability, usability, security)
- [ ] No ambiguous requirements (all specifications measurable, testable, explicit)
- [ ] No placeholder content (all logic implemented, all sections complete)

### Testing
- [ ] Self-test mode (--test flag) functional with mock files and cleanup
- [ ] All 8 failure scenarios tested (missing source, permission, sync failed, validation failed, manual merge, disk space, interrupted, rollback failed)
- [ ] Platform compatibility tested (Linux and macOS)
- [ ] 100 random failure injection tests (verify atomicity and zero data loss)
- [ ] All test cases passing (unit, integration, regression)

### Documentation
- [ ] Inline code comments (key functions and complex logic documented)
- [ ] --help output comprehensive (purpose, usage, flags, exit codes, examples)
- [ ] README.md section added (if test suite README.md doesn't cover sync script, add dedicated section)
- [ ] Exit codes documented (in script header and --help output)
- [ ] Manual recovery procedures documented (for exit code 7 rollback failure)

---

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

---

## Workflow History

### 2025-01-20 20:45:00 - Status: Ready for Dev
- Added to SPRINT-2: User Input Guidance Implementation
- Transitioned from Backlog to Ready for Dev
- Sprint capacity: 40 points (9 stories)
- Priority in sprint: [9 of 9] - Operational sync (final step before deployment)

---

## Notes

**Design Decisions:**

**Atomicity Over Speed:**
- Rollback capability ensures all-or-nothing sync (no partial states)
- Backup creation before every modification (zero data loss guarantee)
- Post-sync validation catches corruption (hash + size checks)
- Trade-off: ~2s overhead for backups/validation, but guarantees data integrity

**Interactive Conflict Resolution:**
- User choice for conflicts (overwrite, merge, diff, cancel)
- No silent overwrites (explicit confirmation required)
- --force flag for automation (skips interactive menu)
- Diffs displayed for informed decisions (unified format, context lines)

**Platform Compatibility:**
- macOS and Linux support via uname detection
- Platform-specific commands abstracted in functions (calculate_hash, get_file_size)
- Same behavior on both platforms (consistent exit codes, output format)

**Modular Architecture:**
- 5+ reusable functions (calculate_hash, create_backup, restore_backup, validate_post_sync, generate_report)
- Clear separation of phases (7 phases, each documented)
- Configuration at top (SOURCE_FILES, OPERATIONAL_FILES arrays)
- Trap handlers for graceful cleanup (SIGINT/SIGTERM)

**Value Proposition:**
- **Automation:** One command syncs all 3 files (no manual copying)
- **Safety:** Backups prevent data loss, rollback on failures
- **Transparency:** Detailed reports, clear logs, comprehensive --help
- **Reliability:** Atomic operations, post-sync validation, signal handling
- **Developer-friendly:** Dry-run mode, interactive menus, clear errors

**Success Criteria from STORY-060:**
- **Atomicity:** 100% (all files synced or none)
- **Zero data loss:** 100% (backups always created, rollback always succeeds)
- **Performance:** <10 seconds for full sync (target met with ~7-8s actual)
- **Reliability:** 100% detection of file corruption (hash + size checks)

**Implementation Complexity:**
- **2 story points justified:** Simple concept (copy files) but comprehensive implementation (atomicity, rollback, validation, platform compat, error handling)
- **Estimated effort:** 3-4 hours (2 hours implementation, 1-2 hours testing all edge cases)

**Related ADRs:**
None required (operational tooling, not architectural change)

**References:**
- **EPIC-011:** User Input Guidance System (parent epic)
- **STORY-052-059:** All source files (must exist before sync)
- **STORY-058:** Sync checklist (documents what needs syncing)
- **DevForgeAI installer pattern:** Follows same src/ → operational sync strategy used by installer

---

## Superseded Notice

**Status:** SUPERSEDED by STORY-065 (2025-11-24)

**Reason:**
- STORY-060 is overly verbose (1,914 lines, 92 KB)
- Contains 33 bash code blocks in Acceptance Criteria section (implementation detail, not requirements)
- Violates AC/Tech Spec separation principle (AC = what, Tech Spec = how)

**Replacement:**
- **STORY-065:** Operational Sync for User Input Guidance System (Lightweight)
- File: `devforgeai/specs/Stories/STORY-065-operational-sync-lightweight.story.md`
- Size: 379 lines, 19.6 KB (80% reduction)
- Identical functionality, proper AC/Tech Spec separation
- Zero bash code in AC section (all moved to Technical Specification)

**Disposition Options:**
1. **Archive STORY-060** - Keep for reference (demonstrates verbose anti-pattern)
2. **Delete STORY-060** - Remove and use only STORY-065
3. **Implement STORY-065** - Use lightweight version for actual development

**Recommendation:** Archive STORY-060 as educational reference showing "what not to do" in AC sections. Implement STORY-065 for actual operational sync functionality.

---

**Story Template Version:** 2.0
**Created:** 2025-01-20
**Superseded:** 2025-11-24 by STORY-065
