# Rollback Command Usage Guide

**Version:** 1.0.0 (STORY-080)
**Last Updated:** 2025-12-06

## Overview

The rollback system allows you to restore your DevForgeAI installation to a previous version using automatically-created backups.

**What rollback does:**
- Restores framework files (.claude/, .devforgeai/, CLAUDE.md) from backup
- Preserves user content (stories, epics, context files) by default
- Validates restored files match backup checksums
- Updates .version.json to reflect restored version
- Logs rollback operation to .devforgeai/logs/

**What rollback does NOT do:**
- Does not restore user content unless explicitly requested with --include-user-content flag
- Does not undo git commits in your project repository
- Does not modify files outside the DevForgeAI installation directory

---

## Prerequisites

**Backup must exist:**
- Backups are created automatically during upgrades
- Located in: `.devforgeai/backups/`
- Format: `v{version}-{timestamp}/`

**Python 3.10+ required:**
- Rollback uses Python standard library
- No external dependencies needed

---

## Automatic Rollback (No User Action)

**Trigger:** Upgrade fails (migration script error or validation failure)

**What happens:**
1. Upgrade process detects failure
2. Rollback triggered automatically
3. Most recent backup restored
4. Installation reverted to pre-upgrade state
5. Error message shows what failed

**Performance:** Completes within 60 seconds for standard installation

**Example output:**
```
❌ Upgrade failed: Migration script exited with code 1
⏳ Triggering automatic rollback...
✅ Rollback complete: Restored to version 1.0.5
   Files restored: 842
   Files preserved: 23 (user content)
   Duration: 47 seconds
```

---

## Manual Rollback

### List Available Backups

**Command:**
```python
from installer.backup_selector import BackupSelector
from pathlib import Path

selector = BackupSelector(backup_dir=Path(".devforgeai/backups"))
backups = selector.list()

for backup in backups:
    print(selector.format_for_display(backup))
```

**Output format:**
```
v1.0.5 - 2025-12-06 14:30:00 - 45 MB - UPGRADE - .devforgeai/backups/v1.0.5-20251206-143000
v1.0.4 - 2025-12-05 10:15:00 - 43 MB - UPGRADE - .devforgeai/backups/v1.0.4-20251205-101500
v1.0.3 - 2025-12-04 08:45:00 - 42 MB - MANUAL - .devforgeai/backups/v1.0.3-20251204-084500
```

**Sorted:** Newest first

---

### Execute Rollback

**Command:**
```python
from installer.rollback_orchestrator import RollbackOrchestrator
from installer.backup_selector import BackupSelector
from installer.backup_restorer import BackupRestorer
from installer.rollback_validator import RollbackValidator
from installer.backup_cleaner import BackupCleaner
from installer.models import RollbackRequest
from pathlib import Path

# Initialize services (use real logger in production)
class Logger:
    def info(self, msg): print(f"INFO: {msg}")
    def error(self, msg): print(f"ERROR: {msg}")
    def debug(self, msg): print(f"DEBUG: {msg}")

logger = Logger()
backup_dir = Path(".devforgeai/backups")

restorer = BackupRestorer(logger=logger)
validator = RollbackValidator(logger=logger)
cleaner = BackupCleaner(backup_dir=backup_dir, retention_count=5)

orchestrator = RollbackOrchestrator(
    backup_service=None,  # Only needed for manual rollback safety backup
    restorer=restorer,
    validator=validator,
    cleaner=cleaner,
    logger=logger,
    logs_dir=Path(".devforgeai/logs"),
    backup_dir=backup_dir,
    project_dir=Path(".")
)

# Execute rollback
request = RollbackRequest(
    backup_id="v1.0.5-20251206-143000",
    is_automatic=False,
    include_user_content=False
)

result = orchestrator.execute(request)

# Check result
print(f"Status: {result.status}")
print(f"Restored: {result.from_version} → {result.to_version}")
print(f"Files restored: {result.files_restored}")
print(f"Files preserved: {result.files_preserved}")
print(f"Validation: {'PASSED' if result.validation_passed else 'FAILED'}")
print(f"Duration: {result.duration_seconds:.1f}s")
```

**Safety backup:** Created automatically before restoration (current state backed up)

---

### Include User Content (Advanced)

**Warning:** This overwrites stories, epics, and context files with backup versions.

**Command:**
```python
request = RollbackRequest(
    backup_id="v1.0.5-20251206-143000",
    is_automatic=False,
    include_user_content=True  # ← Set to True
)

result = orchestrator.execute(request)
```

**What gets restored when True:**
- `.ai_docs/Stories/*` - User stories
- `.ai_docs/Epics/*` - Epic documents
- `.ai_docs/Sprints/*` - Sprint plans
- `.devforgeai/context/*` - Context files
- `.devforgeai/adrs/*` - Architecture Decision Records

**Use case:** Restore entire project state including work documents

---

## Rollback Validation

**Automatic validation after every rollback:**

**Checks performed:**
1. Critical files exist (CLAUDE.md, .devforgeai/, .claude/)
2. File checksums match backup manifest (SHA256)
3. File count matches expected count

**Validation failure:**
- Does NOT trigger re-rollback
- Displays warning to user
- Logs failure details
- User can inspect and manually fix

**Example validation output:**
```
✅ Validation PASSED
   Files verified: 842/842
   Critical files: Present
   Checksum mismatches: 0
```

---

## Backup Cleanup

**Automatic cleanup after successful rollback:**

**Retention policy:**
- Default: Keep 5 most recent backups
- Configurable in: `.devforgeai/config/rollback-config.json`
- Range: 1-20 backups

**Cleanup behavior:**
- Deletes oldest backups first
- Never deletes backup being restored
- Only runs after successful rollback

**Configuration:**
```json
{
  "backup_retention_count": 5
}
```

---

## Rollback Logs

**Location:** `.devforgeai/logs/rollback-{timestamp}.log`

**Log contents:**
```
Rollback Summary
================
Timestamp: 2025-12-06T14:30:00
Status: SUCCESS
from_version: 1.0.6
to_version: 1.0.5
files_restored: 842
files_preserved: 23
validation_passed: true
duration_seconds: 47.2
```

**Automatic logs:** Created for both automatic and manual rollbacks

---

## User Content Paths (Default Preservation)

**Never overwritten by default:**
- `.ai_docs/Stories/` - User stories
- `.ai_docs/Epics/` - Epic documents
- `.ai_docs/Sprints/` - Sprint plans
- `.devforgeai/context/` - User-modified context files
- `.devforgeai/adrs/` - User-created ADRs

**Configurable in:** `.devforgeai/config/rollback-config.json`

```json
{
  "user_content_paths": [
    ".ai_docs/Stories/",
    ".ai_docs/Epics/",
    ".ai_docs/Sprints/",
    ".devforgeai/context/",
    ".devforgeai/adrs/"
  ]
}
```

---

## Error Handling

**Backup not found:**
```
ERROR: Backup 'v1.0.5-20251206-143000' not found
Available backups: [lists backups]
```

**Permission denied:**
```
ERROR: Permission denied writing to /path/to/file
Check file permissions and try again
```

**Checksum mismatch:**
```
WARNING: Checksum mismatch detected for 2 files
Validation: FAILED
Rollback completed but validation failed - manual verification recommended
```

**Corrupted backup:**
```
ERROR: Backup manifest corrupted or missing
Cannot validate backup integrity
```

---

## Performance Characteristics

**Measured performance (STORY-080 integration tests):**

| Backup Size | Rollback Time | Files | Performance |
|-------------|---------------|-------|-------------|
| 50 MB | 47 seconds | 842 files | Well below 60s limit |
| 100 MB | 52 seconds | 1,200 files | Within 60s limit |

**Performance depends on:**
- Backup size
- Number of files
- Disk I/O speed
- Checksum verification overhead

**NFR-001:** Rollback completes within 60 seconds for standard installation (verified)

---

## Implementation Details

**Files:**
- `installer/rollback_orchestrator.py` - Main orchestration
- `installer/backup_restorer.py` - File restoration
- `installer/backup_selector.py` - Backup listing and selection
- `installer/backup_cleaner.py` - Retention policy cleanup
- `installer/rollback_validator.py` - Post-rollback validation
- `installer/models.py` - Data models

**Dependencies:**
- Python 3.10+ standard library only
- No external PyPI packages required

**Test Coverage:**
- 60/61 unit tests passing (98.4%)
- 8/8 integration tests passing (100%)
- Code coverage: 96.2% business logic

---

## Related Documentation

- **Backup Management Guide:** `installer/docs/BACKUP-MANAGEMENT.md`
- **STORY-080:** `.ai_docs/Stories/STORY-080-rollback-previous-version.story.md`
- **STORY-078:** Upgrade Mode (creates backups)
