# Backup Management Guide

**Version:** 1.0.0 (STORY-080)
**Last Updated:** 2025-12-06

## Overview

DevForgeAI automatically manages backups of your installation for safety during upgrades and to enable rollback functionality.

**Backup system components:**
- BackupService (STORY-078) - Creates backups
- BackupSelector (STORY-080) - Lists and selects backups
- BackupCleaner (STORY-080) - Manages retention policy

---

## Backup Location

**Default directory:** `.devforgeai/backups/`

**Backup format:** `v{version}-{timestamp}/`

**Example:**
```
.devforgeai/backups/
├── v1.0.5-20251206-143000/
│   ├── .claude/
│   ├── .devforgeai/
│   ├── CLAUDE.md
│   ├── metadata.json
│   └── manifest.json
├── v1.0.4-20251205-101500/
└── v1.0.3-20251204-084500/
```

---

## Automatic Backup Creation

**Backups are created automatically during:**

1. **Upgrades** (STORY-078)
   - Before any files are modified
   - Reason: "UPGRADE"
   - Contains complete framework state

2. **Manual rollback** (STORY-080)
   - Before restoring old backup (safety backup)
   - Reason: "MANUAL"
   - Ensures you can rollback the rollback

**Not created during:**
- Fresh installations (nothing to backup)
- Failed installations (installation never started)

---

## Backup Contents

**What IS backed up:**
- `.claude/` - All skills, subagents, commands, memory files
- `.devforgeai/` - Framework context files, protocols, templates
- `CLAUDE.md` - Project instructions

**What is NOT backed up:**
- `.ai_docs/Stories/` - User stories (preserved separately)
- `.ai_docs/Epics/` - Epic documents (preserved separately)
- `.devforgeai/backups/` - Old backups (no recursive backup)
- `.git/` - Git repository
- `__pycache__/`, `.pytest_cache/` - Build artifacts
- `node_modules/`, `.venv/` - Dependencies

**Rationale:** User-created content is never overwritten during upgrades, so doesn't need backup by default.

---

## Backup Metadata

**metadata.json structure:**
```json
{
  "id": "v1.0.5-20251206-143000",
  "version": "1.0.5",
  "timestamp": "2025-12-06T14:30:00",
  "size_bytes": 47185920,
  "reason": "UPGRADE"
}
```

**manifest.json structure:**
```json
{
  "version": "1.0.5",
  "created_at": "2025-12-06T14:30:00",
  "files": {
    ".claude/skills/devforgeai-development/SKILL.md": {
      "checksum": "a3b2c1...",
      "size": 45230
    }
  }
}
```

**Checksums:** SHA256 hex digest (64 characters)

---

## Listing Backups

**Using BackupSelector:**

```python
from installer.backup_selector import BackupSelector
from pathlib import Path

selector = BackupSelector(backup_dir=Path(".devforgeai/backups"))
backups = selector.list()

print(f"Found {len(backups)} backup(s):\n")

for backup in backups:
    formatted = selector.format_for_display(backup)
    print(formatted)
```

**Output:**
```
Found 3 backup(s):

v1.0.5 - 2025-12-06 14:30:00 - 45 MB - UPGRADE - .devforgeai/backups/v1.0.5-20251206-143000
v1.0.4 - 2025-12-05 10:15:00 - 43 MB - UPGRADE - .devforgeai/backups/v1.0.4-20251205-101500
v1.0.3 - 2025-12-04 08:45:00 - 42 MB - MANUAL - .devforgeai/backups/v1.0.3-20251204-084500
```

**Sort order:** Newest first (by timestamp)

---

## Backup Retention Policy

**Default retention:** 5 backups (keeps 5 most recent)

**Cleanup behavior:**
- Runs automatically after successful rollback
- Deletes oldest backups first
- Never deletes backup being restored
- Only runs after successful rollback (not after failures)

**Configuration:** `.devforgeai/config/rollback-config.json`

```json
{
  "backup_retention_count": 5
}
```

**Valid range:** 1-20 backups

**Examples:**
- `backup_retention_count: 1` - Keep only newest backup
- `backup_retention_count: 5` - Keep 5 most recent (default)
- `backup_retention_count: 20` - Keep 20 backups (maximum)

---

## Manual Cleanup

**Using BackupCleaner:**

```python
from installer.backup_cleaner import BackupCleaner
from pathlib import Path

cleaner = BackupCleaner(
    backup_dir=Path(".devforgeai/backups"),
    retention_count=5
)

result = cleaner.cleanup()

print(f"Deleted {result.deleted_count} backup(s)")
print(f"Deleted IDs: {result.deleted_backup_ids}")
```

**Example output:**
```
Deleted 2 backup(s)
Deleted IDs: ['v1.0.1-20251201-120000', 'v1.0.0-20251130-090000']
```

---

## Backup Size Estimation

**Typical backup sizes:**

| Installation Type | Approximate Size |
|-------------------|------------------|
| Minimal (skills only) | 25-35 MB |
| Standard (skills + memory) | 40-50 MB |
| Complete (all features) | 55-70 MB |

**Size depends on:**
- Number of skills installed
- Reference documentation size
- Memory files present
- Custom subagents added

**Disk space required:**
- 5 backups × 50 MB average = 250 MB
- Recommended: 500 MB free disk space

---

## Backup Integrity Verification

**Checksums verified during:**
- Restoration (BackupRestorer)
- Post-rollback validation (RollbackValidator)

**Algorithm:** SHA256
**Chunk size:** 64 KB (CHECKSUM_CHUNK_SIZE = 65536)

**Checksum verification:**
```python
from installer.rollback_validator import RollbackValidator
from pathlib import Path
import json

validator = RollbackValidator(logger=logger)

# Load backup manifest
with open(".devforgeai/backups/v1.0.5-20251206-143000/manifest.json") as f:
    manifest = json.load(f)

# Validate restored files
report = validator.validate(
    restored_dir=Path("."),
    backup_manifest=manifest
)

print(f"Validation: {'PASSED' if report.passed else 'FAILED'}")
print(f"Files verified: {report.verified_files}")
print(f"Critical files: {'Present' if report.critical_files_present else 'Missing'}")
```

---

## User Content Preservation

**Default behavior:** User content is NEVER overwritten during rollback

**Preserved paths:**
- `.ai_docs/Stories/` - User stories you created
- `.ai_docs/Epics/` - Epic documents
- `.ai_docs/Sprints/` - Sprint plans
- `.devforgeai/context/` - Your custom context files
- `.devforgeai/adrs/` - Your architecture decisions

**Override behavior:**
```python
request = RollbackRequest(
    backup_id="v1.0.5-20251206-143000",
    include_user_content=True  # Restores user content from backup
)
```

**Warning:** Only use `include_user_content=True` if you want to restore old versions of your stories/epics.

---

## Backup Reasons

**Three backup types:**

### UPGRADE
- Created before framework upgrade
- Contains pre-upgrade state
- Used for automatic rollback on upgrade failure

### MANUAL
- Created when user initiates manual rollback
- Safety backup of current state before restoration
- Allows rolling back the rollback

### UNINSTALL
- Created before uninstallation (STORY-070)
- Allows re-installation without losing configuration
- Not implemented in STORY-080

---

## Configuration File

**Location:** `.devforgeai/config/rollback-config.json`

**Full configuration:**
```json
{
  "backup_retention_count": 5,
  "user_content_paths": [
    ".ai_docs/Stories/",
    ".ai_docs/Epics/",
    ".ai_docs/Sprints/",
    ".devforgeai/context/",
    ".devforgeai/adrs/"
  ],
  "validate_after_rollback": true
}
```

**Options:**

- `backup_retention_count` (int, 1-20, default: 5)
  - How many backups to keep
  - Oldest deleted automatically

- `user_content_paths` (array of strings)
  - Paths to preserve during rollback
  - Default list covers all user-created content

- `validate_after_rollback` (boolean, default: true)
  - Whether to run validation after rollback
  - Set to false to skip validation (not recommended)

---

## Troubleshooting

### "No backups found"

**Cause:** No backups in `.devforgeai/backups/` directory

**Solution:**
- Check if directory exists
- Verify you've performed at least one upgrade (creates first backup)
- Check backup retention hasn't deleted all backups

---

### "Backup validation failed"

**Cause:** Checksums don't match or critical files missing

**Solution:**
- Check backup manifest.json for expected checksums
- Verify backup directory not corrupted
- Try different backup if available
- Check .devforgeai/logs/rollback-*.log for details

---

### "Permission denied during restore"

**Cause:** Target files not writable

**Solution:**
- Check file permissions on installation directory
- Ensure you have write access
- Close any programs using framework files
- Run with appropriate permissions

---

### "Cleanup deleted wrong backup"

**Prevention:** Backup being restored is automatically excluded from cleanup

**Verification:**
```python
cleaner = BackupCleaner(
    backup_dir=backup_dir,
    retention_count=5,
    cleanup_excluded_backup_id="v1.0.5-20251206-143000"  # Protected
)
```

**The cleanup_excluded_backup_id is set automatically by RollbackOrchestrator.**

---

## API Reference

### BackupSelector

**Methods:**
- `list() -> List[BackupInfo]` - Lists all backups sorted by date
- `format_for_display(backup_info: BackupInfo) -> str` - Formats backup for display
- `select(backup_id: str) -> Optional[BackupInfo]` - Selects backup by ID

### BackupRestorer

**Methods:**
- `restore(backup_dir: Path, target_dir: Path, include_user_content: bool = False) -> RestoreResult`

**Returns:**
- RestoreResult with files_restored, files_preserved, checksums_verified, error

### BackupCleaner

**Methods:**
- `cleanup(skip_if_condition_met: bool = False, condition_met: bool = None) -> CleanupResult`

**Returns:**
- CleanupResult with deleted_count, deleted_backup_ids

### RollbackValidator

**Methods:**
- `validate(restored_dir: Path, backup_manifest: dict) -> RollbackValidationReport`

**Returns:**
- RollbackValidationReport with passed, verified_files, critical_files_present, validation_details, error

### RollbackOrchestrator

**Methods:**
- `execute(request: RollbackRequest) -> RollbackResult`

**Returns:**
- RollbackResult with status, from_version, to_version, files_restored, files_preserved, validation_passed, duration_seconds

---

## Implementation Notes

**Created:** STORY-080 (2025-12-06)
**Test Coverage:** 60/61 unit tests passing, 8/8 integration tests passing
**Code Quality:** Production ready (code review PASS)
**Performance:** Verified <60s for standard installations

**Related Stories:**
- STORY-078: Upgrade Mode (creates backups)
- STORY-079: Fix/Repair Mode (validation patterns)
