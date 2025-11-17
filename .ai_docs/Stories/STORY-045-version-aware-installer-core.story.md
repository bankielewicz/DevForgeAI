---
id: STORY-045
title: Version-Aware Installer with Backup and Rollback Capability
epic: EPIC-009
sprint: Backlog
status: Backlog
points: 13
priority: High
assigned_to: TBD
created: 2025-11-16
format_version: "2.0"
depends_on: STORY-042
---

# Story: Version-Aware Installer with Backup and Rollback Capability

## Description

**As a** DevForgeAI user installing the framework in my project,
**I want** a version-aware installer that detects existing installations, compares versions, creates automatic backups, deploys framework files safely, and provides rollback capability,
**so that** I can confidently install or upgrade DevForgeAI without risking data loss or breaking my project.

## Acceptance Criteria

### 1. [ ] Installer Detects Existing Installations and Compares Versions

**Given** a target project directory that may or may not have DevForgeAI installed
**When** I run `python installer/install.py --target=/path/to/project`
**Then** the installer:
- Checks for `.devforgeai/.version.json` (existing installation marker)
- If found: Reads installed version (e.g., "1.0.0")
- Reads source version from `src/devforgeai/version.json` (e.g., "1.0.1")
- Compares using semantic versioning (major.minor.patch)
- Determines installation mode:
  - `fresh_install`: No .version.json found
  - `patch_upgrade`: 1.0.0 → 1.0.1 (bug fixes only)
  - `minor_upgrade`: 1.0.0 → 1.1.0 (new features, backward compatible)
  - `major_upgrade`: 1.0.0 → 2.0.0 (breaking changes, requires migration)
  - `reinstall`: Same version (repair installation)
  - `downgrade`: Source older than installed (warn user, require --force flag)
**And** installer displays: "Detected: {installed_version} → {source_version} ({mode})"
**And** prompts user for confirmation before proceeding

---

### 2. [ ] Automatic Backup Created Before Any File Modifications

**Given** an existing DevForgeAI installation (version 1.0.0) will be upgraded
**When** the installer proceeds with upgrade mode
**Then** before any files are modified:
- Creates timestamped backup directory: `.backups/devforgeai-upgrade-{YYYYMMDD-HHMMSS}/`
- Copies all existing .claude/ files to backup (preserves structure)
- Copies all existing .devforgeai/ files to backup (preserves structure)
- Copies CLAUDE.md to backup (if contains DevForgeAI sections)
- Generates backup manifest: `manifest.json` with:
  ```json
  {
    "created_at": "2025-11-17T14:30:00Z",
    "reason": "upgrade",
    "from_version": "1.0.0",
    "to_version": "1.0.1",
    "files_backed_up": 450,
    "total_size_mb": 15.2,
    "backup_integrity_hash": "sha256..."
  }
  ```
**And** verifies backup integrity (file count matches, manifest hash validates)
**And** displays: "✅ Backup created: .backups/devforgeai-upgrade-20251117-143000/ (450 files, 15.2 MB)"

---

### 3. [ ] Framework Files Deployed from src/ to Target Project Locations

**Given** the installer has valid backup and user confirmed upgrade
**When** deployment phase executes
**Then** framework files are copied with exclusions:

**Deployment operations:**
- Deploy `src/claude/` → `{target}/.claude/` (all subdirectories: agents, commands, memory, scripts, skills)
- Deploy `src/devforgeai/` → `{target}/.devforgeai/` (config, docs, protocols, tests only)
- Exclude patterns applied:
  - `*.backup*`, `*.tmp`, `__pycache__/`, `*.pyc` (artifacts)
  - `qa/reports/`, `RCA/`, `adrs/`, `feedback/imported/`, `logs/` (generated content)
- Set file permissions: directories 755, .sh files 755, .md files 644, .py files 644
- Count deployed files: ~370 from src/claude/, ~80 from src/devforgeai/ = ~450 total

**And** deployment report shows:
  - Files deployed: 450
  - Directories created: 25
  - Permissions set: 450 files
  - Exclusions applied: 60 files excluded
  - Deployment time: <2 minutes
**And** displays: "✅ Deployed 450 framework files to {target}"

---

### 4. [ ] User Configurations Preserved During Upgrade

**Given** the target project has customized `.devforgeai/config/hooks.yaml` and `.devforgeai/feedback/config.yaml`
**When** installer deploys to existing installation
**Then** user configuration files are explicitly preserved:
- `.devforgeai/config/hooks.yaml`: NOT overwritten (user customizations kept)
- `.devforgeai/feedback/config.yaml`: NOT overwritten (user settings kept)
- `.devforgeai/context/*.md`: NOT overwritten (user-created context files)
- `.ai_docs/`: NOT touched (user stories/epics/sprints)
**And** for each preserved file, installer displays: "⏩ Preserved: .devforgeai/config/hooks.yaml (user config)"
**And** if config templates updated in source, installer shows: "ℹ️  New config template available: config/hooks.yaml.example (review for new features)"

---

### 5. [ ] Installation Modes Support Fresh Install, Upgrade, Rollback, Validate, Uninstall

**Given** the installer supports 5 operational modes
**When** I test each mode
**Then** all modes execute correctly:

**Mode 1: Fresh Install** (`--mode=fresh` or no existing installation)
- Deploys all ~450 files to empty project
- Creates initial config files from examples
- Installs CLI: `pip install -e .claude/scripts/`
- Writes version.json with installation timestamp
- Exit code: 0, displays "✅ DevForgeAI 1.0.1 installed successfully"

**Mode 2: Upgrade** (`--mode=upgrade` or detected via version comparison)
- Creates automatic backup
- Selectively updates changed files only (for patch/minor upgrades)
- Full deployment for major upgrades
- Preserves user configs
- Updates version.json
- Exit code: 0, displays "✅ Upgraded from 1.0.0 to 1.0.1 (50 files updated)"

**Mode 3: Rollback** (`--mode=rollback`)
- Lists available backups (sorted by timestamp)
- User selects backup or uses most recent
- Verifies backup integrity (manifest hash, file count)
- Restores all files from backup
- Reverts version.json to backup version
- Exit code: 0, displays "✅ Rolled back to version 1.0.0 from backup {timestamp}"

**Mode 4: Validate** (`--mode=validate`)
- Checks directory structure (all required directories present)
- Validates version.json schema
- Checks CLI installed (`which devforgeai`)
- Verifies critical files exist (commands, skills, protocols)
- Exit code: 0 if valid, 1 if issues found, displays validation report

**Mode 5: Uninstall** (`--mode=uninstall`)
- Creates backup before removal
- Removes .claude/ framework files (preserves user additions if flagged)
- Removes .devforgeai/ framework files (preserves context/, user configs)
- Removes DevForgeAI sections from CLAUDE.md (preserves user sections)
- Uninstalls CLI: `pip uninstall devforgeai-cli`
- Exit code: 0, displays "✅ DevForgeAI uninstalled (backup: {timestamp})"

**And** mode detection: Auto-detects from existing installation state or explicit --mode flag

---

### 6. [ ] Selective Update for Patch/Minor Upgrades (Performance Optimization)

**Given** upgrading from 1.0.0 to 1.0.1 (patch release) with only 5 files changed
**When** installer runs in upgrade mode
**Then** selective update logic activates:
- Computes file changes: Compares checksums between installed and source versions
- Identifies:
  - Modified: 5 files (different checksums)
  - Added: 2 files (new in 1.0.1)
  - Removed: 1 file (deprecated in 1.0.1)
  - Unchanged: 442 files (skip these)
- Creates backup of only 8 files being modified (not all 450)
- Updates only 8 files (5 modified + 2 added + 1 removed)
- Displays: "✅ Updated 8 files (442 unchanged) in 15 seconds"
**And** selective update is 10x faster than full deployment (15s vs 150s)
**And** unchanged file timestamps preserved (no unnecessary touch operations)

---

### 7. [ ] Comprehensive Validation and Error Handling with Rollback on Failure

**Given** installation/upgrade operations can fail (disk full, permissions, corruption)
**When** installer encounters any error during deployment
**Then** error handling activates:
- Error detected (e.g., "Permission denied writing to .claude/commands/")
- Deployment halts immediately (fail-fast, no partial state)
- Error logged with file path, operation, error message
- Automatic rollback initiated:
  - All copied files removed
  - Backup restored (if upgrade) or installation cleaned (if fresh)
  - version.json reverted or removed
- Exit code: 1 (failure)
- Displays: "❌ Installation failed: {error}. Rolled back to previous state. See install.log for details."
**And** project left in valid state (either original installation or clean pre-install)
**And** rollback verified: Original files restored, checksums match backup
**And** user can retry after fixing issue (e.g., `chmod +w .claude/`)

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Worker"
      name: "InstallerCore"
      file_path: "installer/install.py"
      dependencies:
        - "pathlib.Path"
        - "shutil"
        - "json"
        - "datetime"
        - "subprocess"
        - "packaging.version"
      requirements:
        - id: "WKR-001"
          description: "Detect existing installation by checking for .devforgeai/.version.json"
          testable: true
          test_requirement: "Test: Mock .version.json file, verify installer detects and reads version"
          priority: "Critical"

        - id: "WKR-002"
          description: "Compare versions using semantic versioning (major.minor.patch)"
          testable: true
          test_requirement: "Test: Assert compare_versions('1.0.0', '1.0.1') returns 'patch_upgrade'"
          priority: "Critical"

        - id: "WKR-003"
          description: "Create timestamped backup before any modifications"
          testable: true
          test_requirement: "Test: Verify backup directory created with timestamp format YYYYMMDD-HHMMSS"
          priority: "Critical"

        - id: "WKR-004"
          description: "Deploy framework files from src/ to target project"
          testable: true
          test_requirement: "Test: After deployment, verify ~450 files exist in target .claude/ and .devforgeai/"
          priority: "Critical"

        - id: "WKR-005"
          description: "Preserve user configuration files during upgrade"
          testable: true
          test_requirement: "Test: Modify hooks.yaml, run upgrade, verify modification preserved"
          priority: "Critical"

        - id: "WKR-006"
          description: "Write version.json to target with installation metadata"
          testable: true
          test_requirement: "Test: Verify version.json contains version, installed_at timestamp, mode"
          priority: "High"

        - id: "WKR-007"
          description: "Support 5 installation modes (fresh, upgrade, rollback, validate, uninstall)"
          testable: true
          test_requirement: "Test: Run installer with each --mode flag, verify correct behavior"
          priority: "Critical"

        - id: "WKR-008"
          description: "Implement selective update for patch/minor upgrades"
          testable: true
          test_requirement: "Test: Mock 5-file change, verify only 5 files updated (not all 450)"
          priority: "High"

        - id: "WKR-009"
          description: "Auto-rollback on deployment failure (fail-safe operation)"
          testable: true
          test_requirement: "Test: Inject permission error, verify installer rolls back automatically"
          priority: "Critical"

    - type: "Worker"
      name: "VersionDetector"
      file_path: "installer/version.py"
      requirements:
        - id: "WKR-010"
          description: "Read installed version from target .devforgeai/.version.json"
          testable: true
          test_requirement: "Test: get_installed_version(path) returns dict with version, installed_at"
          priority: "Critical"

        - id: "WKR-011"
          description: "Read source version from src/devforgeai/version.json"
          testable: true
          test_requirement: "Test: get_source_version() returns dict with version, release_date"
          priority: "Critical"

        - id: "WKR-012"
          description: "Compare versions using packaging.version for semantic versioning"
          testable: true
          test_requirement: "Test: Verify 1.0.1 > 1.0.0, 1.1.0 > 1.0.5, 2.0.0 > 1.99.99"
          priority: "High"

    - type: "Worker"
      name: "BackupManager"
      file_path: "installer/backup.py"
      requirements:
        - id: "WKR-013"
          description: "Create timestamped backup directory in .backups/"
          testable: true
          test_requirement: "Test: create_backup() returns path like .backups/devforgeai-upgrade-20251117-143000/"
          priority: "Critical"

        - id: "WKR-014"
          description: "Copy .claude/, .devforgeai/, CLAUDE.md to backup using shutil.copytree"
          testable: true
          test_requirement: "Test: Verify backup contains all files (count matches source)"
          priority: "Critical"

        - id: "WKR-015"
          description: "Generate backup manifest.json with metadata and integrity hash"
          testable: true
          test_requirement: "Test: manifest.json contains created_at, files_backed_up, total_size_mb, integrity_hash"
          priority: "High"

        - id: "WKR-016"
          description: "Verify backup integrity (file count, checksums) before proceeding"
          testable: true
          test_requirement: "Test: Backup verification catches corrupted backup (missing files)"
          priority: "Critical"

    - type: "Worker"
      name: "DeploymentEngine"
      file_path: "installer/deploy.py"
      requirements:
        - id: "WKR-017"
          description: "Deploy src/claude/ to target .claude/ with exclusion patterns"
          testable: true
          test_requirement: "Test: Verify ~370 files deployed, 60 excluded (*.backup*, __pycache__)"
          priority: "Critical"

        - id: "WKR-018"
          description: "Deploy src/devforgeai/ to target .devforgeai/ (config, docs, protocols, tests only)"
          testable: true
          test_requirement: "Test: Verify ~80 files deployed, generated dirs excluded (qa/reports, RCA, adrs)"
          priority: "Critical"

        - id: "WKR-019"
          description: "Set executable permissions on .sh and CLI scripts"
          testable: true
          test_requirement: "Test: stat -c %a .claude/scripts/install_hooks.sh returns 755"
          priority: "High"

        - id: "WKR-020"
          description: "Preserve user configs (hooks.yaml, feedback config, context files)"
          testable: true
          test_requirement: "Test: User config file timestamps unchanged after deployment"
          priority: "Critical"

    - type: "Worker"
      name: "RollbackManager"
      file_path: "installer/rollback.py"
      requirements:
        - id: "WKR-021"
          description: "List available backups sorted by timestamp (newest first)"
          testable: true
          test_requirement: "Test: list_backups() returns array of backup dirs sorted descending"
          priority: "High"

        - id: "WKR-022"
          description: "Verify backup integrity before restoring (manifest validation)"
          testable: true
          test_requirement: "Test: Corrupted backup detected (file count mismatch), rollback aborts"
          priority: "Critical"

        - id: "WKR-023"
          description: "Restore all files from backup (complete state restoration)"
          testable: true
          test_requirement: "Test: After rollback, checksums match original pre-upgrade state (100%)"
          priority: "Critical"

        - id: "WKR-024"
          description: "Revert version.json to backup version"
          testable: true
          test_requirement: "Test: version.json version field reverts from 1.0.1 to 1.0.0"
          priority: "High"

    - type: "Worker"
      name: "ValidationEngine"
      file_path: "installer/validate.py"
      requirements:
        - id: "WKR-025"
          description: "Validate directory structure (all required directories present)"
          testable: true
          test_requirement: "Test: Check .claude/skills/, .claude/agents/, .devforgeai/protocols/ exist"
          priority: "Critical"

        - id: "WKR-026"
          description: "Validate version.json schema and consistency"
          testable: true
          test_requirement: "Test: version.json validates against JSON schema, version matches deployment"
          priority: "High"

        - id: "WKR-027"
          description: "Validate CLI installed and accessible (which devforgeai)"
          testable: true
          test_requirement: "Test: subprocess.run(['which', 'devforgeai']) returns exit 0"
          priority: "High"

        - id: "WKR-028"
          description: "Validate critical files exist (skills, commands, protocols)"
          testable: true
          test_requirement: "Test: Check 25 critical files exist (11 commands, 10 skills, 3 protocols, 1 CLAUDE.md)"
          priority: "Critical"

  business_rules:
    - id: "BR-001"
      rule: "Backup must complete successfully before any file modifications (atomic transaction)"
      test_requirement: "Test: Simulate backup failure, verify deployment never starts"

    - id: "BR-002"
      rule: "User configs must NEVER be overwritten (explicit preservation list)"
      test_requirement: "Test: Verify hooks.yaml, feedback config, context files unchanged after upgrade"

    - id: "BR-003"
      rule: "Version downgrades require explicit --force flag (safety check)"
      test_requirement: "Test: Attempt 1.0.1 → 1.0.0 without --force, installer aborts with warning"

    - id: "BR-004"
      rule: "Deployment failure triggers automatic rollback (no partial installs)"
      test_requirement: "Test: Kill installer mid-deployment, verify automatic cleanup or rollback"

    - id: "BR-005"
      rule: "Major version upgrades warn about breaking changes (require user confirmation)"
      test_requirement: "Test: Upgrade 1.x → 2.0, installer displays breaking changes warning, requires 'yes' confirmation"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Fresh installation completes quickly"
      metric: "< 3 minutes for ~450 file deployment"
      test_requirement: "Test: time python installer/install.py, assert <180s"

    - id: "NFR-002"
      category: "Performance"
      requirement: "Selective update faster than full deployment"
      metric: "< 30 seconds for 10-file patch upgrade"
      test_requirement: "Test: Mock 10-file change, time upgrade, assert <30s"

    - id: "NFR-003"
      category: "Performance"
      requirement: "Backup creation efficient"
      metric: "< 20 seconds to backup 450 files (~15 MB)"
      test_requirement: "Test: time create_backup(), assert <20s"

    - id: "NFR-004"
      category: "Reliability"
      requirement: "Atomic operations with fail-safe rollback"
      metric: "0 partial installations (either complete or fully rolled back)"
      test_requirement: "Test: Simulate 5 failure scenarios, verify clean state after each"

    - id: "NFR-005"
      category: "Reliability"
      requirement: "Idempotent installations"
      metric: "Running installer twice produces identical result, 0 errors"
      test_requirement: "Test: Install twice, verify same state, second run reports 'Already at version X'"

    - id: "NFR-006"
      category: "Security"
      requirement: "No sudo/elevated permissions required"
      metric: "Installer runs with standard user permissions"
      test_requirement: "Test: Run as non-root user, completes successfully"

    - id: "NFR-007"
      category: "Usability"
      requirement: "Clear progress reporting during operations"
      metric: "Progress updates every 10% of operation (Deploying 45/450 files - 10%)"
      test_requirement: "Test: Capture stdout, verify progress messages at 10%, 20%, ..., 100%"
```

### Dependencies

**External:**
- Python 3.8+ with pathlib, shutil, json, subprocess
- packaging library (pip install packaging) for semantic versioning
- Git (for validating project repository)
- pip (for CLI installation)

**Internal:**
- STORY-042 complete (src/ must be populated with framework files)

---

## Edge Cases

### 1. Disk Space Insufficient for Backup
**Scenario:** Target project disk has <20 MB free, backup requires 15 MB
**Expected:** Pre-flight check detects insufficient space, aborts with error: "Insufficient disk space: 15 MB required for backup, 8 MB available. Free space and retry."
**Handling:** Check available disk space before backup creation

### 2. Existing Installation Corrupted (Missing version.json)
**Scenario:** `.claude/` exists but `.devforgeai/.version.json` missing or invalid
**Expected:** Installer detects corruption, prompts user: "Corrupted installation detected. (1) Repair (fresh install), (2) Backup and clean install, (3) Abort"
**Handling:** Validate installation state, offer repair options

### 3. Network Interruption During pip install (CLI Installation)
**Scenario:** `pip install -e .claude/scripts/` fails due to network timeout
**Expected:** Installer reports CLI installation failed (non-blocking), framework files deployed successfully, user can manually run pip install later
**Handling:** Try-catch on pip install, continue on failure, add to post-install checklist

### 4. Concurrent Installer Executions (Multiple Terminals)
**Scenario:** User runs installer in two terminals simultaneously on same project
**Expected:** Second instance detects lock file (`.devforgeai/.install.lock`), aborts with: "Installation in progress (PID 1234). Wait or kill process."
**Handling:** Create lock file at start, remove on completion/failure

### 5. Version.json Schema Change Between Versions
**Scenario:** Upgrading from 1.0 (old schema) to 1.1 (new schema with additional fields)
**Expected:** Installer detects schema difference, migrates old schema to new schema (adds default values for new fields), logs migration
**Handling:** Schema version field in version.json, migration functions per schema version

### 6. Symlink Preservation During Deployment
**Scenario:** Target .claude/ has symlink (.claude/skills/shared → ../common)
**Expected:** Installer detects symlink, prompts: "(1) Follow and copy target, (2) Preserve symlink, (3) Skip this file"
**Handling:** Default: Follow symlinks during deployment (rsync -L)

### 7. Large Backup Accumulation Over Time
**Scenario:** After 20 upgrades, `.backups/` contains 20 directories (300 MB)
**Expected:** Installer warns if >10 backups or >100 MB: "10 backups found (250 MB). Clean old backups with: rm -rf .backups/devforgeai-*-202501*"
**Handling:** Display backup count/size, suggest cleanup (not automatic - user decides)

---

## Data Validation Rules

1. **Version format:** Must match `^\d+\.\d+\.\d+$` (semantic versioning)

2. **Backup manifest:** Must contain 7 required fields (created_at, reason, from_version, to_version, files_backed_up, total_size_mb, integrity_hash)

3. **Installation mode:** Must be one of: fresh_install, patch_upgrade, minor_upgrade, major_upgrade, reinstall, downgrade

4. **File count variance:** Deployed file count must be within ±10 of expected (450 ±10)

5. **Checksum algorithm:** Use SHA256 (64-character hex), verify 100% match on rollback

6. **Preserved files list:** Must include hooks.yaml, feedback config, all .devforgeai/context/*.md files

7. **Exclusion patterns:** Must match .gitignore-style syntax, validate before deployment

---

## Non-Functional Requirements

### Performance
- Fresh install: <3 minutes for 450 files
- Selective update: <30 seconds for 10-file patch
- Backup creation: <20 seconds for 450 files
- Rollback: <45 seconds to restore from backup

### Reliability
- Atomic operations: All-or-nothing deployment
- Fail-safe rollback: Auto-rollback on any error
- Idempotent: Safe to run multiple times
- Lock file: Prevents concurrent executions

### Security
- User permissions only (no sudo)
- Backup isolation (.backups/ gitignored)
- No hardcoded paths (all configurable)
- Input validation (prevent path traversal)

### Usability
- Progress reporting: Updates every 10%
- Clear error messages: Actionable fix suggestions
- Dry-run mode: Preview without changes
- Verbose mode: Detailed logging for debugging

---

## Definition of Done

### Implementation
- [ ] installer/install.py created (300-400 lines)
- [ ] installer/version.py created (version detection)
- [ ] installer/backup.py created (backup management)
- [ ] installer/deploy.py created (deployment engine)
- [ ] installer/rollback.py created (rollback manager)
- [ ] installer/validate.py created (validation engine)
- [ ] installer/config.yaml created (configuration)
- [ ] All 5 modes implemented (fresh, upgrade, rollback, validate, uninstall)

### Quality
- [ ] All 7 acceptance criteria validated
- [ ] All 5 business rules enforced
- [ ] All 7 NFRs met and measured
- [ ] All 7 edge cases handled
- [ ] 20+ unit tests passing
- [ ] 5 integration tests passing (one per mode)

### Testing
- [ ] Unit tests: Version detection (5 tests)
- [ ] Unit tests: Backup creation (5 tests)
- [ ] Unit tests: Deployment (5 tests)
- [ ] Unit tests: Rollback (5 tests)
- [ ] Integration test: Fresh install workflow
- [ ] Integration test: Upgrade workflow
- [ ] Integration test: Rollback workflow
- [ ] Integration test: Validate mode
- [ ] Integration test: Uninstall workflow
- [ ] Edge case tests: 7 scenarios

### Documentation
- [ ] installer/README.md with usage examples
- [ ] API documentation for all 5 modes
- [ ] Troubleshooting guide
- [ ] EPIC-009 updated (Phase 5 complete)
- [ ] STORY-046 unblocked (installer ready for CLAUDE.md merge)

### Release Readiness
- [ ] Git commit with installer code
- [ ] Installer tested on copy of DevForgeAI2
- [ ] All modes validated (5/5 working)
- [ ] Ready for STORY-046 (CLAUDE.md merge integration)

---

## Workflow History

- **2025-11-16:** Story created for EPIC-009 Phase 5 (installer core algorithm)
- **2025-11-16:** Priority: High, Points: 13 (complex version-aware installer)
- **2025-11-16:** Can work in parallel with STORY-043, 044 (independent development)
- **2025-11-16:** Blocks STORY-046, 047, 048 (all need installer)
- **2025-11-16:** Status: Backlog (can start after STORY-042)
